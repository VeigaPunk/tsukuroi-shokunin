# AttackLooseQuote — round 16

Status: pre-implementation. `tools/check-section-citations.py` and `corpus/knowledge/section-citation-errata-r16.json` do not exist yet; no output observed or claimed.

Counterexamples (static, `git show db68e62:`):
- Python `"" in row` is True: an empty or whitespace quote passes any resolved row.
- `Do nothing now` or `update-safety` sits inside the row_key, so it proves nothing.
- `` `-Syu` would be INERT `` is in the v3 row (:216), the v3 R15 notice (:398), and v2 §7 rank 1 (:253). A file-scoped match passes even after deleting row :216.
- `—` matches 81 v3 lines.

Impacted axes: correctness and provenance. Fake evidence turns the gate green.

Smallest correction: reject a quote that is empty, has edge whitespace, contains a newline, or is a substring of row_key. Do a case-sensitive raw match on the one resolved row line only, and require exactly one match within the heading section. Use discriminating quotes: board `` `-Syu` now `INERT` `` (unique, line 31); rank `INERT: 0 candidates by three probes` (unique in v3, absent from v2). Selftest: add fixtures for empty, row_key-substring, wrong-case, and notice-only/row-deleted quotes. Each must fail with a fixed finding id.
