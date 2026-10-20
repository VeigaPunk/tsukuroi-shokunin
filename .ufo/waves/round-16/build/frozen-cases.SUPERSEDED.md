# frozen-cases.json — superseded marker (round 17, L1 TsukuroiR17, 2026-10-20)

`frozen-cases.json` (same directory) was an advisory pre-implementation case list for
`tools/check-section-citations.py`. It is **superseded** by the shipped gate's own
in-source `--selftest` (43 cases, `verification-fixed.json`: PASS 43/43, evaluator
sha256 `e7afd26d…eff1bfa`). It is kept byte-unchanged as historical wave evidence and is
not a normative specification. Routed by `corpus/lessons/round-16-verifier-spotcheck.md`
§5 item 4.

Known contradictions with the shipped gate (read the gate, not this JSON):

1. `.count_semantics` says shared findings including `opener/heading/md-scope` block both
   records (count 0), but its own case `cases[id=errata-md-missing]` expects
   `expected_corrections: 2`, and the shipped gate preserves record counts when only the
   MD file is missing. The case vector, not the prose, matches the gate.
2. `.gate.revision_input` and any "worktree" wording are non-normative: the shipped CLI is
   `--revision <rev>` or `--selftest` only; the string `worktree` appears in the gate solely
   as the revision label emitted on CLI errors before a revision resolves
   (`tools/check-section-citations.py:750,753`). There is no worktree evaluation mode.

Round 17 additionally changes the gate's revision admission (hex only, landed on
`master`; `HEAD` rejected) — see `corpus/lessons/round-17.md`; nothing in
`frozen-cases.json` describes that contract.
