# ScoreReview — tsukuroi round 12 (score delta review)

Lane: ScoreReview (leaf, read-only). Repo: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin.
HEAD at review: `b76b5c3` (spec baseline `b76b5c377eaee3e3d8d47fdddde977828d05dbd5` matches). Working tree: only `.ufo/waves/round-12/` untracked; no source, census, SKILL, SCORECARD or LOG edits by round 12 yet.
Tools: none installed or upgraded. Tests/census not run (contract: no test runs mid-flight; parent runs once after integration). Every count below is a static read/count, not a verification.

## 1. Outcome

**Unchanged for all axes in this review.** No round-12 claim has landed, so no after-state exists to score. The defensible delta is conditional and bounded (section 5). No PASS is claimed for C1 or C2.

## 2. Authoritative current scores (what the lowest-axis obligation reads)

Latest authoritative append: SCORECARD.md section `## Fleet round 1 — post-review claim corrections (2026-10-19)`, measured at `459e3ce` (ancestor of HEAD, verified: `git merge-base --is-ancestor 459e3ce HEAD` → yes).

| Axis | Score now | Source |
|---|---|---|
| depth | 8 | Axes table row (`SCORECARD.md` final self-assessment, r4 last change); not re-moved by any later append |
| adjacency | 8 | post-review claim A (7→8) |
| coverage | 9 | post-review claim B (8→9) |
| operability | 9 | final self-assessment, r11 |
| freshness | 9 | post-review claim C (8→9) |
| calibration | 9 | final self-assessment, r10 |

**Conflict to fix before any round-12 append:** the `## Axes — final self-assessment` table still reads adjacency 7, coverage 8, freshness 8 (SCORECARD.md:45–52). The post-review section supersedes those values; the older table was not corrected. Parent should record the supersession in a dated append rather than rewrite history.

## 3. Lowest-axis obligation (AXES.md:33–38)

- Lowest non-retired axes: **depth 8 and adjacency 8, tied**. Retired: none.
- Round-12 C2 works **depth** → satisfies "at least one claim works the lowest-scoring non-retired axis". With a tie, either tied axis qualifies; depth is compliant.
- Stagnation nudge (AXES.md:68–73) does **not** apply: not every owned axis is ≥ saturation line 9 (depth 8, adjacency 8; SCORECARD.md:175–178 states this).
- Claim count 2 (within 1–3). Distinct axes: operability (C1), depth (C2). Compliant.

## 4. Causal separability C1 vs C2 (AXES.md:30–32)

- **Separable only if** C2's decision matrix is built from direct probes (`stat -c '%a %U:%G' /`, `getfacl -p /`, `systemctl cat limine-snapper-sync.service`, `journalctl … -g 'create subvolume failed'`, `snapper list-configs`, `pacman -Qo /`) and **does not cite a new census line** from C1.
- **Not separable** if a C2 branch reads "census root-mode arm" output, or if a C1 fixture asserts EACCES mechanism text. Either makes one claim's verification depend on the other landing. Reject that wiring.
- Current evidence supports separability: `corpus/knowledge/snapper-eacces-mechanism.md` already uses direct probes (lines 12–14, 56–58); the census has no root stat probe (see §6).

## 5. Proposed score delta (bounded)

| Axis | Proposed | Condition / reason |
|---|---|---|
| depth | **unchanged at 8 now**; at most **+1 (8→9)** after C2 lands | Scale is undefined: no rubric maps counts to 0–10 (AXES defines the axis, not a count-to-score map). A +1 step is the most one claim can defensibly move one axis. +2 is not defensible. Requires: ≥4 decision branches each with a source anchor, one discriminating direct probe, and an explicit falsifier; plus independent replay (author-side seat output does not count as independent). |
| operability | **unchanged at 9** | C1 closes a measured blind spot (root metadata 0→1 finding) and is a real verdict improvement, but the axis is at saturation line 9 and the recorded ceiling (D12 `--identity` not landed) remains. A 9→10 claim has no rubric support. Record C1 as "improved, score unchanged" with the before/after finding counts. |
| adjacency | unchanged (not a round-12 claim) | Tied lowest at 8; this review did not re-score it. |

**Harm check:** neither claim should move any axis down. Re-check after landing: freshness 9 and coverage 9 must not be touched by C1/C2 edits to SKILL.md/census.

## 6. Baselines measured now (static, read-only)

| Measure | Value now | Scorecard claimed | Note |
|---|---|---|---|
| census `tools/tsukuroi-census.sh` lines | 2402 (`wc -l`), 2403 py-lines | 2402 | unchanged |
| SKILL.md `wc -l` | **1673** (`wc -l`); 1674 py-lines | 1631 (SCORECARD depth row, r11) | **stale; depth-row pointer does not reproduce** |
| SKILL.md `^\|` lines | 61 incl. header/separators; 54 data rows | 55 (`grep -c '^\|'`, r11) | stale |
| knowledge notes `corpus/knowledge/*.md` | 30 | 24 (r11) | expected after fleet r1 adds |
| census root metadata probes (`stat -c %a` / `getfacl` on `/`) | **0** | — | C1 baseline 0 confirmed |
| SKILL EACCES decision rows | **1** pointer row (SKILL.md:1659), no branch matrix | — | C2 baseline 0 matrix branches |
| EACCES / errno13 mentions across SKILL, knowledge, census, PROVINCE | 20 | — | mostly evidence/narrative, not a decision table |
| SKILL data rows with source anchor + numeric/exit token (heuristic) | 14 of 54 | — | exploratory counter only, not authoritative |

## 7. Counting-command review (test-count-as-quality / token-count risk)

- **Depth row (SCORECARD r4/r11) cites:** note count, `wc -l` of census and SKILL, **80 selftest cases**, "every rule cited". Note count, file line count and test-case count are size/volume measures, not depth. The row is also stale (SKILL 1631 vs 1673). **Replace with a finite decision-row counter:** SKILL table data rows that carry (a) a literal threshold or exit/state token and (b) a `corpus/knowledge/` or `S0NN` source anchor. Baseline heuristic is 14 (§6); C2 must move it by the number of new matrix branches, each with a discriminating probe, not by line/token totals.
- **Operability row cites:** `--selftest` 80/80 and six-plane live rollup. Selftest case count is test-count-as-quality: it can rise without any new live behavior. **Use instead:** for each C1 fixture class (`/` 0755, `/` 0555, `/` unreadable) a recorded run with exit code and the emitted verdict/label, showing three distinct outcomes. Cite that triple, not a case total.
- Do not count "EACCES" token hits as branches (20 hits, mostly narrative).

## 8. Risks and verification gaps

1. **No landed claim.** Every positive delta above is conditional. Parent must not append a depth/operability move from plans or dispatch files.
2. **Stale depth evidence** (SKILL 1631/55 vs measured 1673/61). Must be re-derived in the round-12 append; the stale row must not be reused.
3. **Two conflicting axes tables** in SCORECARD (see §2).
4. **Discernment conflict (outside my axes, flagged for calibration):** `corpus/lessons/round-1-verifier-spotcheck.md:17` says "discernment improved"; `corpus/lessons/round-1.md:19` and the SCORECARD say "discernment unchanged". The spot-check's verifiers are dispatched agents (W3ReviewTsukuroi), which AXES.md:47–49 says do not count as the non-author reviewer. No learning credit should follow from it.
5. **Adjacency tie input verified:** the mori receipt cited for claim A exists at sibling HEAD `6531ac6` (`mori-shokunin/PROVINCE.md:58`, `TSUKUROI-F1-MEM-01`; counts 1 each in PROVINCE/SCORECARD/LOG). The cited ref `20e2255` exists as a commit. The kaika worktree path in SCORECARD (`.tower/worktrees/kaika/mori-shokunin`) is **absent** here, so the SCORECARD's own command is not reproducible in this environment. The receipt text says `prepared` with acknowledgement/acceptance unobserved, so no acceptance credit follows.
6. **Out-of-scope report not verified:** the spot-check reports a second bare `pacman -Sy` at `pacman.log:2287` (2026-10-18). Not checked by this review; it is operator-safety context for the update gate, not a score input.
7. **Unrun:** census selftest, live census, and any C1/C2 fixture. Nothing here is a test result.

## 9. Checks for parent after integration (once, not mid-flight)

- `bash tools/tsukuroi-census.sh --selftest` and the three C1 fixture runs (0755/0555/unreadable), exit codes recorded.
- Re-count SKILL data rows with source anchor + threshold token; confirm C2 branches ≥4 each with a probe and a falsifier.
- Confirm C2 text contains no census-output dependency (grep for census arm names inside the EACCES matrix).
- Confirm no edit touched freshness/coverage rows.

Installs/updates in this review: none.
