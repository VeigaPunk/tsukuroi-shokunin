VERDICT: defect-found

G-2 (self-assessment at tip). The gate is sound and the red is real and fully attributable: at the assigned tip
`f951f288483c1af0cef4afd458488b84cf7a2165` `check-self-assessment.py` exits 1 with **6 mismatches of 27**
(K07 K08 K09 K10 K13 K17). Five of those six are the pending landing-table update for data already committed this
round; the sixth (K10) was already red at the declared base `53b294a`. One table update repairs all six: a measured
simulation of that update in a scratch clone of the lane yields **PASS, 0/27** (receipt `predicted-landing-sim.json`).
The gate must therefore **not** be reported as 27/0 for round 40 until that update lands; conversely, the landing has
a known, measured target.

## 1. Run as instructed (through `run-receipt.py`)

```
python3 tools/run-receipt.py --revision f951f288483c1af0cef4afd458488b84cf7a2165 \
  --out .ufo/waves/round-40/w1/GateSelfAssessment/check-self-assessment-f951f28.jsonl \
  --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin -- tools/check-self-assessment.py --revision '{rev}'
{"out": ".ufo/waves/round-40/w1/GateSelfAssessment/check-self-assessment-f951f28.jsonl",
 "revision": "f951f288483c1af0cef4afd458488b84cf7a2165", "tool": "tools/check-self-assessment.py", "exit_code": 1}
```

Receipt `.ufo/waves/round-40/w1/GateSelfAssessment/check-self-assessment-f951f28.jsonl` (364 lines, sha256
`9cfa4ba60069b652164f30e5ae858b46f38c8d022e11131e638f8a767b2c6c9f`; header `revision` = `tool_revision` = the tip,
footer `exit_code 1`, `timed_out false`). Body: `"checked": 27, "mismatches": 6, "status": "FAIL",
"declaring_round": 39, "axes_heading": "## Axes — current self-assessment (round 39 final measured surface)"`.

## 2. The six mismatches (exact stated vs observed, from the receipt body)

| Check | Cell (SCORECARD.md at tip) | Stated | Observed | Cause |
|---|---|---|---|---|
| K07 | depth row, `:2268` | 60 notes | 61 | `bf23805` added `corpus/knowledge/pacman-exec-environment-r40.md` (C2) |
| K08 | depth row, `:2268` | 3322 `wc -l` | 3324 | `bf23805` added 2 lines to `SKILL.md` (`git diff --numstat a2d7aad f951f28 -- SKILL.md` → `2 0`) |
| K09 | depth row, `:2268` | 885 table lines | 887 | the same two added lines are both pipe-prefixed (C1 and C2 instrument rows) |
| K10 | depth row, `:2268` | 54 lesson files | 55 | **inherited from base**: `53b294a` (round-39 verifier spot-check) added `corpus/lessons/round-39-verifier-spotcheck.md` after the round-39 table was written |
| K13 | operability row, `:2270` | 119 cases | 124 | `c707e35` (C1) added the five mount-table fixtures; selftest prints `TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)` |
| K17 | host-census-gate row, `:2280` | 119 cases | 124 | same count; K17 also enforces the case count (declared at `SCORECARD.md:2026`), not only path existence |

All other checks match, including K01–K06 ordinals 8/9/9/9/9/8, K11 `corpus/README.md` 317, K12, K14, K15, K16,
K18–K27.

### Baseline at the declared base (to separate inherited from new)

```
python3 tools/run-receipt.py --revision 53b294a274656be6479aadf2ec2fee890ded77ce \
  --out .../check-self-assessment-base-53b294a.jsonl --lane <lane> -- tools/check-self-assessment.py --revision '{rev}'
```
Exit 1, `mismatches 1`, status FAIL — **only K10** (`stated 54; corpus/lessons holds 55`). Receipt sha256
`da11bdc57146d229e03c96fa2ecd5bf01ac57adba9b5f6f137d0d74c91fa9930`. So round 40's committed data moved exactly
K07, K08, K09, K13, K17 (five new reds); K10 was already red at base and is not round-40's doing — but the landing
must repair it anyway.

At base the same run also proves the instrument saw 119 selftest cases there: K13 and K17 matched with stated 119.

## 3. Instrument soundness (the red is the lane, not the gate)

`python3 tools/check-self-assessment.py --selftest` → exit 0, `"selftest": "PASS", "failures": [], "cases": 19`, all
19 fixture cases PASS (`instrument-selftest.json`, sha256
`35e28764be9bc6b187d935f0d012745dc1e78343aeed03f08fd114d71e8ac466`). The check set itself behaves as declared on its
stale-count, stale-ordinal, missing-path and cannot-evaluate fixtures.

## 4. Independent recount at the tip (confirmed the observed values, git not working tree)

```
git ls-tree -r --name-only f951f28… corpus/knowledge | grep -c '\.md$'   → 61
git show f951f28…:SKILL.md | wc -l                                      → 3324
git show f951f28…:SKILL.md | grep -c '^|'                               → 887
git ls-tree -r --name-only f951f28… corpus/lessons | wc -l              → 55
git show f951f28…:corpus/README.md | wc -l                              → 317
git show f951f28…:corpus/SOURCES.md | grep -cE '^\| S[0-9]+'            → 225   (base 53b294a: 218)
git diff --name-status a2d7aad f951f28 -- corpus/knowledge              → A corpus/knowledge/pacman-exec-environment-r40.md
git diff --name-status a2d7aad f951f28 -- corpus/lessons                → (empty; the one addition is in 53b294a: A corpus/lessons/round-39-verifier-spotcheck.md)
```

Note the trap: `corpus/lessons/round-40.md` exists in the working tree but is **untracked**, so the gate cannot see it
(`git status --porcelain corpus/lessons` → `?? corpus/lessons/round-40.md`; `git cat-file -e f951f28:corpus/lessons/round-40.md` → fatal, absent in that revision). Working-tree `find corpus/lessons -type f | wc -l` already reads 56.

## 5. Predicted cell values the L1 must write after round 40 lands

"Line" is the tip line of the cell to replace. "Gated" names the check that turns green when the value is right.

| Cell | Line | Now → after landing | Gated | Counting command (run at the landing commit; revision form = what the gate reads) |
|---|---|---|---|---|
| Axes heading | 2262 | `(round 39 final measured surface)` → `(round 40 …)` | K01–K06 `declaring_round` | n/a (heading must name a round; the gate exits 2 otherwise) |
| Axes intro | 2264 | `at the round-39 LOG/SCORECARD commit` → round-40 | — (prose) | n/a |
| depth: notes | 2268 | 60 → **61** | K07 | `git ls-tree -r --name-only <REV> corpus/knowledge \| grep -c '\.md$'` → 61 (tree: `find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l` → 61) |
| depth: SKILL lines | 2268 | 3322 → **3324** | K08 | `git show <REV>:SKILL.md \| wc -l` → 3324 (tree: `wc -l < SKILL.md`) |
| depth: table lines | 2268 | 885 → **887** | K09 | `git show <REV>:SKILL.md \| grep -c '^\|'` → 887 (tree: `grep -c '^\|' SKILL.md`) |
| depth: lessons | 2268 | 54 → **56** if `corpus/lessons/round-40.md` is committed at landing, else **55** | K10 | `git ls-tree -r --name-only <REV> corpus/lessons \| wc -l` → 55 now / 56 after the commit |
| depth: trailing prose | 2268 | `round-39 C2 predicate met with a target defect` → `round-40 C2 …` | — | n/a |
| operability: cases | 2270 | 119 → **124** (twice in the cell text) | K13 | `bash tools/tsukuroi-census.sh --selftest \| tail -1` → `TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)` (30 s, 4 CPUs; observed this session) |
| calibration row | 2272 | `mismatches 0 required at the round-39 tip` → `round-40 tip` | — (prose; K05 reads only the ordinal 9) | `python3 tools/check-self-assessment.py --revision <landing REV>` must print `mismatches 0` |
| Capabilities heading | 2275 | `(round 39)` → `(round 40)` | — | n/a |
| host-census-gate: cases | 2280 | 119 → **124** | K17 | same selftest command as K13 (K17 re-uses the K13 measurement) |
| sources prose (round-40 outcome section) | new | `218 → 225 rows` | — (prose) | `git show <REV>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]+'` → 225 |
| freshness row | 2271 | round-39 wording → round-40 (re-opened libalpm 54d9411 on S219–S225) | — (prose) | n/a |
| coverage row | 2269 | keep README 317; update the parenthetical `(round 39 C1)` → round-40 mount-table fixtures | K11 already matches; recount if README is edited | `git show <REV>:corpus/README.md \| wc -l` → 317 |
| planned (next round) bullet | 2285–2288 | replace the now-done C2/C1 plan with the round-41 plan | — | n/a |

Ordinals do **not** move (K01–K06 stay 8/9/9/9/9/8). The round-40 measured-outcome section may record `depth 8 → 8 …`
freely: with the heading at round 40 the declaring round is 40 and that section is excluded from the K01–K06 reference;
the reference stays at `SCORECARD.md:2171` (coverage), `:2172` (depth) and `:1560` — verified by the simulation in §6
(`declaring_round: 40`, all six still match).

Exact proposed depth/operability rows (post-landing, with `round-40.md` committed):

```
| depth | 8 | 61 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3324 `wc -l` / 887 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 56 files (`find corpus/lessons -type f | wc -l`); round-40 C2 predicate met with a target defect, no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
```
and `PASS (124 cases, 124 passed, 0 failed)` in both the operability row (`:2270`) and the host-census-gate row
(`:2280`).

## 6. The prediction, measured (not assumed)

Scratch clone of the lane (`git clone -q --shared <lane>`, `remote remove origin`, `rev-parse --show-toplevel` ==
clone), the untracked `corpus/lessons/round-40.md` copied in and committed there under fixture identity
`fixture@shokunin.local`, plus exactly the nine replacements in the §5 table (each asserted to match): fixture commit
`699e12b39e85838d198c2ae906f2b5261a5773d1` on top of `f951f28`. Then

```
python3 tools/check-self-assessment.py --revision 699e12b… --repo <clone>
→ {"status": "PASS", "mismatches": 0, "declaring_round": 40}
```
exit 0, 31 s. Receipts: `predicted-landing-sim.json` (sha256 `1746335e01409af9a3b3a4341ac7aecdf2aad8c3a0f31fd0315a73b2af977dcf`),
`predicted-landing.patch` (the exact 16 changed lines, sha256 `c359f85f362ae7111852f7f28b6e530888add21b9c063f09679a44104fe1091f`),
`predicted-landing.stat` (`SCORECARD.md 14 +/-, corpus/lessons/round-40.md 55 +`). The mapping stated → observed is
therefore measured end-to-end: the six reds are exactly the cells in §5. Scratch clone removed; the fixture revision is
not in the lane.

## 7. Risks the L1 must not skip

- **K10's target value depends on the landing commit**: 56 only if `corpus/lessons/round-40.md` is committed with the
  table update (as every prior round did). A table that says 56 while the lesson stays untracked is a K10 mismatch in
  the other direction; the working-tree `find` command reads 56 and would hide the mistake, so count from git.
- **SKILL.md's 3324/887 will change again if the landing appends to `SKILL.md`** (e.g. a "Historical instrument pins —
  round 40" block, as round 39 did). Recount at the landing commit; the two round-40 instrument rows in the diff are
  already inside 3324/887.
- **The census selftest is load-sensitive in this lane's history** (`SCORECARD.md:1558` records one load-dependent
  failure on a first run). K13/K17 flip to mismatch if the PASS line is not printed; the gate has no retry. Three
  independent runs this session printed 124/124 PASS (tip gate, base gate, direct working-tree run).
- **Two K13/K17 statements, one command**: both rows carry the case count; both must be updated together.

## 8. Execution notes, no-harm

- Read-only on the lane: no tracked file was modified, created or deleted; no git/jj mutating command in the lane; the
  only lane writes are this report and the six receipts in `.ufo/waves/round-40/w1/GateSelfAssessment/` (all < 14 kB).
- No host change, no pacman, no sudo, no service or sysfs touch; nothing installed. Scratch was
  `/fast/scratch/hyaku/tsukuroi-r40/GateSelfAssessment/` with `TMPDIR` set to it, removed at the end (verified absent);
  no `/tmp` path used as evidence.
- Not done, stated plainly: I did not run the gate at the real landing commit (it does not exist at dispatch); §6 is a
  simulation of it, not the landing. I did not edit the lane's SCORECARD.md. I did not re-run the two claim counters
  (C1/C2) — other seats own those.
