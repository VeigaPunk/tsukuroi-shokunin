# mori-shokunin — Province

**Domain:** fleet & host observability (森) — whether the fleet, its waves and
its host are alive and progressing.

**Owns (read-only probes):** shokunin watchdog liveness (pid, start time, log
freshness, lane counters); `.ufo/waves/*` settlement state (registry + results
pair); kill/OOM-related catalog-ID records and signal-11 coredump records from
independently labeled user/system journals, plus cgroup `memory.events` and the explicit same-boot journal window after a retained anchor;
resource runway (disk on the fleet root and `/tmp`, memory pressure); lane silence grading (silent / progressing / progressing-weak).

**Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package,
systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal
and cgroup events as fleet evidence and reports them, never owning OS state;
endpoint and model-serving health (→ kama); credential material (→ kagi).
**Detection and report only — never remediation.**

**Out of province → report, never absorb.**

## Core

- **Watchdog liveness** — census `SURFACE watchdog`: watchdog pid/start and log freshness, plus `.ufo/state/*.round` values against each lane's latest launch-ledger entry.
- **Wave settlement** — `SURFACE waves`: registry/dispatch/results presence and per-wave age; report settled, unsettled, or empty without calling an aged wave failed.
- **Kill/OOM classes** — structured, MESSAGE-free journal records carrying catalog IDs for kernel-OOM unit notices, oomd notices, coredumps, unit-process SIGKILL results and unit failures, plus a distinct numeric signal-11 coredump count; independently labeled user/system scopes, never summed. Positive OOM notices and observed `UNIT_RESULT=oom-kill` retain critical `OOM_KILL_JOURNAL`/DRIFT alarms. Failed-unit subject metadata preserves fleet-only `UNIT_FAILURE_JOURNAL` versus non-fleet `UNIT_FAILURE_OUT_OF_SCOPE` with tsukuroi triage routing; absent or unsafe subject metadata remains unknown. `SURFACE cgroup` retains selected-scope kernel memory-event counters, not a replacement for all journal alarms. Journal labels are client-set, not authenticated producer identity; records are not unique victims or fleet-cause attribution. Other structured signals are unimplemented; arbitrary signals without retained records remain unmeasured. See `corpus/knowledge/journal-alarm-routing-r14.md`.
- **Same-boot journal window since anchor** — explicit read-only probe `tools/mori-journal-window.py --anchor PATH --scope user|system` (round-16 build; admitted round 16 — `corpus/lessons/round-16-verifier-spotcheck.md:11`). Reads one journal scope from an operator-retained `mori-journal-anchor-v1` cursor using MESSAGE-free output fields. The first record must match the anchor cursor and boot exactly and is dropped; every later record must be a scalar-cursor object in that same boot. Reports `records_after_anchor` and four separate `positive_*` subset counts (kernel OOM, unit OOM, unit signal, process SIGKILL) using the r15 predicates; no total, victim, emitter or completeness claim. Missing or vacuumed anchor, boot mismatch, malformed, duplicate or truncated capture, nonzero rc, stderr, timeout and overflow return `MORI_JOURNAL_WINDOW_UNAVAILABLE` with no positive totals. Byte equality is conservative: libsystemd documents that one entry may carry several cursor strings, so a mismatch refuses without proving deletion and no dedup is claimed. The anchor is never advanced, stored or written by the probe.
- **Resource runway** — `SURFACE disk` and `SURFACE cgroup`: default `df -P` targets `$ROOT` and `/tmp`, since-boot device-write average, memory PSI/fill/avail, and scope high-watermark.
- **tmux relevance** — `SURFACE tmux`: classify sessions by pane path; bound the freshness probe for each relevant session.
- **Lane silence** — `SURFACE lane.<id>` rows: launch-anchored authorship grading as silent, progressing, progressing-weak, young, not-open, or unavailable.

Round-15 C1 addresses the FR1 **mixed-class alarm suppression** boundary:
individually validated current-boot OOM or user-signal positive evidence may
raise the existing global critical/user warning alarm while an invalidated
class total and subject partition stay unavailable. The additional
`positive_*` fields describe evidence subsets, never a complete count or a
unique victim. Syntactically malformed JSON, unsuccessful or stderr-bearing
capture, missing parser and timeout still produce unavailable, not inferred
positive evidence. Kernel event-time attribution, exhaustive fleet membership
and authenticated client labels remain frontier; no remediation is added.

Round-16 C1 advances FR11 only for the same-boot explicit window above, and only when exact retained-anchor continuity holds. The probe mutates no cursor state, makes no completeness, unique-victim or authenticated-emitter claim, and performs no census cutover. Cursor rotation/vacuum beyond exact-match refusal, cross-boot ordering and cursor-string aliasing stay Frontier (FR11).

## Frontier

- **FR1 — Kernel OOM event-time attribution and fleet correlation** (state F1/F8 + art F2). First evidence: `corpus/knowledge/kernel-oom-line-attribution-r12.md:10-16`; `corpus/knowledge/audit-r11.md:203-204`. Round 13 advances structured system-journal notice records to Core; event-time kernel summary/victim token validation and fleet correlation remain frontier. No raw `MESSAGE` is emitted, and a host record alone does not prove a fleet-caused kill.
- **FR2 — Quota/EDQUOT observability** (state F2). First evidence: `corpus/knowledge/audit-r11.md:218-222`. Boundary: `df` capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state.
- **FR3 — Authoritative wave settlement and emptied-by-hygiene versus never-written** (state F3). First evidence: `corpus/knowledge/audit-r11.md:202`; `../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:28-34,91-120`. Boundary: mori reports filesystem shape; kumitate owns orchestration/result semantics; `empty` alone does not prove never-written, and receipt review stays offline.
- **FR4 — Driver-state versus MANIFEST versus lane-LOG round reconciliation** (state F4). First evidence: `../.ufo/waves/kaika-w1/mori-state.md:31,190`; `corpus/knowledge/observability-surfaces-r2.md:118-125`. Boundary: the census compares driver state with watchdog launch lines only; it does not establish MANIFEST admission or lane-LOG agreement.
- **FR5 — Watchdog daemon identity and degraded-pgrep visibility** (state F5). First evidence: `corpus/knowledge/audit-r11.md:200-201`. Boundary: an unavailable pid probe is not absence, and argv-substring matches do not establish daemon identity.
- **FR6 — Instantaneous disk write-rate** (state F6). First evidence: `corpus/knowledge/surfaces-r8.md:75-89`. Boundary: retain the since-boot average as a different measure; a two-sample rate stays deferred until its added latency meets the stated budget.
- **FR7 — Live tmux relevance/freshness arm** (state F7). First evidence: `corpus/knowledge/surfaces-r8.md:120-124`. Boundary: the host arm is fixture-proved only; do not create or steer sessions, and unavailable is not unhealthy.
- **FR8 — Alert-threshold calibration** (state F9). First evidence: `corpus/knowledge/audit-r11.md:205`. Boundary: thresholds remain labeled local; a quiet window is not a workload distribution or an alert-cost rule.
- **FR9 — Durable fixture evidence** (state F10). First evidence: `corpus/knowledge/audit-r11.md:41-46`. Boundary: scratch paths and unreconstructable fingerprints are not durable evidence; retain a reproducible fixture generator and digest before making replay claims.
- **FR10 — Userspace OOM killers (systemd-oomd and earlyoom)** (art F1). First evidence: `corpus/knowledge/userspace-oom-killers-r12.md:10-15`. Boundary: inactive killers are unavailable, not zero; `memory.events oom_kill` does not cover every userspace kill; never enable or tune a killer.
- **FR11 — Remaining new-since-anchor journal semantics** (art F3). First evidence: `corpus/SOURCES.md:20-21`; `corpus/knowledge/structured-journal-scopes-r13.md:21,81`. Round 16 advances only the explicit same-boot exact-anchor window in Core. Remainder: cursor rotation/vacuum and retention behavior beyond the exact-match refusal, cross-boot ordering, completeness of records after an anchor, persisted or automatically advanced cursor state, and cursor-string aliasing (no byte-level dedup guarantee). Boundary: cursor queries stay read-only and explicit; a byte mismatch is refusal evidence only, not proof of vacuum or deletion.
- **FR12 — Event-driven pressure and CPU/IRQ PSI** (art F4). First evidence: `corpus/SOURCES.md:7-8,16`; `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md:57-73`. Boundary: a PSI trigger watcher is resident, not a one-shot census probe; system CPU `full=0` is not evidence of no stall.
- **FR13 — eBPF kill/OOM tracing** (art F5). First evidence: `corpus/SOURCES.md:11-12,23-26`. Boundary: privilege and version matter; a resident tracer is outside the census, so retain this as knowledge/frontier only.
- **FR14 — Agent-workload telemetry** (art F6). First evidence: `corpus/SOURCES.md:28-32`. Boundary: mori is consume-only; telemetry emission belongs to the emitting lanes and orchestration.

## Adjacent

Report shared evidence to its owner; do not absorb another lane's domain.

| Sibling | Boundary | Evidence |
|---|---|---|
| kumitate | Owns OMP task/hub orchestration and wave plan/run/record/collect semantics; mori passively grades `.ufo/waves/*` filesystem settlement state. No conflicting settlement contract was found. | `../kumitate-shokunin/PROVINCE.md:3-6`; `../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:28-34,91-120`; `PROVINCE.md:6-10` |
| tsukuroi | Owns host OS, package, systemd-unit, driver, firmware, and boot diagnosis. It was the only sibling hit in R12Connector's corpus search for `systemd-oomd`, `earlyoom`, `memory.events`, and `MESSAGE_ID`; this is adjacent host diagnosis, not contested fleet ownership. | `../tsukuroi-shokunin/PROVINCE.md:8-14`; `../tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:231-257,279-281,301,344-367`; `../tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md:30-37,97,120-135`; `PROVINCE.md:12-16` |
| kama | Owns local model-serving and endpoint health; mori does not infer serving health from host/resource signals. | `../kama-shokunin/PROVINCE.md:3-15,40-53` |
| kagi | Owns secrets, vault operations, and credential-hygiene evidence; mori never reads or reports credential material. | `../kagi-shokunin/PROVINCE.md:3-6`; `SKILL.md:374-393` |
| souji | Lists own-uid scratch residue and proposes removal for operator approval; routes liveness/resource findings to mori. Mori reports, never performs reclamation. | `souji-shokunin@fe7590b3010bed9b9b808b79c2bf2be1a18bce2a:PROVINCE.md:8-17,50-52`; the round21 citation erratum below retains the historical context. |

- **Received packet TSUKUROI-F1-MEM-01 (ADJ-04):** `../tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:74-112` records the 2026-10-15T04:53:46Z capture as `prepared`; boot identity/event window were not captured, and acknowledgement/acceptance/resolution are unobserved. Its request is to compare the timestamp with watchdog/wave evidence if retained, not to infer an OOM or cause.
- **What mori can place:** 04:53:46Z is 01:53:46-03:00, between watchdog ticks at 01:50:57 and 01:58:27; `mori round=2` and `tsukuroi round=1` launched at 01:50:57 (`.ufo/watchdog.log:395-402`). Fleet commits bookend that point: `git -C /home/vgpnk/Projects/shokunin show -s --format='%h %ci %s' 99efc52 f2df270` → `99efc52 2026-10-15 01:52:09 -0300`; `f2df270 2026-10-15 01:55:17 -0300`. [INFERENCE] This locates active fleet work, not a settled-wave state at the packet's exact second.
- **Count-only kill sweep for the packet second:** the packet's single PSI snapshot is not a retained pressure series; its PSI `total` fields are cumulative stall time and the fixed root `memory.events` path was absent, not zero (`../tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:94-104`). These time-bounded, MESSAGE-free queries returned 0:

  ```sh
  journalctl -k -b all -q --since='2026-10-15 04:53:46 UTC' --until='2026-10-15 04:53:47 UTC' --grep='^oom-kill:constraint=' -o json --output-fields=_BOOT_ID | wc -l
  # 0
  journalctl --system -b all -q --since='2026-10-15 04:53:46 UTC' --until='2026-10-15 04:53:47 UTC' MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=MESSAGE_ID,_BOOT_ID | wc -l
  # 0
  journalctl --system -b all -q --since='2026-10-15 04:53:46 UTC' --until='2026-10-15 04:53:47 UTC' MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID,_BOOT_ID | wc -l
  # 0
  journalctl --user -b all -q --since='2026-10-15 04:53:46 UTC' --until='2026-10-15 04:53:47 UTC' MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=MESSAGE_ID,_BOOT_ID | wc -l
  # 0
  journalctl --user -b all -q --since='2026-10-15 04:53:46 UTC' --until='2026-10-15 04:53:47 UTC' MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID,_BOOT_ID | wc -l
  # 0
  ```

  No retained kernel OOM, `fe6faa94…` unit-kill notice, or `d989611b…` oomd notice overlaps this bounded query; [UNKNOWN] no independent pressure-series comparison is available for this packet. The single snapshot cannot establish fleet cause or wave settlement. Correlation is not causation.
- **Souji's receipts distinguish only listed removals:** the approval list records hashed `aggregator-r10*` artifacts and the later sweep marks those exact paths `pushed`. For precisely those named paths, receipts support a `swept (pushed-receipt)` classification; for an empty path without a matching receipt, [UNKNOWN] history, so it is not evidence of “never written.” This is offline evidence reading, not a live census dependency.
- **Source overlap:** R12Connector compared the S001–S030 URL set in `../.ufo/waves/kaika-w1/mori-art.md:91-124` with sibling `corpus/SOURCES.md` registries; its exact-URL sweep found no shared URL, so no source rows are merged here.

## Corrections (round 12)

- The existing phrase “scratch roots” does not resolve to a measured target: `/scratch` is absent (the path inspection returned `Path '/scratch' not found`; `../.ufo/waves/kaika-w1/mori-state.md:180` records `ls /scratch` → absent). The census documents `MORI_DISK_TARGETS` as defaulting to `$ROOT /tmp` (`tools/mori-census.sh:211-212,282`); `/scratch` is not a default disk target.

## Round-17 appended scope and closure notes (2026-10-20)

- **Supersedes “verification pending” in the same-boot window Core row:** the
  non-author `corpus/lessons/round-16-verifier-spotcheck.md:9–17` admitted the
  exact-retained-anchor, explicit-scope, anchor-boot capability. It waived no
  procedural breaches. No census cutover, cross-boot continuity, cursor alias
  identity or journal completeness is added.
- **Core, bounded FR14 advance:** passive terminal-at-scan transcript observation
  (`tools/mori-seat-terminal.py`, `corpus/knowledge/seat-terminal-status-r17.md`).
  Version-3 regular transcript files only; field-limited status tallies by naming
  prefix/provider/model. An aged error may later resume: no permanent death,
  authenticated lane membership, incident count or routing decision is claimed.
- **Core, lane-silence provenance:** jj-colocated history reads use the resolved
  local branch, with explicit off-branch HEAD and ambient-author diagnostics
  (`corpus/knowledge/jj-branch-anchor-r17.md`). No bookmark or identity repair.
- **Adjacent tsukuroi handoff, detection only:** today's `/var/log/pacman.log`
  records a 09:15:30 `pacman -Syu` and a 13:23:08 `pacman -U …zcode…`.
  `.ufo/waves/round-17/build/PacmanTxnToday.md` records their transaction evidence;
  `PacmanActorTrace.md` correlates the former to a separate OMP session and leaves
  the latter's human/interactive actor inferred, not authenticated. Package and
  boot-chain interpretation/recovery remain tsukuroi/operator-owned. MorI ran no
  package transaction or service change.
- **FR14 remainder:** telemetry schema changes, concurrent snapshots, permanent
  termination, authoritative wave-result semantics and emission stay frontier or
  kumitate-owned. No scan is an orchestration verdict.


## Round-18 appended scope notes (2026-10-21)

- **Core, own-evidence retention:** mori owns the retention gate over its *own* committed
  evidence (`tools/mori-retention-gate.py`, classes in
  `.ufo/waves/round-18/frozen/c1-policy.json`) and the minimization rule in
  `corpus/knowledge/evidence-minimization-r18.md`. It redacts lane-authored copies at the tip
  only; pushed history, exposure assessment, credential rotation and any history rewrite are
  **kagi/operator**-owned (`.ufo/waves/round-18/build/ConnectKagiExposure.md`). Line digests
  are provenance, not a secrecy claim.
- **Core, freeze-order verdicts:** judging the lane's own claim labels against commit order
  (`tools/mori-freeze-order.py`) is calibration of mori's own record, not a fleet ruling.
- **Core, dispatch-attempt binding (observation only):** one ledger row per whole-wave task
  call binds the committed payload digest to the observed result
  (`tools/mori-dispatch-ledger.py`). Planning, slot acquisition, retrying and adjudicating
  dispatch remain **kumitate/operator**-owned; `wave-slot.sh` grant lines are recorded as
  evidence only (`.ufo/waves/round-18/build/ConnectKumitateDispatch.md`).
- **Correction to the round-17 note above:** the session attribution of the 09:15 package
  transaction is retained only in minimized form; its session identity and private context
  were withheld at the tip in round 18. Package/boot-chain interpretation stays tsukuroi's.

## Round-20 appended scope notes (2026-10-21)

- **Core, per-seat wave settlement (FR3 advance, filesystem shape only):**
  `tools/mori-wave-settlement.py scan` counts, for every `ufo-swarm-wave-dispatch-v1` file
  under a lane's `.ufo/waves/`, which declared members have a non-empty report at their
  `Report:` trailer path (`present`/`empty`/`stub`/`missing`/`misrooted`/`unsafe`/`unparsed`;
  waves `settled`/`partial`/`unsettled`/`no-spawn`/`unavailable`). A missing report is not a
  dead seat; result acceptance and re-dispatch stay **kumitate**'s; a misrooted file is routed
  to its lane L1 (souji's refusal fence covers live round outputs), never moved by mori.
  Knowledge: `corpus/knowledge/wave-settlement-r20.md`. Its `settled` means report-file
  settlement only, not kumitate's lifecycle settlement or result acceptance (wave-2
  `ConnKumitateRoute`); a dispatch file that was never spawned also reads `unsettled`.
- **Still FR3 frontier:** emptied-by-hygiene versus never-written; whether a dispatch file was
  ever dispatched (spawn records are lane-specific ledgers); successor reports for re-run seats.
- **Freshness:** the census behavioral baseline is re-pinned after a complete closed-class
  classification (`corpus/evidence/drift-classification-r20.json`); two disappearance tokens
  (`WATCHDOG_STALE` log-mtime proxy, `WAVE_UNSETTLED_AGE` emptied-wave memory) are recorded
  census design residuals, not fixed here (`corpus/knowledge/drift-repin-r20.md`).

## Round21 correction — retained loss is not lifecycle settlement

Supersedes the round20 freshness note's implication that the closed-class
register licensed the re-pin. CloseMori20 rejected it: removed aggregator-r10
and aggregator-r10-resume markers remain unresolved evidence-loss regression,
not nonblocking live-state. QUALITY69 supersedes67. The historical r20
baseline stays byte-unchanged but invalid for acceptance. FR3 authoritative
settlement and independently evidenced cleanup disposition remain frontier;
mori retains the unknown identities and provenance and blocks acceptance,
never manufactures independent disposition or acts on old wave directories.
The existing bounded report-presence capability remains distinct.
Evidence: `corpus/lessons/round-21.md`; round21 retained loss evidence.

Round21 connector clarification (`.ufo/waves/round-21/build/ConnectKumitate.md`): “blocks
acceptance” above means **mori's own census baseline acceptance only**.
An audit `disposed` row merely cites a structurally validated, hash-bound
independent record; it is not mori's lifecycle settlement, result acceptance,
or a reap/re-dispatch licence. Those remain kumitate-owned. Actor identity
fields are declared evidence requiring outside adjudication, not authenticated
by mori's hash checker.

Round21 souji-citation erratum (`.ufo/waves/round-21/build/ConnectSouji.md`):
the adjacency table's old quotation is historical; current souji scope is
`../souji-shokunin/PROVINCE.md:8-17,50-52`. Its pushed receipt establishes
removal-safety/recoverability only. The pre-removal aggregator artifacts do
not supply independent lifecycle closure; the aggregator's round12 empty-at-
inspection report corroborates loss, not disposition. A future independent
per-wave disposition must come from the operator or an appropriate non-author
wave/lifecycle owner; mori cannot author itself out of this blocker.

Round21 residual-review wording correction: “independent record” in the
connector clarification means **declared-independent record**, pending
outside adjudication. Structural validation and hashes do not establish
authorship or acceptance; every such declaration remains pin-blocked here.

## Round22 own-evidence accounting boundary

The retention reconciler independently recounts the lane's committed evidence
and compares a retained receipt; it does not rewrite the gate, policy, allowlist
or history. Its match is accounting agreement only, not authentication, privacy
clearance, exposure assessment or a kumitate lifecycle/receipt decision. It
cannot authorize baseline acceptance, cleanup, reap, continuation or dispatch.
Non-author hits remain explicitly present in the raw population; their authors
or the operator, not mori, own any change. Pushed-history action remains
operator-owned, with kagi advising only on actual credential/vault concerns.
No frontier row is closed. Ground: round22 lesson and
`corpus/knowledge/retention-reconciliation-r22.md`; connector reports
ConnectKagi/ConnectKumitate/ConnectSouji under round22 build evidence.

## Round23 disposition — no quota Core advance

The declared FR2 capability did not meet its frozen target and was withdrawn from
production and the admitted knowledge/capability surfaces. FR2 stays Frontier;
the Core list and owned runtime probes above are unchanged. No census integration,
threshold change, baseline re-pin, quota configuration/diagnosis or remediation.

The pre-withdrawal pinf3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c measured
29/30 sealed quota cases. Frozen CaseEscapedSpace's expected row opposes the sealed
parent-ID rule; neither is changed or excluded. Actual mocked permission-truncated
mapping also produced false disabled confidence, and primary kernel sources separate
tmpfs active accounting from runtime enforcement. Byte-exact rejected source/note,
source evidence and counterexamples are in `.ufo/waves/round-23/rejected/` and
`corpus/lessons/round-23.md`, not a runnable supported surface.

C1 is independent: the schema-v2 retention accounting cutover removes only the
misleading duplicate key, with exact-source/identity/output guards and no clearance
authority. Kernel-visible mechanism observations do not transfer quota configuration,
cause or reclamation authority: tsukuroi/operator own configuration/diagnosis, souji
proposes eligible residue handling, and operator approval owns reclamation. Four
retention hits, original permission11/12red, two unknown dispositions and blocked
baseline acceptance remain; no rank or subsequent-round authority is granted.

## Round-24 appended scope notes (2026-10-22)

- **Core, one-shot system pressure reading (FR12 partial advance, admitted round 24):**
  `tools/mori-pressure.py` (round-24 build) reads the four **system** pressure files
  `/proc/pressure/{cpu,memory,io,irq}` once each and reports one JSON object
  (`schema: mori-pressure-v1`): a per-resource `state` (`ok`, `absent`, `unsupported`,
  `unreadable`, `malformed`, `counter_regressed`), the `some`/`full` averages and the
  cumulative `total`, a `verdict` (`PRESSURE_OK` | `PRESSURE_HIGH` | `PRESSURE_PARTIAL` |
  `PRESSURE_UNAVAILABLE`) and `findings[]` (`PRESSURE_HIGH` at or above `--warn-avg10`,
  default 10.0, **labeled local, not calibrated**). System CPU `full` is reported with
  `full_system_undefined: true` and is never a threshold input and never evidence of no
  stall; the `irq` resource carries `full` only, so its absent `some` line is expected
  (`some: null`) and never malformed. Unavailable is never zero: `absent`, `unsupported`
  and `unreadable` are named states and **no cause is inferred** from them — kernel and
  boot configuration diagnosis belongs to tsukuroi. The reading is host scope: a
  system-wide `PRESSURE_HIGH` is evidence to correlate, never proof that a lane, a wave
  or the fleet caused it. Read-only: the probe opens the PSI files read-only, registers
  no PSI trigger, writes nothing to `/proc`, `/sys` or a cgroup, and changes no service
  or package. It is not a census surface: no `SURFACE` row, no census finding id, no
  DRIFT verdict, no baseline re-pin; the census keeps reading only the user-slice
  `memory.pressure` it already reads. Knowledge: `corpus/knowledge/system-pressure-r24.md`
  (lands with this round); sources opened this round are the Linux v7.2 PSI
  documentation, `kernel/sched/psi.c`, the cgroup-v2 pressure files, the PSI Kconfig and
  boot parameter, the resource enum and the commit that added IRQ pressure (S090–S095, S145);
  `proc_pressure(5)` does not exist (S146: no such page in the man-pages 6.20 release; the man7 URL returns HTTP 404).
- **Still FR12 frontier:** the resident, event-driven PSI trigger watcher and
  **cgroup-scoped** CPU/IO/IRQ pressure. A trigger watcher is a *write* of a threshold
  into `/proc/pressure/*` plus a polling process, not a one-shot read, and the
  per-cgroup `*.pressure` files are a different scope; the one-shot system read above
  observes neither. The opt-in `--interval S` two-sample mode is **outside** the one-shot
  Core statement: its added cost is about S seconds and it fails the round-8 dwell rule
  (`corpus/knowledge/surfaces-r8.md:47-48`), so a stall rate and its latency budget stay
  with FR6/FR12. FR12 is narrowed here, not closed.
- **Limits carried with the Core row:** a zero or non-advancing `total` is not evidence of
  no stall — the root cgroup's `cgroup.pressure` switch can stop `psi_system` accounting
  while `/proc/pressure/*` stays readable, and the probe does not detect that (wave-1
  finding `CriticC2Semantics.md` F3; the upstream anchors are carried by the knowledge
  note); the threshold is a local placeholder, so FR8 stays open; `avg10` is a decaying
  average, not a ten-second window; and the `full` arm of memory and IO adds no verdict
  information beyond their `some` arm at an equal threshold (`CriticC2Semantics.md` F4).
- **Owns-scope extension (append-only; `PROVINCE.md:6-10` is left byte-unchanged):** the
  Core row above extends the owned read-only probe list named at `PROVINCE.md:6-10`,
  which today names memory pressure, to the one-shot system CPU/IO/IRQ/memory pressure
  read. The header sentence itself is not rewritten by this round; the extension is
  recorded here so no sibling line-range pointer into `PROVINCE.md:3-16` moves.
- **Admission state (2026-10-22):** the tool and its twelve frozen cases are landed
  (`tools/mori-pressure.py`, `tools/fixtures/mori-pressure/cases.json`); the declared
  after-value command prints `MORI_PRESSURE_SELFTEST: PASS 12/12` (exit 0) and one live
  host run returned `PRESSURE_OK` with all four resources `ok`, `irq` `some` null and
  system CPU `full` flagged undefined. The Core row above was **admitted** by the round-24
  non-author closure. No frontier row is closed, no other lane's surface is claimed, and no remediation
  is added.
- **Adjacency (wave-2 finding CriticHarmAxes A1; wave-1 ConnectSiblingPsi):** tsukuroi's census reads the same
  system `/proc/pressure/memory` file (`../tsukuroi-shokunin/tools/tsukuroi-census.sh:376,1100-1115`) for OS memory
  triage and routes fleet correlation of host pressure to mori (`../tsukuroi-shokunin/PROVINCE.md:30-33`). Shared
  evidence is not shared ownership: mori reports the reading as fleet resource runway; explaining a high IRQ or
  memory reading as a device, driver or OS fault stays with tsukuroi.

## Round-25 appended scope notes (2026-10-22)

- **Core, harness background-job capacity runway read (new FR15 advance, admitted round 25):**
  `tools/mori-job-runway.py` (round-25 build) reads two byte sources and reports one JSON object
  (`schema: mori-job-runway-v1`): the **configured** `async.maxJobs` from one settings file
  (`--config`, default the operator's OMP settings file), the **clamp** compiled into the installed
  harness binary (`--binary`, default the real path of `omp` on `PATH`) located by pattern over
  its bytes, and the **setting default** from the binary's own settings table. It then reports
  `effective = max(1, min(clamp, base))` — where `base` is the configured value, or the schema
  default when the file does not carry the key — with the verdicts
  `RUNWAY_AS_CONFIGURED | RUNWAY_CLAMPED | RUNWAY_DEFAULT | RUNWAY_UNKNOWN` (exit 0 / 1 / 0 / 2).
  On this host the read is configured 200, clamp 100 (one site), setting default 100 (one site),
  effective 100, verdict `RUNWAY_CLAMPED`, exit 1: the operator's configured value is **clamped
  by the binary**, not honoured. The clamp lives at the manager's construction site
  (`maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))`), so the ceiling is a
  property of the shipped harness, not of the configuration file.
  **The read is a cap, never a count.** The tool reads no job list and cannot read the number of
  running jobs from outside a session; an effective value is not evidence that any job ran, that
  the runway was free, or that a session is near its cap. `RUNWAY_UNKNOWN` (exit 2) means *this
  tool cannot derive a number from the bytes it was pointed at* — a malformed value, a missing
  clamp pattern, an unreadable binary, or two clamp sites with different numbers — and never
  means "unlimited", "zero" or "no clamp": an absent match is a failed lookup.
  Read-only: it opens one file and one binary for reading, never runs `omp`, never writes a
  settings file and never touches another configuration surface. It is **not** a census surface:
  no `SURFACE` row, no census finding id, no DRIFT verdict, no baseline re-pin.
  Knowledge: `corpus/knowledge/harness-job-capacity-r25.md` (lands with this round); the upstream
  sources opened this round are S098–S103 and S112–S113 (`corpus/SOURCES.md:104-110,118-119`),
  all at oh-my-pi tag `v18.12.6` (commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`), plus the
  installed binary as an own-work row (S102).
- **FR15 — Harness background-job capacity runway** (new row; FR1–FR14 are unchanged and FR14 is
  **not** advanced). First evidence: `corpus/knowledge/harness-job-capacity-r25.md:36-221`;
  `corpus/SOURCES.md:104-110,118-119`. Boundary: the read reports the cap the harness would
  compute from the file and the binary it is pointed at. **Still frontier:** the live count of
  running non-queued jobs in any session (not readable from outside that session); the scope in
  which a counted population lives — one manager per root session tree, children borrowing their
  parent's, so the same *number* applies to every manager while the *population* is per tree, and
  a refusal cannot be attributed to a session from outside it; and every settings layer the tool
  does not read — the project layer (`<cwd>/.omp/`), `--config` / `PI_CONFIG_FILES` overlays,
  runtime overrides, and agent-dir relocation by `OMP_PROFILE`/`PI_PROFILE` or
  `PI_CODING_AGENT_DIR`. The tool reads one file; the runtime resolves a stack, so `configured` is
  that file's value and `effective` is the cap that *would* apply if it were the effective one.
  Also frontier: why the ceiling is 100, what filled a runway when a refusal appeared, and any
  behaviour of other harness versions.
- **Adjacent (kumitate owns the harness mechanism; the operator owns the configuration):** the
  semantics behind the clamp — what the job manager counts (`running` and not `queued`, every job
  type, so a background shell job and a subagent task share one runway), the exact refusal text,
  and the fact that only a top-level session builds the manager — are kumitate's OMP task/hub
  ground (`../kumitate-shokunin/PROVINCE.md:3,19`; its OMP contract entry still has no
  `async.maxJobs` row and still records the effective live OMP setting as UNKNOWN). Mori's part
  is the bounded read and the report of it; it does not own the mechanism, proposes no change to
  `async.maxJobs` or to any settings file, and does not judge the fleet seat gate, which counts a
  different population under a different number (85 on this host, default 200; the harness cap is
  100). Changing harness configuration is operator-owned.
- **Owns-scope extension (append-only; `PROVINCE.md:6-10` is left byte-unchanged):** the Core
  bullet above extends the owned read-only probe list named at `PROVINCE.md:6-10` with a fourth
  resource class — the harness's own background-job concurrency ceiling. The header sentence
  itself is not rewritten by this round; the extension is recorded here so no sibling line-range
  pointer into `PROVINCE.md:3-16` moves.
- **Admission state (2026-10-22):** the tool and its twenty-one frozen cases are landed
  (`tools/mori-job-runway.py`, `tools/fixtures/mori-job-runway/cases.json`); the declared
  after-value command prints `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` (exit 0) and one live host
  run returned `RUNWAY_CLAMPED` with effective 100, exit 1. The Core bullet above was **admitted
  by the round-25 non-author closure**. No frontier row is closed, no other lane's surface is
  claimed, and no remediation is added.

## Round-26 appended scope notes (2026-10-22)

- **Core, one-shot userspace OOM killer read (FR10 partial advance, admitted round 26):**
  `tools/mori-oom-killers.py` reads `systemctl show` for `earlyoom.service` and
  `systemd-oomd.service`, the earlyoom unit journal of the current boot (counts only, in memory) and the
  count of systemd-oomd kill notices (`MESSAGE_ID=d989611b…`) this boot, and reports one JSON object
  (`schema: mori-oom-killers-v1`) with a `KILLER_ACTED` / `KILLERS_UNKNOWN` / `KILLERS_QUIET` verdict.
  Counts are earlyoom log lines, not processes killed. Knowledge: `corpus/knowledge/userspace-oom-killers-r26.md`.
- **Still FR10 frontier:** send lines of an earlier invocation of an active earlyoom in the same boot (reported
  in `earlier_invocation_send_lines`, not a verdict input); previous boots (the round-26 per-boot capture shows
  38 SIGTERM and 1 SIGKILL send lines in the previous boot, none in the current one); oomd cgroup xattrs and
  D-Bus `Killed` signals; fleet attribution of any victim.
- **Adjacency unchanged:** diagnosing, configuring, enabling or tuning either killer, and the earlyoom and
  systemd-oomd unit state as host diagnosis, stay with tsukuroi and the operator; mori cites
  `tsukuroi-shokunin@157ee255:corpus/knowledge/memory-pressure-r25.md` and absorbs none of it.

## Round 27 — FR10 victim selection (knowledge, no new tool)

- **Core, knowledge (FR10 partial advance; round 27 closed `rejected-honest-stop`, so this advance is not admitted):** how earlyoom 1.9.0 and the Linux 7.2 kernel choose
  an OOM victim, where the fleet's `oom_score_adj` 200 comes from (systemd's per-user manager, not the harness), and
  what the fleet's records can and cannot attribute: `corpus/knowledge/oom-victim-selection-r27.md` (S148, S149,
  S150, S130, S151, S132, S142), with the SKILL.md `Round27` decision table.
- **Still FR10 frontier:** which `omp` process an `omp`-class send hit (the send line's 15-byte name cannot tell the
  session process from a second session or the text-prediction daemon); whether a signalled session process exits
  on SIGTERM; the text of the host's prefer/avoid expressions (never read, by rule); seat-level attribution of any
  victim.
- **Adjacency unchanged:** the host's OOM configuration stays with tsukuroi and the operator; the entry cites
  tsukuroi's kill-plane entries and corrects their "+200 band first" model without absorbing them.

## Round-30 correction — head lists and stale pointers (routed R7)

Same-line substitutions this round (no line moved, so the lane's line citations into this file stay valid): `:25`
round-16 build now reads admitted; `:236`, `:283`, `:294`, `:353-354`, `:359` read admitted (rounds 24, 25, 26,
MANIFEST at fleet `63729047`); `:375` states round 27 closed `rejected-honest-stop`; `:47`, `:90`, `:94` point at the
fleet-root `../.ufo/waves/kaika-w1/` files (the `../fleet-ledger/` prefix never existed); `:66` tsukuroi owns range is
`PROVINCE.md:8-14`; `:68` the secret rule is `SKILL.md:374-393`. Evidence: `.ufo/waves/round-30/w1/DraftProvinceR7.md`,
independent scout `.ufo/waves/round-30/w1/ScoutProvinceStale.md`.

The `## Core` head (`:22-28`) lists seven bullets and does not repeat the Core additions appended per round: round 17
`:103`, `:108`; round 18 `:125`, `:132`, `:134`; round 20 `:145`; round 24 `:236`; round 25 `:294`; round 26 `:359`;
round 27 `:375`. The `## Frontier` head (`:44-57`) lists FR1–FR14; FR15 is the round-25 appended row at `:321`.
Neither head is a completeness claim. Still open (named, not fixed this round): sixteen `tools/` files and six
fixture directories are not named here (ScoutProvinceStale items 4–5); the census citation `tools/mori-census.sh:211-212,282`
at `:94` has drifted (the default now sits near `:237`, `:321`; ScoutProvinceStale item 8).
