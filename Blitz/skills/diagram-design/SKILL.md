---
name: diagram-design
description: 'Editorial diagrams as HTML with inline SVG: architecture, flow, sequence, swimlane, timeline, org chart, quadrant. Use on draw this, diagram this, map this out, what does the flow look like. Numbers: viz-dashboards.'
---

# Diagram Design

Structural figures as self-contained HTML with inline SVG, on one editorial design
system with a complexity budget and a taste gate. It draws how things relate, not how
much of them there is: `viz-dashboards` owns every chart, series and dashboard and the
hex 0f0f0f standard they follow, `frontend-taste` and its cinematic reference own the surface a diagram gets
embedded into, and `google-slides` owns the deck the figure lands in. This one owns
the figure. Twenty-two types, each with layout conventions in `references/type-*.md`,
loaded only once a type is chosen.

Forked from cathrynlavery/diagram-design v2.0 (MIT), patched 10-08-2026. What changed is
listed in `CHANGES.md`.

## 0. Skin gate

Two skins ship and the choice is made before drawing, not after.

| Where the diagram lands | Skin | How |
|---|---|---|
| Anywhere not listed below, including a website, doc, blog post, social card, or a deck in the light reading register | **Light**, the default | Build and stop |
| A dashboard, data story, a deck in a dark presented preset, or any hex 0f0f0f surface | **Dark** | Build light, then convert |

Never hand-write dark hex. Build light every time, then run:

```
python3 scripts/skin.py dark diagram.html -o diagram-dark.html
python3 scripts/skin.py check diagram-dark.html
```

`check` must exit clean before delivery. If the owner has not said where the diagram is
going and the conversation is already about a deck or a dashboard, produce both and say
which is which. Do not ask a question you can answer from context.

## 1. Philosophy

**The highest quality move is usually deletion.** Confident restraint, earn every
element, one accent, a small spacing vocabulary. If removing it would not hurt the
figure, remove it.

- Every node is a distinct idea. Two nodes that always travel together are one node.
- Every connection carries information. If the relationship is obvious from layout,
  remove the line.
- The accent is editorial, not a flag. One to two focal nodes. On five nodes it stops
  meaning anything.
- The figure is done when nothing can be removed, not when everything has been added.

Target density 4/10. Complete enough to be technically true, sparse enough to need no
guide. Past nine nodes it is probably two diagrams.

## 2. When not to draw

Before anything else: **would the reader learn more from this than from a well written
paragraph?** If no, write the paragraph.

| Instead of a diagram | Use |
|---|---|
| A list of things | A table or bullets |
| A simple before and after | A two-column table |
| Anything with a measured quantity, a series or a trend | `viz-dashboards` |
| A one-shape "diagram" | One sentence |
| A quick throwaway sketch in chat | Unicode or plain text |

## 3. Type selection

Load the matching `references/type-*.md` before drawing. It carries the layout
conventions, the type-specific anti-patterns and the worked example for that type.

| Showing | Type |
|---|---|
| Components and connections in a system | [architecture](references/type-architecture.md) |
| A legacy IT landscape grouped by phase or department, the before state | [it-state](references/type-it-state.md) |
| Decision logic with branches | [flowchart](references/type-flowchart.md) |
| Time-ordered messages between actors | [sequence](references/type-sequence.md) |
| States, transitions and guards | [state](references/type-state.md) |
| Entities, fields and relationships | [er](references/type-er.md) |
| Events positioned in time | [timeline](references/type-timeline.md) |
| A cross-functional process with handoffs | [swimlane](references/type-swimlane.md) |
| Two-axis positioning or prioritisation | [quadrant](references/type-quadrant.md) |
| A reinforcing cycle where the last step feeds the first | [loop](references/type-loop.md) |
| Hierarchy through containment or scope | [nested](references/type-nested.md) |
| Parent to children relationships | [tree](references/type-tree.md) |
| Ownership, reporting, routing, escalation | [org-chart](references/type-org-chart.md) |
| Stacked abstraction levels | [layers](references/type-layers.md) |
| Overlap between sets | [venn](references/type-venn.md) |
| Ranked hierarchy or conversion drop-off | [pyramid](references/type-pyramid.md) |
| An end-to-end stack on a container cluster | [high-level](references/type-high-level.md) |
| A multi-actor sequential process with data handoffs | [process](references/type-process.md) |
| Multi-tier storage with quality levels and access policy | [medallion](references/type-medallion.md) |
| A data pipeline with typed payloads, who touches each one | [data-flow](references/type-data-flow.md) |
| Integration topology, sources to core to consumers | [dp-integration](references/type-dp-integration.md) |
| Per-role access permissions | [dp-security-matrix](references/type-dp-security-matrix.md) |

Three types overlap on "who touches what" and the split is by grammar, not topic.
`data-flow` needs typed payloads moving through pipeline steps. `swimlane` needs one
process with handoffs between lanes. Everything else with an ownership boundary is
`architecture` with a zone rect. Pick before loading a type reference; loading the wrong
one costs 5k tokens.

Rules of thumb: if a three-column table says the same thing, use the table. If two types
both fit, pick the dominant axis rather than hybridising two grammars. If the content
exceeds the budget in §6, split into an overview plus a detail figure.

Bar, line, scatter, radar and Gantt were removed from this fork. They are quantitative
and belong to `viz-dashboards`, which renders them dark and interactive.

## 4. Anti-patterns

These mark a generated-looking figure of any type. Type-specific ones live in each
`type-*.md`.

| Anti-pattern | Why it fails |
|---|---|
| Dark background with cyan or purple glow | Reads technical without a single design decision |
| Mono as a blanket developer font | Mono is for ports, commands, URLs. Names go in sans |
| Identical boxes for every node | Erases hierarchy |
| A legend floating inside the diagram area | Collides with nodes |
| Three equal-width summary cards | Generic grid, vary the widths |
| A shadow on anything | Shadows are out, borders are in |
| Radius above 10px on a box | Max 6 to 10, or none |
| The accent on every important node | It is one to two editorial accents, not a signalling system |
| An arrow label with no mask rect | Bleeds through the line |
| Vertical `writing-mode` text | Unreadable |

## 5. Connector rules C1 to C5

Non-negotiable, and stated once. The checklist in §8 refers to them by number.

**C1. Orthogonal only.** Rounded right-angle elbows, quarter-arc bends at `r=8`, or
`r=6` in a tight layout. A plain straight `<line>` is legal only when both endpoints
share an x or a y. A diagonal connector between off-axis nodes is an automatic fail. The
elbow path formula is in [primitives-core.md](references/primitives-core.md).

**C2. Label clears the line by 6 to 10px.** Every arrow label needs an opaque `paper`
mask rect behind it, and a visible gap between the bottom of that mask and the stroke.
The mask stops the arrow bleeding through the glyphs, the gap keeps the connector
traceable. A mask touching or crossing its own stroke is a hard fail. On a vertical
segment the same gap goes to the side. Never `writing-mode`.

**C3. No two connectors share a path.** No overlap, no stacked parallels, no shared
segment. Genuine crossings use the bridge or hop primitive in
[primitives-core.md](references/primitives-core.md). Two arrows that want to run
together get offset by 12px or more along their whole length. If connectors keep
stacking, the layout is wrong or the figure is over budget.

**C4. Fan the attach points.** Two connectors never meet a box at the same point. Spread
them along the edge, 12px apart or more, 8px minimum on a small box, snapped to the 4px
grid. Even spacing by eye beats an exact formula that lands off-grid. Route each one
orthogonally from its own point, no merging strokes near the box.

**C5. Never route behind a third box.** Reroute around any box that is not the source or
the destination. One exception: a cross-cutting element such as a footer service bar
that physically sits on the only direct path. In that case the stroke is dashed to read
as transit rather than interaction, the label sits at the visible end near the source,
and no arrowhead lands on the intervening box. When in doubt, reroute.

**Draw all arrows before all boxes** so z-order puts lines behind nodes.

### Primitives

The shapes these rules govern (background, markers, node box, arrow label, legend,
summary cards) are in [primitives-core.md](references/primitives-core.md). Load it when
you start drawing, not while choosing a type.

Optional primitives: [annotation callouts](references/primitive-annotation.md),
[hand-drawn](references/primitive-sketchy.md),
[icons](references/primitive-icons.md) with the gallery at `assets/icons.html`, and the
[terminal window](references/primitive-terminal.md).

## 6. Layout and budget

All colour, type and spacing tokens live in
[style-guide.md](references/style-guide.md). Read it before the first line of SVG. The
grid rule and its four exemptions are stated there and nowhere else.

| Limit | Max |
|---|---|
| Nodes | 9 |
| Arrows or transitions | 12 |
| Accent elements | 2 |
| Annotation callouts | 2 |
| Lifelines (sequence) | 5 |
| Lanes (swimlane) | 5 |
| Items (quadrant) | 12 |
| Entities (er) | 8 |
| Nesting levels | 6 |
| Tree depth | 4 |
| Org chart depth, nodes | 4, 12 |
| Layers, pyramid layers | 6 |
| Venn circles | 3 |

Over budget means two diagrams, an overview and a detail.

Two types hold a named exemption from this table, granted to them and nothing else.
`dp-integration` may run to 20 nodes and 20 arrows. `dp-security-matrix` may run to 14
components by 6 roles, so 20 labelled nodes and 0 arrows; its value cells are not nodes.
Both exemptions are stated in full in their own type reference, and every other row of
this table still binds for them.

**Page structure**: eyebrow in mono, title in Instrument Serif, optional muted subtitle,
then a borderless diagram sitting directly on the page, then optional summary cards in a
grid with varied widths such as `1.1fr 1fr 0.9fr`, then a mono colophon footer above a
hairline. The framed container is opt-in, not the default.

**Whitespace is part of the figure.** A zone or container box sized well past its
contents leaves a dead quadrant and reads as an unfinished layout. Size containers to
their contents plus one padding step, where a padding step is 24 or 32, from the gap
vocabulary. A container under half full of its own area is over budget: drop it, or move
something into it.

## 7. Output

One self-contained `.html` file: embedded CSS, inline SVG, no JavaScript, no external
images. The only network dependency is the Google Fonts link for Instrument Serif, Geist and
Geist Mono. It loads in a published Artifact, where Google Fonts stylesheets are allowed.
A standalone file may open where the link cannot load, and the container shell may not
reach Google Fonts either, so keep a system stack behind every face:
`--font-serif: 'Instrument Serif', Georgia, 'Times New Roman', serif;` (the templates carry
it). When the owner needs the exact faces offline, embed the three families as base64
`@font-face` blocks instead of the link. A render check in a shell without Google Fonts shows
the fallback, so judge layout there, not typography.

Copy the closest starting point from `assets/`: `template.html` for a minimal figure,
`template-full.html` when the diagram is the hero of a long-form page,
`template-terminal.html` for the CLI register. Each type reference names its own worked
example. Then replace the eyebrow, the h1 and the SVG body.

Export to PNG or SVG is **manual, never unprompted**. When the owner asks, load
[export.md](references/export.md).

## 8. Pre-output checklist

Run it before writing the file, not after.

**Fit**: right type for the content, a table or paragraph would not do the job better,
matching `type-*.md` loaded.

**Remove test**: can any node go, can any two merge, can any arrow go, can any label go.

**Signal**: accent on two elements or fewer, legend covers every type used and nothing
extra, inside the budget in §6.

**Technical**: C1 orthogonal, C2 label gap, C3 no shared paths, C4 fanned attach points,
C5 no routing behind a third box. Arrows before boxes. Every arrow label masked. Legend
is a bottom strip. No vertical text. `viewBox` expanded for the legend. Every coordinate
and dimension divides by 4, with only the four exemptions in style-guide.md. No container
sized more than one padding step past its contents.

**Type**: names in sans, technical sublabels in mono, title in Instrument Serif,
callouts in italic Instrument Serif.

**Skin**: if the target is a dark surface, `skin.py check` exits clean.

**Then run the linter.** It is not optional and it is the last step before delivery:

```
python3 scripts/lint-diagram.py diagram.html
```

It enforces two layers. **Geometry**: C1, C2, C4, the grid rule and the output rules.
**Composition**: dead canvas bands over 20 percent of the viewBox, containers under a
third full of their contents, and warnings for uniformly sized nodes, an ad-hoc spacing
vocabulary, and an accent that lands on connectors but on no node. Run
`--no-composition` to check geometry alone while iterating.

What it still cannot see: C3 and C5, which need full geometry; any colour set through a
CSS variable rather than a literal hex; label masks wider than 160px; and anything
inside a nested icon svg. The linter passing is a floor, not the taste gate.

**Then render it and look at it.** This step is not optional either.

```
python3 -c "
import asyncio
from playwright.async_api import async_playwright
async def m():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1400,'height':900})
        await pg.goto('file:///abs/path/diagram.html'); await pg.wait_for_timeout(2500)
        await pg.screenshot(path='/tmp/check.png', full_page=True); await b.close()
asyncio.run(m())"
```

Then open the image and answer the three questions no checker can:

- Does the figure argue the point the title claims, or does the title carry it alone?
- Is any label placed where it reads as belonging to the wrong element, even though it
  clears its own stroke by the required gap?
- Is the accent on the thing that matters, or on the arrow pointing at it?

A figure that passes the linter and fails these is the default failure mode of this
skill. It ships compliant and inert. Fix what you see rather than explaining it.

Pairs with `viz-dashboards` for anything measured, `frontend-taste` and
`google-slides` for the surfaces a figure gets embedded into, and `house-style`
for the prose around the figure.