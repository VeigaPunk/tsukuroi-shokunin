VERDICT: supports

Seat C2RevHookC — item C2-3: S208 (`lib/libalpm/hook.c` at pacman `54d9411`) re-opened live 2026-10-26; every `hook.c` citation of `corpus/knowledge/pacman-hook-order-r38.md` checked against the fetched bytes.

## 1. Live re-open of S208

- URL: https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/hook.c — accessed 2026-10-26, fetched 04:56 UTC.
- Command: `curl -fsSL --retry 3 '<URL>' -o "$S/hook.c"` → exit 0; `sha256sum` → `99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a`; `wc -l` → `683 hook.c`.
- Expected `99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a` → **MATCH**.
- Cross-check: `.ufo/waves/round-38/sources/SHA256SUMS:2` records the identical hash for `hook.c` (header `:1`: fetched 2026-10-26T04:20:21Z from the same URL). Two independent fetches agree byte-for-byte.
- Receipt: fetched copy kept at `.ufo/waves/round-38/w1/C2RevHookC/hook.c` (sha256 re-verified after copy; commands and outputs in `receipts.txt` beside it). All line numbers below are from that copy, which is byte-identical to the pinned snapshot.

## 2. Row-by-row citation audit (quotes verbatim from the fetched hook.c)

### HO1 — cites `hook.c:443-455`, key `:449` — AGREE
- :447-448 `l1 = strlen(h1->name) - suflen;` / `l2 = strlen(h2->name) - suflen;`
- :449 `/* exclude the suffixes from comparison */`
- :450 `ret = strncmp(h1->name, h2->name, l1 <= l2 ? l1 : l2);`
- :451-452 `if(ret == 0 && l1 != l2) {` / `return l1 < l2 ? -1 : 1;`
- Says exactly the row: order by file name minus the `.hook` suffix, bytewise (`strncmp` compares unsigned chars) over the shorter length; on a tie the shorter name sorts first. This comparator is the sort key at :633-634 (`alpm_list_msort(hooks, alpm_list_count(hooks), (alpm_list_fn_cmp)_alpm_hook_cmp)`).
- Consequence arithmetic: `printf 'ascii dash=%d dot=%d\n' "'-" "'."` → `ascii dash=45 dot=46`, so a plain full-name byte sort does place `fontconfig-32.hook` before `fontconfig.hook` (and the two gio pairs likewise), reversing all three pairs exactly as the row's last clause states.

### HO2 — cites `hook.c:540`, `:588-590` — AGREE on both hook.c citations
- :540 `for(i = alpm_list_last(handle->hookdirs); i; i = alpm_list_previous(i)) {` — the walk starts at the LAST list entry and moves backwards: directories are searched from the last list entry to the first. ✓
- :588-590 `if(find_hook(hooks, entry->d_name)) {` / `_alpm_log(handle, ALPM_LOG_DEBUG, "skipping overridden hook %s\n", path);` / `continue;` — the first file seen for a name wins; later same-name files are skipped. ✓
- Scope note: the row's clause "The system directory is the list head; `HookDir` entries follow it" is cited to S211 `alpm.c:56-62`, not to hook.c — not re-opened by this seat (other seat's item). hook.c:540 is what makes that list order decisive for which file wins.

### HO3 — cites `hook.c:118-122` — AGREE on substance; citation window off by one (minor finding, see §3)
- Actual block: :119 `if(hook->triggers == NULL) {`, :120-121 `/* special case: allow triggerless hooks as a way of creating dummy` / ` * hooks that can be used to mask lower priority hooks */`, :122 `return 0;`, :123 `}`. Line 118 is blank.
- The code inside the cited window says exactly what the row says: a triggerless hook is valid (`return 0`) and the comment names masking lower-priority hooks verbatim — "the supported way to mask a lower priority hook".
- "Never runs" is supported outside the cited window: :638 gates running on `_alpm_hook_triggered(handle, hook)`, and `_alpm_hook_triggered` (:427-441) returns 0 when the trigger list is empty (:429-430 declare `ret = 0` and the loop over `hook->triggers` never executes).

### HO4 — cites `hook.c:660-669` — AGREE
- :660-662 `if(_alpm_hook_run_hook(handle, hook) != 0 && hook->abort_on_fail) {` / `ret = -1;` / `}` — a hook's non-zero exit marks the phase failed only when the hook carries `AbortOnFail`. ✓
- :667-669 `if(ret != 0 && when == ALPM_HOOK_PRE_TRANSACTION) {` / `break;` / `}` — the remaining Pre hooks are then skipped. ✓
- (The transaction-level effect of `ret` is trans.c, S210 — other seat's scope.)

### HO5 — cites `hook.c:609-614`, `:629-631` — AGREE on both hook.c citations
- :609-614 `if(parse_ini(path, _alpm_hook_parse_cb, &ctx) != 0` / `|| _alpm_hook_validate(handle, ctx.hook, path)) {` / `_alpm_log(handle, ALPM_LOG_DEBUG, "parsing hook file %s failed\n", path);` / `_alpm_hook_free(ctx.hook);` / `ret = -1;` / `continue;` — any parse or validate failure in any searched hookdir marks the phase failed. ✓
- :629-631 `if(ret != 0 && when == ALPM_HOOK_PRE_TRANSACTION) {` / `goto cleanup;` / `}` — taken before the sort (:633) and before any hook is selected or run: the Pre phase returns an error before any Pre hook runs. ✓
- The row's "(no Exec, no When, bad trigger)" enumerates exactly `_alpm_hook_validate`'s three failure modes: bad trigger :125-129 (`_alpm_trigger_validate(handle, i->data, file) != 0` → `ret = -1`), Missing Exec :131-135 (`hook->cmd == NULL` → :134 `_("Missing Exec option in hook: %s\n")`), Missing When :137-140 (`hook->when == 0` → :140 `_("Missing When option in hook: %s\n")`).
- Scope note: "trans.c turns it into `ALPM_ERR_TRANS_HOOK_FAILED` … and the transaction never starts" is S210 `trans.c:201-204` — not re-opened by this seat.

### HO7 — cites `hook.c:636-641` — AGREE
- :632-634 `hooks = alpm_list_msort(hooks, alpm_list_count(hooks),` / `(alpm_list_fn_cmp)_alpm_hook_cmp);` — candidates sorted in the HO1 order.
- :636-641 `for(i = hooks; i; i = i->next) {` / `struct _alpm_hook_t *hook = i->data;` / `if(hook && hook->when == when && _alpm_hook_triggered(handle, hook)) {` / `hooks_triggered = alpm_list_add(hooks_triggered, hook);` / `triggered++;` / `}` — only hooks of this phase whose triggers matched are kept, appended in the already-sorted order.
- The run loop then iterates `hooks_triggered` only (:651 `for(i = hooks_triggered; i; i = i->next, hook_event.position++) {`), logging `running '%s'...\n` per hook (:653) — matching the row and the pacman.log-oracle consequence.

## 3. Findings

1. (minor, cosmetic) `corpus/knowledge/pacman-hook-order-r38.md:23` cites HO3 as `hook.c:118-122`; the triggerless-mask block is `hook.c:119-123` (line 118 is blank; the closing brace at 123 falls outside the window). All substantive lines (119-122) lie inside the cited window, so the row is not misled and the rule holds. If the corpus is ever unfrozen: change to `hook.c:119-123`.
2. No other imprecision: HO1 (:443-455, key :449), HO2 (:540, :588-590), HO4 (:660-669), HO5 (:609-614, :629-631), HO7 (:636-641) anchor the exact code quoted above.

## 4. Not done / scope

- S209 `alpm-hooks.5.asciidoc`, S210 `trans.c`, S211 `alpm.c` citations were not re-opened (this item lists hook.c citations only; other seats cover the other sources). HO6 (trans.c-only row) not judged here.
- No pacman execution, no host mutation, no lane mutation; read-only git queries only (`check-ignore`, `ls-files`). Nothing installed or upgraded.
- Scratch `/fast/scratch/hyaku/tsukuroi-r38/C2RevHookC/` removed after receipts were copied.

## 5. Per-row verdicts (pre-seat amendment format)

HO1: holds — hook.c:443-455
HO2: holds — hook.c:540,588-590
HO3: holds — hook.c:119-123
HO4: holds — hook.c:660-669
HO5: holds — hook.c:609-614,629-631
HO7: holds — hook.c:636-641
