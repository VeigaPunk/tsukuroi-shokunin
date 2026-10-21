# BindGhost40Annotated — C2 candidate review

## Findings

### High — binder selftest aborts before constructing the annotated ghost-tag fixture

`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:210-216` defines the selftest-local helper `run`; the module's Git helper is named `_git` at `:69-77`. There is no `git` definition in this file, yet annotated-tag fixture selection calls `git(...)` at `:291-292`. For the first candidate that passes the object-inventory check, this raises `NameError` outside `expect()` and before the annotated tag is created at `:294`; therefore the annotated ghost assertion at `:306-307` cannot be reached in the ordinary fixture. The exception is not converted into a test failure record, so `--selftest` aborts rather than completing its cases (`:378-380`). This leaves the binder's required ghost-tag regression unverified and breaks its selftest path.

### Medium — independent judge's annotated fixture does not exercise its own resolver

The judge constructs a full-width annotated ghost name and checks it at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:542-574`. However, `exact_refusal()` at `:473-477` delegates to `refused()`, which calls `run_tool()` for the candidate consumer (`:383-390`); it does not call the judge's local `bind()`. The judge's independent resolver is `object_commit()` / `bind()` at `:139-208`, while its direct selftest only checks an unreferenced `"0" * 40` selector at `:1043-1050`. Thus the annotated fixture proves no direct behavior of the independent judge resolver against a same-named annotated tag, despite that resolver being a separate implementation.

## Checks that pass by source inspection

- The full 40-hex tag-name safeguard is explicit in both fixture builders. Binder checks the name against the current object inventory before creation and checks the refreshed inventory after annotated-tag creation; if the new tag object's OID equals the name, it deletes the ref and retries (`_revision.py:284-305`). The judge performs the same pre/post exact-OID comparison, also excluding existing head/tag refs (`check-revision-binding.py:542-568`). On the selected fixture path, the tag object's OID therefore cannot equal the tag name.
- Both resolver implementations are object-only: `_revision.py:112-146,172-179` and `check-revision-binding.py:139-166,192-199` enumerate object IDs with `rev-parse --disambiguate`, return no selection for a zero-match result, and map that to `E-REVISION-INVALID`. This is the intended rejection path for the chosen absent object name. It is source evidence only; the broken binder fixture prevents its annotated-tag path from being exercised by that selftest.
- In the judge's consumer probe, the selected tag name is submitted bare and the refusal check requires exit class `CANNOT`, the expected finding ID, exactly one binding finding, and no extra binding IDs (`check-revision-binding.py:473-477,571-574`). The object-selector results are included in the aggregate only with `object_selectors=True` (`:663-669,703-725`); the judge's selftest invokes that mode at `:1021-1030`.

## Residual risk and verification gaps

NO-EXEC scope prevented execution, so no concrete tag/object OIDs or runtime resolver outcome were observed. The two equality guards and rejection paths were inspected statically. The binder `NameError` is a concrete blocker independent of runtime Git behavior; the judge's own resolver lacks the corresponding direct tagged fixture assertion. LSP status/references/definition/diagnostics were not requested because the seat's NO-EXEC whitelist permits only read, grep, glob, and report write; source search is not semantic LSP evidence. No host, boot, or safety claim is made; no tools were installed.

Scope: executed=none
