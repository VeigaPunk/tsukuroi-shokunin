VERDICT: defect-found
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Seat R51W1PreRevGR3a, uncounted pre-read of row GR3 at revision 2732ee6c06108c031c4d8043239b994e0504eb2f. Not a counted verdict; the negatives below are for the pre-w2 amendment.

## Setup and mechanical checks

- Entry extracted: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/knowledge/btrfs-scrub-grounding-r45.md` (348 lines). GR3 is lines 181-226; `### Range gaps (R51)` is lines 269-275; Limits is lines 240-268.
- `check-scrub-admission-r51.py --revision 2732ee6c… --section-hash --no-base-check` printed `GR3: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c`. Matches the item. GR1 and GR2 hashes also printed (8eff9637…, 27aa7abb…).
- `lint-grounding-r51.py --revision 2732ee6c…`: verdict PASS, rows_clean 3, quotes 63 / quote_bad 0, cites 28 / cite_bad 0, gaps_computed 62, gap_ok 1, snapshot_problems []. Per row GR3: quotes 12 / quote_bad 0, cites 6 / cite_bad 0.
- Snapshot digests (`sha256sum -c` in each snapshot directory, and direct hash for the capture):
  - S237 = `.ufo/waves/round-42/frozen/src/scrub.c` (btrfs-progs v7.1 `cmds/scrub.c`, 57034 bytes) = 48df2e2f…0801: OK (SOURCES.md:246 agrees). The round-44 `scrub.c` (100417 bytes, f347931b…) is the kernel file, S242, not S237.
  - S244 = `.ufo/waves/round-44/frozen/src/btrfs-scrub@.service` = eaa7af92…0252: OK (SOURCES.md:253 agrees).
  - S248 = `.ufo/waves/round-45/frozen/src/systemd.kill.xml` = 448322830dbbd02c…ae7910e72: OK (SOURCES.md:257 agrees).
  - S249 = `.ufo/waves/round-45/frozen/hostcap/capture.txt` = f5958a83…c3991e70: matches the item and SOURCES.md:258. No SHA256SUMS file exists in that directory.
- Scope note: `--section-hash` and the lint do not check clause truth. Everything below is by reading the pinned lines.

## Defects

### D1. Citation does not carry the signal claim (certain)

Entry, GR3 Statement: "…and every remaining process in the unit's control group receives it."

Cited line `S248 systemd.kill.xml:68` reads: "If set to control-group, all remaining processes in the control group of this" (continuing on line 69 with "unit will be killed on unit stop"). It says "killed", not that the KillSignal signal is sent. The signal replacement is at systemd.kill.xml:84-85, which the row does not cite:
- `systemd.kill.xml:84`: "Processes will first be terminated via SIGTERM (unless the signal to send"
- `systemd.kill.xml:85`: "is changed via KillSignal= or RestartKillSignal=). Optionally,"

Exact replacement for the clause: "…and every remaining process in the unit's control group receives it (`systemd.kill.xml:68` for `control-group`; `:84-85` for the signal that replaces SIGTERM)." Add two quote entries:
- **Quote.** `S248` systemd.kill.xml:84: "<para>Processes will first be terminated via <constant>SIGTERM</constant> (unless the signal to send"
- **Quote.** `S248` systemd.kill.xml:85: "is changed via <varname>KillSignal=</varname> or <varname>RestartKillSignal=</varname>). Optionally,"

(Both lines are inside the S248 declared range 62-116 in SOURCES.md:257, so no gap-block change.)

### D2. The "first step" order claim is cited without its line (certain)

Entry: "First the unit's `KillSignal=`, which this unit sets to SIGINT…". The only cited line for KillSignal is `systemd.kill.xml:108`, which ends "This controls the signal that". The words "sent as first step of shutting down a unit" are on line 109, which is not cited:
- `systemd.kill.xml:109`: "is sent as first step of shutting down a unit (see above), and is usually followed by"

Exact replacement: "First the unit's `KillSignal=` (`systemd.kill.xml:108-109`), which this unit sets to SIGINT instead of the SIGTERM default (`systemd.kill.xml:112`)…". Add quote: **Quote.** `S248` systemd.kill.xml:109: "is sent as first step of shutting down a unit (see above), and is usually followed by"

Note: `:112` reads "Defaults to SIGTERM." (cited in the row's SIGTERM default clause only implicitly; add it as the default citation). Line 109 is inside declared range 62-116.

### D3. "SIGINT reaches that handler" is stated without its installation point (certain)

Entry: "…installs its SIGINT handler on the mount's descriptor (`scrub.c:1546`, `:439`), so SIGINT reaches that handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9)."

Pinned bytes: the only installation of the cancel handler on the no-fork path is `scrub_handle_sigint_child(fdmnt)` at `S237 scrub.c:1546`, whose sigaction is at `scrub.c:436-443`. Nothing in `scrub.c` before line 1546 installs a SIGINT handler on that path. The other `sigaction(SIGINT, …)` at `scrub.c:428-433` is `SIG_IGN` in the forked parent (reached only through `do_background`, which `-B` clears). So between process start and `scrub.c:1546`, a SIGINT does not reach `scrub_sigint_record_progress` at all. The row's unqualified "so SIGINT reaches that handler" is therefore not true for the whole run.

Exact replacement: "…installs its SIGINT handler on the mount's descriptor when it reaches `scrub.c:1546` (`:439`); from that line on, SIGINT reaches that handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9). Before that line this code installs no SIGINT handler [inference: which disposition a SIGINT meets before `scrub.c:1546` is not pinned here]."

The new bracketed mark is the reviewer's suggestion; the L1 decides the wording. The first-part claim (handler installed at 1546, issues ioctl at 421) is supported as cited.

### D4. The `-B` no-fork claim cites the branch, not the option (certain)

Entry: "With `-B` the start does not fork into the background (btrfs-progs `scrub.c:1512`)."

`scrub.c:1512` is `if (do_background) {` (the fork branch). It is skipped only because `-B` clears the flag:
- `S237 scrub.c:1247`: "bool do_background = true;" (default)
- `S237 scrub.c:1292-1293`: `case 'B':` then `do_background = false;` (the -B option; `scrub.c:1293` is `do_background = false;` with leading tabs)

Neither 1247 nor 1293 is in S237's declared ranges (SOURCES.md:246: 67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220, 1330-1340, 1498-1512, 1925-1945). Adding them means the gap block changes.

Exact replacement: "With `-B` the start does not fork into the background (`scrub.c:1293` clears `do_background` for `-B`, whose default is `true` at `:1247`, so the fork branch at `:1512` is skipped)." Add quote: **Quote.** `S237` scrub.c:1293: "do_background = false;"

Required with D4: the `### Range gaps (R51)` S237 bullet must be regenerated on the amended revision with `python3 tools/lint-grounding-r51.py --revision <new REV> --emit-gaps`. By hand it becomes `- S237 scrub.c: 421, 439, 1293, 1546` (and `1247` too if cited). The lint fails if the block is hand-edited.

## Provenance note (not a defect; optional qualifier)

- The clause "because the unit sets no KillMode=" is supported only by the packaged unit file S244 (btrfs-progs 7.1-1 bytes, lines 1-10, no KillMode line). The capture (`capture.txt:3`) reports `KillMode=control-group`, which is also systemd's default, so `systemctl show` cannot show that the installed unit omits the directive, and the installed btrfs-progs version and unit bytes are not captured. If the L1 wants the clause fully host-bound, the optional wording is: "the packaged unit (S244, btrfs-progs 7.1-1) sets no `KillMode=`; `systemctl show` reports the default `control-group` (capture.txt:3)."

## Clauses checked and found supported

- Statement, "in this order under systemd v262": systemd.kill.xml:108-109 (KillSignal first), :114-115 (SIGCONT "will always" follow), :91-97 (SIGKILL after TimeoutStopSec, FinalKillSignal, SendSIGKILL). Tag v262 per SOURCES.md:257.
- "instead of the SIGTERM default": systemd.kill.xml:112 "Defaults to SIGTERM"; btrfs-scrub@.service:9 `KillSignal=SIGINT` (S244).
- "the default control-group applies": systemd.kill.xml:101 "Defaults to control-group."
- "unit sets no KillMode=": S244 lines 1-10 contain no KillMode line (see provenance note).
- "every remaining process … receives it" for control-group: :68 ("all remaining processes … killed on unit stop"), plus :84-85 (see D1).
- "If processes remain once TimeoutStopSec= has passed, … SIGKILL (FinalKillSignal=, unless SendSIGKILL=no)": systemd.kill.xml:91-93, :96-97.
- Quotes (12 of 12 read at the cited lines): S244:9 `KillSignal=SIGINT`; S244:10 `ExecStart=/usr/bin/btrfs scrub start -B %f`; S248:68, :91, :96, :101, :108, :114, :115; S237:421 `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);`, :439 `.sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,`, :1546 `scrub_handle_sigint_child(fdmnt);`.
- Handler issues the ioctl: scrub.c:417-424 (`scrub_sigint_record_progress` calls `ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL)` at :421); `cancel_fd = fd` set in scrub.c:442.
- Installation on fdmnt: scrub.c:1343 `fdmnt = btrfs_open_mnt(path);`, :1546 installs it; scrub.c:436-443 defines the installer.
- Fork branch: scrub.c:1512 `if (do_background) {` with the fork at :1513; skipped under -B (see D4).
- "On this host the unit's effective stop timeout is 5 s" and "`systemctl show` reports KillSignal=2, KillMode=control-group, TimeoutStopUSec=5s, FinalKillSignal=9, SendSIGKILL=yes for btrfs-scrub@-.service": capture.txt:3 (line 3 verbatim).
- "the drop-in /etc/systemd/system.conf.d/10-faster-shutdown.conf sets DefaultTimeoutStopSec=5s": capture.txt:4 (`:2:DefaultTimeoutStopSec=5s`).
- "no package owns that drop-in": capture.txt:5 `dropin_owner … none` (capture.sh:19 checks the pacman local DB only).
- Host reading: systemd 262-1-arch at capture.txt:2; no unit started or stopped (capture.sh is read-only, lines 8-31).
- Marked inference 1, "that this default reaches every system unit without its own TimeoutStopSec= is [inference]": correctly marked; systemd-system.conf(5) is not pinned (SOURCES.md:257 pins only systemd.kill.xml).
- Marked inference 2, "[inference: a start killed before that write leaves the record as it was last written during the run]": correctly marked; the pinned scrub.c:421 handler only issues the cancel ioctl and does not show the write order.
- Gap-block cross-check: S237 declared ranges include 1498-1512, so :1512 is not a gap; 421, 439, 1546 are gaps and are listed (lint gap_ok 1). The gap block is consistent with the current citations; it becomes inconsistent with D4 unless regenerated.

## Verification gaps

- No live `btrfs scrub start -B` stop was run (none in scope); the systemd behaviour is from documentation source, not a trace.
- Behaviour of a SIGINT delivered before `scrub.c:1546` (D3) depends on the inherited disposition, which no pinned file covers; the proposed wording marks it as [inference].
- Words "first", "every", "always" were checked against the pinned systemd.kill.xml and scrub.c text only.
