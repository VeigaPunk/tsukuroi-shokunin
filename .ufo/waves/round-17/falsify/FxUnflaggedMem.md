# FxUnflaggedMem — attacks C2 completeness wording

**Verdict: SURVIVES.** No landed wording asserts total coverage; every count is six- or registry-scoped: `corpus/README.md:154` "Six older entries carry appended `R17-FRESHNESS` notices (…48 records)"; `LOG.md:937` "six entries with appended notices"; `SCORECARD.md:505` quantifies only over "statements carrying a dated R17 notice" (unlike `SCORECARD.md:479` "not total historical correction records", no explicit guard, but no widened domain); `boot-chain-r17.md:158` item 10; `measure/c2-after.json` scope "dated freshness re-verification only".

**Un-noticed [obs]**: both files byte-identical 6923fe0→dd15c183; `git show dd15c183:<f>|grep -c 'R17\|2026-10-20'` → 0. Affirmatively false: `oom-event-plane.md:51,280,346` ("`earlyoom` not installed/absent/not-found"), `:349,384` ("`zswap.enabled=0`"); `kill-event-deep-r8.md:256` (earlyoom absent), `:259` (zswap off), `:265` ("no `sar`/`atop`/`dool`/`dstat`"). Grounds: `fresh-capture.txt:28` earlyoom-1.9.0-1, `:47-51` enabled; `boot-chain-capture.txt:12` `zswap.enabled=1 zswap.max_pool_percent=25`; `:59` sysstat in the 09:15:30 `-Syu`. Expired [unk]: oom 305,345,347,348,350,351; kill 255,257,258,260-264,266.

**Mitigating [obs]**: those cells are captioned measurements (`oom:339-340`, `kill:251-253`) under `recheck: 30d` from 2026-10-14 (`oom:438`, `kill:346`) — the dated-capture rule excludes them from C2's universe except the operator-facing action rows.

**Defect**: `lessons/round-17.md:11` "47 R17 freshness records" vs 48 (`c2-after.json` record_count); gap disclosed only at `build/ConnPlannerWalk.md:18`.

Unverified: earlyoom `is-active`, `/var/log/sa`, live oomd/guard/zswap state.

Scope: executed=none
