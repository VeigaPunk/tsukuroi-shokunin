#!/usr/bin/env bash
# C1ExecFinalPlaneDiff driver: alternating live census runs, base 98020ece vs tip 8eee79db.
# Read-only: the census is the read-only gate itself; this driver only writes under its own out/.
set -u
ROOT=/fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalPlaneDiff
export TMPDIR=$ROOT/s
mkdir -p "$TMPDIR" "$ROOT/out"
cd "$ROOT" || exit 9
: > "$ROOT/out/timing.txt"
: > "$ROOT/out/rc.txt"
: > "$ROOT/out/headers.txt"

run_one() { # run_one REV N
  local rev=$1 n=$2 t0 t1
  t0=$(date -u +%FT%TZ)
  timeout 300 /usr/bin/bash "$ROOT/bin/$rev.sh" > "$ROOT/out/out-$rev-$n.txt" 2> "$ROOT/out/err-$rev-$n.txt"
  local rc=$?
  t1=$(date -u +%FT%TZ)
  printf '%s\n' "$rc" > "$ROOT/out/rc-$rev-$n.txt"
  printf '%s-%s start=%s end=%s rc=%s lines=%s stderr_bytes=%s\n' "$rev" "$n" "$t0" "$t1" "$rc" "$(wc -l < "$ROOT/out/out-$rev-$n.txt")" "$(wc -c < "$ROOT/out/err-$rev-$n.txt")" >> "$ROOT/out/timing.txt"
  printf '%s\t%s\t%s\n' "$rev-$n" "$(head -n1 "$ROOT/out/out-$rev-$n.txt")" "$rc" >> "$ROOT/out/headers.txt"
  printf 'rc-%s-%s=%s\n' "$rev" "$n" "$rc" >> "$ROOT/out/rc.txt"
}

# snapshot a few live trees before the batch (no writes; /var/lib/btrfs is absent today)
snap() {
  local out=$1
  {
    for p in /var/lib/btrfs /sys/fs/btrfs /etc/systemd/system/timers.target.wants; do
      if [ -e "$p" ]; then printf 'E %s %s\n' "$p" "$(stat -c '%F %a %u:%g %y' "$p")"
      else printf 'A %s\n' "$p"; fi
    done
    ls -a /sys/fs/btrfs 2>&1 | sed 's/^/sysfs: /'
    ls -a /etc/systemd/system/timers.target.wants 2>&1 | sed 's/^/wants: /'
    ls -a /var/lib 2>/dev/null | grep -c '^btrfs' | sed 's/^/varlib-btrfs-entries: /'
  } > "$out"
}
snap "$ROOT/out/snap-before.txt"

run_one base 1
run_one tip 1
run_one base 2
run_one tip 2
run_one base 3
run_one tip 3

snap "$ROOT/out/snap-after.txt"
printf 'tmpdir-entries-after=%s\n' "$(ls -A "$TMPDIR" 2>/dev/null | wc -l)" > "$ROOT/out/tmpdir.txt"
exit 0
