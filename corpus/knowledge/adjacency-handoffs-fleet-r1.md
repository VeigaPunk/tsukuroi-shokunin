source: sibling province declarations pinned below; new read-only OS captures by R1MemoryPacket, R1DriverPacket and R1HelperPacket; inherited working-tree ADJ-01..07 vocabulary in PROVINCE.md:35-43.
verified-at: 2026-10-15, fleet round-1; packet capture windows are given separately below. Baseline lane commit: 0ecf3ff1b0aa312d71899581badc5a9798430369.
recheck: §4 for the counting command; §5 for read-only replay. The JSON ledger supplies persisted source digests and line-range anchors, not a new runtime router.

# Fleet round-1 — source-backed handoff contract

## 1. Scope, provenance and scoring claim

One adjacency move. The stored scores at the baseline are depth 8, coverage 8,
operability 9, freshness 8, calibration 9, adjacency 7 (`SCORECARD.md:45-52`).
The initial lane assignment is operability/freshness, but `../MISSION.md:40-46`
and `../AXES.md:25-39` require the lowest stored axis. Adjacency is not retired.
This fleet round-1 does not renumber or rewrite the historical training rounds.

At session entry, `PROVINCE.md` and `SKILL.md` already had uncommitted edits.
Their working-tree SHA-256 values were, respectively,
`e740605dd8caf02c618523dc0139ddd96487c92477b23e21df5a54485436416c` and
`e6057893cbc8e5b05679df3e3a9bd3f43ea394bb562744c7c9c5e7e52e7a0dbd`
(`sha256sum PROVINCE.md SKILL.md`, capture 2026-10-15T04:54:05Z).
Those edits are preserved, not authored or committed by this round. The table
was already present in that inherited tree. It was absent from committed
baseline PROVINCE.md. **No credit is claimed for adding that inherited table.**

This round adds a standalone, source-backed evidence contract in
`adjacency-handoffs-fleet-r1.json`, this executed packet, and an index/lesson.
The measurable artifact delta is complete source-cited contract records
**0 → 7**, not seven completed handoffs. Seven is a structural count, not a
proof of semantic correctness; source reads, counterexamples and packet replay
supply separate evidence. Only ADJ-04 has an exercised observation/request
packet. GPU/helper boundary controls are not endpoint/auth incidents.

Limited score rubric: retain the historical ordinal 7 for narrative handoffs;
8 means a persisted source-backed contract plus one verified, sanitized packet
reported through the fleet report. It does **not** mean 8/10 cases, seven
accepted routes, recipient replay, arbitration or promotion. No score above 8
is supported by this sample. Recipient-side replay/acceptance and the contested
RE owner remain ceilings. Delivery is evidenced only by the later committed
fleet report, not by this earlier note's existence.

## 2. Seven decisions and their limits

The JSON contract is the machine-countable record of the following decisions.
It names each trigger, retained OS scope, recipient, source range/anchor,
minimum packet, counterexample and forbidden inference. It is evidence data,
not a dispatcher or authorization layer. Re-read sources before future use.

| ID | Analysis recipient | Source | Counterexample / retained boundary |
|---|---|---|---|
| ADJ-01 | kama | `../kama-shokunin/PROVINCE.md:3-24` | Stale DKMS alone stays OS diagnosis. GPU readiness does not prove an endpoint. |
| ADJ-02 | kagi | `../kagi-shokunin/PROVINCE.md:3-17,32-54` | Ordinary package drift stays here. Metadata cannot prove credential exposure or safety; the declared janitor substrate is historical/absent. |
| ADJ-03 | mado | `../mado-shokunin/PROVINCE.md:3-16` | Failed user unit alone stays here. Active unit is not visual proof. |
| ADJ-04 | mori | `../mori-shokunin/PROVINCE.md:3-16` | OS repair stays here. Fleet correlation is not wave causation; cumulative counts cannot date an incident. |
| ADJ-05 | kumitate | `../kumitate-shokunin/PROVINCE.md:3-6`; `../mori-shokunin/PROVINCE.md:12-16` | Silence/settlement without a dispatch-mechanism defect goes to mori. |
| ADJ-06 | protocol integrator for ownership ruling | `../kaidoku-shokunin/PROVINCE.md:3-6`; `../revenger-shokunin/PROVINCE.md:3-7` | Both declare shipped-artifact RE. No owner selected, no target run, no raw core forwarded. A version mismatch alone stays here. |
| ADJ-07 | tameshi for method advice | `../tameshi-shokunin/PROVINCE.md:3-18` | Census code/contract/repair remain here. One lane's case cannot establish a general method. |

Source digests were captured with:

```sh
sha256sum ../{kama,kagi,mado,mori,kumitate,kaidoku,revenger,tameshi}-shokunin/PROVINCE.md
```

The eight exact SHA-256 values are persisted in the JSON `source_pins` object.
They pin observed working-tree bytes, not a claim that every sibling has
committed those bytes. A digest match is drift evidence, not ownership proof;
the cited text supplies ownership. Sources are outside this lane's control.

For a mixed question, split the OS diagnosis from the requested sibling
analysis. Unknown/disputed ownership goes to the integrator. Never transfer
ownership because another lane answered first. A recipient is not permission
to write configs, restart services, install packages, read secrets or execute
a target.

## 3. Executed observation packet — TSUKUROI-F1-MEM-01

- Route: ADJ-04; recipient **mori** for fleet-timeline correlation.
- Trigger: a timestamped live resource observation to place on the fleet
  timeline, not a reported OOM or pressure incident.
- Capture: **2026-10-15T04:53:46Z → 2026-10-15T04:53:46Z**. Kernel
  `7.2.3-arch1-3`. Boot identity/time and event window were not captured by
  this seat; no dated historical event is claimed.
- Scope retained: OS memory/journal/boot diagnosis and any repair recommendation.
- State in this child artifact: **prepared**. Report receipt is the later
  `.ufo/reports/round-1/tsukuroi.md` on the fleet repo, after the child commit.
  Acknowledgement, acceptance and resolution are **unobserved**.

R1MemoryPacket executed the following non-mutating commands; outputs are
transcribed without the seat's unsupported "background-noise" assessment.

| Command | Observed output | Exit |
|---|---|---|
| `date -u +%FT%TZ` (open/close) | `2026-10-15T04:53:46Z` at both ends | 0 / 0 |
| `uname -r` | `7.2.3-arch1-3` | 0 |
| `grep -E '^(MemTotal\|MemAvailable\|SwapTotal\|SwapFree):' /proc/meminfo` | `MemTotal: 31721780 kB`; `MemAvailable: 12937876 kB`; `SwapTotal: 35917176 kB`; `SwapFree: 22510168 kB` | 0 |
| `cat /proc/pressure/memory` | `some avg10=0.08 avg60=0.06 avg300=0.23 total=83641285`; `full avg10=0.08 avg60=0.06 avg300=0.22 total=81449469` | 0 |
| `test -e /sys/fs/cgroup/memory.events` | no output; absent at this fixed root path | 1 |
| `cat /sys/fs/cgroup/memory.events` | `cat: /sys/fs/cgroup/memory.events: No such file or directory` | 1 |

Interpretation: meminfo fields are instantaneous gauges. PSI totals are
cumulative stalled time, not an event timestamp. Root `memory.events` was
absent, not zero; no cgroup subtree was enumerated. The packet demonstrates
neither a fresh OOM, nor a harmful-pressure threshold crossing, nor a fleet
cause. Existing warning source: `kill-event-deep-r8.md:172-193` and
`oom-event-plane.md:247-257,365-367`. Their old numeric captures are not
reused as live facts.

Request to mori: place this exact capture window against watchdog/wave
liveness and settlement observations **if retained**. Say whether independent,
dated kill/pressure evidence overlaps that window, or state no retained
comparison is available. Keep correlation separate from causation; do not
reconstruct an event from cumulative PSI or the absent root counter. This
round does not request OS remediation, additional identity-bearing process
captures, or a new observability mechanism.

### Boundary control — ADJ-01, not a delivered incident

R1DriverPacket at **2026-10-15T04:53:18Z** ran `date -u` (exit 0), `uname -r`
(`7.2.3-arch1-3`, exit 0) and
`nvidia-smi --query-gpu=name,driver_version --format=csv,noheader`
(`NVIDIA GeForce RTX 5070, 610.57.04`, exit 0).
No endpoint symptom was reported and no endpoint or serving unit was probed.
The ADJ-01 trigger is absent. This is a negative routing control, **not** an
endpoint health proof or a second completed handoff.

### Boundary control — ADJ-02, metadata is not credential evidence

R1HelperPacket at **2026-10-15T04:54:00Z** ran `stat -c '%a %u %g %n'
/usr/bin/op` → `2755 0 1002 /usr/bin/op` (exit 0) and
`pacman -Qo /usr/bin/op` →
`/usr/bin/op is owned by 1password-cli 2.40.0-2` (exit 0).
The helper was not invoked and its contents, credentials and environment were
not read. No auth incident or credential-safety conclusion is established;
there is no delivered ADJ-02 incident. Kagi's janitor-substrate absence in its
province is an explicit limitation, not a surface this lane may restore.

## 4. Counting contract records

Run from the lane repo. Replace the revision with the actual recorded
implementation commit; the baseline is the literal hash below. Missing-file
handling means exactly zero records for this new ledger, not zero historical
cross-domain work.

```sh
ref=0ecf3ff1b0aa312d71899581badc5a9798430369
file=corpus/knowledge/adjacency-handoffs-fleet-r1.json
if git cat-file -e "$ref:$file" 2>/dev/null; then
  git show "$ref:$file" | jq '[.routes[] | select([.trigger, .retains, .recipient, .counterexample] | all(type == "string" and length > 0)) | select((.sources | length) > 0 and (.minimum_evidence | length) > 0)] | length'
else
  printf '0\n'
fi
```

Baseline execution returned **0**, exit 0. This is a completeness predicate
on structured records, not semantic validation. It excludes no old narrative
mentions and does not count probes or lifecycle milestones as packets.
Counted packet identity set in this note: `{TSUKUROI-F1-MEM-01}` — one
prepared observation. Its later reported receipt must name that same identity,
recipient, request and child commit. Copies into LOG/report are not new
packets. No accepted or resolved packet is claimed.

## 5. Read-only replay and stop line

1. Re-read the seven source ranges in §2. Compare SHA-256 to JSON `source_pins`;
   on mismatch inspect current declarations before using the old mapping.
2. Read each JSON trigger and counterexample. Route the requested question,
   not the binary name. ADJ-06 must remain an arbitration request.
3. Re-run only the explicitly named public OS probes in §3 when current host
   context is needed. Preserve nonzero/absent results; do not silently choose a
   different counter or equate missing evidence with zero. New values are a
   new capture, not a failed replay of old values.
4. Prepare the sanitized packet: capture window, exact command/exit/output,
   OS scope retained, sibling-side question, source citation and explicit
   unknowns. Do not infer an event from cumulative state or endpoint/auth
   safety from metadata.
5. Report it with the child evidence revision. Track `prepared`, `reported`,
   `acknowledged`, `accepted`, `resolved` separately using JSON definitions.
   Only recipient-side durable evidence can advance the last three states.
6. Stop. No installation, service action, config write, endpoint invocation,
   helper execution, core forwarding, credential/environment/argv read or
   claimed recipient outcome is part of this contract.

The integration smoke and committed after measurement are recorded in the
round's LOG/SCORECARD and fleet report. Advisory seats are author-side evidence;
none supplies the non-author promotion/learning spot-check required by the
protocol. No independent replay or accepted handoff is claimed.

## 6. Parent replay receipt

The parent exercised a live, read-only OS availability observation before
delivery. Command:

```sh
date -u '+%Y-%m-%dT%H:%M:%SZ'
free --bytes
rc=$?; printf 'free_exit=%s\n' "$rc"
systemctl --user is-system-running
rc=$?; printf 'user_manager_exit=%s\n' "$rc"
date -u '+%Y-%m-%dT%H:%M:%SZ'
```

Observed open/close **2026-10-15T05:00:03Z**:

```text
               total        used        free      shared  buff/cache   available
Mem:     32483102720 16159678464  3003924480    10633216 13825777664 16323424256
Swap:    36779188224 19483697152 17295491072
free_exit=0
running
user_manager_exit=0
```

This is supplemental current-state context, not a second packet or a historic
OOM reconstruction. A running user manager establishes neither fleet progress
nor dispatch correctness. Changed gauge values are expected between captures;
no unchanged-host or pressure-threshold claim follows.


## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — sibling `PROVINCE.md` source-pin hashes, sanitized handoff packets, and read-only replay probes on host `plazir27`, 2026-10-15.
verified-at: 2026-10-15 (source-pin and packet measurements recorded in this note).
recheck: 180d; procedure: §4 counting command and §5 read-only replay; re-read sibling declarations before a later handoff.
supersedes the pointer-only recheck: line above.
