# Cinematic Frontends

<!-- Modified Blitz adaptation of the identified taste-skill and Impeccable guidance. Attribution and MIT/Apache terms: ../NOTICE.md. Notice added 2026-10-11; substantive rules unchanged. -->

Folded in from the cinematic-frontends skill on 11-09-2026; loaded only when the design read selects the cinematic family.

One dark aesthetic family, not a default. `frontend-taste` runs the design read and the pre-flight gate; this file is what it loads when the read lands on cinematic, film grade, near black, or Higgsfield style. Four surfaces share the system: dashboard, data story, HTML slide deck, landing site.

Patched 04-09-2026 against impeccable.style/slop and taste-skill. Eight primitives this skill used to prescribe are now named AI tells. What changed is in section 7.

## 0. Gate

Run `frontend-taste` first. Every rule there applies here: the hero and nav caps, the eyebrow ration, the three locks, the motion motivation test, the copy audit, the pre-flight checklist. This file adds the aesthetic on top. It does not exempt anything.

Do not select this look by reflex. Select it when the owner names it, when the surface is a data story or a quant tool where a dark stage genuinely serves the content, or when the design read says premium dark tech and the audience supports it. A consumer landing page is not automatically cinematic.

## 1. Non-negotiables (the owner's standing rules)

1. Dark canvas at hex `0f0f0f`. Build contrast from light and spacing, never from glow.
2. Charts set `paper_bgcolor` and `plot_bgcolor` to `#0f0f0f` directly in `update_layout`, every chart, regardless of template. `viz-dashboards` owns the rest of the chart contract and its eight point QA pass.
3. Ship one interactive element beside the charts: a slider, toggle or filter that moves a chart live. Never a static picture wall.
4. Probability and forecast output goes in a table with event definitions, horizon and evidence. Only explicitly mutually exclusive and exhaustive scenarios sum to 100%. Independent events are not normalized. A ranking has criteria, evidence, uncertainty and sensitivity, without invented probabilities.
5. Verify every number before it ships. Anchor to a dated source or label it illustrative in the footer. Never present an invented figure as real.
6. Copy follows `house-style`. Answer first, no dashes of any kind, ranges as X to Y, accounting style negatives.
7. Do not surface his employer, its products or its token names unless he raises them first. Generic labels in demos.

## 2. Design system

Load `references/cinematic/cinematic.css` and `references/cinematic/cinematic.js` as the base, then build on top.

Tokens: `--bg:#0f0f0f`, `--ink:#f5f7fa`, `--mut:#9aa0a8`, `--dim:#767c85`, `--acc:#c6ff3a` (one accent, locked for the whole page), `--acc2:#5c78ff` (secondary, structural use only), `--line:rgba(255,255,255,0.09)`, `--card:rgba(255,255,255,0.025)`.

**Type.** Display sizes on `clamp()`, headline tracking `-0.02em`, hierarchy ratio at least 1.25 between levels. Body at 14 to 16px minimum.

Space Grotesk and Inter are the old defaults and both are now on the discouraged list in `frontend-taste` section 7. Pick the pairing from the brief instead. Reasonable dark tech choices: PP Neue Montreal, ABC Diatype, Cabinet Grotesk, Outfit, GT Walsheim, each with a mono companion (Geist Mono, JetBrains Mono, IBM Plex Mono). Reuse Space Grotesk only when the owner asks for continuity with an existing page.

## 3. Motion primitives

All in `cinematic.js`. Each one still needs its one sentence reason under the motivation test.

* **Reveal on scroll.** Class `reveal`, fades and rises via IntersectionObserver. Stagger with `transition-delay`. The workhorse; use it freely.
* **Count-up.** `data-countup="290.8"` with optional `data-prefix`, `data-suffix`, `data-decimals`. Fires when scrolled into view. Reserve it for figures that carry the argument, not every number on the page.
* **Parallax.** `data-parallax="0.12"` translates on scroll. One or two elements per page.
* **Scroll progress bar.** `#prog`, thin, top of page. Justified on a long data story, noise on a landing page.
* **Film grain.** Fixed `#grain` (SVG feTurbulence), `pointer-events-none`, never on a scrolling container. This is the one texture that survived the audit; it reads as film stock rather than decoration.
* **Vignette.** Fixed `#vignette` overlay. Subtle or not at all.
* Honor `prefers-reduced-motion`: kill animation, show everything.

Dark Plotly: use `Cine.layout(extra)` and `Cine.config` from `cinematic.js`. They preset the `#0f0f0f` backgrounds, muted grid at `rgba(255,255,255,0.06)`, dark hover label and hidden modebar.

## 4. Surface recipes

**Dashboard (control room).** Fixed sidebar or a top KPI strip of glass tiles with count-ups, a grid of chart cards, one live control that refilters. Dense but breathable. Density dial 6 to 8.

**Data story (scrollytelling).** Full viewport hero, then bands that reveal on scroll: framing statement, one large count-up stat, animated charts, a parallax pull quote, an interactive projection, the scenario probability table, a closing line. Bands are titled in plain language, never numbered. See `references/cinematic/example-data-story.html`, and read section 7 before copying its surface treatment.

**HTML slide deck**, only when he asks for a dark deck as a web page. A Google Slides or PowerPoint deck, and anything a bank or board sees, belongs to `google-slides`. Full screen sections snapped with `scroll-snap-type: y mandatory`, keyboard arrow navigation, one idea per slide, an action title carrying the claim, optional chart. Same tokens. `pitch-architect` owns the argument spine.

**Landing site.** This is where `frontend-taste` binds hardest. Section reveals and hover lift are fine. Real images are mandatory, the hero caps apply, the eyebrow ration applies, and dual mode applies unless the owner explicitly asks for dark only.

## 5. Build steps

1. Confirm surface, audience and the real data or copy. Gather and verify figures first.
2. Start from `cinematic.css` plus `cinematic.js`. Set the base to `#0f0f0f`.
3. Lay out sections per the recipe. Put content in `.reveal` blocks.
4. Wire charts with `Cine.layout` and `Cine.config`. Lazy init on first reveal so draw animations play.
5. Add exactly one interactive control that updates a chart via `Plotly.react`.
6. Add the appropriate event or scenario table if there is a forecast; the 100% total applies only to explicitly mutually exclusive and exhaustive scenarios.
7. Footer: dated sources for real numbers, an illustrative label for the rest, and a reusable template tag.

## 6. Verify before delivering

Run the `frontend-taste` pre-flight gate in full first. Then:

```bash
grep -n '<script src="http' page.html    # sandbox rule, see section 9
python3 <frontend-taste-path>/scripts/check-html-js.py page.html
```

* Use the actual method directory for `<frontend-taste-path>`. Check every reported external source separately in its declared classic/module mode; data blocks are explicitly skipped. A partial report is not complete verification. The helper parses inline scripts without executing them; browser behavior still needs the checks below.
* Confirm div, table and script tags balance.
* Charts: both background colors are `#0f0f0f`, modebar hidden, hover works.
* Reveals fire, count-ups land on the right value, the interactive control moves a chart.
* Test `prefers-reduced-motion`: content still fully visible.
* Every on screen number is sourced or labeled illustrative. No dashes in copy.

## 7. What was removed, 04-09-2026

These eight were prescribed by earlier versions of this file and are now named tells in `frontend-taste` section 12. They are opt in for a data story where the composition earns them, never a default, and never on a marketing surface.

| Removed | Why | If it is genuinely wanted |
|---|---|---|
| Breathing radial glow blobs | Radial halo and spotlight glow on dark is a top tier tell | One, low opacity, behind a hero only |
| Neon outer glow on cards and accents | Glow as the "premium dark" signal is the corpus default | Inner border `rgba(255,255,255,0.1)` instead |
| Masked animated grid background | Decorative grid lines that organize nothing | Only when the grid maps real axes |
| Numbered section bands `01 / 02` | Section number eyebrows, banned outright | Name the section in plain language |
| Blinking status dot | Pulsing dots on static data, banned outright | Only on a real live feed with real state |
| Headline sheen sweep | Gradient text on headings, reduces scannability | Weight and color for hierarchy |
| Instrument Serif italic accent phrase | Banned outright as an LLM favorite display serif | A justified serif from the rotation pool, or italic of the same sans |
| Space Grotesk as the standing display face | Among the three most common AI tells | Chosen from the brief |

## 8. Reference files

* `references/cinematic/cinematic.css` tokens, overlays, primitives, keyframes.
* `references/cinematic/cinematic.js` motion engine and dark Plotly helpers (`window.Cine`).
* `references/cinematic/example-data-story.html` full worked scrollytelling page (the stablecoin story).

The example loads its Plotly library externally from `cdn.plot.ly`, with a second CDN version as the fallback; inline the library before reusing the page or any of its chart code.

The JS still ships the blink, grid and glow helpers and the CSS still ships their keyframes. They stay as opt in. This file overrides the defaults; do not call them unless the design read selected them and the reason fits in one sentence. The example page predates this patch: audited 04-09-2026 it carries 10 uppercase eyebrow labels, 6 radial gradients, 8 gradient text clips, Instrument Serif, Space Grotesk, an external Plotly script tag and one `addEventListener("scroll")`. Read it for structure, not for surface treatment, and do not copy it wholesale.

## 9. Gotchas (learned 19-07-2026)

* **Sandbox script loading.** Artifacts and sandboxed viewers block CDN loads and fail silently, which ships a blank page. Inline the library, or precompute coordinates and emit inline SVG.
* **Gate chart init on Plotly being ready** (poll for `window.Plotly`, then draw), and render a small fallback message if it never loads, so a chart never blanks silently.
* **Verify by rendering, not only by `node --check`.** A dead script tag still passes a syntax check but shows nothing. Load the page in a browser, or a jsdom stub with Plotly mocked, and confirm each chart calls `Plotly.newPlot`.
