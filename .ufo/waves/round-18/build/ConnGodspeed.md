# ConnGodspeed

Axes: C1 depth, C2 operability, C3 freshness.

## Evidence

[obs] `spec.json` and `dispatch.json` are both present. The Goal/Contract string occurs once per file (`spec.json:3`, `dispatch.json:523`), not inside tasks. `dispatch.json:933` requires one batched task call.

[obs] Directive once per spawn task. `taskCall.tasks` is 81 names (`dispatch.json:526-926`). Each task starts `/skill:godspeed\n\n` and contains one Godspeed body (`Act directly via tool calls.` on 81 lines). No task line repeats that tag or `Name the axes`. `spec.json` has the body 81 times, `/skill:godspeed` zero times, and no Report trailer.

[obs] Seat count 81 is inside 64–100. `dispatch.json:6-19`: `waveMinLanes` 64, `waveMaxLanes` 100, `hardCeiling` 100, spawn 81, resume 0, total 81. The same 81 names, same order, are spec items, registry keys `dispatch.json:26-506`, task names `:526-926`, and `assignments.json`.

[obs] Roles agree across spec `role`, registry `role`, and task `agent`: executor 11, scribe 9, scout 20, reviewer 20, critic 6, connector 8, revenger 3, sentinel 1, mutation-tester 2, simplifier 1.

[obs] Report rooting is one relative trailer plus one absolute prefix. `reportDir` is `.ufo/waves/round-18/build` (`spec.json:4`, `dispatch.json:24`). All 81 Report lines are that directory plus `/<name>.md` (example `:867`). None are absolute. Absolute `reportDir` was refused (`invalid_report_dir`, `LOG.md:274-276`). The one contract sentence roots the trailer at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`. C2 patch and rerun side files are already absolute there (example `dispatch.json:806`).

## Move

Join that prefix once and admit only those paths. Do not absolutize `reportDir` or the 81 trailers. Do not spawn from `spec.prompt`: that drops the skill tag and the trailer. A parent-cwd relative write drops C1/C3 reports while absolute C2 files still land. Reject the unprefixed file. No ordinal change.

Risk: 11 executor tasks add “except your single labrat” (`dispatch.json:528`) against the leaf ban. Leaf wins.

Check: skill-tag lines = `<name>.md` trailers = 81; the four name lists stay equal.

Model: Grok 4.7. Installs: none.

Scope: executed=none
