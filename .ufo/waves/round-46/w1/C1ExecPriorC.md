VERDICT: no-finding

# Seat C1ExecPriorC — item C1-7 (kill rule: predecessor C1 counters C)

Kill rule, as the item words it: the C1 kill rule also covers `tools/score-storage-hidden-r39.py`,
`tools/score-storage-arm-r38-q82.py`, `tools/score-pacnew-arm-r35b.py` and `tools/score-census-handoff-r32.py`
(each must not go PASS->FAIL base -> IMPL); `tools/score-storage-arm-r38.py` FAILs at base and is outside the
kill universe, reported anyway.

**Not triggered.** All ten runs completed with the base verdict reproduced at IMPL, and the only fields that
change between the two legs are the random seeds/views each counter draws per run (and, for the `FAIL` counters,
no verdict-bearing field at all). No counter flips, so no kill condition from this item fires.

Base `2042117cfb724170772f4c128cc2ddba0b61d817`; IMPL `a44770491eb5ca15ce9f8b3207309d1af683ffaf`
(`git merge-base --is-ancestor 2042117c a4477049` -> exit 0, so this is a linear base->IMPL pair).

## 1. Result table (observed, 10/10 runs through `tools/run-receipt.py`)

| Counter | base `2042117c` | IMPL `a4477049` | base verdict | IMPL verdict | changed fields |
|---|---|---|---|---|---|
| `score-storage-hidden-r39.py` | exit 0 | exit 0 | PASS (`hidden_matched 2`, `views_matched 3`, `fixtures_matched 5`, `live_match 1`, `six_planes_all 1`) | PASS (same five values) | `seed` only (fresh per run) |
| `score-storage-arm-r38-q82.py` | exit 0 | exit 0 | PASS (`ns_views_matched 3`, `views_expected 3`, `ns_available 1`) | PASS (same three values) | `seed` + the random view trees |
| `score-pacnew-arm-r35b.py` (battery) | exit 1 | exit 1 | FAIL (`candidate_matches 4` / `of 24`, `control_matches 24`, `should_fail 17`, `should_fail_accepted 0`, `harness_errors []`) | FAIL (same six values) | fresh random views; `census_sha256` |
| `score-census-handoff-r32.py` | exit 0 | exit 0 | PASS (`routed 24` / `scenarios 24`, `live_consistent true`, `harness_errors 0`, `unrouted []`) | PASS (same values) | `runtime_s` only |
| `score-storage-arm-r38.py` (outside the universe) | exit 1 | exit 1 | FAIL (`fixtures_matched 9` / `fixtures_expected 10`, `live_match 1`, `six_planes_all 1`) | FAIL (same three values) | `revision` field only (whole body byte-identical; see §3) |

No receipt has `timed_out: true`; every footer is `"stderr_tail": ""`.

## 2. Method

Driver `tools/run-receipt.py` (`tools/run-receipt.py:1-30,101-118`): the tool is read from the bound revision's
tracked bytes, run from a private `git clone --no-local` checked out at that revision (`--tool-revision`
defaults to `--revision`, and the five tools are byte-identical at both revisions, so both legs run the same
tool bytes), with `PATH=/usr/bin:/bin LC_ALL=C`, `GIT_CONFIG*` disabled and a private `HOME`.

The five counters are identical blobs at both revisions; only the census moves (so each pair isolates the
census change):

| tool | blob id (both revisions) | receipt `tool_sha256` |
|---|---|---|
| `tools/score-storage-arm-r38.py` | `df214578de1316820e3ccefbada56246c033b790` | `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218` |
| `tools/score-storage-arm-r38-q82.py` | `a366925759b5ff324f6f099f9b963c4b8c072ce9` | `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3` |
| `tools/score-storage-hidden-r39.py` | `c502401cfa185ab80bd04728cdc7ce80f22552fa` | `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973` |
| `tools/score-census-handoff-r32.py` | `e480851f17b5c661e4d8cf3f19a9759f3bbf6f1a` | `61fb2ec2e622f1aab55ad98710e0cabdebc5bd3ae547ac8ccdbd220a51f73750` |
| `tools/score-pacnew-arm-r35b.py` | `d29520f6f8aaf5d0f5765f18cc62bf23aba86e1e` | `7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1` |
| `tools/tsukuroi-census.sh` (the input under test) | base `f129a18e19106ea4fe7927dc4191477fbfc4077c`, IMPL `412d0a4f7b2c76c6f82416350bef89ae85428933` | sha256 base `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc`, IMPL `d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa` |

(The census sha256 values are the ones the counters themselves print as `census_sha256` in the r35b receipts,
cross-checked with `git show <rev>:tools/tsukuroi-census.sh | sha256sum`.)

Exact commands (one pair shown; every run used its own `--scratch` and its own `--out`; `L` = lane,
`S` = the seat scratch under `/fast/scratch/hyaku/tsukuroi-r46/C1ExecPriorC/s`):

```
python3 $L/tools/run-receipt.py --revision <REV> --out $O/r39-<tag>.jsonl --lane $L --timeout 900 -- \
  tools/score-storage-hidden-r39.py --revision '{rev}' --scratch $S/r39-<tag>
python3 $L/tools/run-receipt.py --revision <REV> --out $O/q82-<tag>.jsonl --lane $L --timeout 600 -- \
  tools/score-storage-arm-r38-q82.py --revision '{rev}' --scratch $S/q82-<tag>
python3 $L/tools/run-receipt.py --revision <REV> --out $O/r38-<tag>.jsonl --lane $L --timeout 900 -- \
  tools/score-storage-arm-r38.py --revision '{rev}' --scratch $S/r38-<tag>
python3 $L/tools/run-receipt.py --revision <REV> --out $O/r32-<tag>.jsonl --lane $L --timeout 1800 -- \
  tools/score-census-handoff-r32.py --revision '{rev}' --lane '{lane}' --scratch $S/r32-<tag> --seed d26bdc2550f2b04f
python3 $L/tools/run-receipt.py --revision <REV> --out $O/r35b-<tag>.jsonl --lane $L --timeout 3000 -- \
  tools/score-pacnew-arm-r35b.py --lane '{lane}' --revision '{rev}'
```

Runs were serial (one counter at a time). Wall clocks: q82 23 s / 25 s; r39 67 s / 56 s; r38 40 s / 38 s;
r32 29 s / 25 s; r35b 75 s / 56 s. No tool was installed or upgraded.

## 3. Findings per counter

### 3.1 `score-storage-hidden-r39.py` — PASS -> PASS

Both legs: `hidden_matched 2`, `views_matched 3`, `fixtures_matched 5`, `live_match 1`, `six_planes_all 1`,
`result PASS`, `exit 0`. The hidden legs print exactly
`STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`
in both receipts, the three namespace views carry no `mounts:` token (checked per view: `mounts_token` only in
the two `hidden` entries), the five fixture legs match 5/5, and the live leg matches the counter's own read of
`/sys/fs/btrfs` (`live.match true`, `census_exit 2` — the census' own live exit, unchanged between legs).

### 3.2 `score-storage-arm-r38-q82.py` — PASS -> PASS

Both legs: `ns_views_matched 3` of `views_expected 3`, `ns_available 1`, `result PASS`, `exit 0`. `ns_available 1`
means the unprivileged namespace leg was actually evaluated, not skipped.

### 3.3 `score-pacnew-arm-r35b.py` — FAIL -> FAIL (no change; this counter already fails at base)

Both legs: `candidate_matches 4`, `of 24`, `control_matches 24`, `should_fail 17`, `should_fail_accepted 0`,
`harness_errors []`, exit 1. The candidate matches the same four views at both revisions (`ns-20`, `ns-21`,
`ns-22`, `live`); the other 20 views fail with reason `base parity` at both revisions, so the round-46 census
does not move this counter's verdict in either direction. The per-view outcomes of the 17 should-fail arms
differ between the legs, but that is view randomness, not a verdict change: the views are drawn fresh per run
(23 of the 24 `expected` dicts differ between legs — e.g. `stub-00` base
`{"pacnew": 8, "pacsave": 5, "unreadable": 2, ...}` vs IMPL `{"pacnew": 7, "pacsave": 3, "unreadable": 1, ...}`),
and `should_fail_accepted` stays 0 in both.

### 3.4 `score-census-handoff-r32.py` — PASS -> PASS

Both legs, with the same pinned seed `d26bdc2550f2b04f` (so the same 24 scenarios):
`{"harness_errors": 0, "kind": "summary", "live_consistent": true, "predicate_label": "routed", "routed": 24,
"scenarios": 24, "unrouted": []}`, exit 0. The scenario mix is identical
(`{"both": 4, "coredumps": 4, "cumulative+coredumps": 2, "cumulative-only": 3, "kill-events": 5, "none": 3,
"tsukuroi-only": 3}`), and the live clause is satisfied at IMPL, so the new census does not perturb the
ADJ-04/mori HANDOFF surface or the PLANE/rollup parity the counter compares against base `58cc2e0b`.

### 3.5 `score-storage-arm-r38.py` — FAIL -> FAIL (outside the kill universe)

Both legs: `fixtures_expected 10`, `fixtures_matched 9`, `live_match 1`, `six_planes_all 1`, `result FAIL`,
exit 1. The failing fixture is the same one at both revisions: **`F06-no-btrfs-root`**, expected
`["HEALTHY", 0, 0, 0]`, got `["BLOCKED", 0, 0, 0]`. Stripping only the `revision` line, the two bodies are
byte-identical (4257 bytes each; `difflib` reports exactly one changed line, the `revision` field). This is the
pre-existing R38-ABSENT-ROOT disagreement that round 39's counter was frozen to arbitrate (r39 passes the same
surface at both revisions, §3.1), so this counter supplies no protective signal this round — recorded as a
limit, not harm.

## 4. Receipts (sha256) — `.ufo/waves/round-46/w1/C1ExecPriorC/`

| file | sha256 |
|---|---|
| `r39-base.jsonl` | `1784a145583340c020ce4c147952c7f1636a2519cabd084e5851ab7e95716393` |
| `r39-impl.jsonl` | `cc12d9b5434282b39ce05da9d39e22d74823113f668d8b3e8639c980a215df2b` |
| `q82-base.jsonl` | `3c040d691ec6656bc0f6b2808f2519618a3a0880537012de3b8841a1e740ad83` |
| `q82-impl.jsonl` | `a6c702fd06f04ecf4f0d51c4655e07a2fad2b3793ab129bfdf83c66a11949e30` |
| `r38-base.jsonl` | `e5ec69c501321e19ec476adbdd88ff93dee4e037b52e888982ef58d8b2225ce6` |
| `r38-impl.jsonl` | `c149bfcdb8a2c234c66aa537ffc2d290ff17e6f2af900695f27526284736130c` |
| `r32-base.jsonl` | `968ae8171ae3927ca47414faf7c9f3112fd390e32c56a2a13033e8211e74fb96` |
| `r32-impl.jsonl` | `dcc621382399dcf34c3ee8cea4b81896f85706e4aa16d96e6bf4852aaa995e68` |
| `r35b-base.jsonl` | `d421019e789ecfdbada81726d6a905bf311e4551ed01dd0244d6ec4a846d6c6e` |
| `r35b-impl.jsonl` | `99a48514c346a930040317070e74a473d55836f5ea26e093d7765aa1657cfb57` |

Each is a `run-receipt.py` JSON-lines receipt: header (`revision`, `tool_revision`, `tool`, `tool_sha256`,
`lane_branches`, `argv`, `started_utc`), the tool's own JSON body, footer (`exit_code`, `timed_out`,
`stderr_tail`, `finished_utc`). Every header names `tool_revision == revision` and
`refs/heads/master a44770491eb5ca15ce9f8b3207309d1af683ffaf`.

## 5. Limits and what was not done

* `score-pacnew-arm-r35b.py` accepts no `--scratch`. Its own temp tree is `tempfile.mkdtemp(prefix='r35b-')`
  (`tools/score-pacnew-arm-r35b.py:474`) under the child's `TMPDIR`, which `run-receipt.py`'s fixed child env
  (`tools/run-receipt.py:38-51`) does not set, so it lands under `/tmp` and is removed by the tool; both legs
  left no `/tmp/r35b-*` behind (`ls -d /tmp/r35b-*` -> 0 matches). This is driver/tool behaviour, not a scratch
  path I chose: the seat scratch (`/fast/scratch/hyaku/tsukuroi-r46/C1ExecPriorC/s`) was used for every counter
  that accepts `--scratch` and was removed after the receipts were copied into the seat dir.
* r39 and q82 take no `--seed`; each leg draws fresh random views, so those two pairs are independent
  replications, not paired comparisons. The comparison there is on the verdict-bearing counts, which are equal.
* I did not run the r35b `--skip-battery` mode (not asked; the battery is the measure) and did not re-run any
  counter — one run per leg, as instructed ("one at a time", single measured result each).
* No host state was read beyond what the counters themselves read; no namespace/scrub/systemctl action was run
  by me, no package/service/sysfs change, no `sudo`.
* Lane content was not modified by me: after all runs `git hash-object tools/tsukuroi-census.sh` equals
  `git rev-parse HEAD:tools/tsukuroi-census.sh` (`fedfd73aefcea8f316b5b6076646fa3315cb0506`), and
  `git status --porcelain` shows no new entry outside the untracked `.ufo/waves/round-46/` tree. Two lane paths
  carry fresh mtimes without content change (`tools/tsukuroi-census.sh` 02:31, `tools/__pycache__/` 02:28); the
  pycache entry there is `check-self-assessment.cpython-314.pyc`, a tool none of my five counters import, so
  neither is attributable to this seat (my tools run in `run-receipt.py`'s clone, and all five import stdlib
  only — `tools/score-census-handoff-r32.py:55-67`).
