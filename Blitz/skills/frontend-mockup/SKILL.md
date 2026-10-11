---
name: "frontend-mockup"
description: 'Concept screens for unbuilt products, HTML to PNG. Use on mock up, mockup, wireframe, draw the X screen, what would the page look like, screens for the BRD or PRD. Live pages: frontend-taste; flows: diagram-design.'
---

# Frontend Mockup

This skill draws screens for a product that does not exist yet. Each screen is one self-contained HTML page with invented sample data, rendered to PNG at 2x. The screen is the deliverable; a document is only built when he asks for one. frontend-taste owns pages that ship and their design gate; this skill owns concept screens. website-cloner owns copies of live sites, diagram-design owns flows and architecture, viz-dashboards owns charts as deliverables. doc-style owns the document and its checks; this skill hands it the figure. google-slides places the same PNG in a deck.

## Route first

| Request | Route |
|---|---|
| The screen itself: "mock up the X screen", "what would it look like" | This skill. PNG and HTML, no document |
| Screen figures for a BRD, PRD, spec, memo or deck | This skill, then doc-style or google-slides. See Figures |
| A design he will iterate on, when the session lists a Design artifact type | The Design type. The bar and rules below still apply to its content |
| A standalone concept page to click through or share | This skill's HTML, published as an artifact after artifact-design |
| Review of a page that ships, or "make it look premium" | frontend-taste |
| Boxes and arrows, a flow, an architecture | diagram-design |

## The bar

The reference is a full product screen at 1440 that reads as a shipped product. A screen passes when someone who knows the product type cannot tell it from a live app at a glance. That takes:

* **Full chrome.** Top nav with wordmark, tabs with one active, search, one primary action, account chip. A context header naming what the screen is about with its key figures. A status bar. Nothing floats on a bare canvas.
* **Product density.** 13 px body, 11 px labels, 17 to 20 px table rows, 8 to 12 px panel padding, 1 px hairlines. Every table carries 9 to 15 rows. No list has three rows.
* **Every region filled** with computed data that agrees across panels: the mid in the header equals the mid in the book, the ticket and the chart tag; totals are price times amount; every percentage is derived.
* **States shown.** One selected row, one active tab per tab set, one primary and one secondary button, at least one disabled or "Soon" element, at least one bracketed placeholder.
* **A real chart** where the product has one: candles or lines drawn in SVG from a seeded series, with gridlines, axis labels, a volume strip and a last price tag. Never a grey box labelled "chart".
* **Every control styled.** No default browser inputs, buttons, selects or checkboxes.

Fails, fix before you render: an empty region, lorem ipsum, a table under nine rows, one column of stacked boxes, body text at 16 px or more, a chart placeholder, buy and sell in green and red, a typed figure where a derived one belongs.

## Rules every mockup keeps

1. **Stamp.** The full screen ends with a static footer that reads "Concept mockup · sample data · not a live product". Never use a fixed bar: a full page capture draws it over the content. A crop loses the footer, so every figure caption says "concept mockup with sample data". Add PRIVATE when the brief is private.
2. **Computed sample data.** One data object holds the inputs. Code derives every total, fee, spread, balance, count and status from it. Never type a derived number. A state that does not depend on a number, such as "confirmations met", is an input.
3. **Placeholders.** An unknown input shows in brackets, such as [CONTRACTING ENTITY] or [N] confirmations. Each figure derived from it shows in brackets too. The document lists each placeholder as an open item.
4. **No real marks.** Show no real people, client names, logos or trademarks. Do not copy the signature colors or icons of a named product. "binance.com style" means the generic pattern of order book, chart and ticket, never that brand's look.
5. **No employer data.** Show no current employer name, product, ticker, client or figure, and no data from his job.
6. **Domain copy.** In a regulated product, the domain skill decides what a screen may show. Inside a project that has its own skills, load the project skill that owns the screen's area and the project's veto skill, as the project's skill map lists them. For example, no yield rate appears before a licence.
7. **House text.** UI copy follows house-style: no em or en dashes, ranges as X to Y, and dates DD-MM-YYYY with the time zone named.
8. **Offline page.** Inline CSS, inline SVG icons, system fonts with Arial first (the container has no Inter or Helvetica; Arial resolves to Liberation Sans, a bare sans-serif to DejaVu Sans, which looks dated). Load no CDN script, web font or remote image.
9. **Buy and sell colors.** Blue for buy and orange for sell, not green and red, because color blind viewers can tell blue and orange apart.

## Composition

* **Shell.** `.app{width:1440px}` as a column: nav 48, context header 56 to 60, main grid, bottom panel, status bar 26. The main grid names its fixed columns and one 1fr, such as `grid-template-columns:272px 1fr 300px;gap:1px;background:var(--line)`, which draws the hairlines. Fixed widths plus gaps must fit the viewport; the 1fr column takes the rest.
* **Panel anatomy.** Title row (14 px bold, its control at the right), column header row (11 px muted), rows, footer summary. Numbers right aligned in `.num`. Depth bars: one absolute bar per row, `right:0`, opacity .22, width as a share of the largest row, in that side's color.
* **Ticket.** Two forms side by side, buy left in blue, sell right in orange: available, price, amount, a slider with five stops, total, pay from or settle to, one full width button.
* **Mobile 390.** One column, bottom tab bar 56, the ticket as a sheet, same tokens.
* **Light theme.** Swap the tokens in `:root`. Buy stays blue, sell stays orange.
* **SVG width.** Read the container: `const W = el.clientWidth - paddingX`. A hard coded width wider than its column stretches the grid past the viewport and fails the gate.
* **Axis labels.** Anchor the first label `start` and the last `end`, or a label clips at the edge. The gate cannot see SVG text, so look.
* **Callout badge.** Place it inside its region at the top left, never outside, where it covers the neighbour.

Chart generator, drop in as is; `f` is the number formatter from the shell:

```javascript
function candles(el, D) {   // D.mid, D.hi, D.lo, D.n candles, D.tf minutes, D.end [hh, mm], D.seed
  let s = D.seed; const r = () => (s = s * 16807 % 2147483647) / 2147483647;
  const c = []; let p = D.mid - (D.hi - D.lo) * 0.35;
  for (let i = 0; i < D.n; i++) { const o = p, cl = o + (r() - 0.48) * (D.hi - D.lo) / 8; c.push({ o, h: Math.max(o, cl) + r() * (D.hi - D.lo) / 15, l: Math.min(o, cl) - r() * (D.hi - D.lo) / 15, c: cl, v: 60 + r() * 240 }); p = cl; }
  const d = D.mid - c[c.length - 1].c; c.forEach(k => { k.o += d; k.h += d; k.l += d; k.c += d; });
  const ma = (n, i) => i + 1 < n ? null : c.slice(i + 1 - n, i + 1).reduce((t, k) => t + k.c, 0) / n;
  const W = el.clientWidth - 24, H = 300, VH = 56, L = 4, R = 64, T = 8, B = 20, cw = (W - L - R) / D.n;
  const lo = Math.min(...c.map(k => k.l)), hi = Math.max(...c.map(k => k.h)), y = v => T + (hi - v) / (hi - lo) * (H - T - B), mv = Math.max(...c.map(k => k.v));
  let g = `<svg width="${W}" height="${H + VH + 22}">`;
  for (let i = 0; i <= 4; i++) { const v = lo + (hi - lo) * i / 4; g += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="#1e2126"/><text x="${W - R + 6}" y="${y(v) + 3}">${f(v, 4)}</text>`; }
  c.forEach((k, i) => { const x = L + i * cw + cw / 2, col = k.c >= k.o ? 'var(--buy)' : 'var(--sell)', bh = k.v / mv * VH;
    g += `<line x1="${x}" x2="${x}" y1="${y(k.h)}" y2="${y(k.l)}" stroke="${col}"/><rect x="${x - cw * .32}" y="${y(Math.max(k.o, k.c))}" width="${cw * .64}" height="${Math.max(1, Math.abs(y(k.o) - y(k.c)))}" fill="${col}"/><rect x="${x - cw * .32}" y="${H + 8 + VH - bh}" width="${cw * .64}" height="${bh}" fill="${col}" opacity=".7"/>`; });
  [[7, 'var(--accent)'], [25, '#facc15']].forEach(([n, col]) => g += `<polyline fill="none" stroke="${col}" stroke-width="1.2" points="${c.map((k, i) => ma(n, i)).map((v, i) => v == null ? '' : `${L + i * cw + cw / 2},${y(v)}`).join(' ')}"/>`);
  g += `<line x1="${L}" x2="${W - R}" y1="${y(D.mid)}" y2="${y(D.mid)}" stroke="var(--accent)" stroke-dasharray="3 3"/><rect x="${W - R + 2}" y="${y(D.mid) - 8}" width="58" height="16" rx="2" fill="var(--accent)"/><text x="${W - R + 31}" y="${y(D.mid) + 4}" text-anchor="middle" style="fill:#06221f;font-weight:700">${f(D.mid, 4)}</text>`;
  for (let i = 0; i < D.n; i += 12) { const m = ((D.end[0] * 60 + D.end[1] - (D.n - 1 - i) * D.tf) % 1440 + 1440) % 1440; g += `<text x="${L + i * cw + cw / 2}" y="${H + VH + 20}" text-anchor="${i ? 'middle' : 'start'}">${String(m / 60 | 0).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}</text>`; }
  el.innerHTML = g + '</svg>'; return { c, ma };
}
```

Use `c` for the OHLC strip and `ma(7, c.length - 1)` for the indicator readout, so they agree with the drawing.

## Build

1. **Brief.** Put the brief in an HTML comment at the top of the page. It names the screen, the requirement the screen proves, the viewport (desktop 1440 wide, mobile 390 wide), the theme and the callouts.
2. **Page.** Start from the shell below and the Composition section. Put `data-callout="n"` on each element a requirement names. Put `data-shot="Name"`, in title case, on each region a document needs as a detail crop.
3. **Render and check.** Run `NODE_PATH=$(npm root -g) node render.js "(DD-MM-YY)Title Screen.html" "(DD-MM-YY)Title Screen.png" 1440 900`. It saves each `data-shot` region as `(DD-MM-YY)Title Screen Name.png`. It exits 1 on a missing stamp, an em or en dash, clipped text, horizontal overflow or any external request. Fix the page and rerun; never ship on exit 1.
4. **Callouts.** Render the callout version to its own file, such as `(DD-MM-YY)Title Screen Callouts.png`, with `callouts` as the fifth argument. render.js skips the crops on that pass, so the clean crops stay clean. Build the callout table with `B.dataTable`: callout, element and requirement ID.
5. **Look.** Read every PNG at full size and check it against The bar and its fail list. Check alignment, overlap, truncation, axis labels and callout placement. Check that the numbers agree across panels. A pass on render.js is not a pass on the look.

Shell (dark default; for a light theme, swap the color tokens in `:root`):

```html
<!doctype html><html><head><meta charset="utf-8"><style>
:root{--bg:#0f0f0f;--panel:#16181c;--panel2:#1c1f24;--line:#262a30;--text:#e6e8eb;--muted:#8a9099;--dim:#5c626b;--accent:#2dd4bf;--buy:#3b82f6;--sell:#f97316}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font:13px/1.4 Arial,Helvetica,sans-serif;width:100%}
.app{width:1440px;min-height:900px;display:flex;flex-direction:column}
.num{font-variant-numeric:tabular-nums}
svg text{font:10px Arial,Helvetica,sans-serif;fill:var(--muted)}
.stamp{margin-top:24px;padding:6px 24px;font-size:11px;color:var(--muted);border-top:1px solid var(--line);text-align:right}
.co{position:absolute;width:22px;height:22px;border-radius:11px;background:#facc15;color:#111;font:700 12px/22px Arial;text-align:center}
</style></head><body>
<!-- brief here, then screen markup inside <div class="app"> -->
<div class="stamp">Concept mockup · sample data · not a live product</div>
<script>
const D = { /* inputs only */ };
const f = (n, d = 2) => n.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
// fill every derived field from D here
if (location.search.includes('callouts=1')) document.querySelectorAll('[data-callout]').forEach(e => {
  const r = e.getBoundingClientRect(), b = document.createElement('div'); b.className = 'co'; b.textContent = e.dataset.callout;
  b.style.left = (r.left + scrollX + 6) + 'px'; b.style.top = (r.top + scrollY + 6) + 'px';
  document.body.appendChild(b); });
</script></body></html>
```

`render.js`:

```javascript
// node render.js in.html out.png [width] [height] [callouts]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [, , input, output, w = '1440', h = '900', callouts = ''] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 2 });
  const external = [];
  page.on('request', r => { if (!/^(file|data):/.test(r.url())) external.push(r.url()); });
  await page.goto('file://' + path.resolve(input) + (callouts ? '?callouts=1' : ''));
  await page.waitForTimeout(250);
  const rep = await page.evaluate(() => {
    const t = document.body.innerText;
    return { stamp: /concept mockup/i.test(t) && /sample data/i.test(t),
      dashes: (t.match(/[‒-―]/g) || []).length,
      clipped: [...document.querySelectorAll('body *')].filter(e => !e.children.length && e.innerText
        && e.scrollWidth > e.clientWidth + 1).map(e => e.innerText.slice(0, 40)).slice(0, 10),
      width: document.documentElement.scrollWidth };
  });
  await page.screenshot({ path: output, fullPage: true });
  if (!callouts) for (const el of await page.$$('[data-shot]')) {
    await el.screenshot({ path: output.replace(/\.png$/, ` ${await el.getAttribute('data-shot')}.png`) });
  }
  await browser.close();
  Object.assign(rep, { external, overflow: rep.width > +w });
  console.log(JSON.stringify(rep, null, 1));
  process.exit(!rep.stamp || rep.dashes || rep.clipped.length || external.length || rep.overflow ? 1 : 0);
})();
```

Where no headless Chromium runs, publish the HTML as an artifact. Say in one line that the PNG was not rendered.

## Figures in doc-style documents

* **Print size.** The content width C is `B.CONTENT_WIDTH / 15` CSS px. Text of s CSS px, in a region W CSS px wide, prints at s × (C ÷ W) × 0.75 pt. A full 1440 screen on a portrait page prints 13 px text at about 4.2 pt: that is the low quality document look, so a full screen is an overview only. Put the detail in crops of 860 CSS px or less, which print 13 px text at 7 pt or more. When he wants the whole screen readable inside the document, doc-style gives it a landscape section; otherwise the full PNG goes beside the document.
* **Builder.** Build each figure with this helper. It composes through `B.body` and `B.run` and adds only an `ImageRun`, so it keeps doc-style's builder rule. It overrides the paragraph spacing, because the default line spacing of `B.body` clips an image.

```javascript
const { ImageRun } = require('docx');
function figure(B, png, caption) {                         // png rendered at 2x
  const buf = require('fs').readFileSync(png);
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);      // PNG header
  const width = Math.min(B.CONTENT_WIDTH / 15, Math.round(w / 2)), height = Math.round(width * h / w);
  return [
    B.body([new ImageRun({ type: 'png', data: buf, transformation: { width, height } })],
      { para: { spacing: { before: 120, after: 60 }, keepNext: true } }),
    B.body([B.run(caption, { italics: true })]),
  ];
}
// children.push(...figure(B, 'screen.png', 'Figure 1. Trading screen, concept mockup with sample data.'));
```

* **Numbering.** Number figures in document order: each overview, then its crops.
* **Order.** The figure comes first, then its italic caption, then the callout table, then any prose about it. This is doc-style's table rule, applied to figures.
* **Which render.** A figure with a callout table uses the callout render. Every other figure uses the clean render.
* **Length.** Figure pages count toward doc-style's page limit.
* **Checks.** Run doc-style's verify.sh and its page render as usual. Look at every figure page.
* **Google Doc.** When the Drive connector cannot carry an image (see the dated block), each Google Doc caption adds "Image in the Word copy." Nothing else changes. Send the .docx and the PNGs with the file tool. Tell him in one line that the images go in with Insert, Image. Never retype base64 into a tool call.

## Deliver

* The full PNG and the crops go out for display, the HTML beside them with the same house name. Never only a document.
* Publish the HTML as an artifact when he will click through it or share it.
* Name the open placeholders in one line.

## Host and project prerequisites

Inspect the actual browser, rendering tools, fonts, document helpers and delivery route before relying on them. Tool paths, versions and prior render results are not supplied by this package. Use task-selected colors and verify the current artifact at representative sizes.

Pairs with:
* doc-style, for the document and verify.sh.
* google-slides, for decks.
* frontend-taste, when the look must pass a design gate.
* the project's own skills, from its skill map, for screen copy inside that project.
* cold-read, before a document with figures leaves his hands.