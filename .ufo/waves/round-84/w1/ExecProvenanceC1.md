# ExecProvenanceC1 — C1 provenance re-count (shape gate only)

Seat: Executor. Assignment: re-count the provenance of the round-84 C1 entry
`corpus/knowledge/hibernate-resume-plane-r84.json` with the frozen counter, re-implement the frozen
predicate independently from its docstring text, and test the counter's known limit with a junk entry.
C1 is **exploratory** (withdrawn as a measured claim in `69915b86`); nothing here re-scopes it and no
ordinal move is claimed. The counter is treated as a shape gate, not a measurement.

Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`
→ `69915b8603d9e443f2e1c0021d7c34509186bd9e`.
Candidate read: `c6ee78b2d4184ace3c6d01116190729f0f7c2c31`. Freeze read: `e0f42051bf9b01af5857c28562ca0247a8fef367`.

Instrument sha256 (measured this seat):

```
cb70d4357ebe2d50f360dbbc2079f3a35756a79fc785280cf9d4312268ac8309  tools/count-resume-rows-r84.py
00310ac205f07f396bc4a7a0406f1c0d4baf74c7ab30e27245bbc89d8ce00964  tools/resume-gate-battery-r84.py
cec27b9d19e4ac85ccaa513b94e37f568b51979c546133c3d4bc5f62cd6cea23  tools/capture-resume-facts-r84.py
3d2e1cf58af1576924decb2280a38ba4225905e7de0af2b1c5df9362eccb4556  tools/check-hibernate-resume.py
5d1673de7f893f035cb2808e9579bcdd292339a32dad605c6e3a53d6561f7eef  .ufo/waves/round-84/before/src/SHA256SUMS
4ca3e20939eadff71c190f5e2d27a5f453479d0133321ebd118eb7eef624fde6  .ufo/waves/round-84/before/host/SHA256SUMS
46225614851f966b5632f2cf44cb320d417e51c6a0a6819455651e30ab31842c  corpus/knowledge/hibernate-resume-plane-r84.json (== git blob at master)
```

Pinned input bytes verify:
`cd .ufo/waves/round-84/before/src && sha256sum -c SHA256SUMS` → 8× `OK`, rc 0;
`cd ../host && sha256sum -c SHA256SUMS` → 2× `OK`, rc 0.

## 1. Frozen counter runs (verbatim, from lane root)

```
$ python3 tools/count-resume-rows-r84.py --revision master
{ "verdict": "met", "counted": 10, "failed": 0, "distinct_snapshots": 6,
  "target_rows": 7, "target_snapshots": 4, "rows": [HR1..HR10 all "ok"] }
rc=0
```
(full object in `receipts/counter-master.txt`)

```
$ python3 tools/count-resume-rows-r84.py --revision e0f42051bf9b01af5857c28562ca0247a8fef367
{ "verdict": "cannot-evaluate", "reason": "entry-absent:corpus/knowledge/hibernate-resume-plane-r84.json", "counted": 0 }
rc=2
```

Extra revisions run for the record:

```
$ python3 tools/count-resume-rows-r84.py --revision 64f45b790f2dbbf63b9b343c47810118a79f7a35
{ "verdict": "cannot-evaluate", "reason": "manifest-absent:.ufo/waves/round-84/before/src/SHA256SUMS", "counted": 0 }
rc=2
$ python3 tools/count-resume-rows-r84.py --revision c6ee78b2d4184ace3c6d01116190729f0f7c2c31
met 10/10, distinct_snapshots 6
rc=0
```

Selftest, five runs (`--selftest --root .`), each printed
`"selftest": "PASS (12 cases, 12 passed, 0 failed)"` and exited `rc=0`
(per-run case JSON in `receipts/selftest-5.txt`). An additional 40-run tally of the same command
(`receipts/selftest-40.json`): 40/40 PASS, 0 failing cases; `P1 counted=7` in 40/40 runs;
**`F7 counted=6` in 6/40 runs** (7 in 34/40) — the F7 fixture's generator occasionally returns six
rows instead of seven (its 3-file random sample can include a tiny file and hit the 10000-try cap),
which still passes because 6 < 7. Fixture quantity nondeterminism, not a verdict defect.

## 2. Independent checker (written from the predicate text, not the counter's code)

`check.py` (this dir) re-implements R1–R6 from the docstring of `tools/count-resume-rows-r84.py`,
reading the manifests itself, hashing the files itself, and computing both the documented **local**
minimal-span reading (dropping either end line loses the quote) and a stricter **global** reading
(no shorter span anywhere in the file contains it). Interpretations are disclosed in its header.
Run:

```
$ python3 .ufo/waves/round-84/w1/ExecProvenanceC1/check.py --repo . --revision master \
    --counter tools/count-resume-rows-r84.py --json-out .../receipts/check-master-rev.json
verdict met counted 10 failed 0 distinct_snapshots 6 distinct_snapshot_paths 6
frozen {'rc': 0, 'verdict': 'met', 'counted': 10, 'failed': 0}
all agree True
rc=0
```

Manifest pins observed == frozen pins for both manifests; every declared snapshot/receipt sha256 equals
the manifest entry and the file bytes hash to it. Per-row result (my reason | frozen reason | agree):

| Row | snapshot : lines (quote words) | src local / global minimal | host receipt : lines | host value | mine | frozen | agree |
|---|---|---|---|---|---|---|---|
| HR1 | S336 kernel-parameters.txt :6581-6582 (15) | ok / global-min | :4 | `resume_offset=3795013` | ok | ok | yes |
| HR2 | S337 ch-swapfile.rst :127 (12) | ok / global-min | :13 | `3795013` | ok | ok | yes |
| HR3 | S337 ch-swapfile.rst :118 (9) | ok / global-min | :24 | `3530821` | ok | ok | yes |
| HR4 | S337 ch-swapfile.rst :13 (10) | ok / global-min | :17 | `---------------C------` | ok | ok | yes |
| HR5 | S338 swsusp-and-swap-files.rst :57-58 (20) | ok / global-min | :9 | `/swap/swapfile file 31722876` | ok | ok | yes |
| HR6 | S338 swsusp-and-swap-files.rst :61 (12) | ok / global-min | :32 | `1791060333 257 32484229120` | ok | ok | yes |
| HR7 | S339 systemd-hibernate-resume.service.xml :38 (12) | ok / global-min | :40 | `253:0` | ok | ok | yes |
| HR8 | S340 sysfs-power :307-308 (19) | ok / global-min | :44 | `3795013` | ok | ok | yes |
| HR9 | S341 mkinitcpio-install-resume :11-12 (9) | ok / global-min | :79 | `systemd 262 (262.1-1-arch)` | ok | ok | yes |
| HR10 | S340 sysfs-power :97-98 (19) | ok / global-min | :56 | `12835467264` | ok | ok | yes |

Statement word counts: 38, 43, 46, 34, 35, 42, 42, 36, 44, 44 (all ≥ 8). Six distinct snapshot
**files** are cited (S336–S341); 4 required. The quoted spans, checked verbatim, are exactly:
`resume=` continuation (6579 begins the entry; 6581-6582 is the minimal span), `that will print … for`
(127), `The value is the physical offset on the device.` (118), the NODATACOW bullet (13),
`has to be active … suspending.` (57-58), `the location of its header need not be the same as before.` (61),
`Internally, it works by writing … device node to` (38), `Using this sysfs file will override … disk offset.`
(307-308), the `systemd_ver >= 255` / `add_binary` pair (11-12), `string representing … in bytes.` (97-98).
All host values sit on their cited receipt lines (4, 13, 24, 17, 9, 32, 40, 44, 79, 56).

Verdict: the frozen counter's 10/10 `met` is reproduced exactly by an independent implementation
(10/10 rows agree, same verdict/counts, same distinct-file count), and every row also satisfies the
stricter global minimal-span reading. This is a **provenance-shape** result only.

## 3. Cheapest junk entries — the shape gate's limit (confirmed) and three defects

`junk.py` (this dir) builds mechanically generated entries in a scratch root and runs both tools.
Command: `python3 .../junk.py --lane . --work "$S/junkwork" --mode all --seed 84` → rc 0.
Full matrix in `receipts/junk-all.json`; patched-counter re-runs in `receipts/patched-counter-runs.json`.

| Entry | what it is | frozen counter | independent checker |
|---|---|---|---|
| plain | 7 rows; 4 real snapshots; quotes = random unique 6–10-token windows; host value = random unique receipt token; one boilerplate statement | **met 7/7, rc 0** | met 7/7 |
| cross | 7 rows; `source.snapshot` keys point at **host/receipt.txt** (host manifest), `host.receipt` points at **src/sysfs-power** (source manifest); 4 keys, one file | **met 7/7, rc 0** | unmet 0/7 (`R3-snapshot-not-in-source-manifest`) |
| url | plain with every `url` field removed | unmet 0/7 (`R3-snapshot-url-not-https`) | met 7/7 |
| onefile | 7 rows; 4 snapshot keys all pointing at `kernel-parameters.txt` | **met 7/7, distinct_snapshots 4** | met 7/7, `distinct_snapshot_paths` **1** |

The plain result **confirms** the L1's finding and corollary M3: a boilerplate entry built from random
spans, needing no domain reading, reads `met`. The `cross`, `url` and `onefile` results expose three
further defects in the frozen instrument (below).

## 4. Defects in `tools/count-resume-rows-r84.py` (report only; lane untouched)

**D1 (behaviour contradicts docstring R3/R5; proves met on cross-manifest junk).**
`tools/count-resume-rows-r84.py:121` merges both manifests into one dict
(`manifests.update(parse_manifest(...))`), and `load()` at `:144-155` looks paths up in that merged
dict. So R3 accepts a `source.snapshot` path listed only in the **host** manifest, and R5 accepts a
`host.receipt` path listed only in the **source** manifest, although R3/R5 say the path must be listed
in the named manifest. Measured: the `cross` junk entry (zero genuine source snapshots, zero genuine
host values) reads **met 7/7, rc 0**.
Proposed patch: `.ufo/waves/round-84/w1/ExecProvenanceC1/proposed-counter-fix.diff` (separates the
manifests by kind; applies at lines 113–155). Verified on a scratch copy:
`count-resume-rows-r84.patched.py` reads the lane entry **met 10/10** (no regression) and the `cross`
junk **unmet 0/7** with `R3-snapshot-not-in-frozen-manifest` (`receipts/patched-counter-runs.json`).

**D2 (extra condition not in the predicate text).** `:142` additionally requires
`source.snapshot`'s `url` to start with `https://`. Docstring R3 requires only a manifest-listed path,
matching declared sha256 and matching bytes; R4–R6 say nothing about a URL. Measured: the `url` junk
entry (otherwise identical to a `plain` entry that reads met) is refused 0/7. Either the check should
be dropped or the predicate text amended; that is an L1 freeze decision, so no patch is proposed here.

**D3 (`distinct snapshots` target counts declarations, not files).** `:210,220` count
`src["snapshot"]` keys. Four keys pointing at one file satisfy the `>= 4` target: `onefile` reads
**met 7/7, distinct_snapshots 4** while only one snapshot file is cited (independent checker also
reports `distinct_snapshot_paths: 1`). If "distinct snapshots" is meant as distinct files/URLs, the
verdict is loosened. No impact on the C1 entry itself (6 keys, 6 files). L1 decision.

**D4 (span minimality is local, not global).** `exact_span` (`:97-110`) enforces only that dropping
either end line loses the quote; a 2+-line span is accepted even if the same quote occurs entirely on a
shorter span elsewhere. This matches the docstring's parenthetical, so it is an ambiguity rather than a
bug; recorded because "EXACT minimal raw-line span" can also be read globally. My checker reports both;
all 10 rows and all 10 host values pass the global reading, so no measured impact this round.

**D5 (fixture quantity).** `_random_entry` (`:249-281`) can return six rows for F7 (6/40 selftest runs;
42/200 reproductions at `random.Random(7)`); F7 still passes because 6 < 7. Mechanism measured: all 42
short fixtures' 3-file samples included one of the two tiny code snapshots (`mkinitcpio-install-resume`,
25 lines; `mkinitcpio-hooks-resume`, 42 lines), whose few ≥8-word lines are exhausted by the second/third
row assigned to that key, so the 10000-try loop exits one row short. Cosmetic fixture nondeterminism; P1
itself produced 7 rows in all 40 selftest runs.

## 5. Per-row depth observations handed to ReviewEntry (exploratory; outside the counter verdict)

The shape gate checks provenance shape, not whether a quote supports its statement. Reading the cited
spans against the statements:

- **HR2**: quote stops mid-sentence at S337:127 (`…the adjusted value for`); the `-r` form is evidenced
  by receipt:11 (the command actually run), and the page-division claim by S337:128-129, outside the
  cited span.
- **HR3**: quote S337:118 stops before the contrast it is used for — `not the same value that filefrag
  prints` (S337:119) and the logical/physical explanation (S337:121-124). "logical address" in the
  statement is an interpretation of those lines.
- **HR4**: `even on a compress=zstd mount` (JSON) / `compress=zstd:3` (.md) is **not in the pinned host
  capture**: `grep -n compress receipt.txt facts.json` → no match. Live read-only `findmnt -no
  SOURCE,FSTYPE,OPTIONS /` shows `rw,noatime,compress=zstd:3,…`, so the detail is true today but
  unpinned; the row's host value only proves the `C` attribute.
- **HR9**: the statement's strongest clause (booted UKI initramfs carries the binary) cites
  `.ufo/waves/round-84/after/uki-initrd-contents.txt`, which is git-tracked at `c6ee78b2` but **not in
  the pinned host manifest** (`before/host/SHA256SUMS` lists only receipt.txt and facts.json). R3/R5
  cannot see it.
- **HR10**: "the image must fit in free swap" overstates the cited source: `sysfs-power:97-103` says
  image_size is an upper limit the kernel tries to honour, and "if it turns out to be impossible, the
  kernel will try to suspend anyway using the smallest image possible". The numbers verify:
  image_size 12835467264 B against free swap 31722876−11942400 KiB ≈ 20.3 GB at capture.
- The `.md` host line references all verify exactly (:4, :9, :13, :17, :24, :32, :36, :40, :44, :56,
  :71, :75, :79); HR6 birth `1791060333` = `2026-10-03 17:45:33 -0300` (`date -d @1791060333`); the
  pinned `hooks/resume` + `install/resume` are byte-identical to the host's
  `/usr/lib/initcpio/{hooks,install}/resume` (sha256 `3cf8144c…`, `207d0eb3…`), so the `.md`'s
  QUALITY 103/113 equivalence claim holds; host versions match (kernel `7.2.11-arch1-1`, btrfs-progs
  `v7.1`, systemd `262 (262.1-1-arch)`, mkinitcpio `42.2-1`).
- Live read-only cross-check (pinned values unchanged today): `/sys/power/resume` `253:0`,
  `/sys/power/resume_offset` `3795013`, `/sys/power/image_size` `12835467264`,
  `map-swapfile -r` `3795013`, `filefrag` first physical `3530821`; `/proc/swaps` used is now
  `14933284` KiB (was `11942400`), i.e. HR10's headroom is time-varying as the row says.

## 6. Bounds respected / disclosure

- Host read-only: no hibernate/suspend, no swapon/swapoff, no sysfs writes, no sysctl, no boot/mkinitcpio
  change. Only reads and `sudo -n` read-only inspection (`map-swapfile -r`, `lsattr` not rerun,
  `filefrag -v`). No pacman. No tool installed or upgraded.
- No git/jj mutation; no lane file edited. Scratch root
  `/fast/scratch/hyaku/tsukuroi-r84/ExecProvenanceC1` used for fixture roots, receipts copied here, then
  removed.
- Disclosure: while saving a receipt I accidentally created an untracked file named `2` in the lane root
  (a stray redirect); I detected it immediately, verified it was the checker output, and deleted it.
  Tracked state unchanged; `git status` shows only the pre-existing `M corpus/lessons/round-84.md` and
  the wave's own untracked paths.
- Evidence in this dir: `check.py`, `junk.py`, `count-resume-rows-r84.patched.py`,
  `proposed-counter-fix.diff`, `receipts/{counter-master,counter-freeze,counter-preround,counter-candidate}.txt`,
  `receipts/selftest-5.txt`, `receipts/selftest-40.json`, `receipts/check-master-rev.json`,
  `receipts/check-master.json`, `receipts/check-candidate.json`, `receipts/junk-all.json`,
  `receipts/patched-counter-runs.json`.

## 7. Verdict

- C1 provenance shape gate: **reproduced, met 10/10** on `master` (`69915b86`) and on the candidate
  `c6ee78b2`; 10/10 rows agree with the frozen counter under an independently written predicate, 6/6
  distinct snapshot files, both manifest pins and all pinned bytes verified, all spans globally
  minimal. It remains a **shape** reading: C1 stays exploratory (`unprovable-but-better` only by the
  named reviewer's per-row judgment), earns no ordinal move, and the 10/10 earns nothing.
- The frozen counter is not a measurement: a boilerplate junk entry reads `met` (confirmed), and D1
  lets a cross-manifest junk entry read `met 7/7` with zero genuine citations. If this instrument is to
  gate anything later, apply the D1 patch first; D2/D3/D4 are L1 freeze decisions.
- Unrun: none of this seat's steps; C2's battery and the per-row reviewer judgment belong to other seats.
