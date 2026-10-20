# ReviewExitMap: round-16 verdict, count and registry review

Static reads only. Nothing executed; no installs; no host probes.

1. **HIGH:** `SKILL.md:1857` declares `section-citations` (0/1/2, `--selftest`) and pins `.ufo/waves/round-16/build/frozen-cases.json`. Neither that file nor `tools/check-section-citations.py` exists, so no exit or count is observable yet.
2. **HIGH:** SCORECARD measures `correction_count 0→2`, but no registry row defines it. R14 precedent pins FAIL with count 2 (`tools/check-source-scope-correction.py:467-469`). R16 should emit count only at exit 0 and pin count in selftest.
3. **MEDIUM:** exit 2 means BLOCKED and usage error in the census (`tools/tsukuroi-census.sh:2622-2628`), but could-not-evaluate in gates. Census `--selftest` failure is exit 1, the DEGRADED code. `tools/measure-update-recheck.py` exit 0 covers both ABSENT and COUNTED. Read verdicts from output, not exit alone.
4. **LOW:** R13 prints text with a binary count; R14 and R15 print JSON with revision and count. No registry row pins either format.
5. **Consistent:** `swarm-registry.json`, `dispatch.json` (spawn, tasks, members) and `spec.json` items all total 64, with matching names. ReviewExitMap has `item: null`; its report path appears only in dispatch text (`spec.json:145` omits it).

Residual risk: by static reading, an R15 FAIL cannot reach count 2 [INFERENCE]; no selftest pins this. Verification gaps: no gate or selftest output observed.
