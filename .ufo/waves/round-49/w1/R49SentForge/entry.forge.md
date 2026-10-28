source: S246 S247 S248 S249 S242 S243 S244 S237 (rows in `corpus/SOURCES.md`; S246 is Linux v7.2.11 `lib/cmdline.c`, `lib/vsprintf.c` and `lib/kstrtox.c`, S247 Linux v7.2.11 `fs/btrfs/dev-replace.c`, S248 systemd v262 `man/systemd.kill.xml`, snapshots `.ufo/waves/round-45/frozen/src/`, digests in its `SHA256SUMS`, fetch log `FETCH.txt`; S249 is the host capture `.ufo/waves/round-45/frozen/hostcap/capture.txt`, sha256 f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70; S242 and S243 are `.ufo/waves/round-44/frozen/src/scrub.c` and `sysfs.c`, S244 that directory's `btrfs-scrub@.service`, S237 `.ufo/waves/round-42/frozen/src/scrub.c`)
verified-at: 2026-10-27 (Linux tag v7.2.11, peeled commit a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea; systemd tag v262, peeled commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492; host systemd 262-1-arch, kernel 7.2.11-arch1-1; capture 2026-10-27T02:09:52Z)
recheck: on-release — re-fetch the URLs in `.ufo/waves/round-45/frozen/src/FETCH.txt` and compare `sha256sum` with its `SHA256SUMS`; re-run `bash .ufo/waves/round-45/frozen/hostcap/capture.sh <file>` (unprivileged, read-only); `python3 tools/check-scrub-grounding-r45.py --revision <REV>`

# The btrfs scrub record, round 45: grounding three round-44 inferences

Scope: the storage-integrity surface of `PROVINCE.md` (the scrub record and its census line). The round-44 entry
`corpus/knowledge/btrfs-scrub-record-r44.md` left three statements marked `[inference]` because the code that decides
them was not pinned: what `memparse` accepts when `scrub_speed_max` is written (SR8), whether a device replace runs
through the same scrub context (SR7), and what systemd sends when the packaged scrub service is stopped (SR9). This
entry pins the deciding source for each and adds what it changes for triage on this host. Nothing here writes sysfs,
starts, stops or enables a unit, runs a scrub or a replace, or calls a privileged ioctl.

## GR1

**Statement.** In Linux v7.2.11 a write to `devinfo/<devid>/scrub_speed_max` is parsed by `memparse` (SR8), which
calls `simple_strtoull` with base 0; `simple_strtoull` resolves base 0 through `_parse_integer_fixup_radix`, which
picks hexadecimal for a leading `0x` or `0X` followed by a hex digit, octal for any other leading `0`, and decimal otherwise.
After the digits, `memparse` takes at most one suffix letter, `K`, `M`, `G`, `T`, `P` or `E` in either case, each
step multiplying by a further 1024 (a 10-bit shift per step, so `K` is 1024, not 1000); the suffix counts only when
at least one digit came before it, and a shifted value that overflows becomes `ULLONG_MAX`. The sysfs store then
skips whitespace and returns `-EINVAL` unless the text ends there. So `100M` and `100m` both set 104857600 bytes per
second, `010` sets 8 and `0x10` sets 16; `10MB` (a second letter), `10 M` (a blank before the suffix) and `-1` are
rejected with `EINVAL`; and a write of a bare newline parses as 0 and is accepted, which removes the limit (0 means
no limit, SR8).

**Quote.** `S246` cmdline.c:147: "potentially suffixed with K, M, G, T, P, E."

**Quote.** `S246` cmdline.c:156: "unsigned long long ret = simple_strtoull(ptr, &endptr, 0);"

**Quote.** `S246` cmdline.c:159: "/* Consume valid suffix even in case of overflow. */"

**Quote.** `S246` cmdline.c:189: "if (shl && likely(ptr != endptr)) {"

**Quote.** `S246` cmdline.c:191: "if (unlikely(check_shl_overflow(ret, shl, &ret)))"

**Quote.** `S246` cmdline.c:192: "ret = ULLONG_MAX;"

**Quote.** `S246` vsprintf.c:86: "cp = _parse_integer_fixup_radix(startp, &base);"

**Quote.** `S246` kstrtox.c:29: "if (s[0] == '0') {"

**Quote.** `S246` kstrtox.c:30: "if (_tolower(s[1]) == 'x' && isxdigit(s[2]))"

**Quote.** `S246` kstrtox.c:33: "*base = 8;"

**Quote.** `S243` sysfs.c:2040: "limit = memparse(buf, &endptr);"

**Quote.** `S243` sysfs.c:2043: "if (*endptr != 0)"

**Host reading.** The host's one btrfs device (devid 1) reads `scrub_speed_max` 0, mode 644, owner root
(capture.txt:8), as uid 1000 with no effective capabilities (capture.txt:1): no limit is set, and this caller
[inference: by ordinary file-mode checks, which the capture does not exercise; ACLs and LSM rules are not captured]
cannot write one. Nothing was written to test the parse; the examples above follow from the quoted code.

## GR2

**Statement.** In Linux v7.2.11 a device replace copies the source device through the scrub code: both the replace
start path (the comment "the disk copy procedure reuses the scrub code") and the path that continues an interrupted
replace call `btrfs_scrub_dev` on the source device's devid with `readonly` false and `is_dev_replace` true, the last
two parameters of `btrfs_scrub_dev`. Inside `btrfs_scrub_dev`, after a filesystem-closing check that returns `-EAGAIN` first
(`btrfs_fs_closing`), the function allocates its scrub context and takes the scrub workers
(`scrub_setup_ctx`, `scrub_workers_get`), whose errors return first; then three device checks
answer: an unknown devid, or a missing device on a non-replace call, gives `-ENODEV`; a
non-writeable device on a non-replace, non-readonly call gives `-EROFS`; a device outside the
filesystem metadata, or the replace's own target device, gives `-EIO`. Only after those checks
is a call with `is_dev_replace` false refused with `-EINPROGRESS` while
`btrfs_dev_replace_is_ongoing` is true for the filesystem — which it is when the replace data is
valid (`is_valid`, dev-replace.c:1278-1279) and the state is started or suspended
(dev-replace.c:1286-1287; a replace suspended by an unmount still counts, per the comment at
dev-replace.c:1288-1297) — and any call is refused
with `-EINPROGRESS` while the device already carries a scrub context. So while a replace is ongoing, a scrub start that reaches
`btrfs_scrub_dev` for a present, writeable device that is in the filesystem metadata and is not the replace target is
refused with `EINPROGRESS` (as is a start on any device that already carries a scrub context), and no scrub is
started. While the copy runs, the replace's source device carries the scrub context the copy attached
(scrub.c:3159); by SR7, `btrfs_dev_replace_cancel` stops it with `btrfs_scrub_cancel` for a started
replace (dev-replace.c:1111) and, for a suspended replace, calls `btrfs_scrub_cancel` too
(dev-replace.c:1126-1144) although the pinned code says the replace scrub is not running in that state
(dev-replace.c:1127-1129). When the replace context is absent, the progress query returns `-ENOTCONN`
for a devid that exists (`scrub.c:3222, :3336`); an unknown devid gives `-ENODEV` (`scrub.c:3336`).
The unmount suspend path itself only moves a STARTED replace to SUSPENDED, with `time_stopped` and a
writeback flag (dev-replace.c:1171-1195, state set at :1184-1188), and does not call `btrfs_scrub_cancel`.
[inference for the ioctl and btrfs-progs side: that the scrub-start ioctl hands these returns to userspace
unchanged, and how `btrfs scrub start` and `btrfs scrub status` print them, are not pinned here].

**Quote.** `S247` dev-replace.c:700: "/* the disk copy procedure reuses the scrub code */"

**Quote.** `S247` dev-replace.c:701: "ret = btrfs_scrub_dev(fs_info, src_device->devid, 0,"

**Quote.** `S247` dev-replace.c:703: "&dev_replace->scrub_progress, false, true);"

**Quote.** `S247` dev-replace.c:1259: ""continuing dev_replace from %s (devid %llu) to target %s @%u%%","

**Quote.** `S247` dev-replace.c:1265: "ret = btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid,"

**Quote.** `S247` dev-replace.c:1268: "&dev_replace->scrub_progress, false, true);"

**Quote.** `S242` scrub.c:3081: "bool readonly, bool is_dev_replace)"
**Quote.** `S242` scrub.c:3094: "if (btrfs_fs_closing(fs_info))"
**Quote.** `S242` scrub.c:3095: "return -EAGAIN;"

**Quote.** `S242` scrub.c:3148: "(!is_dev_replace &&"

**Quote.** `S242` scrub.c:3149: "btrfs_dev_replace_is_ongoing(&fs_info->dev_replace))) {"

**Quote.** `S242` scrub.c:3147: "if (dev->scrub_ctx ||"

**Quote.** `S242` scrub.c:3153: "ret = -EINPROGRESS;"

**Quote.** `S242` scrub.c:3123: "ret = -ENODEV;"

**Quote.** `S242` scrub.c:3133: "ret = -EROFS;"

**Quote.** `S242` scrub.c:3139: "test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &dev->dev_state))) {"

**Quote.** `S242` scrub.c:3142: "ret = -EIO;"

**Quote.** `S247` dev-replace.c:1287: "case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:"

**Quote.** `S247` dev-replace.c:1235: "if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {"

**Quote.** `S243` sysfs.c:1288: "str = "device replace\n";"

**Quote.** `S243` sysfs.c:2015: "val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);"

**Quote.** `S247` dev-replace.c:1128: "Scrub doing the replace isn't running so we need to do the"

**Quote.** `S247` dev-replace.c:1143: "/* Scrub for replace must not be running in suspended state */"

**Quote.** `S247` dev-replace.c:1144: "btrfs_scrub_cancel(fs_info);"

**Quote.** `S242` scrub.c:3336: "return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;"

**Quote.** `S242` scrub.c:3109: "sctx = scrub_setup_ctx(fs_info, is_dev_replace);"

**Quote.** `S242` scrub.c:3114: "ret = scrub_workers_get(fs_info);"

**Quote.** `S242` scrub.c:3138: "if (unlikely(!test_bit(BTRFS_DEV_STATE_IN_FS_METADATA, &dev->dev_state) ||"

**Quote.** `S242` scrub.c:3222: "dev->scrub_ctx = NULL;"

**Host reading.** The filesystem lists devid 1 only (capture.txt:9) and the caller has no effective capabilities
(capture.txt:1), so the privileged progress query is out of its reach (the `CAP_SYS_ADMIN` check in the
scrub-progress ioctl, ioctl.c:3132, `-EPERM` at :3133). Replace state is still readable without
privilege through sysfs, which this capture does not record: the filesystem's `exclusive_operation` names
`device replace` while a replace holds the exclusive operation (sysfs.c:1288; the resume path takes it at
dev-replace.c:1235, and the replace ioctl takes it around the start, S240 ioctl.c:3190), and
`devinfo/<devid>/replace_target` reads 1 on the replace's target device (sysfs.c:2015).
Read on this host by wave seat C2ExecHostRecheck on 2026-10-27 (`.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md`
§3), both files are mode 444 and read `none` and `0`. The kernel rules of the row are read from source.

## GR3

**Statement.** Stopping the packaged scrub service (`systemctl stop btrfs-scrub@<instance>.service`) signals the
running `btrfs scrub start -B` in this order under systemd v262. First the unit's `KillSignal=`, which this unit sets
to SIGINT instead of the SIGTERM default; because the unit sets no `KillMode=`, the default `control-group` applies
and every remaining process in the unit's control group receives it. Right after that signal systemd sends SIGCONT.
If processes remain once `TimeoutStopSec=` has passed, the request is repeated with SIGKILL (`FinalKillSignal=`,
unless `SendSIGKILL=no`). On this host the unit's effective stop timeout is 5 s: the drop-in
`/etc/systemd/system.conf.d/10-faster-shutdown.conf` sets `DefaultTimeoutStopSec=5s` (that this default reaches every
system unit without its own `TimeoutStopSec=` is [inference]: `systemd-system.conf(5)` is not pinned here), no package
owns that drop-in, and `systemctl show` reports `KillSignal=2`, `KillMode=control-group`, `TimeoutStopUSec=5s`,
`FinalKillSignal=9` and `SendSIGKILL=yes` for `btrfs-scrub@-.service`. With `-B` the start does not fork into the
background (btrfs-progs `scrub.c:1512`) and installs its SIGINT handler on the mount's descriptor (`scrub.c:1546`,
`:439`), so SIGINT reaches that handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9). Whether the start then writes its
canceled record (SR3) within the 5 s before SIGKILL is not established [inference: a start killed before that write
leaves the record as it was last written during the run].

**Quote.** `S244` btrfs-scrub@.service:9: "KillSignal=SIGINT"

**Quote.** `S244` btrfs-scrub@.service:10: "ExecStart=/usr/bin/btrfs scrub start -B %f"

**Quote.** `S248` systemd.kill.xml:68: "<para>If set to <option>control-group</option>, all remaining processes in the control group of this"

**Quote.** `S248` systemd.kill.xml:91: "<listitem><para>the delay configured via the <varname>TimeoutStopSec=</varname> has passed"

**Quote.** `S248` systemd.kill.xml:96: "the termination request is repeated with the <constant>SIGKILL</constant> signal or the signal specified via"

**Quote.** `S248` systemd.kill.xml:101: "<para>Defaults to <option>control-group</option>.</para>"

**Quote.** `S248` systemd.kill.xml:108: "<listitem><para>Specifies which signal to use when stopping a service. This controls the signal that"

**Quote.** `S248` systemd.kill.xml:114: "<para>Note that, right after sending the signal specified in this setting, systemd will always send"

**Quote.** `S248` systemd.kill.xml:115: "<constant>SIGCONT</constant>, to ensure that even suspended tasks can be terminated cleanly.</para>"

**Quote.** `S237` scrub.c:421: "ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);"

**Quote.** `S237` scrub.c:1546: "scrub_handle_sigint_child(fdmnt);"

**Quote.** `S237` scrub.c:439: ".sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,"

**Host reading.** `systemctl show btrfs-scrub@-.service` reports `KillMode=control-group KillSignal=2
SendSIGKILL=yes TimeoutStopUSec=5s FinalKillSignal=9` (capture.txt:3); the stop default comes from
`10-faster-shutdown.conf` line 2 (capture.txt:4), a drop-in no installed package lists (capture.txt:5); systemd is
262-1-arch (capture.txt:2). No unit was started or stopped.

## How this changes OS triage

- A `scrub_speed_max` that reads a surprising value may come from the parse, not from a typo in the number: a
  leading zero is octal and `K`/`M`/`G` are powers of 1024 (GR1). Writing the limit is root's and a mutation, not a
  triage read; the census only reports it (`limited=`). A bare newline written to the file clears it.
- `EINPROGRESS` from a scrub start does not by itself say why: the kernel returns it when that device already
  carries a scrub context (a scrub, or a replace copying from it) and when a non-replace scrub is asked for while a
  replace is started or suspended (GR2). Read the unprivileged `exclusive_operation` and `replace_target` sysfs
  files first; starting or cancelling either operation stays operator-owned.
- On this host a stopped scrub service gets SIGINT and SIGCONT, and SIGKILL only if a process is still there after
  the 5 s stop timeout (GR3). A scrub record left without a `canceled` mark after a stop is therefore possible
  [inference]; read the record's timestamps before treating it as a finished run.

## Limits

- Kernel behaviour is pinned at Linux v7.2.11 source lines; the Arch kernel 7.2.11-arch1-1 patch touches no file
  under `fs/` or `lib/` [inference carried from round 43 for `fs/`; `lib/` not re-checked this round].
- GR1's examples are derived from the quoted code, not from a write on this host (the caller cannot write the
  attribute, capture.txt:1).
- GR3 pins systemd's documented behaviour (man page source at the host's major version) and the host's effective
  values, not a trace of a real stop.
- GR2's earlier device checks (`-ENODEV`, `-EROFS`, `-EIO`) and the suspended state were added at the round-45
  integration after the counted seats read `partly` (`.ufo/waves/round-45/a2w1/C2RevGR2.md`, `C2CritGR2.md`); the
  corrected row was read by the uncounted residual seats `ResRevGR2` and `ResCritGR2` (wave `a2r1`); the suspended
  case of the progress-query clause was narrowed after `ResCritGR2` finding 1 (dev-replace.c:1143-1144, scrub.c:3222,
  :3336) and no seat has read that last narrowing. The S247 row's declared ranges were widened to the
  quoted lines (1143-1144, 1235, 1276-1300). Three registrations of older rows stay as they are: S242's declared
  ranges (1365-1385, 3140-3162, 3215-3226, 3321-3337) do not list `scrub.c:3081`, 3123, 3133 or 3139; S243's
  (72-74, 2021-2049, 2113) do not list `sysfs.c:1288` or 2015; S237's do not list `scrub.c:421`. The file digests
  cover the whole snapshots (`a2w1/C2ExecQuotes.md` F1-F2, `a2r1/ResRevGR2.md`, `a2r1/ResRevGR3Triage.md` D1).
- GR2's filesystem-closing `-EAGAIN` check (scrub.c:3094-3095) and the unmount-only wording of the suspend-path
  cancellation were added at the round-47 integration after the counted round-46 residual critic read `partly`
  (`.ufo/waves/round-46/r1/V46ResCritGR2.md`); the amended row was re-read by the counted round-47 seats
  (`tools/check-scrub-admission-r47.py`, wave `w1` of `.ufo/waves/round-47/`).

## Gate status — round 45 (the depth gate FAILED; rows pending)

The frozen counter binds no counted verdict: `verdicts_ok` 0 (`SCORECARD.md` "Round 45 — measured outcome"). Of the
six counted seats of wave `a2w1`, `C2RevGR1` ended without a report or a yield (transcript ends mid-turn); the other
five wrote reports whose first lines read GR1 `holds` (critic), GR2 `partly`/`partly`, GR3 `holds`/`holds`, but none
of their yields is a bindable declared line: three are JSON objects with a `verdict` key and no `verdict_line`, two
are text whose first line is not the verdict line, and the orchestrator lost every seat output of the first 41
seats at a kernel restart (`.ufo/waves/round-45/a2w1-results.json` `output` null). Scored with the outputs recovered
verbatim from the seat transcripts, the binding still reads 0 (`.ufo/waves/round-45/a2w1/L1-recovery/`). GR1-GR3
therefore stay pending, not admitted; GR2 as corrected at the integration has been read by no counted seat.

## QUALITY check

1. Falsifiable: each statement names the quoted line that decides it; the host lines are re-runnable with
   `capture.sh`.
2. Every quote is a digest-checked snapshot line (`.ufo/waves/round-45/frozen/src/SHA256SUMS`, round-44 and round-42
   `SHA256SUMS`).
3. `[inference]` marks the two consequences the pinned code does not decide (btrfs-progs printing for GR2, the record
   after SIGKILL for GR3).
4. New entry; the round-44 entry gains an appended pointer, not an edit of its rows.
7. External claims cite S246-S248 (tier A, code and docs at pinned tags); S249 is own-work and carries host values
   only (QUALITY 86).
12. No mechanism is tagged unknown for want of a tool: the deciding source is read and pinned.
86. Each rule row cites an upstream source row; the own-work capture carries host values beside it.
14. The criteria not listed above, read for applicability: 5 (the round's rejects sit in `corpus/lessons/round-45.md`
   `## Gate`), 6 and 13 do not apply (no pacman advice, no EACCES triage); 8 (header lines present; no `[unknown]`
   kept); 9 (the one negative host claim, no package owning the drop-in, rests on the bounded `capture.sh` sweep of
   `/var/lib/pacman/local/*/files` on 2026-10-27, capture.txt:5, re-run by `a2w1/C2ExecHostRecheck.md` §4 with
   `pacman -Qo`; the `fs/`/`lib/` patch claim stays `[inference]`); 10 (the mention sweep `a2w1/C2ExecSweep.md`;
   the SKILL.md corrections land in the same integration); 11 (the LOG.md round-45 entry lands with this entry's
   integration).

## Gate status — round 46 (the depth gate FAILED again; GR1-GR3 stay pending)

Round 46 re-bound the rows through the seat-written channel (`tools/check-scrub-admission-r46.py`, frozen at
`72cc2609`): 16 counted reports, every one bound by its own first two lines. GR1: four bound `holds` on its bytes
(wave w1). GR2: `holds` 1 / `partly` 3 at `a4477049`; narrowed at `b57740c2` (setup returns, the metadata condition, the
suspended `-ENOTCONN` timing); read `partly` again by the residual critic `r1/V46ResCritGR2.md` (an earlier `-EAGAIN`
return on a closing filesystem, scrub.c:3094-3095, and more than one path that sets a replace suspended,
dev-replace.c:1186, :1224, :1238), so no two bound seats read `holds` on its current bytes. GR3: `partly` 2 / `holds` 2
at `a4477049`; narrowed at `b57740c2` (the `-B` handler install, scrub.c:1512, :1546, :439; the
`DefaultTimeoutStopSec` reach marked [inference]); read `holds` by both residual seats. The predicate needs all three
rows, so no row is admitted this round; GR2's residual finding is the next amendment, unread by any counted seat.

## Gate status — round 49 (GR1-GR3 admitted)

Round 49 re-reads GR1-GR3 with a fresh counted cohort of one wave (`w1`, 18 seats: three reviewers
and three critics per row) against the bytes above, after the seven corrections the round-48 counted
seats named were applied before the freeze (GR1: the `0X` prefix and the host-reading inference mark;
GR2: the `is_valid` gate, the cancel sentence's subject, the suspend-path range and effects, the
`ioctl.c:3132` citation and the `-ENODEV` devid case). The frozen predicate and the seat-binding
format are in `.ufo/waves/round-49/frozen/FROZEN.md`; the counter is
`tools/check-scrub-admission-r49.py`. This heading records **pending**, not admission: it says
`admitted` only after the cohort settles `holds` on the current row bytes, and the round-48 findings
are retained above as the reason the rows were not admitted then.
