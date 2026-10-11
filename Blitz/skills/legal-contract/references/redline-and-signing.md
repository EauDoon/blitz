# Redlines, versions and signing

Read before any file leaves for the other side, before a signing copy is made, and whenever a counterparty's draft comes back. Sources read 26-09-2026: Harvey redlining practice notes, Montague Law version-control note, Tech Contracts (Tollen), Contract Nerds rule 7, Adams on comparison etiquette, Gowling WLG and Clayton Utz on post-execution fixes, DocuSign community staff answers, LibreOffice and ECMA-376 pagination documentation.

## A version is two files

* Every version sent to the other side is a clean copy plus a redline made against the version they last saw. The redline is real tracked changes (`amend.py track` from that base), never a hand-typed change list alone.
* Never accept your own changes before sending. Never slip an edit outside the tracked changes: the only untracked edits allowed are in a template before its first send.
* Author is the name he signs with. Date in UTC. One change per ledger row. A short cover note lists the rows changed and nothing else.
* Before sending, test the pair: accept-all on the redline must equal the clean copy word for word; reject-all must equal the base.
* Name `(DD-MM-YY)<Contract short name> v<N>.docx` and `v<N> tracked.docx`. N rises and is never reused. Never `-1` and `-2`, which a download can reorder.

## When their draft comes back

* Run `amend.py compare <last version we sent> <their draft>`. Every changed paragraph is listed with word-level changes. Read that list, not their cover note. A change they did not mention is still a change.
* If their draft carries no tracked-change marks and yet differs, say so in the reply: "their draft changes X and Y without marking them".
* Their "Done" against an ask is checked against the text, never taken as read (see CHANGES.md, v1: a clause marked done was still garbled).
* Update the ledger row statuses (agreed, refused, unanswered) from their draft and messages, with the date, before any further edit.

## The signing file

* DocuSign converts every uploaded document to PDF on its servers and substitutes fonts it does not have. Its staff list of supported fonts: Arial, Calibri, Courier New, MS Gothic, MS Mincho, Tahoma, Times New Roman, Trebuchet, Verdana. Arial Narrow is not on it. A .docx in an unsupported font can re-wrap and split a signature block after upload (see CHANGES.md, v3). DocuSign staff advice: save as PDF first, or embed fonts.
* Rule: the file that goes into an envelope is a PDF made from the final .docx, rendered with the document's own fonts or their metric-compatible twins, page count and signature block page checked with `page_gate.py`. Deliver the .docx for editing and the PDF for signing, and say which is which.
* The .docx keeps `keepNext` and `keepLines` on the whole signature block (`cantSplit` on rows if it is a table), so a re-render in Word holds the block on one page. Also add which side an unagreed change favours when you report it. The spec says a keep chain longer than a page starts on a new page; Word in practice breaks such a chain somewhere (unverified which wins). A signature block is short, so either way it stays whole.
* PDF made here is proof only when `fc-match` returns a metric-compatible font for every font in the file. Arial to Liberation Sans, Times New Roman to Liberation Serif, Calibri to Carlito, Cambria to Caladea, Arial Narrow to Liberation Sans Narrow (build recipe in `docx-mechanics.md`). Otherwise the stamp says "unverified for Word" and names the pages to check.

## After anyone has signed

| Situation | Route |
|---|---|
| Error found before the other side signs (DocuSign envelope open) | Void the envelope, fix the .docx, make a new PDF, send a new envelope. Say so in the first line |
| Both signed, wording wrong | Re-execute a clean corrected copy; or all parties initial a manuscript change with authority on file; or a deed of variation or side letter that names the original and the clauses changed. A variation needs consideration or a deed |
| Both signed, layout only wrong (a split block, a heading drift) | Nothing to fix in law; fix the file for the record only if he asks |
| Digitally signed .docx (`_xmlsignatures/` present) | Do not edit; any byte change invalidates the signature. Edit a copy and have it re-signed |

## Electronic signature validity

Check the jurisdiction's rules in the matching reference file (Singapore: `sg-residential-tenancy.md`). Keep the platform's completion certificate with the signed copy, and offer wet-ink counterparts when a lease or land interest is involved and either side asks.
