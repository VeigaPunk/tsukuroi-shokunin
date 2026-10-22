Verdict: survives with defects. Attacked the C1 `causes` array (the per-cause subcause table) in `.ufo/waves/round-24/measure/c1-22fd1642.json`, recomputed independently from the frozen round-23 falsify bytes at commit 22fd1642. All 11 rows, all 268 per-finding subcauses and every distinct-seat count reproduce exactly. The defects are in the labels, in the output's committed status, and in the lane working tree; none of them changes a count.

## 1. Method

- Frozen inputs, all tracked at 22fd1642 and clean in the lane (`git status` shows no change under `.ufo/waves/round-23`). Their sha256 values equal the pins in `c1-22fd1642.json` `inputs`:
  - `.ufo/waves/round-23/falsify/bindings.json` = 8c72460b…
  - `.ufo/waves/round-23/falsify/events.json` = 52a5021b…
  - `.ufo/waves/round-23/measure/post-falsify/falsify-limit.json` = e8e22aae…
  - `tools/check-seat-bindings.py` = 35079db5… (unchanged between f169b3ba and 22fd1642)
- Independent code: `.ufo/waves/round-24/w2/RevC1Subcauses/recompute.py`. It restates the frozen grammar from `tools/check-seat-bindings.py` and does not import `tools/report-red-causes.py`. The grammar it uses:
  - A lane-local path starts with the lane root plus "/". It has no backslash and no control characters, none of `* ? [ ] ; :`, and no empty, "." or ".." segment (checker `local()`, lines 33-36).
  - For read and grep, a trailing selector is removed first when every token is a valid selector. Grep and glob values are split on ";" first (checker `requested_path()` 43-58, `classify()` 61-113).
  - Each denied value gives one finding. A subcause is the branch that produced the denial: no lane prefix ("outside the lane root"); lane prefix but fails the grammar (split by whether the text before "?" and then ":" is a declared path of the seat); lane-local and well formed but not in the seat's list for that operation ("not bound").
  - Edit calls use the v2 rule (checker `classify_edit()` 119-130). Output: `recomputed-findings.json`, 268 rows.
- Oracle: the frozen checker, unchanged, run in a private clone at 22fd1642 (`/fast/scratch/hyaku/tsuku24w2-RevC1Subcauses/lane`) with `--revision 22fd1642… --manifest .ufo/waves/round-23/falsify/bindings.json --events .ufo/waves/round-23/falsify/events.json`. Result: exit 2, CANNOT_EVALUATE, 268 findings (266 SCOPE-PATH-DENIED, 1 SCOPE-SCHEMA, 1 SCOPE-TRACE-INCOMPLETE). Saved as `checker-22fd1642-falsify.json`.
- Reproduction of the committed tool: the HEAD copy of `tools/report-red-causes.py`, run in the same clone with `--revision 22fd1642…`, gives JSON equal to `c1-22fd1642.json` in every top-level key (`report-head-rerun-in-clone.json`).

## 2. Recomputed subcause table

| Finding | Operation | Subcause (checker branch) | Findings | Distinct seats | Matches committed row |
|---|---|---|---|---|---|
| SCOPE-PATH-DENIED | read | outside the lane root | 11 | 9 | yes |
| SCOPE-PATH-DENIED | grep | outside the lane root | 2 | 1 | yes |
| SCOPE-PATH-DENIED | write | outside the lane root | 2 | 1 | yes |
| SCOPE-PATH-DENIED | read | inside the lane, spelled outside the frozen grammar, base path declared | 100 | 10 | yes |
| SCOPE-PATH-DENIED | read | inside the lane, spelled outside the frozen grammar, base path undeclared | 77 | 3 | yes |
| SCOPE-PATH-DENIED | glob | inside the lane, spelled outside the frozen grammar, base path undeclared | 5 | 1 | yes |
| SCOPE-PATH-DENIED | read | inside the lane, well formed, not bound to the seat | 42 | 5 | yes |
| SCOPE-PATH-DENIED | grep | inside the lane, well formed, not bound to the seat | 26 | 5 | yes |
| SCOPE-PATH-DENIED | glob | inside the lane, well formed, not bound to the seat | 1 | 1 | yes |
| SCOPE-SCHEMA | edit | argument key outside the frozen two-shape edit grammar | 1 | 1 | yes |
| SCOPE-TRACE-INCOMPLETE | none (seat-level) | trace ends before a final message | 1 | 1 | yes, but the label is disputed (F6) |

Totals: 268 = 266 path + 1 schema + 1 seat-level. Path findings fall on 21 distinct seats, which matches `falsify-limit.json` `path_finding_seats` = 21. Per operation: read 230 of 1237 events denied, grep 28 of 263, glob 6 of 6, write 2 of 78, edit 1 of 63 (schema only). These match the per-tool counts in `falsify-limit.json` and `events.json`.

## 3. Comparison with the committed `causes` array

- Rows: 11 committed, 11 recomputed. Finding, operation, subcause, count and distinct-seat count agree in all 11. No row is missing or extra. **Disagreement at count, seat or subcause level: none.**
- Per-finding rows (`per_finding`, 268): the (site, finding, operation, subcause) tuples equal my 268 tuples in both directions. The join keys (call_id, request_line, tool) equal the event at the site index in 268 of 268 rows.
- Oracle: the 268 (site, finding id) pairs from the frozen checker equal my 268 pairs.
- Verified in the committed output: `unknown_argument_sites` keeps `__unknown_argument__` at FxC3Build08:17; `incomplete_seats` keeps ConnFxPlanner; `checker_exit` 2; `checker_status` CANNOT_EVALUATE.

## 4. Checks that held (no defect)

- The declared/undeclared split is robust. Of 182 in-lane spelled-outside values (100 declared, 82 undeclared), the split is identical under three base definitions: the tool's (text before the first "?", then before the first ":"), a stricter "declared for this operation" test, and a cut at the first of "?", "&", ":", "#". All 100 declared bases are in the seat's read list; none is a write-only path.
- The "declared for the other operation only" branch of the HEAD tool fires 0 times, so no "well formed, not bound" row hides a write-only declared path.
- The six grep events with ";" in `path` are fully bound and produce no findings, so per-event labelling cannot mix subcauses in this data.
- `falsify-limit.json` reconciles: `falsify_request_count` 1647 (events.json holds 1647), `edit_requests` 63, `path_findings` 266, `native_completed` 76 (`native-outcomes.json` lists 76 entries with status completed), `trace_complete` 75.
- The spelled roots in the outside-the-lane rows are not lane directories. I tested `/home/vgpnk/Projects/shokunin/` with `[ -e ]` for `tsukuroi-showin`, `tsukuroi-shokuroi`, `tsukuroi-shokuroi-shokunin`, `tsokuroi-shokunin` and `tsukuroi-shokunun`. All five are absent. [obs]

## 5. Findings

**F1. [obs] The lane working tree has uncommitted edits to the C1 tool. As it stands, the claimed counting command would fail closed in the lane [inf], and the edits would also change the labels.**
- Evidence: `git status --short -- tools` shows ` M tools/report-red-causes.py` and ` M tools/check-pause-gate.py`. The working-tree report tool is 17507 bytes, sha256 c13bb464…, mtime 2026-10-22 06:11:20. The committed blob is 15840 bytes, sha256 39df6041…, the same as `git show HEAD:tools/report-red-causes.py | sha256sum`.
- Wider churn at the last check: `git status --short` listed 19 modified tracked paths and 8 untracked paths (for example SKILL.md, corpus files, and round-24 w1 and capture files). The frozen inputs under `.ufo/waves/round-23`, `tools/check-seat-bindings.py`, `tools/_revision.py` and `SCORECARD.md` were unchanged, and HEAD is still 22fd1642.
- The HEAD tool refuses to run on a dirty copy. Its `run()` compares the working-tree file with the revision blob and raises "working-tree report tool differs from the revision blob" (HEAD code, `run()`). I tested this in my own clone: I placed the working-tree bytes at the clone's `tools/report-red-causes.py` and ran the claimed command. Output: `{"status": "CANNOT_EVALUATE", "findings": [{"id": "RED-CAUSES-READ", "site": "working-tree report tool differs from the revision blob"}]}`, exit 2 (`mutant-wt-tool-at-lane-root-command.json`). I then restored the clone with `git checkout -q`, and the restored run matched the first HEAD run byte for byte (`restored-head-tool-rerun.json`). I did not run the command inside the lane. [inf] The lane run would fail the same way, because the check compares the same bytes.
- If the working-tree version were committed, the labels would change. I ran a copy of it under another file name, so its self-check compared the clone's committed copy and passed. Result (`report-worktree-snapshot-run-in-clone.json`): 14 causes rows instead of 11. Eight findings move out of "outside the lane root": four to "dot segments that normalise inside the lane" (grep 2 at FxC1Selftest; read 2 at FxC3Build06 and ConnFxPlanner), and four to "relative path" (read 3 at FxC2OracleLegacy and SentFxPrivacy; write 1 at FxSources). The seat-level label also changes. The working-tree copy has two defects of its own:
  - Line 95 labels the three `redacted-internal-uri` placeholders "relative path". They are neither relative nor paths. The test is only "does not start with /".
  - Line 97 says "normalise inside the lane". The checker never normalises, and the spelled directories do not exist, so the label reads as a resolution claim that is false.
- Smallest correction: the integrator restores `tools/report-red-causes.py` and `tools/check-pause-gate.py` to their committed bytes before any counting run, or commits a reviewed version and re-measures. If the working-tree tool is kept, put a placeholder branch before line 95 and drop the "normalise" wording at line 97. The committed `c1-22fd1642.json` stays valid for the 22fd1642 bytes (F2 and section 3).

**F2. [obs] The committed C1 output is not in the commit it names.**
- Evidence: `git cat-file -t 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0:.ufo/waves/round-24/measure/c1-22fd1642.json` prints "fatal: path … exists on disk, but not in '22fd1642…'" and exits 128. `git ls-files -- .ufo/waves/round-24/measure` prints nothing. `git status --short` lists `?? .ufo/waves/round-24/measure/`. `git show --stat 22fd1642` has no measure file. The same holds for `c2-22fd1642.json` and `c1-f169b3ba.json`.
- The file content is correct: the committed tool reproduces it exactly (section 1), so only the status word is wrong.
- Smallest correction: the integrator commits the measure outputs, or the report stops calling them "committed" and names them as working-tree files with their sha256.

**F3. [obs] "outside the lane root" merges four different spelling families under one label.**
- Evidence: HEAD `tools/report-red-causes.py:90` returns that label for every non-lane spelling. My sub-split (`subsplit.py`, 15 findings, 10 seats):
  - Misspelled lane root, no "..": 5 read findings, 4 seats (FxC2Selftest:20 and :21 spell `tsukuroi-shokuroi-shokunin`; FxC3Pins:2 `tsokuroi-shokunin`; FxKnowReconcile:5 and FxKnowEdit:1 `tsukuroi-shokunun`).
  - Misspelled lane root followed by "/../tsukuroi-shokunin": 4 findings, 3 seats (FxC1Selftest:12 and :13 grep; FxC3Build06:7 read; ConnFxPlanner:28 read).
  - Fleet parent directory, not a lane: 2 findings, 1 seat (FxSources:42 read and :44 write, under `/home/vgpnk/Projects/shokunin/.ufo/`).
  - Relative path: 1 finding, FxSources:38 write.
  - Collector redaction placeholder: 3 findings, 2 seats (FxC2OracleLegacy:17; SentFxPrivacy:13 and :14).
- Smallest correction: split the HEAD label at `tools/report-red-causes.py:90` into four: misspelled lane root (9 findings, 7 seats, 4 of them with "/../"), fleet parent directory (2), relative path (1), collector redaction placeholder (3). The counts do not change.

**F4. [inf] The three placeholder rows receive a lane-root label from a collector rule. Nothing recorded shows what was requested.**
- Evidence: round-23 `collect.py:20-30` (HEAD) replaces any string that contains "://" and is not http(s), not host:port and not exactly `skill://godspeed` with `redacted-internal-uri`. The events therefore cannot show the requested target or its scheme. The checker's denial of the placeholder is real, but a statement about the requested resource is not supported. The lane already says so for this spelling: `.ufo/waves/round-23/falsify/FxC3Falsify03.md` line 71 (R2: "the real target cannot be recovered").
- Smallest correction: give these rows the label "collector redaction placeholder; requested target not recorded" (part of the F3 split). Make no host-side claim about them.

**F5. [obs] The `replace_all` label says "author recollection", but a pinned input records the key.**
- Evidence: the HEAD tool's constant `LABEL` at `tools/report-red-causes.py:34` is applied to every schema key missing from the retained events (HEAD lines 161-164). The key is recorded in `.ufo/waves/round-23/measure/post-falsify/falsify-limit.json` lines 8-14 (`schema_original_keys`, with `replace_all` at line 13). That file is one of the pinned inputs (`inputs` in `c1-22fd1642.json`, sha e8e22aae…). The retained event FxC3Build08:17 holds `__unknown_argument__` because the collector maps unknown keys to that name (`collect.py:58`).
- So "not recoverable from retained events" is true. "Author recollection" is a provenance word that the bytes do not support. The source is an author-written round-23 record. [inf] Whether it came from memory or from the transcript cannot be decided from the lane, and the raw transcript is not in the lane.
- Smallest correction: change `LABEL` to "recorded only in round-23 falsify-limit.json schema_original_keys (author-written, pinned); absent from retained events; not checked against a transcript".

**F6. [unk] The seat-level label names one cause, but the bytes do not establish that cause.**
- Evidence:
  - The ConnFxPlanner seat in `.ufo/waves/round-23/falsify/events.json` has complete = false, `session_exit_line` = null, `native_failure` = null.
  - `.ufo/waves/round-23/falsify/native-outcomes.json` records status "completed" for ConnFxPlanner (duration 36m33s).
  - `SCORECARD.md:734` says the trace "is incomplete despite its observed native completed outcome".
  - The collector's completion gate (`collect.py:280`) is a conjunction of parsed, report_capture_ok and (closed or confirmed_failure or native_final). `native_final` (line 257) needs final assistant text with stop reason stop or end_turn.
  - The HEAD label at `tools/report-red-causes.py:144` ("trace ends before a final message") picks one conjunct and does not say which one failed.
  - The seat transcript (sha256 199767378e…, per events.json) is not on this workstation. A name search of the round-23 coordinator session folder found no ConnFxPlanner file. A wider `find` over /home/vgpnk timed out at its 90-second limit, so absence is not proven.
- Smallest correction: use the wording already in the working-tree copy at line 152, "trace marked incomplete by the collector; which condition failed is not recorded", and show native status "completed" as its own column.

**F7. [obs] The causes array hides that 114 of 266 path findings come from the incomplete seat.**
- Evidence: all 114 are from ConnFxPlanner, whose trace is incomplete (`per_finding` `lower_bound` = true for those rows). Per row, ConnFxPlanner contributes: glob undeclared 5 of 5; grep well formed 14 of 26; read undeclared 67 of 77 (87%); read well formed 27 of 42; read outside 1 of 11. Five of the nine path rows contain incomplete-seat findings. The causes array carries no lower-bound marker; `per_finding` does.
- Smallest correction: add an `incomplete_seat_findings` count to each row, and say "lower bound" in the claim wording for those rows.

## 6. Residual risk and verification gaps

- The lane working tree is changing (F1). My recomputation is pinned to the commit 22fd1642 bytes. The working-tree comparison is pinned to the file sha256 c13bb464… as copied.
- I did not run any command inside the lane. Every run that touched the tool used my private clone.
- The ConnFxPlanner transcript was not found on this workstation, so F6 stays [unk].
- F5 and F4 rest on the lane's own records. Checking them needs the raw round-23 transcripts, which are not in the lane.
- The per-cause labels are checker branches on recorded (collector-projected) spellings. They say nothing about what a seat did on the host. The claim says the same.

## 7. Files

- Recomputation code and outputs, all under `.ufo/waves/round-24/w2/RevC1Subcauses/`: `recompute.py` (main), `subsplit.py`, `check2.py`, `check3.py`, `check4.py`, `recomputed-findings.json`, `checker-22fd1642-falsify.json`, `report-head-rerun-in-clone.json`, `report-worktree-snapshot-run-in-clone.json`, `mutant-wt-tool-at-lane-root-command.json`, `restored-head-tool-rerun.json`.

Scope: read=SCORECARD.md (round-24 sections, lines 740-763, and line 734); lane git metadata (read-only: status, log, show, ls-tree, ls-files, cat-file, diff); tools/report-red-causes.py (HEAD and working-tree copy, read only); tools/check-seat-bindings.py; round-23 falsify bindings.json, events.json, native-outcomes.json, FxC3Falsify03.md, collect.py, measure/post-falsify/falsify-limit.json; round-24 measure/c1-22fd1642.json and c1-f169b3ba.json; a bounded name search of the round-23 session folder and of /home/vgpnk; the /home/vgpnk/Projects/shokunin directory for the misspelled roots. wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevC1Subcauses.md; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevC1Subcauses/ (the files listed in section 7); /fast/scratch/hyaku/tsuku24w2-RevC1Subcauses/lane (private clone at 22fd1642; its tools/report-red-causes.py was restored to HEAD after the mutant test, and one extra copy, tools/report-red-causes-wt-snapshot.py, was added there). executed=`git rev-parse`, `git merge-base --is-ancestor`, `git status`, `git log`, `git show`, `git ls-tree`, `git ls-files`, `git cat-file`, `git diff --stat`, `git clone -q` and `git checkout -q 22fd1642…` (clone only), `git checkout -q -- tools/report-red-causes.py` (clone only); `python3 -B` on recompute.py, subsplit.py, check2.py, check3.py, check4.py, tools/check-seat-bindings.py (clone), tools/report-red-causes.py (clone, HEAD and mutant and restored), tools/report-red-causes-wt-snapshot.py (clone); `sha256sum`, `stat`, `cp` (lane tool to clone), `grep`, `sed`, `ls`, `[ -e ]` checks, `find` (bounded; one run hit its 90-second limit).

Installs: none
