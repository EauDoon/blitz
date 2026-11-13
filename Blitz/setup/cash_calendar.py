"""Event-level liquidity analysis on an explicitly ordered, supplied cash calendar."""
from datetime import date
from decimal import Decimal, localcontext
import hashlib
import json
import re

from company import parse_number, read_local, valid_label
from cash_scenarios import _unique_object
from verify_archive import require


def _day(value, field):
    require(isinstance(value, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value),
            field + " must be YYYY-MM-DD")
    return date.fromisoformat(value)


def _amount(value, field):
    require(value is None or isinstance(value, str) and value != "", field + " must be a decimal string or null")
    return None if value is None else parse_number(value, field, "calendar")


def parse_calendar(data):
    obj = json.loads(data.decode("utf-8-sig"), object_pairs_hook=_unique_object)
    fields = {"schema_version", "currency", "start_date", "end_date", "opening_cash", "reserve_floor", "events"}
    require(isinstance(obj, dict) and set(obj) == fields, "calendar requires exactly the documented fields")
    require(type(obj["schema_version"]) is int and obj["schema_version"] == 1, "unsupported calendar schema_version")
    require(isinstance(obj["currency"], str) and re.fullmatch(r"[A-Z]{3}", obj["currency"]),
            "currency must be one three-letter uppercase code")
    start, end = _day(obj["start_date"], "start_date"), _day(obj["end_date"], "end_date")
    require(0 <= (end - start).days <= 3660, "calendar horizon must span 1 to 3661 days")
    require(isinstance(obj["events"], list) and len(obj["events"]) <= 10000, "provide at most 10000 events")
    events, identities, positions = [], set(), set()
    for event in obj["events"]:
        require(isinstance(event, dict) and set(event) == {"id", "date", "sequence", "direction", "amount"},
                "event requires id, date, sequence, direction and amount")
        identity = valid_label(event["id"], "event id")
        require(identity.casefold() not in identities, "duplicate event id")
        identities.add(identity.casefold())
        when = _day(event["date"], "event date")
        require(start <= when <= end, "event is outside the calendar horizon")
        sequence = event["sequence"]
        require(type(sequence) is int and 0 <= sequence <= 10000, "sequence must be an integer from 0 to 10000")
        require((when, sequence) not in positions, "event date and sequence must be unique; declare intraday order")
        positions.add((when, sequence))
        require(event["direction"] in ("in", "out"), "direction must be in or out")
        events.append({**event, "amount": _amount(event["amount"], "amount")})
    return {**obj, "opening_cash": _amount(obj["opening_cash"], "opening_cash"),
            "reserve_floor": _amount(obj["reserve_floor"], "reserve_floor"),
            "events": sorted(events, key=lambda e: (e["date"], e["sequence"]))}


def calculate_calendar(calendar, input_sha256):
    opening, floor = calendar["opening_cash"], calendar["reserve_floor"]
    unknowns = [field for field in ("opening_cash", "reserve_floor") if calendar[field] is None]
    balances = [opening]
    event_rows, daily_rows = [], []
    first_negative = {"date": calendar["start_date"], "event_id": None, "phase": "opening"} if opening is not None and opening < 0 else None
    first_below = {"date": calendar["start_date"], "event_id": None, "phase": "opening"} if opening is not None and floor is not None and opening < floor else None
    cash = opening
    with localcontext() as context:
        context.prec = 64
        for event in calendar["events"]:
            amount = event["amount"]
            if not daily_rows or daily_rows[-1]["date"] != event["date"]:
                daily_rows.append({"date": event["date"], "opening_cash": cash, "cash_in": Decimal(0),
                                   "cash_out": Decimal(0), "closing_cash": cash, "minimum_cash": cash,
                                   "event_ids": []})
            day = daily_rows[-1]
            if amount is None:
                unknowns.append("event:" + event["id"] + ":amount")
            direction = "cash_in" if event["direction"] == "in" else "cash_out"
            day[direction] = day[direction] + amount if day[direction] is not None and amount is not None else None
            cash = cash + amount * (1 if event["direction"] == "in" else -1) if cash is not None and amount is not None else None
            balances.append(cash)
            if cash is not None and cash < 0 and first_negative is None:
                first_negative = {"date": event["date"], "event_id": event["id"], "phase": "after_event"}
            if cash is not None and floor is not None and cash < floor and first_below is None:
                first_below = {"date": event["date"], "event_id": event["id"], "phase": "after_event"}
            margin = cash - floor if cash is not None and floor is not None else None
            event_rows.append({**event, "balance_after": cash, "cash_above_reserve": margin})
            day["closing_cash"] = cash
            day["minimum_cash"] = min(day["minimum_cash"], cash) if day["minimum_cash"] is not None and cash is not None else None
            day["event_ids"].append(event["id"])
        cash_complete = all(value is not None for value in balances)
        minimum = min(balances) if cash_complete else None
        funding = max(Decimal(0), floor - minimum) if floor is not None and minimum is not None else None
    return {
        "schema_version": 1, "kind": "cash_calendar", "result": "incomplete" if unknowns else "complete",
        "evidence_status": "calculated_from_supplied_unverified_inputs", "input_sha256": input_sha256,
        "currency": calendar["currency"], "start_date": calendar["start_date"], "end_date": calendar["end_date"],
        "event_order": "date_then_explicit_sequence", "opening_cash": opening, "reserve_floor": floor,
        "summary": {"event_count": len(event_rows), "ending_cash": cash, "minimum_cash": minimum,
                    "cash_balances_complete": cash_complete,
                    "additional_opening_cash_to_preserve_floor": funding,
                    "first_observed_negative_balance": first_negative,
                    "first_observed_below_reserve": first_below,
                    "negative_balance_within_horizon": True if first_negative else False if cash_complete else None,
                    "below_reserve_within_horizon": True if first_below else False if cash_complete and floor is not None else None},
        "unknown_inputs": unknowns, "events": event_rows, "days_with_events": daily_rows,
        "limits": ["Supplied cash movements only; no evidence of settlement, collection certainty, completeness or business readiness.",
                   "Dates and explicit sequences define assumed settlement order; no time zones, clearing delays or banking rules are inferred.",
                   "Opening cash is before all events on start_date. Days without events retain the last balance and are omitted from the daily table.",
                   "An unknown amount makes that and subsequent balances unknown; no zero fill or later re-anchoring is performed.",
                   "Funding is a hypothetical opening balance addition under this exact schedule, not a credit facility or permission to spend.",
                   "One currency, no conversion, interest, fees or events outside the horizon unless explicitly supplied. No external actions or writes."],
    }


def assess(raw_input):
    data = read_local(raw_input)
    return calculate_calendar(parse_calendar(data), hashlib.sha256(data).hexdigest())
