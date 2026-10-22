# Round 25 — lesson (tsukuroi, attempt 1, 2026-10-22)

Fixture baseline for the C2 mutation set. The rows below are the sources the six MP rows of
`corpus/knowledge/memory-pressure-r25.md` cite. Every quote was copied from the page named in
its SOURCES row on 2026-10-22 and is at most 25 words.

## Gate

Sources opened this round (all on 2026-10-22, each quote copied from the opened page):

| Row | URL | Located quote (at most 25 words) | Opened by |
|---|---|---|---|
| S115 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | `The "some" line indicates the share of time in which at least some tasks are stalled on a given resource.` | SrcPsiDoc |
| S116 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | "The total absolute stall time (in us) is tracked and exported as well" | SrcPsiDoc |
| S117 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | "Shows pressure stall information for memory." | SrcCgroupV2 |
| S118 | https://man.archlinux.org/man/systemd.resource-control.5 | "ManagedOOMMemoryPressure=auto|kill Specifies how systemd-oomd.service(8) will act on this unit's cgroups." | SrcSystemdCode |
| S119 | https://man.archlinux.org/man/oomd.conf.5 | "DefaultMemoryPressureLimit= Sets the limit for memory pressure on the unit's control group before systemd-oomd will take action." | SrcOomdConf |
| S120 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | "The number of processes belonging to this cgroup killed by any kind of OOM killer." | SrcKernelOomCounter |

Registry changes: rows S115-S120 added (6 rows; tier A; kinds docs 6; status `mined`; opened
2026-10-22; used-by `corpus/knowledge/memory-pressure-r25.md`). Rows touched old→new: none.

## Recheck log

No registry row had its `recheck` cell updated in place this round. Every cited row was opened
on 2026-10-22 for the first time, so the opened-date arm of the C2 rule is the one that applies
to all six rows and the in-place recheck arm applies to none.

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R25-FIXTURE-BASELINE | fixture | This file is a fixture baseline for the C2 mutation set, not the lane's production lesson | MutMemPressurePlan | The mutation fixtures in `.ufo/waves/round-25/w1/MutMemPressurePlan/fixtures/` break one counting rule each; the runner drives `tools/check-memory-pressure.py` over temporary git repositories and records whether each mutant was killed |
