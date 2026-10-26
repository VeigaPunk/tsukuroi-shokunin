## Round 42 — the scrub status record on the storage Frontier (2026-10-26)

Append-only (drafted by wave seat `ScribeReadme`, integrated by the L1); the coverage map and Frontier bullets above
stay as written. The C2 entry is the first statement of the storage Frontier's scrub record — the surface
`../PROVINCE.md:212` keeps Frontier — and it is not a promotion: no census arm reads the record. C1 is a census
operability repair inside `probe_packages` and `probe_update_safety` plus two `run_selftest` cases (8 hunks, 33
insertions and 8 deletions at commit `44766208`; `probe_storage_arm` untouched), not a coverage surface.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/btrfs-scrub-record-r42.md` | The scrub status record of the storage-integrity Frontier at btrfs-progs v7.1 as built by Arch `7.1-1` (kernel `7.2.11-arch1-1`), deepening the plane whose counter reading is `knowledge/storage-health-r26.md` (SH1–SH6): the record for one filesystem is `/var/lib/btrfs/scrub.status.<fsid>`, every update written to a `_tmp` sibling and moved over it with `rename`, a file the CLI creates mode 0600, every open taking a non-blocking exclusive `flock` (`LOCK_EX\|LOCK_NB`), so a reader sees the old or the new record and a held lock fails at once (SC1); the text format — first line `scrub status:1`, then one line per device, the filesystem UUID and the device id followed by `key:value` fields in a fixed order, fourteen progress and error counters then the five run fields `t_start`, `t_resumed`, `duration`, `canceled`, `finished` — so a record carries per-device sums and a per-device finished flag, not one filesystem verdict (SC2); the userspace `btrfs scrub start` process writes it, an all-zero record when the scrub starts and progress records while it runs, recording is switched off with a warning ending "status recording disabled" when `/var/lib/btrfs` cannot be created or the first record written, and whether a scrub is running is asked from the kernel per device with `BTRFS_IOC_SCRUB_PROGRESS`, so a missing record does not prove no scrub ran (SC3); `btrfs scrub status` treats an `ENOENT` open as no history and any other open failure as a warning, folds the device lines (start time the smallest, canceled if any device was, finished only if all are, from a starting 1), words the status `running`/`aborted`/`finished`/`interrupted` and prints `no stats available` with no start time, so `interrupted` is a process outcome, not a device fault (SC4); each device's `devinfo/<devid>/scrub_speed_max` limit reads 0 on a failed read, so "no limit" and "unreadable" cannot be told apart, and the limit, its status report and `btrfs scrub limit` arrived in btrfs-progs 6.6.3 (SC5); the host column reads this host unprivileged — root filesystem `1d02a454-c549-4a35-b567-89d60902af8e`, `/var/lib/btrfs` absent, no `btrfs-scrub@*` timer listed and the unit file `disabled`, the single device's limit 0, no kernel scrub line in the current boot | S237–S239 in `../SOURCES.md` (btrfs-progs v7.1 `cmds/scrub.c` sha256 `48df2e2f…` and `CHANGES` sha256 `bd881ab8…`, pinned in `.ufo/waves/round-42/frozen/src/` with `SHA256SUMS` and `FETCH.txt`; own-work capture `.ufo/waves/round-42/frozen/hostcap/capture.txt` sha256 `942edc91…`, captured 2026-10-26T19:13:44Z); `lessons/round-42.md` Gate (rows S237–S239); counter `../tools/check-scrub-record-r42.py` (frozen at `a84fc9de`, sha256 `dbe933ec…`); `../SCORECARD.md` "Round 42 — declaration" |

### Frontier notice — round 42

Round 42 promotes nothing. The entry above states the storage Frontier's scrub record — its file and write discipline,
its format, its writer and the switch that disables recording, the status command's fold and the per-device
throughput limit — on S237/S238/S239, beside the Core part of the same area, the per-device btrfs error counters the
round-38 arm reads (`corpus/README.md:284`). The round-26 rule that a Frontier area becomes Core only after a
read-only census arm reads it (`corpus/README.md:243`) is not met: at this round's tip
`grep -c scrub tools/tsukuroi-census.sh` prints `0`, and neither `var/lib/btrfs` nor `btrfs-scrub` appears in the
census (both `grep -c` print `0`); C1's hunks stay inside `probe_packages`, `probe_update_safety` and `run_selftest`
(`git diff -U0 c8efaa3f 44766208 -- tools/tsukuroi-census.sh`: 8 hunks, none in `probe_storage_arm`). The storage items
are therefore unchanged — the scrub record and NVMe SMART stay Frontier (`../PROVINCE.md:212,234`).

What the reading changes is triage, not ownership: "no scrub record" reads `UNRECORDED`, not `NEVER SCRUBBED` (SC3),
while SH4's `UNVERIFIED` for stored data stands; a record is per device, so a filesystem `finished` needs every device
finished and one canceled device makes the run `aborted` (SC2, SC4); `interrupted` is a process outcome, not media,
and the per-device error sums are where a device is judged (SC4); a slow scrub is checked against `scrub_speed_max`
before the device is blamed, where a failed read reads 0 (SC5).

Limits, as the entry states them. This host has no record to parse (`capture.txt:6`), so the format row and the status
fold are source-only here, and SC4's host cell records that the status command was not run when the entry was written.
Upstream is pinned at btrfs-progs v7.1 and the Arch build's packaging patches were not compared with `cmds/scrub.c`.
No census arm reads the record, so this Frontier ground is read, not covered by a gate. Row credit is not claimed here:
the wave-1 C2 reviews are first falsifiers whose corrections the L1 integrates before wave 2, and the counter's
verdict conjunct counts only the wave-2 `C2RevSC<n>`/`C2CritSC<n>` seats bound through `w2-dispatch.json` and
`w2-results.json` (`../SCORECARD.md` "Round 42 — declaration"; `../tools/check-scrub-record-r42.py:16-22`).
