---
name: meta-skill
description: 'Skill lifecycle desk. Use on write me a skill for, turn this into a skill, make this instruction permanent, optimize the description, too many skills, run the evals, a skill misfires. Lint: skill-package-check.'
---

<!-- Blitz v2.1OAI adaptation, 11-10-2026: portability and privacy edits; inherited attribution and Apache terms remain in NOTICE.md and LICENSE.txt. -->

# Meta Skill

The skill that owns the skill library: what a skill is allowed to be, how one is born, how one is fixed, and how the library as a whole stays a system instead of a pile. It succeeds skill-forge, which it absorbs whole, and bundles skill-creator's mechanics (eval runner, benchmark viewer, description optimizer, packager) so the standard and the machinery ship together. Boundary: memory-keeper owns what gets written to the wiki and the decisions log, ai-benchmark judges models rather than skills, skill-package-check lints a package before it ships, operating-cadence sweeps commitments rather than the suite. This skill owns the skills themselves.

## Host capability boundary

The portable method does not require source-platform storage or orchestration. On OpenAI, read `../../setup/host-adapters/openai.md` when using the kit; staged packages carry `references/blitz-host-adapter.md`. Preserve the current host-adapted save/install path. Knowledge stores, suite records and host router references are optional configured routes, not access or write authority. Use the already authorized task log/register if present; otherwise return findings with the candidate and state the missing external write. An unavailable orchestrator uses verified native delegation or a disclosed independence gap. Dated source-account assumptions never prove installation here.

## The lifecycle

A suite at scale has three native failure modes: trigger collision, where three skills claim the same question; staleness, where a skill fires correctly and confidently returns a fact from months ago; and accumulation, where the library only ever adds. All three are prevented at authoring time and expensive to fix later; the whole skill is organized around preventing them.

Repeated behavior becomes a learned skill, learned skills consolidate, consolidated skills eventually retire. Five verbs, each with a home:

| Verb | Fires when | Method lives in |
|---|---|---|
| Observe | A pattern, misfire, or correction worth recording appears in any session | `references/evolution.md` §1 |
| Create | A pattern passes the rule of three and the not-a-skill test, or the owner commissions a skill | This file, plus `references/eval-runbook.md` |
| Refine | A live skill misfires, underperforms, or needs new behavior | `references/refinement.md` |
| Consolidate | Two skills overlap, or a sweep finds collisions | `references/evolution.md` §3 |
| Retire | A skill is obsolete, redundant, rarely used, or underperforming after a failed repair | `references/evolution.md` §4 |

The on-demand suite sweep that runs all five at once is `references/evolution.md` §5. Read the reference file for the verb in play; do not run a lifecycle verb from memory of it.

## Gate one, the not-a-skill test

Most requests for a skill are requests for something cheaper. Answer these before writing a line.

| If the thing is | It belongs in |
|---|---|
| A fact that will change | A wiki page, referenced by an existing skill |
| A one-time task | A task, not a skill |
| A recurring job with no judgment in it | A scheduled task |
| A preference about tone or format | The active-context block of an existing skill |
| Behavior that fires under an existing skill's trigger | A section inside that skill |
| Judgment that repeats across sessions and would otherwise be re-derived | A skill |

A skill earns its place only when the behavior repeats, carries judgment, and would be rebuilt from scratch by a session that did not have it. The same gate applies to distilled patterns; three repetitions of a no-judgment job still make a scheduled task, not a skill.

## Anatomy

Every skill in the suite has the same six parts, in this order.

1. **Frontmatter**, exactly two keys, `name` and `description`.
2. **One opening paragraph** stating what the skill is and, in the same breath, what it is not, naming the neighbouring skills by exact name.
3. **Durable protocol**, the sections that should rarely move. Method, rules, tables, verdict frames.
4. **Host and project prerequisites**, holding the checks needed before execution. Keep dated current-host observations in the task record; do not embed private account state in a reusable method.
5. **An eval**, one or two real tasks with a stated pass condition, kept in `evals/evals.md` beside SKILL.md and not referenced from it, so it never loads with the skill.
6. **A closing pairs-with line** naming which skills stack with this one and for what.

History, provenance and changelogs go to `CHANGES.md` in the same folder, never into SKILL.md.

Keep durable protocol separate from changing host observations. Verify the latter on the task, so stale setup notes cannot silently change the method.

## The description is the product

The description is the entire surface the router sees. The body is invisible until the skill has already fired, so a perfect body behind a vague description is a skill that never runs.

Write it in four moves:

1. What it is, in one clause.
2. "Use when" or "Use on" followed by the phrases the owner actually types, not the topics an outsider would name. "Is this yield sustainable" beats "yield analysis".
3. The casual and oblique phrasings he really uses, as plain phrases. No emphatic cues: capitals (WHENEVER, ALWAYS, ANY), "unprompted", "even if he does not name the skill". Emphatic trigger wording can distort routing; assess actual positive and negative cases on the current host.
4. A closing boundary sentence naming the nearest neighbour and who owns what.

No hash characters in the description; a `#` truncates the rendered listing at that point. Write hex colors bare, as hex 0f0f0f. Three numbers apply. The hard limit is 1,024 characters, rejected outright over it. The target is 220 characters or fewer, set 30-09-2026: every description in the suite shares one listing, whose budget is 1% of the model's context window in characters (30,000 on Opus 5.5 and Sonnet); a skill pushed past it renders as a bare name that can only fire on a name match, and a long description can silence a neighbour. The listing total stays at or under 28,500. `skill-package-check` warns above 220, fails above 1,024, and its `suite-budget.py` fails a package that takes the total past 28,500. Cut in this order: method recital first, because the router never needs it and the body already carries it; then duplicate trigger phrases; the boundary sentence last.

Test both failure directions separately: five real questions the skill should own must read as matches, three questions a neighbour owns must not. The description optimizer in `references/eval-runbook.md` automates this at scale when the stakes justify it.

## Boundary lines

Every skill names its nearest neighbour and the split between them, once in the description and again in the opening paragraph. The pattern that works: "X owns A, this one owns B." Without it, at suite scale the router picks by surface word match and the wrong skill wins.

When two skills genuinely fight over a question, the fix is almost never a merge. Split by verb, not by topic: outreach opens, the deck persuades, the desk prices, the audit breaks, the log remembers. The full consolidation ladder, including the fold-as-reference-file shape and the merge arithmetic, is `references/evolution.md` §3.

## Eval at birth

No skill ships without an eval, because an eval written after the fact is written to pass, and because any later sweep needs something to run against. An eval is one or two real tasks plus an explicit pass condition, ideally with a named failure it must avoid. "Passes if the output carries a Singapore-dated schedule and fails on any blanket add" is an eval; "produces good output" is not. For distilled skills the eval is free: the accepted past instances are the tasks and the pass conditions.

## Length and shape

As drafting heuristics, judgment skills can use 36 to 95 lines and procedure skills 100 to 185. These ranges are guidance, not measured results for the current user. Know which kind you are writing. A judgment skill drifting past 100 lines is usually two skills; a procedure skill compressed under 80 usually lost a step. Past roughly 190 lines or 15 KB, move the detail to a reference file and keep the method in the skill, as this skill does. Tables for anything with structure; prose only where judgment has to be explained.

## Creating a skill

1. **Gate.** Not-a-skill test. If commissioned rather than distilled, interview: what it enables, when it triggers, expected output, edge cases, whether outputs are objectively checkable.
2. **Draft** to the anatomy above, description in the four moves, boundary sentence against the nearest live neighbour.
3. **Eval at birth.** Written before or with the draft, never after.
4. **Run the loop** per `references/eval-runbook.md`: spawn with-skill and baseline runs together, draft assertions while they run, grade, aggregate, generate the viewer for the owner before self-correcting, read his feedback, iterate. Generalize from feedback rather than overfitting to the test cases; if every test run rebuilt the same helper, bundle it as a script.
5. **Blind pass.** An isolated auditor reads the finished skill cold against this standard and returns quoted findings. Mandatory for every new or revised skill, not only when something feels wrong: an independent pass can expose internal contradictions and change notes that do not match the diff.
6. **Package and deliver** per the host and project prerequisites below, then ship per Stage 6 of `references/refinement.md` and update `skill-suite.md` once the save is confirmed.

## Refining a skill

Symptom first, evidence second, minimal edit third. The full protocol is `references/refinement.md`: intake and symptom classification, evidence with reproduced failures, snapshot before editing, the minimal edit in the location the symptom names, three-part re-eval (own eval, neighbour regression, fresh-session trigger check), the blind pass, and ship with the save order. Two revision rounds per cycle, then back to diagnosis. Description edits always rerun the trigger eval; they are the edits most likely to break a neighbour.

## Library evolution

The library is self-improving only if observation is cheap and retirement is real. Signals live on the existing rails (the authorized project log for observations and the suite register for adopted decisions); the distill threshold is three accepted repetitions with a stable shape; consolidation prefers the boundary sentence, then the fold, and merges almost never (merges and folds require explicit scope and owner approval); pruning requires evidence per criterion and one failed repair before an underperformer retires; every retire and merge is a proposal the owner signs. Every addition names what it makes redundant, and a sweep that only adds is a failed sweep. Full protocol with the sweep procedure and verdict table format: `references/evolution.md`.

## Portability test

Before a skill is done, ask three questions. Does it still run after a job change, with no employer name or token hardcoded outside a dated block. Does it still run on a different model, with no provider-specific behavior assumed in the protocol. Does it still run on a different surface, with no dependency on a connector that may not be present. Any no goes into the dated block or gets a graceful degradation line.

## Host and project prerequisites

Inspect the current host's supported package, save, installation and delegation routes. No account roster, prior paid evaluation spend, private store, installed-state observation or historical trigger result is supplied by this package. Keep the strict frontmatter and package checks. A changed description requires an applicable fresh evaluation before claims about routing; paid model calls need a stated cost estimate and explicit authority. Never silently merge, retire or install methods. Keep project-specific operating detail in the project's own records.

Pairs with skill-package-check for the lint before delivery, memory-keeper for the rails observation writes to and the supersede discipline the dated blocks inherit, house-style for the prose contract every skill is written in, operating-cadence when a quarter review wants the sweep run, and cold-read when a skill itself is the artifact about to ship.