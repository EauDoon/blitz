#!/usr/bin/env python3
"""Build complete Blitz runtime sources into a NEW, non-live directory. Never install.

Source text stays verbatim inside fenced sections. The index resolves original
paths to those sections; exact executable resources are packaged, not executed.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import posixpath
import re
import stat
import sys
import tempfile
import unicodedata
import zipfile
from urllib.parse import quote, unquote, urlsplit

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).absolute().parent))
from frontmatter import parse_skill_frontmatter
from verify_archive import publish_directory, validated_archive

VERSION = "v2.1OAI-r1"
PREFIX = "Blitz_" + VERSION
INDEX = PREFIX + "_Method_Index.md"
GUIDE = PREFIX + "_Launch_and_Export.md"
BODY = "Blitz_Project_Instructions_" + VERSION + ".md"
REGISTER = "Blitz_System_Register_" + VERSION + ".md"
OPERATING = PREFIX + "_Operating_Contract.md"
OPERATOR = PREFIX + "_Operator_Guide.md"
RUNTIME = "Blitz_" + VERSION + "_Runtime.zip"
OPENER = "Blitz_" + VERSION + "_Open_Runtime.py"
EXPORTER = "Blitz_" + VERSION + "_Export_Item.py"
CONTRACT = "Blitz_" + VERSION + "_Item_Export_Contract.json"
CONTEXT_MANIFEST = PREFIX + "_Context_Manifest.json"
EXACT = {GUIDE: "setup/source-use.md", BODY: "setup/Blitz_Project_Instructions.md",
         REGISTER: "setup/Blitz_System_Register.md", OPERATING: "setup/operating-contract.md",
         OPERATOR: "setup/operator-guide.md", EXPORTER: "setup/export_item.py",
         CONTRACT: "templates/item-export.json", OPENER: "setup/verify_archive.py"}
GROUPS = {
    "Core": "blitz cold-read gauntlet-verify meeting-to-action reasoning-core research-protocol".split(),
    "Writing": "anti-slop doc-style house-style legal-contract my-writing-style write-with-pyramid".split(),
    "Analysis": "calc-workbook metric-pull".split(),
    "Visual": "diagram-design google-slides pitch-architect slide-design viz-dashboards".split(),
    "Building": "frontend-mockup frontend-scroll-craft frontend-taste meta-skill skill-package-check website-cloner".split(),
}
METHOD_GROUP = {name: group for group, names in GROUPS.items() for name in names}
EXCLUDED_PARTS = {"eval", "evals", "tests", "fixtures", "answer-key", "answer-keys",
                  "answer_keys", "hidden_answers", "builder_notes", "buildnotes",
                  "answer_key", "hidden-answers", "builder-notes", "build-notes",
                  "build_notes", "reviews", "__pycache__", "node_modules"}
ROOT_DOCS = {"AGENTS.md", "ENTRYPOINT.md", "PLAYBOOK.md", "README.md", "START.md"}
LIVE_PARTS = {".codex", ".claude", ".agents", "plugins", "skills"}
LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>\n]+>|[^)\n]+)\)")
INLINE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def path_key(value):
    return unicodedata.normalize("NFC", str(value)).casefold()


def guard_path(raw, must_exist=True):
    """Reject aliases before resolve(), including Windows junctions and ADS."""
    text = os.fspath(raw)
    if "//" in text or "\\\\" in text:
        raise ValueError("network or repeated-separator alias is not accepted")
    components = re.split(r"[\\/]", text)
    for component in components:
        if not component or re.fullmatch(r"[A-Za-z]:", component):
            continue
        if (component in {".", ".."} or component.endswith((".", " "))
                or unicodedata.normalize("NFC", component) != component
                or any(ord(c) < 32 or ord(c) == 127 or c in ':*?"<>|' for c in component)
                or PureWindowsPath(component).is_reserved()):
            raise ValueError("unsafe or aliased path component: " + component)
    path = Path(text).absolute()
    for part in [*reversed(path.parents), path]:
        if os.path.lexists(part):
            info = part.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise ValueError("symlink/reparse path is not accepted: " + str(part))
    if must_exist and not path.exists():
        raise ValueError("missing path: " + str(path))
    resolved = path.resolve(strict=must_exist)
    if os.path.normcase(str(path)) != os.path.normcase(str(resolved)):
        raise ValueError("aliased path is not accepted: " + str(path))
    return path


def validate_output(raw, kit):
    out = guard_path(raw, must_exist=False)
    if out == kit or kit in out.parents or out in kit.parents:
        raise ValueError("output must not overlap the kit")
    if out == Path.home() or out == Path(out.anchor):
        raise ValueError("output must not be a home or filesystem root")
    if any(path_key(part) in LIVE_PARTS for part in out.parts):
        raise ValueError("output must not be a live skill/plugin/configuration path")
    if os.path.lexists(out):
        raise ValueError("output is occupied; nothing was replaced")
    if not out.parent.is_dir():
        raise ValueError("output parent must already exist")
    return out


def inventory(kit):
    files, keys, inodes = {}, set(), set()
    def unreadable(error):
        raise error
    for current, dirs, names in os.walk(kit, followlinks=False, onerror=unreadable):
        for name in sorted(dirs + names):
            path = guard_path(Path(current) / name)
            rel = path.relative_to(kit).as_posix()
            key = path_key(rel)
            if key in keys:
                raise ValueError("case/Unicode alias in source: " + rel)
            keys.add(key)
            info = path.lstat()
            if path.is_dir():
                continue
            if not stat.S_ISREG(info.st_mode):
                raise ValueError("non-regular source file: " + rel)
            inode = (info.st_dev, info.st_ino)
            if info.st_nlink > 1 or inode in inodes:
                raise ValueError("hardlink/duplicate file identity: " + rel)
            inodes.add(inode)
            files[rel] = path.read_bytes()
    return files


def group_for(rel):
    parts = PurePosixPath(rel).parts
    if any(path_key(part) in EXCLUDED_PARTS
           or path_key(PurePosixPath(part).stem) in EXCLUDED_PARTS
           or part.startswith(".") for part in parts):
        return None
    # A generated output copied into a source directory must never recursively
    # become runtime input, even when it is under setup or a method folder.
    if (path_key(parts[-1]) in {path_key(CONTEXT_MANIFEST), "source-context-manifest.json"}
            or re.match(r"(?:Blitz_v[^/]*_|Blitz_(?:Project_Instructions_v|System_Register_v))", parts[-1], re.I)):
        return None
    if parts[0] == "skills" and len(parts) > 2:
        return METHOD_GROUP.get(parts[1])
    if rel == "skills/provenance.md" or rel in ROOT_DOCS or parts[0] in {"profiles", "templates", "setup"}:
        return "Shared"
    return None


def readable(rel):
    path = PurePosixPath(rel)
    return path.suffix.lower() in {".md", ".txt", ".json", ".yaml", ".yml"} or path.name in {"LICENSE", "NOTICE"}


def source_id(rel):
    return "source-" + digest(rel.encode("utf-8"))[:16]


def view_name(group):
    return PREFIX + "_Methods_" + group + ".md"


def source_link(row):
    return quote(row["view"]) + ("#" + row["section"] if row.get("section") else "")


def link_refs(text):
    for match in LINK.finditer(text):
        target = match.group(1).strip()
        if target.startswith("<"):
            target = target[1:-1]
        else:
            target = re.split(r'\s+["\']', target, maxsplit=1)[0]
        yield target, "markdown"
    # ponytail: this is a static retrieval map; selected-route execution must
    # inspect dynamic references and code imports rather than invent a parser.
    for match in INLINE.finditer(text):
        token = match.group(1)
        # Commands and dynamic examples are not declared static dependencies.
        if "/" in token and not re.search(r"[<>*{}\n]", token) and not token.startswith(("http:", "https:")):
            yield token, "inline"


def resolve_reference(origin, target, sources, all_files, generated):
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return {"status": "external_or_host_reference"}
    if not parsed.path:
        return {"status": "same_source_fragment", "source": origin}
    path = unquote(parsed.path).replace("\\", "/")
    if path in generated:
        return {"status": "generated_view", "view": path}
    candidates = [posixpath.normpath(posixpath.join(posixpath.dirname(origin), path)), posixpath.normpath(path)]
    if origin.startswith("skills/"):
        candidates.append(posixpath.normpath("/".join(origin.split("/")[:2]) + "/" + path))
    found = next((candidate for candidate in candidates if candidate in sources), None)
    if found:
        row = sources[found]
        return {"status": row["status"], "source": found,
                **({"view": row["view"], "section": row.get("section")} if "view" in row else {})}
    if "manifest.json" in candidates:
        return {"status": "runtime_manifest", "runtime_path": "Blitz/manifest.json"}
    if any(set(PurePosixPath(candidate).parts) & (EXCLUDED_PARTS | {"examples"})
           for candidate in candidates):
        return {"status": "excluded_from_runtime_views"}
    return {"status": "unresolved_or_task_created", "action": "Check the selected route; do not claim this dependency is available."}


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def file_row(path, data):
    row = {"path": path, "bytes": len(data), "sha256": digest(data)}
    try:
        row["characters"] = len(data.decode("utf-8"))
    except UnicodeDecodeError:
        pass
    return row


def make_runtime(payload, descriptions):
    """All selected local resources travel together; external tools do not."""
    licenses = sorted(p for p in payload if PurePosixPath(p).name.lower() in
                      {"license", "license.txt", "license.md", "notice", "notice.md", "third_party_licenses.md"})
    manifest = {
        "kit": "Blitz", "version": VERSION.removeprefix("v"), "built": "11-10-2026",
        "purpose": "Task-local runtime resources; no installation or script execution.",
        "skills": [{"name": name, "description": descriptions[name]} for name in sorted(descriptions)],
        "licenses": licenses,
        "dependencies": {
            "included": "Every selected local method directory, references, scripts, assets, shared templates and setup helpers.",
            "host_external": [
                "Python 3.12 or later for the stdlib opener, compiler, and item exporter.",
                "Task-selected Python libraries such as openpyxl, PyYAML, Pillow, numpy, matplotlib, or anthropic are not bundled.",
                "Node.js and task-selected modules such as Playwright, docx, and rendering libraries are not bundled.",
                "Browsers, document/PDF renderers, fonts, shell utilities, and media encoders must be checked when needed.",
                "Connected apps, credentials, network access, native host tools, delegated agents, and outside source stores are not granted.",
            ],
            "rule": "Read the selected method and its scripts before use. Verify actual capabilities; do not install or contact services merely because a resource mentions them.",
        },
        "files": [file_row(p, b) for p, b in sorted(payload.items())],
        "limits": [
            "Complete selected local resource snapshot, not a parser-proven dependency closure for arbitrary dynamic code.",
            "Excluded evaluations, answer keys and builder history are not runtime dependencies.",
            "Integrity proves bytes and membership, not host execution, native loading, automatic routing, or safe behavior of every script.",
        ],
    }
    entries = {**payload, "manifest.json": json_bytes(manifest)}
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for rel, data in sorted(entries.items()):
            info = zipfile.ZipInfo("Blitz/" + rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compresslevel=9)
    return buffer.getvalue(), manifest


def prepare(kit):
    all_files = inventory(kit)
    names = {rel.split("/")[1] for rel in all_files if re.fullmatch(r"skills/[^/]+/SKILL\.md", rel)}
    if names != set(METHOD_GROUP):
        raise ValueError("method inventory differs from the 25-method release: " + str(sorted(names ^ set(METHOD_GROUP))))
    descriptions = {}
    for name in sorted(names):
        metadata = parse_skill_frontmatter(all_files["skills/" + name + "/SKILL.md"].decode("utf-8").replace("\r\n", "\n"))
        if metadata["name"] != name:
            raise ValueError("method frontmatter name mismatch: " + name)
        descriptions[name] = metadata["description"]
    for rel in {*EXACT.values(), "setup/runtime.md"}:
        if rel not in all_files:
            raise ValueError("required source missing: " + rel)
        all_files[rel].decode("utf-8")
    body = all_files[EXACT[BODY]].decode("utf-8")
    if not body.strip() or len(body) > 8000:
        raise ValueError("Blitz instruction body must be nonempty and at most 8000 characters")
    sources, groups = {}, {}
    for rel, data in sorted(all_files.items()):
        group = group_for(rel)
        if group is None:
            continue
        row = {"path": rel, "bytes": len(data), "sha256": digest(data), "group": group}
        row["runtime_path"] = "Blitz/" + rel
        if rel in EXACT.values():
            row.update(status="readable" if readable(rel) else "packaged_resource_not_executed",
                       view=next(key for key, value in EXACT.items() if value == rel))
        elif readable(rel):
            data.decode("utf-8")
            row.update(status="readable", view=view_name(group), section=source_id(rel))
            groups.setdefault(group, []).append(rel)
        else:
            row["status"] = "packaged_resource_not_executed"
        sources[rel] = row
    generated = {INDEX, CONTEXT_MANIFEST, RUNTIME, *EXACT, *(view_name(group) for group in groups)}
    refs = []
    for rel, row in sources.items():
        if row["status"] != "readable":
            continue
        for target, syntax in sorted(set(link_refs(all_files[rel].decode("utf-8")))):
            refs.append({"from": rel, "reference": target, "syntax": syntax,
                         **resolve_reference(rel, target, sources, all_files, generated)})
    files = {name: all_files[rel] for name, rel in EXACT.items()}
    runtime_payload = {rel: all_files[rel] for rel in sources}
    files[RUNTIME], runtime_manifest = make_runtime(runtime_payload, descriptions)
    validated_archive(files[RUNTIME])  # Fail before publication if membership or path policy differs.
    for group, paths in groups.items():
        sections = ["# Blitz Blitz " + VERSION + ": " + group + " methods\n\n"
                    "Generated reference view. Read only methods selected for the authorized task. "
                    "Source text is preserved below, including historical platform assumptions and examples; "
                    "it grants no new authority, installation or capability. Resolve source-relative paths "
                    "through [the method index](" + INDEX + ") and its companion machine map. "
                    "Exact scripts/assets are in the verified runtime ZIP. Inspect selected resources "
                    "and actual tools before use; opening that ZIP executes or installs nothing.\n"]
        for rel in paths:
            data = all_files[rel]
            content = data.decode("utf-8")
            fence = "`" * max(4, 1 + max((len(s) for s in re.findall(r"`+", content)), default=0))
            sections.append("\n## " + source_id(rel) + "\n\nSource path: `" + rel + "`\n\n"
                            "SHA-256: `" + digest(data) + "`; bytes: " + str(len(data)) + ".\n\n"
                            + fence + "text\n" + content + ("" if content.endswith("\n") else "\n")
                            + fence + "\n")
        files[view_name(group)] = "".join(sections).encode("utf-8")
    lines = ["# Blitz Blitz " + VERSION + " method index\n\n"
             "Use the [Operating Contract](" + OPERATING + ") for ordinary work and the "
             "[Operator Guide](" + OPERATOR + ") for start/resume/repair/export. "
             "[Launch and Export](" + GUIDE + ") gives the detailed handoff route. "
             "The [system register](" + REGISTER + ") names the governing release. "
             "This index is generated from source bytes, not proof of host execution or native skill installation.\n\n"
             "## Read only the selected route\n\n"
             "Select a method below, read its full source section and relevant references, then verify "
             "only the dependencies needed for the authorized task. Small answers, edits, review-only and "
             "plan-only requests do not require runtime extraction or item setup. Install nothing globally; "
             "keep Work and memory settings unchanged.\n\n"
             "Descriptions below are shortened routing hints. Full descriptions, original paths, hashes, "
             "readable sections and reference resolution are in " + CONTEXT_MANIFEST + ". "
             "Resolve original relative paths from the source directory, then kit root, then owning skill "
             "directory. Preserve the original fragment within the mapped source. Do not guess that "
             "an unresolved example, generated output, or host path is an available prerequisite.\n\n"
             "## Method roster\n\n| Method | Route hint | Readable source |\n|---|---|---|\n"]
    for name in sorted(names):
        row = sources["skills/" + name + "/SKILL.md"]
        hint = descriptions[name].replace("|", "\\|").replace("\n", " ")
        if len(hint) > 180:
            hint = hint[:177].rsplit(" ", 1)[0] + "..."
        lines.append("| " + name + " | " + hint + " | [Read](" + source_link(row) + ") |\n")
    lines.append("\n## Exact directly supplied resources\n\n"
                 "| Source name | Original path | SHA-256 | Bytes |\n|---|---|---|---:|\n")
    for alias in (EXPORTER, CONTRACT, OPENER, RUNTIME):
        original = EXACT.get(alias, "Selected original paths under Blitz/ plus internal manifest")
        lines.append("| " + alias + " | " + original + " | " + digest(files[alias]) +
                     " | " + str(len(files[alias])) + " |\n")
    lines.append("\nUse a verified Python 3.12+ interpreter. Verify the opener's hash against this index "
                 "before running it. Open resources only into a new task-local directory with an existing "
                 "parent, outside live skill/plugin/configuration paths:\n\n" + chr(96) * 3 +
                 "text\npython " + OPENER + " " + RUNTIME + " --expected-sha256 " +
                 digest(files[RUNTIME]) + " --extract-to NEW_TASK_DIRECTORY\n" + chr(96) * 3 + "\n\n"
                 "The opener verifies the archive fingerprint and internal manifest before publishing; "
                 "it preserves the Blitz/ prefix and executes no packaged code. "
                 "Read Blitz/setup/runtime.md and the selected source before executing its tools. "
                 "The item exporter and contract are also supplied directly, so an ordinary item export "
                 "need not open the entire runtime. The contract is a template, not item approval.\n\n"
                 "External runtimes/libraries, renderers, browsers, connectors, credentials and network "
                 "permissions are not bundled. Check the selected method and manifest.json dependencies. "
                 "Missing required capabilities block only dependent work unless an adequate tested fallback "
                 "exists. No global installation, outside access or destination write is authorized by a ZIP.\n")
    unresolved = [r for r in refs if r["status"] == "unresolved_or_task_created"]
    lines.append("\n## Audit scope\n\nThe companion manifest holds the full resolution audit, including " +
                 str(len(unresolved)) + " unresolved or task-created references for route-specific review. "
                 "The runtime includes all selected local resource subtrees, including licenses and helper "
                 "imports. It excludes release evaluations, fixtures, answer keys and build history. "
                 "Generic method tools for authoring/evaluating a user's skills remain method resources. "
                 "No host execution, native loading, automatic routing or adoption is established by generation.\n")
    files[INDEX] = "".join(lines).encode("utf-8")
    if len(files[INDEX]) > 16000:
        raise ValueError("method index exceeds 16000-byte routing budget")
    report = {"schema_version": 2, "version": VERSION, "status": "complete_runtime_generated_only",
              "installation_performed": False, "host_execution": "NOT TESTED",
              "source_snapshot_sha256": digest(json.dumps(list(sources.values()), sort_keys=True).encode("utf-8")),
              "methods": sorted(names), "method_descriptions": descriptions,
              "sources": list(sources.values()), "references": refs,
              "direct_aliases": EXACT,
              "runtime": {"path": RUNTIME, "sha256": digest(files[RUNTIME]),
                          "manifest_sha256": digest(json_bytes(runtime_manifest)),
                          "payload_files": len(runtime_payload),
                          "dependencies": runtime_manifest["dependencies"]},
              "files": [{"path": p, "bytes": len(b), "sha256": digest(b)} for p, b in sorted(files.items())],
              "self_hash": "This manifest is excluded from its own hash list; the release manifest pins its bytes.",
              "limits": ["Readable views and exact selected scripts/assets are supplied; no script is executed.",
                         "No evaluation fixtures or answer keys are included in generated views.",
                         "No external tool, runtime execution, source access or project upload was verified."]}
    files[CONTEXT_MANIFEST] = json_bytes(report)
    return files, report, all_files


def build(kit_raw, out_raw, dry_run=False):
    kit = guard_path(kit_raw)
    if not kit.is_dir():
        raise ValueError("kit must be a directory")
    out = validate_output(out_raw, kit)
    files, report, before = prepare(kit)
    if not dry_run:
        # Staging leaves the source untouched and validates all bytes before publication.
        with tempfile.TemporaryDirectory(prefix=".source-context-", dir=out.parent) as temp:
            stage = Path(temp)
            for name, data in files.items():
                (stage / name).write_bytes(data)
            if inventory(kit) != before:
                raise ValueError("source changed during generation; rerun against frozen bytes")
            if inventory(stage) != files:
                raise ValueError("staged output changed; nothing was published")
            validate_output(out, kit)
            # Same-filesystem rename publishes the complete tree at once. The
            # shared primitive fails on occupied targets, including a race.
            publish_directory(stage, out)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kit", default=str(Path(__file__).absolute().parents[1]))
    parser.add_argument("--out", required=True, help="new non-live directory outside the kit")
    parser.add_argument("--dry-run", action="store_true", help="validate without writing")
    args = parser.parse_args()
    try:
        report = build(args.kit, args.out, args.dry_run)
        print(json.dumps({"result": "pass", "mode": "dry_run" if args.dry_run else "generated",
                          "methods": len(report["methods"]), "sources": len(report["sources"]),
                          "files": [row["path"] for row in report["files"]] + [CONTEXT_MANIFEST],
                          "host_execution": "NOT TESTED", "installation_performed": False}, indent=2))
        return 0
    except (OSError, ValueError, UnicodeError) as exc:
        print("ERROR: " + str(exc) + ". No installation or replacement was performed.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
