"""Standalone package identity and archive-member content checks."""
import hashlib
import io
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


if __name__ == "__main__":
    unittest.main()
