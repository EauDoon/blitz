---
name: metric-pull
description: 'Pulls and reconciles an on-chain or protocol metric from two sources, dated. Use on "what is TVL on X", "what does DefiLlama say", "how much USDC is on Base", "check this number before I post it". Meaning: defi-desk.'
---

# Metric Pull

Supply growth and TVL are the KPIs, so the risk sits in acquisition, not analysis. Every number is definitionally ambiguous until defined. A figure ships with a source, an exact definition, a chain scope, and an as-of stamp, or it does not ship. Everything in this file is durable protocol; dated vendor observations sit in references/vendor-notes.md.

## Sources by metric class

| Metric class | Primary | Independent cross-check | Note |
|---|---|---|---|
| Circulating supply | Issuer contract read via chain RPC at a stated block, minus a published exclusion list | DefiLlama or Artemis stablecoin series | RPC read is ground truth; the exclusion list is the whole answer, so publish it |
| Bridged supply per chain | Canonical bridge locked balance | Destination chain wrapper totalSupply | These two should match; a gap means a mint outside the canonical path |
| Protocol and chain TVL | DefiLlama with double count excluded | Protocol contract balances read directly, or Dune on raw transfers | Vendors differ on category membership; reconcile the protocol list before the total |
| DEX and CEX volume | Dune on decoded swap events for DEX, exchange API per venue for CEX | DefiLlama or the DEX subgraph; nothing independent exists for CEX | CEX volume is self reported; never blend venues into one clean number without saying so |
| Holder counts and distribution | Dune or RPC balance snapshot at a block | Block explorer holders tab | Both count addresses, not people |
| Net flows and cohort retention | Dune on labelled address sets, cohorts keyed to first-touch block | Explorer balances over the same window, or a second cohort definition | Label quality and cohort definition are the error terms; no vendor ships retention, so the definition is yours to defend |
| Fees, revenue, realised yield | Token Terminal or DefiLlama income view | Protocol accounting or governance reporting | Vendors split gross fees and protocol take differently |

Two sources reading one indexer are one source. Explorer token pages often display a circulating supply fed by a market data vendor rather than computed from chain state, which makes explorer and vendor one source for supply while they stay independent for balances. Check the field's provenance, not the site.

| Genuinely independent | Quietly one source |
|---|---|
| Chain RPC contract read against any vendor; exchange API against on-chain data; canonical bridge locked balance against destination totalSupply | DefiLlama adapter against the protocol's own dashboard when the protocol wrote the adapter; two Dune queries on one Spellbook table; two dashboards hitting one subgraph; Artemis or any vendor page against the public adapter or aggregator it ingests; the DeFi Brain MCP against whatever provider its envelope names |

## DeFi Brain as first pull when loaded

When DeFi Brain tools are loaded in the session, they are the fast first pull for TVL, fees, revenue, stablecoin supply, volume, yield series, and lending state, and the JSON-RPC contract tools (read-contract, get-storage-slot at a stated block) can serve as the independent chain-read leg. When they are not loaded, or a call errors or does not resolve, pull from the primary and cross-check sources in the table above without comment, and name the source that served each figure. Two rules keep DeFi Brain honest. First, it is a proxy, not a source: every result envelope names the upstream provider, so a DeFi Brain figure fed by DefiLlama is DefiLlama for reconciliation, one source, not two; the cross-check must come from a different provider or a direct contract read. Second, its coverage has honest gaps: a null is never a zero, so read get-coverage before treating any absence as a finding. Carry the envelope's asOf as the as-of stamp, block height where given, and surface its warnings in the shipped figure.

## Reconciliation rule

Two independent sources inside tolerance, or the figure ships marked unverified with the delta stated. Never average a conflict; resolve it or present both with the reason, per research-protocol. Tighten to roughly a quarter of the effect being measured whenever the delta is the point, since a 3% month on month supply gain cannot be evidenced at 5% tolerance, and tighten for public posts, partner and board decks, regulator-facing documents, and any figure used as a denominator.

| Metric | Default tolerance |
|---|---|
| Supply read at a stated block | Exact. Any delta is a definition or block height mismatch, not noise |
| Circulating supply | 1% |
| TVL and net flows | 2% |
| Daily volume | 3% |
| Holder counts | 5% |
| APY or yield | Decompose first; headline APYs are not comparable figures |

## Definitional traps

| Trap | Failure | Check |
|---|---|---|
| LST and LRT layering | One ETH deposit counted at the stake, again in the restaking layer, again as lending collateral, so it lands three to four times | Use double count excluded views; count the base asset once and name where |
| Staked versus deposited | Staked implies a lock, a queue, and a slashing surface; deposited implies none of them | State which, plus the exit path |
| Bridged versus native versus canonical | Summing per chain balances double counts wrapped claims against origin locked units | Net wrappers against locked collateral; name the canonical path |
| Wash and incentivised volume | Volume inflates while fees and unique senders do not follow | Ratio volume to fees and to unique senders; flag campaign windows |
| Circulating versus total versus fully diluted | Three numbers, one ticker, wrong denominator everywhere downstream | Publish the exclusion list beside the figure |
| Exchange-held supply counted as holders | One omnibus address is millions of users; bridges, treasuries, multisigs and contracts are not holders at all | Label and exclude before counting; report addresses, never users |
| APY versus APR versus realised | Compounding assumption, reward token priced at spot versus at claim, trailing versus projected | State window, compounding, and reward pricing; prefer realised |
| USD denomination when the asset just moved 30% | TVL reads down 30% while the unit count is flat | Always carry the native unit series next to the USD series |

## Stamp and shape

Four fields on every series and every standalone figure. A number without an as-of date does not ship.

- **Source:** named vendor, query link, or contract address plus chain. "On-chain data" is not a source. For DeFi Brain results, the source is the provider its envelope names, not "DeFi Brain".
- **Definition:** written out from the traps table, including exclusions.
- **Chain scope:** explicit list. "Aggregate" is not a chain and "multichain" is not a scope.
- **As-of:** timestamp with timezone, UTC in the data and SGT in prose. On-chain reads also carry block height, the only unambiguous as-of.

Time series ship long format, one row per observation, ready for viz-dashboards without reshaping: `ts_utc, metric, chain, value_native, value_usd, price_source, source, xcheck_source, xcheck_delta_pct, status`.

- Daily grain at 00:00 UTC close unless stated; declare the grain in the header block, alongside definition, exclusion list, chain scope, pull timestamp, and query link or contract address.
- Gaps stay null. Zero means zero, and forward filling without a flag column is falsification.
- status is verified, unverified, or estimate; estimates carry [ESTIMATE] into every downstream chart label.

## Revision and backfill

TVL, supply, and volume histories restate. Adapters get rewritten, spells get re-decoded, protocols enter and leave categories, prices get backfilled, chains reorg. A chart pulled today will not match one pulled last month and neither is wrong.

- Snapshot the pulled series to a dated file at pull time. The pull is the artifact, the chart is a rendering of it. Cite the pull date alongside the as-of date; they answer different questions.
- Never compare a fresh pull to an old chart. Re-pull both ends or compare nothing.
- When a series restates, log the delta and the cause instead of silently replacing the old figure, per memory-keeper. Treat the last seven days of any series as provisional, since the recent tail restates most.

## Vendor terms, read live

Plans, prices, rate limits and free-tier terms change without notice, so read the vendor's current pricing or API page before quoting cost or assuming access. Dated observations with no live read yet sit in references/vendor-notes.md.

| Source | Re-check live before relying |
|---|---|
| DefiLlama | Which endpoints the free API at api.llama.fi still covers and which sit behind the Pro API; double count toggles and category definitions |
| Dune | Whether the account's tier can still run queries; Spellbook table re-decodes |
| Explorers and public RPC | Etherscan API V2 free-tier limits and chain coverage; public RPC is unreliable for reads at height, so prefer a paid archive endpoint |
| Token Terminal, Artemis | Which plan carries API or export access; methodology page locations |
| DeFi Brain | Used only when its tools are loaded; get-coverage carries the current gap list, and upstream providers and paywalls shift under it |

Pairs with research-protocol for prose facts and source grading, defi-desk for what the numbers mean, viz-dashboards for the chart, and memory-keeper for the restatement log.
