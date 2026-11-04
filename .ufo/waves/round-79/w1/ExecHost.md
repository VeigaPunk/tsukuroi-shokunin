# ExecHost — round 79 wave w1 — host dependency-directive observation

claim=C1-support
verdict=observed

Capture window 2026-11-04T19:08:44Z–2026-11-04T19:09:59Z (UTC), Arch host. All
commands unprivileged read-only; `sudo -n` was never required and never used. No
unit was started/stopped/restarted/enabled/disabled/masked; no unit file edited;
no writes outside `.ufo/waves/round-79/w1/ExecHost*` and scratch
`/fast/scratch/hyaku/tsukuroi-r79/ExecHost/` (scratch deleted before yield).

## Scope of this item

Read-only host observation supporting C1's **practical scope only**. This is NOT a
C1 measurement and does not move the C1 number: the C1 predicate is the eight
pinned DP1–DP8 rows in `corpus/knowledge/systemd-dependency-propagation-r79.json`
matching `.ufo/waves/round-79/before/expected.json` (frozen SHA-256
`0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21`) with a
digest-bound review. The C1 counter is
`python3 tools/measure-unit-deps-r79.py --revision <REV>`; nothing here substitutes
for it. This item grounds what the eight directive classes look like on a real host.

## 1. Directive classes present on this host (bounded grep)

Command (rc 0, stderr 0 lines — nothing unreadable), 2026-11-04T19:08:44Z:

```
grep -rn --include='*.service' --include='*.timer' --include='*.mount' \
  -E '^(BindsTo|PartOf|Upholds|RequiresMountsFor|Wants|Requires|After|Before)=' \
  /etc/systemd /usr/lib/systemd
```

729 matched lines. Counts per directive name: After= 279, Before= 240, Wants= 75,
Requires= 70, PartOf= 24, RequiresMountsFor= 20, BindsTo= 20, Upholds= 1.
Origin: /usr/lib/systemd 729, /etc/systemd 0.

**Bounds — a zero count here is a bounded grep result, not proof the directives are
unused.** Not covered: (a) drop-ins `*.d/*.conf` (26 under /etc, 32 under /usr/lib)
excluded by the `--include` filters and they can add BindsTo=/PartOf=/Upholds=;
(b) generated/dynamic units under /run (generators, systemd-run scopes) were not in
the scanned trees; (c) `grep -r` does not dereference symlinked unit files found
during traversal, so /etc entries pointing into /usr/lib contributed 0 even though
/etc holds 32 `*.service|*.timer|*.mount` entries; (d) `Requisite=` (DP3's
directive) was outside the assigned pattern and is uncounted, not zero.

Host units carrying the failure-propagation classes (same grep):
- DP4+DP6 live pair: `/usr/lib/systemd/system/systemd-coredump-register.service:16: BindsTo=systemd-coredumpd.service` and `/usr/lib/systemd/system/systemd-coredumpd.service:19: Upholds=systemd-coredump-register.service`.
- DP5: `/usr/lib/systemd/system/sddm.service:6: PartOf=graphical.target` (also swayosd-libinput-backend, systemd-nspawn@ → machines.target, xdg-desktop-portal-rewrite-launchers → graphical-session-pre.target, 24 PartOf= hits total).
- DP7: `/usr/lib/systemd/system/pacman-filesdb-refresh.service:3: RequiresMountsFor="/var/lib/pacman/sync"`, plus btrfs-scrub@/xfs_scrub@ family (`RequiresMountsFor=%f`), rpcbind (`/var/lib/rpcbind`).

## 2. Failed units and what their propagation would look like

- `systemctl list-units --state=failed --no-legend --no-pager` (rc 0): **empty — 0
  system failed units**.
- `systemctl --user list-units --state=failed --no-legend --no-pager` (rc 0): **2
  user failed units**, both transient `systemd-run` scopes:
  `run-p1157862-i1164315.scope`, `run-p1159104-i1145275.scope`
  (argv-bearing description columns dropped).
- `systemctl list-units --type=service --state=running --no-legend --no-pager | wc -l`
  (rc 0): **23** running system services.

`systemctl --user show -p Id,ActiveState,Result,Requires,Wants,BindsTo,PartOf,Upholds,RequiresMountsFor <unit>` (both scopes, rc 0, 2026-11-04T19:09:59Z):

| Property | run-p1157862-i1164315.scope | run-p1159104-i1145275.scope |
|---|---|---|
| ActiveState | failed | failed |
| Result | oom-kill | oom-kill |
| Requires | app.slice | app.slice |
| Wants | (empty) | (empty) |
| BindsTo | (empty) | (empty) |
| PartOf | (empty) | (empty) |
| Upholds | (empty) | (empty) |
| RequiresMountsFor | (empty) | (empty) |

Journal (`journalctl --user -b -u <unit> -n 50 --no-pager`, rc 0; "Started
[systemd-run] …" lines withheld as argv-bearing): both scopes were OOM-killed on
Nov 02 (`Failed with result 'oom-kill'`); scope1 consumed 38.434s CPU / 5.183s wall /
3G memory peak; scope2 3min 19.220s CPU / 11.616s wall / 8G memory peak.

**Reading against DP1–DP8:** the failed scopes carry none of the propagation
directives — no BindsTo= (DP4: nothing stops when they failed), no PartOf= (DP5:
nothing propagated their stop), no Upholds= (DP6: nothing will restart them while an
upholding unit is up — they are inert leaves that will sit failed until
`reset-failed`). The only coupling is the implicit `Requires=app.slice` (DP2 class:
an explicit stop/restart of app.slice would stop them, but nothing failed app.slice
and its stop is not an operator scenario here). Conversely the host's DP4+DP6 pair
means: if `systemd-coredumpd.service` ever fails, DP4 stops
`systemd-coredump-register.service`; while coredumpd stays up, DP6 restarts
coredump-register whenever it is found inactive or failed. DP5 means stopping or
restarting `graphical.target` stops `sddm.service`. DP7 means
`pacman-filesdb-refresh.service` cannot start unless the mount providing
`/var/lib/pacman/sync` is up (implicit Requires=+After= per the row).

## 3. What an operator should check next (read-only; no restart, no edits)

1. `journalctl -k -b | grep -iE 'out of memory|killed process'` (wrap with
   `sudo -n` only if the kernel journal is unreadable) — which process pressure
   produced both oom-kill results.
2. `systemctl --user status run-p1157862-i1164315.scope run-p1159104-i1145275.scope --no-pager -l` — cgroup memory/accounting summary (filter argv lines before pasting anywhere).
3. `systemctl --user cat user.slice app.slice --no-pager` — look for MemoryMax/MemoryHigh drop-ins on the user slice chain; a drop-in bound is the only place a limit could hide given the bounded grep above.
4. `systemctl --user list-dependencies --reverse <scope>` — confirm zero reverse dependencies beyond `app.slice`.
5. When done observing, the operator (not this seat) may run
   `systemctl --user reset-failed <scope>` to clear the two failed rows — that is a
   state change and was deliberately not executed here.

## Execution class, deviations, tooling

EXEC-AUTHORIZED as assigned: the listed systemctl/journalctl/grep/`sudo -n`
read-only commands, python3 read-only, no writes outside the wave dir. `sudo -n`
was never needed. Disclosed deviations, all read-only with no state change:
`date` for capture stamps, `mkdir`+`export TMPDIR` for the scratch tree,
`sed`/`sort`/`uniq`/`cut`-style text pipelines and `grep` applied to my own scratch
copy of the grep output, `find` used only to count drop-in/unit files, and
`journalctl --user -b -u <unit>` (user variant of the listed `journalctl -b -u`
family; unprivileged, so no sudo). No tool was installed or updated; the
tooling-authorization clause was not exercised and PACMAN was not touched.

## Receipts

Machine-readable: `ExecHost/receipts.json` (command, rc, sanitized excerpt, UTC
capture time per receipt). Sanitization: unit names, states, results, timings and
memory peaks kept; argv/environment/credential-bearing output (systemd-run
descriptions, journal "Started [systemd-run] …" lines) dropped. Sanitized handoff:
`ExecHost/handoff.md`.
