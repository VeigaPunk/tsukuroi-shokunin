VERDICT: defect-found

Seat AsmGate, round 42 w1, item A-1 (assimilation; read-only package
`/home/vgpnk/Projects/shokuknow/merge/tsukuroi`). Scope: the merge report's
btrfs entries and the two named staged files
`knowledge/corpus/knowledge/btrfs-ioctl-surface-r27.md` and
`knowledge/corpus/knowledge/btrfs-filesystem-troubleshooting-bilingual-r26.md`;
every scrub-touching proposition (status file, scrub ioctl, progress, limits)
checked against the pinned `.ufo/waves/round-42/frozen/src/scrub.c`, the
PROVINCE scope, and `corpus/QUALITY.md`. Receipts:
`.ufo/waves/round-42/w1/AsmGate/receipts.txt` (commands and observed outputs).

## Check baseline

- Pinned source verified: `sha256sum -c SHA256SUMS` in `.../frozen/src/` →
  `scrub.c: OK`, `CHANGES: OK`; `FETCH.txt:2-3` records the v7.1 tag fetch
  (scrub.c ← `cmds/scrub.c`, fetched 2026-10-26). Receipt 1.
- Local corroboration header: `/usr/include/btrfs/ioctl.h` from installed
  btrfs-progs 7.1-1 (`pacman -Q btrfs-progs` → `btrfs-progs 7.1-1`), i.e. the
  same upstream release as the pinned scrub.c. These header bytes are not part
  of the round's frozen set; used and labeled as corroboration only.
- Bounded sweep for scrub text in the whole package: case-insensitive `scrub`
  → only `SOURCES.append.md` and
  `knowledge/corpus/knowledge/ext4-journal-guarantee-r32.md` (receipt 3).
  Neither named staged entry contains the word "scrub" at all (receipt 2), and
  neither carries a `## QUALITY check` section (receipt 4). The merge report's
  other btrfs rows (`btrfs-space-repair-amend-2026-10-23.md`,
  `eastern-tradition-host-docs-r44.md` via the S342 pointer fix) contain no
  scrub text per the same sweep.

## Entry 1 — btrfs-ioctl-surface-r27.md (staged; S223 tier A, kernel v7.2 uapi; SOURCES.append.md:30)

P1 — the nine-row ioctl table (BTRFS_IOC_SNAP_CREATE nr 1 … SNAP_DESTROY_V2
nr 63, GET_SUBVOL_INFO nr 60) and "the ioctl magic is 0x94".
**ADMIT CANDIDATE.** All nine numbers and the magic verify against the local
same-release header: `/usr/include/btrfs/ioctl.h:34` (magic) and :927, :956,
:958, :973, :975, :977, :978, :1046, :1052 (receipts 7). No scrub content; the
admit extends only as far as this seat's scrub scope reaches.

P2 — "Together they close the btrfs ioctl surface", and "the command surface
is stable and enumerable", as realized by that nine-row table.
**REJECT — falsified.** The pinned scrub.c itself drives three commands absent
from the table: `BTRFS_IOC_SCRUB` (frozen/src/scrub.c:965),
`BTRFS_IOC_SCRUB_PROGRESS` (:986, :1200), `BTRFS_IOC_SCRUB_CANCEL` (:421,
:1792). The header's define block :927-:1056 carries 63 `BTRFS_IOC_*` defines
against the table's nine; the scrub trio sits at nr 27/28/29 (header :979,
:981, :982). This is exactly the lane's Frontier surface:
`PROVINCE.md:161-163` and `:212-214` hold the scrub record (`btrfs scrub
status`, `/var/lib/btrfs/scrub.status.*`, `btrfs-scrub@.timer`) as Frontier
with no census arm reading it, and the round-42 depth rows source precisely
this path from the same pinned file — the status record's write mechanism is
scrub.c:454-543 (scrub_datafile `_`+tmp suffix; scrub_open_file
`flock(fd, LOCK_EX|LOCK_NB)` at :487; scrub_rename_file `rename` at :534).
`corpus/QUALITY.md` criterion 22 bars an exhaustive-surface claim without a
recorded bounded sweep, and criterion 9 requires the sweep behind the implied
negative ("no further ioctls"). **Flip condition:** (a) rewrite the claim to
the bounded proposition the rows support (nine selected subvolume/snapshot
ioctls), or (b) extend the table to the full define block — including
BTRFS_IOC_SCRUB/_CANCEL/_PROGRESS — and record the counting command and date
per criterion 9. Either flip converts P2 to admit; as staged it must not land.

P3 — "a caller can be identified from its ioctl number alone". **REJECT as
stated.** The table's "number" column is the nr field only, and nr is reused
inside this one block: TREE_SEARCH / TREE_SEARCH_V2 share nr 17 (:962, :964),
SET/GET/SUPPORTED_FEATURES share nr 57 (:1036, :1038, :1040), ENCODED_READ /
ENCODED_WRITE share nr 64 (:1054, :1056), SET_RECEIVED_SUBVOL(+_32) share nr
37 (:997, :1001), SEND(+_64) share nr 38 (:1006, :1010). Identity requires
magic + direction + nr (+ size), i.e. the full encoded value, not "the
number". **Flip condition:** reword to the full encoded identity or drop the
sentence; the header's own nr-reuse rows are the falsifier.

Entry-level conditions outside the four scrub categories (recorded as
admission conditions, not adjudicated here): (i) the two mask names
`BTRFS_SUBVOL_CREATE_ARGS_MASK` / `BTRFS_SUBVOL_DELETE_ARGS_MASK` are absent
from the same-release local header, which defines
`BTRFS_VOL_ARG_V2_FLAGS_SUPPORTED` instead (:55-59) — the entry cites kernel
v7.2 uapi (S223) for those names, so those bytes must be pinned/located per
`QUALITY.md` 7/21 before the mask sentences are relied on; (ii) the staged
"BTRFS_SUBVOL_CREATE_ASYNC is marked deprecated since 5.7" collapses the
header's two dates ("Obsolete since 5.15, functionality removed in kernel
5.7", :47-48) into one claim — `QUALITY.md` 66 (keep every branch the source
states).

## Entry 2 — btrfs-filesystem-troubleshooting-bilingual-r26.md (staged; S218/S219 tier B; SOURCES.append.md:25-26)

**No scrub proposition exists in this entry** (bounded sweep, receipt 2): its
propositions are the SUSE rollback precondition, the ENOSPC /
balance / delete-oldest-snapshot procedure, and subvolume quota — none of the
four scrub categories this item names.

Entry-level verdict: **CONDITIONAL ADMIT** as corpus knowledge. In-province:
`PROVINCE.md:176` keeps free-space-as-boot-precondition on this lane's side of
the round-26 split and the lane already holds the btrfs ENOSPC mechanism
ground; the entry's Boundaries section scopes the SUSE chapter as vendor
doctrine that cannot outrank the upstream English page and as a model to
check, not a host verdict; the documented balance/snapper commands remain
operator-owned remediation, matching `PROVINCE.md:215`'s boundary pattern.
S218/S219 are tier B docs rows with located section anchors (§1.15.1.1, both
localisations). **Flip conditions:** (a) the `## QUALITY check` section below;
(b) both cited anchors resolve at the entry's 180d re-fetch. **Reject
trigger:** either flip fails.

## Both entries — QUALITY.md 14 blocker

Neither staged entry carries an explicit `## QUALITY check` section evaluating
the applicable numbered criteria (grep `QUALITY` over both files → no matches,
receipt 4). `QUALITY.md` 14: "Before recording an admit for a new knowledge
entry, require its explicit `## QUALITY check` … a promised check is not a
performed check." No unqualified admit can therefore be recorded for either
entry as staged; both verdicts above are conditional on that section landing
with the entry and resolving its S-row anchors and tiers.

## Required pair (item: "at least one admit candidate and one reject")

- Admit candidate: P1 — the nine-row ioctl-number table plus magic 0x94,
  verified against the local v7.1 header (receipts 7).
- Reject: P2 — the closed/enumerable-surface claim, falsified by the pinned
  scrub.c's own BTRFS_IOC_SCRUB / _PROGRESS / _CANCEL use (scrub.c:421, :965,
  :986, :1200, :1792) and the header's 63-define block at nr 27/28/29.

## Cross-package observation (outside the two named entries, not adjudicated)

The only other staged scrub mention is `ext4-journal-guarantee-r32.md` ("a
`scrub` that verifies and can repair from a replica", "checksum + scrub +
error counters" in its btrfs-vs-ext4 comparison, citing the lane's
storage-health entry) — a general scrub-model statement, not one of the four
scrub categories of this item.

## Why this matters for round 42

The wave-2 depth rows source the scrub status record from pinned scrub.c v7.1.
An admitted entry whose stated conclusion is that the BTRFS_IOC surface is
"closed" by nine subvolume commands misstates the very surface the scrub read
path uses (SCRUB / SCRUB_PROGRESS / SCRUB_CANCEL, nr 27/28/29) — the exact
source-vs-claim mismatch `QUALITY.md` 22 exists to prevent. The defect is
confined to the entry's framing sentence; its per-row facts (P1) are correct.

## What I did not do

- Did not fetch or re-read the S218/S219/S223 URLs; tier and anchor rows are
  accepted as staged, and my verdicts do not depend on them except where
  noted.
- Did not verify the kernel-v7.2-only mask names against a pinned v7.2 header
  (the frozen set holds only scrub.c and CHANGES; the local header is
  btrfs-progs 7.1's bundled copy).
- Did not adjudicate non-scrub propositions beyond the entry-level admission
  conditions above (P3-adjacent flag claims; the bilingual entry's ENOSPC
  facts).
- No tool installs (none needed); no campaign tools run; no scratch created
  (no clone or fixture was required); writes limited to this report and its
  receipts file.

Scope: executed=read-only — sha256sum -c, cat FETCH.txt, grep tool, grep -ril,
pacman -Q; plus mkdir -p and writes of this seat's report and receipts only.
