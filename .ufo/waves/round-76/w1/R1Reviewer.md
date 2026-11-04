# R1Reviewer — scoped truth review

Verdict recommendation: JD3 FAIL; JD7 PARTLY; six rows HOLD. No admission or integration performed.
Unchecked: live min_use; installed-binary equivalence; journalctl allocation implementation; historical rotation/window and timestamp/causal provenance not captured in frozen host receipt.
Axes: depth, C1, attack.

## Findings by severity

1. **High: incorrect JD3 arithmetic.** Actual note corpus/knowledge/journald-retention-plane-r76.md:18,39–40,81 interprets LESS_BY as min(free,keep_free). Pinned journald-manager.c:168 subtracts the reserve with floor zero; :170 clamps used+avail. Correct host avail=759944802304 bytes, not 4GiB. Correct sentence and complete evidence in binding report.
2. **Medium: JD7 wrong function attribution.** Note:22 attributes all four defaults to journal_config_set_defaults. Pinned journald-config.c:51–52 initializes only rate pair; manager_merge_configs applies sync at :133 and max-file at :142. Values at :24–27 hold.
3. **Medium: host effective_limit claim is conditional.** Receipt gives configured MaxUse=256MiB, but not live min_use, which manager:185 raises and :170 uses in clamp. 256MiB follows for min_use<=256MiB; 32MiB is the derived default file size. Do not describe either as measured internal values or hard post-vacuum total bounds.
4. **Medium: broad stale-carrier closure exceeds size derivation.** journal-boot-plane.md:362 explicitly includes 'rotation date of boot −12'; boot-plane.md:240 asks about retention beyond 13 boots. New size arithmetic resolves configuration, not historical rotation dates or guaranteed boot/time retention. Errata should close only the resolved subclaim. degraded-triage-r4.md:70's old measured 3.9G remains historical, not retroactively disproven by 148.6M now; confirm coredump versus journald scope before superseding combined quantities.
5. **Low: unsupported provenance/causality in cited receipt.** Note:75's birth timestamp and :91's causal attribution are not supplied by before/host.txt; either cite additional captured evidence or qualify them. Note:4's independent review must not imply all eight rows passed.

## Deliverables

- .ufo/waves/round-76/w1/R1Reviewer/verdicts.md — source quotes with surrounding ranges, per-row judgments and corrected sentences, host recomputation, exact stale-carrier quotations, residual gaps.
- .ufo/waves/round-76/w1/R1Reviewer/rows.tsv — eight machine-readable row verdicts.

## Exercised checks

Read actual working note and scoped stale-carrier diff; inspected all eight quoted source ranges and surrounding branches; recomputed host integer arithmetic (keep_free=4294967296, avail=759944802304, max_use=268435456, max_file_size=33554432, logical sum=200MiB). Receipt:66–68 directly says journalctl disk usage=148.6M. lsp unavailable ('No such tool'); textual fallback only. No source hash recomputation, counter instrument, live vacuum, build, installation, runtime rerouting, or host mutation. Scratch removed before submission. Main should verify the proposed table/prose/errata corrections together; counters only establish format, not entailment.
