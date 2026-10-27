VERDICT: supports

# Seat C1ExecPriorCounters — item C1-5 (kill rule: frozen predecessor storage counters)

Kill rule, verbatim from the C1 row's last cell (`SCORECARD.md:2760`, round-44 declaration): "any frozen
predecessor storage counter (`score-storage-arm-r38.py`, `-r38-q82.py`, `score-storage-hidden-r39.py`,
`score-size-invariance-r42.py`) FAILs at the measured revision where it PASSes at base".

**Not triggered.** Three of the four PASS at base and PASS at the measured revision with unchanged
verdict-bearing fields; the fourth (`score-storage-arm-r38.py`) FAILs at base *and* at the measured revision
with a body byte-identical apart from the `revision` field, so its antecedent ("PASSes at base") cannot hold.
`score-storage-arm-r38.py` therefore supplies no protective signal this round — recorded as a limit, not harm
(§5).

Base `98020ece0674e0b569ee23aed10ffbee355b248e`; measured `7e081698d4fc3c4ea944884fd093058de9909de1`
(`git merge-base --is-ancestor 98020ece 7e081698` → ancestor, so the pair is a linear base→measured comparison).

## 1. Method

Driver `tools/run-receipt.py` — it runs the tool from a private `git clone --no-local` checked out at the bound
revision, with a fixed child environment (`PATH=/usr/bin:/bin LC_ALL=C`, every `GIT_*` dropped, private `HOME`),
and writes a header/body/footer JSONL receipt naming `revision`, `tool_revision` and `tool_sha256`. Its child env
carries no `TMPDIR`, so `--scratch` was passed explicitly to every counter (all under
`/fast/scratch/hyaku/tsukuroi-r44/C1ExecPriorCounters/s/`; nothing was built or written under `/tmp`).

Runs, one counter at a time. `r42` was given the real lane path (`--lane '{lane}'`) on both legs; the other three
used the driver's default `--repo` (each run's own private clone root, a `--no-local` clone of the lane whose
object DB resolves both revisions), so each pair is internally symmetric:

| # | command (after `python3 .../tools/run-receipt.py --revision <rev> --out <receipt> --`) | wall |
|---|---|---|
| 1 | `tools/score-storage-arm-r38.py --revision '{rev}' --scratch …/s/r38-base` @ base | 30 s |
| 2 | same, `--scratch …/s/r38-meas` @ measured | 28 s |
| 3 | `tools/score-storage-arm-r38-q82.py --revision '{rev}' --scratch …/s/q82-base` @ base | 8 s |
| 4 | same, `--scratch …/s/q82-meas` @ measured | 8 s |
| 5 | `tools/score-storage-hidden-r39.py --revision '{rev}' --scratch …/s/r39-base` @ base | 24 s |
| 6 | same, `--scratch …/s/r39-meas` @ measured | 24 s |
| 7 | `tools/score-size-invariance-r42.py --revision '{rev}' --lane '{lane}' --scratch …/s/r42-base` @ base | 41 s |
| 8 | same, `--scratch …/s/r42-meas` @ measured | 47 s |

The four counters are byte-identical at the two revisions, so the pair isolates the census bytes (git blob ids,
`git rev-parse <rev>:tools/<tool>`):

| tool | blob @ base | blob @ measured | content sha256 (both) |
|---|---|---|---|
| score-storage-arm-r38.py | df214578… | df214578… | e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218 |
| score-storage-arm-r38-q82.py | a3669257… | a3669257… | a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3 |
| score-storage-hidden-r39.py | c502401c… | c502401c… | 75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973 |
| score-size-invariance-r42.py | bf7c16bd… | bf7c16bd… | c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03 |

The census is not identical: blob `18a1db64…` at base vs `f45d0051…` at measured (+177/−1 lines,
`git diff --stat 98020ece 7e081698 -- tools/tsukuroi-census.sh`), so the comparison is not vacuous.

Receipts (sha256), all in `.ufo/waves/round-44/w1/C1ExecPriorCounters/`:
`score-storage-arm-r38.py-98020ece.jsonl` 419276b9…, `…-7e081698.jsonl` 1b402386…;
`score-storage-arm-r38-q82.py-98020ece.jsonl` 6049b36a…, `…-7e081698.jsonl` 3fd396d6…;
`score-storage-hidden-r39.py-98020ece.jsonl` a88da1a2…, `…-7e081698.jsonl` cbbf78a0…;
`score-size-invariance-r42.py-98020ece.jsonl` 33c9b7d9…, `…-7e081698.jsonl` 08304da1….
Machine summary: `prior-counters-summary.json` (02efc6ed…, built by `summarize-pair.py`, exit 0). The three
analysis scripts and that summary are pinned in `scripts-and-summary.sha256` beside the receipts
(`summarize.py`, `summarize-pair.py`, `diff.py`).

## 2. Verdicts

| counter | base | measured | PASS→FAIL? |
|---|---|---|---|
| score-storage-arm-r38.py | FAIL, exit 1, `fixtures_matched 9/10`, live 1, six 1 | FAIL, exit 1, `fixtures_matched 9/10`, live 1, six 1 | no (FAIL at base) |
| score-storage-arm-r38-q82.py | PASS, exit 0, `ns_views_matched 3/3`, `ns_available 1` | PASS, exit 0, `ns_views_matched 3/3`, `ns_available 1` | no |
| score-storage-hidden-r39.py | PASS, exit 0, hidden 2/2, views 3/3, fixtures 5/5, live 1, six 1 | PASS, exit 0, hidden 2/2, views 3/3, fixtures 5/5, live 1, six 1 | no |
| score-size-invariance-r42.py | PASS, exit 0, `cases 10`, `invariant 10`, `ns_invariant 3`, `selftest_pass 1`, `default_equal 1` | PASS, exit 0, same five fields; `selftest_label "PASS (132 …)"` → `"PASS (141 cases, 141 passed, 0 failed)"` | no |

## 3. Changed fields, base → measured (full leaf diff of the receipt bodies)

- **score-storage-arm-r38.py — 1 changed leaf, 0 behavioural.** Only `revision`. Bodies are byte-identical
  after dropping `revision` (`json.dumps(..., sort_keys=True)` comparison → `True`); the same nine fixtures
  match, `F06-no-btrfs-root` returns `['BLOCKED', 0, 0, 0]` at both revisions, the live leg is
  `HEALTHY 1/1/0`, `census_exit 2`, `six_planes_all 1`, `euid_root false` at both.
- **score-storage-arm-r38-q82.py — 19 changed leaves,** `revision` + `seed` (`6bf94c73…` → `f11209fc…`) and 17
  leaves inside `views[0..2].expected/got/storage_lines`. The views are drawn per run — `seed = os.urandom(16)`
  (`tools/score-storage-arm-r38-q82.py:110`) feeding trees of "1-3 filesystems, 1-3 devices each, every counter 0
  or a random 1-99999 value" (its docstring, `:11`) — so the differing numbers are new draws, not a behaviour
  change. Within each run every view is self-consistent: `match` `[true,true,true]` and `expected == got` at both
  revisions.
- **score-storage-hidden-r39.py — 12 changed leaves,** `revision` + `seed` (`b66ff25e…` → `3c343c85…`, same
  `os.urandom(16)` draw at `tools/score-storage-hidden-r39.py:213`) and 10 inside `views[0..2]`. Same reading:
  each run has `expected == got` for all three views, and `hidden` 2/2, `views` 3/3, `fixtures` 5/5, `live` and
  `six_planes_all 1` are unchanged; the live `got` string is byte-identical at both revisions —
  `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`.
- **score-size-invariance-r42.py — 9 changed leaves:** `revision`, the per-process `token`
  (`75f12c67fbb2` → `964c30cc0035`, `TOKEN = os.urandom(6).hex()`, `tools/score-size-invariance-r42.py:176`),
  the six `ns_cases.N1/N3/N6.{small,large}` strings (they differ *only* by that token — after substituting each
  run's token the two bodies are identical), and `selftest_label` `PASS (132 cases, 132 passed, 0 failed)` →
  `PASS (141 cases, 141 passed, 0 failed)`, i.e. exactly the nine declared `R44-C1` selftest cases
  (132 → 141). `cases`, `invariant`, `ns_invariant`, `selftest_pass`, `default_equal`, `base` (`c8efaa3f…`
  census pin) and every `per_case` entry are unchanged.

## 4. Why this supports C1

- The only predecessor field that moved for a semantic reason is r42's selftest case count, and it moved in the
  direction C1 declares (132 → 141, nine `(R44-C1)` cases), with `selftest_pass 1` and `selftest_rc 0`.
- No predecessor's STORAGE reading degraded: r38 keeps the same nine fixture `STORAGE` lines with `match true`
  and the same live line; r39 keeps all five fixture lines and all three namespace views; the q82 namespace views
  stay 3/3. The new `SCRUB` line is printed between `STORAGE` and the rollup and is invisible to all four parsers
  by construction — r38/r39 select only `^STORAGE btrfs-device-stats …` (`tools/score-storage-arm-r38.py:55`,
  `tools/score-storage-hidden-r39.py:58`) and r42 keeps only `PLANE `/`TSUKUROI_CENSUS:` lines plus the exit code
  (`tools/score-size-invariance-r42.py:213-215`); the observed values confirm it.
- Every run at both revisions still printed exactly six `PLANE` lines and one rollup (`six_planes_all 1`), and
  the live census exit code is 2 at both revisions (r38 `live.census_exit 2`, r39 live leg matched).

## 5. Limits and what I did not do

- **r38's FAIL is pre-existing and declared, not a C1 effect.** `SCORECARD.md:2232-2235`: the v1 counter's F06
  "encodes the superseded R38-ABSENT-ROOT rule, so at post-C1 revisions it reads BLOCKED and
  `score-storage-arm-r38.py` FAILs 9/10 by construction"; the observation was recorded in round 39
  (`.ufo/waves/round-39/w1/C1ExecR38Counters.md:40-54`). My two runs measure the identical body, so no
  attribution to `7e081698` is possible. Consequence to record: this counter can neither pass nor falsify this
  round's kill rule — the live guard is carried by the q82/r39/r42 trio.
- I did not run the round-44 C1 counter, the census selftest, or any census gate (other seats own those); the
  "132 cases" / "141 cases" labels above are what the r42 counter itself observed at each revision.
- The kill rule's other two clauses (a live `PLANE`/rollup/exit-code change on the live host; the arm creating a
  file in live mode) are outside this item. My runs give only supporting readings, not the authoritative
  measurement: the live `STORAGE` line and the live census exit code are unchanged at the two revisions.
- Read-only on the host throughout: no package, service, timer, sysfs, mount (outside the counters' own
  unprivileged namespaces), `/etc` or `/var/lib` write; no sudo; no `btrfs scrub` command; no `systemctl` verb.
  Nothing was written in the lane or the fleet repo except this report and my receipt directory.
- No tools were installed or upgraded; no `/tmp` path is used as evidence (explicit `--scratch` on every run,
  scratch removed).
