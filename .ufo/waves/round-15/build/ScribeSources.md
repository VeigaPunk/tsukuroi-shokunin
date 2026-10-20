# ScribeSources — round-15 before45 row history and expected touched fields

Scope: read-only record of `corpus/SOURCES.md` before S046–S048 land. No census execution, no URL fetches, no verification, no product edits.

## Baseline (0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2)
- `corpus/SOURCES.md` in the working tree is byte-identical to the baseline blob (`cmp`). S046–S048 absent. No `*r15*` source-locator or partial-upgrade file exists yet.
- Rows S001–S045: **45**, all 11 cells (malformed 0).
- Tier: A37 / B1 (S023) / C7 (S030, S033, S036, S037, S042, S043, S045).
- Status: mined32 / queued5 (S006, S012, S013, S018, S024) / rejected8 (S029, S030, S033, S036, S037, S042, S043, S045).
- Kind: docs29, code5, community5, own-work3, tool2, dataset1.
- Empty used-by (`—`): S006, S012, S013, S018, S024, S029, S030, S033, S036, S037, S042, S043. All other used-by paths exist on disk.
- Duplicate source URLs across rows (scope-separated): `systemd.exec.5` (S028, S041, S044); omarchy #8047 (S036, S042); `access.2` (S034, S038); omarchy #6629 (S037, S043).

## Row history (append-only, from registry Search log and status columns)
- By 2026-10-19: S001–S033 (S029, S030, S033 rejected).
- Round 12 (2026-10-20): S034–S037 added → 37. S035 flipped queued→mined.
- S038 (`access.2`, supersedes S034's scope) → 38.
- S039, S040 added queued → 40; both flipped to mined when `root-dac-decision-r12` cited them.
- Round 13: S041 (`systemd.exec.5`, mined); S042/S043 rejected, superseding S036/S037 → 43.
- Round 14: S044 (mined, complements S041); S045 rejected, superseding S042 → **45 = baseline**.
- Logged mutable changes are only status flips and used-by appends. S001–S045 content is not rewritten.

## Expected touched fields for S046–S048
- Append after S045, before `## Paths`: three new rows, 11 cells each: `id`, `source`, `kind`=docs, `tier`=A, `scope`, `anchor`, `teaches`, `status`=mined only after the URL is actually opened, `opened`=2026-10-20 (not the 2026-10-19 carry-over date), `recheck`, `used-by`.
- Proposed `recheck`: S046 on-release (systemd 262.1 man-page footer), S047 180d (ArchWiki oldid page), S048 on-release (pacman man page). Precedent: S007/S008/S028 on-release; S010/S011 180d.
- `used-by`: S046 → `corpus/knowledge/source-locator-clarification-r15.md`; S047 and S048 → `corpus/knowledge/partial-upgrade-recheck-r15.md`.
- `## Search log`: append one dated 2026-10-20 SourceRegistry paragraph (URLs opened, quotes ≤25 words, screened and included counts, new registry total).
- Optional mutable: append `source-locator-clarification-r15.md` to S044 `used-by` only if C1 cites S044 (precedent: S027, S028, S034, S035). No status flips required.
- Expected no-edit: `## Paths`, `## Leads (unopened)`, S001–S045 content.

## Expected after-state (if all three land mined)
- 48 rows; tier A40 / B1 / C7; status mined35 / queued5 / rejected8; malformed must stay 0 (no literal `|` inside quoted text).
- W04 duplicate-URL expectation (predicted, not run): S046 reuses `systemd.exec.5`, a fourth occurrence, so +1 W04. S047 gives +1 only if it reuses S010's exact URL `https://wiki.archlinux.org/title/System_maintenance?oldid=885170`. S048 `man.archlinux.org/man/pacman.8` has no baseline row, so 0.

## Discrepancies to route to L1 / SourceRegistry
1. Dispatch SourceRegistry text calls S047 "partial-upgrade unsupported" and S048 "print/query semantics". Spec (IncidentEntry) calls S047 ArchWiki System maintenance and S048 pacman(8). These can agree: ArchWiki System maintenance does say "Partial upgrades are unsupported". But S010 already registers that article at oldid 885170. S047 must teach its distinct claim and either use a different oldid or disclose the W04.
2. The r14 lesson says "6 W04 total", but its own printed census shows 5 W04 lines (S038, S041, S042, S043, S044). Route as a documentation mismatch before the r15 count is quoted.
3. S048 must cite the `--print` / `--print-format` text actually opened, not the dispatch's paraphrase.

## Limits and tools
- Evidence: `git show` of the baseline blob, `cmp`, awk histograms, `test -e` on used-by paths, `grep` on the working tree. No census script, no URL fetch, no test or build.
- Row history is reconstructed from the Search log and status column. Per-flip dates beyond those paragraphs are not recorded in the file.
- The working tree may change while SourceRegistry writes. Recount after it lands.
- Only the 0db618a7 counts (45 rows; A37/B1/C7; mined32/queued5/rejected8) were re-measured. Intermediate counts (33, 37, 38, 40, 43) are Search-log claims, not re-measured.
- Tools: none installed, upgraded, or removed. No pacman, sudo, service, snapper, or daemon action. `git` used read-only.
