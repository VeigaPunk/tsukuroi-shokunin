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

### 4.1 The defect kinds the assignment named, and how each is realised

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

Run the shipped runner against the landed lane state:

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
TOOL=tools/check-self-assessment.py MODE=landed \
  bash .ufo/waves/round-25/w1/MutSelfAssessPlan/run_wave2.sh <REVISION>
```

`MODE=landed` takes the baseline axes table and Capabilities table verbatim
from the revision, so once the lane's repaired table is landed the baseline is
the lane's own artifact and each fixture is that artifact plus one defect. The
expected outcome is the same: baseline `mismatches` 0, 32 killed, 1 control
clean. If the lane's repaired table changes the wording the fixtures anchor
on, `generate_fixtures.py` reports the fixture as `not_materializable` rather
than silently doing nothing, and the manifest's `not_materializable` list names
it.

## 8. Limits

- The tool under test was read from the executor's scratch checkout, not from
  the lane, because the lane copy did not exist when this seat ran. The
  executor owns the file and may still change it; the sha256 above pins the
  exact bytes tested, and `run_wave2.sh` re-pins whatever `TOOL=` points at.
- The run took about eight minutes wall clock, dominated by the census
  selftest (about 14 s per checker invocation, run once per fixture plus once
  for the baseline). The executor's own suggestion of a stub census script
  would make a wave-2 rerun much faster, at the cost of no longer exercising
  the real census.
- The fixtures were generated in `computed` mode against `b9046016`, the
  declared claim base, because the lane's repaired axes table was not landed
  at the time of the run. `landed` mode is the wave-2 form.

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

Scope: read=tools/check-self-assessment.py (executor checkout), SCORECARD.md, SHONEN.md, PROVINCE.md, SKILL.md, corpus/README.md, corpus/knowledge, corpus/lessons, tools/tsukuroi-census.sh at b9046016831237cd04d38da11ba76e50d5380c53 (git archive / git show only); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutSelfAssessPlan/generate_fixtures.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutSelfAssessPlan/run_mutations.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutSelfAssessPlan/run_wave2.sh, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/MutSelfAssessPlan.md, and under /fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/ the fixtures tree, results.json, tool-under-test.py and the scratch repos; executed=git archive and git show (lane, read-only), git init/add/commit/rev-parse (scratch repos only, no remote), bash tools/tsukuroi-census.sh --selftest (inside scratch repos, read-only), python3 tools/check-self-assessment.py --revision <commit> (inside scratch repos, read-only), python3 generate_fixtures.py, python3 run_mutations.py, bash run_wave2.sh; no git push, no git fetch, no lane git write, no pacman transaction, no service action.
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
