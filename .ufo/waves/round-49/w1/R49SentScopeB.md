VERDICT: defect-found

# R49SentScopeB — item P-2: scope and scratch discipline of the non-cohort seats

Seat class EXEC-AUTHORIZED — only the item's commands were run (`ls`, `find`, `stat`, `sha256sum`,
`grep`, `git status`, `git show`, `git rev-parse`, `git diff`, one throwaway `python3` scanner).
Every scanner and copy lived under `/fast/scratch/hyaku/tsukuroi-r49/R49SentScopeB/` and that
directory was removed at exit after the receipts were copied into
`.ufo/waves/round-49/w1/R49SentScopeB/`. Nothing in the lane, the fleet repo, a sibling lane,
`/tmp`, a PATH directory, `~/.omp`, `~/.agents` or `shokuknow` was written. No tools installed.

## Axes

(a) declaration of execution class in the report, (b) command surface actually shown (scratch-only
writes, read-only lane), (c) scratch removal at exit, (d) writes into the fleet repo or a sibling
lane. Kept any finding that improves one axis without weakening another; the per-seat flags are the
frontier (receipt `table.txt`).

## Snapshot

`2026-10-28T14:45:28-0300`. Report files under `w1/`: 60, of which 18 are the counted cohort
(`R49RevGR{1,2,3}{a,b,c}`, `R49CritGR{1,2,3}{a,b,c}`; `.ufo/waves/round-49/frozen/FROZEN.md:31-35`),
leaving **43 non-cohort reports** audited here. Three of those had a live agent at snapshot
(`R49CritAssim`, `R49Distill`, `R49SentScopeA` per `proc://`), so their rows are point-in-time and
their scratch dirs are live, not leftovers; the other live seats at snapshot
(`R49ExecFdB`, `R49RevCounter`, `R49ExecGates`, `R49ExecLiveCensus`, `R49ExecSelfAssess`,
`R49ScoutSources`, `R49ScribeCoverage`, `R49SentSeat-3`, …) had no report yet and are outside this
audit's report set.

## (a) Declaration — 32 of 43 reports carry neither token

`grep -l 'EXEC-AUTHORIZED' w1/*.md` returns 12 files, 11 of them non-cohort:
`R49ConnClaims.md:5`, `R49CritAssim.md`, `R49CritCounter.md:5`, `R49Distill.md`, `R49ExecFdA.md:3`,
`R49MutCounterA.md:5`, `R49ScribeLesson.md:9`, `R49ScribeLog.md:5`, `R49ScribeScore.md:5`,
`R49ScribeSkill.md:3`, `R49SentScopeA.md:23`. `grep -rl 'executed=none' w1/*.md` returns **0**
files: no seat used the `NO-EXEC` / `Scope: executed=none` form, including the three non-cohort
seats whose own text bounds them to reads only — `R49ScoutAdjLl.md:3` ("The counter script was not
executed"), `R49RevCorr.md:137-138` ("I did not run … any selftest/counter"), `R49ExecGRCorr.md:107`
("I did not run `tools/check-scrub-admission-r49.py` itself"). (`R49ScoutIoctl` is not in that set:
it ran `curl` fetches, `R49ScoutIoctl.md:9-15`.)

The remaining 32 non-cohort reports (`table.txt` column `tok`) declare no execution class at all:
`R49ConnWave R49CritAdjA R49CritAdjB R49CritFdA R49CritFdB R49ExecAnchorA R49ExecAnchorB
R49ExecGRCorr R49LabFd R49LabParse R49MutAdj R49MutCounterB R49MutFd R49RevAdjA R49RevAdjB
R49RevCorr R49RevFdA R49RevFdB R49ScoutAdjLl R49ScoutBashRedir R49ScoutCmd R49ScoutConsider
R49ScoutDevRepl R49ScoutIoctl R49ScoutKillXml R49ScoutProcFd R49ScoutQuality R49ScoutReject
R49ScoutSysfs R49ScribeAssim R49ScribeReadme R49SentForge`.

**Why this is a dispatch defect, not (only) seat misconduct.** Every item's prompt opens
`Execution class: EXEC-AUTHORIZED — the commands named in this item, and no other.`
(`w1-spec.json`, 73/73 items), but no item's report contract asks the seat to restate it: the shared
block says only `Report first line (non-counted seats): VERDICT: …`, then evidence
(`w1-spec.json` → `context`). P-2's criterion (a) therefore cannot be satisfied from the report text
for a seat the dispatch never told to write it; the 11 carriers did so voluntarily.

**Substantive proxy (so the axis is still measured).** 31 of 43 reports state a read-only bound in
prose (`table.txt` column `ro`). The 12 that state none are:
`R49CritFdA R49MutAdj R49MutCounterA R49MutFd R49RevCorr R49RevFdB R49ScoutAdjLl R49ScoutConsider
R49ScoutIoctl R49ScoutQuality R49ScoutReject R49SentForge`; each was checked in (b) and (d) by its
shown commands instead — none of them writes anywhere (see below). So the *substance* of (a) holds;
the *declaration* mostly does not exist.

Smallest fix: add one required line to the report contract — `Scope: executed=<n> commands; writes
under <scratch only> | executed=none` — or drop (a) from the sentinel item. Evidence:
`w1-spec.json` items 1-73 prompts.

## (b) Command surface — no lane, fleet, PATH, /tmp or sibling writes by any non-cohort seat

Method: every non-cohort report was scanned for write verbs (`>`, `>>`, `tee`, `cp`, `mv`,
`install`, `touch`, `mkdir`, `sed -i`, `dd of=`, `open(...,'w'|'a')`, `rm -rf`, `trap`) and for
mutating git/jj verbs against the lane; hits were resolved by hand. Receipts `pats.json`,
`pats2.json`, `table.txt`.

- Lane writes: **0**. The only line matching a lane write shape is a quotation of the counter's own
  text, `R49CritAdjA.md:155`. No report shows `git -C <lane>` with `add|commit|stash|checkout|
  switch|reset|clean|rm|mv|pull|push|apply|am`, and no `jj` mutation against the lane.
- Fixture git mutations are all inside a scratch clone with the toplevel assertion stated:
  `R49CritFdB.md:49-52` (`rev-parse --show-toplevel == $D` before the first commit, then
  `git -C "$D" -c user.name=fixture … commit`), `R49ExecAnchorB.md:138`, `R49MutCounterB.md:40,125`
  ("the only git commit anywhere was inside the scratch fixture clone"), `R49ExecFdA.md:81`
  (`checkout -q --detach` in its own clone).
- Scratch citations: 29 of the 43 audited reports cite a path under
  `/fast/scratch/hyaku/tsukuroi-r49/`, and every one cites its **own** `<seat>/` subtree
  (`table.txt`); no seat cites another seat's tree.
- `/tmp`: the only mentions are quotations of the census contract (`R49ScribeSkill.md:181-183`
  quoting `SKILL.md:481-482`), never a seat write. `/home/vgpnk/.omp`, `~/.agents`, `shokuknow` and
  PATH dirs appear only as negations (`R49MutCounterB.md:121`, `R49ScribeSkill.md:235`).
- Receipts stay small: largest file under `w1/` is 1,040,954 B
  (`R49ScoutBashRedir/bash.html`); `find -size +2M` is empty (`receipt-sizes.txt`).

### Deviation B-1 (low) — `R49ScoutCmd` left a staging copy at the shared round root

`/fast/scratch/hyaku/tsukuroi-r49/R49ScoutCmd-srcpreview.md`, 248,933 B, mtime `14:19:32`, still
present at `14:45` after the seat finished (`R49ScoutCmd.md` mtime `14:22:18`). Content is
byte-identical to the frozen registry:

```
$ git -C …/tsukuroi-shokunin show 55c07cd3:corpus/SOURCES.md | sha256sum
bf65ccd35c12dcea9d6f2c1bf3b2a1c6154b92b6e6837ab106261dff21c41a2d  -
$ sha256sum /fast/scratch/hyaku/tsukuroi-r49/R49ScoutCmd-srcpreview.md
bf65ccd35c12dcea9d6f2c1bf3b2a1c6154b92b6e6837ab106261dff21c41a2d  …
```

It is outside the seat's own subtree (`/fast/scratch/hyaku/tsukuroi-r49/R49ScoutCmd/`, which the
report says it removed: `R49ScoutCmd.md:3`) and that seat never mentions it:
`grep -n srcpreview R49ScoutCmd.md R49ScoutCmd/` returns rc 1 (no match), so neither the report nor
its receipts account for the file. The item's own
text names only `mkdir -p /fast/scratch/hyaku/tsukuroi-r49/R49ScoutCmd` and a `curl` into that
directory (`w1-spec.json` item `R49ScoutCmd`), so this path was not authorized by the item either.
Impact: none on lane bytes (it is a copy of frozen bytes, in the designated round scratch root);
the defect is undisclosed residue outside the seat's declared scratch. Smallest remediation: the
seat deletes it, or the L1 records it as scratch residue in the wave closeout.

### Observation B-2 (informational) — two seats used a whitespace path inside their own scratch

`R49ExecFdA.md:81` `TMPDIR="/fast/scratch/hyaku/tsukuroi-r49/R49ExecFdA/selftest tmpdir"` and the
live `R49ExecFdB` tree `/fast/scratch/hyaku/tsukuroi-r49/R49ExecFdB/` contains a `dirty dir` (mtime
`14:37`). The binding says "prefer a space-free path unless your item says otherwise"; here the
space is the object under test (TMPDIR-with-whitespace, S253), and both paths are inside the seat's
own subtree, so this is a deliberate exception, not a deviation.

## (c) Scratch removal — two live dirs, one shared-root empty dir, one disclosed stray

At the snapshot the round scratch root held (`scratch-root.txt`):

```
R49CritAssim  R49Distill  R49ExecFdB  R49ExecGates  R49ExecLiveCensus  R49ExecSelfAssess
R49RevCounter R49ScoutCmd-srcpreview.md  R49ScribeCoverage  R49SentScopeB  R49SentSeat-3
counter-c3  l1
```

- Directories belonging to a **finished** non-cohort seat: **none**. `R49CritAssim` and `R49Distill`
  are running (`proc://`); `R49ExecFdB`, `R49RevCounter`, `R49SentSeat-3`, `R49ExecGates`,
  `R49ExecLiveCensus`, `R49ExecSelfAssess`, `R49ScoutSources`, `R49ScribeCoverage` are running
  seats without a report yet, and `R49SentScopeA`/`R49SentScopeB` are the two sentinel seats (mine
  removed at exit, `R49SentScopeA`'s live while its agent ran).
- Two seats claimed removal while their dir still held files mid-flight, and both claims then held:
  `R49ScribeReadme.md:8` (dir with 5 files at `14:40`–`14:41`, gone by `14:43:43`) and
  `R49ScribeAssim.md:9-10` (dir gone by `14:43:38`). No residue at close.
- `l1/` (empty, `13:40`) is the L1's own scratch root from round setup, not a seat dir.

### Deviation C-1 (low, cross-cutting) — the frozen C3 counter creates `counter-c3` outside any seat's subtree

`/fast/scratch/hyaku/tsukuroi-r49/counter-c3` is an **empty** directory, mtime `14:24`, still present
at `14:45`. It is created by the frozen counter, not by a seat's own `mkdir`:

```
$ git show 55c07cd3:tools/check-fd-band-r49.py | grep -n 'scratch_root\|makedirs\|mkdtemp'
56:def scratch_root(arg):
59:    os.makedirs(base, exist_ok=True)
60:    return tempfile.mkdtemp(prefix='fd-band-', dir=base)
$ git show 55c07cd3:tools/check-fd-band-r49.py | sed -n '25,27p'
… the selftest tree lives under --work (default $HYAKU_SCRATCH/tsukuroi-r49/counter-c3,
HYAKU_SCRATCH default /fast/scratch/hyaku); the counter removes its work dir on exit …
```

So any runner that omits `--work` writes outside its own scratch subtree and leaves the empty
parent behind ("removes its work dir", never `base`). Reports that ran the counter with no `--work`
in the shown invocation: `R49CritFdB.md:33,54,81,109` (cohort seat — outside P-2's per-seat
surface) and `R49MutFd.md:29` ("counter, `--revision …, --census-file <scratch mutant>`", runs at
`:33-41`). [INFERENCE] Creation at `14:24` precedes `R49MutFd`'s first run: its five runs total
77+56+95+110+104 s ≈ 7.4 min and its report lands `14:37:53`, so its counter insance cannot have
created the dir at `14:24`; the earliest no-`--work` invocation on record is `R49CritFdB`'s
(`14:20-14:23`). I did not re-run the counter to settle it (one selftest per seat budget, and the
counter's own runs are other seats' measurement). Impact: an empty directory in the round scratch
root; no lane or fleet byte. Smallest remediation: seats pass `--work <own scratch>/…`, or the
counter's default base moves under the caller's dir.

## (d) Fleet repo and sibling lanes — clean

`git -C /home/vgpnk/Projects/shokunin status --porcelain` (`fleet-status.txt`, 8 entries):

```
 M .scratch/goal-20261028-hyaku-run11.md
?? .scratch/closure-mado-r50.json
?? .scratch/closure-r54/
?? .scratch/source-routing-queue.md
?? .ufo/reports/round-49/tsukuroi.md
?? o.bin
?? oldrep1.out
?? oldrep2.out
```

The only round-49 path is `.ufo/reports/round-49/tsukuroi.md`, the L1's own lane report at its
standard fleet-level path (`mtime 14:02`, before the first seat report at `14:03`; head of file
`# tsukuroi — round 49 (hyaku run 11, attempt 1)`). The other strays predate the round:
`o.bin` `Oct 27 16:58`, `oldrep1.out` `09:10`, `oldrep2.out` `09:11`, `.scratch/closure-r54/`
`12:55` (round start `13:34`). No seat wrote into the fleet repo.

Sibling lanes: 21 lane repos with `.git` were checked with
`git -C <sib> status --porcelain | grep -i 'round-49|r49'` (`sibling-status.txt`): **all NONE**,
including `tsukuroi-shokunin`, whose untracked round-49 entries are L1 wave artifacts
(`before/*.json`, `l1-summary.py`, `w1.ready`, `w1/*`) plus L1's own report.

### Observation D-1 — the lane worktree carries one uncommitted tracked-file change (L1, not a seat)

`git -C tsukuroi-shokunin status --porcelain` → ` M corpus/SOURCES.md`, mtime `14:02:34`, HEAD
`d7cfc273`. The whole diff is the S255 `used-by` cell gaining `, corpus/lessons/round-49.md`
(`git diff corpus/SOURCES.md`, 1 insertion 1 deletion). Timing (before the first seat report, after
`w1.ready` at `13:59`) and content (round-49 lesson wiring) point at the L1, the only writer; no
seat report claims a `SOURCES.md` edit, and two explicitly deny one (`R49ScoutCmd.md:3`,
`R49ScoutQuality.md:58`). Not a seat deviation — but it is an uncommitted tracked edit sitting in the
worktree seats are told to distrust, so the L1 should commit it or state it in the closeout.

## Per-seat flags (snapshot 14:45:28)

`tok` = EXEC-AUTHORIZED/NO-EXEC token in the report; `ro` = read-only bound in prose; `sa` =
scratch-removal accounting; `exe` = command/evidence markers; `dir` = leftover scratch dir.

```
seat               mtime      B     tok ro sa exe dir
R49ConnClaims      14:38:29  16654  Y   Y  Y   16 ---
R49ConnWave        14:38:22  16887  -   Y  Y   26 ---
R49CritAdjA        14:20:46  13801  -   Y  Y   14 ---
R49CritAdjB        14:20:47  12173  -   Y  -    4 ---
R49CritAssim       14:45:27  23695  Y   Y  Y    7 DIR(live)
R49CritCounter     14:22:08  12518  Y   Y  Y    4 ---
R49CritFdA         14:26:02  15346  -   -  Y    8 ---
R49CritFdB         14:23:28  10259  -   Y  Y   22 ---
R49Distill         14:45:22  14434  Y   Y  Y    4 DIR(live)
R49ExecAnchorA     14:18:30  11220  -   Y  Y    5 ---
R49ExecAnchorB     14:20:20  12417  -   Y  Y   18 ---
R49ExecFdA         14:24:52  11553  Y   Y  Y   32 ---
R49ExecGRCorr      14:18:13  10867  -   Y  -    2 ---
R49LabFd           14:24:19   8636  -   Y  Y   13 ---
R49LabParse        14:19:54  13015  -   Y  Y   16 ---
R49MutAdj          14:22:25   8091  -   -  Y   18 ---
R49MutCounterA     14:33:01  13244  Y   -  Y   10 ---
R49MutCounterB     14:20:01  10518  -   Y  Y    5 ---
R49MutFd           14:37:53  12381  -   -  Y    8 ---
R49RevAdjA         14:21:11  19631  -   Y  Y    8 ---
R49RevAdjB         14:21:25  15803  -   Y  Y   16 ---
R49RevCorr         14:19:01  11705  -   -  -    5 ---
R49RevFdA          14:33:28  16872  -   Y  Y    7 ---
R49RevFdB          14:33:28  11951  -   -  Y    1 ---
R49ScoutAdjLl      14:17:05   5749  -   -  -    3 ---
R49ScoutBashRedir  14:30:01   5918  -   Y  -    4 ---
R49ScoutCmd        14:22:18   4701  -   Y  Y    4 ---   (stray file at round root, B-1)
R49ScoutConsider   14:31:29   7671  -   -  -    2 ---
R49ScoutDevRepl    14:22:42   4872  -   Y  -    2 ---
R49ScoutIoctl      14:22:15   3075  -   -  -    3 ---
R49ScoutKillXml    14:28:18   4423  -   Y  -    0 ---
R49ScoutProcFd     14:30:42   7646  -   Y  Y    1 ---
R49ScoutQuality    14:37:08  18908  -   -  Y    1 ---
R49ScoutReject     14:32:51   8321  -   -  -    3 ---
R49ScoutSysfs      14:23:02   3932  -   Y  Y    0 ---
R49ScribeAssim     14:43:33  15007  -   Y  Y    7 ---
R49ScribeLesson    14:34:15  13290  Y   Y  Y    2 ---
R49ScribeLog       14:40:53  14392  Y   Y  -    8 ---
R49ScribeReadme    14:43:43  21225  -   Y  Y   11 ---
R49ScribeScore     14:39:19  16897  Y   Y  Y    5 ---
R49ScribeSkill     14:41:55  19486  Y   Y  Y   12 ---
R49SentForge       14:19:01   8721  -   -  Y    1 ---
R49SentScopeA      14:43:34  16964  Y   Y  -    4 ---   (own seat, live peer)
```

## Deviations, ranked

| # | Seat(s) | Axis | Severity | Evidence | Smallest remediation |
|---|---|---|---|---|---|
| B-1 | `R49ScoutCmd` | (b)/(c) | low | 248,933 B `R49ScoutCmd-srcpreview.md` at the round root after finish; `sha256` = freeze `corpus/SOURCES.md`; `R49ScoutCmd.md:3` claims only its own dir removed | delete the file, or record it as scattered scratch in the closeout |
| C-1 | runner(s) without `--work` (`R49CritFdB.md:33,54,81,109`; `R49MutFd.md:29`) | (c) | low | empty `counter-c3/` at the round root, created by `check-fd-band-r49.py:56-60` `os.makedirs` | pass `--work <own scratch>` in every counter invocation |
| a-1 | 32 non-cohort reports (list above) | (a) | process | no `EXEC-AUTHORIZED`/`NO-EXEC` token anywhere; report contract never required one (`w1-spec.json` context) | add a required `Scope:` line to the report contract, or drop (a) |

No high- or medium-severity deviation found: no lane byte, no fleet-repo byte, no sibling-lane byte,
no PATH/`/tmp`/config write by any of the 43 non-cohort seats.

## What I did not do

- Did not re-verify that each report's quoted command output is true — that is the quality and
  counted seats' surface; I audited path shape and write targets only.
- Did not re-run any counter or selftest (no selftest-bearing command was run in this seat).
- Did not delete another seat's tree: `counter-c3`, `l1` and the live seat dirs are reported, not
  removed.
- Did not audit the 18 cohort reports (P-1's surface; `R49SentScopeA.md:171-178` covers them).
- Seats that submitted after `14:45:28` (`R49ExecGates`, `R49ExecLiveCensus`, `R49ExecSelfAssess`,
  `R49ScoutSources`, `R49ScribeCoverage`, `R49Simplify`, `R49SentSeat`, `R49RevMarks` if late) are
  not in the table; their dirs were live, not leftovers.

## Receipts

`.ufo/waves/round-49/w1/R49SentScopeB/`: `final.json`, `table.txt` (per-seat flags), `scan.json`,
`pats.json`, `pats2.json` (raw pattern hits), `fleet-status.txt`, `sibling-status.txt`,
`scratch-root.txt`, `lane-worktree.txt`, `receipt-sizes.txt`. Scratch
`/fast/scratch/hyaku/tsukuroi-r49/R49SentScopeB/` removed at exit after the copy.

## Post-snapshot recheck (14:47)

`ls -la /fast/scratch/hyaku/tsukuroi-r49/` at `14:47` shows the mid-flight dirs I excluded above all
gone (`R49CritAssim`, `R49Distill`, `R49ScribeReadme`, `R49ScribeAssim`, `R49SentScopeA`) and only
running seats remaining (`R49ExecFdB`, `R49ExecGates`, `R49ExecLiveCensus`, `R49ExecSelfAssess`,
`R49RevCounter`, `R49RevMarks`, `R49ScribeCoverage`, `R49SentSeat-3`) plus the L1's `l1/` and
`l1-check/`. The two residues in this report are unchanged and are the only scratch findings:
`R49ScoutCmd-srcpreview.md` (248,933 B, mtime `14:19:32`) and the empty `counter-c3/` (mtime
`14:24:14`). My own `/fast/scratch/hyaku/tsukuroi-r49/R49SentScopeB/` was removed after the receipts
were copied.
