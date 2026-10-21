# SourceFrontier23 — held-ground instrument improvement vs frontier/repertoire acquisition

**Seat:** SourceFrontier23, round 23 attempt 1 · **Baseline:** `ae01e50f582016384e620022be38bf5367000e2e`
**Execution class:** `NO-EXEC` / `NO-FETCH`. No command, hash, list, `wc`, import, subprocess, fetch, URL read or child task was run.

**Sources actually read (three declared files plus the skill):**
`../snapshot/corpus/QUALITY.md`, `../preregister.json`, `../sources/r22-closure.json`, `skill://godspeed`.
The corpus digest `0141ba62…f30f959` is the supplied declaration; it was not independently computed or validated by any command (§10).

**LSP note:** no code symbol is under analysis here; the objects are a JSON preregister, a JSON closure record and a Markdown quality corpus. No language server was bound in the declared scope and none applies to these data files, so grep was used only as an index; every proposition below is carried by an exact located quote or JSON key, never by grep output as proof.

---

## 1. Axes named (godspeed step 1)

| Axis | Where it is declared | r22 value |
|---|---|---|
| depth | `r22-closure.json` → `verdicts.depth` | improved |
| operability | `verdicts.operability` | improved |
| calibration | `verdicts.calibration` | improved |
| coverage | `verdicts.coverage` | unchanged |
| freshness | `verdicts.freshness` | unchanged |
| adjacency | `verdicts.adjacency` | unchanged |
| expansion (trend) | `trends.expansion` | unchanged |
| quality (trend) | `trends.quality` | unchanged |
| discernment (trend) | `trends.discernment` | improved |

r23 claims bind three of these axes to three instruments: C1 → depth, C2 → operability, C3 → calibration (`preregister.json` → `claims[].axis`). The assignment's vocabulary "frontier/repertoire acquisition" is not a term published in any of the three declared documents; the mapping used below (§3) is labeled inference, and only `expansion`, `quality`, `discernment` are source-named trend axes.

## 2. Observed facts (measurements, not interpretation)

### 2.1 The trend vector is self-separating
`r22-closure.json` → `trends` records `{"expansion": "unchanged", "quality": "unchanged", "discernment": "improved"}` while `verdicts` records three improved axes and three unchanged axes. The same record carries `capabilities_added: []`, `promotions: []`, `minted: []`.

**Observed:** a round can improve depth, operability and calibration and still hold expansion and quality flat. The axes are not coupled in this record; instrument work did not propagate into the two acquisition-sensitive trends.

### 2.2 The admission framing refuses an enforcement reading
`r22-closure.json` → `notes`: "ADMITTED for three bounded instruments, not enforcement." and "it never prevents calls and its red exits are the retained conformance result."

**Observed:** the admitted objects are detection/accounting instruments; their red outputs are the conformance *finding* and are retained, not superseded by a later green.

### 2.3 The instruments operated on ground already enumerated
- C1: "Eight finite source-grounded structured-edit authority decisions; new document contract, not eight repaired runtime behaviors." (`preregister.json` → `claims[0].scope`)
- C2: "legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim." (`claims[1].scope`); `limits` adds "No native per-seat restrictive tool interface exists".
- C3: "does not relabel old violations or retry historic checks for confirmation" (`claims[2].scope`), over "Both fixed r22 cohorts" — i.e. a frozen population.

**Observed:** C2's target class is "exact predeclared structured edit targets", a class already exercised by the round-22 seats; C3's denominator is the frozen round-22 census. Neither names a target class first reached in r23.

### 2.4 Quality moved independently of row bookkeeping
`r22-closure.json` → `verification.rechecks`: "SOURCES82->84 all old rows present, A74->76/B1/C7, mined68->70/queued5/rejected9". The same record's `trends.quality` is `unchanged`, and `notes` states: "Quality trend unchanged: in-round gate hardening and registry repair concern new material; no prior entry superseded or re-verified."

**Observed counterexample to two tempting hypotheses:** neither more source rows (82→84), more mined entries (68→70), nor new gates moved the quality trend. The one stated correlate of the flat value is the absence of a supersession or re-verification of a prior entry.

### 2.5 No-harm was evidenced separately
`r22-closure.json` → `verification.rechecks`: "zero deleted lines B->H, no prior file removed, LOG/SCORECARD/SKILL/QUALITY/README prefix-preserving, PROVINCE unchanged, no axis score row changed".

**Observed:** "unchanged" on six axes is not itself the no-harm proof; the proof is this separate preservation record. The two are different evidence classes.

### 2.6 The eight C1 rows are policy verdicts, not runtime behaviors
`preregister.json` → `edit_decisions` holds exactly eight typed rows: `DECLARED_EDIT/ALLOW`, `UNDECLARED_EDIT/DENY`, `READ_ONLY_EDIT/DENY`, `WRITE_ONLY_EDIT/DENY`, `OPAQUE_PATCH/UNKNOWN`, `EDIT_TRAVERSAL/DENY`, `EDIT_EXTERNAL/DENY`, `EXPANSION/CHECK_EACH` — one ALLOW, five DENY, one UNKNOWN, one per-target recheck.

`QUALITY.md` item 43 states the grading rule: "A source-grounded decision table is depth evidence, not execution evidence".

## 3. Decision rule (inference, explicitly not a source claim)

I separate two kinds of move. The definitions are mine; the tests are chosen so each is falsifiable against the declared records.

**Held ground** — the finite set of objects already enumerated by landed evidence: the declared seat population, the receipt/request records, the source-row list, the path-census cohorts, the registry rows, the admitted knowledge entries. Membership is checkable by naming the row.

**Move H — held-ground instrument improvement.** The move changes detection, classification, accounting or repair *within* that set:
- H1: every target the instrument reads is a row already present in a prior landed enumeration;
- H2: no new action capability appears — the lane could not do anything after the move that it could not do before;
- H3: the metric's "before" value was measurable over the same object set;
- H4: old failures/reds are retained as findings, not cleared by the new instrument.

**Move F — frontier acquisition (domain growth).** A new object class enters the enumerated ground:
- F1: at least one named target row has no predecessor in any prior enumeration;
- F2: the denominator (count of enumerated classes) grows and the new members are listed, not merely counted;
- F3: a discriminating fixture shows the prior instrument failing or returning absent on the new class while succeeding on the old class;
- F4: the new class is admitted through the normal source/registry route (a prospective source row is not yet possession).

**Move R — repertoire acquisition (action growth).** A new reusable action capability enters the lane's repertoire:
- R1: a tool/route/skill is admitted with its own scope and selftests;
- R2: the capability alters what the lane can *do* (not only what it can *detect*);
- R3: governance records the acquisition (`capabilities_added` non-empty, and/or `capability_acquisition` true, and/or `promotions`/`minted` where a capability is claimed);
- R4: R2 is not inferred from prompt text or from a detector's existence — `QUALITY.md` item 47: "task `tools` is additive in the current host API, not a native allowlist".

**Coupling rule (inference):** expansion trend movement requires F; capability acquisition requires R. Instrument novelty alone satisfies neither. H is admissible on its own axis, and may improve discernment without moving expansion or quality.

## 4. Classification of the round-22 moves

| Observed move | Declared axis | Class | Discriminating fact |
|---|---|---|---|
| C1 edit contract, 8 typed rows | depth | H (policy/document instrument) | "new document contract, not eight repaired runtime behaviors"; QUALITY 43 grades decision tables as depth evidence |
| C2 schema-v2 edit-target audit authority | operability | H (audit instrument) | "legacy schema-v1 policy and historical reds unchanged"; "never prevents calls" |
| C3 path-census reconciliation | calibration | H (accounting instrument) | frozen r22 cohorts; "does not relabel old violations or retry historic checks for confirmation" |
| SOURCES 82→84, mined 68→70, A74→76 | — | bookkeeping addition, not a trend move | `trends.quality` stayed `unchanged`; no supersession/re-verification stated |
| Gate hardening and registry repair | — | new-material work | `notes`: "concern new material; no prior entry superseded or re-verified" |
| Three admitted instruments | depth/operability/calibration | not frontier, not repertoire | `capabilities_added: []`; detection ≠ action |

**Result (observed + rule):** round 22 is entirely class H. It is genuine instrument improvement — the instruments are fail-capable and their red exits were retained — but it is not frontier or repertoire acquisition. The trend vector is consistent with that classification rather than merely compatible with it: the two acquisition-sensitive trends did not move while the three instrument axes did.

**Round-23 inheritance:** `preregister.json` declares `capability_acquisition: false` and `exploratory: false` for r23, and its `limits` repeat "No native per-seat restrictive tool interface exists". C1/C2/C3 in r23 are therefore instrument contracts over held ground by their own declared scope; nothing in the preregister claims a new domain or a new action. Applying the r22 evidence to r23 is a scope error — the r22 `capabilities_added: []` is the r22 fact, not a prediction about r23.

## 5. Exact prerequisites for an expansion claim

An expansion claim is admissible only when all of the following are present in the record:

- **E1 — Named new members.** The new target class is enumerated by identity (path/row/selector), not by count alone. A delta such as `82->84` is insufficient: `r22-closure.json` shows exactly such a delta with `expansion: unchanged`.
- **E2 — Denominator accounting.** A declared before/after cardinality for the domain set, with the new rows listed and the old rows shown still present (QUALITY item 23: "Preserve prior notices and append a named citation-only erratum"; item 40: "a finite original-nine count must not silently gain post-outcome rows").
- **E3 — Structural-zero baseline.** The "before" value must be impossible or unmeasured-by-construction over the old ground, not merely observed as zero. A zero that existed because the instrument was absent is not evidence the domain was absent.
- **E4 — Discriminating fixture pair.** One control where the prior instrument fails or reports absent on the new class, and one where it succeeds on the old class. A single passing new class does not exclude a relabeling of old ground.
- **E5 — Admission of the new source/repertoire row.** Prospective rows (`preregister.json` → `sources_opened`: "S085 prospective", "S086 prospective") are intent, not possession; they must be admitted and cited with a located quote before they support expansion.
- **E6 — Separability.** The new claim must be separable from the instrument claims, as `preregister.json` → `separability` requires ("never new C1/C2 production content"). If the same evidence could equally be read as a repaired instrument, the expansion reading is not established.
- **E7 — Governance flags consistent.** `capabilities_added` non-empty and/or `capability_acquisition: true` for repertoire; `promotions`/`minted` when a capability is claimed. Empty lists plus an expansion claim is a contradiction on the record's face.
- **E8 — Enforcement limit preserved.** A detector that classifies requests is not an action capability: QUALITY item 47 and the preregister `limits` both forbid reading prompt scope as runtime prevention.

## 6. Exact prerequisites for a quality claim

Quality is about prior propositions, not new material. A quality movement requires:

- **Q1 — Identified prior object.** A named admitted entry and the exact proposition at issue. New gates, new reports and registry repairs do not qualify: the r22 `notes` sentence is the precedent.
- **Q2 — Located quote and proposition scope.** QUALITY item 19: "name the source object, its located ≤25-word quote and the exact proposition it supports"; no transfer of a disclaimer across objects, no option domain inflated into a mechanism set (items 19, 22).
- **Q3 — Portable locator.** Heading/fragment, exact quote and observed revision or access date (item 21); line ranges are supplemental and withdrawable (items 21, 23, 30). In this corpus the stable locator is the numbered criterion or the JSON key path, which is what this report uses.
- **Q4 — Append-only correction.** "Errata are append-only blocks" (item 4); the rejected historical record stays, with a named erratum (item 23). In-place refresh of historical observations is not a quality move.
- **Q5 — Independent expected outcome.** Expected outputs derived before candidate outputs and not from the module under judgment (items 36, 41); the measuring judge stays independent (item 28: "Keep the measuring judge independent of that module").
- **Q6 — Fail-capable fixtures.** The correction check must reject both the preserved prior defect and restored-defect cases (items 19, 43, 45). A structural count does not establish source agreement (item 19).
- **Q7 — Byte/predicate binding.** "persist the primary reviewed file bytes, SHA-256 and exact predicate before dispatch" (item 42); "Mutable worktree paths are not version identities" (item 38). A quality verdict without a bound snapshot is could-not-evaluate, not improved.
- **Q8 — Superseded-text sweep.** Before a correction lands, sweep README/SKILL/knowledge for superseded mentions and verify table column counts (item 10); knowledge entries carry `source:`, `verified-at:`, `recheck:` (item 8), with no package-manager invocation in `recheck:` (item 26).

**Consequence:** r22's quality value is `unchanged` and correctly so under Q1+Q4 — the round added material and repaired gates but, by its own `notes`, superseded and re-verified nothing prior. Adding two source rows satisfies none of Q1–Q7.

## 7. Exact prerequisites for a discernment claim

Discernment is the ability to classify the held ground correctly and to keep the classification honest. A discernment movement requires:

- **D1 — Exhaustive declared partition.** QUALITY item 48: "fixed declared seats partition into receipt-well-formed, receipt-faulty, absent-observed-failure and absent-unresolved"; every bucket is reported. An unaccounted seat is not a zero.
- **D2 — Absence is observed, not assumed.** Missing reports and malformed receipts stay visible and non-clean (item 44: "Missing reports and period-appended `none.` stay non-clean under the original scope gate"); a dead seat needs an observed provider outcome, never a placeholder (item 48).
- **D3 — Could-not-evaluate distinct from zero.** "The machine key `delivered_conformant` means only receipt-well-formed, never request-scope conformance" (item 48); missing or unparseable trace data is could-not-evaluate.
- **D4 — Independent oracle.** Expected classifications are derived independently of the classifier under test (items 28, 36, 41). A second copy of the same algorithm is not an oracle for untested classes (item 41).
- **D5 — Reds retained.** Detection is the result (item 47's fail-closed rule; r22 `notes`: "its red exits are the retained conformance result"). Cleaning a red by re-grading it is a calibration regression, not improvement.
- **D6 — Frozen prior metrics preserved.** Prior counts keep their original scope; supplementary rows are counted separately (items 40, 43). No post-outcome rows enter an original count.
- **D7 — Explanation, not confirmation rerun.** The declared scope is explanatory: `preregister.json` → `outside_round22.scope`: "Given outside observations are ground truth; r23 explains classifier/unit differences rather than rerunning closure merely to confirm them."
- **D8 — Fail-capable classifier.** The classifier's finite schema must reject wrong outcomes (item 43: "its finite schema must reject wrong type outcomes"); a declaration audit stays separate from runtime scope (item 46: "a literal `Scope: executed=none` never overrides an observed Bash/eval/child invocation"; item 48).

**Consequence:** r22's discernment value is `improved` and is supported by D1+D5 in the record — every seat classified with strict faults kept visible, and the red conformance exits retained. That improvement is classification of the same cohort; it does not transfer to coverage or expansion.

## 8. Non-evidence and category errors (what must not be counted)

1. **Token collision.** `EXPANSION` in `edit_decisions[7]` is a per-target recheck verdict (`CHECK_EACH`) for adapter scoping, not the trend axis `trends.expansion`. A grep-based reconciliation that counts this token as expansion evidence is a unit error.
2. **Instrument novelty as acquisition.** Three new/hardened instruments coexisted with `capabilities_added: []` and `expansion: unchanged`; instrument count is not a domain count.
3. **Detection as enforcement.** A red gate exit is the conformance finding; it is not prevention (`notes`; QUALITY 47; `limits`).
4. **Row increments as quality.** SOURCES/mined/registry increments did not move quality in the same record.
5. **Erasure as repair.** Clearing old reds would not be a quality move (Q4) nor a discernment move (D5).
6. **Decision-table depth as execution.** Eight policy rows are depth evidence, not eight verified runtime behaviors (C1 scope; QUALITY 43).
7. **"unchanged" as harm-free.** No-harm is a separate evidence set (§2.5); equality on a score is not proof that nothing was lost.
8. **Prospective source rows as possessed sources.** S085/S086 are declared prospective; they are not yet citable evidence.
9. **Axis borrowing.** r22's `capabilities_added: []` cannot be reused as an r23 claim; the r23 preregister independently sets `capability_acquisition: false`.

## 9. Falsifiers for this report's rule

- **F-a (instrument → expansion).** Produce a move whose instrument target list contains a row with no predecessor in prior enumerations and a fixture where the prior instrument is absent on that class; then §4's classification of that move flips to F, and my rule fails.
- **F-b (quality without supersession).** Produce a closure with `trends.quality: improved` and no named superseded or re-verified prior proposition; then Q1/Q4 fail as necessary conditions.
- **F-c (discernment without partition).** Produce a closure with `trends.discernment: improved` and an unaccounted declared seat; then D1 fails.
- **F-d (expansion by bookkeeping).** Show a closure where row increments alone coincide with `trends.expansion: improved` and no new domain members; then E1/E2 are too strong.
- **F-e (detection as repertoire).** Show a `capabilities_added` entry that is a pure detector with no new action; then R2's separation fails.
- **F-f (no-harm reverse).** Show a round with improved instrument axes and a deleted prior file or removed old row; then §2.5's separation would not hold for that round.

## 10. Unknowns, bounded scope, and residual gaps

- **U1 — Trend predicates unpublished.** None of the three declared files defines the expansion/quality/discernment predicate; they publish only values. The thresholds and the exact scoring rule are unknown to this seat. Everything in §3–§7 is therefore a *decision rule*, not a restatement of a published rubric; it is marked inference and is falsifiable (§9). This is the report's principal limitation.
- **U2 — r22 report not read.** The lane report `.ufo/reports/round-22/tsukuroi.md` (named in `r22-closure.json` → `report`) is outside the declared read set. I cannot say whether its prose claimed expansion; I can only report the closure's trend fields and notes.
- **U3 — Row admission intent.** Whether S083/S084 were intended as quality movement is unknown; the observed trend is flat. The closure records admission of S084 in `verification.spotcheck` ("Admit S084: agree") without a quality movement.
- **U4 — Negative claims bounded.** Per QUALITY item 9 ("Every negative claim includes its bounded search/probe sweep command, scope and date"): the sweeps behind §2, §4 and §8 were reads/greps restricted to the three declared files and `skill://godspeed`, dated 2026-10-21, with commands deliberately not run under this seat's `NO-EXEC` binding. "Not present" always means "not present in these four declared sources", never a lane-wide absence.
- **U5 — No execution evidence.** This report contains no measurement of any checker. All checker behavior is quoted from the closure's verification record; I did not reproduce it (QUALITY items 24, 31, 46: seat scope binds the narrower declaration).

## QUALITY check (performed, not promised)

- **1** every claim is a located quote/key or is marked inference (§3, §10-U1). **2** sources are file+key/criterion, no oral anchors. **3** observations (§2), inference (§3), unknowns (§10) are separate sections. **4** no erratum is created here, so append-only is untouched. **9** negative scope stated in U4. **19** the only replacement propositions (the rule) are marked inference and carry their supporting objects; no quote is transferred across objects. **21/23/30** locators are numbered criteria and JSON key paths, not fragile line ranges; no historical observation is refreshed. **24/26** no extra probes, no package-manager text. **31** execution class declared at top and in the trailer. **38/42** no candidate bytes are judged here, so no digest/predicate binding is claimed. **43** the eight policy rows are graded as depth evidence, not execution. **44/48** absent/malformed evidence is treated as non-clean and buckets are named. **45** no five-column class table is asserted. **47** no enforcement claim is made anywhere.

## Receipt

Reviewed-SHA256: 0141ba62c2cc324e5c0fdae7c49fb7e22773a54ab8cf7faf23eace73fb30f959
Predicate: r23-sourcefrontier23
Scope: executed=none
