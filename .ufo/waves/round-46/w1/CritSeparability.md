VERDICT: supports

## Axes
- C1 counter isolation: the C1 scorer does not read C2 claim surfaces; measured by its implementation file access.
- C2 counter isolation: the C2 scorer does not read C1 claim surfaces; measured by its implementation file access.
- Causal separability: scoring the designated partial trees yields the expected failure for absent claim legs without a crash.

## Findings

The C1 counter on base `2042117cfb724170772f4c128cc2ddba0b61d817` returned JSON and exit 1, not a crash: `identity_ok=0`, `tracks_ok=0`, `symlink_ok=0`, `unverifiable_ok=0`, `cli_ok=0`, `nowrite_ok=1`, `selftest_pass=1`, `selftest_r46=0`, `verdict=FAIL`. Observed details include unknown `--identity` on identity/tracking/symlink paths; selftest had 154/154 pass but no R46 labels. This is consistent with C1's absent claim leg, and is not cross-claim contamination. Command: `python3 tools/score-census-identity-r46.py --lane <fixture> --revision 2042117cfb724170772f4c128cc2ddba0b61d817 --scratch <scratch>/s`; output captured from this command (full JSON in task execution result, artifact `18188`, line 3).

The C2 counter on implementation `a44770491eb5ca15ce9f8b3207309d1af683ffaf` returned JSON and exit 1, not a crash: `r45_legs_ok=1`, `verdicts_ok=0`, `marks_ok=0`, `verdict=FAIL`. Detailed output showed no counted dispatches for every GR1–GR3 seat and no current section marks. Command: `python3 tools/check-scrub-admission-r46.py --lane <fixture> --revision a44770491eb5ca15ce9f8b3207309d1af683ffaf`; compact captured JSON in scratch `CritSeparability/c2compact.json` (observed line 1).

## Surface-access review

C1 counter's declared code reads only the target revision's `tools/tsukuroi-census.sh` plus synthetic files it creates under `--scratch`; source: `score-census-identity-r46.py:114-160`, `141-160`. Its target path constant is `CENSUS` at `:56`; it does not read C2's grounding entry, round-46 dispatch/results/reports, skill/readme marks, or C2 counter. Later references continue testing only the extracted census and synthetic fixtures (`:162-242`).

C2 counter reads the C2 grounding entry, round-45 counter, round-46 wave dispatch/results/reports, `SKILL.md`, and `corpus/README.md` (`check-scrub-admission-r46.py:56-71`, `95-203`, `218-257`). It does not read the C1 census script, C1 identity report/surface, or C1 counter. The `r45_legs` subcounter is executed in memory from the bytes fetched for the specifically named round-45 counter (`:192-203`), not as a separate C1 surface. Thus the counter file-access implementation supports the declaration of no cross-surface read. This is a code-reading conclusion, not strace evidence.

## Smallest safe correction

No correction indicated for the separability item: both counters produce their expected partial-tree FAIL states, while the independent axes remain isolated by their explicit target paths. Do not interpret either FAIL as an assertion that the full claim failed; these are intentionally incomplete trees.

## Receipts / limitations

C1's execution receipt is full JSON at artifact `18188` (line 3); C2 compact receipt was observed at `/fast/scratch/hyaku/tsukuroi-r46/CritSeparability/c2compact.json:1`. The fixture clone was rooted at `/fast/scratch/hyaku/tsukuroi-r46/CritSeparability/fixture` (checked with `git rev-parse --show-toplevel`); it was subsequently removed by the scratch cleanup trap. No repository surfaces were modified. I did not run `strace`; cross-surface access was checked by reading the counter code. No tools were installed.