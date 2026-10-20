# ReviewRevision: immutable `--revision` handling

Static only; nothing executed; no installs. Baseline `db68e62` equals HEAD (verified as a commit).

**Implementation missing:** `tools/check-section-citations.py` and `corpus/knowledge/section-citation-errata-r16.{json,md}` are absent. Findings come from the sibling gates the executor will copy.

1. `REV` accepts `HEAD`, which moves after the green commit. Require full 40/64-hex and record full hashes.
2. No-argument mode reads the live worktree, a moving-tree measurement. Require `--revision` for any verdict.
3. check-locator:672 and source-scope:528 label invalid input `revision:"worktree"`. Use a distinct invalid label.
4. `resolve()` maps every nonzero exit to invalid. Verified: unknown revision rc 1; not-a-repository rc 128. Only rc 1 should be invalid.
5. Verified: `git show <rev>:corpus/knowledge` returns rc 0 (tree listing). Check object type, read with `git cat-file blob`, add `--no-replace-objects`.
6. Locator selftest `invalid-revision` tests helper `revision_finding()`, not `main`, `resolve`, or git: tautological.
7. root-dac-correction lacks the SystemExit guard: usage to stderr, no JSON.
8. Absent file at a valid revision: FAIL in locator, CANNOT in root-dac. Decide; baseline must be red through FAIL.

Limits: git 2.55.0 behavior verified statically. Textconv behavior of `git show` is unverified [INFERENCE].
