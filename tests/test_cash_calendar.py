"""Synthetic event timing, exact cash arithmetic and malformed calendar regressions."""
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
from cash_calendar import parse_calendar, calculate_calendar, assess


class CashCalendarTests(unittest.TestCase):
    def setUp(self):
        self.path = ROOT / "Blitz/examples/company/service-cash-calendar.json"
        self.raw = json.loads(self.path.read_text())

    def calculate(self):
        data = json.dumps(self.raw).encode()
        return calculate_calendar(parse_calendar(data), hashlib.sha256(data).hexdigest())

    def test_positive_month_close_does_not_hide_intraday_shortfall(self):
        report = self.calculate()
        summary = report["summary"]
        self.assertEqual(summary["ending_cash"], Decimal("500"))
        self.assertEqual(summary["minimum_cash"], Decimal("-200"))
        self.assertEqual(summary["additional_opening_cash_to_preserve_floor"], Decimal("300"))
        self.assertEqual(report["days_with_events"][0]["closing_cash"], Decimal("600"))
        self.assertEqual(report["days_with_events"][0]["minimum_cash"], Decimal("-200"))
        self.assertEqual(summary["first_observed_below_reserve"]["event_id"], "synthetic-supplier-payment")

    def test_explicit_order_not_array_order_controls_settlement(self):
        baseline = self.calculate()
        self.raw["events"].reverse()
        self.assertEqual(self.calculate()["summary"], baseline["summary"])
        for event in self.raw["events"]:
            if event["date"] == "2026-10-05": event["sequence"] = 3 - event["sequence"]
        self.assertEqual(self.calculate()["summary"]["minimum_cash"], Decimal("300"))

    def test_unknown_amount_propagates_and_never_implies_no_breach(self):
        self.raw["events"][0]["amount"] = None
        report = self.calculate()
        self.assertEqual(report["result"], "incomplete")
        self.assertIsNone(report["summary"]["ending_cash"])
        self.assertIsNone(report["summary"]["minimum_cash"])
        self.assertIsNone(report["summary"]["negative_balance_within_horizon"])
        self.assertIsNone(report["summary"]["additional_opening_cash_to_preserve_floor"])
        self.assertTrue(all(event["balance_after"] is None for event in report["events"]))

    def test_known_breach_before_unknown_is_retained(self):
        self.raw["events"][1]["amount"] = None
        summary = self.calculate()["summary"]
        self.assertTrue(summary["negative_balance_within_horizon"])
        self.assertIsNone(summary["minimum_cash"])

    def test_opening_breach_counts_without_events(self):
        self.raw.update(opening_cash="-20", events=[])
        summary = self.calculate()["summary"]
        self.assertEqual(summary["first_observed_negative_balance"]["phase"], "opening")
        self.assertEqual(summary["additional_opening_cash_to_preserve_floor"], Decimal("120"))
        self.assertEqual(summary["minimum_cash"], Decimal("-20"))

    def test_unknown_floor_does_not_hide_known_cash(self):
        self.raw["reserve_floor"] = None
        report = self.calculate()
        self.assertEqual(report["result"], "incomplete")
        self.assertEqual(report["summary"]["ending_cash"], Decimal("500"))
        self.assertIsNone(report["summary"]["below_reserve_within_horizon"])

    def test_missing_opening_cash_remains_unknown(self):
        self.raw["opening_cash"] = None
        report = self.calculate()
        self.assertFalse(report["summary"]["cash_balances_complete"])
        self.assertIsNone(report["summary"]["ending_cash"])

    def test_exact_decimal_arithmetic(self):
        self.raw.update(opening_cash="0.1", reserve_floor="0")
        self.raw["events"] = [{"id": "e", "date": "2026-10-01", "sequence": 1, "direction": "in", "amount": "0.2"}]
        self.assertEqual(self.calculate()["summary"]["ending_cash"], Decimal("0.3"))

    def test_input_is_immutable_and_hashed(self):
        before = self.path.read_bytes()
        parsed = parse_calendar(before)
        copy_before = copy.deepcopy(parsed)
        calculate_calendar(parsed, "fixture")
        self.assertEqual(parsed, copy_before)
        self.assertEqual(assess(self.path)["input_sha256"], hashlib.sha256(before).hexdigest())
        self.assertEqual(self.path.read_bytes(), before)

    def test_duplicate_ids_or_ambiguous_order_rejected(self):
        for field, value in (("id", self.raw["events"][0]["id"].upper()), ("sequence", 1)):
            with self.subTest(field=field):
                obj = copy.deepcopy(self.raw)
                obj["events"][1][field] = value
                with self.assertRaises(ValueError): parse_calendar(json.dumps(obj).encode())

    def test_invalid_dates_and_out_of_horizon_rejected(self):
        for value in ("2026-02-30", "2026-11-01", "20261005", "2026-W40-1", None):
            with self.subTest(value=value):
                self.raw["events"][0]["date"] = value
                with self.assertRaises(ValueError): self.calculate()

    def test_numbers_must_be_nonnegative_bounded_decimal_strings(self):
        for value in ("-1", "NaN", "1e3", 10, True, "", "1.0000001", "1000000000000000000"):
            with self.subTest(value=value):
                self.raw["events"][0]["amount"] = value
                with self.assertRaises(ValueError): self.calculate()

    def test_duplicate_json_keys_and_unknown_fields_rejected(self):
        with self.assertRaises(ValueError): parse_calendar(b'{"schema_version":1,"schema_version":1}')
        self.raw["events"][0]["currency"] = "EUR"
        with self.assertRaises(ValueError): self.calculate()

    def test_cli_complete_incomplete_and_error(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "calendar.json"
            for value, expected in (("500", 0), (None, 2), ("NaN", 1)):
                self.raw["events"][0]["amount"] = value
                source.write_text(json.dumps(self.raw))
                result = subprocess.run([sys.executable, "-B", str(ROOT / "Blitz/setup/company.py"),
                                         "calendar", str(source)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertEqual(json.loads(result.stdout)["result"], {0:"complete", 2:"incomplete", 1:"error"}[expected])


if __name__ == "__main__": unittest.main()
