---
name: "viz-dashboards"
description: 'Chart and dashboard standard: 0f0f0f canvas, libraries inlined, never CDN. Use when numbers are worth comparing, on chart, graph, plot, simulate, dashboard. Chat forecasts get a scenario table. Decks: google-slides.'
---

# Viz and Dashboards

The standard every chart and dashboard in the owner's HTML and Plotly output meets: when a visual earns its place, how it renders without failing silently, and the QA pass before delivery. It does not own the numbers or the structure. metric-pull or the owning domain desk acquires the figures, diagram-design owns structural figures such as architecture and flow, and frontend-taste (its cinematic reference) supplies the visual system when a surface must look premium. Where the built-in dataviz skill also loads (it ships a light palette), this standard wins on canvas, rendering and QA; check which standard loaded before drawing the first chart.

Cost and spend dashboards are charts: model or seat costs by model, token spend, vendor or program spend over time. This skill builds them; orchestrator or the owning desk supplies the numbers and the routing call.

The 0f0f0f canvas applies to HTML, Plotly and dashboard output. A chart inside a deck follows the deck theme and `google-slides` chart rules; a chart inside a document follows the `doc-style` theme.

## When to build

Numbers worth comparing get a chart, and so do multiple scenarios. A probability or forecast question asked in chat gets the scenario table in the reply, not a dashboard; build a dashboard when the owner asks for one or when the deliverable is itself a file. Skip visuals for quick lookups, text edits, and single-number answers; forcing a chart onto those is noise.

## Rendering rules that prevent silent failures

Each rule exists because its violation shipped a broken artifact at least once.

1. **Plotly from Python:** hardcode `paper_bgcolor="#0f0f0f"` and `plot_bgcolor="#0f0f0f"` inside `update_layout()` on every figure, regardless of template. Templates get overridden; direct arguments do not.
2. **Self-contained HTML:** inline every JS dependency. `fig.write_html(path, include_plotlyjs=True)` or inline the library source directly. Sandboxed file viewers block external scripts; a bare `<script src="https://cdn...">` ships a blank page ("Plotly is not defined") that fails only after delivery.
3. **Verify the inlining:** file size over roughly 1 MB when Plotly is inlined, and zero external `<script src=` tags. Grep the file; do not assume.
4. **Artifacts where runtime JS libraries are unreliable:** pure inline SVG with coordinates precomputed in code. No runtime CDN loads.

## Dashboard composition

- Background #0f0f0f throughout, consistent dark palette for text and gridlines.
- KPI strip on top when headline numbers exist.
- 3 to 8 coordinated charts; every panel earns its place.
- Use an event or scenario table adjacent to the relevant charts. Only explicitly mutually exclusive and exhaustive scenarios sum to 100%. Independent or separately defined events are not normalized. A ranking uses criteria, evidence, uncertainty and sensitivity, without invented probabilities. The table in the reply and on the canvas uses the same definitions, rows, horizon and numbers.
- Assumptions block visible next to the visuals: sources, the date of the data, [ESTIMATE] flags.
- Every axis labeled with units. Every chart titled with the claim it supports.
- For heavier modeling, the established pattern is Bayesian structure plus Monte Carlo paths plus sensitivity (Sobol or tornado) where the question justifies it.

## Simulation standards

Gaussian GBM understates crash risk. For price path simulation, prefer regime-switching jump-diffusion with Student-t innovations (nu around 5) and GARCH(1,1) clustering. Macro views enter through regime probabilities, not drift hacks. State the architecture next to the output.

## Eight-point QA pass, mandatory before delivery

1. Math vs text: every number in titles and subtitles matches the computed data. Render both from one params object so they cannot drift.
2. Units consistent across charts, tables, and prose.
3. No label collisions or clipped annotations at default viewport size.
4. Color semantics: red for negative or risk, green for positive, consistent across panels.
5. Negative bars and axis baselines render correctly; zero lines visible.
6. Dead code, unused traces, placeholder panels removed.
7. Interactions do what their labels say: hover, toggles, sliders.
8. Self-containment verified: file size check, no external `<script src=` tags.

Bugs a QA pass would catch are yours to own before the owner sees them, not after.

## Worked micro-example

A revenue-sensitivity dashboard once carried the subtitle "take rate 12%" while the model ran 15%. QA point 1 catches it by comparing rendered strings against the parameter dict. The fix is structural, not cosmetic: define one params object and render it into both the model and the subtitle, so the drift class disappears.

## Host and project prerequisites

Use the current request to choose a chart or a simple table. Check library-loading rules on the actual host, inline dependencies when required, and verify the rendered artifact. The cinematic option remains in frontend-taste's references; it is a design choice, not a personal default or proof of current host support.

Pairs with metric-pull and the domain desks for the numbers going in, reasoning-core for scenario table discipline, diagram-design for structural figures, frontend-taste when the surface must look premium, and cold-read when a dashboard is about to ship.
