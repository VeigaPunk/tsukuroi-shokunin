VERDICT: defect-found

# C2SentHooks — security reading of the operator hook `walker-restart.hook` (item C2-16)

Scope: read-only. No transaction, no sudo, no package/service/sysfs/boot/`/etc` change, no git/jj write,
no clone. Receipts (raw command outputs) at `.ufo/waves/round-38/w1/C2SentHooks/receipts.md`.

## 0. What the capture says (basis)

`walker-restart.hook` is 11 lines, live file byte-identical to the frozen capture
(`sha256 6581717…88b9` both sides; `receipts.md` §1). The hook file itself is root-owned and sane
(`/etc/pacman.d/hooks` root:root 755, hook root:root 644). The defect is not in the hook file.

```
[Trigger] Type = Package / Operation = Upgrade / Target = walker, walker-debug, elephant*
[Action]  When = PostTransaction
          Exec = /home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker
```

## 1. F1 [HIGH] Root exec of a user-writable, package-unowned script — user→root escalation

**Writer set.** Exactly `{uid 1000 (vgpnk), root}`. The target is `vgpnk:vgpnk 755`, 709 B, no named ACL
(`getfacl`); `/home/vgpnk` is `700 vgpnk`, so no other local account can even traverse; the two parent
dirs are `vgpnk:vgpnk 755`. No package owns the file — `pacman -Qo` → `error: No package owns …`
(`receipts.md` §2). It is tracked clean in the user's own checkout of `basecamp/omarchy`
(`git ls-files` hits, `status --porcelain` empty, blob sha256 == working file) — so **today's bytes are
genuine upstream** (last touched `d2a4cc0`, 2026-05-01). This is a trust-placement defect, not an
observed compromise.

**Exploit path (described, not operationalised).**

1. Obtain code execution as uid 1000 — any user-level primitive: browser renderer RCE, a `yay`/AUR
   `build()` (yay 13.0.1-1 is installed, `update-safety-note.md:215`; helper `build()` runs as the invoking user — standard helper behaviour, not exercised here),
   an npm/pip postinstall, an editor plugin. No root needed at this step.
2. Rewrite `/home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker` (owner-writable; the directory
   permits rename/replace; `pacman -Qo` proves no package will restore or verify it, so `pacman -Qkk`
   cannot see the change and no upgrade overwrites it).
3. Wait for an ordinary `pacman -Syu` that upgrades `walker` or any `elephant*`. This needs no attacker
   action: 3 firings are already in the log — `/var/log/pacman.log:2034` (2026-10-11),
   `:3062` (2026-10-20, transaction containing `walker 2.17.0-1 -> 2.17.2-1`),
   `:3123` (2026-10-20, transaction containing `elephant-unicode/-todo/-menus 2.21.0-1 -> 2.22.1-1`,
   `:3115-3122`).
4. libalpm runs the Exec at PostTransaction via `_alpm_run_chroot(handle, hook->cmd[0], hook->cmd, …)`
   — the path executed as given, argv from `wordsplit`, no shell (`hook.c:525-528`, `:239`), as the
   pacman invoker = **root**. Empirically the script took its `EUID == 0` branch on all three firings:
   that branch is the only one calling `systemd-run` (`omarchy-restart-walker:17-21`), and its stdout
   `Running as unit: run-p…service` appears as `[ALPM-SCRIPTLET]` in the log (`pacman.log:2035`, `:3063`,
   `:3124`). No privilege drop occurs in the captured path.
5. The payload runs as root after `transaction completed`. Failure is silent by design: the Pre-phase
   result is checked and aborts (`trans.c:202`), the Post-phase result is not (`trans.c:238`,
   `_alpm_hook_run(...)` return discarded — this is HO6's source). So a crashed or non-zero Exec yields
   exit 0, no `AbortOnFail` (the hook has none; `AbortOnFail` is Pre-only anyway,
   `alpm-hooks.5.asciidoc:87-89`, `:23`). The only trace is `[ALPM-SCRIPTLET]` stdout in pacman.log, which the
   payload — as root — can edit.
6. Persistence: root. Detonation is deferred to a moment the operator initiated deliberately, which is
   the worst place to look for it (a "successful" update).

**Why libalpm does not stop it.** The loader stats only the `.hook` file (`hook.c:593`); validation
checks only that `Exec` is present (`hook.c:131-135`, "Missing Exec option") and that `When`/triggers
parse. Nothing resolves, stats, or checks the Exec target's owner, mode, or location, and the Exec may be
any absolute path. Contrast the two other `/etc` hooks in the same table: row 69 execs
`/usr/share/libalpm/scripts/limine-mkinitcpio-install` (owned by `limine-mkinitcpio-hook 1.40.0-2`) and
row 71 execs `/bin/sh` (glibc) — root-owned, `pacman -Qkk`-verifiable content.

**Impact.** Full local privilege escalation from the everyday desktop account to root, persistent and
silent, triggered by routine maintenance. Blast radius is the host (boot artefacts, keys, vault, the
package DB the lane audits). Integrity of the executed code rests on (a) uid 1000 and (b) TLS-only
integrity of a GitHub checkout — neither is a signature or a package digest.

**Smallest remediation (for the owner, not this lane).** Make the Exec root-owned and package-verified:
ship the restart action as a package-owned script (`/usr/share/libalpm/scripts/…` from the `walker` /
`elephant` / `omarchy` packaging) and point the hook at it, or drop the hook and restart the launcher
manually after those upgrades. Deleting the hook alone removes root-exec but loses the restart behaviour
the note relies on (`update-safety-note.md:162`). This seat cannot apply either (host mutation is
forbidden) and did not.

## 2. F2 [MED] The hook-order entry should state the trust class — one bullet, no analysis

`corpus/knowledge/pacman-hook-order-r38.md:101` is the **only** row of 69 whose `exec` cell is outside
`/usr/`|`/bin/` (verified by awk over the table; `receipts.md` §6). Its `dir = etc` column records where
the *hook file* lives, which invites the inference that row 52 is operator/root-controlled like rows 69
and 71 — while the executed bytes are not. Combined with HO6 ("a Post hook's failure is ignored",
`:26`) and the entry's opening ("Nothing here authorizes a package, hook or transaction action", `:10-11`),
a reader planning an upgrade from this table gets the ordering right and the trust class wrong.

**Recommendation: yes, state it — one factual line, and route the judgement out.** Proposed exact text,
appended as a fourth bullet under `## Observed / inferred / unknown` (after line 106):

```
- [obs] Row 52 is the only one of the 69 whose `Exec` target is not root-owned package content:
  `/home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker` is `vgpnk:vgpnk 755`, owned by no
  package (`pacman -Qo`), and tracked in the user's `basecamp/omarchy` checkout, while rows 69 and 71
  exec package-owned files (`limine-mkinitcpio-hook 1.40.0-2`, glibc). libalpm stats only the `.hook`
  file (`hook.c:593`) and validates only that `Exec` is present (`hook.c:131-135`); the path is run as
  given (`hook.c:525-528`) and a PostTransaction failure is not propagated (`trans.c:238`, HO6). The
  privilege question is not analysed here; it is routed out (`update-safety-note.md:232-238`, and the
  `PROVINCE.md` ADJ row proposed in §3 below).
```

Counter safety: `entry_rows` in `tools/check-hook-order-r38.py:141-154` reads table lines only between
the `## Effective hook order (r38 capture)` heading and the next `## ` heading (it `break`s), and
`source_check` reads only the first `source:` line (`:157-158`). A bullet under
`## Observed / inferred / unknown` cannot change `rows_expected`, `rows_matched`, `extra_rows` or
`source_ok`. **Do not** edit the row-52 cells instead: the counter compares the full 7-tuple, so an
edited `exec` cell becomes a `mismatch`. C2's kill rule (HO1–HO7 verdicts) is untouched by a prose
bullet. The edit needs a new commit and a re-run by the C2 owner; this seat made no lane edit.

## 3. F3 [MED] The lane routes it in prose only; the formal ADJ table has no matching row

Already routed (all present, verified):

- `corpus/knowledge/update-safety-note.md:232-238` — "a **user-owned, operator-writable script run by
  root inside the transaction** (file present: 709 B, mode 755) ⇒ cross-domain observation, reported not
  absorbed (secrets/privilege lane is kagi's; the fleet owner decides)". Factually correct against this
  reading (709 B, 755 confirmed).
- `:404-405` — open question "whether `walker-restart.hook` exec'ing a user-owned script as root is
  intended (operator question)".
- `:445` (sources), `:471` (§11 "Reported, not absorbed … privilege/secrets shape → kagi or the
  operator").
- `SCORECARD.md:52` (repeated in later scorecards) — "`walker-restart.hook` root-exec → kagi/operator"
  inside the adjacency evidence.

Gap: **`PROVINCE.md` has no such row.** `grep -n "walker" PROVINCE.md` returns exactly one line — `:124`
(`OUT-004`/`ADJ-03` → **mado**, who owns the walker *configuration* plane). That is a false attractor for
this question: the defect is the privilege boundary, not the launcher's config. The only kagi handoff is
`ADJ-02` (`PROVINCE.md:47`), whose trigger is "A **credential-bearing helper** has a permission/ownership
finding **or an auth-flow question**" — the walker script carries no credential and is not an auth flow,
so by `PROVINCE.md:59`'s own rule ("select the matching row by the question being asked") a reader has no
row to select. Routing therefore exists as prose + a SCORECARD axis claim, not as formal ownership.

**Owner.** The privilege mechanism is **kagi** (`update-safety-note.md:236`, `SCORECARD.md:52`); the
**operator** owns the intent decision (`update-safety-note.md:404-405`); if that stays unresolved the
lane's own fallback applies — "unresolved ownership goes to the protocol integrator"
(`PROVINCE.md:41-42`). This seat did not read `../kagi-shokunin/PROVINCE.md` (sibling lane, out of bounds
here), so kagi's accept-side province is unverified; `PROVINCE.md:47`'s kagi citation is likewise taken
as given, not re-read.

Proposed new row for `PROVINCE.md`'s ADJ table (exact text; authority is the planner's, not this seat's):

```
| ADJ-08 | A root-executed path (ALPM hook `Exec`, unit `ExecStart`) is user-writable or not package-owned | Hook/unit file ownership; the Exec target's mode, uid/gid and `pacman -Qo` result; the triggering transaction | kagi (privilege mechanism); the operator decides whether the root exec stays | Path, mode, uid/gid, `pacman -Qo` result, capture time, the triggering `pacman.log` line, and the libalpm line showing no Exec-path check. No payload, no transaction run | `../kagi-shokunin/PROVINCE.md:3-6,10-17` (not read by this seat) |
```

Do not absorb: the security judgement, the "is this intended" ruling, and any remediation stay with
kagi/operator. The only thing C2 should carry is the one factual line in §2.

## 4. F4 [LOW] Trigger set — one dead target, one open glob

`Type = Package`, `Operation = Upgrade` only (a fresh *install* of `walker` does not fire;
`hook.c:363-386` separates install from upgrade by `pkg->oldpkg`).

- `walker` — installed, `2.17.2-1`.
- `walker-debug` — **not installed** (`error: package 'walker-debug' was not found`): dead target, and
  its presence implies a debug-repo expectation that does not hold here.
- `elephant*` — a glob (`alpm-hooks.5.asciidoc:61-67` "Shell-style glob patterns are allowed";
  matched by `_alpm_fnmatch_patterns(t->targets, pkg->name)`, `hook.c:372`), matching **13** installed
  packages (`elephant`, `-bluetooth`, `-calc`, `-clipboard`, `-desktopapplications`, `-files`, `-menus`,
  `-providerlist`, `-runner`, `-symbols`, `-todo`, `-unicode`, `-websearch`; the 09:31 transaction also
  pulled in the `-debug` variants). The set is open-ended: any future package whose name begins with
  `elephant`, from any channel, joins it. Not an escalation by itself (installing such a package already
  implies package-level trust), but it is why the firing rate is not tied to `walker` at all.

## 5. F5 [LOW, operability] The restart can fail invisibly

Two silent-failure modes, both consequences of the same placement: (a) if the script is missing,
renamed, or loses `+x`, the Post hook fails and `trans.c:238` discards the result — the upgrade succeeds
and the launcher keeps running the old code, precisely the state `update-safety-note.md:162` warns about
("old code until relogin"); (b) the actual restart happens inside the transient `systemd-run` unit, so
its `echo "Unable to restart Walker -- RESTART MANUALLY"` (`omarchy-restart-walker:13`) goes to the
journal, not to pacman's output — pacman.log records only the wrapper's `Running as unit:` line, which is
printed before the unit runs. The operator therefore sees "hook ran" whether or not the restart worked.
[inference from the script's control flow + the log's SCRIPTLET lines; not exercised — no transaction run.]

## 6. What I did not do

No transaction, no package operation, no service action, no sudo, no host mutation, no `/etc` write, no
lane edit, no git/jj command in the lane, no clone, no scratch dir (none was needed — every probe was a
read of pinned snapshots, the live hook, `pacman.log`, and the live path's metadata), no tool installs,
no sibling lane read. `tools/check-hook-order-r38.py` was not run (not this item; C2's counter is a
separate seat) — its parsing was read statically for §2. The exploit was not executed or staged; the
script's current bytes were verified to match upstream HEAD, so no tamper evidence exists at capture
time (`2026-10-26`).
