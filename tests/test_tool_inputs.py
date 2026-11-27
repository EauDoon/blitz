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


if __name__ == "__main__":
    unittest.main()
