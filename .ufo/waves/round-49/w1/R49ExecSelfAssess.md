VERDICT: defect-found — calibration measures `checked 27, mismatches 2` (K13, K17), not the 3 the round expected (K10 matches at the freeze), and the counter's own census run recorded a self-contradicting `FAIL` case line that makes the round's `PASS (167 cases, 167 passed, 0 failed)` wording unproven.

Seat: R49ExecSelfAssess, item M-3 (self-assessment at freeze). Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`.

## 1. The run (once, as assigned)

Command (cwd `/fast/scratch/hyaku/tsukuroi-r49/R49ExecSelfAssess`, `TMPDIR` set to the same dir):

```
TMPDIR=/fast/scratch/hyaku/tsukuroi-r49/R49ExecSelfAssess timeout 1500 \
  python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-self-assessment.py \
  --revision 55c07cd3f8bff2e12117c34d57b4c618de74d85c
```

Observed: `RC=1`, wall 99.11 s (one census selftest inside), no retry needed.
Result fields (`R49ExecSelfAssess/sa-r49.json`):

```
checked 27   mismatches 2   status FAIL   exit 1
declaring_round 48
axes_heading "## Axes — current self-assessment (round 48 final measured surface)"
reference_lines 632
mismatch ids: K13, K17
```

All other 25 checks are `match`: K01-K12, K14-K16, K18-K27.

## 2. Per mismatch — stale SCORECARD line and corrected text

Line numbers are in `SCORECARD.md` at the freeze (`git -C <lane> show 55c07cd3:SCORECARD.md`).

### K13 — `SCORECARD.md:3031` (operability row of the axes table)

- Check: "operability row case count equals the census selftest case count at the revision".
- Counter: `stated 166`, `observed 167`, `stated_line 3031`, reason `operability row states 166 cases; the census selftest at this revision prints 167 cases (...)`.
- Stale clause (verbatim, `SCORECARD.md:3031`): `bash tools/tsukuroi-census.sh --selftest` prints PASS (166 cases, 166 passed, 0 failed) at round-48 freeze
- Corrected text (numeral, if a clean run is attached): `prints PASS (167 cases, 167 passed, 0 failed) at round-49 freeze`
- Corrected text (honest, given §4 below): `prints 167 cases at round-49 freeze; the round-49 counter run recorded one failed case (R42-C1 evidence arm, §4), so no PASS / "0 failed" is stated until a clean 167/167 run is attached`

### K17 — `SCORECARD.md:3041` (host-census-gate row of the capabilities table)

- Check: "host-census-gate row names only repository paths that exist at the revision" — plus, for this row only, the stated case count must equal the measured census count.
- Counter: all four named paths exist (`stated` == `observed`, so no path defect), `reason: host-census-gate row states 166 cases; the census selftest at this revision prints 167 cases`, `stated_line 3041`.
- Stale clause (verbatim, `SCORECARD.md:3041`): `selftest prints PASS (166 cases, 166 passed, 0 failed) at round-48 freeze`
- Corrected text: `selftest prints PASS (167 cases, 167 passed, 0 failed) at round-49 freeze` — or, with the §4 caveat, `selftest prints 167 cases at round-49 freeze (one case recorded failed in the round-49 counter run; no PASS stated)`.
- Optional, same row: the evidence pointer still cites `.ufo/waves/round-48/after/c1-final.json`; the round-49 receipt would be the calibration JSON this seat wrote (`w1/R49ExecSelfAssess/sa-r49.json`) once the count is restated.

### K10 — expected by the round, but NOT a mismatch at the freeze

- `SCORECARD.md:3029` (depth row) states `corpus/lessons/` 72 files; observed at the freeze is also 72: `git -C <lane> ls-tree -r --name-only 55c07cd3 corpus/lessons/ | wc -l` → `72`. Counter: `K10 match, stated 72, observed 72`.
- Therefore the round's "3 mismatches at the freeze commit" is off by one: the only count mismatches are K13 and K17, both from the 166 → 167 census change.
- K10 becomes stale only when `corpus/lessons/round-49.md` lands (72 → 73); the restated cell must then read `corpus/lessons/` 73 files. Same trigger for the axes table's depth row generally — nothing else in the depth row moved: K07 67 notes = 67, K08 4546 = 4546, K09 1323 = 1323, K11 480 = 480, and K12/K14/K15 (`present`/`present`/`present`) all match.

## 3. Why the freeze is otherwise clean

The axes heading is `round 48`, `declaring_round 48`, and K01-K06 (stated ordinal vs last dated move record in an earlier measured-outcome section) all match across 632 eligible reference lines; K20-K27 (SHONEN boxes: paths exist, `[x]` boxes name a non-author verifier, cited `corpus/knowledge` notes carry no supersession marker in their first 20 lines) all match. Calibration is therefore stale only on the two census-count numerals.

## 4. Side defect found in the same run (operability, not calibration)

The counter keeps only the last line of the census selftest's combined stdout+stderr. In this run that line is a failure line:

```
FAIL degraded: 4002 update candidates keep the names and the trap row (R42-C1): plane evidence missing:
'^PLANE update-safety: DEGRADED \(status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=4002 join_behind=0
names=\[alpha,beta,pad00000\]\); qu=rc=0/4002; sup=4002;'; got: PLANE packages: HEALTHY (...) | PLANE
systemd: HEALTHY (...) | PLANE drivers: HEALTHY (...) | PLANE journal: HEALTHY (...) | PLANE update-safety:
DEGRADED (status=REQUIRES-PREP; pending=REQUIRES-PREP(candidates=4002 join_behind=0
names=[alpha,beta,pad00000]); qu=rc=0/4002; sup=4002; join=equal=2 behind=0 ahead=0 src=sl+expac;
expac=agree; ... trap=-Suu:4002[fixture/alpha 1.1-1]; ...)
```

(`w1/R49ExecSelfAssess/k13-reason.txt`, extracted from the K13 `reason`; `got-line.txt` is the extracted plane line.)

The message contradicts itself: the `got:` planes include a line that matches the very regex reported missing. Verified independently on the extracted line:

```
LC_ALL=C grep -qE -- '^PLANE update-safety: DEGRADED \(status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=4002 join_behind=0 names=\[alpha,beta,pad00000\]\); qu=rc=0/4002; sup=4002;' got-line.txt
→ rc=0
```

`bad()` in the census selftest only runs on an assertion violation (`tools/tsukuroi-census.sh:2215`: `bad() { FAIL=$((FAIL + 1)); printf 'FAIL %s\n' "$*" >&2; }`), so this run had `FAIL >= 1` and its own stdout summary therefore did not read `0 failed`; the counter used the summary only for the case count (`167`), which is why K13/K17 still see 167.

Mechanism, not settled in-seat (two candidates, both `[INFERENCE]`):
- **(a) Latent pipe race in the harness.** The must-match arm uses the idiom the census itself bans elsewhere: `tools/tsukuroi-census.sh:2390` (and `:2421`) `printf '%s\n' "$out" | grep -qE -- "$re" || miss=...`, under `set -euo pipefail` (`:454`); the sibling `ABSENT:` arm at `:2385` was already converted to `<<<"$out"` in round 42 (`# round 42: a SIGPIPE'd pipe here read 'absent' (fail-open)`), and `:731-736` states the rule: "never `printf | grep -q` ... under pipefail on a probe buffer — the early reader exits, printf dies of SIGPIPE, and the pipeline reads false". Measured threshold with the exact case regex (`R49ExecSelfAssess/race3.sh`, match mid-stream, 20 trials each):

  ```
  buffer 8 KiB:  pipe-arm false misses  0/20, herestring 0/20
  buffer 32 KiB: pipe-arm false misses  0/20, herestring 0/20
  buffer 64 KiB: pipe-arm false misses  4/20, herestring 0/20
  buffer 96 KiB: pipe-arm false misses 11/20, herestring 0/20
  buffer 128 KiB: pipe-arm false misses 19/20, herestring 0/20
  buffer 813 KiB (race2.sh): 40/40, herestring 0/40
  ```

  This fires only above ~64 KiB of `$out`. The `got:` PLANE lines total 2 220 bytes and the census emits only short `PLANE`/`HANDOFF`/`SCRATCH` lines, so `$out` is plausibly far below that limit — which argues against (a) for this instance, unless an unobserved non-PLANE line is large (I could not measure `$out`'s size from the counter's JSON).
- **(b) A transient `grep` failure.** The arm records a miss on any non-zero `grep`, and a failure under host load (~90 seats live during this wave) would look exactly like this. Also unverified.

Either way the arm cannot distinguish "evidence absent" from "reader failed", and the round ships with a red selftest case line in its own calibration receipt. I did **not** run the census selftest myself — item M-3 authorizes only the counter run — so the cause stays open; the rerun below settles it and is cheap.

Reproduction for an authorized seat (one selftest, ~60-120 s), which also settles the wording:

```
S=/fast/scratch/hyaku/tsukuroi-r49/<seat>; mkdir -p "$S/x"; cd "$S/x"
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive --format=tar 55c07cd3f8bff2e12117c34d57b4c618de74d85c | tar -x
mkdir .t; env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$PWD/.t" HOME="$PWD/.h" bash tools/tsukuroi-census.sh --selftest > out.txt 2> err.txt; echo rc=$?
grep -E 'TSUKUROI_CENSUS_SELFTEST|^FAIL ' out.txt err.txt
```

Consequences for the round, stated plainly:
1. `cases == 167` (claim C3) is measured and holds; the count is not in doubt.
2. The restated operability / host-census-gate text must not claim `167 passed, 0 failed` on the strength of this counter run. Either fix `tools/tsukuroi-census.sh:2390`/`:2421` to the `<<<"$out"` form (the same change round 42 made at `:2385`) and attach a clean run, or restate the count only.
3. If the C3 counter is run in the same restricted child environment, the same spurious failure can make any `selftest_pass` term of it flaky; a C3 receipt claiming a green selftest is worth re-reading against its captured stderr.

## 5. What I did not do

- No census selftest of my own (outside item M-3's command class); no counter rerun.
- No lane write: no tracked file, index, jj state, or SCRATCH/SCORECARD edit — the corrected texts above are proposals only.
- No tool installs (none needed). Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ExecSelfAssess` removed after the receipts were copied.

## 6. Receipts

- `.ufo/waves/round-49/w1/R49ExecSelfAssess/sa-r49.json` — full counter JSON (27 checks).
- `.ufo/waves/round-49/w1/R49ExecSelfAssess/sa-r49.err` — `RC=1`.
- `.ufo/waves/round-49/w1/R49ExecSelfAssess/k13-reason.txt` — K13 reason incl. the census run's last line.
- `.ufo/waves/round-49/w1/R49ExecSelfAssess/got-line.txt` — the plane line the message claims absent.
- `.ufo/waves/round-49/w1/R49ExecSelfAssess/race2.sh`, `race2.out` — local pipefail/SIGPIPE reproduction at 813 KiB (40/40 false misses vs 0/40 here-string).
- `.ufo/waves/round-49/w1/R49ExecSelfAssess/race3.sh`, `race3.out` — same probe across 8/32/64/96/128 KiB; false misses begin at 64 KiB.
