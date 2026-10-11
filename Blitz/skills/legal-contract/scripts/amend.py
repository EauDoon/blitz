#!/usr/bin/env python3
"""amend.py: edit a contract .docx in place, word by word, without touching its format.

  scan    IN.docx                          fingerprint as JSON (fonts, layout, hidden text parts, protection, signatures)
  apply   IN.docx OUT.docx PLAN.json       clean copy: replacements, heading spacers, keep chain on the signature block
  track   IN.docx OUT.docx PLAN.json --author NAME [--layout]   redline copy: the same changes as tracked changes; --layout also applies spacers and the keep chain
  compare A.docx B.docx                    word level diff of body text, paragraph by paragraph

PLAN.json:
{
  "replacements": [{"id": 1, "old": "exact current text", "new": "exact new text"}],
  "paragraphs":   [{"insert_after": "<text of an existing paragraph>", "text": "<new sub-clause>"}, {"delete": "<text of an existing paragraph>"}],
  "spacers":      [{"after": "SUBLETTING", "add": 2}, {"after": "DIPLOMATIC CLAUSE", "remove": 6}],
  "keep":         {"start": "^(IN WITNESS|SIGNED|EXECUTED)", "stop": "^(List of|LIST OF|Schedule|SCHEDULE|Annex|ANNEX|Appendix|APPENDIX|Inventory|INVENTORY)"}
}
Every "old" must occur exactly once across all text parts, or nothing is written.
"""
import sys, re, json, copy, zipfile, difflib, datetime
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
def q(tag): return f'{{{W}}}{tag}'
TEXT_PARTS = re.compile(r'^word/(document|header\d*|footer\d*|footnotes|endnotes|comments)\.xml$')
STOP_DEFAULT = r'^(List of|LIST OF|Schedule|SCHEDULE|Annex|ANNEX|Appendix|APPENDIX|Inventory|INVENTORY)'
START_DEFAULT = r'^(IN WITNESS|SIGNED,? (SEALED|by|BY|for|FOR)|Signed,? (sealed|by|for)|EXECUTED (by|BY|as|AS)|Executed (by|as))'


class Docx:
    def __init__(self, path):
        self.path = path
        z = zipfile.ZipFile(path)
        self.names = z.namelist()
        self.raw = {n: z.read(n) for n in self.names}
        self.xml = {n: etree.fromstring(self.raw[n]) for n in self.names if TEXT_PARTS.match(n)}

    def save(self, out):
        zo = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
        order = ['[Content_Types].xml'] + [n for n in self.names if n != '[Content_Types].xml']
        for n in order:
            if n.endswith('/'):
                continue
            data = self.raw[n]
            if n in self.xml:
                data = etree.tostring(self.xml[n], xml_declaration=True, encoding='UTF-8', standalone=True)
            zo.writestr(n, data)
        zo.close()

    def max_id(self):
        m = 0
        for root in self.xml.values():
            for el in root.iter():
                v = el.get(q('id'))
                if v and v.lstrip('-').isdigit():
                    m = max(m, int(v))
        return m


# ---------- text model: a paragraph as characters mapped back to w:t nodes ----------

def ptext(p):
    return ''.join(t.text or '' for t in p.iter(q('t')) if t.getparent().getparent() is not None and not _in_del(t))

def _in_del(el):
    a = el.getparent()
    while a is not None:
        if a.tag == q('del'):
            return True
        a = a.getparent()
    return False

def para_chars(p):
    """List of (t_element, index_in_t, char) for the paragraph's live text; tabs count as one char."""
    chars = []
    for r in p.iter(q('r')):
        if _in_del(r):
            continue
        for child in r:
            if child.tag == q('t'):
                for i, ch in enumerate(child.text or ''):
                    chars.append((child, i, ch))
            elif child.tag == q('tab'):
                chars.append((child, 0, '\t'))
            elif child.tag in (q('br'), q('cr'), q('sym'), q('noBreakHyphen'), q('softHyphen'), q('fldChar'), q('instrText'), q('drawing'), q('pict')):
                chars.append((child, 0, '\n'))
    return chars

def find_matches(doc, old):
    hits = []
    for name, root in doc.xml.items():
        for p in root.iter(q('p')):
            chars = para_chars(p)
            s = ''.join(c for _, _, c in chars)
            start = 0
            while True:
                i = s.find(old, start)
                if i < 0:
                    break
                hits.append((name, p, chars, i))
                start = i + 1
    return hits

def set_t(t, text):
    t.text = text
    if text.startswith(' ') or text.endswith(' ') or '  ' in text:
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

def replace_span(chars, i, n, new):
    """Replace chars[i:i+n] with new, writing into the first w:t of the span and blanking the rest."""
    span = chars[i:i + n]
    first_t = span[0][0]
    if first_t.tag != q('t'):
        raise SystemExit('replacement span starts on a tab or break; widen the old text to start on a word')
    # group span positions by t element
    by_t = {}
    for t, k, _ in span:
        by_t.setdefault(t, []).append(k)
    for t, ks in by_t.items():
        if t.tag != q('t'):
            raise SystemExit('replacement span crosses a tab, break or field; split the change in two')
        txt = t.text or ''
        lo, hi = min(ks), max(ks) + 1
        if t is first_t:
            set_t(t, txt[:lo] + new + txt[hi:])
        else:
            set_t(t, txt[:lo] + txt[hi:])


# ---------- apply ----------

def blank(p):
    return not p.xpath('.//w:t[normalize-space(.)!=""] | .//w:tab | .//w:br | .//w:fldChar | .//w:fldSimple | .//w:bookmarkStart | .//w:drawing | .//w:pict', namespaces=NS)

def spacer_ops(doc, ops):
    body = doc.xml['word/document.xml']
    for op in ops:
        heads = [p for p in body.iter(q('p')) if ptext(p).strip() == op['after']]
        if len(heads) != 1:
            raise SystemExit(f"heading {op['after']!r} found {len(heads)} times, need exactly 1")
        h = heads[0]
        parent = h.getparent()
        sibs = [e for e in parent if e.tag == q('p')]
        idx = sibs.index(h)
        following = sibs[idx + 1:]
        if op.get('add'):
            template = next((s for s in following if blank(s)), None)
            if template is None:
                template = next((s for s in sibs if blank(s)), None)
            if template is None:
                raise SystemExit('no blank paragraph to clone in this cell')
            for _ in range(op['add']):
                h.addnext(copy.deepcopy(template))
        if op.get('remove'):
            removed = 0
            for s in following:
                if removed == op['remove']:
                    break
                if not blank(s):
                    break
                if s is sibs[-1]:
                    raise SystemExit('refusing to remove the last paragraph of a cell')
                parent.remove(s); removed += 1
            if removed != op['remove']:
                raise SystemExit(f"could remove only {removed} of {op['remove']} blanks after {op['after']!r}")

def _para_by_text(doc, text):
    body = doc.xml['word/document.xml']
    ps = [p for p in body.iter(q('p')) if ptext(p).strip() == text.strip()]
    if len(ps) != 1:
        raise SystemExit(f"paragraph {text[:50]!r} found {len(ps)} times, need exactly 1")
    return ps[0]

def _mark(tag, rev, author, date):
    el = etree.Element(q(tag)); el.set(q('id'), str(rev)); el.set(q('author'), author); el.set(q('date'), date)
    return el

def paragraph_ops(doc, ops, tracked):
    """ops: [{"insert_after": "<existing paragraph text>", "text": "<new>"}, {"delete": "<existing paragraph text>"}].
    tracked: None for the clean copy, else (next_id_list, author, date) to write revision marks."""
    for op in ops:
        if 'insert_after' in op:
            anchor = _para_by_text(doc, op['insert_after'])
            new = copy.deepcopy(anchor)
            runs = [r for r in new.iter(q('r'))]
            rpr = copy.deepcopy(runs[0].find(q('rPr'))) if runs and runs[0].find(q('rPr')) is not None else None
            for el in list(new):
                if el.tag != q('pPr'):
                    new.remove(el)
            r = etree.SubElement(new, q('r'))
            if rpr is not None:
                r.append(rpr)
            t = etree.SubElement(r, q('t')); set_t(t, op['text'])
            if tracked:
                ids, author, date = tracked
                ppr = new.find(q('pPr'))
                if ppr is None:
                    ppr = etree.Element(q('pPr')); new.insert(0, ppr)
                prpr = ppr.find(q('rPr'))
                if prpr is None:
                    prpr = etree.SubElement(ppr, q('rPr'))
                prpr.insert(0, _mark('ins', ids[0], author, date)); ids[0] += 1
                ins = _mark('ins', ids[0], author, date); ids[0] += 1
                new.remove(r); ins.append(r); new.append(ins)
            anchor.addnext(new)
        elif 'delete' in op:
            p = _para_by_text(doc, op['delete'])
            if not tracked:
                p.getparent().remove(p)
            else:
                ids, author, date = tracked
                ppr = p.find(q('pPr'))
                if ppr is None:
                    ppr = etree.Element(q('pPr')); p.insert(0, ppr)
                prpr = ppr.find(q('rPr'))
                if prpr is None:
                    prpr = etree.SubElement(ppr, q('rPr'))
                prpr.insert(0, _mark('del', ids[0], author, date)); ids[0] += 1
                for r in [r for r in p if r.tag == q('r')]:
                    d = _mark('del', ids[0], author, date); ids[0] += 1
                    p.replace(r, d); d.append(r)
                    for t in r.findall(q('t')):
                        t.tag = q('delText')
        else:
            raise SystemExit(f'unknown paragraph op {op}')

def keep_chain(doc, cfg):
    body = doc.xml['word/document.xml']
    start = re.compile(cfg.get('start') or START_DEFAULT)
    stop = re.compile(cfg.get('stop') or STOP_DEFAULT)
    paras = list(body.iter(q('p')))
    texts = [ptext(p).strip() for p in paras]
    starts = [k for k, t in enumerate(texts) if start.match(t)]
    if not starts:
        print('WARNING: no signature block found (no paragraph matches the start pattern); no keep chain set. Check the last page by eye.')
        return None
    i = starts[0]
    j = next((k for k in range(i + 1, len(paras)) if stop.match(texts[k])), len(paras))
    while j - 1 > i and not texts[j - 1]:
        j -= 1
    chain = paras[i:j]
    if len(chain) > 40 and not cfg.get('start'):
        raise SystemExit(f"keep chain would span {len(chain)} paragraphs from {texts[i][:30]!r}; that is not a signature block. Set keep.start to the exact first line of the block")
    rows = []
    for k, p in enumerate(chain):
        ppr = p.find(q('pPr'))
        if ppr is None:
            ppr = etree.Element(q('pPr')); p.insert(0, ppr)
        # schema order inside w:pPr: pStyle, keepNext, keepLines, then the rest
        for tag in (['keepNext', 'keepLines'] if k < len(chain) - 1 else ['keepLines']):
            if ppr.find(q(tag)) is None:
                pos = 0
                for el in ppr:
                    if el.tag in (q('pStyle'), q('keepNext')) and not (tag == 'keepNext' and el.tag == q('keepNext')):
                        pos = ppr.index(el) + 1
                ppr.insert(pos, etree.Element(q(tag)))
        tr = p.getparent()
        while tr is not None and tr.tag != q('tr'):
            tr = tr.getparent()
        if tr is not None and tr not in rows:
            rows.append(tr)
    for tr in rows:
        trpr = tr.find(q('trPr'))
        if trpr is None:
            trpr = etree.Element(q('trPr')); tr.insert(0, trpr)
        if trpr.find(q('cantSplit')) is None:
            trpr.append(etree.Element(q('cantSplit')))
    return len(chain), texts[i], texts[j - 1]

def do_apply(inp, out, plan):
    doc = Docx(inp)
    if any(n.startswith('_xmlsignatures/') for n in doc.names):
        raise SystemExit('this file carries a digital signature; editing invalidates it. Stop and ask.')
    found = []
    for rp in plan.get('replacements', []):
        hits = find_matches(doc, rp['old'])
        if len(hits) != 1:
            raise SystemExit(f"row {rp.get('id')}: old text found {len(hits)} times, need exactly 1: {rp['old'][:60]!r}")
        found.append((rp, hits[0]))
    # apply from the end of each paragraph backwards, on the character map captured before any edit
    found.sort(key=lambda x: (id(x[1][1]), -x[1][3]))
    last = {}
    for rp, (name, p, chars, i) in found:
        n = len(rp['old'])
        if id(p) in last and i + n > last[id(p)]:
            raise SystemExit(f"row {rp.get('id')} overlaps another row in the same paragraph; merge them into one row")
        last[id(p)] = i
        replace_span(chars, i, n, rp['new'])
    paragraph_ops(doc, plan.get('paragraphs', []), tracked=None)
    spacer_ops(doc, plan.get('spacers', []))
    info = None
    if plan.get('keep') is not None:
        info = keep_chain(doc, plan['keep'])
    doc.save(out)
    print(f"applied {len(found)} replacement(s), {len(plan.get('paragraphs', []))} paragraph op(s), {len(plan.get('spacers', []))} spacer op(s)" +
          (f", keep chain of {info[0]} paragraphs from {info[1][:30]!r} to {info[2][:30]!r}" if info else ', no keep chain'))


# ---------- track ----------

def split_run_at(t, k):
    """Split the run holding w:t `t` so that t's text[k:] moves to a new run after it. Returns the new w:t."""
    r = t.getparent()
    r2 = copy.deepcopy(r)
    for el in list(r2):
        if el.tag != q('rPr'):
            r2.remove(el)
    t2 = etree.SubElement(r2, q('t'))
    set_t(t2, (t.text or '')[k:])
    set_t(t, (t.text or '')[:k])
    r.addnext(r2)
    return t2

def do_track(inp, out, plan, author, layout=False):
    doc = Docx(inp)
    if any(n.startswith('_xmlsignatures/') for n in doc.names):
        raise SystemExit('this file carries a digital signature; editing invalidates it. Stop and ask.')
    next_id = doc.max_id() + 1
    date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    for rp in plan.get('replacements', []):
        hits = find_matches(doc, rp['old'])
        if len(hits) != 1:
            raise SystemExit(f"row {rp.get('id')}: old text found {len(hits)} times, need exactly 1")
        name, p, chars, i = hits[0]
        n = len(rp['old'])
        first_t, k0, _ = chars[i]
        last_t, k1, _ = chars[i + n - 1]
        if first_t.tag != q('t') or last_t.tag != q('t'):
            raise SystemExit('a tracked span must start and end on text, not a tab')
        # isolate the span into whole runs
        if k1 + 1 < len(last_t.text or ''):
            split_run_at(last_t, k1 + 1)
        if k0 > 0:
            first_t = split_run_at(first_t, k0)
        # collect runs from first_t's run to last_t's run (siblings under the same parent)
        runs = []
        r = first_t.getparent()
        end_r = last_t.getparent() if last_t is not first_t or k0 == 0 else first_t.getparent()
        # after splitting, last_t may have moved; recompute the run holding the span end
        span_text = rp['old']
        acc = ''
        while r is not None:
            runs.append(r)
            acc += ''.join((c.text or '') if c.tag == q('t') else '\t' for c in r if c.tag in (q('t'), q('tab')))
            if len(acc) >= len(span_text):
                break
            r = r.getnext()
            while r is not None and r.tag != q('r'):
                r = r.getnext()
        if acc != span_text:
            raise SystemExit(f"row {rp.get('id')}: run isolation failed ({acc[:40]!r} vs {span_text[:40]!r})")
        parent = runs[0].getparent()
        pos = parent.index(runs[0])
        d = etree.Element(q('del')); d.set(q('id'), str(next_id)); d.set(q('author'), author); d.set(q('date'), date); next_id += 1
        for r in runs:
            parent.remove(r)
            for t in r.findall(q('t')):
                t.tag = q('delText')
            d.append(r)
        ins = etree.Element(q('ins')); ins.set(q('id'), str(next_id)); ins.set(q('author'), author); ins.set(q('date'), date); next_id += 1
        nr = etree.SubElement(ins, q('r'))
        rpr = runs[0].find(q('rPr'))
        if rpr is not None:
            nr.append(copy.deepcopy(rpr))
        nt = etree.SubElement(nr, q('t')); set_t(nt, rp['new'])
        parent.insert(pos, d); parent.insert(pos + 1, ins)
    ids = [next_id]
    paragraph_ops(doc, plan.get('paragraphs', []), tracked=(ids, author, date))
    next_id = ids[0]
    if layout:
        spacer_ops(doc, plan.get('spacers', []))
        if plan.get('keep') is not None:
            keep_chain(doc, plan['keep'])
    doc.save(out)
    print(f"tracked {len(plan.get('replacements', []))} replacement(s) and {len(plan.get('paragraphs', []))} paragraph op(s) under {author!r}, revision ids up to {next_id - 1}" + (', layout applied' if layout else ''))


# ---------- compare ----------

def body_paras(path):
    doc = Docx(path)
    out = []
    for name in ['word/document.xml'] + sorted(n for n in doc.xml if n != 'word/document.xml'):
        for p in doc.xml[name].iter(q('p')):
            t = ptext(p)
            if t.strip():
                out.append(t if name == 'word/document.xml' else f'[{name.split("/")[-1]}] {t}')
    tracked = sum(len(r.findall(f'.//{q(tag)}')) for r in doc.xml.values() for tag in ('ins', 'del'))
    return out, tracked

def do_compare(a, b):
    pa, ta = body_paras(a)
    pb, tb = body_paras(b)
    sm = difflib.SequenceMatcher(None, pa, pb, autojunk=False)
    changes = 0
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == 'equal':
            continue
        changes += 1
        print(f'--- paragraph {a1 + 1} ({op})')
        for x in pa[a1:a2]:
            print('  OLD: ' + x)
        for y in pb[b1:b2]:
            print('  NEW: ' + y)
        if op == 'replace' and a2 - a1 == 1 and b2 - b1 == 1:
            wa, wb = pa[a1].split(), pb[b1].split()
            wm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
            for wop, i1, i2, j1, j2 in wm.get_opcodes():
                if wop != 'equal':
                    print(f'      {wop}: {" ".join(wa[i1:i2])!r} -> {" ".join(wb[j1:j2])!r}')
    print(f'COMPARE: {changes} changed paragraph block(s); tracked-change marks in B: {tb}')


# ---------- scan ----------

def do_scan(inp):
    doc = Docx(inp)
    body = doc.xml['word/document.xml']
    d = doc.raw['word/document.xml'].decode('utf8', 'replace')
    settings = doc.raw.get('word/settings.xml', b'').decode('utf8', 'replace')
    paras = list(body.iter(q('p')))
    texts = [ptext(p).strip() for p in paras]
    typed = sum(1 for t in texts if re.match(r'^(\(?[0-9]+[\.\)]|\([a-z]\)|[a-z]\)|[ivx]+\))\s', t))
    auto = sum(1 for p in paras if p.find(f'{q("pPr")}/{q("numPr")}') is not None)
    tbls = body.findall(f'.//{q("tbl")}')
    heading_col = None
    for ti, t in enumerate(tbls):
        for row in t.findall(q('tr')):
            cells = row.findall(q('tc'))
            for ci, c in enumerate(cells):
                ps = [ptext(p).strip() for p in c.iter(q('p'))]
                nonblank = [x for x in ps if x]
                if len(ps) >= 6 and nonblank and sum(1 for x in nonblank if x.isupper() and len(x) < 50) >= 0.6 * len(nonblank):
                    heading_col = {'table_index': ti, 'cell_index': ci, 'headings': len(nonblank), 'blank_spacers': len(ps) - len(nonblank)}
    split_hint = None
    if heading_col is not None:
        t = tbls[heading_col['table_index']]
        cols = [int(g.get(q('w'))) for g in t.findall(f'{q("tblGrid")}/{q("gridCol")}')]
        sect0 = body.find(f'.//{q("sectPr")}')
        pgw = int(sect0.find(q('pgSz')).get(q('w'))) if sect0 is not None and sect0.find(q('pgSz')) is not None else None
        left = int(sect0.find(q('pgMar')).get(q('left'))) if sect0 is not None and sect0.find(q('pgMar')) is not None else 0
        ind = t.find(f'{q("tblPr")}/{q("tblInd")}')
        left += int(ind.get(q('w'))) if ind is not None and ind.get(q('w')) else 0
        if cols and pgw:
            split_hint = round((left + sum(cols[:heading_col['cell_index']])) / pgw - 0.02, 2)
        heading_col['split_hint'] = split_hint
    sect = body.find(f'.//{q("sectPr")}')
    pg = sect.find(q('pgSz')) if sect is not None else None
    mar = sect.find(q('pgMar')) if sect is not None else None
    info = {
        'file': inp,
        'signed': any(n.startswith('_xmlsignatures/') for n in doc.names),
        'protection': re.findall(r'<w:documentProtection[^>]*w:edit="([^"]+)"', settings),
        'embedded_fonts': 'embedTrueTypeFonts' in settings or any(n.startswith('word/fonts/') for n in doc.names),
        'fonts': sorted(set(re.findall(r'(?:w:ascii|w:hAnsi)="([^"]+)"', d + doc.raw.get('word/styles.xml', b'').decode('utf8', 'replace'))
                            + re.findall(r'<a:latin typeface="([^"]+)"', doc.raw.get('word/theme/theme1.xml', b'').decode('utf8', 'replace'))) - {''}),
        'sizes_half_points': sorted(set(re.findall(r'<w:sz w:val="(\d+)"', d)), key=int),
        'page': {'w': pg.get(q('w')) if pg is not None else None, 'h': pg.get(q('h')) if pg is not None else None,
                 'margins': {k: mar.get(q(k)) for k in ('top', 'bottom', 'left', 'right')} if mar is not None else None},
        'paragraphs': len(paras), 'tables': len(tbls), 'sections': d.count('<w:sectPr'),
        'numbering': {'auto': auto, 'typed': typed},
        'heading_column': heading_col,
        'text_parts': [n for n in doc.xml if any(t.text for t in doc.xml[n].iter(q('t')))],
        'hidden_text': {'content_controls': d.count('<w:sdt>') + d.count('<w:sdt '), 'text_boxes': d.count('<w:txbxContent'),
                        'fields': d.count('<w:fldChar') + d.count('<w:fldSimple'), 'bookmarks': d.count('<w:bookmarkStart'),
                        'comments': 'word/comments.xml' in doc.names, 'tracked_changes': d.count('<w:ins ') + d.count('<w:del ')},
        'signature_block_starts': [t[:40] for t in texts if re.match(START_DEFAULT, t)],
    }
    print(json.dumps(info, indent=2))


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    cmd = argv[1]
    if cmd == 'scan':
        do_scan(argv[2])
    elif cmd == 'apply':
        do_apply(argv[2], argv[3], json.load(open(argv[4])))
    elif cmd == 'track':
        author = argv[argv.index('--author') + 1] if '--author' in argv else None
        if not author:
            raise SystemExit('track needs --author "Name as he signs"')
        do_track(argv[2], argv[3], json.load(open(argv[4])), author, layout='--layout' in argv)
    elif cmd == 'compare':
        do_compare(argv[2], argv[3])
    else:
        print(__doc__); return 2
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
