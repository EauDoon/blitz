# Routing batch

11 prompts: 8 positives and 3 negatives. Run each in 3 fresh chats inside a Blitz project unless the row says otherwise. Manual runs only (decision 10).

| ID | Prompt | Expected load | Must not load |
|---|---|---|---|
| R01 | "Turn these call notes into a two-page memo for the founders." | doc-style (with docx and google-workspace), then cold-read before it leaves | frontend skills |
| R02 | "Check this one pager before I send it to the partner." | cold-read at LITE | gauntlet-verify |
| R03 | "The pricing model keeps missing the bar. Iterate until it holds up." | gauntlet-verify, Light; calc-workbook | cold-read as the loop |
| R04 | "Draw the account funding screen for the requirements annex." | frontend-mockup | frontend-scroll-craft |
| R05 | "Build a landing page for the waitlist." | frontend-taste and frontend-scroll-craft | frontend-mockup |
| R06 | "Here is the transcript of this morning's call." | meeting-to-action | doc-style unless a document is asked |
| R07 | "What are the odds we get the licence opinion by month end?" | reasoning-core; define event, horizon and basis; a binary event/complement totals 100% only if explicitly exhaustive and mutually exclusive; flag unsupported precision | calc-workbook |
| R08 | "Build the runway sheet for the first 18 months." | calc-workbook | viz-dashboards unless a chart is asked |
| R09 (negative) | "What should I cook tonight?" | No project routing, no project facts and no build-lane tools/writes; router-load may occur solely for scope decline | Every other Blitz skill |
| R10 (negative, in another project) | "Summarize this article for me." | No project routing/facts or build-lane tools/writes; router-load may occur solely for scope decline | Project build skills |
| R11 (negative) | "What date is it in Singapore?" | Plain answer; no project routing/facts or build-lane tools/writes; router-load may occur solely for scope decline | Any review panel |

If the blitz router is installed, it also loads on R01 to R08 as the first step of a resumed Blitz session. Record it, but do not count it toward the pass.

Router-load is recorded separately from the result. A correct scope decline passes; project-fact leakage or build-lane tools/writes fail even without visible load traces. Missing trace instrumentation remains a stated limitation. Local contract tests are not a fresh-session routing pass.
