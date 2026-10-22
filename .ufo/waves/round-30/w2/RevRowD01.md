# RevRowD01 — round 30 wave 2 falsification of C1 row D01

Verdict: **holds**. Row D01 (JSON, SKILL.md `[R30-D01]` line, `.md` paragraph) is byte-faithful
to a verified source, true to kernel v7.2 behaviour, operator-safe, and new to the lane.
No wording change required; two optional tightenings noted in findings 6 and 7.

## Findings

1. **Snapshot identity holds.** [obs] Fresh `curl -sL` of
   `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/btrfs/space-info.c?h=v7.2`
   returned HTTP 200; sha256 `5654929f065b05cc07bb5fc9e0bdb6e774d44702cef5d7701ae64d4177da5ce1`,
   2267 lines / 73832 bytes — byte-identical to the committed snapshot
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcSpaceInfo/S159-space-info.c`
   (same sha256, `sha256sum` on both) and to the sha256/line/byte counts declared in the S159 row
   of `corpus/SOURCES.md:165`. Fetched bytes saved at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevRowD01/S159-space-info.c`.

2. **Quote is verbatim at the cited line.** [obs]
   `sed -n '177p' <fetched> | grep -cF 'is no unallocated space to be had, all reservations are kept within the'`
   printed `1`; line 177 of both fetched and snapshot copies is that exact text. 10 words, inside
   the 25-word cap. The paragraph (fetched lines 169-178) reads "If there is no unallocated space
   to be had, all reservations are kept within the / free space in the allocated metadata chunks",
   inside the OVERCOMMIT block that explicitly scopes to metadata ("This only happens with
   metadata, data does not allow overcommitting", lines 170-172).

3. **Statement is true to source and behaviour.** [obs/inf] JSON statement
   (`corpus/knowledge/btrfs-space-r30.json`, `"id": "D01"`) says the kernel "keeps every metadata
   reservation inside the free space of already allocated metadata chunks" when no unallocated
   device space remains — faithful restatement of lines 176-178. The consequence "metadata ENOSPC
   can occur while data block groups still show free space" is correct kernel behaviour: data and
   metadata live in separate `btrfs_space_info` pools, free space inside data chunks cannot serve a
   metadata reservation (`.md` line 16 states the same), and with zero unallocated space
   `btrfs_chunk_alloc` cannot add a metadata chunk, so the ticket path fails through
   `btrfs_reserve_metadata_bytes` returning `-ENOSPC` (fetched lines 1935-1952, `ret == -ENOSPC`
   trace at 1943-1947) after `maybe_fail_all_tickets` (lines 1132-1180). These ranges are all inside
   S159's declared anchor list, so nothing in the statement relies on uncited source text.

4. **SKILL.md `[R30-D01]` line is supported and accurate.** [obs] The line at `SKILL.md:2606`
   reads "metadata reservations stay inside the allocated metadata chunks, so ENOSPC can come while
   data chunks have room" — supported per finding 3. `Device unallocated` is the real field name:
   live `btrfs filesystem usage -b /` on this host printed `Device unallocated: 690922455040`
   (exit 0), matching the capture's 690922455040. `df` (statfs) indeed shows free space while this
   failure lurks, since statfs reports pool-free totals, so "read `Device unallocated` before `df`"
   is sound ordering. The hedged "can come" is correct — full metadata plus near-0 unallocated is
   the enabling condition, not a guarantee.

5. **Operator decision is safe.** [obs] The row's decision column prescribes only reads
   (`btrfs filesystem usage -b`, `df`); the JSON advice "read Device unallocated before anything
   else" performs no write. `.md` line 27 routes remediation to the operator ("Operator: free data
   chunks with a usage-filtered balance"), consistent with the section header "Every repair below
   is an operator write; the lane runs none of them". Nothing instructs the lane to write.

6. **Minor (non-blocking): the prioritisation is guidance, not a sourced fact.** [obs]
   "read Device unallocated before anything else" and SKILL's "before `df`" are operational advice
   that no cited line states literally; they are consistent with the mechanism and harmless. If
   maximal citation strictness is wanted, SKILL's `S159 line 177` could widen to `S159 lines
   176-178` (the full sentence) — the checker only requires the source name, so this is optional.

7. **Minor (non-blocking): edge cases exist but the hedge covers them.** [inf] ENOSPC can also
   arise with unallocated > 0 during in-flight flushes, and the kernel tries to hold a ~10 data
   block-group reclaim buffer (`calc_unalloc_target`, fetched lines 2055-2063); neither contradicts
   the row, which describes the enabling condition ("can occur", "near 0 ... is the case"), not an
   exhaustive classifier.

8. **New knowledge for the lane.** [obs]
   `git grep -in 'unallocated' fbfec6bd -- SKILL.md corpus/` → no hits (exit 0, empty);
   `git grep -in 'global reserve' fbfec6bd -- SKILL.md corpus/` → no hits;
   `git show fbfec6bd:SKILL.md | grep -c 'unallocated\|Device unallocated\|ENOSPC'` → `0`.
   The only base `SOURCES.md` ENOSPC hit is mkdir(2) errno semantics (line 41, unrelated
   mechanism). Round-26 SH rows cover scrub/device-error counters and the allocation directory
   name, not the unallocated-space gating of metadata chunk allocation. This matches the counter's
   own declared baseline in `tools/check-btrfs-space-r30.py` (docstring: 0 hits at `fbfec6bd`).

Residual risk: none found in scope. The statement, quote, snapshot, SKILL line, safety, and
novelty all check out against re-fetched upstream bytes at tag v7.2.

Scope: read=corpus/knowledge/btrfs-space-r30.{json,md}, SKILL.md R30 table, corpus/SOURCES.md S159 row, tools/check-btrfs-space-r30.py docstring, snapshot S159-space-info.c, git trees at fbfec6bd (read-only); wrote=.ufo/waves/round-30/w2/RevRowD01.md, .ufo/waves/round-30/w2/RevRowD01/S159-space-info.c; executed=curl (1 fetch, HTTP 200), sha256sum, sed/grep reads, btrfs filesystem usage -b / (read-only, exit 0), git grep/show/ls-tree (read-only)
Model: not exposed
Installs: none
