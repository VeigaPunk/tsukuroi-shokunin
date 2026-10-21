# BindUnlanded — round 20 attempt 1

## Scope and axes

Read-only source review of the unlanded-object binding path and its tests in `/tmp/tsukuroi-r20-binder-20261021`, the binder candidate named by `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:2-7`. Axes: C2 operability, object identity, first-failure/error-class continuity, and honest test evidence. No code changes, runtime invocation, or claim admission.

**Exact identifier:** the canonical R20 expectation is `E-REVISION-NOT-LANDED; exit=2`, not the assignment's shorthand `E-REVISION-UNLANDED` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:37-45`). Both candidate implementations use the canonical spelling: `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:43-49` and `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:82-89`. This report does not treat an identifier rename as part of the claim.

## Findings by severity

### P1 — Object-selector evaluator cannot reach its unlanded-object test

**Evidence:** `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:393-401` defines `accepted(sandbox, name, rev, expect_sha)` with four parameters and calls `run_tool` without a branch argument. The newly added `exact_accept` calls it with five positional arguments, including `branch`, at `:479-482`. Its first call in the object-selector sequence is the valid-prefix branch-shadow case at `:590-596`, before `cases["unlanded_object"]` at `:620`.

**Consequence [INFERENCE from the Python call signature and control flow]:** when normal sandbox prerequisites succeed, `--object-selectors` raises `TypeError` at the first positive selector case. Earlier fixture failures also do not constitute an unlanded test result. Consequently, the new unlanded-object case does not run, and the evaluator cannot furnish the claimed original-nine object-selector result. `measure` invokes the sequence at `:663-669`; `main` converts the signature error to `E-INTERNAL` and exit class 2 at `:1108-1118`. The resulting payload has `object_selector_tools=0`, `object_selector_status="CANNOT_EVALUATE"`, and no per-tool selector cases (`:733-743`), rather than an `E-REVISION-NOT-LANDED` observation for the unlanded probe.

The hermetic selftest also reaches `measure(..., object_selectors=True)` at `:1021-1030`, but catches only `Cannot` at `:1086-1087`. Thus the same `TypeError` escapes that selftest, and its later independent `bind-unlanded` assertion at `:1055-1056` is not reached [INFERENCE; not executed].

This is in the retained C2 route: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/measure/run.py:65-78` selects tool selftests and `check-revision-binding.py --tools-revision ... --object-selectors`. Align the helper signature and branch forwarding; do not remove or weaken the unlanded refusal assertion. No fix was made by this seat.

## Binder and test-path assessment

No source-level bypass of the local ancestry check was found for a uniquely selected, readable commit object with a valid existing target branch. This is a static assessment, not an observed runtime pass.

1. **Object validity is separate from landing.** `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:119-135` enumerates matching object IDs, requires exactly one, checks its type, and returns the selected commit OID directly. A valid commit is not rejected merely because it is unlanded. Invalid/ambiguous/noncommit selection takes the separate `E-REVISION-INVALID` path at `:175-179`.
2. **Landing remains mandatory and precedes push status.** The shared binder resolves `refs/heads/<branch>`, distinguishes a missing branch, and raises `E_NOT_LANDED` on false local ancestry at `:180-185`. It cannot return a `Binding` before this check; optional origin ancestry and the return follow at `:186-192`. `_ancestor` distinguishes Git exit 1 from errors at `:156-160`; exit >=2 remains `E-GIT-FAILED`, not an unlanded or unpushed result. The lane copy has the same local-before-origin ordering at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/_revision.py:134-154`; the candidate changes the revision-resolution call, not this ordering.
3. **The independent judge also retains local ancestry.** `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:192-208` resolves the object before checking the selected local branch and raises `ID_UNLANDED` before inspecting origin. Its ancestry result handling is explicit at `:169-175`.
4. **The unlanded fixture is a real new commit, not an invalid hash.** Judge preparation checks out the measured tip detached and pins local/origin refs at `:233-241`. `probe_commit` creates a commit, obtains its commit OID, and refuses the fixture if it equals the tip or is reachable from the target branch at `:310-319`. `measure` constructs this fixture at `:642-650`. The shared binder's selftest likewise detaches at the tip, commits, and captures the OID at `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:218-228`.
5. **The assertions require the right refusal, not mere non-success.** The shared selftest expects `E_NOT_LANDED` without origin at `:244`, and with origin present at `:258-261`. Its harness compares the actual `RevisionError.fid` at `:198-208`. The judge's existing consumer probe requires exit 2 and the expected finding at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:383-390,412-417`, and the single-ID check rejects double/misclassified findings at `:438-443`. The new object-selector assertion at `:620`, through `exact_refusal` at `:473-477`, additionally requires exactly one finding and exactly `[ID_UNLANDED]`. Its assertion is appropriately strict but unreachable because of P1.

### Original-nine caller propagation inspected

All paths below are relative to `/tmp/tsukuroi-r20-binder-20261021/tools/`. These are source-level bind/catch/emit inspections, not semantic-reference or runtime proof. In each inspected revision-bound path, a shared binding refusal preserves `exc.fid` and exits the content-evaluation path rather than accepting the revision.

| Consumer | Bind and refusal propagation evidence |
| --- | --- |
| `check-locator-clarification.py` | `:782-795` |
| `check-root-dac-correction.py` | `:269-282` |
| `check-section-citations.py` | `:912-927` |
| `check-source-scope-correction.py` | `:635-649` |
| `measure-update-recheck.py` | `:471-481,758-772` |
| `check-boot-chain.py` | `:1572-1584` |
| `check-freshness-r17.py` | `:772-796` |
| `check-recheck-commands.py` | `:744-763` |
| `check-seat-scope.py` | `:258-272,658-665` |

## Residual risk and verification gaps

- The shared binder's direct source path supports the canonical unlanded classification; no runtime pass is asserted. The new evaluator cannot substantiate it until P1 is corrected.
- The new unlanded case uses the full unlanded commit ID (`check-revision-binding.py:620`). The branch/tag shadow cases instead select the landed tip (`:584-609`); this sequence does not separately exercise an unlanded-object prefix shadowed by a ref pointing to a landed commit. That is a finite-coverage gap, not a demonstrated binder defect.
- No LSP device is exposed in the allowed tool inventory, and NO-EXEC prohibits activating one. Status/references/definition/diagnostics were therefore unavailable. Grep was used only to locate source, followed by explicit source reads; it is not presented as semantic caller proof.
- No Git command, test, build, lint, formatter, smoke run, external request, or host probe was performed. The working-file comparison does not independently certify the recorded baseline OID or produce a Git diff. No tool installation/update occurred. Only this named report was written.
- C1/C3, runtime routing, and resume-continuity admission are outside this assigned binder slice; no saturation or admission verdict is issued. Host/boot safety is not established; boot images remain UNKNOWN with no clearance.

Scope: executed=none.
