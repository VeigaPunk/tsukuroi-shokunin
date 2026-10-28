ROW GR2 VERDICT: partly
SECTION SHA256: a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f

Snapshot binding (verified, not assumed). `sha256sum -c SHA256SUMS` returned OK for every file in the three
snapshot directories, and the digests match the entry's `source:` line: S247 = `.ufo/waves/round-45/frozen/src/
dev-replace.c` (f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a), S242 = `.ufo/waves/round-44/
frozen/src/scrub.c` (f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8), S243 = `.ufo/waves/
round-44/frozen/src/sysfs.c` (ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43), S240 =
`.ufo/waves/round-43/frozen/src/ioctl.c` (7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01),
and S249 = `.ufo/waves/round-45/frozen/hostcap/capture.txt` (f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea
38947c3991e70). Hash: `check-scrub-admission-r50.py --revision 8029cdba… --section-hash` printed the frozen
GR2 value, and I reproduced it independently as sha256 of entry lines 56-152 (`## GR2` through the blank line
before `## GR3`) LF-joined; same 64 hex digits.

Clauses checked against the bytes, all resolving:
- Both scrub entry points: dev-replace.c:700 comment, dev-replace.c:701-703 call with `false, true`;
  dev-replace.c:1265-1268 continue path on `dev_replace->srcdev->devid`, again `false, true`; signature
  scrub.c:3079-3081 has those as the last two parameters.
- `-EAGAIN` first: scrub.c:3094-3095 is the first `return` in `btrfs_scrub_dev` (only `progress->last_physical`
  precedes it).
- Context/workers before the device checks: scrub.c:3109-3111 (`PTR_ERR(sctx)`), scrub.c:3114-3116
  (`goto out_free_ctx`).
- `-ENODEV`: scrub.c:3120-3124, `!dev || (MISSING && !is_dev_replace)` — "unknown devid, or a missing device on
  a non-replace call" is exact.
- `-EROFS`: scrub.c:3127-3135, `!is_dev_replace && !readonly && !WRITEABLE`.
- `-EIO`: scrub.c:3138-3144, `!IN_FS_METADATA || REPLACE_TGT` — "outside the filesystem metadata, or the
  replace's own target device" is exact.
- `-EINPROGRESS` last: scrub.c:3147-3155, `dev->scrub_ctx || (!is_dev_replace && is_ongoing)`; the row's "only
  after those checks" and its both-branch wording hold. `is_ongoing`: dev-replace.c:1276-1300 — `is_valid`
  gate at :1278-1279, STARTED/SUSPENDED at :1286-1287, unmount comment at :1288-1297.
- Context attached at scrub.c:3159; cancel on STARTED at dev-replace.c:1111 inside
  `btrfs_dev_replace_cancel` (signature :1085); suspended branch dev-replace.c:1126-1144 with the
  `* ` comment at :1128-1129 and `btrfs_scrub_cancel` at :1144 — the row reports the code's own tension
  instead of smoothing it.
- Progress query: scrub.c:3321-3337, return at :3336 (`dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV`), context
  cleared at scrub.c:3222. The `-ENOTCONN`/`-ENODEV` split is exact.
- Unmount suspend: dev-replace.c:1171-1195 — only the STARTED case moves (:1184-1188), no `btrfs_scrub_cancel`
  in the function. "only … and does not call" holds.
- `[inference]` mark: ioctl.c:3093-3095 makes the call, ioctl.c:3109-3110 overrides with `-EFAULT`, ioctl.c:3115
  returns `ret`. The mark now scopes only to btrfs-progs printing, and the ioctl pass-through is stated as
  pinned. Accurate for any call that reaches `btrfs_scrub_dev`; the pre-call guards (ioctl.c:3081-3082,
  3084-3085, 3088-3090) sit outside the sentence's subject, so I do not count them as a defect.
- Host reading: capture.txt:9 (`devids=1`), capture.txt:1 (`CapEff=0000000000000000`), ioctl.c:3126-3133
  (`CAP_SYS_ADMIN` → `-EPERM`), sysfs.c:1288 under `BTRFS_ATTR(, exclusive_operation, …)` at :1302, and
  sysfs.c:2015 under `BTRFS_ATTR(devid, replace_target, …)` at :2019. The cited seat read is real:
  `.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md` §3 shows both files `-r--r--r--` and reading `0` / `none`.

The four round-50 corrections are in the bytes: the mark narrowed (verified above); S240 named in the
`source:` line (entry line 1, with snapshot path, digest and cited lines) and in QUALITY item 7 (line 261);
dev-replace.c:1128 carries its `* ` prefix and matches the line verbatim; the S247/S240 gaps are declared
(entry lines 229-235) and match the registrations in `corpus/SOURCES.md` S247 (700-703, 1143-1144, 1235,
1256-1268, 1276-1300) and S240 (3066-3075, 3118-3140, 5578-5584).

DEFECT (1, blocking; same class as the round-49 defect 4 that was fixed for S247/S240). The S242 registration
gap disclosure is incomplete. S242 registers only 1365-1385, 3140-3162, 3215-3226, 3321-3337, so GR2's cites
at `scrub.c:3094`, `:3095`, `:3109`, `:3114` and `:3138` fall outside every registered range; entry lines
225-227 name only `scrub.c:3081`, 3123, 3133, 3139. The bytes stay whole-file digest-pinned, so no clause is
unsupported, but a reader following the row's own provenance trail cannot place five of its citations.
Exact replacement for the middle clause of entry lines 225-227:
"S242's declared ranges (1365-1385, 3140-3162, 3215-3226, 3321-3337) do not list `scrub.c:3081`, 3094-3095,
3109, 3114, 3123, 3133 or 3138-3139;"

Verified but not re-derived: the whole-snapshot digest coverage (`sha256sum -c` run here); the "re-fetched
byte-identical on 2026-10-28" claim for S240 (no network fetch from this seat); the host sysfs read (the seat
report was read, the host was not re-probed); btrfs-progs printing (not pinned anywhere). Not done: no upstream
re-fetch, no host sysfs probe, no run of the full C1 counter beyond `--section-hash`, no btrfs-progs source.

Impacted axes: C1 depth (the row cannot bind `holds` while the disclosure defect stands), provenance trail.
No mechanistic clause is contradicted, so partly, not fails. Scratch removed after the receipts were written.
