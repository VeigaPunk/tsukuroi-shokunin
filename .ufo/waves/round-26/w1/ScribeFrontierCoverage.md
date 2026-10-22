# ScribeFrontierCoverage — round 26, wave 1

Verdict: done — the round-26 storage-integrity frontier text is drafted below as (a) an appended `PROVINCE.md` paragraph and (b) an appended `corpus/README.md` section with one coverage row and one Frontier bullet; no lane file was edited.

## Scope of this seat

This seat drafts frontier and coverage prose only. It does not create
`corpus/knowledge/storage-health-r26.md` or its `.json`, does not touch
`corpus/SOURCES.md`, `SKILL.md`, `SCORECARD.md`, `tools/check-storage-health.py`
or `tools/check-self-assessment.py`, and makes no git or jj write. The text
below is a proposal for the L1 (TsukuroiR26) to land; every host fact used is
taken from the frozen round-26 capture, and no fact outside that capture is
restated.

---

## Draft (a) — `PROVINCE.md`, appended paragraph

Placement: append at the end of
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md`, after the
`## R20 ownership clarification — OUT-009` section that currently ends the
file. Append-only: no existing line of `PROVINCE.md` is changed, and the Core
list at `PROVINCE.md:6-33` and the Frontier list at `PROVINCE.md:75-80` stay
byte-unchanged, so the sibling line-range pointers into this file do not move.

```markdown
**Round-26 frontier: storage integrity.** Btrfs device error counters, scrub
records and NVMe health enter this province as a frontier area of the OS
substrate. The lane reads the five per-device btrfs error counters (write,
read, flush, corruption, generation) as the filesystem exposes them in its
sysfs `error_stats` file and as the `btrfs device stats` query reports them;
it reads the scrub record the filesystem keeps (`btrfs scrub status` and the
shipped `btrfs-scrub@.timer` unit), and it reads the NVMe SMART/Health
lifetime fields (`smartctl -H -A`, `nvme smart-log`). Detection and report
only: the same boundary that governs the Core surfaces above applies here.
What stays out of the province — disk-space runway and free-capacity
reporting remain mori's (`../mori-shokunin/PROVINCE.md:26`, the `SURFACE disk`
row with its default `df -P` targets), and filesystem repair, running a
scrub, resetting an error counter and firmware updates remain operator-owned.
This area becomes Core only after a census arm exists; until then it is
Frontier and the knowledge entry is the record of the reading
(`corpus/knowledge/storage-health-r26.md`, rows SH1 to SH6; gate
`python3 tools/check-storage-health.py --revision <REV>`, field
`verified_rows`). No package, service, mount, scrub, counter-reset,
firmware or configuration action is authorized by this paragraph.
```

## Draft (b) — `corpus/README.md`, appended section

Placement: append at the end of
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md`, after the
`### Round-24 notice erratum after falsification` section that currently
ends the file. Append-only: the coverage map table at
`corpus/README.md:3-22` and the Frontier bullets at `corpus/README.md:28-42`
stay as written.

```markdown
## Round 26 — storage integrity (frontier area of the OS substrate)

Append-only; the coverage map above and the Frontier bullets at
`corpus/README.md:28-42` stay as written.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/storage-health-r26.md` and `.json` | Six sourced rows over the storage-integrity frontier area. SH1: the five btrfs per-device error counters (write, read, flush, corruption, generation) and the agreement between the filesystem's sysfs `error_stats` file and the `btrfs device stats` query. SH2: those counters persist across mounts until an explicit reset, so a non-zero value is not a dated incident and a dated incident comes from the kernel's per-error log line. SH3: what scrub verifies and when it can repair — with the data profile `single` a data checksum error is detected but not repaired, while the `dup` metadata profile keeps a second copy. SH4: this host's scrub record — `btrfs scrub status` reports no scrub statistics, `/var/lib/btrfs` is absent and the shipped monthly `btrfs-scrub@.timer` is disabled, so stored data has never been verified end to end. SH5: how `smartctl` derives the NVMe overall-health result and which SMART/Health fields decide it (critical warning, available spare against its threshold, percentage used, media and data integrity errors). SH6: the NVMe lifetime counters (unsafe shutdowns, power cycles, media errors, error log entries) are cumulative over the device's life, not dated incidents. The reading is pinned to the round-26 capture (sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd`), which records all five error counters at 0, no scrub statistics and a disabled scrub timer; counting command `python3 tools/check-storage-health.py --revision <REV>` reports the field `verified_rows`. | `../SOURCES.md` S128-S138 (btrfs-progs v7.1 device, scrub, profile and unit documentation; Linux v7.2 `fs/btrfs/volumes.c` and `fs/btrfs/sysfs.c`; smartmontools 7.5 `nvmeprint.cpp`; the primary definition of the NVMe SMART/Health log lifetime fields); `.ufo/waves/round-26/capture/capture.txt`; `SCORECARD.md` Round 26 C1 |

### Frontier (round-26 addition)

- Storage integrity is a frontier area of the OS substrate, not Core:
  btrfs device error counters, scrub records and NVMe health are entered by
  `knowledge/storage-health-r26.md` (rows SH1 to SH6) and become Core only
  after a census arm exists. Disk-space runway and free-capacity reporting
  stay with mori (`../mori-shokunin/PROVINCE.md:26`); filesystem repair,
  scrub runs, counter resets and firmware updates stay operator-owned. The
  entry is a read-only observation record — no scrub was started, no counter
  was reset and no configuration was written.
```

---

## Findings

1. [obs] The storage-integrity surface named in the draft is genuinely new to
   this province. `PROVINCE.md:8-14` lists the owned surfaces as pacman
   state, systemd user units and timers, journal/boot triage and the
   driver/firmware plane; the additional owned surfaces table at
   `PROVINCE.md:16-23` holds four entries (Arch News gate, `.pacnew`/
   `.pacsave` drift, initramfs v42 and boot recovery, Snapper/rollback net)
   and none of them is btrfs device counters, scrub records or NVMe health.
   Evidence: `PROVINCE.md:6-33` read in full this run.

2. [obs] `PROVINCE.md:75-80` is the existing `## Frontier` section and it
   currently holds two bullets (recipient acknowledgement and replay are
   unverified; kaidoku/revenger shipped-artifact RE ownership is contested).
   The draft therefore enters storage integrity as an appended Frontier area
   rather than editing that list, consistent with the append-only pattern the
   file already uses for its later sections (`PROVINCE.md:108-147` round-19
   anchors, `PROVINCE.md:148-152` the R20 clarification).

3. [obs] Disk-space runway is mori's, by its own declaration: mori's Core
   row reads "**Resource runway** — `SURFACE disk` and `SURFACE cgroup`:
   default `df -P` targets `$ROOT` and `/tmp`" at
   `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md:26`, and its
   owned-surface preamble at line 10 lists "resource runway (disk on the
   fleet root and `/tmp`, memory pressure)". The draft therefore routes
   capacity and free-space questions away from tsukuroi instead of claiming
   them.

4. [obs] The operator-owned boundary is the lane's existing boundary. The
   draft's "no repair, no scrub, no counter reset, no firmware action"
   wording restates the standing rule at `PROVINCE.md:25-28` ("Never
   installs, upgrades, or removes packages; never restarts services.
   Detection and report; the operator remediates.") and the round-26
   declaration's own limit list at `SCORECARD.md:908` ("No exploratory
   claim, capability acquisition, ordinal change, retirement, package
   transaction, sync, scrub, counter reset, service start or restart, boot
   action or configuration write").

5. [obs] The host facts used in the coverage row all come from the frozen
   capture, and only from it: the five error counters are all `0` in the
   sysfs `error_stats` file (`capture.txt:39-45`) and in the
   `btrfs device stats` output (`capture.txt:110-117`); the data allocation
   profile is `single` (`capture.txt:64`) while the metadata and system
   profiles are `dup` (`capture.txt:79`, `capture.txt:100`); `btrfs scrub
   status` prints `no stats available` (`capture.txt:121`) and
   `/var/lib/btrfs` is absent (`capture.txt:126-128`);
   `btrfs-scrub@-.timer` is `disabled` (`capture.txt:130-131`) with the
   shipped unit describing a monthly scrub (`capture.txt:136-148`); and the
   SMART/Health fields quoted in the row (critical warning `0x00`, available
   spare `100%` against a `10%` threshold, percentage used `2%`, media and
   data integrity errors `0`, power cycles `325`, unsafe shutdowns `200`) are
   at `capture.txt:184-197`. The capture's own digest is the one stated in
   the declaration, `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd`
   (`SCORECARD.md:897`).

6. [obs] The SH1 to SH6 wording in the coverage row is the declared row
   text, not a restatement of host state: `SCORECARD.md:895` defines the six
   rows as the btrfs counter identity, counter persistence, scrub verify and
   repair semantics, this host's scrub record, the `smartctl` health
   derivation and the NVMe lifetime counters. The counting command in the
   row's Sources cell is the one fixed in the claim table at
   `SCORECARD.md:892` (`python3 tools/check-storage-health.py --revision
   <REV>` → field `verified_rows`).

7. [inf] The coverage row describes the entry in the terms of the
   declaration. If the landed `corpus/knowledge/storage-health-r26.md` text
   differs in wording or ordering from the SH1 to SH6 definitions, the
   coverage-map row must be reconciled to the landed entry rather than to the
   declaration text; the L1 owns that reconciliation.

8. [unk] Whether the corpus/README coverage map's own table (at
   `corpus/README.md:5-22`) should also gain a row, in addition to the row
   inside the appended round-26 section, is not decided by this seat. The
   assignment asks for one coverage row in an appended section, and the
   draft places exactly one row there; whether a second pointer row belongs
   in the historical table is left to the L1.

9. [obs] The two draft texts carry no new claim that the lane is not able to
   support: the Frontier bullet states the promotion condition ("becomes Core
   only after a census arm exists") in the same terms the province already
   uses for carried debt ("a census arm for root-dir mode ... is carried
   debt", `corpus/README.md:40-41`), and it grants no configuration,
   service, package or boot authority.

## Out of scope for this seat

- Creating or editing `corpus/knowledge/storage-health-r26.md` or its
  `.json`, the `SOURCES.md` rows S128 to S138, the `SKILL.md` registry row
  for `## Storage integrity — round 26`, and the two gate tools.
- Any census arm, any promotion of the storage-integrity area to Core, and
  any change to the existing Core, Adjacent or Frontier lists.
- Any host action: no scrub, no counter reset, no `df` claim, no service or
  package transaction.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md, corpus/README.md, SCORECARD.md round-26 section, corpus/SOURCES.md tail, .ufo/waves/round-26/capture/capture.txt, /home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md; wrote=.ufo/waves/round-26/w1/ScribeFrontierCoverage.md; executed=read and grep only (no sudo, no host command, no git/jj write)

Model: opencode-go/minimax-m3.1-flash-free

Installs: none
