#!/usr/bin/env bash
# C1-10 runner: full census with the stub systemctl/nvidia-smi/lsmod, recorded rc + streams.
# usage: run-census.sh <label> <census-path> <pad-lines>
set +e
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecFullLarge
F=$S/fx; B=$S/bin
label=$1 cen=$2 pad=$3
env FX="$F" PAD_LINES="$pad" \
    TSUKUROI_SYSTEMCTL="$B/systemctl" TSUKUROI_NVIDIA_SMI="$B/nvidia-smi" \
    TSUKUROI_LSMOD="$B/lsmod" TSUKUROI_PCI_SYSFS="$F/pci" TSUKUROI_DEV_DIR="$F/dev" \
    TSUKUROI_CGROUP_ROOT=/sys/fs/cgroup TSUKUROI_PRESSURE_FILE=/proc/pressure/memory \
    TSUKUROI_MEMINFO_FILE=/proc/meminfo \
    TSUKUROI_FIXTURE= TMPDIR="$S/s" CALLS="${CALLS:-}" \
    bash "$cen" > "$S/$label.out" 2> "$S/$label.err"
rc=$?
printf '%s\n' "$rc" > "$S/$label.rc"
printf '%s exit=%s stdout_bytes=%s stderr_bytes=%s\n' "$label" "$rc" \
  "$(wc -c < "$S/$label.out")" "$(wc -c < "$S/$label.err")"
exit 0
