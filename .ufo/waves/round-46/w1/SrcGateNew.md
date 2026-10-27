VERDICT: supports

# Seat SrcGateNew — F-1: draft `## Gate` rows for S250 and S251 (round 46, wave `w1`)

Both new registry rows were re-opened by this seat on 2026-10-27 (UTC) with `curl` into
`/fast/scratch/hyaku/tsukuroi-r46/SrcGateNew/curl`, their live bytes compared with
`.ufo/waves/round-46/frozen/src/SHA256SUMS`, and every quote located by line number in the live fetch.
The block below is ready to paste; the reject table carries five refused candidates, each with a
source-checked reason and a flip.

## Evidence — what was run (observed)

| Check | Command | Observed output |
|---|---|---|
| fetch window | `date -u` before/after the four curls | `2026-10-27T05:23:21Z` → `2026-10-27T05:23:37Z` |
| S250 `shell.c` | `curl -sSL -o shell.c "https://git.savannah.gnu.org/cgit/bash.git/plain/shell.c?h=bash-5.3"` | `http=200 bytes=59208`; sha256 `5f3d539f15e19c032a09ece500efecc9c63d050d408e985b6f385c64329bf73d` |
| S250 `general.c` | same form, `general.c?h=bash-5.3` | `http=200 bytes=36727`; sha256 `669ef408f4bcc6b4ce424677d29532f28e903430c93b335fa1a292dd360bd165` |
| S250 `general.h` | same form, `general.h?h=bash-5.3` | `http=200 bytes=11459`; sha256 `bf9251e3270c933d3387828a263a3d30e4f0de7ec02b802b1f0f99a60ad3f2f2` |
| S251 `proc_pid_fd(5)` | `curl -sSL -o proc_pid_fd.5.html "https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html"` | `http=200 bytes=11359`; sha256 `3a50ddef6f2f3a4f1139dcef3299a5eadf8fc96514df9fcb329a3bffd47ff27e` |
| vs frozen | `sha256sum` on both sides, then `cmp -s` live vs frozen | 4/4 digests equal, `cmp` 4/4 `identical` (`w1/SrcGateNew/digests-live.txt`) |
| tag pin | `git ls-remote https://git.savannah.gnu.org/git/bash.git refs/tags/bash-5.3` (2026-10-27T05:25:53Z) | `b8c60bc9ca365f8261fa97900b6fa939f6ebc303	refs/tags/bash-5.3` — equals `FETCH.txt` and the S250 anchor |
| host package | `pacman -Q bash` | `bash 5.3.20-1` — equals the S250 anchor's host note |
| row shape at IMPL | `git -C …/tsukuroi-shokunin diff --stat 2042117c… a4477049… -- corpus/SOURCES.md` | `1 file changed, 2 insertions(+)` — new rows only; `grep -c '^\| S[0-9]' corpus/SOURCES.md` → `251` |

Located quotes are in `w1/SrcGateNew/quotes.txt` (verbatim lines for `shell.c:782-784`, `:1586`,
`:1697-1703`, `general.c:685-705`, `general.h:250-252`, `proc_pid_fd.5.html:69-88`).

## Draft block for `corpus/lessons/round-46.md` — `## Gate`

### New SOURCES rows (opened 2026-10-27 by wave `w1`; each quote located with `grep -n`/`awk` in a live fetch whose bytes equal the frozen snapshot; drafted by seat SrcGateNew, checked by the L1)

| Row | URL (access 2026-10-27) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S250 | https://git.savannah.gnu.org/cgit/bash.git/plain/shell.c?h=bash-5.3 (same `plain/…?h=bash-5.3` form for `general.c` and `general.h`; live bytes = `frozen/src/SHA256SUMS`) | "try to move the file descriptor to a randomly large one"; "fd = move_to_high_fd (fd, 1, -1);"; "SET_CLOSE_ON_EXEC (default_buffered_input);"; "if (nfds > HIGH_FD_MAX)" / "nfds = HIGH_FD_MAX;"; "for (nfds--; check_new && nfds > 3; nfds--)" / "dup2 (fd, nfds)"; "#define HIGH_FD_MAX	256"; "bash is reading a script from stdin, which is a pipe or redirected file"; "default_buffered_input = fileno (stdin);	/* == 0 */" | shell.c:1697-1698, :1700, :1703, :782-784; general.c:690-691, :696, :700; general.h:252 (the open itself at shell.c:1586, "fd = open (filename, O_RDONLY);") |
| S251 | https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html | "named by its file descriptor, and which is a symbolic link to the actual file"; "For file descriptors for pipes and sockets, the entries will be symbolic links whose content is the file type with the inode"; "type:[inode]" | proc_pid_fd.5.html:73-75, :79-81, :84 |

Snapshot digests: `.ufo/waves/round-46/frozen/src/SHA256SUMS` (shell.c `5f3d539f…bf73d`, general.c
`669ef408…bd165`, general.h `bf9251e3…f2f2`, proc_pid_fd.5.html `3a50ddef…ff27e`), fetch log `FETCH.txt`
(2026-10-27T04:59:34Z; general.h 05:00Z). Live re-fetches by seat SrcGateNew at 2026-10-27T05:23:21Z-05:23:37Z
were byte-identical to all four digests (`sha256sum` 4/4 match, `cmp` live-vs-frozen 4/4 identical,
`w1/SrcGateNew/digests-live.txt`). Tag re-resolved the same day:
`refs/tags/bash-5.3` `b8c60bc9ca365f8261fa97900b6fa939f6ebc303` — unchanged from `FETCH.txt`. The anchor's line
ranges all resolve: `shell.c:776-784` selects script vs stdin, `:1586` opens the file, `:1700-1703` moves and
marks it close-on-exec, `general.c:681-703` is the body of `move_to_high_fd` (function spans 680-710),
`general.h:252` is `HIGH_FD_MAX 256`.

### Reject rows (candidates considered this round and refused)

| Entry (candidate) | Rejected | Reason (source-checked) | Flip |
|---|---|---|---|
| `doc/bash.1` at tag bash-5.3 — https://git.savannah.gnu.org/cgit/bash.git/plain/doc/bash.1?h=bash-5.3 (sha256 `23f7bd155c57125864094d2cb4e1f6ec9f8c2ea002e18bebeb3ed4bcfaad1971`, 392678 bytes, 13495 lines, fetched 2026-10-27 `http=200`) | yes — considered as the docs-tier source for S250's `teaches` cell; refused | The tag's own manual never states which descriptor bash holds an opened script on: `grep -nE '\b255\b'` returns one hit, `:5912` "Exit statuses fall between 0 and 255" (EXIT STATUS); `grep -niE 'HIGH_FD_MAX\|move_to_high_fd\|close.on.exec\|script descriptor'` returns nothing (rc=1); INVOCATION names a script only as `:392` "is started non-interactively, to run a shell script, for example, it looks for the variable BASH_ENV"; the sole descriptor-above-9 sentence is the redirection warning `:4763-4765` "Redirections using file descriptors greater than 9 should be used with care, as they may conflict with file descriptors the shell uses internally" — a caution, not a locator | the manual states the descriptor a script file is read from (or documents `move_to_high_fd`); it then becomes the docs row beside S250 and S250 need only pin the code lines |
| `bash(1)` from the installed package — `/usr/share/man/man1/bash.1.gz` (`pacman -Qo` → `bash 5.3.20-1`), gz sha256 `b68beb3e385f7d8aead26bf7887c12f93ca769dcd528fd7282d70938b09bdffe`, text `415026365b02d5a0c2dd64322bb61065bbb57003de7c5c64a91ba9c07b076c92`, 7319 lines | yes — the patched-page variant of the same candidate | Same negative on the installed page: the only `\b255\b` is `:3160` "255, though, as explained below, the shell may use values above 125 specially" (EXIT STATUS), and `grep -niE 'close.on.exec\|HIGH_FD_MAX\|move_to_high_fd\|script descriptor\|descriptor .*the script'` is empty. ("descriptor" contains the substring "script", so a bare `grep -i script` over-matches; the greps use word boundaries.) It is also host-version-pinned (5.3.20-1) and so cannot carry a `bash-5.3` anchor even if it did | as above; if a patched page documents it, the row must pin the 5.3.20-1 page digest and say the anchor is the host version |
| GNU Bash Reference Manual — https://www.gnu.org/software/bash/manual/bash.html | yes — considered as the tag-current manual; no bytes obtained | Unreachable from this host on 2026-10-27: `curl -sSL --max-time 25` → `curl: (28) Connection timed out after 25001 milliseconds`, `http=000`, 0 bytes; a first attempt failed the same way after 136 s. No bytes → no digest → no quote, so nothing could be admitted | a fetch that returns bytes with a stable locator (or a digest-pinned archived copy) and a line stating the script descriptor |
| `input.c` at bash-5.3 — https://git.savannah.gnu.org/cgit/bash.git/plain/input.c?h=bash-5.3 (sha256 `d88d0583932086cce7dc4a4db18407c084991b1574383c833579ca9ce2f2a50b`, 16027 bytes, fetched 2026-10-27 `http=200`) | yes — read this round for the identity honesty boundary (`w1/C1ScoutBashSrc.md`); not admitted as a registry row | Its lines decide buffering, not the descriptor: `:1` "functions to perform buffered input with synchronization", `:78-79` "Try local buffering to reduce the number of read(2) calls", `:86` "local_bufused = read (fileno (stream), localbuf, sizeof(localbuf))". The consequence it supports — read-ahead means the descriptor bytes hashed are not proof of every byte executed under mutation — is carried as `[inference]` in the entry's Limits, so a row would have no claim of its own | the entry asserts executed-byte equality under concurrent mutation; then `input.c` is pinned with these lines as a registry row |
| staged merge registry `merge/tsukuroi/SOURCES.append.md` (147 rows, first staged id S200; `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/MERGE-REPORT.md:5-10`) | yes — assimilation refused this round (`w1/AsmGate.md`, "Theme recommendation": assimilation none) | 52 of its ids collide with the lane registry S200-S251 (`w1/AsmGate/reg-ids` 251, `staged-ids` 147, `collisions` 52; first `S200`-`S202`, last `S249`-`S251`), so the merge's continuous S-ID assumption does not hold and the registry cannot be appended as-is; its theme search found no staged `census-identity` or `btrfs-scrub-grounding` entry (existence checks false) | staged entries renumbered into a disjoint id space, and a claim carrying a locator for a surface this round moved |

Collision arithmetic checked against round 45's lesson: 50 collisions against 249 rows then, 52 against 251 now —
the two new rows S250/S251 are exactly the difference (`w1/AsmGate/collisions` tail `S249`/`S250`/`S251`).

## Limits — what this seat did not do

- Did not run the C1 counter, `tools/tsukuroi-census.sh --identity`, or any census selftest (one C1 counter per
  seat; C1Exec*/C1Lab* own those), and did not read the `--identity` implementation. The quotes above support the
  SOURCES `teaches` cells, not the implementation.
- Did not run `scripts/sources-census.sh validate` (seat SrcReview, F-2, runs it; this seat avoided a second
  write-capable run).
- Did not re-open S246-S249 or S237/S242-S244 — the "Re-opened rows and rows touched old→new" block is seat
  C2-S10's; my block covers new rows and rejects only.
- The reference manual could not be opened at all (two `curl` failures, `rc=28`), so the manual-side negative rests
  on the tag's own `doc/bash.1` and the installed `bash(1)` page, both of which I did read.
- The S251 row's line numbers are in the man7.org raw HTML, which `cmp` shows identical to the frozen copy; I did
  not compare against the Arch-packaged `proc_pid_fd.5` man page.
- No tool installed or upgraded; nothing written outside `/fast/scratch/hyaku/tsukuroi-r46/SrcGateNew/` (removed)
  and `.ufo/waves/round-46/w1/SrcGateNew{,.md}`. No lane file, fleet-root file, PATH directory or host state touched.

Receipts: `.ufo/waves/round-46/w1/SrcGateNew/` — `digests-live.txt`, `quotes.txt`, `bash53-man-negative.txt`,
`bash-man-negative.txt`, `reject-input-c.txt`, `commands.txt`.
