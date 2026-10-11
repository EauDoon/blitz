---
name: calc-workbook
description: 'Money spreadsheets, .xlsx or Google Sheet: invoices, ledgers, fee and revenue share models, IRR. Use on "build me a spreadsheet", "check the maths in this sheet", "turn this clause into a calculation". Non-money: xlsx.'
---

# Calculation Workbook

House style for spreadsheets whose output is money. The build is an `.xlsx` with live formulas (a Google Sheet copy when he asks for one), a Read Me tab that names every assumption, and a verification pass that proves the arithmetic before anyone sees it. Pair with the built-in `xlsx` skill, which governs file mechanics; this skill governs structure, theme, and the two failure modes that actually cost money here.

## The two failure modes this exists to prevent

**1. Off-by-one cell references.** A formula that points at the row above its intended target recalculates cleanly, reports zero errors, and produces a wrong invoice. So you never write `=C29/C27`. You write `=IFERROR({D3.2}/{D3.1},"")` and the module resolves the addresses on save. If a reference name does not exist, the build fails loudly instead of shipping a plausible number.

**2. Renumbering a governing document's reference scheme.** If the contract says D3.7 is the fee cap, the workbook's D3.7 is the fee cap. Useful extra rows are real, but they take non-colliding labels (`Control`, `CalcD`), never a spare D-number. `check_refs()` proves every expected reference appears exactly once and in order.

Both of these have already happened on a live agreement. Treat them as the point of the skill, not as pedantry.

## When to use

An `.xlsx` or Google Sheet with formulas whose output is money: monthly invoice and reconciliation forms, revenue share and NIM calculations, recoupment ledgers, fee schedules, sensitivity tables, or a rebuild of an existing workbook that has drifted from the clause it implements. For a contract as a `.docx` use `deal-desk`. For a memo use `doc-style`. A spreadsheet that does not compute money goes to the built-in `xlsx` skill. Whether a program is worth paying for is `program-econ`; this skill builds the sheet that computes it.

## Order of operations

1. **Read the governing document first.** If the workbook implements a contract, appendix, or regulatory requirement, read that text and extract the exact reference numbers, defined terms, formulas, thresholds and day count conventions. Do not infer a formula from a worked example.
2. **List the assumptions you are about to hardcode**, with a source for each. Anything with no source is an input cell and an open item, not a constant.
3. **Read the built-in `xlsx` skill** for openpyxl gotchas and the recalc script.
4. **Copy the module.** `cp <skill-dir>/references/calc-workbook.py ./calc_workbook.py`. Copy it verbatim; never transcribe it by hand.
5. **Build** with the recipe below.
6. **Verify.** Mandatory, three passes. See below. A green recalc alone is not verification.
7. **Run `cold-read`** when the workbook is paid against or leaves his hands. Do not ask permission first. Paid-against arithmetic is a cold-read auto-fire class. The three passes below are self-checks by the agent that built the workbook; cold-read adds evaluators that never saw the build. See "Handoff to cold-read" at the end of this skill.
8. **Deliver the `.xlsx` as a file first.** It is the canonical build. When the owner asks for a Google Sheet, follow `doc-style`'s Drive rule: never push the Office file through the Google Drive connector as base64 (it has corrupted in transit, and `doc-style` and `google-slides` forbid it). Upload a text rendering instead: one CSV per tab, passed as `textContent` with `contentMimeType: text/csv` and the target folder's `parentId`, into the folder he names in the authorized destination Drive (if unclear, ask once). Drive converts each upload into a native Sheet. Write formula cells as their formula text; the read-back total confirms Sheets evaluated them. CSV carries no formatting, no colour key and no references across tabs, so a model with cross-tab formulas keeps the `.xlsx` as the working copy. Read each Sheet back through the connector and confirm the tab contents and one checked total before saying it is there, and state what the Sheet copy lacks. If the read-back fails, keep the `.xlsx` delivery and say the Google Sheet was not produced. Say who holds edit rights when a counterparty will see it.

## Structure

Tabs in this order. Omit what does not apply; do not reorder.

| Tab | Contents |
|---|---|
| **Read Me** | Purpose. Which document governs when the two disagree. Who completes what. One line per tab. Colour key. Every assumption and hardcoded figure with its source. Open items that affect the form. |
| **The form or model** | The main tab. Five columns: Ref, Field, Entry, Completed by, Clause / note. Banded sections matching the governing document's Parts. |
| **Schedule tabs** | Per-item computation that feeds the main tab, for example one row per item or per counterparty. Named inputs at the top, a repeating grid below, a totals row. |
| **Ledger** | Period-to-date figures where the main tab asks for a year-to-date number no single monthly form can produce. |
| **Reconciliation log** | Only when rebuilding an existing workbook: every discrepancy against the governing document, with severity and how it was resolved. This is what lets counsel and the counterparty see what moved. |

## The house look

- **Arial throughout.** Gridlines off on every tab.
- **Bands.** Document title white bold on navy `1F3864`. Section band white bold on `2E5C9A`. Table header row white bold on `8EA9DB`. Totals row filled `DDEBF7`. Thin `BFBFBF` borders on every data cell.
- **Colour carries meaning, and the Read Me states it:** yellow fill `FFFF00` with blue text `0000FF` is an input; black is a formula; green `008000` is a formula pulling from another tab; red bold `C00000` marks a row that is new or amended relative to the governing document and not to be relied on until that amendment is agreed.
- **Formats.** Currency `$#,##0;($#,##0);"-"`, percentages `0.0%` stored as fractions, counts `#,##0`, dates `dd mmm yyyy`. Name the unit in the header, never only in a note.
- **Formulas, never computed constants.** `=SUM(...)`, not the Python total. The sheet must recalculate when inputs change.
- **Every assumption in its own labelled cell**, referenced by the formulas that use it. `={D3.3}*{Rate}*{D3.1}/{Days}`, never `*0.037*31/365`.
- **Guard every denominator** with `IFERROR`, and return `""` rather than `0` so an empty form does not read as a zero claim.
- **Rate and day count are inputs, not constants.** A benchmark rate has a date and a source and will move. State the day count basis explicitly; the house position is that the daily rate is the annual rate divided by 365.
- **One example row on a schedule tab**, flagged in red and labelled "EXAMPLE, delete before use". Never add one to a file you were asked to edit.
- **No em dashes anywhere**, including in notes and Read Me text.
- **No Notion-internal references** in any cell or note (a register row number, a page id); name the position in plain words.
- **Prefer Excel-2007-era functions.** `SUMIFS`, `INDEX`, `MATCH`, `IFERROR`, `SUMPRODUCT`, `EXACT`. Never `XLOOKUP`, `FILTER`, `UNIQUE`, `SORT`, `SEQUENCE`: the verification runtime cannot evaluate them and reports zero errors on the truncated result.

## Build step: copy the module, never transcribe it

Every workbook is built from `calc-workbook.py`, which ships with this skill. Copy it into your working directory verbatim, under the name the recipe imports:

```bash
cp <skill-dir>/references/calc-workbook.py ./calc_workbook.py
```

Copy it, never retype it and never reconstruct it from the summary below. It requires `openpyxl` only. Overwrite it from the skill on every run rather than carrying a copy forward: a stale module is how a house-style change silently fails to reach a workbook.

### What the module provides

- `Workbook()`: the container. `sheet(title, entry_col, ncols, gridlines)` makes a tab, `save(path)` resolves every `{REF}` token to a real address and writes the file, `check_refs(sheet_title, expected)` proves the governing document's reference scheme is intact (`missing`, `unexpected`, `duplicated`, `in_order`). `W.anchors[(sheet_title, name)] = "$I$12"` registers a cross-tab target. `Workbook.COLOUR_KEY` is the standard colour legend for the Read Me tab.
- `Sheet`: one tab, with a managed row cursor. `widths(mapping)`, `title(text, *subtitles)`, `band(text)`, `header(labels)`, `note(text)`, `para(text, bold)`, `gap(n)`, `legend(rows)`, `addr(ref, absolute)`.
- `Sheet.field(ref, label, owner, note, fmt, formula, value, flag)`: one labelled row of the main form. Pass `formula` for a calculated cell (the template may carry `{REF}` tokens) or `value` for an input cell. Input cells come out yellow with blue text, cross-tab formulas green, flagged refs red bold. A duplicate reference raises.
- `Sheet.input_block(items)`: named inputs at the top of a schedule tab, resolving as absolute anchors.
- `Sheet.grid(columns, nrows, example, totals, header_height)`: a repeating schedule with a header, per-row `{row}` formulas, an optional totals row and an optional example row. Returns `(first_row, last_row, total_row)`.
- Theme and formats: `T` (the colour constants), `ARIAL`, `BOX`, the `F_*` fonts, and the number formats `CUR`, `CUR2`, `PCT`, `NUM`, `DATEF`.

Reference resolution is the point of the module. You write `formula="={D2.1}+{D2.2}"`, not `=C29+C30`, and an unknown reference raises on `save()` instead of shipping a plausible wrong number.

## Build recipe

```python
from calc_workbook import Workbook, CUR, PCT, NUM, DATEF

W = Workbook()

# 1. Read Me
rm = W.sheet("Read Me", ncols=2)
rm.widths({"A": 34, "B": 108})
rm.title("Monthly Invoice and Reconciliation Statement",
         "Form of Appendix D to the [Agreement].")
rm.band("What this workbook is")
rm.legend([
    ("Purpose", "..."),
    ("Authority", "Appendix D governs. Where this workbook and Appendix D differ, Appendix D governs."),
])
rm.gap().band("Colour key")
rm.legend(W.COLOUR_KEY)
rm.gap().band("Assumptions and hardcoded figures")
rm.legend([
    ("NIM Rate 3.7% placeholder", "FRED DGS3MO 3.72% and NY Fed SOFR 3.63% as at 8 June 2026. Refresh at execution."),
    ("Day count 365", "Daily rate is the annual rate divided by 365. Not stated in the Agreement. Confirm with the counterparty."),
])

# 2. The form
HDR = ["Ref", "Field", "Entry", "Completed by", "Clause / note"]
mi = W.sheet("Monthly Invoice")
mi.widths({"A": 9, "B": 74, "C": 20, "D": 15, "E": 34})
mi.title("...", "...")
mi.band("PART 1: INPUTS (USD)").header(HDR)
mi.field("D1.8", "Monthly Retainer, per clause 5.1", "Party A", "Input. Confirm against the executed agreement.",
         fmt=CUR, value=0)
mi.field("D1.9", "Period type (Term or Tail Period)", "Party A", "Clause 7.4.",
         value="Term")
mi.band("PART 2: AMOUNT CLAIMED THIS MONTH (USD)").header(HDR)
mi.field("D2.1", "Monthly Retainer payable", "Calculated", "Clause 5.1. Nil in a Tail Period.",
         fmt=CUR, formula='=IF({D1.9}="Tail Period",0,{D1.8})', flag=True)
mi.field("D2.2", "Third-party costs approved in advance", "Party B", "Appendix A",
         fmt=CUR, value=0)
mi.field("D2.3", "Total claimed this month", "Calculated", "D2.1 plus D2.2",
         fmt=CUR, formula="={D2.1}+{D2.2}")
mi.note("Only the Retainer and approved costs are payable monthly.")

# 3. Schedule tab: named inputs, then a repeating grid
lv = W.sheet("Per Item Schedule", ncols=11)
lv.title("...").band("Termination inputs")
lv.input_block([
    ("EFF",   "Effective date of termination", None, DATEF, "Caps the balance."),
    ("MEND",  "Statement month end date",      None, DATEF, "Last day of the month."),
    ("LRATE", "NIM Rate, annualised",         0.037, "0.0%", "Must equal the rate input on the form tab."),
])
cols = [
    {"header": "D8.1 Name", "width": 26, "kind": "input"},
    {"header": "D8.2 Balance (USD)", "width": 18, "kind": "input", "fmt": CUR, "right": True},
    {"header": "D8.3 Cap (USD)", "width": 18, "kind": "input", "fmt": CUR, "right": True},
    {"header": "D8.4 Attributable Balance (USD)", "width": 18, "kind": "formula",
     "fmt": CUR, "right": True, "formula": "=MIN(B{row},C{row})"},
]
first, last, total = lv.grid(cols, 15, totals=[4], example={1: "EXAMPLE, delete before use"})
W.anchors[("Per Item Schedule", "LV_ATTR_TOTAL")] = "$D$%d" % total
# the form tab can now use formula="={LV_ATTR_TOTAL}" and it renders green

W.save("out.xlsx")
print(W.check_refs("Monthly Invoice", ["D1.8", "D1.9", "D2.1", "D2.2", "D2.3"]))
```

Cross-tab totals are wired by registering an anchor after `grid()` returns its total row, then referring to that anchor name from the other tab. Formulas containing a quoted sheet name render green automatically.

## Verification, all three passes, every time

**Pass 1: recalculate** with the `recalc.py` script in the built-in `xlsx` skill's scripts folder: `python <path-to>/recalc.py out.xlsx 39`. Must report `total_errors: 0`. Note two operational traps: LibreOffice leaves a `.~lock.<name>#` file behind if a run is killed, and a stale lock makes every later run on that filename time out. Recalculate a freshly named copy rather than fighting it. And `pkill -f soffice` can match the shell wrapper and kill your own session; kill by PID from `ps -eo pid,comm` instead.

**Pass 2: structural reference audit.** Print every formula with each cell reference replaced by the label of the row it points at, and read it. This is what catches the reference that evaluates cleanly and means the wrong thing.

```python
import re, openpyxl
from openpyxl.utils import column_index_from_string
wb = openpyxl.load_workbook("out.xlsx")
ws = wb["Monthly Invoice"]
lab = {r: "%s %s" % (ws.cell(r, 1).value or "", ws.cell(r, 2).value or "")
       for r in range(1, ws.max_row + 1) if ws.cell(r, 2).value}
CELL = re.compile(r"(?<![A-Z0-9_!$'])(\$?)([A-Z]{1,2})(\$?)(\d{1,4})\b")
for r in range(1, ws.max_row + 1):
    v = ws.cell(r, 3).value
    if isinstance(v, str) and v.startswith("="):
        print(ws.cell(r, 1).value, "|",
              CELL.sub(lambda m: "[%s]" % lab.get(int(m.group(4)), m.group(0))[:60], v))
```

Also run `W.check_refs(...)` and confirm `missing`, `unexpected` and `duplicated` are all empty and `in_order` is true.

**Pass 3: numeric harness.** Copy the workbook, populate a realistic scenario, recalculate, and assert every computed cell against a value you calculated independently in Python. Cover the boundaries, not just the happy path: a month where the adjustment clause triggers and a month where it does not, a capped figure where the cap actually bites, a period that has already expired and must return nil, and the final reconciliation flag both ways. Print `got` and `exp` side by side and a failure count.

Run each pass in its own shell call. A recalculation can take most of a minute, and populate-then-assert in one call risks the assertions running against uncalculated cells, which read back as `None`.

## Handoff to cold-read

The three passes above are self-checks. The agent that wrote the formulas is grading its own arithmetic, and it will reproduce its own misreading of the governing document without noticing. So after pass 3, invoke `cold-read` at the tier its stakes test sets: FULL for arithmetic someone is paid against. Do not ask permission and do not skip it because the passes were clean; a clean pass 3 is exactly the state in which a shared misreading survives.

Hand the evaluators these, and nothing else:

- The `.xlsx` and the governing document.
- The stated inputs and the stated method, in plain text.
- The list of assumptions and hardcoded figures from the Read Me tab, with their sources.

Do **not** hand over the build script, the formula templates, or any note explaining why a figure was chosen. The recompute evaluator has to reach its own answer from the inputs before it sees how the workbook got there (cold-read step 3a: a script the main thread runs), and the evidence evaluator has to fail an unsourced figure rather than read the justification and wave it through.

Lenses: recompute, evidence and the brief always. Add a mechanism lens when the workbook models incentives or a revenue share whose behaviour changes with volume, and a hostile-reader lens when the workbook is an annex to a contract or the counterparty will see it.

Report the verdict to the owner with the file. A failing numeric criterion means the workbook does not ship, no matter how clean the recalc was.

## Delivering

Save the `.xlsx` as `(DD-MM-YY)Title With Proper Spaces.xlsx`, for example `(06-08-26)Rental Yield And IRR Model.xlsx`. When a Google Sheet is also delivered, give it that same title string, with the tab name appended when there is one Sheet per tab. Never a lowercase run-together slug and never kebab-case. Report what was verified in numbers, for example "124 formulas, zero errors, 33 numeric checks against independently computed values". Do not describe the tab layout at length; the person can open it.

If the workbook implements a contract, say plainly which document governs where the two differ, and list any conflict you found in the governing document rather than silently resolving it. Where a figure could not be verified because the source is missing, name it as an open item with the person who has to confirm it.

## Guardrails

A verified workbook is not a verified position. Rates, day count conventions and thresholds are commercial and legal terms; confirm them with the counterparty or a qualified adviser rather than treating a clean recalculation as agreement. Do not invent counterparty names, balances or rates; leave them as clearly marked placeholders. Where the workbook will be shared with a counterparty, flag who holds edit rights, because whoever can edit a workbook that a contract points at can edit the obligation.
