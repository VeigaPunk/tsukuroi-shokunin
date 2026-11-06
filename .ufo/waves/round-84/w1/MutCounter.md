# MutCounter — mutation sweep of the frozen C1 provenance counter (round 84, w1)

Seat: mutation-tester (leaf; no subagents, no model choice, no lane edits).
Lane measured: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Revision at measurement: `f19e73f3aa9817e76044e4e43a343c6ca6d929df` (`git rev-parse master`).
The instrument blob is unchanged across the wave: `git show <c6941adb|f19e73f3|HEAD>:tools/count-resume-rows-r84.py`
all hash to `cb70d4357ebe2d50f360dbbc2079f3a35756a79fc785280cf9d4312268ac8309` (the value frozen in the
round-84 declaration). Working-tree copy hashes identically. Host state untouched: no sysfs/proc writes, no
swap/hibernate/mkinitcpio/pacman, no `sudo`.

Subject: `tools/count-resume-rows-r84.py` — the C1 counter the SCORECARD re-declared on 2026-11-06 as a
**provenance shape gate, not a measurement**. This sweep attacks its frozen 8-rule predicate at one point per
mutant and measures whether the instrument's own selftest notices.

## 1. Baseline (pristine, 3 + 1 runs)

```
$ python3 tools/count-resume-rows-r84.py --selftest --root .        # ×3
{"selftest": "PASS (12 cases, 12 passed, 0 failed)", ...}           rc=0, rc=0, rc=0
$ python3 tools/count-resume-rows-r84.py --root .
{"verdict": "met", "counted": 10, "failed": 0, "distinct_snapshots": 6, "target_rows": 7, "target_snapshots": 4, ...}  rc=0
```
Pristine selftest stability at the frozen constants: **0 failures in 200 consecutive runs** (additional sweep).

## 2. Method

20 single-point mutants. Each is the committed file with exactly one textual change; every anchor was asserted to
occur exactly once (`src.count(old) == 1`) before the mutant was written, and mutant files are byte-copies otherwise.
Per mutant: `--selftest --root .` **3×** + `--root .` **1×**, cwd = lane root so the relative entry/manifest paths
resolve. **KILLED** iff any selftest run exits non-zero *or* the real-lane result tuple
`(rc, verdict, counted, failed, distinct_snapshots)` differs from `(0, met, 10, 0, 6)`. A further 10 selftest runs
measured stability. Every survivor then got a **behaviour probe**: a crafted entry applied to a fixture root rebuilt
from the frozen manifests (`_copy_inputs`) per probe, run against pristine and mutant, comparing
`(rc, verdict, counted, failed)`. Scratch root `/fast/scratch/hyaku/tsukuroi-r84/MutCounter` (removed; receipts copied here).

## 3. Results — 8 KILLED, 12 SURVIVED (10 gaps, 2 equivalent)

| id | single-point change (line) | selftest 3× | real | killing case | verdict |
|---|---|---|---|---|---|
| M01 | drop manifest-pin check (L118-120) | FAIL 3/3 | unchanged | `F2b-doctored-snapshot-and-manifest` (rc 1, want 2) | KILLED |
| M02 | drop bytes-vs-manifest check (L154-155) | PASS 3/3 | unchanged | — | SURVIVED (gap) |
| M03 | drop minimal-span check (L108-109) | FAIL 3/3 | unchanged | `F4-widened-span` (rc 0, want 1, counted 7) | KILLED |
| M04 | drop R6 distinctness (L205-210) | FAIL 3/3 | unchanged | `F3-one-row-duplicated` (counted 7, want 1) | KILLED |
| M05 | accept quotes >25 words (L183) | PASS 3/3 | unchanged | — | SURVIVED (gap) |
| M06 | skip host-value span check (L194-197) | FAIL 3/3 | unchanged | `F5-fabricated-host-value` (rc 0, want 1) | KILLED |
| M07 | `TARGET_SNAPSHOTS 4→3` (L52) | PASS 3/3 (+2/10 later) | unchanged | — | SURVIVED (gap, flaky kill) |
| M08 | `counted >=` → `>` (L218) | FAIL 3/3 | unchanged | `P1-random-valid-rows-met` (rc 1, want 0) | KILLED |
| M09 | cannot-evaluate rc 2→1 (L229) | FAIL 3/3 | unchanged | `D0`, `F2b`, `F9` (rc 1, want 2) | KILLED |
| M10 | drop snapshot-url https check (L142-143) | PASS 3/3 | unchanged | — | SURVIVED (gap) |
| M11 | drop R1 duplicate-id check (L172-173) | PASS 3/3 | unchanged | — | SURVIVED (gap) |
| M12 | R2 statement floor 8→5 words (L174) | PASS 3/3 | unchanged | — | SURVIVED (gap) |
| M13 | drop `failed == 0` clause (L218) | PASS 3/3 | unchanged | — | SURVIVED (gap) |
| M14 | quote floor 6→3 words (L183) | PASS 3/3 | unchanged | — | SURVIVED (gap) |
| M15 | `distinct_snapshots >=` → `>` (L218) | FAIL 3/3 | unchanged | `P1-random-valid-rows-met` (rc 1, want 0) | KILLED |
| M16 | skip entire host leg (L190-197) | FAIL 3/3 | unchanged | `F5-fabricated-host-value`, `F8-undeclared-receipt` (rc 0, want 1) | KILLED |
| M17 | drop span upper bound `b <= len(lines)` (L101) | PASS 3/3 | unchanged | — | SURVIVED (equivalent, label only) |
| M18 | drop R5 empty-value check (L195-196) | PASS 3/3 | unchanged | — | SURVIVED (equivalent, label only) |
| M19 | `TARGET_ROWS 7→6` (L51) | PASS 3/3 | unchanged | — | SURVIVED (gap) |
| M20 | R6 keeps quote half, drops span half (L205) | PASS 3/3 | unchanged | — | SURVIVED (gap) |

Verbatim killing-case lines are in `MutCounter/killing-cases.txt`. No mutant changed the real-lane reading: all 20
read `met / counted 10 / failed 0 / distinct 6 / rc 0` on `--root .`, so **the frozen counter's live verdict is
insensitive to every one of these predicate defects** — the selftest is the only detector that exists.

## 4. Survivors — evidence, not inference

Each probe below is a single-entry edit the *pristine* counter refuses and the mutant accepts, on a fixture root
rebuilt from the frozen manifests. `pristine` / `mutant` rows are the tool's own JSON, trimmed to the deciding fields.

| id | probe | pristine | mutant | class |
|---|---|---|---|---|
| M02 | append a line to a snapshot on disk, entry's declared digest + manifest untouched | rc 1, counted 9, `HR1: R3-snapshot-bytes-differ-from-manifest` | rc 0, counted 10, met | **gap** |
| M05 | 30-word quote at S336:1-5 (exact minimal span) | rc 1, `R4-quote-length` | rc 0, counted 10, met | **gap** |
| M07 | 7 valid rows citing only 3 distinct snapshots (`_random_entry(7, 3)`) | rc 1, counted 7, failed 0, distinct 3 | rc 0, met, distinct 3 | **gap (target)** |
| M10 | snapshot url downgraded to `http://` | rc 1, `R3-snapshot-url-not-https` | rc 0, counted 10, met | **gap** |
| M11 | two rows share id `HR1`, quotes/spans distinct | rc 1, counted 8, `R1-duplicate-id` | rc 0, counted 10, met | **gap** |
| M12 | 5-word statement | rc 1, `R2-statement` | rc 0, counted 10, met | **gap** |
| M13 | one fabricated quote on a 10-row entry (counted 9, failed 1) | rc 1, unmet | **rc 0, met with `failed: 1`** | **gap** |
| M14 | 4-word quote at S336:1-1 | rc 1, `R4-quote-length` | rc 0, counted 10, met | **gap** |
| M19 | 6 valid rows, 4 distinct snapshots | rc 1, counted 6 (< 7) | rc 0, met | **gap (target)** |
| M20 | two rows cite the same raw span `S336:110,110` with different 6-word quotes | rc 1, counted 9, `HR2: R6-duplicate-quote-or-span` | rc 0, counted 10, met | **gap** |
| M17 | span end `[a, 10^6]` past EOF | rc 1, `R4-lines-out-of-range` | rc 1, `R4-span-not-minimal` | equivalent (label) |
| M18 | empty host value | rc 1, `R5-empty-value` | rc 1, `R5-empty-needle` | equivalent (label) |

M20's first probe reused row 0's whole `source` (quote *and* span), so the surviving quote half of R6 still refused
it; the isolating probe above replaces only the quote and shows the span half is load-bearing: pristine refuses
`HR2` on the duplicate span, the mutant counts it and reads met. Both `R6` halves are therefore live checks with no
case behind either of them.

**M17 is provably equivalent.** For `b > len(lines)`: if `a < b`, the mutant's "drop line b" comparison uses
`lines[a-1:len]`, identical to the span itself, so the needle is found again and the row is refused as
`span-not-minimal`; if `a == b`, the slice is empty and the row is refused `not-in-span`. Both paths still fail —
only the reason string changes. **M18** is the same shape: an empty `value` becomes an empty needle
(`R5-empty-needle`), and a non-string value raises inside `norm()` and lands in `row-malformed`. Neither can turn a
`failed` row into a `counted` one on any input, which is why no legitimately counted-predicate test can kill them.

## 5. Findings

**F1 — the frozen targets are invisible to the selftest (M07, M19).** `P1` asserts
`counted == TARGET_ROWS`; `F6` builds `base[:TARGET_ROWS-1]` and asserts `counted == TARGET_ROWS-1`; `F7` builds
`_random_entry(..., TARGET_SNAPSHOTS-1)` and asserts `distinct_snapshots == TARGET_SNAPSHOTS-1`. Fixture and
expectation both read the same constant, so lowering either target moves the test with it: **M07 (4→3) and M19 (7→6)
each pass 3/3 and 10/10 and leave the real-lane reading met**. A candidate author could re-scope the C1 target and
the gate would still print `PASS (12 cases, 12 passed, 0 failed)`. This is the r82/r83 failure class (a target
re-declared after the fact) reproduced *inside* the instrument, and for a counter that is now declared a shape gate
rather than a measurement it is the one property the selftest absolutely had to hold.

**F2 — eight of the rule conditions have no case at all.** No selftest case ever produces: bytes that differ from an
intact manifest (M02), a non-https url (M10), a duplicate `id` (M11), a short statement (M12), a short quote (M14), a
long quote (M05), `counted >= target` together with `failed >= 1` (M13), or two different quotes over one raw span
(M20). Each survives 3/3 and 10/10 and each demonstrably flips `unmet → met` on a one-edit entry. The 12 frozen cases
cover R1-format, R3-digest, R4-span-minimality, R5-receipt, R6 and the three rc classes — nothing more.

**F3 — the positive control's generator truncates and makes the M07 kill flaky.** `_random_entry` stops after 10,000
tries and returns whatever it has. With the frozen 4 snapshots that never happened in 400/400 draws (7 rows) and
400/400 (8 rows); with the *mutant's* 3 snapshots it returns 6-row entries in 55/200 and 89/400 draws (144/600 ≈
24 %), because only 3 keys cycle through 7 rows. Those short entries fail P1's `counted == 7` assertion for a reason
unrelated to the mutation, which is why M07's kill is intermittent (2/10 extra runs failed; the captured failure is
`{"case": "P1-random-valid-rows-met", "rc": 1, "want_rc": 0, "counted": 6, "verdict": "unmet"}`). A flaky kill is not
evidence of detection: the "3/3 PASS" reading of M07 and M19 is what a candidate would see.

**F4 — the real-lane verdict is insensitive to all 20 mutants.** Every mutant reads `met` with `counted 10` on the
committed entry. Whatever else the counter is, its live reading is not discriminating between a correct predicate and
eight weakened ones; only the selftest is.

## 6. Proposed patch (not applied; the L1 decides)

- Patch: `.ufo/waves/round-84/w1/MutCounter/proposed/count-resume-rows-r84.patch`
- Derived file: `.../proposed/count-resume-rows-r84.proposed.py` (sha256 `ff1dbcdd…`; committed subject
  sha256 `cb70d435…`). `git apply --check` verified clean in a throwaway fixture; applying it reproduces the
  proposed file byte-for-byte. **`evaluate()`/`exact_span()` are untouched** — the frozen predicate is not re-scoped,
  only its negative controls are extended.
- `G0-frozen-target-literals`: fails when `(TARGET_ROWS, TARGET_SNAPSHOTS) != (7, 4)`; `P1`, `F6`, `F7` now use the
  literal 7/4/3/6 in both fixture and expectation.
- `G1` bytes-differ with intact declared digest; `G2` 30-word quote; `G3` 4-word quote; `G4` 5-word statement;
  `G5` duplicate id (asserts `counted == 5`, `failed == 2`); `G6` http url; `G7` 8-row entry with one fabricated
  quote (asserts `counted == 7`, `failed == 1`, rc 1); `G8` same raw span with a different quote; `G9` empty host
  value. `_any_span`/`_lines_of` helpers derive spans from the pinned snapshots so no fixture is memorised.

Validation:
- Proposed suite on the committed lane: `PASS (22 cases, 22 passed, 0 failed)` three runs, **0 failures in 30 runs**;
  `--root .` still `met, counted 10, failed 0, distinct 6` — the real verdict is unchanged.
- Kill matrix over the same 20 mutants with the proposed suite (3 runs each): **18/20 killed 3/3**, including all eight
  F2 gaps and both targets — `M02→G1`, `M05→G2`, `M07→G0/F7`, `M10→G6`, `M11→G5`, `M12→G4`, `M13→G7`,
  `M14→G3`, `M19→G0/F6`, `M20→G8`. Only M17 and M18 survive, both proven equivalent in §4.
- Residual risk: `G7` needs an 8-row random entry; `_random_entry(8, 4)` produced 8/8 rows in 400/400 draws. If a
  future edit shrinks the snapshot set below 4, G0 fails first by design.

## 7. Restoration / scope evidence

- Subject file never modified: `sha256sum tools/count-resume-rows-r84.py` =
  `cb70d4357ebe2d50f360dbbc2079f3a35756a79fc785280cf9d4312268ac8309` before and after the sweep;
  `git status --porcelain -- tools/ SCORECARD.md` → empty (0 lines).
- All mutants, drivers, probes and results live under `.ufo/waves/round-84/w1/MutCounter/` (20 `mutants/*.py`,
  `drive.py`, `probe.py`, `derive_proposed.py`, `sweep-results.json`, `probe-results.json`,
  `probe-results-extra.json`, `stability.json`, `proposed-kill-matrix.json`, `killing-cases.txt`, `SHA256SUMS`,
  `proposed/`). No lane file, MANIFEST.json, `.ufo/state/`, sibling repo or fleet-root file was touched.
- Scratch `/fast/scratch/hyaku/tsukuroi-r84/MutCounter` removed on exit.
- Tooling: none installed or upgraded (python3/pystdlib only, no pacman/npx/uv).

## 8. Limits

C2's gate battery was not run (out of seat scope). No claim is made about whether the patch should land before or
after the freeze; the patch is selftest-only and post-hoc by construction, so if the L1 wants it in the frozen
instrument it must be disclosed as a control change, not as a predicate change. Nothing here re-scopes C1 or C2.
