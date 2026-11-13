"""Independently synthetic capacity, ordering, unknown-input and CLI cases."""
import copy
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Blitz/setup"))
from delivery_capacity import assess, calculate_plan, parse_plan


def fixture():
    return {
        "schema_version": 1, "periods": ["P1", "P2", "P3"],
        "resources": [
            {"id": "maker", "name": "Synthetic maker", "available_hours": {"P1": "2", "P2": "2", "P3": "2"}},
            {"id": "checker", "name": "Synthetic checker", "available_hours": {"P1": "1", "P2": "1", "P3": "1"}},
        ],
        "work_items": [
            {"id": "first", "name": "Synthetic first task", "owner": "Example owner", "due_period": "P1",
             "depends_on": [], "required_hours": {"maker": "2", "checker": "1"}},
            {"id": "next", "name": "Synthetic next task", "owner": "Example owner", "due_period": "P2",
             "depends_on": ["first"], "required_hours": {"maker": "2"}},
        ],
        "allocations": [
            {"work_item": "first", "resource": "maker", "period": "P1", "hours": "2"},
            {"work_item": "first", "resource": "checker", "period": "P1", "hours": "1"},
            {"work_item": "next", "resource": "maker", "period": "P2", "hours": "2"},
        ],
    }


def evaluate(value):
    parsed = parse_plan(json.dumps(value).encode())
    before = copy.deepcopy(parsed)
    result = calculate_plan(parsed, "synthetic")
    assert parsed == before, "assessment mutated the parsed input"
    return result


class DeliveryCapacityTests(unittest.TestCase):
    def test_complete_plan_checks_every_resource_and_dependency(self):
        result = evaluate(fixture())
        self.assertEqual(result["assessment"], "within_supplied_limits")
        self.assertEqual(result["result"], "complete")
        self.assertEqual(len(result["resource_periods"]), 6)
        self.assertEqual(result["dependencies"][0]["status"], "satisfied")
        self.assertEqual(result["work_items"][1]["planned_completion_period"], "P2")

    def test_shared_load_overload_and_zero_capacity(self):
        plan = fixture()
        plan["work_items"][1]["depends_on"] = []
        plan["allocations"][2]["period"] = "P1"
        result = evaluate(plan)
        self.assertEqual(result["bottlenecks"][0]["overload_hours"], Decimal("2"))
        self.assertEqual({w["work_item"] for w in result["bottlenecks"][0]["work_items"]}, {"first", "next"})
        plan["resources"][0]["available_hours"]["P1"] = "0"
        self.assertEqual(evaluate(plan)["bottlenecks"][0]["overload_hours"], Decimal("4"))

    def test_exact_fractional_hours_and_excess_consume_capacity(self):
        plan = fixture()
        plan["work_items"][1]["required_hours"]["maker"] = "0.3"
        plan["resources"][0]["available_hours"]["P2"] = "0.1"
        plan["resources"][0]["available_hours"]["P3"] = "0.2"
        plan["allocations"][2]["hours"] = "0.1"
        plan["allocations"].append({"work_item": "next", "resource": "maker", "period": "P3", "hours": "0.2"})
        result = evaluate(plan)
        self.assertEqual(result["bottlenecks"], [])
        self.assertEqual(result["work_items"][1]["effort"][0]["planned_hours"], Decimal("0.3"))
        self.assertEqual(result["work_items"][1]["effort_status"], "covered")
        self.assertEqual(result["work_items"][1]["due_status"], "missed")
        plan["allocations"][3]["hours"] = "0.4"
        result = evaluate(plan)
        self.assertEqual(result["bottlenecks"][0]["overload_hours"], Decimal("0.2"))
        self.assertEqual(result["work_items"][1]["effort"][0]["excess_planned_hours"], Decimal("0.2"))

    def test_deadline_checks_all_required_resources(self):
        plan = fixture()
        plan["allocations"][1]["period"] = "P3"
        result = evaluate(plan)
        self.assertEqual(result["work_items"][0]["planned_completion_period"], "P3")
        self.assertEqual(result["work_items"][0]["due_status"], "missed")
        self.assertEqual(result["dependencies"][0]["status"], "conflict")

    def test_same_period_dependency_and_early_partial_work_are_conflicts(self):
        plan = fixture()
        plan["allocations"][2]["period"] = "P1"
        self.assertEqual(evaluate(plan)["dependencies"][0]["status"], "conflict")
        plan["allocations"][2]["hours"] = "0.01"
        plan["allocations"].append({"work_item": "next", "resource": "maker", "period": "P2", "hours": "1.99"})
        self.assertEqual(evaluate(plan)["dependencies"][0]["status"], "conflict")

    def test_uncovered_predecessor_blocks_allocated_successor(self):
        plan = fixture()
        plan["allocations"][0]["hours"] = "1"
        result = evaluate(plan)
        self.assertEqual(result["summary"]["uncovered_work_items"], ["first"])
        self.assertIsNone(result["work_items"][0]["planned_completion_period"])
        self.assertEqual(result["dependencies"][0]["status"], "conflict")

    def test_no_allocations_exposes_work_instead_of_certifying_plan(self):
        plan = fixture()
        plan["allocations"] = []
        result = evaluate(plan)
        self.assertEqual(result["assessment"], "conflicts_found")
        self.assertEqual(result["summary"]["uncovered_work_items"], ["first", "next"])
        self.assertEqual(result["dependencies"][0]["status"], "not_scheduled")

    def test_unknown_capacity_keeps_known_load_and_null_headroom(self):
        plan = fixture()
        plan["resources"][0]["available_hours"]["P1"] = None
        result = evaluate(plan)
        self.assertEqual(result["result"], "incomplete")
        self.assertEqual(result["assessment"], "unknown")
        self.assertEqual(result["resource_periods"][0]["planned_hours"], Decimal("2"))
        self.assertIsNone(result["resource_periods"][0]["overload_hours"])

    def test_unknown_effort_makes_completion_and_dependency_unknown(self):
        plan = fixture()
        plan["work_items"][0]["required_hours"]["maker"] = None
        result = evaluate(plan)
        self.assertEqual(result["work_items"][0]["effort_status"], "unknown")
        self.assertIsNone(result["work_items"][0]["planned_completion_period"])
        self.assertEqual(result["dependencies"][0]["status"], "unknown")

    def test_known_conflict_survives_other_unknown_inputs(self):
        plan = fixture()
        plan["work_items"][0]["required_hours"]["maker"] = None
        plan["allocations"][1]["hours"] = "0.5"
        result = evaluate(plan)
        self.assertEqual(result["result"], "incomplete")
        self.assertEqual(result["assessment"], "conflicts_found")
        self.assertEqual(result["work_items"][0]["due_status"], "missed")
        self.assertEqual(result["dependencies"][0]["status"], "conflict")

    def test_order_is_supplied_not_alphabetic(self):
        plan = fixture()
        plan["periods"] = ["P3", "P1", "P2"]
        plan["work_items"][0]["due_period"] = "P3"
        self.assertEqual(evaluate(plan)["work_items"][0]["due_status"], "missed")

    def test_missing_period_and_duplicate_allocations_fail(self):
        for change in [lambda p: p["resources"][0]["available_hours"].pop("P3"),
                       lambda p: p["allocations"].append(dict(p["allocations"][0])),
                       lambda p: p["periods"].append("p1")]:
            plan = fixture()
            change(plan)
            with self.assertRaises(ValueError):
                evaluate(plan)

    def test_cycles_missing_edges_and_unrequired_resources_fail(self):
        for change in [lambda p: p["work_items"][0]["depends_on"].append("next"),
                       lambda p: p["work_items"][0]["depends_on"].append("absent"),
                       lambda p: p["work_items"][0]["depends_on"].append("first"),
                       lambda p: p["work_items"][1]["depends_on"].append("first"),
                       lambda p: p["allocations"][2].update(resource="checker")]:
            plan = fixture()
            change(plan)
            with self.assertRaises(ValueError):
                evaluate(plan)

    def test_invalid_hours_are_not_coerced(self):
        for value in [0, True, "-1", "NaN", "1e2", "0.0000001", "1000000000000", " 1", "01", {}, []]:
            plan = fixture()
            plan["resources"][0]["available_hours"]["P1"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                evaluate(plan)
        for value in [None, "0"]:
            plan = fixture()
            plan["allocations"][0]["hours"] = value
            with self.assertRaises(ValueError):
                evaluate(plan)

    def test_strict_schema_and_reference_types_fail_cleanly(self):
        for change in [lambda p: p.update(schema_version=True), lambda p: p.update(unknown=1),
                       lambda p: p["work_items"][0].update(due_period=[]),
                       lambda p: p["allocations"][0].update(period={}),
                       lambda p: p["work_items"][0].update(owner="\n"),
                       lambda p: p["resources"].append(p["resources"][0])]:
            plan = fixture()
            change(plan)
            with self.assertRaises(ValueError):
                evaluate(plan)
        with self.assertRaises(ValueError):
            parse_plan(b'{"schema_version":1,"schema_version":1}')
        with self.assertRaises(ValueError):
            parse_plan(b"[" * 2000 + b"]" * 2000)

    def test_limits_are_enforced(self):
        for field, value in [("periods", ["P"] * 121), ("resources", [{}] * 51),
                             ("work_items", [{}] * 501), ("allocations", [{}] * 20001)]:
            plan = fixture()
            plan[field] = value
            with self.assertRaises(ValueError):
                evaluate(plan)

    def test_file_hash_read_only_cli_and_exit_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "plan.json"
            plan = fixture()
            for code, expected in [(0, "complete"), (2, "incomplete"), (1, "error")]:
                if code == 2:
                    plan["resources"][0]["available_hours"]["P1"] = None
                elif code == 1:
                    plan["schema_version"] = 9
                data = json.dumps(plan).encode()
                path.write_bytes(data)
                run = subprocess.run([sys.executable, "-B", str(ROOT / "Blitz/setup/company.py"), "capacity", str(path)],
                                     text=True, capture_output=True)
                self.assertEqual(run.returncode, code, run.stderr + run.stdout)
                self.assertEqual(json.loads(run.stdout)["result"], expected)
                self.assertEqual(path.read_bytes(), data)
                if code == 0:
                    self.assertEqual(assess(path)["input_sha256"], hashlib.sha256(data).hexdigest())

    def test_packaged_example_identifies_overload_and_late_delivery(self):
        result = assess(ROOT / "Blitz/examples/company/delivery-plan.json")
        self.assertEqual(result["bottlenecks"][0]["overload_hours"], Decimal("3"))
        self.assertEqual(result["summary"]["missed_due_work_items"], ["delivery"])
        self.assertEqual(result["summary"]["dependency_conflicts"], 0)


if __name__ == "__main__":
    unittest.main()
