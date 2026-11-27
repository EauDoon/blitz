#!/usr/bin/env python3
"""Verify a Blitz ZIP; optionally open verified bytes into a new task directory.

Standalone standard library only. Extraction requires a separately trusted
archive SHA-256, never executes content, and retains the Blitz/ prefix.
"""
import argparse
import ctypes
import hashlib
import io
import json
import ntpath
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import stat
import sys
import tempfile
import unicodedata
import zipfile


MAX_FILE = 64 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_FILES = 4096
MAX_ARCHIVE = MAX_TOTAL + (MAX_FILES + 1) * 1024
LIVE_PARTS = {".codex", ".claude", ".agents", ".aws", ".ssh", "plugins", "skills"}
# Local secrets and interpreter caches the repository ignores; a manifest that lists one
# would carry it into every release built from that manifest.
IGNORED_PART = re.compile(r"(\.env(\..*)?|\.ds_store|__pycache__|.*\.py[cod])")
LIMITS = ("Integrity and safe opening only; no content execution, installation, "
          "native loading, routing, permission or secret-free certification. "
          "Use a stable local filesystem, not an adversarially changing directory.")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_relative(name):
    if not isinstance(name, str) or not name:
        return False
    path = PurePosixPath(name)
    if (path.is_absolute() or path.as_posix() != name or "\\" in name
            or unicodedata.normalize("NFC", name) != name
            or re.search(r'[\x00-\x1f\x7f<>:"|?*]', name)):
        return False
    for part in path.parts:
        stem = part.split(".", 1)[0].rstrip(" ").upper()
        if (part in {".", ".."} or part.endswith((".", " ")) or re.fullmatch(
                r"CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[1-9\u00b9\u00b2\u00b3]|LPT[1-9\u00b9\u00b2\u00b3]", stem)):
            return False
    return True


def unique_paths(names):
    seen = set()
    for name in names:
        require(safe_relative(name), "unsafe path:" + str(name))
        key = name.casefold()
        require(key not in seen, "duplicate or case collision:" + name)
        seen.add(key)
    for name in names:
        require(not any(parent.as_posix().casefold() in seen
                        for parent in PurePosixPath(name).parents if parent.as_posix() != "."),
                "file directory collision:" + name)


def load_json(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate JSON key:" + key)
            result[key] = value
        return result
    def nonfinite(value):
        raise ValueError("nonfinite JSON value:" + value)
    try:
        return json.loads(data, object_pairs_hook=unique, parse_constant=nonfinite)
    except RecursionError as exc:
        raise ValueError("JSON nesting is too deep") from exc


def validate_manifest(manifest):
    require(isinstance(manifest, dict), "manifest must be an object")
    rows = manifest.get("files")
    require(isinstance(rows, list) and 1 <= len(rows) <= MAX_FILES, "invalid manifest file count")
    for key in ("kit", "version"):
        if key in manifest:
            require(isinstance(manifest[key], str) and bool(manifest[key].strip()), "invalid manifest " + key)
    if "kit" in manifest:
        require(manifest["kit"] == "Blitz", "wrong manifest kit")
    if "schema_version" in manifest:
        require(type(manifest["schema_version"]) is int and manifest["schema_version"] > 0,
                "invalid manifest schema version")
    files = {}
    for row in rows:
        require(isinstance(row, dict) and {"path", "bytes", "sha256"} <= set(row)
                and set(row) <= {"path", "bytes", "sha256", "characters"}, "malformed file row")
        name = row["path"]
        require(safe_relative(name), "unsafe path:" + str(name))
        require(not any(IGNORED_PART.fullmatch(part.casefold()) for part in PurePosixPath(name).parts),
                "ignored local file in manifest:" + name)
        require(PurePosixPath(name).parts[0].casefold() != "manifest.json", "self-referential manifest row")
        require(name not in files, "duplicate manifest row:" + name)
        require(isinstance(row["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]),
                "invalid SHA-256:" + name)
        require(type(row["bytes"]) is int and 0 <= row["bytes"] <= MAX_FILE, "invalid byte size:" + name)
        if "characters" in row:
            require(row["characters"] is None or (type(row["characters"]) is int
                    and 0 <= row["characters"] <= MAX_FILE), "invalid character count:" + name)
        files[name] = row
    unique_paths(list(files))
    require(sum(row["bytes"] for row in files.values()) <= MAX_TOTAL, "oversize manifest payload")
    licenses = manifest.get("licenses", [])
    require(isinstance(licenses, list) and all(isinstance(name, str) for name in licenses), "invalid licenses")
    require(len(set(licenses)) == len(licenses), "duplicate license")
    for name in licenses:
        require(name in files, "missing licence:" + name)
    return files


def validate_payload(name, data, row):
    require(hashlib.sha256(data).hexdigest() == row["sha256"], "hash mismatch:" + name)
    require(len(data) == row["bytes"], "byte size mismatch:" + name)
    if "characters" in row:
        try:
            characters = len(data.decode("utf-8"))
        except UnicodeDecodeError:
            characters = None
        require(characters == row["characters"], "character count mismatch:" + name)


def windows_reserved(component):
    """Windows device-name check on every host; 3.13+ deprecates the pathlib form."""
    if hasattr(ntpath, "isreserved"):
        return ntpath.isreserved(component)
    return PureWindowsPath(component).is_reserved()


def guard_local_path(raw, must_exist=True):
    """Reject host aliases and every existing symlink/reparse ancestor."""
    text = os.fspath(raw)
    require("//" not in text and "\\\\" not in text, "network or repeated separator path")
    for component in re.split(r"[\\/]", text):
        if not component or re.fullmatch(r"[A-Za-z]:", component):
            continue
        require(component not in {".", ".."} and not component.endswith((".", " "))
                and not re.search(r'[\x00-\x1f\x7f:*?"<>|]', component)
                and not windows_reserved(component), "unsafe local path component:" + component)
    path = Path(text).absolute()
    for part in [*reversed(path.parents), path]:
        if os.path.lexists(part):
            info = part.lstat()
            require(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
                    "symlink or reparse path:" + str(part))
    require(not must_exist or path.exists(), "missing path:" + str(path))
    require(os.path.normcase(str(path)) == os.path.normcase(str(path.resolve(strict=must_exist))),
            "aliased local path:" + str(path))
    return path


def validate_destination(raw):
    out = guard_local_path(raw, must_exist=False)
    require(out != Path(out.anchor) and out != Path.home(), "root or home output is prohibited")
    require(not any(part.casefold() in LIVE_PARTS for part in out.parts), "live configuration output is prohibited")
    require(out.parent.is_dir(), "output parent must already exist")
    require(not os.path.lexists(out), "output occupied; nothing was replaced")
    return out


def publish_directory(stage, out):
    """Atomic no-replace directory rename on Windows/Linux, fail elsewhere."""
    stage, out = Path(stage), Path(out)
    require(not os.path.lexists(out), "output occupied; nothing was replaced")
    if os.name == "nt":
        os.rename(stage, out)  # Windows rename fails even for an existing empty directory.
    elif sys.platform.startswith("linux"):
        libc = ctypes.CDLL(None, use_errno=True)
        rename = getattr(libc, "renameat2", None)
        if rename is None:
            raise OSError("atomic no-replace directory publication unavailable")
        rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        rename.restype = ctypes.c_int
        if rename(-100, os.fsencode(stage), -100, os.fsencode(out), 1) != 0:
            code = ctypes.get_errno()
            raise OSError(code, os.strerror(code), str(out))
    else:
        raise OSError("atomic no-replace directory publication supports Windows and Linux only")


def read_archive(path):
    if hasattr(path, "read"):
        data = path.read(MAX_ARCHIVE + 1)
    else:
        path = guard_local_path(path)
        require(path.is_file() and stat.S_ISREG(path.stat().st_mode), "archive is not a regular file")
        require(path.stat().st_size <= MAX_ARCHIVE, "oversize archive bytes")
        with path.open("rb") as stream:
            data = stream.read(MAX_ARCHIVE + 1)
    require(len(data) <= MAX_ARCHIVE, "oversize archive bytes")
    return data


def validated_archive(data, expected_sha256=None):
    digest = hashlib.sha256(data).hexdigest()
    if expected_sha256 is not None:
        require(isinstance(expected_sha256, str) and re.fullmatch(r"[0-9a-f]{64}", expected_sha256), "invalid expected SHA-256")
        require(digest == expected_sha256, "trusted archive hash mismatch")
    with zipfile.ZipFile(io.BytesIO(data)) as bundle:
        infos = bundle.infolist()
        require(len(infos) <= MAX_FILES + 1, "invalid archive count")
        unique_paths([info.filename for info in infos])
        total = 0
        for info in infos:
            name = info.filename
            require(name.startswith("Blitz/") and name != "Blitz/", "unsafe archive root:" + name)
            mode = stat.S_IFMT(info.external_attr >> 16)
            require(mode != stat.S_IFLNK, "symlink entry:" + name)
            require(not info.is_dir() and mode in {0, stat.S_IFREG} and not info.external_attr & 0x400,
                    "nonregular archive entry:" + name)
            require(not info.flag_bits & 1, "encrypted entry:" + name)
            require(0 <= info.file_size <= MAX_FILE, "oversize entry:" + name)
            total += info.file_size
        require(len(infos) >= 2, "invalid archive count")
        require(total <= MAX_TOTAL, "oversize archive")
        names = set(bundle.namelist())
        require("Blitz/manifest.json" in names, "missing manifest")
        manifest_bytes = bundle.read("Blitz/manifest.json")
        manifest = load_json(manifest_bytes)
        files = validate_manifest(manifest)
        require(names == {"Blitz/manifest.json", *("Blitz/" + name for name in files)}, "archive manifest membership mismatch")
        payload = {"Blitz/manifest.json": manifest_bytes}
        for name, row in files.items():
            content = bundle.read("Blitz/" + name)  # zipfile also validates CRC/local headers.
            validate_payload(name, content, row)
            payload["Blitz/" + name] = content
    return payload, {"result": "pass", "errors": [], "files": len(infos), "bytes": total,
                     "sha256": digest, "trusted_hash_verified": expected_sha256 is not None,
                     "limits": LIMITS}


def extract_payload(payload, raw):
    out = validate_destination(raw)
    # Only this invocation's temporary sibling is removed after failure.
    temp = tempfile.TemporaryDirectory(prefix=".blitz-open-", dir=out.parent)
    published, failure = False, None
    result = {"extracted_to": str(out)}
    try:
        stage = Path(temp.name) / "ready"
        stage.mkdir()
        for name, data in sorted(payload.items()):
            path = stage.joinpath(*PurePosixPath(name).parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            require(path.read_bytes() == data, "extracted byte mismatch:" + name)
        validate_destination(out)
        publish_directory(stage, out)
        published = True
    except BaseException as exc:
        failure = exc
        raise
    finally:
        try:
            temp.cleanup()
        except OSError as exc:
            warning = {"path": temp.name, "error": str(exc)}
            if published:
                result["cleanup_warning"] = warning
            elif failure is not None:
                failure.cleanup_warning = warning
            else:
                raise
    return result


def inspect_archive(path, expected_sha256=None, extract_to=None):
    try:
        require(extract_to is None or expected_sha256 is not None, "extraction requires a trusted expected SHA-256")
        payload, result = validated_archive(read_archive(path), expected_sha256)
        if extract_to is not None:
            result.update(extract_payload(payload, extract_to))
        return result
    except (OSError, ValueError, TypeError, KeyError, UnicodeError, zipfile.BadZipFile, RuntimeError, EOFError) as exc:
        result = {"result": "fail", "errors": [str(exc)], "limits": LIMITS}
        if getattr(exc, "cleanup_warning", None):
            result["cleanup_warning"] = exc.cleanup_warning
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive")
    parser.add_argument("--expected-sha256", help="separately trusted lowercase SHA-256")
    parser.add_argument("--extract-to", help="new task-local directory; requires --expected-sha256")
    args = parser.parse_args()
    result = inspect_archive(args.archive, args.expected_sha256, args.extract_to)
    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
