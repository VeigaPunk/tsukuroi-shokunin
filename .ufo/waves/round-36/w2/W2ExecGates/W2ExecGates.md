# W2ExecGates — QUALITY 77 gate receipts

Measured revision and tool revision for all receipts: `c052bb7d41ced49aa888817069afd804eccfecf1`. All seven were invoked through `tools/run-receipt.py`; receipt JSONL files are alongside this report.

## Results

| Gate | Exit | Result |
|---|---:|---|
| `check-self-assessment` | 1 | FAIL; 5 mismatches / 27 checks. First mismatch: K07, depth row states 55 knowledge notes vs 56 observed. K10 specifically reports 46 lesson files stated vs 48 observed (`SCORECARD.md:1570`). Other mismatches: K08, 3009 vs 3060 `SKILL.md` lines; K09, 784 vs 788 pipe-prefixed lines; K11, 256 vs 269 `corpus/README.md` lines. |
| `check-registry-coverage` | 1 | 51 missing registry rows / 53 tools, 2 registered. First finding: `REGISTRY-ROW-MISSING` for `tools/_revision.py`. |
| `check-knowledge-header` | 0 | 56 notes; all 56 clean and complete; no findings. |
| `check-recheck-commands` | 0 | PASS; 40 clean files, 81 invocations, 0 flagged. |
| `check-adjacency-anchors` | 0 | PASS; 10/10 outbound portable, 114/114 inbound classified, no findings. |
| `report-red-causes` | 0 | Receipt succeeded, but its payload reports underlying checker exit 2 / `CANNOT_EVALUATE`, with 268 retained findings (266 `SCOPE-PATH-DENIED`, 1 `SCOPE-SCHEMA`, 1 `SCOPE-TRACE-INCOMPLETE`). This is attribution of recorded round-23 findings, not a clean underlying checker result. |
| `check-pause-gate --revision c052bb7d41ced49aa888817069afd804eccfecf1` | 1 | One `GATE-PREMISE`: inherited P3 `verdict-unverified-not-counted`; P1, P2, P4, P5 verified. |

The first failing check in the requested sequence is self-assessment K07. The expected 48 lesson files are present in its observed count, but the SCORECARD row still states 46 (K10); the run also found four other mismatches above. The observed outcomes do not match the expected six exit-0 gates: self-assessment and registry coverage also exit 1, in addition to the expected pause-gate exit 1.

## Retained evidence

- `quality-77-check-self-assessment.jsonl`
- `quality-77-check-registry-coverage.jsonl`
- `quality-77-check-knowledge-header.jsonl`
- `quality-77-check-recheck-commands.jsonl`
- `quality-77-check-adjacency-anchors.jsonl`
- `quality-77-report-red-causes.jsonl`
- `quality-77-check-pause-gate.jsonl`

Receipt footers record each runner exit and `timed_out: false`; each header binds both `revision` and `tool_revision` to the requested commit. No production files were changed and no tools were installed.

## Risks / blockers

The self-assessment and registry failures need integrator review before claiming the requested gate set passed. This seat is limited to receipt execution and its report; no production corrections were made. The red-causes runner's zero exit must not be interpreted as its embedded checker passing (`checker_exit: 2`, `checker_status: CANNOT_EVALUATE`).