# ExecGateBaselines — round 36

## Baseline and method

Baseline revision: `6d76fb20f6ecbc940e5c8fff36c74060c885e161` (the lane checkout was at this revision). Ran all seven requested gates via `python3 tools/run-receipt.py --revision 6d76fb20f6ecbc940e5c8fff36c74060c885e161 --out <receipt> -- <tool> --revision {rev}`. The driver substituted the full revision and ran each tracked gate from a private sandbox clone at that revision. Each JSONL receipt contains the revision/tool revision, tool SHA-256, gate output, and `receipt_end.exit_code`.

## Gate results

| Gate | Exit | First failing check | Evidence / result | Tool SHA-256 |
|---|---:|---|---|---|
| `check-self-assessment.py` | 1 | `K10` | 27 checked, 1 mismatch: scorecard says 46 `corpus/lessons/` files; 47 observed. | `1e1ab6113d665684e15d147c0f3dae519cf2d313877e1603b841ad4db85d4257` |
| `check-registry-coverage.py` | 0 | — | PASS; 52 registered of 52 rows/tools, 0 findings. | `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812` |
| `check-knowledge-header.py` | 0 | — | PASS; all 55 notes clean and complete; 0 findings. | `592b6c2e765e2a0aec94cc745271878ef748ef3a2e2303ec722828d7cc13f919` |
| `check-recheck-commands.py` | 0 | — | PASS; 55 files, 39 clean, 16 resolved, 81 invocations, `flagged_count: 0`; forbidden list includes `pacman`. | `1c6f349d4c298a3867c7163c7c3fb32f1c768adb0df7110fc7b216a4656b8cd1` |
| `check-adjacency-anchors.py` | 0 | — | PASS; 0 findings; all 114 inbound records classified and 10/10 outbound live objects match. | `a4f500ef680d92132400b1b75f8c2d26db4a9398deed62bcfa8037ec7bbce2e2` |
| `report-red-causes.py` | 0 | — | 268 findings attributed (267 with recorded operations, 1 seat-level); `unattributed: []`. Its retained `checker_status: CANNOT_EVALUATE` is the source checker status, not this gate's exit. | `e84c8af6251277fc1fcb908e9457d7913f42fb2001774b95aab43f3b74a61bc7` |
| `check-pause-gate.py` | 1 | `GATE-PREMISE` (`P3:verdict-unverified-not-counted`) | P3 remains unverified; P1, P2, P4 and P5 are verified. | `eb83986442b37a35e8a584bbd9a225cb51ed2e8d6073974580b87f69f1265128` |

Overall: 5 exit 0, 2 exit 1. “First failing check” is `—` for the five gates that exited 0. The pause-gate P3 is the same inherited red documented at round 35's base and repaired tip (`corpus/lessons/round-35-verifier-spotcheck.md:34`; `corpus/lessons/round-35.md:66`).

## Round-35 repaired-tip shape comparison

- **Registry kinds — holds.** The operative round-35 table includes both `probe` and `gate` rows (`SKILL.md:2945-2970`); registry coverage passes 52/52 with no findings. Examples: `update-recheck | probe` and `recheck-commands | gate`.
- **Note rechecks without pacman invocations — holds under the gate's bounded check.** The recheck receipt has `flagged_count: 0`, and `pacman` is explicitly in the forbidden list. The gate reports 81 invocations across its checked scope; this is not a claim of exhaustive shell analysis.
- **IN-109 — machine record re-pinned; human-readable summary remains stale.** At this revision `corpus/knowledge/adjacency-anchors-r19.json:2453-2470` records `found_line: 2346`, and `tools/tsukuroi-census.sh:2346-2347` contains the D14/D15 quote and its expected result. The JSON-backed adjacency gate passes. However, the Markdown summary still says `found_line 2277` at `corpus/knowledge/adjacency-anchors-r19.md:204,231`; current tool line 2277 is the timer-drift case, not the D14/D15 quote (`tools/tsukuroi-census.sh:2276-2279`). The checker validates the machine record and only checks that the inbound ID appears in knowledge text (`tools/check-adjacency-anchors.py:759-761`); it does not compare the Markdown row's `found_line` to JSON. Thus the repaired machine anchor holds, but the note is not fully internally consistent.

Round 35 recorded the four outcome-commit reds and their repairs, including the 2277→2346 IN-109 shift, then reported all gates except the inherited pause gate green at repaired tip (`corpus/lessons/round-35.md:58-66`). At `6d76fb2`, the registry, recheck and adjacency gates still pass, but the complete gate shape does **not** fully hold: self-assessment is red on K10 (46 stated vs 47 observed), in addition to inherited pause-gate P3. No cause for the K10 count mismatch is inferred here.

## Files and limits

Receipts: `check-self-assessment.jsonl`, `check-registry-coverage.jsonl`, `check-knowledge-header.jsonl`, `check-recheck-commands.jsonl`, `check-adjacency-anchors.jsonl`, `report-red-causes.jsonl`, `check-pause-gate.jsonl`. This report is the only other file created. No production files were changed; no tools were installed. No build, lint, formatter, or unrelated test was run.