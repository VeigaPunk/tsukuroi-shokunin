# MutFxLog — mutation-log audit

## Attacked claim and axes

Primary attack: **frontier/evidence calibration** — whether the retained mutation log establishes 27 meaningful behavioral kills supporting C1/C2/C3. This is not an attack on a claimed native permission boundary: the preregistration explicitly excludes native enforcement and effect/reading proof.

Named axes: **depth (C1)**, sensitivity of the eight finite edit-contract decisions; **operability (C2)**, explicit v2 edit authority and v1 continuity; **calibration (C3)**, the fixed-cohort census ledger and honest distinction between a detected regression and an unevaluable probe.

**Finding:** the retained mutants have identifiable behavioral targets and matching static controls, but the log's criterion, “killed = nonzero exit,” is insufficient without pristine/restored controls and failure attribution. The log reports 27 kills; this read-only audit cannot independently validate those kills. No concrete failure of the landed C1/C2/C3 acceptance behavior was executed or established here.

## Authorized bounded search and evidence

Only the named mutation log, preregistration, three named detector sources, and the authorized Godspeed skill were read. No commands, subprocesses, imports, tests, hashing, fetching, installation, delegation, or scratch mutation were performed. The supplied digest is a declared identity, not an independently verified digest.

Evidence references below use these exact files:

- **M:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/.ufo/waves/round-23/measure/l1-mutation.json`, lines 1–257.
- **P:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json`, lines 26–55 and 98–115.
- **E:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-edit-contract.py`, lines 1–283.
- **B:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-seat-bindings.py`, lines 1–396.
- **R:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-path-reconciliation.py`, lines 1–387.

The mutation harness, earlier survivor runs, temporary copies, and imported revision helper are not available within this binding. No additional file was opened to fill those gaps.

## 1. Concrete falsifier of the kill criterion's sufficiency

M:4 defines a kill solely as a nonzero selftest exit. M:10–256 records only tool, mutant number, replacement strings, exit, a `selftest` status string, and a Boolean kill. It contains no pristine run, restored run, failed-case observations, stderr, replacement-match evidence, or before/mutated/restored byte identities.

**[INFERENCE — counterexample, not an observed incident]:** a temporary-copy setup that omits the imported revision helper fails at module import before reaching any selftest. All three sources import that helper before argument handling (E:12, B:13, R:20). Such an import failure can exit 1 for pristine, mutated, and restored bytes alike. The stated nonzero-only rule would nevertheless call the mutated run killed. A baseline failure must instead make that probe inconclusive. The recorded `exit: 1` does not distinguish this case from an actual failed assertion. This does not assert that the logged runs suffered this setup failure; their raw output and controls are absent.

There is a useful qualification: if a correctly prepared pristine run passes and the unchanged detector emits a complete failed-case report only after the intended production mutation, a nonzero selftest exit is a reasonable summary. A mutation-induced crash can also be a real detection when its causal connection is evidenced; infrastructure failures cannot simply be pooled with it. Here the detector sources do compare expected evaluator exit codes and finding IDs, then emit observations and return a failed-case Boolean (E:237–245, B:338–353, R:330–349). That structure is substantially stronger than the log preserves. An evaluator returning a denial or CANNOT_EVALUATE in a negative fixture is not itself a failed selftest; it may be the expected passing observation.

**Smallest remedy:** retain actual pristine/mutated/restored outputs under the same bounded detector and environment, exact mutation application evidence, and byte identities; attribute each kill to a changed expected case or a demonstrated mutation-caused failure. If those records cannot be recovered, label the existing 27 entries **reported, unvalidated kills / inconclusive as paired mutation evidence**, not independently confirmed kills. Do not fabricate missing output or rerun under this NO-EXEC seat.

## 2. Meaningfulness of the 27 retained mutants

The following is a static mapping, **not executed detector output**. Every retained mutation has an identifiable guard or classification target. Several are strict-schema or diagnostic-classification mutations, not authorization bypasses, and multiple mutants test related guards rather than independent new capabilities.

| Claim / logged mutant | Changed behavior | Existing expected detector/control |
|---|---|---|
| C3 / 0 | Rough rule incorrectly accepts raw-first selectors | `rough-misses-raw-first`; `mixed-raw-range-order` |
| C3 / 1 | Removes exact derived/recorded ledger equality | `forged-disposition`, `dropped-row`, `duplicate-row` |
| C3 / 2 | Disables frozen-input digest comparison | `snapshot-tampered` |
| C3 / 3 | Replaces the first bad component's actual index with zero | `one-per-event-vs-per-component` |
| C3 / 4 | Skips rough path-denied components | Rough-rule unit controls and path-count fixtures |
| C3 / 5 | Relaxes unit-difference justification to any retained finding | `unit-count-mismatch` / `selector-but-retained` |
| C3 / 6 | Removes retained-count agreement with declared totals | `wrong-retained-total` |
| C3 / 7 | Drops canonical local-spelling validation | `canonical-dot-denied` |
| C3 / 8 | Strips arbitrary colon tokens as selectors | `canonical-invalid-token-denied` |
| C3 / 9 | Removes explicit orphan-finding detection | `orphan-retained` requires its specific finding ID |
| C1 / 0 | Ignores prose-table correspondence | Per-decision `table-*`, hidden/fenced prose controls |
| C1 / 1 | Stops checking preregistered policy correspondence | `policy-source-swap`, `policy-source-missing` |
| C1 / 2 | Accepts every evidence shape set | `evidence-unknown-key`, `evidence-one-shape` |
| C1 / 3 | Accepts any nonempty evidence shape set | Same two shape controls; related to, not independent of, mutant 2 |
| C1 / 4 | Stops requiring the visible prose scope limitation | `limit-omitted`, `hidden-limit` |
| C1 / 5 | Allows extra decision-row fields | `extra-row-field` |
| C1 / 6 | Ignores source ownership/tier cells | `source-wrong-tier` |
| C2 / 0 | Allows edit classification without validated v2 mode | v1 `unknown` and v1 continuity controls |
| C2 / 1 | Makes read authority an alternative edit grant | `v2-read-only-target` |
| C2 / 2 | Drops the edit-target read-authority subset requirement | `v2-edit-not-readable` |
| C2 / 3 | Drops the edit-target write-authority subset requirement | `v2-edit-not-writable` |
| C2 / 4 | Allows extra v2 seat keys | `v2-row-marker` |
| C2 / 5 | Accepts path-bearing edit arguments outside the two finite shapes | `v2-unknown-key`, `v2-mixed-shapes`, `v2-half-replace` |
| C2 / 6 | Loses v2 mode during wrapper recursion | `v2-nested-edit`, `v2-nested-denied` |
| C2 / 7 | Reports structured mode enabled even on unevaluable v2 input | v2 schema-error controls require mode zero |
| C2 / 8 | Changes URL-edit denial from FETCH-DENIED to EDIT-DENIED | `v2-url-target` requires the FETCH-DENIED finding |
| C2 / 9 | Treats v1 as a structured-edit schema | `v1-extra-edit-field-no-grant`, `v1-edit-continuity` |

Control definitions: E:195–245, B:210–353, R:291–349. The replacement strings and retained kill labels are M:10–253.

C3/7's direct unit fixture deliberately supplies a dot-segment path in its authority list. It tests local-validation defense behavior; it is not evidence that the fixed r22 cohorts actually contain that input. C2/8 remains a denial after mutation: its significance is correct audit categorization, not successful remote editing. The 27 retained mutations therefore must not be narrated as 27 independent security fixes, eight repaired runtime behaviors, or a measured Pareto improvement. P:34,43,52,55 explicitly states the narrower acceptance boundaries.

## 3. Survivor accounting: disclosed, but classifications need separation

M:5–8 explicitly discloses three earlier survivor descriptions. That is evidence against a claim that all prior survivors were silently omitted, but it does not include their original replacement strings, outputs, byte identities, or retest history. The common label `survivors_fixed_before_record` merges materially different dispositions:

1. **Selector-token survivor — detector strengthened.** The log says a new `canonical-invalid-token-denied` control was added. R:342 contains that exact named control. M:84–90 retains the corresponding unconditional `return base` mutant as C3/8 with `exit: 1`, `selftest: FAIL`, `killed: true`. This supports the stated repair mechanism by inspection; the earlier survival and paired retest remain unverified.
2. **Per-row shape guard — described equivalence / redundant code removed.** E:102–112 collects every observed key shape and requires equality with the complete allowed shape set. For the described redundant membership check, that equality already prevents any extra shape and requires both allowed shapes. Removing a separate per-row membership guard is consistent with equivalence under these preconditions, not a newly killed non-equivalent survivor. The exact retired mutation is absent, so historical equivalence cannot be certified beyond the described check.
3. **Edit-locality guard — described equivalence / redundant code removed.** B:155–161 validates every declared edit target as local and present in both authority lists; B:128–130 accepts only membership in that validated edit-target list. On the supported `evaluate` path, repeating a local check in `classify_edit` is redundant. This is not universal equivalence for arbitrary direct callers with unvalidated bindings, which are not the claimed entry path. Again, exact prior mutation evidence is missing.

**Smallest remedy:** separate the survivor record into “test strengthened and corresponding mutant retested” versus “declared equivalent under explicit preconditions; redundant guard/mutant retired.” Keep the earlier attempts visible with available evidence and do not turn equivalence retirement into a behavioral kill. There is no basis in the allowed files to accuse the author of dishonesty, but the current shared heading and missing history are insufficient for a reproducible survivor disposition audit. Do not infer a complete attempted-mutant denominator from the 27 retained rows plus these three descriptions.

## Selected mutation probe, actual output, verdict, restoration

- **Mutant examined:** retained C2/8, deleting URL/fetch classification before exact edit-target membership (M:236–243; B:119–130).
- **Expected detector:** `v2-url-target` (B:309,344–350). **[INFERENCE]** the mutated evaluator returns exit 1 with `SCOPE-EDIT-DENIED`, whereas the fixture requires exit 1 with `SCOPE-FETCH-DENIED`; the selftest should fail because the required finding ID is absent. No edit permission is granted.
- **Actual available output:** the log records `exit: 1`, `selftest: "FAIL"`, `killed: true` for this mutant. For all retained entries it records the same three values, with totals `killed: 27`, `total: 27` (M:255–256). These are author-side recorded fields, not stdout/stderr reproduced by this seat.
- **Verdict:** statically meaningful classification mutant; recorded as killed; **independent behavioral verdict INCONCLUSIVE** because no authorized run or paired pristine/restored output is available. No newly executed kill or surviving mutant is claimed. The counterexample in section 1 falsifies the sufficiency of the stated kill rule alone, not the actual landed acceptance behavior.
- **Restoration evidence:** no detector, helper, candidate log, or scratch bytes were written by this seat; the only write is this authorized report. Consequently no mutated source required restoration. Before/after source hashes were neither supplied in the log nor computed here. Exact restoration of the author's temporary copies cannot be established from the available record.
- **Remaining prerequisite:** independently confirming the 27 kills requires the missing paired run records, or a separately authorized controlled probe. This seat cannot create that evidence: its command/fetch lists are empty and its sole write/edit target is this report. No other runtime was invoked and no production remedy was applied.

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: 0099486dd22e437a6f8609486657b87f6d0639d3a51ff02e8db8219256f1975d
Predicate: r23f-mutfxlog
Scope: executed=none
