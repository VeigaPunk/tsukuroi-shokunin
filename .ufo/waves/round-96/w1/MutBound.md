# MutBound — round 96 w1 scoped findings (C1 depth: gate mutants beyond the four frozen bends)

Seat dir: `.ufo/waves/round-96/w1/MutBound/` (full command/receipt report: `w1/MutBound/report.md`).
Lane gate under test: `tools/check-limine-pins.py`, frozen sha256 `7d79ac29…` (unchanged before/after).
All receipts cited below exist under `w1/MutBound/`; scratch `/fast/scratch/hyaku/tsukuroi-r96/MutBound/`
was used and deleted. No lane file was written; the bend emitters were not run.

## Mutants (8, one clause each; substitutions asserted to match exactly once)

| mutant | clause bent | battery (--runs 1) | families_passed | failed_families | error rows |
|---|---|---|---|---|---|
| M01-source-flag-always | JSON `limine_version_source` always `flag` | unmet | 101/103 | AUTO-ERA-A, AUTO-ERA-B | 0 |
| M02-source-probe-always | JSON `limine_version_source` always `probe` | unmet | 102/103 | EXPLICIT-VERSION-ECHO | 0 |
| M03-era-from-x-only | `era_b = X >= 12` | unmet | 96/103 | AUTO-ERA-A, ERA-DEFAULT, ERA-FLE-MEASURED-A, ERA-FLE-PANIC-A, EXPLICIT-VERSION-ECHO(1 case), EXPLICIT-VERSION-ERA(1), FIRST-LINE-ENTRY | 0 |
| M04-era-split-12-10-0 | split `(12,9,5)` → `(12,10,0)` | unmet | 96/103 | AUTO-ERA-B, ERA-B-FIRST-BODY, ERA-EXACT-125, ERA-FLE-MEASURED-B, ERA-FLE-PANIC-B, EXPLICIT-VERSION-ECHO(2), EXPLICIT-VERSION-ERA(2) | 0 |
| M05-y-cap-8 | Y component cap `<=8` | unmet | 102/103 | REFUSAL-VERSIONS-9DIGIT-Y | 4 |
| M06-z-cap-8 | Z component cap `<=8` | **met** | **103/103** | — | 0 |
| M07-echo-lower | echo `limine_version.lower()` | **met** | **103/103** | — | 0 |
| M08-refusal-9digit-below-1e8 | 9-digit component accepted only if value ≥ 1e8 | **met** | **103/103** | — | 0 |

Baseline (pristine copy, sha256 `7d79ac29…`): `met 103/103`, 412 cases, 0 error rows, exit 0. Restored
bytes (re-copied from the lane, same sha256) re-run: `met 103/103`, 0 error rows. Receipts:
`receipts/baseline-pristine.json`, `receipts/mutA-…` … `receipts/mutD-…`, `receipts/restore-pristine.json`,
derived table `summary.json` / `matrix.md`; mutant bytes + sha256 `mutants-manifest.json`.

## Frozen bends — own runs (not the emitter's)

| bend | verdict | passed | failed_families (frozen r95 counter) | error rows |
|---|---|---|---|---|
| N01-echo-wrong | unmet | 102/103 | `["EXPLICIT-VERSION-ECHO"]` | 0 |
| N02-y-cap-8 | unmet | 102/103 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | **4** |
| N03-era-label-flip | unmet | 102/103 | `["EXPLICIT-VERSION-ERA"]` | 0 |
| N04-extra-components | unmet | 101/103 | `["EXTRA-COMPONENT", "REFUSAL-VERSIONS"]` | 0 |

**N04 set exactly: `["EXTRA-COMPONENT", "REFUSAL-VERSIONS"]`** (4 + 4 failed cases). Receipts:
`receipts/bendA-N01-echo-wrong.json`, `receipts/bendA-N02-y-cap-8.json`,
`receipts/bendB-N03-era-label-flip.json`, `receipts/bendB-N04-extra-components.json`; official counts in
`receipts/countruns-bend*.txt`.

## New-family kill map

- `EXPLICIT-VERSION-ECHO` → M02 (4/4, source) and N01 (4/4, echo); also flags era bends M03 (1/4) and
  M04 (2/4) because its fixture is era-sensitive (pin consequence changes).
- `EXPLICIT-VERSION-ERA` → N03 (4/4, label), M03 (1/4, the 12.9.4 case), M04 (2/4, 12.9.5/12.9.6).
- `REFUSAL-VERSIONS-9DIGIT-Y` → N02 (4/4) and M05 (4/4), all rc-64 refusals.
- `EXTRA-COMPONENT` → N04 (4/4); the pre-existing `REFUSAL-VERSIONS` family kills the other 4.
- M01 dies only on pre-existing `AUTO-ERA-A`/`AUTO-ERA-B`.

## Findings

1. **F1 (Frontier): the Z component's 9-digit boundary is uncertified — M06 survives 103/103.**
   The landed gate accepts `12.9.999999999` (probe: rc 0, echoed, era B); M06 refuses it (rc 64). No
   family sends a 9-digit Z, so QUALITY 139's boundary rule holds for X and Y only.
2. **F2 (Frontier): a 9-digit component with leading zeros is unsent — M08 survives 103/103.**
   Landed accepts `000000001.0.0` (rc 0, contract: leading zeros normalized); M08 refuses it (rc 64);
   the battery is blind. Distinct from F1 (digit count, not position).
3. **F3 (equivalent mutant, not a gap): M07 `lower()` survives.** The parser admits only ASCII digits
   and two dots, the CLI rejects everything else before `check()`, and the probe returns digits/dots, so
   `lower()` is the identity on every reachable accepted version; probe stdout identical for `12.9.4`
   and `12.09.4` (`receipts/survivor-probes.json`).
4. **F4 (frozen-target discrepancy): N02 carries 4 error rows, not 0.** The four rc-64 refusals have
   empty stdout and the battery records `error="bad-output: JSONDecodeError rc=64 …"`; the frozen
   `count-runs.py` prints `"error_rows": 4` (M05, same clause, also 4). Family kill is exact; the frozen
   C1 sentence "each bend … 0 error rows" and the kill rule's "non-null error row" clause are
   contradicted by the instrument — the round-95 A1 relation recurring, needing an amendment, not an
   instrument edit. Every other bend/leg: 0 error rows.

{"seat":"MutBound","verdict":"findings","notes":"8/8 one-clause mutants scored with the assigned --runs 1 battery: killed M01 (pre-existing AUTO-ERA-A/B), M02 (new EXPLICIT-VERSION-ECHO), M03/M04 (new EXPLICIT-VERSION-ERA + pre-existing era families), M05 (new REFUSAL-VERSIONS-9DIGIT-Y); survived M06 (9-digit-Z cap), M07 (lower() equivalent), M08 (9-digit leading-zero refusal). Frozen bends own-run families exact: N01 [EXPLICIT-VERSION-ECHO], N02 [REFUSAL-VERSIONS-9DIGIT-Y], N03 [EXPLICIT-VERSION-ERA], N04 [EXTRA-COMPONENT, REFUSAL-VERSIONS] (101/103, 8 cases). Baseline and restored bytes 103/103 met, 0 error rows. N02 carries 4 error rows under count-runs.py, contradicting the frozen per-bend '0 error rows' clause (r95-A1 relation); receipts under .ufo/waves/round-96/w1/MutBound/."}
