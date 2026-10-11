# Core SVG primitives

The universal building blocks, written in the **light skin**. Copy them literally, then
convert to dark with `scripts/skin.py` if the target is a dark surface. Type-specialised
primitives (lifeline, activation bar, region, lane) live in the relevant `type-*.md`.

The connector rules C1 to C5 in SKILL.md govern everything below. These are the shapes;
the rules are the law.

---

## Background

Default is a single flat `paper` rect. No pattern, no secondary container.

```svg
<rect width="100%" height="100%" fill="#f5f5f5"/>
```

Opt-in dotted paper, for a long-form editorial hero figure only. Never inside a card,
slide or product page, where the texture compounds with surrounding chrome.

```svg
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="0.9" fill="rgba(45,49,66,0.10)"/>
  </pattern>
</defs>
<rect width="100%" height="100%" fill="#f5f5f5"/>
<rect width="100%" height="100%" fill="url(#dots)" opacity="0.6"/>
```

## Arrow markers

Define only the markers the figure actually uses. An unused `<defs>` entry is an element
that was not earned.

```svg
<marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polygon points="0 0, 8 3, 0 6" fill="#4f5d75"/>
</marker>
<marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polygon points="0 0, 8 3, 0 6" fill="#eb6c36"/>
</marker>
<marker id="arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polygon points="0 0, 8 3, 0 6" fill="#2e5aa8"/>
</marker>
```

| Arrow | Stroke | When |
|---|---|---|
| Default | `muted` `#4f5d75` | Internal, generic |
| Accent | `#eb6c36` | The one primary flow |
| Link | `#2e5aa8` | HTTP and API calls, external systems |
| Dashed | `stroke-dasharray="4,3"` on any colour | Optional, passive, return, async |

Draw every arrow before every box so z-order puts lines behind nodes.

## Node box

Five layers, in this order. The first rect is an opaque mask that stops arrows bleeding
through a transparent fill.

```svg
<rect x="X" y="Y" width="W" height="H" rx="6" fill="#f5f5f5"/>
<rect x="X" y="Y" width="W" height="H" rx="6" fill="FILL" stroke="STROKE" stroke-width="1"/>
<rect x="X+8" y="Y+8" width="32" height="12" rx="2" fill="transparent"
      stroke="STROKE@0.40" stroke-width="0.8"/>
<text x="X+24" y="Y+17" fill="STROKE@0.8" font-size="7" font-family="'Geist Mono', monospace"
      text-anchor="middle" letter-spacing="0.08em">API</text>
<text x="CX" y="CY+2" fill="#2d3142" font-size="12" font-weight="600"
      font-family="'Geist', sans-serif" text-anchor="middle">Node Name</text>
<text x="CX" y="CY+18" fill="#4f5d75" font-size="9"
      font-family="'Geist Mono', monospace" text-anchor="middle">tech:port</text>
```

The type tag is a rectangle at `rx=2`, not a pill. Fill and stroke per the node-type
table in [style-guide.md](style-guide.md).

Every offset above is a multiple of 4 so that an on-grid box produces on-grid children.
If you change a tag width or an inset, keep it divisible by 4 or the whole node fails the
grid check. Text baselines are the exception and are meant to be off-grid.

## Arrow label

Every label gets an opaque mask, and the mask clears the stroke by 6 to 10px. That gap
is rule C2 and it is the single most commonly broken rule in generated diagrams.

```svg
<!-- stroke sits at ARROW_Y; mask spans ARROW_Y-20 to ARROW_Y-8, so the gap is 8px -->
<rect x="MID_X-20" y="ARROW_Y-20" width="40" height="12" rx="2" fill="#f5f5f5"/>
<text x="MID_X" y="ARROW_Y-11" fill="#7a8399" font-size="8"
      font-family="'Geist Mono', monospace" text-anchor="middle" letter-spacing="0.06em">WRITE</text>
```

- 14 characters or fewer, all caps, centred on the segment midpoint.
- On a vertical segment the label goes beside the line with the same 6 to 10px gap.
- When two lanes run close together, check the gap to the **nearest** line, not just to
  the label's own line. A label 8px from its own stroke and 10px from a neighbouring one
  is ambiguous. Give it 12px of clearance from any line it does not belong to.
- Never `writing-mode` vertical text.

## Elbow and hop

Rule C1 requires a rounded right-angle elbow between any two off-axis nodes. One bend:

```svg
<!-- from (x1,y1) rightwards, then down into (x2,y2). r=8, or r=6 in a tight lane. -->
<path d="M x1,y1 H x2-8 Q x2,y1 x2,y1+8 V y2" fill="none" stroke="#4f5d75"
      stroke-width="1.2" marker-end="url(#arrow)"/>
```

Two bends, when the run has to step around something:

```svg
<path d="M x1,y1 V ym-8 Q x1,ym x1+8,ym H x2-8 Q x2,ym x2,ym+8 V y2"
      fill="none" stroke="#4f5d75" stroke-width="1.2" marker-end="url(#arrow)"/>
```

Put every on-path anchor on the 4px grid. Quarter-arc control points are exempt because
they are a function of the radius.

Rule C3 allows one genuine crossing shape, the bridge or hop. The line being crossed
stays straight; the crossing line arcs over it:

```svg
<!-- horizontal run hopping a vertical stroke at x=CX -->
<path d="M x1,y H CX-8 a 8,8 0 0,1 16,0 H x2" fill="none" stroke="#4f5d75"
      stroke-width="1.2" marker-end="url(#arrow)"/>
```

One hop per crossing, always on the same line of the pair, and never two hops within
24px of each other. If a figure needs more than two hops, the layout is wrong.

## Legend

A horizontal strip below the figure, after a hairline. Never floating inside the diagram
area. Grow the `viewBox` height by roughly 60px to hold it.

```svg
<line x1="32" y1="LEGEND_Y-8" x2="VIEWBOX_W-32" y2="LEGEND_Y-8"
      stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>
<text x="32" y="LEGEND_Y+8" fill="#4f5d75" font-size="8" font-family="'Geist Mono', monospace"
      letter-spacing="0.18em">LEGEND</text>
<!-- items in a horizontal row, roughly 160px apart -->
```

The legend covers every treatment used in the figure and nothing else. A legend entry
for a node type that does not appear is noise.

## Summary cards

For the `template-full.html` editorial variant only. Never three identical cards.

```html
<div class="card">
  <p class="eyebrow">SECTION LABEL</p>
  <div class="card-header">
    <span class="card-dot accent"></span>
    <h3>Card Title</h3>
  </div>
  <ul><li>Item</li></ul>
</div>
```

- Background `#ffffff` (a lift off paper, not paper itself), `1px` border at
  `rgba(45,49,66,0.12)`, `border-radius: 6px`, `padding: 1.25rem`.
- No `box-shadow`, ever.
- Card dots are 7px circles in the ink, muted, accent, link or soft roles.
- Vary the column widths, for example `1.1fr 1fr 0.9fr`. Three equal columns read as a
  default grid nobody chose.
