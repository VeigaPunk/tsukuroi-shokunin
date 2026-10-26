VERDICT: supports

Item C2-EX2. Object judged: row EX2 of `corpus/knowledge/pacman-exec-environment-r40.md` at
f951f288483c1af0cef4afd458488b84cf7a2165 (row at file line 22; lane tip confirmed `git -C
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD` → `f951f288483c1af0cef4afd458488b84cf7a2165`,
2026-10-26 07:16:03 UTC). All blobs re-fetched independently; every clause checked against the pinned source.
Row verdict: **holds**. No correction text proposed (required only below `holds`).

## 1. Sources re-opened (independent fetch, sha256 vs frozen manifest)

Fetched 2026-10-26T07:17:32–35Z by C2RevEX2 (receipts: `.ufo/waves/round-40/w1/C2RevEX2/fetch-log.txt`),
compared against `.ufo/waves/round-40/frozen/src/SHA256SUMS` — **all six MATCH**:

| file | URL (raw, commit/tag) | sha256 (first 8…last 4) | result |
|---|---|---|---|
| util.c | gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/util.c | 381618b6…bdd2 | MATCH |
| hook.c | …/-/raw/54d9411/lib/libalpm/hook.c | 99f1044b…199a | MATCH |
| trans.c | …/-/raw/54d9411/lib/libalpm/trans.c | 637c1165…ed07 | MATCH |
| alpm-hooks.5.asciidoc | …/-/raw/54d9411/doc/alpm-hooks.5.asciidoc | 2970cb35…93d3 | MATCH |
| meson_options.txt | …/-/raw/54d9411/meson_options.txt | 89e5b350…5a65b | MATCH |
| PKGBUILD | gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/raw/7.1.0.r9.g54d9411-3/PKGBUILD | 32d40dfd…67f4 | MATCH |

EX2 cites S221 = util.c, so all clause evidence below is util.c at 54d9411 (sha256
381618b6054859ec76807956328b78b330237273bebe10022a559b243cb5bdd2, equal to the pinned copy).

## 2. Clause-by-clause verdict — row EX2 (`corpus-r40.md` blob line 22)

Pinned blob copy for citation: `git -C <lane> show f951f288483c1af0cef4afd458488b84cf7a2165:corpus/knowledge/pacman-exec-environment-r40.md`.
util.c lines cited from the byte-identical re-fetch.

| # | rule clause | verdict | source evidence (util.c:54d9411) |
|---|---|---|---|
| 1 | "The child's stdout and stderr are both duplicated onto one socket" | holds | One channel: `if(socketpair(AF_UNIX, SOCK_STREAM, 0, child2parent_pipefd) == -1) {` :640; child dups both fds onto its HEAD end: `while(dup2(child2parent_pipefd[HEAD], 1) == -1 && errno == EINTR);` :665, `while(dup2(child2parent_pipefd[HEAD], 2) == -1 && errno == EINTR);` :666 |
| 2 | "…that the parent reads" | holds | Parent polls the peer end: `child2parent->fd = child2parent_pipefd[TAIL];` :712, `child2parent->events = POLLIN;` :713; reads it: `_alpm_chroot_read_from_child(handle, child2parent->fd, …)` :740 |
| 3 | "so the two streams arrive merged" | holds | fd 1 and fd 2 are dups of one descriptor target (:665-666), so output is one byte stream; the parent consumes it as one stream and logs it line by line into the ALPM-SCRIPTLET logger (`alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);` :527). The r39 entry states the same from these lines: `pacman-transaction-order-r39.md` blob :78-79 "The child's stdout **and** stderr are both joined to the pipe whose lines become `[ALPM-SCRIPTLET]` (util.c:665-666)" |
| 4 | "its stdin is a second socket" | holds | Second channel: `if(socketpair(AF_UNIX, SOCK_STREAM, 0, parent2child_pipefd) == -1) {` :646; child's fd 0 is its TAIL end: `while(dup2(parent2child_pipefd[TAIL], 0) == -1 && errno == EINTR);` :667. Socket (not pipe) corroborated on the parent side by `nwrite = send(fd, buf, *buf_size, MSG_NOSIGNAL);` :504 and by the code's own comment :688 "bash assumes it's being run under rsh/ssh if stdin is a socket and" |
| 5 | "which the parent closes at once when the caller passes a null input callback" | holds | Parent branch immediately after fork, before the poll loop: `if(stdin_cb) {` :718 arms POLLOUT :719-721; `} else {` :722 `parent2child->fd = -1;` :723, `parent2child->events = 0;` :724, `close(parent2child_pipefd[HEAD]);` :725, `}` :726 — the one-shot close is :725. With a callback the end is kept and fed by `_alpm_chroot_write_to_child` :490-518 (callback-exhausted → pipe closed :497-500) |
| 6 | "so such a child reads end-of-file on stdin" | holds | After :668-669 (child closes both its copies) and parent closes :716 (`close(parent2child_pipefd[TAIL]);`) and :725 (write end), no descriptor references the stdin socket, so `read(0)` returns 0 — the EOF branch `} else if(nread == 0) {` :557 of `_alpm_chroot_read_from_child` :531 |

No clause states or implies more than these lines support (QUALITY 66 check, `corpus/lessons/round-26.md:128`:
statement compared with the quoted source lines): verdict **holds**.

## 3. Quote and citation-range check

- Quote cell: `while(dup2(child2parent_pipefd[HEAD], 2) == -1 && errno == EINTR);` cited at util.c:659-668.
  `grep -Fn 'while(dup2(child2parent_pipefd[HEAD], 2) == -1 && errno == EINTR);'` on the byte-identical re-fetch
  → exactly one hit, line 666 (verbatim, receipt `quote-check.txt`); :666 lies inside the cited :659-668 (child
  fd setup :660-671). **Verbatim.**
- Parenthetical "(stdin end closed in the parent at :722-726)": the else branch is exactly :722-726 with the
  close at :725. Accurate. (My dispatch brief said :714-726 — that wider range also subsumes :725; the row's
  narrower citation is the precise one. No defect.)

## 4. Value and host cells

- Value cell `stdout+stderr: one socket; stdin: second socket` — matches the structure (:640/:665-666 one
  socketpair; :646/:667 second socketpair). Holds.
- Host cell "The `[ALPM-SCRIPTLET]` lines of TO8 carry both streams of a command interleaved; the log gives a
  reader one merged stream" — grounded in the declared r39 ground TO8 (`pacman-transaction-order-r39.md` blob
  line 31, tag from util.c:521-528) plus the r39 boundary note at :78-79 citing util.c:665-666; it cites TO8
  rather than claiming a new live observation, and the entry's Boundaries section honestly discloses that
  EX1–EX3 and EX5 have no host instance in the capture (pacman transactions paused host-wide). No overstatement.
  Holds.

## 5. Not done / residual risk

- No live pacman transaction was observed (host-wide pacman pause; the entry's own Boundaries section discloses
  this for the host column). The host cell was judged against the frozen r39 ground, not a new capture.
- I did not run `tools/check-exec-environment-r40.py` (the frozen counters are not this seat's item) and did not
  re-open `corpus/SOURCES.md` (the S221↔util.c mapping is taken from the row's own citation plus the matching
  filename/digest in SHA256SUMS).
- Nuance, not a defect: "one socket" strictly means one `socketpair()` channel (:640) — the parent reads the
  peer endpoint, the child dups the other. The row's value cell uses "socket" in exactly this channel sense, and
  the source's own error strings call these "pipe" (:641, :647), so no reader is misled.
- Tooling record: nothing installed or upgraded for this seat (preinstalled python3/urllib, git, grep only).
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/C2RevEX2` (corpus blob copy + fetched sources) removed after
  receipts were copied to `.ufo/waves/round-40/w1/C2RevEX2/`; no /tmp path used as evidence; no lane file other
  than this report and the receipts was written.
