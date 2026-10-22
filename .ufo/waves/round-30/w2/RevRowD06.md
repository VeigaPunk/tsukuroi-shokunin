# RevRowD06 — attack on C1 row D06 at 29bf87fa3971df04cb96e4ad9a28805d8154ed2f

Verdict: partly holds. Row D06 is true to the source, byte-exact against a fresh fetch, and its operator advice is safe; it partly fails as pure new depth (the allocation directory itself was already lane knowledge, which the entry itself discloses) and its SKILL citation line is imprecise on two points.

## Findings

1. [obs] Snapshot integrity confirmed. `curl -sL https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c` (HTTP fetch, no fallback needed) gives sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`, 2702 lines — identical to committed snapshot `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcKSysfs/S158-sysfs.c` and to the digest declared in `corpus/SOURCES.md:164` (S158). Fetched bytes saved at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevRowD06/S158-sysfs.c`. JSON row and SKILL line at attack revision 29bf87f verified in a sandbox clone (identical to tip 7165f11).

2. [obs] Quote and line are exact. Snapshot line 1068 is `\tBTRFS_ATTR_PTR(allocation, global_rsv_size),` — quote verbatim, contains the frozen token `allocation` (counter rule R7, `tools/check-btrfs-space-r30.py` ROWS['D06']). Exactly one `| [R30-D06] ` line exists in SKILL.md (line 2611).

3. [obs] Statement true to source and to kernel/btrfs-progs behaviour on the host (7.2.11-arch1-1, btrfs-progs v7.1):
   - singular `allocation`: snapshot line 37 (`allocation_attrs  /sys/fs/btrfs/<uuid>/allocation`) and line 2338 (`kobject_create_and_add("allocation", fsid_kobj)`);
   - attribute list: lines 1066-1069 hold only `global_rsv_reserved` and `global_rsv_size` (`sysfs_create_files` at line 2345);
   - data/metadata/system directories: `alloc_name` returns those names (lines 1912-1926) and `btrfs_sysfs_add_space_info_type` creates them under `space_info_kobj` (lines 1936-1950);
   - world-readable: `BTRFS_ATTR` macro mode 0444 (lines 75-77);
   - host confirms: `ls -l /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/allocation/` shows `-r--r--r--` `global_rsv_reserved`, `global_rsv_size` and `data/ metadata/ system/` dirs; `cat` of both files as this unprivileged seat user returned 536870912/536870912 — "readable without root" holds on the host, not just in code.

4. [obs] Doc-mismatch claim true: S154 snapshot `.ufo/waves/round-30/w1/ScribeSrcSysfsDoc/S154-ch-sysfs.rst:140` heading is `UUID/allocations` (plural) vs kernel singular `allocation`.

5. [obs, minor defect — citation imprecision] The SKILL line cites `S154 line 143` for "the v7.1 chapter heading spells `allocations`", but the heading is line 140; line 143 is the body line under it (it does contain the plural `allocations`, so the claim still lands — cosmetic). Similarly "world-readable" rests on S158 lines 68-78 (mode 0444) and the shows at 672-688, not on cited line 1068 alone. Suggested wording: change the SKILL citation to `S158 lines 37, 68-78, 1066-1068; S154 line 140`.

6. [obs, minor defect — clause not supported by a cited line] SKILL advice "`btrfs filesystem usage` without root lacks chunk detail" is carried by no cited line. It is nonetheless true and already evidenced in this wave's committed capture: `.ufo/waves/round-30/w1/ExecHostCapture/btrfs-filesystem-usage.err.txt:1` = `WARNING: cannot read detailed chunk info, per-device usage will not be shown, run as root`; I reproduced it live (`btrfs filesystem usage /` as seat user, exit 0, same warning, and the output still shows Global reserve but no per-device table). Suggested wording: append `; capture btrfs-filesystem-usage.err.txt line 1` to the citation cell so the clause has a pointer.

7. [obs] Newness: partial. At base `fbfec6bd` (verified by `git archive` extract + grep): `global_rsv` and the `allocations` spelling have zero hits in `SKILL.md`, `corpus/knowledge/`, `corpus/SOURCES.md` (global_rsv appears only inside `.ufo/waves/round-26/` snapshot bytes). BUT the allocation directory itself with its `{data,metadata,system}` children was already lane knowledge: base `SKILL.md:2367` (row SH3) and `corpus/knowledge/storage-health-r26.md:45`, sourced from the same fs/btrfs/sysfs.c bytes registered as S133. The entry discloses this honestly: `corpus/knowledge/btrfs-space-r30.md:12` states "rows D04 and D06 restate those two facts for the space question". So D06 is carry-over surface plus genuinely new detail (the two global_rsv files, mode-0444 world-readability, the doc-vs-kernel spelling mismatch, the unprivileged-capture advice). Under the round-29 depth-framing ruling (routed item 5: restated rows are companion content, not new depth), the disclosure is the required treatment; the row cannot be counted as wholly new depth, and C1's "surface the lane has not covered" framing overstates it for this row specifically.

8. [obs] Operator decision is safe: the SKILL advice instructs only unprivileged reads of sysfs files and a read-only `btrfs filesystem usage` run; nothing writes, and the row's own capture was read-only. No lane write implied or required.

## Residual risk and gaps

- JSON statement clause "readable without root" is supported by the source (mode 0444) and host-observed, though the row's single pinned line (1068) does not itself carry the mode; the row schema pins one line, so this is defensible — optionally tighten the statement to name mode 0444.
- [unk] I did not re-run `tools/check-btrfs-space-r30.py` (verification is the integrator's job); row shape, keys, and quote placement satisfy R2–R9 on inspection.
- Quote-quality note: `grep -cF` on line 1068 for the declared quote returns 1; the quote is a verbatim substring of that one line.

Scope: read=lane files at 29bf87f (sandbox clone), base fbfec6bd via git archive extract, S158 fetched live from raw.githubusercontent.com, host /sys/fs/btrfs read-only, btrfs filesystem usage read-only run; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevRowD06.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevRowD06/S158-sysfs.c, plus scratch under /fast/scratch/hyaku/tsukuroi-r30/RevRowD06/; executed=curl, sha256sum, grep, sed, cat, ls, uname, btrfs filesystem usage (read-only), git clone/checkout/archive/show/rev-parse/ls-tree (sandbox clone only)
Model: devin/swe-2
Installs: none
