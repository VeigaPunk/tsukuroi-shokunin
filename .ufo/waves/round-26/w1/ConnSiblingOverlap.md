# ConnSiblingOverlap — round 26, wave 1 (C1 storage integrity)

Verdict: done — no sibling lane declares or is working any surface in SH1 to SH6, so all six rows are tsukuroi's (OS substrate, read-only diagnosis). Mori holds shared evidence for SH1, SH3 and SH6 and is the recipient for one drafted adjacency row, ADJ-08. Mori round 26 is working earlyoom right now, and C1 does not touch that work. I also found one thing the entry needs: the kernel names `nvme0` and `nvme1` swapped between the last two boots. SH4 to SH6 should therefore be bound to a stable device identity, and the second drive should be named as unmeasured.

Lane HEAD read: `b13e991fb96972b423b868ba122187f75357368c` (the declaration commit). Read window 2026-10-22T13:47Z to 13:53Z.

## Findings

1. [obs] The requested terms have no storage-integrity hits in any sibling province or corpus index. I searched all 20 sibling `PROVINCE.md` and `corpus/README.md` files (40 files; tsukuroi excluded) for the terms below.
   - `btrfs`, `smartctl`, `nvme`, `fstrim`, `unsafe shutdown` and the case-sensitive word `SMART` each had 0 hits. Command: `rg -c -i -F <term> *-shokunin/PROVINCE.md *-shokunin/corpus/README.md | rg -v '^tsukuroi'`, run from `/home/vgpnk/Projects/shokunin`; it printed nothing for these terms.
   - `scrub` had 6 hits in 4 files, and every one is the environment-scrubbing sense, not btrfs scrub: `kotoba-shokunin/corpus/README.md:38`, `kumitate-shokunin/corpus/README.md:99` ("scrubbed git env"), `mori-shokunin/corpus/README.md:14,124` ("pins scrubbed from the exec-time environ"), and `tameshi-shokunin/corpus/README.md:9,266` ("`GIT_*` prefix scrub").
   - `disk`, `filesystem` and `storage` had hits, but only mori's are a storage surface. Mori's are resource runway at `mori-shokunin/PROVINCE.md:10,26,49` and `mori-shokunin/corpus/README.md:158-208,337`.
   - All the other hits use the words incidentally: "on disk" or "removed from the filesystem", souji's quarantine rename semantics (`souji-shokunin/PROVINCE.md:94,107`), kengaku's "storage label" (`kengaku-shokunin/PROVINCE.md:84`), and kotodama's vocabulary entries.
   - The single word-bounded hit for the core term set is `kasegi-shokunin/PROVINCE.md:6`, "`~/Projects/bounties` was removed from the filesystem at 2026-09-28T23:51:31Z". It records a deletion, not an integrity fault.

2. [obs] Mori's province owns disk capacity runway, not device integrity. It routes device and driver faults to tsukuroi. All references below are to `mori-shokunin` at `21386b9ccb634a21aace80e157827d49c29efe14`. `PROVINCE.md` has sha256 `d0c137482e317a326e463a91eaca3060e5842812dbfdc8e3b5e2de6a9b821f07`, and the working tree equals HEAD for this file.
   - `PROVINCE.md:10`: "resource runway (disk on the fleet root and `/tmp`, memory pressure)".
   - `PROVINCE.md:26`: "default `df -P` targets `$ROOT` and `/tmp`, since-boot device-write average".
   - `PROVINCE.md:12-14`: "**Refuses:** … OS package, systemd unit, driver/firmware and boot state (→ tsukuroi)".
   - `PROVINCE.md:289-290`: "explaining a high IRQ or memory reading as a device, driver or OS fault stays with tsukuroi."
   - `SKILL.md:415-418` (sha256 `a623c8ab875959686b04c10a5dd1840110e13115ddba8d0397dac4de8ddc7b9d`, equal to HEAD): "**Never threshold the btrfs chunk percent.** Data-chunk fill reads **94.25%** while `df -P` Capacity on the same device reads **10%**".
   - Mori's census picks the device for its write average from the `df` source and matches the kernel name in `/proc/diskstats` (`mori-shokunin/tools/mori-census.sh:1872-1886`).

3. [obs] Tsukuroi's S133 and mori's S079 are the same source file, and the bytes agree. This is shared evidence, not shared ownership.
   - Mori's `corpus/SOURCES.md:85` row S079 is `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c`. It is mined on 2026-10-21 for qgroup flags and device link names, and records "sha256 ce146120f29ac29c".
   - I fetched the same URL: `curl -fsS -o /fast/scratch/hyaku/tsuku26/ConnSiblingOverlap/sysfs-v7.2.c <url>` exited 0. Its sha256 is `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`, and the prefix matches mori's.
   - The counters SH1 needs are in that file: `btrfs_devinfo_error_stats_show` at line 2074, `"write_errs %d\n"` at 2089, `BTRFS_ATTR(devid, error_stats, btrfs_devinfo_error_stats_show);` at 2100 and `BTRFS_ATTR_PTR(devid, error_stats),` at 2108.
   - [obs] At 13:5xZ the tsukuroi snapshot `.ufo/waves/round-26/sources/S133.*` did not exist yet (`ls .ufo/waves/round-26/sources/` lists S128 to S132 and S134 to S138).
   - Mori's S079 proposition is about qgroups, while S133's is about device error counters. The rows should stay separate and are not merged, following mori's own rule at `PROVINCE.md:90`.

4. [obs] No sibling's last five commits touch any SH surface, and neither do the uncommitted trees. I ran `git -C <lane> log -5 -p` for the 20 siblings (read-only) and matched added or removed lines against `btrfs|smartctl|smartmontools|nvme|fstrim|unsafe shutdown|error_stats|scrub status|btrfs-scrub|Percentage Used|media errors|dev_stats`.
   - Every match except one is the operator tooling-directive text "`btrfs-overlayfs` and `plymouth` hooks still expect `/new_root`", copied into dispatch and result files (chousa 8 lines, kaidoku 130, kasegi 128, kengaku 154, kotodama 4, kumitate 16, souji 321, tabi 128).
   - The one exception is mado: a single line, "Mount is btrfs `@home` with `noatime`, so atime …", about atime, not integrity.
   - Mori had 0 matching lines. Its last five commits are round-26 earlyoom work (finding 5).
   - Uncommitted sibling changes (`git --no-optional-locks status --porcelain`) contain no storage-integrity files. Mori's only modified tracked file is `corpus/knowledge/userspace-oom-killers-r12.md`.
   - A wider scan of tracked sibling `corpus/`, `PROVINCE.md` and `SKILL.md` found btrfs or NVMe text only in contexts unrelated to C1:
     - mori qgroups, S079 to S081, in `corpus/lessons/round-23.md:28,45-47`;
     - mori chunk fill (`SKILL.md:415`) and `/proc/diskstats` device names;
     - souji per-subvolume `st_dev` (`souji-shokunin/corpus/knowledge/quarantine-same-filesystem-rename.md:44`);
     - chousa mount aliases (`chousa-shokunin/corpus/knowledge/mount-alias-r14.md:31`);
     - kumitate's task isolation backend names (`kumitate-shokunin/corpus/knowledge/omp-task-contract.md:94-96`);
     - kasegi's 2026-09-28 mount line, with `/home` on `nvme1n1p2` (`kasegi-shokunin/corpus/knowledge/source-tree-loss-2026-09-28.md:37`);
     - a kengaku round-12 df listing with an older layout (`kengaku-shokunin/corpus/evidence/round12-fleet/r12-endpoint-freshness.md:655-658`).

     None of these mentions error counters, scrub, SMART health or lifetime counters.

5. [obs] Mori round 26 is working earlyoom right now. Its contract `mori-shokunin/.ufo/waves/round-26/contract.md` names FR10 userspace OOM killers, with C1 "supersede the stale FR10 host-state statements" and C2 `tools/mori-oom-killers.py`.
   - Its HEAD commits from 10:28 to 10:39 -03 (13:28Z to 13:39Z) are earlyoom work: `738eec1` "a stopped earlyoom with sends this boot reads KILLER_ACTED", `93aa1b9`, and `b4473ed` "FR10 host captures … per-boot earlyoom line counts".
   - Its working tree modifies `corpus/knowledge/userspace-oom-killers-r12.md`.
   - The roster shows `MoriR26.SrcEarlyoomUnit`, `MoriR26.SrcEarlyoomMainC`, `MoriR26.SrcEarlyoomKillC` and `MoriR26.WriteOomKillersCases` live.

   [inf] C1 does not touch that work:
   - Mori's reads are `systemctl show earlyoom.service`, `journalctl -u earlyoom.service` and the oomd `MESSAGE_ID`. C1 reads the kernel `BTRFS` lines, btrfs counters, scrub status, unit files for `btrfs-scrub@.timer` and `fstrim.timer`, and NVMe health logs. The queries are disjoint, and no C1 source (S128 to S138) is an earlyoom or oomd source.
   - The only conceptual contact is SH6. A hard power-off after a memory-pressure hang would add to `Unsafe Shutdowns: 200` (capture line 196), but that counter is cumulative and undated. SH6 must not be read or written as kill, OOM or earlyoom evidence, and must not be offered to mori as one.
   - The retained journal itself lives on the same btrfs, as the `/var/log` subvolume `@log` (capture line 23). That is a substrate fact, not an overlap.

6. [obs] The host has two NVMe drives of the same model, and their kernel names swapped between the last two boots. The C1 capture measures only one of them.
   - `cat /sys/class/nvme/nvme{0,1}/model` gives `WD_BLACK SN8100 1000GB` for both, with firmware `830ZRR02` for both. Their serial digests differ: sha256 prefixes `95acafc91a0b` and `413f2751ae30`. The serials themselves were not recorded.
   - `lsblk` (exit 0) shows `nvme0n1p2 crypto_LUKS` backing `root` (btrfs `/`, `/home`, `/var/cache/pacman/pkg` and `/var/log`), `nvme0n1p1 vfat /boot`, `nvme1n1p1 xfs /tmp` and `nvme1n1p2 xfs /fast`.
   - `findmnt -T /fast/scratch` gives `/fast /dev/nvme1n1p2 xfs 070be1ea-…`. That is the fleet scratch root.
   - In the kernel journal (user-readable, `journalctl -k -b <n> -o cat`):
     - boot 0 (`6a7f4fdf…`, from 2026-10-22 04:55 -03) has "nvme nvme0: pci function 0000:02:00.0" and "nvme nvme1: pci function 0000:15:00.0";
     - boot -1 (`3e7084f4…`, 2026-10-20 09:57 to 10-22 04:54 -03) has "nvme nvme0: pci function 0000:15:00.0" and "nvme nvme1: pci function 0000:02:00.0";
     - boots -5 to -2 have no such lines [unk why].
   - Mori corroborates this independently. On 2026-10-21, during boot -1, it recorded "/tmp moved from tmpfs to xfs on nvme0n1p1" (`mori-shokunin/corpus/evidence/drift-classification-r20.json:263`) and `io_avg_since_boot=dm-0:… nvme0n1p1:…` (`mori-shokunin/corpus/evidence/baseline-r20-20261021T1051Z.json:13`). Today `/tmp` is `nvme1n1p1`.
   - [inf] Assuming the PCI topology is unchanged, the root drive (PCI `0000:02:00.0`) was `nvme1` in boot -1 and is `nvme0` now. The capture is internally consistent, because capture line 32 (`└─nvme0n1p2 part  crypto_LUKS 929.5G`, unique token `crypto_LUKS`) ties `/dev/nvme0n1` to the LUKS root in the capture's own boot. But a later re-measurement of `/dev/nvme0n1` can read the other drive.
   - [inf] The second drive (XFS `/tmp` and `/fast`) is outside SH4 to SH6. XFS is not covered by btrfs scrub or by the btrfs counters, and its NVMe health log is not in the capture.

7. [inf] Ownership for each SH row. "Tsukuroi" means the core OS substrate in `PROVINCE.md:5-14` (driver and firmware plane, systemd timers, journal and boot triage); mori's own refusal at `mori-shokunin/PROVINCE.md:12-14,289-290` confirms it.

   | Row | Owner | Shared evidence | Sibling owner | Why |
   |---|---|---|---|---|
   | SH1 btrfs per-device error counters, sysfs `error_stats` versus `btrfs device stats` | tsukuroi | yes, mori S079 is the same `sysfs.c` bytes (finding 3) | none | Kernel filesystem error state is OS substrate; mori read that file for qgroup flags only. |
   | SH2 counters persist until reset; dated incident only from the kernel log line | tsukuroi | no | none | Kernel journal triage is tsukuroi core (`PROVINCE.md:11`). Fleet or wave timing of a dated line, if ever asked, is ADJ-08. |
   | SH3 what scrub verifies and repairs by profile (`single` data, `dup` metadata and system) | tsukuroi | partial: the `/sys/fs/btrfs/<uuid>/allocation/` tree the capture lists for profiles also carries the chunk fill that mori forbids thresholding (`mori-shokunin/SKILL.md:415-418`) | none | Profiles and repair ability are filesystem mechanism. The entry must not present chunk allocation as free space; capacity is mori's runway. |
   | SH4 this host's scrub record: no stats, `btrfs-scrub@-.timer` disabled | tsukuroi | no | none | systemd timers and unit files are tsukuroi core (`PROVINCE.md:10-11`). Enabling the timer or starting a scrub is an operator action. The statement covers the root btrfs (UUID `1d02a454-…`) only, not XFS `/tmp` or `/fast`. |
   | SH5 how `smartctl` derives the NVMe health verdict | tsukuroi | no | none | Device health belongs to the driver and firmware plane (`PROVINCE.md:12-13`); no sibling names SMART. It covers the drive at capture `/dev/nvme0n1` (root, PCI `0000:02:00.0`); the other drive is unmeasured. |
   | SH6 NVMe lifetime counters are cumulative | tsukuroi | yes, the same rule as ADJ-04 ("cumulative counters are not dated incidents", `PROVINCE.md:49`) | none | It must not be offered as OOM, kill or earlyoom evidence (finding 5). It has the same device-binding limit as SH5. |

8. [inf] Draft adjacency row for the entry, in the ADJ table style of `PROVINCE.md:44-52`. ADJ-01 to ADJ-07 do not cover it: ADJ-04's trigger is host pressure or a kill signal, not storage integrity.

   | ID | Finding / boundary trigger | Tsukuroi retains | Next analysis recipient | Minimum handoff evidence | Ownership source |
   |---|---|---|---|---|---|
   | ADJ-08 | A storage-integrity finding (btrfs device error counter, scrub record, NVMe health verdict or lifetime counter) is asked to explain fleet disk runway, a capacity alarm, a wave stall or an unexpected reboot | btrfs error counters and their dated kernel lines, scrub record and timer state, NVMe health derivation and lifetime counters, all read-only; cumulative counters are not dated incidents and are not kill or OOM evidence | mori | Capture time, boot id, the drive named by PCI address and mount, with the kernel name `nvmeN` given only as per-boot; exact read-only command, exit code and observed value; cumulative counter kept separate from a dated kernel line. Request correlation with runway or wave evidence, not a claim that a wave caused an error or an unsafe shutdown | `../mori-shokunin/PROVINCE.md:10,12-14,26,289-290` @ `21386b9ccb63` (sha256 `d0c13748…`); `../mori-shokunin/SKILL.md:415-418` |

   The entry should also carry one boundary line: "Capacity and chunk fill are mori's runway; this entry reports filesystem and device integrity only and grants no scrub, trim, reset or timer change."

9. [inf] A prepared packet for mori (state `prepared`; not reported, because seats may not message siblings and the integrator routes it). Mori's `io_avg_since_boot` and drift comparator key the drive by its kernel name, taken from the `df` source and `/proc/diskstats` (`mori-shokunin/tools/mori-census.sh:1872-1886`). That name changed for the same `/tmp` partition between boot -1 (`nvme0n1p1`) and boot 0 (`nvme1n1p1`), per finding 6. Tsukuroi keeps the enumeration fact, which belongs to the driver plane. Whether that name change produces a spurious drift token is mori's census question.

## Proposed move (one, bounded)

Bind SH4 to SH6 to stable identity, and name the unmeasured drive.

- Each of SH4, SH5 and SH6 states the identity it measures:
  - SH4: the root btrfs, by filesystem UUID `1d02a454-c549-4a35-b567-89d60902af8e` (capture line 120, `UUID:`).
  - SH5 and SH6: "the drive holding the LUKS root in the capture's boot". The capture pointer is line 32 with token `crypto_LUKS`.
- Add a limit sentence: "kernel NVMe names are assigned per boot and swapped between boot -1 and boot 0 on this host; the second WD_BLACK SN8100, which holds XFS `/tmp` and `/fast`, is unmeasured, and XFS is outside btrfs scrub."
- The entry carries ADJ-08.
- Optional verification hook for the S133 seat or the L1: the S133 snapshot's sha256 should equal `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`, which mori's S079 independently recorded as `ce146120f29ac29c`.

- Affected axes:
  - depth (C1, declared): more precise scope, with no row-count change;
  - adjacency (held at 8): a new owner-handoff row backed by sibling quotes;
  - calibration (C2): no change. No checker rule, row id, verdict or counting command changes, and `verified_rows` is unaffected.
- Second-order effects:
  - Runtime and substrate: a later `/dev/nvme0n1` read may hit the `/fast` drive, so any trend between rounds ("unsafe shutdowns rose from 200") would compare different drives unless it is bound by PCI address.
  - Contract: SH5 and SH6 stay counted from the frozen capture alone. The boot-swap evidence is journal evidence from this wave, not a capture pointer.
  - Verification: the S133 digest cross-check is free, using bytes another lane already pinned.
- Risks:
  - [inf] The swap inference assumes the PCI addresses `0000:02:00.0` and `0000:15:00.0` are stable across boots.
  - [unk] Boots -5 to -2 lack the "pci function" lines, so the swap frequency is unknown.
  - Stating PCI addresses in the entry adds a fact the frozen capture does not contain. Mark it as wave evidence, or keep the UUID and `crypto_LUKS` binding only.
- Verification:
  - `journalctl -k -b -1 -o cat | rg 'nvme nvme[01]: pci function'` and the same for `-b 0` should show the swapped mapping.
  - `lsblk -o NAME,FSTYPE,MOUNTPOINTS` should show XFS `/tmp` and `/fast` on `nvme1n1`.
  - `sha256sum .ufo/waves/round-26/sources/S133.*` should equal the digest above once S133 lands.
  - `python3 tools/check-storage-health.py --revision <REV>` should be unchanged by the wording.

Contradictions stated, not smoothed:
- The goal text says "one device". That is true for the btrfs filesystem (one devid), but the host has two NVMe drives.
- Mori's 2026-10-21 evidence names `/tmp`'s drive `nvme0n1p1`, while the frozen capture names the root drive `nvme0n1`. Both are correct for their own boot.

## Addendum (14:02Z): full scan of uncommitted sibling files

The full scan of uncommitted and untracked sibling files finished. Almost every hit is the directive text about the `btrfs-overlayfs` hook copied into kagi sandbox copies and tabi spawn results. Kagi's `ClockS027-artifacts/chlog.body` matches only "copy-on-write (in case of btrfs and XFS)", which is changelog text. There are two other hits, and neither is storage integrity:

- [obs] Souji: `souji-shokunin/census/operator-sweep-20261019/fresh-120min.txt` lists `/tmp/xsnap*/…/sudoers/nvme1-scratch-sudoers`. That is the name of a sudoers file in snapshot listings. It is operator configuration residue, not a device finding, and tsukuroi does not read its contents.
- [obs] Tabi: `tabi-shokunin/.ufo/waves/round-22/w2b/RowOutcome06.md:20` (mtime 2026-10-21 14:23 -03, during boot -1) records that "`/tmp` was 100 % full (`/dev/nvme0n1p1 128G 128G 352K 100%`)". This adds to finding 6. The same 128G XFS `/tmp` partition was `nvme0n1p1` in boot -1 and is `nvme1n1p1` now, which confirms the rename independently of mori. A full `/tmp` is a capacity event, so it belongs to mori's runway (`mori-shokunin/PROVINCE.md:10`) and is not part of C1.

The verdict and the ownership table do not change.

## Addendum (14:10Z): where the whole-tree hits in mori come from

A whole-tree scan of the sibling folders counted about 1.4 million storage-term hits in mori, far more than any other lane (kagi has about 111 thousand, the rest fewer). I did not get a per-file breakdown; that job was still running at write time. [inf] The size of mori's tree explains the count. `du -sh` gives `.scratch` 646M, `.ufo` 346G and `corpus` 2.2M. The `.ufo` folder holds `worktrees/`, `interactive-sessions/` and `waves/`, which are fleet session and copy material, not storage-integrity work.

[obs] `df -P -h /` gives `/dev/mapper/root 930G 175G 750G 19%`. So the `du` total of 346G for mori's `.ufo` is larger than the whole root filesystem's used space. [inf] Most of it must be extents shared through btrfs reflinks or snapshots, for example the task-isolation worktrees whose `btrfs` backend kumitate documents. This is a capacity and accounting question for mori's runway, and for souji if it is about reclaiming space. It is not part of C1. The only lesson for the entry is that on this btrfs, a `du` total is not used space, so no SH row should state sizes taken from `du`.

## Addendum (14:15Z): per-file breakdown of mori's hits, and a full-digest match for S133

[obs] The breakdown finished, cut short at 600 s, so it is partial. Hits by subfolder of mori's `.ufo`: `worktrees/round-19` 471,260 (copies inside session worktrees such as `ContentGate`, `FreezeMetadata`), `waves/round-23` 10,807, `worktrees/round-18` 1,857, and `waves/round-21` to `round-15` a few hundred each. The files with the most hits are mori's round-23 kernel source snapshots: `S081-fs_btrfs_inode.c` (2,265), `S080-fs_btrfs_qgroup.c` (936) and `S079-fs_btrfs_sysfs.c` (680). Next come round-23 c2 measurement JSON files (about 170 to 178 hits each). All of this is qgroup and quota work from round 23 plus worktree copies. None of it is error-counter, scrub or SMART work, so the verdict stands.

[obs] Mori's tracked snapshot `.ufo/waves/round-23/evidence/sources/S079-fs_btrfs_sysfs.c` (last commit `c1e8b81`, 2026-10-21T15:01:27-03:00) has sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`. That equals my fetch from this wave byte for byte. Finding 3 compared only a 16-character prefix; this is a full-digest match. For the S133 seat, the S133 snapshot must hash to this value, and a committed copy of the same bytes from another lane already exists to compare against. The rows stay separate.

Scope: read=sibling PROVINCE.md and corpus/README.md (20 lanes), mori PROVINCE.md, SKILL.md:405-434, corpus/SOURCES.md:85-87, round-26 contract and SCORECARD declaration, census device lines, r20 evidence, tsukuroi PROVINCE.md, SCORECARD.md:874-905, round-26 capture.txt, the round-26 sources directory listing, and read-only git log -5 and status of each sibling; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/ConnSiblingOverlap.md, /fast/scratch/hyaku/tsuku26/ConnSiblingOverlap/sysfs-v7.2.c; executed=rg, git log -5 -p and git --no-optional-locks status per sibling, git show and rev-parse (read-only), sha256sum, lsblk, findmnt, systemctl list-unit-files and list-units, cat of /sys/class/nvme/*/{model,firmware_rev,serial} (serial hashed only, never printed), journalctl -k (user, read-only), curl of raw v7.2 fs/btrfs/sysfs.c, rg over uncommitted and untracked sibling files, stat of tabi RowOutcome06.md, du -sh of mori .scratch/.ufo/corpus, df -P -h, ls of mori .ufo, rg -c over mori's tree (partial, 600 s), sha256sum of mori's S079 snapshot, git ls-files and git log -1 on it
Model: cursor/default (as exposed by the host workstation context)
Installs: none
