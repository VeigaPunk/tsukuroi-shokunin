# C2DraftRevSR1 receipts — SR1 source verification (pinned snapshot, read-only)

```
$ (cd .ufo/waves/round-43/../round-42/frozen/src && sha256sum -c SHA256SUMS)
scrub.c: OK
CHANGES: OK

$ sha256sum .ufo/waves/round-42/frozen/src/scrub.c
48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801  .ufo/waves/round-42/frozen/src/scrub.c
$ sha256sum .ufo/waves/round-43/frozen/hostcap/capture.txt
f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556  .ufo/waves/round-43/frozen/hostcap/capture.txt

Quote verbatim check (SR1): quoted string `in` named line, python substring test
  scrub.c:483 OK  | fd = open(datafile, m, 0600);
  scrub.c:487 OK  | ret = flock(fd, LOCK_EX|LOCK_NB);
  scrub.c:517 OK  | return scrub_open_file(datafile, O_WRONLY|O_CREAT);
  scrub.c:534 OK  | ret = rename(datafile_old, datafile_new);
  scrub.c:917 OK  | fd = scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp");
  scrub.c:922 OK  | err = scrub_write_file(fd, fsid, data, n);
  scrub.c:925 OK  | err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");
  scrub.c:1485 OK  | ret = unlink(sock_path);
  -> 8/8 quotes verbatim at their named lines

unlink census in scrub.c (all occurrences):
  :1485  ret = unlink(sock_path);
  :1497  unlink(sock_path);
  :1721  unlink(sock_path);
  -> 3 occurrences
ftruncate/truncate/lseek/pwrite/unlinkat/remove census: no matches
O_TRUNC census: no matches
open( call sites: [(483, 'fd = open(datafile, m, 0600);')]

call sites of scrub_write_file( (excluding definitions):
  :922  err = scrub_write_file(fd, fsid, data, n);
  :1112  ret = scrub_write_file(
call sites of scrub_write_progress( (excluding definitions):
  :1123  ret = scrub_write_progress(spc->write_mutex, fsid,
  :1503  ret = scrub_write_progress(&spc_write_mutex, fsid, sp,
  :1702  ret = scrub_write_progress(&spc_write_mutex, fsid, sp,
call sites of scrub_rename_file( (excluding definitions):
  :925  err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");
call sites of scrub_open_file_w( (excluding definitions):
  :917  fd = scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp");

capture.txt lines 1-10:
  1: captured_utc 2026-10-26T21:51:26Z
  2: uid 1000 euid_caps 0000000000000000
  3: kernel 7.2.11-arch1-1
  4: btrfs_progs btrfs-progs 7.1-1
  5: root_fs btrfs 1d02a454-c549-4a35-b567-89d60902af8e
  6: scrub_progress_ioctl devid=1 errno=EPERM (1)
  7: var_lib_btrfs absent
  8: scrub_status_exit 0
  9: scrub_status| UUID:             1d02a454-c549-4a35-b567-89d60902af8e
  10: scrub_status| 	no stats available
```
