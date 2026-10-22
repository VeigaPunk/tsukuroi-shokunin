#!/usr/bin/env bash
# Probe 2: isolate the overlay-source anomaly and trace the faithful hook sequence.
BASE=/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/tree2
rm -rf "$BASE"; mkdir -p "$BASE"

echo "=== A. does 'mount -t overlay overlay <target>' work with a PLAIN DIR target? ==="
mkdir -p "$BASE/a"/{low,up,work,tgt}
mount -t tmpfs tmpfs "$BASE/a/low"
mount -t overlay overlay -o "lowerdir=$BASE/a/low,upperdir=$BASE/a/up,workdir=$BASE/a/work" "$BASE/a/tgt"
echo "exit=$?"
findmnt --mountpoint "$BASE/a/tgt" -no FSTYPE,SOURCE,TARGET

echo
echo "=== B. same but target is a SYMLINK -> sysroot, sysroot holds a tmpfs ==="
mkdir -p "$BASE/b"/{low,up,work,sysroot}
ln -s sysroot "$BASE/b/new_root"
mount -t tmpfs tmpfs "$BASE/b/sysroot"
mount -t overlay overlay -o "lowerdir=$BASE/b/low,upperdir=$BASE/b/up,workdir=$BASE/b/work" "$BASE/b/new_root"
echo "exit=$?"
echo "--- where did the overlay land?"
findmnt -t overlay -no FSTYPE,SOURCE,TARGET
findmnt --mountpoint "$BASE/b/sysroot" -no FSTYPE,SOURCE,TARGET
echo "findmnt --mountpoint new_root exit:"
findmnt --mountpoint "$BASE/b/new_root" -no FSTYPE,SOURCE,TARGET; echo "exit=$?"

echo
echo "=== C. the earlier failing shape reproduced: target symlink, but with lowerdir pointing at a MOVED mount ==="
mkdir -p "$BASE/c"/{lowdir,ramdir/upper,ramdir/work,sysroot}
ln -s sysroot "$BASE/c/new_root"
mount -t tmpfs tmpfs "$BASE/c/sysroot"
mount --move "$BASE/c/new_root" "$BASE/c/lowdir"; echo "move exit=$?"
mount -t tmpfs tmpfs "$BASE/c/ramdir"; echo "ramdir exit=$?"
mount -t overlay overlay -o "lowerdir=$BASE/c/lowdir,upperdir=$BASE/c/ramdir/upper,workdir=$BASE/c/ramdir/work" "$BASE/c/new_root"
echo "exit=$?"
findmnt -t overlay -no FSTYPE,SOURCE,TARGET

echo
echo "=== D. is the overlay-source failure caused by the SYMLINK TARGET or by the source word? ==="
mkdir -p "$BASE/d"/{low,up,work,sysroot,tgt}
ln -s sysroot "$BASE/d/new_root"
mount -t tmpfs tmpfs "$BASE/d/low"
echo "--- D1: source word 'overlay', target = symlink"
mount -t overlay overlay -o "lowerdir=$BASE/d/low,upperdir=$BASE/d/up,workdir=$BASE/d/work" "$BASE/d/new_root"; echo "exit=$?"
echo "--- D2: source word 'overlay', target = plain dir (same dirs)"
mount -t overlay overlay -o "lowerdir=$BASE/d/low,upperdir=$BASE/d/up,workdir=$BASE/d/work" "$BASE/d/tgt"; echo "exit=$?"
echo "--- D3: source = absolute path that exists, target = symlink"
mount -t overlay "$BASE/d/low" -o "lowerdir=$BASE/d/low,upperdir=$BASE/d/up,workdir=$BASE/d/work" "$BASE/d/new_root"; echo "exit=$?"
findmnt -t overlay -no FSTYPE,SOURCE,TARGET

echo
echo "=== E. faithful hook sequence, mkinitcpio-42 shaped ==="
mkdir -p "$BASE/e"/{lowdir,ramdir/upper,ramdir/work,sysroot}
ln -s sysroot "$BASE/e/new_root"
mount -t tmpfs tmpfs "$BASE/e/sysroot"
echo "--- step1 findmnt --mountpoint /new_root -no FSTYPE"
findmnt --mountpoint "$BASE/e/new_root" -no FSTYPE; echo "exit=$?"
echo "--- step2 findmnt --mountpoint /new_root -no SOURCE"
findmnt --mountpoint "$BASE/e/new_root" -no SOURCE; echo "exit=$?"
echo "--- step3 mount --move /new_root lowdir"
mount --move "$BASE/e/new_root" "$BASE/e/lowdir"; echo "exit=$?"
echo "--- step3b is /new_root still a mountpoint? (the hook would re-check)"
findmnt --mountpoint "$BASE/e/new_root" -no FSTYPE; echo "exit=$?"
echo "--- step4 mount -t overlay onto /new_root"
mount -t tmpfs tmpfs "$BASE/e/ramdir"
mount -t overlay overlay -o "lowerdir=$BASE/e/lowdir,upperdir=$BASE/e/ramdir/upper,workdir=$BASE/e/ramdir/work" "$BASE/e/new_root"; echo "exit=$?"
echo "--- final table (overlay rows)"
findmnt -t overlay -no FSTYPE,SOURCE,TARGET
echo "--- final: is /sysroot-equivalent the overlay?"
findmnt --mountpoint "$BASE/e/sysroot" -no FSTYPE,SOURCE,TARGET; echo "exit=$?"
echo "--- stat -c %D comparison the init script does (real path vs symlink path)"
echo -n "stat -c %D (no -L) sysroot : "; stat -c %D "$BASE/e/sysroot"
echo -n "stat -c %D (no -L) new_root : "; stat -c %D "$BASE/e/new_root"
echo -n "stat -c %D -L new_root     : "; stat -c %D -L "$BASE/e/new_root"

echo "=== DONE ==="
