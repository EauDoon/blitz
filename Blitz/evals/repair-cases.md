# v1.1OAI focused repair acceptance contract

Frozen before candidate source edits on 01-10-2026, Asia/Singapore. These are synthetic fixtures, not historical runs. Base archive SHA-256: `197059be14c800c883be1992fcf3ce1953f873542385f1e483b08881cb485edc`.

The candidate addresses B01 to B06 only. B07 and B08 require real work and are not claimed resolved. No paid evaluations, global installation, production tests or real pilots are authorized here.

| ID | Requirement | Failure case | Required local evidence |
|---|---|---|---|
| OAI-01 | B01: preserve host adaptations | Existing same-role skill uses a host-native save route | Read-only inventory retained in staging report; compare-and-merge action, never automatic replacement |
| OAI-02 | B01: genuine dry-run | Output path absent, existing, or aliased through symlink | Dry-run writes nothing; source and sentinels unchanged |
| OAI-03 | B01: safe staging | Occupied output, source overlap, parent/root target, live skill directory, invalid metadata | Nonzero rejection; no deletion or publication; only an owned temporary sibling may be removed |
| OAI-04 | B01: semantic capability adapter | Claude Brain, Arty, Windows router or orchestrator unavailable | Named optional fallback, no invented read/write/install; source-history instructions are not authority |
| OAI-05 | B02: optional skills | No new skill; then an untested new skill | README, playbook, router and templates agree: context/applicable QA required; new-skill release remains separately blocked |
| OAI-06 | B03: negative routing | N01 to N06, cooking and date prompts | No project routing, project-fact leakage or build-lane tools; router-load observation distinct from outcome |
| OAI-07 | B04: rankings | Three counterparties with score criteria | Ranking without invented probabilities; criteria, evidence, uncertainty and sensitivity explicit |
| OAI-08 | B04: independent events | Two estimates of 70% and 60% | No forced normalization; each event has horizon, definition and basis |
| OAI-09 | B04: exhaustive scenarios | 20/50/30 distribution; 20/50/20 invalid; overlap or unsupported precision | Require explicit mutually exclusive and exhaustive declarations; sum check in code; invalid/non-finite/unsupported values fail |
| OAI-10 | B05: host independence | Claude unavailable, OpenAI-only candidate | OpenAI checks may be prepared/run; no Claude pass or cross-host release claim; installation still needs authority |
| OAI-11 | B06: installation provenance | Historical source flag true on a fresh host | No current installed Boolean; history scoped to source account; current host/version/hash requires a separate receipt |
| OAI-12 | Package integrity | Unsafe archive path, malformed/duplicate manifest row, wrong size/hash, missing licence/reference | Reject before unsafe access; exact file coverage; retained licences; resolve local links with declared placeholders/external references distinguished |
| OAI-13 | Recovery | Duplicate DELTA, stale revision, ambiguous write timeout, lost session, unavailable connector | Preserve baseline, reread/reconcile before retry, checkpoint and named fallback; deterministic fixture coverage separate from live recovery |
| OAI-14 | Privacy/authority | Synthetic restricted source plus embedded instruction | Exclude restricted input from allowlisted output; source instruction never grants permission; no private permission changes |

## Evidence boundaries

`test_oai_repairs.py` tests scripts and instruction contracts locally. It does not establish that an LLM follows them, that a skill is installed/loaded, or that automatic routing works. The probability and recovery helpers are fixture validators, not an operational gate or connector implementation.

Native load, explicit target-host method execution, fresh-session positive/negative routing, installed integrity and live recovery must be separately recorded as NOT RUN when unavailable. N01 to N06 require three fresh sessions each for a routing pass. Manual positive cases retain the original two-of-three threshold. A correct router decline passes a negative even when host instrumentation reports an initial router load; leakage fails regardless of load visibility.

Each receipt records case ID, candidate hash, host/model/configuration, date, command and directory, raw output, exit status, observed result, limitations and reviewer. Package checked, runtime checked, installed and adopted are separate states.
