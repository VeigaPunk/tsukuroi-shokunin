# Round-20 independent source oracle — C2

**Scope:** baseline/source and `preregister.expected.C2` only. No candidate implementation or measurement output was read or used. No execution, measurement, host probe, or implementation change. Axes: C1 adjacency; C2 operability; C3 calibration.

## Source support before measurement

C2 preregisters `object_selector_tools: 0 → 9` for the original nine consumers, with discovered tools informational only. The baseline `tools/check-revision-binding.py:61-80` names five legacy plus four round-17 gates (`TOTAL = 9`); `:468-495` keeps discovered tools outside that original-nine grade. This supports the denominator and scope, not an observed baseline or post-change count.

The baseline `tools/_revision.py:40-48,134-154` accepts 7–64 hex characters, resolves `revision^{commit}`, then checks local-branch ancestry and, when present, remote-branch ancestry. Its resolver is ordinary Git revision parsing, not an object-ID-only resolver. `--end-of-options` only prevents an argument being treated as an option; it does not itself impose object-only resolution. The baseline checker has no `--object-selectors` CLI option (`check-revision-binding.py:515-525`) and its current `probe_tool` cases do not include the named hex/ref-collision classes (`:380-423`). Consequently, the semantic oracle below is source-grounded, but `before=0` is not independently established as a measured result by baseline source.

Official Git documentation supports the required object semantics: [`gitrevisions`](https://git-scm.com/docs/gitrevisions) distinguishes full/unique hexadecimal object names from refnames, and documents `^{commit}` as recursive peeling to a commit (including an annotated tag); [`git rev-parse --verify`](https://git-scm.com/docs/git-rev-parse) documents object/type verification and `--end-of-options`. The baseline `^{commit}` use supports rejecting a blob as non-commit and accepting an annotated tag object when it peels to a commit. The baseline ancestry checks support the distinct NOT-LANDED and NOT-PUSHED refusals.

**Pre-measure support verdict:** the desired pass/fail semantics for all nine classes are supported by the object-name, type-peeling, and ancestry contracts. However, the expected ghost-ref rejection and prefix-shadow identity are specifically *object-only* requirements not enforced by the baseline resolver; they are normative targets, not evidence that baseline already behaves that way. `preregister.expected.C2` supplies class names and expected labels but no literal selector strings or fixture OIDs. Thus exact numeric fixture SHA values are not source-supported here; the SHA oracle must be evaluated against the frozen fixture object's full OID, not filled from candidate output. The preregistered `after=9` is a target, not a result.

## Fixed fixture classes and expected results

Run every row against each of these original-nine consumers: `check-locator-clarification.py`, `check-root-dac-correction.py`, `check-section-citations.py`, `check-source-scope-correction.py`, `measure-update-recheck.py`, `check-boot-chain.py`, `check-freshness-r17.py`, `check-recheck-commands.py`, and `check-seat-scope.py`. Hold the fixture repository, branch, refs, and objects constant across consumers. Let `C` denote a canonical full OID of the intended commit; its required local/remote reachability is stated per case. For shadow cases, ensure the decoy ref target is a *different* commit that is also landed and pushed, so only object identity distinguishes the result. For ghost cases, the selector is 7–64 hex, no object OID has that prefix, and the same-named ref points to an otherwise admissible commit.

| Case / fixed input class | Expected tool result | Finding / bound SHA oracle |
|---|---|---|
| `ghost_hex_branch`: all-hex selector with no matching object; same-named local branch points at an admissible commit | Exit 2 | `E-REVISION-INVALID`; one binding finding; must not bind the branch target |
| `ghost_hex_tag`: all-hex selector with no matching object; same-named tag points at an admissible commit | Exit 2 | `E-REVISION-INVALID`; one binding finding; must not bind the tag target |
| `valid_prefix_shadow_branch`: unique all-hex prefix of landed+pushed commit `C`; same-named branch points at a different landed+pushed commit | Exit other than 2 under the existing `accepted()` predicate | JSON `revision` equals full canonical OID of `C`, never the branch target |
| `valid_prefix_shadow_tag`: unique all-hex prefix of landed+pushed commit `C`; same-named tag points at a different landed+pushed commit | Exit other than 2 | JSON `revision` equals full canonical OID of `C`, never the tag target |
| `uppercase_object`: uppercase spelling of the full OID of landed+pushed commit `C` | Exit other than 2 | JSON `revision` equals canonical full OID of `C` |
| `noncommit_blob`: full OID of an existing blob object | Exit 2 | `E-REVISION-INVALID`; one binding finding; no commit may be bound |
| `unlanded`: full OID of an existing commit not reachable from local target branch | Exit 2 | `E-REVISION-NOT-LANDED`; one binding finding; no commit may be bound |
| `unpushed`: full OID of a commit reachable from local target branch but not from existing `origin/<branch>` | Exit 2 | `E-REVISION-NOT-PUSHED`; one binding finding; no commit may be bound |
| `full_id`: full OID of landed+pushed commit `C` | Exit other than 2 | JSON `revision` equals full canonical OID of `C` |
| `annotated_tag_object`: full OID of an annotated tag object whose peeled target is landed+pushed commit `C` | Exit other than 2 | JSON `revision` equals full canonical OID of `C`, not the tag-object OID |

For accepted cases, “exit other than 2” follows the existing evaluator's `accepted()` contract (`check-revision-binding.py:361-369`): tools may return their own pass/fail status, but a binding refusal is exit 2 and the JSON must name the expected commit. Do not strengthen this to exit 0 unless the unchanged evaluator explicitly requires it. The one-finding refusal count is the existing strict-refusal contract (`:424-429`); the preregistered C2 strings do not themselves specify that count. For a refusal, the bound-SHA expectation is **none**; this does not require a particular error JSON field value.

**Count oracle:** `object_selector_tools` counts original-nine consumers passing the complete matrix, once per consumer, not passing cases and not discovered tools. Expected target: `0` before and `9` after, with denominator 9. The baseline checker’s static shared-import census is expressly not a reachability proof (`check-revision-binding.py:35-38`); only the later unchanged evaluator can establish the measured count.

## Causal before → after criterion

Before: `_revision.py` applies a hex-only lexical filter, then sends that spelling through Git's general `^{commit}` revision parser. That path does not prove that a hex selector names an object rather than a same-named branch/tag. The ghost and shadow pairs distinguish these outcomes directly. After: object-only lookup must reject a no-object ghost even if the corresponding ref exists, and a unique object prefix must bind its actual object even when a same-named ref targets another commit; commit peeling and the existing local/remote ancestry gates must remain intact. Count a consumer only if every row gives the expected result; all nine must pass to support `0 → 9`.

## Admit/reject controls and limits

- **Admit controls:** full OID, unique prefix despite branch/tag shadowing, uppercase full OID, and annotated-tag object OID peeling to a commit. Each proves that object selection preserves the intended commit identity.
- **Reject controls:** missing-object hex strings shadowed by branch/tag refs, a blob OID, an unlanded commit, and a local-only commit. These distinguish invalid selector/type, landing, and push failures rather than collapsing them.
- Freeze and publish literal fixture selectors and their object OIDs before measurement; they are absent from the preregistration and baseline source. No SHA has been invented here. A wrong shadow-target SHA is a failure even if the tool exits successfully.
- Finite syntax/fixture coverage only: no claim about arbitrary shell equivalence, runtime enforcement, or all Git ref/object ambiguity cases. This review makes no current host or boot-readiness claim. No LSP device was available in this seat; no semantic caller/reference claim is made.

## C1/C3 source boundary

- **C1 adjacency:** the pinned OUT-009 record in `corpus/knowledge/adjacency-anchors-r19.json` fixes Revenger at commit `cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97`, blob SHA-256 `63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f`, snapshot `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md`. That snapshot's lines 3–7 declare shipped-artifact reverse engineering and the observation/inference/unknown ledger. This supports the locator's source text, not ownership arbitration or write authority.
- **C3 calibration:** `tools/boot-chain-audit.sh:81-86,794-805` maps live summaries to exit 0 CONSISTENT or exit 2 UNKNOWN; its v2 live path has no exit-1 DEGRADED case. Lines 104–108 give selftest its own exit map where 1 means selftest failure. `corpus/knowledge/boot-chain-r17.md:54-63,65-82,232` limits the emulation/inference and explicitly leaves Btrfs-specific behavior and an actual snapshot boot unverified. This supports the typed distinction only, never a host/boot-safety certificate.

Scope: executed=none
