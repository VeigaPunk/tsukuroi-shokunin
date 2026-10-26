source: S208, S213, S214, S215, S216, S217, S218 in `corpus/SOURCES.md` — libalpm `lib/libalpm/{hook.c,add.c,sync.c,remove.c,util.c,trans.c}` at pacman commit `54d9411` (the installed `pacman 7.1.0.r9.g54d9411-3`; snapshots `.ufo/waves/round-39/frozen/src/`, digests in `SHA256SUMS`), and the own-work transaction capture `.ufo/waves/round-39/frozen/txcapture/` (pacman.log copy, hook owners, hook phases; MANIFEST sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4`)
verified-at: 2026-10-26 (sources fetched 2026-10-26T05:30Z; capture 2026-10-26T05:42:12Z)
recheck: `python3 tools/check-transaction-order-r39.py --revision <REV>` re-verifies every TO row against the pinned snapshots and the two host counts against the frozen capture; on-release of pacman for S208 and S213–S217; 30d for S218

# The libalpm transaction order on this host (round 39)

Ground: the update-safety plane (`PROVINCE.md` Core). `corpus/knowledge/pacman-hook-order-r38.md` holds the
order of hooks **within** a phase (HO1–HO7); this entry holds what happens **between** the phases (TO1–TO8).
Every rule is read from libalpm source at the installed commit; the host column is read from a frozen copy of
this host's `/var/log/pacman.log`, no transaction was read live and no pacman command was run. Nothing here
authorizes a package, hook or transaction action.

It re-grounds, at source, the transaction-order propositions of the staged package entry
`merge/tsukuroi/…/pacman-hook-timing-r25.md` (refused as staged in round 38, `corpus/lessons/round-38.md`
Gate). Which of its propositions this entry admits, corrects or rejects is recorded in
`corpus/lessons/round-39.md` Gate.

## Rules (source-level, pacman 54d9411)

| id | rule | source (file:line at 54d9411 and quote) | host consequence |
|---|---|---|---|
| TO1 | The PreTransaction phase runs **before** `transaction started` is logged and a Pre-phase failure returns before that line; the commit runs between `transaction started` and `transaction completed`; the PostTransaction phase runs after `transaction completed` | S217 trans.c:201-208 “_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1); } trans->state = STATE_COMMITTING; alpm_logaction(handle, ALPM_CALLER_PREFIX, "transaction started\n");”; Post at trans.c:232-239 | In the frozen pacman.log, 60 transactions log `transaction started` (86 `[PACMAN] Running` windows); 0 `running '<hook>'` lines fall inside a commit phase, so every Pre `running` line of a window precedes its `transaction started` line |
| TO2 | A sync commit first removes the conflicting and to-be-replaced packages, then adds or upgrades the targets | S214 sync.c:1336-1356 “/* remove conflicting and to-be-replaced packages */” (`_alpm_remove_packages` :1345, then `_alpm_upgrade_packages` :1354) | No transaction in the capture both removes and adds packages (0 of 60), so the rule has no host instance yet; the 28 `removed` lines all come from removal-only transactions |
| TO3 | Packages are added one at a time in transaction order. Per package: the `pre_install`/`pre_upgrade` scriptlet runs from the package file before any file is extracted; then the files and the local database entry are written; then `installed`/`upgraded` is logged; then the `post_install`/`post_upgrade` scriptlet runs from the local database's `install` file | S213 add.c:466-474 (pre scriptlet), add.c:616-648 “/* run the post-install script if it exists */” (log line `upgraded %s (%s -> %s)` :630, post scriptlet :638-647); loop add.c:669-688 | A package's post-scriptlet output follows its own `installed`/`upgraded` line: pacman.log:123-124 `installed systemd (261.1-1)` then `[ALPM-SCRIPTLET] Initializing machine ID from random generator.`; a pre-scriptlet's output precedes the line |
| TO4 | Install scriptlets receive the **new** version first and the old version second (`pre_upgrade`/`post_upgrade`); install functions receive only the new version | S213 add.c:470-474 “_alpm_runscriptlet(handle, pkgfile, scriptlet_name, newpkg->version, oldpkg ? oldpkg->version : NULL, 1);” | A scriptlet comparing versions must read `$1` as new and `$2` as old |
| TO5 | `_alpm_hook_run` opens each hook directory anew on every call, and the Pre and Post phases are separate calls (TO1): the Pre phase sees the hook files on disk before the commit, the Post phase sees them after it. A hook whose package is first installed in a transaction is not a Pre candidate of that transaction; a hook removed by the transaction is not a Post candidate; an upgraded hook file runs old in Pre and new in Post | S208 hook.c:532-560 “for(i = alpm_list_last(handle->hookdirs); i; i = alpm_list_previous(i)) {” (`opendir` :554 inside the loop) | 17 PreTransaction hook files on this host are owned by a package that the capture shows first installed in some transaction; none of the 17 ran in that transaction's Pre phase. This is consistent with the rule, not a proof of it: the capture cannot separate an absent hook file from a trigger that did not match |
| TO6 | After all package adds, `ldconfig` runs once, before the commit phase ends; if any package failed to commit, `ldconfig` is skipped and the transaction is marked interrupted | S213 add.c:676-692 “/* running ldconfig at this point could possibly screw system */” | An interrupted transaction logs `transaction interrupted`, runs no `ldconfig` and no Post hook (TO1, HO6) |
| TO7 | A removed package (not the old half of an upgrade): `pre_remove` scriptlet, then file removal, then `removed` is logged, then `post_remove`; the old version of an upgraded package is removed with neither scriptlet nor `removed` line | S215 remove.c:699-733 “_alpm_runscriptlet(handle, scriptlet, "pre_remove", pkgver, NULL, 0);” (`removed %s (%s)` :722, `post_remove` :731) | `removed` lines (28 in the capture) appear only for whole-package removals, never for upgrades |
| TO8 | Every command libalpm runs in the chroot — hooks, install scriptlets and `ldconfig` — has each output line logged under the `ALPM-SCRIPTLET` tag; the tag does not mean "install scriptlet" | S216 util.c:521-528 “alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);” (`_alpm_chroot_process_output`; hooks reach it through `_alpm_run_chroot`, S208 hook.c:525-528) | 252 of 441 `[ALPM-SCRIPTLET]` lines in the frozen pacman.log lie outside every commit phase, so they are hook output, not scriptlet output |

## Order of one transaction, end to end

`[PACMAN] Running '<command>'` (the frontend) → Pre hooks in HO1 order (TO1, TO5) → `[ALPM] transaction
started` → removals before adds (TO2, TO7) → each target in transaction order (TO3, TO4) → `ldconfig` once
(TO6) → `[ALPM] transaction completed`, or `interrupted`/`failed` (TO1, HO6) → Post hooks, re-read from disk
(TO1, TO5, HO6).

## Boundaries

- It gives no per-hook verdict beyond TO5's 17-file check; HO7 and the pacman.log `running` lines answer whether a given hook ran.

## QUALITY check

- QUALITY 1–4: every rule row cites a mined tier-A row and a located quote at the cited lines (verified by
  `tools/check-transaction-order-r39.py`); host counts are reproduced from the frozen capture by the same tool.
- QUALITY 9: the snapshot digests and the capture MANIFEST are pinned in the tool and in the source rows.
- QUALITY 14: this section.
