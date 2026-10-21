# FxC2Selector — selector/parser source falsification

## Observed source

`requested_path(value, selector=True)` first denies URL-like spellings, then recognizes the approved `skill://godspeed` literal, and otherwise removes only a terminal chain of colon-prefixed selector tokens (`raw`, `img`, `conflicts`, numeric/range tokens). It then calls `local()` on the resulting base. `local()` requires the literal lane-root prefix and rejects controls, backslashes, wildcard/bracket/semicolon/colon characters, and empty, `.` or `..` path components. `classify()` subsequently requires the normalized path to be an exact member of the selected binding's `read_paths`; it does not use prefix matching.

The candidate's `selftest()` includes `selector`, using `src + ':1-5:raw'` where `src` is explicitly in `read_paths`, and declares expected exit 0. This is consistent with the parser: it removes the terminal selector chain and checks the exact bound `src` spelling.

## Falsification probes and expected verdicts (source-derived; not run)

- For this seat, the bound checker path with `:1-5:raw` normalizes to the exact bound checker path. Expected verdict: allowed (no finding), matching the selftest's selector case.
- An unbound local base such as `.../check-seat-bindings.py.unbound:1-5:raw` normalizes to the `.unbound` base, which is not an exact `read_paths` member. Expected verdict: `SCOPE-PATH-DENIED` (audit exit 1 for a complete, otherwise valid trace).
- A crafted interior colon such as `.../check-seat-bindings.py:unexpected/child:1-5:raw` leaves `:unexpected/child` in the base after stripping only the terminal selector chain; `local()` rejects the colon (and the path is not a bound exact spelling). Expected verdict: `SCOPE-PATH-DENIED` (audit exit 1 for a complete, otherwise valid trace).

No source-visible bypass was found for the tested distinction: a terminal selector suffix is treated as syntax on the same base path, while an unbound base remains unbound and a non-selector/interior colon remains subject to `local()` rejection. This conclusion is bounded to request-spelling classification; it does not establish what a filesystem resolves or what an underlying tool actually reads.

## Evidence limits / unresolved

No execution or runtime fixture observation was made. The selftest's expected selector verdict is source evidence, not an observed test result. The checker itself declares its scope as recorded request spellings only and disclaims runtime prevention, symlink/effect proof, reading proof, and universal trace completeness. The LSP device was unavailable in the supplied tool set, so no semantic references/callers were traced; findings above are based on directly read function bodies, not grep-derived semantic claims. The candidate SHA-256 is the assignment-provided target identity; it was not recomputed.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2selector
Scope: executed=none
