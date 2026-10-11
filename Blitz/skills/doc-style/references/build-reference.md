# Build reference

Read this while actually building a document. `SKILL.md` carries the rules that decide
what a document says; this file carries the builder sample, the size table, and the two
post-mortems behind the colour and bullet rules.

`references/styles.js` is the source of truth for every value below. If a number here ever
disagrees with it, `styles.js` wins.

## Workflow step 3: the builder sample

```javascript
const { createBuilders } = require('./styles.js');
const { Document, Packer } = require('docx');
const B = createBuilders('minimal', { numberedHeadings: false });

const doc = new Document({
  ...B.documentDefaults(),
  sections: [{
    properties: B.sectionProperties(),
    footers: { default: B.footer('Document Title') },
    children: [
      ...B.titleBlock('Document Title', 'Subtitle line'),
      ...B.verdictBlock('One to three sentences. The decision or bottom line, stated first.'),
      B.h1('First Section'),
      B.body('Body text.'),
      ...B.dataTable(
        ['Bucket', 'Committed', 'Trigger'],
        [['Marketing', 'USD 1.8M', 'Revenue > USD 150M']],
        { widths: [3600, 2600, 3160], rightAlignCols: [1] }
      ),
      B.bullet('A bullet.'),
      B.bullet('A sub-point, one level in.', 1),
    ],
  }],
});
```

Builders that return arrays (`titleBlock`, `verdictBlock`, `dataTable`) must be spread with `...`. Table widths must sum to `B.CONTENT_WIDTH` (9360); if omitted, columns split evenly.

Every heading goes through `B.h1` / `B.h2` / `B.h3`. Never construct a `Paragraph` with a `HeadingLevel` directly: a heading built that way carries no explicit run colour and falls back to Word's stock heading blue.

## Retired palettes

Two families are retired and appear in no current theme. The burgundy `6B2B3D` with `F2ECEE` / `F7F1F3` fills, and the drifted green editorial `2B6B47` with `F1F6F3` / `ECF2EE` fills (plus Georgia headings and a 22pt title), which was replaced on 12-08-26 when the editorial theme was pinned to the reference Google Doc. If any of these values, a Georgia heading run, or a 44 half-point title turns up in an `editorial` build, `styles.js` was stale: recopy it from `references/styles.js` and rebuild from source. Do not patch the colours in the output file.

## Type size

Regular text is **9pt** in every theme. Regular text means body paragraphs, bullets, and verdict body copy. In docx-js that is `size: 18`, because sizes are half-points. `bodySize: 18` is set on all three themes and is not a per-document choice.

Everything else derives from it, and the builders already do the arithmetic. Do not set a size by hand:

| Element | Half-points | Points |
|---|---|---|
| Body, bullets, verdict text | 18 | 9 |
| Table cells | 18 | 9 |
| Verdict label, shaded themes (`bodySize - 2`) | 16 | 8 |
| Footer (lives in `footer1.xml`, not `document.xml`) | 15 | 7.5 |
| H3 | 20, or 21 in `boardroom` | 10, 10.5 |
| H2 | 23 `minimal`, 24 `boardroom`, 22 `editorial` | 11.5, 12, 11 |
| H1 | 30 `minimal`, 32 `boardroom`, 26 `editorial` | 15, 16, 13 |
| Subtitle | 26, or 18 in `editorial` | 13, 9 |
| Title | 44, or 28 in `editorial` | 22, 14 |

The `editorial` sizes come straight from the pinned reference Google Doc
export of 12-08-26: title 14pt, H1 13pt, H2 11pt,
H3 10pt, everything Arial, headings and title in 111111, body paragraphs at
6pt-after (`bodyAfter: 120`), and the verdict a plain 0F766E left bar with no
label.

Heading sizes did not move when the body dropped to 9pt, so the hierarchy is now more separated, not less. H3 in `minimal` is 10pt bold against 9pt body, which reads as a heading because of the weight, not the size.

The themes previously ran `minimal` and `editorial` at 20 and `boardroom` at 21. A `styles.js` carrying either value is stale. `assertBodySize()` in the reference source throws at build time if any theme drifts, and the font-size check in `references/verify.sh` greps the built file, which catches a fully stale copy that has no assertion in it.

## Bullets: native list items, never typed dashes

Point form must be a **real list**, so it arrives in Google Docs as a native bulleted list the reader can indent, continue, and restyle. Never type an en dash, `-`, `*`, or any dash character at the start of a line to fake a bullet, and never put a dash marker inside the bullet's own text.

Always use `B.bullet(text)` for a top-level point and `B.bullet(text, 1)` for a sub-point. Nothing deeper than level 1.

The reference source carries the native bullet cascade: the round bullet U+25CF in Noto Sans Symbols, lowercase o in Courier New, the small square U+25AA in Noto Sans Symbols. Those are the exact markers Google Docs itself writes when it exports a bulleted list (verified against the pinned reference export), so a .docx built this way round-trips as a native list rather than as literal dash text.

U+25CF and U+25AA are ordinary BMP codepoints and survive any transport as literals; the old Symbol/Wingdings pair (U+F0B7 / U+F0A7) was Private Use Area and is retired. If a bullet level ever shows an empty `text: ''`, the file was transcribed rather than copied: recopy it.

### The dash-bullet failure, and how to catch it

An older copy of `styles.js` used an en dash (`text: '\u2013'`) at level 0. That copy still builds and still renders without error, so nothing warns you. In Word it produces a dash where the bullet should be; in Google Docs, which does not recognise a dash as a list marker, it imports as literal dash text followed by a wide tab, giving the long-dash-plus-gap look. This is the same class of defect as a stale palette: invisible until someone opens the file, and not fixable by editing the output.

Two guards, and you need both:

- The reference `styles.js` calls `assertBulletsNative()`, which throws at build time if any level marker is a dash, an asterisk, or empty. This catches a partly stale file.
- The bullet-marker check in `references/verify.sh` greps `word/numbering.xml` in the built .docx. This catches a fully stale `styles.js`, which by definition carries no assertion. Run it on every build.

Never fix a dash bullet by editing the output .docx or by search-and-replacing the marker. Recopy `styles.js` from `references/styles.js` and rebuild from source.
