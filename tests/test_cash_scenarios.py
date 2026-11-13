"""Synthetic cash stress regressions, including timing and missing evidence."""
import copy
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Blitz/setup"))
from cash_scenarios import compare, parse_scenarios
from company import COLUMNS, calculate_rows, parse_rows


class CashScenarioTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "cash.csv"
        self.source.write_bytes((ROOT / "Blitz/examples/company/service-cash.csv").read_bytes())
        self.spec = self.root / "scenarios.json"

    def run_scenario(self, scenario):
        self.spec.write_text(json.dumps({"schema_version": 1, "scenarios": [scenario]}))
        before = self.source.read_bytes()
        result = compare(self.source, self.spec)
        self.assertEqual(self.source.read_bytes(), before)
        self.assertEqual(result["input_sha256"], hashlib.sha256(before).hexdigest())
        return result

    def edit_rows(self, edit):
        with self.source.open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        edit(rows)
        with self.source.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    def test_identity_matches_baseline_and_keeps_rows_immutable(self):
        result = self.run_scenario({"name": "Unchanged"})
        self.assertEqual(result["scenarios"][0]["summary"], result["baseline_summary"])
        rows = parse_rows(self.source.read_bytes())
        before = copy.deepcopy(rows)
        calculate_rows(rows, "synthetic")
        self.assertEqual(rows, before)

    def test_delay_conserves_receipts_and_exposes_reserve_shortfall(self):
        case = self.run_scenario({"name": "Late", "receipt_delay_periods": 1})["scenarios"][0]
        self.assertEqual(str(case["receipts_deferred_beyond_horizon"]), "1200")
        self.assertEqual(str(case["summary"]["ending_cash"]), "1316")
        self.assertEqual(str(case["summary"]["maximum_closing_reserve_gap"]), "184")
        self.assertEqual(str(case["ending_cash_difference_from_baseline"]), "-1200")
        self.assertEqual(case["summary"]["first_observed_closing_below_reserve_period"], "Period 1")

    def test_delay_beyond_horizon_preserves_all_deferred_receipts(self):
        case = self.run_scenario({"name": "Later", "receipt_delay_periods": 1200})["scenarios"][0]
        self.assertEqual(str(case["receipts_deferred_beyond_horizon"]), "1800")
        self.assertEqual(str(case["ending_cash_difference_from_baseline"]), "-1800")

    def test_cost_stress_does_not_change_contribution(self):
        result = self.run_scenario({"name": "Cost", "cash_cost_multiplier": "1.2"})
        case = result["scenarios"][0]
        self.assertLess(case["summary"]["ending_cash"], result["baseline_summary"]["ending_cash"])
        self.assertEqual([p["contribution"] for p in case["forecast"]["periods"]],
                         [p["contribution"] for p in result["baseline"]["periods"]])

    def test_unknown_receipts_remain_unknown_even_with_zero_factor(self):
        self.edit_rows(lambda rows: rows[0].update(cash_receipts=""))
        result = self.run_scenario({"name": "Unknown", "receipts_multiplier": "0"})
        self.assertEqual(result["result"], "incomplete")
        self.assertIsNone(result["scenarios"][0]["summary"]["minimum_closing_cash"])

    def test_unknown_deferred_receipts_are_not_reported_as_zero(self):
        self.edit_rows(lambda rows: rows[-1].update(cash_receipts=""))
        result = self.run_scenario({"name": "Unknown late", "receipt_delay_periods": 1})
        self.assertIsNone(result["scenarios"][0]["receipts_deferred_beyond_horizon"])

    def test_invalid_specs_fail_closed(self):
        cases = [
            {"name": "Bad", "receipts_multiplier": 1},
            {"name": "Bad", "receipts_multiplier": "NaN"},
            {"name": "Bad", "cash_cost_multiplier": "10.1"},
            {"name": "Bad", "receipt_delay_periods": True},
            {"name": "Bad", "receipt_delay_periods": -1},
            {"name": "Bad", "receipt_delay_periods": 1201},
            {"name": "Bad", "reciepts_multiplier": "1"},
        ]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                parse_scenarios(json.dumps({"schema_version": 1, "scenarios": [case]}).encode())
        with self.assertRaises(ValueError):
            parse_scenarios(b'{"schema_version":1,"schema_version":1,"scenarios":[]}')

    def test_cli_and_invalid_continuity(self):
        self.run_scenario({"name": "CLI"})
        result = subprocess.run([sys.executable, "-B", str(ROOT / "Blitz/setup/company.py"),
                                 "stress", str(self.source), "--scenarios", str(self.spec)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)["result"], "complete")
        self.edit_rows(lambda rows: rows[1].update(opening_cash="1"))
        with self.assertRaisesRegex(ValueError, "opening_cash differs"):
            compare(self.source, self.spec)


if __name__ == "__main__":
    unittest.main()
