# C1 candidate selftest coverage — round 20 attempt 1

## Scope and evidence

Axis: **C1 adjacency**, specifically the declared `ownership_corrections` 0→1 contract. No other claim is assessed. The candidate is `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py`, as bound by `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:2-7`. Below, `tools/check-adjacency-anchors.py:LINE` always means that exact candidate file.

The fixed positive contract is `ownership_corrections=1; exit=0`; the missing and altered IDs are preregistered at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:5-11,32-35`. I compared the candidate declarations with the production-lane checker at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-anchors.py:38-45,753-776,898-920`: the latter lacks the ownership constants/helper and the seven ownership helper cases. This is a working-file source comparison, not a Git-authenticated baseline diff.

No candidate, selftest, measurement script, or command was run. LSP status/references/definition/diagnostics were unavailable within this seat's permitted read/grep/glob/report-write interface; no LSP result is claimed. Caller and branch observations are literal source analysis, not semantic-server proof.

## Findings, by severity

### Medium — most consequential uncovered branch: positive CLI evaluation and emitted metric

The declared positive helper case checks `_ownership_correction` directly, not the public evaluator or emitted JSON (`tools/check-adjacency-anchors.py:1092-1111`). The only explicit ownership-mode CLI case supplies the generic OUT-001 fixture and expects `FAIL` with `OWNERSHIP-CORRECTION-INVALID` (`:873-894,990-993`); it cannot reach a successful OUT-009 correction because the helper requires one OUT-009 record first (`:140-147`). Moreover, the CLI assertion helper checks only the returned code and finding IDs, never `payload["counts"]` (`:928-944`).

The actual claim depends on the public path copying the helper result into `counts["ownership_corrections"]` (`:761-766`), then emitting that count (`:769-776,838-840`). **[INFERENCE] A mutation changing only `:764` from assigning `correction_count` to assigning `0` would escape all declared selftest assertions while breaking the preregistered positive metric.** The helper-positive test would still check its local count of one; the CLI-negative test would still check only its unchanged failure ID. No mutation was applied or executed.

This is the most consequential coverage gap because it leaves the exact claimed 0→1 observable unasserted through the canonical `main → evaluate → emit` path. Closing it requires a positive ownership-mode assertion on emitted `counts.ownership_corrections == 1` as well as exit/status/findings, with a corresponding default-mode count assertion. This finding does **not** establish that the current assignment at `:764` is wrong.

### Low — negative case names overstate distinct rejection-branch coverage

* `ownership-correction-unpinned-snapshot` changes the registry's digest string to 64 zeroes (`:1126-1128`). It therefore rejects at the **metadata identity** check (`:146-147`), before reading the baseline or snapshot. It does not exercise the snapshot read/digest rejection at `:178-181`. The generic `tampered-snapshot` control mutates OUT-001 and expects `ANCHOR-SNAPSHOT-TAMPERED` (`:995-997`); `revision_case` does not enable ownership mode (`:975-985`), so it is not a replacement for a C1 snapshot-byte negative.
* `ownership-correction-missing-arbitration` deletes arbitration text from the immutable baseline prefix (`:1122-1125`). It rejects at the prefix check (`:171-172`), as does the Kaidoku→Mado prefix mutation (`:1112-1116`). Neither independently exercises the final ADJ-06/arbitration-context rejection at `:192-195`. Because that context is present in the fixed baseline fixture (`:66-75`), deleting it from the candidate is already caught earlier. This is coverage overlap, not evidence that the present rejection fails.

A distinct snapshot negative would retain both metadata pins and the exact province prefix/suffix, but return altered snapshot bytes. Its source-derived helper expectation is count **0**, one `OWNERSHIP-CORRECTION-INVALID`, and synthesized `FAIL`/**1**, specifically through `:178-181`. No such fixture was created or run.

## Exact declared outcome map

The seven cases below call the helper through `ownership_case`. That wrapper synthesizes `got_code = FAIL if found else PASS` and asserts the exact ID list and count (`tools/check-adjacency-anchors.py:1092-1106`). Thus **these numeric outcomes are declared helper-harness expectations, not observed CLI exits**. `PASS=0`, `FAIL=1`, `CANNOT=2` are defined at `:20`.

| Case and declaration | Fixture difference | Exact declared expectation | First relevant gate / actual coverage |
|---|---|---|---|
| Missing — `:1108-1109` | Baseline province only; pinned registry/census retained. | `FAIL (1)`; IDs `[OWNERSHIP-CORRECTION-MISSING]`; count `0`. | No correction heading and bytes equal baseline, `:163-167`. |
| Valid — `:1110-1111` | Baseline plus exactly `"\n" + "\n".join(OWNERSHIP_SECTION_LINES) + "\n"`, constructed at `:1087-1090`. | `PASS (0)`; IDs `[]`; count `1`. | Requires all helper guards and reaches `return 1, []` at `:196`; does not exercise evaluator count propagation or JSON emission. |
| Altered — `:1118-1121` | Replaces `It is not a tsukuroi grant of ownership.` with `It grants tsukuroi ownership.` | `FAIL (1)`; IDs `[OWNERSHIP-CORRECTION-INVALID]`; count `0`. | Exact appended-suffix mismatch, `:173-175`; not a semantic phrase classifier. |
| Missing arbitration — `:1122-1125` | Deletes the two original arbitration lines and trailing newline. | `FAIL (1)`; IDs `[OWNERSHIP-CORRECTION-INVALID]`; count `0`. | Baseline-prefix mismatch, `:171-172`, before final arbitration-context validation. |
| Unpinned — `:1126-1128` | Changes only registry `sibling_blob_sha256` to `"0" * 64`. | `FAIL (1)`; IDs `[OWNERSHIP-CORRECTION-INVALID]`; count `0`. | Original registry pin mismatch, `:146-147`; no snapshot-byte read on this path. |
| Duplicate — `:1129-1131` | Appends a second complete identical correction section. | `FAIL (1)`; IDs `[OWNERSHIP-CORRECTION-INVALID]`; count `0`. | Two exact correction headings, `:163,169-170`, before suffix validation. |
| Prefix mutation — `:1112-1116` | Changes first arbitration line's `Kaidoku` to `Mado`, leaving correction intact. | `FAIL (1)`; IDs `[OWNERSHIP-CORRECTION-INVALID]`; count `0`. | Baseline-prefix mismatch, `:171-172`. |

Each helper-generated missing/invalid finding has site `OUT-009` (`:138-139,166-167`), but the wrapper asserts only IDs, code and count, not site or diagnostic detail (`:1097-1100`). Consequently identical INVALID IDs do not distinguish which negative guard was reached.

## Residual risk and verification gaps

* All seven helper cases share one fixed census and one `FixtureReader`. That reader ignores the requested revision and always supplies the same valid baseline/snapshot by path (`tools/check-adjacency-anchors.py:1079-1096`). These declarations do not establish revision-sensitive reads or fail-closed handling of missing/unsafe baseline/snapshot objects.
* In particular, the baseline-read failure branch at `:156-159` raises `E-OWNERSHIP-BASELINE`, rather than returning a helper finding/count. The public exception path converts it to `CANNOT_EVALUATE`/exit **2** (`:800-801,841-844,769-776`); no ownership declaration asserts that outcome. An exception in the present helper harness instead becomes a general `selftest setup` failure (`:1133-1141`).
* Registry/census identity and uniqueness checks exist (`:140-154`), but the seven declarations vary only one registry digest, not census identity or duplicate OUT-009 records. The duplicate case covers a province heading, not duplicate registry/census identity.
* The production checker's corresponding assertion helper also checks only codes/IDs (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-anchors.py:760-776`), so the missing aggregate metric assertion is not supplied by an inherited assertion convention.
* No selftest pass/fail, emitted count, authenticated commit diff, digest recomputation, runtime saturation, or host/boot safety result is claimed. These finite declarations are not evidence of exhaustive branch coverage. Boot images remain **UNKNOWN**; no clearance. No tools were installed or updated; only this report was written.

Scope: executed=none.
