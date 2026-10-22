# Round 25, wave 1 — MutSelfAssessPlan: C1 mutation-fixture set

Seat: `MutSelfAssessPlan` (mutation tester). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scope: C1 only — the mutation-fixture set for `tools/check-self-assessment.py`.
C2 (memory pressure, MP1 to MP6) is out of scope and untouched.

## Verdict

The C1 mutation-fixture set is delivered and executed: 33 fixtures covering all
23 declared checks K01 to K23, and the checker under test was run read-only
against one throwaway git repo per fixture. **32 of the 32 defect fixtures were
killed** (the checker reported exactly the expected check id and nothing else);
**the one control fixture behaved as a control must** (an earlier, non-last
`## Axes — ` heading produced no mismatch, exit 0). Zero survivors, zero
inconclusive runs, zero baseline failures. The pristine baseline reports
`mismatches` 0 and exit 0.

## 1. What was delivered

Three artifacts, all inside this seat's own directory
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutSelfAssessPlan/`:

| File | What it is |
|---|---|
| `generate_fixtures.py` | Materialises the fixtures for a given revision. Two baseline modes: `computed` (the baseline axes/Capabilities tables are synthesised from values measured at that revision) and `landed` (the baseline tables are taken verbatim from the revision's own files, which is the mode that matters once the lane's repaired table lands). Every mutation is a regex substitution, so the same mutation set works in both modes. |
| `run_mutations.py` | Builds one throwaway git repo per fixture, applies the baseline and then the fixture, commits, runs the checker, and records killed/survived with the checker's own reason strings. |
| `run_wave2.sh` | One-command wave-2 runner: regenerates the fixtures for a revision, runs them, prints the summary. `TOOL=` points it at the checker, `MODE=landed` switches the baseline mode. |

The materialised fixture set lives at
`/fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/fixtures/` (33 directories,
one per fixture, each with the mutated section file and a `meta.json`), with
`manifest.json` indexing all of them and `baseline/` holding the pristine
sections. The machine-readable run record is
`/fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/results.json`.

## 2. The checker under test

The executor's checkout
`/fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/repo/tools/check-self-assessment.py`,
sha256 `970e3efb4e21071e0bf8db19c8783e3b9bdb39ff075f8df29a6049f31e6d4a33`,
copied to `/fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/tool-under-test.py`
before the run so the bytes under test are pinned against further executor
edits. The lane copy of the tool did not exist at the time of this run.

The executor published the contract in a peer message; my fixtures were built
against it and independently confirmed by reading the tool source
(`tools/check-self-assessment.py:34-40` axes and capability names, `:99-129`
path listing, `:267-295` path resolution, `:454-465` the case-count grammar,
`:467-611` the K07 to K19 checks, `:612-650` the K20 to K23 checks). One
difference between the published contract and the pinned bytes is worth
recording: the published text says a row or box that names no path is a
mismatch, and the pinned bytes implement exactly that, but the pinned bytes
also resolve a bare filename against the directory of the nearest preceding
qualified path in the same list (`resolve_paths`, `:267-290`). That resolution
is why the lane's own `after.md` citation in the `host-census-gate` row does
not trip K17.

## 3. Method

1. The lane was read with `git archive` and `git show` only. The lane working
   tree was never written, and no lane git write command was issued.
2. For each fixture a fresh directory was created under
   `/fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/repos/` with `git init`
   and **no remote configured**, so no scratch commit can reach the lane. The
   revision's tree was unpacked with `git archive`, the baseline sections were
   overlaid, the fixture's section was overlaid on top, and the result was
   committed locally.
3. The checker was then run inside that repo as
   `python3 tools/check-self-assessment.py --revision <commit>`.
4. A mutant is **killed** when the checker reports a mismatch on the fixture's
   expected check id, and **survived** when it does not. The pristine baseline
   is run first; a baseline failure would have made every run inconclusive, so
   the baseline is reported explicitly.

## 4. Results

Baseline (pristine, baseline sections applied, no fixture): **exit 0,
`mismatches` 0, no check id mismatching.**

32 defect fixtures, all killed. Each killed fixture reports `mismatches` exactly
1 and exactly the expected check id — no fixture tripped an unrelated check,
and no fixture produced a false extra trip.

| Fixture | Check | Kind | Verdict |
|---|---|---|---|
| M01-ordinal-depth | K01 | ordinal one off | killed |
| M02-ordinal-coverage | K02 | ordinal one off | killed |
| M03-ordinal-operability | K03 | ordinal one off | killed |
| M04-ordinal-freshness | K04 | ordinal one off | killed |
| M05-ordinal-calibration | K05 | ordinal one off | killed |
| M06-ordinal-adjacency | K06 | ordinal one off | killed |
| M07-count-notes | K07 | count one off | killed |
| M08-count-skill-lines | K08 | count one off | killed |
| M09-count-table-lines | K09 | count one off | killed |
| M10-count-lessons | K10 | count one off | killed |
| M11-count-readme-lines | K11 | count one off | killed |
| M12-stale-province | K12 | stale phrase | killed |
| M13-count-cases | K13 | count one off | killed |
| M14-stale-identity | K14 | stale phrase | killed |
| M15-stale-overlap | K15 | stale phrase | killed |
| M15b-omit-overlap | K15 | omitted fact | killed |
| M16-capability-path-sources | K16 | broken capability path | killed |
| M17-capability-path-census | K17 | broken capability path | killed |
| M18-capability-path-metadata | K18 | broken capability path | killed |
| M19-capability-path-bootchain | K19 | broken capability path | killed |
| M20-shonen-box1-checked | K20 | SHONEN `[x]` without verifier | killed |
| M21-shonen-box2-path | K21 | broken path | killed |
| M22-shonen-box3-path | K22 | broken path | killed |
| M23-shonen-box4-path | K23 | broken path | killed |
| M24-axes-second-heading-not-last | K01..K15 (selection) | second `## Axes — ` heading that is not last | **control** (no mismatch, exit 0 — correct) |
| M25-axes-second-heading-last | K01 | second `## Axes — ` heading that is last | killed |
| M26-axes-extra-pipe | K01 (row shape) | table row with an extra pipe | killed |
| M27-omit-province | K12 | omitted fact | killed |
| M28-omit-identity | K14 | omitted fact | killed |
| M29-capability-cases-off | K17 | count one off | killed |
| M30-capability-omit-cases | K17 | omitted fact | killed |
| M31-shonen-box1-no-path | K20 | omitted fact | killed |
| M32-shonen-box4-no-path | K23 | omitted fact | killed |

All 23 declared check ids K01 to K23 are covered by at least one fixture.

### 4.1 The checker's own reason string for every killed fixture

Each line is the checker's verbatim `reason` for the newly tripped check. Every
one names the specific defect, so no kill is unattributable.

| Fixture | Check | Checker's reason |
|---|---|---|
| M01-ordinal-depth | K01 | `axes table depth score 9 differs from the after-value 8 of the last recorded transition (SCORECARD.md:759)` |
| M02-ordinal-coverage | K02 | `axes table coverage score 8 differs from the after-value 9 of the last recorded transition (SCORECARD.md:224)` |
| M03-ordinal-operability | K03 | `axes table operability score 8 differs from the after-value 9 of the last recorded transition (SCORECARD.md:731)` |
| M04-ordinal-freshness | K04 | `axes table freshness score 8 differs from the after-value 9 of the last recorded transition (SCORECARD.md:772)` |
| M05-ordinal-calibration | K05 | `axes table calibration score 8 differs from the after-value 9 of the last recorded transition (SCORECARD.md:771)` |
| M06-ordinal-adjacency | K06 | `axes table adjacency score 9 differs from the after-value 8 of the last recorded transition (SCORECARD.md:620)` |
| M07-count-notes | K07 | `depth row states 47 notes; corpus/knowledge holds 46 .md files` |
| M08-count-skill-lines | K08 | `depth row states 2302 SKILL.md lines; SKILL.md holds 2301 newline characters` |
| M09-count-table-lines | K09 | `depth row states 260 table lines; SKILL.md holds 259 pipe-prefixed lines` |
| M10-count-lessons | K10 | `depth row states 26 lesson files; corpus/lessons holds 25 files` |
| M11-count-readme-lines | K11 | `coverage row states 232 corpus/README.md lines; the file holds 231 newline characters` |
| M12-stale-province | K12 | `coverage row states the sections are absent; PROVINCE.md holds Core=True Frontier=True Adjacent=True` |
| M13-count-cases | K13 | `operability row states 98 cases; the census selftest at this revision prints 97 cases (TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed))` |
| M14-stale-identity | K14 | `operability row states the mode is present; the census script holds a --identity case arm: False` |
| M15-stale-overlap | K15 | `adjacency row states the table is absent; PROVINCE.md holds a '\| ID \| Finding' table: True` |
| M15b-omit-overlap | K15 | `adjacency row states the table is unstated; PROVINCE.md holds a '\| ID \| Finding' table: True` |
| M16-capability-path-sources | K16 | `sources-registry row names 1 path(s) absent at the revision: corpus/SOURCES-registry.md` |
| M17-capability-path-census | K17 | `host-census-gate row names 1 path(s) absent at the revision: .ufo/evidence/round-1-kaika/scout-live-absent.md` |
| M18-capability-path-metadata | K18 | `root-metadata-observer row names 1 path(s) absent at the revision: .ufo/waves/round-12/resumed/absent-fixture.json` |
| M19-capability-path-bootchain | K19 | `boot-chain-audit row names 1 path(s) absent at the revision: .ufo/waves/round-17/l1-capture/absent-audit.txt` |
| M20-shonen-box1-checked | K20 | `SHONEN box 1 is marked [x] without a named non-author verifier` |
| M21-shonen-box2-path | K21 | `SHONEN box 2 names 1 path(s) absent at the revision: corpus/knowledge/absent-fixture.md` |
| M22-shonen-box3-path | K22 | `SHONEN box 3 names 1 path(s) absent at the revision: corpus/knowledge/absent-fixture.md` |
| M23-shonen-box4-path | K23 | `SHONEN box 4 names 1 path(s) absent at the revision: corpus/knowledge/absent-fixture.md` |
| M24-axes-second-heading-not-last | — | *no mismatch; exit 0 — the control behaved correctly* |
| M25-axes-second-heading-last | K01 | `axes table depth score 5 differs from the after-value 8 of the last recorded transition (SCORECARD.md:771)` |
| M26-axes-extra-pipe | K01 | `axes table depth row states no numeric score` |
| M27-omit-province | K12 | `coverage row states the sections are unstated; PROVINCE.md holds Core=True Frontier=True Adjacent=True` |
| M28-omit-identity | K14 | `operability row states the mode is unstated; the census script holds a --identity case arm: False` |
| M29-capability-cases-off | K17 | `host-census-gate row states 98 cases; the census selftest at this revision prints 97 cases` |
| M30-capability-omit-cases | K17 | `host-census-gate row states None cases; the census selftest at this revision prints 97 cases` |
| M31-shonen-box1-no-path | K20 | `SHONEN box 1 names no repository path` |
| M32-shonen-box4-no-path | K23 | `SHONEN box 4 names no repository path` |

[M30 is worth one word: the checker reports the stated case count as `None`
rather than skipping the comparison, which is the correct treatment of a row
that states no count at all.]

### 4.2 The defect kinds the assignment named, and how each is realised

- **An ordinal one off** — M01 to M06. The score cell of one axes row is set
  one off the last recorded ordinal transition for that axis. The offset is
  *relative*: the generator reads the recorded after-value with the declared
  K01 to K06 regex and writes `recorded ± 1`, so the fixture mismatches
  whichever value the checker itself derives rather than a value hard-coded
  here.
- **A count one off** — M07 to M11 (note count, SKILL.md line count, SKILL.md
  table-line count, corpus/lessons file count, corpus/README.md line count),
  M13 (census selftest case count in the operability row) and M29 (the same
  count in the Capabilities row).
- **A stale phrase** — M12, M14, M15. The coverage row's PROVINCE.md
  Core/Frontier/Adjacent statement, the operability row's `--identity`
  statement and the adjacency row's formal-overlap-table statement are each set
  to the token that *contradicts* the observed state. The direction is computed
  from the tree, not hard-coded, so the fixture is correct whether the lane
  lands the state or not.
- **An omitted fact** — M27, M28, M30, M15b, M31, M32. The statement is deleted
  outright, so the checker's stated value is `unstated`, which the declared
  grammar treats as a mismatch.
- **A broken capability path** — M16 to M19. One backticked span inside each
  of the four Capabilities rows is pointed at a path that does not exist at the
  revision. The span is chosen from the row's own backticked spans, because
  the declared grammar reads Capabilities cells from backticked spans.
- **A SHONEN `[x]` without verifier** — M20. Box 1's marker is flipped from
  `[~]` to `[x]` while its text still says non-author verification is owed and
  names no `non-author verifier:`. The checker reports "SHONEN box 1 is marked
  `[x]` without a named non-author verifier".
- **A second `## Axes — ` heading that is not last** — M24, the control. An
  *earlier* `## Axes — ` heading carries a stale axes table (depth 5). The
  declared rule takes the last such heading, so a correct checker reports no
  mismatch; a checker that read the first heading would falsely trip K01. The
  observed behaviour is exit 0 and `mismatches` 0, so the checker's heading
  selection is correct. M25 is the mirror image: a *later* `## Axes — `
  heading with the same stale table, which the checker must take as the current
  axes table, so K01 must trip — and it did.
- **A table row with an extra pipe** — M26. The depth row becomes
  `| depth || 8 | …`, so a fixed-column parser misreads the score cell. The
  checker reports K01 as a mismatch and exits 1; it does not report a clean
  pass, and it does not abort with exit 2.

## 5. Findings

1. **[obs] The checker's heading selection is section-scoped and correct.**
   M24 (earlier heading) produced no mismatch; M25 (later heading) tripped
   K01. Both readings of the declared rule are exercised and both behave as
   declared.

2. **[obs] An "unstated" value is a mismatch for K12, K14 and K15.** M27,
   M28, M30, M15b, M31 and M32 all killed by the checker, each tripping
   exactly the expected id. A row that simply stops mentioning the fact does
   not slip through.

3. **[obs] A SHONEN box marked `[x]` with no `non-author verifier:` name is a
   mismatch (K20).** M20 killed on K20.

4. **[obs] The checker's own path grammar resolves a bare filename against the
   directory of the nearest preceding qualified path in the same list**
   (`resolve_paths`, `tools/check-self-assessment.py:267-290`). The lane's
   `host-census-gate` row cites `` `after.md` `` immediately after
   `` `.ufo/evidence/round-1-kaika/scout-live.md` ``, and the checker resolves
   it to the evidence directory rather than reporting it absent. This is
   [inf] a deliberate reading of "a citation of a file in a named directory is
   not reported as an absent path", and it is what keeps K17 clean on the
   pristine baseline. It also means a fixture that breaks the *directory* of a
   qualified path does not necessarily trip the check, so the capability-path
   fixtures break the qualified path itself.

5. **[obs] The checker reads only the revision, never the working tree.** The
   runner commits the mutated tree and passes the commit; the tool's own
   `git show` / `git ls-tree` reads are what supply the data. The tool's
   published contract states this and the pinned bytes implement it.

6. **[inf] Coverage gap in the fixture set, stated rather than hidden.** The
   declared check set has no check for the *contents* of a row's prose, only
   for the numeric and token fields the grammar names. A fixture that
   reworded the depth row's ceiling without touching a counted field would
   survive by construction. That is a property of the declared check set, not
   of this fixture set, and no fixture claims otherwise.

7. **[obs] The lane's own K16 to K23 rows needed no repair at the base.** On
   the pristine baseline at `b9046016` the Capabilities rows and the four
   SHONEN boxes name only paths that exist at that revision, so the baseline
   reports 0 mismatches once the axes table and the census case count are
   corrected. The stale part of the lane's self-assessment is concentrated in
   the round-11 axes table, which the baseline sections replace.

8. **[obs] The lane now holds two `## Axes — ` sections, and the checker's
   section-scoped selection is what keeps the round-25 one authoritative.**
   SCORECARD.md at `5e7c04e` carries `## Axes — current self-assessment (round
   25)` at line 815 below the older round-11 section at line 39. The declared
   rule takes the last such heading, so the round-25 table is the current axes
   table and the round-11 table is history. This is the same selection the
   M24 and M25 fixtures probe from both sides, and the lane's own landed file
   is the "later heading" case that M25 covers. **[unk]** Whether the landed
   checker selects the round-25 table was not exercised by this seat — the
   wave closed before the `landed`-mode rerun completed — so this is stated as
   a design property of the check set, not as a measured result. §7 gives the
   one-command rerun that settles it.

## 6. Restoration and lane safety

- The lane was never written by this seat. `git status --porcelain` in the
  lane shows only untracked wave-1 files (`.ufo/waves/round-25/w1/…`), which
  this seat's own directory is part of; no tracked lane file was modified.
- No `git push`, `git fetch`, or any other lane git write command was issued
  by this seat at any point. The earlier L1 safety bound about scratch pushes
  into the lane's master was received while this seat was already running;
  this seat had pushed nothing and still pushes nothing.
- Every scratch repository is created with `git init` and has **no remote**;
  the runner never runs `git push` or `git fetch`. Scratch repositories live
  under `/fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/repos/` and are
  deleted after each fixture unless `--keep` is passed.
- The checker was executed read-only against those scratch repositories; the
  lane's own files were read with `git archive` and `git show` only.

## 7. What wave 2 should do

The lane has since landed the checker and a corrected axes table in commit
`5e7c04e` ("round-25: C1 self-assessment checker and current axes table; C2
memory-pressure entry, sources S115-S125, checker, SKILL table and registry;
lesson, QUALITY 57-59, LOG; wave-1 evidence"). At that commit the lane's
`tools/check-self-assessment.py` exists with sha256
`343367fb309e43449ee1be50f97c86b917240de7bb6b34b942fd67a163c6242f`, and
SCORECARD.md now carries a second axes section, `## Axes — current
self-assessment (round 25)` at line 815, below the older round-11 section at
line 39.

**[obs] The landed lane state is exactly the two-heading case the fixture set
was built to probe.** With the declared rule "the last table under the last
heading that starts `## Axes — `", the round-25 section at line 815 is the
current axes table and the round-11 section at line 39 is history. M24 and
M25 are the two sides of that rule and were both executed against the tested
bytes: an earlier heading produced no mismatch (control, exit 0) and a later
heading was taken as the current table (K01 tripped). The lane's landed state
is the "later heading" case, so the checker must read line 815 — and the
lane's own file, which I did not get to exercise before the wave closed, is
the last word on that.

Wave 2 should therefore re-run the shipped runner against the landed state,
in `landed` mode, so the baseline is the lane's own artifact rather than my
synthesised one:

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
TOOL=tools/check-self-assessment.py MODE=landed \
  bash .ufo/waves/round-25/w1/MutSelfAssessPlan/run_wave2.sh 5e7c04e
```

`MODE=landed` takes the baseline axes table and Capabilities table verbatim
from the revision, so each fixture becomes "the lane's own artifact plus one
defect". The expected outcome is the same shape as the run recorded above:
baseline `mismatches` 0, 32 defect fixtures killed with the expected check id
and no other, and the one control clean.

Two things to watch in that rerun, both recorded here rather than left for wave
2 to discover:

1. **[obs] The tested bytes and the landed bytes differ.** The run recorded
   above used sha256 `970e3efb4e21071e0bf8db19c8783e3b9bdb39ff075f8df29a6049f31e6d4a33`;
   the lane copy is `343367fb309e43449ee1be50f97c86b917240de7bb6b34b942fd67a163c6242f`.
   The kill results below are evidence about the first sha256, not about the
   second. `run_wave2.sh` prints the sha256 of whatever `TOOL=` points at, so
   the rerun records which bytes it judged.
2. **[obs] The generator now selects the axes and Capabilities tables by
   header key** (`Axis` and `Capability`) inside the last matching heading's
   section, matching the checker's own selection rule rather than "the last
   table in the section". With two axes sections in the lane file, the older
   round-11 section also holds a table whose header first cell is `Axis`;
   picking the wrong one would make every fixture unattributable. This
   correction was made after the recorded run and is what the wave-2 rerun
   exercises.

If the lane's landed wording changes an anchor the fixtures depend on,
`generate_fixtures.py` reports the fixture as `not_materializable` rather than
silently doing nothing, and the manifest's `not_materializable` list names it.

## 8. Limits

- **[obs] The tool under test was read from the executor's scratch checkout,
  not from the lane**, because the lane copy did not exist when this seat ran.
  The executor owns the file and changed it during the wave; the sha256 above
  pins the exact bytes tested, and the landed sha256 is recorded separately in
  §7.
- **[obs] The recorded run is a `computed`-mode run against `b9046016`**, the
  declared claim base, because the lane's repaired axes table was not landed
  when the run executed. The baseline sections therefore synthesise the axes
  and Capabilities tables from values measured at that revision rather than
  taking the lane's own table. That is a fixture harness, not a lane
  artifact, and §7 gives the `landed` form.
- **[obs] The run took about nine minutes wall clock**, dominated by the
  census selftest (about 14 s per checker invocation, once per fixture plus
  once for the baseline; 34 invocations in total). The executor's own
  suggestion of a stub census script would make a wave-2 rerun much faster,
  at the cost of no longer exercising the real census.
- **[obs] No run against the landed lane state was completed.** The wave
  closed while the `landed`-mode rerun was being set up. Nothing in this
  report asserts a result for the landed sha256; the results recorded are for
  the tested sha256 only.

## 9. Evidence pointers

- Fixture manifest and per-fixture metadata:
  `/fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/fixtures/manifest.json`
- Materialised fixture sections:
  `/fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/fixtures/fixtures/<id>/`
- Machine-readable run record with the checker's reason string for every
  killed fixture:
  `/fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/results.json`
- Pinned tool bytes:
  `/fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/tool-under-test.py`
  (sha256 `970e3efb4e21071e0bf8db19c8783e3b9bdb39ff075f8df29a6049f31e6d4a33`)
- Checker source read for the contract:
  `/fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/repo/tools/check-self-assessment.py`
- This seat's scripts:
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutSelfAssessPlan/`

Scope: read=tools/check-self-assessment.py (executor checkout at sha256 970e3efb…, and the lane copy at 5e7c04e), SCORECARD.md, SHONEN.md, PROVINCE.md, SKILL.md, corpus/README.md, corpus/knowledge, corpus/lessons, tools/tsukuroi-census.sh at b9046016831237cd04d38da11ba76e50d5380c53 and at 5e7c04ecb02735491456de2b8bc44550d0db4609 (git archive / git show / git log / git status only); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutSelfAssessPlan/generate_fixtures.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutSelfAssessPlan/run_mutations.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutSelfAssessPlan/run_wave2.sh, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutSelfAssessPlan.md, and under /fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/ the fixtures tree, results.json, tool-under-test.py and the scratch repos; executed=git archive and git show (lane, read-only), git init/add/commit/rev-parse (scratch repos only, no remote), bash tools/tsukuroi-census.sh --selftest (inside scratch repos, read-only), python3 tools/check-self-assessment.py --revision <commit> (inside scratch repos, read-only), python3 generate_fixtures.py, python3 run_mutations.py, bash run_wave2.sh; no git push, no git fetch, no lane git write, no scratch repo with a remote, no pacman transaction, no service action.
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
