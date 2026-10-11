import sys, zipfile, re, hashlib
KEEP = r'word/(styles|numbering|settings|fontTable|theme/theme\d*|header\d*|footer\d*)\.xml$'
def facts(p):
    z = zipfile.ZipFile(p); d = z.read('word/document.xml').decode('utf8')
    return {'parts': sorted(n for n in z.namelist() if not n.endswith('/')),
            'fixed parts': {k: hashlib.sha1(re.sub(rb'<w:t(?: [^>]*)?>[^<]*</w:t>', b'<w:t/>', z.read(k))).hexdigest() for k in z.namelist() if re.match(KEEP, k)},
            'tables': d.count('<w:tbl>'), 'rows': len(re.findall(r'<w:tr[ >]', d)),
            'cells': len(re.findall(r'<w:tc[ >]', d)), 'sections': d.count('<w:sectPr'),
            'fonts': sorted(set(re.findall(r'w:ascii="([^"]+)"', d))),
            'sizes': sorted(set(re.findall(r'<w:sz w:val="(\d+)"', d))),
            'body blank lines': sum(1 for q in re.findall(r'<w:p[ >].*?</w:p>|<w:p/>', re.sub(r'<w:tbl>.*?</w:tbl>', '', d, flags=re.S), re.S)
                                    if not re.search(r'<w:t[^>]*>[^<]', q)),
            'paragraphs': len(re.findall(r'<w:p[ >/]', d))}
a, b = facts(sys.argv[1]), facts(sys.argv[2])
bad = [k for k in a if k != 'paragraphs' and a[k] != b[k]]
print('paragraphs', a['paragraphs'], '->', b['paragraphs'])
print('STRUCTURE FAIL: ' + ', '.join(bad) if bad else 'STRUCTURE PASS')
