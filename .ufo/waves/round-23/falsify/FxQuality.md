# FxQuality — attack on QUALITY criteria 49–51 (round 23, attempt 1)

Seat: `TsukuroiR23-2.FxQuality-2` (falsify leaf). Predicate `r23f-fxquality`.
Reviewed object: `.ufo/waves/round-23/candidate/corpus/QUALITY.md` (digest supplied, not recomputed).
Attack axis: frontier claim "three new corpus admission criteria + one admission-bar row set (49–51)" and the
three claims they police: **C1** (eight typed structured-edit authority decisions), **C2** (explicit schema-v2
edit audit authority), **C3** (r22 rough-vs-canonical path-census ledger).

## 0. Bounded search actually performed (NO-EXEC, NO-FETCH)

Read (declared paths only, no hashing, no command, no child):

- `.ufo/waves/round-23/candidate/corpus/QUALITY.md` (full file, 51 numbered criteria)
- `.ufo/waves/round-23/candidate/corpus/lessons/round-23.md` (gate table, opened sources S085/S086, Mistakes table, r22 disposition)
- `.ufo/waves/round-23/preregister.json` (claims C1–C3, `edit_decisions` 8 rows, `ordinals`, `path_counts_as_reported`, `limits`)
- `.ufo/waves/round-23/sources/r22-closure.json` (verdicts, `trends`, `notes`, `verification.rechecks`)
- `.ufo/waves/round-23/candidate/.ufo/waves/round-23/measure/l1-mutation.json` (27 mutants, tool names, killed flags)
- `.ufo/waves/round-23/sources/godspeed-directive.txt`

Grep (declared file only): QUALITY.md for `URI|edit|Edit`, `quality|improv|trend|reverif|supersed`,
`remote|http|scheme|external|URI|path traversal|dot-segment`; r22-closure.json for `trends|quality|unchanged|improved`.

Nothing was executed, compiled, imported, fetched or delegated. Absence of a tool/artifact is reported as
"not in the declared read scope", never as "does not exist".

## 1. Headline answer to the assigned question

**"Does 49 actually prevent a quality-improved verdict for this round without prior-entry supersession?"**

Literal reading: **yes, partly.** 49 has a working fallback — "Name the prior weaker/stale entry that was
superseded or reverified, with actual evidence; **otherwise retain unchanged**." With no such entry named, a
quality-improved verdict is disallowed.

Sufficiency reading: **no.** 49's positive condition is satisfiable by the *same artifact the round already
produced* — the correction of the stale r22 author trend label — and by nothing that constitutes corpus-content
improvement. Concretely, the following claim passes 49 word for word while being the wrong verdict for r23:

> "quality: improved — the prior weaker/stale entry is the r22 author report's `quality: improved` label, now
> superseded by the outside verifier CloseKaidoku22 at MANIFEST rounds[422]
> (`.ufo/waves/round-23/sources/r22-closure.json`, `trends.quality = unchanged`); r23 additionally reverified
> the r22 path counts per event (C3)."

Why that claim must be *wrong* for r23, on this round's own ground truth:

- `r22-closure.json` `notes` states the outside quality-trend rule verbatim: "Quality trend unchanged: in-round
  gate hardening and registry repair concern new material; **no prior entry superseded or re-verified**."
  The unit of "entry" there is a corpus entry (S-row / lesson), and correcting a *prior round's trend label* is
  calibration, not corpus-content improvement.
- `.ufo/waves/round-23/candidate/corpus/lessons/round-23.md` gate table rejects exactly the move: "A new gate
  or in-round hardening automatically improves quality trend | **reject** | CloseKaidoku22 judged r22 quality
  unchanged: new material was hardened, but no prior entry was superseded or reverified."
- `preregister.json` C3 scope: the round "does not relabel old violations or **retry historic checks for
  confirmation**" — so the "reverified" branch of 49 cannot be fed by re-running r22 checks; the only r23
  candidate for the positive branch is the trend-label correction, which is circular.

So the honest r23 verdict is `quality: unchanged`, and 49 does not by itself force it: it constrains the
*absence* of supersession but does not constrain *what kind* of supersession qualifies. See **F1** (high).

## 2. Findings by severity

### F1 (high) — QUALITY 49's positive branch is circular for this round: the calibration correction that created 49 also satisfies it

- **Location:** QUALITY.md:97 (criterion 49, `R23-QUALITY-TREND`).
- **Defect:** 49 requires "the prior weaker/stale entry that was superseded or reverified". It never scopes
  *entry* (corpus content entry: knowledge row `S###` / lesson id) against *prior-round report verdict*. The
  r22 author report's stale `quality: improved` label is literally a "prior weaker/stale entry" and is literally
  superseded by r23's own outside-correction record (`lessons/round-23.md` § Outside round22 disposition;
  `r22-closure.json` `trends.quality = unchanged`). An author who cites it satisfies 49 and may then write
  `quality: improved` for r23, while corpus content is unchanged and the outside precedent for r22 says such
  in-round material is `unchanged`.
- **Aggravating:** the round's own gate table and the outside closure both say the r23 trend should be
  `unchanged`; 49 as written does not mechanically exclude the `improved` label. The criterion therefore fails
  the very error class it was minted for (R23-QUALITY-TREND: "do not credit an instrument's existence as corpus
  quality") because it credits a *label correction* as evidence of corpus quality.
- **Bounded falsifier (constructed, not executed):** the claim quoted in §1. Every clause of 49 is satisfied
  (a named prior stale entry; the superseded r22 label; "actual evidence" = `r22-closure.json`
  `trends.quality`; append-only correction respected), yet the resulting verdict contradicts
  `r22-closure.json` `notes` and the r23 gate table. A criterion that admits this claim is not sufficient.
- **Smallest in-scope remedy (one appended sentence set to 49, no rewrite of r22):**
  1. scope the qualifying entry: "the prior entry is a **corpus content entry** (knowledge row `S###` or lesson
     id), not a prior round's trend label or report verdict";
  2. state the negative: "a correction to a prior round's trend label, an appended outside verdict, or in-round
     gate/registry hardening **leaves the quality trend unchanged**";
  3. anchor the evidence: "the trend claim cites the outside MANIFEST entry id and the `trends.quality` field it
     reads, plus the superseded entry's row/lesson id and its superseding row id".
  Preserves append-only: the correction stays an appended block, the r22 author bytes stay untouched.

### F2 (medium-high) — QUALITY 49 is not testable: no falsifier, no defined axis, unbounded "actual evidence"

- **Location:** QUALITY.md:97.
- **Defect:** 49 states no fail-capability condition (contrast 31: "the gate … reports zero … and the gate not
  exiting non-zero"; 32: "Falsified by: moving the quoted sentence one paragraph"; 37: "Test both the inert
  control and mutation control"). "with actual evidence" is unbounded: any citation satisfies it, including a
  citation to the very same outside verdict that created the criterion. The word "quality" is never defined
  against a corpus-content scope, so the criterion is decidable only by a reader's charitable interpretation.
- **Evidence of the sharper failure:** r22-closure.json `notes` is the operational definition
  ("in-round gate hardening and registry repair concern new material; no prior entry superseded or
  re-verified"). 49 paraphrases it but drops the "concern new material" half — which is exactly the half that
  produces `unchanged` for r23.
- **Remedy:** add the fail-capability clause: "Falsified by: a round claiming `quality: improved` while naming
  only new material (new instrument, new gate, new fixture, appended correction to a prior trend label) — such a
  claim is red; the trend is retained `unchanged`." And name the evidence shape required by F1(3).

### F3 (medium) — QUALITY 51 permits unexplained cohorts to be *retained*, contradicting its own cited lesson and the preregistered C3 metric

- **Location:** QUALITY.md:99 (criterion 51, `R23-PATH-UNIT`).
- **Defect:** 51 requires that "Every snapshot digest, row, disposition and subtotal must **agree or remain
  unexplained/non-clean**". The disjunction licenses a state where the counts do not agree and the row is
  simply left flagged. The cited lesson (`lessons/round-23.md` R23-PATH-UNIT fix condition) requires the
  opposite: "Every fixed event/component is accounted with policy and unit differences; **wrong arithmetic,
  dropped/duplicate identity or forged disposition must fail**". The preregistered C3 metric is
  `unexplained_cohorts: before 2 → target 0`, so "remaining unexplained" is by definition a metric above zero,
  i.e. a failed target — yet 51 as written lets it be filed as satisfied-by-disclosure.
- **Note (mitigating):** the landed instrument is stricter than the prose — `l1-mutation.json` records
  `check-path-reconciliation.py` mutants 1 (`RECONCILIATION-LEDGER-MISMATCH` removed), 2 (digest check
  `if False:`), 6 (`totals['retained_path'] != expected['lane_retained']` → `if False:`), 9
  (`if derived['orphan_retained_sites']:` → `if False:`), all `killed: true`, i.e. arithmetic, digest, total and
  orphan mismatches do exit non-zero. The gap is therefore in the **bar's wording**, not in this round's tool:
  the bar permits a state the tool forbids, so the corpus can drift back to the permissive reading.
- **Remedy:** replace the disjunction with: "a row, disposition, subtotal or digest that does not agree is a
  red finding that keeps the preregistered `unexplained_cohorts` metric above zero and exits non-zero; it is never
  discharged by disclosure alone."

### F4 (medium) — QUALITY 51 drops the cited lesson's "policy" requirement, omits the round's actual new failure-mode anchor, and asserts S085 content without quoting it

- **Location:** QUALITY.md:99.
- **Defect (three linked gaps):**
  1. The lesson it cites requires "accounted with **policy and unit** differences". 51 lists only
     "normalization and counting-unit explanation". The *policy* half is the ground truth of this round:
     `lessons/round-23.md` R23-RAW-ORDER — "All six rough-only path events are `:raw:N-M` selectors that the
     **outside regex** leaves as `<path>:raw`" — i.e. an outside-classifier **policy** difference (outside
     rough 25/33 vs retained 23/29, per `preregister.json` `path_counts_as_reported` and the lesson's
     "outside rough25/33 versus retained23/29"), with unit (path-site vs selector-suffix event) as the second
     axis. A reconciliation that explains only units/normalization leaves the actual policy divergence
     unexplained, which is the requirement 51 exists to impose.
  2. 51 never names R23-RAW-ORDER, the tool, or the fail-capability anchors recorded in the lesson
     ("`check-path-reconciliation.py` selftest `mixed-raw-range-order` and unit `rough-misses-raw-first` fail if
     the rough rule is widened (L1 mutant 0 killed)"). 49 and 50 both name their lesson ids; 51 names only
     R23-PATH-UNIT, so the raw-selector discovery — the round's actual new red — has no locatable anchor in the
     bar. `l1-mutation.json` mutant 0 for `check-path-reconciliation.py` (the `ROUGH_SUFFIX` regex) is
     `killed: true`, so the anchor exists in the landed record but is uncited by the criterion.
  3. 51's locator "S085 preserves the exact first-failing-component source rule" asserts the rule's existence
     without stating it, so no reader can check that the ledger applies the same counting rule. S085's quote in
     `lessons/round-23.md` is "if q not in (b['write_paths'] if t=='write' else b['read_paths']):" followed by
     the first-failure break. Criterion 21 (R15-LOCATOR) requires a stable anchor *and an exact quote*; 49 and
     50 satisfy that, 51 does not.
- **Remedy:** in 51 — (a) add "policy" to the required explanation set ("policy and unit differences"); (b) add
  "R23-RAW-ORDER" to the lesson citation together with `tools/check-path-reconciliation.py` selftest
  `mixed-raw-range-order` and unit `rough-misses-raw-first`; (c) replace the S085 assertion with the ≤25-word
  quote "if q not in (b['write_paths'] if t=='write' else b['read_paths']):" and the statement that the retained
  count uses the same first-failure rule.

### F5 (medium) — QUALITY 50's required control enumeration is a strict subset of its own normative enumeration

- **Location:** QUALITY.md:98 (criterion 50, `R23-EDIT-AUTHORITY`).
- **Defect:** 50's normative clause forbids authority from "A v1 row, report ownership, opaque patch body,
  **extra field** or **alternate spelling**", but its fail-capability clause requires controls only for
  "target/subset/**body-key**/wrapper". The cited lesson R23-EDIT-AUTHORITY requires "target/subset/**opaque**/
  **extra-key**/wrapper controls must be discriminating". So "extra-key" was dropped from the control list and
  "opaque" was renamed "body-key" with no stated mapping. A weakened rule that accepts an **extra field** in a
  binding row / edit argument set, or that accepts an **alternate spelling** of a declared target, is therefore
  not covered by any control 50 obliges.
- **Evidence:** in the landed mutation record `l1-mutation.json`, `check-seat-bindings.py` mutants cover target
  membership (1), the read+write requirement (2, 3), seat key-set exactness (4), edit body shape set (5), nested
  wrapper propagation (6) and v1-vs-v2 schema selection (9) — all `killed: true`; but **no mutant exercises an
  alternate-spelled or extra-field edit target**. The gap is therefore in the criterion's obligation, and the
  today-passing implementation does not discharge it either.
- **Remedy:** make the control enumeration match the normative list explicitly, e.g. "Independent literal
  target/subset/body-key/extra-field/alternate-spelling/v1-row/wrapper controls must each fail the corresponding
  weakened rule", or state the mapping "body-key ≡ opaque; extra-field and alternate-spelling controls are
  required in addition to body-key".

### F6 (medium) — One of the eight preregistered C1 decisions (EDIT_EXTERNAL) has no normative home anywhere in QUALITY 1–51

- **Location:** QUALITY.md:98 (criterion 50) vs `preregister.json` `edit_decisions[6]`.
- **Defect:** the eight preregistered decisions are DECLARED_EDIT, UNDECLARED_EDIT, READ_ONLY_EDIT,
  WRITE_ONLY_EDIT, OPAQUE_PATCH, EDIT_TRAVERSAL, **EDIT_EXTERNAL** ("Remote or internal URIs do not become
  filesystem edit targets"), EXPANSION. QUALITY 50 covers six of the seven rule classes (declared/read/write
  requirement, report ownership, opaque body, alternate spelling, per-step audit) but never states the URI rule;
  a grep of the whole file for `URI|remote|http|scheme|external` returns **no occurrence inside 49–51** and no
  occurrence anywhere else in the file. Criterion 47 audits "URL reads" but never denies a URI as an *edit*
  target. Therefore a future admitted decision that treats a remote or internal URI as a filesystem edit target
  violates none of criteria 1–51, while C1's preregistered decision set and the implemented gate both reject it
  (`l1-mutation.json`, `check-seat-bindings.py` mutant 8 removes the `SCOPE-FETCH-DENIED` URL rejection and is
  `killed: true`).
- **Corroborating live concern:** `r22-closure.json` `notes` records r22's out-of-binding reads as "including two
  typo paths and **one internal URI**" — the exact class 50 leaves uncovered.
- **Remedy:** append to 50 one clause: "a remote or internal URI (scheme, authority or path form) is never a
  filesystem edit target; EDIT_EXTERNAL remains a DENY decision."

### F7 (low) — QUALITY 50 restates the nested-audit rule in divergent wording from criterion 47

- **Location:** QUALITY.md:98 ("Audit each recorded adapter step separately") vs QUALITY.md:93 (criterion 47,
  R22-ENFORCEMENT-LIMIT: "audit recorded request arguments separately, including nested parallel wrappers and URL
  reads").
- **Defect:** two formulations of one rule ("adapter step" vs "request argument"; "nested" vs "nested parallel
  wrappers") invite divergent application — 47's recursion/parallel-wrapper clause and 50's "each recorded adapter
  step" are not textually bound to each other. This is duplication-with-divergence, not a duplicate rule.
- **Remedy:** 50 cites 47 for recursion and parallel-wrapper semantics ("each recorded adapter step separately
  (criterion 47's recorded-request-argument audit, including nested parallel wrappers)").

### F8 (low) — QUALITY 49–51 name no checking command or fail-capability artifact, unlike 31 and the preregistration

- **Location:** QUALITY.md:97–99.
- **Defect:** criterion 31 names `tools/check-seat-scope.py` and its required exit state; the preregistration names
  `tools/check-edit-contract.py`, `tools/check-seat-bindings.py` and `tools/check-path-reconciliation.py`. 49–51
  name none, and none cites `.ufo/waves/round-23/measure/l1-mutation.json` (27/27 killed) — the only fail-capability
  evidence in the landed record. Consequence: a later round can cite "criterion 51" without ever exercising a
  discriminating control, and the raw-order mutant-0 kill (the round's own new red) has no criterion-side anchor
  (see F4.2).
- **Remedy:** each of 50/51 cites its tool and the mutation record path; 49 cites the outside MANIFEST entry id
  and field it reads.

## 3. Per-criterion verdicts (testable / non-duplicative / grounded)

| Criterion | Testable | Non-duplicative of 1–48 | Grounded in cited lesson | Blocking finding |
|---|---|---|---|---|
| 49 `R23-QUALITY-TREND` | **No** — no falsifier, unbounded "actual evidence", no defined axis unit (F2) | Yes — no 1–48 row polices cross-round trend calibration; overlaps with 3 only superficially | Yes — lesson row exists; cited evidence (`r22-closure.json` `trends.quality=unchanged`, CloseKaidoku22 rounds[422]) is locatable and present | **F1 (high)**, F2 |
| 50 `R23-EDIT-AUTHORITY` | **Partly** — the landed tool set is fail-capable (mutants 0–9, all killed) but the criterion names no tool and its control list is narrower than its rule list (F5, F8) | Yes — additive over 24/31/42/46/47: it adds edit-authority (read+write+edit), v1/v2 selection and required controls; wording diverges from 47 (F7) | Yes — lesson row R23-EDIT-AUTHORITY exists with S086; but one of the eight preregistered decisions (EDIT_EXTERNAL) is not represented in the bar (F6) | F5, F6, F7, F8 |
| 51 `R23-PATH-UNIT` | **Partly** — the landed tool is fail-capable (10 mutants, all killed) but the criterion names no tool, and its "or remain unexplained/non-clean" clause contradicts the lesson's "must fail" (F3, F4) | Yes — distinct from 9/19/41/46/48; extends 30's "named count corrections include the exact counted … finite input set" to path cohorts; 30 should be cited rather than restated | Partly — lesson row exists, but the criterion drops "policy", omits R23-RAW-ORDER and asserts S085 content without quoting it (F4) | F3, F4, F8 |

**Duplication verdict:** 49–51 are not duplicates of criteria 1–48. The nearest neighbours are 47 (structured
authority vs. prompt-scope non-enforcement), 48 (seat-receipt cohorts vs. path-event cohorts) and 30 (counted
input sets). In each case 49–51 add a distinct, non-covered obligation; the defects above are coverage gaps and
divergent wording, not redundancy. One duplication *does* exist inside 51's own citation: 51 re-derives 30's
"exact counted finite input set" requirement without citing it — harmless, but a cross-reference is cheaper than
a restatement.

## 4. Confirmed-strong points (no finding; recorded so the round is not "fixed" into regression)

- The three lesson ids in the criteria headings match `lessons/round-23.md` exactly
  (`R23-QUALITY-TREND`, `R23-EDIT-AUTHORITY`, `R23-PATH-UNIT`), and R23-RAW-ORDER's `captured-by QUALITY51`
  correctly targets 51.
- 51's clause "A net difference is not a count of missing unsafe events" correctly encodes the round's ground
  truth (outside rough 25/33 vs retained 23/29 → 2 build + 4 falsify = 6 rough-only events, all `:raw:N-M`
  selector artefacts, per R23-RAW-ORDER and `preregister.json` `path_counts_as_reported`).
- 50's "exact edit targets also declared readable/writable" matches the preregistered decisions READ_ONLY_EDIT
  (DENY), WRITE_ONLY_EDIT (DENY) and DECLARED_EDIT (ALLOW) and the killed `check-seat-bindings.py` mutants 1–3;
  "A v1 row … never grants that authority" matches mutant 9 (`schema` `tsukuroi-seat-bindings-v2` vs any `-v*`).
- "preserve all historical v1 reds" (50) and "old violations are never reauthorized" (51) correctly block
  retrospective authorization, matching the round's rejected proposal "Retrospectively allow r22 report reads or
  edits under new v2 policy".
- 49's "Append outside trend corrections rather than rewriting the author report" matches the lesson's
  "Append the outside correction, never rewrite r22".

## 5. Smallest in-scope remedy set (one append-only edit to QUALITY.md, no other file)

1. **49** — append three sentences (F1): qualifying entry = corpus content entry (`S###`/lesson id); a prior
   trend-label correction, an outside verdict append or in-round gate/fixture growth **leaves the trend
   `unchanged`**; the claim must cite the outside MANIFEST entry id + `trends.quality` field + superseded row id
   and superseding row id. Add the F2 falsifier sentence.
2. **50** — (a) extend the control enumeration to the full normative list (v1 row, report ownership, opaque body,
   extra field, alternate spelling) or state the `body-key ≡ opaque` mapping plus the two missing controls (F5);
   (b) add "a remote or internal URI is never a filesystem edit target" (F6); (c) cite criterion 47 for nested /
   parallel-wrapper recursion (F7).
3. **51** — (a) replace "must agree or remain unexplained/non-clean" with "a disagreeing row/disposition/subtotal/
   digest is a red finding that keeps `unexplained_cohorts` above zero and exits non-zero; disclosure never
   discharges it" (F3); (b) add "policy" to the required difference set and cite R23-RAW-ORDER with
   `tools/check-path-reconciliation.py` selftest `mixed-raw-range-order` / unit `rough-misses-raw-first` (F4.1–2);
   (c) quote S085's ≤25-word first-failing-component rule inline instead of asserting it (F4.3).
4. All three — cite the checking command / artifact path (F8): `tools/check-edit-contract.py`,
   `tools/check-seat-bindings.py`, `tools/check-path-reconciliation.py`,
   `.ufo/waves/round-23/measure/l1-mutation.json`.

No production file, lesson file, registry, route or VCS state was modified by this seat; this report is the
only artifact written.

## 6. Residual risk and verification gaps

- **Not verified by execution (NO-EXEC seat):** F3's claim that the *landed* `check-path-reconciliation.py`
  exits non-zero on unexplained cohorts rests on `l1-mutation.json` (mutants 1/2/6/9 `killed: true`), not on a
  run performed here. The bar-vs-tool divergence (F3) is a wording finding and stands either way.
- **Not verified:** that `l1-mutation.json` is the complete landed mutation set for the three tools (the file's
  own `survivors_fixed_before_record` field shows three pre-record removals, so the record is curated by
  declaration, not independently complete).
- **Not in declared read scope, therefore unknown (not "absent"):** the landed `tools/check-edit-contract.py`,
  `tools/check-seat-bindings.py`, `tools/check-path-reconciliation.py` sources; the corpus `corpus/knowledge/`
  entries that 49 calls "prior entries"; the round-23 author report that would carry the trend verdict; the
  outside MANIFEST entry `rounds[422]` itself (only the copied packet
  `.ufo/waves/round-23/sources/r22-closure.json` was readable). Whether r23 superseded any *corpus* entry is
  therefore **could-not-evaluate** from this seat's scope; F1 does not depend on it — F1 is the falsifier that 49
  permits a wrong verdict *even when* no corpus entry was superseded.
- **Open calibration question for Main/L1:** if 49 is read with "entry" = corpus content entry, the r23 verdict
  is `quality: unchanged` and F1 disappears as a live risk; if it is read with "entry" = any prior artifact,
  F1 is live. The remedy in §5.1 makes the reading explicit rather than leaving it to the reader.
- **Untested by this seat:** the C1/C2/C3 claim metrics themselves (eight decisions, structured_edit_mode,
  unexplained_cohorts) — outside this seat's assignment, which is limited to QUALITY 49–51.

Reviewed-SHA256: 99d70d94f1eecebfbf06088d39df0f378c9ce79dac4f6f6d6a4f55f8ee967043
Predicate: r23f-fxquality
Scope: executed=none
