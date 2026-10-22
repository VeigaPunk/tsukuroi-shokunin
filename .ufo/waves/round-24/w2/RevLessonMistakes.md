Verdict: falsified. Attacked corpus/lessons/round-24.md at commit 22fd164: the five mistake rows (evidence pointers, captured-by, and whether each fix can fail as claimed) and the routed-defect table against corpus/lessons/round-23-verifier-spotcheck.md. Evidence pointers survive. Captured-by mostly survives. Two of the five fix demonstrations are false or absent. The routed-defect table is incomplete.

Basis. Every result below uses committed bytes at 22fd164. I cloned the lane to /fast/scratch/hyaku/tsuku24w2-RevLessonMistakes/lane, checked out 22fd164 and ran all tests there. The lane working tree had 21 uncommitted entries at my first check and 32 at my final check, after other seats added files; two of the 32 are my own new report files. The uncommitted edits include corpus/lessons/round-24.md, tools/report-red-causes.py, tools/check-pause-gate.py, .ufo/waves/round-24/capture/capture.sh, SKILL.md and three corpus/knowledge files. I did not judge those edits, except where finding 10 notes them. C1 means the per-cause report (tools/report-red-causes.py). C2 means the pause-lift gate (tools/check-pause-gate.py). Tags: [obs] observed, [inf] inference, [unk] unknown.

Findings

HIGH

1. The "do not elevate" routing for spot-check line 52 is violated in three committed places, and the lesson calls the item fixed.
- [obs] SCORECARD.md:734 says "FxC3Build08:17 carried the unlisted `replace_all` key". corpus/lessons/round-23.md:86 says FxC3Build08:17 contains replace_all alongside path, old_string, new_string and i. LOG.md:1185 lists an unsupported replace_all at FxC3Build08:17 as an observed fact.
- [obs] The retained events hold no replace_all: `grep -c replace_all .ufo/waves/round-23/falsify/events.json` prints 0. The site's retained keys are __unknown_argument__, i, new_string, old_string and path (jq on seat FxC3Build08, event index 17; events.json:14064). The name appears only in the author-written list at .ufo/waves/round-23/measure/post-falsify/falsify-limit.json:13 and in a scope sentence at line 15.
- [obs] The routed row for line 52 says "Fixed in output and as criterion" (corpus/lessons/round-24.md:35). Nothing in round 24 corrects the three loci. The wave-1 scribe draft listed "presenting the literal name as recovered" as a failure the fix must reject (.ufo/waves/round-24/w1/ScribeLessonMistakes/round-24-mistakes.md:10). The committed fix text drops that control.
- Smallest correction: append a dated notice after SCORECARD.md:734 and matching notices in corpus/lessons/round-23.md and LOG.md. The notices say the name is author recollection (falsify-limit.json:13) and that the retained keys are the five listed above (events.json:14064). Change the line-52 disposition to say the label is implemented and the three round-23 loci are corrected by notice.

2. A privacy clause in the routed table is violated, and neither table records it.
- [obs] Spot-check line 64 says "no raw/private body capture is authorized by this note" (corpus/lessons/round-23-verifier-spotcheck.md:64). The round-24 wave rule for sudo journal lines is to record time, user, command name and flags (.ufo/waves/round-24/w1-spec.json:5).
- [obs] The tracked captures .ufo/waves/round-24/capture/l1/capture.txt and l1-2/capture.txt each hold seven "(command continued)" sudo lines, at lines 168-174 in both files. They list package-cache file paths, pulled in by an earlier Plymouth journal filter (CritLearningFit.md:79-80). The pinned captures l1-3 and l1-4 hold none (count 0 each).
- [obs] Wave-1 seats reported it: SentinelCapture.md:3 and CritLearningFit.md:79-80. The lesson has no row for it.
- [obs] I read those lines with archive file names masked. They hold no secret value. The breach is of the round's own reduction rule, and it stays in committed history.
- Smallest correction: add a mistake row (class privacy; evidence capture l1 and l1-2 lines 168-174; captured by SentinelCapture and CritLearningFit; fix: pinned captures l1-3 and l1-4 omit the lines, no gate cites them, and the breach is disclosed as committed history). Add a routed row for the privacy clause of line 64.

MEDIUM

3. The key-recollection row cites a selftest that does not test the label rule, and the label's site scope is untested.
- [obs] In my clone I replaced the label expression (report-red-causes.py:164, `'label': None if key in site_keys else LABEL`) with `'label': None`. The selftest then fails on `pristine` (its label check is at line 240) but still passes on `unknown-key-renamed` (lines 230-231). The row (corpus/lessons/round-24.md:47) and QUALITY 54 (corpus/QUALITY.md:107) both cite `unknown-key-renamed`. That case exits 1 for another reason (no unknown token), and its label check never runs.
- [obs] With that label rule broken, the committed real run exits 1 with preserved false. The rule is enforced on real data, but not by the case the lesson names.
- [obs] The site scope is untested. I widened the key set to every seat's event arguments (site_keys at lines 157-159). The whole selftest still passes. A crafted input (replace_all only at seat B; flagged site A:1 lacks it) gives "label present" in the committed tool and "label absent" in the widened one. The committed data cannot separate them, because replace_all occurs nowhere in events.json.
- [obs] The wave-1 scribe draft said the right thing: "the latter pristine fixture also checks the recollection label" (round-24-mistakes.md:22). The committed row changed it.
- Smallest correction: cite `pristine` for the label rule. Add a selftest where replace_all appears only at another seat's event and the expected label is present. Correct QUALITY 54 to match.

4. The C1 join claim is not shown to fail. The working guard is the digest pins, and a coordinated commit defeats them.
- [obs] With the re-classification check disabled (report-red-causes.py:126, `if fid not in ids:` made false), all eleven selftest cases still pass, including stub-shifted-sites. From reading lines 179-182, that case exits 1 only because read event A:0 has no unknown token. The committed real run reports reclassify_mismatches 0 (.ufo/waves/round-24/measure/c1-22fd1642.json), so the real output cannot show the join either.
- [obs] The pins do catch edits that leave the tool alone. On branches, adding one trailing newline to events.json exits 1 with pin_mismatches naming events.json. The same edit to tools/check-seat-bindings.py exits 1 with that checker named. The row never cites the pins.
- [obs] The pins are constants in report-red-causes.py (lines 35-40), in the same file the revision binds. One commit that edits events.json and the matching constant passes: exit 0, preserved true, 268 of 268 attributed.
- Smallest correction: cite the pins as the real guard and state their limit. Add a selftest where a finding id contradicts a bound event that has unknown tokens, expecting exit 1 and reclassify_mismatches of at least 1. Move the pinned digests outside the committed tool, or say that coordinated edits are caught only by review.

5. The per-finding subcause labels are wrong for 8 of the 15 "outside the lane root" rows.
- [obs] report-red-causes.py:88-90 labels every value that does not start with the lane prefix "outside the lane root". Per the events, four of those are dot-segment paths that normalise inside the lane (FxC1Selftest:12, FxC1Selftest:13, FxC3Build06:7, ConnFxPlanner:28). Four are relative or redacted values (FxC2OracleLegacy:17, SentFxPrivacy:13, SentFxPrivacy:14, FxSources:38). The other seven are absolute and outside. Sources: .ufo/waves/round-24/measure/c1-22fd1642.json (per_finding) and .ufo/waves/round-23/falsify/events.json.
- [obs] The seat-level label "trace ends before a final message" (report-red-causes.py:144) names a cause. The ConnFxPlanner record has no field giving a reason (terminal_evidence session_exit_line and native_failure are both null). [inf] The reason is therefore unrecorded.
- [obs] The uncommitted working-tree tool already splits these labels and says "which condition failed is not recorded". That version is neither committed nor measured.
- Smallest correction: commit the relabelled tool, measure C1 at the new revision, and cite that revision in the lesson.

6. The stale-premise fix is shown only for checker guards, not for the stale premise.
- [obs] Removing each named guard flips its selftest case from PASS to FAIL. Removing the capture hash check flips capture-hash-mismatch; removing the boilerplate check flips boilerplate-only; removing the capture-path check flips no-capture-pointer (check-pause-gate.py:93-94 and 122-126). So "fail as designed" holds for these cases.
- [obs] Those guards answer wave-1 items 8 and 10 of CritClaimSizing.md, not the stale-premise row. No executable check reads SCORECARD declaration text or supersession notices. QUALITY 55 (corpus/QUALITY.md:108) is prose. The scribe draft warned: "Do not credit that stronger fix without a discriminating restored-defect control" (round-24-mistakes.md:18). The row has no such control.
- [obs] The C2 axis moved from freshness (CritClaimSizing.md:59-62 suggested "freshness 9 → 9 (0)") to tied-lowest depth (SCORECARD.md:759). Both are zero-delta. [inf] The closure should judge the change.
- Smallest correction: state that the stale-premise class has no executable check, and describe the fix as the three guards plus the text correction. Or add a restored current-413 fixture that the review must reject.

7. The capture-count row shows no failing case, and the misleading count is still in the pinned capture.
- [obs] The fix adds cache-package-files (l1-4 lines 284-286, value 0; capture.sh:49). The old cache-file-count block remains: l1-4 lines 226-228 print 4 under that label, and capture.sh:46 still runs `ls | wc -l`.
- [obs] The row claims no shown-to-fail check, and none exists. The P5 falsifier is prose (corpus/knowledge/pause-lift-gate-r24.md:76).
- Smallest correction: note in the row and the gate that l1-4 lines 226-228 count directory entries, and cite l1-4 lines 284-286 for package files. Rename that block in the next capture.

8. Three routed-table dispositions point to places that do not exist at 22fd164.
- [obs] "Wording kept ... in SCORECARD" (the lines 17 and 21 row): the round-24 section (SCORECARD.md:739-763) has no "mode 1 means evaluable" or "capability evidence" text. The only SCORECARD hit for "evaluable" is round-22 text at line 688.
- [obs] "Carried unchanged in the round report" (the line-64 retry row): no round-24 report or measured outcome exists at 22fd164. The round-24 section ends at SCORECARD.md:763.
- [obs] "Not exercised: this round recorded no new seat traces" holds for the lane: round 24 has no events file, only attempt-1 fixtures and dispatch JSON. [unk] Whether harness storage outside the lane holds round-24 traces.
- Smallest correction: word the two forward dispositions as "to be carried in the round-24 measured outcome", and keep that wording until the outcome is committed.

9. The routed-defect table is incomplete. See the coverage table below.
- Smallest correction: add a row for each uncovered item, marking it covered, deferred to a named place, or violated with a notice. Say which items the lesson treats as standing constraints rather than defects.

10. The lane has uncommitted drift.
- [obs] git status listed 21 entries at my first check and 32 at my final check; the lane tree keeps changing, and two of the 32 are my report files. Entries include corpus/lessons/round-24.md (one row changed: "other-project" became "other-project"), tools/report-red-causes.py (new subcause labels and a new selftest case, no-incomplete-seat), tools/check-pause-gate.py, capture.sh (boot identifiers, a Plymouth sudo exclusion, package-path and filesystem-id redaction), SKILL.md, three corpus/knowledge files and wave-1 reports.
- [obs] The committed C1 tool will not measure other bytes. Run with the working-tree copy against the committed base, it exits 2 with "working-tree report tool differs from the revision blob" (clone run).
- Smallest correction: the L1 commits, then re-measures C1 and C2 at the landed revision, and the lesson cites that revision.

LOW

11. QUALITY 54 misstates the retained event. corpus/QUALITY.md:107 says the event "keeps only `__unknown_argument__`". It keeps five keys: __unknown_argument__, i, new_string, old_string and path (events.json:14064 region). Smallest correction: "keeps `__unknown_argument__` in place of the unrecognised key, beside i, path, old_string and new_string".

12. The redaction row's captured-by is incomplete, and its test cannot be rerun from the repo.
- [obs] The row credits SentinelCapture. The l1-2 evidence (sudo records at lines 240-697, all labelled outside, none inside) came from ExecSudoAttribution.md:55-64 (its item 6).
- [obs] The four-line synthetic test exists only as prose (corpus/lessons/round-24.md:46; corpus/QUALITY.md:109). I replayed it on synthetic lines (.ufo/waves/round-24/w2/RevLessonMistakes/redaction-replay.txt). The committed awk rule gives inside, outside, inside, outside, inside. The old sed pipeline gives outside on all five. The claim holds, but nothing in the repo reruns it.
- Smallest correction: commit the replay as a script that extracts the rule from capture.sh, and add ExecSudoAttribution to captured-by.

13. Evidence pointer precision.
- The stale-premise row points to a section name; both quotes sit on SCORECARD.md:749. The C1 and capture-count rows give no path and line, only seat names. The C1 row credits CritClaimSizing with "five of nine sandbox mutants", but only CritC1Construction ran mutants (CritC1Construction.md:15-25), and that file's own verdict says "five of eight".
- Smallest correction: add the pointers SCORECARD.md:749, CritC1Construction.md:15-25 and CritClaimSizing.md:17-22, and credit the mutant count to CritC1Construction alone.

14. Wording of the stub case. The C1 row says stub-shifted-sites "fails when sites are shifted". The case is written to pass when the tool exits 1 (report-red-causes.py:256-258). Smallest correction: "the tool exits 1 for shifted sites, and the case passes".

Mistake rows checked

| Row (corpus/lessons/round-24.md line) | Evidence pointer real? | Captured-by honest? | Fix shown able to fail as claimed? |
|---|---|---|---|
| R24-STALE-PREMISE (45) | Yes. SCORECARD.md:749 holds both quotes. The pointer names a section, not a line (13). | Yes. CritClaimSizing.md:59-64, CritLearningFit.md:41-45, ScoutStalePremiseWalk.md:7-8. | Partly. Named guard cases flip (6). The stale-premise class has no check (6). |
| R24-REDACTION-OVERWRITE (46) | Yes. Records at l1-2 lines 240-697; line 239 is the sed echo. | Partly. Credits SentinelCapture only (12). | Yes in outcome (12). Not rerunnable from the repo (12). |
| R24-KEY-RECOLLECTION (47) | Yes. falsify-limit.json:13; events.json:14064 (index 17). | Yes (outside spot-check). The same name is repeated as fact at three loci (1). | No. The cited case does not fail under the label breakage (3). |
| R24-C1-BY-CONSTRUCTION (48) | No path and line, only narrative (13). The "absent at f169b3ba, exit 2" claim is true (verified). | Yes (CritC1Construction, CritClaimSizing), with the mutant count loosely credited (13). | Partly. The tool reads itself (verified). Pins hold against non-coordinated edits (verified). The stub case does not exercise the join, and coordinated edits pass (4). |
| R24-CAPTURE-COUNT (49) | Yes. l1-4 line 286 holds 0. | Yes (CritPauseEvents.md:26-32, ExecRollbackPaths.md:9-16). | No demonstration claimed or shown. The misleading count remains (7). |
| Missing: raw sudo lines | Not applicable. | Not applicable. | Not recorded (2). |

Routed-defect coverage against the round-23 spot-check (19 items)

| Spot-check line | Routed item (short) | Where round-24 handles it | Status at 22fd164 |
|---|---|---|---|
| 8 | Keep unsupported evidence and the two-shape grammar; no third-shape grant, dropped seat, denominator change or exploratory conversion | Line-64 C1 row (grammar, seat) | Partly. Third-shape grant, denominator change and exploratory conversion are not dispositioned. |
| 10 | Native root accounting remains pending the malformed-round repair or executable status proof | None | Not covered. |
| 17 | Mode 1 means evaluable, not clean or natively enforced | Row for lines 17 and 21 | Covered in wording. The SCORECARD disposition is unsupported (8). |
| 17 | Do not force unknown inputs to be accepted to move the bit | None | Not covered. |
| 21 | Selftests are capability evidence, not outside reruns | Row for lines 17 and 21 | Covered in wording. The SCORECARD disposition is unsupported (8). |
| 21 | Carried measured-input identities are not reruns; 13 mutant receipts versus 27 aggregate; no universal adequacy | None | Not covered. |
| 52 | Name not recoverable; label it | Row for line 52 | Covered. The label is implemented; the cited test is wrong (3). |
| 52 | Do not claim the key never existed; do not elevate the list into trace proof; no live-trace reconstruction | Row for line 52, label only | Violated at three loci (1). |
| 55 | Strict receipts 127 of 140 well-formed, 13 faulty; both strict flags FAIL; well-formed receipts prove no absent commands | Line-64 receipt debt | Partly. The strict flags are not carried. |
| 56 | Early 45-105 second retries violated backoff; the later guard does not erase them | Line-64 retry row | Covered in wording. The disposition is unsupported (8). |
| 56 | Prelude-name shadow, delayed skill reload, source/misroot and capture limitations remain disclosed | None | Not covered. |
| 57 | Legacy-v1 expectations at bound semantics; aggregate output not claimed byte-identical; no per-seat prevention | Line-64 native enforcement row | Partly. |
| 62 | Quality: new hardening does not reverify or supersede prior claims | None | Not covered. The SCORECARD.md:734 case shows it applies (1). |
| 64 | Preserve the frozen cohort; per-cause observability without widening, erasing or dropping the incomplete seat | Line-64 C1 row | Covered in design. Subcause labels are wrong for 8 of 15 rows (5). |
| 64 | If recording keeps unknown key names, keep values redacted and commit the generator first | Line-64 row | Covered ("not exercised"; no round-24 events in the lane). |
| 64 | Preserve exact baseline, input and emitter identities | Line-64 C1 row (pins) | Partly. Pins are self-referential (4). The collector identity is not pinned. |
| 64 | Explicit native-completion versus trace-completeness states | None | Not covered. C1 output has no native-completion field; falsify-limit.json lines 4-5 hold 76 and 75. |
| 64 | No raw or private body capture authorized | None | Violated (2). |
| 64 | Keep early retry, scope and receipt debt visible; native toolset enforcement operator-owned | Line-64 row | Covered in wording. The disposition is unsupported (8). |

Summary of the table: 6 not covered; 2 violated; 4 partly covered; 4 covered with a disposition that points nowhere; 3 covered.

What held (checked against committed bytes)
- C1 at f169b3ba: exit 2, "tools/report-red-causes.py is absent at this revision". C1 at 22fd164: exit 0, checker CANNOT_EVALUATE, 268 of 268 attributed, preserved true, incomplete seat ConnFxPlanner, FxC3Build08:17 with the unknown token.
- C1 selftest 11 of 11 and C2 selftest 24 of 24 pass at 22fd164. C2 at 22fd164 verifies 5 of 5 with exit 0. C2 at f169b3ba reports GATE-MISSING with exit 1.
- The sha256 pins of l1-2 and l1-4 match their .sha256 files.
- Pointers checked: SCORECARD.md:749 (both quotes); l1-2 records at 240-697; falsify-limit.json:13; events.json:14064 (index 17); l1-4 line 286 (value 0); l1-4 line 363 (the quoted last-modified header); the job-limit quote in .ufo/waves/round-24/w1-refusal-1.txt.
- The redaction rule gives the right label on the four synthetic cases the lesson names, plus a trailing-slash case. The old rule fails all four.
- The label is correct on the committed data and on the crafted site-scoped input.

Residual risk and verification gaps
- Everything is at committed 22fd164. The 21-entry working tree may land changes that alter findings 4, 5, 10 and 11.
- I did not verify the S087-S103 registry rows or their quotes. Other seats own them.
- Whether round-24 wave traces exist outside the lane is [unk].
- The C1 and C2 measure outputs are untracked in the lane (.ufo/waves/round-24/measure/). Any measured claim needs a committed copy.
- The redaction replay used synthetic lines in the journal's format, not live journal output.
- My mutation runs are my own. I did not use the sibling mutation seats' outputs.

Scope: read=corpus/lessons/round-24.md and corpus/lessons/round-23-verifier-spotcheck.md; SCORECARD.md round-22 to round-24 sections; corpus/QUALITY.md criteria 54-56; LOG.md:1185; corpus/lessons/round-23.md:86; round-23 falsify events.json and falsify-limit.json; round-24 captures l1, l1-2, l1-3, l1-4 and capture.sh; tools/report-red-causes.py, tools/check-pause-gate.py and tools/_revision.py at 22fd164; wave-1 reports (CritC1Construction, CritClaimSizing, CritLearningFit, CritPauseEvents, ExecRollbackPaths, ExecSudoAttribution, ScoutStalePremiseWalk, SentinelCapture, the ScribeLessonMistakes draft, w1-spec.json); lane git status, diff, log, show, ls-files and rev-parse (read-only); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevLessonMistakes.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevLessonMistakes/ (mutation-results.json, selfpin-and-worktree-results.json, synthetic-sudo.log, redaction-replay.txt), and the private clone /fast/scratch/hyaku/tsuku24w2-RevLessonMistakes (branches mut-label, mut-events, mut-checker, mut-selfpin; working edits reverted); executed=in the private clone: python3 tools/report-red-causes.py --selftest, --revision 22fd164 and --revision f169b3ba; python3 tools/check-pause-gate.py --selftest, --revision 22fd164 and --revision f169b3ba; eleven mutation runs (label rule set to None, widened key set, re-classification disabled, digest-breaking branch commits, one self-pinned commit, three gate guard removals, and the lane's working-tree tool copied in); bash replay of the capture.sh sudo pipeline and of the old sed pipeline on synthetic lines; jq and python3 reads of events.json, falsify-limit.json and the measure outputs; sha256sum of the capture files; read-only grep and sed in the lane.
Installs: none
