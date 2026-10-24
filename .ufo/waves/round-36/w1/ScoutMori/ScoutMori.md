# ScoutMori — mori declaration freshness

Seat: ScoutMori. Lane read: `/home/vgpnk/Projects/shokunin/mori-shokunin`. No production edit. No install. Artifact: `mori-head.md` in this directory.

## Findings

1. **Tip.** `master` = `HEAD` = `13f3db7e5c7163e7ef300259ff597a42a79f81f1` (`2026-10-23 23:48:18 -0300`, `round-38: dispatch-log landing record for 96f7f97`). Detached checkout; `HEAD` equals `master`. Confidence: high (two `rev-parse`s).

2. **Tip moved during the read.** At `02:47:23Z` master was `b6993744171a05efc627b5e0664489c31aa5214e`. Reconfirm at `02:48:32Z` is `13f3db7e`. `git diff --stat b6993744 13f3db7e -- PROVINCE.md SCORECARD.md LOG.md` is `SCORECARD.md` one line (`evidence/gate-after.txt:21` → `:22`). PROVINCE blob `b84802587f4ad9a9c5738bd27a9bc3cccc246710` and LOG blob `809c21a3ed4c245905b754b09e428cc467dcecaf` unchanged. Worktree of the three files matches `13f3db7e` (`diff --numstat` empty). Confidence: high.

3. **Coredump / kill handling is still Core, with named Frontier remainder.** `PROVINCE.md:20` `## Core`; `:24` Kill/OOM classes includes coredumps and a distinct signal-11 coredump count. `PROVINCE.md:42` `## Frontier`; `:44` FR1 attribution stays frontier after the round-13 notice-plane advance; `:53` FR10 head stays frontier (partial Core notes at `:359` admitted, `:375` not admitted); `:56` FR13 eBPF kill/OOM tracing stays frontier. `LOG.md:67-71` keeps the signal-11 vs generic-coredump taxonomy. `SCORECARD.md` has no `coredump` hit; `:717-718` repeats the FR1 Core/Frontier split. `kill-event` in LOG `:647`/`:653` is round-12 history; in `PROVINCE.md:66` and `SCORECARD.md:618` it is a citation of tsukuroi's `kill-event-deep-r8.md` on the Adjacent row. Confidence: high.

4. **TSUKUROI-F1-MEM-01 / ADJ-04 is on the tip, dated 2026-10-15.** `PROVINCE.md:71`, `LOG.md:676-677`, `SCORECARD.md:618`. PROVINCE still says acknowledgement/acceptance/resolution are unobserved; LOG and SCORECARD say the packet was answered (no retained kill overlap at `2026-10-15T04:53:46Z`). Confidence: high.

5. **No 2026-10-22 or 2026-10-23 tsukuroi handoff is acknowledged** in those three files. Sole `TSUKUROI-` id is `TSUKUROI-F1-MEM-01`. Tsukuroi `HEAD` `6d76fb20` does have `corpus/knowledge/adjacency-mori-oom-r27.md` (`verified-at: 2026-10-22`) and the JSON companion (`drafted_at: 2026-10-22`); those paths are absent from mori's three files. `PROVINCE.md:384` is mori's own "+200 band first" correction, not a receipt line. Confidence: high for absence on the three files; the tsukuroi file dates are observed on tsukuroi `HEAD`, not a claim that no other channel exists.

## Unknowns

- Whether mori recorded the 2026-10-22 overlap register outside PROVINCE/SCORECARD/LOG (SKILL was not the assigned surface; a side grep shows `SKILL.md:740` states the same "+200 band" correction and does not name `adjacency-mori-oom-r27`).
- Commits after `13f3db7e` (master was moving during this seat).

## Dependency

None blocked. Sibling seat artifacts were not required.
