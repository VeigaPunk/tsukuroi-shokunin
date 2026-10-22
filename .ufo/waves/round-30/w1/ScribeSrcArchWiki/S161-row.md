# S161 draft registry row (unlanded; decision: rejected)

Reserved id S161, tier-B candidate. Row shape follows `corpus/SOURCES.md` rows S148-S151. Anchor
cell carries `sha256 <hex>`; `opened` is 2026-10-22.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S161 | ArchWiki Btrfs — https://wiki.archlinux.org/title/Btrfs | docs | B | The page's space-operability text only: Usage > Displaying used/free space (df and du inaccuracy, the `btrfs filesystem usage` remedy), the Usage > Balance subsection on reducing allocated-but-unused chunks, and Troubleshooting > No space left on device; not a mechanism source for the global reserve, unallocated space or automatic block-group reclaim | § Displaying used/free space lines 1845-1856 (quote at 1846, mixed-profile note at 1850); § Balance h4 under Usage lines 1892-1898; § No space left on device lines 2174-2182; revision oldid 887521, last edited 2026-10-11T22:41, plain curl HTTP 200 2026-10-22, 192669 bytes, sha256 73558a5cef7854cb4130ba88fbcacc10a228c502aed294f0b52bd2ed075d5523; snapshot .ufo/waves/round-30/w1/ScribeSrcArchWiki/S161-archwiki-btrfs.html | REJECTED for this round: it restates tier-A guidance instead of adding a mechanism, since line 1846 repeats the df-versus-usage point of btrfs-filesystem(8) (S152:22-23 and 367-368) and lines 1892-1898 repeat the usage-filter and ENOSPC work-space explanation of btrfs-balance(8) (S153:97-100, 118, 154-183), while the frozen tokens unallocated, global reserve and reclaim occur zero times on the page, so it can answer none of D01, D02 or D05 and is redundant for D03, D04, D06 and D07. Flip: admit as tier-B mined when a knowledge statement needs an Arch-specific operational remark that the btrfs-progs v7.1 docs do not state — the mixed RAID5/6 plus DUP-profile inaccuracy note at line 1850 or the temporary-device remedy at line 2181 — cited at a dated oldid and approved by the L1 | rejected | 2026-10-22 | 180d | — |

Notes for integration:

- Draft only; the L1 owns landing and the final `used-by` cell. No file under the lane tree was edited.
- Because the status is `rejected`, no `S161-rows.json` is drafted: C1 rule R4 admits only a source
  row whose status cell is exactly `mined`, so a D01-D07 candidate row built on S161 would fail R4
  by construction.
- The saved bytes are the live page at revision 887521 (`wgCurRevisionId":887521`, "This page was
  last edited on 11 October 2026, at 22:41."); the address is mutable, so the row pins the oldid and
  the access date rather than the bare URL.
