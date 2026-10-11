import sys, json
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

CL = [('TERM AND FEE', '1. Example Workshop hires one sample label printer know as Unit SAMPLE-07 from Example Tools for nine months, starting 1 April 2030. The monthly fee is 120 test credits, due on the fifth day of each month.'), ('SECURITY DEPOSIT', '2. The hirer pays a refundable deposit of 240 test credits before collection. The deposit does not replace the final monthly fee.'), ('TRANSFER', "(j) The hirer may not transfer the sample unit to another workshop without the supplier's written consent. Consent will not be unreasonably withheld."), ('MINOR REPAIRS', "(k) The hirer pays for accidental minor repairs up to 30 test credits per incident. Normal wear is the supplier's responsibility."), ('EARLY RETURN', "(d) After six completed months, the hirer may end the hire on 30 days' written notice if its sample workshop closes. The hirer must supply evidence of closure and pay any outstanding monthly fees."), ('EXTENSION', '(g) The parties may agree in writing to extend the hire for three additional months at a newly agreed fee.'), ('CLEANING', '(h) Before return, the hirer will clean the label tray and the external case of the sample printer and provide a dated maintenance note.'), ('HANDLING FEE', '(l) A one-time handling fee of 12 test credits is earned when the sample unit is collected.'), ('DISPUTES', '(m) The parties first refer a dispute to their named project owners for written review. This synthetic text is a software fixture, not a usable legal agreement.')]

def fmt(p, size, bold=False):
    pf = p.paragraph_format
    pf.space_before = Pt(0); pf.space_after = Pt(0)
    pf.line_spacing = Pt(12)
    from docx.enum.text import WD_LINE_SPACING
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    for r in p.runs:
        r.font.name = 'Liberation Sans'; r.font.size = Pt(size); r.font.bold = bold
        r._element.rPr.rFonts.set(qn('w:hAnsi'), 'Liberation Sans')

def build(pads, out):
    d = Document()
    s = d.sections[0]; s.page_width = Inches(8.27); s.page_height = Inches(11.69)
    s.left_margin = s.right_margin = Inches(0.8); s.top_margin = s.bottom_margin = Inches(0.8)
    t = d.add_paragraph(); t.add_run('SYNTHETIC EQUIPMENT HIRE - TEST DATA ONLY'); fmt(t, 12, True)
    d.add_paragraph()
    tbl = d.add_table(rows=1, cols=2); tbl.autofit = False
    L, R = tbl.rows[0].cells
    L.width = Inches(5.2); R.width = Inches(1.47)
    L.paragraphs[0]._element.getparent().remove(L.paragraphs[0]._element)
    R.paragraphs[0]._element.getparent().remove(R.paragraphs[0]._element)
    for i, (h, c) in enumerate(CL):
        p = L.add_paragraph(); p.add_run(c); fmt(p, 10)
        p = L.add_paragraph(); p.add_run(''); fmt(p, 10)
        p = R.add_paragraph(); p.add_run(h); fmt(p, 8, True)
        for _ in range(pads[i]):
            p = R.add_paragraph(); p.add_run(''); fmt(p, 8)
    d.save(out)

if __name__ == '__main__':
    build(json.loads(sys.argv[1]), sys.argv[2])
