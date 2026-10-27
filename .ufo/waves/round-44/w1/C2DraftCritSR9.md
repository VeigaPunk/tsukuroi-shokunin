VERDICT: supports

Item C2-14: SR9 pre-read (wave-1; no counted verdict — verdicts bind only from wave-2 C2RevSR9/C2CritSR9). Read SR9 in `corpus/knowledge/btrfs-scrub-record-r44.md` at 7e081698d4fc3c4ea944884fd093058de9909de1 against S244 (`btrfs-scrub@.timer`, `btrfs-scrub@.service`, `PKGBUILD`) and S237 (round-42 frozen `cmds/scrub.c`, btrfs-progs v7.1) line by line. Every SR9 sentence holds; no overreach or wrong claim found. Adjusted replacement text proposed below (two precision nuances + the already-documented inference boundary).

# Evidence (all read-only; no host/lane mutation)

- S244 unit files read at `.ufo/waves/round-44/frozen/src/btrfs-scrub@.timer` (10 lines) and `btrfs-scrub@.service` (10 lines); `PKGBUILD` lines 99-101 install both into `${pkgdir}/usr/lib/systemd/system`. sha256 of all five frozen sources match `SHA256SUMS` exactly (scrub.c f347931b…, sysfs.c ce146120…, timer 9a0b6cc…, service eaa7af9…, PKGBUILD 3b803e8…; receipt `w1/C2DraftCritSR9/sources-and-host-evidence.txt`).
- `PKGBUILD` lines 45-51: `source=(...)` includes `btrfs-scrub@.service` and `btrfs-scrub@.timer` as files of the Arch packaging repo itself (the only git source is upstream btrfs-progs at tag v7.1) — the units are packaging-side, not fetched from upstream.
- Upstream check (GitHub API, recursive tree at tag v7.1, sha 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b, 1253 entries): NO `units/` directory and NO `*.timer`/`*.service` file anywhere; the only paths matching `timer|units|scrub` are `Documentation/Scrub.rst`, `Documentation/btrfs-scrub.rst`, `Documentation/ch-scrub-intro.rst`, `cmds/scrub.c`, `common/units.c`, `common/units.h`, `tests/cli-tests/024-scrub-limit` (receipt `w1/C2DraftCritSR9/upstream-v7.1-tree-hits.txt`; access 2026-10-26).
- S237 identity: round-42 frozen `scrub.c` is byte-identical to upstream v7.1 `cmds/scrub.c` (sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801 both, 2231 lines) — quoting S237 is quoting upstream v7.1.
- Host capture (S245) lines 5-9: wants links 0, `btrfs-scrub@-.timer` disabled, installed-unit hashes (9a0b6cc…, eaa7af9…) byte-identical to the pinned S244 files (match `SHA256SUMS`), owned by btrfs-progs 7.1-1.

# Sentence marks (deciding line per sentence)

S1 “The scheduled scrub on Arch comes from the distribution package, not from btrfs-progs upstream: the Arch btrfs-progs 7.1-1 PKGBUILD installs btrfs-scrub@.service and btrfs-scrub@.timer into /usr/lib/systemd/system.” — HOLDS. Deciding lines: PKGBUILD:49-50 (units are packaging-repo sources), PKGBUILD:100-101 (install to `/usr/lib/systemd/system`); upstream v7.1 tree contains no units/ or *.timer (GitHub API check above).

S2 “The timer fires OnCalendar=monthly with RandomizedDelaySec=1w, keeps Persistent=true and is WantedBy=timers.target, so enabling an instance creates a timers.target.wants/btrfs-scrub@<instance>.timer link.” — HOLDS. Deciding lines: timer:5, timer:7, timer:8, timer:11; the `.wants` link is standard systemd Install semantics, consistent with capture.txt:5 counting exactly those links.

S3 “The service runs btrfs scrub start -B %f with KillSignal=SIGINT.” — HOLDS. Deciding lines: service:10 (`ExecStart=/usr/bin/btrfs scrub start -B %f`), service:9 (`KillSignal=SIGINT`).

S4 “In btrfs-progs v7.1 -B keeps the start in the foreground and sets do_print, so the later recording failures of SR3 are printed into the service's output;” — HOLDS. Deciding lines: scrub.c:1293 (`do_background = false;`), scrub.c:1295 (`do_print = true;`) in the `-B` case (scrub.c:1292-1296); `do_print` gates the error prints including the recording failure at scrub.c:1704 (`if (ret && do_print) error("failed to record the result: %m")`) and scrub.c:1690-1698.

S5 “the foreground start installs a SIGINT handler that issues BTRFS_IOC_SCRUB_CANCEL, so a SIGINT sent to it (the service's stop signal) cancels the running scrub,” — HOLDS (with the inference already disclosed in Limits). Deciding lines: scrub.c:1546 (`scrub_handle_sigint_child(fdmnt);`, foreground path), scrub.c:438-443 (handler = `fd == -1 ? SIG_DFL : scrub_sigint_record_progress`; `cancel_fd = fd`), scrub.c:421 (`ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);`), scrub.c:417-424. The “stop signal” half is systemd.kill(5) behaviour, flagged as inference in Limits; the cancel effect is SR3 — no new claim.

S6 “and a device whose scrub ioctl returns nonzero is recorded with canceled set,” — HOLDS. Deciding line: scrub.c:969 (`sp->stats.canceled = !!ret;`). Nuance (kept in replacement): ANY nonzero ioctl return sets `canceled` — cancellation via SIGINT is one path, not the only one; the sentence as written is faithful to the code.

S7 “which btrfs scrub resume later takes up (SR3).” — HOLDS. Deciding lines: scrub.c:1430-1431 (`if (resume && last_scrub && (last_scrub->stats.canceled || !last_scrub->stats.finished))` — resume takes up a device whose last record has `canceled` set OR `finished` unset, continuing from `last_scrub->p.last_physical`, scrub.c:1433). Nuance (kept in replacement): resume also takes up interrupted (unfinished, uncanceled) records; the sentence correctly includes canceled ones.

Quote accuracy: the twelve SR9 quotes reproduce the pinned files/verbatim at the cited lines (PKGBUILD:100,101; timer:5,7,8,11; service:9,10; scrub.c:1293,1295,421,1546,969). Host-reading sentences match capture.txt:5-9 (see evidence).

# Proposed exact replacement text (Statement paragraph of SR9)

> **Statement.** The scheduled scrub on Arch comes from the distribution package, not from btrfs-progs upstream: the Arch btrfs-progs 7.1-1 `PKGBUILD` carries `btrfs-scrub@.service` and `btrfs-scrub@.timer` in its `source` array and installs them into `/usr/lib/systemd/system`; the upstream v7.1 tree contains no systemd units. The timer fires `OnCalendar=monthly` with `RandomizedDelaySec=1w`, keeps `Persistent=true` and is `WantedBy=timers.target`, so enabling an instance creates a `timers.target.wants/btrfs-scrub@<instance>.timer` link. The service runs `btrfs scrub start -B %f` with `KillSignal=SIGINT`. In btrfs-progs v7.1 `-B` keeps the start in the foreground and sets `do_print`, so the later recording failures of SR3 are printed into the service's output; the foreground start installs a SIGINT handler that issues `BTRFS_IOC_SCRUB_CANCEL`, so a SIGINT sent to it cancels the running scrub [inference: that `systemctl stop` sends this signal is systemd.kill(5) behaviour (Limits); that the ioctl cancels is SR3]. A device whose scrub ioctl returns nonzero is recorded with `canceled` set — any failure, not only cancellation, sets it — which `btrfs scrub resume` later takes up: resume resumes a device whose last record has `canceled` set or `finished` unset, continuing from the recorded position (SR3).

(Quotes, host-reading paragraph and Limits stay unchanged; the two parenthetical nuances and the inline inference marker are the only additions.)

# Not done

- Did not run counters (`check-scrub-record-r44.py`, census selftest), did not run any git/jj mutation or host command, did not start/stop any scrub; nothing here exercises the host. All evidence is static file reads, one GitHub API read, and one `curl` of the pinned upstream raw file (into scratch, read-only).
- Receipts: `w1/C2DraftCritSR9/upstream-v7.1-tree-hits.txt`, `w1/C2DraftCritSR9/sources-and-host-evidence.txt`.
