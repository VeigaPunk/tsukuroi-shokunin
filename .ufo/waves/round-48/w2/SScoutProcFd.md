VERDICT: draft

# SRC-N1 — proc(5) fd magic links: live re-open of record, round 48

Seat: SScoutProcFd (tsukuroi lane, round 48 w2, L2 scout). Item: open the primary documentation
LIVE for C1's `/proc/<pid>/fd/<n>` magic-link mechanism; locate the symlink sentence, the
reopenable statement and directory-fd grounding; draft a non-duplicate SOURCES row.

## Live fetches (opener of record, this round)

`date -u +%F` → **2026-10-28**. Fetches run 2026-10-28T12:03:58Z–12:04Z with
`curl -fsSL --max-time 60` into `/fast/scratch/hyaku/tsukuroi-r48/SScoutProcFd/`
(receipts copied to `w2/SScoutProcFd/`, digests in `w2/SScoutProcFd/SHA256SUMS.txt`):

| URL | bytes | sha256 |
|---|---|---|
| https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html | 11359 | `3a50ddef6f2f3a4f1139dcef3299a5eadf8fc96514df9fcb329a3bffd47ff27e` |
| https://man7.org/linux/man-pages/man5/proc.5.html | 31125 | `b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97` |
| https://docs.kernel.org/filesystems/proc.html | 147701 | `f1c9cfc8d9779e8bb339e9b91761036caf71d3e5a6eb5dda5c1c34e98500b5db` |
| https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_fd.5?h=man-pages-6.19 | 4199 | `81e9f7238c80b5555b2e41a7d35c1427dc8da800a19d94aa8fe868c2f2f3ab13` |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst | 107560 | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` |

**Compare with pinned snapshot digest:** the pinned snapshot is
`.ufo/waves/round-47/frozen/src/proc_pid_fd.5.html` (also round-46's copy), digest
`3a50ddef6f2f3a4f1139dcef3299a5eadf8fc96514df9fcb329a3bffd47ff27e` (recorded in S251's anchor
and `git show ae99f021b76f8eb1c8805d32d80644464afb1ff6:.ufo/waves/round-47/frozen/src/proc_pid_fd.5.html | sha256sum`
→ same). **Today's live fetch is byte-identical to the pin — man7.org render unchanged across
r46→r47→r48 re-opens.** (Round-47's FETCH.txt/SHA256SUMS record only mktemp.html; the fd page
was re-fetched that round per S251's anchor text.)

## Located anchor sentences (verbatim, ≤25-word slices marked)

man7.org `proc_pid_fd(5)` DESCRIPTION, raw-HTML lines 72–76 (receipt `proc_pid_fd.5.html`;
troff `man/man5/proc_pid_fd.5` lines 11–15):

> "This is a subdirectory containing one entry for each file which the process has open,
> named by its file descriptor, and which is a symbolic link to the actual file."

Full sentence is 30 words; a compliant ≤25-word slice naming the sentence itself:
**"one entry for each file which the process has open, named by its file descriptor, and
which is a symbolic link to the actual file."** (25 words.)

**What the page says about the link being reopenable** — DESCRIPTION, raw-HTML lines 71–86:
programs taking a filename argument "can nevertheless be made to use standard input or
standard output by using /proc/pid/fd files as command-line arguments", with worked examples
`foobar -i /proc/self/fd/0 -o /proc/self/fd/1` and `/dev/stdin`–`/dev/stderr` aliases — i.e.
**opening (not just `readlink(2)`-ing) the fd entry re-opens the underlying file**; pipes and
sockets are the documented exception shape (`socket:[2248868]`, `type:[inode]`), and
dereference permission is governed by a `PTRACE_MODE_READ_FSCREDS` ptrace check (line 137).

**Directory fd (`exec N<dir`)** — not stated as a case on the page, but grounded
empirically this round (host kernel 7.2.11-arch1-1, bash in scratch):

```
exec 240<"$D"            # opens: bash < redirection opens directories O_RDONLY
readlink /proc/self/fd/240        → /fast/scratch/hyaku/tsukuroi-r48/SScoutProcFd/fx.Rsmb1J
stat -Lc %F /proc/self/fd/240     → directory
cat "/proc/self/fd/240/sub dir/f.txt" → hi          # traversal THROUGH the dir fd works
readlink -f ".../240/sub dir/f.txt" → $D/sub dir/f.txt
ls -l /proc/self/fd               → lr-x------ 240 -> $D
exec 241<"$S/dirty dir.36mXPg"; cat /proc/self/fd/241/inner/x → ok   # space in path fine
```

This is exactly the frozen census mechanism: `selftest_base_dir` opens TMPDIR on fd 240–249
and spells it `/proc/self/fd/<n>` so a space-bearing TMPDIR still yields a whitespace-free
base INSIDE TMPDIR (`tools/tsukuroi-census.sh@ae99f02:2049-2085`).

**proc(5) parent page** (`proc.5.html`, sha256 `b197c5…72a97`): no inline fd text; its fd
coverage is the hyperlink `proc_pid_fd(5)` — the split-out page above is the correct anchor.

**Kernel `Documentation/filesystems/proc.rst`** (render `docs.kernel.org/filesystems/proc.html`,
sha256 `f1c9cf…5db`; pinned rst `torvalds/linux v7.2`, sha256 `e760f7…d126`, lines 2302–2307),
section **3.13 `/proc/<pid>/fd` — List of symlinks to open files**:

> "This directory contains symbolic links which represent open files the process is maintaining."

(13 words.) Its `ls -l` example shows `10 -> 'socket:[12539]'` quoting inode strings for
sockets, and notes the open-file count is `stat()`'s `size` member. No reopenability or
directory-fd text — corroborating secondary, not the primary anchor.

## SOURCES row draft (11 columns: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by)

**Duplicate-URL check (frozen registry, `grep -cF` on `corpus/SOURCES.md@ae99f02`):**
`man7.org/linux/man-pages/man5/proc_pid_fd` → **1** (S251; a same-URL row is refused);
`docs.kernel.org/filesystems/proc` → 0; `man-pages.git/plain/man/man5/proc_pid_fd` → 0;
`raw.githubusercontent.com/mkerrisk` → 0; `docs.kernel.org` any row → 1 (S063 zswap, unrelated).
`Documentation/filesystems/proc.rst` exists only at S148 under the same torvalds/linux v7.2 URL
for the OOM-badness scope — reusing it would rest on an already-used URL, so the draft below
takes the cleanest non-duplicate: the **upstream man-pages tag source**, byte-digestible and
precedent-matching S181's git.kernel.org scheme.

```
| S253 | man-pages 6.19 — proc_pid_fd(5) — https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_fd.5?h=man-pages-6.19 | docs | A | The /proc/<pid>/fd/<n> entry semantics the census selftest fd alias and census identity rely on: an fd entry is a symbolic link to the actual file, re-openable as a path, with pipe and socket entries reading type and inode instead | tag man-pages-6.19 (annotated tag object 5a7bf78fd314b8390f30bee87aa2e933b7a8f880, peeled commit adb436b2e4471218021d86f188fb58dec3946eb8); man/man5/proc_pid_fd.5 lines 11-15, 17-22, 71-86, 107-116, 128-130; raw bytes sha256 81e9f7238c80b5555b2e41a7d35c1427dc8da800a19d94aa8fe868c2f2f3ab13 | each fd entry is a symbolic link to the actual file and can be opened as a path to reuse the file (worked /proc/self/fd/0 example); pipes and sockets read type:[inode]; traversal of a directory descriptor as /proc/self/fd/N/x is kernel behavior observed on this host, not spelled out by the page | queued | 2026-10-28 | on-release | — |
```

Status `queued` + used-by `—`: no knowledge file cites the row yet. A `mined` flip with
used-by `corpus/knowledge/census-identity-r46.md` is honest only if that file's `source:` line
is amended to name S253 alongside S251 (it currently cites S250 S251). Kernel corroboration,
if the L1 prefers a docs.kernel.org render row instead: §3.13 quote above, render sha256
`f1c9cf…5db` (mutable render — tag-pinned rst `e760f7…d126` is the verifiable blob).

## Gaps / honest notes

- The page does **not** document directory-descriptor child traversal (`/proc/self/fd/N/x`);
  C1's mechanism rests on general symlink semantics — the empirical transcript above is the
  concrete grounding, and bash `exec N<dir` itself is POSIX shell behavior outside this page's
  scope (S250 covers bash's fd handling).
- Reopenability is shown for **stdio-style reuse** (fd 0/1/2 as pathname arguments); the page
  states no reopen guarantee distinct from ordinary symlink lookup.
- No tooling installed this seat; no mutation to lane or fleet. Scratch
  `/fast/scratch/hyaku/tsukuroi-r48/SScoutProcFd` removed after receipts were copied.
