set -u
BASE=/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/tree3
rm -rf "$BASE"; mkdir -p "$BASE"/{lowdir,ramdir/upper,ramdir/work,sysroot}
ln -s sysroot "$BASE/new_root"
mount -t tmpfs tmpfs "$BASE/sysroot"
mount --move "$BASE/new_root" "$BASE/lowdir"
mount -t tmpfs tmpfs "$BASE/ramdir"
echo "### mount syscall trace:"
strace -f -e trace=mount,mount_setattr,statx,newfstatat,openat,readlink -o /fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/strace-overlay.txt \
  mount -t overlay overlay -o "lowerdir=$BASE/lowdir,upperdir=$BASE/ramdir/upper,workdir=$BASE/ramdir/work" "$BASE/new_root"
echo "exit=$?"
