# FxC1EditExternal — FALSIFY wave r23 attempt 1 (C1, row EDIT_EXTERNAL → DENY)

Seat: FxC1EditExternal (leaf member; no subagent dispatch, no delegation).
Target: `.ufo/waves/round-23/candidate/tools/check-edit-contract.py` (declared SHA256 `620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081`, supplied by the assignment; **not** independently computed — this seat's NO-EXEC scope forbids hashing, and the digest is treated as declared identity only).
Execution: none. Every claim below is derived from reading the landed tool, corpus, SOURCES registry, preregister and evidence file. No command was run, no subprocess/subprocess-free import/compile/test/lint was performed, no file outside the declared read set was opened.

## 1. Axes named (godspeed)

- **depth (C1)** — `validated_edit_decisions` target 8. Attack axis: does the landed checker *validate the meaning* of the eight decisions, or only their textual presence? This seat attacks row `EDIT_EXTERNAL` only.
- **operability (C2)** — v2 audit authority for exact predeclared edit targets. Touched only at the C1↔C2 seam (URI-valued declared targets); not attacked.
- **calibration (C3)** — path-census ledger. Out of scope for this seat.
- No other axis is claimed. No runtime-enforcement claim is made anywhere in this report: the corpus itself states "The task API still has no restrictive per-seat allowlist" and the preregister limits state "No native per-seat restrictive tool interface exists".

## 2. Attacked claim

**C1 / depth.** Claim under attack: the landed checker counts the row

`EDIT_EXTERNAL | DENY | Remote or internal URIs do not become filesystem edit targets | S086 | round23-preregister`

as a *validated* edit decision, and the C1 metric `validated_edit_decisions = 8` is therefore evidence that eight finite structured-edit authority decisions are validated.

Falsifier sought: the smallest literal knowledge JSON / Markdown / SOURCES / preregister input that the landed `evaluate()` still reports as validated (exit 0, `validated_edit_decisions: 8`, `findings: []`) while the row's *meaning* — "remote or internal URIs do not become filesystem edit targets" — is violated by the corpus it certifies.

## 3. Landed row vs preregistered tuple — exact match, no divergence

| Carrier | Landed content | Preregistered tuple | Result |
|---|---|---|---|
| `corpus/knowledge/structured-edit-r23.json` (`decisions[6]`) | `EDIT_EXTERNAL / DENY / Remote or internal URIs do not become filesystem edit targets / S086 / round23-preregister` | same | identical |
| `corpus/knowledge/structured-edit-r23.md` (table row, line 21) | `\| EDIT_EXTERNAL \| DENY \| Remote or internal URIs do not become filesystem edit targets \| S086 \| round23-preregister \|` | same | identical |
| `.ufo/waves/round-23/preregister.json` (`edit_decisions[6]`) | `["EDIT_EXTERNAL","DENY","Remote or internal URIs do not become filesystem edit targets"]` | same | identical |

So there is **no literal divergence** between the landed row and the preregistered tuple, and none can be created: the JSON row is pinned by value (`check-edit-contract.py:146-147`), the Markdown row by exact cell-equality plus exactly-one-match (`:148-149`), and the preregister list by equality with the tool's own constant (`:135`).

## 4. Bounded search over the checker's decision surface

The checker reads five inputs. Their degrees of freedom after `evaluate()` (`:115-158`) are:

| Carrier | What the checker actually constrains | Residual freedom |
|---|---|---|
| knowledge JSON | schema, exact key set, exactly 8 unique ids, per-row key set `{id,decision,reason,evidence,policy}`, and each of the 5 values equal to the in-tool `EXPECTED` tuple (`:125-127`, `:146-147`) | none — fully pinned |
| knowledge Markdown | (a) exactly one table row whose first cell is each canonical id, equal cell-for-cell to `EXPECTED` (`:148-149`); (b) `PROSE_LIMIT` substring present somewhere in `visible(text)` (`:153`) | **all other prose content is unconstrained** — including non-canonical table rows and any sentence outside the table |
| `corpus/SOURCES.md` | exactly one row with first cell `S086`, 11 cells, source path ends with the evidence path, kind `own-work`, tier `A`, status `mined`, no backslash in cells (`:137-140`) | every other registry row and every other cell of non-S086 rows |
| preregister | `edit_decisions` equals `[list(e[:3]) for e in EXPECTED]` (`:135`) | **every other preregister field** — `claims`, `limits`, `separability`, `sources_opened`, `ordinals` are never read |
| evidence JSON | schema, observation field shapes, `path.startswith(LANE)` and no `/../` (`:104-112`), argument-key shapes exactly the two observed ones (`:112`) | observation count (extra rows allowed), `recorded_starts` contents, `transcript_sha256` values (format-only, never recomputed) |

**Bounded-search result on the canonical channel:** no literal input to the JSON, the canonical Markdown row, or the preregister tuple can keep `EDIT_EXTERNAL` counted as validated while changing its meaning — the row's five cells are frozen against `EXPECTED`. Search closed.

**Bounded-search result off the canonical channel:** the Markdown is only partly constrained, so falsifiers exist there. The two that survive are F1 and F2 below.

## 5. Falsifier F1 (HIGH) — one added Markdown sentence passes as PASS/8

**Smallest falsifying input.** Leave `structured-edit-r23.json`, `corpus/SOURCES.md`, `preregister.json` and `structured-edit-observations.json` byte-identical to landed. Add exactly one line to `corpus/knowledge/structured-edit-r23.md` (anywhere outside the decision table; it must contain no `|`), for example after line 28:

```
A structured edit whose `path` is a remote or internal URI (`https://…`, `skill://…`, `proc://…`, `agent://…`) is materialized under the lane root and edited as an ordinary filesystem path, so a URI target does become a filesystem edit target.
```

**Trace through the landed `evaluate()` with that prose:**

- `:125-128` JSON: unchanged, 8 unique ids, key set exact → passes.
- `:131` `source_path`/`evidence_ok`: unchanged → no `EDIT-EVIDENCE`.
- `:135` preregister: unchanged → no `EDIT-POLICY-SOURCE`.
- `:137-140` SOURCES: unchanged → no `EDIT-SOURCE`.
- `:142-152` row loop: `table_cells(text)` only inspects lines containing `|` (`:88-99`); the added line has none, so it is not a row. The eight canonical rows are untouched, so for `ident='EDIT_EXTERNAL'`, `matches == [list(expected)]` still holds, and the JSON row still equals `EXPECTED` → `count += 1`. `count` stays **8**.
- `:153` limit check: `data['scope'] == LIMIT` still true; `PROSE_LIMIT` (`'It is not native permission enforcement'`, prose line 31) is still present in `visible(text)` → no `EDIT-LIMIT-MISSING`.
- `:155` `code = 1 if findings else 0` → `findings == []` → **exit 0, status `PASS`, `validated_edit_decisions: 8`**.

**Consequence.** The C1 metric reaches its target of 8 on a corpus that states, in the same document, the operational opposite of the `EDIT_EXTERNAL` row. `validated_edit_decisions: 8` is a count of *echoed literals*, not of *validated decisions*; nothing in the checker ever reads the corpus's operative sentences, so the row's reason is asserted and never exercised. This directly contradicts the corpus's own QUALITY paragraph ("The eight finite policy decisions are falsifiable"): no admitted input can make the tool report a URI-target denial, and none can make it report a URI target allowed — the decision vocabulary (`ALLOW`/`DENY`/`UNKNOWN`/`CHECK_EACH`) is never *computed*, only copied.

## 6. Falsifier F2 (HIGH) — one added non-canonical table row passes as PASS/8

Append one row to the Markdown decision table:

```
| EDIT_EXTERNAL_URI | ALLOW | A declared URI target is edited directly | S086 | round23-preregister |
```

**Trace:** `:148` selects rows by `r[0] == ident`. `'EDIT_EXTERNAL_URI' != 'EDIT_EXTERNAL'`, so the `EDIT_EXTERNAL` match set is unchanged, and the new row matches none of the eight canonical ids, so no loop iteration inspects it. `count` stays 8, `findings` empty, exit 0.

**Consequence.** A contradicting, near-duplicate decision row can live in the very table the checker certifies. Note the asymmetry: the JSON carrier *cannot* host this row (`:127` requires exactly eight unique ids), so the Markdown is the only place where a second decision on the same subject can hide — i.e. the strictest carrier is checked and the loosest carrier is the one the metric rests on.

## 7. Falsifier F3 (MEDIUM-HIGH) — the row is unfalsifiable *in principle* under the admitted evidence shape

`evidence_ok` (`:104-112`) admits an observation only if `row['path'].startswith(LANE)` with `LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/'` (`:32`) and no `/../` (`:107`). Therefore:

- The event class the row is about — a structured edit whose target is a **remote or internal URI** — is **not representable** in the admitted evidence. A captured URI-target edit would make the *whole* evidence file fail (`EDIT-EVIDENCE` at `:131`), and any non-mismatch finding forces `count = 0` (`:157-158`), so the audit would report `FAIL / 0` rather than a row-scoped denial of `EDIT_EXTERNAL`.
- The landed evidence file confirms this: all five observations in `.ufo/waves/round-23/sources/structured-edit-observations.json` are lane-local round-22 build reports (`.../round-22/build/CritRuntime.md`, `.../round-22/build/OraclePathArtifact.md`) with filesystem paths and the two observed argument-key shapes. **Zero observations bear on the URI rule.**
- Yet `validated_edit_decisions: 8` counts the URI row as validated. The tool's own docstring says it "Validate[s] eight finite structured-edit authority decisions", and `LIMIT` claims "Declared audit authority for structured target metadata only" — but for `EDIT_EXTERNAL` the coverage is 0/0: there is no observation, no test, and no code path that could ever detect a violation.

`EDIT_TRAVERSAL` shares the structural defect (the `'/../'` rejection at `:107` means dot-segment spellings are likewise unrepresentable), which is why this is a row-family finding, but it is not counted again here.

## 8. Falsifier F4 (MEDIUM) — the preregister check is not an independent authority

`:135` compares `pre.get('edit_decisions')` against `[list(e[:3]) for e in EXPECTED]` — the *tool's own in-source constant*, which is also the thing the corpus JSON (`:146-147`) and the corpus Markdown (`:148-149`) are compared against. All three carriers are pinned to one literal held inside the file under review, so the "preregister" comparison cannot falsify the corpus: it detects drift from the tool, not corpus-vs-preregister divergence in any independent sense. Concretely, the tool never reads `preregister['claims'][0]` (the C1 claim: axis `depth`, metric `validated_edit_decisions`, before 0, target 8), nor `preregister['limits']`, nor `separability`, nor `sources_opened`; a preregister whose C1 target were `3`, whose limits list were empty, or whose `sources_opened` entry for S086 were removed would still yield `PASS / 8`. The assignment's "compare the landed row against the preregistered tuple" step therefore resolves only in the trivial, tool-mediated sense.

Minor related constraint (not a row defect): the registry status for S086 is hard-required to be `mined` (`:138`, `found[0][7] != 'mined'`), so an honestly *queued* S086 could not be represented without failing `EDIT-SOURCE`; the status vocabulary the checker admits is narrower than the registry's own (`queued` is used by S006/S030/S033 in the same file).

## 9. Under-specification of the row itself (MEDIUM, non-tool)

The corpus leaves `EDIT_EXTERNAL` ambiguous between DENY and UNKNOWN for *declared* URI targets:

- Row (prose line 21): "Remote or internal URIs do not become filesystem edit targets" — about filesystem-ness.
- Bounded procedure step 3 (prose line 28): "Missing structured targets, freeform patches, unknown keys, **URI targets** and alternate path spellings never gain authority **by inference**. Unknown means could-not-evaluate or rejection, never permission."
- Step 1 (prose line 26): declared schema-v2 `edit_paths` are "canonical literal subsets of both read and write targets" — no filesystem-only restriction is stated for the binding grammar.

Under step 3 read literally, a URI target that is *declared* rather than inferred is not covered by the "never gain authority by inference" clause, and step 1 admits any declared literal. The row then forbids only *filesystem* targets, so a declared URI edit is neither DENY nor UNKNOWN by the corpus's own vocabulary — it is unspecified. This matters operationally because internal URIs are live in this lane's own authority model (this seat's binding lists `skill://godspeed` among `read_paths`). The checker cannot detect either reading, since it never parses the procedure text.

## 10. Smallest in-scope remedy (for the C1 owner; not applied by this seat)

**R1 — primary, tool-only, closes F1 and F2 without touching the corpus.** In `evaluate()`, after the row loop (`:143-152`), reject decision-shaped content that the eight canonical rows do not own. One check, e.g. flag a finding `EDIT-UNCHECKED-DECISION` when any `visible(text)` line that is not one of the eight canonical rows contains an uppercase decision token (`ALLOW`, `DENY`, `UNKNOWN`, `CHECK_EACH`) as a whole word, and flag `EDIT-EXTRA-ROW` for any table row whose first cell is not one of the eight canonical ids. The landed corpus keeps `PASS / 8` under the tightened checker: a grep of `structured-edit-r23.md` shows those four uppercase tokens occur **only** in the eight canonical table rows (lines 15-22) and nowhere else in the document. One caveat for the implementer: the token test must be case-sensitive as specified, because prose line 28 contains the title-case word "Unknown" ("Unknown means could-not-evaluate or rejection, never permission"), which a case-insensitive variant would trip; either keep the case-sensitive form or add an explicit allowance for that line. With that, this is a pure tightening with no corpus migration and no loss of the landed `PASS / 8`.

**R2 — metric honesty, three literals in two files.** Change the `LIMIT` constant in the tool and the identical `scope` literal in `structured-edit-r23.json` (plus the same literal inside the `selftest()` fixture in the same tool file) from "Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof." to a string that also states that the count denotes eight *textually pinned* decision tuples with no per-row observational coverage. Without this, `validated_edit_decisions: 8` continues to read as eight validated behaviors.

**R3 — F3 closure, corpus sentence.** Add to `structured-edit-r23.md` one sentence recording that the S086 evidence shape admits only lane-prefixed filesystem paths, so the `EDIT_EXTERNAL` (and `EDIT_TRAVERSAL`) rules are declared policy with **zero** admissible observations; a URI-target edit cannot even be recorded without invalidating the whole evidence file. This must be accompanied by R2, otherwise the sentence is not enforced by the metric.

**R4 — under-specification closure (F4/§9).** State explicitly in the corpus whether a *declared* URI-valued `edit_paths` entry is `UNKNOWN` (could-not-evaluate) or `DENY`, and align the row reason with the answer. If the answer is UNKNOWN, the row's decision vocabulary must change and the preregistered tuple must change with it — which, per F4, currently means editing the tool constant as well, so the change should be done as one coordinated edit of tool + corpus JSON + preregister.

## 11. Residual risk and verification gaps

- **No execution.** This seat's binding has `commands: []` and `fetches: []` (NO-EXEC / NO-FETCH). Every falsifier above is a *reading-based construction* with a line-level trace through `evaluate()`; none was run. If the round requires an executed demonstration, it must be run by a seat with command authority — the construction is small (one Markdown line, zero changes elsewhere) and the expected result is exit 0 / `PASS` / `validated_edit_decisions: 8` / `findings: []`.
- **Digest not independently verified.** `620f3e5b…5081` is supplied identity per the assignment; this seat did not hash, list, or import the file to confirm it, per the receipt rule.
- **C1↔C2 seam not checked.** Whether the v2 binding grammar permits a URI-valued `edit_paths` entry is decided in `.ufo/waves/round-23/<WAVE>/bindings.json` and `tools/check-seat-bindings.py`, neither of which is in this seat's declared read set; the §9 under-specification therefore remains open. Named as the exact next check, not asserted either way.
- **Generalization.** F1/F2/F3 are demonstrated on the `EDIT_EXTERNAL` row only; by construction (the loop at `:143-152` is row-agnostic and the prose checks at `:137-140`, `:153` are row-agnostic) they apply identically to the other seven rows. F3's evidence-shape argument applies to `EDIT_TRAVERSAL` for the same reason.
- **No runtime-enforcement claim.** Nothing here asserts or implies that the lane's task API enforces these decisions; the corpus and preregister both state that no restrictive per-seat allowlist exists.

Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxc1editexternal
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
