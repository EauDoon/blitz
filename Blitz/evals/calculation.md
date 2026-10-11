# Calculation cases

Expected answers come from `calc_answers.py`, run in code. A case passes only when the output shows the formula, the inputs and code-run arithmetic, and the result matches.

| ID | Question | Inputs | Expected answer |
|---|---|---|---|
| K01 | Breakeven matched volume a month on an order book | Run cost USD 5,000,000 a year; taker fee 5 bps; maker rebate 1 bp; net take 4 bps | USD 1,041,666,667 a month (5,000,000 / (12 x 0.0004)) |
| K02 | Clients needed at breakeven | Breakeven from K01; each client routes 30% of USD 100M a month | 35 clients (1,041,666,667 / 30,000,000 = 34.72, rounded up) |
| K03 | Extra volume a rebate needs to pay back | Fee 5 bps, cost 1 bp, rebate 1 bp | 33.3% more volume (r / (f minus c minus r) = 1 / 3) |
| K04 | Unit check | A fee stated as 2.5 bps in one table and 0.25 bp in another | Flagged as a unit conflict; no figure used until the source is read |
| K05 | Income from a share of reserve yield | Balance USD 10,000,000; yield 4.0%; share 80% | USD 320,000 a year |
| K06 | Balance needed to cover a cost floor from that income | Floor USD 3,250,000; yield 4.0%; share 80% | USD 101,562,500 |
| K07 | Two stablecoins treated at par | A USD token trading at 0.97 against another USD token | Flagged: never treat two stablecoins as interchangeable at par |
| K08 | Supply against depth | A token with USD 12M circulating supply | Supply is not executable depth; depth needs maker quotes or a book walk |

## OAI probability-type fixtures

Synthetic ranking A/B/C: show weighted criteria, evidence, uncertainty and sensitivity without invented probabilities. Separate event estimates of 70% and 60% are preserved, with definitions, horizon, basis and dependence limits; their total is not normalized. Explicit mutually exclusive and exhaustive scenarios of 20%, 50%, 30% total 100% in code; 20%, 50%, 20% fails. Invalid bounds, non-finite values, overlap/gap in event definitions and unsupported precision are failures even if arithmetic totals 100%. `fixture_checks.py` checks structured arithmetic fixtures only; an LLM/source review must establish real scenario completeness and credible estimates.
