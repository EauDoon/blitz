#!/usr/bin/env python3
"""Prepare reference candidates, never install or replace host adaptations.

--dry-run validates and reports without writes. --out must be a new non-live
folder outside the kit. An optional read-only inventory describes current host
adaptations; its paths are opaque metadata. Name-map statuses are historical.
Only a temporary sibling created by this invocation may be cleaned up.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontmatter import parse_skill_frontmatter

KIT = Path(__file__).resolve().parents[1]
ADAPTER_REFERENCE = "references/blitz-host-adapter.md"
ADAPTER_HEADER = ("## Host capability adapter\n\n"
                  "Read `references/blitz-host-adapter.md` before using imported host-specific "
                  "instructions. Preserve the host-adapted skill's supported save/install route. "
                  "This reference candidate grants no access, replacement or installation authority.\n\n")
SAFE_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def validate_output(raw):
    out = Path(raw).expanduser().resolve()
    if out == KIT or KIT in out.parents or out in KIT.parents:
        raise ValueError("--out must not overlap the kit or its ancestors")
    if out == Path.home() or out == Path(out.anchor):
        raise ValueError("--out must not be a home or filesystem root")
    for part in out.parts:
        if part in {".agents", ".codex", ".claude"}:
            raise ValueError("--out must not be inside a live skill store")
    if Path(raw).expanduser().is_symlink() or out.exists():
        raise ValueError("--out is occupied; choose a new folder; nothing was removed")
    if not out.parent.is_dir():
        raise ValueError("--out parent must already exist")
    return out


def read_inventory(path):
    if path is None:
        return None
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("skills"), list) or not data.get("observed_at"):
        raise ValueError("inventory needs observed_at and a skills array")
    seen = set()
    for row in data["skills"]:
        if not isinstance(row, dict) or not isinstance(row.get("name"), str) or not isinstance(row.get("role"), str):
            raise ValueError("inventory skill needs string name and role")
        if row["name"] in seen:
            raise ValueError("inventory has duplicate installed names")
        seen.add(row["name"])
    return data


def load_plan(inventory):
    data = json.loads((KIT / "setup/name-map.json").read_text(encoding="utf-8"))
    nm = data["skills"]
    sources = [p for p in sorted((KIT / "skills").iterdir()) if p.is_dir()]
    renames, rows, targets = {}, [], set()
    for src in sources:
        if src.is_symlink() or any(p.is_symlink() for p in src.rglob("*")):
            raise ValueError("symlinks are not accepted in source skills")
        name = src.name
        entry = nm.get(name, {"status": "unknown", "chatgpt_name": None})
        status = entry.get("status")
        if status not in {"same", "renamed", "unknown", "host_tool"}:
            raise ValueError("invalid name-map status for " + name)
        target = entry.get("chatgpt_name") or name
        if not isinstance(target, str) or not SAFE_NAME.fullmatch(target):
            raise ValueError("unsafe mapped skill name for " + name)
        if status != "host_tool":
            if target in targets:
                raise ValueError("duplicate mapped target " + target)
            targets.add(target)
            if target != name:
                renames[name] = target
        matches = [r for r in inventory["skills"]
                   if r["role"] == name or r["name"] in {name, target}] if inventory else []
        if len(matches) > 1:
            raise ValueError("ambiguous existing same-role adaptations for " + name)
        existing = matches[0] if matches else None
        action = ("skip_native_role_capability_check_required" if status == "host_tool" else
                  "retain_host_adaptation_compare_and_merge" if existing else
                  "compare_inventory_then_authorized_new_candidate" if inventory else
                  "inventory_required_before_any_installation")
        rows.append({"source_name": name, "candidate_name": target,
                     "historical_name_map_status": status, "current_installation": "not_verified_here",
                     "action": action, "existing_skill": existing,
                     "existing_observed_at": inventory.get("observed_at") if existing else None})
    return renames, rows


def transformed_files(src, target, renames, adapter):
    files = {}
    patterns = {old: re.compile(r"(?<![\w/.-])" + re.escape(old) + r"(?![\w/-]|\.\w)")
                for old in renames}
    for p in sorted(src.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(src).as_posix()
        if rel == ADAPTER_REFERENCE:
            raise ValueError("adapter reference collision in " + src.name)
        b = p.read_bytes()
        if p.suffix == ".md" and p.name != "CHANGES.md":
            t = b.decode("utf-8")
            for old, new in renames.items():
                t = patterns[old].sub(new, t)
            if rel == "SKILL.md":
                metadata = parse_skill_frontmatter(t)
                if metadata["name"] not in {src.name, target}:
                    raise ValueError(src.name + ": frontmatter name does not match role")
                t = re.sub(r"^name:\s*.*$", 'name: "' + target + '"', t, count=1, flags=re.M)
                boundary = re.match(r"^---\n.*?\n---\n", t, re.S).end()
                t = t[:boundary] + "\n" + ADAPTER_HEADER + t[boundary:].lstrip("\n")
                d = parse_skill_frontmatter(t)["description"]
                if not d or len(d) > 1024 or len(t) > 22000 or len(t.encode("utf-8")) > 22000:
                    raise ValueError(src.name + ": frontmatter/size validation failed after adapter")
            t = t.replace("../../setup/host-adapters/openai.md", ADAPTER_REFERENCE)
            t = t.replace("setup/host-adapters/openai.md", ADAPTER_REFERENCE)
            b = t.encode("utf-8")
        files[rel] = b
    if "SKILL.md" not in files or "agents/openai.yaml" not in files:
        raise ValueError(src.name + ": SKILL.md or OpenAI metadata missing")
    files[ADAPTER_REFERENCE] = adapter
    return files


def prepare(inventory, dry_run):
    renames, rows = load_plan(inventory)
    adapter = (KIT / "setup/host-adapters/openai.md").read_bytes()
    all_files = {}
    for row in rows:
        if row["historical_name_map_status"] == "host_tool":
            continue
        files = transformed_files(KIT / "skills" / row["source_name"], row["candidate_name"], renames, adapter)
        for rel, data in files.items():
            all_files[row["candidate_name"] + "/" + rel] = data
    manifest_bytes = (KIT / "manifest.json").read_bytes()
    manifest_version = json.loads(manifest_bytes)["version"]
    if not isinstance(manifest_version, str) or not manifest_version:
        raise ValueError("manifest version must be a nonempty string")
    report = {"schema_version": 1, "mode": "dry_run" if dry_run else "staged",
              "version": manifest_version, "status": "reference_candidates_only",
              "installation_performed": False,
              "source_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
              "adapter_sha256": hashlib.sha256(adapter).hexdigest(),
              "inventory_sha256": hashlib.sha256(json.dumps(inventory, sort_keys=True).encode()).hexdigest() if inventory else None,
              "skills": rows,
              "files": [{"path": p, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
                        for p, b in sorted(all_files.items())],
              "limits": ["Name rewrites do not prove semantic compatibility.",
                         "Retain host adaptations and merge reviewed necessary method changes before isolated checks.",
                         "No host native load, automatic routing or installed integrity was tested."]}
    return all_files, report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, help="new reference output folder outside kit/live stores")
    ap.add_argument("--dry-run", action="store_true", help="validate and print report with no writes")
    ap.add_argument("--inventory", help="read-only current host skill inventory JSON")
    args = ap.parse_args()
    try:
        out = validate_output(args.out)
        files, report = prepare(read_inventory(args.inventory), args.dry_run)
        if not args.dry_run:
            with tempfile.TemporaryDirectory(prefix=".blitz-stage-", dir=out.parent) as tmp:
                tmp = Path(tmp)
                for rel, data in files.items():
                    p = tmp / rel
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(data)
                (tmp / "stage-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
                # Exclusive destination creation rejects an occupied/raced target.
                # Never delete a destination, including when publication fails.
                shutil.copytree(tmp, out, dirs_exist_ok=False)
        print(json.dumps(report, indent=2))
    except (OSError, ValueError, KeyError, TypeError, UnicodeError) as exc:
        print("ERROR: " + str(exc) + ". Nothing was installed or replaced.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
