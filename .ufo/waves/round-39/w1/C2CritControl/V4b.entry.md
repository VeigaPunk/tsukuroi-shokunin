source: S208, S213, S214, S215, S216, S217, S218 in `corpus/SOURCES.md` — libalpm `lib/libalpm/{hook.c,add.c,sync.c,remove.c,util.c,trans.c}` at pacman commit `54d9411` (the installed `pacman 7.1.0.r9.g54d9411-3`; snapshots `.ufo/waves/round-39/frozen/src/`, digests in `SHA256SUMS`), and the own-work transaction capture `.ufo/waves/round-39/frozen/txcapture/` (pacman.log copy, hook owners, hook phases; MANIFEST sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4`)
verified-at: 2026-10-26 (sources fetched 2026-10-26T05:30Z; capture 2026-10-26T05:42:12Z)
recheck: `python3 tools/check-transaction-order-r39.py --revision <REV>` re-verifies every TO row against the pinned snapshots and the two host counts against the frozen capture; on-release of pacman for S208 and S213–S217; 30d for S218

# The libalpm transaction order on this host (round 39)

Ground: the update-safety plane (`PROVINCE.md` Core). `corpus/knowledge/pacman-hook-order-r38.md` holds the
order of hooks **within** a phase (HO1–HO7). This entry holds what happens **between** the phases: where the
two hook phases sit against the `transaction started` / `transaction completed` log lines, the order of
removals, package writes and install scriptlets inside the commit, the scriptlet arguments, when the hook
directories are read, and what the `[ALPM-SCRIPTLET]` log tag does and does not mean. Every rule is read
from libalpm source at the installed commit; the host column is read from a frozen copy of this host's
`/var/log/pacman.log`. Nothing here authorizes a package, hook or transaction action.

It re-grounds, at source, the transaction-order propositions of the staged package entry
`merge/tsukuroi/…/pacman-hook-timing-r25.md` (refused as staged in round 38, `corpus/lessons/round-38.md`
Gate). Which of its propositions this entry admits, corrects or rejects is recorded in
`corpus/lessons/round-39.md` Gate.

## Rules (source-level, pacman 54d9411)

| id | rule | source (file:line at 54d9411 and quote) | host consequence |
|---|---|---|---|
| TO1 | The PreTransaction phase runs **before** `transaction started` is logged and a Pre-phase failure returns before that line; the commit runs between `transaction started` and `transaction completed`; the PostTransaction phase runs after `transaction completed` | S217 trans.c:201-208 “_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);” | In the frozen pacman.log, 60 transactions log `transaction started` (86 `[PACMAN] Running` windows); 0 `running '<hook>'` lines fall inside a commit phase, so every Pre `running` line of a window precedes its `transaction started` line |
| TO2 | A sync commit first removes the conflicting and to-be-replaced packages, then adds or upgrades the targets | S217 trans.c:201-208 “_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);” | No transaction in the capture both removes and adds packages (0 of 60), so the rule has no host instance yet; the 28 `removed` lines all come from removal-only transactions |
| TO3 | Packages are added one at a time in transaction order. Per package: the `pre_install`/`pre_upgrade` scriptlet runs from the package file before any file is extracted; then the files and the local database entry are written; then `installed`/`upgraded` is logged; then the `post_install`/`post_upgrade` scriptlet runs from the local database's `install` file | S217 trans.c:201-208 “_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);” | A package's post-scriptlet output follows its own `installed`/`upgraded` line: pacman.log:123-124 `installed systemd (261.1-1)` then `[ALPM-SCRIPTLET] Initializing machine ID from random generator.`; a pre-scriptlet's output precedes the line |
| TO4 | Install scriptlets receive the **new** version first and the old version second (`pre_upgrade`/`post_upgrade`); install functions receive only the new version | S217 trans.c:201-208 “_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);” | A scriptlet comparing versions must read `$1` as new and `$2` as old |
| TO5 | `_alpm_hook_run` opens each hook directory anew on every call, and the Pre and Post phases are separate calls (TO1): the Pre phase sees the hook files on disk before the commit, the Post phase sees them after it. A hook whose package is first installed in a transaction is not a Pre candidate of that transaction; a hook removed by the transaction is not a Post candidate; an upgraded hook file runs old in Pre and new in Post | S217 trans.c:201-208 “_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);” | 17 PreTransaction hook files on this host are owned by a package that the capture shows first installed in some transaction; none of the 17 ran in that transaction's Pre phase. This is consistent with the rule, not a proof of it: a Pre hook whose triggers did not match would not have run either |
| TO6 | After all package adds, `ldconfig` runs once, before the commit phase ends; if any package failed to commit, `ldconfig` is skipped and the transaction is marked interrupted | S217 trans.c:201-208 “_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);” | An interrupted transaction logs `transaction interrupted`, runs no `ldconfig` and no Post hook (TO1, HO6) |
| TO7 | A removed package (not the old half of an upgrade): `pre_remove` scriptlet, then file removal, then `removed` is logged, then `post_remove`; the old version of an upgraded package is removed with neither scriptlet nor `removed` line | S217 trans.c:201-208 “_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);” | `removed` lines (28 in the capture) appear only for whole-package removals, never for upgrades |
| TO8 | Every command libalpm runs in the chroot — hooks, install scriptlets and `ldconfig` — has each output line logged under the `ALPM-SCRIPTLET` tag; the tag does not mean "install scriptlet" | S217 trans.c:201-208 “_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);” | 252 of 441 `[ALPM-SCRIPTLET]` lines in the frozen pacman.log lie outside every commit phase, so they are hook output, not scriptlet output |

## Order of one transaction, end to end

1. `[PACMAN] Running '<command>'` (the frontend).
2. PreTransaction hooks whose triggers match, in HO1 order (`running '<name>'` lines; TO1, TO5).
3. `[ALPM] transaction started`.
4. Removals of conflicting or replaced packages (sync commits), each `pre_remove` → files → `removed` → `post_remove` (TO2, TO7).
5. Each target in transaction order: `pre_install`/`pre_upgrade` → files and database entry → `installed`/`upgraded` → `post_install`/`post_upgrade` (TO3, TO4).
6. `ldconfig`, once (TO6).
7. `[ALPM] transaction completed` (or `transaction interrupted` / `transaction failed`, which end it without Post hooks).
8. PostTransaction hooks whose triggers match, re-read from disk (TO1, TO5, HO6).

Every line any step 2–8 child prints is logged as `[ALPM-SCRIPTLET]` (TO8).

## Boundaries — what this entry does NOT establish

- It does not say whether a given hook ran on this host; HO7 and the pacman.log `running` lines answer that.
- TO5's host column is consistency, not proof: the capture cannot separate "the hook file was absent" from
  "its triggers did not match".
- It reads no transaction live and runs no pacman command; the host column comes from the frozen copy.

## QUALITY check

- QUALITY 1–4: every rule row cites a mined tier-A row and a located quote at the cited lines (verified by
  `tools/check-transaction-order-r39.py`); host counts are reproduced from the frozen capture by the same tool.
- QUALITY 9: the snapshot digests and the capture MANIFEST are pinned in the tool and in the source rows.
- QUALITY 14: this section.
