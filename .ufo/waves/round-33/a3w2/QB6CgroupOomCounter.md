QB6CgroupOomCounter — C2 row re-check for class `cgroup oom_kill counter` (read-only)

VERDICT: all eight pointers in the row resolve — two verbatim quotes match, five lane pointers and one paraphrase all land on the claimed lines, nothing was not found, and the row asserts no mori intake or acceptance mori does not declare.

Row under test: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/kill-oom-boundary-r33.md:14` versus the seat original `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/B6CgroupOomCounter/row.md:3`. `diff` of the two lines differs only by a trailing newline on the seat file (seat file lacks it); row content is otherwise byte-identical [obs]. Lane commit re-opened: `c8fcfbf662db6debc6d7128c166ced31ca3176cf`; mori pin: `24603186b555dddb88ebd607e415e27bdea747b4`.

Per-pointer findings:

1. `SKILL.md:1106` (class-table row, signature and "2 slices × 1, `.local` 0" measurement) — verbatim match. `git show c8fcfbf6:SKILL.md | sed -n '1106p'` prints `| cgroup `oom_kill` counter | `memory.events[.local]` | **presence flag**: 2 slices × 1, `.local` 0 (`:120-134`) | flag, never an event count (round-6 rule re-confirmed) |`. Line number exact; the row's signature `memory.events[.local]` is verbatim [obs].

2. `corpus/knowledge/kill-event-deep-r8.md:120-134` (counter map and persisted-state qualification) — verbatim range, paraphrase holds. The range opens with the `### 3.4 The counter map` table at line 122 showing `oom_kill 1` on `user.slice` and `user-1000.slice` (the "2 slices × 1"), `.local` "all 0" on both, and the new `user@1000.service` at `oom_kill 0`; the persisted-state qualification ("the file behaves as **stored state**… read-time live-descendant aggregate would read 0", "[inference]") lands inside lines 132-134, within the cited range [obs].

3. `tools/tsukuroi-census.sh:1083-1100` (census scan) — verbatim range. Line 1083 is the comment `  # C4 — cgroup presence flags, bounded sweep over memory.events[.local]`; lines 1084-1100 are the sweep loop reading `$1 == "oom_kill"` values over `memory.events` and `memory.events.local` with the `-print | sort | head -n 4000` bound [obs].

4. `tools/tsukuroi-census.sh:72-73` (no counter-only dated-kill HANDOFF) — verbatim match. Line 73 is `# never a dated event, so it never reaches a HANDOFF line.` and line 72 names "a `memory.events` oom_kill presence flag" as one cumulative counter [obs]. Additionally code-backed: the only HANDOFF printf lines emitted are `class=kill-events` and `class=coredumps`, both `kind=dated-event` (`tsukuroi-census.sh:2777,2781`), and a selftest asserts `ABSENT:^HANDOFF` when a cumulative `vmstat oom_kill` counter is the only positive (`:2703-2705`) [obs].

5. `PROVINCE.md:49` (ADJ-04 minimum handoff evidence) — verbatim-adjacent paraphrase, exact line. Line 49 is the ADJ-04 row: "Capture time, boot/window, exact counter or PSI command/exit and observed value; distinguish presence, cumulative count and dated event. Request correlation, not a claim that a wave caused OOM". The row's "provide capture time, boot/window, exact counter or PSI command/exit and observed value, and ask for correlation rather than causation" is a faithful near-verbatim compression [obs].

6. Mori `PROVINCE.md:9` at `24603186` — verbatim match. Line 9 reads `independently labeled user/system journals, plus cgroup `memory.events` and the explicit same-boot journal window after a retained anchor;`; the quoted "plus cgroup `memory.events`" appears verbatim [obs].

7. Mori `SKILL.md:29` at `24603186` — verbatim-adjacent paraphrase, exact line. Line 29: `| Positive cgroup `oom_kill` | cumulative counter for the named source; counters alone identify neither the killed PID, event time nor fleet membership, and cover only the selected cgroup — descendants and other scopes sit outside it, so it is not a substitute for the journal `OOM_KILL_JOURNAL` alarm |`. The row's summary ("a positive cgroup counter cumulative… identifies neither PID, event time nor fleet membership, and covers only the selected cgroup") is near-verbatim, eliding "the killed" and "for the named source" [obs].

8. `none declared` cells — none exist in this row; the mori column asserts two declared items (both verified above). Re-grep to check for omitted declared scope: `git grep -i -E 'memory\.events|oom_kill|cgroup|oom' 24603186 -- PROVINCE.md SKILL.md` finds mori additionally declaring `SURFACE cgroup` kernel memory-event counters (`PROVINCE.md:24,26`), the `oom_kill=0` kernel-only error pattern (`SKILL.md:30`), and cgroup event counters as fleet evidence (`PROVINCE.md:14`, `SKILL.md:17,144`) — all consistent with, not contradicted by, the row [obs]. [inf] Omission, not misstatement: the row cites mori's two most direct lines only.

Intake check: the row asserts nothing about mori intake or acceptance — its last column states "No mori intake or acceptance is asserted" — and the mori column cites only items mori does declare at the pin. The row does not claim an intake mori does not declare [obs]. Mori at the pin does declare an ADJ-04-adjacent intake record (`PROVINCE.md:71` "Received packet TSUKUROI-F1-MEM-01 (ADJ-04)"), which the row neither asserts nor denies [obs].

Residual risk: none observed in scope. [unk] Whether rows B1–B5 and B7 verify is outside this seat's assignment.

Scope: read=kill-oom-boundary-r33.md row 14 + seat row.md; `git show` at c8fcfbf6 for SKILL.md:1095-1110, kill-event-deep-r8.md:115-140, tsukuroi-census.sh:60-80 and :1075-1105, PROVINCE.md:40-55; `git show`/`git grep` at mori 24603186 for PROVINCE.md and SKILL.md; wrote=.ufo/waves/round-33/a3w2/QB6CgroupOomCounter.md; executed=git show/diff/grep (read-only) and sed/diff/mkdir only.
Model: not exposed
Installs: none
