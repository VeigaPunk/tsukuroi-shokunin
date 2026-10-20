# FxSrc062 — S062 git-check-ref-format reopened (literal rules only)

Verdict: SURVIVES — SOURCES row and lesson agree with the manual; no precise contradiction.

## Observed

Reopened https://git-scm.com/docs/git-check-ref-format and the pinned `/2.52.0` render via `read`; texts identical. Footer: "git-check-ref-format last updated in 2.52.0"; selector: "2.53.0 → 2.56.0 no changes". DESCRIPTION rules verbatim: rule3 "They cannot have two consecutive dots `..` anywhere."; rule4 "… space, tilde `~`, caret `^`, or colon `:` anywhere."; rule6 "They cannot begin or end with a slash `/` or contain multiple consecutive slashes …". `--branch` paragraph: "a dash may appear at the beginning of a ref component, but it is explicitly forbidden at the beginning of a branch name"; "When run with the `--branch` option in a repository, the input is first expanded for the “previous checkout syntax” `@{-n}`."

`corpus/SOURCES.md:68`: teaches (dots/spaces/trailing slash) matches rules 3/4/6; anchor "rules3,4,6 and --branch paragraph" matches; "last updated2.52.0, accessed2026-10-20" matches the footer and today. Scope's distinction is exactly the manual's "may be stricter than … refs/heads/$name" sentence plus `@{-n}` expansion. Implementation matches the consequence: `tools/_revision.py:15,88` and `tools/check-revision-binding.py:149-150,555` pass `refs/heads/<branch>`; none use `--branch`; leading dash is banned separately by regex `[A-Za-z0-9_][A-Za-z0-9._/-]*` (first character only), matching the manual's name-leading rule.

`corpus/lessons/round-18.md:22`: rule3 quote verbatim modulo backtick markup, 8 whitespace tokens (≤25); rule6 clause is an accurate paraphrase; access date 2026-10-20 equals today.

## Gaps (not contradictions)

- `--refspec-pattern` example `foo/bar*baz/` accepts a trailing slash in pattern mode; a pattern is not a reference name, and the gate never uses this mode.
- `--branch` expansion is repository-scoped and may yield a commit object name (detached HEAD); the row omits both, so its literal-ref design is conservative.
- Lesson rule6 paraphrase omits "multiple consecutive slashes"; the lesson quote does not evidence rule4/spaces.
- Access date is seat-recorded; the page carries no access timestamp.

## Unknowns

- Moving "latest" URL, no byte digest; pinned render checked textually only.
- Shorthand expansion not exercised (correctly out of scope).

Scope: executed=ls corpus/knowledge (read-only listing, exit0); all else read/grep plus source URL fetches; no git, python, package, service, or host action.
