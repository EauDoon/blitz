# Event-level cash calendar

Use this read-only calculator when an invoice is due before a collection, even
though the period-end forecast looks adequate. It complements `company.py cash`
and `stress`: those commands deliberately inspect closing balances only.

```sh
python -B Blitz/setup/company.py calendar Blitz/examples/company/service-cash-calendar.json
```

The synthetic example opens at USD 300. A USD 500 supplier payment occurs before
a same-day USD 800 collection. The lowest balance is **USD -200**, despite a
USD 600 day close and USD 500 month close. Preserving the supplied USD 100 floor
would require **USD 300 additional opening cash** under that exact schedule.
This is arithmetic on fictional assumptions, not a recommendation or financing.

## Input contract

Use a UTF-8 JSON object with exactly these fields:

| Field | Meaning |
|---|---|
| `schema_version` | Integer `1` |
| `currency` | One uppercase three-letter code; no currency conversion |
| `start_date`, `end_date` | Inclusive `YYYY-MM-DD` horizon, at most 3661 days |
| `opening_cash` | Decimal string before all start-date events; may be negative; `null` if unknown |
| `reserve_floor` | Nonnegative decimal string, or `null` if unknown |
| `events` | At most 10000 entries, including an explicitly empty schedule |

Each event has exactly `id`, `date`, `sequence`, `direction` and `amount`.
IDs are nonempty and unique ignoring case. Dates must fall within the horizon.
`sequence` is an integer from 0 to 10000; each `(date, sequence)` pair is unique.
`direction` is `in` or `out`; amount is a nonnegative decimal string or `null`.
Numbers support up to 18 integer and 6 fractional digits. JSON numbers, NaN,
exponents, duplicate keys, extra fields and ambiguous same-date ordering fail.
The entire file is limited to 2 MiB and uses the standard local path guards.

Events are sorted by date and declared sequence, regardless of input array order.
Supply an order supported by evidence, or compare separate possible schedules.
The tool does not guess time zones, banking cutoffs or which payment settles first.
Amounts remain exact decimals. Cash receipts are cash movements, not revenue.

## Reading the report

The report binds the raw input SHA-256, lists event balances, and groups event-day
opening, inflow, outflow, closing and minimum balances. The minimum includes the
initial opening balance and every post-event balance. Days without events retain
the previous balance and do not need table rows.

The summary shows the first observed negative or below-floor balance and the
maximum floor shortfall, expressed as additional opening cash needed to preserve
that floor across the declared schedule. A first breach can be at opening, where
`event_id` is `null` and `phase` is `opening`.

An unknown amount makes its balance and every later balance unknown. Unknown
opening cash has the same effect. Whole-horizon minimum/funding figures then
remain `null`; a breach observed before the gap remains visible. An unknown
reserve leaves cash arithmetic available but reserve checks unknown. Empty events
mean the supplied schedule is empty, not that the tool has proved there are no
obligations. `complete` means all supplied amounts are known, never that the
schedule captures every actual receipt, obligation, fee or tax.

Exit `0` means complete arithmetic, including known shortfalls; `2` means unknown
inputs; `1` means invalid input or a read failure. Output goes to stdout. No file
is saved or adopted, no money moves, and no operating authority is granted.
