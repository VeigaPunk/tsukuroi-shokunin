Verdict: survives with defects. Attacked: C2 (the pause-lift gate count, `python3 tools/check-pause-gate.py --revision <REV>`) at landed commit 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0 and at base f169b3ba9a59abaf3e324c1b591e1e07a4d6003a, plus its capture sha256 pin. The count reproduces exactly: 5 verified premises and exit 0 at the commit, 0 and exit 1 at the base, byte-identical to the measure files, and the pin equals the committed capture bytes. The count is reproducible only from a clean tree, and several statements in the gate entry are not backed by the pinned capture.

## Confirmed by rerun

| Run | Tree used | Result | Exit | Output |
|---|---|---|---|---|
| Landed 22fd1642 | lane root, 06:03:20 -03 (tracked files clean) | PASS, premises_verified 5 of 5, findings [] | 0 | `.ufo/waves/round-24/w2/RevGateRerun/c2-22fd1642.rerun.out` |
| Landed 22fd1642 | fresh clone at 22fd1642 (clean) | same bytes | 0 | `/fast/scratch/hyaku/tsuku24w2-RevGateRerun/clone-22fd.out` |
| Base f169b3ba | lane root, 06:03:20 -03 | FAIL, premises_verified 0, GATE-MISSING at `corpus/knowledge/pause-lift-gate-r24.json` | 1 | `.ufo/waves/round-24/w2/RevGateRerun/c2-f169b3ba.rerun.out` |
| Base f169b3ba | fresh clone | same bytes | 1 | `/fast/scratch/hyaku/tsuku24w2-RevGateRerun/clone-f169.out` |

- Byte comparison: `cmp` reports each lane and clone output identical to `.ufo/waves/round-24/measure/c2-22fd1642.json` (729 bytes) and `c2-f169b3ba.json` (247 bytes). Both measure files are untracked at HEAD (finding 5).
- Per premise at 22fd1642: P1 changed (S087, S088, S089), P2 cleared (S092, S089), P3 changed (S094 to S098), P4 changed (S099, S100, S101, S103), P5 changed (S090, S091, S093, S102). Each has `verified: true` and no problems.
- Capture pin: the committed capture blob (`.ufo/waves/round-24/capture/l1-4/capture.txt`, 21852 bytes, blob 213056c44fc2698be4bcdce8c9f7a067d41dc398) hashes to 87f70f82f05956ce5de60abe8bfdd748f38d716483a491cfe7c183939884a56f. The same value is in the committed gate JSON (`corpus/knowledge/pause-lift-gate-r24.json` line 5, `capture_sha256`), in `capture.sha256`, and in the working-tree file. The gate JSON blob is 8083 bytes, sha256 279f2b7811d4a4b4083fb51b555cac0ad0d8b865ec45d8999c5b27b7b7a9f2ef. The measure JSON files carry no hash field, so "the capture sha256 in the JSON" refers to that gate field.
- Data read from commits: in the clone I overwrote the working-tree gate JSON with `{}` and the working-tree capture with one line. The landed count stayed 5 with exit 0 (`tamper-22fd.out`). After restoring both files, the output was byte-identical to the measure file again. From the other side, the working-tree gate file exists, yet the base count reads GATE-MISSING.
- Pointer cross-check (my own pass over committed bytes): all 31 evidence pointers (P1 6, P2 4, P3 9, P4 5, P5 7) resolve at 22fd1642 under both splitlines and split-on-newline rules. The capture has no carriage return, form feed or other unusual line break. Only S087 to S103 were opened 2026-10-22; all are `mined`; SOURCES.md has 86 rows at base and 103 at the commit.
- Self-test in the clone: `python3 tools/check-pause-gate.py --selftest` gives status PASS, 24 cases, 0 failed, exit 0.
- Caller check in the clone: `python3 tools/check-registry-coverage.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0 --audit-live-map` gives PASS, 26 rows, 0 missing, 0 findings, exit 0.

## Findings

1. **High** [obs]. The count runs the working-tree checker, and an uncommitted edit already changes the result at the same commit.
   - The lane is no longer clean. `git diff --stat` lists six modified tracked files, including `tools/check-pause-gate.py` (6 insertions, mtime 06:09:38). The insertion at working-tree lines 249 to 254 reads the tool's own blob at the revision and returns CANNOT_EVALUATE with GATE-SELF-BINDING when the bytes differ.
   - Lane command now: `python3 tools/check-pause-gate.py --revision 22fd1642…` gives exit 2 and `{"status": "CANNOT_EVALUATE", "revision": "22fd1642…", "findings": [{"id": "GATE-SELF-BINDING", "site": "working-tree checker differs from the revision blob"}]}` (`.ufo/waves/round-24/w2/RevGateRerun/lane-now-22fd1642.out`). The base now gives exit 2 with "tool absent at this revision" (`lane-now-f169b3ba.out`), not the exit 1 GATE-MISSING seen at 06:03.
   - The committed checker has no such check. Committed `tools/check-pause-gate.py` lines 232 to 252 pass the revision's bytes straight to `evaluate` and never compare the running file. C1's tool does bind itself (SCORECARD.md:762, "The tool now reads itself from the revision"). C2 has no equivalent statement.
   - Smallest correction: commit the same self-binding for C2, then measure C2 at that new commit, where the blob matches. Until then, cite only a clean-tree run (the 06:03 lane run or the clone) and record the checker blob sha256 used. Residual gap: finding 11.

2. **Medium** [obs]. The Snapper rollback claim is not backed by the pinned capture.
   - Gate JSON line 228 says "Remaining rollback paths: the Arch Linux Archive and the two read-only Snapper snapshots of 2026-10-20". The same claim appears at `SKILL.md:2249` ("rollback only through the Arch Linux Archive or the 2026-10-20 Snapper snapshots") and at gate `.md` lines 56 and 57.
   - The pinned capture holds only the unprivileged read: `capture.txt:310-313` shows `snapper -c root list` returning "No permissions.", and the committed `capture.sh:52` runs without sudo. `snap-pac` is absent (`capture.txt:315-317`).
   - The two-snapshot fact comes from a root-run `sudo -n snapper list` in the wave-1 report (`.ufo/waves/round-24/w1/ExecRollbackPaths.md:49-50`). That run is not in `capture.sh` and is not pinned.
   - The count does not use this claim (no pointer depends on it), so the 5 is unaffected. The operator's rollback advice is not reproducible from the pinned evidence.
   - Smallest correction: qualify the four loci as "wave-1 root read, not in the pinned capture". Stronger fix: add a root `snapper -c root list` line to `capture.sh` and re-capture under a new pin (L1 decision).

3. **Medium** [obs] with [inf] on origin. The ca-certificates-mozilla security-fix claim rests on an unpinned file that the committed script does not produce.
   - Gate JSON line 48 (P1 limits) names the security fix. The P1 pointer at lines 38 to 40 points to `l1-4/checkupdates.out` line 6. The same claim appears at gate `.md` line 23 and `SKILL.md:2245`.
   - `capture.txt` has no ca-certificates row (grep count 0). The committed `capture.sh` grep at line 61 does not list the package.
   - The committed `capture.sh` writes checkupdates output only to `/fast/scratch/hyaku/tsuku24-checkupdates-db.out` (line 61). No committed command writes `checkupdates.out` into the capture directory, so the copy in the lane came from a manual step or another script that is not recorded [inf].
   - `capture.sha256` pins only `capture.txt`. The checker accepts any committed path as evidence (`tools/check-pause-gate.py:127-145`), so the security-fix statement is unpinned.
   - Smallest correction: qualify the four loci as "unpinned copy of checkupdates.out". Stronger fix: pin `checkupdates.out` by sha256 in the gate JSON and check it in the checker, or add the package to the capture grep and re-capture.

4. **Low** [obs]. The `capture.sh` header is inaccurate, and the working-tree script has drifted from the one that produced the pin.
   - Committed `capture.sh` lines 3 and 4 say "the only writes are capture.txt and capture.sha256 inside a new output directory". Line 61 also writes to `/fast/scratch`.
   - The uncommitted edit (diff stat: 18 changed lines) adds boot-ID redaction in the `boots` section, sudo-line filters, sed redaction of cache paths, and a `checkupdates.out` write into the output directory. The pinned l1-4 capture predates the edit: `capture.txt:13-16` still shows raw boot IDs.
   - Gate `.md` line 3 and `SKILL.md:2252` name `capture.sh` as the recheck procedure. The next recheck would therefore not reproduce the pinned bytes.
   - Smallest correction: restore the committed header wording to list the `/fast/scratch` write. Commit any redaction change only together with a new capture and a new pin.

5. **Low** [obs]. The measure evidence is not in the commit.
   - `git ls-files .ufo/waves/round-24/measure | wc -l` prints 0, and `git status` shows `?? .ufo/waves/round-24/measure/`. The c1 and c2 measure files are therefore not in 22fd1642.
   - Smallest correction: commit the measure directory with the measured appendix, at the commit it describes.

6. **Low** [inf]. `premises_verified` counts valid evidence links, not true premises, and the verdict labels are not checked mechanically.
   - P5's premise (gate JSON line 183, "A rollback by package cache is available, and no package transactions happened during the pause.") is among the five, with verdict "changed" (line 184). The same entry says both halves are false (gate `.md` line 58; JSON line 228).
   - `SKILL.md:2285` correctly says "committed-bytes evidence link count only". The risk sits in the wording of SCORECARD.md:749 and in the field name.
   - Smallest correction: no code change. In the measured appendix write "5 premises with valid evidence links" and state that verdict truth is not measured.

7. **Low** [obs]. SCORECARD.md line 744 says C2 "reads only this round's host capture and newly opened sources". That is not what the checker does.
   - The checker also reads the gate entry (`tools/check-pause-gate.py:79`), all of `corpus/SOURCES.md` (line 97), and every evidence path, which here includes `checkupdates.out` (lines 127 to 145).
   - Smallest correction: "C2 reads the gate entry, corpus/SOURCES.md and the committed files its evidence pointers name."

8. **Low** [obs]. The C2 axis is stated two ways in the declaration.
   - SCORECARD.md line 749 says "freshness 8 → 8 (tied lowest)". The appended refinement at line 759 says the axis is "depth 8 → 8 (tied lowest)" and that freshness was 9. The table row cannot be edited (append-only), so both statements remain visible.
   - Smallest correction: the measured appendix records depth 8 → 8 and cites line 759 as the reason.

9. **Low** [inf]. The "before" value is the landed checker reading base bytes, not a checker that exists at the base.
   - SCORECARD.md line 760 says "the counting command at f169b3ba: the checker and the gate entry are absent there, so 0 premises are verified." The command cannot be run from the base tree. The 0 comes from the landed checker over base bytes: exit 1 GATE-MISSING at 06:03, and exit 2 CANNOT_EVALUATE now (finding 1).
   - Smallest correction: write "landed checker over f169b3ba bytes: GATE-MISSING, premises_verified 0, exit 1", and record the checker blob sha256.

10. **Low** [unk]. The pause-origin citation points outside the lane.
    - Gate `.md` line 8 cites "fleet /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md lines 54-55". The lane's own `.ufo/l0-questions.md` has 2 lines at 22fd1642 (checked with `git show`), so the lane cannot verify the citation. I did not open the fleet file, which is outside this seat's bounds.
    - Smallest correction: label it an external fleet reference that the lane has not verified, or cite the lane file that was meant.

11. **Low** [inf]. Binding residual: `tools/_revision.py` is still loaded from the working tree.
    - `tools/check-pause-gate.py:28` imports `_revision` from the lane root. The uncommitted self-binding (finding 1) covers only `check-pause-gate.py`. `git status` shows no `_revision.py` edit today, so there is no current effect.
    - Smallest correction: bind `_revision.py` the same way, or record its blob sha256 in the appendix.

## Residual risk and verification gaps

- Non-anchor evidence pointers keep only the three-character and substring rules (`tools/check-pause-gate.py:141-145`). The uniqueness and boilerplate rules apply to the anchor pointer only, so a premise can carry extra weak pointers without changing the count. Sibling seat MutGateUniquePointer covers this; I did not test it.
- Exit 1 covers both GATE-MISSING and an honest below-target count. The appendix must read `status` and `premises_verified`, not the exit code alone. RevGateSchema finding 7 (`.ufo/waves/round-24/w1/RevGateSchema.md`) remains open.
- Not examined by this seat: QUALITY criteria 54 to 56, the round-24 lesson file, the README, package-state-plane and partial-upgrade notices, the 17 source URLs and quotes, the 1399-package sweep cited at gate `.md` line 29, and the pin mutation test (MutGateCapturePin's scope).
- I did not run `capture.sh`. Its host reads are time-dependent and would not reproduce the pinned bytes.
- Lane modifications: after my 06:03 run, the lane gained uncommitted edits to `tools/check-pause-gate.py`, `tools/report-red-causes.py`, `.ufo/waves/round-24/capture/capture.sh`, `corpus/lessons/round-24.md`, and two wave-1 files (mtimes 06:07 to 06:10 where I checked). I did not make them and cannot tell from here who did. The L1 should confirm the state before committing.

Scope: read=/home/vgpnk/.omp/agent/RULES.md; SCORECARD.md lines 744-763; SKILL.md lines 2239-2285; corpus/knowledge/pause-lift-gate-r24.json and .md (committed bytes and working tree); corpus/SOURCES.md rows S087-S103 (committed bytes); tools/check-pause-gate.py and tools/_revision.py (committed bytes and working tree); tools/report-red-causes.py (diff only); tools/check-registry-coverage.py (clone run only); .ufo/waves/round-24/capture/capture.sh (committed bytes and working tree), capture/l1-4/capture.txt and checkupdates.out; .ufo/waves/round-24/measure/c2-22fd1642.json and c2-f169b3ba.json; .ufo/waves/round-24/w1/ExecRollbackPaths.md (lines 47-57), RevGateSchema.md, ExecPauseGateChecker.md and CritPauseEvents.md (context only); .ufo/waves/round-24/w2/MutC1SelfBinding.md (context only); lane git state (status, diff, refs, ls-files, show, cat-file) read-only; no fleet-repo paths read; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevGateRerun.md and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevGateRerun/ (c2-22fd1642.rerun.out/.err, c2-f169b3ba.rerun.out/.err, lane-now-22fd1642.out/.err, lane-now-f169b3ba.out/.err), /fast/scratch/hyaku/tsuku24w2-RevGateRerun/ (clone of the lane at 22fd1642 with its own git objects; clone-22fd.out/.err, clone-f169.out/.err, clone-selftest.out/.err, tamper-22fd.out/.err, restored-22fd.out/.err, registry-22fd.out/.err); executed=`python3 tools/check-pause-gate.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0` and `--revision f169b3ba9a59abaf3e324c1b591e1e07a4d6003a` in the lane (06:03 and again later, both exit codes recorded) and in the clone; `python3 tools/check-pause-gate.py --selftest` (clone); `python3 tools/check-registry-coverage.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0 --audit-live-map` (clone); `git clone -q` of the lane into the scratch clone and `git checkout -q 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0` in the clone; overwrite and `git checkout -q --` restore of two working-tree files in the clone; read-only git in the lane (rev-parse, merge-base --is-ancestor, show, cat-file, log, status, diff, diff --stat, grep, ls-files, branch -a); sha256sum, cmp, wc, stat, ls, find -newer; read-only Python snippets over committed blobs (no writes).
Installs: none
