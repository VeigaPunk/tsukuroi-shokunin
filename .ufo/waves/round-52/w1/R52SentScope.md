VERDICT: defect-found

# W-N3 — scope and misroot snapshot

Axes: calibration, scope. Frozen revision tested: `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`; base `cc88b81d78bcbe06bce3f6bf722a108432ad276f`. Observations collected while the wave was still changing (approximately 02:22–02:38, -03). This is not an all-seats-settled clearance.

## (a) Frozen diff — supports path scope

Command: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff cc88b81d78bcbe06bce3f6bf722a108432ad276f ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 --name-status`.

Observed 21 paths: 14 additions under `.ufo/waves/round-52/`; modifications to lane `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`; additions `corpus/lessons/round-51.md` and `tools/check-scrub-admission-r52.py`. No MANIFEST.json, fleet scripts/templates, `.ufo/state`, or sibling-repository path appears. All are lane-relative paths. Receipt: `R52SentScope/a1-diff-name-status.txt:1-21`.

## (b) Fleet status — unrelated root strays observed

The first requested `git -C /home/vgpnk/Projects/shokunin status --porcelain` produced no output. A later snapshot produced:

```
?? count-c1.cover
?? count-c2.cover
```

Receipt: `R52SentScope/b1-fleet-status.txt:1-2` (also `final-snapshot.txt`). Both files were left untouched. Observed mtimes: 02:27:37 and 02:27:47. Their readable embedded paths name `mori-shokunin/.ufo/waves/round-61/count-c1.py` and `count-c2.py`. Text searches observed zero `tsukuroi` and zero `round-52` matches in each. Thus neither meets the assigned tsukuroi/round-52 content condition; attribution to a particular writer is not established. Do not attribute these strays to tsukuroi.

Ignored host dispatcher logs are not included by ordinary porcelain; no global cleanliness claim follows from this check.

## (c) Scratch survivors — cleanup condition not satisfied at snapshot

At 02:36:48, 24 directories were observed (receipt `R52SentScope/c6-survivors-final.txt`, containing observation time, report presence and newest-file paths):

```
R52CritDecl
R52CritForgeC1a
R52CritGR1a
R52CritGR1b
R52CritGR1c
R52CritGR2Host
R52CritGR2a
R52CritGR2b
R52CritGR2c
R52CritGR3a
R52CritGR3b
R52CritGR3c
R52CritHoleC3Relink
R52ExecBattC23
R52ExecLiveHost
R52ExecNoHarm
R52ExecRunC1
R52ExecRunC3
R52ExecValidC2
R52MutAdj
R52MutScorer
R52RevHoleC2Liar
controls
l1
```

This list is point-in-time; later listings differed. Presence is established, completion/liveness is not established merely by report presence or file age. Several directories had files changing during inspection. No survivor was removed by this seat.

### Finding: premature cleanup claims

- **Severity:** low, correctness/provenance defect; finality not established.
- **Failure path:** a reader accepts a filed report's cleanup assertion despite its scratch still being present.
- **Evidence:** `R52ExecRunC3.md:4` says “Clone and scratch were removed after capture.” At inspection, `/fast/scratch/hyaku/tsukuroi-r52/R52ExecRunC3/clone.json` and its directory remained. `R52ExecRunC1.md` similarly claims scratch clones were removed, while its `fx.Pjcdkn` clone remained. Both directories were repeatedly observed after their report mtimes (02:33:10 / 02:35:06); `c6-survivors-final.txt` records report presence and surviving scratch. Observed sizes were approximately 1.3 GB and 411 MB.
- **Impact:** the reports overstate cleanup; the requested empty-scratch condition cannot be certified.
- **Smallest remediation:** owning seats finish/copy receipts, wait for all writers, remove their own scratch, then correct or substantiate cleanup assertions. Do not delete active C2 scratch to obtain an empty listing.

`controls` and `l1` are not dispatch-seat names. `controls` was empty; `l1` contained `bash-pipelines.html`. Their ownership/cleanup must be handled by the L1, not this sentinel.

Removed scratch referenced in reports is not itself a defect: removal is required, and an inline report can preserve observations. Absence of a separate receipt directory does not by itself prove evidence loss or counter failure.

## (d) Newer-than-freeze files — distinguish mtime from byte drift

The assigned find command returned 15 files; full paths are preserved in `R52SentScope/d1-lane-newer-than-freeze.txt:1-15`:

- `controls/battery-summary-r52-freeze-c{1,2,3}.jsonl`;
- `frozen/FROZEN-hashes.txt`, `self-assessment-at-freeze.json`, `self-assessment-at-freeze.rc`, `sources-census-freeze.txt`;
- `make-spec.py`, `w1-spec.json`, `w1-validate.log`, `w1-dispatch.json`;
- `w1.ready`, `report-draft.md`, `w1.ready.partial`;
- lane-root `LOG.md`.

All but LOG.md are under `.ufo/waves/round-52/`. At observed lane HEAD `4ee3226daa221c72acab23eacaacc8f3c9616954`, the battery summaries, self-assessment/source receipts and spec/dispatch files are committed round artifacts. `FROZEN-hashes.txt` and LOG.md exist in the freeze commit. LOG.md's working-tree SHA256 equaled its frozen SHA256 (`da2e332887c8862629f770c7dbee105b37de34cb71654213f1bf400253aa5e6b`): its newer mtime is not evidence of changed bytes; the cause of that mtime is not established.

`report-draft.md`, `w1.ready`, `w1.ready.partial` were untracked, alongside `w1/` (receipt `lane-status.txt:1-4`). Consequently the literal “only committed round files” condition is not fully met at this live snapshot. They are round-level operational artifacts, but authorship is not proved by path. Smallest remediation: L1 deliberately retain/commit or discard these artifacts at closure, and repeat the bounded check after writers settle.

## Supplemental path observations — authorship unresolved

Earlier exploration extended beyond the four assigned checks; these observations are not findings against a named seat:

- At 02:12, `/tmp/battery52.py` matched the frozen round-52 battery SHA256 `48356a8a…`; `/tmp/c3_freeze.py`, `/tmp/c3_r52freeze.py`, `/fast/scratch/hyaku/r52ctr.py` matched the amended C3 counter SHA256 `cfe3ee23…`.
- `/tmp/c3_r51pin.py` and `/fast/scratch/hyaku/r51ctr.py` matched the older `2732ee6c:tools/check-adjacency-table-r51.py` SHA256 `3d09a8e9…`.
- Byte identity and mtime do not identify the writer or prove these copies were executed. They are outside the mandated per-seat scratch paths; L1 should identify their owner before any cleanup. No substitution/exploitation was attempted. Do not infer stale-counter measurement from their presence.

## Limits and handoff

No C1/C2/C3 verdict is adjudicated here. No `resume_continuity_v1` surface was assigned or tested. I did not modify tracked lane files, fleet files, sibling files, or anyone's scratch; no tools installed, no fixture created, no own scratch directory to remove. Only this report and receipts were written. Additional read-only exploration and section-hash runs occurred beyond the four-command surface; they do not establish broader readiness. Later writer completion may change the snapshot. L1 should repeat the four bounded checks after all seats settle, rather than treating this mid-wave report as final clearance.
