# DraftConformance (round 16, static)

**Wave 1 (build, policy v2):** 64 items; 64 dispatched tasks; band 64–100 (`dispatch.json`). `spawn-result.json`: 64 `pending`. `record-result.json` empty; registry `agentId` null. Completion unrecorded.

**Wave 2 (falsify, policy v1):** absent. Required: 32–64 seats; `UFO_CONFIG_PATH=…/ufo-wave-policy.json` (band 32–64); `reportDir` `.ufo/waves/round-16/falsify`; every item names its target. Round total 96–128.

**Conformance gaps:**
- Godspeed: §3 requires verbatim directive bytes; wave 1 carries `/skill:godspeed` only (0/64).
- Mix: executor 3, scout 16, reviewer 16, scribe 11, critic 10, connector 4, sentinel 4, revenger 0.
- Round 15 ran one wave; verifier routed this as debt.

**Scope accounting (this seat):** read skill://godspeed, RULES.md, round prompt, round-15 docs, wave artifacts, policy heads (v2 is mode 0600; read as config only), validator by grep. Read-only git; python3 as JSON parser. No scripts, tests, host probes, pacman, spawns, or writes beyond this report. Tools installed: none.

**Prevent (round-15 deviations):** extra ownership/log reads, isolated matcher runs, py_compile, pacman -S/-Sy/-Syu/-U/-R, service restarts.

**Limits:** does not assert wave 1 completed or wave 2 ran.
