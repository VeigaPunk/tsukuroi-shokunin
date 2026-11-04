# ExecHost handoff — host dependency-directive observation (round 79, wave w1)

Capture: 2026-11-04T19:08:44Z–2026-11-04T19:09:59Z UTC. Every command unprivileged
read-only; `sudo -n` never required. No unit started/stopped/restarted/enabled/
disabled/masked; no unit file edited. Sanitization applied throughout: unit names,
states, results, timings and memory peaks kept; argv/environment/credential-bearing
output dropped (systemd-run description columns, journal "Started [systemd-run] …"
lines).

## Directive classes on this host (counts per name)

Exact commands and capture times are in `receipts.json`. Main sweep, rc 0,
stderr 0 lines (nothing unreadable), 2026-11-04T19:08:44Z:

```
grep -rn --include='*.service' --include='*.timer' --include='*.mount' \
  -E '^(BindsTo|PartOf|Upholds|RequiresMountsFor|Wants|Requires|After|Before)=' \
  /etc/systemd /usr/lib/systemd
```

| directive | hits |
|---|---|
| After= | 279 |
| Before= | 240 |
| Wants= | 75 |
| Requires= | 70 |
| PartOf= | 24 |
| RequiresMountsFor= | 20 |
| BindsTo= | 20 |
| Upholds= | 1 |

Origin: /usr/lib/systemd 729, /etc/systemd 0. Totals: 729 matched lines.

**Zero counts are bounded grep results, not proof the directives are unused.**
Excluded from this sweep: drop-ins `*.d/*.conf` (26 under /etc, 32 under /usr/lib —
they can carry the same directives), generated/dynamic units under /run (generators,
transient units), symlinked unit files in /etc (grep -r does not dereference them
during traversal; /etc holds 32 `*.service|*.timer|*.mount` entries yet contributed
0 hits), and `Requisite=` which was outside the assigned pattern (uncounted, not
zero).

## Failed units on this host, and their propagation

- System: **0 failed units** (`systemctl list-units --state=failed --no-legend --no-pager`, rc 0, empty).
- User: **2 failed units**, both transient `systemd-run` scopes:
  `run-p1157862-i1164315.scope`, `run-p1159104-i1145275.scope`
  (`systemctl --user list-units --state=failed --no-legend --no-pager`, rc 0).
- Both: `ActiveState=failed`, `Result=oom-kill` (kernel OOM killer, Nov 02).
  Dependency surface from
  `systemctl --user show -p Id,ActiveState,Result,Requires,Wants,BindsTo,PartOf,Upholds,RequiresMountsFor`:
  only `Requires=app.slice`; `Wants=`/`BindsTo=`/`PartOf=`/`Upholds=`/
  `RequiresMountsFor=` all empty.
- **No failed unit carries BindsTo=/PartOf=/Upholds=.** Per the DP rows that means:
  DP4 (BindsTo stops the configuring unit when a listed unit stops unexpectedly,
  including failure) fires nowhere — these oom-kill failures stop nothing else;
  DP5 (PartOf propagates stop/restart of the listed unit) fires nowhere — the
  failures propagated to no sibling; DP6 (Upholds restarts listed units found
  inactive or failed while the configuring unit is up) fires nowhere — nothing will
  resurrect these scopes, and the scopes uphold nothing themselves. The two failed
  scopes are inert leaves: they sit failed until an operator runs
  `systemctl --user reset-failed`. The only DP2-class coupling is the implicit
  `Requires=app.slice`: an explicit stop/restart of `app.slice` would stop them,
  but app.slice has not failed and stopping it is not an operator scenario here.
- Host units that DO carry the propagation classes (from the same sweep), so the
  DP rows have live host referents:
  - DP4+DP6 pair: `systemd-coredump-register.service: BindsTo=systemd-coredumpd.service`;
    `systemd-coredumpd.service: Upholds=systemd-coredump-register.service`.
    If coredumpd fails, coredump-register is stopped (DP4); while coredumpd is up,
    coredump-register is restarted whenever found inactive or failed (DP6).
  - DP5: `sddm.service: PartOf=graphical.target` — stopping/restarting
    `graphical.target` propagates to sddm (24 PartOf= hits total, e.g.
    `systemd-nspawn@.service: PartOf=machines.target`).
  - DP7: `pacman-filesdb-refresh.service: RequiresMountsFor="/var/lib/pacman/sync"`
    (+ btrfs-scrub@, xfs_scrub@ family, rpcbind) — implicit Requires=+After= on the
    mount units for those paths; unit cannot start without the mount up.
  - DP1/DP2/DP8 classes (Wants=/Requires=/After=) are abundantly present (75/70/279
    hits); DP3 (`Requisite=`) uncounted by this sweep, see bounds above.

## Operator next steps (read-only; no restart, no edits)

1. `journalctl -k -b | grep -iE 'out of memory|killed process'` — identify the
   memory pressure behind both oom-kill results (wrap with `sudo -n` only if the
   kernel journal is unreadable).
2. `systemctl --user status run-p1157862-i1164315.scope run-p1159104-i1145275.scope --no-pager -l`
   — cgroup accounting summary; filter argv lines before quoting.
3. `systemctl --user cat user.slice app.slice --no-pager` — check for
   MemoryMax/MemoryHigh drop-ins on the user slice chain; given the sweep bounds,
   a drop-in is the only place a bound could hide.
4. `systemctl --user list-dependencies --reverse <scope>` — confirm zero reverse
   dependencies beyond `app.slice`.
5. `systemctl --user reset-failed <scope>` clears the two failed rows when the
   operator is done observing. State change — recorded here as recommendation
   only, NOT executed by this seat.

Nothing in this handoff restarts, edits, masks or enables anything.

## Companion artifacts

`receipts.json` — per-command rc, sanitized excerpt, UTC capture time.
`../ExecHost.md` — binding report (`claim=C1-support`, `verdict=observed`).
