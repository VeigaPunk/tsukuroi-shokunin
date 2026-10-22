# MutSelfAssessQ65 — mutation test of QUALITY 65 in `tools/check-self-assessment.py`

Verdict: partly holds — at revision `099c7b3f42d073203d9448807860f04c175eccd7` the QUALITY 65
implementation kills 7 of 9 mutants with the 15-case `--selftest` and its declaring-round guard is
load-bearing against the lane's own data, but 2 mutants survive the selftest (M7 and M8); both
survivors are real defects, and each names the selftest case that is missing.

## 1. Method and bounds

1. [obs] Read-only export of the attacked revision:
   `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 099c7b3f42d073203d9448807860f04c175eccd7 | tar -x -C /fast/scratch/hyaku/tsuku27a2/MutSelfAssessQ65/tree`.
   The exported `tools/check-self-assessment.py` hashes to
   `sha256 c5c2d6bed4b3422501457039257ed0d11a4961b228aaa96f0701a228d34c0e72`, identical to the lane
   working copy at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-self-assessment.py`
   (checked with `sha256sum`), so the line numbers cited below are the lane's own line numbers.
   The tool is byte-identical to the version introduced by commit `5583d75c9f354bc5e116b68d8b8997d8c742d0a9`
   (`git show 5583d75c:tools/check-self-assessment.py | sha256sum` gives the same digest).
2. [obs] Every mutation was made only in copies under `/fast/scratch/hyaku/tsuku27a2/MutSelfAssessQ65/`.
   The lane repository was never written to; `git status` of the lane was not run, and no git write
   command was issued against it.
3. [obs] The bounded detector is `python3 tools/check-self-assessment.py --selftest` (the tool's own
   15-case fixture selftest), run three times per mutant: on the pristine bytes, on the mutated
   bytes, and on the restored bytes. Driver: `/fast/scratch/hyaku/tsuku27a2/MutSelfAssessQ65/mutate.py`.
   Records: `/fast/scratch/hyaku/tsuku27a2/MutSelfAssessQ65/mutation-records.json`.
4. [obs] Baseline on the pristine export: `python3 tools/check-self-assessment.py --selftest`
   exits 0 and prints `"selftest": "PASS"`, `"cases": 15`, with no failing case
   (`/fast/scratch/hyaku/tsuku27a2/MutSelfAssessQ65/baseline-selftest.json`).

## 2. The code under test

5. [obs] `reference_lines` is at `tools/check-self-assessment.py:364`; its sole caller is at
   `tools/check-self-assessment.py:440` (`reference = reference_lines(score_lines, declaring_round)`),
   and the consuming loop is the K01 to K06 loop at `tools/check-self-assessment.py:487-513`.
   The QUALITY 65 rules are implemented in four places:
   - `tools/check-self-assessment.py:361` — `ROUND_HEADING_RE = re.compile(r"^Round ?(\d+)\b", re.I)`, the heading anchor.
   - `tools/check-self-assessment.py:380-382` — a heading whose text does not start with `Round N` is skipped.
   - `tools/check-self-assessment.py:383-387` — a section of the declaring round or a later round is excluded.
   - `tools/check-self-assessment.py:388-391` — the heading must carry `measured outcome`, and the excluded set is subtracted from the candidate set.
   - `tools/check-self-assessment.py:503-508` — the last matching transition in the reference set wins.

## 3. Mutant results (detector: `--selftest`, 15 cases)

| id | mutation (site) | expected detector | actual output | verdict |
|---|---|---|---|---|
| M1 | drop the round-comparison guard entirely, so a measured-outcome section of **any** round qualifies (`tools/check-self-assessment.py:383-387` deleted) | `own-round-outcome-depth-10` must fail | exit 1; `own-round-outcome-depth-10` FAIL, expected exit 1 and `["K01"]`, actual exit 0 and `[]` | killed |
| M2 | **use `<=` instead of `<`** on the earlier-than test: `if int(match.group(1)) >= declaring_round:` becomes `> declaring_round:` (`tools/check-self-assessment.py:383`), so the declaring round's own record qualifies | `own-round-outcome-depth-10` must fail | exit 1; `own-round-outcome-depth-10` FAIL, expected exit 1 and `["K01"]`, actual exit 0 and `[]` | killed |
| M3 | **drop the heading anchor**: the pattern loses `^` (`tools/check-self-assessment.py:361`) and `.match` becomes `.search` (`tools/check-self-assessment.py:380`) | `outcome-heading-not-round-anchored` must fail | exit 1; `outcome-heading-not-round-anchored` FAIL, reason "axes table depth score 8 differs from the after-value 3 of the last recorded transition (SCORECARD.md:25)" | killed |
| M4 | **drop the `measured outcome` requirement** (`tools/check-self-assessment.py:388-389` deleted) | `declaring-round-declaration-line` must fail | exit 1; `declaring-round-declaration-line` FAIL, reason "axes table depth score 8 differs from the after-value 3 of the last recorded transition (SCORECARD.md:25)" | killed |
| M5 | **drop the nested-section exclusion**: `return candidates - excluded` becomes `return candidates` (`tools/check-self-assessment.py:391`) | `own-round-outcome-depth-10` must fail | exit 1; `own-round-outcome-depth-10` FAIL, expected exit 1 and `["K01"]`, actual exit 0 and `[]` | killed |
| M6 | **take the first instead of the latest earlier record**: the K01 to K06 loop keeps the first match (`tools/check-self-assessment.py:507-508` guarded by `if observed is None:`) | `declaring-round-measured-outcome-line` must fail | exit 1; `declaring-round-measured-outcome-line` FAIL, expected exit 1 and `["K01"]`, actual exit 0 and `[]` | killed |
| M7 | drop the `\b` word boundary after the round number (`tools/check-self-assessment.py:361`) | none in the 15 cases | exit 0, `"selftest": "PASS"`, 15 cases, no failing case | **survived** |
| M8 | make the `measured outcome` match case-sensitive: `text.lower()` becomes `text` (`tools/check-self-assessment.py:388`) | none in the 15 cases | exit 0, `"selftest": "PASS"`, 15 cases, no failing case | **survived** |
| M9 | **drop the round anchor entirely**: a heading that names no round is treated as round 0 and so always qualifies (`tools/check-self-assessment.py:380-382`) | `outcome-heading-not-round-anchored` must fail | exit 1; `outcome-heading-not-round-anchored` FAIL, reason "axes table depth score 8 differs from the after-value 3 of the last recorded transition (SCORECARD.md:25)" | killed |

6. [obs] Seven of nine mutants are killed and each kill lands on the intended case. The two cases
   added by commit `5583d75c` (`own-round-outcome-depth-10`, `outcome-heading-not-round-anchored`)
   are the only detectors for M1, M2, M3, M5 and M9; `declaring-round-declaration-line` is the only
   detector for M4; `declaring-round-measured-outcome-line` is the only detector for M6.
   [inf] The selftest's QUALITY 65 coverage therefore rests on three fixture cases and one
   pre-existing case; each mutant below shows a clause of QUALITY 65 that no case pins.

## 4. The guard is load-bearing against the lane's live data

7. [obs] Measured at the attacked revision, reading the lane read-only:
   `python3 tools/check-self-assessment.py --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision 099c7b3f42d073203d9448807860f04c175eccd7`.
   Pristine tool: exit 1, `"declaring_round": 26`, `"reference_lines": 198`, 7 mismatches; K01 reads
   `SCORECARD.md:730` ("depth8→8" in the `### Round23 measured outcome` section, heading at
   `SCORECARD.md:724`), K03 reads `SCORECARD.md:731`, K04 reads `SCORECARD.md:772`, K05 reads
   `SCORECARD.md:771`, and K02 and K06 are mismatches with "no dated move record".
8. [obs] The same command with mutant M2 (`> declaring_round:`) gives exit 1, `"reference_lines": 209`,
   5 mismatches, and **all six of K01 to K06 now match, every one of them reading `SCORECARD.md:960`**,
   which is the line "Ordinal record, round 26 (dated move record that checks K01 to K06 read; no
   ordinal moved this round): depth 8 → 8; coverage 9 → 9; …" inside the `### Round 26 measured
   outcome` section (heading at `SCORECARD.md:951`) — the declaring round's own outcome record.
   [inf] That is exactly the round-26 defect 2 that QUALITY 65 names ("round 26's K01 to K06 all read
   the round's own line, and a depth-10 mutant passed", `corpus/QUALITY.md:132`), and it is live
   against the lane's current SCORECARD.md: without the guard, two mismatches (K02, K06) vanish
   because the round's own prose certifies the ordinals.
9. [obs] The same command with mutant M6 (first instead of latest) gives exit 1, the same 7
   mismatches, but the evidence pointers regress: K01 reads `SCORECARD.md:658` (the
   `### Round21 measured outcome` section, heading at `SCORECARD.md:652`), K03 reads
   `SCORECARD.md:659`, K05 reads `SCORECARD.md:700` (`### Round22 measured outcome`, heading at
   `SCORECARD.md:692`). [inf] The "latest" half of QUALITY 65 changes which dated record is cited,
   and on this revision the cited record is two to three rounds older; the pass or fail verdicts
   happen to be identical because those rounds recorded the same scores, so a score-only check would
   not see it.
10. [obs] The same command with mutant M8 gives exactly the pristine output (exit 1, 7 mismatches,
    the same observed lines), because every measured-outcome heading in the lane's SCORECARD.md is
    written in lower case.

## 5. Survivor M7 — the missing case

11. [obs] M7 removes the `\b` word boundary from `ROUND_HEADING_RE`
    (`tools/check-self-assessment.py:361`), so a heading such as `## Round 1x measured outcome` or
    `## Round 26th measured outcome` parses as a dated round record.
12. [obs] The 15-case selftest passes with M7 (exit 0, `"selftest": "PASS"`), so no existing case
    pins the word boundary.
13. [obs] The mutant is a real defect, not an equivalent mutant. Probe
    `/fast/scratch/hyaku/tsuku27a2/MutSelfAssessQ65/probe.py` builds a fixture whose SCORECARD.md
    has the extra section `## Round 1x measured outcome` with the line `- depth 8 -> 3` and evaluates
    it with the pristine tool and with M7 (`/fast/scratch/hyaku/tsuku27a2/MutSelfAssessQ65/probe-results.json`):
    pristine gives K01 `status=match`, `observed=8`, `observed_line=16`; M7 gives K01
    `status=mismatch`, `observed=3`, `observed_line=25`, exit 1.
14. [inf] **Missing selftest case (name it `round-heading-word-character-after-number`):** a fixture
    whose measured-outcome heading carries a word character directly after the round number
    (for example `## Round 1x measured outcome`) must **not** be read as a dated round record; the
    tool must keep resolving the ordinal from the earlier valid record. This case pins the `\b` in
    `tools/check-self-assessment.py:361`.

## 6. Survivor M8 — the missing case

15. [obs] M8 makes the `measured outcome` match case-sensitive (`tools/check-self-assessment.py:388`),
    which contradicts the tool's own docstring at `tools/check-self-assessment.py:369` ("carries
    `measured outcome` (case-insensitive)").
16. [obs] The 15-case selftest passes with M8 (exit 0, `"selftest": "PASS"`); every fixture heading
    in the tool spells the phrase in lower case.
17. [obs] The mutant is a real defect, not an equivalent mutant. The same probe with the section
    heading `## Round 1 Measured Outcome`: pristine gives K01 `status=mismatch`, `observed=3`,
    `observed_line=25` (the section counts as a dated record), M8 gives K01 `status=match`,
    `observed=8`, `observed_line=16` (the section is silently ignored and the ordinal falls back to
    the older record).
18. [inf] **Missing selftest case (name it `measured-outcome-different-capitalisation`):** a fixture
    whose measured-outcome heading spells the phrase with different capitalisation
    (for example `## Round 1 Measured Outcome`) must still be read as a dated record, because the
    docstring promises a case-insensitive match. This case pins `text.lower()` at
    `tools/check-self-assessment.py:388`.

## 7. Two further coverage observations (no contract change implied)

19. [obs] The anchor in `tools/check-self-assessment.py:361` is enforced twice: by the `^` in the
    pattern and by `re.match` at `tools/check-self-assessment.py:380`. A first attempt at M3 that
    changed only `.match` into `.search` while leaving `^` in the pattern was an equivalent mutant
    and passed the selftest; the true unanchor needs both edits. [inf] The redundancy is harmless
    today, but a future refactor that removes only one of the two anchors would silently weaken
    QUALITY 65 with no selftest signal.
20. [inf] M1 and M2 are killed by the same case (`own-round-outcome-depth-10`), so the selftest
    cannot distinguish "the declaring round's own record is allowed" from "a record of any round is
    allowed". **Missing selftest case (name it `later-round-outcome-section`):** a fixture with a
    measured-outcome section of a round **later** than the declaring round must not qualify. That
    case would separate M1 from M2. This is a coverage finding, not a request to change QUALITY 65.
21. [inf] Nothing in this report asks for a change to the QUALITY 65 contract. The two surviving
    mutants are defects against the contract as written in `corpus/QUALITY.md:132` and against the
    tool's own docstring; the missing cases are the remedy, and the decision on whether to add them
    belongs to the L1.

## 8. Restoration evidence

22. [obs] For every mutant the tool file was restored to the exact pristine bytes after the mutated
    run, and the detector was run a third time. Pristine digest
    `sha256 c5c2d6bed4b3422501457039257ed0d11a4961b228aaa96f0701a228d34c0e72`; mutated digests:
    M1 `4b74f149cdb27515…`, M2 `47ec8b266c63743a…`, M3 `9ad4ed7a9ffad379…`, M4 `0fa48d6d290a1f05…`,
    M5 `5f5731684e2a2bca…`, M6 `fd7bba3ec20b7e1d…`, M7 `cc00aac4d573bc90…`, M8 `d59d922efe4603e0…`,
    M9 `93aced854c372451…`; restored digest for all nine = `c5c2d6bed4b3422501457039257ed0d11a4961b228aaa96f0701a228d34c0e72`.
    The restored run exits 0 with `"selftest": "PASS"` and a payload byte-identical to the pristine
    run in all nine cases (fields `restored_equals_pristine` and
    `restored_output_identical_to_pristine` in `/fast/scratch/hyaku/tsuku27a2/MutSelfAssessQ65/mutation-records.json`).
23. [obs] No install was needed; no tool was added or upgraded. No lane file was modified: the only
    file written under the lane is this report.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin at 099c7b3f (tools/check-self-assessment.py, corpus/QUALITY.md, SCORECARD.md via git show, commit 5583d75c) and the read-only export /fast/scratch/hyaku/tsuku27a2/MutSelfAssessQ65/tree; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/MutSelfAssessQ65.md and /fast/scratch/hyaku/tsuku27a2/MutSelfAssessQ65/{mutate.py,probe.py,save_mutants.py,mutation-records.json,probe-results.json,baseline/,mutants/,probe/,SCORECARD-099c7b3f.md}; executed=git archive export (read-only), git show (read-only), python3 tools/check-self-assessment.py --selftest (27 runs: pristine, mutated, restored for 9 mutants), python3 tools/check-self-assessment.py --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision 099c7b3f42d073203d9448807860f04c175eccd7 with the pristine and the M2, M6, M8 tools, python3 mutate.py, python3 save_mutants.py, python3 probe.py
Model: MiniMax-M3.1-Flash (minimax-code)
Installs: none
