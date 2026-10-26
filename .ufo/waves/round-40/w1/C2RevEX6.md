VERDICT: supports

# C2-EX6 — `NeedsTargets` stdin semantics (row EX6)

Judged at lane tip `f951f288483c1af0cef4afd458488b84cf7a2165` (`git rev-parse HEAD`, run 2026-10-26T07:15Z, still the tip).
Row: `corpus/knowledge/pacman-exec-environment-r40.md:26` (verbatim row text quoted at the end).

## 1. Source re-fetch and digest equality

Access time **2026-10-26T07:15:05Z**; fetched with `curl -fsSL` into
`/fast/scratch/hyaku/tsukuroi-r40/C2RevEX6/` (copies kept as receipts in `.ufo/waves/round-40/w1/C2RevEX6/`,
fetch log `fetch-log.txt`):

- `https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/hook.c`
- `https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/alpm-hooks.5.asciidoc`
- `https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/util.c` (needed for the EX2-dependent clause)

Observed `sha256sum`:

```
99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a  hook.c.up
2970cb35115a32a5d8a9652dfd795ad535d9354c36039fcc0d25929d9c3493d3  alpm-hooks.5.asciidoc.up
381618b6054859ec76807956328b78b330237273bebe10022a559b243cb5bdd2  util.c.up
```

All three equal `.ufo/waves/round-40/frozen/src/SHA256SUMS` lines 3, 2 and 6 respectively (read 2026-10-26T07:15Z).
SOURCES rows S223/S224 pin the same two digests (`corpus/SOURCES.md:232-233`).

## 2. Clause-by-clause judgment of the rule cell

Rule cell: "A hook marked `NeedsTargets` receives its matched trigger targets on stdin, sorted with
`strcmp`, with duplicate matches from several triggers removed, one target per line; a hook lacking
`NeedsTargets` gets the closed stdin of EX2".

**(a) "receives its matched trigger targets on stdin" — holds.**
`hook.c:519-526`: `if(hook->needs_targets)` → `_alpm_run_chroot(handle, hook->cmd[0], hook->cmd, (_alpm_cb_io) _alpm_hook_feed_targets, &ctx)` (:525-526). The matches fed are the trigger matches accumulated per trigger: `_alpm_hook_trigger_match_pkg` appends matched package names (`hook.c:376,384,401`) and `_alpm_hook_trigger_match_file` appends matched file paths (`hook.c:265-266`), joined into `hook->matches` by the `_save_matches` macro (`hook.c:343-349`) and the join at `hook.c:409-412`. The parent side actually writes them into the child's stdin socket: `util.c:750-753` calls `_alpm_chroot_write_to_child(..., stdin_cb, stdin_ctx)` on POLLOUT; `util.c:495-499` fills the buffer from the callback; `util.c:501` `send(fd, buf, *buf_size, MSG_NOSIGNAL)` on `parent2child_pipefd[HEAD]`; the child's fd 0 is that socket (`util.c:667` `dup2(parent2child_pipefd[TAIL], 0)`). Documented: `alpm-hooks.5.asciidoc:91-93` — "Causes the list of matched trigger targets to be passed to the running hook on 'stdin'." (16 words, fetched 2026-10-26T07:15:05Z).

**(b) "sorted with `strcmp`" — holds.**
`hook.c:521-522`: `hook->matches = alpm_list_msort(hook->matches, alpm_list_count(hook->matches), (alpm_list_fn_cmp)strcmp);`

**(c) "with duplicate matches from several triggers removed" — holds.**
`hook.c:523-524`: comment `/* hooks with multiple triggers could have duplicate matches */` followed by `ctx = hook->matches = _alpm_strlist_dedup(hook->matches);`. `_alpm_strlist_dedup` (`hook.c:492-505`) removes adjacent equal entries (`strcmp(i->data, next->data) == 0`, :497); since the list was just fully msorted, all duplicates are adjacent, so every duplicate is removed. The attribution "from several triggers" mirrors the source comment and is true; the dedup's scope is in fact broader (see §5 precision note) — the rule does not claim exclusivity, so nothing is overstated.

**(d) "one target per line" — holds.**
`hook.c:474-476`: the feed loop copies each target then `buf[len++] = '\n';` (:476) — exactly one newline per target, including the last. The chunked-write path (`hook.c:483-487`) copies a partial target without a newline and advances the list data pointer, so a target split across buffer fills still yields one newline per target in the byte stream.

**(e) "a hook lacking `NeedsTargets` gets the closed stdin of EX2" — holds.**
`hook.c:527-528`: `} else { return _alpm_run_chroot(handle, hook->cmd[0], hook->cmd, NULL, NULL); }` — null input callback. `util.c:718-726`: `if(stdin_cb) {…} else { parent2child->fd = -1; parent2child->events = 0; close(parent2child_pipefd[HEAD]); }` (:722-726) — the parent closes its end of the stdin socket at once, so the child reads EOF on fd 0. This is exactly EX2's stated mechanism (EX2 cites `util.c:722-726`, verified here at the same lines).

## 3. Quote verbatim and citation-range check

- `hook.c:523` is exactly `		/* hooks with multiple triggers could have duplicate matches */` — the source cell's curly-quoted quote is verbatim (whitespace-collapsed) at the cited lines 519-526. ✓
- `_alpm_hook_feed_targets` spans `hook.c:469-490` (signature :469, closing brace :490); the newline is at :476. ✓
- `_alpm_hook_run_hook` spans `hook.c:507-530` (signature :507, closing brace :530); msort-strcmp at :521-522, dedup call at :524 (dedup function itself at :492-505, called from within the cited range). ✓
- `alpm-hooks.5.asciidoc:91-93` is exactly the `*NeedsTargets*::` entry (91: heading, 92-93: the two continuation lines). ✓
- SOURCES rows S223/S224/S225 (`corpus/SOURCES.md:232-234`) name the same files, line ranges and digests; S225's "14 of 69 effective hook files carry NeedsTargets" matches the capture (§4). ✓

## 4. Value and host cells

**Value cell** `sorted, deduplicated, one per line` — character-for-character consistent with clauses (b), (c), (d); the counter derives the same value from the snapshot (`tools/check-exec-environment-r40.py:170`).

**Host cell** "14 of 69 effective hook files carry `NeedsTargets` (S225 `hooks-needstargets.tsv`; a file in `/etc/pacman.d/hooks` replaces the same-named file in `/usr/share/libalpm/hooks`)":

- Frozen capture verified: `sha256sum -c MANIFEST.sha256` in `.ufo/waves/round-40/frozen/hostcap/` → all three files OK; MANIFEST self-digest `57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5` matches the entry header and S225. `awk -F'\t' 'NR>1 && $3==1' hooks-needstargets.tsv | wc -l` → 14; data rows → 69 (header `name path needs_targets exec`, values 0/1 in column 3).
- Independent live recount (read-only, 2026-10-26T07:15Z): `ls /usr/share/libalpm/hooks/*.hook | wc -l` → 67; `ls /etc/pacman.d/hooks/*.hook | wc -l` → 3; union of basenames → 69; `grep -l '^NeedsTargets$'` over both dirs → **15 files**. The discrepancy is exactly the name collision: `90-mkinitcpio-install.hook` exists in **both** dirs (`comm -12` of the two listings), and both copies carry `NeedsTargets`; one copy is shadowed, so 15 − 1 = **14 effective** — the tsv models effectiveness correctly (69 unique names, 14 flagged).
- Override direction grounded in source: `alpm.c:56-62` seeds the handle's hookdirs with `root + SYSHOOKDIR` (= `/usr/share/libalpm/hooks/`, `meson.build:71`); `conf.c:1409` defaults the frontend list to `HOOKDIR` (= `/etc/pacman.d/hooks/`, `meson.build:77`); `conf.c:946-953` appends it ("add hook directories 1-by-1 to avoid overwriting the system directory"); `hook.c:540` iterates `alpm_list_last(handle->hookdirs)` backwards and `hook.c:588-589` skips an already-seen name ("skipping overridden hook") — so the `/etc` copy wins. Documented: `alpm-hooks.5.asciidoc:95-97` "Hooks may be overridden by placing a file with the same name in a higher priority hook directory." (fetched 2026-10-26T07:15:05Z).
- The two colliding files differ and are both package-owned (read-only `pacman -Qo`, 2026-10-26T07:15Z): `/usr/share/libalpm/hooks/90-mkinitcpio-install.hook` → `mkinitcpio 42.2-1`; `/etc/pacman.d/hooks/90-mkinitcpio-install.hook` → `limine-mkinitcpio-hook 1.40.0-2`; `diff -q` → differ. The tsv lists the `/etc` path as the effective row — consistent with the grounded direction.

## 5. Precision note (no correction required)

The dedup removes **all** adjacent duplicates, whatever their cause. A single `Path` trigger can emit the same path twice when two packages in one transaction own it: `_alpm_hook_trigger_match_file` appends per package (`hook.c:258-271`, loop over `handle->trans->add`), so one trigger's `install` list can hold a repeated path. The rule's "duplicate matches from several triggers" reproduces the source comment (`hook.c:523`) and is not false — those duplicates are removed — and it does not claim exclusivity; the value cell's bare `deduplicated` is the operative guarantee and is exact. No text change proposed.

## 6. Counter corroboration

`python3 tools/check-exec-environment-r40.py --revision f951f288483c1af0cef4afd458488b84cf7a2165` (run 2026-10-26T07:15Z, read-only) → `result: PASS, exit: 0`, `rules_verified: 8`, EX6 `{present: true, verified: true, reasons: []}` (full JSON receipt `counter-output.json`).

## 7. Verdict

**holds** — every clause of the rule cell is stated by the pinned source at the cited lines, the quote is verbatim, the value cell matches the derived value, and the host cell's 14-of-69 count and override note are confirmed by the frozen capture, a live recount, and the source-grounded override direction. No correction text is proposed (the item's draft obligation applies only below `holds`).

## 8. What I did not do

- Did not run a transaction to observe a `NeedsTargets` feed end-to-end: pacman transactions are paused host-wide; the stdin path is judged from source only (hook.c + util.c).
- Re-fetched only the three pinned files EX6 cites (hook.c, alpm-hooks.5.asciidoc, util.c); PKGBUILD, meson_options.txt and trans.c were not re-fetched (not cited by EX6). The extra files grounding the override direction (conf.c, conf.h, handle.c, alpm.c, meson.build) are my own fetches, kept as receipts, not part of the frozen SHA256SUMS.
- Did not modify any lane file; all writes were this report and its receipts dir.

## Verbatim row judged

`corpus/knowledge/pacman-exec-environment-r40.md:26`:

```
| EX6 | A hook marked `NeedsTargets` receives its matched trigger targets on stdin, sorted with `strcmp`, with duplicate matches from several triggers removed, one target per line; a hook lacking `NeedsTargets` gets the closed stdin of EX2 | `sorted, deduplicated, one per line` | S223 hook.c:519-526 “/* hooks with multiple triggers could have duplicate matches */” (feed loop `_alpm_hook_feed_targets` :469-490, newline :476); documented in S224 alpm-hooks.5.asciidoc:91-93 | 14 of 69 effective hook files carry `NeedsTargets` (S225 `hooks-needstargets.tsv`; a file in `/etc/pacman.d/hooks` replaces the same-named file in `/usr/share/libalpm/hooks`) |
```
