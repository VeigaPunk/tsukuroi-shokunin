# S176 draft — man-pages 6.19 environ(7) (round 32, wave 1, seat ScribeSrcEnviron7)

## Row (registry shape, `corpus/SOURCES.md`)

| S176 | man-pages 6.19 — environ(7) — https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man7/environ.7?h=man-pages-6.19 | docs | A | How man-pages 6.19 describes the environment supplied to a newly started program by execve(2), copied to a child created by fork(2), and common conventions for PATH, HOME, LANG/LC_*, TZ, TMPDIR, USER, LOGNAME, TERM and SHELL; generic documentation, not proof of how a particular tool constructs or filters its child environment | tag man-pages-6.19; man/man7/environ.7 lines 18-23 (execve environment and fork-child copy), 92-95 (incomplete common-variable list), 97-130 (USER, LOGNAME, HOME, LANG and LC_*), 132-155 (PATH), 177-182 (SHELL and TERM), 224-229 (TMPDIR), 256-263 (TZ); raw bytes sha256 bdb7c597babe0c9bcae31c87d4a29e94a789b5a40c9ddd054bc77e6a778b82ce; snapshot .ufo/waves/round-32/w1/ScribeSrcEnviron7/environ.7 (386 lines, 8495 bytes); fetched with curl -sL --fail from the kernel.org cgit plain endpoint on 2026-10-22 | execve makes an environment available to a newly started program, and a fork-created child inherits a copy; the manual lists the common variable conventions above, but does not establish any lane tool's filtering behavior | mined | 2026-10-22 | on-release | corpus/lessons/round-32.md |

## Gate

- Gate: https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man7/environ.7?h=man-pages-6.19 — accessed 2026-10-22 by plain `curl -sL --fail`; `.ufo/waves/round-32/w1/ScribeSrcEnviron7/environ.7` (386 lines, 8495 bytes), sha256 `bdb7c597babe0c9bcae31c87d4a29e94a789b5a40c9ddd054bc77e6a778b82ce`; raw source lines 18-20: “This array of strings is made available to the process by the .BR execve (2) call when a new program is started.” (22 words); lines 21-23 separately say that a fork-created child inherits a copy.

Date note: the task requested opened 2026-10-23, but the supplied session date is 2026-10-22; this draft records the actual source-open date, 2026-10-22, rather than a future date.
