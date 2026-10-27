#!/usr/bin/env bash
set -uo pipefail
. /fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames/h.sh
UL=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee

rune() { # $1 label : same as run() but under set -euo pipefail
  local lab=$1 o=$S/out/$1
  timeout "${RTO:-10}" bash "$S/drive_e.sh" "$S/census.lib.sh" >"$o.out" 2>"$o.err"
  local rc=$? line re_ok=no
  line=$(sed -n 's/^LINE //p' "$o.out")
  [[ $line =~ $RE ]] && re_ok=yes
  printf '=== %s rc=%s stdout_lines=%s contract_line=%s probe_ms=%s\n' "$lab" "$rc" "$(wc -l < "$o.out")" "$re_ok" "$(sed -n 's/^MS //p' "$o.out")"
  printf '    %s\n' "${line:0:400}"
  [ -s "$o.err" ] && printf '    STDERR: %s\n' "$(tr '\n' '|' < "$o.err")"
}

mkenv H1-seteu-empty-dirs
rune H1-seteu-empty-dirs

mkenv H2-seteu-sysfs-absent-no-records
rm -rf -- "$FX/sysfs"
rune H2-seteu-sysfs-absent-no-records

mkenv H3-sysfs-absent-with-record
rm -rf -- "$FX/sysfs"; : > "$FX/scrub/scrub.status.$UL"
rune H3-sysfs-absent-with-record

mkenv H4-wants-absent
rm -rf -- "$FX/wants"
rune H4-wants-absent

mkenv H5-combined-reasons-and-limited
chmod 000 "$FX/sysfs" 2>/dev/null
mkdir -p "$FX/sysfs2"
chmod 755 "$FX/sysfs"
mkdir -p "$FX/sysfs/$UL/devinfo/1"; printf '4096\n' > "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
: > "$FX/scrub/scrub.progress.$UL"
rm -rf -- "$FX/wants"; : > "$FX/wants"
rune H5-combined-reasons-and-limited

mkenv H6-all-three-kinds
dev0 "$FX/sysfs" "$UL"
: > "$FX/scrub/scrub.status.$UL"
: > "$FX/scrub/scrub.status.${UL}_tmp"
( cd "$FX/scrub" && python3 -c 'import socket; s=socket.socket(socket.AF_UNIX); s.bind("scrub.progress.'"$UL"'")' )
: > "$FX/wants/btrfs-scrub@monthly.timer"
rune H6-all-three-kinds

mkenv H7-seteu-fifo-speedmax
mkdir -p "$FX/sysfs/$UL/devinfo/1"; mkfifo "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
rune H7-seteu-fifo-speedmax

echo "=== H8 default-path resolution with overrides unset (no host read) ==="
env -u TSUKUROI_SCRUB_DIR -u TSUKUROI_BTRFS_SYSFS -u TSUKUROI_TIMER_WANTS bash -c '. /fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames/census.lib.sh; printf "    SCRUB_DIR=%s BTRFS_SYSFS=%s TIMER_WANTS=%s\n" "$SCRUB_DIR" "$BTRFS_SYSFS" "$TIMER_WANTS"' 2>&1

mkenv H9-seteu-4000-records
python3 - "$FX" <<'PY'
import os,sys
fx=sys.argv[1]
for i in range(4000):
    f=f"{i:08x}-1111-2222-3333-{i:012x}"
    open(os.path.join(fx,"scrub","scrub.status."+f),"w").close()
    d=os.path.join(fx,"sysfs",f,"devinfo","1"); os.makedirs(d)
    open(os.path.join(d,"scrub_speed_max"),"w").write("0\n")
PY
RTO=120 rune H9-seteu-4000-records
