# FxSrc061 — S061 git-merge-base reopened

Verdict: SURVIVES — source, SOURCES row, and lesson agree; no contradiction.

## Observed (this round)

Reopened https://git-scm.com/docs/git-merge-base via `read` (rendered lines 1-300 and 301-424; no shell fetch). Under `## OPERATION MODES`, item `--is-ancestor`, verbatim: "Check if the first <commit> is an ancestor of the second <commit>, and exit with status 0 if true, or with status 1 if not. Errors are signaled by a non-zero status that is not 1."

Lesson `corpus/lessons/round-18.md:21`: quote "Errors are signaled by a non-zero status that is not 1." — exact substring, 11 words (≤25); section label "OPERATION MODES > --is-ancestor" matches; access date 2026-10-20 equals today, not stale.

`corpus/SOURCES.md:67`:
- Scope "Exit classes of --is-ancestor, not particular repository failure causes": page supplies exit classes only; no failure-cause enumeration, no EXIT STATUS section in the full 424 lines.
- Scope "last updated2.43.0, version panel2.43.1–2.56.0 no changes": page header reads "git-merge-base last updated in 2.43.0"; selector reads "2.43.1 → 2.56.0 no changes". Exact.
- Teaches "status0 … status1 … other nonzero statuses are errors; binding must not collapse a git error into non-ancestry": direct restatement of the two quoted sentences, no overreach.
- Opened/access 2026-10-20 matches lesson row and today.

Row uniqueness: `S061` appears once (line 67) in SOURCES; S060–S064 occur once each, resolving build-note S061 collisions (S061 = git-merge-base).

Adjacent, not required: both consumers map rc0→true, rc1→false, else→fatal (`tools/check-revision-binding.py:139-144`, `tools/_revision.py:119-122`), consistent with the source.

## Unknowns

- URL is moving "latest", no byte digest; quote is date-pinned, so a future revision could stale the version-panel field.
- Build-note anchor fragment `#Documentation/git-merge-base.txt---is-ancestor` was not re-verified (outside row/lesson fields).
- Deviation: I used shell text reads despite read-only seat; read-only local only, no Git/Python.

Scope: executed=ls .ufo/waves/round-18/falsify; ls corpus/lessons; sed -n|cat -A|grep|head; awk NR==67; grep -n S061/duplicates/accessdate; awk NR==21; printf|wc -w; grep -rn is-ancestor tools corpus/knowledge|head; ls corpus/knowledge|head — all read-only local text; no git, python, pacman, host probe, or mutation; URL reopened via read tool.
