"""calc_workbook.py
House style for calculation workbooks whose output is money. Requires openpyxl only.

Usage:
    cp <skill-dir>/references/calc-workbook.py ./calc_workbook.py
    from calc_workbook import Workbook, CUR, PCT, NUM, DATEF
Copy this file verbatim. Do not transcribe it by hand and do not carry a copy
forward between workbooks; overwrite it from the skill's references directory on
every run. It is imported as calc_workbook, so it must land under that filename.

You write formulas against reference names, not addresses:
    mi.field("D2.3", "Total claimed", "Calculated", "D2.1 plus D2.2",
             fmt=CUR, formula="={D2.1}+{D2.2}")
Addresses are resolved on save(). An unknown reference raises instead of shipping.
"""
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ARIAL = "Arial"

class T:
    ink = "000000"
    navy = "1F3864"        # document title band
    band = "2E5C9A"        # section band
    header = "8EA9DB"      # table header row
    total = "DDEBF7"       # totals row
    input_fill = "FFFF00"  # an input cell
    input_ink = "0000FF"   # blue text: hardcoded input
    calc_ink = "000000"    # black text: formula
    link_ink = "008000"    # green text: formula pulling from another tab
    flag_ink = "C00000"    # red bold: new or amended, pending agreement
    border = "BFBFBF"

CUR = '$#,##0;($#,##0);"-"'
CUR2 = '$#,##0.00;($#,##0.00);"-"'
PCT = '0.0%'
NUM = '#,##0'
DATEF = 'dd mmm yyyy'

_thin = Side(style="thin", color=T.border)
BOX = Border(left=_thin, right=_thin, top=_thin, bottom=_thin)

F_TITLE = Font(name=ARIAL, size=14, bold=True, color="FFFFFF")
F_SUB = Font(name=ARIAL, size=9, italic=True, color="444444")
F_BAND = Font(name=ARIAL, size=11, bold=True, color="FFFFFF")
F_HDR = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
F_REF = Font(name=ARIAL, size=10, bold=True)
F_FLAG = Font(name=ARIAL, size=10, bold=True, color=T.flag_ink)
F_BODY = Font(name=ARIAL, size=10)
F_NOTE = Font(name=ARIAL, size=9, italic=True, color="555555")
F_BOLD = Font(name=ARIAL, size=10, bold=True)
F_INPUT = Font(name=ARIAL, size=10, color=T.input_ink)
F_CALC = Font(name=ARIAL, size=10, color=T.calc_ink)
F_LINK = Font(name=ARIAL, size=10, color=T.link_ink)

_REF_TOKEN = re.compile(r"\{([^{}]+)\}")


class Sheet:
    """One worksheet. Rows are appended in order; the cursor is managed for you."""

    def __init__(self, wb, ws, entry_col=3, ncols=5):
        self.wb = wb
        self.ws = ws
        self.row = 1
        self.entry_col = entry_col
        self.ncols = ncols
        self.refs = {}
        self._pending = []

    def widths(self, mapping):
        for k, v in mapping.items():
            self.ws.column_dimensions[k].width = v
        return self

    def title(self, text, *subtitles):
        c = self.ws.cell(self.row, 1, text)
        c.font = F_TITLE
        for i in range(1, self.ncols + 1):
            self.ws.cell(self.row, i).fill = PatternFill("solid", fgColor=T.navy)
        self.ws.row_dimensions[self.row].height = 26
        self.row += 1
        for s in subtitles:
            self.ws.cell(self.row, 1, s).font = F_SUB
            self.row += 1
        self.row += 1
        return self

    def band(self, text):
        c = self.ws.cell(self.row, 1, text)
        c.font = F_BAND
        for i in range(1, self.ncols + 1):
            self.ws.cell(self.row, i).fill = PatternFill("solid", fgColor=T.band)
        self.ws.row_dimensions[self.row].height = 18
        self.row += 1
        return self

    def header(self, labels, wrap=False, height=None):
        for i, h in enumerate(labels, start=1):
            c = self.ws.cell(self.row, i, h)
            c.font = F_HDR
            c.fill = PatternFill("solid", fgColor=T.header)
            c.border = BOX
            c.alignment = Alignment(wrap_text=wrap, vertical="center",
                                    horizontal="center" if wrap else "left")
        if height:
            self.ws.row_dimensions[self.row].height = height
        self.row += 1
        return self

    def note(self, text):
        c = self.ws.cell(self.row, 1, text)
        c.font = F_NOTE
        c.alignment = Alignment(wrap_text=True, vertical="top")
        self.ws.merge_cells(start_row=self.row, start_column=1,
                            end_row=self.row, end_column=self.ncols)
        self.ws.row_dimensions[self.row].height = 26
        self.row += 1
        return self

    def para(self, text, bold=False):
        c = self.ws.cell(self.row, 1, text)
        c.font = F_BOLD if bold else F_BODY
        c.alignment = Alignment(wrap_text=True, vertical="top")
        self.ws.merge_cells(start_row=self.row, start_column=1,
                            end_row=self.row, end_column=self.ncols)
        self.row += 1
        return self

    def gap(self, n=1):
        self.row += n
        return self

    def field(self, ref, label, owner="", note="", fmt=None,
              formula=None, value=None, flag=False):
        """One labelled row. Give `formula` for a calculated cell (template may use
        {REF} tokens) or `value` for an input cell. Input cells are yellow with blue
        text; formula cells are left plain. `flag=True` marks the ref red bold."""
        r = self.row
        cref = self.ws.cell(r, 1, ref)
        cref.font = F_FLAG if flag else F_REF
        cref.border = BOX
        cref.alignment = Alignment(vertical="center")

        cl = self.ws.cell(r, 2, label)
        cl.font = F_BODY
        cl.border = BOX
        cl.alignment = Alignment(vertical="center", wrap_text=True)

        ce = self.ws.cell(r, self.entry_col)
        ce.border = BOX
        ce.alignment = Alignment(horizontal="right", vertical="center")
        if formula is not None:
            ce.font = F_LINK if "'" in formula else F_CALC
            self._pending.append((r, self.entry_col, formula))
        else:
            ce.value = value
            ce.font = F_INPUT
            ce.fill = PatternFill("solid", fgColor=T.input_fill)
        if fmt:
            ce.number_format = fmt

        if self.ncols >= self.entry_col + 1:
            co = self.ws.cell(r, self.entry_col + 1, owner)
            co.font = F_BODY
            co.border = BOX
            co.alignment = Alignment(horizontal="center", vertical="center")
        if self.ncols >= self.entry_col + 2:
            cn = self.ws.cell(r, self.entry_col + 2, note)
            cn.font = F_NOTE
            cn.border = BOX
            cn.alignment = Alignment(vertical="center", wrap_text=True)

        if ref:
            if ref in self.refs:
                raise ValueError("duplicate reference %r on %s" % (ref, self.ws.title))
            self.refs[ref] = r
        self.row += 1
        return r

    def input_block(self, items, label_w=1, value_w=2, note_w=3):
        """Named inputs for a schedule tab. `items` is a list of
        (anchor_name, label, value, number_format, note). Anchors resolve absolute."""
        for name, label, value, fmt, note in items:
            r = self.row
            self.ws.cell(r, label_w, label).font = F_BODY
            self.ws.cell(r, label_w).border = BOX
            ce = self.ws.cell(r, value_w, value)
            ce.font = F_INPUT
            ce.fill = PatternFill("solid", fgColor=T.input_fill)
            ce.border = BOX
            ce.alignment = Alignment(horizontal="right")
            if fmt:
                ce.number_format = fmt
            cn = self.ws.cell(r, note_w, note)
            cn.font = F_NOTE
            cn.alignment = Alignment(wrap_text=True, vertical="center")
            self.refs[name] = r
            self.wb.anchors[(self.ws.title, name)] = "$%s$%d" % (get_column_letter(value_w), r)
            self.row += 1
        return self

    def grid(self, columns, nrows, example=None, totals=None, header_height=46):
        """A repeating schedule. `columns` is a list of dicts:
            {header, width, kind: 'input'|'formula', fmt, formula, right}
        A formula template may use {row} for the current row and {ANCHOR} for a named
        input on this sheet. Returns (first_row, last_row, total_row)."""
        for i, spec in enumerate(columns, start=1):
            if spec.get("width"):
                self.ws.column_dimensions[get_column_letter(i)].width = spec["width"]
        self.header([c["header"] for c in columns], wrap=True, height=header_height)
        first = self.row
        last = first + nrows - 1
        for r in range(first, last + 1):
            for i, spec in enumerate(columns, start=1):
                c = self.ws.cell(r, i)
                c.border = BOX
                if spec.get("fmt"):
                    c.number_format = spec["fmt"]
                if spec.get("right"):
                    c.alignment = Alignment(horizontal="right")
                if spec["kind"] == "input":
                    c.font = F_INPUT
                    c.fill = PatternFill("solid", fgColor=T.input_fill)
                else:
                    c.font = F_CALC
                    self._pending.append((r, i, spec["formula"].replace("{row}", str(r))))
        self.row = last + 1
        total_row = None
        if totals:
            total_row = self.row
            self.ws.cell(total_row, 1, "Total").font = F_BOLD
            for i in range(1, len(columns) + 1):
                self.ws.cell(total_row, i).fill = PatternFill("solid", fgColor=T.total)
                self.ws.cell(total_row, i).border = BOX
            for i in totals:
                col = get_column_letter(i)
                c = self.ws.cell(total_row, i, "=SUM(%s%d:%s%d)" % (col, first, col, last))
                c.font = F_BOLD
                c.number_format = columns[i - 1].get("fmt") or CUR
            self.row = total_row + 1
        if example:
            for i, v in example.items():
                self.ws.cell(first, i, v)
            self.ws.cell(first, 1).font = Font(name=ARIAL, size=10, italic=True,
                                               color=T.flag_ink)
        self.gap()
        return first, last, total_row

    def legend(self, rows):
        """Colour key or assumptions block: list of (label, explanation)."""
        for label, text in rows:
            ca = self.ws.cell(self.row, 1, label)
            ca.font = F_BOLD
            ca.alignment = Alignment(vertical="top")
            cb = self.ws.cell(self.row, 2, text)
            cb.font = F_BODY
            cb.alignment = Alignment(vertical="top", wrap_text=True)
            self.row += 1
        return self

    def addr(self, ref, absolute=False):
        r = self.refs[ref]
        col = get_column_letter(self.entry_col)
        return ("$%s$%d" % (col, r)) if absolute else ("%s%d" % (col, r))


class Workbook:
    COLOUR_KEY = [
        ("Yellow fill, blue text", "An input. Type here."),
        ("Black text, no fill", "A formula. Do not overwrite."),
        ("Green text", "A formula pulling from another tab in this workbook."),
        ("Red bold reference", "A row that is new or amended relative to the governing "
                               "document. Do not rely on it until that amendment is agreed."),
    ]

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self._first = True
        self.sheets = {}
        self.anchors = {}

    def sheet(self, title, entry_col=3, ncols=5, gridlines=False):
        if self._first:
            ws = self.wb.active
            ws.title = title
            self._first = False
        else:
            ws = self.wb.create_sheet(title)
        ws.sheet_view.showGridLines = gridlines
        s = Sheet(self, ws, entry_col=entry_col, ncols=ncols)
        self.sheets[title] = s
        return s

    def _resolve(self, sheet, template):
        def sub(m):
            key = m.group(1)
            if (sheet.ws.title, key) in self.anchors:
                return self.anchors[(sheet.ws.title, key)]
            if key in sheet.refs:
                return sheet.addr(key)
            for other in self.sheets.values():
                # Anchors first, as on the same sheet: an input_block name is in both, and
                # refs would point at the entry column (the note) instead of the value.
                # A quote inside a sheet title is doubled inside the quoted name.
                title = other.ws.title.replace("'", "''")
                if (other.ws.title, key) in self.anchors:
                    return "'%s'!%s" % (title, self.anchors[(other.ws.title, key)])
                if key in other.refs:
                    return "'%s'!%s" % (title, other.addr(key))
            raise KeyError("unresolved reference %r in %r on %s"
                           % (key, template, sheet.ws.title))
        return _REF_TOKEN.sub(sub, template)

    def save(self, path):
        for s in self.sheets.values():
            for (r, c, template) in s._pending:
                cell = s.ws.cell(r, c)
                cell.value = self._resolve(s, template)
                # Link ink is decided by the resolved text: {REF} to another tab only
                # gains its quoted sheet name here, after the font was first chosen.
                if "'!" in cell.value and cell.font == F_CALC:
                    cell.font = F_LINK
        self.wb.save(path)
        return path

    def check_refs(self, sheet_title, expected):
        """Prove the governing document's reference scheme is intact."""
        s = self.sheets[sheet_title]
        pat = re.compile(r"^[A-Z]\d+\.\d+$")
        found = [s.ws.cell(r, 1).value for r in range(1, s.ws.max_row + 1)
                 if isinstance(s.ws.cell(r, 1).value, str)
                 and pat.match(s.ws.cell(r, 1).value)]
        return {
            "expected": len(expected), "found": len(found),
            "missing": [x for x in expected if x not in found],
            "unexpected": [x for x in found if x not in expected],
            "duplicated": sorted({x for x in found if found.count(x) > 1}),
            "in_order": found == list(expected),
        }
