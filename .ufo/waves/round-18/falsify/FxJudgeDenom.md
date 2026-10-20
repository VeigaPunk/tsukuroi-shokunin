# FxJudgeDenom — read-only scoped review

## Findings

- **SURVIVES — fixed original-nine denominator, including absences.** `tools/check-revision-binding.py:61-80` defines five legacy plus four round-17 tools, then fixes `TOTAL = len(TOOLS)` (9). Missing named tools remain in `per_tool` as `bound: false, consistent: false` (`:214-229,444-448`); the absent-tool fixture expects 8/9 and FAIL (`:692-698`). These are source and fixture expectations, not executed results.
- **SURVIVES — additional discovery is separate and honestly bounded.** `:200-211` inspects only immediate `tools/` entries, excludes underscore-prefixed names, fixed names and the judge, and matches the exact bytes `b'"--revision"'`. There is no recursive/hidden-Python completeness claim. `:455-476` grades only `named`, while preserving extras in `discovered`, `additional_*`, `all_*` and `per_tool`. The selftest expects an inconsistent discovered `check-extra.py` to leave named 9/9 PASS while all tools total 10 (`:723-755`); not run here.
- **UNPROVEN — actual C2 baseline/target counts.** No execution was authorized; the final execution ledger is pending per assignment. The checker documents exit 0 as original-nine consistency only; `SKILL.md:1970` separately requires `shared_tools=9` and zero copies for consolidation, so status alone is not the full C2 criterion.

## Verification gaps

`xd://lsp` is unavailable (“No such tool”); source reads used as fallback. No tests or commands were run. No tool installed.

Scope: executed=none