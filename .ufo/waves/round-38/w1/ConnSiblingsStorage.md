VERDICT: supports

# Item X-1 — Sibling-overlap scan for C1 (storage-integrity arm)

Seat ConnSiblingsStorage (connector, leaf), tsukuroi lane round 38 wave 1. Base
`8bd001f58bfda29c92d90d2a7a413825c0ca9fcb`. Read-only scan; no lane file touched
except this report; no host mutation; no tools installed; no scratch used (nothing
to clone or fixture for an adjacency scan).

## 1. What the C1 STORAGE arm actually reads (the crossing candidate)

`tools/tsukuroi-census.sh` at the implementation commit `52ffd65f8684`:

- Contract header `:353-367`: one verdict-neutral line
  `STORAGE btrfs-device-stats state=HEALTHY|DEGRADED|BLOCKED filesystems=N devices=N nonzero=N [detail=...]`,
  sourced **only** from sysfs `/sys/fs/btrfs/<fsid>/devinfo/<devid>/error_stats`
  (five counters: write/read/flush/corruption/generation). "No privilege is needed
  (sysfs 0444), counters are never reset (`btrfs device stats -z` is
  operator-owned), NVMe SMART (SH5/SH6) is not read. The line is verdict-neutral:
  no PLANE text, rollup term or exit code changes" (`:364-367`).
- State semantics inherit the SH2 discipline: nonzero counters are "a stored
  lifetime total, never a dated event — SH2; date it from error-level kernel
  lines" (`:361-363`).
- `probe_storage_arm()` at `:1847-1887`; print site `:3006-3008`. Selftest cases
  at `:2884-2922`.
- Claim text: `SCORECARD.md:2117` (round-38 declaration table, C1 row) — "Storage
  integrity (btrfs per-device error counters) moves Frontier → Core … met by a
  verdict-neutral census arm".

So the arm touches exactly one host surface: btrfs per-device error counters in
sysfs. That is the only surface a sibling could contest.

## 2. Sibling ownership scan

Sweep command: `grep` over `/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md`
(22 lanes) for `btrfs|error.?counter|scrub|SMART|smartctl|NVMe|nvme|disk|df -P|diskstats|filesystem|firmware`.
Observed: **zero sibling hits** for btrfs, error counters, scrub, SMART, NVMe
health, or filesystem integrity. The only disk-adjacent ownership anywhere is
mori's free-capacity runway; other `filesystem` word matches are unrelated (kasegi
scope-root removal text, kumitate's jj "no filesystem boundary" seat-containment
note, revenger/kaidoku *firmware* reverse engineering). Follow-up repo-wide grep
of mori for `btrfs|error_stats|smartctl|nvme smart|scrub`: no device-integrity
reads (hits are environ-scrub hygiene prose and the round-15 update-safety quote
mentioning the `btrfs-overlayfs` boot hook).

### mori-shokunin — nearest neighbor, read in full

- `mori-shokunin/PROVINCE.md:10` — owns "resource runway (disk on the fleet root
  and `/tmp`, memory pressure)".
- `mori-shokunin/PROVINCE.md:26` — `SURFACE disk`: "default `df -P` targets
  `$ROOT` and `/tmp`, since-boot device-write average, memory PSI/fill/avail".
- `mori-shokunin/PROVINCE.md:49` — FR6 "Instantaneous disk write-rate": the
  since-boot average is retained as a different measure; two-sample rate deferred.
- `mori-shokunin/PROVINCE.md:12-15` — Refuses: "OS package, systemd unit,
  driver/firmware and boot state (→ tsukuroi)".
- `mori-shokunin/PROVINCE.md:66` — Adjacent tsukuroi row: tsukuroi "Owns host OS,
  package, systemd-unit, driver, firmware, and boot diagnosis."

Comparison: mori's disk plane reads **capacity** (`df -P`) and **write rate**
(since-boot device-write average). The C1 arm reads **integrity error counters**
from sysfs `error_stats`. Disjoint metric, disjoint mechanism, disjoint files.
No crossing. The split is already written on both sides:
- `tsukuroi-shokunin/PROVINCE.md:165-166` — "disk-space runway and free-capacity
  reporting remain mori's (`../mori-shokunin/PROVINCE.md:26`, the `SURFACE disk`
  row with its default `df -P` targets)".
- `tsukuroi-shokunin/PROVINCE.md:176` (round-26 wave-2 correction) — "The split
  is by question: free space as fleet runway is mori's, free space as an upgrade
  or boot precondition is this lane's."
- `tsukuroi-shokunin/corpus/README.md:243` (round-26 Frontier bullet) —
  "Disk-space runway stays with mori; scrub runs, counter resets, profile changes
  and firmware updates stay operator-owned."

### kama-shokunin — read in full

`kama-shokunin/PROVINCE.md:3-16`: domain is local model serving & endpoint
health (producer discovery, baseURL pins, served-model reconciliation, probe
conventions). Zero storage or device-health ownership. No crossing. (The NVMe
device mentioned in tsukuroi's round-26 correction is a tsukuroi-side frontier
limit — the second NVMe device is unread — not a kama surface.)

### kumitate-shokunin — read in full

`kumitate-shokunin/PROVINCE.md:3-6`: orchestration & tooling; "Refuses: anything
outside this domain". Zero storage ownership. No crossing.

### souji-shokunin — targeted (closest other "disk" verb in the fleet)

`souji-shokunin/PROVINCE.md:93-94`: the repo-structure probe "reports reachable
objects, not recoverable disk space and not removal authorization" — an explicit
disclaimer of capacity estimation. Repository hygiene, not device integrity.
No crossing.

### kaidoku / revenger

Firmware RE is *shipped-artifact internals* (kaidoku `PROVINCE.md:132-135`
capability table; revenger `PROVINCE.md:3-7`), already refused by tsukuroi
(`tsukuroi-shokunin/PROVINCE.md:25-28`: "binary RE of drivers (→ kaidoku/
revenger — tsukuroi tracks *state and health*, not internals)"). The arm reads
sysfs counters, not firmware bytes. No crossing.

## 3. Crossing analysis — none created

1. **No displaced owner.** No sibling declares btrfs error counters, scrub status,
   SMART/NVMe health, or filesystem integrity. The arm takes nothing from anyone.
2. **mori is disjoint and already documented.** Metric-disjoint (integrity vs
   capacity/rate) and mechanism-disjoint (sysfs `error_stats` vs `df -P`/
   diskstats). The boundary was recorded in round 26 on both sides
   (`tsukuroi-shokunin/PROVINCE.md:165-168,176`; `mori-shokunin/PROVINCE.md:10,26,49,66`;
   `corpus/README.md:243`). C1 does not move any part of it.
3. **Counter discipline is internal.** The arm's SH2 rule (census.sh:361-363,
   "a stored lifetime total, never a dated event") parallels ADJ-04's memory-plane
   rule (`tsukuroi-shokunin/PROVINCE.md:49`: "cumulative counters are not dated
   incidents"). Same lane, same discipline, no ownership overlap with mori.
4. **Operator-owned actions stay operator-owned.** The arm never resets counters,
   never runs a scrub, never reads SMART (census.sh:364-365), matching
   `corpus/README.md:243` verbatim.
5. **Promotion-scope caution for L1.** The round-26 frontier declared **three**
   signal families: btrfs error counters, the scrub record, and NVMe SMART/Health
   (`tsukuroi-shokunin/PROVINCE.md:156-163`). C1 arms only family (a) — the
   error counters. The scrub record and NVMe SMART families remain Frontier /
   knowledge-only (`storage-health-r26.md` SH3–SH6; the wave-2 correction notes
   those reads need `sudo -n` and cover only the root's backing NVMe). The
   graduation wording must move exactly one sub-surface to Core, or it overclaims
   against the lane's own round-26 declaration.

## 4. Proposed Adjacent-line text (exact draft for the lane to carry)

Append to `PROVINCE.md` after the round-26 correction paragraph, in the note
shape of the round-32/33 "Adjacent —" entries:

```markdown
## Adjacent — storage integrity boundary (round 38)

Append-only; the ADJ-01 to ADJ-07 table above is unchanged. The round-26
storage-integrity frontier graduates to Core in exactly one sub-surface: the
verdict-neutral census arm `STORAGE btrfs-device-stats` reads the five
per-device btrfs error counters from sysfs `error_stats` and nothing else
(`tools/tsukuroi-census.sh` `probe_storage_arm`; counters
`tools/score-storage-arm-r38.py` and `tools/score-storage-arm-r38-q82.py`).
No sibling declares this signal and none is displaced. Disk free-space runway
(`df -P` on the fleet root and `/tmp`, since-boot device-write average) remains
mori's (`../mori-shokunin/PROVINCE.md:10,26,49`); free space as an upgrade or
boot precondition remains this lane's (the round-26 correction above). Scrub
runs, error-counter resets (`btrfs device stats -z`), filesystem repair and
firmware updates remain operator-owned; the arm performs none of them, and it
reads no scrub record and no NVMe SMART — those two families of the round-26
frontier stay Frontier until their own read-only arms exist. A nonzero counter
is a stored lifetime total, never a dated event (SH2); dating an error from
error-level kernel lines stays on this lane's journal plane. No package,
service, mount, scrub, counter-reset, firmware or configuration action is
authorized by this arm.
```

## 5. What I did not do

- Did **not** re-run the C1 / Q82 counters — predicate re-verification belongs to
  the Exec seats; this seat is the adjacency scan only.
- Did **not** read sibling corpora beyond the mori repo-wide keyword grep and
  souji's PROVINCE; the seat scoped sibling evidence to `PROVINCE.md` files.
  mori's `tools/mori-census.sh` was not line-read; the grep covers the ownership
  question at lane-content level.
- Did **not** re-pin mori's HEAD against tsukuroi's round-19/32 citations; mori's
  PROVINCE was read live at whatever HEAD is checked out today. The round-19
  anchor apparatus already declares pins stale-by-design, and mori's round-30
  self-note (`mori-shokunin/PROVINCE.md:392-400`) records its own line drift.
- Did **not** message or coordinate with sibling lanes (leaf seat).

## 6. Judged axes

- **Adjacency:** clean. No crossing created; the one live neighbor boundary
  (mori disk runway) is metric- and mechanism-disjoint and was already
  documented in round 26 on both sides. Proposed carry text above records the
  post-graduation boundary so a later seat cannot silently widen the arm into
  mori's runway or the operator's repair actions.
- **C1:** supports. The arm's read-set (sysfs `error_stats` only, verdict-neutral)
  matches the round-26 declaration and disturbs no sibling contract; the only
  defect risk is wording scope (§3 item 5), which is a drafting instruction to
  L1, not a counter failure.
