VERDICT: defect-found

D-5 no-harm battery: 10 predecessor gates run at freeze `8029cdba1049df25632c91a23c8db4eefb54be5f` and at round-start base `b866a1d3d26616119a089f1a69b080136becc17b`. Receipts (raw JSON per gate per revision) in `.ufo/waves/round-50/w1/R50RevNoHarm/` (`sa`, `aa`, `ao`, `kh`, `sc`, `rc`, `an`, `ec`, `sr`, `fd` x `_freeze.txt`/`_base.txt`). Every command was run as `python3 tools/<gate>.py --revision <REV>` from a scratch cwd with `TMPDIR` set; exit codes captured; no lane writes.

## Verdict matrix

| gate | freeze | base | fields changed base→freeze | failure pre-existing at base? |
|---|---|---|---|---|
| check-self-assessment | **FAIL** (checked 27, mismatches 3) | FAIL (27, 1) | mismatches 1→3; K13 and K17 became `mismatch`; K10 unchanged | partially — K10 (lessons 73 vs 74) fails at base; K13/K17 are NEW |
| check-adjacency-anchors | PASS | PASS | identical except `revision` | n/a |
| check-adjacency-overlap | PASS | PASS | identical except `revision` | n/a |
| check-knowledge-header | PASS | PASS | identical except `revision` | n/a |
| check-section-citations | PASS | PASS | identical except `revision` | n/a |
| check-registry-coverage | **FAIL** (findings/missing 9, tools 83, rows 74) | FAIL (6, 80, 74) | findings/missing 6→9; tools_total 80→83; +3 REGISTRY-ROW-MISSING | yes — gate already FAIL; the 3 new misses are NEW this round |
| check-appended-notices | PASS | PASS | identical except `revision` | n/a |
| check-edit-contract | **FAIL** (EDIT-PROSE `corpus/knowledge/structured-edit-r23.md`, decisions 8, validated 0) | FAIL | identical except `revision` | yes — identical failure |
| check-scrub-record-r44 | **FAIL** (verdicts_ok 0; SR7/SR8/SR9 `verdict_ok: false`) | FAIL | identical except `revision` | yes — byte-identical JSON except `revision` |
| check-fd-band-r49 | **FAIL** (band_ok 0, cases 168) | **PASS** (band_ok 1, cases 167) | band_ok 1→0, cases 167→168 | no — NEW regression |

## Findings (severity order)

### F1 (high, new harm): C2's new selftest case flips check-fd-band-r49 PASS→FAIL
- Evidence: `check-fd-band-r49.py --revision 8029cdb` prints `{"band_ok":0,"cases":168,"diag_ok":1,"stale_ok":1,"summary":"TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)","verdict":"FAIL"}` (rc 1, receipt `fd_freeze.txt`); at base `{"band_ok":1,"cases":167,...,"verdict":"PASS"}` (rc 0, `fd_base.txt`).
- Mechanism: `tools/check-fd-band-r49.py` pins the case count — `TARGET_CASES = 167` (line 43), `band_ok` requires `cases == TARGET_CASES` (line 106), predicate `... and cases == 167` (lines 49,113). The selftest itself fully PASSes; only the count pin breaks.
- Root cause: C2 added case `(R50-C2)` to `tools/tsukuroi-census.sh` (freeze lines 3643-3660), raising the selftest 167→168 without updating this predecessor counter. The only other `167` pin in tools/ at freeze is the C2 counter itself (`grep -n "167" tools/`). This is unambiguous harm of the round-50 change on a round-49 gate.

### F2 (high, new harm): self-assessment gains two mismatches from the same case count
- `check-self-assessment` at freeze: `mismatches 3` — K10 (pre-existing at base), K13 `operability row states 167 cases; the census selftest at this revision prints 168 cases`, K17 `host-census-gate row states 167 cases; ... 168 cases` (receipt `sa_freeze.txt`). At base only K10 fails (`sa_base.txt`).
- Stale text: `SCORECARD.md:3153` states ``PASS (167 cases, 167 passed, 0 failed) at round 49`` and `SCORECARD.md:3163` likewise; the C2 diff adds the `(167 → 168 cases)` claim in the new C2 row but leaves the round-49 measured-surface rows stale.

### F3 (medium, worsened): registry-coverage loses 3 more tools
- Freeze: 9 `REGISTRY-ROW-MISSING` of 83 regular tools (`rc_freeze.txt`); base: 6 of 80 (`rc_base.txt`). New misses are exactly the three round-50 counters: `tools/check-adjacency-table-r50.py`, `tools/check-scrub-admission-r50.py`, `tools/check-selftest-matcher-r50.py`. The operative registry table is still `## Gate and probe registry — round46 superseding current rows` (SKILL.md:4467); r47-r50 tools appear in prose only. Same defect class as the 6 pre-existing misses (r47-r49 tools) — the failure is pre-existing, the three new sites are new.

### Pre-existing, unchanged (no harm attributed to freeze)
- check-edit-contract: identical `EDIT-PROSE` finding on `corpus/knowledge/structured-edit-r23.md`, `total_decisions 8, validated_edit_decisions 0` at both revisions.
- check-scrub-record-r44: identical output except `revision` (verdicts_ok 0; SR7/SR8/SR9 `verdict_ok: false`, quotes/props/host/sources all OK). Verified byte-equal JSON minus `revision`.
- self-assessment K10: `depth row states 73 lesson files; corpus/lessons holds 74` at both revisions (SCORECARD.md:3151).
- All five PASS gates produce byte-identical JSON except `revision` (verified by comparison).

## Proposed fixes (exact text)

1. `tools/check-fd-band-r49.py` line 43: `TARGET_CASES = 167` → make the pin a floor so later rounds can extend the selftest: `TARGET_CASES = 167  # floor; later rounds may add cases` and line 105-106 `cases == TARGET_CASES` → `cases >= TARGET_CASES`, line 113 same; update docstring line 21 `(target 167 = 166 + 1)` → `(minimum 167 = 166 + 1)`. This keeps the r49 intent (the new case exists and the summary is clean) without breaking every future case addition.
2. `SCORECARD.md:3153`: change `` `bash tools/tsukuroi-census.sh --selftest` prints PASS (167 cases, 167 passed, 0 failed) at round 49 `` → `prints PASS (168 cases, 168 passed, 0 failed) at round 50`, cite the round-50 evidence (`.ufo/waves/round-50/before/c2-at-base.json` for the base and the w1 C2 counter output for the head).
3. `SCORECARD.md:3163`: same `167`→`168` update in the host-census-gate row.
4. `SCORECARD.md:3151`: `corpus/lessons/ 73 files` → `74 files` (pre-existing K10; optional for this round).
5. Add operative registry rows in the round-46 table (or a new superseding `round<N>` table) naming `tools/check-scrub-admission-r50.py`, `tools/check-selftest-matcher-r50.py`, `tools/check-adjacency-table-r50.py` in a `| name | kind | entry ... |` row each; long-term the same for the six pre-existing r47-r49 misses.

## Not done / verification gaps
- Did not run the round-50 counters (`check-scrub-admission-r50`, `check-selftest-matcher-r50`, `check-adjacency-table-r50`); out of this item's scope.
- Fix proposals above are unverified (text only); no counter was edited.
- One selftest-bearing command ran at a time per the host guard; check-self-assessment and check-fd-band-r49 each ran a census `--selftest` (~30 s each here).

## Tooling
- No installs or upgrades needed or performed (all gates are repo-local python3 + git).
