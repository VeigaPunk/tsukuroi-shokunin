# CritMistake — C1 count + defect-4 gap

Axes: wrong package/citation, registry-count drift, QUALITY26 provenance. Read-only: baseline `842a531`, lane `51dd9ee`, committed captures.

## CE1 — closure defect-4 drift routed to no claim

Defect 4 (`round-17-verifier-spotcheck.md:201-206`) names `SKILL.md:1897` "53 cases" vs evidence 61 (62 author-reported), `:1898` "44" vs 45, `:1902` "probe/all five/23" vs gate over nine/28, `:1900` missing `--exec-log`, and SCORECARD `:164` "44/44" vs `:520` "45/45" [obs, all re-checked at baseline]. Claims route only defect3→C1 and defect5→C3; defect5's list (`:208-211`) does not include these rows. `NoticeSkill` targets only 118/129-133/135/1833 [obs dispatch.json]; `ReviewRegistry` attacks but no seat notices the drifted rows. Known-stale counts persist unmarked at tip [inf scope-read] → LEARNING harmed trigger, unless a seat is assigned or a `planned` line scopes them out.

## CE2 — generic gate count is id-blind and C3-coupled

`BuildNoticeGate` emits one `resolved_records` over mixed `R18-CORR`/`R18-FRESH` in the shared registry; resolved = zero findings [obs spec]. (a) Masking: five clean FRESH records print resolved=5 while all CORR records red — "0→3+" reads satisfied falsely. (b) Coupling: one red FRESH record fails rc for C1. Shown-red fix: emit `resolved_corr`/`resolved_fresh` (or `--ids-prefix`); selftest fixture = 3 clean CORR + 1 broken FRESH expecting rc1 with both counters exposed.

## Qualifier — count ambiguity

Defect3's "40-42 and 43-46" may yield 2 records (NoticeBootCorrections: "two records if distinct") → 0→4 not 0→3; report the exact tally. `BootChainTruthR17` absent under `.ufo/waves/round-17/` [obs find] — hinted fourth slip unlocatable; scribe must not invent it.

## Surviving — QUALITY26

`capture-r18.sh` runs no pacman/checkupdates/yay/paru/mkinitcpio/limine-update; substitutions are `/var/lib/pacman/local` + pacman.log reads; header carries script sha256 → harness-captured exec log, not L1 excerpt [obs]. Defect3 facts verify: B:59 names 12 packages, B:124 is mtime 09:26:22, B:115 the 09:29:18 history copy, lts hashes at B:198-200.

Scope: executed=none
