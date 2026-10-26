#!/usr/bin/env bash
# C1RevNoFalseBlock evidence log — read-only host probes; fixtures under this scratch dir.
set -u
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r39/C1RevNoFalseBlock
R="$LANE/.ufo/waves/round-39/w1/C1RevNoFalseBlock/receipts"
mkdir -p "$R"

echo "== access date: $(date -u '+%Y-%m-%dT%H:%M:%SZ'); host kernel: $(uname -r)"
echo
echo "== host /proc/self/mounts, fstype field == btrfs:"
awk '$3=="btrfs"' /proc/self/mounts
echo "== host /sys/fs/btrfs listing:"
ls /sys/fs/btrfs
echo

echo "== RUN1: live census, no overrides:"
bash "$LANE/tools/tsukuroi-census.sh" --sample 1 2>/dev/null | grep '^STORAGE'
echo

mkdir -p "$S/fx2"
printf '/dev/sda1 /mnt/btrfs-backup ext4 rw,relatime 0 0\nproc /proc proc rw,nosuid 0 0\n' > "$S/fx2/mounts"
echo "== RUN2: fixture table with fstype=ext4 but 'btrfs' substring in mount path; sysfs root absent:"
TSUKUROI_BTRFS_SYSFS="$S/fx2/no-such-root" TSUKUROI_PROC_MOUNTS="$S/fx2/mounts" \
  bash "$LANE/tools/tsukuroi-census.sh" --sample 1 2>/dev/null | grep '^STORAGE'
echo

echo "== RUN3: real sysfs (fsid entry present), unreadable mounts-table override:"
TSUKUROI_PROC_MOUNTS="$S/fx2/does-not-exist" \
  bash "$LANE/tools/tsukuroi-census.sh" --sample 1 2>/dev/null | grep '^STORAGE'
echo

MP="$S/mp"; mkdir -p "$MP"
echo "== lazy-umount probe (tmpfs over $MP inside unshare -rm):"
unshare -rm bash -c "MP='$MP'; mount -t tmpfs none \"\$MP\" && touch \"\$MP/marker\" && ( cd \"\$MP\" && sleep 2 ) & sleep 0.5; echo -n 'entries before umount -l: '; grep -c \"\$MP tmpfs \" /proc/self/mounts; umount -l \"\$MP\"; echo -n 'while fs still busy: '; grep -F \"\$MP\" /proc/self/mounts || echo 'ENTRY GONE from /proc/self/mounts'; wait; echo -n 'after refs dropped: '; grep -F \"\$MP\" /proc/self/mounts || echo 'entry still gone'"
echo
echo "== fsid dirs visible inside plain 'unshare -rm' (no masking):"
unshare -rm bash -c 'ls /sys/fs/btrfs'
echo
echo "== census probe_storage_arm excerpt (worktree == commit 49cc53c, diff-verified):"
sed -n '1862,1869p;1903,1919p' "$S/receipts/census-49cc53c.sh"
