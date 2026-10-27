VERDICT: supports

# C2ExecLiveSources — C2-1 live source re-fetch (round 45, wave a2w1)

Re-fetched every URL in `round-45/frozen/src/FETCH.txt`, resolved the tag commits live, and
re-hashed the round-44 and round-42 frozen sources. Every digest matches; no C2 kill-rule hit on
the source-freshness plane. One citation-granularity observation for the counted GR3 seats is at
the end (not a falsification of my item).

Environment: access date **2026-10-27** (UTC 03:24:48Z–03:26Z), all curls `-sSfL --max-time 60`.
Scratch `/fast/scratch/hyaku/tsukuroi-r45/C2ExecLiveSources` (removed at end of seat).
Receipts: `.ufo/waves/round-45/a2w1/C2ExecLiveSources/` (18 files, 68 KB).

## 1. Round-45 URLs re-fetched, sha256 vs `frozen/src/SHA256SUMS`

Commands (receipt `r45-fetch.log`, `r45-refetch-sha256.txt`, `r45-sums-check.txt`):

```
K=https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain
curl -sSfL "$K/lib/cmdline.c?h=v7.2.11"        -o cmdline.c
curl -sSfL "$K/fs/btrfs/dev-replace.c?h=v7.2.11" -o dev-replace.c
curl -sSfL "$K/lib/kstrtox.c?h=v7.2.11"        -o kstrtox.c
curl -sSfL "$K/lib/vsprintf.c?h=v7.2.11"       -o vsprintf.c
curl -sSfL https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.kill.xml -o systemd.kill.xml
sha256sum cmdline.c dev-replace.c systemd.kill.xml kstrtox.c vsprintf.c
( cd <lane>/.ufo/waves/round-45/frozen/src && sha256sum -c SHA256SUMS )
```

| file | live sha256 (2026-10-27) | stored SHA256SUMS | bytes | verdict |
|---|---|---|---|---|
| cmdline.c | `1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d` | same | 6330 | MATCH |
| dev-replace.c | `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a` | same | 39841 | MATCH |
| systemd.kill.xml | `448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72` | same | 11224 | MATCH |
| kstrtox.c | `0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4` | same | 11483 | MATCH |
| vsprintf.c | `cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca` | same | 92345 | MATCH |

All five curls exited 0 (each logged with timestamp, `curl_exit=0`, byte count).
`sha256sum -c` over the stored directory: `cmdline.c: OK` … `vsprintf.c: OK` (5/5 OK).

## 2. Tag commits resolved live vs `FETCH.txt`

Commands (receipts `ls-remote.log`, `ls-remote-peeled.log`):

```
git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git 'refs/tags/v7.2.11*'
git ls-remote https://github.com/systemd/systemd 'refs/tags/v262*'
git ls-remote https://github.com/systemd/systemd 'refs/tags/v262^{}'
git ls-remote https://github.com/kdave/btrfs-progs 'refs/tags/v7.1*'
```

Observed output, 2026-10-27T03:24:48Z and 03:25:36Z:

```
8316c24ec1b77dba19ba072ca4fe251b36dc65d3	refs/tags/v7.2.11
a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea	refs/tags/v7.2.11^{}
1f7dffaf714cc4488159c498b7a17cf34c5a96d5	refs/tags/v262
8cc40e0c5e9234bf45084751ac53b1fbfe70b492	refs/tags/v262^{}
bf15b74fb4ed33d8be9ce800adf71eb7fbd5431a	refs/tags/v262-rc1
0896c973217b17e66a916b2caa43aefbc5357f3b	refs/tags/v262-rc1^{}
5584ace34ff3775fa6551420c213da2d84c36e14	refs/tags/v262-rc2
3b2900f0508b4875a53e412bd02fd12b80eaf215	refs/tags/v262-rc2^{}
a43267cd0eff05646c88427417240c0f3933a40f	refs/tags/v262-rc3
f3880debd70d384c300a477be0ab44113eee1ac7	refs/tags/v262-rc3^{}
f85dfc5dd463f37b67ce589e511be36f527b19f6	refs/tags/v262.1
73612ea502d53baf9b0df4336cfc296a7ee0d524	refs/tags/v262.1^{}
0a919c7d6e389c07920675b7fad3f793b92aa78b	refs/tags/v7.1
4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b	refs/tags/v7.1^{}
```

`FETCH.txt` (tag block) lines 6–17 of the round-45 file list exactly these ten systemd values plus
`8316c24e…`/`a2de78ee…` for v7.2.11; live output is line-for-line identical, including all
`-rc*` and `v262.1` rows. Peeled commits therefore still resolve to
`a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea` (Linux v7.2.11) and
`8cc40e0c5e9234bf45084751ac53b1fbfe70b492` (systemd v262), as declared.

## 3. Content bound to the commit, not merely to the tag name

A `?h=<tag>` / `<tag>/` URL resolves a name; to exclude a re-pointed or rewritten tag I re-fetched
the same paths pinned to the peeled commit (`git.kernel.org` `?id=<sha>`, raw.githubusercontent
`/<commit>/`). Receipts `pinned.log`, `r45-pinned-sha256.txt`, `r45-pinned-vs-tag.txt`:

```
K=…/plain ; P=a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea
curl -sSfL "$K/lib/cmdline.c?id=$P" -o cmdline.c          # and dev-replace.c, kstrtox.c, vsprintf.c
curl -sSfL https://raw.githubusercontent.com/systemd/systemd/8cc40e0c5e9234bf45084751ac53b1fbfe70b492/man/systemd.kill.xml
for f in …; do cmp -s pinned/$f r45/$f; done
```

Result: all five `IDENTICAL pinned-vs-tag`, and the five commit-pinned digests equal the
tag-resolved digests above. The frozen bytes are the bytes of the declared commits.

## 4. Frozen bytes are the bytes committed at freeze

Receipt `freeze-blobs.txt` (`git -C <lane> show ea6e0ee….ufo/waves/round-45/frozen/src/<f> | sha256sum`):

```
cmdline.c          freeze=1af5ad98…469ca9d live=1af5ad98…469ca9d MATCH
dev-replace.c      freeze=f07ef0a0…34f3a     live=f07ef0a0…34f3a     MATCH
systemd.kill.xml   freeze=44832283…910e72    live=44832283…910e72    MATCH
kstrtox.c          freeze=0c52ae02…8d1ee4    live=0c52ae02…8d1ee4    MATCH
vsprintf.c         freeze=cabb648a…469ca     live=cabb648a…469ca     MATCH
git diff --stat ea6e0ee3 HEAD -- .ufo/waves/round-45/frozen/src   → empty (identical)
```

Ancillary (not my count): `tools/check-scrub-grounding-r45.py` hashes
`a1eb402dffae97fcefd9bd539529f1cacc5034419b6de06e1f8ac1c08d011331`, matching the declared C2
counter digest; `tools/score-census-readers-r45.py` hashes `fe0e31e2…3250bd50`, matching C1's.

## 5. Round-44 sources re-fetched and round-42 / round-44 stored bytes re-hashed

Commands (receipts `r44-fetch.log`, `r44-refetch-sha256.txt`, `r44-sums-check.txt`,
`r42-refetch-sha256.txt`, `r42-sums-check.txt`):

```
K=https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain
G=https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1
curl -sSfL "$K/fs/btrfs/scrub.c?h=v7.2.11" -o scrub.c
curl -sSfL "$K/fs/btrfs/sysfs.c?h=v7.2.11"  -o sysfs.c
curl -sSfL "$G/btrfs-scrub@.timer" -o 'btrfs-scrub@.timer'   # + .service, PKGBUILD
( cd r44 && sha256sum -c <lane>/.ufo/waves/round-44/frozen/src/SHA256SUMS )
( cd <lane>/.ufo/waves/round-42/frozen/src && sha256sum -c SHA256SUMS )
```

Round 44 (live vs `round-44/frozen/src/SHA256SUMS`; `sha256sum -c` 5/5 OK):

| file | live sha256 | bytes |
|---|---|---|
| scrub.c | `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` | 100417 |
| sysfs.c | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` | 72925 |
| btrfs-scrub@.timer | `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad` | 160 |
| btrfs-scrub@.service | `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252` | 190 |
| PKGBUILD | `3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98` | 3057 |

All five identical to the stored digests.

Round 42 (`round-42/frozen/src/SHA256SUMS`, stored files re-hashed: `scrub.c: OK`, `CHANGES: OK`)
and a live re-fetch of the two declared URLs, which also matches:

| file | live re-fetch | stored SHA256SUMS | bytes |
|---|---|---|---|
| scrub.c | `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` | same | 57034 |
| CHANGES | `bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22` | same | 93779 |

`git ls-remote https://github.com/kdave/btrfs-progs 'refs/tags/v7.1*'` still gives annotated tag
`0a919c7d6e389c07920675b7fad3f793b92aa78b` → peeled `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`,
matching `round-42/frozen/src/FETCH.txt` line 1.

Caveat recorded, not claimed as a hit: `round-44/frozen/src/SHA256SUMS` does not cover
`btrfs-scrub@.timer`'s companion link targets beyond the five listed files, and round-42's FETCH
date is 2026-10-26 — both are one day old, so this re-fetch tests reproducibility of a very recent
freeze rather than a long-interval one.

## 6. The GR anchors survive in the live bytes (spot-check, not a GR verdict)

Grep coordinates in the refetched copies, receipt `anchors.txt`:

- GR1: `cmdline.c:153 unsigned long long memparse(const char *ptr, char **retptr)`,
  `EXPORT_SYMBOL(memparse)` at `:201`; the decimal paths it delegates to —
  `vsprintf.c:112 simple_strtoull(...)`, `kstrtox.c:139 int kstrtoull(...)`; and the write side in
  the r44 copy `sysfs.c:2031 btrfs_devinfo_scrub_speed_max_store` → `:2040 limit = memparse(buf, &endptr)`
  → `:2045 WRITE_ONCE(device->scrub_speed_max, limit)`. GR1's parser claim holds on live bytes.
- GR2: `dev-replace.c:701` and `:1265` call `btrfs_scrub_dev(fs_info, …srcdev->devid, …, false, true)`
  (last argument `is_dev_replace = true`); `scrub.c:3148` reads
  `(!is_dev_replace && btrfs_dev_replace_is_ongoing(...))` → `:3153 ret = -EINPROGRESS;`.
  Non-replace scrubs are refused while a replace is ongoing, as GR2 states.
- GR3: `systemd.kill.xml:91` (`TimeoutStopSec=` expiry), `:96`/`:110`/`:172` `SIGKILL` after it,
  `:115` `SIGCONT` before it. The stop-signal *default* is `SIGTERM` (`:107`), and **`SIGINT` does
  not appear anywhere in `man/systemd.kill.xml` v262** (`grep -n SIGINT` → no occurrence).

### Observation for C2RevGR3 / C2CritGR3 (not a C2 kill-rule hit from my side)

GR3 as declared reads "systemctl stop of btrfs-scrub@.service under systemd v262: SIGINT to the
control group, SIGCONT, SIGKILL after TimeoutStopSec; 5 s on this host". The SIGINT step is not
sourced from S248 — it comes from the packaged unit: `round-44/frozen/src/btrfs-scrub@.service:9
KillSignal=SIGINT` (live re-fetch identical). So the row is supported, but only if its citation
block attributes SIGINT to S244 (Arch btrfs-progs 7.1-1 packaging) and reserves S248 for SIGCONT /
SIGKILL-after-`TimeoutStopSec=` / `KillMode=control-group` semantics. If the frozen corpus file
attributes SIGINT to S248, that is a citation defect the counted GR3 seats should rule on — I do
not rule on it.

## 7. What I did not do

- Did not run `tools/check-scrub-grounding-r45.py` (not my item; the counted seats own the counter).
- Did not evaluate GR1–GR3 as rows — only checked that the cited anchors still exist at the cited
  sources; the truth of the rows is C2RevGR*/C2CritGR* work.
- Did not re-fetch S249 `frozen/hostcap/capture.txt` content beyond confirming it is not URL-backed
  (no URL in `FETCH.txt` refers to it); own-work captures cannot be freshness-checked by re-fetch.
- Did not verify the "5 s TimeoutStopSec on this host" number (that is a `systemctl show` host read
  owned by the GR3 seats; it is also the one part of GR3 not derivable from the frozen URLs).
- No tools installed or upgraded; no host mutation; no git/jj mutation; nothing written outside the
  seat dir and scratch.

## 8. Risks / blockers

- None blocking. Residual risk is only that all four freeze sets are ≤1 day old: this proves the
  digests are reproducible now, not that they will stay resolvable (e.g. if `git.kernel.org` or
  `raw.githubusercontent.com` rotate), and the frozen copies remain the durable evidence.
- Fetch endpoint asymmetry worth knowing for later waves: the two host types answer `?h=<tag>` /
  `<tag>/` but only `?id=<sha>` / `/<sha>/` pin to a commit; my commit-pinned re-fetch covers the
  five round-45 files only.

Report path: `.ufo/waves/round-45/a2w1/C2ExecLiveSources.md`
