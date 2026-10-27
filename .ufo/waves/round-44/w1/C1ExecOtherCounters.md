VERDICT: no-finding

Item C1-6 — no-harm for the remaining census counters. All four counters
(`tools/score-census-handoff-r32.py`, `tools/score-pacnew-arm-r35b.py`,
`tools/score-selftest-literals-r40.py`, `tools/score-selftest-mounts-r41.py`) produce the same
verdict at base `98020ece0674e0b569ee23aed10ffbee355b248e` and at the claimed revision
`7e081698d4fc3c4ea944884fd093058de9909de1`. No counter flips, and none of the changes is caused
by the new `SCRUB` line or by the nine `(R44-C1)` selftest cases: the two selftest counters pass
with `selfref == 5`, `mutants_applied` 9/13, `survivors == 0`, `params == 4` at both revisions and
kill the same labels; the two whole-output counters are indifferent to the new line (r32) or
already failed for a pre-round-44 reason and stay at the same count (r35b).

All runs were made with the frozen tools through `tools/run-receipt.py` (private clone at the
named revision), one heavy counter at a time, `TMPDIR=/fast/scratch/hyaku/tsukuroi-r44/C1ExecOtherCounters/s`,
receipts in `.ufo/waves/round-44/w1/C1ExecOtherCounters/`. No tool was installed or upgraded; no
lane file was written; the host was only read.

## 1. Result table (observed)

| Counter | base `98020ece` | rev `7e081698` | change |
|---|---|---|---|
| `score-census-handoff-r32.py` | `routed 24` of 24, `live_consistent true`, `harness_errors 0`, exit 0 | `routed 24` of 24, `live_consistent true`, `harness_errors 0`, exit 0 | none |
| `score-pacnew-arm-r35b.py` (battery) | `candidate_matches 4`, `of 24`, `control_matches 24`, `should_fail_accepted 0`, exit 1 | `candidate_matches 4`, `of 24`, `control_matches 24`, `should_fail_accepted 0`, exit 1 | none |
| `score-pacnew-arm-r35b.py` (`--skip-battery`) | `candidate_matches 4`, `of 24`, exit 1 | `candidate_matches 4`, `of 24`, exit 1 | none |
| `score-selftest-literals-r40.py` | PASS (132 cases), `baseline_pass 1`, `neutral_pass 3`, `mutants_applied 9`, `survivors 0`, `selfref 5`, exit 0 | PASS (141 cases), same fields, exit 0 | none |
| `score-selftest-mounts-r41.py` | PASS (132 cases), `baseline_pass 1`, `neutral_pass 3`, `decoy_pass 1`, `mutants_applied 13`, `survivors 0`, `params 4`, exit 0 | PASS (141 cases), same fields, exit 0 | none |

Receipts (each is a `run-receipt.py` JSON-lines receipt whose header names the revision and the
tool sha256):

* `C1ExecOtherCounters/r32-base.jsonl`, `C1ExecOtherCounters/r32-rev.jsonl` (same seed
  `d26bdc2550f2b04f` in both, so the 24 scenarios are identical)
* `C1ExecOtherCounters/r35b-base.jsonl`, `C1ExecOtherCounters/r35b-rev.jsonl` (battery)
* `C1ExecOtherCounters/r35b-skipbattery-base.jsonl`, `C1ExecOtherCounters/r35b-skipbattery-rev.jsonl`
* `C1ExecOtherCounters/r40-base.jsonl`, `C1ExecOtherCounters/r40-rev.jsonl`
* `C1ExecOtherCounters/r41-base.jsonl`, `C1ExecOtherCounters/r41-rev.jsonl`
* `C1ExecOtherCounters/parity-diff.txt` (the r35b parity diff quoted in §3)
* `*.console` beside each receipt (the driver's timing line)

Exact commands (one example each; every run used the same shape with the other revision):

```
python3 tools/run-receipt.py --revision 98020ece0674e0b569ee23aed10ffbee355b248e \
  --out <seat>/r32-base.jsonl --lane <lane> --timeout 1200 -- \
  tools/score-census-handoff-r32.py --revision '{rev}' --lane '{lane}' --scratch <s>/r32-base
python3 tools/run-receipt.py --revision 7e081698d4fc3c4ea944884fd093058de9909de1 \
  --out <seat>/r32-rev.jsonl --lane <lane> --timeout 1200 -- \
  tools/score-census-handoff-r32.py --revision '{rev}' --lane '{lane}' --scratch <s>/r32-rev --seed d26bdc2550f2b04f
python3 tools/run-receipt.py --revision <REV> --out <seat>/r35b-<tag>.jsonl --lane <lane> --timeout 3000 -- \
  tools/score-pacnew-arm-r35b.py --lane '{lane}' --revision '{rev}' [--skip-battery]
python3 tools/run-receipt.py --revision <REV> --out <seat>/r40-<tag>.jsonl --lane <lane> --timeout 2400 -- \
  tools/score-selftest-literals-r40.py --revision '{rev}' --repo '{lane}' --scratch <s>/r40-<tag>
python3 tools/run-receipt.py --revision <REV> --out <seat>/r41-<tag>.jsonl --lane <lane> --timeout 2400 -- \
  tools/score-selftest-mounts-r41.py --revision '{rev}' --repo '{lane}' --scratch <s>/r41-<tag>
```

Observed tails: r32 `{"routed": 24, "scenarios": 24, "unrouted": [], "live_consistent": true,
"harness_errors": 0, "kind": "summary" ... "exit_code": 0}` at both revisions (receipt line with
`"kind": "summary"`); r40 `"predicate": "baseline_pass == 1 and neutral_pass == 3 and
mutants_applied == 9 and survivors == 0 and selfref == 5"` with `"result": "PASS"`,
`"exit": 0` at both; r41 `"predicate": "baseline_pass == 1 and neutral_pass == 3 and
decoy_pass == 1 and mutants_applied == 13 and survivors == 0 and params == 4"` with
`"params": 4`, `"result": "PASS"`, `"exit": 0` at both.

## 2. Why the new selftest cases do not touch r40/r41

* Selftest case count 132 -> 141 is the only baseline change; r40's PASS regex accepts any case
  count (`tools/score-selftest-literals-r40.py:55`), and both r40 and r41 compare a mutant's case
  count against the baseline's own count of the same revision (`killed()` requires
  `res['cases'] == base['cases']`, `tools/score-selftest-mounts-r41.py:195-199`), so 141 vs 141 is
  consistent.
* `probe_storage_arm` is byte-identical between the two revisions, so all frozen `old` strings
  still occur exactly once: `mutants_applied` is 9 (r40) and 13 (r41) at both revisions. Command:
  `diff <(sed -n '/^probe_storage_arm()/,/^}/p' base.sh) <(sed -n '/^probe_storage_arm()/,/^}/p'
  rev.sh)` -> no output (`probe_storage_arm IDENTICAL`); same for `probe_pacnew*`.
* `SELFREF_BASE = 5` (`tools/score-selftest-literals-r40.py:54`) is unchanged: the r40 regex
  `\$\{?SELF|BASH_SOURCE|\$0\b|/proc/self/(exe|fd)|/proc/\$\$` matches 5 times in the census at
  both revisions (`selfref` 5 in both receipts); a grep of the new `probe_scrub_record` for
  `$0|BASH_SOURCE|/proc/self` returns nothing.
* The mutants are killed by the same labels at both revisions: r41's `mutants` block lists
  `killed: true` for M1-M9, H5, H6, H9, H10 at both revisions with R40-C1/R41-C1 `FAIL` labels
  only — no `R44-C1` label appears in any mutant's `first_fails` (grep of the two r41 receipts).

## 3. Why r35b reads 4 of 24 at *both* revisions (pre-existing, pinned, unchanged)

r35b compares every census line except the first and the `DRIFT pacnew-plane` line against the
round-35 claim-base census `b40c01df38eb26f74c095c471efc6d1649b00fd4`
(`tools/score-pacnew-arm-r35b.py:59`, `:407-408`, `judge()` `:426-436`, `base parity` at `:433`).
That census predates rounds 36-43, so the parity leg already fails on the round-42 STORAGE line at
the base revision; the 4 views that match are the three namespace views and the live view, where
the counter passes `base=None` and does not run the parity leg.

Measured, in one stub fixture built by the counter's own `build_fixture`/`harness` helpers
(`C1ExecOtherCounters/parity-diff.txt`):

```
=== others(census@98020ece) vs others(claim-base b40c01df), rc=2 vs 2
+STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0
=== others(census@7e081698) vs others(claim-base b40c01df), rc=2 vs 2
+STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0
+SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0
```

So C1's line is a second, round-44-only unmatched line: it would fail parity on its own even if
the STORAGE line were excused. It changes no verdict because the parity leg already fails in all
20 stub views at base (per-view reasons: `base parity` in stub-00..stub-19 at both revisions;
candidate rows `stub-*` and `ns-2x`/`live` in both receipts). The counter is outside its window at
both revisions and stays out: `SKILL.md:3317` (`historical-pacnew-arm-r35b`) pins it to census
blobs `10b6d470…` only, from `e2f97e6e` through `7cbaeb63`, and records the same measured 0-of-24
at the claim base. Per-view comparison, base vs rev, is identical:

```
('candidate','live')  base=(True,None,2)   rev=(True,None,2)
('candidate','ns-20..22') base=(True,None,2) rev=(True,None,2)
('candidate','stub-00..19') base=(False,'base parity',2) rev=(False,'base parity',2)
```

The small differences in `should_fail_matches` between the two battery runs (F04 6 vs 3, F06 0 vs
1) come from the counter's per-run random fixture seed (`seed = os.urandom(8)`,
`tools/score-pacnew-arm-r35b.py:445`), not from C1: they never approach `of` 24, and
`should_fail_accepted` is 0 and `control_matches` 24 in both receipts. The two `--skip-battery`
runs reproduce `candidate_matches 4` of 24 at both revisions with independent seeds.

## 4. Why r32 is indifferent to the SCRUB line

`parse_output` keeps only `PLANE …` lines, the `TSUKUROI_CENSUS:` rollup and `HANDOFF …` lines
(`tools/score-census-handoff-r32.py:504-513`); the live legs keep only `PLANE oom:`/`PLANE
journal:`, the rollup and the exit code (`:752`). The SCRUB line is therefore outside every
comparison set, and the live rows confirm parity held (`live_consistent: true`, rollup identical,
`unrouted: []`). The new line is verdict-neutral for the rollup as declared: the rollup text is
equal at both revisions in the same scenarios, since the counter compares it line for line.

## 5. Limits and open channels recorded here

1. **r32 does not see the new arm at all.** The SCRUB line is not in its comparison set, so a
   *wrong* SCRUB line would also leave r32 green. That is a property of the counter, not a harm of
   C1; the arm's own coverage is C1's frozen counter.
2. **The new arm reads live paths in "hermetic" fixture views.** `probe_scrub_record` takes its
   defaults `$BTRFS_SYSFS`/`$TIMER_WANTS` (absolute `/sys/fs/btrfs`,
   `/etc/systemd/system/timers.target.wants`) and uses only shell builtins (`[ -d ]`,
   `[ -e ]`, `read`), so it reaches no stubbed command: r32's hermeticity gate (stub-call log plus
   the host/root/package markers, `:624-648`) cannot observe it. On this host `/var/lib/btrfs` is
   absent (`ls: cannot access '/var/lib/btrfs': No such file or directory`), so the line reads
   `dir=absent` and a live `/sys/fs/btrfs` + timer-wants listing. No host write occurred.
3. **r35b cannot be made green by fixture equality** while any census line is added after round
   42, because it requires exact whole-output parity with `b40c01df`; this is why it is pinned.
4. **Not run here** (outside this seat): the C1 frozen counter and its battery, the census
   `--selftest` itself, and any r44 after-receipts; also no `--scenarios` change and no mutation of
   the four counters (they were run unmodified through `run-receipt.py`). r40/r41 were each run
   once per revision, not repeated for flake.
5. Host untouched: read-only `ls`/`git show`/`git rev-parse` only; no sudo, no service, no sysfs
   write, no scrub command, no package action. Scratch
   `/fast/scratch/hyaku/tsukuroi-r44/C1ExecOtherCounters` was removed after the receipts were
   copied here.
