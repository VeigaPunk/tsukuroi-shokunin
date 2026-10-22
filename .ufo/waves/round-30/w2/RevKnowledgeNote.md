# Reviewer report — RevKnowledgeNote (wave 2)

Verdict: partly holds — every number in `corpus/knowledge/btrfs-space-r30.md` and the SKILL.md "Btrfs space allocation and ENOSPC — round 30" section recomputes exactly from the capture, the header contract and recheck-gate pass, and the mori boundary substance is right; but the .md decision table leaves row 1 and row 4 uncited, row 4's reading is loosely wrong, the mori line range is imprecise, and the claim that this entry "is reported to mori in PROVINCE.md style" has no backing row in PROVINCE.md.

## What I reviewed

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/btrfs-space-r30.md` (tip `29bf87fa`)
- `SKILL.md` section at `29bf87fa:SKILL.md:2600` (heading `## Btrfs space allocation and ENOSPC — round 30`), rows `[R30-D01]`–`[R30-D10]`
- Capture `.ufo/waves/round-30/w1/ExecHostCapture/btrfs-allocation-capture.txt` plus its sibling outputs `btrfs-filesystem-usage.out.txt` and `btrfs-filesystem-df.out.txt`
- Source snapshots under `.ufo/waves/round-30/w1/ScribeSrc{FsUsage,Balance,Mkfs,SysfsDoc,BlockRsv,Subvol,KSysfs,SpaceInfo}/` (S152–S159); sha256s printed in session, e.g. S156 `3a135842…` matches the SOURCES.md anchor
- `corpus/SOURCES.md` rows S152–S163 at the tip; `mori-shokunin` `SKILL.md` at `05db57ed`; lane `PROVINCE.md:150-189`; `tools/check-recheck-commands.py` docstring
- Routed context: `corpus/lessons/round-29-verifier-spotcheck.md` §5

## 1. Numbers — all recompute exactly

- 91.5 percent: capture line 50 `metadata/bytes_used: 35372056576` ÷ line 67 `metadata/total_bytes: 38654705664` = 91.5077%, matching the capture's own derived block (line 99: 91.5077633328%). `.md:34` is exact.
- 643 GiB unallocated: capture line 98 computes `998037782528 − (229789138944 + 77309411328 + 16777216) = 690922455040`; 690922455040 / 2^30 = 643.47 GiB, and `btrfs-filesystem-usage.out.txt:4` reports `Device unallocated: 690922455040`. `.md:35` and D09 agree.
- 2.00 ratio: `btrfs-filesystem-usage.out.txt:11` `Metadata ratio: 2.00`, consistent with DUP (disk_total 77309411328 = 2 × total_bytes 38654705664, capture lines 53/67). `.md:16` is exact.
- Global reserve: `global_rsv_size`/`global_rsv_reserved` both 536870912 (capture 43–44); `.md:36` "at the 512 MiB cap" matches S156:394 (`block_rsv->size = min_t(u64, num_bytes, SZ_512M);`, verified verbatim at that line in snapshot `ScribeSrcBlockRsv/S156-block-rsv.c`); "and full" means reserved == size, and usage.out:12 shows `(used: 0)`, matching SKILL D10's "full and unused". Consistent.
- `bg_reclaim_threshold` 0 (capture 45) and chunk_size 1073741824 = 1 GiB (capture 52): `.md:26` and `.md:37` are exact; the `[unk]` marking is honest.
- Device size 998037782528, profiles single/DUP/DUP, capture time 21:16:37Z, kernel 7.2.11-arch1-1, btrfs-progs v7.1: all verbatim in capture lines 11–15, 95 and usage.out:15–19.

## 2. Overclaim check — "not near metadata ENOSPC" is earned

`.md:39` reads "This host is not near metadata `ENOSPC` at capture time." That follows from S159:176-178 (verified verbatim: "If there is no unallocated space to be had, all reservations are kept within the free space in the allocated metadata chunks") — 643 GiB unallocated means the confined-reservations condition is not met, and the sentence is scoped "at capture time" plus "re-read before acting". Not an overclaim. [obs] Residual: contiguity of the unallocated space is unmeasured (aggregate free_chunk_space can still fail per-extent allocation); the note neither claims nor needs this. `[unk]`

## 3. Defects

1. **`.md` decision-table row 4 (`btrfs-space-r30.md:29`) is uncited and its middle column is loosely wrong.** `global_rsv_reserved` shows `block_rsv->reserved`, not a consumption counter: S158 sysfs.c `global_rsv_reserved_show` returns `&block_rsv->reserved` (verified, `ScribeSrcKSysfs/S158-sysfs.c:681-688`), and `block_rsv->reserved < block_rsv->size` is the under-funded state the kernel refills toward `size` (S156:395-397, the `if (block_rsv->reserved < block_rsv->size)` top-up branch), not "the reserve is being consumed". S154 loosely calls `global_rsv_reserved` "the used bytes" (`S154-ch-sysfs.rst:145-146`), so the doc does not support the wording either. The decision (treat as full, stop writers) is harmless as advice, but the mechanism claim and row carry no citation at all. Fix: cite `S158 sysfs.c:681-688` / `S154:145-152`, and reword to e.g. "the reserve is under its target size — the kernel could not top it up from metadata space (S156:395-397)".
2. **`.md` decision-table row 1 (`btrfs-space-r30.md:26`) is uncited.** The "metadata/chunk_size, 1 GiB here" operand is capture data (capture line 52) and the "not yet an ENOSPC risk" claim is the D01/D09 mechanism (S159:177, S152:398). Fix: append the citations or a `capture line 52` pointer, matching the row-2/3 style that does cite.
3. **The mori line range is exact — no defect here.** `.md:10` and the SKILL.md section cite mori `SKILL.md:415-418` at `05db57ed`. Verified with `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 05db57ed:SKILL.md | sed -n '415,419p'`: the "Never threshold the btrfs chunk percent" bullet occupies exactly lines 415–418 (`415:- **Never threshold the btrfs chunk percent.**` through `418:` ``the `df -P` parser.``); line 419 starts the next bullet. The substance also matches — mori keeps the `df -P` parser and never thresholds the chunk percent, which is what `.md:10` asserts. Recorded so the next reader need not redo it. [obs]
4. **"reported to mori in `PROVINCE.md` style" is not verifiable (`.md:10`).** No PROVINCE.md paragraph reports this entry: `git show 29bf87fa:PROVINCE.md | grep -nE 'round.?30|btrfs|ENOSPC'` shows only round-26/27 material; the relevant text is the existing round-26 split at `PROVINCE.md:165-176` (runway/free-capacity to mori at `:166`, corrected at `:176` to "free space as fleet runway is mori's, free space as an upgrade or boot precondition is this lane's"). The boundary substance does match PROVINCE — this entry claims mechanism/repair decisions, not runway, and explicitly leaves thresholds to mori — but nothing was "reported" anywhere, and "in PROVINCE.md style" has no referent. Fix: either append a one-line PROVINCE note (round-30 frontier entry deferring runway/thresholds to mori) or reword to "consistent with the `PROVINCE.md:165-176` split; no mori report filed".
5. **Minor: SKILL D02 citation covers the definition but not the 512 MiB cap.** SKILL row `[R30-D02]` cites only `S152 line 418` (the usage-field definition, verified at `S152-btrfs-filesystem.rst:418-420`), yet its reading column asserts "capped at 512 MiB in v7.2" — that is S156:394 (kernel code), cited only in the .md prose. Fix: append `; S156 line 394` to the D02 source cell. Similarly SKILL `[R30-D06]`'s trailing claim "btrfs filesystem usage without root lacks chunk detail" is not covered by its cited `S158 line 1068`/`S154 line 143` (the `allocation_attrs` list and directory table, both verified); either source it or drop it. [inf]

## 4. Checks that pass

- Header contract (CORPUS.md:18, :163-165): `source:`/`verified-at:`/`recheck:` are lines 1–3, first. `companion:` on line 4 is an extra key but still before the title — not a violation. `verified-at: 2026-10-22` matches capture `2026-10-22T21:16:37Z`; sources S152–S159 are all `mined` with `opened=2026-10-22`, S160/S161 `rejected` with substantive REJECTED teaches text (the .md "Sources not admitted" section is a fair condensation).
- recheck: command: `tools/check-recheck-commands.py --revision 29bf87fa --paths corpus/knowledge/btrfs-space-r30.md` run in a sandbox clone at `/fast/scratch/hyaku/tsukuroi-r30/RevKnowledgeNote/repo` → `{"status": "PASS", "findings": [], "invocation_count": 0}`, exit 0. The backticked sysfs path and `btrfs filesystem usage -b /` invoke none of the forbidden set (`pacman, checkupdates, yay, paru, mkinitcpio, limine-update`).
- Line citations I verified verbatim in snapshots: S152:398 (unallocated definition, line 398 exact), S152:418-420 (global reserve, exact), S153:51 (`usage=<percent>` definition at line 51; workspace caveat at 52-54), S155:59 ("Default on a single device filesystem is *DUP*", exact), S156:394 (512 MiB cap, exact), S157:40 ("initially share all of the same data blocks", exact; the deletion-frees-nothing inference rides on lines 202-206 about cleaning cost — acceptable, shared-extents is the operative premise), S158:679 and 1068 (`BTRFS_ATTR` lines, exact), S159:176-178 (overcommit comment, exact), S154:143/165-168 (allocations-dir heading and bg_reclaim_threshold definition, exact — note the source spells `allocations` while the kernel creates `allocation`; SKILL D06 flags this correctly).
- SKILL.md table rows all carry a Source column entry; only the .md table drops citations (defects 1–2 above).
- `host-rows.json` statements for D08–D10 are consistent with the capture and with the .md readings; its more cautious "material risk" phrasing does not contradict the note.
- Sibling/PROVINCE coherence: SH3 restatement is accurately described (`.md:12` vs `storage-health-r26.md` SH3 and `SKILL.md:2367`); the D06 "singular `allocation`" note matches S158:1064 comment path.

## 5. Exact fix list
1. `btrfs-space-r30.md:26` — append `capture line 52` and `(S159 line 177)` to the row's cells.
2. `btrfs-space-r30.md:29` — reword the middle cell per kernel semantics and add `S158 sysfs.c:681-688` (or the doc `S154:145-152`).
3. `btrfs-space-r30.md:10` — either add a PROVINCE.md round-30 boundary line or reword "it is reported to mori in PROVINCE.md style" → "consistent with the `PROVINCE.md:165-176` split".
4. SKILL.md `[R30-D02]` source cell — add `S156 line 394` for the 512 MiB cap.
5. SKILL.md `[R30-D06]` decision cell — cite or drop "btrfs filesystem usage without root lacks chunk detail".

## Residual risk

- `.md:37`'s `[unk]` on `bg_reclaim_threshold` 0 is honest; D05's 0-default semantics stay open.
- "Not near ENOSPC" is aggregate-space reasoning; per-extent contiguity is untested (marked `[unk]` above).
- I did not re-run `check-btrfs-space-r30.py` or the battery; my check was citation/number/boundary-level only, and other wave-2 seats own the counter and battery reruns.

Scope: read=corpus/knowledge/btrfs-space-r30.md, SKILL.md@29bf87fa section, capture + usage/df outputs, host-rows.json, CORPUS.md, check-recheck-commands.py docstring, SOURCES.md S152-S163 rows, mori SKILL.md@05db57ed, PROVINCE.md, S152-S159 snapshots, storage-health-r26.md SH3, SCORECARD.md declaration, round-29-verifier-spotcheck.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevKnowledgeNote.md; executed=git show/log/rev-parse (read-only, lane and mori), git clone --no-local + checkout to /fast/scratch/hyaku/tsukuroi-r30/RevKnowledgeNote/repo, sed/grep/awk/sha256sum on committed files and snapshots, python3 tools/check-recheck-commands.py --revision 29bf87fa --paths corpus/knowledge/btrfs-space-r30.md (exit 0, PASS)
Model: devin/swe-2
Installs: none
