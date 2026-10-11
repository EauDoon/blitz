"""Synthetic regression cases for the publication and preview audit repairs."""
import io
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile

from test_release import scanner, ROOT


def archive_bytes(body=b"ordinary", comment=b"", member_comment=b"", extra=b"", name="sample.txt", compression=zipfile.ZIP_DEFLATED):
    memory = io.BytesIO()
    with zipfile.ZipFile(memory, "w", compression=compression) as archive:
        entry = zipfile.ZipInfo(name)
        entry.comment, entry.extra = member_comment, extra
        archive.writestr(entry, body, compress_type=compression)
        archive.comment = comment
    return memory.getvalue()


class AuditSecurityChecks(unittest.TestCase):
    def test_zip_payload_and_metadata_are_not_silent(self):
        token = ("gh" + "p_" + "x" * 36).encode()
        cases = {
            "body": archive_bytes(body=token),
            "archive comment": archive_bytes(comment=token),
            "member comment": archive_bytes(member_comment=token),
            "filename": archive_bytes(name=token.decode() + ".txt"),
            "trailer": archive_bytes() + token,
            "prefix": token + archive_bytes(),
            "extra": archive_bytes(extra=struct.pack("<HH", 0xCAFE, len(token)) + token),
        }
        for name, data in cases.items():
            with self.subTest(name=name):
                rules = scanner.scan_bytes("synthetic.zip", data)
                self.assertTrue(any("github-token" in rule for rule in rules), rules)
                self.assertNotIn(token.decode(), str(rules))

    def test_clean_stored_deflated_and_nested_zip_pass(self):
        for compression in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
            self.assertEqual(scanner.scan_bytes("ordinary.zip", archive_bytes(compression=compression)), set())
        self.assertEqual(scanner.scan_bytes("ordinary.zip", archive_bytes(body=archive_bytes(), name="inner.zip")), set())

    def test_opaque_metadata_and_unsupported_compression_require_review(self):
        for data in (archive_bytes(comment=b"\xff"), archive_bytes(member_comment=b"\xff"),
                     archive_bytes(extra=struct.pack("<HH", 0xCAFE, 2) + b"ok"),
                     archive_bytes(compression=zipfile.ZIP_BZIP2), archive_bytes() + b"unaccounted"):
            self.assertTrue(scanner.scan_bytes("opaque.zip", data))

    def test_zip_limits_and_invalid_crc_fail(self):
        nested = archive_bytes(body=archive_bytes(body=archive_bytes(), name="third.zip"), name="second.zip")
        self.assertTrue(any("nested-archive-limit" in r for r in scanner.scan_bytes("first.zip", nested)))
        data = bytearray(archive_bytes(body=b"ordinary", compression=zipfile.ZIP_STORED))
        data[data.index(b"ordinary")] ^= 1
        self.assertIn("invalid-or-unreadable-archive", scanner.scan_bytes("bad.zip", bytes(data)))

    def test_shallow_history_is_non_success_without_fetching(self):
        with tempfile.TemporaryDirectory(prefix="blitz-shallow-check-") as raw:
            base = Path(raw)
            source, shallow = base / "source", base / "shallow"
            source.mkdir()
            env = {**os.environ, "GIT_AUTHOR_NAME": "Synthetic", "GIT_AUTHOR_EMAIL": "test@example.invalid",
                   "GIT_COMMITTER_NAME": "Synthetic", "GIT_COMMITTER_EMAIL": "test@example.invalid"}
            def git(*args):
                return subprocess.run(["git", "-C", str(source), *args], env=env, check=True, capture_output=True)
            git("init", "--quiet")
            for value in ("gh" + "p_" + "x" * 36, "ordinary current text"):
                (source / "sample.txt").write_text(value, encoding="utf-8")
                git("add", ".")
                git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Synthetic fixture")
            self.assertEqual(scanner.scan(source)["result"], "fail")
            git("-c", "protocol.file.allow=always", "clone", "--quiet", "--depth=1", source.as_uri(), str(shallow))
            before = (shallow / ".git/shallow").read_bytes()
            report = scanner.scan(shallow)
            self.assertEqual(report["reason"], "incomplete-shallow-history")
            self.assertEqual(report["result"], "fail")
            result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/check_publication.py"), "--repo", str(shallow)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["reason"], "incomplete-shallow-history")
            self.assertEqual((shallow / ".git/shallow").read_bytes(), before)

    def test_preview_http_boundaries(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node is required for the preview security gate")
        result = subprocess.run([node, "--test", str(ROOT / "tests/node/test_preview.mjs")], capture_output=True, text=True, encoding="utf-8", timeout=45)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        if os.name != "nt":
            self.assertIn("skipped 0", result.stdout, "Linux must exercise symlink cases")
        print(result.stdout)


if __name__ == "__main__":
    unittest.main()
