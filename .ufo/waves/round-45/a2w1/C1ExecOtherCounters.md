VERDICT: no-finding

Item C1-7 (no-harm, milestone `other census counters`). Lane
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, base `5bbd5ff588120fd8e7c744695351a6978b4241c1`
(lane tip at round start), implementation `18389f44cf6ce414d7be205998b29c79fb0b490c`.

All four counters were run unmodified, one at a time, through `tools/run-receipt.py` (private
`git clone --no-local` sandbox detached at the named revision) at *both* revisions. **No verdict
changes.** Every predicate field that defines a verdict is equal at the two revisions; the only
differences observed are (a) the census selftest case total 148 -> 154, which r40/r41 handle by
construction, (b) a per-run random fixture seed inside r35b's battery, and (c) live-host counters
inside r32's non-compared PLANE notes. The six new `(R45-C1)` selftest cases are on the path of
r40 and r41 only (the two counters that run `--selftest`); they pass in the baseline 154/154 at the
implementation and change no mutant attribution. r32 and r35b never invoke `--selftest`
(`grep -n selftest tools/score-census-handoff-r32.py tools/score-pacnew-arm-r35b.py` -> no match),
so the six cases cannot reach those two counters at all.

Receipts (each a `run-receipt.py` JSON-lines receipt whose header names the revision, the tool and
its sha256), in `.ufo/waves/round-45/a2w1/C1ExecOtherCounters/`:

`r32-base.jsonl`, `r32-rev.jsonl`, `r35b-base.jsonl`, `r35b-rev.jsonl`,
`r35b-skipbattery-base.jsonl`, `r35b-skipbattery-rev.jsonl`, `r40-base.jsonl`, `r40-rev.jsonl`,
`r41-base.jsonl`, `r41-rev.jsonl`, plus `parity.txt` (the per-row comparisons quoted below, computed
from the receipts) and `observed-summary.txt` (header/footer fields per receipt).

Tool identity: each counter's `tool_sha256` in the receipt header is identical at both revisions
(r32 `61fb2ec2…`, r35b `7517af92…`, r40 `8b06de18…`, r41 `8306d999…`), i.e. the four counters are
unchanged by the implementation; the census is not (`git show` -> sha256 base
`17c82406fe7a7d06261b1fb2ac4be56e7d5498c6712ae90fe8233d2bb0e81a35`, impl
`237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc`), so the runs really did
execute two different censuses.

Exact commands (one shape per counter; `{rev}`/`{lane}` are `run-receipt.py` substitutions; the
receipt header records the expanded argv, e.g. `r32-base.jsonl` line 1):

```
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/run-receipt.py \
  --revision <REV> --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --timeout <T> \
  --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-45/a2w1/C1ExecOtherCounters/<tag>.jsonl \
  -- tools/score-census-handoff-r32.py --revision '{rev}' --lane '{lane}' \
     --scratch /fast/scratch/hyaku/tsukuroi-r45/C1ExecOtherCounters/s/<tag> --seed d26bdc2550f2b04f
python3 .../run-receipt.py --revision <REV> --lane <lane> --timeout 3000 --out <seat>/r35b-<tag>.jsonl \
  -- tools/score-pacnew-arm-r35b.py --lane '{lane}' --revision '{rev}' [--skip-battery]
python3 .../run-receipt.py --revision <REV> --lane <lane> --timeout 2400 --out <seat>/r40-<tag>.jsonl \
  -- tools/score-selftest-literals-r40.py --revision '{rev}' --repo '{lane}' \
     --scratch /fast/scratch/hyaku/tsukuroi-r45/C1ExecOtherCounters/s/r40-<tag> --jobs 4
python3 .../run-receipt.py --revision <REV> --lane <lane> --timeout 2400 --out <seat>/r41-<tag>.jsonl \
  -- tools/score-selftest-mounts-r41.py --revision '{rev}' --repo '{lane}' \
     --scratch /fast/scratch/hyaku/tsukuroi-r45/C1ExecOtherCounters/s/r41-<tag> --jobs 4
```

Wall clock observed (receipt header `started_utc` -> footer `finished_utc`): r32 17 s / 19 s,
r35b 38 s / 46 s (battery) and 5 s / 4 s (`--skip-battery`), r40 2 m 43 s / 3 m 7 s, r41 5 m 27 s /
4 m 33 s. No run timed out (`timed_out: false` in every footer); no variant was retried (no
`retried` key).

## 1. Result table (observed, from the receipts)

| Counter | base `5bbd5ff5` | impl `18389f44` | change |
|---|---|---|---|
| `score-census-handoff-r32.py` | `routed 24` of 24, `live_consistent true`, `harness_errors 0`, exit 0 | same, exit 0 | none |
| `score-pacnew-arm-r35b.py` (battery) | `candidate_matches 4`, `of 24`, `control_matches 24`, `should_fail_accepted 0`, exit 1 | same, exit 1 | none |
| `score-pacnew-arm-r35b.py` (`--skip-battery`) | `candidate_matches 4`, `of 24`, exit 1 | same, exit 1 | none |
| `score-selftest-literals-r40.py` | `PASS`, `baseline_pass 1`, `neutral_pass 3`, `mutants_applied 9`, `survivors 0`, `selfref 5`, baseline `PASS (148 cases, 148 passed, 0 failed)`, exit 0 | `PASS`, same fields, baseline `PASS (154 cases, 154 passed, 0 failed)`, exit 0 | none (case total only) |
| `score-selftest-mounts-r41.py` | `PASS`, `baseline_pass 1`, `neutral_pass 3`, `decoy_pass 1`, `mutants_applied 13`, `survivors 0`, `params 4`, baseline 148 cases, exit 0 | `PASS`, same fields, baseline 154 cases, exit 0 | none (case total only) |

## 2. r40 literals counter — PASS at both, six new cases pass inside the baseline

`r40-base.jsonl` / `r40-rev.jsonl`, the single pretty-printed record between header and footer:
`"predicate": "baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and
survivors == 0 and selfref == 5"`, `"result": "PASS"`, `"exit": 0` in both.

* Baseline: `PASS (148 cases, 148 passed, 0 failed)` (base) and `PASS (154 cases, 154 passed,
  0 failed)` (impl) — the six `(R45-C1)` cases are among the 154 and pass.
* `mutants_applied 9`, `survivors 0`, `survivor_names []` both; all nine kill with a nonzero exit.
  Per-mutant FAIL summaries differ only in the case total, with an identical number of failing
  cases (base -> impl): M1 6 -> 6, M2 5 -> 5, M3 1 -> 1, M4 5 -> 5, M5 1 -> 1, M6 1 -> 1,
  M7 1 -> 1, M8 5 -> 5, M9 2 -> 2 (verbatim lines in `parity.txt` §r40). 148-6=142/154-6=148 etc.
* `selfref 5` at both. The r40 self-reference regex
  `\$\{?SELF|BASH_SOURCE|\$0\b|/proc/self/(exe|fd)|/proc/\$\$` (`tools/score-selftest-literals-r40.py:53-54`)
  matches 5 census lines at both revisions:
  `grep -cE '\$\{?SELF|BASH_SOURCE|\$0\b|/proc/self/(exe|fd)|/proc/\$\$'` -> `5`, `5` on
  `git show 5bbd5ff:tools/tsukuroi-census.sh` and `git show 18389f4:tools/tsukuroi-census.sh`.
  The census diff is six hunks, 49 added / 5 deleted lines (`git diff --numstat 5bbd5ff 18389f4 --
  tools/tsukuroi-census.sh` -> `49 5`): five one-line reader replacements (`@@ -965 +965 @@`
  probe_systemd state, `-1003` timer Result, `-1085` nvidia-smi driver, `-1460` boot-target word,
  `-1535` timer ActiveState) and one `@@ -3332,0 +3333,44 @@` block of six selftest cases inside
  `run_selftest`; neither adds a self-read.
* `neutral_pass 3` (N1/N2/N3 each exit 0 with `PASS (148…)`/`PASS (154…)` respectively).

## 3. r41 mounts counter — PASS at both, same 13 kills with the same labels

`r41-base.jsonl` / `r41-rev.jsonl`: `"predicate": "baseline_pass == 1 and neutral_pass == 3 and
decoy_pass == 1 and mutants_applied == 13 and survivors == 0 and params == 4"`, `"result": "PASS"`,
`"exit": 0`, `params 4`, `capture_pass 1` in both.

* Baseline `PASS (148 cases…)` -> `PASS (154 cases…)`; `baseline_labels` 148 -> 154.
* All 13 mutants (M1-M9, H5, H6, H9, H10) killed at both, and the set of failing selftest labels
  extracted from each mutant's `first_fails` is **identical for 13/13** (`parity.txt` §r41). No
  mutant's `first_fails` names an `R45` label, i.e. the six new cases neither kill nor rescue a
  mutant; they are inside the baseline.
* `params 4` rests on the same four `param_cases`, byte-identical at both revisions
  (`P1-mountpoint-not-absolute`, `P2-source-not-dev`, `P3-no-subvol-option`, `P4-two-btrfs-lines`,
  all resolved to the `(R41-C1 H5/H6/H9/H10)` labels).
* `decoy_pass`: `D-all-mutant-texts` exits 0 and PASSes at both; neutrals N1/N2/N3 PASS at both.

## 4. r32 handoff counter — 24/24 routed, 24/24 scenario rows byte-identical

`r32-base.jsonl` / `r32-rev.jsonl`, same seed `d26bdc2550f2b04f` in both (replayed scenarios are
the same 24). Summary rows: `"routed": 24, "scenarios": 24, "unrouted": [], "live_consistent":
true, "harness_errors": 0`, `scenarios_per_type {"both":4,"coredumps":4,"cumulative+coredumps":2,
"cumulative-only":3,"kill-events":5,"none":3,"tsukuroi-only":3}`, exit 0, at both.

* Per-scenario rows: 24/24 **identical field for field** between the two receipts (`parity.txt`
  §r32 — comparison excludes only the `revision` field and the `runtime_s` summary field).
  `plane_parity` true in 24/24 at both revisions, `base_rollup == rev_rollup` and `base_rc ==
  rev_rc` in 24/24. Since r32 compares the rev census's six PLANE lines, rollup and exit code
  against the census at the round-32 claim base (`"base": "58cc2e0b…"` in the summary row; the
  comparison expression is `tools/score-census-handoff-r32.py:978-981` and the per-scenario runs
  are at `:936-960`), this is direct evidence that the rewritten `probe_systemd` `state`,
  `probe_drivers` `driver` and `probe_journal` `t_word` readers produce byte-identical PLANE text
  on all 24 fixtures.
* The live row is the only row that differs, inside `PLANE drivers:` fields the counter itself
  excludes from live comparison: `"live parity: the oom and journal PLANE lines, the rollup line
  (every plane verdict) and the exit code; the other four PLANE notes carry live counters (cgroup
  sweep, memory pressure) that change between two back-to-back runs, so their text is not compared
  live"` (`tools/score-census-handoff-r32.py:748-753`). `consistent` is true in both views in both
  receipts, `filter_k 2`, and both live views settled on attempt 1 (no retry).
* That residue is host drift, not a revision effect: within a single revision two back-to-back runs
  of the same scripts differ in the same fields. Measured (`parity.txt` §r32 live): plain view,
  impl revision, base-script run vs rev-script run `C6_psi_full_total_us` `71180999` vs `71181001`;
  filtered view, base revision, `71163633` vs `71163677`; `C6_avail_kb` differs within the base
  revision's plain pair (`19042672` vs `19205596`).

## 5. r35b pacnew counter — 4 of 24 and exit 1 at both, identical per-view rows

`r35b-base.jsonl` / `r35b-rev.jsonl` (battery) and the two `--skip-battery` receipts: summary
`{"candidate_matches": 4, "of": 24, "control_matches": 24, "should_fail": 17,
"should_fail_accepted": 0, "accepted": [], "harness_errors": []}` and exit 1 in both battery runs;
`{"candidate_matches": 4, "of": 24, "exit_code": 1}` in both skip runs.

* Candidate rows are identical view for view (24/24) in both modes: the four passing views are
  `ns-20`, `ns-21`, `ns-22` and `live`; all 20 stub views fail with reason `base parity` — the
  pre-existing round-35 claim-base parity leg (`b40c01df…`), exactly as the counter is pinned
  (`parity.txt` §r35b). No `R45-C1` line exists in the census (the round only changes readers and
  the selftest), so nothing new enters this counter's parity set either.
* The battery's `should_fail_matches` differ between the two runs in F04 (5 vs 8) and F09 (8 vs 9)
  only; these are 0-accepted shadow arms of 17 whose counts come from the counter's per-run
  `seed = os.urandom(8)` fixture generator (`tools/score-pacnew-arm-r35b.py:445`), they never
  approach `of` 24, and `should_fail_accepted` is 0 in both. Not a verdict field.
* Live view: exit 2 and `matches: true` in both revisions; `harness_errors` empty, so the live host
  reading was unchanged across the runs (the counter re-reads the host log and refuses otherwise,
  `tools/score-pacnew-arm-r35b.py:523-527`). No census file was written by the runs I observed.

## 6. Limits and channels I did not close

1. r32 and r35b never run `--selftest`, so they are structurally blind to the six new cases (and to
   the selftest entirely); my statement about them is about the five readers' output, not about the
   new cases.
2. r32's fixtures feed single-line stub outputs, so its 24/24 parity shows equality for first-line
   values only. It cannot distinguish the old `printf | head -n1` form from the new parameter
   expansion on an output past the pipe buffer — that surface belongs to C1's own frozen counter,
   not to this item.
3. `run-receipt.py` builds a fixed child environment (`tools/run-receipt.py:38-42`: `PATH`,
   `LC_ALL`, the three `GIT_CONFIG_*` variables; `HOME`/`XDG_CONFIG_HOME` added) and therefore
   cannot carry `TMPDIR` into the tool. The tools' own `tempfile.mkdtemp` trees (and r35b's
   fixture trees) were consequently created under `/tmp` by the tools themselves; my `--scratch`
   trees were under `/fast/scratch/hyaku/tsukuroi-r45/C1ExecOtherCounters/s`. Nothing of mine was
   built or kept in `/tmp`.
4. Not run, by design: the C1 frozen counter `score-census-readers-r45.py` and its battery, the
   C2 counter, and any mutation of the four counters (they were run unmodified). r40/r41 were run
   once per revision, not repeated for flake; no timeout, retry or harness error appeared, so no
   repeat was indicated.
5. Host untouched: read-only `git show`/`git cat-file`/`grep`/`python3` only; no package action, no
   service or unit command, no sysfs write, no scrub/replace command, no sudo, no PATH-directory
   write. No tool was installed or upgraded. Scratch `/fast/scratch/hyaku/tsukuroi-r45/
   C1ExecOtherCounters` was removed after the receipts and the two derived text files were written
   here.
