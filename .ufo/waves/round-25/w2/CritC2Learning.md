Verdict: C2 partly holds. The count reproduces (exit 0, `verified_rows` 6 at 5e7c04ec), and MP4 is a real stronger entry that supersedes a weaker one. But `verified_rows` measures whether the evidence links are present, not whether any verdict is right: 9 of 10 adversarial mutations still score 6 of 6, including inverted statements and fabricated Gate quotes. Only MP4, plus the conjunction part of MP5, is new tsukuroi knowledge. The weaker claim that MP4 refutes stays live and unsuperseded in a second tsukuroi note, `kill-event-deep-r8.md:255`.

Seat: TsukuroiR25.CritC2Learning-2 (critic, wave 2). Surfaces: the C2 claim (SCORECARD.md:793, :797, :813), the goal's Learning-claim bar (/home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md:145-149), tools/check-memory-pressure.py, the entry and its JSON twin, the round-25 lesson's Gate, the SKILL.md section at :2303-2320, and the supersession notice at oom-event-plane.md:471-473.

## Findings

1. [obs] **The count reproduces.** `python3 tools/check-memory-pressure.py --revision 5e7c04ecb02735491456de2b8bc44550d0db4609`, run from the lane repo, exits 0 with `verified_rows` 6, status PASS and 0 findings (output kept at /fast/scratch/hyaku/tsukuroi-r25/w2/CritC2Learning/lane-run.json). It matches the receipt /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/measure/exits.txt (`c2 5e7c04ec… exit=0`). The counted pointers are MP1 at lines 14 and 15, MP2 at 14 and 3, MP3 at 34, 38 and 42, MP4 at 73, MP5 at 106 to 108, and MP6 at 52 and 50 (measure/c2-5e7c04ec.json).

2. [obs] **`verified_rows` passes on field presence; a wrong verdict still counts.** I built a sandbox with `git archive 5e7c04ec | tar -x`, ran `git init -b master` with no remote, and ran the lane's checker on each mutated commit (harness /fast/scratch/hyaku/tsukuroi-r25/w2/CritC2Learning/mutate.py; results in mutate-out.jsonl; exit 0). Each row below is one mutation and its result:

| Mutation | exit | verified_rows |
|---|---|---|
| none (pristine) | 0 | 6 |
| every verdict set to `refuted` | 0 | 6 |
| MP4, MP5 and MP6 statements inverted ("auto means oomd actively monitors…", "90 percent rule fires on swap alone", "userspace SIGKILL increments oom_kill") | 0 | 6 |
| every entry quote replaced by "this sentence appears in no opened source" | 0 | 6 (only non-blocking `MP-QUOTE-MISMATCH`) |
| every S115 to S124 Gate quote in corpus/lessons/round-25.md replaced by fabricated words | 0 | 6 (only non-blocking `MP-QUOTE-MISMATCH`) |
| corpus/knowledge/memory-pressure-r25.md deleted | 0 | 6 |
| every `supersedes` and `mori_cross_reference` removed | 0 | 6 |
| every capture pointer moved to line 10 (the systemd feature-flag line, token `+PAM`) | 0 | 6 |
| SKILL MP decision section replaced by one unrelated table line `\| MP1 MP2 MP3 MP4 MP5 MP6 \| unrelated \|` | 0 | 6 |
| every row given one source S118 and the quote "Shows pressure stall information for memory." | 0 | 6 |
| SKILL MP decision section removed | 1 | 2 |

   Why, in code:
   - R1 only tests that `verdict` is a non-empty string (tools/check-memory-pressure.py:540-545).
   - A quote mismatch is `blocking=False` (:603-605).
   - Gate quotes are never compared with the source bytes; the sha256 values recorded in the entry are prose and are never read.
   - `ENTRY_MD` is declared (:55) but never read.
   - R4 only needs some unique line that contains the token, and does not check that the line bears on the row (:413-444).
   - R5 accepts the row id in any SKILL table line (:626-629). In the last case, MP1 and MP6 still pass through the registry line SKILL.md:2355 ("six rows MP1 to MP6").

   [inf] This is not a coding defect against the declaration: SCORECARD.md:797 defines a counted row as exactly these presence rules, and the checker's own docstring says "a count of evidence links" (:34). So 6 is sized to the links that were verified, not to verdict truth. Verdict truth is untested by any committed instrument. Round 24's lesson made the same point ("verdict truth and source fit require review", SCORECARD.md:772), and wave-1 attack 9 predicted it (.ufo/waves/round-25/w1/CritC2Learning.md:50-53). Impacted axes: calibration (risk of over-reading 6 as 6 true rows) and depth.

3. [obs] **Learning claim: only MP4, plus part of MP5, is new knowledge that supersedes a weaker tsukuroi entry. MP1, MP2, MP3 and MP6 restate held ground.**
   - The round's own refinement concedes the four restatements: "MP1, MP2, MP3 and MP6 restate ground the sibling lane mori already holds" (SCORECARD.md:813).
   - MP6 duplicates mori's SKILL error-pattern row, which cites the same kernel lines: "`oom_kill=0` (cgroup `memory.events` or `/proc/vmstat`) | no **kernel** OOM kills — not "no memory kills": both counters move only at the kernel victim site ([oom_kill.c:935-936 v7.2]" (`git -C /home/vgpnk/Projects/shokunin/mori-shokunin show HEAD:SKILL.md`, line 30, HEAD e0e33c1). It also duplicates mori's userspace-oom-killers-r12.md "These userspace kill paths do not increment the kernel OOM counters" (Claim section).
   - MP5's three default values, and its reading of `ManagedOOMMemoryPressureLimit=0` as the default, were already in tsukuroi's own note: "all defaults: `SwapUsedLimit=` 90 %, `DefaultMemoryPressureLimit=` 60 %, `DefaultMemoryPressureDurationSec=` 30 s … `ManagedOOMMemoryPressureLimit=0` (=default)" (`git show 5e7c04ec:corpus/knowledge/kill-event-deep-r8.md`, line 255).
   - New in MP5: the memory-and-swap conjunction, the 5 percent swap floor, and the rule that the limit is ignored unless the unit is set to `kill`. The conjunction and floor are confirmed by systemd v262 oomd.conf.xml:166-168 (sha256 36ae3e47…6617, re-fetched, exit 0): "If the fraction of memory used and the fraction of swap used on the system are both more than what is defined here".
   - MP4 is the real supersession: `auto` means not monitored, which refutes "already set … oomd would likely have acted *before* the kernel" (oom-event-plane.md:344).
   - [obs] MP4's scoped action holds on the host today. My read-only scan with `systemctl show --all -p Id -p ManagedOOMSwap -p ManagedOOMMemoryPressure '*'` found 0 units set to `kill` among 465 system units, and the same scan with `--user` found 0 among 290 user units (exit 0).
   - [inf] The goal's bar ("a stronger entry superseding a weaker one", goal file :146) is met by MP4 alone. A count of 6 overstates the learning by a factor of about three.
   - The PROVINCE label "PROVINCE core: OOM and memory plane" (SCORECARD.md:793) is still not a Core heading. Core lists systemd user units and timers (PROVINCE.md:10); memory appears only at PROVINCE.md:30-33. Wave-1 attack 1 raised this, and it was left unchanged.

4. [obs] **Duplicate authority: the same weaker claim survives unsuperseded in kill-event-deep-r8.md:255.** The r8 note, which describes itself as "Kill-event plane deepened" (line 1), still says "`ManagedOOMSwap=auto` **and** `ManagedOOMMemoryPressure=auto` are already set on `user-1000.slice`, `user@1000.service` and sampled app scopes". It also says "[inference] the swap rule (90 %) is below event A's measured 99.9999 % saturation, so oomd would have had a trigger; it acts by killing the *eligible descendant cgroup*" (column 4 of line 255).
   - `git diff --stat b9046016 5e7c04ec -- corpus/knowledge/` shows that only memory-pressure-r25.{md,json} and oom-event-plane.md (+4 lines) changed.
   - `git grep -n 'would have had a trigger'` at 5e7c04ec finds only kill-event-deep-r8.md:255.
   - The entry's `supersedes` lists name oom-event-plane.md:274, :301, :344 and :347 only.
   - [inf] A reader who reaches the later r8 note gets the refuted inference with no pointer to MP4. That is the "stronger entry superseding a weaker one" left half done. Impacted axes: depth and calibration.

5. [inf] **The second "contradiction" in the R25 notice is overstated.** oom-event-plane.md:473 says line 344 is contradicted on two points; the second is that the 90 percent rule needs memory and swap both above the limit, not swap alone.
   - Event A was a global OOM (oom-event-plane.md:348: "global OOM occurred"), so memory use at that moment was at or near 100 percent. The conjunction would very likely have held.
   - systemd v262 checks the memory arm as `oomd_mem_available_below(&m->system_context, 10000 - m->swap_used_limit_permyriad) && oomd_swap_free_below(...)` (src/oom/oomd-manager.c:478-479, sha256 052f19b3…3a15, fetched, exit 0).
   - The conjunction narrows :344's wording. It does not refute :344's trigger conclusion. Only MP4's point (`auto` means unmonitored, and a swap kill also needs `ManagedOOMSwap=kill` per oomd.conf.xml:169-170, "depends on what the unit has configured for ManagedOOMSwap=") refutes it.
   - [unk] Memory-used fraction at event A's kill second; it is not in the round-25 capture.

6. [obs] **MP6's counted pointer misstates the kernel source; the row is "verified" through a mislabelled line.**
   - memory-pressure-r25.md:335 counts capture line 50 `oom 0` as "the cgroup `memory.events` OOM counter, the class the kernel kill path feeds".
   - In Linux v7.2, `oom` is `MEMCG_OOM`, raised in `mem_cgroup_oom()` before any kill: `memcg_memory_event(memcg, MEMCG_OOM);` (mm/memcontrol.c:1925, also :4861; sha256 8a28e0bc…fd5e, fetched, exit 0).
   - The kill path at mm/oom_kill.c:935-936 feeds `MEMCG_OOM_KILL`, which is the `oom_kill` field (sha256 452f1348…6b4e, matching S119).
   - cgroup-v2.rst:1498-1500 defines `oom` as "The number of time the cgroup's memory usage was reached the limit and allocation was about to fail".
   - MP6's other counted pointer, `oom_group_kill 0` (line 52), is "The number of times a group OOM has occurred" (:1510-1511).
   - Neither counted pointer is the `oom_kill` field that MP6's statement is about; that field (lines 51 and 62) is not unique. The same md section also lists line 50 as a supporting, non-unique line (:340), which contradicts the table five lines above.
   - The checker passes this because the token `oom 0` is on line 50 (finding 2).

7. [obs] **MP2's and MP4's verdict facts have no counted pointer** (wave-1 attack 6 warned about this; the integration accepted it).
   - MP2's verdict "the two reads in the capture differ" rests on line 21, which is not counted. The counted pointers are the first read (line 14) and the first timestamp (line 3).
   - MP4's core fact, `auto` on four units, rests on lines 112 to 140, none of them counted. The only counted pointer is `inactive` (line 73).
   - [inf] For these two rows, R4 certifies an adjacent line, not the premise.

8. [obs] **MP1 and MP3 are correct, but rest on an inference that an opened-class source settles.** systemd v262 src/oom/oomd-util.c:680-684 reads `cg_get_path(path, "memory.pressure", &p)` then `read_resource_pressure(p, PRESSURE_TYPE_FULL, &ctx->memory_pressure)` (sha256 2e94450a…7e7a, fetched, exit 0). That makes "the `full` line is the one the oomd rule reads" checkable, but the entry marks it as an inference (memory-pressure-r25.md:53-55) while giving MP1 the verdict `verified`, which its own vocabulary defines as "holds on this host on the counted evidence" (:15-16). The counted MP1 lines are `/proc/pressure/memory`, which, by MP3's own statement, oomd does not read.

9. [obs] **The SKILL row carries a claim the entry does not hold.** SKILL.md:2314 (MP2 action) adds "because the root cgroup's `cgroup.pressure` switch can stop `psi_system` accounting while `/proc/pressure/*` stays readable (mori limit, cited not absorbed)". `git grep -n 'cgroup.pressure'` over memory-pressure-r25.md and .json at 5e7c04ec returns nothing, and no S115 to S124 Gate quote covers it. MP5's SKILL cell similarly cites `pacman -Qkk systemd`, which is outside the frozen capture (SKILL.md:2317), against the input boundary at SCORECARD.md:788.

## Fixable defects compared with tradeoffs for the canonical judge

- Fixable within the round, with targets unchanged:
  - Append a dated current-use notice to kill-event-deep-r8.md that names line 255 and points to MP4 (finding 4).
  - Correct the "why" text for the MP6 line-50 pointer (memcg limit OOM event, not the kill path), and remove the md self-contradiction at :340 (finding 6).
  - Reword the second point of the R25 notice as a narrowing, not a contradiction (finding 5).
  - Drop or source the `cgroup.pressure` clause in the SKILL MP2 cell (finding 9).
- A tradeoff the judge must weigh, not a defect to patch after landing: `verified_rows` = 6 is faithful to SCORECARD.md:797 but measures evidence links, not truth (finding 2), and the learning content is one row of new knowledge plus one partial row (finding 3). Making `MP-QUOTE-MISMATCH` blocking, reading the md, or restricting R5 to the round-25 section would change the instrument after measurement. The rule "never narrow a target after landing" (goal :157) cuts the same way against tightening it now. Those changes belong to round 26.

## Smallest safe correction

The closure should credit C2's Learning claim to MP4's supersession of oom-event-plane.md:344 only. It should require the kill-event-deep-r8.md:255 notice before admitting that credit, and record `verified_rows` 6 as "6 rows with complete evidence links; verdict truth reviewed per row by non-authors" rather than as 6 verified facts. Corrections to the MP6 pointer label and the R25 notice wording are text edits that do not move the count; I confirmed in the sandbox that the count does not depend on them.

Scope: read=SCORECARD.md:784-861, goal file lines 130-164, tools/check-memory-pressure.py (full), tools/_revision.py grep, memory-pressure-r25.md (full), memory-pressure-r25.json (full via read and git show), oom-event-plane.md:260-473, PROVINCE.md:1-49 and grep, SKILL.md:2300-2324 and grep, corpus/lessons/round-25.md:1-40, kill-event-deep-r8.md:1-4 and :248-270, capture.txt (full), w1/CritC2Learning.md, measure/exits.txt and c2-5e7c04ec.json, mori-shokunin HEAD (e0e33c1) SKILL.md:28-32, corpus/knowledge/userspace-oom-killers-r12.md and git grep, seven upstream files at tags v262 and v7.2 (six saved under src/, systemd-oomd.service.xml read through a pipe); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/CritC2Learning.md, /fast/scratch/hyaku/tsukuroi-r25/w2/CritC2Learning/{mutate.py,mutate-out.jsonl,lane-run.json,sb/ (git archive sandbox, no remote),src/ (fetched upstream files)}; executed=python3 tools/check-memory-pressure.py --revision 5e7c04ec… in the lane repo (exit 0), git archive 5e7c04ec piped to tar into the sandbox plus git init/add/commit/reset inside the sandbox only, python3 mutate.py (11 cases, exit 0), read-only git show/grep/diff --stat/rev-parse/log on the lane and on mori-shokunin, systemctl show --all -p Id -p ManagedOOMSwap -p ManagedOOMMemoryPressure '*' and the same with --user (exit 0), ls of systemd drop-in directories, curl -fsSL of seven tag-pinned raw.githubusercontent.com files (exit 0 each), sed/grep over the fetched files and the capture
Model: not exposed
Installs: none
