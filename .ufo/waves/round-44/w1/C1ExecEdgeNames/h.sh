# shared harness functions (source me)
S=/fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames
RE='^SCRUB btrfs-scrub-record state=(NONE|RECORDED|BLOCKED) dir=(absent|present|unreadable) records=[0-9]+ tmp=[0-9]+ sockets=[0-9]+ unreadable=[0-9]+ orphan=[0-9]+ limited=[0-9]+ timers=[0-9]+( detail=[^[:space:]]+(,[^[:space:]]+)*)?$'
U=11111111-2222-3333-4444-555555555555
run() { # $1 label ; env vars must already be exported
  local lab=$1 o=$S/out/$1
  mkdir -p "$S/out"
  timeout "${RTO:-10}" bash "$S/drive.sh" "$S/census.lib.sh" >"$o.out" 2>"$o.err"
  local rc=$? nline line re_ok=no
  nline=$(wc -l < "$o.out")
  line=$(sed -n 's/^LINE //p' "$o.out")
  [[ $line =~ $RE ]] && re_ok=yes
  printf '=== %s rc=%s stdout_lines=%s contract_line=%s\n' "$lab" "$rc" "$nline" "$re_ok"
  printf '    %s\n' "${line:0:400}"
  [ "${#line}" -gt 400 ] && printf '    (line length %d chars, truncated for display)\n' "${#line}"
  printf '    probe_ms=%s\n' "$(sed -n 's/^MS //p' "$o.out")"
  [ -s "$o.err" ] && printf '    STDERR: %s\n' "$(tr '\n' '|' < "$o.err")"
}
mkenv() { # $1 case name -> sets FX
  FX=$S/fx/$1; rm -rf -- "$FX"; mkdir -p "$FX/scrub" "$FX/sysfs" "$FX/wants"
  export TSUKUROI_SCRUB_DIR=$FX/scrub TSUKUROI_BTRFS_SYSFS=$FX/sysfs TSUKUROI_TIMER_WANTS=$FX/wants
}
dev0() { # $1 sysfs root, $2 fsid  -> a healthy device with speed_max 0
  mkdir -p "$1/$2/devinfo/1"; printf '0\n' > "$1/$2/devinfo/1/scrub_speed_max"
}
