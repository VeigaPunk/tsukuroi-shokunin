# ExecMutMeasure — round 82 w1 report

Seat: ExecMutMeasure. Scope: extend `tools/measure-round81.py --selftest` only, to kill
the four genuine-gap mutants M04/M05/M07/M08. No production clause, constant, exit
mapping or message touched.

## Files changed

- `tools/measure-round81.py` — +45 lines, all inside `selftest()` (inserted after
  `check('defective-double', broken, 3)`, before `finally:`). sha256
  `29b8698cd4515d9863029ea857834f95b3b3c0be6150edea7177f880cb13eacc` (was
  `0e94c9b4a9bc0f3ab92ec33005ea2d8743f558ccac26719adcf1765bfd3f5db9`).
  `git diff --stat`: 1 file, 45 insertions(+), 0 deletions.

## Production lines NOT changed (verified byte-identical)

- L40 `TARGET = 6` (M04's clause)
- L59 `raise CannotEvaluate('export-absent:' + name)` (M08's clause)
- L74 `ok = proc.returncode == want['rc'] and want['token'] in body` (M01/M02)
- L112 `finding = 'met' if met == TARGET else 'gate-standard'` (M07's clause)
- L242 `return 0 if count == TARGET else 1` (M05's clause)
- Existing cases `gate-conformant-double` / `defective-double` and the 0/1/2/3 exit map
  untouched; `git diff` shows zero removed lines.

## New selftest cases (each drives the public CLI `--fixture` over an isolated tree)

Each case builds a fixture tree under the selftest's `tempfile.mkdtemp` root (honours
TMPDIR), writes the frozen expected-table into it, optionally unlinks one export file,
then runs `python3 <this script> --fixture <tree>` as a subprocess with a minimal env
(PATH/TMPDIR/PYTHONDONTWRITEBYTECODE/LC_ALL) and asserts BOTH exit code and finding
token. No writes outside TMPDIR; all scratch removed in `finally`.

| Case name | Gap | Guarded clause | Assertion |
|---|---|---|---|
| `M04-six-of-six-met-cli` | M04 | gate target is 6 conformant cases | 6/6 tree → rc 0 + `"finding": "met"` |
| `M04-M07-five-of-six-gate-standard-cli` | M04 + M07 | target 6 / unmet yields `gate-standard` | exactly-one-case-fails tree (mismatch leg made met-like) → rc 1 + `"finding": "gate-standard"` |
| `M05-unmet-exit-one-cli` | M05 | unmet exits 1 | 3/6 `broken` tree → rc 1 + `"finding": "gate-standard"` |
| `M08-missing-export-could-not-evaluate-cli` | M08 | missing export is could-not-evaluate | `corpus/SOURCES.md` unlinked → rc 2 + `export-absent:` |

M04 and M07 share the five-of-six separating input (the minimal input that splits both
clauses); M05 and M08 each have a dedicated case. Total selftest cases: 6 (2 pre-existing
+ 4 new).

## Verification (commands + observed output)

1. `TMPDIR=$S python3 tools/measure-round81.py --selftest`
   → `SELFTEST total=6 passed=6 failed=0`, `selftest-rc=0`.
2. No-work control re-run before editing (fixture of unedited tools):
   `python3 tools/mutation-kill-r82.py --fixture $S/fix0` →
   `{"killed": 6, "total": 26, "genuine_killed": 0, "finding": "unmet"}` rc 1 —
   matches the frozen declaration; M04/M05/M07/M08 all in the survivor list.
3. Post-edit fixture `$S/fix1` = `tools/{measure-round81,count-mount-rows-r81,_revision}.py`
   + `.ufo/waves/round-82/before/mutants-r82.json`; then
   `python3 tools/mutation-kill-r82.py --fixture $S/fix1` → rc 1,
   `{"killed": 22, "total": 26, "genuine_killed": 16, "target_killed": 24,
   "target_genuine": 17, "finding": "unmet"}`.
   `measure-round81.py` records (all four genuine gaps killed, rc=3 each):
   - M04 `FAIL M04-M07-five-of-six-gate-standard-cli rc=0 expected_rc=1
     token='"finding": "gate-standard"' observed='{"count": 5, "target": 5,
     "finding": "met", ...'` — TARGET=5 mutant reports 5/6 as met.
   - M05 `FAIL M05-unmet-exit-one-cli rc=0 expected_rc=1 ... "count": 3,
     "target": 6, "finding": "gate-standard"` — mutant exits 0 on unmet.
   - M07 `FAIL M05-unmet-exit-one-cli rc=1 expected_rc=1 token=... observed=...
     "finding": "met"` — rc correct, finding token absent.
   - M08 `FAIL M08-missing-export-could-not-evaluate-cli rc=0 expected_rc=2
     token='export-absent:' observed='... "count": 6, "finding": "met"'` — missing
     export silently became met.
   M01/M02/M03/M06 outcomes unchanged-or-better (M01/M02/M03 still killed by the
   pre-existing cases; M06 `recipe-missing:old-string-occurs-0x`, unchanged).

## Risks / blockers (round-level, not fixable inside my write scope)

- **Frozen recipe defects cap the genuine leg at 16/17.** `C16-empty-manifest`
  (`genuine_gap: true`) and `M06-mutation-unlink-noop` have `old` strings containing a
  literal backslash-n (`\\n` in the JSON), which occurs 0× in the tool sources — the
  harness reports `recipe-missing:old-string-occurs-0x` for both. C16 is genuine, so
  `genuine_killed == 17` is unreachable with the frozen recipe set regardless of tool
  work. L1 needs a recipe amendment decision; seats may not touch the frozen file.
- **killed >= 24 requires killing declared-unkillable mutants.** The declaration itself
  states C06/C07 are equivalent and "no test can kill them", yet they count toward the
  26. With C16+M06 unmatchable, max achievable `killed` is 24 only if C06/C07 also die —
  i.e. the 24-leg is reachable only in the degenerate case where every killable recipe
  dies AND at least one equivalent dies by accident. Reported as observed arithmetic,
  not a request to weaken tests.
- Sibling in-flight edits to `tools/count-mount-rows-r81.py`,
  `corpus/knowledge/mount-unit-fstab-plane-r81.{json,md}` and `SCORECARD.md` were present
  in the worktree during my run; my harness fixture used the pristine committed copy of
  `count-mount-rows-r81.py`, so the C16 survivor above reflects the frozen state, not a
  sibling's partial work.

## Scratch

`/fast/scratch/hyaku/tsukuroi-r82/ExecMutMeasure/` deleted before yield (fixtures
`fix0`, `fix1`, `base`, harness JSON `harness-after.json` all under it).
