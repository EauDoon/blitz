# Style Guide

Single source of truth for colour, typography and spacing. Two skins ship: **light** is
the default for a standalone diagram, **dark** is the `#0f0f0f` skin that matches
`cinematic-frontends`, `pitch-architect` and `viz-dashboards` surfaces.

**Read this before the first line of SVG.**

---

## How skinning actually works

Be clear about a thing the upstream project got wrong: the SVG snippets in this skill
and in every `type-*.md` carry **literal hex values**, not token names. Editing the
tables below does not re-skin anything on its own.

So the workflow is one-directional and mechanical:

1. **Always build in the light skin.** Every snippet, every example, every coordinate in
   this skill is written light. Copy them as-is.
2. **Convert to dark with the script**, never by hand:
   `python3 scripts/skin.py dark diagram.html -o diagram-dark.html`
3. **Verify the conversion**: `python3 scripts/skin.py check diagram-dark.html`
   It exits non-zero and names any light token left behind.

Hand-editing hex is how the two skins drift. If a colour is missing from the map, the
script warns and leaves it untouched; add it to `HEX_MAP` rather than patching output.

---

## Tokens

| Role | Purpose | Light | Dark |
|---|---|---|---|
| `paper` | Page background, node mask fill | `#f5f5f5` | `#0f0f0f` |
| `paper-2` | Container and zone fill | `#ececec` | `#1a1a1a` |
| `panel` | Backend node fill (a lift off paper) | `#ffffff` | `#171717` |
| `ink` | Primary text, primary stroke | `#2d3142` | `#f5f7fa` |
| `muted` | Secondary text, default arrows | `#4f5d75` | `#9aa0a8` |
| `soft` | Sublabels, boundary labels | `#7a8399` | `#767c85` |
| `rule` | Hairline borders | `rgba(45,49,66,0.12)` | `rgba(245,247,250,0.12)` |
| `rule-solid` | Stronger borders, baselines | `#bfc0c0` | `#2a2a2a` |
| `accent` | Focal, 1 to 2 elements per diagram | `#eb6c36` | `#c6ff3a` |
| `accent-tint` | Fill behind an accent border | `rgba(235,108,54,0.08)` | `rgba(198,255,58,0.08)` |
| `link` | HTTP and API calls, external arrows | `#2e5aa8` | `#5c78ff` |
| `invert` | An inverted emphasis block, a hub or a shared-state slab | `#2d3142` | `#171717` |
| `invert-text` | Text sitting on an inverted block | `#f5f5f5` | `#f5f7fa` |

The dark column is not a free choice. It is lifted from the owner's `cinematic-frontends`
token set so a diagram dropped into a dashboard, deck or data story matches the surface
it lands on. Do not invent a third dark.

`invert` is the one role whose dark value is not the generic swap of its light value.
An inverted block is a contrast device: ink slab, paper text. Swapped token by token it
becomes a near-white slab on a near-black canvas that outshouts the accent. Declare it as
a CSS custom property named `--invert` and `--invert-text`, never as a raw `var(--ink)`
fill, and `scripts/skin.py` will force the right dark value.

**Opacity washes** invert by base triple, opacity unchanged:
`rgba(45,49,66,X)` becomes `rgba(245,247,250,X)`, `rgba(235,108,54,X)` becomes
`rgba(198,255,58,X)`. The script handles this.

### Series palette

For the four types that genuinely need to separate overlapping entities: `process`,
`data-flow`, `it-state`, `medallion`. The one-focal rule still holds, `accent` stays
reserved for the focal element and these cover the rest.

| Token | Light | Dark |
|---|---|---|
| `series-1` sage | `#7c8f6f` | `#9caf8f` |
| `series-2` dusty blue | `#5e7a9b` | `#82a0c0` |
| `series-3` mustard | `#b8915a` | `#d3ad7a` |
| `series-4` rust brown | `#9c6b50` | `#b88670` |
| `series-5` slate | `#6e6479` | `#8d8298` |

Fills at 0.18 opacity light, 0.22 dark. Strokes at full colour. Do not backfill these
into architecture, flowchart, swimlane or any other type.

### Terminal skin

A fixed third skin for the CLI-window primitive only, see
[primitive-terminal.md](primitive-terminal.md). It is not light and not dark, it is its
own register, and `skin.py` deliberately leaves it alone.

| Token | Hex |
|---|---|
| `terminal-page` | `#0a0a0a` |
| `terminal-paper` | `#141414` |
| `terminal-bar` | `#1b1b1b` |
| `terminal-border` | `#2b2b2b` |
| `terminal-ink` | `#f5f5f5` |
| `terminal-muted` | `#9a9a9a` |
| `terminal-soft` | `#5c5c5c` |
| `terminal-accent` | `#ff5a36` |

---

## Typography

| Role | Family | Size | Weight | Usage |
|---|---|---|---|---|
| `title` | Instrument Serif | 1.75rem | 400 | Page H1 |
| `node-name` | Geist sans | 12px | 600 | Human-readable labels |
| `sublabel` | Geist Mono | 9px | 400 | Port, protocol, URL, field type |
| `eyebrow` | Geist Mono | 7 to 8px | 500, tracked 0.18em, uppercase | Type tags, axis labels |
| `arrow-label` | Geist Mono | 8px | 400, tracked 0.06em | Arrow annotations |
| `callout` | Instrument Serif italic | 14px | 400 | Editorial asides only |

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

Typography is deliberately identical across light and dark. Colour is what makes an
embedded diagram look foreign, not type.

**Mono is for technical content only**: ports, commands, URLs, field types. Names go in
Geist sans. The page title is Instrument Serif. Italic Instrument Serif is reserved for
annotation callouts. Never JetBrains Mono as a blanket developer font.

**Fonts load from Google Fonts over the network.** That works in a published Artifact,
where Google Fonts stylesheets are allowed. A standalone file opened offline, or rendered
from a shell that cannot reach Google Fonts, falls back to the system stack the templates
carry (`'Instrument Serif', Georgia, 'Times New Roman', serif` for the title), which is
legible but off-brand. If the exact faces must survive offline, say so and inline the three
families as base64 in the `<style>` block.

---

## Stroke, radius, spacing

| Token | Value | Use |
|---|---|---|
| `stroke-thin` | 0.8 | Tag outlines, leaf nodes |
| `stroke-default` | 1 | Most strokes |
| `stroke-strong` | 1.2 | Emphasis strokes |
| `radius-sm` | 4 | Small tags |
| `radius-md` | 6 | Node boxes |
| `radius-lg` | 8 | Containers, rings |
| `grid` | 4 | Every coordinate, size and gap divides by 4 |

### The grid rule and its exemptions

Every **x, y, width, height and gap** divides by 4. That is the rule. Four things are
exempt, and these four are the whole list:

1. **Type sizes 7, 9 and 14**, because the `eyebrow`, `sublabel` and `callout` roles
   above require them. Every other font size divides by 4: 8, 12, 16, 20, 24, 28, 32, 40.
2. **Corner radii on a rect**, which come from the radius token set above: 2 for a type
   tag or label mask, 4, 6 or 8 for boxes and containers. A radius is chosen from that
   set, not from the grid. This applies to `rx` on a `rect` only. The `r` of a `circle`
   or an `ellipse` is a dimension, not a corner, so it obeys the grid: a decorative dot
   is `r=4`, never `r=2`, `r=3` or `r=6`.
3. **Stroke widths and opacities**, and the 22 by 22 dot pattern.
4. **Text baselines**, which are derived from the element they sit in rather than placed
   on the grid. A label baseline is `mask_top + 9` for 8px type; a node name is `CY + 2`
   and its sublabel `CY + 18`. The box they hang off is on-grid, so the baseline usually
   is not, and that is correct.

Upstream stated the grid rule and the 7px and 9px type sizes as two hard rules that
contradict each other, forcing a silent violation on every diagram. Exemptions 2 and 4
close the same trap for radii and baselines. Nothing outside this list escapes the grid,
and `scripts/lint-diagram.py` enforces exactly this reading.

---

## Node type to treatment

| Type | Fill | Stroke |
|---|---|---|
| `focal`, 1 to 2 max | `accent-tint` | `accent` |
| `backend` | `panel` | `ink` |
| `store` | `ink @ 0.05` | `muted` |
| `external` | `ink @ 0.03` | `ink @ 0.30` |
| `input` | `muted @ 0.10` | `soft` |
| `optional` | `ink @ 0.02` | `ink @ 0.20`, dashed `4,3` |
| `security` | `accent @ 0.05` | `accent @ 0.50`, dashed `4,4` |

---

## Re-skinning to a different brand

Both skins above are the house default. To map a third brand, see
[onboarding.md](onboarding.md), then add the new skin as a second map in
`scripts/skin.py` rather than editing hex by hand.

### Constraints that survive any re-skin

- **Contrast**: `ink` hits WCAG AA on `paper` at every size. `muted` hits AA on `paper`
  at 11px and up, which the 12px `node-name` role clears. The 9px `sublabel` and 7 to
  8px `eyebrow` roles sit below that threshold by design: they carry secondary technical
  detail, not the content of the figure. Never put a load-bearing label at 9px in
  `muted`, and if a diagram has to meet AA at every size, raise those two roles to 12px
  and widen the boxes to fit.
- **One accent.** Two accents erase the focal signal. If a brand ships eight colours,
  three of them become `paper`, `ink` and `accent`, the rest become `muted` variants.
- **Paper is a low-chroma neutral**, light or near-black. Not a saturated brand colour,
  and not a gradient. The default light paper `#f5f5f5` is a neutral grey by design.
- **Three families, no more**: a serif for the title, a sans for names, a mono for
  technical content. If brand typography is all sans, keep the serif title anyway, the
  contrast is load-bearing.
- **The dot pattern is opt-in**, not the default. Default background is a flat `paper`
  fill. When enabled it sits at roughly 10% `ink` on `paper`.
- **The container is clean by default.** The diagram sits directly on the page, no
  secondary background and no border. The framed variant is opt-in for card-heavy
  layouts.
