VERDICT: supports

Item C2-5 — judge TO5 of corpus/knowledge/pacman-transaction-order-r39.md (row at :28, file last committed at declared 4078eb236c7c67f343c76956c587d0a356e0bf5c, `git status --porcelain` on the file: 0 dirty lines) against live pacman 54d9411 lib/libalpm/hook.c.

## Source identity
- Live refetch, access date 2026-10-26:
  `curl -fsSL --retry 2 'https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/hook.c' -o $S/hook.c && sha256sum $S/hook.c && diff -q $S/hook.c .ufo/waves/round-39/frozen/src/hook.c && echo LIVE==FROZEN`
  → `99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a`, `LIVE==FROZEN`, 683 lines. Matches the assignment prefix `99f1044b…` and the frozen SHA256SUMS line for hook.c (.ufo/waves/round-39/frozen/src/SHA256SUMS:2). Receipt: .ufo/waves/round-39/w1/C2RevHookC/hook.c
- Supplementary fetches (not pinned rows, used only for the handle-cache question): `alpm_handle.h` → HTTP 404 (no such path at 54d9411; the internal struct is handle.h); handle.h sha256 `dbbbd0e6c537f85c7157418baf18081482a3a436cdb33cfc8613b388cce24e93`; handle.c fetched live. Receipts: .ufo/waves/round-39/w1/C2RevHookC/{handle.h,handle.c}

## Quote-at-lines check (the row's cited evidence)
- TO5 cites S208 hook.c:532-560, quote `for(i = alpm_list_last(handle->hookdirs); i; i = alpm_list_previous(i)) {` with `opendir` :554 inside the loop.
- Verified verbatim by raw read of hook.c:532-560: the quoted line is exactly hook.c:540, and hook.c:554 is `if(!(d = opendir(path))) {`. Both inside the cited range. The quote is at the lines.

## Q1 — does _alpm_hook_run open and parse every hook directory on each call?
Yes. Function starts at hook.c:532 (`int _alpm_hook_run(alpm_handle_t *handle, alpm_hook_when_t when)`). On every invocation it walks `handle->hookdirs` (hook.c:540), `opendir`s each directory (hook.c:554; ENOENT → skip at :555-556), `readdir`s entries (hook.c:565), dedups by basename within the call only (`find_hook`, hook.c:588; helper :457), `stat`s the file (hook.c:593), parses it with `parse_ini(path, _alpm_hook_parse_cb, &ctx)` (hook.c:609), names the hook by basename (hook.c:617 `STRDUP(ctx.hook->name, entry->d_name, ...)`), and `closedir`s (hook.c:626). There is no early exit or memoization: each call repeats opendir→readdir→stat→parse_ini over every configured directory.

## Q2 — are Pre and Post separate calls?
Yes. Frozen trans.c (sha256 `637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07`, matches frozen SHA256SUMS) calls the same function twice with the whole commit between them:
- trans.c:202 `_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION)` — before `trans->state = STATE_COMMITTING` (:206) and `transaction started` (:208).
- trans.c:238 `_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION)` — after `transaction completed` (:235).
- The commit work sits strictly between the two calls: `_alpm_remove_packages` (trans.c:213) or `_alpm_sync_commit` (trans.c:221).
So Pre parses the on-disk hook files as they exist before the commit; Post re-parses whatever is on disk after it. The corollaries follow directly from the scan seeing disk state at call time: a hook first installed by this transaction is absent at the Pre scan (not a Pre candidate); a hook removed by this transaction is absent at the Post scan (not a Post candidate).

## Q3 — is 'an upgraded hook file runs old in Pre and new in Post' supported?
Yes. The file is replaced during the commit — extraction happens inside `_alpm_sync_commit` (trans.c:221), strictly between the Pre call (trans.c:202) and the Post call (trans.c:238). Each call reads content fresh from disk at scan time (`stat` hook.c:593, `parse_ini` hook.c:609); no parsed hook struct or file content survives a call — the collected `hooks` list is function-local (hook.c:536) and freed at `cleanup:` on every call (hook.c:679-680 `alpm_list_free_inner(hooks, (alpm_list_fn_free) _alpm_hook_free); alpm_list_free(hooks);`), including error paths via `goto cleanup` (hook.c:606, :617). Therefore Pre parses the old content and Post parses the new content of the same basename.

## Q4 — is anything cached across calls in the handle?
No. The internal struct `struct _alpm_handle_t` (live handle.h at 54d9411, sha256 `dbbbd0e6…`) contains exactly one hook-related field: `alpm_list_t *hookdirs; /* Paths to hook directories */` (handle.h:100). Full field list checked from struct open to close (ends `int lockfd; };`): config path/string lists, siglevels, `pm_errno`, `lockfd` — no hook list, no parse cache, no hash table. `handle->hookdirs` is written only by the option API (live handle.c: `alpm_list_add(handle->hookdirs, newhookdir)` :475, `alpm_option_set_hookdirs` :480-487, remove :507) and freed at teardown (handle.c:100 `FREELIST(handle->hookdirs)`); `_alpm_hook_run` only reads it. It is configuration, not a parse cache — the row's claim ("opens each hook directory anew") concerns `opendir`, which is per-call (hook.c:554).

## Caveats (not contradictions of TO5)
- If the Pre phase fails, Post never runs (trans.c:203 `RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1)`); an interrupted transaction skips Post (trans.c:230-232). Those are TO1/TO6/HO6 subjects.
- A hook file replaced *during* a single scan window (between `opendir` and `parse_ini` of one call) is outside the claim; the claim concerns replacement during the commit, which lies between the two calls.
- The hookdir *list* is pacman.conf configuration set via the option API, not re-read from pacman.conf per call; the row does not claim otherwise.
- Not done here: re-verifying the row's host-consequence column (the 17 PreTransaction hook files census), running the C2 counter, compiling or executing pacman.

## Tooling
- No tools installed or upgraded (curl, sha256sum, diff, grep, git already present). No pacman transactions run; no host mutation; scratch /fast/scratch/hyaku/tsukuroi-r39/C2RevHookC removed after receipts were copied.

TO5: holds — hook.c:540
