# Round 38 — verifier spot-check (integrator, hyaku)

author: hyaku closure (non-author integrator, @m_opus)

Lane-round: tsukuroi round 38 (hyaku run 8, fresh-start round). Base `8bd001f58bfda29c92d90d2a7a413825c0ca9fcb`, after
`f8b4df2aac41e813dc652d82cf3ae0258e4db45a`. Report `.ufo/reports/round-38/tsukuroi.md` (fleet repo), prompt
`.ufo/prompts/tsukuroi-round-38.md`. Closure date 2026-10-26. This file is the only lane path the closure writes. No
lane-authored file was edited. I ran no sibling gate or counter; every "re-measured" line below is my own plain read
(git, sha256sum, jq, a small Python re-derivation, and curl of upstream sources).

Driver digest. Copied from the mutable `.ufo/watchdog.log`, lines 1467 and 1476:
`2026-10-26T01:05:49-03:00 launch tsukuroi round=38 pgid=26219 driver=hyaku-inline attempt=1`;
`2026-10-26T02:28:28-03:00 complete tsukuroi round=38; hyaku-inline attempt=1`.

## 1. Step-1 conformance (re-run results)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %H %cd' -- .ufo/reports/round-38/tsukuroi.md` | `tsukuroi-shokunin <tsukuroi@shokunin.local> 67d35b82886c0b9e8b1f12f1a6281e200328fd67`, committed 02:26:39 -03:00 | pass. Filed after the last cited lane commit `f8b4df2a` (02:25:39) and before the driver completion line (02:28:28) |
| SHONEN heading | read report `## SHONEN` | 4 lines, one per box, all `[~]` with evidence pointers | pass |
| Cited commits exist and are ancestors | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> master` for the 9 full round hashes, the base, and the short forms `7cbaeb63 9c9bb647 fc931bd b0005ae 8bd001f5 f8b4df2a` | all resolve; all ancestors of `master` | pass |
| Lane pushed and clean | `scripts/hyaku/jj-lane.sh state …/tsukuroi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=f8b4df2a… remote=f8b4df2a… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `f8b4df2a…` | pass |
| Round commits are lane-authored | `git log --format='%an' 8bd001f5..f8b4df2a` | 9 commits, all `tsukuroi-shokunin` | pass |
| Prompt carries template contract | every line of `kimi-shokunin/templates/round-prompt.md` (140 lines, 105 literal): literal lines matched verbatim, placeholder lines by fixed fragments | 0 missing. The one fragment miss is the rendered `Working dir:` line (placeholder `<{{LANE}}-repo>` rendered to the lane path). The hyaku addendum is §6 (`:141` ff.); §3 quotes no route map, so there is no MISSION bucket to compare | pass |
| Gate registry rows | `git show f8b4df2a:SKILL.md \| grep -n 'storage-arm-r38\|hook-order-r38'` | rows `storage-arm-r38`, `storage-arm-r38-q82`, `hook-order-r38` at `SKILL.md:3113-3115` | pass |
| Sources & frontier, Trend verdicts sections | read report | both present | pass |

Conformance notes (status-neutral):
- The pre-seat amendment `9c9bb647` was written after the author's own after-receipts (`after/c1-after-52ffd65.json`,
  `c2-after-1fe28e7.json`). The lane disclosed this. It only adds conjuncts and kill rules, and the v1 predicates are
  byte-frozen, so I accept it as a tightening. It cannot turn a fail into a pass.
- S210's anchor cell names `_alpm_trans_commit`, which does not exist at 54d9411. The function is `alpm_trans_commit`
  (`trans.c:167`, my fetch). The erratum is recorded only in the lesson prose. CORPUS.md rule 2 says a correction is a new
  row that opens `supersedes S210 —`. Routed (§6).
- The before receipts carry no `tool_sha256` (the lane's own R38-STREAK-ATTRIBUTION). I verified counter bytes separately
  (§2).

Status: real report with checkable work and pushed commits → **ok**.

## 2. Per-claim re-check (closure's own measurements at `f8b4df2a`)

`git diff --stat b0005ae9 f8b4df2a` touches only the 7 after-receipts, `LOG.md` and `SCORECARD.md`. So the measured
revision `b0005ae9` and the tip have identical census, counter, entry and capture bytes.

### C1 (coverage) — re-measured by plain reads plus evidence-verified receipts. VERIFIED.

Claim: btrfs per-device error counters move Frontier → Core through a verdict-neutral census arm.

| Conjunct / kill rule | Closure measurement | Observed |
|---|---|---|
| Frontier rule at base | `git show 8bd001f5:corpus/README.md` line 243 | "it becomes Core only after a read-only census arm reads it". Base census: `grep -c 'STORAGE\|error_stats'` = 0 |
| Counter bytes frozen | `git show <rev>:tools/score-storage-arm-r38.py \| sha256sum` at `7cbaeb63`, `9c9bb647`, `f8b4df2a` | `e649bfb3…` at all three; only `7cbaeb6` touches the file. Q82 counter `a183ff58…` at `9c9bb647` and tip; check-hook-order `60e3635b…` at all three |
| The arm is real, not fixture-gated (this closes the v1 and Q82 counter gaps by reading the code) | read `probe_storage_arm`, `tools/tsukuroi-census.sh:1855-1901` at tip; `:453` | Only one code path exists. `root=$BTRFS_SYSFS`, defaulting to `/sys/fs/btrfs` (`:453`). It globs `<root>/<uuid>/devinfo/<devid>/error_stats` and reads each file. There is no fixture-name branch, no cached value, and no mountinfo, `$HOME` or `$TMPDIR` read, so the four `Q82Attack` leak arms are counter defects, not properties of this arm. It is read-only (reads and globs only) |
| Verdict-neutral | `sed -n '3028,3045p'` of the census at tip | `printf '%s\n' "$STORAGE_LINE"` comes before the rollup, and `roll` folds only PKG/SYS/DRV/JRN/UPD/OOM. STORAGE never enters `TSUKUROI_CENSUS` |
| Live leg equals my own sysfs reading | `for e in /sys/fs/btrfs/*-*/devinfo/*; do cat $e/error_stats; done` (2026-10-26) | one fs `1d02a454…`, one dev `1`, all five counters 0 → expected `HEALTHY 1/1/0`. The committed `after/c1-final-b0005ae.json` live leg is `got ["HEALTHY",1,1,0]`, `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`. Match |
| v1 predicate (evidence-verified) | `jq` on `before/c1-before.json`, `after/c1-final-b0005ae.json` | before `fixtures_matched 0/10, live_match 0`, FAIL exit 1 at `8bd001f5`. After 10/10, live 1, six 1, PASS exit 0 at `b0005ae9`. Matches the report |
| Q82 conjunct (evidence-verified) | `jq` on `after/c1-q82-final-b0005ae.json` | `ns_views_matched 3`, `ns_available 1`, PASS exit 0, revision `b0005ae9`, seed recorded |
| Selftest no-harm kill rule (evidence-verified) | `cat after/selftest-final-b0005ae.txt` | `TSUKUROI_CENSUS_SELFTEST: PASS (113 cases, 113 passed, 0 failed)` |
| Province/README promotion | `git diff 8bd001f5 f8b4df2a -- PROVINCE.md corpus/README.md` | append-only (26+0, 19+0). Core is scoped to the five counters. Scrub and NVMe SMART stay Frontier. The absent-root limit is stated |

- No kill rule fires.
- The disclosed limits stay limits and do not falsify the after-state:
  - R38-ABSENT-ROOT: an absent root gives a false HEALTHY 0/0/0 inside a namespace that hides `/sys/fs/btrfs`. On this host the root exists.
  - R38-Q82-LEAK: the counter can be beaten by arms that read leaked paths. The real arm reads no such path (read above).
  - Both are routed (§6).
- Axis verdict: **coverage improved** (ordinal 9 → 9 by the lane's choice).

### C2 (depth, sourced S208–S212) — re-measured by independent re-derivation plus upstream re-open. VERIFIED.

| Conjunct / kill rule | Closure measurement | Observed |
|---|---|---|
| Capture integrity | sha256 of `git show f8b4df2a:.ufo/waves/round-38/frozen/hooks-capture/MANIFEST.sha256`; each of its 70 lines checked against the committed file bytes | `da07f434…` (equals the declared pin). 70 entries, 0 bad |
| Capture vs live host | sha256 of every `/usr/share/libalpm/hooks/*.hook` and `/etc/pacman.d/hooks/*.hook` vs the MANIFEST (2026-10-26) | 70 live files, 0 drift |
| 69 rows, order and every cell | my own Python: etc-first-wins override, `strncmp` over the name minus `.hook` with the shorter name first on a tie, triggerless skipped, per-phase position from `When=`, `AbortOnFail`/`NeedsTargets`/first `Exec` token; compared with the entry's `## Effective hook order` table | 69 effective of 70 files, 17 Pre / 52 Post, 0 masks, 0 AbortOnFail, 14 NeedsTargets. Set difference both ways ∅. Row order identical |
| HO1–HO7 against pinned source | `curl -fsSL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/{lib/libalpm/hook.c,doc/alpm-hooks.5.asciidoc,lib/libalpm/trans.c,lib/libalpm/alpm.c}` | sha256 `99f1044b…`, `2970cb35…`, `637c1165…`, `8bbb0a3c…`, equal to the S208–S211 anchors. HO1 `hook.c:443-455` (`/* exclude the suffixes from comparison */` :449, tie :452). HO2 reverse walk :540, `skipping overridden hook` :588-590, `alpm.c:62` list head. HO3 triggerless `return 0` :118-122. HO4 `abort_on_fail` plus Pre `break` :660-669. HO5 parse/validate failure sets `ret = -1` :609-614, and Pre `goto cleanup` :629-631 comes before any hook runs. That return turns into `RET_ERR(…ALPM_ERR_TRANS_HOOK_FAILED…)` at `trans.c:201-203`. HO6: an interrupted commit logs `transaction interrupted` (:230), and Post runs only in the `transaction completed` branch (:235), with the `_alpm_hook_run` result discarded (:238). HO7 triggered-subset filter :636-641 (`hook->when == when && _alpm_hook_triggered` :638). All hold |
| Kill rule: pacman.log run-order oracle | my own parser over `/var/log/pacman.log`: per transaction and phase, the `running '<hook>'` sequence must be increasing in the table's positions | 60 transactions with hooks, 109 phases, 0 violations, 0 names absent from the table. This matches the lane's `w1/C2ExecLogOracle.md` |
| Kill rule: cited quote absent | `grep -n` in the fetched files | S208 `return l1 < l2 ? -1 : 1;` hook.c:452. S209 `alphabetical order of their file name, where the ordering ignores the suffix.` asciidoc:39. S210 `if(!(trans->flags & ALPM_TRANS_FLAG_NOHOOKS) &&` trans.c:201 with `RET_ERR` :203. S211 `myhandle->hookdirs = alpm_list_add(NULL, hookdir);` alpm.c:62. All present |
| Counter receipts (evidence-verified) | `jq` on `before/c2-before.json`, `after/c2-final-b0005ae.json` | before `rows_matched 0/69, source_ok 0`, FAIL exit 1. After 69/69, mismatches 0, extra 0, `source_ok 1`, PASS exit 0. Matches the report |
| Novelty at base | lane `before/c2-novelty-sweep.txt` (evidence-verified) | 0 base hits for the order-rule terms |

- Recorded counter gaps:
  - a stripped entry citing only S212 still passes;
  - dropping an S-id from `source:` survives.
- My row-by-row re-derivation and source re-open cover both gaps, so they do not falsify the after-state. Routed (§6).
- Axis verdict: **depth improved** (ordinal 8 → 8 by the lane's choice).

### Owned axes not claimed

`git diff 8bd001f5 f8b4df2a -- SCORECARD.md` is 102 insertions and 0 deletions. Ordinals are unchanged (depth 8,
coverage 9, operability 9, freshness 9, calibration 9, adjacency 8).

Deletions in the whole round (`git diff --numstat … | awk '$2>0'`):
- `tools/tsukuroi-census.sh`, 4 lines: the selftest `mktemp` path became `${TMPDIR:-/tmp}`, and 1 header comment and 2 help-text lines that named `/tmp` were rewritten.
- `corpus/knowledge/adjacency-anchors-r19.json`, 2 lines: IN-109 `found_line` 2346 → 2425. I checked census line 2425 at the tip, and it holds the anchored `check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED`.

The following are evidence-verified, not re-run:
- `after/gates-final.txt`: nine lane gates `rc=0` PASS.
- `after/self-assessment-final.json`: revision `fc931bd`, `checked 27`, `mismatches 0`, `status PASS`.
- `after/selftest-final-b0005ae.txt`: 113/113.

I swept every sibling `PROVINCE.md` with `grep -ciE 'error_stats|btrfs device stats|alpm hook order|hook run order'`. Every sibling scores 0, so nothing is absorbed.

Verdicts:
- **operability unchanged**: the census selftest grew from 105 cases at base (`w1/C1ExecSelftestTmp/selftest-base.out`) to 113 at `b0005ae9`, all passing, and there is no ordinal claim.
- **freshness unchanged**.
- **calibration unchanged**: the 27/0 receipt holds, and no count is claimed.
- **adjacency unchanged**.

No axis is harmed. One side effect is noted but is not harm: the frozen round-35 probe `score-pacnew-arm-r35b.py` now
reads base-parity failures at post-`52ffd65` revisions, by construction. It is a historical counter, and the lane records
this in `SKILL.md`.

## 3. Discernment spot-check (LEARNING.md — from outside)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S208 (libalpm hook.c) → `pacman-hook-order-r38.md` | admit, tier A, mined | https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/hook.c (fetched 2026-10-26; sha256 `99f1044b…` = anchor) | agree | The quote `return l1 < l2 ? -1 : 1;` is present at :452 inside `_alpm_hook_cmp` :443-455, as the anchor says. My re-derivation of all 69 rows from this rule matches the entry exactly |
| S209 (alpm-hooks.5.asciidoc) | admit, tier A, mined | …/-/raw/54d9411/doc/alpm-hooks.5.asciidoc (sha256 `2970cb35…` = anchor) | agree | The quote (12 words, ≤25) is present verbatim at :39. AbortOnFail "Only applies to PreTransaction hooks." is at :88-89 |
| S210, S211 (trans.c, alpm.c) | admit, tier A, mined | same revision (sha256 `637c1165…`, `8bbb0a3c…` = anchors) | agree, with an anchor defect | Both quotes are present at the stated lines. The S210 anchor names the wrong symbol (`_alpm_trans_commit`), as the lane's own erratum says. The teaching stands |
| `alpm-package-anatomy-r26.md` (staged) | reject | the staged file `shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/alpm-package-anatomy-r26.md:52-53`; https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/PKGBUILD.5.asciidoc | agree | The staged line says "`package()` runs inside `$pkgdir` under `fakeroot`". PKGBUILD(5):351 says of `package()`: "This function is run inside `$srcdir`." (fakeroot is correct, the directory is not.) `grep -c QUALITY` = 0, so QUALITY 14 is unmet too. The flip condition is stated |
| `pacman-hook-timing-r25.md` (staged) | reject (not as staged) | the staged file in `shokuknow/merge/tsukuroi/…` | agree | `grep -c QUALITY` = 0. Its source ids S201, S202, S209, S212 all collide with lane rows at the tip (`grep -E '^\| *S2xx *\|' corpus/SOURCES.md`), as the Gate says. The flip condition is stated. I did not re-judge the content claims |

New `corpus/SOURCES.md` row re-opened: **S209**.
- Its quote is 12 words and resolves at the anchored line.
- Its `teaches` cell is grounded: the manual's suffix-ignoring rule and the S208 comparator agree.
- The snapshot digest equals my fetch.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → `tsukuroi ok`, exit 0, with 33
W04 advisories only.

| Revision | Rows (`grep -cE`) | Malformed (`awk NF!=13`) |
|---|---|---|
| base `8bd001f5` | 207 | not measured |
| tip `f8b4df2a` | 212 | 0 |

The `SOURCES.md` diff is 5+0 (pure append). This matches the report (207 → 212).

Result: the closure agrees with every sampled admit (S208–S211; S212 is checked via the capture MANIFEST) and with both rejects.

## 4. Axis grades (closure)

| Axis | Verdict | Basis |
|---|---|---|
| coverage | improved | C1 verified. The arm code reads production sysfs only; the live leg equals my sysfs read; the receipts (v1, Q82, selftest) agree; the frontier rule is met and the promotion is scoped |
| depth | improved | C2 verified: 69/69 rows re-derived independently, HO1–HO7 re-read at pinned 54d9411, log oracle 0/109 violations |
| operability | unchanged | selftest 113/113 (receipt); no claim |
| freshness | unchanged | no claim |
| calibration | unchanged | self-assessment 27/0 (receipt); no claim |
| adjacency | unchanged | no sibling overlap (province sweep) |

Admission: **admitted**. Both claims verify, and no axis is harmed. Verdict: `admitted`.

## 5. Trend verdicts (closure)

- **expansion: improved.**
  - Btrfs per-device error counters moved from Frontier into Core, behind a read-only census arm.
  - Capability row `storage-error-counter-reader` entered with passing receipts: fixtures, the live host (which I re-read), and namespace views.
  - No admitted entry fails its bar.
- **quality: improved.**
  - HO5/HO6 host cells are corrected append-only.
  - The round-37 duplicate journalctl block is marked by `## Round 38 correction — duplicate round-37 block` (note line 187), with no deletion.
  - The S206/S207 lane copies are byte-identical to the sibling originals (`cmp`).
  - The boot-writers override [inf] is now source-backed by HO2, which I re-read.
  - No admitted entry failed my re-checks.
- **discernment: improved.**
  - The outside spot-check agrees with the Gate on the admits and both rejects.
  - New QUALITY 83 and 84 each cite a lesson row (R38-CLOSURE-DISAGREEMENT, R38-ECHO-UNVALIDATED).

## 6. Routed defects / next-round debts (owner: tsukuroi)

1. **R38-Q82-LEAK**: `tools/score-storage-arm-r38-q82.py` admits four leak-reading arms (`w1/Q82Attack.md`). Next counter:
   - build the views in a tmpfs mounted inside the child namespace;
   - commit the four arms as should-fail controls.
2. **R38-ABSENT-ROOT**: an absent `/sys/fs/btrfs` gives HEALTHY 0/0/0. Add a `/proc/self/mounts` btrfs cross-check under a new frozen counter.
3. **C2 counter gaps**:
   - `tools/check-hook-order-r38.py` passes a stripped entry citing only S212 (`w1/CritControlsC2.md`);
   - it survives an S-id drop from `source:` (`w1/C2MutEntry.md`);
   - it cannot see block duplication past the next `## `.

   Any re-claim on this counter must close these gaps.
4. **S210 anchor**: the anchor names the non-existent `_alpm_trans_commit`. Land a new row whose `teaches` opens `supersedes S210 —` with anchor `alpm_trans_commit` (`trans.c:167`, 201-240). Do not rewrite S210.
5. **Receipt binding** (R38-STREAK-ATTRIBUTION, self-filed): before receipts and `controls.jsonl` carry no `tool_sha256` or revision. Bind every receipt to tool bytes.
6. **Historical probe**: `score-pacnew-arm-r35b.py` reads base-parity failures on post-`52ffd65` census revisions. Mark it historical in the registry, or pin its census input, so no future round cites it at a new revision.
7. **Lesson cross-reference**: the lesson Gate "Spot-check: Non-author closure pending" (`corpus/lessons/round-38.md`) is answered by this file. Cross-reference it next round.

## 7. Closure disposition

Status **ok**. Admitted **true** (`admitted`).

Verdicts:
- improved: coverage, depth
- unchanged: operability, freshness, calibration, adjacency

Trends: expansion improved, quality improved, discernment improved.

SHONEN:
- Boxes 1–2 look checkable by a non-author from the cited evidence: SKILL "Storage integrity arm — round 38" and "Hook order — round 38" tables; the LOG end-to-end task and the pacman.log oracle, which I reproduced.
- Box 3 does not: the whole-SKILL retest is unexecuted.
- Box 4 does not: no-bleed is self-asserted, although my province sweep found no crossing.

Promotion is operator-owned.
