# Blitz README artwork

These files were created for this repository's README during the design task on 11-10-2026.

| File | Canvas | Purpose |
|---|---|---|
| `blitz-motion.gif` | 960 × 360 | One restrained evidence-marker pass through the four gates, followed by a still |
| `blitz-motion-poster.svg` | 960 × 360 | Static reduced-motion and unsupported-source fallback |
| `render-blitz-motion.py` | — | Shared original geometry and reproducible animation authoring source |
| `blitz-banner-light.svg` | 1400 × 400 | Earlier light-theme Blitz wordmark and four-stop angular route |
| `blitz-banner-dark.svg` | 1400 × 400 | Matching earlier dark-theme banner |
| `workflow.svg` | 1400 × 600 | Frame, Test, Deliver and Operate, with a Hold / revise return path |
| `workflow-mobile.svg` | 600 × 1120 | Stacked version of the same gates for narrow screens |

## Source and construction

The geometry, layout and text treatment were authored specifically for this task with an AI assistant. No copied artwork, third-party logos, icon packs, stock media, image templates or external images were used. The routes, stops and evidence marker are simple original paths and rectangles. They illustrate this repository; they are not a claim of trademark registration or exclusive ownership of a geometric idea.

The workflow summarizes the repository's [company profile](../../Blitz/profiles/company.md). Its gate names and operating language come from that document. The complete meaning remains available as text in the [repository README](../../README.md) and company profile. The pictures do not establish readiness, evidence, permission or approval for any company. The animated marker indicates reading order, not a gate result; it disappears when the animation finishes.

The SVG assets have opaque backgrounds and accessible `title` and `desc` elements. They contain no scripts, tracking, animation, embedded raster images, external resource links or font files. Text requests `Segoe UI`, `Arial`, then a generic sans-serif from the viewer's existing fonts. The renderer chooses the available font; no font is copied into this repository.

The motion hero uses a navy canvas, pale text, cobalt gate outlines and an amber evidence marker. Its text stays still. It plays once for 4.8 seconds, then rests on the neutral poster geometry; the GIF has no repeat extension. The README selects the static SVG when reduced motion is requested and uses it as the fallback image. The GIF is selected only for `prefers-reduced-motion: no-preference`. Both variants retain the same four gate names. The complete text equivalent appears in the README.

The GIF was rendered with Python 3.12.10, Pillow 12.0.0 and the existing Windows Segoe UI regular and bold fonts, rasterized into pixels. No font files or rendering libraries are distributed with the artwork. Rebuild with your own locally available fonts by running:

```sh
python docs/assets/render-blitz-motion.py --regular /path/to/regular.ttf --bold /path/to/bold.ttf
```

Install Pillow 12.0.0 in your authoring environment first. The source writes only `blitz-motion.gif` and `blitz-motion-poster.svg` in its own directory by default. A different font or renderer version can change pixels and hashes. The reviewed output is 59,881 bytes, with 63 encoded frames (96 authored samples; identical pauses are merged), a total duration of 4,800 ms and no comments or application metadata. Its SHA-256 is `bb4153ee9d024d2e242f439b596d5dcb508154c8d7941c8d33dea427aa29a65b`.

The earlier banners share geometry and wording across themes. Both workflow variants use a light canvas so their labels and line contrast remain predictable in either theme. The mobile workflow keeps body text at 32 canvas pixels, equivalent to about 17 pixels when displayed at 320 pixels wide.

This note records provenance. It does not grant a license or change the repository's licensing position. See [rights and provenance](../PROVENANCE.md) for the repository's terms and third-party notices.
