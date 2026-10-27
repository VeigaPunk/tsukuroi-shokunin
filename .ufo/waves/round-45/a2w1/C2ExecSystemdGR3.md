VERDICT: supports

# C2-4 — GR3 systemd side (seat C2ExecSystemdGR3, wave a2w1, attempt 2)

Read-only throughout: no unit was started, stopped, enabled, disabled, killed or restarted, no sysfs
write, no mount, no sudo, no pacman transaction (transactions are paused host-wide; none attempted), no
lane or fleet write. Every command below ran as uid 1000 with `CapEff=0000000000000000` (my own
`/proc/self/status`; the round's capture records the same for its run, S249 capture.txt:1). Receipts: `.ufo/waves/round-45/a2w1/C2ExecSystemdGR3/` (r1…r10, `unit-paths.txt`,
`svc-timeouts.txt`). Nothing was installed or upgraded, so there is no tool delta to record.

**Bottom line.** All three clauses the item names hold in substance on this host and in systemd v262
source: the drop-in is real, read by the running manager, and unowned by any package; the unit's stop
path resolves to `KillSignal=SIGINT` / `KillMode=control-group` / `TimeoutStopUSec=5s` /
`FinalKillSignal=9` / `SendSIGKILL=yes`; SIGCONT follows each delivered kill signal per recipient.
Three narrowings and one sequencing finding are reported in §7–§8: "every system unit" is really
"every service unit (plus transient scopes)"; the man's "always send SIGCONT" has a SIGKILL exception
in the code; and the
SIGKILL is not always `TimeoutStopSec` after the first SIGINT — systemd inserts a second terminate
stage after the main process exits, with a fresh timeout. None of these change GR3's operative result
for the scrub start, whose own SIGINT→SIGKILL window is the first 5 s stage.

## 1. Drop-in coverage: the capture's /etc-only gap closes with the same answer

The round's capture checked one directory tree. `frozen/hostcap/capture.sh:22` lists only
`/etc/systemd/system/btrfs-scrub@*.service.d`, `/etc/systemd/system/btrfs-scrub@.service.d` and
`/etc/systemd/system/service.d`; its output line is empty (`capture.txt:7`: `unit_dropins `).

I enumerated every directory systemd actually loads units from, not just the three the item names:

```
$ systemd-analyze unit-paths            # receipt unit-paths.txt
/etc/systemd/system.control
/run/systemd/system.control
/run/systemd/transient
/run/systemd/generator.early
/etc/systemd/system
/etc/systemd/system.attached
/run/systemd/system
/run/systemd/system.attached
/run/systemd/generator
/usr/local/lib/systemd/system
/usr/lib/systemd/system
/run/systemd/generator.late
```

Searching `btrfs-scrub@-.service.d`, `btrfs-scrub@.service.d`, `service.d`, `btrfs-scrub@.timer.d`,
`timer.d`, `btrfs-scrub@-.service`, `btrfs-scrub@.service` in all twelve yields exactly one hit, the
packaged `PRESENT /usr/lib/systemd/system/btrfs-scrub@.service` (r2-dropins.txt). No `.d` directory
exists anywhere in the search path. `/usr/local/lib/systemd/system` — a real unit path the item's list
omits — does not exist at all on this host (r2-dropins.txt), so the omission is harmless here.

The manager agrees independently: `DropInPaths=` is empty for all four btrfs mount instances
(`btrfs-scrub@-.service`, `@home`, `@var-cache-pacman-pkg`, `@var-log`; r9-instances.txt). So no
unit-level drop-in can move `KillSignal`, `KillMode` or `TimeoutStopSec` for this unit from any
directory systemd reads. GR3's silence on unit drop-ins is therefore benign, not an unexamined gap.

Packaged unit text, unchanged on this host (`/usr/lib/systemd/system/btrfs-scrub@.service`, sha256
`eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252`, owned by `btrfs-progs-7.1-1`,
r4-ownership.txt):

```
[Service]
Nice=19
IOSchedulingClass=idle
KillSignal=SIGINT
ExecStart=/usr/bin/btrfs scrub start -B %f
```

No `KillMode=`, no `TimeoutStopSec=`, no `ExecStop=`/`ExecStopPost=`, no `Type=` (so `Type=simple`),
which is exactly the configuration GR3 assumes.

## 2. Live values (read-only queries)

```
$ systemctl show btrfs-scrub@-.service -p KillSignal -p KillMode -p TimeoutStopUSec -p FinalKillSignal \
    -p SendSIGKILL -p SendSIGHUP -p RestartKillSignal -p TimeoutStopFailureMode -p FragmentPath \
    -p DropInPaths -p Type -p TimeoutStartUSec
Type=simple
TimeoutStartUSec=1min 30s
TimeoutStopUSec=5s
TimeoutStopFailureMode=terminate
FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service
DropInPaths=
KillMode=control-group
KillSignal=2
RestartKillSignal=2
FinalKillSignal=9
SendSIGKILL=yes
SendSIGHUP=no
```
(r1-show.txt; the same six values for all four instances in r9-instances.txt. `KillSignal=2` is SIGINT;
`RestartKillSignal=2` is derived from it — v262 `src/core/kill.c:14` "restart_kill_signal is unset by
default and we fall back to kill_signal".)

```
$ systemctl show -p DefaultTimeoutStartUSec -p DefaultTimeoutStopUSec -p DefaultTimeoutAbortUSec
DefaultTimeoutStartUSec=1min 30s
DefaultTimeoutStopUSec=5s
DefaultTimeoutAbortUSec=5s
$ systemctl --user show -p DefaultTimeoutStopUSec
DefaultTimeoutStopUSec=1min 30s
```
(r1-show.txt, §9). The system manager's default stop timeout is 5 s and the unit has no value of its
own, so the 5 s on the unit is inherited, not set. The user manager still reports 90 s: the drop-in is
in `systemd/system.conf.d`, which the system manager reads and the user manager does not.

## 3. The drop-in itself

```
$ cat -A /etc/systemd/system.conf.d/10-faster-shutdown.conf
[Manager]$
DefaultTimeoutStopSec=5s$
$ stat -c '%n %F %U:%G %a %s' /etc/systemd/system.conf.d/10-faster-shutdown.conf
/etc/systemd/system.conf.d/10-faster-shutdown.conf regular file root:root 644 35
$ sha256sum /etc/systemd/system.conf.d/10-faster-shutdown.conf
dbd88d8f4f55a28d51b19fb6ccb2679ad14f07041192e0dac1eceb5b66b06f35
```
(r3-config.txt.)

`systemd-analyze cat-config systemd/system.conf` reads three files — `/etc/systemd/system.conf` (whose only
uncommented line is the `[Manager]` section header), `/etc/systemd/system.conf.d/10-faster-shutdown.conf`,
`/etc/systemd/system.conf.d/99-omarchy-nofile.conf`
— and the only non-comment settings are `DefaultTimeoutStopSec=5s` and `DefaultLimitNOFILE=65536:524288`
(r3-config.txt). Nothing later overrides the stop timeout. `/run/systemd/system.conf.d` and
`/usr/lib/systemd/system.conf.d` do not exist, so the /etc copy is the only source for the value.

## 4. v262 defaults for `DefaultTimeoutStopSec` and `TimeoutStopSec` (item requirement)

man.archlinux.org was unreachable from this seat; I record both attempts rather than claim them:

```
$ curl -sSL https://man.archlinux.org/man/systemd-system.conf.5.en        # 2026-10-27T03:26:28Z
curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading
$ curl -sSL --http1.1 https://man.archlinux.org/man/systemd-system.conf.5.en   # 2026-10-27T03:29:55Z
curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading
```
(r5-urls.txt). The item's fallback, "the v262 tag sources", was used instead, plus the host's own
rendered page from `systemd-262-1-arch`.

**`man/systemd-system.conf.xml` @ v262**, https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml,
accessed 2026-10-27T03:25:10Z, sha256 `161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58`:

- line 652: "Configures the default timeouts for starting, stopping and aborting of units, as well"
- lines 661–663: "`DefaultTimeoutStartSec=` and `DefaultTimeoutStopSec=` default to
  `&DEFAULT_TIMEOUT_SEC;` in the system manager and `&DEFAULT_USER_TIMEOUT_SEC;` in the user manager."
- lines 657–658: "For non-service units, `DefaultTimeoutStartSec=` sets the default `TimeoutSec=` value."

**`man/systemd.service.xml` @ v262**, https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml,
accessed 2026-10-27T03:25:10Z, sha256 `12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44`:

- lines 724–727: "Defaults to `DefaultTimeoutStopSec=` from the manager configuration file"
  (with 718–721: "configures the time to wait for the service itself to stop … forcibly terminated by
  `SIGKILL`").

The entities resolve only at build time, so I read the numbers off the host's installed rendered pages
(`systemd-262-1-arch`, same v262 text; r8-man-local.txt): "default to 90 s in the system manager and
90 s in the user manager." That is the baseline the 5 s drop-in replaces, and it matches the live
`DefaultTimeoutStartUSec=1min 30s`.

**Code path for the default.** v262 `src/core/manager.c:5558-5559` seeds the manager defaults with
`manager_default_timeout(scope)` (`src/core/manager.c:895`: `DEFAULT_TIMEOUT_USEC` for the system scope,
`DEFAULT_USER_TIMEOUT_USEC` for the user scope), and `src/core/service.c:195-196` copies them onto every
service at load:

```
195:        s->timeout_start_usec = u->manager->defaults.timeout_start_usec;
196:        s->timeout_stop_usec = u->manager->defaults.timeout_stop_usec;
```

The config file value then overwrites `defaults.timeout_stop_usec` (`src/core/manager.c:4645`), which is
why the live unit shows 5 s while the unit file sets nothing. This is the mechanism GR3 asserts; it is
confirmed both ways (file → manager property → unit property).

## 5. Ownership of the drop-in (`/var/lib/pacman/local/*/files`)

Method used by the capture (`capture.sh:19-20`) and repeated here verbatim, plus a positive control so a
broken lookup cannot masquerade as "unowned" (r4-ownership.txt; 1410 package directories):

```
etc/systemd/system.conf.d/10-faster-shutdown.conf          -> NONE
etc/systemd/system.conf.d/99-omarchy-nofile.conf           -> NONE
etc/systemd/system/user@.service.d/faster-shutdown.conf    -> NONE
etc/systemd/system.conf.d                                  -> NONE
etc/systemd/system.conf.d/                                 -> NONE
etc/systemd/system.conf                                    -> systemd-262-1     (positive control)
usr/lib/systemd/system/btrfs-scrub@.service                -> btrfs-progs-7.1-1 (positive control)
$ grep -rl 'faster-shutdown' /var/lib/pacman/local/ | wc -l
0
```

So: no package owns the drop-in, and none owns its directory either. The only `systemd` package entries
mentioning `system.conf.d` are the man pages (`systemd-262-1/files:1574,1576`). GR3's "no package owns
that drop-in" is exact, including the stronger form (the directory is unowned local configuration too).
It is unprivileged-visibility evidence only: the pacman database is read, no package database is
modified and no package manager binary is invoked for a transaction.

## 6. SIGCONT ordering

GR3: "Right after that signal systemd sends SIGCONT."

Documented: frozen `S248` (`frozen/src/systemd.kill.xml`, sha256
`448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72`, equal to the frozen SHA256SUMS
entry — recomputed today) under `KillSignal=`:

- line 114: "Note that, right after sending the signal specified in this setting, systemd will always send"
- line 115: "`SIGCONT`, to ensure that even suspended tasks can be terminated cleanly."

In code (v262, all fetched 2026-10-27, hashes in r5-urls.txt):

- `src/core/unit.c:5108,5111` signal the main and control pids through `unit_kill_context_one`, which
  calls `pidref_kill_and_sigcont` (`unit.c:5036`); `src/basic/pidref.c:363-374` sends `pidref_kill(sig)`
  and then, if that succeeded and `sig` is neither `SIGCONT` nor `SIGKILL`, `pidref_kill(SIGCONT)`.
- `src/core/unit.c:5144-5156`, the `KillMode=control-group` path this unit uses, calls
  `cg_kill_recursive(crt->cgroup_path, sig, CGROUP_SIGCONT|CGROUP_IGNORE_SELF, pid_set, …)`, where
  `pid_set` excludes the main/control pids already signalled. `src/basic/cgroup-util.c:320-330` kills each
  enumerated pid and then does `(void) pidref_kill(&pidref, SIGCONT)` in the same iteration;
  `cgroup-util.c:264-265` strips `CGROUP_SIGCONT` when `sig` is `SIGCONT` or `SIGKILL`. The enumeration
  repeats until no new pid appears, so processes forked during the stop are caught too.

So "right after" is literal (the SIGCONT is the next syscall for that recipient), with the narrowings in
§7.

## 7. Clause-by-clause

**7.1 "sets `DefaultTimeoutStopSec=5s` for every system unit without its own value" — holds for service
(and scope) units; the breadth word needs narrowing.**
Every service unit that inherits shows 5 s, and the exceptions are exactly the units that set their own
value. Survey of the 140 loaded service units (`svc-timeouts.txt`, r7-survey.txt):

```
    124 5s
      9 1min 30s
      4 infinity
      1 3min
      1 20s
      1 10min
```
The 16 exceptions each carry their own `TimeoutSec=`/`TimeoutStopSec=`, verified in the unit files: the
nine at 1 min 30 s are exactly the `systemd-*` units that set `TimeoutSec=90s`
(`systemd-binfmt`, `systemd-hwdb-update`, `systemd-journal-catalog-update`, `systemd-journal-flush`,
`systemd-machine-id-commit`, `systemd-modules-load`, `systemd-rfkill`, `systemd-sysctl`,
`systemd-sysusers`); `plymouth-quit.service:9 TimeoutSec=20`; `systemd-udev-settle.service:25
TimeoutSec=180` (3 min); `systemd-random-seed.service:35 TimeoutSec=10min`; and four `infinity`
(`plymouth-quit-wait.service:9 TimeoutSec=0`, `systemd-fsck-root.service:24`,
`systemd-fsck@.service:24`, `systemd-quotacheck-root.service:25`). Every one of the 140 either
inherits 5 s or sets its own value; none falls back to the 90 s compile-time default.

Narrowing (a): **it reaches services and scopes only; other unit types do not read this default.**
Grepping every v262 `src/core` unit-type file for `defaults.timeout_*usec` (r10-unit-types.txt) shows
the stop default is copied onto services (`service.c:196`) and scopes (`scope.c:44`:
`s->timeout_stop_usec = u->manager->defaults.timeout_stop_usec;`), and on nothing else: sockets, mounts
and swaps seed their `TimeoutSec=` from the *start* default — `src/core/socket.c:127`,
`src/core/mount.c:187`, `src/core/swap.c:142` all assign `u->manager->defaults.timeout_start_usec` —
which the drop-in leaves at 90 s, and `automount.c`, `path.c`, `device.c`, `timer.c`, `slice.c`,
`target.c` reference neither timeout. Observed:

```
$ systemctl show -p Id -p TimeoutUSec -p TimeoutStopUSec -- systemd-journald.socket systemd-udevd-varlink.socket -.mount dev-hugepages.mount
Id=systemd-journald.socket       TimeoutUSec=1min 30s
Id=systemd-udevd-varlink.socket  TimeoutUSec=1min 30s
Id=-.mount                       TimeoutUSec=1min 30s
Id=dev-hugepages.mount           TimeoutUSec=1min 30s
```
(no `TimeoutStopUSec` property is emitted for these types. `systemd-udevd-control.socket` is a symlink to
`systemd-udevd-varlink.socket` on this host — v262 merged the control socket into varlink — so querying
either name reports `Id=systemd-udevd-varlink.socket`.) Scopes, the other type that reads the stop
default, do show it:

```
$ systemctl show -p Id -p TimeoutStopUSec init.scope session-2.scope
Id=init.scope        TimeoutStopUSec=5s
Id=session-2.scope   TimeoutStopUSec=5s
```

So the accurate breadth is "every service and scope unit of the system manager without its own value",
not "every system unit"; a scope carries no configuration of its own, so in practice the sentence means
services. The man sentence quoted in §4 says the same:
"For non-service units, `DefaultTimeoutStartSec=` sets the default `TimeoutSec=` value."

Narrowing (b): "system unit" excludes user-manager units — the user manager reports
`DefaultTimeoutStopUSec=1min 30s` (§2). GR3 already says "system", so this is a confirmation, not a
correction; it matters only if a reader generalises to the whole host.

**7.2 "no package owns that drop-in" — holds exactly, including the directory.** See §5 (with positive
controls).

**7.3 SIGCONT "right after" — holds; the man's "always" is bounded by the code.**
Narrowing (c): SIGCONT is (i) sent per recipient inside the enumeration loop, not as one event after the
whole control group has been signalled, so processes are not synchronised; (ii) skipped when the
delivered signal is `SIGKILL` or `SIGCONT` (`cgroup-util.c:264-265`, `pidref.c:370`,
`process-util.c:932`) — so after the *final* kill signal there is no SIGCONT, despite "always" in `S248`
line 114; (iii) sent only if the first `kill()` succeeded, and a process may be gone by then (the second
call is ignored). For the case GR3 asserts — after `KillSignal=SIGINT` — it holds unconditionally.

## 8. Finding beyond the three clauses: the stop sequence has two terminate stages, so "SIGKILL after
`TimeoutStopSec`" is true per stage, not from the stop request

v262 `src/core/service.c`, with `Type=simple`, no `ExecStop=` and no `ExecStopPost=`:

1. `systemctl stop` → `service_enter_stop` → `service_enter_signal(SERVICE_STOP_SIGTERM)` (`service.c:2672-2705`):
   `unit_kill_context(KILL_TERMINATE)` sends the KillSignal (SIGINT) plus SIGCONT to the control group and
   arms `s->timeout_stop_usec` (`service.c:2689`), state `STOP_SIGTERM` (`KILL_TERMINATE` for
   `STOP_SIGTERM`/`FINAL_SIGTERM`: `service.c:2655-2661`).
2. When the main process exits, `service_sigchld_event` → `service_enter_stop_post` (`service.c:4674-4679`),
   and with no `ExecStopPost=` that function's else-branch calls `service_enter_signal(SERVICE_FINAL_SIGTERM, …)`
   (`service.c:2644-2645`). That **re-sends the same KillSignal (SIGINT) plus SIGCONT** to any remaining
   processes and arms a **fresh** `timeout_stop_usec` (`service.c:2687-2695`).
3. Only when that second window expires does `service_dispatch_timer`'s `SERVICE_FINAL_SIGTERM` branch
   escalate: "State 'final-sigterm' timed out. Killing." → `service_enter_signal(SERVICE_FINAL_SIGKILL, …)`
   (`service.c:5311-5317`), which sends `FinalKillSignal=9` with no SIGCONT.
4. If instead the main process lingers through the first window, `STOP_SIGTERM` times out straight to
   `STOP_SIGKILL` (same timer, "Stopping timed out. Killing.") — one 5 s window.

Consequences for GR3's wording:

- For the scrub start (the main process) the effective window from SIGINT to SIGKILL is still
  `TimeoutStopSec=` = 5 s; GR3's inference "whether the start writes its canceled record within the 5 s
  before SIGKILL" is unaffected.
- A *leftover* process (a child still in the cgroup after the main exits) can be signalled SIGINT **twice**
  and may see SIGKILL up to ≈2×5 s = 10 s after the stop request, not 5 s. GR3's "the request is repeated
  with SIGKILL" therefore omits an intermediate repetition of the KillSignal.
- Nothing here was observed at runtime: the host guard forbids stopping units, `btrfs-scrub@.timer` is
  `disabled` and no `btrfs-scrub*` instance is loaded or active (r9-instances.txt). This finding is
  state-machine reading of the pinned v262 sources, not a live trace.

## 9. Adjacent observation (same drop-in, different timeout)

Because `DefaultTimeoutAbortSec=` is unset, the watchdog-abort window follows the stop default too:
`src/core/manager.h:554-557` — `manager_default_timeout_abort_usec()` returns
`timeout_abort_set ? timeout_abort_usec : timeout_stop_usec` — which is why
`DefaultTimeoutAbortUSec=5s` (§2) while `/etc/systemd/system.conf` still shows the commented 90 s baseline.
The man text agrees: "`DefaultTimeoutAbortSec=` is not set by default so that all units fall back to
`TimeoutStopSec=`" (`systemd-system.conf.xml:663-664`). Not part of GR3; recorded because it is a second
effect of the same drop-in on this host.

## 10. What I did not do

- Did not stop, start, kill, restart, enable or disable any unit; did not write `scrub_speed_max`; did not
  run `btrfs scrub`/`btrfs replace`. Hence no runtime packet/trace evidence for the signal order — the
  ordering is grounded in the pinned v262 sources and the shipped man page only, plus the live resolved
  property values.
- Did not read the btrfs-progs side of the stop path (`btrfs scrub start -B`'s SIGINT handler,
  `BTRFS_IOC_SCRUB_CANCEL`); that is SR9 / the btrfs half of GR3 and belongs to the other seats.
- Did not test a counterfactual 90 s timeout (that would need a manager restart), and did not re-run the
  round's capture script (its `/etc`-only drop-in line is superseded by §1's full-path enumeration).
- man.archlinux.org fetch failed twice (TLS, §4); substituted the v262 tag sources plus the host's
  installed rendered pages.

## 11. Proposed narrowings (for the L1; GR3 text is frozen, so this is a proposal only)

Replace

> the drop-in `/etc/systemd/system.conf.d/10-faster-shutdown.conf` sets `DefaultTimeoutStopSec=5s` for
> every system unit without its own value, no package owns that drop-in

with

> the drop-in `/etc/systemd/system.conf.d/10-faster-shutdown.conf` sets `DefaultTimeoutStopSec=5s`, which
> every service (and transient scope) unit of the system manager without its own
> `TimeoutStopSec=`/`TimeoutSec=` inherits — 124 of the 140 loaded service units here, plus `init.scope`
> and the session scopes, including all four `btrfs-scrub@` instances; other unit types keep the 90 s
> default, since their `TimeoutSec=` is seeded from `DefaultTimeoutStartSec=`; no package owns the
> drop-in (nor its directory)

and, for the signal order, append after "Right after that signal systemd sends SIGCONT.":

> per recipient, immediately after the `kill()` that delivered the signal, and not when the signal
> itself is `SIGKILL`; if the main process exits during the stop, systemd re-sends the same `KillSignal=`
> plus SIGCONT once (state `final-sigterm`) with a fresh `TimeoutStopSec=` before escalating to
> `FinalKillSignal=`, so a leftover process can be INT-signalled twice and reach SIGKILL up to two
> timeout windows after the stop request, while the main process's own window remains one
> `TimeoutStopSec=`.

## Receipts (in `.ufo/waves/round-45/a2w1/C2ExecSystemdGR3/`)

| file | content |
|---|---|
| r1-show.txt | unit kill/timeout properties + manager defaults (`systemctl show`) |
| r2-dropins.txt | 12-dir unit-path existence + full drop-in enumeration |
| r3-config.txt | `systemd-analyze cat-config system.conf` files+settings, drop-in bytes/stat/sha256 |
| r4-ownership.txt | pacman local-db ownership with positive controls |
| r5-urls.txt | fetch log (URLs, access times, sizes), 2 failed man.archlinux.org attempts, sha256 of every fetched v262 file |
| r6-sigcont.txt | S248 SIGCONT text + `cgroup-util.c`/`unit.c`/`process-util.c`/`pidref.c`/`kill.c` excerpts |
| r7-survey.txt | 140-unit stop-timeout distribution and the 16 exceptions |
| r8-man-local.txt | host rendered `systemd.service(5)`/`systemd.kill(5)`/`systemd-system.conf(5)` excerpts |
| r9-instances.txt | per-instance properties of all four `btrfs-scrub@` instances, timer state |
| r10-unit-types.txt | which v262 unit-type files consume `defaults.timeout_stop_usec` + `init.scope`/`session-2.scope` at 5 s |
| svc-timeouts.txt | raw unit→TimeoutStopUSec pairs |
| unit-paths.txt | `systemd-analyze unit-paths` |

Scratch `/fast/scratch/hyaku/tsukuroi-r45/C2ExecSystemdGR3/` held the fetched v262 sources and all receipt
generation; it is removed after the receipts above were copied here. No lane file, fleet file, PATH
directory, unit, service, timer or sysfs attribute was written.
