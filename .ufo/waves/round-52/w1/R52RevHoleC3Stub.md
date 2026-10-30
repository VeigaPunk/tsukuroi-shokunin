VERDICT: supports

## Axes
C3 adjacency correctness; displayed-pin identity binding; caller-override isolation; reproducible frozen-byte evidence.

## Findings by severity
No surviving instance of either assigned round-50 hole was observed. This is a scoped recommendation, not admission or integration.

All five commands ran the canonical `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-table-r51.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`, with the case-specific arguments recorded verbatim in the receipts below. Each receipt includes exit status, stdout, stderr, cwd and TMPDIR. Receipt paths below are relative to this report's sibling directory `R52RevHoleC3Stub/`.

| Case / receipt | Exit / verdict | Observed result |
|---|---|---|
| `baseline.json` | 0 / PASS | `display_forge_fails=1`, `stub_fails=1`, `override_blocked=1`, `r50_blind=1`; all full-predicate legs pass. |
| `adapted-stub-override.json` | 3 / OVERRIDE-NOT-MEASURED | Fabricated province, matching fabricated registry and scratch fake sibling cannot become a measurement. |
| `adapted-stub-control.json` | 1 / CONTROL-FAIL | Old shape legs remain 7/7, checker rc 0, pin/live content counts both 9; new display binding, quote specificity, digest binding and recipient counts are 0. `stub_fails=1` remains true, but this does not admit the adapted stub. |
| `false-display-override.json` | 3 / OVERRIDE-NOT-MEASURED | False displayed locator cannot become a measurement through caller input. |
| `false-display-control.json` | 1 / CONTROL-FAIL | `display_bound_ok=9` rather than 10; pin/live counts remain 9, quote specificity and digest binding remain 10. `display_forge_fails=0` on already-forged input; this is expected, not a failed baseline probe. |

**Baseline answer: both `display_forge_fails == 1` and `stub_fails == 1` still hold at the named freeze. Neither reconstructed hole scores PASS.** See `baseline.json:77-87` and the five command receipts; `summary.json` collects the comparable legs.

### Fixture fidelity
The prior report is `.ufo/waves/round-50/w1/R50CritCheatC3.md:10,14-16`. The adapted fixture retains the built-in stub's headings, finding/recipient/proposition text and quote; uses a committed scratch sibling named `fake`, its actual commit and blob digest, and adds OUT-007 and OUT-009 to their respective ADJ ownership cells so nine distinct references resolve. `adapted-stub.md`, `adapted-registry.json` and `fixture-identities.json` preserve those inputs and identity evidence.

The false-display fixture was a shared scratch clone detached at the freeze, with exactly the OUT-009 displayed locator changed from `revenger-shokunin/PROVINCE.md @ cf02419276e5` to `kagi-shokunin/PROVINCE.md @ deadbeefcafe`, leaving registry and digest appendix untouched. It was committed only inside its asserted scratch toplevel and its scratch origin/master advanced as in the prior report. `false-display.patch` preserves the sole mutation. The canonical freeze counter received that committed province through its documented override/control route; the requested measurement revision remained the freeze, not the derived fixture commit.

### Why rejection is real
Frozen `tools/check-adjacency-table-r51.py:110-140` binds each displayed path, commit prefix, heading and quote to its own registry row. Lines 317-320 reject overridden measurements before scoring; lines 357 and 397-403 require the display sensitivity probe and complete binding legs. Lines 412-415 distinguish CONTROL verdicts from measurement PASS. Numbered frozen source receipts are `check-adjacency-table-r51.py.numbered.txt` and `check-adjacency-table-r50.py.numbered.txt`; these citations refer to the frozen source, not mutable checkout assumptions.

## Residual risk and verification gaps
- The adapted control still reports `stub_fails=1` while its nine fabricated pin/live references resolve. That leg remains a narrow hard-coded negative probe, not proof against arbitrary fabricated evidence. The override gate and additional binding legs reject this case; do not attribute rejection to `stub_fails` alone (`adapted-stub-control.json`; inherited stub logic in frozen r50 source:333-349).
- `anchors_checker_rc=0` in both failing controls still certifies canonical lane inputs, not supplied fixture inputs. It must not be presented independently as fixture validation (`adapted-stub-control.json`, `false-display-control.json`; frozen r51:334-343 and r50:350-357).
- Only the two assigned constructions and the counter's built-in sensitivity were exercised. No claim of general semantic entailment, arbitrary coordinated registry/sibling-history forgery resistance, or host-shim resistance is made; frozen r51 docstring:62-69 names those limits.
- LSP was unavailable: `read xd://lsp` returned “No such tool”. Frozen-source inspection and literal search were used as fallback, not semantic caller/reference proof. No runtime, resume or rerouting code changed or was exercised.

## Provenance and execution hygiene
`source-identity.json` records SHA-256 and exact frozen/working-byte equality for the canonical counter, imported r50 counter, anchors checker and `_revision.py`. R51 hash: `cfe3ee233fde7600d95df14ace4421d7a55914f98483934e26078a6504eda3be`. All four matched before execution. No lane tracked content or fleet files were modified; only this report/receipts and seat scratch were written. No tools installed; no selftest-bearing commands run. Scratch free space observed before work: 450631577600 bytes. All fixture subprocesses completed before scratch removal; removal returned `scratch_removed True`. No additional battery was run.
