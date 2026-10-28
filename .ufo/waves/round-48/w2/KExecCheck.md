VERDICT: supports

# KExecCheck — C3-X1 (C3 counter at three revisions + which SCORECARD table it reads)

Round 48 (hyaku run 10, attempt 2), wave w2, seat KExecCheck. 2026-10-28.
Counter under test: `tools/check-self-assessment.py` sha256 `44b474fb5401559d9a4052f04f03145cd165a688a78455694d7dd25dba5838e6`,
identical in the lane working tree, at base `5fdf062f969292736e36513e39f98b1b8de43635` and at FREEZE
`ae99f021b76f8eb1c8805d32d80644464afb1ff6` (`sha256sum` of the file and of `git show <rev>:tools/check-self-assessment.py`,
three identical digests; `git status --porcelain` on that path empty — so the cited line numbers hold at all three revisions).

All runs executed from `/fast/scratch/hyaku/tsukuroi-r48/KExecCheck/` (free space seen: `/dev/nvme1n1p2 804G, 540G avail`).
No `--scratch` was passed, so the counter placed its own `git archive` work dir and the census child's TMPDIR under the
default temp root; that is the counter's documented own write (docstring line 8 and `census_case_count`, `tools/check-self-assessment.py:176-205`),
not a seat write.

## 1. Three counter runs, one at a time (status / checked / mismatches / exit)

| # | Revision | exit | status | checked | mismatches | declaring_round | axes_heading read | reference_lines | wall |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `5fdf062f` (base) | 1 | FAIL | 27 | 1 | 46 | `## Axes — current self-assessment (round 46 final measured surface)` | 618 | 52.4 s |
| 2 | `ae99f021` (FREEZE) | 1 | FAIL | 27 | 3 | 46 | same round-46 heading | 618 | 64.1 s |
| 3 | `5fdf062f` (base, repeat) | 1 | FAIL | 27 | 1 | 46 | same round-46 heading | 618 | 76.1 s |

Receipts: `KExecCheck/run1-base.json`, `run2-freeze.json`, `run3-base-repeat.json` (each `.err` empty).

Every non-`match` check, verbatim fields:

- **Run 1 (base), 1 mismatch — exactly the declared K10:**
  - `K10` — subject `depth row corpus/lessons file count equals the file count under corpus/lessons/`; **stated 70**, **observed 71**;
    `stated_line` **3029**; reason `depth row states 70 lesson files; corpus/lessons holds 71 files`.
- **Run 2 (FREEZE), 3 mismatches — exactly the declared K10, K13, K17:**
  - `K13` — subject `operability row case count equals the census selftest case count at the revision`; **stated 164**, **observed 166**;
    `stated_line` **3031**; reason `operability row states 164 cases; the census selftest at this revision prints 166 cases (TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed))`.
  - `K17` — subject `host-census-gate row names only repository paths that exist at the revision`; **stated** `["tools/tsukuroi-census.sh", ".ufo/evidence/round-1-kaika/scout-live.md", ".ufo/evidence/round-1-kaika/after.md"]`,
    **observed** the same three paths; `stated_line` **3041**; reason `host-census-gate row states 164 cases; the census selftest at this revision prints 166 cases`.
    Note for the L1: K17's mismatch is **not** a path problem — its stated and observed path arrays are identical; the mismatch is
    carried by the case count inside the same capability cell (`tools/check-self-assessment.py:700-716`: for `host-census-gate`,
    `stated_count = stated_case_count(cell_text, ...)` is compared against the K13 census count). So the capability row needs the
    `164`→`166` edit too, or K17 keeps failing after the axes row is fixed.
  - `K10` — as in run 1, `stated_line` **3029**.
- **Run 3 (base repeat), 1 mismatch:** `K10` stated 70 → observed 71, `stated_line` 3029. **`cmp run1-base.json run3-base-repeat.json` → identical** (byte-identical, so the
  counter is deterministic on the same revision; only wall time varies, 52.4 s vs 76.1 s).

C3's declared before-values therefore reproduce exactly: 1 (K10) at base, 3 (K10, K13, K17) at FREEZE, `checked` 27 in all runs.

Independent corroboration of the two observed numbers: `corpus/lessons/` holds 71 files at both base and FREEZE
(`git ls-tree -r --name-only <rev> -- corpus/lessons | wc -l` → `71` twice), and the census blob at FREEZE is
sha256 `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`, matching the frozen C1 blob, whose selftest prints 166 cases
(the only census change between base and FREEZE is commit `174a2c79`; base census blob sha256 `adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41`).

## 2. Which table the counter reads — `--help` + declaration + measured sandbox matrix

`--help` (`tools/check-self-assessment.py:1094-1100`) exposes only `--revision`, `--repo`, `--selftest`, `--scratch`; nothing selects a round.

Selection is **"the last `## Axes —` heading by line order"**, not "the largest round number":

- `section = find_section(score_lines, re.compile(r"^##\s+Axes\s+[—-]\s"))` — `tools/check-self-assessment.py:459`;
  `find_section` keeps overwriting `found` while scanning forward, i.e. **last match wins** (`tools/check-self-assessment.py:250-259`), and its
  section end is the next `^##\s` line (`:256-259`). The round is then parsed out of that heading
  (`ROUND_IN_TEXT_RE.search(axes_heading)`, `:462-467`, regex `:363`); `declaring_round` only feeds `reference_lines` (`:468`, used at `:411`/`:529`)
  and the result field (`:812`).
- The declaration's own wording ("SCORECARD self-assessment restated at round end against observed state", `.ufo/waves/round-48/frozen`-era
  text in `SCORECARD.md` § "Round 48 — declaration", C3 row) is satisfied by either route measured below.

Sandbox: `git clone -q --shared <lane> /fast/scratch/hyaku/tsukuroi-r48/KExecCheck/lane`, `git -C … rev-parse --show-toplevel`
→ `/fast/scratch/hyaku/tsukuroi-r48/KExecCheck/lane`, detached at `ae99f021…`; all four commits made inside that clone only
(`-c user.name=fixture -c user.email=fixture@invalid`). Counter invoked as
`python3 <lane>/tools/check-self-assessment.py --repo /fast/scratch/hyaku/tsukuroi-r48/KExecCheck/lane --revision <sandbox commit>`.

| Variant | Sandbox commit | Change | exit | status | mismatches | declaring_round read | axes_heading read | reference_lines |
|---|---|---|---|---|---|---|---|---|
| A | `932078a4` | `## Axes — current self-assessment (round 48 final measured surface)` + copied round-46 table **appended at EOF** | 1 | FAIL | 3 | **48** | the new round-48 heading | 632 |
| B | `5f0a5f7a` | the same round-48 heading+table **inserted at line 3024, before** the round-46 heading (now line 3037) | 1 | FAIL | 3 | **46** | the **round-46** heading | 618 |
| C | `86160ab3` | `## Axes — self-assessment (unqualified surface)` appended, no round number | **2** | CANNOT_EVALUATE | – | – | `error: no round number in the axes heading` | – |
| A2 | `9b05e55e` | variant A + restated counts (`71` lessons, `166` cases in the axes row **and** in the host-census-gate capability row) | **0** | **PASS** | **0** | 48 | the new round-48 heading | 632 |
| D | `66113b8f` | no new heading: the round-46 table cells restated in place (`70`→`71`, `164`→`166`) + capability row `164`→`166` | **0** | **PASS** | **0** | 46 | the round-46 heading | 618 |

Receipts: `run4-variantC.json`, `run5-variantA.json`, `run6-variantB.json`, `run7-variantA2.json`, `run8-variantD.json`.

Answers to the item's two questions:

1. **Does the counter read exactly the table the L1 will restate?** Yes — **provided the new heading is the last `## Axes —` heading in
   `SCORECARD.md`**. Appended at EOF it is read (variant A/A2: `axes_heading` is the round-48 heading, `declaring_round 48`, and the depth/operability
   `stated_line`s move 3029/3031 → 3119/3121). Inserted anywhere before the round-46 heading it is **silently ignored** (variant B: round-46 read,
   `declaring_round 46`, `stated_line`s +14 → 3043/3045/3055). At FREEZE the last `## Axes —` heading is line 3023 (round 46);
   `SCORECARD.md` also carries an earlier `## Axes — final self-assessment (landed round 11; …)` at line 39 and duplicated headings
   (round 26 twice at 938/970, round 37 twice at 1976/2000), so "last by line order" is the operative rule, and today it coincides with
   "largest round number" only because headings were appended chronologically.
2. **Does adding a NEW round-48 heading change which table is read?** Yes when appended: the round-48 table is read and `declaring_round`
   rises 46→48, which widens the eligible ordinal-reference set (`reference_lines` 618 → **632**, i.e. the round-46/47 sections become eligible
   references). K01-K09 still matched in variants A and A2 at this tree, so the widening is harmless here — but it is a real semantic change the
   L1 should re-confirm by reading K01-K09 in the final run, and it is avoidable entirely by route D.
   A heading without a round number in the last position is fatal: exit 2, `CANNOT_EVALUATE`, before any census work.

**Both restatement routes close C3** (A2 append-new-heading → PASS, 0 mismatches; D in-place-then-no-new-heading → PASS, 0 mismatches).
The counter requires the *counts* to be right in whichever table ends up last; it does not require a round-48 heading.

## 3. Exact restatement checklist for the L1 (derived from the counter's parsers)

1. `SCORECARD.md:3029` depth row (the row line the counter reports as `stated_line`): `| depth | 8 | 67 notes … \`corpus/lessons/\` 70 files …` → `… 71 files …`
   (K10 parses `(\d+)\s+files?\b` near `corpus/lessons/`, `tools/check-self-assessment.py:620-624`).
2. Operability axes row, `SCORECARD.md:3031`: the **first** case-count form present wins, `PASS \((\d+)\s+cases`
   (`stated_case_count`, `tools/check-self-assessment.py:578-589`), so the edit must be in the `PASS (…)` form:
   `prints PASS (164 cases, 164 passed, 0 failed)` → `prints PASS (166 cases, 166 passed, 0 failed)`.
3. `SCORECARD.md:3041` host-census-gate capability row (`## Capabilities — current full evidence set (round 46)`): same edit,
   `PASS (164 cases, 164 passed, 0 failed)` → `PASS (166 cases, 166 passed, 0 failed)` (K17, `:700-716`). Leaving this row alone keeps K17 red
   even after step 2 is done.
4. Keep any new `## Axes — current self-assessment (round 48 …)` heading **after** the round-46 axes section, and give it the `round 48` label.
5. **Commit before measuring**: every input is read through Git at one revision (`tools/check-self-assessment.py:7-9`, `show_blob` `:134-139`);
   an uncommitted restatement is invisible to the gate.
6. **Re-derive, do not copy, the two observed numbers at the final revision**: K13 runs the census `--selftest` from `git archive <REV>`
   (`:176-205`), so if w2 integration changes `tools/tsukuroi-census.sh` again the observed case count moves off 166; likewise `corpus/lessons/`
   becomes 72 if a round-48 lesson file lands. Restate from the counter's own `observed` fields at the final revision.
7. Expected end state: `status PASS`, `checked 27`, `mismatches 0`, exit 0 — measured as reachable (variants A2 and D).

## 4. Risks and limits of this evidence

- Variant A2/D restatement was applied to **copies** of the freeze `SCORECARD.md` in the sandbox clone; the digest of the real
  `SCORECARD.md` and the lane working tree were never touched (`git status --porcelain` on the lane was clean for the counter file; no lane writes).
- Each run costs ~50-110 s wall and 8-29 CPU-min because K13 runs the census selftest; the counter is not a cheap check. All eight runs were
  serialized (never two at once).
- The three graded numbers reproduce identically on a repeat run (byte-identical JSON), so a single final run is sufficient for the gate.
- Host observation, unattributed: `/tmp/self-assessment-census-fm_ny_gu` (364 MB, mtime 09:04:25) and `/tmp/self-assessment-git-g0dqqqzh` (0 B,
  09:04:22) are stale counter temp dirs from **some** seat's killed run — the counter's cleanup is a `finally: shutil.rmtree`
  (`tools/check-self-assessment.py:203-204`) and the module-level `TemporaryDirectory` (`:69`), so only a killed process leaks. My eight runs all
  returned normally and left no `self-assessment-*` directory at their finish times. I did not delete them: the prefix is shared by every seat
  running this counter and one may still be in flight. Free space at start: 540 G on `/fast`, so no ENOSPC risk here.
- Not done (so not passed): I did not run the counter's own `--selftest` (out of scope for C3-X1 and it contains census runs), did not verify the
  round's other claims (C1, C2), and did not attempt any lane restatement.

## 5. Tooling

No tools installed or upgraded (no pacman, `uv`, `npx` or binary install was needed). Scratch
`/fast/scratch/hyaku/tsukuroi-r48/KExecCheck/` (clone + receipts) was removed after the receipts were copied here.
