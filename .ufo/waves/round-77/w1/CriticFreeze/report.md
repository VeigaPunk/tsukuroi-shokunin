# CriticFreeze — round 77 w1

## Scope and finding

Axes: **depth (8, tied lowest)** and **freshness (9)**; calibration is affected if mechanical equality is represented as source understanding or complete claim validation.

Reviewed immutable declaration `eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5` against base `06f1bbbb803790b35358d277bb7807b82a9fab99`. **No false source-arithmetic or correction-text conjunct found in the frozen declaration.** This is a critic finding, not admission, scoring, integration approval, or certification of an eventual candidate. The strongest counterexamples expose the instrument's expressly bounded reach, not a reason to change its frozen predicate.

Durable command exits, full hashes, computed vectors, source literals and counterexample observations: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/w1/CriticFreeze/receipts.json`.

## Literal source and expected integrity

- `journald-manager.c:168`: `avail = LESS_BY(vfs_avail, metrics->keep_free);`
- `:170`: `space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use);`
- `:171`: `space->available = LESS_BY(space->limit, vfs_used);`
- `macro.h:325` subtracts only when the first operand is greater; otherwise returns zero. Lines 344–348 test the high bound first, then low, then input. These agree with every quoted source conjunct in the declaration.
- Independently recomputed `(avail, limit, available)`: A1 `(900,1000,900)`; A2 `(0,100,0)`; A3 `(0,100,0)`; A4 `(900,500,400)`; A5 `(0,300,200)`; A6 `(0,500,0)`. All six match; every number and addition is within uint64 and every `min_use <= max_use`.
- `patch_min_use`, lines 176–185, changes the startup minimum. A5/A6 must remain finite arithmetic examples, not assertions about startup-normalized metrics, current manager state, actual writable disk space, or guaranteed journald behavior. The declaration already makes that boundary.
- The entire expected specification was loaded from the frozen commit with duplicate-key rejection, not reconstructed selectively: six ordered A1–A6 objects, two complete source pins, three complete repair strings, and exactly the assigned predicate labels.
- Full expected SHA-256: `1469154cf9ce2b3c8bcaf6d8ee6698cca912c8ba8ea7e21452b47a5d31fa8694`.
- Full instrument SHA-256: `e686baf3a7b489f2b55c6fdd61b68600562e0adc6f595f892bf62c5d700b2878`, matching the frozen controls receipt.
- Source pins: macro `1bd38a180b2cccacf0732e3e5b6388ac3d71e453839236c388501080a11a75b8`; manager `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`. Both match frozen bytes and SHA256SUMS. Expected, instrument and both snapshots also matched working-tree bytes at capture. This is a point-in-time comparison, not assurance against later changes.

## C2 truth conjuncts

1. **R77-GATE-SHAPE:** The base lesson's Search log indeed says “rejected none this round.” Frozen outside closure section 3 explicitly agrees with substantive rejection decisions but disputes the absent Gate reject row. The repair carefully limits its supersession to a description of the whole round, rather than falsely saying none of the four screened snapshots was included. The rejected minimum formula contradicts the pinned subtraction; round-77 outside spot-check is correctly pending.
2. **R77-GATE-COUNT:** Direct immutable `780bad66cd0d62a58153bad541531ebc4f349c4e:corpus/SOURCES.md` row extraction gives **323**, including S323, not the base lesson's 322. The frozen repair's counting-command claim agrees with that independent extraction.
3. **R77-COLLISION-COUNT:** Frozen collision lists contain **323 registry ids, 147 staged ids and 124 exact intersections**, without duplicates. The complete registry list equals independently extracted base registry ids. Outside round-76 closure also states 124/147 and the continuing quarantine. **Limit:** staged ids were checked as the complete frozen list, not independently re-extracted from the quarantined package; no external staged-package provenance proof is claimed.

The base S320 row still explicitly teaches the false minimum formula. This is real inherited debt, not a false round-77 conjunct: the declaration names that debt and requires a scoped S325 supersession rather than editing historical S320. An eventual C1 claim without the promised source/companion explanation remains incomplete despite its count.

## Strongest counterexamples

Tests called the **unchanged frozen `evaluate` function**, compiled in memory, with reader mappings. No alternate judge/runtime, CLI execution, production fixture, or instrument change. Reported normalized exits below are derived from its Boolean result, **not observed subprocess exits**.

| Input | Claim | Count / met | Derived CLI exit | Meaning |
|---|---|---|---|---|
| Do-nothing base | C1 | 0 / false | 1 | Source snapshot missing; cannot reach target |
| Do-nothing base | C2 | 0 / false | 1 | None of the full corrective blocks present |
| Exact vectors, `source: []` | C1 | 0 / false | 1 | Literal sourceless JSON refused |
| Exact exposed vectors plus only `source: ["S324","S325"]`, pinned snapshots; **no registry or companion prose** | C1 | 6 / true | 0 | Source-id tokens are not source attribution/understanding |
| Same exact objects plus companion prose claiming minimum and universal startup state | C1 | 6 / true | 0 | Actual false explanatory conjunct escapes the mechanical count |
| Three exact blocks entirely inside an HTML comment | C2 | 3 / true | 0 | Hidden byte presence reaches the predicate without rendered correction |
| Three exact blocks preceded by “These are false statements, not adopted corrections” | C2 | 3 / true | 0 | Contradictory context escapes substring matching |

**Impact and smallest safe correction:** C1 counterexamples affect depth and potential calibration; C2 counterexamples affect freshness and potential calibration. Preserve instrument, expected and predicates exactly. Read the eventual companion prose, actual source rows and adopted correction context separately against the already-frozen full claim/kill rules. Disclose equality as six worked objects and substring presence as three exact blocks. Do not call either proof of understanding. A real false explanation or contradictory correction must be surfaced as an actual failed conjunct; do not silently narrow the claim to the numerical counter.

**Tradeoff versus defect:** The declaration explicitly exposes the numerical answers, denies a source-reading inference, requires reviewer reading and reserves closure. A minimal answer-copy reaching its finite predicate is therefore a declared limitation, not by itself a new contradiction. Missing/false companion content is a fixable candidate defect under the existing contract; changing the instrument after data to make that distinction executable would violate freeze. No observed production axis harm or eventual-candidate acceptance is inferred from synthetic attacks.

## Commands, exits and limits

- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5:SCORECARD.md` — exit **0**; read frozen round-77 declaration and inherited rejection precedents. Only round-77 data controlled this review.
- `sha256sum -c /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/before/src/SHA256SUMS`, cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/before/src` — exit **0**, both OK.
- Python Eval “Falsifying frozen finite acceptance” and “Completing immutable conjunct evidence” — completed without exception. Read-only `git show` subprocess argv/exits are retained in receipts; every recorded subprocess exited **0**. They read frozen expected/tool/snapshots, base lesson/registry, measured registry, collision lists, controls and frozen outside closure. Arithmetic and adversarial mapping results are recorded separately from process exits.
- Existing controls' selftest 16/16 and base CLI exits 1 were **read as prior receipts**, not rerun or relabelled as this seat's executions. No unrelated build, lint, selftest, host, package or service checks ran.
- No installs or updates. No credentials/raw journal messages, commits, pushes, git mutations, production changes, sibling writes, assimilation or promotion. Scratch `/fast/scratch/hyaku/tsukuroi-r77/CriticFreeze/` was the sole live scratch directory; explicit TMPDIR set to it; all test mappings stayed in memory. Durable receipts copied before the scratch directory was deleted.
- The alternative trailer `.ufo/waves/round-77/w1/CriticFreeze.md` lies outside the explicit sole-write directory. This report uses the narrower authorized acceptance path instead.

Self-evaluation: accuracy 4/5 (staged-package provenance not independently re-derived); completeness 4/5 (eventual integrated artifacts deliberately outside this pre-integration review); clarity 4/5 (mapping results carefully distinguished from CLI exits); actionability 4/5 (existing kill rules identify the safe correction, while closure remains external); conciseness 4/5 (full hashes and evidence tables retained for audit). Overall 4.0/5. Highest-impact remaining external check: independently bind staged-package ids and review the actual candidate's prose/source rows. These are limits, not self-granted admission. Would the user agree? The evidence and bounded conclusion are explicit.
