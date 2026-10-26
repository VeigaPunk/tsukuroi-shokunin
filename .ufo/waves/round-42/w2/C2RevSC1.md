ROW SC1 VERDICT: holds

Seat C2RevSC1, item V-1a (counted verdict), 2026-10-26. Reviewer did not author the row.

## Scope and method

- Row SC1 read from the integrated text at the pinned commit: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 78abb8b5cdc9da511b4fc523e661517a68dd33d3:corpus/knowledge/btrfs-scrub-record-r42.md` (168 lines; verified the commit resolves: `git rev-parse` → `78abb8b5cdc9da511b4fc523e661517a68dd33d3`). No `Corrections` section exists in the file at this commit; SC1's section carries no appended corrections, so the integrated text is the text reviewed.
- Pinned snapshots verified before reading: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-42/frozen/src` → `scrub.c: OK`, `CHANGES: OK`. Host capture digest re-computed: `942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c  capture.txt`, equal to the digest declared in the record's source line. All paths below are relative to that `frozen/` directory unless absolute.
- Every SC1 sentence checked against `src/scrub.c` (v7.1) and `hostcap/capture.txt`. All six Quote lines checked by literal `grep -n` for the quoted string at the cited line number.

## Quote-line verification (all six pass)

`grep -n` with the exact quoted string, pinned `src/scrub.c`:

| Cited | Quote | Observed |
|---|---|---|
| scrub.c:67 | `#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` | line 67, exact |
| scrub.c:459 | `datafile[ret] = '.';` | line 459, exact |
| scrub.c:467 | `datafile[ret] = '_';` | line 467, exact |
| scrub.c:483 | `fd = open(datafile, m, 0600);` | line 483, exact |
| scrub.c:487 | `ret = flock(fd, LOCK_EX\|LOCK_NB);` | line 487, exact |
| scrub.c:534 | `ret = rename(datafile_old, datafile_new);` | line 534, exact |

## Statement, sentence by sentence

S1. "The record for one filesystem is the file `/var/lib/btrfs/scrub.status.<fsid>` (the base path plus a dot plus the filesystem UUID; the name pattern is already held, SH4)." — **True.** Base define at scrub.c:67; `scrub_datafile` (scrub.c:446-475) copies the base (454), writes the dot at 459, appends `fn_local` at 460; every caller passes the unparsed UUID: `uuid_unparse(fi_args.fsid, fsid)` at scrub.c:1360 then `scrub_open_file_r(SCRUB_DATA_FILE, fsid)` at 1361 (also 917/925 writer side, 1915/1930 status side), giving `/var/lib/btrfs/scrub.status.<fsid>`. Cross-reference accurate: `corpus/knowledge/storage-health-r26.md:57` at the pinned commit says "btrfs-progs keeps scrub.status.<UUID> files".

S2. "Every update is written to a sibling file `scrub.status.<fsid>_tmp` and then moved over the record with `rename`, so a reader sees either the old or the new record, never a half-written one." — **True.** The single record-write function `scrub_write_progress` (scrub.c:897-944) opens the sibling `scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp")` (917; `scrub_datafile` appends `'_'` at 467 then `"tmp"` at 468 → `scrub.status.<fsid>_tmp`), writes the content (922), then `scrub_rename_file` (925) → `rename(datafile_old, datafile_new)` (534). All three record-write events route through it: initial all-zero at start (1503), periodic progress in the recorder thread (1123), final result (1702). Falsification attempt: the only other `scrub_write_file` call (scrub.c:1112) writes to `peer_fd`, the progress **socket** connection, not the record — no bypass found. Readers open only the fixed record path (`scrub_open_file_r`: 1361, 1930; the sole `open()` of a scrub datafile in the file is 483), so rename(2) atomicity gives old-or-new, never torn; a pre-first-record reader gets ENOENT and is treated as no history (1931-1935), which is "no record", not a half-written one.

S3. "A record or `_tmp` file the CLI creates gets mode 0600 (the `open` mode argument, subject to the umask), and every open of either, for reading or writing, must take a non-blocking exclusive `flock` (`LOCK_EX`), so a second writer or a reader that finds the lock held fails at once instead of waiting." — **True.** `open(datafile, m, 0600)` at 483 is the only open; the writer's flags are `O_WRONLY|O_CREAT` (517), so the created `_tmp` gets 0600 masked by the umask (open(2) semantics), and the record inherits that mode via the rename (534); reader flags are `O_RDONLY` (505, mode arg inert). No `chmod`/`fchmod`/`umask` call exists anywhere in scrub.c (grep: 0 matches), so nothing alters the 0600 derivation. Every open of either file funnels through `scrub_open_file` (478-492): `flock(fd, LOCK_EX|LOCK_NB)` at 487 unconditional after a successful open; on lock failure it closes and returns `-errno` immediately (488-491) — LOCK_NB, no retry, no wait. Callers propagate the failure without retrying: readers warn and bail (1364, and 1933 with `err = 1`), writer failure disables recording at start (1507) or ends the thread / reports at final write (1123-1126, 1706). The lock is held by whichever process owns the file it opened, so a second writer (on `_tmp`) and a reader (on the record — including one racing the rename, since the renamed inode keeps the writer's lock until close at 928-930) each fail at once.

S4. "(The progress socket `/var/lib/btrfs/scrub.progress.<fsid>` is a different file, created by `bind`, not covered here.)" — **True.** `SCRUB_PROGRESS_SOCKET_PATH "/var/lib/btrfs/scrub.progress"` (scrub.c:68); `scrub_datafile(SCRUB_PROGRESS_SOCKET_PATH, fsid, NULL, ...)` (1461-1463) builds `/var/lib/btrfs/scrub.progress.<fsid>`; created by `bind(prg_fd, ...)` (1466), an AF_UNIX socket, not by the record's open/rename path. SC1 indeed covers it no further.

## Host reading

"No record exists: `/var/lib/btrfs` is absent (capture.txt:6) for the root filesystem `1d02a454-c549-4a35-b567-89d60902af8e` (capture.txt:5)." — **True.** `hostcap/capture.txt:5` = `root_fsid 1d02a454-c549-4a35-b567-89d60902af8e`; `:6` = `var_lib_btrfs absent`. The capture producer `hostcap/capture.sh:11` emits "absent" when `-e /var/lib/btrfs` is false, i.e. no file of any type at that path, so no `scrub.status.<fsid>` record can exist for that fsid on this host. Capture digest matches the declared pin (above).

## Overreach check

No sentence claims more than its cited mechanism. Two adjacent facts the row does not claim, recorded as observations (neither falsifies a sentence):
- The `_tmp` file is opened `O_WRONLY|O_CREAT` **without** `O_TRUNC` (scrub.c:517) and scrub.c contains no `ftruncate`; a stale `_tmp` left by a crashed run could lend trailing stale bytes to a later renamed record. Visibility remains atomic old-or-new — the sentence's actual claim — so this is context, not a defect in SC1.
- Writer and reader locks never meet (different inodes: `_tmp` vs record); atomicity comes from rename alone, which is exactly how S2 attributes it.

## Corrections

None required — no sentence is incomplete, overreaching, or false.

## Not done

- `src/CHANGES` was digest-verified only; no SC1 sentence rests on it (S238 is cited by SC5, outside this item).
- No live system call was run against `/var/lib/btrfs` (host guard); the Host reading is judged solely against the pinned capture, which is the item's stated basis.

Receipts: `.ufo/waves/round-42/w2/C2RevSC1/verify.txt` (checksum verifications, quote-line greps, call-site map, capture lines 5-6, capture.sh absence test). Scratch removed after writing.
