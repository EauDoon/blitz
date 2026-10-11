---
name: "google-slides"
description: 'Builds new Google Slides and PowerPoint decks in the house look. Use on create a pptx, gslides or Google Slides deck, "turn my notes into slides", slides for a meeting or talk. Pitch argument: pitch-architect.'
---

<!-- Modified adaptation of the Apache-2.0 sources named in NOTICE.md: combines borrowed presentation rules with Blitz routing, house look and output guidance. Attribution and modification notice added on 2026-10-11; see NOTICE.md and LICENSE.txt. -->

# Google Slides

Builds every new .pptx or Google Slides deck and lands it where the owner asked: a Google Slides file in Drive, or a PowerPoint file. This skill owns the canvas, the look of every deck (pitch, strategy, proposal and board decks included), charts on slides, render QA and delivery. It does not own the argument or the file mechanics. pitch-architect owns the argument spine of persuasion decks: action titles, the scenario table, the risk slide and the one ask. Where the two overlap, pitch-architect wins on argument and this skill wins on look. The pptx skill owns pptxgenjs mechanics, validation and all edits to an existing .pptx; take only its mechanics and QA commands, because this design standard overrides its design section. diagram-design draws structural figures for slides. cold-read runs the blind check before a deck leaves the building.

## 1. Route

| Request | Build | Deliver |
|---|---|---|
| Names Google Slides or gslides, or "put it in my Drive" | .pptx as the carrier | Section 5, Google route |
| Names PowerPoint, ppt or pptx | .pptx | Section 5, file route |
| Pitch, strategy, proposal or board deck | pitch-architect spine; this skill for look, canvas, QA and delivery | As named |
| Change an existing Google Slides deck | Out of scope while no Slides write tool exists | List the edits slide by slide, or rebuild as a new version if he asks. Never overwrite |
| Fix an attached .pptx | pptx skill alone | Same file type back |

## 2. Story before slides

* Write all titles first. Each content slide title is a full sentence that states a conclusion: 15 words or fewer, 2 lines at most. Cover and section slides are exempt. Read the content titles alone, in order: they must tell the whole argument. For an external deck, show the owner the title list before building.
* One idea per slide. A stranger names the point in 3 seconds.
* Pick one register and hold it. Reading, the default: the deck is read, not watched; 100 to 250 body words a page in sentences, at most one exhibit a page, a source on every page that shows data. Presented, only when he says presented, keynote, talk or on stage: the speaker carries it, 7 body words or fewer, no bullets, large type.
* Never invent a number. A missing figure shows as [CONFIRM] on the slide and in the handover note.

## 3. Design standard

**Canvas.** pptxgenjs LAYOUT_16x9, 10 x 5.625 in, the Google Slides default page. Side margins 0.45 in. The title sits at the same position on every slide. Colors go into pptxgenjs without a hash.

### Reading register, default

The consulting and banking look: small regular weight type, dense well set prose, hairlines, one quiet hue. Nothing on a content page is larger than the title, so no hero numbers. Emphasis comes from bold run in phrases inside regular body text, two to four a page, never from size.

| Role | Navy, default | Paper |
|---|---|---|
| Background | FFFFFF | F7F5F0 |
| Tint, table totals and callouts | EEF2F7 | EEEBE3 |
| Exhibit panel | F6F8FB | F2EFE8 |
| Hairline | C9D1DC | CFC9BA |
| Ink | 1F2430 | 1B1A17 |
| Muted | 6B7280 | 5C584F |
| Structural hue: cover band, rules, trackers, outlines | 092C61 | 1A2B45 |
| Accent, the one highlighted series or figure | 092C61 | A8461F |
| Chart context series | 9DB0CC | B9B2A3 |
| Negative, data only | B4203A | A8243C |

Color covers 2 to 8 percent of a content page and comes from hairlines, tints, caps labels and one highlighted series. Only the cover carries a full color band; section dividers are white with a structural band and a number; nothing else bleeds. A brand color replaces the structural hue. Navy on white for anything external, anything a bank or board will see, and anything data heavy; Paper for internal pre reads and memos read on screen at length, and for warm brands. One base for the whole deck, never both.

**Furniture on every content page.** Tracker in caps, 7.5 pt bold structural, top left at 0.28 in. A sticker top right (PRELIMINARY DRAFT, FOR DISCUSSION, ILLUSTRATIVE) only when the status is qualified: 6.5 pt caps in a 0.5 pt outlined box, 1.5 x 0.24 in at x 8.05, y 0.24. Title at 0.5 in, 18 pt regular serif, one or two lines. Lead sentence at 1.18 in, 11 pt muted, one rendered line (about 110 characters); on a table page the lead carries the units. A 0.75 pt structural rule at 1.5 in. Body from 1.62 to 4.95 in, column gutter 0.3 in. Source, then Note with numbered notes, at 5.02 in, 7 pt muted. Confidential line centered at 5.36 in, 6.5 pt. Page number bottom right, 7 pt.

**Type**, in pt on this canvas, line spacing 1.2 unless stated:

| Role | Size | Weight and notes |
|---|---|---|
| Cover title | 26 | regular serif, white on the band; 1.1 spacing |
| Slide title | 18 | regular serif; large or bold, never both; 1.1 spacing |
| Lead | 11 | regular, muted |
| Section label, tracker | 7.5 | bold caps, structural, charSpacing 1 |
| Prose, numbered blocks | 10.5 | regular; bold run in claims only |
| Bullets | 10 | square bullet (code 25AA), two levels at most, paraSpaceAfter 6 |
| Callout, kicker, decision box | 10 to 10.5 | bold lead in, then regular |
| Table | 8.5 | header bold over a 1.25 pt structural rule, 0.5 pt hairline rows, no zebra, numbers right aligned, negatives in parentheses, totals or the one comparison row on the tint, row height 0.27 in |
| Chart labels | 8 | regular; exhibit heading 9 bold with units |
| Source, note | 7 | muted |

**Density.** 100 to 250 body words a content page, counting prose, bullets, tables, callouts and exhibit headings and excluding the title, lead, tracker, chart labels, source, footer and notes; 100 is concise, 250 the ceiling, and an executive summary runs 200 to 250. Sentences average 15 words and never pass 25. Lines run 50 to 90 characters, so a text column is 3.5 to 6.3 in wide and a full width page uses two or three columns. Paragraphs where the logic is causal, bullets only for items of the same kind.

**Page types.** Cover: structural band from the top to 2.35 in, tracker in caps at 0.55 in, title at 0.9 in, then subtitle and date at 11 pt below the band and a draft note at 7 pt near the foot. Section divider: the same band with the section number as tracker and the section title, nothing else. Exhibit panel: from 1.85 to 4.8 in. Executive summary: three or four numbered blocks, each a bold claim sentence and one to three supporting sentences, no exhibit; block numerals 14 pt regular serif in the structural hue. Situation and implication: exhibit on the left 55 to 60 percent in the panel tint with its heading and units, SITUATION and IMPLICATION labels on the right with two or three sentences each, a "So what" kicker over a hairline at the bottom. Key considerations: two or three columns with bold heads over hairlines, three to five hedged square bullets each, a "Preliminary view" line over a hairline. Table page: units in the lead, the table spec above, one sentence of reading below. Next steps: a table with owner and timing, then the decision requested in a 0.75 pt outlined box.

**Charts.** The title states the finding; the exhibit heading carries the metric and units. The accent goes on the one series that makes the point, the rest take the context color. Label data directly; no legend for a single series; bar axes start at zero. Build native pptxgenjs charts with chartArea and plotArea filled to the panel tint. On the Google route charts arrive as images, so chart data also ships as a table file named (DD-MM-YY)Title Chart Data: a Google Sheet in the deck folder when the bridge worked, a CSV next to the .pptx otherwise. Name it in the speaker notes.

### Presented register

For a talk. Three tonal presets, three surface tiers each; Graphite is the default and matches the hex 0f0f0f chart standard.

| Role | Graphite | Paper | Ultramarine |
|---|---|---|---|
| Background, surface 1, surface 2 | 0F0F0F, 181B21, 23272E | F7F5F0, EEEBE3, E4E0D5 | F3F0E8, E7E2D6, DAD3C3 |
| Line, ink, muted | 353A44, EEF0F4, 98A0AE | CFC9BA, 1B1A17, 5C584F | BAB2A1, 111111, 57534A |
| Accent; structural hue for full bleed | F4B544; 1C2A45 | A8461F; 1A2B45 | 2A3BE0; 2A3BE0 |
| Ink, muted, accent on the structural hue | EEF0F4, A9B4C6, F4B544 | F7F5F0, A9B4C6, EE8B5E | F3F0E8, C9CFFA, E9FF5C |
| Good, bad, data only | 3FB97A, F0616D | 256B40, A8243C | 17603A, B4203A |

Rules: ink stays above 12 to 1 contrast on the base and surface tiers and above 4.5 to 1 on the structural hue, which the presets satisfy; the structural hue goes full bleed on the cover, the close and one section break per 4 to 6 content slides, never two in a row; the accent covers under 5 percent of a base slide and marks one idea; each surface family has exactly one accent. Depth comes from flat shapes, two or three per deck: a base colored panel inset 0.45 in on a full bleed slide, an oversized numeral crossing a panel edge, an ellipse 120 to 140 percent of the slide height pushed off the canvas in the structural hue, a chart inside a surface 1 panel, cards in surface 1 with the list numbers in accent, a photo under an ink rectangle at transparency 20 to 40. Body text never sits on the structural hue below 14 pt. Type: cover and statement 40 to 50 bold for 12 words or fewer, else 32; title 28 bold, 24 over 10 words, regular when the face is Instrument Serif; body 18; hero number 72 to 150 bold at 0.9 spacing; label 10 bold caps; tables and chart labels 10 to 12; source 9. Layouts, at least three a deck: cover, section, statement, two column (6 and 6, or 7 and 5 on a 12 column grid), chart with a takeaway column (7 and 5), big number, table, closing with the one ask. Font pairs by preset: Geist with Graphite, Instrument Serif and Inter with Paper, Newsreader and IBM Plex Sans with Ultramarine.

### Fonts by route

| Register and route | Titles | Body, numbers | Note |
|---|---|---|---|
| Reading, Google | Source Serif 4; EB Garamond when he says bank or banking | Source Sans 3 | both tabular by default; the narrowest, smallest x-height pair, which reads as understated |
| Reading, PowerPoint | Georgia | Arial | Arial for every number; Georgia has old style figures |
| Presented, Google | Geist; or Instrument Serif, regular only, 24 pt or larger; or Newsreader | Geist with Geist Mono numbers; Inter; IBM Plex Sans, in the same order | Geist and Inter never in the reading register: wide, tall x-height, proportional digits |
| Presented, PowerPoint | Georgia | Segoe UI | |

Two weights only, regular and bold, through the bold flag. Write the exact family name on every text run. Google Slides renders a family from its own font library by name and turns every other font into Arial; PowerPoint turns a missing font into Calibri or Arial. If a family is missing from the Slides font menu, fall back to PT Serif for titles, IBM Plex Sans for text and JetBrains Mono for numbers.

**Never:** centered body text; hero numbers, or anything larger than the title, on a reading page; a bold title on a reading page; header bars on content pages, lines under titles other than the one structural rule, edge stripes, small all caps labels above content titles other than the tracker; zebra stripes; cream or beige as a base other than the preset papers, never a tone such as F5F5DC or FAF0E6; gradients, glows, shadows or 3D; purple to cyan gradients, glass cards, abstract 3D renders; three icon cards by reflex, or an icon per bullet; the same background on every presented slide; topic label titles such as "Q3 Results" on content slides; a second accent; pure black text; semantic colors as decoration; text that overflows or depends on autofit (cut or split the slide instead).

## 4. Build and QA

1. Read the pptx skill SKILL.md for mechanics, then write one pptxgenjs script per deck. Speaker notes carry the talk track and full source detail. Check table cell margin units against `references/active-context.md`.
2. Name the file per house-style: (DD-MM-YY)Title With Proper Spaces.pptx.
3. Run the pptx skill validate.py. Install the route's fonts before rendering, or the preview lies about text width: on the Google route fetch the family files from raw.githubusercontent.com/google/fonts/main/ofl/<family>/ (folder names are lowercase with no spaces, such as sourcesans3, and the bracketed axis names in the file names must be URL encoded), copy a static file as it is, and turn a variable file into static Regular and Bold instances with the fontTools instancer (pin wdth to 100 and opsz to the axis default) into ~/.fonts, then fc-cache; use the installed fontTools API and verify the generated instances; no private helper script is bundled. If the fetch is blocked, or on the file route where Georgia, Arial and Segoe UI are not installed, leave 10 percent width slack and say so in the handover. Render every slide (its soffice.py to PDF, then pdftoppm) and look at each image. Fix overflow, overlaps, uneven gaps and weak contrast, then render again. Stop after two fix rounds and state any warning that remains.
4. Count body words a page with markitdown, or python-pptx if it is missing, excluding the furniture. A reading page outside 100 to 250, or a lead that renders on two lines, gets rewritten before delivery.
5. On the final render, read the content titles only. The title test must still pass.

## 5. Deliver

**Google route.** If a Drive doc titled `google-slides-bridge-config` exists, try the Apps Script bridge in `references/bridge.md` first (not deployed as of 23-09-2026). Otherwise, or when the bridge fails, use the fallback: put the .pptx and any chart data CSV in the session outputs folder and any connected folder, and tell him in one line how to import it: drag it into Drive with Convert uploads on, or open it and use File, Save as Google Slides. Name the step that failed.

Never upload the deck itself as base64 through Drive create_file. The model would have to type every character of the file; the size problem is in `references/active-context.md`.

**File route.** Put the .pptx in the session outputs folder, then commit it to a connected folder if one is connected. No Drive upload unless he asks.

**No Drive connector.** Skip the bridge lookup and the Sheet. Use the fallback.

Dated findings (Google conversion, pptxgenjs units, font availability, the measured reading register) are in `references/active-context.md`. Read it before the first build of a session.

Pairs with pitch-architect for the argument of persuasion decks, pptx for pptxgenjs mechanics and edits to existing files, diagram-design for figures placed on slides, viz-dashboards for chart color discipline off the slide, cold-read before an external deck ships, and house-style for every word on a slide.

Credits: rules borrowed from zairuilab/consulting-deck v0.3.0 and trev0rr/executive-slide-skill, both Apache 2.0. consulting-deck is the heavy option for a full evidence ledger engagement deck; it is not installed.