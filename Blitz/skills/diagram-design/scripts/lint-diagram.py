#!/usr/bin/env python3
"""Mechanical checks on a generated diagram HTML. Catches the rules a model breaks silently.

    python3 scripts/lint-diagram.py diagram.html [--accent HEX] [--no-composition]

Exits 1 on any FAIL. WARN lines do not fail the run but should be looked at.
`--no-composition` runs the geometry gate alone, for sweeping a corpus against C1,
C2, C4 and the grid without the composition opinions below.

WHAT IT COVERS, from SKILL.md
  C1    no diagonal <line> and no diagonal L segment in a path. Quarter-arc and
        quadratic elbows (A, Q, C) are legal and are followed correctly, so the
        segment after a rounded bend is measured from the right point.
  C2    an arrow-label mask must not sit on, or within 6px of, the stroke it labels.
        Horizontal strokes are checked vertically and vertical strokes horizontally.
  C4    connector endpoints landing on one edge of a node box must be 12px apart.
  grid  x, y, width, height, cx, cy, line endpoints and path M/L/H/V coordinates
        divide by 4. Font sizes 7 and 9, corner radii, and x/y on <text> and <tspan>
        are exempt per references/style-guide.md.
  budget  accent element count.
  output  self-contained, no script, no external stylesheet, no box-shadow anywhere,
        no vertical text.

WHAT COMPOSITION COVERS, from the four §8 questions
  Every rule above is local geometry: a figure can satisfy all of them and still be
  visually inert. These five make as much of §8 mechanical as can be done honestly.
  Findings are their own `composition:` category.

  1 dead canvas   FAIL. The bounding box of every drawn element, minus the full-bleed
        background and minus the bottom legend strip, against the viewBox. An edge
        band over 20% of that dimension and at least 40px, with nothing in it, is a
        viewBox that wants cropping. §8 question one.
  2 container fill  FAIL, else WARN. For every zone rect holding two or more boxes,
        the fraction of its area covered by them, always reported. §6 allows one
        padding step past the contents, so 64px of slack on an axis is the budget. It
        FAILS under 0.35 full with more than 96px of slack, and WARNs under 0.50 full
        with more than 64px. The slack condition is not decoration: measured across the
        whole example corpus a healthy zone in this design system sits at 0.35 to 0.50
        by area, so the ratio alone fails good work. §8 question three.
  3 uniform nodes  WARN. Four or more node boxes with one identical width and height,
        quoting the §4 anti-pattern "Identical boxes for every node". Never a FAIL: a
        grid of peers is occasionally correct. §8 question two.
  4 spacing vocabulary  WARN. Distinct gaps, rounded to the 4px grid, between boxes
        that share a row or a column. More than three on one axis is the ad-hoc 72
        then 32 then 44 pattern, against §1 "a small spacing vocabulary".
  5 accent weight  WARN. The accent on connector strokes but on no node fill and no
        node stroke: the accent is on the arrow rather than on the thing it points at.
        Half of §8 question four.

Geometry is read from the OUTERMOST <svg>, found by a balanced-depth scan so inline
icon <svg> elements do not truncate the file. Content inside <defs>, <symbol> and any
nested <svg> is spec-fixed or borrowed artwork, so it is excluded from C1, C2, C4 and
the grid check.

WHAT IT DOES NOT COVER
  C3    shared connector paths, and C5 routing behind a third box. Both need full
        geometry and layer order; they stay a human check.
  Curve and arc CONTROL points are exempt from the grid. Only the on-path endpoints
  are checked. Control points of a quarter-arc elbow are a function of the radius and
  land off-grid by construction, so checking them produced nothing but noise.
  <polygon> and <polyline> point lists are not grid-checked.
  Colour tokens. That is scripts/skin.py.
  Anything inside a `style` attribute or a CSS rule, except box-shadow.
  Coordinates under a `transform`, for C1, C2, C4 and the grid. The composition
  checks do follow a plain `translate()`, and give up on rotate, scale and matrix.

WHAT REMAINS A HUMAN JUDGEMENT, after composition
  Whether the eye actually lands on the accent first, and whether the accented node is
  the one that matters. Check 5 only proves the accent is not exclusively on arrows;
  it cannot tell a well-chosen focal node from a badly chosen one. The other half of
  §8 question four stays with the human.
  Whether an identical-size grid is the right call for this content, which is why
  check 3 warns and never fails.
  Whether the dead band a crop would remove was load-bearing whitespace. The check
  measures emptiness, not intent.
  Whether the figure is worth drawing at all, whether a node can be deleted, and
  everything in §2 and the remove test in §8. Composition measures the layout of what
  was drawn, never the decision to draw it.
  Text extents are estimated from character count at 0.6em, so a band within a few
  pixels of the 20% line is a coin flip, not a verdict.

This script is a floor, not a taste gate.
"""

import argparse
import re
import sys
from pathlib import Path

ACCENT_LIGHT = "#eb6c36"
ACCENT_DARK = "#c6ff3a"
ACCENT_TERMINAL = "#ff5a36"

NUM = r"-?\d+(?:\.\d+)?"
# path data allows .5, +3, 1e3
PATH_NUM = r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?"

LINE_RE = re.compile(
    r'<line\b[^>]*?x1="(' + NUM + r')"[^>]*?y1="(' + NUM + r')"'
    r'[^>]*?x2="(' + NUM + r')"[^>]*?y2="(' + NUM + r')"',
    re.S,
)
PATH_TAG_RE = re.compile(r"<path\b[^>]*>", re.S)
RECT_RE = re.compile(r"<rect\b[^>]*>", re.S)
TAG_RE = re.compile(r"<([a-zA-Z][\w:.-]*)\b([^>]*)>", re.S)
ATTR_KV_RE = re.compile(r'([\w:.-]+)\s*=\s*"([^"]*)"')
DEFS_RE = re.compile(r"<defs\b.*?</defs>", re.S)
SYMBOL_RE = re.compile(r"<symbol\b.*?</symbol>", re.S)

# 7 and 9 are the eyebrow and sublabel roles, 14 is the Instrument Serif callout.
# All three are mandated by the typography table in references/style-guide.md.
GRID_EXEMPT_FONT = {7.0, 9.0, 14.0}
GRID_ATTRS = {
    "x", "y", "width", "height", "rx", "ry", "x1", "y1", "x2", "y2", "cx", "cy",
    "r", "font-size",
}
RADIUS_TOKENS = {0.0, 2.0, 4.0, 6.0, 8.0}
# C4: SKILL.md says 12px apart, 8px minimum on a small box. The linter enforces the
# 12px figure; a legal 8px fan on a small box will show up here and is a judgement call.
C4_MIN_GAP = 12.0
C4_SMALL_GAP = 8.0
SMALL_EDGE = 96.0

# rx ry rot large-arc sweep x y. The two flags are single characters and may be written
# with no separator ("0 018 8"), so they get their own pattern rather than a number scan.
ARC_ARG_RE = re.compile(
    r"([-+]?[\d.]+(?:[eE][-+]?\d+)?)[,\s]*"
    r"([-+]?[\d.]+(?:[eE][-+]?\d+)?)[,\s]*"
    r"([-+]?[\d.]+(?:[eE][-+]?\d+)?)[,\s]*"
    r"([01])[,\s]*"
    r"([01])[,\s]*"
    r"([-+]?[\d.]+(?:[eE][-+]?\d+)?)[,\s]*"
    r"([-+]?[\d.]+(?:[eE][-+]?\d+)?)"
)
CMD_SPLIT_RE = re.compile(r"([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)")
ARGC = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "Z": 0}


def fails(msg, out):
    out.append(("FAIL", msg))


def warns(msg, out):
    out.append(("WARN", msg))


# --------------------------------------------------------------------------- markup

def outer_svg(html: str) -> str:
    """The outermost <svg> element, by balanced depth.

    The old `<svg\\b.*?</svg>` was non-greedy, so on any file carrying an inline icon
    <svg> the linter stopped at the icon's closing tag and never saw the rest of the
    diagram. On example-high-level.html that hid most of the figure.
    """
    i = html.find("<svg")
    if i < 0:
        return ""
    depth = 0
    for m in re.finditer(r"<svg\b[^>]*?(/?)>|</svg\s*>", html[i:], re.S):
        tok = m.group(0)
        if tok.startswith("</"):
            depth -= 1
            if depth <= 0:
                return html[i:i + m.end()]
        elif m.group(1) == "/":
            if depth == 0:          # a self-closing outermost <svg/>, nothing inside
                return html[i:i + m.end()]
        else:
            depth += 1
    return html[i:]                 # unbalanced markup: take the rest, other checks will moan


def geometry_body(svg: str) -> str:
    """The outer svg with defs, symbols and nested icon <svg> elements removed.

    Marker and pattern geometry inside <defs> is spec-fixed, and an inline icon or a
    <symbol> glyph is borrowed artwork on its own coordinate system. Reading either as
    diagram geometry produced false C1 diagonals and false off-grid values on many
    files. check_grid stripped defs already; C1, C2 and C4 did not.
    """
    open_m = re.match(r"<svg\b[^>]*>", svg, re.S)
    body = svg[open_m.end():] if open_m else svg
    body = re.sub(r"</svg\s*>\s*$", "", body)
    while True:
        j = body.find("<svg")
        if j < 0:
            break
        sub = outer_svg(body[j:])
        if not sub:
            break
        body = body[:j] + body[j + len(sub):]
    body = DEFS_RE.sub("", body)
    body = SYMBOL_RE.sub("", body)
    return body


def attrs_of(tag: str) -> dict:
    return {k.lower(): v for k, v in ATTR_KV_RE.findall(tag)}


def num_or_none(v: str):
    return float(v) if re.fullmatch(NUM, v.strip()) else None


VIEWBOX_RE = re.compile(
    r'viewBox\s*=\s*"\s*(' + NUM + r')\s+(' + NUM + r')\s+(' + NUM + r')\s+(' + NUM + r')')


def viewbox_of(svg: str):
    """(min-x, min-y, width, height), or None."""
    m = VIEWBOX_RE.search(svg)
    if not m:
        return None
    vb = tuple(float(v) for v in m.groups())
    return vb if vb[2] > 0 and vb[3] > 0 else None


def viewbox_area(svg: str) -> float:
    """Kept for callers that only want the area; main works off viewbox_of()."""
    vb = viewbox_of(svg)
    return vb[2] * vb[3] if vb else 0.0


# ------------------------------------------------------------------------ path data

def path_segments(d: str):
    """(kind, x0, y0, x1, y1) per drawn segment. kind: line, curve, arc, close.

    Tracks the cursor through EVERY command. check_c1 previously advanced it only on
    M, L, H and V, so the first L after a Q, A or C elbow was compared against a stale
    point and read as a diagonal. That is the exact elbow idiom SKILL.md C1 mandates.
    Relative commands and implicit argument repeats are handled.
    """
    segs = []
    cur = None
    start = None
    for cmd, args in CMD_SPLIT_RE.findall(d):
        up = cmd.upper()
        rel = cmd.islower()
        if up == "Z":
            if cur is not None and start is not None:
                segs.append(("close", cur[0], cur[1], start[0], start[1]))
                cur = start
            continue
        if up == "A":
            for g in ARC_ARG_RE.findall(args):
                x, y = float(g[5]), float(g[6])
                if rel and cur is not None:
                    x, y = cur[0] + x, cur[1] + y
                p0 = cur if cur is not None else (x, y)
                segs.append(("arc", p0[0], p0[1], x, y))
                cur = (x, y)
                if start is None:
                    start = cur
            continue
        nums = [float(n) for n in re.findall(PATH_NUM, args)]
        n = ARGC.get(up, 0)
        if n == 0 or len(nums) < n:
            continue
        i = 0
        first_pair = True
        while i + n <= len(nums):
            chunk = nums[i:i + n]
            i += n
            if up == "M":
                x, y = chunk
                if rel and cur is not None:
                    x, y = cur[0] + x, cur[1] + y
                if first_pair:
                    cur = (x, y)
                    start = cur
                    first_pair = False
                else:
                    # extra coordinate pairs after a moveto are implicit linetos
                    segs.append(("line", cur[0], cur[1], x, y))
                    cur = (x, y)
                continue
            first_pair = False
            if cur is None:
                cur = (0.0, 0.0)
            if up == "L":
                x, y = chunk
                if rel:
                    x, y = cur[0] + x, cur[1] + y
                segs.append(("line", cur[0], cur[1], x, y))
                cur = (x, y)
            elif up == "H":
                x = chunk[0] + (cur[0] if rel else 0.0)
                segs.append(("line", cur[0], cur[1], x, cur[1]))
                cur = (x, cur[1])
            elif up == "V":
                y = chunk[0] + (cur[1] if rel else 0.0)
                segs.append(("line", cur[0], cur[1], cur[0], y))
                cur = (cur[0], y)
            else:                                    # C, S, Q, T
                x, y = chunk[-2], chunk[-1]
                if rel:
                    x, y = cur[0] + x, cur[1] + y
                segs.append(("curve", cur[0], cur[1], x, y))
                cur = (x, y)
    return segs


def drawn_paths(body: str):
    """(tag, d) for every path that is a connector.

    A connector is always `fill="none"`; a path with a real fill is a shape. The
    document-icon glyph in example-nested.html is filled AND stroked and its folded
    corner is a legitimate diagonal, so filtering on stroke alone reported it as a C1
    failure. Filter on fill instead.
    """
    for m in PATH_TAG_RE.finditer(body):
        tag = m.group(0)
        a = attrs_of(tag)
        d = a.get("d")
        if not d:
            continue
        fill = a.get("fill", "none").strip().lower()
        if fill not in ("", "none", "transparent"):
            continue                                 # a filled shape, not a connector
        yield tag, d


def all_paths(body: str):
    for m in PATH_TAG_RE.finditer(body):
        a = attrs_of(m.group(0))
        if a.get("d"):
            yield m.group(0), a["d"]


# --------------------------------------------------------------------------- checks

def check_c1(body, out):
    """Diagonal <line>, and diagonal L segments in paths. Arcs and curves are legal."""
    for m in LINE_RE.finditer(body):
        x1, y1, x2, y2 = (float(v) for v in m.groups())
        if x1 != x2 and y1 != y2:
            fails(f"C1 diagonal <line> ({x1},{y1}) to ({x2},{y2})", out)

    for _tag, d in drawn_paths(body):
        for kind, x0, y0, x1, y1 in path_segments(d):
            # arc and curve are the mandated rounded elbow, not a diagonal.
            # close (Z) is skipped: it is a shape-closing hop, not a connector run.
            if kind != "line":
                continue
            if x0 != x1 and y0 != y1:
                fails(f"C1 diagonal segment ({x0},{y0}) to ({x1},{y1}) in path", out)


def horizontal_strokes(body):
    """Every horizontal stroke as (y, xmin, xmax)."""
    segs = []
    for m in LINE_RE.finditer(body):
        x1, y1, x2, y2 = (float(v) for v in m.groups())
        if y1 == y2:
            segs.append((y1, min(x1, x2), max(x1, x2)))
    for _tag, d in drawn_paths(body):
        for kind, x0, y0, x1, y1 in path_segments(d):
            if kind == "line" and y0 == y1:
                segs.append((y0, min(x0, x1), max(x0, x1)))
    return segs


def vertical_strokes(body):
    """Every vertical stroke as (x, ymin, ymax). C2 covers these too and they were missed."""
    segs = []
    for m in LINE_RE.finditer(body):
        x1, y1, x2, y2 = (float(v) for v in m.groups())
        if x1 == x2:
            segs.append((x1, min(y1, y2), max(y1, y2)))
    for _tag, d in drawn_paths(body):
        for kind, x0, y0, x1, y1 in path_segments(d):
            if kind == "line" and x0 == x1:
                segs.append((x0, min(y0, y1), max(y0, y1)))
    return segs


def check_c2(body, out):
    """A label mask must not overlap, or crowd, the stroke it labels.

    SKILL.md C2: 'On a vertical segment the same gap goes to the side.' The vertical
    case was not implemented, so a mask sitting on a vertical connector passed.
    """
    hsegs = horizontal_strokes(body)
    vsegs = vertical_strokes(body)
    if not hsegs and not vsegs:
        return
    for m in RECT_RE.finditer(body):
        tag = m.group(0)
        a = attrs_of(tag)
        vals = {k: num_or_none(v) for k, v in a.items() if k in ("x", "y", "width", "height")}
        if any(v is None for v in vals.values()):
            continue
        if not {"x", "y", "width", "height"} <= vals.keys():
            continue
        w, h = vals["width"], vals["height"]
        # a label mask: short and wide-ish, height at or under 16
        if h > 16 or w > 160:
            continue
        if a.get("stroke", "none").strip().lower() not in ("", "none"):
            continue  # a styled box, not a mask
        x0, y0 = vals["x"], vals["y"]
        x1, y1 = x0 + w, y0 + h
        hit = False
        for sy, sx0, sx1 in hsegs:
            if sx1 < x0 or sx0 > x1:
                continue
            if y0 - 0.5 <= sy <= y1 + 0.5:
                fails(f"C2 label mask ({x0},{y0} {w}x{h}) sits on a horizontal stroke at y={sy}", out)
                hit = True
                break
            gap = min(abs(sy - y1), abs(y0 - sy))
            if gap < 6:
                fails(f"C2 label mask ({x0},{y0} {w}x{h}) clears horizontal stroke y={sy} "
                      f"by only {gap}px, need 6", out)
                hit = True
                break
        if hit:
            continue
        for sx, sy0, sy1 in vsegs:
            if sy1 < y0 or sy0 > y1:
                continue
            if x0 - 0.5 <= sx <= x1 + 0.5:
                fails(f"C2 label mask ({x0},{y0} {w}x{h}) sits on a vertical stroke at x={sx}", out)
                break
            gap = min(abs(sx - x1), abs(x0 - sx))
            if gap < 6:
                fails(f"C2 label mask ({x0},{y0} {w}x{h}) clears vertical stroke x={sx} "
                      f"by only {gap}px, need 6", out)
                break


def check_grid(body, out):
    """Every coordinate and dimension divides by 4, with only style-guide.md's exemptions."""
    bad = []
    for m in TAG_RE.finditer(body):
        name = m.group(1).lower()
        tag = m.group(0)
        if name in ("!--", "!doctype"):
            continue
        for k, v in ATTR_KV_RE.findall(tag):
            k = k.lower()
            if k not in GRID_ATTRS:
                continue
            val = num_or_none(v)
            if val is None:
                continue                       # "100%", "auto", a var() call
            if k == "font-size":
                if val in GRID_EXEMPT_FONT or val % 4 == 0:
                    continue
                bad.append(f"font-size={val}")
                continue
            if name in ("text", "tspan") and k in ("x", "y"):
                # x is as derived as y. A centred label on a legal box whose width is
                # 4 mod 8 lands on a half-step by construction, so the skill's own node
                # box primitive failed the skill's own check. Both are exempt.
                continue
            if k in ("r", "rx", "ry"):
                if name in ("circle", "ellipse"):
                    # on a circle or ellipse these are real dimensions, not corner
                    # radii, so the radius token set does not apply. Grid does.
                    if val % 4 != 0:
                        bad.append(f"{name}.{k}={val}")
                    continue
                # corner radii come from the radius token set, not the grid
                if val not in RADIUS_TOKENS:
                    bad.append(f"{k}={val}")
                continue
            if val % 4 != 0:
                bad.append(f"{k}={val}")

    # path coordinates were not checked at all, so off-grid elbows passed silently.
    # Only on-path endpoints are checked; see the module docstring on control points.
    for _tag, d in all_paths(body):
        for kind, x0, y0, x1, y1 in path_segments(d):
            if kind == "close":
                continue
            for label, val in (("x", x1), ("y", y1)):
                if val % 4 != 0:
                    bad.append(f"path {label}={val}")

    if bad:
        uniq = sorted(set(bad))
        fails(f"grid: {len(bad)} off-grid value(s), e.g. {', '.join(uniq[:8])}", out)


def node_boxes(body, canvas_area):
    """Stroked rects big enough to be a node. Backgrounds and masks are not nodes."""
    boxes = []
    for m in RECT_RE.finditer(body):
        tag = m.group(0)
        a = attrs_of(tag)
        vals = {k: num_or_none(a.get(k, "")) for k in ("x", "y", "width", "height")}
        if any(v is None for v in vals.values()):
            continue
        if a.get("stroke", "none").strip().lower() in ("", "none"):
            continue                                  # unstroked: background or mask
        w, h = vals["width"], vals["height"]
        if w < 32 or h < 20:
            continue                                  # a tag chip or legend swatch
        if canvas_area and w * h > 0.6 * canvas_area:
            continue                                  # a zone or frame, not a node
        boxes.append((vals["x"], vals["y"], w, h))
    return boxes


def connector_endpoints(body):
    """Both ends of every <line>, and the two ends of every stroked path."""
    pts = []
    for m in LINE_RE.finditer(body):
        x1, y1, x2, y2 = (float(v) for v in m.groups())
        pts.append((x1, y1))
        pts.append((x2, y2))
    for _tag, d in drawn_paths(body):
        segs = path_segments(d)
        if not segs:
            continue
        pts.append((segs[0][1], segs[0][2]))
        pts.append((segs[-1][3], segs[-1][4]))
    return pts


def check_c4(body, out, canvas_area):
    """C4: two connectors never meet a box at the same point, and fan 12px apart."""
    boxes = node_boxes(body, canvas_area)
    pts = connector_endpoints(body)
    if not boxes or not pts:
        return
    tol = 1.5
    for bx, by, bw, bh in boxes:
        edges = {
            "left":   (lambda p: abs(p[0] - bx) <= tol and by - tol <= p[1] <= by + bh + tol, 1),
            "right":  (lambda p: abs(p[0] - (bx + bw)) <= tol and by - tol <= p[1] <= by + bh + tol, 1),
            "top":    (lambda p: abs(p[1] - by) <= tol and bx - tol <= p[0] <= bx + bw + tol, 0),
            "bottom": (lambda p: abs(p[1] - (by + bh)) <= tol and bx - tol <= p[0] <= bx + bw + tol, 0),
        }
        for edge, (on_edge, axis) in edges.items():
            hits = sorted({round(p[axis], 2) for p in pts if on_edge(p)})
            dupes = [p for p in pts if on_edge(p)]
            if len(dupes) > len(hits):
                fails(f"C4 two connectors share a point on the {edge} edge of box "
                      f"({bx},{by} {bw}x{bh})", out)
            # SKILL.md C4: "12px apart or more, 8px minimum on a small box". A small
            # box is one whose relevant edge is under SMALL_EDGE long, where 12px of
            # fanning would crowd the corners. Under 8px always fails.
            edge_len = bh if edge in ("left", "right") else bw
            floor = C4_SMALL_GAP if edge_len < SMALL_EDGE else C4_MIN_GAP
            for a_, b_ in zip(hits, hits[1:]):
                if b_ - a_ < floor:
                    fails(f"C4 attach points {a_} and {b_} on the {edge} edge of box "
                          f"({bx},{by} {bw}x{bh}, edge {edge_len:g}px) are {b_ - a_}px "
                          f"apart, need {floor:g}", out)


def check_output(html, svg, out):
    if re.search(r"<script\b", html, re.I):
        fails("output: <script> present, diagrams ship with no JavaScript", out)
    for m in re.finditer(r'\bsrc\s*=\s*["\']https?://', html, re.I):
        fails("output: external src, diagram must be self-contained", out)
    ext_links = [
        h for h in re.findall(r'<link\b[^>]*href="([^"]+)"', html, re.I)
        if h.startswith("http") and "fonts.googleapis.com" not in h
    ]
    for h in ext_links:
        fails(f"output: external stylesheet {h}, only Google Fonts is allowed", out)
    # every declaration, not just the first. Splitting on the first occurrence meant a
    # single `box-shadow: none` reset anywhere disabled the check for the whole file.
    for m in re.finditer(r"box-shadow\s*:\s*([^;}\"']*)", html, re.I):
        val = m.group(1).strip().lower()
        if val and not val.startswith("none"):
            fails(f"output: box-shadow '{val[:40]}' present, shadows are out and borders are in", out)
    if re.search(r"writing-mode", html, re.I):
        fails("output: writing-mode vertical text", out)
    if not svg:
        fails("output: no inline <svg> found", out)


def check_accent(svg, accent, out):
    n = len(re.findall(re.escape(accent), svg, re.I))
    if n == 0:
        warns(f"signal: accent {accent} never used, no focal element", out)
    # each accent node typically costs a fill plus a stroke plus a label
    if n > 14:
        warns(f"signal: accent {accent} appears {n} times, check it is on 2 elements or fewer", out)


# --------------------------------------------------------------------- composition
#
# Everything above reads raw attributes off one tag at a time. Composition needs the
# opposite: where each element actually lands, which means following `translate()` and
# resolving fill, stroke and font-size through the <style> block, because half the
# corpus styles its nodes with a class rather than an attribute. A node whose fill and
# stroke live in CSS is invisible to an attribute-only reader, and a check that cannot
# see the nodes silently passes everything.

DEAD_BAND = 0.20            # §8: "more than roughly a fifth empty"
DEAD_BAND_MIN_PX = 40.0     # below this a band is a rounding artefact, not dead canvas
FILL_FAIL = 0.35
FILL_WARN = 0.50
PAD_STEP = 32.0             # §6 padding step, the larger of the two
SLACK_WARN = 2 * PAD_STEP   # one padding step per side is the §6 budget on an axis
SLACK_FAIL = 3 * PAD_STEP   # half again over budget, i.e. a dead strip not padding
GAP_VOCAB_MAX = 3           # §1 "a small spacing vocabulary"
GAP_MIN, GAP_MAX = 4.0, 160.0
LANE_OVERLAP = 0.8          # share a row or column, not merely brush past each other
NODE_MIN_W, NODE_MIN_H = 32.0, 20.0
CHAR_W = 0.6                # Geist Mono advance; over-estimates sans, which is the
                            # safe direction: a wider text bbox means a smaller band

CSS_RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S)
VAR_DECL_RE = re.compile(r"--([\w-]+)\s*:\s*([^;}]+)")
VAR_USE_RE = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,[^)]*)?\)")
TOKEN_RE = re.compile(r"<(/?)([a-zA-Z][\w:.-]*)\b([^>]*?)(/?)>|<!--.*?-->", re.S)
TRANSLATE_RE = re.compile(r"\s*translate\(\s*(" + NUM + r")\s*(?:[, ]\s*(" + NUM + r"))?\s*\)\s*")
LEGEND_RE = re.compile(r"^(legend|key)\b", re.I)
STYLED_PROPS = ("fill", "stroke", "font-size")
VOID_TAGS = {"line", "rect", "circle", "ellipse", "path", "polygon", "polyline",
             "use", "image"}
# no geometry of their own, or geometry already accounted for by the outer svg
NON_INK_TAGS = {"title", "desc", "g", "defs", "symbol", "style", "marker", "pattern",
                "clippath", "lineargradient", "radialgradient", "stop", "svg", "tspan",
                "textpath", "a", "switch", "metadata", "filter", "mask", "animate",
                "animatetransform"}
BLANK_PAINTS = ("", "none", "transparent")


def css_rules(html):
    """[(frozenset(class names), {prop: value})] in document order.

    Only the last compound of a selector is read, and every class in it must be on the
    element. That is enough to get `.node.focal` right, which matters: mapping it by
    single class name would paint every `.node` with the focal accent.
    """
    rules = []
    for style in STYLE_RE.findall(html):
        for sel, decls in CSS_RULE_RE.findall(style):
            props = {}
            for p in STYLED_PROPS:
                m = re.search(r"(?<![\w-])" + p + r"\s*:\s*([^;]+)", decls)
                if m:
                    props[p] = m.group(1).strip()
            if "font-size" not in props:
                fm = re.search(r"(?<![\w-])font\s*:\s*([^;]+)", decls)
                if fm:
                    sm = re.search(r"([\d.]+)px", fm.group(1))
                    if sm:
                        props["font-size"] = sm.group(1) + "px"
            if not props:
                continue
            for one in sel.split(","):
                one = one.strip()
                if not one:
                    continue
                classes = frozenset(re.findall(r"\.([\w-]+)", one.split()[-1].split(">")[-1]))
                if classes:
                    rules.append((classes, props))
    return rules


def css_vars(html):
    return {"--" + m.group(1): m.group(2).strip() for m in VAR_DECL_RE.finditer(html)}


def deref(value, variables, depth=0):
    """Expand var(--x) so a class-driven colour can be compared against the accent."""
    if not value or depth > 4:
        return value
    out = VAR_USE_RE.sub(lambda m: variables.get(m.group(1), m.group(0)), value)
    return deref(out, variables, depth + 1) if out != value else out


def styled(a, rules, prop, default=None):
    """Attribute first, then the CSS cascade over the element's classes."""
    v = a.get(prop)
    if v is not None:
        return v.strip()
    have = set(a.get("class", "").split())
    if have:
        for classes, props in rules:
            if prop in props and classes <= have:
                v = props[prop]
    return v.strip() if v is not None else default


def painted(value):
    return (value or "none").strip().lower() not in BLANK_PAINTS


def svg_items(body):
    """(tag, attrs, dx, dy, text, placed) with plain translate() offsets accumulated.

    A rotate, scale or matrix transform is not followed. Its subtree keeps the parent
    offset, so those elements are flagged `placed=False` and dropped from every check
    that depends on where they sit. Flagging per element rather than per file means one
    decorative rotated glyph does not switch the whole check off.
    """
    stack, items = [(0.0, 0.0, True)], []
    for m in TOKEN_RE.finditer(body):
        if m.group(0).startswith("<!--"):
            continue
        closing, name, attrstr, selfclose = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if closing:
            if len(stack) > 1:
                stack.pop()
            continue
        a = {k.lower(): v for k, v in ATTR_KV_RE.findall(attrstr)}
        dx, dy, placed = stack[-1]
        tr = a.get("transform")
        if tr:
            tm = TRANSLATE_RE.fullmatch(tr)
            if tm:
                dx += float(tm.group(1))
                dy += float(tm.group(2)) if tm.group(2) else 0.0
            else:
                placed = False
        text = ""
        if name in ("text", "tspan"):
            end = body.find("</" + name, m.end())
            if end > 0:
                text = re.sub(r"<[^>]*>", " ", body[m.end():end])
        items.append((name, a, dx, dy, text, placed))
        if not selfclose and name not in VOID_TAGS:
            stack.append((dx, dy, placed))
    return items


def _num(a, key, default=None):
    v = a.get(key)
    if v is None:
        return default
    v = v.strip()
    return float(v) if re.fullmatch(NUM, v) else default


def elem_bbox(name, a, dx, dy, text, rules):
    """(x0, y0, x1, y1) of one drawn element, or None if it draws nothing placeable."""
    if name in ("rect", "use", "image"):
        x, y = _num(a, "x", 0.0), _num(a, "y", 0.0)
        w, h = _num(a, "width"), _num(a, "height")
        if None in (x, y, w, h):
            return None
        return (x + dx, y + dy, x + w + dx, y + h + dy)
    if name == "line":
        v = [_num(a, k) for k in ("x1", "y1", "x2", "y2")]
        if None in v:
            return None
        return (min(v[0], v[2]) + dx, min(v[1], v[3]) + dy,
                max(v[0], v[2]) + dx, max(v[1], v[3]) + dy)
    if name == "circle":
        cx, cy, r = _num(a, "cx", 0.0), _num(a, "cy", 0.0), _num(a, "r")
        if r is None:
            return None
        return (cx - r + dx, cy - r + dy, cx + r + dx, cy + r + dy)
    if name == "ellipse":
        cx, cy = _num(a, "cx", 0.0), _num(a, "cy", 0.0)
        rx, ry = _num(a, "rx"), _num(a, "ry")
        if None in (rx, ry):
            return None
        return (cx - rx + dx, cy - ry + dy, cx + rx + dx, cy + ry + dy)
    if name in ("polygon", "polyline"):
        nums = [float(v) for v in re.findall(NUM, a.get("points", ""))]
        if len(nums) < 4:
            return None
        xs, ys = nums[0::2], nums[1::2]
        return (min(xs) + dx, min(ys) + dy, max(xs) + dx, max(ys) + dy)
    if name == "path":
        d = a.get("d")
        if not d:
            return None
        segs = path_segments(d)
        if not segs:
            return None
        xs, ys = [], []
        for _kind, x0, y0, x1, y1 in segs:
            xs += [x0, x1]
            ys += [y0, y1]
        return (min(xs) + dx, min(ys) + dy, max(xs) + dx, max(ys) + dy)
    if name == "text":
        x, y = _num(a, "x"), _num(a, "y")
        if x is None or y is None:
            return None
        fs = _num(a, "font-size")
        if fs is None:
            raw = styled(a, rules, "font-size")
            fm = re.match(r"([\d.]+)", raw) if raw else None
            fs = float(fm.group(1)) if fm else 12.0
        label = " ".join(text.split())
        w = len(label) * fs * CHAR_W
        anchor = a.get("text-anchor", "start")
        x0 = x - w / 2 if anchor == "middle" else x - w if anchor == "end" else x
        return (x0 + dx, y - fs * 0.85 + dy, x0 + w + dx, y + fs * 0.3 + dy)
    return None


def ink_elements(body, rules):
    """[(tag, attrs, bbox, text, placed)] for everything that puts marks on the canvas."""
    out = []
    for name, a, dx, dy, text, placed in svg_items(body):
        if name in NON_INK_TAGS:
            continue
        bb = elem_bbox(name, a, dx, dy, text, rules)
        if bb:
            out.append((name, a, bb, text, placed))
    return out


def is_full_bleed(name, a, bb, vb):
    """The background rect, which is not content and must not anchor the bounding box."""
    if name != "rect":
        return False
    w, h = a.get("width", "").strip(), a.get("height", "").strip()
    if w.endswith("%") and h.endswith("%"):
        return True
    return (bb[2] - bb[0]) >= 0.97 * vb[2] and (bb[3] - bb[1]) >= 0.97 * vb[3]


def box_inside(inner, outer, tol=2.0):
    if (abs(inner[0] - outer[0]) < tol and abs(inner[1] - outer[1]) < tol
            and abs(inner[2] - outer[2]) < tol and abs(inner[3] - outer[3]) < tol):
        return False                       # the same rect, not containment
    return (inner[0] >= outer[0] - tol and inner[1] >= outer[1] - tol
            and inner[2] <= outer[2] + tol and inner[3] <= outer[3] + tol)


def composition_boxes(ink, rules, vb):
    """(containers, nodes).

    A container is a rect holding two or more other boxes AND carrying a stroke. The
    stroke is what separates a zone from a swimlane band: every zone in the corpus has
    a hairline, every lane stripe is fill-only, and scoring a lane's fill ratio is
    meaningless because a lane is deliberately mostly empty.

    A node is a leaf box. The node primitive draws a paper base rect and an identical
    styled rect on top, so identical geometry is merged rather than counted twice, and
    a box wholly inside another leaf (an ER header slab, a divider) is dropped.
    """
    boxes, seen = [], {}
    for name, a, bb, _text, placed in ink:
        if not placed or name not in ("rect", "path", "polygon"):
            continue
        if is_full_bleed(name, a, bb, vb):
            continue
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        if w < NODE_MIN_W or h < NODE_MIN_H:
            continue                       # a tag chip, a label mask, a legend swatch
        fill = styled(a, rules, "fill", "none")
        stroke = styled(a, rules, "stroke", "none")
        filled, stroked = painted(fill), painted(stroke)
        if name in ("path", "polygon") and not filled:
            continue                       # an unfilled path is a connector
        if not (filled or stroked):
            continue
        key = (name, round(bb[0], 1), round(bb[1], 1), round(w, 1), round(h, 1))
        if key in seen:
            prev = seen[key]
            if stroked and not prev["stroked"]:
                prev.update(stroke=stroke, stroked=True, a=a)
            if filled and not prev["filled"]:
                prev.update(fill=fill, filled=True)
            continue
        rec = dict(name=name, bb=bb, w=w, h=h, area=w * h, fill=fill, stroke=stroke,
                   filled=filled, stroked=stroked, a=a)
        seen[key] = rec
        boxes.append(rec)

    for b in boxes:
        b["kids"] = [o for o in boxes if o is not b and box_inside(o["bb"], b["bb"])
                     and o["area"] <= 0.6 * b["area"]]
    grouping = [b for b in boxes if len(b["kids"]) >= 2]
    group_ids = {id(b) for b in grouping}
    containers = [b for b in grouping if b["stroked"]]
    leaves = [b for b in boxes if id(b) not in group_ids]
    nodes = [b for b in leaves
             if not any(box_inside(b["bb"], o["bb"]) for o in leaves if o is not b)]
    for c in containers:
        c["direct"] = [k for k in c["kids"]
                       if not any(id(o) != id(k) and box_inside(k["bb"], o["bb"])
                                  and box_inside(o["bb"], c["bb"]) for o in grouping)]
    return containers, nodes


def legend_floor(ink, vb, boxes):
    """Top y of the bottom legend strip, or None.

    The legend runs the full width of the figure, so leaving it in the bounding box
    hides a dead left or right band behind it. Cropping is only safe when the strip is
    genuinely a bottom strip: if any node or zone reaches into it, this is a legend
    floating inside the diagram area, which is its own §4 anti-pattern, and the crop is
    abandoned rather than guessed at.
    """
    tops = []
    for name, a, bb, text, placed in ink:
        if not placed:
            continue
        if "legend" in a.get("class", "").lower():
            tops.append(bb[1])
        elif name == "text" and LEGEND_RE.match(" ".join(text.split())):
            tops.append(bb[1])
    if not tops:
        return None
    top = min(tops)
    if top < vb[1] + 0.5 * vb[3]:
        return None                        # not a bottom strip
    for name, a, bb, _text, placed in ink:   # pull in the hairline above the strip
        if (placed and name == "line" and abs(bb[3] - bb[1]) < 2 and (bb[2] - bb[0]) > 0.4 * vb[2]
                and top - 40 <= bb[1] < top):
            top = bb[1]
    for b in boxes:
        if b["bb"][3] > top + 0.5:
            return None
    return top


def axis_gaps(nodes, axis):
    """Gaps, on the 4px grid, between boxes that share a row (axis 0) or column (1)."""
    other = 1 - axis
    lanes = []
    for n in sorted(nodes, key=lambda n: n["bb"][axis]):
        a0, a1 = n["bb"][other], n["bb"][other + 2]
        for lane in lanes:
            overlap = min(a1, lane["hi"]) - max(a0, lane["lo"])
            if overlap > LANE_OVERLAP * max(a1 - a0, lane["hi"] - lane["lo"]):
                lane["items"].append(n)
                lane["lo"], lane["hi"] = max(lane["lo"], a0), min(lane["hi"], a1)
                break
        else:
            lanes.append(dict(lo=a0, hi=a1, items=[n]))
    gaps = []
    for lane in lanes:
        row = sorted(lane["items"], key=lambda n: n["bb"][axis])
        for a, b in zip(row, row[1:]):
            g = b["bb"][axis] - a["bb"][axis + 2]
            if GAP_MIN <= g <= GAP_MAX:
                gaps.append(int(round(g / 4.0) * 4))
    return gaps


def hex_rgb(value):
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def is_accent_colour(colour, accent, variables):
    """True for the accent hex or any rgba() wash built on the same triple."""
    if not colour:
        return False
    c = deref(colour, variables).strip().lower()
    if accent in c:
        return True
    m = re.match(r"rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)", c)
    return bool(m and tuple(int(m.group(i)) for i in (1, 2, 3)) == hex_rgb(accent))


def check_composition(body, out, viewbox, html="", accent=ACCENT_LIGHT):
    """The five §8 questions this script can answer without a human eye."""
    if not viewbox:
        return
    vb = viewbox
    rules = css_rules(html)
    variables = css_vars(html)
    ink = ink_elements(body, rules)
    if len(ink) < 6:
        return                             # a template skeleton, nothing to compose
    containers, nodes = composition_boxes(ink, rules, vb)
    floor = legend_floor(ink, vb, containers + nodes)
    bottom = floor if floor is not None else vb[1] + vb[3]

    def in_figure(bb):
        return floor is None or bb[1] < floor - 0.5

    # 1 -- dead canvas
    xs0, ys0, xs1, ys1 = [], [], [], []
    for name, a, bb, _text, placed in ink:
        if not placed or is_full_bleed(name, a, bb, vb) or not in_figure(bb):
            continue
        xs0.append(max(bb[0], vb[0]))
        ys0.append(max(bb[1], vb[1]))
        xs1.append(min(bb[2], vb[0] + vb[2]))
        ys1.append(min(bb[3], bottom))
    if len(xs0) >= 6:
        height = bottom - vb[1]
        bands = (
            ("left", min(xs0) - vb[0], vb[2]),
            ("right", (vb[0] + vb[2]) - max(xs1), vb[2]),
            ("top", min(ys0) - vb[1], height),
            ("bottom", bottom - max(ys1), height),
        )
        for edge, px, dim in bands:
            if dim <= 0 or px < DEAD_BAND_MIN_PX or px / dim <= DEAD_BAND:
                continue
            move = {"top": "up", "bottom": "down"}.get(edge, edge)
            fails(f"composition: {edge} {px:.0f}px of a {dim:.0f}px canvas is empty, "
                  f"{px / dim * 100:.0f} percent. Crop the viewBox or move the figure "
                  f"{move}.", out)

    # 2 -- container fill ratio
    for c in containers:
        kids = c.get("direct", [])
        if len(kids) < 2:
            continue                       # §8 counts a container by what it holds
        ratio = sum(k["area"] for k in kids) / c["area"]
        # every mark inside the zone, not just the node boxes: a connector routed
        # through the slack, or a zone badge sitting in it, means that slack is used
        contents = [bb for _n, _a, bb, _t, placed in ink
                    if placed and box_inside(bb, c["bb"], 1.0)]
        if contents:
            slack_x = ((min(b[0] for b in contents) - c["bb"][0])
                       + (c["bb"][2] - max(b[2] for b in contents)))
            slack_y = ((min(b[1] for b in contents) - c["bb"][1])
                       + (c["bb"][3] - max(b[3] for b in contents)))
        else:
            slack_x = slack_y = max(c["w"], c["h"])
        slack = max(slack_x, slack_y)
        where = f"({c['bb'][0]:g},{c['bb'][1]:g} {c['w']:g}x{c['h']:g})"
        if ratio < FILL_FAIL and slack > SLACK_FAIL:
            fails(f"composition: container {where} is {ratio:.2f} full of its {len(kids)} "
                  f"boxes and runs {slack:.0f}px past them on one axis. Shrink it to its "
                  f"contents plus one padding step, or move something into it.", out)
        elif ratio < FILL_WARN and slack > SLACK_WARN:
            warns(f"composition: container {where} is {ratio:.2f} full of its {len(kids)} "
                  f"boxes, with {slack:.0f}px of slack on one axis. Under half full is "
                  f"over budget, see SKILL.md section 6.", out)

    # 3 -- identical node sizes
    dims = {(round(n["w"]), round(n["h"])) for n in nodes}
    if len(nodes) >= 4 and len(dims) == 1:
        w, h = dims.pop()
        warns(f"composition: all {len(nodes)} nodes are {w:g}x{h:g}. SKILL.md section 4, "
              f"'Identical boxes for every node', erases hierarchy. Vary them by role, "
              f"unless this is genuinely a grid of peers.", out)

    # 4 -- spacing vocabulary
    for axis, label in ((0, "horizontal"), (1, "vertical")):
        vocab = sorted(set(axis_gaps(nodes, axis)))
        if len(vocab) > GAP_VOCAB_MAX:
            warns(f"composition: {len(vocab)} distinct {label} gaps between adjacent "
                  f"nodes, {vocab}. SKILL.md section 1 asks for a small spacing "
                  f"vocabulary; pick two or three and reuse them.", out)

    # 5 -- accent weight
    on_connector = on_shape = 0
    for name, a, bb, _text, placed in ink:
        if placed and not in_figure(bb):
            continue                       # a legend swatch is not the figure's accent
        stroke = styled(a, rules, "stroke")
        fill = styled(a, rules, "fill")
        if name == "line" or (name == "path" and not painted(fill)):
            if is_accent_colour(stroke, accent, variables):
                on_connector += 1
        elif name in ("rect", "circle", "ellipse", "polygon", "path"):
            if name == "rect" and (bb[2] - bb[0] < 24 or bb[3] - bb[1] < 16):
                continue
            if is_accent_colour(stroke, accent, variables) or is_accent_colour(fill, accent, variables):
                on_shape += 1
    if on_connector and not on_shape:
        warns(f"composition: the accent is on {on_connector} connector stroke(s) and on "
              f"no node fill or node stroke. Put it on the thing that matters, not only "
              f"on the arrow pointing at it.", out)


GALLERY_PAGES = {"index.html", "icons.html"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--accent", default=None)
    ap.add_argument("--no-composition", action="store_true",
                    help="skip the composition checks and run the geometry gate alone")
    a = ap.parse_args()

    if Path(a.path).name in GALLERY_PAGES:
        # Gallery and contact-sheet pages hold many diagrams plus their own chrome and
        # script. They are not diagram deliverables, so the geometry rules do not apply.
        print(f"SKIP  {Path(a.path).name}: gallery page, not a diagram")
        return 0

    html = Path(a.path).read_text(encoding="utf-8")
    svg = outer_svg(html)
    body = geometry_body(svg) if svg else ""
    viewbox = viewbox_of(svg) if svg else None
    area = viewbox[2] * viewbox[3] if viewbox else 0.0

    accent = (a.accent.lower() if a.accent
              else ACCENT_TERMINAL if ACCENT_TERMINAL in html.lower()
              else ACCENT_DARK if ACCENT_DARK in html.lower() else ACCENT_LIGHT)

    out = []
    check_output(html, svg, out)
    if svg:
        check_c1(body, out)
        check_c2(body, out)
        check_c4(body, out, area)
        check_grid(body, out)
        check_accent(svg, accent, out)
        if not a.no_composition:
            check_composition(body, out, viewbox, html=html, accent=accent)

    failed = [x for x in out if x[0] == "FAIL"]
    for level, msg in out:
        print(f"{level}  {msg}")
    if not out:
        print(f"PASS  {Path(a.path).name}: all mechanical checks clean")
    elif not failed:
        print(f"PASS  {Path(a.path).name}: no failures, {len(out)} warning(s)")
    else:
        print(f"FAILED  {Path(a.path).name}: {len(failed)} failure(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
