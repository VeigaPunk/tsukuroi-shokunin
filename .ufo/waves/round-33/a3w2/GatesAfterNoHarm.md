# GatesAfterNoHarm — no-harm re-run of six gates at f761fade (round 33, a3w2)

Verdict: two of six gates got worse than base — check-adjacency-anchors (exit 0 → 1, INBOUND-CLASSIFICATION-WRONG) and check-recheck-commands (exit 0 → 2 CANNOT_EVALUATE, E-RECHECK-MISSING) — both attributable to c8fcfbf662db6debc6d7128c166ced31ca3176cf; check-self-assessment stayed exit 1 but its findings grew 1 → 4; check-registry-coverage improved (1 → 0); check-pause-gate and report-red-causes are unchanged.

Method: each gate re-run through `tools/run-receipt.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision f761fade8a452ec9dd0831be7743601b0adda3e5 --tool-revision f761fade8a452ec9dd0831be7743601b0adda3e5 --timeout 1900` with the registry `--revision <REV>` argv form `tools/<gate>.py --revision '{rev}'` (identical argv shape to the base receipts in `.ufo/waves/round-33/a3w1/ExecGateBaselines/base-*.jsonl`, which ran at 9c89ff4f). Receipts: `.ufo/waves/round-33/a3w2/GatesAfterNoHarm/<gate>.jsonl`. No timeouts; stderr empty in all six.

## Results (base exit → tip exit)

| gate | base | tip | delta |
|---|---|---|---|
| check-adjacency-anchors | 0 PASS | 1 FAIL | worse |
| check-pause-gate | 1 | 1 | same finding |
| check-registry-coverage | 1 FAIL | 0 PASS | better |
| check-recheck-commands | 0 PASS | 2 CANNOT_EVALUATE | worse |
| check-self-assessment | 1 (1 mismatch, K10) | 1 (4 mismatches) | worse in findings |
| report-red-causes | 0 | 0 | same |

## Findings

1. [obs] check-adjacency-anchors regressed: base exit 0 → tip exit 1. Finding `INBOUND-CLASSIFICATION-WRONG` at `corpus/knowledge/adjacency-anchors-r19.json:inbound[100]` (receipt `.ufo/waves/round-33/a3w2/GatesAfterNoHarm/check-adjacency-anchors.jsonl` line 2): "classification RESOLVES is inconsistent: found_line is not an occurrence of evidence_quote". Row IN-101 is tameshi's `.ufo/waves/round-18/w1/C04GitEnvPriorArt.md:44` pointer to `tools/_revision.py:62-72` whose evidence_quote is `env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}` — the ambient-copy expression c8fcfbf6 replaced with the allow-list builder (`git show f761fade:corpus/knowledge/adjacency-anchors-r19.json`, row field `found_line` 63 vs new allow-list lines 62-66). The row was left classified RESOLVES instead of DRIFTED/UNRESOLVABLE. Counts moved: inbound_classified 114 → 113, RESOLVES 97 → 96; outbound 10/10 still portable. Attribution: c8fcfbf6 changed the pinned bytes without reclassifying the anchor.

2. [obs] check-recheck-commands regressed: base exit 0 → tip exit 2 CANNOT_EVALUATE. Finding `E-RECHECK-MISSING` at `corpus/knowledge/kill-oom-boundary-r33.md`: "no recheck: line" (receipt `check-recheck-commands.jsonl`). The gate reads the last `recheck:` line of every `corpus/knowledge/*.md` file (tool line 660: `raise Cannot("E-RECHECK-MISSING", path, "no recheck: line")`); the C2 note added by c8fcfbf6 carries zero `recheck:` lines (`git show f761fade:corpus/knowledge/kill-oom-boundary-r33.md | grep -c 'recheck:'` = 0). file_count collapsed 52 → 0, invocation_count 81 → 0: the gate aborts before scanning anything.

3. [obs] check-self-assessment stayed exit 1 but worsened from 1 mismatch to 4: K07 notes stated 52 observed 53 (kill-oom-boundary-r33.md added), K08 SKILL.md lines stated 2812 observed 2870 (round33 registry table appended), K09 table lines stated 628 observed 678, K10 lessons stated 40 observed 41 (same mismatch as base). All four read the round-32 axes table, which is stale at tip — prior rounds cleared this staleness by appending the round's own axes table at close [inf]. Receipt `check-self-assessment.jsonl`.

4. [obs] check-pause-gate unchanged: exit 1 with the same single finding `GATE-PREMISE` at `P3:verdict-unverified-not-counted`; P1-P5 verdicts byte-identical to base. Tool bytes changed per the declared pin bump: tool_sha256 54938539… → eb839864… (`_revision.py` sha256 pin at check-pause-gate.py:245 bumped to fc861ec8 in c8fcfbf6). [obs] `checkupdates_attachment_pinned: true` at both revisions.

5. [obs] check-registry-coverage improved: base exit 1 (REGISTRY-ROW-MISSING at tools/probe-child-env-allowlist-r33.py; registered 47, missing 1) → tip exit 0 (registered 48, rows_total 48, missing 0). f761fade's round33 registry table added the probe row.

6. [obs] report-red-causes unchanged: exit 0; attributed_findings 268, attributed_with_recorded_operation 267, attributed_seat_level 1 at both revisions. Tool sha256 0c4785ac… → e84c8af6… (the same fc861ec8 pin bump at report-red-causes.py:203).

7. [obs] Context: at run time lane HEAD was 783d79e05a525995158d0cc85bf101e8d2078277, one commit past the assigned f761fade; all six receipts pin `revision f761fade` while their `branch_tip` field names 783d79e0. The regressions above are in files f761fade itself carries (c8fcfbf6 is its parent), so the verdict stands at the assigned revision [inf]; whether 783d79e0 repairs either gate was not measured [unk].

Residual risk / verification gaps: single run per gate (deterministic checkers, no flaky evidence seen); the 783d79e0 tip commit's effect on the two regressed gates is unmeasured; check-self-assessment's extra three mismatches will presumably clear when the round-33 axes table is appended — that is expectation, not measurement.

Scope: read=SCORECARD.md round-33 declaration at 9c89ff4f, six base receipts under .ufo/waves/round-33/a3w1/ExecGateBaselines/, tools/run-receipt.py, tools/check-recheck-commands.py E-RECHECK-MISSING site, corpus/knowledge/adjacency-anchors-r19.json inbound[100] and kill-oom-boundary-r33.md at f761fade, commits 5a967ce..f761fad; wrote=.ufo/waves/round-33/a3w2/GatesAfterNoHarm/{check-adjacency-anchors,check-pause-gate,check-registry-coverage,check-recheck-commands,check-self-assessment,report-red-causes}.jsonl and .ufo/waves/round-33/a3w2/GatesAfterNoHarm.md; executed=read-only git log/show/grep/cat-file/rev-parse/status and six `python3 tools/run-receipt.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision f761fade8a452ec9dd0831be7743601b0adda3e5 --tool-revision f761fade8a452ec9dd0831be7743601b0adda3e5 --out <seat>/<gate>.jsonl --timeout 1900 -- tools/<gate>.py --revision '{rev}'` runs.
Model: not exposed
Installs: none
