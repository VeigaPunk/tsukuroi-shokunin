VERDICT: defect-found
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Scope: uncounted pre-read of row GR3 (`## GR3`, corpus/knowledge/btrfs-scrub-grounding-r45.md lines 181-225) at revision 2732ee6c06108c031c4d8043239b994e0504eb2f, with the `### Range gaps (R51)` block (entry lines 269-275) and Limits (240-267) for context. Entry copy: /fast/scratch/hyaku/tsukuroi-r51/R51W1PreCritGR3a/entry.md (removed after this report).

## Preliminary checks

- Section hash: `check-scrub-admission-r51.py --revision 2732ee6c… --section-hash --no-base-check` printed GR3 = 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c. Matches the item. (GR1 8eff9637…, GR2 27aa7abb… also printed by the structural run; not reviewed here.)
- Lint: `lint-grounding-r51.py --revision 2732ee6c…` → verdict PASS, lint_ok 3, rows_clean 3, quotes 63 (GR3: quotes 12, quote_bad 0; cites 6, cite_bad 0), gap_ok 1, gaps_computed 62, problems []. The lint does not check clause truth; everything below is the clause check.
- Snapshot digests (`sha256sum -c` in each snapshot dir, plus direct sha256sum):
  - S237 = `.ufo/waves/round-42/frozen/src/scrub.c` (btrfs-progs tag v7.1, FETCH.txt line 1-2): 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801. OK.
  - S244 = `.ufo/waves/round-44/frozen/src/btrfs-scrub@.service` (Arch btrfs-progs 7.1-1, FETCH.txt): eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252. OK.
  - S248 = `.ufo/waves/round-45/frozen/src/systemd.kill.xml` (systemd tag v262, FETCH.txt line 3): 448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72. OK.
  - S249 = `.ufo/waves/round-45/frozen/hostcap/capture.txt`: f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70. OK.
  - Registry rows in corpus/SOURCES.md (S237 line 246, S244 line 253, S248 line 257, S249 line 258) carry the same digests.

## Defects

### D1 — "KillSignal first, to every process" is cited to a line that does not name the signal
Entry (Statement, lines 184-186): "First the unit's `KillSignal=`, which this unit sets to SIGINT instead of the SIGTERM default; because the unit sets no `KillMode=`, the default `control-group` applies and every remaining process in the unit's control group receives it. Right after that signal systemd sends SIGCONT."
Contradicting/unsupporting pinned line: `S248` systemd.kill.xml:68 is quoted for this, but reads "…all remaining processes in the control group of this / unit will be killed on unit stop" — it says "killed", not which signal. The signal identity and "first" are at systemd.kill.xml:84-85 ("Processes will first be terminated via SIGTERM (unless the signal to send / is changed via KillSignal= …)"), :109 ("is sent as first step of shutting down a unit"), and the SIGTERM default at :112 ("Defaults to SIGTERM."). None of 84, 85, 109, 112 is quoted or cited in GR3.
Exact fix: add these quote rows directly after the existing `S248 systemd.kill.xml:68` quote:
- `**Quote.** S248 systemd.kill.xml:84: "<para>Processes will first be terminated via <constant>SIGTERM</constant> (unless the signal to send"`
- `**Quote.** S248 systemd.kill.xml:85: "is changed via <varname>KillSignal=</varname> or <varname>RestartKillSignal=</varname>). Optionally,"`
- `**Quote.** S248 systemd.kill.xml:109: "is sent as first step of shutting down a unit (see above), and is usually followed by"`
- `**Quote.** S248 systemd.kill.xml:112: "Defaults to <constant>SIGTERM</constant>.</para>"`
Clause fix: "…which this unit sets to SIGINT instead of the SIGTERM default (`S248` :112); that signal is the first step for every process the stop reaches (`S248` :84-85, :109). Because the unit sets no `KillMode=` (`S244` lines 6-10 have none), the default `control-group` applies (`S248` :101) and every remaining process in the unit's control group is included (`S248` :68)."
(Lines 84-85, 109, 112 are inside S248's declared range 62-116, so no gap-block change for them.)

### D2 — "With -B … does not fork" cites the test, not the flag
Entry (lines 192-193): "With `-B` the start does not fork into the background (btrfs-progs `scrub.c:1512`)".
`S237` scrub.c:1512 is `if (do_background) {`; the -B flag is what clears it, at scrub.c:1292-1293 (`case 'B':` / `do_background = false;` / `do_wait = true;`). Those lines are not cited anywhere in GR3, so the clause's premise is uncited. (Observed: scrub.c:1288 getopt "BdqrRc:n:f"; 1292-1293 as above.)
Exact fix: add quote rows:
- `**Quote.** S237 scrub.c:1292: "case 'B':"`
- `**Quote.** S237 scrub.c:1293: "do_background = false;"`
and change the clause to "With `-B` (`scrub.c:1292-1293` clears `do_background`) the start does not fork into the background (`scrub.c:1512`)".
Note for the L1: scrub.c:1292-1293 are outside S237's registry declared ranges (SOURCES.md line 246 declares 67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220, 1330-1340, 1498-1512, 1925-1945). The `### Range gaps (R51)` block (entry line 271) must be regenerated with `lint-grounding-r51.py --emit-gaps` after any such change, or the lint fails.

### D3 — "so SIGINT reaches that handler" is unqualified; the handler exists only in a window
Entry (lines 192-194): "installs its SIGINT handler on the mount's descriptor (`scrub.c:1546`, `:439`), so SIGINT reaches that handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9)."
Pinned bytes: the handler is set at scrub.c:1546 (`scrub_handle_sigint_child(fdmnt);`) and reset to SIG_DFL at scrub.c:1710 (`scrub_handle_sigint_child(-1);`). The only other SIGINT disposition is scrub.c:1522 (`scrub_handle_sigint_parent()`), which is inside the `if (pid)` fork-parent branch (1512-1543) and is not reached on the -B path. So on the -B path a SIGINT delivered before scrub.c:1546 finds no installed handler, and one delivered after scrub.c:1710 finds none either. The unqualified clause is therefore wrong for those windows. The sentence also cites :439 but not :442 (`cancel_fd = fd;`), which is where the descriptor is stored.
Exact fix: add quote rows `**Quote.** S237 scrub.c:442: "cancel_fd = fd;"` and `**Quote.** S237 scrub.c:1710: "scrub_handle_sigint_child(-1);"`, and replace "so SIGINT reaches that handler" with:
"…installs its SIGINT handler on the mount's descriptor (`scrub.c:1546`, `:439`, `:442`). From `scrub.c:1546` until `scrub.c:1710` resets it, SIGINT reaches that handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9); a SIGINT that arrives before `scrub.c:1546` finds no handler on this path (the only other SIGINT disposition, `scrub.c:1522`, is set only in the fork branch) [inference: which action the default disposition takes, and whether systemd leaves SIGINT at its default for this service, is not pinned here]."
Registry note: 442, 1293 and 1710 are outside S237's declared ranges; regenerate the gap block (see D2).

### D4 — The host's btrfs side is not pinned; the chain is btrfs-progs v7.1 source applied to an unobserved binary
Entry (Statement, line 183-184): "signals the running `btrfs scrub start -B` in this order under systemd v262". Every scrub.c citation (S237) is btrfs-progs tag v7.1 (FETCH.txt line 1-2; SOURCES.md line 246). S249 (`capture.txt`, all 9 lines read) records the kernel (line 1: uid/CapEff; line 2: kernel 7.2.11, systemd 262-1-arch), the unit's show values (line 3), the drop-in (lines 4-6), the unit drop-ins (line 7), and the device sysfs (lines 8-9). It records no btrfs-progs version and not the unit's `ExecStart=` line; the host's `btrfs` binary is never identified. S244's `ExecStart=/usr/bin/btrfs scrub start -B %f` (line 10) is the Arch 7.1-1 packaging file; only `KillSignal=2` is corroborated on the host.
Exact fix: in the Statement, change "under systemd v262" to "under systemd v262, with the `btrfs` side read from btrfs-progs v7.1 (`S237`; the packaged unit `S244` runs it) [inference: that the host's installed `btrfs` and its unit file are those v7.1 files; S249 records neither their version nor their ExecStart]". I did NOT run a pacman-database or binary version check: the item's execution class names only the commands listed, so whether the host has btrfs-progs 7.1-1 is open for the L1 to decide (a read of /var/lib/pacman/local for btrfs-progs would settle it; not run by this seat).

### D5 — The `FinalKillSignal=` / `SendSIGKILL=` parenthetical is cited to a line that lacks both names
Entry (line 187-188): "the request is repeated with SIGKILL (`FinalKillSignal=`, unless `SendSIGKILL=no`)."
`S248` :96 (quoted) supports "repeated with SIGKILL … or the signal specified via"; the words FinalKillSignal= and SendSIGKILL= are on :97 (`<varname>FinalKillSignal=</varname> (unless this is disabled via the <varname>SendSIGKILL=</varname>`), which is not cited.
Exact fix: add `**Quote.** S248 systemd.kill.xml:97: "<varname>FinalKillSignal=</varname> (unless this is disabled via the <varname>SendSIGKILL=</varname>"`. (Inside S248's declared range 62-116.)

### Non-blocking notes (not defects of truth)
- "SR3" and "SR9" are labels of rows in corpus/knowledge/btrfs-scrub-record-r44.md (SR9 at its lines 91-101 covers the timer/service and the SIGINT→cancel path; SR3 is the canceled-record row). GR3 does not define them; a parenthetical "(SR9 of btrfs-scrub-record-r44.md)" would make the row self-contained.
- The [inference] at line 195-196 ("a start killed before that write leaves the record as it was last written during the run") is conservatively marked. The pinned bytes write records to a temp file and rename it into place (scrub.c:513-535; progress writer scrub.c:897). The mark may stay; the timing question is genuinely not pinned.

## Claims checked and found supported (as written)
- Entry lines 183-184 "signals ... in this order under systemd v262": systemd tag v262 is the S248 source (FETCH.txt line 3; registry line 257); host reports `systemd 262 (262-1-arch)` (capture.txt:2). Supported (the systemd side only; see D4 for btrfs).
- Line 184-185 "KillSignal=SIGINT": S244 btrfs-scrub@.service:9 `KillSignal=SIGINT` (exact). Host: capture.txt:3 `KillSignal=2` (SIGINT).
- Line 185 "the unit sets no KillMode=": S244 lines 6-10 ([Service]: Nice, IOSchedulingClass, KillSignal, ExecStart) contain no KillMode; capture.txt:7 `unit_dropins` empty.
- Line 185-186 "the default control-group applies": S248:101 "Defaults to control-group." (exact); host capture.txt:3 `KillMode=control-group`.
- Line 186 "Right after that signal systemd sends SIGCONT": S248:114 "right after sending the signal specified in this setting, systemd will always send" and :115 "SIGCONT, to ensure …". Universal "always" is in the source.
- Line 187 "If processes remain once TimeoutStopSec= has passed": S248:91 "the delay configured via the TimeoutStopSec= has passed (applies to KillMode=: control-group …)". Supported.
- Line 187-188 "repeated with SIGKILL": S248:96 "the termination request is repeated with the SIGKILL signal or the signal specified via" — supported (the parenthetical needs :97, D5).
- Line 188-189 "the drop-in /etc/systemd/system.conf.d/10-faster-shutdown.conf sets DefaultTimeoutStopSec=5s": capture.txt:4 `stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s` (exact).
- Line 189 "no package owns that drop-in": capture.txt:5 `dropin_owner … none` (capture.sh lines 19-20 grep the pacman local DB files lists). Supported for the capture-time DB.
- Line 190 "[inference] that this default reaches every system unit": correctly marked; S248 does not pin systemd-system.conf(5); nothing in GR3's cited lines decides it.
- Line 190-191 "KillSignal=2, KillMode=control-group, TimeoutStopUSec=5s, FinalKillSignal=9 and SendSIGKILL=yes for btrfs-scrub@-.service": capture.txt:3, verbatim.
- Line 192 "the start does not fork (scrub.c:1512)": scrub.c:1512 `if (do_background) {` — supports the conditional; see D2 for the flag.
- Line 193 "scrub.c:439" handler conditional on descriptor: scrub.c:439 `.sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,` (exact); see D3 for the omitted :442.
- Line 193 "scrub.c:1546": scrub.c:1546 `scrub_handle_sigint_child(fdmnt);` (exact); fdmnt is `btrfs_open_mnt(path)` at scrub.c:1343, the mount's descriptor — supported.
- Line 194 "BTRFS_IOC_SCRUB_CANCEL (SR9)": scrub.c:421 `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);` (exact). The SR9 cross-reference resolves to btrfs-scrub-record-r44.md SR9 (see non-blocking note).
- Line 195-196 "Whether the start then writes its canceled record … is not established": marked as inference; pinned code (scrub.c:1701-1706 final write; 1123 progress writer) does not decide timing.
- Lines 222-225 "Host reading": capture.txt:3 (unit show), :4 (stop default, drop-in line 2), :5 (no owner), :2 (systemd 262-1-arch) — all match; "No unit was started or stopped": capture.sh:4 states it is read-only (no start/stop/enable).
- Quotes (GR3 has 12 quote rows): all whole-line matches to the cited lines (S244:9, :10; S248:68, :91, :96, :101, :108, :114, :115; S237:421, :439, :1546) — lint-confirmed; each quote's clause is covered except as noted in D1-D5.

## Not done
- No host command was run (EXEC-AUTHORIZED: named commands only). The host's btrfs-progs version and unit ExecStart were not observed (D4).
- No `systemctl` or pacman query; the capture file is the only host evidence used.
- No check of the GR1 or GR2 rows (out of this item's scope).
