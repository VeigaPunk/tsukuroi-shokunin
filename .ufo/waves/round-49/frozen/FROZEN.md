# Round 49 — FROZEN record (tsukuroi, hyaku run 11, L1 TsukuroiR49, attempt 1)

Base revision (lane tip at round start, before any round-49 byte):
`6256760d1382ce4ce20fcba830d4b2912cfbf12b` · branch `master`.

Freeze revision = the lane commit that carries this file (`round-49: FREEZE — claims C1/C2/C3,
frozen counters, corrections applied before data`). Every seat reads lane bytes with
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <FREEZE>:<path>`; the working tree
is mutable and is never the bytes under test.

## Claims (1–3, causally separable, distinct axes)

| Claim | Axis | Surface moved | Frozen counter | Before at base | Target predicate |
|---|---|---|---|---|---|
| C1 | depth (lowest tied 8) | `corpus/knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3: the seven corrections the round-48 counted seats named (CritGR1a ×2, CritGR2a ×4, RevGR2a ×2 as one list of seven) are in the bytes and gone from the defect strings, and a fresh 18-seat cohort of one wave re-reads the corrected rows `holds` with distinct bodies | `python3 tools/check-scrub-admission-r49.py --revision <REV>` | `corr_ok 0, verdicts_ok 0, seats_ok 0, marks_ok 0` → FAIL | `structural_ok == 1 and corr_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3` |
| C2 | adjacency (lowest tied 8) | `PROVINCE.md` ADJ-01..07 **Ownership source** cells: bare sibling `*.md:N-M` ranges replaced by the OUT-0NN anchor naming that ADJ class, each anchor's pin/heading/quote and its registry blob digest checked | `python3 tools/check-adjacency-table-r49.py --revision <REV>` | `bare_ranges 9, linked_rows 0` → FAIL | `adj_rows == 7 and linked_rows == 7 and bare_ranges == 0 and anchors_ok == 7 and registry_ok == 7 and anchors_checker_rc == 0` |
| C3 | operability (sourced: S255 bash fd>9, re-opened this round) | `tools/tsukuroi-census.sh`: the stale `builds a /tmp fixture tree` comment is gone, the alias resolver records `ST_BASE_ERR` and `run_selftest` prints the named `fd band … exhausted` diagnostic, and one new selftest case `(R49-C3)` proves the exhausted-band path under a two-descriptor band | `python3 tools/check-fd-band-r49.py --revision <REV>` | `stale_ok 0, diag_ok 0, band_ok 0, cases 166` → FAIL | `stale_ok == 1 and diag_ok == 1 and band_ok == 1 and cases == 167` |

Frozen row hashes at the freeze revision (LF-joined row lines, no trailing LF; print with
`--section-hash`):

| Row | Extent | sha256 |
|---|---|---|
| GR1 | `## GR1` → `## GR2` | `3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1` |
| GR2 | `## GR2` → `## GR3` | `d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f` |
| GR3 | `## GR3` → `## How this changes OS triage` | `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` |

The row bytes are frozen from here: the only post-wave edit allowed is the `## Gate status — round 49`
heading text (outside every row extent), the SKILL/README marks, SCORECARD/LOG/README prose.

## Counted cohort (claim C1) — 18 seats in wave `w1`

`R49RevGR{1,2,3}{a,b,c}` (reviewer) and `R49CritGR{1,2,3}{a,b,c}` (critic). A report binds only as a
FILE at `.ufo/waves/round-49/w1/<seat>.md`, line 1 `ROW GR<n> VERDICT: holds|partly|fails`, line 2
`SECTION SHA256: <hex>`, body >= 300 bytes with `file:line` citations resolving in the pinned
snapshots. A bound-format negative (`partly`/`fails`) on the current hash blocks the row whatever its
citations; a report whose citations do not resolve earns nothing. Each expected seat must also be one
completed entry of `w1-results.json` (name, agent, non-empty output) and one dispatch task with the
declared role.

## Pre-data controls (frozen counters; receipts in `.ufo/waves/round-49/controls/`)

| Counter | Controls |
|---|---|
| C1 | K0 base/freeze bytes and no cohort (FAIL) · K1 corrected entry + marks, no cohort (FAIL) · K2 all-holds synthetic cohort on bytes with the five r48 defect strings restored (FAIL: `corr_ok 0`) · K3 one bound `partly` (FAIL) · K4 two byte-identical bodies (FAIL) · K5 reviewers only, no critics (FAIL) · K6 reports present but results entries absent (FAIL: `seats_ok < 18`) · K-pass the corrected entry + marks + 18 synthetic reports/results (PASS) |
| C2 | K0 base province (FAIL: `bare_ranges 9`) · K1 anchors added but ranges kept (FAIL) · K2 ranges removed, one `OUT-099` nonexistent (FAIL) · K3 all seven rows pointed at `OUT-001` (FAIL: wrong ADJ class) · K-pass the edited province (PASS) |
| C3 | K0 base census (FAIL: stale, no diagnostic, 166 cases) · K1 diagnostic added, new case removed (FAIL) · K2 case added, stale comment kept (FAIL) · K-pass the edited census (PASS) |

The K-pass runs use synthetic fixtures to prove the counter CAN pass; they are never reported as the
claim's measurement. The measurement is the live integrated revision.

## Environment / guards carried into every seat prompt

Lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (git `master`, jj-colocated: L1 is the only
writer, `jj-lane.sh` only). Seats are read-only on tracked files and write only their report plus
receipts under `.ufo/waves/round-49/w1/<seat>[.md]`; scratch under
`/fast/scratch/hyaku/tsukuroi-r49/<seat>/`, removed on exit; no git/jj mutation outside a throwaway
fixture repo under that scratch dir; tooling authorization with the pacman pause (install via
`uv tool`/`npx`/official `~/.local/bin` binary only). Relative `Report:` trailers land under the lane
root.

## Control outcomes (scored at `32a85560`, before wave w1 was dispatched)

Receipts: `controls/battery-summary-r49-c1.jsonl` (K0 K1 K2 K3 K4 K5 K6 FAIL, K-pass PASS), `-c2.jsonl`
(K0 K1 K2 K3 FAIL, K-pass PASS), `-c3.jsonl` (K0 K1 K2 FAIL, K-pass PASS). The K-pass fixtures prove each
counter can pass; they are not the claim measurement. Two fixture bugs were found and fixed while scoring
(C3-K1 cut the wrong `(R49-C3)` comment, C3-K2's stale-comment replacement did not match); both were
controls-only and no claim byte changed.
