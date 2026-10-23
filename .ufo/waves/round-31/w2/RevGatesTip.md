# Round 31 wave 2 — RevGatesTip gate receipts at f3a5723a988bf1c2835985880e7a38d477462cd0

Verdict: **fails on one gate, otherwise holds.** All receipts ran at `f3a5723a988bf1c2835985880e7a38d477462cd0` via `tools/run-receipt.py` (sandbox clone, `--lane /fast/scratch/hyaku/tsukuroi-r31/RevGatesTip/repo`) except the sources census, which validates the live fleet root as specified. `sources-census.sh validate` **regressed** (exit 0 → 1, ten new E12 rows S164–S173 outside the Registry section). `check-self-assessment` is still FAIL exactly as expected (K10 pending the round-31 axes table) but its mismatch set grew from 1 to 4 (K07/K08/K09 also now mismatch, same root cause). All other gates PASS unchanged vs the start receipts (`.ufo/waves/round-31/w1/ExecGatesStart/`).

Receipt copies: `.ufo/waves/round-31/w2/RevGatesTip/` (`check-self-assessment.jsonl`, `check-registry-coverage.jsonl`, `check-recheck-commands.jsonl`, `check-owed-statements-r29.jsonl`, `probe-git-env-residual-r30.jsonl`, `probe-git-env-leak.jsonl`, `tsukuroi-census-selftest.jsonl`, `sources-census-validate.txt`).

## Findings (by severity)

**1. [finding] sources-census validate regressed: exit 0 → 1, ten E12 rows S164–S173 outside the `## Registry` section.**
- Start receipt `.ufo/waves/round-31/w1/ExecGatesStart/census-start.txt`: 28 `W04` warnings, one `tsukuroi ok …/corpus/SOURCES.md` row, `EXIT_CODE=0`.
- Now: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 1; output `/fast/scratch/hyaku/tsukuroi-r31/RevGatesTip/sources-census-validate2.txt` (copied to `.ufo/waves/round-31/w2/RevGatesTip/sources-census-validate.txt`) has the same 28 `W04` rows (lines 1–28), then ten new `E12 S164…S173 row outside Registry section` rows (lines 29–38) and no `ok` row. The 28 W04 lines are byte-identical to the start file (diff of the two run outputs: IDENTICAL), so the only delta is the E12 block.
- Cause confirmed in the validator: `scripts/sources-census.sh:621` `printf "%s\tE12\t%s row outside Registry section\n",lane,id` runs for row-shaped sources outside the `## Registry` section (comment at line 30 `E12 row-shaped source outside the ## Registry section`).
- The rows are committed at the lane tip, not working-tree noise: at `f3a5723` (`/fast/scratch/hyaku/tsukuroi-r31/RevGatesTip/repo/corpus/SOURCES.md`) the headings are `## Registry` (line 3), `## Paths` (171), `## Search log` (178), `## Leads (unopened)` (238), and S164–S173 sit under `## Leads (unopened)` (lines 258–267), outside `## Registry` (S160–S163 are inside, lines 166–169). The live file has the same layout today. [obs]
- The same ten rows were introduced by the wave-1 integration commit `13ca52d0` ("S164-S173 … registry" in its summary), so the E12 failure is baked into the revision under attack. [inf]

**2. [finding] check-self-assessment still FAIL (exit 1) as expected, but the mismatch set grew from K10-only to K07+K08+K09+K10.**
- Start receipt `.ufo/waves/round-31/w1/ExecGatesStart/check-self-assessment.jsonl`: `mismatches: 1`, only K10 (36 stated vs 37 observed lesson files), exit 1.
- New receipt `.ufo/waves/round-31/w2/RevGatesTip/check-self-assessment.jsonl` line 4–6: `checked: 27`, `mismatches: 4`, `status: FAIL`, exit 1:
  - K07 (lines 72–79): depth row states 51 knowledge notes; `corpus/knowledge` holds 52 `.md` files.
  - K08 (80–88): SKILL.md stated 2672 lines; observed 2743.
  - K09 (89–97): SKILL.md stated 517 table lines; observed 574.
  - K10 (98–106): depth row states 36 lesson files; `corpus/lessons` holds 38.
- Per the assignment, K10 is expected to fail until the round-31 axes table lands — confirmed, it still does (36 vs 38; start was 36 vs 37). K07–K09 are the same condition: the axes table still declares round 30 (`axes_heading: "## Axes — current self-assessment (round 30)"`, `declaring_round: 30`, lines 7–8) while round-31 content growth changed the observed counts. [inf] Not a separate defect, but the gate's failure signature changed (1 → 4 mismatches), so the L1 should expect the axes-table landing to correct all four, not just K10.

**3. [obs] All remaining gates PASS, unchanged vs start.**
- `check-registry-coverage`: exit 0, `status PASS`, registered 45/45, findings 0 (last line `{"branch":"master","branch_tip":"f3a5723…","counts":{"findings":0,"missing":0,"registered":45,"rows_total":45,"tools_total":45},"findings":[],"status":"PASS"}`). **Improved** over start (which FAILed with `REGISTRY-ROW-MISSING` for `tools/check-btrfs-repair-r31.py` and `tools/probe-git-child-env-r31.py`).
- `check-recheck-commands`: exit 0, `status PASS`, findings 0, flagged 0 (counts now file_count 52 / clean_count 36 vs 51/35 at start; `invocation_count` 81 both).
- `check-owed-statements-r29`: exit 0, 12/12 items marked, `unmarked []` (identical shape to start).
- `probe-git-env-residual-r30`: exit 0, `targets 11, pairs 33, leaking 0, harness_errors []` — identical to start receipt (11 targets, 33 pairs, 0 leaking).
- `probe-git-env-leak`: exit 0, `targets 8, leaking 0, leaking_tools []`, all `canary_changed: false` (no spurious "canary fingerprint changed" verdicts this run; start: 8 targets, 0 leaking).
- `tsukuroi-census.sh --selftest`: exit 0, last line `TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)` — identical to start.

## Verification notes / gaps
- First attempt omitted the tools' required `--revision` argument; run-receipt.py wrote tool exit 2 (`CANNOT_EVALUATE`/usage) receipts. Those were discarded and all gates rerun with `--revision {rev}` (and `--lane {lane}` where the tool takes one), matching the start receipts' argv. The JSONL files in the seat dir are the rerun results.
- The fleet repo HEAD moved during this run (a `b304b8e` wave-2 repair commit appeared); the receipt runs are pinned to `f3a5723` via the sandbox clone, and a rerun of the sources census after that commit landed still fails identically (diff of the two validate outputs: IDENTICAL), so finding 1 is not a transient.
- [unk] None material: the two probes exercised the same target sets as the start receipts (11 and 8 tools), so no new tool was added to either probe's scope at this revision.

Scope: read=.ufo/waves/round-31/w1/ExecGatesStart/* (8 receipts), tools/run-receipt.py, generated receipts under /fast/scratch/hyaku/tsukuroi-r31/RevGatesTip/, corpus/SOURCES.md (live and at f3a5723), scripts/sources-census.sh, read-only git log/status/diff on the fleet repo; wrote=.ufo/waves/round-31/w2/RevGatesTip.md, .ufo/waves/round-31/w2/RevGatesTip/*.jsonl (7) + sources-census-validate.txt; executed=run-receipt.py × 7 (each tool at f3a5723), sources-census.sh validate × 2, read-only git commands.
Model: not exposed
Installs: none
