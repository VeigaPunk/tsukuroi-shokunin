VERDICT: supports

# C1FinalSelftest — item C1-F2 (round 43, wave w2, falsify)

Seat scope: export `tools/boot-chain-audit.sh` at the wave-1 tip, run `--selftest` twice, and
show, per `R43-C1-*` case, the smallest single revert of the fix that turns it red; report any
case no revert can turn red.

Revision under test: `8acf0b022586a0f3164c77659fb96ba5f90949b6`.
Export: `git -C <lane> show 8acf0b022586a0f3164c77659fb96ba5f90949b6:tools/boot-chain-audit.sh`
→ sha256 `77c80be827d69df08e172c531ddf87d6585c39140f6b3389b840b5d8ad9141ad`, 53559 bytes
(receipt `C1FinalSelftest/boot-chain-audit.8acf0b02.sh`). Run host: Linux 7.2.11-arch1-1 x86_64,
`bash 5.3.20(1)`, child-shell `find (GNU findutils) 4.11.0-modified`, `grep (GNU grep) 3.12-modified`,
`findutils 4.11.0-1` (`C1FinalSelftest/versions.txt`). Every run below was `bash ./<copy> --selftest`
with `TMPDIR` and cwd inside `/fast/scratch/hyaku/tsukuroi-r43/C1FinalSelftest/` — the selftest is
hermetic (fixtures under `$TMPDIR`, no host reads) and no lane file was read at run time.

## 1. Selftest, twice — expectation met

```
cd /fast/scratch/hyaku/tsukuroi-r43/C1FinalSelftest
TMPDIR=…/tmp bash ./boot-chain-audit.sh --selftest
```

Observed on both runs, rc=0, stderr empty (receipts `st1.out`, `st2.out`, `st1.err`, `st2.err`):

```
TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=49 failed=0
```

Same host, same invocation, two neighbouring revisions (receipts `base6951ead.out`,
`fix717b716a.out`):

| revision | selftest line | `st_check 'R43` occurrences |
|---|---|---|
| `6951ead` (base) | `PASS total=45 failed=0` | 0 |
| `717b716a` (implementation) | `PASS total=48 failed=0` | 3 (lines 1232/1235/1237) |
| `8acf0b02` (tip under test) | `PASS total=49 failed=0` | 4 (lines 1232/1235/1237/1239) |

So the frozen wording "four `R43-C1-*` selftest cases (selftest 45 → 49 at
8acf0b02…)" is exact for the tip, and the fourth case is the wave-1 integration addition
(`git log -S"R43-C1-missing-start-point-silent" -- tools/boot-chain-audit.sh` → `9b974f2a`,
whose subject says "R43-C1 stderr selftest case (49)"); 45 → 48 at the implementation commit,
48 → 49 at integration. Not a contradiction, but the 49 figure is not attributable to
`717b716a`.

Citations at the export: helper `inputs_newer_than` 463-475 (`find` call 469), `boot_inputs_newer`
477-489, R43 case block 1225-1239, `st_check` 824-831 (failure line 830), PASS printf 1242.

## 2. One mutation each — which cases go red

Each mutant is the 8acf0b02 export with exactly one edit; the unified diff, stdout and stderr of
each are receipts (`m*.diff`, `m*.out`, `m*.err`). Runs were sequential, one at a time.

| # | single change vs 8acf0b02 | R43 cases red | failed |
|---|---|---|---|
| M1 `basepipe` | helper body back to the pre-fix expression `if find "$@" -newermt "@$epoch" -print -quit 2>/dev/null \| grep -q .; then` (byte-identical to base `6951ead:480-483`) | `R43-C1-missing-start-point-deep-newer` | 1 |
| M2 `nostderr` | `2>/dev/null` dropped from the `find` call (469) | `R43-C1-missing-start-point-silent` | 1 |
| M3 `overfix` | `find … 2>/dev/null) \|\| { printf '1\n'; return 0; }` — find failure read as "newer" | `…-none-newer`, `…-silent` | 2 |
| M4 `invert` | helper polarity inverted (`-n "$hit"` → prints 0) | all four | 4 |
| M5 `inline` | helper deleted, base pipeline inlined in `boot_inputs_newer` (coarse pre-fix shape) | all four (`got []`, one `command not found`) | 4 |
| M6 `shallow` | `-maxdepth 1` added (recursion lost) | `…-deep-newer`, `…-all-present-deep-newer` | 2 |
| M7 `always0` | `hit=''` (detection disabled) | `…-deep-newer`, `…-all-present-deep-newer` | 2 |

Observed red lines (verbatim, from the receipts):

- M1 → `FAIL R43-C1-missing-start-point-deep-newer: expected [1] got [0]` (`m1_basepipe.out:1`)
- M2 → `FAIL R43-C1-missing-start-point-silent: expected [0] got [find: '…/bootinputs/missing': No such file or directory` ⏎ `0]` (`m2_nostderr.out:1-2`) — the stray stderr text the case is written to catch
- M3 → `…-none-newer: expected [0] got [1]` and `…-silent: expected [0] got [1]` (`m3_overfix.out:1-2`)
- M6/M7 → `…-deep-newer: expected [1] got [0]`, `…-all-present-deep-newer: expected [1] got [0]` (`m6_shallow.out:1-2`, `m7_always0.out:1-2`)

No mutant broke any of the other 45–48 cases beyond the R43 ones listed: the failed counts above
are exactly the R43 reds (M1 1, M2 1, M3 2, M4 4, M5 4, M6 2, M7 2).

## 3. Per-case verdict, and the two cases no revert reddens

| case (export lines) | reddened by the *revert* | smallest red-producing change | red-before? |
|---|---|---|---|
| `R43-C1-missing-start-point-none-newer` (1231-1232) | no | M3 over-correction only | **no** |
| `R43-C1-missing-start-point-deep-newer` (1234-1235) | **yes — M1** | restore the base pipeline in the helper (1 hunk) | **yes** |
| `R43-C1-all-present-deep-newer` (1236-1237) | no | M6 recursion loss / M7 disabled detection | **no** |
| `R43-C1-missing-start-point-silent` (1238-1239) | **yes — M2** | drop `2>/dev/null` (1 line) | **yes** |

- `…-deep-newer` is the regression killer for the fix itself: reverting the helper to the base
  expression (`find … | grep -q .` under `set -o pipefail`) makes the missing start point's exit
  status mask the listed hit and the case reports `expected [1] got [0]`, i.e. exactly the
  fail-open in the C1 claim.
- `…-silent` is the killer for the stderr suppression carried inside the new helper. Caveat for
  the record: base `6951ead:483` *also* had `2>/dev/null`, so dropping it is a revert of a retained
  detail rather than of the base→fix diff — it is nevertheless the operator's own example of a
  "smallest single revert", and it is the only change among the seven that reddens this case.
- `…-none-newer` and `…-all-present-deep-newer` assert behaviour the fix leaves unchanged, so no
  revert of the fix can turn either red: both are green under M1 (base semantics), M2, and each
  other's reverts. They are **not vacuous** — each has a behavioural witness: `…-none-newer` goes
  red only under the over-correction family (M3: find failure read as "newer"; also M4/M5), and
  `…-all-present-deep-newer` goes red under under-detection (M6 recursion lost, M7 detection
  disabled; also M4/M5). Together they bracket the helper: 0 when nothing newer even though `find`
  errors, 1 when the newest input sits two levels below a start point.

**Answer to the item's reporting question:** no `R43-C1-*` case is vacuous (each fails under at
least one measured mutation, with a behavioural witness, not merely by deleting the symbol). But
only two of the four — `…-deep-newer` and `…-silent` — are red-before-under-revert; `…-none-newer`
and `…-all-present-deep-newer` are direction guards that pass at base-equivalent semantics. If the
milestone "red-before per case" is read as "each case reddens under a revert of the fix", it holds
for 2/4.

## 4. Coverage note (measured, adjacent to the claim)

The fix comment (464-466) names two arms: a missing start point **or** an unreadable directory. All
four cases exercise only the missing-start-point arm. I measured the unreadable-directory arm
directly with the two helper bodies copied verbatim (`probe-unreadable.sh`,
`probe-unreadable.out`): directory `locked` at mtime 1000, mode 000, listed before `d` whose
`newer` file is at 3000, epoch 2000 —

```
raw find over (unreadable-dir, dir-with-newer):
  stdout=[…/d] find_exit=1
fixed  helper -> [1]
base   helper -> [0]
```

i.e. the second arm reproduces (GNU find prints the hit but exits 1; base pipeline reports "none
newer"), and the fixed helper handles it. It is the same single line, so M1 reddens it through
`…-deep-newer`; there is no dedicated unreadable-directory case. Not a gap that lets the fix
regress silently, but the comment claims an arm the case set does not name.

## 5. What I did not do

- Did not run the frozen C1 counter (`tools/score-bootinputs-r43.py`) or the round-42 census
  selftest — other seats hold those, and no heavy counter was run here (all runs above were ~1 s).
- Did not run `--live` (that would read host `/etc`, `/usr/lib` and the ESP; unnecessary here).
- Did not run any test other than `--selftest` on the mutated copies, and no formatter/linter.
- No package installs or upgrades were needed; pacman is host-wide paused and unused; no sudo.

Host guard: the only lane paths written are this report and
`.ufo/waves/round-43/w2/C1FinalSelftest/` (140 KB of receipts). No tracked lane file was edited, no
git/jj mutating command ran in the lane, no lane tool was imported as a Python module (no
`tools/__pycache__` exists), and the scratch tree
`/fast/scratch/hyaku/tsukuroi-r43/C1FinalSelftest/` was removed after the receipts were copied out.

## Replay

```
R=<lane>/.ufo/waves/round-43/w2/C1FinalSelftest
S=$(mktemp -d /fast/scratch/hyaku/tsukuroi-r43/replay.XXXXXX)
cp "$R/boot-chain-audit.8acf0b02.sh" "$S/boot-chain-audit.sh"
cp "$S/boot-chain-audit.sh" "$S/m1_basepipe.sh"; patch -p0 -d "$S" < "$R/m1_basepipe.diff"
TMPDIR=$S bash "$S/m1_basepipe.sh" --selftest   # → FAIL total=49 failed=1, …-deep-newer
(sha256 of the unmutated export: 77c80be8…ad9141ad)
```
