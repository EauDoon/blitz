"""Rebuild the original Blitz README hero; no downloaded art or bundled fonts.

Requires Python 3.12+ and Pillow 12.0.0. Run from the repository root:
  python docs/assets/render-blitz-motion.py --regular FONT.ttf --bold BOLD.ttf
The reviewed render uses the installed Windows Segoe UI regular/bold fonts.
Only the two explicitly named outputs in --out are written.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, SCALE = 960, 360, 2
FRAME_MS, FRAME_COUNT = 50, 96
BG = "#101C2E"
INK = "#F2F6FD"
MUTED = "#BBC9DD"
LINE = "#405571"
BLUE = "#7CA6FF"
AMBER = "#F2B968"
GATES = ((74, "Frame"), (344, "Test"), (616, "Deliver"), (886, "Operate"))


def smooth(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def rgb(value: str) -> tuple[int, int, int]:
    return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))


class Canvas:
    """Keep the still SVG and raster frames on the same original geometry."""

    def __init__(self, regular: Path, bold: Path):
        self.image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
        self.draw = ImageDraw.Draw(self.image)
        self.fonts = {False: regular, True: bold}
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title description">',
                    '<title id="title">Blitz, a founder operating kit</title>',
                    '<desc id="description">Make a promise, deliver it, get paid and run the next cycle. The four evidence gates are Frame, Test, Deliver and Operate. This illustration does not establish that a gate is passed.</desc>']

    def rect(self, x, y, w, h, fill, stroke=None, width=1):
        self.draw.rectangle(tuple(round(v * SCALE) for v in (x, y, x + w, y + h)),
                            fill=fill, outline=stroke, width=round(width * SCALE))
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="{width}"/>')

    def line(self, coords, color, width):
        self.draw.line(tuple(round(v * SCALE) for v in coords), fill=color, width=round(width * SCALE))
        x1, y1, x2, y2 = coords
        self.svg.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"/>')

    def text(self, x, baseline, label, size, color, bold=False, anchor="start"):
        font = ImageFont.truetype(str(self.fonts[bold]), size * SCALE)
        self.draw.text((round(x * SCALE), round(baseline * SCALE)), label, fill=color,
                       font=font, anchor={"start": "ls", "middle": "ms", "end": "rs"}[anchor])
        self.svg.append(f'<text x="{x}" y="{baseline}" font-family="Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}" fill="{color}">{html.escape(label)}</text>')

    def finish(self):
        return self.image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def base(regular: Path, bold: Path) -> Canvas:
    c = Canvas(regular, bold)
    c.rect(0, 0, WIDTH, HEIGHT, BG)
    c.rect(0.5, 0.5, WIDTH - 1, HEIGHT - 1, None, LINE)
    c.rect(48, 36, 30, 4, BLUE)
    c.text(47, 148, "Blitz", 116, INK, True)
    c.text(53, 184, "A founder operating kit", 24, MUTED)
    c.text(620, 85, "Make a promise.", 25, INK)
    c.text(620, 120, "Deliver. Get paid.", 25, INK)
    c.text(620, 155, "Run the next cycle.", 25, INK)
    c.line((74, 261, 886, 261), LINE, 2)
    for i, (x, label) in enumerate(GATES, 1):
        c.text(x, 231, f"0{i}", 16, MUTED, anchor="middle")
        c.rect(x - 15, 246, 30, 30, BG, BLUE, 2)
        c.rect(x - 3, 258, 6, 6, BLUE)
        # Slightly inset the endpoint names, retaining generous canvas margins.
        c.text(x if i not in (1, 4) else (91 if i == 1 else 869), 326,
               label, 31, INK, anchor="middle")
    return c


def marker(t: float) -> tuple[float, float]:
    """Three measured moves with pauses. Fade is confined to a 12 px marker.

    0-.45: Frame; .45-1.35: move; 1.35-1.7: Test; 1.7-2.6: move;
    2.6-2.95: Deliver; 2.95-3.85: move; 3.85-4.3: Operate;
    4.3-4.7: fade out; 4.7-4.8: neutral still. The GIF plays once.
    """
    for start, end, a, b in ((.45, 1.35, 74, 344), (1.7, 2.6, 344, 616), (2.95, 3.85, 616, 886)):
        if start <= t < end:
            return a + (b - a) * smooth((t - start) / (end - start)), 1.0
    if t < .45:
        return 74, 1.0
    if t < 1.7:
        return 344, 1.0
    if t < 2.95:
        return 616, 1.0
    if t < 4.3:
        return 886, 1.0
    if t < 4.7:
        return 886, 1.0 - smooth((t - 4.3) / .4)
    return 886, 0.0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regular", type=Path, required=True)
    parser.add_argument("--bold", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    still = base(args.regular, args.bold)
    # Neutral still: no gate is shown as approved; all four remain visible.
    poster = args.out / "blitz-motion-poster.svg"
    poster.write_text("\n".join(still.svg + ["</svg>", ""]), encoding="utf-8")
    background = still.image
    frames = []
    for i in range(FRAME_COUNT):
        frame = background.copy()
        x, opacity = marker(i * FRAME_MS / 1000)
        # Local alpha compositing preserves route/node geometry under the packet.
        overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle(tuple(round(v * SCALE) for v in (x - 6, 255, x + 6, 267)),
                     fill=(*rgb(AMBER), round(255 * opacity)))
        frame.paste(overlay, (0, 0), overlay)
        frames.append(frame.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS))
    # A shared palette keeps the static title, text and edges identical per frame.
    sample = Image.new("RGB", (WIDTH, HEIGHT * 4 + 32))
    for j, i in enumerate((0, 20, 49, 83)):
        sample.paste(frames[i], (0, HEIGHT * j))
    # Reserve palette representation for the tiny marker and its fade shades.
    sd = ImageDraw.Draw(sample)
    for j, alpha in enumerate((0, 64, 128, 192, 255)):
        shade = tuple(round(a + (b - a) * alpha / 255)
                      for a, b in zip(rgb(BG), rgb(AMBER)))
        sd.rectangle((j * 192, HEIGHT * 4, (j + 1) * 192, HEIGHT * 4 + 31), fill=shade)
    palette = sample.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    output = args.out / "blitz-motion.gif"
    indexed[0].save(output, save_all=True, append_images=indexed[1:],
                    duration=FRAME_MS, optimize=True, disposal=1)
    print(json.dumps({"canvas": [WIDTH, HEIGHT], "authored_frames": FRAME_COUNT,
                      "authored_duration_ms": FRAME_COUNT * FRAME_MS,
                      "files": [{"path": p.name, "bytes": p.stat().st_size,
                                 "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                                for p in (output, poster)]}, indent=2))


if __name__ == "__main__":
    main()
