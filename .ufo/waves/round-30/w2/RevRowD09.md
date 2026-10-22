# RevRowD09 — C1 row D09 falsification review

Verdict: holds.

Row under attack: corpus/knowledge/btrfs-space-r30.json D09 (S152, snapshot line 398, capture line 98, value 690922455040) and SKILL.md line 2614 `| [R30-D09] ...`.

## Findings

1. Source/snapshot byte-equality confirmed. Refetched https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-filesystem.rst with plain curl (HTTP 200, 24932 bytes); sha256 a0ce33f5babd8521f0956cf6ce934412c2ab2d6e93f32c2c08ff9ae63f8597bc is identical to the committed snapshot .ufo/waves/round-30/w1/ScribeSrcFsUsage/S152-btrfs-filesystem.rst (same sha256). Refetched bytes saved at .ufo/waves/round-30/w2/RevRowD09/S152-refetch.rst. [obs]

2. Quote verified verbatim on the refetched bytes: `sed -n '398p' | grep -cF 'Device unallocated* -- the remaining unallocated space for future'` returns 1. The documented semantics support the statement: line 395-397 define "Device allocated" as "sum of total space allocated for data/metadata/system profiles" and line 398-399 define "Device unallocated" as "the remaining unallocated space for future allocations (difference of the above two numbers)". So Device unallocated = Device size - Device allocated = device size - (data + metadata + system disk_total) exactly as D09's parenthetical states. [obs]

3. Arithmetic and dual confirmation. Capture line 98 derives 998037782528 - (229789138944 + 77309411328 + 16777216) = 690922455040; recomputed independently, correct, and the sum 307115327488 equals the "Device allocated:" field the unprivileged `btrfs filesystem usage -b /` printed at capture (.ufo/waves/round-30/w1/ExecHostCapture/btrfs-filesystem-usage.out.txt line 3), whose line 4 prints "Device unallocated: 690922455040" directly. The sysfs derivation and the progs output agree to the byte. [obs]

4. Live re-read, no drift in the operands. At 2026-10-22T21:39:54Z (vs capture 2026-10-22T21:16:37Z, capture line 11): data/disk_total 229789138944, metadata/disk_total 77309411328, system/disk_total 16777216, device size 998037782528 — all identical, so unallocated is still 690922455040. Only metadata/bytes_used moved (35372056576 -> 35382575104, +10.5 MB), which does not enter the unallocated formula. [obs]

5. "A new metadata chunk could still be allocated at capture time" is supported and safe. Metadata is DUP (metadata/disk_total 77309411328 = 2 x total_bytes 38654705664, capture lines 53/67; chunk_size 1073741824, line 52), so one new metadata chunk needs ~2 GiB raw, far below 690 GiB unallocated. Even accounting for the kernel-side reservation in .ufo/waves/round-26/sources/S132.c (avail excludes the [0,1M) reserved range and sub-stripe remainders), ~690 GiB - 1 MiB still passes; the progs-vs-kernel 1 MiB definitional gap is immaterial at this magnitude. The SKILL operator decision "no action" is read-only — no write by the lane. [obs/inf]

6. New knowledge at fbfec6bd confirmed. `git grep` at fbfec6bd for "690922455040" and "998037782528": zero hits. `git grep "disk_total"` outside round-26/29 sources hits only .ufo/waves/round-26/capture/capture.txt lines 56/77/98, which are `ls` listings of sysfs attribute names, not values or the unallocated derivation. The only prior "Unallocated" mention (round-26 S128.rst lines 174/183/198) is btrfs-device.rst's per-device field in a different table. The host value, the sysfs-to-progs equality, and the derivation are all new. [obs]

7. Minor nits, not defects [inf]: (a) the parenthetical equates whole-device byte size with progs "Device size"; they coincide here only because Device slack is 0 (usage.out.txt line 6), which the capture shows, so the statement is accurate for this host; (b) "could still be allocated" also rests on the DUP raw requirement, which is in the capture but not among the SKILL line's two cited lines — acceptable as the cites point at the evidence file, not every operand. No wording change required.

Scope: read=lane JSON/SKILL/SOURCES/capture/snapshot, refetched S152, live sysfs, git grep at fbfec6bd; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevRowD09.md and .../w2/RevRowD09/S152-refetch.rst; executed=curl, sha256sum, sed/grep reads, cat of /sys/fs/btrfs files, lsblk, date, git grep/show (read-only)
Model: not exposed
Installs: none
