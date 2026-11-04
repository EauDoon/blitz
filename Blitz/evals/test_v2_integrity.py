#!/usr/bin/env python3
"""v2 intake/opening regressions. Synthetic fixtures only, no external writes."""
import hashlib
import contextlib
import importlib.util
import io
import json
import os
import shutil
from pathlib import Path
import stat
import struct
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile


sys.dont_write_bytecode = True
SETUP = Path(__file__).resolve().parents[1] / "setup"
sys.path.insert(0, str(SETUP))
import verify_archive as archive
import verify_kit as kit
import export_item as item
from test_item_export import fixture as item_fixture, REVISION as ITEM_REVISION


def digest(data):
    return hashlib.sha256(data).hexdigest()


def row(name, data):
    return {"path": name, "bytes": len(data), "sha256": digest(data),
            "characters": len(data.decode("utf-8"))}


def bundle(payload=None, manifest=None, raw_manifest=None, modes=None, extras=None):
    payload = {"README.md": b"Synthetic"} if payload is None else payload
    if manifest is None:
        manifest = {"kit": "Blitz", "schema_version": 2,
                    "files": [row(name, data) for name, data in payload.items()], "licenses": []}
    memory = io.BytesIO()
    with zipfile.ZipFile(memory, "w") as output:
        for name, data in payload.items():
            info = zipfile.ZipInfo("Blitz/" + name)
            info.create_system = 3
            info.external_attr = ((modes or {}).get(name, stat.S_IFREG | 0o644)) << 16
            output.writestr(info, data)
        for name, data in (extras or {}).items():
            output.writestr(name, data)
        output.writestr("Blitz/manifest.json", raw_manifest if raw_manifest is not None
                        else json.dumps(manifest).encode())
    return memory.getvalue()


def inspect(data, **kwargs):
    return archive.inspect_archive(io.BytesIO(data), **kwargs)


class ArchiveTests(unittest.TestCase):
    def test_baseline_and_trusted_digest(self):
        data = bundle()
        self.assertEqual(inspect(data)["result"], "pass")
        self.assertTrue(inspect(data, expected_sha256=digest(data))["trusted_hash_verified"])
        self.assertEqual(inspect(data, expected_sha256="0" * 64)["result"], "fail")
        self.assertEqual(inspect(data, expected_sha256="invalid")["result"], "fail")

    def test_portable_path_corpus(self):
        cases = [["A.md", "a.md"], ["CON"], ["README.md."], ["cafe\u0301.md"],
                 ["README.md "], ["x:stream"], ["../escape"], ["/absolute"], ["x\\y"],
                 ["NUL.txt"], ["COM\u00b9.txt"], ["CONOUT$.log"], ["a", "a/b"],
                 ["Manifest.json"], ["manifest.json/inside"]]
        for names in cases:
            with self.subTest(names=names):
                self.assertEqual(inspect(bundle({name: b"x" for name in names}))["result"], "fail")

    def test_special_entries(self):
        for mode in (stat.S_IFIFO, stat.S_IFCHR, stat.S_IFBLK, stat.S_IFSOCK, stat.S_IFLNK, stat.S_IFDIR):
            with self.subTest(mode=mode):
                self.assertEqual(inspect(bundle(modes={"README.md": mode | 0o644}))["result"], "fail")

    def test_schema_corpus(self):
        valid = row("README.md", b"Synthetic")
        cases = [[], {"files": {}}, {"files": [7]}, {"files": []},
                 {"files": [valid, valid]}, {"files": [dict(valid, bytes=True)]},
                 {"files": [dict(valid, bytes=-1)]}, {"files": [dict(valid, characters=True)]},
                 {"files": [dict(valid, sha256="X" * 64)]}, {"files": [dict(valid, injected="bad")]},
                 {"files": [valid], "schema_version": True}, {"files": [valid], "kit": "Other"},
                 {"files": [valid], "licenses": "README.md"},
                 {"files": [valid], "licenses": ["missing"]},
                 {"files": [valid], "licenses": ["README.md", "README.md"]}]
        for manifest in cases:
            with self.subTest(manifest=manifest):
                self.assertEqual(inspect(bundle(manifest=manifest))["result"], "fail")

    def test_duplicate_json_keys_and_nonfinite(self):
        rows = json.dumps([row("README.md", b"Synthetic")])
        for text in ('{"files":[],"files":' + rows + '}', '{"files":' + rows + ',"invalid":NaN}',
                     '{"files":[{"path":"bad","path":"README.md","bytes":9,"sha256":"' +
                     digest(b"Synthetic") + '"}]}'):
            with self.subTest(text=text):
                self.assertEqual(inspect(bundle(raw_manifest=text.encode()))["result"], "fail")

    def test_membership_hash_byte_and_character_checks(self):
        valid = row("README.md", b"Synthetic")
        for altered in (dict(valid, path="missing.md"), dict(valid, sha256="0" * 64),
                        dict(valid, bytes=10), dict(valid, characters=10)):
            with self.subTest(altered=altered):
                self.assertEqual(inspect(bundle(manifest={"files": [altered]}))["result"], "fail")
        self.assertEqual(inspect(bundle(extras={"Blitz/unlisted.md": b"x"}))["result"], "fail")
        self.assertEqual(inspect(bundle(extras={"Elsewhere/file.md": b"x"}))["result"], "fail")

    def test_bounded_counts_and_sizes(self):
        data = bundle()
        for name, value in (("MAX_FILES", 0), ("MAX_FILE", 1), ("MAX_TOTAL", 1), ("MAX_ARCHIVE", 1)):
            with self.subTest(limit=name), patch.object(archive, name, value):
                self.assertEqual(inspect(data)["result"], "fail")

    def test_crc_and_encryption(self):
        data = bytearray(bundle())
        with zipfile.ZipFile(io.BytesIO(data)) as source:
            first = source.infolist()[0]
            offset = first.header_offset + 30 + len(first.filename.encode()) + len(first.extra)
        data[offset] ^= 1
        self.assertEqual(inspect(bytes(data))["result"], "fail")
        data = bytearray(bundle())
        for signature, flag_offset in ((b"PK\x03\x04", 6), (b"PK\x01\x02", 8)):
            offset = data.find(signature)
            flags = struct.unpack_from("<H", data, offset + flag_offset)[0]
            struct.pack_into("<H", data, offset + flag_offset, flags | 1)
        result = inspect(bytes(data))
        self.assertEqual(result["result"], "fail")
        self.assertIn("encrypted", result["errors"][0])


class DirectoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="v2-kit-")
        self.root = Path(self.temp.name)
        self.previous = kit.KIT
        kit.KIT = str(self.root)
        (self.root / "README.md").write_bytes(b"Synthetic")

    def tearDown(self):
        kit.KIT = self.previous
        self.temp.cleanup()

    def check(self, manifest=None, raw=None):
        if manifest is None:
            manifest = {"files": [row("README.md", b"Synthetic")]}
        (self.root / "manifest.json").write_bytes(raw if raw is not None else json.dumps(manifest).encode())
        failures = []
        kit.check_integrity(failures)
        return failures

    def test_directory_positive(self):
        self.assertEqual(self.check(), [])

    def test_unreadable_unlisted_subtree_fails_main(self):
        self.check()
        (self.root / "skills").mkdir()
        (self.root / "hidden").mkdir()
        (self.root / "hidden/unlisted").write_bytes(b"Synthetic")
        original = os.scandir
        def denied(path):
            if Path(path) == self.root / "hidden":
                raise PermissionError("synthetic unreadable subtree")
            return original(path)
        output = io.StringIO()
        with patch.object(os, "scandir", denied), contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as failure:
                kit.main()
        self.assertEqual(failure.exception.code, 1)
        self.assertIn("unreadable subtree", output.getvalue())
        self.assertNotIn("KIT OK", output.getvalue())

    def test_directory_schema_and_path_corpus(self):
        for name in ("CON", "cafe\u0301.md", "../escape", "README.md.", "x:stream", "manifest.json", "a/b"):
            with self.subTest(name=name):
                self.assertTrue(self.check({"files": [row(name, b"Synthetic")]}))
        valid = row("README.md", b"Synthetic")
        for rows in ([valid, dict(valid, path="readme.md")], [dict(valid, bytes=True)],
                     [dict(valid, characters=True)], [dict(valid, sha256="0" * 64)]):
            with self.subTest(rows=rows):
                self.assertTrue(self.check({"files": rows}))
        raw = ('{"files":[],"files":' + json.dumps([valid]) + '}').encode()
        self.assertTrue(self.check(raw=raw))

    def test_actual_unlisted_and_hardlinked_files(self):
        (self.root / "extra").write_bytes(b"x")
        self.assertTrue(self.check())
        (self.root / "extra").unlink()
        os.link(self.root / "README.md", self.root / "alias.md")
        self.assertTrue(any("hardlink" in error for error in self.check()))

    def test_reparse_guard(self):
        original = Path.lstat
        def marked(path):
            if path == self.root / "README.md":
                return SimpleNamespace(st_mode=stat.S_IFREG, st_file_attributes=0x400)
            return original(path)
        with patch.object(Path, "lstat", marked):
            self.assertTrue(any("reparse" in error for error in self.check()))

    def test_native_symlink_guard(self):
        outside = self.root / "outside.md"
        outside.write_bytes(b"private synthetic")
        (self.root / "README.md").unlink()
        try:
            (self.root / "README.md").symlink_to(outside)
        except OSError as error:
            self.skipTest("Native symlink fixture unavailable: " + str(error))
        self.assertTrue(any("symlink" in error for error in self.check()))


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="v2-open-")
        self.base = Path(self.temp.name)
        self.data = bundle({"README.md": b"Synthetic", "setup/never.py": b"raise RuntimeError('never execute')"})
        self.archive_path = self.base / "runtime.zip"
        self.archive_path.write_bytes(self.data)
        self.output = self.base / "opened"
        self.hash = digest(self.data)

    def tearDown(self):
        self.temp.cleanup()

    def invoke(self, expected=True):
        return archive.inspect_archive(self.archive_path, self.hash if expected else None, self.output)

    def assert_clean(self):
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.base.glob(".blitz-open-*")), [])

    def test_new_directory_only_and_exact_bytes(self):
        result = self.invoke()
        self.assertEqual(result["result"], "pass", result)
        self.assertEqual((self.output / "Blitz/README.md").read_bytes(), b"Synthetic")
        self.assertEqual((self.output / "Blitz/setup/never.py").read_bytes(),
                         b"raise RuntimeError('never execute')")
        self.assertEqual(archive.inspect_archive(self.archive_path)["result"], "pass")
        self.assertEqual(list(self.base.glob(".blitz-open-*")), [])

    def test_missing_trusted_hash_and_bad_bytes_make_no_output(self):
        self.assertEqual(self.invoke(False)["result"], "fail")
        self.assert_clean()
        self.archive_path.write_bytes(bundle({"CON": b"x"}))
        self.hash = digest(self.archive_path.read_bytes())
        self.assertEqual(self.invoke()["result"], "fail")
        self.assert_clean()

    def test_existing_nonempty_or_empty_directory_untouched(self):
        for marker in (False, True):
            with self.subTest(marker=marker):
                self.output.mkdir(exist_ok=True)
                if marker:
                    (self.output / "kept").write_bytes(b"user")
                self.assertEqual(self.invoke()["result"], "fail")
                self.assertTrue(self.output.is_dir())
                if marker:
                    self.assertEqual((self.output / "kept").read_bytes(), b"user")

    def test_write_failure_cleans_only_temporary_tree(self):
        original = Path.open
        def failed(path, mode="r", *args, **kwargs):
            if mode == "xb" and path.name == "never.py":
                raise OSError("injected write failure")
            return original(path, mode, *args, **kwargs)
        with patch.object(Path, "open", failed):
            self.assertEqual(self.invoke()["result"], "fail")
        self.assert_clean()
        self.assertEqual(self.invoke()["result"], "pass")

    def test_publication_failure_and_retry(self):
        with patch.object(archive, "publish_directory", side_effect=OSError("injected publication failure")):
            self.assertEqual(self.invoke()["result"], "fail")
        self.assert_clean()
        self.assertEqual(self.invoke()["result"], "pass")

    def test_cleanup_warning_preserves_open_result_or_original_failure(self):
        original = shutil.rmtree
        def denied(path, *args, **kwargs):
            if Path(path).name.startswith(".blitz-open-"):
                raise PermissionError("synthetic cleanup failure")
            return original(path, *args, **kwargs)
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(shutil, "rmtree", denied))
            # Some 3.12 builds bind tempfile._rmtree at import, past the shutil patch.
            if getattr(tempfile, "_rmtree", None) is original:
                stack.enter_context(patch.object(tempfile, "_rmtree", denied))
            with patch.object(archive, "publish_directory", side_effect=OSError("original publication failure")):
                failed = self.invoke()
            passed = self.invoke()
        self.assertEqual(failed["result"], "fail")
        self.assertEqual(failed["errors"], ["original publication failure"])
        self.assertTrue(Path(failed["cleanup_warning"]["path"]).is_dir())
        self.assertEqual(passed["result"], "pass")
        self.assertEqual(passed["sha256"], self.hash)
        self.assertEqual(passed["extracted_to"], str(self.output))
        self.assertTrue(Path(passed["cleanup_warning"]["path"]).is_dir())
        self.assertEqual((self.output / "Blitz/README.md").read_bytes(), b"Synthetic")

    def test_racing_output_is_not_replaced(self):
        original = archive.publish_directory
        def occupied(stage, out):
            out.mkdir()
            (out / "kept").write_bytes(b"racing user")
            return original(stage, out)
        with patch.object(archive, "publish_directory", occupied):
            self.assertEqual(self.invoke()["result"], "fail")
        self.assertEqual((self.output / "kept").read_bytes(), b"racing user")
        self.assertEqual(list(self.base.glob(".blitz-open-*")), [])

    def test_live_destination_and_path_alias_rejected(self):
        for bad in (self.base / ".codex" / "opened", str(self.base / "opened") + ".",
                    str(self.base) + "/../opened"):
            with self.subTest(bad=bad):
                result = archive.inspect_archive(self.archive_path, self.hash, bad)
                self.assertEqual(result["result"], "fail")
        self.assert_clean()

    def test_cli_exit_status(self):
        good = subprocess.run([sys.executable, "-B", str(SETUP / "verify_archive.py"),
                               str(self.archive_path), "--expected-sha256", self.hash],
                              capture_output=True, text=True, timeout=30)
        bad = subprocess.run([sys.executable, "-B", str(SETUP / "verify_archive.py"),
                              str(self.archive_path), "--extract-to", str(self.output)],
                             capture_output=True, text=True, timeout=30)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(bad.returncode, 1, bad.stderr)
        self.assert_clean()


class PlainCLITests(unittest.TestCase):
    def test_ordinary_verifier_and_stage_dry_run_do_not_write_bytecode(self):
        with tempfile.TemporaryDirectory(prefix="v2-plain-cli-") as temp:
            base = Path(temp)
            copied = base / "Blitz"
            shutil.copytree(SETUP.parent, copied, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            def snapshot():
                return {path.relative_to(copied).as_posix(): digest(path.read_bytes())
                        for path in copied.rglob("*") if path.is_file()}
            before = snapshot()
            environment = {name: value for name, value in os.environ.items()
                           if name.upper() not in {"PYTHONDONTWRITEBYTECODE", "PYTHONPYCACHEPREFIX"}}
            commands = [("stage-dry", [str(copied / "setup/chatgpt_stage.py"),
                                      "--out", str(base / "dry-output"), "--dry-run"]),
                        ("verify-kit", [str(copied / "setup/verify_kit.py")])]
            outcomes = []
            for label, arguments in commands:
                with self.subTest(command=label):
                    result = subprocess.run([sys.executable, *arguments], cwd=base, env=environment,
                                            capture_output=True, text=True, encoding="utf-8", timeout=60)
                    self.assertEqual(before, snapshot(), label + " changed the source tree")
                    self.assertEqual(list(copied.rglob("__pycache__")), [])
                    self.assertFalse((base / "dry-output").exists())
                    if label == "stage-dry":
                        self.assertEqual(result.returncode, 0, result.stderr)
                    else:
                        # Manifest freshness is the separate release gate; this also
                        # proves ordinary verification is read-only before refreeze.
                        self.assertIn(result.returncode, (0, 1), result.stderr)
                        self.assertIn("KIT OK" if result.returncode == 0 else "KIT FAILED", result.stdout)
                    outcomes.append({"command": label, "exit": result.returncode, "source_unchanged": True})
            print(json.dumps({"plain_cli_no_write": outcomes}), flush=True)


class ItemTrustTests(unittest.TestCase):
    def test_export_cleanup_warning_preserves_result_or_original_failure(self):
        with tempfile.TemporaryDirectory(prefix="v2-item-cleanup-") as temp:
            base = Path(temp)
            root, contract = item_fixture(base)
            config, output = base / "contract.json", base / "item.zip"
            config.write_text(json.dumps(contract), encoding="utf-8")
            original = Path.unlink
            def denied(path, *args, **kwargs):
                if path.name.startswith(".item-export-"):
                    raise PermissionError("synthetic cleanup failure")
                return original(path, *args, **kwargs)
            with patch.object(Path, "unlink", denied):
                with patch.object(os, "link", side_effect=OSError("original publication failure")):
                    with self.assertRaisesRegex(OSError, "original publication failure") as failed:
                        item.build_archive(root, config, output, ITEM_REVISION)
                self.assertFalse(output.exists())
                passed = item.build_archive(root, config, output, ITEM_REVISION)
            self.assertTrue(Path(failed.exception.cleanup_warning["path"]).is_file())
            self.assertEqual(passed["result"], "pass")
            self.assertEqual(passed["archive"], str(output))
            self.assertTrue(Path(passed["cleanup_warning"]["path"]).is_file())
            self.assertEqual(item.inspect_archive(output)["sha256"], passed["sha256"])

    def test_export_prohibited_nested_directory_variants(self):
        with tempfile.TemporaryDirectory(prefix="v2-item-denied-") as temp:
            base = Path(temp)
            root, contract = item_fixture(base)
            config, original = base / "contract.json", base / "original.zip"
            config.write_text(json.dumps(contract), encoding="utf-8")
            item.build_archive(root, config, original, ITEM_REVISION)
            with zipfile.ZipFile(original) as source:
                payload = {name: source.read(name) for name in source.namelist()}
            for directory in ("answer-key", "answer-keys", "answer_key", "builder-notes", "hidden-answers", "nested/Answer-Key"):
                with self.subTest(directory=directory):
                    name, data = directory + "/synthetic.json", b"Synthetic fixture only"
                    candidate = json.loads(json.dumps(contract))
                    entry = {"path": name, "sha256": digest(data), "revision": ITEM_REVISION,
                             "classification": "permitted", "role": "source", "dependencies": []}
                    candidate["files"].append(entry)
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
                    config.write_text(json.dumps(candidate), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "prohibited_path"):
                        item.build_archive(root, config, base / "denied.zip", ITEM_REVISION)
                    manifest = json.loads(payload["manifest.json"])
                    manifest["files"].append(dict(entry, bytes=len(data)))
                    tampered = base / "tampered.zip"
                    with zipfile.ZipFile(tampered, "w") as output:
                        for member, content in payload.items():
                            if member != "manifest.json":
                                output.writestr(member, content)
                        output.writestr(name, data)
                        output.writestr("manifest.json", json.dumps(manifest))
                    with self.assertRaisesRegex(ValueError, "prohibited_path"):
                        item.inspect_archive(tampered)

    def test_item_expected_digest_rejects_before_zip_parse(self):
        with tempfile.TemporaryDirectory(prefix="v2-item-trust-") as temp:
            path = Path(temp) / "not-a-zip.zip"
            path.write_bytes(b"not a zip")
            with self.assertRaisesRegex(ValueError, "trusted_archive_hash_mismatch"):
                item.inspect_archive(path, expected_sha256="0" * 64)
            with self.assertRaisesRegex(ValueError, "invalid_expected_hash"):
                item.inspect_archive(path, expected_sha256="bad")

    def test_item_nonfinite_json_rejected(self):
        with self.assertRaisesRegex(ValueError, "nonfinite"):
            item.load_json('{"bytes":NaN}')


if __name__ == "__main__":
    unittest.main(verbosity=2)
