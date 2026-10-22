Attacked QUALITY criterion 54 (R24-SUMMARY-RECALL) at commit 22fd1642 on its three claims (failing example, cited selftest case, frozen-grammar non-widening): survives with defects. The failing example is real and the grammar is not widened, but the "shown able to fail" claim is falsified: the cited selftest case `unknown-key-renamed` passes under every label-rule breakage I ran.

Evidence conventions. [22fd1642] marks a committed blob read with `git show 22fd1642:<path>`; it matches my private clone /fast/scratch/hyaku/tsuku24w2-RevQuality54/lane at that commit, and its line numbers are the committed ones. The lane working tree has drifted since I started (finding 8). corpus/QUALITY.md, the round-23 data files and the round-24 lesson rows I cite are unchanged in the working tree, so they are cited by lane path.

## Findings, by severity

1. HIGH. The cited selftest case does not test the label rule. [obs]
   Criterion text, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:107: "Shown able to fail: `python3 tools/report-red-causes.py --selftest` case `unknown-key-renamed`."
   The same false claim is in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-24.md:47 (row R24-KEY-RECOLLECTION): "selftest case `unknown-key-renamed` fails when the label rule is broken."
   Why the case cannot see labels: [22fd1642] tools/report-red-causes.py:230-231 builds a trace with no `__unknown_argument__` token and expects exit 1. Line 181, "and all(s['unknown_tokens'] > 0 for s in unknown_sites) and bool(unknown_sites)", makes the result false before any label is read. Line 240, "label_ok = name != 'pristine' or ...", is true for every case except `pristine`, and line 241 folds it into every case's pass test, so it never changes the outcome of `unknown-key-renamed`. Replaying the fixture on committed code (Python harness, constructed from lines 214-236): exit 1, preserved false, unknown_tokens [0]; the labels come out as five unlabelled names plus `other` labelled, but nothing asserts them.
   Mutation test. Each mutant is a private clone with one line changed; each was run with `python3 tools/report-red-causes.py --selftest`. `git diff --stat` shows one insertion and one deletion for each.

   | Mutant (committed line changed) | Selftest exit | Failing selftest cases | Case `unknown-key-renamed` | Real-input run: exit, preserved |
   |---|---|---|---|---|
   | Pristine at 22fd1642 | 0 (PASS, 11 cases) | none | pass | 0, true |
   | A: line 164 becomes `'label': None})` | 1 | pristine, stub-pristine | pass | 1, false |
   | B: line 164 becomes `'label': LABEL if key in site_keys else None})` | 1 | pristine, stub-pristine | pass | 1, false |
   | C: line 164 becomes `'label': LABEL})` | 1 | pristine | pass | 0, true (four present keys labelled) |
   | D: line 159 reads keys from every event of every seat | 0 | none | pass | 0, true |
   | E: line 181 drops `all(s['unknown_tokens'] > 0 ...)` | 1 | unknown-key-renamed | fail | 0, true |
   | F: line 34 shortens LABEL to `author recollection, not recoverable` | 0 | none | pass | 0, true (short label accepted) |

   The real-input runs call the tool's attribute() on the committed inputs; the revision binding and pin checks were run separately, through the command line, on the pristine tree only.
   In mutants A, B and C only `pristine` fails (A and B also fail `stub-pristine`). The real run catches A and B through lines 182-183, which set preserved to false and exit to 1, but it does not catch C. Mutant E shows the cited case does respond, but to the removal of the unknown-token check, which guards a different invariant: that `__unknown_argument__` stays visible at the site.
   Smallest correction: in QUALITY.md:107 and lessons/round-24.md:47, replace "case `unknown-key-renamed`" with "case `pristine` (its label check, tools/report-red-causes.py:240)". Optional tool change if the lane owner wants the cited case to test labels: extend `label_ok` to `unknown-key-renamed` with the expected list `[None]*5 + [LABEL]`, which is the list the replay produced.
   The wave-1 draft had this right. /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ScribeLessonMistakes/round-24-mistakes.md:22 reads "The latter pristine fixture also checks the recollection label." The committed lesson row changed that to the wrong case.

2. MEDIUM. The scope of "the retained bytes it summarizes" is undefined, and the tool implements a third scope. [obs]
   Three scopes appear in the corpus. The lesson routing row, lessons/round-24.md:35, says the label goes on "each name absent from the flagged site's retained event". The tool docstring, [22fd1642] tools/report-red-causes.py:9-10, says "labelled as author recollection wherever a name is absent from the retained events". The tool code, [22fd1642] tools/report-red-causes.py:157-159, builds `site_keys` as the union of `retained_keys` over every schema-finding site. Criterion 54 says only "the retained bytes it summarizes".
   Constructed checks (Python harness on committed inputs; they change nothing in the corpus):
   (a) `replace_all` added to the args of FxC1DeclaredEdit event 0, with no finding at that site. Result: still labelled (in_retained_site_event false). This contradicts the docstring reading "absent from the retained events".
   (b) The same name added at a second schema site, FxC1DeclaredEdit:0. Result: `replace_all` has in_retained_site_event true and no label, and preserved is true. The cited site FxC3Build08:17 keeps only ['__unknown_argument__', 'i', 'new_string', 'old_string', 'path'], so a limit file could pass the rule through another site.
   Corpus scale. `git grep -l replace_all 22fd1642 -- .ufo/waves/round-23` lists 11 files: nine critic, draft or build reports (for example .ufo/waves/round-23/falsify/FxC2SchemaV2.md:75, "`replace_all` is a real, documented parameter of the harness `edit` tool"), plus falsify-limit.json and integration.json. Read broadly, "retained bytes" would mean the label never applies. The spot-check's own wording (corpus/lessons/round-23-verifier-spotcheck.md:52, "not independently recoverable from those retained event bytes") points to event records.
   Smallest correction: in criterion 54, replace "the retained bytes it summarizes" with "the recorded argument keys of the event at the site the file names (for falsify-limit.json, `schema_site` at line 7)". In the tool, build `site_keys` only from `limit['schema_site']`, and change the docstring at lines 9-10 and lesson line 35 to match.

3. MEDIUM-LOW. The label text the criterion quotes is not pinned by any check. [obs]
   Mutant F (table above) changes LABEL at [22fd1642] tools/report-red-causes.py:34 to 'author recollection, not recoverable'. The selftest still exits 0 with all 11 cases passing, and the real-input run still reports preserved true. Line 240 compares labels to the constant `LABEL`, not to the criterion's literal string.
   Smallest correction: add one literal assertion to the selftest, for example `assert LABEL == 'author recollection, not recoverable from retained events'`.

4. LOW-MEDIUM. The gate's label clause is one-sided. [obs]
   [22fd1642] tools/report-red-causes.py:182 reads "and all(r['in_retained_site_event'] or r['label'] == LABEL for r in recollection))". It accepts a label on a name the site retains. Mutant C's real-input run exits 0 with preserved true while labelling i, new_string, old_string and path, which the site does retain.
   Smallest correction: require agreement in both directions, `and all(r['in_retained_site_event'] == (r['label'] is None) for r in recollection))`.

5. LOW-MEDIUM. The criterion claims more than it demonstrates or checks. [obs]
   QUALITY.md:107 covers "a key, count, site or version". The only demonstration and the only implemented check cover `schema_original_keys`. Nothing checks the counts or sites in falsify-limit.json (falsify_request_count 1647, native_completed 76, trace_complete 75, path_findings 266, edit_requests 63, schema_site on line 7). A wave-1 reviewer checked those counts by hand: .ufo/waves/round-24/w1/RevC1Attribution.md:40.
   Smallest correction: narrow criterion 54 to named keys, or state that counts, sites and versions are reviewer-checked and have no control yet.

6. LOW. Failing-example wording and the status of the frozen file. [obs]
   (a) "keeps only `__unknown_argument__`" (QUALITY.md:107). The event at FxC3Build08:17 is events[17] of seat FxC3Build08 in .ufo/waves/round-23/falsify/events.json. The seat has 18 events, so index 17 is the last. A jq query on the file returns `{"n":18,"e17":{"tool":"edit","args":{"i":null,"path":"…/FxC3Build08.md","old_string":null,"new_string":null,"__unknown_argument__":null},"request_line":53,…}}`. The event keeps four other keys; only the extra key is replaced by the marker. The failing example is otherwise real: falsify-limit.json:13 lists "replace_all" under "schema_original_keys" (lines 8-14), and `git show 22fd1642:.ufo/waves/round-23/falsify/events.json | grep -c replace_all` printed 0 (exit 1).
   (b) The failing example is the frozen falsify-limit.json itself, which lists replace_all with no label. The criterion does not say whether frozen artifacts are exempt. The label appears only in derived output, .ufo/waves/round-24/measure/c1-22fd1642.json, field `schema_original_keys`.
   Smallest correction: change the wording to "keeps `__unknown_argument__` in place of the extra key; the other four keys stay". Add "frozen artifacts are not edited; the label is carried by derived reports."

7. LOW. [inf] "contain that name" is a byte test in the criterion but a key test in the tool. Under the literal wording a name that appears only inside a string value would count, while the tool would not count it. The failing example is not affected (zero byte matches).
   Smallest correction: "record that name as an argument key of that event".

8. MEDIUM for the lane owner, outside the committed revision. The lane has uncommitted edits, and the committed command no longer runs there. [obs]
   `git status --short` shows ` M tools/report-red-causes.py` and ` M corpus/lessons/round-24.md`. `git diff --stat` shows five changed files, 24 insertions and 15 deletions, which also include .ufo/waves/round-24/capture/capture.sh, .ufo/waves/round-24/w1/ExecPacmanLogCensus.md and .ufo/waves/round-24/w1/ExecRecapture/cap-head/capture.txt. The tool file's mtime is 2026-10-22 06:11:20 -0300.
   The working-tree docstring now says "absent from the flagged site's retained event", but the working-tree label code (lines 165-172) still unions every schema-finding site, so the new docstring is not implemented. The working tree also adds a selftest case `no-incomplete-seat`, which I did not evaluate.
   Running `python3 tools/report-red-causes.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0` inside the lane now exits 2 with `{"status": "CANNOT_EVALUATE", "findings": [{"id": "RED-CAUSES-READ", "site": "working-tree report tool differs from the revision blob"}]}`, from the self-check at lines 193-194. Lane HEAD is still 22fd1642.
   Smallest correction: the lane owner either commits the edits and re-runs the selftest and the revision command at the new commit, or reverts them. The docstring must match whichever scope rule finding 2 settles on.

## Checks that survived

- Failing example is real. falsify-limit.json:7 has "schema_site": "FxC3Build08:17", and :13 lists "replace_all". The committed sha256 values e8e22aae… (falsify-limit.json) and 52a5021b… (events.json) match the pins at tools/report-red-causes.py:38-39. Lesson pointers resolve: lessons/round-24.md:41 starts "## Mistakes" and row 47 follows it; round-23-verifier-spotcheck.md:52 holds the falsify-limit paragraph.
- Label string is identical. QUALITY.md:107 and tools/report-red-causes.py:34 both read "author recollection, not recoverable from retained events". The missing literal check is finding 3.
- Frozen grammar is not widened. The checker blob 9b5ef9f2 is the same at f169b3ba and 22fd1642, and `git diff --stat f169b3ba 22fd1642` lists no checker change. Its sha256, 35079db5…, is pinned at tools/report-red-causes.py:36, and a mismatch exits 1 (lines 209-210). The only edit shapes are tools/check-seat-bindings.py:116, "EDIT_SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'})", and line 121 rejects any other key set. No tool file contains replace_all except the selftest fixtures (tools/report-red-causes.py:224, 230-231). The label is computed only in attribute() (lines 163-164); it feeds the report output and the preserved clause (lines 182-183), and no code path admits a key from it.
- Status, exit and incomplete seat are preserved. The committed real run gives checker_status CANNOT_EVALUATE, checker_exit 2, incomplete seat ConnFxPlanner (incomplete_seat_is_frozen true), and exit 0 with preserved true.

## Residual risk and verification gaps

- Only the committed revision was evaluated. The lane's uncommitted edits (finding 8) were not evaluated, and the revision command currently fails in the lane.
- Mutation coverage is six single-line mutants (A to F) plus constructed replays. That is not proof that the selftest catches every label fault.
- Constructed checks (a) and (b) in finding 2 are not observed in the corpus. On the committed data they change nothing: there is one schema site and no replace_all in events.json.
- Criteria 55 and 56 and the C1 counts were not reviewed, except where criterion 54 needed them.
- I did not identify who made the working-tree edits at 06:11 (no process record was available).

Scope: read=committed 22fd1642 blobs (corpus/QUALITY.md, corpus/lessons/round-24.md, corpus/lessons/round-23-verifier-spotcheck.md, tools/report-red-causes.py, tools/check-seat-bindings.py, tools/_revision.py), round-23 falsify and measure files, the round-24 measure file c1-22fd1642.json, wave-1 reports under .ufo/waves/round-24/w1/, the SCORECARD round-24 sections, /home/vgpnk/.omp/agent/RULES.md and the godspeed skill; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevQuality54.md, plus private scratch files under /fast/scratch/hyaku/tsuku24w2-RevQuality54/ (lane clone at 22fd1642, mutant clones mutA to mutF, real-run-22fd.json, mutX-selftest.json); executed=`git clone -q` of the lane into scratch and `git checkout -q 22fd1642…` there; `python3 tools/report-red-causes.py --selftest` in the clone (exit 0, PASS, 11 cases); `python3 tools/report-red-causes.py --revision 22fd1642…` in the clone (exit 0, preserved true, 268 of 268 attributed); six mutant selftests (exit 1, 1, 1, 0, 1, 0) with `git diff --stat` in each clone; a Python harness calling attribute() on committed inputs for the lane and mutants A to F, the two constructed checks, and the fixture replay; read-only lane git (rev-parse, log, status, diff, show, grep -l, ls-tree, hash-object, check-ignore, diff --stat f169b3ba 22fd1642); `python3 tools/report-red-causes.py --revision 22fd1642…` run inside the lane (exit 2, self-check, no writes); glob and stat on two lane __pycache__ files, which predate this session and are gitignored, so I left them.
Installs: none
