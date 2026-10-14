"""Claude Code project-skill entries stay pointers to the selected kit methods."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from test_release import module, ROOT

entries = module("sync_claude_skills")
SELECTED = json.loads((ROOT / "tools/claude_skills.json").read_text(encoding="utf-8"))["expose"]


def copy_sources(base):
    (base / "Blitz/setup").mkdir(parents=True)
    (base / "tools").mkdir()
    shutil.copy2(ROOT / "Blitz/manifest.json", base / "Blitz/manifest.json")
    shutil.copy2(ROOT / "Blitz/setup/frontmatter.py", base / "Blitz/setup/frontmatter.py")
    shutil.copy2(ROOT / "tools/claude_skills.json", base / "tools/claude_skills.json")
    for source in (ROOT / "Blitz/skills").glob("*/SKILL.md"):
        target = base / "Blitz/skills" / source.parent.name / "SKILL.md"
        target.parent.mkdir(parents=True)
        shutil.copy2(source, target)


class ClaudeSkillEntries(unittest.TestCase):
    def test_checked_in_entries_match_the_selection(self):
        report = entries.check(ROOT)
        self.assertEqual(report["findings"], [])
        self.assertEqual((report["result"], report["exposed"]), ("pass", len(SELECTED)))
        self.assertEqual(sorted(path.name for path in (ROOT / ".claude/skills").iterdir()), SELECTED)

    def test_entries_carry_method_frontmatter_and_point_to_the_kit(self):
        for name in SELECTED:
            with self.subTest(name=name):
                method = (ROOT / "Blitz/skills" / name / "SKILL.md").read_text(encoding="utf-8")
                entry = (ROOT / ".claude/skills" / name / "SKILL.md").read_text(encoding="utf-8")
                head = method[:method.index("\n---\n", 4) + 5]
                self.assertTrue(entry.startswith(head))
                self.assertIn("Blitz/skills/" + name + "/SKILL.md", entry)
                self.assertLess(len(entry.encode("utf-8")), 2048)

    def test_drift_fails_and_write_repairs_without_deleting(self):
        with tempfile.TemporaryDirectory(prefix="blitz-claude-skills-") as raw:
            base = Path(raw)
            copy_sources(base)
            self.assertEqual({row["rule"] for row in entries.check(base)["findings"]}, {"missing-entry"})
            self.assertEqual(entries.write(base)["result"], "pass")
            changed = base / ".claude/skills/blitz/SKILL.md"
            changed.write_text(changed.read_text(encoding="utf-8") + "edited\n", encoding="utf-8")
            extra = base / ".claude/skills/cold-read/SKILL.md"
            extra.parent.mkdir()
            extra.write_text("---\nname: cold-read\n---\n", encoding="utf-8")
            report = entries.check(base)
            self.assertEqual(report["result"], "fail")
            self.assertEqual({(row["path"], row["rule"]) for row in report["findings"]},
                             {(".claude/skills/blitz/SKILL.md", "changed-entry"),
                              (".claude/skills/cold-read/SKILL.md", "unexpected-entry")})
            self.assertEqual(entries.write(base)["findings"],
                             [{"path": ".claude/skills/cold-read/SKILL.md", "rule": "unexpected-entry"}])
            self.assertTrue(extra.exists())

    def test_selection_must_name_known_sorted_methods(self):
        for expose in (["unlisted"], ["website-cloner", "blitz"], ["blitz", "blitz"], []):
            with self.subTest(expose=expose), tempfile.TemporaryDirectory(prefix="blitz-claude-skills-") as raw:
                base = Path(raw)
                copy_sources(base)
                (base / "tools/claude_skills.json").write_text(json.dumps({"expose": expose}), encoding="utf-8")
                with self.assertRaises(ValueError):
                    entries.check(base)

    def test_method_folder_without_manifest_row_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="blitz-claude-skills-") as raw:
            base = Path(raw)
            copy_sources(base)
            shutil.rmtree(base / "Blitz/skills/metric-pull")
            with self.assertRaises(ValueError):
                entries.check(base)


if __name__ == "__main__":
    unittest.main()
