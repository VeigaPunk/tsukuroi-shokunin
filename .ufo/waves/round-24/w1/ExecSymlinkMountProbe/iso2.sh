B=/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/iso4
rm -rf $B; mkdir -p $B/{low,sysroot}
ln -s sysroot $B/new_root
mount -t tmpfs tmpfs $B/sysroot
# CORRECT ORDERING: mount tmpfs FIRST, then mkdir inside it
mkdir -p $B/ram
mount -t tmpfs tmpfs $B/ram
mkdir -p $B/ram/upper $B/ram/work
echo "=== overlay, up/work on tmpfs, target = symlink to mounted dir ==="
mount -t overlay overlay -o "lowerdir=$B/low,upperdir=$B/ram/upper,workdir=$B/ram/work" $B/new_root
echo "exit=$?"
findmnt -t overlay -no FSTYPE,SOURCE,TARGET
echo "=== findmnt --mountpoint new_root ==="
findmnt --mountpoint $B/new_root -no FSTYPE,SOURCE,TARGET; echo "exit=$?"
echo "=== findmnt --mountpoint sysroot ==="
findmnt --mountpoint $B/sysroot -no FSTYPE,SOURCE,TARGET; echo "exit=$?"
