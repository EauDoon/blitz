#!/usr/bin/env python3
"""Exercise the generated runtime, atomic publication, and resource closure."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch
import zipfile

sys.dont_write_bytecode = True
KIT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("v2_context", KIT / "setup/build_thor_context.py")
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def rejected(call):
    try:
        call()
    except (OSError, ValueError):
        return
    raise AssertionError("Invalid operation was accepted")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def execute(*args):
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run([sys.executable, "-B", *map(str, args)], capture_output=True, text=True, env=env)
    check(result.returncode == 0, result.stdout + result.stderr)
    return result


def main():
    with tempfile.TemporaryDirectory(prefix="v2-runtime-check-") as raw:
        base = Path(raw)
        out = base / "runtime"
        report = context.build(KIT, out)
        actual = {p.name for p in out.iterdir()}
        expected = {context.INDEX, context.CONTEXT_MANIFEST, context.RUNTIME, *context.EXACT,
                    *(context.view_name(group) for group in [*context.GROUPS, "Shared"])}
        check(actual == expected and len(actual) == 17, "Incomplete direct source set")
        check(len((out / context.INDEX).read_bytes()) <= 16000, "Routing index became a full catalog")
        for row in report["files"]:
            data = (out / row["path"]).read_bytes()
            check(sha(data) == row["sha256"] and len(data) == row["bytes"], "Generated file is not pinned")
        check(actual == {row["path"] for row in report["files"]} | {context.CONTEXT_MANIFEST},
              "A generated artifact is not recorded")
        for alias, original in context.EXACT.items():
            check((out / alias).read_bytes() == (KIT / original).read_bytes(), "Alias differs from original")
        index = (out / context.INDEX).read_text(encoding="utf-8")
        for alias in (context.OPENER, context.EXPORTER, context.CONTRACT, context.RUNTIME):
            check(alias in index and sha((out / alias).read_bytes()) in index, "Resource discovery lacks hash")
        check(len(report["methods"]) == 25, "Missing method coverage")
        runtime_hash = sha((out / context.RUNTIME).read_bytes())
        with zipfile.ZipFile(out / context.RUNTIME) as archive:
            check(archive.testzip() is None, "Runtime ZIP CRC failed")
            manifest = json.loads(archive.read("Blitz/manifest.json"))
            expected_payload = {row["path"] for row in report["sources"]}
            check(set(archive.namelist()) == {"Blitz/manifest.json", *("Blitz/" + p for p in expected_payload)},
                  "Runtime membership differs from selected source set")
            for row in manifest["files"]:
                data = archive.read("Blitz/" + row["path"])
                check(data == (KIT / row["path"]).read_bytes(), "Runtime changed original source bytes")
                check(sha(data) == row["sha256"] and len(data) == row["bytes"], "Runtime hash mismatch")
            check(set(manifest["licenses"]) == {
                p for p in expected_payload if Path(p).name.lower() in
                {"license", "license.txt", "license.md", "notice", "notice.md", "third_party_licenses.md"}},
                "Licenses did not travel")
            check(not any(set(Path(p).parts) & context.EXCLUDED_PARTS for p in archive.namelist()),
                  "Evaluation, private build material, or caches leaked into runtime")
            # Real helper dependencies and frontend assets must survive compilation.
            for path in ("setup/frontmatter.py", "setup/verify_archive.py", "setup/export_item.py",
                         "skills/meta-skill/scripts/utils.py", "skills/meta-skill/scripts/generate_report.py",
                         "skills/frontend-scroll-craft/engine/scrollcraft.js",
                         "skills/frontend-scroll-craft/engine/scrollcraft.css",
                         "skills/frontend-taste/references/cinematic/cinematic.js",
                         "skills/frontend-taste/references/cinematic/cinematic.css",
                         "skills/meta-skill/eval-viewer/viewer.html"):
                check("Blitz/" + path in archive.namelist(), "Omitted local helper or asset: " + path)
            check(manifest["dependencies"]["host_external"], "External capabilities not declared")
        # Standalone aliases run in an output directory with no kit import path.
        execute(out / context.OPENER, "--help")
        execute(out / context.EXPORTER, "--help")
        opened = base / "opened"
        result = execute(out / context.OPENER, out / context.RUNTIME,
                         "--expected-sha256", runtime_hash, "--extract-to", opened)
        check(json.loads(result.stdout)["result"] == "pass", "Standalone runtime opener failed")
        check((opened / "Blitz/setup/frontmatter.py").is_file(), "Dependency not extracted")
        check(not any(p.name == "__pycache__" for p in opened.rglob("*")), "Opening executed payload code")
        execute(opened / "Blitz/setup/export_item.py", "--help")
        # Parse every shipped Python resource without importing it or its external deps.
        for path in (opened / "Blitz").rglob("*.py"):
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        # Reproducing from the opened runtime proves compiler-local import closure.
        clone = base / "reproduced"
        execute(opened / "Blitz/setup/build_thor_context.py", "--kit", opened / "Blitz", "--out", clone)
        check({p.name: p.read_bytes() for p in clone.iterdir()} ==
              {p.name: p.read_bytes() for p in out.iterdir()}, "Runtime regeneration is nondeterministic")
        # A hostile generated file placed back in selected inputs is excluded.
        fixture = base / "fixture"
        shutil.copytree(opened / "Blitz", fixture)
        nested_generated = fixture / "skills/blitz" / context.RUNTIME
        nested_generated.write_bytes(b"DO_NOT_RECURSE_GENERATED_OUTPUT")
        files, _, _ = context.prepare(fixture)
        check(files[context.RUNTIME] == (out / context.RUNTIME).read_bytes(), "Generated artifact recursed")
        nested_generated.unlink()
        # Simulate write failure before publication. No partial occupied target survives.
        failed = base / "write-failed"
        original_write = Path.write_bytes
        writes = 0
        def fail_write(path, data):
            nonlocal writes
            writes += 1
            if writes == 2:
                raise OSError("injected disk failure")
            return original_write(path, data)
        with patch.object(Path, "write_bytes", fail_write):
            rejected(lambda: context.build(fixture, failed))
        check(not failed.exists() and not list(base.glob(".thor-context-*")), "Partial output leaked")
        context.build(fixture, failed)
        check((failed / context.CONTEXT_MANIFEST).is_file(), "Retry after failure did not work")
        occupied = base / "occupied"
        occupied.mkdir()
        (occupied / "sentinel").write_bytes(b"owner data")
        rejected(lambda: context.build(fixture, occupied))
        check((occupied / "sentinel").read_bytes() == b"owner data", "Occupied target was changed")
        race = base / "raced"
        publish = context.publish_directory
        def occupy_then_publish(stage, destination):
            destination.mkdir()
            (destination / "sentinel").write_bytes(b"concurrent owner")
            publish(stage, destination)
        with patch.object(context, "publish_directory", occupy_then_publish):
            rejected(lambda: context.build(fixture, race))
        check((race / "sentinel").read_bytes() == b"concurrent owner", "Race replaced another writer")
        check(not list(base.glob(".thor-context-*")), "Publication failure leaked scratch output")
        # Source drift invalidates the staged output without publishing any of it.
        drift_out = base / "drifted"
        inventory = context.inventory
        reads = 0
        def change_second_source_read(path):
            nonlocal reads
            if path == fixture:
                reads += 1
                if reads == 2:
                    (fixture / "setup/thor.md").write_bytes(b"Changed while generating")
            return inventory(path)
        with patch.object(context, "inventory", change_second_source_read):
            rejected(lambda: context.build(fixture, drift_out))
        check(not drift_out.exists(), "Changing source tree was published")
        # A missing essential runtime alias fails before even creating a destination.
        (fixture / "setup/export_item.py").unlink()
        rejected(lambda: context.build(fixture, base / "missing"))
        check(not (base / "missing").exists(), "Missing resource yielded a partial runtime")
    print("PASS: complete 17-source runtime; 25 methods; exact aliases; compact index; hashes/licenses; "
          "local helper/assets closure; standalone opening/exporter; clean deterministic regeneration; "
          "generated exclusion; write failure/retry; occupied/racing target preservation; source drift; missing dependency.")


if __name__ == "__main__":
    main()
