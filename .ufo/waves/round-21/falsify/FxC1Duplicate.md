# FxC1Duplicate — source-only duplicate contract-class probe

Reviewed-SHA256: 1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7
Predicate: C1-duplicate contract class

## Axes and result

- **Depth / C1:** challenge the invariant that the source contract contains exactly five distinct object-type decision classes. The proposed defect is one additional, otherwise unchanged `commit` decision.
- **Calibration / C3 boundary:** distinguish inspected source branches and supplied byte receipts from unperformed behavioral measurements. This review is not an executed mutation kill, reviewed-byte hash recomputation, non-author closure, or outside promotion.
- **Operability / C2 boundary:** no consumer, CLI, host, ancestry, push, or target-type matrix behavior was exercised or certified.

**Verdict: inconclusive as a behavioral mutation probe because execution was prohibited.** Source inspection predicts rejection of the proposed duplicate by an explicit uniqueness branch; it does not establish an observed kill or survival. No source-level escape was identified for this one proposed duplicate-row fixture.

## Primary bytes and auxiliary dependencies

The primary file is `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/corpus/knowledge/selector-contract-r21.json`, read at lines 1–11. The supplied inventory `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate-files.json`, lines 99–102, records its receipt above at candidate revision `0a14952b59d20179e1c813af58befaecd6992a17`. That digest was read from the predispatch inventory, not independently recomputed. The Reviewed-SHA256 line binds only this primary file.

Auxiliary frozen dependencies, each recorded at the same candidate revision in that inventory:

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-selector-contract.py` — SHA256 `239758b49da4f24415f53adb52cc6833818d0e340f0832d0389416bce50aea50` (inventory lines 89–92). Inspected evaluator, result construction, duplicate selftest, and CLI boundary, lines 17–83 and 100–166.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/corpus/knowledge/selector-contract-r21.md` — SHA256 `b4966a9bcf4ac124a964718b0ed76104e2f07c41b63050dc8bda618ea5136353` (inventory lines 104–107). Inspected lines 1–39, including the five-row table at 17–23 and source-versus-consumer limitations.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/corpus/SOURCES.md` — SHA256 `ef697b7c6b60bf0e5b71e1267f30cda678d5de01abc803b24dcc7dce1b93c3e4` (inventory lines 109–112). The relevant S081/S082 registry rows are at 88–89; they declare the expected versioned URLs, tier A, and mined status. Registry context and the round21 curation paragraph were also inspected. No linked documentation was fetched.

The ExecDecision build draft comparison below is advisory only. Neither draft file is listed in candidate-files.json; neither is a pinned candidate dependency or evidence of production behavior. No live production file was read for the candidate conclusion.

## One proposed mutant — not materialized

Append an exact duplicate of the primary JSON's first decision, preserving the original five decisions, their order, the schema, and source identities. The sole semantic change is a sixth decision with an already-present `class`. The appended row would be:

```json
{"class": "commit", "outcome": "accept-if-landed-and-pushed", "finding": null, "source": "S082", "rationale": "A commit already has the requested type; lane ancestry and origin tracking checks remain separate."}
```

This models a plausible copy/paste or merge duplication without changing any decision outcome or removing a required class. It isolates uniqueness rather than confounding it with a missing class: the proposed class sequence is `commit, tree, blob, tag-to-commit, tag-to-noncommit, commit`; its distinct-class set remains exactly the required set. No scratch fixture was written and no candidate bytes were edited.

## Observed source facts

1. The primary JSON visibly contains the five named classes once each, with the expected outcome/finding pairs (lines 5–9). Its prose companion contains one matching table row for each class (lines 19–23).
2. The frozen checker builds `classes = [row["class"] for row in rows]` at line 50. Lines 51–52 explicitly reject either duplicate classes or a class-set mismatch:
   `if len(set(classes)) != len(classes) or set(classes) != set(EXPECTED):`
   followed by `fail("SELECTOR-CONTRACT-MISMATCH", "exact five unique classes required")`.
3. This branch precedes source-registry checks and per-row scoring. `fail` returns `result(0, ...)` (lines 36–37); `result` defaults to exit code 1 when findings exist and retains `decision_total = len(EXPECTED)` (lines 26–32). Thus the duplicate diagnostic is a contract mismatch, not the `E-REVISION-INVALID` object-refusal value recorded within individual decision rows.
4. A built-in selftest already declares the same append operation: `("duplicate", lambda d: d["decisions"].append(d["decisions"][0]))` (line 115). Lines 119–121 assign expected code 1 and `SELECTOR-CONTRACT-MISMATCH`; lines 125–130 compare the actual code and finding-ID set when that selftest is run. Its existence and assertions were inspected, not executed. It does not assert the exact duplicate detail string or the reported decision count.

## Expected bounded detector and output — source predictions only

The bounded detector is the frozen checker's `evaluate(raw, markdown, registry)` function, using the primary JSON text and the same frozen Markdown and registry texts for all three conceptual states. No import or invocation occurred. A CLI run would additionally depend on revision binding and committed-file reads (checker lines 152–160), which this probe does not evaluate.

| State | Actual detector output | Source-predicted result |
|---|---|---|
| Pristine primary | None; not invoked | Exit 0, `status=PASS`, `decision_rows=5`, `decision_total=5`, no findings, provided the inspected texts are supplied directly to the evaluator. |
| Proposed appended duplicate | None; not invoked | Exit 1, `status=FAIL`, `decision_rows=0`, `decision_total=5`, exactly one `SELECTOR-CONTRACT-MISMATCH` finding with detail `exact five unique classes required`. |
| Exact pristine bytes after conceptual removal | None; not invoked; no actual restoration was necessary | Same predicted result as pristine under the same detector and auxiliaries. |

For the proposed duplicate, six classes versus five distinct classes makes the first line-51 condition true; the second condition remains false. The early return therefore specifically detects duplication rather than merely loss of a required class. The predicted evaluator payload is:

```json
{"status":"FAIL","decision_rows":0,"decision_total":5,"findings":[{"id":"SELECTOR-CONTRACT-MISMATCH","detail":"exact five unique classes required"}],"scope":"five declared source-grounded decisions; not consumer behavior or host health"}
```

This payload is a source-derived expectation, not captured stdout. There is no observed exit code, stdout, stderr, pristine success, mutated failure, or restored success. A failed pristine run would make an executed probe inconclusive; no clean baseline is claimed here.

## ExecDecision build draft — advisory comparison only

Inspected `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/drafts/ExecDecision/check-selector-contract.py` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/drafts/ExecDecision/selector-contract-r21.json` as explicitly requested build-draft advice, not as production or pinned-candidate authority.

The draft uses `schema_version`, `rows`, and separate row `id` fields, unlike the candidate's `schema`, `decisions`, and class-as-row-identity arrangement. Its checker lines 279–283 explicitly reject repeated IDs before enforcing the exact five IDs. An analogous duplicated first row in that draft's own schema is source-predicted to return `FAIL` / exit 1 / `SELECTOR-CONTRACT-MISMATCH`, with detail `decision row IDs are not unique` and `decision_rows=6`. Its selftest declares that duplication at lines 336–338. The candidate instead returns the combined class-uniqueness diagnostic and `decision_rows=0`. These are different implementation/reporting shapes with an explicit duplicate refusal in each; the draft does not establish that the candidate was run. Feeding candidate JSON directly to the different draft schema would not be a valid duplicate-specific comparison.

## Hash and restoration evidence; limits

- **Before:** inventory-supplied primary SHA256 `1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7`; no independent digest computation.
- **Mutated:** no materialized mutant, so no mutated-file digest or behavioral output exists.
- **After/restoration:** this seat performed no write to the primary or auxiliary source files; no restoration operation was needed. Under the immutable-snapshot premise the expected after digest is the same supplied primary SHA256. An after hash was not independently measured, and byte-for-byte restoration is not represented as an executed check.
- **Writes:** only this scoped report. No production/sibling edits, scripts, subprocesses, tests, imports, compilers, network programs, VCS mutations, host probes, installs, or child-agent dispatches. Tool installation/update: none; no tool was needed for source review.
- **Limits:** one proposed duplicate-row defect only. This is a finite source prediction, not general checker correctness, consumer execution coverage, source-document reopening, independent admission, or promotion evidence. No contract change is proposed on the strength of an unrun mutant.

Report: .ufo/waves/round-21/falsify/FxC1Duplicate.md
Scope: executed=none
