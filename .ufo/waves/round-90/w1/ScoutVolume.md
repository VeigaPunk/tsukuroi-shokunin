# Seat ScoutVolume — round-90 w1, C2 volume half

**Lane revision measured.** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` `master` = `9b4d9cda5018bab51860129656155bf96c27bedd`
(the C2 entry with rows TV1-TV9 already landed at that revision; the C1 candidate gate is `ce89df93`, the freeze
commit is `6511437e`, the pre-round tip is `c0f91856`).  This seat wrote **no lane file**: no edit to
`corpus/`, `tools/`, `SCORECARD.md`, or any other tracked path.

**Deliverables (this seat's own wave dir).**
- `.ufo/waves/round-90/w1/ScoutVolume/proposed-rows.md` — 12 candidate rows SV1-SV12 for
  `corpus/knowledge/limine-tpm-volume-r90.md`, 38 quotes, every one machine-verified as a substring of the
  whitespace-normalised raw line range (`receipt-quote-verification.txt`: `BAD 0 VERIFIED 38`).
- `.ufo/waves/round-90/w1/ScoutVolume/proposed-sources.md` — 4 draft `corpus/SOURCES.md` rows **S373-S376**
  (S372 is taken by the L1's TCG-spec row; my rows are renumbered accordingly) plus the sha256/URL table for the
  three files the lane does not yet pin.
- Receipts in the same dir: `receipt-upstream-vs-clone.txt`, `receipt-pins-vs-clone.txt`,
  `receipt-src-c2-vs-clone.txt`, `receipt-quote-verification.txt`, `receipt-guid-harness.txt`,
  `receipt-host-observations.txt`.

## Verdict per check

| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | Do `guid()`/`uuid()` match a GPT partition GUID, a filesystem GUID, or both? | **GPT partition GUID only, in practice** — but the `guid_valid` arm of the lookup is a *different* GUID (the whole-medium GPT **disk** GUID), not a filesystem GUID | SV1, SV2, SV4a/b, SV5, SV6, SV7, SV8, SV9, SV10 |
| 2 | Does a FAT volume serial ever count as a `uuid()`? | **No** — `fs_get_guid()` returns false for every filesystem, so no filesystem UUID is ever recorded; and `86D8-C3F6` is not GUID-shaped, so the parser rejects it before any lookup | SV3, SV5, SV36 + harness (`string_to_guid_mixed("86D8-C3F6") ok=0`) |
| 3 | Is `fslabel` case-insensitive, and does the FAT label count? | **Case-insensitive** (`strcasecmp`); the FAT label comes from the root directory's **volume-label entry** (attribute `0x08`), not the BPB label field, and the ISO 9660 label from the PVD identifier | SV7, SV20-SV23, SV35 |
| 4 | How is `boot(N)` numbered, and does `boot(1)` name this ESP? | **1-based over GPT entry slots, gaps preserved**; `boot(N)` = partition N of the *boot volume's drive*; empty-root `boot()` = the boot volume's own partition | SV5, SV6, SV11, SV11b, SV12, SV13-SV15 |
| 5 | What does an unknown GUID do on an `efi` path? | **Silent NULL** -> `efi: Failed to open image` panic (chainload.c 434-435) | SV9, SV31, SV32 |
| 6 | Which URIs would name **this host's** ESP? | `boot():/...` and `guid(<ESP PARTUUID>):/...` (and `uuid()` with the same text). `fslabel()` **cannot** (label empty). `hdd()`/`odd()` **cannot** be written from Linux's names — their drive index is Limine's own counter | SV10, SV11, SV12 |
| 7 | Byte order: is the `lsblk` PARTUUID text the text a `guid()` URI must carry? | **Yes — now proven, not inferred.** `guid_to_string` and `string_to_guid_mixed` are exact inverses on GUID text (50000/50000 random texts round-trip; `string_to_guid_mixed(guid_to_string(x)) == x` for 50000 random byte patterns; 0 collisions in 20000) | `receipt-guid-harness.txt` |

## Two corrections to the landed rows (for the L1 to decide)

1. **TV5's phrasing of the two match arms is misleading.** `volume_get_by_guid` compares `volume->guid` and
   `volume->part_guid` (part.s2.c 1037-1044). TV5 calls the first arm "a volume's filesystem GUID", but
   `fs_get_guid()` returns false for every filesystem, so `guid_valid` is false on every *partition*; the only
   volume where the first arm can be true is the **whole medium**, and there it holds the GPT **header disk GUID**
   (`gpt_get_guid` -> `header.disk_guid`, part.s2.c 495; set at disk.s2.c 986-988). So the two arms are
   "GPT disk GUID" and "GPT unique partition GUID" — neither is a filesystem GUID. Suggested wording in SV1/SV4.
2. **TV8's "GPT partitions are numbered from 1" needs the gap caveat.** `ret->partition = partition + 1` where
   `partition` is the GPT **entry slot index**, and the enumeration loop skips empty slots (`NO_PARTITION`) without
   renumbering (disk.s2.c 1010-1013) — so the numbers are slot numbers with gaps, not a dense count of existing
   partitions. MBR primaries are likewise slot-based and logicals are 5+ (`partition + 4 + 1`, part.s2.c 847).

**Also new, and operator-relevant:** the host mapping (SV10) is stated in the landed TV6/TV8 as two separate
inferences; SV10 states it once, with the reason each of the seven resources can or cannot name the ESP.

## Open / unresolved

- Limine's **drive index** for `hdd(d:p)`/`odd(d:p)` is not observable from Linux (it is Limine's own enumeration
  counter: BIOS 0x80+ probe order, UEFI `LocateHandleBuffer` order; `hdd_indices`/`optical_indices` start at 1 and
  the two spaces are disjoint). No `hdd()`/`odd()` URI can be authored from this host's `lsblk` output.
- Nothing was booted and no Limine-side volume enumeration was observed; the ESP identification rests on the
  `LoaderDevicePartUUID` efivar (Limine writes it from `boot_volume->part_guid`) plus the `lsblk`/`blkid` PARTUUID.
- The FAT-serial question is answered for the *whole* class of filesystems, but I did not enumerate every
  filesystem Limine can open beyond FAT and ISO 9660 (those are the two `fs_get_label`/`fopen` back ends in
  file.s2.c 13-25 and 58-63).
- Upstream drift past v12.9.4 was not examined here (that is the drift seat's scope).

## Refused / not done

- **No `sudo`**, no write to `/boot`, `/efi`, `/etc`, `/usr`, `/var`, `/sys`, `/proc`; `/boot/limine.conf` was not
  read (permission denied without root) — the r90 host receipt is the authority for its contents.
- No `git`/`jj` mutation, no commit, no branch or tag created; the clone is a scratch clone under
  `/fast/scratch/hyaku/tsukuroi-r90/ScoutVolume/` (removed on exit).
- No `pacman` transaction (none needed); nothing installed — `gcc 16.2.1` was already present and was used only to
  compile a throw-away harness from the pinned upstream `guid.c` in scratch.
- No LANE file was edited; no `agent://all` broadcast; no subagent dispatched.

## Host mapping used (all read-only)

ESP = `/dev/nvme0n1p1`, PARTN 1, PARTUUID `b80445be-18ee-45e6-9a30-14339ea785a7`, vfat, BPB volume serial
`86D8-C3F6`, **no FAT label**, mounted `/boot`; EFI `LoaderDevicePartUUID` = `b80445be-18ee-45e6-9a30-14339ea785a7`,
`LoaderInfo` = `Limine 12.9.4`; host package `limine 12.9.4-1`.  Every `path:` in `/boot/limine.conf` is
`boot():/...` (r90 host receipt lines 47-72).
