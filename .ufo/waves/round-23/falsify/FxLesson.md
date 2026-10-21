# FxLesson — round23 falsify review of `corpus/lessons/round-23.md`

Seat: TsukuroiR23-2.FxLesson-2, leaf critic. NO-EXEC, NO-FETCH. Nothing was executed, hashed, or counted with a tool.

## Bounded search

I read only the declared files:

- the landed lesson at `.ufo/waves/round-23/candidate/corpus/lessons/round-23.md`
- `.ufo/waves/round-23/preregister.json`
- `.ufo/waves/round-23/sources/r22-closure.json`
- `.ufo/waves/round-23/candidate/.ufo/waves/round-23/measure/l1-mutation.json`
- `.ufo/waves/round-23/sources/godspeed-directive.txt`, which I used because `skill://godspeed` is not resolvable in this runtime

This report did not exist before I wrote it.

These files were outside my binding, so I did not read them: QUALITY criteria, `path-reconciliation.json`, `r22-rough-census.txt`, the build refusal and attempt receipts, the checker sources, and the r22 lesson and report. Pointers into them are marked unverified, not false.

Axes I checked: completeness of the row schema (class, evidence, captured-by, fail-capable fix), whether evidence pointers resolve, whether captured-by is honest, whether each fix is shown able to fail, internal arithmetic, and provenance/identity.

## Verdict

The lesson breaks its own invariant. It says "No fix is counted before observed failure controls", but three of the seven Mistakes rows have no observed failure control:

- R23-QUALITY-TREND
- R23-RECEIPT-EXAMPLES
- R23-PRELUDE-SHADOW

Two more rows state a "must fail" obligation without pointing to the controls that already exist in `l1-mutation.json`:

- R23-PATH-UNIT
- R23-EDIT-AUTHORITY

R23-RETRY-SPACING claims its guard fired, but cites no receipt for that, and its gap figure is off by one second.

R23-RAW-ORDER is the only row whose fix cites a recorded control that I could check: L1 mutant 0 against `check-path-reconciliation.py` has exit 1 and `killed: true`.

All of these defects can be fixed in the lesson text. None of them requires a canonical-judge rejection of C1, C2 or C3 on their metrics. However, a judge should not count any of the three no-control rows as fail-capable lessons.

## Per-row findings

### 1. R23-QUALITY-TREND (frontier / quality trend)

**Fix not shown able to fail.**

- **Evidence.** It resolves for the outside side: in `r22-closure.json`, `trends.quality` is `"unchanged"`, and the notes say "in-round gate hardening ... concern new material; no prior entry superseded or re-verified". The author-side "improved" label has no pointer to the r22 lesson or report. The disagreement is therefore cited from one side only.
- **Captured-by is misattributed.** The row says "LEARNING quality definition, QUALITY1/3". The closure shows that the outside verifier, CloseKaidoku22 at MANIFEST rounds[422], caught the mistake. The internal criteria existed in r22 and did not catch the author's "improved" label, so they are prevention text, not the capture.
- **Fix.** The fix is a norm ("do not credit an instrument's existence as corpus quality") plus "New criterion cites this outside disagreement". The row names no check that turns red when a future lesson claims quality improved without a superseded or reverified prior entry. No red control is cited.
- **Falsifier.** Write a future lesson that reports "quality improved" based only on new gates. Nothing cited in the row would reject it.
- **Smallest remedy.**
  - Set Captured-by to `outside closure CloseKaidoku22, MANIFEST rounds[422]`.
  - Add the author-side pointer, which is the r22 lesson or report row.
  - Either cite a check that has a red control for an "improved quality without supersede or reverify" claim, or label the fix "unenforced norm — not fail-capable".

### 2. R23-PATH-UNIT (C3)

**Fail capability is asserted prospectively and not cited.**

- **Fix.** The fix reads "wrong arithmetic, dropped/duplicate identity or forged disposition must fail". This is an obligation, not an observed failure.
- **Controls that do exist (author-side) in `l1-mutation.json` for `check-path-reconciliation.py`:**
  - mutant 1: deleting the ledger-mismatch check is killed
  - mutant 6: the retained-total check is killed
  - mutant 9: the orphan-retained check is killed
  - mutants 3 and 4: the first-failure index logic is killed
  - mutant 5: the disposition branch is killed
- **Gap.** No recorded mutant targets duplicate identity. "Duplicate identity must fail" therefore has no shown control.
- **Duplicate authority.** This row and R23-RAW-ORDER explain the same discrepancy, the "2+4" events behind 25/33 versus 23/29, with two separate fixes. The 2+4 matches the preregister and closure counts: 25−23=2 and 33−29=4. Counting both fixes double-credits one C3 discrepancy.
- **Unverified.** The pointer to the S085 source cell is outside my binding.
- **Smallest remedy.**
  - Cite `l1-mutation.json` mutants 1, 3, 4, 5, 6 and 9 for the arithmetic and disposition controls.
  - Either name a control for duplicate identity or drop "duplicate identity" from the fail claim.
  - Mark R23-RAW-ORDER as the concrete instance of this row instead of a second fix.

### 3. R23-EDIT-AUTHORITY (C1 / C2)

**Fail capability is asserted prospectively and not cited.**

- **Evidence.** It resolves: the closure records "edit16/17=unknown-tool16/17" and out-of-binding reads.
- **Fix.** It says the target, subset, opaque, extra-key and wrapper controls "must be discriminating". The row cites no control.
- **Controls that do exist (author-side) for `check-seat-bindings.py`:**

  | Fix element | Mutant | What the mutant does |
  |---|---|---|
  | v1 cannot inherit | 0 | `allow_structured_edit` gate dropped |
  | v1 cannot inherit | 9 | v2 schema match widened |
  | read authority does not grant edit | 1 | `read_paths` accepted as edit target |
  | read+write requirement | 2, 3 | one of the two requirements dropped |
  | extra key | 4 | seat key-set check removed |
  | opaque / shape | 5 | `path`-only instead of shape set |
  | wrapper | 6 | flag not propagated to children |
  | external URI | 8 | URL check removed |

  `check-edit-contract.py` mutants 0–6 cover the eight C1 decision rows.
- **Kill criterion weakness [INFERENCE].** The receipt's method is "killed = nonzero exit". A mutant that crashes, for example with a TypeError, SyntaxError or IndentationError, counts as killed without proving the selftest discriminates. Seat-bindings mutant 6 drops the `allow_structured_edit` argument. If `classify` has no default for that parameter, the mutant dies from a TypeError, not from a wrapper-edit assertion. The receipt records neither the failing case names nor the exception type, so I cannot tell which happened.
- **Smallest remedy.**
  - Cite the mutant IDs above in the row.
  - In the mutation receipt, record which named selftest case failed, so that a crash is distinguishable from a discriminating kill.

### 4. R23-RECEIPT-EXAMPLES (frontier / receipt process)

**Fix not shown able to fail.**

- **Evidence.** Partly resolves: the closure has "faulty buckets 3+5", which equals 8, plus the FxC2TraceMissing and FxC2ParallelExec faults. The second pointer, "r22 final summary", has no path.
- **Fix.** The fix is a prompt instruction: "Tell seats to indent example receipt lines". "Original faults stay red" is a regression property of the strict checker. It does not show the instruction can fail.
- **No control.** None of the 27 mutants in `l1-mutation.json` targets receipt parsing or the one-actual-receipt rule. "Source-only strings never prove reading" has no control either.
- **Falsifier.** A seat that pastes an unindented example receipt plus its real receipt passes every control cited in the row, because none is cited.
- **Smallest remedy.**
  - Replace "r22 final summary" with a path.
  - Either cite a strict-receipt selftest that goes red on a duplicated, unindented example prefix (with a mutant or red-case reference), or label the fix "prompt norm — not fail-capable".

### 5. R23-RETRY-SPACING (frontier / process)

**Arithmetic error, and the guard's failure claim has no receipt.**

- **Arithmetic.** The six listed times give gaps of 45, 71, 104, 75 and 105 seconds. From 13:32:58 to 13:34:43 is 105 seconds, so the stated range "45–104 s" is wrong. The total of 9 attempts is consistent: 2 predecessor + 6 mine + mine-7 = 9. Mine-7 at 13:38:13 is 210 seconds after 13:34:43, which is at least 180 seconds.
- **Unreceipted guard claim.** "A 180 s guard ... refused three early calls" is the row's only fail-capability claim. Its evidence column cites only `refusal-03.json` and `attempt-mine-2..6.json`, which are the six cap and backoff attempts. All six had gaps under 180 seconds. If the guard had existed then, it would have refused them, so the three guard refusals must be separate calls, presumably inside the 210-second window. No receipt is cited for them, and they are not counted in the "9 attempts in all".
- **Captured-by.** The cited "hyaku addendum job-cap rule" is the rule that was violated, not the mechanism that detected the violation.
- **Stale contradiction.** The "Mechanics and limits" section still says "First whole64-seat build call was refused ... retained for a full-payload retry after backoff". That is the state before the spawn, and it contradicts this row's report that mine-7 spawned 64.
- **Smallest remedy.**
  - Change "45–104 s" to "45–105 s".
  - Cite the three guard-refusal receipts, or withdraw "refused three early calls".
  - Change Captured-by to the actual detector, either self-audit or the guard.
  - Append one sentence to Mechanics recording that the mine-7 spawn succeeded.

### 6. R23-PRELUDE-SHADOW (frontier / tooling)

**Fix not shown able to fail. The row confuses showing the defect with showing the fix.**

- **Captured-by.** It is "none", so the row has no capture mechanism and fails the schema requirement as written.
- **Fix.** The fix is a norm: "Never bind prelude names in coordinator kernels". The claimed demonstration, "the shadowed kernel failed, and the reset kernel dispatched", shows the bug producing an AttributeError and a reset fixing it. It does not show any control that detects a rebinding of a prelude name before dispatch.
- **Falsifier.** Rebind `tool` in a later kernel. Nothing cited detects it until the runtime AttributeError happens again.
- **Smallest remedy.**
  - Relabel the fix "unenforced norm; captured-by none; fix not fail-capable".
  - Or cite a kernel check that has a red control for assigning a prelude name.
  - Remove the sentence "The fix is shown able to fail".

### 7. R23-RAW-ORDER (C3)

**Shown able to fail. Residual gaps are noted below.**

- **Control.** `l1-mutation.json` mutant 0 of `check-path-reconciliation.py` widens `ROUGH_SUFFIX` with a leading `(:raw)?`, and the result is exit 1, killed. I traced the regex by hand:
  - the original leaves `p:raw:N-M` as `p:raw`
  - it fully strips `p:N-M:raw`
  - the mutant fully strips `p:raw:N-M`

  This is consistent with the row's "mixed raw/range order" explanation.
- **Gap: attribution.** The receipt records only "selftest: FAIL". It does not show that `mixed-raw-range-order` or `rough-misses-raw-first` was the failing case, so the attribution in the row is not evidenced.
- **Gap: one direction only.** Only widening is mutated. No narrowing mutant exists, for example removing the trailing `(:raw)?`.
- **Gap: binding to the outside rule [INFERENCE].** I found no cited control that binds `ROUGH_SUFFIX` byte-for-byte to the outside regex in S085. Mutant 2 covers frozen data digests, not equality between the regex and its source.
- **Gap: zero lane-only events.** "All six rough-only path events" together with a net difference of 2+4 implies there are no lane-only (cancelling) events. The row does not state that explicitly, and the ledger needed to check it is outside my binding.
- **Gap: "independently located".** It is asserted, but ReconBuild08 and ReconFalsify01 were dispatched by the same L1. This is unverified.
- **Smallest remedy.**
  - Record the failing case names in the mutation receipt.
  - State "zero lane-only events" in the row with a pointer to the ledger.
  - Optionally add a narrowing mutant.

## Provenance / identity

- **Author mismatch.** The header says "author: TsukuroiR22 continuing under Main's new round23 attempt1 claim". The mutation receipt names "TsukuroiR23-2 (L1, author-side)", and R23-RETRY-SPACING speaks as the "Replacement L1" ("mine 1–6"). The lesson credits all its rows to one author, while its own text shows two coordinators.
  - Smallest remedy: name both authors in the header, and attribute rows 5–7 to the replacement L1.
- **Author-side mutation receipt.** It is labelled "not an outside verifier". The rows that rely on it should say "author-side mutation" rather than imply independent confirmation.

## Impacted axes

- **Calibration (C3):** rows R23-PATH-UNIT and R23-RAW-ORDER (double-credit, unshown duplicate-identity control, raw-order attribution).
- **Depth and operability (C1 and C2):** row R23-EDIT-AUTHORITY (controls exist but are uncited; crash kills look the same as discriminating kills).
- **Process and receipt hygiene (frontier):** rows R23-QUALITY-TREND, R23-RECEIPT-EXAMPLES, R23-RETRY-SPACING and R23-PRELUDE-SHADOW.
- No prior entry was shown harmed. These findings do not reach the preregistered metric values.

## Named fixes not shown able to fail

- R23-QUALITY-TREND: the "do not credit instrument existence" norm and the new criterion.
- R23-RECEIPT-EXAMPLES: the "indent example receipt lines" instruction.
- R23-PRELUDE-SHADOW: the "never bind prelude names" norm.
- R23-RETRY-SPACING: the 180 s guard, whose claimed refusals are unreceipted.
- R23-PATH-UNIT: "duplicate identity must fail", which has no recorded control.

Reviewed-SHA256: b1ed78ac818ed5b1d9bd201de9c3a9c530f95a59944618133c4b51bf3b911199
Predicate: r23f-fxlesson
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
