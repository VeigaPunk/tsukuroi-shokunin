# RevSpotcheckRouting — routing review of round-30 spot-check defects 1–6 into round 31

Verdict: **partly holds**. Defects 1–5 are each routed to a declaration sentence, a wave-1 item, and (for 4 and for the C1/C2 controls) committed evidence; defect 6 is deliberately unrouted (stays owed). One sub-item of defect 5 — the low-power enclosing-repo channel for the two owed-statement batteries — has **no declaration sentence and no wave-1 item**; it is named only in the spot-check itself. QUALITY 80, the erratum, and the QUALITY 78/79 note exist only as in-flight wave-1 drafts, not yet integrated at the tip (expected at this point in wave 1).

## Per-defect routing

### Defect 1 — able-to-fail depth target
- Declaration sentence: `SCORECARD.md:1217` ("1 the able-to-fail depth target is this declaration's C1 design plus QUALITY 80 (a novelty and do-nothing-control criterion grounded in a round-31 Mistakes row)"); design in `SCORECARD.md:1198,1205,1211` (frozen predicate `new_sourced`; K0–K4/K1 below 8, K5 = 8; sealed builder).
- Wave-1 items: `ScribeMistakeQuality` (drafts `quality-80.md`, `mistake-row.md` with row `R31-DEPTH-UNFALSIFIABLE`), `MutCounterC1` (rebuilds K2/K3/K4 + positive control), `RevControlsC1` (re-derives controls).
- Committed evidence (before data, tip `8cff9e7`): `.ufo/waves/round-31/measure/controls/c1-K0-base.jsonl` … `c1-K5-reader-ceiling.jsonl` — K0–K4/K1 exit 1 with per-row `new_sourced: false`; K5 exit 0 with `new_sourced: 8`; headers carry `tool_revision f4861f4d`, `tool_sha256 4f69a109…` (matches `sha256sum tools/check-btrfs-repair-r31.py`). `measure/controls/sealed-builder.sha256` committed; `measure/c1-before-f4861f4d….jsonl` exit 1.
- Status: controls evidence committed; QUALITY 80 / Mistakes row still drafts at `w1/ScribeMistakeQuality/` (quality-80.md, mistake-row.md), not yet in `corpus/QUALITY.md` / `corpus/lessons/round-31.md` (grep: no "80." criterion, no round-31 lesson, no R31-DEPTH-UNFALSIFIABLE at tip).

### Defect 2 — duplicate declaration erratum
- Declaration sentence: `SCORECARD.md:1217` ("2 an erratum for the duplicate round-30 declaration at `SCORECARD.md:1181-1194` (appended, never rewritten)").
- Wave-1 item: `ScribeMistakeQuality` (drafts `scorecard-erratum.md`).
- Committed evidence: none yet; grep for "erratum" in `SCORECARD.md` finds the routed sentence but no appended erratum. Draft exists at `w1/ScribeMistakeQuality/scorecard-erratum.md`.
- Status: in-flight; not yet integrated.

### Defect 3 — dangling QUALITY 78/79 pointers
- Declaration sentence: `SCORECARD.md:1217` ("3 the dangling QUALITY 78 and 79 lesson pointers are corrected by an appended note").
- Wave-1 item: `ScribeMistakeQuality` (drafts `quality-7879-note.md`).
- Committed evidence: none yet; at tip `corpus/QUALITY.md:149,151` still cite `R30-GIT-RESIDUAL-CHANNELS` / `R30-SOURCED-ROWS` (the IDs absent from `corpus/lessons/round-30.md`). Draft exists at `w1/ScribeMistakeQuality/quality-7879-note.md`.
- Status: in-flight; not yet integrated.

### Defect 4 — leftover attack fixtures
- Declaration sentence: `SCORECARD.md:1217` ("4 the three untracked round-30 symlink fixtures are deleted and the three committed `__pycache__/*.pyc` files are removed").
- Wave-1 item: none (L1 direct action, not a seat).
- Committed evidence: `.ufo/waves/round-31/l1/leftovers-removed.txt` (committed in `8cff9e7`); deletions committed in the same tip: `git diff 2077e2fa..8cff9e7 --name-status` shows `D .ufo/waves/round-30/w1/CritCounterShapes/__pycache__/shapes.cpython-314.pyc`, `D …/w2/CritCounterV2/w1rerun/__pycache__/shapes.cpython-314.pyc`, `D …/…/shapes.cpython-315.pyc`.
- Working-tree verification: `git status --porcelain` clean for round-30 (only the three round-31 `??` paths `w1-spec.json`, `w1-dispatch.json`, `w1/`); `find .ufo/waves/round-30 -type l` → none; S900.txt absent from G1/G2/G3 fixture dirs (`ls` shows only regular S901–S909 files); `find .ufo/waves/round-30 -name '*.pyc'` → none; `git ls-files '*.pyc'` → empty.
- Verdict: defect 4 fully closed with committed evidence.

### Defect 5 — C2 probe gaps
- Declaration sentence: `SCORECARD.md:1217` ("5 the probe gaps are claim C2 (stdout parity, `LD_PRELOAD`/`PYTHONPATH`, dropped `.git` pointer, system-config scope through the child contract); repository-local `include`/`core.fsmonitor` stays owed and is named as such").
- Wave-1 items: claim C2 (counter `tools/probe-git-child-env-r31.py`, sha256 `b168b9b8…` matching receipt headers; channels `loader-env`/`child-contract`/`dotgit-pointer`, `CHANNELS` at probe line 77) implemented by `ExecScrubA/B/C/D` (fix contract on the eleven tools), falsified by `CritProbeC2Design`, `MutProbeC2`, `SentinelChildEnv`; owed repository-local include/fsmonitor evidence produced by `SentinelRepoLocal` (its prompt: "This channel is NOT in the frozen claim; it is evidence for the owed item").
- Committed evidence: `measure/c2-before-f4861f4d….jsonl` (leaking 11, pairs 33, harness_errors []) and controls `c2-H1.jsonl` (leaking 1/3) / `c2-H2.jsonl` (leaking 0/3), both with `tool_sha256 b168b9b8…`.
- Gap: the spot-check's defect-5 bullet "the low-power enclosing-repo channel for both owed-statement batteries" (`corpus/lessons/round-30-verifier-spotcheck.md:188`) has **no declaration sentence and no wave-1 item** — no match in `w1-spec.json`/`w1-dispatch.json` (grep low-power/enclosing → 0 hits), not in the probe, and not in the routed-items line. The declaration names only repository-local include/fsmonitor as owed.
- Verdict: 5 of 6 bullets routed; the low-power enclosing-repo bullet is unrouted (finding 1 below).

### Defect 6 — carried owed items
- Declaration sentence: `SCORECARD.md:1217` ("6 the carried items stay owed unless a wave-1 seat lands one with a receipt").
- Wave-1 items: none (deliberate). No item addresses counter-v2 shapes, `check-report-receipts.py` over-reporting, S155/S130 or S158/S133 merging, or `run-receipt.py` LOW findings (grep of all 34 prompts: no hits).
- Verdict: consistent with declaration; defect 6 has no item by design. Not a mis-routing, but named so integration never mistakes it for addressed.

## Items not matching their defect
- None. `ScribeMistakeQuality` matches routed 1/2/3 exactly; `SentinelRepoLocal` matches the owed include/fsmonitor channel; the executor/critic/sentinel items match claim C2. No item claims to implement a routed item it does not.

## Findings
1. [obs] Defect-5 sub-item "low-power enclosing-repo channel for both owed-statement batteries" (spotcheck line 188) is not routed: absent from `SCORECARD.md:1217`, from `w1-spec.json` (all 34 prompts), from `w1-dispatch.json`, and from the probe. It is neither a claim, nor named owed.
2. [obs] Defects 1/2/3 evidence is still draft-only at `w1/ScribeMistakeQuality/` (quality-80.md, mistake-row.md, quality-7879-note.md, scorecard-erratum.md); none is integrated at tip (no QUALITY 80, no round-31 lesson, no erratum in SCORECARD, no appended note in QUALITY 78/79). Wave 1 is in flight, so this is expected, not a defect.
3. [obs] C1/C2 control receipts are committed before data with correct headers (tool_revision f4861f4d; tool_sha256 4f69a109… / b168b9b8…; K0 base at revision 2077e2fa; K1/K5 sealed-control revisions); K0–K4/K1 all exit 1 with `new_sourced` false, K5 exit 0 with `new_sourced: 8`; C2 before 11/33, H1 1/3, H2 0/3.
4. [obs] Defect 4 fully verified: three symlinks gone (worktree has zero symlinks under round-30), three tracked .pyc deleted and committed, `leftovers-removed.txt` committed, `git status --porcelain` clean for round-30.
5. [inf] Defect 6's "stays owed" routing is coherent with the declaration, but with no item and no receipt the carried items remain exactly as unaddressed as at round-30 close; if the round intends them closed, a later wave must land them.

## Residual risk / verification gaps
- The correctness of the QUALITY 80 text, the erratum/ and the 78/79 note (drafts) is not yet checkable against the lane; verify after L1 integration.
- Whether the omitted low-power enclosing-repo channel should be added as a named owed item or a claim is an orchestrator decision; it is currently silent.
- Deep conformance of the frozen predicates (declaration sentence vs counter docstring vs receipt `predicate` field) is the RevDeclaration seat's scope; here I only verify the predicate label `new_sourced` appears in counter docstring (line 5/7) and receipts, and the probe docstring/code carry the three channels and `leaking` conditions (lines 20–48).

Scope: read=round-30 spotcheck lesson, SCORECARD.md round-31 section, w1-spec.json (all 34 items), w1-dispatch.json, l1/leftovers-removed.txt, measure/control receipts (all c1-K*, c2-H*, c1/c2-before), QUALITY.md 78/79, tools/check-btrfs-repair-r31.py, tools/probe-git-child-env-r31.py, ScribeMistakeQuality drafts, round-30 fixture dirs; wrote=.ufo/waves/round-31/w1/RevSpotcheckRouting.md; executed=git status/ls-files/diff/log, git grep, sha256sum, python json reads, find, ls.
Model: not exposed
Installs: none
