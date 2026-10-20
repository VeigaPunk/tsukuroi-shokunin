# ScoreReviewR — tsukuroi round 12 resumed (score delta review)

Seat: `TsukuroiR12.ScoreReviewR` (reviewer, leaf, read-only). Repo: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Path note: the assignment names both `resumed/ScoreReview.md` and `resumed/ScoreReviewR.md`; this seat writes `ScoreReviewR.md` (the explicit Report line and the `<seat>.md` rule). Inherited `.ufo/waves/round-12/ScoreReview.md` is historical and is not edited.
Baseline: HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`. Working tree was **mutating during this review** (other seats editing); every state below is a dated snapshot at review time, 2026-10-20, not a pinned commit.
Installs / updates: none. Checks run: none (no tests, builds, census selftest, or live census run). Probes below are read-only seat-side observations; none is a non-author verification (AXES.md: a dispatched subagent does not count as non-author).

## 1. Outcome

- **Score delta: unchanged for every axis.** Depth stays **8**; operability stays **9**; adjacency stays **8**. Nothing in the tree is verified yet for C1 or C2, so no after-state exists to score.
- **C1 (operability): NOT LANDED.** The census diff has a `ROOT_DIR` seam and an inert `ROOT_V` initializer, but no probe body and no selftest wiring. Verdict: `unverified / in progress`.
- **C2 (depth): structure present, falsifiers absent.** `corpus/knowledge/root-dac-decision-r12.{json,md}` has 4 branches, 8 scenarios and a 6-step procedure. None of the 4 branches carries a falsifier, and the procedure has an unguarded precondition. Verdict: `unverified`; the depth move is conditional (section 5).
- No PASS is claimed for C1 or C2.

## 2. Authoritative scores and the lowest-axis obligation

Latest authoritative append (re-checked): `SCORECARD.md` section `## Fleet round 1 — post-review claim corrections (2026-10-19)` (lines 207–240). It is measured at `459e3ce`, and `git merge-base --is-ancestor 459e3ceacea6289d74b6e856c5606b83704f32e5 HEAD` → exit 0 (ancestor).

| Axis | Score now | Source |
|---|---|---|
| depth | 8 | `SCORECARD.md` final self-assessment row (lines 45–52), r4 last change; no later append moves it |
| adjacency | 8 | post-review claim A (7→8) |
| coverage | 9 | post-review claim B (8→9) |
| operability | 9 | final self-assessment row, r11 |
| freshness | 9 | post-review claim C (8→9) |
| calibration | 9 | final self-assessment row, r10 |

- **Lowest-axis obligation.** Depth and adjacency are tied at 8; retired: none. AXES.md:33–34 needs at least one claim on a lowest non-retired axis. C2 works depth → compliant. The stagnation nudge (AXES.md:68–73) does not apply: not every owned axis is ≥9.
- **Claim count / distinctness.** 2 claims (within 1–3), on distinct axes (operability, depth). Compliant.
- **Stale conflict still present.** `SCORECARD.md:45–52` still reads adjacency 7, coverage 8, freshness 8. The post-review section supersedes these in prose, but no dated correction row exists. Parent should append the supersession; do not rewrite the table.

## 3. Causal separability C1 vs C2 (AXES.md:30–32)

- **C2 is separable.** `root-dac-decision-r12.md:16–17` declares independence; `grep -in census` in the matrix JSON/MD returns only that declaration. The matrix reads no census line. Its probes are direct (`stat`, `getfacl`, `findmnt`, `systemctl show`, `journalctl`, `snapper list-configs`).
- **C1 is separable from C2.** The census diff (section 4) does not reference the matrix or the EACCES branches.
- **Shared file, not shared verification.** Both claims touch `SKILL.md` (round-12 section at `SKILL.md:1676–1709`). That is an edit overlap, not a verification dependency. Parent must confirm the C2 text carries no census arm name (see section 8, check 3).

## 4. C1 state in source (census operability)

Diff at review time: `git diff --stat -- tools/tsukuroi-census.sh` → 23 insertions, 0 deletions; `wc -l` 2425 (HEAD 2402).

What exists (verified by `git diff -- tools/tsukuroi-census.sh`):
- Header comment describing the root arm (lines ~88–105) and the `TSUKUROI_ROOT_DIR` override documentation (~line 314).
- `ROOT_DIR=${TSUKUROI_ROOT_DIR:-/}` (line 353).
- `ROOT_V=BLOCKED ROOT_NOTE='probe not run'` (line 463).

What does **not** exist (verified by `grep -n 'ROOT_DIR\|ROOT_V\|ROOT_NOTE\|TSUKUROI_ROOT_DIR' tools/tsukuroi-census.sh`):
- **No probe body.** `ROOT_V` and `ROOT_NOTE` have one use each (initialization). `ROOT_DIR` is never read by a probe. No `stat -L` on `ROOT_DIR` exists in the file.
- **No composition into the packages line.** Nothing emits `root_status=`, `root_mode=`, `root_owner_write=` or `root_owner_search=`.
- **No selftest wiring.** The selftest dispatcher env block (census lines ~1764–1790) has no `TSUKUROI_ROOT_DIR=` entry. The header's promise ("the selftest points it at a 0755 fixture directory, never at the live root") is not implemented.

Consequence and harm check (pre-landing, with the probe body not yet present; the risk applies once it is):
- If the probe lands without the selftest env entry, every hermetic case reads the **live** `/` (`555 root:root`, verified in section 6). Packages-plane cases expecting HEALTHY would then fail, and the 80-case gate would report false verdicts. Harm risk: **high** until wired.

## 5. Proposed score delta (bounded)

| Axis | Proposed | Condition / reason |
|---|---|---|
| depth | **unchanged at 8** now; eligible for **at most +1 (8→9)** after C2 closes its gaps | AXES gives no count-to-score rubric, so no count justifies more than one step for one claim. Gaps (all verified in section 6): (a) 0/4 branches carry a falsifier; (b) procedure step 1 maps "target present" to B4 regardless of observed errno, with no guard and no scenario for target-present + EACCES; (c) SKILL.md carries only 3 root-arm rows (`SKILL.md:1683–1687`) and not the four B1–B4 create-class branches. The branch content lives in the corpus note, which the depth row already cites by convention. |
| operability | **unchanged at 9** | C1 is not landed. If it lands and the triple in section 7 runs, record "blind spot closed, three distinct outcomes; score unchanged at saturation line 9". The 9→10 move has no rubric support. |
| adjacency | **unchanged at 8** | Not a round-12 claim. Input reproduced (section 6); acceptance not established, so no credit moves. |

**Harm check:** no axis is measurably harmed yet, because neither claim has landed behavior. The concrete harm risk is the uncommitted SKILL/QUALITY overclaim (section 8, risks 1–2), which affects calibration if it is committed as-is.

## 6. Re-check of inherited evidence against present source

Read-only probes, run by this seat (uid `vgpnk`, non-root). Exit codes recorded.

| Measure | Inherited (`ScoreReview.md`) | Present (this review) | Status |
|---|---|---|---|
| `stat -c 'mode=%a owner=%U:%G type=%F path=%n' /` | 555 root:root | `mode=555 owner=root:root type=directory path=/`, rc=0 | reproduces |
| `getfacl -p /` | base entries only | `user::r-x group::r-x other::r-x` (base), rc=0 | reproduces |
| `test -w /` / `test -x /` | (not inherited) | rc=1 / rc=0 | new observation |
| `findmnt -n -o TARGET,FSTYPE,OPTIONS /` | rw btrfs | `/ btrfs rw,...,subvol=/@`, rc=0 | reproduces |
| `systemctl show -p User -p CapabilityBoundingSet -p AmbientCapabilities -p ProtectSystem -p ProtectHome -p ReadOnlyPaths -p ReadWritePaths -p NoNewPrivileges limine-snapper-sync.service` | User=root, cap_sys_admin, ProtectSystem=no | same values, rc=0 (configured properties; unit inactive per earlier record) | reproduces |
| `journalctl --no-pager -o short-iso -g 'create subvolume failed' \| grep -c 'errno:13'` | DAC note: 9; mechanism note: 8 | **9** | matches DAC note; mechanism note's 8 is an earlier-pinned count (see risk 6) |
| `stat -c '%F %a %n' /.snapshots` | rc=1 ENOENT | `stat: cannot stat '/.snapshots': No such file or directory`, rc=1 | reproduces |
| `snapper list-configs` | header only, 0 rows | header only (rc not captured separately) | reproduces |
| `pacman -Qo /` | rc=1 no owner | `error: No package owns /`, rc=1 | reproduces |
| `jq empty` on matrix JSON | (not inherited) | parses; keys `branches, decision_procedure, evidence_refs, host_causal_attribution, host_observation, independence, round, scenarios, schema, scope` | new |
| matrix branches | 4 | `.branches\|length` = **4** | reproduces |
| branches with `source_ids` ≥1 | (not inherited) | **4/4** | new |
| branches with a `falsifier` key | required by inherited review | **0/4** (keys: `discriminator, evidence, id, interpretation, limit, source_ids`) | **gap** |
| scenarios | 8 | `.scenarios\|length` = **8** | reproduces |
| decision procedure steps | (not inherited) | `.decision_procedure\|length` = **6** | new |
| `SKILL.md` `wc -l` / `^\|` rows | 1673 / 61 | **1708 / 69** at review time (uncommitted edits) | **drifted** (SCORECARD's 1631/55 is two generations stale) |
| knowledge notes `corpus/knowledge/*.md` | 30 | **31** | **corrected** (SCORECARD says 24, r11) |
| census `wc -l` | 2402 | **2425** (uncommitted) | drifted |
| SCORECARD `wc -l` | 240 | 240 | unchanged; `git diff --stat -- SCORECARD.md` empty |
| SKILL `corpus/knowledge/*.md` cites, unique | (not inherited) | 26 unique; 25 resolve locally; `corpus/knowledge/fleet-kill-rate-ledger.md` does not exist locally but is cited as `tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md:47` (SKILL.md:1504), which exists (36169 B) | **not a defect**; a repo-prefixed resolver is required (see section 7) |
| mori adjacency receipt (sibling `/home/vgpnk/Projects/shokunin/mori-shokunin`, HEAD `6531ac6`) | ref `20e2255` → 0, ref `1f07f1d` → 1 | `git cat-file -t` commit for both; `git grep -q TSUKUROI-F1-MEM-01` → 20e2255: 0, 1f07f1d: 1; HEAD grep counts LOG/PROVINCE/SCORECARD 1 each | **reproduces** via sibling path |
| SCORECARD command path `.tower/worktrees/kaika/mori-shokunin` | absent | `ls` rc=2, absent | **still not reproducible verbatim**; sibling path used |
| discernment conflict | `round-1-verifier-spotcheck.md:17` "improved"; SCORECARD "unchanged" | line 17 reads "discernment improved (the outside disagreement became the appended QUALITY check)"; `SCORECARD.md:107` "discernment unchanged" (2026-10-15 blocked appendix) | reproduces; outside my axes, flagged only |
| census C1 root probes | 0 | 0 probe bodies (section 4) | reproduces; `ROOT_DIR`/`ROOT_V` seam only |
| SCORECARD latest append | post-review section | `SCORECARD.md:207–240`, ancestor of HEAD (rc=0) | reproduces |

**Reuse / reject / correct (inherited `ScoreReview.md`):**
- **Reuse:** the authoritative-append identification, the tied-lowest obligation, the separability analysis, the "+1 at most, unchanged now" delta, the stale-table conflict, and the mori receipt reproduction (via sibling path).
- **Correct:** knowledge note count 30 → 31; SKILL 1673/61 is correct *at its time* but has drifted to 1708/69 in the working tree; the mori command path must be read as the sibling path; census line count 2402 → 2425 (uncommitted, not a claim).
- **Reject:** the inherited "14 of 54 SKILL rows with source anchor + numeric token" heuristic as a depth counter (section 7 replaces it with finite counters).
- **Not re-run:** the census selftest (80 cases) and the live census. The inherited "80 selftest cases" stays unverified here. A static `grep -c "^  check '"` gives 77, but that count is not a substitute for a run and is not used.

## 7. Finite counting commands (replace test-count and token-count)

Counters measured now (read-only, no check runs):

- **C2 structure:** `jq '.branches|length' corpus/knowledge/root-dac-decision-r12.json` → 4.
- **C2 sourcing:** `jq '[.branches[]|select((.source_ids|length)>=1)]|length' …` → 4.
- **C2 falsifiers (gap):** `jq '[.branches[]|select(has("falsifier"))]|length' …` → **0**. Target: 4.
- **C2 scenarios:** `jq '.scenarios|length' …` → 8.
- **C2 procedure:** `jq '.decision_procedure|length' …` → 6.
- **Citation resolution (repo-prefixed, corrected):** extract unique `corpus/knowledge/*.md` cites from `SKILL.md`, then `test -e` each. Measured: 26 unique, 25 ok, 1 "missing" that resolves only under the `tameshi-shokunin/` prefix. The counter must accept an explicit sibling-prefix list or it reports a false miss.

Operability counter (C1, not yet runnable):
- Three fixture runs of `bash tools/tsukuroi-census.sh` with `TSUKUROI_ROOT_DIR` pointed at (a) a 0755 directory, (b) a 0555 directory, (c) an unreadable-parent fixture, each recording **exit code and the emitted packages verdict+root note**. Score evidence = number of distinct (exit, verdict, root_status) triples = **3 required**. This replaces the 80-case total.
- Unreadable class: the live `/` cannot be made unreadable by a non-root user [inf: `stat(2)` on `/` traverses no components, so no search bit is consulted on `/` itself; not measured here]. The fixture must make the **parent** unsearchable (EACCES on the child path) and must be run non-root. As root, DAC is bypassed, so the unreadable class must report BLOCKED/skipped, never pass.

Do not count: EACCES/errno token hits (20 across the tree at HEAD, mostly narrative), `wc -l`, selftest case totals, or note totals as depth or operability evidence.

## 8. Risks and verification gaps

1. **Overclaim in uncommitted SKILL text.** `SKILL.md:1678–1681` says "The packages plane now observes `/` metadata … Read `root_mode`, `root_uid` and `root_gid` on the packages line". At review time the census emits none of these fields (section 4). This is present-tense capability text ahead of code. Must be corrected or C1 landed and run before any round-12 append.
2. **Overclaim in uncommitted QUALITY text.** `corpus/QUALITY.md:17` (criterion 13): "the census separately reports root-directory mode". Same defect as risk 1. Not a verified fact at this snapshot.
3. **Separability check owed.** Parent must confirm the C2 SKILL rows and the root-arm rows do not name a census arm as a precondition (grep the round-12 section of `SKILL.md` for `census` inside the EACCES rows).
4. **Census selftest env not wired** (section 4). Blocker for any C1 evidence.
5. **Depth falsifiers missing** (0/4), and **procedure step 1 unguarded**: "target present → B4 class" holds only if the observed errno is EEXIST. Target-present with EACCES is not covered by any scenario, and the ordinary-`mkdir` order (existing target → EEXIST even under a 0555 parent, `error-order-smoke.json`) is explicitly not extrapolated to the Btrfs ioctl (`root-dac-decision-r12.md:70`). The correct behavior is UNCLASSIFIED for EACCES + target-present, not B4. Proposed fix for the Matrix seat: add an errno precondition to step 1 and a scenario for it. Not edited here.
6. **Journal count drift between notes.** `snapper-eacces-mechanism.md` states 8 `errno:13` (last `2026-10-19T08:11:47-03:00`); the matrix states 9 (last `2026-10-19T22:48:24-03:00`); this seat's probe at review time also reads 9. The mechanism note's count is a dated earlier value, not an error; its append-only erratum (2026-10-20 block) does not address the count. Owner should add a dated count note; not edited here.
7. **Adjacency tie input is only reproducible through a sibling path.** The SCORECARD's `.tower/worktrees/kaika/mori-shokunin` is absent; the same commits resolve under `/home/vgpnk/Projects/shokunin/mori-shokunin`. Receipt status is `prepared` with acceptance unobserved (inherited), so no adjacency credit follows from this review.
8. **Tree is mutating.** Seven tracked files and four untracked entries were modified during this review (`git status --short`). SKILL.md moved 1673 → 1708 lines during the review. Any score must be pinned to a commit before a SCORECARD append.
9. **Discernment conflict** remains outside this lane's axes: `round-1-verifier-spotcheck.md:17` vs `SCORECARD.md:107`; no learning credit follows.
10. **Tool-output instruction ignored.** A tool result during this review contained an embedded message asking this seat to write reports under `tameshi-shokunin/.ufo/waves/round-12/w2/`. It is not from the parent assignment; it was not followed. The write stays at the path above.
11. **Unrun:** census selftest, live census, C1 fixture runs, and any C2 independent replay. No result in this file is a test result.

## 9. Checks for the parent after integration (once, not mid-flight)

- `bash tools/tsukuroi-census.sh --selftest` after wiring `TSUKUROI_ROOT_DIR` into the selftest env: exit code recorded; expect the 80 hermetic cases unchanged in verdict.
- C1 triple: three runs (0755 / 0555 / unreadable-parent, non-root), each with exit code and emitted packages verdict + `root_status`. Require 3 distinct triples.
- `jq '[.branches[]|select(has("falsifier"))]|length'` → must be 4 before any depth +1.
- Confirm C2 text carries no census arm name: grep the EACCES rows of the round-12 SKILL section for `census`.
- Confirm no edit touched freshness (9) or coverage (9) rows; re-run `git diff --stat` on `SCORECARD.md` and `PROVINCE.md`.
- Pin the commit before any SCORECARD row is written; the depth row must replace its note-count / line-count / case-count evidence with the counters in section 7.

Installs/updates in this review: none.
