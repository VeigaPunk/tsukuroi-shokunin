VERDICT: falsifies

# proc_pid_fd live re-open (R49ScoutProcFd)

Opener of record for the C3 `proc_pid_fd(5)` candidate. The live page is byte-identical to the S251 pin, so that row's symlink and `type:[inode]` sentences still hold. It does not state `/proc/self/fd/<n>/<child>` traversal for a directory descriptor. A new admit that said it did would overclaim; the candidate row below is a rejection, not an admit. Receipts: `.ufo/waves/round-49/w1/R49ScoutProcFd/`. Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ScoutProcFd` removed after the copy (`SCRATCH_REMOVED`). No tools installed. `SOURCES.md` not edited.

## 1. Fetch

- URL (the item, and S251 at freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c:corpus/SOURCES.md` line 260): `https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html`
- Redirects: none. `curl -fsSL --max-time 60` recorded `http_code=200`, `num_redirects=0`, `url_effective=` that same URL, `size=11359` (`curl-meta-proc-pid-fd.txt`). Response start: `HTTP/1.1 200 OK`, `Content-Type: text/html`, `Content-Length: 11359`, `Last-Modified: Thu, 08 Oct 2026 17:39:35 GMT` (`headers-proc-pid-fd.txt`).
- Access date: 2026-10-28. `date -u +%F` printed `2026-10-28`; `date -u +%Y-%m-%dT%H:%M:%SZ` printed `2026-10-28T17:27:04Z` (`access-date.txt`, `access-time.txt`). Response `Date: Wed, 28 Oct 2026 17:27:25 GMT`.
- sha256: `3a50ddef6f2f3a4f1139dcef3299a5eadf8fc96514df9fcb329a3bffd47ff27e` (`sha256-live.txt`). Same digest on the freeze blob `55c07cd3:.ufo/waves/round-46/frozen/src/proc_pid_fd.5.html` (`sha256-pin.txt`) and on that revision's `SHA256SUMS` line `3a50ddef…ff27e  proc_pid_fd.5.html`.
- Byte equality: `cmp -s` of the live file against that freeze blob printed `CMP_IDENTICAL` (`cmp.txt`). Both are 11359 bytes (`wc.txt`).
- Upstream did not move. This URL is not a branch and not a tag; the colophon says the HTML was obtained from `man-pages-6.19.tar.gz` on 2026-09-09 (live lines 168-171) and the footer is `Linux man-pages 6.19` dated 2026-02-08 (line 178). The body is byte-identical to the 2026-10-27 pin. `Last-Modified: 2026-10-08` is older than this fetch and the bytes match, so that header is not a content change.
- `proc(5)`, also fetched, reachable: `https://man7.org/linux/man-pages/man5/proc.5.html`, `http_code=200`, `num_redirects=0`, `size=31125`, sha256 `b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97` (`curl-meta-proc5.txt`, `sha256-proc5.txt`). Response `Date: Wed, 28 Oct 2026 17:27:40 GMT`. No lane pin exists for this URL, so there is no `cmp`. Same release: colophon line 270 "This page was obtained from the tarball man-pages-6.19.tar.gz"; footer line 280 `Linux man-pages 6.19` 2026-02-08. The fd body is not in this page. The only fd hit is the referrer link at line 388, `proc_pid_fd(5)`. DESCRIPTION ends at the per-file link list (line 239); it does not describe `/proc/pid/fd`.

## 2. Anchors

Live bytes equal the pin, so these line numbers are the snapshot's. Quotes are tag-stripped wrapped lines joined with one space. Word counts are `anchors.tsv` column 2. Each is at most 25 words.

- Symlink, lines 74-75 (DESCRIPTION, inside the `/proc/pid/fd/` paragraph that starts at line 72): "which the process has open, named by its file descriptor, and which is a symbolic link to the actual file." (20 words). This is the sentence that an fd entry is a symbolic link to the file it refers to.
- Pipe and socket, lines 79-81: "For file descriptors for pipes and sockets, the entries will be symbolic links whose content is the file type with the inode." (22 words).
- readlink format, lines 81-84: "A readlink(2) call on this file returns a string in the format: type:[inode]" (13 words). The token `type:[inode]` is line 84 alone.
- Socket example, lines 86-87: "For example, socket:[2248868] will be a socket and its inode is 2248868." (12 words).
- Only `/proc/self/fd/N` path example, line 120: `$ foobar -i /proc/self/fd/0 -o /proc/self/fd/1 ...`. Both operands are the fd entry itself. Neither has a further path component.
- Dereference, lines 136-137: "Permission to dereference or read (readlink(2)) the symbolic links in this directory" (12 words). That is a ptrace permission on the symlink, not permission to append a child.

Directory-child traversal: not stated. The 268-line live HTML has no `fd/N/`, `/child`, `additional path`, `path component`, `directory descriptor`, `O_DIRECTORY`, or `Not a directory` (Python `str.find` on the fetched bytes returned -1 for each). The word directory occurs only for the fd directory itself: line 73 "This is a subdirectory containing one entry for each file"; line 105 "the contents of this directory"; line 137 "symbolic links in this directory". None says the open file is a directory, and none says `/proc/self/fd/<n>/<child>` looks up inside one.

Pipe and socket: the census must not treat those entries as directories. Lines 79-87 say their symlink text is `type:[inode]`, for example `socket:[2248868]`, not a filesystem path. That is the located reason. Applying it to `tools/tsukuroi-census.sh` is this seat's reading of that sentence, not a sentence on the page.

[inference] If the open file were a directory, following "a symbolic link to the actual file" (lines 74-75) would land on that directory, and a later path component would be ordinary resolution. The page does not say this. Do not put it in `teaches`.

## 3. Cadence and pins

S251's `180d` recheck and sha256 pin still read right: the untagged HTML is the man-pages 6.19 render, and today's bytes match the pin recorded on the freeze row (line 260), including the row's own note that SScoutProcFd re-opened it on 2026-10-28 with the digest unchanged. The anchor "raw HTML lines 72-81, 84" still covers the symlink sentence, the pipes-and-sockets sentence, and `type:[inode]`. It does not include the socket example at lines 86-87; that example illustrates the same `type:[inode]` sentence rather than a second mechanism.

## 4. Proposed status / recheck / used-by

no change

Freeze S251 fields (line 260; `git diff -U0 55c07cd3 -- corpus/SOURCES.md` printed no S251 hunk): status `mined`, recheck `180d`, used-by `corpus/knowledge/census-identity-r46.md, corpus/lessons/round-48.md`.

## Proposed row (id assigned by the L1)

Do not admit. The symlink and `type:[inode]` facts are already S251. The directory-child proposition is not on the page.

`| (L1) | Linux man-pages proc_pid_fd(5) — https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html | docs | A | Whether /proc/pid/fd/N can be followed by a child path when the descriptor is a directory, as distinct from a pipe or socket | DESCRIPTION lines 73-87 and the only /proc/self/fd/N example at line 120; Linux man-pages 6.19 footer 2026-02-08; HTML sha256 3a50ddef6f2f3a4f1139dcef3299a5eadf8fc96514df9fcb329a3bffd47ff27e; fetched 2026-10-28, byte-identical to the S251 pin | REJECTED: duplicates S251 (lines 73-84 already say the entry is a symlink to the actual file and that a pipe or socket reads type:[inode]); the page never states /proc/self/fd/N/child traversal for a directory descriptor; flip: a located sentence that a directory descriptor's fd symlink may be followed by a further path component, or a pipe-versus-socket fact outside lines 72-88 | rejected | 2026-10-28 | 180d | — |`

Gate quote for that rejection (lines 74-75, 20 words): "which the process has open, named by its file descriptor, and which is a symbolic link to the actual file."

## Not done

Did not run the census or its selftest. Did not fetch the man-pages git tag (the authorized fetches were the two man7 URLs). Did not test a live directory fd or a pipe fd on this host.
