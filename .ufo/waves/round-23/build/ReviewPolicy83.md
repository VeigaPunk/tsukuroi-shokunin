# ReviewPolicy83 — r23 prospective-only audit of the new v2 edit authority against frozen r22 evidence

Seat: `TsukuroiR23-2.ReviewPolicy83-7` (leaf reviewer, no subagent dispatch).
Predicate value: `r23-reviewpolicy83`. Baseline: `ae01e50f582016384e620022be38bf5367000e2e`.

## 1. Method and evidence surface

Read (declared seat read paths only, absolute paths under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`):

| # | Path | Role in this review |
|---|---|---|
| S-A | `.ufo/waves/round-23/snapshot/corpus/lessons/round-22.md` | frozen r22 lesson corpus; declared SHA256 `2fd1a5bca6633a0ede1de5efc4d0ff5504bb3bc9f3676dbee11addb8c53376f5` (supplied declaration, **not** independently computed — no hash/wc/command was run) |
| S-B | `.ufo/waves/round-23/preregister.json` | r23 frozen claims C1/C2/C3, edit_decisions, ordinals, limits, outside-r22 admission |
| S-C | `.ufo/waves/round-23/sources/edit-decision-policy.json` | the new v2 structured-edit decision authority under review |
| S-D | `.ufo/waves/round-23/sources/godspeed-directive.txt` + `skill://godspeed` | posture/directive |
| S-E | `.ufo/waves/round-23/build/ReviewPolicy83.md` | this report (absent at read time; written by this seat) |

No command, fetch, subprocess, import, compile, test, lint, format, hash or directory listing was executed (`commands: []`, `fetches: []` — NO-EXEC / NO-FETCH). No sibling file, production file, Git state or route was touched. No child task, background job or peer was dispatched.

Tooling transparency: the `lsp` device was **not** reachable in this seat. The xd:// route space is forbidden outright by the seat contract ("No web_search/browser/URL/xd/proc/agent fetch"), so `read xd://lsp` status could not be performed and no LSP server could be asked about S-B/S-C. Reader/grep were therefore used as the literal fallback; per the reviewer role, grep output here is **literal-text evidence only, not semantic proof** of caller/definition/diagnostic relations. No semantic caller or definition claim is made in this report.

**Read-surface gap (recorded, not improvised):** S-C names `source_path: .ufo/waves/round-23/sources/structured-edit-observations.json` (S-C:61) as the grounding source for all eight decisions, and S-B lists S085/S086 as *prospective* (S-B:117–120). That file, the r22 `measure/` artifacts, and `tools/` are **outside this seat's declared read paths**, so I did not open them. Every statement below about S086 content, about `tools/check-edit-contract.py`, `tools/check-seat-bindings.py`, `tools/check-path-reconciliation.py`, or about the r22 measure JSON is an **inference from declared prose**, marked `[INFERENCE]`. Nothing about unseen bytes is asserted as observed.

## 2. What the new v2 authority actually says (S-C, S-B)

S-C carries exactly eight decisions, each with `id`, `decision`, `reason`, `evidence: "S086"`, `policy: "round23-preregister"`, plus a `scope` line (S-C:62): *"Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof."*

Cross-check performed: the eight `(id, decision, reason)` triples in S-B:56–96 are **byte-identical** to the eight S-C decision objects on those three fields (DECLARED_EDIT/ALLOW, UNDECLARED_EDIT/DENY, READ_ONLY_EDIT/DENY, WRITE_ONLY_EDIT/DENY, OPAQUE_PATCH/UNKNOWN, EDIT_TRAVERSAL/DENY, EDIT_EXTERNAL/DENY, EXPANSION/CHECK_EACH). This is a genuine positive finding, and it is the only part of the v2 surface that is currently *consistently* duplicated. The duplication itself is a defect — see F5.

The four prospective-only anchors already present in S-B are correct in intent and are quoted verbatim below (S-B:34, 43, 52, 113):

- C1: *"Eight finite source-grounded structured-edit authority decisions; new document contract, not eight repaired runtime behaviors."*
- C2: *"New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."*
- C3: *"Both fixed r22 cohorts have exhaustive per-event/component explanation of rough-versus-lane path counts, frozen digests and declared arithmetic; does not relabel old violations or retry historic checks for confirmation."*
- limit: *"No historical manifest/report rewrite or retrospective authorization"*

My findings below are therefore **not** "the round violated its own prospectivity rule". They are: **the intent is stated, but three concrete HIGH gaps in the artifact leave the prospective-only property unenforced**, and each gap is the exact place where a retrospective clearance could occur undetected.

## 3. Findings by severity

### HIGH

**F1 — The v2 authority artifact carries no applicability epoch or record-generation gate, and its own schema id collides with the legacy id it claims to extend.**
S-C:2 declares `"schema": "tsukuroi-edit-policy-v1"`. S-B:43 says the new authority is *"schema-v2"* and that *"legacy schema-v1 policy and historical reds unchanged"*. The v1/v2 words in S-B:43 therefore refer to the **binding/manifest** schema, while S-C:2 uses `v1` for the **new policy document's own** schema id. Two different "v1"s now denote two different authorities in the same decision surface, and the new artifact carries no field (no `applies_to`, no `effective_from`, no `applies_to_event_generations`) that says which captured events it may be applied to. The only disambiguator is the per-row `"policy": "round23-preregister"` string (S-C:9, 16, 23, 30, 37, 44, 51, 58) — a prose label, not a dispatch key.
*Why it matters:* C2's own command is path-scoped to round-23 captures (`--manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`, S-B:42), which is a real structural protection — I credit it. But the *policy* is not, and the policy is what decides. A checker that resolves "which policy applies" by schema id, or that applies S-C to any captured event set it is handed, can route r22's captured events (`.ufo/waves/round-22/build/initial-events.json`, `native-outcomes.json`, and the preserved `seat-execution-requests.json` lineage cited at S-A:30) through the new decision table and produce **different verdicts than r22's own audit produced for the same records**. That is precisely "relabel old violations", forbidden by S-B:52 and by S-A:102's *"No receipt is rewritten to clear these."*
*Required fix:* add an explicit applicability field to S-C (e.g. `"applies_to_event_generations": ["round-23"]` / `"effective_from_revision": "ae01e50f..."`) **and** require the checker to refuse any event record lacking a matching v2 discriminator, rather than defaulting. `[INFERENCE]` — I could not read the checker to confirm a default exists; the requirement stands regardless.

**F2 — "No matching decision row" must never mean "permitted"; the eight rows cover edit authority only, and r22's exec-denied seats and the retained forbidden Bash expansion lie entirely outside them.**
The eight rows are all about *edit* targets. Bash is not an edit, so r22's two exec-denied seats — **OracleReceiptCRLF** and **DebtFetch** (S-A:100; S-A:56, 66) — and the *"known forbidden Bash expansion is retained for the auditor, not treated as clean"* (S-A:82) have **no** row in S-C. The same is true of the 33 unknown-tool and 52 path-denied findings (S-A:100) and the 13-Bash/nine-seat + six-fetch/two-seat historical debt (S-A:40).
*Why it matters:* a v2 verdict that reports "no applicable decision ⇒ permitted" for a non-edit event, or that reports a seat as "v2-clean" because no edit row matched, retroactively converts r22's red findings into apparent cleanliness. r22 already established the correct precedent for exactly this shape: *"malformed/unresolved/unavailable accounting cannot credit the mode"* and *"unreadable reports are explicitly unclassified, not falsely declared absent or delivered"* (S-A:74), and *"malformed/incomplete traces cannot clear a seat"* (S-A:10). A seat's v2-edit verdict must be reported as **edit-scoped only**, and every non-edit finding from r22 must survive as an independently visible red.
*Required fix:* state in S-C and in the C2 checker output that a non-edit event, or an event matching no row, yields `not-scoped`/`unclassified` — never `permitted` — and that the v2 result never clears a non-edit finding. The eight-row table must never be reported as a seat-level compliance verdict.

**F3 — `OPAQUE_PATCH = UNKNOWN` is a fail-open verdict value unless it is defined as non-crediting.**
S-C:33–38 declares the decision `UNKNOWN` for a missing structured target. `UNKNOWN` is not `DENY`, and r22's rule for structurally-undecidable inputs was **fail closed**: *"unknown argument keys fail closed and the collector preserves key presence without bodies"* (S-A:73), *"malformed/unresolved/unavailable accounting cannot credit the mode"* (S-A:74), and *"fail closed means at judgment time, not at call time"* (S-A:51). A checker that treats `UNKNOWN` as "not a denial, therefore fine", or that omits `UNKNOWN` from its finding set, turns an undecidable opaque patch into a silent pass — a new fail-open surface that did not exist in r22.
*Why it matters:* this is the one place where the new table can silently *add* permissiveness relative to r22's classifier, and it is the most likely place for an accidental retrospective softening of a r22 "unknown/unclassified" seat.
*Required fix:* define `UNKNOWN` explicitly as a **non-crediting, unresolved** outcome that (a) appears in the findings output, (b) cannot satisfy a "clean" or "permitted" aggregate, and (c) never contributes to an allowance count. If the intent was "deny", the value must be `DENY`, not `UNKNOWN`; the two are not interchangeable under r22's fail-closed rule.

### MEDIUM

**F4 — `EXPANSION = CHECK_EACH` is a procedure, not a verdict, and its aggregation rule is undefined; "eight validated decisions" therefore counts a non-decision.**
S-C:54–58 and S-B:92–96 set the eighth decision to `CHECK_EACH` with reason *"Every recorded adapter read or write remains separately scoped"*, while the other seven rows carry verdicts. Two defects follow. (i) **No aggregate rule:** if one expansion contains one allowed member and one denied member, what is the expansion's result? "Check each" prescribes procedure, not outcome, so the outcome vocabulary for a split expansion is undefined — and an undefined aggregate defaults, in practice, to the permissive member. (ii) **Metric category error:** C1's metric is `validated_edit_decisions` before 0 → target 8 (S-B:30–32) and C1's scope calls them *"Eight finite source-grounded structured-edit authority decisions"* (S-B:34) — but only seven are decisions; the eighth is a scoping rule. So "8 validated decisions" is satisfiable by counting a rule as a decision.
*Why it matters:* r22's C1 counterexample is exactly this class — the candidate's own fixture accepted a DEAD-policy oracle edit that an independent literal fixture killed (S-A:34, S-A:104). An under-specified aggregation rule is the same shape of hole.
*Required fix:* give the expansion a defined per-member verdict and a defined aggregate (e.g. any denied member ⇒ expansion denied; report the member list); and either restate C1's metric as counting seven verdicts plus one scoping rule, or define the eighth row's verdict vocabulary so eight verdicts genuinely exist.

**F5 — Two copies of the eight decisions in two different shapes, with no declared canonical source or field-projection rule.**
S-B:56–96 stores eight 3-tuples `(id, decision, reason)`. S-C:3–60 stores eight objects with five fields (`id`, `decision`, `reason`, `evidence`, `policy`). The three overlapping fields agree today, but the two copies are not byte-comparable and nothing declares which is canonical. A drift in `evidence` or `policy` — the two fields that carry the round binding and the source pointer — is **invisible** to any 3-field comparison, and the 3-tuple form cannot express a source pointer at all.
*Why it matters:* r22's own registry defect (R22-REGISTRY-LITERAL) was exactly a stale literal in a duplicated row that had to be restored byte-exactly, with the original red measurement retained (S-A:38, S-A:88, S-A:106). Duplicated decision tables without a canonical owner are how that recurs.
*Required fix:* declare one canonical artifact for the eight decisions (S-C is the better candidate, being the machine-facing one), derive S-B's tuples from it, and have `tools/check-edit-contract.py` compare **all five fields per row plus the exact row set and row count**, failing on any extra/missing/duplicate id — the visible-column and exact-tuple discipline r22 already applies to its tables (S-A:53).

**F6 — Source-grounding of all eight decisions rests on one undifferentiated pointer (`S086`) into a source that is still declared *prospective*.**
Every S-C row carries `"evidence": "S086"` (S-C:8, 15, 22, 29, 36, 43, 50, 57) with no per-row source cell, quote or locator, and S-B:117–120 lists S085/S086 as *"prospective"*. S-B:34 nevertheless claims *"Eight finite **source-grounded** structured-edit authority decisions"*.
*Why it matters:* r22's registry standard gives each source row a URI, an access date and a located quote of at most 25 words, and requires the census to close with mined/queued/rejected counts and `validate 0` (S-A:21–24, S-A:106). A uniform pointer to a not-yet-opened source cannot distinguish eight independently grounded rows from one self-referential pair (policy asserts S086; S086 may be derived from the same observations the policy claims to ground). r22's oracle lesson applies directly: many oracles read the policy/host decision rather than executable schema and are therefore *"independent expected controls, not implementation verification"* (S-A:54).
*Required fix:* bind each of the eight rows to a distinct source locator/quote, and close the source census (rows added, mined/queued/rejected counts, `validate 0`) before the C1 target of 8 is claimed. `[INFERENCE]` — I could not read `structured-edit-observations.json` or the census to see whether per-row locators exist there already; if they do, they are simply not referenced from S-C.

**F7 — `ALLOW`/`DENY` wording must never be reported as runtime enforcement; the authority is judgment-time only.**
S-C:62 correctly disclaims *"no native prevention"* and S-B:111–112 disclaims *"No native per-seat restrictive tool interface exists"* and *"No runtime prevention, effect/reading/recorder-completeness or universal tool/patch semantics"*. This matches r22's settled position: *"fail closed means at judgment time, not at call time. Native tools remain exposed; no wrapper could prevent bypass"* (S-A:51); *"Actual adapter/host runtime enforcement remains kumitate/operator territory"* (S-A:84); *"no native prevention exists"* (S-A:95); the r21 native-toolset question *"remains kumitate/operator work; Main confirms no such restrictive interface is exposed"* (S-A:108). `[INFERENCE]` The risk is in reporting, not in S-C: the verdict vocabulary `ALLOW`/`DENY` reads like a permission system, and a final summary that says "edits allowed" without the audit-time qualifier would repeat the R22-ENFORCEMENT-LIMIT overclaim that r22 explicitly had to guard against (S-A:33).
*Required fix:* in the C1/C2 result rendering, qualify every verdict as an audit-time judgment over declared bindings, and never as runtime enforcement, prevention, permission or effect.

**F8 — C3 must explain the rough-versus-lane path-count *unit* difference without relabeling r22's path-denied findings, and must read frozen r22 evidence rather than re-running historic checks.**
S-B:14–22 admits the outside r22 counts as ground truth: rough build **25** / falsify **33**, lane build **23** / falsify **29** (outside verifier `CloseKaidoku22`, commit `4482c275f9381f219ee4d092e0324d417c3cb1e7`, S-B:7–8). The two cohort deltas are therefore **2 (build)** and **4 (falsify)**, and C3's `unexplained_cohorts` 2 → 0 (S-B:48–50) requires **both** cohorts to be explained, not one.
*Why it matters:* two distinct failure modes are available. (i) Explaining the deltas by **reclassifying which paths count** would change r22's 52 path-denied findings and the 43 distinct seats (S-A:100) — forbidden by S-B:52 and by S-A:102 (*"No receipt is rewritten to clear these"*). (ii) Explaining them by **re-running the r22 audits** to reproduce fresh numbers is forbidden by S-B:52's *"or retry historic checks for confirmation"* and by S-B:24's *"r23 explains classifier/unit differences rather than rerunning closure merely to confirm them"*. The admissible route is a per-event/component decomposition of the *counting unit* difference, over frozen r22 evidence (S-A:88's measured code `f39e40a4adad5bf02bd9ddcfb2473b93b139595a`, `measure/finalr22/results.json`, `measure/round-summary.json`), with the 87 findings / 43 seats / 33+52+2 split / 121 files / 113 strict-conformant / 7 absent-dead / 0 unresolved (S-A:96, 100) held **invariant** in the output.
*Required fix:* state the counting unit of each of the four numbers explicitly, give the 2 and the 4 as separate component decompositions, and assert the r22 finding inventory unchanged as an invariant of the reconciliation output. `[INFERENCE]` — I could not read `tools/check-path-reconciliation.py` or the frozen measure JSON to see whether it reads frozen evidence or re-runs r22 checks.

### LOW

**F9 — Ordinal semantics must be stated so that "depth = 8" is not read as an ordinal uplift.**
S-B:98–105 keeps ordinals at depth 8 / adjacency 8 / coverage 9 / operability 9 / freshness 9 / calibration 9 with `"ordinal_delta": 0` (S-B:106) and `"retired": []` (S-B:107), while C1/C2/C3 move metrics on the depth / operability / calibration axes (S-B:28–52). The numeric collision between the depth ordinal `8` (S-B:99) and C1's target `8` (S-B:32) is a reader trap. r22's precedent is explicit that untouched ordinals are *"inherited, not newly measured/no-harm certified"* (S-A:52) and that a round ended with *"No source frontier graduation, new repertoire row or ordinal uplift"* (S-A:106). *Fix:* state in the results that axis-metric movement does not uplift the axis ordinal and that `ordinal_delta: 0` is deliberate.

**F10 — The new r23 checker needs independent literal negative fixtures, not self-generated ones.**
S-B:33 introduces `tools/check-edit-contract.py`. r22's binding precedent (R22-ORACLE-LOCKSTEP, S-A:34) is that *"Independent literal fixture kills the DEAD-policy oracle edit that the candidate's self-generated fixture accepts; in-memory oracle is restored"*, and S-A:72 records the fix *"exact independent literal selftest inputs no longer derive from the evaluator map"*. *Fix:* the r23 checker's negative fixtures must be independent literals, and the eight-row copy comparison (F5) must not be derived from the same map it validates.

## 4. Exact historical evidence that cannot be cleared by the new v2 permissions

This is the requested inventory. Every row below is historical r22/r21 evidence whose clearance would require rewriting an original report, manifest, settlement record or measurement — all explicitly ruled out by S-B:113 and S-A:14 (*"Original reports/manifests stay immutable; no denominator repair by dropping seats"*), S-A:102 and S-A:40. **None of it may be cleared by DECLARED_EDIT=ALLOW, by a v2-clean seat verdict, or by the C1/C2/C3 metrics turning green.**

**Layer A — the two named `executed=none` scope-trailer absence assertions (self-contradicted, superseded by named correction, report NOT rewritten)**

| Seat | Exact historical evidence | Where | Why the v2 authority cannot clear it |
|---|---|---|---|
| **OracleReceiptCRLF** | Report literally reproduces an `executed=none` scope trailer while disclosing that it ran `sha256sum` and `wc -l` despite NO-EXEC; *"That absence assertion is superseded by this named correction, not by rewriting its report"* | S-A:56; also S-A:100 | The supersession is of the **assertion**, not of the **violation**. The violation is a recorded native Bash start; the original report bytes still carry the false trailer. A v2 edit-authority verdict covers neither the trailer nor the start. |
| **DebtFetch** | Disclosed `wc -l` request *"independently contradicts its required none trailer; this named correction supersedes the absence assertion without rewriting the report"*; its inferred arithmetic about six fetches versus source-row counts is *"not admitted"* | S-A:66 | Same. The six fetch calls / two seats are ground truth from the steer (S-A:31), not a count derivable from source rows (S-A:66) — so a v2 source-derived count cannot discharge it. |

**Layer B — r22's own measured scope findings (two disjoint waves, 43 distinct seats, 1373 records)**

| Evidence | Exact figure | Where | Clearance bar |
|---|---|---|---|
| Total auditable records | **1373** (1338 primary requests + 35 additional adapter starts) | S-A:100 | Primary and adapter starts are counted separately and *"neither is advertised as a unique-effects count"* (S-A:100, S-A:84). A v2 `EXPANSION=CHECK_EACH` re-scoping must not merge or drop the 35. |
| Findings / seats | **87 findings across 43 distinct seats**; **33 unknown-tool, 52 path-denied, 2 exec-denied** | S-A:100 | The v2 table has no row for unknown-tool, path-denied (non-edit) or exec-denied events → F2. These must remain visible as r22 reds. |
| Known EXEC requests | **OracleReceiptCRLF, DebtFetch** | S-A:100 | As Layer A. |
| FETCH-DENIED | **Zero** findings carry FETCH-DENIED, and *"unknown tools/path denials and limited start summaries are not transformed into a universal no-fetch/effects certificate"* | S-A:100 | Absence of fetch findings is **not** a no-fetch certificate; v2 must not be read as supplying one. |
| Per-wave scope gates | Both scope gates **exit 1** with 41/46 findings; strict exits 1 remain | S-A:93 (C2 row), 94 (C3 row) | Green r23 metrics cannot erase r22's exit-1 gates. |

**Layer C — r22 receipt-conformance findings (immutable by name)**

| Class | Exact names | Where |
|---|---|---|
| Faulty build receipts (3) | **OracleTraceEmpty, OracleReceiptPeriod, OracleReceiptDuplicate** (strict digest / predicate / scope-declaration findings) | S-A:102 |
| Faulty falsify receipts (5) | **FxC1NoExec, FxC1Table, FxC2Wildcard** (same three), **FxC2ParallelExec** (predicate), **FxC2TraceMissing** (digest) | S-A:102 |
| Cohort totals | **8 faulty reports remain immutable; 113 strict-conformant / 121 files; 7 absent-dead; 0 unresolved** | S-A:96 |
| Separation rule | *"Scope conformance and strict receipt identity are separate, so a clean receipt never clears an observed unauthorized request"* | S-A:102 |

**Layer D — the two adapter/expansion facts the v2 `EXPANSION` row must not touch**

| Evidence | Exact statement | Where | Why it cannot be cleared |
|---|---|---|---|
| Adapter expansion | *"one reported `edit` emits native report-read and report-write starts under the same parent call ID. Those are not silently dropped or retrospectively authorized"* | S-A:82 | The expanded native starts are separate auditable events. A v2 `ALLOW` for the **parent** edit must not inherit down to the expanded native write, and must not erase the parent-call-id identity r22 preserved (same-identity rerouting). |
| Forbidden Bash expansion | *"A known forbidden Bash expansion is retained for the auditor, not treated as clean"* | S-A:82 | Bash is outside all eight rows → F2. Retention is the recorded state. |

**Layer E — superseded-but-retained r22 artifacts (superseded ≠ cleared)**

| Evidence | Where | Note |
|---|---|---|
| Interim projection **55 complete / 64, 16 failed** on 9 Swe critic traces — *"superseded, not actual task/provider failures"*; red-before projection preserved in `build/initial-events.json` and `initial-settlement.json` | S-A:62 | The original bytes are the historical record and must not be deleted by the r23 collector work. |
| Registry literal first red; exact frozen row restored, checker unchanged; earlier results *"carried with their original measured hash, not relabelled"* (`f39e40a4…` final, `cb3ba8a6…` repair-r22 only, 174 claim inputs/evaluators byte-identical) | S-A:38, 88, 106 | r23 must carry r22 results at their original digests; re-labelling under an r23 revision is prohibited by S-B:113. |
| Source census **82 → 84** rows (A74→76 / B1 / C7), mined 68→70 / queued 5 / rejected 9, all old 82 rows unchanged, new S083/S084 only, initial/end `validate 0`, 9 unchanged URL warnings | S-A:106 | S085/S086 must be **additive**; editing S083/S084 or any older row is prohibited. |
| r21 recurrence row S083: *"Two provider-dead seats with no report still have recorded Bash starts"* | S-A:21 | A dead provider and an absent report are not evidence of cleanliness. |
| r22 gate rejections that remain rejections | S-A:13–15 | *"Green receipt or dead provider implies no earlier command/fetch" → reject*; *"Rewrite six historical receipt faults or replace failed seats" → reject*; *"Complete accounting means all receipts conform or no harm" → reject*. |
| r22 gate rejections on capability | S-A:95, 97, 98 | *"All current seats obeyed the prompt → reject"*; *"Runtime enforcement, reading, request effects … → reject"*; *"Self-admission / outside promotion tick → reject"*. v23 inherits these debts; it does not discharge them. |
| Failed/absent seats | 3 code executors + SentinelMetadata failed at Codex capacity; ScribeBoundary failed Anthropic 429; *"They are not replaced … their missing reports remain missing"* (S-A:50); 7 absent-dead in the cohort (S-A:96) | S-A:50, 96 | Missing reports cannot be manufactured by a v2 verdict; absent is not clean. |
| r22 falsify findings' evidentiary standing | *"Fresh64-seat falsify completed without replacing any seat. All findings are source-only expectations, not empirically killed mutants"*; *"the immutable candidate snapshots and original reports remain unchanged"* | S-A:70 | r23 may not promote source-only expectations to empirically killed mutants, nor mutate the immutable candidate snapshots. |
| r22 self-graded limits that r23 inherits | outside closure still owed (S-A:98); no-harm/admission not self-granted (S-A:108) | — | r23 is not an admission tick either. |

## 5. Residual risk and verification gaps

**Residual risk (cannot be closed inside this seat's read surface):**

1. **F1/F2 remain the live retroactive-clearance path.** Both require either a code change in the r23 checker or an explicit applicability clause in S-C. Until one of those exists, "prospective-only" is a prose property of S-B, not an enforced property of the artifact.
2. **F3 is the only place the new table can be *more* permissive than r22's classifier.** `UNKNOWN` must be non-crediting or the table has introduced a fail-open surface that r22's fail-closed discipline (S-A:51, 73, 74) never had.
3. **F4's undefined expansion aggregate** is the most likely place a split expansion resolves permissively.
4. **S-B's `sources_opened` lists S085/S086 as prospective** (S-B:117–120), while S-C already cites S086 as the evidence for all eight decisions and S-B:34 already claims they are source-grounded. If the census is not closed before the C1 target is claimed, the C1 metric can be green on ungrounded rows.
5. **No native enforcement exists** (S-B:111; S-A:51, 95, 108). Every v2 verdict is a judgment-time audit over declared bindings; reporting it otherwise re-opens R22-ENFORCEMENT-LIMIT.

**Verification gaps (things I could not do, stated plainly):**

- I did **not** open `structured-edit-observations.json` (S-C:61) — outside my declared read paths — so I cannot confirm whether per-row source locators/quotes for S086 exist, nor whether that file is independent of S-C or derived from it. F6 is therefore a *binding/traceability* finding, not a claim that the grounding is absent. `[INFERENCE]`
- I did **not** read `tools/check-edit-contract.py`, `tools/check-seat-bindings.py` or `tools/check-path-reconciliation.py`, so I cannot confirm whether the checkers read frozen r22 evidence or re-run historic checks (F8), whether they default schema-less events to v2 (F1), or whether their negative fixtures are independent literals (F10). These are requests for the owning executor/L1, not assertions.
- I did **not** read the r22 `measure/` artifacts (`results.json`, `round-summary.json`, `native-outcomes.json`) or `build/initial-events.json`; all r22 figures above are quoted from the frozen lesson file S-A, which is the declared and digested surface.
- **No LSP/diagnostics check was possible** (xd route space forbidden by the seat contract; no `lsp` device reachable). Reader/grep were the literal fallback and are presented as such.
- The r22 digest is the **supplied declaration**; no hash, `wc`, or any command was run to recompute it, and no fetch of any kind was performed.
- The r23 wave directories referenced by S-B:42 (`<WAVE>/bindings.json`, `<WAVE>/events.json`) do not yet exist in my surface; F1's applicability-gate finding applies to whatever is landed there.

## 6. Bottom line

The v2 structured-edit authority is a **new document contract**, honestly scoped at judgment time, and it does **not** by itself reach back into r22: S-B:34/43/52/113 state the prospective-only rule correctly, S-C:62 disclaims prevention, and the eight decision rows agree field-for-field between S-B and S-C. What is missing is enforcement of the property, not the intent: **no applicability epoch in the authority artifact (F1), no "no matching row ⇒ not permitted" rule for the non-edit events that carry every r22 red (F2), and one newly fail-open verdict value (`UNKNOWN`, F3).** With F1–F3 closed and F4–F8 made explicit, the eight decisions are safe to land as a prospective instrument.

The historical evidence listed in §4 — the two self-contradicted `executed=none` scope trailers of **OracleReceiptCRLF** and **DebtFetch**, the 1373-record / 87-finding / 43-seat scope inventory with its 33 unknown-tool / 52 path-denied / 2 exec-denied split, the eight named faulty receipts, the retained forbidden Bash expansion and the parent-call-id adapter expansion, the 7 absent-dead seats, the superseded 55/16 interim projection, the carried r21 provider-dead-with-recorded-starts row, and the r22 gate rejections — **cannot be cleared by the new v2 permissions**, and no r23 metric turning green may be reported as having cleared any of it.

Reviewed-SHA256: 2fd1a5bca6633a0ede1de5efc4d0ff5504bb3bc9f3676dbee11addb8c53376f5
Predicate: r23-reviewpolicy83
Scope: executed=none
