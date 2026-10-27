VERDICT: supports

# C1ExecPriorA — item C1-5 (kill rule: counters A)

Kill-rule question: does `tools/score-census-readers-r45.py`, `tools/score-scrub-arm-r44.py` or
`tools/score-bootinputs-r43.py` go PASS->FAIL between base `2042117cfb724170772f4c128cc2ddba0b61d817`
and implementation `a44770491eb5ca15ce9f8b3207309d1af683ffaf`? **No.** All three are PASS at the
implementation revision I graded, and none is PASS at base -> FAIL at IMPL. One base attempt of
`score-census-readers-r45` returned FAIL on a single census-selftest case that did not reproduce in
eleven later observations of the same base bytes; the base rerun of the same counter is PASS.

## Method

Each counter ran through the frozen driver, from a private `--no-local` sandbox clone at the named
revision, one counter at a time, `TMPDIR=/fast/scratch/hyaku/tsukuroi-r46/C1ExecPriorA`,
`--scratch /fast/scratch/hyaku/tsukuroi-r46/C1ExecPriorA/s`, receipts under
`.ufo/waves/round-46/w1/C1ExecPriorA/`:

```
python3 <lane>/tools/run-receipt.py --revision <REV> --lane <lane> --timeout 1800 \
  --out .ufo/waves/round-46/w1/C1ExecPriorA/<tool>-<rev8>.jsonl \
  -- tools/<counter>.py --revision <REV> --scratch /fast/scratch/hyaku/tsukuroi-r46/C1ExecPriorA/s
```

Receipt files (7), each header names the run revision and the counter sha256, each footer the exit:

| receipt | counter sha256 (prefix) | exit | timed_out | finished_utc |
|---|---|---|---|---|
| `score-census-readers-r45-2042117c.jsonl` | `fe0e31e25c5b3c92` | 1 | false | 2026-10-27T05:30:56Z |
| `score-census-readers-r45-2042117c-rerun.jsonl` | `fe0e31e25c5b3c92` | 0 | false | 2026-10-27T05:48:51Z |
| `score-census-readers-r45-a4477049.jsonl` | `fe0e31e25c5b3c92` | 0 | false | 2026-10-27T05:35:29Z |
| `score-scrub-arm-r44-2042117c.jsonl` | `1409a5fd75adaa4c` | 0 | false | 2026-10-27T05:38:42Z |
| `score-scrub-arm-r44-a4477049.jsonl` | `1409a5fd75adaa4c` | 0 | false | 2026-10-27T05:39:19Z |
| `score-bootinputs-r43-2042117c.jsonl` | `886f92c8cd58e52e` | 0 | false | 2026-10-27T05:39:28Z |
| `score-bootinputs-r43-a4477049.jsonl` | `886f92c8cd58e52e` | 0 | false | 2026-10-27T05:39:31Z |

Both counters I cite as frozen (`score-scrub-arm-r44`, `score-bootinputs-r43`) carry the same
`tool_sha256` at base and at IMPL, i.e. the tool did not change inside the round; `git diff --stat
2042117c a4477049 -- tools/` lists only `tools/tsukuroi-census.sh` (+121/-4) plus the two round-46
counters (`tools/score-census-identity-r46.py`, `tools/check-scrub-admission-r46.py`), so the census
is the only tool these three counters read that the round touched.

## Verdicts

- `score-scrub-arm-r44`: base **PASS**, IMPL **PASS**. Base: `cases 16, correct 16, identity_ok 1,
  wired_ok 1, live_agree 1, selftest_pass 1, selftest_r44 16, selftest_failures []`; IMPL the same
  values. Live string identical on both sides:
  `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`.
- `score-bootinputs-r43`: base **PASS**, IMPL **PASS**, fields identical apart from `revision`:
  `cases 16, correct 16, identity_ok 1, live_agree 1, live {"expect":"0","got":"0","rc":0},
  selftest_pass 1, selftest_r43 4, selftest_line "TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=49 failed=0"`.
  `btime 1793027300` is the same on both sides (one boot).
- `score-census-readers-r45`: base **PASS** (rerun) / one earlier base attempt **FAIL**, IMPL **PASS**.

## Every changed field (base -> IMPL)

`score-census-readers-r45` (receipt `-2042117c-rerun` -> `-a4477049`):

| field | base | IMPL |
|---|---|---|
| `revision` | `2042117cfb724170772f4c128cc2ddba0b61d817` | `a44770491eb5ca15ce9f8b3207309d1af683ffaf` |
| `census_sha256` | `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc` | `d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa` |
| `seed` | `8771ebffc5ea43c6` | `1ff541c8baa24e1b` |
| `selftest_line` | `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)` | `TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)` |

Unchanged in that counter: `verdict PASS`, `lexical_hits 0`, `sites_found 5`, `equiv_ok 5`,
`revert_killed 6` (all six mutants `killed: true`, `r45_fail_lines 1`), `selftest_pass 1`,
`selftest_r45 6`, `selftest_timed_out false`, `adjacency {status PASS, exit 0, findings [],
bytes_base true}` and every `per_site` line (`S1 965`, `S2 1003`, `S3 1085`, `S4 1460`, `S5 1535`,
each `draws 8, mismatches 0`).

`score-scrub-arm-r44`: only `revision`, `selftest_line` (154->160 cases) and the drawn fixture pair
`wired.got`/`wired.want` differ. `wired` is a random draw per run, not a revision difference: base
drew `... records=0 tmp=2 ... unreadable=2 ... limited=1 timers=1 detail=1d02a454:38:speed_max=31461844`
with `rc 2`, IMPL drew `... records=1 tmp=1 ... unreadable=1 orphan=1 limited=2 timers=2
detail=1d02a454:17:speed_max=69072958,d5bf085e:39:speed_max=14318804` with `rc 2`, and
`wired_ok`/`live_agree` are 1 on both. Everything else (`cases 16`, `correct 16`, `identity
["1000","1000","1000"]`, `identity_ok 1`, `live`, `wrong []`, `selftest_failures []`) is identical.

`score-bootinputs-r43`: only `revision`.

## Why the census selftest line changed by six cases

`git diff --stat 2042117c a4477049 -- tools/tsukuroi-census.sh` = `121 insertions(+), 4 deletions(-)`;
the added block is the `--identity` arm and its self-test, `tools/tsukuroi-census.sh:3384` ("---- round
46 (C1): --identity ... ----") through the six `(R46-C1)` checks ending `tools/tsukuroi-census.sh:3459`
(`cli: --identity with --help exits 2, never usage and 0 (R46-C1)`), before the unchanged summary
printf at `tools/tsukuroi-census.sh:3462`. 154 -> 160 is exactly +6. The R45 case set is otherwise
untouched: `selftest_r45 6` before and after, all five reader sites at their base lines (`per_site`
identical), and all six reader-revert mutants still killed.

## The one base FAIL: single-case flake, not reproduced

Receipt `score-census-readers-r45-2042117c.jsonl` (seed `ff26321d8d4c3803`, finished
2026-10-27T05:30:56Z) reads `verdict FAIL`, `selftest_pass 0`, `selftest_line
"TSUKUROI_CENSUS_SELFTEST: FAIL (154 cases, 153 passed, 1 failed)"`, with every other leg nominal
(`lexical_hits 0`, `sites_found 5`, `equiv_ok 5`, `revert_killed 6`, `adjacency PASS`). That base
census is byte-identical to round-45's graded bytes rather than to anything round 46 made: its
`census_sha256 237b21c9…b5fcdc` equals `census_sha256` in `.ufo/waves/round-45/after/c1-final-44560592.jsonl`
(PASS, `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)`) and in
`.ufo/waves/round-45/after/c1-check-194a4523.jsonl` (PASS).

The same base bytes then passed the census selftest in eleven later observations:

1. direct run of the base checkout (`bash tools/tsukuroi-census.sh --selftest`, cwd/TMPDIR in scratch):
   `rc=0`, 154 `PASS` lines, `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)`
   — full output kept as `base-selftest-direct-2042117c.stdout.txt` (157 lines, stderr empty);
2. eight iterations of a copy of the counter's own `selftest()` call (`cwd=tmp`, `TMPDIR=tmp`,
   `LC_ALL=C`, `TSUKUROI_*`/`UFO_*` stripped, `stdin` closed, `start_new_session`), driver
   `probe_selftest.py`: `iter 0..7 rc=0 PASS (154 cases, 154 passed, 0 failed)`;
3. `score-scrub-arm-r44-2042117c.jsonl`: `selftest_pass 1`, `selftest_failures []`,
   `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)` (same base census, same run
   environment — that counter extracts and keeps FAIL lines, `tools/score-scrub-arm-r44.py:628`);
4. `score-census-readers-r45-2042117c-rerun.jsonl` (seed `8771ebffc5ea43c6`): `verdict PASS`,
   `selftest_line "…PASS (154 cases, 154 passed, 0 failed)"`, exit 0.

So base is PASS->PASS against IMPL on this counter, and the single base FAIL is a one-in-twelve
occurrence under a host load average of 36 (`uptime` at 2026-10-27 02:37 local: `load average:
14.61, 22.86, 36.44`; the failing run started around 05:16Z, in that band).

What I cannot state: **which** case failed. The round-45 counter keeps only the summary line
(`tools/score-census-readers-r45.py:288-290` extracts `SUMMARY_RE`, `:335` emits `selftest_line` and
`selftest_pass` and no failure list), unlike `score-scrub-arm-r44.py:628` and
`score-bootinputs-r43.py:341`, which both keep `selftest_failures` and both reported `[]` at base and
at IMPL. That is a receipt-completeness gap in the round-45 counter (pre-existing, not caused by this
round); it is the reason the flake cannot be attributed to a named case after the fact.

## Adjacency leg

The `score-census-readers-r45` adjacency leg ran, it did not refuse: both base receipts and the IMPL
receipt read
`"adjacency": {"status": "PASS", "exit": 0, "findings": [], "bytes_base": true}`, `adjacency_ok 1`.
The driver's `--no-local` clone carries the lane's refs, so `refs/heads/master` =
`refs/remotes/origin/master` = `a44770491eb5ca15ce9f8b3207309d1af683ffaf` (receipt header
`lane_branches` records `refs/heads/master a44770491eb5…`), and base `2042117c…` is an ancestor of
it; the revision-binding leg of `tools/_revision.py` therefore resolved without the origin/master
workaround the item anticipated. No ref was created or moved (read-only clone, `git clone --no-local`
from the lane).

## Findings for the L1

1. Kill rule does not fire: `score-scrub-arm-r44` PASS->PASS, `score-bootinputs-r43` PASS->PASS,
   `score-census-readers-r45` FAIL(flaked)/PASS->PASS against IMPL PASS. The R46 census edit adds six
   selftest cases and moves no reader site, keeps `selftest_r45 6`, keeps all six revert mutants
   killed, and keeps the adjacency leg PASS.
2. Pre-existing receipt gap (round-45 counter, out of this round's scope to fix): a census selftest
   failure at `score-census-readers-r45` is unnameable from its receipt because only the summary line
   is retained (`tools/score-census-readers-r45.py:288-290`, `:335`).
3. Load sensitivity: the census selftest flaked once (1 of 154 cases) at load average ~36 and not in
   11 later runs at load 14-30. Anyone re-running this counter at base on a loaded host may see the
   same single-case FAIL; it is not a revision property.

## Limits of this report

- I ran no builds, linters, formatters or the round's own counters (`score-census-identity-r46.py`,
  `check-scrub-admission-r46.py`); the round is still in its editing wave and the parent owns the
  gate. The three counters above are the whole of this item.
- I installed or upgraded no tool (pacman transactions are paused host-wide; nothing needed).
- I wrote only `.ufo/waves/round-46/w1/C1ExecPriorA/` (this report plus seven receipts) and my scratch
  `/fast/scratch/hyaku/tsukuroi-r46/C1ExecPriorA/`, which I removed after copying receipts out.
- No host mutation: only read-only queries were used (`git show`/`rev-parse` in the lane and clones,
  `sha256sum`, the sandboxed counters). No service, unit, sysfs, mount, package or scrub action.
- Landing state while I wrote this: the integrator committed the first six receipts (both revisions of
  all three counters) at `b313963c` ("wave w1/r1 evidence") and the lane HEAD was `102cf670`
  ("kill-rule receipts so far"). Still untracked as of this report: this file,
  `score-census-readers-r45-2042117c-rerun.jsonl`, `base-selftest-direct-2042117c.stdout.txt`,
  `probe_selftest.py`. The base FAIL receipt
  (`score-census-readers-r45-2042117c.jsonl`, landed in `b313963c`) must be read together with the
  PASS rerun beside it, or the round's kill rule will look fired when it is not.
