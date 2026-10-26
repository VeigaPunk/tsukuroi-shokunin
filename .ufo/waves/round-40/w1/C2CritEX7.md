VERDICT: defect-found

The three mechanisms the seat names hold in the pinned 54d9411 snapshot: the `running` line is written
before `Depends` is read (hook.c:653 versus :660 -> :511-517), a failing `AbortOnFail` hook sets `ret = -1`
in both phases but only the PreTransaction loop breaks (:660-662 versus :667-669), and the PostTransaction
caller discards the return (trans.c:237-239, then :242-244). The EX7 cell is nevertheless defective for its
stated audience — a hook author — in two places: it leaves a PostTransaction `AbortOnFail` hook reading as
supported when libalpm admits it, warns about it, runs it and throws its failure away; and "an installed
package satisfying a listed `Depends` is missing" describes the lookup in a way that hides that the lookup
reads the local database *before the commit starts*, so a `Depends` on a package the same transaction
installs fails for that transaction. Both are text-only, and the exact replacement row below scores PASS
under the unchanged frozen counter (8/8).

Evidence base: frozen snapshots `.ufo/waves/round-40/frozen/src/` verified against their own digests —

    $ sha256sum -c SHA256SUMS
    PKGBUILD: OK   alpm-hooks.5.asciidoc: OK   hook.c: OK   meson_options.txt: OK
    trans.c: OK    util.c: OK

All line numbers below are from those files (`hook.c` = lib/libalpm/hook.c, `trans.c` = lib/libalpm/trans.c).

## 1. Is the `running` line written for a hook whose `Depends` fail? Yes — order confirmed

hook.c:651-670, the triggered-hook loop:

    653  alpm_logaction(handle, ALPM_CALLER_PREFIX, "running '%s'...\n", hook->name);
    660  if(_alpm_hook_run_hook(handle, hook) != 0 && hook->abort_on_fail) {
    661      ret = -1;
    662  }

The `Depends` test is inside the callee, hook.c:507-517:

    509  alpm_list_t *i, *pkgs = _alpm_db_get_pkgcache(handle->db_local);
    511  for(i = hook->depends; i; i = i->next) {
    512      if(!alpm_find_satisfier(pkgs, i->data)) {
    513          _alpm_log(handle, ALPM_LOG_ERROR, _("unable to run hook %s: %s\n"),
    514                  hook->name, _("could not satisfy dependencies"));
    515          return -1;

So the sequence for an unsatisfiable `Depends` is: selection (`_alpm_hook_triggered`, :638) -> `running` log
(:653) -> HOOK_RUN_START event (:655-658) -> `Depends` loop -> error log (:513-514) -> `return -1` (:515)
-> HOOK_RUN_DONE event (:664-665). `_alpm_run_chroot` (:525-526 for `NeedsTargets`, :528 otherwise) is never
reached, so the command is skipped while a `running` line and a RUN_DONE event both exist. The cell's
ordering clause and the cell's consequence ("a `running` line proves the hook was selected, and its command
may still have been skipped") are therefore exactly right.

Host observation supporting the consequence column:

    $ grep -c 'could not satisfy dependencies' /var/log/pacman.log
    0                       # exit 1 (no match)
    $ grep -c "running '" /var/log/pacman.log
    295
    $ ls -l /var/log/pacman.log
    -rw-r--r-- 1 root root 252016 Oct 25 13:12 /var/log/pacman.log

295 `running` lines against 0 dependency errors is consistent with the cell and does not distinguish
selection from execution — which is precisely the cell's point. The frozen host value in the cell
("the live log holds 0 such errors") reproduces.

## 2. Both phases set `ret`; only the PreTransaction loop breaks

hook.c:660-662 has no `when` guard, so a PostTransaction hook with `AbortOnFail` that fails sets `ret = -1`
identically. The gate is only at the bottom of the loop:

    667  if(ret != 0 && when == ALPM_HOOK_PRE_TRANSACTION) {
    668      break;
    669  }

Consequences, both derived from those two lines and not stated anywhere in EX7:

- PreTransaction: `break` skips every remaining triggered pre-hook. Their `running` lines are never written
  and their commands never run, so an abort leaves a `running` trace that stops mid-phase.
- PostTransaction: no break, so the phase keeps running every remaining triggered post-hook after a failure,
  and `_alpm_hook_run` returns -1 at :682 regardless. The phase is best-effort.

## 3. What the Post-phase caller does with the return: discards it

trans.c:230-245:

    237  if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS)) {
    238      _alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION);
    239  }
    242  trans->state = STATE_COMMITTED;
    244  return 0;

The call at :238 is a bare statement: no comparison, no `RET_ERR`, no `pm_errno`. It runs after
`"transaction completed"` was logged (:235) and after the `STATE_INTERRUPTED` branch (:230-231) decided the
transaction went through. `alpm_trans_commit` then returns 0. `_alpm_hook_run` has exactly two callers in the
snapshot:

    $ grep -rn "_alpm_hook_run" *.c | grep -v "^hook.c:5[0-9][0-9]"
    hook.c:660:            if(_alpm_hook_run_hook(handle, hook) != 0 && hook->abort_on_fail) {
    trans.c:202:                   _alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) {
    trans.c:238:                   _alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION);

(First line is the inner per-hook call, `_alpm_hook_run_hook`, not the phase entry point.)
PreTransaction at :202 is checked and aborts the transaction at :203:

    201  if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS) &&
    202          _alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) {
    203      RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);
    206  trans->state = STATE_COMMITTING;

So a PostTransaction `AbortOnFail` failure is invisible to every caller of libalpm; its only trace is the
`ALPM_LOG_ERROR` line from hook.c:513-514. It cannot abort anything because the commit it would abort has
already returned from `_alpm_remove_packages`/`_alpm_sync_commit` (:212-228).

## 4. Validation does allow `AbortOnFail` on a Post hook — with a warning only

hook.c:113-147, `_alpm_hook_validate`:

    117  int ret = 0;
    119  if(hook->triggers == NULL) {
    120      /* special case: allow triggerless hooks as a way of creating dummy
    121       * hooks that can be used to mask lower priority hooks */
    122      return 0;
    123  }
    ...
    141  } else if(hook->when != ALPM_HOOK_PRE_TRANSACTION && hook->abort_on_fail) {
    142      _alpm_log(handle, ALPM_LOG_WARNING,
    143              _("AbortOnFail set for PostTransaction hook: %s\n"), file);
    144  }
    146  return ret;

`ret` is untouched by the :141-144 branch, so the hook is admitted and runs. Two details worth carrying:

- The branch is `else if` on `hook->when == 0` (:137-140), so a hook that is missing `When` gets the error
  and the warning is skipped; a hook that names `PostTransaction` gets the warning and stays valid.
- A triggerless hook returns 0 at :122 before reaching :141, so it gets no warning — and can never trigger
  either (`_alpm_hook_triggered`, :427-441, loops over an empty trigger list and returns 0), so the omission
  has no behavioural consequence.
- Because hook files are re-parsed in *each* phase (`_alpm_hook_run` at trans.c:202 and :238, validation at
  hook.c:609-610), an operator carrying such a hook sees this warning on both phases of every transaction
  that completes, i.e. twice per commit.

The man page states the intent the code declines to enforce — `alpm-hooks.5.asciidoc`:

    23  AbortOnFail (Optional, PreTransaction only)
    87  *AbortOnFail*::
    88      Causes the transaction to be aborted if the hook exits non-zero.  Only
    89      applies to PreTransaction hooks.

EX7 cites only :83-85 (the `Depends` paragraph), so the `AbortOnFail` sentence that the abort clause rests on
is never cited. That citation gap is part of the defect.

## 5. Does the rule's "aborts only a PreTransaction AbortOnFail hook" hold?

Yes, scoped to the failure the cell is about (an unsatisfiable `Depends`), and it needs no correction of its
truth value — the quantification is airtight: at :667 the only way `ret != 0` can stop the loop is a hook
with `abort_on_fail` at :660, because a `ret` set by anything earlier would already have been caught by
:629-631 (PreTransaction) and the loop would never start. The defect is scope, not truth:

- The cell says where A is honoured; it does not say that A on a Post hook is accepted, warned about, and
  inert, which is the answer a hook author actually needs (`AbortOnFail` + `When = PostTransaction` is a
  silent no-op).
- The cell's "installed package satisfying a listed `Depends` is missing" omits the timing: the lookup at
  hook.c:509 reads `handle->db_local`'s pkgcache while the PreTransaction phase runs at trans.c:201-202,
  i.e. before `STATE_COMMITTING` (:206) and before the install/remove step (:212-228). A hook that
  `Depends` on a package the same transaction installs is therefore evaluated against the pre-transaction
  database and skips — logging `could not satisfy dependencies` and aborting the transaction if it also
  carries `AbortOnFail`. `[INFERENCE]` the direction of the write (the new package enters the local db
  during the commit) rests on add.c, which is outside the frozen snapshot; everything the replacement text
  below asserts about ordering is frozen evidence at trans.c:201-206.

## 6. Adjacent defect (for the L1 to route; not a change to EX7)

A malformed hook file aborts every transaction, and no `AbortOnFail` is involved. hook.c:608-615:

    609  if(parse_ini(path, _alpm_hook_parse_cb, &ctx) != 0
    610          || _alpm_hook_validate(handle, ctx.hook, path)) {
    613      ret = -1;
    614      continue;

then :629-631:

    629  if(ret != 0 && when == ALPM_HOOK_PRE_TRANSACTION) {
    630      goto cleanup;

`ret = -1` also arrives from an unopenable hookdir (:554-563), `readdir` failure (:620-623), `stat` failure
(:593-597), an over-long hookdir (:546-549) or file name (:574-577) and allocation failure (:605-606). Any of
these makes the
*load* of the PreTransaction phase return -1 with no hook selected and no `running` line, and trans.c:201-203
turns that into `ALPM_ERR_TRANS_HOOK_FAILED` — the transaction never commits, so the Post phase never runs.
The man page documents nothing about invalid hook files (`grep -n "invalid\|ignored\|skip\|mask"
alpm-hooks.5.asciidoc` → no output, exit 1), so this behaviour is code-only. It looks like a round-41 EX row
(a single bad file in `/etc/pacman.d/hooks` blocks all transactions) rather than a patch to EX7, and it is
the one place where a reader could over-extend EX7's abort clause: EX7's "only for a hook carrying
`AbortOnFail`" is correct for the `Depends` failure and false for the phase as a whole.
Source-level only: I did not execute it (host transactions are paused; a live transaction is the only way
to observe it, and the host was off-limits).

## 7. Smallest safe correction — exact text

Cells 0 (`EX7`) and 2 (`` `could not satisfy dependencies` ``) unchanged. Three edits inside the row,
nothing else. Each block below is one line, ready to paste; the complete replacement row is
`ex7-proposed-row.txt` (single line) and the diff against the lane tip is `ex7-proposal.diff`.

Edit 1, cell 1 (rule) — two changes: the `Depends` qualifier becomes "the local package cache lacks a
match for a listed Depends", and the PostTransaction sentence is appended after the abort clause.
Resulting cell, one line:

```
The `running '<name>'...` log line is written before the hook's `Depends` are checked; when the local package cache lacks a match for a listed `Depends`, libalpm logs `unable to run hook <name>: … satisfy dependencies` and skips the command, and that failure stops the PreTransaction phase, and with it the transaction, only for a hook carrying `AbortOnFail`; a PostTransaction hook carrying `AbortOnFail` is admitted at load (validation returns 0, warning at hook.c:141-144 for a hook with triggers), and its failure reaches alpm_trans_commit as a return value the call discards (trans.c:237-239)
```

Edit 2, cell 3 (source) — append after `` `Depends` documented in S224 alpm-hooks.5.asciidoc:83-85 ``:

```
; `AbortOnFail` “Only applies to PreTransaction hooks” in S224 alpm-hooks.5.asciidoc:87-89
```

Edit 3, cell 4 (host) — insert before `` the live log holds 0 such errors ``:

```
a PreTransaction `Depends` is resolved against the local database as it stands when the phase runs (hook.c:509, called from trans.c:201-202, ahead of `STATE_COMMITTING` :206), so a hook that Depends on a package the same transaction installs skips during that transaction; 
```

(Edit 3 carries a trailing space before the existing clause, so the cell keeps its single separator.)

Verification of that text against the *unchanged* frozen counter, in a scratch clone of the lane
(`git clone -q --shared`, `remote remove origin`, commit on `master`, fixture identity
`fixture@shokunin.local`):

    $ python3 tools/check-exec-environment-r40.py --repo <scratch> --revision 5486e9d0…
    result PASS, rules_verified 8, exit 0, novelty_base_hits 0, EX7 {"verified": true, "reasons": []}
    (receipt: counter-v6-pass.json)

    baseline, lane tip f951f288… : result PASS, rules_verified 8, exit 0   (receipt: counter-baseline.json)
    negative control 34f888d2… (same text with "the call discards" -> "the call does not discard"):
        result FAIL, rules_verified 7,
        EX7 reasons ["rule carries negation word 'not'"]                    (receipt: counter-negation-fail.json)

The negative control matters for the wording: `tools/check-exec-environment-r40.py:97` rejects the negation
words `not|never|no|none|nothing|without|instead|unless|cannot|neither|nor|n't` in a rule cell, so the inert
Post-phase behaviour has to be phrased positively ("the call discards"); a shorter and more natural
"libalpm does not honour it" would fail the frozen counter. The tested text is the proposed text: variant v6
is the exact row in `ex7-proposed-row.txt`, and it keeps the four required EX7 tokens (`Depends`, `running`,
`AbortOnFail`, `satisfy dependencies`), the value cell, and the 4-25 word quote check intact.

## 8. Impacted axes

- EX7 (rule, source, host cells) — corrected as above.
- The derived list "What a hook or scriptlet author can rely on", item 5 ("A `running` line is selection, not
  execution"): true and unaffected; if the L1 wants one more derived line, "an `AbortOnFail` on a
  PostTransaction hook is accepted and inert" is the candidate, and it is a doc-level addition, not a row.
- No effect on EX6 (`NeedsTargets`/stdin), EX8 (Path triggers) or the C1 census item: nothing in
  `probe_storage_arm` or the selftest fixtures is touched by this finding.
- Counter `check-exec-environment-r40.py` unchanged and still PASS (8/8) on the proposed text.

## What I did not do

- Did not run a pacman transaction, install a hook file or touch `/etc`: transactions are paused host-wide
  and the host is off-limits, so "Post `AbortOnFail` is inert" and the bad-hook-file abort are code-path
  conclusions from the frozen snapshot, not observed runs. The only host observations are the two
  `grep` counts on `/var/log/pacman.log` and the `sha256sum -c` on the snapshots.
- Did not verify what pacman's frontend prints or its exit code after a discarded Post-phase failure;
  `alpm_trans_commit` returning 0 (trans.c:244) is as far as the frozen evidence goes.
- Did not edit, stage or commit anything in the lane; wrote only this report and the receipts under
  `.ufo/waves/round-40/w1/C2CritEX7/` (`ex7-proposed-row.txt`, `ex7-proposal.diff`,
  `counter-baseline.json`, `counter-v6-pass.json`, `counter-negation-fail.json`).
- No tools installed or upgraded; spent no package operations. Scratch
  `/fast/scratch/hyaku/tsukuroi-r40/C2CritEX7/` removed after the receipts were copied.
