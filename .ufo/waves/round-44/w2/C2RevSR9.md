ROW SR9 VERDICT: partly

Seat: C2RevSR9 (reviewer, round 44 wave 2). Row read at 8eee79db608b5815c325a5af7cbfdeac50eda9f4
(`git show` of `corpus/knowledge/btrfs-scrub-record-r44.md`; `git diff --quiet 8eee79db -- .ufo/waves/round-44/frozen
.ufo/waves/round-42/frozen` ⇒ working tree byte-identical to the frozen commit for every input read from the tree).
Method: every sentence checked against its deciding source line; every quote checked verbatim at its cited line in
the digest-verified frozen files; host readings checked against `capture.txt` (9 lines total, sha256
efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900 — matches the header declaration; `sha256sum -c
SHA256SUMS` in `frozen/src` all OK). No mutations; no pacman/systemctl/sysfs run by this seat.

## Quote checks — all 13 hold at the cited lines, verbatim

- `S244` PKGBUILD:100 `install -Dm644 btrfs-scrub@.service "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.service"` ✓ (:raw read)
- `S244` PKGBUILD:101 `install -Dm644 btrfs-scrub@.timer "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.timer"` ✓
- `S244` btrfs-scrub@.timer:5 `OnCalendar=monthly` ✓; :7 `RandomizedDelaySec=1w` ✓; :8 `Persistent=true` ✓; :11 `WantedBy=timers.target` ✓ (file is 11 lines: 1 `[Unit]`, 2 `Description=Monthly Btrfs scrub on %f`, 4 `[Timer]`, 6 `AccuracySec=1d`, 10 `[Install]`)
- `S244` btrfs-scrub@.service:9 `KillSignal=SIGINT` ✓; :10 `ExecStart=/usr/bin/btrfs scrub start -B %f` ✓ (file is 10 lines)
- `S237` scrub.c:1293 `do_background = false;` ✓ and :1295 `do_print = true;` ✓ (inside `case 'B':` at 1292, with `do_wait = true;` at 1294; `do_background` defaults true at 1247, so `-B` does keep the start foreground)
- `S237` scrub.c:421 `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);` ✓ (inside `scrub_sigint_record_progress`, 417–424)
- `S237` scrub.c:1546 `scrub_handle_sigint_child(fdmnt);` ✓ (after the `do_background` fork block, so the foreground/`pid==0` scrubbing process installs the handler; at 438–443 it sets `.sa_handler = scrub_sigint_record_progress` and `cancel_fd = fd`)
- `S237` scrub.c:969 `sp->stats.canceled = !!ret;` ✓ (in `scrub_one_dev`; `ret` is the return of `ioctl(sp->fd, BTRFS_IOC_SCRUB, …)` at 966 — any nonzero ioctl result sets `canceled`, exactly as worded)

## Sentence checks against deciding lines — all hold except the last host clause

- "comes from the distribution package, not from btrfs-progs upstream": PKGBUILD `source=(` at 45–50 lists `btrfs-scrub@.service` and `btrfs-scrub@.timer` as packaging-local files beside the upstream git tag; `package()` installs them from `${srcdir}` into `${pkgdir}/usr/lib/systemd/system` — holds.
- "fires OnCalendar=monthly with RandomizedDelaySec=1w, keeps Persistent=true and is WantedBy=timers.target": timer:5/7/8/11 verbatim; "enabling an instance creates a timers.target.wants link" is [Install] WantedBy semantics, and capture.sh's glob `/etc/systemd/system/timers.target.wants/btrfs-scrub@*.timer` matches that reading — holds.
- "service runs `btrfs scrub start -B %f` with KillSignal=SIGINT": service:9/10 verbatim — holds.
- "`-B` keeps the start in the foreground and sets `do_print`, so the later recording failures of SR3 are printed": verified at 1293–1295; `do_print` gates `error("scrubbing %s failed for device id %lld…")` (1630–1633), `error("recording progress failed: %m")` (1696–1698) and `error("failed to record the result: %m")` (1704–1706) — the exact "recording failures" r43-SR3 names; the service's foreground process prints them to its output — holds.
- "the foreground start installs a SIGINT handler that issues BTRFS_IOC_SCRUB_CANCEL, so a SIGINT sent to it (the service's stop signal) cancels the running scrub": 1546 → 417–424 → 421 verified; handler comment ("cancels a running scrub and makes the master process record the current progress status before exiting", 412–415) supports the chain; the row's Limits section discloses the systemd.kill(5) side as unpinned — holds.
- "a device whose scrub ioctl returns nonzero is recorded with `canceled` set, which `btrfs scrub resume` later takes up (SR3)": 966→969 verified; resume uptake verified at 1430 `if (resume && last_scrub && (last_scrub->stats.canceled ||` — matches r43-SR3's "canceled or unfinished … `resumed` source" — holds.
- "No instance is enabled: no `btrfs-scrub@*.timer` link under `timers.target.wants` (capture.txt:5), `btrfs-scrub@-.timer` is `disabled` (capture.txt:6)": verbatim against capture lines 5 (`wants_btrfs_scrub_instances 0`) and 6 (`is_enabled_btrfs-scrub@-.timer disabled`) — holds.
- "the installed unit files are byte-identical to the pinned ones (capture.txt:7, capture.txt:8)": independently verified — installed digests `9a0b6cc2…` (timer) and `eaa7af92…` (service) equal `sha256sum` of the pinned frozen files exactly — holds.

## Overreaching clause (why not `holds`)

Sentence: "**Host reading.** … the installed unit files are byte-identical to the pinned ones (capture.txt:7,
capture.txt:8) **and belong to btrfs-progs 7.1-1 (capture.txt:9).**"

Deciding source: `capture.txt:9` = `pacman_owner /usr/lib/systemd/system/btrfs-scrub@.timer is owned by btrfs-progs
7.1-1` — it covers **only the timer**. `capture.sh` runs `pacman -Qo` on the timer path alone; `capture.txt` is 9
lines and contains no ownership line for `btrfs-scrub@.service`. The sentence cites line 9 as evidence for both
files' package ownership; for the service file the claim is unsupported by the capture. The claim is very likely
true (the installed service is byte-identical to the packaged file, and PKGBUILD:101 installs it), but this row's
discipline — and SR8's, which pins each host clause to its own line — is that host readings match the capture
lines, and seat rules forbid this seat from re-running pacman to close the gap itself.

## Proposed narrowing text

Replace the host-reading tail (line 130) with:

> the installed unit files are byte-identical to the pinned ones (capture.txt:7, capture.txt:8), and the timer is
> owned by btrfs-progs 7.1-1 (capture.txt:9); the capture does not query the service file's package owner.

(Alternative upstream fix: extend `capture.sh` to `pacman -Qo` both unit paths and re-capture; then the original
sentence stands with a two-line citation.)

## Consistency checks beyond the row cell

- Triage bullet (corpus:138–140): "the census counts the timers.target.wants links" matches capture.sh's glob; "Stopping a running scrub service cancels the scrub and leaves a canceled, resumable record" follows the verified chain — consistent.
- Limits (corpus:148–149): the systemd.kill side of "the service's stop signal" is explicitly marked unpinned inference — honest, no hidden claim.
- Counter self-check of scope: every required SR9 source (timer, service, PKGBUILD, S237 scrub.c) is quoted, all quoted lines fall inside the frozen counter's windows, and all proposition tokens appear in the statement.

Verdict basis: 13/13 quotes verbatim at cited lines; all statement sentences hold; host reading holds except the
package-ownership clause, which cites one capture line (9) for two files while that line names only the timer ⇒
`partly` with the narrowing above.
