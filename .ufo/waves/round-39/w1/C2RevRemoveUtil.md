VERDICT: supports

# C2-4 — TO7/TO8 re-opened against live source, pacman 54d9411

Fetched 2026-10-26 from `https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/<file>` into scratch, receipts copied to `.ufo/waves/round-39/w1/C2RevRemoveUtil/src/`.

## Source identity (sha256 check)

`sha256sum` on the live downloads vs `.ufo/waves/round-39/frozen/src/SHA256SUMS` — all six match byte-for-byte:

- remove.c `a052d455f088f34bf1d713a434957de7e1b9322862a07b69160c65ee15dca314` — match
- util.c `381618b6054859ec76807956328b78b330237273bebe10022a559b243cb5bdd2` — match
- add.c `fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1` — match
- hook.c `99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a` — match
- sync.c `6b297364eaba94e82a1e30b50dde9b3b96f88075855b66ff455aca1e24995d46` — match
- trans.c `637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07` — match

Judgments below are therefore against the same bytes as the frozen snapshot and the doc's S215/S216 rows (corpus/knowledge/pacman-transaction-order-r39.md:30-31).

## TO7 — removal order; old half of an upgrade gets neither scriptlet nor `removed` line

Row: corpus/knowledge/pacman-transaction-order-r39.md:30 (S215 remove.c:699-733).

**Order holds.** Inside `_alpm_remove_single_package` (remove.c:685), for a true removal (`newpkg == NULL`), in program order:

1. `pre_remove` scriptlet: remove.c:711 `_alpm_runscriptlet(handle, scriptlet, "pre_remove", pkgver, NULL, 0);` (gated on `alpm_pkg_has_scriptlet` and not `ALPM_TRANS_FLAG_NOSCRIPTLET`, remove.c:707-709)
2. file removal: remove.c:716-718 `remove_package_files(...)` (skipped only under `ALPM_TRANS_FLAG_DBONLY`)
3. `removed %s (%s)`: remove.c:721-724, `alpm_logaction(handle, ALPM_CALLER_PREFIX, ...)`, version string at :722
4. `post_remove`: remove.c:731, same gates (:727-730)

**Old half of an upgrade holds.** The `newpkg` non-NULL branch (remove.c:698-700) emits only `ALPM_LOG_DEBUG "removing old package first (%s-%s)"` — a debug line, no scriptlet, no `removed`. Every user-visible emission is `!newpkg`-gated: `pre_remove` :711 sits in the else-branch of :698; `removed` :721-724; `post_remove` :726-733.

**Caller with `newpkg` set.** add.c:485, inside `commit_single_pkg` (add.c:415):

```
if(oldpkg) {
    /* set up fake remove transaction */
    if(_alpm_remove_single_package(handle, oldpkg, newpkg, 0, 0) == -1) {
```

— the add/upgrade commit path; the old version's files are removed with `newpkg` set, so neither scriptlet nor `removed` fires. The only other caller is `_alpm_remove_packages` (remove.c:781), which passes `NULL` for every `trans->remove` target — used by remove transactions (trans.c:213) and the sync-commit removal phase (sync.c:1345), consistent with the doc's step-4 line (pacman-transaction-order-r39.md:38).

**Quote-at-lines:** the doc's S215 quote `_alpm_runscriptlet(handle, scriptlet, "pre_remove", pkgver, NULL, 0);` is at remove.c:711, inside the cited range 699-733; `removed %s (%s)` at :722; `post_remove` at :731 — all as cited.

## TO8 — every chroot child's output line logged under ALPM-SCRIPTLET

Row: corpus/knowledge/pacman-transaction-order-r39.md:31 (S216 util.c:521-528; hooks S208 hook.c:525-528).

**Chain holds.**

- `_alpm_chroot_process_output` (util.c:521-529): every line → `alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);` util.c:527, plus an `ALPM_EVENT_SCRIPTLET_INFO` event :528.
- `_alpm_chroot_read_from_child` (util.c:531) routes all four line-emission paths through it: each complete line :544; buffer-full forced flush :553-554; EOF flush of a trailing partial line :559-561; read-error flush :569-570. No path drops a line unlogged.
- `_alpm_run_chroot` (util.c:610): the child dup2's **both stdout and stderr** onto the captured socket (`dup2(child2parent_pipefd[HEAD], 1)` util.c:666, `..., 2)` :667); the parent's poll loop drains it via `_alpm_chroot_read_from_child` at util.c:740; any residual buffer is flushed via `_alpm_chroot_process_output` at util.c:762-763.

**Is ldconfig routed there? Yes.** `_alpm_ldconfig` (util.c:820-835) calls `_alpm_run_chroot(handle, LDCONFIG, argv, NULL, NULL)` at util.c:833, so ldconfig's output gets the same `ALPM-SCRIPTLET` tag — the tag does not mean "install scriptlet".

**Completeness of the funnel.** `_alpm_run_chroot` has exactly three call sites in libalpm at 54d9411, covering all three command classes the row names:

- hooks: hook.c:525-526 and :528 in `_alpm_hook_run_hook` (hook.c:504), both the `needs_targets` and plain branches — matches the cited S208 hook.c:525-528 exactly.
- install/remove scriptlets: trans.c:410 inside `_alpm_runscriptlet` (trans.c:337). Note for the record: there is no `lib/libalpm/scriptlet.c` at 54d9411 — the raw URL 404s and the GitLab tree listing (receipt `libalpm-tree-54d9411.json`, 62 files) has no such entry; scriptlet execution lives in trans.c at this pin.
- ldconfig: util.c:833.

util.c's sandbox code (util.c:964 `_alpm_use_sandbox`) is download-directory staging only, not an alternate execution path for these commands — no bypass of the tag.

**Quote-at-lines:** the doc's S216 quote `alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);` is at util.c:527, inside the cited 521-528 — as cited.

## Not done / residual

- Static source judgment only: no pacman run, no log-capture recount. The capture-side counts in the rows' right columns (28 `removed` lines; 252 of 441 `[ALPM-SCRIPTLET]` lines outside commit phases) were not recomputed by this seat — that is the counter's check, and I did not run tools/check-transaction-order-r39.py.
- `SCRIPTLET_SHELL` and `LDCONFIG` macro values were not opened (defined outside the fetched files); the routing verdict does not depend on their values.
- Judged only TO7 and TO8 (this seat's item); no other TO row reviewed.

TO7: holds — lib/libalpm/remove.c:698-733 (caller with newpkg set: lib/libalpm/add.c:485)
TO8: holds — lib/libalpm/util.c:521-528 (chain util.c:610→531→527; all chroot callers hook.c:525-528, trans.c:410, util.c:833)
