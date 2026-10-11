---
name: "house-style"
description: 'Mechanics for text he sends, signs or publishes: answer first, banned words, no dashes, ranges as X to Y, accounting negatives, counterparty names, file naming. Use on "my formatting rules". Chat follows account rules.'
---

# House Style

The mechanics of text the owner sends, signs or publishes: structure, names, counterparty framing, dashes and numbers, the one canonical banned-word list, and deliverable naming. Chat replies to the owner follow the current account instructions, not this skill. `my-writing-style` owns voice, `anti-slop` owns the pattern pass and the post pass, `write-with-pyramid` owns argument structure; the four lanes, each stated once:

| Lane | Owner |
|---|---|
| Mechanics, the one canonical banned-word list, names and counterparty rules, deliverable naming | this skill |
| Voice: ASD-STE100 sentence caps, register, tone | `my-writing-style` |
| The pattern pass (what word lists miss) and the scored post pass for X and LinkedIn | `anti-slop` |
| Argument structure: Minto, SCQA, MECE, named reader | `write-with-pyramid` |

American English, except where a channel skill sets its own spelling (`the configured LinkedIn method` uses British). The concision test: if a word can be cut without changing the meaning, cut it. Goal: prose that reads like a sharp human wrote it, not a model.

## Structure

- Lead with the answer or recommendation. Reasoning follows by the shortest path. Verdict-first stays, but never labeled "VERDICT" and never closed with "confirmed", "settled", or "final". The position does the work; the label and the closure words are theatre.
- Short declarative sentences. On documents, emails and messages, the ASD-STE100 caps in `my-writing-style` govern and uniform rhythm is accepted. On social posts, vary length naturally; let it breathe like speech.
- One proposition per paragraph. A run of three or more parallel items becomes a bullet list.
- Concrete nouns and specific numbers over abstractions. Plain verbs over nominalizations ("decide", not "make a decision").
- Prose by default. Bullets only for truly parallel items. Tables for comparisons of 3 or more items. Headers in documents, not in short messages.
- No sentences about the document itself: no counts of what follows, no pointers to what a later section answers, no statements of the document's own rigor, no pointers to sibling deliverables.
- Binding conditions, kill criteria, and gates never sit under a "Note:" prefix. They belong in the table or in unlabeled body prose. A "Note:" label reads as optional, and a binding condition is not.
- Gloss every internal version label or codename at first use, then check the gloss against every other use of that label in the document.
- Do not restate the intro as the conclusion. Make the point and stop.
- Cut hedges ("somewhat", "quite", "rather", "very") unless they carry weight.

## Names and attribution

The stated rule, 12-08-2026: no individual's name anywhere at the start of a document, not in the title block, the verdict, or any sentence that states or justifies a recommendation. The call is carried by the mechanism, the number, or the named workstream document and date, never by a person.

- People appear later in the body, in structured positions only: the Owner column of an open items table, or a dated source cell in a status table. Never in argument prose, never in a comparison table cell, never as the reason a position is correct.
- Role labels are fine anywhere: the CEO, Legal, Strategic Finance, Taiwan counsel.
- If a person's message is the origin of a question, state the question and drop the person. "Whether traditional FIs lend before Aave, and on what basis", not "Mark's question about whether Aave takes a while."
- When removing a name as the stated ground for a call, insert the substantive ground in the same edit, then confirm every recommendation still has a stated basis somewhere in the document. Removing the attribution and the evidence it pointed to together leaves the call unsupported, which is the most expensive failure of this rule.

## Counterparty framing

For any text a partner could ever be shown, and any internal document about a route that touches one.

- Write the partner-dependent phase forward and conditional: state what must be true, then it proceeds. Never write a partner as blocked, shortfalled, or unready.
- Never assert that a third party will act. Write the condition and the counterparty's recorded role. A commitment written on their behalf is a claim they can be shown.
- Do not stage a quantified deficiency case against a partner or its asset in a document whose subject is a different route. Cite the workstream note that holds those numbers by name and date; the numbers live there.
- Do not describe a route whose stated advantage is that it avoids a partner's governance step. If it matters commercially, record it in the internal workstream note and reference it.

## Mechanics

- No em dashes or en dashes anywhere in the text. Use commas, periods, colons, or parentheses. Hyphens are fine inside compound words and identifiers (buy-side, on-chain, file names); never use a hyphen as a dash.
- Ranges: write "X to Y".
- Negative values in accounting parentheses in financial contexts: (4.2%).
- Probability and forecast tables identify events, horizon, evidence and key drivers. Only explicitly mutually exclusive and exhaustive scenarios sum to 100%; validate definitions, bounds and arithmetic. Independent or separately defined events are not normalized. A ranking shows criteria, evidence, uncertainty and sensitivity, without invented probabilities. Flag unsupported precision.
- Numbers that are claims about the world carry a source and date. Every figure carries the date of the data, not the date it was read.
- Dates are absolute, never relative. Document prose: 15 July 2026. Memory files, calendar text and dated blocks: DD-MM-YYYY. Deliverable file names take the (DD-MM-YY) prefix below. Clock times addressed to him in 12-hour form (5:18 PM, not 17:18), his stated global default.
- In documents, bullets are native list items, never typed dashes, nested at most one level.
- Deliverable files and doc titles: (DD-MM-YY)Title With Proper Spaces, two-digit year, for example (12-08-26)Payment Rails Position.docx. Never kebab-case, never a run-together slug, never year-first.

## Banned words, the canonical list

This is the one list. `my-writing-style` and `anti-slop` reference it and do not restate it. Avoid these unless there is no honest substitute; most have a plainer word.

delve, tapestry, testament, underscore/underscores, pivotal, crucial, vital, intricate, intricacies, landscape (figurative), realm, navigate/navigating (figurative), foster, leverage (as a verb; the noun is literal finance vocabulary and is fine), robust, seamless/seamlessly, holistic, vibrant, bustling, breathtaking, nestled, multifaceted, nuanced, comprehensive, meticulous/meticulously, curate/curated, resonate, boast/boasts, elevate, embark, treasure trove, plethora, myriad, cornerstone, hallmark, showcase/showcasing, underpin, paradigm, synergy, beacon, symphony, kaleidoscope, mosaic, oasis, dazzling, captivating, enchanting, allure, profound, transformative, unparalleled, unwavering, cutting-edge, game-changer, harness, empower, streamline, facilitate, utilize, commendable, noteworthy, remarkable, invaluable, indelible, ever-evolving, ever-changing, fast-paced, enhance, bolster/bolstered, garner/garnered, interplay, enduring, emphasizing, valuable, notable, notably, renowned.

**Borrowed-grandeur nouns** (inflate flat subjects): tapestry, mosaic, symphony, labyrinth, beacon, cornerstone, bedrock, cacophony, kaleidoscope, odyssey, and "ecosystem" as decorative metaphor. "Ecosystem" is literal domain vocabulary in the owner's work and is fine in that sense.

**Inflated-significance verbs**, when they stand in for "is" or "has": stands as, marks, represents, embodies, exemplifies, highlights, offers, features.

## Banned phrases

"It's important to note that", "It's worth noting that", "plays a crucial/vital/significant/pivotal role", "stands as a testament to", "when it comes to", "in the realm of", "in the world of", "navigating the complexities of", "shed light on", "at the forefront of", "in today's fast-paced world", "in today's digital age", "in the ever-evolving landscape of", "rich tapestry of", "rich cultural heritage", "a beacon of", "the key takeaway", "speaks volumes", "leaves a lasting impression", "leaves a lasting impact/legacy", "continues to captivate", "more than just", "a wide range of", "whether you're X or Y", "maintain an active social media presence", "is here to stay", "the possibilities are endless", "needless to say", "last but not least", "first and foremost".

## Banned closers and transitions

"In conclusion", "In summary", "Overall,", "Ultimately,", "Furthermore,", "Moreover,", "Additionally,", "That said,", "In essence,", "Essentially,". Make the point and stop.

## Chatbot residue

"Certainly!", "Of course!", "Absolutely!", "Great question", "Sure! Here's", "I hope this helps", "Feel free to", "Let me know if you have any questions", "As an AI".

## Replacements

| Instead of | Write |
|---|---|
| utilize | use |
| in order to | to |
| a number of | several, many, or the actual number |
| due to the fact that | because |
| it is important to note that | (delete; just say it) |
| plays a role in | affects, shapes, drives |
| a wide range of | many, various |
| facilitate | help, let, enable |
| in the event that | if |

## Structural tells

Sentence and structure patterns (rule of three, bolded lead-ins on every bullet, same-shape sections, hollow both-sides framing, vague authority, promotional tone) belong to the `anti-slop` pattern pass.

## Social content

The channel skills own register on X and LinkedIn, and `anti-slop` runs the post pass. From this file, posts take the mechanics above plus one rule: no tilde hedging on numbers. Fact-check claim by claim before publishing, per the channel skill's claim ledger.

Pairs with `my-writing-style` for voice, `anti-slop` for the pattern and post passes, `write-with-pyramid` for argument structure, and `doc-style` and `google-slides` for the built artifact that carries these mechanics.
