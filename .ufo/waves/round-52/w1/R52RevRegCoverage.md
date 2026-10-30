VERDICT: defect-found

# W-N4 — registry coverage review

Axes: operability; registry conformance. Bytes reviewed: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:SKILL.md` and the same revision's `tools/check-scrub-admission-r52.py`. No lane code changed; recommendation only, not admission.

## Findings (severity order)

### Medium — honest `none` does not satisfy the protocol's self-test requirement

Row conformant: **no against the full Gate standard**, although its eight-column registry shape and coverage pass. At the frozen revision, `SKILL.md:4558` labels `scrub-admission-r52` a gate and truthfully says `none: no self-test mode`. The frozen tool's `main()` parser exposes revision/fixture overrides, not a self-invocation fixture test. `/home/vgpnk/Projects/shokunin/PROTOCOL.md:385-389` requires every gate to expose an isolated self-invocation asserting exit code and a stable expected finding-id; `:402-403` requires that command/spelling in the registry. An external `controls/battery.py` pointer is not such a mode. Keep the truthful `none`; do not describe full Gate-standard compliance without resolving this discrepancy. This does not determine round admission.

### Low — measurement and pinned-value cells are under-specified

The same row (`SKILL.md:4558`) describes how the counter differs from round 51 in its Self-test cell instead of naming the GR rows/lint/w1 cohort/marks measurement. Its Pinned values cell reads only `Round-52 C1; same limits as scrub-admission-r51`, with no pinned-value path required by `PROTOCOL.md:402-403`. The prior row at `SKILL.md:4557` names the *w2* cohort; relying on it implicitly is ambiguous for round 52's w1. The frozen r52 tool docstring explicitly names GR1-GR3, lint, R52 seats and three marks, and points to `.ufo/waves/round-52/frozen/FROZEN.md`; its constants include `BASE = cc88b81d78bcbe06bce3f6bf722a108432ad276f` and the six-conjunct predicate. These are available, not missing prerequisites.

Suggested cell text (documentation correction only):
- Self-test: `none: no self-test mode; frozen GR1-GR3 rows, lint, the round-52 w1 18-seat cohort and three admission marks are the measurement; controls .ufo/waves/round-52/controls/battery.py`.
- Pinned values: `Round-52 C1; tools/check-scrub-admission-r52.py constants BASE/PREDICATE/ROWS and round bindings; .ufo/waves/round-52/frozen/FROZEN.md; same substance/forgery limits as scrub-admission-r51`.

## Required observations

- **Coverage PASS**, exit 0, at the requested revision. Command: `TMPDIR=/fast/scratch/hyaku/tsukuroi-r52/R52RevRegCoverage python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-registry-coverage.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`. Observed counts: `registered=89`, `tools_total=89`, `rows_total=89`, `missing=0`, `findings=0`, `findings=[]`. The displayed branch tip was `4ee3226daa221c72acab23eacaacc8f3c9616954`; the measured revision remained the freeze. Receipts: `R52RevRegCoverage/coverage.json` and `R52RevRegCoverage/coverage-receipt.json` beside this report. Coverage of this tool follows from that complete set plus the actual operative row; the output does not itself list registered names.
- Amended five-cheat map: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:SKILL.md | grep -c 'counter-cheats-r51.*cheats == 5'` produced **1**, exit 0. `SKILL.md:4560` explicitly requires `real_pass == 1 and cheats == 5 and cheats_rejected == 5 and r50_cheats_rejected == 0`. Receipt: `R52RevRegCoverage/five-cheat-receipt.json`. No stale four-cheat value in that operative cell.
- Name, kind, entry command, 0/1/2 verdict map, read-only/fixture-only write scope and owner `tsukuroi` are present in `SKILL.md:4558`. The six-conjunct map matches the frozen tool's PREDICATE and final run decision. Stale/insufficient cells are the two described above, not the five-cheat map.

## Residual risk and verification gaps

`xd://lsp` is unavailable (device read returned `No such tool`); inspection used immutable Git blobs and literal text, not semantic reference proof. Protocol citations are to the available fleet protocol, read-only, not a claimed freeze-revision protocol snapshot. Coverage is a structural registry check, not proof of self-test capability, cohort truth or admission. Ran only the two assigned checks; did not run the admission gate, controls battery, census selftest or C2 scorer. No runtime/rerouting/resume behavior was changed or claimed by this registry-only review. No tools installed. Scratch was removed in `finally` after receipt capture.
