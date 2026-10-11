"""Adversarial item-export checks. These test code, not model or host behavior."""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
import zipfile

KIT = Path(__file__).resolve().parents[1]
EXPORTER = KIT / "setup/export_item.py"
ITEM = "SYNTHETIC-FINANCE-01"
REVISION = "r01"


class Blocked(Exception):
    pass


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def fixture(base):
    root = base / "item"
    payload = {
        "README.md": "# Synthetic item\n[Start](PROJECT_INSTRUCTIONS.md). [State](context/00.md). [Brief](deliverables/brief.md). [Method](methods/SKILL.md).\n",
        "PROJECT_INSTRUCTIONS.md": "# Scope\nOnly SYNTHETIC-FINANCE-01 r01. Read [state](context/00.md) and [method](methods/SKILL.md). Do not publish or install.\n",
        "context/00.md": "# SYNTHETIC-FINANCE-01\nGoverning revision: r01. Canonical owner: Blitz. Source: [costs](../sources/costs.csv).\n",
        "deliverables/brief.md": "# Brief\nSynthetic total USD 12. [Evidence](../sources/costs.csv).\n",
        "sources/costs.csv": "component,usd\nsynthetic,12\n",
        "methods/SKILL.md": "# Method\nRead [check](references/check.md) and retain [license](LICENSE.md).\n",
        "methods/references/check.md": "# Check\nRecompute from the included source; preserve scope.\n",
        "methods/LICENSE.md": "Synthetic fixture only, released for this test.\n",
    }
    dependencies = {
        "README.md": ["PROJECT_INSTRUCTIONS.md", "context/00.md", "deliverables/brief.md", "methods/SKILL.md"],
        "PROJECT_INSTRUCTIONS.md": ["context/00.md", "methods/SKILL.md"],
        "context/00.md": ["sources/costs.csv"],
        "deliverables/brief.md": ["sources/costs.csv"],
        "methods/SKILL.md": ["methods/references/check.md", "methods/LICENSE.md"],
    }
    rows = []
    for name, content in payload.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        role = "license" if name.endswith("LICENSE.md") else "method" if name.startswith("methods/") else "source" if name.startswith("sources/") else "deliverable" if name.startswith("deliverables/") else "record"
        rows.append({"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "revision": REVISION, "classification": "permitted", "role": role, "dependencies": dependencies.get(name, [])})
    contract = {"schema_version": 1, "item_id": ITEM, "revision": REVISION, "blitz_version": "1.5OAI", "destination": "controlled-receiver", "review": {"reviewed_by": "synthetic-independent-test", "approved_for_export": True, "dependency_review_complete": True}, "required_paths": ["README.md", "PROJECT_INSTRUCTIONS.md", "context/00.md", "deliverables/brief.md"], "files": rows, "prerequisites": [], "reference_exceptions": []}
    return root, contract


def invoke(*args):
    p = subprocess.run([sys.executable, str(EXPORTER), *map(str, args)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    return {"exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def build(base, root, contract, revision=REVISION, output=None):
    config = base / "contract.json"
    config.write_text(json.dumps(contract, indent=2), encoding="utf-8")
    output = output or base / "item.zip"
    return output, invoke("build", "--root", root, "--contract", config, "--output", output, "--expected-revision", revision)


def inspect(path, revision=REVISION, item=ITEM):
    return invoke("inspect", path, "--expected-item-id", item, "--expected-revision", revision)


def rejected(base, root, contract, revision=REVISION):
    output, result = build(base, root, contract, revision)
    check(result["exit"] != 0, "Unsafe contract was accepted: " + json.dumps(result))
    check(not output.exists(), "Rejected build left a destination archive")
    return result


def replace_file(root, contract, name, content):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    row = next(r for r in contract["files"] if r["path"] == name)
    row["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()


def rewrite_zip(source, target, mutation):
    with zipfile.ZipFile(source) as z:
        entries = [(info, z.read(info.filename)) for info in z.infolist()]
    entries = mutation(entries)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for info, data in entries:
            z.writestr(info, data)


def manifest_mutation(entries, change):
    found = 0
    for index, (info, content) in enumerate(entries):
        if Path(info.filename).name == "manifest.json":
            manifest = json.loads(content)
            change(manifest)
            entries[index] = (info, json.dumps(manifest).encode())
            found += 1
    check(found == 1, "Expected exactly one manifest")
    return entries


def run_case(name, mutation=None, mode="reject"):
    with tempfile.TemporaryDirectory(prefix="blitz-export-eval-") as directory:
        base = Path(directory)
        root, contract = fixture(base)
        if mutation:
            mutation(base, root, contract)
        if mode in {"reparse_guard", "atomic_failure"} or mode.startswith("path_guard:"):
            spec = importlib.util.spec_from_file_location("blitz_export_eval_target", EXPORTER)
            module = importlib.util.module_from_spec(spec)
            old_bytecode_setting = sys.dont_write_bytecode
            try:
                sys.dont_write_bytecode = True
                spec.loader.exec_module(module)
            finally:
                sys.dont_write_bytecode = old_bytecode_setting
            if mode == "atomic_failure":
                config = base / "contract.json"
                config.write_text(json.dumps(contract), encoding="utf-8")
                output = base / "item.zip"
                with patch.object(module.os, "link", side_effect=OSError("injected publication failure")):
                    try:
                        module.build_archive(root, config, output, REVISION)
                    except OSError:
                        check(not output.exists(), "Failed atomic publication left output")
                        check(not list(base.glob(".item-export-*.zip")), "Failed publication left temporary archive")
                        check((root / "README.md").is_file(), "Failed publication damaged source")
                        return {"mode": "injected_atomic_publication_failure", "cleanup": "No archive or temporary ZIP remains; source remains."}
                    raise AssertionError("Atomic publication failure was swallowed")
            if mode.startswith("path_guard:"):
                try:
                    module.safe_path(mode.split(":", 1)[1])
                except ValueError:
                    return {"mode": "direct_unsafe_path_guard"}
                raise AssertionError("Unsafe Windows path accepted by path guard")
            target = root / "sources/costs.csv"
            original = Path.lstat
            def attributes(path, *args, **kwargs):
                if path == target:
                    return SimpleNamespace(st_mode=stat.S_IFREG | 0o644, st_file_attributes=0x400)
                return original(path, *args, **kwargs)
            with patch.object(Path, "lstat", attributes):
                try:
                    module.no_links(target)
                except ValueError:
                    return {"mode": "injected_lstat_reparse_flag", "limit": "Guard branch checked; not a native Windows reparse filesystem test."}
                raise AssertionError("Reparse attribute was accepted")
        if mode == "reject":
            return rejected(base, root, contract)
        archive, result = build(base, root, contract)
        check(result["exit"] == 0 and archive.is_file(), "Normal build failed: " + json.dumps(result))
        if mode == "pass":
            verified = inspect(archive)
            check(verified["exit"] == 0, "Normal inspect failed: " + json.dumps(verified))
            with zipfile.ZipFile(archive) as z:
                names = z.namelist()
                manifest = json.loads(z.read("manifest.json"))
                check(manifest["external_access_required"] is any(p["required"] for p in contract["prerequisites"]), "External access requirement was mislabeled")
                declared = {r["path"]: r for r in contract["files"]}
                check(all(row["revision"] == declared[row["path"]]["revision"] for row in manifest["files"]), "Pinned source revisions were changed")
                check(len(names) == len(contract["files"]) + 1, "Archive includes unselected files or omits payload")
                for row in contract["files"]:
                    matches = [n for n in names if n == row["path"] or n.endswith("/" + row["path"])]
                    check(len(matches) == 1, "Allowlisted file missing or duplicated: " + row["path"])
                    check(z.read(matches[0]) == (root / row["path"]).read_bytes(), "Payload differs from selected bytes")
            return {"build": result, "inspect": verified}
        if mode == "no_overwrite":
            previous = archive.read_bytes()
            _, second = build(base, root, contract)
            check(second["exit"] != 0, "Existing output overwritten or silently accepted")
            check(archive.read_bytes() == previous, "Existing output bytes changed")
            return second
        if mode == "stale_build":
            return rejected(base, root, contract, "r02")
        if mode == "wrong_revision":
            result = inspect(archive, "r02")
        elif mode == "wrong_identity":
            result = inspect(archive, item="OTHER-ITEM")
        else:
            tampered = base / "tampered.zip"
            transforms = {
                "hash": lambda e: [(i, b + b"tampered") if i.filename.endswith("deliverables/brief.md") else (i, b) for i, b in e],
                "unlisted": lambda e: e + [("unlisted.txt", b"not approved")],
                "unsafe_zip": lambda e: e + [("../escape.txt", b"escape")],
                "case_zip": lambda e: e + [(e[0][0].filename.swapcase(), e[0][1])],
                "manifest_hash": lambda e: manifest_mutation(e, lambda m: m["files"][0].update(sha256="0" * 64)),
                "manifest_dependency": lambda e: manifest_mutation(e, lambda m: m["files"][0].setdefault("dependencies", []).append("missing/nested.md")),
                "manifest_revision": lambda e: manifest_mutation(e, lambda m: m.update(revision="r02")),
                "manifest_prerequisite": lambda e: manifest_mutation(e, lambda m: m.setdefault("prerequisites", []).append({"id": "restricted", "required": True, "status": "unavailable", "evidence": "", "locator": "receiving access required"})),
                "manifest_false_access": lambda e: manifest_mutation(e, lambda m: m.update(external_access_required=True)),
                "manifest_false_limits": lambda e: manifest_mutation(e, lambda m: m.update(limits="All tools are verified and installed.")),
                "manifest_unknown_blob": lambda e: manifest_mutation(e, lambda m: m.update(private_context="unselected information")),
                "manifest_bytes": lambda e: manifest_mutation(e, lambda m: m["files"][0].update(bytes=0)),
                "missing_manifest": lambda e: [(i, b) for i, b in e if Path(i.filename).name != "manifest.json"],
                "zip_symlink": archive_symlink,
            }
            rewrite_zip(archive, tampered, transforms[mode])
            result = inspect(tampered)
        check(result["exit"] != 0, "Invalid archive accepted: " + json.dumps(result))
        return result


def archive_symlink(entries):
    info = zipfile.ZipInfo("linked.md")
    info.create_system = 3
    info.external_attr = (stat.S_IFLNK | 0o777) << 16
    return entries + [(info, b"README.md")]


def missing_required(name):
    def mutate(base, root, contract):
        contract["files"] = [r for r in contract["files"] if r["path"] != name]
        contract["required_paths"] = [p for p in contract["required_paths"] if p != name]
        for row in contract["files"]:
            row["dependencies"] = [d for d in row["dependencies"] if d != name]
        (root / name).unlink()
    return mutate


def bad_path(path):
    return lambda b, r, c: c["files"][0].update(path=path)


def symlink_source(base, root, contract):
    source = root / "sources/costs.csv"
    outside = base / "outside.csv"
    outside.write_bytes(source.read_bytes())
    source.unlink()
    try:
        source.symlink_to(outside)
    except OSError as exc:
        raise Blocked("Host did not permit symlink creation: " + str(exc)) from exc


def unlisted_nested(base, root, contract):
    replace_file(root, contract, "methods/references/check.md", "# Check\nRead [nested](nested.md) before any calculation.\n")
    (root / "methods/references/nested.md").write_text("Present but not allowlisted", encoding="utf-8")


def external_missing(base, root, contract):
    contract["files"][0]["dependencies"].append("external:restricted")
    contract["prerequisites"].append({"id": "restricted", "required": True, "status": "unavailable", "evidence": "", "locator": "receiving finance connector"})


def case_duplicate(base, root, contract):
    row = copy.deepcopy(contract["files"][0])
    row["path"] = "readme.md"
    contract["files"].append(row)


def private_path(base, root, contract):
    path = root / "PRIVATE/notes.md"
    path.parent.mkdir()
    path.write_text("synthetic private notes", encoding="utf-8")
    contract["files"].append({"path": "PRIVATE/notes.md", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "revision": REVISION, "classification": "permitted", "role": "source", "dependencies": []})


def hardlink_source(base, root, contract):
    try:
        os.link(root / "sources/costs.csv", base / "hardlink.csv")
    except OSError as exc:
        raise Blocked("Host did not permit hardlink creation: " + str(exc)) from exc


def blitz_reference(base, root, contract, declared=False, syntax="inline"):
    target = "https://chatgpt.com/g/g-p-synthetic/project"
    name = "methods/references/check.md"
    if syntax == "autolink":
        content = "Read the required project record: <" + target + ">.\n"
    elif syntax == "html_entity":
        content = '<a href="' + target.replace("/g/", "/&#x67;/") + '">Required project record</a>\n'
    elif syntax == "encoded_path":
        target = target.replace("/g/", "/%67/")
        content = "Read [the required project record](" + target + ").\n"
    else:
        content = "Read [the required project record](" + target + ").\n"
    replace_file(root, contract, name, content)
    if declared:
        contract["prerequisites"].append({"id": "project", "required": True, "status": "verified", "evidence": "Synthetic prior read receipt, not actual account access proof", "locator": target})
        next(row for row in contract["files"] if row["path"] == name)["dependencies"].append("external:project")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    cases = [
        ("normal_package_and_verify", None, "pass"),
        ("unselected_file_stays_out", lambda b, r, c: (r / "not-selected.txt").write_text("omit", encoding="utf-8"), "pass"),
        ("source_hash_changed", lambda b, r, c: (r / "sources/costs.csv").write_text("changed", encoding="utf-8"), "reject"),
        ("stale_build_revision", lambda b, r, c: c.update(revision="r02"), "reject"),
        ("missing_file_revision", lambda b, r, c: c["files"][0].update(revision=""), "reject"),
        ("source_revision_preserved", lambda b, r, c: c["files"][0].update(revision="source-r00"), "pass"),
        ("missing_readme", missing_required("README.md"), "reject"),
        ("missing_instructions", missing_required("PROJECT_INSTRUCTIONS.md"), "reject"),
        ("missing_declared_dependency", lambda b, r, c: c["files"][0]["dependencies"].append("absent.md"), "reject"),
        ("undeclared_nested_reference", unlisted_nested, "reject"),
        ("unavailable_nested_reference", lambda b, r, c: replace_file(r, c, "methods/references/check.md", "Read [missing](absent.md).\n"), "reject"),
        ("parent_traversal", bad_path("../README.md"), "reject"),
        ("absolute_path", bad_path("/README.md"), "reject"),
        ("windows_absolute_path", bad_path("C:/README.md"), "reject"),
        ("backslash_path", bad_path("methods\\SKILL.md"), "reject"),
        ("case_duplicate", case_duplicate, "reject"),
        ("private_path", private_path, "reject"),
        ("unapproved_classification", lambda b, r, c: c["files"][0].update(classification="private"), "reject"),
        ("unapproved_review", lambda b, r, c: c["review"].update(approved_for_export=False), "reject"),
        ("unreviewed_dependency_closure", lambda b, r, c: c["review"].update(dependency_review_complete=False), "reject"),
        ("source_symlink", symlink_source, "reject"),
        ("source_hardlink", hardlink_source, "reject"),
        ("reparse_flag_guard", None, "reparse_guard"),
        ("windows_superscript_device_guard", None, "path_guard:COM\u00b9.txt"),
        ("windows_console_device_guard", None, "path_guard:CONIN$"),
        ("windows_spaced_device_guard", None, "path_guard:CON .txt"),
        ("reserved_manifest_directory", bad_path("manifest.json/nested.md"), "reject"),
        ("unknown_contract_blob", lambda b, r, c: c.update(private_context="not allowlisted"), "reject"),
        ("boolean_schema_version", lambda b, r, c: c.update(schema_version=True), "reject"),
        ("existing_archive_unchanged", None, "no_overwrite"),
        ("atomic_failure_cleans_temporary", None, "atomic_failure"),
        ("external_prerequisite_unavailable", external_missing, "reject"),
        ("external_prerequisite_missing_evidence", lambda b, r, c: c["prerequisites"].append({"id": "needed", "required": True, "status": "verified", "evidence": "", "locator": "connector"}), "reject"),
        ("absolute_local_reference", lambda b, r, c: replace_file(r, c, "methods/references/check.md", "Read [required](C:/Blitz/only.md).\n"), "reject"),
        ("undeclared_blitz_reference", blitz_reference, "reject"),
        ("declared_external_reference", lambda b, r, c: blitz_reference(b, r, c, declared=True), "pass"),
        ("undeclared_blitz_autolink", lambda b, r, c: blitz_reference(b, r, c, syntax="autolink"), "reject"),
        ("declared_blitz_autolink", lambda b, r, c: blitz_reference(b, r, c, declared=True, syntax="autolink"), "pass"),
        ("undeclared_blitz_html_entity", lambda b, r, c: blitz_reference(b, r, c, syntax="html_entity"), "reject"),
        ("declared_blitz_html_entity", lambda b, r, c: blitz_reference(b, r, c, declared=True, syntax="html_entity"), "pass"),
        ("undeclared_blitz_encoded_path", lambda b, r, c: blitz_reference(b, r, c, syntax="encoded_path"), "reject"),
        ("declared_blitz_encoded_path", lambda b, r, c: blitz_reference(b, r, c, declared=True, syntax="encoded_path"), "pass"),
        ("wrong_inspect_revision", None, "wrong_revision"),
        ("wrong_inspect_identity", None, "wrong_identity"),
        ("tampered_payload_hash", None, "hash"),
        ("unlisted_zip_file", None, "unlisted"),
        ("unsafe_zip_path", None, "unsafe_zip"),
        ("case_duplicate_zip_path", None, "case_zip"),
        ("tampered_manifest_hash", None, "manifest_hash"),
        ("tampered_manifest_dependency", None, "manifest_dependency"),
        ("tampered_manifest_revision", None, "manifest_revision"),
        ("tampered_manifest_prerequisite", None, "manifest_prerequisite"),
        ("tampered_manifest_access_claim", None, "manifest_false_access"),
        ("tampered_manifest_limits", None, "manifest_false_limits"),
        ("tampered_manifest_unknown_blob", None, "manifest_unknown_blob"),
        ("tampered_manifest_bytes", None, "manifest_bytes"),
        ("missing_manifest", None, "missing_manifest"),
        ("archive_symlink", None, "zip_symlink"),
    ]
    results = []
    starting_exporter_hash = hashlib.sha256(EXPORTER.read_bytes()).hexdigest()
    for name, mutation, mode in cases:
        try:
            detail = run_case(name, mutation, mode)
            result = {"id": name, "status": "pass", "detail": detail}
        except Blocked as exc:
            result = {"id": name, "status": "blocked", "detail": str(exc)}
        except Exception as exc:
            result = {"id": name, "status": "fail", "detail": str(exc)}
        results.append(result)
        print(result["status"].upper() + ": " + name + (": " + str(result["detail"]) if result["status"] != "pass" else ""))
    final_exporter_hash = hashlib.sha256(EXPORTER.read_bytes()).hexdigest()
    if final_exporter_hash != starting_exporter_hash:
        results.append({"id": "code_changed_during_run", "status": "fail", "detail": "Exporter changed during execution; results do not describe one candidate."})
    summary = {s: sum(r["status"] == s for r in results) for s in ["pass", "fail", "blocked"]}
    report = {"kind": "executable_item_export_checks", "exporter_sha256": final_exporter_hash, "exporter_sha256_start": starting_exporter_hash, "test_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "summary": summary, "cases": results, "limits": "Code checks only. No model execution, actual receiving access, Blitz routing, installation or adoption is inferred. A blocked filesystem symlink test remains blocked even if ZIP symlink rejection passes."}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(summary))
    return 1 if summary["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
