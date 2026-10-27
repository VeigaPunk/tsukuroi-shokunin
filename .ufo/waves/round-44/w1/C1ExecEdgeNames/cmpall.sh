#!/usr/bin/env bash
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames
UL=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
FX=$S/fx/allcmp
line_of() { timeout 30 bash "$S/drive.sh" "$1" 2>/dev/null | sed -n 's/^LINE //p'; }
show() { local a b; a=$(line_of "$S/census.lib.sh"); b=$(line_of "$S/census.all.lib.sh")
  printf '== %s\n   arm    : %s\n   patched: %s\n' "$1" "$a" "$b"; }
setup() { rm -rf -- "$FX"; mkdir -p "$FX/scrub" "$FX/sysfs" "$FX/wants"; export TSUKUROI_SCRUB_DIR=$FX/scrub TSUKUROI_BTRFS_SYSFS=$FX/sysfs TSUKUROI_TIMER_WANTS=$FX/wants; }
dev0() { mkdir -p "$1/$2/devinfo/1"; printf '0\n' > "$1/$2/devinfo/1/scrub_speed_max"; }

setup; rm -rf -- "$FX/sysfs"; : > "$FX/sysfs"; : > "$FX/scrub/scrub.status.$UL"; show "G1 non-dir sysfs root"
setup; mkdir -p "$FX/wants/btrfs-scrub@data.timer"; show "G2 timer is a directory"
setup; ln -s /usr/lib/systemd/system/gone.timer "$FX/wants/btrfs-scrub@data.timer"; show "G2b timer is a dangling link"
setup; ln -s /usr/lib/systemd/system/btrfs-scrub@.timer "$FX/wants/btrfs-scrub@home.timer"; : > "$FX/wants/btrfs-scrub@.timer"; : > "$FX/wants/fstrim.timer"; show "G2c selftest timer shape (must be timers=2)"
setup; mkdir -p "$FX/sysfs/$UL/devinfo/1"; printf '77\n' > "$FX/out"; ln -s "$FX/out" "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"; show "G3 symlink speed_max"
setup; mkdir -p "$FX/sysfs/$UL"; : > "$FX/scrub/scrub.status.$UL"; show "G4 fsid without devinfo"
setup; dev0 "$FX/sysfs" "$UL"; : > "$FX/scrub/scrub.status.$UL"; : > "$FX/scrub/scrub.status.${UL}_tmp"; ( cd "$FX/scrub" && python3 -c 'import socket; s=socket.socket(socket.AF_UNIX); s.bind("scrub.progress.'"$UL"'")' ); : > "$FX/wants/btrfs-scrub@monthly.timer"; show "regress H6: all three kinds + a FILE timer (now not-link)"
setup; ln -s /usr/lib/systemd/system/btrfs-scrub@.timer "$FX/wants/btrfs-scrub@monthly.timer"; dev0 "$FX/sysfs" "$UL"; : > "$FX/scrub/scrub.status.$UL"; show "regress H6b: all three kinds + a LINK timer (healthy)"
setup; rm -rf -- "$FX/sysfs"; : > "$FX/scrub/scrub.status.$UL"; show "regress H3: sysfs absent with a record"
setup; show "regress H1: empty fixtures"
setup; mkdir -p "$FX/sysfs/$UL/devinfo/1"; mkfifo "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"; show "regress C1: FIFO speed_max"
setup; dev0 "$FX/sysfs" "${UL^^}"; : > "$FX/scrub/scrub.status.$UL"; show "regress A2: uppercase sysfs fsid"
