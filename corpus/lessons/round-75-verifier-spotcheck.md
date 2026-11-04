# Round 75 — verifier spot-check (hyaku closure, non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04
lane: tsukuroi-shokunin
base → measured: `a21302a48d24cf5242ac2a66cc5b5b453f7a1b20` → `bd0acc444cd6c82823602ed7a49bd1ef11360d2d`; lane tip / remote `bd0acc444cd6c82823602ed7a49bd1ef11360d2d`

Round verdict: **rejected-honest-stop** — real, verified work (six true sourced JT rows; both r74
repairs), but the frozen C1 clause "propagating restart only as try-restart" is falsified by the
pinned `transaction.c` (branch-scoped comment at `:1203-1204`; direct `JOB_RESTART` at `:1019` via
the `:1220-1247` graceful branch), so not every claim verifies. The lane self-declared the honest
stop; this closure independently reproduces it. C2 verifies. No axis harmed.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report authorship | `git log --format='%an <%ae> %H' -- .ufo/reports/round-75/tsukuroi.md` (fleet) | `tsukuroi-shokunin <tsukuroi@shokunin.local> 350b464fd163774835947de782311a0f018edbef`; committer identical; ancestor of `origin/main` and `origin/master` | PASS |
| SHONEN heading | `grep -c '^## SHONEN'` + `grep -cE '^- \[(x| |~)\]'` | 1 heading, 4 `[~]` lines (4 boxes), no `[x]` | PASS |
| Cited commits exist + ancestor of branch | `git cat-file -t <h>` + `git merge-base --is-ancestor <h> master` for `1e2bb29c`, `c15fe829`, `71ab09f4`, `e5f5ca9e`, `bd0acc44`, base `a21302a4` | all present; all `ancestor-of-master OK` | PASS |
| Lane pushed / no lane debt | `scripts/hyaku/jj-lane.sh state` | `branch=master local=bd0acc44 remote=bd0acc44 ahead=0 behind=0 head=detached tracked=0 untracked=7` | PASS (markers noted) |
| Working tree | `git -C tsukuroi-shokunin status --porcelain` | seven untracked wave-runner markers: `.ufo/waves/{66,67,73,74,75}/w1.ready.dispatched`, `round-73/w1-run.stderr`, `round-75/w1.ready`; the r75 spec, dispatch and results are committed (`c15fe829`, `e5f5ca9e`). Not lane round work; carried as runtime bookkeeping | PASS (noted, defect 5) |
| Report ordering | lane tip / report commit / driver complete timestamps | lane tip `01:35:09`, report `01:35:55`, `complete tsukuroi round=75` `01:36:55`; report cites the pushed lane tip | PASS |
| Prompt contract | read `.ufo/prompts/tsukuroi-round-75.md` (704 lines) | template sections 1–5 with placeholders substituted; all five child-lane items (report path/filename, commit-before-report, SHONEN heading, hash-citation, write scope); §6 run-15 addendum + §7 scratch discipline; L2 floor ≥8 matches `MISSION.md` §L2; committed `8afab848`, pushed | PASS |
| Prompt route label | compare §6 routing lines with `~/.omp/agent/config.yml` `task.agentModelOverrides` | the prompt's "latest amendment" says only `reviewer` uses `@m_zfl`; the live operator config also routes `critic`, `executor`, `scribe`, `connector`, `sentinel`, `mutation-tester` to `@m_zfl`. The prompt itself makes the config the authority and forbids passing `model`; operator-owned drift, not a lane defect | PASS (noted) |
| Marker predicate | report substance | real report, five landed commits, evidence pointers throughout | not a marker |

Dispatch/complete digest (copied from `.ufo/watchdog.log`):
`2026-11-04T01:15:01-03:00 launch tsukuroi round=75 pgid=1836578 driver=hyaku-inline attempt=1`;
`2026-11-04T01:36:55-03:00 complete tsukuroi round=75; hyaku-inline attempt=1`. No lane-dead line
for this round.

## 2. Per-claim re-check (closure-run measurements over committed bytes; lane gates not executed)

### C1 depth — mechanical target reproduces; literal frozen clause independently FALSIFIED

```
$ grep -cE '^\| *JT[1-6] ' corpus/knowledge/systemd-job-transaction-plane-r75.md
6
$ (cd .ufo/waves/round-75/before/src && sha256sum -c SHA256SUMS)
transaction.c: OK
job.c: OK
job.h: OK
$ git cat-file -e a21302a4:corpus/knowledge/systemd-job-transaction-plane-r75.md; echo rc=$?
rc=128
```

The six quote cells locate verbatim in their snapshots (whitespace-normalized, closure-run):
JT1 job.c FOUND, JT2 job.c FOUND, JT3 job.h FOUND, JT4 job.h FOUND, JT5 transaction.c FOUND,
JT6 transaction.c FOUND. Three sources (`S314`, `S315`, `S316`), three snapshots, no malformed row
(`awk -F'|' '/^\| *JT[1-6] / && NF!=8'` → 0). The report's `JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3
JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1` values reproduce by plain counts.

Literal-claim falsification (closure-read of the pinned snapshot):

```
$ grep -n "only as TRY_RESTART" .ufo/waves/round-75/before/src/transaction.c
1203:                        /* We propagate RESTART only as TRY_RESTART, in order not to start dependencies that
$ grep -n "type = JOB_RESTART;" .ufo/waves/round-75/before/src/transaction.c
1019:                        type = JOB_RESTART;
```

The `:1203` comment belongs to the `UNIT_ATOM_PROPAGATE_STOP` branch (`:1199-1217`). The later
`UNIT_ATOM_PROPAGATE_STOP_GRACEFUL` branch (`:1220-1247`) calls `job_type_propagate_stop_graceful`
(`:999-1027`), which returns `JOB_RESTART` at `:1019` when a `JOB_START` is already in the
transaction. The frozen C1 sentence's unqualified "propagating restart only as try-restart" is
therefore false; the note's JT6 row and `SCORECARD.md` erratum `R75-DECL-PROPAGATE-SCOPE` state both
branches. **C1 is not verified as declared**; the lane claims no depth uplift (depth stays 8).

Gate standard (Closure consequence): the lane gate was **not executed** by this closure. Its
committed evidence was verified: instrument sha256 `5e87238ce6909823797446b5be79194e2f701de46d3c4087ca75f289fca8cd71`
at both `1e2bb29c` and `bd0acc44`; `--selftest` 13 cases (read in the committed tool and in
`after/measure-final.txt`); base `JT_MAP absent` rc 128 in `before/absence-controls.txt`; after
receipts at `c15fe829`, `71ab09f4` and `e5f5ca9e` print the predicate rc 0. The after receipt
names `e5f5ca9e`, not `bd0acc44` (defect 4); the byte delta is the receipt commit only, and the
closure's plain counts at `bd0acc44` are unchanged.

### C2 freshness — four r74 routed defects close; verified

```
base a21302a4:                       tip bd0acc44:
R74-DEATH-RECEIPT-MISSING 0          R74-DEATH-RECEIPT-MISSING 1
R74-REPORT-WORDING 0                 R74-REPORT-WORDING 3
R74-SWEEP-RESIDUE 0                  R74-SWEEP-RESIDUE 1
Round 75 — axes table restated 0     Round 75 — axes table restated 2
```

Each token block carries a supersede verb inside the frozen 80-line window: the death-receipt and
wording blocks live in `corpus/lessons/round-74.md` with explicit `supersedes`/`erratum` wording; the
sweep-residue block in `.ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt` quotes both the
fabricated OID `d749a625f483c66f2a6f2005db3799630c776bc3` and the resolving real OID
`d749a625b3054b7cb3435983fb9626ab3d0ed0c4`; the `SCORECARD.md` axes block has six owned-axis rows,
each with a backticked counting command, and says it supersedes the round-65 table. The r74 seat
death evidence (`w1-results.json` SC3Index `output: ""`, `note: null`) and the 27552-byte
`w1/SC3Index/report.md` both exist as the appended corrections state.

Instrument evidence: sha256 `4b5c801ce4be7ea7562d9b472ce58badcd113d1062280220500275730f567d2c` at
declaration and tip; `--selftest` 13 cases; `before/absence-controls.txt` reads
`ROUTED_STALE=4 ROUTED_OK=0/4` rc 1; `after/measure-final.txt` reads `ROUTED_STALE=0 ROUTED_OK=4/4`
rc 0. Closure plain greps reproduce the same 0→1 token presence and the same verdict. **C2 verified.**

Supporting counts (closure-run over committed bytes): registry 313→317
(`git show <REV>:corpus/SOURCES.md | grep -cE '^ {0,3}\| *S[0-9]+ *\|'`), knowledge notes 92→93,
lesson files 124→125. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi` → `tsukuroi ok …`, exit 0 (pre-existing W04 duplicate-URL warnings only).

## 3. Discernment spot-check (LEARNING.md — non-author, this file)

| item | lane decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S314 admit (`transaction.c` v262) | admit, mined, tier A | `.ufo/waves/round-75/before/src/transaction.c:1203-1204`; digest `c1c704bb…`; `sha256sum -c` OK | **agree (admit); disagree (teaches cell)** | the located quote is verbatim and ≤25 words (16); the source is tier A/code. The `teaches` cell's "restart propagates only as try-restart" is over-broad: the graceful branch (`:999-1027`, called at `:1220-1247`) may enqueue a direct `JOB_RESTART` — the same clause the round's erratum overturns. Routed defect 1 |
| S315 admit (`job.c` v262) | admit, mined, tier A | `.ufo/waves/round-75/before/src/job.c:399`; digest `024a1acc…`; `sha256sum -c` OK | **agree** | quote "Merging is commutative, so imagine the matrix as symmetric. We store only" is verbatim at :399, 12 words; grounds JT1/JT2 |
| S316 admit (`job.h` v262) | admit, mined, tier A | `.ufo/waves/round-75/before/src/job.h:33`; digest `22d7b942…`; `sha256sum -c` OK | **agree** | quote "JOB_TRY_RESTART can never appear in a transaction, because" is verbatim at :33, 9 words; grounds JT3/JT4 |
| S317 reject (`systemctl(1)` manual) | reject, tier A/docs | saved HTML `.ufo/waves/round-75/w1/SC2Sources/systemctl.1.html:72-73` (sha256 `406c79cf…`); `grep -n "single job transaction"` → `:402` | **agree** | the DESCRIPTION quote is verbatim, 17 words; the manual's one transaction sentence (`:402`) is orderedness/CLI surface, narrower than merge, collapse or activation rules; the stated flip condition is sound |
| SOURCES row shape (new rows S314-S317) | 4 rows, all tier A; 3 mined, 1 rejected | `sources-census.sh validate` exit 0; `grep -nE '^\| *S31[4-7] *\|'` → four NF=13 rows; `used-by` path exists for mined rows | **agree** | rows are contract-shaped, no `|` in cells, dates/cadence valid, quote word counts 16/12/9/17 ≤25. The S314 `teaches` wording is the one disagreement (defect 1) |

Spot-check result: **3 admits + 1 reject re-opened; gate decisions agree; one row-level wording
disagreement (S314 `teaches`) is routed.** Discernment is checked from outside this round by this
closure.

## 4. Wave accounting (corroborated from committed spec/results)

12 seats, roles {scout 1, executor 3, scribe 3, connector 1, reviewer 2, critic 1,
mutation-tester 1}; band 8–16 (spawn 12); strict attack 4/12 = 33 % (R1Reviewer, R2Reviewer,
K1Critic, M1Mutation); connector 1; L1 held the planner seat; residual 0; spec and dispatch under
`.ufo/waves/round-75/`; `w1-results.json` has 12 results, all `output` nonempty (no dead seat), no
replacement. Matches the report.

## 5. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth | unchanged | C1's mechanical target reproduces, but the frozen literal clause is falsified; honest stop, no uplift (8 → 8) |
| coverage | unchanged | no coverage claim; registry growth is expansion, not new surface coverage |
| operability | unchanged | no capability row; the two new gates are claim instruments registered in `SKILL.md`, not repertoire entries; census selftest 218 carried |
| freshness | **improved** | all four r74 routed defects close append-only (base/tip token 0→1, supersede verbs present); checker evidence 4→0 stale |
| calibration | unchanged | strong self-catch (C1 refused; limits named), append-only SCORECARD; the report's "six mistakes" / "no admitted artifact" overstatements are defects 1-3, not an ordinal move |
| adjacency | unchanged | C1Connector scanned 20 sibling repos; no absorption; boundaries restated |

No owned axis harmed: `git diff --numstat a21302a4 bd0acc44` = 99 files, **13511 insertions, 0
deletions**; `SCORECARD.md` = 91/0; LOG/PROVINCE/SKILL/README/QUALITY are appends only.

## 6. Trend verdicts

- **expansion: improved.** One new sourced knowledge entry on verified-new ground (held-ground sweep
  0 matches at base, `before/held-ground.txt`), three mined tier-A code snapshots plus one measured
  documentation refusal, registry 313→317 and notes 92→93 closure-counted, census exit 0.
- **quality: improved.** Six true JT rows with an independent reviewer pass and two append-only
  errata; two gates with hermetic 13-case selftests, registered rows and frozen digests; four
  in-wave defects corrected before landing; the four r74 stale items close. The S314 `teaches`
  over-broad clause and the JT5 "nine comma items" miscount are corrections-sweep/count defects
  (routed 1-2); the admitted knowledge entry itself is true, so the corpus quality signal improved,
  but the report's "no admitted artifact is left failing its own re-check" is overstated (defect 6).
- **discernment: improved.** The outside check of round 74 (four routed defects) is closed with
  committed bytes; the round refused its own C1 claim rather than let a lexical PASS stand; QUALITY
  108 makes correction propagation a standing obligation; the Gate's 3 admits and 1 reject re-open
  and agree. The S314 `teaches` disagreement is row-level, not a gate-decision reversal, and is
  routed.

## 7. Routed defects for the lane's next round

1. **S314 `teaches` is over-broad.** The new row says "restart propagates only as try-restart"; the
   pinned graceful branch may enqueue a direct `JOB_RESTART` (`transaction.c:999-1027,1220-1247`).
   Append a superseding SOURCES row (contract rule 2 — `teaches` opens `supersedes S314 —`) scoped to
   the `PROPAGATE_STOP` branch and naming the graceful branch; add this corrected proposition to the
   QUALITY 108 propagation map, whose three propositions omit it.
2. **JT5 erratum count.** `corpus/knowledge/systemd-job-transaction-plane-r75.md` says the JT5 row
   "compresses the list into nine comma items"; the row has eight comma-separated items (ten labels
   after splitting the two compound items). Correct the count or state the split-count method.
3. **Mistake count.** The report says "six mined mistakes"; `corpus/lessons/round-75.md` `## Mistakes`
   has five rows (plus two owed rows) and `LOG.md` says five. Reconcile the count and carry its
   counting command.
4. **Measured-revision / receipt pointer.** `after/measure-final.txt` heads `e5f5ca9e`, while the
   report's after column says `bd0acc44`; the base `JT_MAP absent` control is in
   `before/absence-controls.txt`, not in the after receipt the report names. Re-run and record the
   gates at the cited tip, or cite the measured revision explicitly.
5. **Untracked wave markers.** `round-75/w1.ready` and `round-75/w1.ready.dispatched` (plus carried
   r66/r67/r73/r74 `.ready.dispatched` and `w1-run.stderr`) remain untracked; classify them as
   runtime markers in the report or clean/commit them. Not lane round work.
6. **Quality evidence wording.** "No admitted artifact is left failing its own re-check" is
   contradicted by defect 1 (and the defect-2 count); say "no admitted knowledge entry" or enumerate
   the carriers.

**Operator note (not a lane defect):** all four `SHONEN.md` boxes still look fully checkable by a
non-author — box 1 (SKILL r75 diagnosis table + JT1-JT6 + S314-S316), box 2 (logged read-only host
probe with receipts), box 3 (twelve seats executed the note/counter; the whole-SKILL
no-oral-context retest remains the open round-60 L0 item), box 4 (connector scan clean). Promotion
review is operator-owned; no `[x]` was written by this closure.

Closure grade: round **rejected-honest-stop** (C1 literal claim falsified; C2 verified; no axis
harmed; the routed items are wording/count/evidence-pointer level and do not rescue the C1 miss).
