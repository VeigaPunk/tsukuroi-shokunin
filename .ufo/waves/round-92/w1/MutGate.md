# MutGate — held-out mutants of the V2 era clause (round 92, wave w1)

Seat: MUTATION-TESTER. Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
(git `master`, jj-colocated). Scratch: `/fast/scratch/hyaku/tsukuroi-r92/MutGate/`
(`TMPDIR=/fast/scratch/hyaku/tsukuroi-r92/MutGate/tmp`; deleted at exit).
Date: 2026-11-08.

Target clause: the V2 version-selected visibility rule of
`tools/check-limine-pins.py` — `parse_limine_version`, `VISIBILITY_ERA_SPLIT = (12, 9, 5)`,
`era_b`, the first-entry cut (`in_global`), the first-line-is-entry exception, the
`visibility_era`/`limine_version` reporting fields, and the `unverified_image_lines` (U1) list
under the era cut.

## Instruments and integrity

| item | sha256 (before = after) |
|---|---|
| gate `tools/check-limine-pins.py` | `af90ae637222a21b5c098ceed289e29cd010a629df143c2fcd8d92539839c123` |
| battery `tools/limine-pin-battery-r92.py` | `fde864ea29f1b61d9e8cdcb1063942e6c9b07bfdf81cec5766e804488542b166` |
| do-nothing battery `tools/limine-pin-battery-r91.py` | `655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9` |
| pristine gate copy `$S/gate-pristine.py` | `af90ae637222a21b5c098ceed289e29cd010a629df143c2fcd8d92539839c123` |

`sha256sum -c .ufo/waves/round-92/before/freeze-manifest.sha256` from the lane root: all 36
lines OK, including the three instruments above (lane observation: the tasking says 30 lines,
the manifest on disk holds 36 and every line verifies).
`git rev-parse HEAD` = `429fd1a34dfcdf951bf4aaedb2df4bc45835bede` (receipts from sibling seats
have landed on top of freeze commit `da99b2f4…`; no instrument byte moved).
Environment: `/usr/bin/python3` 3.14.8, bubblewrap 0.13.1 (`/usr/bin/bwrap`).
Nothing installed or upgraded; no pacman/uv/npx transaction was attempted.

## Method

- 20 one-clause mutants of the gate, each a **copy** under `$S/mut/Mxx.py`; the lane file was
  never opened for writing. Each mutant differs from the pristine bytes by exactly one hunk
  (M10/M11 repeat the same one-clause expression in the two return statements it occurs in;
  recorded as `hunks=2`, same clause).
- Primary detector (the seat's protocol):
  `TMPDIR=$S/tmp python3 tools/limine-pin-battery-r92.py --gate $S/mut/Mxx.py --runs 1 --work $S/w/Mxx --json $S/results/Mxx.json`
  → verdict `met` = 89/89 (SURVIVED), `unmet` = killed, with the failed families.
- Positive control: the pristine copy on the same command, three times.
  `89/89 met` on all three (work dirs `positive`, `pos2`, `pos3`; logs in receipts).
- Secondary detectors, to separate *instrument gap* from *equivalent mutant*:
  1. `python3 tools/limine-pin-battery-r92.py --usage-check --gate <copy>` (the battery's
     separate refusal mode: `12.9`/`abc`/`12.9.6.1`/`""` → rc 64; `12.9.4`/`12.9.5`/`13.0.0`/
     absent → rc 0).
  2. `python3 -I <copy> --selftest` (the gate's own 37-case selftest; not the judge).
  3. Differential probes: pristine vs mutant on one hand-built fixture that isolates the
     mutated clause, run as `python3 -I <copy> --conf … --esp … [--limine-version …]`
     (fixtures under `$S/probes/`, results in `probes.json`).

No run was inconclusive: every mutant returned rc 0/1 with a complete 89-family verdict, no
timeout, no `bad-output`.

## Mutant table (primary detector = 89-family battery, `--runs 1`)

| # | mutant (one clause) | rule violated / family semantics that can see it | failed families | verdict | judgment |
|---|---|---|---|---|---|
| M01 | `VISIBILITY_ERA_SPLIT = (12,9,4)` | V2 boundary: 12.9.4 must be era A (exception kept) | ERA-DEFAULT, ERA-FLE-MEASURED-A, ERA-FLE-PANIC-A, FIRST-LINE-ENTRY | killed 85/89 | non-equivalent, covered |
| M02 | `VISIBILITY_ERA_SPLIT = (12,9,6)` | V2 lower boundary at 12.9.5: every 12.9.5 case must be era B | — | **SURVIVED 89/89 ×2** | non-equivalent (probe P1), **coverage gap**: no era-sensitive family runs at 12.9.5 |
| M03 | `era_b = version < VISIBILITY_ERA_SPLIT` | both era directions inverted | ERA-DEFAULT, ERA-FLE-{PANIC,MEASURED}-A/B, FIRST-LINE-ENTRY | killed 83/89 | non-equivalent, covered |
| M04 | `measured_boot` read without the `in_global` guard | V1/V2 scoping of `on_panic` (measured key in entry body must be invisible) | ERA-FLE-MEASURED-B, GLOBAL-VS-ENTRY, MEASURED-IN-ENTRY | killed 86/89 | non-equivalent, covered |
| M05 | `era_b = False` (`--limine-version` parsed then ignored) | V2 selection itself: era-B first-line cases must differ from era A | ERA-FLE-MEASURED-B, ERA-FLE-PANIC-B | killed 87/89 | non-equivalent, covered |
| M06 | CLI default `12.9.6` | V2 default must be 12.9.4 when the flag is omitted | ERA-DEFAULT | killed 88/89 | non-equivalent, covered (one family) |
| M07 | parser accepts two components (`12.9`) | V2 refusal: version outside `X.Y.Z` is rc 64 | — | **SURVIVED 89/89** | non-equivalent (probe P4); **gap in the family run only** — `--usage-check` kills it |
| M08 | parser accepts one component (`12`) | same refusal clause | — | **SURVIVED 89/89** | same as M07 (probe P5) — `--usage-check` kills it |
| M09 | parser accepts `""` (returns `(0,0,0)`) | same refusal clause | — | **SURVIVED 89/89** | same as M07 (probe P6) — `--usage-check` kills it |
| M10 | `visibility_era` label swapped in both returns | reporting of the selected era | — | **SURVIVED 89/89** | reporting-only (battery ignores extra keys); non-equivalent as output (probe P7); gate `--selftest` kills it 33/37 |
| M11 | `limine_version` echoed as `"12.9.4"` in both returns | reporting echo of the selected version | — | **SURVIVED 89/89** | reporting-only, non-contract field (GATE OUTPUT CONTRACT: extra keys ignored); no detector kills it (probe P8) |
| M12 | cut applied one line early in era B (line before the first entry leaves the global section) | V1/V2 global-section extent: that line is global | ERA-GLOBAL-KEY-A, ERA-GLOBAL-KEY-B | killed 87/89 | non-equivalent, covered |
| M13 | cut applied one line late: first body line of a first-line entry visible to `hash_mismatch_panic` in era B | V2: after the label-end cut nothing in the entry body is global | — | **SURVIVED 89/89 ×2** | non-equivalent (probe P2), **coverage gap**: no era-B family puts `hash_mismatch_panic` on the first body line |
| M14 | first-line exception kept in era B for both keys | V2: the create_menu_tree rule has no exception | ERA-FLE-MEASURED-B, ERA-FLE-PANIC-B | killed 87/89 | non-equivalent, covered |
| M15 | first-line exception kept in era B for `measured_boot` only | V2 uniformity of the cut across both keys | ERA-FLE-MEASURED-B | killed 88/89 | non-equivalent, covered |
| M16 | first-line exception removed in era A (`era_b or True`) | V1/V2 era-A exception (`c > config_addr` guard) | ERA-DEFAULT, ERA-FLE-MEASURED-A, ERA-FLE-PANIC-A, FIRST-LINE-ENTRY | killed 85/89 | non-equivalent, covered |
| M17 | `measured_boot` scoped only when `not era_b` (whole file in era B) | V2 scoping of `on_panic` in era B | ERA-FLE-MEASURED-B | killed 88/89 | non-equivalent, covered |
| M18 | U1 image lines restricted to the pre-cut text in era B | U1 in era B (pins are parsed from the entry tree, not the global prefix) | — | **SURVIVED 89/89 ×2** | non-equivalent (probe P3), **coverage gap**: every U1 family runs at the default 12.9.4 |
| M19 | U1 image lines restricted to the pre-cut text in **every** era (control for M18) | U1 + R9 image-line semantics generally | EFI-IMAGE-MISSING, EMPTY-PATH, EMPTY-PIN-LIST, FIRST-PATH, FIRST-PROTOCOL, HOST-SHAPE, MEASURED-{DECOY,FIRST,GLOBAL-ONLY,IN-ENTRY,SB,TPM-ABSENT,TPM0,TPM1,VALUE-CASE}, MISSING, MULTI-FAULT, NO-PAREN, PATH-PRECEDENCE, PROTOCOL-DECOY, UNHASHED-DECOYS, UNVERIFIED-{IMAGE,IMAGE-PATH,MIXED,NON-EFI,SORTED} | killed 63/89 | non-equivalent, covered outside era B — shows M18 survives *because* of the era-B hole, not a dead detector |
| M20 | `hash_mismatch_panic` read from the whole file | V1/V2 scoping of the panic key | ERA-FLE-PANIC-B, PANIC-AFTER-PIN | killed 87/89 | non-equivalent, covered |

Totals: **12 killed / 8 survived / 0 inconclusive**. Killed mutants always failed the family
that models the mutated rule; no mutant was killed by an unrelated family.

### Actual outputs (representative failing case per killed mutant)

Payload is `(rc, verdict, pins, on_panic)` as the battery logged `want`/`got`;
`[3, 'LP-MISMATCH', 'panic']` = `(line 3, status, consequence)`.

| # | family | want | got |
|---|---|---|---|
| M01 | ERA-FLE-MEASURED-A | `[0,'HEALTHY',[[3,'OK','none'],[7,'OK','none']],'halt']` | `…,'menu'` |
| M03 | FIRST-LINE-ENTRY | `[1,'DEGRADED',[[3,'LP-MISMATCH','prompt'],[8,'OK','none']],'halt']` | `[[3,'LP-MISMATCH','panic'],…],'menu'` |
| M04 | ERA-FLE-MEASURED-B | `[0,'HEALTHY',[[3,'OK','none'],[7,'OK','none']],'menu']` | `…,'halt'` |
| M05 | ERA-FLE-MEASURED-B | `…,'menu'` | `…,'halt'` |
| M06 | ERA-DEFAULT | `[1,'DEGRADED',[[3,'LP-MISMATCH','prompt'],[7,'OK','none']],'menu']` | `[[3,'LP-MISMATCH','panic'],…]` |
| M12 | ERA-GLOBAL-KEY-A | `[1,'DEGRADED',[[6,'LP-MISMATCH','prompt'],[9,'OK','none']],'menu']` | `[[6,'LP-MISMATCH','panic'],…]` |
| M14 | ERA-FLE-MEASURED-B | `…,'menu'` | `…,'halt'` |
| M15 | ERA-FLE-MEASURED-B | `…,'menu'` | `…,'halt'` |
| M16 | ERA-FLE-MEASURED-A | `…,'halt'` | `…,'menu'` |
| M17 | ERA-FLE-MEASURED-B | `…,'menu'` | `…,'halt'` |
| M19 | MEASURED-FIRST | `[1,'DEGRADED',[[6,'LP-MISSING','panic']],'halt']` | `[[6,'LP-MISSING','not-modelled']]` |
| M20 | ERA-FLE-PANIC-B | `[1,'DEGRADED',[[3,'LP-MISMATCH','panic'],[7,'OK','none']],'menu']` | `[[3,'LP-MISMATCH','prompt'],…]` |

Full 356-case logs for every run (4 case rows × 89 families, with `want`/`got`/`error` per case)
are in `MutGate/case-logs/*.json.gz`; the run manifest is `MutGate/sweep.json`.

## Survivors — differential evidence and judgment

Each survivor was probed against the pristine gate on a fixture that isolates the mutated
clause; a difference proves the mutant is **not** equivalent, so a survivor is a coverage gap
in the named detector, never an equivalent mutant.

| probe | fixture / version | pristine | mutant | difference |
|---|---|---|---|---|
| P1 (M02) | first line `/e`, body `hash_mismatch_panic: no` + bad-hash pin; `--limine-version 12.9.5` | `visibility_era: 12.9.5+`, pin `(4, LP-MISMATCH, panic)` | `visibility_era: pre-12.9.5`, pin `(4, LP-MISMATCH, prompt)` | consequence flips at the boundary release |
| P2 (M13) | line 1 `/e`, line 2 `hash_mismatch_panic: no`, line 3 `protocol: efi`, line 4 bad-hash pin; `12.9.6` | pin `(4, LP-MISMATCH, panic)` (key invisible) | pin `(4, LP-MISMATCH, prompt)` (key visible) | first body line wrongly in the global section |
| P3 (M18) | `timeout: 5` / `/e` / `protocol: efi` / `path: /EFI/Linux/a.efi` (no URI shape); `12.9.6` | `unverified_image_lines: [4]` | `unverified_image_lines: []` | U1 reporting lost in era B |
| P4 (M07) | healthy conf, `--limine-version 12.9` | rc 64, no JSON | rc 0, `HEALTHY`, era A | refusal skipped |
| P5 (M08) | healthy conf, `--limine-version 12` | rc 64 | rc 0, `HEALTHY` | refusal skipped |
| P6 (M09) | healthy conf, `--limine-version ""` | rc 64 | rc 0, `HEALTHY` | refusal skipped |
| P7 (M10) | healthy conf, `12.9.6` then `12.9.4` | `12.9.5+` then `pre-12.9.5` | `pre-12.9.5` then `12.9.5+` | label inverted |
| P8 (M11) | healthy conf, `12.9.6` | `limine_version: 12.9.6` | `limine_version: 12.9.4` | echo wrong |

Secondary-detector outcomes on the survivors:

- `--usage-check`: pristine `met`; **M07, M08, M09 `unmet`** (rc 64 rows fail). The refusal
  clause of C2 is measured by this mode, not by the 89-family verdict.
- gate `--selftest`: pristine PASS 37/37; **M02 FAIL 35/37** (`era-b-global-key` era field,
  `version-parser` constant comparison), **M07/M08/M09 FAIL 36/37** (`version-parser`),
  **M10 FAIL 33/37** (all four era cases assert `visibility_era`), **M13/M18/M11 PASS 37/37**.
- Re-runs: M02, M13, M18 each reproduced `89/89 met` a second time (independent random
  fixtures). M07–M11 are deterministic per-version and were not re-run.

Judgments:

1. **M02 is the load-bearing defect in the C2 evidence.** The battery's only 12.9.5 case is
   ERA-GLOBAL-KEY-A, whose key sits in a real global section and therefore answers identically
   in both eras. No family distinguishes "split at 12.9.5" from "split at 12.9.6". A candidate
   gate that puts 12.9.5 in era A reads 89/89 met. C2's sentence "from 12.9.5" is therefore
   *not established* by the 89-family receipt; only the gate's own selftest (a non-judge) pins
   the constant.
2. **M13 and M18 are coverage gaps in the judge, not equivalents.** Both are caught by neither
   the battery's family run nor the gate's selftest, and both change modelled behavior
   (era-B global-section extent; era-B U1 list).
3. **M07–M09 are gaps in the 89-family path only.** The instrument does measure the refusal
   contract, but in the separate `--usage-check` mode; a C2 reading that cites only "89
   families x3" as its depth evidence does not cover rc 64.
4. **M10/M11 are reporting-only.** `visibility_era`/`limine_version` are outside the battery's
   stated output contract ("other extra keys are allowed and ignored"); M10 is still a lie the
   gate's own selftest catches, M11 is killed by nothing in the instrument set. Neither
   changes a pin, verdict, `on_panic` or rc, so they do not touch C2's behavioral sentence —
   they are named here so no one mistakes them for behavioral coverage.
5. The 12 killed mutants confirm each era clause is load-bearing in at least one family
   (boundary, direction, default, cut position ±1, per-key exceptions, whole-file scoping,
   U1 machinery when unguarded). The surviving set is concentrated exactly at the era edges
   the roster does not sample: the 12.9.5 release itself, the first body line after the cut,
   and era B under the U1 families.

## Restoration evidence

- The lane gate was never modified: `af90ae637222a21b5c098ceed289e29cd010a629df143c2fcd8d92539839c123`
  before the sweep and after it; `sha256sum -c` on the freeze manifest: OK.
- Battery bytes unchanged: `fde864ea29f1b61d9e8cdcb1063942e6c9b07bfdf81cec5766e804488542b166`
  before and after; manifest OK.
- All 20 mutants exist only as copies under `$S/mut/` (per-mutant sha256 in
  `MutGate/mutants.json`, diffs in `MutGate/mutant-diffs.diff`); the pristine copy under `$S`
  is byte-identical to the lane gate and was made read-only before any run.
- `$S` (`/fast/scratch/hyaku/tsukuroi-r92/MutGate/`) is deleted at exit; the receipts named
  above live in `.ufo/waves/round-92/w1/MutGate/`.

## Verdict

**Supports C2 for the landed gate on the inputs probed (pristine reads 89/89 met in 3/3
positive-control runs, and every era clause is load-bearing under mutation), but falsifies
that the 89-family battery establishes C2's depth:** M02 (split at 12.9.6) survives 89/89
twice and differs from the landed gate at 12.9.5 (P1), so the lower era boundary is unpinned
by any family; M13 (cut one line late) and M18 (U1 on the pre-cut text in era B) each survive
89/89 twice and are non-equivalent (P2, P3); M07–M09 (malformed `--limine-version` accepted)
survive the family run and are killed only by the separate `--usage-check` mode. Receipts:
`.ufo/waves/round-92/w1/MutGate/` (`table.json`, `sweep.json`, `probes.json`,
`secondary.json`, `case-logs/*.json.gz`, `mutant-diffs.diff`) — lane instruments unchanged
(`af90ae63…`, `fde864ea…`; freeze manifest OK).
