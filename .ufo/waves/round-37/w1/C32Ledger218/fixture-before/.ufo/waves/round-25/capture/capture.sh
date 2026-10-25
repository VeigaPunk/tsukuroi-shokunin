#!/usr/bin/env bash
# Round 25 C2 host capture: memory pressure (PSI) and systemd-oomd state.
# Read-only: no sudo, no writes outside the output file given as $1, no service or config change.
set -u
out=${1:?usage: capture.sh <output-file>}
blk() { printf '### %s\n' "$1"; }
run() { printf '$ %s\n' "$*"; "$@" 2>&1; printf '[exit %s]\n' "$?"; }
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
  run systemctl is-enabled systemd-oomd.socket
  blk oomd-config
  printf '$ systemd-analyze cat-config systemd/oomd.conf | grep -vcE "^(#|;|$)"  (count of active lines)\n'
  systemd-analyze cat-config systemd/oomd.conf 2>&1 | grep -vcE '^(#|;|$)'; printf '[exit %s]\n' "${PIPESTATUS[1]}"
  run systemd-analyze cat-config systemd/oomd.conf
  blk managed-oom-properties
  for u in user@1000.service user-1000.slice user.slice -.slice; do
    run systemctl show -p ManagedOOMMemoryPressure -p ManagedOOMMemoryPressureLimit -p ManagedOOMMemoryPressureDurationUSec -p ManagedOOMSwap -p ManagedOOMPreference -p MemoryPressureWatch -p MemoryPressureThresholdUSec -- "$u"
  done
  blk manager-defaults
  run systemctl show -p DefaultMemoryPressureWatch -p DefaultMemoryPressureThresholdUSec
  blk end
  run date -u +%Y-%m-%dT%H:%M:%SZ
} > "$out"
sha256sum "$out"
