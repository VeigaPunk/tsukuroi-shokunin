#!/usr/bin/env bash
# C2/P3 mechanism probe: does findmnt --mountpoint and mount resolve through
# a relative symlink (new_root -> sysroot) as mkinitcpio 42 creates it?
# Read-only to the host: everything happens inside an unprivileged user+mount
# namespace over a scratch tree under /fast/scratch/hyaku/.

BASE=/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/tree
rm -rf "$BASE"
mkdir -p "$BASE"

echo "=== 0. tool versions ==="
findmnt --version
mount --version
uname -r

echo
echo "=== 1. build the mkinitcpio-42 shaped tree ==="
# functions:1212-1213 -> install -dm755 \$buildroot/sysroot ; ln -s "sysroot" \$buildroot/new_root
install -dm755 "$BASE/sysroot"
ln -s "sysroot" "$BASE/new_root"
ls -la "$BASE"
echo "--- readlink new_root ->"
readlink "$BASE/new_root"

echo
echo "=== 2. mount a tmpfs on the sysroot dir (stands in for the real root mount) ==="
mount -t tmpfs tmpfs "$BASE/sysroot"
echo "exit=$?"
echo "--- findmnt --mountpoint \$BASE/sysroot  (control: the real dir)"
findmnt --mountpoint "$BASE/sysroot" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"
echo "--- findmnt --mountpoint \$BASE/new_root  (THE PROBE: through the symlink)"
findmnt --mountpoint "$BASE/new_root" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"
echo "--- findmnt --mountpoint \$BASE/new_root/ (trailing slash)"
findmnt --mountpoint "$BASE/new_root/" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"
echo "--- findmnt -T \$BASE/new_root  (--target, path-resolution flavour)"
findmnt -T "$BASE/new_root" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"
echo "--- findmnt --target \$BASE/new_root"
findmnt --target "$BASE/new_root" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"
echo "--- findmnt (no args) full table in this namespace"
findmnt -no FSTYPE,SOURCE,TARGET

echo
echo "=== 3. what does stat say (the mechanism the init script uses) ==="
echo -n "stat -c %D new_root : "; stat -c %D "$BASE/new_root"; echo "exit=$?"
echo -n "stat -c %D sysroot  : "; stat -c %D "$BASE/sysroot"; echo "exit=$?"

echo
echo "=== 4. mount --move through the symlink (the hook's own operation) ==="
mkdir -p "$BASE/lowdir"
mount --move "$BASE/new_root" "$BASE/lowdir"
echo "exit=$?"
echo "--- findmnt --mountpoint \$BASE/new_root after move"
findmnt --mountpoint "$BASE/new_root" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"
echo "--- findmnt --mountpoint \$BASE/lowdir after move"
findmnt --mountpoint "$BASE/lowdir" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"
echo "--- full table"
findmnt -no FSTYPE,SOURCE,TARGET

echo
echo "=== 5. mount -t overlay with the symlink as the target (the hook's second operation) ==="
mkdir -p "$BASE/ramdir/upper" "$BASE/ramdir/work"
mount -t tmpfs tmpfs "$BASE/ramdir"
echo "ramdir tmpfs exit=$?"
mount -t overlay overlay \
	-o "lowerdir=$BASE/lowdir,upperdir=$BASE/ramdir/upper,workdir=$BASE/ramdir/work" \
	"$BASE/new_root"
echo "exit=$?"
echo "--- findmnt --mountpoint \$BASE/new_root after overlay"
findmnt --mountpoint "$BASE/new_root" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"
echo "--- findmnt --mountpoint \$BASE/sysroot after overlay"
findmnt --mountpoint "$BASE/sysroot" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"
echo "--- full table"
findmnt -no FSTYPE,SOURCE,TARGET

echo
echo "=== 6. mount --bind with the symlink as source and as target ==="
mkdir -p "$BASE/bindsrc" "$BASE/bindtgt"
mount --bind "$BASE/new_root" "$BASE/bindsrc"
echo "bind-symlink-source exit=$?"
findmnt --mountpoint "$BASE/bindsrc" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"
mount --bind "$BASE/sysroot" "$BASE/bindtgt"
echo "bind-real-source exit=$?"
findmnt --mountpoint "$BASE/bindtgt" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"

echo
echo "=== 7. device identity: is the mount at the symlink the same device as the real dir? ==="
echo -n "stat -c '%d %D' new_root : "; stat -c '%d %D' "$BASE/new_root"
echo -n "stat -c '%d %D' sysroot  : "; stat -c '%d %D' "$BASE/sysroot"
echo -n "stat -c '%d %D' /       : "; stat -c '%d %D' /

echo
echo "=== 8. does findmnt --mountpoint find a NON-mounted dir through a symlink? ==="
mkdir -p "$BASE/plain" "$BASE/plainsym_target"
ln -s "plainsym_target" "$BASE/plainsym"
findmnt --mountpoint "$BASE/plainsym" -no FSTYPE,SOURCE,TARGET
echo "exit=$? (expect empty / nonzero: not a mountpoint)"

echo
echo "=== 9. negative control: symlink to a directory that IS a mountpoint via a DIFFERENT path ==="
mkdir -p "$BASE/alias"
ln -s "sysroot" "$BASE/alias_root"
findmnt --mountpoint "$BASE/alias_root" -no FSTYPE,SOURCE,TARGET
echo "exit=$?"

echo "=== DONE ==="
