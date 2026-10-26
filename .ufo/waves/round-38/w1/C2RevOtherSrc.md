VERDICT: defect-found

Seat C2RevOtherSrc, item C2-4 (round 38, tsukuroi lane). Re-opened S209-S211 at pacman 54d9411 on
2026-10-26 (this seat's fetch 04:41-04:57Z). All three sha256 match `.ufo/waves/round-38/sources/SHA256SUMS`
and the frozen snapshots. One minor defect found: the S210 anchor cell names `_alpm_trans_commit`, a symbol
that does not exist at 54d9411 — the function is `alpm_trans_commit` (trans.c:167). Everything else in the
S209-S211 rows (anchors, teaches cells) and the HO2/HO5/HO6 citations holds. Proposed fix in §4. No lane
file was edited (read-only seat). No tools installed; only curl (already present) was used.

## 1. Re-open and hashes (access date 2026-10-26)

Fetched with `curl -fsSL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/<path>` into scratch
`/fast/scratch/hyaku/tsukuroi-r38/C2RevOtherSrc/` (copies kept as receipts in this seat dir):

    $ sha256sum alpm-hooks.5.asciidoc trans.c alpm.c
    2970cb35115a32a5d8a9652dfd795ad535d9354c36039fcc0d25929d9c3493d3  alpm-hooks.5.asciidoc
    637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07  trans.c
    8bbb0a3c90f23d8904a78faaf907a645e9329ddd05652c2b410d695f18f0834a  alpm.c

All three equal SHA256SUMS lines 3-5 and the frozen lane copies: `sha256sum` over
`.ufo/waves/round-38/sources/{hook.c,alpm-hooks.5.asciidoc,trans.c,alpm.c}` reproduced all four digests
including hook.c `99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a`.
Note: the first fetch of alpm-hooks.5.asciidoc returned `curl: (22) ... 404` (transient); an immediate
retry succeeded with the matching digest. Also fetched, unpinned: `error.c` (03f2dd96…) and `handle.c`,
used only to confirm the quoted error string and the hookdir append order.

## 2. SOURCES.md rows S209-S211 (corpus/SOURCES.md:218-220)

### S209 (:218) — alpm-hooks.5.asciidoc — HOLDS
- Anchor "DESCRIPTION lines 34-39": DESCRIPTION heading at :27-28; the hooks-read/run paragraph is
  :35-39 (:34 blank); run-order sentence :38-39 "Hooks are run in alphabetical order of their file
  name, where the ordering ignores the suffix." (16 words). Range bounds the paragraph. VERIFIED.
- Anchor "AbortOnFail lines 87-89": exact — :87 `*AbortOnFail*::`; :88-89 "Causes the transaction to
  be aborted if the hook exits non-zero. Only applies to PreTransaction hooks." (16 words). VERIFIED.
- Teaches cell "The manual states the suffix-ignoring alphabetical order the code implements, so S208
  and S209 agree": manual :38-39 above; code side `_alpm_hook_cmp` hook.c:443-455 — :449
  `/* exclude the suffixes from comparison */`, :450 `ret = strncmp(h1->name, h2->name, l1 <= l2 ? l1 : l2);`,
  :451-452 shorter name first on a tie. Agreement holds. VERIFIED.

### S210 (:219) — trans.c — DEFECT (anchor name only), substance HOLDS
- Anchor "`_alpm_trans_commit` lines 201-240": the line range is correct and sits inside the commit
  function, but the function is `alpm_trans_commit` — trans.c:167 `int SYMEXPORT
  alpm_trans_commit(alpm_handle_t *handle, alpm_list_t **data)`; `grep -n '_alpm_trans_commit' trans.c`
  returns nothing. DEFECT: spurious leading underscore in the anchor's function name.
- Teaches cell "A Pre-phase error stops the transaction before it starts, and Post hooks run only
  after a completed commit with their result ignored": trans.c:201-204 Pre-hook failure →
  `RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1)` returns before `STATE_COMMITTING` (:206) and the
  "transaction started" log (:208); :212-228 failed commit paths return -1 with no post hooks;
  :230-231 interrupted branch runs none; :235 `"transaction completed"` then :237-239
  `_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION);` with the return value discarded. VERIFIED.

### S211 (:220) — alpm.c — HOLDS
- Anchor "`alpm_initialize` lines 56-62": signature alpm.c:37-38 `alpm_handle_t SYMEXPORT
  *alpm_initialize(const char *root, const char *dbpath, alpm_errno_t *err)`; :62
  `myhandle->hookdirs = alpm_list_add(NULL, hookdir);` — the system dir is the list head. VERIFIED.
- Teaches cell "The system hook directory is the list head, so HookDir entries searched first
  override it": alpm.c:62 (head) + handle.c:475 `handle->hookdirs = alpm_list_add(handle->hookdirs,
  newhookdir);` (HookDir appended after the head) + hook.c:540 walk last→first + :588-590 first seen
  wins. VERIFIED.

## 3. HO2/HO5/HO6 citations (corpus/knowledge/pacman-hook-order-r38.md:22,25,26)

### HO2 (:22) — HOLDS
- "Directories are searched from the last list entry to the first": hook.c:540
  `for(i = alpm_list_last(handle->hookdirs); i; i = alpm_list_previous(i)) {`. VERIFIED.
- "the first file seen for a name wins and later same-name files are skipped": hook.c:588-590
  `if(find_hook(hooks, entry->d_name)) {` … `"skipping overridden hook %s\n"` … `continue;`. VERIFIED.
- "The system directory is the list head; `HookDir` entries follow it": cited S211 alpm.c:56-62 →
  alpm.c:62; HookDir appended after the head at handle.c:475. S007 exists (corpus/SOURCES.md:13,
  "Later HookDir directories take precedence"). The etc-overrides-usr host consequence follows. VERIFIED.

### HO5 (:25) — HOLDS
- "fails to parse or validate … return an error before any Pre hook runs": hook.c:609-614
  `if(parse_ini(path, _alpm_hook_parse_cb, &ctx) != 0 || _alpm_hook_validate(handle, ctx.hook, path)) {`
  … `ret = -1; continue;`; hook.c:629-631 `if(ret != 0 && when == ALPM_HOOK_PRE_TRANSACTION) { goto cleanup; }`
  — the sort (:633-634) and the run loop come after, so no Pre hook has run. VERIFIED.
- "`trans.c` turns it into `ALPM_ERR_TRANS_HOOK_FAILED`": trans.c:201-204 (cited) `RET_ERR(handle,
  ALPM_ERR_TRANS_HOOK_FAILED, -1)`; quoted string exact — error.c:105-106 `case
  ALPM_ERR_TRANS_HOOK_FAILED:` / `return _("failed to run transaction hooks");` (5 words). VERIFIED.
- "(no Exec, no When, bad trigger)" grounded in S209: :44 "Hooks must contain at least one
  '[Trigger]' section" (8 words); :76-78 `*Exec =* <command>::` … "Required."; :80-81 `*When =* …`
  "Required.". VERIFIED.
- "A transaction flagged `ALPM_TRANS_FLAG_NOHOOKS` skips both phases (`trans.c:201`, `:237`)": :201
  `if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS) &&`, :237 `if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS)) {`.
  VERIFIED.

### HO6 (:26) — HOLDS
- Cited S210 trans.c:212-240: failed commit :212-228 returns -1 (no post hooks); interrupted
  :230-231 `"transaction interrupted"` branch runs none; :235 `"transaction completed"` precedes
  :237-239 post-hook run; post-hook failure ignored (:238 return value discarded). VERIFIED.

## 4. Proposed exact text (corpus/SOURCES.md:219, anchor cell only)

Replace:
    `_alpm_trans_commit` lines 201-240
with:
    `alpm_trans_commit` lines 201-240

Read-only seat: not applied by me. No other text in S209-S211 or HO2/HO5/HO6 needs a change.

## 5. Not done
- Did not re-run `tools/check-hook-order-r38.py` or any counter (other seats own it; not in this item).
- Did not verify the S208 row itself or HO1/HO3/HO4/HO7 rows (other seats' items); hook.c lines
  443-455, 540, 588-590, 609-614, 629-631 were read only as citation targets of HO2/HO5 and the S209
  teaches cell.
- Did not execute pacman, did not touch the host, did not reset any counter.

## HO rows judged (per pre-seat amendment)

HO2: holds — lib/libalpm/hook.c:540,588-590; lib/libalpm/alpm.c:62 (handle.c:475)
HO5: holds — lib/libalpm/hook.c:609-614,629-631; lib/libalpm/trans.c:201-204 (error.c:105-106)
HO6: holds — lib/libalpm/trans.c:212-240
