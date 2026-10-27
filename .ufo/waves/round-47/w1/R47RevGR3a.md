ROW GR3 VERDICT: holds
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Seat R47RevGR3a, item C1-GR3-R47RevGR3a. Reviewed the GR3 row of corpus/knowledge/btrfs-scrub-grounding-r45.md at revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 (bytes via `git show`; row extent `## GR3` up to exclusive `## How this changes OS triage`, lines 141-186 of the shown file; no other `## ` header inside the extent). Also read the entry's `## Limits` section (lines 200-221) for context; the round-47 GR2 amendment does not touch GR3's bytes, and the current bytes were judged.

Hash binding (step 2):
- Frozen counter `tools/check-scrub-admission-r47.py --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash` printed `"GR3": "43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c"`, matching the declared expected value.
- Independently re-derived: sha256 over the LF-joined lines from `## GR3` to (exclusive) `## How this changes OS triage`, no trailing LF, gives 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c. Matches.

Snapshot digest verification (step 3):
- .ufo/waves/round-45/frozen/src/SHA256SUMS: cmdline.c, dev-replace.c, systemd.kill.xml (S248), kstrtox.c, vsprintf.c all `OK` via `sha256sum -c`.
- .ufo/waves/round-44/frozen/src/SHA256SUMS: scrub.c, sysfs.c, btrfs-scrub@.timer, btrfs-scrub@.service (S244), PKGBUILD all `OK`.
- .ufo/waves/round-42/frozen/src/SHA256SUMS: scrub.c (S237), CHANGES all `OK`.
- capture.txt (S249): `sha256sum capture.txt` = f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70, matching the digest stated in the entry header (line 1 of the entry).

Quote-text verification (step 4): every `**Quote.**` string appears verbatim on its cited line of the pinned snapshot (leading-tab whitespace aside):
- S244 btrfs-scrub@.service:9 = `KillSignal=SIGINT`; :10 = `ExecStart=/usr/bin/btrfs scrub start -B %f`. Confirmed with `cat -n` (unit is 11 lines; no `KillMode=` anywhere in it).
- S248 systemd.kill.xml:68, :91, :96, :101, :108, :114, :115 each contain the quoted text (checked with `sed -n '<n>p'`).
- S237 scrub.c:421 = `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);`; :1546 = `scrub_handle_sigint_child(fdmnt);`; :439 = `.sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,`. Confirmed.

Clause-by-clause:

- Statement clause "signals the running `btrfs scrub start -B` in this order under systemd v262": systemd v262 is pinned by S248 (FETCH.txt fetch of systemd tag v262; entry header `verified-at`) and the host runs "systemd 262 (262-1-arch)" (capture.txt:2). The unit's ExecStart runs `btrfs scrub start -B %f` (btrfs-scrub@.service:10). Supported.
- Clause "First the unit's `KillSignal=`, which this unit sets to SIGINT instead of the SIGTERM default": unit sets KillSignal=SIGINT (btrfs-scrub@.service:9); systemd.kill.xml:112 states KillSignal "Defaults to SIGTERM" in the same entry quoted at :108. Supported.
- Clause "the unit sets no `KillMode=`, the default `control-group` applies and every remaining process in the unit's control group receives it": the unit has no KillMode= (full 11-line unit read); systemd.kill.xml:101 "Defaults to control-group."; systemd.kill.xml:68-69 "all remaining processes in the control group of this unit will be killed on unit stop". Supported.
- Clause "Right after that signal systemd sends SIGCONT": systemd.kill.xml:114-115 "right after sending the signal specified in this setting, systemd will always send SIGCONT". Supported.
- Clause "If processes remain once `TimeoutStopSec=` has passed, the request is repeated with SIGKILL (`FinalKillSignal=`, unless `SendSIGKILL=no`)": systemd.kill.xml:91 "the delay configured via the TimeoutStopSec= has passed"; systemd.kill.xml:96-97 "the termination request is repeated with the SIGKILL signal or the signal specified via FinalKillSignal= (unless this is disabled via the SendSIGKILL= option)". Supported.
- Clause "On this host the unit's effective stop timeout is 5 s: the drop-in /etc/systemd/system.conf.d/10-faster-shutdown.conf sets DefaultTimeoutStopSec=5s": capture.txt:4 `stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`. Supported.
- Clause "(that this default reaches every system unit without its own TimeoutStopSec= is [inference]: systemd-system.conf(5) is not pinned here)": the reach of the system.conf default is explicitly marked [inference] with the pin gap named; mark correctly placed at exactly the point the pinned sources stop. Supported.
- Clause "no package owns that drop-in": capture.txt:5 `dropin_owner /etc/systemd/system.conf.d/10-faster-shutdown.conf none`. Supported ("none" = no owning package listed).
- Clause "`systemctl show` reports KillSignal=2, KillMode=control-group, TimeoutStopUSec=5s, FinalKillSignal=9 and SendSIGKILL=yes for btrfs-scrub@-.service": capture.txt:3 contains all five key=value pairs on the unit_show line. KillSignal=2 is SIGINT on Linux, consistent with the unit's KillSignal=SIGINT. Supported.
- Clause "With `-B` the start does not fork into the background (btrfs-progs scrub.c:1512)": S237 scrub.c:1512 `if (do_background) {` gates the fork at :1513; `-B` sets `do_background = false` (scrub.c:1292-1294, `case 'B':`) and the option table documents `-B` as "do not background" (scrub.c:1743). The bare `scrub.c:1512` citation resolves in S237, a declared snapshot for this row. Supported.
- Clause "installs its SIGINT handler on the mount's descriptor (scrub.c:1546, :439)": scrub.c:1546 `scrub_handle_sigint_child(fdmnt);` passes the mount fd; scrub.c:437-441 defines scrub_handle_sigint_child(int fd) with `.sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress` (:439) and `cancel_fd = fd` (:440). Supported.
- Clause "SIGINT reaches that handler, which issues BTRFS_IOC_SCRUB_CANCEL (SR9)": scrub.c:416-423 defines scrub_sigint_record_progress, whose body is the ioctl at :421 `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);` with cancel_fd bound to fdmnt. Supported.
- Clause "Whether the start then writes its canceled record (SR3) within the 5 s before SIGKILL is not established [inference: ...]": explicitly stated as not established, with the inference mark and justification; nothing asserted as fact beyond the pinned lines. Correctly hedged.

Host reading verification (step 4):
- capture.txt:3 reports KillMode=control-group KillSignal=2 SendSIGKILL=yes TimeoutStopUSec=5s FinalKillSignal=9 for btrfs-scrub@.service (FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service on the same line). Supported.
- capture.txt:4 stop default from 10-faster-shutdown.conf line 2. Supported.
- capture.txt:5 drop-in owner "none". Supported.
- capture.txt:2 systemd 262-1-arch. Supported.
- "No unit was started or stopped": consistent with capture.txt:1 (captured uid=1000, CapEff=0000000000000000, i.e. unprivileged capture; the capture script is read-only per the entry header). Not contradicted by any pinned source.

Limits-section context noted for the record: GR3's own limit bullet (lines 208-209) states GR3 "pins systemd's documented behaviour (man page source at the host's major version) and the host's effective values, not a trace of a real stop", which matches exactly what the row does; no overreach found.

Verdict rationale: every Statement and Host-reading clause is supported by the cited snapshot line; all twelve quoted texts are verbatim on their cited lines; both [inference] marks (reach of system.conf default; canceled-record-within-5s) sit precisely where the pinned sources stop and are labeled as inferences or as not-established. No clause overreaches; the row's core is right. Verdict: holds.
