source: S114 (earlyoom v1.9.0 README at tag v1.9.0 = commit 202d4db0d308ca6478f68de68b46cae34896ddaf — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md — the act rule, the staged SIGTERM-then-SIGKILL order, where actions are logged, the journal-reading advice and the v1.9.0 changelog; sha256 23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd, opened 2026-10-22); S115 (earlyoom v1.9.0 MANPAGE.md at the same tag — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md — the both-below rule, the PERCENT/2 kill default and the `user mem total` definition; sha256 cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda, opened 2026-10-22); S116 (earlyoom v1.9.0 meminfo.c at the same tag — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c — the memory and swap percentages earlyoom compares against its limits; sha256 526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb, opened 2026-10-22); S117 (earlyoom tag history — https://github.com/rfjakob/earlyoom/releases and https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c — the v1.9.0 tag and commit, the v1.2 removal of the kernel-oom option and its 2026-02-02 re-introduction on master; opened 2026-10-22); S118 (earlyoom v1.9.0 kill.c and msg.c at the same tag — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c and https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.c — the action, escalation and kill-failure literals, the signal-delivery path, the `warn()`/`info()` write targets and the `"%5.2lf%%"` percentage format; sha256 b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3 and a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197, opened 2026-10-22); S119 (earlyoom v1.9.0 main.c at the same tag — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c — the two startup threshold literals, the act decision, the compiled defaults, the dry-run and low-memory literals and the version literal; sha256 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4, opened 2026-10-22); S120 (earlyoom v1.9.0 service unit template and the installed Arch package — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in and `pacman -Qi earlyoom` on this host — the unit's EnvironmentFile/ExecStart shape, the package version 1.9.0-1 and its install date; sha256 d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd, opened 2026-10-22); S121 (systemd v262 oomd-util.c and message catalog — https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c and https://raw.githubusercontent.com/systemd/systemd/v262/catalog/systemd.catalog.in — oomd's own kill accounting and the d989611b… notice id; sha256 2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a and e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592, opened 2026-10-22); S122 (systemd v262 journal documentation — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html and https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html — `journalctl -q -b -u`, `--output-fields=`, the `MESSAGE`/`MESSAGE_ID` field semantics and `_TRANSPORT=kernel`; systemd 262 man pages opened 2026-10-22); S123 (systemd v262 logs-show.c and utf8.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c and https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/utf8.c — how `journalctl` emits the requested journal fields (`logs-show.c:554` parses `MESSAGE=`, `:1456`/`:1459` emit `MESSAGE` and each requested `--output-fields=` entry) and the UTF-8 validation and escaping helpers (`utf8.c:16,105,129,152`) that govern a non-UTF-8 message payload; sha256 abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f and 7cbebe621330509d7ed4928ea0e8374cf7155e954fee2745ebf08b90cd030d27, opened 2026-10-22); S124 (systemd v262 resource-control and systemd-oomd manual pages — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml and https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml — `ManagedOOMSwap=`/`ManagedOOMMemoryPressure=` auto|kill, the meaning of `auto`, and which cgroups systemd-oomd monitors; sha256 d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8 and 4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d, opened 2026-10-22); S125 (sibling lane tsukuroi, memory-pressure-r25.md at commit 157ee255 — https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md — this host's systemd-oomd `auto` reading and oomd defaults, cited and never absorbed; sha256 ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25, opened 2026-10-22); S126 (Arch Linux packaging of earlyoom 1.9.0-1 — https://gitlab.archlinux.org/archlinux/packaging/packages/earlyoom — the packaged unit and the default arguments file the unit reads; values of that file are not copied; opened 2026-10-22); own-work host capture of 2026-10-22 (`.ufo/waves/round-26/capture/capture.txt` and `.ufo/waves/round-26/capture/capture-boots.txt`, committed; counts, states, thresholds and version strings only — no MESSAGE text, process name, uid, command line or `--avoid`/`--prefer` value was read or copied).
verified-at: 2026-10-22 — upstream sources opened as raw bytes at earlyoom tag v1.9.0 (commit 202d4db0d308ca6478f68de68b46cae34896ddaf) and at systemd tag v262; host observation read-only on 2026-10-22 (committed capture): earlyoom 1.9.0-1 active and enabled, systemd 262-1, systemd-oomd inactive and disabled, kernel 7.2.11-arch1-1; the package was installed on 2026-10-20, and the running earlyoom invocation began 2026-10-22 04:55:44 -03 (ActiveEnterTimestampMonotonic 19964362 µs) — that stamp is the current invocation, not a first activation.
recheck: `systemctl is-active earlyoom.service; systemctl is-enabled earlyoom.service; systemctl is-active systemd-oomd.service; systemctl is-enabled systemd-oomd.service; pacman -Q earlyoom systemd`; `journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE,__MONOTONIC_TIMESTAMP` (classify in memory, keep counts); `journalctl -q -b MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID | wc -l`; on an earlyoom release, re-open the five earlyoom files at the new tag and re-read the eight grammar literals; on a systemd release, re-open the v262 catalog anchor for d989611b…
author: MoriR26 (L1), from the wave-1 scribe draft `.ufo/waves/round-26/w1/DraftEntryR26.md`.

# Userspace OOM killers on this host — earlyoom is running, systemd-oomd is not, and what each one's record can and cannot prove

## Scope

This note records the two userspace OOM-killer services on this host — **earlyoom** and
**systemd-oomd** — as they are on 2026-10-22: which one is running, what each one does when it
acts, how each one's actions appear in the journal, and which of its lines are stable enough to
count. It exists because the previous entry on this ground
(`corpus/knowledge/userspace-oom-killers-r12.md`) said, in the present tense, that both services
are inactive here; that was true on 2026-10-19 and is false now.

It is a **reading** note. It describes service state, thresholds, log grammar and counting rules.
It does not enable, disable, start, stop, restart or tune either service, does not read or copy
`/etc/default/earlyoom` or any `--avoid`/`--prefer` expression, does not echo journal `MESSAGE`
text, and does not count processes killed by anyone.

Every fact below is tagged. **`verified`** — the statement holds on this host on the counted
evidence of 2026-10-22. **`scoped`** — it holds inside a stated limit the evidence does not cross.
**`[INFERENCE]`** — a reading that follows from the evidence but is not itself measured.

## Facts

**F1 — the host state, and the one that changed.** `earlyoom.service` is **active** and
**enabled**; `systemd-oomd.service` is **inactive** and **disabled**. The installed earlyoom is
**1.9.0-1** (Arch) and the installed systemd is **262-1**; the host kernel is `7.2.11-arch1-1`. The
earlyoom **package was installed on 2026-10-20**, and the **running invocation** began
`2026-10-22 04:55:44 -03` — that stamp is the current invocation's start, not a first activation,
and earlyoom is not new to this host.
*Verdict: `verified`* — the committed read-only capture
`.ufo/waves/round-26/capture/capture.txt` (lines with `unit_earlyoom.service_is_active=active`,
`unit_earlyoom.service_is_enabled=enabled`,
`unit_systemd-oomd.service_is_active=inactive`,
`unit_systemd-oomd.service_is_enabled=disabled`,
`unit_show_ActiveEnterTimestampMonotonic=19964362`, `package_earlyoom=1.9.0-1`,
`package_systemd=262-1`, `uname_release=7.2.11-arch1-1`), plus this seat's own read-only
`systemctl` and `pacman -Q` queries (§3.1) and the package install date from `pacman -Qi`
(§3.1).
*Limit:* this is a one-day snapshot of one host, not a fleet fact and not a standing property.

**F2 — the act rule is a conjunction, and the kill is staged.** earlyoom sends `SIGTERM` only when
**both** the available-memory percentage **and** the free-swap percentage are at or below their
SIGTERM limits, and sends `SIGKILL` only when **both** are at or below the lower SIGKILL limits.
The shipped defaults are **10 %** for the SIGTERM limit with the SIGKILL limit at **half** of it
(`PERCENT/2`), for memory and for swap alike.
*Verdict: `verified`* — the decision itself is upstream code (`main.c:500-503`, the `lowmem_sig()`
conjunction), the default pair is upstream code (`main.c:137-140`: 10 / 10 / 5 / 5) and the
half-rule is the upstream option parser (`msg.c:202`), and the prose agrees (`MANPAGE.md:41-45`,
`README.md:239-240`: "both memory and swap must be below minimum for earlyoom to act").
*Limit:* the half-rule applies when only one value is given for an option; an explicit
`PERCENT,KILL_PERCENT` pair overrides it.

**F3 — the percentages are not shares of total RAM.** "mem avail %" is
`MemAvailableKiB * 100 / UserMemTotalKiB`, where *user mem total* is `MemAvailable + AnonPages`;
"swap free %" is `SwapFreeKiB * 100 / SwapTotalKiB` and is forced to `0` when there is no swap at
all.
*Verdict: `verified`* — `meminfo.c:112-119`. The startup line prints both totals so a reader can
see the denominator in use.
*Limit:* because the swap percentage is `0` without swap, the swap half of the conjunction in F2
is then satisfied trivially and the decision rests on memory alone. **`[INFERENCE]`** — that
follows from the two source lines, not from an observation of a swapless host.

**F4 — earlyoom's actions are plain text, not catalog records.** earlyoom writes its warnings to
stderr and its informational lines to stdout; under this unit both land in the journal as records
whose `MESSAGE` is the raw line. Those records carry **no `MESSAGE_ID`** — in the current boot
12 of the 13 earlyoom records have no `MESSAGE_ID` field at all, and the single record that has
one is systemd's own unit-lifecycle line. Every record in the unit's slice carries
`PRIORITY 6`, including earlyoom's own `warn()` output, so **priority does not separate an action
line from a periodic report line**.
*Verdict: `verified`* — `msg.c:99-131` for the write targets, and the journal read in §3.2 for
the fields.
*Limit:* this is one host's systemd configuration; a unit with `StandardError=journal` would
give a different priority. **`[INFERENCE]`** — the priority is the manager's console stream
rather than the writer's own facility, because the unit inherits stderr; the cause was not
isolated.

**F5 — the lines that are stable enough to count, and the ones that are not.** The countable
classes are prefix-anchored literals from the v1.9.0 sources: the version line `earlyoom <version>`;
the two startup threshold lines `sending SIGTERM when mem avail <= <a>% and swap free <= <b>%,`
and `SIGKILL when mem avail <= <c>% and swap free <= <d>%`; the action lines
`sending SIGTERM to process ` and `sending SIGKILL to process `; the escalation line
`escalating to SIGKILL after `; the failure line `kill failed: `; the two low-memory lines
`low memory! at or below SIGTERM limits` and `low memory! at or below SIGKILL limits`; and the
dry-run flag `dryrun mode enabled`. Four constraints make these a counting grammar rather than a
parser:

- The action line's body carries a **uid, a process name and a full command line**. A reader
  counts it and **never copies it**. The same holds for the two startup filter-echo lines, which
  restate the configured prefer/avoid expressions: they are neither countable nor copyable.
- An **escalation prints no action line**: the daemon raises the signal it already decided on,
  so `escalating to SIGKILL after ` is a second signal on the same pid, not a new victim, and it
  is not a `sending SIGKILL to process ` record. The SIGKILL-action count and the escalation
  count are different populations.
- **`kill failed: `** covers two distinct causes — the signal call itself failing, and the
  ten-second wait for the victim to exit timing out. It therefore does **not** prove that no
  signal was delivered.
- The periodic `mem avail:` report and the `mem total:` startup line are **not actions**. Neither
  is `memory situation has recovered while selecting victim`, which is pressure evidence at a
  moment when no kill happened.

*Verdict: `verified`* — each literal and each constraint is upstream source at tag v1.9.0
(`main.c:161,295,414,416,519,523`; `kill.c:318,627,654`; `msg.h:10`), and the class separation was
checked against 273 retained earlyoom records (§3.2).
*Limit:* one percentage format, `"%5.2lf%%"`, right-aligns in five columns, so a one-digit
percent renders with a leading space (`<=  5.00%`). A grammar that expects a single space misses
the SIGKILL threshold line.

**F6 — the scope is the current invocation.** earlyoom's records for one invocation are the lines
whose `__MONOTONIC_TIMESTAMP` is at or above the unit's `ActiveEnterTimestampMonotonic`; the
completeness test is **whether the version line is inside that window**, not whether it is the
first line in it. On this host the unit's own start record lands 8 µs inside the bound and
precedes the version line by about 17 ms, and the two startup threshold lines carry the same
timestamp as each other.
*Verdict: `verified`* — `main.c:161` for the version literal, and the timestamps read in §3.2.
*Limit:* a service restart inside one boot moves the bound forward; the current boot shows one
invocation. **`[INFERENCE]`** — with a `Type=notify` unit the bound would move past the version
print, so the completeness test depends on the unit staying `Type=simple`.

**F7 — earlyoom's kills do not move the kernel's OOM counters, and on this host it could not
delegate to the kernel even if it wanted to.** earlyoom delivers the signal itself — a `kill(2)`
call on the victim pid, followed by a `pidfd` release — and never enters the kernel's OOM-victim
path, which is the only place the kernel increments `count_vm_event(OOM_KILL)` and
`memcg_memory_event_mm(mm, MEMCG_OOM_KILL)`. Therefore `/proc/vmstat`'s `oom_kill` and a cgroup's
`memory.events` `oom_kill` do not count earlyoom's kills. **The delegation exception that the
previous entry named does not exist in earlyoom 1.9.0**: the `-k` / kernel-OOM option was removed
in v1.2 and is ignored for compatibility, the v1.9.0 sources contain no such option, and the
installed binary on this host contains no such string and prints "Option -k is ignored since
earlyoom v1.2".
*Verdict: `verified`* — `kill.c:242` for the signal call and `kill.c:246-262` for the pidfd
release, against the kernel's increment site in `oom-kill-counter-kernel-only-r12.md` (upstream
v7.2 `mm/oom_kill.c:935-936`); the absence of the option is verified on the tag's sources and on
the installed binary's bytes (§3.3).
*Limit:* the kernel-side statement is anchored to the upstream v7.2 implementation the existing
entry opened; the host kernel is `7.2.11-arch1-1` and the distro source identity was not checked.
Upstream master has carried a kernel-OOM trigger option again since 2026-02-02, so that exception
is a statement about a **different, later build** and must not be carried into a note about the
1.9.0 that runs here.

**F8 — the systemd-oomd side.** systemd-oomd is inactive and disabled here, and every unit the
sibling lane captured — `user@1000.service`, `user-1000.slice`, `user.slice` and `-.slice` —
carries `auto` on both `ManagedOOMSwap=` and `ManagedOOMMemoryPressure=`, so nothing in that chain
would be monitored even if the service were started; `auto` is the upstream default and means the
cgroup's data is not actively used for monitoring and detection. systemd-oomd's own kill
accounting is the `user.oomd_ooms` and `user.oomd_kill` cgroup attributes plus a `Killed` D-Bus
signal, and its journal notice is the catalog id `d989611b15e44c9dbf31e3c81256e4ed` ("systemd-oomd
killed one or more processes in unit @UNIT@"). That notice has **0 occurrences in every retained
boot** on this host.
*Verdict: `scoped`* — the `auto` reading and the "systemd-oomd inactive and disabled" reading are
the sibling lane's dated capture, cited here and **not absorbed**: OS and unit diagnosis is
tsukuroi's ground (`PROVINCE.md` adjacency row), and the sibling's own verdict for that row is
`scoped` because it read four units, not the host. This seat's own read of the same four units on
2026-10-22 returned `auto` on both properties for all four, and its own read of the oomd notice
count returned 0 for every retained boot.
*Limit:* one notice means "one or more processes in a unit", never a process count; the notice
count is bounded by journal scope and retention.

**F9 — what the retained journals actually hold.** Counts only, classified in memory; no `MESSAGE`
text was read into any output. The **current boot** holds 13 earlyoom records: 1 version line, 2
threshold lines, 6 periodic reports, 1 memory-totals line, 2 filter echoes and systemd's own
unit-start record — and **0 action lines, 0 escalations, 0 failed kills, 0 low-memory warnings**.
The **previous boot** holds 252 earlyoom records, including **38 `sending SIGTERM to process`
lines and 1 `sending SIGKILL to process` line** (39 actions), 40 low-memory warnings (39 at the
SIGTERM limit, 1 at the SIGKILL limit), 1 "recovered while selecting victim" line, 39 signal
releases and 39 victim-exit lines — and **0 escalations and 0 failed kills**. The retained
journals hold exactly **1** kernel OOM summary and exactly **1** kernel "Killed process" record,
both in that same previous boot, timestamped about 39 minutes **after** earlyoom's last action
there.
*Verdict: `verified`* — the committed per-boot capture
`.ufo/waves/round-26/capture/capture-boots.txt` (`boot_index=0 … lines=13 version=1
term_thresholds=1 kill_thresholds=1 send_sigterm=0 send_sigkill=0 escalating=0 kill_failed=0
low_memory_sigterm=0 low_memory_sigkill=0 mem_avail_report=6`; `boot_index=-1 … lines=252
send_sigterm=38 send_sigkill=1 escalating=0 kill_failed=0 low_memory_sigterm=39
low_memory_sigkill=1 mem_avail_report=83`; `oomd_notices=0` on every boot), the committed
current-boot capture `.ufo/waves/round-26/capture/capture.txt`
(`journal_entries_in_scope=13`, `journal_scope_complete=1`, the per-class counts, the threshold
values 10.00/10.00 and 5.00/5.00, and `oomd_notice_count=0`), and this seat's own counts (§3.2).
*Limit:* the two records are distinct events; nothing here shows that the kernel record was or
was not a consequence of the same pressure episode. **`[INFERENCE]`** — the kernel OOM record is
**not** an earlyoom action: the timestamp ordering and the absence of any kernel-delegation option
in 1.9.0 (F7) both point that way.

## Decision table

Observable → what it means → what it does **not** mean.

| Observable | What acted | What it does NOT prove |
|---|---|---|
| a kernel-journal OOM summary (`oom-kill:constraint=`) or a kernel "Killed process" record, `_TRANSPORT=kernel` | the **kernel** OOM killer acted; the kernel's own OOM counters move at that path | that no userspace killer also acted in the same window — earlyoom's kills are invisible to those counters (F7) |
| a `sending SIGTERM to process ` or `sending SIGKILL to process ` line inside the current invocation's scope (F6), in an invocation that did not log `dryrun mode enabled` | **earlyoom** signalled a victim it selected (under `-g`, a whole process group: one line, many processes) | that the victim died (a `kill failed: ` line says the opposite is possible), that the kernel counters moved (F7), or the victim's identity — the line body carries a uid, a name and a command line and must not be copied; in dry-run mode the same line is printed and no signal is sent (S118 `kill.c:271-273`) |
| an `escalating to SIGKILL after ` line | earlyoom raised the signal on a pid it had already signalled — a **second signal on the same victim**, not a new victim, and **not** an action line | a new victim, or a SIGKILL-action count increase |
| a systemd-oomd notice with `MESSAGE_ID=d989611b…` | **systemd-oomd** killed one or more processes in a unit | a process count (the notice says "one or more"), or that the kernel counters moved |
| a `low memory! at or below SIG… limits` line with no action line after it | earlyoom saw the limits breached and, this time, did not kill | that a kill happened; on this host one such line in the previous boot was followed by "memory situation has recovered while selecting victim" |
| `oom_kill=0` in `/proc/vmstat` or in a cgroup's `memory.events` | **no kernel OOM victim** in that counter's scope and window | that no memory-related kill happened: earlyoom's kills never touch those counters (F7), and systemd-oomd's kills are accounted in its own cgroup attributes (F8) |
| the `user.oomd_ooms` / `user.oomd_kill` cgroup attributes | systemd-oomd's own accounting of its kill attempts and killed pids | a durable event history: the attributes live and die with the cgroup path |
| no record of any kind, with earlyoom **active** | no **positive evidence** of a userspace-killer action in that scope and window | that nothing was killed; the counter surfaces and the journal are different populations, and a kill by any other actor is not visible here |
| earlyoom **inactive** or **absent** | no current invocation: its action counts are `null` (unavailable), never `0`; send lines earlier in the same boot are still positive evidence | that zero kills happened, or that the host is healthy on the memory plane |
| earlyoom's journal **unreadable** | unknown: the counts are `null` and no verdict of quiet is possible | that zero kills happened |
| a plain SIGKILL with none of the records above | an unclassified termination | that a userspace OOM killer acted; it may be a unit manager's action, an external signal, or a policy kill |

## Limits

- **One host, one day.** Every host reading is 2026-10-22 on this machine. The earlyoom
  **package was installed on 2026-10-20** and the first earlyoom record in journal retention is
  from that day, so the `2026-10-22 04:55:44 -03` stamp is the **current invocation's** start, not
  a first activation. This note says "active and enabled", never "active since".
- **One earlyoom version.** Every literal and every constraint is anchored at tag `v1.9.0`
  (commit `202d4db0d308ca6478f68de68b46cae34896ddaf`). Upstream master has moved since — it
  carries a kernel-OOM trigger option again, and its README documents message shapes the tag does
  not have. A different release may move the literals; re-read the sources at the new tag.
- **A counting grammar, not a parser.** The classes in F5 are prefix-anchored (the round-26 tool also
  matches the process-group and journald suppression lines). A line that does not match a class is
  unclassified, and unclassified is not zero.
- **Counts, never text.** The action line carries a uid, a process name and a command line; two
  startup lines carry the configured prefer/avoid expressions. Only counts, states, thresholds and
  version strings leave this note.
- **The journal is the only surface read.** earlyoom exposes its own log, not oomd's cgroup
  attributes, not the D-Bus signal, and not the kernel counters. None of these surfaces sees the
  others.
- **Scope differences are not additive.** The earlyoom action counts are **invocation-horizon**
  numbers; the oomd notice count is a **boot-horizon** number; the kernel counter is a
  **counter-scope** number. They are never summed.
- **Detection and report only.** No service was started, stopped, enabled, disabled or tuned; no
  configuration file was read for its values; no package was installed or removed.
- **The vocabulary of the round-26 tool** (`active` / `inactive` / `absent` / `unavailable`,
  `KILLER_ACTED` / `KILLERS_QUIET` / `KILLERS_UNKNOWN`) is the tool's own contract, not
  earlyoom's or systemd's.

## What it changes for mori

- For the SKILL.md `Did something get killed?` decision row, the userspace-killer arm gains
  **earlyoom** as a class of its own, read from earlyoom's own journal records inside the
  current invocation, with the unavailable-not-zero rule intact: an inactive or unreadable
  earlyoom is `unavailable`, never `0`.
- For the `oom_kill=0` error-pattern row, the label stays **kernel-OOM-only**, and the two
  userspace killers' own counters and records are named beside it.
- The round-26 read tool `tools/mori-oom-killers.py` implements the earlyoom and oomd parts of this
  reading for the **current boot only**: the F5 grammar plus process-group, dry-run and journald
  suppression lines, the current-invocation scope, send lines of earlier invocations this boot, the
  thresholds from earlyoom's own startup lines and the oomd notice count. It does not read previous
  boots, kernel records, kernel counters or oomd's cgroup attributes. Its live run on 2026-10-22
  returned `KILLERS_QUIET` with earlyoom `active`, `grammar: verified-1.9.0`, thresholds 10.00/10.00 and
  5.00/5.00, zero action lines in the current invocation, and oomd `inactive` with 0 notices; the
  previous boot, which the tool does not read, held 38 SIGTERM and 1 SIGKILL send lines
  (`capture-boots.txt`). A quiet verdict means "no positive evidence from the killers that are
  readable in this boot", not "zero kills".
- For `corpus/README.md` and the FR10 row in `PROVINCE.md`, the "inactive on this host" summary
  is replaced by "earlyoom active and enabled, systemd-oomd inactive and disabled" with a date.
- The r12 entry's kernel-delegation sentence is corrected rather than carried: see F7 and §4.2.

## Adjacency

- `tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md` at commit `157ee255` — this host's
  systemd-oomd reading, the `auto` semantics and the oomd defaults are **tsukuroi's** ground and
  are cited here, not absorbed (F8). Its MP4 row is the source of the "every captured unit is
  `auto`" statement and of the oomd-side limit; its verdict for that row is `scoped`.
- `corpus/knowledge/oom-kill-counter-kernel-only-r12.md` — owns the kernel-counter semantics this
  note cites in F7. This note does not restate the increment sites; it says which killer's
  actions do and do not reach them.
- `corpus/knowledge/kill-classes-by-message-id-r12.md` and
  `corpus/knowledge/kernel-oom-line-attribution-r12.md` — own the journal **catalog** classes
  (`fe6faa94…`, `d989611b…`, `98e32220…`) and the kernel-record attribution. earlyoom's own
  records carry no `MESSAGE_ID` (F4), so earlyoom's actions are counted by prefix and never enter
  a catalog class.

## Not claimed

- No claim that the stale 2026-10-19 statement was wrong about that date, only about the present.
- No claim about any earlyoom build other than 1.9.0, and no claim about upstream master.
- No claim that earlyoom prevented, caused or mitigated any kernel OOM event; the retained
  journals hold one of each and they are separate records (F9).
- No claim about a fleet, another host, or any other lane's service state.
- No claim that a cgroup's `oom_kill` is zero because nothing was killed (F7).
- No process count, victim identity, uid, command line, prefer/avoid expression or `MESSAGE` text.
