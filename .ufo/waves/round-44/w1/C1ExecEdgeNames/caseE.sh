#!/usr/bin/env bash
set -uo pipefail
. /fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames/h.sh
UL=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee

# ---- D6: oversized attribute payloads (fixture-only reachability) ----
mkenv D6-8MiB-single-line
mkdir -p "$FX/sysfs/$UL/devinfo/1"
head -c 8388608 /dev/zero | tr '\0' '7' > "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
RTO=60 run D6-8MiB-single-line

mkenv D6b-4MiB-many-lines
mkdir -p "$FX/sysfs/$UL/devinfo/1"
head -c 4194304 /dev/zero | tr '\0' '1' | fold -w1 | sed 's/$/\n/' > "$FX/sysfs/$UL/devinfo/1/scrub_speed_max" 2>/dev/null || true
awk 'BEGIN{for(i=0;i<2000000;i++) print "1"}' > "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
printf '    lines=%s bytes=%s\n' "$(wc -l < "$FX/sysfs/$UL/devinfo/1/scrub_speed_max")" "$(wc -c < "$FX/sysfs/$UL/devinfo/1/scrub_speed_max")"
RTO=120 run D6b-2M-lines

# ---- E: 1000 records ----
mkenv E1-1000-records-1000-fsids
python3 - "$FX" <<'PY'
import os,sys,uuid
fx=sys.argv[1]
for i in range(1000):
    f=f"{i:08x}-1111-2222-3333-{i:012x}"
    open(os.path.join(fx,"scrub","scrub.status."+f),"w").close()
    d=os.path.join(fx,"sysfs",f,"devinfo","1"); os.makedirs(d)
    open(os.path.join(d,"scrub_speed_max"),"w").write("0\n")
PY
RTO=60 run E1-1000-records-1000-fsids

mkenv E2-1000-records-empty-sysfs
python3 - "$FX" <<'PY'
import os,sys
fx=sys.argv[1]
for i in range(1000):
    open(os.path.join(fx,"scrub",f"scrub.status.{i:08x}-1111-2222-3333-{i:012x}"),"w").close()
PY
RTO=60 run E2-1000-records-empty-sysfs

mkenv E3-1000-timers
python3 - "$FX" <<'PY'
import os,sys
fx=sys.argv[1]
for i in range(1000):
    open(os.path.join(fx,"wants",f"btrfs-scrub@d{i}.timer"),"w").close()
PY
RTO=60 run E3-1000-timers

# ---- F: timers ----
mkenv F1-timer-is-directory
mkdir -p "$FX/wants/btrfs-scrub@data.timer"
run F1-timer-is-directory

mkenv F2-timer-dangling-symlink
ln -s /usr/lib/systemd/system/gone.timer "$FX/wants/btrfs-scrub@data.timer"
run F2-timer-dangling-symlink

mkenv F3-bare-template
: > "$FX/wants/btrfs-scrub@.timer"
run F3-bare-template

mkenv F4-wants-is-regular-file
rm -rf -- "$FX/wants"; : > "$FX/wants"
run F4-wants-is-regular-file

mkenv F5-nonmatching-names
: > "$FX/wants/btrfs-scrub@x.timer.bak"
: > "$FX/wants/btrfs-scrub@x.service"
: > "$FX/wants/btrfs-scrub@.service"
: > "$FX/wants/xbtrfs-scrub@y.timer"
: > "$FX/wants/btrfs-scrub@x.TIMER"
run F5-nonmatching-names

mkenv F6-newline-instance
: > "$FX/wants/btrfs-scrub@"$'\n'".timer"
run F6-newline-instance

# ---- G2 redo: sockaddr_un path limit avoided by relative bind ----
mkenv G2-record-is-socket
( cd "$FX/scrub" && python3 -c 'import socket; s=socket.socket(socket.AF_UNIX); s.bind("scrub.status.'"$UL"'")' )
run G2-record-is-socket

mkenv G2b-progress-socket
( cd "$FX/scrub" && python3 -c 'import socket; s=socket.socket(socket.AF_UNIX); s.bind("scrub.progress.'"$UL"'")' )
run G2b-progress-socket
