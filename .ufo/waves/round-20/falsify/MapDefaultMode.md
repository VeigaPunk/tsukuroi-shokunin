# MapDefaultMode — default coverage versus opt-in metric

## Scope and finding

**Design only; no mutation or detector execution.** Axes: backward-compatible generic registry coverage, C3 calibration, and preservation of the opt-in output contract. The assigned registry candidate is `/tmp/tsukuroi-r20-registry-20261021`; the lane records baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472` and this worktree at `.ufo/waves/round-20/worktree-bindings.json:2-7`. The implementation assignment explicitly requires backward-compatible generic coverage (`.ufo/waves/round-20/build/spec.json:15`). C3's registered command includes `--audit-live-map`, with legacy-live-1 rejection and corrected-map acceptance (`.ufo/waves/round-20/preregister.json:21-27,49-53`).

**Static finding:** the candidate currently gates both semantic checking and metric emission correctly. However, its selftest assertions do not protect the absence of `audit_live_map_errors` in default-mode output. A one-guard mutation can leak an unmeasured zero into default output without changing generic coverage results or the explicit-mode results. This is a proposed coverage counterexample, not an observed production defect or a measured surviving mutant.

Paths below beginning with `candidate/` mean `/tmp/tsukuroi-r20-registry-20261021/`. Other relative paths are under the production lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

## Source-level contract

- The inherited lane checker exposes the generic revision/baseline-tools interface, constructs only the five base counts, and optionally adds baseline-tool accounting: `tools/check-registry-coverage.py:266-269,281-292,321-331`. This is the inspected lane source, not a Git-object verification of the baseline bytes.
- The candidate adds `--audit-live-map` with `action="store_true"` and describes it as an additional check (`candidate/tools/check-registry-coverage.py:317-318`). Its invocation helper defaults `audit_live_map=False` and appends the flag only when requested (`:433-443`).
- Generic coverage runs first. With the flag absent, `map_findings` is an empty list; with it present, `_audit_live_map(rows)` runs. The metric key is separately emitted only under the same flag (`:348-355`). `_base_counts` itself has no audit metric (`:291-294`).
- Probe coverage requires code tokens 0 and 2, not the new exact live-map semantics (`:233-240`). Both the corrected map and the legacy map containing an additional live `1 DEGRADED` therefore remain acceptable to otherwise-clean generic coverage.
- Explicit-mode checking compares the selected audit row against the exact, whitespace-normalized mode-labelled constant (`:270-288`); that constant separates live 0/2 from selftest 0/1 (`:31-34`). The final status and return code follow the combined findings (`:351-362`), and JSON serialization includes the counts exactly as constructed (`:297-303`).

Thus default compatibility means both **no new semantic rejection** and **no new audit metric key**. A missing key is materially different from a reported zero: zero under the explicit flag means the finite map check ran and found no errors; absent means that check was not requested.

## One proposed mutant — leak the metric into default output

**Behavior-bearing point:** `candidate/tools/check-registry-coverage.py:354`.

Hypothetical mutation, not applied:

```diff
-        if args.audit_live_map:
+        if True:
             counts["audit_live_map_errors"] = len(map_findings)
```

This models accidentally dropping the output guard while refactoring count construction. Leave the semantic guard at line 351, the parser, the map comparator, and every fixture unchanged. It is one predicate mutation, not a second implementation of the check.

[INFERENCE] In default mode this adds `audit_live_map_errors: 0` even for a legacy live-1 map, because `map_findings` is still `[]`. Generic exit status, generic findings, and generic count values remain unchanged. Explicit-mode behavior remains unchanged. The defect is therefore specifically the loss of flag-controlled metric emission and the resulting unchecked-zero ambiguity, not an accidental default-on semantic audit.

## Same bounded detector: exact expectations

The following is a detector design only. All outcomes in this section are **[INFERENCE] source-derived expectations**, not captured outputs.

Use two otherwise-clean, single-tool committed fixtures with the existing fixture constructors:

- **G / corrected:** `SKILL.md = _skill([corrected_audit])`, and the only regular tool is `tools/boot-chain-audit.sh` containing the existing `audit_source` text. These are already defined at `candidate/tools/check-registry-coverage.py:565-568,575-577`.
- **L / legacy:** the same fixture except its audit row uses `legacy_audit`, inserting `1 DEGRADED` into the live clause and retaining the separate selftest clause (`:569-574,583-585`).

The source text is only inspected for the selftest token, not executed by coverage (`:247-255`). Fixture table/heading construction is at `:376-389`; the selected row's one-based location is retained at `:137-183`. For these exact `_skill([row])` fixtures, the sole row is `SKILL.md:6`.

Let `H_G` and `H_L` denote the respective valid landed fixture revisions. Do not invent their OIDs. No `--baseline-tools` argument is needed for this bounded detector. For both fixtures, the exact generic zero-finding counts are:

```json
{"tools_total":1,"rows_total":1,"registered":1,"missing":0,"findings":0}
```

Apply the same four assertions to pristine candidate bytes, the hypothetical mutated bytes, and exact restored pristine bytes:

| Fixture / invocation | Required pristine and restored result | Predicted mutant result |
|---|---|---|
| G: `--revision H_G` | exit **0**, status `PASS`, `findings=[]`; counts equal the five-key object above; **`audit_live_map_errors` absent** | Same exit, status, and findings; counts acquire **`audit_live_map_errors=0`**. Detector must reject the extra key. |
| L: `--revision H_L` | exit **0**, status `PASS`, `findings=[]`; same five-key counts; **`audit_live_map_errors` absent**. Legacy semantic wording does not change generic coverage. | Same exit, status, and findings; counts acquire **`audit_live_map_errors=0`** despite no semantic audit. Detector must reject the extra key. |
| G: `--revision H_G --audit-live-map` | exit **0**, status `PASS`, `findings=[]`; same generic counts plus **`audit_live_map_errors=0`** | Identical to required result. |
| L: `--revision H_L --audit-live-map` | exit **1**, status `FAIL`; counts exactly `tools_total=1, rows_total=1, registered=1, missing=0, findings=1, audit_live_map_errors=1`; findings exactly the object below | Identical to required result. |

The exact sole legacy explicit-mode finding is:

```json
{"id":"REGISTRY-AUDIT-LIVE-MAP","site":"SKILL.md:6","detail":"schema-v2 live0/2 and separate selftest0/1 map required"}
```

Also require `payload.revision == H_G` or `H_L` as appropriate, and unchanged binding metadata between the three evaluator-byte phases for the same fixture. A generic coverage failure, invalid revision, or table-selection failure makes this experiment inconclusive; it must not be counted as a killed mutant. These fixtures deliberately avoid unrelated findings so the metric boundary cannot be masked.

The decisive assertion is exact default count-key membership, not `counts.get("audit_live_map_errors", 0) == 0`: the latter accepts both the required absence and the mutant's leaked zero. Explicit G/L assertions simultaneously establish that the requested metric is genuinely measuring the semantic distinction rather than always reporting zero.

## Existing source-level coverage gap

1. **Default selftests do not assert metric absence.** The existing clean default invocation asserts status, tool total, registered count, and empty findings, but not the count-key set (`candidate/tools/check-registry-coverage.py:471-475`). The other default cases check particular findings/counts, not absence of the audit metric (`:477-563`). The corrected and legacy audit fixtures are never paired with default invocations; all four audit-map cases explicitly enable the flag (`:575-613`).
2. **[INFERENCE] This mutant would survive the current selftest assertions.** The four explicit audit cases see the same counts as before. Default cases receive an additional zero count that none of their predicates rejects. Early error cases are unaffected. This predicts survival of those assertions only; no selftest was run, and no actual survival verdict is claimed.
3. **The retained measurement driver does not close this output-contract gap by itself.** C3 before/after invocations include the flag; the separate `registry-coverage` invocation omits it (`.ufo/waves/round-20/measure/run.py:70-82`). Its recorder stores stdout/stderr but computes `matched_exit` only from the return code (`:31-43`). This mutation changes neither relevant exit. The driver's selftest loop delegates to the candidate's existing assertions (`:65-69`). The changed-tool smoke checks help/exit behavior, not default count keys (`.ufo/waves/round-20/measure/smoke.py:36-49`). No claim is made about unrelated labels or any later human review of retained stdout.

The narrow missing assertion is the paired default/explicit contract above, particularly `"audit_live_map_errors" not in payload["counts"]` for both valid default fixtures. The inspected implementation already has the required guard; this report does not recommend changing the contract or production code on the basis of a hypothetical survivor.

## Actual output, verdict, and restoration evidence

- **Actual detector output:** none. Pristine, mutated, and restored detector phases were not executed.
- **Verdict:** **UNEXECUTED**. Neither killed nor survived is an observed result. The proposed paired detector predicts a kill; the existing assertions predict survival, both explicitly source-level inferences.
- **Mutation/restoration:** no source bytes were written, no scratch mutation was applied, and no restoration action was needed. The only write by this seat is this named report. Exact source byte identity across time was not independently measured.
- **Before/after hashes:** before SHA-256 not computed; mutated SHA-256 not applicable because no mutant was materialized; restored SHA-256 not computed. No hash equality is claimed.
- **Limits:** read-only source/artifact inspection within the assigned candidate and exact R20 lane evidence. No subprocess, tests, build, lint, formatter, smoke, package install/update, external request, host operation, Git/jj mutation, integration decision, or runtime admission. No tool installs or updates. Boot images remain **UNKNOWN**; no host or boot-safety clearance is implied.

Scope: executed=none
