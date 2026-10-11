---
name: write-with-pyramid
description: 'Argument structure for prose carrying an ask or decision: Minto pyramid, SCQA. Use on "make this land", "tighten this email or memo so it lands", "why did nobody reply", "heard nothing back", status updates, escalations.'
---

# Write with pyramid

Structure the argument before writing the prose. Answer on top, reasons beneath, proof at the base, one ask with one date.

## What this owns, and what it does not

| Layer | Owner |
|---|---|
| Argument shape: what goes first, how support is grouped, where proof sits | This skill |
| Mechanics, the canonical banned-word list, names and attribution | house-style |
| Voice: ASD-STE100 sentence caps, register, tone | my-writing-style |
| The pattern pass and the X and LinkedIn post pass | anti-slop |
| Pitch and proposal structure, objection slides | pitch-architect |
| Deck look, design system and build | google-slides |
| Outreach sequencing, cadence, give-up point, intro blurbs | the configured outbound method |
| Public voice on X and LinkedIn | the configured X-post method, the configured LinkedIn method |
| Whether the decision itself is right | decision-os |
| Whether the numbers are right | the owning desk plus reasoning-core |

Run structure first, prose second. A well written paragraph in the wrong position still fails.

## The spine

Three levels. Not five.

**Top.** One sentence. The recommendation, decision, or ask. Must survive being read alone.

**Middle.** Two to four supporting points, each a reason the top is true. MECE: no two overlap, together they leave no obvious gap. Two is a legitimate count. Three is not a quota.

**Base.** The proof under each middle point. Numbers, sources, quotes, attachments. Every number here traces to a computed figure or a cited source.

Test: every sentence in the draft is the answer, a reason, or proof. Anything else is cut.

## Operation 1: build the spine

Given a messy draft or a raw intent:

1. Extract the actual ask. If the draft does not contain one, stop and ask what outcome is wanted. Do not invent an ask.
2. Write the top sentence. Verb first where possible ("Recommend X", "Approve Y", "Move Z to").
3. Group the reasoning into two to four points. Merge overlaps, name gaps.
4. Attach proof to each point. Mark any point with no proof as unsupported rather than dropping it silently.
5. Cut everything that is not the answer, a reason, or proof.
6. Add the ask and the date.

Output the spine as a skeleton before drafting prose, so the shape can be corrected cheaply.

Never organize the spine around a person, and never hand builders a brief organized around one. If a person's message is the origin, apply house-style's question-not-person conversion; verbatim messages go to a provenance appendix marked not-for-quotation. A brief that opens with a person makes every downstream draft open by citing them; the 12-08-2026 rewrite traced exactly that failure to a source pack whose first section was titled with a colleague's name.

## Operation 2: the SCQA opener

Use for anything longer than a short email, anything the reader did not ask for, and anything the reader may resist.

* **Situation.** One sentence the reader already agrees with.
* **Complication.** One sentence on what changed or broke.
* **Question.** The question the complication creates, usually implied rather than written.
* **Answer.** The recommendation.

Four sentences maximum. The answer still arrives fast, it just arrives after shared ground is established.

**Skip SCQA when** the reader asked the question, the message is under five sentences, or the relationship is transactional. In those cases go straight to the top sentence. An SCQA preamble on a reply to a direct question reads as stalling.

## Operation 3: MECE audit

Run on any message above real stakes, before send.

1. Do any two support points say the same thing in different words? Name the overlap and merge.
2. Is there an obvious angle a sharp reader would raise that no point covers? Name the gap.
3. Propose a rewritten set of two to four points that are clean.
4. One sentence explaining each change.

MECE is a coverage test, not a symmetry test. Do not pad to three. Do not split one point into two to look thorough. If the argument genuinely rests on one reason, say so and make the proof heavy.

## Operation 4: the named-reader test

Do not simulate a generic busy executive. Simulate the actual reader.

Before the test, state four things:

| Field | Example |
|---|---|
| Reader | Head of partnerships at the counterparty |
| Their decision | Whether to allocate eng time this quarter |
| Cost of yes | Two engineers, three weeks, opportunity cost against their roadmap |
| Most likely objection | "We tried something like this and volume never came" |

Then grade the draft:

1. After the first two sentences, does the reader know what they are being asked to do? Yes or no.
2. Which support point is weakest, most redundant, or missing given this reader's objection?
3. Would this reader act, ask for more, or ignore? Be blunt.
4. If ignore, rewrite the first two sentences.

A generic CEO simulation grades tone. A named-reader simulation grades whether the specific objection was pre-empted, which is the thing that actually decides the reply.

## Non-negotiables

* **One ask.** Two asks in one message halves the response rate on both. Split into two messages.
* **One date.** Every ask carries a by-when. "Decision needed by Friday to hold the launch date" beats "let me know your thoughts".
* **The subject line carries the answer.** For email, subject is part of the spine. "CRM vendor recommendation, decision by Fri" not "CRM vendors".
* **Proof traceability.** Any number in the middle layer exists in the base layer with a source or a computation. No orphan figures.
* **Shorter than the input.** If the rewrite is longer than the draft, structure was added but nothing was cut. Go again. Cut from narration, never from arithmetic: derivations, input tables, legal mechanisms, and caveats attached to numbers are the document; framing and process narration are the padding.
* **Titles work forward.** Section titles say what the content does for the reader's next decision, not what is lost ("How Phase 1 works with Phase 2", not "What Phase 1 gives up"). After a retitle, reread the body against the new title.
* **Once, in the owning section.** Each guardrail, restriction, and open question is stated exactly once. If the body closes a question, close or update its open items row in the same pass.
* **Examples, not rankings.** Third-party firms appear in body prose and table cells as examples ("e.g. Chailease, Incomlend"), never ranked selections. Rankings live in the open items table or an annex, where they read as a workstream.

## Failure modes

| Failure | Symptom | Correction |
|---|---|---|
| Forced answer | Confident recommendation on a question still genuinely open | Ship the decision frame instead: the options, what would resolve it, by when. Structure the uncertainty, do not hide it |
| MECE theater | Always exactly three points, one of them padded | Use the true count. Two supported points beat three where one is filler |
| Cold open on a hostile reader | Reader rejects the answer before reaching the reasons | Use SCQA. Establish shared situation, then answer at sentence four |
| Structure without stakes | Clean pyramid, no ask, no date, no reply | Add the ask and the date. A pyramid with no ask is a status report nobody needed |
| Pyramiding a thinking document | The exploration is the point, and answer-first kills it | Narrative memo is a different form. Do not apply the spine to a document whose purpose is to think in public. Amazon six-pagers are narrative by design, not pyramid |
| Proof drift | Support points assert numbers absent from the base | Every figure traces down. If it cannot, mark it unverified or cut it |
| Answer-first as bluntness | Reads as curt to a relationship that is not yet transactional | Structure stays; one line of warmth before the top sentence is allowed and costs nothing |
| Person-framed spine | The top sentence or a support point rests on who said it | Restate as the question or the mechanism; the person moves to an Owner column or a provenance appendix, per house-style |

## Worked example

**Before.** 118 words, ask on line 9, no date.

> Hey Jamie, hope you had a good week. Wanted to circle back on the vendor conversation. We have been evaluating three options for the new CRM and I went deep on each over the past two weeks. Vendor A is cheapest but integrations are limited. Vendor B has better features but higher pricing. Vendor C sits in the middle. I spoke to references at each, looked at pricing carefully, and mapped our must-haves. Based on all of that I think we should probably go with Vendor B, but wanted to run it by you first.

**After.** 71 words, ask on line 1, dated, three MECE points, proof attached.

> Subject: CRM recommendation, Vendor B, decision needed by Fri
>
> Recommend Vendor B. Three reasons.
>
> One. Only option with native Salesforce and Slack integrations, which sales uses daily.
> Two. Costs $4,200 more than Vendor A over three years, saves an estimated 12 hours per week across the team.
> Three. All four reference customers at our scale renewed after year one.
>
> Decision by Friday to hold the launch date. Full analysis attached.

The information is identical. The second one gets approved because the reader knows what they are deciding before they decide whether to keep reading.

## Composition

When this fires alongside other skills, the order is fixed:

1. Domain desk produces the substance and the numbers.
2. reasoning-core verifies before anything is asserted.
3. This skill sets the structure.
4. The three prose lanes in the ownership table render it.
5. decision-os owns the call itself if the message commits to something.

Structure never overrides correctness. If the spine requires a claim the desk cannot support, the claim comes out, not the caveat.

Before citing the method's history (Minto, McKinsey, Amazon memos), read `references/provenance.md`; most of the folklore is unsourced.
