2026-11-03T22:39:00Z
# SC1Scribe — C1 note draft receipt (round 68 w1)

Seat: SC1Scribe (scribe, prose only). Draft written:
`.ufo/waves/round-68/drafts/c1/note.md`, 67 lines, sha256
1d2a4d8d78a0c1d0a704d887b26df4cc4e0c5f8fc979062f1fc7602fa30bbd8b
(`sha256sum .ufo/waves/round-68/drafts/c1/note.md`, rc 0). No lane file, no tracked
file, no registry row was written or edited by this seat.

## 1. Every quote in the note, with its grep -cF count and line number

All commands run in
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-68/before/src/` with
`grep -cF -- "<quote>" <file>` and `grep -nF -- "<quote>" <file>`; the count is lines
matched, and a multi-tag cell lists the count in that tag's file.

| # | quote (verbatim) | words | v7.2 line | v7.2 count | v7.3 line | v7.3 count |
|---|---|---|---|---|---|---|
| 1 | `Note that all fields in this file are hierarchical` | 9 | 1474 | 1 | 1501 | 1 |
| 2 | `killed by any kind of OOM killer.` | 7 | 1508 | 1 | 1535 | 1 |
| 3 | `Similar to memory.events but the fields in the file are local` | 11 | 1518 | 1 | 1545 | 1 |
| 4 | `Set perms to 0, disable /sys/module/btrfs/parameter/read_policy interface.` | 7 | 1339 | 1 | — | 0 (grep rc 1) |
| 5 | `Set perms to 0, disable /sys/module/btrfs/parameters/read_policy interface.` | 7 | — | 0 (grep rc 1) | 1339 | 1 |
| 6 | `A read-only nested-keyed file.` | 4 | 1912 (also 1996, 2172) | 3 | 2027 | 1 |
| 7 | `A read-write nested-keyed file.` | 4 | 1084, 1216 | 2 | 1084, 1241, 1939, 2203 | 4 |

Quotes 1-3 are the three S138 anchor sentences (cgroup-v2.rst). Quotes 4-5 are the one
S158 changed line, each side found once in its own tag and zero times in the other
(sysfs.c). Quotes 6-7 are the memory.pressure access-mode pair; in v7.3 the memory
heading's line is 1939 (`sed -n '1939p'` prints `A read-write nested-keyed file.`) and in
v7.2 the same anchor line is 1912 (`sed -n '1912p'` prints `A read-only nested-keyed
file.`). The registry status word `rejected` (quote in RW5) is not a pinned-bytes quote;
its command is `sed -n '191p' corpus/SOURCES.md` (rc 0, prints the S185 row) with field 9
of that row read as `rejected`.

Word counts: `printf '%s' "<quote>" | wc -w` per row above; the largest is 11 words, all
under the 25-word gate. No quote in the note appears inside a fence (the note contains no
fence at all: `grep -c '^```\|^~~~' note.md` prints 0, grep rc 1).

## 2. Note shape and the frozen counter

    $ python3 .ufo/waves/round-68/drafts/c1/count-rw-r68.py .ufo/waves/round-68/drafts/c1/note.md
    RW_ROWS=6
    LAYOUT=8
    rc=0

No REJECT line was printed. The table header at note line 28 is
`| id | row-kind | fact | v7.2 anchor | v7.3 anchor | verdict | applicability | evidence |`
and each RW row has exactly 8 pipe-separated data cells
(`awk '/^\| RW[0-9]+ \|/{n=gsub(/\|/,"|"); print n}'` prints 9 pipes per row, i.e. two edge
pipes). The first three lines are the three frontmatter keys at column 0, outside any
fence (`head -3 note.md`, rc 0):

    source: S138, S149, S158, S182, S185, S286, S287 — the pinned upstream files (sha256 in corpus/SOURCES.md rows and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-68/before/src/SHA256SUMS)
    verified-at: 2026-11-03 (fleet round 68, the v7.3 bytes in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-68/before/src/)
    recheck: on-release

## 3. Measurements behind the rows

    $ sha256sum v72-Documentation_admin-guide_cgroup-v2.rst v73-Documentation_admin-guide_cgroup-v2.rst
    a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad  v72-…
    2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68  v73-…
    rc 0

    $ grep -c '^@@' <(diff -u v72-Documentation_admin-guide_cgroup-v2.rst v73-…rst)
    16
    rc 0

    $ sha256sum v72-fs_btrfs_sysfs.c v73-fs_btrfs_sysfs.c
    ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43  v72-…
    098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377  v73-…
    rc 0

    $ grep -c '^@@' <(diff -u v72-fs_btrfs_sysfs.c v73-fs_btrfs_sysfs.c); grep -c '^[-+][^-+]' <(diff -u v72-… v73-…)
    1
    2
    rc 0

    $ cmp -s <(sed -n '37,40p' v72-fs_btrfs_sysfs.c) <(sed -n '37,40p' v73-fs_btrfs_sysfs.c); echo $?
    0
    (the same pair for 68,78 and 672,688 each prints 0)

    $ sha256sum v72-mm_oom_kill.c v73-mm_oom_kill.c
    452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  v72-…
    452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  v73-…
    rc 0

    $ sha256sum v72-Documentation_accounting_psi.rst v73-Documentation_accounting_psi.rst
    11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692  v72-…
    11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692  v73-…
    rc 0

    $ cmp -s v72-mm_oom_kill.c v73-mm_oom_kill.c; echo $?   → 0
    $ cmp -s v72-Documentation_accounting_psi.rst v73-Documentation_accounting_psi.rst; echo $?   → 0
    $ wc -l v72-mm_oom_kill.c v73-mm_oom_kill.c v72-Documentation_accounting_psi.rst v73-Documentation_accounting_psi.rst
    1257 / 1257 / 188 / 188

    $ sed -n '2,3p' .ufo/waves/round-68/before/host.txt
    7.2.11-arch1-1
    linux 7.2.11.arch1-1

S138 headings used in the note: `grep -n '^  memory.events'` prints 1468 and 1517 (v7.2),
1495 and 1544 (v7.3); `grep -n 'oom_kill$'` prints 1506 (v7.2) and 1533 (v7.3). S158
changed line: `sed -n '1339p'` of each tag prints the two comment strings quoted above.
The 16-hunk controller attribution in RW1 is taken from
`.ufo/waves/round-68/drafts/c1/S1Scout-verify.md` (first line `2026-11-03T22:35:41Z`):
CPU 6, Memory 1, IO 3, Cpuset 1, RDMA 3, DMEM 1, Misc 1, with hunk 7
(`@@ -1909,7 +1936,7 @@`) the single memory-section hunk.

## 4. Conflicts recorded verbatim (for the canonical judge)

1. SCORECARD.md line 5119, C1/RW1: "the changed hunks named and shown outside the
   memory-controller section". Measured: 15 of the 16 hunks are outside the memory
   controller section and 1 is inside it — hunk 7 at `@@ -1909,7 +1936,7 @@` changes
   `memory.pressure` from `A read-only nested-keyed file.` to `A read-write nested-keyed
   file.` (v7.3 line 1939), inside the Memory section (v7.3 heading `Memory` at 1294). The
   independent scout receipt records the same: "Touches memory controller: YES" for hunk 7.
   The note states the measured split rather than the declaration's phrasing.
2. SCORECARD.md lines 5110-5111, anchor spot-check: "(memory.events 1468 → 1495; oom_kill
   1507 → 1533; memory.events.local 1517 → 1544)". Measured: the three anchor *sentences*
   are at v7.2 1474, 1508, 1518 and v7.3 1501, 1535, 1545 (uniform +27); the v7.2 sentence
   line 1507 maps to v7.3 1534, while 1533 is the v7.3 `oom_kill` heading line (v7.2 1506
   + 27). The declaration's oom_kill pair mixes the v7.2 sentence line with the v7.3
   heading line. The note cites both heading and sentence lines so no anchor is ambiguous.

## 5. Source defects observed while reading

1. `S1Scout-verify.md` §2 gives the section heading line numbers in v7.2 numbering for the
   post-drift sections (Memory 1267, Memory Interface Files 1290, RDMA 2774, DMEM 2866,
   Misc 2942); the v7.3 headings are 1294, 1317, 2812, 2917, 2999
   (`grep -n '^Memory$'` prints 1294 then 3509 in v7.3 and 1267 then 3452 in v7.2). Its
   hunk count (16), memory-hunk count (1) and controller names agree with this seat's own
   reads, so only the heading line numbers are affected; the note takes the controller
   names from the receipt and its own heading lines from the pinned v7.3 file.
2. `count-rw-r68.py` line 24 emits `SyntaxWarning: "\|" is an invalid escape sequence`
   from its own module docstring on this Python; the counter still prints RW_ROWS and rc 0.
3. The S138 registry anchor cell reads "line 1914 (memory.pressure)"; in v7.2, 1911 is the
   `memory.pressure` heading and 1914 is the pressure-stall sentence, so the anchor line
   names the sentence rather than the heading. The note cites heading lines measured by
   grep and does not restate 1914.

## 6. Limits

- No network fetch by this seat: every byte read is the L1's pinned copy under
  `.ufo/waves/round-68/before/src/`. v7.3 was not installed or built; nothing here is a
  runtime observation.
- The note is a draft for L1 integration; this seat ran no lane gate, no census and no
  registry edit. The counter run in §2 is a shape read, not the canonical judgment.
- Memory evidence and kill/OOM attribution stay with mori (PROVINCE.md OUT-001); the note
  states none.
