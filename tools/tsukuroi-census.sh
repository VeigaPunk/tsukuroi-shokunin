#!/usr/bin/env bash
# tsukuroi-census.sh — six-plane host health census (tsukuroi-shokunin; started round 3, TSUKUROI-R3-2).
# Emits six PLANE lines: packages (incl. the root-directory metadata arm) / systemd-user /
# drivers (incl. the memory-pressure arm) / journal-boot / update-safety / oom (kill-event watch).
# v1 (round 2, TSUKUROI-R2-1) was the three-plane gate: 743 lines, md5
# 7a3d3b94ecd73fbe1a9a98e9dc88b92f (SKILL.md:235-247, LOG.md:41-49). v2 adds the
# journal/boot plane on top of that settled revision — same vocabulary, same exit map.
#
# Answers exactly one question, read-only: "what is the state of the six owned host
# planes right now, and can it be assessed at all from an unprivileged shell".
# It never installs, upgrades, removes, restarts, or writes anything (PROVINCE.md:16-17);
# its whole product is verdict + evidence + suggested operator action.
#
# Plan anchor v1: plans/round-2.plan.md:3-9 — operability axis, "an executable health census
# (tools/tsukuroi-census.sh — packages/systemd/drivers planes) emits
# TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED with a firmware-style exit map, a hermetic
# --selftest on a fixture tree, and honest verdicts on the live host".
# Anti-claim v1: plans/round-2.plan.md:8 — any plane unreadable live -> BLOCKED arm fires,
# never a fake pass.
# Plan anchor v2: plans/round-3.plan.md:3-11 — "the journal/boot plane joins the census
# (new census arms ...: boot errors, failed services history, timer drift)". The `journal`
# plane below carries those three arms, each with its own selftest cases.
# Anti-claim v2: plans/round-3.plan.md:8 — journal unreadable without elevated perms ->
# the journal arm fails closed BLOCKED; the remaining planes still report.
# Round-7 addition (lane S7-2): the drivers plane carries the memory-pressure arm —
# the round-6 OOM-event plane's detection classes (corpus/knowledge/oom-event-plane.md
# §8 C1-C6) become live evidence on the drivers line and fold into its verdict. The four
# plane ids and the rollup line keep their shape (the arm rides `drivers`), so every
# pre-round-7 consumer of the census format reads the fields it read before.
# Round-9 addition (lane S9-1): the update-safety plane — the fifth owned surface, carried by
# notes since round 1 and by `plans/round-7.plan.md` claim (a) since round 7 without an
# executable presence — becomes an executed plane: a fifth `PLANE update-safety` line and a
# fifth term in the rollup parenthetical. Both are format changes for consumers (4 -> 5 plane
# lines; `update-safety=<verdict>` appended to the rollup); the verdict vocabulary, the exit
# map and the worst-plane rule are unchanged, and the plane carries its own arm word inside
# the note exactly as the memory-pressure arm does. VERSION stays `census-v2`: it is the
# revision identity quoted by SKILL.md and LOG.md, arms and the mem plane have ridden it since
# round 7, and a bump is the note seat's call — recorded here, not silently applied.
# Round-9 addition (lane S9-2): the oom plane — the kill-event watch. `plans/round-8.plan.md`
# (claim (a)/(b)) specified the OOM/kill-event watch as the census's next plane line and the
# `PLANE oom` emitter never landed (the S8-4 round-8 record draft: claim (a)/(b) "are not in
# the landed gate at this append's write time"; `memory-arm-ver-s8.md` D3 reads the same pin).
# This lands the watch: a fifth (now sixth with S9-1's update-safety plane) `PLANE oom` line
# and a matching rollup term, carrying the memory-arm findings as census output. The
# `drivers.mem` arm is untouched (double-count precedent, round 3): the arm reads THIS boot
# at entry level and folds into the drivers verdict; this plane reads the whole retained
# window, clusters the event list by minute, and compares it against the declared waves —
# cross-boot state the arm does not keep. VERSION stays `census-v2` (revision identity
# quoted by SKILL.md/LOG.md; a bump is the note seat's call — recorded, not silently applied).
#
# Round-32 addition (C1): the ADJ-04 sibling handoff. After the six PLANE lines and before
# the rollup, the census prints one HANDOFF line per sibling-owned class it measured:
#   HANDOFF ADJ-04 mori class=kill-events value=<n> kind=dated-event state=prepared \
#     window=<oom window> source=journal-window
#   HANDOFF ADJ-04 mori class=coredumps  value=<m> kind=dated-event state=prepared \
#     scope=boot0-merged selector=SYSLOG_IDENTIFIER
# Contract: PROVINCE.md's ADJ-04 row names mori as the recipient of OS memory, journal and
# boot evidence, so the ADJ table becomes executable as a routing line. `state=prepared`
# means the census prepared a packet line — it is NOT a report, an acknowledgement or an
# acceptance, and nothing is delivered, received or agreed (mori's own PROVINCE.md reads an
# earlier tsukuroi packet the same way: "records the capture as `prepared`;
# acknowledgement/acceptance/resolution are unobserved"). tsukuroi keeps the OS finding:
# the oom and journal planes still report it, and the PLANE lines, the rollup line and the
# exit code are unchanged by the handoff — the HANDOFF lines only add a routing line.
# `value=` is the census's OWN count, never one of mori's: the dated kill events it
# text-matched and clustered over the retained journal window (the oom plane's `clusters=`)
# and the boot-0 coredump entries whose SYSLOG_IDENTIFIER is `systemd-coredump`, merged
# across the journals it read. mori counts by MESSAGE_ID per scope and never sums the
# scopes (.ufo/waves/round-32/w1/ConnSiblingOverlap.md finding 4), so these two numbers are
# not comparable and neither replaces the other. Routing is unconditional: it is decided by
# the counts the probes already measured, never by a TSUKUROI_* name or a fixture marker,
# and a cumulative counter (`vmstat oom_kill`, a `memory.events` oom_kill presence flag) is
# never a dated event, so it never reaches a HANDOFF line.
#
# Verdict vocabulary (SKILL.md:22-31): HEALTHY | DEGRADED | BLOCKED, never a scalar.
#   HEALTHY   every probe of the plane returned the pass value
#   DEGRADED  the plane answers, but carries a named defect or an unresolved unknown
#   BLOCKED   the probe itself cannot run (privilege gate / missing binary / db locked),
#             or the plane's core function is offline; never "the package is corrupt"
#
# Exit map (firmware-style, plan:5): 0 HEALTHY | 1 DEGRADED | 2 BLOCKED.
# Usage errors also exit 2. Rollup: worst plane wins (BLOCKED > DEGRADED > HEALTHY).
#
# Plane decision table as implemented (probe -> pass / degrade / block):
#
#   packages (PACMAN plane)
#     probe   pacman -Qkk over a bounded sample of `pacman -Qq` (SAMPLE_N=8, default),
#             pacman -Qm | name+version list compared against the accepted foreign baseline,
#             pacman-conf IgnorePkg IgnoreGroup, /etc/pacman.conf HoldPkg
#     pass    sample drift == 0 (rc may still be 1: backup-file diffs alone do not set rc —
#             SKILL.md:47-52, "a full sweep rc=1 is not corruption evidence"), every foreign
#             package known at its baseline version (new == 0, drift == 0, gone == 0),
#             IgnorePkg/IgnoreGroup empty
#     degrade sample drift > 0 (drift is pacman's own "N altered files" counts, which already
#             exclude `backup file:` diffs), any foreign package new / version-drifted /
#             gone vs the accepted baseline, the foreign baseline absent or unreadable
#             (never HEALTHY off a missing baseline), or IgnorePkg/IgnoreGroup non-empty
#             (holds declared, SKILL.md:45), or pins unknown
#     block   pacman binary missing, pacman -Qq fails (local db unreadable), db.lck present
#             (interrupted transaction — SKILL.md:41,45), sample probe emits `error:` or rc
#             outside {0,1}
#     note    the sample is bounded on purpose: the full sweep costs ~17 s warm (SKILL.md:107)
#             and belongs to the operator checklist, not to a gate latency budget. The sample
#             rc never decides anything on its own; the drift count does.
#             round 7 (lane S7-1): the foreign arm became a watch — `pacman -Qm` is compared
#             against the accepted baseline (default: the embedded r6 census snapshot, 16
#             rows, live `foreign=16` at round 6, rows from
#             corpus/knowledge/aur-risk-plane.md §1; TSUKUROI_FOREIGN_BASELINE may point at
#             an external name<TAB>version file instead — the register's proposed baseline
#             shape). The note reads known=new=drift=gone= plus the source, and each
#             non-empty class is named. Fail-closed both ways: a baseline row hides neither
#             a new package nor a version change, and a missing/unreadable baseline or an
#             unreadable -Qm probe never reads as a pass. This realizes the round-6
#             baseline contract (plans/round-6-record-draft.md §4) in the gate.
#             round 12 (C1): the same plane carries the root-directory metadata arm — the
#             blind spot `pacman -Qo /` exposes (rc=1, no owner; QUALITY.md #13). Evidence is
#             appended to the emitted plane note, not threaded through PKG_NOTE, so it
#             survives every early return above:
#               root_status=<ok|unavailable(...)|non-directory(...)> root_mode=<%04a|unknown>
#               root_uid= root_gid= root_euid= root_owner_write=<present|absent|unknown>
#               root_owner_search=<present|absent|unknown>
#               [root_report=<names> root_intent=not-assessed]
#               root_src=<default|override> root_dir=<absolute path|empty|relative|unsafe>
#             `stat -L` (symlinks resolved) on TSUKUROI_ROOT_DIR, default `/`. Owner-write
#             (0200) / owner-search (0100) absence is REPORT-ONLY: printed as facts, never a
#             verdict change (the parent ruling after systemd's tmpfiles.d/root.conf `z / 555`
#             showed 0555 can be a declared mode; the census does not assess intent and makes
#             no writability claim). Metadata unavailable (missing path / EACCES / dangling
#             link), a non-directory, or an empty/relative/unsafe TSUKUROI_ROOT_DIR override
#             (rejected before stat; the caller path is never echoed) -> BLOCKED, never a fake
#             pass. No universal 0755 requirement, no mount inference and no
#             "wrong/read-only" wording: 0575/0775/0751/1777/2755 with owner w+x are
#             observations, not findings; special bits ride `%04a` verbatim and are parsed as
#             octal, never decimal.
#
#   systemd (user scope only — PROVINCE.md:8-9 owns `systemctl --user`; the system-scope
#   row lives in SKILL.md:42 and is out of this gate's scope)
#     probe   systemctl --user is-system-running; list-units --state=failed;
#             list-unit-files --type=timer --state=enabled; show <timer> -p Result for each
#             enabled timer (bounded by TIMER_SCAN_MAX)
#     pass    state == running, failed == 0, every scanned timer Result == success
#     degrade failed > 0, any timer Result != success, any Result unreadable (unresolved
#             unknown), or state in {degraded,starting,stopping}
#     block   systemctl missing, the --user bus is unreachable (output is not a state word),
#             a list probe fails, or state in {offline,maintenance} (core function offline)
#     note    deliberate refinement vs SKILL.md:42, which lists `degraded` under BLOCKED:
#             SKILL.md:31 glosses BLOCKED as "cannot be assessed read-only"; a degraded scope
#             is fully assessed by the failed-units probe, so this gate reports it as
#             DEGRADED with the failed set named. Recorded here, not silently applied.
#
#   drivers (nvidia / kernel ring plane)
#     probe   kernel error ring — `dmesg --level=err,crit,alert,emerg` preferred, else
#             `journalctl -k -b -p err -o json` (entry-level counts; SKILL.md:220 errata:
#             line counts are traps, use entries). Then nvidia presence: PCI vendor 0x10de
#             inventory (/sys/bus/pci/devices), `nvidia-smi --query-gpu=name,driver_version`,
#             `lsmod` nvidia rows, /dev/nvidia* nodes
#     pass    kerr == 0 with a non-empty ring, and nvidia either present-and-answering
#             (smi ok + module loaded + nodes exist) or absent from PCI inventory
#     degrade kerr > 0, classes counted at entry level (oom / io / gpu / other); the plane's
#             noise floor is [unknown], so any kernel error entry is a named unresolved item
#     block   both rings unusable, ring empty (cannot tell "clean" from "no data"),
#             nvidia hardware in PCI but core function offline (smi not answering, module not
#             loaded, or no /dev/nvidia* node), or PCI inventory unreadable with no other
#             positive evidence
#     note    dmesg is restricted on the measured host (`dmesg_restrict=1`, SKILL.md:158-160);
#             the ring source actually used is printed as `ring=` in the plane line.
#
#   drivers.mem (memory-pressure arm — rides the drivers plane's line and verdict;
#   round 7, lane S7-2, detection-only). Vocabulary: the round-6 OOM-event plane's
#   detection contract (corpus/knowledge/oom-event-plane.md §8, classes C1-C6):
#             C1 kernel OOM dump entries (`journalctl -k -b -p err -o json` + the OOM
#             regex — the same source and semantics as the ring's `oom=` class),
#             C2 systemd OOM attribution (`kernel OOM killer killed some processes`,
#             emitted at PRIORITY=5, i.e. the only attribution for a session-wide
#             SIGKILL class that leaves no kernel record),
#             C3 SIGKILL/teardown class (`status=9/KILL|Failed with result
#             '(signal|oom-kill)'`),
#             C4 cgroup `memory.events[.local]` oom_kill PRESENCE FLAGS (§4.2: two
#             documented kill waves left the surviving counter at 1 — a flag per
#             cgroup, never an event count),
#             C5 swap-pressure anchors (swap.events `fail`, swap.peak vs meminfo
#             SwapTotal, `memory.stat` pswpin/pswpout, `sock_throttled`),
#             C6 live shape (PSI `avg300`/`total`, MemAvailable, Shmem), plus the
#             guards shape (§4.5: memory.max/high, memory.oom.group).
#     pass    every signal readable and every class zero
#     degrade any class > 0 (C1/C2/C3 entries, any oom_kill flag, swap fail > 0), or
#             any required signal unreadable — named in `unknown=[...]`, never silent
#     block   cgroup sweep empty AND all three journal probes unusable: no class can
#             be read at all (fail closed, same stance as the ring arms)
#     note    probe cost ≈0.3 s live (190 cgroup files + 3 bounded `--grep` reads;
#             whole-gate live run 1.11 s, inside the recorded 0.69–1.75 s band).
#             `journalctl --grep` exits 1 on no-match (measured 2026-10-14) — rc 1 is
#             "0 entries", any other non-zero rc is "unreadable". Page-cache-inclusive
#             `memory.peak` is not a pressure reading (§4.4), so the arm reports the
#             swap plane instead, and `memory.events` counters are never read as meters.
#             First live run (2026-10-14T18:33:02Z, drivers line verbatim): mem=[DEGRADED]
#             C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2
#             [user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922849
#             C5_swap_peak_pct=99% C5_pswp=72117839/93795670 C5_sock_throttled=67558;
#             C6_psi_full_avg300=0.00 C6_psi_full_total_us=68342659 C6_avail_kb=19214152
#             C6_shmem_kb=6907048; guards=max/max oom.group=0 — the round-6 OOM plane's
#             state re-measured (2 kill waves, swap plane at 99%), not quoted: live
#             counters drift, re-run before citing. The arm carries no cross-run delta
#             (the census keeps no state); "new vs baseline" is the class-presence
#             reading plus the note's per-round recheck ledger.
#
#   oom (kill-event watch — the retained window, new-vs-baseline; round 9, lane S9-2,
#   detection-only, read-only; the round-8 plan's specified-not-landed claim (a))
#     probe   window: `journalctl --list-boots` — boot count and the date bounds of the
#             retained journal. C1: kernel OOM family over the whole window, server-side
#             `--grep`, entry-level count with `-- Boot <id> --` separators counted out (a
#             whole-journal grep prints one per scanned boot — the counting trap).
#             C2/C3: the event list over the window (attribution messages; kill9/teardown
#             class) clustered by minute — a bare count is a trap (event A's kernel family is
#             3 lines, one event). ledger: `/proc/vmstat oom_kill`, the kernel's own kill
#             counter (F1's discriminator), shape-only.
#     pass    window measured (>=1 boot), every scan readable, every observed cluster known
#             to the declared baseline, no declared wave lost inside the window, baseline
#             readable, ledger readable
#     degrade a cluster not in the baseline (named `new`), a declared wave inside the window
#             that is not observed (named `missing` — unexplained loss of declared evidence),
#             an absent/unreadable baseline (never HEALTHY off a missing baseline), or an
#             unreadable ledger (named `unknown`)
#     block   `journalctl --list-boots` unreadable or 0 boots (an empty scan is only a pass
#             when the window itself is measured), or any window scan rc outside {0,1} (the
#             watch cannot be assessed at all — fails closed, same stance as the other arms)
#     note    baseline = the declared waves as an embedded snapshot (`R8_OOM_BASELINE`, rows
#             `<date> <HH:MM> <id> <class> <note>`; the two measured waves A/B from the
#             round-6 note re-measured by round 8, `kill-event-deep-r8.md` §1 F1-F3), external
#             file via `TSUKUROI_OOM_BASELINE` — the round-7 foreign-watch mechanism, one
#             mechanism two readers; `out_of_window=N` is retention loss, a coverage fact,
#             never a health fact. Reading rules printed, never adjudicated (round-8
#             findings): counters are presence flags, never event counts; `memory.peak` /
#             `swap.peak` are lifetime maxima and are not datable to a kill (F5); `Started
#             app-*.scope` counts launches, never live units (F6); the 13:10:59 slice notice
#             carries both readings (late report of the 23:44:30 kill | session-SIGKILL
#             attribution) and both stay carried (H1-H3). First live run of the landed
#             revision is quoted in the round record, never here from memory.
#   journal (this-boot triage — SKILL.md:43 row; all probes read-only)
#     probe   arm 1 boot record: `journalctl --list-boots --no-pager` (index-0 line must exist)
#             arm 2 boot target: `systemctl is-active $BOOT_TARGET` (default graphical.target)
#             arm 3 boot errors: `journalctl -b -p err -o json --no-pager` — ENTRY count, and
#             disjoint classes on the JSON lines (coredump | kernel | other). Line counts are
#             traps (60 941 lines vs 238 entries, systemd-user-plane.md:104-116); only `-o json`
#             lines (= entries) are ever counted.
#             arm 4 failed services history: journal-derived from the same err stream, so units
#             that failed earlier this boot and were reset since are still named — the systemd
#             plane reports only the current failed set.
#             arm 5 timer drift: for each enabled user timer, `show <t> -p ActiveState` (bounded
#             TIMER_SCAN_MAX); an enabled timer that is not `active` will not fire as configured.
#             Deliberate: avoids brittle relative-time parsing of `list-timers`, and reuses the
#             systemd plane's timer-loop shape.
#     pass    index-0 boot line present, target == active, err entries == 0 with a non-empty
#             journal this boot, failedhist == 0, every enabled timer armed
#     degrade err entries > 0 (noise floor [unknown]; classes named — same stance as drivers),
#             failedhist > 0, timer drift > 0, or timer ActiveState unreadable (unresolved
#             unknown — mirrors the systemd plane's unreadable-Result semantics)
#     block   journalctl missing or --list-boots unreadable (fails closed — anti-claim v2,
#             plans/round-3.plan.md:8), no index-0 boot line, boot target not `active`
#             (SKILL.md:43 "no boot reaches graphical.target"), err stream unreadable, or the
#             journal is empty this boot (clean vs no-data cannot be told apart)
#     note    kernel entries also appear in the drivers plane's ring; the journal plane's
#             distinct value is the non-kernel classes (coredumps, service messages), the boot
#             record/target, and the armed-state of user timers. `coredumpctl` is deliberately
#             NOT probed: table parsing is a measured trap (systemd-user-plane.md:169) and
#             `--json` would add a jq dependency; the `systemd-coredump` entry class IS the
#             storm signal. First full-gate live run of v2 (2026-10-14T14:51:17Z): boots=13
#             current=yes target=graphical.target:active err=251 (coredump=211 kernel=38
#             other=2) failedhist=0 timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 —
#             snapshot only (counts drift with the live coredump storm: 249 at 14:48, 251 at
#             14:51); re-run, never quote as now.
#
#   update-safety (the fifth plane — round 9, lane S9-1; finished from the measured model, not
#   re-designed: claim (a) `plans/round-7.plan.md:53-98`, arm vocabulary and composition
#   `SKILL.md:358-368`, the r2 §7 decision table `update-safety-note.md:334-381`, the class ×
#   update-path reading `update-safety-v2.md` / `-v3.md`. Detection and recommendation only:
#   PROVINCE.md:16-17 — nothing here refreshes, downloads, installs or writes.)
#     probe   channel reading: repo `*.db` under $PACMAN_DB/sync — births (`stat -c %W`) and
#             content stamps (`stat -c %Y` = the db file's mtime, upstream's own file stamp
#             preserved at download). `offline.db` is NOT a channel (it is the offline-exile
#             preservation archive; its 2026-07-20 stamp would drag an age it does not own) —
#             it is reported separately.
#             candidates: `pacman -Qu` UNPIPED (rc 1 + 0 lines = empty; rc 0 + n>0 lines =
#             candidates; any other shape = unreadable, never INERT — the pipeline-rc trap)
#             cross-checked against the plan verb `pacman -Sup --print-format '%r/%n %v'`;
#             disagreement keeps the larger count (fail closed).
#             third reading: the repo-side version join — `pacman -Sl`, first occurrence per
#             name = pacman's own repo order (the r2 note's last-wins `expac` trap, `:403-411`,
#             is why first-wins), `vercmp` for direction; `expac -S` cross-checks it when
#             present, and `expac=absent` / `join=unavailable` are printed — never a silent pass.
#             fold: the SAME-process packages-arm reading (`pacman -Qm` vs the accepted
#             baseline; never re-probed here) joined against the r6 register's rows
#             (`aur-risk-plane.md` §1: 14 offline-exile / 2 aur-local).
#             log: bounded tail (TSUKUROI_LOG_TAIL_N) for the last command class and the last
#             refresh-class command inside that window (`none-in-window` is a statement about
#             the window, never about the host).
#             trap: `pacman -Suu --print-format` (verb-level DO-NOT row).
#     pass    INERT — both candidate probes read empty AND the channel reading is present and
#             not stale. `PASS` is never emitted: an empty candidate set is INERT by the r2
#             table's own row 2, so the word is carried in the vocabulary only.
#     degrade REQUIRES-PREP (candidates > 0, or a `behind` row from the join) and
#             UNKNOWN-UPSTREAM (the oldest channel content stamp older than
#             TSUKUROI_CHANNEL_MAX_AGE_D, default 7 d — the r2 table's row 1 arm, "empty proves
#             nothing newer than the snapshot" — or a stamp whose age cannot be measured); plus
#             the fold's rows: a `new` foreign arrival prints `unknown-provenance=[…]` and an
#             absent/unreadable baseline prints `classes=unavailable` — both degrade, never a pass.
#     block   pacman missing, db.lck present, `-Qu` or `-Sup` unreadable, or no repo db in
#             `sync/` — an empty candidate set over no channel cannot be told apart from an
#             up-to-date one (same fail-closed stance as the memory arm)
#     note    mapping to the gate verdict is RECORDED here, not silently applied: BLOCKED ->
#             BLOCKED; UNKNOWN-UPSTREAM / REQUIRES-PREP -> DEGRADED; INERT -> HEALTHY; the fold
#             can only worsen (`worse`), never lift a BLOCKED probe. The `-Suu` trap row, the
#             `offline.db` row and the log rows are printed and verdict-neutral (DO-NOT stays
#             verb-level note content, `plans/round-7.plan.md:95-97`). Every arm word carries
#             its firing rows so a non-author can re-derive it (r2 note `:338-339`).
#             Live reading, executed 2026-10-14T20:07Z and 20:08Z (two runs, byte-identical,
#             rc=1; the line is quoted from the run, not from a plan): `status=UNKNOWN-UPSTREAM;
#             pending=none; qu=rc=1/0; sup=0; join=equal=1171 behind=0 ahead=1 src=sl+expac;
#             expac=agree; chan=dbs=4 fetch=3d stamp=36d; offline.db=present(stamp=85d birth=10d);
#             log=cmd=-S@2026-10-13T16:37:58-0300; refresh=none-in-window(last 300 lines);
#             classes=offline-exile:14,aur-local:2; trap=-Suu:1[omarchy/1password-beta
#             8.12.42_32.BETA-1]` -> the plane is DEGRADED: 36 d of channel lag is the named
#             unknown, the candidate set is empty and the `-Suu` trap row is printed without
#             raising the verdict. Counts drift, re-run; the join reproduces the v3 note's
#             measured `equal=1171 behind=0 ahead=1` the same day.
#             Cost: the plane's probes measure `-Qu` 0.11 s, `-Sup` 0.29 s, `-Suu` 0.29 s,
#             `-Q` 0.01 s, `-Sl` 0.11 s, `expac -S` 0.11 s (single pass each, 2026-10-14) and the
#             whole-gate live run is 2.24–2.25 s over two runs — the recorded 0.69–1.75 s band
#             belonged to the four-plane gate and moved with this plane; recorded here rather
#             than trimmed by dropping a probe.
#
# Round-35 addition (C1): the pacnew/pacsave drift arm. PROVINCE.md Core owns `.pacnew` /
# `.pacsave` drift ("Pair pacman-log history with current readable filesystem findings; report
# skipped unreadable paths"); until round 35 only corpus/knowledge/pacnew-plane.md said how to
# read it. The arm prints ONE line after the HANDOFF lines and before the rollup:
#   DRIFT pacnew-plane pacnew=N pacsave=N pacorig=N unreadable=N log_pacnew=N log_pacsave=N
#     unlogged=N gone=N log=ok|unreadable
# pacnew/pacsave/pacorig: non-directory entries under TSUKUROI_ETC_DIR (default /etc) named
# `*.pacnew`, `*.pacsave` or `*.pacsave.[0-9]*`, `*.pacorig` (pacdiff 1.13.1's find names, S193,
# minus directories; symlinks are counted and never followed). unreadable: directories the
# sweep could not read (find's "Permission denied"; uid-dependent: root sees fewer).
# log_pacnew/log_pacsave: pacman's own warnings `[..] [ALPM] warning: F installed as F.pacnew`
# and `F saved as F.pacsave` (libalpm add.c / remove.c at 7.1.0, S191/S192) with F under /etc/.
# unlogged: counted entries named by no such warning (a `.pacsave.N` is never logged: pacman
# renames it without a log line, S192 shift_pacsave). gone: distinct logged targets that are no
# counted entry and lie beneath no unreadable directory. Names only — file contents are never
# read (ADJ-02). The line is verdict-neutral: no PLANE text, rollup term or exit code changes.
# Live mode creates no files (two find sweeps into shell variables, no mktemp).
#
# Round-38 addition (C1): the storage-integrity arm. corpus/README.md (round 26) kept storage
# integrity as Frontier "until a read-only census arm reads it"; this arm reads it. It prints ONE
# line after the DRIFT line and before the rollup:
#   STORAGE btrfs-device-stats state=HEALTHY|DEGRADED|BLOCKED filesystems=N devices=N nonzero=N
#     [detail=<fsid8>:<devid>:<key>=<value>|<fsid8>:<devid>:<reason>,...]
# filesystems: entries under TSUKUROI_BTRFS_SYSFS (default /sys/fs/btrfs) named as a btrfs fsid
# (lowercase UUID); `features` and other names are ignored. devices: entries under each
# filesystem's devinfo/. Each device's error_stats must carry exactly the five counters
# write_errs, read_errs, flush_errs, corruption_errs, generation_errs (Linux fs/btrfs/sysfs.c,
# S133; storage-health-r26.md SH1) as non-negative integers, each once; nonzero counts the
# (device, counter) pairs above zero. state: BLOCKED when a filesystem has no devinfo entry or
# an error_stats file is unreadable or malformed; else DEGRADED when nonzero > 0 (a stored
# lifetime total, never a dated event — SH2; date it from error-level kernel lines); else
# HEALTHY. An absent TSUKUROI_BTRFS_SYSFS means no btrfs filesystem is mounted: HEALTHY 0/0/0
# (round 38; superseded round 39, R38-ABSENT-ROOT): an absent root, or one holding no fsid entry,
# reads HEALTHY 0/0/0 only when the mount table (TSUKUROI_PROC_MOUNTS, default /proc/self/mounts)
# lists no btrfs mount; with a btrfs mount listed it is BLOCKED detail=mounts:btrfs-without-sysfs
# (a namespace or mount that hides /sys/fs/btrfs must not read as a clean disk), and a mount table
# that is unreadable, not a regular file (a FIFO would block) or empty is BLOCKED
# detail=mounts:unreadable. A root with fsid entries never reads the table.
# No privilege is needed (sysfs 0444), counters are never reset (`btrfs device stats -z` is
# operator-owned), NVMe SMART (SH5/SH6) is not read. The line is verdict-neutral: no PLANE
# text, rollup term or exit code changes (frozen consumers pin six PLANE lines, e.g.
# tools/score-census-handoff-r32.py). Live mode reads sysfs (and, since round 39, the mount table
# when the sysfs root holds no fsid) and creates no files.
# Round-38 wave-1 hardening (same commit series, before the measured revision): a devinfo entry
# whose name is not a decimal devid is BLOCKED as `<fsid8>:?:bad-devid` and its name is never
# echoed (a newline in a fixture name forged extra census lines, C1SentGrammar); an existing root
# the reader cannot list is BLOCKED `root:unreadable` instead of a silent 0/0/0 (C1RevSharedState).
# Known limit at round 38 (C1CritAbsentRoot): an ABSENT root read HEALTHY 0/0/0, so a namespace that
# hid /sys/fs/btrfs while btrfs was mounted gave a false all-clear. Repaired in round 39 by the
# mount-table cross-check described above (R38-ABSENT-ROOT); the round-38 v1 counter's F06 fixture
# encodes the old rule and reads BLOCKED at round-39 revisions by construction.
#
# Round-44 addition (C1): the scrub-record arm. PROVINCE.md kept the scrub record Frontier "until a
# read-only census arm reads it" (round 38 section, round-42/43 notes); this arm reads the part an
# unprivileged reader can see. It prints ONE line after the STORAGE line and before the rollup:
#   SCRUB btrfs-scrub-record state=NONE|RECORDED|BLOCKED dir=absent|present|unreadable records=N
#     tmp=N sockets=N unreadable=N orphan=N limited=N timers=N [detail=<reason>,...,<fsid8>:<devid>:speed_max=<v>,...]
# dir: TSUKUROI_SCRUB_DIR (default /var/lib/btrfs, btrfs-progs' SCRUB_DATA_FILE directory, S237:67-68).
# Under it only names btrfs-progs writes are read, by name and stat, never by content: records
# `scrub.status.<fsid>` (regular files), tmp `scrub.status.<fsid>_tmp` (a failed or killed update,
# SR1), sockets `scrub.progress.<fsid>` (a `btrfs scrub start` progress socket; a killed start can
# leave one, so it is a reading, not the running state, which needs CAP_SYS_ADMIN — SR6). <fsid> is a
# lowercase UUID; other names are ignored and no name is ever echoed (QUALITY 84). unreadable: records
# and tmp files the caller cannot read (a root scrub writes mode-0600 files). orphan: records whose
# fsid has no entry under TSUKUROI_BTRFS_SYSFS (a filesystem not mounted now). limited: devices whose
# sysfs devinfo/<devid>/scrub_speed_max reads a nonzero decimal (bytes/s; 0 = no limit), listed in
# detail as <fsid8>:<devid>:speed_max=<v>. timers: entries `btrfs-scrub@<instance>.timer` under
# TSUKUROI_TIMER_WANTS (default /etc/systemd/system/timers.target.wants: what `systemctl enable`
# links; the bare template name is not an instance and is not counted). state: BLOCKED when a
# reading is unavailable — an existing dir, sysfs root or wants dir the caller cannot list
# (dir:unreadable, sysfs:unreadable, timers:unreadable), a record, tmp or progress name of the wrong
# file type (record:not-regular, tmp:not-regular, progress:not-socket), a device whose
# scrub_speed_max is unreadable or not one decimal line (<fsid8>:<devid>:speed-unreadable,
# NONE. Globs run under LC_ALL=C, so the detail order is bytewise. Known limit: an absent sysfs root
# with no record reads limited=0; the STORAGE line's mount-table guard is what flags a hidden sysfs.
# No privilege, no ioctl, no `btrfs` or `systemctl` call; the line is verdict-neutral (no PLANE
# text, rollup term or exit code changes) and live mode creates no files.
#
# Read-only guarantee: no probe writes; the gate creates no files at all in live mode
# (selftest writes only under a mktemp dir named ${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX).
# Secrets are never read: only public package/system unit/driver/journal state is queried.
#
# Hermetic selftest: `--selftest` builds a /tmp fixture tree with a dispatcher stub for
# every probe command and re-invokes this script against it via env overrides. Each case
# asserts exit code + final verdict + one or more evidence substrings, and asserts the
# fixture tree is byte-unchanged after the run (zero mutation). Every probe command and
# every host path read in live mode has an override below, so the selftest touches no
# host state:
#   TSUKUROI_PACMAN TSUKUROI_PACMAN_CONF TSUKUROI_PACMAN_CONF_FILE TSUKUROI_PACMAN_DB
#   TSUKUROI_ROOT_DIR (root-directory metadata arm; default / — the selftest points it at a
#   0755 fixture directory, never at the live root)
#   TSUKUROI_FOREIGN_BASELINE (external baseline path; empty/unset = embedded r6 snapshot)
#   TSUKUROI_SYSTEMCTL TSUKUROI_DMESG TSUKUROI_JOURNALCTL TSUKUROI_NVIDIA_SMI TSUKUROI_LSMOD
#   TSUKUROI_PCI_SYSFS TSUKUROI_DEV_DIR TSUKUROI_HOSTNAME_FILE TSUKUROI_DMESG_RESTRICT_FILE
#   TSUKUROI_BOOT_TARGET TSUKUROI_SAMPLE_N TSUKUROI_TIMER_SCAN_MAX TSUKUROI_FIXTURE (selftest only)
#   TSUKUROI_CGROUP_ROOT TSUKUROI_MEM_SLICE TSUKUROI_PRESSURE_FILE TSUKUROI_MEMINFO_FILE
#   (the memory-pressure arm's paths; the arm itself has no other host read)
#   TSUKUROI_VMSTAT_FILE TSUKUROI_OOM_BASELINE (the oom watch: kernel-kill ledger path;
#   external declared-wave baseline; empty/unset = the embedded r8 snapshot)
#   TSUKUROI_PACMAN_LOG TSUKUROI_OFFLINE_DB TSUKUROI_EXPAC TSUKUROI_VERCMP
#   TSUKUROI_ETC_DIR (round 35: the pacnew/pacsave drift arm's tree; default /etc)
#   TSUKUROI_BTRFS_SYSFS (round 38: the storage-integrity arm's sysfs root; default /sys/fs/btrfs)
#   TSUKUROI_PROC_MOUNTS (round 39: the storage arm's mount table; default /proc/self/mounts)
#   TSUKUROI_SCRUB_DIR TSUKUROI_TIMER_WANTS (round 44: the scrub-record arm's record directory and
#   timers.target.wants directory; defaults /var/lib/btrfs, /etc/systemd/system/timers.target.wants)
#   TSUKUROI_CHANNEL_MAX_AGE_D TSUKUROI_LOG_TAIL_N (the update-safety plane's seams). The
#   channel stamp is the fixture db file's own mtime — settable with `touch -d` — so the
#   stale-channel case is executed against a real probe, not asserted vacuous.
#
# Sources: PROVINCE.md:5-12,16-18 · SKILL.md:20-31 (vocabulary), :33-45 (decision table incl.
# the journal/boot row), :47-83 (Qkk benign classes), :85-135 (update-safety checklist),
# :137-172 (boundary rule) · AGENTS.md:3-5 · corpus/QUALITY.md:1-5 ·
# corpus/knowledge/package-state-plane.md, systemd-user-plane.md (§5-6 err classes + coredump
# census, §8 method traps), driver-firmware-plane.md · plans/round-2.plan.md:3-9 ·
# plans/round-3.plan.md:3-11 · plans/round-6-record-draft.md §4 (baseline contract) ·
# corpus/knowledge/aur-risk-plane.md §1 (the 16 baseline rows and their classes) ·
# plans/round-7.plan.md:53-98 (the unlanded claim (a) this plane finishes) ·
# corpus/knowledge/update-safety-note.md:334-381 (r2 §7 arms + the 36 d content-stamp row) ·
# update-safety-v2.md / update-safety-v3.md (class × update-path, the `-Suu` measured trap).
set -euo pipefail
umask 077

VERSION='census-v2'
SELF=${BASH_SOURCE[0]:-}  # round 46 (C1): empty when the script is read from stdin (--identity: unverifiable)

# ---- probe surface (every command and every host path is override-able) ------
PACMAN=${TSUKUROI_PACMAN:-pacman}
PACMAN_CONF=${TSUKUROI_PACMAN_CONF:-pacman-conf}
PACMAN_CONF_FILE=${TSUKUROI_PACMAN_CONF_FILE:-/etc/pacman.conf}
PACMAN_DB=${TSUKUROI_PACMAN_DB:-/var/lib/pacman}
# Root-directory metadata arm (round 12, C1): `/` is owned by no package (`pacman -Qo /`
# rc=1), so -Qkk cannot judge it (QUALITY.md #13). `${VAR-default}` (not `:-`) is deliberate:
# an explicitly empty TSUKUROI_ROOT_DIR must read as unavailable, never silently become the
# live `/`. Overridable so the hermetic selftest never reads the live root.
ROOT_SRC=default
if [ "${TSUKUROI_ROOT_DIR+set}" = set ]; then ROOT_SRC=override; fi
ROOT_DIR=${TSUKUROI_ROOT_DIR-/}
SYSTEMCTL=${TSUKUROI_SYSTEMCTL:-systemctl}
DMESG=${TSUKUROI_DMESG:-dmesg}
JOURNALCTL=${TSUKUROI_JOURNALCTL:-journalctl}
NVIDIA_SMI=${TSUKUROI_NVIDIA_SMI:-nvidia-smi}
LSMOD=${TSUKUROI_LSMOD:-lsmod}
PCI_SYSFS=${TSUKUROI_PCI_SYSFS:-/sys/bus/pci/devices}
DEV_DIR=${TSUKUROI_DEV_DIR:-/dev}
HOSTNAME_FILE=${TSUKUROI_HOSTNAME_FILE:-/proc/sys/kernel/hostname}
DMESG_RESTRICT_FILE=${TSUKUROI_DMESG_RESTRICT_FILE:-/proc/sys/kernel/dmesg_restrict}
BOOT_TARGET=${TSUKUROI_BOOT_TARGET:-graphical.target}
SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}
TIMER_SCAN_MAX=${TSUKUROI_TIMER_SCAN_MAX:-12}
CGROUP_ROOT=${TSUKUROI_CGROUP_ROOT:-/sys/fs/cgroup}
MEM_SLICE=${TSUKUROI_MEM_SLICE:-user.slice/user-1000.slice}
PRESSURE_FILE=${TSUKUROI_PRESSURE_FILE:-/proc/pressure/memory}
MEMINFO_FILE=${TSUKUROI_MEMINFO_FILE:-/proc/meminfo}
VMSTAT_FILE=${TSUKUROI_VMSTAT_FILE:-/proc/vmstat}
OOM_BASELINE=${TSUKUROI_OOM_BASELINE:-}
FOREIGN_BASELINE=${TSUKUROI_FOREIGN_BASELINE:-}
PACMAN_LOG=${TSUKUROI_PACMAN_LOG:-/var/log/pacman.log}
ETC_DIR=${TSUKUROI_ETC_DIR:-/etc}
BTRFS_SYSFS=${TSUKUROI_BTRFS_SYSFS:-/sys/fs/btrfs}
PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}
SCRUB_DIR=${TSUKUROI_SCRUB_DIR:-/var/lib/btrfs}
TIMER_WANTS=${TSUKUROI_TIMER_WANTS:-/etc/systemd/system/timers.target.wants}
OFFLINE_DB=${TSUKUROI_OFFLINE_DB:-$PACMAN_DB/sync/offline.db}
EXPAC=${TSUKUROI_EXPAC:-expac}
VERCMP=${TSUKUROI_VERCMP:-vercmp}
CHANNEL_MAX_AGE_D=${TSUKUROI_CHANNEL_MAX_AGE_D:-7}
LOG_TAIL_N=${TSUKUROI_LOG_TAIL_N:-300}
CHANNEL_ARCHIVE='offline.db'   # the offline-exile preservation archive, not a channel
EXPAC_FMT=$'%n\t%v'

# Accepted foreign baseline — the round-6 census snapshot (live `foreign=16` at round 6,
# 2026-10-14; re-measured live before landing this arm and byte-identical, so the snapshot
# still equals the host's set). Source of the rows: corpus/knowledge/aur-risk-plane.md §1
# (14 offline-exile + 2 AUR-local, `name version` per row). The register owns the rows;
# this gate owns the comparison. TSUKUROI_FOREIGN_BASELINE may point at an external
# name-version file (the register's proposed corpus/knowledge/foreign-aur-baseline.tsv
# shape); unset or empty = this snapshot. Rows are never re-guessed here: a class claim
# needs the register's measured trail, and the selftest hit-case pins this constant's
# 16-row content so an edit to it cannot pass silently.
R6_FOREIGN_BASELINE='android-apktool-bin 3.0.3-1
elephant 2.21.0-1
elephant-bluetooth 2.21.0-1
elephant-calc 2.21.0-1
elephant-clipboard 2.21.0-1
elephant-desktopapplications 2.21.0-1
elephant-files 2.21.0-1
elephant-menus 2.21.0-1
elephant-providerlist 2.21.0-1
elephant-runner 2.21.0-1
elephant-symbols 2.21.0-1
elephant-todo 2.21.0-1
elephant-unicode 2.21.0-1
elephant-websearch 2.21.0-1
obsidian-cli-inspector 1.0.3-1
omarchy-walker 1.0.0-2'

# Declared OOM/kill-event waves — the round-8 embedded-snapshot baseline (the round-7
# foreign-watch mechanism, one mechanism two readers). Rows `<date> <HH:MM> <id> <class>
# <note>`, from the round-6 note's two waves re-measured by round 8 (`kill-event-deep-r8.md`
# §1 F1-F3): A = 2026-10-13 23:44 kernel OOM (victim python3, pid 1732581); B =
# 2026-10-14 13:10 session-teardown SIGKILL class, no kernel record (F1). The operator/register
# owns the rows (append-only); this gate owns the comparison and never auto-extends its own
# baseline. TSUKUROI_OOM_BASELINE may point at an external file of the same row shape;
# unset or empty = this snapshot. The selftest hit-case pins this constant's two rows so an
# edit to it cannot pass silently.
R8_OOM_BASELINE='2026-10-13 23:44 A kernel+attrib+kill9 event A: global OOM, victim python3 (pid 1732581)
2026-10-14 13:10 B attrib+kill9 event B: session teardown SIGKILL class, no kernel record (F1)'

CLASS_OOM='Out of memory|oom-kill|oom_reaper'
CLASS_IO='I/O error|Buffer I/O error|critical medium error|critical target error'
CLASS_GPU='NVRM|nvidia|NVIDIA|GSP|drm'
CLASS_FAILED='Failed to |entered failed state|Failed with result'
CLASS_OOM_SYS='kernel OOM killer killed some processes'
CLASS_SIGKILL="status=9/KILL|Failed with result '(signal|oom-kill)'"

# The r6 register's per-package classes (corpus/knowledge/aur-risk-plane.md §1: channel B
# AUR-local = 2 rows, channel A offline-exile = 14 rows). The register owns the rows; this
# gate owns the join against the SAME-process `pacman -Qm` reading. Rows are never re-guessed
# here (the note's probe order is the register's), and the selftest pins this constant's
# 16-row content so an edit to it cannot pass silently — same stance as R6_FOREIGN_BASELINE.
R6_FOREIGN_CLASSES='android-apktool-bin aur-local
obsidian-cli-inspector aur-local
elephant offline-exile
elephant-bluetooth offline-exile
elephant-calc offline-exile
elephant-clipboard offline-exile
elephant-desktopapplications offline-exile
elephant-files offline-exile
elephant-menus offline-exile
elephant-providerlist offline-exile
elephant-runner offline-exile
elephant-symbols offline-exile
elephant-todo offline-exile
elephant-unicode offline-exile
elephant-websearch offline-exile
omarchy-walker offline-exile'

# ---- shared state ------------------------------------------------------------
PKG_V=BLOCKED PKG_NOTE='probe not run'
SYS_V=BLOCKED SYS_NOTE='probe not run'
DRV_V=BLOCKED DRV_NOTE='probe not run'
MEM_V=BLOCKED MEM_NOTE='arm not run'
JRN_V=BLOCKED JRN_NOTE='probe not run'
OOM_V=BLOCKED OOM_NOTE='probe not run'
UPD_V=BLOCKED UPD_NOTE='probe not run'
# published by probe_packages for the update-safety plane's fold (the same-process reading:
# never re-probe `pacman -Qm`); PKG_FOREIGN_FOLD is not-run (arm returned before the fold) |
# ok | qm-unreadable | baseline-absent | baseline-unreadable
PKG_FOREIGN_LIVE='' PKG_FOREIGN_FOLD='not-run'
# root-directory metadata arm (round 12, C1) — composed into the packages line at emit
# time, never through PKG_NOTE, so every early return above still publishes it.
ROOT_V=BLOCKED ROOT_NOTE='probe not run'
# ADJ-04 handoff (round 32, C1) — the counts the probes already measured, published for
# main()'s HANDOFF lines. They are the same variables the PLANE notes print from, never a
# second host read and never a regex over the note text. OOM_WINDOW is the oom plane's
# retained window (`boots=<n> <first>..<last>`), printed with spaces replaced by ':' so the
# window= field stays one key=value token; 0/empty means the probe never measured a count,
# so no HANDOFF line is prepared for that class.
OOM_CLUSTERS=0 OOM_WINDOW='' JRN_COREDUMPS=0

usage() {
  cat <<'EOF'
usage: tsukuroi-census.sh [--selftest] [--sample N] [--identity] [--help]

  (no flags)   run the live read-only census over packages / systemd-user / drivers
               (incl. the memory-pressure arm) / journal-boot / update-safety / oom (kill-event watch),
               plus the verdict-neutral DRIFT (pacnew), STORAGE (btrfs error counters) and SCRUB
               (btrfs scrub record, unprivileged view) lines
  --selftest   hermetic fixture-tree test of every verdict arm (writes only under
               ${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.*); exit 0 pass, 1 fail
  --sample N   packages plane: size of the pacman -Qkk sample (default 8)

Verdict line: TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED (packages=.. systemd=.. drivers=.. journal=.. update-safety=.. oom=..)
Exit map:     0 HEALTHY | 1 DEGRADED | 2 BLOCKED (worst plane wins; usage errors also 2); --identity alone prints one TSUKUROI_CENSUS_IDENTITY line naming the executed script bytes, exit 0, no host probe
EOF
}

# ---- helpers -----------------------------------------------------------------
CAP_OUT='' CAP_RC=0
cap() { # run read-only probe; capture stdout+stderr and rc without tripping set -e
  set +e
  CAP_OUT=$("$@" 2>&1)
  CAP_RC=$?
  set -e
}

have() { command -v "$1" >/dev/null 2>&1; }

rank() {
  case "$1" in
    HEALTHY)  printf 0 ;;
    DEGRADED) printf 1 ;;
    BLOCKED)  printf 2 ;;
    *)        printf 9 ;;
  esac
}

worse() { # worse A B -> the more severe of the two
  if [ "$(rank "$2")" -gt "$(rank "$1")" ]; then printf '%s' "$2"; else printf '%s' "$1"; fi
}

nlines() { # count of lines in a string (0 for empty)
  if [ -z "$1" ]; then printf 0; else printf '%s\n' "$1" | grep -c . || true; fi
}

count_glob() { # count_glob DIR PATTERN -> number of matching entries (0 if none)
  local dir=$1 pat=$2 n=0 p
  [ -d "$dir" ] || { printf 0; return; }
  for p in "$dir"/$pat; do
    [ -e "$p" ] && n=$((n + 1))
  done
  printf '%s' "$n"
}

count_pci_nvidia() { # count_pci_nvidia DIR -> nvidia (0x10de) vendor files, or -1 if DIR unreadable
  local dir=$1 n=0 v
  [ -d "$dir" ] || { printf -- '-1'; return; }
  for v in "$dir"/*/vendor; do
    [ -f "$v" ] || continue
    if [ "$(head -c 7 -- "$v" 2>/dev/null || true)" = '0x10de' ]; then n=$((n + 1)); fi
  done
  printf '%s' "$n"
}

class_counts() { # class_counts json|text HAYSTACK -> "oom=N io=N gpu=N other=N"
  local mode=$1 text=$2 pre='' o i g u total
  [ "$mode" = json ] && pre='"MESSAGE":"[^"]*'
  o=$(printf '%s\n' "$text" | grep -cE "${pre}(${CLASS_OOM})" || true)
  i=$(printf '%s\n' "$text" | grep -cE "${pre}(${CLASS_IO})" || true)
  g=$(printf '%s\n' "$text" | grep -cE "${pre}(${CLASS_GPU})" || true)
  u=$(printf '%s\n' "$text" | grep -cE "${pre}(${CLASS_OOM}|${CLASS_IO}|${CLASS_GPU})" || true)
  total=$(nlines "$text")
  printf 'oom=%s io=%s gpu=%s other=%s' "$o" "$i" "$g" "$((total - u))"
}

mem_read() { # mem_read FILE -> first line (trimmed); empty when unreadable
  [ -r "$1" ] || return 0
  head -n1 -- "$1" 2>/dev/null | tr -d '\r' || true
}

mem_field() { # mem_field FILE KEY -> second field of the first KEY row, or empty
  # (the trailing colon of /proc/meminfo keys is tolerated; cgroup keys have none)
  [ -r "$1" ] || return 0
  awk -v k="$2" '{ key = $1; sub(/:$/, "", key) } key == k { print $2; exit }' "$1" 2>/dev/null || true
}

oom_keys() { # oom_keys STDOUT -> sorted unique "YYYY-MM-DD HH:MM" event-cluster keys
  # (short-iso-precise lines only; `-- Boot <id> --` separators are counted out)
  printf '%s\n' "$1" | grep -v '^-- Boot' \
    | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}' | sed -E 's/T/ /' | sort -u || true
}

# ---- plane: packages ---------------------------------------------------------
probe_packages() {
  PKG_V=HEALTHY
  local notes='' names=() s_rc='' drift=0 backup=0 nonroot=0 s_out='' sample_n=0

  if ! have "$PACMAN"; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman=missing (probe cannot run)"
    return
  fi
  if [ -e "$PACMAN_DB/db.lck" ]; then
    PKG_V=BLOCKED
    PKG_NOTE='db.lck=present — interrupted transaction (SKILL.md:41,45)'
    return
  fi

  cap "$PACMAN" -Qq
  local qq_rc=$CAP_RC
  if [ "$qq_rc" -ne 0 ]; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qq rc=$qq_rc [local db unreadable]"
    return
  fi
  mapfile -t names < <(printf '%s\n' "$CAP_OUT" | grep -v '^[[:space:]]*$' | head -n "$SAMPLE_N")
  sample_n=${#names[@]}
  if [ "$sample_n" -eq 0 ]; then
    PKG_V=BLOCKED
    PKG_NOTE='pacman -Qq listed no packages [local db empty; state not assessable]'
    return
  fi

  cap "$PACMAN" -Qkk "${names[@]}"
  s_rc=$CAP_RC
  s_out=$(printf '%s\n' "$CAP_OUT" | tr '\r' '\n')
  if [ "$s_rc" -ne 0 ] && [ "$s_rc" -ne 1 ]; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample rc=$s_rc [probe cannot run]"
    return
  fi
  # Round 42 (R41-CENSUS-PIPEFAIL-692): never `printf | grep -q` / `| grep -m1` / `| head` under pipefail on a
  # probe buffer — the early reader exits, printf dies of SIGPIPE, and the pipeline reads false (a wrong verdict)
  # or, in an assignment, kills the census with exit 141. Let awk consume the whole input: no early exit, and no
  # here-string either (a here-string over 64 KiB is a temporary file, which breaks the no-write contract and, on a
  # full $TMPDIR or /tmp, silently skips the test — round-42 wave 1, C1RevFix D1).
  local err_line=''
  if err_line=$(printf '%s\n' "$s_out" | awk '/^error:/ { if (!p) { print; p = 1 } } END { if (!p) exit 1 }'); then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample probe error: $err_line"
    return
  fi

  drift=$(printf '%s\n' "$s_out" \
    | sed -nE 's/^[^:]+: [0-9]+ total files, ([0-9]+) altered files?.*/\1/p' \
    | awk '{s += $1} END {print s + 0}')
  backup=$(printf '%s\n' "$s_out" | grep -c '^backup file: ' || true)
  nonroot=$(printf '%s\n' "$s_out" \
    | grep -cE '\(failed to calculate SHA256 checksum\)|\(Permission denied\)' || true)
  local drift_pkgs
  drift_pkgs=$(printf '%s\n' "$s_out" \
    | sed -nE 's/^([^:]+): [0-9]+ total files, [1-9][0-9]* altered files?.*/\1/p' \
    | paste -sd, - || true)

  local foreign_n='?' foreign_rc=0
  cap "$PACMAN" -Qm
  foreign_rc=$CAP_RC
  if [ "$foreign_rc" -eq 0 ]; then foreign_n=$(nlines "$CAP_OUT"); fi

  # foreign watch arm (round 7, lane S7-1): compare `pacman -Qm` (name version per row)
  # against the accepted baseline so the plane reports known-vs-new instead of a bare
  # count. Fail-closed both ways: a baseline row hides neither a new package nor a
  # version change, and an absent/unreadable baseline or an unreadable -Qm probe never
  # reads as a pass (r6 baseline contract, plans/round-6-record-draft.md §4).
  local base_txt='' base_state='' foreign_known=0 foreign_new_n=0 foreign_drift_n=0 foreign_gone_n=0
  local foreign_new='' foreign_drift='' foreign_gone=''
  if [ -n "$FOREIGN_BASELINE" ]; then
    if [ -f "$FOREIGN_BASELINE" ] && [ -r "$FOREIGN_BASELINE" ]; then
      base_txt=$(cat -- "$FOREIGN_BASELINE" 2>/dev/null || true)
      base_state="file($(nlines "$base_txt"))"
    elif [ -e "$FOREIGN_BASELINE" ]; then
      base_state='unreadable'
    else
      base_state='absent'
    fi
  else
    base_txt=$R6_FOREIGN_BASELINE
    base_state="r6($(nlines "$base_txt"))"
  fi

  if [ "$foreign_rc" -eq 0 ] && [ "$base_state" != absent ] && [ "$base_state" != unreadable ]; then
    local nm ver bn live_names=''
    while read -r nm ver _; do
      [ -n "$nm" ] || continue
      live_names="$live_names $nm"
      bn=$(printf '%s\n' "$base_txt" | awk -v n="$nm" '$1 == n && !f { print $2; f = 1 }')   # full read (round 42: an awk `exit` under pipefail killed the census on a large baseline)
      if [ -z "$bn" ]; then
        foreign_new_n=$((foreign_new_n + 1)); foreign_new="$foreign_new $nm"
      elif [ "$ver" = "$bn" ]; then
        foreign_known=$((foreign_known + 1))
      else
        foreign_drift_n=$((foreign_drift_n + 1)); foreign_drift="$foreign_drift $nm($bn->${ver:-?})"
      fi
    done <<< "$CAP_OUT"
    local rn rv
    while read -r rn rv _; do
      [ -n "$rn" ] || continue
      case " $live_names " in
        *" $rn "*) : ;;
        *) foreign_gone_n=$((foreign_gone_n + 1)); foreign_gone="$foreign_gone $rn" ;;
      esac
    done <<< "$base_txt"
  fi

  local fr_note
  if [ "$foreign_rc" -ne 0 ]; then
    fr_note="foreign=? [pacman -Qm unreadable]"
  elif [ "$base_state" = absent ] || [ "$base_state" = unreadable ]; then
    fr_note="foreign=$foreign_n(base=$base_state [known/new/drift/gone unknown])"
  else
    fr_note="foreign=$foreign_n(known=$foreign_known new=$foreign_new_n drift=$foreign_drift_n gone=$foreign_gone_n) base=$base_state"
    [ -n "$foreign_new" ] && fr_note="$fr_note new=[${foreign_new# }]"
    [ -n "$foreign_drift" ] && fr_note="$fr_note drift=[${foreign_drift# }]"
    [ -n "$foreign_gone" ] && fr_note="$fr_note gone=[${foreign_gone# }]"
  fi

  # publish the same-process reading for the update-safety plane's class fold (round 9,
  # lane S9-1) — the fold joins these names against the register's classes; it never
  # re-probes `pacman -Qm`. `${live_names:-}`: the name list is declared inside the fold
  # block above, which does not run for an absent/unreadable baseline (set -u would abort).
  PKG_FOREIGN_LIVE="${live_names:-}"
  if [ "$foreign_rc" -ne 0 ]; then
    PKG_FOREIGN_FOLD='qm-unreadable'
  elif [ "$base_state" = absent ]; then
    PKG_FOREIGN_FOLD='baseline-absent'
  elif [ "$base_state" = unreadable ]; then
    PKG_FOREIGN_FOLD='baseline-unreadable'
  else
    PKG_FOREIGN_FOLD='ok'
  fi

  local pins_n='?' pins_rc=0 pins_names='' holds='none'
  cap "$PACMAN_CONF" IgnorePkg IgnoreGroup
  pins_rc=$CAP_RC
  if [ "$pins_rc" -eq 0 ]; then
    pins_n=$(nlines "$CAP_OUT")
    pins_names=$(printf '%s\n' "$CAP_OUT" | grep . | paste -sd, - || true)
  fi
  if [ -r "$PACMAN_CONF_FILE" ]; then
    holds=$(grep -hE '^[[:space:]]*HoldPkg' "$PACMAN_CONF_FILE" 2>/dev/null \
      | head -n1 | sed -E 's/^[[:space:]]*HoldPkg[[:space:]]*=[[:space:]]*//' || true)
    holds=${holds:-none}
  fi

  PKG_NOTE="pacman -Qkk rc=$s_rc sample=$sample_n($(printf '%s,' "${names[@]}" | sed -E 's/,$//')) drift=$drift${drift_pkgs:+[$drift_pkgs]} backup_diffs=$backup nonroot_artifacts=$nonroot"
  PKG_NOTE="$PKG_NOTE; $fr_note; pins=${pins_names:-none}; holds=$holds; db.lck=absent"

  if [ "$drift" -gt 0 ]; then PKG_V=DEGRADED; fi
  if [ "$foreign_rc" -ne 0 ] || [ "$base_state" = absent ] || [ "$base_state" = unreadable ] \
    || [ "$foreign_new_n" -gt 0 ] || [ "$foreign_drift_n" -gt 0 ] || [ "$foreign_gone_n" -gt 0 ]; then
    PKG_V=DEGRADED
  fi
  if [ "$pins_n" != '0' ]; then PKG_V=DEGRADED; fi
  return
}

root_locator_class() { # root_locator_class PATH -> absolute|empty|relative|unsafe
  # An override path is caller data, not host evidence. Only an absolute path from a
  # conservative character set may be stat'd and printed; `=` and whitespace are rejected
  # so a path like `/x root_mode=0755` can neither forge a token nor reach stat. The raw
  # override is never echoed for the empty/relative/unsafe classes.
  case "$1" in
    '') printf 'empty' ;;
    /*)
      case "$1" in
        *[!A-Za-z0-9._/+-]*) printf 'unsafe' ;;
        *) printf 'absolute' ;;
      esac
      ;;
    *) printf 'relative' ;;
  esac
}

# ---- plane arm: root-directory metadata (round 12, C1) -----------------------
# The packages plane cannot judge `/` or any unowned directory: `pacman -Qo /` rc=1 and
# `-Qkk` verifies package-owned files only (QUALITY.md #13). This arm reads the root
# directory's own metadata and reports it as facts; it makes no writability claim for any
# process and applies no universal mode policy. Owner-write (0200) / owner-search (0100)
# absence is REPORT-ONLY: the bits are printed with `root_report=`, but the arm stays
# HEALTHY (parent ruling 2026-10-20, after /usr/lib/tmpfiles.d/root.conf `z / 555` was
# found: a declared 0555 root must not be graded unhealthy). Only unavailable metadata
# (missing path / EACCES / dangling link), a non-directory, or an empty/relative/unsafe
# TSUKUROI_ROOT_DIR override (rejected before stat, caller path never echoed) is BLOCKED.
# The report states observed bits, not intent, and never says a mode is wrong or should be
# 0755.
probe_root_meta() {
  ROOT_V=HEALTHY
  local rc mode='' uid='' gid='' ftype='' why='unknown' link='' num ow ox report='' loc cls
  cls=$(root_locator_class "$ROOT_DIR")
  if [ "$cls" != 'absolute' ]; then
    # Empty/relative/unsafe override: BLOCKED before any stat, no caller path echoed.
    ROOT_V=BLOCKED
    ROOT_NOTE="root_status=unavailable(override=$cls) root_mode=unknown root_uid=unknown root_gid=unknown root_euid=$EUID root_owner_write=unknown root_owner_search=unknown root_src=$ROOT_SRC root_dir=$cls"
    return
  fi
  loc=$ROOT_DIR
  # `stat -L` resolves symlinks (a bare `[ -d ]` and plain stat would disagree); LC_ALL=C
  # keeps %F and strerror tokens stable; %04a pins a four-digit octal mode (0555/1777), so
  # a consumer never sees the 555-vs-0555 token drift. `cap` keeps a failed probe from
  # tripping set -e: a bare command substitution would exit 1 here, and 1 is DEGRADED.
  cap env LC_ALL=C stat -L -c '%04a %u %g %F' -- "$ROOT_DIR"
  rc=$CAP_RC
  if [ "$rc" -ne 0 ]; then
    # Match the strerror suffix, not a bare phrase: the message echoes the path.
    case "$CAP_OUT" in
      *': Permission denied'*) why='permission-denied' ;;
      *': No such file or directory'*) why='missing' ;;
      *': Too many levels of symbolic links'*) why='symlink-loop' ;;
    esac
    cap env LC_ALL=C stat -c '%F' -- "$ROOT_DIR"
    if [ "$CAP_RC" -eq 0 ] && [ "$CAP_OUT" = 'symbolic link' ]; then
      link=' root_type=symlink(unresolved)'
    fi
    ROOT_V=BLOCKED
    ROOT_NOTE="root_status=unavailable(stat=rc=$rc errno=$why) root_mode=unknown root_uid=unknown root_gid=unknown$link root_euid=$EUID root_owner_write=unknown root_owner_search=unknown root_src=$ROOT_SRC root_dir=$loc"
    return
  fi

  read -r mode uid gid ftype <<< "$CAP_OUT"
  ftype=${ftype// /-}   # one token: regular-empty-file, symbolic-link, ...
  case "$mode" in
    '' | *[!0-7]*)
      ROOT_V=BLOCKED
      ROOT_NOTE="root_status=mode-unparseable(mode=$mode) root_mode=unknown root_uid=unknown root_gid=unknown root_euid=$EUID root_owner_write=unknown root_owner_search=unknown root_src=$ROOT_SRC root_dir=$loc"
      return
      ;;
  esac
  # uid/gid are printed facts; a malformed stat field must not be carried as evidence.
  # Non-numeric -> unavailable(parse=...) with the observed mode kept.
  local badmeta=''
  case "$uid" in '' | *[!0-9]*) badmeta='uid' ;; esac
  case "$gid" in '' | *[!0-9]*) badmeta="${badmeta:+$badmeta,}gid" ;; esac
  if [ -n "$badmeta" ]; then
    ROOT_V=BLOCKED
    ROOT_NOTE="root_status=unavailable(parse=$badmeta) root_mode=$mode root_uid=unknown root_gid=unknown root_euid=$EUID root_owner_write=unknown root_owner_search=unknown root_src=$ROOT_SRC root_dir=$loc"
    return
  fi
  if [ "$ftype" != 'directory' ]; then
    ROOT_V=BLOCKED
    ROOT_NOTE="root_status=non-directory(type=$ftype) root_mode=$mode root_uid=$uid root_gid=$gid root_euid=$EUID root_owner_write=unknown root_owner_search=unknown root_src=$ROOT_SRC root_dir=$loc"
    return
  fi

  # `%04a` is four octal digits and may carry a special-bit digit (1777/2755). `8#` is
  # mandatory: decimal arithmetic on "0755" tests the wrong bit; string slicing would
  # mangle special bits. Special bits themselves are verdict-neutral.
  num=$((8#$mode))
  ow=$(( (num & 0200) ? 1 : 0 ))
  ox=$(( (num & 0100) ? 1 : 0 ))
  ROOT_NOTE="root_status=ok root_mode=$mode root_uid=$uid root_gid=$gid root_euid=$EUID"
  ROOT_NOTE="$ROOT_NOTE root_owner_write=$([ "$ow" -eq 1 ] && printf present || printf absent)"
  ROOT_NOTE="$ROOT_NOTE root_owner_search=$([ "$ox" -eq 1 ] && printf present || printf absent)"
  [ "$ow" -eq 0 ] && report='owner-write-absent'
  [ "$ox" -eq 0 ] && report="${report:+$report,}owner-search-absent"
  if [ -n "$report" ]; then
    # Report-only by parent ruling: no ROOT_V change, so the packages verdict is untouched.
    ROOT_NOTE="$ROOT_NOTE root_report=$report root_intent=not-assessed"
  fi
  ROOT_NOTE="$ROOT_NOTE root_src=$ROOT_SRC root_dir=$loc"
  return
}

# ---- plane: systemd (user scope) ---------------------------------------------
probe_systemd() {
  SYS_V=HEALTHY
  if ! have "$SYSTEMCTL"; then
    SYS_V=BLOCKED
    SYS_NOTE='systemctl=missing (probe cannot run)'
    return
  fi

  cap "$SYSTEMCTL" --user is-system-running --no-pager
  local s_rc=$CAP_RC state
  state=${CAP_OUT%%$'\n'*}; state=${state//$'\r'/}; state=${state%"${state##*[![:space:]]}"}   # first line, no early reader (R45-C1)
  case "$state" in
    running | degraded | starting | stopping | maintenance | offline | unknown) : ;;
    *)
      SYS_V=BLOCKED
      SYS_NOTE="systemctl --user unusable rc=$s_rc [$(printf '%s' "$state" | cut -c1-90)]"
      return
      ;;
  esac
  if [ "$state" = offline ] || [ "$state" = maintenance ]; then
    SYS_V=BLOCKED
    SYS_NOTE="scope=user state=$state [core function offline]"
    return
  fi

  cap "$SYSTEMCTL" --user list-units --state=failed --no-legend --plain --no-pager
  local f_rc=$CAP_RC failed=0
  if [ "$f_rc" -ne 0 ]; then
    SYS_V=BLOCKED
    SYS_NOTE="list-units --state=failed rc=$f_rc [probe cannot run]"
    return
  fi
  failed=$(printf '%s\n' "$CAP_OUT" | awk 'NF && $2 == "loaded" && $3 == "failed"' | wc -l)

  cap "$SYSTEMCTL" --user list-unit-files --type=timer --state=enabled --no-legend --no-pager
  local t_rc=$CAP_RC timers_enabled=0 timers=() t_scan=0
  if [ "$t_rc" -ne 0 ]; then
    SYS_V=BLOCKED
    SYS_NOTE="list-unit-files --type=timer --state=enabled rc=$t_rc [probe cannot run]"
    return
  fi
  timers_enabled=$(printf '%s\n' "$CAP_OUT" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | wc -l)
  mapfile -t timers < <(printf '%s\n' "$CAP_OUT" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | head -n "$TIMER_SCAN_MAX")

  local t_fail=0 t_unknown=0 bad='' r
  for t in "${timers[@]}"; do
    t_scan=$((t_scan + 1))
    cap "$SYSTEMCTL" --user show "$t" -p Result --value --no-pager
    r=${CAP_OUT%%$'\n'*}; r=${r//$'\r'/}   # first line, no early reader (R45-C1)
    if [ "$CAP_RC" -ne 0 ] || [ -z "$r" ]; then
      t_unknown=$((t_unknown + 1))
    elif [ "$r" != success ]; then
      t_fail=$((t_fail + 1))
      bad="${bad}${t}=${r} "
    fi
  done

  SYS_NOTE="scope=user state=$state failed=$failed timers_enabled=$timers_enabled timers_scanned=$t_scan timer_fail=$t_fail timer_unknown=$t_unknown"
  [ -n "$bad" ] && SYS_NOTE="$SYS_NOTE ($bad)"

  if [ "$failed" -gt 0 ] || [ "$t_fail" -gt 0 ] || [ "$t_unknown" -gt 0 ]; then SYS_V=DEGRADED; fi
  case "$state" in degraded | starting | stopping) SYS_V=DEGRADED ;; esac
  return
}

# ---- plane: drivers ----------------------------------------------------------
probe_drivers() {
  DRV_V=HEALTHY
  local ring='' ring_rc=0 kerr=0 cls='oom=0 io=0 gpu=0 other=0' restrict='?'

  restrict=$(head -n1 "$DMESG_RESTRICT_FILE" 2>/dev/null | tr -d '\r' || true)
  restrict=${restrict:-?}

  if have "$DMESG"; then
    cap "$DMESG" --level=err,crit,alert,emerg
    if [ "$CAP_RC" -eq 0 ]; then
      ring=dmesg
      kerr=$(nlines "$CAP_OUT")
      cls=$(class_counts text "$CAP_OUT")
    else
      ring_rc=$CAP_RC
    fi
  else
    ring_rc=127
  fi

  if [ -z "$ring" ]; then
    if ! have "$JOURNALCTL"; then
      DRV_V=BLOCKED
      DRV_NOTE="kernel ring unusable: dmesg rc=$ring_rc, journalctl=missing"
      return
    fi
    cap "$JOURNALCTL" -k -b -p err -o json --no-pager
    if [ "$CAP_RC" -ne 0 ]; then
      DRV_V=BLOCKED
      DRV_NOTE="kernel ring unusable: dmesg rc=$ring_rc, journalctl -k rc=$CAP_RC"
      return
    fi
    ring='journalctl-k'
    kerr=$(nlines "$CAP_OUT")
    cls=$(class_counts json "$CAP_OUT")
  fi

  # kerr == 0 is only a pass if the ring really has data; an empty ring cannot be told
  # apart from a clean one, and must never be quoted as a fake HEALTHY.
  if [ "$kerr" -eq 0 ]; then
    if [ "$ring" = 'journalctl-k' ]; then
      cap "$JOURNALCTL" -k -b -o json --no-pager
      if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then
        DRV_V=BLOCKED
        DRV_NOTE='kernel ring empty/unreadable (journalctl -k -b lists no kernel entries)'
        return
      fi
    else
      cap "$DMESG"
      if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then
        DRV_V=BLOCKED
        DRV_NOTE='kernel ring empty/unreadable (dmesg lists no records)'
        return
      fi
    fi
  fi

  local pci_n smi='absent' smi_rc=127 driver='' mods=-1 nodes=0 nv='' modnote=''
  pci_n=$(count_pci_nvidia "$PCI_SYSFS")
  if have "$NVIDIA_SMI"; then
    cap "$NVIDIA_SMI" --query-gpu=name,driver_version --format=csv,noheader
    smi_rc=$CAP_RC
    if [ "$smi_rc" -eq 0 ] && [ -n "$(printf '%s' "$CAP_OUT" | tr -d '[:space:]')" ]; then
      smi=ok
      driver=${CAP_OUT%%$'\n'*}; driver=$(printf '%s\n' "$driver" | awk -F', *' '{print $NF}')   # first line, no early reader (R45-C1)
    else
      smi="rc=$smi_rc"
    fi
  fi
  if have "$LSMOD"; then
    cap "$LSMOD"
    mods=$(printf '%s\n' "$CAP_OUT" | grep -cE '^nvidia' || true)
  fi
  nodes=$(count_glob "$DEV_DIR" 'nvidia*')

  if [ "$pci_n" -gt 0 ]; then
    if [ "$smi" != ok ]; then
      DRV_V=BLOCKED
      modnote="pci_10de=$pci_n but nvidia-smi not answering ($smi) — core function offline (SKILL.md:44)"
    elif [ "$mods" -le 0 ]; then
      DRV_V=BLOCKED
      modnote="pci_10de=$pci_n but no nvidia module loaded — core function offline"
    elif [ "$nodes" -eq 0 ]; then
      DRV_V=BLOCKED
      modnote="pci_10de=$pci_n but no /dev/nvidia* node — core function offline (SKILL.md:44)"
    else
      nv=present
    fi
  elif [ "$pci_n" -eq 0 ]; then
    nv='absent(pci_10de=0)'
  else
    if [ "$smi" = ok ] && [ "$mods" -gt 0 ]; then
      nv='present(pci inventory unreadable)'
    else
      DRV_V=BLOCKED
      modnote='PCI inventory unreadable and no positive nvidia evidence — cannot assess read-only'
    fi
  fi

  if [ "$DRV_V" != BLOCKED ]; then
    if [ "$kerr" -gt 0 ]; then
      DRV_V=DEGRADED
      DRV_NOTE="ring=$ring dmesg_restrict=$restrict kerr=$kerr ($cls) [unknown: accepted noise floor]; nvidia=$nv smi=${driver:-$smi} modules=$mods nodes=$nodes pci_10de=$pci_n"
    else
      DRV_NOTE="ring=$ring dmesg_restrict=$restrict kerr=0 ($cls); nvidia=$nv smi=${driver:-$smi} modules=$mods nodes=$nodes pci_10de=$pci_n"
    fi
  else
    DRV_NOTE="$modnote; ring=$ring kerr=$kerr ($cls); smi=${driver:-$smi} modules=$mods nodes=$nodes pci_10de=$pci_n"
  fi
  return
}

# ---- arm: memory pressure (rides the drivers plane's line and verdict) -------
# Round-7 addition, lane S7-2. Detection-only, read-only, non-root. Vocabulary:
# corpus/knowledge/oom-event-plane.md §8 (classes C1-C6) plus the note's reading
# rules — `memory.events oom_kill` is a PRESENCE FLAG, never an event count (§4.2),
# the journal messages are the event list, and the page-cache-inclusive
# `memory.peak` is not a pressure reading (§4.4). Fails closed: an unreadable
# signal is a named unknown and degrades the arm; only a total inability to read
# any class (cgroup sweep empty AND all journal probes unusable) reads BLOCKED —
# never a fake pass. Nothing is written; no cgroup, unit or service is touched;
# the operator remediates.
probe_mem_arm() {
  MEM_V=HEALTHY
  local unk='' deg=0 j_ok=0 cg_ok=0
  local k_oom='?' s_oom='?' sg_oom='?'
  local sweep=0 present=0 localp=0 names=''
  local sock='-' swap_fail='-' swap_peak='-' swap_total='-' swap_pct='-'
  local ps_in='-' ps_out='-' psi_s='-' psi_f='-' psi_t='-'
  local avail='-' shmem='-' g_max='-' g_high='-' g_grp='-'
  local slice="$CGROUP_ROOT/$MEM_SLICE" f rel v

  # C1-C3 — the journal side: entry counts only (`-o json` lines). `journalctl
  # --grep` exits 1 on no-match (measured 2026-10-14), so rc 1 = "0 entries" and
  # any other non-zero rc = unreadable.
  if have "$JOURNALCTL"; then
    cap "$JOURNALCTL" -k -b -p err -o json --no-pager --grep "$CLASS_OOM"
    case "$CAP_RC" in
      0) k_oom=$(nlines "$CAP_OUT"); j_ok=$((j_ok + 1)) ;;
      1) k_oom=0; j_ok=$((j_ok + 1)) ;;
      *) unk="${unk}C1 " ;;
    esac
    cap "$JOURNALCTL" -b -o json --no-pager --grep "$CLASS_OOM_SYS"
    case "$CAP_RC" in
      0) s_oom=$(nlines "$CAP_OUT"); j_ok=$((j_ok + 1)) ;;
      1) s_oom=0; j_ok=$((j_ok + 1)) ;;
      *) unk="${unk}C2 " ;;
    esac
    cap "$JOURNALCTL" -b -o json --no-pager --grep "$CLASS_SIGKILL"
    case "$CAP_RC" in
      0) sg_oom=$(nlines "$CAP_OUT"); j_ok=$((j_ok + 1)) ;;
      1) sg_oom=0; j_ok=$((j_ok + 1)) ;;
      *) unk="${unk}C3 " ;;
    esac
  else
    unk="${unk}C1 C2 C3 "
  fi

  # C4 — cgroup presence flags, bounded sweep over memory.events[.local]
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    sweep=$((sweep + 1))
    v=$(awk '$1 == "oom_kill" { print $2; exit }' "$f" 2>/dev/null || true)
    if [ -n "$v" ] && [ "$v" != 0 ]; then
      rel=${f#"$CGROUP_ROOT"/}
      rel=${rel%/memory.events}
      case "$f" in
        *.local) localp=$((localp + 1)) ;;
        *)
          present=$((present + 1))
          [ "$present" -le 3 ] && names="${names}${names:+,}${rel}"
          ;;
      esac
    fi
  done < <(find "$CGROUP_ROOT" -xdev \( -name memory.events -o -name memory.events.local \) \
             -print 2>/dev/null | LC_ALL=C sort | head -n 4000)
  [ "$sweep" -gt 0 ] && cg_ok=1

  # C5 — swap-pressure anchors (+ the socket-throttle class and the guards shape)
  if [ -d "$slice" ]; then
    swap_fail=$(mem_field "$slice/memory.swap.events" fail)
    swap_peak=$(mem_read "$slice/memory.swap.peak")
    ps_in=$(mem_field "$slice/memory.stat" pswpin)
    ps_out=$(mem_field "$slice/memory.stat" pswpout)
    sock=$(mem_field "$slice/memory.events" sock_throttled)
    g_max=$(mem_read "$slice/memory.max")
    g_high=$(mem_read "$slice/memory.high")
    g_grp=$(mem_read "$slice/memory.oom.group")
    [ -r "$slice/memory.swap.events" ] || unk="${unk}C5-swap "
    [ -r "$slice/memory.stat" ] || unk="${unk}C5-stat "
  else
    unk="${unk}C5-slice "
  fi
  swap_total=$(mem_field "$MEMINFO_FILE" SwapTotal)
  case "$swap_peak" in '' | *[!0-9]*) swap_peak='-' ;; esac
  case "$swap_total" in '' | *[!0-9]*) swap_total='-' ;; esac
  if [ "$swap_peak" != '-' ] && [ "$swap_total" != '-' ] && [ "$swap_total" -gt 0 ]; then
    swap_pct=$(awk -v p="$swap_peak" -v t="$swap_total" \
      'BEGIN { printf "%d%%", (p / 1024 / t) * 100 }')
  fi
  case "$swap_fail" in '' | *[!0-9]*) swap_fail='-' ;; esac
  case "$sock" in '' | *[!0-9]*) sock='-' ;; esac
  case "$ps_in" in '' | *[!0-9]*) ps_in='-' ;; esac
  case "$ps_out" in '' | *[!0-9]*) ps_out='-' ;; esac
  g_max=${g_max:-'-'} g_high=${g_high:-'-'} g_grp=${g_grp:-'-'}

  # C6 — live shape: PSI (avg300 + total) and the meminfo picture
  [ -r "$MEMINFO_FILE" ] || unk="${unk}C6-meminfo "
  avail=$(mem_field "$MEMINFO_FILE" MemAvailable); avail=${avail:-'-'}
  shmem=$(mem_field "$MEMINFO_FILE" Shmem); shmem=${shmem:-'-'}
  if [ -r "$PRESSURE_FILE" ]; then
    read -r psi_s psi_f psi_t < <(awk '
      $1 == "some" || $1 == "full" {
        for (i = 2; i <= NF; i++) { split($i, a, "="); v[a[1]] = a[2] }
        if ($1 == "some") s = v["avg300"]; else { f = v["avg300"]; t = v["total"] }
      }
      END { printf "%s %s %s\n", (s == "" ? "-" : s), (f == "" ? "-" : f), (t == "" ? "-" : t) }' \
      "$PRESSURE_FILE" 2>/dev/null || true)
    psi_s=${psi_s:-'-'} psi_f=${psi_f:-'-'} psi_t=${psi_t:-'-'}
  else
    unk="${unk}C6-psi "
  fi

  # verdict: any class > 0 degrades; any unreadable signal degrades; BLOCKED only
  # when no class can be read at all (fail closed — never a fake pass)
  [ "$k_oom" != '?' ] && [ "$k_oom" -gt 0 ] && deg=1
  [ "$s_oom" != '?' ] && [ "$s_oom" -gt 0 ] && deg=1
  [ "$sg_oom" != '?' ] && [ "$sg_oom" -gt 0 ] && deg=1
  [ "$present" -gt 0 ] && deg=1
  [ "$localp" -gt 0 ] && deg=1
  [ "$swap_fail" != '-' ] && [ "$swap_fail" -gt 0 ] && deg=1

  if [ "$j_ok" -eq 0 ] && [ "$cg_ok" -eq 0 ]; then
    MEM_V=BLOCKED
  elif [ "$deg" -gt 0 ] || [ -n "$unk" ]; then
    MEM_V=DEGRADED
  fi

  MEM_NOTE="[${MEM_V}] C1_kernel_oom=$k_oom C2_sysd_oom=$s_oom C3_sigkill=$sg_oom; C4_sweep=$sweep C4_present=$present${names:+[$names]} C4_local=$localp; C5_swap_fail=$swap_fail C5_swap_peak_pct=$swap_pct C5_pswp=$ps_in/$ps_out C5_sock_throttled=$sock; C6_psi_some_avg300=$psi_s C6_psi_full_avg300=$psi_f C6_psi_full_total_us=$psi_t C6_avail_kb=$avail C6_shmem_kb=$shmem; guards=$g_max/$g_high oom.group=$g_grp${unk:+; unknown=[${unk% }]}; r6 vocab: oom-event-plane.md §8"
  return
}

# ---- plane: oom (the kill-event watch — round 8's specified-not-landed contract) ------------
# Round-9 addition, lane S9-2. `plans/round-8.plan.md:57-115` specified the OOM/kill-event watch
# as the census's next plane line; its memory-arm half landed in round 7 as `drivers.mem`, the
# watch half did not (S8-4's round-8 record draft: claim (a)/(b) "are not in the landed gate").
# This lands the watch — the memory-arm findings as census output — on the round-7
# embedded-snapshot baseline mechanism, with `drivers.mem` untouched (double-count precedent,
# round 3: the arm reads THIS boot at entry level and folds into the drivers verdict; this
# plane reads the whole retained window, clusters the event list, and compares it against the
# declared waves — cross-boot state the arm does not keep).
#
# Reading rules from the round-8 kill-event findings (`kill-event-deep-r8.md` §1 F1-F8),
# printed, never adjudicated: counters are presence flags, never event counts (F3); peaks are
# lifetime maxima, not datable to a kill (F5); launch counts are not live units (F6); the
# 13:10:59 slice notice carries both readings (H1-H3). Fails closed: an unreadable window or
# scan is BLOCKED, an absent baseline/new cluster/lost declared wave/unreadable ledger is
# DEGRADED, never a fake pass. Nothing is written; no cgroup, unit or service is touched.
probe_oom_plane() {
  OOM_V=HEALTHY
  OOM_CLUSTERS=0
  local unk='' bad=''
  local boots=0 win_first='-' win_last='-'
  local k_n=0 k_kill=0 a_n=0 s_n=0
  local a_out='' s_out=''
  local clusters='' cjoin='' clist='' cluster_n=0
  local base_txt='' base_state='' bjoin=''
  local known=0 new_n=0 missing=0 oow=0
  local known_ids='' new_keys='' miss_keys='' oow_keys=''
  local ledger='-'

  if ! have "$JOURNALCTL"; then
    OOM_V=BLOCKED
    OOM_NOTE='journalctl=missing (window cannot be read)'
    return
  fi

  # window — measured, never assumed: boot count + retained date bounds from --list-boots.
  # 0 boots (or an unreadable record) is BLOCKED — an empty scan is only a pass when the
  # window itself is measured.
  cap "$JOURNALCTL" --list-boots --no-pager
  local lb_rc=$CAP_RC
  if [ "$lb_rc" -ne 0 ]; then
    OOM_V=BLOCKED
    OOM_NOTE="window unreadable: journalctl --list-boots rc=$lb_rc [fails closed]"
    return
  fi
  read -r boots win_first win_last < <(printf '%s\n' "$CAP_OUT" | awk '
    NF && $1 ~ /^-?[0-9]+$/ { n++; if (n == 1) f = $4; l = $8 }
    END { printf "%d %s %s\n", n + 0, (f == "" ? "-" : f), (l == "" ? "-" : l) }')
  if [ "$boots" -lt 1 ] || [ "$win_first" = '-' ] || [ "$win_last" = '-' ]; then
    OOM_V=BLOCKED
    OOM_NOTE="window empty: boots=$boots [no boot measured; empty is not a clean window]"
    return
  fi
  # the retained window, published verbatim for the ADJ-04 handoff line (the PLANE note
  # below builds the same string; kept separate so no PLANE text is touched here)
  OOM_WINDOW="boots=$boots $win_first..$win_last"

  # C1 — kernel OOM family over the whole window (server-side --grep; entry-level count with
  # `-- Boot <id> --` separators counted out). killed_process is the F1 discriminator.
  cap "$JOURNALCTL" -k --grep "$CLASS_OOM" -o short-iso-precise --no-pager
  case "$CAP_RC" in
    0 | 1)
      k_n=$(printf '%s\n' "$CAP_OUT" | grep -v '^-- Boot' | grep -c . || true)
      k_kill=$(printf '%s\n' "$CAP_OUT" | grep -c 'Killed process' || true)
      ;;
    *) bad="${bad}C1 "; k_n='?' ;;
  esac

  # C2/C3 — the event list over the window (rc 1 = "0 entries", measured systemd 261; any
  # other non-zero rc is unreadable and fails the plane closed). Clusters are minute keys:
  # a bare line count is a trap (event A's 3 kernel lines are one event).
  cap "$JOURNALCTL" --grep "$CLASS_OOM_SYS" -o short-iso-precise --no-pager
  case "$CAP_RC" in
    0 | 1) a_out=$CAP_OUT; a_n=$(printf '%s\n' "$a_out" | grep -v '^-- Boot' | grep -c . || true) ;;
    *) bad="${bad}C2 "; a_n='?' ;;
  esac
  cap "$JOURNALCTL" --grep "$CLASS_SIGKILL" -o short-iso-precise --no-pager
  case "$CAP_RC" in
    0 | 1) s_out=$CAP_OUT; s_n=$(printf '%s\n' "$s_out" | grep -v '^-- Boot' | grep -c . || true) ;;
    *) bad="${bad}C3 "; s_n='?' ;;
  esac
  clusters=$(oom_keys "$(printf '%s\n%s\n' "$a_out" "$s_out")")
  if [ -n "$clusters" ]; then
    cjoin=$(printf '%s\n' "$clusters" | paste -sd' ' -)
    clist=$(printf '%s\n' "$clusters" | paste -sd, -)
  fi
  cluster_n=$(printf '%s\n' "$clusters" | grep -c . || true)
  case "$cluster_n" in '' | *[!0-9]*) cluster_n=0 ;; esac
  # the dated kill-event cluster count, published for the ADJ-04 handoff line (the same
  # number the PLANE oom note prints as `clusters=`; a cumulative ledger never reaches it)
  OOM_CLUSTERS=$cluster_n

  # baseline — embedded r8 snapshot by default, external file via override (round-7 pattern)
  if [ -n "$OOM_BASELINE" ]; then
    if [ -f "$OOM_BASELINE" ] && [ -r "$OOM_BASELINE" ]; then
      base_txt=$(cat -- "$OOM_BASELINE" 2>/dev/null || true)
      base_state="file($(nlines "$base_txt"))"
    elif [ -e "$OOM_BASELINE" ]; then
      base_state='unreadable'
    else
      base_state='absent'
    fi
  else
    base_txt=$R8_OOM_BASELINE
    base_state="r8($(nlines "$base_txt"))"
  fi

  if [ -n "$base_txt" ]; then
    bjoin=$(printf '%s\n' "$base_txt" | awk 'NF >= 2 { printf "%s %s\n", $1, $2 }' | paste -sd' ' -)
    local bd bt bid
    while read -r bd bt bid _; do
      case "$bd" in '' | '#'*) continue ;; esac
      case " $cjoin " in
        *" $bd $bt "*)
          known=$((known + 1))
          known_ids="${known_ids}${known_ids:+, }${bid:-?}"
          ;;
        *)
          if [ "$bd" \< "$win_first" ] || [ "$bd" \> "$win_last" ]; then
            oow=$((oow + 1))
            oow_keys="${oow_keys}${oow_keys:+,}$bd $bt"
          else
            missing=$((missing + 1))
            miss_keys="${miss_keys}${miss_keys:+,}$bd $bt"
          fi
          ;;
      esac
    done <<< "$base_txt"
    local k
    while read -r k; do
      [ -n "$k" ] || continue
      case " $bjoin " in
        *" $k "*) : ;;
        *) new_n=$((new_n + 1)); new_keys="${new_keys}${new_keys:+,}$k" ;;
      esac
    done <<< "$clusters"
  fi

  # ledger — the kernel's own kill counter (shape-only, never window-scoped)
  ledger=$(mem_field "$VMSTAT_FILE" oom_kill)
  case "$ledger" in '' | *[!0-9]*) ledger='-'; unk="${unk}ledger " ;; esac

  # verdict — a window scan unreadable is BLOCKED (the watch cannot be assessed at all); an
  # absent/unreadable baseline, a new cluster, a lost declared wave, or an unreadable ledger
  # is DEGRADED; only a fully measured window with no delta reads HEALTHY.
  if [ -n "$bad" ]; then
    OOM_V=BLOCKED
  elif [ "$base_state" = absent ] || [ "$base_state" = unreadable ] || [ "$new_n" -gt 0 ] \
    || [ "$missing" -gt 0 ] || [ -n "$unk" ]; then
    OOM_V=DEGRADED
  fi

  if [ "$base_state" = absent ] || [ "$base_state" = unreadable ]; then
    OOM_NOTE="window=boots=$boots $win_first..$win_last; C1_kernel=$k_n killed_process=$k_kill; C2_events=$a_n C3_events=$s_n clusters=$cluster_n${clist:+[$clist]}; base=$base_state [known/new/missing/out_of_window unknown]"
  else
    OOM_NOTE="window=boots=$boots $win_first..$win_last; C1_kernel=$k_n killed_process=$k_kill; C2_events=$a_n C3_events=$s_n clusters=$cluster_n${clist:+[$clist]}; base=$base_state known=$known${known_ids:+[$known_ids]} new=$new_n${new_keys:+[$new_keys]} missing=$missing${miss_keys:+[$miss_keys]} out_of_window=$oow${oow_keys:+[$oow_keys]}"
  fi
  OOM_NOTE="$OOM_NOTE; ledger=vmstat.oom_kill=$ledger${unk:+; unknown=[${unk% }]}; anchors=see drivers.mem; traps=presence-not-count,peak-not-datable,launch-not-live; rule=both-readings-carried; r8 vocab: kill-event-deep-r8.md §1"
  if [ -n "$bad" ]; then
    OOM_NOTE="scans unreadable:${bad% } [fails closed]; $OOM_NOTE"
  fi
  return 0
}

# ---- plane: journal / boot (this-boot triage) --------------------------------
probe_journal() {
  JRN_V=HEALTHY
  JRN_COREDUMPS=0
  local boots=0 cur=no lb_rc=0

  if ! have "$JOURNALCTL"; then
    JRN_V=BLOCKED
    JRN_NOTE='journalctl=missing (probe cannot run)'
    return
  fi

  # arm 1 — boot record: an index-0 (current boot) line must exist (SKILL.md:43)
  cap "$JOURNALCTL" --list-boots --no-pager
  lb_rc=$CAP_RC
  if [ "$lb_rc" -ne 0 ]; then
    JRN_V=BLOCKED
    JRN_NOTE="journalctl --list-boots rc=$lb_rc [boot record unreadable; fails closed]"
    return
  fi
  read -r boots cur < <(printf '%s\n' "$CAP_OUT" \
    | awk 'NF && $1 ~ /^-?[0-9]+$/ { n++; if ($1 == 0) c=1 } END { printf "%d %s\n", n+0, (c ? "yes" : "no") }')
  if [ "$cur" != yes ]; then
    JRN_V=BLOCKED
    JRN_NOTE="boot record missing: boots=$boots, no index-0 (current) line"
    return
  fi

  # arm 2 — boot target reached (SKILL.md:43 "no boot reaches graphical.target")
  local target=$BOOT_TARGET t_word='' t_rc=127
  if have "$SYSTEMCTL"; then
    cap "$SYSTEMCTL" is-active "$target" --no-pager
    t_rc=$CAP_RC
    t_word=${CAP_OUT%%$'\n'*}; t_word=${t_word//$'\r'/}; t_word=${t_word%"${t_word##*[![:space:]]}"}   # first line, no early reader (R45-C1)
  fi
  case "$t_word" in
    active) : ;;
    reloading | activating | inactive | deactivating | failed | maintenance | unknown | refreshing)
      JRN_V=BLOCKED
      JRN_NOTE="boot target $target=$t_word [boot did not reach $target] (is-active rc=$t_rc)"
      return
      ;;
    *)
      JRN_V=BLOCKED
      JRN_NOTE="boot target probe unusable rc=$t_rc [$(printf '%s' "$t_word" | cut -c1-80)]"
      return
      ;;
  esac

  # arm 3 — boot error entries, counted at ENTRY level (`-o json` lines); line counts are
  # traps (SKILL.md:217-220). Classes are disjoint: coredump > kernel > other.
  cap "$JOURNALCTL" -b -p err -o json --no-pager
  local e_rc=$CAP_RC err_n=0 cls='coredump=0 kernel=0 other=0'
  if [ "$e_rc" -ne 0 ]; then
    JRN_V=BLOCKED
    JRN_NOTE="err stream unreadable: journalctl -b -p err rc=$e_rc [fails closed; no fake pass]"
    return
  fi
  err_n=$(nlines "$CAP_OUT")
  if [ "$err_n" -eq 0 ]; then
    # an empty err stream is only a pass if the journal really holds entries this boot
    cap "$JOURNALCTL" -b -n 1 -o json --no-pager
    if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then
      JRN_V=BLOCKED
      JRN_NOTE='journal empty/unreadable this boot (no entries; clean vs no-data cannot be told apart)'
      return
    fi
  else
    # One pass over the captured boot-0 error stream; the class counts are published twice:
    # `cls` is the PLANE journal note text (unchanged), and JRN_COREDUMPS is the boot-0
    # coredump count the ADJ-04 handoff line carries.
    local cls_n='' cd_n=0 kd_n=0 ot_n=0
    cls_n=$(printf '%s\n' "$CAP_OUT" | awk '
      /"SYSLOG_IDENTIFIER":"systemd-coredump"/ { c++; next }
      /"SYSLOG_IDENTIFIER":"kernel"|"_TRANSPORT":"kernel"/ { k++; next }
      { o++ }
      END { printf "%d %d %d", c+0, k+0, o+0 }')
    read -r cd_n kd_n ot_n <<< "$cls_n"
    cls="coredump=$cd_n kernel=$kd_n other=$ot_n"
    JRN_COREDUMPS=$cd_n
  fi

  # arm 4 — failed services HISTORY this boot (journal-derived: units that failed earlier
  # and were reset since are still named; the systemd plane owns the current failed set)
  local fh_n=0 fh_names=''
  fh_n=$(printf '%s\n' "$CAP_OUT" | grep -cE "\"MESSAGE\":\"[^\"]*(${CLASS_FAILED})" || true)
  if [ "$fh_n" -gt 0 ]; then
    fh_names=$(printf '%s\n' "$CAP_OUT" \
      | grep -E "\"MESSAGE\":\"[^\"]*(${CLASS_FAILED})" \
      | grep -oE '[A-Za-z0-9_.@-]+\.(service|socket|timer|mount|target|device|path|scope|slice)' \
      | sort -u | head -n 6 | paste -sd, - || true)
  fi

  # arm 5 — timer drift: every enabled user timer must be armed (ActiveState=active).
  # An unreadable probe is an unresolved unknown -> DEGRADED (mirrors the systemd plane's
  # unreadable-Result semantics), never a silent pass.
  local te=0 ts=0 armed=0 drift=0 t_unknown=0 bad='' r t timers=()
  cap "$SYSTEMCTL" --user list-unit-files --type=timer --state=enabled --no-legend --no-pager
  if [ "$CAP_RC" -ne 0 ]; then
    JRN_V=DEGRADED
    JRN_NOTE="boots=$boots current=$cur target=$target:$t_word err=$err_n ($cls); failedhist=$fh_n${fh_names:+[$fh_names]}; timer plane unreadable [drift unknown]"
    return
  fi
  te=$(printf '%s\n' "$CAP_OUT" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | wc -l)
  mapfile -t timers < <(printf '%s\n' "$CAP_OUT" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | head -n "$TIMER_SCAN_MAX")
  ts=${#timers[@]}
  for t in "${timers[@]}"; do
    cap "$SYSTEMCTL" --user show "$t" -p ActiveState --value --no-pager
    r=${CAP_OUT%%$'\n'*}; r=${r//$'\r'/}; r=${r%"${r##*[![:space:]]}"}   # first line, no early reader (R45-C1)
    if [ "$CAP_RC" -ne 0 ] || [ -z "$r" ]; then
      t_unknown=$((t_unknown + 1))
    elif [ "$r" = active ]; then
      armed=$((armed + 1))
    else
      drift=$((drift + 1))
      bad="${bad}${t}=${r} "
    fi
  done

  JRN_NOTE="boots=$boots current=$cur target=$target:$t_word err=$err_n ($cls); failedhist=$fh_n${fh_names:+[$fh_names]}; timers_enabled=$te timers_scanned=$ts armed=$armed timer_drift=$drift timer_unknown=$t_unknown"
  [ -n "$bad" ] && JRN_NOTE="$JRN_NOTE (${bad% })"

  if [ "$err_n" -gt 0 ] || [ "$fh_n" -gt 0 ] || [ "$drift" -gt 0 ] || [ "$t_unknown" -gt 0 ]; then JRN_V=DEGRADED; fi
  return
}

# ---- helper: repo-side version join ------------------------------------------
version_join() { # stdin: installed name<TAB>version rows, a __MAP__ line, then repo-side
  # name<TAB>version rows. stdout: one `D<TAB>name<TAB>installed<TAB>repo` line per
  # version difference, then `S<TAB>equal<TAB>diff<TAB>installed_n`. First occurrence wins
  # on the repo side (the caller feeds it in pacman's own repo order).
  awk -F'\t' '
    $0 == "__MAP__" { inmap = 1; next }
    !inmap { if (NF >= 2) { inst[$1] = $2; n++ } ; next }
    { if (!($1 in rv)) rv[$1] = $2 }
    END {
      e = 0; d = 0
      for (k in inst) {
        if (k in rv) {
          if (rv[k] == inst[k]) e++
          else { d++; print "D\t" k "\t" inst[k] "\t" rv[k] }
        }
      }
      printf "S\t%d\t%d\t%d\n", e, d, n
    }'
}

# ---- plane: update-safety (round 9, lane S9-1) --------------------------------
# The fifth owned surface: what an `-Syu` would touch, and whether that question can be
# answered read-only at all. Vocabulary and composition are the r2 note's (:334-339,
# restated at SKILL.md:358-368): PASS · INERT · REQUIRES-PREP · BLOCKED · UNKNOWN-UPSTREAM ·
# DO-NOT — strongest fired wins, BLOCKED > UNKNOWN-UPSTREAM > REQUIRES-PREP > INERT > PASS.
# The composed word is printed as `status=` together with its firing rows, so a non-author
# can re-derive it. Gate-verdict mapping (recorded in the header, not silently applied):
# BLOCKED -> BLOCKED; UNKNOWN-UPSTREAM / REQUIRES-PREP -> DEGRADED; INERT -> HEALTHY; the
# exposure fold can only worsen (`worse`), never lift a BLOCKED probe. Anti-claim: nothing
# here mutates — `-Qu`, `-Sup`/`-Suu --print-format` (plan verbs), `-Q`, `-Sl`, `expac -S`,
# `stat` and bounded log tail reads; no `-Sy`, no transaction, no download, no db write, no
# AUR RPC, no external site (PROVINCE.md:16-17).
probe_update_safety() {
  UPD_V=HEALTHY
  local now qu_rc=0 qu_n=0 qu_state='' sup_rc=0 sup_n=0 suu_rc=0 suu_n=0 suu_first=''
  local cand=0 cand_names='' disagree='' status='' pend='none' trap_row=''
  local sy_dir="$PACMAN_DB/sync" chan_n=0 fetch_d='?' stamp_d='?' stamp_unk='' chan_row=''
  local f base mt_y b_ep oldest='' newest=''
  local q_rc=0 sl_rc=0 equal=0 diff_unk=0 behind=0 ahead=0 behind_names=''
  local join_row='' join_src='' expac_row='' m_join='' pair_out='' cl_out='' oe=0 au=0
  local unk_names='' offline_row='' log_row='' refresh_row='' class_row='' dir=''

  case "$CHANNEL_MAX_AGE_D" in '' | *[!0-9]*) CHANNEL_MAX_AGE_D=7 ;; esac

  if ! have "$PACMAN"; then
    UPD_V=BLOCKED
    UPD_NOTE='status=BLOCKED; pacman=missing (probe cannot run)'
    return
  fi
  if [ -e "$PACMAN_DB/db.lck" ]; then
    UPD_V=BLOCKED
    UPD_NOTE='status=BLOCKED; db.lck=present — interrupted transaction (SKILL.md:41,45)'
    return
  fi
  now=$(date +%s)

  # --- channel reading: repo dbs under $PACMAN_DB/sync. Birth = the local fetch instant
  # (`%W`); content stamp = the db file's mtime (`%Y`), which is upstream's own file stamp
  # preserved at download — the freshness that matters. offline.db is excluded: it is the
  # offline-exile preservation archive, not a configured repo.
  for f in "$sy_dir"/*.db; do
    [ -e "$f" ] || continue
    base=${f##*/}
    [ "$base" = "$CHANNEL_ARCHIVE" ] && continue
    chan_n=$((chan_n + 1))
    mt_y=$(stat -c %Y -- "$f" 2>/dev/null || true)
    case "$mt_y" in
      '' | *[!0-9]*) stamp_unk="${stamp_unk}${base} " ;;
      *) if [ -z "$oldest" ] || [ "$mt_y" -lt "$oldest" ]; then oldest=$mt_y; fi ;;
    esac
    b_ep=$(stat -c %W -- "$f" 2>/dev/null || true)
    case "$b_ep" in
      '' | 0 | - | *[!0-9]*) : ;;
      *) if [ -z "$newest" ] || [ "$b_ep" -gt "$newest" ]; then newest=$b_ep; fi ;;
    esac
  done
  [ -n "$oldest" ] && stamp_d=$(( (now - oldest) / 86400 ))
  [ -n "$newest" ] && fetch_d=$(( (now - newest) / 86400 ))
  if [ "$chan_n" -eq 0 ]; then
    chan_row='dbs=0 [no repo *.db under sync/ — an empty candidate set cannot be told from an up-to-date one]'
  else
    chan_row="dbs=$chan_n fetch=${fetch_d}d stamp=${stamp_d}d"
    [ -n "$stamp_unk" ] && chan_row="$chan_row stamp_unreadable=[${stamp_unk% }]"
  fi

  # --- candidate set: `-Qu` UNPIPED (rc/emptiness; any other shape = unreadable, never
  # INERT — the pipeline-rc trap) cross-checked against the one allowed plan verb.
  cap "$PACMAN" -Qu
  qu_rc=$CAP_RC
  qu_n=$(nlines "$CAP_OUT")
  if [ "$qu_rc" -eq 1 ] && [ "$qu_n" -eq 0 ]; then
    qu_state='empty'
  elif [ "$qu_rc" -eq 0 ] && [ "$qu_n" -gt 0 ]; then
    qu_state='cand'
  else
    qu_state='unreadable'
  fi
  if [ "$qu_state" = 'unreadable' ]; then
    UPD_V=BLOCKED
    UPD_NOTE="status=BLOCKED; qu=rc=$qu_rc/$qu_n [pacman -Qu unreadable — never INERT]; chan=$chan_row"
    return
  fi
  if [ "$qu_state" = 'cand' ]; then
    cand=$qu_n
    cand_names=$(printf '%s\n' "$CAP_OUT" | awk 'NR <= 3 {print $1}' | paste -sd, -)
  fi

  cap "$PACMAN" -Sup --print-format '%r/%n %v'
  sup_rc=$CAP_RC
  if [ "$sup_rc" -ne 0 ]; then
    UPD_V=BLOCKED
    UPD_NOTE="status=BLOCKED; sup=rc=$sup_rc [pacman -Sup --print-format unreadable — candidate set not confirmable]; qu=rc=$qu_rc/$qu_n; chan=$chan_row"
    return
  fi
  sup_n=$(nlines "$CAP_OUT")
  if [ "$qu_state" = 'empty' ] && [ "$sup_n" -gt 0 ]; then
    disagree=" disagree[qu=0 sup=$sup_n]"
    cand=$sup_n
    cand_names=$(printf '%s\n' "$CAP_OUT" \
      | awk 'NR <= 3 {n=$1; sub(/^[^/]+\//, "", n); print n}' | paste -sd, -)
  elif [ "$qu_state" = 'cand' ] && [ "$sup_n" -ne "$qu_n" ]; then
    disagree=" disagree[qu=$qu_n sup=$sup_n]"
    if [ "$sup_n" -gt "$cand" ]; then
      cand=$sup_n
      cand_names=$(printf '%s\n' "$CAP_OUT" \
        | awk 'NR <= 3 {n=$1; sub(/^[^/]+\//, "", n); print n}' | paste -sd, -)
    fi
  fi

  # --- trap row (verb-level DO-NOT; verdict-neutral — r2 table row 11, kept as note
  # content by plans/round-7.plan.md:95-97).
  cap "$PACMAN" -Suu --print-format '%r/%n %v'
  suu_rc=$CAP_RC
  if [ "$suu_rc" -eq 0 ]; then
    suu_n=$(nlines "$CAP_OUT")
    [ "$suu_n" -gt 0 ] && suu_first=$(printf '%s\n' "$CAP_OUT" | awk 'NR == 1' | tr -d '\r')
    trap_row="-Suu:${suu_n}${suu_first:+[$suu_first]}"
  else
    trap_row="-Suu:unreadable(rc=$suu_rc)"
  fi

  # --- offline.db: presence/birth/stamp only; the fold's rows come from the register
  if [ -e "$OFFLINE_DB" ]; then
    local off_y off_b off_d off_bd
    off_y=$(stat -c %Y -- "$OFFLINE_DB" 2>/dev/null || true)
    off_b=$(stat -c %W -- "$OFFLINE_DB" 2>/dev/null || true)
    case "$off_y" in '' | *[!0-9]*) off_d='?' ;; *) off_d="$(( (now - off_y) / 86400 ))d" ;; esac
    case "$off_b" in '' | 0 | - | *[!0-9]*) off_bd='?' ;; *) off_bd="$(( (now - off_b) / 86400 ))d" ;; esac
    offline_row="present(stamp=$off_d birth=$off_bd)"
  else
    offline_row='absent'
  fi

  # --- bounded log tail: the command class only. A window miss is printed, never smoothed
  # into a claim about the host.
  if [ -r "$PACMAN_LOG" ]; then
    local tail_txt last_run l_ts l_cmd last_ref
    tail_txt=$(tail -n "$LOG_TAIL_N" -- "$PACMAN_LOG" 2>/dev/null || true)
    last_run=$(printf '%s\n' "$tail_txt" | grep -E "\[PACMAN\] Running '" | tail -n1 || true)
    if [ -n "$last_run" ]; then
      l_ts=$(printf '%s\n' "$last_run" | sed -nE 's/^\[([^]]+)\].*/\1/p')
      l_cmd=$(printf '%s\n' "$last_run" | sed -nE "s/.*Running 'pacman ([^ ']+).*/\1/p")
      log_row="cmd=${l_cmd:-?}@${l_ts:-?}"
    else
      log_row="cmd=unknown [window miss: no Running line in the last $LOG_TAIL_N lines]"
    fi
    last_ref=$(printf '%s\n' "$tail_txt" | grep -E "\[PACMAN\] Running 'pacman -S[^ ']*[yu]" | tail -n1 || true)
    if [ -n "$last_ref" ]; then
      refresh_row="$(printf '%s\n' "$last_ref" | sed -nE "s/.*Running 'pacman ([^ ']+).*/\1/p")@$(printf '%s\n' "$last_ref" | sed -nE 's/^\[([^]]+)\].*/\1/p')"
    else
      refresh_row="none-in-window(last $LOG_TAIL_N lines)"
    fi
  else
    log_row='unreadable'
    refresh_row='unreadable'
  fi

  # --- third reading: the repo-side version join. `pacman -Sl`, first occurrence per name
  # = pacman's own repo order (the r2 note's last-wins `expac` trap, :403-411); `expac -S`
  # cross-checks when present; `vercmp` gives direction. Absence is always printed.
  cap "$PACMAN" -Q
  q_rc=$CAP_RC
  local q_live="$CAP_OUT"
  cap "$PACMAN" -Sl
  sl_rc=$CAP_RC
  if [ "$q_rc" -ne 0 ] || [ "$sl_rc" -ne 0 ]; then
    join_row="unavailable(q=rc=$q_rc sl=rc=$sl_rc)"
    expac_row='n/a(join unavailable)'
  else
    m_join=$(printf '%s\n' "$CAP_OUT" | awk 'NF >= 3 && !seen[$2]++ { print $2 "\t" $3 }')
    pair_out=$( { printf '%s\n' "$q_live" | awk 'NF >= 2 { print $1 "\t" $2 }'
                  printf '__MAP__\n'
                  printf '%s\n' "$m_join"; } | version_join )
    local s_line
    s_line=$(printf '%s\n' "$pair_out" | grep '^S' | tail -n1 || true)
    equal=$(printf '%s' "$s_line" | cut -f2); equal=${equal:-0}
    while IFS=$'\t' read -r tag dn dv rv; do
      [ "$tag" = 'D' ] || continue
      if have "$VERCMP"; then
        dir=$("$VERCMP" "$dv" "$rv" 2>/dev/null || true)
      else
        dir='?'
      fi
      case "$dir" in
        '-1') behind=$((behind + 1)); [ "$behind" -le 6 ] && behind_names="$behind_names $dn" ;;
        '1') ahead=$((ahead + 1)) ;;
        *) diff_unk=$((diff_unk + 1)) ;;
      esac
      [ "$((behind + ahead))" -ge 40 ] && break
    done <<< "$pair_out"
    if have "$EXPAC"; then
      cap "$EXPAC" -S "$EXPAC_FMT"
      if [ "$CAP_RC" -eq 0 ] && [ -n "$(printf '%s' "$CAP_OUT" | tr -d '[:space:]')" ]; then
        local e_join e_out e_behind=0 e_ahead=0 e_unk=0
        e_join=$(printf '%s\n' "$CAP_OUT" | awk -F'\t' 'NF >= 2 && !seen[$1]++ { print $1 "\t" $2 }')
        e_out=$( { printf '%s\n' "$q_live" | awk 'NF >= 2 { print $1 "\t" $2 }'
                   printf '__MAP__\n'
                   printf '%s\n' "$e_join"; } | version_join )
        while IFS=$'\t' read -r tag dn dv rv; do
          [ "$tag" = 'D' ] || continue
          if have "$VERCMP"; then
            dir=$("$VERCMP" "$dv" "$rv" 2>/dev/null || true)
          else
            dir='?'
          fi
          case "$dir" in
            '-1') e_behind=$((e_behind + 1)) ;;
            '1') e_ahead=$((e_ahead + 1)) ;;
            *) e_unk=$((e_unk + 1)) ;;
          esac
        done <<< "$e_out"
        if [ "$e_unk" -gt 0 ]; then
          expac_row='partial'
        elif [ "$e_behind" -eq "$behind" ] && [ "$e_ahead" -eq "$ahead" ]; then
          expac_row='agree'
        else
          expac_row="disagree(behind=$e_behind ahead=$e_ahead)"
          [ "$e_behind" -gt "$behind" ] && behind=$e_behind
        fi
        join_src='sl+expac'
      else
        expac_row="rc=$CAP_RC"
        join_src='sl'
      fi
    else
      expac_row='absent'
      join_src='sl'
    fi
    join_row="equal=$equal behind=$behind ahead=$ahead src=$join_src"
    [ "$diff_unk" -gt 0 ] && join_row="$join_row diff_unclassifiable=$diff_unk"
    [ -n "$behind_names" ] && join_row="$join_row behind_names=[${behind_names# }]"
  fi

  # --- risk-class fold (exposure only): the SAME-process `pacman -Qm` reading joined
  # against the register's classes. An absent/unreadable baseline is never a pass.
  if [ "$PKG_FOREIGN_FOLD" != 'ok' ]; then
    class_row="unavailable(${PKG_FOREIGN_FOLD})"
  else
    if [ -n "$PKG_FOREIGN_LIVE" ]; then
      cl_out=$(awk 'NR == FNR { if (NF >= 2) cls[$1] = $2; next } NF { if ($1 in cls) print cls[$1]; else print "?" $1 }' \
        <(printf '%s\n' "$R6_FOREIGN_CLASSES") <(printf '%s\n' "$PKG_FOREIGN_LIVE" | tr ' ' '\n'))
      oe=$(printf '%s\n' "$cl_out" | grep -c '^offline-exile$' || true)
      au=$(printf '%s\n' "$cl_out" | grep -c '^aur-local$' || true)
      unk_names=$(printf '%s\n' "$cl_out" | grep '^?' | sed 's/^?//' | head -n6 | paste -sd, - || true)
    fi
    class_row="offline-exile:$oe,aur-local:$au"
    [ -n "$unk_names" ] && class_row="$class_row unknown-provenance=[$unk_names]"
  fi

  # --- composition (strongest fired arm wins) and the recorded verdict mapping
  if [ "$chan_n" -eq 0 ]; then
    status='BLOCKED'
  elif [ -n "$stamp_unk" ] || [ "$stamp_d" = '?' ]; then
    status='UNKNOWN-UPSTREAM'
  elif [ "$stamp_d" -gt "$CHANNEL_MAX_AGE_D" ]; then
    status='UNKNOWN-UPSTREAM'
  elif [ "$cand" -gt 0 ] || [ "$behind" -gt 0 ]; then
    status='REQUIRES-PREP'
  else
    status='INERT'
  fi
  if [ "$cand" -gt 0 ] || [ "$behind" -gt 0 ]; then
    pend="REQUIRES-PREP(candidates=$cand join_behind=$behind${cand_names:+ names=[$cand_names]})"
  fi

  case "$status" in
    BLOCKED) UPD_V=BLOCKED ;;
    UNKNOWN-UPSTREAM | REQUIRES-PREP) UPD_V=DEGRADED ;;
    INERT) UPD_V=HEALTHY ;;
    *) UPD_V=DEGRADED ;;
  esac
  if [ "$PKG_FOREIGN_FOLD" != 'ok' ] || [ -n "$unk_names" ]; then
    UPD_V=$(worse "$UPD_V" DEGRADED)
  fi

  UPD_NOTE="status=$status; pending=$pend; qu=rc=$qu_rc/$qu_n; sup=$sup_n$disagree; join=$join_row; expac=$expac_row; chan=$chan_row; offline.db=$offline_row; log=$log_row; refresh=$refresh_row; classes=$class_row; trap=$trap_row; traps=[-Qu blind to shadowed-newer; '%s' is not a size]; vocab: SKILL.md:358-368"
  return
}

# ---- pacnew/pacsave drift arm (round 35, C1; contract in the header) ---------------
probe_pacnew_arm() {
  local etc=$ETC_DIR log=$PACMAN_LOG fs='' err='' ln='' ls='' host='' tg='' lk='' l d t under
  local total=0 pn=0 ps=0 po=0 unr=0 lpn=0 lps=0 unl=0 gone=0 lstate=ok
  fs=$(LC_ALL=C find "$etc" ! -type d \( -name '*.pacnew' -o -name '*.pacsave' -o -name '*.pacsave.[0-9]*' -o -name '*.pacorig' \) -print 2>/dev/null || true)
  err=$(LC_ALL=C find "$etc" -type d -print 2>&1 >/dev/null || true)
  if [ -n "$fs" ]; then
    total=$(printf '%s\n' "$fs" | wc -l)
    pn=$(printf '%s\n' "$fs" | grep -c '\.pacnew$' || true)
    po=$(printf '%s\n' "$fs" | grep -c '\.pacorig$' || true)
    ps=$((total - pn - po))
    host=$(while IFS= read -r l; do printf '/etc/%s\n' "${l#"$etc"/}"; done <<< "$fs" | LC_ALL=C sort -u)
  fi
  if [ -n "$err" ]; then
    unr=$(printf '%s\n' "$err" | grep -c ': Permission denied$' || true)
    while IFS= read -r l; do
      case "$l" in
        "find: '$etc/"*"': Permission denied")
          d=${l#"find: '$etc/"}; lk+="/etc/${d%"': Permission denied"}/"$'\n' ;;
      esac
    done <<< "$err"
  fi
  if [ -r "$log" ]; then
    ln=$(LC_ALL=C grep -E '^\[[^]]*\] \[ALPM\] warning: (/etc/.+) installed as \1\.pacnew$' "$log" 2>/dev/null | sed -E 's/^.* installed as //' || true)
    ls=$(LC_ALL=C grep -E '^\[[^]]*\] \[ALPM\] warning: (/etc/.+) saved as \1\.pacsave$' "$log" 2>/dev/null | sed -E 's/^.* saved as //' || true)
  else
    lstate=unreadable
  fi
  [ -n "$ln" ] && lpn=$(printf '%s\n' "$ln" | wc -l)
  [ -n "$ls" ] && lps=$(printf '%s\n' "$ls" | wc -l)
  tg=$(printf '%s\n%s\n' "$ln" "$ls" | sed '/^$/d' | LC_ALL=C sort -u)
  if [ -n "$host" ]; then
    unl=$(LC_ALL=C comm -23 <(printf '%s\n' "$host") <(printf '%s\n' "$tg" | sed '/^$/d') | wc -l)
  fi
  if [ -n "$tg" ]; then
    while IFS= read -r t; do
      [ -n "$host" ] && grep -qxF -- "$t" <<< "$host" && continue
      under=0
      while IFS= read -r d; do
        [ -n "$d" ] || continue
        case "$t" in "$d"*) under=1 ;; esac
      done <<< "$lk"
      [ "$under" -eq 1 ] || gone=$((gone + 1))
    done <<< "$tg"
  fi
  DRIFT_LINE="DRIFT pacnew-plane pacnew=$pn pacsave=$ps pacorig=$po unreadable=$unr log_pacnew=$lpn log_pacsave=$lps unlogged=$unl gone=$gone log=$lstate"
}

# ---- storage-integrity arm (round 38, C1; contract in the header) -------------------
probe_storage_arm() {
  local root=$BTRFS_SYSFS fsd dev f k v extra fs8 fsn=0 devn=0 nz=0 blocked=0 nd seen nk dnz ddet detail=''
  local uuid='^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
  local keys=' write_errs read_errs flush_errs corruption_errs generation_errs '
  if [ -d "$root" ] && { [ ! -r "$root" ] || [ ! -x "$root" ]; }; then
    # an existing but unlistable root must not read as "no btrfs filesystem" (round-38 W1
    # C1RevSharedState): the glob would expand to nothing and print a silent HEALTHY 0/0/0
    blocked=1; detail+='root:unreadable,'
  elif [ -d "$root" ]; then
    for fsd in "$root"/*; do
      [ -e "$fsd" ] || continue
      [[ ${fsd##*/} =~ $uuid ]] || continue
      fsn=$((fsn + 1)); nd=0; fs8=${fsd##*/}; fs8=${fs8:0:8}
      for dev in "$fsd"/devinfo/*; do
        [ -e "$dev" ] || continue
        nd=$((nd + 1)); devn=$((devn + 1)); f=$dev/error_stats
        # kernel devids are decimal integers; any other entry name is never echoed into the
        # one-line grammar (round-38 W1 C1SentGrammar: a newline in a name forged census lines)
        if ! [[ ${dev##*/} =~ ^[0-9]+$ ]]; then blocked=1; detail+="$fs8:?:bad-devid,"; continue; fi
        if [ ! -f "$f" ] || [ ! -r "$f" ]; then
          blocked=1; detail+="$fs8:${dev##*/}:unreadable,"; continue
        fi
        # a device counts only when its file carries each of the five counters exactly once,
        # as a non-negative integer, and nothing else; its nonzero pairs count only then
        seen=' ' nk=0 dnz=0 ddet=''
        while IFS=' ' read -r k v extra || [ -n "${k:-}" ]; do
          if [[ $keys != *" ${k:-} "* ]] || [ -n "${extra:-}" ] || ! [[ ${v:-} =~ ^[0-9]+$ ]] \
            || [[ $seen == *" $k "* ]]; then
            nk=-1; break
          fi
          seen+="$k "; nk=$((nk + 1))
          if ! [[ $v =~ ^0+$ ]]; then dnz=$((dnz + 1)); ddet+="$fs8:${dev##*/}:$k=$v,"; fi
        done < "$f"
        if [ "$nk" -ne 5 ]; then
          blocked=1; detail+="$fs8:${dev##*/}:malformed,"; continue
        fi
        nz=$((nz + dnz)); detail+=$ddet
      done
      if [ "$nd" -eq 0 ]; then blocked=1; detail+="$fs8:-:no-devinfo,"; fi
    done
  fi
  if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]; then
    # round 39 (R38-ABSENT-ROOT): no fsid under the root is "no btrfs" only if no btrfs is mounted
    local mtab mt=0 _src _mp fst _rest
    # round-39 W1 hardening (C1SentMounts): only a regular, non-empty file is a mount table — a FIFO
    # would block the census forever, and an empty file or /dev/null is never a real table (/ is mounted)
    if [ -f "$PROC_MOUNTS" ] && mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null) && [ -n "$mtab" ]; then
      while read -r _src _mp fst _rest; do
        if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi
      done <<< "$mtab"
      if [ "$mt" -gt 0 ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; fi
    else
      blocked=1; detail+='mounts:unreadable,'
    fi
  fi
  local state=HEALTHY
  if [ "$blocked" -eq 1 ]; then state=BLOCKED; elif [ "$nz" -gt 0 ]; then state=DEGRADED; fi
  STORAGE_LINE="STORAGE btrfs-device-stats state=$state filesystems=$fsn devices=$devn nonzero=$nz"
  if [ -n "$detail" ]; then STORAGE_LINE+=" detail=${detail%,}"; fi
  return 0
}

# ---- scrub-record arm (round 44, C1; contract in the header) ----------------------------
probe_scrub_record() {
  local LC_ALL=C
  local dir=$SCRUB_DIR root=$BTRFS_SYSFS tw=$TIMER_WANTS fsd dev f v line nl e n fs8
  local uuid='[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
  local ds=absent sysok=0 fsids=' ' blocked=0 detail='' info=''
  local rec=0 tmp=0 sock=0 unr=0 orph=0 lim=0 tim=0
  # sysfs: which fsids are mounted now, and each device's scrub_speed_max (0 = no limit)
  if [ -d "$root" ] && { [ ! -r "$root" ] || [ ! -x "$root" ]; }; then
    blocked=1; detail+='sysfs:unreadable,'
  elif [ -d "$root" ]; then
    sysok=1
    for fsd in "$root"/*; do
      [ -e "$fsd" ] || continue
      [[ ${fsd##*/} =~ ^${uuid}$ ]] || continue
      fsids+="${fsd##*/} "; fs8=${fsd##*/}; fs8=${fs8:0:8}
      for dev in "$fsd"/devinfo/*; do
        [ -e "$dev" ] || continue
        if ! [[ ${dev##*/} =~ ^[0-9]+$ ]]; then blocked=1; detail+="$fs8:?:bad-devid,"; continue; fi
        f=$dev/scrub_speed_max
        if [ ! -f "$f" ] || [ ! -r "$f" ]; then blocked=1; detail+="$fs8:${dev##*/}:speed-unreadable,"; continue; fi
        v='' nl=0
        while IFS= read -r line || [ -n "$line" ]; do nl=$((nl + 1)); v=$line; done < "$f"
        if [ "$nl" -ne 1 ] || ! [[ $v =~ ^[0-9]+$ ]]; then
          blocked=1; detail+="$fs8:${dev##*/}:speed-malformed,"; continue
        fi
        if ! [[ $v =~ ^0+$ ]]; then lim=$((lim + 1)); info+="$fs8:${dev##*/}:speed_max=$v,"; fi
      done
    done
  fi
  # the record directory: names and stat only, never content
  if [ -e "$dir" ] || [ -L "$dir" ]; then
    if [ ! -d "$dir" ] || [ ! -r "$dir" ] || [ ! -x "$dir" ]; then
      ds=unreadable; blocked=1; detail+='dir:unreadable,'
    else
      ds=present
      for e in "$dir"/scrub.*; do
        [ -e "$e" ] || [ -L "$e" ] || continue
        n=${e##*/}
        if [[ $n =~ ^scrub\.status\.(${uuid})$ ]]; then
          if [ -L "$e" ] || [ ! -f "$e" ]; then blocked=1; detail+='record:not-regular,'; continue; fi
          rec=$((rec + 1))
          [ -r "$e" ] || unr=$((unr + 1))
          if [ "$sysok" -eq 1 ] && [[ $fsids != *" ${BASH_REMATCH[1]} "* ]]; then orph=$((orph + 1)); fi
        elif [[ $n =~ ^scrub\.status\.${uuid}_tmp$ ]]; then
          if [ -L "$e" ] || [ ! -f "$e" ]; then blocked=1; detail+='tmp:not-regular,'; continue; fi
          tmp=$((tmp + 1))
          [ -r "$e" ] || unr=$((unr + 1))
        elif [[ $n =~ ^scrub\.progress\.${uuid}$ ]]; then
          if [ -L "$e" ] || [ ! -S "$e" ]; then blocked=1; detail+='progress:not-socket,'; continue; fi
          sock=$((sock + 1))
        fi
      done
      if [ "$rec" -gt 0 ] && [ "$sysok" -eq 0 ]; then
        if [ -d "$root" ]; then :   # an unlistable dir was already flagged sysfs:unreadable above
        elif [ -e "$root" ] || [ -L "$root" ]; then blocked=1; detail+='sysfs:not-directory,'
        else blocked=1; detail+='sysfs:absent,'; fi
      fi
    fi
  fi
  # enabled scrub timer instances: the links `systemctl enable btrfs-scrub@<inst>.timer` makes
  if [ -e "$tw" ] || [ -L "$tw" ]; then
    if [ ! -d "$tw" ] || [ ! -r "$tw" ] || [ ! -x "$tw" ]; then
      blocked=1; detail+='timers:unreadable,'
    else
      for e in "$tw"/btrfs-scrub@*.timer; do
        [ -e "$e" ] || [ -L "$e" ] || continue
        [ "${e##*/}" != 'btrfs-scrub@.timer' ] || continue
        [ -d "$e" ] && continue
        tim=$((tim + 1))
      done
    fi
  fi
  local state=NONE
  if [ "$blocked" -eq 1 ]; then state=BLOCKED; elif [ $((rec + tmp + sock)) -gt 0 ]; then state=RECORDED; fi
  SCRUB_LINE="SCRUB btrfs-scrub-record state=$state dir=$ds records=$rec tmp=$tmp sockets=$sock unreadable=$unr orphan=$orph limited=$lim timers=$tim"
  detail+=$info
  if [ -n "$detail" ]; then SCRUB_LINE+=" detail=${detail%,}"; fi
  return 0
}

# ---- hermetic selftest -------------------------------------------------------
run_selftest() {
  local bin fx
  work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")
  # A 000 fixture directory would block `rm -rf` (unlink needs write+search on the parent);
  # restore permissions on the temp tree only, never on a live path.
  trap 'chmod -R u+rwx -- "${work:-}" 2>/dev/null || true; rm -rf -- "${work:-}" 2>/dev/null || true' EXIT INT TERM
  bin="$work/bin"
  mkdir -p "$bin" "$work/fx"

  cat > "$bin/.dispatch" <<'STUB'
#!/usr/bin/env bash
# tsukuroi-census selftest fixture dispatcher; answers from $TSUKUROI_FIXTURE only.
set -uo pipefail
name=${0##*/}
fix=${TSUKUROI_FIXTURE:-}
[ -n "$fix" ] || { printf 'fixture dispatcher: TSUKUROI_FIXTURE unset\n' >&2; exit 97; }
rc_of() { local f="$fix/$1.rc"; if [ -f "$f" ]; then cat "$f"; else printf 0; fi; }
out_of() { local f="$fix/$1"; if [ -f "$f" ]; then cat "$f"; fi; }
args="$*"
case "$name" in
  pacman)
    case "${1:-}" in
      -Q) out_of q; exit "$(rc_of q)" ;;
      -Qq) out_of pq; exit "$(rc_of pq)" ;;
      -Qm) out_of pm; exit "$(rc_of pm)" ;;
      -Qkk) out_of qkk.out; exit "$(rc_of qkk)" ;;
      -Qu) out_of qu; exit "$(rc_of qu)" ;;
      -Sup) out_of sup; exit "$(rc_of sup)" ;;
      -Suu) out_of suu; exit "$(rc_of suu)" ;;
      -Sl) out_of sl; exit "$(rc_of sl)" ;;
      *) printf 'fixture pacman: unexpected args: %s\n' "$args" >&2; exit 64 ;;
    esac
    ;;
  expac)
    case "${1:-}" in
      -S) out_of expacsl; exit "$(rc_of expacsl)" ;;
      *) printf 'fixture expac: unexpected args: %s\n' "$args" >&2; exit 64 ;;
    esac
    ;;
  pacman-conf) out_of pconf; exit "$(rc_of pconf)" ;;
  systemctl)
    case "$args" in
      *is-system-running*) out_of sysrunning; exit "$(rc_of sysrunning)" ;;
      *is-active*) out_of boottarget; exit "$(rc_of boottarget)" ;;
      *list-units*failed*) out_of failedunits; exit "$(rc_of failedunits)" ;;
      *list-unit-files*) out_of timerlist; exit "$(rc_of timerlist)" ;;
      *show*ActiveState*) out_of timeractivestate; exit "$(rc_of timeractivestate)" ;;
      *show*Result*) out_of timerresult; exit "$(rc_of timerresult)" ;;
      *) printf 'fixture systemctl: unexpected args: %s\n' "$args" >&2; exit 64 ;;
    esac
    ;;
  dmesg)
    case "${1:-}" in
      --level*) out_of dmesg.out; exit "$(rc_of dmesg)" ;;
      *) out_of dmesg-all.out; exit "$(rc_of dmesg-all)" ;;
    esac
    ;;
  journalctl)
    case "$args" in
      *"-o short-iso-precise"*)
        # oom watch window scans (lane S9-2; separate fixture files from the arm's -b scans)
        case "$args" in
          *--grep*oom_reaper*) out_of oomwin-kernel; exit "$(rc_of oomwin-kernel)" ;;
          *--grep*"OOM killer"*) out_of oomwin-attrib; exit "$(rc_of oomwin-attrib)" ;;
          *--grep*"status=9"*) out_of oomwin-sigkill; exit "$(rc_of oomwin-sigkill)" ;;
          *) printf 'fixture journalctl: unexpected window args: %s\n' "$args" >&2; exit 64 ;;
        esac
        ;;
      *--grep*"OOM killer"*) out_of oom-attrib.json; exit "$(rc_of oom-attrib)" ;;
      *--grep*oom_reaper*) out_of oom-kernel.json; exit "$(rc_of oom-kernel)" ;;
      *--grep*"status=9"*) out_of oom-sigkill.json; exit "$(rc_of oom-sigkill)" ;;
      *"--list-boots"*) out_of listboots; exit "$(rc_of listboots)" ;;
      *"-p err"*) out_of journal-err.json; exit "$(rc_of journal-err)" ;;
      *"-n 1"*) out_of journal-last; exit "$(rc_of journal-last)" ;;
      *) out_of journal-all.json; exit "$(rc_of journal-all)" ;;
    esac
    ;;
  nvidia-smi) out_of smi.out; exit "$(rc_of smi)" ;;
  lsmod) out_of lsmod; exit "$(rc_of lsmod)" ;;
esac
printf 'fixture dispatcher: unknown command %s\n' "$name" >&2
exit 96
STUB
  chmod 700 "$bin/.dispatch"
  local c
  for c in pacman pacman-conf systemctl dmesg journalctl nvidia-smi lsmod expac; do
    ln -s .dispatch "$bin/$c"
  done

  PASS=0 FAIL=0
  ok() { PASS=$((PASS + 1)); printf 'PASS %s\n' "$*"; }
  bad() { FAIL=$((FAIL + 1)); printf 'FAIL %s\n' "$*" >&2; }
  skip() { printf 'SKIP %s\n' "$*"; }

  fx_default() { # clean fixture: everything passes, dmesg restricted like the measured host
    local d=$1
    mkdir -p "$d/pacmandb" "$d/pci" "$d/dev" "$d/root" "$d/etc"
    # Round-12 C1 fixture root: mode 0755 explicitly — umask 077 makes a bare mkdir 0700,
    # and the healthy-case regexes pin 0755, so an implicit mode would hide a mode leak.
    chmod 0755 "$d/root"
    printf 'alpha\nbeta\ngamma\ndelta\n' > "$d/pq"
    printf 'alpha: 10 total files, 0 altered files\nbeta: 20 total files, 0 altered files\n' > "$d/qkk.out"
    printf 0 > "$d/qkk.rc"
    : > "$d/pm"
    : > "$d/fbase"
    : > "$d/pconf"
    # round 39: the storage arm's mount table; no btrfs mount, so an absent sysfs root stays 0/0/0
    printf 'proc /proc proc rw,nosuid 0 0\n/dev/fx0 / ext4 rw,relatime 0 0\n' > "$d/mounts"
    # update-safety plane fixture (S9-1): a fresh 2-db channel, an empty candidate set at the
    # real `-Qu` rc (1 = none), the plan verbs empty, the joined sources agreeing, and a
    # bounded log window holding one non-refresh command.
    mkdir -p "$d/pacmandb/sync"
    : > "$d/pacmandb/sync/core.db"
    : > "$d/pacmandb/sync/omarchy.db"
    : > "$d/pacmandb/sync/offline.db"
    : > "$d/qu"; printf 1 > "$d/qu.rc"
    : > "$d/sup"; printf 0 > "$d/sup.rc"
    : > "$d/suu"; printf 0 > "$d/suu.rc"
    printf 'alpha 1.0-1\nbeta 2.0-1\n' > "$d/q"
    printf 'fixture alpha 1.0-1\nextra beta 2.0-1\n' > "$d/sl"
    printf 'alpha\t1.0-1\nbeta\t2.0-1\n' > "$d/expacsl"
    printf '%s\n' "[2026-10-13T16:37:58-0300] [PACMAN] Running 'pacman -S --needed --noconfirm fixture-pkg'" > "$d/pacman.log"
    printf 'HoldPkg = pacman glibc\n' > "$d/pacman.conf"
    printf 'running\n' > "$d/sysrunning"
    printf 0 > "$d/sysrunning.rc"
    : > "$d/failedunits"
    printf 'ai-usage.timer enabled enabled\n' > "$d/timerlist"
    printf 'success\n' > "$d/timerresult"
    printf 1 > "$d/dmesg.rc"
    : > "$d/dmesg.out"
    : > "$d/dmesg-all.out"
    printf 0 > "$d/dmesg-all.rc"
    : > "$d/journal-err.json"
    printf '{"MESSAGE":"fixture: kernel line 1"}\n{"MESSAGE":"fixture: kernel line 2"}\n{"MESSAGE":"fixture: kernel line 3"}\n' > "$d/journal-all.json"
    printf 0 > "$d/journal-err.rc"
    printf 0 > "$d/journal-all.rc"
    : > "$d/smi.out"
    printf 1 > "$d/smi.rc"
    : > "$d/lsmod"
    printf 'fixture-host\n' > "$d/hostname"
    printf 1 > "$d/dmesg_restrict"
    printf 'IDX BOOT ID                          FIRST ENTRY                 LAST ENTRY\n' > "$d/listboots"
    printf ' -1 73a8e2fc20cc48749b3cbd24ed5dc7c1 Sun 2026-10-11 19:02:51 -03 Tue 2026-10-13 10:57:30 -03\n' >> "$d/listboots"
    printf '  0 d7f0bc8d938e4249b4a1f250cbfacf58 Tue 2026-10-13 11:02:03 -03 Wed 2026-10-14 11:42:34 -03\n' >> "$d/listboots"
    printf 0 > "$d/listboots.rc"
    printf 'active\n' > "$d/boottarget"
    printf 0 > "$d/boottarget.rc"
    printf '{"MESSAGE":"fixture: journal last entry"}\n' > "$d/journal-last"
    printf 0 > "$d/journal-last.rc"
    printf 'active\n' > "$d/timeractivestate"
    printf 0 > "$d/timeractivestate.rc"
    # memory-pressure arm fixture (S7-2): quiet cgroup tree, PSI, meminfo and the three
    # journal `--grep` arms — the live host's shape (95 memory.events files) in miniature
    mkdir -p "$d/cgroup/user.slice/user-1000.slice/user@1000.service" "$d/pressure"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/memory.events"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/memory.events.local"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/user-1000.slice/memory.events"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/user-1000.slice/memory.events.local"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/user-1000.slice/user@1000.service/memory.events"
    printf 'high 0\nmax 0\nfail 0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.swap.events"
    printf '0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.swap.peak"
    printf 'pswpin 0\npswpout 0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.stat"
    printf 'max\n' > "$d/cgroup/user.slice/user-1000.slice/memory.max"
    printf 'max\n' > "$d/cgroup/user.slice/user-1000.slice/memory.high"
    printf '0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.oom.group"
    printf 'some avg10=0.00 avg60=0.00 avg300=0.00 total=0\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n' > "$d/pressure/memory"
    printf 'MemTotal: 1000000 kB\nMemAvailable: 900000 kB\nSwapTotal: 8000000 kB\nSwapFree: 8000000 kB\nShmem: 1000 kB\n' > "$d/meminfo"
    : > "$d/oom-kernel.json"; printf 0 > "$d/oom-kernel.rc"
    : > "$d/oom-attrib.json"; printf 0 > "$d/oom-attrib.rc"
    : > "$d/oom-sigkill.json"; printf 0 > "$d/oom-sigkill.rc"
    # oom watch fixture (S9-2): retained-window stubs — the boot list is the existing
    # listboots fixture; the scans default to "0 entries" (rc 1, the measured --grep
    # no-match semantics) and the kernel-kill ledger reads 0.
    printf 'oom_kill 0\n' > "$d/vmstat"
    : > "$d/obase"
    : > "$d/oomwin-kernel"; printf 1 > "$d/oomwin-kernel.rc"
    : > "$d/oomwin-attrib"; printf 1 > "$d/oomwin-attrib.rc"
    : > "$d/oomwin-sigkill"; printf 1 > "$d/oomwin-sigkill.rc"
  }

  fx_hash() { # tree digest: entry type/mode/owner/group AND regular-file content
    # Content-only hashing is blind to a chmod/ownership change on a fixture directory;
    # the root arm makes `$FX/root`'s mode an assertion target, so metadata must be inside
    # the zero-mutation proof. Permission errors on a 000 fixture dir are suppressed and
    # hash identically before/after.
    { find "$1" -printf '%y %m %U %G %p\n' 2>/dev/null || true
      find "$1" -type f -exec sha256sum {} + 2>/dev/null || true
    } | LC_ALL=C sort | sha256sum | cut -d' ' -f1
  }

  fx_no_mutation() { # assert the fixture tree is byte-identical after a census run
    local d=$1 before=$2 after
    after=$(fx_hash "$d")
    if [ "$after" != "$before" ]; then bad "fixture mutated by census run ($d)"; fi
  }

  EXTRA_ENV=()
  ROOT_EXPECT=''
  check() { # check LABEL WANT_RC WANT_VERDICT WANT_RE [WANT_RE...]
    # A WANT_RE prefixed with `ABSENT:` is a must-not-match assertion (round 32, C1: the
    # ADJ-04 handoff lines must be absent where no dated event was measured). Every other
    # WANT_RE is a must-match assertion, as before.
    local label=$1 wrc=$2 wverdict=$3
    shift 3
    local out rc before re miss='' unwanted='' pkgline root_expect=${ROOT_EXPECT:-$FX/root}
    before=$(fx_hash "$FX")
    set +e
    out=$(env \
      TSUKUROI_FIXTURE="$FX" \
      TSUKUROI_PACMAN="$bin/pacman" \
      TSUKUROI_PACMAN_CONF="$bin/pacman-conf" \
      TSUKUROI_PACMAN_CONF_FILE="$FX/pacman.conf" \
      TSUKUROI_PACMAN_DB="$FX/pacmandb" \
      TSUKUROI_ROOT_DIR="$FX/root" \
      TSUKUROI_FOREIGN_BASELINE="$FX/fbase" \
      TSUKUROI_SYSTEMCTL="$bin/systemctl" \
      TSUKUROI_DMESG="$bin/dmesg" \
      TSUKUROI_JOURNALCTL="$bin/journalctl" \
      TSUKUROI_NVIDIA_SMI="$bin/nvidia-smi" \
      TSUKUROI_LSMOD="$bin/lsmod" \
      TSUKUROI_PCI_SYSFS="$FX/pci" \
      TSUKUROI_DEV_DIR="$FX/dev" \
      TSUKUROI_HOSTNAME_FILE="$FX/hostname" \
      TSUKUROI_DMESG_RESTRICT_FILE="$FX/dmesg_restrict" \
      TSUKUROI_CGROUP_ROOT="$FX/cgroup" \
      TSUKUROI_MEM_SLICE='user.slice/user-1000.slice' \
      TSUKUROI_PRESSURE_FILE="$FX/pressure/memory" \
      TSUKUROI_MEMINFO_FILE="$FX/meminfo" \
      TSUKUROI_VMSTAT_FILE="$FX/vmstat" \
      TSUKUROI_OOM_BASELINE="$FX/obase" \
      TSUKUROI_PACMAN_LOG="$FX/pacman.log" \
      TSUKUROI_ETC_DIR="$FX/etc" \
      TSUKUROI_BTRFS_SYSFS="$FX/btrfs" \
      TSUKUROI_PROC_MOUNTS="$FX/mounts" \
      TSUKUROI_SCRUB_DIR="$FX/scrub" \
      TSUKUROI_TIMER_WANTS="$FX/wants" \
      TSUKUROI_EXPAC="$bin/expac" \
      "${EXTRA_ENV[@]}" \
      "$BASH" "$SELF" 2>&1)
    rc=$?
    set -e
    pkgline=$(printf '%s\n' "$out" | grep '^PLANE packages:' | head -n1 || true)
    if [ "$rc" -ne "$wrc" ]; then
      bad "$label: exit $rc wanted $wrc; output: $(printf '%s' "$out" | tail -n2 | tr '\n' '|')"
    elif ! printf '%s\n' "$out" | grep -q 'host=fixture-host'; then
      bad "$label: hostname override not honoured — possible host read"
    elif ! printf '%s\n' "$pkgline" | grep -qE '^PLANE packages: [A-Z]+ \(.*root_status=.*root_mode=.*root_dir='; then
      bad "$label: root metadata not composed into the packages line (blind spot survives?)"
    elif [[ "$pkgline" != *"root_dir=$root_expect "* && "$pkgline" != *"root_dir=$root_expect)" ]]; then
      bad "$label: configured root not asserted at a field boundary (wanted root_dir=$root_expect; possible live-root read)"
    elif ! printf '%s\n' "$out" | grep -qE "^TSUKUROI_CENSUS: ${wverdict} \("; then
      bad "$label: verdict not ${wverdict}; got: $(printf '%s\n' "$out" | grep '^TSUKUROI_CENSUS:' | head -n1)"
    else
      for re in "$@"; do
        case "$re" in
          ABSENT:*)
            if grep -qE -- "${re#ABSENT:}" <<<"$out"; then   # round 42: a SIGPIPE'd pipe here read 'absent' (fail-open)
              unwanted="$unwanted '${re#ABSENT:}'"
            fi
            ;;
          *)
            printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss '$re'"
            ;;
        esac
      done
      if [ -n "$miss" ]; then
        bad "$label: plane evidence missing:$miss; got: $(printf '%s\n' "$out" | grep '^PLANE ' | tr '\n' '|')"
      elif [ -n "$unwanted" ]; then
        bad "$label: evidence present that must be absent:$unwanted; got: $(printf '%s\n' "$out" | grep -E '^HANDOFF ' | tr '\n' '|')"
      else
        ok "$label (exit $rc, $wverdict)"
      fi
    fi
    fx_no_mutation "$FX" "$before"
    EXTRA_ENV=()
    ROOT_EXPECT=''
  }

  check_cli() { # check_cli LABEL WANT_RC RE... -- ARGS...; runs "$BASH" "$SELF" ARGS with no fixture env
    # (only arms that exit before any probe: usage errors and --help; never a host read)
    local label=$1 wrc=$2; shift 2
    local res=() out rc miss='' re
    while [ $# -gt 0 ] && [ "$1" != '--' ]; do res+=("$1"); shift; done
    [ "${1:-}" = '--' ] && shift
    set +e
    out=$("$BASH" "$SELF" "$@" 2>&1)
    rc=$?
    set -e
    if [ "$rc" -ne "$wrc" ]; then
      bad "$label: exit $rc wanted $wrc; output: $(printf '%s' "$out" | tail -n2 | tr '\n' '|')"
    else
      for re in "${res[@]}"; do
        printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss '$re'"
      done
      if [ -n "$miss" ]; then
        bad "$label: output missing:$miss"
      else
        ok "$label (exit $rc)"
      fi
    fi
  }

  local case_home='healthy'
  mkdir -p "$work/fx"
  FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: all planes pass' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*drift=0'

  case_home='healthy-gpu'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/pci/0000:01:00.0"; printf '0x10de\n' > "$FX/pci/0000:01:00.0/vendor"
  printf 'NVIDIA GeForce RTX 5070, 610.57.04\n' > "$FX/smi.out"; printf 0 > "$FX/smi.rc"
  printf 'nvidia 12345678 42\nnvidia_uvm 1234567 0\n' > "$FX/lsmod"
  : > "$FX/dev/nvidia0"; : > "$FX/dev/nvidiactl"
  check 'healthy: nvidia present and answering' 0 HEALTHY \
    '^PLANE drivers: HEALTHY .*nvidia=present'

  case_home='healthy-dmesg'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 0 > "$FX/dmesg.rc"; : > "$FX/dmesg.out"
  printf 'fixture kernel line 1\nfixture kernel line 2\nfixture kernel line 3\n' > "$FX/dmesg-all.out"
  printf 0 > "$FX/dmesg-all.rc"
  check 'healthy: unrestricted dmesg ring preferred' 0 HEALTHY 'ring=dmesg .*kerr=0'

  case_home='healthy-benign-backup'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'backup file: alpha: /etc/alpha.conf (Modification time mismatch)\nbackup file: alpha: /etc/alpha.conf (SHA256 checksum mismatch)\nalpha: 10 total files, 0 altered files\n' > "$FX/qkk.out"
  printf 1 > "$FX/qkk.rc"
  check 'healthy: rc=1 backup-only sample is not a defect' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*drift=0 backup_diffs=2'

  case_home='degraded-sample-drift'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'warning: alpha: /usr/bin/alpha (Size mismatch)\nalpha: 10 total files, 1 altered file\nbeta: 20 total files, 2 altered files\n' > "$FX/qkk.out"
  printf 1 > "$FX/qkk.rc"
  check 'degraded: Qkk sample drift' 1 DEGRADED '^PLANE packages: DEGRADED .*drift=3\[alpha,beta\]'

  case_home='degraded-foreign'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'elephant-a\nelephant-b\nelephant-c\n' > "$FX/pm"
  check 'degraded: foreign packages' 1 DEGRADED '^PLANE packages: DEGRADED .*foreign=3'

  # ---- round 7 foreign watch arm (lane S7-1): the r6 census rows as the accepted
  # baseline, exercised hit / embedded-default / new / version-drift / gone / absent.
  local r6base
  r6base=$(printf '%s\n' \
    'android-apktool-bin 3.0.3-1' 'elephant 2.21.0-1' 'elephant-bluetooth 2.21.0-1' \
    'elephant-calc 2.21.0-1' 'elephant-clipboard 2.21.0-1' 'elephant-desktopapplications 2.21.0-1' \
    'elephant-files 2.21.0-1' 'elephant-menus 2.21.0-1' 'elephant-providerlist 2.21.0-1' \
    'elephant-runner 2.21.0-1' 'elephant-symbols 2.21.0-1' 'elephant-todo 2.21.0-1' \
    'elephant-unicode 2.21.0-1' 'elephant-websearch 2.21.0-1' \
    'obsidian-cli-inspector 1.0.3-1' 'omarchy-walker 1.0.0-2')
  if [ "$(printf '%s\n' "$r6base" | wc -l)" -ne 16 ]; then
    bad 'fixture: r6 baseline literal is not 16 rows'
  fi

  case_home='healthy-foreign-baseline'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r6base" > "$FX/pm"
  printf '%s\n' "$r6base" > "$FX/fbase"
  check 'healthy: foreign set equals the accepted baseline (16 rows, hit)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*foreign=16\(known=16 new=0 drift=0 gone=0\) base=file\(16\)'

  case_home='healthy-foreign-embedded'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r6base" > "$FX/pm"
  EXTRA_ENV=(TSUKUROI_FOREIGN_BASELINE=)
  check 'healthy: embedded r6 snapshot is the default source' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*foreign=16\(known=16 new=0 drift=0 gone=0\) base=r6\(16\)'

  case_home='degraded-foreign-new'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\nnew-tool-bin 4.2-1\n' "$r6base" > "$FX/pm"
  printf '%s\n' "$r6base" > "$FX/fbase"
  check 'degraded: new foreign arrival is named' 1 DEGRADED \
    '^PLANE packages: DEGRADED .*new=1 drift=0 gone=0\) base=file\(16\) new=\[new-tool-bin\]'

  case_home='degraded-foreign-drift'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r6base" | sed -E 's/^android-apktool-bin 3\.0\.3-1$/android-apktool-bin 3.0.4-1/' > "$FX/pm"
  printf '%s\n' "$r6base" > "$FX/fbase"
  check 'degraded: baseline version change shows both versions' 1 DEGRADED \
    '^PLANE packages: DEGRADED .*new=0 drift=1 gone=0\) base=file\(16\) drift=\[android-apktool-bin\(3\.0\.3-1->3\.0\.4-1\)\]'

  case_home='degraded-foreign-gone'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r6base" | grep -v '^obsidian-cli-inspector ' > "$FX/pm"
  printf '%s\n' "$r6base" > "$FX/fbase"
  check 'degraded: baseline row no longer installed is never silent' 1 DEGRADED \
    '^PLANE packages: DEGRADED .*new=0 drift=0 gone=1\) base=file\(16\) gone=\[obsidian-cli-inspector\]'

  case_home='degraded-foreign-baseline-absent'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r6base" > "$FX/pm"
  EXTRA_ENV=(TSUKUROI_FOREIGN_BASELINE="$FX/fbase-absent")
  check 'degraded: absent baseline never reads HEALTHY' 1 DEGRADED \
    '^PLANE packages: DEGRADED .*foreign=16\(base=absent \[known/new/drift/gone unknown\]\)'

  case_home='degraded-pins'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'linux\n' > "$FX/pconf"
  check 'degraded: declared hold (IgnorePkg)' 1 DEGRADED '^PLANE packages: DEGRADED .*pins=linux'

  case_home='degraded-unit'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'broken.service loaded failed failed fixture failure\n' > "$FX/failedunits"
  check 'degraded: failed unit' 1 DEGRADED '^PLANE systemd: DEGRADED .*failed=1'

  case_home='degraded-timer'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'failed\n' > "$FX/timerresult"
  check 'degraded: timer last run failed' 1 DEGRADED '^PLANE systemd: DEGRADED .*timer_fail=1'

  case_home='degraded-kerr'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '{"MESSAGE":"Out of memory: Killed process 42"}\n{"MESSAGE":"Buffer I/O error on dev sr0"}\n{"MESSAGE":"other kernel complaint"}\n' > "$FX/journal-err.json"
  check 'degraded: kernel error ring' 1 DEGRADED '^PLANE drivers: DEGRADED .*kerr=3'

  case_home='blocked-lck'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/pacmandb/db.lck"
  check 'blocked: pacman db.lck' 2 BLOCKED '^PLANE packages: BLOCKED .*db\.lck=present'

  case_home='blocked-pacman-missing'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_PACMAN="$bin/pacman-absent")
  check 'blocked: pacman binary missing' 2 BLOCKED '^PLANE packages: BLOCKED .*pacman=missing'

  case_home='blocked-sample-error'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'error: package %s was not found\n' "'alpha'" > "$FX/qkk.out"
  printf 1 > "$FX/qkk.rc"
  check 'blocked: sample probe error' 2 BLOCKED 'sample probe error'

  # Round 42 (R41-CENSUS-PIPEFAIL-692): the same error line ahead of ~300 KB of further -Qkk output. Under pipefail
  # the old `printf | grep -q '^error:'` read false once the sample outgrew the pipe buffer (DEGRADED/HEALTHY).
  case_home='blocked-sample-error-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  { printf 'error: alpha: /usr/bin/alpha (Permission denied)\n'
    awk 'BEGIN { for (i = 0; i < 4000; i++) printf "warning: beta: /usr/share/beta/doc/f%05d.html (Modification time mismatch)\n", i }'
    printf 'alpha: 10 total files, 0 altered files\nbeta: 20 total files, 0 altered files\n'; } > "$FX/qkk.out"
  printf 1 > "$FX/qkk.rc"
  check 'blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1)' 2 BLOCKED \
    '^PLANE packages: BLOCKED \(pacman -Qkk sample probe error: error: alpha: /usr/bin/alpha \(Permission denied\);'

  case_home='blocked-bus'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'Failed to connect to bus: No such file or directory\n' > "$FX/sysrunning"
  printf 1 > "$FX/sysrunning.rc"
  check 'blocked: systemd user bus unreachable' 2 BLOCKED '^PLANE systemd: BLOCKED .*unusable rc=1'

  case_home='blocked-gpu'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/pci/0000:01:00.0"; printf '0x10de\n' > "$FX/pci/0000:01:00.0/vendor"
  printf 'NVIDIA-SMI has failed because it could not communicate with the NVIDIA driver\n' > "$FX/smi.out"
  printf 6 > "$FX/smi.rc"
  check 'blocked: nvidia hardware, driver offline' 2 BLOCKED 'nvidia-smi not answering'

  case_home='blocked-rings'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 1 > "$FX/dmesg.rc"; printf 1 > "$FX/journal-err.rc"; printf 1 > "$FX/journal-all.rc"
  check 'blocked: both kernel rings unusable' 2 BLOCKED 'kernel ring unusable'

  case_home='blocked-empty-ring'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 0 > "$FX/dmesg.rc"; : > "$FX/dmesg.out"; : > "$FX/dmesg-all.out"; printf 0 > "$FX/dmesg-all.rc"
  : > "$FX/journal-all.json"
  check 'blocked: empty ring is not a clean bill' 2 BLOCKED 'kernel ring empty'

  case_home='healthy-journal'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: journal/boot plane in the rollup' 0 HEALTHY \
    '^TSUKUROI_CENSUS: HEALTHY \(packages=HEALTHY systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY( [a-z-]+=[A-Z]+)*\)' \
    '^PLANE journal: HEALTHY \(boots=2 current=yes target=graphical\.target:active err=0 \(coredump=0 kernel=0 other=0\); failedhist=0; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0\)'

  case_home='degraded-boot-errors'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '{"SYSLOG_IDENTIFIER":"systemd-coredump","MESSAGE":[103,111,100,111,116]}\n{"SYSLOG_IDENTIFIER":"kernel","MESSAGE":"Buffer I/O error on dev sr0"}\n{"SYSLOG_IDENTIFIER":"sddm-helper","MESSAGE":"gkr-pam could not unlock the login keyring"}\n{"SYSLOG_IDENTIFIER":"limine-snapper-sync","MESSAGE":"No Snapper config found"}\n' > "$FX/journal-err.json"
  check 'degraded: journal boot errors at entry level' 1 DEGRADED \
    '^PLANE journal: DEGRADED .*err=4 \(coredump=1 kernel=1 other=2\)'

  case_home='degraded-failedhist'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '{"SYSLOG_IDENTIFIER":"systemd","MESSAGE":"Failed to start foo.service - Foo.","_SYSTEMD_UNIT":"foo.service"}\n{"SYSLOG_IDENTIFIER":"systemd","MESSAGE":"bar.service: Failed with result exit-code."}\n' > "$FX/journal-err.json"
  check 'degraded: failed services history from journal' 1 DEGRADED \
    '^PLANE journal: DEGRADED .*failedhist=2\[bar\.service,foo\.service\]'

  case_home='degraded-timer-drift'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'inactive\n' > "$FX/timeractivestate"
  check 'degraded: enabled timer not armed (drift)' 1 DEGRADED \
    '^PLANE journal: DEGRADED .*timer_drift=1 .*\(ai-usage\.timer=inactive\)'

  case_home='blocked-journal-missing'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_JOURNALCTL="$bin/journalctl-absent")
  check 'blocked: journalctl missing (fails closed)' 2 BLOCKED '^PLANE journal: BLOCKED .*journalctl=missing'

  case_home='blocked-boot-record'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/listboots"
  check 'blocked: boot record missing' 2 BLOCKED '^PLANE journal: BLOCKED .*boot record'

  case_home='blocked-boot-target'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'inactive\n' > "$FX/boottarget"
  printf 3 > "$FX/boottarget.rc"
  check 'blocked: boot target not reached' 2 BLOCKED '^PLANE journal: BLOCKED .*graphical\.target=inactive'

  case_home='blocked-journal-empty'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/journal-err.json"
  : > "$FX/journal-last"
  check 'blocked: empty journal is not a clean bill' 2 BLOCKED '^PLANE journal: BLOCKED .*no entries'

  case_home='blocked-journal-err'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 1 > "$FX/journal-err.rc"
  check 'blocked: journal err stream unreadable' 2 BLOCKED '^PLANE journal: BLOCKED .*err stream unreadable'

  # ---- round-5 mutation hardening (lane S5-1, 2026-10-14): one case per survivor class
  # from the census-v2 mutation sweep (tameshi's mutate-and-run.sh, 23 single-edit
  # defects, first pass 13 killed / 10 survived — the label suffixes name the defect
  # each case kills): D02 empty local db, D05 nonroot-artifact count, D06 bounded sample
  # size, D09 unreadable timer Result, D10 scope state degraded, D12 missing /dev node,
  # D14/D15 driver class counts, D19 unreadable PCI inventory, D20 journal timer plane.
  case_home='blocked-empty-pkgdb'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/pq"
  check 'blocked: empty local db is not a pass (D02)' 2 BLOCKED \
    '^PLANE packages: BLOCKED .*pacman -Qq listed no packages'

  case_home='healthy-nonroot-artifact'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'warning: alpha: /boot/amd-ucode.img (Permission denied)\nalpha: 10 total files, 0 altered files\nbeta: 20 total files, 0 altered files\n' > "$FX/qkk.out"
  printf 1 > "$FX/qkk.rc"
  check 'healthy: privilege artifacts counted, not drift (D05)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*drift=0 backup_diffs=0 nonroot_artifacts=1'

  case_home='healthy-sample-bound'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_SAMPLE_N=2)
  check 'healthy: bounded -Qkk sample honors its size (D06)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*sample=2\(alpha,beta\)'

  case_home='degraded-timer-unknown'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/timerresult"
  check 'degraded: empty timer Result is an unknown, not a failure (D09)' 1 DEGRADED \
    '^PLANE systemd: DEGRADED .*timer_fail=0 timer_unknown=1'

  case_home='degraded-scope'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'degraded\n' > "$FX/sysrunning"
  printf 1 > "$FX/sysrunning.rc"
  check 'degraded: user scope state degraded (D10)' 1 DEGRADED \
    '^PLANE systemd: DEGRADED .*state=degraded'

  case_home='blocked-no-node'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/pci/0000:01:00.0"; printf '0x10de\n' > "$FX/pci/0000:01:00.0/vendor"
  printf 'NVIDIA GeForce RTX 5070, 610.57.04\n' > "$FX/smi.out"; printf 0 > "$FX/smi.rc"
  printf 'nvidia 12345678 42\n' > "$FX/lsmod"
  check 'blocked: nvidia module loaded but no /dev node (D12)' 2 BLOCKED \
    '^PLANE drivers: BLOCKED .*no /dev/nvidia\* node'

  case_home='degraded-kerr-classes'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 0 > "$FX/dmesg.rc"
  printf 'Out of memory: Killed process 42\nBuffer I/O error on dev sr0\nNVRM: Xid 13: graphics fault\nfixture: unattributed kernel error\n' > "$FX/dmesg.out"
  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
    '^PLANE drivers: DEGRADED .*kerr=4 \(oom=1 io=1 gpu=1 other=1\)'

  case_home='blocked-pci-unreadable'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_PCI_SYSFS="$FX/no-pci-inventory")
  check 'blocked: unreadable PCI inventory is not a pass (D19)' 2 BLOCKED \
    '^PLANE drivers: BLOCKED .*PCI inventory unreadable'

  case_home='degraded-jrn-timer-plane'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 1 > "$FX/timerlist.rc"
  check 'degraded: journal timer plane unreadable, drift unknown (D20)' 2 BLOCKED \
    '^PLANE journal: DEGRADED .*timer plane unreadable \[drift unknown\]'

  # ---- round 7 memory-pressure arm (lane S7-2): the round-6 OOM-event plane's classes
  # (corpus/knowledge/oom-event-plane.md §8 C1-C6) as live evidence on the drivers line,
  # exercised quiet / presence-flag / classes-with-the-ring / swap anchors / `.local` /
  # named-unknown / blocked.
  case_home='healthy-mem-quiet'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: memory-pressure arm quiet (S7-2)' 0 HEALTHY \
    '^PLANE drivers: HEALTHY .*mem=\[HEALTHY\] C1_kernel_oom=0 C2_sysd_oom=0 C3_sigkill=0' \
    'mem=\[HEALTHY\].*C4_present=0 C4_local=0; C5_swap_fail=0 C5_swap_peak_pct=0% C5_pswp=0/0' \
    'guards=max/max oom\.group=0; r6 vocab: oom-event-plane\.md §8'

  case_home='degraded-mem-presence'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 7\noom_group_kill 0\nsock_throttled 0\n' \
    > "$FX/cgroup/user.slice/memory.events"
  check 'degraded: memory arm — oom_kill is a presence flag, not a count (S7-2)' 1 DEGRADED \
    '^PLANE drivers: DEGRADED .*mem=\[DEGRADED\] .*C4_sweep=5 C4_present=1\[user\.slice\] C4_local=0'

  case_home='degraded-mem-classes'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 0 > "$FX/dmesg.rc"
  printf 'Out of memory: Killed process 1732581 (python3)\n' > "$FX/dmesg.out"
  printf '{"MESSAGE":"Out of memory: Killed process 1732581 (python3)"}\n' > "$FX/oom-kernel.json"
  printf '%s\n' '{"MESSAGE":"app.scope: The kernel OOM killer killed some processes in this unit."}' \
    '{"MESSAGE":"user-1000.slice: The kernel OOM killer killed some processes in this unit."}' \
    > "$FX/oom-attrib.json"
  printf '%s\n' '{"MESSAGE":"Main process exited, code=killed, status=9/KILL"}' \
    '{"MESSAGE":"a.service: Failed with result (signal)."}' \
    '{"MESSAGE":"b.scope: Failed with result (oom-kill)."}' > "$FX/oom-sigkill.json"
  check 'degraded: memory arm — ring oom class and C1/C2/C3 reported together (S7-2)' 1 DEGRADED \
    '^PLANE drivers: DEGRADED .*kerr=1 \(oom=1 io=0 gpu=0 other=0\)' \
    'mem=\[DEGRADED\] C1_kernel_oom=1 C2_sysd_oom=2 C3_sigkill=3'

  case_home='degraded-mem-swap'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'high 0\nmax 0\nfail 5922849\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.swap.events"
  printf '36744949760\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.swap.peak"
  printf 'pswpin 72117252\npswpout 93795670\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.stat"
  printf 'SwapTotal: 35917176 kB\nMemAvailable: 19482144 kB\nShmem: 6882556 kB\n' > "$FX/meminfo"
  check 'degraded: memory arm — swap-pressure anchors C5 (S7-2)' 1 DEGRADED \
    'mem=\[DEGRADED\] .*C5_swap_fail=5922849 C5_swap_peak_pct=99% C5_pswp=72117252/93795670'

  case_home='degraded-mem-local'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 2\noom_group_kill 0\nsock_throttled 0\n' \
    > "$FX/cgroup/user.slice/memory.events.local"
  check 'degraded: memory arm — memory.events.local flag reported separately (S7-2)' 1 DEGRADED \
    'mem=\[DEGRADED\] .*C4_present=0 C4_local=1'

  case_home='degraded-mem-psi-unknown'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_PRESSURE_FILE="$FX/no-such-pressure")
  check 'degraded: memory arm — unreadable PSI is a named unknown, not a pass (S7-2)' 1 DEGRADED \
    'mem=\[DEGRADED\] .*unknown=\[C6-psi\]'

  case_home='degraded-mem-slice-unknown'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_MEM_SLICE='user.slice/no-such-slice')
  check 'degraded: memory arm — unreadable slice anchors are a named unknown (S7-2)' 1 DEGRADED \
    'mem=\[DEGRADED\] .*unknown=\[C5-slice\]'

  case_home='blocked-mem-unreadable'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_CGROUP_ROOT="$FX/no-cgroup" TSUKUROI_JOURNALCTL="$bin/journalctl-absent")
  check 'blocked: memory arm — no cgroup and no journal: no class readable (S7-2)' 2 BLOCKED \
    'mem=\[BLOCKED\]'

  # ---- round 9 update-safety plane (lane S9-1): the fifth owned surface exercised — INERT
  # over a live channel, candidates, an unreadable `-Qu`, no channel at all, a stale content
  # stamp (and the threshold that flips it), both fold rows, the class-split pin, the `-Suu`
  # trap row, the log window miss, the repo-side join, expac absence and an unreadable join.
  # Vocabulary and composition: update-safety-note.md:334-339 (an empty candidate set is
  # INERT only with a channel reading; unreadable probes are BLOCKED; the 36-day-class
  # content stamp is UNKNOWN-UPSTREAM — never a clean bill).
  case_home='healthy-update-safety'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: update-safety INERT over a fresh channel (R9)' 0 HEALTHY \
    '^PLANE update-safety: HEALTHY \(status=INERT; pending=none; qu=rc=1/0; sup=0; join=equal=2 behind=0 ahead=0 src=sl\+expac; expac=agree; chan=dbs=2 fetch=[0-9?]+d stamp=0d; offline\.db=present' \
    'classes=offline-exile:0,aur-local:0; trap=-Suu:0' \
    '^TSUKUROI_CENSUS: HEALTHY \(packages=HEALTHY systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY( [a-z-]+=[A-Z]+)*\)'

  case_home='degraded-update-candidates'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'alpha 1.0-1 -> 1.1-1\nbeta 2.0-1 -> 2.1-1\n' > "$FX/qu"; printf 0 > "$FX/qu.rc"
  printf 'fixture/alpha 1.1-1\nextra/beta 2.1-1\n' > "$FX/sup"
  check 'degraded: update candidates are REQUIRES-PREP with names (R9)' 1 DEGRADED \
    '^PLANE update-safety: DEGRADED \(status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=2 join_behind=0 names=\[alpha,beta\]\); qu=rc=0/2; sup=2;'

  # Round 42 (R41-CENSUS-PIPEFAIL-692): 4002 candidates (~100 KB) on -Qu, -Sup and -Suu. The old `printf | head -n3`
  # and `| head -n1` assignments killed the whole census with exit 141 once a list outgrew the pipe buffer.
  case_home='degraded-update-candidates-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  { printf 'alpha 1.0-1 -> 1.1-1\nbeta 2.0-1 -> 2.1-1\n'
    awk 'BEGIN { for (i = 0; i < 4000; i++) printf "pad%05d 1.0-1 -> 1.0-2\n", i }'; } > "$FX/qu"; printf 0 > "$FX/qu.rc"
  { printf 'fixture/alpha 1.1-1\nextra/beta 2.1-1\n'
    awk 'BEGIN { for (i = 0; i < 4000; i++) printf "extra/pad%05d 1.0-2\n", i }'; } > "$FX/sup"
  cp "$FX/sup" "$FX/suu"
  check 'degraded: 4002 update candidates keep the names and the trap row (R42-C1)' 1 DEGRADED \
    '^PLANE update-safety: DEGRADED \(status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=4002 join_behind=0 names=\[alpha,beta,pad00000\]\); qu=rc=0/4002; sup=4002;' \
    'trap=-Suu:4002\[fixture/alpha 1\.1-1\]'

  # Round 42 (wave-1 C1MutSelftest): the two -Sup disagreement arms with a -Sup side past the pipe buffer. The
  # equal-count case above never enters them, and the old `printf | head -n3` assignment died there (exit 141).
  case_home='degraded-update-sup-disagree-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/qu"; printf 1 > "$FX/qu.rc"
  { printf 'fixture/alpha 1.1-1\nextra/beta 2.1-1\n'
    awk 'BEGIN { for (i = 0; i < 4000; i++) printf "extra/pad%05d 1.0-2\n", i }'; } > "$FX/sup"
  check 'degraded: -Qu empty against a large -Sup keeps the disagree names (R42-C1)' 1 DEGRADED \
    '^PLANE update-safety: DEGRADED \(status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=4002 join_behind=0 names=\[alpha,beta,pad00000\]\); qu=rc=1/0; sup=4002 disagree\[qu=0 sup=4002\];'

  case_home='degraded-update-qu-sup-mismatch-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'alpha 1.0-1 -> 1.1-1\nbeta 2.0-1 -> 2.1-1\n' > "$FX/qu"; printf 0 > "$FX/qu.rc"
  { printf 'fixture/alpha 1.1-1\nextra/beta 2.1-1\n'
    awk 'BEGIN { for (i = 0; i < 4000; i++) printf "extra/pad%05d 1.0-2\n", i }'; } > "$FX/sup"
  check 'degraded: -Qu/-Sup count mismatch against a large -Sup keeps the disagree names (R42-C1)' 1 DEGRADED \
    '^PLANE update-safety: DEGRADED \(status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=4002 join_behind=0 names=\[alpha,beta,pad00000\]\); qu=rc=0/2; sup=4002 disagree\[qu=2 sup=4002\];'

  case_home='blocked-update-qu'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 0 > "$FX/qu.rc"
  check 'blocked: an empty -Qu at rc=0 is unreadable, never INERT (R9)' 2 BLOCKED \
    '^PLANE update-safety: BLOCKED \(status=BLOCKED; qu=rc=0/0 \[pacman -Qu unreadable — never INERT\]; chan=dbs=2'

  case_home='blocked-update-nochannel'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  rm -f "$FX/pacmandb/sync/core.db" "$FX/pacmandb/sync/omarchy.db"
  check 'blocked: empty over no channel is not an up-to-date reading (R9)' 2 BLOCKED \
    'status=BLOCKED; .*chan=dbs=0' 'offline\.db=present'

  case_home='degraded-update-stale'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  touch -d "@$(( $(date +%s) - 30 * 86400 ))" "$FX/pacmandb/sync/core.db"
  check 'degraded: a stale content stamp is UNKNOWN-UPSTREAM, never INERT (R9)' 1 DEGRADED \
    'status=UNKNOWN-UPSTREAM; pending=none; .*chan=dbs=2 fetch=[0-9?]+d stamp=30d'

  case_home='healthy-update-chanmax'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  touch -d "@$(( $(date +%s) - 30 * 86400 ))" "$FX/pacmandb/sync/core.db"
  EXTRA_ENV=(TSUKUROI_CHANNEL_MAX_AGE_D=60)
  check 'healthy: the channel-freshness threshold is honoured, not decorative (R9)' 0 HEALTHY \
    'status=INERT; .*stamp=30d'

  case_home='degraded-update-fold-new'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\nnew-tool-bin 4.2-1\n' "$r6base" > "$FX/pm"
  printf '%s\n' "$r6base" > "$FX/fbase"
  check 'degraded: the fold names unknown-provenance arrivals and can only worsen (R9)' 1 DEGRADED \
    'status=INERT; .*classes=offline-exile:14,aur-local:2 unknown-provenance=\[new-tool-bin\]'

  case_home='degraded-update-fold-absent'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r6base" > "$FX/pm"
  EXTRA_ENV=(TSUKUROI_FOREIGN_BASELINE="$FX/fbase-absent")
  check 'degraded: the fold never reads off a missing baseline (R9)' 1 DEGRADED \
    'classes=unavailable\(baseline-absent\)'

  case_home='healthy-update-split'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'android-apktool-bin 3.0.3-1\nobsidian-cli-inspector 1.0.3-1\n' > "$FX/pm"
  printf 'android-apktool-bin 3.0.3-1\nobsidian-cli-inspector 1.0.3-1\n' > "$FX/fbase"
  check 'healthy: the joined class split is the register AUR-local pair (R9)' 0 HEALTHY \
    'classes=offline-exile:0,aur-local:2' '^PLANE update-safety: HEALTHY'

  case_home='healthy-update-suu'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'omarchy/1password-beta 8.12.42_32.BETA-1\n' > "$FX/suu"
  check 'healthy: the -Suu trap row is printed and verdict-neutral (R9)' 0 HEALTHY \
    'trap=-Suu:1\[omarchy/1password-beta 8\.12\.42_32\.BETA-1\]'

  case_home='healthy-update-log-miss'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '[2026-10-13T16:37:59-0300] [ALPM] installed fixture-pkg (1.0-1)\n' > "$FX/pacman.log"
  check 'healthy: a log window miss prints cmd=unknown (R9)' 0 HEALTHY \
    'log=cmd=unknown \[window miss' 'refresh=none-in-window'

  case_home='degraded-update-join'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'fixture alpha 1.1-1\nextra beta 2.0-1\n' > "$FX/sl"
  printf 'alpha\t1.1-1\nbeta\t2.0-1\n' > "$FX/expacsl"
  check 'degraded: a repo-side behind row joins the candidate class (R9)' 1 DEGRADED \
    'status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=0 join_behind=1\); .*join=equal=1 behind=1 ahead=0 src=sl\+expac behind_names=\[alpha\]'

  case_home='healthy-update-expac-absent'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_EXPAC="$bin/expac-absent")
  check 'healthy: absent expac prints its absence, never a silent pass (R9)' 0 HEALTHY \
    'join=equal=2 behind=0 ahead=0 src=sl; expac=absent'

  case_home='healthy-update-join-unavailable'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 1 > "$FX/sl.rc"
  check 'healthy: an unreadable join is printed, never silent (R9)' 0 HEALTHY \
    'join=unavailable\(q=rc=0 sl=rc=1\); expac=n/a\(join unavailable\)'

  # ---- round 9 oom plane (lane S9-2): the round-8 specified-not-landed watch lands —
  # retained window, event clusters, new-vs-baseline, fail-closed. The declared-wave
  # literal is pinned here so an edit to the embedded constant cannot pass silently.
  local r8oom
  r8oom=$(printf '%s\n' \
    '2026-10-13 23:44 A kernel+attrib+kill9 event A: global OOM, victim python3 (pid 1732581)' \
    '2026-10-14 13:10 B attrib+kill9 event B: session teardown SIGKILL class, no kernel record (F1)')
  if [ "$(printf '%s\n' "$r8oom" | wc -l)" -ne 2 ]; then
    bad 'fixture: r8 oom baseline literal is not 2 rows'
  fi

  case_home='healthy-oom-clean'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: oom watch clean over the retained window (S9-2)' 0 HEALTHY \
    '^PLANE oom: HEALTHY \(window=boots=2 2026-10-11\.\.2026-10-14; C1_kernel=0 killed_process=0; C2_events=0 C3_events=0 clusters=0; base=file\(0\) known=0 new=0 missing=0 out_of_window=0; ledger=vmstat\.oom_kill=0'

  case_home='healthy-oom-r8-baseline'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' \
    '2026-10-13T23:44:30.574948-03:00 fixture-host systemd[1573]: app-x.scope: The kernel OOM killer killed some processes in this unit.' \
    '2026-10-14T13:10:59.400591-03:00 fixture-host systemd[1]: user-1000.slice: The kernel OOM killer killed some processes in this unit.' \
    > "$FX/oomwin-attrib"
  printf 0 > "$FX/oomwin-attrib.rc"
  printf '%s\n' \
    '2026-10-14T13:10:59.380873-03:00 fixture-host systemd[1]: user@1000.service: Main process exited, code=killed, status=9/KILL' \
    > "$FX/oomwin-sigkill"
  printf 0 > "$FX/oomwin-sigkill.rc"
  printf '%s\n' \
    '2026-10-13T23:44:30.638238-03:00 fixture-host kernel: Out of memory: Killed process 1732581 (python3)' \
    > "$FX/oomwin-kernel"
  printf 0 > "$FX/oomwin-kernel.rc"
  EXTRA_ENV=(TSUKUROI_OOM_BASELINE=)
  check 'healthy: oom watch — embedded r8 baseline, both declared waves known (S9-2)' 0 HEALTHY \
    '^PLANE oom: HEALTHY \(window=boots=2 .*C1_kernel=1 killed_process=1; C2_events=2 C3_events=1 clusters=2\[2026-10-13 23:44,2026-10-14 13:10\]; base=r8\(2\) known=2\[A, B\] new=0 missing=0 out_of_window=0'

  case_home='healthy-oom-baseline-hit'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r8oom" > "$FX/obase"
  printf '%s\n' \
    '2026-10-13T23:44:30.574948-03:00 fixture-host systemd[1573]: app-x.scope: The kernel OOM killer killed some processes in this unit.' \
    > "$FX/oomwin-attrib"
  printf 0 > "$FX/oomwin-attrib.rc"
  printf '%s\n' \
    '2026-10-14T13:10:59.380873-03:00 fixture-host systemd[1]: user@1000.service: Main process exited, code=killed, status=9/KILL' \
    > "$FX/oomwin-sigkill"
  printf 0 > "$FX/oomwin-sigkill.rc"
  check 'healthy: oom watch — external baseline file, both waves known (S9-2)' 0 HEALTHY \
    '^PLANE oom: HEALTHY .*base=file\(2\) known=2\[A, B\] new=0 missing=0 out_of_window=0'

  case_home='degraded-oom-new'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '2026-10-13 23:44 A attrib+kill9 declared wave A\n' > "$FX/obase"
  printf '%s\n' \
    '2026-10-13T23:44:30.574948-03:00 fixture-host systemd[1573]: app-x.scope: The kernel OOM killer killed some processes in this unit.' \
    '2026-10-12T09:15:11.000001-03:00 fixture-host systemd[1573]: app-y.scope: The kernel OOM killer killed some processes in this unit.' \
    > "$FX/oomwin-attrib"
  printf 0 > "$FX/oomwin-attrib.rc"
  check 'degraded: oom watch — a cluster not in the baseline is new and named (S9-2)' 1 DEGRADED \
    '^PLANE oom: DEGRADED .*base=file\(1\) known=1\[A\] new=1\[2026-10-12 09:15\] missing=0 out_of_window=0'

  case_home='degraded-oom-missing'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r8oom" > "$FX/obase"
  printf '%s\n' \
    '2026-10-13T23:44:30.574948-03:00 fixture-host systemd[1573]: app-x.scope: The kernel OOM killer killed some processes in this unit.' \
    > "$FX/oomwin-attrib"
  printf 0 > "$FX/oomwin-attrib.rc"
  check 'degraded: oom watch — a declared wave missing inside the window (S9-2)' 1 DEGRADED \
    '^PLANE oom: DEGRADED .*base=file\(2\) known=1\[A\] new=0 missing=1\[2026-10-14 13:10\] out_of_window=0'

  case_home='healthy-oom-out-of-window'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '2026-09-30 02:00 Z attrib+kill9 older than the retained window\n' > "$FX/obase"
  check 'healthy: oom watch — declared wave older than the window (retention loss only) (S9-2)' 0 HEALTHY \
    '^PLANE oom: HEALTHY .*base=file\(1\) known=0 new=0 missing=0 out_of_window=1\[2026-09-30 02:00\]'

  case_home='degraded-oom-baseline-absent'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_OOM_BASELINE="$FX/obase-absent")
  check 'degraded: oom watch — absent baseline never reads HEALTHY (S9-2)' 1 DEGRADED \
    '^PLANE oom: DEGRADED .*base=absent \[known/new/missing/out_of_window unknown\]'

  case_home='degraded-oom-ledger'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_VMSTAT_FILE="$FX/no-such-vmstat")
  check 'degraded: oom watch — unreadable kernel-kill ledger is a named unknown (S9-2)' 1 DEGRADED \
    '^PLANE oom: DEGRADED .*ledger=vmstat\.oom_kill=-; .*unknown=\[ledger\]'

  case_home='blocked-oom-window'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 4 > "$FX/listboots.rc"
  check 'blocked: oom watch — window unreadable (S9-2)' 2 BLOCKED \
    '^PLANE oom: BLOCKED \(window unreadable: journalctl --list-boots rc=4'

  case_home='blocked-oom-window-empty'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'IDX BOOT ID   FIRST ENTRY   LAST ENTRY\n' > "$FX/listboots"
  check 'blocked: oom watch — no boot measured is not a clean window (S9-2)' 2 BLOCKED \
    '^PLANE oom: BLOCKED \(window empty: boots=0'

  case_home='blocked-oom-scan'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 3 > "$FX/oomwin-attrib.rc"
  check 'blocked: oom watch — a window scan unreadable fails closed (S9-2)' 2 BLOCKED \
    '^PLANE oom: BLOCKED \(scans unreadable:C2 \[fails closed\]; .*C2_events=\?'

  # ---- round 10 (lane S10-2): the mutation sweep's four survivors and their covering cases ----
  # Pre-hardening sweep via the tameshi service (target pin c396662e…, 10 defects, two tool
  # revisions): 6/10 killed; the survivors were the default -Qkk sample cap (H1), the CLI exit
  # map (H2), the rollup field order (H3) and the update-safety -Sup fail-closed arm (H4).
  # Each case below is falsifiable: it red-flags its covering mutant (the post-hardening
  # covering sweep) and passes on this revision.
  case_home='healthy-sample-cap'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'a01\na02\na03\na04\na05\na06\na07\na08\na09\na10\na11\na12\n' > "$FX/pq"
  check 'healthy: the default -Qkk sample cap bounds the sample (S10-2)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*sample=8\(a01,a02,a03,a04,a05,a06,a07,a08\)'

  case_home='blocked-rollup-mixed'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/pacmandb/db.lck"
  check 'blocked: the rollup line names every plane field in order (S10-2)' 2 BLOCKED \
    '^TSUKUROI_CENSUS: BLOCKED \(packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=BLOCKED oom=HEALTHY\)$'

  case_home='blocked-upd-sup-unreadable'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 1 > "$FX/sup.rc"
  check 'blocked: update-safety -Sup unreadable fails closed (S10-2)' 2 BLOCKED \
    '^PLANE update-safety: BLOCKED \(status=BLOCKED; sup=rc=1'

  # ---- round 12 (lane C1): root-directory metadata arm, hermetic ---------------------
  # Finding pattern pinned by every case below: the packages line always carries
  # `root_status= root_mode= ... root_dir=` (the check() harness asserts these universally,
  # including `root_dir=<configured fixture root>`, so a live-/ leak cannot pass). The arm
  # is report-only for owner bits: 0555/0644/0400 stay HEALTHY with distinct present/absent
  # facts; only unavailable metadata or a non-directory is BLOCKED. Mode assertions anchor
  # the four-digit `%04a` token (`root_mode=0555 `, not a 555 substring) so a decimal parse
  # or a format drift turns the case red.
  case_home='healthy-root-0755'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: C1 root arm — 0755 owner bits present (R12-C1)' 0 HEALTHY \
    "^PLANE packages: HEALTHY .*root_status=ok root_mode=0755 root_uid=$(id -u) root_gid=$(id -g) root_euid=$(id -u) root_owner_write=present root_owner_search=present root_src=override root_dir=$FX/root"

  case_home='healthy-root-0555-report'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  chmod 0555 "$FX/root"
  check 'healthy: C1 root arm — 0555 owner-write absent is report-only (R12-C1)' 0 HEALTHY \
    '^TSUKUROI_CENSUS: HEALTHY \(packages=HEALTHY ' \
    '^PLANE packages: HEALTHY .*root_status=ok root_mode=0555 root_uid=[0-9]+ root_gid=[0-9]+ .*root_owner_write=absent root_owner_search=present root_report=owner-write-absent root_intent=not-assessed'

  case_home='healthy-root-0644-search'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  chmod 0644 "$FX/root"
  check 'healthy: C1 root arm — owner-search absent independently (R12-C1)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*root_status=ok root_mode=0644 root_uid=[0-9]+ root_gid=[0-9]+ .*root_owner_write=present root_owner_search=absent root_report=owner-search-absent root_intent=not-assessed'

  case_home='healthy-root-0400-both'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  chmod 0400 "$FX/root"
  check 'healthy: C1 root arm — both owner bits absent, both named (R12-C1)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*root_status=ok root_mode=0400 root_uid=[0-9]+ root_gid=[0-9]+ .*root_owner_write=absent root_owner_search=absent root_report=owner-write-absent,owner-search-absent root_intent=not-assessed'

  case_home='healthy-root-sticky'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  chmod 1777 "$FX/root"
  check 'healthy: C1 root arm — 1777 sticky parses as octal, bits present (R12-C1)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*root_status=ok root_mode=1777 root_uid=[0-9]+ root_gid=[0-9]+ .*root_owner_write=present root_owner_search=present root_src=override root_dir='

  case_home='healthy-root-setgid'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  chmod 2755 "$FX/root"
  check 'healthy: C1 root arm — 2755 setgid does not disturb owner bits (R12-C1)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*root_status=ok root_mode=2755 root_uid=[0-9]+ root_gid=[0-9]+ .*root_owner_write=present root_owner_search=present root_src=override root_dir='

  case_home='healthy-root-sticky-norewrite'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  chmod 1555 "$FX/root"
  check 'healthy: C1 root arm — 1555 sticky with owner-write absent, report-only (R12-C1)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*root_status=ok root_mode=1555 root_uid=[0-9]+ root_gid=[0-9]+ .*root_owner_write=absent root_owner_search=present root_report=owner-write-absent'

  # Not fixtureable without CAP_CHOWN: a non-root-owned root cannot be built by the selftest
  # user. The verdict is ownership-independent by design (bits only) and root_uid/gid are
  # printed facts, so this is a named skip, never a pass.
  skip 'C1 root arm — non-root-owned fixture (requires CAP_CHOWN; verdict is ownership-independent)'
  # No 000-parent fixture: it would leave an unreadable subtree for find/rm, and under euid 0
  # DAC is bypassed so the case would be vacuous. Missing/dangling/loop cover the class.
  skip 'C1 root arm — EACCES metadata case not built (000 subtree residue; uid 0 bypasses DAC)'

  case_home='blocked-root-missing'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_ROOT_DIR="$FX/no-such-root")
  ROOT_EXPECT="$FX/no-such-root"
  check 'blocked: C1 root arm — missing metadata BLOCKED with explicit unknowns (R12-C1)' 2 BLOCKED \
    "^PLANE packages: BLOCKED .*root_status=unavailable\\(stat=rc=1 errno=missing\\) root_mode=unknown root_uid=unknown root_gid=unknown root_euid=$(id -u) root_owner_write=unknown root_owner_search=unknown root_src=override root_dir=$FX/no-such-root"

  case_home='blocked-root-regular-file'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/root-file"; chmod 0644 "$FX/root-file"
  EXTRA_ENV=(TSUKUROI_ROOT_DIR="$FX/root-file")
  ROOT_EXPECT="$FX/root-file"
  check 'blocked: C1 root arm — regular file is a non-directory (R12-C1)' 2 BLOCKED \
    "^PLANE packages: BLOCKED .*root_status=non-directory\\(type=regular-empty-file\\) root_mode=0644 root_uid=$(id -u) root_gid=$(id -g) root_euid=$(id -u) root_owner_write=unknown root_owner_search=unknown root_src=override root_dir=$FX/root-file"

  case_home='blocked-root-dangling'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  ln -s "$FX/no-such-target" "$FX/root-link"
  EXTRA_ENV=(TSUKUROI_ROOT_DIR="$FX/root-link")
  ROOT_EXPECT="$FX/root-link"
  check 'blocked: C1 root arm — dangling symlink is unavailable, not a pass (R12-C1)' 2 BLOCKED \
    "^PLANE packages: BLOCKED .*root_status=unavailable\\(stat=rc=1 errno=missing\\) root_mode=unknown root_uid=unknown root_gid=unknown root_type=symlink\\(unresolved\\) root_euid=$(id -u) root_owner_write=unknown root_owner_search=unknown root_src=override root_dir=$FX/root-link"

  case_home='blocked-root-loop'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  ln -s "$FX/loop-b" "$FX/loop-a"; ln -s "$FX/loop-a" "$FX/loop-b"
  EXTRA_ENV=(TSUKUROI_ROOT_DIR="$FX/loop-a")
  ROOT_EXPECT="$FX/loop-a"
  check 'blocked: C1 root arm — symlink loop is unavailable, never a pass (R12-C1)' 2 BLOCKED \
    '^PLANE packages: BLOCKED .*root_status=unavailable\(stat=rc=1 errno=symlink-loop\) root_mode=unknown root_uid=unknown root_gid=unknown root_type=symlink\(unresolved\) root_euid=[0-9]+ root_owner_write=unknown root_owner_search=unknown'

  case_home='blocked-root-empty-override'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_ROOT_DIR=)
  ROOT_EXPECT='empty'
  check 'blocked: C1 root arm — empty override never falls back to live / (R12-C1)' 2 BLOCKED \
    '^PLANE packages: BLOCKED .*root_status=unavailable\(override=empty\) root_mode=unknown root_uid=unknown root_gid=unknown root_euid=[0-9]+ root_owner_write=unknown root_owner_search=unknown root_src=override root_dir=empty'

  case_home='blocked-root-unsafe-override'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_ROOT_DIR="$FX/root root_mode=0755")
  ROOT_EXPECT='unsafe'
  check 'blocked: C1 root arm — unsafe override rejected, raw path not echoed (R12-C1)' 2 BLOCKED \
    '^PLANE packages: BLOCKED .*root_status=unavailable\(override=unsafe\) root_mode=unknown root_uid=unknown root_gid=unknown root_euid=[0-9]+ root_owner_write=unknown root_owner_search=unknown root_src=override root_dir=unsafe'

  # Metadata survives every packages early return: composition happens at emit time in main,
  # so these four returns (binary missing / lock / empty db / sample rc) are representative
  # proofs, not special cases. The harness's universal root_dir assertion runs on each too.
  case_home='blocked-root-early-pacman-missing'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_PACMAN="$bin/pacman-absent")
  check 'blocked: C1 root arm survives pacman=missing early return (R12-C1)' 2 BLOCKED \
    '^PLANE packages: BLOCKED .*pacman=missing .*root_status=ok root_mode=0755 root_uid=[0-9]+ root_gid=[0-9]+'

  case_home='blocked-root-early-lck'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/pacmandb/db.lck"
  check 'blocked: C1 root arm survives db.lck early return (R12-C1)' 2 BLOCKED \
    'db\.lck=present' 'root_status=ok root_mode=0755 root_uid=[0-9]+ root_gid=[0-9]+ root_euid=[0-9]+ root_owner_write=present'

  case_home='blocked-root-early-empty-db'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/pq"
  check 'blocked: C1 root arm survives empty-db early return (R12-C1)' 2 BLOCKED \
    'pacman -Qq listed no packages' 'root_status=ok root_mode=0755 root_uid=[0-9]+ root_gid=[0-9]+'

  case_home='blocked-root-early-qkk-rc'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 2 > "$FX/qkk.rc"
  check 'blocked: C1 root arm survives sample-rc early return (R12-C1)' 2 BLOCKED \
    'pacman -Qkk sample rc=2' 'root_status=ok root_mode=0755 root_uid=[0-9]+ root_gid=[0-9]+'

  # ---- round 32 (C1): the ADJ-04 sibling handoff lines ------------------------------
  # Four falsifiable cases: the handoff is absent on a clean host; a dated kill event
  # routes one kill-events line whose value is the oom plane's own cluster count; a boot-0
  # coredump entry routes one coredumps line whose value is the journal plane's own
  # coredump count; and a cumulative vmstat oom_kill counter (read, and visible as
  # `ledger=`) is never a dated event, so it routes no kill-events line.
  case_home='handoff-absent-healthy'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: no ADJ-04 handoff line without a dated event (R32-C1)' 0 HEALTHY \
    'ABSENT:^HANDOFF'

  case_home='handoff-kill-events'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' \
    '2026-10-13T23:44:30.574948-03:00 fixture-host systemd[1573]: app-x.scope: The kernel OOM killer killed some processes in this unit.' \
    '2026-10-14T13:10:59.400591-03:00 fixture-host systemd[1]: user-1000.slice: The kernel OOM killer killed some processes in this unit.' \
    > "$FX/oomwin-attrib"
  printf 0 > "$FX/oomwin-attrib.rc"
  printf '%s\n' \
    '2026-10-14T13:10:59.380873-03:00 fixture-host systemd[1]: user@1000.service: Main process exited, code=killed, status=9/KILL' \
    > "$FX/oomwin-sigkill"
  printf 0 > "$FX/oomwin-sigkill.rc"
  printf '%s\n' \
    '2026-10-13T23:44:30.638238-03:00 fixture-host kernel: Out of memory: Killed process 1732581 (python3)' \
    > "$FX/oomwin-kernel"
  printf 0 > "$FX/oomwin-kernel.rc"
  EXTRA_ENV=(TSUKUROI_OOM_BASELINE=)
  check 'healthy: a dated kill event routes one kill-events handoff, value = the cluster count (R32-C1)' 0 HEALTHY \
    'C2_events=2 C3_events=1 clusters=2\[' \
    '^HANDOFF ADJ-04 mori class=kill-events value=2 kind=dated-event state=prepared window=boots=2:2026-10-11\.\.2026-10-14 source=journal-window$'

  case_home='handoff-coredumps'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' \
    '{"MESSAGE":"Main process terminated with signal 11 (Segmentation fault) of user 1000","PRIORITY":"3","SYSLOG_IDENTIFIER":"systemd-coredump","_BOOT_ID":"d7f0bc8d938e4249b4a1f250cbfacf58","__REALTIME_TIMESTAMP":"1799000000000000"}' \
    '{"MESSAGE":"Main process terminated with signal 6 (Aborted) of user 1000","PRIORITY":"3","SYSLOG_IDENTIFIER":"systemd-coredump","_BOOT_ID":"d7f0bc8d938e4249b4a1f250cbfacf58","__REALTIME_TIMESTAMP":"1799000060000000"}' \
    '{"MESSAGE":"Main process terminated with signal 11 (Segmentation fault) of user 1000","PRIORITY":"3","SYSLOG_IDENTIFIER":"systemd-coredump","_BOOT_ID":"d7f0bc8d938e4249b4a1f250cbfacf58","__REALTIME_TIMESTAMP":"1799000120000000"}' \
    > "$FX/journal-err.json"
  check 'degraded: boot-0 coredumps route one coredumps handoff, value = the boot-0 count (R32-C1)' 1 DEGRADED \
    'err=3 \(coredump=3 kernel=0 other=0\)' \
    '^HANDOFF ADJ-04 mori class=coredumps value=3 kind=dated-event state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER$'

  case_home='handoff-cumulative-only'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'oom_kill 3\n' > "$FX/vmstat"
  check 'healthy: a cumulative vmstat oom_kill counter never routes a kill-events handoff (R32-C1)' 0 HEALTHY \
    'ledger=vmstat\.oom_kill=3' \
    'ABSENT:^HANDOFF'

  # ---- round 35 (C1): the pacnew/pacsave drift arm ---------------------------------
  case_home='drift-counts'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/etc/a/b" "$FX/etc/d.pacnew"
  : > "$FX/etc/a/x.conf.pacnew"; : > "$FX/etc/a/b/y.pacsave"; : > "$FX/etc/a/b/y.pacsave.1"
  : > "$FX/etc/z.pacorig"; : > "$FX/etc/a/x.conf.pacnew.bak"; : > "$FX/etc/a/q.pacsave~"
  ln -s /nonexistent-r35 "$FX/etc/a/l.pacnew"
  check 'healthy: the drift arm counts pacdiff names and symlinks, never directories or near-names (R35-C1)' 0 HEALTHY \
    '^DRIFT pacnew-plane pacnew=2 pacsave=2 pacorig=1 unreadable=0 log_pacnew=0 log_pacsave=0 unlogged=5 gone=0 log=ok$'

  case_home='drift-pairing'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/etc/a" "$FX/etc/b"
  : > "$FX/etc/a/x.pacnew"; : > "$FX/etc/b/x.pacnew"; : > "$FX/etc/a/s.pacsave"
  { printf '%s\n' \
      '[2026-10-11T16:14:18-0300] [ALPM] warning: /etc/a/x installed as /etc/a/x.pacnew' \
      '[2026-10-11T16:14:19-0300] [ALPM] warning: /etc/a/s saved as /etc/a/s.pacsave' \
      '[2026-10-11T16:14:20-0300] [ALPM] warning: /etc/c/x installed as /etc/c/x.pacnew' \
      '[2026-10-11T16:14:21-0300] [ALPM] warning: /etc/a/m installed as /etc/b/m.pacnew' \
      '[2026-10-11T16:14:22-0300] [ALPM] warning: /usr/share/u installed as /usr/share/u.pacnew' \
      '[2026-10-11T16:14:23-0300] [ALPM] installed asdcontrol (1:0.6.0-1)'
    cat "$FX/pacman.log"; } > "$FX/pacman.log.new"
  mv "$FX/pacman.log.new" "$FX/pacman.log"
  check 'healthy: the drift arm pairs /etc warnings by full path; unlogged and gone (R35-C1)' 0 HEALTHY \
    '^DRIFT pacnew-plane pacnew=2 pacsave=1 pacorig=0 unreadable=0 log_pacnew=2 log_pacsave=1 unlogged=1 gone=1 log=ok$'

  case_home='drift-unreadable'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/etc/k" "$FX/etc/o"
  : > "$FX/etc/k/h.pacnew"; : > "$FX/etc/o/v.pacnew"
  { printf '%s\n' '[2026-10-11T16:14:18-0300] [ALPM] warning: /etc/k/h installed as /etc/k/h.pacnew'
    cat "$FX/pacman.log"; } > "$FX/pacman.log.new"
  mv "$FX/pacman.log.new" "$FX/pacman.log"
  chmod 000 "$FX/etc/k"
  check 'healthy: an unreadable directory is reported, and its logged target is neither present nor gone (R35-C1)' 0 HEALTHY \
    '^DRIFT pacnew-plane pacnew=1 pacsave=0 pacorig=0 unreadable=1 log_pacnew=1 log_pacsave=0 unlogged=1 gone=0 log=ok$'
  chmod 755 "$FX/etc/k"

  case_home='drift-no-log'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/etc/w.pacnew"
  EXTRA_ENV=(TSUKUROI_PACMAN_LOG="$FX/absent.log")
  check 'healthy: an absent log prints log=unreadable and zero log counts, never a pass on pairing (R35-C1)' 0 HEALTHY \
    '^DRIFT pacnew-plane pacnew=1 pacsave=0 pacorig=0 unreadable=0 log_pacnew=0 log_pacsave=0 unlogged=1 gone=0 log=unreadable$'

  # ---- round 38 (C1): the storage-integrity arm (verdict-neutral) -------------------
  EXTRA_ENV=()
  local sfs=11111111-2222-3333-4444-555555555555 sfs2=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
  st_write() { # st_write FILE w r f c g -> one error_stats file in sysfs order
    mkdir -p "${1%/*}"
    printf 'write_errs %s\nread_errs %s\nflush_errs %s\ncorruption_errs %s\ngeneration_errs %s\n' "$2" "$3" "$4" "$5" "$6" > "$1"
  }
  case_home='storage-absent'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: no btrfs sysfs root reads as no btrfs filesystem, 0/0/0 (R38-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0$'

  case_home='storage-zero'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  st_write "$FX/btrfs/$sfs/devinfo/1/error_stats" 0 0 0 0 0
  mkdir -p "$FX/btrfs/features" "$FX/btrfs/$sfs/features"; : > "$FX/btrfs/not-a-uuid"
  check 'healthy: five zero counters on one device; features and non-fsid names ignored (R38-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0$'

  case_home='storage-nonzero'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  st_write "$FX/btrfs/$sfs/devinfo/1/error_stats" 1 0 0 3 0
  st_write "$FX/btrfs/$sfs2/devinfo/2/error_stats" 0 0 0 0 010
  check 'healthy rollup: nonzero lifetime counters read DEGRADED on the STORAGE line only; 010 is ten, not octal (R38-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=DEGRADED filesystems=2 devices=2 nonzero=3 detail=11111111:1:write_errs=1,11111111:1:corruption_errs=3,aaaaaaaa:2:generation_errs=010$' \
    '^TSUKUROI_CENSUS: HEALTHY '

  case_home='storage-malformed'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1"
  printf 'write_errs 0\nread_errs 0\nflush_errs 0\ncorruption_errs 0\n' > "$FX/btrfs/$sfs/devinfo/1/error_stats"
  st_write "$FX/btrfs/$sfs/devinfo/2/error_stats" 0 2 0 0 0
  check 'healthy rollup: a missing counter is BLOCKED; the healthy sibling device still counts (R38-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=2 nonzero=1 detail=11111111:1:malformed,11111111:2:read_errs=2$'

  case_home='storage-duplicate'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  st_write "$FX/btrfs/$sfs/devinfo/1/error_stats" 0 0 0 0 0
  printf 'read_errs 0\n' >> "$FX/btrfs/$sfs/devinfo/1/error_stats"
  check 'healthy rollup: a repeated counter or extra line is malformed, never a pass (R38-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:malformed$'

  case_home='storage-no-devinfo'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/features"
  check 'healthy rollup: a mounted filesystem with no readable devinfo is BLOCKED (R38-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=0 nonzero=0 detail=11111111:-:no-devinfo$'

  case_home='storage-bad-devid'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  st_write "$FX/btrfs/$sfs/devinfo/1 x/error_stats" 0 0 0 0 0
  check 'healthy rollup: a non-integer devid is BLOCKED and its name is never echoed (R38-W1 hardening)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:\?:bad-devid$'

  case_home='storage-root-unreadable'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  st_write "$FX/btrfs/$sfs/devinfo/1/error_stats" 0 0 0 0 0
  chmod 000 "$FX/btrfs"
  check 'healthy rollup: an unlistable btrfs sysfs root is BLOCKED, never a silent 0/0/0 (R38-W1 hardening)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=root:unreadable$'
  chmod 755 "$FX/btrfs"

  # ---- round 39 (C1, R38-ABSENT-ROOT): the mount table guards an absent or empty root --------
  local fxmt='/dev/mapper/root / btrfs rw,noatime,subvolid=256,subvol=/@ 0 0'
  case_home='storage-hidden-absent'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'proc /proc proc rw 0 0\n%s\n' "$fxmt" > "$FX/mounts"
  check 'healthy rollup: btrfs mounted with no sysfs root is BLOCKED, never 0/0/0 (R39-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'

  case_home='storage-hidden-empty'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/features"; printf '%s\n' "$fxmt" > "$FX/mounts"
  check 'healthy rollup: btrfs mounted with a root holding no fsid is BLOCKED (R39-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'

  case_home='storage-mounts-unreadable'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  rm -f "$FX/mounts"
  check 'healthy rollup: an unreadable mount table with no sysfs root is BLOCKED (R39-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:unreadable$'

  case_home='storage-mounted-populated'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  st_write "$FX/btrfs/$sfs/devinfo/1/error_stats" 0 0 0 0 0; printf '%s\n' "$fxmt" > "$FX/mounts"
  check 'healthy: a root with an fsid entry is read and the mount table adds nothing (R39-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0$'

  case_home='storage-mounts-fifo'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  rm -f "$FX/mounts"; mkfifo "$FX/mounts"
  check 'healthy rollup: a FIFO as the mount table is BLOCKED and never read, so it cannot hang (R39-W1 hardening)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:unreadable$'

  case_home='storage-mounts-empty'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/mounts"
  check 'healthy rollup: an empty mount table is no table, BLOCKED not 0/0/0 (R39-W1 hardening)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:unreadable$'

  # ---- round 40 (C1, R39-FIXTURE-MONOCULTURE): the btrfs mount line varies in device, mountpoint,
  # options, subvolume and position, and btrfs-looking text outside the fstype field is not a btrfs mount
  case_home='storage-mounts-varied-home'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0' \
    '/dev/nvme0n1p3 /home btrfs rw,relatime,ssd,discard=async,space_cache=v2,subvolid=5,subvol=/ 0 0' \
    'tmpfs /tmp tmpfs rw,nosuid,nodev 0 0' > "$FX/mounts"
  check 'healthy rollup: a btrfs /home on another device and options, not last, is BLOCKED (R40-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'

  case_home='storage-mounts-varied-multi'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/features"
  printf '%s\n' 'sysfs /sys sysfs rw,nosuid,nodev,noexec,relatime 0 0' 'UUID=0b1c /boot vfat rw,relatime 0 0' \
    '/dev/sda2 /var/lib/machines btrfs ro,noatime,compress=zstd:3,subvolid=263,subvol=/machines 0 0' \
    '/dev/sdb1 /srv ext4 rw,relatime 0 0' > "$FX/mounts"
  check 'healthy rollup: one read-only btrfs mount among four lines, empty root, is BLOCKED (R40-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'

  case_home='storage-mounts-btrfs-in-path'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' 'proc /proc proc rw 0 0' \
    '/dev/disk/by-label/btrfs-old /mnt/btrfs-backup ext4 rw,relatime,comment=btrfs 0 0' > "$FX/mounts"
  check 'healthy: btrfs in the device, mountpoint or options of an ext4 line is no btrfs mount (R40-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0$'

  case_home='storage-mounts-fstype-case'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' 'proc /proc proc rw 0 0' '/dev/fx0 / BTRFS rw,relatime 0 0' > "$FX/mounts"
  check 'healthy: the fstype match is exact, so BTRFS is not btrfs (R40-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0$'

  # ---- round 41 (C1, round-40 held-out survivors H5, H6, H9 and count direction H10): a btrfs line counts
  # by its fstype field alone; each table varies one shape the round-40 tables all shared
  case_home='storage-mounts-mp-relative'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0' \
    '/dev/vdc1 relative/mnt btrfs rw,relatime,subvolid=5,subvol=/ 0 0' > "$FX/mounts"
  check 'healthy rollup: a btrfs line whose mountpoint is not absolute still counts, BLOCKED (R41-C1 H5)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'

  case_home='storage-mounts-src-uuid'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0' \
    'UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8 /data btrfs rw,relatime,subvolid=5,subvol=/ 0 0' > "$FX/mounts"
  check 'healthy rollup: a btrfs line whose source is not under /dev still counts, BLOCKED (R41-C1 H6)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'

  case_home='storage-mounts-no-subvol-opt'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0' \
    '/dev/sdc1 /mnt/plain btrfs rw,commit=60 0 0' > "$FX/mounts"
  check 'healthy rollup: a btrfs line with no subvol= option still counts, BLOCKED (R41-C1 H9)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'

  case_home='storage-mounts-two-btrfs'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' '/dev/nvme0n1p2 / btrfs rw,relatime,ssd,subvolid=256,subvol=/@ 0 0' \
    'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0' \
    '/dev/nvme0n1p2 /home btrfs rw,relatime,ssd,subvolid=257,subvol=/@home 0 0' > "$FX/mounts"
  check 'healthy rollup: two btrfs lines are still btrfs without sysfs, BLOCKED (R41-C1 H10)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'

  case_home='storage-root-unreadable-mounted'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  st_write "$FX/btrfs/$sfs/devinfo/1/error_stats" 0 0 0 0 0
  printf '%s\n' 'proc /proc proc rw 0 0' '/dev/vdb /data btrfs rw,relatime,subvolid=5,subvol=/ 0 0' > "$FX/mounts"
  chmod 000 "$FX/btrfs"
  check 'healthy rollup: an unlistable root keeps its one reason; the mount table is never added (R40-C1)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=root:unreadable$'
  chmod 755 "$FX/btrfs"

  # ---- round 44 (C1): the scrub-record arm (verdict-neutral; names and stat, never content) -----
  case_home='scrub-absent'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: no record directory, no sysfs root, no wants directory reads NONE with zero counts (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0$'

  case_home='scrub-recorded'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1" "$FX/scrub"; printf '0\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"
  printf 'scrub status:1\n' > "$FX/scrub/scrub.status.$sfs"; chmod 644 "$FX/scrub/scrub.status.$sfs"
  : > "$FX/scrub/notes.txt"; : > "$FX/scrub/scrub.status.NOT-A-UUID"
  check 'healthy: one readable record of a mounted fsid reads RECORDED; other names are ignored (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0$'

  case_home='scrub-tmp-orphan-unreadable'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1" "$FX/scrub"; printf '0\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"
  printf 'scrub status:1\n' > "$FX/scrub/scrub.status.$sfs"; chmod 000 "$FX/scrub/scrub.status.$sfs"
  printf 'scrub status:1\n' > "$FX/scrub/scrub.status.$sfs2"; chmod 644 "$FX/scrub/scrub.status.$sfs2"
  printf 'scrub status:1\nlonger tail\n' > "$FX/scrub/scrub.status.${sfs}_tmp"; chmod 600 "$FX/scrub/scrub.status.${sfs}_tmp"
  check 'healthy: a 000 record is unreadable, a record of an unmounted fsid is an orphan, a _tmp counts apart (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=RECORDED dir=present records=2 tmp=1 sockets=0 unreadable=1 orphan=1 limited=0 timers=0$'
  chmod 644 "$FX/scrub/scrub.status.$sfs"

  case_home='scrub-limited'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1" "$FX/btrfs/$sfs/devinfo/2"
  printf '0\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"; printf '104857600\n' > "$FX/btrfs/$sfs/devinfo/2/scrub_speed_max"
  check 'healthy: a nonzero scrub_speed_max counts as limited and is listed; 0 is no limit (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:2:speed_max=104857600$'

  case_home='scrub-speed-malformed'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1" "$FX/btrfs/$sfs/devinfo/3"
  printf 'fast\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"
  check 'healthy rollup: a non-decimal limit is BLOCKED and a missing limit file is unreadable, never no-limit (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:1:speed-malformed,11111111:3:speed-unreadable$' \
    '^TSUKUROI_CENSUS: HEALTHY '

  case_home='scrub-dir-unreadable'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/scrub"; printf 'scrub status:1\n' > "$FX/scrub/scrub.status.$sfs"; chmod 000 "$FX/scrub"
  check 'healthy rollup: an unlistable record directory is BLOCKED, never an absent record (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=BLOCKED dir=unreadable records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=dir:unreadable$'
  chmod 755 "$FX/scrub"

  case_home='scrub-timers'; FX="$work/fx/$case_home"; mkdir -p "$FX/wants"; fx_default "$FX"
  ln -s /usr/lib/systemd/system/btrfs-scrub@.timer "$FX/wants/btrfs-scrub@-.timer"
  ln -s /usr/lib/systemd/system/btrfs-scrub@.timer "$FX/wants/btrfs-scrub@home.timer"
  : > "$FX/wants/btrfs-scrub@.timer"; : > "$FX/wants/fstrim.timer"; : > "$FX/wants/btrfs-scrub.timer"; : > "$FX/wants/btrfs-scrub@home-timer"
  check 'healthy: enabled scrub timer instances count by link name; the bare template and other timers do not (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=2$'

  case_home='scrub-wrong-types'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1" "$FX/scrub/scrub.status.$sfs2"; printf '0\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"
  ln -s /etc/hostname "$FX/scrub/scrub.status.$sfs"; mkfifo "$FX/scrub/scrub.progress.$sfs"
  : > "$FX/scrub/scrub.status.$sfs"$'\n''TSUKUROI_CENSUS: HEALTHY (forged)'
  check 'healthy rollup: a symlinked or directory record and a non-socket progress name are BLOCKED; a newline name is never echoed (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=BLOCKED dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=progress:not-socket,record:not-regular,record:not-regular$' \
    'ABSENT:^TSUKUROI_CENSUS: HEALTHY \(forged'

  case_home='scrub-sysfs-absent'; FX="$work/fx/$case_home"; mkdir -p "$FX/scrub"; fx_default "$FX"
  local srec="$FX/scrub/scrub.status.$sfs"
  printf 'scrub status:1\n' > "$srec"; chmod 644 "$srec"
  check 'healthy rollup: records with no sysfs root to judge orphans by are BLOCKED (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=BLOCKED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=sysfs:absent$'

  # ---- round 44 wave-1 hardening (C1MutSelftest survivors; each case is red on its mutant) ----
  case_home='scrub-locale-fsid'; FX="$work/fx/$case_home"; mkdir -p "$FX/btrfs" "$FX/scrub"; fx_default "$FX"
  local lfs=$'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa\xc3\xa1a'
  mkdir -p "$FX/btrfs/$lfs/devinfo/1"; printf '0\n' > "$FX/btrfs/$lfs/devinfo/1/scrub_speed_max"
  printf 'scrub status:1\n' > "$FX/scrub/scrub.status.$lfs"; chmod 644 "$FX/scrub/scrub.status.$lfs"
  EXTRA_ENV=(LC_ALL=en_US.UTF-8)
  check 'healthy: the probe pins LC_ALL=C so a collation-inflated name is never a uuid (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0$'

  case_home='scrub-speed-empty'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1"; printf '\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"
  check 'healthy rollup: an empty scrub_speed_max line is malformed, never a silent no-limit (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:1:speed-malformed$'

  case_home='scrub-speed-zero-padded'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1"; printf '000\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"
  check 'healthy: a zero-padded scrub_speed_max is still no limit (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0$'

  case_home='scrub-tmp-only'; FX="$work/fx/$case_home"; mkdir -p "$FX/btrfs/$sfs/devinfo/1" "$FX/scrub"; fx_default "$FX"
  printf '0\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"
  printf 'scrub status:1\n' > "$FX/scrub/scrub.status.${sfs}_tmp"; chmod 600 "$FX/scrub/scrub.status.${sfs}_tmp"
  check 'healthy: an in-progress _tmp record alone reads RECORDED with zero finished records (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=RECORDED dir=present records=0 tmp=1 sockets=0 unreadable=0 orphan=0 limited=0 timers=0$'

  case_home='scrub-detail-info-both'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1" "$FX/btrfs/$sfs/devinfo/2"
  printf 'fast\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"; printf '104857600\n' > "$FX/btrfs/$sfs/devinfo/2/scrub_speed_max"
  check 'healthy rollup: detail evidence precedes limit info in the detail join (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:1:speed-malformed,11111111:2:speed_max=104857600$'

  case_home='scrub-sysfs-not-dir'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '0\n' > "$FX/btrfs"; mkdir -p "$FX/scrub"
  printf 'scrub status:1\n' > "$FX/scrub/scrub.status.$sfs"; chmod 644 "$FX/scrub/scrub.status.$sfs"
  check 'healthy rollup: a sysfs root that exists but is not a directory is BLOCKED, never a silent no-orphan scan (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=BLOCKED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=sysfs:not-directory$'

  case_home='scrub-timers-dir'; FX="$work/fx/$case_home"; mkdir -p "$FX/wants"; fx_default "$FX"
  mkdir -p "$FX/wants/btrfs-scrub@x.timer"
  check 'healthy: a directory named like a scrub timer is not an enabled instance (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0$'

  # Round 45 (C1; routed since round 42, R43 item 3): five probe readers kept only the first line of a captured
  # output through `printf '%s\n' "$CAP_OUT" | head -n1` in an assignment. Under `set -euo pipefail` an output past
  # the pipe buffer killed the census with exit 141 (the R41-CENSUS-PIPEFAIL-692 class). Each case below puts the
  # deciding first line in front of ~150 KB of padding; the last case drives the foreign-baseline lookup (the
  # round-42 full-read form) past the pipe buffer with the deciding row at the end of the baseline.
  r45pad() { awk -v t="$1" 'BEGIN { for (i = 0; i < 2000; i++) printf "%s padding line %05d ..................................................\n", t, i }'; }

  case_home='r45-sysrunning-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  { printf 'degraded\n'; r45pad sysrunning; } > "$FX/sysrunning"; printf 1 > "$FX/sysrunning.rc"
  check 'degraded: a large is-system-running output keeps its first line (R45-C1)' 1 DEGRADED \
    '^PLANE systemd: DEGRADED .*state=degraded failed=0 '

  case_home='r45-timerresult-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  { printf 'failed\n'; r45pad result; } > "$FX/timerresult"
  check 'degraded: a large timer Result output keeps its first line (R45-C1)' 1 DEGRADED \
    '^PLANE systemd: DEGRADED .*timer_fail=1 timer_unknown=0 \(ai-usage\.timer=failed \)\)$'

  case_home='r45-smi-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/pci/0000:01:00.0"; printf '0x10de\n' > "$FX/pci/0000:01:00.0/vendor"
  { printf 'NVIDIA GeForce RTX 5070, 610.57.04\n'; r45pad 'NVIDIA GeForce RTX 5070, 999.99.99'; } > "$FX/smi.out"; printf 0 > "$FX/smi.rc"
  printf 'nvidia 12345678 42\nnvidia_uvm 1234567 0\n' > "$FX/lsmod"
  : > "$FX/dev/nvidia0"; : > "$FX/dev/nvidiactl"
  check 'healthy: a large nvidia-smi output keeps the first GPU line (R45-C1)' 0 HEALTHY \
    '^PLANE drivers: HEALTHY .*smi=610\.57\.04 '

  case_home='r45-boottarget-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  { printf 'inactive \t\r\n'; r45pad active; } > "$FX/boottarget"; printf 3 > "$FX/boottarget.rc"
  check 'blocked: a large is-active output keeps its first word, trailing blanks and CR dropped (R45-C1)' 2 BLOCKED \
    '^PLANE journal: BLOCKED \(boot target graphical\.target=inactive \[boot did not reach graphical\.target\]'

  case_home='r45-timeractive-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  { printf 'inactive\n'; r45pad active; } > "$FX/timeractivestate"
  check 'degraded: a large timer ActiveState output keeps its first line (R45-C1)' 1 DEGRADED \
    '^PLANE journal: DEGRADED .*timer_drift=1 .*\(ai-usage\.timer=inactive\)'

  case_home='r45-foreign-baseline-large'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  { printf '%s\n' "$r6base"
    awk 'BEGIN { for (i = 0; i < 2000; i++) printf "zz-r45-baseline-padding-package-%05d 1.0-1\n", i }'; } > "$FX/fbase"
  { printf '%s\n' "$r6base"
    awk 'BEGIN { for (i = 0; i < 1999; i++) printf "zz-r45-baseline-padding-package-%05d 1.0-1\n", i
                 printf "zz-r45-baseline-padding-package-01999 1.0-2\n" }'; } > "$FX/pm"
  check 'degraded: a foreign baseline past the pipe buffer still finds its last row (R45-C1)' 1 DEGRADED \
    '^PLANE packages: DEGRADED .*foreign=2016\(known=2015 new=0 drift=1 gone=0\) base=file\(2016\) drift=\[zz-r45-baseline-padding-package-01999\(1\.0-1->1\.0-2\)\]'

  check_cli 'cli: unknown argument exits 2 with usage (S10-2)' 2 \
    '^usage: tsukuroi-census\.sh' -- --bogus
  check_cli 'cli: --sample 0 refuses before the parse continues (S10-2)' 2 \
    '--sample needs a positive integer' -- --sample 0 --bogus
  check_cli 'cli: --help prints usage and exits 0 (S10-2)' 0 \
    '^usage: tsukuroi-census\.sh' -- --help

  # ---- round 46 (C1): --identity, the one-command census identity (routed debt D12) ----
  # Expected values are computed here with sha256sum/md5sum/wc over the same file, never read
  # back from the identity line; the copy, symlink and stdin cases kill a constant writer and a
  # path hasher (a decoy regular file named `bash` sits in the stdin case's cwd).
  id_line() { # id_line FILE-FOR-EXPECTED -> the four byte fields as the identity prints them
    printf 'sha256=%s md5=%s bytes=%s lines=%s' "$(sha256sum < "$1" | cut -d' ' -f1)" \
      "$(md5sum < "$1" | cut -d' ' -f1)" "$(wc -c < "$1")" "$(wc -l < "$1")"
  }
  id_check() { # id_check LABEL WANT-FIELDS OUTPUT RC
    local label=$1 want=$2 out=$3 rc=$4 planes
    planes=$(grep -E "^  printf 'TSUKUROI_CENSUS: %s \(" "$SELF" | head -n1 | grep -oE '[a-z-]+=%s' | sed 's/=%s$//' | paste -sd, -)
    if [ "$rc" -ne 0 ]; then
      bad "$label: exit $rc wanted 0; output: $(printf '%s' "$out" | tr '\n' '|')"
    elif [ "$(printf '%s\n' "$out" | grep -c .)" -ne 1 ]; then
      bad "$label: wanted exactly one line; got: $(printf '%s' "$out" | tr '\n' '|')"
    elif [[ "$out" != "TSUKUROI_CENSUS_IDENTITY: version=$VERSION $want planes=$planes exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified="* ]]; then
      bad "$label: wanted '$want' planes=$planes; got: $out"
    else
      ok "$label (exit $rc)"
    fi
  }
  local idd id_out id_rc id_self_want id_copy_want id_abs
  id_abs=$(readlink -f -- "$SELF")
  idd="$work/identity"
  mkdir -p "$idd/dec"
  cp -- "$SELF" "$idd/copy.sh"
  printf '\n# r46 identity selftest copy\n' >> "$idd/copy.sh"   # the census ends without a newline
  ln -s -- "$id_abs" "$idd/link.sh"
  { cat -- "$SELF"; printf '# decoy\n'; } > "$idd/dec/bash"
  id_self_want=$(id_line "$SELF")
  id_copy_want=$(id_line "$idd/copy.sh")
  set +e
  id_out=$("$BASH" "$SELF" --identity 2>&1); id_rc=$?
  set -e
  id_check 'identity: one line naming this file, digests recomputed here, verified=yes (R46-C1)' \
    "$id_self_want" "$id_out" "$id_rc"
  [[ "$id_out" == *' verified=yes' ]] || bad 'identity: this file must read verified=yes (R46-C1)'
  set +e
  id_out=$("$BASH" "$idd/copy.sh" --identity 2>&1); id_rc=$?
  set -e
  if [ "$id_copy_want" = "$id_self_want" ]; then
    bad 'identity: a one-line copy must change every byte field (R46-C1)'
  else
    id_check 'identity: a copy with one appended line reports its own bytes, not a constant (R46-C1)' \
      "$id_copy_want" "$id_out" "$id_rc"
  fi
  set +e
  id_out=$("$BASH" "$idd/link.sh" --identity 2>&1); id_rc=$?
  set -e
  id_check 'identity: a symlink invocation reports the target file (R46-C1)' "$id_self_want" "$id_out" "$id_rc"
  set +e
  id_out=$(cd "$idd/dec" && "$BASH" -s -- --identity < "$id_abs" 2>&1); id_rc=$?
  set -e
  id_check 'identity: a script read from stdin prints unverifiable, never a decoy file named bash (R46-C1)' \
    'sha256=unverifiable md5=unverifiable bytes=unverifiable lines=unverifiable' "$id_out" "$id_rc"
  [[ "$id_out" == *' verified=no' ]] || bad 'identity: a stdin script must read verified=no (R46-C1)'
  { printf 'mv -f -- "$R46_DECOY" "$R46_PATH"\n'; cat -- "$SELF"; } > "$idd/repl.sh"
  { cat -- "$SELF"; printf '\n# decoy\n'; } > "$idd/repl.decoy"
  set +e
  id_out=$(R46_DECOY="$idd/repl.decoy" R46_PATH="$idd/repl.sh" "$BASH" "$idd/repl.sh" --identity 2>&1); id_rc=$?
  set -e
  id_check 'identity: a file replaced after bash opened it prints unverifiable, never the new bytes (R46-C1)' \
    'sha256=unverifiable md5=unverifiable bytes=unverifiable lines=unverifiable' "$id_out" "$id_rc"
  check_cli 'cli: --identity with another flag exits 2 (R46-C1)' 2 \
    '--identity takes no other argument' -- --identity --selftest

  printf 'TSUKUROI_CENSUS_SELFTEST: %s (%d cases, %d passed, %d failed)\n' \
    "$([ "$FAIL" -eq 0 ] && printf PASS || printf FAIL)" "$((PASS + FAIL))" "$PASS" "$FAIL"
  [ "$FAIL" -eq 0 ]
}

# ---- --identity (round 46, C1): one-command census identity (routed debt D12) ---------
# Prints ONE line naming the bytes this bash process executes, so a reader re-derives the
# census revision with one command (closeout-r11.md D12: identity is by hash, not VERSION).
# The digests are read through the descriptor bash holds open on the script (bash opens the
# script file and moves it to a high descriptor, normally 255), re-opened as /proc/$$/fd/<n>,
# and only when that descriptor resolves to the same file as $SELF. A script read from stdin
# or from a pipe has no such descriptor: the four byte fields then print `unverifiable` and
# verified=no — a path is never hashed on trust. sha256 is taken again after the other
# fields; a change in between also reads unverifiable. Reads /proc and the script only;
# writes nothing; runs no plane probe. Exit 0.
CENSUS_PLANES='packages,systemd,drivers,journal,update-safety,oom'
census_identity() {
  local self_real fdp='' p sha md5 bytes lines sha2
  local f_sha=unverifiable f_md5=unverifiable f_bytes=unverifiable f_lines=unverifiable verified=no
  self_real=$(readlink -f -- "$SELF" 2>/dev/null || true)
  if [ -n "$self_real" ] && [ -f "$self_real" ]; then
    for p in "/proc/$$/fd/255" /proc/$$/fd/*; do
      case "${p##*/}" in '' | *[!0-9]*) continue ;; esac
      [ "${p##*/}" -ge 10 ] || continue
      [ -f "$p" ] || continue
      if [ "$(readlink -- "$p" 2>/dev/null || true)" = "$self_real" ]; then fdp=$p; break; fi
    done
  fi
  if [ -n "$fdp" ]; then
    sha=$(sha256sum < "$fdp" 2>/dev/null | cut -d' ' -f1 || true)
    md5=$(md5sum < "$fdp" 2>/dev/null | cut -d' ' -f1 || true)
    bytes=$(wc -c < "$fdp" 2>/dev/null || true)
    lines=$(wc -l < "$fdp" 2>/dev/null || true)
    sha2=$(sha256sum < "$fdp" 2>/dev/null | cut -d' ' -f1 || true)
    if [[ "$sha" =~ ^[0-9a-f]{64}$ && "$md5" =~ ^[0-9a-f]{32}$ && "$bytes" =~ ^[0-9]+$ \
      && "$lines" =~ ^[0-9]+$ && "$sha2" = "$sha" ]]; then
      f_sha=$sha f_md5=$md5 f_bytes=$bytes f_lines=$lines verified=yes
    fi
  fi
  printf 'TSUKUROI_CENSUS_IDENTITY: version=%s sha256=%s md5=%s bytes=%s lines=%s planes=%s exit_map=%s verified=%s\n' \
    "$VERSION" "$f_sha" "$f_md5" "$f_bytes" "$f_lines" "$CENSUS_PLANES" '0:HEALTHY,1:DEGRADED,2:BLOCKED' "$verified"
}

# ---- main --------------------------------------------------------------------
main() {
  local selftest=0 identity=0 nargs=$#
  while [ $# -gt 0 ]; do
    case "$1" in
      --identity) identity=1; shift ;;
      --selftest) selftest=1; shift ;;
      --sample)
        SAMPLE_N=${2:-}
        case "$SAMPLE_N" in
          '' | *[!0-9]*) printf 'tsukuroi-census: --sample needs a positive integer\n' >&2; exit 2 ;;
        esac
        [ "$SAMPLE_N" -gt 0 ] || { printf 'tsukuroi-census: --sample needs a positive integer\n' >&2; exit 2; }
        shift 2
        ;;
      --help | -h) usage; exit 0 ;;
      *) printf 'tsukuroi-census: unknown argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
    esac
  done

  if [ "$identity" -eq 1 ]; then # round 46 (C1): --identity stands alone, before any probe
    if [ "$nargs" -ne 1 ]; then
      printf 'tsukuroi-census: --identity takes no other argument\n' >&2; usage >&2; exit 2
    fi
    census_identity
    exit 0
  fi

  if [ "$selftest" -eq 1 ]; then
    run_selftest
    return
  fi

  local host
  host=$(head -n1 "$HOSTNAME_FILE" 2>/dev/null | tr -d '\r' || true)
  host=${host:-unknown}
  printf 'tsukuroi-census %s — host=%s — %s — read-only\n' \
    "$VERSION" "$host" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  probe_packages
  probe_root_meta
  PKG_V=$(worse "$PKG_V" "$ROOT_V")
  probe_systemd
  probe_drivers
  probe_mem_arm
  DRV_V=$(worse "$DRV_V" "$MEM_V")
  probe_journal
  probe_update_safety
  probe_oom_plane

  printf 'PLANE packages: %s (%s; %s)\n' "$PKG_V" "$PKG_NOTE" "$ROOT_NOTE"
  printf 'PLANE systemd: %s (%s)\n' "$SYS_V" "$SYS_NOTE"
  printf 'PLANE drivers: %s (%s; mem=%s)\n' "$DRV_V" "$DRV_NOTE" "$MEM_NOTE"
  printf 'PLANE journal: %s (%s)\n' "$JRN_V" "$JRN_NOTE"
  printf 'PLANE update-safety: %s (%s)\n' "$UPD_V" "$UPD_NOTE"
  printf 'PLANE oom: %s (%s)\n' "$OOM_V" "$OOM_NOTE"

  # ---- ADJ-04 handoff (round 32, C1): the sibling-owned classes routed to mori --------
  # Printed after the six PLANE lines and before the rollup; they change no PLANE text,
  # no rollup term and no exit code (tsukuroi keeps the OS finding). Routing is
  # unconditional and reads only what the probes already measured: a class is prepared
  # when its dated-event count is >= 1. A cumulative counter (vmstat oom_kill, a
  # memory.events oom_kill flag) never becomes a kill-events line by construction — the
  # value is the oom plane's clustered journal events, not the ledger. See the header's
  # HANDOFF contract paragraph for the prepared/not-acknowledged stance and for why
  # value= is the census's own count rather than one of mori's catalog counts.
  if [ "$OOM_CLUSTERS" -ge 1 ]; then
    printf 'HANDOFF ADJ-04 mori class=kill-events value=%s kind=dated-event state=prepared window=%s source=journal-window\n' \
      "$OOM_CLUSTERS" "${OOM_WINDOW// /:}"
  fi
  if [ "$JRN_COREDUMPS" -ge 1 ]; then
    printf 'HANDOFF ADJ-04 mori class=coredumps value=%s kind=dated-event state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER\n' \
      "$JRN_COREDUMPS"
  fi

  # ---- pacnew/pacsave drift arm (round 35, C1): one verdict-neutral line ----------
  probe_pacnew_arm
  printf '%s\n' "$DRIFT_LINE"

  # ---- storage-integrity arm (round 38, C1): one verdict-neutral line ---------------
  probe_storage_arm
  printf '%s\n' "$STORAGE_LINE"

  # ---- scrub-record arm (round 44, C1): one verdict-neutral line ----------------------------
  probe_scrub_record
  printf '%s\n' "$SCRUB_LINE"

  local roll=HEALTHY
  roll=$(worse "$roll" "$PKG_V")
  roll=$(worse "$roll" "$SYS_V")
  roll=$(worse "$roll" "$DRV_V")
  roll=$(worse "$roll" "$JRN_V")
  roll=$(worse "$roll" "$UPD_V")
  roll=$(worse "$roll" "$OOM_V")

  printf 'TSUKUROI_CENSUS: %s (packages=%s systemd=%s drivers=%s journal=%s update-safety=%s oom=%s)\n' \
    "$roll" "$PKG_V" "$SYS_V" "$DRV_V" "$JRN_V" "$UPD_V" "$OOM_V"

  case "$roll" in
    HEALTHY)  exit 0 ;;
    DEGRADED) exit 1 ;;
    BLOCKED)  exit 2 ;;
    *)        exit 2 ;;
  esac
}

main "$@"