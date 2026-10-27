ROW SR9 VERDICT: holds

Seat C2CritSR9 (critic), tsukuroi lane round 44 wave 2. Target: row SR9 of
`corpus/knowledge/btrfs-scrub-record-r44.md` at integrated tip 8eee79db608b5815c325a5af7cbfdeac50eda9f4.
Method: adversarial falsification against the digest-pinned snapshots (sha256 re-verified locally for
S237 scrub.c, S244 timer/service/PKGBUILD) and the counter's own gates in `tools/check-scrub-record-r44.py`.

VERDICT: supports (no contradiction found; the row survives the strongest counterexamples I could build).

## Evidence — every sentence checked against the pinned lines

1. "comes from the distribution package, not from btrfs-progs upstream" — PKGBUILD `source` lines 49-50
   list `btrfs-scrub@.service`/`.timer` as packaging-repo files beside `initcpio-*`, distinct from the
   `git+...btrfs-progs.git` source (line 46); `package()` `cd "${srcdir}"` (line 95) then installs them
   (lines 100-101, quoted verbatim). `FETCH.txt` lines 4-6 confirm S244 was fetched from
   `gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/`, not upstream. Holds.

2. Timer: `OnCalendar=monthly` (timer:5), `RandomizedDelaySec=1w` (:7), `Persistent=true` (:8),
   `WantedBy=timers.target` (:11) — all quoted exactly. "enabling an instance creates a
   `timers.target.wants/btrfs-scrub@<instance>.timer` link" is correct systemd template semantics and is
   precisely what the C1 arm counts (`tsukuroi-census.sh` probe_scrub_record lines 2024-2035 globs
   `btrfs-scrub@*.timer` under `TSUKUROI_TIMER_WANTS` default `/etc/systemd/system/timers.target.wants`).
   Unclaimed `AccuracySec=1d` (timer:6) is an omission, not a contradiction.

3. Service: `KillSignal=SIGINT` (:9), `ExecStart=/usr/bin/btrfs scrub start -B %f` (:10) — exact.
   `KillSignal=` as the signal `systemctl stop` sends verified against host `systemd.kill(5)`: it is the
   first stop signal (default SIGTERM; here overridden to SIGINT), SIGKILL follows only after
   TimeoutStopSec. The row correctly marks this systemd side as unpinned inference; the semantics hold.

4. "-B keeps the start in the foreground and sets do_print" — scrub.c:1292-1296 `case 'B':
   do_background=false; do_wait=true; do_print=true;`. "the later recording failures of SR3 are printed"
   — SR3's two recording-failure prints are `do_print`-gated (`scrub.c` "recording progress failed: %m"
   ~1698 and "failed to record the result: %m" ~1706); the service passes no `-q` and no quiet BCONF, so
   `do_print` survives the `verbose==QUIET` reset at ~1332. Journal output = service output. Holds.

5. "the foreground start installs a SIGINT handler that issues BTRFS_IOC_SCRUB_CANCEL" —
   `scrub_handle_sigint_child(fdmnt)` (1546, quoted) sets `cancel_fd=fdmnt` and installs
   `scrub_sigint_record_progress`, whose body is the quoted `ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL,
   NULL)` (421). Reached by the -B foreground path (no fork taken since do_background=false) *and* by the
   background-start child (call site is unconditional, after the `if (do_background) fork` block); the
   background parent takes `SIG_IGN` via `scrub_handle_sigint_parent` (426-434). So the claim is true —
   and slightly narrower than reality (the handler is not foreground-exclusive). Not a defect.
   `fdmnt` is `btrfs_open_mnt(path)` (1343), the fd the cancel ioctl wants; under
   `KillMode=control-group` (default) systemd's SIGINT reaches the process holding it.

6. "a device whose scrub ioctl returns nonzero is recorded with canceled set, which btrfs scrub resume
   later takes up (SR3)" — `ret = ioctl(sp->fd, BTRFS_IOC_SCRUB, ...)`; `sp->stats.canceled = !!ret`
   (965-969, quoted); the final `scrub_write_progress` (1701-1708) records it; resume consumes
   `last_scrub->stats.canceled` (1430-1434). Exact match to the row's wording. Depth note: `!!ret` marks
   `canceled` for ANY nonzero ioctl return (e.g. ENODEV mid-run, EINPROGRESS race), not only a
   user/systemd cancel — the row states this faithfully; readers should not read "canceled" as
   "was canceled" beyond what the code does.

7. Host reading — capture.txt:5 counts the same directory the arm counts (script line 14 globs
   `/etc/systemd/system/timers.target.wants/btrfs-scrub@*.timer`, result 0); capture.txt:6
   `is_enabled_btrfs-scrub@-.timer disabled`; capture.txt:7-8 installed-unit sha256s equal the pinned
   S244 digests byte-for-byte (verified); capture.txt:9 `pacman -Qo` names btrfs-progs 7.1-1 for the
   timer. Caveat: line 9 directly covers only the `.timer`; `.service` ownership is indirect via its
   byte-identical digest to the packaging file — sufficient support for "belong to btrfs-progs 7.1-1"
   but noted as the weakest evidentiary link. "No instance is enabled" is also technically the
   `/etc`-persistent sense (a `systemctl enable --runtime` link under `/run` would evade line 5) —
   which matches the arm's own counting semantics, so the row and the arm stay consistent.

8. Counter gates re-verified for SR9: 13/13 quotes land on their named lines of digest-verified
   snapshots (independent re-check, not the counter's); every frozen window holds ≥1 quote
   (timer 1-11, service 1-10, PKGBUILD 99-101, scrub.c 412-444/1286-1296/1510-1548/960-972); all four
   required (id,file) keys present (S244 timer/service/PKGBUILD, S237 scrub.c); all six prop tokens
   (`btrfs-scrub@`, `OnCalendar=monthly`, `Persistent=true`, `KillSignal=SIGINT`, `-B`,
   `BTRFS_IOC_SCRUB_CANCEL`) appear in the statement; host block cites existing non-empty capture
   lines 5-9.

## Proposed text

None — the row needs no correction. Optional depth footnote for a future round: (a) note that the
SIGINT handler is installed unconditionally at scrub.c:1546 (background-start child too), so
"the foreground start" describes the service path, not the only path; (b) note `canceled` records any
nonzero scrub-ioctl return, not only explicit cancels; (c) capture could add a `pacman -Qo` for the
`.service` to close the one indirect evidentiary link. All three are improvements, not falsifications.
