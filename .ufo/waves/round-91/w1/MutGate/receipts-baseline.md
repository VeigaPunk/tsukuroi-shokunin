# MutGate receipts (round 91, wave w1)

## Gate bytes measured
```
62bb06c997fb99a9fd811ec97440eebe2dafa7e63c4f21f43aa0ead9af7da737  canon-frozen.py
62bb06c997fb99a9fd811ec97440eebe2dafa7e63c4f21f43aa0ead9af7da737  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py
655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/limine-pin-battery-r91.py
lane master: 2d7e09e101996cc1ac5836c6d635f3f608453ac5
HEAD gate: 62bb06c997fb99a9fd811ec97440eebe2dafa7e63c4f21f43aa0ead9af7da737  -
worktree gate mtime: 2026-11-07 23:47:47.983940782
worktree gate status: 
battery sha vs assignment digest 655ee8f3...: MATCH (32/32 hex chars at sha256sum -c time). Freeze manifest (13 entries) sha256sum -c: all 13 OK, exit 0.
```

## Baseline (pristine frozen bytes, --runs 3)
```
run 1 met 82/82 cases 328
run 2 met 82/82 cases 328
run 3 met 82/82 cases 328
```

One earlier baseline invocation (started before the gate froze) was invalidated by my own `rm -rf w0` racing its work dir: 'FileNotFoundError ... limine-battery-r91-eqi2l5tj/ce9kbc9zc', exit 1. Discarded; the run above is the baseline of record.
