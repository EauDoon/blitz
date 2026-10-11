"""Release safety, history scanning and actual two-build reproducibility checks."""
import importlib.util
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / (name + ".py"))
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


release = module("release")
scanner = module("check_publication")


class ReleaseChecks(unittest.TestCase):
    def test_two_builds_are_byte_identical(self):
        with tempfile.TemporaryDirectory(prefix="blitz-repro-") as raw:
            base = Path(raw)
            first = release.build(base / "first")
            second = release.build(base / "second")
            compared = release.compare(base / "first", base / "second")
            identity = module("check_identity")
            self.assertEqual(identity.scan(base / "first", artifacts=True)["result"], "pass")
            self.assertEqual(first["artifacts"], second["artifacts"])
            self.assertGreater(compared["identical_artifacts"], 2)
            self.assertTrue(first["verification"]["source_unchanged"])
            for artifact in (base / "first").rglob("*"):
                if artifact.is_file():
                    self.assertEqual(scanner.scan_bytes(artifact.name, artifact.read_bytes()), set(), artifact.name)
            name = f"Blitz_v{first['version']}.zip"
            with zipfile.ZipFile(base / "first" / name) as archive:
                for info in archive.infolist():
                    self.assertEqual(info.date_time, release.FIXED_TIME)
                    self.assertEqual(info.external_attr >> 16, 0o100644)
                    self.assertTrue(info.filename.startswith("Blitz/"))
                self.assertEqual(archive.namelist(), sorted(archive.namelist()))
            print(json.dumps({"reproducibility": "pass", "artifacts": compared["identical_artifacts"]}))

    def test_occupied_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as raw:
            out = Path(raw) / "occupied"
            out.mkdir()
            (out / "sentinel").write_bytes(b"keep")
            with self.assertRaises(ValueError):
                release.build(out)
            self.assertEqual((out / "sentinel").read_bytes(), b"keep")

    def test_kit_overlap_and_live_output_rejected(self):
        with self.assertRaises(ValueError):
            release.build(release.KIT / "new-release")
        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaises(ValueError):
                release.build(Path(raw) / ".codex" / "release")

    def test_empty_comparison_is_not_reproducibility(self):
        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaises((OSError, ValueError)):
                release.compare(Path(raw), Path(raw))


class PublicationChecks(unittest.TestCase):

    def synthetic_repository(self, root):
        env = {**os.environ, "GIT_AUTHOR_NAME": "Synthetic Test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
               "GIT_COMMITTER_NAME": "Synthetic Test", "GIT_COMMITTER_EMAIL": "test@example.invalid"}
        def git(*args, data=None):
            result = subprocess.run(["git", "-C", str(root), *args], input=data, check=True, env=env, capture_output=True)
            return result.stdout.decode().strip()
        git("init", "--quiet")
        (root / "safe.txt").write_text("Synthetic clean baseline\n", encoding="utf-8")
        (root / "nested").mkdir()
        (root / "nested/also-safe.txt").write_text("Synthetic clean baseline\n", encoding="utf-8")
        git("add", ".")
        git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Synthetic baseline")
        self.assertEqual(scanner.scan(root)["result"], "pass")
        return git

    def assert_token_report(self, report, token, origin):
        self.assertEqual(report["result"], "fail")
        self.assertTrue(any(row["rule"] == "github-token" and row["origin"] == origin for row in report["findings"]))
        self.assertNotIn(token, json.dumps(report))

    def test_nested_repo_argument_scans_root_worktree(self):
        with tempfile.TemporaryDirectory(prefix="blitz-nested-") as raw:
            root = Path(raw)
            self.synthetic_repository(root)
            token = "gh" + "p_" + "x" * 36
            (root / "safe.txt").write_text(token, encoding="utf-8")
            report = scanner.scan(root / "nested")
            self.assertEqual(report["tracked_files"], 2)
            self.assert_token_report(report, token, "worktree")
            self.assertTrue(any(row["path"] == "safe.txt" for row in report["findings"]))

    def test_nested_repo_argument_scans_root_index_with_clean_worktree(self):
        with tempfile.TemporaryDirectory(prefix="blitz-index-") as raw:
            root = Path(raw)
            git = self.synthetic_repository(root)
            token = "gh" + "p_" + "x" * 36
            (root / "safe.txt").write_text(token, encoding="utf-8")
            git("add", "safe.txt")
            (root / "safe.txt").write_text("Synthetic clean baseline\n", encoding="utf-8")
            report = scanner.scan(root / "nested")
            self.assert_token_report(report, token, "index")
            self.assertFalse(any(row["origin"] == "worktree" for row in report["findings"]))

    def test_annotated_tag_text_is_scanned_without_disclosing_token(self):
        with tempfile.TemporaryDirectory(prefix="blitz-tag-") as raw:
            root = Path(raw)
            git = self.synthetic_repository(root)
            token = "gh" + "p_" + "x" * 36
            git("-c", "tag.gpgsign=false", "tag", "-a", "synthetic-tag", "-m", token)
            self.assert_token_report(scanner.scan(root), token, "history-tag")

    def test_direct_blob_ref_is_scanned_without_commit_tree(self):
        with tempfile.TemporaryDirectory(prefix="blitz-blob-ref-") as raw:
            root = Path(raw)
            git = self.synthetic_repository(root)
            token = "gh" + "p_" + "x" * 36
            identity = git("hash-object", "-w", "--stdin", data=token.encode())
            git("update-ref", "refs/tags/synthetic-blob", identity)
            self.assert_token_report(scanner.scan(root), token, "history")

    def test_direct_tree_ref_checks_new_path_for_existing_clean_blob(self):
        with tempfile.TemporaryDirectory(prefix="blitz-tree-ref-") as raw:
            root = Path(raw)
            git = self.synthetic_repository(root)
            blob = git("rev-parse", "HEAD:safe.txt")
            child = git("mktree", data=("100644 blob " + blob + "\tnotes.md\n").encode())
            tree = git("mktree", data=("040000 tree " + child + "\tprivate\n").encode())
            git("update-ref", "refs/tags/synthetic-tree", tree)
            report = scanner.scan(root)
            self.assertEqual(report["result"], "fail")
            self.assertTrue(any(row["path"] == "private/notes.md" and row["origin"] == "history"
                                and row["rule"] == "private-or-generated-path" for row in report["findings"]))

    def test_oversized_tag_fails_closed_before_content_read(self):
        with tempfile.TemporaryDirectory(prefix="blitz-tag-size-") as raw:
            root = Path(raw)
            git = self.synthetic_repository(root)
            git("-c", "tag.gpgsign=false", "tag", "-a", "synthetic-large-tag", "-m", "x" * 5000)
            with patch.object(scanner, "MAX_BLOB", 4096):
                report = scanner.scan(root)
            self.assertEqual(report["result"], "fail")
            self.assertTrue(any(row["origin"] == "history-tag" and row["rule"] == "oversized-blob-not-scanned"
                                for row in report["findings"]))

    def test_secret_patterns_and_no_match_value_in_report(self):
        secret = "gh" + "p_" + "a" * 36
        result = scanner.scan_bytes("example.txt", secret.encode())
        self.assertIn("github-token", result)
        self.assertNotIn(secret, str(result))

    def test_private_paths_and_nested_zip_are_scanned(self):
        self.assertIn("private-or-generated-path", scanner.scan_bytes(".baseline/release.txt", b"ordinary"))
        memory = io.BytesIO()
        with zipfile.ZipFile(memory, "w") as archive:
            archive.writestr("private/notes.txt", "gh" + "p_" + "a" * 36)
        findings = scanner.scan_bytes("example.zip", memory.getvalue())
        self.assertTrue(any("github-token" in rule for rule in findings))
        self.assertTrue(any("private-or-generated-path" in rule for rule in findings))

    def test_reviewed_private_paths_are_hash_bound(self):
        path = next(iter(scanner.REVIEWED_PRIVATE_PATHS))
        self.assertIn("private-or-generated-path", scanner.scan_bytes(path, b"changed private content"))

    def test_reviewed_media_is_bound_to_path_bytes_and_scope(self):
        path = "docs/assets/blitz-motion.gif"
        data = (ROOT / path).read_bytes()
        self.assertEqual(scanner.scan_bytes(path, data), set())
        for name, value, depth in [(path, data + b"\x00", 0),
                                   ("docs/assets/unreviewed.gif", data, 0),
                                   (path, data, 1)]:
            self.assertIn("binary-requires-human-review", scanner.scan_bytes(name, value, depth))
        with patch.object(scanner, "MAX_BLOB", len(data) - 1):
            self.assertIn("oversized-blob-not-scanned", scanner.scan_bytes(path, data))
        private = ".baseline/image.gif"
        with patch.dict(scanner.REVIEWED_MEDIA, {private: scanner.REVIEWED_MEDIA[path]}):
            self.assertIn("private-or-generated-path", scanner.scan_bytes(private, data))

    def test_reviewed_media_versions_preserve_bounded_history_scanning(self):
        path = "docs/assets/blitz-motion.gif"
        versions = (b"GIF89a\x00\xffsynthetic-first", b"GIF89a\x00\xffsynthetic-second")
        pins = frozenset(hashlib.sha256(value).hexdigest() for value in versions)
        with tempfile.TemporaryDirectory(prefix="blitz-media-versions-") as raw:
            root = Path(raw)
            git = self.synthetic_repository(root)
            asset = root / path
            asset.parent.mkdir(parents=True)
            with patch.dict(scanner.REVIEWED_MEDIA, {path: pins}):
                for index, value in enumerate(versions):
                    asset.write_bytes(value)
                    git("add", path)
                    git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", f"Synthetic version {index}")
                report = scanner.scan(root)
                self.assertEqual(report["result"], "pass")
                self.assertEqual(report["reachable_commits"], 3)
                for value in versions:
                    self.assertIn("binary-requires-human-review", scanner.scan_bytes(path, value + b"changed"))
                    self.assertIn("binary-requires-human-review", scanner.scan_bytes("other.gif", value))
                    self.assertIn("binary-requires-human-review", scanner.scan_bytes(path, value, depth=1))

    def test_changed_reviewed_media_is_found_in_index_and_history(self):
        path = "docs/assets/blitz-motion.gif"
        data = (ROOT / path).read_bytes()
        with tempfile.TemporaryDirectory(prefix="blitz-media-history-") as raw:
            root = Path(raw)
            git = self.synthetic_repository(root)
            target = root / path
            target.parent.mkdir(parents=True)
            target.write_bytes(data)
            git("add", path)
            git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Reviewed synthetic media case")
            self.assertEqual(scanner.scan(root)["result"], "pass")
            target.write_bytes(data + b"\x00")
            git("add", path)
            target.write_bytes(data)
            report = scanner.scan(root)
            self.assertTrue(any(row["path"] == path and row["origin"] == "index"
                                and row["rule"] == "binary-requires-human-review" for row in report["findings"]))
            git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Synthetic altered media")
            git("add", path)
            git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Restore reviewed bytes")
            report = scanner.scan(root)
            self.assertEqual(report["result"], "fail")
            self.assertTrue(any(row["path"] == path and row["origin"] == "history"
                                and row["rule"] == "binary-requires-human-review" for row in report["findings"]))
            self.assertFalse(any(row["origin"] == "worktree" for row in report["findings"]))

    def test_deleted_secret_still_found_in_history(self):
        with tempfile.TemporaryDirectory(prefix="blitz-history-") as raw:
            root = Path(raw)
            env = {**os.environ, "GIT_AUTHOR_NAME": "Synthetic Test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
                   "GIT_COMMITTER_NAME": "Synthetic Test", "GIT_COMMITTER_EMAIL": "test@example.invalid"}
            def git(*args):
                subprocess.run(["git", "-C", str(root), *args], check=True, env=env, capture_output=True)
            git("init", "--quiet")
            (root / "fixture.txt").write_text("gh" + "p_" + "a" * 36, encoding="utf-8")
            git("add", "fixture.txt")
            git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Synthetic fixture")
            (root / "fixture.txt").write_text("clean current bytes", encoding="utf-8")
            git("add", "fixture.txt")
            git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Remove synthetic token")
            report = scanner.scan(root)
            self.assertEqual(report["result"], "fail")
            self.assertTrue(any(row["origin"] == "history" and row["rule"] == "github-token" for row in report["findings"]))
            self.assertFalse(any(row["origin"] == "worktree" for row in report["findings"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
