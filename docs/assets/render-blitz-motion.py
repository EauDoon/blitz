"""Author all Blitz README artwork from original vector geometry.

Optional authoring dependencies: Python 3.12+, Pillow 12.0.0, local fonts.
No dependency or font is used by the distributed kit at runtime. Example:
  python docs/assets/render-blitz-motion.py --regular FONT.ttf --bold BOLD.ttf \
      --display DISPLAY-BOLD.ttf --out docs/assets --evidence /path/to/evidence

Only the six named artwork outputs are written to --out. Optional --evidence
writes PNG render checks, every encoded GIF frame, contact sheets and JSON.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

SCALE = 2
WIDTH, HEIGHT = 960, 800
FRAME_MS, FRAME_COUNT = 50, 96
PAPER = "#F6F1E7"
PANEL = "#FFFCF6"
INK = "#252923"
MUTED = "#60635B"
RULE = "#85877E"
SOFT = "#DAD8CD"
ORANGE = "#C13F17"
FONT_FAMILY = "Segoe UI, Arial, sans-serif"
DISPLAY_FAMILY = "Georgia, Times New Roman, serif"
HERO_DESC = ("Blitz. Minimum Viable Company kit. Listen, collect, sprint. "
             "Reduce cycle time. Distinct input fragments gather into evidence "
             "and form a bounded output. This is a process illustration, not "
             "proof of demand, completed work or approval.")
WORKFLOW_DESC = ("Frame the offer and next test; Test observed customer and payer "
                 "behavior; Deliver the result and verify acceptance; Operate with "
                 "reconciled cash and a feasible next cycle. At every gate an owner "
                 "checks evidence and existing authority. Record Proceed for the next "
                 "permitted step, Hold to pause the dependent action, or Walk to reject "
                 "the scoped option. New evidence or revised scope returns to the "
                 "affected gate. A gate does not grant permission.")


def smooth(value):
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def n(value):
    return f"{value:.3f}".rstrip("0").rstrip(".") if isinstance(value, float) else str(value)


def rgb(color):
    return tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))


class Canvas:
    """One geometry record drives accessible SVG and raster inspection views."""

    def __init__(self, width, height, fonts, title, description, background=PAPER):
        self.width, self.height = width, height
        self.fonts = fonts
        self.background = background
        self.image = Image.new("RGB", (width * SCALE, height * SCALE), background)
        self.draw = ImageDraw.Draw(self.image)
        self.text_boxes = []
        self.svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
            f'<title id="title">{html.escape(title)}</title>',
            f'<desc id="description">{html.escape(description)}</desc>',
        ]
        self.rect(0, 0, width, height, background)

    def rect(self, x, y, w, h, fill=None, stroke=None, weight=1):
        coords = tuple(round(v * SCALE) for v in (x, y, x + w, y + h))
        self.draw.rectangle(coords, fill=fill, outline=stroke, width=max(1, round(weight * SCALE)))
        self.svg.append(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" '
                        f'fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="{n(weight)}"/>')

    def line(self, points, color=RULE, weight=2, dashed=False):
        coords = [(round(x * SCALE), round(y * SCALE)) for x, y in points]
        if dashed:
            for a, b in zip(points, points[1:]):
                distance = math.dist(a, b)
                for start in range(0, math.ceil(distance), 14):
                    end = min(start + 7, distance)
                    if distance:
                        p = [(round((a[0] + (b[0] - a[0]) * t / distance) * SCALE),
                              round((a[1] + (b[1] - a[1]) * t / distance) * SCALE)) for t in (start, end)]
                        self.draw.line(p, fill=color, width=round(weight * SCALE))
        else:
            self.draw.line(coords, fill=color, width=round(weight * SCALE))
        path = "M" + " L".join(f"{n(x)} {n(y)}" for x, y in points)
        dash = ' stroke-dasharray="7 7"' if dashed else ''
        self.svg.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{n(weight)}"{dash}/>')

    def arrow(self, a, b, color=RULE, weight=2, size=9):
        self.line([a, b], color, weight)
        theta = math.atan2(b[1] - a[1], b[0] - a[0])
        left = (b[0] - size * math.cos(theta - .6), b[1] - size * math.sin(theta - .6))
        right = (b[0] - size * math.cos(theta + .6), b[1] - size * math.sin(theta + .6))
        self.line([left, b, right], color, weight)

    def text(self, x, baseline, label, size, color=INK, kind="regular", anchor="start"):
        font = ImageFont.truetype(str(self.fonts[kind]), round(size * SCALE))
        xy = (round(x * SCALE), round(baseline * SCALE))
        anch = {"start": "ls", "middle": "ms", "end": "rs"}[anchor]
        box = self.draw.textbbox(xy, label, font=font, anchor=anch)
        self.text_boxes.append({"text": label, "size": size,
                                "box": [round(v / SCALE, 2) for v in box]})
        self.draw.text(xy, label, fill=color, font=font, anchor=anch)
        family = DISPLAY_FAMILY if kind == "display" else FONT_FAMILY
        self.svg.append(f'<text x="{n(x)}" y="{n(baseline)}" font-family="{family}" '
                        f'font-size="{n(size)}" font-weight="{700 if kind != "regular" else 400}" '
                        f'text-anchor="{anchor}" fill="{color}">{html.escape(label)}</text>')

    def raster(self):
        return self.image.resize((self.width, self.height), Image.Resampling.LANCZOS)

    def save(self, path):
        path.write_text("\n".join(self.svg + ["</svg>", ""]), encoding="utf-8", newline="\n")


def fragment(c, box, variant, color=ORANGE, background=PAPER):
    x, y, w, h = box
    if variant == 0:
        c.rect(x, y, w, h, color)
        c.rect(x + 9, y + h * .3, min(9, w * .09), h * .4, background)
    elif variant == 1:
        c.rect(x, y, w, h, background, color, 5)
        c.line([(x + w * .7, y), (x + w * .7, y + h)], color, 5)
    else:
        c.rect(x, y, w, h * .38, color)
        c.rect(x, y + h * .62, w * .76, h * .38, color)


INPUTS = ((72, 559, 118, 30), (143, 608, 109, 32), (88, 665, 142, 28))
COLLECTED = ((418, 569, 132, 26), (418, 609, 132, 26), (418, 649, 132, 26))
OUTPUT = ((759, 600, 108, 18), (759, 632, 108, 18), (759, 664, 108, 18))


def positions(seconds):
    # Three separate records converge, pause as evidence, then fit an open brief.
    if seconds < .5:
        return INPUTS
    if seconds < 1.85:
        amount = smooth((seconds - .5) / 1.35)
        return tuple(tuple(a + (b - a) * amount for a, b in zip(src, dst))
                     for src, dst in zip(INPUTS, COLLECTED))
    if seconds < 2.3:
        return COLLECTED
    if seconds < 3.7:
        amount = smooth((seconds - 2.3) / 1.4)
        return tuple(tuple(a + (b - a) * amount for a, b in zip(src, dst))
                     for src, dst in zip(COLLECTED, OUTPUT))
    return OUTPUT


def hero(fonts, seconds=4.8, dark=False):
    bg, ink, muted, rule = (INK, PAPER, "#C8CBC1", "#9B9F93") if dark else (PAPER, INK, MUTED, RULE)
    accent = "#FF986D" if dark else ORANGE
    c = Canvas(WIDTH, HEIGHT, fonts, "Blitz — Minimum Viable Company kit", HERO_DESC, bg)
    c.rect(52, 45, 84, 8, accent)
    c.text(45, 223, "Blitz", 184, ink, "display")
    c.text(54, 291, "Minimum Viable Company kit", 48, ink)
    c.text(50, 406, "Listen, collect, sprint.", 70, ink, "bold")
    c.text(50, 488, "Reduce cycle time.", 70, ink, "bold")
    # The fine rule separates promise from its abstract process illustration.
    c.line([(54, 518), (906, 518)], rule, 1)
    # Empty source impressions retain the provenance of the collected pieces.
    for box in INPUTS:
        c.rect(*box, None, rule, 2)
    c.arrow((280, 627), (344, 627), rule, 2, 11)
    # Three staggered pages, open and unapproved. No checked/completed state.
    c.rect(386, 542, 188, 149, bg, rule, 2)
    c.rect(396, 552, 188, 149, bg, rule, 2)
    c.rect(406, 562, 188, 149, bg, rule, 2)
    # Evidence stays recorded when a work packet is shaped from it. The record
    # appears smoothly as the orange pieces arrive and then remains in place.
    recorded = smooth((seconds - 1.55) / .3)
    record_color = "#" + "".join(f"{round(a + (b - a) * recorded):02X}"
                                  for a, b in zip(rgb(bg), rgb(muted)))
    for i, box in enumerate(COLLECTED):
        fragment(c, box, i, record_color, bg)
    c.arrow((620, 627), (688, 627), rule, 2, 11)
    c.rect(731, 556, 162, 155, bg, ink, 2)
    c.line([(749, 577), (840, 577)], ink, 4)
    # Corner brackets make the final output's boundary visible, not a seal.
    c.line([(715, 582), (715, 540), (757, 540)], accent, 4)
    c.line([(867, 728), (909, 728), (909, 686)], accent, 4)
    for i, box in enumerate(positions(seconds)):
        fragment(c, box, i, accent, bg)
    c.text(162, 767, "Inputs", 42, ink, "bold", "middle")
    c.text(490, 767, "Evidence", 42, ink, "bold", "middle")
    c.text(810, 767, "Output", 42, ink, "bold", "middle")
    return c


GATES = (
    ("Frame", ["Bound the offer", "and next test."], ["Offer · owner · cap"]),
    ("Test", ["Observe customer", "and payer behavior."], ["Criteria · observation"]),
    ("Deliver", ["Verify the result", "and acceptance."], ["Output · acceptance"]),
    ("Operate", ["Reconcile cash.", "Prepare the next cycle."], ["Cash · capacity · owner"]),
)


def workflow(fonts, mobile=False):
    if mobile:
        return workflow_mobile(fonts)
    c = Canvas(1440, 1020, fonts, "Blitz — evidence gates and owner decisions", WORKFLOW_DESC)
    c.rect(56, 44, 64, 7, ORANGE)
    c.text(56, 115, "Evidence sets the next move.", 58, INK, "bold")
    c.text(56, 161, "Four gates for the specific next commitment.", 30, MUTED)
    # One evidence category group; no misleading automatic gate-passage arrows.
    c.rect(56, 203, 1328, 325, PANEL, RULE, 2)
    for i, (title, body, evidence) in enumerate(GATES):
        x = 80 + i * 332
        if i:
            c.line([(x - 24, 231), (x - 24, 500)], SOFT, 2)
        c.text(x, 257, f"0{i + 1}", 30, ORANGE, "bold")
        c.text(x, 321, title, 49, INK, "bold")
        for j, label in enumerate(body):
            c.text(x, 376 + j * 41, label, 28, INK)
        c.line([(x, 451), (x + 281, 451)], SOFT, 2)
        c.text(x, 490, evidence[0], 24, MUTED)
        c.line([(x + 140, 528), (x + 140, 559)], RULE, 2)
    c.line([(220, 559), (1216, 559)], RULE, 2)
    c.arrow((718, 559), (718, 595), RULE, 2)
    c.rect(56, 596, 1328, 107, INK)
    c.text(84, 660, "AT EVERY GATE", 28, PAPER, "bold")
    c.text(438, 663, "Owner checks evidence + authority", 39, PAPER, "bold")
    c.line([(720, 703), (720, 734)], RULE, 2)
    c.line([(272, 734), (1168, 734)], RULE, 2)
    for x, name, detail in ((56, "Proceed", "Next permitted step"),
                             (504, "Hold", "Pause dependent action"),
                             (952, "Walk", "Reject scoped option")):
        c.arrow((x + 216, 734), (x + 216, 758), RULE, 2)
        c.rect(x, 760, 432, 122, PANEL, RULE, 2)
        c.text(x + 25, 811, name, 39, INK, "bold")
        c.text(x + 25, 855, detail, 27, MUTED)
    c.line([(720, 882), (720, 927)], ORANGE, 2, True)
    c.text(84, 958, "New evidence or revised scope → revisit the affected gate", 34, INK, "bold")
    c.line([(57, 946), (28, 946), (28, 367)], ORANGE, 3, True)
    c.arrow((28, 367), (55, 367), ORANGE, 3, 9)
    c.text(84, 996, "Proceed uses existing authority. A gate does not grant permission.", 26, MUTED)
    return c


def workflow_mobile(fonts):
    c = Canvas(600, 1840, fonts, "Blitz — evidence gates and owner decisions", WORKFLOW_DESC)
    c.rect(44, 35, 64, 7, ORANGE)
    c.text(44, 104, "Evidence sets", 48, INK, "bold")
    c.text(44, 161, "the next move.", 48, INK, "bold")
    c.text(44, 217, "For the next commitment.", 32, MUTED)
    c.rect(44, 252, 512, 748, PANEL, RULE, 2)
    for i, (title, body, _) in enumerate(GATES):
        y = 252 + i * 187
        if i:
            c.line([(67, y), (532, y)], SOFT, 2)
        c.text(68, y + 57, f"0{i + 1}", 28, ORANGE, "bold")
        c.text(127, y + 59, title, 44, INK, "bold")
        for j, label in enumerate(body):
            c.text(68, y + 111 + j * 42, label, 34, INK)
    c.arrow((300, 1000), (300, 1031), RULE, 2)
    c.rect(44, 1032, 512, 175, INK)
    c.text(68, 1077, "AT EVERY GATE", 28, PAPER, "bold")
    c.text(68, 1131, "Owner checks evidence", 35, PAPER, "bold")
    c.text(68, 1180, "+ existing authority", 35, PAPER, "bold")
    c.line([(300, 1207), (300, 1230), (65, 1230), (65, 1533)], RULE, 2)
    for i, (name, detail) in enumerate((("Proceed", "Next permitted step"),
                                      ("Hold", "Pause dependent action"),
                                      ("Walk", "Reject scoped option"))):
        y = 1250 + i * 122
        c.arrow((65, y + 38), (94, y + 38), RULE, 2)
        c.text(112, y + 45, name, 40, INK, "bold")
        c.text(112, y + 91, detail, 32, MUTED)
    c.line([(44, 1630), (556, 1630)], SOFT, 2)
    c.text(68, 1680, "New evidence / revised scope", 32, INK, "bold")
    c.text(68, 1724, "Revisit the affected gate.", 34, INK, "bold")
    c.line([(47, 1708), (21, 1708), (21, 626)], ORANGE, 3, True)
    c.arrow((21, 626), (43, 626), ORANGE, 3, 9)
    c.text(68, 1785, "A gate does not grant", 32, MUTED)
    c.text(68, 1825, "permission.", 32, MUTED)
    return c


def contrast(a, b):
    def lum(value):
        values = [v / 255 for v in rgb(value)]
        linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
        return sum(a * b for a, b in zip(linear, (.2126, .7152, .0722)))
    a, b = sorted((lum(a), lum(b)))
    return round((b + .05) / (a + .05), 3)


def file_record(path):
    data = path.read_bytes()
    return {"path": path.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def evidence_report(directory, canvases, gif, fonts, records):
    directory.mkdir(parents=True, exist_ok=True)
    frames_dir = directory / "encoded-frames"
    frames_dir.mkdir(exist_ok=True)
    for name, c in canvases.items():
        c.raster().save(directory / (name + ".png"))
        if c.width in (600, 960):
            c.raster().resize((320, round(c.height * 320 / c.width)), Image.Resampling.LANCZOS).save(directory / (name + "-320.png"))
    decoded, durations = [], []
    with Image.open(gif) as im:
        loop = im.info.get("loop")
        metadata = {key: value for key, value in im.info.items() if key not in ("transparency", "background")}
        for i in range(im.n_frames):
            im.seek(i)
            frame = im.convert("RGB")
            decoded.append(frame)
            durations.append(im.info.get("duration", 0))
            frame.save(frames_dir / f"{i:03}.png")
    # Full contact sheet preserves every encoded frame for visible inspection.
    thumb_w, thumb_h = 240, 200
    sheet = Image.new("RGB", (thumb_w * 8, math.ceil(len(decoded) / 8) * (thumb_h + 24)), PAPER)
    sd = ImageDraw.Draw(sheet)
    small_font = ImageFont.truetype(str(fonts["regular"]), 14)
    elapsed = 0
    for i, (frame, duration) in enumerate(zip(decoded, durations)):
        x, y = (i % 8) * thumb_w, (i // 8) * (thumb_h + 24)
        sheet.paste(frame.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS), (x, y))
        sd.text((x + 8, y + thumb_h + 2), f"{i:02} · {elapsed / 1000:.2f}s · {duration}ms", fill=INK, font=small_font)
        elapsed += duration
    sheet.save(directory / "motion-all-frames-contact.png")
    keyframes = [hero(fonts, t).raster() for t in (0, 1.15, 2.1, 3.0, 4.8)]
    key_sheet = Image.new("RGB", (480 * 5, 428), PAPER)
    kd = ImageDraw.Draw(key_sheet)
    for i, (frame, label) in enumerate(zip(keyframes, ("Inputs", "Gathering", "Collected evidence", "Shaping output", "Resting poster"))):
        key_sheet.paste(frame.resize((480, 400), Image.Resampling.LANCZOS), (i * 480, 0))
        kd.text((i * 480 + 24, 403), label, fill=INK, font=small_font)
    key_sheet.save(directory / "motion-story-contact.png")
    # GIF labels and title must be bit-identical in every decoded frame.
    fixed_regions = ((0, 0, WIDTH, 533), (0, 737, WIDTH, HEIGHT))
    fixed_ok = all(ImageChops.difference(decoded[0].crop(box), frame.crop(box)).getbbox() is None
                   for frame in decoded for box in fixed_regions)
    extent = None
    changed_counts = []
    from_first = []
    for frame in decoded:
        box = ImageChops.difference(decoded[0], frame).getbbox()
        if box:
            extent = box if extent is None else (min(extent[0], box[0]), min(extent[1], box[1]), max(extent[2], box[2]), max(extent[3], box[3]))
        mask = ImageChops.difference(decoded[0], frame).convert("L").point(lambda v: 255 if v else 0)
        from_first.append(mask.histogram()[255])
    for previous, frame in zip(decoded, decoded[1:]):
        mask = ImageChops.difference(previous, frame).convert("L").point(lambda v: 255 if v else 0)
        changed_counts.append(mask.histogram()[255])
    poster_delta = ImageStat.Stat(ImageChops.difference(canvases["blitz-motion-poster"].raster(), decoded[-1]))
    fits = {}
    for name, c in canvases.items():
        clipped = [entry for entry in c.text_boxes if entry["box"][0] < 0 or entry["box"][1] < 0 or entry["box"][2] > c.width or entry["box"][3] > c.height]
        overlaps = []
        for i, a in enumerate(c.text_boxes):
            for b in c.text_boxes[i + 1:]:
                x1, y1, x2, y2 = a["box"]
                u1, v1, u2, v2 = b["box"]
                if max(x1, u1) < min(x2, u2) and max(y1, v1) < min(y2, v2):
                    overlaps.append([a["text"], b["text"]])
        fits[name] = {"dimensions": [c.width, c.height], "clipped_text": clipped, "overlapping_text": overlaps, "text_boxes": c.text_boxes}
    report = {
        "files": records,
        "gif": {"dimensions": [WIDTH, HEIGHT], "authored_frames": FRAME_COUNT,
                "encoded_frames": len(decoded), "duration_ms": sum(durations),
                "frame_durations_ms": durations, "loop_extension": loop,
                "metadata_keys": list(metadata), "fixed_text_pixels_identical": fixed_ok,
                "motion_extent": extent, "max_consecutive_changed_pixels": max(changed_counts),
                "max_consecutive_changed_canvas_fraction": round(max(changed_counts) / (WIDTH * HEIGHT), 5),
                "max_changed_from_first_pixels": max(from_first),
                "last_frame_vs_poster_mean_absolute_channel_error": [round(v, 3) for v in poster_delta.mean],
                "final_still_duration_ms": durations[-1]},
        "contrast_ratios": {"ink_on_paper": contrast(INK, PAPER), "muted_on_paper": contrast(MUTED, PAPER),
                            "orange_on_paper": contrast(ORANGE, PAPER), "rule_on_paper": contrast(RULE, PAPER),
                            "paper_on_ink": contrast(PAPER, INK)},
        "at_320px": {"hero_wordmark_px": round(184 / 3, 2), "hero_descriptor_px": 16,
                     "hero_tagline_px": round(70 / 3, 2), "hero_min_stage_label_px": 14,
                     "mobile_workflow_body_px": round(32 * 320 / 600, 2)},
        "fit": fits,
        "limits": ["Font fallback can differ on other hosts; no font is bundled.",
                   "Raster fit checks do not prove browser font fallback fit; inspect rendered SVG views.",
                   "Static pixel and motion-area checks are not a clinical photosensitivity assessment.",
                   "Artwork does not establish business readiness, demand or permission."]
    }
    (directory / "art-checks.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regular", type=Path, required=True)
    parser.add_argument("--bold", type=Path, required=True)
    parser.add_argument("--display", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()
    fonts = {"regular": args.regular, "bold": args.bold, "display": args.display}
    for path in fonts.values():
        if not path.is_file():
            parser.error(f"Missing local font: {path}")
    args.out.mkdir(parents=True, exist_ok=True)
    canvases = {"blitz-motion-poster": hero(fonts), "workflow": workflow(fonts),
                "workflow-mobile": workflow(fonts, mobile=True),
                "blitz-banner-light": hero(fonts), "blitz-banner-dark": hero(fonts, dark=True)}
    files = []
    for name, canvas in canvases.items():
        path = args.out / (name + ".svg")
        canvas.save(path)
        files.append(path)
    frames = [hero(fonts, i * FRAME_MS / 1000).raster() for i in range(FRAME_COUNT)]
    # A global palette makes all static text pixel-identical across frames.
    sample = Image.new("RGB", (WIDTH, HEIGHT * 4), PAPER)
    for j, i in enumerate((0, 24, 43, 95)):
        sample.paste(frames[i], (0, HEIGHT * j))
    palette = sample.quantize(colors=122, method=Image.Quantize.MEDIANCUT)
    # Reserve exact brand colors rather than allowing median cut to shift the
    # dominant paper field. A fixed palette also prevents background flicker.
    colors = palette.getpalette()[:122 * 3]
    colors += [channel for color in (PAPER, INK, MUTED, RULE, SOFT, ORANGE) for channel in rgb(color)]
    colors += [0] * (768 - len(colors))
    palette.putpalette(colors)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    # Pillow's palette search uses a reduced-precision lookup cache. Pin the
    # selected indices after lookup as well, so flat brand fields stay exact.
    exact = indexed[0].getpalette()
    for color in (PAPER, INK, MUTED, RULE, SOFT, ORANGE):
        index = Image.new("RGB", (1, 1), color).quantize(palette=palette, dither=Image.Dither.NONE).getpixel((0, 0))
        exact[index * 3:index * 3 + 3] = rgb(color)
    for frame in indexed:
        frame.putpalette(exact)
    gif = args.out / "blitz-motion.gif"
    # Deliberately omit loop: no NETSCAPE repeat extension; play once and hold.
    indexed[0].save(gif, save_all=True, append_images=indexed[1:], duration=FRAME_MS, optimize=True, disposal=1)
    files.append(gif)
    records = [file_record(path) for path in files]
    if args.evidence:
        report = evidence_report(args.evidence, canvases, gif, fonts, records)
        print(json.dumps({"files": records, "gif": report["gif"], "contrast_ratios": report["contrast_ratios"],
                          "fit_issues": {name: {k: v for k, v in detail.items() if k in ("clipped_text", "overlapping_text")}
                                         for name, detail in report["fit"].items()}}, indent=2))
    else:
        print(json.dumps({"files": records}, indent=2))


if __name__ == "__main__":
    main()
