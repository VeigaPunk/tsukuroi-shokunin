VERDICT: `unprovable-but-better` — C2's deliverable exists, is sourced and per-class, and survived wave-2 attacks with verifiable repairs; it improves the adjacency surface it names, but no counter can establish an ordinal change, so the claim stays in the exploratory class the declaration fixed.

# JudgeC2Exploratory — named non-author review of round-33 C2 (adjacency, exploratory)

The declaration's C2 row (`SCORECARD.md:1343` at `9c89ff4f093d07a6f92925518310ca6a7c8a2fa0`) declares a per-class examination: "for each kill or memory-pressure evidence class this lane's `SKILL.md` and census read, a sourced row of what tsukuroi retains, what goes to mori under ADJ-04, and mori's own declared scope quoted at a pinned mori revision", surface "PROVINCE.md ADJ-04 (one trigger for every class today) gains a per-class boundary note", after-value "a new note `corpus/knowledge/kill-oom-boundary-r33.md` and one appended ADJ-04 pointer in `PROVINCE.md`", verdict `unprovable-but-better` only with a named non-author reviewer on record. I am that reviewer (seat JudgeC2Exploratory, residual wave a3res).

## Findings

1. [obs] The declared surface change landed exactly as scoped. `git show dd426fe1ab1c2cb5a5f5319307e52b3dab390850:PROVINCE.md | tail -6` shows the append-only section `## Adjacent — ADJ-04 per-class boundary note (round 33, exploratory)` which names the note and states "it adds no route, no intake and no new trigger"; the ADJ-01..07 table above it is unchanged (the ADJ-04 row text at `PROVINCE.md:49` is byte-identical to the claim base — QB1 verified the `1f521b9→c8fcfbf` diff is one tail hunk `@@ -191,3 +191,7 @@`).

2. [obs] The prior state is documented as lacking this. `SHONEN.md:12` at `1f521b93` records "the kill and OOM classification boundary against SKILL.md:1078-1102 is unexamined", and prior `PROVINCE.md:44-52` is the ADJ-01..07 table where ADJ-04 is a single trigger ("Host pressure or a kill signal needs fleet/wave attribution…") covering every class uniformly. The note replaces that blanket with a per-class boundary: structured-notice overlap (systemd row), a shared-declared surface with a split stated on both sides (PSI row), signature-level gaps (swap/socket-throttle — "mori declares the theme, not these reads"), partial overlap (MemAvailable overlaps, Shmem unnamed), non-routable mechanism (teardown purge), non-dated counters (cgroup `oom_kill`), and precise packet routing (classes 3+4 feed the one `HANDOFF ADJ-04 mori class=kill-events` line; class 1's vmstat ledger never reaches a handoff). [inf] That is an examination producing distinctions ADJ-04's one trigger could not express — better, and the declared before-state says why the prior lacked it.

3. [obs] Wave-2 attacks were met by repair, not dismissal. CritC2Absorb (`a3w2/CritC2Absorb/CritC2Absorb.md`) found no scope absorption and no invented mori intake, plus a malformed table row (unescaped `|` in the teardown-purge grep). CritC2Gaps (`a3w2/CritC2Gaps.md`) found the seven-row table narrower than the declared domain: the census reads coredump entries, PSI, swap/sock-throttle and meminfo classes that had no rows, plus the `Failed with result 'oom-kill'` subtype and a needed "this census does not read oomd/earlyoom" caveat. At the tip the note carries a second table with exactly those four added classes, a closing paragraph naming the `oom-kill` subtype (`tsukuroi-census.sh:457` ↔ mori `UNIT_RESULT=oom-kill`) and the oomd/earlyoom absence, an L1 "Reading" paragraph resolving the routing ambiguity CritC2Absorb flagged, and the teardown row's grep pipes escaped (`KillMode=mixed\|TimeoutStopSec=5s\|teardown purge`, note line 15 at tip).

4. [obs] All seven original rows were independently re-opened by quote-check seats QB1–QB7 (`a3w2/QB*.md`), each reporting every lane pointer verbatim or accurate paraphrase at `c8fcfbf`, mori quotes verbatim at `24603186`, `none declared` greps reproduced where present, and no claimed intake beyond mori's declared scope. QB seats' only nits: an unbalanced parenthesis in one signature citation (QB3) and drift watches, since repaired.

## Independent spot-checks (three, as required)

- Lane: `git show dd426fe1:SKILL.md | sed -n '1097,1107p'` prints the class table exactly as cited — seven rows, e.g. line 1101 `kernel OOM kill (global)` with signature `` `-p err` entry `Out of memory: Killed process …`; `/proc/vmstat oom_kill` ledger `` and the "event A only: 1 print, ledger **1**" measurement the row compresses. [obs]
- Mori at `24603186b555dddb88ebd607e415e27bdea747b4`: `PROVINCE.md:8-9` contains verbatim "kill/OOM-related catalog-ID records and signal-11 coredump records from independently labeled user/system journals, plus cgroup `memory.events`…"; :24 is the `Kill/OOM classes` core bullet naming kernel-OOM unit notices, coredumps, unit-process SIGKILL results and `UNIT_RESULT=oom-kill`; :44 is Frontier item FR1 ("event-time kernel summary/victim token validation and fleet correlation remain frontier"); :359-361 declares the userspace-killer read (earlyoom/systemd-oomd) the note correctly says this census lacks. [obs]
- Post-Gaps rows: `git show dd426fe1:tools/tsukuroi-census.sh` at the cited lines — :400-401 default `PRESSURE_FILE`/`MEMINFO_FILE`; :1103-1109 read `memory.swap.events fail`, `memory.swap.peak`, `memory.stat` pswpin/pswpout, `sock_throttled`; :1131-1145 read MemAvailable/Shmem and PSI some/full avg300+total; :1402-1410 count `SYSLOG_IDENTIFIER=systemd-coredump`; :2780-2782 emit `HANDOFF ADJ-04 mori class=coredumps value=… state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER`. The added PSI row's mori quote is verbatim: `PROVINCE.md:287-291` at the pin says "Shared evidence is not shared ownership: mori reports the reading as fleet resource runway; explaining a high IRQ or memory reading as a device, driver or OS fault stays with tsukuroi." [obs]

## Why `unprovable` is the honest half of the verdict

5. [inf] No counting command exists by design; the improvement is precision of a boundary, not an ordinal change (the declaration itself pins adjacency 8→8). The note's negative cells rest on bounded greps over pinned files — reproducible but inherently bounded. Mori's declared scope is quoted at a fixed pin; mori can drift (the note's `recheck` line names the re-open procedure). Historical host counts were captured by wave-1 seats and verified for pointer accuracy, not re-certified as host fact.

6. [obs] Residual nit: `SHONEN.md` box 4 at `dd426fe` still reads "the kill and OOM classification boundary … is unexamined" — stale relative to the landed note. This is self-assessment wording lag, not a defect in the claimed surface (the declared change was the note plus the ADJ-04 pointer, both present).

7. [unk] Row line numbers cited by QB seats (`kill-oom-boundary-r33.md:9-15`) are off by +2 at tip because the `recheck` header line was inserted; all content verified regardless.

## Residual risk and verification gaps

- Historical counts (e.g., "0 prints in 13 boots", "3 notices A→2 B→1") rest on the round-8/round-33 captures; I verified the pointers, not the captures. [unk]
- I re-ran no `none declared` grep end-to-end myself; QB2 and QB7 re-ran theirs (exit 1, no output) and CritC2Gaps' bounded sweep is recorded at `a3w2/CritC2Gaps/source-bindings.txt`. [obs]
- The note's added rows were authored by the L1 after wave-2; my spot-check verified their key census and mori pointers, but I did not re-derive every cell.

Conclusion: better, verifiably so, within the exploratory class — `unprovable-but-better`.

Scope: read=frozen C2 declaration row (SCORECARD.md:1343 @9c89ff4), note + PROVINCE tail + SKILL class table + SHONEN box + census producers at dd426fe, prior PROVINCE/SHONEN at 1f521b9, mori PROVINCE.md @24603186, wave-2 attacks CritC2Absorb/CritC2Gaps and QB1–QB7 reports; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3res/JudgeC2Exploratory.md (+/tmp/r33note.md scratch); executed=read-only `git show`/`git log` on the lane and mori repos, sed/awk/fold/grep pipelines; no git writes, no probes, no sources fetched
Model: devin/swe-2
Installs: none
