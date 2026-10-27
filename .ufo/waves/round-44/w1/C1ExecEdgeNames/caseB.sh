#!/usr/bin/env bash
set -uo pipefail
. /fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames/h.sh
UL=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee

# ---- B: SCRUB_DIR shapes ----
mkenv B1-dangling-symlink-dir
rm -rf -- "$FX/scrub"; ln -s "$FX/nonexistent-target" "$FX/scrub"
run B1-dangling-symlink-dir

mkenv B2-dir-is-regular-file
rm -rf -- "$FX/scrub"; : > "$FX/scrub"
run B2-dir-is-regular-file

mkenv B3-dir-absent
rm -rf -- "$FX/scrub"
run B3-dir-absent

mkenv B4-dir-mode000
touch -- "$FX/scrub/scrub.status.$UL"; chmod 000 "$FX/scrub"
run B4-dir-mode000
chmod 755 "$FX/scrub"

# ---- C: sysfs shapes ----
mkenv C1-fifo-speedmax
mkdir -p "$FX/sysfs/$UL/devinfo/1"; mkfifo "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
run C1-fifo-speedmax

mkenv C2-symlink-speedmax-devzero
mkdir -p "$FX/sysfs/$UL/devinfo/1"; ln -s /dev/zero "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
run C2-symlink-speedmax-devzero

mkenv C3-symlink-speedmax-regular
mkdir -p "$FX/sysfs/$UL/devinfo/1"; printf '77\n' > "$FX/outside"; ln -s "$FX/outside" "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
run C3-symlink-speedmax-regular

mkenv C4-no-speedmax
mkdir -p "$FX/sysfs/$UL/devinfo/1"
run C4-no-speedmax

mkenv C5-empty-speedmax
mkdir -p "$FX/sysfs/$UL/devinfo/1"; : > "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
run C5-empty-speedmax

mkenv C6-two-lines
mkdir -p "$FX/sysfs/$UL/devinfo/1"; printf '5\n6\n' > "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
run C6-two-lines

mkenv C7-speedmax-is-dir
mkdir -p "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
run C7-speedmax-is-dir

mkenv C8-sysfs-root-is-file
rm -rf -- "$FX/sysfs"; : > "$FX/sysfs"
touch -- "$FX/scrub/scrub.status.$UL"
run C8-sysfs-root-is-file

mkenv C9-fsid-without-devinfo
mkdir -p "$FX/sysfs/$UL"
touch -- "$FX/scrub/scrub.status.$UL"
run C9-fsid-without-devinfo

mkenv C10-devid-nondecimal
mkdir -p "$FX/sysfs/$UL/devinfo/1a"; printf '0\n' > "$FX/sysfs/$UL/devinfo/1a/scrub_speed_max"
run C10-devid-nondecimal

mkenv C11-sysfs-mode000
mkdir -p "$FX/sysfs/$UL/devinfo/1"; printf '0\n' > "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"; chmod 000 "$FX/sysfs"
run C11-sysfs-mode000
chmod 755 "$FX/sysfs"

# ---- G: record/tmp/socket file types ----
mkenv G1-progress-regular
: > "$FX/scrub/scrub.progress.$UL"
run G1-progress-regular

mkenv G2-record-is-socket
python3 -c 'import socket,sys; s=socket.socket(socket.AF_UNIX); s.bind(sys.argv[1])' "$FX/scrub/scrub.status.$UL"
run G2-record-is-socket

mkenv G3-record-is-symlink
: > "$FX/outside2"; ln -s "$FX/outside2" "$FX/scrub/scrub.status.$UL"
run G3-record-is-symlink

mkenv G4-record-is-fifo
mkfifo "$FX/scrub/scrub.status.$UL"
run G4-record-is-fifo

mkenv G5-record-unreadable
: > "$FX/scrub/scrub.status.$UL"; chmod 000 "$FX/scrub/scrub.status.$UL"
dev0 "$FX/sysfs" "$UL"
run G5-record-unreadable
chmod 644 "$FX/scrub/scrub.status.$UL"

mkenv G6-tmp-unreadable
: > "$FX/scrub/scrub.status.${UL}_tmp"; chmod 000 "$FX/scrub/scrub.status.${UL}_tmp"
dev0 "$FX/sysfs" "$UL"
run G6-tmp-unreadable
chmod 644 "$FX/scrub/scrub.status.${UL}_tmp"

mkenv G7-control-healthy
dev0 "$FX/sysfs" "$UL"; : > "$FX/scrub/scrub.status.$UL"
run G7-control-healthy
