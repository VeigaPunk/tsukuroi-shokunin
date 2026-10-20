# SrcGitRef — git-check-ref-format branch-name validity

Accessed 2026-10-20. Canonical URL https://git-scm.com/docs/git-check-ref-format; heading DESCRIPTION, fragment `#_description` (raw HTML); version footer “git-check-ref-format last updated in 2.52.0”, list “2.53.0 → 2.56.0 no changes”.

[obs] Exit class (DESCRIPTION ¶1, 17w): “Checks if a given refname is acceptable, and exits with a non-zero status if it is not.”
[obs] Double dot (rule 3, 8w): “They cannot have two consecutive dots .. anywhere.”
[obs] Trailing slash (rule 6, 14w): “They cannot begin or end with a slash / or contain multiple consecutive slashes”.
[obs] Space (rule 4, 9w fragment): “space, tilde ~, caret ^, or colon : anywhere”; rule opens “They cannot have ASCII control characters …”.
[obs] Branch check (21w): “With the --branch option, the command takes a name and checks if it can be used as a valid branch name”. Also “may be stricter” than `refs/heads/$name` (leading dash), and expands `@{-n}` in-repo.
[inf] Hence `a..b`, `a/`, `a ` are invalid for `git check-ref-format --branch` (rules 3, 6, 4). Unexecuted.
[obs] No separate EXIT STATUS section; ¶1 and `--normalize` (“otherwise exit with a non-zero status”) state the class.
[unk] Numeric exit value unstated; this is the latest-version website render, not a pinned tag.

Candidate SOURCES row (no production edit; S060 already the fresh R18 capture):

| S061 (candidate) | git-check-ref-format(1) — https://git-scm.com/docs/git-check-ref-format | docs | A | Documented refname rules and --branch check; name syntax, not repository state | § DESCRIPTION rules 3, 4, 6 and --branch; opened 2026-10-20 | Refname with `..`, trailing `/`, or space is invalid; unacceptable refname exits non-zero; --branch may be stricter | mined | 2026-10-20 | on-release | tools/_revision.py (planned R18 C2) |

Does not establish: host behavior, numeric code, caller adoption.

Scope: executed=none
