# mori-head — freshness (tsukuroi round 36, ScoutMori)

Observed `2026-10-24T02:48:32Z` (UTC). Read-only. No tools installed.

## Hash

- `master` = `HEAD` = `13f3db7e5c7163e7ef300259ff597a42a79f81f1`
- subject: `round-38: dispatch-log landing record for 96f7f97`
- author-date: `2026-10-23 23:48:18 -0300`
- parent: `96f7f97e890eb43dfd8c48986dff192ae8a050f3`
- blobs: `PROVINCE.md` `b84802587f4ad9a9c5738bd27a9bc3cccc246710`; `LOG.md` `809c21a3ed4c245905b754b09e428cc467dcecaf`; `SCORECARD.md` `fc1e977411dedc2958afb19cab0f68c934795077` (worktree matches; `git diff --numstat master --` those three files is empty)
- Checkout is detached (`git branch --show-current` empty) but `HEAD` equals `master`.

During this read `master` moved. At `02:47:23Z` it was `b6993744171a05efc627b5e0664489c31aa5214e` (`2026-10-23 23:23:21 -0300`, `round-38: instrument hardening…`). `git diff --stat b6993744 master -- PROVINCE.md SCORECARD.md LOG.md` is only `SCORECARD.md | 2 +-`: `evidence/gate-after.txt:21` became `:22` (round-38 transcription). PROVINCE and LOG blobs are identical across that move. Classification quotes below are from `13f3db7e`.

## Core vs Frontier (coredump / kill-event)

Still **Core** for structured coredump / signal-11 coredump counts. Still **Frontier** for kernel event-time attribution, leftover FR10 userspace-killer semantics, and eBPF kill/OOM tracing. `SCORECARD.md` at the tip does not contain the word `coredump`.

`PROVINCE.md:20` `## Core`

`PROVINCE.md:8` (Owns): `pair); kill/OOM-related catalog-ID records and signal-11 coredump records from`

`PROVINCE.md:24`:

> - **Kill/OOM classes** — structured, MESSAGE-free journal records carrying catalog IDs for kernel-OOM unit notices, oomd notices, coredumps, unit-process SIGKILL results and unit failures, plus a distinct numeric signal-11 coredump count; independently labeled user/system scopes, never summed. Positive OOM notices and observed `UNIT_RESULT=oom-kill` retain critical `OOM_KILL_JOURNAL`/DRIFT alarms. Failed-unit subject metadata preserves fleet-only `UNIT_FAILURE_JOURNAL` versus non-fleet `UNIT_FAILURE_OUT_OF_SCOPE` with tsukuroi triage routing; absent or unsafe subject metadata remains unknown. `SURFACE cgroup` retains selected-scope kernel memory-event counters, not a replacement for all journal alarms. Journal labels are client-set, not authenticated producer identity; records are not unique victims or fleet-cause attribution. Other structured signals are unimplemented; arbitrary signals without retained records remain unmeasured. See `corpus/knowledge/journal-alarm-routing-r14.md`.

`PROVINCE.md:42` `## Frontier`

`PROVINCE.md:44`:

> - **FR1 — Kernel OOM event-time attribution and fleet correlation** (state F1/F8 + art F2). First evidence: `corpus/knowledge/kernel-oom-line-attribution-r12.md:10-16`; `corpus/knowledge/audit-r11.md:203-204`. Round 13 advances structured system-journal notice records to Core; event-time kernel summary/victim token validation and fleet correlation remain frontier. No raw `MESSAGE` is emitted, and a host record alone does not prove a fleet-caused kill.

`PROVINCE.md:53` FR10 head remains Frontier (userspace OOM killers). Appended partial Core, not a head rewrite: `PROVINCE.md:359` `Core, one-shot userspace OOM killer read (FR10 partial advance, admitted round 26)`; `PROVINCE.md:365` `Still FR10 frontier`; `PROVINCE.md:375` round-27 victim-selection knowledge is labeled Core but `not admitted`.

`PROVINCE.md:56`:

> - **FR13 — eBPF kill/OOM tracing** (art F5). First evidence: `corpus/SOURCES.md:11-12,23-26`. Boundary: privilege and version matter; a resident tracer is outside the census, so retain this as knowledge/frontier only.

`LOG.md:67-71` (round-1 correction 7, still the tip text): signal-11 filter vs generic coredump count — taxonomy, not a Core/Frontier flip.

> **Round-1 correction 7 (appended 2026-10-15).** Coredump taxonomy recorded: the
> segfault probe filters `COREDUMP_SIGNAL=11` at the journal, which keeps it
> signal-specific — `terminated abnormally` lines are signal **5** (SIGTRAP) and share
> the coredump MESSAGE_ID without carrying the `dumped core` text, so neither a text
> grep nor a generic coredump count may stand in for it.

`LOG.md:647` and `LOG.md:653` say `kill-event` only as round-12 motivation (`mori-art.md` "kill-event ground uncovered"; "four kill-event knowledge entries"), not as a current Core/Frontier label.

`SCORECARD.md:717-718` (round-13 section, still present): `FR1 notice/result plane advances to Core; kernel victim-token attribution and fleet correlation remain Frontier.`

`PROVINCE.md:66` cites tsukuroi's `kill-event-deep-r8.md` on the Adjacent tsukuroi row (host diagnosis), not as mori Core.

## TSUKUROI-F1-MEM-01 / ADJ-04

Present at the tip. Only packet id `git grep` finds in the three files.

`PROVINCE.md:71`:

> - **Received packet TSUKUROI-F1-MEM-01 (ADJ-04):** `../tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:74-112` records the 2026-10-15T04:53:46Z capture as `prepared`; boot identity/event window were not captured, and acknowledgement/acceptance/resolution are unobserved. Its request is to compare the timestamp with watchdog/wave evidence if retained, not to infer an OOM or cause.

`LOG.md:676-677`:

> PROVINCE `## Core`/`## Frontier` (FR1–FR14)/`## Adjacent` (souji added; TSUKUROI-F1-MEM-01
> answered: no retained kill record overlaps 2026-10-15T04:53:46Z) + scratch-roots correction;

`SCORECARD.md:618`:

> | adjacency | **improved** | 6 (held) | unclaimed contract repair, not one of the round's three claims, so no counting command and no score move: souji added to PROVINCE `## Adjacent` (siblings named 4 → 5); inbound TSUKUROI-F1-MEM-01 answered in PROVINCE (no retained kill record overlaps 2026-10-15T04:53:46Z; all 5 are dated 2026-10-18); tsukuroi's `oom-event-plane.md`/`kill-event-deep-r8.md` cited from each kill entry |

Wording tension, observed: PROVINCE still says acknowledgement/acceptance/resolution are unobserved; LOG and SCORECARD say the packet was answered. The capture date in all three is 2026-10-15, not 2026-10-22/23.

## 2026-10-22 / 2026-10-23 tsukuroi handoffs

Not acknowledged in `PROVINCE.md`, `SCORECARD.md`, or `LOG.md` at `13f3db7e`.

`git grep` of `TSUKUROI-` over those three files returns only `TSUKUROI-F1-MEM-01`. No hit for `adjacency-mori-oom-r27`. Dates `2026-10-22` and `2026-10-23` in LOG/PROVINCE are mori's own round 24–37 notes.

Tsukuroi `HEAD` `6d76fb20f6ecbc940e5c8fff36c74060c885e161` does contain `corpus/knowledge/adjacency-mori-oom-r27.md` (`verified-at: 2026-10-22`) and `adjacency-mori-oom-r27.json` (`drafted_at: 2026-10-22`). Those names are absent from mori's three tip files. `PROVINCE.md:384` is mori's own outbound correction of tsukuroi's "+200 band first" model, not a receipt of that register. `PROVINCE.md:111` is a 2026-10-20 pacman-log note routed toward tsukuroi, not a 10-22/23 inbound packet.

## Freshness verdict

At `13f3db7e` (reconfirmed `02:48:32Z`; tip moved from `b6993744` during the read without touching PROVINCE or LOG bytes), mori still classifies catalog coredump records and the signal-11 coredump count as Core (`PROVINCE.md:8`, `:24`) and leaves kernel attribution (FR1), residual userspace-killer semantics (FR10 head plus the "still frontier" clauses), and eBPF kill tracing (FR13) on the Frontier list. The only named tsukuroi packet on those tips is the 2026-10-15 `TSUKUROI-F1-MEM-01` / `ADJ-04` answer; no 2026-10-22 or 2026-10-23 tsukuroi handoff, including `adjacency-mori-oom-r27`, is acknowledged there. Adjacency for this round is stale relative to that 2026-10-22 register and current relative to the Core/Frontier coredump split, which has not flipped.
