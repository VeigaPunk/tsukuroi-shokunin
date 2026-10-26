VERDICT: supports

# C1ExecPriorCounters — item C1-4 (kill rule: prior counters)

Item: at the C1 implementation commit `44766208`, the two prior-round counters must still pass —
`score-selftest-mounts-r41.py` (expect PASS) and `score-storage-hidden-r39.py` (expect PASS).
Both were run once each, serially, alone on the host, at the pinned revision. **Both PASS, exit 0.**
The declared kill rule is therefore not tripped by the C1 implementation.

## 1. score-selftest-mounts-r41.py — PASS

Command (run from the seat scratch dir with `TMPDIR` inside it; one counter at a time):

```
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-selftest-mounts-r41.py \
  --revision 447662088dfd3155e31aed239179a79c1d1046c7 \
  --scratch /fast/scratch/hyaku/tsukuroi-r42/C1ExecPriorCounters/a --jobs 4
```

Observed: process exit `0`; wall time **212.18 s** (harness-measured). stdout/stderr saved as
`.ufo/waves/round-42/w1/C1ExecPriorCounters/selftest-mounts-r41.out` (62 391 B, sha256
`d6a27af6993bab39cdc534d0ff20cacfb9d922617f79575ad89ade65d1c4d156`) and `.err` (0 B).

Verdict lines, `selftest-mounts-r41.out`:

| field | value | location |
|---|---|---|
| counter | `score-selftest-mounts-r41` | :2 |
| revision | `447662088dfd3155e31aed239179a79c1d1046c7` | :3 |
| branch_tip (informational) | `87c4f7c627e377e5f6d361498e8db9b3886d7953` | :4 |
| baseline last line | `TSUKUROI_CENSUS_SELFTEST: PASS (130 cases, 130 passed, 0 failed)` | :8 |
| baseline_pass | 1 | :14 |
| neutral_pass | 3 | :16 |
| decoy_pass | 1 | :17 |
| mutants_applied | 13 | :18 |
| survivors | 0 | :19 |
| params | 4 | :21 |
| result / exit | `PASS` / 0 | :343 |

Frozen predicate it scores — `baseline_pass == 1 and neutral_pass == 3 and decoy_pass == 1 and
mutants_applied == 13 and survivors == 0 and params == 4` (:5) — every conjunct holds, so the
counter's own rule fires PASS, not just the harness expectation.

All 13 mutants are recorded `killed: true` with `confirmed: true` and a second confirming run
(`confirm_last` = `FAIL (130 cases, …)`) beside `first_fails`: 13 occurrences of
`"killed": true` at `selftest-mounts-r41.out` lines 60, 84, 102, 126, 144, 162, 180, 204, 224, 242,
260, 278, 296 and 13 of `"confirmed": true`; e.g. `M1-VA-device-literal` opens at :37 and its
`"killed": true` / `"confirm_last": "TSUKUROI_CENSUS_SELFTEST: FAIL (130 cases, 124 passed, 6 failed)"`
sit at :58–:60. The three neutrals and the decoy print
`PASS (130 cases, 130 passed, 0 failed)` (:304, :314, :324, :336), i.e. the decoy here-document
carrying every mutant's text is *not* refused — the arm is judged by behaviour, as the counter
designs. All four parameter cases P1–P4 are bound to a PASSing baseline label (`param_cases`), so
the declared parameter conjunct is not vacuous.

## 2. score-storage-hidden-r39.py — PASS

Command (started only after run 1 had exited):

```
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-storage-hidden-r39.py \
  --revision 447662088dfd3155e31aed239179a79c1d1046c7 \
  --scratch /fast/scratch/hyaku/tsukuroi-r42/C1ExecPriorCounters/b
```

Observed: exit `0`; wall time **36.23 s** (harness-measured). Saved as
`.ufo/waves/round-42/w1/C1ExecPriorCounters/storage-hidden-r39.out` (4 517 B, sha256
`06e9200192b0803bc68f1f4333185b8e05bd044283943da5599469c746e2ca38`) and `.err` (0 B).

Verdict lines, `storage-hidden-r39.out`:

| field | value | location |
|---|---|---|
| predicate | `hidden_matched == 2 and views_matched == 3 and fixtures_matched == 5 and live_match == 1 and six_planes_all == 1` | :6 |
| hidden_matched | 2 | :7 |
| views_matched | 3 | :8 |
| fixtures_matched | 5 | :9 |
| live_match | 1 | :10 |
| six_planes_all | 1 | :11 |
| result / exit | `PASS` / 0 | :12 |

Every leg carries a non-vacuous expectation and matches it, e.g. H1/H2
`STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`
(the round-38 absent-root/false-all-clear defect stays refused at this revision), the three
namespace-filled views H0–H2 produce `HEALTHY 2/5/0`, `DEGRADED 2/2/5`, `DEGRADED 3/8/11` from the
counter's own model, fixtures F1–F5 match all five expected lines, and the live leg matches the
counter's independent read (`HEALTHY 1/1/0`). Randomisation seed for this run:
`c53b42d72cd6f078fd8baa6d796cb27c` (:5).

## 3. Cross-checks and limits

- **Identities read** (read-only): `tools/score-selftest-mounts-r41.py` sha256
  `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`;
  `tools/score-storage-hidden-r39.py` sha256
  `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`. The results above belong to
  these bytes; if either file is later edited the run must be repeated.
- **Pinned revision, not the tip.** Both runs bind `--revision 44766208…` and read the census via
  `git show`; the lane worktree HEAD is `87c4f7c627e377e5f6d361498e8db9b3886d7953` (advanced past the
  C1 commit during the wave). `branch_tip` inside both JSON records names the tip at run time and is
  informational. I did **not** re-run either counter at the tip — that is not this item.
- **Baseline case count 130** observed in the r41 counter (`…OUT:8`) matches the declared
  "selftest 128 -> 130 cases". Informational only; the case-count claim belongs to the C1
  implementation seats, and this counter's `PASS_RE` does not pin a count.
- Cheap corroboration that the two new cases are present in the pinned census: at `44766208`,
  `git show 44766208…:tools/tsukuroi-census.sh | grep -c R42-C1` printed `2`.
- **What this item does not establish:** it does not test C1's pipefail/pipeline fix itself (that is
  `tools/score-size-invariance-r42.py`, other seats), does not audit the census diff hunks, and does
  not cover the C2 scrub-record counter.
- **Run-count honesty:** one invocation each; no repeat after load. Both counters perform their own
  serial retry of flaky legs (r41: `retried`; `first_fails` are recorded), and no retry field was
  populated in the r41 record's top-level baseline, so no verdict here is a second attempt.
- **Timing method:** wall times are the tool-harness measurements; the shell-side attempt was
  discarded because `/usr/bin/time` and `bc` are absent on this host (`error: command not found:
  /usr/bin/time`), so no in-shell figure is quoted anywhere in this report.

## 4. Host guard compliance

Read-only on the lane (`git log`, `git rev-parse`, `git show`, `git status` only; no add/commit/
checkout/reset/stash, no jj). No package/service/sysfs/mount/boot/`/etc`/`/var/lib` change and no
sudo; the only namespaces were the counters' own private `unshare -rm` children. No btrfs
scrub/device-stats mutation. No tools installed or upgraded. Writes: this report, the two counter
outputs, `run-log.txt` under `.ufo/waves/round-42/w1/C1ExecPriorCounters/`, and scratch under
`/fast/scratch/hyaku/tsukuroi-r42/C1ExecPriorCounters/` (removed after the receipts were copied; the
counters left `a/` and `b/` empty). No background process of mine survives; only the two counter
invocations were run, serially.

Files changed: none in the lane's tracked tree. Blockers: none.
