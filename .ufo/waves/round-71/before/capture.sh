#!/usr/bin/env bash
# round-71 C1 host capture — read-only, no privilege, no writes outside stdout.
# Emits the module-parameter surface this host actually presents, for the entry's
# host-applicability read. Run: bash capture.sh > host.txt
set -uo pipefail
printf '## date\n'; date -u +%Y-%m-%dT%H:%M:%SZ
printf '\n## kernel\n'; uname -r
printf '\n## modules with a parameters dir\n'
ls -d /sys/module/*/parameters 2>/dev/null | wc -l
printf '\n## parameter files\n'
ls /sys/module/*/parameters/* 2>/dev/null | wc -l
printf '\n## nvidia module parameter files (mode size name value)\n'
for m in nvidia nvidia_drm nvidia_modeset nvidia_uvm; do
  d=/sys/module/$m/parameters
  [ -d "$d" ] || { printf '%s absent\n' "$m"; continue; }
  for f in "$d"/*; do
    [ -e "$f" ] || continue
    v=$(tr -d '\n' < "$f" 2>/dev/null | cut -c1-60)
    printf '%s %s %s %s=%s\n' "$m" "$(stat -c '%A' "$f" 2>/dev/null)" "$(stat -c '%s' "$f" 2>/dev/null)" "${f##*/}" "$v"
  done
done
printf '\n## writable parameter files among the four nvidia modules\n'
for m in nvidia nvidia_drm nvidia_modeset nvidia_uvm; do
  for f in /sys/module/$m/parameters/*; do
    [ -w "$f" ] && printf '%s\n' "$f"
  done
done
printf '\n## /proc/cmdline\n'; cat /proc/cmdline
printf '\n## modprobe.d files (paths and modes only; contents never read)\n'
for d in /etc/modprobe.d /usr/lib/modprobe.d; do
  [ -d "$d" ] || { printf '%s absent\n' "$d"; continue; }
  find "$d" -maxdepth 1 -type f -printf '%m %p\n' 2>/dev/null | LC_ALL=C sort
done
printf '\n## btrfs read_policy (a perm==0 example named by S287)\n'
if [ -e /sys/module/btrfs/parameters/read_policy ]; then
  printf 'present\n'
else
  printf 'absent (perm==0 hides it)\n'
fi
