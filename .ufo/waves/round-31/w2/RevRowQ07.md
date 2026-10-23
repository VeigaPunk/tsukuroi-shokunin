# RevRowQ07 — C1 row Q07 per-row review (round-31 wave 2, falsify)

Verdict: **holds** — C1 row Q07 at lane revision f3a5723a988bf1c2835985880e7a38d477462cd0 satisfies the frozen `new_sourced` predicate (quote verbatim at the cited snapshot line; every clause of the statement, the `| [R31-Q07] ` SKILL.md line and the decision-table row supported by S168's cited lines; question fully answered; fact novel against base 2077e2fa).

## Findings

1. [obs] Snapshot pin verified. `curl -sL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-replace.rst` → sha256 `da4bf595f072a96a309535c1022b0171a8657a4f207a3d3da73250886fd8bc9e` (138 lines, 4562 bytes). This equals the frozen pin in the S168 row (`corpus/SOURCES.md:262`, "raw bytes sha256 da4bf595…") and is byte-identical to the in-lane snapshot `.ufo/waves/round-31/w1/ScribeSrcReplace/btrfs-replace.rst` at f3a5723 (git show of that blob → same sha256).

2. [obs] Quote verbatim at the cited line. JSON row Q07 (`corpus/knowledge/btrfs-repair-r31.json` @ f3a5723) has `quote` = "btrfs replace start 1 /dev/sdc /mnt/my-vault/", `line` 106; `sed -n '106p' <fetched bytes> | grep -cF "btrfs replace start 1 /dev/sdc /mnt/my-vault/"` → 1. Line 106 sits inside the larger-drive example block (lines 101-119).

3. [obs] Clause-by-clause source support (quotes from the fetched v7.1 bytes, line numbers of the raw file):
   - "On a live filesystem, `btrfs replace start` duplicates the source's current data to the target" ↔ lines 22-24: "On a live filesystem, duplicate the data to the target device which is currently stored on the source device."
   - "If the source is unavailable, or `-r` is set, data is built using RAID redundancy" ↔ lines 25-26: "If the source device is not available anymore, or if the -r option is set, the data is built only using the RAID redundancy mechanisms."
   - "with `-r`, the source is read only when no other zero-defect mirror exists, an option documented for drives with many read errors and slow access" ↔ lines 54-57: "-r only read from *srcdev* if no other zero-defect mirror exists. (enable this if your drive has lots of read errors, the access would be very slow)"
   - "The source argument can be its device path or filesystem devid; a disconnected source must use devid" ↔ lines 30-33 ("otherwise it is the path to the source device. If the source device is disconnected … you have to use the devid parameter format").
   - "Completion removes the source" ↔ lines 27-28: "After completion of the operation, the source device is removed from the filesystem."
   - "The target must be the same size as or larger than the source" ↔ line 34: "The *targetdev* needs to be same size or larger than the *srcdev*."
   - "using all of a larger target requires resizing the filesystem to `<devid>:max`" ↔ lines 35-38: "The filesystem has to be resized to fully take advantage of a larger target device; this can be achieved with `btrfs filesystem resize <devid>:max /path`".
   QUALITY 66: no "always"; every "only" in the row texts exists in the source (lines 25, 54); no branch from lines 20-38 / 54-57 / 101-119 is lost in any of the three row texts.

4. [obs] SKILL.md decision line: exactly one `| [R31-Q07] |` line at f3a5723 (`SKILL.md:2686`, count via `git show …:SKILL.md | grep -c` → 1). Every clause ("replacement duplicates source data"; "for a source with many read errors, consider `-r` knowing access can be very slow"; "If the source is unavailable or `-r` is selected, data is built from RAID redundancy"; "`-r` reads the source only if no other zero-defect mirror exists"; "Use devid for a disconnected source"; "choose a target the same size as or larger than the source") maps to source lines 20-34/54-57 as in finding 3. Its citation "S168 lines 20-33, 54-57" is accurate. Decision-table row `corpus/knowledge/btrfs-repair-r31.md:18` (citation `` `btrfs-replace.rst:20-38` (S168) ``) is likewise supported, including "data is built only using RAID redundancy" (source line 25) and "the filesystem must be resized to use a larger target fully" (lines 35-38).

5. [obs] Question fully answered. Frozen question Q07 ("How is a failing or missing btrfs device replaced, and what size must the target be?") is answered by the statement: unavailable/missing source → RAID-redundancy rebuild and devid naming; live source → duplication; `-r` read-error path; completion removal; target size condition ("same size as or larger than the source") plus the resize-to-use-larger-target condition.

6. [obs] Novelty vs base 2077e2fa4fa70ea79aa77b6d91f4acd35bc54897. `git grep -i -F -c` over SKILL.md, PROVINCE.md, corpus/ → "btrfs replace" 0, "replace start" 0, "zero-defect" 0, "RAID redund" 0. The broader synonyms "replacement" and "devid" hit only unrelated base contexts: `devid` appears in sysfs `devinfo/<devid>/error_stats` paths (`SKILL.md:2365`, `corpus/knowledge/storage-health-r26.md:15,17,21`, `corpus/SOURCES.md:139` S133) — no replacement semantics; "replacement" hits are pacman/recheck-commands R17-R18 replacement and SE3 NVMe "replacement question for the operator" guidance. No base line couples btrfs with device-replacement behavior (regex sweep for `btrfs.*replace|replace.*btrfs|device.*replace|replace.*device` over the base corpus → no relevant hits). The fact is not held at base. This matches the errata (`SCORECARD.md:1222`: "Q02, Q03, Q04, Q05 and Q07 have no held neighbours").

7. [obs] Frozen counter at lane tip: `python3 tools/check-btrfs-repair-r31.py --revision f3a5723a988bf1c2835985880e7a38d477462cd0 --lane /fast/scratch/hyaku/tsukuroi-r31/RevRowQ07/repo` → `{"id": "Q07", "new_sourced": true, "fail": []}`; overall `new_sourced` 8 of 8, exit 0; `counter_sha256` 4f69a109e9b56b3fcba0df5a3555f7ff833b6b04fff28176060efe82ebde5cb8 (matches the declaration's frozen predicate sha256). No sealed answer keys were printed or recovered.

## Residual risk and verification gaps

- [inf] Sealed answer-key groups were not recovered (per instruction). Wording coverage of every key group therefore rests on the counter's empty `fail` list for Q07, not on an independent byte-level check.
- [unk] None else: the snapshot was fetched once (raw.githubusercontent.com, HTTP 200, sha256 matched the pin and the in-lane blob); no second fetch/further gap found. No action remains in scope for row Q07.

Scope: read=SCORECARD.md:1196-1224; corpus/SOURCES.md:262; SKILL.md @ f3a5723 (grep + count); corpus/knowledge/btrfs-repair-r31.md:18; btrfs-repair-r31.json row Q07 @ f3a5723; fetched v7.1 btrfs-replace.rst (138 lines); base 2077e2fa greps over SKILL.md/PROVINCE.md/corpus; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevRowQ07.md; executed=git show / git grep (read-only, sandbox clone), curl -sL, sha256sum, sed -n … | grep -cF, python3 tools/check-btrfs-repair-r31.py --revision f3a5723… --lane /fast/scratch/hyaku/tsukuroi-r31/RevRowQ07/repo

Model: inception/mercury-3

Installs: none
