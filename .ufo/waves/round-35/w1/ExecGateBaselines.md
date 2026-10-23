# ExecGateBaselines — gate receipts at the round-35 tip, and the round-34 routed defect 4 (round 35, wave w1)

**Verdict: at the pre-freeze candidate `6b4561e43e15c1cce038e390ad7d4691b0af4cc8` four of the seven gates are green and three are red — `check-self-assessment` exit 1 (finding `K10`), `check-registry-coverage` exit 1 (finding `REGISTRY-ROW-MISSING` at `tools/score-pacnew-arm-r35.py`) and `check-pause-gate` exit 1 (finding `GATE-PREMISE` at `P3:verdict-unverified-not-counted`); `check-recheck-commands`, `check-knowledge-header`, `check-adjacency-anchors` and `report-red-causes` are exit 0.** The `check-registry-coverage` red is **new at the tip** (exit 0 at the claim base `b40c01d` and exit 0 in the round-34 w2 receipts at `879daa95`) and is caused by the round-35 declaration commit itself; the other two reds are inherited unchanged from the base. Routed defect 4 (unreceipted gate line) is discharged: receipts naming a committed revision now exist for all four gates the round-34 spot-check named, and the round-34 report's line-50 gate claim is independently reproduced.

Seat directory for every receipt and run log: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ExecGateBaselines/`. Receipts are in the committed-receipt form (`tools/run-receipt.py`: header line, tool stdout lines, footer line with `exit_code`, `timed_out`, `stderr_tail`).

---

## 1. The seven tip receipts (routed defect 4)

Each receipt was produced by one invocation of the form (quoted from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ExecGateBaselines/tip-check-self-assessment.runlog` and its siblings):

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  python3 tools/run-receipt.py \
    --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
    --revision 6b4561e43e15c1cce038e390ad7d4691b0af4cc8 \
    --tool-revision 6b4561e43e15c1cce038e390ad7d4691b0af4cc8 \
    --out .../ExecGateBaselines/tip-<tool>.jsonl --timeout 800 \
    -- tools/<tool>.py --revision '{rev}'
```

`{rev}` is substituted by `run-receipt.py` with the resolved full hash, so every receipt's `argv` names the full 40-hex tip hash. Each tool was read from the same revision as it was run at (the tool revision equals the measured revision), and the run happened in `run-receipt.py`'s private `--no-local` clone under `/fast/scratch/hyaku/run-receipt-*`, never in the lane working tree.

| # | Gate | Tool sha256 (tip blob) | Exit | Finding ids | Receipt (sha256 of the receipt file) |
|---|---|---|---|---|---|
| 1 | `check-self-assessment` | `1e1ab6113d665684e15d147c0f3dae519cf2d313877e1603b841ad4db85d4257` | **1** | `K10` (1 mismatch of 27 checks) | `tip-check-self-assessment.jsonl` (`70c8020b425299557fea9f99850a8e86b0023023665c889c115cbfbad14569ee`) |
| 2 | `check-registry-coverage` | `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812` | **1** | `REGISTRY-ROW-MISSING` ×1 | `tip-check-registry-coverage.jsonl` (`7111ece478199411dfa3695b536a1780b51f211d3e1fbdf3abe29f969fc11371`) |
| 3 | `check-recheck-commands` | `1c6f349d4c298a3867c7163c7c3fb32f1c768adb0df7110fc7b216a4656b8cd1` | **0** | none (`findings: []`, `flagged_count: 0`) | `tip-check-recheck-commands.jsonl` (`0d49ab1bcb856601899ddc7b26010f8b8f95dc72a0c1477211ee1d524f080dfb`) |
| 4 | `check-knowledge-header` | `592b6c2e765e2a0aec94cc745271878ef748ef3a2e2303ec722828d7cc13f919` | **0** | none (`finding_count: 0`, 54/54 notes complete) | `tip-check-knowledge-header.jsonl` (`11855a9d9492f5131dd1bc7f3c789bb4c89201ae680de020a3f374df4457d7a2`) |
| 5 | `check-adjacency-anchors` | `a4f500ef680d92132400b1b75f8c2d26db4a9398deed62bcfa8037ec7bbce2e2` | **0** | none (`findings: []`) | `tip-check-adjacency-anchors.jsonl` (`e591db112b5f70d18529659f92625d2155cc9d7257fdd73b81d29635cf8d41f9`) |
| 6 | `check-pause-gate` | `eb83986442b37a35e8a584bbd9a225cb51ed2e8d6073974580b87f69f1265128` | **1** | `GATE-PREMISE` ×1 (`P3:verdict-unverified-not-counted`) | `tip-check-pause-gate.jsonl` (`9aa9b923eb42a3a0b64c7450335383806d9e4bc3bb3a1e3f20bd22626e2fa9c9`) |
| 7 | `report-red-causes` | `e84c8af6251277fc1fcb908e9457d7913f42fb2001774b95aab43f3b74a61bc7` | **0** | none (attribution report; `checker_exit: 2`, `checker_status: CANNOT_EVALUATE` preserved) | `tip-report-red-causes.jsonl` (`57c618379ea0331e05b1be5f9c8a430301068c69b475da360d652a6e4f036525`) |

No receipt timed out (`timed_out: false` in every footer) and every `stderr_tail` is empty. Total evidence under the seat directory: 27 receipt files plus 27 run logs, 307 480 bytes of receipts.

[obs] The seven tool blobs are byte-identical at `879daa95`, at the claim base `b40c01d` and at the tip `6b4561e4` (`git show <rev>:tools/<tool>.py | sha256sum` for each of the three revisions gives the same digest as the receipt's `tool_sha256` header). Every gate verdict in this report is therefore a property of the measured repository bytes, not of a changed gate.

## 2. The round-34 w2 comparison (`879daa95`)

The round-34 w2 receipts under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/GatesAfterNoHarm/` were re-run at the same revision with this wave's tool bytes (`r34w2-*.jsonl`, tool revision `6b4561e4`) so that the two sets are comparable.

| Gate | round-34 w2 receipt at `879daa95` (committed) | my re-run at `879daa95` | tip at `6b4561e4` | Verdict |
|---|---|---|---|---|
| `check-self-assessment` | exit 1, 4 mismatches `K07`–`K10` | exit 1, same 4 mismatches — **body byte-identical** to the committed receipt | exit 1, **1 mismatch (`K10`)** | improved; still red |
| `check-registry-coverage` | exit 0 `PASS`, `tools_total 50`, `registered 50` | exit 0 `PASS`, identical counts (only `branch_tip` differs) | exit 1 `FAIL`, `tools_total 51`, `registered 50`, 1 finding | **regressed at the tip** |
| `check-recheck-commands` | exit 0 `PASS` | exit 0 `PASS`, identical body apart from `branch_tip` | exit 0 `PASS` | unchanged |
| `check-knowledge-header` | exit 0 `PASS`, 54/54 | exit 0 `PASS`, identical body apart from `branch_tip` | exit 0 `PASS` | unchanged |
| `check-adjacency-anchors` | exit 0 `PASS` | (identical tool bytes; tip body differs only in revision fields) | exit 0 `PASS` | unchanged |
| `check-pause-gate` | exit 1, `GATE-PREMISE` `P3` | exit 1, same finding | exit 1, same finding | unchanged |
| `report-red-causes` | exit 0 | (same tool bytes) | exit 0 | unchanged |

[obs] The `check-self-assessment` receipt body I produced at `879daa95` is byte-identical to the committed round-34 w2 receipt body after normalising only the private run-receipt directory name (`/fast/scratch/hyaku/run-receipt-<random>`). That is the strongest form of the reproducibility claim available here: same exit code, same findings, same bytes.

[obs] The improvement of `check-self-assessment` from 4 mismatches to 1 is caused by the round-34 measured-outcome commit `a8b46ac8` restating the depth row (54 notes, 2942 `SKILL.md` lines, 730 table lines) — `git show 6b4561e4:SCORECARD.md:1492` reads `| depth | 8 | 54 notes … 2942 … 730 … (44 files) |`, and `SCORECARD.md:1390` at `a8b46ac8` still reads the stale `53 notes … 2870 … 678 … (42 files)`.

## 3. The claim-base baseline (`b40c01d`)

The same seven gates at the round-35 claim base `b40c01df38eb26f74c095c471efc6d1649b00fd4`, tool revision `6b4561e4` (`base-*.jsonl`):

| Gate | exit at base | exit at tip | difference |
|---|---|---|---|
| `check-self-assessment` | 1 (`K10`: stated 44 lesson files, observed 45) | 1 (`K10`, same) | none — inherited |
| `check-registry-coverage` | **0 `PASS`** (`tools_total 50`, `registered 50`) | **1 `FAIL`** (`tools_total 51`, 1 finding) | **new red at the tip** |
| `check-recheck-commands` | 0 | 0 | none |
| `check-knowledge-header` | 0 | 0 | none |
| `check-adjacency-anchors` | 0 | 0 | none |
| `check-pause-gate` | 1 (`GATE-PREMISE` `P3`) | 1 (same) | none — inherited |
| `report-red-causes` | 0 | 0 | none (bodies byte-identical after revision normalisation) |

[obs] `check-pause-gate` bodies at base and tip are byte-identical after normalisation (`premises_total 5`, `premises_verified 4`; P1 `changed`, P2 `cleared`, P3 `unverified` + `verdict-unverified-not-counted`, P4 `changed`, P5 `changed`; `checkupdates_attachment_pinned: true`).

[obs] `report-red-causes` bodies at base and tip are byte-identical after normalisation: `total_findings 268`, `findings_by_id {SCOPE-PATH-DENIED: 266, SCOPE-SCHEMA: 1, SCOPE-TRACE-INCOMPLETE: 1}`, `expected_split` equal to `findings_by_id`, `split_matches` true, `checker_exit 2`, `checker_status CANNOT_EVALUATE`, `incomplete_seat_is_frozen: true`, `attributed_findings 268`, `attributed_with_recorded_operation 267`.

## 4. Findings

1. **`check-registry-coverage` is red at the tip and the red is caused by the round-35 declaration commit.** Finding id `REGISTRY-ROW-MISSING`, site `tools/score-pacnew-arm-r35.py`, detail `no operative row names this regular tools/ file`; counts `{"findings": 1, "missing": 1, "registered": 50, "rows_total": 50, "tools_total": 51}`; `status: FAIL` [obs, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ExecGateBaselines/tip-check-registry-coverage.jsonl`]. The same gate at the base is exit 0 with `tools_total 50` [obs, `base-check-registry-coverage.jsonl`]. The gate's own logic is that every regular `tools/` file must be named by an operative registry row (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-registry-coverage.py:319-321`), and the operative section is the highest-numbered `## Gate and probe registry — roundN superseding current rows` heading (`tools/check-registry-coverage.py:52-53,194-215`). The tip's highest such heading is still round 34 at `SKILL.md:2884`, and `grep -c 'score-pacnew-arm-r35' SKILL.md` returns **0** at the tip, while `git diff --name-status b40c01d 6b4561e4 -- tools/` shows `tools/score-pacnew-arm-r35.py` added (372 lines) [obs]. **This is a no-harm regression the declaration introduced, and it is fixable by the lane in one place** (a round-35 registry section, or a row naming the counter in the operative table); I did not edit `SKILL.md` because my seat may only write inside its own directory [inf: the fix belongs to the L1's repair list].

2. **`check-self-assessment` at the tip has exactly one mismatch, `K10`, and it is inherited from the base, not introduced this round.** Stated 44 lesson files against 45 observed, `stated_line: 1492` (`SCORECARD.md:1492` reads `` `corpus/lessons/` (44 files) ``), `status: FAIL`, `mismatches: 1`, `checked: 27`, `declaring_round: 34`, `axes_heading: "## Axes — current self-assessment (round 34)"` [obs, `tip-check-self-assessment.jsonl`]. The base receipt is identical in the mismatch (`base-check-self-assessment.jsonl`), while the round-34 w2 receipt at `879daa95` had four (`K07`–`K10`) [obs]. The count moved because the round-34 verifier spot-check commit `b40c01d` added `corpus/lessons/round-34-verifier-spotcheck.md`, taking the directory from 44 files at `6aad5b12` to 45 (`git ls-tree --name-only <rev> corpus/lessons/ | wc -l` gives 43 at `879daa95`, 44 at `6aad5b12`, 45 at `b40c01d` and at the tip), while the depth row was last restated at `a8b46ac8` when the count was 44 [obs]. `K01`–`K09` and `K11`–`K27` all report `status: match` at the tip, including `K13` (census selftest 101/101 cases at the tip) [obs].

3. **`check-pause-gate` is red at the tip with the same single finding it had at the base and at `879daa95` — a pre-existing red, unchanged.** Finding id `GATE-PREMISE`, site `P3:verdict-unverified-not-counted`; `premises_total 5`, `premises_verified 4`, `status: FAIL` [obs, `tip-check-pause-gate.jsonl`; identical in `base-check-pause-gate.jsonl` and in the round-34 w2 receipt]. The gate counts only `cleared`/`still-holds`/`changed` verdicts (`tools/check-pause-gate.py:31`), so P3's `unverified` verdict is not counted. Nothing in the round-35 declaration touches `corpus/knowledge/pause-lift-gate-r24.json` (`git diff --name-status b40c01d 6b4561e4` lists no such path) [obs].

4. **Routed defect 4 is discharged at the tip.** The round-34 spot-check routed: *"Issue receipts for check-self-assessment, check-registry-coverage, check-recheck-commands and check-knowledge-header at the tip, or restate them as measured at `879daa95`"* (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-34-verifier-spotcheck.md` §5 item 4). All four now have committed-receipt-form receipts naming `6b4561e43e15c1cce038e390ad7d4691b0af4cc8` as both the measured revision and the tool revision, and three more gates were added for completeness (§1 table) [obs]. The receipts carry the header fields the defect complained about (absent before): `revision`, `tool_revision`, `tool`, `tool_sha256`, `argv`, `lane_branches`, `started_utc`, and a footer with `exit_code`, `timed_out`, `stderr_tail`, `finished_utc`.

5. **The round-34 report's gate line is true at the revision it names, and its one unverifiable clause is reproduced only in part.** Report line 50 (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/reports/round-34/tsukuroi.md:50`, in the fleet repo, not the lane) reads: *"Gates at `a8b46ac8`, all exit 0: knowledge-header, self-assessment, registry-coverage, recheck-commands. Knowledge-header was exit 1 at `6de666c4`; self-assessment and registry-coverage were exit 1 at base."* I re-ran all four at `a8b46ac8` with the tip's tool bytes (`r34claim-*.jsonl`): **all four are exit 0** (`status PASS` for registry-coverage, recheck-commands and knowledge-header; `status PASS`/0 mismatches for self-assessment) [obs]. I also ran `check-knowledge-header` at `6de666c4` (`r34kb-check-knowledge-header.jsonl`): **exit 1** with `KNOWLEDGE-HEADER-MISSING` ×2 and `KNOWLEDGE-HEADER-VALUE` ×3, the misses on `corpus/knowledge/kill-oom-boundary-r33.md` [obs]. The remaining clause — *"self-assessment and registry-coverage were exit 1 at base"* — reproduces for self-assessment (exit 1 at the round-34 base `2641591e`, `K10`: stated 42, observed 43; `r34base-check-self-assessment.jsonl`) but **not** for registry-coverage, which I measured **exit 0 `PASS`** at `2641591e` with the tip's tool bytes (`r34base-check-registry-coverage.jsonl`) and also **exit 0 `PASS`** with the base's own tool bytes (`r34base-tools-check-registry-coverage.jsonl`, `tools_total 48`, `registered 48`, 0 findings) [obs]. [unk] Which revision the report's word "base" denoted is not recoverable from the receipt-less claim; the two readings available (the round-34 base `2641591e`, or the round-33 tip) are not separated by any committed receipt, so I report the measurement rather than a verdict on the report.

6. **Every other gate is green and byte-stable across the three revisions measured.** `check-recheck-commands`: `PASS`, `file_count 54`, `clean_count 38`, `flagged_count 0`, `invocation_count 81`, `pointer_section_count 42`, `resolved_count 16`, forbidden list `pacman, checkupdates, yay, paru, mkinitcpio, limine-update` [obs, `tip-check-recheck-commands.jsonl`]. `check-knowledge-header`: `PASS`, `note_count 54`, `complete_count 54`, `clean_count 54`, `finding_count 0` [obs]. `check-adjacency-anchors`: `PASS`, `outbound_total 10`, `inbound_total 114`, `inbound_classified 114`, `live_object_checked 10`, `live_object_match 10`, `findings: []` [obs]. `report-red-causes`: exit 0 with the frozen round-23 split preserved and no re-grading [obs].

7. **Every receipt is reproducible from committed bytes only.** All three revisions I measured (`879daa95`, `2641591e`, `b40c01d`, `a8b46ac8`, `6b4561e4`) are ancestors of the tip (`git merge-base --is-ancestor <rev> 6b4561e4` exits 0 for each), the lane working tree carried no tracked modification at the start of this seat (`git status --porcelain` showed only untracked `.ufo/waves/round-35/` paths), and `run-receipt.py` executes each tool in a private clone with every inherited `GIT_*` name dropped and global/system git config off (`tools/run-receipt.py:38-46,71-88`) [obs]. The only writes this seat made are the receipt files and run logs under its own seat directory; no lane file was edited, no git write command was run in the lane, and no host package or service action was taken.

## 5. Files this seat wrote

All under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ExecGateBaselines/` (27 receipts + 27 run logs, 307 480 bytes of receipts) and this report at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ExecGateBaselines.md`. The receipts are untracked in the lane working tree; the L1 owns committing them, and this seat ran no git write command in the lane.

Scope: read=<round-35 tip 6b4561e4, claim base b40c01d, round-34 w2 879daa95, round-34 claim a8b46ac8, round-34 base 2641591e, the seven lane gate tools, run-receipt.py, SKILL.md registry headings, SCORECARD.md axes/depth rows, corpus/lessons file counts, corpus/lessons/round-34-verifier-spotcheck.md §5, the fleet report .ufo/reports/round-34/tsukuroi.md line 50>; wrote=.ufo/waves/round-35/w1/ExecGateBaselines/{tip,base,r34w2,r34claim,r34base,r34base-tools,r34kb}-*.jsonl, .ufo/waves/round-35/w1/ExecGateBaselines/*.runlog, .ufo/waves/round-35/w1/ExecGateBaselines.md; executed=27 run-receipt.py invocations of tools/{check-self-assessment,check-registry-coverage,check-recheck-commands,check-knowledge-header,check-adjacency-anchors,check-pause-gate,report-red-causes}.py across revisions 6b4561e4, b40c01d, 879daa95, a8b46ac8, 2641591e, 6de666c4, plus read-only git plumbing (rev-parse, show, ls-tree, diff, merge-base, for-each-ref, status, log)>
Model: minimax-code/MiniMax-M3.1-Flash
Installs: none
