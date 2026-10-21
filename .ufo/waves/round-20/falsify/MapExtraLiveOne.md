# MapExtraLiveOne — C3 input-mutation design, not executed

## Scope and invariant

Axes: calibration of the operative live map; preservation of live0/live2 and the separate selftest map; detector specificity. Baseline identity: `0cbc34dd6b20896085a8fb07943e3ea4027d8472` (`.ufo/waves/round-20/worktree-bindings.json:2`). This report inspects the inherited registry candidate and exact R20 lane evidence only.

C3 requires the highest operative boot-chain-audit map to advertise live `0 CONSISTENT/observation` and `2 UNKNOWN/could-not-evaluate`; code `1` belongs to failed selftests, never live DEGRADED (`.ufo/waves/round-20/preregister.json:21-27,49-53`). The underlying candidate audit source independently supports this distinction: live summary selects only exit 2/UNKNOWN or exit 0/CONSISTENT, while selftest assertion failures return 1 (`/tmp/tsukuroi-r20-registry-20261021/tools/boot-chain-audit.sh:794-806,1216-1221`).

## One minimal mutant

**Proposed target, not edited:** the Verdict map cell of the corrected round20 `boot-chain-audit` row, whose source specimen is lane `SKILL.md:2109`, under the round20 heading at `SKILL.md:2096`. In an isolated fixture/copy, insert only `1 DEGRADED;` between the existing live0 and live2 entries. Do not change the evaluator, other cells, table heading, historical rows, or any audit-script behavior.

Before:

```text
live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance
```

Mutated:

```text
live: 0 CONSISTENT/observation;1 DEGRADED;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance
```

This preserves both correct live entries, legitimate selftest1, usage2, and even the contradictory `no live DEGRADED` qualification. It models accidental resurrection of a legacy live exit map. Merely finding the allowed digits or the disclaimer cannot reject it.

**Important pristine-control distinction:** the inherited registry worktree's own `SKILL.md` still has the round19 operative heading and legacy live1 row (`/tmp/tsukuroi-r20-registry-20261021/SKILL.md:2060,2073`). That row is already a red input, not a corrected pristine control. Use the corrected R20 specimen above or the candidate's corrected fixture. A failing historical/pristine baseline must not be called a killed mutant.

## Expected bounded detector and exact result

The declared detector is `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map` (`.ufo/waves/round-20/preregister.json:26`). This is a design reference, not an executed command.

[INFERENCE] Holding the candidate evaluator fixed and using otherwise coverage-clean, valid bound fixture revisions, the expected three-phase result is:

| Input | Exit / status | `counts.audit_live_map_errors` | Findings |
|---|---|---:|---|
| Corrected pristine map | 0 / PASS | 0 | none |
| Same map plus live `1 DEGRADED` | 1 / FAIL | 1 | exactly one `REGISTRY-AUDIT-LIVE-MAP` |
| Exact restored pristine map | 0 / PASS | 0 | none |

For the proposed line-preserving R20 specimen, the exact expected finding object is:

```json
{"id":"REGISTRY-AUDIT-LIVE-MAP","site":"SKILL.md:2109","detail":"schema-v2 live0/2 and separate selftest0/1 map required"}
```

A generated minimal fixture has its own row line number instead of 2109. Do not invent a revision or branch-tip value: output must identify the bound input revision.

The candidate selects the unique highest exact registry heading (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:137-183`) and compares the selected audit row's whitespace-normalized entire Verdict map against `AUDIT_LIVE_MAP`, not a required-substring set (`:31-34,270-288`). The insertion therefore produces the single specified map finding. The CLI counts map findings and returns FAIL when findings exist (`:350-362`); `_emit` maps that exit to status FAIL (`:297-303`). Generic probe coverage alone only requires code-token presence for 0 and 2 (`:233-240`), so it does not reject this particular insertion. The C3 option must be enabled.

The detector reads committed `SKILL.md` at the bound revision, not loose worktree bytes (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:90-107,341-348`). A loose-file mutation followed by an unchanged `--revision` would not exercise the mutant. No fixture, commit, ref, or other Git state was created here.

## Existing declared selftest coverage

**[INFERENCE] The registry candidate explicitly covers this exact input mutation; no missing fixture was found for this assigned shape.**

- `corrected_audit` uses the accepted map (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:565-568`).
- `legacy_map` performs exactly the proposed insertion, preserving live0/live2 and the remaining map text (`:569-574`).
- `audit-live-map-correct` explicitly enables audit mode and requires PASS, metric 0, and no findings (`:575-581`).
- `audit-live-map-live1` explicitly enables audit mode and requires FAIL, metric 1, and the finding-ID list exactly `["REGISTRY-AUDIT-LIVE-MAP"]` (`:583-590`). Thus accepting the extra live1 would fail this declared assertion.
- The historical-table controls require a corrected highest table to pass and a legacy highest table to fail even when the older table is corrected (`:592-613`). Historical live0/live2 text cannot rescue the mutant.

**Limit:** fixture coverage is not a scan of the current lane document. The registry `--selftest` builds its own temporary repository and resets `ROOT` to it (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:462-465`). A mutation only to the real R20 registry row does not enter those selftests automatically; the explicit revision-bound detector must inspect that row. Likewise, the audit script's declared `--selftest` runs its own audit fixtures, separately dispatched from live mode (`/tmp/tsukuroi-r20-registry-20261021/tools/boot-chain-audit.sh:876-888,1231-1246`), not a registry-document check. Passing selftests alone would not establish that the operative documentation is unmutated.

The R20 measurement script declares both selftest invocations and the separate C3 before/after revision checks (`.ufo/waves/round-20/measure/run.py:65-78`); these are declarations, not observed receipts in this report. The earlier build design independently names the same insertion and expected rejection (`.ufo/waves/round-20/build/MapExtraOne.md:12-22`), also explicitly without execution.

## Actual output, verdict, and restoration evidence

- Actual behavioral output: **none**. Pristine, mutated, and restored detectors were not run; all results above are predictions from source and declared assertions.
- Verdict: **INCONCLUSIVE / not executed** as an empirical mutation probe; neither killed nor survived. Static inspection predicts rejection and confirms a matching declared negative fixture, not an observed kill or passing selftest.
- Mutation/restoration: no source bytes were changed and no mutant scratch copy was created, so restoration was unnecessary. The only write was this named report.
- Before/mutant/after file hashes: **not measured / not applicable / not measured**. No byte-identity hash evidence is claimed, and the baseline commit identity is not substituted for a file digest.
- No tools were installed or updated. No command execution, external request, host probe, package/service/boot action, delegation, or Git-state write occurred. This finite documentation-map analysis gives no host or boot clearance; boot images remain UNKNOWN.

Scope: executed=none
