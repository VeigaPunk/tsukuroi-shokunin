# RevSourceS161 — wave-2 falsification review of SOURCES.md row S161 (REJECT)

Verdict: **agree with the rejection.** Every factual premise in the row's REJECTED cell is true on the live page, the digest and quote checks pass, and admitting the source would have added nothing the tier-A rows lack.

## Integrity checks (all pass)

1. Live bytes re-fetched today 2026-10-22 by plain `curl -sL https://wiki.archlinux.org/title/Btrfs` → HTTP 200, 192669 bytes, sha256 `73558a5cef7854cb4130ba88fbcacc10a228c502aed294f0b52bd2ed075d5523`. This equals (a) the anchor cell digest and (b) the committed snapshot `.ufo/waves/round-30/w1/ScribeSrcArchWiki/S161-archwiki-btrfs.html` (verified in the pinned tree `29bf87fa`, same sha256, 192669 bytes). The live page is still `wgCurRevisionId":887521`, "last edited on 11 October 2026, at 22:41", matching the pinned oldid — zero drift since the row was written. [obs]
   Fetched bytes saved at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS161/S161-live.html`.

2. Gate quote: `sed -n '1846p' S161-live.html | grep -cF 'will inaccurately report free space on a Btrfs partition as they do not account for both file and metadata usage'` → 1. Word count 20 ≤ 25. The Gate row draft at `.ufo/waves/round-30/w1/ScribeSrcArchWiki/S161-gate.md` is verbatim and correctly located. [obs]

3. Row shape: NF=13 under `awk -F'|'`, i.e. exactly 11 cells. `status` = `rejected` (in the v1 enum), `opened` = ISO `2026-10-22`, `recheck` = `180d` (a permitted cadence). `kind` = `docs`, `tier` = `B` — correct for an expert community write-up; `community` is not involved, no tier inflation. [obs]

## Attacking the rejection reason — every premise verified

4. Line 1846 (the drafted quote) is the df-versus-usage point already in btrfs-filesystem(8): S152 snapshot lines 22-23 ("not suitable for quick overview") and 366-368 ("supposed to replace the `btrfs filesystem df` command in the long run") — both confirmed verbatim at `.ufo/waves/round-30/w1/ScribeSrcFsUsage/S152-btrfs-filesystem.rst`. The row cites S152:367-368 for the second; the phrase spans 367-368. [obs]

5. Lines 1892-1898 restate the usage-filter and ENOSPC work-space story of btrfs-balance(8): S153 snapshot confirms "it usually needs ... work space, otherwise it fails for ENOSPC" at lines 97-100, "`usage=0` ... will reclaim the space" at 118-120, and the usage-filter examples at 154-183 — matching the row's cited ranges. [obs]

6. Frozen tokens: `unallocated` = 0, `global reserve` = 0, `reclaim` = 0 occurrences on the live bytes (case-insensitive). True. [obs]

7. Lines 2174-2182 (Troubleshooting > No space left on device) re-host an external blog list (line 2175: "suggests and explains the following checks/steps") plus a pointer to Forza's Ramblings at 2182 — the page states no mechanism of its own. Confirmed. [obs]

8. Would admitting it add anything tier-A lacks? The two candidate uniques the row itself names do not survive: (a) line 1850's RAID5/6+DUP inaccuracy note cites btrfs-man5 and is irrelevant to this corpus — no host filesystem uses RAID5/6, and S152 already covers the mixed-profile caveat on `Free (estimated)`; (b) line 2181's temporary-device remedy is the operational consequence already implied by the S153:97-100 work-space explanation the corpus holds. No D01-D10 row needs either remark; every D-row is grounded on tier-A sources (S152-S159). Rejecting costs nothing. [inf]

9. Flip condition soundness: "admit as tier-B mined when a knowledge statement needs an Arch-specific operational remark that the btrfs-progs v7.1 docs do not state — ... cited at a dated oldid and approved by the L1" is a sound, need-keyed gate — it names concrete candidate content (lines 1850, 2181), requires pinning against the mutable address, and routes through L1 approval. Better than blanket admission or blanket ban. [inf]

## Residual nits (do not change the verdict)

10. `teaches` cell reads "REJECTED for this round: ... Flip: ..." rather than the contract's literal template "REJECTED: <reason>; flip: <what would change the verdict>" (CORPUS.md:102). S160 uses the identical convention, so it is a round-wide style, not a lone defect; semantics preserved. [obs]

11. At the pinned commit `29bf87fa` the `used-by` cell lists `corpus/lessons/round-30.md`, which did not exist in that commit (committed later at 7165f11/b0cf50b). Both listed files do cite S161 today (`btrfs-space-r30.md:1,44`; `round-30.md:20,24`). The v1 census existence check covers only `mined` rows, so nothing fails; flagging as a forward-dated-path nit only. [obs]

12. Minor citation slippage: the row cites "S152:22-23" for the "not suitable for quick overview" line; the phrase sits at line 23 of the snapshot (line 20 is the `df` synopsis). The teaches claim omits D08-D10 from its coverage accounting; those are point-in-time host captures on S154/S152/S158 — also unhelped by S161. [obs]

Scope: read=SOURCES.md@29bf87fa row 167 + S152/S153/S160 rows, CORPUS.md contract v1 §SOURCES.md, S161 gate/row drafts and snapshot, btrfs-space-r30.json rows D01-D10, btrfs-space-r30.md, round-30.md lesson, live ArchWiki Btrfs page; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS161.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS161/S161-live.html; executed=curl fetch, sha256sum, sed/grep -cF verification, read-only git show/log/ls-tree/status in the lane
Model: not exposed
Installs: none
