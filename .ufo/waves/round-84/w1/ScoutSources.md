# ScoutSources — re-open every source of the hibernate-resume entry (round 84, wave w1)

Seat: ScoutSources (leaf, no subagents). Lane axes: operability + freshness.
Lane measured: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, `git rev-parse master` =
**f19e73f3aa9817e76044e4e43a343c6ca6d929df** ("round-84: registry rows — single tool per row, code-2 maps").
Freeze `e0f42051bf9b01af5857c28562ca0247a8fef367`, candidate `c6ee78b2d4184ace3c6d01116190729f0f7c2c31`,
C1 re-declaration `69915b8603d9e443f2e1c0021d7c34509186bd9e`. Nothing in this lane file was edited; the
working tree carries uncommitted edits by other seats (entry JSON/MD, lessons, QUALITY, the gate) — every
claim below is stated against the committed master tip, and I say so where the worktree differs.
Host actions were read-only: `curl`, `sha256sum`, `sed -n`, `grep`, `stat`, `cat /proc /sys`, and
`sudo -n btrfs inspect-internal map-swapfile -r` / `lsattr` / `filefrag -v`. No hibernate, no swapon,
no writes to /sys, /proc, /boot; no mkinitcpio; no pacman. No tool was installed (nothing needed installing:
curl, sha256sum, python3 and GNU tar were already present — see §7).

## 1. Live re-fetch of every source URL — PASS (9/9, byte-identical to every pin)

Command (all in parallel, into `$S/fetch`), `curl -sS -L --max-time 60 -o <f> -w '%{http_code}' <url>`:

```
kernel-parameters.txt                 http=200 rc=0 bytes=317993 sha256=23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c
swsusp.rst                            http=200 rc=0 bytes=18419  sha256=11f0c8cbe7aee9e17e172463dc1475f619e0bfa87568d448d6e6a75f853e52b6
swsusp-and-swap-files.rst             http=200 rc=0 bytes=2884   sha256=7334ffa5adb44c87d6b59cef49b26a2133436b3a4b84e044ecaf9887639ba71d
sysfs-power                           http=200 rc=0 bytes=18554  sha256=c2be59dd56c9c036b9daedc9fc041333a1dee964abdb71ca6bcefa8c9592a102
ch-swapfile.rst                       http=200 rc=0 bytes=7046   sha256=4442dc5b86a211618163461336a0f9d68a533f9a717f7a2e6c9e92baae4f2447
mkinitcpio-hooks-resume               http=200 rc=0 bytes=1124   sha256=3cf8144c2b528b6411c7a7aea1627472cf1aa77cf74547cebd663351ee931950
mkinitcpio-install-resume             http=200 rc=0 bytes=555    sha256=207d0eb3c469ebfeaad29a4ca7c209ab097d26087c458cf916012fe58ce4e83e
systemd-hibernate-resume.service.xml  http=200 rc=0 bytes=2717   sha256=170fb1f73bf34c85e20418168a649b45cd9e30d8b979a4f247860ec3ca3a43c5
cpython-subprocess.py (S342)          http=200 rc=0 bytes=90748  sha256=7fa4af83422024a19e64a80937f6c8094244c3397372a495b348dfbe44a5dd72
```
stderr files empty for all nine; exit status 0 for all nine.

Comparison against the pins:
* `before/src/SHA256SUMS` — `sha256sum -c SHA256SUMS` in `before/src/` → `ch-swapfile.rst: OK`,
  `kernel-parameters.txt: OK`, `mkinitcpio-hooks-resume: OK`, `mkinitcpio-install-resume: OK`,
  `swsusp-and-swap-files.rst: OK`, `swsusp.rst: OK`, `sysfs-power: OK`,
  `systemd-hibernate-resume.service.xml: OK`; **rc=0** (8/8 OK).
* S342's separate pin `7fa4af83422024a19e64a80937f6c8094244c3397372a495b348dfbe44a5dd72` — **match**
  (live fetch = pinned snapshot `.ufo/waves/round-84/before/src-lesson/cpython-subprocess.py` =
  `7fa4af83…`, verified by `sha256sum`; and the host's own `/usr/lib/python3.14/subprocess.py` has the
  same sha256 `7fa4af83…`, i.e. the pinned tag equals the host's file byte-for-byte).
* The manifest files themselves match the pins quoted in the declaration:
  `sha256sum .ufo/waves/round-84/before/src/SHA256SUMS` = `5d1673de7f893f035cb2808e9579bcdd292339a32dad605c6e3a53d6561f7eef`,
  `sha256sum .ufo/waves/round-84/before/host/SHA256SUMS` = `4ca3e20939eadff71c190f5e2d27a5f453479d0133321ebd118eb7eef624fde6`
  — both equal the frozen values in `tools/count-resume-rows-r84.py:47-50`.

**Freshness verdict: no upstream drift.** Every pinned snapshot still hashes to its declared digest; the
sources are still fetchable at the pinned tags with HTTP 200 and identical bytes. Receipt:
`.ufo/waves/round-84/w1/ScoutSources-receipts/fetch-sha256-2026-11-06.txt`.

## 2. HR1–HR10: quote at the cited raw lines, ≤25 words, verbatim modulo whitespace — PASS (10/10)

Method: I re-fetched the sources (§1) and re-implemented the frozen counter's own two predicates
(`norm` = whitespace-collapse; `exact_span` = quote inside span AND dropping line *a* or line *b* loses
the quote) against **my fetched copies**, then cross-checked with the frozen instrument.

For every row: the normalized quote occurs verbatim inside the normalized text of the cited raw lines in
my copy, and the cited span is the minimal span under the counter's rule.

```
HR1 S336 6581-6582 words=15 src=ok/ok host=ok/ok      HR6 S338 61-61    words=12 src=ok/ok host=ok/ok
HR2 S337 127-127   words=12 src=ok/ok host=ok/ok      HR7 S339 38-38    words=12 src=ok/ok host=ok/ok
HR3 S337 118-118   words=9  src=ok/ok host=ok/ok      HR8 S340 307-308  words=19 src=ok/ok host=ok/ok
HR4 S337 13-13     words=10 src=ok/ok host=ok/ok      HR9 S341 11-12    words=9  src=ok/ok host=ok/ok
HR5 S338 57-58     words=20 src=ok/ok host=ok/ok      HR10 S340 97-98   words=19 src=ok/ok host=ok/ok
```
Word counts (whitespace split) are 9–20 → all within the frozen 6–25 window. Host values verified at the
cited receipt lines of `before/host/receipt.txt` (sha256 `467a8827…`, matches the host manifest).

Cross-check with the frozen instrument at the candidate commit and at master tip:

```
$ python3 tools/count-resume-rows-r84.py --revision c6ee78b2d4184ace3c6d01116190729f0f7c2c31
{"verdict": "met", "counted": 10, "failed": 0, "distinct_snapshots": 6, "target_rows": 7, "target_snapshots": 4, …}
rc=0
$ python3 tools/count-resume-rows-r84.py --root .          # same, at the working tree
{"verdict": "met", "counted": 10, "failed": 0, "distinct_snapshots": 6, …}   rc=0
```
(Per the L1's own re-declaration, this 10/10 is a **provenance shape gate**, not a measurement; it earns
nothing. I report it as such.)

Verbatim line dumps (my fetched copies) for the ten cited spans — all ten rows' quotes sit inside them:
* `kernel-parameters.txt:6581-6582` → `given by "resume=" at which the swap header is located,` / `in <PAGE_SIZE> units (needed only for swap files).`
* `ch-swapfile.rst:127` → `that will print the device physical offset and the adjusted value for`
* `ch-swapfile.rst:118` → `The value is the physical offset on the device. Note that **this is not the same`
* `ch-swapfile.rst:13` → `* swapfile - must be NODATACOW (i.e. also NODATASUM, no compression)`
* `swsusp-and-swap-files.rst:57-58` → `partition.  In particular, the swap file has to be active (ie. be present in` / `/proc/swaps) so that it can be used for suspending.`
* `swsusp-and-swap-files.rst:61` → `the location of its header need not be the same as before.  Thus every time`
* `systemd-hibernate-resume.service.xml:38` → `Internally, it works by writing the major:minor of selected device node to`
* `sysfs-power:307-308` → `Using this sysfs file will override any values that were` / `set using the kernel command line for disk offset.`
* `mkinitcpio-install-resume:11-12` → `if (( systemd_ver >= 255 )); then` / `add_binary /usr/lib/systemd/systemd-hibernate-resume`
* `sysfs-power:97-98` → `string representing a non-negative integer that will be used` / `as an upper limit of the image size, in bytes.  The kernel's`

## 3. Live re-verification of the host side of every HR row (read-only, today) — PASS with one drift note

| Row | Claim | Live reading (2026-11-06) | Receipt value | Verdict |
|---|---|---|---|---|
| HR1 | cmdline `resume=/dev/mapper/root resume_offset=3795013` | `/proc/cmdline` → `resume=/dev/mapper/root` `resume_offset=3795013` | line 4 | confirmed |
| HR2 | `map-swapfile -r` → 3795013 | `sudo -n btrfs inspect-internal map-swapfile -r /swap/swapfile` → `3795013`; full form `Physical start: 15544373248` / `Resume offset: 3795013`; 15544373248/4096 = 3795013.0 exactly | line 13 | confirmed |
| HR3 | filefrag first extent physical 3530821 ≠ 3795013 | `sudo -n filefrag -v /swap/swapfile` → `0: 0.. 0: 3530821.. 3530821: 1:` | line 24 | confirmed |
| HR4 | `lsattr` shows `C` (No_COW) | `sudo -n lsattr /swap/swapfile` → `---------------C------` | line 17 | confirmed, and I checked the letter's meaning (below) |
| HR5 | swap file active, 31722876 KiB | `/proc/swaps` → `/swap/swapfile  file  31722876  …` | line 9 | confirmed |
| HR6 | birth 1791060333 = 2026-10-03 17:45:33 -03 | `stat -c %W /swap/swapfile` → `1791060333`; `date -d @1791060333` → `2026-10-03 17:45:33 -0300` | line 32 | confirmed |
| HR7 | `/sys/power/resume` = 253:0 = /dev/mapper/root | `cat /sys/power/resume` → `253:0`; `stat -L -c '%t %T' /dev/mapper/root` → `fd 0` (0xfd = 253) | lines 40, 36 | confirmed |
| HR8 | `/sys/power/resume_offset` = 3795013 | `cat /sys/power/resume_offset` → `3795013` (equal to cmdline and map-swapfile) | line 44 | confirmed |
| HR9 | systemd 262 | `systemctl --version` → `systemd 262 (262.1-1-arch)`; host pkgs `mkinitcpio 42.2-1`, `btrfs-progs 7.1-1`, `systemd 262.1-1`; `/usr/lib/initcpio/{install,hooks}/resume` diff empty vs the pinned snapshots | line 79 | confirmed |
| HR10 | image_size 12835467264 | `cat /sys/power/image_size` → `12835467264` | line 56 | confirmed |

**Drift note (expected, not a defect):** `/proc/swaps` *used* moved from the captured `11942400` KiB to
`14940124` (then `13650688`) KiB during the session — swap pressure only. Captured free swap =
31722876−11942400 = 19780476 KiB = 18.86 GiB = **20.26 GB (decimal)**, which matches the MD's "≈ 20.3 GB";
live free is still ≈ 16.0 GiB, above image_size (11.95 GiB), so HR10's headroom statement still holds.

**HR4's `C` letter — semantics verified, the entry reads it right.** `lsattr`'s output has 22 fixed
positions; I fetched e2fsprogs v1.47.4 `lib/e2p/pf.c` (upstream, HTTP 200) and the order is
`s,u,S,D,i,a,d,A,c,E,j,I,t,T,e,C,x,F,N,P,V,m` — so position 16 (0-based 15) is `C` = `FS_NOCOW_FL`
("No_COW"), while lowercase `c` is `EXT2_COMPR_FL` (Compression_Requested). The host's string has `C` at
position 16 and `c` absent. The kernel side matches: `FS_NOCOW_FL 0x00800000` in `include/uapi/linux/fs.h`
and btrfs `fs/btrfs/ioctl.c` maps `BTRFS_INODE_NODATACOW → FS_NOCOW_FL`. So `C` really is NODATACOW
(NODATASUM, no compression) — the entry's HR4 reading is correct, and the file is *not* compressed
(`c` absent) despite the `compress=zstd:3` mount option. (`/swap` the directory also shows `C`; btrfs
`mkswapfile` sets NOCOW on the file itself.)

## 4. SOURCES.md rows S336–S342 — anchor / tier / kind / used-by — 6 confirmed, 2 defects

Checked against **my fetched copies** (not the pinned ones) plus the pinned snapshots.

| id | anchor in SOURCES.md | anchor matches snapshot? | kind | tier | used-by file cites the id? | verdict |
|---|---|---|---|---|---|---|
| S336 | kernel-parameters.txt raw 6574-6583 | 6574 `resume=`, 6579 `resume_offset=`, 6583 `See Documentation/power/swsusp-and-swap-files.rst` — the block is exactly as described | docs ✓ | A ✓ | `corpus/knowledge/hibernate-resume-plane-r84.md` → `grep -c S336` = 1 ✓ | confirmed |
| S337 | ch-swapfile.rst raw 9-13, 111-146 | 9-13 = the five constraint bullets; 111 `Hibernation`, 146 `single device, etc.` — the `-r` example sits at 141-144 inside the range | docs ✓ | A ✓ | same file, `grep -c S337` = 3 ✓ | confirmed |
| S338 | swsusp-and-swap-files.rst raw 16-23, 56-58, 60-63 | 16-23 = the partition/offset paragraph; 57-58 = the `/proc/swaps` sentence; 60-63 = the recreate→update-resume_offset passage | docs ✓ | A ✓ | same file, `grep -c S338` = 2 ✓ | confirmed |
| S339 | systemd xml raw 36-50 (Description) | 36-50 are `<para>`s, but the `<title>Description</title>` is at line 32 and `</refsect1>` at 51 — the anchor labelled "(Description)" does not cover the section title | docs ✓ | A ✓ | same file, `grep -c S339` = 1 ✓ | **mismatch (minor)** — see D1 |
| S340 | sysfs-power raw 42-56, 91-103, 296-308 | 42 `What: /sys/power/disk`, 91 `/sys/power/image_size`, 296 `/sys/power/resume_offset` — exact | docs ✓ | A ✓ | same file, `grep -c S340` = 2 ✓ | confirmed |
| S341 | mkinitcpio install/resume raw 9-14, hooks/resume raw 12-17 | install 9-14 = the `systemctl --version` / `>= 255` block ending `fi`; hooks 12-17 = the comment + `-x` test + exec + `return` + `fi` | code ✓ | A ✓ | same file, `grep -c S341` = 1 ✓ | confirmed |
| S342 | cpython subprocess.py raw 388-401 (def call), 397-400 | `def call` actually spans **388-402**; line 402 is the `raise` — the very evidence for "then re-raises". The anchor's own claim "equal to inspect.getsource(subprocess.call) on the host" holds only for 388-402 | code ✓ | A ✓ | `corpus/lessons/round-84.md` → `grep -c S342` = 5 ✓ | **mismatch** — see D2 |

Also checked for every row: the cited pinned snapshot exists, its sha256 equals the digest in the row, and
equals the digest in the manifest; the URL in SOURCES.md is the URL I fetched.

## 5. Defects (file:line + proposed patch under my wave dir; the L1 decides what lands)

### D1 — `corpus/SOURCES.md:350` (S339 row): anchor range excludes the "Description" title it names
`tag v262, raw lines 36-50 (Description)` — but `<title>Description</title>` is at raw line 32 of
`systemd-hibernate-resume.service.xml` and `</refsect1>` is at 51; 36-50 starts at the second `<para>`
and drops both the title (32) and the first paragraph (34-35). HR7's cited line 38 is inside the range, so
the entry is unaffected; only the registry anchor mislabels its extent.
Proposed patch (`patch-D1-SOURCES-S339-anchor.md`, applied to a copy only):
`sed` on `corpus/SOURCES.md:350`, replace `raw lines 36-50 (Description)` with `raw lines 31-51 (Description
section); 38 (major:minor write)` — both endpoints verified against the fetched file.

### D2 — `corpus/SOURCES.md:353` (S342 row) and `corpus/lessons/round-84.md:27` (S342 row): the cited
range cannot support the claim, and one cited range is non-minimal
* SOURCES.md:353 says `raw lines 388-401 (def call), 397-400 (wait with timeout, kill in except)` and
  teaches "call() kills the child when wait(timeout) raises, **then re-raises**". In the pinned/tagged
  file the `raise` is line **402**; `397-400` ends at `p.kill()` (400) and never reaches it. The claim
  "equal to inspect.getsource(subprocess.call) on the host" is true only for 388-402 — I verified
  `pinned[388..402] == inspect.getsource(subprocess.call)` → **True**, and `pinned[388..401]` → **False**
  (missing the trailing `raise`). The row's own `teaches` clause is therefore uncited as written.
* lessons/round-84.md:27 cites `raw 397-400` for the quote
  "return p.wait(timeout=timeout) except: # Including KeyboardInterrupt, wait handled that. p.kill()".
  That normalized text sits in **398-400**; under the frozen counter's own `exact_span` rule 397-400 is
  `span-not-minimal` (dropping line 397 = `try:` still contains the quote). The quote itself is verbatim
  modulo whitespace ✓ (line 399's double space collapses).
Proposed patch (`patch-D2-S342-anchor.md`):
* `corpus/SOURCES.md:353` → `raw lines 388-402 (def call), 398-400 (wait with timeout, kill in except)`;
  and keep the "equal to inspect.getsource(subprocess.call) on the host" clause, which then holds exactly.
* `corpus/lessons/round-84.md:27` → `raw 398-400` instead of `raw 397-400`.
* `corpus/lessons/round-84.md:33` (the round-83 correction paragraph) → `raw 397-400 (S342)` → `raw 398-400 (S342)`.
Note the same correction is already reflected in the uncommitted working-tree copy of the lessons file —
which is why the master-tip text still carries the old range.

### D3 — `corpus/lessons/round-84.md:21,26,27`: the quoted word/token counts do not match the quotes
Whitespace-split counts of the quoted strings vs the labels printed in the row:
* :21 S336 — quote has **15** words, label says `(14 words)`;
* :26 S341 — quote has **9** tokens, label says `(8 tokens)`;
* :27 S342 — quote has **10** tokens, label says `(11 tokens)`.
The label convention is not defined anywhere I could find, and the same off-by-one appears elsewhere in
the corpus (`corpus/lessons/round-83.md:18` claims 17 vs 18; `corpus/lessons/round-81.md:25` claims 16 vs 15),
so it is a pre-existing bookkeeping habit rather than a new regression. It does **not** affect the frozen
predicate: the counter measures the JSON quotes (`len(q.split())`, 6–25) and all ten are 9–20 ✓.
Proposed patch (`patch-D3-lesson-wordcounts.md`): relabel :21 `(15 words)`, :26 `(9 tokens)`, :27 `(10 tokens)`.
Low severity; the L1 may prefer to leave the corpus convention alone.

## 6. Depth findings for the named non-author reviewer (C1 is exploratory: `unprovable-but-better`)

These are not provenance defects — every quote is verbatim at its cited lines — but they are places where a
row's *statement* asserts more than its *cited span* carries, and a per-row reviewer should weigh them.

1. **HR3 (JSON:87, cite S337:118)** — the statement says "filefrag … its physical_offset column is a
   btrfs logical address, not the device offset", but the cited line 118 is only
   "The value is the physical offset on the device." The filefrag contrast lives on line **119**
   ("this is not the same value that filefrag prints as physical offset!") and the logical↔physical
   explanation on **121-124** ("Btrfs filesystem uses mapping between logical and physical addresses …
   It's the device-specific physical offset that is suitable as resume offset"). The upstream never says
   "logical address" — the entry's reading is technically right (btrfs's filefrag `physical_offset` is a
   btrfs block address, not a device offset) but it is an inference the cited span does not state.
2. **HR2 (JSON:67, cite S337:127)** — the statement's "`-r` form prints the value already divided by the
   page size" is supported by lines **128-129** ("Note that the value is divided by page size") and
   **141-142** ("the option *-r* will print just the offset"), not by the cited 127. The upstream example
   (Physical start 811511726080 → Resume offset 198122980) and this host's own arithmetic
   (15544373248/4096 = 3795013) confirm the substance.
3. **HR9 (JSON:207, cite S341 install/resume:11-12)** — the statement's "so resume runs through that
   binary, not the hook's own resume= parser" is supported by **hooks/resume:12-17** (the `-x` test and
   the exec), which the row does not cite (the JSON cites only the install hook). SOURCES.md S341 does
   name both files and the hooks range, so the corpus holds the evidence; the row's own span does not.
   The uncommitted working-tree revision of HR9 already drops the "not the hook's own resume= parser"
   clause — the committed master-tip text still carries it.
4. **HR10 (JSON:227, cite S340:97-98)** — "the image must fit in free swap" is the entry's operational
   reading; the cited ABI text only bounds the image size ("will do its best to ensure the image size
   will not exceed this number. However, if it turns out to be impossible, the kernel will try to suspend
   anyway using the smallest image possible" — sysfs-power:99-101, outside the cited span). So the
   "must fit" is a *practice*, not a kernel guarantee. Worth a per-row note.
5. **HR8 (JSON:187, cite S340:307-308)** — "so no writer has changed it since boot" is inferred from
   sysfs == cmdline == map-swapfile; the ABI text says the sysfs file "overrides any values that were
   set using the kernel command line", so equality cannot distinguish "never written" from "written with
   the same number". The entry's own Limits section concedes it does not show which writer set it; that
   honesty should be reflected in the row's Status as well.
6. **Units note for HR10** — the MD computes free swap as "≈ 20.3 GB"; that is decimal GB (18.86 GiB).
   Both are stated consistently, but a reviewer should note the unit is GB, not GiB.
7. **ZWSP hazard (not a defect, a caution)** — `systemd-hibernate-resume.service.xml` contains **2718**
   U+200B zero-width spaces inside its `<filename>` tags (first on line 1). HR7's quote stops before any
   `<filename>` tag, so it is unaffected; any future quote that touches a filename must be ZWSP-aware.

New-ground check (supports the exploratory claim's premise): at the pre-round tip `64f45b79`,
`git grep -li 'map-swapfile' -- corpus/knowledge` and `-li 'image_size'` return **nothing**, and
`resume_offset` appears only at `journal-boot-plane.md:62` and `systemd-user-plane.md:218` — both merely
printing the cmdline. The new plane therefore lands on host ground no prior entry held, and it adds the
rule separating `map-swapfile` (3795013) from `filefrag` (3530821) that the prior state lacked.

## 7. Tooling

No tool was installed or upgraded: the seat needed only `curl`, `sha256sum`, `stat`, `sed`, `grep`,
`python3` (3.14.8, host default) and GNU `tar`, all already present. Per
`/home/vgpnk/.omp/agent/RULES.md` nothing was fetched outside the pinned upstream URLs except two
read-only upstream references used only to check a letter's meaning (`tytso/e2fsprogs` v1.47.4
`lib/e2p/pf.c`, `lib/ext2fs/ext2_fs.h`, `misc/chattr.c`; `torvalds/linux` v7.2 `include/uapi/linux/fs.h`,
`fs/btrfs/ioctl.c`, `fs/btrfs/inode.c`) — none of these are cited by the corpus; they are corroboration for
§3's `lsattr` reading. No pacman transaction was attempted (pacman guard: all transactions paused).

Scratch: `/fast/scratch/hyaku/tsukuroi-r84/ScoutSources/` (removed on exit); the fetch receipt was copied
into the wave dir at `.ufo/waves/round-84/w1/ScoutSources-receipts/fetch-sha256-2026-11-06.txt`.
No lane file was modified; the proposed patches live only under this wave dir.

## 8. Verdict summary

| check | result |
|---|---|
| 9/9 source URLs fetched live (8 from `URLS.txt` + S342) | HTTP 200, rc 0, byte counts and sha256 recorded |
| sha256 vs `before/src/SHA256SUMS` (8 files) | 8/8 OK (`sha256sum -c` rc 0) |
| sha256 vs S342 pin `7fa4af83…` | match (also = host `/usr/lib/python3.14/subprocess.py`) |
| manifest digests vs the frozen pins | `5d1673de…` / `4ca3e209…` — both match |
| HR1–HR10 quote in my copy at cited lines, ≤25 words, verbatim | **10/10 confirmed** (9–20 words each) |
| HR1–HR10 host value at cited receipt lines | 10/10 confirmed |
| frozen counter at candidate `c6ee78b2` and at master tip | `met`, 10/10, 6 snapshots, rc 0 (provenance gate only) |
| live host re-read of all 10 host facts | 10/10 confirmed; only swap *used* drifted (expected) |
| SOURCES.md S336–S342 anchors vs the fetched snapshots | 6 confirmed, **S339 and S342 mismatched** (D1, D2) |
| SOURCES.md tier / kind / used-by | 7/7 correct (docs×5, code×2; all tier A; every used-by file cites its id) |
| quote word/token labels in `corpus/lessons/round-84.md` | 3 off (D3) |
| new-ground premise at `64f45b79` | confirmed: no `map-swapfile` / `image_size` in `corpus/knowledge` |
| host actions | read-only only; no hibernate/suspend/swapon/sysctl//sys or //proc write, no mkinitcpio, no pacman |
