# RevSourceS159 — wave-2 re-open review of SOURCES.md row S159

Verdict: partly holds. The row's identity, digest, quote, shape, enums, tier, kind, scope and
teaches are all accurate, but at the audited revision 29bf87fa3971df04cb96e4ad9a28805d8154ed2f
the used-by cell names `corpus/lessons/round-30.md`, which does not exist at that revision
(the contract's mined-used-by census would print `missing:` for it). The file was committed
two commits later and exists at lane HEAD 857126711c9a5dd5e62f5f0ad2bf403f479fa4f0, so the
defect is healed on the current tip but real at the attacked revision.

## Findings

1. [obs] Live bytes match the anchor digest and the committed snapshot exactly.
   `curl -sL https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/btrfs/space-info.c?h=v7.2`
   returned HTTP 200, 73832 bytes, 2267 lines, sha256
   `5654929f065b05cc07bb5fc9e0bdb6e774d44702cef5d7701ae64d4177da5ce1` — identical to the sha256
   in the row's anchor cell (corpus/SOURCES.md line 165) and to the committed blob
   `29bf87f:.ufo/waves/round-30/w1/ScribeSrcSpaceInfo/S159-space-info.c` (git show | sha256sum
   gives the same digest). `cmp -s` confirms live bytes are byte-identical to the snapshot.
   Fetched copy saved at `.ufo/waves/round-30/w2/RevSourceS159/S159-space-info-live.c`.

2. [obs] Gate quote is verbatim on the cited line and within the limit. The seat gate file
   `.ufo/waves/round-30/w1/ScribeSrcSpaceInfo/S159-gate.md` quotes
   "is no unallocated space to be had, all reservations are kept within the" citing line 177.
   `sed -n '177p' <snapshot> | grep -cF 'is no unallocated space to be had, all reservations
   are kept within the'` prints 1. The quote is 13 whitespace-separated words (≤ 25). The
   gate's note that the sentence continues on line 178 is also accurate
   ("free space in the allocated metadata chunks." is line 178).

3. [obs] Row shape and enums conform to CORPUS.md contract v1. Line 165 has NF=13 under
   `awk -F'|'`, i.e. 11 cells; id S159 fits `S` + 3 digits; kind `code`, tier `A`, status
   `mined` are all in the permitted enums; `opened` = 2026-10-22 is a valid ISO date matching
   today's re-open date; `recheck` = `on-release` is a listed cadence form. No `|` inside
   cells.

4. [obs] Anchor line ranges resolve to the claimed content in the live file:
   20-183 is the "HOW DOES SPACE RESERVATION WORK" model comment (verified at lines 20-30 and
   its tail at 176-183); 176-178 is the unallocated-space overcommit limit; 452-521 spans
   `calc_available_free_space` (definition at 452, `return avail` at 521); 845-958 spans the
   `flush_space` comment + function (comment at 845-850, ALLOC_CHUNK branch at 901-902,
   `trace_btrfs_flush_space` at 957); 1132-1180 covers `maybe_fail_all_tickets` (comment from
   1132, function at 1143, `btrfs_try_granting_tickets` call at 1179); 1935-1952 is
   `btrfs_reserve_metadata_bytes` with the `space_info:enospc` trace at ~1946; 2055-2063 is
   the "reasonable buffer for unallocated space is 10 data block_groups" reclaim comment
   feeding `calc_unalloc_target` at 2061. [inf] All anchor claims are accurate.

5. [obs] teaches cell is grounded in the source: reservations accounted in
   `space_info->bytes_may_use` and moving to `bytes_reserved`/`bytes_used` (comment lines
   39-64); tickets served in order by the flush sequence (`The reservation code handles
   tickets in order`, ~line 1134); `-ENOSPC` returned only when flushing makes no progress and
   the global reserve cannot be stolen (`steal_from_global_rsv` at 1096, called at 1164 inside
   the ticket grant loop); overcommit confined to unallocated space (lines 176-178). [inf]
   Teaches is accurate and matches the declared scope (metadata reservation, ordered flush
   states, ENOSPC at the ticket layer, free_chunk_space role in chunk allocation).

6. [obs] kind `code` and tier `A` are correct: this is upstream kernel C source pinned to tag
   v7.2 — primary source code for the stated scope, satisfying the tier-A definition
   ("source code" is explicitly tier A in the contract).

7. [obs] used-by defect at the audited revision: the cell lists
   `corpus/knowledge/btrfs-space-r30.json, corpus/knowledge/btrfs-space-r30.md, SKILL.md,
   corpus/lessons/round-30.md`. In a pristine clone at
   29bf87fa3971df04cb96e4ad9a28805d8154ed2f, the first three exist and each cites S159
   (json: `"source": "S159"` at lines 16 and 117; md: source line 1 plus citations at lines
   18 and 27; SKILL.md: registry line 2606 `| S159 line 177 |`). But
   `corpus/lessons/round-30.md` is absent at 29bf87f — `git cat-file -e
   29bf87f:corpus/lessons/round-30.md` fails ("exists on disk, but not in 29bf87f..."). It
   was committed in 7165f11 ("round-30: adjacency padding-shape repair ... lesson draft"),
   reachable from lane HEAD 8571267. At lane HEAD the file does cite S159 (3 matches). So
   at the attacked revision the frozen contract's mined-used-by census
   (`awk … status=="mined" → check [ -e path ]`) would emit
   `missing: corpus/lessons/round-30.md` — a real dangling-path violation at that commit,
   resolved by HEAD. [inf] The row was landed naming a still-uncommitted lesson draft;
   severity is low because the file was committed promptly and the other three used-by paths
   were all valid, keeping `mined` status honest.

8. [unk] Whether the used-by cell's inclusion of a not-yet-committed path was deliberate
   forward reference or a sequencing slip cannot be determined from the artifacts; the
   observable state at 29bf87f is the defect described above.

Residual risk: none on content — every substantive cell re-verified against live upstream
bytes fetched today at the row's own URL (the kernel.org cgit fallback named in the anchor;
raw.githubusercontent.com was not needed since git.kernel.org answered HTTP 200).
Verification gap: `opened` 2026-10-22 asserts the row author opened the source today; the
gate file and snapshot are consistent with that and the live re-open reproduces the bytes,
so only the author's clock is unverifiable.

Scope: read=corpus/SOURCES.md L165 + CORPUS.md contract §SOURCES, S159 gate/row/snapshot
files, used-by citers at 29bf87f, live cgit bytes; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS159.md
and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS159/S159-space-info-live.c;
executed=git clone --no-local to /fast/scratch/hyaku/tsukuroi-r30/RevSourceS159/repo (checkout
29bf87f, all GIT_* unset), read-only git log/show/cat-file/ls-files/rev-parse on the lane,
curl, sha256sum, sed/grep/awk/cmp/wc.
Model: not exposed
Installs: none
