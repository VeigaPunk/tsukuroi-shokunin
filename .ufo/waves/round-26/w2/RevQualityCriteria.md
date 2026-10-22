# RevQualityCriteria: review of QUALITY criteria 60 to 63 and the round-26 Mistakes table

Verdict: Partly holds. All four criteria cite a Mistakes row that exists in the round-26 lesson, and all four failing examples are true when re-run, but the sweep that criterion 60 names misses 11 real removals in the lane's own history, criteria 61 and 62 are enforced only in part (criterion 62 never reads a date), criterion 63 is mostly an exhortation, and Mistakes row R26-GATE-COLUMN-OFFSET has no fix.

Basis. The revision is 7dfea9244a84a0e2439f0698e54491e5d7b7c467. I read it through `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 7dfea9244a84a0e2439f0698e54491e5d7b7c467 | tar -x -C /fast/scratch/hyaku/tsuku26/w2/RevQualityCriteria/snap`, then ran `git init` with no remote. Every path below under `/fast/scratch/hyaku/tsuku26/w2/RevQualityCriteria/snap/` is a file at that revision. I wrote nothing into the lane. The criteria are at `/fast/scratch/hyaku/tsuku26/w2/RevQualityCriteria/snap/corpus/QUALITY.md:124-127`, and the Mistakes table is at `/fast/scratch/hyaku/tsuku26/w2/RevQualityCriteria/snap/corpus/lessons/round-26.md:84-90`.

## Findings, most severe first

1. High, [obs]. The criterion 60 sweep is incomplete, so its own test can pass while removals go undisclosed.
   - Criterion 60 names `git diff -U0 <base> <REV> -- <files> | grep -E '^-[^-]'` (`snap/corpus/QUALITY.md:124`). A removed line whose text starts with a hyphen appears in diff output as "--", and a removed blank line appears as "-". The pattern matches neither.
   - I ran `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log -p -U0 --format=@@COMMIT %h -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md` and removed the header lines. The output (`/fast/scratch/hyaku/tsuku26/w2/RevQualityCriteria/out/history-p.txt`) holds 104 removed content lines. The criterion's pattern matches 93 and misses 11. The misses are: commit 9bcd162 (2026-10-14, four `- [ ]` SHONEN box lines); commit 9b70381 (2026-10-17, four `- [~]` SHONEN box lines and one blank line); commit 82e5192 (2026-10-21, one `- **planned (current):**` bullet in SCORECARD.md); commit b30a3a3 (2026-10-21, one blank line in corpus/SOURCES.md).
   - On commit 9bcd162 alone, `git -C <lane> diff -U0 9bcd162^ 9bcd162 -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md | grep -E '^-[^-]'` prints 4 lines (exit 0). The same diff, read with a header-aware filter, removes 8 lines.
   - Sandbox A (`/fast/scratch/hyaku/tsuku26/w2/RevQualityCriteria/sweep-demo`) removes the bullet `- alpha rule` and one blank line from `corpus/QUALITY.md` in place. The criterion's command prints nothing and exits 1. The full diff shows `-- alpha rule` and `-`.
   - Replacement, tested: `git diff -U0 <base> <REV> -- <files> | grep -E '^-' | grep -vE '^--- (a/|/dev/null)'`. On sandbox A it prints `-- alpha rule` and `-`. On commit 9bcd162 it prints 8 lines.
   - Round 26's own range is clean. The four round-26 commits (b13e991f, 4de2b6b, ef72f10, 7dfea92) contribute no misses, and the three SHONEN lines listed at `snap/corpus/lessons/round-26.md:76-80` are the complete removed-line set for e9f5356c to 7dfea92.
   - Consequence: the Mistakes row R26-UNDISCLOSED-INPLACE claims a fix shown able to fail. It is shown able to fail only for table rows and prose lines. A future round could change SHONEN box lines, and this sweep would print nothing.
   - [inf] A two-point diff also hides a line that is removed in one commit and restored in a later one. I did not test this.

2. Medium, [obs]. Criterion 61's general rule has no enforcing check.
   - Criterion 61 (`snap/corpus/QUALITY.md:125`) covers any source row added in a round. The only Gate check in the lane is in `snap/tools/check-storage-health.py`, around lines 663-721, and it reads only the rows the C1 entry cites.
   - Sandbox C (`/fast/scratch/hyaku/tsuku26/w2/RevQualityCriteria/sb-c-uncited-row`) adds row S140 to `corpus/SOURCES.md` with status mined, opened 2026-10-22, no citing entry, and no Gate record. `python3 tools/check-storage-health.py --repo <sandbox> --revision <sha> --branch master` exits 0 with 6 of 6 rows verified.
   - A diff test catches it. The S-ids added to SOURCES.md between e9f5356c and the sandbox commit, minus the Gate ids in the lesson, leave `['S140']`.
   - For the real round, the added ids are S128 to S139, and each has a Gate row. So the rule holds for round 26 by inspection only.

3. Medium, [obs]. Criterion 62 never reads a date, and it accepts any move the same round writes into its own measured-outcome section.
   - The check at `snap/tools/check-self-assessment.py:470-513` takes the last `axis N → M` match inside a measured-outcome section, in file order. It reads no date.
   - Sandbox E (`/fast/scratch/hyaku/tsuku26/w2/RevQualityCriteria/sb-e2-undated-move`) changes the current depth row from 8 to 9 and adds the undated line "Mutant line with no measurement and no date: depth 8 → 9." to the round-26 measured-outcome section. `python3 tools/check-self-assessment.py --repo <sandbox> --revision <sha>` exits 0, with 0 mismatches and K01 reported as "match" at `SCORECARD.md:962`.
   - At 7dfea92, K01, K04 and K05 all read `snap/SCORECARD.md:960`. That line calls itself "dated", but it carries no date.
   - So the check confirms only that the table agrees with the newest self-written transition. It confirms neither a measurement nor a date.
   - What holds: an axis with no transition is a mismatch (K02 and K06 at e9f5356c, "no dated move record"), and the selftest has the cases `declaring-round-declaration-line` and `axis-without-move-record` (`snap/tools/check-self-assessment.py:959-963`).

4. Medium, [inf]. Criterion 63 is an exhortation except for two checkable parts.
   - "Marked as an assumption" has no check. A search of `snap/tools/` for assumption markers found none; the only hit is a comment in `tsukuroi-census.sh`.
   - The checkable parts hold. The refinements commit 4de2b6b (2026-10-22 11:06:01 -03) comes before the first commit that adds measure receipts, which is 7dfea92 (11:41:50 -03), per `git log --diff-filter=A -- .ufo/waves/round-26/measure`. The target strings "6 verified rows, SH1 to SH6" and "0 of the 27 fixed checks" appear once each in b13e991f, 4de2b6b, ef72f10 and 7dfea92.
   - The failing example is true but understates the case. The refinements at `snap/SCORECARD.md:914-918` correct five declared rows: SH5, SH3, SH4, SH2 and SH6.

5. Medium, [obs]. Mistakes row R26-GATE-COLUMN-OFFSET has no fix.
   - The row (`snap/corpus/lessons/round-26.md:90`) says "Not fixed after pinning" and "Fix owed next round". The defect is real. Sandbox D (`/fast/scratch/hyaku/tsuku26/w2/RevQualityCriteria/sb-d-unquoted-gate`) strips the quote marks and backticks from every Gate quote cell. The checker then exits 1 with `SH-GATE-QUOTE-MISSING` and reports 0 of 6 rows verified. The committed entry uses quotes, so the 6-of-6 measurement is unaffected.
   - By the table's own standard (each fix shown able to fail), this row is open.

6. Low, [obs]. One Gate quote is not verbatim in its snapshot (source S136).
   - Lesson row S136 (`snap/corpus/lessons/round-26.md:40`) quotes "systemd-oomd.service will monitor this unit's cgroup and evaluate the specified rulesets against it." and gives the location as lines 1643-1644, "tag-free text".
   - In `snap/.ufo/waves/round-26/sources/S136.xml`, lines 1643-1644 read `<citerefentry><refentrytitle>systemd-oomd.service</refentrytitle><manvolnum>8</manvolnum></citerefentry>` followed by a new line and "will monitor this unit's cgroup and evaluate the specified rulesets against it." With tags removed, the text reads "systemd-oomd.service8 will monitor". The quote is a substring in neither form.
   - S137 is a substring after tag removal, which matches its "tag-free text" label. Nothing checks S136's quote, because the C1 checker reads only SH-cited rows.

7. Low, [obs]. The red-before for Mistakes row R26-PREMISE-BEFORE-SOURCE is a text comparison, not a check.
   - The declared wording is at `snap/SCORECARD.md:895`: "which fields (critical warning, available spare against its threshold, percentage used, media and data integrity errors) decide it".
   - `snap/.ufo/waves/round-26/sources/S134.cpp:450-451` prints PASSED from `(!w ? "PASSED" : "FAILED!")`, where `w` is the critical-warning byte. Line 840 passes only `smart_log.critical_warning`, and no other PASSED print exists in S134. So percentage used and the media and data integrity errors do not decide PASSED. Available spare reaches the result only through critical-warning bit 0x01, as the refinement at `snap/SCORECARD.md:914` says.
   - The contradiction holds, but no command can fail on a later declaration. The fix is a refinement sentence.
   - The entry itself was corrected: `snap/corpus/knowledge/storage-health-r26.md:99` lists percentage used and media errors as separate signals.

8. Info, [obs]. The lane moved after 7dfea92.
   - Three commits on master after 7dfea92 (7f9f088, 75449b1, dd923c0) add 6 lines to QUALITY.md (QUALITY 64 to 66), 47 lines to the round-26 lesson, 21 to SCORECARD.md, 3 to SOURCES.md and 2 to LOG.md. None removes a line from QUALITY.md or the lesson, so criteria 60 to 63 and the five Mistakes rows are unchanged on master.
   - I did not review the appended text. [unk] whether it fixes findings 1 to 7.

## Criteria 60 to 63 against the four checks

| Criterion | Cited Mistakes row (lesson line) | Failing example, re-run | Testable? |
|---|---|---|---|
| 60 | R26-UNDISCLOSED-INPLACE (:86) | True. The sweep on b9046016..e9f5356c prints 2 lines (SCORECARD.md:51 and the SHONEN box 2 line). `snap/corpus/lessons/round-25.md:82-84` records one. | Partly. The named command misses 11 of 104 removed lines (finding 1). |
| 61 | R26-GATE-RECORD-MISSING (:87) | True. `grep -c S127 corpus/lessons/round-25.md` prints 0. S126 has no Gate row; it appears once, in an errata bullet at round-25.md:72. | Partly. Enforced for C1-cited rows only (finding 2). |
| 62 | R26-SELF-REFERENT-ORDINAL (:88) | True. The v1 checker at 157ee255 reports K01, K04 and K05 at SCORECARD.md:793, 807 and 792, all round-25 declaration lines. `snap/corpus/lessons/round-25-verifier-spotcheck.md:62` says the same. | Partly. Consistency is checked; dates and evidence are not (finding 3). |
| 63 | R26-PREMISE-BEFORE-SOURCE (:89) | True. SCORECARD.md:895 lists percentage used and the media and data integrity errors as deciding fields; S134.cpp:450-451 shows they do not decide PASSED (finding 7). | Mostly an exhortation (finding 4). |

Every criterion cites `corpus/lessons/round-26.md`, and each cited ID exists in the Mistakes table. Every Gate row and every Mistakes row has five columns. Every Gate quote is at most 24 words.

## Mistakes rows: red-before commands reproduced

| Row | Stated red-before | Reproduced | Is the fix able to fail? |
|---|---|---|---|
| R26-UNDISCLOSED-INPLACE | The sweep at b9046016..e9f5356c prints 2 lines for 1 disclosed edit. | Yes. It printed 2 lines, exit 0. | Only partly (finding 1). |
| R26-GATE-RECORD-MISSING | `grep -c S127 corpus/lessons/round-25.md` returns 0. | Yes. It printed 0. | For cited rows, yes: sandbox B (`/fast/scratch/hyaku/tsuku26/w2/RevQualityCriteria/sb-b-gate-s134-removed`, S134 Gate lines removed) exits 1 with `SH-GATE-QUOTE-MISSING`, 4 of 6 verified. For uncited rows, no: sandbox C exits 0. |
| R26-SELF-REFERENT-ORDINAL | The v1 checker at e9f5356c reports K01 at SCORECARD.md:793; v2 reports :730. | Yes. v1 K01 observed_line is 793. v2 K01 observed_line is 730, inside a Round 23 measured-outcome section (e9 headings at lines 724 to 739). | Yes for this case. Dates are not checked (finding 3). |
| R26-PREMISE-BEFORE-SOURCE | The declared SH5 wording is false against S134 line 451. | Yes, by reading S134.cpp:450-451 against SCORECARD.md:895. | Not a check (finding 7). |
| R26-GATE-COLUMN-OFFSET | None; no fix. | Defect reproduced: sandbox D gives 0 of 6 with unquoted quotes. | No fix (finding 5). |

## Residual risk and verification gaps

- Finding 8 is not reviewed beyond the diff stat.
- The v2 checker's 13 selftest cases were run as one unit (exit 0, selftest PASS). I did not inspect each fixture.
- S126 was checked against a fetch of https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml. Its sha256 is 36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617, which equals the anchor, and both Gate quotes are present.
- S127 was checked against `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 4f05dd5a:corpus/knowledge/system-pressure-r24.md`. Its sha256 is 5d3a322aadb00c6ba3700b6c5b31d4e5b5305b404731f0eb37a5a3474c019ce5, and the Gate quote is present.
- [unk] Whether the historical box-line removals in commits 9bcd162 and 9b70381 were disclosed at the time. They predate round 26; the point here is the sweep's blind spot.
- The v2 checker runs the census selftest on a git archive of the revision. That script runs fixture binaries, and a grep of it for `sudo` returned no hit.

## Direction for the lane (not implemented here)

- Criterion 60: use the header-aware pattern above, and add a fixture to the selftest that removes a bullet line and a blank line.
- Criterion 61: add a check that every `| S###` row added to SOURCES.md in a round has a Gate row in that round's lesson.
- Criterion 62: require a date in every measured-outcome transition line, and add a selftest case for an undated move (sandbox E).
- Criterion 63: list each declared mechanism statement with its assumption marker or source row, and check the markers mechanically.

Scope: read=the 7dfea92 snapshot files QUALITY.md, round-25 and round-26 lessons, round-25 spot-check, SCORECARD round-26 sections and measured outcome, check-self-assessment.py, check-storage-health.py, _revision.py, tsukuroi-census.sh (grep only), S134.cpp, S136.xml, S137.xml, storage-health-r26.md; the lane's git history of the five disclosure-scoped files and commit metadata; the public URL for S126; read-only git objects of mori-shokunin commit 4f05dd5a; RULES.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevQualityCriteria.md and scratch under /fast/scratch/hyaku/tsuku26/w2/RevQualityCriteria/ (snap, v1, e9, r25, out, sweep-demo, sb-baseline, sb-b-gate-s134-removed, sb-c-uncited-row, sb-d-unquoted-gate, sb-e2-undated-move); executed=git cat-file, git archive piped to tar, git init and git commit in scratch sandboxes only, git log -p -U0, git diff -U0 and --stat, git show, git for-each-ref, git rev-parse, git log --diff-filter=A; grep -c and grep -E pipelines; python3 tools/check-self-assessment.py for v1 and v2 at e9f5356c, 157ee255 and 7dfea92, the v2 selftest, and sandbox E; python3 tools/check-storage-health.py for the selftest, the lane at 7dfea92 with --branch master, and sandboxes baseline, B, C and D; a Python urllib GET of the S126 public URL; a read-only git show of mori-shokunin commit 4f05dd5a.
Model: anthropic/claude-haiku-5-5 (as stated in the session workstation context; not independently confirmed)
Installs: none
