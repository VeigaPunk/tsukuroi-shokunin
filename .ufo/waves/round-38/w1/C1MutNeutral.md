VERDICT: supports

Seat C1MutNeutral (L2, tsukuroi lane, round 38 wave 1). Item C1-5: mutation test of the
round-38 C1 storage-integrity arm's verdict-neutrality invariant — two plausible defects,
each run against the census `--selftest`, the frozen C1 counter
`tools/score-storage-arm-r38.py` (six_planes_all conjunct), the amendment's q82 counter,
and the frozen consumer `tools/score-census-handoff-r32.py`. Both mutants are killed by
the C1 harness pair (selftest + counters); the kill sets are disjoint, and the frozen
r32 consumer would have been broken loudly by the extra-plane mutant while being blind
to the rollup-fold mutant on this host. No silent survival anywhere in the C1 gate.

# 0. Target bytes and pristine baseline

- Target: `tools/tsukuroi-census.sh` as frozen at the C1 implementation commit
  `52ffd65f868431f021b8615ab281efd87195eac6`. Byte-identity verified:
  `sha256sum` of the scratch clone's working tree == `git show 5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf:tools/tsukuroi-census.sh | sha256sum` == `git show 52ffd65f…:tools/tsukuroi-census.sh | sha256sum`
  == `8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c` (167654 bytes;
  receipt `hashes.txt`). `git diff --stat 52ffd65… HEAD -- tools/tsukuroi-census.sh
  tools/score-storage-arm-r38.py` is empty (run 2026-10-26), so HEAD carries the exact
  frozen C1 bytes.
- Pristine census `--selftest`: `TMPDIR=<scratch> bash tools/tsukuroi-census.sh --selftest`
  -> rc=0, final line `TSUKUROI_CENSUS_SELFTEST: PASS (111 cases, 111 passed, 0 failed)`
  (receipt `selftest-pristine.txt`).
- Pristine frozen C1 counter (live leg included):
  `python3 tools/score-storage-arm-r38.py --repo <clone> --revision 5edb6c2…` -> rc=0,
  `result=PASS`, `fixtures_matched=10/10`, `live_match=1`, `six_planes_all=1`; live
  `storage_lines=["STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0"]`,
  live `census_exit=2` (receipt `counter-pristine.json`).
- Pristine frozen consumer r32: `python3 tools/score-census-handoff-r32.py --lane <clone>
  --revision 5edb6c2… --seed 3838 --scenarios 12` -> rc=0, `routed=12/12`,
  `live_consistent=true`, `harness_errors=0`, runtime 16.1s (receipt `r32-pristine.jsonl`).
  The consumer is green on the current census, so every mutant result below is
  attributable to the mutant, not to a pre-existing break.
- Live host storage surface (read-only `ls`/`cat`, 2026-10-26): `/sys/fs/btrfs` holds one
  fsid dir `1d02a454-c549-4a35-b567-89d60902af8e` plus `features`;
  `devinfo/1/error_stats` reads all five counters as `0` -> live storage state HEALTHY,
  filesystems=1 devices=1 nonzero=0 (matches the counter's live leg above). The live
  six-plane rollup was DEGRADED-or-worse in every observed run (census_exit=2 in the
  counter's live leg; `TSUKUROI_CENSUS: DEGRADED`, rc=1 in the m2 sample run of §2).

# 1. Method

- Scratch: `/fast/scratch/hyaku/tsukuroi-r38/C1MutNeutral/` (`mkdir -p`; `TMPDIR` exported
  there in every run, so the selftest's `${TMPDIR:-/tmp}` fixture tree landed in scratch,
  never in `/tmp`). Lane clone for counters:
  `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin <scratch>/clone`,
  then `git -C <clone> remote remove origin` (so `_revision.bind`'s pushed check is
  skipped — `tools/_revision.py:186-191` checks `refs/remotes/origin/<branch>` only when
  it exists), `git -C <clone> config user.name 'C1MutNeutral-scratch'`,
  `user.email 'c1mutneutral@scratch.invalid'`, `commit.gpgsign false`;
  `git -C <clone> rev-parse --show-toplevel` == the clone dir; `status --porcelain` empty.
- Each mutant was written into the clone's working tree with a two-context edit, captured
  as a diff receipt, committed on the clone's `master` (scratch only — the lane repo was
  never written; the only lane git calls were read-only rev-parse/log/diff/show), then
  measured: `bash <clone>/tools/tsukuroi-census.sh --selftest` (working-tree bytes) and
  `python3 tools/score-storage-arm-r38.py --repo <clone> --revision <mutant-sha>`
  (committed bytes via `git show`, per the counter's own contract,
  `tools/score-storage-arm-r38.py:9-10`). After each mutant round the working tree was
  restored from a saved pristine copy and sha256-verified (§4).
- No tools were installed or upgraded (python3/git/bash sufficed); no pacman transaction,
  no sudo, no host mutation of any kind; every census run was read-only by construction.

# 2. Mutant m1 — storage state folded into the rollup

Mutant (2 inserted lines; full diff receipt `mutant-m1-vs-pristine.diff`; commit
`592503cd44b55c10a5b14fbe21081e69d9dd78cf` in the scratch clone; census blob sha256
`df45c694d10d42578d5250e6249cffbe6d8b0a236f3daf505def549b0b0fcec9`):

```diff
--- a/tools/tsukuroi-census.sh
+++ b/tools/tsukuroi-census.sh
   printf '%s\n' "$STORAGE_LINE"
+  local st=${STORAGE_LINE#*state=}; st=${st%% *}
 
   local roll=HEALTHY
   ...
   roll=$(worse "$roll" "$OOM_V")
+  roll=$(worse "$roll" "$st")
```

i.e. the rollup becomes `worse(…, storage state)` (`worse` at
`tools/tsukuroi-census.sh:581-583`; pristine rollup chain at `:3010-3016`, storage print
at `:3006-3008`).

- census `--selftest`: **KILLED**. rc=1, final line
  `TSUKUROI_CENSUS_SELFTEST: FAIL (111 cases, 107 passed, 4 failed)` (receipt
  `selftest-m1.txt`). The four failing cases are exactly the four R38-C1 cases with
  planted non-HEALTHY storage (`tools/tsukuroi-census.sh:2899,2906,2913,2919`); the two
  HEALTHY-storage cases (`:2889,2893`) still pass. First failure verbatim:
  `FAIL healthy rollup: nonzero lifetime counters read DEGRADED on the STORAGE line only; 010 is ten, not octal (R38-C1): exit 1 wanted 0; output: STORAGE btrfs-device-stats state=DEGRADED filesystems=2 devices=2 nonzero=3 detail=…|TSUKUROI_CENSUS: DEGRADED (packages=HEALTHY systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)`
  — the rollup verdict and exit code flip while all six plane verdicts stay HEALTHY;
  the other three failures (malformed, duplicate, no-devinfo) flip exit 0->2 and
  HEALTHY->BLOCKED the same way. `check()` asserts the exit code and the
  `^TSUKUROI_CENSUS: <verdict> (` regex (`tools/tsukuroi-census.sh:2091-2143`), so both
  assertions fire.
- frozen C1 counter: **SURVIVES**. rc=0, `result=PASS`, `fixtures_matched=10/10`,
  `live_match=1`, `six_planes_all=1` (receipt `counter-m1.json`, revision bound
  `592503cd…`). Why: the six_planes_all conjunct only counts lines —
  `len(planes) == 6 and len(rollups) == 1` (`tools/score-storage-arm-r38.py:164-173`) —
  and never compares rollup TEXT; m1 changes neither count, and the STORAGE fields it
  matches are untouched. On this host even the recorded per-fixture `census_exit` stays 2
  (the live six-plane rollup is already BLOCKED, and `worse(BLOCKED, DEGRADED)=BLOCKED`).
- q82 counter (part of the C1 gate per the pre-seat amendment): **SURVIVES**. rc=0,
  `result=PASS`, `ns_views_matched=3/3`, `ns_available=1` (receipt `q82-m1.json`). Same
  reason: per-view `ok = got == exp and six`
  (`tools/score-storage-arm-r38-q82.py:122-125`) — STORAGE fields and plane counts
  unchanged inside the namespace views.
- frozen consumer r32: **SURVIVES on this host**. rc=0, `routed=12/12`,
  `live_consistent=true`, `harness_errors=0` (receipt `r32-m1.jsonl`). Why: (a) r32's
  fixture env sets no `TSUKUROI_BTRFS_SYSFS`
  (`tools/score-census-handoff-r32.py:454-485`), so its fixture runs read the live
  `/sys/fs/btrfs`, which is HEALTHY here (§0) — rev rollup == base rollup on every
  fixture; (b) live parity compares the rollup text (`r32:754`), but the live six-plane
  rollup was DEGRADED-or-worse in every observed run, so `worse(roll, HEALTHY)` is a
  no-op. m1 becomes observable to r32 only on a host where the storage state ranks above
  the six-plane rollup (then the fixture leg's full parity, `r32:978-980`, would catch
  it). Side observation: r32's fixture legs are not hermetic w.r.t. the round-38 arm —
  they read the live sysfs because the harness predates that seam; read-only, and
  parity-neutral here, but worth knowing when reading r32 receipts.

# 3. Mutant m2 — STORAGE line re-emitted as a seventh `PLANE storage:` line

Mutant (1 inserted line; full diff receipt `mutant-m2-vs-pristine.diff`; commit
`59f24059c33afc53e5fac34ebf139045a4b9d3f0` in the scratch clone; census blob sha256
`ec9ee94efb085aec60861bfe294d33dbaf90c2ebbacf6ec98e3f496df05afe5c`):

```diff
   printf '%s\n' "$STORAGE_LINE"
+  printf 'PLANE storage: %s\n' "${STORAGE_LINE#STORAGE }"
```

- Direct output sample (m2 census extracted via `git show 59f2405…:tools/tsukuroi-census.sh`,
  run with `TSUKUROI_BTRFS_SYSFS=<nonexistent>`): 7 `PLANE `-prefixed lines
  (`grep -c '^PLANE '` = 7), including literally
  `PLANE storage: btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0`
  between the STORAGE line and `TSUKUROI_CENSUS: DEGRADED (…)`; rc=1 (receipt
  `m2-output-sample.txt`).
- census `--selftest`: **SURVIVES**. rc=0, final line
  `TSUKUROI_CENSUS_SELFTEST: PASS (111 cases, 111 passed, 0 failed)` (receipt
  `selftest-m2.txt`). Why: `check()` asserts exit code, hostname override, packages-plane
  root fields, the verdict regex and per-line must/must-not-match regexes
  (`tools/tsukuroi-census.sh:2091-2143`) — no case counts PLANE lines, and the extra
  line matches none of the `ABSENT:` (HANDOFF) must-not-match regexes.
- frozen C1 counter: **KILLED**. rc=1, `result=FAIL`, `fixtures_matched=10/10`,
  `live_match=1`, `six_planes_all=0` (receipt `counter-m2.json`, revision bound
  `59f2405…`); `six_planes=False` on every fixture and on the live leg (7 != 6). The
  STORAGE fields themselves still match — the kill comes solely from the six_planes_all
  conjunct (`tools/score-storage-arm-r38.py:27-28,164-173,230`).
- q82 counter: **KILLED**. rc=1, `result=FAIL`, `ns_views_matched=0/3`,
  `ns_available=1`, `six_planes=False` in all three namespace views (receipt
  `q82-m2.json`; per-view `ok = got == exp and six`, `q82:122-125`).
- frozen consumer r32: **CAUGHT — the consumer would have been broken, loudly**. rc=1,
  `routed=0/12`, `plane_parity=False` on all 12 scenarios, `harness_errors=0`
  (receipt `r32-m2.jsonl`). The fixture leg compares the FULL plane list
  (`r32:978-980`), so 7 != 6 unrouts every scenario and the run's predicate fails
  (exit 0 -> 1 per `r32:1044-1046`). Two precision points: (a) the base-six-planes
  harness check (`r32:759-761`) applies to the BASE census `58cc2e0b…` (pinned at
  `r32:70`), so this is a clean predicate failure, not a harness error; (b) the live leg
  alone is BLIND to m2: live parity keeps only the oom and journal PLANE lines
  (`r32:752-754`), and indeed `live_consistent=true` under m2 (observed). So the frozen
  consumer would have been broken by m2 — visibly, in its routing predicate — but only
  its fixture leg does the killing; a live-leg-only consumer would have passed it.

# 4. Kill matrix and restoration evidence

| Harness | m1 (rollup fold) | m2 (7th PLANE line) |
|---|---|---|
| census `--selftest` (111 cases) | KILLED (4 R38-C1 cases: exit + verdict) | survives (111/111 PASS) |
| frozen C1 counter `score-storage-arm-r38.py` | survives (PASS 10/10, live 1, six 1) | KILLED (`six_planes_all=0`) |
| q82 counter `score-storage-arm-r38-q82.py` | survives (PASS 3/3) | KILLED (0/3, six_planes=False per view) |
| frozen consumer `score-census-handoff-r32.py` | survives on this host (12/12 routed, live consistent) | caught by fixture leg (routed 0/12, plane_parity=False x12, exit 1); live leg blind |

- Restoration: after each mutant round the clone's working tree was overwritten from the
  saved pristine copy and sha256-verified — observed `restored worktree sha256 match:
  True 8e0084f6…` after m1 and after m2, and again in the final check
  (`hashes.txt`: worktree-after-final-restore == pristine, True). Mutant commits
  `592503cd…` / `59f2405…` exist only in the scratch clone (origin removed, scratch
  identity, never pushed); the lane's tracked files, index and jj state were never
  touched. Scratch dir removed as the final step (`rm -rf --` + `trap … EXIT`), after
  receipts were copied into this seat dir.
- Receipts in `.ufo/waves/round-38/w1/C1MutNeutral/`: `hashes.txt`,
  `selftest-{pristine,m1,m2}.txt`, `counter-{pristine,m1,m2}.json`,
  `q82-{m1,m2}.json`, `r32-{pristine,m1,m2}.jsonl`, `mutant-m1.diff`,
  `mutant-m1-vs-pristine.diff`, `mutant-m2.diff`, `mutant-m2-vs-pristine.diff`,
  `m2-output-sample.txt`.

# 5. Coverage findings (not contract changes)

- The kill sets are disjoint and complementary. The counters' `six_planes` conjunct
  (`score-storage-arm-r38.py:164-173`; reused by q82 at `q82:122-125`) is the only guard
  against plane-count mutations — the selftest never counts planes. The selftest's four
  planted non-HEALTHY storage cases (`tsukuroi-census.sh:2899-2922`) are the only guard
  against rollup folds — neither counter reads rollup text. Each harness alone passes one
  of the two mutants; the C1 gate as a whole (selftest + v1 counter + q82) kills both.
- r32's live leg is structurally blind to an added plane line (keep-filter
  `r32:752-754`) and to a rollup fold whenever the live rollup already ranks at/above
  the storage state; its fixture leg carries the plane-count kill. On this host neither
  mutant is live-detectable beyond the plane count (live storage HEALTHY; live rollup
  DEGRADED-or-worse in every observed run) — the m1 survival statements are
  host-conditional and stated as such.
- Other consumers: a grep of `tools/` for `PLANE ` (2026-10-26) finds only r32, the two
  round-38 counters (all run above) and the round-35 DRIFT scorers.
  `score-pacnew-arm-r35b.py` was NOT run: its stub-view judge compares residual output
  lines against a claim-base census pinned at `b40c01df…` (round-35 era,
  `score-pacnew-arm-r35b.py:59`) via `others()` (`:407-408`, `:432`); the round-38
  STORAGE line is new, so even the pristine census cannot pass that parity — a baseline
  failure would be inconclusive, not a kill.

# 6. What I did not do

- Did not run r32 at its default 24 scenarios (ran 12 with fixed seed 3838 across all
  three runs for comparability; parity behavior is per-scenario, so the kill/survive
  attribution does not depend on the count).
- Did not run `score-pacnew-arm-r35b.py` (baseline-incompatible with any round-38
  census; §5).
- Did not exercise a host whose storage state ranks above the six-plane rollup (this
  host cannot exhibit it: §0); the conditional statements in §2/§5 are code-read plus
  host-observed reasoning, not run there.
- Did not modify any tracked lane file, the lane's git/jj state, the fleet repo, any
  sibling lane, or shokuknow; no installs, no pacman, no sudo, no service or sysfs
  mutation.
