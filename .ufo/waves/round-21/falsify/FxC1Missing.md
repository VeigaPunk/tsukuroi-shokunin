# FxC1Missing — missing-contract and schema source attack

Reviewed-SHA256: 1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7
Predicate: C1-missing contract source

## Axes and boundary

- **Depth / C1:** whether five counted decisions require nonempty decision data, matching prose and the named source registry, rather than passing on an empty denominator.
- **Operability / C2 boundary:** trace the checker entry/read/error branches without claiming any consumer or Git behavior was exercised.
- **Calibration / C3:** distinguish observed source text, source-derived predictions and unmeasured runtime outcomes; bind the primary receipt only to its assigned JSON bytes.

This is a leaf, NO-EXEC, advisory source review. Candidate revision is `0a14952b59d20179e1c813af58befaecd6992a17`; declared baseline is `82e519203e676c532b1dc5ea91a85671f2286e7b`. No source mutation, detector invocation, test, import, subprocess, network program, installation, child dispatch or production edit occurred. No outside admission, promotion or non-author closure is claimed.

## Reviewed bytes and auxiliary dependencies

The primary is `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/corpus/knowledge/selector-contract-r21.json`, lines 1–11. Its five explicit objects contain the expected class/outcome/finding values, both named sources and nonempty rationales.

The following auxiliary snapshots were read. Their predispatch SHA-256 values and common candidate revision come from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate-files.json`, not from a hash program run by this seat:

- **A1, checker:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/check-selector-contract.py`, SHA-256 `239758b49da4f24415f53adb52cc6833818d0e340f0832d0389416bce50aea50`; reviewed lines 1–166.
- **A2, prose:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/corpus/knowledge/selector-contract-r21.md`, SHA-256 `b4966a9bcf4ac124a964718b0ed76104e2f07c41b63050dc8bda618ea5136353`; reviewed lines 1–39, including the five table rows at 19–23.
- **A3, registry:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/corpus/SOURCES.md`, SHA-256 `ef697b7c6b60bf0e5b71e1267f30cda678d5de01abc803b24dcc7dce1b93c3e4`; relied on complete rows S081/S082 at 88–89. Earlier long registry rows were not needed for this predicate.
- **A4, binder:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/tools/_revision.py`, SHA-256 `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf`; relied on lines 54–77 and 172–192 for binding/error precedence, not its unexecuted selftests.
- **A5, round lesson:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/corpus/lessons/round-21.md`, SHA-256 `ab841b2562e41fa69f90b63b8444d5ab47670ce2acf0ec1208f71cf7980349c9`; relied on lines 9–12, 37 and 45–51 for finite scope and pending measurement.
- **A6, gate registration:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/SKILL.md`, SHA-256 `c43477cbb012fe0b0c4170610d4fa034d2e8ae5b09005e3f48a4cccd38f843b3`; relied on lines 2121–2151, particularly selector-contract row 2150.
- **A7, measurement declaration:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/SCORECARD.md`, SHA-256 `04403120de891fa8eb1c90276da8ea339ec2b0f46442940dbd0fdd5d86ae4e25`; relied on lines 632–650, not historical measurement sections.
- **A8, quality boundary:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/corpus/QUALITY.md`, SHA-256 `1ac6354185c4685f87fba07c702132b87e8102c44412871e5a13622ea6948596`; relied on criteria 3, 24, 31, 38 and 43 for evidence and execution scope.

These auxiliary digests are dependencies disclosed in prose; the standalone Reviewed-SHA256 receipt above authenticates only the assigned primary, not this entire dependency set. Hash equality was not independently recomputed.

## Observed guards and source predictions

**Observed source:** A1 lines 26–32 derive the normal status from findings while keeping `decision_total=len(EXPECTED)`, whose map contains five classes at 17–23. Lines 38–67 reject absent inputs, invalid initial shapes, missing classes and missing registry support before the row-counting loop. A2 supplies one table line for each class; A3 supplies both versioned, A/mined source rows.

**[INFERENCE]** The following are predicted results of A1's unchanged evaluator with other inputs held at the frozen candidate values. They are not command output, constructed fixtures or executed mutation results. Every predicted payload also has `decision_total: 5` and the scope string defined at A1 line 32.

| Input condition | Predicted code / status | Predicted decision_rows | Predicted finding ID(s) and detail | Source path |
|---|---|---:|---|---|
| Frozen candidate data, prose and registry | 0 / PASS | 5 | empty findings | A1:35–83; primary:2–9; A2:19–23; A3:88–89 |
| Decision file absent and read as `raw=None` | 1 / FAIL | 0 | SELECTOR-CONTRACT-MISSING: `decision data or prose absent` | A1:38–39 |
| Prose file absent and read as `markdown=None`, or both files absent | 1 / FAIL | 0 | SELECTOR-CONTRACT-MISSING: `decision data or prose absent` | A1:38–39 |
| Empty or malformed JSON text | 2 / CANNOT_EVALUATE | 0 | SELECTOR-CONTRACT-SCHEMA: `invalid JSON` | A1:40–43 |
| JSON `null`/array, wrong or absent schema marker, absent/non-list decisions | 2 / CANNOT_EVALUATE | 0 | SELECTOR-CONTRACT-SCHEMA: `invalid contract shape` | A1:44–46 |
| Non-object decision, or absent/non-string class | 2 / CANNOT_EVALUATE | 0 | SELECTOR-CONTRACT-SCHEMA: `invalid decision shape` | A1:48–49 |
| Empty decisions or any missing class | 1 / FAIL | 0 | SELECTOR-CONTRACT-MISMATCH: `exact five unique classes required` | A1:50–52 |
| Top-level sources missing or not exactly S081 then S082 | 1 / FAIL | 0 | SELECTOR-CONTRACT-MISMATCH: `exact opened source identities required` | A1:53–54 |
| SOURCES file absent and read as `registry=None` | 1 / FAIL | 0 | SELECTOR-CONTRACT-MISMATCH: `source registry absent` | A1:55–56 |
| SOURCES empty, required row absent/malformed, wrong URL, non-A tier or non-mined status | 1 / FAIL | 0 | SELECTOR-CONTRACT-MISMATCH: `opened scoped A/mined source row required` | A1:57–67 |
| Prose present but empty | 1 / FAIL | 0 | Five SELECTOR-CONTRACT-MISMATCH findings, one per class | A1:70–83 |

Whole-file absence is therefore not source-predicted to become a vacuous clean count. The empty-array `any(...)` check alone would be vacuous, but the following exact-class-set guard rejects it. Missing prose uses a separate early refusal; empty prose cannot supply any supported row. A count of zero is accompanied by non-clean status in these branches.

### Baseline and committed-read qualification

**Observed source:** A1 lines 86–97 distinguish a failed committed read with a confirmed absent path (`None`) from another read failure (`RuntimeError`). Lines 153–160 bind first, then read JSON, prose and SOURCES from the same bound commit. Binding failure yields its typed finding with code 2; the listed read/decode/timeout exceptions yield `E-READ`, code 2, rows 0. Neither branch substitutes an empty successful contract.

**[INFERENCE]** If the declared baseline binds successfully and lacks the decision JSON or prose, with the other reads completing or confirming absence, its expected result is FAIL/1, rows 0, SELECTOR-CONTRACT-MISSING. If a later argument read fails instead, evaluation is not reached and the expected result is non-clean E-READ/2. An earlier binding failure likewise takes precedence. Thus the missing-file result is conditional on successful binding/read access, not an observed baseline measurement.

For declaration context, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/preregister.json:3–19` names the baseline and C1 0→5 target. Its snapshot inventory at 45–73 is selected, not a complete baseline tree. The read-only listing of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/snapshot/corpus` contains selected lesson/QUALITY snapshots; that incomplete selection cannot establish absence of the contract files in the actual baseline commit. No baseline runtime result or committed-tree absence was independently measured here.

## One selected mutation — omitted nullable finding

**Mutant, conceptual only:** remove the `"finding": null` member from the primary's `commit` decision at line 5, leaving the rest of that row and every other byte logically unchanged. No mutant file was created.

**Expected detector:** the unchanged A1 evaluator, with frozen A2/A3, would be the bounded detector. A required-field schema check would reject a missing member of the declared class/outcome/finding tuple; that is the omission predicate being challenged, not a changed Git outcome.

**Observed mechanism:** A1:48–49 requires only object shape and string class initially. A1:77 compares `row.get("finding")` with the expected value; for the commit class, A1:18 sets that expected value to `None`. There is no separate membership check for `finding`. All other predicates remain satisfied by this deletion.

**[INFERENCE] Predicted output, not actual output:** evaluator code 0, status PASS, decision_rows 5, decision_total 5, findings empty. At the CLI this prediction additionally requires a successful committed binding/read of such an input. The pristine and unchanged/restored-input predictions are also code 0 / PASS / five rows.

**Verdict:** runtime **INCONCLUSIVE / NOT RUN** under NO-EXEC. Source prediction: the selected omitted-field mutant **SURVIVES**. This is a conditional required-field/schema-coverage finding, not a claim that an entirely missing contract, prose or SOURCES file can pass. The frozen prose/registry do not explicitly say that a nullable finding must be present rather than defaulted; consequently the source proves absence and explicit null are conflated, but does not alone establish that this is a violated mandatory-field contract. Do not promote the general claim to “all invalid schemas are rejected” on these guards or this review.

A1's selftest source at 109–123 includes missing raw data, malformed JSON, missing Markdown and an empty source registry. It does not include the selected omitted-null-member case or a `registry=None` case. Its assertions at 125–130 compare code and finding-ID set, not row-count/total/status fields. These are source observations about coverage, not a selftest pass or failure.

## Advisory comparison with the build draft

Read-only advisory artifacts were `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/drafts/ExecDecision/selector-contract-r21.json:1–62` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/drafts/ExecDecision/check-selector-contract.py:1–422`. No predispatch SHA-256 for those drafts is supplied by candidate-files.json; they are not production evidence or dependencies of the candidate result predictions above.

The draft declares a different `schema_version`/`rows` format, versus the frozen candidate's `schema`/`decisions`. Its `ROW_KEYS` and exact row-key guard (draft checker:27–29, 269–271) would reject an omitted field in its own format. That is an advisory comparison only: its stricter shape cannot be imported as the candidate's normative schema. Likewise, draft missing-prose/read refusals at 147–159 and 229–238 do not prove the candidate's behavior. The draft does not read SOURCES in its main path at 403–418, whereas the frozen candidate explicitly does. Its separate missing-origin policy at 394–401 is not the candidate's contract. No draft was executed or substituted for the pinned checker.

## Actual output and restoration evidence

- **Actual detector output:** none. All code/status/finding values above are explicitly source predictions.
- **Before hash:** assigned/inventoried primary SHA-256 `1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7`.
- **Mutated hash:** none; no mutated bytes were written.
- **After hash:** not independently recomputed. The source was never a write/edit target; the expected unchanged digest is the same supplied primary digest, not an observed post-restoration hash.
- **Restoration:** unnecessary because no mutation was applied. Only this assigned report was written; no scratch, candidate, draft, sibling or production source bytes were changed by this seat. No pristine/mutated/restored detector sequence or killed-mutant evidence is claimed.
- **Tools:** read operations and this report write only. Operator RULES were read; no tool installation/update was needed or performed.

Scope: executed=none