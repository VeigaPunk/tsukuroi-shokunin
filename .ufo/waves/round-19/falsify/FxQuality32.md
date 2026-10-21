## Attack

Tested QUALITY criterion 32 (R19-ADJ-POINTERS): whether the baseline evaluated with the target registry is red for both outbound and inbound publication, whether the selftest kills both wrong-classification directions, and whether publishing outbound anchors could mask an all-`RESOLVES` inbound-registry regression.

## Method

- Ran `python3 tools/check-adjacency-anchors.py --revision 452a054677f6b18284917d7c08c45361f91c25ac --registry-from 8e5916360f2dfe7bc4eb4ba144081af555900116`.
- Ran `python3 tools/check-adjacency-anchors.py --selftest`.
- Ran `python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116`.
- In a fresh `/tmp` clone at `8e5916360f2dfe7bc4eb4ba144081af555900116`, checked every inbound evidence quote against its `found_line` in the target file and compared that line with `target_ranges`. No target-revision files were modified.

## Verdict

**CONFIRM — QUALITY #32 catches the requested classification-only regression.** The baseline replay fails with exactly 10 outbound `ANCHOR-UNPUBLISHED` and 114 inbound `INBOUND-UNPUBLISHED` findings. The target passes with 10/10 outbound anchors and 114/114 inbound classifications. The selftest passes both wrong-classification fixtures. **[INFERENCE]** If the 17 target `DRIFTED` classifications alone were changed to `RESOLVES` while their quotes, found lines, and target ranges stayed intact, the gate would emit 17 `INBOUND-CLASSIFICATION-WRONG` findings; publishing outbound anchors does not bypass the inbound checks.

## Evidence

- The criterion requires portable publication for all ten outbound pointers and a found line plus class for each inbound pointer: `corpus/QUALITY.md:53-63`.
- Baseline replay output: `status=FAIL`; counts show `outbound_total=10`, `outbound_portable=0`, `inbound_total=114`, `inbound_classified=0`; findings are exactly `ANCHOR-UNPUBLISHED: 10` and `INBOUND-UNPUBLISHED: 114` (exit 1). The outbound findings are at registry `outbound[0..9]`; the inbound findings are at `inbound[0..113]`.
- The selftest output is `PASS (12 cases, 12 passed, 0 failed)`. `tools/check-adjacency-anchors.py:723-739` verifies each fixture's exact expected exit code and finding IDs; lines 825-834 define `wrong-resolves-outside-range` and `wrong-drifted-inside-range`, each expecting `INBOUND-CLASSIFICATION-WRONG`.
- Target self-check output is `status=PASS`, with 10/10 outbound anchors and 114/114 inbound records classified (97 `RESOLVES`, 17 `DRIFTED`; 25 operative, 89 historical; exit 0).
- The gate checks the actual quote occurrence at `found_line`, derives `RESOLVES` only when that line lies in the census ranges and otherwise derives `DRIFTED`, and emits `INBOUND-CLASSIFICATION-WRONG` for a mismatch: `tools/check-adjacency-anchors.py:521-545`.
- The read-only target-data check found 114/114 existing records consistent with that rule. All 17 `DRIFTED` rows have a quote at `found_line` outside their target ranges; relabeling those rows as `RESOLVES` would therefore mismatch the derived class for 17 rows. Example: `IN-001` has `found_line=51`, `target_ranges=[[42,42]]`.

## Residual

I did not commit and run a separate all-114-rows-`RESOLVES` mutant. Its predicted 17 classification failures are an inference from the gate's checked rule and the observed target records; the selftest directly exercises both mismatch directions on fixtures. No tools were installed or updated.

Scope: executed=python3 tools/check-adjacency-anchors.py --revision 452a054677f6b18284917d7c08c45361f91c25ac --registry-from 8e5916360f2dfe7bc4eb4ba144081af555900116; python3 tools/check-adjacency-anchors.py --selftest; python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116