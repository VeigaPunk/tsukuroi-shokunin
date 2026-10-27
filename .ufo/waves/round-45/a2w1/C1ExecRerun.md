VERDICT: supports

# C1-1 — C1 counter re-run stability (seat C1ExecRerun, wave a2w1)

Item: verify the frozen C1 counter identity, then run the C1 counter receipt twice at the implementation
revision `18389f44cf6ce414d7be205998b29c79fb0b490c` and once at the base
`5bbd5ff588120fd8e7c744695351a6978b4241c1`; report per-run legs; compare with `before/` and with control
`C1-K8`; answer whether the result is stable across seeds.

All three counters were run one at a time in this seat (never two concurrently), each through
`tools/run-receipt.py` from a private `--no-local` clone at tool revision
`ea6e0ee38d8066663bb0871b53bade14441eb304`, with `TMPDIR=/fast/scratch/hyaku/tsukuroi-r45/C1ExecRerun`.

## 1. Frozen tool identity — holds

```
$ git -C …/tsukuroi-shokunin show ea6e0ee38d8066663bb0871b53bade14441eb304:tools/score-census-readers-r45.py | sha256sum
fe0e31e25c5b3c92cc5aace48acc56bc6dab39b4b3c09b49708a715a3250bd50  -
$ sha256sum …/tsukuroi-shokunin/tools/score-census-readers-r45.py
fe0e31e25c5b3c92cc5aace48acc56bc6dab39b4b3c09b49708a715a3250bd50  …/tools/score-census-readers-r45.py
```

Frozen blob == working file == the declared `fe0e31e2…bd50`; SCORECARD.md:2901 ("The C1 counter is unchanged
(sha256 `fe0e31e2…bd50`)"). Every receipt header below carries the same `tool_sha256`, so the receipts were
produced by the frozen tool, not by a working-copy variant.

Supporting identity, static legs by import (`importlib` on the frozen counter, `functions`/`locate`/`LEX_RE`):
census at IMPL `237b21c9…fcdc` with `lexical_hits=0` (0 lines before `run_selftest()` match
`"$CAP_OUT" | head`), 5/5 sites at lines 965/1003/1085/1460/1535, 6 `check` labels carrying `(R45-C1)`;
census at BASE `17c82406…1a35` with `lexical_hits=5` (lines 965, 1003, 1085, 1460, 1535) and 0 `(R45-C1)`
labels. Diff shape base→impl: `git diff -U0 … | grep '^@@'` gives exactly
`@@ -965 +965 @@`, `@@ -1003 +1003 @@`, `@@ -1085 +1085 @@`, `@@ -1460 +1460 @@`, `@@ -1535 +1535 @@`,
`@@ -3332,0 +3333,44 @@` — five 1-for-1 site rewrites (line numbers preserved) plus 44 added selftest lines
(`49 5 tools/tsukuroi-census.sh` by `--numstat`). The candidate bytes scored in the pre-data battery are the
same file: `sha256sum controls/c1-candidate/tools/tsukuroi-census.sh` → `237b21c9…fcdc`, `diff -q` against the
working census prints nothing.

## 2. Receipts (this seat, `.ufo/waves/round-45/a2w1/C1ExecRerun/`)

| receipt | revision | seed | exit | verdict | wall |
|---|---|---|---|---|---|
| `c1-after-1.jsonl` | `18389f44cf6c` | `3b6155522c50d965` | 0 | PASS | 273 s (03:24:12Z→03:28:44Z) |
| `c1-after-2.jsonl` | `18389f44cf6c` | `f49cccb970e32695` | 0 | PASS | 313 s (03:28:51Z→03:34:02Z) |
| `c1-base-1.jsonl`  | `5bbd5ff58812` | `962ef5a06fc43e24` | 1 | FAIL | 240 s (03:34:18Z→03:38:16Z) |

`runs-summary.json` in the same directory holds the extracted fields, per-site rows, revert rows, header/footer
times and each receipt's own sha256 (first-16 shown in the table's receipt ids are not hashes; the summary
records `7ad18acd…`, `a8bca618…`, `0292776b…`).

### Run 1 and run 2 (IMPL `18389f44`), both PASS

Both receipts: `lexical_hits 0`, `sites_found 5`, `equiv_ok 5`, `selftest_pass 1`,
`selftest_line "TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)"`, `selftest_r45 6`,
`revert_killed 6`, `adjacency_ok 1`, `census_sha256 237b21c9…fcdc`, `timed_out false`, `stderr_tail ""`.

Per-site (identical in both): S1 line 965, S2 1003, S3 1085, S4 1460, S5 1535, each `draws 8`,
`mismatches 0`, `first_mismatch []` — i.e. no per-site mismatch in either run.

Revert detail (identical in both): S1–S6 each `{"exit": 1, "r45_fail_lines": 1, "killed": true,
"timed_out": false}` — each reverted-to-base site and the S6 foreign-baseline regression guard are killed by
exactly one `FAIL … (R45-C1)` selftest line.

Adjacency leg (identical in both): `{"bytes_base": true, "exit": 0, "findings": [], "status": "PASS"}`.

### Run 3 (BASE `5bbd5ff5`), FAIL — the defect reproduces

`lexical_hits 5`, `sites_found 5`, `equiv_ok 0`, `selftest_pass 1`,
`selftest_line "TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)"`, `selftest_r45 0`,
`revert_killed 0`, `adjacency_ok 0`, `census_sha256 17c82406…1a35`, exit 1, `timed_out false`.

Per-site mismatches at base, with the deciding evidence: S1 4/8, S2 3/8, S3 6/8, S4 4/8, S5 4/8. Every first
mismatch is a `kind: "large"` draw whose BASE statement exits 141 while the oracle (base statement on the
first line alone) exits 0:

```
S1 {"kind":"large","len":175497,"oracle":"maintenance","oracle_rc":0,"rev":"","rev_rc":141}
S2 {"kind":"large","len":186911,"oracle":"signal",     "oracle_rc":0,"rev":"","rev_rc":141}
S3 {"kind":"large","len":111358,"oracle":"",           "oracle_rc":0,"rev":"","rev_rc":141}
S4 {"kind":"large","len":201406,"oracle":"inactive",   "oracle_rc":0,"rev":"","rev_rc":141}
S5 {"kind":"large","len": 95909,"oracle":"failed",     "oracle_rc":0,"rev":"","rev_rc":141}
```

That is the declared R41-CENSUS-PIPEFAIL-692 mechanism exactly (pipe buffer exceeded → producer SIGPIPE →
assignment returns 141 under `set -euo pipefail`), reproduced independently of the pre-data battery. The revert
leg at base is a no-op by construction (base line replaced by itself): S1–S6 each `exit 0`,
`r45_fail_lines 0`, `killed false` — so `revert_killed 0` here is the expected "nothing to kill", not a leg
failure. Adjacency leg at base: `{"bytes_base": true, "exit": 1,
"findings": ["INBOUND-CLASSIFICATION-WRONG"], "status": "FAIL"}`.

## 3. Comparison

**Against `controls/C1-K8.jsonl` (candidate control, must PASS):** every scored field is equal —
`verdict PASS`, `lexical_hits 0`, `sites_found 5`, `equiv_ok 5`, `selftest_pass 1`, `selftest_line` identical,
`selftest_r45 6`, `revert_killed 6`, `adjacency_ok 1`, `census_sha256 237b21c9…fcdc`; and the whole
`per_site`, `revert` and `adjacency` objects are byte-equal (`per_site==: True  revert==: True  adjacency==: True`).
The only differing fields are `seed` and `revision`: K8's revision `84c80b5bc7bc9be8932a4adccb703a1f5d2a6be3` is
a fixture commit outside the lane (not in the lane object store: `git show 84c80b5b…` → "fatal: bad object"), and
it carries the same census bytes (`237b21c9…fcdc`). So my lane-revision runs reproduce the battery's PASS control
on a different clone, a different seed and a different commit id.

**Against `before/`:** `before/` holds no C1 counter receipt (only `c2-before.jsonl`, `self-assessment-base.txt`,
`sources-census-start.txt`, `adjacency-base.txt`, `census-selftest-base.txt`). Both base anchors it does hold are
reproduced by my base run: `before/census-selftest-base.txt` — `TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148
passed, 0 failed)` — matches my base `selftest_line`, and `before/adjacency-base.txt` (`"status": "FAIL"`,
finding id `INBOUND-CLASSIFICATION-WRONG`, `revision 5bbd5ff5…`) matches my base run's adjacency object field for
field. Relative to base, the receipt pair also shows the intended "before/after" split of the declared claim:
148 → 154 cases, `selftest_r45` 0 → 6, `lexical_hits` 5 → 0, `equiv_ok` 0 → 5, `revert_killed` 0 → 6,
`adjacency_ok` 0 → 1.

**Base run vs `controls/C1-K0.jsonl`** (do-nothing control over a BASE-tree commit `c82a5fae…`, must FAIL):
identical on every aggregate field and on the adjacency object and `census_sha256`; the two seeds draw different
per-site mismatch counts — K0 `{S1 5, S2 4, S3 4, S4 6, S5 3}` vs mine `{S1 4, S2 3, S3 6, S4 4, S5 4}` — with
≥3 large 141-exit mismatches per site in both. That difference is the expected seed effect and is itself
evidence that the seeds are drawing real variation, not replaying a fixed fixture.

## 4. Stable across seeds? — yes on IMPL, and the failing side is stable too

Three independent seeds score the implemented census bytes `237b21c9…fcdc` PASS with identical legs: mine
`3b6155522c50d965` and `f49cccb970e32695`, plus the battery's `541cdcdf3a4c3adc` (`controls/C1-K8.jsonl`).
Run 1 vs run 2: `identical except seed: True` over the entire result object (`per_site`, `revert`, `adjacency`
included); each run draws 8 captured outputs per site with at least 3 large (>70 KB, up to 300 KB) tails, so the
equivalence leg is exercised on the pipe-buffer crossing regime in every run rather than by luck of one seed. On
the base side, two seeds (`962ef5a06fc43e24` mine, `468bae6f9336e727` K0) give the same aggregate FAIL and
per-site rc-141 mismatch signature, with only the per-site counts varying (each ≥3).

## 5. Limits of this receipt (not claimed)

- I ran the base revision once, not twice; base-side seed stability rests on my run plus the pre-data K0 control
  (different commit id, same tree).
- The base run's receipt is named `c1-base-1.jsonl`; the item named a pattern only for the two IMPL runs
  (`c1-after-<n>.jsonl`), which I followed (`c1-after-1.jsonl`, `c1-after-2.jsonl`).
- The PASS is a property of this host's bash and of the counter's `bash -c` harness (`CAP_OUT=$(cat file)`,
  `set -euo pipefail`, `LC_ALL=C`, 30 s per statement), i.e. the same capture semantics the census's `cap()`
  uses; it is not a claim about hosts with different pipe buffer sizes.
- No tool was installed or upgraded; no host state, lane tracked file, or PATH directory was touched. Scratch
  `/fast/scratch/hyaku/tsukuroi-r45/C1ExecRerun/` (with the counter's `s/`) was removed after the receipts were
  copied into this seat directory; the `run-receipt` clones and homes are removed by the harness itself.
