# Separability re-attack

**Verdict: FAILS as strict input-file independence; SURVIVES for content registries/targets; actual count independence UNPROVEN.**

- [obs] The current worktree drafts have disjoint content sets: C1’s four `R18-CORR` records all target `boot-chain-r17.md` (`corpus/knowledge/statement-corrections-r18.json:6-43`); C3 has 49 `R18-FRESH` records across eight other targets (`corpus/knowledge/freshness-recheck-r18.json:1-496`; path inventory query). This matches the narrower Scorecard wording (`SCORECARD.md:537-541`). Both registry files are untracked and absent at baseline `842a531…` and prerequisite `51dd9ee…`; `tools/check-appended-notices.py` is absent at the prerequisite, so no immutable count/gate result exists yet.
- [obs] Inputs still intersect: C1 CORR-01 cites `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:59` (`statement-corrections-r18.json:11-12`); C3 Health-06 cites that same capture line (`freshness-recheck-r18.json:121-122`). The quote portions differ, but evidence-file independence is false.
- [obs] Both claims use the planned generic gate, which accepts `--revision`/`--registry` and imports `_revision` (`spec.json:55`); `_revision.py` is the shared implementation (`tools/_revision.py:7-9,130-150`), which C2 measures. Thus C1/C3 depend on C2’s shared module for revision binding, though not on each other’s target records.
- [inf] If the planned gate lands as `tools/check-appended-notices.py`, the independent judge will discover it because it scans other `tools/*.py` files containing `--revision` (`tools/check-revision-binding.py:186-197`). It aggregates named plus discovered tools in top-level counts (`:375-408`); original-nine figures must be derived from `per_tool`, not misreported as aggregate 9/9. No gate execution was authorized/performed.

[unk] No LSP device is mounted (`xd://lsp` unavailable); source reads and literal lookup only. R18 count outcomes remain unverified.

Scope: executed=git rev-parse, git status, git diff, git show, git ls-files, git cat-file