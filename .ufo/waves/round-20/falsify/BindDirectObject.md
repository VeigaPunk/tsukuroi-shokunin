# BindDirectObject — round 20 attempt 1

## Scope and axes

Reviewed the object-ID-first binding path in `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py` (read snapshot `0A58`), its literal callers, and the independent selector-probe source. Axis: C2 operability, specifically object selection and preservation of the selected commit identity. C1 adjacency, C3 calibration, exec-log filtering, orchestration/resume behavior, and host/boot safety are outside this slice. The original-nine C2 requirement is recorded at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:13-19,37-47`.

## Findings by severity

**No confirmed in-scope ref-fallback defect.** I could not substantiate a hexadecimal revision selector that binds a same-named branch/tag target instead of its selected object in this source snapshot. This is a source-review result, not an admission or a measured `object_selector_tools=9` result.

### Normalization and uniqueness

- `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:41,172-177` permits only 7–64 ASCII hexadecimal characters and validates the branch before resolving the revision. Nonhex ref syntax cannot reach the object resolver through `bind()`.
- `tools/_revision.py:119` passes `revision.lower()` only as the value of `--disambiguate=`, not as a positional revision expression. Uppercase input therefore does not take a distinct ref-resolution route.
- `tools/_revision.py:122-126` requires exactly one enumerated object **before** checking its type. Both zero matches and multiple matches return `None`; `bind()` converts that to `E-REVISION-INVALID` at `:177-179`. There is no retry through `_commit(repo, revision)`.
- `tools/_revision.py:127-137` checks the unique object's type. A commit returns its enumerated full `oid` directly; a non-tag, non-commit object returns `None`. The implementation does not filter the enumeration down to commits and then accept an otherwise ambiguous prefix.

### Concrete selector attack and ref-resolving selector

Use the concrete spelling **`deadbeef`**, with a hypothetical `refs/tags/deadbeef` (or `refs/heads/deadbeef`) aimed at decoy commit B:

1. If no object ID begins with `deadbeef`, the zero-object path returns `None` at `tools/_revision.py:122-124`, and binding rejects at `:177-179` without consulting that ref.
2. If exactly one matching object is commit A, the selected full A is returned at `:126-135`, not the original `deadbeef` spelling.
3. If multiple objects match, rejection occurs at `:123-124` before the type check or any branch lookup.

These are source-derived branches, not observations from a constructed repository. They do not supply a successful counterexample.

A selector that **does** intentionally resolve a ref is **`refs/heads/master^{commit}`**: `_commit()` constructs that expression at `tools/_revision.py:98-100` when `bind()` passes the qualified local branch at `:180-181`. The analogous optional origin selector comes from `:186-191`. Neither is a fallback interpretation of the supplied revision. Treating this deliberate branch verification as an object-selector defect would conflate the two inputs.

The remaining revision-parser boundary is an annotated-tag object: `tools/_revision.py:139-142` submits the already-enumerated full `oid` as `<oid>^{commit}`. Thus an abbreviated input selecting tag object T does not send the original abbreviation back to the parser. A ref named with T's full OID is the relevant remaining shadow attempt, but the presence of this parser call alone does **not** establish that Git will prefer such a ref over the full object ID. I do not report that unproved precedence assumption as a finding.

### Caller and error-path observations

- `tools/_revision.py:119-121` reports a nonzero disambiguation command as `E-GIT-FAILED`; zero/multiple successful matches are invalid selectors. Type/peeling failure in a readable repository returns `None` at `:128-146`; subprocess timeout/unavailability raises `RevisionError` through `:69-77`.
- `tools/_revision.py:180-192` uses the resolved `sha` for local/origin ancestry and returns it in `Binding`; it does not restore the supplied revision spelling after resolution. `_commit()` is used for the qualified branch refs and informational `branch_tip()` at `:163-169`, not as an object-lookup fallback.
- Literal caller inspection found consumers using the returned identity, for example `/tmp/tsukuroi-r20-binder-20261021/tools/check-recheck-commands.py:747-752`, `tools/check-section-citations.py:912-917`, and `tools/check-seat-scope.py:261-266`; the corresponding `RevisionError` paths remain explicit. These observations are textual, not semantic reference proofs.
- The independent checker has its own resolver at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:139-166,192-208`. Its probe source separately constructs prefix branch/tag shadows at `:584-601` and full commit/tag OID shadows at `:602-612`, comparing to the expected object identity. Those are visible probe definitions, **not executed results**.

## Residual risk and verification gaps

- No Git command, test, import, runtime, build, formatter, subprocess, external request, or host probe was executed. Under the NO-EXEC contract, the full-OID tag-peeling parser boundary and ancestry commands were not dynamically verified.
- `read xd://lsp` returned `No such tool: xd://lsp` (mounted devices listed only `ast_edit` and `debug`). No LSP status/reference/definition/diagnostic service was available. Grep was used only to locate literal callers and is not represented as semantic proof.
- The baseline identity is assignment-provided. No Git diff or independent checkout-identity check was available within this read-only seat; conclusions apply to the cited candidate source, not a verified baseline-to-candidate patch.
- No selector fixture was created and no literal object OID was fabricated. No saturation, C2 nine-tool pass, integration clearance, current host safety, or boot safety is established. Boot images remain UNKNOWN.
- Wrote only this report. Installed or updated no tools and edited no source, configuration, Git state, or sibling files.

Scope: executed=none
