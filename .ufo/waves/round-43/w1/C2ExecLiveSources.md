VERDICT: supports

Item C2-1 (live source re-fetch, round-43 w1, seat C2ExecLiveSources). All three declared sources
re-fetched live on 2026-10-26T22:16:45Z are byte-identical to the frozen snapshots, both declared tags
resolve to the declared peeled commits on two independent forges, and all 28 `path:line` quotes in the
C2 draft rows SR1/SR3/SR6 still match the live files. Two additions the declaration does not carry: the
Arch `btrfs-progs` 7.1-1 package ships upstream v7.1 unpatched (patch list is empty), and the host
kernel's `fs/btrfs/ioctl.c` is upstream-identical (the Arch kernel patch touches no btrfs file). One
freshness caveat: upstream has moved to btrfs-progs v7.3 and stable 7.2.13, with no change to any SR
anchor.

## What I ran

Fetches (curl -sSfL, all HTTP/2 200, receipt-http-provenance.txt), `sha256sum`/`cmp` against the frozen
snapshots, `git ls-remote` on four remote/repo pairs, `git verify-tag` and `gpg --verify` in an isolated
`GNUPGHOME` under scratch, the Arch GitLab API for packaging metadata, one kernel.org release tarball,
and a scripted line-anchor comparison of the draft's quotes against the live files. No privileged ioctl,
no scrub, no write to `/var/lib/btrfs`, no host mutation.

Scratch: `/fast/scratch/hyaku/tsukuroi-r43/C2ExecLiveSources/` (removed at the end; receipts copied to
`.ufo/waves/round-43/w1/C2ExecLiveSources/`).

## 1. Live content is byte-identical to the frozen snapshots

| source | URL (fetched 2026-10-26T22:16:45Z) | live sha256 | frozen sha256 | verdict |
|---|---|---|---|---|
| S237 scrub.c | `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` | `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` | `48df2e2f…` (`.ufo/waves/round-42/frozen/src/SHA256SUMS`) | identical (`cmp` clean) |
| S240 ioctl.c (git.kernel.org) | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11` | `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01` | `7b3488f2…` (`.ufo/waves/round-43/frozen/src/SHA256SUMS`) | identical (`cmp` clean) |
| S240 ioctl.c (GitHub mirror) | `https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/ioctl.c` | `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01` | same | identical to the kernel.org copy (`cmp` clean) |

Evidence: `.ufo/waves/round-43/w1/C2ExecLiveSources/receipt-sha256.txt` (live sums, frozen sums, and the
three `cmp` results: `scrub.c: live==frozen-r42`, `ioctl.c: live==frozen-r43`,
`ioctl.c: gregkh==kernel.org`), `receipt-http-provenance.txt` (content-length 57034 and 145999 on both
ioctl.c URLs, etags recorded). Sizes match the frozen files on disk (57034, 145999 bytes).

The declaration's S241 host capture also re-hashes to its declared value: `capture.txt`
= `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556` (`sha256sum` run 2026-10-26).

## 2. Tag identity holds on both forges

`git ls-remote`, 2026-10-26T22:18:14Z (`receipt-ls-remote.txt`):

```
0a919c7d6e389c07920675b7fad3f793b92aa78b	refs/tags/v7.1        (github.com/kdave/btrfs-progs)
4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b	refs/tags/v7.1^{}
0a919c7d…/4ab0e80b…   (same two lines from git.kernel.org/…/kdave/btrfs-progs.git)
8316c24ec1b77dba19ba072ca4fe251b36dc65d3	refs/tags/v7.2.11     (github.com/gregkh/linux)
a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea	refs/tags/v7.2.11^{}
8316c24e…/a2de78ee…   (same two lines from git.kernel.org/…/stable/linux.git)
```

So the declared peeled commits `4ab0e80b…` (btrfs-progs v7.1) and `a2de78ee…` (stable v7.2.11) are
confirmed, and the tag objects `0a919c7d…` / `8316c24e…` named in the two `FETCH.txt` files are
confirmed. Both tags are annotated; `git verify-tag v7.1` in scratch reports
`Good signature from "David Sterba <dsterba@suse.cz>"`, signature made Tue 14 Jul 2026 19:41:55 -03, key
`F2B41200C54EFB30380C1756C565D5F9D76D583B` (`receipt-tag-signature.txt`; peeled commit in that repo
`4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`).

## 3. Independent artifact path: the release tarball agrees

`https://www.kernel.org/pub/linux/kernel/people/kdave/btrfs-progs/btrfs-progs-v7.1.tar.xz`
(sha256 `d1f55cc2971398c9142eaa79d203e63d586a3b4b867f956664a1d68322cd4e34`, 4997528 bytes) contains
`btrfs-progs-v7.1/cmds/scrub.c` = `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`,
i.e. a third copy (release tarball) equal to the GitHub-raw tag content and to the round-42 frozen
snapshot (`receipt-sha256.txt`, line `scrub-tarball-v71.c`, plus `scrub.c: release-tarball==github-raw`).
`btrfs-progs` ships no kernel `fs/btrfs/ioctl.c` (0 matches in the tarball listing), so S240 has no
tarball path — its provenance is the two forge copies plus the tag.

The tarball's detached signature verifies: `gpg --verify btrfs-progs-v7.1.tar.sign btrfs-progs-v7.1.tar`
→ `Good signature`, RSA key `F2B41200C54EFB30380C1756C565D5F9D76D583B`, signature dated Tue 14 Jul 2026
19:42:12 -03, exit 0 (`receipt-tarball-signature-refreshed.txt`).

Caveat worth recording: with the key copy vendored in the Arch packaging repo
(`keys/pgp/F2B41200C54EFB30380C1756C565D5F9D76D583B.asc`) gpg reports
`Good signature … [expired]` / `Note: This key has expired!` (`receipt-tarball-signature.txt`), because
that copy's self-signature expires 2024-08-24 — before the 2026-07-14 signature date. The refreshed copy
from `keyserver.ubuntu.com` carries expiry 2034-01-09 and verifies without the expired flag. So the
expiry flag is an artifact of the stale vendored key copy, not a bad signature; the load-bearing chain is
tag→tarball→file, which is intact.

## 4. Arch `btrfs-progs` 7.1-1 applies no patches

Arch packaging repo `archlinux/packaging/packages/btrfs-progs`, tag `7.1-1` = commit
`0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0` (2026-07-15, "upgpkg: 7.1-1: update to latest version",
Tobias Powalowski), tag object `4fd401153bd8eac8ab9e37e6511e1bf2350fdd07`
(`receipt-arch-packaging.txt`).

- **Patch list: empty.** The recursive tree at `7.1-1` has 15 entries and 0 `*.patch` files
  (`PKGBUILD-7.1-1` and the recursive blob list in `receipt-arch-packaging.txt`).
- `source=()` is `git+https://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git?signed#tag=v${pkgver}`
  plus four packaging files (`PKGBUILD-7.1-1:46-51`), i.e. a signed checkout of the very tag whose
  peeled commit is `4ab0e80b…`.
- `prepare()`'s patch loop (`PKGBUILD-7.1-1:59-69`) is inert: `[[ $src = *.patch ]] || continue` never
  matches.
- Packaging files relevant to this lane: `initcpio-install-btrfs` / `initcpio-hook-btrfs` (installed as
  `/usr/lib/initcpio/hooks/btrfs`, body `btrfs device scan` at line 4 — a boot-chain input under C1's
  `/usr` start points), `btrfs-scrub@.service` with `ExecStart=/usr/bin/btrfs scrub start -B %f` (line
  10), `btrfs-scrub@.timer` (`OnCalendar=monthly` line 5, `Persistent=true` line 8).

Consequence: the host's `/usr/bin/btrfs` (`btrfs --version` → `btrfs-progs v7.1`; `pacman -Q btrfs-progs`
→ `btrfs-progs 7.1-1`) is upstream v7.1 source, so S237's line numbers and logic describe the binary that
wrote any record on this host. This also makes SR3's print condition live on the host: the shipped unit
passes `-B`, which sets `do_print` (scrub.c:1295), so a recording failure under the shipped service would
print.

## 5. The host kernel's ioctl.c is upstream-identical

Arch `linux` 7.2.11.arch1-1 (commit `0c178d550ec6392265d3a443333229823634bd08`, 2026-10-16;
`receipt-arch-kernel.txt`) builds from `linux-7.2.11.tar.xz` plus
`archlinux/linux` release `v7.2.11-arch1` → `linux-v7.2.11-arch1.patch.zst`
(sha256 `741d473c4db335d97d9e1d9b8be9337090522550804fe6454ba336d21e580fd6`, equal to
`sha256sums[2]` in `arch-linux-PKGBUILD:65`). That patch is 160 lines and touches only `Makefile`,
`drivers/gpu/drm/amd/display/amdgpu_dm/amdgpu_dm.c`, `drivers/gpu/drm/i915/display/intel_dp.c` and
`kernel/fork.c` — **0** occurrences of "btrfs". So the running kernel's `fs/btrfs/ioctl.c` is the file S240
froze, and SR6's `-EPERM` gate describes this host (consistent with the capture's
`scrub_progress_ioctl devid=1 errno=EPERM (1)` at `capture.txt:6`).

## 6. Every quote in the draft rows still lands on the same live line

A script compared all 28 `**Quote.**` pairs of `corpus/knowledge/btrfs-scrub-record-r43.md` (rows SR1,
SR3, SR6) against the freshly fetched files: **28 match, 0 mismatch**
(`receipt-quote-anchors.txt`), e.g.
`S237 scrub.c:517` = `return scrub_open_file(datafile, O_WRONLY|O_CREAT);`,
`S237 scrub.c:925` = `err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");`,
`S240 ioctl.c:3133` = `return -EPERM;`.

Mechanism checks behind the statements (live file, line numbers as in S237/S240):

- SR1, no truncation anywhere: `grep -c 'lseek|ftruncate|truncate('` on scrub.c = **0**. So the record is
  written from offset 0 of a non-truncated `_tmp`, which is exactly the premise of the draft's
  trailing-bytes `[inference]`. `open(…, m, 0600)` at :483 and `flock(fd, LOCK_EX|LOCK_NB)` at :487.
- SR1, "never unlinked": exactly three `unlink(` calls in scrub.c (:1485, :1497, :1721) and all three
  name `sock_path`; none names a record or `_tmp` path.
- SR1 ordering: :917 open `_tmp` → :922 write → :925 rename, with `if (err) goto out1;` at :923-924 and
  :926-927, so a failed write skips the rename.
- SR3: `cmd_scrub_resume` = `return scrub_start(cmd, argc, argv, true);` (:1833); `scrub_resumed_stats`
  (:800-828) sums the 13 counters and sets `dest->stats.t_start = data->resumed->stats.t_start;` (:823)
  and `duration = resumed->duration + duration` (:824-825).
- SR3, failure printing: both branches are gated by `do_print` — :1690 `if (do_print && ret)` and :1696
  `if (do_print && terr && terr != PTHREAD_CANCELED)` printing "recording progress failed: %m" (:1698),
  :1704 `if (ret && do_print)` printing "failed to record the result: %m" (:1706); neither assigns `err`.
  `do_print` defaults false (:1249), set by `-B` (:1295), cleared when quiet (:1332-1333).
- SR6: `is_scrub_running_in_kernel` (:1190-1206) returns 1 only on `if (!ret)` (:1201-1202) and otherwise
  falls through to `return 0` (:1205) — any errno, including `EPERM`, reads as not running.
- SR6, "as do the scrub start and cancel ioctls": ioctl.c:3072 (`btrfs_ioctl_scrub`, :3066), :3120
  (`btrfs_ioctl_scrub_cancel`, :3118) and :3132 (`btrfs_ioctl_scrub_progress`, :3126) all read
  `if (!capable(CAP_SYS_ADMIN))` then `return -EPERM;` (:3073, :3121, :3133).

## 7. Freshness: upstream moved, the anchors did not

Probe at 2026-10-26T22:19:32Z (`receipt-freshness.txt`, `receipt-http-provenance.txt`):

- btrfs-progs newest tags: `v7.0, v7.1, v7.3` (there is no v7.2 tag); `v7.3` = `b5cb02e0…` peeled
  `afdc3a65e33f4d42f768ad50dca20c32e5ee1496`. Arch packaging's newest tag in the same repo is `7.3-1`.
- kernel.org `releases.json`: latest stable `7.3`, stable branch `7.2.13` (`v7.2.13` = `296212c4…` peeled
  `3c172eed…`). The host is on 7.2.11-arch1-1.
- `fs/btrfs/ioctl.c` is **byte-identical** between v7.2.11 and v7.2.13
  (`7b3488f2…` both, `diff` 0 lines), so SR6 is current, not merely historical.
- scrub.c v7.1 → v7.3 (`scrub-v71-vs-v73.diff`, 52 diff lines / 24 changed): two message-and-comment
  typo fixes (`pos`→`position`, `ie.`→`i.e.`) and one relocation — the scrub-throughput-limit revert
  moves out of the per-device loop into its own loop. No SR1/SR3/SR6 code path, flag, message or
  ordering changes; v7.3 still has 0 `lseek/ftruncate/truncate`, the same three `sock_path` unlinks
  (:1485, :1497, :1723), the same open→write→rename sequence at :917/:922/:925, and both `do_print`
  messages (:1700, :1708).

So the rows are not stale, but the pinned snapshot is one upstream release behind and the doc's
`recheck: on-release` trigger has now fired for btrfs-progs (v7.3) and for stable (7.2.13).

## Findings, risks, caveats

1. **No defect found in the frozen provenance.** All three declared digests, both declared peeled
   commits, both tag objects and the host capture digest reproduce exactly.
2. **The Arch package adds nothing to v7.1** (empty patch list), so S237 is not Arch-modified; and the
   Arch kernel patch adds nothing to `fs/btrfs`, so S240 is not Arch-modified. Neither source needs an
   "Arch divergence" caveat.
3. **Key-expiry artifact (informational).** The vendored Arch key copy shows expiry 2024-08-24 while both
   the tag and the tarball signatures date 2026-07-14; with a refreshed key copy both verify clean. Do
   not cite the "[expired]" line as a provenance failure.
4. **Freshness debt.** btrfs-progs v7.3 and stable 7.2.13 exist; the draft's `verified-at`/`recheck` lines
   pin v7.1/v7.2.11 without noting that later tags exist. Content-wise harmless (see §7), but a reader
   checking "is this current" would find v7.3. Optional wording below.
5. **Not verified by me:** the `linux-7.2.11.tar.xz` signature (140 MB not downloaded — the chain here is
   PKGBUILD sha256 of the Arch patch + the Arch patch's file list); the `.sig` of the Arch kernel patch
   (its sha256 matches the PKGBUILD, which is what the package pins); and the signature of the
   `archlinux/linux` patch tag. None of these bears on the SR rows, whose sources are the two files above.
6. **Not run:** any scrub, any privileged ioctl, any write under `/var/lib/btrfs`; no `/etc` or `/usr`
   change; no package operation. `pacman -Q`/`-Qi` and file reads only.

## Optional proposed text (not requested by this item)

If the L1 wants the freshness note in the doc header, a one-line addition to the `recheck:` paragraph of
`corpus/knowledge/btrfs-scrub-record-r43.md`:

> Later tags exist and were checked on 2026-10-26: btrfs-progs `v7.3` (no `v7.2` tag) and stable
> `v7.2.13`; `fs/btrfs/ioctl.c` is byte-identical between `v7.2.11` and `v7.2.13`, and the `v7.1`→`v7.3`
> `scrub.c` diff (24 changed lines) touches only two message typos and the relocation of the
> throughput-limit revert, so no SR1/SR3/SR6 line or code path moved.

## Receipts

`.ufo/waves/round-43/w1/C2ExecLiveSources/`: `receipt-sha256.txt`, `receipt-ls-remote.txt`,
`receipt-tag-signature.txt`, `receipt-tarball-signature.txt` (stale-key copy),
`receipt-tarball-signature-refreshed.txt`, `receipt-arch-packaging.txt`, `receipt-arch-kernel.txt`,
`receipt-quote-anchors.txt`, `receipt-freshness.txt`, `receipt-http-provenance.txt`,
`live-sha256.txt`, `fetched_utc.txt`, `PKGBUILD-7.1-1`, `SRCINFO-7.1-1`, `tag-7.1-1.json`,
`releases.json`, `scrub-v71-vs-v73.diff` (72 KB total).

Tooling: nothing installed or upgraded; only host tools used (`curl`, `git`, `gpg`, `sha256sum`, `cmp`,
`diff`, `zstd`, `tar`, `python3`, `pacman -Q`).
