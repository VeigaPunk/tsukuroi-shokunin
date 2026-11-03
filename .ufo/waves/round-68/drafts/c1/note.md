source: S138, S149, S158, S182, S185, S286, S287 — the pinned upstream files (sha256 in corpus/SOURCES.md rows and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-68/before/src/SHA256SUMS)
verified-at: 2026-11-03 (fleet round 68, the v7.3 bytes in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-68/before/src/)
recheck: on-release

# Linux v7.3 pinwatch — the five v7.2-pinned rows re-read (round 68)

## Scope

QUALITY 98 watch: the upstream tag Linux v7.3 appeared after the host's 7.2.11 was
pinned, so the five registry rows that pin v7.2 bytes were re-read against the v7.3
bytes of the same four files. The note is a reading of text, not a runtime study: it
records, per row, whether the file changed, whether the registered anchor text survived,
and whether the row's host statement still holds on the installed 7.2.11. Two v7.3
reference rows are opened with this note — S286 for Documentation/admin-guide/cgroup-v2.rst
at v7.3 and S287 for fs/btrfs/sysfs.c at v7.3 — so a later re-read cites v7.3 bytes
directly instead of this note. The five existing rows are not edited in place.

Method and provenance. The eight files are the L1's pre-declaration fetches, saved under
`.ufo/waves/round-68/before/src/` (URLs in `FETCH.txt`, digests in `SHA256SUMS`); this
seat read those saved bytes and fetched nothing. Every verdict below is a pair of reads
of the same file at the two tags. Host state comes only from `before/host.txt`.

The registry rows are readings of upstream text. Nothing in this note asserts that this
host generated a memory.events value, saw pressure, or killed a process.

## Rows

| id | row-kind | fact | v7.2 anchor | v7.3 anchor | verdict | applicability | evidence |
|---|---|---|---|---|---|---|---|
| RW1 | registry-row S138 | Documentation/admin-guide/cgroup-v2.rst changed: sha256 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad at v7.2, 2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68 at v7.3; the three registered anchor sentences — `Note that all fields in this file are hierarchical`, `killed by any kind of OOM killer.` and `Similar to memory.events but the fields in the file are local` — are byte-identical at v7.3 lines 1501, 1535 and 1545 (grep -cF prints 1 in each tag), and the v7.3 bytes are the round's S286 reference row; the diff is 16 hunks, attributed by the independent scout receipt drafts/c1/S1Scout-verify.md (its own re-fetch, all four sha256 MATCH) as CPU 6, Memory 1, IO 3, Cpuset 1, RDMA 3, DMEM 1 and Misc 1, and the single Memory hunk is the memory.pressure access-mode line, so 15 hunks sit outside the memory controller section and 1 sits inside it | sentence lines 1474, 1508 and 1518, heading lines 1468, 1506 and 1517 (grep -nF of each sentence, grep -n '^  memory.events' and grep -n 'oom_kill$' on the v7.2 file) | sentence lines 1501, 1535 and 1545, heading lines 1495, 1533 and 1544 (grep -nF of each sentence, grep -n '^  memory.events' and grep -n 'oom_kill$' on the v7.3 file) | CHANGED for the file; the three anchor sentences UNCHANGED; one hunk changes memory.pressure from read-only to read-write inside the memory controller section | the v7.2 bytes and their anchors remain the host-correct reading at 7.2.11 (RW6); the 16 hunks are v7.3 text, not host state | sha256sum of the two files prints a9433bb0… and 2750c11a… (rc 0); grep -c '^@@' <(diff -u v72-Documentation_admin-guide_cgroup-v2.rst v73-Documentation_admin-guide_cgroup-v2.rst) prints 16 (rc 0); grep -cF of each of the three sentences prints 1 in each tag; sed -n '1939p' of the v7.3 file prints `A read-write nested-keyed file.` where v7.2 line 1912 prints `A read-only nested-keyed file.` (grep -cF prints 3 and 2 in v7.2, 1 and 4 in v7.3) |
| RW2 | registry-row S158 | fs/btrfs/sysfs.c changed: sha256 ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43 at v7.2, 098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377 at v7.3, and the v7.3 bytes are the round's S287 reference row; the diff is exactly 1 hunk and it is comment-only at v7.3 line 1339, where v7.2 reads `Set perms to 0, disable /sys/module/btrfs/parameter/read_policy interface.` and v7.3 reads `Set perms to 0, disable /sys/module/btrfs/parameters/read_policy interface.`; the registered anchor ranges 37-40, 68-78 and 672-688 MATCH | lines 37-40, 68-78 and 672-688, changed line 1339 (sed -n '37,40p', '68,78p', '672,688p' and '1339p' on the v7.2 file) | the same three ranges and the same line 1339 (cmp -s on each extracted range prints rc 0) | CHANGED for the file, comment only; the registered ranges MATCH byte for byte | the allocation sysfs surface the S158 reading describes is untouched by the single comment line, so the v7.2 reading stays host-correct at 7.2.11 | sha256sum of the two files prints ce146120… and 098cb522… (rc 0); grep -c '^@@' <(diff -u v72-fs_btrfs_sysfs.c v73-fs_btrfs_sysfs.c) prints 1 and grep -c '^[-+][^-+]' on the same diff prints 2 (rc 0); cmp -s of the three extracted ranges prints rc 0 three times; grep -cF of each side of line 1339 prints 1 in its own tag and 0 in the other |
| RW3 | registry-row S149 | mm/oom_kill.c is byte-identical at both tags: sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e twice, 1257 lines each, so every registered anchor line resolves to the same bytes at v7.3 | lines 199, 216, 228, 233, 263, 306, 340, 348, 362, 367, 372, 710 and 1145 (sed -n with those 13 addresses on the v7.2 file) | the same 13 line numbers, byte-identical (cmp -s on the whole file prints rc 0) | UNCHANGED | the oom_badness and victim-selection reading stays host-correct at 7.2.11; no kill attribution is drawn from it (see Boundary) | sha256sum of both files prints 452f1348… on both lines (rc 0); cmp -s v72-mm_oom_kill.c v73-mm_oom_kill.c prints rc 0; wc -l prints 1257 and 1257; sed -n '199p;216p;228p;233p;263p;306p;340p;348p;362p;367p;372p;710p;1145p' prints the same 13 lines on each tag |
| RW4 | registry-row S182 | mm/oom_kill.c is the same file as S149: sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e twice, 1257 lines each, so the registered lines 935-936, 945-951 and 1168-1170 resolve identically at both tags | lines 935-936, 945-951 and 1168-1170 (sed -n '935,936p;945,951p;1168,1170p' on the v7.2 file) | the same line numbers, byte-identical (cmp -s on the whole file prints rc 0) | UNCHANGED | the system-wide versus memory-cgroup kill-log label reading stays host-correct at 7.2.11; no OOM attribution is made here | sha256sum of both files prints 452f1348… twice (rc 0); cmp -s v72-mm_oom_kill.c v73-mm_oom_kill.c prints rc 0; wc -l prints 1257 and 1257; sed -n '935,936p;945,951p;1168,1170p' prints the same lines on each tag |
| RW5 | registry-row S185 | Documentation/accounting/psi.rst is byte-identical at both tags: sha256 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692 twice, 188 lines each, so the registered lines 45-49 resolve to the same bytes; the registry row remains rejected, its status cell reading `rejected` verbatim | lines 45-49 (sed -n '45,49p' on the v7.2 file) | the same lines, byte-identical (cmp -s on the whole file prints rc 0) | UNCHANGED; row status rejected | a rejected row adds no authority, so no host statement or ownership-boundary claim is derived from it | sha256sum of both files prints 11c6b712… twice (rc 0); cmp -s prints rc 0; wc -l prints 188 and 188; sed -n '191p' corpus/SOURCES.md prints the S185 registry row whose status cell reads rejected |
| RW6 | host applicability | the installed kernel is 7.2.11, so the five rows that pin v7.2 bytes remain host-correct readings and no v7.3 text applies to this host | host kernel 7.2.11 (sed -n '2,3p' before/host.txt prints 7.2.11-arch1-1 and linux 7.2.11.arch1-1) | not installed (the same host record names no v7.3 kernel) | APPLICABLE to 7.2.11 | falsifier: installed kernel >= 7.3 re-opens RW1-RW2 for host statements | sed -n '2,3p' .ufo/waves/round-68/before/host.txt prints 7.2.11-arch1-1 then linux 7.2.11.arch1-1 (rc 0); the same file records pacman -Qu rc=1, so no pending kernel upgrade was visible at capture |

## Boundary

`memory.events` and cgroup memory evidence belong to mori: `PROVINCE.md` OUT-001 owns
kill/OOM and cgroup memory evidence, cited here by anchor id and not by line number. This
note states no kill or OOM attribution and performs no fleet pressure correlation. The
registry rows it cites are readings of upstream text, not reports of host state; nothing
above asserts that this host produced a `memory.events` change, an `oom_kill` increment or
a kill record.

## Limits

- No v7.3 code was run: no 7.3 kernel is installed (RW6, before/host.txt) and neither tag
  was built, so no runtime behaviour of either tag is observed here.
- All bytes are the L1's pre-declaration pinned copies under
  `.ufo/waves/round-68/before/src/` (eight URLs in FETCH.txt); this seat fetched nothing,
  so the note carries no claim about bytes outside those eight files.
- No claim about upstream behaviour beyond the quoted text. The 16-hunk controller
  attribution in RW1 is taken from the independent scout receipt
  `.ufo/waves/round-68/drafts/c1/S1Scout-verify.md` (2026-11-03T22:35:41Z, its own
  re-fetch with all four sha256 MATCH); this seat separately reproduced the 16-hunk
  count, the 1 memory-section hunk and the three anchor lines from the pinned bytes.
  The scout receipt's heading line numbers are v7.2 numbering for the post-drift
  sections (grep -n '^Memory$' prints 1294 then 3509 in v7.3 and 1267 then 3452 in
  v7.2), so this note takes only the controller names from it and its own heading
  lines from the v7.3 file.
- The memory.pressure access-mode change is documentation text only; the note does not
  claim that the v7.3 kernel behaves differently at runtime from v7.2.
- S286 and S287 are opened as the v7.3 reference rows behind RW1 and RW2; their registry
  cells are landed by the L1, and this note asserts no registry state for them.
- The five existing rows (S138, S149, S158, S182, S185) are not edited in place; every
  verdict above is an appended reading.
