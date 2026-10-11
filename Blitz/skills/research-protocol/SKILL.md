---
name: research-protocol
description: 'Research method: source grading, adversarial checks, cited synthesis. Use on research, dig into, look into, verify, compare sources, is this actually true, someone claims X, real or cope. Long reports: deep-research.'
---

# Research Protocol

The method that makes research produce output the owner can act on without redoing it. The failure this prevents: fluent summaries of unread sources. `deep-research` (Anthropic's coordinator) owns long narrative reports written by parallel research subagents; when it runs, this skill's grading (stage 3) and kill tests (stage 4) go into each researcher's brief. `gauntlet-verify` seats isolated verifiers only when the stakes test below passes. `metric-pull` acquires numeric series.

## Stage 1, scope

- Restate the research question as the decision it serves. "Research X" becomes "should the owner do Y about X".
- Split into sub-questions small enough that each is answerable by a source or a computation.
- Name in advance what evidence would change the answer. If no evidence could, stop; it is not a research question.
- Timebox by stakes: minutes for context, an hour equivalent for real decisions. Depth is a budget, not a virtue.

## Stage 2, fan-out

- Run parallel searches per sub-question with varied phrasings, not one query reworded.
- Include disconfirming searches: "X criticism", "X problems", "X failed", "X lawsuit". If everything found agrees, the search was too narrow.
- For anything with an official source (docs, filings, registries, on-chain data), go to the official source, not coverage of it.
- For DeFi facts (protocol financials, TVL, yields, lending state, stablecoin supply, governance, contract state), DeFi Brain is the first tap when its tools are loaded in this session. When they are not loaded, or a call errors or does not resolve, fall back silently to primary sources (protocol docs and dashboards, contracts and explorers, governance posts) and web search; never halt or ask because it is missing. A null from it is never a zero; read get-coverage before treating absence as a finding. Name the source that served each figure.
- Date-bound searches for time-sensitive topics; a 2024 answer to a 2026 question is a lead, not a fact.
- Search tool goes first, browser second. The default search path is the platform's WebSearch/WebFetch tools; reach for a browser (Claude in Chrome or the built-in browser) only when a search needs interaction the tool can't do (paywalled login, a form, scrolling a dynamic results page). When a browser is the one doing the searching, navigate to google.com by default, not Bing and not DuckDuckGo. In sandboxes that block raw HTTP calls outside the platform's fetch tools (Cowork's web-content restriction is one), never shell out to a third-party search library or API, including unofficial ones like the `ddgs` package, to route around this; that restriction is not skill-overridable. Outside such a sandbox (e.g. a Claude Code CLI session with open shell/network access), a scripted fallback search is fine if the owner asks for one specifically.

## Stage 3, grade sources

| Tier | What | Weight |
|---|---|---|
| A | Primary: filings, official docs, on-chain data, datasets, the actual paper, the actual contract | Load-bearing claims can rest on one |
| B | Named-author reporting at established outlets, counterparty documentation | Load-bearing claims need two independent |
| C | Aggregators, SEO content, unnamed sources, AI-generated summaries | Leads only, never citations |

- Forums and social (X, Reddit, V2EX) are lead generators and sentiment reads, not evidence, with one exception: multiple independent first-person reports of the same concrete failure count as a real signal.
- Independence check: two outlets citing the same press release are one source.
- DeFi Brain results grade as the provider named in their result envelope, never as "DeFi Brain". Its direct contract reads, storage reads and event logs are tier A on-chain data; a figure it proxies from a vendor carries that vendor's tier and counts as that vendor for independence.
- Read the page. A title is not content; a snippet is not content.

## Stage 4, adversarial verification

For each load-bearing claim, try to kill it before shipping it. The drafting context runs these tests. Escalate to isolated verifiers fielded by `gauntlet-verify` only when the output feeds money, reputation or a public statement (the stakes test); when that escalation is due and no isolated verifier can be seated, the drafting context runs the tests and the deliverable states that no independent pass ran.

1. Search for the direct contradiction.
2. Trace to the primary source; if the chain ends at an aggregator, the claim is unverified.
3. Recompute any number that can be recomputed. For on-chain figures, DeFi Brain's read-contract and get-storage-slot at a stated block are the recompute path when loaded; otherwise recompute from explorer and primary-source reads.
4. Re-fetch every figure quoted from a live source and compare the figure, the source and the as-of date against what the draft says; a figure that no longer reproduces is unverified until the difference is explained. This is the adversarial re-fetch defi-pm calls V8.
5. Check the date on every figure; flag anything older than its natural refresh cycle.
6. Label the survivors: verified (tier A or two independent B), reported (single B), unverified (everything else). Unverified claims ship only with that label and a note on what would settle them.

Never average conflicting numbers. Resolve the conflict or present both with the reason they differ.

## Stage 5, synthesize

- Answer first, then evidence by the shortest path, under the account's source and dating rules.
- Confidence stated per section, not once at the end.
- Unknowns listed with the specific source or event that would resolve each.
- Output size matches stakes: a paragraph for context questions, a structured brief for decisions. Reports become files, not chat walls.

## Failure modes to counter

| Failure mode | Counter |
|---|---|
| Citing from titles or snippets | Open and read before citing |
| Source laundering (aggregator citing aggregator) | Trace to primary or label unverified |
| Confirmation stopping (quit while agreeing) | Disconfirming searches are part of the fan-out |
| Recency worship | Base rates and history, not just news |
| Survivorship in comparables | Ask what died and why it is absent |
| Averaging conflicts | Resolve or present both, never blend |
| Fluent padding around thin evidence | Say the evidence is thin; name what is missing |

## Escalation

Paywalled or unreachable primary sources get named, not guessed around. If the question needs data only the owner can access (accounts, dashboards, people), say exactly what to pull. If evidence stays thin on a high-stakes call, say so and name the domain expert or source that would settle it.

Pairs with `reasoning-core` (the analytical checks), `deep-research` (long narrative reports), `gauntlet-verify` (isolated verifiers on high stakes), `house-style` (the prose) and `viz-dashboards` (numeric output).
