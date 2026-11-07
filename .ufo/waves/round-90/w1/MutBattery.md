# Round 90 / wave w1 — MutBattery (mutation tester)

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (git master). Lane revision at start of
work `ce89df93e5f576c5c236d4547299e9ea954e8853`; at the end of work `b380483e2a1d8edc97556fdd021794f619b6e1a6`
(the L1 landed the C2 entry + docs mid-wave). `git diff ce89df93 master -- tools/` is empty, and
the bytes I measured hash to the frozen digests, so both revisions carry the same battery and gate:

```
$ sha256sum tools/limine-pin-battery-r90.py tools/check-limine-pins.py
8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5  tools/limine-pin-battery-r90.py
4780da83ba411db1dc6afc250b618edc336a42790d79578018b40a2d7593a332  tools/check-limine-pins.py
$ git status --porcelain tools/            # empty
$ git show ce89df93:tools/check-limine-pins.py | sha256sum
4780da83ba411db1dc6afc250b618edc336a42790d79578018b40a2d7593a332  -
```

Freeze manifest line 1 (`.ufo/waves/round-90/before/freeze-manifest.sha256`) matches: `8f0daee8… tools/limine-pin-battery-r90.py`.

## Axes

1. **Operability (primary)** — does the frozen battery actually stop a wrong gate? Measured as
   kill/survive over 28 named controls (K2 + N01–N27) and reported per mutant.
2. **Freshness** — does each family still carry its own discriminating force, or is it dead weight
   whose deletion no control notices (per-family load-bearing table).
3. Cost — 761 battery runs total (~26 s per run; 14.6 min wall for the 667-run sweep at `-P 20`).

## Method (bound)

- Scratched the battery: `cp tools/limine-pin-battery-r90.py $S/battery.py`, sha256 verified equal
  to the freeze digest before any mutation.
- 43 mutants, three classes, every one a **textual patch with a `pattern absent` assertion**, all
  parse (`ast.parse`) and all read **`met` against the candidate gate first** (purity check; a
  mutant that fails the candidate is a re-scope, not a weakening — none did).
  - 23 mechanical weakenings of the oracle/families (`build_mutants.py`).
  - 20 single-family deletions (`build_famdel.py`), one per family that is the sole killer family
    of some control plus the r90 families that are not.
- Detector: the pristine battery's read of each control. A mutant is **DETECTED** iff ≥1 control
  that the pristine battery rejects (rc 1) reads `met` (rc 0) under the mutant. Every single-run
  escape was re-run with `--runs 3`; all 55 confirmations were `met=3 unmet=0` (stable, not a draw).
- K1 (`do-nothing`) was measured for the baseline but left out of the detection set: it fails all
  73 families, so it cannot discriminate between mutants.
- Host untouched; no lane file edited; no tool installed; nothing committed.

## Baseline (pristine battery, one run each, 30 runs)

```
$ python3 tools/limine-pin-battery-r90.py --gate tools/check-limine-pins.py --work "$S/work/w-candidate"
families_passed 73/73 verdict met failed -
rc=0
$ … --gate .ufo/…/controls/gates/K2-landed-adapter.py
families_passed 50/73 verdict unmet failed BAD-OVER-UNRESOLVED,BAD-RESOURCE,BAD-RESOURCE-OPTIONAL,DOUBLE-DOLLAR,EFI-IMAGE-MISSING,EMPTY-PATH,EMPTY-ROOT-RESOURCE,FIRST-PATH,FIRST-PROTOCOL,MEASURED-DECOY,MEASURED-FIRST,MEA…
rc=1
$ … --gate .ufo/…/controls/gates/N18-tpm-ignored.py
families_passed 70/73 verdict unmet failed MEASURED-TPM-ABSENT,MEASURED-TPM0,SECUREBOOT
rc=1
```

All 27 N-controls and K2 read `unmet`; K1 reads `0/73`. Full baseline log:
`w1/MutBattery/baseline/*.out` (with the per-control `failed` lists).

## Result summary

| class | mutants | detected | survived |
|---|---|---|---|
| mechanical weakening | 23 | 8 | 15 |
| family deletion | 20 | 13 | 7 |
| **total** | **43** | **21 (48.8 %)** | **22** |

## Detected mutants (control that escapes, confirmed 3/3)

| mutant | what it weakens | controls that now read `met` |
|---|---|---|
| M01-drop-on-panic-check | `and (want_op is None or got[6] == want_op)` removed (line 1436) | N16, N17, N18, N19, N20, N21, N23 |
| M02-pins-line-status-only | pin tuple compared as `(line,status)` only; `consequence` unchecked (line 1435) | N03, N07, N08, N09, N10, N11, N12, N13, N14, N15, N22 |
| M13-nonutf8-family-ascii | NON-UTF8 fixture made pure ASCII (line 1243–1245) | N26 |
| M14-large-file-shrunk | LARGE-FILE blobs 64–4096 B instead of 1.1–2.5 MiB (1228, 1232) | N25 |
| M15-roster-first-50 | FAMILIES+FAMILY_ROSTER truncated to the r89 prefix | N03, N04, N08, N09, N10, N11, N12, N13, N14, N15, N16, N17, N21, N22, N23, N25, N26, N27 |
| M20-drop-family-BAD-RESOURCE-OPTIONAL | family removed | N03 |
| M22-drop-family-PANIC-AFTER-PIN | family removed | N27 |
| M23-drop-family-DOUBLE-DOLLAR | family removed | N06 |
| F-del-FORMAT-BEFORE-BAD | family removed | N04 |
| F-del-NON-EFI-MISSING | family removed | N09 **and** N15 |
| F-del-PATH-PRECEDENCE | family removed | N11 |
| F-del-FIRST-PATH | family removed | N12 |
| F-del-FIRST-PROTOCOL | family removed | N10 |
| F-del-ENTRY-SCOPE | family removed | N14 |
| F-del-PROTOCOL-DECOY | family removed | N22 |
| F-del-MEASURED-VALUE-CASE | family removed | N16 |
| F-del-MEASURED-FIRST | family removed | N17 |
| F-del-MEASURED-IN-ENTRY | family removed | N21 |
| F-del-MEASURED-DECOY | family removed | N23 |
| F-del-LARGE-FILE | family removed | N25 |
| F-del-NON-UTF8 | family removed | N26 |

Verbatim single-run escapes (all re-confirmed `--runs 3` = 3× `verdict met`):

```
$ python3 $S/mutants/M02-pins-line-status-only.py --gate …/N07-any-key-panics.py
families_passed 73/73 verdict met failed -
rc=0
$ python3 $S/mutants/F-del-LARGE-FILE.py --gate …/N25-hash-first-mib.py
families_passed 72/72 verdict met failed -
rc=0
```

The consequence field is the single largest coupling: dropping the `consequence` comparison alone
frees 11 of 28 controls (M02). Dropping the `on_panic` comparison frees 7 (M01), i.e. all of R10's
control force flows through one expression.

## Survived mutants — properties no control pins

| mutant | property left unpinned | evidence |
|---|---|---|
| M03-drop-rc-field | `rc` field independent of exit code (line 1434) | 0/28 escapes |
| M04-drop-verdict-field | `verdict` string vs `rc` | 0/28 escapes |
| M05-drop-exit-code | process exit code (line 1434) | 0/28 escapes |
| M06-drop-r8-entry-labels | R8 `entry` label on every pin | 0/28 escapes |
| M07-drop-r8-panic-metadata | R8 `hash_mismatch_panic` {line,value} object | 0/28 escapes |
| M08-cases-per-family-1 | 4 draws per family (73×4 → 73) | 0/28 escapes |
| M09-drop-family-BAD-RESOURCE | R4 invalid-name→BAD-RESOURCE family in isolation | 0/28 (N01/N02/N05 keep other families) |
| M10-drop-family-EFI-IMAGE-MISSING | R9 "efi image missing ⇒ panic" family | 0/28 — no control is caught by it alone |
| M11-tpm-flag-always-absent | drawn `--tpm-present` on non-R10 families (line 1380) | 0/28 — vacuous dimension |
| M12-sbflag-never-drawn | drawn `--secure-boot-enforced 0` (line 1377) | 0/28 — vacuous dimension |
| M16-skip-blank-protocol-line | a `protocol:` line with an empty value (line 301) | 0/28 — no fixture writes one |
| M17-timeout-600 | 20 s per-case bound (line 129) | 0/28 — no control is slow |
| M18-drop-family-VALID-RESOURCES | the seven valid names' LP-UNRESOLVED family | 0/28 |
| M19-efi-protocols-drop-chainload | `efi_chainload` accepted as an efi protocol | **0/28 — no control is chainload-blind**; the mutant also silently stops generating the `efi_chainload` fixture, so it reads `73/73 met` on the correct candidate (see finding below) |
| M21-drop-family-MALFORMED-INPUT | MALFORMED-INPUT family | 0/28 — only K1 kills it |

The largest single finding is a **self-reference** in the fixture generator, not a gate hole: `fam_efi_image_missing`
emits its three protocol names from the same `EFI_PROTOCOLS` constant that `r9_image_lines` uses as
the oracle (line 976 vs 132). The pristine battery does test the spelling — a gate with
`EFI_PROTOCOLS = {"efi","uefi"}` is killed (`72/73 unmet, failed EFI-IMAGE-MISSING`) — but a
mutation of the constant is invisible: with the constant reduced the generator stops writing
`efi_chainload` and the correct candidate still reads `73/73 met`, so the property can vanish from
the battery while the verdict stays `met`. No frozen control notices this (M19, 0/28).

Second: **no control falsifies the blank protocol value.** A gate that reads `protocol:` with an
empty value as `efi` reads `73/73 met` under the pristine battery, and no fixture writes such a
line (M16, 0/28).

Third: **R8 is unfalsifiable by the control set** (M06, M07), and the three quarters of the
answer envelope (`rc` field, `verdict` string, exit code) each survive removal alone (M03–M05);
only the selftest's one-field lie wrappers cover those, and only when `--selftest --reference` is
run, which the C1 counting command does not.

## Per-r90-family load-bearing estimate

"Load-bearing" = deleting the family lets a named control escape (measured, 3/3). "Not
load-bearing" = measured deletion with zero escapes, or `[INFERENCE]` from the pristine killer
sets (a family is not singly load-bearing when every control that fails it also fails another
family).

| r90 family | load-bearing? | control(s) escaping on deletion |
|---|---|---|
| EFI-IMAGE-MISSING | **no against controls** (measured), yes against a chainload-blind gate: deleting it lets that gate read `72/72 met`, pristine rejects it `72/73` | — |
| NON-EFI-MISSING | yes | N09, N15 |
| PATH-PRECEDENCE | yes | N11 |
| FIRST-PATH | yes | N12 |
| FIRST-PROTOCOL | yes | N10 |
| ENTRY-SCOPE | yes | N14 |
| PROTOCOL-DECOY | yes | N22 |
| BAD-RESOURCE | **no** (measured) | — (N01/N02/N05 held by BAD-RESOURCE-OPTIONAL, RESOURCE-CASE, DOUBLE-DOLLAR) |
| BAD-RESOURCE-OPTIONAL | yes — sole pin of N03 | N03 |
| VALID-RESOURCES | **no** (measured) | — |
| BAD-OVER-UNRESOLVED | **no** (measured) | — |
| FORMAT-BEFORE-BAD | yes — sole pin of N04 | N04 |
| MEASURED-TPM1 | **no** (measured) | — |
| MEASURED-TPM0 | **no** (measured) | — (N18 still held by MEASURED-TPM-ABSENT + SECUREBOOT) |
| MEASURED-TPM-ABSENT | **no** (measured) | — (N19 still held by SECUREBOOT) |
| MEASURED-SB | **no** (measured) | — (N20 still held by SECUREBOOT) |
| MEASURED-VALUE-CASE | yes | N16 |
| MEASURED-FIRST | yes | N17 |
| MEASURED-DECOY | yes | N23 |
| MEASURED-IN-ENTRY | yes | N21 |
| LARGE-FILE | yes | N25 |
| NON-UTF8 | yes | N26 |
| PANIC-AFTER-PIN | yes | N27 |
| EMPTY-PATH (r90 expectation change) | **no** `[INFERENCE]` | killer set {K1,K2,N07}; N07 also held by FIRST-PATH, PATH-PRECEDENCE |
| DOUBLE-DOLLAR (r90 expectation change) | yes | N06 |

So 13 of 23 r90 families are load-bearing on their own; 10 are not, 4 of those (MEASURED-TPM1,
MEASURED-TPM0, MEASURED-TPM-ABSENT, MEASURED-SB) only because SECUREBOOT overlaps them and the
R10 tpm branches are otherwise redundant. Deleting all four R10 tpm families at once is untested
here and would be the natural follow-up; the measured single deletions do not let any control
escape, so R10's tpm semantics rest on SECUREBOOT's drawn `--tpm-present` plus these families.

## Proposed battery patches (for the L1; written here, not applied)

`w1/MutBattery/proposed-battery-patch.diff` (against `8f0daee8…`, r90 rules untouched):

1. **`tools/limine-pin-battery-r90.py:976`** — emit the three chainload protocols from a literal
   tuple in `fam_efi_image_missing` (`chainload = ("efi", "uefi", "efi_chainload")`) instead of
   `EFI_PROTOCOLS`, plus `assert chainload == EFI_PROTOCOLS`. Purpose: decouple the generator from
   the oracle so a constant edit cannot hide. Receipts: unpatched constant-drop reads `73/73 met`
   on the correct candidate (silent); with the assert removed, the patched battery reads
   `72/73 unmet, failed EFI-IMAGE-MISSING` on the same candidate (loud). With the assert in place
   the edit trips at import.
2. **`tools/limine-pin-battery-r90.py:1078`** (`fam_protocol_decoy`) — add after the first `c.pin("LP-MISSING")` an
   `efi_entry(c, None)` whose only protocol-shaped line is `protocol:` with an empty value, so a
   blank protocol value is exercised (R1 value = "" ⇒ not efi). Receipts: pristine reads
   `73/73 met` for a gate that treats a blank protocol as `efi`; patched reads
   `72/73 unmet, failed PROTOCOL-DECOY`, and the patched battery still reads `73/73 met` on the
   candidate.
3. Control-set gap (frozen, so report-only): no control falsifies R8 `entry` /
   `hash_mismatch_panic`, the `rc` field, `verdict`, exit code, the 20 s bound, or
   `CASES_PER_FAMILY`'s draw count. The selftest's lie wrappers cover the first five but are not
   part of the C1 counting command.

## Restoration evidence

Nothing in the lane was modified at any point; all mutations were copies under
`$S/mutants/`. Re-read after the run:

```
$ sha256sum tools/limine-pin-battery-r90.py tools/check-limine-pins.py
8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5  tools/limine-pin-battery-r90.py
4780da83ba411db1dc6afc250b618edc336a42790d79578018b40a2d7593a332  tools/check-limine-pins.py
$ git -C …/tsukuroi-shokunin status --porcelain tools/
(empty)
```

Scratch `/fast/scratch/hyaku/tsukuroi-r90/MutBattery` removed after copying receipts; receipts
(`baseline/`, `mutants/`, `sweep/`, `confirm3/`, both build scripts) live in
`.ufo/waves/round-90/w1/MutBattery/`.
