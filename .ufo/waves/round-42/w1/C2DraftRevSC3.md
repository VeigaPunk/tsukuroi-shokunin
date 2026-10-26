ROW SC3 FIRST-READ: holds

Seat C2DraftRevSC3, 2026-10-26. Row audited: corpus/knowledge/btrfs-scrub-record-r42.md:61-79 at f50c28d83e1832ecd7eba765caace531f45d6b27 (Statement :63-68, Quotes :70-74, Host reading :76-79). Receipts: .ufo/waves/round-42/w1/C2DraftRevSC3/receipt-0{1,2,3}-*.txt.

## Basis

- Snapshot integrity: `sha256sum -c SHA256SUMS` in .ufo/waves/round-42/frozen/src → `scrub.c: OK`, `CHANGES: OK` (receipt 01).
- Live equality: fetched https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c and .../CHANGES on 2026-10-26 → sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801 and bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22, byte-identical to the snapshot (receipt 01). A shallow clone at the tag's peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b (= FETCH.txt) served for tree-wide greps.
- Every `scrub.c:NNN` below is the pinned snapshot, which equals live v7.1.

## Statement — sentence by sentence

1. "The record is written by the userspace `btrfs scrub start` process, not by the kernel" — holds. The only write-capable open of the record is scrub.c:517 (`O_WRONLY|O_CREAT` in scrub_open_file_w), whose only caller is scrub.c:917 inside scrub_write_progress (scrub.c:897-935; tmp-suffix open 917, rename 925). scrub_write_progress is called at exactly three sites: scrub.c:1503 (pre-fork in cmd_scrub_start), scrub.c:1123 (monitor thread scrub_progress_cycle, an in-process pthread created at scrub.c:1585), scrub.c:1702 (final write after the device loop). The fork at scrub.c:1512-1516 keeps all three inside the start process (one write pre-fork, monitor + final in the forked child). Kernel side, the ioctls only fill userspace memory (scrub.c:965 BTRFS_IOC_SCRUB start; scrub.c:986, 1200 BTRFS_IOC_SCRUB_PROGRESS); a tree-wide grep of the v7.1 clone finds the path `/var/lib/btrfs` only at cmds/scrub.c:67-68 (receipt 03), so no kernel or other-component writer exists.

2. "…it writes an all-zero record when the scrub starts" — holds. scrub.c:1501-1510, comment at :1502. `sp` is zeroed at scrub.c:1402 (`sp = calloc(fi_args.num_devices, sizeof(*sp))`); the setup loop scrub.c:1410-1449 sets only scrub_args/resumed/skip/ioprio/limit, never stats, and on resume the prior record stays in `sp[i].resumed` — copied into `sp[i].stats` only at scrub.c:1549-1553, after the :1503 write. So the pre-fork record has zero progress counters and zero stats for every device. Fine-grain nuance, not a defect: the record still carries each device's devid; "all-zero" refers to the data, exactly as the source's own comment says.

3. "…and progress records while it runs" — holds. Monitor loop: scrub.c:1042-1043 (5 s poll cycle), per-device BTRFS_IOC_SCRUB_PROGRESS via progress_one_dev (scrub.c:1060 → :986) for devices not yet finished, then a record write every cycle (scrub.c:1121-1126).

4. "Recording is switched off, with a warning that ends 'status recording disabled', when the directory `/var/lib/btrfs` cannot be created" — holds, and the directory named is exact. mkdir_p is local to scrub.c:1151-1167 (not common/utils.c; grep receipt 03) and mkdirs every proper prefix of `datafile` = SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status" (scrub.c:67, copied at :1269) — i.e. it creates /var/lib and /var/lib/btrfs and never the last component. Failure → warning scrub.c:1336 + `do_record = false` :1338, then falls through.

5. "…or the first record cannot be written" — holds. scrub.c:1505-1509: warning :1507 + `do_record = false` :1508, then falls through into the fork/device loop.

6. "…the scrub itself still runs" — holds. Both disable sites only clear do_record and continue (next statements scrub.c:1341 and :1512); the device threads and BTRFS_IOC_SCRUB run regardless (spawn scrub.c:1567-1571, ioctl :965). do_record has no other off-switch: it is born true (scrub.c:1250) and the option loop scrub.c:1280-1332 exposes no flag touching it.

7. "Whether a scrub is running is asked from the kernel with the `BTRFS_IOC_SCRUB_PROGRESS` ioctl per device, independent of the file" — holds. is_scrub_running_in_kernel scrub.c:1190-1207: per-device devid (:1199), ioctl (:1200), no file access in the function. Callers: `scrub status` takes in_progress solely from it (scrub.c:1946, applied :1976 per-device and :1985 for the fs summary); `scrub start` uses it to auto-force (:1378). Context, not contradiction: start's duplicate-run refusal is socket-based (scrub.c:1460-1483) and the unfinished-record refusal is file-based (scrub.c:1170-1186 used at :1392) — but the kernel ioctl gates that path at :1378, and neither of those sets the running state.

8. "So a missing record does not prove that no scrub ran: a scrub whose recording was disabled, or one driven by another tool through the ioctl, leaves none." — holds. All three record writers are guarded by do_record (scrub.c:1501, :1121, :1700), so a recording-disabled run updates nothing; and since no code outside cmds/scrub.c references the record path (receipt 03), a scrub driven directly through BTRFS_IOC_SCRUB by another tool leaves no record.

## Quotes — all five verified

grep -n on the snapshot (receipt 03) matches every quote verbatim at exactly the cited lines:
- scrub.c:1502 `/* write all-zero progress file for a start */` — ok
- scrub.c:1336 `warning("cannot create scrub data file, mkdir %s failed: %m, status recording disabled",` — ok
- scrub.c:1507 `warning("failed to write the progress status file: %m, status recording disabled");` — ok
- scrub.c:1121 `if (!spc->do_record)` — ok
- scrub.c:1200 `ret = ioctl(fd, BTRFS_IOC_SCRUB_PROGRESS, &sp.scrub_args);` — ok
CHANGES (S238) carries no SC3 quotes; pinned CHANGES = live, sha verified.

## Host reading — verified

- capture.txt:6 `var_lib_btrfs absent` (capture.sh:11 test) — re-checked live 2026-10-26: absent.
- capture.txt:7 `scrub_timers_listed 0` (capture.sh:12) and capture.txt:8 `scrub_timer_unit_file btrfs-scrub@.timer disabled disabled` (capture.sh:13) — re-checked live: `0` and `btrfs-scrub@.timer disabled disabled`.
- capture.txt:10 `journal_scrub_lines 0` = `journalctl -k -b 0 --no-pager -q --grep 'scrub: (started|finished)' | wc -l` (capture.sh:17). Re-checked live: 0 lines; journalctl exits 1 with empty stderr (grep-style no-match), and systemd 262 is built with +PCRE2, so the 0 is a genuine no-match, not a silently failed query. `-b 0 -k` is exactly the reading's "current boot's kernel log".
- Conclusion of the reading — nothing on this host records a scrub, which is weaker than "no scrub ran" — follows from the row's mechanism: recording lives in /var/lib/btrfs (absent), no timer unit is enabled, and the kernel's own scrub start/stop log lines are absent from this boot; a scrub driven through the ioctl would leave no trace on this host.

## Defects

None. Every sentence of the Statement, every quote (line and text), and every host citation checks out.

## Depth notes (non-defect; for the L1 to weigh before the counted wave-2 reads)

- N1 — resume also writes the all-zero record. scrub.c:1501-1510 executes before the started/resumed print (:1520-1523) and before skip devices restore prior stats (:1549-1553), so `btrfs scrub resume` transiently replaces the interrupted record with zeros; the real numbers return only at the final write (:1700-1706) once the run ends. If precision is wanted: "when the scrub starts (or is resumed)".
- N2 — a third, quieter way a scrub ends up unrecorded. A record-write failure inside the monitor thread exits the thread (scrub.c:1125-1126 `goto out`) without the "status recording disabled" warning and without clearing do_record; scrubbing continues, and only the final write still reports failure ("failed to record the result", :1704-1706, printed only when output is enabled). The Statement does not claim its two disable paths are exhaustive, so this is a note, not a defect.
- N3 — "all-zero" means counters/stats; the record still carries per-device devids (needed for the per-device fold of SC4). Matches the source's own comment at scrub.c:1502.

## Residual risk / what I did not do

- No dynamic exercise: I ran no scrub (host guard forbids `btrfs scrub start/cancel/resume/limit -l`); every mechanism claim above is a source-reading proof at the cited lines, not an observed run.
- Packaging: the host runs Arch's btrfs-progs 7.1-1 (capture.txt:3). I did not diff Arch's package source against pristine v7.1 — the same caveat the row itself records (knowledge file :146-147); a patch to cmds/scrub.c would move line numbers.
- Rows SC1, SC2, SC4, SC5 are out of scope; I read them only for context.
- Tooling: nothing installed or upgraded; used system git, curl, grep, awk, sha256sum only.
