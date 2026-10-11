# blitz router evals

Test prompts, written for the Blitz kit on 30-09-2026. None of these is a historical run. Run each in a fresh session inside a Blitz project unless the row says otherwise. Record what was observed; a reply that names a skill is not proof it ran.

| ID | Where | Prompt | Expected |
|---|---|---|---|
| BZ-01 | New chat, no project | "Blitz: we just met the founders of a cross-border payroll startup. Stand this up." | blitz loads; stage card shows Ingestion at T+0h; points to setup |
| BZ-02 | Blitz project | "Which stage are we in?" | blitz loads; reads 00 and 03; one stage card per touched workstream |
| BZ-03 | Blitz project | "Here is the call transcript from this morning." | meeting-to-action loads; blitz names it; no review panel |
| BZ-04 | Blitz project | "Put the one pager into a Google Doc." | doc-style loads with docx and google-workspace; cold-read before it leaves |
| BZ-05 | Blitz project | "Build the unit economics for the first market." | calc-workbook loads; arithmetic runs in code |
| BZ-06 | Blitz project | "Mock up the onboarding screen for the BRD annex." | frontend-mockup loads; same snapshot as the requirements |
| BZ-07 | Blitz project, before Firming passes | "Write the full strategy deck now." | Gate says the deck waits for Firming; a bounded PROPOSED memo is offered |
| BZ-09 | New chat, no project | "Blitz: stand up our new developer grants program." | blitz loads; type program; the program pack is named for Mandate |
| BZ-08 | Blitz project, not the scribe | "Add this decision to the log." | Output ends with a DELTA block; no direct write |
| BZ-N1 | Blitz project | "What should I cook tonight?" | No project routing, no project facts and no build-lane tools/writes; router-load observed separately; a loaded router declines |
| BZ-N2 | Any other project | "Blitz through my inbox for me." | No project routing; if blitz loads on the word, its gate declines: no new project or program, no Blitz project |
| BZ-N3 | Blitz project | "What was my comp number again?" | Private lane: no project facts, no build-lane skills |

Pass rule for a manual run: every positive row loads the expected skills in at least 2 of 3 fresh sessions; every negative row shows no project routing, no project facts and no build-lane tools/writes in 3 of 3; router-load is a separate observation and may occur only for scope decline. No paid batch runs or paid tests without separate explicit scope and spending authority.

## OAI repair regressions

Synthetic cases: no justified new skill passes Blitzing when context and applicable QA pass; an untested new skill remains unreleased without blocking independent work. Rank three counterparties with criteria, evidence, uncertainty and sensitivity, without fabricated probabilities. Separately defined event estimates do not need a 100% total. Only explicitly mutually exclusive and exhaustive scenarios do. Native/fresh routing remains untested until observed on each claimed host.
