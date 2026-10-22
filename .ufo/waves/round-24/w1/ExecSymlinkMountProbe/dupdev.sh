B=/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/dup
rm -rf $B; mkdir -p $B/{A,B,C}
mount -t tmpfs tmpfs $B/A
mount --bind $B/A $B/B
ln -s A $B/symA
ln -s B $B/symB
echo "=== mountinfo rows for A and B ==="
findmnt -no TARGET,SOURCE,FSTYPE $B/A
findmnt -no TARGET,SOURCE,FSTYPE $B/B
echo "=== findmnt --mountpoint symA (-> A) ==="
findmnt --mountpoint $B/symA -no TARGET,SOURCE,FSTYPE; echo "exit=$?"
echo "=== findmnt --mountpoint symB (-> B) ==="
findmnt --mountpoint $B/symB -no TARGET,SOURCE,FSTYPE; echo "exit=$?"
echo "=== findmnt --mountpoint A (real) ==="
findmnt --mountpoint $B/A -no TARGET,SOURCE,FSTYPE; echo "exit=$?"
