# C1ReportTrace — Round20 attempt1

## Findings, by severity

**No concrete broken/circular C1 source provenance, counting-command mismatch, or author-swarm-to-outside-verifier substitution was established in the inspected artifacts.** The source trace is coherent, but it ends at a planned evaluation/report rather than an observed C1 result. This is a recommendation from source review, not claim admission.

### Low — the planned ledger summary is exit-only, not a C1 contract assertion

`.ufo/waves/round-20/measure/run.py:31-44` saves raw stdout/stderr and records `matched_exit` solely as `p.returncode == want`. Its C1 caller at `:70-78` expects before exit 1 and after exit 0, but does not parse or assert the emitted revision, `counts.ownership_corrections`, or finding IDs. The preregistration requires missing `OWNERSHIP-CORRECTION-MISSING`, altered `OWNERSHIP-CORRECTION-INVALID`, and positive `ownership_corrections=1; exit=0` (`.ufo/waves/round-20/preregister.json:31-35`).

[INFERENCE] A before result with exit 1 for an unrelated legacy anchor finding would receive `matched_exit: true` without establishing the preregistered missing-correction failure. Similarly, an exit-only summary cannot independently establish the numeric 0→1 delta. The current candidate's source does wire the metric correctly; this observation is about what the retained summary proves, not an observed wrong candidate output.

The runner explicitly says “no automatic claim admission” (`measure/run.py:114`), and the source lesson leaves numeric admission pending (`corpus/lessons/round-20.md:7,45,51`). Therefore this is **not evidence of an existing false-pass or dishonest report**. The final report must cite the actual C1 stdout fields/IDs and bound revisions, not promote `matched_exit` or the runner's own completion into metric verification. A summary-only C1 certification would be unsupported.

## End-to-end trace

Paths below are relative to the production lane unless shown as absolute.

| Link | Exact evidence | Trace result |
|---|---|---|
| Frozen claim identity | `.ufo/waves/round-20/preregister.json:3-11` | Baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472`; C1 adjacency; metric `ownership_corrections` 0→1; precise sibling declaration without arbitration/write authority. |
| LOG registration | `LOG.md:1027-1029,1035` | Same baseline and C1 ownership-clarification intent; references SCORECARD/preregistration, isolates four candidate worktrees, and says verification had not run at declaration. These are author statements, not independently authenticated chronology. |
| SCORECARD counting contract | `SCORECARD.md:616-626` | C1 adjacency 8→8, ordinal delta 0; same 0→1 metric and exact command; measurements explicitly unobserved pending recorded L1 evaluation. Saturation 9/window 3 is retained, not an uplift or new capability claim. |
| Fixed correction input | `.ufo/waves/round-20/ownership-correction.txt:1` | Precise artifact classes, explicit non-grant, unresolved Kaidoku/Revenger arbitration, and no configuration/service/package/boot/sibling-file writes. |
| Published correction | `PROVINCE.md:148-152` | Same correction under the named OUT-009 heading. Explanation explicitly supersedes the old ownership/package paraphrase, preserves the other nine locators and handoff states, and repeats the exact counting command. |
| Historical proposition being corrected | `PROVINCE.md:128-132`; `corpus/knowledge/adjacency-anchors-r19.json:112-123` | The stronger “Revenger owns”/bare “packages” text is retained as historical evidence, not silently rewritten. The named correction identifies that exact proposition. |
| Candidate binding | `.ufo/waves/round-20/worktree-bindings.json:2-7`; `seeded-implementation.json:4,10-11` | C1 worktree is `/tmp/tsukuroi-r20-adjacency-20261021`; ExecAdjacency owns the new mode; L1 final evaluation is reserved and seed metadata does not claim a pass. |
| Candidate count definition | `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:43-65,135-196` | Fixed expected correction, explanation and R20 baseline; original registry/census pins; exact baseline-prefix plus exact appended suffix; snapshot digest/quote/heading and preserved arbitration; accepted case returns exactly `(1, [])`, refusals return count 0 with findings. |
| Count propagation and observable CLI | Same candidate `:761-775,783-788,819-840` | CLI flag reaches `evaluate`, which writes `counts["ownership_corrections"]`; JSON emits counts and findings with the bound revision. No alternative metric with the same name was found in the scoped literal caller search. |
| Planned immutable evaluation | `.ufo/waves/round-20/measure/run.py:53-64,70-78` | One checkout of the final supplied revision supplies the evaluator for both baseline and after runs. Evaluator digests are planned for retention. The C1 argv exactly matches preregistration/SCORECARD, with only `<REV>` substituted. |
| Planned report/closure boundary | `corpus/lessons/round-20.md:7,45,49-51`; `corpus/README.md:182-188` | Final measured revision, actual wave accounting and retained results belong in the later ledger/scorecard/report. Author-dispatched seats are not outside closure. No measured C1 verdict is supplied by these planning statements. |

### Evidence pointer is not circular

The correction's source pointer at `PROVINCE.md:152` leads to the OUT-009 registry record, which provides a concrete snapshot path, full sibling commit, recorded blob SHA-256, heading and exact quote (`corpus/knowledge/adjacency-anchors-r19.json:112-123`). The local retained snapshot actually contains the named source classes, including **Electron/JavaScript packages**, at `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md:3-7`; its separate repository-only/no-substrate-remediation boundary is at `:25-29`. This chain reaches source text, not merely another author assertion that the correction is true.

S078 points to the same concrete snapshot with the same recorded commit/digest (`corpus/SOURCES.md:85`); the knowledge entry identifies it as an attributed declaration, not an integrator ruling (`corpus/knowledge/contract-corrections-r20.md:1-11`). The candidate freezes that source identity and reads the snapshot to compare its digest/quote (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:77-100,140-154,178-195`). The R19 schema baseline at candidate `:21` and R20 ownership baseline at `:65` have distinct purposes; they are not conflicting claim baselines.

The helper does not read the correction's own “Source:” wording as proof. It compares fixed expected bytes and then checks the independent retained sibling declaration. That is a deliberately finite correction check, not an unrestricted semantic ownership verifier. Digest equality and original sibling-object authenticity were not recomputed by this seat.

### Author-produced oracle is not outside verification

`build/OracleC1.md:7-11` discloses no execution, no Git authentication of working-tree bytes to the baseline, and a C2/C3 scope deviation. Its C1 section distinguishes source-supported semantics from preregistered new IDs and unimplemented baseline mode behavior (`:15-25`). In particular, it does not claim the baseline evaluator already emitted this new metric. Its C2/C3 sections must not be treated as independent C1-oracle work or as outside claim closure.

The production lesson expressly calls these expectations for the **author-side evaluator**, not outside SHONEN/final admission (`corpus/lessons/round-20.md:49-51`). The ownership draft also distinguishes author-side replay/swarm work from outside closure and labels the evaluator unrun/pending (`build/ScribeOwnership.md:15,35`). No contrary current admission claim was observed in the scoped LOG/SCORECARD/knowledge/report-planning trace.

## Residual risk and verification gaps

- At inspection, the round20 measurement inventory contained `run.py` and `smoke.py`, not retained C1 before/after stdout, result JSON or evaluator-digest receipts. No final R20 report was found in the scoped lane report inventory. This is a premeasurement/final-report gap, not proof that a planned run failed or a report was falsely completed.
- The production checker inspected still exposes the R19 parser without `--ownership-corrections` (`tools/check-adjacency-anchors.py:613-629`), while the external candidate adds it (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:783-788`). Therefore executing the current production/baseline executable with the new flag would not establish the claimed baseline count. The planned final runner avoids that mismatch by using the final evaluator for both revisions (`measure/run.py:53-78`); actual final executable identity remains unobserved.
- The planned source logic supports one canonical final evaluator, not a second review runtime. This seat did not invoke any runtime, inspect route/model/configuration, authenticate Git state, or assess resume-continuity preflights; those are not established by this C1 trace.
- LSP status/references/definition/diagnostics were unavailable through this seat's authorized interface: NO-EXEC permits only read/grep/glob and the named report write. Literal grep was used only to locate candidate definitions/callers and documents; it is not semantic caller or diagnostic proof. Source conclusions above come from the cited read ranges.
- No build, test, lint, formatter, smoke, command/subprocess, external request, host probe, target execution, digest recomputation, Git operation, tool install/update, delegation, code edit, sibling write or shared-state write was performed. Only this named report was written.
- Boot images remain **UNKNOWN**. No host/boot safety, remediation permission, arbitration ruling, handoff acceptance, saturation uplift or final claim admission follows from this report.

Scope: executed=none
