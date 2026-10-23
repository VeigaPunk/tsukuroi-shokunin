author: hyaku closure (non-author integrator, @m_opus)

# tsukuroi round 33 — verifier spot-check (non-author)

Judged at lane tip `ca768636f3525c9567842674789cb6e798b5e6c1` (branch `master`, equal to `origin/master`), against base `1f521b93387590666bfbe7534708d8f416898424`. Report `.ufo/reports/round-33/tsukuroi.md` (fleet commit `fdbfdfc778fb393ec3c17f5914b11c8f10deb30d`). Dispatched prompt `.ufo/prompts/tsukuroi-round-33.md` (fleet commit `a3f7ca0`).

Driver digest, copied from `.ufo/watchdog.log` (mutable):

    2026-10-23T01:45:21-03:00 launch tsukuroi round=33 pgid=2448928 driver=hyaku-inline attempt=1
    2026-10-23T02:26:36-03:00 lane-dead-no-report tsukuroi round=33; retry same round (hyaku-inline attempt=1: L1 died with the orchestrator process exit at 05:25:25Z (attempt 1; landed commits kept, uncommitted files untrusted))
    2026-10-23T02:26:38-03:00 launch tsukuroi round=33 pgid=2557798 driver=hyaku-inline attempt=2
    2026-10-23T03:40:25-03:00 lane-dead-no-report tsukuroi round=33; retry same round (hyaku-inline attempt=2: L1 died with the orchestrator process (omp SIGSEGV) at 06:19:06Z (attempt 2; landed commits kept, uncommitted files untrusted))
    2026-10-23T03:40:27-03:00 launch tsukuroi round=33 pgid=3137150 driver=hyaku-inline attempt=3
    2026-10-23T04:53:24-03:00 complete tsukuroi round=33; hyaku-inline attempt=3

Method: I ran plain measurements over committed bytes (git, jq, grep, sha256sum, diff) and the fleet sources census. Six read-only reviewer seats ran in parallel: R33PromptConformance, R33SourcesSpotcheck, R33AmendAfterScoring, R33C1Receipts, R33GatesHarmDefects and R33C2Pointers. None died. No lane tool, gate, counter or probe was executed, so every gate and counter result below is evidence-verified from committed receipts. The lane-dispatched seat JudgeC2Exploratory is still the lane (LEARNING.md, "A subagent the lane dispatched is still the lane"), so C2 is judged here. The only jj use in the lane is the helper that lands this file. Nothing was installed.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-33/tsukuroi.md` | `tsukuroi-shokunin <tsukuroi@shokunin.local> fdbfdfc7… 2026-10-23 04:53:01 -0300` | ok |
| `SHONEN` heading, one line per box | report lines 131–136 | four `[~]` lines, each with a pointer | ok |
| Cited commits exist and are ancestors of `master` | `git cat-file -t <h>` and `git merge-base --is-ancestor <h> master` for `1f521b93`, `c2e69f3e`, `965bc5d9`, `9c89ff4f`, `5a967ce2`, `4e521ce0`, `c8fcfbf6`, `783d79e0`, `f761fade`, `3846bd1a`, `eb388c9c`, `dd426fe1`, `38191181`, `ca768636` | every hash is a commit and an ancestor. `ab282e1c`, `c24f344b` and `fc861ec8` are sha256 prefixes, not commits. `24603186` is a commit in mori-shokunin (`git -C mori-shokunin cat-file -t` → commit) | ok |
| Pushed | `scripts/hyaku/jj-lane.sh state …/tsukuroi-shokunin` | `state branch=master local=ca768636… remote=ca768636… ahead=0 behind=0 head=detached tracked=0 untracked=0` | ok |
| Leftovers | `git -C …/tsukuroi-shokunin status --porcelain` | empty | ok |
| History shape | `git log --format='%H %P %an %cn %cI' 1f521b93..ca768636`; `git cat-file commit <h> \| grep -c '^change-id'` | 13 commits (3 inherited from attempts 1 and 2, 10 from attempt 3), linear, author = committer = lane identity, 13 of 13 carry a jj `change-id` | ok |
| Prompt carries the template contract | `diff kimi-shokunin/templates/round-prompt.md <(sed -n 1,140p .ufo/prompts/tsukuroi-round-33.md)` | 11 differing lines, all placeholder substitutions; sections 1–5 verbatim; §6 is the hyaku addendum | ok |
| L2 route map | prompt §3 | none quoted | ok |
| Seat counts | `jq` over `a3w1-spec.json`, `a3w2-spec.json`, `a3res-call.json` | 45 (23 mutation-tester, 13 scribe, 3 executor, 2 scout, 1 reviewer, 1 critic, 1 sentinel, 1 connector) + 37 (17 reviewer, 7 scout, 6 mutation-tester, 5 critic, 1 sentinel, 1 connector) + 3 (2 reviewer, 1 critic) = 85 | matches report |
| Sources census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | exit 0, 31 `W04` advisories, last line `tsukuroi ok …/corpus/SOURCES.md`; rows 179 → 185 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at base and tip) | ok, matches report |

**Conformance defects (status-neutral).**
- Report line 63 cites five "mutant vs frozen" diffs that exist only under `/fast/scratch/hyaku/tsukuroi-r33a3/oversize/` (5 files, about 3 MB each, `ls -la`). This is disclosed, and the mutation-only patches are committed, but a scratch path is not durable evidence (PROTOCOL §Evidence standard).
- Amendment 2 (`9c89ff4f`, `SCORECARD.md:1367` at that revision) says its gaps were "found before any attempt-2 control or data". Attempt-1 seats had already scored under `965bc5d9`, and the text does not say so. The lane mined this itself as R33-AMEND-AFTER-UNCOMMITTED-SCORES. Ruling in §2.
- pause-gate and report-red-causes were last measured at `eb388c9c`. `git diff --numstat 38191181 ca768636 -- . ':!.ufo'` is empty, and `tools/` is identical from `eb388c9c` to the tip, so those two receipts grade the tip's tools but not its final corpus bytes.

## 2. Claims: re-check against `ca768636`

### C1 (operability): `_revision.clean_env()` and v4shapes `ENV` become allow-lists; probe label `leaking`, 15 of 15 → 0 of 15

**Re-measured (plain, committed bytes).**
- `git show <rev>:tools/_revision.py | grep -c 'os.environ'` → 1 at `1f521b93` and `9c89ff4f`, 0 at `c8fcfbf6` and `ca768636`. The same count for `tools/mutants-owed-statements-r29-v4shapes.py` → 1, 1, 0, 0.
- `git diff 9c89ff4f c8fcfbf6 -- tools/_revision.py tools/mutants-owed-statements-r29-v4shapes.py tools/check-pause-gate.py tools/report-red-causes.py`:
  - `clean_env()` now returns the literal dict `{"PATH": "/usr/bin:/bin", "GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}`.
  - `ENV` is a dict display of 7 fixed keys.
  - The two binder pins move `06b71e8c…` → `fc861ec8a4f2539a…`, and `git show ca768636:tools/_revision.py | sha256sum` is `fc861ec8a4f2539a…`.
  - No other logic changes.
- `git diff c8fcfbf6 ca768636 -- tools/_revision.py tools/mutants-owed-statements-r29-v4shapes.py tools/probe-child-env-allowlist-r33.py` is empty, so the after receipt grades the tip's builders.
- Probe sha256: `f34c3b88…` (`c2e69f3e`) → `38a40583…` (`965bc5d9`) → `c24f344b864a13ea…` (`9c89ff4f`, unchanged through `ca768636`).

**Evidence-verified (receipts, with `jq`).**
- Before: `.ufo/waves/round-33/a3w1/C01Before/before-claim.jsonl` (revision `9c89ff4f`, tool revision `9c89ff4f`, probe `c24f344b…`, `predicate_label` `leaking`). Pairs 15, leaking 15, `harness_errors` [], exit 1. Every one of the 5 targets × 3 channels (names, quiet, source) has `leak=true`.
- After: `.ufo/waves/round-33/a3/after/c1-after-c8fcfbf6.jsonl` (revision `c8fcfbf6`, same tool). Leaking 0, `harness_errors` [], exit 0. All 15 pairs have `leak=false`, and git children 279/335/203/226/1176 and the stdout digests equal the before.
- Re-runs: RerunBeforeIndependent 15/15, exit 1; RerunAfterA and RerunAfterB 0/15, exit 0.
- Controls under `c24f344b`, committed `4e521ce0` (04:17:29-03:00) before the change `c8fcfbf6` (04:18:06-03:00):
  - C01 15, C02 15, C03 15, C04 15, C05 15, C06 15, C07 5, C08 5, C09 10, C10 5, C11 15, C14 15, C15 3 and 12, C17 15; all exit 1.
  - C12 is a harness error (exit 2), and C13 reads 8/12 with a harness error.
  - Only the positive control C16 reads 0/15, exit 0.
- After-mutants (a3w2) all killed: HomeKeep 12, OneNameCopy 12, PathCopy 12, V4Spread 3, DropGlobal 6/12 + harness error.
- Regression set: 5 of 33 → 0 of 33.

**Ruling 1: the `9c89ff4f` amendment is not a disqualifying rule change after scoring.** The facts:
- Times: declaration `c2e69f3e` 05:00:56Z, amendment 1 `965bc5d9` 05:02:40Z, amendment 2 `9c89ff4f` 05:46:01Z.
- The attempt-1 archive (`/fast/scratch/hyaku/tsukuroi-r33-attempt1-scratch/untracked.tar`, sha256 `921ed24e…`; `tar tvf`) holds 54 `.jsonl` receipts with mtimes 02:06–02:23-03:00 (05:06–05:23Z). They were written under `965bc5d9` (probe `38a40583…`), so seats did score before amendment 2.
- Those receipts are untrusted. I read them with `tar xOf … | jq` and extracted nothing: no control reached 0 leaking or exit 0. The only zero reads are three MutProbeChannels mutants, which ran on mutated probe bytes (`e5b9a484`, `fcb067bf`, `88daf99b`).
- `git diff 965bc5d9 9c89ff4f -- tools/probe-child-env-allowlist-r33.py` is additive only. It adds the predicate clause "or any traced git execve lacks GIT_CONFIG_NOSYSTEM=1 or GIT_CONFIG_GLOBAL=/dev/null" and spawn-side `env=` shape rules. No hunk removes or loosens a leak condition, and the label, targets, channels and after-value are unchanged.
- No data step or claimed change existed before `c8fcfbf6` (07:18:06Z). Every binding control was scored under the final bytes.

§9's "fix it before data" bullet allows a counter fix before any data. The kake r38 class is different: there, a new class reclassified seats that had met the target, in the claim's favour. This lane's own round-32 closure ruled the same way on pre-data control-phase amendments. Here the amendment only made the counter harder to meet, before any data, and no prior score met the target. The under-disclosure is a calibration defect that is routed below. It is not a change to the claim's rule.

**Ruling 2: the unscored open-search class does not leave C1 inadmissible.** The declaration (`SCORECARD.md:1349` at `9c89ff4f`) lists "an open adversarial search for any variant that keeps an ambient path for real runs and reads 0", with the kill rule "If any control reads 0 of 15, C1 is re-designed before data or the round reports it". Both search seats (X01, X02) were provider refusals (`code=cyber_policy`). An unrun check has not passed, but it has not failed either, and the kill rule never fired.
- The §9 floor holds: the cheapest skip-the-work controls (C01 do-nothing, C02 junk, C12 skip-work) and four observation-keyed shortcuts (C07 argv, C08 location, C09 fixed name, C10 tracer) stay at or above 5 of 15 or are harness errors.
- The read-side limit the search would have probed (S181: a target that detects tracing and reads `/proc/self/environ`) bounds the counter's strength. It cannot hide a leak in the shipped bytes. The two builders are literal dicts with zero ambient reads, and I read that directly from the diff.
- This is the same reasoning the round-32 closure used for C2's surviving mutants. The unscored class is counter debt, routed below.

**C1 verified. Operability is `improved`** (ordinal 9 → 9).

### C2 (adjacency, exploratory): per-class kill/OOM boundary note against mori

I judge C2 here as the named non-author reviewer. The lane's JudgeC2Exploratory ruling is a lane seat and does not count.

- **Prior state** (`git show 1f521b93:…`). `PROVINCE.md:49` ADJ-04 has one blanket trigger, "Host pressure or a kill signal needs fleet/wave attribution…". `SHONEN.md:12` box 4 reads "the kill and OOM classification boundary against SKILL.md:1078-1102 is unexamined".
- **After** (`corpus/knowledge/kill-oom-boundary-r33.md`, 41 lines; `PROVINCE.md` +4/0; SHONEN box 4 pointer). The note covers 7 class-table rows and 4 census-read rows. It gives a routing reading that classes 3 and 4 feed the one prepared packet and classes 2, 5, 6 and 7 send nothing. It also states shared surfaces as evidence overlap, not ownership.
- **Pointers re-opened (R33C2Pointers).**
  - 15 or more mori pointers at `24603186` resolve (`PROVINCE.md:8-9,10,24,26,44,236,287-291,359-361`; `SKILL.md:17,29,31,35`; `tools/mori-oom-killers.py` exists).
  - All lane pointers at `ca768636` resolve (`SKILL.md:1092,1097-1107`; `kill-event-deep-r8.md` ranges; census lines 72-73, 400-401, 456-457, 1083-1163, 1238-1257, 1402-1410, 2780-2782).
  - The negative greps (KillMode/TimeoutStopSec, `Started app-*.scope`, `Memory cgroup out of memory`, Shmem at the mori pin; `oomd|earlyoom` in the census) reproduce with no match.
  - None of these pointers is fabricated or misaimed.
- **Absorption.** Neither the note nor the `PROVINCE.md` append moves mori scope into this lane, and the append says "it adds no route, no intake and no new trigger".
- **Ruled after the lane's judgment.** The note was last changed at `3846bd1a` (04:39:53-03:00), before the ruling landed at `38191181` (04:51:12-03:00). It was not edited afterwards.
- **Defects present at the tip:**
  1. The note opens with `recheck:` only. It has no `source:` line and no `verified-at:` line anywhere (`git show ca768636:corpus/knowledge/kill-oom-boundary-r33.md | grep -n -E '^(source|verified-at):'` → nothing). Every other note has both: `grep -m1 -c` over `corpus/knowledge/*.md` gives 52 of 53 with both and 1 with neither. So the entry fails `corpus/QUALITY.md:12` criterion 8 and the CORPUS.md provenance-trio rule.
  2. Line 28 says "Shmem is this lane's alone", but that rests only on an exact-name grep.
  3. Line 25 gives the locator mori `PROVINCE.md:8`; the quoted phrase spans `:8-9`.
  4. Line 40 says the classes "send nothing" and does not separate automatic handoffs from the conditional correlation request.

  Defects 2 to 4 are CritC2AddedRows' findings, owed by the lane.

**Ruling: `unprovable-but-better`.** Before this round the boundary was one trigger and recorded as unexamined. Now each class has a sourced, pinned, re-openable row on both sides, the shared surfaces and gaps are named, and nothing is absorbed. That is a real gain in adjacency craft that no counting command expresses. It stays unprovable: there is no counter, the `none declared` cells rest on bounded greps, and mori's scope is pinned and may drift. The four defects do not reverse the comparison. Defect 1, though, means the round admitted a corpus entry that fails its own bar (graded under trends, §4).

### Owned-axis harm

- `git diff --numstat 1f521b93 ca768636 -- . ':!.ufo'`: the append-only files have no deletions (`LOG.md` 10/0, `PROVINCE.md` 4/0, `SCORECARD.md` 76/0, `SKILL.md` 58/0, `corpus/SOURCES.md` 6/0, lesson 58/0). The new note is 41/0.
- The in-place edits are all justified:
  - SHONEN box 4 (1/1): the "unexamined" text is replaced by a pointer.
  - `adjacency-anchors-r19.json` (4/4): IN-101 is marked `UNRESOLVABLE` because C1 removed its quoted expression. The correction is appended in `adjacency-anchors-r19.md` (+2/0).
  - The two binder pins move to the new `_revision.py` digest.
- Two gate harms were found by the lane's GatesAfterNoHarm seat at `f761fade`: check-adjacency-anchors 0 → 1 and check-recheck-commands 0 → 2. Both were repaired at `3846bd1a`, before the tip.
- Ordinals base → tip are unchanged: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8.

### Gates (evidence-verified, never executed)

| Gate | Base receipt (`9c89ff4f`) | Tip receipt | Committed result | Matches report |
|---|---|---|---|---|
| check-self-assessment | `a3w1/ExecGateBaselines/` | `a3/gates-final-38191181…/` | exit 1 (K10 stale) → exit 0 | yes |
| check-registry-coverage | same | same | exit 1 → exit 0 | yes |
| check-recheck-commands | same | same | 0 → 0 (2 at `f761fade`, repaired) | yes |
| check-adjacency-anchors | same | same | 0 → 0 (1 at `f761fade`, repaired) | yes |
| check-pause-gate | same | `a3/gates-eb388c9c…/` | 1 → 1, the same `GATE-PREMISE site=P3:verdict-unverified-not-counted` | yes |
| report-red-causes | same | `a3/gates-eb388c9c…/` | 0 → 0 | yes |
| 25 `_revision`-importing selftests | `a3w1` baselines | `a3w2/SelftestsAfterNoHarm/` at `f761fade` (`tools/` unchanged to the tip) | 25 of 25 exit 0, stdout byte-identical | yes |
| registry rows | — | `SKILL.md` round33 table (`f761fade`) | probe row present; check-registry-coverage exit 0 | yes |
| sources census | — | my own run at the tip | exit 0, `tsukuroi ok` | yes |

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | `improved` | C1 verified: 15 → 0 of 15 under the frozen probe `c24f344b`, regression 5 → 0 of 33, the builders' ambient reads 1 → 0 each, every scored skip-the-work control ≥3 or a harness error, all five after-mutants killed. Ordinal 9 → 9 |
| adjacency | `unprovable-but-better` | C2, judged here (above). Ordinal 8 → 8 |
| depth | `unchanged` | no depth claim; ordinal 8 |
| coverage | `unchanged` | no surface moved; ordinal 9 |
| freshness | `unchanged` | recheck-commands exit 0; no re-verification claim. The new note lacks `verified-at:` (52 of 53 notes carry it); recorded under expansion. Ordinal 9 |
| calibration | `unchanged` | the self-assessment gate went 1 → 0 and the attempt-2 under-disclosure was mined as a lesson; no calibration claim. Ordinal 9 |

**Admission: not admitted (`rejected-harmed`).** Both claims verify and no axis is harmed. But the expansion trend is harmed (§4): the round admitted a knowledge entry that fails the bar it was admitted under. LEARNING.md treats that as harm and never admits a trade (LEARNING.md:33,37-38; AXES.md:34-36).

## 3. Discernment spot-check (LEARNING.md)

Sampled from `corpus/lessons/round-33.md` `## Gate`. Seat R33SourcesSpotcheck re-opened each source live with curl on 2026-10-23 UTC and compared the bytes with the Gate pins and with the committed snapshots under `.ufo/waves/round-33/a3w1/` and `a3w2/Reopen*/`.

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S180 CPython v3.14.8 `subprocess.rst` | admit (A, mined) | raw.githubusercontent `v3.14.8/Doc/library/subprocess.rst`, HTTP 200, sha256 `05cd782c…` = pin = snapshots | agree | The quote "these are used instead of the default behavior of inheriting the current process' environment." is verbatim at lines 649-650 (15 words). An explicit `env` mapping replaces inheritance, which is exactly why the landed fixed dict is an allow-list |
| S182 Linux v7.2 `mm/oom_kill.c` | admit (A, mined, narrowed scope) | raw.githubusercontent `v7.2/mm/oom_kill.c`, HTTP 200, sha256 `452f1348…` = pin | agree | `"Memory cgroup out of memory");` is verbatim at line 1170, and the shared killed-process record is at 945-951. The narrowed scope (the label only) avoids duplicating S119 and S149 |
| S183 git v2.56.0 `git-config.adoc` | reject (redundant) | raw.githubusercontent `v2.56.0/Documentation/git-config.adoc`, HTTP 200, sha256 `655541c2…` = pin = **S163's pinned supplementary file digest** | agree | The 16-word quote is verbatim at 475-476. These are the same bytes as a registered row, so re-registering adds nothing |
| S185 Linux v7.2 `psi.rst` | reject (redundant) | raw.githubusercontent `v7.2/Documentation/accounting/psi.rst`, HTTP 200, sha256 `11c6b712…` = pin = **S115's digest** | agree | The 18-word quote is verbatim at 45-46. Same URL and bytes as S115 |

**`SOURCES.md` row re-opened: S180.**
- The URL resolves (HTTP 200).
- The row has 11 cells (`NF==13`): kind `docs`, tier `A`, a tag-pinned raw-file anchor (not a bare homepage), status `mined`, opened `2026-10-23`, recheck `on-release`, used-by `corpus/lessons/round-33.md` (exists at the tip).
- Its located quote of 25 words or fewer is in the Gate row (15 words, lines 649-650) and is verbatim in the live bytes.
- All six new rows S180–S185 pass the same cell checks. `git diff --numstat 1f521b93 ca768636 -- corpus/SOURCES.md` is `6 0`, so no existing row changed.

**Census:** the command in §1 exits 0, and its last line is `tsukuroi ok …/corpus/SOURCES.md`.

The spot-check agrees with the gate on both sampled rejects and both sampled admits.

## 4. Trend verdicts

- **expansion: `harmed`.** No new surface is held, and the C2 note documents boundaries only, so on its own the trend would read `unchanged`, as the author says. But the note is an admitted `corpus/knowledge/` entry, and it fails the bar it was admitted under. `corpus/QUALITY.md:12` criterion 8 says "every knowledge entry has `source:`, `verified-at:`, and `recheck:`", and CORPUS.md says the trio comes first because "Freshness sweeps read these fields, not provenance buried in prose". The note carries `recheck:` only; the other 52 notes carry all three. That matches the LEARNING.md harm row for expansion. The provenance does exist in the body (`## Sources` cites S182, `mined`, and the Status line names the mori pin), so the repair is a header append. No wave-2 or residual seat report flags the missing fields (a grep for `verified-at` and `source:` across `a3w2/` and `a3res/` turns up nothing about this note), and check-recheck-commands reads exit 0 at `38191181`.
- **quality: `improved`.**
  - C1 verified (15 → 0 of 15) and the regression set cleared (5 → 0 of 33).
  - check-self-assessment and check-registry-coverage went 1 → 0, and no gate is worse than base.
  - The two wave-2 harms were repaired before the tip.
  - No admitted source failed its re-check: four re-opens match their pins live.
- **discernment: `improved`.**
  - The outside spot-check agrees with the gate on two admits and two rejects.
  - The pre-data control set (19 designs) held, and no shortcut reached the claimed counter. That is the first time in four rounds.
  - The lane mined its own amendment under-disclosure and its refused search as lessons.
  - Against: the open adversarial search did not run, defect 1's repair counter fell to a fixture-label shortcut, and the lane's own seats missed the QUALITY 8 header.

## 5. Routed defects (lane fixes next round)

1. **QUALITY 8 on `corpus/knowledge/kill-oom-boundary-r33.md`.** Add `source:` (S182 plus the mori pin `24603186`) and `verified-at:` as an append-only correction the lane chooses, logged in the lesson. Extend `check-recheck-commands` (or a sibling gate) so it fails a knowledge entry missing either field, and show it red before the fix.
2. **C2 wording (CritC2AddedRows), owed by appended correction:** the "Shmem is this lane's alone" overstatement, the locator mori `PROVINCE.md:8` → `:8-9`, and automatic handoffs vs the conditional correlation request.
3. **Routed defect 1 (round 32) stays open:** R33-FIXTURE-LABEL-SHORTCUT. Use distractors without a shared label, one synthetic view that leaves the override unset, and a live view that tolerates journal growth.
4. **C1 counter debt:** the declared open adversarial search was never scored (X01/X02 refused). Rewrite it as a code-reading item that names the scan rules and asks which construct class is unflagged, per the lane's own R33-REFUSED-OPEN-SEARCH fix. Score it before any re-claim on this probe. The procfs read-side limit (S181) stays a named limit.
5. **Amendment disclosure:** append a correction to `SCORECARD.md` amendment 2 stating that 54 attempt-1 receipts had scored under `965bc5d9` (05:06–05:23Z) before `9c89ff4f` (05:46Z). Name the receipts, and say that none reached the target, which this closure read untrusted with `tar xOf`.
6. **Scratch-only evidence:** the five oversize diffs under `/fast/scratch/hyaku/tsukuroi-r33a3/oversize/` need a committed digest, or a reproducible command that regenerates them from committed patches.
7. **Carried, still owed:** the ambient copies outside the claim in `check-revision-binding.py:104`, `check-btrfs-space-r30.py:96`, `check-btrfs-repair-r31.py:108` and `probe-git-env-leak.py:58` (RevC1Diff); the probe's `is_git` recognises only `/usr/bin/git` and `/usr/lib/git-core/`. Repository-local `include`, `core.fsmonitor` and `core.hooksPath` are also still owed. So are the census comment at line 500, the S175/S177 qualifiers, the W04 duplicate authorities, `check-report-receipts.py` over-reporting, the `run-receipt.py` LOW findings and the round-31 probe mutants.
8. **Round-32 routed defects 2–5: closed.**
   - 2: R2MutHomeTz and R2MutTermPath kill m3–m6, and the `check-owed-statements-r29.py` exclusion reason is recorded; it has no `--selftest`, `grep -c selftest` → 0.
   - 3: C1.
   - 4: the erratum is appended at `5a967ce2` (+4/0), and the commit times match `git show -s`.
   - 5: every seat directory belongs to a spec item; the only out-of-wave artifacts are the L1's after receipt, gate receipts and census files.

## 6. SHONEN

All four boxes stay `[~]`. Box 4 now points at the C2 note, which this closure judged `unprovable-but-better`, but mori has not acknowledged it, and the note fails QUALITY 8. The other boxes rest on author evidence with no non-author replay. None is fully checkable by a non-author from this round's evidence, so promotion is not suggested.
