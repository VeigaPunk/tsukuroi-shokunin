# Oracle08TagBlob — check-recheck-commands.py × annotated-tag→blob object ID selector

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-recheck-commands.py-TagBlob-expected-source-only
Lane bounds: leaf member — no subagent dispatch.

The digest above is the one the assignment supplied for the pinned binder
`.ufo/waves/round-21/snapshot/tools/_revision.py`, whose source is `tools/_revision.py`. Under
NO-EXEC I did not recompute it. The consumer `tools/check-recheck-commands.py` has no
snapshot copy (`snapshot/tools/` holds only `_revision.py`, `check-revision-binding.py` and
`check-seat-scope.py`), so I read the consumer from the working tree at review time. That
version is not pinned.

## Axes
1. Expected behaviour: exit code, status, findings and the `revision` field, derived without the binder's algorithm.
2. Whether the consumer passes `--revision` and `--branch` to the binder and maps its errors correctly.
3. Whether the round-20 judge matrix covers this case.
4. The smallest realistic weakening mutant the round-20 judge would miss.

## Fixture (what is selected)
`T` is a full-length annotated-tag object ID, made with `git tag -a <name> -m … <B>`, where `B`
is a blob object (`git hash-object -w`). The selector is the full 40-hex `T`, or 64-hex in a
SHA-256 repository. The fixture uses the full ID because a prefix could become ambiguous with
another object, which would test a different error path. `--branch` is the default `master`,
which exists. `--forbid` is the default and valid.

## Git object-type invariant (oracle basis, no binder code)
- An annotated tag object has exactly one `object <oid>` header and one `type <kind>` header,
  and both are set when the tag is created. Here the type is `blob`, which the fixture knows
  from how it built the tag.
- Object IDs are content hashes and objects never change, so `T` will always point at `B`, and
  `B` will always be a blob.
- A blob has no parents and points at no other object. Peeling `T` therefore ends at `B` and
  can never reach a commit.
- Contract step 3 of `_revision.py` (docstring lines 15–19) requires that the revision
  "uniquely matches an object ID, then peels to a commit". Step 3 must fail here, and steps 1
  and 2 pass. Under the first-failure-wins rule, the result is exactly one
  `E-REVISION-INVALID` finding.

The expected output needs only the documented contract and the type recorded at fixture
construction. It does not need `_object_commit`, `--disambiguate` or any `^{commit}` logic. In
the oracle, the type should come from fixture construction or from `git cat-file -p T`
reporting `type blob`. It must not come from calling `bind` or copying `_object_commit`.

## Consumer propagation (source-observed, `tools/check-recheck-commands.py`)
- Line 55 imports `_revision`, the module next to the consumer in `tools/`.
- Line 916 parses `forbid_list(args.forbid)` before binding. The default value is valid.
- Line 918 calls `_revision.bind(repo, args.revision, branch)`. It passes `args.revision`
  unchanged, with no lowercasing and no stripping, and `branch` is `args.branch`.
- Lines 919–921 handle `RevisionError` as follows:
  - set `tip = _revision.branch_tip(repo, branch)`;
  - re-raise the error as `Cannot(exc.fid, exc.site, exc.detail)`, keeping its id, site and detail unchanged;
  - leave `sha` and `origin_tip` as `None`.
- Lines 930–934 emit `CANNOT_EVALUATE` with `revision = sha or args.revision`, which is the
  selector echoed back, and with exactly one `Finding`. `counts` is `None`.
- Line 795 maps `CANNOT_EVALUATE` to exit code 2.
- No paths, files or exec log are read, because path expansion (line 923) comes after binding.

## Expected result (stated before any candidate output)

| field | expected |
|---|---|
| exit | 2 |
| `status` | `CANNOT_EVALUATE` |
| `findings` | exactly 1: `{"id":"E-REVISION-INVALID","site":"revision","detail":"<T as given> does not name one commit"}` |
| `revision` | the selector `T`, echoed byte for byte as given. It is not a commit SHA, not `B` and not a peeled value. |
| `branch` | `master` |
| `branch_tip` | full SHA of `refs/heads/master` in the sandbox. This field is informational. |
| `origin_tip` | `null`, because it is set only on successful binding |
| counts | `forbidden: []`, every `*_count` 0, no `exec_violation_count`, no `message` |

Full-SHA rule: an accepted binding has to report the full commit ID that the selector peels
to. Nothing in this fixture peels to a commit, so the correct outcome is a refusal. Reporting
`B` or `T` as an accepted revision, or getting any exit other than 2, means the consumer is
wrong. A `revision` field equal to `T` in a `CANNOT_EVALUATE` payload is only the echoed
selector, not an acceptance, as the comment at judge lines 482–483 says. Graders should check
the finding ID exactly. Checking only for exit 2 is not enough.

## Does the round-20 matrix cover it? No.
- The judge's `object_selector_probes` (snapshot `check-revision-binding.py` lines 475–673)
  covers four selector kinds:
  - direct blob, `noncommit_blob` (line 633), expected to be refused;
  - annotated tag pointing at a commit, `annotated_tag_object` and `annotated_tag_prefix` (lines 631–632), expected to be accepted;
  - ghost refs and ref-shadow selectors;
  - unlanded and unpushed selectors.
- `probe_tool` checks `blob-revision` (line 449). That case is also a direct blob.
- No judge case uses an annotated tag that points at a blob. A grep for `peel`, `to_blob` and
  `tag.?blob` finds only the judge's own `object_commit` helper.
- The binder's own selftest has `annotated-tag-to-blob-invalid` at `_revision.py` lines
  413–418. That test runs only inside the binder. It does not exercise the consumer and is not
  the independent judge.
- The consumer's own selftest (sections 14 and 14b, lines 1432–1455) has no case for a tag
  pointing at a non-commit.

## Smallest realistic weakening mutant the round-20 judge misses
Change the peel target in `_object_commit` at line 140 from `f"{oid}^{{commit}}"` to
`f"{oid}^{{}}"`. Mistaking "peel to commit" for "peel the tag" is a plausible error.

How each judge case fares under the mutant:
- A tag pointing at a commit still peels to that commit, so `annotated_tag_*` still pass.
- A direct blob is never peeled because it is not a tag, so `noncommit_blob` and `blob-revision` still pass.
- Every other round-20 case is unchanged.
- For a tag pointing at a blob, the mutant returns `B` as `sha`. Binding then reaches
  `_ancestor(repo, B, refs/heads/master)`.

[INFERENCE] `git merge-base --is-ancestor` rejects a blob with exit code 2 or higher (git's
"not a commit" fatal error). The binder would then raise `E-GIT-FAILED` instead of
`E-REVISION-INVALID`. The exit code stays 2, so only the exact finding ID shows the mutant.

A second mutant is equally invisible to the judge: when the peel fails but the repository is
readable, `return oid` instead of `None`.

Either mutant is caught only by a TagBlob row that requires
`binding_ids == ["E-REVISION-INVALID"]` with `finding_count == 1`. The judge's existing
`exact_refusal` helper already enforces that, so only the fixture row is missing.

## Limits and unknowns
- I did not recompute the SHA-256 of the binder, or of any other file.
- The consumer was read from the working tree because no pinned snapshot of it exists.
- The exit code of `merge-base` on a blob is inferred and was not observed.
- I did not check SHA-256-format repositories. With 64-hex object IDs only the selector length changes.

Scope: executed=none
