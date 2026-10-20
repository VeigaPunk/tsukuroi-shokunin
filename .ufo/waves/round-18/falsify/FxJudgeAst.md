# FxJudgeAst — read-only review

## Finding — Medium: consolidation PASS omits two required fields
`tools/check-revision-binding.py:463-467` sets `status` from `consistent == TOTAL` alone; `:479-480` likewise grades exit status without `shared_tools` or `local_rev_regex_copies`. Yet its contract at `:44-45` says consolidation additionally requires `shared_tools == 9` and zero local copies. The selftest is a concrete counterexample: `:647-668` expects PASS for all-bound fixtures, while `:703-704` expects their shared census to be `(0, 0)`. Thus the reported PASS/exit can certify behaviorally consistent copied implementations as consolidated. The consolidation grade must require all three conditions (or keep a clearly separate consistency-only status that cannot imply consolidation).

## Survives / residual risk
The AST census at `:232-262` requires an imported `_revision.bind` and a bind call, and omits literal-false `if` branches. Selftests at `:735-748` cover dead-import and string-only cases; the mutation receipt `falsify/FxMutJudge.HTur9a/observations.json:140-158` records the dead-import mutant failing. This is deliberately bounded structural evidence, not semantic reachability: calls in unused functions or nonliteral guards may still count. The finite runtime probes at `:367-417` are not universal equivalence proof, as documented at `:35-38`.

## Verification gaps
No `lsp` device/server was available (`xd://lsp` returned “No such tool”); I used direct source reads, with literal search only for locating references—not as semantic proof. No execution or tests were run, per assignment. No tool was installed.

Scope: executed=none