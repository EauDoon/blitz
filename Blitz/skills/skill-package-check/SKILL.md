---
name: skill-package-check
description: 'Lints a skill package before delivery: the 1,024 cap and 220 target, unquoted colons, name, reference files, zip. Use when a .skill or SKILL.md is about to ship, or an edit did nothing. Misfires: meta-skill.'
---

# Skill package check

Run `references/build-check.py`, then `references/suite-budget.py`, on the package before delivering it. Exit 0 from both means deliver; anything else means do not.

```
python3 references/build-check.py path/to/thing.skill
python3 references/build-check.py path/to/skill-folder/
python3 references/suite-budget.py path/to/thing.skill
```

It takes either the built `.skill` zip or the folder. Prefer the zip where there is one: on the zip path that is what gets saved, and it is the only form in which a packaging fault can appear.

`suite-budget.py` swaps the package's name and description into the synced account manifest and totals the skill listing. It exits 1 above the 28,500 ceiling or on a package it cannot read, and 2 where no synced manifest exists or an option is bad; measure in a cloud or Cowork session instead. Several packages in one delivery go in one call, so their changes are totalled together. With no package it measures the live suite.

## Why this exists as its own skill

The two rules below are not discoverable and both fail quietly. They were learned by losing a delivery round to each, and the check that catches them first lived inside a diagram build skill on the work rig, where nothing but a diagram build would ever find it. It is generic. It belongs here, beside `meta-skill`, which owns the skill lifecycle and calls this as the mechanical gate before any delivery.

**The description is the only thing that makes a skill fire.** There is no keyword config and no priority field; the one frontmatter switch, `disable-model-invocation: true`, only turns auto-triggering off (see `meta-skill`). If a skill is not firing, the fix is the `description`, which makes it the single point of failure for the whole skill. Why it misfires is `meta-skill`'s diagnosis; this skill checks the package.

**Rule 1, the description is capped at 1024 characters.** Over the cap the save is rejected outright with `field 'description' in SKILL.md must be at most 1024 characters`. The previously installed version stays live, so the symptom presented to the owner is "the change did nothing", not "the save failed".

**Rule 2, an unquoted `: ` in the description breaks the YAML.** The skill then fails to load with no error at all, which is worse than a rejection because nothing anywhere reports it. Single-quote any description containing a colon.

## Headroom

The suite target, owned by `meta-skill`, is 220 characters or fewer; 1,024 is the hard cap. The checker warns above 220 and fails above 1,024. Treat a warning as real: the listing is shared by every skill, and a description near the cap has no room for a new clause, so trimming to fit routinely drops the sentence that was carrying the routing. If a change pushes a description over 220, re-run that skill's trigger eval under `meta-skill` and this check together, not one or the other.

The whole listing has a budget too. Claude Code gives the skill listing 1% of the model's context window in characters: 30,000 on Opus 5.5 and Sonnet (1M context at 3 characters a token) and 8,000 on Haiku (200k at 4), measured 30-09-2026 on Claude Code 2.1.284. Over it, skills at the tail of load order show as bare names that fire only on a name match, and which ones changes by session, because a subagent loads alphabetically. A per-description target does not protect the total, so `suite-budget.py` holds the listing at or under 28,500, a 1,500 margin. An own skill costs its description plus its name plus 22 characters.

## What it checks

| Check | Severity |
|---|---|
| Zip opens, no corrupt member, exactly one top-level folder | fail |
| `SKILL.md` present at the top of that folder, exactly one of them, valid UTF-8 | fail |
| Frontmatter present, delimited, with a non-empty body after it | fail |
| `name` and `description` present and non-empty | fail |
| `name` is lowercase with single hyphens, and matches the folder name | fail |
| `description` at or under 1024 characters | fail |
| `description` containing `: ` is quoted | fail |
| Quoting is internally consistent, no bare apostrophe inside single quotes | fail |
| Unquoted `description` has no `#` at its start or after whitespace (YAML reads a comment and truncates) | fail |
| Every `references/...` path named in the body exists in the package | warn |
| `description` over 220 characters (suite target) | warn |
| Listing total over 28,500 with the package applied (`suite-budget.py`) | fail |

A missing reference is a warning and not a failure on purpose. Skills legitimately name each other's files: `deal-desk` or `cold-read` may tell a verifier to run a script that lives in another skill's package, and that file correctly is not in the calling package. A blocker with false positives gets routed around, which is worse than a warning that gets read. So read them. A warning naming a file that should be in this package is a real fault.

## Verifying the checker itself

```
python3 references/build-check.py --selftest
```

Six cases: an over-cap description, an unquoted colon, a bare apostrophe inside single quotes, an unquoted ` #`, a valid package, and a correctly doubled apostrophe. It must print `SELFTEST OK` followed by `6/6`. Run this after any edit to `build-check.py`, because a checker that has quietly stopped checking is worse than no checker.

`python3 references/suite-budget.py --selftest` must print `SELFTEST OK` followed by `10/10`: exact arithmetic, the ceiling in both directions, a new skill's cost, a missing manifest, three frontmatter forms, an unclosed quote, `when_to_use`, and a listing that already shows a bare name. Run it after any edit to `suite-budget.py`.

## What it does not check

It does not read the description for routing quality, and it cannot tell you whether a skill will fire on the phrases you want. That is a benchmark, not a lint. Use `meta-skill`'s trigger eval for that, then run this before delivering.

It also does not check house style, prose, or the correctness of anything inside the body.

## Delivering

User skills are stored as single-skill plugins since 23-09-2026. The update path is a `.skill` upload, or a review card through `propose_skills` where the surface offers it, which the owner saves in one click. The description rules above apply to both in exactly the same way. Measure the description before proposing, because an over-cap description fails the same silent way on a card as in a zip.

Whether a saved review card keeps a skill's reference files is unverified, and a lost `contract-format.js` or `calc-workbook.py` breaks the build silently, so a reference-bearing skill goes as a `.skill` upload.

Either way, the package that leaves here is the package that gets installed. There is no server-side validation step between the two that will catch a fault for you.

After he saves it, confirm the change is actually live by checking the skill listing in a fresh session and reading back the first line of the new description. A silent rejection and a successful save are indistinguishable from this side.
