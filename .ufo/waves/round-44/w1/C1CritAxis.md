VERDICT: defect-found

Item C1-13 — framing of the C1 promotion (scrub-record line of the storage-integrity frontier, Frontier → Core).
The counter and the measured surface are sound; the defect is that the promotion condition's literal wording, a
read-only census arm "reads it", is only partially met, so the promotion note MUST state the narrower sub-surface
or it overclaims against `PROVINCE.md:212-214` and `corpus/README.md:243`. Exact wording in §6.

## 1. The declared surface vs the promotion condition

- `PROVINCE.md:212-214` (exact): "**Still Frontier:** the scrub record (`btrfs scrub status`, `/var/lib/btrfs/scrub.status.*`,
  `btrfs-scrub@.timer`; SH3/SH4) and NVMe SMART/Health (`smartctl -H -A`, `nvme smart-log`; SH5/SH6) — no census
  arm reads them." The bundle is three-fold: (a) the CLI report `btrfs scrub status` (record content + running
  state), (b) the record files' content, (c) the timer.
- `corpus/README.md:243` (promotion condition): "Storage integrity is a frontier area, not Core: it becomes Core
  only after a read-only census arm reads it (shape proposed in `.ufo/waves/round-26/w1/ScoutHostSurfaces.md`)."
  Applied per-item since round 38: `corpus/README.md:295-296` "is met for the btrfs per-device error counters only;
  the scrub record and NVMe SMART stay Frontier", restated at `corpus/README.md:382` (round-41) and re-asserted at
  `corpus/README.md:412-414` (round-42) and `:424` (round-43): "the scrub record stays Frontier (no census arm reads it)".

## 2. What the arm actually reads (probe_scrub_record, `tools/tsukuroi-census.sh:1967-2055`)

- Record directory `/var/lib/btrfs`: entry **names** and type checks only (`-d`/`-f`/`-L`/`-S`/`-e`), readability
  (`-r`) for the `unreadable=N` count, orphan = fsid absent from sysfs. The function never opens a record file:
  the only file whose content is read in the whole function is the sysfs `scrub_speed_max` attribute (needed to
  classify 0 vs nonzero → `limited=N`).
- Timer links under `/etc/systemd/system/timers.target.wants`: names matching `btrfs-scrub@*.timer` (count only).
- Never an ioctl; never running state. The kernel running state is unreadable unprivileged: SR6,
  `corpus/knowledge/btrfs-scrub-record-r43.md:98-117` — `BTRFS_IOC_SCRUB_PROGRESS` returns `-EPERM` unless
  `CAP_SYS_ADMIN` ("a census running as the user cannot learn from the kernel whether a scrub is in progress").
- The frozen counter's oracle is equally content-free (`tools/score-scrub-arm-r44.py:178-262`: the model is
  type/readability only; the case builder writes `'scrub status:1\n'` into record files but nothing ever reads it
  back). Arm and counter lock the no-content contract.

Conclusion: the arm satisfies a narrower condition than "a read-only census arm reads [the scrub record]": it reads
the record's presence/config artifact set — names, types, readability, orphan-ness, the sysfs throttle value and
the timer links — not the record's data and not running state. The promotion is a sub-surface move and must be
stated as such.

## 3. Which parts stay Frontier

- Record content: outcomes inside `scrub.status.<fsid>` (state fold finished/canceled/interrupted, per-device
  statistics, dates) — not read.
- Kernel running state (`BTRFS_IOC_SCRUB_PROGRESS`) — unreadable unprivileged (SR6). The `sockets=N` count
  reveals a live userspace `btrfs scrub start` process only, not kernel state.
- SH3 (repair semantics: `single`-replica uncorrectable, NOCOW file data unverified) is knowledge and stays
  Frontier.
- SH4: the arm now verifies *file absence* on this host (live leg at `after/c1-after-ab8aae1.jsonl`:
  `state=NONE dir=absent records=0`), so SH4's "no record exists" is census-checkable as file absence; record-content
  claims stay unverified.
- `btrfs scrub status` itself stays operator-invoked.

## 4. Do-nothing controllability (target not vacuous)

- `before/c1-before.jsonl` (base `98020ece`): verdict FAIL, `correct=0`, `wired_ok=0`, `live_agree=0`,
  `selftest_r44=0` — the target is unreachable by doing nothing.
- Battery `controls/battery-summary-c1.jsonl`: K0 (do-nothing candidate) FAIL `correct=0`; `control_accepted=1`,
  `should_fail_accepted=0`. K1 (constant emitter) reaches `correct=1/live_agree=1` but is gated by
  `selftest_pass/selftest_r44`; K11/K12/K13 gate the selftest labels, wiring and line placement.
- This satisfies round-prompt §6 item 9's requirement "A target must be one a do-nothing control cannot reach"
  (`/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-44.md:481`).

## 5. Axis fit: coverage is right for the surface actually changed

- `AXES.md:12`: coverage = "Fraction of the domain's real surfaces the skill governs (repo paths, tools, edge
  classes) | PROVINCE.md lists every surface; none unexplored without reason".
- §6 item 9: "Name the axis by the surface the round changes, not by the number it produces … A coverage claim
  names the surface it moves (frontier → core, a new tool, operation or edge class) and the command that would
  show it unmoved" (`tsukuroi-round-44.md:486-489`).
- The round moves exactly one surface: the scrub-record line of the storage-integrity frontier, for the
  unprivileged view. That is textbook coverage (frontier → core); the claim names the command
  (`tools/score-scrub-arm-r44.py`) that shows it unmoved at base, and the base receipt proves it. `depth` is C2's
  axis (sourced rows); operability/freshness name other surfaces. So coverage is right — provided the named surface
  is the narrowed one; naming "the scrub record" wholesale would exceed the moved surface.

## 6. Required wording (exact proposed text)

### PROVINCE.md — append a new section (style follows the round-38/39 sections; the round-38 "Still Frontier" bullet and the round-42/43 notes stay as written):

```
## Round-44 promotion — R44-C1-SCRUB-RECORD: the scrub-record presence/config line moves Frontier → Core (unprivileged view)

Append-only; the round-38 and round-39 sections stay as written. The round-26 condition ("becomes Core only after
a read-only census arm reads it", `corpus/README.md:243`) is met for the scrub-record line for the unprivileged
view only: the census arm reads the record's presence and configuration, never its content and never running state.

**Core now:** the unprivileged presence-and-configuration surface of the scrub record, reported on the census's
verdict-neutral `SCRUB btrfs-scrub-record state=… dir=… records=N tmp=N sockets=N unreadable=N orphan=N limited=N
timers=N [detail=…]` line (`probe_scrub_record` in `tools/tsukuroi-census.sh`; `SKILL.md` "Scrub-record arm —
round 44"), printed after STORAGE and before the TSUKUROI_CENSUS rollup: `/var/lib/btrfs` entries by name and
type only — regular `scrub.status.<fsid>` record files, `scrub.status.<fsid>_tmp` staging files and
`scrub.progress.<fsid>` sockets, with unreadable and orphan counts — each device's sysfs `scrub_speed_max` value
(0 = no limit), and enabled `btrfs-scrub@*.timer` links under `timers.target.wants`. Unprivileged, resets
nothing, never enters `TSUKUROI_CENSUS`, never opens a record file's content, never issues an ioctl and never
queries running state (`BTRFS_IOC_SCRUB_PROGRESS` requires `CAP_SYS_ADMIN`, SR6).

**Still Frontier, unchanged portion:** the scrub record's content — the outcomes and per-device statistics inside
`scrub.status.<fsid>` (state fold, last-run data, error totals) — and whether a scrub is currently running in the
kernel; the census arm reads neither, and `btrfs scrub status` remains operator-invoked. The socket count reveals
a live userspace `btrfs scrub start` process only. SH3 (repair semantics) stays knowledge; SH4's "no record
exists on this host" is now census-checkable only as file absence. NVMe SMART/Health stays Frontier as before.

Counted by `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR>` at the round-44 measured
revision (`SCORECARD.md` "Round 44 — measured outcome"); the base receipt
`.ufo/waves/round-44/before/c1-before.jsonl` FAILs (correct=0), so the target is unreachable by a do-nothing
control. No package, service, mount, scrub, counter-reset, firmware or configuration action is authorized by
this section.
```

### corpus/README.md — add a new "Frontier notice — round 44" after the round-40 notice (superseding `:412-414`/`:424`'s "no census arm reads it" for this sub-surface only):

```
### Frontier notice — round 44

The round-26 condition is now met for the scrub-record line of the storage-integrity frontier for the
unprivileged view only: the census arm reads record-file, socket and staging-name presence and types, per-device
sysfs `scrub_speed_max` values, and enabled `btrfs-scrub@*.timer` links (`../tools/tsukuroi-census.sh`
`probe_scrub_record`; `../PROVINCE.md` "Round-44 promotion — R44-C1-SCRUB-RECORD"). It does not read record
content and cannot see running state (SR6), so the record's outcomes, per-device statistics and the kernel
running state stay Frontier, and `btrfs scrub status` stays operator-invoked. This supersedes the round-38/42/43
"the scrub record … stays Frontier" sentences for this sub-surface only. Measured with
`../tools/score-scrub-arm-r44.py` at the revision named in `../SCORECARD.md` "Round 44 — measured outcome";
base receipt FAIL.
```

## 7. Smallest safe correction

Statement-level only: the promotion notes must carry the "unprivileged view / presence-and-configuration only;
content and running state stay Frontier" qualifier (exact text above). No code or counter change is required: the
counter's predicate measures exactly the narrowed surface, the base receipt fails, and the declaration already
says "for the unprivileged view" (`SCORECARD.md` "Round 44 — declaration"). The defect is in the promotion-note
wording to be written after measurement, not in the counter or the arm.
