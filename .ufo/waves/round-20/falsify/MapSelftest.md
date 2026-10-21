# MapSelftest — C3 selftest/live cell collision

## Finding

**Fixable finite mode-binding gap:** the candidate protects the exact live/selftest wording in the Verdict map cell, but does not bind that wording to the modes in the Entry command and Self-test cells. A one-token command-cell mutation can therefore leave `audit_live_map_errors=0` while the purported live entry invokes only the hermetic selftest. This is a source-derived counterexample, not an observed checker or host result.

The delivered round20 row itself is correctly labelled: its entry is `bash tools/boot-chain-audit.sh --live` (explicitly not live-run round20), its Self-test cell uses `--selftest`, and its map separates live `0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate` from selftest `0 PASS;1 FAIL` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:2109`). The defect is acceptance of a cell collision, not a claim that this row currently conflates the results.

## Exact status evidence

All audit-source citations below are in `/tmp/tsukuroi-r20-registry-20261021/tools/boot-chain-audit.sh`:

| Mode | Source-backed meaning | Evidence |
|---|---|---|
| Live, exit 0 | `TSUKUROI_BOOTCHAIN: CONSISTENT`; observation, not selftest PASS or boot clearance | `:794-806` assigns only `CONSISTENT`/0 or `UNKNOWN`/2. |
| Live, exit 2 | `UNKNOWN`; evaluation could not establish the bounded audit result | `:794-800`; live refusal paths also print UNKNOWN/2 at `:1249-1257`. |
| Selftest, exit 0 | `TSUKUROI_BOOTCHAIN_SELFTEST: PASS`; fixture assertions passed, not a live-host finding | `:104-108` says hermetic, no sudo, no /boot, no host read; `:1216-1218` prints the separate SELFTEST prefix and returns 0. |
| Selftest, exit 1 | `TSUKUROI_BOOTCHAIN_SELFTEST: FAIL`; failed assertions, not live DEGRADED | `:1220-1221`. The live header explicitly excludes a schema-v2 live exit 1 at `:81-86`. |

The source also documents selftest exit 2 for a harness error (`:108`). A bare exit code therefore cannot identify the mode or establish a host result.

The finite expectation is explicit: C3 is calibration, live 1 is forbidden, and `selftest1_only` is allowed rather than classified as live DEGRADED (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:21-27,49-53`).

## Smallest counterexample — design only

In an otherwise coverage-clean, uniquely highest operative table, preserve the entire corrected Verdict map and every other row. Change only the boot-chain-audit Entry command token:

- Before: `bash tools/boot-chain-audit.sh --live`
- After: `bash tools/boot-chain-audit.sh --selftest`

Leave the Self-test cell as `bash tools/boot-chain-audit.sh --selftest`. Both command cells now invoke the same fixture-only mode, while the Verdict map still advertises a live observation map. No command needs to be executed to expose this contradiction.

**[INFERENCE] Candidate result:** for a valid bound revision with otherwise clean coverage, the mutation still produces exit 0 / checker status PASS, no findings, and `audit_live_map_errors=0`. This follows from the candidate source, not a run:

1. `/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:270-288` requires the named probe row, the Entry cell's extracted path set, and whitespace-normalized equality of the Verdict map to `AUDIT_LIVE_MAP`. It never checks the Entry mode token or Self-test cell.
2. `:186-192,208-211` extracts tool paths, so changing the flag leaves both path sets unchanged. `:233-240` still finds the required probe codes in the untouched map.
3. `:247-255` only checks flags found in the Self-test cell against source text; that cell is unchanged and `--selftest` exists in the audit source (`boot-chain-audit.sh:1232`). It does not cross-check the Entry mode.
4. `:351-362` counts the empty map findings as zero and returns PASS when the remaining findings are empty; `:297-303` defines that checker status. Checker PASS is registry conformance, not the audit's live CONSISTENT status.

The inverse collision is also unguarded: changing only the Self-test cell to `bash tools/boot-chain-audit.sh --live` removes its recognized selftest flag, leaving the `:247-255` loop empty. This could present a live invocation as a selftest. It was neither applied nor executed here.

The declared green fixture asserts the canonical mixed-mode map passes (`check-registry-coverage.py:565-581`); the red fixture inserts live `1 DEGRADED` and asserts one map finding (`:583-590`). Thus literal `selftest: 0 PASS;1 FAIL` and negated `no live DEGRADED` are correctly accepted by the exact-text rule. The command-cell collision is outside that protection; this finding does not claim those declared assertions ran or failed.

## Impacted axes and smallest safe correction

- **Calibration (C3):** a zero documentation-map error count can coexist with an Entry command that cannot supply the advertised live result. Treating its selftest PASS as host observation would be false provenance.
- **Operability, bounded command guidance:** the inverse mutation can label a live invocation as fixture-only. No change to the separately claimed C2 metric is established by this review.
- **Safety limit:** neither selftest PASS, checker PASS nor live CONSISTENT clears any host/package/service/hook/initramfs/bootloader/reboot action. Boot images remain UNKNOWN here.

Bind the two command cells to the known finite modes within the existing boot-chain-audit check: require the documented Bash Entry command to select `--live`, the documented Self-test command to select `--selftest`, and reject missing, swapped or conflicting selectors. Preserve the current exact live/selftest map and no-clearance qualification. Add a declarative negative control for the one-token collision, expecting one `REGISTRY-AUDIT-LIVE-MAP` and `audit_live_map_errors=1`; retain the corrected selftest-1-only map as the admit control. This needs no general shell interpreter or arbitrary-program semantics claim.

If command/mode binding is intentionally excluded from the canonical finite-cell contract, the residual must remain an explicit limitation: zero proves only the selected Verdict map text, not the correctness of its documented invocation. The canonical judge, not this review, decides acceptance of that tradeoff.

## Limits

Read-only source/artifact inspection only. No candidate changes, fixture construction, tests, runtime invocation, host reads, external requests or installations. All predicted outcomes are static inferences conditional on a valid bound, otherwise coverage-clean revision. No host or boot safety claim is made.

Scope: executed=none
