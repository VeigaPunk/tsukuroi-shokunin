# Falsification report — FxKnowReconcile (tsukuroi round23, attempt1, FALSIFY wave)

Seat: `TsukuroiR23-2.FxKnowReconcile-2` (leaf reviewer; no subagents dispatched, no edits outside this report).
Target: `.ufo/waves/round-23/candidate/corpus/knowledge/path-reconciliation-r23.md`
Declared SHA256 (supplied by seat binding, NOT computed by this seat): `7661f37ab6b40668ec025b2a68f86791784ef296eccba7a458a6862dde89c3fc`
Baseline pinned by the target and this seat: `ae01e50f582016384e620022be38bf5367000e2e`
Outside round22 closure admitted at MANIFEST rounds[422], fleet `4482c275f9381f219ee4d092e0324d417c3cb1e7`.

Scope of work: every factual sentence of the reconciliation knowledge entry was attacked against the ledger
(`.ufo/waves/round-23/path-reconciliation.json`), the frozen r22 inputs
(`.ufo/waves/round-23/snapshot/r22/{build,falsify}/{events,bindings,audit}.json`), the frozen input pins
(`.ufo/waves/round-23/frozen/reconciliation-inputs.json`), the gate
(`tools/check-path-reconciliation.py`), the v1 sibling authority (`tools/check-seat-bindings.py`), the recorded
mutants (`.ufo/waves/round-23/measure/l1-mutation.json`), the copied outside sources
(`.ufo/waves/round-23/sources/r22-rough-census.txt`, `sources/r22-closure.json`), the preregistration and the
landed round-23 lesson. Read-only. NO-EXEC honoured: nothing was executed, imported, compiled, hashed or
counted by a command; every count below was derived by reading and by targeted grep over file bytes.

## Axes named for this attack

1. **Arithmetic** — do the entry's counts reconcile with the ledger, the audits and the outside numbers?
2. **Event identity** — are the six rough-only events, their seats and their dispositions what the entry says?
3. **Classifier faithfulness** — is the quoted rough regex the one actually re-authored, and does the stated
   canonical grammar exist as described?
4. **Subset / arithmetic identity** — is "retained ⊂ rough" true at site level, and is
   `rough − retained = selector-normalization − Σ(unit extra)` the identity the gate enforces?
5. **Honest saturation** — does the entry claim only what the instrument proves (no enforcement, no effects,
   no retroactive authorization), and do the selftest/mutant claims match the recorded artefacts?
6. **Frontier** — is any part of the entry a *new* claim (rather than calibration of two historical counting
   methods) that the landed state does not support?

## Claim ledger — attacked claim, falsifier or bounded search, verdict

| # | Attacked claim | Falsifier / bounded search performed | Verdict |
|---|---|---|---|
| C1 | Table counts: build rough 25 / retained 23 / agree 376 / selector-norm 2 / unit-diff 0 / unexplained 0; falsify 33 / 29 / 991 / 4 / 0 / 0; events 378 and 995 | Read ledger `totals` blocks (`path-reconciliation.json:4970-4976` build, `:17979-17985` falsify): byte-identical to the table. Independently recounted from ledger rows by grep over the whole file: exactly **25** build rows with `"rough_category": "path"` (23 of them `retained_path_count: 1`, 2 with `retained_path_count: 0`), exactly **33** falsify `"path"` rows (29 retained, 4 retained-0); 52 retained rows total = 23+29. Independently counted the frozen audits: `build/audit.json` `SCOPE-PATH-DENIED` = **23**; `falsify/audit.json` `SCOPE-PATH-DENIED` = **29**. Event totals: `build/audit.json` classes = PATH 23 + EXEC 2 + TOOL-UNKNOWN 16 = **41**, `falsify/audit.json` = PATH 29 + TOOL-UNKNOWN 17 = **46**, matching `sources/r22-closure.json` recheck `requests378/995, violations41/46`. Outside numbers `rough 25/33`, `lane 23/29` match `preregister.json` `outside_round22.path_counts_as_reported` and `frozen/reconciliation-inputs.json` `expected`. | **HOLDS** (independently reproduced three ways) |
| C1a | "Every event in both fixed cohorts (build 378, falsify 995 recorded requests) was classified twice from the frozen bytes" | Ledger rows carry `tool`, `rough_category`, `rough_first_bad`, `canonical_bad`, `canonical_path_count`, `retained_path_count`, `disposition` for every event; `exec` and `unknown` rows are present (build exec at `:2842` `OracleReceiptCRLF:7`, `:4172` `DebtFetch:5`; build `unknown` rows 16, falsify `unknown` rows 17), so the non-path events are classified, not dropped. `derive()` in the gate enumerates `ev['seats'][*]['events'][*]` with no filter. | **HOLDS** |
| C2 | "All six rough-only events are `read` requests"; sites `DebtSixReceipts:4`, `ReviewReservation:4` (build) and `FxC1Unknown:8/9/10/14` (falsify) | Grep for `"disposition": "selector-normalization"` over the ledger returns exactly six row sites: `:4351` (DebtSixReceipts:4), `:4710` (ReviewReservation:4), `:5768` (FxC1Unknown:8), `:5781` (FxC1Unknown:9), `:5794` (FxC1Unknown:10), `:5846` (FxC1Unknown:14). All six rows carry `"tool": "read"`, `rough_path_count: 1`, `canonical_path_count: 0`, `retained_path_count: 0`, `rough_first_bad: 0`. Frozen snapshot confirms the same six seats/events (`build/events.json` call ids `call_2824ccfabf13434f969518b5`, `call_a6b2165b628a4b4283fde50c`; `falsify/events.json` `toolu_01SCLctdiGzTL9cNPCdfjFYW`, `toolu_01ASiJwaeMcZrphAZyuTztc3`, `toolu_01K3ih69GpJx5agmk4hChSei`, `toolu_01R72arcerJspPr3z3wvNHRL`). | **HOLDS** (dispositions, tool, seat identity) |
| C2a | "The bare path is literally bound for each of those seats" | `build/bindings.json`: `DebtSixReceipts.read_paths` and `ReviewReservation.read_paths` both contain `.../round-22/snapshot/corpus/lessons/round-21.md` — exactly the path those two events read. `falsify/bindings.json`: `FxC1Unknown.read_paths` contains `.../round-22/candidate/tools/check-boundary-contract.py` and `.../round-22/candidate/tools/_revision.py` — the two paths those four events read. Entry's parentheticals ("snapshot round-21 lesson", "round22 candidate tools") match the bound paths. | **HOLDS** |
| C2b | The two inline example spellings `(<path>:raw:58-58`, `<path>:raw:15-60>)` describe the six events | Grep `":raw:"` over the whole frozen snapshot tree returns exactly six occurrences, with **five** distinct spellings: `round-21.md:raw:58-58` (build ×2), `check-boundary-contract.py:raw:15-60`, `check-boundary-contract.py:raw:58-102`, `check-boundary-contract.py:raw:103-175`, `_revision.py:raw:172-193` (falsify ×4). Four of the six events therefore use a range the entry never names. | **FAILS** (see D1) |
| C3a | "The retained findings are a strict subset of the rough ones; no retained site is missing from the rough set and no retained finding is orphaned" | All 52 rows with `retained_path_count: 1` (23 build at ledger `:521`…`:4634`, 29 falsify at `:5640`…`:16954`) also carry `rough_category: "path"` and `rough_path_count: 1` — no retained site lacks a rough flag. Both cohorts carry `orphan_retained_sites: []`. Counts differ (25≠23, 33≠29) so the inclusion is strict. Gate enforces both (`RECONCILIATION-ORPHAN-FINDING` on orphans, `RECONCILIATION-LEDGER-MISMATCH` on ledger≠recomputation; selftest cases `orphan-retained`, `dropped-row`, `duplicate-row`, `forged-disposition`). | **HOLDS** |
| C3b | "no event had more than one denied component" | Grep for `"[a-z_]*_path_count": [2-9]` over the whole ledger: **no matches**; likewise no `"rough_first_bad": [1-9]`, no `"disposition": "unexplained"`, no `"disposition": "unit-difference"`. Maximum component count anywhere is 1. | **HOLDS** |
| C3c | "The 2- and 4-event gaps are therefore entirely selector normalization" — arithmetic identity `rough − retained = selector-normalization − Σ(unit extra)` | 25−23 = 2 = 2−0; 33−29 = 4 = 4−0. The gate computes the same identity (`totals['rough_path'] - totals['retained_path'] != totals['selector-normalization'] - unit_extra` → `RECONCILIATION-ARITHMETIC`), and the selftest carries `wrong-arithmetic-total`. | **HOLDS** |
| C4 | The quoted rough regex `:(raw\|\d[\d\-+,:]*\|-\d+\|\d+-)(:raw)?$` is the outside rule, "strips only a trailing range or a trailing `raw`", so `:raw:N-M` leaves `<path>:raw` | `tools/check-path-reconciliation.py` `ROUGH_SUFFIX` is byte-identical to the entry's quote and to `strip_sel` in `sources/r22-rough-census.txt` (S085). Hand-trace of the anchored alternation on `<path>:raw:58-58`: the `raw` alternative fails the `$` anchor at the first colon, the scan advances, `\d[\d\-+,:]*` matches `58-58` at the second colon, so the strip yields `<path>:raw` — matching the entry. The gate's own literal unit control `rough-misses-raw-first` asserts the rough rule flags `a:raw:1-2` as `('path', 0)`, and `rough-strips-range-raw` asserts `a:1-2:raw` is `clean`. The six ledger rows confirm `rough_category: "path"` with `rough_first_bad: 0` and canonical/retained clear. | **HOLDS** |
| C5 | "The canonical selector grammar accepts `raw`/`img`/`conflicts` and range tokens in any order" | `tools/check-path-reconciliation.py:75-83`: `_selector_token` = `token in ('raw','img','conflicts') or all(re.fullmatch(r'\d+(?:[-+]\d*)?\|-\d+', part) …)` and `canonical_base` docstring "Local selector grammar: any order of raw/img/conflicts and line-range tokens after the path", returning `base` when all tokens validate. `tools/check-seat-bindings.py:52-55` carries the identical token rule. The six events' `:raw:N-M` selectors are therefore canonical-clear, matching `canonical_bad: []` in the ledger. | **HOLDS** |
| C6 | Reconciliation-contract bullets (pin by SHA-256; exit 2 on changed/missing snapshot; recomputation must equal the recorded ledger; rough/retained totals must equal 25/33 and 23/29; canonical = retained; no orphan; arithmetic identity) | `evaluate()` in the gate returns `2 / CANNOT_EVALUATE` with `SNAPSHOT-MISSING` and `SNAPSHOT-TAMPERED` for missing/changed pinned bytes; `cohort_findings()` emits `RECONCILIATION-ROUGH-COUNT`, `-RETAINED-COUNT`, `-CANONICAL-MISMATCH`, `-ORPHAN-FINDING`, `-ARITHMETIC`, `-UNEXPLAINED`, `-LEDGER-MISMATCH`; `evaluate()` also enforces ledger schema, cohort roster and `inputs_sha256` identity against the pins file. `frozen/reconciliation-inputs.json` pins all seven inputs (events/bindings/audit per cohort plus `sources/r22-rough-census.txt`) by SHA-256. Every contract bullet maps onto an implemented check. | **HOLDS** |
| C7 | "The gate's literal selftest includes mixed `:raw:range` order, per-component units, forged dispositions, dropped/duplicate rows, tamper and orphan controls" | `selftest()` in the gate contains exactly those case names: `mixed-raw-range-order`, `one-per-event-vs-per-component`, `unit-count-mismatch`, `forged-disposition`, `dropped-row`, `duplicate-row`, `wrong-arithmetic-total`, `snapshot-tampered`, `orphan-retained`, plus `selector-but-retained`, `offsetting-pair-net-zero`, `wrong-rough-total`, `wrong-retained-total`, `agree-clean`, `ledger-missing`, `ledger-duplicate-key`, `ledger-wrong-pins`, `event-roster-forgery`, `non-path-events`; and unit controls `rough-misses-raw-first`, `rough-strips-range-raw`, `rough-break-first`, `canonical-both-orders`, `canonical-components`, `canonical-invalid-token-denied`, `canonical-dot-denied`, `write-no-selector-strip`. | **HOLDS** |
| C8 | "the recorded L1 mutants (`.ufo/waves/round-23/measure/l1-mutation.json`) are all killed" | The file's `results` array holds 27 entries; grep for `"killed": false`, `"exit": 0`, `"selftest": "PASS"` over it returns **no matches**; the file's own summary reads `killed: 27, total: 27`. Mutant 0 of `check-path-reconciliation.py` is precisely the `ROUGH_SUFFIX` widening (`(:raw)?:(raw|…)`) that the entry's regex claim depends on, and it is killed. The file also discloses three survivors that were fixed before recording (`survivors_fixed_before_record`), so "the recorded mutants are all killed" is accurate as written. | **HOLDS** |
| C9 | Frontier/honesty disclaimers: "not native runtime enforcement, effects/read proof, retrospective authorization, an instruction to repair old receipt text, or a general shell/URL/Markdown/Git theorem"; "Row creation itself is neither expansion nor a quality-trend improvement" | Consistent with the gate's own docstring and `SCOPE` constant ("never executes the retained outside source cell, never reauthorizes an old event and is not native runtime enforcement, effects proof or a universal selector theorem"), with `preregister.json` `limits` ("No native per-seat restrictive tool interface exists", "No historical manifest/report rewrite or retrospective authorization") and with the landed lesson's outside disposition (quality unchanged, three bounded instruments admitted, not enforcement). The entry introduces no new runtime capability. | **HOLDS** |
| C10 | "Before round23 the two cohorts had no event-level explanation" | Consistent: `sources/r22-closure.json` recheck says the outside census was "approximate own path-binding census 25/33 vs checker23/29 (selector-normalization differences, **not decisive**)" — the outside suspected selector normalization but produced no per-event proof. | **HOLDS** (see D8: the outside anticipation could be cited) |
| C11 | QUALITY attribution sentence ("QUALITY9/19/36/41/42/46–48/51 require bounded searches, exact source/policy attribution, independent literal cases, predeclared byte identities and preservation of failures") | The QUALITY clause text is not in this seat's bound read set, so the clause→requirement mapping is **unverified** (gap G3). The landed lesson attributes R23-PATH-UNIT to QUALITY9/19/36/41/46 and R23-RAW-ORDER to QUALITY51 — consistent with, not contradicting, the entry's list. | **UNVERIFIED** |

## Findings by severity

### D1 — MEDIUM — the two inline example spellings do not describe four of the six rough-only events

- Attacked claim (C2b): "All six rough-only events are `read` requests whose selector puts `raw` before a line
  range (`<path>:raw:58-58`, `<path>:raw:15-60`)."
- Evidence: the only six `:raw:` occurrences in the frozen snapshot are
  `…/round-22/snapshot/corpus/lessons/round-21.md:raw:58-58` (build ×2),
  `…/round-22/candidate/tools/check-boundary-contract.py:raw:15-60`,
  `…/round-22/candidate/tools/check-boundary-contract.py:raw:58-102`,
  `…/round-22/candidate/tools/check-boundary-contract.py:raw:103-175`,
  `…/round-22/candidate/tools/_revision.py:raw:172-193` (falsify ×4).
  Only two of the six events use one of the two spellings the entry prints; the ranges `58-102`, `103-175` and
  `172-193` are never mentioned. As written the sentence reads as an exhaustive spelling list, which it is not.
- Why it matters: this is the entry's only literal rendering of the six events; a reader auditing the
  reconciliation would try to re-find three of the four falsify events in the snapshot and fail, which reads as a
  missing event even though the dispositions and counts are correct.
- Bounded search that found no defect in the substance: every other element of the sentence (all six are `read`
  requests; `raw` precedes the range in every case; the rough rule flags all six; canonical and retained clear
  all six; the bare paths are bound) is confirmed by the ledger rows and the frozen bindings.
- Smallest in-scope remedy: in the same sentence, either print all five distinct spellings, or mark the two as
  examples and point at the six ledger sites, e.g. "(`…round-21.md:raw:58-58` ×2; `…check-boundary-contract.py:raw:15-60`, `:raw:58-102`, `:raw:103-175`; `…_revision.py:raw:172-193`; ledger rows `DebtSixReceipts:4`, `ReviewReservation:4`, `FxC1Unknown:8/9/10/14`)".
  No count, disposition or contract statement changes.

### D2 — LOW/MEDIUM — `agree` (1367 of 1373 rows) is undefined in the entry's own disposition glossary

- Attacked claim: the contract bullet "one disposition: `agree`, `selector-normalization` (…), or
  `unit-difference` (…). Anything else is `unexplained`." and the table column "Agree events 376 / 991".
- Evidence: the gate implements `agree` as `rough_count == len(canonical) == kept`
  (`tools/check-path-reconciliation.py`, `derive()`), i.e. *agree covers both "both classifiers found nothing"
  and "both flagged the same single component"*. The 52 retained violation rows (23 build, 29 falsify) are
  themselves `agree` rows, and so are the 18 build / 17 falsify non-path events (`exec`, `unknown`).
  The entry glosses only the two non-`agree` dispositions.
- Impact: a reader who reads "Agree events 376" as "376 events with no violation found" concludes that 376+23 =
  399 build events, contradicting the entry's own 378 and its "no event had more than one denied component".
  The entry's arithmetic is right; the vocabulary is what is missing.
- Smallest in-scope remedy: add the missing gloss to the same bullet — "`agree` (rough, canonical and retained
  counts are equal: all zero, or one denied component each)". No number changes.

### D3 — LOW/MEDIUM — "2 exec" is not attributed to a cohort; under the natural per-cohort reading it contradicts the admitted closure

- Attacked claim: "The other retained reds (16/17 unknown-tool, 2 exec) are untouched by this reconciliation and
  stay red."
- Evidence: `frozen/snapshot/r22/build/audit.json` classes are `SCOPE-PATH-DENIED` 23, `SCOPE-EXEC-DENIED` 2,
  `SCOPE-TOOL-UNKNOWN` 16 (total 41); `falsify/audit.json` classes are `SCOPE-PATH-DENIED` 29,
  `SCOPE-TOOL-UNKNOWN` 17 and **no exec class** (total 46); `sources/r22-closure.json` recheck states
  `violations41/46` and `bash exactly2 (build only)`. So the parenthetical is correct only if "2 exec" means
  *build only*; read as per-cohort it yields falsify 29+17+2 = 48 against the closure's 46.
- Smallest in-scope remedy: write "build: 16 unknown-tool + 2 exec; falsify: 17 unknown-tool, 0 exec" and cite
  `sources/r22-closure.json` `violations41/46` so the residual reds are checkable in one line.

### D4 — LOW — the disposition glosses are looser than the predicates the gate actually enforces

- Attacked claim: "`unit-difference` (rough counts one event, canonical and retained count more than one
  component)" and "`selector-normalization` (rough flags, canonical and retained clear, and the rough-stripped
  spelling differs from the canonical base)".
- Evidence: the implemented predicates are `rough_count == 1 and kept == len(canonical) > 1 and first_bad ==
  canonical[0]` (unit-difference) and `rough_count == 1 and kept == 0 and not canonical and tool in
  ('read','grep') and ROUGH_SUFFIX.sub('', component) != canonical_base(component, True)` (selector-normalization).
  The entry omits `first_bad == canonical[0]` and the read/grep restriction.
- Impact: none on these cohorts (unit-difference 0, and the six selector rows are reads), but the glossary is the
  contract a future cohort would be judged by.
- Smallest in-scope remedy: mirror the two predicates in the bullet (one added clause each).

### D5 — LOW — the second classifier is not literally "canonical literal v1 authority": remote/fetch spellings are excluded from path classification, undisclosed

- Attacked claim: "Every event … was classified twice from the frozen bytes: once by the outside rough rule …
  and once by canonical literal v1 authority."
- Evidence: the reconciliation's canonical classifier (`canonical_event`) *skips* components matching
  `^https?://` or `^[^/:\s]+:[0-9]+/` ("fetch spellings are a separate class") and special-cases
  `skill://godspeed`, whereas the v1 authority in `tools/check-seat-bindings.py` classifies the same spellings as
  `SCOPE-FETCH-DENIED` (visible in the recorded mutant 8 of that tool). The rough rule, by contrast, treats an
  unstripped URL as an unbound path. The two classifiers therefore do not judge the same class of value.
- Bounded search that found no count impact: no ledger row is affected — the only fetch-spelling row in the
  cohorts (`OracleFetchHTTPS:2`, an `edit` tool call with an `https` path) is rough `unknown` and canonical
  skipped, and there are **no** `unexplained` rows and no row with `rough_first_bad != 0`, which is what a
  rough-flags-URL/canonical-skips-URL row would have produced.
- Smallest in-scope remedy: one clause in the Finding paragraph noting that URL/fetch spellings are excluded
  from path classification on both sides of this comparison and are not counted here.

### D6 — LOW — `call_id` is not a unique event identity in the frozen cohorts

- Evidence: `build/events.json` seat `OracleFetchHTTPS` records three entries sharing
  `call_id: toolu_018MtbybV9AAieTGyATnJU97` (one `edit`, one `read …:raw`, one `write`) with two
  `"origin": "additional-recorded-start"` markers; the ledger faithfully reproduces the same `call_id` on rows
  `OracleFetchHTTPS:3` and `OracleFetchHTTPS:4` with different `request_arguments_sha256`.
- Impact: the entry's contract bullet says "Enumerate every seat/event with its call ID and argument digest" —
  fine as written, but a reader may treat the call ID as the primary key.
- Smallest in-scope remedy: state that the site (`seat:index`) plus the argument digest is the identity and that
  a call ID may cover several recorded starts.

### D7 — INFO — the outside closure had already named selector normalization before round 23

- `sources/r22-closure.json` recheck: "approximate own path-binding census 25/33 vs checker23/29
  (selector-normalization differences, **not decisive**)". The entry's "Before round23 the two cohorts had no
  event-level explanation" is accurate, but the entry does not acknowledge that the outside reviewer had already
  attributed the gap to selector normalization while declining to call it decisive. Citing that makes the
  round-23 contribution (event-level proof) rather than the attribution itself the new ground.
- Remedy (optional, one clause): cite the outside phrase where the entry states the gap.

### D8 — INFO — a bound read path in this seat's binding does not exist; the entry's cited path does

- The seat binding lists `.ufo/waves/round-23/candidate/.ufo/waves/round-23/measure/l1-mutation.json`; that path
  does not exist. The recorded mutant file is at the wave root, `.ufo/waves/round-23/measure/l1-mutation.json`,
  which is the path the entry itself cites — so the entry is right and the binding is stale.
- Remedy: none inside the entry; recorded here so the wave owner can correct the binding.

## Verification gaps (not defects)

- **G1 — no execution.** NO-EXEC forbids running `tools/check-path-reconciliation.py`, so the contract's
  strongest sentence — "A cohort counts as explained only if the recorded ledger equals the recomputation
  exactly" — is **not** verified by this seat. What was verified by reading: the ledger's `totals` blocks are
  arithmetically reproducible from the ledger's own rows (25/23 and 33/29 path and retained counts recomputed by
  enumerating row classes), the ledger's cohort/row/totals key sets match exactly what `derive()` produces (so
  `recorded != derived` is a meaningful comparison), the six selector rows match the frozen snapshot call ids and
  argument digests, and every row-level count is ≤ 1. The remaining unverifiable link is byte-identity of the
  ledger with a fresh `derive()` run and of `inputs_sha256` against the pins file.
- **G2 — the reviewed digest is supplied, not computed.** Per the seat rule no hashing/list/wc was run; the
  `Reviewed-SHA256` line below is the identity handed to this seat.
- **G3 — QUALITY clause text** (QUALITY9/19/36/41/42/46–48/51) is not in this seat's bound read set, so the
  entry's QUALITY attribution sentence is unverified; the landed lesson's own attribution is consistent with it.
- **G4 — MANIFEST entry rounds[422]** itself was not read (not in the bound read set); only the lane's copied
  packet `sources/r22-closure.json` was used, so all outside numbers here are as copied.
- **G5 — scope note.** To attack the entry's own sentences this seat read, read-only, the files the entry itself
  cites or that its `recheck:` line names: `tools/check-path-reconciliation.py`, `tools/check-seat-bindings.py`
  (grammar line only), `.ufo/waves/round-23/path-reconciliation.json`,
  `.ufo/waves/round-23/measure/l1-mutation.json`, `.ufo/waves/round-23/frozen/reconciliation-inputs.json` and
  `.ufo/waves/round-23/snapshot/r22/**`. No command was run, nothing was fetched, no state outside this report
  file was written, and no production/VCS/ref/route file was touched.

## Bottom line

The reconciliation entry's load-bearing content survives this attack: the table counts are independently
reproduced from the ledger rows, from the frozen r22 audits and from the copied outside closure; the six
rough-only events are exactly the six `selector-normalization` rows with the seats and tools stated; the strict
subset and the arithmetic identity hold per row and per cohort; the quoted rough regex is byte-identical to the
re-authored rule and to S085 and behaves exactly as the entry explains; the canonical selector grammar exists as
described; and every reconciliation-contract bullet maps onto an implemented check with a literal selftest case,
with all 27 recorded mutants killed. No falsifier was found for the counts, the six events, the strict-subset
claim or the regex explanation. What did fail is precision in four places (D1 most materially: the printed
spellings do not cover four of the six events) plus two undisclosed classification details (D3 cohort
attribution of the exec reds, D5 the fetch-spelling class). Each remedy is a one-clause edit inside the entry's
existing sentences; none of them changes a count, a disposition, a contract clause or the frontier claim, and
none requires touching the ledger, the gate, the mutant record or any production file.

Reviewed-SHA256: 7661f37ab6b40668ec025b2a68f86791784ef296eccba7a458a6862dde89c3fc
Predicate: r23f-fxknowreconcile
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
