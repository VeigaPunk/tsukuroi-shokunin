# C2CritSR1 receipts (round 43, wave w2)

All commands run on 2026-10-26 in `/fast/scratch/hyaku/tsukuroi-r43/C2CritSR1` (scratch), read-only.

## 1. Pins

```
$ sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c
48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801  .../scrub.c

$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/frozen/src && sha256sum -c SHA256SUMS
ioctl.c: OK

$ sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/frozen/hostcap/capture.txt
f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556  .../capture.txt
```

## 2. Quote fidelity (programmatic; 9/9 OK)

```
  483 OK | fd = open(datafile, m, 0600);
  487 OK | ret = flock(fd, LOCK_EX|LOCK_NB);
  517 OK | return scrub_open_file(datafile, O_WRONLY|O_CREAT);
  534 OK | ret = rename(datafile_old, datafile_new);
  905 OK | ret = pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, &old);
  917 OK | fd = scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp");
  922 OK | err = scrub_write_file(fd, fsid, data, n);
  925 OK | err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");
 1485 OK | ret = unlink(sock_path);
quotes_ok 9 / 9
```

## 3. Censuses (whole S237 file)

```
census 'unlink': 3 hits -> [1485, 1497, 1721]
census 'O_TRUNC': 0 hits -> []
census 'ftruncate': 0 hits -> []
census 'truncate': 0 hits -> []
census 'remove(': 0 hits -> []
census 'unlinkat': 0 hits -> []
census 'lseek': 0 hits -> []
census 'pwrite': 0 hits -> []
```

## 4. Call sites and cancel-state anchors (read of S237)

- `scrub_write_progress` call sites: :1123 (progress thread), :1503 (initial), :1702 (final).
- `scrub_open_file_w` sole call site: :917; `scrub_write_file` call sites: :922 (record), :1112 (socket peer).
- Cancel-state: disable :905 (before open :917), enable :941 (after rename :925).

## 5. Frozen counter (run as script, writes nothing)

```
$ cd /fast/scratch/hyaku/tsukuroi-r43/C2CritSR1 && python3 \
  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-record-r43.py \
  --revision 8acf0b022586a0f3164c77659fb96ba5f90949b6 \
  --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
{"base": "6951ead90566b2d74f7c45b4efca29246badad64", "capture_ok": true, ...,
 "per_row": {"SR1": {"host_ok": true, "present": true, "prop_ok": true, "quote_ok": true,
   "quotes": {"bad": 0, "files": ["scrub.c"], "good": 9, "in_window": 9},
   "verdict_ok": false, "verdicts": {"crit": null, "residual": null, "rev": null}}, ...},
 "host_ok": 3, "novelty_base_hits": 0, ...}
exit=1
```

(`verdict_ok: false` because the w2 C2 seats have not submitted yet; all other SR1 conjuncts hold.)
