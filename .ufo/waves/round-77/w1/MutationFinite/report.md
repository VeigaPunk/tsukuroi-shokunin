# MutationFinite — round 77 w1

## Result

Axes: **depth 8 (lowest tied)** and **freshness 9**. Frozen declaration `eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5`; base `06f1bbbb803790b35358d277bb7807b82a9fab99`.

**should_fail_total=76; should_fail_accepted=0; killed=76; survived=0; inconclusive=0.** All 76 pristine controls and all 76 restored controls exited 0. All 76 mutants exited 1. This is a bounded actual-CLI load probe, not the instrument's helper-only selftest. No production changes or admission decision.

## Instrument, scope and commands

Read the frozen SCORECARD declaration, expected.json, SHA256SUMS, macro.h:320–350 and journald-manager.c:143–186. The driver asserted both current instrument and expected bytes equal their committed frozen versions before constructing data. It copied only the two pinned source snapshots into one isolated fixture and created the six-vector JSON plus three-block lesson there. The frozen specification is read by the actual CLI from its instrument root, not supplied by a replacement helper.

Executed command, exit **0**:

```sh
env TMPDIR=/fast/scratch/hyaku/tsukuroi-r77/MutationFinite/tmp PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/w1/MutationFinite/probe.py
```

Each subprocess used absolute argv below, cwd `/fast/scratch/hyaku/tsukuroi-r77/MutationFinite`, explicit TMPDIR above, and 15-second timeout:

```sh
/usr/bin/python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/measure-journal-arithmetic-r77.py --root /fast/scratch/hyaku/tsukuroi-r77/MutationFinite/fixture --claim C1
/usr/bin/python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/measure-journal-arithmetic-r77.py --root /fast/scratch/hyaku/tsukuroi-r77/MutationFinite/fixture --claim C2
```

Same command per claim ran pristine → single mutation → byte-exact restored fixture for every case. Full argv, cwd, TMPDIR, stdout, stderr, exit codes, mutated contents and before/mutated/restored hashes are preserved in **receipts.json**. **probe.py** is the reproducible driver; **fixture-descriptor.json** retains the minimal valid data/blocks, four fixture file digests and mutation names. No fixture tree survives.

## Mutation coverage

| Plausible defect | Cases | Expected detector | Actual |
|---|---:|---|---|
| Each A1–A6 output `avail`, `limit`, `available` independently +1 | 18 | C1 equality refuses one altered row | All exit 1, killed |
| Boolean substituted independently for each of eight numeric fields in each row | 48 | C1 exact integer type/equality refuses bool | All exit 1, killed |
| One extra row | 1 | C1 exact six-row shape | Exit 1, killed |
| Swap A1/A2 ordering | 1 | C1 ordered vector equality | Exit 1, killed |
| Duplicate `source` JSON key, second value otherwise valid | 1 | Actual duplicate-key JSON loader | Exit 1, killed |
| Empty source-id list | 1 | Exact S324/S325 source list | Exit 1, killed |
| Empty each pinned source snapshot independently | 2 | Pinned source digest | Both exit 1, killed |
| Remove each complete corrective block independently | 3 | C2 exact complete-block presence | All exit 1, killed |
| Only the three correction marker strings, no block bodies | 1 | C2 full-block matching, not marker matching | Exit 1, killed |

Representative full stdout (stderr empty):

```text
C1 pristine/restored, rc 0:
C1 predicate="six pinned arithmetic vectors match" count=6 met=1 reason=vectors
A1 avail +1, rc 1:
C1 predicate="six pinned arithmetic vectors match" count=5 met=0 reason=vectors
Duplicate JSON key, rc 1:
C1 predicate="six pinned arithmetic vectors match" count=0 met=0 reason=duplicate key
C2 pristine/restored, rc 0:
C2 predicate="three exact corrective blocks exist" count=3 met=1 reason=blocks
One corrective block removed, rc 1:
C2 predicate="three exact corrective blocks exist" count=2 met=0 reason=blocks
Marker-only strings, rc 1:
C2 predicate="three exact corrective blocks exist" count=0 met=0 reason=blocks
```

## Live controls

The initial valid isolated fixture passed C1 count=6 and C2 count=3, both exit 0. Two additional read-only current-lane `--root /home/vgpnk/Projects/shokunin/tsukuroi-shokunin` controls were captured during the running wave:

- C1 exit 1, count=0, missing `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/journald-space-arithmetic-r77.json`.
- C2 exit 0, count=3, met=1, reason=blocks.

These are time-local observations of a concurrently evolving production root, not a frozen-revision measurement or a baseline failure for these isolated mutants. All mutation verdicts use passing isolated pristine/restored controls.

## Restoration and immutable inputs

Every case's `exact_restoration=true`: all four fixture file hashes before and after each mutation equal the original pristine map. Final fixture hashes also match:

| File | Original = restored SHA-256 |
|---|---|
| Vector JSON | `0bab6f65b8c798427e7515abd3c551ecf1bdebcd14b56cee408a3924556e3d50` |
| Fixture lesson | `e522d3d2f7079fd589a37fb9e72405e265e80218be873e0f41ee2e34afe54349` |
| macro.h | `1bd38a180b2cccacf0732e3e5b6388ac3d71e453839236c388501080a11a75b8` |
| journald-manager.c | `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2` |

Instrument before=after: `e686baf3a7b489f2b55c6fdd61b68600562e0adc6f595f892bf62c5d700b2878`.
Expected before=after: `1469154cf9ce2b3c8bcaf6d8ee6698cca912c8ba8ea7e21452b47a5d31fa8694`.

The driver removed the entire own scratch directory in `finally`; receipt records `scratch_deleted=true`. Durable receipts and descriptors were emitted before terminal return. No git/jj mutation, delegation, package transaction, service action, credentials or journal-message read. Tools installed/updated: **none**.

## Verdict and limits

All assigned finite counter/load mutants were killed with clean baseline and restoration controls. No surviving mutant found in this battery. This demonstrates rejection sensitivity for the specified finite examples, source-byte pins and exact block strings, not source understanding, universal arithmetic correctness, repair truth or production readiness. No statement concerns startup-normalized metrics; numeric examples are the fixed small non-overflowing tuples with min_use ≤ max_use. L1 alone integrates and the non-author closure rules admission.

Self-evaluation (1–5; overall 4.0): accuracy 4, grounded in full process receipts but live-root observation is not revision-bound; completeness 4, all named probes covered but not an exhaustive malformed-input battery; clarity 4, categorical table summarizes machine receipts but exact per-case detail needs JSON; actionability 4, replay driver/descriptors retained but requires recreating deleted scratch; conciseness 4, evidence is necessarily detailed and full repeated subprocess outputs remain in JSON rather than prose. Improvement priorities: use frozen revision receipts for production admission, and keep the report's finite-coverage boundary explicit. User agreement expected because the requested controls, mutations, hashes and cleanup are evidenced without a broader claim.
