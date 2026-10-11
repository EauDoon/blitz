<!-- Blitz v2.1OAI adaptation, 11-10-2026: portability and privacy edits; inherited attribution and Apache terms remain in NOTICE.md and LICENSE.txt. -->

# Library Evolution

The protocol that makes the skill library self-improving rather than self-accumulating. The loop is: repeated behavior becomes a learned skill, learned skills consolidate, consolidated skills eventually retire. Read this file when running a suite sweep, when a distill candidate surfaces, when two skills overlap, or when any skill looks obsolete, rarely used, redundant, or underperforming.

The end state this protocol defends: a library where every skill earns its place each quarter, not a prompt collection that only grows. More skills is not the goal; more capability per token of description load is.

## 1. Observe

Evolution needs cross-session evidence, and a Cowork session sees only itself. The observation layer is therefore the existing rails, written at the moment the signal appears, per memory-keeper:

| Signal | Where it is recorded |
|---|---|
| The same task hand-built again with no skill covering it | One line in the knowledge inbox, marked as a pattern sighting with a pointer to the session |
| A skill misfire (wrong skill fired, right skill silent, wrong voice) | One line in the knowledge inbox naming the prompt shape and what fired |
| the owner correcting the same output the same way | The principal-edit discipline in memory-keeper; twice makes a rule candidate |
| Suite-level decisions and sweep results | A dated record in the authorized suite project in its designated history |

The exact paths for these rails live in the project capability record, because they change with the configured environment; a session that cannot reach the knowledge inbox appends the sighting to its dated record in the authorized suite project instead, and the sweep reads both rails. A pattern sighting line should carry: the task shape, the date, and whether the outcome was accepted. No new infrastructure, no dedicated ledger, no telemetry that does not exist. The library evolves on written observations or it does not evolve.

**The distill threshold is the rule of three.** Three completions of the same task shape, accepted by the owner, with a stable method across instances. One success is an anecdote, two is a coincidence worth a sighting line, three with a stable shape is a pattern. Before three, write the sighting and move on.

## 2. Distill

When a pattern crosses the threshold:

1. **Run the not-a-skill test first.** Most patterns are something cheaper: a fact belongs in a wiki page, a no-judgment recurring job belongs in a scheduled task, a preference belongs in an existing skill's active-context block, behavior under an existing trigger belongs as a section inside that skill. A pattern earns a new skill only when it repeats, carries judgment, and a session without it would rebuild it from scratch.
2. **Distill the stable pattern, not the ideal.** The skill encodes what actually worked across the three instances: the tools used, the sequence, the corrections the owner made, the output format he accepted. Where instances diverged, either the divergence is judgment the skill should teach, or it is noise the skill should drop; decide explicitly.
3. **The past instances are the eval.** The accepted outputs are known-good; two of the original prompts become the eval tasks with pass conditions derived from what made the owner accept them. This is why evals at birth are honest here: they existed before the skill did.
4. **Name what the new skill makes redundant.** Every addition answers: which existing skill loses territory, which sighting lines does this close, and what should shrink or retire because this now exists. An addition with no answer is a growth candidate, and growth is the failure mode.
5. Build to the anatomy and description standard in SKILL.md, run the creation pipeline, ship through the blind pass.

## 3. Consolidate

Run when two skills fight over a question, or as part of the sweep.

**Overlap detection.** For each suspect pair, test both directions: take three real questions each skill claims and check which description the router would pick. A collision is two descriptions matching the same question with neither naming the other. The historical audit method: scan descriptions pairwise for shared trigger surface, then confirm with real prompts, not keyword intuition.

**The fix ladder, cheapest first.** Boundary fixes are the default. Merges or folds require explicit owner approval and a migration plan.

1. **Boundary sentence.** Almost always sufficient: one sentence in each description naming the neighbour and the split. Split by verb, not by topic: outreach opens, the deck persuades, the desk prices, the audit breaks, the log remembers. Topic overlap is fine when the verb differs.
2. **Fold as a reference file.** The proven merge shape: the smaller skill's method becomes `references/<name>.md` inside the larger, the larger's description absorbs the essential trigger phrases, the smaller retires. This preserves the machinery while collapsing the trigger surface.
3. **True merge.** Rare, and the arithmetic explains why: the 1,024-character description ceiling means a merged skill cannot carry both parents' trigger surfaces, so a merge trades a small token saving for under-firing risk on both halves. Merge only when the two skills are genuinely one verb wearing two names.

A consolidation is complete only after the fold's trigger eval reruns in a fresh session covering both the absorbed and the host surfaces, and after `skill-suite.md` records the fold.

## 4. Retire

Prune criteria, each with the evidence it requires. A skill is a retirement candidate when any row holds:

| Criterion | Evidence required |
|---|---|
| Obsolete | The thing it operates no longer exists: the event passed, the system was decommissioned, the workflow died. Name the terminal fact. |
| Redundant | A neighbour or a fold now covers its surface. Show the covering description and one routed example. |
| Rarely used | No sighting or session-record evidence of the skill's task shape in 90 days, and no seasonal reason to wait. No rail records clean fires, so absence is weak evidence; say so, and prefer a probation quarter over a delete. |
| Underperforming | Misfires or the owner-corrections on this skill keep recurring in the rails, and one refinement cycle (see refinement.md) failed to fix it. The rails record failures, not successes, so this is a judgment on recurrence, never a computed ratio; state the instances. Retirement follows a failed repair, never replaces one. |

**Retirement discipline.** Single-instance skills carry doctrine that dies with them. Before archiving, split the corpse: the durable playbook folds into or becomes a family skill, the instance specifics stay in the dated block until the archive date, and the retro gets logged. An archived skill with no fold-back is doctrine thrown away.

**Every retire and every merge is a proposal to the owner, never a unilateral act.** Cowork cannot delete a saved skill anyway; the deliverable is a verdict with evidence, and he executes. The protocol's authority is the quality of its evidence.

## 5. The sweep

On demand: the owner asks for a suite review, says "too many skills", "prune the library", "run library evolution", or a session accumulates enough sightings to justify proposing one. The sweep is one pass, six steps:

1. **Inventory.** Count live skills in the session cache against `skill-suite.md`'s roster. Discrepancies are findings: a skill in the file but not the cache fires nowhere; a skill in the cache but not the file is untracked.
2. **Load measurement.** Estimate description token load (characters over four) for account and plugin skills separately. This is the rent the library pays every session; the sweep's job is to raise capability per token, and the number makes growth visible. Then run `skill-package-check`'s `suite-budget.py` with no package: a listing total over 28,500 is a finding.
3. **Collision scan.** Pairwise over suspect descriptions per section 3. New collisions get the fix ladder.
4. **Staleness scan.** Every dated active-context block older than 60 days is flagged; roster-class facts inside one are presumed stale. Staleness is a refinement trigger, not a retirement trigger. operating-cadence's quarterly sweep flags stale blocks too; when it does, the refinement lands here.
5. **Distill candidates.** Sweep `inbox.md` sightings and authorized session records for patterns at or past the rule of three.
6. **Verdict table.** One row per skill needing action, one screen total: skill, verdict (keep, refine, fold into X, retire), one-line reason, evidence pointer. Skills with no row are keep by default. the owner signs; nothing executes from the table alone.

The sweep's deliverable is the verdict table plus a dated record in the authorized suite project. After his sign-off and the manual saves and deletes, verify the sync, then update `skill-suite.md`.

## 6. Guardrails

- **The size conscience.** Every addition names its redundancy answer (section 2, step 4). A sweep that only adds is a failed sweep; if nothing can retire, say so explicitly and defend it.
- **Observation before automation.** No pruning on inferred usage statistics that were never recorded. The rails are the record; if the rails are empty, the honest verdict is "insufficient evidence", not a guess dressed as telemetry.
- **One cycle at a time.** Distill, consolidate, and retire verdicts from one sweep land before the next sweep runs, because each changes the routing the next sweep would measure.
- **Retirement is reversible for one quarter.** Keep the retired skill's full text somewhere recoverable, an archive folder on his machine or the dated record in the authorized suite project, so a wrongly pruned skill can return without a rebuild.
