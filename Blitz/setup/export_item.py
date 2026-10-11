#!/usr/bin/env python3
"""Build or inspect an allowlisted item ZIP without extracting or executing it."""
import argparse
import hashlib
import html
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile


MAX_FILE = 64 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_FILES = 4096
ROLES = {"record", "deliverable", "source", "method", "license", "verification", "runtime"}
DENIED_PARTS = {"private", "credentials", "secrets", ".git", ".aws", ".ssh",
                "__pycache__", "node_modules", "evals", "fixtures", "answer_keys",
                "hidden_answers", "grader", "builder_notes", "answer-key", "answer-keys",
                "answer_key", "builder-notes", "hidden-answers"}
LIMITS = ("Integrity and declared dependency checks only. No script execution, secret-free "
          "certification, permission verification, native loading, or behavioral portability proof.")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def load_json(data):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value, "duplicate_json_key:" + key)
            value[key] = item
        return value
    def nonfinite(value):
        raise ValueError("nonfinite_json_value:" + value)
    return json.loads(data, object_pairs_hook=unique, parse_constant=nonfinite)


def safe_path(name):
    require(isinstance(name, str) and bool(name), "invalid_path")
    path = PurePosixPath(name)
    require(not path.is_absolute() and path.as_posix() == name and
            all(part not in {".", ".."} for part in path.parts) and
            "\\" not in name and not re.search(r'[\x00-\x1f\x7f<>:"|?*]', name) and
            unicodedata.normalize("NFC", name) == name, "unsafe_path:" + name)
    for part in path.parts:
        stem = part.split(".", 1)[0].rstrip(" ").upper()
        require(not part.endswith((".", " ")) and not re.fullmatch(
            r"CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[1-9\u00b9\u00b2\u00b3]|LPT[1-9\u00b9\u00b2\u00b3]", stem),
                "unsafe_path:" + name)
    return name


def allowed_path(name):
    safe_path(name)
    parts = PurePosixPath(name).parts
    folded = [part.casefold() for part in parts]
    require(not any(part in DENIED_PARTS for part in folded), "prohibited_path:" + name)
    base = folded[-1]
    require(not (base == ".env" or base.startswith(".env.") or
                 base in {"id_rsa", "id_ed25519", "credentials.json", "secrets.json"} or
                 base.endswith((".key", ".pem", ".p12", ".pfx", ".pyc")) or
                 re.search(r"(?i)(?:^|[_ -])(private|answer[_ -]?keys?|builder[_ -]?notes)(?:[_. -]|$)", base)),
            "prohibited_path:" + name)
    require(not ("context" in folded[:-1] and re.match(r"^(06|07|08)(?:[ ._-]|$)", base)),
            "private_lane:" + name)
    return name


def no_links(path):
    """Reject links/reparse points on every existing component, including ancestors."""
    path = Path(os.path.abspath(path))
    for part in [*reversed(path.parents), path]:
        info = part.lstat()
        require(not stat.S_ISLNK(info.st_mode) and
                not getattr(info, "st_file_attributes", 0) & 0x400,
                "link_or_reparse:" + str(part))
    return path


def text_field(value, name):
    require(isinstance(value, str) and bool(value.strip()) and
            not re.search(r"[\x00-\x1f\x7f]", value), "invalid_field:" + name)


def validate_contract(contract, expected_revision=None):
    require(isinstance(contract, dict) and type(contract.get("schema_version")) is int and
            contract["schema_version"] == 1, "invalid_schema")
    require(set(contract) <= {"schema_version", "item_id", "revision", "blitz_version", "destination",
                             "review", "required_paths", "files", "prerequisites", "reference_exceptions",
                             "format", "limits", "external_access_required"}, "unknown_contract_field")
    for key in ("item_id", "revision", "blitz_version", "destination"):
        text_field(contract.get(key), key)
    if expected_revision is not None:
        require(contract["revision"] == expected_revision, "revision_mismatch")
    review = contract.get("review")
    require(isinstance(review, dict) and review.get("approved_for_export") is True and
            review.get("dependency_review_complete") is True, "export_review_required")
    require(set(review) == {"reviewed_by", "approved_for_export", "dependency_review_complete"},
            "unknown_review_field")
    text_field(review.get("reviewed_by"), "reviewed_by")
    rows = contract.get("files")
    require(isinstance(rows, list) and 2 <= len(rows) <= MAX_FILES, "invalid_files")
    files, names = {}, set()
    for row in rows:
        require(isinstance(row, dict), "invalid_file_row")
        require(set(row) <= {"path", "sha256", "revision", "classification", "role", "dependencies", "bytes"},
                "unknown_file_field")
        name = allowed_path(row.get("path"))
        require(PurePosixPath(name).parts[0].casefold() != "manifest.json", "reserved_manifest_path")
        require(name.casefold() not in names, "duplicate_or_case_collision:" + name)
        names.add(name.casefold())
        require(isinstance(row.get("sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]),
                "invalid_hash:" + name)
        if "bytes" in row:
            require(type(row["bytes"]) is int and 0 <= row["bytes"] <= MAX_FILE,
                    "invalid_bytes:" + name)
        text_field(row.get("revision"), "file_revision:" + name)
        require(row.get("classification") in {"public", "permitted"}, "prohibited_classification:" + name)
        require(row.get("role") in ROLES, "invalid_role:" + name)
        require(isinstance(row.get("dependencies"), list) and
                all(isinstance(x, str) for x in row["dependencies"]), "invalid_dependencies:" + name)
        files[name] = row
    for name in files:
        require(not any(parent.as_posix().casefold() in names for parent in PurePosixPath(name).parents
                        if parent.as_posix() != "."), "file_directory_collision:" + name)
    required = contract.get("required_paths")
    require(isinstance(required, list), "invalid_required_paths")
    for name in ["README.md", "PROJECT_INSTRUCTIONS.md", *required]:
        safe_path(name)
        require(name in files, "missing_required_path:" + name)
    prereqs = contract.get("prerequisites", [])
    require(isinstance(prereqs, list), "invalid_prerequisites")
    external = {}
    for row in prereqs:
        require(isinstance(row, dict), "invalid_prerequisite")
        require(set(row) <= {"id", "locator", "required", "status", "evidence"}, "unknown_prerequisite_field")
        for key in ("id", "locator"):
            text_field(row.get(key), "prerequisite_" + key)
        require(row["id"] not in external, "duplicate_prerequisite:" + row["id"])
        require(isinstance(row.get("required"), bool) and row.get("status") in
                {"verified", "unavailable", "not_tested"}, "invalid_prerequisite_status:" + row["id"])
        if row["required"] or row["status"] == "verified":
            require(row["status"] == "verified", "incomplete_prerequisite:" + row["id"])
            text_field(row.get("evidence"), "prerequisite_evidence:" + row["id"])
        external[row["id"]] = row
    for name, row in files.items():
        for dependency in row["dependencies"]:
            if dependency.startswith("external:"):
                key = dependency[9:]
                require(key in external and external[key]["required"], "undeclared_required_prerequisite:" + name)
            else:
                safe_path(dependency)
                require(dependency in files, "missing_dependency:" + name + ":" + dependency)
    exceptions = contract.get("reference_exceptions", [])
    require(isinstance(exceptions, list), "invalid_reference_exceptions")
    for row in exceptions:
        require(isinstance(row, dict) and row.get("source") in files and
                row.get("kind") == "nonrequired_example", "invalid_reference_exception")
        require(set(row) == {"source", "target", "kind", "reason"}, "unknown_reference_exception_field")
        text_field(row.get("target"), "reference_target")
        text_field(row.get("reason"), "reference_reason")
    return files, external


def markdown_targets(text):
    """Conservative common Markdown subset; ambiguous inline destinations fail closed."""
    targets = []
    for match in re.finditer(r"!?\[[^\]\n]*\]\(", text):
        start, index, depth = match.end(), match.end(), 1
        while index < len(text) and depth:
            if text[index] == "\\":
                index += 2
                continue
            if text[index] == "(":
                depth += 1
            elif text[index] == ")":
                depth -= 1
            index += 1
        require(depth == 0, "ambiguous_markdown_link")
        raw = text[start:index - 1].strip()
        if raw.startswith("<"):
            end = raw.find(">")
            require(end >= 0, "ambiguous_markdown_link")
            target = raw[1:end]
            tail = raw[end + 1:].strip()
        else:
            split = re.split(r"\s+", raw, maxsplit=1)
            target, tail = split[0], split[1] if len(split) > 1 else ""
        require(not tail or (len(tail) >= 2 and tail[0] in "\"'(" and
                             tail[-1] == {"\"": "\"", "'": "'", "(": ")"}[tail[0]]),
                "ambiguous_markdown_link")
        targets.append(re.sub(r"\\([() ])", r"\1", target))
    for match in re.finditer(r"(?m)^\s{0,3}\[[^\]\n]+\]:\s*(?:<([^>]+)>|(\S+))", text):
        targets.append(match.group(1) or match.group(2))
    for match in re.finditer(r"(?i)\b(?:href|src)\s*=\s*['\"]([^'\"]+)['\"]", text):
        targets.append(match.group(1))
    for match in re.finditer(r"(?i)<((?:https?|mailto):[^<>\s]+)>", text):
        targets.append(match.group(1))
    return targets


def validate_references(contract, payload, external):
    exceptions = {(row["source"], row["target"]) for row in contract.get("reference_exceptions", [])}
    dependencies = {row["path"]: row["dependencies"] for row in contract["files"]}
    for name, data in payload.items():
        if PurePosixPath(name).suffix.casefold() != ".md":
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("markdown_not_utf8:" + name) from exc
        for target in markdown_targets(text):
            if (name, target) in exceptions or target.startswith("#") or not target:
                continue
            normalized_target = html.unescape(target)
            url = urlsplit(normalized_target)
            if url.scheme in {"https", "http", "mailto"}:
                if url.hostname in {"chatgpt.com", "chat.openai.com"} and unquote(url.path).startswith(
                        ("/g/g-p-", "/c/", "/share/")):
                    require(any(html.unescape(row["locator"]) == normalized_target and row["required"] and
                                "external:" + key in dependencies[name] for key, row in external.items()),
                            "undeclared_project_reference:" + name)
                # Required remote access is a reviewed contract dependency, never inferred from a URL.
                continue
            require(not url.scheme and not url.netloc, "absolute_or_unsupported_reference:" + name)
            target_path = unquote(url.path)
            require(not target_path.startswith(("/", "\\")) and "\\" not in target_path,
                    "absolute_local_reference:" + name)
            parts = list(PurePosixPath(name).parent.parts)
            for part in target_path.split("/"):
                if part == "..":
                    require(bool(parts), "escaping_reference:" + name)
                    parts.pop()
                elif part not in {"", "."}:
                    parts.append(part)
            resolved = "/".join(parts)
            require(resolved in payload, "missing_local_reference:" + name + ":" + target)


def manifest_for(contract, payload):
    manifest = {key: value for key, value in contract.items()
                if key not in {"format", "limits", "external_access_required"}}
    manifest["format"] = "blitz-item-export-v1"
    manifest["files"] = [dict(row, bytes=len(payload[row["path"]]))
                         for row in sorted(contract["files"], key=lambda row: row["path"])]
    manifest["limits"] = LIMITS
    manifest["external_access_required"] = any(row["required"] for row in contract.get("prerequisites", []))
    return manifest


def inspect_archive(archive, expected_item_id=None, expected_revision=None, expected_sha256=None):
    archive = no_links(Path(archive))
    require(archive.is_file(), "archive_not_file")
    max_archive = MAX_TOTAL + (MAX_FILES + 1) * 1024
    require(archive.stat().st_size <= max_archive, "oversize_archive_bytes")
    with archive.open("rb") as stream:
        archive_data = stream.read(max_archive + 1)
    require(len(archive_data) <= max_archive, "oversize_archive_bytes")
    archive_hash = sha(archive_data)
    if expected_sha256 is not None:
        require(isinstance(expected_sha256, str) and re.fullmatch(r"[0-9a-f]{64}", expected_sha256),
                "invalid_expected_hash")
        require(archive_hash == expected_sha256, "trusted_archive_hash_mismatch")
    with zipfile.ZipFile(io.BytesIO(archive_data)) as bundle:
        infos = bundle.infolist()
        require(3 <= len(infos) <= MAX_FILES + 1, "invalid_archive_count")
        seen, total = set(), 0
        for info in infos:
            safe_path(info.filename)
            folded = info.filename.casefold()
            require(folded not in seen, "duplicate_or_case_collision:" + info.filename)
            seen.add(folded)
            mode = info.external_attr >> 16
            require(not info.is_dir() and (stat.S_IFMT(mode) in {0, stat.S_IFREG}) and
                    not info.external_attr & 0x400, "nonregular_archive_entry:" + info.filename)
            require(not info.flag_bits & 1, "encrypted_entry:" + info.filename)
            require(info.file_size <= MAX_FILE, "oversize_entry:" + info.filename)
            total += info.file_size
        require(total <= MAX_TOTAL, "oversize_archive")
        require("manifest.json" in bundle.namelist(), "missing_manifest")
        contract = load_json(bundle.read("manifest.json"))
        require(isinstance(contract, dict) and contract.get("format") == "blitz-item-export-v1",
                "invalid_archive_format")
        files, external = validate_contract(contract, expected_revision)
        require(contract.get("limits") == LIMITS and type(contract.get("external_access_required")) is bool and
                contract["external_access_required"] == any(row["required"] for row in external.values()),
                "manifest_declaration_mismatch")
        if expected_item_id is not None:
            require(contract["item_id"] == expected_item_id, "item_id_mismatch")
        require(set(bundle.namelist()) == {*files, "manifest.json"}, "archive_allowlist_mismatch")
        payload = {}
        for name, row in files.items():
            data = bundle.read(name)
            require(sha(data) == row["sha256"], "hash_mismatch:" + name)
            require(type(row.get("bytes")) is int and row["bytes"] == len(data), "byte_mismatch:" + name)
            payload[name] = data
        validate_references(contract, payload, external)
    return {"result": "pass", "item_id": contract["item_id"], "revision": contract["revision"],
            "files": len(payload), "bytes": sum(map(len, payload.values())),
            "sha256": archive_hash, "trusted_hash_verified": expected_sha256 is not None, "limits": LIMITS}


def build_archive(root, contract_path, output, expected_revision):
    root = no_links(Path(root))
    require(root.is_dir() and root.parent != root, "invalid_item_root")
    contract_path = no_links(Path(contract_path))
    require(contract_path.is_file(), "contract_not_file")
    contract = load_json(contract_path.read_bytes())
    files, external = validate_contract(contract, expected_revision)
    output = Path(os.path.abspath(output))
    require(output.suffix.casefold() == ".zip", "output_must_be_zip")
    parent = no_links(output.parent)
    require(parent.is_dir(), "output_parent_not_directory")
    require(not output.is_relative_to(root) and not root.is_relative_to(output), "output_in_item_root")
    require(not output.exists() and not output.is_symlink(), "output_exists")
    payload, total = {}, 0
    for name, row in files.items():
        source = no_links(root.joinpath(*PurePosixPath(name).parts))
        require(source.is_relative_to(root) and source != contract_path and source != output,
                "source_scope_violation:" + name)
        info = source.stat()
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "nonregular_or_hardlinked_file:" + name)
        require(info.st_size <= MAX_FILE, "oversize_entry:" + name)
        data = source.read_bytes()
        require(len(data) <= MAX_FILE and sha(data) == row["sha256"], "source_hash_drift:" + name)
        total += len(data)
        require(total <= MAX_TOTAL, "oversize_item")
        payload[name] = data
    validate_references(contract, payload, external)
    manifest = manifest_for(contract, payload)
    payload["manifest.json"] = json_bytes(manifest)
    handle, temporary_name = tempfile.mkstemp(prefix=".item-export-", suffix=".zip", dir=parent)
    temporary = Path(temporary_name)
    published, failure = False, None
    try:
        with os.fdopen(handle, "w+b") as stream:
            with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
                for name, data in sorted(payload.items()):
                    info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
                    info.create_system = 3
                    info.external_attr = (stat.S_IFREG | 0o644) << 16
                    info.compress_type = zipfile.ZIP_DEFLATED
                    bundle.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            stream.flush()
            os.fsync(stream.fileno())
        result = inspect_archive(temporary, contract["item_id"], expected_revision)
        no_links(parent)
        # A hard-link publication is atomic and fails if the destination already exists.
        # No overwrite fallback: filesystems without this primitive must use another destination.
        result = dict(result, archive=str(output))
        os.link(temporary, output)
        published = True
    except BaseException as exc:
        failure = exc
        raise
    finally:
        try:
            temporary.unlink(missing_ok=True)
        except OSError as exc:
            warning = {"path": str(temporary), "error": str(exc)}
            if published:
                result["cleanup_warning"] = warning
            elif failure is not None:
                failure.cleanup_warning = warning
            else:
                raise
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build")
    for field in ("root", "contract", "output", "expected-revision"):
        build.add_argument("--" + field, required=True)
    inspect = commands.add_parser("inspect")
    inspect.add_argument("archive")
    inspect.add_argument("--expected-item-id")
    inspect.add_argument("--expected-revision")
    inspect.add_argument("--expected-sha256", help="separately trusted lowercase archive SHA-256")
    args = parser.parse_args()
    try:
        if args.command == "build":
            result = build_archive(args.root, args.contract, args.output, args.expected_revision)
        else:
            result = inspect_archive(args.archive, args.expected_item_id, args.expected_revision, args.expected_sha256)
    except (OSError, ValueError, TypeError, KeyError, zipfile.BadZipFile, RuntimeError) as exc:
        result = {"result": "fail", "errors": [str(exc)], "limits": LIMITS}
        if getattr(exc, "cleanup_warning", None):
            result["cleanup_warning"] = exc.cleanup_warning
    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
