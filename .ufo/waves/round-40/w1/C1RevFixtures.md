VERDICT: supports

Item C1-7 — review of the five round-40 selftest cases (R39-FIXTURE-MONOCULTURE repair) at lane tip
f951f288483c1af0cef4afd458488b84cf7a2165. All five expectations are correct per the round-39 rule
(census header) and the code order; all five mount tables are valid /proc/self/mounts lines and every
btrfs option string is spelled exactly as the kernel emits it on this host; every case kills at least
one of the nine frozen counter mutants, so none tests nothing new. Two minor realism defects in
fields the census never reads (a `UUID=` spec, a `comment=` option) are reported below with proposed
text. Receipts: .ufo/waves/round-40/w1/C1RevFixtures/receipts.txt.

## Evidence

### The five cases
`grep -n 'R40-C1' tools/tsukuroi-census.sh` → checks at :3015, :3023, :3029, :3034, :3041; fixtures
written at :3012-3014, :3018-3022, :3026-3028, :3032-3033, :3037-3040. Selftest at the tip:
`TMPDIR=/fast/scratch/hyaku/tsukuroi-r40/C1RevFixtures bash tools/tsukuroi-census.sh --selftest` →
`TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)` (34.75 s wall).

Per-case probes (probe_storage_arm inputs only — TSUKUROI_BTRFS_SYSFS + TSUKUROI_PROC_MOUNTS pointed
at copies of the fixture tables, census run live otherwise; receipts file has the exact lines):

| probe | observed STORAGE line |
|---|---|
| varied-home | `state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` |
| varied-multi | `state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` |
| btrfs-in-path | `state=HEALTHY filesystems=0 devices=0 nonzero=0` |
| fstype-case | `state=HEALTHY filesystems=0 devices=0 nonzero=0` |
| root-unreadable-mounted | `state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=root:unreadable` |

Each equals the case's WANT_RE (:3016, :3024, :3030, :3035, :3042).

### 1. Mount-line syntax and btrfs option spelling — valid, kernel-real
- Fields: every fixture line carries the six /proc/self/mounts fields (spec, mountpoint, fstype,
  options, dump=0, passno=0). Host reference: `awk '{print NF}' /proc/self/mounts | sort | uniq -c`
  → `33 6` (33 lines, all 6 fields).
- btrfs option spelling: this host's live /proc/self/mounts (accessed 2026-10-26) emits
  `/dev/mapper/root / btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@ 0 0`
  — so `compress=zstd:3`, `ssd`, `discard=async`, `space_cache=v2`, `subvolid=<n>`, `subvol=/…` are
  all kernel-emitted spellings, and the fixtures use exactly these: :3013
  `rw,relatime,ssd,discard=async,space_cache=v2,subvolid=5,subvol=/`; :3021
  `ro,noatime,compress=zstd:3,subvolid=263,subvol=/machines`; :3039
  `rw,relatime,subvolid=5,subvol=/`. subvolid=5/subvol=/ is the top-level subvolume — valid;
  /var/lib/machines (:3021) is a real systemd mountpoint.
- Octal escapes: no fixture field contains a character the kernel escapes (space/tab/newline/
  backslash in fields 1–2), so none is needed or misused. Extra probe (not a census case): a table
  line `/dev/sda1 /mnt/my\040dir btrfs rw,relatime 0 0` still resolves field 3 — the arm returned
  `BLOCKED … detail=mounts:btrfs-without-sysfs` — so the fstype check is robust to kernel-style
  escapes and the absence of an escape fixture hides nothing.

### 2. Each expectation matches the round-39 rule and the code order
Rule (census :365-369): an absent root, or one holding no fsid entry, reads HEALTHY 0/0/0 only when
the mount table lists no btrfs mount; a listed btrfs mount is BLOCKED
detail=mounts:btrfs-without-sysfs; an unreadable, not-regular or empty table is BLOCKED
detail=mounts:unreadable; "A root with fsid entries never reads the table." Unlistable root:
:377-378 prescribes BLOCKED `root:unreadable`.

- Case 1 (:3011-3016, absent root — fx_default creates no $FX/btrfs, :2022-2048): one btrfs line
  mid-table → BLOCKED mounts:btrfs-without-sysfs. Code: table read guarded by
  `if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]` (:1906), fstype compared exactly at :1913, detail
  appended at :1915. Probe reproduces the expected line. ✓
- Case 2 (:3018-3024, root holds features/ — no fsid entry, :3019): same rule path; read-only btrfs
  mid-table among four lines → BLOCKED mounts:btrfs-without-sysfs. ✓ (Wording nit: the label says
  "empty root" but the root holds features/; the rule's phrase is "one holding no fsid entry"
  (:365) — the expectation is right either way.)
- Case 3 (:3026-3030): btrfs text in the device (`/dev/disk/by-label/btrfs-old`), mountpoint
  (`/mnt/btrfs-backup`) and options (`comment=btrfs`) of ext4 lines; fstype field is ext4 → mt=0 →
  HEALTHY 0/0/0, no detail. ✓
- Case 4 (:3032-3035): fstype `BTRFS` fails the exact compare `[ "${fst:-}" = btrfs ]` (:1913) →
  HEALTHY 0/0/0. ✓
- Case 5 (:3037-3043): `chmod 000` root → :1869-1872 sets blocked=1 with detail `root:unreadable`;
  the table read at :1906 requires `blocked -eq 0`, so the btrfs line in the table (:3039) is never
  consulted — exactly one reason, `detail=root:unreadable`. The expectation follows from the code
  order; the probe reproduces it with no second reason. ✓

### 3. Newness — every case kills frozen mutants; none is dead weight
tools/score-selftest-literals-r40.py MUTANTS (:68-88) are literal-keyed guards. The round-39 fixture
set (fxmt :2975 = `/dev/mapper/root / btrfs rw,noatime,subvolid=256,subvol=/@ 0 0`, always last,
lowercase; root:unreadable fixture :2970-2975 with a btrfs-free table) makes all nine behave
identically to baseline — the declared monoculture (survivors 9 at base). Kill map:
- Case 1 kills M1 (keyed `'/dev/mapper/root'`), M2 (`' / btrfs '`), M4 (`subvolid=256`),
  M8 (`subvol=/@`), M9 (`tail -n 1` — btrfs not last).
- Case 2 kills the same five (redundant kills; its unique value is the variation breadth the claim
  declares: read-only btrfs, four-line table, subvol=/machines, non-fsid root).
- Case 3 kills M3 (keyed `*btrfs*`) and M5 (`grep -c btrfs`) — the anti-substring arm.
- Case 4 kills M6-b (fstype casefold, counter :77) — the case-sensitivity pin.
- Case 5 kills M7 (guard drops `&& [ "$blocked" -eq 0 ]`) — the ordering pin.

## Findings (minor; none affects an expectation)

F1 (minor realism) — :3020 filler `UUID=0b1c /boot vfat rw,relatime 0 0`: a real /proc/self/mounts
never carries a `UUID=` spec (libmount resolves it before mount(2)); this host's table has 0/33 lines
starting `UUID=`, and `0b1c` is not a valid 8-4-4-4-12 UUID. The census reads only field 3, so the
expectation is unaffected. Proposed text (the host's real /boot line shape, /proc/self/mounts
2026-10-26):
    '/dev/nvme0n1p1 /boot vfat rw,relatime,fmask=0077,dmask=0077 0 0'

F2 (minor realism) — :3028 `comment=btrfs` on the ext4 line: `comment=` is a userspace fstab
annotation — mount(8) does not pass it on (mount.8:2675 lists `comment` among the options not passed
to the mount.<suffix> helpers; man7.org/linux/man-pages/man8/mount.8.html and the kernel ext4 admin
guide, docs.kernel.org admin-guide/ext4: comment is a userspace annotation, "mount does not pass it
to the kernel" — both accessed 2026-10-26), and ext4 rejects unrecognized options at mount time, so
no real table can contain it. The device and mountpoint carriers are realistic (labels and directory
names are arbitrary); the options carrier is synthetic — and no real ext4 option can carry the
substring, so the options-field guard is inherently synthetic. Proposed text (drop the synthetic
carrier; the case title's "device, mountpoint or options" still holds):
    '/dev/disk/by-label/btrfs-old /mnt/btrfs-backup ext4 rw,relatime 0 0'
  (If an options carrier is wanted, a realistic one is an overlayfs mount:
  `overlay /mnt/ovl overlay rw,lowerdir=/btrfs-old,upperdir=/mnt/btrfs-backup/u,workdir=/mnt/btrfs-backup/w 0 0`.)
  Caveat: any census text change needs a fresh C1 commit and a counter re-run; no frozen mutant
  targets fixture strings (grep of score-selftest-literals-r40.py for the fixture strings hits only
  :77 M6-b, which targets the compare line of code).

F3 (note, no change requested) — :3033 `BTRFS` fstype: the kernel registers and emits lowercase
`btrfs` (host table), so an uppercase fstype is not kernel-emittable; the case is a parser-contract
pin for user-supplied tables (TSUKUROI_PROC_MOUNTS accepts any path, :408/:463) and kills M6-b —
keep it. A one-line comment noting that it pins the census's own contract, not kernel behavior,
would prevent a future "realism" cleanup from deleting it.

## Not done
- Did not run tools/score-selftest-literals-r40.py end-to-end (13 selftests, ~75 s) — executor seats
  own that run; I read its MUTANTS/NEUTRAL tables statically (:60-95) for the kill map.
- Did not mount a real btrfs filesystem (no unprivileged btrfs device/image path taken);
  option-spelling realism rests on the host's live /proc/self/mounts emission quoted above.
- Tooling authorization unused: no tools installed.
- Scratch /fast/scratch/hyaku/tsukuroi-r40/C1RevFixtures removed after receipts were copied.
