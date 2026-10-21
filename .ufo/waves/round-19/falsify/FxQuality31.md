## Attack

Attack R19-SEAT-DECLARE / QUALITY 31 on whether its required dispatch class and exact-command restrictions are enforced by a fail-capable gate, and whether the round-19 build red is preserved rather than reclassified. A classless dispatch with `Scope: executed=none` is a direct counterexample candidate: QUALITY 31 calls for a non-zero gate result if such an item is dispatched, so the gate should not pass it cleanly.

## Method

- Ran `python3 tools/check-seat-scope.py --revision 7cc59c8e3761ffb668067c47655216376f0a4e48 --wave .ufo/waves/round-19/build`.
- Ran `python3 tools/check-seat-scope.py --selftest`.
- Read QUALITY 31, the committed round-19 outcome and landed measurement, the gate evaluation/selftest code, the round-19 lesson, and the relevant dispatch/report records. Ran `python3 -B /tmp/fx31/analyze.py` to compare the committed spec, dispatch, registry and report trailers without changing lane files.

## Verdict

**REFUTE — QUALITY 31 / R19-SEAT-DECLARE (gate-backed enforcement).** The specified build-wave measurement is genuine and remains red, and the selftest contains red cases. However, the gate accepts a classless seat when its report says `executed=none`; it therefore does not enforce the criterion's stated classless-dispatch falsifier. It also checks only for the `EXEC-AUTHORIZED` substring when commands are reported, not whether those commands are within the authorization's exact list.

## Evidence

- `corpus/QUALITY.md:42-50` requires a dispatch-time class and exact commands, says the gate must have zero named violations for green, and identifies a classless dispatch as a falsifier.
- Revision-mode check exited 1 at `7cc59c8e3761ffb668067c47655216376f0a4e48`; its JSON reported `SCOPE-EXEC-UNAUTHORIZED: 14`, `SCOPE-UNDECLARED: 1`, `SCOPE-REPORT-MISSING: 0`, and `SCOPE-TRAILER-MALFORMED: 0`. `.ufo/waves/round-19/build/outcome.json:19` records the same 14/1/0/0 counts. The landed record `.ufo/waves/round-19/measure/build-landed/seat-scope-build.stdout:1` also records 14/1/0/0 at that revision. Thus the build red was retained, not converted to green.
- `tools/check-seat-scope.py:75-91` continues immediately when the final trailer is `none`; only for a command-list trailer does it test whether the prompt contains `EXEC-AUTHORIZED`. There is no check that a prompt has exactly one dispatch class or that reported commands match the authorized list.
- The selftest passed: `CHECK_SEAT_SCOPE_SELFTEST: PASS (54 cases, 54 passed, 0 failed)`. Its source supplies the counterexample: `tools/check-seat-scope.py:331-335` defines `plain` seats with empty prompts and expects the `clean` case with `Scope: executed=none` to pass. The suite also has a fail-capable unauthorized-command case and an authorized-command case at `:337-343`; these establish some failure sensitivity, not the missing class check.
- The missing exact-command check is observable in a real report: `.ufo/waves/round-19/build/spec.json:338-340` gives `ReviewSnapshotBytes` the two authorized command forms and says “nothing else”; `.ufo/waves/round-19/build/ReviewSnapshotBytes.md:24,28` discloses additional `jq`/`cat` use beyond those forms. The gate's output contains no finding for that seat, although the overall command exits 1 for other seats. The disclosed deviation remains in the report, but the gate does not validate the exact-command restriction.
- The red itself is not relabelled: `corpus/lessons/round-19.md:52,64` records the build red and says the waves were re-measured at a landed hash. However, line 52's phrase “although each item said NO-EXEC” is inconsistent with the dispatched classes: the `ReviewSnapshotBytes` authorization at `spec.json:340` is one explicit `EXEC-AUTHORIZED` example; line 64's “NO-EXEC or EXEC-AUTHORIZED per item” is the accurate summary.

## Residual

The actual build's committed specification and dispatch have no class-marker mismatch in the read-only comparison; this attack does not find a classless item in that wave. Accordingly, the reproduced false-green path is a gate/selftest defect, not evidence that the landed build wave itself was green. I did not run the falsify-wave gate at the build revision: its recorded landed measurement is `CANNOT_EVALUATE` because that wave's registry/spec did not exist at 7cc59c8.

Scope: executed=python3 tools/check-seat-scope.py --revision 7cc59c8e3761ffb668067c47655216376f0a4e48 --wave .ufo/waves/round-19/build; python3 tools/check-seat-scope.py --selftest; python3 -B /tmp/fx31/analyze.py