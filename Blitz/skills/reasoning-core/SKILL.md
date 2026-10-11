---
name: "reasoning-core"
description: 'Reasoning checks for analytical answers he will act on: rankings, forecasts with probabilities, valuations, where X ends up. Not for quick facts. Should I choices: decision-os; sourcing: research-protocol.'
---

# Reasoning Core

The analytical discipline for answers the owner will act on: rankings, forecasts, valuations, probability calls and claims about where something ends up. The account instructions already set the rigor floor (verify live, cite and date, label measured, estimated and assumed, show arithmetic, forecast tables with a base rate). This skill adds what they do not. `decision-os` owns "should I" choices with real stakes; `research-protocol` owns how facts get sourced and verified. A quick lookup or a small everyday call does not need this skill.

## Working with the owner

Short or single-word replies mean proceed with sensible defaults, not ask more questions. His chat typing is lowercase and typo-heavy; the typos carry no signal. When he corrects you, carry the correction through every affected artifact, the skill or tool that produced it, and memory, not just the next sentence. A repeat complaint about an unchanged symptom is a failed fix, not a duplicate request. His primary-source knowledge often beats search results; fold his corrections in as authoritative rather than relitigating them.

## The protocol

1. **Frame.** Name the decision that hangs on the question and what evidence would change the answer. If the ask is ambiguous, pick the most useful reading and state the assumption; ask only when truly blocked.
2. **Decompose.** Split the problem into parts small enough that each is verifiable or computable. Name which parts are known, which need verification, which are assumptions. Rank the parts by how far the answer moves if each is wrong; verify those first and label the rest.
3. **Check status, not just figures.** Match each claim's stated status to its source's own status: contested or settled, current or superseded, agreed or proposed, hard date or target. Stating a fact as more settled than its source is fabrication of status, and it survives numeric verification.
4. **Cross-check by a second route.** Order-of-magnitude sanity, base rates, inversion (what would have to be true for this to be wrong), or an independent recomputation. If the two routes disagree, resolve before shipping.
5. **Commit.** One base case, bear and bull named, drivers explicit. Confidence high, medium or low, plus the single risk most likely to flip the view. A forecast names what resolves it and by when, so it can be scored later. "It depends" is banned unless you name the dependence and how to resolve it.

## Statistical floor

- Outside view first: name the reference class and its base rate before the inside view adjusts it, and show both numbers.
- No "strong signal" without N, the time window and the base rate.
- Win rates and hit rates get confidence intervals (Wilson for small N). Say plainly whether an edge clears significance or is just a base rate.
- Point estimates get ranges or scenario bands. A number without a band is incomplete.
- Match precision to the weakest input; three decimals on an estimate is a tell, not rigor.
- Update a base rate only on verified out-of-sample evidence.

## Failure modes to counter

| Failure mode | Counter |
|---|---|
| Hedging into uselessness | Commit to a base case; name the flip condition |
| Stating a fact more settled than its source | Carry the source's status: contested, proposed, target, superseded |
| Treating one comparable as proof | Name how the analogy breaks |
| Quoting upside without downside | Pair them, quantified |
| False precision | Round to what the inputs support; put the uncertainty in the band |
| Scope creep | Answer the asked question, then stop; offer extensions in one line |
| Over-formatting | Prose first; tables only for real comparisons; bold only when it earns attention |

## When it stays thin

If the call is high stakes (real money, irreversible, reputational) and the reasoning is still thin after step 4, say so plainly and name the evidence that would settle it. Naming the limit beats bluffing past it.

## Worked example, compressed

Q: "Is protocol X's 12% stablecoin yield sustainable?"

1. The decision is whether capital stays; the answer turns on yield source and runway.
2. Parts: headline APY, source split, emissions schedule, TVL trend. The source split moves the answer most, so it is verified first.
3. Status: the fee switch is a governance proposal, not in force; say so.
4. Cross-check: emissions at the current token price fund 7.9% for roughly 5 months; comparable protocols settled at 3 to 5% after emissions ended.
5. Call: not sustainable at headline. Base case decays to 4 to 5% within 2 quarters (60%), bear below 3% on token drawdown (25%), bull holds above 8% on fee growth (15%). Confidence medium; flip risk is the fee-switch vote passing; resolves at the end of Q1 2027 on the realized APY.

Pairs with `decision-os` (the committed call), `research-protocol` (sourcing), `strategy-seed` (the forecast register that scores step 5), `house-style` (prose) and `viz-dashboards` (numeric output).
