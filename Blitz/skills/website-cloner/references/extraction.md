# Extraction Scripts

Run these through `javascript_tool {action:"javascript_exec", text: "<script>", tabId}`. Each returns a JSON string. That tool is sanctioned for inspection, which is exactly this. Never use it to patch the clone's UI; edit source files instead.

## 1. Global audit

One pass over the whole page. Run this first, before any per-section work.

```javascript
JSON.stringify({
  images: [...document.querySelectorAll('img')].map(img => ({
    src: img.currentSrc || img.src,
    alt: img.alt,
    natural: [img.naturalWidth, img.naturalHeight],
    parentClasses: img.parentElement?.className?.toString().slice(0, 120),
    siblingImgs: img.parentElement ? img.parentElement.querySelectorAll('img').length : 0,
    position: getComputedStyle(img).position,
    zIndex: getComputedStyle(img).zIndex
  })),
  videos: [...document.querySelectorAll('video')].map(v => ({
    src: v.currentSrc || v.src || v.querySelector('source')?.src,
    poster: v.poster, autoplay: v.autoplay, loop: v.loop, muted: v.muted
  })),
  backgroundImages: [...document.querySelectorAll('*')]
    .map(el => ({ el, bg: getComputedStyle(el).backgroundImage }))
    .filter(x => x.bg && x.bg !== 'none')
    .map(x => ({ url: x.bg, el: x.el.tagName + '.' + (x.el.className?.toString().split(' ')[0] || '') })),
  fonts: [...new Set([...document.querySelectorAll('h1,h2,h3,h4,p,span,a,button,li,code,label')]
    .map(el => getComputedStyle(el).fontFamily))],
  favicons: [...document.querySelectorAll('link[rel*="icon"], link[rel="manifest"]')]
    .map(l => ({ rel: l.rel, href: l.href, sizes: l.sizes?.toString() })),
  meta: [...document.querySelectorAll('meta[property^="og:"], meta[name^="twitter:"]')]
    .map(m => ({ k: m.getAttribute('property') || m.getAttribute('name'), v: m.content })),
  svgCount: document.querySelectorAll('svg').length,
  // Framework and library fingerprints
  stack: {
    next: !!document.querySelector('#__NEXT_DATA__') || !!window.__NEXT_DATA__,
    nuxt: !!window.__NUXT__,
    react: !!document.querySelector('[data-reactroot]') || !!window.React,
    lenis: !!document.querySelector('.lenis') || !!window.Lenis,
    locomotive: !!document.querySelector('[data-scroll-container]'),
    gsap: !!window.gsap,
    framerMotion: !!document.querySelector('[style*="transform-origin"]')
  },
  scrollSnap: [...document.querySelectorAll('*')]
    .filter(el => { const v = getComputedStyle(el).scrollSnapType; return v && v !== 'none'; })
    .map(el => el.tagName + '.' + (el.className?.toString().split(' ')[0] || ''))
});
```

## 2. Per-component walk

Run once per section container. Replace the selector at the bottom. Filters out default values so the output stays readable, and caps depth and breadth so it does not blow up the response.

```javascript
(function (selector) {
  const el = document.querySelector(selector);
  if (!el) return JSON.stringify({ error: 'Not found: ' + selector });
  const PROPS = [
    'fontSize','fontWeight','fontFamily','lineHeight','letterSpacing','color',
    'textTransform','textDecoration','textAlign','backgroundColor','backgroundImage',
    'padding','paddingTop','paddingRight','paddingBottom','paddingLeft',
    'margin','marginTop','marginRight','marginBottom','marginLeft',
    'width','height','maxWidth','minWidth','maxHeight','minHeight',
    'display','flexDirection','flexWrap','justifyContent','alignItems','gap',
    'gridTemplateColumns','gridTemplateRows',
    'borderRadius','border','borderTop','borderBottom','borderLeft','borderRight',
    'boxShadow','overflow','overflowX','overflowY',
    'position','top','right','bottom','left','zIndex',
    'opacity','transform','transition','animation','cursor',
    'objectFit','objectPosition','mixBlendMode','filter','backdropFilter',
    'whiteSpace','textOverflow','webkitLineClamp'
  ];
  const SKIP = new Set(['none','normal','auto','0px','rgba(0, 0, 0, 0)','static','visible','0s']);
  const styles = e => {
    const cs = getComputedStyle(e), out = {};
    PROPS.forEach(p => { const v = cs[p]; if (v && !SKIP.has(v)) out[p] = v; });
    return out;
  };
  const walk = (e, d) => {
    if (d > 4) return null;
    const kids = [...e.children];
    const onlyText = e.childNodes.length === 1 && e.childNodes[0].nodeType === 3;
    return {
      tag: e.tagName.toLowerCase(),
      classes: e.className?.toString().split(' ').slice(0, 5).join(' '),
      text: onlyText ? e.textContent.trim().slice(0, 200) : null,
      styles: styles(e),
      img: e.tagName === 'IMG'
        ? { src: e.currentSrc || e.src, alt: e.alt, natural: [e.naturalWidth, e.naturalHeight] }
        : null,
      childCount: kids.length,
      children: kids.slice(0, 20).map(c => walk(c, d + 1)).filter(Boolean)
    };
  };
  return JSON.stringify(walk(el, 0), null, 2);
})('SELECTOR');
```

## 3. State diff

The diff between two captures is the behavior spec. Capture A, trigger the change through `computer` (scroll, click, hover), capture B, then diff.

Snapshot a flat set of properties for one element:

```javascript
(function (selector) {
  const el = document.querySelector(selector);
  if (!el) return JSON.stringify({ error: 'Not found: ' + selector });
  const cs = getComputedStyle(el);
  const out = {};
  for (const p of cs) out[p] = cs.getPropertyValue(p);
  return JSON.stringify({ scrollY: window.scrollY, styles: out });
})('SELECTOR');
```

Then diff the two snapshots in your own reasoning, or paste both back in and run:

```javascript
(function (a, b) {
  const changed = {};
  for (const k in b) if (a[k] !== b[k]) changed[k] = { from: a[k], to: b[k] };
  return JSON.stringify(changed, null, 2);
})(SNAPSHOT_A, SNAPSHOT_B);
```

Record the result as a sentence in the spec: *property X goes from A to B, triggered by T, transition `0.3s ease`.*

For hover specifically, `computer {action:"hover"}` then re-snapshot. For scroll-triggered, snapshot at `scrollY: 0`, scroll past the threshold, snapshot again, and binary-search the scroll position if you need the exact trigger point.

## 4. Tab and state content

For any tab group, click each control and pull its panel content:

```javascript
(function (tabSelector) {
  return JSON.stringify([...document.querySelectorAll(tabSelector)].map((t, i) => ({
    index: i,
    label: t.textContent.trim(),
    ariaSelected: t.getAttribute('aria-selected'),
    ariaControls: t.getAttribute('aria-controls'),
    classes: t.className?.toString()
  })));
})('TAB_SELECTOR');
```

Click each via `computer`, then run the per-component walk on the panel container. Record which content belongs to which state.

## 5. Text harvest

```javascript
(function (selector) {
  const root = document.querySelector(selector);
  if (!root) return JSON.stringify({ error: 'Not found: ' + selector });
  const out = [];
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let n; while ((n = w.nextNode())) {
    const t = n.textContent.trim();
    if (t) out.push({ text: t, parent: n.parentElement.tagName.toLowerCase() });
  }
  return JSON.stringify({
    text: out,
    alts: [...root.querySelectorAll('img[alt]')].map(i => i.alt),
    aria: [...root.querySelectorAll('[aria-label]')].map(e => e.getAttribute('aria-label')),
    placeholders: [...root.querySelectorAll('[placeholder]')].map(e => e.placeholder)
  }, null, 2);
})('SELECTOR');
```

## Notes

- `currentSrc` beats `src` on responsive images: it gives you the variant actually loaded at that viewport.
- Run the global audit again at 390px. `srcset` often swaps in different art entirely, not just a smaller file.
- If a selector returns nothing, use `read_page` to get the labeled tree and find the real one rather than guessing.
- Very large pages can exceed the response limit. Scope to a section container instead of `body`.

---

Scripts adapted from [ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) (MIT), extended here with stack fingerprinting, a runnable state diff, and text harvesting.
