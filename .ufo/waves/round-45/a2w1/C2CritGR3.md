ROW GR3 VERDICT: holds

Seat C2CritGR3 — counted critic for row GR3 of corpus/knowledge/btrfs-scrub-grounding-r45.md @ 18389f44cf6ce414d7be205998b29c79fb0b490c (row text at lines 91-127 of that blob). Adversarial read done; every quoted line opened in its pinned snapshot.

# Digest verification (all pass)

- .ufo/waves/round-45/frozen/src/SHA256SUMS: `sha256sum -c` → cmdline.c, dev-replace.c, systemd.kill.xml, kstrtox.c, vsprintf.c all OK.
- S248 = systemd.kill.xml, fetched from raw.githubusercontent.com/systemd/systemd/v262/man/systemd.kill.xml; tag v262 peels to 8cc40e0c5e9234bf45084751ac53b1fbfe70b492 (FETCH.txt) — matches the row's verified-at line.
- .ufo/waves/round-44/frozen/src/SHA256SUMS: btrfs-scrub@.service OK (S244). .ufo/waves/round-42/frozen/src/SHA256SUMS: scrub.c OK (S237 = btrfs-progs v7.1, FETCH.txt peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b).
- capture.txt sha256 = f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70, matching the doc's source line (S249).

# Quote-line fidelity (verbatim at cited line numbers)

- S244 btrfs-scrub@.service:9 `KillSignal=SIGINT` — exact.
- S244 btrfs-scrub@.service:10 `ExecStart=/usr/bin/btrfs scrub start -B %f` — exact.
- S248 systemd.kill.xml:68 `<para>If set to <option>control-group</option>, all remaining processes in the control group of this` — exact.
- xml:91 `the delay configured via the <varname>TimeoutStopSec=</varname> has passed` — exact.
- xml:96 `the termination request is repeated with the <constant>SIGKILL</constant> signal or the signal specified via` — exact.
- xml:101 `Defaults to <option>control-group</option>.` — exact.
- xml:108 `Specifies which signal to use when stopping a service.` — exact (the SIGTERM default is the unquoted tail of the same para, xml:112: `Defaults to <constant>SIGTERM</constant>.`).
- xml:114 `right after sending the signal specified in this setting, systemd will always send` — exact (SIGCONT named on xml:115).
- S237 scrub.c:421 `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);` — exact, inside `scrub_sigint_record_progress` (scrub.c:417-424), the SIGINT handler.

# Per-sentence judgment — Statement

1. "Stopping the packaged scrub service … signals the running `btrfs scrub start -B` in this order under systemd v262." — HOLDS. KillSignal "is sent as first step of shutting down a unit" (xml:108-109); ExecStart is `btrfs scrub start -B` (service:10). The order that follows is pinned by xml:114-115 (SIGCONT) and xml:91-97 (SIGKILL on TimeoutStopSec).

2. "First the unit's `KillSignal=`, which this unit sets to SIGINT instead of the SIGTERM default; because the unit sets no `KillMode=`, the default `control-group` applies and every remaining process in the unit's control group receives it." — HOLDS. Unit file is 10 lines, no `KillMode=` line (service:1-10); default control-group (xml:101); "all remaining processes in the control group … will be killed" (xml:68-69); SIGTERM default confirmed at xml:112. Effective mode corroborated: capture.txt:3 `KillMode=control-group`. Residual: capture.sh:22 only `ls`es drop-in dirs under /etc/systemd/system — an unchecked /run or /usr/lib drop-in could exist, but `systemctl show` measures the merged result, so the outcome is bound regardless.

3. "Right after that signal systemd sends SIGCONT." — HOLDS. xml:114-115: "right after sending the signal specified in this setting, systemd will always send SIGCONT". SendSIGHUP interplay (xml:93-100, default no) is irrelevant here since nothing enables it.

4. "If processes remain once `TimeoutStopSec=` has passed, the request is repeated with SIGKILL (`FinalKillSignal=`, unless `SendSIGKILL=no`)." — HOLDS. TimeoutStopSec listitem applies to KillMode=control-group (xml:91-94); the request "is repeated with the SIGKILL signal or the signal specified via FinalKillSignal=" unless disabled via SendSIGKILL= (xml:96-98). Parenthetical is compressed but accurate: FinalKillSignal= is the override knob (defaults to SIGKILL, xml:161-172), SendSIGKILL=no suppresses (xml:145-156). On this host FinalKillSignal=9 and SendSIGKILL=yes, so effective behavior is exactly as stated.

5. "On this host the unit's effective stop timeout is 5 s: the drop-in …/10-faster-shutdown.conf sets `DefaultTimeoutStopSec=5s` for every system unit without its own value, no package owns that drop-in, and `systemctl show` reports `KillSignal=2`, `KillMode=control-group`, `TimeoutStopUSec=5s`, `FinalKillSignal=9` and `SendSIGKILL=yes` for `btrfs-scrub@-.service`." — HOLDS. All five values verbatim in capture.txt:3; directive at drop-in line 2 (capture.txt:4); owner `none` (capture.txt:5). Causal attribution is sound: capture.sh greps both /etc/systemd/system.conf and all of /etc/systemd/system.conf.d (script lines 12-15) and finds no other setting; any /run or /usr/lib drop-in is lower precedence than /etc; and the observed value 5s differs from systemd's compiled default (90s), leaving the drop-in as the only source. The unit itself sets no TimeoutStopSec= (service:1-10). Verified live: my recapture (receipt recapture.txt) shows identical `TimeoutStopUSec=5s`.

6. "SIGINT reaches the foreground start's handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9)." — HOLDS. `-B` sets `do_background=false` (scrub.c:1247 `bool do_background = true;`, 1292-1293 `case 'B': do_background = false;`; OPTLINE at 1743 "do not background"), so the `if (do_background) { pid = fork(); … }` block at scrub.c:1512 is skipped and scrub.c:1546 `scrub_handle_sigint_child(fdmnt)` installs `scrub_sigint_record_progress` on the single foreground process; that handler's body is the quoted ioctl (scrub.c:417-424). Edge case honestly bounded: a SIGINT landing before line 1546 (during startup) would hit the default disposition and not cancel — but the claim covers "the running start". Residual: the claim is pinned at S237 (btrfs-progs v7.1) while the host's installed btrfs-progs version is uncaptured; the row presents exactly what the pinned source does, and its parenthetical (SR9) scopes it as mechanism.

7. "Whether the start then writes its canceled record (SR3) within the 5 s before SIGKILL is not established [inference: a start killed before that write leaves the record as it was last written during the run]." — HOLDS with honest [inference] marking. Code support for the inference: the final `scrub_write_progress` runs after the scrub loop and progress-thread join (scrub.c:1697-1704), while an initial zero write happens at start (scrub.c:1497-1504) and the progress thread writes periodically — so a SIGKILL before the final write indeed leaves the last periodic record. The uncertainty is not asserted as fact.

# Per-sentence judgment — Host reading

1. "`systemctl show btrfs-scrub@-.service` reports `KillMode=control-group KillSignal=2 SendSIGKILL=yes TimeoutStopUSec=5s FinalKillSignal=9` (capture.txt:3); the stop default comes from `10-faster-shutdown.conf` line 2 (capture.txt:4), a drop-in no installed package lists (capture.txt:5); systemd is 262-1-arch (capture.txt:2)." — HOLDS. All four capture lines verbatim (capture.txt:3 also carries FragmentPath and the row reports the five relevant properties, not claiming completeness); the capture.sh invocations are exactly `systemctl show … -p KillSignal -p KillMode -p TimeoutStopUSec -p FinalKillSignal -p SendSIGKILL` (script line 11) and `systemctl --version` (script line 10, output line "systemd 262 (262-1-arch)"). My read-only recapture reproduced every line identically except the timestamp (receipt recapture.txt + diff).

2. "No unit was started or stopped." — HOLDS. capture.sh header states it (script line 4) and the body only runs id, awk on /proc/self/status, uname, systemctl --version, systemctl show, grep/stat/cat/ls — no start/stop/kill.

# Residual risks noted (none move the verdict)

- The triage bullet (file line 137) says "gets SIGINT, SIGCONT and, 5 s later, SIGKILL" without the "if it survives" conditionality the Statement carries — a downstream compression, outside the Statement/Host reading judged here; the bullet's "[inference]" is honestly marked.
- SIGKILL is itself followed by SIGCONT under the same "always send SIGCONT" machinery — immaterial since SIGKILL is uncatchable; the stated order is complete for observable behavior.
- Host btrfs-progs version unpinned (see sentence 6); the row's framing is mechanism-at-pinned-source, not a host trace — explicitly declared in "Limits" (file lines 147-148: "pins systemd's documented behaviour … and the host's effective values, not a trace of a real stop").

All snapshot digests verified, all eight quotes verbatim at cited lines, every sentence follows from cited lines, both [inference] markings honest. Verdict: holds.

Receipts: .ufo/waves/round-45/a2w1/C2CritGR3/recapture.txt (fresh read-only capture), digest verification transcript in this report body. No tools installed. No mutations: lane read-only; capture.sh writes only its argument, which I pointed at scratch.
