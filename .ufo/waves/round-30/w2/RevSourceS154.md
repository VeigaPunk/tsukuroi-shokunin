# RevSourceS154 — wave-2 falsification of SOURCES.md row S154 at 29bf87fa3971df04cb96e4ad9a28805d8154ed2f

Verdict: agree, with one reservation — every reproducibility check passes byte-for-byte, but the
`used-by` cell names `corpus/lessons/round-30.md`, which does not exist at the pinned tip (it is
first committed at `7165f11`, three commits after the tip; at lane HEAD `b0cf50b` it does cite S154).

## Findings

1. Live bytes match anchor digest and committed snapshot [obs]. `curl -sL` of
   `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-sysfs.rst` today
   (2026-10-22) returned HTTP 200 and sha256
   `295b92653a70a0b896b10d5ec04bfa7f7c7221c47a00cdb08e0f4f6645803bc6` (464 lines, 13204 bytes) —
   identical to the digest and size claimed in the anchor cell and to the committed snapshot
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcSysfsDoc/S154-ch-sysfs.rst`
   (`sha256sum` output identical; `git cat-file -e` at the tip confirms the snapshot is committed).
   Fetched bytes kept at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS154/S154-live.rst`.

2. Gate quote is verbatim and within the 25-word cap [obs]. The drafted quote
   `Files and directories in :file:`/sys/fs/btrfs/UUID/allocations` directory are:` from
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcSysfsDoc/S154-gate.md`
   is a verbatim substring of line 143 of both the committed snapshot and today's live bytes:
   `sed -n '143p' <file> | grep -cF '<quote>'` prints 1 for each. `wc -w` on the quoted string = 7
   words, ≤ 25. The lesson gate table at (worktree) `corpus/lessons/round-30.md:13` carries the same
   row with URL, access date 2026-10-22, quote and location, satisfying contract rule 1.

3. Row shape conforms to contract v1 [obs]. The row at `corpus/SOURCES.md:160` parses to NF=13 under
   `awk -F'|'`, i.e. 11 cells, matching the header `| id | source | kind | tier | scope | anchor |
   teaches | status | opened | recheck | used-by |`. `status` = `mined`, `opened` = `2026-10-22`
   (ISO date), `recheck` = `on-release` — all in the contract's vocabulary; `mined` semantics
   (cited by ≥1 used-by path) are satisfied. The row at the pinned tip is byte-identical to the
   working-tree row (`grep S154 | sha256sum` both `16f6a1e7…`).

4. Admit cells are accurate [obs]. `kind` = `docs` fits a Documentation/*.rst chapter; `tier` = `A`
   fits "official docs, authoritative for that scope". `scope` is accurate against the file: the
   chapter documents `/sys/fs/btrfs/UUID/allocation` (layout table lines 8–18), the top-level
   `bg_reclaim_threshold` (lines 38–42), the `UUID/allocations` section with `global_rsv_reserved`,
   `global_rsv_size` and the `data/`, `metadata/`, `system/` directories (lines 140–158), and the
   per-type files list (lines 163–254) — all twelve names in the anchor (`chunk_size`, `disk_total`,
   `disk_used`, `dynamic_reclaim`, `flags`, `force_chunk_alloc`, `periodic_reclaim`, `reclaim_bytes`,
   `reclaim_count`, `reclaim_errors`, `size_classes`, `total_bytes`) appear verbatim in lines
   182–254 of the snapshot. `teaches` matches this content. The scope's "installed btrfs-progs 7.1"
   is true on this host: `btrfs --version` prints `btrfs-progs v7.1`. The gate row honestly notes
   upstream's own `allocations` (section heading, line 140/143) vs `allocation` (layout table, line
   10) inconsistency.

5. `used-by` defect at the pinned tip [obs]. The cell lists
   `corpus/knowledge/btrfs-space-r30.json` (cites `"source": "S154"` twice at the tip blob, plus two
   snapshot-path references — 4 matches), `corpus/knowledge/btrfs-space-r30.md` (2 matches,
   e.g. line 30 `(S154 line 168)`), `SKILL.md` (3 matches, rows R30-D05/D06/D08), and
   `corpus/lessons/round-30.md`. `git cat-file -e 29bf87f:corpus/lessons/round-30.md` exits 128
   ("exists on disk, but not in '29bf87f'") and `git ls-tree` of `corpus/lessons/` at the tip omits
   it; `git log --follow` shows the file first committed at `7165f11` and modified at `b0cf50b`
   (lane HEAD, three commits past the pushed tip). At the revision under attack the cell therefore
   names one file that does not exist. Impact is low: `mined` is independently supported by the
   three real citers, and at lane HEAD `corpus/lessons/round-30.md` exists and cites S154 four
   times, so the claim is true for the branch — it was simply asserted one commit-generation early.

## Residual risk and gaps

- The `allocations`/`allocation` spelling mismatch is upstream's own inconsistency, disclosed in
  the gate note and SKILL row R30-D06; not a row defect [obs].
- The lesson file's late arrival is an append-order wrinkle, not content fraud — the gate row it
  carries is consistent with the seat draft [inf].
- Whether a forward-referencing `used-by` path violates contract v1 rule 2 (rows written "only
  after opening the source") is a judgment call for the L1; the contract's census check tests
  working-tree existence, which now passes [unk].

Scope: read=corpus/SOURCES.md row 160, CORPUS.md contract section, S154 gate draft, S154 snapshot
(464 lines), lane git objects at 29bf87f/7165f11/b0cf50b; wrote=.ufo/waves/round-30/w2/RevSourceS154.md,
.ufo/waves/round-30/w2/RevSourceS154/S154-live.rst; executed=curl, sha256sum, sed, grep, awk, wc,
read-only git (show/ls-tree/cat-file/ls-files/status/log/rev-parse/merge-base), btrfs --version
Model: devin/swe-2
Installs: none
