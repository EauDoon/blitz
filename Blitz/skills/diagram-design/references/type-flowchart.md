# Flowchart

**Best for:** decision logic, algorithms, user-facing branching flows ("Should I…?"), onboarding routing, support-triage trees.

## Layout conventions
- Shape carries type, not color:
  - **Pill**: start / end. Draw it as a `<path>` outline, not as a `<rect>` with a large `rx`: two horizontal edges joined by a semicircular arc cap at each end, arc radius = half the box height, closed with `Z`. On the 160 × 48 terminators in `assets/example-flowchart.html` that is `M444 40 H556 A24 24 0 0 1 556 88 H444 A24 24 0 0 1 444 40 Z`; the coral focal terminator is 160 × 56 and uses `A28 28`. Keeping the caps as arcs means no box in the figure carries a radius above the 8 ceiling in the radius token set, so the "radius above 10px on a box" anti-pattern in SKILL.md §4 still holds.
  - **Rectangle** (`rx=6`): step / action
  - **Diamond**: decision (≤3 exits)
  - **Small filled ink dot** (`r=4`): merge point where branches rejoin
- Flow runs top→down. From a diamond, conventional exits: Yes to the right, No below, but label every outgoing arrow regardless.
- Use coral on the happy path *or* on the single most consequential decision: never on every decision.
- If two arrows must cross, use a small arc jump on one so the crossing is readable.

## Anti-patterns
- Using fill color to signal node type (shape does that).
- Decision diamond with 4+ exits: refactor into nested diamonds.
- Unlabeled decision branches.

## Examples
- `assets/example-flowchart.html`: minimal light
- `assets/example-flowchart-dark.html`: minimal dark
- `assets/example-flowchart-full.html`: full editorial
