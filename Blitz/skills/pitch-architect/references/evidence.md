# Evidence standards

How to make the numbers land with a numerate, skeptical audience. Read this when building slides 4, 6, 7, and the appendix.

## Provenance tiers

Label every number with its tier. Mixing tiers silently is how decks lose numerate audiences.

| Tier | Source | Example citation |
|------|--------|------------------|
| T1 | On-chain, independently verifiable | contract address, explorer link, block height |
| T2 | Audited or official reporting | audit report, attestation, filed financials |
| T3 | Third-party analytics | DefiLlama, Dune query link, Kaiko, Token Terminal |
| T4 | Internal estimate or model | "internal model, assumptions in appendix" |

Rules:

- Never present T4 as anything but T4. "Illustrative" or "internal estimate" in the source line, every time.
- Slide source lines: bottom of every data slide, small and muted: `Source: DefiLlama, 90d trailing (T3); retention model internal (T4), assumptions p. A2.`
- If a T4 number is decisive to the argument, its assumptions get an appendix slide. A decisive number with hidden assumptions is where Q&A goes to die.

## Scenario table spec

The centerpiece of the numbers slide. Structure:

| Scenario | Probability | Key assumption | Outcome (metric) | Implication |
|----------|------------:|----------------|-----------------:|-------------|
| Bear | 25% | driver that breaks | value | decision meaning |
| Base | 55% | central driver | value | decision meaning |
| Bull | 20% | driver that compounds | value | decision meaning |
| **EV** | **100%** | | **Σ p·x** | |

Rules:

- This table is for explicitly mutually exclusive and exhaustive scenarios only. Check their event boundaries and arithmetic; then percentages sum to 100%. Independent or separately defined events are not normalized, and rankings need criteria/evidence/uncertainty/sensitivity rather than probabilities. Flag unsupported precise estimates; qualitative uncertainty is allowed when the evidence does not support a number.
- Use as many non-overlapping scenarios as the event definition needs, including a residual when necessary. Three rows are a presentation default, not proof of exhaustive coverage.
- Each scenario names its **driver**, not just its outcome. "Bear: 35% TVL retention after emissions end" is arguable; "Bear: $14M" alone is not.
- Show expected value. It converts the table from three stories into one number a decision-maker can weigh against cost.
- The base case row gets visual emphasis (accent border or tint).
- Where a simulation produced the distribution, say so and chart it (fan chart or histogram) beside the table.

## Comparables

- Pick precedents with the same **structure**, not the same logo tier. A matched-emissions program at a mid-size venue is a better comp than an unrelated program at a famous one.
- Normalize or it isn't evidence: $ of TVL per $1 of incentive at day 90; % retained 90 days after emissions end; fee revenue per $1M TVL.
- State the differences between the comp and your plan in one line each. An audience that finds the difference before you name it stops trusting the comp.
- Two strong comps beat five weak ones.

## DeFi metric definitions (use precisely; misuse is instantly detected)

- **TVL:** state the venue and whether double-counted (wrapped/restaked). Distinguish incentivized vs organic. The honest number is **retention**: % of TVL remaining N days after emissions end.
- **Stablecoin supply:** native mint vs bridged; circulating vs issued. Holder count and median balance separate distribution from whale concentration. Velocity (volume/supply) separates money that moves from money that parks.
- **Incentive efficiency:** $ TVL at day 90 per $1 spent, and retained-$ at day 180 per $1. The second is the real one; mercenary capital makes the first flatter.
- **Liquidity depth:** quote ±2% depth, not pool size. A $40M pool with $600K depth at ±2% is a $600K pool for anyone trading size.
- **Protocol revenue vs emissions:** revenue after incentive spend. A pool earning $1M fees on $3M emissions is losing $2M, and the audience will do this subtraction if the deck doesn't.
- **APR/APY:** state which, and what's variable. Quoting a peak as if it were a mean is the fastest way to lose a fund's desk.

## Number formatting

- $2.4M, not $2,400,000. 3.1x, 47%, +38pp (points vs percent; don't mix).
- One decimal for money and multiples; whole numbers for percentages unless the decimal decides something.
- Deltas signed: +38%, −12pp.
- Absolute dates: "by 31 Jul 2026," never "in six weeks."
- Round consistently. $38.61M in one slide and "$39M" in another reads as sloppiness, and sloppiness in formatting implies sloppiness in modeling.
