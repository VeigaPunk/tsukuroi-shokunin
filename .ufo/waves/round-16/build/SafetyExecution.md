# SafetyExecution — seat-instruction contradictions (static)

1. **HIGH, child spawn.** The CitationGate, CitationEntry and FrozenCases trailers (`dispatch.json` taskCall.tasks[0–2]) say "no subagent dispatch except your single labrat". The context says "Every seat is a leaf, no child spawning". The global card `~/.omp/agent/agents/executor.md:5` sets `spawns: labrat`, and `labrat.md:11` describes it as "running the probe". No wave file names a probeParent. This is the same defect as `corpus/lessons/round-15.md:89-90`. `spawn-result.json` reports projectAgentsDir:null, so the leaf card `shokunin/.omp/agents/executor.md` may not be bound [INFERENCE].
2. **HIGH, test execution.** `executor.md:20` says "Run the narrow behavioral check covering the change." This contradicts "Gate author … NEVER runs them" and CitationGate's "No executions".
3. **MED, packages.** Every delivered task has an operator Tooling directive appended: 128 hits in `spawn-result.json`, 0 in `dispatch.json`. It permits `sudo pacman -S … --noconfirm` "without asking", but the context says pacman is PAUSED.
4. **LOW, wording.** `sentinel.md:14-15` asks for verification "using the canonical run logic". `reviewer.md:12` asks for "diagnostics checks", which reads like linting.
5. **LOW, messaging.** "Send choices to CitationGate" conflicts with "message TsukuroiR16 only".

**Fix:** L1 sends the three executors a direct "no child, no run" message, as was done in R15. Remove the labrat suffix.

**Limits:** I read the wave files and agent cards. I did not read any seat transcripts, executed nothing and installed nothing.
