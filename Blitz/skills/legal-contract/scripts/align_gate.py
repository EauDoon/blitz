import sys, re, subprocess, html
HEAD = re.compile(r"^(?=(?:.*[A-Z]){2})[A-Z0-9 /&,\.\-\(\)'’]+$")  # short bold caps headings, not the ) of a signature block
def pairs(pdf, split):
    x = subprocess.run(['pdftotext', '-bbox-layout', pdf, '-'], capture_output=True, text=True).stdout
    out = []
    for pn, (w, body) in enumerate(re.findall(r'<page width="([\d.]+)" height="[\d.]+">(.*?)</page>', x, re.S), 1):
        cut = float(w) * split
        lines = []
        for ln in re.findall(r'<line xMin="([\d.]+)" yMin="([\d.]+)"[^>]*>(.*?)</line>', body, re.S):
            words = [html.unescape(t) for t in re.findall(r'>([^<]+)</word>', ln[2])]
            lines.append((float(ln[0]), float(ln[1]), ' '.join(words)))
        left = [l for l in lines if l[0] < cut]
        heads = [l for l in lines if l[0] >= cut and HEAD.match(l[2].strip())]
        for hx, hy, ht in heads:
            near = min(left, key=lambda l: abs(l[1] - hy), default=None)
            if near:
                out.append((ht, pn, round(hy - near[1], 1), ' '.join(near[2].split()[:4])))
    return out
split = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7
a, b = pairs(sys.argv[1], split), pairs(sys.argv[2], split)
if [p[0] for p in a] != [p[0] for p in b]:
    print('ALIGN FAIL: heading list changed', len(a), '->', len(b))
if not a:
    print(f'ALIGN FAIL: no heading lines found right of split {split}; take the split from amend.py scan (heading_column.split_hint)')
    sys.exit(1)
bad = 0
for (ht, pa, da, ta), (_, pb, db, tb) in zip(a, b):
    if ta != tb or abs(da - db) > 2:
        bad += 1
        print(f'MOVED  {ht!r}  was p{pa} beside {ta!r} ({da}pt)  now p{pb} beside {tb!r} ({db}pt)')
print(f'ALIGN {"PASS" if not bad and len(a) == len(b) else "FAIL"}: {len(a) - bad} of {len(a)} heading lines beside the same clause text')
sys.exit(1 if bad or len(a) != len(b) else 0)
