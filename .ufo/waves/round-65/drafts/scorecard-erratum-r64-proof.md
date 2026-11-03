## Round 65 — routed repair (R64-SPOTCHECK-C1-PROOF): the round-64 C1 identity proof re-expressed

Append-only repair; supersedes only the WORDING of the round-64 C1 identity proof named below —
the normalization fact stands as measured (stray-CR 0/0/0 on the `431f0c9` blobs; additive-only
delta; removed=0).

The r64 closure (`.ufo/reports/round-64/`, corpus/lessons/round-64-verifier-spotcheck.md §5)
ruled: the C1 identity proof as worded — `git show 2f3061ef:F | tr -d '\r' | cmp - F` rc 0 ×3 —
"is only true against the fix-time worktree; re-run against the cited measured revision `431f0c9`
it is false for SOURCES/SKILL because the same commit carries the round's additive work." The
original wording compared the stripped declaration-commit blobs against the *uncommitted worktree*
at fix time; at the cited revision the same comparison correctly fails, because `431f0c9` carries
the round's additive work on top of the normalization.

Re-expressed proof (the form the closure asked for — "stripped-base vs blob diff is additions
only", re-runnable green at the cited revision from committed bytes alone):

```
for F in corpus/SOURCES.md SKILL.md SCORECARD.md; do
  diff <(git show 2f3061ef:"$F" | tr -d '\r') <(git show 431f0c9:"$F")
done
# SOURCES.md: added=3 removed=0   (S279-S281, the round's three registry rows)
# SKILL.md:   added=120 removed=1 (the round's SKILL appends; the -1 is the disclosed EOF
#                                  newline artifact the r64 closure already named)
# SCORECARD.md: added=0 removed=0 (byte-identical at the measured revision)
```

Measured 2026-11-03, receipt `.ufo/waves/round-65/after/reidentity-at-431f0c9.txt` (added/removed
per file exactly as stated). The C1 EOL-repair claim of round 64 stands on this form: the three
files differ from the CR-stripped base by ADDITIONS ONLY — zero content was rewritten by the
normalization. The original `cmp -` wording remains true only against the fix-time worktree and
is superseded by this diff form for every future re-run.
