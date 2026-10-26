VERDICT: defect-found

# C2-6 — attack on HO5 (round 38, hyaku run 8, seat C2CritHO5)

Item: HO5 in `corpus/knowledge/pacman-hook-order-r38.md:25` —

> Any `.hook` file in either directory that fails to parse or validate (no Exec, no When, bad trigger) makes
> the Pre-phase run return an error **before any Pre hook runs**; `trans.c` turns it into
> `ALPM_ERR_TRANS_HOOK_FAILED` ("failed to run transaction hooks") and the transaction never starts
> — S208 `hook.c:609-614`, `:629-631`; S210 `trans.c:201-204`.
> Consequence cell: "The one Pre-phase path to a blocked upgrade on this host is a broken hook file, including
> the three operator files in `/etc/pacman.d/hooks/`."

The **mechanism** the row names holds, and I proved it by running the pinned code, not by reading it. Two
statements *inside the same row* are false as written: the parenthetical `(no Exec, no When, bad trigger)` and
the consequence's "the one Pre-phase path … is a broken hook file". Details, counterexamples and a minimal
replacement text follow.

---

## 1. What holds — verified against the pinned source and by execution

Source (snapshots verified against `.ufo/waves/round-38/sources/SHA256SUMS`, `sha256sum -c` → all four `OK`,
2026-10-26):

- `sources/hook.c:540` — the scan iterates **every** hook directory (`alpm_list_last` → `alpm_list_previous`),
  and `sources/hook.c:609-615` parses and validates **every** candidate file, with no reference to `when`.
  `when` is read only later, at `:638` (trigger filter) and `:629` (phase gate).
- `sources/hook.c:629-631` — `if(ret != 0 && when == ALPM_HOOK_PRE_TRANSACTION) goto cleanup;` sits **before**
  the run loop at `:636-642`, so a scan error returns before any hook's trigger is even evaluated.
- `sources/trans.c:201-204` — `_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION) != 0` →
  `RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1)`, before `trans->state = STATE_COMMITTING` (`:206`) and
  before `"transaction started"` is logged (`:208`), so the transaction genuinely never starts.
- Message string: `lib/libalpm/error.c:105-106` at 54d9411 → `case ALPM_ERR_TRANS_HOOK_FAILED: return
  _("failed to run transaction hooks");` (fetched 2026-10-26 from
  `https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/error.c`; excerpt kept in
  `C2CritHO5/fetched-lines.txt`). The frontend renders it via `src/pacman/sync.c:850-851`
  `_("failed to commit transaction (%s)\n")` → user sees
  `failed to commit transaction (failed to run transaction hooks)`.

Execution (`C2CritHO5/matrix.txt`, harness `C2CritHO5/fx.c`, driver `C2CritHO5/cases.sh`). The harness links
the **installed** libalpm, which is the pinned code: `pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3`,
`libalpm.so.16`, `-lalpm` headers in `/usr/include/alpm.h`. It builds a throwaway root under scratch, copies one
real local-DB entry (`which-2.25.1`, 12 K) into it, and runs
`alpm_trans_init(NODEPS)` → `alpm_remove_pkg` → `alpm_trans_prepare` → `alpm_trans_commit`, printing
`alpm_errno`/`alpm_strerror`. No host object is touched; hooks that "run" fail at `chroot` with EPERM
(`ALPM-SCRIPTLET could not change the root directory`), which is irrelevant because the observable is the
`running '<name>'...` line `hook.c:653` writes before the exec attempt.

| case | hook tree | `RESULT` |
|---|---|---|
| T0 | one valid, never-triggered Post hook (control) | `rc=0 … is_hook_failed=0` |
| T1 | `/etc` hook: valid `[Trigger]`, `When = PostTransaction`, **no Exec** | `rc=-1 errnum=32 "failed to run transaction hooks"` + `[E] Missing Exec option in hook: /etc/pacman.d/hooks/50-bad-post.hook` |
| T2 | same, `When = PreTransaction` | `rc=-1 errnum=32`, `[E] Missing Exec …` |
| T2b | valid `[Trigger]` + `Exec`, **no When** | `rc=-1 errnum=32`, `[E] Missing When option …` |
| T5 | broken file only in `/usr/share/libalpm/hooks` | `rc=-1 errnum=32`, `[E] Missing Exec …50-bad-sys.hook` |
| T9 | `Type = Bogus` under a `[Trigger]` | `rc=-1 errnum=32`, `[E] … line 3: invalid value Bogus` |
| T10 | `[Bogus]` section | `rc=-1 errnum=32`, `[E] … line 1: invalid section Bogus` |
| T11 | file mode 0000, name ends `.hook` | `rc=-1 errnum=32`, `[E] error while reading hook …: Permission denied` |

T11 also proves the fopen path: `src/common/ini.c:57-60` returns `cb(file, 0, NULL, NULL, NULL, data)` when
`fopen` fails, and `hook.c:159-160` turns that into `error(...); return 1;`.

**"before any Pre hook runs" — proven by A/B run, not by reading.** T14 and T15 carry an *identical* matched
Pre hook (`10-runme.hook`, trigger `Remove/package/which`, and the transaction removes `which`):

- T15 (clean tree): `RESULT rc=0 …` and pacman.log contains
  `running '10-runme.hook'...` — the Pre hook is reached.
- T14 (same tree **plus** `/usr/share/libalpm/hooks/zz-bad.hook` = `[Trigger]` + `[Action] When = PostTransaction`,
  no Exec): `RESULT rc=-1 errnum=32 "failed to run transaction hooks"`, `[E] Missing Exec option in hook:
  …/zz-bad.hook`, and the transaction log is **0 bytes** — `10-runme.hook` never reached `hook.c:653`.

## 2. Question 1 — does a broken PostTransaction-only hook file also block? **Yes.**

`hook.c:609` parses every candidate regardless of its `When`; the gate at `:629` keys on the **phase being run**
(`when == PRE_TRANSACTION`), never on the broken file's own `When`. T1 and T14 (the file is PostTransaction-only)
both return `ALPM_ERR_TRANS_HOOK_FAILED`. So HO5's body is even stronger than the parenthetical suggests — and this
is host-material, because **all three** `/etc/pacman.d/hooks/*.hook` files are PostTransaction
(`90-mkinitcpio-install.hook:29`, `99-limine.hook:9`, `walker-restart.hook:10` — `grep -n When`, 2026-10-26). A syntax error
in the operator's most-edited hook blocks the entire upgrade at the Pre phase, it does not merely skip a
post-install step. HO5 should say so explicitly.

## 3. Question 2 — does an unreadable (EACCES) HookDir block? **Yes**, and the branch is wider than the row.

`hook.c:554-562`: `opendir` failure is tolerated **only** for `ENOENT` (`:555-556 continue;`); any other errno logs
`could not open directory` and sets `ret = -1` (`:558-561`), which then hits the `:629` gate. Runs:

- T3 — `/etc/pacman.d/hooks` mode 0000 → `[E] could not open directory: /etc/pacman.d/hooks/: Permission denied`,
  `rc=-1 errnum=32`.
- T16 — hookdir replaced by a regular file → `[E] could not open directory: /etc/pacman.d/hooks/: Not a directory`,
  `rc=-1 errnum=32`.
- T4 — dangling symlink `50-dangling.hook -> /nonexistent/target.hook` → `[E] could not stat file …: No such file
  or directory` (`hook.c:593-597`), `rc=-1 errnum=32`.

Honest caveat: pacman runs as root, and root bypasses the DAC bits T3 exercises, so T3 answers the source
question ("the non-ENOENT branch blocks") rather than claiming a realistic host trigger. The **root-reachable**
forms of the same branch are T16 (`ENOTDIR`) and T4 (a dangling `.hook` symlink, `stat()` follows the link —
`hook.c:593`), plus `EIO`/`ENAMETOOLONG` (`:546-551`, `:574-579`) and a `readdir` error (`:620-624`). Every one of
these sets the same `ret = -1` and blocks the Pre phase **with no parse or validation failure anywhere**. This is
what falsifies the consequence sentence "The one Pre-phase path … is a broken hook file".

## 4. Question 3 — are there cases where parse/validate problems are only warnings? **Yes.**

`hook.c` emits exactly two warning sites (`grep ALPM_LOG_WARNING`: `:142`, `:188`), and both are non-blocking:

- `hook.c:141-144` — `AbortOnFail` on a `PostTransaction` hook logs
  `[W] AbortOnFail set for PostTransaction hook: …` and returns 0. T8: `rc=0 … is_hook_failed=0`. The man page
  says it "only applies to PreTransaction hooks" (`sources/alpm-hooks.5.asciidoc:87-89`), i.e. the file *is*
  invalid per the documented schema and still does not block.
- `hook.c:188` — overwriting a previous `Type` inside one `[Trigger]` is a warning.

Three further non-blocking shapes, all run:

- **T7 — triggerless hook** `[Action] Description = mask only` (no `[Trigger]`, no `Exec`, no `When`):
  `_alpm_hook_validate` returns 0 before any check (`hook.c:119-123`), `rc=0 … is_hook_failed=0`. So "no Exec, no
  When" are **not** parse failures for a file without a `[Trigger]` section — exactly HO3's mask semantics. The
  row's parenthetical is false without that qualifier.
- **T6 — overridden file**: `[D] skipping overridden hook /usr/share/libalpm/hooks/90-shadow.hook`, where that
  file is broken (no Exec). It is skipped at `hook.c:588-591` **before** the parse at `:609`, `rc=0`. So "in
  either directory" needs the HO2 carve-out: on this host the shadowed file is
  `/usr/share/libalpm/hooks/90-mkinitcpio-install.hook`; were *that* copy the broken one, `/etc`'s valid copy
  wins (HO2) and nothing blocks.
- **T12 / T13** — a *directory* named `50-isdir.hook` (`:600-603`) and a non-`.hook` file (`:582-586`) are DEBUG
  skips, `rc=0`.

No genuine parse error is downgraded to a warning: every parse failure uses the `error(...)` macro that returns 1
(`hook.c:156-157`), so the `parse_ini(...) != 0 ||` at `:609` always fires.

## 5. One asymmetry the row should record

The gate is Pre-only by construction (`hook.c:629`), and `trans.c:238` calls
`_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION)` **discarding its return value**. So a hook file that becomes
broken *after* the Pre scan — the concrete case is a package installed by the transaction dropping a malformed
hook, which the Post scan then parses (`/usr/share/libalpm/hooks` is re-scanned) — logs its errors, runs every
Post hook anyway, and `alpm_trans_commit` still returns 0. "The transaction never starts" is a Pre-phase property
only. [INFERENCE] on reachability of that scenario; the two source facts (`hook.c:629`, `trans.c:238`) are direct.

## 6. Closing HO5's own `[unk]`

"A transaction flagged `ALPM_TRANS_FLAG_NOHOOKS` skips both phases (`trans.c:201`, `:237`); which pacman options
set that flag is not read here [unk]" — resolvable, and I read it: `src/pacman/pacman.c:720-724`, the `OP_DBONLY`
case sets `ALPM_TRANS_FLAG_DBONLY | ALPM_TRANS_FLAG_NOSCRIPTLET | ALPM_TRANS_FLAG_NOHOOKS`, i.e. **`--dbonly`**
is the option. `grep -n NOHOOKS` over the fetched `src/pacman/pacman.c`, `conf.c`, `sync.c` yields that single
site; `--hookdir` only *adds* a directory (`pacman.c:483-487`). The `[unk]` can be replaced with a citation.

## 7. Proposed replacement text (tightening only; no new claim about the host)

Replace the HO5 rule cell with:

> Any `.hook` file that is actually parsed — its name ends in `.hook`, it is not skipped as overridden by a
> same-name file in a higher-precedence directory (HO2), and it is not a directory — and that fails to parse or
> validate makes the Pre-phase run return an error **before any Pre hook runs**; `trans.c` turns it into
> `ALPM_ERR_TRANS_HOOK_FAILED` ("failed to run transaction hooks") and the transaction never starts. Validation
> failures require at least one `[Trigger]` section (triggerless files are exempt, HO3): missing `Exec`, missing
> `When`, bad trigger value/type/operation, unknown section, invalid option, unreadable file. The broken file need
> not be a Pre hook: a PostTransaction-only file aborts the Pre phase identically. A transaction flagged
> `ALPM_TRANS_FLAG_NOHOOKS` skips both phases (`trans.c:201`, `:237`); `--dbonly` is the pacman option that sets
> it (`pacman.c:720-724`).

Replace the HO5 host-consequence cell with:

> A broken hook file is *not* the only Pre-phase blocker: `opendir` failing for any reason other than `ENOENT`
> (`hook.c:554-562`), a `.hook` entry that cannot be `stat`ed (`:593-597`, e.g. a dangling symlink), a
> `PATH_MAX` overflow (`:546-551`, `:574-579`) and a `readdir` error (`:620-624`) also return an error and block.
> Non-blocking shapes: a triggerless hook with no `Exec`/`When` (`hook.c:119-123`), `AbortOnFail` on a
> PostTransaction hook (`:141-144`, warning), an overridden file (`:588-591`) and a `*.hook` directory
> (`:600-603`). All three `/etc/pacman.d/hooks/*.hook` files are PostTransaction, so a break in any of them blocks
> an upgrade at the Pre phase rather than skipping a post step. The Post phase is ungated and its error is
> discarded (`trans.c:238`), so only a Pre-scan failure stops a transaction.

If the row is kept verbatim instead, at minimum the parenthetical must gain "in a file that has a `[Trigger]`"
and the consequence must lose "the one".

## 8. Non-findings / limits of this seat

- I did not judge HO1–HO4, HO6, HO7, the 69-row table, or the two counters — other seats own those.
- I did not run a hook to completion (non-root: `chroot` → EPERM). The "no Pre hook ran" result rests on the
  absence of the `running '…'...` line `hook.c:653` writes **before** the exec attempt, which T15 shows is emitted
  normally — so the observable is sound for ordering, and I state it as ordering evidence only.
- No installs, no upgrade, no `pacman` transaction, no service restart, no `/etc` or sysfs write. Tools used were
  already present (`gcc`, `-lalpm`, `curl`); nothing was installed, so there is no tool record to report.
- Host state confirmed untouched after the runs: `/usr/bin/which` present (27280 bytes), `/var/log/pacman.log`
  mtime still 2026-10-25 13:12:06, local DB still lists `which`.
- Scratch `/fast/scratch/hyaku/tsukuroi-r38/C2CritHO5/` removed after the receipts were copied to
  `.ufo/waves/round-38/w1/C2CritHO5/` (`fx.c`, `cases.sh`, `matrix.txt`, `log/T*.out`, `log/T*.err`,
  `fetched-lines.txt`).

HO5: partly — .ufo/waves/round-38/sources/hook.c:609-631 (mechanism holds as run; the parenthetical at `hook.c:119-123` and the "one path" consequence at `hook.c:554-562` are false as written)
