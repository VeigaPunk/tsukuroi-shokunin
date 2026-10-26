ROW SR1 VERDICT: holds

Seat: C2CritSR1 (round 43, wave w2, counted verdict). Item V-SR1-C, row SR1 of
`corpus/knowledge/btrfs-scrub-record-r43.md` at 8acf0b022586a0f3164c77659fb96ba5f90949b6. Adversarial review:
I hunted for a false or overreaching sentence and found none. Every sentence of the row's `Statement.` and
`Host reading.` is supported by the pinned source lines (S237 scrub.c, S240 ioctl.c, S241 capture.txt); the
one `[inference]` sentence is labelled and is a reasonable reading of those lines; the label names the wave-1
reproduction (C2ExecTailRepro).

## 1. Pins verified (commands, observed output)

- `sha256sum .ufo/waves/round-42/frozen/src/scrub.c` →
  `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` (matches declared 48df2e2f…0801).
- `cd .ufo/waves/round-43/frozen/src && sha256sum -c SHA256SUMS` → `ioctl.c: OK`, rc=0 (matches declared S240).
- `sha256sum .ufo/waves/round-43/frozen/hostcap/capture.txt` →
  `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556` (matches declared f7ecbe7c…c556).

## 2. Quote fidelity: 9/9 verbatim at their named lines (programmatic substring check)

| Line | Quote | Result |
|---|---|---|
| scrub.c:483 | `fd = open(datafile, m, 0600);` | OK |
| scrub.c:487 | `ret = flock(fd, LOCK_EX|LOCK_NB);` | OK |
| scrub.c:517 | `return scrub_open_file(datafile, O_WRONLY|O_CREAT);` | OK |
| scrub.c:534 | `ret = rename(datafile_old, datafile_new);` | OK |
| scrub.c:905 | `ret = pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, &old);` | OK |
| scrub.c:917 | `fd = scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp");` | OK |
| scrub.c:922 | `err = scrub_write_file(fd, fsid, data, n);` | OK |
| scrub.c:925 | `err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");` | OK |
| scrub.c:1485 | `ret = unlink(sock_path);` | OK |

(Full table with observed line text in receipts `w2/C2CritSR1/receipts-sr1.md`.)

## 3. Statement, sentence by sentence

- S1 "Every update of the record file goes through `scrub_write_progress` (its three call sites write the first
  record, the progress thread's records and the final record)" — holds. `scrub_write_progress` has exactly three
  call sites: scrub.c:1123 (progress thread loop, guarded by `if (!spc->do_record) continue;` :1121-1122),
  :1503 (initial record at start/resume, `if (do_record)` :1501, comment :1502 "write all-zero progress file for a
  start"), :1702 (final record after thread join, `if (do_record)` :1701). The only other open of the record file
  is read-only `scrub_open_file_r` (:1361, :1930 → `O_RDONLY` :505); `scrub_write_file` is also called at :1112
  but on `peer_fd`, the progress-socket client, not the record. No other writer exists.
- S2 "it opens `scrub.status.<fsid>_tmp` with `O_WRONLY|O_CREAT` and no `O_TRUNC` (open mode argument 0600,
  subject to the umask; then a non-blocking `flock` `LOCK_EX`)" — holds. `scrub_open_file_w(SCRUB_DATA_FILE,
  fsid, "tmp")` (:917) → `scrub_datafile` builds `scrub.status.<fsid>_tmp` (:446-476; SCRUB_DATA_FILE =
  `/var/lib/btrfs/scrub.status` :67) → `scrub_open_file` → `open(datafile, m, 0600)` with `m =
  O_WRONLY|O_CREAT` (:483, :517), then `flock(fd, LOCK_EX|LOCK_NB)` (:487). O_TRUNC census over the whole file:
  0 hits; the only open modes anywhere are O_RDONLY (:505) and O_WRONLY|O_CREAT (:517).
- S3 "writes the whole record from the start of that file" — holds. Fresh fd, offset 0 (no O_APPEND/O_TRUNC, no
  lseek/pwrite anywhere); `scrub_write_file` (:843-895) writes the version prefix (:856-859) and every device's
  line (loop :863-893) sequentially via `scrub_write_buf` = plain `write(2)` (:773-778) / `scrub_writev`
  (:782-793). n = `fi_args.num_devices` ≥ 1 (guaranteed by the early exit when `!num_devices`, :1354-1358).
- S4 "renames `_tmp` over `scrub.status.<fsid>` only when the write returned no error; a failed write skips the
  `rename`" — holds. :922 `err = scrub_write_file(…)`; :923-924 `if (err) goto out1;`; rename only at :925
  (`scrub_rename_file` → `rename(datafile_old, datafile_new)` :534). A failed rename also keeps `_tmp` (:926-927).
- S5 "No code in `scrub.c` removes a `_tmp` file: its three `unlink` calls all name the progress socket path" —
  holds. `unlink` occurs exactly three times: :1485, :1497, :1721 — all inside `scrub_start`, all on `sock_path`
  (filled from SCRUB_PROGRESS_SOCKET_PATH :1461-1462), the socket, never the record path. Censuses: `remove(`,
  `unlinkat`, `truncate`, `ftruncate`, `util_TRUNC` — 0 hits each.
- S6 "So a `_tmp` left behind by a failed write, a failed `rename`, or a writer process killed between the open
  and the rename (for example by SIGKILL; the progress thread itself disables cancellation from before the open
  until after the rename) is opened again by the next update" — holds. All three leave-behind cases close the fd
  or die (flock released); the next `scrub_write_progress` re-opens the same deterministic `_tmp` path with
  O_CREAT and no O_TRUNC (:483/:517), i.e. opens the leftover in place. Cancel-state parenthetical verified:
  `pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, &old)` at :905 precedes the open (:917), and the re-enable at
  :941 comes after the rename (:925) — in every branch (error paths reach :941 too).
- S7 "if that update's write and rename succeed and the new record is shorter, the old file's bytes past the new
  end stay in place and are renamed into the record with it [inference from the open flags; reproduced in a scratch
  harness compiled from the pinned write path, round-43 wave-1 seat C2ExecTailRepro; not observed on this host]" —
  holds as the tagged inference it is. It follows from S2+S3+S4 (open without O_TRUNC at offset 0, no
  ftruncate anywhere, rename publishes whatever bytes the file then holds) and is labelled `[inference]`, with the
  reproduction named; not observed on this host (no record directory).

**Host reading.** "Not observable on this host: there is no record directory (`var_lib_btrfs absent`,
capture.txt:7)." — holds. capture.txt:7 is exactly `var_lib_btrfs absent`; capture digest matches S241 (section 1).

## 4. Wave-1 attacks vs. the integrated text

The wave-1 falsifier (w1/C2DraftCritSR1.md) found F1 ("killed writer" overreach), F2 (umask), F3 (record-file
scope), F4 (inference conditional on next update succeeding) and F5 (n<1 corner, declared not a defect). The
integrated text at 8acf0b answers F1-F4: F3 → "Every update of the record file" + three call sites; F2 → "open
mode argument 0600, subject to the umask"; F1 → "a writer process killed between the open and the rename (for
example by SIGKILL; the progress thread itself disables cancellation…)" with the cancel-state parenthetical; F4 →
"if that update's write and rename succeed". F5 is unreachable in practice (call sites pass num_devices ≥ 1) and
is not a sentence in the row. I judged the text as it stands: no remaining false or overreaching sentence.

## 5. Frozen counter state

`python3 tools/check-scrub-record-r43.py --revision 8acf0b022586a0f3164c77659fb96ba5f90949b6 --lane
…/tsukuroi-shokunin` (run as a script, writes nothing; exit 1): SR1 has `quote_ok: true` (9 good, 0 bad, 9/9
in window), `prop_ok: true`, `host_ok: true`; global `host_ok: 3`, `novelty_base_hits: 0`, `capture_ok: true`.
`verdict_ok` is false solely because the w2 C2 seats (including this one) have not yet submitted — expected.

## 6. What I did not do

Read-only seat: no fixture clone, no compile/run of btrfs-progs, no scrub started, no btrfs ioctl issued
(including the read-only capture probe), no host mutation, no tools installed. Every claim above is a direct read
of the pinned files at the frozen revision; the quote table and censuses are programmatic scans of S237.
