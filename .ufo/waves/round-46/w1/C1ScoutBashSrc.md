VERDICT: supports

Access date: 2026-10-27. Scope: C1 source claims and honesty boundary.

- S250 re-fetch: all three GNU Bash 5.3 files match frozen SHA256SUMS byte-for-byte: shell.c `5f3d…bf73d`, general.c `669e…bd165`, general.h `bf92…f2f2`; S251 proc_pid_fd(5) matches `3a50…ff27e`. Full digests in `.ufo/waves/round-46/w1/C1ScoutBashSrc/digests.txt`. URLs are recorded in frozen `FETCH.txt` lines 2-8. [Observed: FETCH.txt lines 2-8; receipt digests.txt.]
- Cited source locations confirmed in fetched/tag-pinned S250: `shell.c:776-785` selects the script path or stdin and assigns stdin as descriptor 0; `shell.c:1584-1586` opens the filename; `shell.c:1697-1703` calls `move_to_high_fd(fd, 1, -1)`, assigns the resulting fd to `default_buffered_input`, and sets close-on-exec. `general.c:680-704` scans for a high fd, uses `dup2`, closes the original on successful move, and returns the descriptor; `general.h:251-252` sets `HIGH_FD_MAX` to 256. [Observed: frozen source paths/lines; URLs in FETCH.txt.]
- Official patch index `https://ftp.gnu.org/gnu/bash/bash-5.3-patches/` accessed 2026-10-27 lists 001–020, with 020 latest observed. Patch 016 is the only one of these touching `general.c`; none touches `shell.c`. 016 and 019 touch `general.h`. No downloaded patch body references `open_shell_script` or `move_to_high_fd`; neither cited function is modified in patches 001–020. Target-file inventory and SHA256s: `.ufo/waves/round-46/w1/C1ScoutBashSrc/patch-list.txt`. Host reports `bash 5.3.20-1` (`pacman -Q bash` output); that confirms installed package version, not independent patch provenance.
- `input.c` is relevant to a bounded caveat, not a contradiction: its header calls it buffered input, and source lines 78-86 read into local buffers; lines 180-228 manage per-fd buffered streams and input descriptor state (upstream `input.c`, SHA in digest receipt). Therefore a descriptor identifies the opened file object, but once Bash has read ahead, its buffered bytes may no longer reflect later changes to that object. The descriptor-backed identity is a claim about bytes accessible through the held descriptor at measurement time, not proof every byte executed was identical if the underlying file mutates during execution. [Inference from observed input buffering; source URL `https://git.savannah.gnu.org/cgit/bash.git/plain/input.c?h=bash-5.3`, accessed 2026-10-27.]

Located source quotes (each <=25 words):
- S250 shell.c:782-784: “Bash is reading a script from stdin, which is a pipe or redirected file.”
- S250 shell.c:1697-1703: “try to move the file descriptor to a randomly large one” then assigns it as buffered input and sets close-on-exec.
- S250 general.h:251-252: “Default maximum for move_to_high_fd” / `HIGH_FD_MAX 256`.
- S250 input.c:1: “functions to perform buffered input with synchronization.”
- S251 `proc_pid_fd(5)` fetched from `https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html`; matching digest recorded. The specific `/proc/$$/fd/<n>` reopening semantics were not separately quoted here; see pinned S251 document for its full language.

No tools installed. No lane/source files modified. Scratch removed after receipts.