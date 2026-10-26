VERDICT: supports

# Item C1-2 — mutant "malformed rule" (probe_storage_arm accepts <5 counters)

Seat: C1MutMalformed (leaf, no subagents). Lane untouched (read-only). Scratch
`/fast/scratch/hyaku/tsukuroi-r38/C1MutMalformed/` removed at the end; receipts in
`.ufo/waves/round-38/w1/C1MutMalformed/`.

## Mutant

Target: `probe_storage_arm`, the malformed-error_stats gate at
`tools/tsukuroi-census.sh:1874` (`if [ "$nk" -ne 5 ]; then` — a device counts only when its
file carries each of the five counters exactly once; contract text at
`tools/tsukuroi-census.sh:357-361`). Weakened to `-lt 1`, so a device whose error_stats has
fewer than five counters (1–4 recognized counter lines) is accepted and its nonzero pairs
counted, instead of BLOCKED. Structural garbage (wrong key, duplicate, extra field,
non-integer → `nk=-1`) still blocks, isolating the "fewer than five" defect. Full diff:
receipt `mutant.diff`; mutant script: receipt `mutant.sh`
(sha256 e4a0aee1c5ec1042b95f536d98878c33f32d8cb722c40b589dfb210d4421dfe8; pristine copy
sha256 8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c, identical to the
lane file before and after — see Restoration).

## Harness 1 — census `--selftest`: KILLED

Baseline (pristine): `TMPDIR=$S bash $S/pristine.sh --selftest` → exit=0, stderr empty,
`TSUKUROI_CENSUS_SELFTEST: PASS (111 cases, 111 passed, 0 failed)`
(receipt `selftest-pristine.out`).

Mutant: `TMPDIR=$S bash $S/mutant.sh --selftest` → **exit=1**,
`TSUKUROI_CENSUS_SELFTEST: FAIL (111 cases, 110 passed, 1 failed)`
(receipt `selftest-mutant.out`; stderr receipt `selftest-mutant.err:1`). Exactly one case
fails, and it is a storage case — the one that pins the missing-counter rule:

```
FAIL healthy rollup: a missing counter is BLOCKED; the healthy sibling device still counts
(R38-C1): plane evidence missing: '^STORAGE btrfs-device-stats state=BLOCKED filesystems=1
devices=2 nonzero=1 detail=11111111:1:malformed,11111111:2:read_errs=2$'; got: PLANE
packages: HEALTHY (...)
```

(the `got:` dump in `selftest-mutant.err:1` is truncated before the STORAGE line, so the
mutant's actual line was captured by a direct probe instead — below.)

## Harness 2 — frozen counter `score-storage-arm-r38.py`: KILLED

Fixture clone per recipe: `D=$(mktemp -d $S/fx.XXXXXX)` →
`/fast/scratch/hyaku/tsukuroi-r38/C1MutMalformed/fx.NnQhwi`;
`git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D"`;
`git -C "$D" remote remove origin`; `git -C "$D" rev-parse --show-toplevel` = `$D`
(verified); branch `master`, base `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` (lane HEAD).
Mutant copied over `tools/tsukuroi-census.sh` and committed on master with fixture identity
(`-c user.name='C1MutMalformed fixture' -c user.email='c1mutmalformed@fixture.invalid'`):
mutant sha `111121e9c59369dcee38dd61b11671a592a8dac7`. Counter tools copied from the lane
working tree into the clone: `tools/score-storage-arm-r38.py` sha256
`e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218` — matches the declared
frozen counter (`e649bfb3...`); `tools/_revision.py` copied alongside.

Run (in the clone): `TMPDIR=$S python3 tools/score-storage-arm-r38.py --repo "$D"
--revision 111121e9c59369dcee38dd61b11671a592a8dac7 --scratch "$S/s"` → **exit=1**,
stderr empty, receipt `counter-mutant.out`:

```
 "revision": "111121e9c59369dcee38dd61b11671a592a8dac7",
 "predicate": "fixtures_matched == FIXTURES_EXPECTED and live_match == 1 and six_planes_all == 1",
 "fixtures_matched": 9,
 "live_match": 1,
 "six_planes_all": 1,
 "result": "FAIL",
```

The dropped fixture is the mutant's direct target, `F04-missing-counter`
(`counter-mutant.out`, fixture entry): expected `["BLOCKED", 1, 1, 0]`, got
`["HEALTHY", 1, 1, 0]` — the mutant accepted the four-counter device as healthy. The live
leg (real `/sys/fs/btrfs`, five-counter files) still matched (live_match=1), so the kill is
purely fixture-driven, as expected.

Baseline leg for the same detector (pristine, declared C1 implementation commit):
`... --revision 52ffd65f868431f021b8615ab281efd87195eac6 --scratch "$S/sp"` → exit=0,
`"fixtures_matched": 10, "live_match": 1, "six_planes_all": 1, "result": "PASS"`
(receipt `counter-pristine.out`). Baseline passes, so both verdicts above are conclusive.

## Direct A/B probe (mutant's actual STORAGE line)

Minimal fixture replicating the selftest `storage-malformed` case (fs
`11111111-2222-3333-4444-555555555555`, devinfo/1 with only four counters
write/read/flush/corruption all zero, devinfo/2 with read_errs=2),
`TSUKUROI_BTRFS_SYSFS=$FX/btrfs bash <script>` (receipt `ab-probe.out`):

```
pristine: STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=2 nonzero=1 detail=11111111:1:malformed,11111111:2:read_errs=2
mutant:   STORAGE btrfs-device-stats state=DEGRADED filesystems=1 devices=2 nonzero=1 detail=11111111:2:read_errs=2
```

The mutant silently downgrades a malformed error_stats file from BLOCKED to DEGRADED and
drops the `malformed` detail — the exact invariant the C1 census arm claims to enforce.

## Verdict table

| Harness | Detector | Mutant result | Verdict |
|---|---|---|---|
| census `--selftest` | 111-case hermetic selftest | storage-malformed case FAILs, exit 1 | KILLED |
| `score-storage-arm-r38.py` | 10 fixtures + live leg | fixtures_matched 9/10 (F04 BLOCKED→HEALTHY), FAIL, exit 1 | KILLED |

## Restoration evidence

- The lane was never written: only `cp` out. Lane census sha256 before =
  after = `8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c`
  (receipt `hashes.txt`); no git/jj mutation in the lane, no host mutation, no sudo.
- Scratch `/fast/scratch/hyaku/tsukuroi-r38/C1MutMalformed/` (including the fixture clone
  and the mutant) removed after receipts were copied; nothing left under /tmp (the
  selftest's own mkdtemp trees were created under TMPDIR=$S and cleaned by its trap).

## Not done / scope

- Only this one mutant was probed (assignment scope). The q82 `unshare -rm` counter
  (`score-storage-arm-r38-q82.py`) was not run — not in this item's harness list.
- No package installs or tool upgrades were needed; none performed.
- The mutant surviving neither harness is a kill of the mutation, not evidence about C2.
