# FxC3Buckets — cohort partition and all-faulty strict-red attack

Target: `.ufo/waves/round-22/candidate/tools/check-review-cohort.py`
Declared digest: `34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0` (accepted as assigned; not recomputed because this seat is NO-EXEC).
Mode: source-only reads of declared paths. No execution, no imports, no fetches, no production edits. Expected fixture verdicts below are read from source; **observed runtime is empty** (no fixture was executed).

## Predicate decomposition

The attack names two testable conjuncts:

- **P1 partition:** `delivered_conformant + delivered_faulty + absent_dead + absent_unresolved == total == accounted`, with one per-seat row per declared declaration.
- **P2 all-faulty stays strict-red:** a cohort whose seats are all faulty never presents as a strict pass.

## Observed source facts

- `counts` starts at zero for exactly the four bucket names: `check-review-cohort.py:26`.
- One loop over `reviews` (`:52`) computes exactly one `category` (`:58-61`), increments exactly that bucket (`:62`), and appends exactly one row (`:63-65`). There is no `continue`, `break`, or conditional skip in the loop.
- `total` is `len(reviews)` and `accounted` is `sum(counts.values())` in the same result object (`:71-72`).
- Settlement must have one unique agent per seat, valid outcomes, and errors consistent with outcomes (`:42-47`), and its name set must equal the manifest name set (`:50-51`).
- The strict evaluator rejects an empty review list, duplicate names, and duplicate report paths before accounting (`check-review-snapshots.py:63-66,78-80`).
- Per-seat strict evaluation rebuilds a one-review manifest from the same row (`:56-57`) and buckets on `one_code` (`:58-61`).
- Aggregate strict verdict is `1` for findings, `2` for read/encoding errors, else `0` (`check-review-snapshots.py:121`).
- Cohort exit is `2 if strict_code == 2 else (1 if findings else 0)` (`:70`). `findings` receives only `COHORT-UNRESOLVED` for any `absent_unresolved` (`:66-67`) and `COHORT-STRICT-UNAVAILABLE` for strict exit `2` (`:68-69`).
- `strict_conformance` is computed independently from `strict_code` (`:73`), while top-level `status` is derived from `code` (`:79`).

## P1 — holds by construction (bounded reason)

After schema validation, the loop executes exactly once per review, and each iteration performs exactly one bucket increment and one row append. No path inside the loop continues or skips. Floats/duplicates cannot distort the sum because `total` and `accounted` are computed from the same `reviews` list, and duplicate names are rejected by the strict schema before the loop is reached. Settlement set-equality makes the settlement population identical to the manifest population, so `len(seats) == total == accounted`.

Exceptions do not produce a partial partition: any exception in the loop leaves through `:75-78`, where the payload contains `COHORT-SCHEMA` or `COHORT-READ` and **no** `counts`, `total`, or `accounted` fields. So on every payload that reports a partition, the partition is total.

Assumption for the per-seat congruence: `read_bytes` is content-stable for a pinned revision. Production passes a `git_read(binding.sha, path)` lambda (`:153`), which reads committed blobs at one fixed revision, so the aggregate and per-seat passes see identical bytes. Under a non-deterministic reader the two passes could disagree, but that is not the shipped path.

**P1 verdict: Holds.** No source-visible counterexample found.

## P2 — split result: holds in the nested field, falsified at the process verdict

### Bounded reason the nested strict field stays red

Strict findings are row-local: every finding depends only on one `row` plus the bytes read for that row; `total`, `distinct_source_files`, and `pinned_reviews` are computed but never feed `code` (`check-review-snapshots.py:49,67,81,121,126-127`). The one-review manifest used per seat carries the same validated schema and the same row, and the only aggregate shape requirement beyond the per-row checks is a non-empty `reviews` list, which a singleton satisfies. Therefore the aggregate finding set is a superset of each row's finding set, and any read/encoding error is identical in both passes. Contrapositive: if any report-present seat has `one_code != 0` (i.e. `delivered_faulty`), then `strict_code != 0`, so `strict_conformance` is `FAIL` or `CANNOT_EVALUATE`, never `PASS` (`:73`). This holds for an all-faulty cohort too.

### Concrete counterexample at the top-level verdict

Construct (source-visible, not executed): a manifest with two reviews `A` and `B`, both sources digest-matching, both reports present, both reports carrying a predicate line that differs from the manifest predicate. Settlement has `A` and `B`, each `outcome: completed`, `error: ""`.

Expected trace:

- aggregate strict evaluation: two `REVIEW-PREDICATE-MISMATCH` findings, no read/encoding error, so `strict_code == 1`;
- per-seat evaluation: each `one_code == 1`, each report non-`None`, so `category == delivered_faulty` twice (`:61`);
- `delivered_faulty == 2`, `total == 2`, `accounted == 2`, two rows;
- `absent_unresolved == 0` and `strict_code != 2`, so `findings == []` (`:66-69`);
- `code = 0` (`:70`), `status = "PASS"` (`:79`), process exit `0` (`:160`);
- simultaneously `strict_receipt_exit == 1` and `strict_conformance == "FAIL"` (`:72-73`).

So an all-faulty cohort prints `PASS` and exits `0`. The same occurs for an all-`absent_dead` cohort: every report `None`, every settlement outcome `failed` with an observed error, `strict_code == 1`, `absent_unresolved == 0`, `findings == []`, exit `0`.

This is not an untested corner: the built-in fixtures encode that expectation. Every fixture manifest has exactly one review (`check-review-cohort.py:86-103`), so each single-seat faulty case is an all-faulty cohort of size one:

- `dead-missing` → exit `0`, `absent_dead == 1`, `strict_receipt_exit == 1` (`:95`);
- `partial-failed` → exit `0`, `delivered_faulty == 1`, `strict_receipt_exit == 1` (`:96`);
- `period`, `predicate`, `digest` → exit `0`, `delivered_faulty == 1`, `strict_receipt_exit == 1` (`:97-98`);
- `duplicate-receipt` → exit `0`, `delivered_faulty == 1`, `strict_receipt_exit == 1` (`:100`);
- `unicode` → exit `0`, `delivered_faulty == 1`, `strict_receipt_exit == 1` (`:102`).

**P2 verdict:** holds if "strictred" means the nested `strict_conformance`/`strict_receipt_exit` fields; **falsified** if it means the tool's top-level `status` or exit code. The docstring promise "without converting strict receipt faults to passes" is true for the nested fields and false for the process verdict: `status: PASS` coexists with `strict_conformance: FAIL` whenever all delivered seats are faulty and none is unresolved. A consumer that gates on exit code or `status` — the natural reading of the preregister command — sees a green all-faulty cohort.

## Fixture coverage gaps (why the selftest cannot settle this)

- No successful multi-seat case exists: every accepted fixture manifest has one review; the only two-review case is `duplicate-manifest` (`:106-107`), which is rejected before accounting.
- The fixture harness (`:112-118`) asserts only the exit code, that one named bucket equals `1`, finding-id membership, and `strict_receipt_exit`. It never asserts `total`, `accounted`, the sum of the four counts, `len(seats)`, per-row name/agent/category, or the top-level `status` string.
- Consequently P1 and the per-seat-output contract have zero fixture coverage; they are code invariants only. P2 is fixtured only through the nested `strict_receipt_exit`, never through top-level status.

## Adjacent C3 calibration hazard

`cohort_accounting_mode` is `1` not only on the accounted path but also on both fail-closed error payloads (`:75-78`), where `total` and all four counts are absent; only a missing manifest yields mode `0` (`:23`). A malformed settlement, dropped/duplicate/unknown seat, false death, duplicate JSON key, or missing settlement therefore reports `cohort_accounting_mode: 1` with exit `2`. The preregister metric `cohort_accounting_mode == 1` can thus be satisfied by a build in which cohort accounting produced no partition at all. If acceptance reads only that field, target `1` is not evidence for P1; it should additionally require `accounted == total` (ties `total` to the sum) and `status == "PASS"`.

## Expected fixture verdict vs observed runtime

Source-expected exits from `:93-108` (not executed here):

| fixture | expected exit | expected bucket/finding | expected strict exit |
|---|---|---|---|
| clean | 0 | delivered_conformant=1 | 0 |
| dead-missing | 0 | absent_dead=1 | 1 |
| partial-failed | 0 | delivered_faulty=1 | 1 |
| missing-unresolved | 1 | absent_unresolved=1, COHORT-UNRESOLVED | 1 |
| period / predicate / digest | 0 | delivered_faulty=1 | 1 |
| duplicate-receipt | 0 | delivered_faulty=1 | 1 |
| crlf | 0 | delivered_conformant=1 | 0 |
| unicode | 0 | delivered_faulty=1 | 1 |
| encoding | 2 | delivered_faulty=1, COHORT-STRICT-UNAVAILABLE | 2 |
| dropped / duplicate / unknown / false-death | 2 | COHORT-SCHEMA, no counts | n/a |
| manifest-missing | 1 | COHORT-MANIFEST-MISSING, mode 0 | n/a |
| duplicate-manifest / duplicate-json-key | 2 | COHORT-SCHEMA, no counts | n/a |

Observed runtime: **none**. This seat executed no fixture, so no runtime verdict was observed; the table is a source-derived expectation and must not be recorded as a run.

## Verdict summary

| claim | verdict | confidence |
|---|---|---|
| four counts sum to fixed total, `accounted == total`, rows == total | holds by construction; unfixtured | high |
| all-faulty keeps nested strict fields red | holds | high (given content-stable reader) |
| all-faulty keeps top-level verdict/exit strict-red | **falsified**; concrete two-seat and one-seat counterexamples, fixture-encoded | high |
| P1 is demonstrated by the selftest | **falsified**; no multi-seat or aggregate assertion exists | high |
| `cohort_accounting_mode == 1` evidences accounting | **falsified**; error payloads also set mode 1 | high |

Residual unknowns: the declared digest was not recomputed (NO-EXEC); actual `.ufo/waves/round-22/build/reviews.json` and `settlement.json` are outside this seat's read paths; no runtime observation exists. The predicate should be pinned to either the nested strict field or the process verdict before it is scored, because those two readings disagree on the all-faulty case.

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3buckets
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
