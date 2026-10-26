ROW SR1 VERDICT: holds

Seat C2RevSR1 (reviewer), tsukuroi lane round 43 wave w2, item V-SR1-R. Row SR1 of corpus/knowledge/btrfs-scrub-record-r43.md at 8acf0b022586a0f3164c77659fb96ba5f90949b6 (record lines 17-50; `## SR1` = line 17, `## SR3` = line 51).

Pins (all verified):
- sha256sum .ufo/waves/round-42/frozen/src/scrub.c = 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801 ✓
- `cd .ufo/waves/round-43/frozen/src && sha256sum -c SHA256SUMS` → ioctl.c: OK ✓
- sha256sum .ufo/waves/round-43/frozen/hostcap/capture.txt = f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556 ✓

Quotes — all nine verbatim on their named S237 scrub.c lines (asserted by awk: 483 OK, 487 OK, 517 OK, 534 OK, 905 OK, 917 OK, 922 OK, 925 OK, 1485 OK):
- 517: `return scrub_open_file(datafile, O_WRONLY|O_CREAT);` ✓
- 483: `fd = open(datafile, m, 0600);` ✓
- 487: `ret = flock(fd, LOCK_EX|LOCK_NB);` ✓
- 905: `ret = pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, &old);` ✓
- 917: `fd = scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp");` ✓
- 922: `err = scrub_write_file(fd, fsid, data, n);` ✓
- 925: `err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");` ✓
- 534: `ret = rename(datafile_old, datafile_new);` ✓
- 1485: `ret = unlink(sock_path);` ✓

Statement, per sentence (lines checked):
1. "Every update of the record file goes through scrub_write_progress (its three call sites write the first record, the progress thread's records and the final record)" — grep shows exactly three scrub_write_progress calls: 1123 (progress-thread loop), 1503 (start: "write all-zero progress file for a start"), 1702 (after pthread_join(t_prog), final result). The record file (SCRUB_DATA_FILE /var/lib/btrfs/scrub.status, define 67) is written only via scrub_open_file_w (917) + scrub_rename_file (925) inside scrub_write_progress; the only other opens are read-only scrub_open_file_r at 1361 and 1930. Supported.
2. "it opens scrubub.<fsid>_tmp with O_WRONLY|O_CREAT and no O_TRUNC (open mode argument 0600, subject to the umask; then a non-blocking flock LOCK_EX)" — 517 passes O_WRONLY|O_CREAT to scrub_open_file; 483 open(datafile, m, 0600) with no O_TRUNC; 487 flock(fd, LOCK_EX|LOCK_NB) after open. Supported.
3. "writes the whole record from the start of that file" — scrub_write_file (848-895) writes the version prefix then all per-device kv rows via write() on the freshly opened fd (offset 0) and returns -EOVERFLOW on any write failure. Supported.
4. "and renames _tmp over scrubub.<fsid> only when the write returned no error; a failed write skips the rename" — 922-927: err = scrub_write_file; `if (err) goto out1;` before scrub_rename_file. Supported.
5. "No code in scrub.c removes a _tmp file: its three unlink calls all name the progress socket path." — grep: unlink only at 1485, 1497, 1721 — all `unlink(sock_path)` (sock_path guarded by `if (sock_path[0])` at 1496/1720); no remove()/truncate() anywhere in scrub.c. Supported.
6. "So a _tmp left behind by a failed write, a failed rename, or a writer process killed between the open and the rename (for example by SIGKILL; the progress thread itself disables cancellation from before the open until after the rename) is opened again by the next update" — failed write: 923-924 goto out1 before rename; failed rename: 926-927 goto out1; both leave `_tmp`. Next update reopens the same path with O_CREAT and no O_TRUNC (483/517). Cancellation disabled at 905 (before mutex lock and open at 917) and re-enabled at 941 (after close at 931 and rename at 925), so deferred cancellation cannot interrupt between open and rename; SIGKILL can (no cleanup path exists). Supported.
7. "if that update's write and rename succeed and the new record is shorter, the old file's bytes past the new end stay in place and are renamed into the record with it [inference ...]" — labelled [inference] with provenance (scratch harness, wave-1 seat C2ExecTailRepro; not observed on this host). It is a reasonable reading of the pinned lines: no O_TRUNC, no truncate()/remove(), write from offset 0 (483, 517, 848-895, 534). Allowed inference.

Host reading. "Not observable on this host: there is no record directory (`var_lib_btrfs absent`, capture.txt:7)." — capture.txt line 7 is verbatim `var_lib_btrfs absent`; SCRUB_DATA_FILE is /var/lib/btrfs/scrub.status (define 67), so the record directory is absent on this host. Supported.

Findings: none. No sentence contradicted (not fails); no unmarked sentence exceeds the lines (not partly).

What was not done: no host mutation, no lane edits, no counters run (this seat only judges the row against pinned lines); the wave-1 harness reproduction was not re-run.
