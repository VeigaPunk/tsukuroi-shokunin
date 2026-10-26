VERDICT: supports

> Note: the oracle finds **zero** order violations (C2's HO7 holds on all 60
> transactions in the host log, including against an order derived from the
> hook files by HO1/HO2 rather than from the table). One **documentation-level**
> defect was found in HO5's *prose* ("three operator files" — one of the three
> `/etc/pacman.d/hooks/` files is package-shipped); see §7. No HO1–HO7 *rule
> row* was judged by this seat.

Seat: C2ExecLogOracle, item C2-1 (kill-rule oracle, `/var/log/pacman.log` run order).
All work read-only: `read`, `grep`, `pacman -Qoq`/`pacman -Ql` (queries, no
transaction, no database write), `stat`. No host mutation, no pacman transaction,
no `sudo`, no git/jj command in the lane, no tool installed. Scratch
`/fast/scratch/hyaku/tsukuroi-r38/C2ExecLogOracle/` removed after receipts were
copied to `.ufo/waves/round-38/w1/C2ExecLogOracle/`.

## 1. Inputs, pinned

| input | pin |
|---|---|
| `/var/log/pacman.log` | 3254 lines, 252016 bytes, sha256 `0845c1df31fcccd1b629f3b5c8190c037a572bbfbd6d9e11f81be635b1a4fc67`, mtime `2026-10-25 13:12`; single file, no rotation (`ls -la /var/log/pacman.log*` → one file, no `.gz`) |
| `corpus/knowledge/pacman-hook-order-r38.md` | sha256 `b56c90f1ebbdfa3d07f369e39b7580d6b0050da69eb9d4d2b560b58771c73f61` |
| hook dirs at check time | 67 files `/usr/share/libalpm/hooks` + 3 files `/etc/pacman.d/hooks` = 70 files, 69 effective names |
| sources (frozen lane snapshot) | `.ufo/waves/round-38/sources/trans.c`, `hook.c` |

Digests are in the receipt `inputs.sha256`; all receipts under
`.ufo/waves/round-38/w1/C2ExecLogOracle/` with `MANIFEST.sha256`.

## 2. Log structure, as actually found (this drove the parser)

1. **Hook marker**: `[<iso8601>] [ALPM] running '<name>.hook'...` — exactly 295 such
   lines (`grep -c "running '" /var/log/pacman.log` → `295`), always with the
   trailing `...`, always the `.hook` suffix, always the `[ALPM]` (not
   `[ALPM-SCRIPTLET]`) prefix.
2. **Transaction delimiters**: `[ALPM] transaction started` × 60,
   `[ALPM] transaction completed` × 60; `transaction failed`/`interrupted` × 0.
3. **Phase position is unambiguous in this log**: Pre hooks are logged *before*
   `transaction started`, Post hooks *after* `transaction completed` — e.g.
   `:1398` `running '10-limine-snapper-lock.hook'...` → `:1399` `transaction started`
   → `:1401` `transaction completed` → `:1402-1404` Post hooks. This matches
   `trans.c:201-203` (the Pre run happens before the log line) and `trans.c:208`
   (`transaction started\n`), `trans.c:235-238` (`transaction completed` then the
   Post run).
4. **Two epochs in one file**: lines `1-478` are the installer bootstrap
   (`pacman -b /mnt//var/lib/pacman/ -r /mnt …`, last one `:478`, timestamps
   `+0000`); from `:480` the host (`-0300`). The checker orders by **line
   number**, never by timestamp.
5. **86 `[PACMAN] Running '<cmd>'` lines but 60 transactions**: 26 commands
   produced no transaction (`-D …` database-flag commands, `-Sc`/`-Scc` cache
   clean, bare `-Sy`, `-Sw` download-only, and superseded `-S` invocations, e.g.
   `:1413`). Zero hook runs are orphaned, so no `running` line belongs to those
   commands — consistent with `trans.c:182-184` returning early on an empty
   transaction and `:192-193` on `--downloadonly`.
6. **Hook runs, by phase**: 59 Pre (across 49 transactions) + 236 Post (across
   all 60) = 295, i.e. every `running` line is assigned to exactly one phase of
   one transaction; 0 orphan, 0 inside a transaction body.
7. **Names carry no directory**: the log prints basenames only, so HO2's
   same-name override is not directly observable (§6 gives the indirect,
   execution-level evidence).
8. Scriptlet output is interleaved as `[ALPM-SCRIPTLET]` and is ignored.

## 3. The oracle (receipts: `check-pacman-log-order.py`, `log-order.json`, `summary.txt`, `transactions.txt`)

State machine over the log: `[PACMAN] Running` resets the command context;
`running` lines while idle accumulate into the *pending Pre* bucket; `transaction
started` takes that bucket as the Pre phase; `running` lines while in the
post-state are appended to the Post phase of the last transaction.

Checks per transaction, per phase:

- **T1/T2** the observed name sequence is a subsequence of the table's
  phase order (greedy match over the table's `pos` column) — HO7 (doc `:27`).
- **T3** no hook repeats within one phase of one transaction (a total order has
  no duplicates).
- **T4** the observed phase equals the phase the table records for that name.
- **T5** every observed name is a table row; anything else is reported as a hook
  in the log but not in the table (with the on-disk dirs consulted).
- Structural assertions that also gate exit status: no hook run between
  `started` and `completed`, and no Pre hook run without a transaction.

## 4. Results — the four numbers C2-1 asks for

Command and observed output:

```
$ python3 check-pacman-log-order.py \
    --table corpus/knowledge/pacman-hook-order-r38.md --json log-order.json
transactions=60 phases_checked=109 hook_runs=295 orphans=0 anomalies=0 findings=0 unknown_hooks=0
(exit 0)
```

| asked | result |
|---|---|
| transactions checked | **60** (all transactions in the file; 60 started = 60 completed) |
| phases checked | **109** = 49 Pre + 60 Post. The other 11 Pre phases are empty: tx1–tx11 (`phases_empty` in `log-order.json`) |
| violations | **0**. 0 subsequence violations, 0 duplicate-in-phase, 0 phase mismatches. Longest Pre phases are tx14 (5 hooks, `:1417-1421`) and tx44 (7 hooks, `:2466-2478`); both are strict subsequences in table order (tx44: pos 2, 3, 4, 8, 9, 11, 17) |
| hooks in the log but not in the table | **0** — all **49** distinct hook names observed are table rows, so no hook has been removed from the host during the logged window |

Why the 11 empty Pre phases are empty, and why that confirms the model rather
than hiding a miss: the only Pre hook most transactions ever run is
`10-limine-snapper-lock.hook` (a `Type = Package`, `Target = *`, all-operations
trigger, `/usr/share/libalpm/hooks/10-limine-snapper-lock.hook:4-9`). Its owner
`limine-snapper-sync` was first installed at `:1346`, inside tx11 (`:1345-1348`);
the hook first runs at `:1398`, in tx12. A Pre-phase hook set is the *pre*-
transaction tree, so tx1–tx11 cannot run it — 49 = 60 − 11 transactions have a
Pre phase, and all 49 contain exactly this hook.

## 5. Non-vacuity — the oracle fires (receipts `selftest-oracle.py`, `selftest.txt`)

A checker that never reports anything is worthless as a kill-rule oracle, so six
mutants of a scratch copy of the log were planted and each expected detection
asserted, with the pristine copy asserted silent:

```
PASS  M0 pristine baseline: no findings  rc=0  [transactions=60 phases_checked=109 hook_runs=295 orphans=0 anomalies=0 findings=0 unknown_hooks=0]
PASS  M1 swap post hooks tx1 (256 before 255)  rc=1  ['subsequence']
PASS  M2 move pre hook 10-limine-snapper-lock.hook (line 1398) into Post phase  rc=1  ['phase-mismatch']
PASS  M3 insert hook line inside tx1 body  rc=1  ['hook-run-inside-transaction-body']
PASS  M4 duplicate post hook 256 in tx1  rc=1  ['duplicate-in-phase', 'subsequence']
PASS  M5 rename one hook to zzz-gone.hook  rc=0  ['zzz-gone.hook']      (reported as unknown, on_disk_now=false)
PASS  M6 strip '...' from one hook line (must be ignored, not invented)  rc=0  [294]
SELFTEST PASS
```

M6 is the negative control on the parser: a malformed marker is *not* invented
into a hook run (count drops 295→294, no finding), so a clean result cannot come
from over-matching.

## 6. Independent corroboration

### 6a. Order derived from the rule itself, not from the table (`check-rule-order.py`, `rule-order.json`, `rule-order-baseline.txt`)

The table's `pos` column is the thing under test, so the same subsequence check
was run against an order computed directly from the 70 hook files using
**HO1** (compare the suffix-less names bytewise over the shorter length, shorter
first — `hook.c:443-455`) and **HO2** (reversed directory list, first file per
name wins — `hook.c:540`, `:588-590`):

```
derived Pre=17 Post=52 (files: 67 usr + 3 etc)
A table==derived: True
B phases=109 violations=0
```

So (A) the table is exactly the filesystem-derived order, and (B) the log's 109
non-empty phases are subsequences of that *derived* order — the log corroborates
HO1+HO7 on its own terms. Positive controls on this axis: a copy of the table
with `fontconfig.hook`/`fontconfig-32.hook` (doc `:75-76`, pos 32/33) swapped
gives `A table==derived: False`, first mismatch reported at index 31 (receipt
`rule-order-M1-swapped-order.txt`); deleting one row trips the position-contiguity
guard (`rule-order-M2-row-removed.txt`). Both exit 1.

### 6b. HO2 seen in execution (same basename, two different Execs)

`90-mkinitcpio-install.hook` has two files on this host: `/usr/share/libalpm/hooks/`
(`mkinitcpio`) and the higher-precedence `/etc/pacman.d/hooks/` shipped by
`limine-mkinitcpio-hook`. The log cannot print the directory, but it prints the
scriptlet output, and the two Execs are distinguishable:

- `:269` `running '90-mkinitcpio-install.hook'...` → `:270` `==> Building image from preset: /etc/mkinitcpio.d/linux.preset: 'default'` (the `usr/` Exec).
- `:1362`, `:1989`, `:2983` → `Building UKI for linux (…)` (the `etc/` override, Exec `/usr/share/libalpm/scripts/limine-mkinitcpio-install`, doc `:69`).

The first limine-style run is `:1362`, in the same transaction that installed
`limine-mkinitcpio-hook` at `:1347` — which also demonstrates that the **Post**
hook list is re-read after the commit (the override file arrived in that
transaction), whereas the **Pre** list is the pre-transaction tree (§4). Same
asymmetry visible in tx1: `:3 started` … `:251 completed` → `:252 running
'20-systemd-sysusers.hook'`, although `systemd` itself was installed in that
transaction at `:123`.

### 6c. Arrival consistency (`check-hook-arrival.py`, `arrival.txt`, `hook-arrival.json`)

Rule: no hook may be logged before the package that ships its file was
installed. Owners resolved with `pacman -Qoq`; arrival = first
`installed|upgraded|reinstalled|downgraded <owner>` line.

```
hooks=49 ok=47 violations=0
```

47 packaged hooks satisfy first-sighting > owner-arrival (e.g.
`10-limine-snapper-lock.hook` first `:1398`, owner arrived `:1346`;
`fontconfig-32.hook` first `:2283`, owner `lib32-fontconfig` arrived `:2143`).
The remaining two are **unowned operator files** — `99-limine.hook` and
`walker-restart.hook` return `error: No package owns …` from `pacman -Qoq` — whose
arrival pacman cannot log, so the rule does not apply.

## 7. Defect found (documentation prose, HO5 — not an HO row's truth)

Doc `:25` (HO5, host-consequence cell) says the one Pre-phase path to a blocked
upgrade is "a broken hook file, including **the three operator files** in
`/etc/pacman.d/hooks/`". There are three *files* there, but only two are operator
files:

```
$ for f in /etc/pacman.d/hooks/*.hook; do printf '%s -> ' "$f"; pacman -Qoq "$f" || echo "UNOWNED"; done
/etc/pacman.d/hooks/90-mkinitcpio-install.hook -> limine-mkinitcpio-hook
/etc/pacman.d/hooks/99-limine.hook -> error: No package owns /etc/pacman.d/hooks/99-limine.hook   UNOWNED
/etc/pacman.d/hooks/walker-restart.hook -> error: No package owns /etc/pacman.d/hooks/walker-restart.hook   UNOWNED
```

(receipt `etc-owners.txt`). HO5's *rule* — an unparseable file in either dir
aborts the Pre run (`hook.c:609-614`, `:629-631`; `trans.c:201-204`) — is
untouched by this, and I did not judge it; only the count/label in the prose is
wrong. Suggested wording: "…including the two operator files in
`/etc/pacman.d/hooks/` (`99-limine.hook`, `walker-restart.hook`; the third file
there, `90-mkinitcpio-install.hook`, is shipped by `limine-mkinitcpio-hook`)".

## 8. Coverage — 20 of 69 table rows are never exercised, and why that is not evidence against the table

49 of 69 rows are observed. For each of the 20 unobserved rows the reason is
falsifiable and falls in three groups:

**(a) 11 rows with `Operation = Remove` on a package the log never removes.**
The log contains 28 `removed` lines (none for `glibc`, `lib32-glibc`, `glib2`,
`lib32-glib2`, `gtk3`, `gdk-pixbuf2`, `man-db`, `shared-mime-info`), so
`10-glibc-remove-locale-archive`, `11-glibc-remove-ldconfig-cache`,
`12-glibc-remove-iconvconfig-cache`, `12-lib32-glibc-remove-iconvconfig-cache`,
`gdk-pixbuf-remove-loaders-cache`, `gio-remove-module-cache`,
`gio-remove-module-cache-32`, `glib-remove-compiled-schemas`,
`gtk-remove-immodules-cache`, `man-db-remove-cache`,
`shared-mime-info-remove-cache` cannot trigger. (`texinfo-remove.hook` — same
shape, target `texinfo` — *did* run at `:2478`, so the mechanism is exercised.)

**(b) 8 `Type = Path` rows whose pattern no installed package ships**
(queries `pacman -Ql`, all installed packages):

| row | trigger | why it cannot match here |
|---|---|---|
| `25-systemd-binfmt.hook` | `usr/lib/binfmt.d/*.conf` | no installed package ships any `binfmt.d/*.conf` (`pacman -Ql \| grep -E "binfmt\.d/[^/]*\.conf$"` → empty) |
| `dconf-update.hook` | `etc/dconf/db/*.d/` | no package ships a `…/dconf/db/<x>.d/` path; `dconf` ships only `/etc/dconf/db/` and `.placeholder` |
| `gio-querymodules-32.hook` | `usr/lib32/gio/modules/*.so` | `lib32-glib2` ships `/usr/lib32/gio/modules/.keep` only |
| `luarocks-make-manifest-5.2.hook` … `-5.5.hook` | `usr/lib/luarocks/rocks-5.2…5.5/*/**` | only a `rocks-5.1` tree exists (`lua51-lpeg`) — which is exactly why `…-5.1.hook` ran once at `:1257` |
| `nvimdoc.hook` | `usr/share/nvim/site/pack/dist/start/*/doc/` | `neovim` ships no `site/pack` path |

**(c) 1 `Type = Path`, `Operation = Upgrade` row explained by upgrade semantics:**
`70-dkms-upgrade.hook`. Its targets are `usr/src/*/dkms.conf` (plus two
`usr/lib/modules/…` paths) with `Operation = Upgrade` only. For Path triggers,
libalpm computes `upgrade` as *paths present in both the new and the old package
file list* (`hook.c:258-341`, `ret` at `:339-341`); a DKMS module version is part
of the path (`nvidia-open-dkms` ships `/usr/src/nvidia-615.78.08/dkms.conf`), so
a module upgrade is `install`+`remove`, never `upgrade`. That is why
`70-dkms-install.hook` (`Install|Upgrade`, same targets) ran in tx14 `:1977` and
tx44 `:2969` while `71-dkms-remove.hook` (`Remove`) ran in the Pre phase of both
(`:1421`, `:2470`) and the `Upgrade`-only hook never fires. This is an
[INFERENCE] from the pinned source plus the log; see §9.

## 9. What this does and does not show

- It **does** show: HO7's host consequence ("the pacman.log `running` sequence of
  any one transaction must be a subsequence of the table's order for its phase")
  is satisfied by all 60 transactions × 109 non-empty phases in the host's real
  history, against the table *and* against an order derived independently from
  the hook files by HO1/HO2. The doc's last bullet ("[unk] the order of hooks
  within a real transaction is not executed here; the round-38 wave checks the
  table against the pacman.log `running` sequences as an outside oracle", `:108-109`)
  is now answered for this host.
- It does **not** show that any specific hook's *trigger configuration* is
  correct — only that the triggered subset runs in table order. Absence of a row
  from the log is never treated as a violation (§8 explains each absence).
- I did **not** judge the HO1–HO7 rule rows against source (other seats); I used
  HO1/HO2/HO7 only as the ordering model that this oracle tests.
- Limits: the log spans 2026-10-03…2026-10-25 and has two timestamp epochs
  (`+0000` bootstrap, `-0300` host) — ordering is by line number, not timestamp.
  Hook names carry no directory, so HO2 is corroborated indirectly (§6b). The
  §8(b) absence checks use the *current* installed file lists; a package that
  shipped a matching path during the log window and no longer does would be
  misclassified (mitigated for the luarocks group by the observed 5.1 run, and
  for group (a) by depending only on log-level removals).
- The §8(c) mechanism (`Upgrade` = intersection of new and old file lists) is
  read from the frozen `hook.c`; I did not run a synthetic transaction to
  confirm it empirically.

## 10. Proposed text (optional, for the knowledge doc)

Replace the `[unk]` bullet at `corpus/knowledge/pacman-hook-order-r38.md:108-109`
with:

> - [obs] (round 38, C2-1) HO7 holds on the host's real history: in all 60
>   transactions of `/var/log/pacman.log` (2026-10-03…2026-10-25; 109 non-empty
>   phases = 49 Pre + 60 Post, 295 hook runs) each phase's `running` sequence is
>   a subsequence of this table — and of the order derived independently from
>   the 70 hook files by HO1/HO2 — with 0 violations, 0 duplicates and 0
>   hooks absent from the table. 49 of 69 rows are exercised; the other 20 are
>   not reachable on this host (11 have a `Remove` trigger on a package never
>   removed; 8 have a `Path` trigger no installed package ships; 1,
>   `70-dkms-upgrade.hook`, needs a same-path `dkms.conf` upgrade, which a
>   version-embedded module path never produces). Receipts:
>   `.ufo/waves/round-38/w1/C2ExecLogOracle/`.

## 11. Receipts (`.ufo/waves/round-38/w1/C2ExecLogOracle/`, digests in `MANIFEST.sha256`)

`check-pacman-log-order.py` (the item's checker), `log-order.json` (per-transaction
phases with log line numbers), `summary.txt`, `transactions.txt` (all 60
transactions, Pre/Post with line numbers), `selftest-oracle.py` +
`selftest.txt` (§5), `check-rule-order.py` + `rule-order.json` +
`rule-order-baseline.txt` + `rule-order-M1-swapped-order.txt` +
`rule-order-M2-row-removed.txt` + `table.R1.md`, `table.R2.md` (§6a),
`check-hook-arrival.py` + `hook-arrival.json` + `arrival.txt` (§6c),
`etc-owners.txt` (§7), `inputs.sha256`.
