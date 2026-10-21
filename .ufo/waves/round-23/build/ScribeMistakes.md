# ScribeMistakes: r22 quality verdict correction draft (round 23, attempt 1)

Mode: NO-EXEC, NO-FETCH, leaf seat. No command, fetch, hash, list, or install was run. No installs are recorded because this seat's scope forbids them.

Sources read: `sources/r22-closure.json` (full, raw lines 1-42), `preregister.json` (raw lines 1-121), `sources/godspeed-directive.txt`, `skill://godspeed`, `snapshot/corpus/QUALITY.md` (criteria 1-48).

Not read: `.ufo/reports/round-22/tsukuroi.md` (the author report) and `corpus/lessons/round-22.md`. Both are outside the declared read paths. The outside entry 422 is seen only through the `outside_round22` summary in `preregister.json`.

## 1. Premise check

The assignment frames the r22 author verdict as "quality improved" against outside "quality unchanged". The declared sources do not support that framing.

- `r22-closure.json` line 25: `trends.quality` = `"unchanged"`.
- `r22-closure.json` lines 15-22: `verdicts` has no `quality` key. Its keys are depth, operability, calibration (all `improved`), coverage, freshness, and adjacency (all `unchanged`).
- `r22-closure.json` notes: "Quality trend unchanged: in-round gate hardening and registry repair concern new material; no prior entry superseded or re-verified."
- `preregister.json` `outside_round22.trends.quality` = `"unchanged"`.

Result: the declared author and outside sources agree on quality (unchanged). No quality disagreement exists in them. I disagree with the premise as stated. Any "quality improved" wording inside the undeclared author report is unverified by this seat.

The real author/outside divergence in the declared sources is calibration path counts (section 2, row 4).

## 2. Agree / disagree

| # | Item | Verdict | Reason (sources) |
|---|------|---------|------------------|
| 1 | Quality unchanged (author and outside) | Agree | The closure gives its reason: only new material, and no prior entry was superseded or re-verified. This matches QUALITY 3 (observation/inference/unknown kept separate) and QUALITY 4 (append-only errata). |
| 2 | Discernment improved (author and outside) | Agree | Both sources record it. This seat does not re-audit it. |
| 3 | Depth and operability improved (author) | Agree, bounded | The closure calls C1 and C2 bounded instruments, not enforcement ("never prevents calls"; "not enforcement"). That matches QUALITY 47. |
| 4 | Calibration improved (author), against outside path counts | Disagree as settled | Outside rough counts are build 25 / falsify 33. Outside lane counts are build 23 / falsify 29. The closure's own recheck reports the same two numbers (its approximate census 25/33 and checker 23/29). It then calls the gap "selector-normalization differences, not decisive" with no per-path attribution. That is an inference presented without a bounded sweep (QUALITY 3, 9). The preregister records `before: 2` unexplained cohorts for C3. The calibration verdict should stay conditional until C3 attributes every event. |
| 5 | Two forbidden Bash calls called "process noncompliance, not axis harm" | Agree on harm, disagree on closure | The raw-transcript reads are read-only (`sha256sum` plus `wc -l`). No writes or host effects are recorded, so axis harm is not shown. QUALITY 46 still requires a scope/calibration defect to be reported even when the declaration gate is green. The closure lists the calls in its notes but does not record them as calibration defects. Correction: record them as calibration defects. Do not clear them. |
| 6 | "Evidence-verified (not rerun)" wording in rechecks | Partly agree | The closure separates retained-evidence checks from reruns. The label "Evidence-verified" is still ambiguous. QUALITY 3 and 14 require the label to say which kind of check was performed. Use "retained-evidence observed" for items not rerun. |
| 7 | Source-only checker existence as quality (C1 eight decisions, C2 v2 schema, `tools/check-*.py` present) | Disagree | The preregister itself scopes C1 as "new document contract, not eight repaired runtime behaviors" and C2 as "no native enforcement/effects claim". QUALITY 19 and 23 say a passing structural count does not establish source agreement, and a fixture must fail the preserved prior defect. These belong under depth/operability. They are not quality. |
| 8 | No native per-seat restrictive tool interface | Agree | `preregister.json` limits and closure notes both state it. QUALITY 47 applies. |

## 3. Draft correction (report only; not applied to QUALITY.md)

Candidate criterion 49, probation draft, not admitted:

> 49. **Quality trend needs re-verification, not new gates (R22-QUALITY-TREND):** a quality improvement is recorded only when an existing corpus entry is re-verified against a located source anchor, or when a preserved prior defect is retired by an append-only named correction whose fail-capable check rejects that defect. New checkers, schemas, fixtures, registries, contract documents, and passing source-only counts are recorded under their own axis (depth, operability, calibration), never as quality. Round 22 quality is unchanged: no prior entry was superseded or re-verified. Sources: `r22-closure.json` trends and notes; `preregister.json` `outside_round22.trends`.

Candidate mistake entries for the round-22 record (appended, not rewritten):

- **R22-CALIBRATION-DISMISSAL:** rough-versus-lane path counts (25/33 vs 23/29) were attributed to "selector-normalization, not decisive" without per-path attribution. Keep these as unexplained until C3 attributes every event. Do not let that label clear the r22 calibration verdict.
- **R22-DECLARATION-SCOPE:** two forbidden Bash calls were classed as process noncompliance only. Record them also as scope/calibration defects (QUALITY 46). They are not axis harm, and this classification does not clear them.
- **R22-EVIDENCE-LABEL:** "Evidence-verified (not rerun)" blurs retained-evidence observation with rerun verification. Relabel the item as retained-evidence observed (QUALITY 3, 14).

## 4. Limits

- The undeclared author report (`.ufo/reports/round-22/tsukuroi.md`) was not read. Any report-level quality claim is unverified here.
- The outside entry 422 is seen only through the preregister summary.
- The SHA-256 supplied for `r22-closure.json` is a declared identity. It was not computed or checked.
- No checker was run. The C1, C2, and C3 status is taken from the declared sources, not observed.
- Nothing was edited except this report.

Reviewed-SHA256: e13cde76422140a13284f730950f2bf36d308d55e30ce956bc59ff5af7d9e68c
Predicate: r23-scribemistakes
Scope: executed=none
