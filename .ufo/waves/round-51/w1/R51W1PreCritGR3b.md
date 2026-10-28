VERDICT: defect-found
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Seat R51W1PreCritGR3b (critic, uncounted pre-read, row GR3 at revision 2732ee6c06108c031c4d8043239b994e0504eb2f).

## Checks run

- Entry extracted to scratch (`git show 2732ee6c…:corpus/knowledge/btrfs-scrub-grounding-r45.md`, 348 lines). GR3 is entry.md:181-225.
- Section hash: `check-scrub-admission-r51.py --revision 2732ee6c… --section-hash --no-base-check` printed `"GR3": "43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c"`. Matches. (Also GR1 8eff9637… and GR2 27aa7abb… printed, unread by me beyond that.)
- Lint: `lint-grounding-r51.py --revision 2732ee6c…` → `"verdict": "PASS"`, `"lint_ok": 3`, GR3 `cites: 6, cite_bad: 0, quotes: 12, quote_bad: 0`, `gap_ok: 1`, `gap_missing: []`, `gap_extra: []`. Receipt: `.ufo/waves/round-51/w1/R51W1PreCritGR3b/lint-grounding-r51.out`. Lint does not check clause truth; everything below is my reading.
- Pinned digests (`sha256sum -c SHA256SUMS`, and direct hash):
  - round-45/frozen/src: `systemd.kill.xml: OK` (S248; SOURCES.md:257 raw sha 448322…910e72 matches).
  - round-44/frozen/src: `btrfs-scrub@.service: OK` (S244; SOURCES.md:253 sha eaa7af92…240252 matches).
  - round-42/frozen/src: `scrub.c: OK` (S237; SOURCES.md:246 raw sha 48df2e…8f0801 matches).
  - round-45/frozen/hostcap/capture.txt: sha256 f5958a83…3991e70 (S249; SOURCES.md:258). hostcap has no SHA256SUMS file; the digest matches the entry's pin.
- Snapshot-to-row mapping: S237 = `.ufo/waves/round-42/frozen/src/scrub.c` = btrfs-progs v7.1 `cmds/scrub.c` (SOURCES.md:246). S244 = `.ufo/waves/round-44/frozen/src/btrfs-scrub@.service` (SOURCES.md:253). S248 = `.ufo/waves/round-45/frozen/src/systemd.kill.xml` (SOURCES.md:257). S249 = `.ufo/waves/round-45/frozen/hostcap/capture.txt` (SOURCES.md:258).
- Whole-line quotes read against the bytes and matched: S244:9 `KillSignal=SIGINT`; S244:10 `ExecStart=/usr/bin/btrfs scrub start -B %f`; S248:68, 91, 96, 101, 108, 114, 115; S237:421, 439, 1546.

## Defects

### D1 — unqualified SIGINT-reaches-handler clause
Entry (GR3 Statement, ll.13-14): "installs its SIGINT handler on the mount's descriptor (`scrub.c:1546`, `:439`), so SIGINT reaches that handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9)."
Pinned contradiction: the handler is installed only at scrub.c:1546 (`scrub_handle_sigint_child(fdmnt);`). Before that line, `scrub_start` runs `btrfs_open_mnt` (scrub.c:1343), sysfs limit writes (scrub.c:1413-1414) and the progress-socket setup (scrub.c:1459-1499). The only SIGINT dispositions in scrub.c are `sigaction(SIGINT, …)` at scrub.c:433 and :443 (grep of the file); no `signal(` call exists. So a SIGINT arriving before scrub.c:1546 is not caught by any handler in this file; its disposition is whatever the process inherited at exec, which is not pinned here. Also after scrub.c:1710 (`scrub_handle_sigint_child(-1)`) the handler is SIG_DFL again.
Exact replacement wording:
"installs its SIGINT handler on the mount's descriptor at `scrub.c:1546` (the handler is the `:439` branch with `fd != -1`), so a SIGINT that arrives after that line reaches the handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9). No SIGINT disposition is set elsewhere in `scrub.c` (`:433`, `:443` are the only `sigaction(SIGINT, …)` calls, `:1710` restores SIG_DFL), so a SIGINT that arrives before `:1546` or after `:1710` takes the disposition the process inherited at exec [inference: not pinned here]."
Registration note for L1: `scrub.c:433` and `:443` are not in S237's declared SOURCES ranges (1498-1512 among them); citing them changes the `### Range gaps (R51)` block, which must be regenerated with `lint-grounding-r51.py --emit-gaps`.

### D2 — "-B" is cited to the wrong line
Entry (GR3 Statement, l.13): "With `-B` the start does not fork into the background (btrfs-progs `scrub.c:1512`)."
Pinned: scrub.c:1512 is only `if (do_background) {` — the fork guard. The `-B` link is scrub.c:1292-1293: `case 'B': do_background = false;`. The clause is true, but its cited line does not show `-B`, so a reader who opens :1512 cannot see the premise.
Exact replacement wording:
"With `-B` the start does not fork into the background (btrfs-progs `scrub.c:1292-1293` sets `do_background = false`; `scrub.c:1512` forks only when it is set)."
Registration note: `scrub.c:1292-1293` is outside S237's declared SOURCES ranges (1330-1340, 1498-1512 among them), so the R51 gap block must be regenerated as in D1.

### D3 — "in this order" omits the optional SIGHUP step, and SendSIGHUP is not captured on this host
Entry (GR3 Statement, ll.3-7): the sequence is KillSignal, then SIGCONT, then SIGKILL, "in this order under systemd v262".
Pinned: systemd.kill.xml:84-87 — "Processes will first be terminated via SIGTERM (unless the signal to send is changed via KillSignal=…). Optionally, this is immediately followed by a SIGHUP (if enabled with SendSIGHUP=)." The entry cites none of these lines. S244 (btrfs-scrub@.service, 1-10) sets no `SendSIGHUP=`. capture.txt:3 (the `unit_show` line) queries KillSignal, KillMode, TimeoutStopUSec, FinalKillSignal, SendSIGKILL, FragmentPath, but not SendSIGHUP; no other capture line gives it. So on this host the absence of SIGHUP is unobserved.
Exact replacement wording (insert after the KillSignal sentence, ending "…and is usually followed by SIGKILL"):
"A SIGHUP follows immediately only if `SendSIGHUP=` is enabled (`systemd.kill.xml:84-87`); `btrfs-scrub@.service` (`S244`, lines 1-10) does not set it, and this host's value was not captured [inference: the systemd default is no, which is outside the pinned lines]."
Also add to the Quote list, if the citation is wanted: `S248` systemd.kill.xml:84: "<para>Processes will first be terminated via <constant>SIGTERM</constant> (unless the signal to send".

### D4 — the SIGTERM default is uncited
Entry (GR3 Statement, l.5): "which this unit sets to SIGINT instead of the SIGTERM default".
Pinned: systemd.kill.xml:112 "        Defaults to <constant>SIGTERM</constant>.</para>". None of the cited S248 lines (68, 91, 96, 101, 108, 114, 115) contains it; line 108 is "Specifies which signal to use when stopping a service…" and ends before the default.
Exact replacement wording: add a Quote entry: "**Quote.** `S248` systemd.kill.xml:112: "Defaults to <constant>SIGTERM</constant>.</para>"". The sentence itself stays.

### D5 — "the unit sets no KillMode=" is an absence with no cited range
Entry (GR3 Statement, l.5): "because the unit sets no `KillMode=`, the default `control-group` applies".
Pinned: S244 btrfs-scrub@.service:1-10 has no `KillMode=` (I read all ten lines; grep of the file for KillMode/SendSIGHUP returns 0). The entry cites only lines 9 and 10.
Exact replacement wording: "…because the unit sets no `KillMode=` (`S244` btrfs-scrub@.service:1-10, the whole unit), the default `control-group` applies…". Keep the existing S248:101 quote for the default.

### D6 — host binding of the btrfs-progs code is not captured
Entry (GR3 Statement, l.13; Host reading): the start path is described by btrfs-progs `scrub.c:1512`, `:1546`, `:439`; "`btrfs scrub start -B`" runs on this host.
Pinned: the code is btrfs-progs v7.1 (S237, SOURCES.md:246). capture.txt (S249) records systemd, kernel, the unit's systemctl properties, drop-ins, sysfs and devinfo, but no btrfs-progs version or binary digest. capture.txt:3 does give `FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service`, and `KillSignal=2` corroborates S244:9, but the host unit file itself was not hashed. The S244 SOURCES row names btrfs-progs 7.1-1 as the packaging that installs this unit, so the installed binary is probably v7.1 — that is inference, not observation.
Exact replacement wording: add to the Host reading paragraph: "The btrfs-progs code cited above is v7.1 (`S237`, the version packaged as 7.1-1 with this unit, `S244`); the installed `btrfs` binary's version was not captured by S249 [inference: it is that package]. The host's `btrfs-scrub@.service` file was not digest-pinned; its `KillSignal=2` matches `S244` line 9."

## Clauses checked and found supported (no defect)

- "the unit's `KillSignal=`, which this unit sets to SIGINT" — S244:9 (quoted); host `KillSignal=2` (capture.txt:3).
- "every remaining process in the unit's control group receives it" under `KillMode=control-group` — S248:68-69 ("all remaining processes in the control group of this unit will be killed on unit stop"), S248:101 (quoted default). The per-signal reach is S248:84-85 and :108-110, which are uncited but support it.
- "Right after that signal systemd sends SIGCONT" — S248:114-115 (quoted; "will always send").
- "If processes remain once TimeoutStopSec= has passed, the request is repeated with SIGKILL (FinalKillSignal=, unless SendSIGKILL=no)" — S248:91-93, 96-98 (quoted; FinalKillSignal and SendSIGKILL named at :96-97).
- "the unit's effective stop timeout is 5 s" — capture.txt:3 (`TimeoutStopUSec=5s`).
- "the drop-in … sets DefaultTimeoutStopSec=5s" — capture.txt:4 (`/etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`). The capture's grep covers /etc/systemd/system.conf and all /etc drop-ins; the other drop-in (99-omarchy-nofile.conf) sets no such key.
- "no package owns that drop-in" — capture.txt:5 `dropin_owner … none`; capture.sh:19 greps `/var/lib/pacman/local/*/files` for the path, so the claim is pacman-only, which is what the sentence says.
- "systemd is 262-1-arch" — capture.txt:2. Man page at tag v262 (SOURCES.md:257); the host version string is `262`.
- "`systemctl show btrfs-scrub@-.service` reports KillMode=control-group KillSignal=2 SendSIGKILL=yes TimeoutStopUSec=5s FinalKillSignal=9" — capture.txt:3; capture.sh:11 queries the unit `btrfs-scrub@-.service`.
- "No unit was started or stopped." — capture.sh:4-5 (read-only; systemctl show only) and :11.
- "cancel: `ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL)`" — S237:421 (quoted). `cancel_fd` is set to `fdmnt` by `scrub_handle_sigint_child(fd)` at scrub.c:442; quote at :439 and :1546 match.
- "`:439`" handler selection and "`:1546`" install — S237:439 and :1546 (quoted).
- Inference mark on DefaultTimeoutStopSec reaching every system unit — correctly marked: systemd-system.conf(5) is not pinned, and the host value shows the 5 s for this unit only.
- Inference mark on the SR3 canceled record "within the 5 s before SIGKILL" — correctly marked: the canceled-record write is scrub.c:1702, after the device-thread joins (scrub.c:1608) and gated on `do_record` (:1701); timing is not in the pinned bytes. The inference's second clause holds on the code: `scrub_write_progress` writes a `tmp` file and renames it (scrub.c:917-925), so a kill mid-write leaves the previous record.
- Word "every" (two uses) and "always" (SIGCONT) are supported by S248:68-69 and S248:114.
- Cross-references SR3 and SR9 resolve to btrfs-scrub-record-r44.md:91-101 (SR9) and the SR3 entries in the record family; SR9's text ("a SIGINT sent to it … cancels the running scrub") agrees with the row.

## Not done

- No runs of any tool beyond those listed; I did not run `pacman -Q` or read the pacman database myself (execution class limited the commands).
- I did not check the GR1 or GR2 rows, the controls, or the other lanes.
- Receipts: `.ufo/waves/round-51/w1/R51W1PreCritGR3b/lint-grounding-r51.out` (lint output). Scratch removed after copying.
