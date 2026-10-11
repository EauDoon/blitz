# Contract review checklist

Read when the job is a review, an "ok to sign?", or a check of a counterparty's draft. Three passes, then the integrity pass, then the output. Sources read 26-09-2026; practitioner method from Adams (adamsdrafting.com), Sterling Miller (tenthings.blog), LexisNexis commercial contract checklist, SDCBA offense and defense review; evaluation criteria from Vals VLAIR, Harvey BigLaw Bench, CUAD and ContractNLI.

## Pass 1, the deal

Every agreed term is in the document, nothing is added, and each is quoted verbatim against its source (LOI, term sheet, agreed messages, the ledger).

| Check | What to confirm |
|---|---|
| Parties | Full legal names, ID or registration numbers, capacity to sign, the party who performs is the party who signs |
| Subject | The exact premises, goods, services or rights, with the address, unit and postcode right |
| Money | Rent or price, deposit, fees, timing, currency; words and figures agree; who pays what to whom and by when |
| Term | Start, end, renewal option and its trigger, notice periods, break or diplomatic clause and its conditions and proof |
| Conditions | Anything that must happen first (consent, payment cleared, inventory signed), and what happens if it does not |
| Obligations | Repairs and caps, maintenance, insurance, taxes, utilities, servicing, cleaning at exit, access |
| Exit | Termination rights for each side, deposit return mechanics and deductions, handover state, holdover |
| Boilerplate | Governing law, dispute resolution, notices, entire agreement, variation in writing, counterparts, e-signature |

## Pass 2, reality

Every item, room, party, figure and document the contract names exists as written. Test clause text against the inventory, the asset register, IDs and passes, the actual rooms, the signed LOI. A clause that matches the request but not the unit is still wrong (see CHANGES.md, v1: a curtains heading covered bedrooms only while the living room curtains were not motorised).

## Pass 3, the other side's lawyer

For each party ask "what if I breach?" and "what happens if the other party does not perform?". Then hunt:
* Exits: every trigger that lets them leave early, and its cost to him.
* Delay and cost shifting: "reasonable efforts", "to be mutually agreed", "at X's discretion", "notwithstanding", "provided however". Each is a term not yet negotiated.
* Consent clauses: whose consent, and whether it can be withheld; "not to be unreasonably withheld" hands the decision to a court.
* Money leaks: fees, commissions and refunds that survive termination or renewal; deposit set-off.
* Ambiguity: "and" and "or" in lists of conditions, undefined capitalised terms, two terms for one thing.

## Integrity pass, mechanical, never skipped

| Class | How it fails | Check |
|---|---|---|
| Cross-references | A clause is deleted and "see clause 7.2" now points at the wrong text | List every "clause", "section", "schedule" reference and read the target |
| Defined terms | Capitalised term never defined, defined never used, defined twice, "Borrower" written for "Guarantor" | Build the defined-term list and check each use |
| Schedules | "the inventory list attached hereto" and nothing is attached | List every attachment named and confirm it exists |
| Words vs digits | "Six Thousand Three Hundred (S$6,830)" | Compare every words-and-figures pair |
| Dates | Start after end, notice longer than the term, a date that is not a real day | Compute every date and period |
| Blanks | Underscores, "[ ]", "TBC", agency name left empty | Grep for blank fields and list them |
| Numbering | Duplicate or missing clause letters after an edit | Read the sequence in order |
| Typos that change meaning | Name, address, unit, postcode, ID, amount, date | Verify each against a source document |

## Grading and output

Grade every clause you comment on: Acceptable, Needs review, or Not acceptable, and give fallback wording for the last two. Rank by cost to him. Severity: before signing (money, exit or liability), should fix (clarity, drift from the deal), optional (style). Comment only on what fails to express the deal, is confusing, or carries real risk; never rewrite to taste.

Output table: clause, current text verbatim, problem in one line, paste-ready replacement, grade, severity. Then the refused points with residual risk in one line each. Then the "ok to sign once you confirm" list for anything that cannot be tested from here.

Scorecard the skill is judged on: recall of a lawyer's issue list; every finding quotes the exact span (an invented or misquoted clause is a hard fail); the integrity pass fully listed; redline hygiene per `redline-and-signing.md`; restraint, with grades and fallbacks rather than rewrites.
