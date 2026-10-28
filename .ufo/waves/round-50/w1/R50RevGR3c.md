ROW GR3 VERDICT: partly
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

I did not write GR3 and I am not its author. Everything below is against the freeze bytes at
8029cdba1049df25632c91a23c8db4eefb54be5f, extracted with
`git -C .../tsukuroi-shokunin show 8029cdb…:corpus/knowledge/btrfs-scrub-grounding-r45.md` (307 lines;
GR3 = entry lines 153-198, i.e. `## GR3` up to the `## How this changes OS triage` heading at 199).

## Frame verified first
- Section hash recomputed independently (the row's lines joined with LF, no trailing LF):
  `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` — equals the frozen GR3 value and the
  counter's own report: `check-scrub-admission-r50.py --revision 8029cdb… --section-hash` →
  `{"section_sha256": {… "GR3": "43430a14…c32c"}, "structural_ok": 1, "problems": []}`.
- Digests, all checked by `sha256sum -c SHA256SUMS` in each snapshot directory: round-45/src 5/5 OK,
  round-44/src 5/5 OK, round-42/src 2/2 OK. `hostcap/capture.txt` = `f5958a83…3991e70` (matches the item and
  SOURCES.md:258), `hostcap/capture.sh` = `c6d2c448…180a751fc` (matches SOURCES.md:258).
- S-row → snapshot file, as the item asks: **S248** = `.ufo/waves/round-45/frozen/src/systemd.kill.xml`
  (44832283…e7910e72, fetched from systemd tag v262 per `src/FETCH.txt`); **S244** =
  `.ufo/waves/round-44/frozen/src/btrfs-scrub@.service` (eaa7af92…00fb240252, btrfs-progs packaging tag 7.1-1);
  **S237** = `.ufo/waves/round-42/frozen/src/scrub.c` (48df2e2f…d8ed8f0801, btrfs-progs tag v7.1);
  **S249** = `.ufo/waves/round-45/frozen/hostcap/capture.txt`.
- All 12 `**Quote.**` lines of GR3 resolve at the cited line as exact text (scripted substring check against the
  digest-pinned snapshots): S244:9, S244:10, S248:68, :91, :96, :101, :108, :114, :115, S237:421, :1546, :439.
  The XML quotes carry their element prefix exactly (`<para>` at :68/:101/:114, `<listitem><para>` at :91/:108),
  and the code quotes carry no lost `* ` or tab prefix.

## Clause by clause
1. Order SIGINT → SIGCONT → SIGKILL "under systemd v262": `systemd.kill.xml:84-87` ("Processes will first be
   terminated via SIGTERM (unless the signal to send is changed via KillSignal=…)"), `:91-93` (timeout applies to
   `control-group`), `:96-97` ("the termination request is repeated with the SIGKILL signal or the signal specified
   via FinalKillSignal= (unless this is disabled via the SendSIGKILL= option)"), `:114-115` ("right after sending the
   signal specified in this setting, systemd will always send SIGCONT"). Host is `systemd 262 (262-1-arch)`
   (`capture.txt:2`; live `systemctl --version` today reads the same). Holds.
2. "KillSignal= … this unit sets to SIGINT instead of the SIGTERM default": `btrfs-scrub@.service:9`
   `KillSignal=SIGINT`, `systemd.kill.xml:112` "Defaults to SIGTERM". Holds.
3. "no KillMode= → default control-group, every remaining process receives it": `btrfs-scrub@.service:1-10` is the
   whole file and sets no `KillMode=` (also no `TimeoutStopSec=`, no `SendSIGHUP=`); `systemd.kill.xml:101`
   "Defaults to control-group", `:68` "all remaining processes in the control group of this unit will be killed".
   `capture.txt:3` KillMode=control-group and `capture.txt:7` (empty `unit_dropins`) confirm nothing overrides it.
   The universal "every remaining process" does not overreach `:68`'s "all remaining processes". Holds.
4. Effective stop timeout 5 s: `capture.txt:4`
   `stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`, `capture.txt:3`
   `TimeoutStopUSec=5s`, `capture.txt:5` `dropin_owner … none`. I re-read the drop-in read-only today:
   line 1 `[Manager]`, line 2 `DefaultTimeoutStopSec=5s`; re-ran the same pacman-files grep → empty (no owner);
   `ls -d` of the unit drop-in dirs → empty. The reach of that default to every system unit without its own
   `TimeoutStopSec=` is marked `[inference]` with the right reason (`systemd-system.conf(5)` is not pinned; only
   `systemd.kill.xml` is). Mark present and correctly scoped. Holds.
5. "With -B the start does not fork into the background": true in the bytes — `scrub.c:1292-1293`
   (`case 'B': do_background = false;`), default `scrub.c:1247`, and the fork gated at `scrub.c:1512`
   (`if (do_background) {` … `fork()` at :1513). See F2 for the citation.
6. "installs its SIGINT handler on the mount's descriptor (scrub.c:1546, :439)": `scrub.c:1546`
   `scrub_handle_sigint_child(fdmnt);` sits in `cmd_scrub_start` after the background block, so the `-B` path
   reaches it; `scrub.c:439` `.sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,` inside
   `scrub_handle_sigint_child` (436-444). `fdmnt` is `btrfs_open_mnt(path)` at `scrub.c:1343` with a `< 0` bail at
   `:1344-1345`, so fd ≠ -1 and the installed handler really is `scrub_sigint_record_progress`, not `SIG_DFL`.
   Holds.
7. "…which issues BTRFS_IOC_SCRUB_CANCEL (SR9)": `scrub.c:417-424` is that handler and `scrub.c:421` is the ioctl
   inside it (no range running into the next function: 417-424 ends before `scrub_handle_sigint_parent` at 426).
   Holds.
8. "Whether the start then writes its canceled record (SR3) within the 5 s before SIGKILL is not established
   [inference: …]": marked, and the bracket states the consequence rather than a fact. Holds.
9. Optional SIGHUP: `systemd.kill.xml:86-87` documents an optional SIGHUP between KillSignal and the timeout step.
   GR3's three-step order omits it; that is decided by the pinned bytes, not guessed — the unit file (S244, whole
   file) sets no `SendSIGHUP=`, `capture.txt:7` shows no unit drop-in, and today's live
   `systemctl show btrfs-scrub@-.service -p SendSIGHUP` reads `SendSIGHUP=no`. Not a defect; recorded so the next
   reader does not have to re-derive it.
10. No universal word overreaches the quoted code: "only"/"never"/"exact" do not appear in the row outside the
    quotes; "always" occurs only inside the S248:114 quote.

## Defects (each makes the verdict `partly`; none contradicts the core)
F1 — undeclared S237 range gap (same class as the round-49 critic's defect 4, which round 50 fixed for S247/S240
but not here). S237's registered ranges at the freeze (`corpus/SOURCES.md:246`) are 67-70, 280-330, 446-535,
826-895, 1110-1125, 1186-1220, 1330-1340, 1498-1512, 1925-1945. GR3 cites `scrub.c:1512` (inside 1498-1512) but
also `scrub.c:439` (entry:165-166 and Quote at entry:192) and `scrub.c:1546` (entry:165 and Quote at entry:190),
which fall outside every range; entry:227 declares only `scrub.c:421`. The claims are still supported (the snapshot
digest pins whole files), but the gap is left undeclared. Exact replacement for the sentence at entry:227:

  `S237's (67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220, 1330-1340, 1498-1512, 1925-1945) do not list`
  `` `scrub.c:421` ``, `` `:439` `` `or` `` `:1546` ``, the handler-selection, handler-install and cancel-ioctl lines GR3 quotes and cites; the snapshot bytes are digest-pinned whole-file.`

F2 — the `-B` clause cites only the fork guard. Entry:165 reads "With `-B` the start does not fork into the
background (btrfs-progs `scrub.c:1512`)". `scrub.c:1512` shows the fork is conditional on `do_background` but not
that `-B` clears it; that assignment is `scrub.c:1292-1293`, which the row never cites (and which is itself outside
S237's ranges). Exact replacement for that clause in entry:165-166:

  "With `-B` the start does not fork into the background (`-B` clears `do_background` at btrfs-progs `scrub.c:1292-1293`,
  and `scrub.c:1512` gates the fork on it) and installs its SIGINT handler on the mount's descriptor (`scrub.c:1546`, `:439`)"

  If that replacement is taken, `scrub.c:1292-1293` must be added to the F1 declaration as well.

## The four round-49 GR2 corrections, checked against bytes (not judged admissible by me)
1. `[inference]` narrowed to btrfs-progs printing: entry:83 reads "[inference: how `btrfs scrub start` and
   `btrfs scrub status` print these returns is not pinned here; the …".
2. S240 in the `source:` line: entry:1 lists `S240` and the round-50 ioctl.c cites; entry:261 (QUALITY item 7)
   names S240.
3. `dev-replace.c:1128` quote carries its `* ` prefix: line 1128 of the pinned dev-replace.c is
   "\t\t * Scrub doing the replace isn't running so we need to do the".
4. S247/S240 range gaps declared: entry:229-236, the two `- Round 50:` Limits bullets.
Items 1-2 were reached by targeted grep of the GR2 span only, not by a full GR2 read.

## Verified but not re-derived
The pinned fetch provenance (I compared digests to the shipped `SHA256SUMS` and `FETCH.txt` tags; I did not re-fetch
from kernel.org/GitHub), the cohort's seat reports, and the counter's other legs (`corr_ok`, `quotes_ok`,
`verdicts_ok`, `seats_ok`) — those belong to other seats.

## What I did not do
No unit was started, stopped or enabled; no scrub ran; no privileged ioctl; no sysfs write. I did not re-run
`capture.sh` (I re-read the same four settings read-only instead: drop-in line 2, pacman ownership, unit drop-in
dirs, `systemctl show` incl. `SendSIGHUP=no`). I did not read GR1 or GR2 row prose and I do not judge their
admissibility. I did not check whether the S237 registration itself should be widened in SOURCES.md — F1 offers the
Limits declaration as the minimal fix, matching how round 50 handled S247/S240.
