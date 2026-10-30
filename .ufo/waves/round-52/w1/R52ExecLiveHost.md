VERDICT: no-finding

# Round-52 live host evidence

## Census

Executed in order as assigned from `/fast/scratch/hyaku/tsukuroi-r52/R52ExecLiveHost`:

- `bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh` — emitted timestamp `2026-10-30T05:35:52Z`, host `plazir27`; exit **1**. Rollup: `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)`. Full captured stdout and `EXIT_CODE=1` retained in the census command output for this seat (tool artifact `20558`; raw full output was read). Per-plane results: packages DEGRADED (`pacman -Qkk rc=1`, sample 8; foreign 23, of which new 7 and drift 13); systemd HEALTHY (user scope running, failed 0); drivers DEGRADED (kernel errors 135; memory subplane degraded); journal DEGRADED (5 boots, current graphical target active, 369 errors, failed-history indicator 1); update-safety DEGRADED (`UNKNOWN-UPSTREAM`, pending none, sync DB timestamp 8 days); OOM DEGRADED (5-boot window, 153 clusters). Additional emitted lines: DRIFT pacnew 3; STORAGE healthy, one filesystem/device and zero nonzero counters; SCRUB none, directory absent. These are reported observations, not repair authorization.
- `bash .../tools/tsukuroi-census.sh --identity` — `TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=aeda2cbcdcc4b08b09fefcddc237da7c0d8ee903aaf063a1578452081e0245dc md5=cdfe4ade5d732422f73472abdb7bc190 bytes=222197 lines=3824 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes`; exit **0**.
- `bash .../tools/boot-chain-audit.sh --selftest` — `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=49 failed=0`; exit **0**.
- `systemctl --user is-system-running` — `running`; exit **0**.
- `systemctl --user --failed --no-legend | wc -l` — `0`; pipeline exit **0**.
- `pacman -Qk 2>/dev/null | tail -1` — `zydis: 477 total files, 0 missing files`; pipeline exit **0**.
- `df -h / /boot /fast | tail -3` — `/`: 930G total, 360G used, 534G available, 41%; `/boot`: 2.0G total, 1.4G used, 687M available, 67%; `/fast`: 804G total, 448G used, 356G available, 56%; pipeline exit **0**.

The first census row was long and the tool's initial display abbreviated it; the complete output is available at the cited artifact. No output files were written outside the allowed report path and scratch.

## Round-start comparison limitation

There is no census capture in `.ufo/waves/round-52/before/` (as stated in the assignment). The round-50 SCORECARD text describes the census selftest as PASS with 168/168 and the identity mode as landed (`tsukuroi-shokunin/SCORECARD.md:3257`); it does not provide a round-50 live per-plane census snapshot. Its round-50 measured-outcome rows describe the census selftest/matcher, not live plane statuses (`SCORECARD.md:3240-3249`). Therefore these results establish the current plane states but cannot establish which plane changed since the round-start description; no plane-change claim is made.

## Scope

All listed commands were read-only. No install, mutation, or host recovery action was performed. Scratch `/fast/scratch/hyaku/tsukuroi-r52/R52ExecLiveHost` was removed before completion. No checks beyond those assigned were run.