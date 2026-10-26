VERDICT: supports

Seat: C2DraftRevSR1 (round 43, wave w1) — first-falsifier review of row SR1 of
`corpus/knowledge/btrfs-scrub-record-r43.md` at 717b716a8943151ace8657e0ca23d7d9b8434f26.
NOT a counted verdict (the frozen counter counts only w2 `C2RevSR*`/`C2CritSR*` seats).
Receipts: `.ufo/waves/round-43/w1/C2DraftRevSR1/receipts-sr1.md` (all commands + observed output).
Method: static read of the pinned sources only; no scrub run, no privileged ioctl, no host mutation;
no tools installed (none needed). This is a wave-1 falsifier read: I tried to break every sentence and could not.

## 1. Pinning (all verified)

- `cd .ufo/waves/round-43/frozen/src && sha256sum -c SHA256SUMS` → `ioctl.c: OK`, rc=0. That SHA256SUMS has the
  single line `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01  ioctl.c` — matches the declared
  S240 digest `7b3488f2…`. The directory contains only `FETCH.txt`, `SHA256SUMS`, `ioctl.c`.
- S237 scrub.c digest: `sha256sum .ufo/waves/round-42/frozen/src/scrub.c` →
  `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` — exact match to the declared digest. The
  round-43 `FETCH.txt` states scrub.c "(S237) is the round-42 frozen snapshot …, not re-fetched here", and the
  round-42 `SHA256SUMS` also passes (`scrub.c: OK`, `CHANGES: OK`).
- S241 capture digest: `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556` — matches.
- Draft revision: `git show 717b716…:corpus/knowledge/btrfs-scrub-record-r43.md | sha256sum` and
  `sha256sum` of the working-tree file both give `ee0d04797f88c8292b7dd9157ec23f0340134f939b92d99faf5187d398d83a1d`;
  `git diff --stat 717b716… 7d0ed1c…` over the draft is empty. The reviewed text is the pinned revision's text.

## 2. Quote fidelity: 8/8 verbatim at their named lines

Python substring test of each quoted string against its named line of the pinned scrub.c (receipts file):

- scrub.c:483 `fd = open(datafile, m, 0600);` — OK
- scrub.c:487 `ret = flock(fd, LOCK_EX|LOCK_NB);` — OK
- scrub.c:517 `return scrub_open_file(datafile, O_WRONLY|O_CREAT);` — OK
- scrub.c:534 `ret = rename(datafile_old, datafile_new);` — OK
- scrub.c:917 `fd = scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp");` — OK
- scrub.c:922 `err = scrub_write_file(fd, fsid, data, n);` — OK
- scrub.c:925 `err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");` — OK
- scrub.c:1485 `ret = unlink(sock_path);` — OK

## 3. Statement, sentence by sentence

S1 "Every record update goes through `scrub_write_progress`" — **holds.**
`scrub_write_file` has exactly two call sites: scrub.c:922 (the record `_tmp`) and scrub.c:1112, whose fd is
`peer_fd`, the connected progress-socket client (context :1110-1118: `write_poll_fd.fd = peer_fd; …
scrub_write_file(peer_fd, …); close(peer_fd);`) — a socket write, not a record write. `scrub_write_progress` call
sites: :1123 (progress thread, guarded by `if (!spc->do_record) continue;` :1121-1122), :1503 (initial all-zero
record at start, comment :1502 "write all-zero progress file for a start") and :1702 (final record). The only
`open(` call in the file is :483; the only write-mode open is :517 `O_WRONLY|O_CREAT` via `scrub_open_file_w`, whose
sole call site is :917. Even the record's creation goes through `scrub_write_progress`, so "every record update" is
not an overreach.

S2 "it opens `scrub.status.<fsid>_tmp` with `O_WRONLY|O_CREAT` and no `O_TRUNC` (mode 0600, then a non-blocking
`flock` `LOCK_EX`)" — **holds.** :917 passes tmp suffix `"tmp"`; `scrub_datafile` (:446-466) builds
`fn_base "." fn_local "_" fn_tmp`; `SCRUB_DATA_FILE` is `/var/lib/btrfs/scrub.status` (:67), so the opened path is
`/var/lib/btrfs/scrub.status.<fsid>_tmp`. Open flags `O_WRONLY|O_CREAT` (:517), mode 0600 (:483), then
`flock(fd, LOCK_EX|LOCK_NB)` (:487) returning `-errno` on failure (:488-491). `O_TRUNC` census over the whole
file: no matches; the only open modes used anywhere are `O_RDONLY` (:505) and `O_WRONLY|O_CREAT` (:517).

S3 "writes the whole record from the start of that file" — **holds.** The fd comes from a fresh `open(2)` (:483), so
the file offset is 0; `scrub_write_file` (:843-894) writes the version line (:856-859) plus one line per device for
all n devices (loop :863-893) through `scrub_write_buf` → `write(2)` (:773-777) and `scrub_writev` (:782-793).
Census: no `lseek`/`lseek64`/`pwrite`/`pwrite64`/`ftruncate`/`truncate` calls anywhere in scrub.c.

S4 "renames `_tmp` over `scrub.status.<fsid>` only when the write returned no error; a failed write skips the
`rename`" — **holds.** :922 `err = scrub_write_file(…)`, :923-924 `if (err) goto out1;`, :925
`err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp")`, which renames `…_<fsid>_tmp` → `….<fsid>` (`fn_tmp=NULL`
for the new name, :528-533) at :534, returning `-errno` on failure.

S5 "No code in `scrub.c` removes a `_tmp` file: its three `unlink` calls all name the progress socket path" —
**holds.** Census: exactly three `unlink` occurrences — :1485 `ret = unlink(sock_path);`, :1497
`unlink(sock_path);`, :1721 `unlink(sock_path);` — all inside `scrub_start`, all on `sock_path`
(decl :1271, filled from `SCRUB_PROGRESS_SOCKET_PATH` `/var/lib/btrfs/scrub.progress` :68 at :1461-1462).
No `remove(` / `unlinkat(` anywhere (census none). Nothing ever removes a `_tmp` file.

S6 "So a `_tmp` left behind by a failed write, a failed `rename` or a killed writer is opened again by the next
update" — **holds.** In all three leave-behind cases the flock is free: the failed write/rename paths close the fd
at `out1` (:929-932), and a killed writer's flock dies with the process; the next `scrub_write_progress` re-opens
the same path with `O_CREAT` and no `O_TRUNC` (:483/:517), which opens the existing leftover in place.

S7 "and when the new record is shorter, the old file's bytes past the new end stay in place and are renamed into the
record with it [inference from the open flags; not reproduced on this host]" — **holds as the tagged inference it
is.** It follows arithmetically from S2+S3+S4 (open without O_TRUNC at offset 0, no ftruncate anywhere, rename
publishes whatever bytes the file then holds), and my census (no `O_TRUNC`, no `ftruncate`/`lseek`/`pwrite`,
single `open(` at :483) corroborates the flags reading. It is honestly marked `[inference from the open flags; not
reproduced on this host]`, and no reproduction exists here either (the record directory is absent, capture.txt:7;
the host guard forbids running a scrub). I do not propose untagging it.

**Host reading.** "Not observable on this host: there is no record directory (`var_lib_btrfs absent`,
capture.txt:7)." — **holds.** capture.txt:7 is exactly `var_lib_btrfs absent`; capture digest matches S241's
declared `f7ecbe7c…` (section 1).

## 4. Findings by severity

- Blockers / defects: none. No sentence of SR1's Statement or Host reading overreaches the pinned sources.
- Informational (no replacement proposed): the Statement writes the temp name as `scrub.status.<fsid>_tmp`, the
  basename of `/var/lib/btrfs/scrub.status.<fsid>_tmp` (SCRUB_DATA_FILE, scrub.c:67 + scrub_datafile :446-466).
  This matches the row's own convention elsewhere ("`scrub.status.<fsid>_tmp` lying beside the record"), so no text
  change is warranted.

## 5. Proposed replacement text

None. Every sentence holds; the one inference (S7) is already correctly tagged. The row's frozen proposition tokens
(`_tmp` opened `O_WRONLY|O_CREAT` without `O_TRUNC`; renamed only after a successful write; never unlinked;
trailing-bytes consequence `[inference]`) are preserved untouched.

## 6. Residual risk and verification gaps

- Static source read only: I did not compile or execute btrfs-progs, and did not reproduce the trailing-bytes
  behaviour (impossible within the host guard: no record directory on this host, scrub start forbidden).
- I verified the pinned snapshots' digests against the declared values and the round-42/round-43 `SHA256SUMS`
  files; I did not re-fetch upstream (that is the row's `recheck: on-release` procedure). FETCH.txt (round-43)
  documents the 2026-10-26 fetch of ioctl.c at tag v7.2.11.
- The Limits-section claim that Arch's btrfs-progs 7.1-1 applies no patch is attributed to round-42 wave-1
  (C2ExecLiveSources) and is outside SR1's Statement/Host reading; I did not re-check it.
- SR3/SR6 rows and the ioctl.c side (S240) are out of my scope; only the S240 digest was checked.
- First-request semantics: all lookups here are file reads of pinned snapshots (no LSP server involved for C source);
  the per-line quote test is programmatic, not a cold-cache guess.
