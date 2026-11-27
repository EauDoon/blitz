"""Read-only cash scenario comparisons using the company's Decimal engine."""

from decimal import Decimal, localcontext
import hashlib
import json

from company import calculate_rows, parse_rows, read_local, valid_label
from verify_archive import require

COST_FIELDS = ("variable_cash_costs", "fixed_cash_costs", "one_off_cash_costs")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate scenario JSON key: " + key)
        result[key] = value
    return result


def _factor(value, field):
    import re
    require(isinstance(value, str) and re.fullmatch(r"(?:0|[1-9][0-9]?)(?:\.[0-9]{1,6})?", value),
            field + " must be a decimal string between 0 and 10 with at most six decimal places")
    number = Decimal(value)
    require(number <= 10, field + " must be at most 10")
    return number


def parse_scenarios(data):
    try:
        specification = json.loads(data.decode("utf-8-sig"), object_pairs_hook=_unique_object)
    except RecursionError as exc:
        raise ValueError("scenario JSON nesting is too deep") from exc
    require(isinstance(specification, dict) and set(specification) == {"schema_version", "scenarios"},
            "scenario file requires only schema_version and scenarios")
    require(type(specification["schema_version"]) is int and specification["schema_version"] == 1,
            "unsupported scenario schema_version")
    scenarios = specification["scenarios"]
    require(isinstance(scenarios, list) and 1 <= len(scenarios) <= 25, "provide 1 to 25 scenarios")
    names, parsed = set(), []
    fields = {"name", "receipts_multiplier", "cash_cost_multiplier", "receipt_delay_periods"}
    for item in scenarios:
        require(isinstance(item, dict) and set(item) <= fields and "name" in item,
                "scenario has missing name or unsupported fields")
        name = valid_label(item["name"], "scenario name")
        require(name.casefold() not in names, "duplicate scenario name")
        names.add(name.casefold())
        delay = item.get("receipt_delay_periods", 0)
        require(type(delay) is int and 0 <= delay <= 1200, "receipt_delay_periods must be an integer from 0 to 1200")
        parsed.append({"name": name, "receipt_delay_periods": delay,
                       "receipts_multiplier": _factor(item.get("receipts_multiplier", "1"), "receipts_multiplier"),
                       "cash_cost_multiplier": _factor(item.get("cash_cost_multiplier", "1"), "cash_cost_multiplier")})
    return parsed


def _summary(forecast):
    closings = [row["closing_cash"] for row in forecast["periods"]]
    margins = [row["cash_above_reserve"] for row in forecast["periods"]]
    return {
        "ending_cash": closings[-1],
        "minimum_closing_cash": min(closings) if all(value is not None for value in closings) else None,
        "maximum_closing_reserve_gap": max(Decimal(0), -min(margins)) if all(value is not None for value in margins) else None,
        "first_observed_closing_below_reserve_period": forecast["first_observed_closing_below_reserve_period"],
    }


def compare(raw_input, raw_scenarios):
    data, specification = read_local(raw_input), read_local(raw_scenarios)
    source_hash = hashlib.sha256(data).hexdigest()
    rows, scenarios = parse_rows(data), parse_scenarios(specification)
    # Validate the original continuity before replacing later opening anchors.
    baseline = calculate_rows(rows, source_hash)
    baseline_summary = _summary(baseline)
    results = []
    with localcontext() as context:
        context.prec = 64
        for scenario in scenarios:
            delay = scenario["receipt_delay_periods"]
            shifted = [dict(row) for row in rows]
            receipts = [row["cash_receipts"] * scenario["receipts_multiplier"]
                        if row["cash_receipts"] is not None else None for row in rows]
            for index, row in enumerate(shifted):
                if index:
                    row["opening_cash"] = None
                row["cash_receipts"] = receipts[index - delay] if index >= delay else Decimal(0)
                for field in COST_FIELDS:
                    if row[field] is not None:
                        row[field] *= scenario["cash_cost_multiplier"]
            deferred = receipts[max(0, len(receipts) - delay):] if delay else []
            forecast = calculate_rows(shifted, source_hash)
            summary = _summary(forecast)
            ending, base_ending = summary["ending_cash"], baseline_summary["ending_cash"]
            results.append({
                "assumptions": scenario,
                "summary": summary,
                "ending_cash_difference_from_baseline": ending - base_ending if ending is not None and base_ending is not None else None,
                "receipts_deferred_beyond_horizon": sum(deferred, Decimal(0)) if all(value is not None for value in deferred) else None,
                "forecast": forecast,
            })
    return {
        "result": "complete" if baseline["result"] == "complete" and all(item["forecast"]["result"] == "complete" for item in results) else "incomplete",
        "schema_version": 1,
        "input_sha256": source_hash,
        "scenario_input_sha256": hashlib.sha256(specification).hexdigest(),
        "baseline": baseline,
        "baseline_summary": baseline_summary,
        "scenarios": results,
        "limits": [
            "Hypothetical cash assumptions only, not probabilities, recommendations or accepted budgets.",
            "Later opening cash anchors are recomputed from the first opening balance; unknown amounts remain unknown, including when multiplied by zero.",
            "Delay shifts the supplied receipts schedule; no receipts arriving from before the supplied horizon are assumed. Deferred receipts are not a promise of collection.",
            "Cash cost stress affects variable, fixed and one-off cash costs only. Earned revenue, delivery economics, refunds, taxes and financing are unchanged.",
            "Reserve gaps use closing balances only and are not an intraperiod funding requirement. Unknown periods prevent a complete minimum or maximum.",
            "Input files are read only; no forecast is saved or adopted and no external action occurs.",
        ],
    }
