---
name: "frontend-scroll-craft"
description: 'New websites and landing pages as scroll experiences. Use on build me a site, a frontend for, new landing page, cinematic, immersive, scrollytelling, Apple-style. Look: frontend-taste; data stories: viz-dashboards.'
---

# Frontend Scroll Craft

The build lane for a new website or landing page where scroll is the experience: the wheel is a scrubber, the page is a film with real text on top, and each section behaves differently enough that the visitor keeps going. It is a fork of nateherkai/scroll-craft with the engine, scripts and references intact (provenance in `CHANGES.md`). It is not the design gate: `frontend-taste` runs the design read before this skill writes markup and the pre-flight after, owns app UI, components, redesigns and the review of any existing page, and on a new page the two stack, this one building and that one gating. `viz-dashboards` owns any chart on the page and every dashboard or data story, cinematic or not. `frontend-mockup` owns concept screens rendered to PNG; `website-cloner` owns copies of an existing site. `house-style` owns every visible string.

## What you produce

`BRIEF.md`, a page grammar, a journey, a feeling curve with one engineered peak, a score table, one signature move, assets (supplied or generated), one real HTML page on the token floor, a strip of screenshots proving it holds at every scroll position, and a short report.

## The spine

Four rules. Everything else in the references serves them.

1. **Variety is the product.** At least four device families per page and never the same device twice in a row. [references/devices.md](references/devices.md).
2. **The world is photographic unless the brand itself is illustrated.** Clay diorama and low-poly are banned as defaults. [references/worlds.md](references/worlds.md).
3. **No continuous chain unless the brief says one continuous journey.** Vary the device and the cut disappears for free. Worldflight is the one sanctioned exception: [references/worldflight.md](references/worldflight.md).
4. **A different world is not a different page.** Structure is its own axis. Pick a grammar, invent a signature move, pass the fingerprint gate. [references/uniqueness.md](references/uniqueness.md).

## Step 0: The brief

Full interview in [references/brief.md](references/brief.md). Short form: eight questions in one pass (vibe and three non-site references; the scroll journey in their words; the energy curve; the feeling stage by stage and the ONE moment; one thing no site does; how far from premium-minimal; one unbroken world or distinct scenes; what assets exist), then the four that cannot be defaulted (what it is and for whom; the one belief; the one action and its single label; art direction from worlds.md). Write `BRIEF.md` in their words with the feeling curve, the peak as a sentence a visitor would say, the tell-someone sentence, and any authored silence. [references/feel.md](references/feel.md) is the spec.

Explicit delegation ("use your judgment") is a normal route: write a `Self-authored under explicit creative delegation` brief and proceed without a second interview. Unattended with no delegation: self-author, mark it `Self-authored, not interviewed`, and say so in the report.

Then the journey: four to seven beats, each a shift in what the visitor knows or feels. Sections serve beats; a section that serves no beat is cut.

## Step 1: Bootstrap

Environment, done once after the interview.

```bash
node <skill>/scripts/doctor.mjs                 # node, full ffmpeg, playwright, Chrome, key, workspace
node <skill>/scripts/workspace.mjs --ensure     # resolves the workspace, seeds FINGERPRINTS.md
```

Workspace resolution, first hit wins: `SCROLLCRAFT_HOME`, the nearest `.scrollcraft.json` (`{ "workspace": "..." }`), then `<git root>/scrollcraft`. Builds live in `<workspace>/builds/<name>/`; the registry starts empty on purpose.

Copy `engine/scrollcraft.js` and `engine/scrollcraft.css` into the build folder. **Never edit the engine per project.** Theme it with six colour tokens and two fonts; write your own markup; drive anything bespoke off the `--sc-p` custom property.

**Spend gate.** Building from supplied photos and footage costs nothing and is a first-class route. Generation through kie.ai bills per call, so before the first `kie.mjs still` or `shot`, list the planned calls with their credit sum at the documented rates (active context below) and wait for a go. An unattended run never generates.

## Step 2: Grammar, gate, then score

Detail in [references/uniqueness.md](references/uniqueness.md) and [references/feel.md](references/feel.md).

1. **Pick a grammar** from the eight (filmic one-shot, chaptered editorial, live surface, continuous world, typographic poster, gallery, split stage, rhythmic cutlist). Nav, hero and close follow from it. Filmic one-shot carries a burden of proof: choosing it means saying why the other seven lost.
2. **Invent the signature move.** One bespoke interaction coded in the page. A parameter change to a kit device is not one.
3. **Run the fingerprint gate.** The plan must differ from every row in `<workspace>/FINGERPRINTS.md` on at least 4 of 6 dimensions (grammar, nav, hero device, act-sequence shape, close, signature move). Fail: change the plan, never the log.
4. **Write the feeling curve before the score.** One line per act, emotion then cause. Two adjacent acts with the same feeling means one is filler. Name the peak and give it the largest span.
5. **Score each beat to a device** in a table (beat, device, why). Then check: the grammar's bans hold; four or more device families; no family twice in a row; at most two `scrub` acts; one peak with the largest span and a quieter act before it; every act earns its span (8 to 14 viewport-heights is a pacing reference for long cinematic pages, not a quota; never add filler to hit a length).

## Step 3: Assets

Pipeline, prompt scaffolds and encoding in [references/assets.md](references/assets.md). Hero layering in [references/hero-depth.md](references/hero-depth.md): a layered hero is the default when the brief asks for a premium marketing hero, cinematic, immersive or depth, and the grammar allows a media hero; it is not a law.

```bash
node <skill>/scripts/kie.mjs still "<style preamble>\n\n<scene>" out/01-hero.png --ar 16:9 [--ref brand.png]
node <skill>/scripts/kie.mjs shot  "<camera move>" out/01-hero.png out/01.mp4 --dur 5
bash  <skill>/scripts/encode.sh out/01.mp4 assets/01.mp4
bash  <skill>/scripts/encode.sh out/01.mp4 assets/01-m.mp4 mobile
```

Four things decide premium versus generated: one style preamble reused verbatim in every prompt; look at every asset before using it; encode for scrubbing (dense GOP), not playback; layer the hero into planes that move at different rates. Every clip's poster is its own first frame, pulled with ffmpeg.

## Step 4: Build the page

Write real HTML: real `<h1>`, real `<p>`, real links, real reading order. The engine reads `data-sc-*` attributes and never generates DOM. Start from [references/template.html](references/template.html) and rearrange it to your score; a page that keeps the template's structure verbatim is the failure this skill exists to avoid. Read [references/taste.md](references/taste.md) before writing markup, then run `frontend-taste`'s design read on the brief: its canvas rule decides light or dark for a marketing surface, and its hero, nav, eyebrow and copy caps all apply here.

Theme by overriding tokens:

```css
:root {
  --sc-canvas: #0A0806;  --sc-surface: #16110E;
  --sc-ink:    #F5EBDD;  --sc-ink-soft: #A2968A;
  --sc-accent: #FF5A3D;  --sc-accent-ink: #15110F;
  --sc-font-display: "Archivo", system-ui, sans-serif;
  --sc-font-text:    "Geist", system-ui, sans-serif;
}
```

## Step 5: Verify by scrolling it

Not optional. A scroll page has no single state; the failures live between the two positions you looked at. Full procedure in [references/verify.md](references/verify.md); the delivery gate is [approved-collection.md §7](references/approved-collection.md).

```bash
cd <build project> && npm i playwright-core     # once, in the build folder
node <skill>/scripts/serve.mjs --root . --port 4500 &
node <skill>/scripts/shoot.mjs --url http://localhost:4500 --out lab/shots
node <skill>/scripts/shoot.mjs --url http://localhost:4500 --out lab/mobile --width 390 --height 844
node <skill>/scripts/shoot.mjs --url http://localhost:4500 --out lab/reduced --reduced-motion
```

The harness samples every act at six positions, waits for the playhead to arrive, and reports dead scroll, frozen clips, cues that never peak, and contrast measured on the composited frame at the worst position under each line. It writes a contact sheet. Then do what it cannot: read `sheet.png` for composition and motion, tab through for focus order, and run the feel check ([feel.md §6](references/feel.md)): scroll cold, one word per act, then diff against `BRIEF.md`. Where they disagree the page is wrong, not the brief.

A worldflight page also runs `node <skill>/scripts/worldflight-assert.mjs --url <url>`, the mechanical checks that mode makes ([worldflight.md §9](references/worldflight.md)).

A green run does not cover a real phone. Headless Chrome cannot reproduce an iPhone decoder, autoplay policy or Low Power Mode. On the first mobile defect report, deploy [references/device-diag.html](references/device-diag.html) beside the site and let the device answer. Report what was verified and what was not.

## Hard rules

Ship-blockers. Each one makes a page read as machine-made.

| Never | Instead |
|---|---|
| Clay diorama, low-poly or claymation as the default world | Photographic. worlds.md |
| A scroll cue, arrow or animated mouse icon | Nothing. They are looking at the hero |
| `01 / 06` section counters | Delete them |
| An eyebrow above every heading | At most one per three sections |
| Em dash or en dash anywhere visible | Period, comma, colon, parentheses, "to" |
| Centred copy in every act | Vary the anchor: lead, trail, centre, split |
| The same device twice in a row | Score the journey properly |
| Generating before the brief and creative authority are clear | Step 0, recorded in `BRIEF.md` |
| Generating before the spend gate | List the calls and the credit sum, get the go |
| No engineered peak, or three competing ones | One peak: the asset budget, the silence before it, the most scroll room |
| An ending that fades out or just becomes a footer | The close resolves and holds |
| Planning acts before the feeling curve exists | Curve first, devices second |
| Shipping without a bespoke signature move | Invent one. A recoloured spotlight is not one |
| Fewer than 4 of 6 fingerprint dimensions cleared against any row | Change the plan, not `FINGERPRINTS.md` |
| Editing the engine for a bespoke behaviour | Bespoke JS in the page off `--sc-p` and your own `data-sc-*` |
| Filmic one-shot because it is what the last build did | Pick from all eight and say why the other seven lost |
| A full-frame dark overlay to fix contrast | A scrim only where the text sits, as a sibling of the copy |
| Text baked into a generated image | Real markup, always |
| Invented statistics in a counter | Real numbers or no counter |
| `transition: all`, or animating width, height, top, left | `transform` and `opacity`; `clip-path` for wipes |
| Gradient text, neon glow, zero-offset halo shadows | Weight and size for emphasis; shadows with offset and blur |
| Any audio on a scrub clip | Strip the track; `encode.sh` already does |
| A CDN script or an external image in a page delivered as an artifact | Inline the engine and the images |
| Shipping without Step 5 | Run Step 5 |

## Output

The build folder including `BRIEF.md`, then a short report: the grammar and why the other seven lost, the signature move, the fingerprint gate result against each row, the journey, the feeling curve and the peak, the feel-check diff, the score table, what was generated and what it cost at the documented rates (a planning ceiling, not a measured spend), what was verified with screenshots, what was not, and whether the brief was interviewed or self-authored. Give the local URL or the artifact. Then append the build's row to `<workspace>/FINGERPRINTS.md`. Before anything external-facing ships, hand it to `cold-read`.

## Host and project prerequisites

Bundled engine and scripts originate from upstream revision `0b816225945e45380397d6a0487efa3c98916858` (v0.3.0); see `LICENSE`. Verify Node, ffmpeg, browser and codec support locally before execution. Asset generation is optional and requires explicit cost and upload authority; keep `KIE_AI_API_KEY` unset otherwise. `kie.mjs` does not provide its own spending guard and can read a `.env` from parent directories. Do not treat historical model names, rates, or host observations as current. Preserve reduced-motion behavior and test current outputs. Source or package availability does not prove execution.

Pairs with `frontend-taste` for the design read before markup and the gate after, `house-style` for every visible string, `viz-dashboards` when a chart lives on the page, `gauntlet-verify` when a named bar is set on the build, and `cold-read` before anything external-facing ships.
