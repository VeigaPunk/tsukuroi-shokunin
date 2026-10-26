## Round-42 storage reading — R42-SCRUB-RECORD: the record's shape is read; the promotion condition is unchanged

Append-only; the round-26 frontier section, the round-38 promotion (R38-STORAGE-CORE) and the round-39 closure
(R38-ABSENT-ROOT) above stay as written, and the **Still Frontier** sentence that names the scrub record is neither
closed nor narrowed here.

Round 42 read the record itself instead of the host's counters. `corpus/knowledge/btrfs-scrub-record-r42.md` states,
at btrfs-progs v7.1 as built by Arch `7.1-1` on kernel `7.2.11-arch1-1`, five rows: the file
`/var/lib/btrfs/scrub.status.<fsid>`, written to a `_tmp` sibling and moved over by `rename`, created 0600, every open
under a non-blocking exclusive `flock` (SC1); the `scrub status:1` first line and the per-device `key:value` line with
its fixed field order (SC2); that the userspace `btrfs scrub start` process writes it, that recording is disabled with a
warning when the directory cannot be created or the first record written, and that running state comes from
`BTRFS_IOC_SCRUB_PROGRESS` rather than the file (SC3); how `btrfs scrub status` folds device lines — start time
smallest, canceled if any device was, finished only if all are, `running`/`aborted`/`finished`/`interrupted`,
`no stats available` on no start time, `ENOENT` as no history (SC4); and the per-device `scrub_speed_max` limit, which
reads 0 on a failed read and arrived with `btrfs scrub limit` in btrfs-progs 6.6.3 (SC5). Sources S237 and S238 (the
pinned v7.1 `cmds/scrub.c` and `CHANGES`) and S239 (this host's unprivileged capture: `/var/lib/btrfs` absent, no
`btrfs-scrub@*` timer listed and the unit file `disabled`, the root device's limit 0, no kernel scrub line in the
current boot).

**The promotion condition is unchanged.** The round-26 rule — "This area becomes Core only after a census arm exists"
(`PROVINCE.md:169`; `corpus/README.md:243`) — is not met for the scrub record: at this round's tip
`grep -c scrub tools/tsukuroi-census.sh` prints `0`, and neither `var/lib/btrfs` nor `btrfs-scrub` appears in the
census, so no arm reads `/var/lib/btrfs/scrub.status.<fsid>`, `btrfs scrub status` or `btrfs-scrub@.timer`; round 42's
C1 change stays inside `probe_packages`, `probe_update_safety` and `run_selftest` (8 hunks, 33 insertions and 8
deletions at `44766208`, `probe_storage_arm` untouched). The scrub record and NVMe SMART therefore stay Frontier
exactly as the round-38 promotion left them (`PROVINCE.md:212`, `:234`), and the second NVMe device stays unread.

**Within Frontier, what the reading buys.** Absence of a record is `UNRECORDED`, not "never scrubbed" (SC3); a record
is per device and a filesystem `finished` needs every device (SC2, SC4); `interrupted` is a process outcome, not media,
so a device is judged from its per-device error sums (SC4); a slow scrub is checked against `scrub_speed_max` before
the device is blamed, and a limit that reads 0 may be a failed read (SC5). SH4's `UNVERIFIED` for stored data is
unchanged.

**Limits.** This host has no record to parse (`.ufo/waves/round-42/frozen/hostcap/capture.txt:6`), so SC2's format and
SC4's fold are source-only here, and SC4's host cell records that the status command was not run when the entry was
written. The Arch `7.1-1` packaging patches were not compared with `cmds/scrub.c`. Row credit belongs to the wave-2
bound verdicts, not this paragraph: `python3 tools/check-scrub-record-r42.py --revision <REV>` (frozen at
`a84fc9de`, sha256 `dbe933ec…`) counts a row only from its bound `C2RevSC<n>`/`C2CritSC<n>` seats.

Operator-owned actions are unchanged: running a scrub, enabling `btrfs-scrub@.timer`, setting a per-device limit
(`btrfs scrub limit`) and any repair. No package, service, mount, scrub, counter-reset or configuration action is
authorized by this section.
