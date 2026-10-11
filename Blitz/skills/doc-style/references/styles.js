// styles.js - house document theme system.
// Usage:
//   const { createBuilders } = require('./styles.js');
//   const B = createBuilders('minimal', { numberedHeadings: false });
// Then compose documents exclusively from B.* builders. Do not hand-roll
// Paragraph/TextRun styling outside this module; that is how drift happens.
//
// This file is disposable. Overwrite it from the skill's references/styles.js on every run.
// Never carry a copy forward between documents or sessions.

const {
  Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
  LevelFormat, Footer, PageNumber, TabStopType,
} = require('docx');

// A4 with 1240-twip left/right margins => usable width; keep tables at this.
const CONTENT_WIDTH = 9360;

// Bullet glyphs: the exact markers Google Docs writes when it exports a
// bulleted list, verified against the pinned editorial reference export:
// round bullet U+25CF in
// Noto Sans Symbols, lowercase o in Courier New, small square U+25AA in
// Noto Sans Symbols. All BMP codepoints, safe in any transport. The old
// Symbol/Wingdings PUA pair (F0B7/F0A7) is retired.
const BULLET_ROUND = '\u25CF';   // level 0, Noto Sans Symbols
const BULLET_SQUARE = '\u25AA';  // level 2, Noto Sans Symbols

// Retired palettes. No theme below may use these values.
// 6B2B3D / F2ECEE / F7F1F3 was the old editorial burgundy.
// 2B6B47 / F1F6F3 / ECF2EE was the drifted green editorial, replaced on
// 12-08-26 by the theme pinned to the reference Google Doc.
const RETIRED_COLORS = ['6B2B3D', 'F2ECEE', 'F7F1F3', '2B6B47', 'F1F6F3', 'ECF2EE'];

// House regular size, in half-points. Body paragraphs, bullets and verdict copy
// are 9pt in every theme. Table cells, verdict labels and the footer derive from
// it. This is a house constant, not a per-document choice: a theme that carries
// 20 or 21 is a stale file, from before the size was standardised.
const BODY_SIZE = 18;

// Markers that must never appear as a list level marker. An older styles.js used
// an en dash at level 0; it builds and renders without complaint, but Google Docs
// does not treat a dash as a list marker, so the list imports as literal dash text
// with a wide tab after it. Reject the whole family, plus empty (dropped PUA char).
const BANNED_MARKERS = [
  '', '-', '*', '·', '‐', '‑', '‒',
  '–', '—', '―', '−',
];

const THEMES = {
  // Default. Internal circulation, high-frequency deliverables.
  minimal: {
    bodyFont: 'Arial', headFont: 'Arial',
    bodySize: 18,             // half-points => 9pt (house regular size)
    accent: '0F766E',
    accentLight: 'F0F7F6',
    ruleColor: 'DDDDDD',
    tableHeaderFill: 'FFFFFF', tableHeaderText: '0F766E',
    tableBorder: 'E2E2E2',
    verdictStyle: 'leftbar',
    h1: 30, h2: 23, h3: 20,
    h3Italic: false,
  },
  // External counterparties; when the document must carry visual authority.
  boardroom: {
    bodyFont: 'Georgia', headFont: 'Arial',
    bodySize: 18,             // 9pt (house regular size)
    accent: '1F2A44',
    accentLight: 'EEF1F6',
    ruleColor: '1F2A44',
    tableHeaderFill: '1F2A44', tableHeaderText: 'FFFFFF',
    tableBorder: 'C9CFDA',
    verdictStyle: 'shaded',
    h1: 32, h2: 24, h3: 21,
    h3Italic: true,
  },
  // Legal/compliance review, reference documents. Pair with numberedHeadings.
  // PINNED EXACTLY to a reference Google Doc, extracted from its
  // .docx export on 12-08-26. Arial only, black headings 111111, teal 0F766E
  // accent, 14pt title, 9pt subtitle with a DDDDDD rule, plain left-bar verdict
  // with no label, white table header with a 0F766E underline, E2E2E2 hairline
  // cells, body 9pt with 6pt after and 1.15 line. Do not restore Georgia, the
  // green 2B6B47, or the burgundy 6B2B3D: all retired.
  editorial: {
    bodyFont: 'Arial', headFont: 'Arial',
    bodySize: 18,             // 9pt (house regular size)
    accent: '0F766E',
    accentLight: 'F0F7F6',
    ruleColor: 'DDDDDD',
    tableHeaderFill: 'FFFFFF', tableHeaderText: '111111',
    tableBorder: 'E2E2E2',
    verdictStyle: 'leftbar-plain',
    h1: 26, h2: 22, h3: 20,   // 13 / 11 / 10 pt, per the reference styles.xml
    h3Italic: false,
    headColor: '111111', h3Color: '111111',
    titleSize: 28, subtitleSize: 18, subtitleColor: '111111',
    bodyAfter: 120,           // 6pt after body paragraphs, per the reference
  },
};

// Fail loudly at build time rather than quietly shipping a burgundy document.
function assertPaletteCurrent() {
  for (const [name, t] of Object.entries(THEMES)) {
    for (const [key, val] of Object.entries(t)) {
      if (typeof val === 'string' && RETIRED_COLORS.includes(val.toUpperCase())) {
        throw new Error(
          `styles.js is stale: theme "${name}" uses retired colour ${val} at ${key}. ` +
          `Recopy styles.js from the doc-style skill's references/styles.js.`
        );
      }
    }
  }
}

// Fail loudly at build time rather than quietly shipping a 10pt document.
function assertBodySize() {
  for (const [name, t] of Object.entries(THEMES)) {
    if (t.bodySize !== BODY_SIZE) {
      throw new Error(
        `styles.js is stale: theme "${name}" sets bodySize ${t.bodySize}, ` +
        `house regular size is ${BODY_SIZE} half-points (9pt). ` +
        `Recopy styles.js from the doc-style skill's references/styles.js.`
      );
    }
  }
}

// Fail loudly at build time rather than quietly shipping dash "bullets".
function assertBulletsNative(levels) {
  for (const lvl of levels) {
    if (BANNED_MARKERS.includes(lvl.text)) {
      throw new Error(
        `styles.js is stale: bullet level ${lvl.level} uses marker ${JSON.stringify(lvl.text)}, ` +
        `which Google Docs imports as literal text rather than a list marker. ` +
        `Level 0 must be the round bullet U+25CF in Noto Sans Symbols. ` +
        `Recopy styles.js from the doc-style skill's references/styles.js.`
      );
    }
  }
}

function createBuilders(themeName = 'minimal', opts = {}) {
  assertPaletteCurrent();
  assertBodySize();
  const T = THEMES[themeName];
  if (!T) throw new Error(`Unknown theme "${themeName}". Use: ${Object.keys(THEMES).join(', ')}`);
  const numberedHeadings = !!opts.numberedHeadings;

  // Auto section numbering state (1, 1.1, 1.2, 2, 2.1 ...)
  let h1Count = 0, h2Count = 0;

  const noBorders = () => {
    const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
    return { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none };
  };

  // Native Word / Google Docs bullet cascade: round bullet, lowercase o
  // (Courier New), small square. These are the exact markers Google Docs writes
  // when it exports a bulleted list, so the .docx imports as a native list
  // instead of literal dash characters.
  const bulletLevel = (level, text, font, left) => ({
    level, format: LevelFormat.BULLET, text,
    style: { paragraph: { indent: { left, hanging: 220 } }, run: { font } },
  });

  // Numbering config: passed through documentDefaults().
  const bulletLevels = [
    bulletLevel(0, BULLET_ROUND, 'Noto Sans Symbols', 360),
    bulletLevel(1, 'o', 'Courier New', 720),
    bulletLevel(2, BULLET_SQUARE, 'Noto Sans Symbols', 1080),
  ];
  assertBulletsNative(bulletLevels);

  const numbering = { config: [{ reference: 'bullets', levels: bulletLevels }] };

  const body = (text, opts2 = {}) => new Paragraph({
    children: Array.isArray(text)
      ? text // allow pre-built TextRun arrays for mixed emphasis
      : [new TextRun({ text, font: T.bodyFont, size: T.bodySize, ...opts2.run })],
    spacing: { after: T.bodyAfter || 140, line: 276 },
    ...opts2.para,
  });

  // Inline runs for mixed-emphasis body text: body([run('x'), run('y', {bold:true})])
  const run = (text, o = {}) => new TextRun({ text, font: T.bodyFont, size: T.bodySize, ...o });

  // Reject text that carries its own typed marker; the list supplies the marker.
  const bullet = (text, level = 0) => {
    if (typeof text === 'string' && /^\s*[-*•·‐-―−]\s/.test(text)) {
      throw new Error(
        `bullet() text begins with a typed marker: ${JSON.stringify(text.slice(0, 48))}. ` +
        `Pass the text only.`
      );
    }
    return new Paragraph({
      children: Array.isArray(text)
        ? text
        : [new TextRun({ text, font: T.bodyFont, size: T.bodySize })],
      numbering: { reference: 'bullets', level },
      spacing: { after: 80, line: 276 },
    });
  };

  const h1 = (text) => {
    h1Count += 1; h2Count = 0;
    const label = numberedHeadings ? `${h1Count}. ` : '';
    return new Paragraph({
      heading: HeadingLevel.HEADING_1,
      children: [new TextRun({ text: label + text, font: T.headFont, size: T.h1, bold: true, color: T.headColor || T.accent })],
      spacing: { before: 320, after: 160 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: T.ruleColor, space: 4 } },
    });
  };

  const h2 = (text) => {
    h2Count += 1;
    const label = numberedHeadings ? `${h1Count}.${h2Count} ` : '';
    return new Paragraph({
      heading: HeadingLevel.HEADING_2,
      children: [new TextRun({ text: label + text, font: T.headFont, size: T.h2, bold: true, color: T.headColor || T.accent })],
      spacing: { before: 260, after: 120 },
    });
  };

  const h3 = (text) => new Paragraph({
    heading: HeadingLevel.HEADING_3,
    children: [new TextRun({ text, font: T.headFont, size: T.h3, bold: true, italics: T.h3Italic, color: T.h3Color || '333333' })],
    spacing: { before: 200, after: 100 },
  });

  // Title block: title and subtitle, with a rule beneath the last line.
  const titleBlock = (title, subtitle) => {
    const rule = { bottom: { style: BorderStyle.SINGLE, size: 4, color: T.ruleColor, space: 8 } };
    if (subtitle) {
      return [
        new Paragraph({
          children: [new TextRun({ text: title, font: T.headFont, size: T.titleSize || 44, bold: true, color: '111111' })],
          spacing: { after: 60 },
        }),
        new Paragraph({
          children: [new TextRun({ text: subtitle, font: T.headFont, size: T.subtitleSize || 26, color: T.subtitleColor || T.accent })],
          spacing: { after: 240 },
          border: rule,
        }),
      ];
    }
    return [
      new Paragraph({
        children: [new TextRun({ text: title, font: T.headFont, size: T.titleSize || 44, bold: true, color: '111111' })],
        spacing: { after: 240 },
        border: rule,
      }),
    ];
  };

  // Verdict block. Always the first element after the title block.
  // Returns an array, so spread it into children.
  const verdictBlock = (text, label = 'Verdict') => {
    // Reference form: a plain teal left bar, no label, one bordered paragraph
    // per blank-line-separated block of the input. Adjacent identical borders
    // merge into one continuous bar when rendered.
    if (T.verdictStyle === 'leftbar-plain') {
      const blocks = Array.isArray(text) ? [text] : String(text).split(/\n\n+/);
      return blocks.map(t => new Paragraph({
        children: Array.isArray(t)
          ? t
          : [new TextRun({ text: t, font: T.bodyFont, size: T.bodySize })],
        border: { left: { style: BorderStyle.SINGLE, size: 24, color: T.accent, space: 12 } },
        spacing: { before: 120, after: 240, line: 276 },
        indent: { left: 240 },
      }));
    }
    if (T.verdictStyle === 'leftbar') {
      return [new Paragraph({
        children: [
          new TextRun({ text: label.toUpperCase() + '  ', font: T.headFont, size: T.bodySize, bold: true, color: T.accent }),
          new TextRun({ text, font: T.bodyFont, size: T.bodySize }),
        ],
        border: { left: { style: BorderStyle.SINGLE, size: 24, color: T.accent, space: 12 } },
        spacing: { before: 120, after: 240, line: 276 },
        indent: { left: 240 },
      })];
    }
    return [
      new Table({
        columnWidths: [CONTENT_WIDTH],
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        borders: noBorders(),
        rows: [new TableRow({
          children: [new TableCell({
            width: { size: CONTENT_WIDTH, type: WidthType.DXA },
            shading: { type: ShadingType.CLEAR, fill: T.accentLight },
            margins: { top: 160, bottom: 160, left: 200, right: 200 },
            children: [
              new Paragraph({
                children: [new TextRun({ text: label.toUpperCase(), font: T.headFont, size: T.bodySize - 2, bold: true, color: T.accent })],
                spacing: { after: 60 },
              }),
              new Paragraph({
                children: [new TextRun({ text, font: T.bodyFont, size: T.bodySize })],
                spacing: { after: 0, line: 276 },
              }),
            ],
          })],
        })],
      }),
      new Paragraph({ children: [], spacing: { after: 120 } }),
    ];
  };

  // Data table. headers: string[]; rows: string[][]; rightAlignCols: index set for numeric cols.
  // Column widths must sum to CONTENT_WIDTH; pass widths or they are split evenly.
  const dataTable = (headers, rows, { widths, rightAlignCols = [] } = {}) => {
    const nCols = headers.length;
    const colW = widths || Array(nCols).fill(Math.floor(CONTENT_WIDTH / nCols));
    const diff = CONTENT_WIDTH - colW.reduce((a, b) => a + b, 0);
    colW[colW.length - 1] += diff; // absorb rounding
    const right = new Set(rightAlignCols);

    const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: T.tableBorder };
    const headerBottom = { style: BorderStyle.SINGLE, size: 8, color: T.accent };
    const noneB = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };

    const cell = (text, i, header = false) => new TableCell({
      width: { size: colW[i], type: WidthType.DXA },
      shading: header ? { type: ShadingType.CLEAR, fill: T.tableHeaderFill } : undefined,
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      borders: header && T.tableHeaderFill === 'FFFFFF'
        ? { top: noneB, bottom: headerBottom, left: noneB, right: noneB }
        : { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder },
      children: [new Paragraph({
        alignment: right.has(i) ? AlignmentType.RIGHT : AlignmentType.LEFT,
        children: [new TextRun({
          text: String(text), font: header ? T.headFont : T.bodyFont, size: T.bodySize,
          bold: header, color: header ? T.tableHeaderText : '222222',
        })],
        spacing: { after: 0 },
      })],
    });

    return [
      new Table({
        columnWidths: colW,
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        rows: [
          new TableRow({ tableHeader: true, children: headers.map((h, i) => cell(h, i, true)) }),
          ...rows.map(r => new TableRow({ children: r.map((c, i) => cell(c, i)) })),
        ],
      }),
      new Paragraph({ children: [], spacing: { after: 120 } }), // breathing room after table
    ];
  };

  // Footer: doc title left, "Page X of Y" right, hairline rule above.
  const footer = (docTitle) => new Footer({
    children: [new Paragraph({
      tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_WIDTH }],
      children: [
        new TextRun({ text: docTitle, font: T.bodyFont, size: 15, color: '999999' }),
        new TextRun({ children: ['\t'], font: T.bodyFont, size: 15 }),
        new TextRun({ children: ['Page ', PageNumber.CURRENT, ' of ', PageNumber.TOTAL_PAGES], font: T.bodyFont, size: 15, color: '999999' }),
      ],
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'DDDDDD', space: 6 } },
    })],
  });

  // Standard section properties + default run style for `new Document(...)`.
  const documentDefaults = () => ({
    numbering,
    styles: { default: { document: { run: { font: T.bodyFont, size: T.bodySize } } } },
  });

  const sectionProperties = () => ({
    page: { margin: { top: 1080, bottom: 1080, left: 1240, right: 1240 } }, // A4 default size
  });

  return {
    T, CONTENT_WIDTH, numbering,
    body, run, bullet, h1, h2, h3,
    titleBlock, verdictBlock, dataTable, footer,
    documentDefaults, sectionProperties, noBorders,
  };
}

module.exports = { THEMES, RETIRED_COLORS, BODY_SIZE, createBuilders, CONTENT_WIDTH };
