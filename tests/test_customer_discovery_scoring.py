"""Preserve the frozen corpus and reject unverified evaluator inputs."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DiscoveryScoringChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="blitz-evaluator-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = self.root / "tests/evals/customer-discovery"
        self.helper = self.base.with_name("customer-discovery-scoring-v3")
        shutil.copytree(ROOT / "tests/evals/customer-discovery", self.base)
        shutil.copytree(ROOT / "tests/evals/customer-discovery-scoring-v3", self.helper)
        spec = importlib.util.spec_from_file_location("discovery_scoring", self.helper / "prepare.py")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.out = self.root / "prepared"

    def inventory(self):
        return {str(p.relative_to(self.base)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.base.rglob("*") if p.is_file()}

    def test_valid_preparation_preserves_frozen_inputs_and_lineage(self):
        before = self.inventory()
        self.module.prepare(self.out)
        self.assertEqual(self.inventory(), before)
        self.assertEqual((self.base / "cases.jsonl").read_bytes(), (self.out / "cases.jsonl").read_bytes())
        self.assertEqual((self.base / "FREEZE.json").read_bytes(), (self.out / "PARENT_FREEZE_V1.json").read_bytes())
        self.assertFalse((self.out / "FREEZE.json").exists())
        receipt = json.loads((self.out / "EVALUATOR_REVISION.json").read_text())
        for name, digest in receipt["files"].items():
            self.assertEqual(hashlib.sha256((self.out / name).read_bytes()).hexdigest(), digest)

    def test_unlisted_file_is_rejected_before_output_creation(self):
        (self.base / "unexpected.txt").write_text("unverified fixture material")
        with self.assertRaisesRegex(ValueError, "unlisted"):
            self.module.prepare(self.out)
        self.assertFalse(self.out.exists())

    def test_unlisted_symlink_is_not_followed(self):
        outside = self.root / "outside.txt"
        outside.write_text("outside fixture material")
        (self.base / "unexpected.txt").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.module.prepare(self.out)
        self.assertFalse(self.out.exists())

    def test_listed_symlink_is_rejected_even_with_identical_bytes(self):
        source = self.base / "cases.jsonl"
        outside = self.root / "outside.jsonl"
        outside.write_bytes(source.read_bytes())
        source.unlink()
        source.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "unsafe"):
            self.module.prepare(self.out)
        self.assertFalse(self.out.exists())

    def test_freeze_metadata_tampering_is_rejected(self):
        (self.base / "FREEZE.json").write_text("{}\n")
        with self.assertRaisesRegex(ValueError, "metadata differs"):
            self.module.prepare(self.out)
        self.assertFalse(self.out.exists())

    def test_occupied_destination_remains_intact(self):
        self.out.mkdir()
        marker = self.out / "keep.txt"
        marker.write_text("keep existing output")
        with self.assertRaisesRegex(ValueError, "output must be new"):
            self.module.prepare(self.out)
        self.assertEqual(marker.read_text(), "keep existing output")
        self.assertEqual(list(self.out.iterdir()), [marker])

    def test_source_descendant_destination_is_rejected(self):
        out = self.base / "forbidden"
        with self.assertRaisesRegex(ValueError, "outside"):
            self.module.prepare(out)
        self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
