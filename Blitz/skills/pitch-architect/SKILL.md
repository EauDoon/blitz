---
name: pitch-architect
description: 'Persuasion structure for pitches, proposals, budget asks, exec approvals, investment memos and board decks. Use on pitch deck, convince them, get the CEO to approve, one-pager. Building: google-slides, doc-style.'
---

# Pitch Architect

Structure decks and memos that get a yes: partnership pitches, exec strategy approvals, budget asks, investment memos, DeFi growth and integration proposals.

One belief drives everything here: **decks fail from structure, not slides.** Fix the argument first, then hand it to the builder. A beautiful deck with a buried conclusion loses to an ugly deck with a clear one. This skill owns the argument; `google-slides` owns the deck look and build, and `doc-style` builds the memo.

## Why this persuades

The reader is busy, numerate, and skeptical. They decide within two slides whether to engage or skim, and they will attack the weakest number you show. So:

1. **Answer first.** The full argument and the ask appear by slide 2. Evidence follows the conclusion, never precedes it. Skimmers read slide 2 and the ask slide; the middle exists so verifiers can check the work.
2. **Titles carry the argument.** Every headline is a conclusion ("Base case: TVL 2.1x in 90 days"), never a topic label ("TVL Projections"). Reading only the titles must reconstruct the entire case: the title test.
3. **Numbers have provenance.** One unsourced figure and a numerate audience discounts everything else. Every number gets a source and a tier (see `references/evidence.md`).
4. **Define the forecast type.** Only explicitly mutually exclusive and exhaustive scenarios form a distribution summing to 100%, with expected value where outcomes share units. Independent or separately defined event estimates need definitions, horizon, basis and dependence limits, without normalization. Rankings need criteria, evidence, uncertainty and sensitivity, without invented probabilities. Flag unsupported precision.
5. **Objections are pre-empted.** A risk slide the audience didn't have to ask for converts skeptics. If you don't write the risk ledger, they write it in their heads, and theirs is worse. Arguing against your own interest is the cheapest credibility available.
6. **One ask, exact.** Amount, action, decision date, and what happens in the first 30 days after yes. Two asks produce zero decisions.

## Workflow

### 1. Intake

Get these before outlining (ask the user; derive and label as estimates only where they can't supply):

- **Audience and decision.** Who decides, and what single decision is sought? Pick the audience mode: partner, exec, or investor (`references/persuasion.md`).
- **The one metric.** What does this move: TVL, supply, revenue, share? A deck that moves three metrics moves none.
- **Scenario inputs where applicable.** Event boundaries, horizon, drivers and evidence; probability weights only when defensible. Do not invent a distribution to complete a pitch.
- **Comparables.** Precedents that make the plan feel like a reference class, not a leap.
- **Top objections.** The three hardest questions this audience will ask.
- **Decision date.** An ask without a date is a suggestion.

### 2. Outline before design

Write every action title first, in order, as plain text. Check the title test: do the titles alone reconstruct the argument? Fix the outline before opening any design tool; structural surgery is cheap here and expensive later. For high-stakes decks, show the user the title outline for approval before building.

### 3. Hand off the build

Decks go to `google-slides`, which owns the look, the canvas, charts on slides, render QA and the Google Slides route: navy on white for anything a bank or board sees. Memos go to `doc-style`, which builds and verifies the document. Hand the builder the approved title outline, the scenario table, the risk ledger and the ask. Whatever the builder, these hold:

- One idea per slide.
- Source line on every slide that shows data.
- The ask on its own slide, with the decision date.

`references/design-system.md` is an option for one case only: a pitch delivered as a dark HTML page (a web one-pager or an Artifact), never a deck or a document.

### 4. Pre-flight (do not skip)

- [ ] Title test passes top to bottom
- [ ] Every number has a source and tier; estimates labeled as estimates
- [ ] Forecast type and event definitions checked; only an explicitly mutually exclusive and exhaustive distribution sums to 100%; expected value only where meaningful
- [ ] Risk slide: named risks, mitigations, residual exposure
- [ ] Exactly one ask, with a decision date
- [ ] Audience mode applied (their upside first for partners; options + recommendation for execs; downside math first for investors)
- [ ] Copy rules pass (below)
- [ ] Kill criteria stated where the plan spends money over time

## The spine

Default: 10 slides + appendix. Cut before adding; past 15 slides you are hiding the argument.

| # | Slide | Title pattern | Job |
|---|-------|---------------|-----|
| 1 | Title | Thesis in one sentence | Set the frame before they set it |
| 2 | Executive summary | The answer + the ask | The whole deck for skimmers |
| 3 | Why now | What changed | Urgency from facts, not adjectives |
| 4 | Opportunity | The sized prize | Anchor high, honestly |
| 5 | Mechanism | How it works | A plan they can picture works |
| 6 | Numbers | Scenario table + EV | Show the distribution |
| 7 | Proof | Precedent → result | Reference class, not faith |
| 8 | Risks | Named + mitigated + residual | Pre-empt the objection |
| 9 | Ask | Exact + dated | Force the decision |
| 10 | Next steps | 30 / 60 / 90 | Make yes cheap to say |
| A | Appendix | None | Methodology, sources, sensitivity, hardest Q&A |

**Memo variant:** same spine as section headings, 1 to 2 pages. Exec summary is the first paragraph; the ask is bolded in it.

## Audience modes (summary; full treatment in references/persuasion.md)

- **Partner / BD:** Their P&L leads. Their fees, their users, their TVL on slides 1 to 4; your ask arrives only after their upside is established. Quantify their integration cost as small (eng-days, not "easy").
- **Exec / internal:** Lead with the metric moved and the cost of inaction. Execs pick between options, not yes/no: present A/B/C with a recommendation. State kill criteria; nothing buys trust faster than naming what would make you stop.
- **Investor:** Return math and the downside case lead. They are pricing risk: hand them the risk ledger before they build a worse one. Why-now and why-you must survive the question "why hasn't someone done this?"

## Copy rules

Short declarative sentences. Lead with the point. Concrete nouns and specific numbers over abstractions. Plain verbs ("decide," not "make a decision"). Cut hedges unless they carry information. Format numbers tight: $2.4M, 3.1x, 47%, +38pp. Absolute dates ("by 31 Jul"), never relative ("in six weeks").

Banned words and phrases: `house-style`'s canonical list. Pitch-specific additions: revolutionary, game-changing, unlock. If a word wouldn't survive a skeptical CFO reading it aloud, cut it.

## References

- `references/persuasion.md`: read when structuring the argument or tailoring to an audience mode
- `references/evidence.md`: read when building the numbers: provenance tiers, scenario table spec, comparables, DeFi metric definitions
- `references/design-system.md`: read only for a pitch delivered as a dark HTML page
