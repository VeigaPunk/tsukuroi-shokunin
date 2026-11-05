# MutCheck — mutation test of the C2 and C3 repair (round 82, w1)

Read-only in the lane; every command ran in `/fast/scratch/hyaku/tsukuroi-r82/MutCheck/`
(`TMPDIR`, `--fixture`, `--work` pointed there). Only lane file written: this one.

    c6f76afc…21bb  tools/count-mount-rows-r81.py   (worktree candidate)
    29b8698c…acc   tools/measure-round81.py        (worktree candidate)
    27be5932…d50   SCORECARD.md (C3 snapshot; 6f365d30…fc8 after the round-82 block)
    5e176afc…b43   .ufo/.../before/mutants-r82.json (frozen, unchanged)
    6e6d9715…c24   tools/mutation-kill-r82.py      (frozen)
    888a3da9…e84   tools/check-scorecard-ordinals.py (frozen)

## 1. Harness output

`python3 <snap>/tools/mutation-kill-r82.py --fixture <snap> --work <snap>/work2` -> rc 1

    killed 22 / 26   genuine_killed 16 / 17   finding unmet
    survivors ["C06-source-id-shape","C07-own-work-rejection","C16-empty-manifest","M06-mutation-unlink-noop"]

21 kills exit rc 3 with an explicit `FAIL <case> rc=.. expected_rc=.. token=..` line; 1 kill
(M03) exits rc 1 with a traceback and no case fired (§3c). Against the pre-freeze bytes
(`--revision 683ae456`) the same command reproduces the control: 6/26, genuine 0/17.

## 2. Headline: the frozen C2 target is unattainable as the recipe file stands

C16 and M06 never apply — their `old`/`new` strings carry a **literal backslash-n**, not a
newline, and no leading indentation:

    $ python3 -c "...print('\\n' in r[k]['old'], chr(10) in r[k]['old'])"
    C16-empty-manifest        literal_bn=True real_newline=False
    M06-mutation-unlink-noop  literal_bn=True real_newline=False
    $ grep -c '\\\\n' .ufo/waves/round-82/before/mutants-r82.json -> 4   (2 recipes x old+new)

Occurrences of each recipe's `old`: 24 recipes 1x, `C16-empty-manifest` 0x,
`M06-mutation-unlink-noop` 0x. The harness records `recipe-missing:old-string-occurs-0x`,
which the frozen kill rule says is **not a kill**. Ceilings: `killed <= 26-2(equivalent)-2
= 22`, `genuine_killed <= 17-1(C16) = 16`. The frozen target (`>= 24`, `== 17`) cannot be
reached by any candidate. Proof it is the recipes, not the selftests — same candidate bytes,
scratch recipe copy with `\\n` replaced by a real newline and the indentation prepended:

    $ python3 <snap>/tools/mutation-kill-r82.py --fixture <fixrec2> --work <fixrec2>/workx2 -> rc 0
    killed 24 / 26   genuine_killed 17 / 17   finding met
    survivors ["C06-source-id-shape","C07-own-work-rejection"]
    C16-empty-manifest rc=3  FAIL empty-manifest rc=1 ...
    M06-mutation-unlink-noop rc=3  FAIL M04-six-of-six-met-cli rc=1 expected_rc=0 ...

Both clauses are already covered by the candidate's new cases. The declaration's own no-work
control already printed these ids with `recipe-missing` in `records[].detail`; nothing
checked recipe reachability before freezing. **Routed defect, not edited.** Corroborated by
`.ufo/waves/round-82/after/c2-recipe-applicability.txt` (`C16 … old_occurs=0`,
`M06 … old_occurs=0`) and `SCORECARD.md:7025`; my run adds the measured ceiling proof.

## 3. Three hand re-derivations

Method: copy the tool, apply exactly the recipe's `old -> new`, run `--selftest` with cwd and
`TMPDIR` in the mutant dir, read rc and the FAIL line.

**a. C08-digest-check** (`if sha(data) != want:` -> `if False:`) — rc 3.
`FAIL snapshot-tampered rc=1 body={"claim":"C1",…,"count":0,…,"finding":"unmet"…}`. The case
asserts rc 2 + `snapshot_tampered`; with the compare gone the tampered snapshot parses, its
rows unlocate, rc 1. Genuine assertion kill.

**b. C13-exit-code-mapping** (`return 0 if finding == 'met' else 1` -> `return 0`) — rc 3.
`SELFTEST total=19 passed=4 failed=15`; first `FAIL measured-wrong-source rc=0 body=…
"count": 7 … "finding": "unmet"`. Assertion kill, but it fires on the round-81 case, not a
new one.

**c. M03-table-from-disk** (`json.loads(read(TABLE))` -> `json.loads((ROOT/TABLE).read_text())`)
— rc 1, `FileNotFoundError: …/work2/mut/.ufo/waves/round-81/before/gate-standard-r81.json`.
**No case fired: this "kill" is a crash.** `is_killed = rc != 0` (mutation-kill-r82.py:125)
and only the *pristine* tool is baseline-checked (:98-107). Three synthetic recipes
(`@@@` after `import argparse`; a missing `_revision_missing`; an undefined symbol at
import) score `killed 3/3, genuine 3/3` with details `SyntaxError`, `ModuleNotFoundError`,
`NameError`; a timeout (rc 124, :71) is scored the same. The M03 clause *is* testable — a
well-formed decoy table at `ROOT/TABLE` flips the verdict (`FAIL gate-conformant-double
met=0 expected=6 …`) — but no committed case plants one, so the debt is invisible (§6).

**New cases assert, they do not merely print.** `count-mount-rows-r81.py:190` asserts
`proc.returncode == expect_rc and expect_token in body`; `measure-round81.py:223` asserts
`proc.returncode == expect_rc and token in body`. Case counts 6 -> 19 and 2 -> 6.
Aggregate-assertion weakness in the old `check()` cases (`met == expect_met`) was attacked
and did **not** yield a survivor: `ok = True` -> rc 3 (`defective-double met=6 expected=3`);
a compensating `B-met`-out/`C-mismatch`-in mutant -> rc 3 (`gate-conformant-double met=5
expected=6`, `defective-double met=2 expected=3`). The 6/6 + 3/6 two-tree design closes it.

## 4. Equivalent-mutant verdict: C06 and C07 stay equivalent; both labels are correct

**C07** (drop `or entry['kind'] == OWN_WORK`): redundant — `OWN_WORK='own-work'` is not in
`KINDS`, so `not in KINDS` already rejects it. Mutant runs `SELFTEST total=19 passed=19
failed=0`, **including** `own-work-source`. Counterfactual in scratch: with `'own-work'`
added to `KINDS` the same mutant dies (`FAIL own-work-source rc=0 … "count": 8, "finding":
"met"`). The firing case already exists; equivalence follows from the frozen `KINDS`.
**C06** (drop `SOURCE_ID.match(src)`): `entry is not None` implies the key came from
`registry_rows`, whose `^\s{0,3}\|\s*S[0-9]{3,}\s*\|` plus `strip()` can only yield
`^S[0-9]{3,}$`. Mutant green 19/19; relaxing that regex to `S[0-9]+` still green.
No new case can kill either without changing `KINDS` or the registry parser, so the frozen
`genuine_gap: false` labels are right and "no test can kill them" holds.

## 5. C3 forgery results (copies of SCORECARD.md in scratch)

Base: worktree `SCORECARD.md` (sha `6f365d30`) -> `count 0, examined 80, rc 0`; cutting the
`## Round 81 — ordinal correction` block out of it -> `count 1, examined 81`; HEAD 683ae456
-> `count 1, examined 78` (81, depth {8,9}). Then, on copies:

| fixture | shape | count / examined | rc |
|---|---|---|---|
| f1 | two disagreeing round-82 blocks | 1 / 78 | 1 |
| f2 | f1 + `supersedes-ordinal: round-82 depth` in the **earlier** block | 0 / 77 | 0 |
| f3 | f1 + the line in the **later** block | 0 / 77 | 0 |
| f4 | `supersedes-ordinal` + `depth 8 → 99` | 0 / 77 | 0 |
| f5 | `supersedes-ordinal: round-82 depth,calibration` | 0 / 77 | 0 |
| f6 | `depth8 → 9` vs `depth8 → 8` (no space after the axis) | 0 / 77 | 0 |
| f7 | `depth 8 to 9` vs `depth 8 to 8` | 0 / 77 | 0 |
| f8 | `Axes now: depth9` vs `depth8` | 1 / 78 | 1 |
| f9 | worktree + a later block asserting `depth 8 → 9` | 0 / 80 | 0 |
| f10 | f9 + its own supersedes line | 0 / 80 | 0 |
| f11 | f1 with `### Round 82` headings | 0 / 77 | 0 |

* **Order-insensitive.** f2: a supersedes line in an *earlier* block retires a *later* one,
  contradicting check-scorecard-ordinals.py:100 ("never later ones"). The guard at :102 is
  `if key[0] == round_no or True:` — `or True` makes it dead code; retirement is global.
* **Retire-into-silence.** f3/f4/f5: the correcting block's own ordinal is retired too, so
  the counter says `clean` while **no** ordinal stands for that (round, axis). The landed
  correction does exactly this: (round 81, depth) is gone from the ledger even though
  `SCORECARD.md:7007` prints `depth 8 → 8`. The predicate asks that every standing assertion
  carry exactly one after-ordinal; the instrument satisfies it by deleting the assertion.
  `count 0` is not evidence of one voice.
* **Permanent blindness.** f9/f10: after one supersedes line, any *later* contradiction on
  that (round, axis) is invisible for the rest of the file (current bytes: 0 / 80).
* **Its own C3 number is not reproducible.** `SCORECARD.md:7026` quotes `examined 77`; the
  file carrying that row measures `examined 80` (the block adds three round-82 assertions).
* **Spelling/heading evasion.** f6, f7, f11: `depth8 → 9`, `depth 8 to 9` and `### Round N`
  produce 0 findings on a real contradiction. Round 81 was caught only because it also wrote
  `Axes now: depth9`.

## 6. Coverage debt that remains

| survivor / suspect | clause left open | status |
|---|---|---|
| C16-empty-manifest | R4 `if not digests: raise CannotEvaluate('snapshot-manifest-empty')` | **covered** by the new `empty-manifest` case (dies once the recipe escapes are fixed); ledger cannot record it |
| M06-mutation-unlink-noop | unlink mutation actually applied | **covered** by the new CLI cases (`gate-conformant-double`, `M04-six-of-six-met-cli`); ledger cannot record it |
| C06-source-id-shape | R3 `SOURCE_ID.match(src)` | unobservable by construction; equivalent, correctly labelled |
| C07-own-work-rejection | R3 `kind == OWN_WORK` | redundant given `KINDS`; equivalent, correctly labelled, firing case exists |
| M03-table-from-disk | table read through `read()` at the bound revision | **open**: killed only by `FileNotFoundError`; no case plants a decoy table (observable, untested) |
| C2 score itself | any mutant that fails to import/parse/times out | **open**: `rc != 0` is a kill (:125), so 24 crashing mutants would read as `met` |

For the integrator (not applied): the two recipe entries need real newlines and correct
indentation, and the counter should separate `killed-by-assertion` from `killed-by-crash`
(rc 1 + traceback with no `FAIL` line, or rc 124). Both are frozen bytes this wave may not
touch; C2 must be reported `unmet` with the ceiling 22/26, 16/17 unless the operator
re-freezes.

## 7. Hygiene

No tool installed or upgraded (none needed; python3 3.14.8). No git/jj mutation, no lane file
touched but this report. Scratch `/fast/scratch/hyaku/tsukuroi-r82/MutCheck/` (2 snapshots,
5 harness runs, 12 C3 fixtures, mutant and counterfactual trees) deleted before yield;
nothing written under `/tmp`.
