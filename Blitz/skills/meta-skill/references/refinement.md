<!-- Blitz v2.1OAI adaptation, 11-10-2026: portability and privacy edits; inherited attribution and Apache terms remain in NOTICE.md and LICENSE.txt. -->

# Refinement Protocol

The structured method for improving an existing skill. Read this whenever a live skill misfires, underperforms, gets new requirements, or the owner says fix, improve, tune, or "it keeps doing X". The method is deliberately heavier than the edit itself, because a careless revision is how a working suite rots: the skill still fires, still sounds confident, and is now wrong.

Two principles govern every stage. Revision, not rewrite: the symptom names the fix location, and everything else is left alone. Evidence before edit: no change ships on a feeling; it ships on a reproduced failure and a passed re-eval.

## Stage 0. Intake

Write the symptom in one sentence before touching anything. "It never fires on X", "it fired on deal-desk's question", "it cited a stale rate", "the method gave the wrong answer on Y". If the symptom cannot be written in one sentence, it is two symptoms; run the protocol twice.

Classify with the symptom table. The fix location is almost fixed by the symptom:

| Symptom | Fix in |
|---|---|
| Never fires, or fires late | Description, trigger phrases |
| Fires on a neighbour's question | Description, boundary sentence |
| Right skill, wrong voice | house-style, or a tone line in the opening paragraph |
| Right method, wrong facts | The dated active-context block |
| Method itself is wrong | The protocol, and log the reason as a decision |
| Model wastes time on unproductive detours | Cut the section causing it; leaner beats longer |
| Same helper rebuilt in every run | Bundle it as a script in `scripts/` |

Protocol edits are the rare case. A skill whose protocol moves on every revision never had the right protocol; say so and consider a redesign instead of another patch.

## Stage 1. Evidence

Collect the actual failing instances: the prompt, what fired, what it produced, what should have happened. Quotes, not summaries. Reproduce the failure once if it is cheap to do so. Then write the failure as a falsifiable claim: "given prompt P, the skill does X; after the fix it should do Y." That sentence becomes the regression test for stage 4.

the owner's own edits to skill output are first-class evidence. A correction he made once is a data point; the same correction twice is a rule candidate. An inconsistent pair of edits gets flagged back to him, never silently absorbed.

## Stage 2. Snapshot

Before any edit, copy the current skill to a `skill-snapshot/` directory in the workspace. This is the baseline for the with-skill versus old-skill comparison and the rollback if the revision makes things worse. Preserve the skill's name and directory name exactly; a revised skill ships under its original identity, never as `-v2`.

## Stage 3. Minimal edit

Make the fix in the location stage 0 named, and only there.

- Trigger and boundary fixes live entirely in the description. Recount the characters after editing; the hard limit is 1,024 and the target is 220 or fewer, per SKILL.md. Trim trigger phrases before trimming the boundary sentence.
- Fact fixes go into the dated active-context block, supersede style: the new fact enters, the old one is marked superseded, the block date is bumped.
- Protocol fixes get one more test before they land: explain why the method was wrong, not just what the new method is. If the why cannot be stated, the fix is a guess.
- While in the file, resist the adjacent tidy-up. Unrequested edits widen the diff, invalidate the eval comparison, and hide which change actually mattered.

## Stage 4. Re-eval

Three checks, scaled to what was touched.

1. **The skill's own eval.** Run the skill's eval tasks against the revised version, with the stage 2 snapshot as baseline, per `eval-runbook.md`. The stage 1 falsifiable claim is added as an assertion. Many older skills carry no `evals/evals.md`; when the skill under repair has none, write its eval now, from the failing instance plus one known-good instance, before the fix ships. The eval debt is itself a finding worth logging.
2. **Neighbour regression.** If the edit touched the description or boundary, test both failure directions: five real questions this skill should own, three questions the nearest neighbour owns. All eight must land correctly. A description edit that fixes under-firing by capturing a neighbour's traffic is a failure, not a fix. Note the tooling's limit: the bundled description optimizer tests a description in isolation, so it measures match and false-match but never which of two live skills wins a contested prompt; that head-to-head can only be judged in a fresh session with both installed.
3. **Fresh-session trigger check.** Description edits change routing, and routing can only be judged from a session that has not already loaded the skill. Rerunning the trigger eval in a fresh session is part of the revision, not an optional follow-up; a revision whose trigger eval has not rerun is not done, it is deployed untested.

Cap revision at two rounds per cycle. If two rounds of edit and re-eval have not cleared the symptom, stop patching: the diagnosis is wrong, and the next move is back to stage 0 with the new evidence, or a redesign decision for the owner.

## Stage 5. Blind pass

Before shipping, an isolated auditor reads the revised skill cold: no build context, no chat history, just the artifact and the standard. It checks internal self-consistency as a distinct failure mode from being wrong about the world, because the author cannot see contradictions in his own structure. Check both internal consistency and whether the change record matches the actual diff. The auditor gets the diff and the whole file, and returns quoted findings. Fix-before-ship findings get fixed; cosmetic ones get judged.

## Stage 6. Ship

Deliver as a `.skill` upload, or as a review card through `propose_skills` where the surface offers it (a skill with reference files goes as `.skill`, because card handling of reference files is unverified). Run `skill-package-check` first. Report it delivered, not saved, until a later session confirms it in the synced listing, and state the save order: the owner saves the revised skill, a later session confirms it appears in the synced cache (the delivering session's cache does not refresh), then any replaced skill is deleted by hand. The configured suite register updates only if the roster changed; a content or description change updates nothing there. If the protocol moved, append the reason to the decisions log per memory-keeper. A skill reported as installed but absent from the sync fires nowhere; verify the sync before trusting the revision is live.
