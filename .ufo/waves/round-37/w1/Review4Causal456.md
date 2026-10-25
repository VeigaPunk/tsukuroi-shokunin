# Review4Causal456 — round-37 declaration review

Scope: read-only review of `SCORECARD.md:1857-1968` against `PROTOCOL.md`, `AXES.md`, `CORPUS.md`, `MISSION.md`, and `LEARNING.md`; declaration base `564db0b614b2914de5452f9ebd537a0653ae1de5`. No lane files outside this report were changed. No external source was cited; evidence is local and opened this round.

## Findings

### C1 — operability: sourced evidence pointers do not identify the staged S200/S201 rows

`SCORECARD.md:1899-1900` says the probe note cites “a strace(1) row opened this round (S200-strace) plus the probe's own-work row (S201-probe).” The staged append actually assigns S200 to `mount(2)` and S201 to Btrfs ioctl source code, with both `used-by` values pointing to knowledge notes, not a strace row or the probe (`.ufo/waves/round-37/assimilation/SOURCES.append.md:1-2`). Thus the declaration's cited source identities cannot resolve to the evidence it claims. CORPUS SOURCES rule 1 requires new rows to be opened this round and the lesson to record URL, access date, and a located quote; PROTOCOL evidence standard requires resolvable pointers. Repair the C1 source pointers to the actual rows/quotes or ensure the intended S200/S201 rows are what gets admitted, without reusing those IDs. This is a concrete sourced-evidence defect, not a finding about the probe's runtime behavior.

### C2 — depth: the promised unchanged rejection line is outside the stated counter

`SCORECARD.md:1906-1915` declares that “the rejection line stays verbatim,” but says the checker asserts only the 15-term table, the `-n` distinction, and the action-override row. The counter's stated three-fact predicate therefore does not verify that additional promised invariant. The base note has the rejection line at `corpus/knowledge/journalctl-v262-field-filter-r36.md:13-15`; a later edit could alter it while all three declared assertions still pass. Add an exact-line assertion (or remove the unchanged-line assertion from the claim). This follows AXES' requirement that each non-exploratory claim have a falsifiable, measurable before→after.

### C3 — calibration: no defect found in the corrected claim's declared measurement

The superseded ledger/checker C3 at `SCORECARD.md:1924-1948` is explicitly withdrawn by the pre-freeze correction at `:1950-1972`. The operative C3 is the fixed 27-check self-assessment predicate at `:1958-1968`. The committed before receipt reports 27 checks, 5 mismatches, FAIL (`.ufo/waves/round-37/before/c3-before.json:2-8`); the recorded after receipt reports 27 checks, 0 mismatches, PASS at revision `0e5f70fadba12bc9bbb9db564c2262c2c0194535` (`.ufo/waves/round-37/after-c3-0e5f70.json:2-8`). The checker's bytes/population are declared unchanged, and the base control cannot meet the target. That is an observable calibration correction, consistent with AXES' definition; no concrete C3 defect established from the inspected evidence.

## Residual risk and verification gaps

C1 source-row mismatch and C2 predicate omission are declaration defects; this review did not execute the C1 probe or C2 checker, whose round-37 versions are not present in `tools/` at this inspection. C3 evidence is a stored before/after receipt, not an independent closure rerun. Other declaration clauses (including the complete assimilation census and all C1 mutant sensitivities) were not independently re-executed here.

Trailer: Report: `.ufo/waves/round-37/w1/Review4Causal456.md`