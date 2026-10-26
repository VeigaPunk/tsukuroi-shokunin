VERDICT: supports

Item C2-EX7 — row EX7 of corpus/knowledge/pacman-exec-environment-r40.md, judged at lane tip
f951f288483c1af0cef4afd458488b84cf7a2165 (HEAD == f951f288483c1af0cef4afd458488b84cf7a2165;
`git diff --stat f951f288483c1af0cef4afd458488b84cf7a2165 -- corpus/knowledge/pacman-exec-environment-r40.md`
empty, exit 0 — the judged row is the dispatch revision's row).

Row verdict: **holds**. Every clause of the rule is stated by the pinned source at the cited
lines; the source-cell quote and the value cell are verbatim; the host cell reproduces. No
correction text proposed (verdict is `holds`, so the append-only-correction branch does not apply).

## Pin and re-fetch integrity

- Frozen pin intact: `sha256sum -c .ufo/waves/round-40/frozen/src/SHA256SUMS` → all six OK
  (hook.c 99f1044badd3…, alpm-hooks.5.asciidoc 2970cb35115a…, trans.c 637c1165790d…,
  util.c 381618b60548…, meson_options.txt 89e5b350af28…, PKGBUILD 32d40dfd3691…).
- Upstream re-opened by this seat (access 2026-10-26T07:15:31Z–07:15:36Z): hook.c/trans.c/util.c
  from https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/<file>,
  alpm-hooks.5.asciidoc and meson_options.txt from …/-/raw/54d9411/…, PKGBUILD from
  https://gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/raw/7.1.0.r9.g54d9411-3/PKGBUILD.
  All six fetched sha256 values equal the SHA256SUMS values (receipt:
  .ufo/waves/round-40/w1/C2RevEX7/receipts.md).
- SOURCES cross-ref: corpus/SOURCES.md:232 (S223, hook.c @54d9411, snapshot sha256 99f1044b…)
  and :233 (S224, alpm-hooks.5.asciidoc @54d9411, snapshot sha256 2970cb35…) — both match.

## Clause-by-clause judgment of the rule

Rule text (verbatim from the row): "The `running '<name>'...` log line is written before the
hook's `Depends` are checked; when an installed package satisfying a listed `Depends` is
missing, libalpm logs `unable to run hook <name>: … satisfy dependencies` and skips the
command, and that failure stops the PreTransaction phase, and with it the transaction, only
for a hook carrying `AbortOnFail`"

1. "The `running '<name>'...` log line is written before the hook's `Depends` are checked" — **holds**.
   hook.c:653 `alpm_logaction(handle, ALPM_CALLER_PREFIX, "running '%s'...\n", hook->name);`
   precedes the only call of `_alpm_hook_run_hook` at hook.c:660 (definition hook.c:507; grep
   over the file shows exactly two occurrences of the symbol, :507 and :660 — no earlier path
   reaches the check). The Depends check is the callee's first loop, hook.c:511-517
   (`for(i = hook->depends; i; i = i->next) { if(!alpm_find_satisfier(pkgs, i->data)) …`).
   `hook->depends` is otherwise only stored at parse time (hook.c:229) and freed (:82) — no
   earlier check exists.

2. "when an installed package satisfying a listed `Depends` is missing, libalpm logs
   `unable to run hook <name>: … satisfy dependencies` and skips the command" — **holds**.
   hook.c:511-515: on `!alpm_find_satisfier(pkgs, i->data)` libalpm emits
   `_alpm_log(handle, ALPM_LOG_ERROR, _("unable to run hook %s: %s\n"), hook->name,
   _("could not satisfy dependencies"));` (:513-514) and `return -1;` (:515) — the
   `_alpm_run_chroot` calls (:525/:528) are never reached, so the hook's Exec is skipped.
   `pkgs` is `_alpm_db_get_pkgcache(handle->db_local)` (:509), i.e. installed packages;
   `alpm_find_satisfier` (deps.c:289-296, supplementary fetch, sha256 e42e6c015dbe…) resolves
   through `find_dep_satisfier` → `_alpm_depcmp(pkg, dep)` (deps.c:86-95), so the satisfier is
   an installed package matching by name or provision — the rule's "an installed package
   satisfying" is accurate, not an overstatement. Rendered text is
   `unable to run hook <name>: could not satisfy dependencies`; the rule's `…` elides `could not `.

3. "that failure stops the PreTransaction phase … only for a hook carrying `AbortOnFail`" — **holds**.
   hook.c:660-662 `if(_alpm_hook_run_hook(handle, hook) != 0 && hook->abort_on_fail) { ret = -1; }`
   — the Depends failure (return -1) sets ret only when `hook->abort_on_fail` is set;
   hook.c:667-669 `if(ret != 0 && when == ALPM_HOOK_PRE_TRANSACTION) { break; }` — the break
   that skips the remaining hooks of the phase fires only for that ret, and only in the
   PreTransaction phase. Without `AbortOnFail` the failure logs and skips the command but the
   phase continues and ret stays 0.

4. "and with it the transaction" — **holds**. trans.c:201-204, inside `alpm_trans_commit`
   (trans.c:167): `if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS) &&
   _alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) { RET_ERR(handle,
   ALPM_ERR_TRANS_HOOK_FAILED, -1); }` — the commit fails before
   `trans->state = STATE_COMMITTING` (trans.c:206) and before the "transaction started"
   logaction, i.e. before any package change. The PostTransaction run (trans.c:237-239)
   ignores the return value, consistent with the rule's PreTransaction-only scoping.

5. Man page grounding — **holds**. alpm-hooks.5.asciidoc:83-85: `*Depends =* <package>:: /
   Packages that must be installed for the hook to run. May be specified / multiple times.` —
   matches the row's citation :83-85. :87-89: `*AbortOnFail*:: Causes the transaction to be
   aborted if the hook exits non-zero.  Only applies to PreTransaction hooks.` corroborates
   clause 3's scoping. Nuance, not a row defect: the man page says "exits non-zero", while the
   code also aborts when the hook fails pre-execution on unmet Depends (hook.c:515 returns
   before any command runs). The row cites hook.c:660-668 for the abort behavior and cites the
   man page only for `Depends` documentation, so the rule does not inherit the narrower wording.

## Quote, value and host cells

- Source-cell quote `_("unable to run hook %s: %s\n"), hook->name, _("could not satisfy
  dependencies"));` — byte-verified verbatim, joined across hook.c:513-514 (the join replaces
  the 513→514 newline+indent with a space; the leading `_alpm_log(handle, ALPM_LOG_ERROR, `
  is outside the quote). The row's cited range :507-517 contains both lines. Check output:
  `QUOTE-VERBATIM-AT-513-514` (receipt file).
- Value cell `could not satisfy dependencies` — verbatim at hook.c:514.
- Source-cell parentheticals all exact: `running` logged :653; `_alpm_hook_run_hook` :660;
  abort :660-668 (ret=-1 :660-662, break :667-668).
- Host cell: `grep -c 'could not satisfy dependencies' /var/log/pacman.log` → `0` (grep exit 1),
  rerun by this seat 2026-10-26 — "the live log holds 0 such errors" reproduces. "A `running`
  line in `pacman.log` proves the hook was selected" is grounded: the logaction (:653) runs for
  every entry of `hooks_triggered`, built from trigger matches (hook.c:636-642), before the
  Depends check; "its command may still have been skipped" per clause 2. Additional grounding
  for the asymmetry the cell relies on: `running` reaches pacman.log via `alpm_logaction`
  (hook.c:653 → log.c:45), while the Depends error goes through `_alpm_log` (hook.c:513 →
  log.c:101-112) to the frontend callback only — pacman's `cb_log` (callback.c:1139-1156,
  supplementary fetch, sha256 9dadcc564658…) writes to stderr and never calls
  `alpm_logaction`, so the error text is not expected in pacman.log; the row does not claim it
  is, and the 0-count observation stands either way.

## Not done

- No live transaction was run to observe the behavior at runtime: pacman transactions are
  paused host-wide and the row is source-level by design (its Boundaries section says so).
  The host-side check performed is the pacman.log grep above.
- deps.c, log.c and callback.c are supplementary fetches, not among the row's pinned sources;
  they were used only to confirm satisfier semantics and the log-surface asymmetry.

## Proposed correction text

None — verdict is `holds`; every clause is stated by the pinned source at the cited lines,
the quote and value cell are verbatim, and the host cell reproduces.
