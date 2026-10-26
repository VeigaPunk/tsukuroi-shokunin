VERDICT: supports

# C2-2 — independent re-derivation of the 69-row hook table (seat C2ExecIndepDerive)

Item C2-2 asked for the 69-row effective-hook table to be re-derived from the frozen capture and the
pinned libalpm source alone, by my own implementation of the rules, and diffed against the entry table.
Result: **69/69 rows identical, 0 differences**; the entry's rule HO1 also reproduces exactly (3 naive-sort
inversions, no more, no fewer).

I did not read, import or copy `tools/check-hook-order-r38.py` (I only hashed it:
`sha256 60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8` — matches the declared
`60e3635b…`). Nothing was executed against a package database, no transaction, no host change.

## Artifacts (all under `.ufo/waves/round-38/w1/C2ExecIndepDerive/`)

| file | sha256 | what |
|---|---|---|
| `derive-hook-order.py` | `8aab8f0f04b5f0dd16104b70b4b6c0ac1cdf4df71cf34dbb9529a056bcb42062` | independent derivation: capture walk + INI parse + validation + `_alpm_hook_cmp` + per-phase rows |
| `derived-rows.txt` | `7bea12e19518234d69e5dc14efac02af9b6364745b109a472a4df690d75f25ed` | the 69 rendered rows `when pos name dir abort needs exec0` |
| `derive.stderr` | `232c5c39bd4cf6ea6d8d9126362ce95eed7a170609e7b77f9fdd6602c4155885` | counts + the diff verdict |
| `global-order.txt` | `ef43da427f3c492c07c3c27a825fca367936a26ba315e5cb064a35710e7e45ca` | the 69 names in `_alpm_hook_cmp` order (before phase split) |
| `xcheck-sort.txt` | `78a57271a22d9a6160048da4dcd85486abcc58ce0675f1b0555ea4bcd53d3787` | cross-check against `LC_ALL=C sort` |
| `counterfactual-ho2.txt` | `c1d5d0b1a8502f6bcc0292e81360f57e792b7ec004468590870a461828e086ff` | what changes if the HookDir precedence direction is flipped |
| `check-log-order.py` | `d837fbae926627dee354ee87d4fff13b5e014902e593d53809530e0c604c1f30` | outside oracle against `/var/log/pacman.log` |
| `log-oracle.txt` | `8f82621adc0d0d4988048d65d6255c6940059f1d3c1ba2bc1f8538f8f8c04e32` | oracle result + one 39-run transaction dumped |
| `log-coverage.txt` | `1c5438062e64d891da58b69ea95fc50530cbf75bc5fb42d84d19c6bfcafb8574` | which of the 69 rows have been observed running |
| `drift-check.txt`, `live-hooks.sha256` | `66e83704ac0c6a3ae6c7ff528273b8777295ff131f6b0d968c2b5db66785b1aa`, `3a4c875990310b8690d439140673e0f624fd06610bd023eb0fc44a35d937d169` | capture vs live dirs today |

## Inputs verified before deriving

- Source snapshot digests match `sources/SHA256SUMS` (`sha256sum .ufo/waves/round-38/sources/*.c *.asciidoc`):
  `hook.c 99f1044b…`, `trans.c 637c1165…`, `alpm.c 8bbb0a3c…`, `alpm-hooks.5.asciidoc 2970cb35…`.
- Capture integrity: `sha256sum -c MANIFEST.sha256` in `frozen/hooks-capture/` → 70 files, all `OK`;
  `MANIFEST.sha256` itself = `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`, the
  value the entry cites.
- Completeness of the capture: live `/usr/share/libalpm/hooks` (67 entries) and `/etc/pacman.d/hooks`
  (3 entries) contain **only** regular files ending in `.hook` (no dirs, no symlinks, no stray files),
  and their 70 hashes equal the 70 capture hashes → `drift-check.txt`: `diff … EMPTY - capture equals live`.
  So no file pacman would load is missing from, or newer than, the capture.
- Entry text I diffed against is the committed blob: `git show 1fe28e7:corpus/knowledge/pacman-hook-order-r38.md | sha256sum`
  = `b56c90f1ebbdfa3d07f369e39b7580d6b0050da69eb9d4d2b560b58771c73f61` = `sha256sum` of the working-tree
  file, and `git status --porcelain` for that path is empty.

## Rules as implemented (my reading of the snapshot, with the lines I encoded)

| step | snapshot line | my implementation |
|---|---|---|
| directory walk order | `hook.c:540` (`for(i = alpm_list_last(handle->hookdirs); i; i = alpm_list_previous(i))`) + `alpm.c:56-62` (`myhandle->hookdirs = alpm_list_add(NULL, hookdir)` puts the system dir at the list head) | walk `/etc/pacman.d/hooks` first, then `/usr/share/libalpm/hooks` |
| file filter | `hook.c:582-586` (`name_len < suflen || strcmp(name + name_len - suflen, ALPM_HOOK_SUFFIX)`) | accept only `*.hook`; skip directories (`hook.c:600-602`) |
| same-name override | `hook.c:588-590` + `find_hook` (`:457-467`) | first name seen wins, later same-name file skipped |
| parse | `hook.c:149-256` (`_alpm_hook_parse_cb`): only `[Trigger]`/`[Action]`, only the documented keys, `When ∈ {PreTransaction, PostTransaction}`; redefinition of `When` overwrites (warning only) | strict INI, unknown section/key/value raises → hook dropped (`hook.c:609-614`) |
| validate | `hook.c:113-147`: triggerless hook valid (dummy mask, `:119-122`), else every trigger needs Target+Type+Operation and the hook needs Exec+When | same; `AbortOnFail` on a Post hook is only a warning (`:141-144`), so it stays a flag |
| ordering | `hook.c:443-455` `_alpm_hook_cmp` (`l = strlen(name) - strlen(".hook")`, `strncmp` over `min(l1,l2)`, prefix tie → shorter first) + `:633-634` msort | byte comparison over the suffix-stripped prefixes, prefix-tie shorter-first |
| phase + positions | `hook.c:636-641` (filter `hook->when == when`, collect in sorted order) | positions counted per phase in the sorted order |
| `exec0` | `hook.c:525`, `:528` (`_alpm_run_chroot(handle, hook->cmd[0], …)`) | first whitespace-split word of `Exec` (quotes stripped), not the full command |
| `abort`/`needs` | `hook.c:149-256` (`AbortOnFail`, `NeedsTargets` are bare flags: presence sets the int) | presence → `yes` |

## The diff (the requested deliverable)

`python3 derive-hook-order.py corpus/knowledge/pacman-hook-order-r38.md` (observed):

```
OVERRIDE etc/90-mkinitcpio-install.hook wins, usr/90-mkinitcpio-install.hook skipped
# walk order (dir name): etc/90-mkinitcpio-install.hook, etc/99-limine.hook, etc/walker-restart.hook ...
# hook-suffixed files: 70, overridden: 1, invalid: 0, effective: 69
# Pre=17 Post=52 masks=0 AbortOnFail=0 NeedsTargets=14
# _alpm_hook_cmp order differs from full-name byte sort for:
#   fontconfig.hook before fontconfig-32.hook (naive sort reverses this)
#   gio-querymodules.hook before gio-querymodules-32.hook (naive sort reverses this)
#   gio-remove-module-cache.hook before gio-remove-module-cache-32.hook (naive sort reverses this)

# diff vs corpus/knowledge/pacman-hook-order-r38.md: derived=69 entry=69
# IDENTICAL
```

The comparison is on the full rendered 7-tuple per row, so this simultaneously confirms for every row:
`when`, per-phase `pos`, `name`, `dir` (usr/etc provenance), `abort`, `needs`, and `exec0`. Row counts,
phase split (17 Pre / 52 Post), file count (70), override count (1), masks (0), `AbortOnFail` (0) and
`NeedsTargets` (14) all agree with the entry's "Counts:" paragraph.

Reproducibility of the shipped script: re-running the saved `derive-hook-order.py`
(`sha256 8aab8f0f…`, the exact file in this seat dir) reproduces `derived-rows.txt` and
`global-order.txt` **byte-identically** (`cmp` clean); `derive.stderr` differs only in the one line that
echoes where the global order was written. So the receipt is the output of the file as shipped.

## Independent corroboration beyond the entry

1. **Second implementation of the comparator.** `LC_ALL=C sort` of the names with `.hook` removed
   reproduces my 69-name global order element-for-element (`xcheck-sort.txt`, check A: `True`); a plain
   `LC_ALL=C sort` of the full file names differs in **exactly three** inversions, and they are precisely
   the three pairs HO1 names (`fontconfig.hook` / `fontconfig-32.hook`, `gio-querymodules.hook` /
   `gio-querymodules-32.hook`, `gio-remove-module-cache.hook` / `gio-remove-module-cache-32.hook`) —
   check C: 3 pairs, nothing else. HO1's host consequence is therefore exact, not illustrative.
2. **Outside oracle on the order (HO7), from `/var/log/pacman.log`.** 60 `transaction started` lines,
   295 `running '<name>'…` lines, all 295 attributable to the 69 rows, 0 names outside the table
   (no older host state in this log), 0 violations of: per-phase positions strictly increasing, no hook
   between `transaction started` and `transaction completed`, all Post runs of a transaction before the
   next transaction's Pre runs (`log-oracle.txt`). The largest window is a 2026-10-20 transaction with
   38 Post runs in exactly table order (positions 1…52 with the untriggered 8/19/30/34/36/40/42-49
   absent) — a genuine strict subsequence of the derived table, not a permutation.
3. **Coverage honesty**: 49 of the 69 rows appear in the log; 20 have never run in this log's span
   (`log-coverage.txt`, e.g. `nvimdoc.hook`, the `luarocks-make-manifest-5.2…5.5` rows, most `rm`-based
   Pre cache hooks). Those 20 rest on derivation only, as the entry's `[unk]` bullet implies.
4. **Depends are satisfiable** (not part of the row schema, checked because `hook.c:511-517` refuses to
   run a hook whose `Depends` is unresolved): the hooks declare `Depends` on `bash glibc coreutils rsync
   systemd dkms luarocks` only, and `pacman -Qq <p>` reports every one installed. No row is blocked at
   runtime by a missing dependency.

## How much of the table depends on HO2 (the one un-snapshotted step)

HO2's direction rests on `alpm.c:56-62` (system dir is the list head) plus the assumption that `HookDir`
entries are *appended* after it — that append lives in libalpm's config parsing, which is **not** in the
pinned snapshot (only `hook.c`, `trans.c`, `alpm.c`, the manpage are). I measured the exposure instead of
hand-waving it: re-running the same derivation with the walk order flipped (`--swap-priority`,
`counterfactual-ho2.txt`) changes **exactly one row and nothing else**:

```
< PostTransaction 26 90-mkinitcpio-install.hook etc no yes /usr/share/libalpm/scripts/limine-mkinitcpio-install
> PostTransaction 26 90-mkinitcpio-install.hook usr no yes /usr/share/libalpm/scripts/mkinitcpio
```

So the 69-row **order** (and 68 of 69 rows in full) is invariant to the HookDir precedence direction; only
the `dir`/`exec` cells of the single overridden name depend on it, and the entry's own HO2 evidence
(`alpm.c:56-62` + the manpage's "higher priority hook directory", `alpm-hooks.5.asciidoc:95-99`) is the
basis for picking `etc`. This is a dependency, not a defect: no reading of the pinned files makes the
system directory the *higher*-priority one, given the reversed walk at `hook.c:540`.

## Notes on the entry's citations (spot-checked while deriving, all correct)

`hook.c:443-455` (comparator), `:540` (reversed walk), `:588-590` (override skip), `:119-122` (mask
special case), `:609-614` and `:629-631` (parse failure aborts the Pre phase), `:636-641` (phase filter),
`:653` (the `running '…'` log line), `alpm.c:56-62`, `trans.c:201-204`, `:235-238` — all verified by
`grep -n`/`awk` against `.ufo/waves/round-38/sources/`.

## What I did not do

- Did not run `tools/check-hook-order-r38.py` (independence constraint of this item; its `fixtures_matched
  == 10` predicate is another seat's target). Hashed it only.
- Did not execute any transaction, hook, `pacman` write operation, or `sudo`; no package operation; no tool
  install or upgrade (nothing was needed). Only read-only reads of the lane, `/var/log/pacman.log`,
  `/usr/share/libalpm/hooks`, `/etc/pacman.d/hooks`.
- Did not edit any lane file. Scratch `/fast/scratch/hyaku/tsukuroi-r38/C2ExecIndepDerive/` was removed
  after the receipts above were copied into the seat dir.

## Difference list

None. Zero row differences, zero count differences, zero ordering inversions relative to the entry.

## Optional one-line entry addition (not applied; lane is read-only for this seat)

If the entry wants its own robustness boundary stated in "Observed / inferred / unknown", the derivation
supports exactly this sentence:

> [obs] the 69-row order is invariant to the HookDir precedence direction; flipping the walk changes only
> the `dir`/`exec` cells of `90-mkinitcpio-install.hook` (HO2), leaving all 69 positions unchanged
> (`w1/C2ExecIndepDerive/counterfactual-ho2.txt`).
