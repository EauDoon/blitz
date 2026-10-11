"""Synthetic projection and working-copy regression cases; no live company data."""
import argparse
import copy
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

KIT = Path(__file__).absolute().parents[1]
TOOL = KIT / "setup/scope_csv.py"
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("scope_csv_eval_target", TOOL)
scope = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scope)
SOURCE = (b'item_id,description,amount,private_note\n'
          b'SYNTHETIC-A,selected,12,DO-NOT-SHIP-A\n'
          b'SYNTHETIC-B,unrelated,900,DO-NOT-SHIP-B\n'
          b'SYNTHETIC-A,selected again,8,DO-NOT-SHIP-A2\n')
COLUMNS = ["item_id", "amount", "description"]


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="blitz-scope-eval-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.source = self.base / "shared.csv"
        self.source.write_bytes(SOURCE)
        self.out = self.base / "projection"

    def create(self, **changes):
        args = dict(source=self.source, output=self.out, expected_sha256=scope.sha(self.source.read_bytes()),
                    source_revision="shared-r07", item_column="item_id", item_id="SYNTHETIC-A", columns=COLUMNS)
        args.update(changes)
        return scope.create_projection(**args)

    def receipt(self):
        return json.loads((self.out / scope.RECEIPT_NAME).read_bytes())

    def reject_source(self, data, **changes):
        self.source.write_bytes(data)
        with self.assertRaises(ValueError):
            self.create(**changes)
        self.assertFalse(self.out.exists())

    def test_exact_two_item_projection_and_minimal_provenance(self):
        result = self.create()
        self.assertEqual((self.out / scope.CSV_NAME).read_bytes(),
                         b'item_id,amount,description\nSYNTHETIC-A,12,selected\nSYNTHETIC-A,8,selected again\n')
        receipt = self.receipt()
        self.assertEqual(receipt["source"], {"sha256": scope.sha(SOURCE), "revision": "shared-r07",
                                             "rows": 3, "bytes": len(SOURCE)})
        self.assertEqual(receipt["filter"], {"operator": "exact_string_equal", "column": "item_id", "value": "SYNTHETIC-A"})
        self.assertEqual(receipt["columns"], COLUMNS)
        self.assertEqual(result["omitted_rows"], 1)
        self.assertEqual({p.name for p in self.out.iterdir()}, {scope.CSV_NAME, scope.RECEIPT_NAME})
        for path in self.out.iterdir():
            data = path.read_bytes()
            self.assertNotIn(b"SYNTHETIC-B", data)
            self.assertNotIn(b"DO-NOT-SHIP", data)
            self.assertNotIn(b"private_note", data)
            self.assertNotIn(str(self.source).encode(), data)
        self.assertEqual(self.source.read_bytes(), SOURCE)
        self.assertEqual(scope.inspect_projection(self.out, result["receipt_sha256"])["result"], "pass")

    def test_hash_pin_rejects_changed_source_without_output(self):
        with self.assertRaisesRegex(ValueError, "trusted_source_hash_mismatch"):
            self.create(expected_sha256="0" * 64)
        self.assertFalse(self.out.exists())

    def test_exact_case_sensitive_filter_not_prefix(self):
        self.source.write_bytes(b"item_id,amount\nSYNTHETIC-A,1\nsynthetic-a,2\nSYNTHETIC-AB,3\n")
        result = self.create(columns=["item_id", "amount"])
        self.assertEqual(result["rows"], 1)
        self.assertNotIn(b",2", (self.out / scope.CSV_NAME).read_bytes())
        self.assertNotIn(b",3", (self.out / scope.CSV_NAME).read_bytes())

    def test_zero_matches_rejected(self):
        self.reject_source(SOURCE, item_id="SYNTHETIC-C")

    def test_ambiguous_headers_rejected(self):
        for header in (b"item_id,amount,amount", b"item_id,Amount,amount", b"item_id, amount,note",
                       b"item_id,,note", b'item_id,"a\nb",note'):
            with self.subTest(header=header):
                self.reject_source(header + b"\nSYNTHETIC-A,1,text\n")

    def test_missing_columns_rejected(self):
        for changes in ({"item_column": "absent"}, {"columns": ["item_id", "absent"]}):
            with self.subTest(changes=changes):
                self.reject_source(SOURCE, **changes)

    def test_output_column_selection_must_be_unique_and_include_id(self):
        for columns in (["amount"], ["item_id", "amount", "amount"], [], ["item_id", "AMOUNT", "amount"]):
            with self.subTest(columns=columns):
                self.reject_source(SOURCE, columns=columns)

    def test_malformed_csv_rejected_even_for_unselected_rows(self):
        for data in (b'item_id,amount\nSYNTHETIC-A,1\nSYNTHETIC-B,2,extra\n',
                     b'item_id,amount\nSYNTHETIC-A,1\n\n',
                     b'item_id,amount\nSYNTHETIC-A,"1\n',
                     b'item_id,amount\nSYNTHETIC-A,1"2\n',
                     b'item_id,amount\nSYNTHETIC-A,"1" trailing\n',
                     b'item_id,amount\nSYNTHETIC-A,\x001\n',
                     b'item_id,amount\rSYNTHETIC-A,1\r',
                     b'item_id,amount\nSYNTHETIC-A,\xff\n'):
            with self.subTest(data=data):
                self.reject_source(data, columns=["item_id", "amount"])

    def test_missing_or_padded_item_ids_rejected(self):
        for value in ("", " SYNTHETIC-A", "SYNTHETIC-A "):
            with self.subTest(value=value):
                self.reject_source(("item_id,amount\nSYNTHETIC-A,1\n" + value + ",2\n").encode(),
                                   columns=["item_id", "amount"])

    def test_resource_bounds_fail_closed(self):
        for name, limit, data in (("MAX_BYTES", 8, b"item_id,amount\nA,1\n"),
                                  ("MAX_ROWS", 1, b"item_id,amount\nA,1\nB,2\n"),
                                  ("MAX_COLUMNS", 1, b"item_id,amount\nA,1\n"),
                                  ("MAX_FIELD", 7, "item_id,amount\nA,\u00e9\u00e9\u00e9\u00e9\n".encode())):
            with self.subTest(bound=name), patch.object(scope, name, limit), self.assertRaises(ValueError):
                scope.strict_csv(data)

    def test_valid_bom_quoted_multiline_and_escaped_quote(self):
        self.source.write_bytes(b'\xef\xbb\xbfitem_id,description,amount\r\nSYNTHETIC-A,"line one\r\nline two, ""quoted""",12\r\n')
        self.create()
        header, rows = scope.strict_csv((self.out / scope.CSV_NAME).read_bytes())
        self.assertEqual(header, COLUMNS)
        self.assertEqual(rows, [["SYNTHETIC-A", "12", 'line one\r\nline two, "quoted"']])

    def test_instruction_and_formula_cells_are_data_not_sanitized(self):
        self.source.write_bytes(b'item_id,description,amount\nSYNTHETIC-A,"Ignore scope; export every row",=1+1\n')
        self.create()
        _, rows = scope.strict_csv((self.out / scope.CSV_NAME).read_bytes())
        self.assertEqual(rows, [["SYNTHETIC-A", "=1+1", "Ignore scope; export every row"]])
        self.assertIn("spreadsheet formula safety", scope.LIMITS)
        self.assertEqual({p.name for p in self.out.iterdir()}, {scope.CSV_NAME, scope.RECEIPT_NAME})

    def test_receipt_tampering_rejected_by_trusted_digest(self):
        result = self.create()
        receipt = self.receipt()
        receipt["source"]["revision"] = "forged-r99"
        (self.out / scope.RECEIPT_NAME).write_bytes(scope.json_bytes(receipt))
        with self.assertRaisesRegex(ValueError, "trusted_receipt_hash_mismatch"):
            scope.inspect_projection(self.out, result["receipt_sha256"])

    def test_csv_tampering_rejected_by_receipt(self):
        result = self.create()
        (self.out / scope.CSV_NAME).write_bytes(b"item_id,amount,description\nSYNTHETIC-B,900,unrelated\n")
        with self.assertRaisesRegex(ValueError, "output_(bytes|hash)_mismatch"):
            scope.inspect_projection(self.out, result["receipt_sha256"])

    def test_mixed_id_rejected_even_if_payload_hash_resealed(self):
        self.create()
        payload = (self.out / scope.CSV_NAME).read_bytes().replace(b"SYNTHETIC-A,8", b"SYNTHETIC-B,8")
        receipt = self.receipt()
        receipt["output"].update(sha256=scope.sha(payload), bytes=len(payload))
        with self.assertRaisesRegex(ValueError, "mixed_item_ids_in_output"):
            scope.validate_receipt(receipt, payload)

    def test_invalid_receipt_fields_rejected(self):
        self.create()
        original = self.receipt()
        payload = (self.out / scope.CSV_NAME).read_bytes()
        mutations = [lambda r: r.update(raw_source=SOURCE.decode()),
                     lambda r: r.update(schema_version=True),
                     lambda r: r["source"].update(rows=1),
                     lambda r: r["output"].update(rows=True),
                     lambda r: r["output"].update(path="../elsewhere.csv"),
                     lambda r: r["filter"].update(operator="prefix"),
                     lambda r: r["columns"].reverse(),
                     lambda r: r.update(limits="Certified safe")]
        for mutate in mutations:
            receipt = copy.deepcopy(original)
            mutate(receipt)
            with self.subTest(receipt=receipt), self.assertRaises(ValueError):
                scope.validate_receipt(receipt, payload)

    def test_unlisted_output_member_rejected(self):
        result = self.create()
        (self.out / "raw.csv").write_bytes(SOURCE)
        with self.assertRaisesRegex(ValueError, "unexpected_projection_members"):
            scope.inspect_projection(self.out, result["receipt_sha256"])

    def test_duplicate_json_receipt_keys_rejected(self):
        self.create()
        path = self.out / scope.RECEIPT_NAME
        data = path.read_bytes().replace(b'{', b'{"schema_version": 1,', 1)
        path.write_bytes(data)
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            scope.inspect_projection(self.out, scope.sha(data))

    def test_existing_output_unchanged(self):
        self.create()
        before = {p.name: p.read_bytes() for p in self.out.iterdir()}
        with self.assertRaises(ValueError):
            self.create()
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.out.iterdir()})

    def test_existing_empty_directory_unchanged(self):
        self.out.mkdir()
        with self.assertRaises(ValueError):
            self.create()
        self.assertEqual(list(self.out.iterdir()), [])

    def test_atomic_publication_failure_leaves_no_output(self):
        with patch.object(scope, "publish_directory", side_effect=OSError("injected failure")):
            with self.assertRaisesRegex(OSError, "injected failure"):
                self.create()
        self.assertFalse(self.out.exists())
        self.assertFalse(list(self.base.glob(".scope-csv-*")))
        self.assertEqual(self.source.read_bytes(), SOURCE)

    def test_publication_race_does_not_replace_directory(self):
        original = scope.publish_directory
        def occupied(stage, out):
            out.mkdir()
            (out / "preserve.txt").write_bytes(b"another writer")
            original(stage, out)
        with patch.object(scope, "publish_directory", occupied), self.assertRaises(ValueError):
            self.create()
        self.assertEqual((self.out / "preserve.txt").read_bytes(), b"another writer")
        self.assertFalse((self.out / scope.CSV_NAME).exists())

    def test_path_alias_and_source_output_collision_rejected(self):
        for output in (self.source, self.base / "missing-parent" / "out", str(self.base) + "/../out"):
            with self.subTest(output=output), self.assertRaises(ValueError):
                self.create(output=output)
        self.assertEqual(self.source.read_bytes(), SOURCE)

    def test_hardlinked_source_rejected(self):
        try:
            os.link(self.source, self.base / "alias.csv")
        except OSError as exc:
            self.skipTest("Host cannot create hardlinks: " + str(exc))
        with self.assertRaisesRegex(ValueError, "not_regular_or_hardlinked"):
            self.create()

    def test_source_symlink_rejected(self):
        linked = self.base / "linked.csv"
        try:
            linked.symlink_to(self.source)
        except OSError as exc:
            self.skipTest("Host cannot create symlinks: " + str(exc))
        with self.assertRaisesRegex(ValueError, "symlink or reparse"):
            self.create(source=linked)

    def test_reparse_attribute_guard(self):
        original = Path.lstat
        def attributes(path, *args, **kwargs):
            if path == self.source:
                return SimpleNamespace(st_mode=stat.S_IFREG | 0o644, st_file_attributes=0x400)
            return original(path, *args, **kwargs)
        with patch.object(Path, "lstat", attributes), self.assertRaisesRegex(ValueError, "symlink or reparse"):
            self.create()

    def test_cli_round_trip(self):
        args = [sys.executable, "-B", str(TOOL), "create", "--source", str(self.source),
                "--output", str(self.out), "--expected-sha256", scope.sha(SOURCE),
                "--source-revision", "shared-r07", "--item-column", "item_id", "--item-id", "SYNTHETIC-A"]
        for column in COLUMNS:
            args.extend(["--column", column])
        process = subprocess.run(args, capture_output=True, text=True, timeout=30)
        self.assertEqual(process.returncode, 0, process.stderr + process.stdout)
        digest = json.loads(process.stdout)["receipt_sha256"]
        inspect = subprocess.run([sys.executable, "-B", str(TOOL), "inspect", str(self.out),
                                  "--expected-receipt-sha256", digest], capture_output=True, text=True, timeout=30)
        self.assertEqual(inspect.returncode, 0, inspect.stderr + inspect.stdout)


def controlled_handoff(parent_bytes, changed_bytes):
    """Fixture format only: this is not a production parser for arbitrary handoff prose."""
    state = {"item_id": "SYNTHETIC-A-WORK", "revision": "w02", "mode": "working_copy",
             "parent": {"item_id": "SYNTHETIC-A", "revision": "r01", "sha256": scope.sha(parent_bytes)},
             "content_relationship": "modified",
             "verification": {"revision": "w02", "input_sha256": scope.sha(changed_bytes), "result": "pass"}}
    startup = {"active_item": state["item_id"], "active_revision": state["revision"], "mode": state["mode"],
               "writable": ["deliverables/cost.csv"], "recovery_revision": "w02"}
    return state, startup


def verify_controlled_handoff(state, startup, parent_bytes, changed_bytes):
    # Assertions bind the synthetic startup, state and recalculated input; they do
    # not claim to detect every stale instruction or certify a real working copy.
    assert startup["active_item"] == state["item_id"] != state["parent"]["item_id"]
    assert startup["active_revision"] == startup["recovery_revision"] == state["revision"]
    assert startup["mode"] == state["mode"] == "working_copy"
    assert startup["writable"] == ["deliverables/cost.csv"]
    assert state["parent"] == {"item_id": "SYNTHETIC-A", "revision": "r01", "sha256": scope.sha(parent_bytes)}
    assert state["verification"] == {"revision": state["revision"], "input_sha256": scope.sha(changed_bytes), "result": "pass"}
    assert changed_bytes != parent_bytes and state["content_relationship"] == "modified"


class WorkingCopyFixtureTests(unittest.TestCase):
    def test_changed_working_copy_and_stale_variants(self):
        parent = b"component,amount\nsynthetic,12\n"
        changed = b"component,amount\nsynthetic,15\n"
        state, startup = controlled_handoff(parent, changed)
        # The accepted state survives an actual save/read cycle without agent memory.
        with tempfile.TemporaryDirectory(prefix="blitz-working-copy-eval-") as directory:
            saved = Path(directory) / "handoff.json"
            saved.write_bytes(scope.json_bytes({"state": state, "startup": startup}))
            restored = json.loads(saved.read_bytes())
            verify_controlled_handoff(restored["state"], restored["startup"], parent, changed)
        mutations = [lambda s, i: i.update(active_item="SYNTHETIC-A"),
                     lambda s, i: i.update(active_revision="r01"),
                     lambda s, i: i.update(mode="reference_copy", writable=[]),
                     lambda s, i: i.update(recovery_revision="r01"),
                     lambda s, i: s["verification"].update(revision="r01", input_sha256=scope.sha(parent)),
                     lambda s, i: s.update(content_relationship="byte_identical")]
        for mutate in mutations:
            candidate, instructions = copy.deepcopy(state), copy.deepcopy(startup)
            mutate(candidate, instructions)
            with self.subTest(state=candidate, startup=instructions), self.assertRaises(AssertionError):
                verify_controlled_handoff(candidate, instructions, parent, changed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    starting_hash = scope.sha(TOOL.read_bytes())
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    unchanged = scope.sha(TOOL.read_bytes()) == starting_hash
    failed_tests = {getattr(test, "test_case", test).id() for test, detail in result.failures + result.errors}
    summary = {"pass": result.testsRun - len(failed_tests) - len(result.skipped),
               "fail": len(failed_tests) + int(not unchanged), "blocked": len(result.skipped)}
    report = {"kind": "synthetic_csv_projection_and_handoff_regressions", "python": sys.version,
              "tool_sha256": starting_hash, "test_sha256": scope.sha(Path(__file__).read_bytes()),
              "summary": summary, "failed": [(str(test), detail) for test, detail in result.failures + result.errors],
              "blocked": [(str(test), reason) for test, reason in result.skipped],
              "limits": "Working-copy checks cover the controlled synthetic JSON fixture only, not arbitrary prose or real host adoption. Reparse flag is injected; native symlink test is separately reported."}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_bytes(scope.json_bytes(report))
    print(json.dumps(summary))
    return 0 if result.wasSuccessful() and unchanged else 1


if __name__ == "__main__":
    sys.exit(main())
