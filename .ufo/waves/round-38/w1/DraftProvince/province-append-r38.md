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
