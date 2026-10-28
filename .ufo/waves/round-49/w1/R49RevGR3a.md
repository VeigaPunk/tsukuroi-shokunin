ROW GR3 VERDICT: holds
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Section extent and convention. `section_hashes()` in tools/check-scrub-admission-r49.py:178-190 hashes the entry
lines from the `## GR3` header to the line before the next `## ` header — corpus/knowledge/btrfs-scrub-grounding-r45.md
lines 152-197 at 55c07cd — joined with LF, so the hashed string ends with one LF. My recompute gives 43430a14…c32c;
the same lines with that final LF dropped give 17b19a53…20e7, so my convention differs from the seat brief's
"no trailing LF" parenthetical by that last newline and matches the counter, which prints 43430a14…c32c
(`--section-hash`, problems=[]). No `## ` line occurs inside the row.

Pins, verified before reading (the tracked blobs at 55c07cd are byte-identical to the files I hashed):
S237 .ufo/waves/round-42/frozen/src/scrub.c 48df2e2f…f0801 (btrfs-progs v7.1 cmds/scrub.c per its FETCH.txt);
S244 .ufo/waves/round-44/frozen/src/btrfs-scrub@.service eaa7af92…40252 (Arch btrfs-progs 7.1-1; the live
/usr/lib/systemd/system/btrfs-scrub@.service has the same sha256); S248 .ufo/waves/round-45/frozen/src/systemd.kill.xml
44832283…10e72 (systemd tag v262 per its FETCH.txt); S249 .ufo/waves/round-45/frozen/hostcap/capture.txt f5958a83…91e70
(matches the seat brief and the counter's SNAPSHOTS map; hostcap carries no SHA256SUMS, so the digest is the recorded
one). `sha256sum -c SHA256SUMS` was OK in all three src snapshot directories.

Clauses, each checked against those bytes:
1. KillSignal is the first stop signal, and this unit makes it SIGINT not the SIGTERM default:
   btrfs-scrub@.service:9 `KillSignal=SIGINT`; systemd.kill.xml:108 says `KillSignal=` "controls the signal that is sent
   as first step of shutting down a unit"; the SIGTERM default is systemd.kill.xml:112. (The row quotes :108 but not
   :112, which it paraphrases.)
2. The unit sets no `KillMode=`, so the default control-group applies and every remaining process in the cgroup gets
   that signal: service lines 1-10 contain only Description/ConditionPathIsMountPoint/RequiresMountsFor/Nice/
   IOSchedulingClass/KillSignal/ExecStart; systemd.kill.xml:101 "Defaults to control-group"; :68-69 "all remaining
   processes in the control group of this unit will be killed on unit stop"; :84-85 "Processes will first be terminated
   via SIGTERM (unless the signal to send is changed via KillSignal=…)". capture.txt:7 `unit_dropins` is empty, and my
   own read-only check found no /etc/systemd/system/btrfs-scrub@.service.d, no
   /usr/lib/systemd/system/btrfs-scrub@.service.d, no global service.d, and no /etc unit override.
3. SIGCONT right after that signal: systemd.kill.xml:114-115.
4. If processes remain after the timeout, the request is repeated with SIGKILL, i.e. FinalKillSignal=, unless
   SendSIGKILL=no: systemd.kill.xml:91-93 (the TimeoutStopSec arm explicitly names KillMode=control-group) and :96-98.
5. The 5 s effective stop timeout on this host: capture.txt:3 `TimeoutStopUSec=5s`; my own read-only
   `systemctl show btrfs-scrub@-.service` (2026-10-28) returns TimeoutStopUSec=5s too.
6. Provenance of that 5 s: capture.txt:4 `/etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`;
   capture.txt:5 `dropin_owner … none`. I re-read the pacman local db myself (1415 package dirs, world-readable) and no
   `/files` lists that path, and `grep -n DefaultTimeoutStopSec /etc/systemd/system.conf.d/*` returns line 2. The
   DefaultTimeoutStopSec -> TimeoutStopSec propagation is in no pinned file (systemd-system.conf(5) is not in the
   snapshot) and the row marks exactly that step [inference].
7. The `systemctl show` readings: capture.txt:3 carries KillSignal=2, KillMode=control-group, SendSIGKILL=yes,
   TimeoutStopUSec=5s, FinalKillSignal=9 and FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service — every value
   the row names. My re-run reproduces them and additionally reports SendSIGHUP=no, which the row does not rely on.
8. `-B` does not fork into the background: scrub.c:1288 optstring "BdqrRc:n:f"; :1292-1295 `case 'B'` sets
   do_background=false, do_wait=true, do_print=true; the only `fork(` in the file is scrub.c:1513, inside
   `if (do_background)` at :1512; :1565 and :1585 are pthread_create (threads, not forks). The clause is true; the
   -B -> do_background=false link is :1292-1294, and the statement cites only :1512.
9. The handler is installed with the mount's descriptor and issues the cancel ioctl: scrub.c:1343
   `fdmnt = btrfs_open_mnt(path)`; :1546 `scrub_handle_sigint_child(fdmnt)`; :436-443 with :439
   `scrub_sigint_record_progress` and :442 `cancel_fd = fd`; :417-424 with :421
   `ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL)`. The disposition is reset to SIG_DFL at :1710 after the run, so the
   sentence holds for the running scrub, which is what it asserts.
10. The canceled-record sentence claims nothing established: it says only that whether the canceled record is written
    within the 5 s is "not established", and marks the consequence [inference]. SR3
    (corpus/knowledge/btrfs-scrub-record-r43.md:52 onward) grounds the write discipline, not the post-SIGINT timing, so
    the hedge is honest and not a masked defection.

Quotes: all 12 `**Quote.**` lines resolve verbatim at the cited line on the pinned snapshots — counter quote leg
GR3 quotes=12 ok=12 bad=[], and my own byte comparison is identical for each — including the man-page quotes that end
mid-sentence (:68, :91, :96, :108, :114/:115), whose text is exactly the cited line's text.

Marks: the only statements the capture does not decide are the DefaultTimeoutStopSec propagation and the post-SIGINT
record timing; both carry [inference]. No undecided assertion is unmarked.

Universal words: "only", "never" and "exact" do not appear; "every remaining process" tracks systemd.kill.xml:68
"all remaining processes"; "always" appears only inside the quoted doc text (:114); "does not fork into the
background" is exact for -B given the single fork site.

Defects: none found; no replacement text is proposed.

Thin spots (true as written, but thinner citation than ideal): (a) -B -> do_background=false lives at scrub.c:1292-1294
while only :1512 is cited; (b) "installs its SIGINT handler on the mount's descriptor" compresses "handler installed
process-wide (:443) with cancel_fd set to the mount fd (:442)"; (c) the SIGTERM default is systemd.kill.xml:112, which
the row paraphrases but does not quote.

Verified but not re-derived: man-page semantics beyond the quoted lines (I read the pinned XML, not systemd's source);
the tag peels in FETCH.txt (not re-fetched from the network); btrfs-progs runtime behaviour — no scrub and no unit was
started or stopped, and I did not run capture.sh.

Not done: I did not run the full C1 counter (the corr/quotes/verdicts/seats/marks predicate, and no --selftest) — only
`--section-hash` plus an in-process quote leg; I did not read or judge GR1/GR2; no tools were installed.
