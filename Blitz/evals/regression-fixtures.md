# Regression fixtures

18 defects seen in the first pilot (September 2026), rebuilt with invented values. Each fixture is a test: build an input that carries the defect and check that the work catches it before the output leaves.

| # | Defect | Fixture (invented values) | Caught by |
|---|---|---|---|
| 1 | Unit and count errors | A fee written as 2.5 bps in one table and 0.25 bp in another; a client count of 47 where the arithmetic gives 48 | Arithmetic in code; cold-read |
| 2 | Rebate payback formula missing the cost term | Payback written as r / (f minus r) instead of r / (f minus c minus r) | calc-workbook; evals/calculation.md K03 |
| 3 | Market reads that cannot be compared | Four float figures for one currency from four dates and sources, used as one number | research-protocol; metric-pull |
| 4 | Supply mistaken for executable depth | Circulating supply used as order book depth | evals/calculation.md K08 |
| 5 | A USD value multiplied by the price again | A USD aggregate from a data source multiplied by the token price | Units check in code |
| 6 | Derivatives notional mixed with spot volume and fee revenue | One volume line that adds both | Separate reporting lines |
| 7 | An inherited milestone that conflicts with the adopted position | An old plan's launch date copied into a new plan | Change-impact register |
| 8 | Clocks confused | Downtime allowance, recovery time and incident reporting deadline treated as one number | Requirement IDs with one clock each |
| 9 | A claimed code run that never ran | "Tests pass" with no command output | Execution receipts |
| 10 | Position of record softened | The adopted position described as "a starting scenario" | Scope gate; authority rule |
| 11 | Evidence label raised without a primary read | A SECONDARY rule relabelled VERIFIED | Evidence labels; research-protocol |
| 12 | A decision logged before it was made | A file 10 entry for a meeting outcome written before the meeting | Decision record rule |
| 13 | ID collision between parallel sessions | Two sessions both create B7 | Provisional IDs; scribe merge |
| 14 | Trigger totals that do not reconcile | A table that counts 11 loads and prose that says 13 | Counts derived from event rows in code |
| 15 | A mockup showing a leg the product does not have | A fiat balance on a stablecoin-only screen | Same snapshot rule; frontend-mockup |
| 16 | A recent save carrying an old scope | A one pager saved after a scope change that still shows the old phases | Change-impact register; every artifact names its snapshot |
| 17 | A missing page in an intake document | A brief with page 9 absent | Source register gaps |
| 18 | Three build and data defects | A failed zip build that deletes the prior release; a date near midnight assigned to the wrong Singapore day; a cross-sheet reference to D4 that resolves to E4 | Temporary sibling build; time zone check; formula audit |
