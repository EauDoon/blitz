#!/usr/bin/env python3
"""Check current tracked source or emitted artifacts for retired package branding.

History is deliberately excluded: this check never rewrites immutable commits.
Binary artwork still requires the separately recorded render/frame inspection.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile

RETIRED = re.compile(r"(?<![a-z])" + "th" + "or" + r"(?![a-z])", re.I)
MAX_BYTES = 64 * 1024 * 1024


def inspect(path, data, report, depth=0):
    report["files_checked"] += 1
    if RETIRED.search(path):
        report["findings"].append({"path": path, "rule": "retired-name-in-path"})
    if len(data) > MAX_BYTES:
        report["findings"].append({"path": path, "rule": "size-limit"})
        return
    if path.lower().endswith(".zip"):
        if depth >= 2:
            report["findings"].append({"path": path, "rule": "archive-depth-limit"})
            return
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            rows = archive.infolist()
            if len(rows) > 4096 or sum(row.file_size for row in rows) > 256 * 1024 * 1024:
                raise ValueError("Archive exceeds bounded identity scan")
            for row in rows:
                inspect(path + "!/" + row.filename, archive.read(row), report, depth + 1)
        return
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        report["binary_review_required"].append({"path": path, "sha256": hashlib.sha256(data).hexdigest()})
        return
    if RETIRED.search(text):
        report["findings"].append({"path": path, "rule": "retired-name-in-content"})


def scan(root, artifacts=False):
    root = Path(root).resolve()
    if artifacts:
        paths = sorted(path for path in root.rglob("*") if path.is_file())
    else:
        names = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"]).decode().split("\0")
        paths = [root / name for name in sorted(set(names)) if name and (root / name).is_file()]
    report = {"files_checked": 0, "findings": [], "binary_review_required": [],
              "scope": "emitted artifact names and decompressed bytes" if artifacts else "current source paths and text; no Git history"}
    for path in paths:
        if path.is_symlink():
            raise ValueError("Identity scan does not follow symlinks")
        inspect(path.relative_to(root).as_posix(), path.read_bytes(), report)
    report["result"] = "fail" if report["findings"] else ("partial" if report["binary_review_required"] else "pass")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--artifacts", action="store_true")
    args = parser.parse_args()
    try:
        report = scan(args.root, args.artifacts)
    except (OSError, ValueError, subprocess.SubprocessError, zipfile.BadZipFile) as error:
        report = {"result": "fail", "error": type(error).__name__}
    print(json.dumps(report, indent=2))
    return {"pass": 0, "partial": 2, "fail": 1}[report["result"]]


if __name__ == "__main__":
    raise SystemExit(main())
