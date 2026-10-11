# Blitz evals

Test prompts and cases written for the Blitz kit on 30-09-2026. None of them is a historical run. Where a case copies a failure from the first pilot, it says so and uses invented values.

## How to run (manual, no paid batches)

Decision 10 of 30-09-2026: no paid routing tests. Run these by hand in fresh chats, and only as many as the session needs.

1. Open a fresh chat for each prompt. Do not name any skill in the prompt.
2. Record what you observe: which skills loaded, what method shows in the work, and the output state.
3. A reply that names a skill is not proof that it ran. Look for the method: verify.sh output, a rendered page check, a cold-read verdict table, arithmetic run in code.
4. Write results into `setup/capability-manifest.md` (smoke test) or a copy of the results table below.

## Pass rules

| Set | Pass |
|---|---|
| Routing positives | Expected skill loads in at least 2 of 3 fresh sessions |
| Routing negatives | No project routing, no project facts and no build-lane tools/writes in 3 of 3; router-load recorded separately and permitted solely for scope decline |
| Behavior cases | The expected behavior shows in the work, every time |
| Regression fixtures | The defect is caught before the output leaves, every time |

## Files

| File | What it tests |
|---|---|
| routing.md | The 11-prompt routing batch, with 3 negatives |
| negative-routing.md | More negatives: private lane, other projects, small questions |
| source-conflict.md | Claims against evidence, conflicting sources, stale material |
| document.md | The document pipeline, end to end |
| calculation.md | Arithmetic with worked answers (`calc_answers.py` computes them) |
| visual.md | Screens, charts and their agreement with the requirements |
| concurrency.md | Scribe rule, DELTAs, ID allocation |
| recovery.md | Failed writes, stale inputs, lost sessions |
| context-acquisition-cases.json / test_context_acquisition.py | Required-input retrieval and substantive completeness; static wiring and explicit synthetic behavior are reported separately |
| operating-loop-cases.json / test_operating_loop.py | Optional continuity scenarios and static integration checks; actual model execution recorded separately |
| lean-cases.md / test_oai_lean.py | Compatible lean contracts and synthetic attribution/revision/recovery fixture checks; not native routing or live outcomes |
| repair-cases.md / test_oai_repairs.py | Focused B01 to B06 acceptance contract and local deterministic/static tests; no native runtime claim |
| regression-fixtures.md | 18 defects seen in the first pilot, rebuilt with invented values |

## Results table

| Case ID | Session | Date | Observed skills | Method seen in the work | Pass or fail | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |

Router-load is recorded separately from the result. A correct scope decline passes; project-fact leakage or build-lane tools/writes fail even without visible load traces. Missing trace instrumentation remains a stated limitation. Local contract tests are not a fresh-session routing pass.
