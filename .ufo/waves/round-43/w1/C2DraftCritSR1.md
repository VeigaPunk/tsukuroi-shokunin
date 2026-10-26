VERDICT: defect-found

Item: C2-C-SR1 — adversarial attack (wave-1 first falsifier, NOT a counted verdict) on row SR1 of
corpus/knowledge/btrfs-scrub-record-r43.md (at 717b716a8943151ace8657e0ca23d7d9b8434f26), against pinned sources
S237 = .ufo/waves/round-42/frozen/src/scrub.c (btrfs-progs v7.1), S240 = .ufo/waves/round-43/frozen/src/ioctl.c
(Linux v7.2.11), S241 = .ufo/waves/round-43/frozen/hostcap/capture.txt. All source line numbers below are S237.

## 1. Clause-by-clause verification (what holds)

- "Every record update goes through `scrub_write_progress`" — TRUE for the record file. Grep of S237 shows exactly three
  call sites: :1123 (progress thread, periodic), :1503 (start/resume initial all-zero write), :1702 (final result write).
  The only other open of SCRUB_DATA_FILE is read-only `scrub_open_file_r` (:1361, :1930; `O_RDONLY`, :505) — it never
  creates or modifies the record. The socket handoff at :1112 writes to `peer_fd` (progress socket), not the record.
- Open flags — TRUE. `scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp")` (:917) → `scrub_datafile` builds
  "…/scrub.status.<fsid>_tmp" (:446-476) → `scrub_open_file` opens `open(datafile, m, 0600)` with
  `m = O_WRONLY|O_CREAT` (:483, :517) then `flock(fd, LOCK_EX|LOCK_NB)` (:487). No `O_TRUNC`, `truncate`/`ftruncate`,
  `remove(`, `rmdir` or `unlinkat` appears anywhere in S237 (grep, zero hits).
- "writes the whole record from the start of that file" — TRUE for n >= 1. `scrub_write_file` (:843-895) writes the
  version prefix and all per-device lines via `scrub_write_buf` = plain `write(2)` (:773-778); the file offset after the
  fresh open is 0 (no O_APPEND/O_TRUNC), so every update overwrites from offset 0.
- "renames `_tmp` over `scrub.status.<fsid>` only when the write returned no error; a failed write skips the `rename`" —
  TRUE. :922 `err = scrub_write_file(…)`; :923-924 `if (err) goto out1;`; rename only at :925. A failed rename also
  leaves `_tmp` (:926-927).
- "No code in `scrub.c` removes a `_tmp` file: its three `unlink` calls all name the progress socket path" — TRUE.
  `unlink` appears exactly three times: :1485 (bind-retry when `EADDRINUSE`), :1497, :1721 (socket cleanup, both guarded
  by `sock_path[0]`). `sock_path` is built only from `SCRUB_PROGRESS_SOCKET_PATH` (:1461), never from the record path.
- Host reading "var_lib_btrfs absent" — verified against S241 line 7; consistent with the row's own "not observable on
  this host" caveat.

## 2. Findings (overreach / omitted conditions) with exact replacement text

### F1 — "a killed writer" overreaches (the tool's own termination paths complete the update first)
The sentence "a `_tmp` left behind by a failed write, a failed `rename` or a killed writer" reads as if any kill leaves a
partial `_tmp`. The tool's cooperative cancellation paths do not:
- The progress thread disables cancellation before opening and re-enables only after close/unlock:
  `pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, &old)` at :905 precedes `scrub_open_file_w` (:917); re-enable at :941
  comes after the rename (:925) and close (:930-934). A pending `pthread_cancel` is therefore delivered only after the
  update (write + rename) has completed — even under the thread's `PTHREAD_CANCEL_ASYNCHRONOUS` type (:1021), because the
  disable window covers the whole write path.
- The master cancels and joins the thread at :1685/:1687 before the final record write (:1701-1708), and the cancelled
  thread still completes its last write+rename first.
- The parent ignores SIGINT (:426-434); the worker's SIGINT handler performs an ioctl cancel, not a kill
  (`BTRFS_IOC_SCRUB_CANCEL`, :417-424).

So the only kills that can leave a partial `_tmp` are uncatchable or default-terminate ones during the open→rename window
(SIGKILL, SIGTERM, power loss). Narrower replacement:
  "So a `_tmp` left behind by a failed write, a failed `rename`, or a writer killed by an uncatchable or
   default-terminate signal (SIGKILL, SIGTERM, power loss) before the rename is opened again by the next update…"
  (+ optional clause: "the progress thread's own cancellation (`pthread_cancel`, :1685; SIGINT→BTRFS_IOC_SCRUB_CANCEL,
   :421) is deferred until after the write and rename (cancel-state disable :905, re-enable :941) and never leaves a
   partial `_tmp`.")

### F2 — "mode 0600" omits the umask caveat
`open(datafile, m, 0600)` (:483) passes 0600 as the *mode argument*; the effective mode of a newly created file is
`0600 & ~umask`. Round-42 SC1 already held this caveat ("subject to the umask", btrfs-scrub-record-r42.md:23). Narrower
replacement: "(mode argument 0600; effective mode subject to the caller's umask)".

### F3 — "Every record update goes through `scrub_write_progress`" needs a record-file scope
True as written, but the same thread also writes live progress to the socket fd (`scrub_write_file(peer_fd, …)`, :1112),
which is not a record update. Narrower replacement: "Every record-file update in `scrub.c` goes through
`scrub_write_progress` (the three call sites :1123, :1503, :1702)".

### F4 — the trailing-bytes inference is conditional on the next update succeeding; and on no lock contention
The [inference] clause presumes the next update's write *and* rename succeed; if the next write fails, the tail stays in
the `_tmp` and is not renamed into the record. Also, `flock(LOCK_EX|LOCK_NB)` is non-blocking: if a lock holder existed
the open would fail (`-errno`, :488-492) and no reuse would occur — unreachable in practice because a second writer on the
same fsid is blocked at the progress socket (:1474-1480). Precision note: "…is opened again by the next update, and if
that update's write and rename succeed and the new record is shorter, the old file's bytes past the new end stay in place
and are renamed into the record with it."

### F5 — corner, not a defect: n < 1
`scrub_write_file` returns `-EINVAL` without writing a byte when n < 1 (:852-853), leaving an empty `_tmp` behind (the
open already created it). The three call sites pass `ndev = num_devices` ≥ 1 (:1005, :1124), so this is unreachable in
practice; if the row wants absolute precision: "writes the whole record (all n devices; n = num_devices ≥ 1)".

## 3. Does SR1 add detail the lane does not already hold as verified text?

- As verified (counted) text, the lane held none of this before round 43: round-42 SC1 — which held the write discipline
  — is withdrawn ("SC1 and SC3 below stand withdrawn and are not a verified outcome", r42.md:4), and SKILL.md holds only
  the absence-reading SH4 (SKILL.md:2368: no record ⇒ UNVERIFIED), not the write mechanism.
- The write-discipline facts DO already appear verbatim in the round-42 "Corrections — round-42 wave 2" block
  (r42.md:178-184: full `_tmp` write→rename discipline, `O_WRONLY|O_CREAT` without `O_TRUNC`, never deleted, reuse from
  offset 0, shorter-record tail). That block explicitly carries no counted verdict (r42.md:171, :175-176) and is seat-written
  text — i.e., a candidate, per lesson R42-ADOPTED-UNREAD. SR1 re-grounds the same claims as a count-eligible row.
- Genuinely new detail in SR1: (a) the unlink enumeration — "its three `unlink` calls all name the progress socket path"
  (the r42 corrections assert "never deleted" without this justification); (b) quote-level grounding of every clause to
  pinned lines; (c) the explicit [inference] tag on the trailing-bytes consequence — the r42 corrections asserted that
  consequence as fact (r42.md:182-184), exactly the pattern R42-ADOPTED-UNREAD warns against; SR1 fixes that.
- SR1 drops the reader-side consequence present in the r42 corrections ("`btrfs scrub status` reports `invalid data on
  line …` (:569-576) until a longer record is written", r42.md:183-184). That fact survives today only in the uncounted
  corrections; the `_SCRUB_INVALID` warning is real (scrub.c:569-576, warning text at :571). If the lane wants it, it
  needs its own counted row, not SR1.

## 4. What I did not do
Read-only seat: no fixture, no clone, no live run; no scrub started; no ioctl issued; no host mutation; no tools
installed (none needed). Scratch dir /fast/scratch/hyaku/tsukuroi-r43/C2DraftCritSR1 created, unused, and removed.
Every claim above is a direct read of the pinned files (paths as quoted) on 2026-10-26.
