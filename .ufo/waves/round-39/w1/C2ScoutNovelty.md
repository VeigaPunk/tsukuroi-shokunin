VERDICT: supports

# C2ScoutNovelty — item C2-13: novelty of TO1–TO8 against the lane at base 0eff65b2

Scope: `git grep` at tree `0eff65b21bb81195ee06c96a83afbd7a07e52eef` over `corpus/ SKILL.md PROVINCE.md`, pattern `pre_upgrade|post_install|post_upgrade|pre_install|pre_remove|post_remove|ALPM-SCRIPTLET|transaction started|transaction completed|ldconfig|replaced|scriptlet` plus `add.c|sync.c|remove.c|util.c|chroot|interrupted`. Receipt (92 hit lines, `replaced` noise included): `.ufo/waves/round-39/w1/C2ScoutNovelty/base-grep.txt`. Held text read at base: `corpus/knowledge/pacman-hook-order-r38.md` (HO1–HO7 + "Round 38 correction"), `corpus/knowledge/boot-writers-r19.md`, `SKILL.md:3181`, `corpus/lessons/round-38.md:48`, and the r38 wave receipts `AsmS209Scriptlet.md`, `AsmRevTiming.md`. PROVINCE.md has no hit for any pattern.

## Count

8 rows: **4 new** (TO2, TO4, TO5, TO7), **4 sharpen** (TO1, TO3, TO6, TO8), **0 pure restatements**. Every row adds at least one proposition no base file holds. The three rows with the heaviest overlap (TO1, TO3, TO6) overlap on one clause each; the rest of each row is new.

## What the lane held at base (all the relevant ground)

- Hook phase order and failure (S208/S210): `pacman-hook-order-r38.md:20` HO5 (Pre-phase error → "the transaction never starts", `trans.c:201-204`); `:21` HO6 (Post only after `transaction completed`, failed/interrupted run none, Post failure ignored, `trans.c:212-240`); `:22` HO7; `:136` (round-38 correction: commits per target, no rollback, `add.c:670-687`, `sync.c:1336-1360`; interrupt returns 0, `trans.c:230-232`, `:242-244`). `SKILL.md:3181` repeats the same with `trans.c:230-241`, `add.c:670-687`, `sync.c:1336-1357`, `add.c:673-675`.
- Hook directory handling: HO2 (`hook.c:540`, `:588-590` dir order; first name wins); round-38 correction cites `opendir` only as an error path (`hook.c:554-562`).
- `add.c`/`remove.c` only for backup files: S191/S192 and `pacman-backup-files-r35.md` (`.pacnew`/`.pacsave`, `add.c:302-404`, `remove.c:347-426`). No base row cites scriptlet, ldconfig or `removed`-line code.
- Install scriptlets: no base file states a scriptlet execution rule. Hits are `aur-risk-plane.md:202` ("install-time code execution — `install` scriptlet", fires 0/16), `driver-firmware-plane.md:79` (DKMS scriptlets, observation) and `SKILL.md:753`. Not rules about order or arguments.
- `ALPM-SCRIPTLET`: used as an attribution signature only — `boot-writers-r19.md:40` (signature of W-MKINITCPIO-HOOK), `:68-71` (EV-01/03/04 = `[ALPM-SCRIPTLET]` lines pacman.log 2021, 3015, 3047), `:91` (expected `[ALPM-SCRIPTLET] Updated: /boot/limine.conf` inside a transaction with `running '90-mkinitcpio-install.hook'`), `SKILL.md:2012,2022,2045`, `QUALITY.md:70`. `corpus/lessons/round-19.md:13`: "hook identity for ALPM events is [inf]". The tag's mechanism is not stated anywhere.
- `transaction started`: only as a log observation (`foreign-provenance-r6.md:69`), never as an ordering anchor.
- `ldconfig`: only as host hook files — `pacman-hook-order-r38.md:39` (`11-glibc-ldconfig.hook`, PostTransaction) and `update-safety-note.md:120` ("ldconfig/iconv hooks" coupling). Nothing on libalpm's own `_alpm_ldconfig`.
- Staged-but-not-admitted: `pacman-hook-timing-r25.md` was rejected "not as staged" (`corpus/lessons/round-38.md:48`). Its flip condition names what the lane did not hold: "upgrade order old-Pre → scriptlets → new-Post; provider lifecycle". `AsmRevTiming.md` §1 sweep: no lane file holds "the hook lifecycle (availability bound to the providing package), the old→new upgrade order, the `.INSTALL` scriptlet contract". `AsmS209Scriptlet.md` §1b verified in the man page (not code) that `pre_upgrade`/`post_upgrade` take new version first — a wave receipt, never in `corpus/`.

## Per row

| row | class | held at base | what TO adds |
|---|---|---|---|
| TO1 | **sharpens** | Two of three clauses restate held rules: Pre-phase failure returns before the transaction starts (HO5, `pacman-hook-order-r38.md:20`, `trans.c:201-204`); Post only after `transaction completed` (HO6, `:21`, `SKILL.md:3181`) | New: placing the Pre phase against the logged `transaction started` line and the commit between `started`/`completed` (`trans.c:201-208`), so each phase has a log-line boundary; host count 60 started / 86 `Running` windows / 0 `running` lines inside a commit |
| TO2 | **new** | `sync.c:1336-1357/1360` is cited at `SKILL.md:3181` and `pacman-hook-order-r38.md:136`, but only for "commits are per-target"; no row says removals precede adds | Remove-conflicting/replaced first, then add/upgrade (`sync.c:1336-1356`); host: no transaction has both (0 of 60) |
| TO3 | **sharpens** | The per-target loop restates `pacman-hook-order-r38.md:136` / `SKILL.md:3181` (`add.c:670-687`) | Intra-package order pre-scriptlet → files → log line → post-scriptlet, and where each scriptlet script comes from (package file vs local db `install`); nothing in base states it |
| TO4 | **new** | Only the man-page form existed, as an unadmitted wave receipt (`AsmS209Scriptlet.md` §1b, staged r25 claim rejected by `round-38.md:48`); no `corpus/` hit | New in corpus and at code level: `_alpm_runscriptlet(..., newpkg->version, oldpkg ? oldpkg->version : NULL, 1)` (`add.c:470-474`) |
| TO5 | **new** | HO2 holds dir order; round-38 correction holds `opendir` failure (`hook.c:554-562`); neither says the directories are re-read on each `_alpm_hook_run` call, hence nothing on which hooks are visible in Pre vs Post for a hook installed, removed or upgraded by the same transaction. `AsmRevTiming.md` §1 lists "hook lifecycle" as not held | The re-read-per-phase rule (`hook.c:532-560`) and its three consequences; host column is consistency only (the row says so) |
| TO6 | **sharpens** | The "if any package failed to commit, interrupted, no Post" clause restates `SKILL.md:3181` (`add.c:673-675`) and `pacman-hook-order-r38.md:136`. `ldconfig` appears only as hook files | New: libalpm calls `ldconfig` itself, once, after all adds, skipped on failure (`add.c:676-692`); distinct from the `11-glibc-ldconfig.hook` hook (`pacman-hook-order-r38.md:39`) |
| TO7 | **new** | S192/`remove.c` held only for backup-file save (`remove.c:347-426`); no remove-scriptlet or `removed`-line rule; `aur-risk-plane` counts are observations | pre_remove → files → `removed` → post_remove; upgrade's old half has no scriptlet and no `removed` line (`remove.c:699-733`); host: 28 `removed` lines, removal-only |
| TO8 | **sharpens** | The lane attributes `[ALPM-SCRIPTLET]` lines to hooks by observation (`boot-writers-r19.md:40,68-71,91`; `SKILL.md:2022`), identity marked [inf] (`round-19.md:13`); mechanism unstated | Source rule: `_alpm_chroot_process_output` tags every chroot child line (`util.c:521-528`); tag ≠ "install scriptlet"; host 252/441 lines outside any commit window |

## Receipts for the TO8/TO1 interaction with r19

My own pass over the frozen `pacman.log` (`.ufo/waves/round-39/frozen/txcapture/pacman.log`; receipt `.ufo/waves/round-39/w1/C2ScoutNovelty/evlines-vs-windows.txt`): the three r19 events EV-01/03/04 (pacman.log 2021, 3015, 3047) each follow a `transaction completed` line (1950, 2941, 2941), i.e. they sit in the Post phase, not in a commit window. Together with TO1 and TO8 this turns the r19 "[inf]" (`round-19.md:13`) hook attribution of those three lines into a source-backed reading: an install scriptlet cannot produce a line after `transaction completed`. The same pass reproduces the TO8 host count (441 `[ALPM-SCRIPTLET]` lines, 252 outside commit windows). This is a consequence, not a change to any TO row.

## Defect notes (observed, none kills a row)

- TO3/TO4/TO7 state scriptlet execution unconditionally. The cited source gates it: `add.c:467-469` — `if(alpm_pkg_has_scriptlet(newpkg) && !(trans->flags & ALPM_TRANS_FLAG_NOSCRIPTLET))`. A transaction with the NOSCRIPTLET flag runs no scriptlet and no TO3/TO4/TO7 scriptlet clause then applies. The entry does not say this and does not call it out in its Boundaries. [I read `add.c:467-474` in the frozen snapshot; I did not check `remove.c` for the same gate.]
- TO6 wording "if any package failed to commit, `ldconfig` is skipped and the transaction is marked interrupted" matches `add.c:673-690` (frozen snapshot, read).
- Not judged: this seat did not verify the host-column counts other than the 441/252 one (re-run above) and the three EV lines; did not verify TO rows against the source other than the lines quoted above (TO1 `trans.c:199-208`, TO2 `sync.c:1336-1356`, TO4 `add.c:466-474`, TO6 `add.c:673-692`, TO8 `util.c:518-528`, TO5 `hook.c:548-556` opens `opendir` inside the loop) — I read these lines in `.ufo/waves/round-39/frozen/src/`; TO3 post-scriptlet lines, TO7 `remove.c`, TO5's full loop were not re-read. The kill rule (a reviewer judging a TO row FALSE) is not exercised by this seat beyond the lines named.

TO1: holds — .ufo/waves/round-39/frozen/src/trans.c:201-208
TO2: holds — .ufo/waves/round-39/frozen/src/sync.c:1336-1356
TO4: holds — .ufo/waves/round-39/frozen/src/add.c:466-474
TO5: partly — .ufo/waves/round-39/frozen/src/hook.c:548-556 (opendir inside the loop seen; the loop header at :532-560 and the per-phase consequences not re-read)
TO6: holds — .ufo/waves/round-39/frozen/src/add.c:673-692
TO8: holds — .ufo/waves/round-39/frozen/src/util.c:521-528 (the `_alpm_run_chroot`/hook.c:525-528 link not re-read)

Tools installed or updated: none.
