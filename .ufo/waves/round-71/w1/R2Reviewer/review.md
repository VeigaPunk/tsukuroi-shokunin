# R2Reviewer — C2 adversarial review

Axes: operability; C2 frozen predicate; falsification. Recommendation only, not admission.

## Findings by severity

### P2 — a surviving descendant escapes the per-case lifecycle
`tools/tsukuroi-census.sh:2673-2699`, `bounded_run`, polls only the direct child PID. If that child starts a grandchild and exits, the loop ends without TERM/KILL of the remaining process group. Exact helper attack: `bounded_run 1 bash -c 'sleep 30 & echo DESCENDANT=$!; exit 0'`. Receipt `attacks.txt`: timeout=0, rc=0, elapsed=102ms, group=1; descendant PID 3473487 remained non-zombie and alive after return. Reviewer killed that exact owned PID during cleanup. With the leader still waiting, the counterpart attack timeout=1 and killed the descendant, so negative-PGID signaling itself works. The missing case is a leader exiting before its descendant. Add that lifecycle case to catch leaked case work; the existing FIFO/TERM/slow R71-C2 cases do not test it. This finding does not claim that the frozen predicate explicitly requires descendants to be waited for after an otherwise successful case.

### Resolved during review — unbounded secondary callers
Measured revision sha256 `487feeb6caa687daf586d4b7577746e5f1ed22ca336e9c0e0194d13995bd4b3c` left `arm_run` and identity case children outside `bounded_run` (then lines 4230-4235 and 4024-4061), contradicting “every selftest case.” Reported to L1. Subsequent observed code routes arm_run and all six identity invocations through bounded_run/id_run. The two suite receipts below measure the earlier digest, not that repaired revision. Do not cite them as final-revision verification.

## Exercised evidence

- `selftest-run1.txt`: canonical landed script, external timeout 300s, rc=0, elapsed=54.997s, `TSUKUROI_CENSUS_SELFTEST: PASS (217 cases, 217 passed, 0 failed)`; exactly three emitted R71-C2 lines.
- `selftest-run2.txt`: same digest, external timeout 300s, rc=0, elapsed=56.985s, same 217/217/0 summary and three emitted R71-C2 lines. Timing fields differ; count/status determinism holds, not byte-identical output.
- Group a FIFO: timeout=1, rc=143, 1209ms under 1s plus grace; survived.
- Group b TERM-ignoring FIFO: timeout=1, rc=137, 1209ms; survived.
- Group c grandchild: killed when leader also blocks; survives when leader exits first; not survived overall.
- Group d 0.7s finishing child: timeout=0, rc=0, FINISHED, 705ms under 1s; survived.
- Group e unset/0/empty/non-numeric bound: exact configuration block resolves each to 60; explicit 1 resolves to 1. No unsupported rejection requirement inferred; survived documented fallback behavior.
- Group f normal suite exit and summary shape: rc0, PASS (217 cases, 217 passed, 0 failed), twice; survived.
- `live-diff.txt`: baseline/live rc both 1, rollup identical, five of six PLANE lines byte-identical. Only drivers differs in changing memory/swap/PSI counters; therefore literal live-output equality is NOT proven, and that drift is not attributed to harness code. The timeout helper is defined inside run_selftest, not live main.

## Patch applicability and review boundary

The assigned harness.patch was initially absent. E1Harness later supplied it and an already-applied copy; L1 stated the canonical harness had independently landed and instructed attacking those canonical bytes. Reviewer role forbids edits, so no clone, patch application, stage, commit, or lane modification was performed. Read-only `patch --dry-run --batch -p1 -d /home/vgpnk/Projects/shokunin/tsukuroi-shokunin -i /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-71/probes/E1Harness/harness.patch` returned rc1:

```text
checking file tools/tsukuroi-census.sh
Hunk #1 succeeded at 2710 with fuzz 1 (offset 65 lines).
Hunk #2 FAILED at 2922.
Hunk #3 FAILED at 2969.
Hunk #4 FAILED at 4258.
Hunk #5 succeeded at 4705 with fuzz 2 (offset 112 lines).
3 out of 5 hunks FAILED
```

This is an obsolete-wave-artifact result, not a canonical-code defect. Patch SHA256: `a363b3076d020f00d7aa58150325028cab17eb568fd4e96babeb3e07bcbe757c`. No actual sandbox application occurred.

## Residual risk and verification gaps

- LSP unavailable: `read xd://lsp` returned “No such tool”; references/definition/diagnostics unavailable. Text caller search was fallback, not semantic proof.
- Frozen declaration read from E1Harness's `scorecard-round71-declaration.md`, exported by its owner from commit `0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e`; current SCORECARD C2 was also read. Export provenance is owner-reported rather than independently git-verified here.
- Main must exercise the repaired final revision; these raw suites are revision-bound above. No alternate runtime, no saturation judgment, no resume-path changes in this C2 assignment.
- Host observations are read-only; no secrets or parameter values were inspected. No tools installed or upgraded. Scratch `/fast/scratch/hyaku/tsukuroi-r71/R2Reviewer` removed before completion; owned attack descendant explicitly killed.
- Self-evaluation: accuracy 4 (explicit revision/provenance limits); completeness 4 (sandbox application prohibited; final moving revision not rerun); clarity 4 (historical/repaired finding separated); actionability 4 (concrete missing descendant case); conciseness 4 (raw evidence kept outside findings). Overall 4.0. Main should bind final receipts to the repaired bytes before admission.

PATCH_APPLIES=no
CASES=217
PASS=217/217/0_twice
R71_C2_LINES=3_per_run
GROUPS_SURVIVED=a,b,d,e,f

## Requested repaired-revision follow-up (supersedes earlier status)

L1 explicitly requested repeating all attack groups after repairs. Exercised stable script SHA256 `a641bcf6b2eb1e37cece5afa79ce292be63667988937f2a31d5f9f0be3948fb9`; start/end digest identical. New receipts: `repaired-selftest.txt`, `repaired-attacks.txt`.

### P1 — bounded identity wrapper drops stdin and breaks the suite

The repaired stdin identity case passes its script through stdin into id_run/bounded_run, but bounded_run launches `setsid "$@" ... &` without explicitly forwarding stdin. The asynchronous shell child receives empty stdin. Direct exact-helper probe `bounded_run 1 bash -s <<< "echo STDIN_MARKER"` returns timeout=0 rc=0 with empty BOUND_OUT. Full suite exits 1: `TSUKUROI_CENSUS_SELFTEST: FAIL (219 cases, 217 passed, 2 failed)`. The two failures are the existing stdin-identity assertions: wanted exactly one output line, got none; expected verified=no, got none. See repaired-selftest.txt:220-225. Preserve the caller's input explicitly through the asynchronous launch rather than dropping or weakening these identity assertions. Reported immediately to L1.

The prior descendant leak is closed in this measured revision: both early-parent-exit and timeout-with-waiting-parent descendants are non-running after return. FIFO and TERM-ignore return timeout=1 rc=124 at ~3015ms under a 1s bound plus 2s grace; finishing child passes in 709ms. Unset/0/empty/non-numeric environment values still each resolve to 60. All four emitted R71-C2 selfchecks, including daemonizing-child, pass, but normal-suite group f fails because of the stdin regression.

UPDATED_CASES=219
UPDATED_PASS=217_passed_2_failed
UPDATED_R71_C2_LINES=4
UPDATED_GROUPS_SURVIVED=a,b,c,d,e
UPDATED_GROUP_F=failed_stdin_identity_regression
UPDATED_SCRATCH_REMOVED=yes
