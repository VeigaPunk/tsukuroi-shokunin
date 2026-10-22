set -x
B=/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/faith2
rm -rf "$B"; mkdir -p "$B/sysroot"
ls -la "$B"
ln -s sysroot "$B/new_root"
ls -la "$B"
mount -t tmpfs tmpfs "$B/sysroot"; echo "S1 exit=$?"
findmnt --mountpoint "$B/new_root" -no FSTYPE; echo "S2 exit=$?"
findmnt --mountpoint "$B/new_root" -no SOURCE; echo "S3 exit=$?"
low=$(mktemp -d -p "$B" lowdir_XXX); ram=$(mktemp -d -p "$B" ramdir_XXX)
mount -t tmpfs cowspace "$ram"; echo "ram exit=$?"
mkdir -p "$ram/upper" "$ram/work"
mount --move "$B/new_root" "$low"; echo "S5 exit=$?"
findmnt --mountpoint "$B/new_root" -no FSTYPE,SOURCE,TARGET; echo "after move new_root findmnt exit=$?"
findmnt --mountpoint "$low" -no FSTYPE,SOURCE,TARGET; echo "lowdir findmnt exit=$?"
mount -t overlay overlay -o "lowerdir=$low,upperdir=$ram/upper,workdir=$ram/work" "$B/new_root"; echo "S6 exit=$?"
findmnt --mountpoint "$B/new_root" -no FSTYPE,SOURCE,TARGET; echo "final findmnt exit=$?"
