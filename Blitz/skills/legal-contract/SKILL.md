---
name: "legal-contract"
description: 'Contracts in hand: ok to sign, amend its .docx, compare or merge, draft clauses, signing PDF; tenancy, LOI, NDA. Use on review this agreement, edit the changes in, deconflict. New paper: deal-desk; code: defi-eng.'
---

# Legal Contract

Owns any contract document in hand, his or the other side's: reading it, checking it against what was agreed and against what exists, drafting clause wording, amending the file itself so it comes back in its own font, format and layout with only the instructed words changed, and preparing the copy that gets signed. It is not the negotiation: deal-desk owns what to ask for and new deal paper in the house format, wealth-desk owns whether a property deal makes money, defi-eng owns smart contracts. cold-read is the blind final pass this skill calls, at the scope set in Step 5.

**Precedence.** On a contract in hand this skill decides the method over docx, doc-style, deal-desk and house-style: no docx-js Create path, no doc-style theme, no `contract-format.js`, no house-style rewrites (dashes, ranges, dates, negatives) inside the contract. house-style and my-writing-style still govern his messages about it.

**Files.** `scripts/`: `amend.py` (scan, apply, track, compare) and the three gates. `references/`: `review-checklist.md`, `sg-residential-tenancy.md`, `redline-and-signing.md`, `docx-mechanics.md`. If `scripts/` is missing, the skill was installed without its files: say so and stop before any edit.

## First three moves, before anything else

1. **Binary check, first tool call.** List every upload and connected folder and find the original. For an amendment only a `.docx` that `unzip` opens is a base; `*.docx.txt` or `*_docx.txt` is an extraction. A PDF is a real file for review and compare. If only text arrived for an amendment, reply with exactly this and continue with the paste-ready amendment list: "Your .docx reached me as text only, so I will not rebuild it. Put it in Google Drive and give me the name, or attach it again while I am replying."
2. **Live-session check.** Search recent chats and the contract record for the contract name where the surface allows. If another chat touched it in the last 3 hours or holds a newer counterparty message, ask which one is live before any edit.
3. **Ledger load.** Read the contract's ledger from its record. Any counterparty reply in this turn (pasted text, screenshot, email, a returned draft) updates the ledger before anything else happens.

## Hard rules

1. **The original file is the only base.** Edit its XML in place with `amend.py`. Never regenerate a contract, not even as a stopgap, not even "just to show the layout".
2. **Change the words, nothing else.** New text takes the `w:rPr` of the run it replaces; a new sub-clause is cloned from its anchor paragraph (`paragraphs` in the plan). Heading spacers and the keep chain on the signature block are the only layout changes allowed. No new font, size, colour, style, indent, table, row, cell or section, and no change to the contract's own blank lines, spacing or margins outside the heading column.
3. **Smallest edit that carries the change.** A phrase before a sentence, a sentence before a clause. No new recitals, definitions or boilerplate unless the change cannot work without them.
4. **Write in the contract's voice.** Its defined terms, numbering style, words-and-figures money format, spelling and capitals. Leave its typos alone; a typo that changes meaning (name, address, amount, date, ID) goes into the ledger as a proposed change, never a silent fix.
5. **Apply what he instructs; label its status.** Agreed rows go into the signing copy. A refused or unanswered row goes into the version sent to the other side only on his explicit yes, stamped "proposal, unanswered", and no signing PDF is made from that version until the row is agreed or he says sign anyway.
6. **Keep numbering and cross-references stable.** When a sub-clause goes, delete it if he said remove (`{"delete": ...}`), then renumber and fix every reference. Otherwise use the contract's own deleted-clause wording, else "[Deleted]", and keep the number.
7. **Layout is part of the contract.** Repair drift inside the existing structure per Step 4. Restructuring the template needs his explicit yes.
8. **Every change is disclosed.** A version sent to the other side is two files: the clean copy and a redline tracked from the version they last saw. Never accept own changes before sending; never an untracked edit.
9. **Scope is the ask.** Edit first, deliver, then anything else. Benchmarks, tax, regulatory lookups and extra subagents are offered in one closing line, never launched unasked. A new message from him stops any running fan-out; no turn ends without a reply. On "focus", "don't deviate", "do what I asked" or a rejected side-task call: stop every side task, deliver the literal ask, name anything dropped in one line.
10. **The signature block is never split.** Every signing copy carries the keep chain, and the page gate proves the block sits on one page. If the page count differs from the original, the first line of the reply says so.
11. **The signing file is a PDF.** E-signature platforms convert uploads to PDF and substitute fonts they lack, which re-wraps the text. The envelope document is the PDF made from the final .docx and passed by the page gate. If the other side requires a .docx envelope, send it with the PDF beside it, say in the first line that the page gate proves nothing for that platform's render, and ask him to check the signature page in the platform preview before release.
12. **No gate, no file.** A contract file goes out only after Step 5 passes and carries the delivery stamp.

## Step 1, the ledger

Build it before touching the file. Sources, newest first: every counterparty reply, the signed LOI or term sheet, agreed messages.

| # | Clause | Current text, verbatim | New text, verbatim | Status: agreed, refused, unanswered | Source: who, when |
|---|---|---|---|---|---|

Before a row is applied, name anything the old text did that the new text drops, and any clause that relied on it (a clawback, a cross-reference, a defined term). Flag it in one line; apply the row anyway if it is agreed.

One ledger per contract, kept in the contract's record in the project that owns it and shown to him when it has more than three rows or any refused or unanswered row. Update it; never fork it. The version log sits under it.

## Step 2, fingerprint

`python3 scripts/amend.py scan original.docx`. `signed` true: stop. Anything under `protection` or `hidden_text`, or `numbering.auto` above zero: read `references/docx-mechanics.md` first. `heading_column` means a padded margin-heading layout; its `split_hint` feeds the alignment gate. `signature_block_starts` lists keep-chain anchors; if the first is not the block, set `keep.start`. `fc-match` every listed font; without a metric-compatible match for each, renders here are unverified for Word and DocuSign and the stamp says so. Render the original and run `page_gate.py original.pdf original.pdf` to record its page count and signature page.

## Step 3, edit

Write `plan.json` from the ledger: `replacements` (each `old` verbatim and unique), `paragraphs` (insert or delete whole sub-clauses), `spacers` (Step 4), `keep` (`{}` for defaults; `null` when the file has no signature block). The signing copy takes agreed rows only. Then:

```
python3 scripts/amend.py apply original.docx "<name> v<N>.docx" plan.json
python3 scripts/amend.py track "<version they last saw>.docx" "<name> v<N> tracked.docx" plan-delta.json --author "<name he signs with>"
python3 <docx skill>/scripts/office/validate.py "<name> v<N>.docx" --original original.docx
python3 <docx skill>/scripts/office/validate.py "<name> v<N> tracked.docx" --original "<version they last saw>.docx" --author "<name>"
```

`plan-delta.json` holds only the rows new since the version they last saw (for v2: the original and the full plan). `apply` refuses an `old` that matches zero or several times, overlapping rows, a span across a tab or break, a keep chain past 40 paragraphs, or a digitally signed file. Fix the plan, never the checks. The tracked copy carries word changes only; add `--layout` when scan shows `protection: trackedChanges` (then it is the only file the other side accepts; make the signing PDF from its accept-all).

## Step 4, layout repair

**Headings** (only when scan shows `heading_column`). A clause that grew pushes every clause below it down. Add blank spacers in the heading cell after that clause's heading, one per added line (`{"after": "<HEADING>", "add": n}`); a clause that shrank needs blanks removed (`"remove": n`). Rerun `apply`, render, run the alignment gate, repeat until it passes. If it cannot pass inside the existing structure, stop and ask in two lines: what the structural fix changes, and what stays wrong without it.

**Pagination.** `apply` sets the keep chain on the signature block (first "IN WITNESS" or "SIGNED by" line through the last line before a schedule or occupant list; rows get `cantSplit`). Render and run `page_gate.py original.pdf "<name> v<N>.pdf"` (pass `--start=` and `--stop=` if the plan's `keep` patterns were changed):
* `PAGE FAIL`: never ship. Fix the patterns, rerun.
* `PAGES CHANGED`: ship only with the first line of the reply saying "The contract is now M pages, not N; the signature block is whole on page M." Then offer the two ways to win the page back: remove named blank lines above the signature block (a visible change, only on his yes), or tighten the new wording (needs the other side's yes).
* `PAGE n/a`: no signature line found; view the last page and say so in the stamp.

## Step 5, verify

| Gate | Command | Passes when |
|---|---|---|
| Ledger | `amend.py compare original.docx "<name> v<N>.docx"` | Every row meant for this copy appears verbatim; no other change listed (headers and footers included) |
| Structure | `structure_gate.py original.docx "<name> v<N>.docx"` | `STRUCTURE PASS`; paragraph change equals the spacers plus inserted or deleted sub-clauses |
| Alignment | `align_gate.py original.pdf "<name> v<N>.pdf" <split_hint>` | `ALIGN PASS`, or every MOVED line is the first line of an edited clause beside that clause's new first line; `n/a` when there is no heading column |
| Page | `page_gate.py original.pdf "<name> v<N>.pdf"` | `PAGE PASS`, or `PAGES CHANGED` with the first-line notice, or `PAGE n/a` with the last page viewed; never `PAGE FAIL` |
| Redline | `accept_changes.py` (docx skill) on the tracked copy, then `amend.py compare` against the clean copy | 0 changed blocks; `validate.py --author` reports no untracked change |
| Render | every page of the PDF viewed | No heading orphaned at a page foot; PAGE and NUMPAGES still live fields |

One cold-read checker runs these at LITE, one round, with this table as the whole rubric. On an amendment job this overrides cold-read's FULL tier, because the substance was reviewed before the edit. A FULL cold read, gauntlet or fan-out runs when he asks for one. When he says fan out, split these gates across subagents; a subagent never edits the file. Where no subagent can run, run the gates in-line and say so in the stamp.

## Step 6, deliver

Three files and a stamp: `<name> v<N>.docx` (editable), `<name> v<N> tracked.docx` (the redline), `<name> v<N>.pdf` (the signing file the page gate passed). The stamp, and nothing longer:
* Base: original file name and size in bytes.
* Changes: ledger rows applied, by number.
* Structure and Alignment: the gate lines, or "unverified for Word, check pages" plus the list.
* Pages: the page gate line and the fonts it rendered with. Signing file: the PDF name.
* Checker: LITE cold-read, or in-line.
* Version: this name, and the version it supersedes.

## When their draft comes back

`amend.py compare <last version we sent> <their draft>`, then `validate.py <their draft> --original <last version we sent> --author "<their name>"`. Every change goes into the ledger with status, date and which side it favours; their "done" is checked against the text, never taken as read. An unagreed change makes the verdict "not yet": name it, give him the keep-or-revert choice, hold the candidate signing PDF in the work folder, deliver nothing until he decides. Then the review below. Detail: `references/redline-and-signing.md`.

## Merging versions

Trace each version to its base file and ledger rows (`amend.py compare` against the original) in a table: version, base, rows applied, rows missing, verdict. The one built on the original with the latest agreed rows is the base; apply its missing agreed rows per Steps 3 to 5. Never merge by rebuilding; never pick a winner without naming what the loser had that the winner lacks.

## Reviewing a draft

Follow `references/review-checklist.md`: deal pass, reality pass, the other side's lawyer pass, then the integrity pass (cross-references, defined terms, missing schedules, words vs digits, dates, blanks, numbering, meaning-changing typos). On a Singapore residential tenancy also run `references/sg-residential-tenancy.md` and list the post-signing to-dos with deadlines. Output the ranked table with grades (Acceptable, Needs review, Not acceptable) and paste-ready fallbacks; refused points with residual risk; "ok to sign once you confirm:" for anything untestable from here. No "ok to sign" in a reply that does not list the integrity pass. If a verdict changes, name the new fact. One line, only when it applies: this clause needs a lawyer.

## Drafting clause wording

Replace the whole sub-clause when the old text is garbled; otherwise change the phrase. Test every trigger, condition, notice period, proof requirement and payer against the three review passes. The message to the counterparty is numbered, cites the clause, gives the exact text and argues only when asked.

## Files, versions and after signing

`(DD-MM-YY)<Contract short name> v<N>.docx`, `v<N> tracked.docx`, `v<N>.pdf`; N rises and is never reused. Log each version under the ledger (base, rows, status: draft, proposal, sent, signed, void). After anyone signs, the table in `references/redline-and-signing.md` decides: void and resend, re-execute, initial with authority, or a deed of variation. Say which.

## Host and project prerequisites

Obtain readable original document bytes through the current supported file route. Inspect actual fonts and conversion behavior; verify final pagination and signature layout. Review jurisdiction-specific reference dates before relying on them. Keep each contract ledger and version history in its own authorized project records. No personal contract or live negotiation is supplied by this package.

Pairs with docx for validation and mechanics beyond `amend.py`, deal-desk for positions and new deal paper, cold-read for the scoped blind check, wealth-desk for the money behind a property contract, my-writing-style and house-style for messages to the counterparty, and memory-keeper for the contract record.
