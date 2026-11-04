status: complete
verdict: held

# S1Scout — independent second-route verification (round 73, wave 1)

Done. `ROUTE2_OK=3/3` (raw, codeload tarball, contents API all byte-identical to the committed
snapshots; the resolved signed tag `v262` = commit `8cc40e0c`, and that commit's raw files match too).
All six planned quotes located in the committed v262 bytes:

```
quote=systemd.unit.xml:368-370
quote=systemd.unit.xml:238-239
quote=unit.c:3875-3875
quote=unit.c:3908-3908
quote=install.c:345-345
quote=install.c:351-351
```

Host surface re-captured read-only: `HOST_DELTAS=0` over 15 checks against `before/host.txt`.
Unclaimed probe: `/etc` and `/usr/lib` drop-in dirs are unprivileged-visible (755, all files
world-readable); `/run` has zero `*.d` dirs (vacuous). Limit recorded: host ships v262.1 and its
`install.c` differs from pinned v262 in 4 hunks (quoted strings unchanged, lines 348/354 vs 345/351);
the only candidate non-GitHub route (gitlab.freedesktop.org mirror) is auth-walled.

Full evidence, commands and outputs in `report.md` in this directory (also written to
`.ufo/waves/round-73/w1/S1Scout.md` for the trailer path).
