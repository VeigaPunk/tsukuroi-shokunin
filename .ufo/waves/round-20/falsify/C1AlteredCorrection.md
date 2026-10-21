# C1 altered/broadened correction selftest review

## Finding — Medium: the positive oracle is coupled to the correction constant, so a broadened canonical text can be self-approved

**Concrete mutation:** in `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py`, change the expected correction phrase at lines 45–47 from `Electron/JavaScript packages` to `all packages` (or an equivalent broader package scope). This should be rejected: the fixed R20 correction in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/ownership-correction.txt:1` limits the scope to Electron/JavaScript packages, and the checker’s own explanation at candidate lines 52–56 calls that the precise package scope and disclaims arbitrary packages.

The selftest does not independently pin that intended text. `OWNERSHIP_SECTION_LINES` is assembled from the mutable `OWNERSHIP_CORRECTION` constant (`check-adjacency-anchors.py:43–61`), and `ownership_valid` is then generated from those same lines (`:1089–1090`). The positive case accepts this generated fixture and expects count 1 (`:1110–1111`). The only correction-text alteration control replaces the separate ownership-negation phrase `It is not a tsukuroi grant of ownership.` with `It grants tsukuroi ownership.` (`:1118–1121`); it does not mutate or independently assert the package-scope phrase. Thus, with the proposed package-scope broadening in the constant, the valid fixture follows the broadened constant, while the existing altered control still changes the ownership-negation clause and is still expected to fail. By source inspection, the selftest can therefore bless a broadened canonical correction rather than catch it. No selftest was run.

The runtime exact-suffix comparison (`:171–175`) rejects text differing from whatever `OWNERSHIP_SECTION_LINES` currently defines, but that does not independently protect the intended correction: changing the constant changes the accepted suffix as well as the selftest’s positive fixture. This finding is about the selftest’s oracle coupling, not evidence that an unmodified candidate accepts arbitrary edits to `PROVINCE.md`.

## Residual risk and verification gaps

The review was limited to the candidate checker’s correction constants, validator, and selftest definitions plus the fixed lane correction. No tests or commands were executed; no LSP checks were performed. A direct test of the broadened phrase is absent from the visible C1 selftest cases.

Scope: executed=none
