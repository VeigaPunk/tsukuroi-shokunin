# ScribeClaims — round 15 evidence outline

Seat: TsukuroiR15.ScribeClaims. Baseline 0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2. Read-only; no probes, no web fetches, no verification run, tools none.

## Axes and ordinal deltas (all 0)
- Claimed: C1 depth (ordinal 8 → 8), C2 freshness (ordinal 9 → 9).
- Unchanged: coverage 9, operability 9, calibration 9, adjacency 8 (SCORECARD.md:48–52 round-11 table; SCORECARD.md:294 round-13 "Current ordinal scores" line).
- No axis harmed is claimed. Expansion/quality/discernment verdicts belong to L1.

## C1 depth — evidence outline
E1 Quote. R14 registry row S044 (SOURCES.md:50) and R14 JSON corrections[0].quote hold “Takes a boolean argument or the special values "full" or "strict".” (11 words). R15 must re-observe this from the reopened page; this seat has not.
E2 Locator defect. R14 MD line 34 and JSON corrections[0].location cite “rendered lines 1266–1267.” The R14 lesson (lines 233–239) records that the same closure's reader shows AF_UNIX there, ProtectSystem= at 1270, definition at 1272–1273. Repair: R15-LOCATOR names the stable heading SANDBOXING > ProtectSystem=, the footer version, and the renderer. Bare line numbers are not primary. R14 bytes stay unrewritten (append-only).
E3 Negative claim. R14 replacement text (JSON corrections[0].replacement; MD lines 42, 52–53) says the page “documents no further values for this option.” No command/date sweep backs it (lesson lines 240–246). Repair: R15-POSITIVE-DOMAIN supersedes that sentence and keeps only the positive definition. It must not claim exhaustive absence or parser proof.
E4 Preservation. R15 must not edit S001–S045 rows, the R14 pair, or the r13 lesson. S046 is the new reopen row (docs/A/mined), to be created by SourceRegistry only after opening.
E5 Census expectation. S046 shares its URL with S041/S044. R14 census showed W04 scope-separated duplicate-URL warnings with exit 0. Expect the same class for S046; disclose, do not claim a warning-free pass.

## C2 freshness — evidence outline
F1 Trigger. Operator-reported libinput partial upgrade at 2026-10-20 04:25 (spec context). Historical pending413 is context only; fresh counts may differ.
F2 Evidence file. .ufo/waves/round-15/build/host-snapshot.json was ABSENT when this seat read the wave directory. Required keys: package_versions, pending_updates, sync_metadata, libinput_log, boot_hook_mentions. Each probe needs command/exit/stdout/stderr. Only HostSnapshot runs probes.
F3 Historical log anchor. S032 (SOURCES.md:38) records /var/log/pacman.log at 2397 lines on 2026-10-19, including `-Sy fuse2` at line 1405 and last `-Syu` at 1414. The libinput transaction should fall after line 2397 if logged. IncidentEntry should compare line count and tail against that anchor, using the snapshot, not new commands.
F4 Sources. S047 (ArchWiki System maintenance) and S048 (pacman(8)) are not yet in SOURCES.md. Duplicate risk: S010 already opens ArchWiki System maintenance at oldid 885170 (SOURCES.md:16). SourceRegistry must either pin a different revision with a stated reason, or record S047 as a duplicate.
F5 Pacman guard. Only -Sp --print-format dry-run may be considered, and only for uninstalled candidates. This round never executes -S. Existing installed package = forbidden partial upgrade. No dry run was executed here.
F6 Decision. decision = BLOCKED_FOR_AGENT_PACKAGE_ACTION regardless of fresh counts. No clearance, no repair, no freshness uplift.

## Four unchanged axes — what to state and why
- coverage 9: no new surface. C1/C2 stay on existing rollback-net and update-gate ground (SOURCES.md:55–56). Ceiling noted, not moved.
- operability 9: census script not modified; no selftest run by this seat. Baseline drift: SCORECARD.md:49 cites 80/80 selftest, while the round-12 record (SCORECARD.md:257) cites 97/97. L1 must cite the value it measures, not either historical figure.
- calibration 9: no independent verdict is produced by r15 scribes. Future calibration evidence is the r15 verifier spot-check; state that it is pending.
- adjacency 8: no sibling, fleet, or routing edits. Scribe outputs remain in the wave build directory.

## Recommendations for L1
1. Keep depth 8 and freshness 9. Describe C1 as "documentation-debt repair, ordinal unchanged", not as depth uplift.
2. Use stable heading plus footer as the locator. Mark any renderer line numbers as reader-specific.
3. Keep the positive domain sentence verbatim (11 words). Do not restore "no further values" or any absence claim.
4. Disclose W04 for S046/S044/S041 URL reuse. Do not present exit 0 as warning-free.
5. Resolve the S010/S047 duplicate before claiming a new source. Do not count it as independent support.
6. C2 freshness: record "re-verified, blocked" and keep the ordinal at 9. Do not use the word improved.
7. Use the measured selftest count in LOG/SCORECARD; reconcile 80 versus 97 explicitly.

## Sources and limits
- Read this seat (local only): AGENTS.md; lesson round-14-verifier-spotcheck.md (lines 1–265 read); corpus/SOURCES.md (lines 1–84 read); corpus/knowledge/source-scope-correction-r14.json (lines 8–25, 140–158, grep); SCORECARD.md (lines 1–300 read); wave spec.json, dispatch.json, validation.json.
- Not opened: systemd.exec(5), GitHub endpoints, ArchWiki, pacman(8), any host command. This seat's claims rest on local artifacts and prior closure observations, marked as such.
- Not yet present at read time: source-locator-clarification-r15.{md,json}, partial-upgrade-recheck-r15.{md,json}, host-snapshot.json, S046–S048 rows.
- Limits: the R14 closure's reader observations are not reproducible here. Positive-domain wording does not prove exhaustiveness. Freshness evidence depends on the HostSnapshot capture, not on this report.

## Tools
None. No installs, updates, package changes, sudo, pacman, service actions, snapper queries, or daemon activation. Files written: this file only.
