# FxFresh11 — C3 package-state-plane (NoticePackages-01–11)

P=`corpus/knowledge/package-state-plane.md` at 68a8ae0 (read via clone `/tmp/tsukuroi-r18-fxcountc3.fxGwXs/repo`; lane tree drifted mid-read); C=`.ufo/waves/round-18/l1-capture/host-capture-r18.txt`; R17=`.ufo/waves/round-17/l1-capture/`.

**FAILS — unmarked same-premise neighbors:**
- P:71,302 `-Qu` = 0 — R15 413 rows (`corpus/knowledge/host-health-report-r3.md:591`); full upgrade started 09:15:31 (R17 fresh-capture.txt:8); R17 sweep flagged (`.ufo/waves/round-17/build/FreshPackagePlaneSweep.md:25`). Add "pending UNKNOWN, never zero".
- P:42,45 16 foreign/3 explicit — later `-U` invocations hopper (C:71), zcode (C:73; `--asexplicit` C:65). Add "[unk]".
- P:65-69,299 "NOT in the omarchy sync db … no yay cache" — C:72 names yay-cache archives for all 13 elephant names; Foreign-04 marks reachability [unk].
- P:277-278 list-configs empty; snapper/limine-snapper-sync versions → C:37/C:31 (R17 boot-chain-capture.txt:50 upgraded). Add supersession.

**FAILS 09 (negative):** no rollback claim, but "snapshot existence … not measured" ignores R17 snapshots #1/#2 ro=true (boot-chain-capture.txt:159-167) and list-configs home/root (fresh-capture.txt:42-46), credited in `corpus/knowledge/freshness-recheck-r17.json:169-181`. Fix: scope to S060, cite; persistence/restore untested.

**FAILS 05/06:** "last logged pacman transaction" = C:63-65, two hook lines + `pacman -D` invocation, no completion (dup FxSrc060; lane-tree json:199 `reason` keeps it). New, 05: directory mtime ≠ last write — libalpm rewrites `desc` in place (pacman `lib/libalpm/be_local.c:997`; set_reason :1199-1200), so C:65 may write after 13:23:08.487. Fix: "last entry create/remove; last write ≥13:23:08.487, exact [unk]".

**FAILS 06 reason:** "conflated a file mtime with an update time" recasts history: P:96-99 paired local pubring/trustdb mtime 16:14:29 with install 16:14:27; R18 never reread them. Fix: "dated inference; keyring now 20260909-1 (C:28); update time [unk]".

**UNPROVEN 03:** "four configured" superseded by five sync-dir files; pacman.conf unread; offline.db (P:82-85) shows sync `.db` ≠ configured (Aur-10: [unk]). Fix: heading "sync-directory DB files four to five"; add "configured-repo set [unk]".

**SURVIVES (7/11):** 01 (count; "same method as P:86-87" overstates), 02, 04, 07, 08, 10, 11 — C:6,25,28,30,36,48-54,83; 11 keeps C:72 invocation-only.

**Unknowns:** no git-blob check; libalpm read at master; pending, foreign counts, snapshot persistence unmeasured.

Scope: executed=none
