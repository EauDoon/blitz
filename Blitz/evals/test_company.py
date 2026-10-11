"""Focused founder CLI checks using synthetic inputs and temporary directories.

These verify arithmetic and filesystem behavior, never company effectiveness.
"""
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

KIT = Path(__file__).absolute().parents[1]
SCRIPT = KIT / "setup" / "company.py"
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("blitz_company_eval", SCRIPT)
company = importlib.util.module_from_spec(spec)
spec.loader.exec_module(company)


def row(period="Period 1", **changes):
    values = dict.fromkeys(company.COLUMNS, "0")
    values.update(period=period, currency="USD", opening_cash="1000",
                  cash_receipts="200", variable_cash_costs="100", fixed_cash_costs="50",
                  reserve_floor="100", units_delivered="2", earned_revenue="300",
                  variable_delivery_cost="120", founder_delivery_hours="4", available_delivery_hours="8")
    values.update(changes)
    return values


class CompanyChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="blitz-company-eval-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def cli(self, *args):
        process = subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)],
                                 capture_output=True, text=True, encoding="utf-8", timeout=20,
                                 env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1"))
        self.assertFalse(process.stderr, process.stderr)
        return process.returncode, json.loads(process.stdout)

    def cash(self, rows, header=None):
        path = self.base / "cash.csv"
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=header or company.COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        return self.cli("cash", path)

    def test_init_new_draft_and_exact_receipt(self):
        output = self.base / "company"
        code, receipt = self.cli("init", "--out", output, "--name", "Synthetic & Co", "--owner", "Test Owner")
        self.assertEqual(code, 0)
        self.assertEqual(receipt["result"], "created_draft")
        self.assertEqual(receipt["readiness"], "unassessed")
        self.assertFalse(receipt["adopted_position"])
        expected = {"README.md", "company-brief.md", "company-cash.csv", "context/00 Read Me First.md",
                    "context/03 Position Of Record.md", "context/09 Open Questions.md", "context/10 Decision Log.md"}
        self.assertEqual({p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}, expected)
        for record in receipt["files"]:
            content = (output / record["path"]).read_bytes()
            self.assertEqual(len(content), record["bytes"])
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["sha256"])
        self.assertIn("UNADOPTED", (output / "context/03 Position Of Record.md").read_text(encoding="utf-8"))
        self.assertIn("Synthetic &amp; Co", (output / "company-brief.md").read_text(encoding="utf-8"))
        self.assertEqual((output / "company-cash.csv").read_bytes(), (KIT / "templates/company-cash.csv").read_bytes())
        cash_code, cash = self.cli("cash", output / "company-cash.csv")
        self.assertEqual(cash_code, 2)
        self.assertEqual(cash["result"], "incomplete")
        self.assertIsNone(cash["periods"][0]["closing_cash"])

    def test_existing_file_and_directory_are_untouched(self):
        for kind in ("file", "directory"):
            with self.subTest(kind=kind):
                output = self.base / kind
                if kind == "file":
                    output.write_text("keep", encoding="utf-8")
                    sentinel = output
                else:
                    output.mkdir()
                    sentinel = output / "keep.txt"
                    sentinel.write_text("keep", encoding="utf-8")
                code, result = self.cli("init", "--out", output, "--name", "Synthetic", "--owner", "Owner")
                self.assertEqual(code, 1)
                self.assertIn("occupied", str(result))
                self.assertEqual(sentinel.read_text(), "keep")

    def test_empty_existing_directory_is_not_replaced(self):
        output = self.base / "empty"
        output.mkdir()
        code, _ = self.cli("init", "--out", output, "--name", "Synthetic", "--owner", "Owner")
        self.assertEqual(code, 1)
        self.assertEqual(list(output.iterdir()), [])

    def test_source_overlap_rejected(self):
        output = KIT / "company-eval-must-not-exist"
        self.assertFalse(output.exists())
        code, result = self.cli("init", "--out", output, "--name", "Synthetic", "--owner", "Owner")
        self.assertEqual(code, 1)
        self.assertIn("overlap", str(result))
        self.assertFalse(output.exists())

    def test_unsafe_output_paths(self):
        targets = [str(self.base / "NUL"), str(self.base / "bad."), str(self.base / "bad:stream"),
                   str(self.base) + "/../escape", str(self.base) + "/./alias", "//server/share/out"]
        for target in targets:
            with self.subTest(target=target):
                code, _ = self.cli("init", "--out", target, "--name", "Synthetic", "--owner", "Owner")
                self.assertEqual(code, 1)
        self.assertEqual(list(self.base.iterdir()), [])

    def test_live_metadata_and_baseline_paths_rejected(self):
        for name in (".git", ".codex", ".baseline", "skills"):
            with self.subTest(name=name):
                parent = self.base / name
                parent.mkdir()
                code, _ = self.cli("init", "--out", parent / "new", "--name", "Synthetic", "--owner", "Owner")
                self.assertEqual(code, 1)
                self.assertEqual(list(parent.iterdir()), [])

    def test_invalid_name_does_not_create_files(self):
        for name in ("", " padded ", "new\nline", "x\u202ey", "x" * 201):
            with self.subTest(name=name):
                code, _ = self.cli("init", "--out", self.base / "new", "--name", name, "--owner", "Owner")
                self.assertEqual(code, 1)
        self.assertEqual(list(self.base.iterdir()), [])

    def test_publication_failure_cleans_only_own_stage(self):
        sentinel = self.base / "sentinel.txt"
        sentinel.write_text("keep", encoding="utf-8")
        with patch.object(company, "publish_directory", side_effect=OSError("injected publication failure")):
            with self.assertRaisesRegex(OSError, "injected"):
                company.initialize(self.base / "new", "Synthetic", "Owner")
        self.assertEqual(list(self.base.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_text(), "keep")

    def test_destination_appearing_at_publication_is_preserved(self):
        original = company.publish_directory
        output = self.base / "new"
        def race(stage, out):
            out.mkdir()
            (out / "competitor.txt").write_text("keep", encoding="utf-8")
            return original(stage, out)
        with patch.object(company, "publish_directory", side_effect=race):
            with self.assertRaisesRegex(ValueError, "occupied"):
                company.initialize(output, "Synthetic", "Owner")
        self.assertEqual([p.name for p in output.iterdir()], ["competitor.txt"])
        self.assertEqual((output / "competitor.txt").read_text(), "keep")
        self.assertEqual(list(self.base.iterdir()), [output])

    def test_reparse_ancestor_rejected_without_native_symlink_privilege(self):
        original = Path.lstat
        def reparse(path, *args, **kwargs):
            info = original(path, *args, **kwargs)
            if path == self.base:
                return SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400)
            return info
        with patch.object(Path, "lstat", reparse):
            with self.assertRaisesRegex(ValueError, "symlink or reparse"):
                company.initialize(self.base / "new", "Synthetic", "Owner")
        self.assertEqual(list(self.base.iterdir()), [])

    def test_delayed_collections_and_exact_cash_arithmetic(self):
        code, result = self.cash([
            row(cash_receipts="0", refunds_cash_out="25", financing_cash_in="100",
                financing_cash_out="20", tax_cash="10", one_off_cash_costs="15"),
            row("Period 2", opening_cash="", cash_receipts="500", earned_revenue="0"),
        ])
        self.assertEqual(code, 0)
        first, second = result["periods"]
        self.assertEqual(first["closing_cash"], "880")
        self.assertEqual(second["opening_cash"], "880")
        self.assertEqual(second["opening_source"], "prior_computed_closing")
        self.assertEqual(second["closing_cash"], "1230")
        self.assertEqual(first["contribution"], "180")
        self.assertEqual(first["contribution_per_unit"], "90.000000")
        self.assertEqual(first["founder_utilization"], "0.500000")
        self.assertEqual(first["capacity_units_at_same_delivery_rate"], "4.000000")
        self.assertEqual(result["evidence_status"], "calculated_from_supplied_unverified_inputs")
        self.assertEqual(result["runway_beyond_horizon"], "not_estimated")

    def test_decimal_precision_no_binary_float_drift(self):
        code, result = self.cash([row(opening_cash="0.1", cash_receipts="0.2", variable_cash_costs="0", fixed_cash_costs="0")])
        self.assertEqual(code, 0)
        self.assertEqual(result["periods"][0]["closing_cash"], "0.3")

    def test_unknowns_propagate_and_do_not_become_zero(self):
        code, result = self.cash([row(cash_receipts=""), row("Period 2", opening_cash="")])
        self.assertEqual(code, 2)
        self.assertIsNone(result["periods"][0]["closing_cash"])
        self.assertIsNone(result["periods"][1]["opening_cash"])
        self.assertIsNone(result["periods"][1]["closing_cash"])
        self.assertIsNone(result["negative_closing_within_horizon"])
        self.assertIsNone(result["closing_below_reserve_within_horizon"])
        self.assertIn("cash_receipts", result["periods"][0]["unknown_fields"])
        self.assertFalse(result["cash_observations_complete"])

    def test_unknown_currency_is_incomplete(self):
        code, result = self.cash([row(currency="")])
        self.assertEqual(code, 2)
        self.assertIsNone(result["currency"])
        self.assertIsNone(result["periods"][0]["closing_cash"])
        self.assertIsNone(result["periods"][0]["contribution"])

    def test_new_anchor_after_unknown_continuity_is_disclosed(self):
        code, result = self.cash([row(cash_receipts=""), row("Period 2", opening_cash="750")])
        self.assertEqual(code, 2)
        self.assertEqual(result["periods"][1]["closing_cash"], "800")
        self.assertIn("continuity is unknown", str(result["periods"][1]["warnings"]))

    def test_conflicting_opening_cash_rejected(self):
        code, result = self.cash([row(), row("Period 2", opening_cash="999")])
        self.assertEqual(code, 1)
        self.assertIn("differs from prior", str(result))

    def test_negative_cash_and_capacity_breach_are_visible(self):
        code, result = self.cash([row(opening_cash="-20", cash_receipts="0", available_delivery_hours="2")])
        self.assertEqual(code, 0)
        self.assertEqual(result["periods"][0]["closing_cash"], "-170")
        self.assertTrue(result["negative_closing_within_horizon"])
        self.assertTrue(result["closing_below_reserve_within_horizon"])
        self.assertIn("exceed available", str(result["periods"][0]["warnings"]))
        self.assertIn("negative opening", str(result["periods"][0]["warnings"]))

    def test_reserve_summary_is_close_only_and_opening_warning_remains(self):
        code, result = self.cash([row(opening_cash="0", cash_receipts="200", variable_cash_costs="0", fixed_cash_costs="0")])
        self.assertEqual(code, 0)
        self.assertFalse(result["closing_below_reserve_within_horizon"])
        self.assertIn("opening cash is below", str(result["periods"][0]["warnings"]))
        self.assertIn("intraperiod", result["limits"])

    def test_breach_after_unknown_is_first_observed_only(self):
        code, result = self.cash([row(cash_receipts=""), row("Period 2", opening_cash="0", cash_receipts="0")])
        self.assertEqual(code, 2)
        self.assertEqual(result["first_observed_negative_closing_period"], "Period 2")
        self.assertEqual(result["first_observed_closing_below_reserve_period"], "Period 2")
        self.assertTrue(result["closing_below_reserve_within_horizon"])

    def test_zero_ratios_never_become_infinity(self):
        code, result = self.cash([row(units_delivered="0", available_delivery_hours="0", founder_delivery_hours="0")])
        self.assertEqual(code, 0)
        period = result["periods"][0]
        for field in ("contribution_per_unit", "founder_utilization", "delivery_hours_per_unit", "capacity_units_at_same_delivery_rate"):
            self.assertIsNone(period[field])
        self.assertIn("undefined", str(period["warnings"]))

    def test_negative_net_earned_revenue_can_represent_refunds(self):
        code, result = self.cash([row(earned_revenue="-30")])
        self.assertEqual(code, 0)
        self.assertEqual(result["periods"][0]["contribution"], "-150")
        self.assertIn("negative contribution", str(result["periods"][0]["warnings"]))

    def test_nonfinite_oversized_or_malformed_numbers_rejected(self):
        for value in ("NaN", "Infinity", "-Infinity", "1e999", "1,000", "9999999999999999999", "0.0000001", "--1"):
            with self.subTest(value=value):
                code, result = self.cash([row(cash_receipts=value)])
                self.assertEqual(code, 1)
                self.assertIn("finite decimal", str(result))

    def test_negative_magnitude_inputs_rejected(self):
        for field in set(company.COLUMNS[2:]) - {"opening_cash", "earned_revenue"}:
            with self.subTest(field=field):
                code, result = self.cash([row(**{field: "-1"})])
                self.assertEqual(code, 1)
                self.assertIn("nonnegative", str(result))

    def test_mixed_currency_duplicate_period_and_bad_currency_rejected(self):
        for rows in ([row(), row("Period 2", currency="SGD")], [row(), row("PERIOD 1")], [row(currency="usd")]):
            with self.subTest(rows=rows):
                code, _ = self.cash(rows)
                self.assertEqual(code, 1)

    def test_empty_missing_extra_or_duplicate_header_rejected(self):
        path = self.base / "cash.csv"
        for content in ("", ",".join(company.COLUMNS) + "\n", "period,currency\nPeriod 1,USD\n",
                        ",".join(company.COLUMNS + ("currency",)) + "\n", ",".join(company.COLUMNS) + "\nPeriod 1,USD\n"):
            with self.subTest(content=content):
                path.write_text(content, encoding="utf-8")
                code, _ = self.cli("cash", path)
                self.assertEqual(code, 1)

    def test_utf8_bom_and_reordered_complete_header_supported(self):
        path = self.base / "cash.csv"
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=list(reversed(company.COLUMNS)))
        writer.writeheader()
        writer.writerow(row())
        path.write_bytes(stream.getvalue().encode("utf-8-sig"))
        code, result = self.cli("cash", path)
        self.assertEqual(code, 0)
        self.assertEqual(result["periods"][0]["closing_cash"], "1050")

    def test_bounded_input_bytes_and_periods(self):
        path = self.base / "cash.csv"
        path.write_bytes(b"x" * (company.MAX_INPUT_BYTES + 1))
        code, result = self.cli("cash", path)
        self.assertEqual(code, 1)
        self.assertIn("2 MiB", str(result))
        code, result = self.cash([row(str(i), opening_cash="") for i in range(company.MAX_PERIODS + 1)])
        self.assertEqual(code, 1)
        self.assertIn("1200 periods", str(result))


if __name__ == "__main__":
    unittest.main(verbosity=2)
