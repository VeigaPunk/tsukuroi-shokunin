VERDICT: supports

Item C1-4 — mutation test of `probe_storage_arm` at 52ffd65f868431f021b8615ab281efd87195eac6
(seat C1MutUuid). Both assigned mutants KILLED; no coverage gap found.

# Method

- Target bytes: `tools/tsukuroi-census.sh` at 52ffd65, `probe_storage_arm()` (blob lines 1848–1887),
  pristine blob sha256 `8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c`
  (`git -C <clone> show 52ffd65:tools/tsukuroi-census.sh | sha256sum` → receipt `logs/pristine-hash.txt`).
- Detector battery, identical for every state (pristine / mutant A / mutant B / restored):
  1. `bash tools/tsukuroi-census.sh --selftest` (111 cases; exit 0 = pass),
  2. frozen counter `python3 tools/score-storage-arm-r38.py --repo <clone> --revision <sha>`
     (10 fixtures + live leg; predicate fixtures_matched==10 ∧ live_match==1 ∧ six_planes_all==1).
- Counter identity: sha256(tools/score-storage-arm-r38.py) = `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`
  — matches the declared frozen counter (sha256sum run 2026-10-26).
- Environment: scratch clone `/fast/scratch/hyaku/tsukuroi-r38/C1MutUuid/clone/lane`
  (`git clone -q --shared` of the lane; `rev-parse --show-toplevel` verified equal to the clone path;
  `remote remove origin`; throwaway identity `mut-c1uuid@fixture.invalid`; `checkout -q -B master 52ffd65`).
  TMPDIR pointed at the seat scratch. The lane itself was never written to (only my seat report/receipts);
  no host mutation, no pacman, no sudo, no tool installs (none needed: bash/python3/git already present).
- Observed on every counter leg, pristine included: the census child exits 2 (BLOCKED verdict on this
  host's live planes); identical across all four legs, and the counter keys on the STORAGE line grammar,
  not the exit code — pristine counter still PASSes (receipt `logs/pristine-counter.json`).

# Baseline (pristine 52ffd65) — detector green

- Selftest: exit 0, `TSUKUROI_CENSUS_SELFTEST: PASS (111 cases, 111 passed, 0 failed)` (`logs/pristine-selftest.out`).
- Counter: exit 0, `fixtures_matched: 10, live_match: 1, six_planes_all: 1, result: PASS` (`logs/pristine-counter.json`).
- Live `/sys/fs/btrfs` inventory (read-only ls): `1d02a454-c549-4a35-b567-89d60902af8e`, `features`.

# Mutant A — UUID-name filter dropped: KILLED

- Mutation: delete blob line 1855 `[[ ${fsd##*/} =~ $uuid ]] || continue` (the only application of the
  fsid regex bound at :1850), so every entry under the sysfs root counts as a filesystem.
  Diff: receipt `diff-mutA.patch` (one line removed, nothing else).
- Mutant commit `fc9618159eed9ab5a244bb177a9603f785a2d4aa`, blob sha256
  `c3dffe9def0d682dc3c783c83168bc19c99d6e08aebaaf1dee4419eceae7c0d1` (`logs/mutA-uuid-filter-dropped-hash.txt`).
- Selftest: exit 1, `TSUKUROI_CENSUS_SELFTEST: FAIL (111 cases, 110 passed, 1 failed)`. Deciding case:
  **storage-zero** — "healthy: five zero counters on one device; features and non-fsid names ignored
  (R38-C1)" (selftest case at blob :2896). stderr (`logs/mutA-uuid-filter-dropped-selftest.err`):
  `FAIL healthy: five zero counters on one device; features and non-fsid names ignored (R38-C1): plane
  evidence missing: '^STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0$'`.
- Direct reproduction of that fixture against the mutant blob (`TSUKUROI_BTRFS_SYSFS` override):
  `STORAGE btrfs-device-stats state=BLOCKED filesystems=3 devices=1 nonzero=0 detail=features:-:no-devinfo,not-a-uu:-:no-devinfo`
  — the `features` dir and `not-a-uuid` file are counted as filesystems and trip the (still-present)
  no-devinfo rule.
- Counter: exit 1, `fixtures_matched: 9, live_match: 0, six_planes_all: 1, result: FAIL`
  (`logs/mutA-uuid-filter-dropped-counter.json`). Deciding fixture **F08-zero-with-noise**
  (counter :84–86): expected `[HEALTHY,1,1,0]`, got `[BLOCKED,3,1,0]` with exactly the line above.
  The live leg flips independently: expected `[HEALTHY,1,1,0]`, got `[BLOCKED,2,1,0]`
  `detail=features:-:no-devinfo` (the real root's `features` entry counted).

# Mutant B — `nd -eq 0` no-devinfo BLOCKED rule dropped: KILLED

- Mutation: delete blob line 1879 `if [ "$nd" -eq 0 ]; then blocked=1; detail+="$fs8:-:no-devinfo,"; fi`.
  Diff: receipt `diff-mutB.patch` (one line removed, nothing else).
- Mutant commit `46a282c4ab12122538d22bc0abd67f34afd73ca9`, blob sha256
  `d6649d3a7a8f0f48859272d790d7587504e95e2ead97241099c58bb53d85ae4b` (`logs/mutB-nodevinfo-rule-dropped-hash.txt`).
- Selftest: exit 1, `TSUKUROI_CENSUS_SELFTEST: FAIL (111 cases, 110 passed, 1 failed)`. Deciding case:
  **storage-no-devinfo** — "healthy rollup: a mounted filesystem with no readable devinfo is BLOCKED
  (R38-C1)" (selftest case at blob :2921). stderr (`logs/mutB-nodevinfo-rule-dropped-selftest.err`):
  wanted regex `^STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=0 nonzero=0 detail=11111111:-:no-devinfo$`
  not matched.
- Direct reproduction against the mutant blob on the same tree shape:
  `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=0 nonzero=0` — a mounted fs with no
  devinfo reads as silent HEALTHY.
- Counter: exit 1, `fixtures_matched: 9, live_match: 1, six_planes_all: 1, result: FAIL`
  (`logs/mutB-nodevinfo-rule-dropped-counter.json`). Deciding fixture **F07-fs-without-devinfo**
  (counter :83): expected `[BLOCKED,1,0,0]`, got `[HEALTHY,1,0,0]`.

# Restoration evidence

- After each mutant leg: `git -C <clone> checkout -q -B master 52ffd65…`; restored master blob sha256 =
  `8e0084f6…` = pristine; worktree sha256 identical; `git status --porcelain` = 0 entries. Script printed
  `RESTORE-VERIFIED bytes identical to pristine 52ffd65 blob` after both legs.
- Detector re-run on restored bytes: selftest exit 0 PASS 111/111; counter exit 0 PASS
  (fixtures 10/10, live_match 1, six_planes 1) (`logs/restored-selftest.out`, `logs/restored-counter.json`).

# Findings

- Mutant A: KILLED — deciding fixture F08-zero-with-noise (counter) and selftest case storage-zero;
  live leg fails independently on this host (`features` present in the real root).
- Mutant B: KILLED — deciding fixture F07-fs-without-devinfo (counter) and selftest case
  storage-no-devinfo. Note: the counter's live leg alone would NOT kill mutant B (live_match=1 under
  the mutant — this host's mounted fs has readable devinfo); F07 is the discriminator. Mutant A is
  killed twice over (F08 + live).
- The C1 predicate is falsified by each mutant (fixtures_matched 9/10), so the frozen counter plus the
  selftest discriminate the claimed implementation from both plausible defects. Coverage finding: none;
  the two probes are covered.
- Not done (honest scope): only the two assigned mutation points were probed; no other mutant classes
  (e.g. key-set or state-priority mutations) were tested; C2 untouched; no lane file edited; no tool
  installed (nothing needed).

Receipts: `.ufo/waves/round-38/w1/C1MutUuid/` — `logs/` (selftest out/err + counter JSON per leg),
`diff-mutA.patch`, `diff-mutB.patch`, mutant blobs `mutA-census.sh`/`mutB-census.sh`, hash files,
`phase1.sh`, `phase-mut.sh`. Scratch `/fast/scratch/hyaku/tsukuroi-r38/C1MutUuid/` removed after archiving.
