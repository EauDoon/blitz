/* Blitz audit repair, 2026-10-11. Browser helper for an explicitly selected,
 * trusted static diagram. Does not write files or fetch resources. */
globalThis.blitzExportSvg = function (selector) {
  const matches = [...document.querySelectorAll(selector)];
  if (matches.length !== 1 || matches[0].tagName.toLowerCase() !== 'svg' || matches[0].parentElement?.closest('svg')) {
    throw new Error('Select exactly one outer SVG explicitly');
  }
  const source = matches[0];
  if (!source.hasAttribute('viewBox')) throw new Error('A declared viewBox is required');
  if (source.querySelector('script, foreignObject, animate, animateMotion, animateTransform, set')) {
    throw new Error('Active, animated or foreignObject content needs a separately verified route; use PNG for foreignObject');
  }
  const clone = source.cloneNode(true);
  const originals = [source, ...source.querySelectorAll('*')];
  const copies = [clone, ...clone.querySelectorAll('*')];
  const properties = ('color fill fill-opacity fill-rule stroke stroke-width stroke-opacity stroke-linecap stroke-linejoin ' +
    'stroke-miterlimit stroke-dasharray stroke-dashoffset opacity display visibility font-family font-size font-style ' +
    'font-weight font-stretch font-variant letter-spacing word-spacing text-anchor dominant-baseline alignment-baseline ' +
    'baseline-shift text-decoration white-space paint-order vector-effect stop-color stop-opacity flood-color flood-opacity ' +
    'lighting-color clip-path clip-rule mask filter marker-start marker-mid marker-end transform transform-origin transform-box').split(' ');
  const ids = new Set(originals.map(element => element.id).filter(Boolean));
  if (ids.size !== originals.filter(element => element.id).length) throw new Error('Duplicate SVG IDs');
  const reference = value => {
    const url = new URL(value, document.baseURI);
    const current = new URL(document.URL);
    if (!url.hash || url.href.split('#')[0] !== current.href.split('#')[0] || !ids.has(decodeURIComponent(url.hash.slice(1)))) {
      throw new Error('External or missing SVG dependency; embed authorized resources and verify again');
    }
    return url.hash;
  };
  originals.forEach((element, index) => {
    const copy = copies[index];
    for (const attr of [...element.attributes]) {
      if (/^on/i.test(attr.name)) throw new Error('Event handlers are outside static export');
      if (attr.localName === 'href') copy.setAttributeNS(attr.namespaceURI, attr.name, reference(attr.value));
    }
    copy.removeAttribute('class');
    copy.removeAttribute('style');
    const computed = getComputedStyle(element);
    for (const property of properties) {
      let value = computed.getPropertyValue(property);
      value = value.replace(/url\(\s*['"]?([^)'"\s]+)['"]?\s*\)/g, (_, url) => `url("${reference(url)}")`);
      if (value) copy.style.setProperty(property, value);
    }
  });
  // Page selectors/custom properties have now been resolved at the selected theme.
  clone.querySelectorAll('style').forEach(element => element.remove());
  clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  clone.setAttribute('width', source.viewBox.baseVal.width);
  clone.setAttribute('height', source.viewBox.baseVal.height);
  const xml = new XMLSerializer().serializeToString(clone);
  const parsed = new DOMParser().parseFromString(xml, 'image/svg+xml');
  if (parsed.querySelector('parsererror')) throw new Error('Exported XML did not parse');
  return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml + '\n';
};
