# Blitz README artwork

Original editorial artwork for Blitz, a **Minimum Viable Company kit**. The exact two-line tagline is:

> Listen, collect, sprint.<br>Reduce cycle time.

The 11 October 2026 revision replaces the earlier small-marker animation with a visible transformation of distinct inputs into collected evidence and a bounded output. Warm paper, charcoal type and a restrained orange accent give the reusable kit a technical field-guide treatment. The composition uses one responsive hero; its descriptor is 16 pixels and its tagline is about 23 pixels when the image is displayed at 320 pixels wide.

| File | Canvas | Purpose |
|---|---|---|
| `blitz-motion-poster.svg` | 960 × 800 | Default static hero and reduced-motion fallback |
| `blitz-motion.gif` | 960 × 800 | One 4.8-second sequence, then a coherent still |
| `workflow.svg` | 1440 × 1020 | Four evidence gates, owner check, decisions and return path |
| `workflow-mobile.svg` | 600 × 1840 | The same gate and decision relationships in a legible narrow layout |
| `blitz-banner-light.svg` | 960 × 800 | Retained legacy path, updated to the current static hero |
| `blitz-banner-dark.svg` | 960 × 800 | Retained legacy path, updated to the same composition in charcoal |
| `render-blitz-motion.py` | — | Editable authoring source for all six artwork outputs |

## Meaning and boundaries

The hero's three distinct fragments gather into a common evidence record, pause, and change dimensions to fit a bounded work packet. The evidence stays visible when the output is formed. Input, evidence and output labels remain fixed throughout. The orange corner marks describe a scope boundary; they are not an approval seal. The picture does not claim that demand is validated, a task is accepted, a company is demonstrated, or an action is authorized.

The workflow summarizes the [company profile](../../Blitz/profiles/company.md): Frame bounds the offer and next test; Test observes customer and payer behavior; Deliver verifies the result and acceptance; Operate reconciles cash and prepares the next cycle. The four gates feed an owner check of evidence and existing authority, followed by a recorded Proceed, Hold or Walk decision for the specific next commitment. New evidence or revised scope returns to the affected gate. The shared gate group is deliberate: reading order is not automatic progression or permission. The [repository README](../../README.md) supplies the full text equivalent, including the distinctions between preparation, demonstrated MVC and repetition.

The tagline is an operating intention. It does not replace the evidence gates or promise a measured reduction in cycle time.

## Construction and provenance

The geometry, composition and text treatment were authored specifically for this repository with an AI assistant. Only original vector lines, rectangles, brackets and fragment patterns were used. No copied logos, third-party artwork, stock media, icon packs, image templates, screenshots, remote fonts or downloaded visual assets are included. The forms illustrate this kit; they are not a claim of trademark registration or ownership of a geometric idea.

All SVGs have opaque backgrounds and accessible `title` and `desc` elements. They contain no scripts, animation, tracking, embedded raster images or external resource references. The wordmark requests `Georgia`, `Times New Roman`, then a local serif; other text requests `Segoe UI`, `Arial`, then a local sans-serif. Fonts are supplied by the viewer's system, so metrics can vary. No font files are distributed.

The GIF was rasterized from the same geometry as the static poster. It has 96 authored samples, 56 encoded frames after identical pauses are combined, a total duration of 4,800 milliseconds, and a final still held for 1,100 milliseconds within that duration. There is no repeat extension, comment, or application extension. It plays once and rests on the final frame. Text never moves or changes. Motion is confined to the illustration beneath the tagline; there is no flashing, full-frame movement or looping. The README selects it only for `prefers-reduced-motion: no-preference`; the static SVG is the default fallback.

## Reproduction

The renderer has **optional authoring dependencies only**: Python 3.12+, Pillow 12.0.0, and three explicitly supplied local font files. Using Blitz does not require them. In an authoring environment with those prerequisites, run from the repository root:

```sh
python docs/assets/render-blitz-motion.py \
  --regular /path/to/regular.ttf \
  --bold /path/to/bold.ttf \
  --display /path/to/display-bold.ttf
```

Use `--out /path/to/output` to write to another directory. The renderer writes only the six named artwork outputs there. Optional `--evidence /path/to/evidence` also saves raster inspection views, all decoded animation frames, contact sheets, and duration, pixel, contrast and text-fit checks. The default asset build needs no browser. Files are written with LF newlines; the GIF remains binary.

The reviewed build used Python 3.12.10, Pillow 12.0.0, and existing Windows Segoe UI regular/bold and Georgia bold fonts. A second render reproduced all six files byte for byte. Different fonts or renderer versions can change pixels and hashes. The reviewed local font SHA-256 digests are:

| Local authoring font | SHA-256 |
|---|---|
| Segoe UI regular (`segoeui.ttf`) | `8134dbcd09e7b123c9a7f229d49cffbcb01352cc72ea5e1076b65d0dca9f73cd` |
| Segoe UI bold (`segoeuib.ttf`) | `aeb9e4a6ec5cc59f4d72df8189032d7dbb28f45161cf1552174818b5465dac4e` |
| Georgia bold (`georgiab.ttf`) | `72a6cd94fab6c179392075d3fb361e269cdddfad41bb7ab385fa22a37e49a900` |

## Reviewed files

| File | Bytes | SHA-256 |
|---|---:|---|
| `blitz-motion.gif` | 183,052 | `6fa3b6b19fe0d2c89168870306b9cc1cf4b067648f0e9476d321532e62ee1116` |
| `blitz-motion-poster.svg` | 4,201 | `8e34f460b1b89515d11c438d1e8cc5159138c51d194a14a6bfd54192e7b29b41` |
| `workflow.svg` | 8,569 | `65984550df88a9afa4f9900b59120b6203d089825b508fe88675622a6c3e0ff3` |
| `workflow-mobile.svg` | 7,358 | `a522b2baa40540c63c46d4442de894a16f86df9f702e5e8362b9517665e86c4e` |
| `blitz-banner-light.svg` | 4,201 | `8e34f460b1b89515d11c438d1e8cc5159138c51d194a14a6bfd54192e7b29b41` |
| `blitz-banner-dark.svg` | 4,201 | `b6e686aeb8bd77fee1bb39d6567de067f0f6aeb102301578cdab63a16b8add77` |

The authoring source SHA-256 is `0ce1aea949b24e6b4c5a57babd6672267fd86fd71d66b2c01688ff670684dfd1`.

The earlier reviewed GIF remains reachable in repository history at the same path: 59,881 bytes, 960 × 360, 63 encoded frames, 4,800 milliseconds, SHA-256 `bb4153ee9d024d2e242f439b596d5dcb508154c8d7941c8d33dea427aa29a65b`. That is a historical version, not the current output. Recording it preserves the exact provenance of the earlier public artifact.

## Inspection and limits

Every encoded frame was exported and inspected in a contact sheet. Pixel checks confirm identical title and label regions across frames, exact paper-color preservation, no loop extension, and no more than 1.14% of canvas pixels changing between consecutive encoded frames. The last frame and poster share geometry; their mean absolute channel difference is at most 0.219 out of 255 because the GIF uses a palette. These are scoped pixel checks, not a clinical photosensitivity assessment.

The text-fit check found no clipped or overlapping text. The poster, both retained banners and both workflows were rendered in local Chrome. The hero and mobile workflow were inspected at 320 pixels wide. Main ink on paper is 13.14:1, secondary ink 5.43:1, orange 4.67:1 and structural rules 3.24:1. The mobile workflow's body text is at least 17 pixels at 320 pixels wide; the hero's fixed diagram labels are 14 pixels. System-font fallbacks on other hosts can produce different typography. Standalone artwork checks do not establish how every Markdown client handles `picture` media selection.

This note records provenance. It does not grant a license or change the repository's licensing position. See [rights and provenance](../PROVENANCE.md) for repository terms and retained third-party notices.
