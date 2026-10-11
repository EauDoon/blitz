---
name: "slide-design"
description: 'Reviews and amends slides that already exist, in Google Slides or .pptx: layout, speaker notes. Use on review this deck, fix slide 4, is this deck ready, make these slides land, rehearse me. New decks: google-slides.'
---

# Slide design

This skill looks at slides and says what is wrong with them. It does not build new decks.

## Boundary

| Work | Owner |
|---|---|
| Build or rebuild a whole deck from its content, the deck look, delivery to Drive | `google-slides` |
| The argument of a pitch, proposal or board deck | `pitch-architect` |
| Mechanical edits inside a .pptx file | `pptx` |
| Amend named slides in a deck that exists | this skill |
| Review a deck that exists, his or a counterparty's | this skill |
| Choose the layout a piece of content takes | this skill |
| Speaker notes and rehearsal | this skill |
| A chart inside a slide | `google-slides` chart rules and deck theme |
| A structural figure inside a slide | `diagram-design` |
| A document or a spreadsheet | `doc-style`, `calc-workbook` |

The seam is the unit of work, not the file. One slide, or a handful he names, is amended here in
place. A whole deck rebuilt from its content goes to `google-slides` (with `pitch-architect` on the
argument of a pitch) with the review attached. Whole-deck reordering is still an amendment and stays here; only a
rebuild from the content leaves.

`cold-read` is a different job. It checks whether a deliverable clears its bar and is true. This
skill checks whether a deck works in the room. A partner or board deck needs both, and the order is design first,
gate second, because the gate should read the version that is actually going.

## Never review a deck you have not seen

A review written from the text alone is worthless. Text tells you what a slide says. It does not
tell you that the title wrapped, that the source line is unreadable, or that the table runs off the
bottom edge. Open the deck and look at every slide.

### Google Slides

1. Find the file. `mcp__Google_Drive__search_files` with
   `mimeType = 'application/vnd.google-apps.presentation'` and a title clause. Take the `id`.
2. Read the copy. `mcp__Google_Drive__read_file_content` returns every word in the deck.
   **It returns one undelimited run** (verified 09-09-26): no slide boundaries, no separation of
   title from body from table cell from source line. Use it to read the argument end to end. Never
   use it to say which slide a line sits on.
3. Look at the slides. Open the browser pane at:

   ```
   https://docs.google.com/presentation/d/<id>/preview
   ```

   Then screenshot. Advance by navigating to the next slide directly:

   ```
   https://docs.google.com/presentation/d/<id>/preview?slide=id.p2#slide=id.p2
   ```

   Both the query and the fragment are needed. Arrow keys and the on-screen next control do not
   advance this viewer (verified 09-09-26). Decks that arrived as .pptx use page ids `p1`, `p2`,
   `p3`. If the slide does not change, the deck was authored natively and its ids look like
   `g263a1b4c5d_0_12`: open the edit URL, click each slide, and read the id out of the address bar.
4. Screenshot at `scale` 0.6. Full scale for a slide with a dense table or a small source line.

### A .pptx on disk or attached

```bash
soffice --headless --convert-to pdf --outdir /tmp/check "<deck>.pptx"
pdftoppm -png -r 72 /tmp/check/<deck>.pdf /tmp/check/s
```

Then Read the PNGs. Fonts substitute in LibreOffice, so this is a layout read, not a typography
read.

### A screenshot or a pasted running order

A screenshot is a single slide and is reviewed as one. Say so, and do not generalize from it to the
deck. A pasted list of titles is the sequence only: run the deck pass below, skip the slide pass,
and say which pass you could not run.

## The review

Two passes. Do the deck pass first, because a slide that is well made and does not belong is still
cut.

### Deck pass

- **Does it carry an argument.** Situation, then what changed, then what we do, then the ask. A deck
  that is a list of updates has no argument and the room will not remember it.
- **Does the sequence hold.** Read the titles alone, in order, and nothing else. They should read as
  a paragraph that makes the case. If the titles are topics ("Partner", "Timeline", "Risks") the deck
  is a filing cabinet.
- **Is the ask on a slide.** A deck that asks for a decision states the decision, the options and
  the recommendation. A deck that asks for nothing should be an email.
- **Length against the slot.** About one slide per minute, and fewer if there is discussion. A 20
  minute slot does not take 30 slides. When he is over, say which slides to cut, by number.
- **Audience fit.** A technical room wants the mechanism. A committee wants the exposure, the
  decision and the date. A partner wants what they get and what we need from them. Cut the half
  that belongs to the other room.

### Slide pass

For each slide, in order:

| Check | Fails when |
|---|---|
| One idea | The slide needs two sentences of explanation to make sense |
| Title is a claim | The title names a topic instead of stating the point |
| Reads in five seconds | The eye has to hunt for where to start |
| Figures sourced | A number sits on the slide with no source line |
| Nothing clipped | Text crosses the bottom edge, wraps into a rule, or overlaps the page number |
| Source line legible | The foot line runs to two dense sentences nobody can read at the back |
| Body earns its place | A line repeats the title, or says what the speaker will say anyway |
| Layout matches content | See the rubric below |

Report findings per slide, most serious first, with the slide number and the fix. Not a list of
observations. A fix he can apply.

## Layout rubric

Pick the layout from the shape of the content, not from what the last slide used. The names below
are generic; map them to the builder's own layout names (`google-slides`, or the deck's template)
before recommending one.

| Content | Layout |
|---|---|
| One number that is the whole point of the slide | Big number |
| Two to four numbers that only mean something together | Stat tiles |
| Workstreams with a stage, a date and a status | Workstream tracker |
| A fixed set of columns compared across rows | Table |
| Two parties, two sides of a deal, before and after | Two columns |
| A claim and the three things that support it | Claim plus three supports |
| A plan phased over time | Roadmap |
| A break in the argument | Section divider |

Two rules on top of the table. A slide that fits no layout is two slides. A slide whose content
fits a layout only after the copy is cut to fragments is the wrong layout, so widen the column or
split the slide instead of compressing the sentence.

## Anti-patterns

Name these when you see them. The first three follow Corey Haines' sales-enablement guidance.

- **Wall of text.** Over about 200 words on a slide. Nobody reads it while someone is talking. If it
  has to be read, it is a document.
- **Feature dump.** Every slide a thing we have, with no "so what" and no link to the room.
- **Missing arc.** Slides that are each fine and that do not follow from one another.
- **Written for the auditor.** Clause numbers, document titles and bracketed caveats on the slide
  face. Proof moves to the notes and the
  source line. The slide face carries plain sentences.
- **Two numbers in one clause.** Split them or drop one.
- **The unread source line.** A citation so long it becomes decoration. Keep the slide face to the
  figures that carry the point and move the rest to the notes.

## Speaker notes and rehearsal

Notes carry what he would say and would not put on a slide: the source, the clause reference, the
caveat, the number he wants ready if asked. One short paragraph per slide, in his own speaking
voice, not slide copy repeated.

For a rehearsal, walk the deck slide by slide and give him, per slide, the one sentence that opens
it and the question the room is most likely to ask. Name the slide where he is most exposed. If a
slide only makes sense once he has explained it, that is a finding against the slide, not a note.

## Amending

Never write into his live deck without asking. That is his file and an overwrite is not reversible.

Three routes, in order of preference:

1. **He applies it.** Give the exact edit per slide: slide number, the old line, the new line. This
   is the default for a deck he is already editing, and for anything owned by someone else.
2. **A new version alongside.** Copy the file in Drive under the next version name, amend the copy,
   leave the original untouched. Ask before doing it.
3. **A rebuild.** Only when the deck is his and the finding is structural. Hand it to
   `google-slides` (with `pitch-architect` on the argument of a pitch) with the review attached.

Change only the slides he named. A request to fix slide 4 is not a licence to restyle the deck.

Leave his file names alone unless he asks. Several decks in his Drive do not follow his naming
rule, and renaming a file breaks every link already sent to a room.

## Handoff

- Any amendment that changes a figure goes to `cold-read` before it ships.
- Any amended deck leaving the building goes to `cold-read` (an auto-fire class), FULL for a
  partner or board deck.
- A pure layout or copy-tightening pass on an internal deck does not fire the gate.
- Prose he will read out or send with the deck goes through `my-writing-style` and `anti-slop`.

## Register

Slide copy is written for the room: plain business English, one complete sentence per line, one
figure per line with its unit. No em dashes or en dashes anywhere, on the slide or in the notes.
No individual is named on a cover, a verdict slide, or any line that carries a recommendation.