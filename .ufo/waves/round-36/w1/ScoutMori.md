# ScoutMori — mori declaration freshness

Same findings as `.ufo/waves/round-36/w1/ScoutMori/ScoutMori.md`. Detail and quotes: `.ufo/waves/round-36/w1/ScoutMori/mori-head.md`.

- Tip at `02:48:32Z`: `13f3db7e5c7163e7ef300259ff597a42a79f81f1` (`round-38: dispatch-log landing record for 96f7f97`, `2026-10-23 23:48:18 -0300`). Moved from `b6993744` during the read; PROVINCE and LOG blobs unchanged; SCORECARD delta is `evidence/gate-after.txt:21` → `:22` only.
- Coredump / signal-11 coredump count remains **Core** (`PROVINCE.md:8`, `:24` under `## Core` at `:20`). FR1 attribution, FR10 head, and FR13 eBPF kill tracing remain **Frontier** (`PROVINCE.md:42-56`). SCORECARD has no `coredump` token; `:717-718` restates the FR1 split.
- `TSUKUROI-F1-MEM-01` / `ADJ-04` is present (`PROVINCE.md:71`, `LOG.md:676-677`, `SCORECARD.md:618`) for the **2026-10-15** capture. No 2026-10-22/23 tsukuroi handoff is named. Tsukuroi `HEAD` `6d76fb20` has `corpus/knowledge/adjacency-mori-oom-r27.md` (`verified-at: 2026-10-22`); that name is absent from mori's three tip files.
- Verdict: Core/Frontier coredump split is current; adjacency is stale against the 2026-10-22 overlap register.
