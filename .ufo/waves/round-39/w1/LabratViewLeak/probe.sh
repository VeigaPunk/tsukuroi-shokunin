#!/usr/bin/env bash
# LabratViewLeak probe. Runs in the r39 counter's view namespace in place of the census script,
# and enumerates every channel through which a census arm could learn the view's values or the
# expected line without reading the mounted /sys/fs/btrfs tree.
set +e
export LC_ALL=C
D=$(cd "$(dirname "$0")" && pwd)
P=$PPID
say() { printf '%s\n' "$*"; }
sec() { printf '\n=== %s\n' "$*"; }

sec SELF
say "pid=$$ ppid=$P"
say "argv: $(tr '\0' '|' < /proc/self/cmdline)"
say "uid_map: $(tr '\n' ' ' < /proc/self/uid_map)"
grep -E '^(Uid|Gid|CapEff|NoNewPrivs|Seccomp):' /proc/self/status 2>&1

sec STDIN_INHERITED
say "readlink fd0: $(readlink /proc/self/fd/0)"
nb=$(timeout 2 head -c 65536 < /proc/self/fd/0 2>/dev/null | wc -c)
say "bytes_readable_on_fd0=$nb"
say "fd0_is_devnull=$([ "$(readlink /proc/self/fd/0)" = /dev/null ] && echo yes || echo no)"

sec SELF_FDS
ls -l /proc/self/fd 2>&1

sec ENV
env | sort

sec MOUNTS
say "-- btrfs entries in /proc/self/mountinfo:"
grep ' btrfs ' /proc/self/mountinfo 2>&1 | head -8
say "-- mount line(s) for /sys/fs/btrfs:"
grep -E ' /sys/fs/btrfs ' /proc/self/mountinfo 2>&1
awk '$2=="/sys/fs/btrfs"{print $1, $2, $3}' /proc/self/mounts 2>&1
say "-- mount line(s) for /sys/fs:"
grep -E ' /sys/fs ' /proc/self/mountinfo 2>&1

sec VIEW_TREE
say "-- /sys/fs/btrfs (path the arm is contracted to read):"
find /sys/fs/btrfs -maxdepth 3 2>&1 | head -40
say "-- /sys/fs listing:"
ls /sys/fs 2>&1

sec PARENT_PROC
timeout 60 python3 -u "$D/probe_proc.py" "$P" 2>&1
say "probe_proc_exit=$?"
exit 0
