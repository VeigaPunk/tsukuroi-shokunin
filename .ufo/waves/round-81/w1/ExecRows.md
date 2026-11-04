# ExecRows — round 81, w1, independent re-derivation of C1

- lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
- base: `96ad75b84160da58efaee4997576ce718fd72e2b`
- declaration-only commit: `8023711867eaa788f68af09d7f29d24db749cca7` (author trials preceded it; **not** a compliant pre-data freeze — see F10)
- HEAD observed: `e8e5d5b39b25a83f705dc3aa760df21c6a2af508`
- role: leaf executor, read-only over the lane tree; no Git mutation, no commit, no dispatch
- receipts: `.ufo/waves/round-81/w1/ExecRows/{rows.txt,counters.txt,findings.json,rederive.py}`

## Axes

1. **depth** — every row re-derived against the pinned bytes, in two coordinate systems, with the quote-locate rule re-implemented rather than called; plus the entry prose checked sentence by sentence against the same bytes.
2. **operability** — can the instrument be run, does its selftest pass, can the entry's own `recheck:` line be executed at the revision the entry is delivered at.
3. **freshness** — are the pinned bytes the genuine v262 file (upstream re-fetch), are the digests identical at base / declaration / HEAD, is the entry itself under version control.

## Method

I did not run the lane's counter first and adopt its number. I wrote an independent
instrument (`.ufo/waves/round-81/w1/ExecRows/rederive.py`, 6.2 kB) that re-implements the
seven frozen clauses from the tool's own header prose and never imports
`tools/count-mount-rows-r81.py`. Only after it produced its own totals did I run the lane
counter, and I report both.

## Inputs read

| path | observation |
|---|---|
| `.ufo/waves/round-81/before/src/systemd.mount.xml` | 707 raw lines, 703 after whole-document tag stripping (drift 4) |
| `.ufo/waves/round-81/before/src/SHA256SUMS` | 3 entries |
| `.ufo/waves/round-81/before/host/generator.txt` | 149 lines, 2026-11-04T17:54:25-03:00 |
| `.ufo/waves/round-81/before/host/capture.txt` | `systemctl show` for five mounts + generator listing |
| `corpus/knowledge/mount-unit-fstab-plane-r81.json` | 8 rows, 3 measured legs |
| `corpus/knowledge/mount-unit-fstab-plane-r81.md` | 70 lines |
| `.ufo/waves/round-81/before/declaration-baseline.json` | C1/C2/C3 trials at 8023711 |
| `.ufo/waves/round-81/before/gate-standard-r81.json` | C2 case matrix (6 cases) |
| `corpus/SOURCES.md` | S331 `docs`, S332 `own-work` |

## Counts I measured

```
$ python3 tools/count-mount-rows-r81.py --fixture /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
{"claim": "C1", "revision": "fixture", "count": 8, "target": 8, "finding": "met", "problems": []}
RC=0

$ python3 tools/count-mount-rows-r81.py --selftest
SELFTEST total=6 passed=6 failed=0
RC=0

independent re-derivation: rows=8 verified=8 measured=3 distinct_settings=8 finding=met
```

- rows in entry: **8**
- rows passing R1–R7: **8**
- measured legs: **3** (MT2, MT5, MT6)
- distinct settings: **8**
- row-clause finding: **met**

The row clause reproduces. The entry as a whole does **not** close: the human-readable
`.md` is never read by the instrument and two of its statements are contradicted by the
pinned capture (F1, F2).

## Per-row re-derivation

`rows.txt` holds the full table (statement, quote, exact text at the cited lines with tags
stripped, locate verdict in both coordinate systems, measured leg). Summary:

| id | setting | cited | quote at stripped | quote at raw file lines | verdict |
|---|---|---|---|---|---|
| MT1 | DefaultDependencies | 133-137 | 133-136 → inside | 135-138 → **outside cited end** | quote located (stripped) |
| MT2 | nofail | 498-503 | 500-501 | 502-503 → inside | located; measured leg :140-143 |
| MT3 | noauto | 481-487 | 484-485 | 486-487 → inside | located |
| MT4 | x-systemd.automount | 489-491 | 489-490 | 491-492 → **outside cited end** | located (stripped) |
| MT5 | x-systemd.before= | 229-241 | 232-234 | 234-236 → inside | located; measured leg :99-100 |
| MT6 | x-systemd.device-timeout= | 335-347 | 337-339 | 339-341 → inside | located; measured leg :124-127 |
| MT7 | x-systemd.requires= | 194-212 | 196-199 | 198-201 → inside | located |
| MT8 | x-systemd.wanted-by= | 254-265 | 257-258 | 259-260 → inside | located |

All eight quotes locate verbatim after whitespace normalisation **in the tag-stripped
coordinate system**. In the file's own coordinate system every cited range starts two
lines early and two quotes fall outside it (F4).

## Statements the pinned snapshot does not support

1. **md:30** — "`/etc/fstab` carries six local file systems; four are required and two are
   not". The pinned capture generates **seven** mount units; five sit in
   `local-fs.target.requires`, two in `local-fs.target.wants`. The sentence also
   contradicts its own md:32 bullet, which lists five required mounts. **Contradicted.**
2. **md:49-50** — "The generated `Options=` line keeps `nofail` but drops the `x-systemd.*`
   tokens". `generator.txt:77` is
   `Options=rw,noatime,nosuid,nodev,logbsize=256k,nofail,x-systemd.before=local-fs.target`.
   Only `x-systemd.device-timeout=` is dropped (into the device drop-in). **Contradicted.**
3. **md:42-43** — the anchor `(S332 :35-47 vs :95-107)`; `:95-107` is `var-log.mount`
   (a required mount), `tmp.mount` is `:64-77`. The claim is true, the anchor is not.
4. **md:51-55** — "still delays `local-fs.target` by up to the device timeout … up to ten
   seconds for `/tmp` and nothing for `/fast`". Neither pinned source states this, and the
   `nofail` sentence it is derived from says the opposite ("the boot will continue without
   waiting for the mount unit"). **[INFERENCE], unverified — not contradicted, not supported.**
5. **md:62** — "The line anchors above are v262 upstream lines". The upstream file is
   byte-identical to the snapshot (sha256 `afbf3be6…` re-fetched, http 200, 37234 bytes), and
   in *that* file line 133 is the `umount.target` bullet, not MT1's text. The anchors are the
   instrument's tag-stripped lines. **False as written.**
6. **JSON MT7** — "they always attach to the created mount unit even under automount". The
   automount-independence note exists only in the `x-systemd.requires=` entry (raw 212-214);
   `x-systemd.wants=` says only "similar to the `x-systemd.requires=` option". The `wants=`
   half is an inference.
7. **md:5** — the `recheck:` procedure (`--revision <REV>` must print met rc 0) is not
   executable at any committed revision today: base → `cannot-evaluate:CalledProcessError`
   rc 2, declaration → `note-absent` rc 1, HEAD → `note-absent` rc 1, and the entry is
   untracked at HEAD (`git ls-files` prints nothing).

## Observation / inference / unknown

- **Observed**: every command output quoted above and in `counters.txt`; the sha256 values;
  the line numbers; the git object presence checks.
- **Inference** (mine, marked): that `Options=` token retention (F2) reflects the generator
  applying `x-systemd.before=` as an ordering directive while leaving the token in `Options=`;
  I did not read `fstab-generator.c` to confirm the mechanism, so this stays an inference.
- **Unknown**: whether `local-fs.target` actually waits for a `nofail` mount that carries
  `x-systemd.before=local-fs.target` (F5). Not testable read-only; no boot/device-removal
  test was run and none was authorised.

## Gate-standard note (round-80 counter repair axis)

R7 accepts a measured leg on locatability alone. MT2's leg cites `generator.txt:140-143`,
which is `### local-fs.target.requires` plus three required mounts — it contains no
`nofail` token and no `wants` block, so it passes R7 while not evidencing the row it
attaches to. The wants block is `:136-139`. Likewise, the selftest's only quote-negative
case replaces a quote with an absent sentence; no case exercises a **shifted** range whose
quote still happens to fall inside (the F4 shape), and no case mutates the entry's `url` or
`snapshot_sha256`, which C1 never reads (C2's gate-standard does have a url case).

## Tooling

None installed, none upgraded. No pacman transaction attempted (host-wide pause respected),
no `uv tool`, no binary written to any PATH directory. Everything ran with the system
`python3` and `curl` already present.

## Scratch

`/fast/scratch/hyaku/tsukuroi-r81/ExecRows/` (`HYAKU_SCRATCH` was unset; the `/fast/scratch/hyaku`
default was used) — removed before yielding; receipts copied into the seat directory first.

## Limits and risks

- Read-only over the lane tree: nothing in the entry was fixed; F1/F2/F4/F6/F8 are reported
  for the integrator to apply.
- The instrument convention (tag-stripped line numbers) is defensible but undocumented in
  the entry; until md:62 or the JSON rows say so, every `S331 :a-b` anchor misleads a reader
  who checks the file directly.
- F5 remains open and is the one claim in the entry that would change the boot-cost
  conclusion if it turned out false.
