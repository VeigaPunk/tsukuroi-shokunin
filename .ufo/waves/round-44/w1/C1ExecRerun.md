VERDICT: supports

Item C1-1 — C1 re-run stability. The frozen C1 counter is byte-identical at the freeze commit and in
the working tree, and it returns PASS with identical scored output on three independent draws at the
declared implementation revision `7e081698`, and FAIL at base `98020ece` exactly as the declared
before receipt. Nothing in the C1 claim is falsified; no defect found.

## 1. Counter identity (freeze blob == working file)

```
$ git -C <lane> show 1d2afffeaedbb553d951f53c9edb0190e345b1ab:tools/score-scrub-arm-r44.py | sha256sum
1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388  -
$ sha256sum <lane>/tools/score-scrub-arm-r44.py
1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388  <lane>/tools/score-scrub-arm-r44.py
$ git -C <lane> log --oneline -1 -- tools/score-scrub-arm-r44.py
1d2afffe round-44: declaration, frozen C1/C2 counters, control batteries + receipts, ...
```
Both hashes equal the declared `1409a5fd…6388`; no commit after the freeze has touched the counter, so
the working file is the freeze blob. Every receipt header below independently records
`"tool_sha256": "1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388"`.

Topology (so the measured surface is pinned): `1d2afffe` (freeze) → `ab8aae16` (arm + 9 selftest cases;
after receipt) → `7e081698` (C2 SR7 narrowing; after receipt re-recorded) → `ff2c264a` (w1 spec, lane
HEAD now). `git diff --stat ab8aae16 7e081698 -- tools/tsukuroi-census.sh` is empty and the census blob
is identical at both revisions (`fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c`),
vs base `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9`. `git diff --stat 7e081698
ff2c264a -- tools/` is empty, so the measured surface is still the lane's current tools.

## 2. Reruns (three draws at `7e081698`, one at base)

Commands (cwd `/fast/scratch/hyaku/tsukuroi-r44/C1ExecRerun`, `TMPDIR=/fast/scratch/hyaku/tsukuroi-r44/C1ExecRerun`,
run one at a time, ~30–41 s each):

```
python3 <lane>/tools/run-receipt.py --revision 7e081698d4fc3c4ea944884fd093058de9909de1 \
  --tool-revision 1d2afffeaedbb553d951f53c9edb0190e345b1ab \
  --out <lane>/.ufo/waves/round-44/w1/C1ExecRerun/c1-after-<n>.jsonl \
  -- tools/score-scrub-arm-r44.py --revision '{rev}' --scratch /fast/scratch/hyaku/tsukuroi-r44/C1ExecRerun/s
# same with --revision 98020ece0674e0b569ee23aed10ffbee355b248e -> c1-base-1.jsonl
```

| receipt | rev | cases | correct | wrong | identity | identity_ok | wired_ok | live_agree | selftest_line | selftest_r44 | selftest_pass | verdict | exit | wall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `c1-after-1.jsonl` | 7e081698 | 16 | 16 | 0 | [1000,1000,1000] | 1 | 1 | 1 | PASS (141 cases, 141 passed, 0 failed) | 9 | 1 | PASS | 0 | 30.3 s |
| `c1-after-2.jsonl` | 7e081698 | 16 | 16 | 0 | [1000,1000,1000] | 1 | 1 | 1 | PASS (141 cases, 141 passed, 0 failed) | 9 | 1 | PASS | 0 | 38.6 s |
| `c1-after-3.jsonl` | 7e081698 | 16 | 16 | 0 | [1000,1000,1000] | 1 | 1 | 1 | PASS (141 cases, 141 passed, 0 failed) | 9 | 1 | PASS | 0 | 40.7 s |
| `c1-base-1.jsonl` | 98020ece | 16 | 0 | 16 | [1000,1000,1000] | 1 | 0 | 0 | PASS (132 cases, 132 passed, 0 failed) | 0 | 1 | FAIL | 1 | 31.6 s |

Predicate row in every receipt: `cases == 16 and correct == 16 and identity_ok == 1 and wired_ok == 1
and live_agree == 1 and selftest_pass == 1 and selftest_r44 >= 6` (`tools/score-scrub-arm-r44.py:53`).

Live leg, identical in all three reruns and equal to the declared after receipt:
`SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0
limited=0 timers=0`, `wired: 1`. Base live leg: `got: []`, `wired: 0` (line absent at base).

Base failure cause is absence, not a wrong line: all 16 `wrong` entries carry `rc: 127` and
`got: ""` — `probe_scrub_record` does not exist at base (`git show 98020ece:tools/tsukuroi-census.sh |
grep -c probe_scrub_record` → `0`; at `7e081698` there are `9` `(R44-C1)` selftest labels).

## 3. Comparison with the declared receipts

- `before/c1-before.jsonl` (98020ece): mine matches it on every scored field — `cases 16, correct 0,
  identity_ok 1, wired_ok 0, live_agree 0, selftest_line "PASS (132 cases, 132 passed, 0 failed)",
  selftest_r44 0, selftest_pass 1, verdict FAIL`, footer `exit_code 1`, and the same 16 `wrong`
  ids in the same order with the same `rc`. Only the `wrong[].want` strings differ between the two
  runs, because they embed the per-run drawn fixture values (see §4). Live leg is byte-identical.
- `after/c1-after-ab8aae1.jsonl` (ab8aae16): identical to my reruns on `cases, correct, identity_ok,
  wired_ok, live_agree, selftest_line, selftest_r44, selftest_pass, verdict, channels_open` and on the
  whole `live` object. The `wired.want`/`wired.got` line differs between that receipt and each of my
  runs because it is a drawn fixture (§4) — each run matched its own oracle (`wired_ok: 1`).

## 4. Is the result stable across draws? Yes, with a measured reason it is not a fixed replay

The counter draws fixture values per run from an unseeded RNG: `rng = random.Random(os.urandom(16))`
(`tools/score-scrub-arm-r44.py:559`), then `drawn = make_cases(rng, live_fsids)` and
`wired_cases = make_cases(rng, live_fsids)` (`:562-563`); the expected line is recomputed by the
independent oracle `expect(model)` (`:582, :589`) from the drawn model, never from the scored output.

Evidence the three runs were genuine independent draws: the wired full-census line differs in all
three (`limited`/`timers`/`records`/`detail` counts and speed_max pairs change), yet each equalled its
own oracle:

```
run1: SCRUB ... records=3 tmp=0 sockets=1 unreadable=1 orphan=1 limited=2 timers=0 detail=8ca6e54a:17:speed_max=17162687,8ca6e54a:32:speed_max=26138606
run2: SCRUB ... records=3 tmp=0 sockets=0 unreadable=1 orphan=1 limited=0 timers=3
run3: SCRUB ... records=2 tmp=0 sockets=1 unreadable=1 orphan=1 limited=1 timers=3 detail=1d02a454:16:speed_max=38646806
```
(3/3 distinct). The 16 case ids are fixed and identically ordered on every draw (extracted by
importing `make_cases` with two synthetic seeds): `none-dir-absent, recorded-readable,
root-records-unreadable, orphan-records, tmp-beside-record, progress-socket, limited-devices,
speed-malformed, speed-unreadable, dir-unreadable, dir-not-directory, timers-enabled,
timers-unreadable, wrong-types, sysfs-unreadable, mixed`; only their values are drawn
(`tools/score-scrub-arm-r44.py:372-441`).

Limitation, stated rather than papered over: because a passing run reports only counts, the receipt
does not record the drawn per-case values, so run-to-run value identity/inequality for the 16 namespace
cases cannot be read from the receipts; the wired leg is the direct evidence of fresh draws.

## 5. Independent corroboration: live census unchanged (no-harm observation)

I also captured the whole live census from a sandbox at both revisions (read-only, 3.7 s each):
`census-live-98020ece.jsonl`, `census-live-7e081698.jsonl` (this time `--tool-revision` = the measured
revision, see §7).

- exit code: `2` at base and `2` at measured.
- rollup line identical: `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=BLOCKED drivers=DEGRADED
  journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)`.
- six PLANE lines: five byte-identical; `PLANE drivers` has the same verdict word `DEGRADED` and the
  same discrete fields (`kerr=37 oom=0 io=35`, `C1_kernel_oom=0 C2_sysd_oom=0 C3_sigkill=1
  C4_sweep=212`, `C5_swap_fail=417`, `guards=max/max`), differing only in live kernel counters that
  advanced between the two runs (`C5_pswp 484819→484826`, `C6_psi_full_total_us
  51373505→51373527`, `C6_avail_kb 19119880→18946192`, `C6_shmem_kb 25004→25000`). That drift is host
  activity, present between any two runs and not attributable to the revision; the text-level PLANE
  diff should therefore not be scored as a kill-rule hit, and I flag it so the seat that owns the
  no-harm measurement uses the discrete fields.
- line set differs by exactly the intended insertion: measured has
  `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`
  at line 12 of 13, i.e. after `STORAGE btrfs-device-stats ...` (line 11) and before the rollup
  (line 13) — the declared position, matching `tools/tsukuroi-census.sh:3370-3376` (`probe_storage_arm;
  printf STORAGE_LINE`, then `probe_scrub_record; printf SCRUB_LINE`, then the rollup).

That live SCRUB line also agrees with direct host inspection: `/var/lib/btrfs` does not exist, and
`/etc/systemd/system/timers.target.wants` holds only `fstrim.timer paccache.timer snapper-cleanup.timer
snapper-timeline.timer` (no `btrfs-scrub@*.timer`) — so `state=NONE dir=absent records=0 timers=0` is
the true value, not a fabricated default.

## 6. Host non-mutation

Before the first counter run and after the last: `/var/lib/btrfs` absent (`ls: cannot access
'/var/lib/btrfs': No such file or directory`), the `timers.target.wants` dir unchanged (same four
entries), `/sys/fs/btrfs` = `1d02a454-c549-4a35-b567-89d60902af8e features`. No package, service,
sysfs write or scrub command was issued; no sudo. No file was created at the fleet root, in the lane
tree, or in any PATH directory. Scratch `/fast/scratch/hyaku/tsukuroi-r44/C1ExecRerun/s` is empty after
all runs (the counter removes its own `scrub-arm-r44.*` work dirs), and I removed the scratch tree after
copying receipts.

## 7. Procedure note for the L1 (not a lane defect)

`run-receipt.py` executes the tool from `--tool-revision` (default `--revision`), and `--revision` is
only substituted into `{rev}`. Passing `--tool-revision 1d2afffe` while measuring the **census** runs
the pre-wave census, which prints no SCRUB line (my first capture, since overwritten at the same
`census-live-*.jsonl` paths, showed `STORAGE` immediately followed by the rollup). For the counter
(`score-scrub-arm-r44.py`, itself unchanged since the freeze) `--tool-revision 1d2afffe` is correct,
because the census under test is read from `--revision` inside the counter's own clone.

## 8. Not done here (assigned elsewhere / out of scope)

The full no-harm kill-rule battery (frozen predecessor storage counters `score-storage-arm-r38.py`,
`-r38-q82.py`, `score-storage-hidden-r39.py`, `score-size-invariance-r42.py`), the namespace case
oracle audit beyond the counter's own scoring, control-battery replay (`controls/`), and anything on
C2 were not run by me. The PLANE-drift observation in §5 is a single pair of live runs, not a battery.

## Receipts (this seat)

`<lane>/.ufo/waves/round-44/w1/C1ExecRerun/` — `c1-after-1.jsonl`, `c1-after-2.jsonl`,
`c1-after-3.jsonl`, `c1-base-1.jsonl`, `census-live-7e081698.jsonl`, `census-live-98020ece.jsonl`.
No tool was installed or upgraded for this seat.
