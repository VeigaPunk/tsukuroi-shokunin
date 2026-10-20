# ReviewNoOral: runbook commands and exit meanings (round 15)

Scope: read-only research on new runbook sections only. Not a SKILL recertification. No gate, census, selftest, awk-on-log, or pacman command was executed. No verification claimed.

Read: `SKILL.md` `## Fleet round-1 append` (:1639-1674), `### Gate registry` (:1705-1715), `## Round 13` + `### Erratum (2026-10-20, round 14)` + `### Round-14 correction-conformance gate registry` (:1717-1785); `corpus/lessons/round-14-verifier-spotcheck.md` (§Step-1, §C1, §census); `tools/check-source-scope-correction.py`, `tools/check-root-dac-correction.py`, `tools/tsukuroi-census.sh`, `scripts/sources-census.sh` (outside lane, read-only).

## Exit meanings (from source; not run)

| Command | Exit meaning | Source |
|---|---|---|
| `check-source-scope-correction.py [--revision REV]` | 0 PASS · 1 FAIL · 2 CANNOT_EVALUATE | constants L14; `main` L502-539 returns `result.code` |
| `check-source-scope-correction.py --selftest` | 0 PASS · 1 FAIL (in-memory) | L430-499 |
| `check-source-scope-correction.py` bad CLI | 2; one JSON line, `status=CANNOT_EVALUATE`, finding `E-CLI` | L510-515 |
| `check-root-dac-correction.py [--revision REV]` | 0 PASS · 1 FAIL · 2 CANNOT_EVALUATE | constants L19; `main` L349-375 |
| `check-root-dac-correction.py --selftest` | 0 PASS · 1 FAIL | L346-348 |
| `check-root-dac-correction.py` bad CLI | 2 from argparse usage on stderr; no `CHECK_ROOT_DAC_CORRECTION` line | L354 bare `parse_args` |
| `tsukuroi-census.sh` | 0 HEALTHY · 1 DEGRADED · 2 BLOCKED (worst plane wins); usage errors 2 | L2622-2628, L2673-2676 |
| `tsukuroi-census.sh --selftest` | 0 pass · 1 fail; `[ "$FAIL" -eq 0 ]` propagates through `run_selftest`→`main` | L2608-2610, L2632-2634, L2680 |
| `tsukuroi-census.sh --help` | 0 | L2627 |
| `scripts/sources-census.sh validate <lane>` | 0 clean or W-only · 1 any E-code (or census missing) · 2 usage/env/missing registry · 3 selftest failure | header L16-18; L739, L803-806 |
| `git merge-base --is-ancestor` | 0 ancestor / 1 not ancestor / 128 error [INFERENCE: general git behaviour, not re-checked] | lesson §Step-1 |

Lesson's gate table (`source-scope`: 1 on baseline, 0 at implementation, selftest 0, invalid CLI 2) is consistent with this code. The lesson's observed results were not reproduced here.

## Findings

- **F1, medium (static, not reproduced): `check-root-dac-correction.py` has no catch-all.** `main` catches only `Cannot` (L369). `git()` (L226-230) does not guard `FileNotFoundError`, and `evaluate` errors other than `JSONDecodeError` are unhandled. An uncaught exception gives a traceback and exit 1, which the registry maps to "1 failed", not "2 could-not-evaluate". `check-source-scope-correction.py` avoids this with `except Exception` → CANNOT (L529-530). This is a verdict-map defect in a lane-owned tool. Not fixed here.
- **F2, low: root-dac bad CLI does not emit the CANNOT line.** The registry's "2 could-not-evaluate" matches only numerically. A verifier should not expect a structured line there.
- **F3, medium: pacman awk counts cannot see full upgrades.** Count 1 needs `Running .pacman -S ` (literal space after `-S`), so `-Sy`/`-Syu`/`-Syyu` are missed. Count 4 needs ` -Su`, which `-Syu` does not contain, so it is also blind to `-Syu`. `downgraded` is not counted. The line anchor `NR>=2287` is positional, not time-based. A zero `-Su` count does not exclude a `-Syu`. Only `[ALPM] upgraded` (0 on 2026-10-19) discriminates. Recorded values `7/64/0/0` are 2026-10-19 values, not fresh. [INFERENCE] A fresh run after the 2026-10-20 04:25 libinput partial upgrade may show nonzero `upgraded` if it was logged; not observed. Recommend timestamp anchoring and patterns `-S[a-zA-Z]*`, `-R[a-zA-Z]*`, `downgraded`; confirm log timestamp format first.
- **F4, medium: stale count and hash pins.** Current `tools/tsukuroi-census.sh` is md5 `b7de3bdd53325d411b66df3e2e718e36`, 2679 lines. SKILL pins the r10 revision `945c76fc…`, 2402 lines (:1592). SKILL:525-526 expects `PASS (26 cases…)`; :1593 pins 80. Neither count is established for the current file. A verifier must take the count from the run, not from these pins.
- **F5, verified: source-scope pin.** `sha256sum tools/check-source-scope-correction.py` = `0771619dde7cc69fdb37538ad786f293b629f4062167a44a2d9cf4702ec6d428`, matching the lesson. Current root-dac `4422941d8e1dadb5e4f8326ecf44169d19cfd083336c3c4c9066d5a2aa95ad44`, 375 lines, has no pin in the registry.
- **F6, none: sources-census W-codes.** Only E-codes set exit 1 (L739, L805), so the lesson's `exit0` with five W04 rows is consistent with the code.

## Recommendations

1. L1 runs once after integration: `source-scope --revision 8606bad…` (expect 1), `--revision 9dd82bc…` (expect 0), each selftest (0), `census --selftest` (0, count taken from output), `sources-census.sh validate … tsukuroi` (0). Record each exit and stdout line; re-resolve HEAD first.
2. Lane fix for F1: add a catch-all in root-dac `main` mapping to `CANNOT`, and a test for it. Owner: tsukuroi lane, not this seat.
3. Replace the pacman awk set per F3 before any C2 claim; state the anchor used.
4. Stop quoting fixed census case counts in SKILL; reference the printed count.

## Limits and tools

- Static reading only. The root-dac exception path (F1) and argparse exit-2 behaviour were not executed.
- Source-scope invalid-revision path was read only in part (L519-530).
- `sources-census.sh` is outside the lane root; read, not edited.
- Commands run: `sha256sum`, `wc -l`, `md5sum`, `grep -n` (read-only). No pacman, no `-Sp`, no `checkupdates`, no sudo, no installs.
- Tools installed or updated: **none**.
