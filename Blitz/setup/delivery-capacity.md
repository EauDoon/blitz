# Assess delivery capacity

Use the local `capacity` command before agreeing the next delivery cycle. It checks a supplied plan across shared people, teams or equipment, including internal departments that do not use the commercial cash schema:

```sh
python -B Blitz/setup/company.py capacity Blitz/examples/company/delivery-plan.json
```

The synthetic example plans 11 analyst hours against 8 available in Week 2, and finishes delivery effort in Week 3 against a Week 2 due period. The report identifies both conflicts, the work contributing to each overloaded period, and the dependency checks. It preserves the supplied plan and emits JSON on standard output. It does not assign work, change a calendar, adopt a budget or authorize a commitment.

Copy the [example](../examples/company/delivery-plan.json) outside reusable source. Keep evidence for available hours, effort estimates, due periods and authority in the existing brief or resource records. This optional file is a calculation input, not an additional required company record. No currency or budget approval belongs in its hour fields.

## Schema version 1

The top-level object requires exactly `schema_version`, `periods`, `resources`, `work_items` and `allocations`. Unknown fields and duplicate JSON keys are errors. Files use UTF-8, at most 2 MiB, and the same guarded local-file reader as the cash command.

| Field | Contract |
|---|---|
| `schema_version` | Integer `1` |
| `periods` | 1 to 120 unique labels, in chronological order as supplied; the command does not infer dates or sort labels |
| `resources` | 1 to 50 objects with unique `id`, descriptive `name`, and `available_hours` |
| `available_hours` | One entry for every period; a nonnegative decimal string or `null` when unknown |
| `work_items` | 1 to 500 objects with unique `id`, `name`, `owner`, `due_period`, `depends_on` and `required_hours` |
| `due_period` | One supplied period, interpreted as its end |
| `depends_on` | List of predecessor work item IDs; no duplicates, missing references or cycles |
| `required_hours` | Map of one or more resource IDs to positive decimal strings or `null` when unknown; omit resources the work does not require |
| `allocations` | Up to 20,000 objects with `work_item`, `resource`, `period` and positive decimal-string `hours`; at most one entry for each work/resource/period combination |

IDs are lowercase ASCII letters followed by lowercase letters, digits, underscores or hyphens, at most 64 characters. Names, owners and period labels use the existing 1 to 200 character label rules. Hour strings have at most 12 integer and 6 fractional digits; JSON numbers, booleans, exponent notation, negative values and nonfinite values are rejected. All sums and differences use exact decimal arithmetic. `0` is known zero availability; `null` is missing evidence. An allocation must refer to a resource required by that work item. Empty allocations are permitted and expose uncovered work.

Supply availability **net of obligations outside this plan**. Include support, rework and other shared obligations as work items when they consume this plan's capacity. Do not subtract them from availability as well. Use one stable resource ID for the same constrained pool; creating separate IDs for the same person would conceal a bottleneck. Hours cannot move between resources or periods. An equipment resource can use operating hours; all amounts for that resource must describe the same capacity unit.

## Read the report

`resource_periods` gives available and planned hours, signed headroom and overload for every resource/period. `bottlenecks` lists known overloads with contributing work. Unknown availability produces null headroom and overload; a complete-looking total never substitutes zero for it.

Each work item lists required, planned, planned-by-due, uncovered and excess hours for each resource. `planned_completion_period` is the first period by whose end cumulative allocations cover every known requirement; it is null if any requirement is unknown or uncovered. It is conditional on delivering those hours, including when the report separately finds an overload or dependency conflict. Excess allocations still consume capacity, but do not increase the supplied effort requirement. They may indicate that effort estimates need revision.

`due_status` is `missed` if any known requirement is not covered by the due period, `unknown` if unknown effort prevents a conclusion, and otherwise `within_due_period`. A known miss remains visible even if another requirement is unknown. These statuses concern planned hours, not actual delivery or acceptance.

Dependencies are finish-to-start at period boundaries: **all allocations** for dependent work must begin in a period strictly after its predecessor's planned completion. A same-period handoff is a conflict because its timing is not evidenced at this resolution. Uncovered predecessor work is a conflict when dependent work has allocations; unknown predecessor effort yields an unknown dependency check. A dependent work item with no allocations is `not_scheduled`, and its uncovered effort is reported separately. A satisfied edge does not override another constraint or certify the predecessor's delivery.

`assessment` is `conflicts_found` whenever there is a known overload, uncovered effort, missed due period or dependency conflict. Otherwise it is `unknown` when inputs are missing, or `within_supplied_limits` when the supplied plan satisfies these checks. This last result is not a readiness gate, acceptance decision or proof of operational feasibility: intraperiod concurrency, indivisible shifts, external dependencies, quality and actual execution remain outside the model. This command checks a plan; it does not optimize or infer that no alternative schedule exists.

`result` describes input completeness separately from conflicts. Exit **0** means all inputs are known, including when conflicts exist; exit **2** means one or more inputs are unknown; exit **1** means invalid input. Inspect `assessment`, not only the process exit code, before reviewing a commitment. `input_sha256` binds the report to the exact input bytes. Retain the report with the source revision and resolve conflicts in the owner's records; the command never changes them.
