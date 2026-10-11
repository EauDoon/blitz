# Export to PNG / SVG

Convert a generated diagram HTML file into a portable `.svg` and/or `.png` next to it. **Manual only: never run unprompted.**

## Trigger

Load this file when:

- The user asks for an export by name, for example "export this diagram" or "/export".
- The user asks in natural language to export, save, rasterize, convert, or download a diagram in `.svg` or `.png` form. Typical phrasings:
  - "export this as PNG"
  - "save as SVG"
  - "give me a PNG of that diagram"
  - "rasterize it"
  - "convert to png and svg"

The slash command is a thin wrapper that delegates here: both paths run the same procedure below.

## Scope

Both formats are **diagram-only**: just the `<svg>` node. Editorial wrappers (header, summary cards, footer in `-full` variants) are intentionally dropped: the export deliverable is the diagram itself, suitable for Figma, slides, social cards, or blog images.

If the user explicitly asks for "a screenshot of the whole page including the cards", that's a different request: fall back to a normal full-page screenshot via the user's OS or browser.

## SVG export procedure

1. Read the source HTML file.
2. Extract the **first** `<svg ...>...</svg>` block. Use a multiline regex anchored on `<svg` and `</svg>`. Most generated diagrams have only one SVG; if there are multiple, the first is the diagram (gallery files are an exception: see *Edge cases*).
3. Make it standalone:
   - Ensure the opening tag has `xmlns="http://www.w3.org/2000/svg"`. Add it if missing.
   - Ensure a `viewBox` is present. The skill's templates always include one; warn the user if absent rather than guessing.
   - Inject Google Fonts `@import` so the SVG renders with correct typography in a browser:
     ```svg
     <defs>
       <style>@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap');</style>
     </defs>
     ```
     If the SVG already contains a `<defs>` block, **merge** the `<style>` into it (don't add a second `<defs>`).
4. Prepend `<?xml version="1.0" encoding="UTF-8"?>\n` so the file is well-formed XML.
5. Write to `<basename>.svg` next to the source (e.g. `example-architecture.html` → `example-architecture.svg`). Honour an explicit output path if the user provides one.

### Caveat to surface to the user

Tools that don't fetch remote fonts at import time (offline Illustrator, some Figma import paths, older SVG viewers) will substitute typography. The SVG renders correctly in any modern browser. For pixel-perfect portability, recommend the PNG export.

**Medallion: do not export as SVG, use PNG.** `type-medallion.md` §2.2 mandates `<foreignObject>` for every wrapping field value, and `assets/example-medallion.html` carries 15 of them. Browsers render `foreignObject`; Figma, Illustrator, Inkscape and most SVG import paths drop it silently, so the tool, format and writer values vanish from every tier card and the export looks like a set of empty boxes with no error anywhere. The same warning applies to any other diagram containing a `foreignObject`. Before an SVG export, grep the source for `foreignObject`; if it is present, tell the user the SVG will lose those values and offer the PNG instead.

This is also why the bullet at the bottom of this file forbids *adding* `foreignObject` during export. Medallion is the one type that ships with it by design, and PNG is the export path that survives it.

## PNG export procedure

Render **the original HTML** (not the extracted SVG) and screenshot only the `<svg>` element's bounding box. This keeps font loading reliable (already wired in the source HTML) while satisfying the "diagram only" rule.

**The PNG is opaque, not transparent.** Every diagram opens its SVG with a full-bleed background rect (`<rect width="100%" height="100%" fill="#f5f5f5"/>`, or the same rect sized to the viewBox), so the `paper` colour is painted *inside* the screenshot region. `omit_background=True` only drops the browser's own page background, which the rect already covers. The default export therefore carries a `#f5f5f5` field on a light diagram and `#0f0f0f` on a dark one. Placed on a slide of a different colour, that reads as a halo.

To get a genuinely transparent PNG, hide the background rect before rasterising (see *Transparent variant* below). Otherwise match the slide to the skin: light PNG on a light slide, dark PNG on a `#0f0f0f` slide.

### Detection

Before running anything, verify Playwright is installed:

```
python -c "import playwright" 2>NUL || python -c "import playwright"
```

If the import fails, surface this exact instruction to the user and stop:

> Playwright isn't installed. To enable PNG export, run:
> ```
> pip install playwright
> playwright install chromium
> ```
> Then ask me to export again.

Don't auto-install. The user asked for one feature, not a system change.

### Rasterize

Write the snippet below to a temp file and run it with `python <tmp.py> <src.html> <out.png>`:

```python
from playwright.sync_api import sync_playwright
import sys, pathlib

src, out = sys.argv[1], sys.argv[2]
scale = int(sys.argv[3]) if len(sys.argv) > 3 else 2

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(device_scale_factor=scale)
    page.goto(f"file://{pathlib.Path(src).resolve()}")
    page.wait_for_load_state("networkidle")
    page.locator("svg").first.screenshot(path=out, omit_background=True)
    browser.close()
```

Default `device_scale_factor=2` for crisp output. Accept `1` for compact assets or `3` for print/retina hero use, passed as a third CLI arg.

### Transparent variant

Only when the user asks for transparency. Hide the full-bleed background rect in the loaded page, then screenshot. This touches the DOM in the browser, never the source file.

```python
    page.eval_on_selector("svg", """svg => {
      const vb = svg.viewBox.baseVal;
      for (const r of svg.querySelectorAll('rect')) {
        const w = r.getAttribute('width'), h = r.getAttribute('height');
        const fullBleed = (w === '100%' && h === '100%') ||
                          (parseFloat(w) >= vb.width && parseFloat(h) >= vb.height);
        if (fullBleed && !r.getAttribute('x') && !r.getAttribute('y')) {
          r.style.display = 'none';
          break;
        }
      }
    }""")
    page.locator("svg").first.screenshot(path=out, omit_background=True)
```

Warn the user that a transparent light diagram is unreadable on a dark surface and the reverse, because `ink` and `muted` are picked for contrast against `paper`. Transparency removes the guarantee. Converting the skin with `scripts/skin.py` is the correct fix for a dark surface; transparency is not.

### Output naming

`example-architecture.html` → `example-architecture.png`, written next to the source. Honour explicit user-provided paths.

## Edge cases

- **Source is `assets/index.html`** (the gallery, multiple SVGs in one file): refuse the export and ask the user which specific diagram file they meant. Don't guess.
- **No `<svg>` block found**: the source isn't a diagram file. Tell the user; don't write anything.
- **Surrounding HTML matters to the user**: they want cards/header in the image. Tell them this skill exports diagrams only, and recommend a browser-based full-page screenshot (or a separate PDF print).
- **Source is missing fonts at runtime**: Playwright will substitute, the screenshot will look off. Check that the source HTML has the `<link href="...fonts.googleapis.com...">` tag in `<head>`. If absent, the file isn't from a current template: fix the source rather than working around it in export.

## What this command never does

- Modifies the source HTML.
- Adds export buttons or `<script>` tags to generated diagrams (the "no JS in deliverables" rule in SKILL.md §7 Output still stands).
- Auto-emits `.svg` or `.png` alongside HTML generation. Manual on every call.
- Embeds an HTML wrapper (cards, headers) into the SVG via `foreignObject`. Too fragile across renderers.
