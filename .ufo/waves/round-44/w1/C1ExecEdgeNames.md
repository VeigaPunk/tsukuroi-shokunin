VERDICT: defect-found

Item C1-8 — edge inputs the C1 counter does not draw. Arm measured: lane revision
`7e081698d4fc3c4ea944884fd093058de9909de1`, `tools/tsukuroi-census.sh` sha256
`fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c` (identical at the arm
revision and at lane HEAD `ff2c264a`, receipt `C1ExecEdgeNames/revisions.txt`).

`defect-found` means: the arm survived **all 65** edge fixtures with contract-shaped output,
no hang, no forged line, no stderr and no injected token — the declared C1 contract holds on
every enumerated case — but five uncontracted behaviours exist, and one of them (**Gap 1**)
prints a reading the probe cannot support (`orphan=0`, `state=RECORDED`, no BLOCKED reason)
when the sysfs root exists but is not a directory. None of the five is reachable on this
host's live shape (`C1ExecEdgeNames/live-shape.txt`). No live-host defect; no claim of C1 is
falsified.

## 1. What holds (the C1 claim survived its edges)

- 65 fixture cases; every one emitted **exactly two stdout lines** and **zero stderr bytes**
  (`C1ExecEdgeNames/summary.txt`; each `.out`/`.err` under `C1ExecEdgeNames/out/`). Every
  SCRUB line matched the header grammar
  `^SCRUB btrfs-scrub-record state=(NONE|RECORDED|BLOCKED) dir=(absent|present|unreadable)
  records=N tmp=N sockets=N unreadable=N orphan=N limited=N timers=N( detail=<tok>(,<tok>)*)?$`
  with **no whitespace inside `detail`** — the regex is in `C1ExecEdgeNames/h.sh:3` and was
  applied to every run.
- No hang: a FIFO at `devinfo/1/scrub_speed_max` (C1), a symlink to `/dev/zero` there (C2),
  a FIFO record (G4), dangling symlinks (B1, C12, F2) all returned; every case ran under
  `timeout 10` (default) and the two pathological payload cases under `timeout 60`/`120`.
  Longest observed probe: 4585 ms (D6b, a 2,000,000-line attribute fixture; 4.6-5.4 s across
  three reruns).
- No injection: names are never echoed. A `TSUKUROI_SCRUB_DIR` containing a space **and** a
  newline reads `dir=present` with the path absent from the line (C13), and every `detail`
  token is one of a closed set, a validated 8-hex fsid prefix, a decimal devid, or a
  `^[0-9]+$` value (`tools/tsukuroi-census.sh:1971-2036`).
- Verdict-neutral and errexit-safe: `probe_scrub_record` ends in an unconditional
  `return 0` (`tools/tsukuroi-census.sh:2039`) and a driver that sources the census minus its
  final `main "$@"` line under the census's own `set -euo pipefail`
  (`tools/tsukuroi-census.sh:453`) printed its line in every H case — an empty, absent or
  unreadable sysfs cannot abort the census under `set -u`/`set -e`.
- `18446744073709551615` (D1), `000` (D2), `5\r\n` (D4), `+5`, ` 5`, `5 `, `0x10`, 31 digits
  (D5), 8 MiB of digits (D6): no arithmetic on the value anywhere, so no overflow; every one
  either counts as limited with the literal preserved or reads `speed-malformed`.
- Scale: 1000 records + 1000 fsids 154 ms (E1), 1000 records on an empty sysfs `orphan=1000`
  32 ms (E2), 1000 timer links 5 ms (E3), 4000 records + 4000 fsids 1525 ms (H9). The orphan
  test rescans `fsids` per record (`tools/tsukuroi-census.sh:2009`), so cost is quadratic in
  fsid count; on any real host that count is the number of mounted btrfs filesystems.

## 2. Novelty vs the nine `(R44-C1)` selftest cases

Already drawn by the selftest (`tools/tsukuroi-census.sh:3229,3236,3244,3251,3257,3263,3271,3278,3285`)
— my cases only re-confirm, they are not new: absent dir/absent sysfs (B3, H2); 000 record dir
(B4); non-uuid names ignored (A3 near-miss); missing `scrub_speed_max` (C4); non-decimal
value (C5's text class); sysfs absent with a record (H3); bare template + non-scrub timers
(F3, F5); newline name never echoed (A5, A6 — case 3278 already plants a newline name with a
forged rollup); symlink and directory record, non-socket progress (G1, G3).

Not drawn by any of the nine: uppercase/mixed-case fsid, trailing-text names, spaces, glob
characters; a dangling-symlink or regular-file `SCRUB_DIR`; `sysfs:unreadable` for **this**
arm (1974 is only exercised by the round-38 storage arm); a FIFO or `/dev/zero` symlink at
`scrub_speed_max`; a symlink-to-file there; an empty or two-line attribute; `u64max`, `000`,
CR; non-decimal devid for this arm; non-dir sysfs root; fsid without `devinfo`; 1000/4000
records and 1000 timers; a **directory** named `btrfs-scrub@x.timer`; a dangling timer link;
`wants` as a regular file; `set -eu` with empty fixtures; a `SCRUB_DIR` containing a newline.

## 3. Method

- `tools/tsukuroi-census.sh` at the arm revision with only its last line (`main "$@"`)
  removed (`head -n -1`, 195,246 B, sha256 in `C1ExecEdgeNames/revisions.txt`) → the scratch
  library the drivers source; driver
  `C1ExecEdgeNames/drive.sh` (`set -uo pipefail`) and `C1ExecEdgeNames/drive_e.sh`
  (`set -euo pipefail`) source it, call `probe_scrub_record`, print `LINE $SCRUB_LINE` and
  `MS <ms>` (`${EPOCHREALTIME}` delta around the probe only).
- Every fixture under `/fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames/fx/<case>` with
  `TSUKUROI_SCRUB_DIR` / `TSUKUROI_BTRFS_SYSFS` / `TSUKUROI_TIMER_WANTS` pointing into it;
  no host path read by any case except the read-only live-shape capture (§6).
  `TMPDIR` set to the scratch dir; no `btrfs`, `systemctl`, `sudo`, sysfs write or service
  call; no live-mode run (the live leg belongs to `C1ExecLiveRead`).
- Harness + all case scripts are receipts (`C1ExecEdgeNames/h.sh`, `caseA|B|D|E|F|G.sh`,
  `drive.sh`, `drive_e.sh`), so every number below is reproducible; the patch-validation pair
  is `C1ExecEdgeNames/cmp5.sh` + `patch5.py` (payload matrix) and `cmpall.sh` + `patch_all.py`
  (all five gaps, §5.6).

## 4. Full case table (65 cases, the line as printed)

```
<case>  ms=<probe ms>  <SCRUB line>
```
The table is `C1ExecEdgeNames/summary.txt` (66 lines: 65 cases + 1 note). Groups: A = record/
sysfs *names*, B = `SCRUB_DIR` shape, C = sysfs/attribute shape, D = attribute *values*,
E = scale, F = timers, G = record/tmp/progress file types, H = `set -euo pipefail`, absent
paths, combined reasons. Nothing in it deviates from §1; the five gaps in §5 are the
substantive remainder.

## 5. Contract gaps and proposed fixes

### Gap 1 (substantive) — a sysfs root that exists but is not a directory silently disables the orphan test

Evidence (C8): `TSUKUROI_BTRFS_SYSFS` a regular file, one record present →
`state=RECORDED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`
— no detail, no BLOCKED. Compare the two neighbouring shapes, which are both BLOCKED: a
dangling symlink at that path → `detail=sysfs:absent` (C12), a 000 root →
`detail=sysfs:unreadable` (C11). Locus: `tools/tsukuroi-census.sh:1974` (`-d` + unreadable),
`:1976` (`elif [ -d ]`), and the closing test at `:2019`
`[ "$rec" -gt 0 ] && [ "$sysok" -eq 0 ] && [ ! -e "$root" ]` — a regular file is `-e`, so
`sysfs:absent` never fires while `sysok` is 0, and `orphan` stays 0. The contract's own words
("an existing dir, sysfs root or wants dir the caller cannot list", header
`tools/tsukuroi-census.sh:401-402`) already imply this shape is BLOCKED; the enumerated reason
list just has no token for it. Consequence: a record for an unmounted filesystem is reported
as mounted. Header's stated purpose ("the part an unprivileged reader can see") is defeated
silently, which is the one class the arm's own comment (`:1899-1901`, round-38 arm) calls out.

Proposed code (`:2019`):
```bash
      if [ "$rec" -gt 0 ] && [ "$sysok" -eq 0 ]; then
        blocked=1
        if [ -e "$root" ]; then detail+='sysfs:not-directory,'; else detail+='sysfs:absent,'; fi
      fi
```
Proposed header text (replace the last clause of the BLOCKED list, `:405-406`):
"records present with no sysfs root to judge orphans by (sysfs:absent), or with a sysfs root
that exists but is not a directory (sysfs:not-directory); else RECORDED …".
Proposed selftest case: a fixture whose `TSUKUROI_BTRFS_SYSFS` is a regular file (nothing to
list) plus one record → `state=BLOCKED dir=present records=1 tmp=0 sockets=0 unreadable=0
orphan=0 limited=0 timers=0 detail=sysfs:not-directory`.

Note (not mine to fix): the round-38 storage arm has the same `-d`-only shape and no `-e`
fallback at all (`tools/tsukuroi-census.sh:1908-1914`), so a non-dir root makes it read
"no btrfs filesystem" 0/0/0. Flagged for the integrator; the same one-line fix applies.

### Gap 2 — timer entries are counted with no type check

Evidence: a **directory** named `btrfs-scrub@data.timer` → `timers=1` (F1); a dangling
symlink → `timers=1` (F2); names containing `*` and `[b]` → `timers=2` (C14). Locus
`tools/tsukuroi-census.sh:2027-2031`: the loop tests only `-e`/`-L` and the bare-template
name. The header says "entries … (what `systemctl enable` links)" (`:398-400`); `systemctl
enable` writes symlinks, so a directory is not an enabled timer — and unlike records and
progress it is not flagged as a wrong type.

Proposed code (`:2027-2031`):
```bash
      for e in "$tw"/btrfs-scrub@*.timer; do
        [ -e "$e" ] || [ -L "$e" ] || continue
        [ "${e##*/}" != 'btrfs-scrub@.timer' ] || continue
        if [ ! -L "$e" ]; then blocked=1; detail+='timers:not-link,'; continue; fi
        tim=$((tim + 1))
        [ -e "$e" ] || detail+='timers:dangling,'
      done
```
Proposed header text (`:398-400`): "timers: `btrfs-scrub@<instance>.timer` **symlinks** under
TSUKUROI_TIMER_WANTS — what `systemctl enable` creates; the bare template name is not an
instance and is not counted, a name of that shape that is not a symlink is BLOCKED
(timers:not-link), and a symlink whose target is gone is still counted and listed
(timers:dangling)." Selftest: `mkdir -p "$FX/wants/btrfs-scrub@data.timer"` → BLOCKED
`detail=timers:not-link`; `ln -s /nonexistent …/btrfs-scrub@data.timer` → `timers=1
detail=timers:dangling`.

### Gap 3 — `scrub_speed_max` is followed through a symlink and its target is read

Evidence (C3): a symlink at `devinfo/1/scrub_speed_max` → a regular file outside sysfs →
`limited=1 detail=aaaaaaaa:1:speed_max=77`. Locus `:1986` tests only `-f`/`-r`, which follow
links. Records, tmp and progress all reject symlinks explicitly (`:2006`, `:2011`, `:2015`), so
this is the one kind without the same guard; the kernel never creates a symlink at a sysfs
attribute path (S243 `.ufo/waves/round-44/frozen/src/sysfs.c:2021-2049`,
`BTRFS_ATTR_RW(devid, scrub_speed_max, …)`).

Proposed code (`:1986`):
```bash
        if [ -L "$f" ] || [ ! -f "$f" ] || [ ! -r "$f" ]; then blocked=1; detail+="$fs8:${dev##*/}:speed-unreadable,"; continue; fi
```
and header text at `:404-405`: "… or not one decimal line (<fsid8>:<devid>:speed-unreadable;
a symlink at that path is not the attribute), …".

### Gap 4 — a mounted fsid with no `devinfo` subtree reads `limited=0` unflagged

Evidence (C9): `sysfs/<fsid>/` with no `devinfo` → `records=1 orphan=0 limited=0`, no detail;
`devinfo` as a plain file behaves the same. The kernel creates `devinfo` in
`btrfs_sysfs_add_fsid` (S243 `sysfs.c:2275`) and one `<devid>` kobject per device in
`btrfs_sysfs_add_device` (`sysfs.c:2134-2166`), so an empty/absent `devinfo` under a mounted
fsid is not a steady state and deserves at least a token. Locus `:1978-1983`: the glob is
skipped silently when it does not expand.
Proposed (non-blocking, so the verdict map is untouched): append `detail+="$fs8:?:no-devinfo,"`
after the device loop when `[ -d "$fsd/devinfo" ]` is false or the glob did not expand; header
addition to the clause at `:404-405` and to the known-limit paragraph at `:407-408`: "a mounted
fsid whose devinfo subtree is absent or empty reads limited=0 and is listed as
<fsid8>:?:no-devinfo".

### Gap 5 — the attribute read is unbounded

Evidence: an 8 MiB single-line attribute (D6) is accepted and reproduced verbatim in the
census's own line — `detail=…` makes the SCRUB line **8,388,751 characters**, 249 ms
(`out/D6-8MiB-single-line.out.TRUNCATED.txt` keeps the head plus the byte count); 2,000,000
one-digit lines (D6b) cost 4585 ms in the `while read` loop before `speed-malformed`.
Locus `:1987-1990`. A kernel attribute cannot exceed one page and prints `%llu\n`
(S243 `sysfs.c:2021-2028`, `sysfs_emit(buf, "%llu\n", …)`), so the live risk is nil — but the
path is reachable through Gap 3 or an override, and the arm's contract is "one line" of a fixed
grammar.
Proposed code (replace `:1987-1990`; 20 digits is the widest legal value, so 32 is safe slack;
`rest` joins the `local` list at `:1969` and `line`/`nl` leave it):
```bash
        v='' rest=''
        { IFS= read -r -n 33 v || [ -n "$v" ] || true          # bounded: 20 digits + \n + slack
          IFS= read -r -N 1 rest || [ -n "$rest" ] || true; } < "$f"   # any further byte = not one number
        if [ "${#v}" -ge 33 ] || [ -n "$rest" ] || ! [[ $v =~ ^[0-9]+$ ]]; then
          blocked=1; detail+="$fs8:${dev##*/}:speed-malformed,"; continue
        fi
        if ! [[ $v =~ ^0+$ ]]; then lim=$((lim + 1)); info+="$fs8:${dev##*/}:speed_max=$v,"; fi
```
Two details are load-bearing and were both found the hard way (variants rejected by test,
`out/patch5-validation.txt`): the two reads must share **one** redirect (a second `< "$f"`
reopens the file at byte 0, and reading stdin reads nothing); and the second read must be
`-N 1`, not `-n 1`, because `-n` honours and *swallows* the delimiter, so `5\n\n` would pass as
`5` where the arm reads `speed-malformed`. Also `read -N` assigns nothing at EOF, so `-n 33`
is used for the value read. Header: "… not one decimal line of at most 32 bytes
(…:speed-malformed)".

### Validation of the five patches (`out/patchall-validation.txt`, `out/patchall-selftest.txt`)

All five applied to a scratch copy of the arm (`patch_all.py`, `cmpall.sh`) and measured
against the unpatched arm on the same fixtures:
`non-dir sysfs root` → `BLOCKED … detail=sysfs:not-directory` where the arm reads `RECORDED
orphan=0`; `directory named …@data.timer` → `BLOCKED … detail=timers:not-link` (arm `timers=1`);
`dangling timer link` → `timers=1 detail=timers:dangling` (arm `timers=1`, no detail);
`symlink scrub_speed_max` → `BLOCKED … speed-unreadable` (arm `limited=1 speed_max=77`);
`fsid without devinfo` → `detail=aaaaaaaa:?:no-devinfo` (arm silent); the eight-payload value
matrix is byte-identical (`out/patch5-validation.txt`: 17 `SAME`, 1 intended `DIFF` — the 8 MiB
line becomes `speed-malformed`, and D6b drops from 5391 ms to 0 ms); and the arm's own
`--selftest` still reports `TSUKUROI_CENSUS_SELFTEST: PASS (141 cases, 141 passed, 0 failed)`
— same count as the arm's after receipt (`.ufo/waves/round-44/after/c1-after-ab8aae1.jsonl`,
`selftest_line`). One intended change of reading is worth naming: with Gap 2 applied, a
**regular file** named `btrfs-scrub@x.timer` in `timers.target.wants` turns a `RECORDED` line
into `BLOCKED` (H6 regression fixture); if the integrator prefers to keep the state and only
flag it, use a non-blocking `timers:plain-file` token instead of `timers:not-link`+BLOCKED —
either way the header must stop implying "any entry".

## 6. Live host shape (read-only context, `C1ExecEdgeNames/live-shape.txt`)

`/var/lib/btrfs` absent; `/sys/fs/btrfs` holds `1d02a454-c549-4a35-b567-89d60902af8e` with
`devinfo/1/scrub_speed_max` = 0; `timers.target.wants` has no `btrfs-scrub@*` entry; uid 1000.
So the live reading is `dir=absent … limited=0 timers=0` (`state=NONE`), and none of the five
gaps has a live shape here: Gap 1 needs a non-dir `/sys/fs/btrfs`, Gap 2 a non-link
`btrfs-scrub@*.timer`, Gap 3 a symlink under `devinfo`, Gap 4 a `devinfo`-less mounted fsid,
Gap 5 an attribute larger than a page.

## 7. Host-guard disclosure — misroot (mine, disclosed as instructed)

At **21:08:59** my inline `bash -c` batch ran with cwd `/home/vgpnk/Projects/shokunin` and one
hand-written fixture argument was `dev0 "$PWD/fx/A2-uppercase-fsid-sysfs/sysfs"`, which created
`/home/vgpnk/Projects/shokunin/fx/A2-uppercase-fsid-sysfs/sysfs/11111111-2222-3333-4444-555555555555/devinfo/1/scrub_speed_max`
(4 bytes, `0\n`) in the fleet root. The L1 detected it; the orchestrator moved it to
quarantine; `ls -ld /home/vgpnk/Projects/shokunin/fx` → "No such file or directory" when I
checked at 21:12, and I did not touch the quarantined copy. Cause: the harness function
`mkenv` already used the absolute `$S`, only that one inline argument did not. Every later
case script uses `$S`/`$FX` absolute (`C1ExecEdgeNames/case*.sh`), and all my writes are under
`/fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames/` plus this seat's two permitted paths.
Same batch defect, disclosed: its UUID was digits-only (`1111…-5555…`), so "uppercase" was
vacuous; A1/A2 were re-run with a hex-letter UUID (`aaaaaaaa-…-eeeeeeeeeeee`, `AAAAAAAA-…`) and
the table/receipts carry only the re-run (the two stale receipts were deleted).

## 8. Tooling

Nothing installed, upgraded or removed (no pacman — transactions are paused host-wide —, no
`uv tool`, no `npx`, no binary). Used: bash 5, coreutils, python3 (fixture generation and the
one `AF_UNIX` socket bind, run with a relative path because the scratch path exceeds the
108-byte `sockaddr_un` limit).

## 9. What I did not do

- Did not run the full census on the live host (that is `C1ExecLiveRead`); my only live reads
  are the four `ls`/`cat` in §6 plus the shipped defaults, which I resolved without touching
  them (`SCRUB_DIR=/var/lib/btrfs BTRFS_SYSFS=/sys/fs/btrfs
  TIMER_WANTS=/etc/systemd/system/timers.target.wants`, `out/H8-default-paths.txt`).
- Did not run the C1 counter or the C2 counter (other seats own those gates). I did run
  `--selftest` **once** on my patched scratch copy (35.8 s, 141/141 — `out/patchall-selftest.txt`)
  to validate the proposed fixes; the shipped arm's selftest I did not run, so the arm's
  141/141 figure is quoted from its after receipt, and my statements about which edge cases the
  nine `(R44-C1)` cases draw are read from `:3226-3287`, not from a run.
- Did not test signals/`SIGINT`-cancel semantics, `btrfs scrub start` behavior or anything
  needing CAP_SYS_ADMIN — out of an unprivileged read-only seat.
- Did not edit the lane, regenerate fixtures against other revisions, or judge the arm's
  verdict-neutrality on the live host.
