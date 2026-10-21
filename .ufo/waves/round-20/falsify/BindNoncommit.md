# BindNoncommit — R20 source-only review

## Scope and axes

- Axes reviewed: C2 object-type integrity, refusal/error identity, and whether the candidate's finite selector fixtures can reach their noncommit checks.
- Assigned candidate: `/tmp/tsukuroi-r20-binder-20261021`, as recorded in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:2-5`. Reviewed source snapshots: `tools/_revision.py#0A58` and `tools/check-revision-binding.py#4BEA`.
- Normative outcomes: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:37-47` requires a blob selector to produce `E-REVISION-INVALID`, exit 2, while a unique annotated-tag object remains commit-ish and peels to its commit. C2 is the original-nine, finite-fixture claim, not host or boot safety (`:13-19,65`).
- LSP unavailable: reading `xd://lsp` returned `No such tool`, with only `ast_edit` and `debug` mounted. No LSP status, references, definition, or diagnostics result could be obtained. The fallback below is textual source inspection, not semantic-reference proof.

## Findings, by severity

### P1 — The new selector probe calls `accepted` with an unsupported fifth argument, so its noncommit fixture cannot be reached

Evidence:

- `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:393-401` defines `accepted(sandbox, name, rev, expect_sha)`, with four parameters, and calls `run_tool` without a branch argument.
- Its new `object_selector_probes.exact_accept` calls `accepted(sandbox, name, revision, expected_sha, branch)` with five positional arguments at `:479-482`.
- The first positive shadow-prefix case invokes that wrapper at `:592-596`; the blob refusal is later at `:619`. Annotated-tag acceptance cases are also later at `:617-618`.
- `measure` invokes `object_selector_probes` for each present original-nine tool at `:663-669`. The CLI's generic exception boundary maps an exception here to `E-INTERNAL`, exit class 2, at `:1114-1118`.
- The independent judge selftest invokes the same measurement at `:1021-1030`, but its outer handler catches only `Cannot` at `:1086-1087`.

**Consequence [INFERENCE from Python argument binding and the displayed control flow]:** after successful fixture setup and the preceding refusal probes, the first positive selector probe raises `TypeError` before invoking the tool. The ordinary CLI reports `E-INTERNAL`, rather than producing the selector case report; the judge selftest lets the exception escape. In either path the new `noncommit_blob` case is not exercised. Thus these candidate sources cannot substantiate `object_selector_tools=9`, regardless of whether the underlying noncommit resolver is correct. This is a harness error identity, not evidence that a blob was admitted or that the binder itself returned the wrong refusal ID.

Recommended correction: make the helper interface and call agree while retaining branch forwarding and exact expected-commit checks. Do not remove the positive controls or weaken the blob refusal assertion to bypass the error.

### P2 — The binder selftest uses an undefined `git` helper before its tag and noncommit checks

Evidence:

- `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:69-77` defines `_git`; the selftest's local helper is `run` at `:210-216`. The module imports at `:30-39` introduce no `git` function.
- The newly added annotated-ghost loop nevertheless calls `git(repo, "rev-parse", ...)` at `:286-294`. Textual inspection of this complete module found no definition, import, or assignment binding that bare name.
- This call is outside `expect`; `expect` itself catches only `RevisionError` (`:198-208`). `__main__` calls `selftest()` without a surrounding exception boundary at `:378-380`.
- All tag-object peeling controls (`:315-329`), the ambiguity control (`:332-353`), the blob-selector refusal (`:359-362`), and the noncommit-origin error check (`:363-365`) occur after the undefined call.

**Consequence [INFERENCE]:** the fresh selftest reaches an unused candidate name in that loop and raises `NameError`, preventing its later checks and its documented PASS/FAIL summary (`:370-375`). The source contains a blob-refusal assertion, but that assertion is unreachable through this selftest entry point as written.

Recommended correction: use the existing appropriate Git helper rather than the undefined bare name, preserving the distinction between a returned process and `run`'s decoded string.

## Object-type and error-path review

No ordinary blob/tree/tag-to-noncommit admission was identified in the resolver's displayed control flow. This is a source conclusion under normal Git object/type semantics, not an executed result:

| Selected object | Candidate path and expected outcome |
| --- | --- |
| Unique commit | `_object_commit` returns the enumerated OID directly at `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:126-135`; `bind` then applies local landing and optional origin checks at `:180-192`. |
| Unique blob or tree | The type is neither `commit` nor `tag`, so `:133-137` returns `None`; `bind` raises the single `E-REVISION-INVALID` before consulting the local branch at `:177-183`. No type-filtered prefix selection admits a commit beside a colliding blob: object-count ambiguity is rejected first at `:119-124`. |
| Annotated tag to a commit, including nested tags | Only an already uniquely selected tag reaches `oid^{commit}` at `:139-142`. Successful peeling returns the commit identity, which is then subjected to the same landing/push checks. Acceptance here is expressly required by preregistration, not a noncommit bypass. |
| Annotated tag ending in a blob or tree | The `^{commit}` type assertion must fail; in a readable repository `:143-145` returns `None`, and `bind` emits `E-REVISION-INVALID` at `:177-179`. The independent resolver implements the corresponding type/peel paths at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:139-166,197-199`. |
| Noncommit object used as the origin ref, rather than as the revision selector | `_exists` is followed by `_ancestor` (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:186-191`); an ancestry-command status other than 0/1 is `E-GIT-FAILED` at `:156-160`. This is intentionally a different error identity from an invalid revision selector; the existing blob-origin fixture expects it at `:363-364`. |

The old production-lane source calls `_commit(repo, revision)` directly at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/_revision.py:134-145`; the candidate substitutes object enumeration/type selection at `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:172-183`. Thus the reviewed change is the actual new object-selection path, not merely its descriptive artifact.

A textual caller scan of the original-nine set (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:61-80`) found shared binding/refusal propagation in `check-locator-clarification.py:783-795`, `check-root-dac-correction.py:274-282`, `check-section-citations.py:913-930`, `check-source-scope-correction.py:638-649`, `measure-update-recheck.py:475-479,769-772`, `check-boot-chain.py:1572-1584`, `check-freshness-r17.py:772-795`, `check-recheck-commands.py:746-763`, and `check-seat-scope.py:261-265,663-665`, all under that candidate root. No caller-specific noncommit admission was found in those displayed binding boundaries. Additional shared consumers were located textually; this is not a semantic call-graph or reachability certification.

## Residual risk and verification gaps

- The selector measurement constructs a tag targeting `tip` at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:490-501`, tests its acceptance at `:617-618`, and supplies only a blob for noncommit refusal at `:619`. It does not provide a direct-tree, tag-to-blob, tag-to-tree, or nested-tag-ending-in-noncommit fixture. The binder selftest likewise provides a positive commit-target tag (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:315-323`) and a direct blob (`:359-362`), not those other type combinations. These are finite-coverage gaps, not demonstrated admissions. The stated C2 oracle itself names a blob, so missing other cases is not presented as a breach of its enumerated acceptance criterion.
- The findings above block reaching existing checks; no claim is made that those checks pass after the two source defects are corrected. No replacement-ref, corrupt-object, missing-object-storage, SHA-256 repository, or concurrent-object/ref-change behavior was established by this review.
- The baseline OID is taken from the assigned R20 artifacts. No Git diff, committed-blob identity, worktree status, runtime output, metric result, or test result was independently obtained. No independent runtime was invoked and no admission/integration judgment is issued.
- No code, tests, Git state, sibling report, routing, package, service, host, kernel, mount, or boot artifact was changed. Tools installed/updated: none. Boot images remain UNKNOWN; no host or boot-safety clearance is implied.

Scope: executed=none.
