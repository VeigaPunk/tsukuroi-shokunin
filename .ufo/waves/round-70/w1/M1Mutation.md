# M1Mutation — mutation battery on the frozen C1 counter and the C2 XFS-stats arm

Round 70, wave w1 (the round's only wave). Seat M1Mutation, mutation-tester, leaf (no dispatch).
Lane HEAD at measurement `84e013a732d7526d08064c6823858d602029ecd7`. Read-only detection: every
byte I mutated lives in `/fast/scratch/hyaku/tsukuroi-r70/M1Mutation`; the lane received only the
receipts under `.ufo/waves/round-70/probes/M1Mutation/` and this report. No pacman/`uv`/network
install (none needed); no git mutation in any tracked tree (one `git clone --shared` and one
`git apply` inside that scratch clone, both naming `-C <scratch>/clone`).

Instruments under test (hashes re-derived at measurement, not copied from a claim):

| instrument | bytes | sha256 |
|---|---|---|
| `tools/count-xs-rows-r70.py` (frozen, unchanged) | 208 lines | `65065d9d18cea52027619697264de430780e65ff13ab6da2a790c3d2054f6f5c` (equals the frozen digest) |
| delivered arm: sandbox clone `tools/tsukuroi-census.sh` after `git apply` of `probes/E1XfsArm/r70-xfs-arm.diff` | — | `5268b53949eb0d5988fe3f3d5b9a605622e16ea00b76c15afd488627d357ff7d` (equals the producer receipt `applied-vs-sandbox-sha256.txt`) |

Detector definition used throughout: a case is a bounded behavioral reading (counter `--fixture`
rc, or the census `--selftest` verdict) whose expected value is derived from the frozen
declaration. A mutant is **killed** when at least one case deviates from that expected value; a
mutant that keeps every expected value is a **survivor** (coverage finding, never a contract
change). Baseline first, mutant second, and a baseline failure would have made the run
inconclusive — none occurred (counter: 12/12 cases at their expected rc; arm: 211/211 PASS rc 0).

## 1. C1 counter mutants (7 mutants)

Method. The committed pre-data battery (`.ufo/waves/round-70/before/control/build_battery.py`,
8 cases) was rebuilt under scratch with `COUNTER` pointed at a byte-identical copy of the frozen
counter (`XS_BATTERY_SCRATCH=<scratch>/battery-pre`): 8/8 PASS, rc 0 — the committed receipt
reproduces. Added detectors, all built from the frozen clauses: one well-formed control note over
the **real committed snapshots** (the four `before/src` files copied byte-exact — verified
`53bda67b…/4b6a9b6c…/1cbcffa1…/84fdd0be…` — with a registry whose source cells carry the
`SOURCES.json` map URLs; reads `XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4 XS_SNAPSHOTS=4`, met=1, rc 0)
and five clause-targeted fixtures built on those same real snapshots (only the note, or the map,
varies): `x-stopword` (statements of 12 stopwords present in the snapshot), `x-noncontiguous`
(ids 1,2,3,4,5,7), `x-pipe-cell` (a pipe inside the statement cell), `x-short-11` (an exactly
11-word statement), `x-map-drift-foreign` (the map's entry digest is wrong while a foreign map
entry carries the row's digest).

| mutant | frozen clause broken | killed by | pre-data battery alone |
|---|---|---|---|
| M1-drop-source-binding | source-to-snapshot URL binding | `mutant-any-registered-id` (rc 1→0) | **killed** |
| M2-any-snapshot-digest | map digest is per snapshot (`SOURCES.json`) | `x-map-drift-foreign` (rc 1→0) | survives |
| M3-no-stopword-filter | distinct **non-stopword** tokens | `x-stopword` (rc 1→0) | survives |
| M4-drop-quote-location | quote located verbatim in the snapshot | `mutant-quote-absent` (rc 1→0) | **killed** |
| M5-short-statement-7 | statement ≥ 12 words | `x-short-11` (rc 1→0) | survives |
| M6-any-id-order | ids contiguous from 1 | `x-noncontiguous` (rc 1→0) | survives |
| M7-pipe-in-cell | exactly 6 cells, no pipe in a cell | `x-pipe-cell` (rc 1→0) | survives |

Score: **7/7 killed** by the extended detector set; **2/7 killed** by the committed pre-data
battery alone. Every mutant wrote rc 0 on at least one malformed case before the added fixture.

Evidence detail (raw table in `counter-mutation-table.txt`, unified diffs in
`counter-mutants.diff`, per-case rc matrix in `mutant-results.json`):

- `M2-any-snapshot-digest` survives the committed battery for a specific reason: its
  `mutant-digest-swap` case is killed by the **snapshot-bytes** check
  (`XS_ROW fail XS1 digest-mismatch map-digest`), not by the map clause — a row digest that
  matches the snapshot but not `SOURCES.json` is not exercised. It is only killed by a map whose
  drift is masked by a foreign entry holding the row's digest.
- `M3`, `M6`, `M7` are invisible to the committed battery: `mutant-content-free` fails on the
  content clause with only one non-stop hit and `mutant-duplicate-id` fails on `duplicate-id`
  (and its contiguity is already false), so neither isolates the stopword filter or the
  contiguity test; no case puts a pipe in a cell.
- `M5` (threshold lowered to 7) survives because the only short statement in the committed
  battery is 4 words; an exactly-11-word row is what pins the frozen ≥12 boundary.
- `M1` and `M4` are properly detected by the committed battery.
- The pristine counter's own control is sound: the real-snapshot control is rc 0, and each
  targeted fixture fails only on its own clause (`statement-tokens=0`; `ids-not-contiguous`;
  `malformed`; `statement-words=11`; `map-digest`).

## 2. C2 arm mutants (8 mutants over the delivered arm)

Method. `git clone --shared` of the lane into scratch, `git rev-parse --show-toplevel` asserted
the clone, `git apply` of the delivered `probes/E1XfsArm/r70-xfs-arm.diff`; applied bytes hash
equals the producer's receipt. Baseline selftest on those bytes: **PASS (211 cases, 211 passed,
0 failed)**, rc 0 — includes the 15 `R70-C2` labels. Each mutant is a separate copy of those
bytes (`arm/<label>/tsukuroi-census.sh`; diffs in `arm-mutants.diff`), run with a hermetic
`TMPDIR` under scratch and a 100 s watchdog.

| mutant | frozen arm clause broken | killing case (label) | evidence |
|---|---|---|---|
| A1-no-dedupe | mounts == **distinct** xfs source count | `... one source mounted twice counts once, so the fields stay per-filesystem (R70-C2)` | FAIL 1/211, rc 1 |
| A2-global-as-fs | the global stats dir is never a filesystem | `... the global stats directory under the sysfs root is never counted as a filesystem (R70-C2)` | FAIL 1/211, rc 1 |
| A3-echo-bad-name | unvalidated basename never spelled/used; `echo:bad-name` | `... an escaped-space source and an embedded forged line never forge the census line (R70-C2)` | FAIL 1/211, rc 1 |
| A4-read-fifo | a FIFO is never opened | `... a FIFO stats file is never opened (no block) ... (R70-C2)` (run reached 200 PASS then hung) | watchdog rc 124 |
| A5-unreadable-parsed | unreadable stats file names `stats:unreadable`, never counted | `... a mode-000 stats file is never counted and names stats:unreadable (R70-C2)` | FAIL 3/211, rc 1 |
| A6-rollup-term | the line is never a rollup term | `healthy rollup: an unreadable mount table with no sysfs root is BLOCKED (R39-C1)` (first of 11) | FAIL 11/211, rc 1 |
| A7-silent-absent | absent names `sysfs:absent` | `... a listed xfs mount with no sysfs root counts absent and names sysfs:absent (R70-C2)` | FAIL 1/211, rc 1 |
| A8-no-first-line | first line must match the frozen regex, else `stats:malformed` | `... a first line outside the frozen shape names stats:malformed and is not counted (R70-C2)` | FAIL 1/211, rc 1 |

Score: **8/8 killed, 0 survivors.** Two precision notes for the integrator:

- **A6** (rollup term) is caught by three pre-existing R39 rollup cases and by eight R70 shape
  cases, but **not** by the new R70 neutrality A/B case: that fixture seeds
  `ai-usage.timer loaded failed failed`, so the journal plane is already DEGRADED and the rollup
  line cannot change. The clause is enforced, but not by the case that claims to enforce it.
- **A4** is killed by the watchdog, not by an assertion: the FIFO case cannot report a FAIL when
  the arm blocks, so a hang is the only observable. The selftest's own case therefore proves the
  non-block only if the runner has a timeout; without one, the suite hangs rather than fails.

## 3. What this battery does and does not say

- Both instruments are mutation-robust under the full detector set built here: counter 7/7,
  arm 8/8, no survivors.
- The **committed** C1 pre-data battery under-detects its own clauses: 5 of 7 mutants escape it.
  That is a coverage finding about a committed receipt, not a defect in the frozen predicate and
  not a licence to amend the contract; any added case is a planner amendment.
- Mutants are textual and single-clause; equivalent mutants (e.g. dropping `verified == len(rows)`
  in the final conjunction, which is subsumed by `verified == TARGET_ROWS` with `rows == 6`) were
  not counted as kills. The arm was mutated only in its body and its rollup wiring, not in its
  fixture cases or its header.
- One host, one revision, no network. Scratch under `/fast/scratch/hyaku/tsukuroi-r70/M1Mutation`
  was removed after the receipts were written.

Restoration evidence: the pristine counter copy still hashes
`65065d9d…4f6f5c` and the applied clone's census still hashes `5268b539…7ff7d` after the whole
battery (verified post-run); no mutant was ever written over either file, and the lane tree was
never in a mutation path.

Raw receipts: `probes/M1Mutation/{environment,counter-mutation-table,counter-mutants.diff,
fixture-digests,mutant-results.json,arm-mutation-table,arm-mutants.diff,arm-results.json,
arm-baseline-and-A6}.txt|json|diff`.

COUNTER_MUTANTS=7 COUNTER_KILLED=7 ARM_MUTANTS=8 ARM_KILLED=8 SURVIVORS=none
COUNTER_PREDATA_BATTERY_KILLED=2
