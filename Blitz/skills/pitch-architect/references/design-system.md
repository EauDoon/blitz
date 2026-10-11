# Design system: dark HTML pitch page (option)

Use this file for one case only: a pitch delivered as a dark HTML page, such as a web one-pager or an Artifact. It never applies to a deck or a document. Decks take their look from `google-slides` (navy on white for anything a bank or board sees), memos from `doc-style`, and charts inside either follow that deck or document theme.

The theme is dark because a crypto or quant-native reader lives in dark trading terminals and analytics tools, where big light-on-dark numbers carry authority. The canvas matches the owner's 0f0f0f standard for HTML output, and `viz-dashboards` rules (libraries inlined, never CDN loaded, eight-point QA) apply to every chart on the page.

## Tokens

| Token | Value | Use |
|-------|-------|-----|
| bg | #0F0F0F | page background, every chart background |
| surface | #1A1A1A | cards, table headers, callout boxes |
| line | #2A2A2A | borders, gridlines, dividers |
| text | #F5F5F5 | headlines, body |
| muted | #9CA3AF | captions, source lines, secondary labels |
| accent | #22D3EE | the hero color: key number, base-case row, hero series, the ask |
| good | #34D399 | semantic positive only |
| bad | #F87171 | semantic negative only |
| context | #6B7280 | non-hero chart series |

Rules: one accent per page. Swap #22D3EE for a brand color if the user has one, but never run two accents. Green and red are semantics, not decoration. Everything important is accent; if everything is accent, nothing is.

## Typography

A system sans stack, so the page needs no font download: `system-ui, -apple-system, "Segoe UI", Arial, sans-serif`. Sizes in px, converted from the old slide sizes at 4/3 px per pt.

| Role | Size | Weight | Color |
|------|------|--------|-------|
| Hero number | 88 to 128 | bold | accent |
| Action title | 34 to 40 | bold | text |
| Section or kicker | 16 to 17, all caps, letterspaced | bold | muted |
| Body | 20 to 24 | regular | text |
| Table text | 17 to 20 | regular | text |
| Source line | 13 to 15 | regular | muted |

Body text: at most about 5 lines per section. If it needs more, the section has two ideas: split it or cut.

## Section layouts

Six patterns cover the whole spine, one per screen-height section:

1. **Hero number** (opportunity, ask): kicker top-left → action title → one huge accent number center → one line of context under it → source line. Nothing else.
2. **Scenario table** (numbers): action title → table with probability column → EV row → base-case row tinted surface with accent left-border → chart beside or below → source line.
3. **Mechanism diagram**: 3 to 5 surface-colored rounded boxes, left→right flow, accent arrows, one label each, at most 4 words per box. Two-line caption below. If the mechanism needs 8 boxes, the section is explaining too much: simplify or split. `diagram-design` draws it when the figure is more than a simple row of boxes.
4. **Comparables**: 2 to 4 rows, each "precedent → normalized result," biggest normalized number in accent.
5. **Risk register**: 3 to 5 rows of risk → mitigation → residual. Residual column in muted, never hidden.
6. **Ask section**: surface card with accent border; inside: the ask (large), decision date, what they get, kill criteria. This is the only element allowed a border glow.

Global: generous margins, no clip art, no stock photos, no gradients except a subtle one behind the title. No external resources: every script and image inline.

## Chart spec

Charts on this page are Plotly with the library inlined into the file, or inline SVG. Rules:

- Background #0F0F0F for paper AND plot area. **Plotly: set `paper_bgcolor="#0f0f0f"` and `plot_bgcolor="#0f0f0f"` directly in `update_layout()` on every chart, regardless of template.**
- Hero series in accent; every other series #6B7280. The chart makes one point; color says which.
- **Annotate the takeaway on the chart** ("$38M base case", arrow to the point). A chart the reader must decode is a chart that failed.
- Chart title = mini action title, not axis description.
- Gridlines #2A2A2A, horizontal only where possible. Direct-label series ends instead of legends when there are 3 series or fewer.
- Text at least 14 px.

Plotly boilerplate:

```python
fig.update_layout(
    paper_bgcolor="#0f0f0f", plot_bgcolor="#0f0f0f",
    font=dict(color="#F5F5F5", size=14),
    xaxis=dict(gridcolor="#2A2A2A", zerolinecolor="#2A2A2A"),
    yaxis=dict(gridcolor="#2A2A2A", zerolinecolor="#2A2A2A"),
    colorway=["#22D3EE", "#6B7280", "#9CA3AF"],
)
fig.write_html(path, include_plotlyjs=True)  # inline the library, never CDN
```

## Build notes

- Tables: header row surface (#1A1A1A) bold, row borders #2A2A2A, no zebra striping, numbers right-aligned, base-case row emphasized.
- Verify contrast: muted on bg is the minimum readable pair; never put muted text on surface below 14 px.
- Run `viz-dashboards`' self-containment check (zero external `<script src=` tags) before delivery.
