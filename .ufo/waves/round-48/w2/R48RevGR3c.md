ROW GR3 VERDICT: holds
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Reviewer R48RevGR3c, row GR3 of btrfs-scrub-grounding-r45 at revision ae99f021b76f8eb1c8805d32d80644464afb1ff6 (entry lines 146-191, header of the next section at line 192). Judged as a stranger, against the pinned snapshots only.

Hash: the counter's --section-hash printed the expected GR3 value above. I re-derived it myself: sha256 over the LF-joined lines from the GR3 header to the line before the next header, with the trailing blank line dropped, gives 43430a14...bbc32c, identical. (With one extra trailing blank line the hash differs, so the counter's convention is the exact one I used.)

Snapshot digests, each checked with sha256sum against its SHA256SUMS file:
- systemd.kill.xml (S248, round-45 dir): 448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72, matches.
- btrfs-scrub@.service (S244, round-44 dir): eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252, matches.
- scrub.c (S237, round-42 dir, btrfs-progs v7.1 per its FETCH.txt): 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801, matches. The round-44 scrub.c (S242) has a different digest and is NOT the one the row cites; all line numbers below are in the round-42 file.
- capture.txt (S249): f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70, equals the digest in the entry header (line 1 of the entry).

Quote lines, each verified verbatim on the cited line:
- btrfs-scrub@.service:9 is "KillSignal=SIGINT"; btrfs-scrub@.service:10 is "ExecStart=/usr/bin/btrfs scrub start -B %f". The file is 10 lines long.
- systemd.kill.xml:68 (control-group: all remaining processes in the unit's control group are killed), :91 (TimeoutStopSec delay has passed), :96 (termination request repeated with SIGKILL or FinalKillSignal), :101 (Defaults to control-group), :108 (KillSignal= is the signal used when stopping a service), :114-115 (right after sending that signal, systemd always sends SIGCONT). All present.
- scrub.c:421 is the BTRFS_IOC_SCRUB_CANCEL ioctl in the handler; scrub.c:1546 is scrub_handle_sigint_child(fdmnt); scrub.c:439 is the sa_handler ternary. All present.

Clause-by-clause:
1. Order KillSignal first, then SIGCONT, then SIGKILL after TimeoutStopSec: systemd.kill.xml:108-109 (first step of shutting down), :114-115 (SIGCONT right after), :91 and :96 (repeat with SIGKILL or FinalKillSignal unless SendSIGKILL=no, :97). Supported. The optional SIGHUP of systemd.kill.xml:86 is off unless SendSIGHUP= is set; the row does not claim it, so no overreach.
2. Unit sets KillSignal=SIGINT, no KillMode=, no TimeoutStopSec=: the whole unit file is btrfs-scrub@.service:1-10 and has only KillSignal as a kill setting. capture.txt:7 shows no drop-ins found. Default control-group per systemd.kill.xml:101, all remaining processes per :68. Supported.
3. 5 s effective timeout: capture.txt:3 shows TimeoutStopUSec=5s, and capture.txt:4 shows the system.conf.d drop-in line 2 setting DefaultTimeoutStopSec=5s. The step that the default reaches every unit without its own TimeoutStopSec= is correctly marked [inference] (systemd-system.conf(5) is not pinned). Mark placed correctly, only on the undecided part.
4. No package owns the drop-in: capture.txt:5 reads "none". Supported.
5. systemctl show values KillSignal=2, KillMode=control-group, TimeoutStopUSec=5s, FinalKillSignal=9, SendSIGKILL=yes: all on capture.txt:3. The instance name btrfs-scrub@-.service is not printed in the capture file itself; it is the argument in the pinned capture script that produced it (the script is in the same hostcap directory). Not an overreach, since FragmentPath on the same line names the template.
6. -B does not fork: -B sets do_background to false (scrub.c:1293) and the fork sits under if (do_background) at scrub.c:1512, matching the row's citation. Supported.
7. SIGINT handler on the mount descriptor: scrub.c:1546 calls scrub_handle_sigint_child(fdmnt), where fdmnt comes from btrfs_open_mnt(path) at scrub.c:1343; scrub.c:436-443 stores cancel_fd and installs the handler when fd is not -1 (scrub.c:439). Handler issues BTRFS_IOC_SCRUB_CANCEL at scrub.c:421. Supported. Mild imprecision only: the handler is not installed before line 1546 and is reset to default at scrub.c:1710 after the run, but the row speaks of the running scrub, so it stands.
8. SR9 and SR3 cross-references: SR9 in btrfs-scrub-record-r44 already states the foreground handler and the service stop signal; SR3 is the canceled record. The closing [inference] (a start killed before the record write leaves the last-written record) is correctly marked, since nothing pinned decides the write timing within 5 s.
9. Host reading: capture.txt:2 shows systemd 262 (262-1-arch); "No unit was started or stopped" matches the capture script header, which states systemctl show only, no start or stop.

No clause names an effect, ordering, path or condition that the cited lines do not show; inference marks sit only on the undecided points. Not done by me: no live service was stopped, and systemd-system.conf(5) was not consulted (not pinned). Verdict: holds.
