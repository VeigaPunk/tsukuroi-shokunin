# ConnectorScope — round 82 w1 report (connector)

Axes walked: depth · operability · calibration.

## Sibling overlap inventory

| item / query | owner lane | path:line | round | overlap verdict (owned / partial / free) | what this round should say about it |
|---|---|---|---|---|---|
| 1. Mutation-kill tooling for counters | `tameshi-shokunin` (runner), `kaidoku-shokunin` (batteries) | `tameshi-shokunin/tools/mutate-and-run.sh:2`, `kaidoku-shokunin/tools/round-67/mutation-battery.py:1` | tameshi r3-2 / probation r2 (`2a22adeb`), kaidoku r67 (`39a91a99d`) | owned | Tsukuroi must NOT claim mutation-testing of counters as new fleet ground. Tameshi owns generic runner; Kaidoku owns counter batteries. Tsukuroi legitimately adds: lane-local operability killing 17 genuine-gap mutants in *this* lane's counters (`count-mount-rows-r81.py`, `measure-round81.py`) via `--selftest`. |
| 2. Scorecard / self-assessment gate | `tabi-shokunin`, `kama-shokunin`, `souji-shokunin` | `tabi-shokunin/scripts/check-selfassessment.mjs:2`, `kama-shokunin/tools/round41-scorecard-reconcile.py:1`, `souji-shokunin/tools/souji-record-agreement.py:1` | tabi r24 (`f6f7f453`), kama r41 (`6fec0c4c`), souji r23 (`47652502`) | owned | Tabi owns cross-file self-assessment calibration (SCORECARD/LOG). Tsukuroi's C3 gate `check-scorecard-ordinals.py` (r82 `2786562e`) is a lane-local ordinal check enforcing exactly one standing *after* ordinal per (round, axis) and requiring explicit `supersedes-ordinal:` lines. |
| 3. Anchor / coordinate checking | `kumitate-shokunin`, `mori-shokunin`, `tameshi-shokunin` | `kumitate-shokunin/scripts/anchor-truth.mjs:3`, `mori-shokunin/tools/mori-anchor-check.py:2`, `tameshi-shokunin/tools/anchor-drift-sweep.py:2` | kumitate r38 (`e18ff1af`), mori r72 (`d2f55d8c`), tameshi r69 (`d958326e`) | owned | Kumitate/Mori own citation line & quote verification. Tsukuroi's C1 tool `check-anchor-coordinates.py` (r82 `2786562e`) does not claim general citation checking; it fixes a lane-specific XML tag-strip coordinate shift by checking exact raw spans `[first, last]` against a line-preserving strip. |
| 4. Systemd mount/fstab plane in corpus | `tsukuroi-shokunin` (sole owner) | `tsukuroi-shokunin/corpus/knowledge/mount-unit-fstab-plane-r81.json:52`, `.md:23` | tsukuroi r81 (`9e723336`) | free | Uncontested territory. No sibling holds `x-systemd.before`, `nofail`, or `fstab` under `*/corpus/knowledge/` (0 matches). Tsukuroi retains exclusive domain ownership under its recovery/boot-chain charter. |

## Commands run (read-only evidence)

- Sibling mutation tools: `find /home/vgpnk/Projects/shokunin/*-shokunin/tools -type f \( -name "*mutat*" -o -name "*kill*" \)` → found `tameshi-shokunin/tools/mutate-and-run.sh` (first commit `2a22adeb` r17; header cites r3-2), `kaidoku-shokunin/tools/round-67/mutation-battery.py` (commit `39a91a99d` r67), `kaidoku-shokunin/tools/round-76/mutation-check.py` (commit `98407fadb` r76), `kaidoku-shokunin/tools/round-84/mutation-closure.py` (commit `e0de2088a` r84).
- Sibling scorecard gates: `find /home/vgpnk/Projects/shokunin/*-shokunin -maxdepth 3 \( -name "*scorecard*" -o -name "*self-assess*" \)` → `tabi-shokunin/scripts/check-selfassessment.mjs` (commit `f6f7f453` r24), `kama-shokunin/tools/round41-scorecard-reconcile.py` (commit `6fec0c4c` r41), `souji-shokunin/tools/souji-record-agreement.py` (commit `47652502` r23).
- Sibling anchor tools: `find /home/vgpnk/Projects/shokunin/*-shokunin/tools /home/vgpnk/Projects/shokunin/*-shokunin/scripts -type f \( -name "*anchor*" -o -name "*coord*" \)` → `kumitate-shokunin/scripts/anchor-truth.mjs` (commit `e18ff1af` r38), `mori-shokunin/tools/mori-anchor-check.py` (commit `d2f55d8c` r72), `tameshi-shokunin/tools/anchor-drift-sweep.py` (commit `d958326e` r69).
- Corpus scan: `grep -rnI -i "x-systemd.before" /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge` → 0 sibling hits; `nofail` → 0 sibling hits; `fstab` → 0 sibling hits. Sibling corpus is 100% free of systemd mount/fstab content.
- Instrument hashes (frozen, verified on disk):
  `fedd45ce350b3d62f6fcc526c44bca4846abe7c533a35c3633318454c5acc3b3  tools/check-anchor-coordinates.py`
  `6e6d9715739e2231f8eba0f33bee2f017c436709b5e17188e7759e8d4fdf7c24  tools/mutation-kill-r82.py`
  `888a3da9b34dcbd4786a815f5656854c946d2168b7d73cc9f79c2eaa7c341e84  tools/check-scorecard-ordinals.py`
  `5e176afc62d475904e2accbc53b564d5689ac757204dd7c6ff11df395b83cb43  .ufo/waves/round-82/before/mutants-r82.json`

## Contested scope / contradictions for operator arbitration

1. **Frozen recipe literal `\\n` escaping defect**:
   In `.ufo/waves/round-82/before/mutants-r82.json`, `C16-empty-manifest` (`genuine_gap: true`) and `M06-mutation-unlink-noop` (`genuine_gap: false`) carry double-escaped newlines (`\\n`, characters 92 and 110) in their `old` fields:
   `C16`: `"if not digests:\\n        raise CannotEvaluate('snapshot-manifest-empty')"`
   `M06`: `"if mutation['action'] == 'unlink':\\n                    path.unlink()"`
   In Python source files, newlines are 0x0A (`\n`). Thus `source.count(old) == 0`, producing `recipe-missing:old-string-occurs-0x`. Under the frozen kill rule (`a recipe whose old-string no longer occurs is not a kill`), C16 cannot be killed. This caps `genuine_killed` at 16/17 and total `killed` at 22/26 (since C06/C07 are also unkillable equivalents). This defect was present at freeze commit `2786562e` (controls.txt line 48 records C16/M06 as `recipe-missing:old-string-occurs-0x`).
2. **Arithmetic contradiction on C2 target**:
   Target requires `killed >= 24 / 26` and `genuine_killed == 17 / 17`. With C16/M06 unmatchable and C06/C07 unkillable, maximum possible score without cheating is 22/26 total and 16/17 genuine.

## Bounded proposal (UFO-FSD connector synthesis)

- **Evidence**: `ExecAnchor` proves C1 depth met (count 8/8, exact raw spans :135-138 etc.); `ScribeOrdinal` proves C3 calibration clean (findings 0/77 via `supersedes-ordinal: round-81 depth`); `ExecMutCount` and `ExecMutMeasure` kill 16/16 achievable genuine mutants and 22/22 achievable total mutants, with C16/M06 blocked solely by the frozen JSON `\\n` string mismatch.
- **Affected axes**: operability (primary), calibration (secondary).
- **Proposed move**: Land C1 (depth 8) and C3 (calibration 9) cleanly. For C2 (operability), report C2 as unmet (16/17 genuine, 22/26 total) resulting from the frozen recipe JSON string-encoding defect, rather than attempting ad-hoc source workarounds that would pollute production code.
- **Risks**: C2 does not advance to ordinal 9 this wave without operator arbitration; however, honest reporting preserves calibration and avoids falsifying the frozen contract.
- **Verification**: Run `python3 tools/check-anchor-coordinates.py --fixture <lane>` (rc 0), `python3 tools/check-scorecard-ordinals.py --fixture <SCORECARD.md>` (rc 0), and `python3 tools/mutation-kill-r82.py --fixture <lane>` (rc 1, genuine 16/17).

## Honesty & bounds
No scratch directory left behind. No git mutations performed (`git add|commit|push|checkout` never run). Outside reads only.
