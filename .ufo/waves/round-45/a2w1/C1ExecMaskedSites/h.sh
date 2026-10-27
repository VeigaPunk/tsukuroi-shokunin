#!/usr/bin/env bash
# Harness: run the census at 18389f44 against a fixture tree (the revision's own
# selftest dispatcher + fx_default), with per-site padding injected by the caller.
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecMaskedSites
. "$S/fxfn.sh"   # fx_default() extracted verbatim from tools/tsukuroi-census.sh:2140-2229

mkfix() { local d=$1; mkdir -p "$d"; fx_default "$d"; }

run() { # run FX -> $OUT, $RC
  local FX=$1
  set +e
  OUT=$(env \
    TSUKUROI_FIXTURE="$FX" \
    TSUKUROI_PACMAN="$S/bin/pacman" \
    TSUKUROI_PACMAN_CONF="$S/bin/pacman-conf" \
    TSUKUROI_PACMAN_CONF_FILE="$FX/pacman.conf" \
    TSUKUROI_PACMAN_DB="$FX/pacmandb" \
    TSUKUROI_ROOT_DIR="$FX/root" \
    TSUKUROI_FOREIGN_BASELINE="$FX/fbase" \
    TSUKUROI_SYSTEMCTL="$S/bin/systemctl" \
    TSUKUROI_DMESG="$S/bin/dmesg" \
    TSUKUROI_JOURNALCTL="$S/bin/journalctl" \
    TSUKUROI_NVIDIA_SMI="$S/bin/nvidia-smi" \
    TSUKUROI_LSMOD="$S/bin/lsmod" \
    TSUKUROI_PCI_SYSFS="$FX/pci" \
    TSUKUROI_DEV_DIR="$FX/dev" \
    TSUKUROI_HOSTNAME_FILE="$FX/hostname" \
    TSUKUROI_DMESG_RESTRICT_FILE="$FX/dmesg_restrict" \
    TSUKUROI_CGROUP_ROOT="$FX/cgroup" \
    TSUKUROI_MEM_SLICE='user.slice/user-1000.slice' \
    TSUKUROI_PRESSURE_FILE="$FX/pressure/memory" \
    TSUKUROI_MEMINFO_FILE="$FX/meminfo" \
    TSUKUROI_VMSTAT_FILE="$FX/vmstat" \
    TSUKUROI_OOM_BASELINE="$FX/obase" \
    TSUKUROI_PACMAN_LOG="$FX/pacman.log" \
    TSUKUROI_ETC_DIR="$FX/etc" \
    TSUKUROI_BTRFS_SYSFS="$FX/btrfs" \
    TSUKUROI_PROC_MOUNTS="$FX/mounts" \
    TSUKUROI_SCRUB_DIR="$FX/scrub" \
    TSUKUROI_TIMER_WANTS="$FX/wants" \
    TSUKUROI_EXPAC="$S/bin/expac" \
    /usr/bin/bash "$S/census.sh" 2>&1)
  RC=$?
  set -e
}

field() { # field RE -> the first matching line of $OUT
  printf '%s\n' "$OUT" | grep -nE -- "$1" | head -n1
}

verdict() { printf '%s\n' "$OUT" | grep -E '^TSUKUROI_CENSUS:' | head -n1; }
