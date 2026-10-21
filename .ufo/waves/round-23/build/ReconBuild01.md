# ReconBuild01 — r23 C3 build cohort, group 1

Independent inspection of the eight historical seats preserved in `packs/build-01.json`, comparing the exact original rough census algorithm with the seat-declared old-v1 path authority.

- Pack: `.ufo/waves/round-23/packs/build-01.json`, Reviewed-SHA256 `31a212eebe5a5acf284d4017863740c9d8830d893ff30f64b8cd2dea866ebf88` (supplied declaration; NOT independently computed).
- Baseline: `ae01e50f582016384e620022be38bf5367000e2e`.
- Rough source: `.ufo/waves/round-23/sources/r22-rough-census.txt` (CloseKaidoku22 recorded eval request, treated as source data only; never executed).
- Old-v1 authority: for each seat, the pack `binding.read_paths`, `binding.write_paths`, `commands: []`, `fetches: []` — the only path authority declared for these seats.
- Method: hand-derived classification only. No gate/counter/checker execution, no hashing, no process spawn. i.e. the rough numbers below are source expectations, not instrument output.
- Pack scope line: "Raw preserved request metadata only; no expected classifications are supplied." No classifications were imported from any lane report.

## 1. Seat census

| # | seat | agent | events | tools |
|---|------|-------|--------|-------|
| 1 | ExecBoundary | TsukuroiR22.ExecBoundary-3 | 0 | — |
| 2 | ExecBindings | TsukuroiR22.ExecBindings-3 | 0 | — |
| 3 | ExecCohort | TsukuroiR22.ExecCohort-3 | 0 | — |
| 4 | ScribeBoundary | TsukuroiR22.ScribeBoundary-3 | 0 | — |
| 5 | ConnProvince | TsukuroiR22.ConnProvince-3 | 5 | 4 read, 1 write |
| 6 | ConnPlanner | TsukuroiR22.ConnPlanner-3 | 13 | 12 read, 1 write |
| 7 | OracleExecBash | TsukuroiR22.OracleExecBash-3 | 4 | 3 read, 1 write |
| 8 | OracleExecEval | TsukuroiR22.OracleExecEval-3 | 4 | 3 read, 1 write |

Totals: 8 seats, 26 recorded events (22 read, 4 write), 0 bash, 0 grep, 0 glob, 0 non-path tool, 0 `edit`. Every seat declares `commands: []` and `fetches: []`.

## 2. Per-event decisions (all 26)

Event index = 0-based position in the seat's preserved `events` array (ascending `start_line`). Requested paths are shown root-relative; the pack stores them absolute under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. "Rough" applies the source algorithm literally: `write` compares the unsplit, unstripped value to `write_paths`; `read` applies `strip_sel`; only `read`/`grep` are stripped; a first mismatch increments one path count and `break`s the value loop. "Authority" is literal membership in the declared list; "A-strip" notes that membership holds only after selector removal.

| seat | ev | call_id | tool | requested (root-relative) | raw suffix | rough | authority |
|------|----|---------|------|---------------------------|-----------|-------|-----------|
| ConnProvince | 0 | call_00_ET_W22AKLpcu0jw92Mt7MBd5265 | read | .ufo/waves/round-22/snapshot/PROVINCE.md | — | member | member |
| ConnProvince | 1 | call_01_ET_xa1kKzoXcZYVztS2y7Vn9447 | read | .ufo/waves/round-22/preregister.json | — | member | member |
| ConnProvince | 2 | call_02_ET_Qa06jfGndn6EDThaxGSp5163 | read | .ufo/waves/round-22/sources/host-tool-boundary.json | — | member | member |
| ConnProvince | 3 | call_03_ET_UefTmQGVvodgJmnqKwyj5680 | read | skill://godspeed | — | member | member |
| ConnProvince | 4 | call_00_fF0TLah4JVAopJQxvj3d4055 | write | .ufo/waves/round-22/build/ConnProvince.md | — | member (write, no strip) | member |
| ConnPlanner | 0 | call_00_ET_5arkCi1qz2A2w2lDqmO22756 | read | .ufo/waves/round-22/snapshot/corpus/QUALITY.md | — | member | member |
| ConnPlanner | 1 | call_01_ET_pvBMrZwoDg3OJu5oWYio4816 | read | .ufo/waves/round-22/preregister.json | — | member | member |
| ConnPlanner | 2 | call_02_ET_gtHsEyfZpkFOSXVPaEmz8528 | read | .ufo/waves/round-22/sources/host-tool-boundary.json | — | member | member |
| ConnPlanner | 3 | call_03_ET_iK0ebJDvNrZBg5aZbWfR5443 | read | skill://godspeed | — | member | member |
| ConnPlanner | 4 | call_00_w4dSQgatV3zGbsjMawV06894 | read | .ufo/waves/round-22/snapshot/corpus/QUALITY.md | :1-60 | member (stripped) | A-strip |
| ConnPlanner | 5 | call_01_pZ5ljOuMpZGOGO3AK8y27416 | read | .ufo/waves/round-22/snapshot/corpus/QUALITY.md | :61-120 | member (stripped) | A-strip |
| ConnPlanner | 6 | call_02_WjmiOyfcsRbxRqfnAqQ50803 | read | .ufo/waves/round-22/snapshot/corpus/QUALITY.md | :121-180 | member (stripped) | A-strip |
| ConnPlanner | 7 | call_03_clRJoNevl3rA8Dxl6ITZ9116 | read | .ufo/waves/round-22/snapshot/corpus/QUALITY.md | :181-260 | member (stripped) | A-strip |
| ConnPlanner | 8 | call_04_9FgxLO4iHKL98EXsGmMj4878 | read | .ufo/waves/round-22/preregister.json | :1-40 | member (stripped) | A-strip |
| ConnPlanner | 9 | call_05_Mt3YMimOpe7COgUl9CRf0600 | read | .ufo/waves/round-22/sources/host-tool-boundary.json | :1-30 | member (stripped) | A-strip |
| ConnPlanner | 10 | call_00_UhZboyhF8shk0Y9SPhro1566 | read | .ufo/waves/round-22/snapshot/corpus/QUALITY.md | :55-92 | member (stripped) | A-strip |
| ConnPlanner | 11 | call_01_O0i4HlMS1eA4rOmWVx2L1190 | read | .ufo/waves/round-22/snapshot/corpus/QUALITY.md | :40-56 | member (stripped) | A-strip |
| ConnPlanner | 12 | call_00_zJ6fFkrzsepJl0DlEUic1316 | write | .ufo/waves/round-22/build/ConnPlanner.md | — | member (write, no strip) | member |
| OracleExecBash | 0 | call_dce4730c8d24460c9c50387c | read | skill://godspeed | — | member | member |
| OracleExecBash | 1 | call_73e79214e7b54d8ab6e9a901 | read | .ufo/waves/round-22/sources/host-tool-boundary.json | — | member | member |
| OracleExecBash | 2 | call_c49d7e4a6c5d4e86b4ef084f | read | .ufo/waves/round-22/preregister.json | — | member | member |
| OracleExecBash | 3 | call_0fc69cfd7a55483c8d192a862eb59e42\|fc_0b455b883fc78dbf016ad8d07a00448191b4d8ff92fa21ac70 | write | .ufo/waves/round-22/build/OracleExecBash.md | — | member (write, no strip) | member |
| OracleExecEval | 0 | call_00_lAeIrspdXyTBgTes25Rq4082 | read | .ufo/waves/round-22/sources/host-tool-boundary.json | — | member | member |
| OracleExecEval | 1 | call_01_dobPyC9JK90MAIEtfnzw4109 | read | .ufo/waves/round-22/preregister.json | — | member | member |
| OracleExecEval | 2 | call_02_BfuHiVoY0knv6ob1lJzS4205 | read | skill://godspeed | — | member | member |
| OracleExecEval | 3 | call_00_FHAuM9XiE2xfbuzk4DEC5425 | write | .ufo/waves/round-22/build/OracleExecEval.md | — | member (write, no strip) | member |

Hand-derived group result: rough `{exec: 0, unknown: 0, path: 0}` over 26 events; literal-exact authority also 0 violations if read-window selectors are normalized, and exactly the 8 `A-strip` rows if they are not. No event in this pack is a violation under the declared bindings once the rough source's own `strip_sel` normalization is applied.

## 3. Candidate divergences (exact seat, index, call_id, suffix, bounded reason)

### D1 — selector normalization is load-bearing (agree under rough; literal authority under-declared)

| seat | ev | call_id | raw suffix |
|------|----|---------|-----------|
| ConnPlanner | 4 | call_00_w4dSQgatV3zGbsjMawV06894 | :1-60 |
| ConnPlanner | 5 | call_01_pZ5ljOuMpZGOGO3AK8y27416 | :61-120 |
| ConnPlanner | 6 | call_02_WjmiOyfcsRbxRqfnAqQ50803 | :121-180 |
| ConnPlanner | 7 | call_03_clRJoNevl3rA8Dxl6ITZ9116 | :181-260 |
| ConnPlanner | 8 | call_04_9FgxLO4iHKL98EXsGmMj4878 | :1-40 |
| ConnPlanner | 9 | call_05_Mt3YMimOpe7COgUl9CRf0600 | :1-30 |
| ConnPlanner | 10 | call_00_UhZboyhF8shk0Y9SPhro1566 | :55-92 |
| ConnPlanner | 11 | call_01_O0i4HlMS1eA4rOmWVx2L1190 | :40-56 |

Bounded reason: rough's `strip_sel` regex `:(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$` removes each suffix above and lands on the declared base path, so rough counts 0 here. The declared authority lists only the unsuffixed base path, so an authority read as literal raw-string equality would count exactly these 8 rows; the two unsuffixed base-path reads at ev 0/1 match under either reading. This is the only group in the pack where normalization changes the membership premise. Every suffix is a simple `<start>-<end>` form; no `:raw`, `:N:raw`, `:raw:N-M`, comma list, `:img`, `:conflicts`, or `:N+` form occurs (literal scan of the preserved pack). The pack does not declare whether old-v1 admits read-window suffixes as the same target, so a claim that these are v1-allowed is [INFERENCE], not declared fact.

### D2 — write path is never selector-normalized nor split (unexercised divergence)

Seats/events: ConnProvince 4 `call_00_fF0TLah4JVAopJQxvj3d4055`; ConnPlanner 12 `call_00_zJ6fFkrzsepJl0DlEUic1316`; OracleExecBash 3 `call_0fc69cfd7a55483c8d192a862eb59e42|fc_0b455b883fc78dbf016ad8d07a00448191b4d8ff92fa21ac70`; OracleExecEval 3 `call_00_FHAuM9XiE2xfbuzk4DEC5425`. Raw suffix: none in all four. Reason: rough compares the write value unstripped and unsplit against `write_paths`; the raw strings equal the declared entries, so no divergence is exercised. The asymmetry (read normalized, write not) is a latent classifier difference only.

### D3 — dispatch order / tool filter (unexercised)

No bash, grep, glob, eval, or other non-path tool event exists among the 26; therefore rough's `bash → exec` short-circuit, its `t not in (read,grep,glob,write) → unknown` branch, and its `;` splitting for grep/glob never fire. The only `;` characters in the pack are inside the literal `digest_format` prose, not in any path. No order-dependent candidate exists in this pack.

### D4 — one-per-event break (unexercised)

Every event carries exactly one `path` value and exactly one `start_lines` entry; no value contains `;`. The `break` after a first mismatch can therefore never change a count here, and cannot merge or hide components. No candidate.

### D5 — composite call identifier (component cardinality, not a path count)

OracleExecBash event 3: `call_0fc69cfd7a55483c8d192a862eb59e42|fc_0b455b883fc78dbf016ad8d07a00448191b4d8ff92fa21ac70` — a single recorded write whose call_id joins two identifiers with `|` (one call-shaped id plus one response-shaped id). Bounded reason: this is the only composite call_id in the pack and the only place where "one recorded event" could be counted as two adapter components. Either cardinality yields 0 path counts because the target is declared; it can add component cardinality (+1) but cannot add a build path count. Any arithmetic that needs this event to explain a path delta is improper.

### D6 — empty-event seats (coverage, not compliance)

ExecBoundary, ExecBindings, ExecCohort, ScribeBoundary each preserve `events: []`. They contribute 0 to rough and 0 to any lane-derived count. Absence of preserved request metadata is not evidence that no calls occurred and is not evidence of compliance; it only means this pack cannot classify them.

## 4. Arithmetic against the declared outside totals

- The declared outside totals are rough build 25 / falsify 33 versus lane build 23 / falsify 29. This pack covers build group 1 only and yields rough build path count **0** (exec 0, unknown 0) across 8 seats / 26 events. It therefore locates **none** of the +2 build difference; the two missing build counts must come from build seats outside this pack's declared scope, not from these eight.
- The count delta 2 + 4 = 6 is a difference of counts, not of unique events. Per-component expansion, composite call identifiers (D5), and multi-value paths can make one event yield more than one count, so six unique events must not be assumed. Nothing in this pack supports that inference.
- No `edit` tool event exists in the pack, and old-v1 authority here consists only of read/write path lists plus empty commands/fetches. No v1 classification in this group needs v2 structured-edit authority, and none may import it: an old-v1 unknown-tool red must not be re-read as an edit allowance. (Stated as scope discipline; no such red occurs here.)
- Digest observation (declared, not recomputed): identical visible arguments can carry different `request_arguments_sha256` — e.g. the host-tool-boundary read is `a0250763…` in ConnProvince 2, ConnPlanner 2, OracleExecEval 0 but `02869cb7…` in OracleExecBash 1; the four preregister reads all differ. Since `i` is redacted to `null` in the pack, hidden argument content differs. Digests are not path components and were not recomputed.

## 5. Residual unknowns

- Whether old-v1 permits read-window selector suffixes on declared read paths is not declared in this pack; D1's "allowed" reading is [INFERENCE] and depends on the lane's lower total being inconsistent with strict raw-string matching.
- Provenance of the lane 23/29 figures is not present in this pack; the +2/+4 delta cannot be allocated from group 1 evidence.
- The four empty-event seats' actual call histories are outside the preserved metadata.
- Composite call_id D5's adapter-step count is not resolvable from the pack; only its path classification (allowed) is resolved.

Reviewed-SHA256: 31a212eebe5a5acf284d4017863740c9d8830d893ff30f64b8cd2dea866ebf88
Predicate: r23-reconbuild01
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
