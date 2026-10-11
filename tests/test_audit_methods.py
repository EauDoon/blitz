"""Executable method and staged-reference regressions; no live host claims."""
import importlib.util
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "Blitz"
sys.path.insert(0, str(KIT / "setup"))
import chatgpt_stage


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


js = load(KIT / "skills/frontend-taste/scripts/check-html-js.py", "html_js")
diagram = load(KIT / "skills/diagram-design/scripts/lint-diagram.py", "diagram_lint")


class MethodRepairs(unittest.TestCase):
    def test_saved_svg_render_matches_styled_nested_source(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node is required for rendered SVG verification")
        result = subprocess.run([node, "--test", str(ROOT / "tests/node/test_svg_export.mjs")], capture_output=True, text=True, encoding="utf-8", timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_inline_scripts_classic_module_data_and_external(self):
        cases = [
            ('<script>const a=1;</script>', "pass", 1),
            ('<SCRIPT nonce="synthetic"\nTYPE="module">export const a=1; await Promise.resolve();</SCRIPT>', "pass", 1),
            ('<script type="module">const a=1;</script><script type="module">const a=2;</script>', "pass", 2),
            ('<!-- <script>const = ;</script> --><script type="application/ld+json">{"x":1}</script><script type="importmap">{"imports":{}}</script>', "pass", 0),
            ('<script src="https://example.invalid/fixture.js"></script>', "partial", 0),
            ('<script>const = ;</script>', "fail", 1),
            ('<script/>const broken = ;</script>', "fail", 1),
            ('<script/>const markup="<p>";</script>', "pass", 1),
            ('<script type="module">export const = ;</script>', "fail", 1),
            ('<script>return 1;</script>', "fail", 1),
            ('<script>const okay=1;</script><script type="module">export const = ;</script>', "fail", 2),
            ('<p>No scripts</p>', "pass", 0),
        ]
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "page.html"
            for source, status, checked in cases:
                with self.subTest(source=source):
                    path.write_text(source, encoding="utf-8")
                    result = js.check(path)
                    self.assertEqual((result["result"], result["checked"]), (status, checked))
            path.write_text("<script>const x=1", encoding="utf-8")
            with self.assertRaises(ValueError):
                js.check(path)

    def test_reference_geometry_and_negative_controls(self):
        reference = (KIT / "skills/diagram-design/references/type-data-flow.md").read_text(encoding="utf-8")
        constants = {name: int(re.search(r"^" + name + r"\s*=\s*(\d+)", reference, re.M)[1])
                     for name in ["label_col_w", "step_slot_w", "node_w", "node_h", "header_h", "lane_h", "step_chip_y"]}
        for steps, lanes in [(1, 1), (5, 4), (6, 4)]:
            elements = []
            for j in range(steps):
                center = constants["label_col_w"] + (j + .5) * constants["step_slot_w"]
                x = center - constants["node_w"] / 2
                elements.append(f'<rect x="{center-16}" y="{constants["step_chip_y"]}" width="32" height="16" rx="8"/>')
                for k in range(lanes):
                    y = constants["header_h"] + k * constants["lane_h"] + 8
                    elements.append(f'<rect x="{x}" y="{y}" width="{constants["node_w"]}" height="{constants["node_h"]}" rx="6"/>')
                    for dx, dy in [(4, 4), (4, 52), (84, 52)]:
                        elements.append(f'<rect x="{x+dx}" y="{y+dy}" width="16" height="8" rx="4"/>')
                        self.assertLessEqual(dx+16, constants["node_w"])
                        self.assertLessEqual(dy+8, constants["node_h"])
            result = []
            diagram.check_grid("".join(elements), result)
            self.assertEqual(result, [])
        medallion = (KIT / "skills/diagram-design/references/type-medallion.md").read_text(encoding="utf-8")
        for path in re.findall(r"`(M \d+,80 C [^`]+)`", medallion):
            result = []
            diagram.check_grid(f'<path d="{path}" fill="none"/>', result)
            self.assertEqual(result, [], path)
        for bad in ['<rect x="2" width="16"/>', '<rect width="18"/>', '<circle r="6"/>', '<text font-size="6.5"/>']:
            result = []
            diagram.check_grid(bad, result)
            self.assertTrue(any(row[0] == "FAIL" for row in result), bad)

    def test_medallion_checklist_anchors_follow_grid(self):
        text = (KIT / "skills/diagram-design/references/type-medallion.md").read_text(encoding="utf-8")
        constants = {name: int(re.search(r"^" + name + r"\s*=\s*(\d+)", text, re.M)[1])
                     for name in ["tier_w", "tier_gap", "left_pad"]}
        checklist = text.split("## 7. Reproducibility checklist", 1)[1].split("## 8.", 1)[0]
        anchors = re.search(r"anchors at `\((\w+)\(i\), 80\)` → `\((\w+)\(i\+1\), 80\)`", checklist)
        self.assertIsNotNone(anchors)
        center = lambda i: constants["left_pad"] + i * (constants["tier_w"] + constants["tier_gap"]) + constants["tier_w"] / 2
        functions = {"tier_cx": center, "arc_anchor_x": lambda i: 4 * (center(i) // 4)}
        for tiers in [3, 5, 6]:
            for i in range(tiers - 1):
                start, end = functions[anchors[1]](i), functions[anchors[2]](i + 1)
                result = []
                diagram.check_grid(f'<path d="M {start},80 C {start},0 {end},0 {end},80"/>', result)
                self.assertEqual(result, [], "The mandatory checklist must produce valid connector geometry")
        chip = re.search(r"Tag chip: rect at `\(path_x \+ (\d+), path_y \+ (\d+)\)`", text)
        self.assertIsNotNone(chip)
        result = []
        diagram.check_grid(f'<rect x="{16+int(chip[1])}" y="{476+int(chip[2])}" width="64" height="12" rx="2"/>', result)
        self.assertEqual(result, [], "The documented path chip must follow the grid")
        matrix = (KIT / "skills/diagram-design/references/type-dp-security-matrix.md").read_text(encoding="utf-8")
        sizes = re.findall(r"role(?: at |, )(\d+)px", text + "\n" + matrix)
        self.assertGreater(len(sizes), 8)
        for size in sizes:
            result = []
            diagram.check_grid(f'<text font-size="{size}">Synthetic role label</text>', result)
            self.assertEqual(result, [], "Documented role font size " + size)

    def test_all_shipped_diagrams_keep_their_geometry_gate(self):
        paths = sorted((KIT / "skills/diagram-design/assets").glob("*.html"))
        self.assertEqual(len(paths), 105)
        for path in paths:
            result = subprocess.run([sys.executable, "-B", str(KIT / "skills/diagram-design/scripts/lint-diagram.py"), str(path), "--no-composition"], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, path.name + "\n" + result.stdout + result.stderr)

    def test_staged_candidates_and_transitive_master_links_are_closed(self):
        before = chatgpt_stage.source_inventory(KIT)
        files, report = chatgpt_stage.prepare(None, True)
        self.assertEqual(before, chatgpt_stage.source_inventory(KIT))
        self.assertEqual(len(report["skills"]), 25)
        self.assertEqual(sum(r["historical_name_map_status"] != "host_tool" for r in report["skills"]), 24)
        for rel, data in before.items():
            self.assertEqual(files[chatgpt_stage.SOURCE_ROOT + "/" + rel], data)
        count = 0
        for path, data in files.items():
            if not path.endswith(".md"):
                continue
            for match in chatgpt_stage.MARKDOWN_LINK.finditer(data.decode("utf-8")):
                raw = match[2].split(' "')[0].strip("<>")
                url = urlsplit(raw)
                if url.scheme or url.netloc or not url.path:
                    continue
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), unquote(url.path)))
                self.assertFalse(resolved.startswith("../"), (path, raw))
                self.assertTrue(resolved in files or any(p.startswith(resolved.rstrip("/") + "/") for p in files), (path, raw))
                count += 1
        self.assertGreater(count, 51)
        # URL-encoded spaces, fragments and source escapes are separate cases.
        source = KIT / "setup/host-adapters/openai.md"
        text = "[budget](../../templates/context/04%20Economics%20And%20Budget.md#scope)"
        transformed = chatgpt_stage.rewrite_context_links(text, source, "blitz/references/blitz-host-adapter.md")
        self.assertIn("04%20Economics%20And%20Budget.md#scope", transformed)
        with self.assertRaises(ValueError):
            chatgpt_stage.rewrite_context_links("[escape](../../../../outside.md)", source, "blitz/references/adapter.md")


if __name__ == "__main__":
    unittest.main()
