# FxKnowEdit — falsification of the round23 structured-edit knowledge entry

Target: `.ufo/waves/round-23/candidate/corpus/knowledge/structured-edit-r23.md` (landed candidate copy; the declared digest is the supplied identity and was not recomputed — this seat is NO-EXEC/NO-FETCH and ran no hash, list, count or any other command).
Landed state under attack: 5a25c88b77f52e940bcad87825c4ac1cd529470d. Round baseline in the entry's frontmatter: ae01e50f582016384e620022be38bf5367000e2e.

Files read (all inside this seat's declared read set): the target entry (whole file, 33 content lines), `.ufo/waves/round-23/preregister.json` (whole file), `.ufo/waves/round-23/candidate/corpus/lessons/round-23.md`, `.ufo/waves/round-23/candidate/.ufo/waves/round-23/measure/l1-mutation.json` (whole file, raw), `.ufo/waves/round-23/sources/r22-closure.json`, `.ufo/waves/round-23/sources/godspeed-directive.txt`, and one directory listing of `.ufo/waves/round-23/` used only to confirm the existence of the declared preregister path. No other filesystem search, no command, no fetch, no delegation.

Attacked claims (C1/C2/C3/frontier): **C1** (eight finite structured-edit authority decisions, landed as the knowledge entry) and its QUALITY paragraph; **C2** is touched only where the entry states v2 edit authority; **C3** and the frontier claims are out of this seat's target and were not attacked.

---

## Findings by severity

### F1 — High. The `Evidence` column asserts source grounding for six of eight rows that the source never observed; the entry's own first paragraph refutes it.

Claim attacked: the decision table's `Evidence` column (all eight rows = `S086`) and the entry's QUALITY sentence "with observed source metadata separated from normative authority"; the same overclaim is in the preregister's C1 scope, "Eight finite source-grounded structured-edit authority decisions".

Evidence.
- Entry line 7 (the entry's only permitted description of S086): "The source observes structured `edit` requests with a `path` field and either `stream_content` or `old_string`/`new_string` argument keys. Body values are deliberately omitted. Recorded native steps include report reads/writes under the same parent call ID. These observations establish those finite metadata shapes, not universal editor semantics or proof of effects."
- Entry lines 15–22: every row's `Evidence` cell is `S086`, including `UNDECLARED_EDIT`, `READ_ONLY_EDIT`, `WRITE_ONLY_EDIT`, `OPAQUE_PATCH`, `EDIT_TRAVERSAL`, `EDIT_EXTERNAL`.
- `.ufo/waves/round-23/preregister.json` → `edit_decisions` is a list of `[id, decision, reason]` triples only. It carries **no** per-row source mapping, and its `sources_opened` entry for S086 is "prospective: observed structured edit request keys and recorded adapter steps".

Bounded search performed: I enumerated the observation classes the entry itself attributes to S086 — one `path` field, two argument-key shapes, recorded native report read/write steps under a parent call ID — and looked for a matching observed class in the eight row subjects. Found none for six rows: the source observed no undeclared edit, no read-only edit, no write-only edit, no opaque patch, no dot-segment/alternate spelling, and no URI/remote target. The `Policy` column already carries the real warrant (`round23-preregister`); the `Evidence` column therefore repeats a source pointer where an observation is claimed.

Falsifier (not executable from this seat, see gap G1): reading `.ufo/waves/round-23/sources/structured-edit-observations.json` and finding an actual recorded instance of an undeclared / read-only / write-only / opaque / traversal / URI edit would refute this finding.

Smallest in-scope remedy: split the column into `Source fact (S086)` and `Policy (preregister edit_decisions[i])`; put the observed shapes only in the rows they actually ground and mark the other six `policy-only; no S086 observation`; and qualify the preregister C1 scope from "source-grounded" to "source-anchored argument-key shapes, policy-defined rows" (or drop the qualifier).

### F2 — High. "The eight finite policy decisions are falsifiable" and the demanded per-row controls are not backed by any landed instrument; the landed C1 check is document-versus-constant self-consistency.

Claim attacked: QUALITY paragraph, sentences 1–2: "The eight finite policy decisions are falsifiable … Independent literal positive/negative controls must check every row, source/policy mapping and refusal class; source-only opinions are not empirical runs." and "QUALITY42/46–48 require frozen inputs, actual request precedence and honest incomplete evidence."

Evidence.
- Preregister C1 metric is `validated_edit_decisions`, before 0 → target 8, command `python3 tools/check-edit-contract.py --revision <REV>`. A count of eight, produced by a document checker.
- `.ufo/waves/round-23/candidate/.ufo/waves/round-23/measure/l1-mutation.json`, `check-edit-contract.py` mutant 1: original `if declared != [list(e[:3]) for e in EXPECTED]:` — the table is compared field-by-field against the tool's own hardcoded `EXPECTED` constant. Mutant 5: `correct = (row is not None and set(row) == {'id', 'decision', 'reason', 'evidence', 'policy'}` — the row *key set* is checked; the mutation record contains no mutant that constrains the *values* of the `evidence` and `policy` cells. Mutants 2/3: `return shapes == {frozenset(s) for s in SHAPES}` — shape discrimination is set-level, not per-row. The record's own `survivors_fixed_before_record` states: "edit-contract per-row shape check: redundant with shape-set equality, removed".
- Preregister C2 metric is `structured_edit_mode` 0→1 (a mode flag; `check-seat-bindings.py` mutant 7: `result['structured_edit_mode'] = int(code != 2)`), not a per-row refusal-class table.

Reading: the landed discriminating surface is (a) table vs. the tool's own constant, (b) argument-shape set vs. a constant, (c) row key set, (d) a `scope` field and a prose-limit string, (e) one provenance row (`found[0][2:4] != ['own-work', 'A']`, `found[0][7] != 'mined'`). A document that restates the tool's constant is *validated* in the sense of "restated correctly"; that is not falsifiability of the eight decisions, and no literal positive/negative control pair (a synthetic request per row and its expected class ALLOW/DENY/UNKNOWN/CHECK_EACH) is evidenced anywhere in the declared files. Preregistered C1 scope itself concedes the instrument is "new document contract, not eight repaired runtime behaviors" — so the entry's QUALITY sentence, read literally, overclaims the landed instrument.

Falsifier (gap G2): a landed artifact that runs one literal positive and one literal negative control per row and records a refusal class per row would refute this finding.

Smallest in-scope remedy: make the QUALITY sentence describe what the landed check actually discriminates ("the checker's discriminating surface is table-constant equality, shape-set equality, row key set, scope field and prose limit"), and move "literal positive/negative controls must check every row … and refusal class" into a requirement attached to a named, preregistered control artifact (or delete it). The entry's closing clause "no unrun result is asserted here" stays true only if the requirement is not phrased as a satisfied property; "are falsifiable" must go.

### F3 — Medium. The document whose thesis is source-vs-policy separation stores source and policy in a single frontmatter field.

Claim attacked: the entry's separation claim, at the machine-readable level.

Evidence: entry line 1 is one key: `source: S086 — .ufo/waves/round-23/sources/structured-edit-observations.json, observations argument_keys/path/recorded_starts; policy: .ufo/waves/round-23/preregister.json edit_decisions`. A frontmatter reader gets key `source` with a compound value and **no** `policy` key. The checker's own contract is key-based (`data.get('scope') != LIMIT`, mutation record `check-edit-contract.py` mutant 4), so key-level separation is exactly what the machine contract consumes.

Falsifier: an artifact showing the checker parses this line as two keys (e.g. a declared frontmatter grammar that splits on `; policy:`) would refute this.

Remedy: two frontmatter lines — `source: S086 — …` and `policy: .ufo/waves/round-23/preregister.json#edit_decisions` — and give the `Policy` column a per-row pointer (`edit_decisions[0]` … `edit_decisions[7]`).

### F4 — Medium. Two of the eight rows are not decidable from the document, and the demanded "refusal class" control cannot discriminate for one of them.

Claim attacked: bounded procedure step 2 ("with only separately allowed metadata keys"), step 3 ("Unknown means could-not-evaluate or rejection, never permission"), and the QUALITY demand for controls on "refusal class" and "actual request precedence".

Evidence.
- The set of "separately allowed metadata keys" is never enumerated anywhere in the entry, while the landed seat-binding checker treats the harness key `i` as permissible: `if not isinstance(args, dict) or set(args) - {'i'} not in EDIT_SHAPES:` (mutation record, `check-seat-bindings.py` mutant 5). An auditor implementing from the entry alone cannot decide whether `{path, old_string, new_string, i}` is a valid shape; the entry is silent on a key the tool allows.
- Step 3 merges two semantically opposite events into one recorded value: an opaque patch the auditor *refused* to infer a target for, and an opaque patch the auditor *could not evaluate* (recorder gap or missing capability). The `OPAQUE_PATCH` row's decision value is `UNKNOWN` (preregister `edit_decisions[4]`), so the recorded outcome is identical for a policy-conformant refusal and for an evidence gap. The QUALITY paragraph nonetheless demands literal controls that check "refusal class" for *every* row.
- No precedence rule: the entry never says which row governs when several match one request, and never says what the event-level verdict is for `EXPANSION` (`CHECK_EACH`) when the frontend is `DECLARED_EDIT` and one backend step is out of binding. Step 4 says a valid frontend target "cannot clear an out-of-binding backend step", which forbids aggregation into ALLOW but defines no aggregate value.

Falsifier: a per-row control table in a landed artifact (expected class per literal request, including an opaque-patch refusal and an unevaluable case) would refute the decidability gap.

Remedy: (a) enumerate the allowed metadata keys literally in step 2; (b) split `OPAQUE_PATCH` into `REFUSED` and `UNEVALUABLE` recorded outcomes, or state in QUALITY that the row's control covers only the refusal case and that inability is reported separately; (c) add one precedence sentence ("the most specific matching row governs; a DENY-class row beats ALLOW") and one aggregate sentence ("an event verdict is ALLOW only if every in-scope step is in binding; otherwise a violation is recorded independently of the frontend row").

### F5 — Medium. `same parent call ID` is offered as a source observation, but no policy rule defines attribution; `EXPANSION`/`CHECK_EACH` is therefore not evaluable as written.

Claim attacked: entry line 7 vs. bounded procedure step 4, and the `EXPANSION` row's "Every recorded adapter read or write remains separately scoped".

Evidence: the entry states the correlation key as an observation of the source ("Recorded native steps include report reads/writes under the same parent call ID") inside the *source* paragraph, while the policy side never says the auditor may use that key. Step 4 requires auditing "every captured native read/write expansion", but "expansion" is never defined: which backend step belongs to which frontend edit is unspecified. Step 3 forbids gaining authority "by inference", so an implementer cannot lawfully use the parent-call-ID correlation without an explicit rule, and an implementer who does use it is inferring attribution from an unstated rule. Without attribution, the set of steps to be audited per event is undefined, and the `EXPANSION` row has no determinate outcome.

Falsifier: a declared attribution rule (in the entry or in the C2 policy artifact) that maps recorded steps to frontend edits; absent that, the finding stands.

Remedy: one sentence in step 4 — "A recorded native step is attributed to a frontend edit only when it carries that edit's parent call ID; a step with no parent call ID is audited against the seat's global authority; parent-call-ID correlation never grants authority."

### F6 — Low–Medium. The `recheck:` line is an unfilled placeholder with no stated pass criterion, and two different landed hexes are in play this round.

Evidence: entry line 3: `recheck: python3 tools/check-edit-contract.py --revision <landed-hex>`; entry line 2: "verified-at: 2026-10-21; source snapshot baseline ae01e50f582016384e620022be38bf5367000e2e; final gate measurement recorded in SCORECARD". The round-23 lesson records the claims as "landed56c8ba3840cc506e55c1211d7eed0676e69e7ac6", while the integrated landed state under review is 5a25c88b77f52e940bcad87825c4ac1cd529470d — `<landed-hex>` is therefore ambiguous between two live values. The entry states neither the expected exit code nor the expected counts, so even a successful run is not a falsifier of any particular sentence. The SCORECARD pointer names no path and no row (the wave holds a `snapshot/SCORECARD.md` copy, 84.7KB, outside this seat's declared read set — gap G3).

Remedy: fill the hex, and state the pass criterion ("exit 0; validated_edit_decisions = 8; rows = preregister edit_decisions[0..7]"), and cite the SCORECARD path plus the row that carries the C1 measurement.

### F7 — Low. One canonical runtime is not pinned: two physical copies of the checker exist during landing.

Evidence: the wave directory listing shows `candidate/` carrying its own `tools/` tree, while the entry's recheck names a bare repo-relative `tools/check-edit-contract.py`; the mutation record's method line says only "single textual mutant per temp copy with tools/_revision.py" and does not state which copy was mutated. If the root copy is stale relative to the candidate copy, the entry's recheck measures a different binary than the one the mutation record characterizes. The `--revision <REV>` argument may already resolve this; the entry does not say that it does.

Remedy: state the root the recheck must run from, or pin the checker's digest, and say explicitly that `--revision` selects the tree under test.

### F8 — Low. The source's snapshot identity is misstated as the round baseline.

Evidence: entry line 2: "source snapshot baseline ae01e50f582016384e620022be38bf5367000e2e", while the r23 lesson records S086 as *prospective* ("S086 prospective: observed structured edit request keys and recorded adapter steps"), created inside round 23 (`.ufo/waves/round-23/sources/structured-edit-observations.json`, 3.5KB, present in the wave). A file created in round 23 cannot be a snapshot of the pre-round baseline commit; the field conflates "round baseline" with "source snapshot identity".

Remedy: write "round baseline <hex>; source S086 recorded 2026-10-21 at .ufo/waves/round-23/sources/structured-edit-observations.json" and let the source's own digest be recorded where the digest is available (not computable by this seat).

### F9 — Low. No rule covers a structured edit nested inside another tool call, and the document's own language invites the outer-call shortcut.

Evidence: the landed seat-binding checker *does* recurse into nested tool calls with the same binding and the same structured-edit flag — `findings.extend(classify(child.get('recipient_name'), child.get('parameters'), binding, depth + 1, allow_structured_edit))` (mutation record, `check-seat-bindings.py` mutant 6) — but the C1 authority document (eight rows + four steps) never says a nested structured edit is decided by the same rows against the same authority. An auditor working from the entry alone can clear the outer, declared call and never examine the inner edit; step 4's "a valid frontend target cannot clear an out-of-binding backend step" speaks to native expansions, not to nested edit requests.

Remedy: one sentence in step 2 or 4 — "A structured edit nested inside another tool call is decided by the same rows against the same authority; a valid outer call never clears it."

---

## Checks that passed (no finding)

- **Decision-table drift:** all eight rows of the entry's table match `preregister.json` → `edit_decisions[0..7]` exactly on `id`, `decision` and `reason` (read both files whole; compared by eye across all eight triples). No id, decision-value or reason drift.
- **Limits honesty:** the entry's limits paragraph ("not native permission enforcement, a sandbox, body/patch interpretation, actual reading or effects proof, complete recorder coverage, or permission for host/package/service/boot actions … Numeric mode availability is not compliance") is consistent with the r22 closure record (C2 admitted as a fail-capable post-hoc detection instrument that "never prevents calls"; `native_per_seat_allowlist=false`) and with the preregister's `limits` list. No overclaim found in the limits paragraph itself.
- **Frontier/saturation claim:** "This deepens held evidence-operability ground, not an uncovered frontier, repertoire addition or outside promotion" matches the preregister's `ordinals`/`ordinal_delta: 0` and the r22 closure trends (expansion unchanged, quality unchanged). This is an honest negative claim, not an overclaim.
- **Separation of the two source-vs-policy layers in the prose:** the second paragraph ("Authority is separately declared lane policy") and the closing limits paragraph are correctly separated in prose; the defects above are in the table's column, the frontmatter, and the procedure, not in that paragraph.

## Residual risk

- F1, F2, F4 and F5 all sit on the same seam: the entry asserts more empirical grounding (per-row source evidence, per-row falsifiability, decidable rows, evaluable expansion) than the landed instruments and the entry's own description of S086 can support. If the entry is read as the C1 "authority" document by a later lane, each of the four will be inherited as fact.
- F2 is the one with external consequence: C1's preregistered metric (`validated_edit_decisions` 0→8) can be satisfied by a document that merely restates the checker's constant, so the "depth" axis gain for C1 is, on this evidence, a document-contract gain and not a decision-validity gain. The preregister's own C1 scope says as much, so the risk is that the entry's QUALITY paragraph re-widens the claim.
- F3/F8 are cheap provenance defects that will propagate into any later corpus index that reads the frontmatter programmatically.
- F6/F7 mean no reader can deterministically re-run the entry's own recheck from the document, so the entry's self-verification is currently a pointer rather than a check.

## Verification gaps (declared, not improvised around)

- **G1** — `.ufo/waves/round-23/sources/structured-edit-observations.json` (S086) is **not** in this seat's declared read set, so F1's decisive test (does S086 contain any observed undeclared/read-only/write-only/opaque/traversal/URI edit?) was not run. My bound is the entry's own paragraph 1 plus the r23 lesson's S086 scope row ("Observed structured path metadata and recorded adapter steps only, not universal tool semantics, native permission enforcement, effects, or reading proof"). A sibling seat holding S086 can close this in one read.
- **G2** — `tools/check-edit-contract.py` and `tools/check-seat-bindings.py` are outside this seat's declared read set, so F2/F4/F9 rest on the mutation record's quoted source lines rather than on the tools themselves. The mutation record shows the discriminating surface of the checkers only through killed mutants; an unmutated branch may exist that I could not see. No tool was read, listed, executed or hashed.
- **G3** — the SCORECARD copy (`snapshot/SCORECARD.md`) and `sources/edit-decision-policy.json` are outside the declared read set, so the entry's "final gate measurement recorded in SCORECARD" clause was not checked against any measurement, and the separate policy artifact was not compared with the preregister's `edit_decisions`.
- **G4** — the QUALITY identifiers cited by the entry (QUALITY1/3/7/19/45, 42/46–48) could not be checked against the criterion catalogue: the catalogue is not in the declared read set. Only the cross-references visible in the r23 lesson (QUALITY1/3, 9/19/36/41/46, 24/31/42/46/47, 38/42/44/48, 51) were observable, and QUALITY7 and QUALITY45 are not among them.
- **G5** — no command, hash, listing, fetch, subagent or delegation was performed; the declared digest is carried as supplied identity, not as an independently computed one.

Reviewed-SHA256: 4e9e79f1ee2f8d5becb039a5669e916c6758860dc9d1a073d61ed9b3fbdd8014
Predicate: r23f-fxknowedit
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
