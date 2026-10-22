B=/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/faith
rm -rf $B; mkdir -p $B/{sysroot}
ln -s sysroot $B/new_root
echo "== S1: root fs mounted at sysroot (btrfs analog: tmpfs) =="
mount -t tmpfs tmpfs $B/sysroot
echo "== S2: hook probe 1: findmnt --mountpoint /new_root -no FSTYPE =="
findmnt --mountpoint $B/new_root -no FSTYPE; echo "exit=$?"
echo "== S3: hook probe 2: findmnt --mountpoint /new_root -no SOURCE =="
findmnt --mountpoint $B/new_root -no SOURCE; echo "exit=$?"
echo "== S4: mktemp lower/ram dirs, ram tmpfs, upper/work AFTER mount =="
low=$(mktemp -d -p $B lowdir_XXX)
ram=$(mktemp -d -p $B ramdir_XXX)
mount -t tmpfs cowspace $ram
mkdir -p $ram/upper $ram/work
echo "== S5: mount --move /new_root \$low (hook op) =="
mount --move $B/new_root $low; echo "exit=$?"
echo "-- after move: findmnt --mountpoint new_root (expect none) --"
findmnt --mountpoint $B/new_root -no FSTYPE,SOURCE,TARGET; echo "exit=$?"
echo "-- findmnt --mountpoint lowdir --"
findmnt --mountpoint $low -no FSTYPE,SOURCE,TARGET
echo "== S6: mount -t overlay ... /new_root (hook op) =="
mount -t overlay overlay -o "lowerdir=$low,upperdir=$ram/upper,workdir=$ram/work" $B/new_root; echo "exit=$?"
echo "-- findmnt --mountpoint /new_root (expect overlay at resolved target) --"
findmnt --mountpoint $B/new_root -no FSTYPE,SOURCE,TARGET; echo "exit=$?"
echo "-- findmnt --mountpoint /sysroot --"
findmnt --mountpoint $B/sysroot -no FSTYPE,SOURCE,TARGET; echo "exit=$?"
echo "== S7: btrfs-property analog (stat/readlink across symlink) =="
readlink $B/new_root; stat -c '%F %N' $B/new_root
echo "== DONE =="
