# FxC1Selftest — falsification of C1 selftest independence (round 23, attempt 1)

Target: `.ufo/waves/round-23/candidate/tools/check-edit-contract.py` (declared SHA256 supplied by seat binding, not computed here).
Method: read-only inspection of the declared files only. NO-EXEC (seat `commands: []`), NO-FETCH, no hashing, no subprocess/import of the target, no subagents (leaf member).

Files read (all inside the seat's declared read set):
`candidate/tools/check-edit-contract.py`, `preregister.json`, `candidate/corpus/knowledge/structured-edit-r23.json`, `candidate/corpus/knowledge/structured-edit-r23.md`, `candidate/corpus/SOURCES.md`, `sources/structured-edit-observations.json`, `sources/godspeed-directive.txt`.

## Attacked claim

**C1** — "Eight finite source-grounded structured-edit authority decisions", measured by `validated_edit_decisions` (before 0 → target 8), command `python3 tools/check-edit-contract.py --revision <REV>`.
Sub-claim attacked (stated in the landed prose, `structured-edit-r23.md:37`): *"Independent literal positive/negative controls must check every row, source/policy mapping and refusal class."*
Secondary sub-claim attacked: the selftest's own header comment at `check-edit-contract.py:166` — *"Independent literal fixture: never synthesized from the evaluator's EXPECTED map."*

C2 (v2 seat-binding edit audit authority) and C3 (path-census ledger) are out of this seat's declared attack and were not attacked; the two files that would carry them (`check-seat-bindings.py`, `check-path-reconciliation.py`) are not in the seat's declared read set.

## Verdict on the stated question: are clean fixtures literal and independent of production EXPECTED?

**Literal — yes. Independent — only in the one-sided sense, and materially incomplete.**

1. `literal` (`:167-176`) is a hand-written transcription, not derived from `EXPECTED` at runtime — the header comment is truthful on that narrow point.
2. But `literal` is a **byte-for-byte twin of `EXPECTED`** (`:20-29`): all 8 ids, decisions, reasons, evidence `S086`, policy `round23-preregister` match field-for-field. The selftest's `pre` witness is then built *from the same twin* (`:189`), so the selftest's "policy-source" case is EXPECTED-vs-literal, not a third independent witness. The genuine third copy — `.ufo/waves/round-23/preregister.json` — is only consulted in production `--revision` mode.
3. Consequence: the selftest is a **unit** test of `evaluate()`. It never loads the landed corpus, the landed `SOURCES.md`, the landed preregister, the landed evidence file, and never calls `main()`, `git_read()` or `_revision.bind()` (`:248-281` are entirely outside the selftest). A selftest PASS therefore certifies "the evaluator agrees with the fixture", not "the landed revision passes".
4. The twin *does* work as a one-sided tripwire: any edit to `EXPECTED` (including the `POLICY` constant at `:22`, which `EXPECTED` embeds) makes the `clean` case fail loudly, because the clean fixture is built from the twin. That is the one real independence property the fixture buys.
5. The twin is **narrower than the landed corpus**: the fixture's evidence has 2 observations (one per shape) and a placeholder `sources` row, while the landed evidence has 4 observations and the landed `SOURCES.md` S086 row has 11 populated cells. Every rule that the fixture happens to satisfy "naturally" is therefore never probed. That is exactly where the weakened rules below live.

Case inventory used for the coverage proof (source-derived, not executed): **68 cases** = 3 (`clean`, `missing`, `missing-prose`) + 8 ids × (4 field mutations + 1 prose id mutation) + 25 hand-written cases (`:195-236`). Coverage of the prose argument across all 68: `None`, whole-prose HTML comment, whole-prose fence, **id** cell rewrite, an extra duplicate row, and two non-table sentence edits. **No case rewrites a prose cell *value*** while keeping the id. This single gap produces findings F1 and F2 below.

## Findings (severity order)

### F1 — HIGH: the prose↔JSON value cross-check is unpinned; a one-line change makes prose/JSON disagreement certify as PASS

*Rule:* `:149` — `if not correct or matches != [list(expected)]:` (with `matches` built at `:148`, `correct` at `:146-147`).
*One-line weakening:* replace `matches != [list(expected)]` with `len(matches) != 1` (i.e. keep "the id appears exactly once", drop "the row equals the expected 5-tuple").
*Why no selftest case detects it:* the only prose mutations are (a) id rewrite (`table-i`, `:203`), which still leaves exactly one row per id, (b) whole-prose hiding (`hidden`, `fenced`), (c) a duplicate row (`quoted-duplicate`, `:218`), (d) sentence edits outside the table (`limit-omitted`, `hidden-limit`). Under the weakening, (a) is still caught (`matches` becomes empty → `len != 1`), (b) still caught (0 rows), (c) still caught (2 rows), (d) unaffected. **No case changes a table cell's value, so the value half of the comparison is never exercised.** All 68 cases still pass.
*Bounded falsifier (concrete, current evaluator rejects it, weakened evaluator accepts it):* leave the JSON untouched and rewrite one prose cell to
`| DECLARED_EDIT | DENY | Exact target is predeclared for edit and for both read and write | S086 | round23-preregister |`
Today: `matches != [list(expected)]` → `EDIT-DECISION-MISMATCH`, exit 1. Weakened: `correct` (JSON) is True and `len(matches) == 1` → no finding, `validated_edit_decisions = 8`, `status = PASS`, exit 0 — the machine-readable authority and the human-readable authority table disagree about DECLARED_EDIT while the tool certifies 8/8.
*Impact on the claim:* the C1 artifact exists in two carriers (JSON + Markdown table) and the only thing binding them is this comparison. A one-line change silently converts the checker into a JSON-only checker, and the "positive and negative controls" prose asserts control over both.
*Smallest in-scope remedy:* add one selftest case that rewrites a single prose cell *value* (keep the id) and expects `EDIT-DECISION-MISMATCH`; optionally assert the prose row against the JSON row directly rather than only against `EXPECTED`.

### F2 — HIGH: the failure-mode value of the preregistered metric `validated_edit_decisions` is never asserted; a one-line change lets a FAIL run report 8

*Rule:* `:159-160` — `if any(f['id'] != 'EDIT-DECISION-MISMATCH' for f in findings): count = 0`, feeding `validated_edit_decisions` at `:161`.
*One-line weakening:* invert the predicate to `f['id'] == 'EDIT-DECISION-MISMATCH'` (or delete `:159-160`).
*Why no selftest case detects it:* the case assertion at `:241` is
`ok = code == expected_code and (expected_id is None or expected_id in ids) and (expected_code != 0 or result['validated_edit_decisions'] == 8)`
— the count is checked **only** when the expected exit code is 0. Every one of the 25 hand-written failure cases and all 40 mutation cases skip the count entirely. So the count's semantics on failure paths are unasserted, and the `clean` case (no findings) is unaffected by the inversion.
*Bounded falsifier:* run the evaluator on a corpus whose eight decision rows are all correct but whose `SOURCES.md` S086 row is wrong (the `source-wrong-tier` shape, `:224`). Today: `EDIT-SOURCE` is raised and `count` is forced to 0 → `{"status":"FAIL","validated_edit_decisions":0}`. Weakened: `count` stays 8 → `{"status":"FAIL","validated_edit_decisions":8}`. The preregister names `validated_edit_decisions` as the C1 metric with target 8 (`preregister.json` claims[0]); a scorer that reads the metric without also gating on `status` would credit C1=8 from a FAIL run. The scorer's read path is **not** in this seat's declared read set, so I cannot close whether `status` is consulted — I report the gap rather than guess.
*Smallest in-scope remedy:* assert `validated_edit_decisions == 0` for the failure cases where all eight rows are correct (e.g. `source-missing`, `evidence-missing`, `limit-omitted`) and `== 7` for a single-row mismatch case, so the metric's failure-mode value is pinned.

### F3 — MEDIUM-HIGH: the evidence transcript-digest format rule is never exercised

*Rule:* `:109` — `not re.fullmatch(r'[0-9a-f]{64}', row.get('transcript_sha256', ''))`.
*One-line weakening:* relax to `r'[0-9a-f]+'`, `r'.{0,64}'`, or drop the clause.
*Why no selftest case detects it:* the fixture's digests are `'a'*64` and `'b'*64` (`:186`, `:188`); the five `evidence-*` mutators touch `body_fields`, `argument_keys`, the observation list, `path` and `tool` (`:227-231`) — **none touches `transcript_sha256`**. Every fixture digest is already valid, so the clause is never the deciding factor in any of the 68 cases.
*Bounded falsifier:* an evidence file with `transcript_sha256: "a"*63` (or `"A"*64`, or `""`) passes `evidence_ok` under the weakened rule and would then be admitted as S086 source evidence for a decision set whose anchor text claims "transcript SHA-256" (`SOURCES.md:93`).
*Smallest remedy:* one mutator setting a 63-char or uppercase digest, expecting `EDIT-EVIDENCE`.

### F4 — MEDIUM-HIGH: the dot-segment guard in the evidence path check is never independently exercised, while `EDIT_TRAVERSAL` is one of the eight certified decisions

*Rule:* `:107` — `or not row['path'].startswith(LANE) or '/../' in row['path']`.
*One-line weakening:* delete `or '/../' in row['path']`.
*Why no selftest case detects it:* the only path mutation is `path='/etc/passwd'` (`:230`), which fails the **earlier** `startswith(LANE)` clause, so the `'/../'` clause is never the deciding term in any case. The rule as written is short-circuit-`or`; removing the third term changes no case outcome.
*Bounded falsifier:* a lane-prefixed but escaping path such as `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/../../etc/passwd` is rejected today by the `'/../'` term; under the weakening it is admitted as valid S086 evidence. The tool would then certify `EDIT_TRAVERSAL → DENY` ("No dot-segment or alternate spelling expands the target list", `structured-edit-r23.md:20`) while its own evidence gate accepts a dot-segment path.
*Smallest remedy:* one mutator with `path = LANE + '../outside.md'` expecting `EDIT-EVIDENCE`.

### F5 — MEDIUM: the evidence document's schema-value check is untested

*Rule:* `:100` — `data.get('schema') != 'tsukuroi-structured-edit-observations-v1'`.
*One-line weakening:* accept any `tsukuroi-*` schema, or drop the comparison.
*Why no selftest case detects it:* no mutator changes the evidence `schema`; the five `evidence-*` mutators (`:227-231`) each trip a *different*, independent clause (`body_fields`, shape set, `path`, `tool`), so removing the schema term leaves all of them still failing for their own reason.
*Bounded falsifier:* an observations document with `schema: "tsukuroi-structured-edit-observations-v2"` (or an unrelated vendor schema) is admitted as S086 evidence under the weakened rule, even though the tool's docstring claims the source "proves only observed metadata shapes" with a versioned carrier.
*Smallest remedy:* one mutator setting the evidence schema to `-v2`, expecting `EDIT-EVIDENCE`.

### F6 — MEDIUM: the policy document's schema-value check is untested

*Rule:* `:125` — `data.get('schema') != 'tsukuroi-edit-policy-v1'`.
*One-line weakening:* accept any schema value.
*Why no selftest case detects it:* the only cases touching `schema` are `duplicate-key` (`:214`, raw `{"schema":1,"schema":2}` — fails in the `unique()` hook at `:36-42`, before the schema comparison) and `extra-top-key` (`:215`, fails on `set(data) != {...}`). **No case carries a wrong schema with an otherwise well-formed top level**, so the schema term is never decisive.
*Bounded falsifier:* a policy document with `schema: "tsukuroi-edit-policy-v2"` is validated under v1 rules, giving no version signal that the authority carrier has moved. That matters for a round whose C2 is explicitly a *v2* authority schema and whose C1 asserts a *v1* policy contract.
*Smallest remedy:* one case with `schema: "tsukuroi-edit-policy-v2"` expecting `EDIT-SCHEMA`.

### F7 — MEDIUM: the duplicate-argument-key sub-clause is untested

*Rule:* `:105` — `len(keys) != len(set(keys))` (the "no repeated argument key" clause).
*One-line weakening:* delete `len(keys) != len(set(keys))`.
*Why no selftest case detects it:* `evidence-unknown-key` (`:229`) *appends* a new key `patch`, which changes the shape set and is therefore caught by `:112` (`shapes == {…SHAPES}`) — a different clause. No case repeats an existing key.
*Bounded falsifier:* `argument_keys: ["path","path","stream_content"]` yields `frozenset(set(keys) - {'i'}) == {'path','stream_content'}` — the same shape — so under the weakening it is accepted, and a recorded request that reported the same key twice is treated as a clean observation of the `stream_content` shape.
*Smallest remedy:* one mutator duplicating a key, expecting `EDIT-EVIDENCE`.

### F8 — MEDIUM: the `recorded_starts` presence/type clause is untested, and it is the only structural support for `EXPANSION → CHECK_EACH`

*Rule:* `:108` — `not isinstance(row.get('recorded_starts'), list) or not row['recorded_starts']`.
*One-line weakening:* drop the `or not row['recorded_starts']` term (accept an empty list).
*Why no selftest case detects it:* the fixture's `recorded_starts` are always non-empty lists (`:185-188`); no mutator touches them.
*Bounded falsifier:* an observation with `recorded_starts: []` is admitted under the weakened rule. `EXPANSION`'s certified reason is "Every recorded adapter read or write remains separately scoped" (`structured-edit-r23.md:22`); the evidence gate is the only place where "recorded steps exist" is enforced at all.
*Smallest remedy:* one mutator setting `recorded_starts: []`, expecting `EDIT-EVIDENCE`.

### F9 — MEDIUM: the revision-binding and read path are outside the selftest entirely (same-identity rerouting risk)

*Untested code:* `git_read()` (`:248-255`), `_revision.bind()` (`:271`), and `main()` (`:258-281`). The selftest calls `evaluate()` directly with in-memory strings (`:239`).
*One-line weakening (illustrative, not present in the landed file): any change to the revision-resolution or path-resolution logic in `git_read`/`_revision.bind` — e.g. resolving a path against the working tree instead of the bound revision, or a fallback that reads the candidate copy — is invisible to the selftest, because no case executes that code.
*Why this matters here:* the scored C1 measurement is exactly the `--revision <REV>` path, and the seat's own review packet is a *candidate copy* under `.ufo/waves/round-23/candidate`. A selftest that only exercises `evaluate()` gives no assurance that the scored run read the bound revision rather than a working-tree file.
*Smallest remedy (scope permitting): one selftest case that exercises the revision read path against a fixture revision, or a `--selftest` case that asserts the resolved binding identity fields.

### F10 — LOW-MEDIUM: the S086 source-row arity rule and the backslash rule are untested

*Rules:* `:138` — `len(found[0]) != 11`; `:139` — `any('\\' in cell for cell in found[0])`.
*One-line weakening:* drop either term. (Changing the constant `11` is caught by the `clean` case — it would make the clean fixture fail — so the *removal* is the undetected form.)
*Why no selftest case detects it:* `source-duplicate` (`:226`) adds a **row** (so `len(found) != 1` fires), and `source-wrong-tier`/`source-rejected`/`source-wrong-path` change **cell values**; no case changes the **cell count** and no case introduces a backslash.
*Bounded falsifier:* an S086 registry row with 10 or 12 cells, or containing a backslash in any cell, is accepted under the weakened rule. A backslash in a path cell is precisely the "alternate spelling" hazard the `EDIT_TRAVERSAL` decision names.
*Smallest remedy:* one case with a short/long S086 row and one with a backslash cell, both expecting `EDIT-SOURCE`.

### F11 — LOW: the non-enforcement limit check is a single substring match and is only pinned in the "phrase absent" direction

*Rule:* `:153` — `PROSE_LIMIT not in '\n'.join(visible(text))`, with `PROSE_LIMIT = 'It is not native permission enforcement'` (`:31`).
*Observation:* the check is a presence test for one substring, and it is satisfied by a single sentence anywhere in the visible prose, in any polarity or negation. `limit-omitted` (`:219`) and `hidden-limit` (`:221`) pin the *removal*/commenting direction, so deleting the check entirely would be caught; but nothing rejects a prose that carries the required sentence **and also** asserts native enforcement elsewhere. The `scope` field of the JSON is likewise compared for exact equality (`:153` first term) but the prose has no contradicting-claim check.
*Consequence:* the C1 artifact's own honesty bound ("never native runtime enforcement", docstring `:2`, `LIMIT` `:30`) is certified by a substring, not by an absence of contradicting claims.
*Smallest remedy:* assert the absence of contradicting phrases (e.g. `native runtime enforcement`, `runtime enforcement`) in the visible prose, and require the limit sentence to be present, not merely present-compatible.

## Residual risk and verification gaps

* **Landed state is statically consistent.** By hand-checking the landed `structured-edit-r23.json` (8 rows, exact key set, `source_path` and `scope` equal to `EVIDENCE`/`LIMIT`), `structured-edit-r23.md` (exactly one 5-cell row per id, values equal to `EXPECTED`; `PROSE_LIMIT` present in visible prose at line 31; no fences/comments), `SOURCES.md:93` (exactly one S086 row, 11 cells, `own-work`/`A` at `[2:4]`, `mined` at `[7]`, path cell ending in `EVIDENCE`, no backslash), `sources/structured-edit-observations.json` (schema ok; 4 observations, all `tool=edit`, unique keys, `body_fields` exact, lane-prefixed paths without `..`, non-empty `recorded_starts`, 64-char lowercase-hex digests, shape union == the two `SHAPES`), and `preregister.json` (`edit_decisions` == the 8 three-element `[id, decision, reason]` triples matching `EXPECTED[:3]`) — the `--revision` run should yield `PASS` with `validated_edit_decisions = 8`. This is a **static read-based conclusion, not an executed measurement** (seat is NO-EXEC; the declared SHA256 was supplied, not computed).
* The 68-case count and all coverage claims above are **source-derived**; no case was executed, and the target was never imported, run, hashed, or linted.
* Whether the scorer that consumes `validated_edit_decisions` also gates on `status` is **outside the declared read set** (F2's impact is therefore stated conditionally, not asserted).
* `_revision.py` (imported at `:12`) is not in the declared read set; the binding semantics behind F9 were not inspected.
* C2 (`check-seat-bindings.py`, v2 edit audit authority) and C3 (`check-path-reconciliation.py`, path-census ledger) were not attacked; the C1 selftest's independence findings do not transfer to them by analogy, and I make no claim about them.
* No native restrictive per-seat tool interface exists in this environment; nothing in this report may be read as runtime enforcement. C1 remains a declared document contract.

## Smallest in-scope remedy, consolidated

One selftest-only change in `candidate/tools/check-edit-contract.py` closes F1–F8, F10 (F9 needs a revision-path case; F11 needs one contradicting-claim case):
1. add a prose-cell-**value** mutation case (F1);
2. assert `validated_edit_decisions` on failure paths (F2);
3. add evidence mutators for `transcript_sha256` (F3), `'/../'` path (F4), evidence `schema` (F5), duplicate argument key (F7), empty `recorded_starts` (F8);
4. add a policy-`schema` case (F6);
5. add S086 cell-count and backslash cases (F10);
6. add a contradicting-claim case for the limit sentence (F11);
7. add one case that exercises `git_read`/`_revision.bind` against a fixture revision (F9).
No production corpus file, `SOURCES.md`, preregister, or evidence file needs to change; the landed C1 content is statically consistent and should not be modified for these findings.

Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxc1selftest
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
