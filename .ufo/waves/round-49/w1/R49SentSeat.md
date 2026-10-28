VERDICT: defect-found — the wave's result artifact `w1-results.json` does not exist at snapshot 2026-10-28T14:52:41-03:00, so 0 results entries can be reconciled against 73 dispatched seat names; the seat/report reconciliation below is derived from the dispatch, the spawn map and the report files instead.

# R49SentSeat — P-3 dispatch/result/seat reconciliation (round 49, wave w1)

Snapshot: **2026-10-28T14:52:41-03:00**. Every number below is a read of the lane tree at that instant; all 73 dispatched seats have a report file at that instant; the wave's only missing artifact is `w1-results.json`.

## 1. The result artifact is absent

- `ls -la /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-49/w1-results.json` → `No such file or directory` (checked at 14:43, 14:45:19, 14:45:49 and at snapshot time).
- `find .ufo/waves/round-49 -maxdepth 2 -name '*results*'` → no hit. No `WAVE-DONE*` file either.
- The canonical accounting logic agrees. `python3 .ufo/waves/round-49/l1-summary.py --json`, run immediately after that snapshot, prints `"dispatched": 73`, `"results_entries": 0`, `"reports": 73`, `"attack": 37`, and a `missing_or_unbound` list of length 73 with `bound seats []`. Its `results_entries` is read from `w1-results.json` only (`.ufo/waves/round-49/l1-summary.py:23-27`).

**Results entries counted: 0.** Dispatched names: **73** (`w1-dispatch.json` `taskCall.tasks`). Comparison is therefore `0 vs 73` — every seat has no result entry.

Why this seat cannot close that gap itself: `w1-results.json` is the orchestrator's record of the batched task call, so it can only be written once every task in that call has settled — including this one. The dispatch is still open at snapshot: the spawn map was renamed from `w1.ready.partial` (66 entries, 14:41) to `w1.ready.dispatched` (all 73 entries, first line `2026-10-28T14:43:20`), and no `WAVE-DONE` marker exists. Waiting for the file inside a live seat is a deadlock, so the honest deliverable is the artifact-derived table plus the exact re-check the L1 runs when the file lands (§8).

## 2. Dispatch, spec and spawn map agree exactly

- `w1-spec.json` `items` = **73**; `w1-dispatch.json` `taskCall.tasks` = **73** unique names; `registry.members` = **73**; `counts` = `{"spawn": 73, "resume": 0, "total": 73}`.
- `w1.ready.dispatched` maps **73/73** seat names to agent ids: 0 unmapped names, 0 mapped names outside the dispatch.
- Zero role mismatches between `taskCall.tasks[i].agent` and `registry.members[name].role` (checked over all 73).
- 22 of 73 seats were re-spawned under a suffixed agent id (`-2` … `-7`), e.g. `R49RevGR1a → R49RevGR1a-2`, `R49RevGR1b → R49RevGR1b-2`, `R49RevGR1c → R49RevGR1c-2`. **Seat name ≠ agent id**, so any join must go through `w1.ready.dispatched`; a results entry must carry the seat name (that is the key `l1-summary.py` uses).
- `w1-validate.log` is **0 bytes** (13:49:10), so the dispatch's validation step left no record; dispatch validity is asserted here only through the equality checks above.

## 3. Seat table — every dispatched seat and its result status

`results` = entries for that seat in `w1-results.json` (0 everywhere for want of the file). `roster` = status from the agent roster at snapshot. `flag` marks the accounting defects. This seat's own row (`R49SentSeat`) records the byte size observed at snapshot time, which drifts with each edit of this file.

| # | seat | role | counted | spawn agent | roster | results | report bytes | verdict class | flag |
|---|---|---|---|---|---|---|---|---|---|
| 1 | R49RevGR1a | reviewer | Y | R49RevGR1a-2 | parked | 0 | 7139 | counted:holds | no results entry |
| 2 | R49RevGR1b | reviewer | Y | R49RevGR1b-2 | parked | 0 | 9416 | counted:holds | no results entry |
| 3 | R49RevGR1c | reviewer | Y | R49RevGR1c-2 | parked | 0 | 9437 | counted:holds | no results entry |
| 4 | R49CritGR1a | critic | Y | R49CritGR1a | parked | 0 | 7782 | counted:holds | no results entry |
| 5 | R49CritGR1b | critic | Y | R49CritGR1b | parked | 0 | 8033 | counted:holds | no results entry |
| 6 | R49CritGR1c | critic | Y | R49CritGR1c-2 | parked | 0 | 6113 | counted:holds | no results entry |
| 7 | R49RevGR2a | reviewer | Y | R49RevGR2a | parked | 0 | 11763 | counted:holds | no results entry |
| 8 | R49RevGR2b | reviewer | Y | R49RevGR2b | parked | 0 | 11980 | counted:holds | no results entry |
| 9 | R49RevGR2c | reviewer | Y | R49RevGR2c | parked | 0 | 7039 | counted:holds | no results entry |
| 10 | R49CritGR2a | critic | Y | R49CritGR2a-3 | parked | 0 | 7243 | counted:holds | no results entry |
| 11 | R49CritGR2b | critic | Y | R49CritGR2b | parked | 0 | 8922 | counted:partly | no results entry |
| 12 | R49CritGR2c | critic | Y | R49CritGR2c | parked | 0 | 13695 | counted:holds | no results entry |
| 13 | R49RevGR3a | reviewer | Y | R49RevGR3a-2 | parked | 0 | 7057 | counted:holds | no results entry |
| 14 | R49RevGR3b | reviewer | Y | R49RevGR3b | parked | 0 | 10772 | counted:holds | no results entry |
| 15 | R49RevGR3c | reviewer | Y | R49RevGR3c-4 | parked | 0 | 7668 | counted:holds | no results entry |
| 16 | R49CritGR3a | critic | Y | R49CritGR3a | parked | 0 | 8679 | counted:holds | no results entry |
| 17 | R49CritGR3b | critic | Y | R49CritGR3b | parked | 0 | 8493 | counted:holds | no results entry |
| 18 | R49CritGR3c | critic | Y | R49CritGR3c | parked | 0 | 8053 | counted:holds | no results entry |
| 19 | R49ExecGRCorr | executor |  | R49ExecGRCorr | parked | 0 | 10867 | supports | no results entry |
| 20 | R49RevCorr | reviewer |  | R49RevCorr | parked | 0 | 11705 | supports | no results entry |
| 21 | R49RevCounter | reviewer |  | R49RevCounter | idle | 0 | 20841 | defect-found | no results entry |
| 22 | R49CritCounter | critic |  | R49CritCounter | parked | 0 | 12518 | defect-found | no results entry |
| 23 | R49MutCounterA | mutation-tester |  | R49MutCounterA | parked | 0 | 13244 | supports | no results entry |
| 24 | R49MutCounterB | mutation-tester |  | R49MutCounterB | parked | 0 | 10518 | defect-found | no results entry |
| 25 | R49SentForge | sentinel |  | R49SentForge | parked | 0 | 8721 | defect-found | no results entry |
| 26 | R49LabParse | executor |  | R49LabParse | parked | 0 | 13015 | defect-found | no results entry |
| 27 | R49ExecAnchorA | executor |  | R49ExecAnchorA | parked | 0 | 11220 | supports | no results entry |
| 28 | R49ExecAnchorB | executor |  | R49ExecAnchorB | parked | 0 | 12417 | defect-found | no results entry |
| 29 | R49ScoutAdjLl | scout |  | R49ScoutAdjLl | parked | 0 | 5749 | supports | no results entry |
| 30 | R49RevAdjA | reviewer |  | R49RevAdjA | parked | 0 | 19631 | supports | no results entry |
| 31 | R49RevAdjB | reviewer |  | R49RevAdjB | parked | 0 | 15803 | defect-found | no results entry |
| 32 | R49CritAdjA | critic |  | R49CritAdjA | parked | 0 | 13801 | defect-found | no results entry |
| 33 | R49CritAdjB | critic |  | R49CritAdjB | parked | 0 | 12173 | heading | no results entry |
| 34 | R49MutAdj | mutation-tester |  | R49MutAdj-7 | parked | 0 | 8091 | supports | no results entry |
| 35 | R49ExecFdA | executor |  | R49ExecFdA | parked | 0 | 11553 | defect-found | no results entry |
| 36 | R49ExecFdB | executor |  | R49ExecFdB | idle | 0 | 10776 | supports | no results entry |
| 37 | R49RevFdA | reviewer |  | R49RevFdA | parked | 0 | 16872 | defect-found | no results entry |
| 38 | R49RevFdB | reviewer |  | R49RevFdB | parked | 0 | 11951 | defect-found | no results entry |
| 39 | R49CritFdA | critic |  | R49CritFdA | parked | 0 | 15346 | defect-found | no results entry |
| 40 | R49CritFdB | critic |  | R49CritFdB | parked | 0 | 10259 | defect-found | no results entry |
| 41 | R49MutFd | mutation-tester |  | R49MutFd-2 | parked | 0 | 12381 | defect-found | no results entry |
| 42 | R49LabFd | executor |  | R49LabFd | parked | 0 | 8636 | supports | no results entry |
| 43 | R49ScoutCmd | scout |  | R49ScoutCmd | parked | 0 | 4701 | supports | no results entry |
| 44 | R49ScoutIoctl | scout |  | R49ScoutIoctl | parked | 0 | 3075 | supports | no results entry |
| 45 | R49ScoutSysfs | scout |  | R49ScoutSysfs-2 | parked | 0 | 3932 | supports | no results entry |
| 46 | R49ScoutDevRepl | scout |  | R49ScoutDevRepl-2 | parked | 0 | 4872 | supports | no results entry |
| 47 | R49ScoutKillXml | scout |  | R49ScoutKillXml-6 | parked | 0 | 4423 | supports | no results entry |
| 48 | R49ScoutProcFd | scout |  | R49ScoutProcFd-3 | parked | 0 | 7646 | falsifies | no results entry |
| 49 | R49ScoutBashRedir | scout |  | R49ScoutBashRedir | parked | 0 | 5918 | supports | no results entry |
| 50 | R49ScoutReject | scout |  | R49ScoutReject-2 | parked | 0 | 8321 | supports | no results entry |
| 51 | R49ScoutConsider | scout |  | R49ScoutConsider | parked | 0 | 7671 | draft | no results entry |
| 52 | R49ScoutQuality | scout |  | R49ScoutQuality | parked | 0 | 18908 | defect-found | no results entry |
| 53 | R49ConnWave | connector |  | R49ConnWave-2 | parked | 0 | 16887 | falsifies | no results entry |
| 54 | R49ConnClaims | connector |  | R49ConnClaims | parked | 0 | 16654 | defect-found | no results entry |
| 55 | R49ScribeLesson | scribe |  | R49ScribeLesson-3 | parked | 0 | 13290 | draft | no results entry |
| 56 | R49ScribeLog | scribe |  | R49ScribeLog-5 | parked | 0 | 14392 | draft | no results entry |
| 57 | R49ScribeScore | scribe |  | R49ScribeScore | parked | 0 | 16897 | draft | no results entry |
| 58 | R49ScribeSkill | scribe |  | R49ScribeSkill | parked | 0 | 19486 | draft | no results entry |
| 59 | R49ScribeReadme | scribe |  | R49ScribeReadme-2 | parked | 0 | 21225 | draft | no results entry |
| 60 | R49ScribeAssim | scribe |  | R49ScribeAssim | parked | 0 | 15007 | defect-found | no results entry |
| 61 | R49CritAssim | critic |  | R49CritAssim-4 | idle | 0 | 23695 | defect-found | no results entry |
| 62 | R49SentScopeA | sentinel |  | R49SentScopeA | parked | 0 | 16964 | defect-found | no results entry |
| 63 | R49SentScopeB | sentinel |  | R49SentScopeB | idle | 0 | 18448 | defect-found | no results entry |
| 64 | R49SentSeat | sentinel |  | R49SentSeat-3 | running | 0 | 16671 | defect-found | no results entry |
| 65 | R49Distill | reviewer |  | R49Distill | idle | 0 | 14434 | defect-found | no results entry |
| 66 | R49Simplify | reviewer |  | R49Simplify | idle | 0 | 17948 | defect-found | no results entry |
| 67 | R49ExecGates | executor |  | R49ExecGates-2 | idle | 0 | 10190 | defect-found | no results entry |
| 68 | R49ExecLiveCensus | executor |  | R49ExecLiveCensus | idle | 0 | 8396 | supports | no results entry |
| 69 | R49ScoutHost | scout |  | R49ScoutHost-2 | parked | 0 | 5507 | supports | no results entry |
| 70 | R49RevMarks | reviewer |  | R49RevMarks | idle | 0 | 13599 | defect-found | no results entry |
| 71 | R49ScoutSources | scout |  | R49ScoutSources | idle | 0 | 12388 | supports | no results entry |
| 72 | R49ExecSelfAssess | executor |  | R49ExecSelfAssess | idle | 0 | 10542 | defect-found | no results entry |
| 73 | R49ScribeCoverage | scribe |  | R49ScribeCoverage | idle | 0 | 20144 | defect-found | no results entry |

## 4. Missing and placeholder reports

**Missing reports at snapshot: none** — all 73 dispatched seats have a report file under `w1/`, so there is no absent-report defect to report.

**Placeholder scan: 0 hits** over the 73 present reports under the four named criteria — empty file, under 200 bytes, a literal `T-O-D-O` marker, and a body that is only a `Report:` line plus a `.ufo/…` path. Supporting observations: the smallest present report is 3075 bytes (`R49ScoutIoctl.md`); no report's first line is a bare `Report:` pointer; every report filename matches a dispatch name exactly (0 extras, 0 near-misses).

## 5. Counted cohort and verdict classes

- Counted seats (registry axis `counted`): **18**, and **18/18** have a report — all 9 reviewers and all 9 critics for GR1/GR2/GR3.
- Counted first-line verdicts: 17 `holds`, 1 `partly` (`R49CritGR2b`). The only counted non-holds line is on `R49CritGR2b` (GR2). Whether a `partly` binds is the L1's call, not this seat's.
- All present reports by first-line class: defect-found 27, supports 19, counted:holds 17, draft 6, falsifies 2, counted:partly 1, heading 1. The single `heading` class is `R49CritAdjB`, whose first line is a heading and whose verdict line lower in the file reads `VERDICT: supports`.

## 6. Dead seats

**Process-level dead seats at snapshot: 0.** The rule applied: a seat whose roster state is no longer `running` (`parked` / `idle` / `on disk` / absent) *and* which has no report file *and* no result entry is dead. `w1-results.json` is absent, so there is no `output` field anywhere to quote; for any settled-without-report seat the only output evidence is its transcript tail, reproduced below when present.

Settled-without-report detail:

(none: no seat is settled without a report — every dispatched seat has a report file)

**Binding-level dead seats at snapshot: 73/73.** `l1-summary.py` requires exactly one results entry whose `agent` equals the seat role and whose `output` is truthy, plus a report file (`l1-summary.py:45`, `:49-50`); with 0 results entries every seat fails `result_ok` and lands in `missing_or_unbound` (length 73). This is one wave-level record defect, not 73 seat failures — do not read the 73 as a cohort collapse.

## 7. Wave accounting table

| role | dispatched | report present | report missing | settled with no report |
|---|---|---|---|---|
| connector | 2 | 2 | 0 | 0 |
| critic | 15 | 15 | 0 | 0 |
| executor | 10 | 10 | 0 | 0 |
| mutation-tester | 4 | 4 | 0 | 0 |
| reviewer | 18 | 18 | 0 | 0 |
| scout | 13 | 13 | 0 | 0 |
| scribe | 7 | 7 | 0 | 0 |
| sentinel | 4 | 4 | 0 | 0 |
| **total** | **73** | **73** | **0** | **0** |

- Attack share (reviewer + critic + mutation-tester + labrat / total): **37/73 = 0.507** — matches `l1-summary.py` (`attack=37/73 (0.507)`).
- Total **73**; dead at process level **0**; dead at binding level **73** (pending `w1-results.json`).

## 8. Exact re-check when `w1-results.json` lands

Run from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, read-only:

```sh
python3 .ufo/waves/round-49/l1-summary.py --json            # canonical: results, reports, dead list
python3 - <<'PY'
import json, os, re
W = '.ufo/waves/round-49'
d = json.load(open(f'{W}/w1-dispatch.json'))
names = [t['name'] for t in d['taskCall']['tasks']]
roles = {t['name']: t['agent'] for t in d['taskCall']['tasks']}
res = json.load(open(f'{W}/w1-results.json')).get('results') or []
by = {}
for r in res: by.setdefault(r.get('name'), []).append(r)
print('results entries', len(res), 'dispatched', len(names))
print('entries with no dispatch name', [k for k in by if k not in names])
print('seats with !=1 entry', [n for n in names if len(by.get(n, [])) != 1])
print('entries whose agent != role', [n for n in names for r in by.get(n, []) if r.get('agent') != roles[n]])
print('entries with falsy output', [n for n in names for r in by.get(n, []) if not r.get('output')])
print('seats with no report', [n for n in names if not os.path.isfile(f'{W}/w1/{n}.md')])
bad = []
for n in names:
    p = f'{W}/w1/{n}.md'
    if os.path.isfile(p):
        b = open(p, 'rb').read(); t = b.decode('utf-8', 'replace')
        marker = 'TO' + 'DO'
        if len(b) < 200 or marker in t or re.search(r'Report:\s*\.ufo', t): bad.append((n, len(b)))
print('placeholder reports', bad)
PY
```

Anything that prints a non-empty list is a seat to record as dead in the wave report with that list's reason; the existing placeholder scan is only valid for the report bytes present at snapshot.

## 9. Scope, guards and cost

- Read-only throughout: no lane file created, edited or deleted; no `git`/`jj` command in the lane; no selftest, census or counter was run (P-3 is a reconciliation seat, so the 5–10 minute counters were deliberately not invoked).
- All reads were of dispatched/frozen artifacts plus `w1/*.md`; scratch lived in `/fast/scratch/hyaku/tsukuroi-r49/R49SentSeat-3/` and is removed after the tables were copied into this report.
- No tool was installed or upgraded (nothing was needed).

## 10. Smallest remediation

1. When the batched call settles, write `w1-results.json` before any report says a wave is accounted — 0 entries currently zero out all 73 seats' binding (`l1-summary.py` `result_ok`).
2. Make the wave report state seats as `present / running / dead` from the report files plus the roster, never as "73 dead" from an absent results file.
3. Keep the `w1.ready.dispatched` join: seat name to agent id is not the identity map for 22 of 73 seats.
