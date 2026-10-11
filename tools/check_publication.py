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
import struct
import subprocess
import sys
import zipfile
import zlib

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
# Exact reviewed source artwork versions only, including retained Git history.
# Changed bytes and other paths still fail.
# Frame, metadata and authorship notes: docs/assets/README.md.
REVIEWED_MEDIA = {
    "docs/assets/blitz-motion.gif": frozenset({
        "bb4153ee9d024d2e242f439b596d5dcb508154c8d7941c8d33dea427aa29a65b",
        "6fa3b6b19fe0d2c89168870306b9cc1cf4b067648f0e9476d321532e62ee1116",
        "cf2cac59867c7a9d72e3f26eaff1b84b9006d560a483b6bd9dc8bc8294e9e5a9",
    }),
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


def text_rules(text):
    rules = {name for name, pattern in PATTERNS.items() if pattern.search(text)}
    if "\x00" in text:
        rules.add("binary-requires-human-review")
    words = re.findall(r"[a-z0-9]+", text.lower())
    grams = set(words) | {a + " " + b for a, b in zip(words, words[1:])}
    if any(hashlib.sha256(value.encode()).hexdigest()[:16] in RESTRICTED for value in grams):
        rules.add("restricted-term-fingerprint")
    return rules


def zip_metadata_rules(archive, data):
    """Account for every non-payload span of an ordinary single-disk ZIP.

    Comments/names are scanned. Extra fields, gaps and unsupported structures
    require review; they never receive a publication pass merely as opaque bytes.
    Payload bytes are decompressed, CRC-checked and scanned separately below.
    """
    rules = set()
    def metadata(label, value, encoding="utf-8"):
        try:
            text = value.decode(encoding)
        except UnicodeDecodeError:
            rules.add(label + ":opaque-metadata-requires-review")
            text = value.decode("latin-1") # Still detect known ASCII patterns.
        rules.update(label + ":" + rule for rule in text_rules(text))
    def extra(label, value):
        if value:
            rules.add(label + ":extra-fields-require-review")
            metadata(label, value)
    rows = archive.infolist()
    cursor = 0
    for index, row in enumerate(sorted(rows, key=lambda item: item.header_offset)):
        label = "archive-local-" + str(index)
        start = row.header_offset
        if start != cursor:
            rules.add("archive-prefix-or-unaccounted-bytes")
            metadata(label + "-gap", data[cursor:start])
        if start < cursor or start + 30 > len(data):
            raise ValueError("Overlapping or truncated ZIP local header")
        header = struct.unpack_from("<4s5H3I2H", data, start)
        if header[0] != b"PK\x03\x04":
            raise ValueError("Invalid ZIP local header")
        name_end = start + 30 + header[9]
        payload_start = name_end + header[10]
        if payload_start > archive.start_dir:
            raise ValueError("Truncated ZIP local metadata")
        metadata(label + "-name", data[start + 30:name_end], "utf-8" if header[2] & 0x800 else "cp437")
        extra(label, data[name_end:payload_start])
        cursor = payload_start + row.compress_size
        payload = data[payload_start:cursor]
        if len(payload) != row.compress_size:
            raise ValueError("Truncated ZIP payload")
        if row.file_size > MAX_BLOB:
            rules.add("oversized-archive-member-not-scanned")
        elif row.compress_type == zipfile.ZIP_STORED:
            if len(payload) != row.file_size:
                rules.add("inconsistent-stored-archive-member")
        elif row.compress_type == zipfile.ZIP_DEFLATED:
            inflater = zlib.decompressobj(-15)
            expanded = inflater.decompress(payload, MAX_BLOB + 1)
            if not inflater.eof or inflater.unused_data or inflater.unconsumed_tail or len(expanded) != row.file_size:
                rules.add("incomplete-or-extra-compressed-member-bytes")
            del expanded
        else:
            rules.add("unsupported-archive-compression-requires-review")
        if header[2] & 8:
            # Supported 32-bit descriptor, with or without its optional signature.
            if data[cursor:cursor + 4] == b"PK\x07\x08":
                cursor += 4
            if cursor + 12 > len(data) or struct.unpack_from("<III", data, cursor) != (row.CRC, row.compress_size, row.file_size):
                rules.add("unsupported-archive-data-descriptor")
            cursor += 12
        if cursor > archive.start_dir:
            raise ValueError("ZIP payload overlaps directory")
    if cursor != archive.start_dir:
        rules.add("archive-prefix-or-unaccounted-bytes")
        metadata("archive-directory-gap", data[cursor:archive.start_dir])
    cursor = archive.start_dir
    for index, row in enumerate(rows):
        if cursor + 46 > len(data):
            raise ValueError("Truncated ZIP directory")
        header = struct.unpack_from("<4s6H3I5H2I", data, cursor)
        if header[0] != b"PK\x01\x02":
            raise ValueError("Invalid ZIP directory")
        name_end = cursor + 46 + header[10]
        extra_end = name_end + header[11]
        comment_end = extra_end + header[12]
        if comment_end > len(data):
            raise ValueError("Truncated ZIP directory metadata")
        label = "archive-central-" + str(index)
        metadata(label + "-name", data[cursor + 46:name_end], "utf-8" if header[3] & 0x800 else "cp437")
        extra(label, data[name_end:extra_end])
        metadata(label + "-comment", data[extra_end:comment_end])
        if header[13] != 0:
            rules.add("unsupported-multidisk-archive")
        cursor = comment_end
    if cursor + 22 > len(data) or data[cursor:cursor + 4] != b"PK\x05\x06":
        # ZIP64/footer extensions are outside this bounded ordinary-ZIP contract.
        rules.add("unsupported-archive-footer-requires-review")
        metadata("archive-footer", data[cursor:])
        return rules
    end = struct.unpack_from("<4s4H2IH", data, cursor)
    if end[1:5] != (0, 0, len(rows), len(rows)) or end[5] != cursor - archive.start_dir or end[6] != archive.start_dir:
        rules.add("inconsistent-archive-directory")
    archive_end = cursor + 22 + end[7]
    if archive_end > len(data):
        raise ValueError("Truncated ZIP comment")
    metadata("archive-comment", data[cursor + 22:archive_end])
    if archive_end != len(data):
        rules.add("archive-trailing-bytes-require-review")
        metadata("archive-trailer", data[archive_end:])
    return rules


def scan_bytes(path, data, depth=0):
    findings = set(path_rules(path, data)) | text_rules(path)
    if len(data) > MAX_BLOB:
        return findings | {"oversized-blob-not-scanned"}
    if data.startswith((b"PK\x03\x04", b"PK\x05\x06")) or path.lower().endswith(".zip"):
        if depth >= 2:
            return findings | {"nested-archive-limit"}
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                rows = archive.infolist()
                if len(rows) > 4096 or sum(row.file_size for row in rows) > MAX_ZIP_TOTAL:
                    return findings | {"archive-size-limit"}
                findings.update(zip_metadata_rules(archive, data))
                for index, row in enumerate(rows):
                    # Numeric member identities avoid echoing a credential-like filename.
                    label = "archive-member-" + str(index)
                    findings.update(label + ":name:" + rule for rule in text_rules(row.orig_filename))
                    allowed_types = {0, stat.S_IFREG, stat.S_IFDIR} if row.is_dir() else {0, stat.S_IFREG}
                    if row.flag_bits & 1 or row.file_size > MAX_BLOB or stat.S_IFMT(row.external_attr >> 16) not in allowed_types or (row.is_dir() and row.file_size):
                        findings.update(label + ":" + rule for rule in path_rules(row.filename, b""))
                        findings.add(label + ":unscannable-archive-member")
                        continue
                    for rule in scan_bytes(row.filename, archive.read(row), depth + 1):
                        findings.add(label + ":" + rule)
        except (OSError, ValueError, RuntimeError, struct.error, zlib.error, zipfile.BadZipFile, NotImplementedError):
            findings.add("invalid-or-unreadable-archive")
        return findings
    expected_media = REVIEWED_MEDIA.get(path)
    if depth == 0 and expected_media and hashlib.sha256(data).hexdigest() in expected_media:
        return findings  # Path and size checks still apply; archives get no exception.
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return findings | {"binary-requires-human-review"}
    findings.update(text_rules(text))
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
    if git(root, "rev-parse", "--is-shallow-repository").strip() != b"false":
        return {"result": "fail", "reason": "incomplete-shallow-history", "findings": [],
                "limits": "A shallow checkout cannot satisfy publication history verification. No history was fetched."}
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
    # Legacy grafts can prune rev-list without marking a checkout shallow.
    # Validate the raw parent closure, unaffected by graft traversal rules.
    for identity in sorted(commits):
        data = objects[identity]["data"]
        if data is None:
            continue  # The oversized-object finding below still blocks publication.
        for line in data.split(b"\n\n", 1)[0].split(b"\n"):
            if line.startswith(b"parent "):
                parent = line[7:]
                if not re.fullmatch(rb"[0-9a-f]{40}|[0-9a-f]{64}", parent) or parent.decode("ascii") not in commits:
                    return {"result": "fail", "reason": "incomplete-parent-history", "findings": [],
                            "limits": "Raw commit parents are missing from the scanned history. Grafts or incomplete traversal cannot satisfy publication verification. No history was fetched."}
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
    # Keep ordinary paths useful, but never echo recognized secret-like path text.
    for row in findings:
        if text_rules(row["path"]):
            row["path"] = "<redacted-path-sha256:" + hashlib.sha256(os.fsencode(row["path"])).hexdigest() + ">"
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
