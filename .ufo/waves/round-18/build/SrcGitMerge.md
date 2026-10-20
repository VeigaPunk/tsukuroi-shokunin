# SrcGitMerge — `--is-ancestor` exit classes (accessed 2026-10-20)

[obs] Primary source <https://git-scm.com/docs/git-merge-base> (English latest), opened 2026-10-20. Heading **OPERATION MODES → `--is-ancestor`**; fragment `#Documentation/git-merge-base.txt---is-ancestor` (raw HTML line 1700). Version footer: “git-merge-base last updated in 2.43.0”; panel shows 2.43.1–2.56.0 no changes.

[obs] Designated quote, 25 words, lines 1702–1703:
> Check if the first <commit> is an ancestor of the second <commit>, and exit with status 0 if true, or with status 1 if not.

[obs] Next sentence, 13 words, line 1704:
> Errors are signaled by a non-zero status that is not 1.

[inf] Three classes: 0 ancestor, 1 not ancestor, other nonzero error. A gate must not fold rc≥2 into “not ancestor”; map 1 to `E-REVISION-NOT-LANDED`, other nonzero to `E-GIT-FAILED`.

[unk] No numeric error code or failure-cause list here (Git commonly 128/129, unstated). Treat any non-1 nonzero as error.

Candidate SOURCES row (S061 provisional; S060 = round-18 capture, `corpus/SOURCES.md:66`):
| S061 | git-merge-base(1) — https://git-scm.com/docs/git-merge-base | docs | A | `--is-ancestor` distinguishes ancestor, non-ancestor and error statuses | OPERATION MODES > `--is-ancestor`, fragment `#Documentation/git-merge-base.txt---is-ancestor`; v2.43.0, unchanged to 2.56.0; accessed 2026-10-20 | Exit 0 = ancestor, 1 = not, any other non-zero = error; never treat error as “not an ancestor” | queued | 2026-10-20 | on-release | tools/_revision.py (planned C2) |

[pinned] Quote tied to accessed date, not byte digest; URL is moving latest.

Scope: executed=read-only `ls`/`grep`/`wc`; no mutation, gate, test, or host probe.
