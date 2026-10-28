VERDICT: supports

# R50ExecRaceProbe — item C2-B2 (independent reproduction of the SIGPIPE false-miss defect)

Axes: **operability** (does the selftest harness read its own evidence truthfully), **C2** (is the frozen
matcher change justified by a measured defect), **probe** (a minimal, re-runnable reproduction with a rate).

Bytes under test: base census `b866a1d3d26616119a089f1a69b080136becc17b:tools/tsukuroi-census.sh`
(3791 lines, 220117 B, sha256 `4e032bcb4a119640e30b6a37d49c5b7f768660d8265bca02c6ee91234beaa4c2`,
extracted to `census-base.sh` in the receipts dir). Frozen bytes read (not run):
`8029cdba1049df25632c91a23c8db4eefb54be5f:tools/tsukuroi-census.sh`. All commands ran under
`TMPDIR=/fast/scratch/hyaku/tsukuroi-r50/R50ExecRaceProbe/tmp*`; the lane working tree was never written.

## (a) Base census `--selftest`, three warm runs — the round-49 self-contradiction does NOT reproduce

Command (per run): `TMPDIR="$S/tmp" bash "$S/census-base.sh" --selftest >stN.out 2>stN.err`

| run | rc | wall | stdout summary line | stderr bytes | `FAIL` lines |
|---|---|---|---|---|---|
| 1 | 0 | 34 s | `TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)` | 0 | 0 |
| 2 | 0 | 34 s | `TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)` | 0 | 0 |
| 3 | 0 | 35 s | `TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)` | 0 | 0 |

Receipts `st1.out`/`st2.out`/`st3.out` (15574 B each, byte-identical) and `st1.err`/`st2.err`/`st3.err`
(0 B each). **No `FAIL` line exists on stderr in any run**, so no `got:` text can match a reported-missing
pattern (the round-49 V7 self-contradiction, `R49ExecSelfAssess.md:70-96`) appeared in 3/3 warm runs. This
does not clear the base harness — see (c): the flake is load-dependent and its in-situ buffer is too small.

## (b) Minimal reproduction — `printf '%s\n' "$buf" | grep -qE` under `set -euo pipefail`

Script `repro.sh` (100/200/400 KB, 20 trials, marker line mid-buffer, single huge line), `repro-matrix.sh`
(size sweep), `repro-ext.sh` (line-shaped buffers, marker position), `repro-boundary.sh` (pipe-capacity
boundary). Every "miss" below is `rc=141`, i.e. `printf` killed by SIGPIPE while `grep` returned 0.

| buffer | shape | trials | false misses |
|---|---|---|---|
| 102400 B (100 KB) | single line, marker mid | 20 | **0** |
| 204800 B (200 KB) | single line, marker mid | 20 | **19** (rc 141 ×19) |
| 409600 B (400 KB) | single line, marker mid | 20 | **20** (rc 141 ×20) |
| 98304 B (96 KiB) | 60-col multi-line, marker mid | 200 | **117 (58.5 %)** — run under load |
| 98304 B (96 KiB) | single line, marker mid | 200 | 1 |
| 131072 B (128 KiB) | 60-col multi-line, marker mid | 20 | 16 |
| 204800 B | single line, marker **start** | 20 | 20 |
| 204800 B | single line, marker **end** | 20 | **0** |
| 204800 B | 60-col multi-line, marker mid | 20 | 19 |
| 61440 / 65536 / 98304 B | 60-col multi-line, mid | 20 each | 1 / 1 / 2 — same host, quiet, later |

Direct proof that the match *is* found and the pipeline still fails (`pipestatus.sh`, 200018 B buffer):

```
buflen=200018 PIPESTATUS[0]=141 PIPESTATUS[1]=0
grep-alone-hits=1
```

So the arm's `printf … | grep -qE -- "$re" || miss=…` records a miss for text that `grep` matched
(`rc=0`), because `pipefail` propagates `printf`'s 141.

**Load dependence (reported as measured, both runs).** The 96 KiB multi-line rate was 117/200 while the
host was running a concurrent selftest (≈90 live seats); the same shape re-measured minutes later on a quiet
host gave 2/20 at 96 KiB and 1/20 at 64 KiB. The race is between `grep`'s read-ahead and `printf`'s blocked
write, so the rate is a scheduling property, not a constant: the round-49 `11/20 at 96 KiB` figure
(`R49ExecSelfAssess/race3.out:4`, harness `race3.sh` = `fold -w 60` line-shaped buffer) sits inside the
observed band (55 % vs 58.5 % under load).

## (c) Mechanism (re-runnable in one paragraph) and the buffer sizes the census actually produces

**Mechanism.** `printf` is a shell builtin writing the whole formatted buffer to a pipe; when the buffer
exceeds the pipe capacity (`F_GETPIPE_SZ` measured 65536 B, `pipesz.txt`) the write blocks after filling the
pipe. `grep -q` exits at the first matching line and closes the read end, so `printf`'s remaining write takes
EPIPE/SIGPIPE (observed rc 141) even though `grep` found the line (rc 0). Under `set -o pipefail`
(`tools/tsukuroi-census.sh:454` at base) the pipeline's status is 141, so the must-match arm
`printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss '$re'"` (`tools/tsukuroi-census.sh:2401`, and the
same arm in `check_cli` at `:2432`) counts a miss; the case then prints a `FAIL` whose `got:` line contains
the very text reported missing (`bad()` at `:2226`; `ok()` at `:2225`). Re-run: `bash repro.sh`,
`bash repro-ext.sh`, `bash pipestatus.sh` in the receipts dir (each is self-contained, `set -euo pipefail`,
no writes outside `$TMPDIR`). The base census already states this rule for other arms at `:732-736`
("never `printf | grep -q` / `| grep -m1` / `| head` under pipefail on a probe buffer"), and the `ABSENT:`
arm at `:2396` was converted in round 42; the must-match arms were left on the idiom (4 `printf '%s\n' "$out"
| grep -q` sites and 2 `| head -n1` sites at base).

**Sizes the census's own cases produce (instrumented copy, `check`/`check_cli`/`id_check` capture dumps).**
One extra selftest on a scratch copy that only adds an output dump (verdicts unchanged: `PASS (167 cases,
167 passed, 0 failed)`, `instr2.out`): 163 of 167 case outputs captured directly (`check` 151, `check_cli` 5,
`id_check` 7; the other 4 cases assert fixed short strings via `ok`/`bad` directly, `:3555-3625`),
total 392994 B, `case-sizes.txt`. Largest = **2907 B** (`degraded: a foreign baseline past the pipe buffer
still finds its last row (R45-C1)`, `largest-case-2907B-R45-C1.out`). The R42-C1 4002-candidate case named
in the item is **2698 B** (`r42c1-4002-case-2698B.out`) — the census prints only `names=[alpha,beta,pad00000]`,
never the 4002 names; the ~96 KiB figure in the source comment (`:2762`) is the **fixture input**
(`qu` = 96041 B, `sup` = 84037 B, `fixture-input-sizes.txt`), not the census's stdout. `check_cli` arms are
≤1518 B and the `id_check` outputs are 229/288 B. **Every selftest buffer is ≤2.9 KB, i.e. 22× below the
65536 B pipe capacity**, so the pipe arm cannot SIGPIPE on any output the census's own selftest produces —
arithmetic, and consistent with 0/20 misses at 64-100 KB single-line in (b).

## Consequence for C2 (what this seat measured, and the residual)

- The defect class the claim fixes is real and reproduced independently of the counter: 19/20 at 200 KB,
  20/20 at 400 KB, 58.5 % at 96 KiB line-shaped under load; `PIPESTATUS` 141/0 with `grep` alone matching.
- The frozen replacement is the full-read form: `buf_has()` at `8029cdba:tools/tsukuroi-census.sh:2236`
  (`printf '%s\n' "$1" | RE="$2" awk '$0 ~ ENVIRON["RE"] { f = 1 } END { exit(f ? 0 : 1) }'` — awk reads
  every line, no early exit, no here-string) with `out_has()` at `:2239`; the only surviving occurrence of
  the old idiom in the frozen bytes is the explanatory comment at `:2230`. The new pin `(R50-C2)` at
  `:3643-3661` uses a ~200 KB probe (100000 `x` + marker + 100000 `x`) over 20 trials; my 200 KB
  single-line measurement (19/20 misses) says 20 trials separate the two matchers with probability
  ≈ 1 − 0.05^20.
- **Residual, stated as a limitation not a claim defect:** the frozen `buf_has` still maps *any* reader
  failure to "miss", so the arm cannot distinguish "evidence absent" from "reader failed". Since the
  census's own case buffers are ≤2.9 KB, the round-49 self-contradiction cannot be explained by the pipe
  race in situ; the round-49 seat's alternative candidate (a transient `grep` failure, §4 mechanism (b))
  remains the better fit for that instance, and the C2 change removes the SIGPIPE class without closing it.
  C2's stated predicate does not claim otherwise, so this does not falsify C2.

## What I did not do

- Did not run the frozen (`8029cdba`) census selftest or the C2 counter (`check-selftest-matcher-r50.py`) —
  outside this item's authorized commands and the counter's own seat.
- Did not run the live (non-fixture) census; all measurements are fixture-hermetic or synthetic.
- No installs/upgrades were needed (no tool changed: bash, grep, awk, python3, git as shipped).

## Receipts (`.ufo/waves/round-50/w1/R50ExecRaceProbe/`)

`census-base.sh`, `census-base.sha256`, `st1.out`…`st3.out`, `st1.err`…`st3.err`, `instr.out`,
`instr2.out`, `repro.sh`, `repro.out`, `repro-matrix.sh`, `repro-matrix.out`, `repro-ext.sh`,
`repro-ext.out`, `repro-boundary.sh`, `repro-boundary.out`, `pipestatus.sh`, `pipestatus.out`,
`pipesz.txt`, `case-sizes.txt`, `largest-case-2907B-R45-C1.out`, `r42c1-4002-case-2698B.out`,
`fixture-input-sizes.txt`.
