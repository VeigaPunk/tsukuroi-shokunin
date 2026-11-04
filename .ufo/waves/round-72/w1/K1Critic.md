# K1Critic — round 72 (seat report)

Critique of the round-72 declaration (`6b42676`, base `a7015d27`). Full conjunct tables, measurements
and corrections: `.ufo/waves/round-72/w1/K1Critic/critique.md`; raw transcript:
`.ufo/waves/round-72/w1/K1Critic/controls.txt`.

**Verdict.** Not falsified as targets: all three predicates are measurable, every before-state
reproduces at `a7015d27` (note absent rc 128; `--selftest` rc 2/0 case lines; `ROUTED_STALE=3` rc 1;
registry 300; notes 89; digests and `sha256sum -c` ok; batteries 11/11 and 5/5 re-run), and the
drafted after-artefacts already read what the claims ask (counter `met=1` rc 0; `--selftest` rc 0
with 9 case lines; `ROUTED_STALE` reachable). What fails is claim-prose vs instrument: each of the
three targets survives a do-nothing/fabricated artefact, one cited red-before is not committed, one
host fact is false, one battery case does not test its clause, and the window arithmetic is wrong.

**Claims and axes.** C1 depth (8, tied lowest with adjacency 8) — SOURCED S301–S303, 6 MD rows,
counter `count-md-rows-r72.py`; C2 operability (9, capability `gate-selftest`); C3 freshness (9),
checker `check-r71-routed-r72.py`. Axes distinct, artefacts disjoint, each verifies alone.

**Controls (measured).**
1. C1 target reached by a note whose MD1 statement negates its own verbatim quote → `MD_VERIFIED=6`,
   `met=1` rc 0. The empty note fails (rc 1); the *fabricated* note does not.
2. C2 target reached by an echo: a `--selftest` printing seven PASS lines and `SELFTEST: PASS` with
   no fixtures and no core reads rc 0, 7 case lines, r70 self-demo still 214/18.
3. C3 target reached twice: 137 bytes of hand-typed receipt + one-line erratum + one-line
   "correction" with zero paths → `ROUTED_STALE=0` rc 0; and a *contradicted* pair ("No erratum is
   needed"; "there are not five or four … paths") → also rc 0. The committed green fixture of the
   routed battery already demonstrates the zero-path pass.

**Defects (9; severities and exact corrections in critique.md §4).**
D1 HIGH — `before/control/selftest-redbefore.txt` is cited by C2 but absent at `6b42676` (rc 128);
it is untracked and names a delete-with-scratch mutant. D2 HIGH — C3's SCORECARD/NOTE conjuncts are
substring tests; direction and the five paths are unchecked. D3 MEDIUM — `/proc/cmdline` carries
`zswap.enabled=1` and `zswap.max_pool_percent=25` (both real module parameters), so declaration (b)'s
"no `module.parameter` token" is false. D4 MEDIUM — C2 requires N ≥ 7 but names six cases; the
seventh is only in the uncommitted red-before; "stable finding id", the fixture build and the
"never `/tmp`" kill rule have no named measurement. D5 MEDIUM — the C1 battery's
`mutant-duplicate-id` case is killed by `snapshot-reuse` (`MD_VERIFIED=6`), so `duplicate-id` and
`ids-not-contiguous` have no isolating case (r71 erratum (d) class recurs). D6 MEDIUM — "window at
2 of 3" contradicts `AXES.md` and the r68/r70/r71 precedents (capability at r71 → **1 of 3**); no
duty change since depth is 8. D7 LOW — "canonical census validate rc 0" names no command (r71
erratum (c) recurred). D8 LOW — instrument docstrings say "eleven mutants"/"three red mutants" while
the code and receipts have 10/4. D9 LOW — "all under `before/` at base `a7015d27`": those 13 files
were introduced by `6b42676`; only the measured tree is at `a7015d27`.

**Residual limits.** C1's lexical channel (a negating row reads `met=1`) is disclosed in "planned";
the C1 verdict must say "lexically grounded", not "content-correct". The SOURCED binding is
self-attested through in-round registry labels; only the snapshot digests are byte-anchored.
`R71-RECEIPT-MISPATH` is a report-time promise, unverifiable now.

**Impacted axis.** Calibration (record accuracy) for D1–D9; measured axes unharmed if the frozen
predicates are read as frozen. The scoring hazard is C2: accepting the echo would make the
`gate-selftest` capability row false provenance. Nine append-only errata are requested; no frozen
predicate is amended.

CLAIMS=3
OVERCLAIMS=3
CONTROL_REACHES=3
D_ITEMS=9
