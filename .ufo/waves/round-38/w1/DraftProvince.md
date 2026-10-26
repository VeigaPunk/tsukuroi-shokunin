VERDICT: draft

# P-1 — append-only PROVINCE.md text for R38-STORAGE-CORE (Frontier → Core, error counters only)

Seat `DraftProvince`, leaf, read-only on lane content. No product file was edited; the only bytes
written are this report and its receipt directory. No scratch tree was created (`/fast/scratch/...`
unused), so nothing to remove. No tool installed or upgraded.

## 1. Where to append

Append at the **end of `PROVINCE.md`, after line 197** (its last section is the round-33 note,
`PROVINCE.md:195-197`). Prepend exactly one blank line: the file currently ends with the single
bytes `new trigger.\n` (`tail -c 120 PROVINCE.md | od -c`), so the append is
`"\n" + text below` and nothing else.

Why the end, not the Core section: every later-round move in this file is an end-appended section
that leaves the tables above untouched (`PROVINCE.md:154` "## Round-26 frontier — storage
integrity", `:178` round 27, `:191` round 32, `:195` round 33), and the append carries a
round-scoped id like `R13-DAC-EXCLUSIVITY` (`PROVINCE.md:92`) or `R20-OUT009` (`:150`). The Core
list at `:6-33` is not edited; the new section states that it is the Core list's record for this
surface.

## 2. Exact proposed text (verbatim; receipt bytes at
`.ufo/waves/round-38/w1/DraftProvince/province-append-r38.md`, sha256 in §6)

```markdown
## Round-38 promotion — R38-STORAGE-CORE: the btrfs error counters move Frontier → Core

Append-only. The `## Round-26 frontier — storage integrity` section above and its wave-2
correction stay as written; this section records that the one condition that section set for
itself — "This area becomes Core only after a census arm exists" (`PROVINCE.md:169-170`) — is met
for the per-device error-counter reading, and for nothing else in that section.

**What is Core now.** Reading the five per-device btrfs error counters `write_errs`, `read_errs`,
`flush_errs`, `corruption_errs` and `generation_errs` from
`/sys/fs/btrfs/<fsid>/devinfo/<devid>/error_stats`, as the census's storage-integrity arm reports
them on one verdict-neutral line after the DRIFT line and before the rollup:
`STORAGE btrfs-device-stats state=HEALTHY|DEGRADED|BLOCKED filesystems=N devices=N nonzero=N
[detail=<fsid8>:<devid>:<key>=<value>|…]` (`tools/tsukuroi-census.sh:1847-1888`, emitted at
`:3007-3008`; contract at `:350-370`). `nonzero` counts the (device, counter) pairs above zero;
`BLOCKED` on this line means the reading itself was impossible (a filesystem without a `devinfo`
entry, or an `error_stats` file unreadable or not carrying exactly the five counters once each).
The reading is unprivileged (sysfs 0444), it resets nothing, and its state word never enters
`TSUKUROI_CENSUS`: no `PLANE` text, rollup term or exit code changes. The five counters through
`btrfs device stats <mountpoint>` are the ioctl view of the same stored values (SH1), not a second
surface. A nonzero value is a stored cumulative total, not a dated event: after an operator-run
scrub it may come from the scrub itself, and dating an incident from error-level kernel `errs:`
lines is an inference from the kernel source, not a source sentence (SH2 and its wave-2
correction; `corpus/knowledge/storage-health-r26.md`). For a reader of the Core list at the top of
this file: this counter reading is now one of its surfaces; that list is not edited here, and this
section is its record.

**What stays Frontier — the rest of the round-26 section.** The scrub record (`btrfs scrub
status`, the `scrub.status.<UUID>` files under `/var/lib/btrfs`, the `btrfs-scrub@.timer` unit;
SH3/SH4) and NVMe SMART/Health (`smartctl -H -A`, `nvme smart-log`; SH5/SH6) stay Frontier
unchanged: no census arm reads either. The arm enumerates every mounted btrfs filesystem; on this
host that is the root alone (`/dev/mapper/root`), and the second NVMe (`nvme1n1`, xfs on `/tmp`
and `/fast`) exposes no btrfs error counters, so the round-26 wave-2 covering limit still holds —
that device's integrity and its SMART stay unread.

**What stays operator-owned.** Running a scrub, enabling `btrfs-scrub@.timer`, resetting a counter
(`btrfs device stats -z`, which prints and then zeroes the values), changing a block-group
profile, firmware updates, LUKS/crypttab work and any filesystem repair. The STORAGE line is
detection only; no package, service, mount, scrub, counter-reset, firmware or configuration action
is authorized by this section, and the census itself never resets a counter.

**What stays mori's.** Disk-space runway, under the round-26 wave-2 split recorded above: free
space as fleet runway is mori's, free space as an upgrade or boot precondition is this lane's.
The STORAGE line carries no capacity or free-space field, and this section adds none.

**How the move is counted.** Both frozen counters, at the measured revision of `SCORECARD.md`
"Round 38": `python3 tools/score-storage-arm-r38.py --revision <REV>` (ten fixtures, the live leg
and six `PLANE` lines per run) and `python3 tools/score-storage-arm-r38-q82.py --revision <REV>`
(the census with no override inside `unshare -rm`, a per-run random tree bind-mounted over
`/sys/fs/btrfs`; predicate `ns_views_matched == VIEWS and ns_available == 1`). The second is
required, not optional: a fixture-gated arm passes the first (QUALITY 82,
`.ufo/waves/round-38/controls/controls-q82.jsonl`). The sourced rows stay the reading's evidence
(SH1/SH2; `python3 tools/check-storage-health.py --revision <REV>`).

Known limit recorded here, not repaired here: `corpus/knowledge/storage-health-r26.md` still says
"No census arm reads these signals yet" (line 114). That sentence remains true for SH3 to SH6 and
is historical for the SH1/SH2 counters from this round; the entry is not rewritten by this
section. This section moves one counter file into Core and widens neither the province nor the
repair authority by one action.
```

## 3. Evidence for each assertion in the text

| Assertion in the draft | Evidence (path:line or command output) |
|---|---|
| Round-26 set itself the "Core only after a census arm exists" condition | `PROVINCE.md:169-170` — "This area becomes Core only after a census arm exists; until then it is / Frontier…"; `corpus/README.md:243` — "it becomes Core only after a read-only census arm reads it" |
| Only the error counters are promoted; scrub + SMART stay Frontier | `PROVINCE.md:158-163` (counters, `btrfs scrub status`, `btrfs-scrub@.timer`, `smartctl -H -A`, `nvme smart-log` all inside the round-26 area); the arm's own contract excludes them: `tools/tsukuroi-census.sh:364-365` — "No privilege is needed (sysfs 0444), counters are never reset … NVMe SMART (SH5/SH6) is not read" |
| Line format `STORAGE btrfs-device-stats state=… filesystems=N devices=N nonzero=N [detail=…]` | `tools/tsukuroi-census.sh:352-354` (contract) and `:1884-1885` (`STORAGE_LINE=` + `detail=` append) |
| `nonzero` = (device, counter) pairs above zero | `tools/tsukuroi-census.sh:359-360` — "nonzero counts the (device, counter) pairs above zero" |
| `BLOCKED` = reading impossible (no `devinfo`, unreadable, malformed) | `tools/tsukuroi-census.sh:360-361`; exercised by fixtures F04/F05/F07/F10 in `.ufo/waves/round-38/after/c1-after-52ffd65.json` |
| Placement: after DRIFT, before rollup | `tools/tsukuroi-census.sh:3002-3008` (DRIFT comment/probe/print, then `probe_storage_arm` and its `printf`), rollup starts `:3010` |
| State word never enters `TSUKUROI_CENSUS`, no PLANE/rollup/exit change | `:365-366` — "The line is verdict-neutral: no PLANE / text, rollup term or exit code changes"; roll at `:3010-3029` is computed from the six plane vars only |
| Unprivileged, no reset | `:364-365` — "No privilege is needed (sysfs 0444), counters are never reset" |
| ioctl view is the same counters | `corpus/knowledge/storage-health-r26.md:13-26` (SH1: same five counters, shorter sysfs names; `btrfs device stats` reads them through an ioctl) |
| Cumulative total not a dated event; scrub can move counters; "dates an incident" is inference | SH2 at `corpus/knowledge/storage-health-r26.md:27-40`; wave-2 correction at `:120` — "the counters also change during a scrub run … 'Only the error-level line dates an incident' is an inference from S132" |
| `-z` prints then zeroes (no "destroys history" claim) | wave-2 correction `corpus/knowledge/storage-health-r26.md:121` — "`-z` resets the values to zero after printing" |
| Operator-owned list unchanged | `PROVINCE.md:168` (repair, scrub run, counter reset, firmware); `SKILL.md:2361` (never starts a scrub, never `-z`, never enables the timer, no profile/LUKS change) |
| Mori split = round-26 wave-2 correction, not the overstated phrase | `PROVINCE.md:176-177` — "The split is by question: free space as fleet runway is mori's, free space as an upgrade or boot precondition is this lane's"; also "the second NVMe device (`/tmp`, `/fast`) is unread" |
| Only the root's btrfs fs is enumerated on this host | `ls /sys/fs/btrfs/` → `1d02a454-c549-4a35-b567-89d60902af8e` + `features`; live leg in `.ufo/waves/round-38/after/c1-after-52ffd65.json` → `filesystems=1 devices=1 nonzero=0` |
| `nvme1n1` (`/tmp`, `/fast`) is xfs, no btrfs counters | `stat -f -c '%n %T' / /boot /tmp` → `/ btrfs`, `/boot msdos`, `/tmp xfs`; `lsblk -no NAME,FSTYPE,MOUNTPOINTS /dev/nvme1n1` → `nvme1n1p1 xfs /tmp`, `nvme1n1p2 xfs /fast`; `df -P` → `/dev/mapper/root /`, `/dev/nvme1n1p1 /tmp` |
| Two counters, Q82 required because v1 is fixture-gateable | `SCORECARD.md:2117` (C1 row), `:2139-2152` (QUALITY 82; fixture-gated control scores v1 PASS 10/10 live 1; predicate `ns_views_matched == VIEWS and ns_available == 1`; "C1 is not verified unless the Q82 counter PASSes at the measured revision"); `.ufo/waves/round-38/controls/controls-q82.jsonl` record `C1-real-arm` → `q82 {ns_views_matched: 3, ns_available: 1, result: PASS, exit: 0}` |
| Registry rows exist for both gates | `SKILL.md:3113` (`storage-arm-r38`; its note says the QUALITY 82 gap means "it is used only with `storage-arm-r38-q82`") and `:3114` (`storage-arm-r38-q82`, unshare/`/sys/fs/btrfs` bind mount) |
| Implementation commit and freeze | `git log --oneline -4 -- tools/tsukuroi-census.sh` → `52ffd65 round-38: C1 storage-integrity census arm…`; `git cat-file -e 7cbaeb63…` → ok; `git diff --stat 52ffd65..HEAD -- tools/tsukuroi-census.sh corpus/knowledge/storage-health-r26.md` → empty (arm bytes unchanged to tip) |

## 4. Evidence state — what is measured and what is not (this seat ran neither counter)

- v1 C1 after receipt exists: `.ufo/waves/round-38/after/c1-after-52ffd65.json` →
  `fixtures_matched 10/10, live_match 1, six_planes_all 1, result PASS, exit 0`, live
  `STORAGE … state=HEALTHY filesystems=1 devices=1 nonzero=0`.
- **No Q82 after receipt exists** at any revision: `ls .ufo/waves/round-38/after/` lists only
  `c1-after-52ffd65.json` and `c2-after-1fe28e7.json`. The Q82 pass on the real arm is a *control*
  (`controls-q82.jsonl`, `C1-real-arm`, 3/3) recorded in the amendment, not a measured-revision
  receipt. **The draft must not land until `score-storage-arm-r38-q82.py --revision <REV>` PASSes
  at the measured revision**; the text itself gates on both counters rather than asserting a
  count, so it stays true either way.
- `git diff --stat 52ffd65..HEAD -- tools/tsukuroi-census.sh` is empty, so the arm bytes at the tip
  equal `52ffd65`; a tip Q82 pass is therefore *expected* but is an [INFERENCE], not observed.
- I did not run `tools/tsukuroi-census.sh`, either counter, or the storage-health gate; I did not
  touch sysfs, sudo, systemd or pacman.

## 5. Findings

- **F1 (stale line in the knowledge entry, not repaired here).**
  `corpus/knowledge/storage-health-r26.md:114` says "No census arm reads these signals yet; until
  one exists the area stays frontier (`PROVINCE.md`)." After C1 lands, that sentence is stale for
  SH1/SH2 and still true for SH3-SH6. The draft records this as a known limit and does not rewrite
  the entry; the landing round should add an append-only correction there (the lane's own
  convention, e.g. `:116` "## Wave-2 corrections (appended 2026-10-22)").
- **F2 (the promotion sentence needs the wave-2 caveats, or it contradicts the source entry).** A
  bare "nonzero = lifetime total, date it from error-level lines" would conflict with
  `storage-health-r26.md:120` (counters also move during a scrub; the dating sentence is an
  inference). The draft carries both caveats.
- **F3 (the second NVMe is outside the arm, and that is not a defect of the arm).**
  `/tmp` and `/fast` are xfs on `nvme1n1` (`lsblk`), so no btrfs counter exists for them; the
  round-26 wave-2 covering limit (`PROVINCE.md:176`) remains exactly true. The draft says so
  instead of implying whole-host counter coverage.
- **F4 (the "verdict-neutral" word is load-bearing and verified in code).** The line is printed
  after DRIFT and before the rollup and the rollup is computed only from the six plane variables
  (`tools/tsukuroi-census.sh:3002-3029`), so the Core addition cannot change an exit code. This is
  what makes the move a coverage move rather than a verdict move.
- **F5 (promotion is conditional on the Q82 counter, per the pre-seat amendment).** The draft names
  the Q82 counter inside the text; a later editor must not drop it as redundant — dropping it would
  re-open QUALITY 82 (a fixture-gated arm passes v1: `controls-q82.jsonl` `C1-fixture-gated` →
  `v1 {fixtures_matched: 10, live_match: 1, six_planes_all: 1, result: PASS}` / `q82 {ns_views_matched: 0, result: FAIL}`).
- **F6 (no ordering conflict).** PROVINCE's last append is round 33 (`:195-197`); rounds 34-37
  added nothing to this file, so the round-38 section appends cleanly and its self-citation
  `PROVINCE.md:169-170` stays valid because the append shifts no earlier line.

## 6. Touched surfaces / artifacts

- Written (only): `.ufo/waves/round-38/w1/DraftProvince.md` (this report) and
  `.ufo/waves/round-38/w1/DraftProvince/province-append-r38.md` (exact append bytes).
- Receipt digest: `sha256sum .ufo/waves/round-38/w1/DraftProvince/province-append-r38.md` →
  `7de818de5d352b6021fb077d8465460c0928a9f4f72338b56d36788f623d91ee` (4550 bytes, computed after
  the last edit to that file; `wc -c` agrees).
- Read only: `PROVINCE.md`, `corpus/README.md`, `corpus/knowledge/storage-health-r26.md`,
  `SCORECARD.md`, `SKILL.md`, `tools/tsukuroi-census.sh`, `tools/score-storage-arm-r38-q82.py`,
  `.ufo/waves/round-38/after/*`, `.ufo/waves/round-38/controls/controls-q82.jsonl`.
- Out of scope and untouched: no lane product edit, no git/jj write, no counter run, no census run,
  no host action, no sibling lane, no `/home/vgpnk/Projects/shokuknow`, no subagent.
