"""Assess a supplied delivery plan without allocating resources or adopting it."""

from collections import deque
from decimal import Decimal, localcontext
import hashlib
import json
import re

from company import read_local, valid_label
from verify_archive import require

LIMITS = [
    "Calculated from supplied, unverified hours; no staffing, scheduling, spending or commitment is authorized.",
    "This assesses the supplied allocations, not an optimized schedule or a proof that an alternative plan is impossible.",
    "Periods follow the supplied order. Hours must be comparable within each resource; resources are not interchangeable.",
    "Dependencies require predecessor effort to be fully allocated in an earlier period. Same-period handoffs are not assumed.",
    "Planned completion is conditional on the allocations being delivered; acceptance, quality, leave and support must be accounted for by the owner.",
    "Period totals do not model intraperiod timing, indivisible shifts or tasks, parallelism limits, or resources outside this plan.",
    "Null means unknown. Capacity must be net of obligations outside the plan; no unused hours carry between periods.",
    "Input files are read only. This is neither an adopted resource plan nor a business-readiness decision.",
]


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate capacity JSON key: " + key)
        result[key] = value
    return result


def _fields(value, fields, label):
    require(isinstance(value, dict) and set(value) == set(fields),
            label + " has missing or unsupported fields")


def _identifier(value, field):
    require(isinstance(value, str) and re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", value),
            field + " must be a lowercase identifier of 1 to 64 characters")
    return value


def _hours(value, field, *, unknown=False, positive=False):
    if unknown and value is None:
        return None
    require(isinstance(value, str) and re.fullmatch(r"(?:0|[1-9][0-9]{0,11})(?:\.[0-9]{1,6})?", value),
            field + " must be a nonnegative decimal string with at most 12 integer and 6 fractional digits"
            + (", or null for unknown" if unknown else ""))
    number = Decimal(value)
    require(not positive or number > 0, field + " must be positive")
    return number


def parse_plan(data):
    try:
        plan = json.loads(data.decode("utf-8-sig"), object_pairs_hook=_unique_object)
    except RecursionError as exc:
        raise ValueError("capacity JSON nesting is too deep") from exc
    _fields(plan, {"schema_version", "periods", "resources", "work_items", "allocations"}, "capacity plan")
    require(type(plan["schema_version"]) is int and plan["schema_version"] == 1, "unsupported capacity schema_version")
    periods = plan["periods"]
    require(isinstance(periods, list) and 1 <= len(periods) <= 120, "provide 1 to 120 periods")
    periods = [valid_label(value, "period") for value in periods]
    require(len({p.casefold() for p in periods}) == len(periods), "duplicate capacity period")
    resources = plan["resources"]
    require(isinstance(resources, list) and 1 <= len(resources) <= 50, "provide 1 to 50 resources")
    parsed_resources = {}
    for resource in resources:
        _fields(resource, {"id", "name", "available_hours"}, "resource")
        identifier = _identifier(resource["id"], "resource id")
        require(identifier not in parsed_resources, "duplicate resource id: " + identifier)
        _fields(resource["available_hours"], periods, identifier + " available_hours")
        parsed_resources[identifier] = {
            "id": identifier, "name": valid_label(resource["name"], "resource name"),
            "available_hours": {p: _hours(resource["available_hours"][p], identifier + " availability", unknown=True)
                                for p in periods},
        }
    work = plan["work_items"]
    require(isinstance(work, list) and 1 <= len(work) <= 500, "provide 1 to 500 work_items")
    parsed_work = {}
    for item in work:
        _fields(item, {"id", "name", "owner", "due_period", "depends_on", "required_hours"}, "work item")
        identifier = _identifier(item["id"], "work item id")
        require(identifier not in parsed_work, "duplicate work item id: " + identifier)
        require(isinstance(item["due_period"], str) and item["due_period"] in periods, identifier + ": unknown due_period")
        dependencies = item["depends_on"]
        require(isinstance(dependencies, list) and len(dependencies) <= 500, "depends_on must be a list of at most 500 ids")
        dependencies = [_identifier(d, "dependency") for d in dependencies]
        require(len(set(dependencies)) == len(dependencies), identifier + ": duplicate dependency")
        effort = item["required_hours"]
        require(isinstance(effort, dict) and effort and set(effort) <= set(parsed_resources),
                identifier + ": required_hours must name at least one known resource")
        parsed_work[identifier] = {
            "id": identifier, "name": valid_label(item["name"], "work item name"),
            "owner": valid_label(item["owner"], "work item owner"),
            "due_period": item["due_period"], "depends_on": dependencies,
            "required_hours": {r: _hours(value, identifier + " effort", unknown=True, positive=True)
                               for r, value in effort.items()},
        }
    # Iterative graph validation avoids recursion limits and never silently drops an edge.
    children = {identifier: [] for identifier in parsed_work}
    remaining = {}
    for identifier, item in parsed_work.items():
        remaining[identifier] = len(item["depends_on"])
        for dependency in item["depends_on"]:
            require(dependency in parsed_work, identifier + ": unknown dependency " + dependency)
            children[dependency].append(identifier)
    ready = deque(identifier for identifier, count in remaining.items() if not count)
    visited = 0
    while ready:
        identifier = ready.popleft()
        visited += 1
        for child in children[identifier]:
            remaining[child] -= 1
            if not remaining[child]:
                ready.append(child)
    require(visited == len(parsed_work), "work dependency graph contains a cycle")
    allocations = plan["allocations"]
    require(isinstance(allocations, list) and len(allocations) <= 20000, "provide at most 20000 allocations")
    parsed_allocations, seen = [], set()
    for allocation in allocations:
        _fields(allocation, {"work_item", "resource", "period", "hours"}, "allocation")
        work_id = _identifier(allocation["work_item"], "allocation work_item")
        resource_id = _identifier(allocation["resource"], "allocation resource")
        period = allocation["period"]
        require(work_id in parsed_work, "allocation names an unknown work item")
        require(resource_id in parsed_work[work_id]["required_hours"], "allocation resource is not required by this work item")
        require(isinstance(period, str) and period in periods, "allocation names an unknown period")
        key = (work_id, resource_id, period)
        require(key not in seen, "duplicate allocation for work item, resource and period")
        seen.add(key)
        parsed_allocations.append({"work_item": work_id, "resource": resource_id, "period": period,
                                   "hours": _hours(allocation["hours"], "allocation hours", positive=True)})
    return {"periods": periods, "resources": parsed_resources,
            "work_items": parsed_work, "allocations": parsed_allocations}


def calculate_plan(plan, input_sha256):
    """Assess parsed data, preserving it and using exact fixed-point hours."""
    periods, resources, work = (plan[key] for key in ("periods", "resources", "work_items"))
    positions = {period: index for index, period in enumerate(periods)}
    loads = {(p, r): Decimal(0) for p in periods for r in resources}
    contributors = {(p, r): [] for p in periods for r in resources}
    assigned = {identifier: {} for identifier in work}
    unknowns, resource_periods, work_results, dependencies = [], [], [], []
    with localcontext() as context:
        context.prec = 64
        for allocation in plan["allocations"]:
            identifier, r, p, hours = (allocation[k] for k in ("work_item", "resource", "period", "hours"))
            loads[p, r] += hours
            contributors[p, r].append({"work_item": identifier, "hours": hours})
            assigned[identifier][r, p] = hours
        for p in periods:
            for r, resource in resources.items():
                available, planned = resource["available_hours"][p], loads[p, r]
                if available is None:
                    unknowns.append({"kind": "available_hours", "resource": r, "period": p})
                headroom = available - planned if available is not None else None
                resource_periods.append({
                    "period": p, "resource": r, "resource_name": resource["name"],
                    "available_hours": available, "planned_hours": planned,
                    "headroom_hours": headroom,
                    "overload_hours": max(-headroom, Decimal(0)) if headroom is not None else None,
                    "work_items": contributors[p, r],
                })
        for identifier, item in work.items():
            effort_rows, completion_indexes, due_checks = [], [], []
            for r, required in item["required_hours"].items():
                total, by_due, completion = Decimal(0), Decimal(0), None
                for index, p in enumerate(periods):
                    total += assigned[identifier].get((r, p), Decimal(0))
                    if index <= positions[item["due_period"]]:
                        by_due = total
                    if required is not None and completion is None and total >= required:
                        completion = index
                if required is None:
                    unknowns.append({"kind": "required_hours", "work_item": identifier, "resource": r})
                completion_indexes.append(completion)
                due_checks.append(by_due >= required if required is not None else None)
                effort_rows.append({
                    "resource": r, "required_hours": required, "planned_hours": total,
                    "planned_by_due_hours": by_due,
                    "uncovered_hours": max(required - total, Decimal(0)) if required is not None else None,
                    "excess_planned_hours": max(total - required, Decimal(0)) if required is not None else None,
                })
            first = min((positions[p] for _, p in assigned[identifier]), default=None)
            complete = max(completion_indexes) if all(index is not None for index in completion_indexes) else None
            known_gap = any(row["uncovered_hours"] is not None and row["uncovered_hours"] > 0 for row in effort_rows)
            work_results.append({
                "id": identifier, "name": item["name"], "owner": item["owner"], "due_period": item["due_period"],
                "first_planned_period": periods[first] if first is not None else None,
                "planned_completion_period": periods[complete] if complete is not None else None,
                "effort_status": "uncovered" if known_gap else "unknown" if None in completion_indexes else "covered",
                "due_status": "missed" if False in due_checks else "unknown" if None in due_checks else "within_due_period",
                "effort": effort_rows,
            })
        result_by_id = {item["id"]: item for item in work_results}
        for identifier, item in work.items():
            first = result_by_id[identifier]["first_planned_period"]
            for predecessor in item["depends_on"]:
                prior = result_by_id[predecessor]
                finish = prior["planned_completion_period"]
                if first is None:
                    status, reason = "not_scheduled", "dependent work has no allocation"
                elif prior["effort_status"] == "uncovered":
                    status, reason = "conflict", "predecessor effort is not fully allocated within the horizon"
                elif finish is None:
                    status, reason = "unknown", "predecessor completion depends on unknown effort"
                elif positions[first] <= positions[finish]:
                    status, reason = "conflict", "dependent work must start in a period after predecessor completion"
                else:
                    status, reason = "satisfied", "predecessor effort is allocated in earlier periods"
                dependencies.append({"work_item": identifier, "predecessor": predecessor,
                                     "status": status, "reason": reason})
    bottlenecks = [row for row in resource_periods if row["overload_hours"] is not None and row["overload_hours"] > 0]
    uncovered = [item["id"] for item in work_results if item["effort_status"] == "uncovered"]
    missed = [item["id"] for item in work_results if item["due_status"] == "missed"]
    dependency_conflicts = [edge for edge in dependencies if edge["status"] == "conflict"]
    conflicts = bool(bottlenecks or uncovered or missed or dependency_conflicts)
    return {
        "schema_version": 1, "result": "incomplete" if unknowns else "complete",
        "assessment": "conflicts_found" if conflicts else "unknown" if unknowns else "within_supplied_limits",
        "evidence_status": "calculated_from_supplied_unverified_inputs", "input_sha256": input_sha256,
        "period_order": "as_supplied", "periods": periods,
        "summary": {"resource_count": len(resources), "work_item_count": len(work),
                    "overloaded_resource_periods": len(bottlenecks), "uncovered_work_items": uncovered,
                    "missed_due_work_items": missed, "dependency_conflicts": len(dependency_conflicts),
                    "unknown_input_count": len(unknowns)},
        "bottlenecks": bottlenecks, "resource_periods": resource_periods,
        "work_items": work_results, "dependencies": dependencies, "unknown_inputs": unknowns,
        "limits": LIMITS,
    }


def assess(raw_input):
    data = read_local(raw_input)
    return calculate_plan(parse_plan(data), hashlib.sha256(data).hexdigest())
