# CritCalibration — N-10 calibration (round-43 w2)

VERDICT: defect-found

Seat: CritCalibration (critic, w2). Item N-10: count mismatches between the lane's
self-assessment and observed repo state at `8acf0b022586a0f3164c77659fb96ba5f90949b6`
(SCORECARD round-43 declaration claims/before values/controls/sha256s; SHONEN.md boxes;
lesson round-43 counts). One mismatch found; everything else checked matched.

## Mismatch 1 — SCORECARD C1 row declares three R43-C1 selftest cases; repo has four

- Claim (`SCORECARD.md:2661`, C1 Surface cell): "plus three `R43-C1` selftest cases (45 → 48)".
- Observed at tip:
  - `tools/boot-chain-audit.sh:1232,1235,1237,1239` carry **four** `R43-C1-` `st_check`
    cases (`missing-start-point-none-newer`, `missing-start-point-deep-newer`,
    `all-present-deep-newer`, `missing-start-point-silent`).
  - `grep -c "st_check '" tools/boot-chain-audit.sh` per revision (git show):
    base `6951ead` → **45**; impl `717b716` → **48** (3 `R43-C1-`); tip `8acf0b` →
    **49** (4 `R43-C1-`).
  - Fresh counter run: `python3 tools/score-bootinputs-r43.py --revision 8acf0b… --lane <lane> --scratch <scratch>`
    → `{"correct": 16, "identity_ok": 1, "live_agree": 1, "selftest_pass": 1,
    "selftest_r43": 4, "selftest_line": "TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=49 failed=0",
    "verdict": "PASS"}`.
  - Wave-1 integration commit `9b974f2a` added the fourth case ("R43-C1 stderr selftest
    case (49)"), so the freeze-era row (accurate at `717b716`) was not updated.
- The frozen claim text used for dispatch states "four `R43-C1-*` selftest cases
  (selftest 45 → 49 at 8acf0b…)" — the SCORECARD row disagrees with both the repo and the
  authoritative claim text.
- Impact: committed declaration drift (stale count). Predicate and kill rule unaffected
  (`selftest_r43 >= 2` still true; kill rule is function-scoped).

## Everything else matched (no further mismatch)

### sha256s recomputed — all match declared values
| Artifact | Declared | Recomputed |
|---|---|---|
| tools/score-bootinputs-r43.py | 886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f | identical |
| tools/check-scrub-record-r43.py | b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854 | identical |
| .ufo/waves/round-42/frozen/src/scrub.c | 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801 | identical |
| .ufo/waves/round-43/frozen/src/ioctl.c | 7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01 | identical |
| .ufo/waves/round-43/frozen/hostcap/capture.txt | f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556 | identical |
| .ufo/waves/round-43/controls/run_controls_c1.py | 8eb691711eefda48c3e557c06ac4b156299e2829e2688a893b84ad7b4a131493 | identical |
| .ufo/waves/round-43/controls/run_controls_c2.py | 7564862737a027b5efa31e849fd73bc7b543ade1968744d401bb10e723f4184f | identical |
| .ufo/waves/round-43/controls/candidate-boot-chain-audit.sh | 3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74 | identical |
| .ufo/waves/round-43/frozen/hostcap/capture.sh (lesson) | 77ffeecb…a1a9 | 77ffeecb4955a36324efa45d8c07b03d7879ed232cf3cd4d20aea9cb36d2a1a9 |

### Claims (C1/C2)
- C1 base surface as declared: `git show 6951ead:tools/boot-chain-audit.sh` — `set -uo
  pipefail` at :139; `boot_inputs_newer` find pipeline at :480-487 (`find … -newermt
  "@$btime" -print -quit 2>/dev/null | grep -q .`). Helper `inputs_newer_than` exists at
  :463 (tip) and is used at :494; `boot_inputs_newer` at :477.
- Before values: `.ufo/waves/round-43/before/c1-before.jsonl` → `correct 8`,
  `selftest_line … total=45`, `selftest_r43 0`, `FAIL` ✓; `c2-before.jsonl` → `rows 0`,
  `FAIL` ✓.
- Implementation: `.ufo/waves/round-43/after/c1-after-717b716.jsonl` → `correct 16`,
  `total=48`, `selftest_r43 3`, `PASS` ✓.
- Tip: fresh C1 run (above) PASS `correct 16`, `total=49`, `selftest_r43 4` ✓.
- C2 at tip: `python3 tools/check-scrub-record-r43.py --revision 8acf0b…` →
  `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, pointer_ok 1,
  novelty_base_hits 0, verdicts_ok 0` (FAIL only on `verdicts_ok`, wave-2 results pending —
  exactly the claim "every conjunct but verdicts_ok holds") ✓.

### Controls
- `controls/battery-summary-c1.jsonl` / `-c2.jsonl`: both `should_fail_accepted 0,
  control_accepted 1`. C1: K0-K6,K10 FAIL, K8/K9 PASS, K7 recorded (exit 0, variant
  sha256 67b95da3…). C2: K0-K2,K4-K13 FAIL, K3 PASS. All match the declaration's control
  expectations ✓.

### SHONEN.md boxes
All cited ranges verified at tip (only 12-line file; 8 boxes):
- SKILL.md:38-50 "## Health-verdict decision table (per plane)" ✓; :90-141
  "## Update-safety checklist (read-only until the stop line)" ✓; :179-209 "## Sources" ✓;
  :522-532 "### Executor checklist (no-oral-context, self-contained)" ✓;
  :1717-1721 "The round-12 matrix pointer above is a historical entry rejected at outside
  closure" ✓; :2028-2036 "### Error patterns" (E1-E6) ✓; :1078-1102 "### The kill-event
  classes — two kill waves, two classes (S8-2)" ✓.
- PROVINCE.md:44-52 ADJ-01…07 table ✓; :75-83 Frontier limits ✓; :85-90 round-12
  refinement (historical as claimed) ✓; :92-106 round-13 correction + round-14 erratum ✓;
  :121-146 round-19 ownership anchors (OUT-001…OUT-010 with pinned digests) ✓;
  :148-152 R20 OUT-009 clarification ✓.
- Referenced files all exist: package-state-plane.md, systemd-user-plane.md,
  driver-firmware-plane.md, aur-risk-plane.md, host-health-report-r3.md,
  adjacency-anchors-r19.md, adjacency-recheck-2026-10-19.md, kill-oom-boundary-r33.md,
  .ufo/waves/round-33/a3res/JudgeC2Exploratory.md ✓.
- adjacency-handoffs-fleet-r1.md:136 = "## 4. Counting contract records" ✓ (section 3 holds
  TSUKUROI-F1-MEM-01 at :74 ✓). executor-test-sufficiency.md:15-20, :106-136 hold the
  revision table and per-step sufficiency ✓. LOG.md has 90 round-3 mentions ✓.

### Lesson counts
- "w1 (build + first falsifiers, 44 seats)": `w1-results.json` `"seats": 44`, `len(results)
  == 44` ✓.
- "w2 … six counted C2 row verdicts": `w2-dispatch.json` registry members whose axes include
  `counted` = exactly `{C2RevSR1, C2RevSR3, C2RevSR6, C2CritSR1, C2CritSR3, C2CritSR6}`
  (6) ✓.
- Rows: `btrfs-scrub-record-r43.md` has `## SR1`, `## SR3`, `## SR6` sections (counter
  `rows 3`) ✓.
- Entry-gate source lines spot-checked against frozen snapshots: `scrub_write_progress(`
  at scrub.c:1123/:1503/:1702; :483 `fd = open(datafile, m, 0600);`; :922-927 `err` /
  `goto out1` before and after rename; :806-818 thirteen `_SCRUB_SUM` macros + :819
  `_SCRUB_COPY(dest, data, last_physical);`; :1427 `last_dev_scrub`; :1946
  `in_progress = is_scrub_running_in_kernel(`; :1336/:1507 `warning(…status recording
  disabled)`; ioctl.c:3072/:3120/:3132-3133 `if (!capable(CAP_SYS_ADMIN))` /
  `return -EPERM;`; handlers open :3066/:3118/:3126; dispatch :5582 ✓.

## Not checked / pending
- "Round 43 — measured outcome" SCORECARD section does not exist at tip (round open); the
  lesson references it prospectively — not a mismatch.
- No round-43 capabilities table exists yet, so the R43-CAP-HEADER-DUP able-to-fail target
  ("round 43 must print 1") is not yet observable; the round-42 table still double-headers at
  SCORECARD.md:2630/2632 (`awk …` prints 2), consistent with the mistake row's red state.
- Live re-fetch byte-identity of S237/S240/S241 not re-downloaded (accepted from wave-1
  receipts cited in the lesson); no git/network mutation performed.
- Non-author closure / spot-check pending; SHONEN non-author verification of SKILL.md is
  explicitly owed by the author (not verifiable here).

## Tooling
No tools installed or updated (no pacman/uv/npx actions). Scratch:
`/fast/scratch/hyaku/tsukuroi-r43/CritCalibration-2/` (created, used for the C1 counter
run and selftest, removed on exit).
