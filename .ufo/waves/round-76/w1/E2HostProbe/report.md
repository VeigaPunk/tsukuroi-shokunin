# E2HostProbe verdict

**Host receipts complete.** Source-correct derivation gives `SystemMaxUse=256M`, `effective_limit=256M`, `SystemMaxFileSize=32M`; observed `148.6M`. All requested read-only host probes returned rc=0. No corpus/config/service changes; no tests/build/lint/formatters, no tool installs. Axes: depth/source correctness, C1 host evidence, C2 freshness.

## Evidence retained
- `01-config.txt`: full merged config, including size.conf.
- `02-usage.txt`: full requested outputs plus file count; systemd262.1-1, 13 journal files, specified boots pipeline3, drop-in birth2026-10-16 11:53:47.068871418 -0300. Commands and exits retained.
- `03-derivation.txt`: arithmetic, source anchors, runtime-floor caveat, and explicit correction of the requested wrong formula.
- `04-stale-carriers.txt`: exact historical text at journal-boot-plane.md:49-52,362-363; degraded-triage-r4.md:70; boot-plane.md:79-80,240, plus precise supersession scope.
- `05-usage-rule.txt`: per-file st_blocks/logical lengths and aggregation. 304360*512=155832320 allocated bytes=148.61328125MiB, matching rounded148.6M. Logical209715200 bytes; difference53882880. Largest logical file24MiB<=32MiB. No rotation schedule claimed.

## Correctness risks communicated to parent
1. Pinned manager:168 uses `LESS_BY(free,keep_free)` = saturating subtraction, **not min**. Correct host avail759892086784; used+avail760047919104; max_use268435456 binds. The wrong min formula happens to yield the same host limit, so the result alone cannot validate JD3's wording. S1Scout-12 supplied the v262 macro anchor; parent notified. KeepFree default is capped4GiB, not the uncapped15% value.
2. Runtime min_use/startup floor and daemon's loaded config are not introspected. Reported256M is a source-based configured-limit derivation, not proof of runtime-manager state; birth timestamp does not prove a reload.
3. `journalctl --disk-usage` excludes coredump payloads. Its148.6M cannot refute J2's historical3.9G coredump usage. Missing older records/exact rotation dates remain unknown. Existing append-only errata were already present and were not edited here.
4. Probes ran concurrently; filesystem values can drift. Supplied df and stat measurements agreed at their captures. No LSP tool was available; no supported-language code symbols were edited or refactored.

## Handoff
Parent owns integrated gates. No additional host-mutating action is warranted. Inspect JD3/default-cap wording in the sourced note/registry before accepting the C1 claim; inspect C2 errata for the coredump-vs-journal distinction. No blocker to this receipt deliverable.

Self-evaluation (advisory, not a claim judgment): accuracy4 (runtime floor not observable here); completeness4 (full requested probes retained, but no daemon-state introspection); clarity4 (formula discrepancy needs explicit caveat); actionability5 (exact receipts and parent correction targets); conciseness4 (raw outputs necessarily repeated across receipts). Overall4.2. Improvements: parent should close JD3 macro wording, keep freshness correction narrowly journal-scoped, preserve runtime-state caveat. The user should agree because outputs and limits are explicit rather than overstated.
