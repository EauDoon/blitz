#!/usr/bin/env python3
"""Create a draft company workspace or calculate a local, supplied cash forecast.

Standard library only. No network, incorporation, payment, outreach, or agent
integration. Requires the adjacent verify_archive.py path/publication guards.
"""
import argparse
import csv
from decimal import Decimal, localcontext
import hashlib
import html
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import unicodedata

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).absolute().parent))
from verify_archive import guard_local_path, publish_directory, require, validate_destination

KIT = Path(__file__).absolute().parents[1]
MAX_INPUT_BYTES = 2 * 1024 * 1024
MAX_PERIODS = 1200
COLUMNS = (
    "period", "currency", "opening_cash", "cash_receipts", "refunds_cash_out",
    "variable_cash_costs", "fixed_cash_costs", "one_off_cash_costs",
    "financing_cash_in", "financing_cash_out", "tax_cash", "reserve_floor",
    "units_delivered", "earned_revenue", "variable_delivery_cost",
    "founder_delivery_hours", "available_delivery_hours",
)
INFLOWS = ("cash_receipts", "financing_cash_in")
OUTFLOWS = (
    "refunds_cash_out", "variable_cash_costs", "fixed_cash_costs",
    "one_off_cash_costs", "financing_cash_out", "tax_cash",
)
LIMITS = (
    "Arithmetic on supplied assumptions only. Inputs are not independently verified; "
    "this is not evidence of profitability, demand, legal formation, launch readiness, "
    "or future receipts. Periods stay in supplied order and must cover consistent, "
    "chronological intervals. No runway is extrapolated beyond the supplied horizon."
    " Summary breach flags examine closing balances only; intraperiod cash timing is not modeled."
)


def read_local(raw):
    path = guard_local_path(raw)
    require(path.is_file() and stat.S_ISREG(path.stat().st_mode), "input is not a regular file")
    require(path.stat().st_size <= MAX_INPUT_BYTES, "input exceeds 2 MiB")
    with path.open("rb") as stream:
        data = stream.read(MAX_INPUT_BYTES + 1)
    require(len(data) <= MAX_INPUT_BYTES, "input exceeds 2 MiB")
    return data


def valid_label(value, field):
    require(isinstance(value, str) and value == value.strip() and 1 <= len(value) <= 200,
            field + " must contain 1 to 200 characters without surrounding whitespace")
    require(not any(unicodedata.category(c).startswith("C") for c in value),
            field + " contains control characters")
    require(unicodedata.normalize("NFC", value) == value, field + " must use NFC Unicode")
    return value


def markdown(value):
    return re.sub(r"([\\`*_{}\[\]()#+.!|>\-])", r"\\\1", html.escape(value, quote=False))


def destination(raw, kit):
    out = validate_destination(raw)
    require(unicodedata.normalize("NFC", str(out)) == str(out), "output path must use NFC Unicode")
    require(not any(part.casefold() in {".git", ".baseline"} for part in out.parts),
            "repository metadata or immutable baseline output is prohibited")
    require(out != kit and kit not in out.parents and out not in kit.parents,
            "output must not overlap the source kit")
    return out


def initialize(raw_out, name, owner):
    name, owner = valid_label(name, "name"), valid_label(owner, "owner")
    kit = guard_local_path(KIT)
    out = destination(raw_out, kit)
    sources = {p: read_local(kit / "templates" / p)
               for p in ("company-brief.md", "company-cash.csv")}
    # A stale/incompatible cash template cannot silently become the new interface.
    parse_rows(sources["company-cash.csv"])
    brief = sources["company-brief.md"].decode("utf-8")
    name_md, owner_md = markdown(name), markdown(owner)
    brief = brief.replace("[COMPANY NAME]", name_md).replace("[OWNER]", owner_md)
    contents = {
        "company-brief.md": brief,
        "company-cash.csv": sources["company-cash.csv"].decode("utf-8"),
        "README.md": (
            f"# {name_md}: draft company workspace\n\n"
            "Start with [the company brief](company-brief.md), then record the adopted "
            "position in [file 03](context/03%20Position%20Of%20Record.md) only after "
            "the owner makes that decision. This initializer created drafts; it did "
            "not validate demand, form an entity, authorize external actions, or "
            "establish launch readiness.\n\n"
            "[File 00](context/00%20Read%20Me%20First.md) identifies the owner and scope. "
            "[File 09](context/09%20Open%20Questions.md) holds missing evidence, and "
            "[file 10](context/10%20Decision%20Log.md) holds consequential decisions. "
            "Keep one canonical writer. Do not put credentials in these files.\n\n"
            "Use company-cash.csv with the Blitz setup/company.py cash command. "
            "Blank inputs are unknown; enter 0 only when zero is supported. Record "
            "sources, status, period duration, and units in the brief. No software, "
            "scheduler, account connection, or agent was installed.\n"
        ),
        "context/00 Read Me First.md": (
            f"# {name_md} 00: Read Me First\n\n"
            f"Scribe / canonical owner: {owner_md}. Status: initialized draft.\n\n"
            "## Project profile\n\n| Field | Value |\n|---|---|\n"
            f"| Type | venture |\n| Decision owner | {owner_md} |\n"
            "| Mandate pack | company profile; scope not yet adopted |\n"
            "| Regulated | Unknown; determine activity and jurisdictions |\n\n"
            "## Project skill map\n\nNo project skill or agent integration is established.\n\n"
            "## What is live now\n\nOnly this draft workspace was created. No pilot was commissioned.\n\n"
            "## Stage records\n\nIngestion. No readiness transition is established.\n\n"
            "## File map\n\n00: owner and scope. 03: adopted position. 09: open questions. "
            "10: decision log. ../company-brief.md: proposed business and evidence. "
            "../company-cash.csv: supplied financial assumptions.\n\n"
            "## Canonical locations\n\nThis workspace is the draft working location. "
            "Any ownership transfer or external canonical location remains undecided.\n\n"
            "## Capability manifest (summary)\n\nLocal file creation only. Other tools and "
            "save/recovery routes remain unverified for this company.\n\n"
            "## Allowlist: files that may leave this project\n\nEmpty. No export has been authorized.\n"
        ),
        "context/03 Position Of Record.md": (
            f"# {name_md} 03: Position Of Record\n\n"
            "Status: DRAFT, UNADOPTED. No governing business position exists yet.\n\n"
            "## 1. The position\n\nComplete the company brief and review the supporting evidence.\n\n"
            "## 2. Mandate statement\n\nObjective, success measure, scope, constraints, "
            "decision rights, deadlines and assumptions remain undecided.\n\n"
            "## 3. Scope\n\nLocal planning drafts only. External actions require applicable authority.\n\n"
            "## 4. What this position does not decide\n\nCustomer, offer, formation, budget, "
            "pricing, regulated activities, and launch decision remain open in file 09.\n\n"
            "## 5. Version history\n\nNo adopted version.\n\n"
            "## Revision rule\n\nOnly an explicit owner decision may adopt or replace the "
            "position. Log its scope, evidence, version and affected outputs in file 10.\n"
        ),
        "context/09 Open Questions.md": (
            f"# {name_md} 09: Open Questions\n\n"
            "Close an item only after reviewing the settling evidence.\n\n"
            "| ID | Question | Evidence that settles it | Owner | Status |\n"
            "|---|---|---|---|---|\n"
            f"| A1 | What cash, costs and collections are supported? | Dated sources "
            f"and forecast assumptions | {owner_md} | OPEN |\n"
            f"| B1 | Which formation, tax or regulatory questions apply? | Activity, "
            f"jurisdiction and applicable professional review | {owner_md} | OPEN |\n"
            f"| C1 | What customer and offer warrant the next test? | Customer evidence "
            f"and acceptance criterion in the brief | {owner_md} | OPEN |\n"
            f"| D1 | Can delivery fit available founder capacity? | Defined service "
            f"unit and measured hours | {owner_md} | OPEN |\n\n"
            "## Source register\n\nNo company evidence has been supplied by the initializer.\n"
        ),
        "context/10 Decision Log.md": (
            f"# {name_md} 10: Decision Log\n\n"
            "Append only. Record actual decisions with date, decision-maker, scope and "
            "evidence. Correct prior entries with a superseding entry.\n\n"
            "## Entries\n\nNo business decision or readiness gate was made by this initializer.\n"
        ),
    }
    files = {path: text.encode("utf-8") for path, text in contents.items()}
    result = {
        "result": "created_draft", "company": name, "owner": owner,
        "output": str(out), "readiness": "unassessed", "adopted_position": False,
        "files": [{"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                  for path, data in sorted(files.items())],
        "template_sha256": {path: hashlib.sha256(data).hexdigest() for path, data in sources.items()},
        "limits": "Draft local files only. No business, financial, legal, or launch acceptance is established. "
                  "Atomic publication supports Windows and Linux on a stable local filesystem.",
    }
    temp = tempfile.TemporaryDirectory(prefix=".blitz-company-", dir=out.parent)
    published, failure = False, None
    try:
        stage = Path(temp.name) / "ready"
        stage.mkdir()
        for name, data in files.items():
            path = stage / name
            path.parent.mkdir(exist_ok=True)
            with path.open("xb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            require(path.read_bytes() == data, "saved byte mismatch:" + name)
        destination(out, kit)
        publish_directory(stage, out)
        published = True
    except BaseException as exc:
        failure = exc
        raise
    finally:
        try:
            temp.cleanup()
        except OSError as exc:
            warning = {"path": temp.name, "error": str(exc)}
            if published:
                result["cleanup_warning"] = warning
            elif failure is not None:
                failure.cleanup_warning = warning
            else:
                raise
    return result


def parse_number(value, field, period):
    if value == "":
        return None
    # Bounded fixed-point values keep both arithmetic and resource use predictable.
    require(re.fullmatch(r"-?(?:0|[1-9][0-9]{0,17})(?:\.[0-9]{1,6})?", value) is not None,
            period + ": " + field + " must be a finite decimal with at most 18 integer and 6 fractional digits")
    number = Decimal(value)
    require(number >= 0 or field in {"opening_cash", "earned_revenue"},
            period + ": " + field + " must be nonnegative")
    return number


def parse_rows(data):
    reader = csv.reader(io.StringIO(data.decode("utf-8-sig"), newline=""), strict=True)
    header = next(reader, None)
    require(header is not None and len(header) == len(COLUMNS) and set(header) == set(COLUMNS),
            "CSV header must contain each documented column exactly once")
    rows, seen, currencies = [], set(), set()
    for raw in reader:
        require(len(rows) < MAX_PERIODS, "CSV exceeds 1200 periods")
        require(len(raw) == len(header), "CSV row has missing or extra fields")
        values = dict(zip(header, (v.strip() for v in raw)))
        period = valid_label(values["period"], "period")
        require(period.casefold() not in seen, "duplicate period:" + period)
        seen.add(period.casefold())
        currency = values["currency"]
        require(currency == "" or re.fullmatch(r"[A-Z]{3}", currency),
                period + ": currency must be a three-letter uppercase code or blank when unknown")
        if currency:
            currencies.add(currency)
        require(len(currencies) <= 1, "mixed currencies require separate forecasts")
        row = {"period": period, "currency": currency or None}
        row.update({key: parse_number(values[key], key, period) for key in COLUMNS[2:]})
        rows.append(row)
    require(bool(rows), "CSV must contain at least one period")
    return rows


def known_sum(row, fields):
    return sum((row[field] for field in fields), Decimal(0)) if all(row[f] is not None for f in fields) else None


def ratio(numerator, denominator):
    if numerator is None or denominator is None or denominator == 0:
        return None
    return (numerator / denominator).quantize(Decimal("0.000001"))


def decimal_string(value):
    if isinstance(value, Decimal):
        return format(value if value else Decimal(0), "f")
    raise TypeError("unsupported JSON value")


def forecast(raw_input):
    data = read_local(raw_input)
    rows = parse_rows(data)
    return calculate_rows(rows, hashlib.sha256(data).hexdigest())


def calculate_rows(rows, input_sha256):
    """Calculate parsed rows without mutating them; shared by scenario analysis."""
    periods, previous_close = [], None
    with localcontext() as context:
        context.prec = 64
        for index, row in enumerate(rows):
            warnings = []
            opening = row["opening_cash"]
            opening_source = "supplied" if opening is not None else "unknown"
            if index and opening is None and previous_close is not None:
                opening, opening_source = previous_close, "prior_computed_closing"
            elif index and opening is not None:
                if previous_close is not None:
                    require(opening == previous_close, row["period"] + ": opening_cash differs from prior closing_cash")
                else:
                    warnings.append("prior cash continuity is unknown; this supplied opening is a new anchor")
            unknown = [key for key in COLUMNS[1:] if row[key] is None
                       and not (key == "opening_cash" and opening is not None)]
            cash_in = known_sum(row, INFLOWS) if row["currency"] else None
            cash_out = known_sum(row, OUTFLOWS) if row["currency"] else None
            change = cash_in - cash_out if cash_in is not None and cash_out is not None else None
            closing = opening + change if opening is not None and change is not None else None
            above_reserve = closing - row["reserve_floor"] if closing is not None and row["reserve_floor"] is not None else None
            contribution = (row["earned_revenue"] - row["variable_delivery_cost"]
                            if row["currency"] and row["earned_revenue"] is not None
                            and row["variable_delivery_cost"] is not None else None)
            units, hours, available = (row[key] for key in (
                "units_delivered", "founder_delivery_hours", "available_delivery_hours"))
            if opening is not None and opening < 0:
                warnings.append("negative opening cash")
            if opening is not None and row["reserve_floor"] is not None and opening < row["reserve_floor"]:
                warnings.append("opening cash is below the supplied reserve floor")
            if closing is not None and closing < 0:
                warnings.append("negative closing cash; financing or payment timing must be resolved")
            if above_reserve is not None and above_reserve < 0:
                warnings.append("closing cash is below the supplied reserve floor")
            if contribution is not None and contribution < 0:
                warnings.append("negative contribution before fixed costs and unpaid founder time")
            if units == 0:
                warnings.append("per-unit metrics are undefined with zero delivered units")
            if available == 0:
                warnings.append("utilization is undefined with zero available delivery hours")
            if hours == 0:
                warnings.append("capacity in units is undefined with zero measured delivery hours")
            if hours is not None and available is not None and hours > available:
                warnings.append("founder delivery hours exceed available delivery hours")
            capacity = ratio(available * units, hours) if available is not None and units is not None and units > 0 else None
            periods.append({
                "period": row["period"], "currency": row["currency"],
                "result": "incomplete" if unknown else "complete", "unknown_fields": unknown,
                "opening_cash": opening, "opening_source": opening_source,
                "cash_in": cash_in, "cash_out": cash_out, "net_cash_change": change,
                "closing_cash": closing, "reserve_floor": row["reserve_floor"],
                "cash_above_reserve": above_reserve,
                "contribution": contribution, "contribution_per_unit": ratio(contribution, units),
                "delivery_hours_per_unit": ratio(hours, units),
                "founder_utilization": ratio(hours, available),
                "capacity_units_at_same_delivery_rate": capacity, "warnings": warnings,
            })
            previous_close = closing
    first_negative = next((p["period"] for p in periods if p["closing_cash"] is not None and p["closing_cash"] < 0), None)
    first_below = next((p["period"] for p in periods if p["cash_above_reserve"] is not None and p["cash_above_reserve"] < 0), None)
    complete_cash = all(p["closing_cash"] is not None for p in periods)
    complete_reserve = all(p["cash_above_reserve"] is not None for p in periods)
    return {
        "result": "complete" if all(p["result"] == "complete" for p in periods) else "incomplete",
        "evidence_status": "calculated_from_supplied_unverified_inputs",
        "input_sha256": input_sha256,
        "currency": next((p["currency"] for p in periods if p["currency"]), None),
        "forecast_horizon_periods": len(periods), "period_order": "as_supplied",
        "cash_observations_complete": complete_cash,
        "first_observed_negative_closing_period": first_negative,
        "negative_closing_within_horizon": True if first_negative else False if complete_cash else None,
        "first_observed_closing_below_reserve_period": first_below,
        "closing_below_reserve_within_horizon": True if first_below else False if complete_reserve else None,
        "runway_beyond_horizon": "not_estimated",
        "periods": periods, "limits": LIMITS,
        "metric_definitions": {
            "closing_cash": "opening_cash + cash_receipts + financing_cash_in - refunds_cash_out - variable_cash_costs - fixed_cash_costs - one_off_cash_costs - financing_cash_out - tax_cash",
            "contribution": "earned_revenue - variable_delivery_cost; before fixed costs and unpaid founder time; not profit",
            "founder_utilization": "founder_delivery_hours / available_delivery_hours, fraction not percent",
            "capacity_units_at_same_delivery_rate": "available_delivery_hours * units_delivered / founder_delivery_hours; assumes the same unit and measured delivery rate",
            "rounding": "Cash and contribution remain exact decimals; ratios use six fractional digits, half-even rounding. Null means unknown or an undefined zero-denominator ratio.",
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="create draft files in a new local directory")
    init.add_argument("--out", required=True)
    init.add_argument("--name", required=True)
    init.add_argument("--owner", required=True)
    cash = commands.add_parser("cash", help="calculate a supplied CSV forecast; blank means unknown")
    cash.add_argument("input")
    stress = commands.add_parser("stress", help="compare a forecast with local cash scenarios")
    stress.add_argument("input")
    stress.add_argument("--scenarios", required=True, help="scenario JSON; see cash-scenarios.md")
    capacity = commands.add_parser("capacity", help="assess a supplied delivery resource plan")
    capacity.add_argument("input", help="plan JSON; see delivery-capacity.md")
    calendar = commands.add_parser("calendar", help="inspect event-level liquidity and settlement order")
    calendar.add_argument("input", help="calendar JSON; see cash-calendar.md")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = initialize(args.out, args.name, args.owner)
        elif args.command == "stress":
            from cash_scenarios import compare
            result = compare(args.input, args.scenarios)
        elif args.command == "calendar":
            from cash_calendar import assess
            result = assess(args.input)
        elif args.command == "capacity":
            from delivery_capacity import assess
            result = assess(args.input)
        else:
            result = forecast(args.input)
    except (OSError, ValueError, UnicodeError, csv.Error, RecursionError) as exc:
        result = {"result": "error", "errors": [str(exc)]}
        if getattr(exc, "cleanup_warning", None):
            result["cleanup_warning"] = exc.cleanup_warning
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 1
    print(json.dumps(result, default=decimal_string, ensure_ascii=True, indent=2, allow_nan=False))
    return 2 if result["result"] == "incomplete" else 0


if __name__ == "__main__":
    sys.exit(main())
