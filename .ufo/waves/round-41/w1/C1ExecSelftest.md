VERDICT: supports

# C1ExecSelftest — C1-2: census `--selftest` at tip 71851d6 (128/128, twice) + live census vs base

Seat: C1ExecSelftest (L2, leaf). Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin.
Item: C1-2. Judged on operability, C1. Milestone: selftest at tip.

## What I ran (read-only on the lane; no host mutation, no sudo, no package/service change)

Exported census at the dispatch tip (not the file in the worktree):

```
$ mkdir -p /fast/scratch/hyaku/tsukuroi-r41/C1ExecSelftest/t
$ cd /fast/scratch/hyaku/tsukuroi-r41/C1ExecSelftest
$ git -C <lane> show 71851d636ab1bffaf8fee5016617c88878a666f1:tools/tsukuroi-census.sh > c.sh   # rc=0, 3176 lines
646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95  c.sh
$ git -C <lane> show 0e5805a1f149bd2ed9fe0db2e0a832afb034a835:tools/tsukuroi-census.sh > base.sh  # rc=0, 3149 lines
032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733  base.sh
$ git -C <lane> rev-parse HEAD
71851d636ab1bffaf8fee5016617c88878a666f1
```

All runs: cwd `/`, `TMPDIR=/fast/scratch/hyaku/tsukuroi-r41/C1ExecSelftest/t`, `bash <file>` (no `--jobs`; the selftest and the live census are not counter runs). No counter was executed by this seat.

## 1. `--selftest` at tip, twice — PASS both times, byte-identical

```
run1: rc=0  wall≈47.8s  TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)
run2: rc=0  wall≈53s    TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)
$ grep -c '^PASS' st1.out st2.out
st1.out:128
st2.out:128
$ diff <(sed 's/([0-9.]*s)//' st1.out) <(sed 's/([0-9.]*s)//' st2.out)   # empty output
```

No flaky case: the two runs differ in nothing (the `diff` is empty after stripping any per-case elapsed-time decoration; there were no such decorations in the output, so plain `diff st1.out st2.out` is also empty). Receipts: `C1ExecSelftest/selftest-summary.txt`, `r41-cases-run1.txt`, `r41-cases-run2.txt`, `timings.txt`.

Base for the case-count delta (one extra read-only run, for attribution only):

```
base.sh --selftest: rc=0  wall≈59s  TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)
```

128 − 124 = 4: the tip's selftest is the base's 124 cases plus exactly the four new R41-C1 cases, and the base file contains none of them (`grep -c 'R41-C1' base.sh` → `0`). Receipt: `selftest-summary-base.txt`.

## 2. The four new R41-C1 case labels, each PASS (run1 line numbers; run2 identical at the same lines)

```
123 PASS healthy rollup: a btrfs line whose mountpoint is not absolute still counts, BLOCKED (R41-C1 H5) (exit 0, HEALTHY)
124 PASS healthy rollup: a btrfs line whose source is not under /dev still counts, BLOCKED (R41-C1 H6) (exit 0, HEALTHY)
125 PASS healthy rollup: a btrfs line with no subvol= option still counts, BLOCKED (R41-C1 H9) (exit 0, HEALTHY)
126 PASS healthy rollup: two btrfs lines are still btrfs without sysfs, BLOCKED (R41-C1 H10) (exit 0, HEALTHY)
```

(`$L/c.sh:3042,3048,3054,3061` carry the same four labels.) Each case asserts exit 0 / `HEALTHY` with the mount-table reason surfacing only on the storage line, `^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$` — e.g. `c.sh:3039-3043` (table `/dev/vdc1 relative/mnt btrfs ...`), `c.sh:3045-3049` (`UUID=0b1c2d3e-... /data btrfs ...`), `c.sh:3051-3055` (`/dev/sdc1 /mnt/plain btrfs rw,commit=60`), `c.sh:3056-3062` (two btrfs lines, `/` and `/home`). Failures would be loud per case (`bad "$label"`), and none appeared.

Attribution corroboration (static read, no counter run): the four labels correspond 1:1 to the frozen mutants in `tools/score-selftest-mounts-r41.py:98-103` — `H5-mountpoint-absolute`, `H6-source-devonly`, `H9-subvolkey-option`, `H10-count-exactly-one` (`if [ "$mt" -gt 0 ]` → `if [ "$mt" -eq 1 ]`). Receipt: `counter-mutant-labels.txt`. I did **not** run the counter (out of this item's scope; it is a ~5–20 min run and the parent owns the once-per-item rule).

## 3. Deployment shape of the change — only `run_selftest` moved

```
$ git -C <lane> diff --numstat 0e5805a1f...71851d63 -- tools/tsukuroi-census.sh
27  0  tools/tsukuroi-census.sh
```

Pure insertion (27 added, 0 deleted), all inside the selftest `check` block (`@@ -3034,6 +3034,33 @@`, first added line `c.sh:3042`). That is consistent with the claim that `probe_storage_arm` is not changed in this round and that the new cases are the whole delta. Receipt: `census-diff.txt` (numstat + every added line).

## 4. Live census at tip vs live census at base — same host, same minute

Both binaries run from cwd `/`, back to back:

```
tip  c.sh     rc=1  wall=5s  header 2026-10-26T18:06:20Z (15:06:20-03:00)
base base.sh  rc=1  wall=6s  header 2026-10-26T18:06:25Z (15:06:25-03:00)
```

Six PLANE lines and the STORAGE line, tip run (`live-tip-lines.txt`); base run is identical in verdicts (`live-base-lines.txt`):

| line | tip | base |
|---|---|---|
| `PLANE packages` | DEGRADED | DEGRADED |
| `PLANE systemd` | HEALTHY | HEALTHY |
| `PLANE drivers` | DEGRADED | DEGRADED |
| `PLANE journal` | DEGRADED | DEGRADED |
| `PLANE update-safety` | DEGRADED | DEGRADED |
| `PLANE oom` | DEGRADED | DEGRADED |
| `STORAGE btrfs-device-stats` | `state=HEALTHY filesystems=1 devices=1 nonzero=0` | identical string |

Rollups agree too: `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)` in both, and `HANDOFF ADJ-04 mori class=kill-events value=139` / `class=coredumps value=20` / `DRIFT pacnew-plane pacnew=3 … log=ok` are byte-identical.

`diff` of the seven PLANE/STORAGE lines across the two runs has exactly one hunk — the `PLANE drivers` line — and only in the four live host gauges that necessarily move between two runs 5 s apart (`live-diff-raw.txt`):

```
C5_pswp=10716/140739 (tip)      vs C5_pswp=10750/140739 (base)
C6_psi_full_total_us=14149458   vs C6_psi_full_total_us=14149472
C6_avail_kb=17996796            vs C6_avail_kb=18171680
C6_shmem_kb=5040                vs C6_shmem_kb=5048
```

Normalising those four gauges, the full 12-line outputs of the two revisions are identical except the header timestamp, i.e. the tip's live read is the base's live read. Both exit 1 because the rollup contains DEGRADED planes (pre-existing host state: `drift=2[1password-beta,1password-cli]`, `foreign=21(known=3 new=5 drift=13 gone=0)`, `kerr=37 (oom=0 io=35 gpu=0 other=2)`, 3 shadowed-newer candidates) — the same degradations already at base, not new ones.

## 5. Findings, limits, and what I did not do

- Selftest claim holds as stated for operability at tip: 128 cases, 0 failed, twice, same output; the four R41-C1 cases each PASS; base has 124 and none of those labels.
- Live census: six PLANE verdicts and the STORAGE line match base; no verdict drift from the round-41 selftest change. The only deltas are live host gauges on `PLANE drivers`. A non-flaky re-run was not needed (two identical selftest runs, and the live comparison is a single run per revision — if the parent wants duplicate live runs for flake evidence, they were not taken here).
- Wall times measured on a loaded shared host: selftest ≈48–59 s per run, live census ≈5–6 s per run. Four sequential runs total (~3.5 min), no parallel census/counter overlap.
- Mutant kill evidence (survivors == 0, params == 4, decoy/neutral counts) is **not** in this report: I did not run `tools/score-selftest-mounts-r41.py`. Static reading only confirms the four labels exist as the H5/H6/H9/H10 mutant targets.
- Scratch `/fast/scratch/hyaku/tsukuroi-r41/C1ExecSelftest/` removed after copying receipts; nothing was written in the lane outside this report and its seat dir; no git/jj mutating command, no package manager, no sudo, no service touched. No tool installs were needed.

Receipts: `.ufo/waves/round-41/w1/C1ExecSelftest/` — `selftest-summary.txt`, `selftest-summary-base.txt`, `r41-cases-run1.txt`, `r41-cases-run2.txt`, `live-tip-lines.txt`, `live-base-lines.txt`, `live-diff-raw.txt`, `census-diff.txt`, `counter-mutant-labels.txt`, `timings.txt`.
