# MutBattery — round-91 w1: mutation probe of the frozen C1 battery

Seat: mutation-tester (leaf, no subagents). Report path: `.ufo/waves/round-91/w1/MutBattery.md`.
Receipts: `.ufo/waves/round-91/w1/MutBattery/`.

## Verdicts

| assignment item | result |
|---|---|
| battery mutants written (≥15 required) | **31** (26 pure weakenings + 5 model-changing probes) |
| purity ((a): mutant must still read `met` vs the candidate gate) | **26/31 pure**; 5 are not pure and are excluded from the control matrix (named below) |
| detection ((b): ≥1 control that the frozen battery rejects now reads `met`) | **4/26 pure mutants DETECTED** — 7 escape runs, each confirmed `met` 3/3 |
| mutants no control detects | **22/26 pure mutants** (coverage findings; the contract is not changed) |
| non-pure probes vs the controls (stage E, advisory) | 2/5 let their twin control escape (`N07`, `N06`) — the oracle moved onto the control's model, so no weakening is possible; 3/5 let nothing escape |
| r91 families load-bearing (deleting it lets a named control escape) | **2/11**: `PANIC-AFTER-PIN` (N01, N10) and `FIRST-LINE-ENTRY` (N03); the other 9 are not singly load-bearing |

No lane file was edited; no host path was written; no tool was installed or upgraded.

## Binding facts (measured)

- Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, `git rev-parse master` = `git rev-parse HEAD`
  = **2d7e09e101996cc1ac5836c6d635f3f608453ac5** (detached HEAD on the same commit).
- Frozen battery `tools/limine-pin-battery-r91.py` sha256
  **655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9** = the tasking digest.
  `sha256sum -c .ufo/waves/round-91/before/freeze-manifest.sha256` → every line `OK`; manifest
  sha256 `7f373954a30162e2992ae38a75d69d4c8bcef83e754d7a55098f394f5202adf2`.
- Candidate gate measured: `tools/check-limine-pins.py` sha256
  **62bb06c997fb99a9fd811ec97440eebe2dafa7e63c4f21f43aa0ead9af7da737** (blob at lane commits
  `45ae6518`, `3d645e2c`, `2d7e09e1`). The gate file changed at 23:47:47 during the wave: the
  wave-start tip `b516d6ae` held blob `dfc63548…`; commit `45ae6518` ("V1/U1 gate fixes") replaced
  it **before** the mutant matrix began (all matrix runs used a byte-identical snapshot,
  `gate/candidate-62bb06c9.py`).
- Controls: all 12 gates in `.ufo/waves/round-91/before/controls/gates/`; sha256 of each recorded
  in `MutBattery/control-gate-sha256.txt`. (N01 and N10 are byte-identical: both
  `7e158cd2…`.)
- Frozen battery vs candidate gate: `families_passed 82/82 verdict met failed -` — twice: on
  `dfc63548…` (23:46, before the landing) and on `62bb06c9…` (23:58, after it). This is the
  purity anchor for every mutant.
- Frozen battery vs the 12 controls (one run each) reproduces the wave's canonical family counts
  exactly: K1 2/82, K2 0/82, N01 81, N02 80, N03 81, N04 78, N05 2, N06 6, N07 76, N08 78,
  N09 78, N10 81 — all `unmet`. See `MutBattery/pristine-baseline.tsv`.

## Mutants and purity

31 mutants, one textual mutation each, `py_compile`d, AST-checked so that
`tuple(FAMILIES) == FAMILY_ROSTER` and that a dropped family is removed from both. Full diffs:
`MutBattery/mutants.patch`; generator: `MutBattery/gen.py`; hashes:
`MutBattery/mutant-sha256.txt`. Purity run: `python3 mut/<name>.py --gate <candidate> --runs 1`.

PURE (26; candidate reads `met`, so the mutation only weakens the oracle/fixtures):

| mutant | mutation | candidate |
|---|---|---|
| `DROP-<family>` ×11 | one r91 family removed from `FAMILIES` + `FAMILY_ROSTER`: PANIC-AFTER-PIN, GLOBAL-VS-ENTRY, FIRST-LINE-ENTRY, PANIC-GLOBAL-ONLY, MEASURED-GLOBAL-ONLY, MEASURED-IN-ENTRY, UNVERIFIED-IMAGE, UNVERIFIED-MIXED, UNVERIFIED-NON-EFI, UNVERIFIED-IMAGE-PATH, UNVERIFIED-SORTED | met 81/81 each |
| `NO-ONPANIC-COMPARE` | drops `got[6] == want_op` from the case oracle | met 82/82 |
| `NO-U1-COMPARE` | drops `u1_ok` (the `unverified_image_lines` equality) | met 82/82 |
| `NO-R8-ENTRIES` | drops the per-pin `entry` label check | met 82/82 |
| `NO-R8-PANIC` | drops the `hash_mismatch_panic` object check | met 82/82 |
| `NO-R8-ALL` | drops both R8 checks (compound) | met 82/82 |
| `NO-RCFIELD-COMPARE` | drops JSON `rc` == exit code | met 82/82 |
| `NO-EXIT-COMPARE` | drops process exit code == expected rc | met 82/82 |
| `NO-VERDICT-COMPARE` | drops the verdict string equality | met 82/82 |
| `NO-PIN-COMPARE` | drops the per-pin `(line,status,consequence)` equality | met 82/82 |
| `NO-CASE-COUNT-CHECK` | `met` no longer requires `len(log) == 82*4` | met 82/82 |
| `CASES-PER-FAMILY-1` | `CASES_PER_FAMILY = 1` | met 82/82 |
| `EFI-PROTOCOL-NO-BLANKS` | `efi_entry` writes `protocol:efi` with no blanks | met 82/82 |
| `ENUM-ONE-PROTOCOL` | EFI-IMAGE-MISSING draws 1 of 3 chainload protocols | met 82/82 |
| `ENUM-ONE-BAD-NAME` | BAD-RESOURCE draws 1 of 4 invalid names | met 82/82 |
| `ENUM-ONE-VALID-RESOURCE` | VALID-RESOURCES draws 1 of 7 valid names | met 82/82 |

NOT PURE (5; candidate reads `unmet`, so they change the expected answers, not just coverage):

| probe | mutation | candidate | changed families |
|---|---|---|---|
| `IMPURE-GLOBAL-WHOLE-FILE` | global section = whole file (undoes V1) | 79/82 | GLOBAL-VS-ENTRY, MEASURED-IN-ENTRY, PANIC-AFTER-PIN |
| `IMPURE-R9-IGNORE-PROTOCOL` | `r9_image_lines` ignores the protocol filter | 76/82 | ENTRY-SCOPE, FIRST-PROTOCOL, NON-EFI-MISSING, PROTOCOL-DECOY, UNVERIFIED-NON-EFI, UNVERIFIED-SORTED |
| `IMPURE-UNVERIFIED-INCLUDES-PINS` | every efi image line is listed unverified | 6/82 | 76 families |
| `IMPURE-WANT-ONPANIC-IGNORE-TPM` | `want_on_panic` ignores `--tpm-present` | 79/82 | MEASURED-TPM-ABSENT, MEASURED-TPM0, SECUREBOOT |
| `NO-BAD-RESOURCE-CONVERT` | `pin()` keeps the requested status instead of converting an invalid resource name to `LP-BAD-RESOURCE` | 79/82 | DOUBLE-DOLLAR, EMPTY-ROOT-RESOURCE, RESOURCE-CASE |

The five listed in the tasking as candidate weakenings split as follows: `r9_image_lines` ignores
protocol and `want_on_panic` ignores tpm are **not** pure (the battery's own expected answers bind
those model clauses); stopping the LP-BAD-RESOURCE auto-conversion is **not** pure either
(3 families rely on it); dropping the `on_panic` comparison, skipping the `efi_entry` protocol
blanks, `CASES_PER_FAMILY=1`, the enumerated-set reduction and the family deletion are pure.

## Escape matrix (26 pure mutants × 12 control gates, 312 runs)

DETECTED — the mutant lets a control that the frozen battery rejects read `met`:

| mutant | escaping control(s) | stage-B line | 3× confirmation |
|---|---|---|---|
| `DROP-PANIC-AFTER-PIN` | `N01-panic-whole-file`, `N10-panic-first-anywhere` | `81/81 met` | `81 81 81` / `met met met` (both controls) |
| `DROP-FIRST-LINE-ENTRY` | `N03-no-first-line-exception` | `81/81 met` | `81 81 81` / `met met met` |
| `NO-ONPANIC-COMPARE` | `N02-measured-whole-file` | `82/82 met` | `82 82 82` / `met met met` |
| `NO-U1-COMPARE` | `N05-no-unverified-field`, `N06-unverified-includes-pins`, `N08-unverified-unsorted` | `82/82 met` | `82 82 82` / `met met met` (each) |

Every other cell — 305 of the 312 stage-B runs — stays `unmet` (exit 1). Full matrix:
`MutBattery/matrix-stageB.tsv`; escape list: `MutBattery/escapes-stageB.tsv`.

NOT DETECTED — no control escapes (22 pure mutants):

`CASES-PER-FAMILY-1`, `DROP-GLOBAL-VS-ENTRY`, `DROP-MEASURED-GLOBAL-ONLY`,
`DROP-MEASURED-IN-ENTRY`, `DROP-PANIC-GLOBAL-ONLY`, `DROP-UNVERIFIED-IMAGE`,
`DROP-UNVERIFIED-IMAGE-PATH`, `DROP-UNVERIFIED-MIXED`, `DROP-UNVERIFIED-NON-EFI`,
`DROP-UNVERIFIED-SORTED`, `EFI-PROTOCOL-NO-BLANKS`, `ENUM-ONE-BAD-NAME`, `ENUM-ONE-PROTOCOL`,
`ENUM-ONE-VALID-RESOURCE`, `NO-CASE-COUNT-CHECK`, `NO-EXIT-COMPARE`, `NO-PIN-COMPARE`,
`NO-R8-ALL`, `NO-R8-ENTRIES`, `NO-R8-PANIC`, `NO-RCFIELD-COMPARE`, `NO-VERDICT-COMPARE`.

### Model-changing probes against the controls (stage E; not weakenings)

The five non-pure probes were also run against all 12 controls, for completeness. Two let a
control escape, and in both cases the control's defect is **the same model change** — the mutant's
oracle moved onto the control's answer, so the pair agrees and the battery has no independent
ground truth left to reject it. They are not usable as weakenings and are not counted as
detections.

| probe | escaping control | stage E | 3× confirmation |
|---|---|---|---|
| `IMPURE-R9-IGNORE-PROTOCOL` | `N07-unverified-non-efi` | `82/82 met` | `82/82 met` ×3 |
| `IMPURE-UNVERIFIED-INCLUDES-PINS` | `N06-unverified-includes-pins` | `82/82 met` | `82/82 met` ×3 |
| `IMPURE-GLOBAL-WHOLE-FILE` | none (N02 81/82 on `PANIC-AFTER-PIN`, N01 80/82, N04 81/82) | `unmet` | – |
| `IMPURE-WANT-ONPANIC-IGNORE-TPM` | none | `unmet` | – |
| `NO-BAD-RESOURCE-CONVERT` | none | `unmet` | – |

So N06 and N07 are rejected by the frozen battery only because the battery's oracle holds the r91
truth; a battery whose oracle moved to their model would accept them. The battery's own
expectations are load-bearing for those two controls, and the 12 controls cannot certify that the
battery keeps them.

Because the battery draws fresh fixtures per run, the five fixture-mutating mutants
(`CASES-PER-FAMILY-1`, `EFI-PROTOCOL-NO-BLANKS`, `ENUM-ONE-*`) were run a **second, independent
pass** against all 12 controls: 60/60 `unmet` (`MutBattery/secondpass-stageD.tsv`). In the pristine
data every control fails whole families deterministically (all 4 cases) except N08's
`EMPTY-PIN-LIST` (1 of 4 cases passes); `CASES_PER_FAMILY=1` therefore cannot flip N08 either —
it still fails `UNVERIFIED-IMAGE`, `UNVERIFIED-IMAGE-PATH`, `UNVERIFIED-SORTED`.

## Load-bearing per r91 family (deleting it lets a named control escape)

| r91 family | controls that fail it (pristine) | escapes when deleted | load-bearing |
|---|---|---|---|
| `PANIC-AFTER-PIN` | 7 | N01, N10 | **yes** (N01/N10 fail only this family) |
| `FIRST-LINE-ENTRY` | 6 | N03 | **yes** (N03 fails only this family) |
| `GLOBAL-VS-ENTRY` | 6 | none | no (N02 also fails MEASURED-IN-ENTRY) |
| `MEASURED-IN-ENTRY` | 6 | none | no (N02 also fails GLOBAL-VS-ENTRY) |
| `PANIC-GLOBAL-ONLY` | 4 | none | no |
| `MEASURED-GLOBAL-ONLY` | 4 | none | no |
| `UNVERIFIED-IMAGE` | 5 | none | no |
| `UNVERIFIED-MIXED` | 4 | none | no |
| `UNVERIFIED-NON-EFI` | 5 | none | no |
| `UNVERIFIED-IMAGE-PATH` | 6 | none | no |
| `UNVERIFIED-SORTED` | 6 | none | no |

Residual evidence that the pairs are joint, not single, checks:
`DROP-GLOBAL-VS-ENTRY` → N02 `80/81 unmet`, still failing `MEASURED-IN-ENTRY`;
`DROP-MEASURED-IN-ENTRY` → N02 `80/81 unmet`, still failing `GLOBAL-VS-ENTRY`.
The five U1 families are pinned collectively by the `u1_ok` equality (see `NO-U1-COMPARE`) but no
single U1 family deletion lets a control escape.

## What the frozen controls pin, and what they do not

Pinned by at least one control (a pure removal lets a control escape):

- the `on_panic` equality (`N02`; N04 improves 78→80 but still fails `FIRST-LINE-ENTRY` and
  `PANIC-AFTER-PIN` on pins);
- the `unverified_image_lines` equality (`N05`, `N06`, `N08`; N07 stays at 78/82 on the four
  R9/protocol families, N09 at 81/82 on `PATH-PRECEDENCE`);
- family `PANIC-AFTER-PIN` (`N01`, `N10`) and family `FIRST-LINE-ENTRY` (`N03`).

Not pinned by any of the 12 controls (surviving mutants — reported, contract untouched):

- R8 per-pin `entry` labels (`NO-R8-ENTRIES`);
- the `hash_mismatch_panic` object (`NO-R8-PANIC`): N01 also leaks pins, and `NO-PIN-COMPARE`
  leaves the object check failing, so no single removal frees it (`NO-R8-ALL` + `NO-PIN-COMPARE`
  together would, but that is a compound);
- `rc` JSON field == exit code (`NO-RCFIELD-COMPARE`), verdict string (`NO-VERDICT-COMPARE`),
  exit code itself (`NO-EXIT-COMPARE`);
- the per-pin `(line,status,consequence)` tuple (`NO-PIN-COMPARE`): every informant also leaks a
  second check (N01 → R8 object; N03 → `on_panic`; N07/N09 → R9 families);
- the case-count check (`NO-CASE-COUNT-CHECK`) and the fixture reductions (`CASES-PER-FAMILY-1`,
  `EFI-PROTOCOL-NO-BLANKS`, `ENUM-ONE-*`);
- 9 of the 11 r91 families.

Two by-products worth recording for the L1:

- K1 (r90 gate) reads 2/82 with the frozen battery but **79/82 with `NO-U1-COMPARE`**, still
  unmet on exactly the three V1 families. So the r90→r91 gate delta measured here is the U1 field
  plus GLOBAL-VS-ENTRY, MEASURED-IN-ENTRY, PANIC-AFTER-PIN; the "80 failed families" headline for
  K1 is dominated by the missing `unverified_image_lines` field.
- K2 (r90 adapter) stays 0/82 under every mutant (it errors on `--tpm-present`, 984 error cases);
  no battery property can change its verdict.

## Evidence (verbatim, exit codes included)

```
$ python3 base/battery.py --gate gate/candidate-62bb06c9.py --runs 1 …
families_passed 82/82 verdict met failed -                     # EXIT=0
$ python3 mut/DROP-PANIC-AFTER-PIN.py --gate …/N01-panic-whole-file.py --runs 1 …
families_passed 81/81 verdict met failed -                     # EXIT=0   (escape)
$ python3 mut/DROP-PANIC-AFTER-PIN.py --gate …/N01-panic-whole-file.py --runs 3 …
families_passed 81/81 verdict met failed -
families_passed 81/81 verdict met failed -
families_passed 81/81 verdict met failed -                     # EXIT=0
$ python3 mut/NO-U1-COMPARE.py --gate …/N05-no-unverified-field.py --runs 3 …
families_passed 82/82 verdict met failed -  (three times)      # EXIT=0
$ python3 mut/NO-R8-PANIC.py --gate …/N01-panic-whole-file.py --runs 1 …
families_passed 81/82 verdict unmet failed PANIC-AFTER-PIN     # EXIT=1 (no escape)
$ python3 mut/DROP-GLOBAL-VS-ENTRY.py --gate …/N02-measured-whole-file.py --runs 1 …
families_passed 80/81 verdict unmet failed MEASURED-IN-ENTRY   # EXIT=1 (joint family)
```

Run totals: 31 purity runs (26 exit 0, 5 exit 1), 312 stage-B runs (7 exit 0, 305 exit 1),
7 stage-C `--runs 3` confirmations (all exit 0, 3/3 `met`), 60 stage-D second-pass runs (all
exit 1), 60 stage-E non-pure probe runs (2 exit 0, 58 exit 1), 2 stage-F `--runs 3` confirmations
of the non-pure twin escapes (all exit 0, 3/3 `met`).

## Bounds observed

- Writes only in `.ufo/waves/round-91/w1/` (this report + `MutBattery/`) and scratch
  `/fast/scratch/hyaku/tsukuroi-r91/MutBattery/`; no lane edit, no git/jj mutation, no host write,
  no `sudo`, no `/boot`/`/efi`/`/etc`/`/usr`/`/var`/`/sys`/`/proc` write, no sysctl, no model
  selection, no subagents, no `agent://all` message, no pacman.
- One gate fact changed under the seat: `tools/check-limine-pins.py` went from `dfc63548…` to
  `62bb06c9…` at 23:47:47 (commit `45ae6518`), before the mutant matrix started; both blobs were
  measured with the frozen battery (82/82 `met` each) and the matrix used a pinned snapshot.

## Receipts

`MutBattery/ENVIRONMENT.txt`, `baseline-candidate.txt`, `METHOD.md`, `gen.py`, `mutants.patch`, `mutant-sha256.txt`,
`control-gate-sha256.txt`, `pristine-baseline.tsv`, `purity-stageA.tsv`, `matrix-stageB.tsv`,
`escapes-stageB.tsv`, `undetected.tsv`, `confirm-stageC.tsv`, `secondpass-stageD.tsv`,
`impure-stageEF.tsv`, and the per-run logs under `MutBattery/logs/{A,B,C,D,E,F}/`.
