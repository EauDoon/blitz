---
name: "doc-style"
description: 'Builds .docx and Google Docs in house themes. Use when he names Word, .docx, gdoc or Google Doc, says "write this up" or "put this in a doc", or wants something formal for his boss or a partner. Decks: google-slides.'
---

# Document House Style

Every document deliverable follows one structural doctrine and one of three visual themes. The theme system lives as code in this skill's `references/styles.js`, not prose, so output is pixel-consistent across sessions. Never hand-roll paragraph or table styling; compose documents exclusively from that module's builders.

**This is the Google Doc skill.** There is no separate one: any request naming a Google Doc, a gdoc, or Google Docs formatting routes here. See the Google Docs section below.

## Surfaces

| Surface | What applies |
|---|---|
| .docx or Word file | Everything in this file: builders, themes, verify.sh, checklist |
| Google Doc | Everything, plus the HTML upload path in "Google Docs" below |
| Living doc made with the `docs` skill | Structural doctrine, writing register, naming, and checklist items 1, 2, 9 and 11 to 17. The `docs` skill owns the container and its mechanics; the builders and verify.sh do not apply |
| Markdown or PDF deliverable | Structural doctrine, writing register, naming |

**No format named.** When he asks for something formal to share (a write-up for his boss, a report for the team) and names no format, and the `docs` skill or the Docs Artifact type is available, `docs` asks first: reply, doc or file. If he picks a Word file or a Google Doc, build it here. If he picks a living doc, the `docs` row above applies. If `docs` is not available, build the .docx here and offer the Google Doc in one line.

Boundaries with neighbouring skills:

- **Contracts, agreements, MOUs, engagement letters and deeds** follow `deal-desk`'s contract format: traditional first page, no verdict block, no theme. Only the naming rule and the no-dash rule from this file apply.
- **Pitch memos and proposals** take their argument spine from `pitch-architect`. This file builds them: themes, builders, naming, register and the full checklist.
- **Decks and spreadsheets** are out of scope: `google-slides` builds new decks, `slide-design` amends existing ones, `calc-workbook` builds money spreadsheets and `xlsx` the rest.

## Commission and profile precedence

For a Blitz run, the agreed commission and selected lean/comprehensive profile govern format and destination. Preserve the current host-adapted document method and supported native save/render route; this reference copy does not replace installed skills. Lean does not require a Google Doc plus DOCX pair. Comprehensive keeps that default for an unspecified-format business document when authorized and supported. An explicit requested format wins in either profile. Sending a DOCX to a Drive folder does not itself request Google conversion or a second deliverable. Keep all applicable build, render, arithmetic, final-artifact and review checks; no format choice grants upload or publishing authority.

For a Blitz commission, use [context acquisition](../blitz/references/context-acquisition.md) before building dependent content: retrieve and extract missing required inputs from relevant authorized sources and populate the requested result. Keep templates and partial drafts within scope. A known source needs a lookup, not automatic web research; access or evidence gaps remain explicit. This supplements the commissioned content and acceptance checks without replacing the native format/render method.

## Workflow

1. **Load the built-in `docx` skill first**, by name via the Skill tool. Do not look for it by file path. It covers docx-js gotchas, editing existing files, and validation. This skill layers on top of it.
2. **Pick the theme** (see Theme selection below). Default to `minimal` unless the document's audience says otherwise.
3. **Copy `references/styles.js` into the working directory as `styles.js`, verbatim** (`cp <skill-dir>/references/styles.js ./styles.js`). Unconditionally, on every run. Never transcribe it by hand, never edit the copy, never carry one forward. If a `styles.js` is already present, overwrite it: do not read it, do not diff it, do not reuse it. A stale copy has shipped both a wrong-coloured document and one whose bullets were typed dashes, and both are invisible until someone opens the file. Then build from its builders, following `references/build-reference.md`.
4. **Verify before delivering.** Render to PDF, rasterize, and actually look at every page (commands in the built-in docx skill). Then run `references/verify.sh`, which must pass, and work the checklist at the bottom of this file.
5. **Deliver.** Follow the commissioned format and destination. A DOCX-only commission delivers the verified DOCX, including to Drive when that upload is authorized, without automatic Google conversion. Produce a Google Doc only when requested or selected in the applicable delivery contract, read back and verify the conversion, and deliver a verified DOCX companion only when that contract includes it (see "Google Docs" below). Retain source/rollback files locally as applicable; they need not become extra user deliverables.
6. **Hand the finished build to `cold-read` when the document leaves his hands**, at LITE by default, FULL where cold-read's stakes test sets it. Give its evaluators the checklist below as part of the rubric, with the verbatim `verify.sh` and name sweep output. cold-read owns the isolated check; this skill does not spawn a second one.

## Theme selection

| Theme | When | Traits |
|---|---|---|
| `minimal` (default) | Internal circulation, high-frequency deliverables | All Arial, teal accent, left-bar verdict, lightest tables |
| `boardroom` | External counterparties; documents that must carry visual authority | Georgia body, Arial headings, navy, shaded verdict, solid table headers |
| `editorial` | Legal/compliance review; reference documents | All Arial, black 13/11/10pt headings, 14pt title, teal 0F766E accent, plain left-bar verdict with no label, hairline tables; pair with `numberedHeadings: true`. Pinned exactly to a reference Google Doc export of 12-08-26; `styles.js` carries the values |

`numberedHeadings: true` auto-numbers H1/H2 as 1, 1.1, 1.2, 2, ... It works with any theme but is the norm for `editorial`. Never number headings manually in the text.

Every theme's accent is a green or blue-green. Nothing in the house palette is red or burgundy: red reads as a correction mark on a document going out for review, and it collides with the red flag convention in spreadsheets. Two palettes are retired: the burgundy 6B2B3D family and the green 2B6B47 editorial family it drifted into before the theme was pinned to the reference doc on 12-08-26. What to do if either appears in a built document is in `references/build-reference.md`.

If the user names a different colour or brand palette, override `THEMES.<name>.accent` (and `accentLight`, kept very pale) rather than departing from the builders.

## Type size

Regular text is 9pt in every theme (`size: 18`, because docx-js sizes are half-points), and every other size derives from it. The builders do the arithmetic; never set a size by hand. Full table in `references/build-reference.md`.

## Bullets

Point form is always a native list, built with `B.bullet(text)` and `B.bullet(text, 1)`, never a typed dash. The bullet cascade and the dash-bullet post-mortem are in `references/build-reference.md`.

## Figures

Screen mockups and other images come from the `frontend-mockup` skill. Build each figure with its `figure()` helper. The helper composes through `B.body` and `B.run` and adds only an `ImageRun`, so it keeps the builder rule and passes `verify.sh`. A figure sits ahead of the prose that discusses it, like a table, with an italic caption under it. Figure pages count toward the page limit. The Drive connector cannot carry an image into the Google Doc, so each caption in the HTML rendering adds "Image in the Word copy." and the PNGs go with the .docx.

## Structural doctrine (non-negotiable)

- **Verdict first.** Title block, then a verdict block of one to three sentences stating the conclusion, recommendation, or bottom line. The reader should be able to stop after the verdict and know the answer. Never open with background.
- **Hard numbers, flagged assumptions.** Every figure that is an estimate or depends on an assumption gets flagged inline ("Assumption, flagged: ...") or in a short assumptions list. Never present derived numbers as observed ones.
- **Tight.** Default length is 1 to 2 pages. Three pages needs a reason; more than three needs the user to have asked. Cut preamble, cut restatement, cut hedging. If the user sets a page limit, it is a hard limit.
- **Heading hierarchy is strict.** H1 for major sections, H2 for subsections, H3 for sub-subsections. Never skip levels. Never use bold body text as a fake heading.
- **No decorative elements.** No emoji, no icons, no horizontal-rule paragraphs between sections (H1s carry their own rule), no coloured callouts beyond the verdict block, no cover pages unless asked.
- **Tables carry the numbers.** Any comparison of 3+ items with 2+ attributes goes in a `dataTable`, numeric columns right-aligned. Do not bury figures in prose that belong in a table; do not build tables for things that are one sentence.
- **Bullets are native list bullets, one line where possible.** Built with `B.bullet()`, never typed dashes. Full sentences, no nesting deeper than one level, and never a substitute for argued prose in analytical sections.
- **No em dashes or en dashes in prose either.** Use commas, semicolons, or parentheses.
- **Never speak for a regulator.** No language that speaks for a regulator or promises regulator access.
- **Tables sit inline in the section they belong to, ahead of the prose that discusses them.** Prose after a table reads as commentary on the table.
- **Every load-bearing relationship is a full sentence with a named actor and a finite verb.** No nominalized event nouns ("contract commencement"), no telegraphic verb-noun pairs ("model needs rebuild"), no substitution carried by a pronoun ("replaces it as a visible input"). Write "commencement is unset", "the owner must rebuild the cost model", "the bank funding cost replaces the 5.0% borrow rate".
- **Status columns are uniform.** If a table has a status column, every row opens with a status verb of the same class, or no row does. A row stating a new arrangement without saying whether the prior position is closed, superseded or still live is incomplete.
- **No internal tracker references.** Never a tracker row number, a page id or a database id in a document. Name the position in plain words (31-08-26).

The sibling writing skills own the rest of the doctrine, and every document applies them:

- `house-style`: names and attribution (no individual in the title block, the verdict or a recommendation sentence), counterparty framing, the plain verdict with no label or closure word, no sentences about the document, one proposition per paragraph, glossing labels at first use, no binding condition under "Note:", and the banned words.
- `write-with-pyramid`: forward section titles, saying each thing once, third-party firms as examples rather than rankings, and cutting narration before arithmetic.

## Writing register

Verdict-first extends to paragraphs: lead sentence carries the point, the rest supports it. Prefer "the cap binds only in Year 1" over "it should be noted that the cap may potentially bind primarily in Year 1". No filler openings ("This document aims to..."), no throat-clearing, no restating the question. Currency figures as "USD 1.2M" style. Dates as "15 July 2026".

Sentence discipline is the ASD-STE100 core in `my-writing-style`. The pattern floor is `anti-slop` Part 1, which every document runs; its uniformity and dense-prose rules are off here, because STE governs rhythm on this surface.

## Naming the output

Every document this skill produces is named `(DD-MM-YY)Title With Proper Spaces`. Real spaces, real capitals, parentheses around a two-digit-year date, no space after the closing parenthesis. For example `(06-08-26)Quarterly Budget Review.docx`.

The same string is the Google Drive title. Drive takes its title from the uploaded filename, so a name decided sloppily at build time is the name the owner sees in his Drive forever. Set the filename deliberately before the upload, not after.

Never emit a lowercase run-together slug such as `06082026quarterlybudgetreview`. That is the specific failure this rule exists to stop: it comes from collapsing a date-prefixed filename into something punctuation-free, and it makes documents unfindable by title search. Kebab-case is also wrong here, as is a `YYYY-MM-DD-` prefix. If an older instruction anywhere says kebab-case or year-first, this rule supersedes it.

The date is the date the document is produced, in Singapore time.

## Google Docs

Requests naming a Google Doc, a gdoc, or "the google-doc skill" are handled here. There is no separate Google Doc skill.

The .docx is still the canonical build. Build it from the theme builders and verify it exactly as above: render, rasterize, look at every page, run `references/verify.sh`, and work the checklist at the bottom of this file. Keep it Drive-safe: Arial/Georgia only, DXA table widths, A4, no text boxes.

A native Google Doc is produced from HTML, not from the .docx:

1. Render the same content to one self-contained HTML file.
2. Upload that file with the Google Drive connector, passing `contentMimeType: text/html` and the target folder's `parentId`. Drive converts the upload into a native Google Doc.
3. Read the file back through the connector. Confirm the verdict block and every table survived the conversion before telling the owner it is there.
4. Deliver the verified .docx beside it only when the commissioned delivery contract includes that companion. Otherwise retain the verified build source for recovery without adding an unrequested deliverable.

If the document is not going to Drive, or the Drive connector is unavailable, deliver the verified .docx through the file tool and say the Google Doc was not produced.

Never upload the .docx through the Drive connector for conversion. It has failed twice: once with "Unable to convert uploaded content", and once with a 225KB file corrupting in base64 transit (19-08-26). On 04-09-26 the Google Doc again had to be produced from HTML.

The HTML rendering takes its type sizes and colors from the chosen theme in `references/styles.js`. Read the values out of that module; do not guess them. Arial or Georgia only, percentage column widths, native `<ul>` and `<ol>` lists, no text boxes.

The Drive file carries the same `(DD-MM-YY)Title With Proper Spaces` string as the .docx.

Google Docs is the strictest consumer of this pipeline: it silently degrades anything it does not recognise, including a non-native list marker. Never skip `references/verify.sh` on a document headed for Drive.

### Where it lands in Drive

Use the folder the owner names. If he names none, ask once, or state the assumed folder in the delivery line when he is away.

## Pre-delivery checklist

For a Blitz deliverable, first compare the actual artifact with the commission: required information is populated, source-supported, current enough and consistent across narrative, tables and totals. Fix omissions from authorized evidence. Essential unresolved inputs prevent a final-complete claim; apply the narrower acceptance of a template or partial draft.

Render, rasterize, view every page, then confirm:

1. Verdict block is the first content element and actually states a verdict (a conclusion, not a topic).
2. Heading hierarchy has no skipped levels; numbering (if on) reads 1 / 1.1 / 1.2 correctly.
3. No orphaned heading at the bottom of a page with its content on the next; if found, restructure or add a page break.
4. Tables fit the content width, numeric columns right-aligned, no black-shaded cells.
5. Bullets render as round native bullets (level 0 solid, level 1 hollow "o"), with hanging indent and no dash characters anywhere in the list text.
6. **Machine checks pass.** Run `bash <skill-dir>/references/verify.sh "OUTPUT.docx"`, quoting the path (the house filename contains spaces and parentheses). It checks bullet markers, palette, filename form and font sizes: the four defects that look deliberate on the page and survive a visual pass. It must exit 0 before delivery.
7. Footer shows title and correct page count.
8. Page count within limit.
9. Every estimate is flagged; no unflagged derived numbers.
10. No decorative elements crept in.
11. **Name sweep.** No individual is named in the title block, the verdict, or any sentence stating or justifying a recommendation. Every remaining name in the body sits in an Owner column or a dated source cell. Build `roster.txt` in the working directory from every individual's name in the source inputs and the conversation, one per line, longest form first. Then run `bash <skill-dir>/references/namesweep.sh "SOURCE.md" roster.txt` against the source markdown before the build, and read every hit.
12. **Every recommendation has a stated basis that is not a person**, and the cross-reference it points at still exists.
13. No "VERDICT" label in the body text, no closure word on the verdict, and no sentence about the document itself.
14. Each table sits in its own section ahead of the prose discussing it, and no binding condition sits under a "Note:" prefix.
15. **STE pass.** No descriptive sentence over 25 words, no instruction over 20, no passive on a load-bearing claim, no paragraph over six sentences.
16. **Slop floor pass.** Run `anti-slop` over the source markdown before the build, alongside the name sweep. No false agency on a load-bearing sentence, no copula avoidance, no binary contrast, no mannered prose, no synonym cycling on a defined term, no vague attribution, and no sentence that would read the same about another company or another token.
17. No internal tracker ids anywhere in the text.
18. Delivery matches the commissioned format/destination. When Google Doc conversion is selected, its final content/layout is checked and read back. A DOCX companion is delivered only when commissioned; any requested DOCX is verified. Each delivered artifact carries the house name; the destination and rollback pointer are stated.
19. Figures, when present: each built with the `frontend-mockup` skill's `figure()` helper, each caption present, each figure page viewed in the render.

If any check fails, fix at source (recopy `styles.js`, rebuild) and re-render; never edit the output .docx. Do not deliver on the first render without looking at it, and do not deliver without a clean `verify.sh` run.

## False positives, from the log

Reporting any of these as a defect is itself the defect:

- A list of three items with distinct referents (three parties, three dates, three products) is an enumeration. The rule-of-three tell is three near-synonyms or three parallel clauses doing one job.
- An explicitly mutually exclusive and exhaustive scenario set sums to 100. Independent milestone probabilities do not, must not be renormalized, and must be labelled independent.
- Heading numbers the builder emits, and title-block metadata placed before the verdict.
- A conclusion that appears in the verdict, its own section and the open items table. The structure mandates it.
- A bulleted procedure in an STE document.
- A spelling variant used consistently through the document. The finding is inconsistency, not the variant.