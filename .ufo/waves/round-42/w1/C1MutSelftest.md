VERDICT: supports
# C1-8 — the six single-site reverts scored by the 4476620 census's own `--selftest`

Seat C1MutSelftest (leaf, w1, r42 hyaku 9). Item: revert each of the six sites the C1
implementation commit 447662088dfd3155e31aed239179a79c1d1046c7 fixed (base
c8efaa3f120834541f8de1e5e0367e8d1593bae6), run the reverted census's own `--selftest` per
mutant, report kills/labels/survivors, and propose exact selftest cases for every survivor,
shown red on the revert and green on 4476620. All runs are scratch copies; the lane's tracked
content was never written, and no frozen counter was run (that is item C1-7's scope).

## 1. Method (bounded, one selftest at a time)

- Green and base census files extracted read-only:
  `git -C <lane> archive 4476620 -- tools/tsukuroi-census.sh | tar -x -C $S/green` (same for base).
  Blob check: `git rev-parse 4476620:tools/tsukuroi-census.sh` = ed83079c400594ab5ed84da045a6ed020c1a2542
  (matches the `index dda066f4..ed83079c` header of the base..impl diff); green file sha256
  46d62a24…f1b1, base blob dda066f4…, base file sha256 646c84fc… (receipts/hashes.txt).
- Each mutant = scratch copy of green with exactly one site reverted to the base text
  (`diff -U0` changed-line counts green→mutant: 692:2 694:2 1621:2 1635:4 1641:4 1652:2).
  Mutant sha256 before == after every run (receipts/hashes.txt) — no run mutated its own file.
- Detector: `TMPDIR=$S bash <variant>/tools/tsukuroi-census.sh --selftest` (the script re-invokes
  itself per case via `SELF=${BASH_SOURCE[0]}`, census.sh:427, with all probe surfaces pointed at
  fixture stubs, census.sh:2152-2183), run sequentially, one at a time, scratch-only TMPDIR.
- Baseline first: green = `TSUKUROI_CENSUS_SELFTEST: PASS (130 cases, 130 passed, 0 failed)`,
  exit 0, 28.45 s (receipts/green-baseline.out). A mutant is KILLED iff its selftest exits 1.

## 2. The six mutants and the selftest verdicts

Base line numbers per the declaration; green line numbers in parentheses (blob ed83079c).

| # | base :line (green) | site | verdict | killing label / observed check output |
|---|---|---|---|---|
| 1 | :692 (green :695) | `printf \| grep -q '^error:'` if-condition | **KILLED** | `blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1)` — `FAIL … : exit 0 wanted 2; output: …TSUKUROI_CENSUS: HEALTHY (packages=HEALTHY …)` |
| 2 | :694 (green :697) | `$(printf \| grep -m1 '^error:')` PKG_NOTE | **KILLED** | same label — `FAIL … : exit 141 wanted 2` |
| 3 | :1621 (green :1624) | -Qu `cand_names` `head -n3` | **KILLED** | `degraded: 4002 update candidates keep the names and the trap row (R42-C1)` — `FAIL … : exit 141 wanted 1` |
| 4 | :1635 (green :1638-1639) | qu-empty/-Sup disagree `cand_names` `head -n3` | **SURVIVED** | selftest `PASS (130 cases, 130 passed, 0 failed)`, exit 0 |
| 5 | :1641 (green :1644-1645) | -Qu/-Sup mismatch `cand_names` `head -n3` | **SURVIVED** | selftest `PASS (130 cases, 130 passed, 0 failed)`, exit 0 |
| 6 | :1652 (green :1655) | -Suu `suu_first` `head -n1` | **KILLED** | `degraded: 4002 update candidates keep the names and the trap row (R42-C1)` — `FAIL … : exit 141 wanted 1` |

Observed summaries (full logs in receipts/, one file per run):
- mut692: `FAIL blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1): exit 0 wanted 2; output: STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0|TSUKUROI_CENSUS: HEALTHY (packages=HEALTHY systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)` then `TSUKUROI_CENSUS_SELFTEST: FAIL (130 cases, 129 passed, 1 failed)`, exit 1. Note the mode: the SIGPIPE'd pipeline reads false in the `if`, the error line is ignored, and the census **lies HEALTHY** — the R41 defect mode, not a crash.
- mut694: `FAIL blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1): exit 141 wanted 2; output: tsukuroi-census census-v2 — host=fixture-host — 2026-10-26T19:50:36Z — read-only` then FAIL (130, 129, 1), exit 1 — the census child died of SIGPIPE (141) in the reverted command-substitution assignment under `set -euo pipefail` (census.sh:423).
- mut1621 / mut1652: `FAIL degraded: 4002 update candidates keep the names and the trap row (R42-C1): exit 141 wanted 1; …` then FAIL (130, 129, 1), exit 1 each (receipts/mut1621.out, mut1652.out).
- mut1635 / mut1641: PASS (130, 130, 0), exit 0 each (receipts/mut1635.out, mut1641.out).

## 3. Why the two survivors survive (coverage finding)

The only >64 KiB update-safety fixture at 4476620 is `degraded-update-candidates-large`
(census.sh:2558-2565), where -Qu and -Sup **agree** at 4002 candidates. Both survivor sites sit
inside branches that require -Qu/-Sup disagreement: `if [ "$qu_state" = 'empty' ] && [ "$sup_n" -gt 0 ]`
(census.sh:1635) and `elif [ "$qu_state" = 'cand' ] && [ "$sup_n" -ne "$qu_n" ]` (census.sh:1640) —
neither executes on that fixture. Every other update fixture is fx_default-sized (2 candidates,
~40 B), where `head -n3` and `awk 'NR <= 3'` are output-identical and nothing approaches the
64 KiB pipe buffer, so the revert is semantically indistinguishable there. A surviving mutant is a
coverage finding, not a contract change: the two R42-C1 cases kill the four reachable-in-their-
fixture sites and no case enters the disagreement arms with a large -Sup side.

## 4. Proposed selftest cases for the two survivors (exact text)

Insert into `run_selftest` immediately after the `check 'degraded: 4002 update candidates keep the
names and the trap row (R42-C1)' …` call (census.sh:2564-2565), before `case_home='blocked-update-qu'`.
Both cases only add run_selftest content — the kill rule's allowed hunk region — and touch no
production line. Verbatim, as I inserted and ran them (green copy lines 2567-2586):

```bash

  # Round 42 (C1-8, seat C1MutSelftest): the -Qu-empty/-Sup disagreement arm with a -Sup side
  # that outgrew the 64 KiB pipe buffer — the equal-count R42-C1 case never enters this branch,
  # and the old `printf | head -n3` assignment died of SIGPIPE (census exit 141) exactly here.
  case_home='degraded-update-sup-disagree-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/qu"; printf 1 > "$FX/qu.rc"
  { printf 'fixture/alpha 1.1-1\nextra/beta 2.1-1\n'
    awk 'BEGIN { for (i = 0; i < 4000; i++) printf "extra/pad%05d 1.0-2\n", i }'; } > "$FX/sup"
  check 'degraded: -Qu empty against a large -Sup keeps the disagree names (R42-C1)' 1 DEGRADED \
    '^PLANE update-safety: DEGRADED \(status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=4002 join_behind=0 names=\[alpha,beta,pad00000\]\); qu=rc=1/0; sup=4002 disagree\[qu=0 sup=4002\];'

  # Round 42 (C1-8, seat C1MutSelftest): the -Qu/-Sup count-mismatch disagreement arm with a
  # -Sup side that outgrew the 64 KiB pipe buffer — the equal-count R42-C1 case never enters
  # this branch, and the old `printf | head -n3` assignment died of SIGPIPE (exit 141) here.
  case_home='degraded-update-qu-sup-mismatch-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'alpha 1.0-1 -> 1.1-1\nbeta 2.0-1 -> 2.1-1\n' > "$FX/qu"; printf 0 > "$FX/qu.rc"
  { printf 'fixture/alpha 1.1-1\nextra/beta 2.1-1\n'
    awk 'BEGIN { for (i = 0; i < 4000; i++) printf "extra/pad%05d 1.0-2\n", i }'; } > "$FX/sup"
  check 'degraded: -Qu/-Sup count mismatch against a large -Sup keeps the disagree names (R42-C1)' 1 DEGRADED \
    '^PLANE update-safety: DEGRADED \(status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=4002 join_behind=0 names=\[alpha,beta,pad00000\]\); qu=rc=0/2; sup=4002 disagree\[qu=2 sup=4002\];'
```

Fixture text per case (knob files under $FX, on top of `fx_default`; dispatcher mapping
`-Qu→qu/qu.rc`, `-Sup→sup/sup.rc`, census.sh:1960-1962): case A sets `-Qu` = empty output at rc 1
(the real "no updates" shape, qu_state='empty', census.sh:1617-1618) and `-Sup` = 4002 lines
`fixture/alpha 1.1-1`, `extra/beta 2.1-1`, then 4000×`extra/padNNNNN 1.0-2` (~100 KB); case B sets
`-Qu` = rc 0 with the 2 candidate lines `alpha 1.0-1 -> 1.1-1`, `beta 2.0-1 -> 2.1-1` and the same
large `-Sup`. Expected evidence is the single ERE regex shown on each `check` (pinned prefix of the
`PLANE update-safety` line, including `disagree[qu=0 sup=4002]` / `disagree[qu=2 sup=4002]` and the
prefix-stripped first three names `[alpha,beta,pad00000]`).

### 4.1 Red/green demonstration (both run)

- GREEN on 4476620: green + both proposed cases → `PASS degraded: -Qu empty against a large -Sup keeps the disagree names (R42-C1) (exit 1, DEGRADED)` and `PASS degraded: -Qu/-Sup count mismatch against a large -Sup keeps the disagree names (R42-C1) (exit 1, DEGRADED)`, summary `TSUKUROI_CENSUS_SELFTEST: PASS (132 cases, 132 passed, 0 failed)`, exit 0 (receipts/props-green.out).
- RED on revert 4 (mut1635 + case A only): `FAIL degraded: -Qu empty against a large -Sup keeps the disagree names (R42-C1): exit 141 wanted 1; output: tsukuroi-census census-v2 — host=fixture-host — 2026-10-26T19:54:19Z — read-only`, summary `FAIL (131 cases, 130 passed, 1 failed)`, exit 1 (receipts/propsmut1635.out).
- RED on revert 5 (mut1641 + case B only): `FAIL degraded: -Qu/-Sup count mismatch against a large -Sup keeps the disagree names (R42-C1): exit 141 wanted 1; output: tsukuroi-census census-v2 — host=fixture-host — 2026-10-26T19:54:44Z — read-only`, summary `FAIL (131 cases, 130 passed, 1 failed)`, exit 1 (receipts/propsmut1641.out).

Each survivor is thereby covered by a case that is red on its revert (census child dies with
SIGPIPE exit 141 inside the reverted assignment) and green on 4476620. With these two cases
integrated, all six reverts of this item are selftest-killed.

## 5. What this does and does not claim

- Supports the C1 implementation claim at its own bar: the census `--selftest` at 4476620 kills
  4 of the 6 single-site reverts, with the two new R42-C1 labels carrying every kill; the two
  survivors are named above with demonstrated covering cases for the L1 to integrate (wave 2).
- Not run here: the frozen counter score-size-invariance-r42.py (item C1-7's scope), the live
  census, anything under `unshare`, and any lane-file edit. No tools were installed or upgraded
  for this seat (bash/awk/git only). One selftest at a time; nothing outside scratch + my report/
  receipts was written. Scratch /fast/scratch/hyaku/tsukuroi-r42/C1MutSelftest removed after
  receipt copy; census-copy sha256 values before == after all runs (receipts/hashes.txt).
