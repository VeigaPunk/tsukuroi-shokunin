# C1ExecRerun — C1-1 command log

Host: linux 7.2.11-arch1-1, python3 3.14. Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
Scratch: /fast/scratch/hyaku/tsukuroi-r39/C1ExecRerun (removed after receipts copied)

1. sha256sum tools/score-storage-hidden-r39.py
   -> 75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973  tools/score-storage-hidden-r39.py
2. git show 6a08925daa30767809eb13bb4b01448ff954d46a:tools/score-storage-hidden-r39.py | sha256sum
   -> 75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973  -
3. export TMPDIR=/fast/scratch/hyaku/tsukuroi-r39/C1ExecRerun
   python3 tools/score-storage-hidden-r39.py --revision 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82 \
       --scratch /fast/scratch/hyaku/tsukuroi-r39/C1ExecRerun/s > c1-rerun-49cc53c.jsonl
   -> exit 0; stderr empty; 33.93 s wall
4. python3 tools/score-storage-hidden-r39.py --revision 2e1c2a40c13dc52e155d89e72f3fdd560db7399a \
       --scratch /fast/scratch/hyaku/tsukuroi-r39/C1ExecRerun/s2 > c1-rerun-2e1c2a4.jsonl
   -> exit 0; stderr empty; 33.33 s wall
5. census + counter blobs identical at 49cc53c, 2e1c2a4, 394e1ba:
   tools/tsukuroi-census.sh e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d (all three)
   tools/score-storage-hidden-r39.py 75a9e8ab...f973 (all three)
6. python3 tools/check-adjacency-anchors.py --revision 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82
   -> exit 0, status PASS, findings []
