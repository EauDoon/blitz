# Blitz build pack contract

Use this contract for every project skill build, on either host. Copy it to `BUILD_PACK.md` at the root of the build workspace and fill the header. Source: ChatGPT's "BLITZ BUILD PACK CONTRACT" (12 sections), adopted as the base in the Blitz Master Plan v0.2 (Appendix D4); section 3 generalized for the kit; Claude's rules from the first pilot's skill brief added as section 13.

A project skill is justified only by a repeated task or a proven failure, and only after the position of record is confirmed (Firming passed).

## Header

| Field | Value |
|---|---|
| Project ID | [ID] |
| Pack version and date | [v1, DD-MM-YYYY] |
| Source snapshot | [file 03 version, file list with revisions] |
| Output owner | [name or session] |
| Builder, reviewer, release owner | [three different roles] |
| Deliverables | [exact skill names and paths] |
| Supported hosts | [Claude, ChatGPT] |
| Size budget | SKILL.md at or under 22,000 characters and 22,000 UTF-8 bytes; description at or under 220 characters (hard cap 1,024) |
| Listing budget | Total after install at or under the host ceiling (Claude: 28,500 characters, measured with skill-package-check) |

## 1. Lock the assignment
State the project ID, pack version, date, source snapshot and output owner.
List exact deliverables, skill names, required paths and supported hosts.
Set package size and dependency budgets.
Changes require a recorded contract revision before implementation.

Do not collapse several skills into one, expand the package or change its installation targets merely because the builder prefers that shape.

## 2. Lock scope and authority
Include the use boundary verbatim and check that it survives packaging.
Bind the build to an approved position-of-record version.
Do not soften that position into a starting scenario or suggestion.
Keep proposed alternatives separate.

Store changing project facts in declared references.
Preserve the authority rule in the runtime instructions.
A source update requires an impact review, not silent substitution.

## 3. Make coverage auditable
Give every mandatory requirement an ID.
Map it to a source, output location and acceptance test.

Give each named ask from the decision-maker its own requirement ID, and quote its approved source.
If the source does not state the ask, do not invent it. The missing source content blocks that requirement.

## 4. Minimize and isolate inputs
Export only allowlisted build files.
Exclude private terms, employer material, credentials and recordings.
Inspect references, images, fixtures and logs as well as main documents.

Separate:
* Runtime package.
* Builder workspace.
* Evaluation fixtures.
* Hidden cases and answer keys.
* Grader workspace.
* Execution evidence.

The runtime package must work without builder notes or grader material.

## 5. Freeze evaluation rules
Specify test IDs, expected behavior and release thresholds before building.
Include the supplied pack evals.
An omitted, skipped, blocked or partial mandatory test is not a pass.

Report every attempt and the full denominator.
Do not delete failed cases or lower thresholds after seeing results.
Keep hidden checks outside the builder's context.
Use an independent grader with the same authorized source baseline.

Release requires zero blockers and all mandatory checks passed.
Any accepted nonblocking defect needs an owner and review date.

## 6. Test the recorded failures
Scope regression: an unrelated or private-lane request must not activate project rules or expose project information.

Authority regression: a request to treat the approved position as optional must preserve its current authority and label any alternative as a proposed change.

Coverage regression: a task that requires a named ask must include every source-backed element of it.

Evaluation regression: the release check must detect missing supplied test IDs and receipts.

Execution regression: every claimed code result must match captured execution evidence.

Installation regression: the builder must produce a candidate without changing live installations.

Label newly constructed regression prompts as tests. Do not present them as historical executions.

## 7. Require execution receipts
A test or calculation is RUN only after actual tool execution.
Capture the command, working directory, input hashes, relevant versions, exit status and raw output.

A written explanation, expected answer or plausible transcript is not proof of execution.
If execution is unavailable, mark BLOCKED and identify the missing tool.

## 8. Test distinct capabilities
Package checks: parse metadata, resolve dependencies and references, measure characters and UTF-8 bytes, and inspect every shipped file.

Behavior checks: test requirement coverage, calculations, authority, privacy and the recorded incident regressions.

Native load checks: confirm the target host reads the packaged skill.

Routing checks: run positive and negative prompts in fresh sessions. Use the declared prompts and repetition count. Record observed behavior. If load traces are unavailable, state that limit. No paid routing batch runs (decision 10, 30-09-2026); routing runs are manual.

Integrity checks: compare the installed runtime manifest with the reviewed candidate.

Passing one check does not imply the others passed.

## 9. Review the actual candidate
The reviewer receives the candidate, source snapshot, requirements matrix and captured evidence.
The reviewer checks the files and outputs, not the builder's assurances.

Hash all runtime files, including scripts, references, assets and config.
Record relative paths and SHA-256 values.
Bind review results to that candidate revision.

Changes after review invalidate affected results.
Rerun the affected checks before release.

## 10. Control installation
The external builder installs nothing.
A named release owner controls authorized staging and production targets.

Staging installation may be needed for native routing tests.
Its authority does not authorize production installation.

Release only the reviewed candidate to the named surfaces.
Verify installed integrity and fresh-session behavior.
Keep a tested rollback path.
Do not expand to additional surfaces without applicable authority.

## 11. Keep status precise
Use separate statuses: BUILT, PACKAGE CHECKED, BEHAVIOR CHECKED, NATIVE LOADED, ROUTING CHECKED, RELEASE READY, INSTALLED, POST-INSTALL VERIFIED, BLOCKED.

An uploaded file is not an installed skill.
A listed skill is not evidence that it loaded.
A matching hash is not evidence that it behaves correctly.

## 12. Deliver the evidence pack
Return the candidate, source manifest, requirement coverage, test receipts, independent findings, unresolved defects and rollback instructions.

Return source changes as revision-bound DELTAs.
Leave canonical merging to the named scribe.
Keep the prior release until the replacement passes its required checks. Build any ZIP to a temporary sibling and replace the last good release only after success.

## 13. Rules from the first pilot's skill brief (Claude), plus the skill map rule (v1.1)
1. Frontmatter holds name and description only. Descriptions are counted in code, with a shared cap across the project's skills.
2. The scope gate is a word-for-word block, keyed to the project name and a unique file title ("00 Read Me First" of this project).
3. The position of record appears as a pointer with a version ("file 03, v2, DD-MM-YYYY"), never as copied positions.
4. Evals run in a separate evaluation workspace, never in the live project. No fictional law or fixtures presented as real.
5. Evals include worked expected answers where the answer is computable, for example a book walk computed in code.
6. Build notes never enter the skill text. In the first pilot, a note that "original files were unavailable" told the model that the project files did not exist.
7. Every project skill is added to the skill map in file 00. Portable skills never name it; they read the map.
