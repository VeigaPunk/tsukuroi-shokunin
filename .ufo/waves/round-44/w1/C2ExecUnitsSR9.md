VERDICT: supports

# C2-6 — SR9's systemd side: `KillSignal=`, `Persistent=`, `RandomizedDelaySec=`, `WantedBy=`, `%f`, and the `systemctl enable` link (seat C2ExecUnitsSR9)

Item: verify read-only the systemd half of SR9 in `corpus/knowledge/btrfs-scrub-record-r44.md` at
`7e081698d4fc3c4ea944884fd093058de9909de1` — what `KillSignal=` means for `systemctl stop` (signal, target
processes, `KillMode=` default), `Persistent=`, `RandomizedDelaySec=`, `WantedBy=` and the `%f` specifier — and
decide whether "enabling an instance creates a `timers.target.wants/btrfs-scrub@<instance>.timer` link" is right for
a template unit with `WantedBy=`. Nothing was enabled, started, stopped, masked, written to sysfs or otherwise
changed: every command below is a `man`, `systemctl show|cat|is-enabled|list-timers|list-dependencies`, `sha256sum`,
`ls`, `readlink` or `systemd-escape` read. No counter was run (not needed here; the C2 counter is the L1's).

**Answer in one line:** SR9's systemd side is correct in every clause I checked. `KillSignal=SIGINT` is exactly the
first-step signal a stop job sends, to *all* remaining processes in the unit's control group (`KillMode=` default
`control-group`), not merely to the main process; `Persistent=true` stores a stamp and catches up missed runs
subject to `RandomizedDelaySec=`; `RandomizedDelaySec=1w` adds an evenly distributed 0–1w delay on top of the
calendar point; `WantedBy=timers.target` + `systemctl enable <instance>` does create
`/etc/systemd/system/timers.target.wants/btrfs-scrub@<instance>.timer` pointing at
`/usr/lib/systemd/system/btrfs-scrub@.timer`; and `%f` for instance `-` is `/` (visible in the effective
`ExecStart`). Five precision items (D1-D5), one of them host-specific, belong in the row; the `Limits` sub-item
that calls this behaviour "not pinned" can now cite the man page and be closed.

## 1. Pages, versions, method

- Local: `systemd 262 (262-1-arch)` (`systemctl --version`); `/usr/share/man/man5/systemd.{kill,timer,unit,service}.5.gz`
  are owned by `systemd 262-1` (receipts:5-9).
- Online: `https://man.archlinux.org/man/{systemd.kill.5,systemd.timer.5,systemd.unit.5,systemctl.1,systemd.service.5,systemd.special.7}.en`,
  accessed 2026-10-26; each page's footer reads **`systemd 262.1`, package `core/systemd 262.1-1`**. So the online
  text is one patch release ahead of the installed `262-1`; I checked both and the clauses cited below are
  word-identical in the two except where noted.
- `systemd.time(5)` has no `man.archlinux.org` page (`https://man.archlinux.org/man/systemd.time.5.en` → HTTP 404,
  2026-10-26), so the `monthly` alias is taken from the local page (`systemd 262-1`, `man systemd.time`, "monthly →
  *-*-01 00:00:00") and cross-checked against the manager's own parse (§2.H).
- Every quote below is ≤25 words, carries its URL and access date or its `man` page plus package version, and is
  reproduced from the page text (local: `man … | col -b`; online: the page fetched and de-tagged into
  `/fast/scratch/hyaku/tsukuroi-r44/C2ExecUnitsSR9`, a throwaway scratch dir, since deleted).

## 2. Point-by-point

### A. `KillSignal=` — what `systemctl stop` sends, to which processes, `KillMode=` default

- `systemd.kill(5)` §`KillSignal=`: "Specifies which signal to use when stopping a service. This controls the
  signal that is sent as first step of shutting down a unit" (23 words) — https://man.archlinux.org/man/systemd.kill.5.en,
  2026-10-26, package `systemd 262.1-1`. Same text locally (`systemd 262-1`). The paragraph's next sentence is
  "and is usually followed by SIGKILL"; the default is "Defaults to SIGTERM".
- The unit sets `KillSignal=SIGINT` (`frozen/src/btrfs-scrub@.service:9`) and sets no `KillMode=`; effective value
  is `KillMode=control-group` (receipts:51).
- `systemd.kill(5)` §`KillMode=`: "If set to control-group, all remaining processes in the control group of this
  unit will be killed on unit stop" (19 words) and "Defaults to control-group." (same URL, 2026-10-26). So the
  SIGINT goes to the whole cgroup, not only `ExecStart`'s main process — for this unit that is the single
  `btrfs` process and its threads (under `-B` the `if (do_background)` fork at `S237` `scrub.c:1512` is not taken,
  and `scrub_handle_sigint_child(fdmnt)` at `scrub.c:1546` runs in that process; see the sibling SR9 seat for the
  handler itself).
- Also per `systemd.kill(5)`: "Note that, right after sending the signal specified in this setting, systemd will
  always send SIGCONT" (18 words), and "the termination request is repeated with the SIGKILL signal or the signal
  specified via FinalKillSignal=" (18 words) once `TimeoutStopSec=` expires. Effective `FinalKillSignal=9`,
  `SendSIGHUP=no`, `SendSIGKILL=yes` (receipts:51-55).
- No `ExecStop=` is set, so the stop signal is sent immediately: `systemd.service(5)` §`TimeoutStopSec=`, "If no
  ExecStop= commands are specified, the service gets the SIGTERM immediately" (12 words) —
  https://man.archlinux.org/man/systemd.service.5.en, 2026-10-26, `systemd 262.1-1`. The page names SIGTERM because
  SIGTERM is `KillSignal=`'s default; `KillSignal=SIGINT` replaces it (the clause quoted above). Effective
  `TimeoutStopUSec=5s` (receipts:47) — see D1.
- Conclusion: SR9's "a SIGINT sent to it (the service's stop signal)" is right, and the fuller statement is: a stop
  job sends SIGINT to every remaining process of the unit's control group (default `KillMode=control-group`),
  immediately (no `ExecStop=`), always followed by SIGCONT, and by SIGKILL after `TimeoutStopSec=` (5 s on this
  host — D1). A restart job would use `RestartKillSignal=`, unset here, so also SIGINT.

### B. `Persistent=`

- `systemd.timer(5)` §`Persistent=`: "If true, the time when the service unit was last triggered is stored on
  disk." (16 words) and "the service unit is triggered immediately if it would have been triggered at least once
  during the time when the timer was inactive" (23 words), "Note that this setting only has an effect on timers
  configured with OnCalendar=." (13 words) — https://man.archlinux.org/man/systemd.timer.5.en, 2026-10-26,
  `systemd 262.1-1`. The unit's `OnCalendar=monthly` satisfies that condition.
- The catch-up run is not immediate in wall-clock terms: the same paragraph adds "Such triggering is nonetheless
  subject to the delay imposed by RandomizedDelaySec=" (11 words) — see C.
- Host: effective `Persistent=yes` (receipts:66) and **no** stamp file for it: `/var/lib/systemd/timers/` holds
  stamps only for other timers, none named `stamp-btrfs-scrub@-.timer` (receipts:122-131). Consistent with a timer
  instance that was never enabled/started.
- The stamp file is manager state in `/var/lib/systemd/timers/`, not a btrfs scrub record: `systemctl clean
  --what=state <timer>` removes it (same page). The census reads `/var/lib/btrfs` (`SCRUB_DIR`), so a timer stamp
  never appears in its `records=` count, and its absence here is independent evidence no instance ran.

### C. `RandomizedDelaySec=1w`

- `systemd.timer(5)` §`RandomizedDelaySec=`: "Delay the timer by a randomly selected, evenly distributed amount of
  time between 0 and the specified time value." (20 words), "The delay is added on top of the next determined
  elapsing time" (12 words) — https://man.archlinux.org/man/systemd.timer.5.en, 2026-10-26, `systemd 262.1-1`.
- `1w` parses: effective `RandomizedDelayUSec=1w` (receipts:65). A `w` suffix is a valid time-span unit
  (`systemd.time(5)`), and the manager's own echo proves the parse.
- Combined with `AccuracySec=1d` (`btrfs-scrub@.timer:6`) and `OnCalendar=monthly` the actual fire time is the 1st
  of a month, 00:00, plus 0–1 day of jitter (`AccuracySec=`), plus 0–1 week of random delay — i.e. somewhere
  between the 1st and about the 9th, not a fixed monthly minute. `systemd.timer(5)` §`AccuracySec=`: "The timer is
  scheduled to elapse within a time window starting with the time specified in OnCalendar=" (18 words, same URL).
  SR9's "the timer fires OnCalendar=monthly with RandomizedDelaySec=1w" is true but a reader can take "monthly" as
  a precise date; the window is the honest reading.

### D. `WantedBy=`

- `systemd.unit(5)` §`WantedBy=`: "A symbolic link is created in the .wants/, .requires/, or .upholds/ directory of
  each of the listed units" (19 words) — https://man.archlinux.org/man/systemd.unit.5.en, 2026-10-26,
  `systemd 262.1-1`. Same words locally (`systemd 262-1`).
- Location and link target: the page's Example 1 gives "a symlink /etc/systemd/system/multi-user.target.wants/foo.service
  linking to the actual unit will be created" (14 words; same URL), so for system units the link lives under
  `/etc/systemd/system`, i.e. the directory the census arm reads by default.
- `timers.target` is the sanctioned hook: `systemd.special(7)` "It is recommended that timer units installed by
  applications get pulled in via Wants= dependencies from this unit." (21 words) —
  https://man.archlinux.org/man/systemd.special.7, 2026-10-26, `systemd 262.1-1`.
- The timer's own `Unit=` is unset, so it activates the same-instance service:
  `systemd.timer(5)` §`Unit=`: "If not specified, this value defaults to a service that has the same name as the
  timer unit, except for the suffix." (22 words; effective `Unit=btrfs-scrub@-.service`, receipts:62).

### E. `%f`

- `systemd.unit(5)` §Specifiers, `"%f"`: "Unescaped filename … This is either the unescaped instance name (if
  applicable) with / prepended (if applicable)" (16 words) — https://man.archlinux.org/man/systemd.unit.5.en,
  2026-10-26, `systemd 262.1-1`. The rule is path unescaping: "This implements unescaping according to the rules
  for escaping absolute file system paths discussed above" (same cell).
- Instance `-` is the escaped form of `/`: `systemd-escape --path /` prints `-` (rc=0, receipts:11-13).
- Effective resolution, from the manager: `ExecStart={ path=/usr/bin/btrfs ; argv[]=/usr/bin/btrfs scrub start -B /
  … }` (receipts:48) — so for `btrfs-scrub@-.timer`/`@-.service` both `%f` occurrences (`Description=`,
  `ConditionPathIsMountPoint=%f`, `RequiresMountsFor=%f`, `ExecStart=`) read `/`. For an instance such as
  `btrfs-scrub@mnt-data.timer`, `%f` is `/mnt/data`; that matters for D4.

### F. The enable question — "enabling an instance creates a `timers.target.wants/btrfs-scrub@<instance>.timer` link"

Right, and it is exactly the template case the man page spells out:

- `systemd.unit(5)` §`WantedBy=`, template rule: "the listing unit must have DefaultInstance= set, or systemctl
  enable must be called with an instance name" (18 words) and the worked analogue "systemctl enable getty@tty2.service
  creating a getty.target.wants/getty@tty2.service link to getty@.service" (10 words) —
  https://man.archlinux.org/man/systemd.unit.5.en, 2026-10-26, `systemd 262.1-1`. `btrfs-scrub@.timer` is a
  template listing a non-template (`timers.target`) and has no `DefaultInstance=`, so the only valid enable is
  `systemctl enable btrfs-scrub@<instance>.timer`; the *link name* is the instance name and the *target* is the
  one template file.
- `systemctl(1)` §`enable`: "This will create a set of symlinks, as encoded in the [Install] sections of the
  indicated unit files." (19 words) and "symlinks named the same as instances are created … they point to the
  single template unit file they are instantiated from" —
  https://man.archlinux.org/man/systemctl.1.en, 2026-10-26, `systemd 262.1-1`. Enabling does not start anything
  ("Enabling and starting units is orthogonal", same page).
- Live analogue on this host (read-only): `/etc/systemd/system/getty.target.wants/getty@tty1.service ->
  /usr/lib/systemd/system/getty@.service`, `systemctl is-enabled getty@tty1.service` → `enabled`, and there is **no**
  `/etc/systemd/system/getty@tty1.service` alias (receipts:97-100). That is precisely the shape SR9 describes,
  produced by the same install logic for an instance of a template with a `WantedBy=`.
- Contrast pair proving what `enable` writes and where: `fstrim.timer` — link in
  `/etc/systemd/system/timers.target.wants`, `UnitFileState=enabled`, `FragmentPath=/usr/lib/systemd/system/fstrim.timer`;
  `man-db.timer` — link only in `/usr/lib/systemd/system/timers.target.wants`, still `ActiveState=active` but
  `UnitFileState=disabled` (receipts:102-114). The `/etc` link is the enablement; the vendor `/usr/lib` link is not
  (see D3).
- The arm counts exactly what such an enable writes: `tools/tsukuroi-census.sh:2027-2030` globs
  `"$tw"/btrfs-scrub@*.timer`, skips the bare template name (`:2029`) and increments `tim`, with
  `TIMER_WANTS=${TSUKUROI_TIMER_WANTS:-/etc/systemd/system/timers.target.wants}` (`:495`); contract at `:398-400`
  ("what `systemctl enable` links; the bare template name is not an instance and is not counted").
- No instance exists on this host: `/etc/systemd/system/timers.target.wants` holds `fstrim`, `paccache`,
  `snapper-cleanup`, `snapper-timeline` only (receipts:77-84); `systemctl is-enabled btrfs-scrub@-.timer` →
  `disabled` and 0 scrub timers listed (receipts:116-120). Matches `frozen/hostcap/capture.txt:5-6`.

### G. `systemctl cat btrfs-scrub@-.timer` (read-only)

Shows exactly one file, `/usr/lib/systemd/system/btrfs-scrub@.timer`, with the pinned body and no drop-in
(receipts:15-27); `DropInPaths=` is empty for the service (receipts:39) and `systemctl cat` lists no drop-in file
for the timer. The installed units are byte-identical to the pinned `S244` files — `9a0b6cc2…` and `eaa7af92…` on
both sides (receipts:29-33), owned by `btrfs-progs 7.1-1` (`capture.txt:9`).

### H. `OnCalendar=monthly` and the manager's parse

- Local `systemd.time(5)` (`systemd 262-1`): "monthly → *-*-01 00:00:00".
- Manager parse of the installed unit: `TimersCalendar={ OnCalendar=*-*-01 00:00:00 ; next_elapse=(null) }`
  (receipts:63). `next_elapse=null` because the timer is not active — an inactive timer has no next elapse; that
  is not an error.

## 3. Depth findings (for the row's precision, not falsifiers)

**D1 — the stop window on this host is 5 s, not 90 s, and `Type=simple` cannot extend it.** The manager's
`DefaultTimeoutStopUSec=5s` (receipts:69-70) comes from an **unowned** host drop-in,
`/etc/systemd/system.conf.d/10-faster-shutdown.conf`: `[Manager]` / `DefaultTimeoutStopSec=5s` (`pacman -Qo` →
"No package owns …", receipts:72-75). The unit sets no `TimeoutStopSec=`, so SR9's "SIGINT … cancels the running
scrub, and … is recorded with `canceled` set" has a **5 s** budget between SIGINT and the SIGKILL that
`systemd.service(5)` describes ("If it does not terminate in the specified time, it will be forcibly terminated by
SIGKILL", 17 words, https://man.archlinux.org/man/systemd.service.5.en, 2026-10-26, `systemd 262.1-1`). Only
`Type=notify` services can extend that via `EXTEND_TIMEOUT_USEC=`; this unit is `Type=simple` (receipts:45). If the
cancel + record write does not finish inside 5 s the master process dies without writing the record. I did not
measure whether a real cancel completes inside 5 s (that needs a running scrub); the row should not claim the
record is always left.

**D2 — after such a stop the unit is left `failed`, not `inactive (dead)`.** btrfs-progs counts a cancelled device
as an error: `scrub.c:1626-1628` (`case ECANCELED:` → `++err;`) and `scrub.c:1725-1726` (`if (err) return 1;`), so
`ExecStart` exits 1. In systemd v262 `src/core/service.c` (fetched 2026-10-26 from
https://raw.githubusercontent.com/systemd/systemd/v262/src/core/service.c — supplemental, not part of the frozen
sources) a clean exit with status 1 gives `f = SERVICE_FAILURE_EXIT_CODE` (`:4780`), recorded by
`if (s->result == SERVICE_SUCCESS) s->result = f;` (`:4831-4832`); `service_enter_dead()` keeps it
(`:2506-2507`, `if (s->result == SERVICE_SUCCESS || f == SERVICE_FAILURE_START_LIMIT_HIT)`) and maps it to
`end_state = SERVICE_FAILED` (`:2519`). [INFERENCE, source-grounded, not measured: nothing was started or
stopped.] If instead the scrub finished before the SIGINT arrived, the handler's cancel fails (`scrub.c:421-423`
`perror("Scrub cancel failed")`), `err` stays 0 and the unit ends inactive. Either way the timer stays enabled and
fires again next month.

**D3 — the arm's `timers=` counts one enablement channel out of three.** `systemctl enable` writes the persistent
system configuration directory `/etc/systemd/system`; `--runtime` enables "for only this boot of the system"
(`systemctl(1)` §`enable`, https://man.archlinux.org/man/systemctl.1.en, 2026-10-26, `systemd 262.1-1`), i.e. the
runtime directory `/run/systemd/system`, which `systemd.unit(5)` lists in its "System Unit Search Path" beside
`/etc/systemd/system/*` and `/usr/lib/systemd/system/*` (https://man.archlinux.org/man/systemd.unit.5.en,
2026-10-26, `systemd 262.1-1`); a distribution may also ship a vendor link under
`/usr/lib/systemd/system/timers.target.wants`, which the manager honours for activation. This host proves it:
`man-db.timer` is `ActiveState=active` and a dependency of `timers.target` with its only link in
`/usr/lib/systemd/system/timers.target.wants`, yet `UnitFileState=disabled`; a `/run` (`--runtime`) link has the
same effect (receipts:85-114). The probe reads only `$TIMER_WANTS` (default `/etc/...`, `:495`), so an enabled
vendor or `--runtime` instance would read `timers=0`. Arch's `btrfs-progs` ships no such link — `PKGBUILD:100-101`
installs only the two unit files, and `/usr/lib/systemd/system/timers.target.wants` contains no `btrfs-scrub@*`
entry (receipts:85-93, 116-120) — so on Arch the default is adequate; the caveat is for the general reading, not
this host.

**D4 — a `timers.target.wants` link is necessary, not sufficient, for a scrub.** The service carries
`ConditionPathIsMountPoint=%f` (`btrfs-scrub@.service:3`); `systemd.unit(5)` "verifies that a certain path exists
and is a mount point" (10 words, `systemd 262-1`, §`ConditionPathIsMountPoint=`). An instance whose unescaped `%f`
is not a mount point (e.g. `systemctl enable btrfs-scrub@foo.timer` → `%f=/foo`) still yields a link the probe
counts, but the service is skipped at fire time; a masked instance (`systemctl(1)`: "makes it impossible to start
them") is likewise a link without a scrub when the link is present; and a dangling link still counts, because the
probe accepts either `-e` or `-L` (`tools/tsukuroi-census.sh:2028`), so a removed unit file leaves `timers=1`. So
`timers=N` is a count of enabled instances, and the triage bullet "A monthly scrub exists only if an instance of
the packaged timer is enabled (SR9); the census counts the … links (`timers=`)" should be read one-way only — a
nonzero `timers=` does not prove the scrub runs, a zero does prove nothing is scheduled. On this host `/` *is* a
mount point (`/proc/self/mountinfo` root line, receipts:136) and the condition has never been evaluated
(`ConditionTimestamp=` empty and `ConditionResult=no` for this unit, receipts:42-44; the contrast is
`systemd-random-seed.service`, `ConditionResult=yes` with a timestamp, receipts:138-146); I did not start the unit
to evaluate it.

**D5 — `WantedBy=` alone does not make a service startable-by-enable.** `btrfs-scrub@.service` has no `[Install]`
section at all (`frozen/src/btrfs-scrub@.service:1-10`), so the service's `UnitFileState` is `static` (receipts:40)
and `systemctl enable` on the *service* would only warn; the timer is what is enabled and
the timer pulls the same-instance service (`Unit=btrfs-scrub@-.service`, receipts:62). SR9's wording "enabling an
instance creates a …timer link" is therefore the correct one — and the only one.

## 4. Proposed exact text

**(a) SR9, sentence 3 — replace**

> The service runs `btrfs scrub start -B %f` with `KillSignal=SIGINT`; a stop job sends that signal as the first
> step to every remaining process of the unit's control group (`KillMode=` default `control-group`), always
> followed by `SIGCONT`, and by `SIGKILL` once `TimeoutStopSec=` expires.

(one sentence; the systemd side is `systemd.kill(5)` — see (d).)

**(b) SR9, sentence 2 — keep, with the link location and the enable precondition made explicit**

> … and is `WantedBy=timers.target`, so `systemctl enable btrfs-scrub@<instance>.timer` (the template has no
> `DefaultInstance=`, so an instance name is required) creates a
> `/etc/systemd/system/timers.target.wants/btrfs-scrub@<instance>.timer` link to
> `/usr/lib/systemd/system/btrfs-scrub@.timer`.

**(c) SR9, `Host reading` — append one sentence**

> `%f` for the instance `-` is `/` (the manager's `ExecStart` argv ends `-B /`), `/` is a mount point, and the
> service's `ConditionPathIsMountPoint=%f` has never been evaluated because no instance has ever been started.

**(d) SR9, `Limits` — replace the second bullet**

> SR9's systemd side is pinned at `systemd.kill(5)`, `systemd.timer(5)`, `systemd.unit(5)` and `systemctl(1)`
> (man.archlinux.org, accessed 2026-10-26, package `systemd 262.1-1`; local pages `systemd 262-1`): `KillSignal=`
> is the first-step stop signal, sent to the whole control group under the default `KillMode=control-group`;
> `WantedBy=timers.target` plus an instance name is what writes the `timers.target.wants` link. Not measured: a
> real stop of a running scrub. On this host `DefaultTimeoutStopSec=5s` (unowned
> `/etc/systemd/system.conf.d/10-faster-shutdown.conf`) caps the SIGINT-to-SIGKILL window, and `Type=simple` cannot
> extend it, so "SIGINT leaves a canceled record" holds only if the cancel and the record write finish in 5 s
> [inference].

**(e) `How this changes OS triage`, third bullet — append**

> `timers=` counts enabled instances, not scrubs that ran: an instance whose `%f` is not a mount point, a masked
> link or a dangling one can be counted while no scrub can run, and a vendor or `--runtime` link outside
> `/etc/systemd/system/timers.target.wants` is not counted at all.

## 5. Not done

- Nothing enabled/started/stopped/masked; no `systemctl enable|start|stop`, no `systemctl daemon-reload`, no
  `--dry-run` either, because the guard forbids the subcommand. The enable semantics are therefore documented
  evidence (three man pages) + the live `getty@tty1` analogue + the arm's own code, not a trial.
- Did not run `tools/check-scrub-record-r44.py` or `tools/tsukuroi-census.sh` (their selftest); did not run
  `btrfs scrub …`, `systemd-analyze verify`, or any package/host mutation. Supplemental fetch beyond the frozen
  sources: `systemd` v262 `src/core/service.c` from GitHub raw (read-only, in scratch, D2 only) and the six
  `man.archlinux.org` pages.
- Receipts: `.ufo/waves/round-44/w1/C2ExecUnitsSR9/receipts-systemd.txt` (146 lines; the line numbers `receipts:N`
  above are that file's lines). Scratch `/fast/scratch/hyaku/tsukuroi-r44/C2ExecUnitsSR9` removed.
- No tool installed or upgraded; no package, service, unit, timer, sysfs, `/etc` or `/var/lib` was changed, and no
  process was signalled. Only reads: `man`, `systemctl` queries, `sha256sum`, `ls`/`readlink`/`find`,
  `systemd-escape`, `pacman -Qo/-Q`, `curl` of the six man pages and of systemd v262 source files from GitHub raw
  (all into scratch, now deleted).
