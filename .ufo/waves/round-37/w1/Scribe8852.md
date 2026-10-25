# Round 37 item 8 — scoped evidence draft

**Axes:** C2 depth (correction completeness); C3 calibration (27-check self-assessment); frontier assimilation (errno discrimination). **Status:** evidence draft only; no lane product changes or outcomes measured by this seat.

## Claim boundaries and evidence status

- **[OBS: declaration text]** `SCORECARD.md` at lines 1906–1919 defines C2 as correcting `corpus/knowledge/journalctl-v262-field-filter-r36.md`: exactly the corrected 15-term predicate table, the `-n` third-state distinction (`-F` truncation versus unchanged `-N` output), and an action-override classification, while preserving the rejection line verbatim. Its declared checker is `tools/check-journalctl-v262-corrections.py`; base exit 1 and change-commit exit 0 are declaration statements, not execution evidence in this seat.
- **[OBS: declaration text]** The pre-freeze correction at `SCORECARD.md:1950–1970` withdraws the proposed new verified-rate ledger/checker because it could not be independently grounded against stable complete history. It replaces that proposal with C3: repair five current self-assessment count cells (K07–K11) so the existing checker reports 0 mismatches among 27 checks at the measured tip; declaration says base had 5 mismatches. These are specified target/baseline claims, not this seat's observed run.
- **[OBS: declaration text]** Assimilation specifies one theme, errno discrimination, and names three proposed package entries (`errno-name-discrimination-r25.md`, `mount-errno-contract-r26.md`, `errno-contract-variance-r37.md`) plus source rows S204/S205/S214/S220/S279–S282/S286/S287. It also states that a 12-row quarantine slice was hand-checked. I did not inspect the named package files, transformed rows, or row-level verdicts; their correctness/admission remains **[UNKNOWN]** here.
- **[INFERENCE]** The C3 correction reduces evidence surface and calibration risk relative to creating a new ledger: it uses an already-fixed 27-check population and an existing counter. Whether all five count-cell changes are accurate at the tip depends on the declared measurement and was not verified by this seat.

## Acceptance checklist for closure

1. Preserve C2's explicit three correction facts and exact rejection line; cite the actual note and checker receipt before claiming completion.
2. For C3, report the pinned revision, exact checker command, `checked`, `mismatches`, `status`, and exit; do not present declaration text as execution evidence.
3. Keep the withdrawn ledger/checker out of the scored claim; do not convert the proposal or its rationale into a verified outcome.
4. For errno assimilation, inspect each source and each proposed row; preserve source attribution and claim boundaries, distinguish observed source facts from inference/unknown, and substantiate each quarantine verdict. No external source rows are proposed here because no external source was opened this round.

## Scope / provenance

Read this round: mandated `~/.omp/agent/RULES.md`; the round-37 SCORECARD declaration and correction; neighboring `C14SourceChannel04.md`; search results locating earlier round-36 evidence. No source URL was opened, no command was executed, no install/update occurred, and no lane tracked file or Git/jj state was changed. This report is the only authored artifact. It contains no external-source citation because none was opened.
