# Compare cash scenarios

Use the local `stress` command to inspect collections timing and cash-cost assumptions before making the next commitment:

```sh
python -B Blitz/setup/company.py stress Blitz/examples/company/service-cash.csv --scenarios Blitz/examples/company/cash-scenarios.json
```

The JSON report includes the original forecast, each scenario's complete period calculations, ending-cash differences, receipts deferred beyond the horizon, and the largest closing reserve gap. Input files remain unchanged. Nothing is saved, adopted, sent or funded by this command.

Copy the synthetic scenario file outside the kit and state assumptions with your own evidence. Schema version 1 accepts 1 to 25 uniquely named scenarios. Each may set `receipts_multiplier` and `cash_cost_multiplier` as decimal strings from `0` to `10` (up to six decimal places), and `receipt_delay_periods` as an integer from 0 to 1200. Omitted multipliers are `1`; omitted delay is `0`. Unknown fields and duplicate JSON keys fail rather than silently ignoring a typo.

Receipt delays shift the entire supplied schedule by that many periods, with zero receipts before the shifted schedule begins. Receipts falling after the last period are reported separately, not discarded or added to ending cash. The model assumes no collections arriving from before the supplied horizon. The cost multiplier changes variable, fixed and one-off cash costs. It leaves revenue recognition, contribution, delivery capacity, refunds, financing and tax assumptions unchanged; this is a cash stress test, not a full operating-model simulation.

The baseline first validates any supplied opening balances against prior closing balances. Scenarios retain the first opening balance and recalculate every later one, replacing later supplied anchors. Missing amounts remain unknown, even under a zero multiplier. A missing amount shifted outside the horizon can still make deferred receipts unknown. Complete minimum cash and maximum gap statistics require every relevant period to be known.

Exit codes match `cash`: 0 for complete calculations (including shortfalls), 2 for incomplete inputs, and 1 for invalid inputs. A reserve gap is measured at period close; intraperiod financing needs may be larger. Results do not assign probabilities or establish business readiness.
