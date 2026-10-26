VERDICT: defect-found

# DefOwnWorkCopy — D-3 (routed defect 7): S206/S207 sibling-repo own-work anchors

Seat: leaf, round 38 wave 1. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` at HEAD
`5edb6c2` (observed: `git log -1 --format='%H %s'` → `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf
round-38: registry rows for storage-arm-r38, storage-arm-r38-q82, hook-order-r38 (QUALITY 70)`).
No lane file was edited; no git/jj mutation; no host change (no pacman transaction, service, hook,
sysfs, journal, boot or `/etc` action); `/home/vgpnk/Projects/shokuknow` was read only.

Defect 7 is confirmed as stated in `corpus/lessons/round-37-verifier-spotcheck.md:131`
("S206/S207 own-work anchors are sibling-repo paths (`shokuknow/lanes/tsukuroi/round9/…`). Commit
the captures into the lane, or cite a re-runnable command."). The rows' **taught lines are not
falsified**: both are byte-exact. The defect is the anchor's resolvability, and this seat lands the
lane copy plus a drafted append-only correction.

## 1. What the rows claim, and where the anchor points

`corpus/SOURCES.md:215-216` (read verbatim):

```
| S206 | shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt — own-work host mapping capture | own-work | A | EACCES-to-number mapping on the captured Arch Linux x86_64 host | lines 1-10, capture 2026-10-24 | define EACCES 13 /* Permission denied */ | mined | 2026-10-25 | on-release | corpus/knowledge/errno-contract-variance-r37.md |
| S207 | shokuknow/lanes/tsukuroi/round9/lane-errno13-probe.txt — own-work lane recheck capture | own-work | A | The bounded 2026-10-24 recheck of retained errno:13 journal evidence | lines 1-8, capture 2026-10-24 | probe journal matches for errno:13 -> 0 | mined | 2026-10-25 | on-release | corpus/knowledge/errno-contract-variance-r37.md |
```

The same unresolvable string is propagated to `corpus/knowledge/errno-contract-variance-r37.md:6-7`
(`source: S206 — \`shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt\``), to
`corpus/lessons/round-37.md:17-18`, and to the staged append `.ufo/waves/round-37/assimilation/SOURCES.append.md:7-8`.
The round-37 closure itself recorded the caveat and the byte check
(`corpus/lessons/round-37-verifier-spotcheck.md:94`: "Both quoted lines match byte-for-byte. Caveat:
the anchor is a sibling-repo path, not a lane path (§6)").

## 2. Resolution failure, reproduced read-only

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
ls shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt
  -> ls: cannot access 'shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt': No such file or directory
ls /home/vgpnk/Projects/shokunin/shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt
  -> ls: cannot access '/home/vgpnk/Projects/shokunin/shokuknow/...': No such file or directory
ls -l /home/vgpnk/Projects/shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt
  -> -rw-r--r-- 1 vgpnk vgpnk 485 Oct 24 07:21 /home/vgpnk/Projects/shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt
```

The row path is relative to `/home/vgpnk/Projects` only, so it is neither lane-relative nor
absolute; a reviewer cannot follow it from the lane or from the fleet root.

## 3. Byte-exact lane copy, digests, provenance pin

Copied with `cp --preserve=timestamps,mode` into
`.ufo/waves/round-38/w1/DefOwnWorkCopy/` (mode 644 and the source mtimes are preserved):

| lane copy (lane-relative) | bytes | lines | sha256 |
|---|---|---|---|
| `.ufo/waves/round-38/w1/DefOwnWorkCopy/host-errno-capture.txt` | 485 | 10 | `50149f0d093437cd9be86d65fbda13fa263c8209670ae690d5c66f2eff01fcc6` |
| `.ufo/waves/round-38/w1/DefOwnWorkCopy/lane-errno13-probe.txt` | 372 | 8 | `1b2f2ac2b09bd709f535bbdbc0fa132d6dbb90a4e0474570a63cc5cdc42c968a` |

Verification performed (all observed):

- `cmp <shokuknow file> <lane copy>` → silent, exit 0, for both files.
- `sha256sum` on the sibling working-tree files → the two digests above (identical to the lane copies).
- Provenance pin: the sibling repo's commit `a9a1ee2c19cbc396da31dd7a7368f657fed6cfe1`
  ("Round 9: 25 of 32 members finished; …", 2026-10-24 07:25:06 -0300) holds both files; the commit's
  blobs are `f11b0256f787af4a532ed090023a0318da75d9d6` and
  `0de07080bb0dcc57340700a5f9608c2ce602488a` (`git rev-parse a9a1ee2c…:<path>`), and
  `git cat-file blob <blob> | sha256sum` reproduces the two digests above. Piping the same blob into
  `cmp - <lane copy>` prints `IDENTICAL` for both files, and
  `git -C /home/vgpnk/Projects/shokuknow status --porcelain -- lanes/tsukuroi/round9/` is empty.
  `git hash-object` of the lane copies returns the same two blob ids.
- File history, which the row text leaves out: both captures were introduced at
  `b7c17115a672afc37d14e4df54d1464cd48bde29` (2026-10-24 07:18:21 -0300) and rewritten at `a9a1ee2`
  (`git diff --stat b7c1711 a9a1ee2 -- lanes/tsukuroi/round9/` → host file 15 +/-, probe file 14 +/-).
  The `b7c1711` blobs are `c649d0d2f9eda550baea4895c3dc794575a1fceb` and
  `6c0d821df091ba9b75e632c2b835bc4109f49a27`; the differences are material to how the captures are
  read (§4a).
- Lane-copy inventory: `MANIFEST.sha256` in the seat dir holds exactly the two `sha256sum` lines.

Current lane state: `.ufo/waves/round-38/w1/DefOwnWorkCopy/` is **not** in HEAD
(`git ls-tree -r --name-only HEAD -- .ufo/waves/round-38/w1/DefOwnWorkCopy` → 0 lines; HEAD tracks 86
files under `.ufo/waves/round-38/`). `git check-ignore -v` on the lane copy → rc 1 (not ignored), so
the integration commit can add the directory normally.

## 4. Anchor cell vs teaches cell

Both comparisons are exact string equality against the parsed SOURCES cells (bash `[ "$t" = "$line" ]`),
plus `cat -A` to show no trailing-space artifact:

- S206 anchor `lines 1-10, capture 2026-10-24`: the file has 10 lines; line 1 is
  `# host errno number-to-name binding, captured 2026-10-24T07:21:36-03:00`; line 6 is exactly
  `define EACCES 13 /* Permission denied */` → `S206 teaches == line 6: EXACT`.
- S207 anchor `lines 1-8, capture 2026-10-24`: the file has 8 lines; line 1 is
  `# snapper-eacces-mechanism recheck probe re-run 2026-10-24T07:21:36-03:00`; line 3 is exactly
  `probe journal matches for errno:13 -> 0` → `S207 teaches == line 3: EXACT`.
- Scope cells are supported by the same bounded file, not by inference: S206 scope (EACCES mapping,
  Arch x86_64) rests on line 2 (`uname: Linux x86_64   distro: "Arch Linux"`), line 6 and line 10
  (`# summary: on this host EACCES is 13 and EROFS is 30`); S207 scope (bounded 2026-10-24 journal
  recheck) rests on lines 1-6, and its line 2 procedure reference resolves —
  `sed -n '3p' corpus/knowledge/snapper-eacces-mechanism.md` is the `recheck:` procedure containing
  `journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep -c 'errno:13'`.
- The taught proposition is narrower than the file, so nothing is over-claimed: S207's file also
  carries `probe errno:13 matches anywhere since 2026-10-01 -> 0`, `retained boots -> 6` and three
  `mechanism:` lines (lines 4-8) that the teaches cell does not assert.

Anchor-cell defects found: **none that falsify a row.** Two precision observations, recorded without
editing the rows (append-only):

1. Both anchor cells give a whole-file range (`lines 1-10`, `lines 1-8`) while the quote is at line 6
   and line 3. That matches the row style but is looser than `corpus/lessons/round-37.md:17-18`
   ("line 6" / "line 3"); a reader must scan to find the quoted line.
2. S206 line 1 self-describes the capture as a "number-to-name binding" while the content and the
   teaches cell are name-to-number (`define EACCES 13`). This is capture metadata wording; it does
   not change the quoted bytes.

Re-runnable cross-check (read-only; supports the S206 mapping without the sibling repo):

```
grep -nE '^#define[[:space:]]+(EACCES|EROFS)[[:space:]]' /usr/include/asm-generic/errno-base.h
17:#define<EACCES>13	/* Permission denied */
34:#define<EROFS>30	/* Read-only file system */
pacman -Qo /usr/include/asm-generic/errno-base.h
  -> ... is owned by linux-api-headers 7.2-1
```

(Tabs shown as `<…>`; observed on 2026-10-26.) Caveat: the capture is not raw command output — see
§4a — so the teaches cells equal the capture bytes, not the raw header bytes; the numbers agree.
S207's re-runnable form is the journal procedure at `corpus/knowledge/snapper-eacces-mechanism.md:3`,
whose result is time-dependent; the lane copy preserves the 2026-10-24 result. This seat did **not**
re-run that journal probe.

### 4a. Capture fidelity: `a9a1ee2` rewrote both files editorially

`git diff b7c1711 a9a1ee2 -- lanes/tsukuroi/round9/{host-errno-capture,lane-errno13-probe}.txt`
shows the earlier version was the literal form:

- host header `# host errno number->name binding, captured 2026-10-24T07:11:32-03:00`; line
  `#define<TAB>EACCES<TAB><TAB>13<TAB>/* Permission denied */`
- probe line `journalctl -g 'create subvolume failed' | grep -c errno:13 -> 0`

and `a9a1ee2` replaced them with the bytes the rows quote: `define EACCES 13 /* Permission denied */`
(no `#`, single spaces, plus a new line-10 summary) and `probe journal matches for errno:13 -> 0`
(plus a reworded second probe line and `mechanism:` lines), with both header timestamps moved from
`07:11:32` to `07:21:36`. So the current files are own-work **transcriptions/summaries**, not raw
captures: S206's quoted line is a rendering of `/usr/include/asm-generic/errno-base.h:17`, not that
header's bytes, and S207's quoted line no longer displays the command behind the zero. Both versions
assert the same EACCES 13 mapping and the same zero result, so no taught line is falsified; the
literal form stays retrievable read-only with `git -C /home/vgpnk/Projects/shokuknow cat-file blob
b7c1711:lanes/tsukuroi/round9/<name>`.

## 5. Draft — exact proposed append-only correction (SOURCES.md)

Insert as a new paragraph immediately after the existing "Round-37 search-log erratum" paragraph at
`corpus/SOURCES.md:294` and before `## Leads (unopened)` (`corpus/SOURCES.md:295`). Rows 215-216 stay
untouched.

```markdown
Round-38 S206/S207 own-work anchor correction (2026-10-26, routed defect 7): rows S206 and S207 name
`shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt` and `lane-errno13-probe.txt`, a path relative
to `/home/vgpnk/Projects` that resolves neither from this lane root nor from the fleet root (`ls
shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt` → "No such file or directory"), while both
taught lines are exact in the lane copies committed with this wave:
`.ufo/waves/round-38/w1/DefOwnWorkCopy/host-errno-capture.txt` (sha256
50149f0d093437cd9be86d65fbda13fa263c8209670ae690d5c66f2eff01fcc6, 10 lines, S206 quote at line 6) and
`.ufo/waves/round-38/w1/DefOwnWorkCopy/lane-errno13-probe.txt` (sha256
1b2f2ac2b09bd709f535bbdbc0fa132d6dbb90a4e0474570a63cc5cdc42c968a, 8 lines, S207 quote at line 3),
each `cmp`-identical to the shokuknow blobs f11b0256f787af4a532ed090023a0318da75d9d6 and
0de07080bb0dcc57340700a5f9608c2ce602488a at commit a9a1ee2c19cbc396da31dd7a7368f657fed6cfe1; those
lane paths are the anchors of record for S206/S207, the sibling paths are provenance only, and the
S206 mapping is re-runnable read-only with `grep -nE '^#define[[:space:]]+(EACCES|EROFS)[[:space:]]'
/usr/include/asm-generic/errno-base.h` → lines 17 and 34 (linux-api-headers 7.2-1, 2026-10-26).
```

Companion correction for the note that cites the rows (`corpus/knowledge/errno-contract-variance-r37.md`,
append; its `source:` lines 6-7 are header text and must not be rewritten in place):

```markdown
Round-38 anchor correction (2026-10-26): the `source:` lines above name S206/S207 by their sibling-repo
provenance path; the anchors of record are the lane copies under
`.ufo/waves/round-38/w1/DefOwnWorkCopy/` with the digests recorded in the round-38 S206/S207 correction
in `corpus/SOURCES.md`, and the sibling path is provenance only.
```

Optional third sentence for the same spot, because the pinned files are transcriptions rather than raw
output (`§4a` above):

```markdown
Round-38 S206/S207 capture-fidelity note (2026-10-26): both own-work files are transcriptions, not raw
command output — commit a9a1ee2 rewrote the literal `#define<TAB>…` header lines and the
`journalctl … | grep -c errno:13 -> 0` line into the normalized forms the rows quote — so the quotes are
exact against the lane copies while the S206 mapping is checked against
`/usr/include/asm-generic/errno-base.h:17` and the S207 zero against the procedure at
`corpus/knowledge/snapper-eacces-mechanism.md:3`, not against an archived raw transcript.
```

If a later gate needs a `capture_ref` in the round-18 appended-notices schema, note that
`tools/check-appended-notices.py`'s `CAPTURE_RE` accepts only
`^\.ufo/waves/round-[0-9]+/l1-capture/<name>$`; that registry would need a relocated copy with these
same digests. Not required for a SOURCES erratum.

## 6. Risks and limits

- The drafted sentence is true only once the wave's integration commit lands these lane copies; at
  HEAD `5edb6c2` the seat dir is untracked (verified in §3). The copies are not ignored, so a normal
  commit captures them.
- The sibling working tree can drift after `a9a1ee2`; the pin is the commit's blobs and the digests,
  not the mutable path.
- Capture fidelity: the pinned bytes are fixed, but they are editorial transcriptions (§4a). The
  `a9a1ee2` header time `2026-10-24T07:21:36-03:00` predates that commit by ~3.5 minutes and cannot be
  independently verified by this seat; a future recheck that needs raw output must read the `b7c1711`
  blobs or re-run the procedure. A digest pin does not supply that.
- Because the correction is append-only, the broken path text stays in rows 215-216 and in
  `corpus/lessons/round-37.md:17-18`; readers must apply the erratum.
- Not done by this seat: no journal probe re-run; no lane-gate or counter run (wave rules put gates
  with the parent); no attempt to fix the row cells themselves.

## 7. Files written (this seat only)

- `.ufo/waves/round-38/w1/DefOwnWorkCopy.md` — this report.
- `.ufo/waves/round-38/w1/DefOwnWorkCopy/host-errno-capture.txt` (485 B) and
  `lane-errno13-probe.txt` (372 B) — byte-exact lane copies.
- `.ufo/waves/round-38/w1/DefOwnWorkCopy/MANIFEST.sha256` — the two digests.
- `.ufo/waves/round-38/w1/DefOwnWorkCopy/COPY-RECEIPT.txt` — commands, outputs, provenance pin,
  path-resolution failure, host cross-check.

Scratch `/fast/scratch/hyaku/tsukuroi-r38/DefOwnWorkCopy` was used only as `TMPDIR` and is removed.
