# .docx mechanics for in-place contract edits

Read when `amend.py scan` shows anything under "hidden_text", "protection", "signed", auto numbering or an unusual font, and whenever an edit has to go beyond what `amend.py` does. Sources read 26-09-2026: ECMA-376 via docx4java and c-rex references, Microsoft Learn, LibreOffice source (writerfilter DomainMapper, FontTable, EmbeddedFontsManager), python-docx issues, anthropics/skills issue 489.

## What amend.py already handles

* Paragraph ops: `{"insert_after": "<anchor text>", "text": "<new>"}` clones the anchor's paragraph properties and first run's `w:rPr`; `{"delete": "<text>"}` removes the paragraph. In `track` these become an inserted paragraph mark plus `w:ins`, or `w:del` on every run plus a deleted paragraph mark, so accept merges cleanly.
* Keep chain: refuses when the chain would run past 40 paragraphs, which means the start pattern matched a body sentence; set `keep.start` to the block's first line.

* Split runs: Word breaks a sentence into many `w:r` (rsid, proofErr, formatting). `amend.py` maps every character of a paragraph to its `w:t`, so "old" text is found across runs; the replacement is written into the first run's `w:t`, keeping that run's `w:rPr`; later runs lose only the matched characters. It refuses a span that starts or crosses a tab.
* `xml:space="preserve"` is set on any `w:t` that starts or ends with a space; without it Word drops the space.
* Tracked changes: `w:del` holding the original runs with `w:t` renamed to `w:delText`, then `w:ins` with a run cloned from the first run's `w:rPr`. Both sit as children of `w:p`, never inside `w:r`. Revision `w:id` values are allocated above the highest id of any kind in every part; whether bookmarks and revisions share one id space is unverified, and allocating above all of them is safe either way (a collision has been seen to make Word call a file corrupt).
* Spacers: blank paragraphs added by cloning a blank sibling in the same cell, removed only if they hold no text, tab, break, field, drawing or bookmark, and never the last paragraph of a cell.
* Keep chain: `w:keepNext` and `w:keepLines` on the signature block, `w:cantSplit` on its table rows.
* Repack: `[Content_Types].xml` first, DEFLATE, forward slashes, no directory entries, XML declaration kept (`merge_runs.py` from the docx skill drops `standalone="yes"`; `amend.py` does not use it).
* Stops on `_xmlsignatures/`.

## When scan shows something else

| Scan field | Meaning | What to do |
|---|---|---|
| `numbering.auto` > 0 | Clause numbers are computed from `w:numPr`, never stored; deleting a numbered paragraph renumbers everything after it | Delete as a tracked change in the redline (numbers move only on accept); in the clean copy keep the paragraph with the contract's deleted-clause wording, or renumber and fix every typed cross-reference by hand |
| `hidden_text.content_controls` | Text inside `w:sdt` is skipped by python-docx and by naive searches | `amend.py` searches inside them; confirm the match count is exactly 1 |
| `hidden_text.text_boxes` | Text boxes carry the same text twice (mc:Choice and mc:Fallback) | Edit both copies or the file shows two different texts; `amend.py` will report 2 matches, so pass the edit once per copy with distinguishing context, or edit the XML by hand |
| `hidden_text.fields`, `bookmarks` | REF and PAGEREF fields point at hidden bookmarks; dropping a `w:bookmarkStart` pair prints "Error! Reference source not found." | Change only `w:t` text; never delete or reorder bookmark or comment range markers; if field results must refresh, set `w:dirty="true"` on the field and `w:updateFields` in settings.xml |
| `text_parts` beyond document.xml | Headers, footers, footnotes, comments hold text | A replacement is searched there too; a heading or party name in a header needs its own ledger row |
| `protection` = `trackedChanges` | The other side wants every change tracked | Deliver only the tracked copy; a clean copy is for his eyes |
| `protection` = `readOnly` or `forms` | Advisory only; raw XML edits bypass it | Say so, and ask before editing a protected file |
| `signed` = true | Digital signature parts present | Stop. Edit a copy and have it re-signed |
| `embedded_fonts` = true | `word/fonts/*.odttf` with `w:fontKey` in fontTable.xml | Never touch fontTable.xml or word/fonts; a key mismatch makes Word report unreadable content |

## Fonts and rendering

* `w:rFonts` carries ascii, hAnsi, eastAsia and cs, plus theme attributes that override the plain names; `w:sz` is in half-points. Copy a whole `w:rPr` from the neighbouring run; never compose one.
* LibreOffice honours keepNext, keepLines, widowControl and cantSplit on import (its writerfilter maps them) and prints its own layout to PDF; that this layout matches Word's is only as good as the fonts: it substitutes fonts it does not have. Metric-compatible substitutes give the same line breaks: Arial to Liberation Sans, Times New Roman to Liberation Serif, Calibri to Carlito, Cambria to Caladea, Arial Narrow to Liberation Sans Narrow.
* Liberation Sans Narrow is not in the Liberation 2.x packages (licence); build it from the 1.07 line in about two minutes: `apt-get install -y fontforge`, `git clone --depth 1 https://github.com/liberationfonts/liberation-sans-narrow`, then for each of Regular, Bold, Italic, BoldItalic: `fontforge -lang=ff -c 'Open($1); Generate($2)' liberation-sans-narrow/src/LiberationSansNarrow-<style>.sfd ~/.fonts/LiberationSansNarrow-<style>.ttf`, then `fc-cache -f`. Confirm with `fc-match "Arial Narrow"`.
* LibreOffice may show a stale NUMPAGES total in the footer. Word and DocuSign recompute it.
* Never save the deliverable through LibreOffice: it re-serialises the whole file and drops markup it does not model. Use it to render only.

## Validation

`validate.py out.docx --original in.docx` from the docx skill after every write; add `--author "<name>"` on the tracked copy so untracked text changes are reported. Then the three gates.
