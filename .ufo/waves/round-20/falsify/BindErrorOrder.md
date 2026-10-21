# BindErrorOrder — R20 source-only review

## Findings by severity

### P2 — Added fixture calls an undefined helper, aborting the binder selftest

**Evidence:** `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:291-292` calls `git(repo, ...)` while constructing the annotated ghost-tag fixture. This module imports no `git` binding (`:30-39`), defines the process-returning helper as `_git` (`:69-77`), and defines the selftest's successful-command helper as `run` (`:210-216`). The complete inspected module contains no definition or assignment for the bare name `git`.

**[INFERENCE, not an executed failure]:** On reaching the first eligible candidate in `:287-294`, Python raises `NameError` before creating the annotated tag. The call is outside `expect`; `expect` itself catches only `RevisionError` (`:198-208`), and the CLI directly calls `selftest()` (`:378-380`). Consequently the normal selftest invocation cannot reach its summary (`:370-375`) or the later blob/origin-blob/unavailable-repository controls (`:357-366`). This is an unintended selftest/observability change, not a change authorized by object-only selector semantics. The baseline-side selftest proceeds directly from pushed-tip to those controls, with no such bare-helper call (`/tmp/tsukuroi-r20-registry-20261021/tools/_revision.py:224-244`).

**Impact:** The source still declares the legacy precedence controls, but the expanded suite cannot provide complete evidence while this call remains. The retained R20 runner includes every Python tool's selftest (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/measure/run.py:65-69`), making this a concrete evaluation-path regression.

**Recommended correction, not applied:** Use the existing process-returning `_git` helper for the return-code presence check. The local `run` helper is not equivalent here: it raises on a nonzero status, including the expected absent-ref result (`:214-215`).

## Error-precedence comparison

**Result:** No out-of-claim reordering was found in `bind` for the requested invalid-branch, invalid-revision, missing-branch, not-landed, or not-pushed cases. This is a bounded source conclusion, not a runtime pass or C2 admission.

### Compared sources and provenance

- Baseline identity and candidate locations are declared in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:2-7`: baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472`, binder candidate `/tmp/tsukuroi-r20-binder-20261021`.
- **B** below means `/tmp/tsukuroi-r20-registry-20261021/tools/_revision.py`, the retained baseline-side copy. Its inspected implementation (`:40-154`) also matches the production-lane copy at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/_revision.py:40-154`. The retained baseline-only oracle independently describes that implementation at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/build/OracleC2.md:9-11`.
- **C** below means `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py`.
- Source snapshots are B `F7BF` and C `0A58`. These are reader snapshot identifiers, not Git OIDs or content digests. No Git command was used to authenticate the retained copy against the baseline object.

### First-failure matrix

All B/C citations below resolve to the exact file paths above. The conclusions assume the relevant Git operation completes normally; operational failures are addressed separately.

| Competing failures / invariant | Baseline | Candidate | Comparison |
|---|---|---|---|
| Invalid branch syntax, even with invalid revision syntax | B:83-94,136-138 validates branch first | C:84-95,174-176 validates branch first | Same `E-BRANCH-INVALID`; branch type/regex, `HEAD` rejection, and `check-ref-format` are unchanged. This includes `a..b` and `master/`, which require Git's format check. |
| Valid branch syntax, invalid revision syntax, and absent local branch | B:137-138 rejects before any commit/local-ref lookup | C:175-176 rejects before any object/local-ref lookup | Same `E-REVISION-INVALID`, not `E-BRANCH-MISSING`. The string/type and 7–64 hex requirements are unchanged (B:40-41; C:41-42). |
| Syntactically valid but unresolved/noncommit selector and absent branch | B:139-145 resolves selector first | C:177-183 resolves selector first | Same ordering: selector refusal precedes missing branch. C's object-vs-ref interpretation is the intended changed stage, not a moved gate. |
| Valid resolved commit and missing local branch, regardless of origin | B:142-145 obtains local tip and refuses before ancestry/origin | C:180-183 does the same | Same `E-BRANCH-MISSING`. Both still use `_commit` for the fully qualified local ref; that helper is unchanged (B:97-108; C:98-109). |
| Existing branch; selected commit is neither landed locally nor pushed to origin | B:146-147 raises before B:148-153 | C:184-185 raises before C:186-191 | Same single `E-REVISION-NOT-LANDED`; no second NOT-PUSHED finding. |
| Commit is landed locally, origin exists but does not contain it | B:150-152 | C:188-190 | Same single `E-REVISION-NOT-PUSHED`. |
| Commit is landed locally and no origin ref exists | B:148-154 | C:186-192 | Same successful binding with `origin_tip=None`; no added push requirement. |
| Local ancestry fails operationally, or origin is a noncommit object | B:118-122 distinguishes merge-base rc 0/1 from other statuses | C:156-160 retains that distinction | Same `E-GIT-FAILED`, never a false NOT-LANDED/NOT-PUSHED. An earlier local non-ancestor refusal still wins over a bad origin. |

The executable body change at the selector stage is specifically B:139 `_commit(repo, revision)` → C:177 `_object_commit(repo, revision)`. C:119-137 enumerates object IDs, requires exactly one, and checks its type before the existing local/origin gates. C:139-146 retains tag-to-commit peeling. Changed results caused by rejecting a ghost hex ref or binding a real object's identity instead of a shadow ref are within C2's declared scope (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:13-19,37-47`). They do not establish a changed precedence contract.

### Operational diagnostic delta, not a precedence defect

There is a narrower observable difference outside ordinary selector success/refusal outcomes. B:99-108 handles a failed revision parse by checking repository availability, then raises `RevisionError(E_GIT, ref, "repository unavailable: ...")` if unavailable. C:119-121 immediately raises `RevisionError(E_GIT, "revision", "object lookup failed: ...")` on nonzero disambiguation status. Thus, **[INFERENCE]** an unavailable-repository call with valid branch/revision syntax keeps the same error ID and stage but changes the exposed `site` and `detail`, and performs no second availability probe. On a nonzero disambiguation result in a readable repository, the new path also does not apply B's failed-parse-to-INVALID normalization. No supported healthy-repository input producing that latter condition was demonstrated here; it is not claimed as a concrete new misclassification.

The unavailable-repository selftest only compares `fid` (B:160-166,235; C:198-204,366), so its declaration would not catch a diagnostic-text difference. No exact diagnostic wording guarantee was found in the inspected binding contract, so this is recorded as compatibility detail, not a second actionable defect.

## Caller and declared-control checks

LSP was unavailable: reading `xd://lsp` returned `No such tool`, with only `ast_edit` and `debug` mounted. No LSP server/status/references/definition/diagnostics result could be obtained. Literal searches were used solely to locate the following source adapters; they are not semantic reference or reachability proof.

The original-nine list is defined at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:61-80`. Inspected adapters retain the shared error's `fid`, `site`, and `detail`, rather than selecting a competing binding failure:

| Original-nine consumer, all under `/tmp/tsukuroi-r20-binder-20261021/tools/` | Inspected adapter evidence |
|---|---|
| `check-locator-clarification.py` | `:782-795` |
| `check-root-dac-correction.py` | `:274-282` |
| `check-section-citations.py` | `:912-927` |
| `check-source-scope-correction.py` | `:636-649` |
| `measure-update-recheck.py` | `:471-481` |
| `check-boot-chain.py` | `:1572-1584` |
| `check-freshness-r17.py` | `:771-796` |
| `check-recheck-commands.py` | `:744-763` |
| `check-seat-scope.py` | `:260-272` |

The informational consumers in the same candidate directory likewise propagate the shared error: `check-adjacency-anchors.py:651-676`, `check-boot-writers.py:569-595`, `check-appended-notices.py:475-502`, and `check-registry-coverage.py:312-342`. Where consumers bind a second registry/baseline revision, the primary revision remains first. Informational `branch_tip` calls do not replace the original binding exception: B:125-131 and C:163-169 both absorb their own `RevisionError` and return `None`. Argument-parser and other pre-bind CLI failures are not newly attributed to the shared binder.

Declared controls retain branch-before-revision, revision-before-missing, missing-branch, not-pushed, unlanded-single-ID, origin-blob, and unavailable-repository expectations (B:207-235; C:245-263,357-366). A consumer also explicitly declares unknown-before-missing, missing-before-landed, and landed-before-invalid-origin cases at `/tmp/tsukuroi-r20-binder-20261021/tools/check-root-dac-correction.py:426-447`. These are inspected declarations only, not observed passing tests.

## Residual risk and verification gaps

- No runtime, import, Git command, test, build, lint, formatter, smoke check, external request, or host probe was invoked. No tool was installed or updated. Only this report was written.
- Baseline provenance rests on retained R20 bindings, the matching source copies, and the baseline-only oracle; the Git object itself was not extracted or authenticated under NO-EXEC.
- The precedence conclusion is conditional on object selection yielding the same commit and Git operation outcomes. It does not certify every ref/object ambiguity, corruption, timeout, concurrent ref change, or arbitrary consumer reachability path.
- The undefined-helper finding is source-grounded and unexecuted. It blocks treating the entire expanded selftest as established evidence; no C2 `0→9` measurement or saturation claim is made.
- No route/runtime integration, resume path, C1/C3 admission, host safety, boot-image safety, or boot clearance is assessed. Boot images remain UNKNOWN.

Scope: executed=none
