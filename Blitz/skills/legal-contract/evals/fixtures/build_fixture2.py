import sys, json
from docx.shared import Pt
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_fixture.py')).read().split("if __name__")[0])
from docx import Document
def sigblock(d, filler):
    for _ in range(filler):
        p = d.add_paragraph(); p.add_run(''); fmt(p, 10)
    rows = ['SYNTHETIC SIGNATURE BLOCK - NO REAL IDENTITIES', '', 'SIGNED by the Supplier', 'Name: SAMPLE SUPPLIER', 'Test ID: EXAMPLE-SUPPLIER', 'Witness: SAMPLE WITNESS A', '', 'SIGNED by the Hirer', 'Name: SAMPLE HIRER', 'Test ID: EXAMPLE-HIRER', 'Witness: SAMPLE WITNESS B', '', 'List of equipment:']
    for r in rows:
        p = d.add_paragraph(); p.add_run(r); fmt(p, 10, bold=r.startswith(('SIGNED', 'List')))
def build2(pads, filler, out):
    build(pads, out)
    d = Document(out); sigblock(d, filler); d.save(out)
if __name__ == '__main__':
    build2(json.loads(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
