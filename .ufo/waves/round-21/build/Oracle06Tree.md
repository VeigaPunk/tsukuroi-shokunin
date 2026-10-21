# Oracle06Tree — check-boot-chain.py × Tree object ID selector (expected, source-only)

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: check-boot-chain.py-Tree-expected-source-only

## Axes
- **A1 correctness of refusal** — exit/status/finding for a tree selector.
- **A2 propagation fidelity** — raw `--revision` string → `_revision.bind` unchanged.
- **A3 type-coverage depth** — which Git object types the round20 matrix exercises.
- **A4 mutant sensitivity** — minimal surviving weakening of the type guard.

## Call/argument propagation (consumer, read-only)
`tools/check-boot-chain.py:1573` — `binding = _revision.bind(ROOT, args.revision, branch)`;
`args.revision` passes through unmodified (metavar REV, line 834), `branch` = `args.branch`
(default `"master"`, line 1570). `RevisionError` is caught at 1578 and re-emitted as a single
`Finding(exc.fid, exc.site, exc.detail)` via `emit(Result(CANNOT,...), revision, branch, branch_tip)`
at 1584. Because the raise precedes `revision = binding.sha` (1574), the emitted `revision`
field is the literal `"unbound"` and `branch_tip` is `None` for any binding failure.

## Expected behavior for a Tree object ID selector (pre-registration)
Selector: 7–64-hex string (short unique prefix or full 40-hex OID) naming one **tree** object.
Binder path in `_revision.py`: `validate_branch` → `REV.fullmatch` passes (hex) →
`_object_commit` → `rev-parse --disambiguate=<lower>` yields exactly the tree OID (unique) →
`cat-file -t` → `"tree"` → `object_kind != "tag"` → `return None` → `bind` raises
`RevisionError(E-REVISION-INVALID, "revision", "<typed-selector> does not name one commit")`.

Preregistered consumer output (before any candidate output exists):
- **exit 2**, status `CANNOT_EVALUATE`.
- **exactly one finding**: `{"id":"E-REVISION-INVALID","site":"revision","detail":"<selector> does not name one commit"}` (detail echoes the selector as typed).
- **full-SHA semantics**: `revision` field is the literal `"unbound"` — no SHA is emitted for a refusal (contrast accepted commit/tag inputs, where `revision` = resolved full 40-hex commit SHA, lowercase, and `branch_tip` = local branch tip). `branch_tip: null`, `verdicted_kernel_entries: 0`, `entry_count: 0`. No `git show` reads occur; binding failure precedes all corpus I/O.
- Same result for a tree prefix that disambiguates to >1 object (`len(objects)!=1 → None`) and for any ref shadow — refs are never consulted; object IDs resolve before refs by design.

## Round20 matrix coverage of this pair — NO
`check-revision-binding.py::object_selector_probes` exercises commit (`tip`, prefixes,
uppercase, ref-shadowed), annotated tag (`tag_object`, `tag_prefix`, tag→commit peel),
**blob** (`noncommit_blob`), ghost selectors, and unlanded/unpushed commits. The only
non-commit, non-tag object probed is the blob. **No tree object ID selector case exists**
for any consumer, including `check-boot-chain.py` (present in `R17_GATES`, extra argv `()`).
This consumer/type pair is uncovered.

## Smallest realistic weakening mutant the matrix misses
Widen the commit branch by one clause in `_object_commit` (line 134):
`if object_kind == "commit"` → `if object_kind in ("commit", "tree")`. Every matrix case
passes unchanged (blob still falls to `!= "tag"` → INVALID; tags still peel; commits
unchanged), yet a tree selector now returns the tree OID as `sha`, and
`merge-base --is-ancestor <tree> refs/heads/master` exits non-zero/128 →
`RevisionError(E-GIT-FAILED, "refs/heads/master", ...)` → consumer emits
CANNOT/`E-GIT-FAILED` instead of CANNOT/`E-REVISION-INVALID`. One-token weakening,
observably wrong for this pair, invisible to the entire round20 matrix.

Second-order gap (worth recording): relaxations that merely move tree onto the tag peel
path — e.g. deleting `if object_kind != "tag": return None`, or `!= "tag"` → `== "blob"` —
are *equivalent mutants* on current Git (the `tree^{commit}` peel still fails → INVALID).
A black-box tree probe would not kill them either; they are guard-integrity weakenings
caught only by source inspection, so the preregistered oracle covers the observable axis
but cannot cover structural guard deletion.

## Oracle independence (no binder import)
Derive expectation from the Git object-type invariant, not the binder algorithm: Git has
four object types; `rev-parse <oid>^{commit}` is identity on commits, recursively peels
annotated tags to their target commit, and **fails on tree and blob** — a tree is reachable
*from* a commit but names none. So `cat-file -t <oid>` alone determines outcome:
`commit` → accept candidate; `tag` → one `^{commit}` peel decides; `tree`/`blob` →
E-REVISION-INVALID. Two independent git facts suffice; importing `_revision._object_commit`
would make the oracle circular. `check-revision-binding.py::object_commit` (lines 139–166)
is exactly this pattern — a reimplementation, not an import.

## Limits
- Source-only derivation; no execution, no sandbox. The exact `detail` string echoes the
  typed selector verbatim (case preserved); `site` is the literal `"revision"`.
- `merge-base` behavior on a tree operand is asserted from Git's object model (non-commit
  → fatal exit → `E-GIT-FAILED`), not observed here.
Scope: executed=none
