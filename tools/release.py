#!/usr/bin/env python3
"""Build verified, reproducible Blitz archives in a new output directory."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "Blitz"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def archive_helper(kit):
    spec = importlib.util.spec_from_file_location("release_archive", kit / "setup/verify_archive.py")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    return helper


def run_python(script, *args):
    result = subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=180,
                            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"})
    if result.returncode:
        raise ValueError(f"{script.name} failed (exit {result.returncode}):\n" + result.stdout + result.stderr)
    return result.stdout


def snapshot(kit, helper):
    """Read only manifest-listed regular files after the complete kit gate."""
    manifest_data = (kit / "manifest.json").read_bytes()
    manifest = helper.load_json(manifest_data)
    listed = helper.validate_manifest(manifest)
    payload = {"manifest.json": manifest_data}
    for rel, row in sorted(listed.items()):
        path = helper.guard_local_path(kit / rel)
        info = path.lstat()
        helper.require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "nonregular source:" + rel)
        data = path.read_bytes()
        helper.validate_payload(rel, data, row)
        payload[rel] = data
    actual = {p.relative_to(kit).as_posix() for p in kit.rglob("*") if p.is_file()}
    helper.require(actual == set(payload), "source membership changed")
    return manifest, payload


def git_identity():
    def call(*args):
        try:
            result = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                                    text=True, encoding="utf-8", errors="replace", timeout=15)
            return result.stdout.strip() if result.returncode == 0 else None
        except (OSError, subprocess.TimeoutExpired):
            return None
    commit = call("rev-parse", "--verify", "HEAD")
    state = call("status", "--porcelain", "--untracked-files=no") if commit else None
    return {"commit": commit, "tracked_tree_dirty": None if state is None else bool(state)}


def build(out_raw, kit=KIT):
    kit = Path(kit).absolute()
    helper = archive_helper(kit)
    kit = helper.guard_local_path(kit)
    out = helper.validate_destination(out_raw)
    helper.require(out != kit and kit not in out.parents and out not in kit.parents,
                   "release output must not overlap the kit")
    run_python(kit / "setup/verify_kit.py")
    manifest, before = snapshot(kit, helper)
    version = manifest.get("version")
    helper.require(isinstance(version, str) and re.fullmatch(r"[0-9]+(?:\.[0-9]+)*OAI(?:-r[1-9][0-9]*)?", version),
                   "unsupported release version")
    archive_name = f"Blitz_v{version}.zip"
    with tempfile.TemporaryDirectory(prefix=".blitz-release-", dir=out.parent) as temporary:
        stage = Path(temporary)
        master = stage / archive_name
        with zipfile.ZipFile(master, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
            for rel, data in sorted(before.items()):
                entry = zipfile.ZipInfo("Blitz/" + rel, FIXED_TIME)
                entry.create_system = 3
                entry.external_attr = (stat.S_IFREG | 0o644) << 16
                bundle.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        master_hash = digest(master.read_bytes())
        checked = helper.inspect_archive(master, expected_sha256=master_hash)
        helper.require(checked["result"] == "pass", "master archive validation failed")
        runtime_output = run_python(kit / "setup/build_context.py", "--kit", kit,
                                    "--out", stage / "runtime")
        runtime_report = json.loads(runtime_output)
        helper.require(runtime_report.get("result") == "pass", "runtime compilation failed")
        runtimes = list((stage / "runtime").glob("*_Runtime.zip"))
        helper.require(len(runtimes) == 1 and runtimes[0].name == f"Blitz_v{version}_Runtime.zip",
                       "runtime version differs from release manifest")
        runtime_check = helper.inspect_archive(runtimes[0], expected_sha256=digest(runtimes[0].read_bytes()))
        helper.require(runtime_check["result"] == "pass", "runtime archive validation failed")
        run_python(kit / "setup/verify_kit.py")
        _, after = snapshot(kit, helper)
        helper.require(before == after, "source changed during release build")
        artifacts = []
        for path in sorted(stage.rglob("*")):
            if path.is_file():
                data = path.read_bytes()
                artifacts.append({"path": path.relative_to(stage).as_posix(), "bytes": len(data), "sha256": digest(data)})
        receipt = {"schema_version": 1, "kit": "Blitz", "version": version,
                   "source_manifest_sha256": digest(before["manifest.json"]),
                   "git": git_identity(), "artifacts": artifacts,
                   "verification": {"kit": "pass", "master": "pass", "runtime": "pass", "source_unchanged": True},
                   "limits": "Local packaging only. No installation, publication, host routing, company readiness or secret-free certification."}
        (stage / "release-manifest.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        helper.publish_directory(stage, out)
    return receipt


def artifact_hashes(root):
    root = Path(root)
    receipt = json.loads((root / "release-manifest.json").read_text(encoding="utf-8"))
    listed = receipt.get("artifacts")
    if not isinstance(listed, list) or not listed or receipt.get("kit") != "Blitz":
        raise ValueError("invalid release manifest")
    actual = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError("release comparison does not accept symlinks")
        if path.is_file() and path.relative_to(root).as_posix() != "release-manifest.json":
            data = path.read_bytes()
            actual[path.relative_to(root).as_posix()] = {"bytes": len(data), "sha256": digest(data)}
    expected = {}
    for row in listed:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256"} or row["path"] in expected:
            raise ValueError("invalid release artifact row")
        expected[row["path"]] = {"bytes": row["bytes"], "sha256": row["sha256"]}
    if actual != expected:
        raise ValueError("release artifacts differ from their manifest")
    if f"Blitz_v{receipt.get('version')}.zip" not in actual:
        raise ValueError("release master missing")
    return {path: row["sha256"] for path, row in actual.items()}


def compare(first, second):
    left, right = artifact_hashes(first), artifact_hashes(second)
    if not left or left != right:
        raise ValueError("release payloads differ or are empty")
    return {"result": "pass", "identical_artifacts": len(left), "sha256": left}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    package = commands.add_parser("build")
    package.add_argument("--out", required=True, help="new directory outside Blitz; parent must exist")
    check = commands.add_parser("compare")
    check.add_argument("first")
    check.add_argument("second")
    args = parser.parse_args()
    try:
        result = build(args.out) if args.command == "build" else compare(args.first, args.second)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print("Release failed: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
