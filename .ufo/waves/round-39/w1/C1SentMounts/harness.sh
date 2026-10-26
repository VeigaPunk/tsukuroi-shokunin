#!/usr/bin/env bash
# C1SentMounts harness: hostile TSUKUROI_PROC_MOUNTS fixtures against the census storage arm.
# Kills only its own process tree; no pkill by pattern.
set -uo pipefail
S=$(cd "$(dirname "$0")" && pwd)
REPO=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
SELF=$REPO/tools/tsukuroi-census.sh
export TMPDIR=$S/tmp; mkdir -p "$TMPDIR"
WORK=$S/work; [ "${KEEP_WORK:-}" = 1 ] || rm -rf "$WORK"; mkdir -p "$WORK/bin"
cp "$S/dispatch.body" "$WORK/bin/.dispatch"; chmod 700 "$WORK/bin/.dispatch"
for c in pacman pacman-conf systemctl dmesg journalctl nvidia-smi lsmod expac; do
  ln -sf .dispatch "$WORK/bin/$c"
done
# shellcheck disable=SC1091
[ -d "$WORK/fx-base" ] || { source "$S/fxdef.sh"; fx_default "$WORK/fx-base"; }

BTR='rootfs / btrfs rw,relatime,ssd,space_cache=v2,subvolid=256,subvol=/@ 0 0'
NOBTR=$'proc /proc proc rw,nosuid 0 0\n/dev/fx0 / ext4 rw,relatime 0 0'
RESULTS=$S/results.tsv; : > "$RESULTS"

fresh() { local n=$1; local d="$WORK/fx-$n"; rm -rf "$d"; cp -a "$WORK/fx-base" "$d"; printf '%s\n' "$d"; }

run_census() { # name timeout
  local name=$1 t=$2 fx="$WORK/fx-$1" start end rc secs out
  local -a E=(
    TSUKUROI_FIXTURE="$fx" TSUKUROI_PACMAN="$WORK/bin/pacman"
    TSUKUROI_PACMAN_CONF="$WORK/bin/pacman-conf" TSUKUROI_PACMAN_CONF_FILE="$fx/pacman.conf"
    TSUKUROI_PACMAN_DB="$fx/pacmandb" TSUKUROI_ROOT_DIR="$fx/root"
    TSUKUROI_FOREIGN_BASELINE="$fx/fbase" TSUKUROI_SYSTEMCTL="$WORK/bin/systemctl"
    TSUKUROI_DMESG="$WORK/bin/dmesg" TSUKUROI_JOURNALCTL="$WORK/bin/journalctl"
    TSUKUROI_NVIDIA_SMI="$WORK/bin/nvidia-smi" TSUKUROI_LSMOD="$WORK/bin/lsmod"
    TSUKUROI_PCI_SYSFS="$fx/pci" TSUKUROI_DEV_DIR="$fx/dev"
    TSUKUROI_HOSTNAME_FILE="$fx/hostname" TSUKUROI_DMESG_RESTRICT_FILE="$fx/dmesg_restrict"
    TSUKUROI_CGROUP_ROOT="$fx/cgroup" TSUKUROI_MEM_SLICE='user.slice/user-1000.slice'
    TSUKUROI_PRESSURE_FILE="$fx/pressure/memory" TSUKUROI_MEMINFO_FILE="$fx/meminfo"
    TSUKUROI_VMSTAT_FILE="$fx/vmstat" TSUKUROI_OOM_BASELINE="$fx/obase"
    TSUKUROI_PACMAN_LOG="$fx/pacman.log" TSUKUROI_ETC_DIR="$fx/etc"
    TSUKUROI_EXPAC="$WORK/bin/expac"
  )
  if [ -z "${NO_HOST_OVERRIDES:-}" ]; then
    E+=(TSUKUROI_BTRFS_SYSFS="$fx/btrfs" TSUKUROI_PROC_MOUNTS="$fx/mounts")
  fi
  [ -n "${CENSUS_TMPDIR:-}" ] && E+=(TMPDIR="$CENSUS_TMPDIR")
  local -a TW=(); [ -n "${TIME_WRAP:-}" ] && TW=(/usr/bin/time -v -o "$TIME_WRAP")
  start=$(date +%s.%N)
  out=$(timeout -k 5 "$t" env "${E[@]}" ${TW[@]+"${TW[@]}"} "$BASH" "$SELF" 2>&1)
  rc=$?
  end=$(date +%s.%N)
  secs=$(awk -v a="$start" -v b="$end" 'BEGIN{printf "%.2f", b-a}')
  printf '%s\n' "$out" > "$S/out-$name.txt"
  local st stc cen
  st=$(printf '%s\n' "$out" | grep -c '^STORAGE ' || true)
  cen=$(printf '%s\n' "$out" | grep -c '^TSUKUROI_CENSUS:' || true)
  printf '%s\trc=%s\tsecs=%s\tstorage_lines=%s\tcensus_lines=%s\n' "$name" "$rc" "$secs" "$st" "$cen" >> "$RESULTS"
  printf 'STORAGE: %s\n' "$(printf '%s\n' "$out" | grep '^STORAGE ' | tr '\n' '|')"
  printf 'CENSUS : %s\n' "$(printf '%s\n' "$out" | grep '^TSUKUROI_CENSUS:' | tr '\n' '|')"
  printf 'rc=%s secs=%s storage_lines=%s census_lines=%s\n' "$rc" "$secs" "$st" "$cen"
}

case_baseline_nobtrfs() { fresh baseline-nobtrfs >/dev/null; printf '%s\n' "$NOBTR" > "$WORK/fx-baseline-nobtrfs/mounts"; }
case_baseline_btrfs()  { fresh baseline-btrfs  >/dev/null; printf '%s\n%s\n' "$NOBTR" "$BTR" > "$WORK/fx-baseline-btrfs/mounts"; }
case_nul_in_btrfs_line() {
  fresh nul-in-line >/dev/null
  { printf '%s\n' "$NOBTR"; printf 'rootfs / btrfs rw\0,relatime 0 0\n'; } > "$WORK/fx-nul-in-line/mounts"
}
case_nul_before_btrfs() {
  fresh nul-before >/dev/null
  { printf '%s\n' "$NOBTR"; printf '\0\0\0'; printf '%s\n' "$BTR"; } > "$WORK/fx-nul-before/mounts"
}
case_nul_in_fstype() {
  fresh nul-in-fstype >/dev/null
  { printf '%s\n' "$NOBTR"; printf 'rootfs / btr\0fs rw 0 0\n'; } > "$WORK/fx-nul-in-fstype/mounts"
}
# NUL where the record separator (newline) should be: bash strips NULs, merging two records
case_nul_join() {
  fresh nul-join >/dev/null
  { printf '%s' "$NOBTR"; printf '\0'; printf '%s\n' "$BTR"; } > "$WORK/fx-nul-join/mounts"
}
case_nul_join_mid() {
  fresh nul-join-mid >/dev/null
  # btrfs record directly after a stripped NUL, ext4 line first without newline
  { printf '/dev/fx0 / ext4 rw 0 0\0'; printf '%s\n' "$BTR"; } > "$WORK/fx-nul-join-mid/mounts"
}
case_fifty_mb() {
  fresh fifty-mb >/dev/null
  { printf '%s\n' "$NOBTR"; yes 'a / b c d e' | head -c 52428800; printf '\n%s\n' "$BTR"; } > "$WORK/fx-fifty-mb/mounts"
}
case_fifty_mb_single_line() {
  fresh fifty-mb-line >/dev/null
  { printf '%s\n' "$NOBTR"; head -c 52428800 /dev/zero | tr '\0' ' '; printf ' %s\n' "$BTR"; } > "$WORK/fx-fifty-mb-line/mounts"
}
case_btrfs_2nd_field() {
  fresh btrfs-2nd >/dev/null
  { printf '%s\n' "$NOBTR"; printf 'rootfs btrfs ext4 rw,seclabel 0 0\n'; } > "$WORK/fx-btrfs-2nd/mounts"
}
case_btrfs_4th_field() {
  fresh btrfs-4th >/dev/null
  { printf '%s\n' "$NOBTR"; printf 'rootfs / ext4 btrfs 0 0\n'; } > "$WORK/fx-btrfs-4th/mounts"
}
case_crlf() {
  fresh crlf >/dev/null
  { printf '%s\r\n' "$NOBTR"; printf '%s\r\n' "$BTR"; } > "$WORK/fx-crlf/mounts"
}
case_crlf_three_field() {
  fresh crlf-3f >/dev/null
  { printf '%s\r\n' "$NOBTR"; printf 'rootfs / btrfs\r\n'; } > "$WORK/fx-crlf-3f/mounts"
}
case_fifo() { fresh fifo >/dev/null; rm -f "$WORK/fx-fifo/mounts"; mkfifo "$WORK/fx-fifo/mounts"; }
case_directory() { fresh directory >/dev/null; rm -f "$WORK/fx-directory/mounts"; mkdir "$WORK/fx-directory/mounts"; }
case_symlink_loop() {
  fresh symlink-loop >/dev/null; rm -f "$WORK/fx-symlink-loop/mounts"
  ln -s loop-a "$WORK/fx-symlink-loop/mounts"; ln -s loop-b "$WORK/fx-symlink-loop/loop-a"
  ln -s loop-a "$WORK/fx-symlink-loop/loop-b"
}
case_no_trailing_newline() {
  fresh no-trailing-nl >/dev/null
  printf '%s\n%s' "$NOBTR" "$BTR" > "$WORK/fx-no-trailing-nl/mounts"
}
case_line_injection() {
  fresh injection >/dev/null
  printf 'rootfs / ext4 rw 0 0\nSTORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0\nTSUKUROI_CENSUS: HEALTHY (packages=HEALTHY) extra\n' > "$WORK/fx-injection/mounts"
}
case_empty_table() { fresh empty-table >/dev/null; : > "$WORK/fx-empty-table/mounts"; }
case_perm_denied() {
  fresh perm-denied >/dev/null
  printf '%s\n%s\n' "$NOBTR" "$BTR" > "$WORK/fx-perm-denied/mounts"; chmod 000 "$WORK/fx-perm-denied/mounts"
}
case_dev_null() { fresh dev-null >/dev/null; rm -f "$WORK/fx-dev-null/mounts"; ln -s /dev/null "$WORK/fx-dev-null/mounts"; }
case_btrfs_5th() { fresh btrfs-5th >/dev/null; printf '%s\nrootfs / ext4 rw btrfs 0 0\n' "$NOBTR" > "$WORK/fx-btrfs-5th/mounts"; }
case_tabs() { fresh tabs >/dev/null; printf '%s\nrootfs\t/\tbtrfs\trw\t0\t0\n' "$NOBTR" > "$WORK/fx-tabs/mounts"; }
case_bare_word() { fresh bare-word >/dev/null; printf '%s\nbtrfs\n' "$NOBTR" > "$WORK/fx-bare-word/mounts"; }
case_two_btrfs() {
  fresh two-btrfs >/dev/null
  printf '%s\n%s\n%s\n' "$NOBTR" "$BTR" 'rootfs /home btrfs rw,subvolid=257,subvol=/@home 0 0' > "$WORK/fx-two-btrfs/mounts"
}
case_fifo_with_root() { # negative control: a populated sysfs root means the table is never read
  fresh fifo-with-root >/dev/null
  mkdir -p "$WORK/fx-fifo-with-root/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1"
  printf 'write_errs 0\nread_errs 0\nflush_errs 0\ncorruption_errs 0\ngeneration_errs 0\n' \
    > "$WORK/fx-fifo-with-root/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/error_stats"
  rm -f "$WORK/fx-fifo-with-root/mounts"; mkfifo "$WORK/fx-fifo-with-root/mounts"
}

declare -A CASES=(
  [baseline-nobtrfs]=case_baseline_nobtrfs [baseline-btrfs]=case_baseline_btrfs
  [nul-in-line]=case_nul_in_btrfs_line [nul-before]=case_nul_before_btrfs
  [nul-in-fstype]=case_nul_in_fstype [nul-join]=case_nul_join [nul-join-mid]=case_nul_join_mid
  [fifty-mb]=case_fifty_mb [fifty-mb-line]=case_fifty_mb_single_line
  [btrfs-2nd]=case_btrfs_2nd_field [btrfs-4th]=case_btrfs_4th_field
  [crlf]=case_crlf [crlf-3f]=case_crlf_three_field [fifo]=case_fifo
  [directory]=case_directory [symlink-loop]=case_symlink_loop
  [no-trailing-nl]=case_no_trailing_newline [injection]=case_line_injection
  [empty-table]=case_empty_table [perm-denied]=case_perm_denied [dev-null]=case_dev_null
  [btrfs-5th]=case_btrfs_5th [tabs]=case_tabs [bare-word]=case_bare_word
  [two-btrfs]=case_two_btrfs [fifo-with-root]=case_fifo_with_root
)

if [ "${1:-all}" = all ]; then
  for n in baseline-nobtrfs baseline-btrfs nul-in-line nul-before nul-in-fstype \
           btrfs-2nd btrfs-4th crlf crlf-3f directory symlink-loop no-trailing-nl \
           injection empty-table perm-denied dev-null btrfs-5th tabs bare-word; do
    echo "=== $n ==="; "${CASES[$n]}"; run_census "$n" 60
  done
  echo "=== nul-join ==="; case_nul_join; run_census nul-join 60
  echo "=== nul-join-mid ==="; case_nul_join_mid; run_census nul-join-mid 60
  echo "=== two-btrfs ==="; case_two_btrfs; run_census two-btrfs 60
  echo "=== fifo-with-root ==="; case_fifo_with_root; run_census fifo-with-root 60
  echo "=== fifo ==="; case_fifo; run_census fifo 10
  echo "=== fifty-mb ==="; case_fifty_mb; run_census fifty-mb 300
  echo "=== fifty-mb-line ==="; case_fifty_mb_single_line; run_census fifty-mb-line 300
else
  n=$1; "${CASES[$n]}"; run_census "$n" "${2:-60}"
fi
