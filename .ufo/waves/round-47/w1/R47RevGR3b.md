ROW GR3 VERDICT: holds
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Counted seat R47RevGR3b, item C1-GR3-R47RevGR3b. Row GR3 of corpus/knowledge/btrfs-scrub-grounding-r45.md at revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 (freeze), extent `## GR3` .. exclusive `## How this changes OS triage`, judged on current bytes.

Binding and hashes
- Frozen counter `python3 tools/check-scrub-admission-r47.py --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash` prints GR3 = 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c, structural_ok 1.
- Independent re-derivation: sha256 over the LF-joined lines from `## GR3` (index 140) to exclusive `## How this changes OS triage` (index 185) of the entry at that revision = 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c (matches the counter).
- Full counter run at the freeze revision for GR3: quotes 12 ok / 12, bad []; citations_ok true; citation_problems []; section_sha256 as above; structural_ok 1 (verdicts_ok 0 only because no seat reports are committed yet — seats bind in this wave).
- Snapshot digests verified with `sha256sum -c` from inside each frozen dir: systemd.kill.xml OK (round-45 frozen/src/SHA256SUMS), btrfs-scrub@.service OK (round-44), scrub.c OK (round-42). capture.txt sha256 = f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70, matching the entry header's recorded digest for S249.
- All 12 `**Quote.**` legs verified verbatim on their cited lines (each checked with sed -n '<line>p').

Statement clauses
- Stop order, first signal = unit's KillSignal=: systemd.kill.xml:84-87 states processes are first terminated via SIGTERM "unless the signal to send is changed via KillSignal="; the unit sets KillSignal=SIGINT (btrfs-scrub@.service:9); KillSignal= "Defaults to SIGTERM" (systemd.kill.xml:112). Supported.
- "the unit sets no KillMode=": the full S244 unit is 10 lines ([Unit] + [Service] with Nice, IOSchedulingClass, KillSignal, ExecStart only) — no KillMode= line. Default control-group: systemd.kill.xml:101 "Defaults to control-group" sits inside the KillMode= varlistentry (systemd.kill.xml:63). Supported.
- "every remaining process in the unit's control group receives it": systemd.kill.xml:68 "all remaining processes in the control group of this unit will be killed on unit stop". Supported.
- "Right after that signal systemd sends SIGCONT": systemd.kill.xml:114-115 "right after sending the signal specified in this setting, systemd will always send SIGCONT". Supported.
- "once TimeoutStopSec= has passed, the request is repeated with SIGKILL (FinalKillSignal=, unless SendSIGKILL=no)": systemd.kill.xml:91 (TimeoutStopSec= delay listitem) + systemd.kill.xml:96-98 ("repeated with the SIGKILL signal or the signal specified via FinalKillSignal= (unless this is disabled via the SendSIGKILL= option)"). Supported.
- Host 5 s stop timeout from drop-in: capture.txt:4 `stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`. The step "this default reaches every system unit without its own TimeoutStopSec=" is explicitly marked [inference] with the reason (systemd-system.conf(5) not pinned) — mark correctly placed; the unit itself sets no TimeoutStopSec= (full S244 file above).
- "no package owns that drop-in": capture.txt:5 `dropin_owner /etc/systemd/system.conf.d/10-faster-shutdown.conf none`. Supported.
- systemctl show values: capture.txt:3 lists FinalKillSignal=9, KillMode=control-group, KillSignal=2, SendSIGKILL=yes, TimeoutStopUSec=5s for btrfs-scrub@-.service — every value the row states; KillSignal=2 is SIGINT, matching the unit's KillSignal=SIGINT. Supported.
- systemd v262: capture.txt:2 `systemd 262 (262-1-arch)`. Supported.
- "-B the start does not fork into the background (btrfs-progs scrub.c:1512)": scrub.c:1512 is `if (do_background) {` gating `pid = fork()`; scrub.c:1292-1294 `case 'B': do_background = false; do_wait = true;`. Supported. (Cite resolves in the S237 btrfs-progs snapshot the row quotes; the bare `scrub.c:1512` should be read against that snapshot.)
- "installs its SIGINT handler on the mount's descriptor (scrub.c:1546, :439)": scrub.c:1546 `scrub_handle_sigint_child(fdmnt);`; scrub.c:439 `.sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,`; scrub.c:441 `cancel_fd = fd;`. Supported.
- "SIGINT reaches that handler, which issues BTRFS_IOC_SCRUB_CANCEL (SR9)": scrub.c:421 `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);` inside `scrub_sigint_record_progress`. Supported; SR9 is the round-44 record's open-inference label for "what systemd sends when the packaged scrub service is stopped", which this row grounds.
- "Whether the start then writes its canceled record (SR3) within the 5 s before SIGKILL is not established [inference: ...]": stated as not established with the mark inline; SR3 is the round-44 record's resumable canceled-record label (corpus/knowledge/btrfs-scrub-record-r44.md:101). Honest non-claim, correctly marked.

Host reading
- capture.txt:3, capture.txt:4, capture.txt:5, capture.txt:2 all read exactly as cited in the row. "No unit was started or stopped" is a capture-conduct note, consistent with the entry's scope paragraph.

Limits context read (entry `## Limits`): GR3 pins systemd's documented behaviour (man source at the host's major version) plus the host's effective values, not a trace of a real stop — exactly what the row claims; the noted S237 registration gap (declared ranges not listing scrub.c:421) does not affect this row's quote legs, which the frozen counter re-verified as 12/12.
