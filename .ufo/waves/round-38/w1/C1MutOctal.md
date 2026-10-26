VERDICT: supports

Seat C1MutOctal — Item C1-3: mutation probe of tools/tsukuroi-census.sh at 52ffd65f868431f021b8615ab281efd87195eac6.
Mutants: the zero test `[[ $v =~ ^0+$ ]]` replaced by (M1) `[ "$v" -gt 0 ]` and (M2) `(( v > 0 ))`, one line, census.sh:1872.
Harnesses run per mutant: the census's own `--selftest` and the frozen counter tools/score-storage-arm-r38.py
(sha256 e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218 — verified, §1), plus the pre-seat amendment's
q82 counter as a supplementary third harness. Result: BOTH MUTANTS KILLED BY EVERY HARNESS RUN; pristine baseline green;
bytes restored exactly. No surviving mutant, no coverage gap found for this mutation class.

## 1. Target and provenance
- Mutated line — tools/tsukuroi-census.sh:1872 (pinned bytes; the only `^0+$` occurrence in the file — grep over the
  clone at 52ffd65 matched exactly one line):
  `if ! [[ $v =~ ^0+$ ]]; then dnz=$((dnz + 1)); ddet+="$fs8:${dev##*/}:$k=$v,"; fi`
- Contract it implements — tools/tsukuroi-census.sh:359-361: "nonzero counts the (device, counter) pairs above zero …
  else DEGRADED when nonzero > 0"; the line is emitted at :1884-1885 as
  `STORAGE btrfs-device-stats state=… filesystems=… devices=… nonzero=…[ detail=…]`.
- Pinned revision: `git -C <lane> log --oneline -1 52ffd65…` →
  "52ffd65 round-38: C1 storage-integrity census arm (verdict-neutral STORAGE line, 6 selftest cases, TMPDIR-honouring selftest)".
- Scratch clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin …/C1MutOctal/clone`, then
  `git -C … checkout 52ffd65…`; `git -C … rev-parse --show-toplevel` == the clone dir; the clone's census sha256
  8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c equals the lane working-tree file (`diff -q` clean).
  Receipt: census-pristine.sh + receipts/pristine.sha.
- Counter bytes: the clone's tools/score-storage-arm-r38.py sha256 e649bfb3… matches the declared frozen sha. The q82
  counter was taken from the lane working tree (sha256 a183ff580cb9…, copied to receipts/score-storage-arm-r38-q82.py);
  both q82 runs reached view scoring with no `error` field, which means its internal v1-model digest pin
  (V1_FREEZE 7cbaeb6…, V1_SHA256 e649bfb3…, q82-counter.py:30-32, load_v1 digest check) passed.
- Counter binding: counters ran with `--repo <clone> --branch mut`. Branch `mut` was created at 52ffd65 inside the
  CLONE and `git remote remove origin` was run in the CLONE only — the wave context's prescribed remedy so unpushed
  mutant commits bind (tools/_revision.py:172-192: bind() requires the revision to be an ancestor of the local branch
  tip (:185 E-NOT-LANDED) and, when refs/remotes/origin/<branch> exists, of the origin tip (:190 E-NOT-PUSHED)).
  The lane repo was never written: only read-only `rev-parse`/`cat-file`/`log` were run against it.

## 2. Bash semantics the mutants rely on (observed)
Probe receipts: receipts/bash-semantics.txt and receipts/bash-octal-discriminator.txt (drivers probe.sh, probe2.sh;
/usr/bin/bash 5.3.20(1)-release; the harness temp shell's bash 5.2.37 agreed on every overlapping line of a partial
identical probe run before the file was overwritten by the 5.3.20 rerun):

- `[ "010" -gt 0 ]` → TRUE (status 0); `[ "010" -eq 10 ]` → TRUE; `[ "010" -eq 8 ]` → FALSE
  → bash's `[` builtin parses integers as DECIMAL: "010" is ten.
- `[[ 010 =~ ^0+$ ]]` → FALSE (status 1); `[[ 00 =~ ^0+$ ]]` → TRUE (status 0)
  → the original regex classifies "010" as nonzero and "00"/"000" as zero.
- `(( 010 > 0 ))` → TRUE; `(( 010 == 8 ))` → TRUE; `(( 010 == 10 ))` → FALSE; `v=010; (( v == 8 ))` → TRUE
  → bash arithmetic parses "010" as OCTAL 8, both as a literal and via a variable's value.
- `v=08; (( v > 0 ))` and `v=09; (( v > 0 ))` → "((: 08: value too great for base (error token is \"08\")", status 1
  → under M2's `if ! (( v > 0 ))`, an "08"/"09" value would be COUNTED as nonzero (status 1 inverted) with an
    arithmetic error on stderr. No harness case uses such a value (§7).

## 3. Pristine baseline (all green — the kills below are meaningful)
- `bash tools/tsukuroi-census.sh --selftest` (clone worktree == pinned bytes) →
  "TSUKUROI_CENSUS_SELFTEST: PASS (111 cases, 111 passed, 0 failed)", exit 0. Receipt: receipts/selftest-pristine.txt.
- Frozen v1 counter: `python3 tools/score-storage-arm-r38.py --repo <clone> --revision 52ffd65… --branch mut` →
  PASS, exit 0: fixtures_matched=10, live_match=1, six_planes_all=1. Receipt: receipts/counter-pristine.json.
- q82 counter: PASS, exit 0: ns_views_matched=3/3 (VIEWS=3), ns_available=1. Receipt: receipts/q82-pristine.json.

## 4. Mutant M1 — `[[ $v =~ ^0+$ ]]` → `[ "$v" -gt 0 ]` (census.sh:1872)
- Bytes: census sha256 f9b48f9f23283a2dd0ec3593804f1019da74454564db67214b2a981699856fce; worktree hash == committed
  hash (receipts/m1-worktree.sha == m1-committed.sha), so the selftest and the counter exercised identical bytes.
  Scratch-clone commit 3045f8c892e0c1e083552424015923966db62f87 (branch mut); one-line diff: receipts/m1.diff.
- `--selftest`: KILLED — "TSUKUROI_CENSUS_SELFTEST: FAIL (111 cases, 108 passed, 3 failed)", exit 1
  (receipts/selftest-m1.txt). Failing cases (selftest-m1.txt:106-108): storage-zero, storage-nonzero,
  storage-malformed — exactly the three cases whose fixtures reach the zero test with values on both sides.
  storage-absent (:105), storage-duplicate (:109) and storage-no-devinfo (:110) still pass: the blocked/absent paths
  never classify a value.
- Direct capture (the selftest's storage-nonzero fixture reproduced verbatim under TSUKUROI_BTRFS_SYSFS):
  mutant prints `STORAGE btrfs-device-stats state=DEGRADED filesystems=2 devices=2 nonzero=7
  detail=11111111:1:read_errs=0,11111111:1:flush_errs=0,11111111:1:generation_errs=0,aaaaaaaa:2:write_errs=0,
  aaaaaaaa:2:read_errs=0,aaaaaaaa:2:flush_errs=0,aaaaaaaa:2:corruption_errs=0`
  vs expected `…nonzero=3 detail=11111111:1:write_errs=1,11111111:1:corruption_errs=3,aaaaaaaa:2:generation_errs=010`
  (census.sh:2903). The mutant counts the seven ZERO pairs and drops the three nonzero values (1, 3, and 010 —
  which `[` reads as decimal ten, still > 0, hence excluded). Receipts: receipts/m1-storage-line.txt,
  m1-storage-nonzero-direct.txt.
- Frozen v1 counter: KILLED — FAIL, exit 1: fixtures_matched=5/10, live_match=0, six_planes_all=1
  (receipts/counter-m1.json). Mismatches: F01-zero-one-device (HEALTHY,1,1,0)→got (DEGRADED,1,1,5);
  F02-two-counters-nonzero (DEGRADED,1,1,2)→got (DEGRADED,1,1,3); F03-second-device-nonzero (DEGRADED,1,2,1)→got
  (DEGRADED,1,2,9); F08-zero-with-noise (HEALTHY,1,1,0)→got (DEGRADED,1,1,5); F09-second-fs-nonzero
  (DEGRADED,2,2,1)→got (DEGRADED,2,2,9). F04/F05/F06/F07/F10 still match (blocked/absent paths never reach the
  zero test). Live leg: this host's /sys/fs/btrfs is 1 fs (1d02a454), 1 device, all-zero counters → got
  (DEGRADED,1,1,5) vs expected (HEALTHY,1,1,0) → live_match=0.
- q82 counter (supplementary): KILLED — FAIL, exit 1: ns_views_matched=0/3, ns_available=1 (receipts/q82-m1.json):
  view0 zero-mode (HEALTHY,2,3,0)→got (DEGRADED,2,3,15); view1 nonzero-mode (DEGRADED,3,6,11)→got (DEGRADED,3,6,19);
  view2 any-mode (DEGRADED,3,7,17)→got (DEGRADED,3,7,18). stderr_tail empty in all views (values are plain decimals).
- Restoration: `git -C <clone> checkout 52ffd65… -- tools/tsukuroi-census.sh`; `cmp` against the saved pristine copy
  → RESTORED-OK, sha256 8e0084f6… (receipts/m1-restored.sha).

## 5. Mutant M2 — `[[ $v =~ ^0+$ ]]` → `(( v > 0 ))` (census.sh:1872)
- Bytes: census sha256 5558f660f327d17e4ed7585429b617893fd3a7a1300aa43bd82218da51d951cb; worktree hash == committed
  hash (receipts/m2-worktree.sha == m2-committed.sha). Scratch-clone commit 3c1b1a5257625af843500d1c7508c0a8a7727592
  (branch mut); one-line diff: receipts/m2.diff.
- `--selftest`: KILLED — "TSUKUROI_CENSUS_SELFTEST: FAIL (111 cases, 108 passed, 3 failed)", exit 1; the same three
  cases fail (receipts/selftest-m2.txt:106-108).
- Direct capture: the same wrong line as M1 — `…nonzero=7 detail=…` listing only zero pairs
  (receipts/m2-storage-line.txt). Mechanism: "010" enters `(( v > 0 ))` as OCTAL 8 (probe: `(( 010 == 8 ))` TRUE,
  `(( 010 == 10 ))` FALSE, `v=010; (( v == 8 ))` TRUE) → 8 > 0 → TRUE → the pair is excluded from nonzero; the seven
  zeros are counted instead; nonzero=7 ≠ 3 misses the pinned regex (census.sh:2903).
- Frozen v1 counter: KILLED — FAIL, exit 1: fixtures_matched=5/10, live_match=0, six_planes_all=1; the same fixture
  pattern as M1 (F01/F02/F03/F08/F09 mismatch, F04/F05/F06/F07/F10 match) (receipts/counter-m2.json).
- q82 counter: KILLED — FAIL, exit 1: ns_views_matched=0/3, ns_available=1 (receipts/q82-m2.json): view0 zero-mode
  (HEALTHY,3,4,0)→got (DEGRADED,3,4,20); view1 nonzero-mode (DEGRADED,3,4,7)→got (DEGRADED,3,4,13); view2 any-mode
  (DEGRADED,1,2,3)→got (DEGRADED,1,2,7).
- Restoration: RESTORED-OK, sha256 8e0084f6… (receipts/m2-restored.sha).

## 6. Kill matrix (the item's question: which harness kills each mutant, and why)

| harness | M1 `[ "$v" -gt 0 ]` | M2 `(( v > 0 ))` |
|---|---|---|
| census `--selftest` (111 cases) | KILLED — 3 storage cases fail, exit 1 | KILLED — 3 storage cases fail, exit 1 |
| frozen v1 counter (score-storage-arm-r38.py) | KILLED — 5/10 fixtures, live 0 → FAIL exit 1 | KILLED — 5/10 fixtures, live 0 → FAIL exit 1 |
| q82 counter (supplementary, amendment) | KILLED — 0/3 views → FAIL exit 1 | KILLED — 0/3 views → FAIL exit 1 |

Why:
1. Both mutants INVERT the zero-classification at census.sh:1872. The original counts pairs whose value is not
   spelled all-zeros (`! [[ $v =~ ^0+$ ]]`); the mutants count pairs whose value is not > 0 — the exact complement
   over the arm's validated non-negative-integer domain (validation is the digit regex at census.sh:1870, so only
   digit strings reach the zero test). Zeros become "nonzero" and nonzero values vanish from `nonzero=`. Every
   harness case holding either a zero or a nonzero counter sees it: selftest storage-zero/nonzero/malformed;
   counter F01/F02/F03/F08/F09 + the live leg; q82's three random views.
2. The selftest's storage-nonzero case is the designed trap for exactly this rewrite: "010 is ten, not octal
   (R38-C1)" (census.sh:2902) — it feeds generation_errs=010 and pins nonzero=3 AND the raw detail token
   `generation_errs=010` (census.sh:2903). M1's `[` reads "010" as decimal ten (10 > 0 → wrongly excluded); M2's
   `(( ))` reads it as octal eight (8 > 0 → wrongly excluded). Either arithmetic form fails the case; the regex
   original passes it. The counter's own oracle reads the same way (isdigit + int, decimal:
   tools/score-storage-arm-r38.py:139-142, nonzero = pairs > 0 at :146, line grammar at :54-56), which is why the
   counter's fixtures kill the mutants too.
3. M2 carries an extra latent behavior that NO harness case exercises: an "08"/"09" value makes `(( ))` raise
   "value too great for base" with status 1, so `if ! (( v > 0 ))` would count it as nonzero and print an arithmetic
   error to stderr (probe, §2). All harness values are plain decimals or "010", so this path is unobserved in every
   run above — a coverage edge of the harnesses, not a finding against the claim.

## 7. Observations and limits (what was NOT done)
- The counter's census child exits 2 (BLOCKED rollup) under the counter's minimal child env (PATH=/usr/bin:/bin, no
  user bus) in EVERY run — pristine included (receipts/counter-pristine.json: all 11 census_exit fields are 2 with
  match=true) — the predicate reads only the STORAGE line, the six PLANE lines and rollup presence, so this is not a
  mutation effect.
- No "08"/"09" value was pushed through the census itself: no fixture or selftest case exists, and creating one
  would mean editing lane files (forbidden). Only the bash semantics were probed directly (§2).
- The live leg was exercised only against this host's all-zero /sys/fs/btrfs (1 fs, 1 device); the nonzero direction
  of the live oracle is covered by fixtures F02/F03/F09 and q82's forced-nonzero view instead.
- No tool was installed or upgraded (no pacman, no uv, no npx; bash 5.3.20 / python3 / git / unshare all
  preexisting) — nothing to record under the 2026-10-19 tooling authorization.
- Lane untouched: no tracked lane file edited, created or deleted; no git add/commit/checkout/stash/reset and no jj
  command in the lane; no host mutation (no sudo, no package, no service, no sysfs write, no counter reset). All
  scratch (clone, fixture trees, TMPDIR) lived under /fast/scratch/hyaku/tsukuroi-r38/C1MutOctal/ and was removed
  after the receipts were copied (cleanup output: "scratch removed: YES"). The mutant commits (3045f8c8…, 3c1b1a52…)
  existed only in the scratch clone; their bytes and hashes are preserved as receipts.

## 8. Receipts index (all under .ufo/waves/round-38/w1/C1MutOctal/)
- Scripts and pinned bytes: census-pristine.sh (8e0084f6…), census-mutant-m1.sh (f9b48f9f…), census-mutant-m2.sh
  (5558f660…), m1.diff, m2.diff, probe.sh, probe2.sh, base.sh, m1.sh, m2.sh, cleanup.sh
- receipts/: pristine.sha, bash-semantics.txt, bash-octal-discriminator.txt, score-storage-arm-r38-q82.py
  (a183ff58…), selftest-pristine.txt, counter-pristine.json, q82-pristine.json, selftest-m1.txt,
  m1-storage-line.txt, m1-storage-nonzero-direct.txt, counter-m1.json, q82-m1.json, m1.sha, m1-worktree.sha,
  m1-committed.sha, m1-restored.sha, selftest-m2.txt, m2-storage-line.txt, m2-storage-nonzero-direct.txt,
  counter-m2.json, q82-m2.json, m2.sha, m2-worktree.sha, m2-committed.sha, m2-restored.sha
