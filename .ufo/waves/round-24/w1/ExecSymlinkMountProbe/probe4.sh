BASE=/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/t4
rm -rf "$BASE"; mkdir -p "$BASE"/{low,up,work,sysroot}
ln -s sysroot "$BASE/new_root"
echo "### CASE 1: no prior mount --move, target = symlink"
mount -t overlay overlay -o "lowerdir=$BASE/low,upperdir=$BASE/up,workdir=$BASE/work" "$BASE/new_root" 2>&1; echo "exit=$?"
echo "### CASE 2: after a mount --move of an unrelated tmpfs, target = symlink"
mkdir -p "$BASE/mvsrc" "$BASE/mvdst"
mount -t tmpfs tmpfs "$BASE/mvsrc"
mount --move "$BASE/mvsrc" "$BASE/mvdst" 2>&1; echo "move exit=$?"
mkdir -p "$BASE/low2" "$BASE/up2" "$BASE/work2"
mount -t overlay overlay -o "lowerdir=$BASE/low2,upperdir=$BASE/up2,workdir=$BASE/work2" "$BASE/new_root" 2>&1; echo "exit=$?"
