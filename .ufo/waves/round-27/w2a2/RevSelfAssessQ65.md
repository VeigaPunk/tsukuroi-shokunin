# RevSelfAssessQ65 — routed round-26 defect 2 (QUALITY 65 in check-self-assessment.py)

Verdict: partly holds. QUALITY 65 is implemented in `tools/check-self-assessment.py` at `099c7b3f42d073203d9448807860f04c175eccd7` (commit `5583d75c`, an ancestor of the pinned tip, verified with `git merge-base --is-ancestor`), the pinned selftest passes 15 of 15 cases including both new QUALITY 65 cases, and a live run at the tip confirms the round-26 record is excluded. Two honest residuals: the module docstring still documents the pre-fix "from any round" rule, and the checker now exits 1 with 7 mismatches at the tip.

## 1. QUALITY 65 as written

`corpus/QUALITY.md:132` (export at `099c7b3f`): "65. An ordinal check never reads a record written by the round it measures (R26-SELF-AGREEMENT-ORDINAL): a score is checked against the latest measured-outcome record of an earlier round; the declaring round's own outcome record is the next round's reference, and the heading match is anchored to the start of the heading."

## 2. K01 to K06 reference code, by line

The reference set is built by `reference_lines` and consumed by the K01–K06 loop. Quoted verbatim from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-self-assessment.py` (md5 `7610ac4aa62332a7e228ecb869c7e531`, byte-identical in the `git archive` export at `099c7b3f`):

- Line 361: `ROUND_HEADING_RE = re.compile(r"^Round ?(\d+)\b", re.I)` — anchored at the start of the heading text; a heading that mentions a round later in its text ("Notes on the round 1 measured outcome") does not match.
- Lines 364–376: docstring of `reference_lines(lines, declaring_round)` — "Only lines inside a section whose heading (any level) starts with `Round N` ... and carries `measured outcome` (case-insensitive) qualify, and only when N is earlier than the declaring round: a round's own outcome record is the next round's reference, never its own (QUALITY 65, round-26 routed defect 2; added in round 27)."
- Line 377: `candidates, excluded = set(), set()`
- Lines 378–382: for each heading, `text = heading[2].strip()`; `match = ROUND_HEADING_RE.match(text)`; `if match is None: continue` — non-anchored or non-round headings neither add nor exclude lines (their content is inherited from the enclosing section).
- Lines 383–387: `if int(match.group(1)) >= declaring_round: excluded.update(range(heading[0], heading[3]))` — a section of the declaring round or a later round is always excluded, even when nested inside an earlier round's outcome section.
- Lines 388–389: `if MEASURED_OUTCOME in text.lower(): candidates.update(range(heading[0], heading[3]))` — earlier-round outcome sections supply candidate lines (`MEASURED_OUTCOME = "measured outcome"`, line 337).
- Line 390: `return candidates - excluded` — the nested-exclusion subtraction.
- Lines 435–439: `declaring_round` is parsed from the axes-table heading with `ROUND_IN_TEXT_RE` (`re.search` over the last `## Axes - ` section heading); a heading without a round number raises `CannotEvaluate` (exit 2).
- Line 440: `reference = reference_lines(score_lines, declaring_round)`.
- Lines 494–508 (the K01–K06 loop): for each axis, `for index, line in enumerate(score_lines)` skips the axes-table block (`axes_lo <= index < axes_hi`) and any `index not in reference`, then takes the last match of the round-25 transition regex `\b<axis>\b[^0-9|→\n]{0,12}?(\d{1,2})\s*(?:→|->)\s*(\d{1,2})` with both numbers in 0..10; the winning `observed`/`observed_line` feed the check at lines 511–528, where a stated score with no qualifying record is a mismatch with reason "no dated move record" (never a silent pass, never exit 2).

## 3. Live run at 099c7b3f

Command: `cd /fast/scratch/hyaku/tsuku27a2/RevSelfAssessQ65/tree && python3 tools/check-self-assessment.py --revision 099c7b3f42d073203d9448807860f04c175eccd7 --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Exit 1. JSON receipt: `/fast/scratch/hyaku/tsuku27a2/RevSelfAssessQ65/run-099c7b3f.json` (copy at `.ufo/waves/round-27/w2a2/RevSelfAssessQ65/run-099c7b3f.json`).

Result: `status FAIL`, `checked 27`, `mismatches 7`, `declaring_round 26`, `reference_lines 198`, `axes_heading "## Axes — current self-assessment (round 26)"`. Identical check-for-check to the committed receipt `.ufo/waves/round-27/measure/selfassess-q65-75784ea4.json` (the `099c7b3f` refinements commit changed no check outcome). Mismatches and which checks:

- K02 coverage: stated 9, observed none — "no dated move record for coverage: no coverage ordinal transition in any measured-outcome section".
- K06 adjacency: stated 8, observed none — same reason for adjacency.
- K07: stated 48 knowledge notes vs 50 `.md` files under `corpus/knowledge/`.
- K08: stated 2418 SKILL.md lines vs 2436.
- K09: stated 336 SKILL.md table lines vs 348.
- K10: stated 28 lesson files vs 30 under `corpus/lessons/`.
- K11: stated 248 `corpus/README.md` lines vs 256.
- All other checks match: K01 (8=8, observed_line 730), K03 (9=9, line 731), K04 (9=9, line 772), K05 (9=9, line 771), K12–K27.

QUALITY 65 behaving on real data: K01/K03–K05 resolve to SCORECARD.md lines 730, 731, 771, 772, which sit inside `### Round23 measured outcome` (heading line 724) and `### Round 24 measured outcome` (heading line 765) — rounds 23 and 24, both earlier than the declaring round 26. The round-26 record `SCORECARD.md:960` ("Ordinal record, round 26 ... coverage 9 → 9 ... adjacency 8 → 8"), which every one of K01–K06 read before the fix (round-26 report, K01–K06 all at line 960), is now excluded, so K02 and K06 honestly report "no dated move record" rather than self-agreement. SCORECARD.md:960 itself admits coverage and adjacency "had no earlier ordinal transition inside any measured-outcome section ... so this line is their first dated record" — the only earlier-looking transitions (SCORECARD.md:192, 213, 224, 620) sit in non-outcome sections and are correctly ignored.

Selftest: `python3 tools/check-self-assessment.py --selftest --repo <lane>` on the export → exit 0, `selftest PASS`, 15 cases, 0 failures (receipt `selftest.json` next to the run receipt). The two QUALITY 65 cases pass: `own-round-outcome-depth-10` (a `### Round 2 measured outcome` nested inside the earlier `## Round 1 measured outcome` section is excluded; K01 mismatches as required) and `outcome-heading-not-round-anchored` (a non-anchored heading names no dated record). Red-before evidence exists and is non-empty: `.ufo/waves/round-27/measure/selfassess-red-before.txt` (119 bytes) records "old reference_lines with the round-27 cases: FAIL ['own-round-outcome-depth-10', 'outcome-heading-not-round-anchored']". The lesson's defect-2 row (`corpus/lessons/round-27.md:42`) describes exactly the implemented semantics.

## 4. Findings

1. [obs] Stale module docstring (minor). Lines 14–16 of `tools/check-self-assessment.py` still document the pre-fix rule: "The ordinal reference holds only the SCORECARD lines inside a section whose heading (any level, `#` to `######`) carries `measured outcome` (case-insensitive), from any round". The implemented rule requires the heading to start `Round N` with N < declaring round. The docstring is the document the declarations cite ("check set v2 ... declared in SCORECARD.md"); it now mis-describes K01–K06. No behavioral effect.
2. [obs] Formatting hazard (minor, latent). `Round-13 measured outcome` (hyphenated, SCORECARD.md:320) does not match `ROUND_HEADING_RE` (`Round ?(\d+)` allows zero or one space, no hyphen), so round 13's recorded transitions silently contribute no reference lines. Harmless only because rounds 23/24 supply later anchors; a future hyphenated "Round-NN measured outcome" heading would silently drop that round's records, letting an older transition masquerade as the latest. Same class: "Round  16" (two spaces) is also unread, despite the docstring claiming `Round16`/`Round 16` coverage.
3. [inf] K02/K06's "no dated move record" is the correct QUALITY 65 outcome, not a regression: the only dated record for coverage/adjacency was written by round 26, the declaring round, so it is the next round's reference, never its own. These two mismatches are the price of honest anchoring and will clear only when a round ≥ 27 axes table is checked against records including round 26's.
4. [obs] K07–K11 are genuine staleness in the round-26 axes table (corpus grew in rounds 26/27 while the table stayed put); they predate this fix and are unchanged between `75784ea4` and `099c7b3f`.

## 5. What the round-27 report must say about defect 2

- QUALITY 65 is implemented at `5583d75c` and present at the measured tip `099c7b3f`: `reference_lines` admits only sections whose heading starts `Round N` and carries `measured outcome`, requires N < declaring round, and subtracts a same-or-later-round section nested inside an earlier one (lines 361–390, consumed at 440 and 494–508). Green selftest 15/15; red-before receipt `selfassess-red-before.txt` shows the old logic failing both new cases.
- The tool at the tip is not clean: `--revision 099c7b3f` exits 1 with 7 mismatches — K02 and K06 ("no dated move record", the expected QUALITY 65 consequence of excluding the declaring round's own record) plus K07–K11 (stale counts in the round-26 axes table). The report must not claim a zero-mismatch self-assessment, and no calibration credit may be drawn from K01–K06: K02/K06 are mismatches, and the matches K01/K03–K05 now rest on round-23/24 records.
- Disclose the stale docstring (lines 14–16 still say "from any round") and the hyphenated-heading blind spot (`Round-13` at SCORECARD.md:320 is silently not a round heading).

Residual risk: low on the defect itself (mutants and live data agree), moderate on documentation (the docstring mis-describes the rule a future declaration might cite verbatim). Verification gap: the `--selftest` run covers heading anchoring and nesting but not a hyphenated round heading; no lane file currently needs one.

Scope: read=tools/check-self-assessment.py (whole), SCORECARD.md headings+declaration+outcome sections, corpus/QUALITY.md:116-140, corpus/lessons/round-27.md:40-45, committed receipt selfassess-q65-75784ea4.json, selfassess-red-before.txt, w1/RevRoutedDefects.md grep hits, git log/show/merge-base (read-only); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/RevSelfAssessQ65.md, .ufo/waves/round-27/w2a2/RevSelfAssessQ65/run-099c7b3f.json, .ufo/waves/round-27/w2a2/RevSelfAssessQ65/selftest.json, /fast/scratch/hyaku/tsuku27a2/RevSelfAssessQ65/ (export tree + receipts); executed=git archive|tar export at 099c7b3f, python3 tools/check-self-assessment.py --revision 099c7b3f... --repo <lane> (exit 1), --selftest (exit 0), git merge-base --is-ancestor, md5sum, grep/sed reads
Model: devin/swe-2
Installs: none
