# Example run: Harbourline (synthetic)

Harbourline is invented. It is a cross-border invoice financing service for small exporters. Every name, figure and time below is sample data made for this kit. The example shows the shape of a Blitz run on the 72-hour clock, not advice about any real venture.

## The clock

T0: 06-10-2026 9:00 AM SGT, the founders' written brief. First contact: 03-10-2026 4:30 PM SGT, a call.

| Mark | Target | Actual | Note |
|---|---|---|---|
| Setup done | T+1h | T+0h 45m | Instructions read back; tail matched on the second paste |
| Ingestion gate | T+8h | T+7h 10m | Hold: no bank evidence for the stated capital |
| Firming gate | T+24h | T+26h 30m | Missed by 2h 30m; the founder call moved. Reported, not reset |
| Mandate pack accepted | T+48h | T+47h 40m | One pager, scope with 24 requirement IDs, rough model, 3 GTM hypotheses, 1 experiment card |
| Blitzing gate | T+60h | T+58h | Instructions refreshed; no project skill built (no repeated task yet) |
| Delivering rehearsal | T+72h | T+70h 20m | One request end to end; recovery drill RC01 passed in 6 min |

## Ingestion (T+0h to T+7h 10m)

* 11 sources registered. S04, a 30-page deck, has pages 21 and 22 missing; the gap is in the source register.
* 19 claims extracted. Two are load bearing: the capital figure and the lending licence.
* Gate record in file 10:

```text
06-10-2026 4:10 PM | gate | Ingestion gate: Hold. Reason: capital claim (C03) has no bank evidence; lending licence (C07) cites a register entry that does not match the entity name. May continue: diligence, call card, bounded decision memo, rough model (PROPOSED). Releases it: bank letter for C03; register extract for C07, requested in writing 06-10-2026 4:20 PM. Decision owner: founder A. | S02, S05
```

## Firming (T+7h to T+26h 30m)

* Call card: three goals tied to C03, C07 and the first market.
* Capture: recording on, storage named, speaker labels checked the same day.
* Debrief from the transcript 50 min after the call.
* Position of record v1 in file 03, confirmed by founder A at T+26h 30m.

## Mandate (T+26h to T+47h 40m)

Commission briefs for four outputs, each from file 03 v1. The one pager went through doc-style and cold-read LITE (7 findings, all fixed). The model ran in calc-workbook; gauntlet-verify Light caught a financing fee applied twice.

## Blitzing (T+40h to T+58h)

A founder message at T+41h moved the first market. That is a revision: file 03 v2, with the change-impact register listing the one pager, requirements 3 to 7 and the model as stale. All three were refreshed by T+52h.

## Delivering (T+58h to T+70h 20m)

One request ran end to end: a partner brief from intake to canonical save and handoff. Recovery drill RC01: a Drive upload timed out; the session checked for the file before retrying and found it saved.

## Stage card at T+30h

```text
Blitz: Economics at Mandate, T+30h on the 72-hour pilot clock (behind by 2h 30m).
Gate: Proceed conditionally: fee rate assumed at 1.2% until the partner quote arrives (E04).
Next: rough model with calc-workbook, then gauntlet-verify Light. Skipped: viz-dashboards, no chart asked.
```

## A DELTA from a second session

```text
DELTA H-S2-004
Expected revision: 09 Open Questions, last update 07-10-2026 11:05 AM
Target: 09 Open Questions, section B
Change: add "B3 | Does the partner bank's licence cover receivables bought from another country? | Bank letter; counsel note | Founder A | OPEN"
Evidence: S09, transcript 07-10-2026, minute 14
Affects: requirements FN-02 and FN-03; the one pager, section 3
```

## For comparison: the first pilot (September 2026)

Stage durations and failure classes only. The run built mandate work before Firming, opened its project at T+81h and reached its position of record at T+152h, against the 72-hour target. The failure classes it recorded are the source of the kit's rules: two hosts holding two scopes, mandate before Firming, a late project, skills built on a moving position, parallel write races, document churn, untested skill routing, cut-off instructions, blurred state words, and recent saves carrying an old scope.
