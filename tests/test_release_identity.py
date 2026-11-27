"""Standalone package identity and archive-member content checks."""
import hashlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile
from test_release import module, ROOT, scanner

identity = module("check_identity")


class IdentityChecks(unittest.TestCase):
    def test_current_source_has_only_standalone_identity(self):
        report = identity.scan(ROOT)
        self.assertEqual(report["findings"], [])
        # Pixels are reviewed independently; only the exact pinned artwork is allowed.
        for row in report["binary_review_required"]:
            self.assertIn(row["sha256"], scanner.REVIEWED_MEDIA.get(row["path"], ()))

    def test_archive_content_names_and_word_boundaries(self):
        old = "Th" + "or"
        for path, body in [(old + "_Guide.md", "ordinary"), ("guide.md", old.lower() + "_context"),
                           ("guide.md", "Use " + old.upper())]:
            memory = io.BytesIO()
            with zipfile.ZipFile(memory, "w") as archive:
                archive.writestr(path, body)
            report = {"files_checked": 0, "findings": [], "binary_review_required": []}
            identity.inspect("candidate.zip", memory.getvalue(), report)
            self.assertTrue(report["findings"])
        self.assertIsNone(identity.RETIRED.search("author authority authorized authorship"))

    def test_symlinked_directories_are_rejected_before_the_file_filter(self):
        old = "th" + "or"
        with tempfile.TemporaryDirectory(prefix="blitz-identity-") as raw:
            base = Path(raw)
            outside = base / "outside"
            outside.mkdir()
            (outside / "guide.md").write_text("Use " + old, encoding="utf-8")
            artifacts = base / "artifacts"
            artifacts.mkdir()
            (artifacts / "clean.md").write_text("ordinary", encoding="utf-8")
            (artifacts / "linked").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlinks"):
                identity.scan(artifacts, artifacts=True)
            # Git tracks a directory link as one blob; its name must not drop out either.
            source = base / "source"
            (source / "inner").mkdir(parents=True)
            (source / "clean.md").write_text("ordinary", encoding="utf-8")
            (source / (old + "-docs")).symlink_to("inner", target_is_directory=True)
            subprocess.run(["git", "init", "-q", str(source)], check=True)
            subprocess.run(["git", "-C", str(source), "add", "-A"], check=True)
            with self.assertRaisesRegex(ValueError, "symlinks"):
                identity.scan(source)


if __name__ == "__main__":
    unittest.main()
