# ReviewIndependence

Axes: independent grader; fixed-ID fixture coverage.

## Verdict: FAILS (narrow)

- **Independent binding SURVIVES.** [obs] `tools/check-revision-binding.py:53-54,79-86,92-157` imports only standard-library modules and defines its own `Cannot`, IDs, revision regex, Git helpers, and `bind`; it does not import `_revision`. `measure` uses that local `bind` for the selected revision (`:375-378`). Expected IDs are local literals (`:80-86`), and the branch/Git probes compare against them (`:349-364`).
- **Single-id enforcement FAILS.** [obs] The contract says each refusal is exactly one finding ID (`tools/_revision.py:11-24`). The judge's `binding_ids()` filters JSON findings to recognized binding IDs only (`tools/check-revision-binding.py:261-267`); `finding_id()` accepts the first ID (`:270-277`); and `single-id` passes when the filtered list is `[E-REVISION-NOT-LANDED]` (`:356-359`). [inf] A refusal containing that expected finding plus an unrelated finding ID therefore passes `single-id`, despite having two IDs. The selftest's `double` stub only emits two recognized binding IDs (`:515-516`) and asserts that case fails (`:643-650`); it does not falsify the unrelated-ID case. This can overcount `consistent_tools` for a tool violating the one-ID contract.

## Residual risk / verification gaps

LSP is unavailable: `xd://lsp` returned “No such tool”; no semantic references/definition/diagnostics were available. No target code or tests were run. [obs] Read-only diffs were inspected against baseline `842a5312b704b5cda10fd80ec1fdee5fb381ba97` and prerequisite `51dd9eeaa305539fa3cfc6ee275978dc18043b79`.

Scope: executed=read-only `git diff --no-ext-diff --unified=3 842a5312b704b5cda10fd80ec1fdee5fb381ba97 -- tools/check-revision-binding.py tools/_revision.py`; read-only `git diff --no-ext-diff --unified=2 51dd9eeaa305539fa3cfc6ee275978dc18043b79 -- tools/check-revision-binding.py tools/_revision.py`.