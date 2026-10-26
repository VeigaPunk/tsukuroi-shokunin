VERDICT: supports (HO5's [unk] resolves: exactly one pacman CLI option, `--dbonly`, sets ALPM_TRANS_FLAG_NOHOOKS; no condition or config key sets it)

Item C2-10. Source: shallow-equivalent full clone of https://gitlab.archlinux.org/pacman/pacman.git into /fast/scratch/hyaku/tsukuroi-r38/C2ScoutNohooks/src, `git checkout 54d9411`; `git rev-parse HEAD` = 54d94116164b0b2202c6061c4a59c6f3e70820d8. Accessed 2026-10-26. Greps ran on that checkout (the lane has no tools installed/changed; no host mutation).

## Answer
Only one setter exists at 54d9411.

`grep -rni "nohooks|no-hooks|NOHOOK"` over the whole tree (excluding po/ and .git/) returned exactly 5 hits:
- lib/libalpm/alpm.h:2839 `ALPM_TRANS_FLAG_NOHOOKS = (1 << 7),` (doc comment line 2838: "Do not run hooks during a transaction")
- src/pacman/pacman.c:723 `config->flags |= ALPM_TRANS_FLAG_NOHOOKS;` — the ONLY setter
- lib/libalpm/trans.c:201 and :237 — the two ONLY consumers
- README:727 changelog note "alpm_transflag_t - added ALPM_TRANS_FLAG_NOHOOKS"

The setter sits in `parsearg_trans()` (src/pacman/pacman.c:709), `case OP_DBONLY:` (720-724):
```
720  case OP_DBONLY:
721      config->flags |= ALPM_TRANS_FLAG_DBONLY;
722      config->flags |= ALPM_TRANS_FLAG_NOSCRIPTLET;
723      config->flags |= ALPM_TRANS_FLAG_NOHOOKS;
```
So `--dbonly` implies DBONLY + NOSCRIPTLET + NOHOOKS. Option table: src/pacman/pacman.c:1034 `{"dbonly", no_argument, 0, OP_DBONLY}`; enum src/pacman/conf.h:180.

Conversely `--noscriptlet` (OP_NOSCRIPTLET, pacman.c:728-729) sets ONLY ALPM_TRANS_FLAG_NOSCRIPTLET; it does NOT set NOHOOKS. Hooks still run under --noscriptlet.

## Which operations accept it
parsearg_trans is called from parsearg_remove (pacman.c:761, -R), parsearg_upgrade (804, -U), parsearg_files (847, -F), and parsearg_sync (885) which calls parsearg_upgrade (-S). Dispatch: pacman.c:1088 (remove), 1091 (sync), 1094 (upgrade), 1097 (files). So `--dbonly` is parsed for -R, -S, -U (and -F, which opens no transaction). Not parsed for -D/-Q/-T.

Flag reaches libalpm only where `config->flags` is passed: src/pacman/remove.c:90, sync.c:710, upgrade.c:97 (`trans_init(config->flags, ...)` -> util.c:89 `alpm_trans_init(config->handle, flags)` -> trans.c:61 `trans->flags = flags`). Callers passing literal 0 (cannot carry NOHOOKS): src/pacman/sync.c:910 (-Sc clean), src/pacman/database.c:64 (-D). alpm_trans_init is called from exactly one place in the tree (util.c:89).

## Other conditions: none
- `config->flags |=` sites in pacman.c: 565,568 (ALLDEPS/ALLEXPLICIT, -D), 715/717 (NODEPS/NODEPVERSION), 721-723 (DBONLY/NOSCRIPTLET/NOHOOKS), 729, 767 (CASCADE), 771 (NOSAVE), 776/778 (RECURSE*), 783 (UNNEEDED), 812/815/818, 829-830 (DOWNLOADONLY, NOCONFLICTS), 1297-1298 (`--print`: NOCONFLICTS, NOLOCK). Only 723 is NOHOOKS. `--print` does NOT set NOHOOKS.
- No pacman.conf key sets it: grep of src/pacman/conf.c for config->flags returned nothing (only `HookDir`, conf.c:666-675, 947-948, which adds hook dirs, not disables).
- libalpm itself never sets it: grep `NOHOOKS|hook_run` lib/libalpm/*.c shows only trans.c:201/237 consuming, hook.c:507/532 defining `_alpm_hook_run*`.
- pacman.8.asciidoc has no NOHOOKS/“disable hooks” option: its only hook mentions are `--hookdir` (doc/pacman.8.asciidoc:177-180) and the see-also (592). The `--dbonly` entry (doc/pacman.8.asciidoc:235-236) reads "Adds/removes the database entry only, leaving all files in place." — the manual does NOT document that --dbonly skips hooks; only source + commit message do. `-h` text for -R/-S/-U: pacman.c:204 "--dbonly only modify database entries, not package files" (also silent).
- Provenance: `git log -S ALPM_TRANS_FLAG_NOHOOKS` -> be76f8bf "libalpm: add ALPM_TRANS_FLAG_NOHOOKS" and 165e4924 "pacman: don't run hooks when using --dbonly". Commit 165e4924 body quote: "--dbonly is meant to only touch the database and not the actual system. However hooks still run" (Allan McRae).

## What the flag suppresses (effect, for HO5 text)
lib/libalpm/trans.c, inside alpm_trans_commit (starts :167):
- :201-204 `if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS) && _alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(... ALPM_ERR_TRANS_HOOK_FAILED ...)}` — PreTransaction hooks skipped (and thus can't abort).
- :237-239 `if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS)) { _alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION); }` — PostTransaction skipped. This sits in the else branch of `if(trans->state == STATE_INTERRUPTED)` (:~232-240 region), i.e. only on a completed transaction.
- Both are the only hook_run call sites in libalpm; there is no per-hook or per-When partial suppression. Note both are reached only after the "nothing to do" early return (trans.c:~182-184 `if(trans->add == NULL && trans->remove == NULL) return 0;`) — so empty transactions run no hooks regardless of the flag; and `--print`/download-only paths that return from prepare/commit early never reach 201.

## Proposed replacement text for HO5's [unk]
"ALPM_TRANS_FLAG_NOHOOKS is set by exactly one pacman option: `--dbonly` (-R, -S, -U; src/pacman/pacman.c:720-723, which also sets DBONLY and NOSCRIPTLET). `--noscriptlet`, `--print`, and pacman.conf keys do not set it; libalpm never sets it (grep over 54d9411). With the flag, trans.c:201 and trans.c:237 skip every PreTransaction and PostTransaction hook; the man page (doc/pacman.8.asciidoc:235) does not document this." 

## Not done
- No runtime test of `pacman --dbonly` (host-mutating; none run). Claim rests on 54d9411 source only; the host's installed pacman version was not compared to 54d9411 by me.
- Did not check the lib `alpm_trans_get_flags` consumers elsewhere (e.g. AUR helpers) — outside scope.
- pacman.8 wording quote (<=25 words, doc/pacman.8.asciidoc:235-236, accessed 2026-10-26): "Adds/removes the database entry only, leaving all files in place."
- Source quote (src/pacman/pacman.c:720-723, 54d9411, accessed 2026-10-26): "case OP_DBONLY: ... config->flags |= ALPM_TRANS_FLAG_NOHOOKS;"

Scratch /fast/scratch/hyaku/tsukuroi-r38/C2ScoutNohooks/ removed at end (receipt = the commands above; HEAD hash recorded). No tools installed.
