BASE=/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/iso
rm -rf "$BASE"
echo "=== CASE 1 (fresh ns, up/work on tmpfs) ==="
mkdir -p "$BASE"/{low,ram/upper,ram/work,tgt}
mount -t tmpfs tmpfs "$BASE/ram"
mount -t overlay overlay -o "lowerdir=$BASE/low,upperdir=$BASE/ram/upper,workdir=$BASE/ram/work" "$BASE/tgt"; echo "exit=$?"
echo "=== CASE 2 (fresh ns, up/work on plain dir) ==="
mkdir -p "$BASE"/{low,up,work,tgt2}
mount -t overlay overlay -o "lowerdir=$BASE/low,upperdir=$BASE/up,workdir=$BASE/work" "$BASE/tgt2"; echo "exit=$?"
