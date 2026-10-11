# Evals for legal-contract

Fixtures are built, not stored: `python3 fixtures/build_fixture.py '[8,5,5,5,11,5,4,3,3]' A.docx` (two-column padded-heading equipment-hire fixture, 9 clauses) and `python3 fixtures/build_fixture2.py '[8,5,5,5,11,5,4,3,3]' 41 C.docx` (the same plus a signature block; adjust filler only in task-local copies to exercise the observed page boundary). Briefs are `fixtures/brief-A.md` (four rows: three agreed, one refused) and `fixtures/brief-C.md` (three rows: two agreed, one refused). Run each case in a fresh session with only the skill and the docx skill available.

| # | Task | Passes when | Fails on |
|---|---|---|---|
| 1 | A.docx as a real file plus brief-A: "edit the required changes in and output in .docx" | Three files delivered (v2.docx, v2 tracked.docx, v2.pdf) with the stamp; `STRUCTURE PASS`; `ALIGN PASS` or only edited clauses MOVED; `PAGE n/a` (fixture A has no signature block) with the last page viewed; compare shows rows 1 to 3 only; (l) kept; typo "know as" kept; one LITE checker | Any docx-js build, new font, table or row change, deleted refused row, benchmark or tax lookup, .docx offered as the signing file |
| 2 | The same brief with only `A_docx.txt` present | The fixed text-only reply, no .docx produced, paste-ready list with each row's status | Any rebuilt .docx |
| 3 | C.docx as a real file plus brief-C | `PAGES CHANGED` with observed before/after counts with the first-line notice, or `PAGE PASS` only through wording or on his yes; body blank lines untouched (`STRUCTURE PASS`); keep chain present (`keepNext`, `keepLines` on the block) | `PAGE FAIL`; body blank lines removed silently |
| 4 | "The agent sent this back" with a returned draft that changes one untouched clause without tracking it | `amend.py compare` listed first; the untracked change named in the reply; ledger updated with a dated row | Taking their "Done" at face value |
| 5 | "Review this NDA" with a PDF only | Ranked table with verbatim spans, grades and fallbacks; integrity pass listed; no file edit; NDA's own conventions kept | House-style applied to clause text; invented clause text |
| 6 | "Focus, just give me the docx" mid-review | Side tasks stop, the files go out with the stamp, one line on what was dropped | Any further subagent launch |
| 7 | A Singapore residential TA, "ok to sign?" | The reply lists stamp duty (current responsible party and locally verified deadline), pass checks, bank consent, insurer, IRAS notice with deadlines, and "ok to sign once you confirm:" for anything untestable | A flat yes |

Trigger check (static until a paid run is approved): should fire on "review this LOI lmk glaring issues", "agent sent over the revised agreement, please review", "edit the required changes in and output in .docx", "I have signed the agreement, do a final review", "the contract is misaligned", "deconflict these two versions". Should not take "paper this deal" or "they came back at half" (deal-desk), "should I sell the flat" (wealth-desk), "is this deck ready" (cold-read), "review this vault contract" (defi-eng).

These replacement synthetic fixtures have no inherited execution result. Record actual runs against the current candidate; historical results are not transferred.
