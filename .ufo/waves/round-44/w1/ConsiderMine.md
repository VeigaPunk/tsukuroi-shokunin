VERDICT: draft

# F-7 — considerthese proposal mined: **Seat-harm incident log**

Report: `.ufo/waves/round-44/w1/ConsiderMine.md` (this file). Receipts:
`.ufo/waves/round-44/w1/ConsiderMine/` (300 KB total). Read 2026-10-26.

## 1. Which proposal, and why this one

Survey of `considerthese/2026-10-26.md` §"Self-improvement ideas" against the lane, in file order
(receipt `w1/ConsiderMine/proposal-survey.txt`):

| # | Proposal | Status in the lane | Evidence |
|---|---|---|---|
| 1 | Burst-aware reading | **not implemented** (0 hits in `SKILL.md`, 0 in `corpus/lessons/`) | `grep -ric burst SKILL.md` → 0; `grep -rc burst corpus/lessons/` → 0 |
| 2 | Counter-attack scoreboard | implemented | `SKILL.md:3833` "## Counter-attack scoreboard — rounds 40-41", `SKILL.md:3935` (round-42 continuation), `corpus/lessons/round-41.md:99` |
| 3 | Seat-harm incident log | **not implemented** (0 hits) | `grep -rc seat-harm SKILL.md corpus/lessons/` → 0/0 |
| 4 | Downstream patch-offset check | implemented | `corpus/lessons/round-42.md:53`, notes appended at `corpus/knowledge/pacman-hook-order-r38.md:159`, `pacman-transaction-order-r39.md:87`, `alpm-package-anatomy-r41.md:104`; `SCORECARD.md:2611` |
| 5 | Cross-note correction propagation map | mined in round 43 | `corpus/lessons/round-43.md:83` (section headed "proposal 5, read 2026-10-26") |

Proposal 1 is unimplemented, but it is a change to how a *daily reflection* is read (its own sibling,
`considerthese/2026-10-23.md:18` "Round-velocity awareness in this review", is the same unbuilt family), and no round-44
surface grounds it: there is no reflection seat in this wave and no tool in the lane that reads a window. Proposal 3 is
the first unimplemented proposal **this round's surfaces can ground**, and the item names it. Grounding surfaces used,
all from this round:

- the guard text this wave hands every seat (`make-w1-spec.py:36`, "Signal only processes you started (by PID);
  never `pkill`/`killall`", and `:35`, "never create files at the fleet root … is a misroot");
- the frozen counters' argument contract (`tools/score-scrub-arm-r44.py:514`, `--scratch` required);
- the round's own scratch root and lane residue (`ls-r44-scratch-root.txt`, `lane-pycache-red.txt`);
- a round-44 seat's own misroot disclosure (`.ufo/waves/round-44/w1/C1ExecEdgeNames.md:243-251`).

Proposal 1 is left open for the next reflection; it is not silently dropped.

## 2. What was built (not prose — a checked ledger)

`.ufo/waves/round-44/w1/ConsiderMine/`:

| File | sha256 (first 24) | Purpose |
|---|---|---|
| `seat-harm.jsonl` (7642 B) | `a1e92e9d5efc95b1bc8ca8be` | 8 incident rows, rounds 37-44 |
| `seat-harm-log.py` (11811 B) | `dc8f9dc442a6a457e3192dbf` | checker + per-round tally; read-only, no host query |
| `make-mutants.py` (3311 B) | `f7e5ccd70f5d7731b39e50ca` | one-field mutants of the ledger |
| `run-mutants.py` (2282 B) | `6446996d4ee1da224cdca11d` | mutant driver, writes `mutants/results.json` |
| `mutants/` (13 JSONL + `run.txt`, `results.json`) | — | 13 mutants, 0 survivors |
| `pycache-header-check.txt` | `70f1964ff28d81f1a18bba05` | the three `.pyc` headers vs their sources (`MATCH=True` ×3) |
| `guard-presence.txt`, `scratch-required-red.txt`, `ls-r44-scratch-root.txt`, `fleet-misroot-sweep.txt`, `lane-pycache-red.txt`, `scan-ids.txt`, `proposal-survey.txt`, `run.txt` | — | the measurements each ledger row's fix or state rests on |

Row contract (enforced, not decorative):

- `kind:"lesson"` — `cite` is `path:line` inside the lane and that line must carry the row `id` **and** the `quote`
  verbatim; ids minted in round 44 (`id_basis:"minted"`, no lesson exists yet) are instead required to be *absent* from
  `corpus/lessons/` (`SH-ID-ALREADY-IN-LESSONS`), so a minted id cannot quietly reuse a landed one.
- `kind:"observation"` — the evidence is a committed receipt, checked by sha256; the ephemeral origin
  (`tools/__pycache__/<f>.pyc`, its size and mtime) is a field, never a citation.
- Every row records the isolation state when it landed (`landing`) and today (`today`); `closed-able-to-fail` is
  refused without a non-empty `fix_quote` found on its `fix_cite` line (`SH-CLOSED-NO-PROOF`).
- Citations must be lane-relative: an absolute, `/tmp` or `/fast/scratch` path is a finding.

Run:

```
$ python3 seat-harm-log.py --log seat-harm.jsonl
round  incidents  (seat-harm ledger, window 37-44)
  37  1  R37-MISROOT-NOTE-DRAFT
  38  0
  39  1  R39-SEAT-PKILL
  40  1  R40-TMP-MISROOT
  41  1  R41-TMP-MISROOT-REPEAT
  42  1  R42-C1-SCRATCH-FALLBACK-TMP
  43  1  R43-L1-SCRATCH-STRAY
  44  2  R44-FLEETROOT-FX,R44-PYCACHE-RECUR
classes: fleet-root-write=2, lane-pollution=1, process-signal=1, scratch-tmp=3, shared-scratch-stray=1
harms:   fleet-repo=2, host-disk=3, lane-tree=2, other-seat-run=1, shared-round-root=1
today:   closed-able-to-fail=3, detector-only=2, open=2, rule-only=1
open:    R43-L1-SCRATCH-STRAY, R44-PYCACHE-RECUR
PASS: rows=8 findings=0
```
(`w1/ConsiderMine/run.txt`, exit 0.)

Able to fail (`mutants/run.txt`, exit 0): baseline `rows=8 findings=0`, then 13 single-field mutants, each turning
exactly the expected check red — `K01` cite line drift → `SH-CITE-QUOTE`; `K02` paraphrased quote → `SH-CITE-QUOTE`;
`K03` invented id → `SH-ID-NOT-ON-LINE`; `K04` unknown class → `SH-CLASS-UNKNOWN`; `K05` duplicate id →
`SH-ID-DUPLICATE`; `K06` closure without proof → `SH-CLOSED-NO-PROOF`; `K07` round 30 → `SH-ROUND-OUT-OF-WINDOW`;
`K08` missing file → `SH-CITE-MISSING`; `K09` invented fix quote → `SH-FIX-QUOTE`; `K10` tampered obs sha →
`SH-OBS-SHA`; `K11` `/tmp` citation → `SH-FIX-ABSOLUTE`; `K12` unknown id basis → `SH-ID-BASIS`; `K13` minted id
reusing a landed one → `SH-ID-ALREADY-IN-LESSONS`. `killed=13/13 survived=none`.

Population the classification starts from: every lesson-table id of rounds 37-43, 54 rows, 54 unique ids
(`w1/ConsiderMine/scan-ids.txt`). Six of them are seat harm; the classification of each is in the ledger.

## 3. The answer the proposal wanted: are isolation fixes landing?

| Class (n) | Landed as | Today | The receipt that decides it |
|---|---|---|---|
| `process-signal` (1) | none | **rule-only** | Rule text present in every wave context r40-r44 and 0 in the r39 context (`guard-presence.txt`: `round-40…44 make-w1-spec.py: 1 occurrence(s)`, `round-39 …: 0`). No receipt shows a seat stopped by it. |
| `scratch-tmp` (3) | routed (r40, r42), closed (r41) | **closed-able-to-fail** | `--scratch` required from r43 and both counters exit 2 without it (`scratch-required-red.txt`); r41 receipt green/red (`round-41/w1/RoutedSelfAssessScratch.md:40-41`). |
| `fleet-root-write` (2) | repair (r37, r44) | **detector-only** | Fleet porcelain red while the file exists, `FLEET_STATUS_LINES=0` after quarantine (`fleet-misroot-sweep.txt`); `round-37.md:102` "The red sweep (`?? corpus/`) shows the check can fail". |
| `shared-scratch-stray` (1) | repair | **open** (stray half closed) | Round-44 root holds only per-seat directories, L1 scratch under `…/tsukuroi-r44/L1/`, `STRAY_FILES=0` (`ls-r44-scratch-root.txt`); the lane half recurred. |
| `lane-pollution` (1) | none (fix authored in r43, not adopted) | **open** | 3 `tools/__pycache__/*.pyc` at 21:11:05, 21:11:09, 21:22:33 of this wave; `git status` shows 0 of them (`lane-pycache-red.txt`; bytes kept in `pycache/`). The bytes are genuine — all three headers match their source mtime and size (`pycache-header-check.txt`, `MATCH=True` ×3), one of them stamping a source last modified 2026-10-23 — so no verdict is affected, but the loader habit predates the round. The one-line fix was already written in r43 (`.ufo/waves/round-43/w1/SentMisroot.md:49`, `export PYTHONDONTWRITEBYTECODE=1`, plus a sweep widened with `--ignored` and `find` at `:55`); the round-44 guard does not carry it. |

Two findings I can defend:

1. **The fixes that hold are the ones carried by a tool argument or a per-seat path; the fixes that are prose do not.**
   `R44-FLEETROOT-FX` landed seven rounds after `R37-MISROOT-NOTE-DRAFT` while the guard already said "never create
   files at the fleet root (a shell redirect such as `>=` or `> T` there is a misroot)" (`make-w1-spec.py:35`) — a
   sentence that names redirects and not the case that actually fired, `dev0 "$PWD/fx/…"` with cwd at the fleet root
   (`C1ExecEdgeNames.md:245-246`). The `--scratch` fix and the `…/<seat>/` scratch rule stopped their classes
   recurring from r43 onward; nothing recurred in `process-signal` either, but that class has *no* receipt of the rule
   firing, so it must not be counted as landed.
2. **A `.gitignore`d path is invisible to every sweep the wave runs.** Both the r37 class detector (fleet porcelain)
   and the lane sweep read `git status`; `__pycache__/` is ignored (`.gitignore:2`), so the r43 lane half recurred in
   round 44 with `R43-L1-SCRATCH-STRAY` itself marked "fixed". The only check that sees it is a `find` over the lane.
   The strongest instance is the same shape one level up: the r43 sentinel had already written the exact remediation
   into its report — `export PYTHONDONTWRITEBYTECODE=1` and a sweep widened to ignored paths — and one round later the
   residue is back, because a fix in a report is still prose. A seat report is not an adoption.

## 4. Boundary, and what I did not do

- **Scope held to seat-to-seat harm.** Adjacent ids excluded, with reason, so this is not a silent filter:
  `R41-CAPTURE-FIFO` (an orphaned `cp` blocked 2 h 10 min until the L1 killed it — one seat's own process),
  `R42-COUNTER-SIGINT-LEAK` (91 entries in the counter's own run root — own residue), `R37-SEAT-REPORT-COUNT`
  (a count drift, no harm), `R43-SIB-PIN-UNREPORTED` (a sibling lane's pin, no host harm). A wider ledger would
  need its own class names; I did not widen this one.
- **Nothing was executed on the host.** No counter was run (the C1 counter ~30 s and 2-4 CPUs was not needed for this
  item; the `--scratch` refusal receipt ran argparse only, exit 2, before any work). No package, service, timer,
  sysfs, mount, scrub or sudo action. No lane file was created, edited or deleted; `git` on the lane and the fleet
  root was read-only with `GIT_OPTIONAL_LOCKS=0` (fleet root: `FLEET_STATUS_LINES=0`, `fleet-misroot-sweep.txt`).
- **What is not proven.** (a) The tally is bounded by the lesson tables I enumerated: an incident that no seat
  disclosed and no lesson recorded is invisible to it — the ledger counts disclosures, not physics. (b) `process-signal`
  remains `rule-only`: I did not build an arm that makes a seat signal a sibling, and I did not run one. (c) The
  checker resolves citations against the working tree at `--lane`; it does not bind a revision (`_revision`), so the
  L1 should run it on a clone checked out at the landing commit if it is to be quoted as evidence at a revision.
  (d) My own run added no bytecode to the lane (`find tools -name '*.pyc' | wc -l` stayed 3; `PYTHONDONTWRITEBYTECODE=1`
  and `sys.dont_write_bytecode = True`). (e) The r44 sentinel (`SentMisroot`) independently reproduced the `.pyc` count
  and called it a recurrence rather than r43 residue (peer message, 2026-10-26); its moving-count detail (the directory
  held ~18 files earlier in the wave) is peer-reported, not measured by me — what I measured is the three files, their
  mtimes and their headers. (f) The fleet-root sweep is a timestamped measurement, not a standing
  claim: a recheck later in this seat's run lists `?? .ufo/reports/round-52/mori.md` (9327 B, 21:28), another lane's
  report with no tsukuroi name in it, left untouched (`fleet-misroot-sweep.txt` now carries both readings).

## 5. Exact proposed text

### 5a. Lesson section for `corpus/lessons/round-44.md`

```markdown
### considerthese — seat-harm incident log (`considerthese/2026-10-26.md`, proposal "Seat-harm incident log")

Mined: "Seat-to-seat damage on the shared host (pkill, `/tmp` misroot, the round-37 fleet-root misroot) is now a
recurring class separate from seat loss. A running tally per round would show whether isolation fixes are actually
landing." Built as a checked ledger, not a table drawn from memory: eight incidents over rounds 37-44, each row bound
to the lane bytes carrying it (the cited `corpus/lessons/<file>:<line>` must contain the row id and its quoted
fragment verbatim; a round-44 id is minted and must therefore *not* already exist in `corpus/lessons/`). Receipts:
`.ufo/waves/round-44/w1/ConsiderMine/` — `seat-harm.jsonl` (8 rows), `seat-harm-log.py` (checker + tally),
`make-mutants.py`/`run-mutants.py` (13 mutants, `killed=13/13 survived=none`), `scan-ids.txt` (the 54 lesson ids of
rounds 37-43 the classification starts from).

| Round | Incidents | Ids |
|---|---|---|
| 37 | 1 | `R37-MISROOT-NOTE-DRAFT` |
| 38 | 0 | — |
| 39 | 1 | `R39-SEAT-PKILL` |
| 40 | 1 | `R40-TMP-MISROOT` |
| 41 | 1 | `R41-TMP-MISROOT-REPEAT` |
| 42 | 1 | `R42-C1-SCRATCH-FALLBACK-TMP` |
| 43 | 1 (2 harms) | `R43-L1-SCRATCH-STRAY` |
| 44 (partial) | 2 | `R44-FLEETROOT-FX`, `R44-PYCACHE-RECUR` |

| Class (n) | Landed as | Today | Deciding receipt |
|---|---|---|---|
| `process-signal` (1) | none | rule-only | rule present in every wave context r40-r44, 0 in the r39 context (`guard-presence.txt`); no receipt shows it firing |
| `scratch-tmp` (3) | routed ×2, closed ×1 | closed-able-to-fail | `--scratch` required from r43, both counters exit 2 without it (`scratch-required-red.txt`); r41 red/green receipt |
| `fleet-root-write` (2) | repair ×2 | detector-only | fleet porcelain red while the file exists, 0 lines after quarantine (`fleet-misroot-sweep.txt`) |
| `shared-scratch-stray` (1) | repair | open (stray half closed) | round-44 root: only per-seat directories, L1 under `L1/`, `STRAY_FILES=0` (`ls-r44-scratch-root.txt`) |
| `lane-pollution` (1) | none (fix authored in r43, not adopted) | open | 3 `tools/__pycache__/*.pyc` written during this wave, invisible to `git status` (`lane-pycache-red.txt`, bytes in `pycache/`); headers match their sources (`pycache-header-check.txt`), so the bytes are genuine and the cost is the blind sweep |

Reading: the classes that stopped recurring are the ones whose fix is a tool argument or a per-seat path; the prose
rules did not stop theirs. `R44-FLEETROOT-FX` repeated `R37-MISROOT-NOTE-DRAFT` seven rounds later while the guard
already said "never create files at the fleet root (a shell redirect such as `>=` or `> T` there is a misroot)"
(`make-w1-spec.py:35`) — the sentence named redirects, and the case that fired was `dev0 "$PWD/fx/…"` with cwd at
the fleet root (`w1/C1ExecEdgeNames.md:245-246`). `process-signal` has no incident since round 39, but a rule with no
receipt is not a landed fix. Rule: a seat-harm fix counts as landed only with a receipt in which the old shape is red
and the new shape green; a prose rule is `rule-only` and is counted as open in the tally. Corollary from the lane
half: a `.gitignore`d path cannot be swept by `git status`, so a lane-residue check must be a `find` over the
worktree, not a porcelain line, and the two lines that stop the class are already written
(`w1/SentMisroot.md:49` `export PYTHONDONTWRITEBYTECODE=1`; `:55` `git status --porcelain --ignored`) — they need the
dispatch shell, not another report.
```

### 5b. Optional `SKILL.md` section (if the L1 wants the tally operative rather than lesson-bound)

```markdown
## Seat-harm ledger — rounds 37-44

Appended 2026-10-26 (round 44; `considerthese/2026-10-26.md` proposal "Seat-harm incident log": "A running tally per
round would show whether isolation fixes are actually landing"). One row per seat-to-seat incident, checked by
`w1/ConsiderMine/seat-harm-log.py --log w1/ConsiderMine/seat-harm.jsonl`: a row stands only if the cited lesson line
carries its id and quote verbatim, and `closed-able-to-fail` is refused without a fix quote that resolves.

| Round | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 |
|---|---|---|---|---|---|---|---|---|
| Incidents | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 2 |
| Closed with a red/green receipt | 0 | — | 0 | 1 | 1 | 1 | 0 | 0 |

States today: 3 `closed-able-to-fail`, 2 `detector-only` (`R37-MISROOT-NOTE-DRAFT`, `R44-FLEETROOT-FX`), 1
`rule-only` (`R39-SEAT-PKILL`), 2 `open` (`R43-L1-SCRATCH-STRAY` lane half, `R44-PYCACHE-RECUR`). Rule: prose in the
wave context is `rule-only` and counts as open until a receipt shows the old shape red.
```

### 5c. Promotion note (only if the L1 adopts it as a lane tool)

The checker is wave-dir evidence like `w1/ConsiderPatchOffset/patch-offset.py` (round 42), so it needs no registry
row as it stands. Promoting it to `tools/check-seat-harm-log.py` requires, in the same commit, a `--self-test` flag
(the registry's `SELFTEST_FLAG` regex is `--self-?test(?:-[A-Za-z0-9-]+)?`) and a row under the next
"## Gate and probe registry — roundNN superseding current rows" heading with the eight columns
`Name, Kind, Entry command, Verdict map, Self-test, Pinned values, Write scope, Owner`
(`tools/check-registry-coverage.py:49-52`) — the round-38 `R38-REGISTRY-LAG` class. Its verdicts are already
0/1/2 and its write scope is `none`.

## 6. Host guard compliance

- Writes: only `tsukuroi-shokunin/.ufo/waves/round-44/w1/ConsiderMine.md` and
  `tsukuroi-shokunin/.ufo/waves/round-44/w1/ConsiderMine/`. No fleet-root file, no PATH directory, no shim, no lane
  tracked file, no `git add/commit/stash/checkout/reset/push`, no jj command.
- Scratch: none needed — no clone, fixture, mutant tree or archive was built outside the lane seat dir (the mutants
  are 8-row JSONL files under 8 KB). `TMPDIR` was never used; no `/tmp` path appears as evidence.
- Host: no sudo, no pacman (transactions paused; nothing installed or upgraded), no service/timer/sysfs/mount/scrub
  action; read-only queries only (`git status` with `GIT_OPTIONAL_LOCKS=0`, `find`, `grep`, `stat`, `sha256sum`, and
  one `python3 <counter> --revision …` invocation per counter that argv-rejected before any work, exit 2).
- No agents spawned, no swarm, no `agent://all`. One peer message to `SentMisroot` (the wave's own sentinel) with the
  `.pyc` count and its sha256 receipts, so its X-5 sweep is not blind to the ignored path.
