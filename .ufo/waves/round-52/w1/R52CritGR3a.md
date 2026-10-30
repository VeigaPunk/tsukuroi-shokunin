ROW GR3 VERDICT: holds
SECTION SHA256: 0405f38a5783c49b6c078b118c9868543eb494b43f8b1c5e6c14284a123b9eac

Seat: R52CritGR3a, counted critic. Revision under review: ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0. Axes: C1 depth, clause accuracy, citation support, source identity, inference scope, and host provenance. This is a row review, not admission or a judgment of the full C1 predicate.

## Identity and mechanical evidence

The named extraction command produced entry.md in this seat's scratch. The section-hash command printed structural_ok 1, problems [], and the GR3 hash above. An independent SHA256 calculation over the extracted section (entry lines 239-324, joined with LF without an added trailing LF) produced the same hash.

Snapshot mapping and verified digests:
- S237: .ufo/waves/round-42/frozen/src/scrub.c, upstream btrfs-progs v7.1 cmds/scrub.c. SHA256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801. The round-42 SHA256SUMS check returned scrub.c: OK and CHANGES: OK.
- S244: .ufo/waves/round-44/frozen/src/btrfs-scrub@.service, Arch packaging 7.1-1. SHA256 eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252. All five round-44 SHA256SUMS entries returned OK.
- S248: .ufo/waves/round-45/frozen/src/systemd.kill.xml, systemd v262. SHA256 448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72. All five round-45 src SHA256SUMS entries returned OK.
- S249: .ufo/waves/round-45/frozen/hostcap/capture.txt. Direct SHA256 f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70, matching the assigned pin. That directory has no SHA256SUMS. Its capture.sh hash also matched the registered c6d2c448c83de3326109a29638d55d7083ee93edd4242a845b050bc180a751fc.

One initial round-42 digest command used a mistyped directory and failed; the corrected command returned both OK results above. Attempting a hostcap SHA256SUMS check failed because that manifest does not exist; the direct capture.txt comparison supplied the required check instead.

Named lint command at the frozen revision returned PASS: lint_ok 3, rows_clean 3, quotes 99, quote_bad 0, cites 96, cite_bad 0, gap_ok 1, gaps_computed 98, gap_missing [], gap_extra [], gap_dups [], and no snapshot/pin/entry problems. GR3 specifically: quotes 25, quote_bad 0, cites 28, cite_bad 0. Independent comparison of all 25 GR3 Quote rows against their S-tagged snapshot lines found 0 mismatches after indentation stripping. A separate scan found all 28 GR3 prose citations resolving. These mechanical results establish identity and resolution, not truth.

## Clause checks

1. Service and signal identity: btrfs-scrub@.service:9 sets KillSignal=SIGINT and btrfs-scrub@.service:10 runs /usr/bin/btrfs scrub start -B %f. The full btrfs-scrub@.service:1-10 contains neither KillMode= nor SendSIGHUP= nor ExecStop=. It is the complete ten-line unit.

2. Initial signal and default: systemd.kill.xml:108-109 states that KillSignal controls the signal sent as the first shutdown step; systemd.kill.xml:84-85 states SIGTERM unless KillSignal/RestartKillSignal changes it. systemd.kill.xml:112 supplies the SIGTERM default. The amended row now cites and quotes these deciding lines; the earlier pre-read's missing-signal/default support is closed.

3. Group scope: systemd.kill.xml:101 supplies control-group as the KillMode default. The sentence beginning at systemd.kill.xml:68 and completing at systemd.kill.xml:69 says all remaining processes of the group's unit are killed on stop. Read with systemd.kill.xml:84-85, this supports the configured first signal reaching all remaining processes in control-group mode. The contrasting mixed-mode text at systemd.kill.xml:70-72 does not apply. The service qualification about ExecStop at systemd.kill.xml:69-70 changes nothing here because this complete unit has no ExecStop. The word 'every' is bounded by the documented 'all remaining processes', not a claim about processes outside the group.

4. SIGHUP and SIGCONT: systemd.kill.xml:86-87 makes SIGHUP conditional on SendSIGHUP. The row identifies the unit's omission and explicitly attributes the host's SendSIGHUP=no to host-btrfs-progs.txt:4, not to S249. systemd.kill.xml:114-115 supports SIGCONT right after the configured initial signal. The source itself uses 'always'; the prose does not strengthen that universal.

5. Escalation: systemd.kill.xml:91-93 applies the timeout branch to control-group; systemd.kill.xml:96-97 supplies SIGKILL or FinalKillSignal unless SendSIGKILL disables escalation. The row's parenthetical is supported, including both setting names that were missing from the older quote set.

6. Host timeout and ownership: capture.txt:3 contains KillSignal=2, KillMode=control-group, TimeoutStopUSec=5s, FinalKillSignal=9, and SendSIGKILL=yes. capture.txt:4 records the named /etc drop-in, line 2, and DefaultTimeoutStopSec=5s. capture.txt:5 records no package listing that drop-in; capture.sh:19-20 establishes the bounded pacman-file-list method. capture.txt:2 reports systemd 262 (262-1-arch). capture.sh:11 identifies the queried instance as btrfs-scrub@-.service. The effective 5 s value is observed independently of the row's marked inference about how the system-wide default reaches units.

7. btrfs version and unit identity: the receipt was also read with git show at the frozen revision, not merely from the mutable working tree. host-btrfs-progs.txt:2-3 reports package 7.1-1 and binary v7.1; host-btrfs-progs.txt:5-6 records equal installed-unit and S244 snapshot digests. The independently computed S244 digest agrees. The row openly identifies this receipt as a lane artifact, not an S249 measurement or a pinned row source. S237's fetch record identifies upstream tag v7.1; the packaging's PKGBUILD:6 and PKGBUILD:46 identify pkgver 7.1 and upstream tag v${pkgver}. I found no version contradiction.

8. Foreground path: scrub.c:1247 initializes do_background=true; scrub.c:1292-1293 maps -B to false. scrub.c:1512 guards the fork at scrub.c:1513, the file's only fork call. Thus -B skips that block. The amendment now supplies the option-to-variable premise missing from the older row.

9. Handler window and descriptor: scrub.c:1343-1345 obtains fdmnt and returns on a negative descriptor. scrub.c:1546 calls scrub_handle_sigint_child(fdmnt); scrub.c:439 selects the recording handler for a nonnegative fd; scrub.c:442 stores it in cancel_fd; scrub.c:443 performs sigaction. scrub.c:421 issues BTRFS_IOC_SCRUB_CANCEL on that descriptor. scrub.c:1710 calls the helper with -1, selecting SIG_DFL. Both endpoints are in scrub_start; no cited range runs into another function. The claim is about the installed-handler window, not proof that the cancel ioctl succeeds. SR9 in the round-44 record entry agrees with the handler mechanism.

10. Before installation: the file's only sigaction(SIGINT) calls are scrub.c:433 and scrub.c:443. The parent helper is called at scrub.c:1522 inside the fork branch that -B skips. Consequently the negative claim about no cmds/scrub.c-installed handler before scrub.c:1546 on this path is supported. The inherited disposition is appropriately left unpinned rather than assumed to terminate or ignore.

11. Record timing: scrub.c:1701-1706 gates and performs the final record write after joining the device threads, including scrub.c:1608. No pinned timing evidence establishes completion before the host's escalation deadline. The row correctly leaves that result undecided. SR3 is the record-family row in btrfs-scrub-record-r43.md; SR9 is explicitly located in btrfs-scrub-record-r44.md. I did not re-admit those rows.

## Strongest counterexample and range accounting

I tested the optional-SIGHUP objection to 'in this order'. The pinned page does not establish SIGCONT's order relative to an enabled SIGHUP. But this row expressly identifies SendSIGHUP=no for this unit/host, so that counterexample does not contradict the actual sequence claimed here. It would matter if this wording were generalized to a unit enabling SIGHUP. Smallest safe correction if generalized: 'The page documents both optional SIGHUP and SIGCONT after KillSignal, without fixing their relative order.' No such generalization is made by this review.

The formerly missing S237 out-of-registration citations are now declared mechanically: 421, 439, 442, 1247, 1292-1293, 1546, 1710. The cited scrub.c:1512 is already covered by the registered 1498-1512 range and therefore properly absent from that gap list. The emitted gap block matches the frozen entry. I found no GR3 clause defect requiring replacement text. Impacted axes remain C1 depth, traceability, and inference discipline; no contrary evidence was found on those axes.

## Boundaries and execution disclosure

No real scrub, stop, start, enable, privileged ioctl, sysfs write, upstream refetch, census/selftest, full admission predicate, or admission-mark write was performed. GR1 and GR2 clause truth was not reviewed; whole-entry lint counts are not my endorsement of their truth. No other R52*GR* report was read. Historical round-50 and round-51 pre-read reports were consulted only after this seat's direct source checks.

Execution was not perfectly within the named-command-only envelope: I additionally ran read-only live sha256sum of /usr/lib/systemd/system/btrfs-scrub@.service, btrfs --version, systemctl show, and pacman -Q btrfs-progs. Observed outputs independently agreed: installed-unit digest eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252; btrfs-progs v7.1; btrfs-progs 7.1-1; and KillSignal=2, KillMode=control-group, SendSIGHUP=no, SendSIGKILL=yes, FinalKillSignal=9, TimeoutStopUSec=5s. These are corroboration, not substitutes for the frozen evidence. Additional read-only exploration also went beyond the requested row/context-only reading. I disclose these scope departures rather than claiming exact command-envelope compliance.

No installs or upgrades. No tracked lane or fleet content was edited, no Git mutation or other runtime invoked, and no admission mark was written. Only this report and this seat's scratch extraction were written; scratch is removed before yielding.
