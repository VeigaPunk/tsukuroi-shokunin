ROW GR3 VERDICT: holds
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Evidence, clause by clause, against the pinned snapshots (all digest-verified; sha256sum -c OK for
.ufo/waves/round-45/frozen/src/SHA256SUMS (systemd.kill.xml), .ufo/waves/round-44/frozen/src/SHA256SUMS
(btrfs-scrub@.service), .ufo/waves/round-42/frozen/src/SHA256SUMS (scrub.c); capture.txt sha256
f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70 matches the entry header).

Section hash: the frozen counter
(tools/check-scrub-admission-r47.py --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash)
prints GR3 = 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c; my independent sha256 over the
LF-joined lines from `## GR3` up to (exclusive) `## How this changes OS triage` reproduces the same value.

Statement clauses:

- "First the unit's KillSignal=, which this unit sets to SIGINT instead of the SIGTERM default" —
  btrfs-scrub@.service:9 is `KillSignal=SIGINT` (S244; quote text matches the line exactly). SIGTERM default:
  systemd.kill.xml:112 "Defaults to <constant>SIGTERM</constant>." (S248, the KillSignal= entry at :107-112).
  Supported.

- "because the unit sets no KillMode=, the default control-group applies and every remaining process in the
  unit's control group receives it" — the S244 file is 10 lines and contains no KillMode= (verified by reading
  the whole file). systemd.kill.xml:101 "<para>Defaults to <option>control-group</option>.</para>" (quote exact).
  systemd.kill.xml:68-69: "If set to <option>control-group</option>, all remaining processes in the control group
  of this unit will be killed on unit stop" (quote at :68 exact). Supported.

- "Right after that signal systemd sends SIGCONT" — systemd.kill.xml:114-115: "Note that, right after sending
  the signal specified in this setting, systemd will always send <constant>SIGCONT</constant>, to ensure that
  even suspended tasks can be terminated cleanly." (quotes at :114 and :115 exact). Supported.

- "If processes remain once TimeoutStopSec= has passed, the request is repeated with SIGKILL (FinalKillSignal=,
  unless SendSIGKILL=no)" — systemd.kill.xml:91 "the delay configured via the <varname>TimeoutStopSec=</varname>
  has passed" (quote exact; :91-93 lists the condition) and systemd.kill.xml:96-98 "the termination request is
  repeated with the <constant>SIGKILL</constant> signal or the signal specified via
  <varname>FinalKillSignal=</varname> (unless this is disabled via the <varname>SendSIGKILL=</varname> option)"
  (quote at :96 exact). Supported.

- "On this host the unit's effective stop timeout is 5 s: the drop-in
  /etc/systemd/system.conf.d/10-faster-shutdown.conf sets DefaultTimeoutStopSec=5s" — capture.txt:4
  records `stop_default` naming that drop-in, its line 2 carrying `DefaultTimeoutStopSec=5s` (S249).
  Supported.

- "(that this default reaches every system unit without its own TimeoutStopSec= is [inference]:
  systemd-system.conf(5) is not pinned here)" — correctly marked: the capture shows the value but the
  propagation rule to units without their own TimeoutStopSec= is not pinned by any S-source. The unit file
  itself sets no TimeoutStopSec= (10-line read). Honest mark placement.

- "no package owns that drop-in" — capture.txt:5 "dropin_owner
  /etc/systemd/system.conf.d/10-faster-shutdown.conf none" (S249). Supported.

- "systemctl show reports KillSignal=2, KillMode=control-group, TimeoutStopUSec=5s, FinalKillSignal=9 and
  SendSIGKILL=yes for btrfs-scrub@-.service" — capture.txt:3 "unit_show FinalKillSignal=9
  FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service KillMode=control-group KillSignal=2 SendSIGKILL=yes
  TimeoutStopUSec=5s" (S249). All five properties present on the line. Supported.

- "With -B the start does not fork into the background (btrfs-progs scrub.c:1512)" — scrub.c:1512 is
  `if (do_background) {` guarding the fork() at :1513; the -B option sets do_background=false at
  scrub.c:1292-1293 (`case 'B': do_background = false;`). Citation adequate and the claim precise. Supported.

- "and installs its SIGINT handler on the mount's descriptor (scrub.c:1546, :439)" — scrub.c:1546 is
  `scrub_handle_sigint_child(fdmnt);` (quote exact) and scrub.c:439 is
  `.sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,` (quote exact); the handler body uses
  cancel_fd = fd (:442). Supported.

- "so SIGINT reaches that handler, which issues BTRFS_IOC_SCRUB_CANCEL (SR9)" — scrub.c:421 is
  `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);` inside scrub_sigint_record_progress (:417-424)
  (quote exact). SR9 is this row's own label per the entry header. Supported.

- "Whether the start then writes its canceled record (SR3) within the 5 s before SIGKILL is not established
  [inference: a start killed before that write leaves the record as it was last written during the run]" —
  explicitly stated as not established, with the inference mark and a reasoned explanation; nothing asserted
  as fact beyond the pinned lines. SR3 is the scrub-record row referenced by the corpus. Supported as an
  honest limit.

Quotes: all 12 quoted texts verified character-for-character on the cited lines
(btrfs-scrub@.service:9, :10; systemd.kill.xml:68, :91, :96, :101, :108, :114, :115; scrub.c:421, :1546, :439).

Host reading: capture.txt:2 "systemd 262 (262-1-arch)" matches "systemd is 262-1-arch (capture.txt:2)";
capture.txt:3, :4, :5 as above; "No unit was started or stopped" is consistent with the capture header
(captured uid=1000, CapEff=0000000000000000) and the entry's Limits ("GR3 pins systemd's documented behaviour
... and the host's effective values, not a trace of a real stop"), which the row respects.

Limits read for context (round-47 GR2 amendment does not touch GR3's bytes; I judged the current section).

No clause overreaches; both [inference] marks sit exactly where the pinned sources stop. Verdict: holds.
