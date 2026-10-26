#!/usr/bin/env bash
# Seat C1LabratProcAbsent — round 39 C1 unreadable-table reachability probes.
# Read-only: every mount happens inside a private `unshare -rm` namespace; no host state touched.
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r39/C1LabratProcAbsent
export TMPDIR="$S"
CEN=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin

say() { printf '\n===== %s =====\n' "$*"; }
head_info() {
  printf 'lane HEAD:      %s\n' "$(git -C "$LANE" rev-parse HEAD)"
  printf 'census sha256:  %s\n' "$(sha256sum "$CEN" | cut -d' ' -f1)"
  printf 'census commit:  %s\n' "$(git -C "$LANE" log -1 --format=%H -- tools/tsukuroi-census.sh)"
  printf 'unshare:        %s\n' "$(unshare --version)"
  printf 'bash:           %s\n' "$(bash --version | head -1)"
}
head_info

say "A/P0 baseline: unshare -rm, nothing hidden"
unshare -rm bash -c "
  printf 'ns-mounts-btrfs-lines='; grep -c ' btrfs ' /proc/self/mounts
  printf 'host-sysfs-fsid='; ls /sys/fs/btrfs | tr '\n' ' '; echo
  bash $CEN 2>&1 | grep -E '^STORAGE|^TSUKUROI_CENSUS'
  echo rc=\${PIPESTATUS[0]}
"

say "B/P1 hide /sys/fs/btrfs only (/proc intact)"
unshare -rm bash -c "
  mount -t tmpfs r39hide /sys/fs/btrfs && echo hide-active
  printf 'ns-mounts-btrfs-lines='; grep -c ' btrfs ' /proc/self/mounts
  bash $CEN 2>&1 | grep -E '^STORAGE|^TSUKUROI_CENSUS'
"

say "C/P2 naive masked /proc (tmpfs over /proc) + hidden sysfs"
unshare -rm bash -c "
  mount -t tmpfs r39hide /sys/fs/btrfs
  mount -t tmpfs r39proc /proc
  echo proc-masked; ls /proc/self/mounts 2>&1
  bash $CEN > $S/c-p2.out 2>&1; echo census_rc=\$?
  echo out_lines=\$(wc -l < $S/c-p2.out)
  echo storage_lines=\$(grep -c '^STORAGE' $S/c-p2.out)
  cat $S/c-p2.out
"

say "D/P2c control: naive masked /proc, sysfs VISIBLE"
unshare -rm bash -c "
  mount -t tmpfs r39proc /proc
  echo proc-masked
  bash $CEN > $S/d-p2c.out 2>&1; echo census_rc=\$?
  echo out_lines=\$(wc -l < $S/d-p2c.out)
  echo storage_lines=\$(grep -c '^STORAGE' $S/d-p2c.out)
  cat $S/d-p2c.out
"

say "E/P3 fresh procfs (unshare -rmpf --mount-proc) + hidden sysfs"
unshare -rmpf --mount-proc bash -c "
  mount -t tmpfs r39hide /sys/fs/btrfs
  printf 'ns-mounts-btrfs-lines='; grep -c ' btrfs ' /proc/self/mounts
  printf 'dev-fd-present='; ls /dev/fd >/dev/null && echo yes
  bash $CEN 2>&1 | grep -E '^STORAGE|^TSUKUROI_CENSUS'
"

say "F/P5 umount /proc inside unshare -rm"
unshare -rm bash -c "
  grep -E ' /proc ' /proc/self/mounts
  umount -v /proc; echo umount_rc=\$?
  ls -l /proc/self/mounts
"

say "G/P4 per-pid bind mask of /proc/<pid>/mounts does not reach the reader"
unshare -rm bash -c "
  mount --bind /dev/null /proc/\$\$/mounts; echo bind_rc=\$?
  printf 'child-sees-bytes='; cat /proc/self/mounts | wc -c
"

say "H/P7 masked /proc + /proc/self/fd relayed to a real procfs + hidden sysfs"
unshare -rmpf bash -c "
  S=$S; CEN=$CEN
  mkdir -p \$S/realproc-h && mount -t proc proc \$S/realproc-h && echo realproc-mounted
  printf 'real-ns-mounts-btrfs-lines='; grep -c ' btrfs ' \$S/realproc-h/self/mounts
  mount -t tmpfs r39hide /sys/fs/btrfs && echo sysfs-hidden
  mount -t tmpfs r39proc /proc && echo proc-masked
  mkdir -p /proc/self && ln -s \$S/realproc-h/self/fd /proc/self/fd
  printf 'procsub-ok='; mapfile -t z < <(printf 'a\nb\n'); echo n=\${#z[@]}
  printf 'census-table-open: '; cat /proc/self/mounts 2>&1; echo cat_rc=\$?
  bash \$CEN > \$S/h-p7.out 2>&1; echo census_rc=\$?
  grep -E '^STORAGE|^TSUKUROI_CENSUS' \$S/h-p7.out
"

say "I/P8 control: same masking, sysfs VISIBLE (fsid path, table never read)"
unshare -rmpf bash -c "
  S=$S; CEN=$CEN
  mkdir -p \$S/realproc-i && mount -t proc proc \$S/realproc-i
  mount -t tmpfs r39proc /proc
  mkdir -p /proc/self && ln -s \$S/realproc-i/self/fd /proc/self/fd
  bash \$CEN 2>&1 | grep -E '^STORAGE'
"

say "J/P9 masked /proc + relay + readable EMPTY /proc/self/mounts + hidden sysfs"
unshare -rmpf bash -c "
  S=$S; CEN=$CEN
  mkdir -p \$S/realproc-j && mount -t proc proc \$S/realproc-j
  mount -t tmpfs r39hide /sys/fs/btrfs
  mount -t tmpfs r39proc /proc
  mkdir -p /proc/self && ln -s \$S/realproc-j/self/fd /proc/self/fd && : > /proc/self/mounts
  printf 'masked-table-bytes='; wc -c < /proc/self/mounts
  printf 'real-ns-mounts-btrfs-lines='; grep -c ' btrfs ' \$S/realproc-j/self/mounts
  bash \$CEN > \$S/j-p9.out 2>&1; echo census_rc=\$?
  grep -E '^STORAGE' \$S/j-p9.out
"

say "K/P10 /proc intact, sysfs hidden, override seam points at an absent table"
unshare -rm bash -c "
  mount -t tmpfs r39hide /sys/fs/btrfs
  TSUKUROI_PROC_MOUNTS=/nonexistent/table bash $CEN 2>&1 | grep -E '^STORAGE'
"

say "END"
