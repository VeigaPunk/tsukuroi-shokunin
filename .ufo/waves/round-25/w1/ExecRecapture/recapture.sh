#!/usr/bin/env bash
# Round 25 C2 cross-check re-capture: memory pressure (PSI) and systemd-oomd state.
# Read-only. No sudo. No service start/stop/restart. No configuration write.
# Writes only to the output file given as $1.
# Format is deliberately identical to .ufo/waves/round-25/capture/capture.sh
# so that both files can be parsed by the same comparator.
set -u
out=${1:?usage: recapture.sh <output-file>}
blk() { printf '### %s\n' "$1"; }
run() { printf '$ %s\n' "$*"; "$@" 2>&1; printf '[exit %s]\n' "$?"; }

# Units under test (same four as the frozen capture).
UNITS="user@1000.service user-1000.slice user.slice -.slice"

# Drop-in directories that could set ManagedOOM*=kill, plus the instance
# directories that a locally created override would land in.
DROPIN_DIRS="
/usr/lib/systemd/system/user@.service.d
/etc/systemd/system/user@.service.d
/usr/lib/systemd/system/user-.slice.d
/etc/systemd/system/user-.slice.d
/usr/lib/systemd/system/-.slice.d
/etc/systemd/system/-.slice.d
/usr/lib/systemd/system/user.slice.d
/etc/systemd/system/user.slice.d
/usr/lib/systemd/system/user@1000.service.d
/etc/systemd/system/user@1000.service.d
/usr/lib/systemd/system/user-1000.slice.d
/etc/systemd/system/user-1000.slice.d
/etc/systemd/system/systemd-oomd.service.d
/etc/systemd/system/systemd-oomd.socket.d
"

{
  blk header
  run date -u +%Y-%m-%dT%H:%M:%SZ
  run uname -r
  run systemctl --version

  blk system-memory-psi-read-1
  run cat /proc/pressure/memory
  run sleep 10

  blk system-memory-psi-read-2
  run cat /proc/pressure/memory
  run date -u +%Y-%m-%dT%H:%M:%SZ

  blk root-cgroup-memory-pressure
  run cat /sys/fs/cgroup/memory.pressure

  blk user-slice-memory-pressure
  run cat /sys/fs/cgroup/user.slice/memory.pressure
  run cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.pressure
  run cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.pressure

  blk user-slice-memory-events
  run cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.events
  run cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.swap.events

  blk kernel-oom-counter
  run grep -E '^oom_kill ' /proc/vmstat

  blk swap
  run grep -E '^(SwapTotal|SwapFree|MemTotal|MemAvailable):' /proc/meminfo

  blk oomd-unit
  run systemctl is-active systemd-oomd.service
  run systemctl is-enabled systemd-oomd.service
  run systemctl is-active systemd-oomd.socket
  run systemctl is-enabled systemd-oomd.socket

  blk oomd-config
  printf '$ systemd-analyze cat-config systemd/oomd.conf | grep -vcE "^(#|;|$)"  (count of active lines)\n'
  systemd-analyze cat-config systemd/oomd.conf 2>&1 | grep -vcE '^(#|;|$)'; printf '[exit %s]\n' "${PIPESTATUS[1]}"
  run systemd-analyze cat-config systemd/oomd.conf
  printf '$ ls -1 /etc/systemd/system/oomd.conf.d  (drop-ins for oomd.conf)\n'
  ls -1 /etc/systemd/system/oomd.conf.d 2>&1; printf '[exit %s]\n' "$?"

  blk managed-oom-properties
  for u in $UNITS; do
    run systemctl show -p ManagedOOMMemoryPressure -p ManagedOOMMemoryPressureLimit -p ManagedOOMMemoryPressureDurationUSec -p ManagedOOMSwap -p ManagedOOMPreference -p MemoryPressureWatch -p MemoryPressureThresholdUSec -- "$u"
  done

  blk manager-defaults
  run systemctl show -p DefaultMemoryPressureWatch -p DefaultMemoryPressureThresholdUSec

  blk managed-oom-dropin-dirs
  for d in $DROPIN_DIRS; do
    printf '$ ls -1 %s\n' "$d"
    if [ -d "$d" ]; then
      ls -1 "$d" 2>&1
      printf '[exit %s]\n' "$?"
    else
      printf '(absent)\n'
      printf '[exit 0]\n'
    fi
  done

  blk managed-oom-dropin-contents
  # For each unit, print the unit and drop-in file paths systemd resolves, then
  # only the ManagedOOM*/MemoryPressure* settings found inside them. Nothing
  # else from those files is printed.
  for u in $UNITS; do
    printf '$ systemctl cat %s  (paths only)\n' "$u"
    systemctl cat "$u" 2>/dev/null | grep -E '^(# /)' ; printf '[exit %s]\n' "$?"
    printf '$ grep -hE "ManagedOOM|MemoryPressure" over resolved unit+drop-in files for %s\n' "$u"
    files=$(systemctl cat "$u" 2>/dev/null | grep -E '^(# /)' | sed 's/^# //')
    if [ -n "$files" ]; then
      grep -hE 'ManagedOOM|MemoryPressure' $files 2>/dev/null
      printf '[exit %s]\n' "$?"
    else
      printf '(no resolvable unit or drop-in file)\n'
      printf '[exit 0]\n'
    fi
  done

  blk managed-oom-kill-search
  printf '$ grep -rlE "ManagedOOM(MemoryPressure|Swap)=kill" /etc/systemd/system /usr/lib/systemd/system 2>/dev/null\n'
  grep -rlE 'ManagedOOM(MemoryPressure|Swap)=kill' /etc/systemd/system /usr/lib/systemd/system 2>/dev/null
  printf '[exit %s]\n' "$?"

  blk end
  run date -u +%Y-%m-%dT%H:%M:%SZ
} > "$out"
sha256sum "$out"
