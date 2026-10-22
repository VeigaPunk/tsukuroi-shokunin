source: round-25 L1 read-only capture
verified-at: 2026-10-22
recheck: 90d

# Memory pressure and systemd-oomd — round 25

Fixture baseline for the C2 mutation set, not the lane's production entry. Six rows, MP1 to
MP6, each with a statement, a verdict on this host, an operator action, its sources, its
located quotes and its pointers into the frozen capture
`.ufo/waves/round-25/capture/capture.txt` (sha256
`e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`).

The machine-readable form of this entry is `corpus/knowledge/memory-pressure-r25.json`.

## MP1 — the `some` and `full` lines of system memory pressure

Statement: the `some` line of `/proc/pressure/memory` counts the share of time in which at
least one task was stalled waiting for memory, and the `full` line counts the share of time in
which all non-idle tasks were stalled at once.

Verdict: confirmed on this host; both lines are readable and carry the stall averages for
kernel 7.2.11-arch1-1.

Action: read-only. `cat /proc/pressure/memory` before and after a suspected stall. No host
change is proposed.

Sources: S115. Quotes: S115 (lesson Gate, 2026-10-22). Capture pointers: lines 14 and 15.

## MP2 — `total` is cumulative stall time

Statement: the `total` field of a pressure line is a cumulative stall time in microseconds, so
a dated incident needs two reads and the difference between them.

Verdict: confirmed on this host; `total` grows between the two captured reads of the same file.

Action: read-only. Two `/proc/pressure/memory` reads at least 10 s apart, then subtract the
`total` values. No host change is proposed.

Sources: S115. Quotes: S115 (lesson Gate, 2026-10-22). Capture pointers: line 14.

## MP3 — per-cgroup memory pressure files

Statement: each cgroup exposes its own `memory.pressure` file; the per-cgroup files report the
stall of that cgroup's own tasks, while `/proc/pressure/memory` reports the whole system.

Verdict: confirmed on this host; the root cgroup, `user.slice`, `user-1000.slice` and
`user@1000.service` each expose a readable `memory.pressure` file.

Action: read-only. `cat /sys/fs/cgroup/<path>/memory.pressure` for the cgroup under
investigation, compared with the system file. No host change is proposed.

Sources: S116. Quotes: S116 (lesson Gate, 2026-10-22). Capture pointers: lines 34, 38 and 42.

## MP4 — `ManagedOOMMemoryPressure=` and `ManagedOOMSwap=`, and what they mean here

Statement: `ManagedOOMMemoryPressure=` and `ManagedOOMSwap=` take `auto` or `kill`; with
systemd-oomd inactive and disabled on this host, neither setting can act, so the properties are
recorded rather than relied on.

Verdict: not armed on this host; `systemd-oomd.service` is inactive and disabled, and
`user@1000.service` carries `MemoryPressureWatch=skip`.

Action: read-only. `systemctl is-active systemd-oomd.service` and `systemctl show -p
ManagedOOMMemoryPressure -p ManagedOOMSwap -p MemoryPressureWatch -- user@1000.service`.
Arming systemd-oomd is an operator-owned change and is not proposed here.

Sources: S117 and S119. Quotes: S117 and S119 (lesson Gate, 2026-10-22). Capture pointer: line 73.

## MP5 — the systemd-oomd default limits for systemd 262

Statement: for systemd 262 the shipped systemd-oomd defaults are
`DefaultMemoryPressureLimit=60%`, `DefaultMemoryPressureDurationSec=30s` and
`SwapUsedLimit=90%`, all three left commented in `/etc/systemd/oomd.conf` on this host.

Verdict: the compiled-in defaults are in force here; the shipped configuration file comments
every one of the three limits.

Action: read-only. `systemd-analyze cat-config systemd/oomd.conf`. Changing the limits is an
operator-owned configuration change and is not proposed here.

Sources: S118. Quotes: S118 (lesson Gate, 2026-10-22). Capture pointers: lines 106, 107 and 108.

## MP6 — kernel OOM kill evidence is a separate plane

Statement: kernel OOM kill evidence is a separate plane from pressure stall evidence; the
`oom` and `oom_group_kill` counters of `memory.events` record kills that already happened, while
pressure counters record time spent stalled.

Verdict: no kill has occurred on this host; the captured `memory.events` counters read zero.

Action: read-only. `cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.events` and
`grep -E '^oom_kill ' /proc/vmstat`. No host change is proposed.

Sources: S116 and S120. Quotes: S120 (lesson Gate, 2026-10-22). Capture pointers: lines 50 and 52.

## QUALITY

Fixture baseline. Each row carries a verdict and a read-only action, cites at least one mined
SOURCES row whose used-by names this entry and that was opened on 2026-10-22, carries a located
quote of at most 25 words recorded in the `corpus/lessons/round-25.md` Gate, points at least
once into the frozen capture on a line whose text is unique in the capture and is neither a
section header nor a command echo nor an exit line, and has a decision-table row in `SKILL.md`.
