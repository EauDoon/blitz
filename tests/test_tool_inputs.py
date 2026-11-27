"""Handled failures for hostile or mistaken tool input; synthetic data only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEEP = b"[" * 100000 + b"]" * 100000


def run(*args):
    return subprocess.run([sys.executable, "-B", *map(str, args)], capture_output=True, text=True)


class ToolInputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_scope_inspect_reports_deeply_nested_receipt_as_failure(self):
        projection = self.root / "projection"
        projection.mkdir()
        (projection / "projected.csv").write_bytes(b"item_id\nSYNTHETIC-A\n")
        (projection / "provenance.json").write_bytes(DEEP)
        result = run(ROOT / "Blitz/setup/scope_csv.py", "inspect", projection,
                     "--expected-receipt-sha256", hashlib.sha256(DEEP).hexdigest())
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "fail")
        self.assertIn("nesting is too deep", report["error"])

    def test_update_manifest_help_and_unknown_arguments_do_not_write(self):
        manifest = ROOT / "Blitz/manifest.json"
        before = manifest.read_bytes()
        stale = json.loads(before)
        stale["files"] = stale["files"][:-1]
        try:
            manifest.write_text(json.dumps(stale, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            marker = manifest.read_bytes()
            helped = run(ROOT / "tools/update_manifest.py", "--help")
            self.assertEqual(manifest.read_bytes(), marker, "--help rewrote the manifest")
            self.assertEqual(helped.returncode, 0)
            self.assertIn("usage:", helped.stdout)
            mistaken = run(ROOT / "tools/update_manifest.py", "--check")
            self.assertEqual(manifest.read_bytes(), marker, "an unknown argument rewrote the manifest")
            self.assertEqual(mistaken.returncode, 2)
        finally:
            manifest.write_bytes(before)


if __name__ == "__main__":
    unittest.main()
