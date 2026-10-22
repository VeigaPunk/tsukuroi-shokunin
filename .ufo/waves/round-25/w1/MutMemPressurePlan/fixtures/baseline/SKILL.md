# SKILL — tsukuroi (fixture baseline for the C2 mutation set)

This file is a fixture baseline, not the lane's production SKILL.md. It carries the round-25
memory-pressure decision table in the column order the C2 declaration names: id, observation,
read-only command, verdict, action, entry pointer.

## Memory pressure and systemd-oomd — round 25

Authority: reading and decision entry only, from `corpus/knowledge/memory-pressure-r25.md`
(2026-10-22 capture `.ufo/waves/round-25/capture/capture.txt`; counting command
`python3 tools/check-memory-pressure.py --revision <commit>`). Nothing here lets a lane arm
systemd-oomd, change a systemd-oomd limit, start or stop a service, or write configuration.
The operator alone decides whether systemd-oomd is armed or its limits are changed.

| id | observation | read-only command | verdict | action | entry pointer |
|---|---|---|---|---|---|
| MP1 | the `some` and `full` lines of the system memory pressure file | `cat /proc/pressure/memory` | confirmed: both lines are readable and carry the stall averages for kernel 7.2.11-arch1-1 | Read the file before and after a suspected stall; no host change is proposed | entry row MP1 |
| MP2 | the `total` field of a pressure line is cumulative stall time | `cat /proc/pressure/memory` twice, 10 s apart | confirmed: `total` grows between the two captured reads | Take two reads and subtract the totals; no host change is proposed | entry row MP2 |
| MP3 | each cgroup exposes its own memory.pressure file | `cat /sys/fs/cgroup/<path>/memory.pressure` | confirmed: the root cgroup, user.slice, user-1000.slice and user@1000.service each expose a readable file | Compare the cgroup file with the system file; no host change is proposed | entry row MP3 |
| MP4 | `ManagedOOMMemoryPressure=` and `ManagedOOMSwap=` take `auto` or `kill` | `systemctl is-active systemd-oomd.service`; `systemctl show -p ManagedOOMMemoryPressure -p ManagedOOMSwap -p MemoryPressureWatch -- user@1000.service` | not armed: systemd-oomd.service is inactive and disabled and user@1000.service carries MemoryPressureWatch=skip | Record the properties; arming systemd-oomd is an operator-owned change and is not proposed here | entry row MP4 |
| MP5 | the systemd 262 memory pressure, duration and swap limits | `systemd-analyze cat-config systemd/oomd.conf` | the compiled-in defaults are in force: the shipped file comments every one of the three limits | Read the three defaults; changing them is an operator-owned configuration change | entry row MP5 |
| MP6 | kernel OOM kill counters are a separate plane from pressure stall counters | `cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.events`; `grep -E '^oom_kill ' /proc/vmstat` | no kill has occurred: the captured memory.events counters read zero | Read both planes before diagnosing a stall; no host change is proposed | entry row MP6 |
