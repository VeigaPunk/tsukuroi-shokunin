# ReviewQuotes — round-16 quote matching

Baseline db68e62, clean tree. Static reads only; nothing executed; no installs.

## Findings

1. **Implementation missing.** `corpus/knowledge/section-citation-errata-r16.json`, `tools/check-section-citations.py`, the S050 row and R16 notices are absent from the tree and `git log --all`. Quote matching is unverified.
2. **Lesson paraphrases are not bytes.** Files read `§1 verdict-board row 5` (`host-health-report-r3.md:581`) and `§7 rank 1 row` (`update-safety-v3.md:398`), not `row5`/`rank1`. Match file bytes.
3. **False positive.** `update-safety-v2.md:372` `§7 rank 1 row` is correct (v2 §7 heading at :244). Scope detection to v3:398.
4. **Whitespace policy.** Sibling `norm()`/`plain()` collapse whitespace, strip backticks and fold curly quotes, contradicting "exact". Use byte-exact single-line substring; target lines have no trailing whitespace. Wrapped notice prose (`host-health-report-r3.md:581-582`) needs an explicit notice-only rule.
5. **Uniqueness.** `section()` returns the first heading match. Baseline headings occur once. `| 1 | Do nothing now |` also appears at `update-safety-v2.md:253`, so search only inside the target section.
6. **Exit code.** Missing errata at baseline must exit 1 with a finding, not 2, or the required red baseline is ambiguous.

## Limits

Source-row bytes verified by static reads only; no gate output observed.
