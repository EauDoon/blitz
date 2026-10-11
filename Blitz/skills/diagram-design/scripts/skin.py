#!/usr/bin/env python3
"""Convert a light-skin diagram HTML into the dark skin, or check one for stray light tokens.

The skill's snippets and examples are written in the light skin. This script is the
only sanctioned way to produce the dark skin, so the two never drift by hand.

    python3 scripts/skin.py dark  diagram.html [-o diagram-dark.html]
    python3 scripts/skin.py check diagram-dark.html

WHAT IT COVERS
  - Hex colours in 3, 4, 6 and 8 digit notation. `#fff`, `#FFF`, `#ffffff` and
    `#ffffffcc` are all recognised; an alpha pair is preserved and only the base
    triple is remapped.
  - `rgb()` and `rgba()` functional notation, comma or space separated, with the
    alpha argument passed through untouched.
  - Terminal-skin files. These are detected at file level and refused, because the
    terminal register shares `#f5f5f5` with light `paper` and a token exemption list
    cannot tell the two apart. See "Terminal skin" in references/style-guide.md.

WHAT IT DOES NOT COVER
  - Named CSS colours (`fill="white"`). They are reported as a WARNING in both modes
    and are never rewritten: `white` on a dark canvas is sometimes correct (text) and
    sometimes wrong (a panel fill), and the script cannot tell which. Fix the source
    to use a hex token. Named colours do not change the exit code.
  - `hsl()`, `color()`, `lab()`, CSS colour keywords beyond the named list below, and
    colours injected by JavaScript. Diagrams ship without JavaScript, so the last one
    is out of scope by construction.
  - Anything that is not a colour. A colophon still reading "light" is warned about in
    `check` but not rewritten.

`check` exits 1 and prints every light-skin token still present. Run it before
delivering any dark diagram. `dark` exits 1 when a colour had no mapping. A terminal
file exits 0 from both modes, having done nothing, because doing nothing is correct.
"""

import argparse
import re
import sys
from pathlib import Path

# Light hex -> dark hex. Sourced from references/style-guide.md.
# Every hex that appears anywhere in the shipped corpus is covered.
# INVARIANT: two light colours may share a dark target only when they are near
# duplicates of one role (the accent variants below). Two colours at opposite ends of
# the lightness range must never merge. _dangerous_merges() enforces this at runtime.
HEX_MAP = {
    # core roles
    "#f5f5f5": "#0f0f0f",  # paper
    "#ececec": "#1a1a1a",  # paper-2
    "#ffffff": "#171717",  # backend node fill (white -> lifted panel)
    "#2d3142": "#f5f7fa",  # ink
    "#4f5d75": "#9aa0a8",  # muted
    "#7a8399": "#767c85",  # soft
    "#bfc0c0": "#2a2a2a",  # rule-solid
    "#eb6c36": "#c6ff3a",  # accent
    "#2e5aa8": "#5c78ff",  # link
    # accent and link variants that leaked into the corpus
    "#f08a59": "#c6ff3a",
    "#f7591f": "#c6ff3a",
    "#ff6a30": "#c6ff3a",
    "#c73a2b": "#c6ff3a",
    "#6a95d8": "#5c78ff",
    # zone and container fills (high-level, datalake).
    # #3d4460 moved off #1a1a1a: it is the high-level chevron alternate fill and
    # #ececec (paper-2) is the container fill, and both appear in
    # example-high-level-full.html. Sharing #1a1a1a merged two deliberately distinct
    # fills. The trio now steps 0b -> 26 -> 20 and collides with nothing.
    "#1c1f2e": "#0b0b0b",
    "#3d4460": "#262626",
    "#4a5270": "#202020",
    # legacy paper tints (assets/index.html palette)
    "#f8f6f0": "#0f0f0f",
    "#f5f4ed": "#0f0f0f",  # paper
    "#efeee5": "#1a1a1a",  # paper-2, previously unmapped and left light
    # #0b0d0b and #111111 are near-black INK, not paper. Mapping them to #0f0f0f put
    # body text at the same value as the page background, which is what broke
    # assets/index.html. They are ink, so they take the dark ink value.
    "#111111": "#f5f7fa",
    "#0b0d0b": "#f5f7fa",
    "#52534e": "#9aa0a8",  # legacy muted, previously unmapped
    "#65655c": "#767c85",  # legacy soft, previously unmapped
    # series palette -> upstream's own dark equivalents
    "#7c8f6f": "#9caf8f",
    "#5e7a9b": "#82a0c0",
    "#b8915a": "#d3ad7a",
    "#9c6b50": "#b88670",
    "#6e6479": "#8d8298",
    # semantic status colors used by process / it-state / medallion
    "#b85450": "#d97a78",
    "#5a7d9a": "#82a0c0",
    "#7a8c47": "#9caf8f",
    "#8c6d3f": "#d3ad7a",
    "#c9a23a": "#d9c06a",
    "#9aac67": "#9caf8f",
    "#666666": "#9aa0a8",
}

# rgb()/rgba() base triples, opacity preserved.
RGB_MAP = {
    (45, 49, 66): (245, 247, 250),     # ink washes
    (235, 108, 54): (198, 255, 58),    # accent washes
    (79, 93, 117): (154, 160, 168),    # muted washes
    (245, 245, 245): (15, 15, 15),     # paper washes
    (122, 131, 153): (118, 124, 133),  # soft washes
    (240, 138, 89): (198, 255, 58),
    (94, 122, 155): (130, 160, 192),
    (184, 84, 80): (217, 122, 120),
    (156, 107, 80): (184, 134, 112),
    (124, 143, 111): (156, 175, 143),
    (255, 255, 255): (23, 23, 23),
}

# Named CSS custom properties whose dark value is NOT the generic mapping of their light
# value. The inverted hub block is the case that forced this: on light it is an ink slab
# with paper text, and a straight token swap turns it into a near-white slab on a
# near-black canvas, which outshouts the accent. Forced after the generic pass, so they
# win. Add a role here rather than hand-editing a dark file.
VAR_OVERRIDES = {
    "--invert": "#171717",       # inverted block fill, light #2d3142
    "--invert-text": "#f5f7fa",  # text on an inverted block, light #f5f5f5
}
VAR_DECL_RE = re.compile(r"(--[a-z0-9-]+)(\s*:\s*)(#[0-9a-fA-F]{3,8})")

# Terminal colours that are unambiguous: they belong to no other skin, so leaving them
# alone is always right even if they turn up inside a non-terminal file.
# terminal-ink #f5f5f5 is deliberately NOT here. It is byte-identical to light `paper`,
# so exempting the token would break every ordinary light-to-dark conversion. Terminal
# files are protected at file level instead, by is_terminal_file().
TERMINAL_EXEMPT = {
    "#0a0a0a", "#141414", "#1b1b1b", "#2b2b2b", "#ff5a36", "#9a9a9a", "#5c5c5c",
}

# A terminal-skin file carries the terminal custom-property block or the
# template-terminal DOM. Two independent signals so a hand-edited file still trips it.
TERMINAL_MARKERS = (
    re.compile(r"--terminal-[a-z-]+\s*:", re.I),           # terminal- custom properties
    re.compile(r"--color-page\s*:\s*#0a0a0a", re.I),       # terminal page background
    re.compile(r'class\s*=\s*"[^"]*\bterminal\b', re.I),   # template-terminal structure
    re.compile(r'class\s*=\s*"[^"]*\btitlebar\b', re.I),
)

# Longest form first so a 6-digit value is never read as a 3-digit one plus junk.
# The trailing guard stops #aabbccdd being split into #aabbcc + dd.
HEX_RE = re.compile(
    r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})(?![0-9a-fA-F])"
)

# rgb() and rgba(), comma or whitespace separated, optional 4th argument after , or /.
# Separators are captured so the rewrite preserves the source's spacing.
RGB_FUNC_RE = re.compile(
    r"\b(rgba?)\(\s*(\d{1,3})(\s*,\s*|\s+)(\d{1,3})(\s*,\s*|\s+)(\d{1,3})"
    r"(\s*(?:,|/)\s*[^)]*)?\)"
)

# Named CSS colours that carry skin meaning. Reported, never rewritten; see docstring.
NAMED_COLOURS = {
    "white", "black", "whitesmoke", "gainsboro", "silver", "lightgray", "lightgrey",
    "darkgray", "darkgrey", "dimgray", "dimgrey", "gray", "grey", "ivory", "snow",
}
# Only look inside a colour-bearing property or attribute, so the word "black" in a
# node label is not reported.
_COLOUR_SLOT_RE = re.compile(
    r"(?<![-\w])(?:fill|stroke|stop-color|flood-color|lighting-color|color|background"
    r"|background-color|border|border-color|border-top|border-bottom|border-left"
    r"|border-right|outline)\s*[:=]\s*[\"']?([^;\"'<>{}]{0,60})",
    re.I,
)
_NAMED_IN_VALUE_RE = re.compile(
    r"(?<![-\w])(" + "|".join(sorted(NAMED_COLOURS, key=len, reverse=True)) + r")(?![-\w])",
    re.I,
)


def is_terminal_file(text: str) -> bool:
    """True when the file is the terminal register, which has no light/dark pair."""
    return any(p.search(text) for p in TERMINAL_MARKERS)


def split_hex(raw: str) -> tuple[str, str]:
    """('#fff' | '#ffff' | '#ffffff' | '#ffffffcc') -> ('#ffffff', alpha_pair_or_empty).

    3 and 4 digit shorthand expands by digit doubling, per CSS. The alpha pair is
    returned separately so the rewrite can put the source's own alpha back on the
    mapped colour instead of dropping it.
    """
    body = raw[1:]
    if len(body) in (3, 4):
        base = "".join(c * 2 for c in body[:3])
        alpha = body[3] * 2 if len(body) == 4 else ""
    else:
        base = body[:6]
        alpha = body[6:]
    return "#" + base.lower(), alpha


def _rgb_of(hex6: str) -> tuple[int, int, int]:
    return tuple(int(hex6[i:i + 2], 16) for i in (1, 3, 5))


def _dist(a: str, b: str) -> float:
    ra, rb = _rgb_of(a), _rgb_of(b)
    return sum((x - y) ** 2 for x, y in zip(ra, rb)) ** 0.5


def dangerous_merges(threshold: float = 120.0) -> list[str]:
    """Light colours that map to one dark colour but are nowhere near each other.

    Two accent variants collapsing onto one accent is intended. A paper and an ink
    collapsing onto one value is the defect that made assets/index.html unreadable.
    Distance is plain RGB euclidean; 120 separates 'same role, different shade' from
    'opposite ends of the ramp'.
    """
    groups: dict[str, list[str]] = {}
    for light, dark in HEX_MAP.items():
        groups.setdefault(dark, []).append(light)
    bad = []
    for dark, lights in sorted(groups.items()):
        for i, a in enumerate(lights):
            for b in lights[i + 1:]:
                if _dist(a, b) > threshold:
                    bad.append(f"{a} and {b} both map to {dark} (distance {_dist(a, b):.0f})")
    return bad


def named_colours(text: str) -> dict[str, int]:
    """Named CSS colours used in a colour slot, with counts."""
    found: dict[str, int] = {}
    for slot in _COLOUR_SLOT_RE.finditer(text):
        for nm in _NAMED_IN_VALUE_RE.finditer(slot.group(1)):
            key = nm.group(1).lower()
            found[key] = found.get(key, 0) + 1
    return found


def to_dark(text: str) -> tuple[str, list[str]]:
    unmapped = []

    def hex_sub(m):
        raw = m.group(0)
        base, alpha = split_hex(raw)
        if base in TERMINAL_EXEMPT:
            return raw
        if base in HEX_MAP:
            # alpha pair survives the swap; only the base triple is a skin token
            return HEX_MAP[base] + alpha
        unmapped.append(raw)
        return raw

    def rgb_sub(m):
        fn, r, s1, g, s2, b, tail = m.groups()
        triple = (int(r), int(g), int(b))
        if triple in RGB_MAP:
            nr, ng, nb = RGB_MAP[triple]
            return f"{fn}({nr}{s1}{ng}{s2}{nb}{tail or ''})"
        unmapped.append(m.group(0))
        return m.group(0)

    out = HEX_RE.sub(hex_sub, text)
    out = RGB_FUNC_RE.sub(rgb_sub, out)  # covers rgb() as well as rgba()
    def var_force(m):
        name, sep, _val = m.group(1), m.group(2), m.group(3)
        if name in VAR_OVERRIDES:
            return f"{name}{sep}{VAR_OVERRIDES[name]}"
        return m.group(0)

    out = VAR_DECL_RE.sub(var_force, out)
    return out, sorted(set(unmapped))


def check_var_overrides(text: str) -> list[str]:
    """A dark file must carry the forced value for every overridden custom property."""
    wrong = []
    for m in VAR_DECL_RE.finditer(text):
        name, val = m.group(1), m.group(3).lower()
        want = VAR_OVERRIDES.get(name)
        if want and val != want:
            wrong.append(f"{name} is {val}, dark requires {want}")
    return wrong


def check(text: str) -> list[str]:
    """Return light-skin tokens still present in what should be a dark file."""
    strays = []
    for m in HEX_RE.finditer(text):
        base, _ = split_hex(m.group(0))
        if base in TERMINAL_EXEMPT:
            continue
        if base in HEX_MAP:
            strays.append(m.group(0))
    for m in RGB_FUNC_RE.finditer(text):
        triple = (int(m.group(2)), int(m.group(4)), int(m.group(6)))
        if triple in RGB_MAP:
            strays.append(m.group(0))
    return sorted(set(strays))


def report_named(text: str) -> None:
    """WARNING only. See docstring for why these are not rewritten."""
    for name, count in sorted(named_colours(text).items()):
        print(f"WARNING named CSS colour '{name}' x{count}: "
              f"not skinned, replace with a hex token from style-guide.md")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", choices=["dark", "check"])
    ap.add_argument("path")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    # Guard the map against the class of bug that broke index.html, on every run.
    for msg in dangerous_merges():
        print(f"WARNING HEX_MAP merge: {msg}", file=sys.stderr)

    src = Path(a.path)
    if not src.is_file():
        print(f"not a file: {src}", file=sys.stderr)
        return 2
    text = src.read_text(encoding="utf-8")

    # The terminal register is a third skin with no light/dark pair. Refuse both modes
    # rather than trust a token exemption list that drifts.
    if is_terminal_file(text):
        verb = "not converted" if a.mode == "dark" else "not checked"
        print(f"SKIP {src.name}: terminal skin file, {verb}. "
              f"The terminal register is fixed and skin.py leaves it alone "
              f"(references/style-guide.md, 'Terminal skin'). No output written.")
        return 0

    if a.mode == "check":
        # colour is converted; words are not. Catch a colophon still saying "light".
        for m in re.finditer(r"(?i)>[^<]*\blight\b[^<]*<", text):
            print(f"WARNING text still says light: {m.group(0)[1:-1].strip()[:60]}")
        report_named(text)
        for w in check_var_overrides(text):
            print(f"FAIL var override: {w}")
        strays = check(text) + (["var-override"] if check_var_overrides(text) else [])
        strays = [s for s in strays if s != "var-override"] or ([] if not check_var_overrides(text) else ["see var override above"])
        if strays:
            print(f"FAIL {src.name}: {len(strays)} light-skin token(s) present")
            for s in strays:
                print(f"  {s}")
            return 1
        print(f"OK {src.name}: no light-skin tokens")
        return 0

    out, unmapped = to_dark(text)
    dest = Path(a.out) if a.out else src.with_name(src.stem + "-dark" + src.suffix)
    dest.write_text(out, encoding="utf-8")
    print(f"wrote {dest}")
    report_named(out)
    if unmapped:
        print(f"WARNING {len(unmapped)} colour(s) had no mapping and were left as-is:")
        for u in unmapped:
            print(f"  {u}")
        print("Add them to HEX_MAP / RGB_MAP, or fix the source to use a semantic role.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
