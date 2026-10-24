# Customer-discovery scoring corrections, v2

Use this scorer revision with the [100 frozen v1 tasks](../customer-discovery/README.md). The original corpus, references, controls and freeze receipt remain unchanged. Three reference ambiguities are corrected in [corrections.json](corrections.json): first monthly billing timing, purchasing authority versus payer identity, and pre-payment versus post-payment cash headroom.

The two numeric alternatives require the accompanying semantic explanation. Accepting a numeric value alone cannot establish a pass. All 100 substantive review criteria and the original business/authority constraints remain required.

From the repository root, prepare an output directory outside the source kit whose parent already exists:

```sh
python -B tests/evals/customer-discovery-scoring-v2/prepare.py --out .verification/customer-discovery-evaluator-v2
```

The command verifies the original frozen payload, refuses an occupied destination, copies it and applies only the declared reference/scorer corrections. It retains the original freeze as lineage and emits a fresh evaluator inventory. It neither generates target responses nor changes the 100 task inputs.

Validate the prepared package with the eval-workflow offline helper when available. Regrade preserved actual outputs under a new scoring run, recording their original generation conditions; this is not a fresh target execution or evidence of improved model behavior. Required natural-language review remains a separate evidence-backed assessment. Do not expose answer keys, controls or previous outputs to task-solving executors. Native generation, arithmetic checks, semantic review and host installation remain separate claims.
