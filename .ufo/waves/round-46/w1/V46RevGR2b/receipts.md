# Receipts for seat V46RevGR2b (round 46 w1, item C2-GR2-b), 2026-10-27

## 1. Section hash (counter run)

Command: `python3 tools/check-scrub-admission-r46.py --revision a44770491eb5ca15ce9f8b3207309d1af683ffaf --section-hash` (cwd = lane root)

```json
{"entry": "corpus/knowledge/btrfs-scrub-grounding-r45.md", "revision": "a44770491eb5ca15ce9f8b3207309d1af683ffaf", "section_sha256": {"GR1": "fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8", "GR2": "a963df81745c7770f73406eda78cfdf6c1355e23c65c17d43b16e3ebeff62781", "GR3": "8fa626768b49a98186b5a03fbc348175e5ed73484648b6e68a4277c6907a2800"}}
```

## 2. Snapshot digest checks

`sha256sum -c SHA256SUMS` in .ufo/waves/round-45/frozen/src → vsprintf.c OK, systemd.kill.xml OK, kstrtox.c OK, dev-replace.c OK, cmdline.c OK, exit 0.
`sha256sum -c SHA256SUMS` in .ufo/waves/round-44/frozen/src → sysfs.c OK, scrub.c OK, PKGBUILD OK, btrfs-scrub@.timer OK, btrfs-scrub@.service OK, exit 0.
`sha256sum` .ufo/waves/round-45/frozen/hostcap/capture.txt → f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70 (matches entry header and S249 row).
`sha256sum` .ufo/waves/round-43/frozen/src/ioctl.c → 7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01 (matches S240 raw-bytes digest in corpus/SOURCES.md at the pinned revision); round-43 SHA256SUMS lists `7b3488f2…  ioctl.c`.

## 3. Quote line pins (grep -n on snapshots)

dev-replace.c (round-45): 700 comment; 701/703 start-path call; 1111 and 1144 the only two `btrfs_scrub_cancel(fs_info);` calls (both inside `btrfs_dev_replace_cancel`, begins 1085); 1143 invariant comment; 1171 `btrfs_dev_replace_suspend_for_unmount` (no scrub cancel, flips STARTED→SUSPENDED at 1183-1185); 1235 `if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {` (resume); 1259 continuing message; 1265/1268 continue-path call; 1276 `bool __pure btrfs_dev_replace_is_ongoing`; 1287 its SUSPENDED case.
scrub.c (round-44): 3081 `bool readonly, bool is_dev_replace)`; 3123 -ENODEV; 3127-3133 -EROFS condition/return; 3139 REPLACE_TGT fragment; 3142 -EIO; 3147-3149 refusal condition; 3153 -EINPROGRESS; 3336 `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`.
sysfs.c (round-44): 1288 `str = "device replace\n";`; 2015 `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);`.
ioctl.c (round-43): 3186-3194 = `switch (p->cmd) { / case BTRFS_IOCTL_DEV_REPLACE_CMD_START: / if (sb_rdonly(fs_info->sb)) / return -EROFS; / if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) { / ret = BTRFS_ERROR_DEV_EXCL_RUN_IN_PROGRESS; / } else { / ret = btrfs_dev_replace_by_ioctl(fs_info, p); / btrfs_exclop_finish(fs_info);` — line 3190 is the exclop_start line.

## 4. Live sysfs reproduction (2026-10-27, uid 1000)

`stat -c '%a %U'` on /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/exclusive_operation and …/devinfo/1/replace_target → `444 root` both; `od -c` contents → `n o n e \n` and `0 \n`.

## 5. S240 registration gap (evidence)

corpus/SOURCES.md at the pinned revision, S240 row: declared ranges "fs/btrfs/ioctl.c lines 3066-3075, 3118-3140, 5578-5584" — 3190 outside all three; entry header `source:` line lists S246 S247 S248 S249 S242 S243 S244 S237 (no S240); entry `## Limits` records the S247 range widening but no S240 change.
