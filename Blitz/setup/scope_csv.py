#!/usr/bin/env python3
"""Project one exact item from a reviewed CSV into a new directory, never execute it."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import sys
import tempfile
import unicodedata

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).absolute().parent))
from verify_archive import (guard_local_path, load_json, publish_directory,
                            require, validate_destination)

MAX_BYTES = 64 * 1024 * 1024
MAX_ROWS = 250000
MAX_COLUMNS = 256
MAX_FIELD = 1024 * 1024
FORMAT = "blitz-item-csv-projection"
CSV_NAME = "projected.csv"
RECEIPT_NAME = "provenance.json"
LIMITS = ("Exact row and column projection plus integrity only. Source revision is a "
          "caller assertion. No permission, semantic isolation, secret-free, spreadsheet "
          "formula safety, or working-copy readiness certification. Treat all cells as data.")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def hash_field(value):
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value), "invalid_sha256")


def label(value):
    require(isinstance(value, str) and bool(value) and value == value.strip()
            and not re.search(r"[\x00-\x1f\x7f]", value)
            and unicodedata.normalize("NFC", value) == value, "invalid_label")


def columns_field(columns):
    require(isinstance(columns, list) and 1 <= len(columns) <= MAX_COLUMNS, "invalid_columns")
    for value in columns:
        label(value)
    require(len({value.casefold() for value in columns}) == len(columns), "duplicate_columns")


def read_file(raw):
    path = guard_local_path(raw)
    info = path.stat()
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "not_regular_or_hardlinked")
    require(info.st_size <= MAX_BYTES, "oversize_file")
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    require(len(data) <= MAX_BYTES, "oversize_file")
    return path, data


def strict_csv(data):
    """Fixed UTF-8 comma/double-quote dialect, rejecting permissive CSV ambiguities."""
    require(len(data) <= MAX_BYTES, "oversize_csv")
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("csv_not_utf8") from exc
    require(not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\ufeff]", text), "csv_control_character")
    require(not re.search(r"\r(?!\n)", text), "csv_bare_cr")
    # csv.reader(strict=True) still accepts quotes inside unquoted fields.
    # Validate lexical quoting first, with no row values in error messages.
    state = "start"
    for character in text:
        if state == "quoted":
            if character == '"':
                state = "closed"
        elif state == "closed":
            if character == '"':
                state = "quoted"
            elif character == ",":
                state = "start"
            elif character in "\r\n":
                state = "start"
            else:
                raise ValueError("csv_characters_after_quote")
        elif character == '"':
            require(state == "start", "csv_quote_in_unquoted_field")
            state = "quoted"
        elif character in ",\r\n":
            state = "start"
        else:
            state = "unquoted"
    require(state != "quoted", "csv_unclosed_quote")
    previous_limit = csv.field_size_limit()
    try:
        csv.field_size_limit(MAX_FIELD)
        rows = []
        for row in csv.reader(io.StringIO(text, newline=""), strict=True):
            require(len(rows) <= MAX_ROWS, "too_many_rows")
            require(1 <= len(row) <= MAX_COLUMNS, "invalid_row_width")
            require(all(len(value.encode("utf-8")) <= MAX_FIELD for value in row), "oversize_field")
            rows.append(row)
    except csv.Error as exc:
        raise ValueError("malformed_csv") from exc
    finally:
        csv.field_size_limit(previous_limit)
    require(bool(rows), "missing_header")
    columns_field(rows[0])
    require(all(len(row) == len(rows[0]) for row in rows[1:]), "ragged_csv")
    return rows[0], rows[1:]


def project(data, item_column, item_id, columns):
    label(item_column)
    label(item_id)
    columns_field(columns)
    require(item_column in columns, "item_column_required_in_output")
    header, rows = strict_csv(data)
    require(item_column in header and all(name in header for name in columns), "missing_column")
    id_index = header.index(item_column)
    for row in rows:
        label(row[id_index])
    indices = [header.index(name) for name in columns]
    selected = [[row[index] for index in indices] for row in rows if row[id_index] == item_id]
    require(bool(selected), "no_matching_rows")
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(columns)
    writer.writerows(selected)
    payload = output.getvalue().encode("utf-8")
    require(len(payload) <= MAX_BYTES, "oversize_projection")
    return payload, len(rows), len(selected)


def validate_receipt(receipt, payload):
    require(isinstance(receipt, dict) and set(receipt) == {
        "schema_version", "format", "source", "filter", "columns", "output", "limits"}, "invalid_receipt")
    require(type(receipt["schema_version"]) is int and receipt["schema_version"] == 1
            and receipt["format"] == FORMAT and receipt["limits"] == LIMITS, "invalid_receipt_format")
    source, selected, output = receipt["source"], receipt["filter"], receipt["output"]
    require(isinstance(source, dict) and set(source) == {"sha256", "revision", "bytes", "rows"}, "invalid_source_receipt")
    hash_field(source["sha256"])
    label(source["revision"])
    require(type(source["bytes"]) is int and 0 < source["bytes"] <= MAX_BYTES, "invalid_source_bytes")
    require(type(source["rows"]) is int and 1 <= source["rows"] <= MAX_ROWS, "invalid_source_rows")
    require(isinstance(selected, dict) and set(selected) == {"operator", "column", "value"}
            and selected["operator"] == "exact_string_equal", "invalid_filter")
    label(selected["column"])
    label(selected["value"])
    columns_field(receipt["columns"])
    require(selected["column"] in receipt["columns"], "item_column_required_in_output")
    require(isinstance(output, dict) and set(output) == {"path", "sha256", "bytes", "rows"}
            and output["path"] == CSV_NAME, "invalid_output_receipt")
    hash_field(output["sha256"])
    require(type(output["bytes"]) is int and output["bytes"] == len(payload), "output_bytes_mismatch")
    require(output["sha256"] == sha(payload), "output_hash_mismatch")
    header, rows = strict_csv(payload)
    require(header == receipt["columns"], "output_columns_mismatch")
    require(type(output["rows"]) is int and 1 <= output["rows"] <= source["rows"]
            and output["rows"] == len(rows), "output_rows_mismatch")
    index = header.index(selected["column"])
    require(all(row[index] == selected["value"] for row in rows), "mixed_item_ids_in_output")


def inspect_projection(directory, expected_receipt_sha256):
    hash_field(expected_receipt_sha256)
    root = guard_local_path(directory)
    require(root.is_dir(), "projection_not_directory")
    require({path.name for path in root.iterdir()} == {CSV_NAME, RECEIPT_NAME}, "unexpected_projection_members")
    _, receipt_data = read_file(root / RECEIPT_NAME)
    require(sha(receipt_data) == expected_receipt_sha256, "trusted_receipt_hash_mismatch")
    _, payload = read_file(root / CSV_NAME)
    receipt = load_json(receipt_data)
    validate_receipt(receipt, payload)
    return {"result": "pass", "receipt_sha256": sha(receipt_data),
            "output_sha256": sha(payload), "rows": receipt["output"]["rows"], "limits": LIMITS}


def create_projection(source, output, expected_sha256, source_revision, item_column, item_id, columns):
    hash_field(expected_sha256)
    label(source_revision)
    source_path, data = read_file(source)
    require(sha(data) == expected_sha256, "trusted_source_hash_mismatch")
    out = validate_destination(output)
    require(not source_path.is_relative_to(out) and not out.is_relative_to(source_path), "source_output_overlap")
    payload, source_rows, output_rows = project(data, item_column, item_id, columns)
    receipt = {"schema_version": 1, "format": FORMAT,
               "source": {"sha256": expected_sha256, "revision": source_revision,
                          "bytes": len(data), "rows": source_rows},
               "filter": {"operator": "exact_string_equal", "column": item_column, "value": item_id},
               "columns": columns, "output": {"path": CSV_NAME, "sha256": sha(payload),
                                               "bytes": len(payload), "rows": output_rows},
               "limits": LIMITS}
    receipt_data = json_bytes(receipt)
    # The output name becomes visible only after both complete files are checked.
    with tempfile.TemporaryDirectory(prefix=".scope-csv-", dir=out.parent) as temporary:
        stage = Path(temporary) / "projection"
        stage.mkdir()
        (stage / CSV_NAME).write_bytes(payload)
        (stage / RECEIPT_NAME).write_bytes(receipt_data)
        result = inspect_projection(stage, sha(receipt_data))
        publish_directory(stage, out)
    return dict(result, source_rows=source_rows, omitted_rows=source_rows - output_rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create", help="prepare a reviewed item projection")
    for field in ("source", "output", "expected-sha256", "source-revision", "item-column", "item-id"):
        create.add_argument("--" + field, required=True)
    create.add_argument("--column", action="append", required=True, dest="columns")
    inspect = commands.add_parser("inspect", help="check projection against a separately trusted receipt hash")
    inspect.add_argument("directory")
    inspect.add_argument("--expected-receipt-sha256", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "create":
            result = create_projection(args.source, args.output, args.expected_sha256,
                                       args.source_revision, args.item_column, args.item_id, args.columns)
        else:
            result = inspect_projection(args.directory, args.expected_receipt_sha256)
    except (OSError, ValueError, UnicodeError) as exc:
        result = {"result": "fail", "error": str(exc), "limits": LIMITS}
    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
