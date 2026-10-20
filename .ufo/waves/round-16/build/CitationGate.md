# CitationGate — tools/check-section-citations.py

Delivered complete gate (780 lines, r15-checker conventions). `--revision`/`--selftest` mutually exclusive, required; revision regex blocks option injection; `record.path` compared to pins, never dereferenced (reads only the two pinned target paths). Exit 0/1/2; CANNOT on parse/git/CLI errors.

Mechanics: schema `tsukuroi-section-citation-errata-v1`, top-level exactly {schema, corrections}, two records, eight fields each pinned to contract values. Fence-aware exact heading resolution → unique row_key row → quote substring. Wrong-locator literals `§1 verdict-board row 5`/`§7 rank 1` tolerated only inside R15-UPDATE-STATE section or resolving R16 notice; baseline prefix compared against `git show db68e62…` bytes. Notices require pinned heading + old_locator, "supersed… citation only", R15-UPDATE-STATE + partial-upgrade-recheck-r15 routing + exact safety sentence. MD openers/headings/scope; S050→SOURCES row linkage.

Selftest: 37 fixed cases mirroring frozen-cases.json (38 of 40; `worktree-clean` dropped — no worktree mode per L1; its count prose conflicts resolved toward case vectors). Scope is citation resolution only, no health/update-safety verdict.

Limits: never executed; L1 runs it post-integration.


R16-SOURCE-ROW is implemented and non-optional: emitted when SOURCES.md is absent or no `| S050 |` row names both target files. Shared blocker (count 0); expected in `baseline` and `source-row-missing` cases.