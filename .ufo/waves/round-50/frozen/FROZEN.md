# Round 50 — FROZEN record (tsukuroi, hyaku run 11, L1 TsukuroiR50, attempt 1)

Base revision (lane tip at round start, before any round-50 byte):
`b866a1d3d26616119a089f1a69b080136becc17b` · branch `master`.

Freeze revision = the lane commit that carries this file (`round-50: FREEZE — claims C1/C2/C3,
frozen counters, corrections applied before data`). Every seat reads lane bytes with
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <FREEZE>:<path>`; the working tree
is mutable and is never the bytes under test.

Round 49 closed `rejected-honest-stop` (`corpus/lessons/round-49-verifier-spotcheck.md` §8:
C2 adjacency and C3 operability verified, C1 depth not verified because the cohort bound one
`partly`). Ordinals at base: depth 8, coverage 9, operability 9, freshness 9, calibration 9,
adjacency 8 — depth and adjacency tied lowest, so the lowest-axis duty binds (saturation line 9,
window 3: not every axis is ≥9). C1 works depth, C3 works adjacency, C2 works operability.

## Claims (1–3, causally separable, distinct axes)

| Claim | Axis | Surface moved | Frozen counter | Before at base | Target predicate |
|---|---|---|---|---|---|
| C1 | depth (lowest tied 8) | `corpus/knowledge/btrfs-scrub-grounding-r45.md`: the four corrections the round-49 counted critic `R49CritGR2b` named (the `[inference]` mark narrowed to btrfs-progs printing, S240 named in the `source:` line and QUALITY item 7, the `dev-replace.c:1128` quote exact, the S247/S240 range gaps declared in Limits) are in the bytes, the counter's citation leg binds real reports, and a fresh 18-seat cohort of ONE wave reads GR1-GR3 `holds` on those bytes | `python3 tools/check-scrub-admission-r50.py --revision <REV>` | `corr_ok 0, verdicts_ok 0, seats_ok 0, marks_ok 0` → FAIL | `structural_ok == 1 and corr_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3` |
| C2 | operability (sourced: S256 opened this round) | `tools/tsukuroi-census.sh` selftest harness: the must-match arms no longer use `printf '%s\n' "$out" \| grep -q` / `\| head -n1` under `set -euo pipefail` (the round-49 flake, `R49ExecSelfAssess` §4: 11/20 false misses at a 96 KiB buffer), replaced by `buf_has`/`out_has` (awk, full read, no early exit, no here-string), and one new case `(R50-C2)` pins the matcher with 20 trials on a 200 KB buffer (167 → 168 cases) | `python3 tools/check-selftest-matcher-r50.py --revision <REV> --scratch <DIR>` | `idiom_sites 7, cases 167, case_ok 0` → FAIL | `idiom_sites == 0 and base_misses > 0 and full_misses == 0 and cases == 168 and pass_runs == 2 and case_ok == 1` |
| C3 | adjacency (lowest tied 8) | `tools/check-adjacency-table-r50.py`: the ADJ-01..07 anchors are verified by CONTENT — registry digest, heading and quote against the pinned sibling blob, and the quote again at the sibling's live tip — and the counter must fail a shape-valid stub that the round-49 counter passed (routed defect 3, V5 "the counter is a shape test") | `python3 tools/check-adjacency-table-r50.py --revision <REV>` | `quote_at_pin_ok 0, live_quote_ok 0, stub_fails 0` (legs absent at r49) → FAIL | `adj_rows == 7 and linked_rows == 7 and bare_ranges == 0 and anchors_ok == 7 and registry_ok == 7 and anchors_checker_rc == 0 and quote_at_pin_ok == 9 and live_quote_ok >= 8 and stub_fails == 1` |

Frozen row hashes at the freeze revision (LF-joined row lines including the blank line before
the next `## ` heading, printed by `--section-hash`):

| Row | Extent (freeze lines) | sha256 |
|---|---|---|
| GR1 | `## GR1` → `## GR2` | `3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1` |
| GR2 | `## GR2` → `## GR3` | `a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f` |
| GR3 | `## GR3` → `## How this changes OS triage` | `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` |

The row bytes are frozen from here: the only post-wave edit allowed is the `## Gate status — round 50`
heading text (outside every row extent), the SKILL/README marks, and SCORECARD/LOG/README prose.

## Counted cohort (claim C1) — 18 seats in wave `w1`

`R50RevGR{1,2,3}{a,b,c}` (reviewer) and `R50CritGR{1,2,3}{a,b,c}` (critic). A report binds only as a
FILE at `.ufo/waves/round-50/w1/<seat>.md`, line 1 `ROW GR<n> VERDICT: holds|partly|fails`, line 2
`SECTION SHA256: <hex>`, body >= 300 bytes citing at least TWO distinct row source files by
`file:line` that resolve in the pinned snapshots (or in a declared lane artifact — the round-50
citation repair). A bound-format negative (`partly`/`fails`) on the current hash blocks the row
whatever its citations; a report whose citations do not resolve earns nothing. Each expected seat
must also be one completed entry of `w1-results.json` (name, agent, non-empty output) and one
dispatch task with the declared role.

## Pre-data controls (frozen counters; receipts in `.ufo/waves/round-50/controls/`)

Battery `controls/battery.py --freeze <FREEZE>`; summary files
`battery-summary-r50-c{1,2,3}.jsonl`.

| Counter | Controls |
|---|---|
| C1 | K0 base entry, no cohort (FAIL) · K1 corrected entry + marks, no cohort (FAIL: `seats_ok 0`) · K2 all-holds cohort on bytes with the round-49 quote defect restored (FAIL: `corr_ok 0`) · K3 one bound `partly` (FAIL) · K4 whitespace-padded identical bodies (FAIL: distinct bodies) · K5 GR1 reviewers only (FAIL) · K6 reports but no results entries (FAIL: `seats_ok < 18`) · K7 lane-artifact citations only (FAIL: no row source cited) · K-pass corrected entry + marks + 18 valid reports (PASS) |
| C2 | K0 base census (FAIL: `idiom_sites 7, cases 167, case_ok 0`) · K1 the fix with the new case removed (FAIL: `cases 167`) · K2 the fix with one pipe idiom restored (FAIL: `idiom_sites 1`) · K-pass the freeze census (PASS) |
| C3 | K1 shape-valid stub via `--province-file`/`--registry-file` (FAIL: content legs 0) · K2 ADJ-02 pointed at `OUT-002` (FAIL) · K3 one registry digest mutated (FAIL: `quote_at_pin_ok 8`) · K-pass the freeze province + registry (PASS) |

The K-pass runs use synthetic fixtures to prove a counter CAN pass; they are never reported as the
claim's measurement. The measurement is the live integrated revision.

## Environment / guards carried into every seat prompt

Lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (git `master`, jj-colocated: L1 is the only
writer, `jj-lane.sh` only). Seats are read-only on tracked files and write only their report plus
receipts under `.ufo/waves/round-50/w1/<seat>[.md]`; scratch under
`/fast/scratch/hyaku/tsukuroi-r50/<seat>/`, removed on exit; no git/jj mutation outside a throwaway
fixture repo under that scratch dir; tooling authorization with the pacman pause (install via
`uv tool`/`npx`/official `~/.local/bin` binary only). Relative `Report:` trailers land under the lane
root.
