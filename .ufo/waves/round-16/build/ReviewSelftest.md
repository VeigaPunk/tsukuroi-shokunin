# ReviewSelftest (round-16, static)

**Status:** no selftest exists to review. Absent at `db68e62` and in the worktree: `tools/check-section-citations.py`, `corpus/knowledge/section-citation-errata-r16.json`, `.ufo/waves/round-16/build/frozen-cases.json`. Nothing observed passing. Tools installed/updated: none.

**Concerns for CitationGate** (precedent: `tools/check-locator-clarification.py`, selftest lines 555-651):

1. **Exit ambiguity:** an uncaught exception inside `selftest()` exits 1, identical to FAIL. Wrap each case; internal errors must return 2.
2. **Wrong surface:** `invalid-revision` and `invalid-cli` test helper predicates, not `main()`. Drive `main([...])` and assert exit 2.
3. **Coverage gap:** the R15 selftest never triggers `R15-*-PIN/FIELD/SOURCE`, `CORRECTION-ID/COUNT` or `MD-OPENERS`, the family repaired in `942fa0a`. Assert every emitted id literally.
4. **Tautology:** fixture digests call production `digest()`, not literal pins. Each `.replace()` mutation needs `assert mutated != original`.
5. **Do not copy:** root-dac's `want - got` ignores extra ids; its `kinds.get(i,'PIN')` fallback masks specific ids.
6. **Hermeticity:** selftest must not call git; inject the reader so missing-file cases simulate absence.
7. **Controls:** each restored-notice case needs a notice-removed twin differing only in that notice.

**Limits:** R15 evidence is recorded output (`942fa0a:.ufo/waves/round-15/build/verification.json`), not re-run.
