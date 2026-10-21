# FxC2Traversal — source-only traversal falsification

## Axes and disposition

Axes: rejection of noncanonical request spellings; literal allowlist matching; honest separation of source inference from runtime evidence.

**Bounded source verdict: holds for the assigned traversal, dot-component and double-slash families.** No source-visible acceptance counterexample was found in the reviewed control flow. This is a post-hoc recorded-request classification conclusion, not preventive runtime enforcement, filesystem resolution, symlink safety or proof of tool effects.

## Target and plausible defect challenged

Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`.

Plausible defect hypothesis: normalize a noncanonical absolute request into an allowed spelling before authorization, thereby accepting `LANE/x/../source`, `LANE/./source` or `LANE//source` because its collapsed destination is allowed. No such mutation was applied: the seat explicitly permits source-only falsification, not execution or source changes.

Here `LANE` denotes the literal `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; `src` is `LANE/source`, matching the existing selftest's declared read path.

## Source-visible detector reasoning

- Lines 33–36: `local(path)` requires the literal `LANE + '/'` prefix and checks every slash-separated component after the initial absolute-path separator. An empty component, `.` or `..` makes the predicate false. It does not collapse those components.
- Lines 43–56: `requested_path` strips only recognized read-selector suffixes, then calls `local`. Selector removal cannot remove a slash component: all recognized suffix forms are colon-delimited and contain no slash. A traversal component therefore remains present after any recognized selector is removed.
- Lines 87–91: `classify` records the returned path denial before attempting exact membership in the bound read paths. There is no resolution or normalization on this authorization route. The `PurePosixPath` import at line 7 does not participate in it.
- Lines 111–114: the binding paths themselves must also satisfy `local` (apart from the explicit read-only skill exception). A noncanonical spelling cannot be made valid merely by declaring it as an allowed local binding.
- Lines 138–151: for an otherwise valid complete trace, a path-denial finding produces exit code 1 and status `FAIL`.

For `LANE/x/../source`, the `..` component is rejected; for `LANE/./source`, the `.` component is rejected; for `LANE//source`, the extra separator produces an empty component. Leading double slashes fail the literal lane prefix. These outcomes do not depend on the collapsed destination being present in the allowlist.

## Expected fixture verdicts — source inference only

Assume the well-formed one-seat binding and complete one-event `read` trace constructed at lines 155–158, with exactly `src` and the skill URI in the read allowlist. None of the following fixtures was executed.

| Recorded path spelling | Expected exit / status | Expected finding |
|---|---|---|
| `LANE/source` | 0 / `PASS` | None; canonical positive control |
| `LANE/x/../source` | 1 / `FAIL` | `SCOPE-PATH-DENIED` |
| `LANE/./source` | 1 / `FAIL` | `SCOPE-PATH-DENIED` |
| `LANE//source` | 1 / `FAIL` | `SCOPE-PATH-DENIED` |
| `LANE/x/..//source` | 1 / `FAIL` | `SCOPE-PATH-DENIED` |
| `LANE/source/.` | 1 / `FAIL` | `SCOPE-PATH-DENIED` |
| `LANE/source/` | 1 / `FAIL` | `SCOPE-PATH-DENIED` |
| `LANE/x/../source:1-5:raw` | 1 / `FAIL` | `SCOPE-PATH-DENIED` after selector stripping |
| `LANE/./source:1-5:raw` | 1 / `FAIL` | `SCOPE-PATH-DENIED` after selector stripping |
| `LANE//source:1-5:raw` | 1 / `FAIL` | `SCOPE-PATH-DENIED` after selector stripping |

For each negative row under these assumptions, the inferred result has one finding at `A:0`, one violation and one total recorded request. Declaring any noncanonical local spelling in the binding instead is expected to produce exit 2 / `CANNOT_EVALUATE` with `SCOPE-SCHEMA`, not an authorized request.

Existing selftest source at lines 173–174 explicitly includes `LANE/x/../source` and `LANE/./source`. The listed selftest cases do not explicitly include a double-slash path or a traversal path combined with a selector. That is a bounded fixture-coverage observation, not evidence of acceptance or a killed/surviving mutant.

## Observed output, mutation verdict and restoration evidence

Observed evidence consists only of permitted local source reads. No checker, fixture, example, import, command, hash computation or other runtime was executed. There is no observed runtime exit code or runtime detector output. No mutant was created; killed/survived is therefore not established, and any runtime mutation-probe verdict is inconclusive. The completed source-only verdict remains the bounded rejection reasoning above.

The assigned SHA-256 is the supplied target identifier in the receipt below; it was not independently recomputed. Before/after computed hashes are unavailable under this seat's no-execution restrictions. This seat wrote no target, production or scratch-copy bytes, so it made no change requiring restoration. Exact byte equality against concurrent external changes was not independently checked. Its only write is this authorized findings report. No tools were installed or updated.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2traversal
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
