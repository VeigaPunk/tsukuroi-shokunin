#!/usr/bin/env bash
# round-72 pre-declaration host capture — read-only; paths and modes only, never config contents.
set -u
echo "# round-72 host capture ($(date -Iseconds))"
echo "## kernel"; uname -r
echo "## kmod"; modprobe --version 2>&1 | head -3
echo "## config directories (path + mode; contents never read)"
for d in /etc/modprobe.d /run/modprobe.d /usr/local/lib/modprobe.d /usr/lib/modprobe.d /lib/modprobe.d; do
  if [ -e "$d" ] || [ -L "$d" ]; then stat -c '%A %U:%G %n -> %N' "$d"; else echo "ABSENT $d"; fi
done
echo "## /lib resolution"; readlink -f /lib; readlink -f /usr/lib/modprobe.d 2>/dev/null || true
echo "## names only (ls, no file reads)"
for d in /etc/modprobe.d /usr/lib/modprobe.d; do [ -d "$d" ] && { echo "-- $d"; ls -1 "$d"; }; done
echo "## cmdline"; cat /proc/cmdline
echo "## loaded modules touching nvidia/bluetooth (names only)"
lsmod | awk 'NR==1 || /^(nvidia|btusb|bluetooth)/ {print $1, $3}'
echo "## /sys/module parameter dirs"; ls -d /sys/module/*/parameters 2>/dev/null | wc -l
