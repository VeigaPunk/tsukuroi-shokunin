# BindUpperHex — C2 independent edge-case oracle

**Axis:** C2 operability. Preregistered expected behavior is `uppercase_object: same commit` (`.ufo/waves/round-20/preregister.json:37-47`). This report is a baseline-only fixture design; no candidate code/output was inspected.

## Baseline evidence

- `tools/_revision.py:40` admits both `a-f` and `A-F` in 7–64-character selectors. `bind()` validates this syntax before `_commit()` (`:134-141`); `_commit()` asks `git rev-parse --verify ... <selector>^{commit}` and returns Git's resolved object name (`:97-108`). Its hermetic selftest already expects `bind(repo, tip.upper()).sha == tip` (`:194-205`), but has no uppercase abbreviated-ID case.
- The independent `tools/check-revision-binding.py` says its binder is intentionally independent (`:7-11`) and also admits uppercase hex (`:82`, `:162-176`). Its per-tool probes currently cover lowercase `tip` and `tip[:8]`, plus nonhex `master`, but no uppercase selector (`:380-388`). `accepted()` compares `got.lower()` to `expect_sha.lower()` (`:361-369`), so by itself it proves object identity, not that JSON output is normalized to canonical lowercase. The judge's own selftest already expects `refs/heads/master` to be `E-REVISION-INVALID` (`:790-799`), but that case is not run against every consumer.

## Proposed fixed synthetic fixture and expected results

Use the judge's hermetic temp-repository shape (`make_fixture`: `master`, base commit, then landed tip; `check-revision-binding.py:626-642`) with no origin ref. Let `T` be the lowercase full OID of the landed tip. Select/fix the synthetic tip so `T[:8]` contains at least one `a-f`; this guarantees both `T.upper()` and `T[:8].upper()` actually differ from lowercase inputs rather than accidentally exercising a no-op uppercase conversion.

For each original-nine consumer, add these object-selector probes to `probe_tool()`'s required `cases`:

| Input (`--revision`) | Expected binding/result |
|---|---|
| `T.upper()` (40 hex in this SHA-1 fixture) | accepted, resolved commit is exactly `T` |
| `T[:8].upper()` (unique short prefix) | accepted, resolved commit is exactly `T` |
| `refs/heads/master` | exit 2, sole finding `E-REVISION-INVALID` |

Retain the existing `master` case (`:382-385`) as the short nonhex-ref rejection. For `bind()` directly, expected values are `bind(repo, T.upper()).sha == T`, `bind(repo, T[:8].upper()).sha == T`, and `bind(repo, "master")` / `bind(repo, "refs/heads/master")` each raise `RevisionError` with `fid == E-REVISION-INVALID`.

For the CLI-level acceptance records, require `exit != 2` and JSON `revision == T` (exact lowercase string, not merely case-insensitive equality). For each ref refusal, require `exit == 2`, `finding == E-REVISION-INVALID`, `binding_ids == [E-REVISION-INVALID]`, and `finding_count == 1`. The exact lowercase comparison is important: the current case-folding comparison in `accepted()` would accept a consumer that echoes an uppercase input as its JSON revision instead of returning the canonical resolved OID.

## Source justification and mutant

Git's official `gitrevisions` 2.56.0 documentation, “SPECIFYING REVISIONS” / `<sha1>`, defines a full hexadecimal object name or a unique leading substring as object-name syntax, and separately defines names such as `master` and `refs/heads/master` as symbolic `<refname>` syntax: <https://git-scm.com/docs/gitrevisions/2.56.0>. That distinction matches `_revision.py`'s explicit hex-only gate. The documentation does not itself state case-folding; uppercase acceptance is grounded in this module's `[0-9a-fA-F]` contract and existing `upper-hex` selftest.

Smallest regression killed: narrow the revision regex from `[0-9a-fA-F]` to `[0-9a-f]`; both uppercase object probes then fail instead of resolving `T`. A separate one-line bypass of the hex-only gate would let a real `master`/`refs/heads/master` ref resolve and fail the required `E-REVISION-INVALID` refusal. Exact lowercase JSON equality additionally kills a pass-through implementation that resolves correctly but emits the uppercase selector rather than canonical `T`.

**Scope/limitations:** baseline and public documentation only; no candidate diff, runtime, or fixture output was inspected or executed. The synthetic OID is computed by the fixture; its prefix-letter condition must be enforced before accepting the fixture as exercising uppercase-short behavior.

Scope: executed=none