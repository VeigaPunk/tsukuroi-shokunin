VERDICT: supports

# C2-1 — live re-fetch of every round-44 frozen source (seat C2ExecLiveSources)

Access timestamp: 2026-10-26 21:12–21:14 local = 2026-10-27T00:12–00:14Z (host clock UTC−3).
Host: Linux 7.2.11-arch1-1 (uname -srm), btrfs-progs 7.1-1.
Scratch: `/fast/scratch/hyaku/tsukuroi-r44/C2ExecLiveSources/` (removed at end; receipts copied first).
No tool was installed or upgraded for this item; no package, unit, service, sysfs or mount state was touched.

Every URL in `FETCH.txt` was re-fetched, every digest matched `SHA256SUMS` byte-for-byte, both tags peel to the
commits recorded in `FETCH.txt`, and the one `[inference]` in SR7 is now **verified at v7.2.11 source**. Two
precision defects were found and are stated with exact replacement text: the second `dev-replace.c` locator is one
line short, and `dev-replace.c` is not pinned at all (undisclosed by the freeze, disclosed by the entry).

## 1. The five frozen files: fresh fetch vs `SHA256SUMS`

Commands (all rc=0; cwd = scratch):

```
curl -sfL 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/scrub.c?h=v7.2.11' -o scrub.c
curl -sfL 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/sysfs.c?h=v7.2.11' -o sysfs.c
curl -sfL 'https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub@.timer' -o btrfs-scrub@.timer
curl -sfL 'https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub@.service' -o btrfs-scrub@.service
curl -sfL 'https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/PKGBUILD' -o PKGBUILD
sha256sum scrub.c sysfs.c btrfs-scrub@.timer btrfs-scrub@.service PKGBUILD
```

| file | `SHA256SUMS` (frozen, `.ufo/waves/round-44/frozen/src/SHA256SUMS:1-5`) | fresh fetch 2026-10-27T00:12Z | match |
|---|---|---|---|
| scrub.c | `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` | `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` | yes |
| sysfs.c | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` | yes |
| btrfs-scrub@.timer | `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad` | `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad` | yes |
| btrfs-scrub@.service | `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252` | `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252` | yes |
| PKGBUILD | `3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98` | `3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98` | yes |

Byte comparison against the frozen tree (`cmp -s`): `IDENTICAL` for all five (`refetch-2026-10-26.txt`).

Independent cross-host re-fetch of the three kernel-side files from the gregkh mirror (different infra and clone):

```
curl -sfL https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/{scrub.c,sysfs.c,dev-replace.c}   # rc=0 each
```
→ `scrub.c.gh` `f347931b…`, `sysfs.c.gh` `ce146120…` — identical to the kernel.org fetch and to `SHA256SUMS`;
`dev-replace.c.gh` `f07ef0a0…` identical to the kernel.org fetch (§3). Arch packaging was re-fetched a second time
**by the peeled commit** (`…/-/raw/0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0/<file>`) and returned the same three
digests, so tag content and commit content agree (`xcheck-2026-10-26.txt`).

## 2. Tag peeling vs `FETCH.txt`

```
git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git 'refs/tags/v7.2.11' 'refs/tags/v7.2.11^{}'
8316c24ec1b77dba19ba072ca4fe251b36dc65d3	refs/tags/v7.2.11
a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea	refs/tags/v7.2.11^{}
git ls-remote https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs.git 'refs/tags/7.1-1' 'refs/tags/7.1-1^{}'
4fd401153bd8eac8ab9e37e6511e1bf2350fdd07	refs/tags/7.1-1
0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0	refs/tags/7.1-1^{}
```

`FETCH.txt:2` "peeled a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea" — match. `FETCH.txt:4` "commit
0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0" — match (that is the peeled commit; the annotated tag object is
`4fd40115…`, so `FETCH.txt` is precise about what it records, only silent about the tag object). The same two
kernel SHAs come back from the independent gregkh mirror (`tags-2026-10-26.txt`), so the tag→content binding is
corroborated on two hosts.

`FETCH.txt:6` "lines 99-101 install both units" — PKGBUILD:99 is the comment `# install scrub service/timer`,
:100 the `.service` install, :101 the `.timer` install. Exact.

## 3. `dev-replace.c` at v7.2.11 — SR7's replace-side inference

```
curl -sfL 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/dev-replace.c?h=v7.2.11' -o dev-replace.c   # rc=0
sha256 f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a   (1322 lines)
```

Signature under test, `scrub.c:3079-3081` (fresh bytes): `int btrfs_scrub_dev(struct btrfs_fs_info *fs_info, u64 devid,
u64 start, u64 end, struct btrfs_scrub_progress *progress, bool readonly, bool is_dev_replace)` — the 7th argument is
the one in question.

Call site 1 — **cited range 701-703 is exact**:

```
699:
700:	/* the disk copy procedure reuses the scrub code */
701:	ret = btrfs_scrub_dev(fs_info, src_device->devid, 0,
702:			      btrfs_device_get_total_bytes(src_device),
703:			      &dev_replace->scrub_progress, false, true);
```

Call site 2 — **the call starts at 1265 and the arguments under test are on 1268**:

```
1265:	ret = btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid,
1266:			      dev_replace->committed_cursor_left,
1267:			      btrfs_device_get_total_bytes(dev_replace->srcdev),
1268:			      &dev_replace->scrub_progress, false, true);
```

Both sites pass `readonly=false, is_dev_replace=true`, so SR7's replace-side `[inference]` — device replace runs
through the same `btrfs_scrub_dev` — **holds at v7.2.11 source**, on freshly fetched bytes corroborated by a second
host. What does *not* hold is the locator as written: a reader who opens exactly `1265-1267` never sees `true`.

### Defect D1 (precision, non-substantive) — locator one line short

`corpus/knowledge/btrfs-scrub-record-r44.md:21` currently reads:

```
`fs/btrfs/dev-replace.c`, opened this round at v7.2.11 lines 701-703 and 1265-1267 but not pinned].
```

Proposed exact replacement (only `1265-1267` → `1265-1268`):

```
`fs/btrfs/dev-replace.c`, opened this round at v7.2.11 lines 701-703 and 1265-1268 but not pinned].
```

### Defect D2 (pinning gap) — `dev-replace.c` is absent from the frozen set

`ls .ufo/waves/round-44/frozen/src/` = FETCH.txt, PKGBUILD, SHA256SUMS, btrfs-scrub@.service,
btrfs-scrub@.timer, scrub.c, sysfs.c. There is no `dev-replace.c`, so the *only* file that carries SR7's replace
side is unpinned, unfrozen and absent from `FETCH.txt`. The entry is honest about this ("but not pinned"), but the
freeze means a later reader cannot tell whether the fetched bytes drifted.

The C2 counter does not fail on this: `tools/check-scrub-record-r44.py:69` (`F44`) and the `SNAP` map at
`:70-82` pin only the five files, and `QUOTE_RE` at `:105-106` accepts only `scrub.c|ioctl.c|sysfs.c|
btrfs-scrub@.timer|btrfs-scrub@.service|PKGBUILD`, so a `dev-replace.c` quote would be silently skipped rather
than credited — i.e. the replace side cannot be promoted from prose to a pinned quote under the frozen counter as
written. Measured digest for whoever decides to freeze it:

```
f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a  dev-replace.c
```

Proposed `FETCH.txt` line (fits the existing column layout, same tag, same source id as `scrub.c`):

```
dev-replace.c  https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/dev-replace.c?h=v7.2.11   (same tag)  -> S242
```
and a `SHA256SUMS` line: `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a  dev-replace.c`.
I did **not** write either file — frozen content and the lane are read-only to this seat, and changing `frozen/src`
after the freeze commit is the L1's call, not a wave-1 executor's.

## 4. Why this matters for C1 (the arm's predicates)

The three semantics SR7/SR8/SR9 pin are the ones the `SCRUB` line reports, and all three re-read clean on fresh
bytes (`row-basis-2026-10-26.txt`):

- **SR7 progress direction** — `scrub.c:3304-3307` `sctx = dev->scrub_ctx; if (!sctx) … return -ENOTCONN;`,
  `scrub.c:3336` `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`, unknown devid at `scrub.c:3121-3124`
  (`if (!dev || (test_bit(BTRFS_DEV_STATE_MISSING…` → `ret = -ENODEV;`). So `state=RECORDED` can only be read
  while a context is attached: exactly the arm's `state=` semantics.
- **SR8 attribute** — `sysfs.c:2028` `%llu` show, `:2040` `memparse`, `:2042-2044` `skip_spaces`/`-EINVAL`,
  `:2048-2049` `BTRFS_ATTR_RW(devid, scrub_speed_max, …)` with `BTRFS_ATTR_RW` = `__INIT_KOBJ_ATTR(_name, 0644,
  …)` at `:72-74`. The arm's name+stat-only read of the attribute is sound, and `limited=` (value ≠ 0) is sound.
- **SR9 units** — fresh timer: `OnCalendar=monthly`, `AccuracySec=1d`, `RandomizedDelaySec=1w`,
  `Persistent=true`, `WantedBy=timers.target`; fresh service: `KillSignal=SIGINT`,
  `ExecStart=/usr/bin/btrfs scrub start -B %f`. Note the PKGBUILD installs into `/usr/lib/systemd/system`
  (`:100-101`), not `/etc`, so the arm's `/etc/systemd/system/timers.target.wants/btrfs-scrub@*.timer` count is
  counting enable-links, which is the right surface for "is a monthly scrub scheduled".

## 5. Freshness of every quoted line (33/33)

Parsed all `**Quote.** `Snnn` file:N: "…"` locators from `corpus/knowledge/btrfs-scrub-record-r44.md` and compared
each to line N of the **fresh** bytes (S242/S243/S244), the re-hashed r43 snapshot (S240) and the r42 snapshot
(S237): **33/33 substring-exact, 32/33 strip-equal, 0 mismatches, 0 duplicate locators**. Distribution: S237 5,
S240 2, S242 11, S243 7, S244 8. The single non-strip-equal quote is a macro-continuation excerpt that is
correctly trimmed — `S243 sysfs.c:72` quote `#define BTRFS_ATTR_RW(_prefix, _name, _show, _store)` vs line
`…#define BTRFS_ATTR_RW(_prefix, _name, _show, _store)\t\t\t\` — the trailing `\` is deliberately omitted, not a
drift. Every cited line number therefore still points at the same text a day after the freeze.

## 6. Predecessor snapshots re-hashed

```
sha256sum .ufo/waves/round-42/frozen/src/scrub.c
48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801   == round-42 SHA256SUMS:1   ✔
sha256sum .ufo/waves/round-43/frozen/src/ioctl.c
7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01   == round-43 SHA256SUMS:1   ✔
```

These are also the two digests `tools/check-scrub-record-r44.py:71-74` (`SNAP`) pins for `S237`/`S240`, so the
round-44 C2 counter's predecessor pins are intact. `tools/check-scrub-record-r44.py` itself still hashes to its
declared `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059` (measured).

## 7. Host side corroboration (S245 is not a URL, checked anyway)

The installed units on this host are byte-identical to the freshly fetched tag content:
`sha256sum /usr/lib/systemd/system/btrfs-scrub@.timer /usr/lib/systemd/system/btrfs-scrub@.service` →
`9a0b6cc2…`, `eaa7af92…`. Re-running the frozen capture (unprivileged, read-only, writes only its argument —
`capture.sh:3`) into scratch reproduced `capture.txt` line-for-line except the timestamp line
(`NO_DRIFT_except_timestamp`): kernel 7.2.11-arch1-1, btrfs-progs 7.1-1, `var_lib_btrfs absent`,
`devinfo/1/scrub_speed_max mode=644 owner=root value=0`, `wants_btrfs_scrub_instances 0`, timer disabled. So the
host state the entry describes had not moved between the freeze and this re-fetch.

## What I did not do

- Did not run any counter (`score-scrub-arm-r44.py`, `check-scrub-record-r44.py` full run) — not this item; wave 2
  binds verdicts. I read the counter's pin maps statically to date D2's impact.
- Did not `btrfs scrub start/cancel/resume`, write sysfs, enable/start/stop any unit, or touch `/etc`,
  `/var/lib/btrfs`, mounts, packages or services. `pacman -Q/-Qo` inside the frozen `capture.sh` are read-only
  queries.
- Did not fetch the full kernel tree; only the three plain-text files and two `ls-remote` ref queries per remote.
- Did not write `frozen/src` (D2's fix), the entry (D1's fix), or any lane file; only this report and my receipts.
- Did not check `btrfs-scrub@.service`'s systemd `KillSignal=` semantics — that is the entry's own declared
  `[inference]` at `:144-145` and belongs to a wave-2 row review, not to source freshness.

## Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w1/C2ExecLiveSources/`
- `refetch-2026-10-26.txt` — commands, five+one digests, frozen `SHA256SUMS`, `cmp` results
- `tags-2026-10-26.txt` — kernel.org `ls-remote`, Arch `ls-remote`, gregkh-mirror `ls-remote`
- `xcheck-2026-10-26.txt` — gregkh-mirror digests, Arch files fetched by peeled commit
- `dev-replace-2026-10-26.txt` — digest, line-numbered excerpts of 699-705 and 1263-1269, signature
- `row-basis-2026-10-26.txt` — SR7/SR8/SR9 quote lines from the fresh bytes; verbatim units; PKGBUILD 99-101
- `predecessors-2026-10-26.txt` — r42/r43 re-hash vs their `SHA256SUMS`
- `quote-sweep-2026-10-26.txt` — the 33-quote locator sweep result
- `host-corroboration-2026-10-26.txt` — installed-unit digests, capture replay
