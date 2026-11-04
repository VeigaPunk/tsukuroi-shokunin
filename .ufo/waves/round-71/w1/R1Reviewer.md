# R1Reviewer receipt

Scope: frozen round-71 C1, SC1Entry draft plus SC2Sources draft bindings, not an integrated commit.
Findings: P2 MP6 missing built-in cmdline constraint; P2 MP3 missing get -errno alternative and optional set/get; P2 MP2 explanation incorrectly equates nonzero perm with store installation.
Evidence and full source spans: R1Reviewer/review.md. Row diff: R1Reviewer/verdicts.tsv. Raw output and pins: R1Reviewer/evidence.json. Reproducer sources: R1Reviewer/checker.py and R1Reviewer/fixture-builder.py.
Base and draft pass both checkers; sixteen mutants fail both; row agreement 105/105; return-code agreement 18/18. No claim of universal lexical equivalence or integrated-revision verification.
No tools installed; LSP device unavailable. No lane edits, commits, host writes or service operations. Scratch cleaned before yield.
ROWS=6 AGREE=105/105 DEFECTS=3 INDEPENDENT_RC=0
