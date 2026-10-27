ROW GR3 VERDICT: holds
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Seat R47CritGR3a, item C1-GR3-R47CritGR3a. Attacked row GR3 of corpus/knowledge/btrfs-scrub-grounding-r45.md at revision 77e9e2b2e96b85d8f048ae2087e246a542b71611. Verdict: holds — every clause of the Statement and Host reading is supported by the cited lines in the pinned snapshots; inference marks are correctly placed.

== Hash and structural binding ==

- Frozen counter `tools/check-scrub-admission-r47.py --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash` printed `"GR3": "43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c"`, `structural_ok: 1`, `problems: []` — matching the expected value in my item.
- Independent re-derivation: extracted the extent from `## GR3` up to (exclusive) `## How this changes OS triage` from the frozen blob and computed sha256 over the LF-joined lines with no trailing newline (the counter's `'\n'.join(lines[i:j])` form in its `section_hashes` function) — got `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c`, identical to the counter.
- Extent integrity: no other `## ` header inside the GR3 extent (counter structural check passed; the row runs 46 lines to just before `## How this changes OS triage`).

== Snapshot digest verification ==

- `.ufo/waves/round-45/frozen/src/SHA256SUMS`: `systemd.kill.xml: OK` (S248, systemd v262 man page source).
- `.ufo/waves/round-44/frozen/src/SHA256SUMS`: `btrfs-scrub@.service: OK` (S244), also `scrub.c: OK`, `sysfs.c: OK` (S242/S243 present, not quoted by this row).
- `.ufo/waves/round-42/frozen/src/SHA256SUMS`: `scrub.c: OK` (S237, btrfs-progs source).
- `.ufo/waves/round-45/frozen/hostcap/capture.txt` (S249): sha256sum = `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`, exactly the digest declared in the entry header line ("sha256 f5958a83...c3991e70").

== Quote verification (all 14 quotes verbatim on cited lines) ==

- S244 `btrfs-scrub@.service:9` = `KillSignal=SIGINT` — exact. `:10` = `ExecStart=/usr/bin/btrfs scrub start -B %f` — exact.
- S248 `systemd.kill.xml:68` control-group quote — exact. `:91` TimeoutStopSec= delay quote — exact. `:96` SIGKILL/FinalKillSignal= quote — exact. `:101` "Defaults to control-group" — exact. `:108` KillSignal= quote — exact. `:114` SIGCONT-always-sent quote — exact. `:115` SIGCONT continuation — exact.
- S237 `scrub.c:421` = `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);` — exact. `:1546` = `scrub_handle_sigint_child(fdmnt);` — exact. `:439` = `.sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,` — exact.

== Clause-by-clause attack ==

- "signals the running `btrfs scrub start -B` in this order under systemd v262": capture.txt:2 reads `systemd 262 (262-1-arch)`; S244:10 pins the unit's command as `btrfs scrub start -B %f`. Supported.
- "First the unit's KillSignal=, which this unit sets to SIGINT instead of the SIGTERM default": S244:9 `KillSignal=SIGINT`; S248:112 (KillSignal= entry) "Defaults to SIGTERM". Supported.
- "the unit sets no KillMode=, the default control-group applies and every remaining process in the unit's control group receives it": the service file is 10 lines with `grep -in 'killmode|timeoutstop|sendsigkill|finalkill'` returning nothing (rc=1, verified this seat); S248:101 "Defaults to control-group"; S248:68-69 "all remaining processes in the control group of this unit will be killed on unit stop". Host corroboration capture.txt:3 `KillMode=control-group`. Supported.
- "Right after that signal systemd sends SIGCONT": S248:114-115 "right after sending the signal specified in this setting, systemd will always send SIGCONT, to ensure that even suspended tasks can be terminated cleanly". Supported.
- "If processes remain once TimeoutStopSec= has passed, the request is repeated with SIGKILL (FinalKillSignal=, unless SendSIGKILL=no)": S248:91-94 (delay item), S248:96-98 "the termination request is repeated with the SIGKILL signal or the signal specified via FinalKillSignal= (unless this is disabled via the SendSIGKILL= option)". Supported; the parenthetical faithfully carries the doc's FinalKillSignal=/SendSIGKILL= nuance.
- "On this host the unit's effective stop timeout is 5 s: the drop-in /etc/systemd/system.conf.d/10-faster-shutdown.conf sets DefaultTimeoutStopSec=5s": capture.txt:4 = `stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf` line 2 `DefaultTimeoutStopSec=5s` (path and `line 2` rendered with a space here so the report carries no pseudo-citation; the captured line itself places the line number after the path). Supported. The parenthetical "that this default reaches every system unit without its own TimeoutStopSec= is [inference]: systemd-system.conf(5) is not pinned here" is a correctly placed inference mark — the pinned sources stop at the drop-in line and the unit's effective value.
- "no package owns that drop-in": capture.txt:5 = `dropin_owner /etc/systemd/system.conf.d/10-faster-shutdown.conf none`. Supported.
- "systemctl show reports KillSignal=2, KillMode=control-group, TimeoutStopUSec=5s, FinalKillSignal=9 and SendSIGKILL=yes for btrfs-scrub@-.service": capture.txt:3 = `unit_show FinalKillSignal=9 FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service KillMode=control-group KillSignal=2 SendSIGKILL=yes TimeoutStopUSec=5s` — all five properties present verbatim. Supported.
- "With -B the start does not fork into the background (btrfs-progs scrub.c:1512)": S237 scrub.c:1512 is `if (do_background) {` with `pid = fork();` at :1513; the option parsing at scrub.c:1292-1293 (`case 'B': do_background = false; do_wait = true;`) completes the support — under -B the guard is false and no fork occurs. Cited line is the deciding guard; clause supported by the cited region.
- "installs its SIGINT handler on the mount's descriptor (scrub.c:1546, :439), so SIGINT reaches that handler, which issues BTRFS_IOC_SCRUB_CANCEL": S237 scrub.c:1546 `scrub_handle_sigint_child(fdmnt);`; :439 handler is `scrub_sigint_record_progress` when fd != -1; :442 `cancel_fd = fd;` binds the handler's ioctl fd to fdmnt; :421 `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);`. Chain fully supported.
- "Whether the start then writes its canceled record (SR3) within the 5 s before SIGKILL is not established [inference: ...]": properly marked as not established; nothing asserted as fact beyond the pinned lines.
- Host reading: systemd 262-1-arch (capture.txt:2), the five unit_show properties (capture.txt:3), stop default from 10-faster-shutdown.conf line 2 (capture.txt:4), drop-in owner none (capture.txt:5) — all verbatim. "No unit was started or stopped": capture header line 1 shows `uid=1000 CapEff=0000000000000000`, a read-only capture. Supported.

== Notes (non-blocking) ==

- The clause citing scrub.c:1512 for the no-fork property relies on the reader also seeing the `-B` parsing at scrub.c:1292-1293; both are in the same pinned snapshot, so the citation resolves and the clause is true. Not a defect — a reviewer following the citation finds the deciding guard one line above the fork.
- The [inference] mark inside the 5 s sentence is load-bearing and correctly scoped: only the reach of DefaultTimeoutStopSec= to units without their own TimeoutStopSec= is inferred; the unit's own effective 5 s is observed (capture.txt:3 `TimeoutStopUSec=5s`).
- Limits section confirms GR3 "pins systemd's documented behaviour (man page source at the host's major version) and the host's effective values, not a trace of a real stop" — consistent with what the row does. Round-47 pre-wave amendment touched GR2 only (per the Limits note citing .ufo/waves/round-46/r1/V46ResCritGR2.md); GR3 bytes judged here are the current bytes.

No counterexample found; the row is admissible as written.
