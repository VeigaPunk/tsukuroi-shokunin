ROW GR2 VERDICT: holds
SECTION SHA256: d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f

Seat R49CritGR2c, counted critic, claim C1, row GR2 of
`corpus/knowledge/btrfs-scrub-grounding-r45.md` at `55c07cd3f8bff2e12117c34d57b4c618de74d85c`
(extracted to scratch with `git -C … show 55c07cd3…:corpus/knowledge/btrfs-scrub-grounding-r45.md`;
working tree not used). Receipts: `.ufo/waves/round-49/w1/R49CritGR2c/{digests,quotes,section-hash,lines,registration-gap}.txt`.

## Provenance before reading

`sha256sum -c SHA256SUMS` (receipt `digests.txt`): round-45 src 5/5 OK, round-44 src 5/5 OK, round-43 src 1/1 OK.
File → S-row map, cross-checked against `corpus/SOURCES.md:249,251,252,256` and each `FETCH.txt`:

- S247 = `.ufo/waves/round-45/frozen/src/dev-replace.c`, digest `f07ef0a0…`
- S242 = `.ufo/waves/round-44/frozen/src/scrub.c`, digest `f347931b…`
- S243 = `.ufo/waves/round-44/frozen/src/sysfs.c`, digest `ce146120…`
- S240 = `.ufo/waves/round-43/frozen/src/ioctl.c`, digest `7b3488f2…`
- S249 = `.ufo/waves/round-45/frozen/hostcap/capture.txt`, sha256 `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`, equal to the digest the entry records at line 1.

Section hash: the tool prints GR2 `d4296085…` with `structural_ok 1` and `problems []`. My own recompute
agrees under the convention **lines 56–151 of the entry (the `## GR2` heading through the line before `## GR3`)
joined with LF, no trailing LF**; with a trailing LF the digest is `72d6f2b8…`, so the convention matters and I
state both (receipt `section-hash.txt`).

## Clause-by-clause against the pinned bytes

1. *Replace start path uses the scrub code.* `dev-replace.c:700` comment, then `:701` `btrfs_scrub_dev(fs_info,
   src_device->devid, 0,`, `:702` `btrfs_device_get_total_bytes(src_device)`, `:703`
   `&dev_replace->scrub_progress, false, true);`. The "last two parameters" claim is exact: `scrub.c:3079-3081`
   declares `(… struct btrfs_scrub_progress *progress, bool readonly, bool is_dev_replace)`. Holds.
2. *Continue path.* `dev-replace.c:1265-1268` repeats the call with `dev_replace->srcdev->devid`,
   `committed_cursor_left`, total bytes, `false, true`, inside `btrfs_dev_replace_kthread` (`:1249-1274`). Holds.
3. *Order inside `btrfs_scrub_dev`.* `scrub.c:3094-3095` `btrfs_fs_closing` → `-EAGAIN` is the first error return;
   `:3109` `scrub_setup_ctx` (error returns at `:3110-3111`) and `:3114` `scrub_workers_get` (error `:3115-3116`)
   both precede every device check; the device checks are `:3119-3125` (ENODEV), `:3127-3135` (EROFS),
   `:3137-3144` (EIO); the EINPROGRESS block is `:3146-3155`. The row's "whose errors return first" and "three
   device checks" are right, and the `-EAGAIN`/setup returns are correctly placed before the device checks. Holds.
4. *ENODEV condition.* `scrub.c:3120-3121` `!dev || (test_bit(BTRFS_DEV_STATE_MISSING, &dev->dev_state) &&
   !is_dev_replace)`. The row's "unknown devid, or a missing device on a non-replace call" matches both limbs. Holds.
5. *EROFS condition.* `scrub.c:3127-3128` needs `!is_dev_replace && !readonly && !WRITEABLE`; the row says
   "non-replace, non-readonly". Exact. Holds.
6. *EIO condition.* `scrub.c:3138-3139` `!test_bit(IN_FS_METADATA) || test_bit(REPLACE_TGT)` → `:3142`. The row's
   "outside the filesystem metadata, or the replace's own target device" is both limbs. Holds.
7. *EINPROGRESS and "no scrub is started".* `scrub.c:3147-3149` `dev->scrub_ctx || (!is_dev_replace &&
   btrfs_dev_replace_is_ongoing(&fs_info->dev_replace))` → `:3153` `ret = -EINPROGRESS; goto out;`. `goto out`
   (`:3248-3254`) only releases the workers ref and frees the ctx; `dev->scrub_ctx = sctx` at `:3159` is never
   reached, so no scrub starts. The "any call" half (`dev->scrub_ctx` tested before the `is_dev_replace`
   qualifier) is exactly what the byte says. Holds.
8. *What `btrfs_dev_replace_is_ongoing` requires.* `dev-replace.c:1278-1279` `if (!dev_replace->is_valid) return
   false;`; `:1282-1285` NEVER_STARTED/FINISHED/CANCELED → false; `:1286-1287` STARTED/SUSPENDED fall through to
   `:1300 return true`. The comment `:1288-1297` names the suspend-by-umount, missing-tgtdev remount case and says
   "This does not stop the dev_replace procedure" (`:1295-1296`), which is what the row's "a replace suspended by
   an unmount still counts" cites it for. Holds — the `is_valid` gate the round-48 seats asked for is now present.
9. *Source device carries the context while the copy runs.* `scrub.c:3159` `dev->scrub_ctx = sctx;` is reached only
   after the checks, and the field is cleared at `:3222` in the same function's cleanup, so "while the copy runs"
   is the correct scope. Holds.
10. *Which function each `btrfs_scrub_cancel` call sits in.* `grep -n btrfs_scrub_cancel dev-replace.c` returns
    exactly two hits, `:1111` and `:1144`; function heads put both inside `btrfs_dev_replace_cancel`
    (`:1085-1168`): `:1107-1125` is the STARTED case, `:1126-1145` the SUSPENDED case. `:1144` is at the end of
    that same case block, so the cited range `1126-1144` does not run into the next function. `btrfs_dev_replace_suspend_for_unmount`
    is `:1171-1195` and contains no cancel call. Holds.
11. *The "not running" remark.* `dev-replace.c:1127-1129` ("Scrub doing the replace isn't running so we need to do
    the cleanup step … here") and the comment at `:1143-1144` say it, and `btrfs_scrub_cancel` returns `-ENOTCONN`
    when `scrubs_running` is 0 (`scrub.c:3280-3283`), which is consistent with a suspended replace. The row
    reports the code's own words rather than asserting a kernel opinion of its own. Holds.
12. *Progress query.* `scrub.c:3321-3336`: `dev` looked up (`:3329`), `sctx = dev->scrub_ctx` (`:3331`), and
    `:3336 return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`. So a found devid with no context is `-ENOTCONN`, an
    unknown devid `-ENODEV`. `:3222` is the detach site that creates the "no context" state. Holds.
13. *Unmount suspend path: extent and effects.* `dev-replace.c:1171-1195` is exactly
    `btrfs_dev_replace_suspend_for_unmount` (opens `:1171`, closes `:1195`); the switch `:1178-1191` changes state
    only in the STARTED case (`:1184-1190`): state → SUSPENDED (`:1185-1186`), `time_stopped` (`:1187`),
    `item_needs_writeback = 1` (`:1188`), plus an `btrfs_info` line (`:1189`); every other state `break`s
    (`:1179-1183`); no `btrfs_scrub_cancel`. The row's "only moves a STARTED replace to SUSPENDED, with
    `time_stopped` and a writeback flag … and does not call `btrfs_scrub_cancel`" is exact, and the range ends at
    the function's closing brace, not in the next function. Holds.
14. *Host reading.* `capture.txt` is 9 lines: `:1` `captured 2026-10-27T02:09:52Z uid=1000
    CapEff=0000000000000000`, `:9` `devinfo 1d02a454-…/devinfo devids=1`; `grep -c 'exclusive_operation\|replace_target'`
    is 0, so "which this capture does not record" is true. The `CAP_SYS_ADMIN` gate and `-EPERM` are at
    `ioctl.c:3132`/`:3133` inside `btrfs_ioctl_scrub_progress` (`:3126`). `sysfs.c:1287-1288` maps
    `BTRFS_EXCLOP_DEV_REPLACE` to `device replace`; the exclop is taken on the resume path at
    `dev-replace.c:1235` and around the start at `ioctl.c:3190` (`:3190-3194`); `sysfs.c:2015` is the
    `REPLACE_TGT` bit behind `replace_target` (`:2019`), and the bit is set on the target at
    `dev-replace.c:209-210`/`:309` and cleared at `:970`. I also re-read the two live attributes as uid 1000
    (receipt `lines.txt`): both `-r--r--r--`, values `none` and `0`, matching what `a2w1/C2ExecHostRecheck.md`
    §3 (lines 84-89) reported. Holds.

## Quotes

29 `**Quote.**` rows parsed from the row and compared against the cited line of the cited snapshot: **29 exact,
0 mismatches** (receipt `quotes.txt`). Two are display-stripped in the entry-wide convention — `dev-replace.c:1128`
drops the ` * ` comment leader and `:1259` shows the literal's own opening quote — and neither changes a byte of the
quoted text. The `[inference]` bracket at the end of the statement covers the only consequence the pinned bytes do
not decide (btrfs-progs printing), so no unmarked inference is present.

## Findings (reported, not applied — I do not edit lane content)

**F1 — the Limits paragraph's registration accounting is stale against the frozen row's own citations.**
`corpus/SOURCES.md` at the freeze declares S247 as `700-703, 1143-1144, 1235, 1256-1268, 1276-1300`
(`SOURCES.md:256`), S242 as `1365-1385, 3140-3162, 3215-3226, 3321-3337` (`:251`), S243 as
`72-74, 2021-2049, 2113` (`:252`), S240 as `3066-3075, 3118-3140, 5578-5584` (`:249`). Computed membership
(receipt `registration-gap.txt`), quoted lines outside their row's declared ranges are: `scrub.c:3081, 3094, 3095,
3109, 3114, 3123, 3133, 3138, 3139`; `sysfs.c:1288, 2015`; `dev-replace.c:1128`. Cited-only lines outside them:
`ioctl.c:3190`; `dev-replace.c:1111, 1126-1142, 1171-1195`. The row's Limits sentence (entry lines 223-227)
discloses four of the S242 lines (`3081, 3123, 3133, 3139`) and both S243 lines, but not the six S242 lines the
round-47 amendment added, not `dev-replace.c:1128` (quoted), not the cancel/suspend ranges `1111`/`1126-1142`/
`1171-1195`, and not `ioctl.c:3190`; it also says S247's ranges "were widened to the quoted lines (1143-1144,
1235, 1276-1300)", which was true of the round-45 quote set (at `194a452` the entry had no `1128` quote: grep
count 0) and no longer covers the frozen set. Every sentence in Limits is literally true as written
(the ranges named really do omit the lines named) — it is a non-exhaustive disclosure, not a false claim — and
the bytes themselves are not in doubt because the snapshot digests cover whole files (`a2w1/C2ExecQuotes.md:37-38`),
so this does not move the verdict. It does need the one-line amendment below, since an unregistered quoted line is
exactly the F1/F2 class that seat raised.

Exact replacement (entry lines 223-225, first two sentences):
- old: "The S247 row's declared ranges were widened to the quoted lines (1143-1144, 1235, 1276-1300). Three
  registrations of older rows stay as they are: S242's declared ranges (1365-1385, 3140-3162, 3215-3226,
  3321-3337) do not list scrub.c:3081, 3123, 3133 or 3139; S243's (72-74, 2021-2049, 2113) do not list
  sysfs.c:1288 or 2015; S237's do not list scrub.c:421."
- new: "The S247 row's declared ranges were widened to the quoted lines (1143-1144, 1235, 1276-1300) and still do
  not list dev-replace.c:1111, 1126-1142 (quoted at 1128) or 1171-1195. Four registrations of older rows stay as
  they are: S242's declared ranges (1365-1385, 3140-3162, 3215-3226, 3321-3337) do not list scrub.c:3081,
  3094-3095, 3109, 3114, 3123, 3133 or 3138-3139; S243's (72-74, 2021-2049, 2113) do not list sysfs.c:1288 or
  2015; S240's (3066-3075, 3118-3140, 5578-5584) do not list ioctl.c:3190; S237's do not list scrub.c:421."

**F2 — wording, not wrong.** "When the replace context is absent" names the field the code tests, `dev->scrub_ctx`
(`scrub.c:3331-3336`), which a plain scrub also sets, so the phrase invites a false reading ("no replace running →
ENOTCONN"). The citations force the intended reading, and three earlier seats read it the same way as a nit
(`round-48/w2/R48CritGR2b.md:17`; this wave's `R49RevGR2a.md:103-104`, `R49RevGR2c.md:63`). Exact optional
tightening:
- old: "When the replace context is absent, the progress query returns `-ENOTCONN` for a devid that exists
  (`scrub.c:3222, :3336`); an unknown devid gives `-ENODEV` (`scrub.c:3336`)."
- new: "When the device's scrub context is absent, the progress query returns `-ENOTCONN` for a devid that exists
  (`scrub.c:3336`; the context is cleared at `:3222` when a scrub ends); an unknown devid gives `-ENODEV`
  (`scrub.c:3336`)."

**F3 — the inference bracket under-claims.** It says the ioctl side "is not pinned here", but S240 is pinned and
`ioctl.c:3093-3115` decides the scrub-start ioctl's return: `ret = btrfs_scrub_dev(…)` is returned unchanged at
`:3115`, replaced by `-EFAULT` only if the args copy fails (`:3109-3110`). Optional:
- new: "[inference for the btrfs-progs side only: how `btrfs scrub start` and `btrfs scrub status` print these
  returns is not pinned here; the scrub-start ioctl's own return is pinned at `S240` ioctl.c:3093-3115, where
  `btrfs_scrub_dev`'s `ret` is returned unless the args copy fails, then `-EFAULT` (`:3109-3110`)]."

None of F1-F3 contradicts a Statement clause or a Quote, so the verdict stands at `holds`; F1 is the one I would
fix in the same integration, because it is the only one that leaves a quoted line undisclosed.

## Verified but not re-derived

The snapshot digests were checked against each `SHA256SUMS`, but the SHA256SUMS→upstream binding rests on the
`FETCH.txt` files (round-43, round-44 read) and on `SOURCES.md`'s "reopened live 2026-10-28, byte-identical"
note for S240; I did not re-fetch any file live, so I did not independently re-derive that these bytes are the
v7.2.11 bytes. The host's `CapEff=0` is the capture's word only (I did re-read the two sysfs attributes live, but
not the capability set). I did not re-read S237 (round-42 `scrub.c`), any GR1/GR3 byte, or the btrfs-progs side.
The row's arithmetic consequences for scrub exit codes are not touched here.

## What I did not do

No counter run: I used `tools/check-scrub-admission-r49.py` only in its read-only `--section-hash` mode; I did not
run `--revision <REV>` in full, any selftest, or the census. No network. No git or jj mutation anywhere; no
write outside this report and the receipt directory `R49CritGR2c/`; I did not edit the entry or `SOURCES.md`.
