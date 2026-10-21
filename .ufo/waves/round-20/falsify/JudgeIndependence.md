# Judge independence — round 20, attempt 1

Claim axis: **C2 operability**, `object_selector_tools` 0→9. Focus: whether `tools/check-revision-binding.py --object-selectors` independently checks the shared resolver rather than confirming its own implementation.

The recorded baseline is `0cbc34dd6b20896085a8fb07943e3ea4027d8472`; the binder candidate is `/tmp/tsukuroi-r20-binder-20261021` (`.ufo/waves/round-20/worktree-bindings.json:2-7`). Candidate source snapshots read: `check-revision-binding.py#4BEA`, `_revision.py#0A58`. Findings concern those source snapshots, not a subsequently changed or integrated revision. Recommendation only; no admission, integration, or shipment.

## Findings, by severity

### HIGH — JI-1: the object-selector judge calls its acceptance helper with the wrong arity

- `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:393-401` defines `accepted(sandbox, name, rev, expect_sha)` with **four** parameters.
- The new `exact_accept()` calls `accepted(sandbox, name, revision, expected_sha, branch)` with **five** positional arguments at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:479-482`.
- This is not a dead path: `object_selector_probes()` first calls `exact_accept(shadow, tip)` for `real_prefix_shadow_branch` at `:590-596`; `measure()` invokes these probes for each present original-nine tool at `:663-669`.
- The CLI catches ordinary exceptions from `measure()` and emits `E-INTERNAL`, exit 2, at `:1108-1118`; `cannot_payload()` sets the selector count to zero and status to `CANNOT_EVALUATE` at `:733-743`.

**Impact [INFERENCE, not executed]:** after successful fixture preparation, the first positive selector case raises `TypeError` before the suite can produce a completed per-tool grade. The present candidate therefore cannot supply a valid C2 0→9 measurement through this path. Its object-selector selftest also invokes this path at `:1021-1030`, but its exception handler catches only `Cannot` (`:1086-1087`), not this arity error.

**Recommended correction:** align the acceptance helper/caller interface and deliberately forward the selected branch to `run_tool`; do not merely drop the branch argument and silently measure the default branch instead. This review made no edit.

### MEDIUM — JI-2: the new positive-case comparator changes the existing binding oracle

- The judge documents accepted binding as `exit != 2` with the expected JSON commit at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:19-24`; `accepted()` implements that distinction at `:393-401`.
- The object-selector wrapper additionally requires `case["exit"] == PASS` at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:479-482`.
- This distinction is meaningful for actual consumers: `/tmp/tsukuroi-r20-binder-20261021/tools/check-locator-clarification.py:784-790` binds the revision successfully before evaluating document content; `:799-804` emits that evaluation with the bound revision. Its evaluator can return `FAIL` for document findings (`:424`), and its payload preserves `revision` while returning the domain result code (`:427-436`).

**Impact [INFERENCE, not executed]:** a consumer returning domain exit 1 with the correct bound SHA passes the original binding predicate but fails the new selector predicate. Thus, once JI-1 is corrected, selector counts can depend on unrelated document correctness rather than object-selector identity. This is oracle drift, not evidence that the resolver failed; it does not itself create a tautological positive result.

**Recommended correction:** preserve the existing non-CANNOT acceptance contract for selector probes, keeping any domain-cleanliness requirement separate from the C2 selector count.

## Independence audit

### No executable import of the implementation was found

The judge's actual imports are standard-library modules at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:55-57`. Its `_revision` occurrences at `:277-307` inspect consumer AST import/call nodes; they do not import the implementation. The apparent import in `stub_source()` is generated text under `if False` (`:846-848`). The other import examples are strings passed to the AST census (`:1003-1012`). Reading the judge source did not reveal a dynamic loader or a direct call into `_revision.py`.

The consumers, not the judge, import the implementation. For example, `/tmp/tsukuroi-r20-binder-20261021/tools/check-locator-clarification.py:19,784-789` imports `_revision` and calls its `bind()`. The judge launches consumer scripts in separate Python subprocesses and parses their output (`check-revision-binding.py:359-371,383-401`). The literal call/import search covered all nine names listed at `:61-80`; that search is a locator, not semantic reference proof.

### Resolver logic is substantially duplicated, but the per-case oracle is not that resolver

There is clear structural and literal overlap:

- Judge `object_commit()` at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:139-166` and implementation `_object_commit()` at `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:112-146` both lowercase a prefix, use `rev-parse --disambiguate`, require exactly one object, inspect its type, return commit OIDs directly, and peel tag OIDs through `rev-parse ... ^{commit}`.
- Judge `bind()` (`check-revision-binding.py:192-208`) and implementation `bind()` (`_revision.py:172-192`) follow the same branch/syntax/object/landing/origin sequence.
- Environment construction is also duplicated (`check-revision-binding.py:100-104`; `_revision.py:62-66`). These are separate function definitions and newly constructed dictionaries, not a shared imported callable or mutable cache. Source similarity alone does not establish who copied whom.

This is **not algorithmically diverse bootstrap validation**: `measure()` obtains `tip` from the judge's own similar resolver (`check-revision-binding.py:635-638`). Common-mode defects in that initial revision selection remain a residual risk.

However, the selector cases do **not** call `object_commit()` or `_revision.bind()` to compute the expected result for each tested selector. Ghost expectations are fixed `ID_INVALID` values after an object-inventory absence check (`:502-525`); shadow expectations are the previously selected `tip`, deliberately distinct from `decoy` (`:584-609`); the annotated tag is explicitly created pointing at `tip` (`:490-501`) and is later required to bind that `tip` (`:615-618`). `accepted()` compares the consumer's JSON against the supplied expected SHA (`:393-401`). Thus, duplicated bootstrap logic is a common-mode risk, **not sufficient evidence of a tautological per-case pass**. Preserve this fixture-derived oracle separation rather than replacing expectations with calls to either resolver.

### Shared fixture state is visible, not a hidden shared verdict

The judge prepares one temporary clone, materializes the selected consumer sources, and runs consumers sequentially in it (`check-revision-binding.py:233-274,635-673`). Probes intentionally modify the clone's refs and normally restore them in `finally` blocks (`:516-540,590-630`). The object/ref database is therefore shared test input, but expected IDs and SHAs are not learned from the consumer's returned verdict. No imported implementation state was found in the judge process.

This is not process isolation against malicious tools: the judge explicitly discloses the caller-authority trust boundary at `:49-53`. No stronger isolation or host-safety conclusion follows from the temporary clone.

## Canonical evaluation and limits

The retained R20 run logic checks out one evaluation revision and uses that evaluator for both baseline and after-target commands (`.ufo/waves/round-20/measure/run.py:53-78`). Each judge invocation then creates its own temporary clone (`check-revision-binding.py:635-645`). The selector aggregate counts only the original-nine tools' case results, not `_revision` import-census matches (`:674-717,721-725`). This supports a finite nine-consumer interpretation, not saturation over arbitrary selectors or programs.

No direct import/shared-state mechanism was found that makes this source automatically agree with `_revision.py`. The duplicated bootstrap algorithm remains a common-mode limitation, and JI-1 currently prevents completed positive-case evaluation. No C2 measurement is certified here.

## Residual risk and verification gaps

- LSP was unavailable: reading `xd://lsp` returned `No such tool`; mounted devices listed only `ast_edit` and `debug`. LSP status, references, definitions, and diagnostics could not be obtained. Literal searches located source; conclusions above rely on directly read definitions/calls, not grep as semantic proof.
- No evaluator, import, fixture, Git command, build, test, linter, formatter, smoke run, subprocess, or external request was executed. Failure-path descriptions marked `[INFERENCE]` are static deductions, not captured runtime output.
- No Git diff or commit/object-identity verification was performed. The recorded baseline/worktree binding and directly read candidate source are the available provenance; later edits and integration are unverified.
- No routing or resume-continuity implementation was in this slice. No host, service, package, mount, kernel, bootloader, or boot-image operation was performed. Boot images remain **UNKNOWN**; no host/boot clearance is implied.
- No tools were installed or updated. Only this named report was written.

Scope: executed=none
