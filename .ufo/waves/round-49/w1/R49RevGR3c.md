ROW GR3 VERDICT: holds
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Reviewer R49RevGR3c (independent: I did not write this row). Bytes under test =
`git -C …/tsukuroi-shokunin show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:corpus/knowledge/btrfs-scrub-grounding-r45.md`.
Row extent: entry lines 152-197 (`## GR3` at 152, next header `## How this changes OS triage` at 198).

Hash convention: sha256 over those 46 lines joined with LF, with the single LF after the 46th line dropped (the
blank line at 197 is part of the content) = 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c,
3291 bytes, identical to `--section-hash`. Keeping the trailing LF gives a different digest, so the frozen value is
the no-trailing-LF convention; mine matches it, no divergence.

Snapshot digests, `sha256sum -c SHA256SUMS` in each `src/` dir, all OK:
- S248 = round-45/frozen/src/systemd.kill.xml, 448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72;
  FETCH.txt: systemd/systemd tag v262 (host is 262-1-arch, capture.txt:2).
- S244 = round-44/frozen/src/btrfs-scrub@.service, eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252;
  Arch btrfs-progs 7.1-1 packaging tag (FETCH.txt).
- S237 = round-42/frozen/src/scrub.c, 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801;
  kdave/btrfs-progs v7.1 cmds/scrub.c (FETCH.txt), same version as the 7.1-1 package.
- S249 = round-45/frozen/hostcap/capture.txt, f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70
  (equals the digest in the task/entry header).
Disambiguation matters: round-44/frozen/src/scrub.c is a DIFFERENT file (S242, kernel fs/btrfs/scrub.c); its line
1512 is `find_first_extent_item`, not a fork. The row's `scrub.c:1512/:1546/:421/:439` resolve only in the round-42
file, which is the S237 the row names — the S-row label disambiguates correctly.

Quotes: all 12 are verbatim (leading indentation stripped) substrings of their cited lines —
btrfs-scrub@.service:9 `KillSignal=SIGINT`, :10 `ExecStart=/usr/bin/btrfs scrub start -B %f`;
systemd.kill.xml:68, :91, :96, :101, :108, :114, :115; scrub.c:421, :439, :1546. No quote is reworded.

Clause check:
1. Order (KillSignal first → SIGCONT right after → SIGKILL/FinalKillSignal after TimeoutStopSec unless
   SendSIGKILL=no). systemd.kill.xml:84-85 "Processes will first be terminated via SIGTERM (unless the signal to
   send is changed via KillSignal=…)", :114-115 "right after sending the signal specified in this setting, systemd
   will always send SIGCONT", :91 TimeoutStopSec delay (applies to control-group, lines 92-93), :96-97 "repeated
   with the SIGKILL signal or the signal specified via FinalKillSignal= (unless this is disabled via the
   SendSIGKILL= option)". Supported. The optional SIGHUP step (:86-87) is off unless SendSIGHUP= is set; it is
   "Defaults to <literal>no</literal>" (:138), the unit never sets it, and capture.txt:7 shows no unit drop-ins, so
   the enumerated order is complete for this unit.
2. Unit sets SIGINT, not the SIGTERM default: btrfs-scrub@.service:9; default at systemd.kill.xml:112
   ("Defaults to <constant>SIGTERM</constant>"). True (see note N2 on the missing :112 citation).
3. Unit sets no KillMode=, so control-group applies and every remaining process in the group gets it:
   the whole unit file is lines 1-10 (Description, ConditionPathIsMountPoint, RequiresMountsFor, Nice,
   IOSchedulingClass, KillSignal, ExecStart) — no KillMode=, no ExecStop=, no TimeoutStopSec=; default at
   systemd.kill.xml:101, all-remaining-processes at :68, signal delivered to them per :84-85. capture.txt:3 shows
   the effective KillMode=control-group. Supported; "every" does not overreach.
4. 5 s effective stop timeout: capture.txt:3 `TimeoutStopUSec=5s`; capture.txt:4
   `stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`. The generalisation
   that the default reaches every unit lacking its own TimeoutStopSec= carries the [inference] mark and names the
   unpinned manual — placed on exactly the undecided step.
5. No package owns the drop-in: capture.txt:5 `dropin_owner … none`, produced by the pacman files-DB grep at
   capture.sh:19-20. Supported as an observation of that DB.
6. systemctl show values KillSignal=2, KillMode=control-group, TimeoutStopUSec=5s, FinalKillSignal=9,
   SendSIGKILL=yes: capture.txt:3, same line. Supported.
7. `-B` does not fork: `-B` clears do_background and sets do_wait/do_print (scrub.c:1292-1294), and the fork sits
   under `if (do_background) {` (scrub.c:1512); OPTLINE("-B", "do not background") at :1743 states the semantics.
   With -B control falls through to scrub.c:1546 in the same process. Supported.
8. SIGINT handler installed on the mount's descriptor: scrub.c:1343 `fdmnt = btrfs_open_mnt(path)` with a `< 0`
   early return at :1344, :1546 `scrub_handle_sigint_child(fdmnt)`, :436-443 selects
   `scrub_sigint_record_progress` when fd != -1 (:439) and stores `cancel_fd = fd` (:442). The handler issues
   `ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL)` (:421). Mechanism is attributed to the right function
   (installer vs handler); "on the mount's descriptor" is shorthand for the cancel fd, not a claim that the
   signal is bound to an fd. Supported.
9. SR9/SR3 pointers: SR9 is the packaged timer/service row (btrfs-scrub-record-r44.md:91) and its statement
   already carries the foreground-handler/cancel-ioctl chain; SR3 is the canceled-record row
   (btrfs-scrub-record-r43.md:52). Both resolve; neither is asserted as a quote.
10. Final clause: "Whether the start then writes its canceled record (SR3) within the 5 s before SIGKILL is not
    established [inference: …]". Post-run write at scrub.c:1702 with "canceled" at :1667/:1672 shows the write
    exists but nothing pinned bounds it against the 5 s window; the mark sits on the undecided part only.
11. Host reading: capture.txt:2 (262-1-arch), :3, :4, :5 all match; "No unit was started or stopped" matches
    capture.sh:4-5 (show/read only). Supported.

Universal words: "every" (row lines 6, 9) is covered by :68 + :84-85 and the empty drop-in list; "always" appears
only inside the :114 quote, in systemd's own words. No "only", "never" or "exact" in the row.

Non-blocking precision notes (claims are TRUE in the pinned bytes; these are citation-completeness only, not
defects, so they do not change the verdict):
N1. The `-B` → no-fork link is cited only as `scrub.c:1512`; the deciding lines are 1292-1294. Replacement text:
    "With `-B` the start does not fork into the background (`scrub.c:1292-1294` clears `do_background`;
    `scrub.c:1512` gates the fork)".
N2. "instead of the SIGTERM default" has no citation; add `systemd.kill.xml:112`.
N3. The instance name `btrfs-scrub@-.service` is not printed in capture.txt:3; it is the argument at capture.sh:11.
N4. The handler is only installed when the run reaches :1546 (before that SIGINT is default) and is reset after the
    run; the row speaks of the running scrub, so no overreach.

Verified but not re-derived: I did not re-fetch the upstream files (digests checked against the frozen
SHA256SUMS only); I did not read systemd's C source, so clause 1-3 rest on the pinned v262 man page plus the
capture; I did not re-derive the counter's quotes_ok/marks_ok logic.
Not done: no unit was started, stopped, or signalled; no live timing was measured; I did not read GR1 or GR2 of the
entry (only GR3 lines 152-197; entry line 10 surfaced incidentally in a grep for the SR9 label). Scratch dir
removed. No tool installs; no pacman, git or jj mutation anywhere.
