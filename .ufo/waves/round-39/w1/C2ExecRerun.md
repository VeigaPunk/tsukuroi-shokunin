VERDICT: supports

Seat C2ExecRerun, item C2-1: frozen-artifact identity of the C2 counter, re-run of it at the C2
implementation commit and at the dispatch tip, and comparison against the authored `after/` receipt.
Every number below is from a command run in this seat; receipts in
`.ufo/waves/round-39/w1/C2ExecRerun/`.

## 1. Frozen artifact identity — matches the declaration

```
$ sha256sum tools/check-transaction-order-r39.py
f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e  tools/check-transaction-order-r39.py
$ git show 6a08925daa30767809eb13bb4b01448ff954d46a:tools/check-transaction-order-r39.py | sha256sum
f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e  -
$ git diff --quiet HEAD -- tools/check-transaction-order-r39.py && echo identical
identical
```

- Declared pin `f1c97836…c991e`: worktree hash equals it, and the blob at the frozen counter revision
  `6a08925daa30767809eb13bb4b01448ff954d46a` hashes to the same value, so the run below used exactly the
  frozen bytes (lane worktree file is byte-identical to `HEAD` = `394e1ba`).
- Frozen inputs the counter reads from its own tree also match their pins
  (`.ufo/waves/round-39/frozen/src/SHA256SUMS` vs recomputed, section "frozen src sha256" of
  `.ufo/waves/round-39/w1/C2ExecRerun/independent-evidence.txt`): add.c
  `fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1`, hook.c
  `99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a`, remove.c
  `a052d455f088f34bf1d713a434957de7e1b9322862a07b69160c65ee15dca314`, sync.c
  `6b297364eaba94e82a1e30b50dde9b3b96f88075855b66ff455aca1e24995d46`, trans.c
  `637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07`, util.c
  `381618b6054859ec76807956328b78b330237273bebe10022a559b243cb5bdd2`; capture MANIFEST sha256
  `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4` recomputed identically.

## 2. Re-runs — PASS at both revisions, exit 0, no stderr

```
$ python3 tools/check-transaction-order-r39.py --revision 4078eb236c7c67f343c76956c587d0a356e0bf5c
rc=0   -> .ufo/waves/round-39/w1/C2ExecRerun/rerun-4078eb236c7c67f343c76956c587d0a356e0bf5c.json
$ python3 tools/check-transaction-order-r39.py --revision 2e1c2a40c13dc52e155d89e72f3fdd560db7399a
rc=0   -> .ufo/waves/round-39/w1/C2ExecRerun/rerun-2e1c2a40c13dc52e155d89e72f3fdd560db7399a.json
```
Both `.err` files are 0 bytes.

| field | 4078eb2 | 2e1c2a4 | predicate needs |
|---|---|---|---|
| entry_present | true | true | — |
| rules_verified | 8 | 8 | == 8 |
| duplicate_rows | 0 | 0 | == 0 |
| duplicate_headings | 0 | 0 | == 0 |
| source_ok | 1 | 1 | == 1 |
| counts_ok | 2 | 2 | == 2 |
| oracle_violations | 0 | 0 | == 0 |
| result / exit | PASS / 0 | PASS / 0 | |
| host | windows 86, transactions_started 60, scriptlet_tag_outside_commit 252, scriptlet_tag_total 441, running_inside_commit 0 | identical | feeds counts_ok / oracle_violations |

`branch_tip`: 4078eb2 run → `394e1ba4fab39a417abe66a7802f87cf1ff8dd61` (current `master`); 2e1c2a4 run →
same. The two rerun records differ from each other only in `revision`.

## 3. Comparison with the authored `after/` receipt — reproduces exactly

`after/c2-after-4078eb2.jsonl` holds three concatenated JSON documents (not one-per-line): a `receipt: 1`
wrapper (`tool_revision 6a08925…`, `revision 4078eb2…`, `lane_branches`), the counter record, and a
`receipt_end` (`exit_code 0`, `finished_utc 2026-10-26T06:00:23Z`).

Robot comparison (`python3` with `json.JSONDecoder().raw_decode` loop) of my 4078eb2 rerun against the
record in that file:

```
a rules == after rules: True
a minus branch_tip == after minus branch_tip: True
```

So every predicate field, the whole `rules` dict, the `host` block and the `predicate` string are
byte-equal to the authored receipt; the only difference is `branch_tip` (`4078eb2` then — `master` was the
implementation commit when the receipt was authored; `394e1ba` now), which is not in the predicate and is
expected to move. `before/c2-before.jsonl` at base `0eff65b` records `entry_present false`,
`rules_verified 0`, `result FAIL`, `exit 1`; my own run at that same revision reproduces it (§5 control 1).

## 4. Per-row flags and reasons — all eight verified, no reasons, at both revisions

Both reruns and the after receipt report `present: true, verified: true, reasons: []` for TO1–TO8. Because a
green flag alone proves nothing about whether the cited lines actually carry the quote, I re-located every
quote myself with an independent implementation (own regex/collapse, no import of the counter):
`.ufo/waves/round-39/w1/C2ExecRerun/independent-evidence.txt`, section "independent quote-at-cited-lines
check".

| row | required file (counter) | cited span | quote matches inside span | first source line carrying the quote text |
|---|---|---|---|---|
| TO1 | trans.c | 201-208 | yes (16 words) | trans.c:202 (`_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) {` … through trans.c:208 `alpm_logaction(… "transaction started\n");`) |
| TO2 | sync.c | 1336-1356 | yes (7 words) | sync.c:1340 `/* remove conflicting and to-be-replaced packages */` |
| TO3 | add.c | 616-648 | yes (9 words) | add.c:638 `/* run the post-install script if it exists */` |
| TO4 | add.c | 470-474 | yes (10 words) | add.c:472 `_alpm_runscriptlet(handle, pkgfile, scriptlet_name,` + 473 `newpkg->version, oldpkg ? oldpkg->version : NULL, 1);` |
| TO5 | hook.c | 532-560 | yes (8 words) | hook.c:540 `for(i = alpm_list_last(handle->hookdirs); i; i = alpm_list_previous(i)) {` |
| TO6 | add.c | 676-692 | yes (11 words) | add.c:681 `/* running ldconfig at this point could possibly screw system */` |
| TO7 | remove.c | 699-733 | yes (6 words) | remove.c:711 `_alpm_runscriptlet(handle, scriptlet, "pre_remove", pkgver, NULL, 0);` |
| TO8 | util.c | 521-528 | yes (4 words) | util.c:527 `alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);` |

Rows' inline pointers also check out: TO2 `_alpm_remove_packages` sync.c:1345 then `_alpm_upgrade_packages`
sync.c:1354; TO3 log line `upgraded %s (%s -> %s)` add.c:630 and post scriptlet add.c:638-647; TO5 `opendir`
hook.c:554; TO6 `_alpm_ldconfig` add.c:691 after the loop 670-687; TO7 `removed %s (%s)` remove.c:722,
`post_remove` remove.c:731; TO8 `_alpm_chroot_process_output` util.c:521 and the hooks' route
hook.c:525-528.

`source_ok` inputs are real at both revisions (`corpus/SOURCES.md` sha256 `c2e45986…` at 4078eb2 and at
2e1c2a4 — identical): S208 `mined`, opened 2026-10-26, used-by `pacman-hook-order-r38.md,
pacman-transaction-order-r39.md`, title `…/blob/54d9411/lib/libalpm/hook.c`; S213 add.c, S214 sync.c,
S215 remove.c, S216 util.c, S217 trans.c, S218 own-work capture, each `mined`/2026-10-26/used-by
`pacman-transaction-order-r39.md`. S210 (the superseded trans.c anchor) is still `mined` but is not on the
entry's `source:` line, so the "S217 supersedes S210's anchor" form of the declaration is consistent with
the data rather than a doubled anchor.

Host counts, recomputed from `.ufo/waves/round-39/frozen/txcapture/pacman.log` by a state machine I wrote
(not the counter's), give exactly the numbers the receipt claims:
`{'windows': 86, 'transactions_started': 60, 'scriptlet_total': 441, 'scriptlet_outside': 252,
'running_inside_commit': 0}`; `removed` lines 28, windows holding both removals and adds 0 (TO2/TO7 host
columns); 17 `PreTransaction` hooks of 70, all 17 owned by a package whose first `installed` line is in some
window, 0 of the 17 `running '<name>'` in that same window (TO5 host column). TO1's host cell carries
"60 transactions" and "86 `[PACMAN] Running` windows", TO8's "252 of 441" — matching `counts_ok == 2`.

Additional currency check: `sha256sum /var/log/pacman.log` today is
`0845c1df31fcccd1b629f3b5c8190c037a572bbfbd6d9e11f81be635b1a4fc67`, identical to the frozen capture, so
the host counts are not stale relative to the live log at run time (no pacman run since capture).

## 5. Controls — the green flags are falsifiable

1. Base control (reproduces the declared "Before at base: FAIL"):
   `python3 tools/check-transaction-order-r39.py --revision 0eff65b21bb81195ee06c96a83afbd7a07e52eef` →
   `{'entry_present': False, 'rules_verified': 0, 'source_ok': 0, 'counts_ok': 0, 'result': 'FAIL', 'exit': 1}`
   (`.ufo/waves/round-39/w1/C2ExecRerun/control-base-0eff65b.json`).
2. Mutation control in a scratch clone (clone of the lane under
   `/fast/scratch/hyaku/tsukuroi-r39/C2ExecRerun/`, `git -C "$D" rev-parse --show-toplevel` verified equal
   to `$D` before the commit, `remote remove origin`, mutant committed on `master` there, counter invoked
   with `--repo "$D"`): TO4's quoted argument order swapped to
   `… oldpkg ? oldpkg->version : NULL, newpkg->version, 1);` →
   `rules_verified 7`, `TO4: ['no 4-25 word quote found in add.c at the cited lines']`, `result FAIL`,
   `exit 1` (`.ufo/waves/round-39/w1/C2ExecRerun/control-mutant-to4.json`). A quote reworded so it no longer
   occurs at its cited lines is caught, so `verified: true` on the eight rows is not vacuous.

## 6. Observations (executor evidence, not row judgments)

I am the C2-1 executor seat; the declaration's kill rule assigns truth judgment of TO rows to reviewer
seats, so I deliberately emit no `TO<n>: holds|partly|fails` lines. What my reading of the pinned snapshots
surfaced, with exact coordinates, for whoever does judge:

- **NOHOOKS gate is absent from the entry.** `grep -c NOHOOKS corpus/knowledge/pacman-transaction-order-r39.md`
  → `0`. Both hook phases are conditional in the pinned source: trans.c:201
  `if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS) &&` guards the Pre call at :202, and trans.c:237
  `if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS)) {` guards the Post call at :238. TO1's unconditional
  "The PreTransaction phase runs **before** `transaction started` is logged" therefore holds for hook-enabled
  transactions only; a `--nohooks` transaction logs `transaction started` (trans.c:208) with no Pre phase, and
  TO5's "Pre phase sees the hook files on disk before the commit" inherits the same condition. The quoted
  excerpt itself is honest to its citation — it simply starts at :202, after the flag test.
- **TO1's quote is a collapsed splice, not a contiguous excerpt.** It begins mid-condition at trans.c:202
  (`_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0) {`) and continues through :203-204
  `RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);` `}`, :206 `trans->state = STATE_COMMITTING;`, :208
  `alpm_logaction(handle, ALPM_CALLER_PREFIX, "transaction started\n");`, skipping the intervening blank
  lines, brace and the flags test at :201. The counter's documented test (quote occurs, whitespace-collapsed,
  inside lines A..B) accepts this by design; it is contract-consistent, worth knowing when the row is read as
  a verbatim quotation.
- **TO1's "Post at trans.c:232-239" carries no quote** and the counter needs only one quote to hit one cited
  span. I read the span: :235 logs `transaction completed\n`, :238 calls
  `_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION)`, inside the `else` of the `STATE_INTERRUPTED` test at
  :230 — the pointer is accurate, just unquoted.
- **TO5's span start is loose, not wrong:** hook.c:532 is `int _alpm_hook_run(alpm_handle_t *handle,
  alpm_hook_when_t when)`, the quoted `for` is at :540, `opendir` at :554 as the cell says.
- **TO3's intra-package order is confirmed by line order in add.c**, matching the rule text: pre scriptlet
  from the package file :472-473 → `_alpm_local_db_prepare` :493 → extraction :530/:560 →
  `_alpm_local_db_write` :599 → `installed`/`upgraded` log :618-630 → post scriptlet from the local db
  `install` path :641/:644. This is order evidence; the rule's truth verdict remains with reviewers.
- **TO6's cited span starts on a blank line:** add.c:676 is empty, :677 is
  `if(commit_single_pkg(handle, newpkg, pkg_current, pkg_count)) {`; the quote is at :681 inside the failure
  branch that sets `trans->state = STATE_INTERRUPTED` (:679) and `skip_ldconfig = 1` (:682), with
  `_alpm_ldconfig` at :691 under `if(!skip_ldconfig)` (:689) — span-true.

## 7. Bounds honoured

Read-only on lane content: the only files I wrote are this report and
`.ufo/waves/round-39/w1/C2ExecRerun/` (five receipts: two reruns, two controls, one evidence transcript,
plus the two zero-byte stderr files from the reruns).
No `git add/commit/stash/checkout/reset/push`, no jj command, nothing written in `/home/vgpnk/Projects/shokunin`,
no sibling lane, no `/home/vgpnk/Projects/shokuknow`, no host mutation, no pacman, no sudo, no service
restart, no `agent://all`. All clones/mutants lived under
`/fast/scratch/hyaku/tsukuroi-r39/C2ExecRerun/` (287 MB at peak) and the directory is removed — `ls -d` on it
now reports "No such file or directory". Lane `git status --porcelain` shows only changes that were already
there or belong to sibling seats (`PROVINCE.md`, `SKILL.md`, `w1-dispatch.err`, `w1.ready.dispatched`, `w1/`);
none of them are mine. Tools installed: none (nothing needed); no version changes to record.

## 8. What I did not do

- Did not judge whether each TO rule's *text* is true of the pinned source (reviewer/critic remit per the
  declaration's kill rule); I verified where each quote lands and recomputed the host counts.
- Did not re-fetch libalpm from gitlab to compare the frozen snapshots with upstream at `54d9411`; identity
  here is the pinned `SHA256SUMS` inside the lane, not a network re-download.
- Did not run the counter's own C1 sibling, the lane's build/lint/test suites, or the selftest — post-integration
  gates belong to the L1.
