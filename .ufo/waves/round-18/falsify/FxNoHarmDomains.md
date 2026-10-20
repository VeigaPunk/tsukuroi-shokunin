# FxNoHarmDomains

## Findings by severity
- **None observed** in the reviewed no-harm domains; no concrete regression found.

## Verdicts
- **SURVIVES (bounded).** Pre-migration baseline run at `51dd9ee` recorded freshness `record_count=48`, `resolved_records=48`, PASS, exit 0, and boot-chain `entry_count=6`, `verdicted_kernel_entries=5`, PASS, exit 0 (`.ufo/waves/round-18/build/RerunLegacy.outputs.txt:10-40`). The same report records baseline/prerequisite input diff exit 0 for these checkers, knowledge files, and R17 captures (`:5-8`). Current R17 registry has 48 records (`corpus/knowledge/freshness-recheck-r17.json`, `.records | length` = 48); current freshness source counts actual records (`tools/check-freshness-r17.py:141,298-305,314-315`). Boot retains default branch `master` and its normal evaluator/count path; correction mode is opt-in (`tools/check-boot-chain.py:804-823,551-585,1559-1573`).
- **SURVIVES (binding boundaries).** Shared binding returns the resolved SHA for the same requested branch and only changes refusal precedence on malformed inputs (`tools/_revision.py:11-24,134-154`). The judge keeps the original five-gate legacy set, adds four R17 gates, and grades nine originals separately from discovered tools (`tools/check-revision-binding.py:61-80,455-475,765`); its static census is bounded evidence, not universal runtime proof.
- **UNPROVEN.** Migration-seat reports describe retained domain fixtures and report post-change selftests (Boot 62→73; Fresh 53→57; Recheck 43→80; Root-DAC 13 domain fixtures untouched/23→54; Section 61→68; Seat 52; Locator 37; Update 20). Source-scope says its 15 domain cases were unchanged, but tests/judge were not run and counts are inferred (`.ufo/waves/round-18/build/MigSourceScope.md:5-6`). No target-tip execution was authorized; `RerunLegacy` is pre-migration, and the final ledger is pending. LSP was unavailable (`read xd://lsp`: “No such tool”), so caller/definition/diagnostic checks were not possible; source/diff review is not semantic LSP proof.
- **FAILS:** none observed; this is not proof of absence outside this scope.

Scope: executed=none