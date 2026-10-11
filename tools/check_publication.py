#!/usr/bin/env python3
"""Scan tracked bytes, staged blobs and all reachable Git history before a push.

Findings disclose only paths, origins and rule names, never matched values.
This bounded heuristic complements human review; it is not a secret-free certificate.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import zipfile

MAX_BLOB = 64 * 1024 * 1024
MAX_ZIP_TOTAL = 256 * 1024 * 1024
MAX_HISTORY_BYTES = 512 * 1024 * 1024
FORBIDDEN_PARTS = {".git", ".baseline", ".verification", ".dist", ".aws", ".ssh", ".codex",
                   ".agents", "node_modules", "__pycache__", "private", "secrets", "personal-notes",
                   "customer-data", "live-projects", "credentials"}
REVIEWED_PRIVATE_PATHS = {
    "Blitz/templates/context/06 Terms PRIVATE.md": "e4fbc9b438b1c1d9f614f5fdd534b193147794951c193dae623ec18bb9bfd07b",
    "Blitz/templates/context/07 Guardrails PRIVATE.md": "904141849f7ccfec2844ba8a1fe4a169fb4bd8f8bcedfefa049ca8e373fe3645",
    "Blitz/templates/context/08 Decision Frame PRIVATE.md": "70ba67354e6485adacc066872cdc3e267c56734145c2f24777c508d16bc59e15",
    "Blitz/evals/context-acquisition/cases/CA06/PRIVATE/owner-notes.md": "61e3de5e52a601bc396837556db110a68d5e9846205e39ef3ffa301c2ee42984",
}
# Exact reviewed source artwork only; changed bytes and other paths still fail.
# Frame, metadata and authorship notes: docs/assets/README.md.
REVIEWED_MEDIA = {
    "docs/assets/blitz-motion.gif": "bb4153ee9d024d2e242f439b596d5dcb508154c8d7941c8d33dea427aa29a65b",
}
# Existing kit restricted-term fingerprints; no private source names are embedded.
RESTRICTED = {"324ffbadc4c9f775", "b0442c88eea3fe5d", "040974aabfd1c691", "bc9a1a86ec98507e",
              "e999375bf16caa32", "848a37fa85f16979", "1b33caf91a913c55", "7603839d7c30c103",
              "997077f5a47a9efa", "6342a668c18d000b", "a932573e7ecf5cc3", "c213e91aeee06b20", "41c55ac752be450f"}
PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "openai-key": re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{24,}\b"),
    "aws-access-key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "slack-token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "local-user-path": re.compile(r"(?i)(?:[a-z]:[\\/]+Users[\\/]+[^\s\\/]+|/(?:Users|home)/[A-Za-z0-9_.-]+/)"),
    "credential-assignment": re.compile(r'''(?im)^\s*["']?(?:api_key|access_token|auth_token|client_secret|password)["']?\s*[:=]\s*["']?[^\s"'<>\[\]{}#]{20,}'''),
}


def git(root, *args, data=None):
    result = subprocess.run(["git", "--no-replace-objects", "-C", str(root), *args], input=data, capture_output=True, timeout=120)
    if result.returncode:
        raise ValueError("Git query failed: " + " ".join(args[:2]))
    return result.stdout


def path_rules(path, data):
    parts = PurePosixPath(path).parts
    private = any(part.casefold() in FORBIDDEN_PARTS for part in parts) or bool(re.search(r"(?i)(?:^|[ /_-])private(?:[ ._-]|$)", path))
    expected = REVIEWED_PRIVATE_PATHS.get(path)
    if private and (expected is None or hashlib.sha256(data).hexdigest() != expected):
        yield "private-or-generated-path"
    if any(part.casefold() == ".env" or part.casefold().startswith(".env.") for part in parts):
        yield "environment-file"
    if PurePosixPath(path).suffix.casefold() in {".pem", ".p12", ".pfx", ".key", ".db", ".sqlite", ".sqlite3", ".pyc"}:
        yield "sensitive-or-generated-file-type"
    if path.startswith("/") or "\\" in path or ".." in parts:
        yield "unsafe-path"


def scan_bytes(path, data, depth=0):
    findings = set(path_rules(path, data))
    if len(data) > MAX_BLOB:
        return findings | {"oversized-blob-not-scanned"}
    if data.startswith(b"PK\x03\x04") or path.lower().endswith(".zip"):
        if depth >= 2:
            return findings | {"nested-archive-limit"}
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                rows = archive.infolist()
                if len(rows) > 4096 or sum(row.file_size for row in rows) > MAX_ZIP_TOTAL:
                    return findings | {"archive-size-limit"}
                for row in rows:
                    if row.is_dir():
                        continue
                    if row.flag_bits & 1 or row.file_size > MAX_BLOB or stat.S_IFMT(row.external_attr >> 16) not in {0, stat.S_IFREG}:
                        findings.add("unscannable-archive-member:" + row.filename)
                        continue
                    for rule in scan_bytes(row.filename, archive.read(row), depth + 1):
                        findings.add("archive-member:" + row.filename + ":" + rule)
        except (OSError, ValueError, RuntimeError, zipfile.BadZipFile, NotImplementedError):
            findings.add("invalid-or-unreadable-archive")
        return findings
    expected_media = REVIEWED_MEDIA.get(path)
    if depth == 0 and expected_media and hashlib.sha256(data).hexdigest() == expected_media:
        return findings  # Path and size checks still apply; archives get no exception.
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return findings | {"binary-requires-human-review"}
    if "\x00" in text:
        findings.add("binary-requires-human-review")
    findings.update(name for name, pattern in PATTERNS.items() if pattern.search(text))
    words = re.findall(r"[a-z0-9]+", text.lower())
    grams = set(words) | {a + " " + b for a, b in zip(words, words[1:])}
    if any(hashlib.sha256(value.encode()).hexdigest()[:16] in RESTRICTED for value in grams):
        findings.add("restricted-term-fingerprint")
    return findings


def read_objects(root, identities):
    if not identities:
        return {}
    # Size-check every object type before reading content, including commit and tag text.
    order = sorted(identities)
    request = "".join(identity + "\n" for identity in order).encode()
    metadata = git(root, "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)", data=request)
    permitted, too_large, total, sizes, kinds = [], set(), 0, {}, {}
    for line in metadata.decode().splitlines():
        identity, kind, size = line.split()
        if identity not in identities or kind not in {"blob", "tree", "commit", "tag"}:
            raise ValueError("Unexpected Git object identity or type")
        kinds[identity] = kind
        total += int(size)
        if total > MAX_HISTORY_BYTES:
            raise ValueError("History exceeds scan memory budget; no complete scan claimed")
        if int(size) > MAX_BLOB:
            too_large.add(identity)
        else:
            permitted.append(identity)
            sizes[identity] = int(size)
    if set(kinds) != set(identities):
        raise ValueError("Incomplete Git object metadata")
    result = {identity: {"kind": kinds[identity], "data": None} for identity in too_large}
    # The aggregate byte limit was checked before reading any historical content.
    batches, batch, batch_bytes = [], [], 0
    for identity in permitted:
        if batch and batch_bytes + sizes[identity] > 8 * 1024 * 1024:
            batches.append(batch)
            batch, batch_bytes = [], 0
        batch.append(identity)
        batch_bytes += sizes[identity]
    if batch:
        batches.append(batch)
    for batch in batches:
        response = io.BytesIO(git(root, "cat-file", "--batch", data="".join(value + "\n" for value in batch).encode()))
        for identity in batch:
            header = response.readline().decode().strip().split()
            if header != [identity, kinds[identity], str(sizes[identity])]:
                raise ValueError("Unexpected Git batch identity")
            content = response.read(sizes[identity])
            if len(content) != sizes[identity] or response.read(1) != b"\n":
                raise ValueError("Truncated Git batch content")
            result[identity] = {"kind": kinds[identity], "data": content}
        if response.read(1):
            raise ValueError("Unexpected trailing Git batch data")
    return result


def scan(root):
    requested = Path(root).resolve()
    # Every query and worktree read must use the same complete repository root.
    # Git otherwise limits ls-files to a caller-supplied subtree silently.
    root = Path(os.fsdecode(git(requested, "rev-parse", "--show-toplevel")).rstrip("\r\n")).resolve(strict=True)
    tracked = [os.fsdecode(value) for value in git(root, "ls-files", "-z").split(b"\0") if value]
    if not tracked:
        raise ValueError("No tracked files; stage the intended repository files before scanning")
    findings = []
    def record(path, data, origin):
        rules = {"oversized-blob-not-scanned"} if data is None else scan_bytes(path, data)
        findings.extend({"path": path, "origin": origin, "rule": rule} for rule in sorted(rules))
    for path in tracked:
        file = root / path
        try:
            info = file.lstat()
            ancestors = [parent for parent in file.parents if parent != root and root in parent.parents]
            aliased = any(parent.is_symlink() or getattr(parent.lstat(), "st_file_attributes", 0) & 0x400
                          for parent in ancestors)
            if aliased or not stat.S_ISREG(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                findings.append({"path": path, "origin": "worktree", "rule": "nonregular-tracked-file"})
            else:
                record(path, file.read_bytes() if info.st_size <= MAX_BLOB else None, "worktree")
        except OSError:
            findings.append({"path": path, "origin": "worktree", "rule": "unreadable-tracked-file"})
    entries = set()
    for line in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if line:
            header, path = line.split(b"\t", 1)
            mode, identity, stage = header.decode().split()
            path = os.fsdecode(path)
            if mode not in {"100644", "100755"} or stage != "0":
                findings.append({"path": path, "origin": "index", "rule": "nonregular-or-unmerged-index-entry"})
            else:
                entries.add((path, identity, "index"))
    # Include annotated tags and objects referenced directly by refs, even when
    # no commit tree refers to them. Disable replacement-object indirection in git().
    reachable = set(git(root, "rev-list", "--objects", "--all", "--no-object-names").decode("ascii").splitlines())
    ref_objects = set(git(root, "for-each-ref", "--format=%(objectname)").decode("ascii").splitlines())
    reachable.update(ref_objects)
    index_objects = {identity for _, identity, _ in entries}
    objects = read_objects(root, reachable | index_objects)
    root_trees = {identity for identity in ref_objects if objects[identity]["kind"] == "tree"}
    commits = {identity for identity in reachable if objects[identity]["kind"] == "commit"}
    tags = {identity for identity in reachable if objects[identity]["kind"] == "tag"}
    for identity in sorted(commits | tags):
        obj = objects[identity]
        kind, data = obj["kind"], obj["data"]
        record("<" + kind + "-object>", data, "history-" + kind)
        if data is None:
            continue  # already a failing unscanned-size finding
        field = b"tree" if kind == "commit" else b"object"
        first_line = data.split(b"\n", 1)[0].split(b" ", 1)
        if len(first_line) != 2 or first_line[0] != field:
            raise ValueError("Invalid reachable commit/tag object header")
        target = first_line[1].decode("ascii")
        if target not in objects:
            raise ValueError("Incomplete reachable-object closure")
        if objects[target]["kind"] == "tree":
            root_trees.add(target)
    # Every historical root tree is expanded independently so one blob used under
    # multiple paths receives every path classification, including direct tree refs.
    for tree in sorted(root_trees):
        for line in git(root, "ls-tree", "-r", "-z", tree).split(b"\0"):
            if line:
                header, path = line.split(b"\t", 1)
                mode, kind, identity = header.decode().split()
                path = os.fsdecode(path)
                if kind != "blob" or mode not in {"100644", "100755"}:
                    findings.append({"path": path, "origin": "history", "rule": "nonregular-history-entry"})
                else:
                    if identity not in objects or objects[identity]["kind"] != "blob":
                        raise ValueError("Incomplete historical tree closure")
                    entries.add((path, identity, "history"))
    scanned_blobs = set()
    for path, identity, origin in sorted(entries):
        if objects[identity]["kind"] != "blob":
            raise ValueError("Expected staged or historical Git blob")
        record(path, objects[identity]["data"], origin)
        scanned_blobs.add(identity)
    for identity in sorted(reachable - scanned_blobs):
        obj = objects[identity]
        if obj["kind"] == "blob":
            record("<reachable-blob>", obj["data"], "history")
            scanned_blobs.add(identity)
        elif obj["kind"] == "tree" and obj["data"] is None:
            record("<tree-object>", None, "history-tree")
    return {"result": "fail" if findings else "pass", "tracked_files": len(tracked),
            "reachable_commits": len(commits), "reachable_tags": len(tags),
            "reachable_objects": len(reachable), "unique_blobs": len(scanned_blobs),
            "findings": findings,
            "limits": "Heuristic scan of the complete repository worktree/index, all ref-reachable blobs, commit/tag text, historical tree paths and bounded ZIP contents. Not a secret-free certificate; semantic privacy and authorization require human review."}



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        report = scan(args.repo)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        report = {"result": "fail", "error": str(error)}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
