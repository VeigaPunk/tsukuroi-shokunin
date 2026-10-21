# ScribeErrata — R20 append-only correction draft

Author round: TsukuroiR20, round20 attempt1. Seat: TsukuroiR19Recovery.ScribeErrata-2 (author-dispatched scribe; not outside closure). NO-EXEC; draft prose only. Immutable assigned baseline: `0cbc34dd6b20896085a8fb07943e3ea4027d8472`.

## Axes and behavior

C1 adjacency 8→8 (tied-lowest), C2 operability 9→9, C3 calibration 9→9; ordinal deltas all 0. This draft supports C3's named corrections, not an extra axis claim. It preserves the distinction between numerical tool coverage and semantic live-map accuracy, and between author swarm evidence and outside judgment. No production edit or R19 rewrite is performed.

## Evidence and provenance

`report:r19` below means fleet-root `/home/vgpnk/Projects/shokunin/.ufo/reports/round-19/tsukuroi.md`, not a lane-relative report. Other references are lane-relative unless explicitly stated.

- `report:r19:122`, appended erratum C3, says verbatim: “the operative `boot-chain-audit` verdict row no longer claims DEGRADED from the live probe.” `LOG.md:1023` repeats that assertion. Both are contradicted by the retained R19 operative row.
- `report:r19:78`, quality verdict, says verbatim: “all corpus/PROVINCE/SKILL edits are append-only (verified prefix checks in the round-18 closure style and by the no-harm gates above).” Outside closure explicitly records the SKILL exception.
- `SKILL.md:1997–2003` defines the unique highest-numbered complete registry table as operative, with older tables historical; `:2060–2073` identifies the round19 table and its `boot-chain-audit` cell `0 CONSISTENT;1 DEGRADED;2 UNKNOWN`. Historical round18 `:1965` instead says live 0/2 and selftest failure 1. Repairing the historical cell did not repair the then-operative cell.
- `tools/boot-chain-audit.sh:81–86` says no v2 verdict maps to DEGRADED; `:795–800` assigns live summary rc2 UNKNOWN or rc0 CONSISTENT. Selftest source at `:1216–1221` returns 0 for success and 1 for failed assertions; harness/usage failure may return 2. These are source observations, not executions.
- Outside lesson `corpus/lessons/round-19-verifier-spotcheck.md:5` supplies R19 provenance: round baseline `452a054677f6b18284917d7c08c45361f91c25ac`; measured revision `1f35705a5f08fc5cd80e2e6d4d7b79510a3ba6c2`; delivered tip `e1865d17725230c8c9f9bfa747b5fd8d5a98833e`; initial fleet report commit `dea61a93e6978c64131d163c771c7d9e5f40e6ec`; appended report erratum commit `d70ce4224ceef71300684f24649ea7cad7d15941`. These identities are cited from that lesson, not independently checked through Git by this seat.
- That lesson §2 C3 (`:79–92`) admits structural missing-row coverage 1→0 for 14 baseline tools, with three discovered tools separate, while explicitly refuting the operative-map assertion. §5 items2–3 (`:147–148`) routes the false erratum and reports committed SKILL `+80/−1`, with a historical row1965 changed in place; among PROVINCE/LOG/SCORECARD/QUALITY/README/SKILL, only SKILL failed the baseline-prefix test. The historical correction was stronger text, not demonstrated axis harm.
- Read during this seat: R20 draft corrections already appear in `SKILL.md:2084–2088`, a round20 table at `:2096–2118`, and `LOG.md:1031–1033`. These are concurrent L1-owned content, not edits or landed/measured evidence supplied by this seat.

## Draft for append in the R20 report/lesson only

### R20-FALSE-OPERATIVE-MAP — named correction to report:r19 erratum C3

The assertion in `report:r19` §“Erratum (attempt 2 follow-up, 2026-10-21)” C3 (`:122`) that “the operative `boot-chain-audit` verdict row no longer claims DEGRADED from the live probe,” repeated in the R19 LOG repair paragraph (`LOG.md:1023`), was false. At the delivered R19 tip, the highest selected registry was round19 and its boot-chain-audit row (`SKILL.md:2073`) still advertised live `1 DEGRADED`; only historical round18 row1965 had been corrected. The source's schema-v2 live summary returns `0 CONSISTENT` or `2 UNKNOWN`, never live DEGRADED; failed selftest assertions return 1. This corrects the supplemental semantic-repair assertion, not the separately verified R19 numerical coverage result (14 baseline tools, missing1→0; three discovered tools separate). The non-author R19 spotcheck §2 C3 and §5 item2 explicitly identified this incomplete repair. The false original statements remain visible as historical records; this correction supersedes them, rather than rewriting R19. R20's intended repair is a new highest operative table with the live/selftest distinction, subject to the separately recorded immutable measurement; candidate prose is not a passing receipt.

### R20-SKILL-PREFIX-EXCEPTION — named correction to report:r19 quality verdict

The append-only assertion in `report:r19:78` was inaccurate for SKILL.md. The outside R19 spotcheck records committed SKILL `+80/−1`: the historical round18 boot-chain-audit row1965 was corrected in place. Consequently SKILL did not retain its full raw baseline prefix, unlike the named PROVINCE, LOG, SCORECARD, QUALITY and README surfaces. This is a specific historical exception, not a general license to rewrite history, not a claim all other corpus content was exhaustively prefix-audited here, and not evidence of a demonstrated harmed axis. Keep the stronger historical correction and the filed R19 report bytes; disclose the exception in this R20 correction. R20 should append its superseding current registry without representing the R19 SKILL delta as wholly append-only.

### Outside closure is not the author swarm

The R19 fleet-report erratum's “66 independent seat reports” (`report:r19:126`) describes author-dispatched falsifiers, not independent non-author closure. They remain author-side evidence. The outside judgment is the separately authored `corpus/lessons/round-19-verifier-spotcheck.md` (author/provenance at :1–7, distinction at :138–140): its bounded admission of R19's three declared claims does not accept every supplemental assertion, certify universal registry semantics, or clear a boot/package/service action. This R20 scribe and other author-dispatched R20 oracle/falsifier seats do not constitute new outside closure. R20 admission and outside closure remain pending.

## Gates and measurements

Exact executable commands run by this seat: none. No imports, gates, selftests, host probes, installs or subprocesses. Inspection used only read/grep/glob; the sole write is this report. No prior work was rerun to decorate evidence.

The following are preregistered L1 measurement commands, quoted as data, NOT executed by this seat; all R20 before/after outcomes remain **PENDING / NOT OBSERVED**, not PASS:

| Claim | Intended metric | Command (unrun here) |
|---|---|---|
| C1 | ownership_corrections 0→1 | `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections` |
| C2 | object_selector_tools 0→9 | `python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors` |
| C3 | audit_live_map_errors 1→0 | `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map` |

Source: `.ufo/waves/round-20/preregister.json:3–27,49–65` and `SCORECARD.md:614–627`. The C3 fixed expectations require rejection of legacy live1 and a historical-row-only fix, and allowance of selftest1 without live DEGRADED. Expected outputs are a contract/oracle preregistration, not execution results. No new no-harm/trend verdict, promotion, landed revision, prefix-preservation measurement or safety certificate is issued here.

## Touched surfaces, scope and limits

- Only written artifact: `.ufo/waves/round-20/build/ScribeErrata.md` in the production lane. No product, fleet-report, lesson, SKILL, LOG, registry, judge, Git/index/ref or sibling edits.
- R19 report and outside lesson were read as historical evidence; no correction was applied to either. R20 candidate bytes are a moving worktree observation, not proof of baseline equivalence, commit ancestry or completed integration.
- Out of scope: current host/boot-image state (UNKNOWN), initramfs contents, hook freshness, packages, services, mounts, reboot/recovery, credentials/private configuration, routing, execution authorization and independent R20 closure. No boot image was inspected or dumped; no runtime invoked or delegated.
- Retained finding: the false operative-map repair claim and inaccurate SKILL append-only claim require named additive disclosure; numerical coverage admission does not resolve either. Draft above is ready for the sole integration writer to incorporate without rewriting R19.
- Tool installs/updates: none.

Scope: executed=none
