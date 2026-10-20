# RevJjHelper — jj-lane.sh (R17)

## Q1 — refs after commit

[obs] `commit` returns 0 only after `do_push` (jj-lane.sh:660) → `jj git push`
(:341) → `report_landed`, which requires the `git ls-remote` tip to equal
`git rev-parse refs/heads/$b` (:227-234) and prints `landed <remote_tip>`
(:249). Both refs carry the printed hash; live: `refs/heads/master`
= `refs/remotes/origin/master` = 6923fe0.

[obs+inf] HEAD: the helper never writes HEAD (no checkout/switch/symbolic-ref
write; :117/:166 read it). Documented "git HEAD is detached after the
first helper commit" (lane-addendum.md:136-138; closure-prompt.md:23), detached
at `@`, the empty child of the tip (`hash=@-` :597; `@-`==tip required
:575-583). Live attached HEAD==tip only because the last HEAD move was a
plain-git rebase (git reflog HEAD 10:18:50), not the helper.

## Q2 — revision binding

[obs] Landed commit passes both ancestor tests: measured
`merge-base --is-ancestor 6923fe0 refs/heads/master` and `... refs/remotes/
origin/master` exit 0. Rejections: rewritten-away 534d442 → exit 1
(NOT-LANDED); literal `@`/`HEAD` non-hex → INVALID; exit-3 tip (bookmark set
:649-650, push :660) is ancestor of heads only → NOT-PUSHED.

## Findings

- **Med** — no binding here: `.jj` (12:29 today) lacks
  `repo/config.toml`; `lane.branch`/`lane.id` unset [obs] → `state` exits 1 (:159);
  `commit` exits 1 [inf] (:504-506, :510-512). Only `init` repairs.
- **Low** — `report_landed` never re-verifies `refs/remotes/origin/$b`; a stale
  tracking ref is an ancestor → no false NOT-PUSHED [inf].

[unk] @-is-child inferred; jj never executed (no grant).

Scope: executed=git log, git status, git symbolic-ref, git rev-parse, git merge-base --is-ancestor, git reflog, git config --list, git cat-file, grep, sed, cat, ls, find, strings, wc
