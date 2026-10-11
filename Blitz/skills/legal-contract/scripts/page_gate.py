import sys, re, subprocess
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = {a.split('=')[0]: a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--') and '=' in a}
START = re.compile(opt.get('--start') or r'^(IN WITNESS|SIGNED,? (SEALED|by|BY|for|FOR)|Signed,? (sealed|by|for)|EXECUTED (by|BY|as|AS)|Executed (by|as))')
STOP = re.compile(opt.get('--stop') or r'^(List of|LIST OF|Schedule|SCHEDULE|Annex|ANNEX|Appendix|APPENDIX|Inventory|INVENTORY)')
def pages(pdf):
    x = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    pg = [[l.strip() for l in p.split('\n') if l.strip()] for p in x.split('\f')]
    pg = [p for p in pg if p]
    norm = lambda l: re.sub(r'\d+', '#', l)
    edge = {}
    for p in pg:
        for l in set(p[:2] + p[-2:]):
            edge[norm(l)] = edge.get(norm(l), 0) + 1
    return [[l for l in p if edge.get(norm(l), 0) < 2 or START.match(l)] for p in pg]
def block(pdf):
    pg, on, where = pages(pdf), False, []
    for n, p in enumerate(pg, 1):
        for l in p:
            if START.match(l): on = True
            elif on and STOP.match(l): return len(pg), sorted(set(where))
            if on: where.append(n)
    return len(pg), sorted(set(where))
(na, a), (nb, b) = block(args[0]), block(args[1])
print(f'pages {na} -> {nb}; signature block on page {a} -> {b}')
if not a and not b:
    print(f'PAGE n/a: no signature line matched; pages {na} -> {nb}; check the last page by eye or pass --start=<regex>')
elif not b or len(b) > 1:
    print('PAGE FAIL: signature block split across pages' if b else 'PAGE FAIL: signature block not found in the amended file'); sys.exit(1)
elif nb != na:
    print(f'PAGES CHANGED: {na} -> {nb}; signature block whole on page {b[0]}; say so in the first line, then offer the two ways to win the page back')
else:
    print('PAGE PASS')
