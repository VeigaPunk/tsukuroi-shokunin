Verdict: I attacked the round-24 trend picture landed at 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0 (expansion, quality and discernment, judged against /home/vgpnk/Projects/shokunin/LEARNING.md:31-38 and corpus QUALITY 49). Any author-side reading of "expansion improved" or "quality improved" at this commit is **falsified**. A bounded "discernment improved" reading **survives with defects** and stays provisional until the outside spot-check.

Proposed verdicts (author-side proposal from a lane-dispatched seat; outside closure decides):

| Trend | Proposed verdict at 22fd1642 | After the smallest corrections below |
|---|---|---|
| expansion | unchanged | unchanged |
| quality | harmed: a premise this round found stale is left unmarked at its own loci | improved, bounded to four named superseded or reverified loci |
| discernment | improved, bounded to QUALITY 54; provisional, author-side only | same; the outside spot-check needs a sampleable reject |

`unprovable-but-better` does not apply to any of the three. The round declares "No exploratory claim" (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:753). That verdict is reserved for exploratory claims judged by a named non-author reviewer (/home/vgpnk/Projects/shokunin/LEARNING.md:46-48).

No author trend verdict is on record yet. A grep of the lane for `(expansion|quality|discernment) … (improved|unchanged|harmed|unprovable)` outside rounds 20-23 returns no match, and SCORECARD has no round-24 measured-outcome section after :755-763. The findings below are therefore a pre-emptive attack on the readings the landed bytes invite.

## Expansion

1. [obs] The C2 ground is Core and is already held. Update-safety is a PROVINCE Core surface, the coverage-map row `corpus/README.md:10` holds the update-safety plane, and PROVINCE.md has no diff between f169b3ba and 22fd1642 (`git diff --stat f169b3ba 22fd1642 -- PROVINCE.md` prints nothing). This agrees with wave 1: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/CritLearningFit.md:38-39 (findings 7-8), and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ScoutCorpusNovelty.md:42-46 (P3 is "freshness continuation", "a new coverage-map row for it would inflate coverage"). C1 works the round-21 to round-23 seat-audit surface. No entry lands on uncovered coverage-map ground.
2. [obs] The 17 new rows S087-S103 are not expansion. CORPUS rule 4 says "Expansion is knowledge, not rows" (/home/vgpnk/Projects/shokunin/CORPUS.md:123-125). They also bring no new kind of source. Kind counts parsed from `git show f169b3ba:corpus/SOURCES.md` and from `22fd1642` are: before code 9, community 5, dataset 1 (S029), docs 46, own-work 23, tool 2; after code 16, community 5, dataset 2, docs 55, own-work 23, tool 2.
3. [obs] No frontier area is entered and no capability is admitted. The README Frontier list (`corpus/README.md:28-43`) gains no bullet. The round-24 notice only narrows an old one (`corpus/README.md:223`), and SCORECARD.md:753 rules out a capability acquisition.
4. [inf] Inflation risk: `corpus/README.md:221-227` adds a `| Note | Holds | Sources |` table, the same shape as the coverage map at :5, under a heading that begins "Frontier notice". Unlike round 18 (`corpus/README.md:160`: "Held surfaces, not new coverage"), it carries no sentence saying it adds no coverage. A row counter or a hurried judge could score it as a coverage row or as a frontier entry.
   Smallest correction: append one sentence to that notice: "Held update-safety surface; not new coverage, frontier entry or capability."
5. [inf] Not harmed. The admitted gate entry has locator defects (finding 9 below, and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/CritSupersedes.md findings 3, 4 and 6), but none of them changes a P1-P5 verdict (CritSupersedes.md:64). No admitted entry is shown failing the bar it was admitted under.

**Expansion: unchanged.**

## Quality (QUALITY 49: a named prior entry, superseded or reverified, with actual evidence)

6. [obs] These count under QUALITY 49, because each names a prior weaker or open entry and replaces it with dated capture evidence:
   - Q+1: `corpus/knowledge/package-state-plane.md:39-40`, "[unknown] Whether `stable-mirror` lags upstream Arch". The R24 notice at `:444-446` answers it from S100 ("changes only when a release ships") and S101 (core.db `last-modified` 2026-10-22 04:40:03 GMT). The answer is qualitative only; the size of the lag is unmeasured (CritSupersedes.md finding 11).
   - Q+2: the R18 state "The current pending count is UNKNOWN" (`corpus/knowledge/host-health-report-r3.md:628`) gives way to measured values. `pacman -Qu` shows 3 rows (`.ufo/waves/round-24/capture/l1-4/capture.txt:40-47`), and the temporary-database check shows 134 (`:374`). `l1-4/checkupdates.out` has 134 lines (`wc -l`, 134). The capture sha256 is `87f70f82…a56f` (`sha256sum`). The notice landed in `partial-upgrade-recheck-r15.md:202-204`, not at the UNKNOWN locus.
   - Q+3: `corpus/README.md:10`, "sync dbs born 2026-10-11, `-Sy` never run since", is now marked historical at `:223`. The stated reason is off target; the `pacman -Sy` at `capture.txt:221` is what falsifies the line (CritSupersedes.md finding 10).
   - Q+4: P2 re-verifies the open residue question at `partial-upgrade-recheck-r15.md:40-42` and `:182`. It finds zero installed-newer rows and libinput 1.32.0-1 equal to its sync version (`capture.txt:57-59`, `:73`, `:88`).
7. [obs] These do **not** count:
   - The "413 pending" and "Pending mkinitcpio 42 upgrade" supersessions. Round 17 had already superseded both, at `partial-upgrade-recheck-r15.md:176` (R17-FRESH-PARTIAL-02, "413 is not a current-use value") and at `corpus/README.md:149-151`, with round 18 repeating it at :164. Re-superseding them is not a QUALITY 49 gain. The round's own lesson admits this as R24-STALE-PREMISE (`corpus/lessons/round-24.md:45`). Wave 1 found it too: CritLearningFit.md finding 9; CritSupersedes.md findings 8 and 12.
   - `premises_verified` 5, the 17 rows, the new checker and its selftests. QUALITY 49 says "new instrument existence, fixture growth or in-round hardening is not by itself `quality: improved`" (`corpus/QUALITY.md:97`). The checker also never reads the `## Supersedes` list (CritSupersedes.md finding 13: a mutant with fake loci still gives exit 0 and 5 verified). So the C2 count is not evidence for any supersession.
8. [obs] **Strongest counterexample: the 1password-beta downgrade trap is found stale by this round and left unmarked where it lives.**
   - The gate entry declares the trap superseded (`corpus/knowledge/pause-lift-gate-r24.md:82`). The capture shows the installed beta is now behind its channel: `1password-beta 8.12.42_34.BETA-1 -> 8.12.44_25.BETA-1` (`capture.txt:40`, repository `omarchy` at `:52`).
   - At 22fd1642 the trap still reads as current, with no forward notice, at these loci (`git grep -n -E "would downgrade|downgrades" 22fd1642 -- corpus/knowledge SKILL.md`):
     - `SKILL.md:386`, an operator-facing "`DO-NOT`" row;
     - `corpus/knowledge/update-safety-note.md:32`, `:282`, `:374` and `:397`;
     - `corpus/knowledge/degraded-triage-r4.md:77` and `:394`;
     - `corpus/knowledge/host-health-report-r3.md:335`.
   - `update-safety-note.md` has no diff. The SKILL.md diff adds only `:2237-2285`, which never mentions 1password-beta.
   - The gate's own locator `SKILL.md:382` is wrong; that line reads "stamp means kernel / libc / driver classes are in scope" (`git show 22fd1642:SKILL.md | sed -n 382p`).
   - Rules that apply:
     - LEARNING.md:34: quality is `harmed` when "an entry is found false or stale and left unmarked". `improved` requires "no admitted entry failing its re-check", and this entry failed its re-check this round.
     - QUALITY 10 (`corpus/QUALITY.md:14`): "Before a correction commit, sweep every mention in README.md, SKILL.md and corpus/knowledge/".
     - QUALITY 55, written this round: "A stale premise is re-measured or marked historical, never reused as current."
   - Strongest counter-reading: the Supersedes list in the new entry is itself the marking. It fails for three reasons. The list sits in a different file. The checker does not verify it. It misses the operator-facing row. The round itself appended in-place notices for three other loci (README, package-state-plane, partial-upgrade-recheck-r15), so by its own convention "marked" means a notice at the stale file.
   - Impacted axes: depth (the C2 axis), quality trend, operator safety guidance.
9. [obs] Further stale loci were found during this round and are still unmarked at 22fd1642:
   - `SKILL.md:99`: "`pacman -Qu` → empty here, **rc=1**". The capture shows exit 0 with 3 rows.
   - `SKILL.md:1658`: "`mkinitcpio` ≥42 is the candidate". 42.2-1 has been installed since 2026-10-20.
   - `SKILL.md:1805-1814`: the 2026-10-20 07:44 current-use pointer `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.
   - `SKILL.md:50` and `corpus/README.md:7`: the 2026-10-11 database birth stamp.

   The wave-1 seat ScoutStalePremiseWalk listed these for the L1 (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ScoutStalePremiseWalk.md:132-142), and the lesson cites that seat (`corpus/lessons/round-24.md:45`). A grep of 22fd1642 SKILL.md for any later reference to `:99`, `:1658`, `1805` or "is the candidate" returns only the original lines. [inf] These went stale before round 24, so they are inherited debt rather than damage done this round. They still meet "found … and left unmarked".
10. [obs] One new overstatement enters the corpus. `corpus/README.md:223` says boot 0 "shows plymouth reaching the real root", but the gate entry tags the same proposition `[inf]` (`pause-lift-gate-r24.md:38`). The notice also drops the upstream symlink watch item that round 17 kept at `:152-153` (CritSupersedes.md findings 7 and 9).

**Quality as landed: harmed** (finding 8, supported by findings 9 and 10). The genuine gains in finding 6 cannot be netted against it, because LEARNING's `improved` condition is conjunctive. [inf] Because expansion is unchanged, this is not the expansion-for-quality trade LEARNING.md:37-38 describes. It is a single-trend defect that append-only edits can repair.

Smallest correction (append-only; no old bytes rewritten):
- Append one dated R24 notice each to `SKILL.md`, `corpus/knowledge/update-safety-note.md`, `corpus/knowledge/degraded-triage-r4.md` and `corpus/knowledge/host-health-report-r3.md`. The notices name the loci in findings 8 and 9 and cite `l1-4/capture.txt:40-47`, `:374` and gate P1/P3. The host-health-report-r3 notice also supersedes `:628` UNKNOWN.
- Append an erratum to the gate entry: `SKILL.md:382` becomes `:386-388`, `update-safety-note.md:281-282` becomes `:280-284`, and the UNKNOWN locus becomes `host-health-report-r3.md:628`.
- Append one README sentence that restores the watch item and the `[inf]` tag.

After these edits, propose **quality improved, bounded to Q+1 to Q+4**.

## Discernment

11. [obs] One route to `improved` is met on its face. The round-23 outside spot-check disagreed at line 52: `replace_all` was presented as data but cannot be recovered from the retained events (`corpus/lessons/round-23-verifier-spotcheck.md:52`). That disagreement became lesson R24-KEY-RECOLLECTION (`corpus/lessons/round-24.md:47`) and criterion QUALITY 54 (`corpus/QUALITY.md:107`). The criterion has an executable able-to-fail case: the selftest `unknown-key-renamed`. The wave-2 seat MutC1Label killed a label-removal mutant through both `--selftest` and `--revision` (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/MutC1Label.md:3). The tool compares against the flagged site's keys, not every seat's (`tools/report-red-causes.py:157-164`), so the wave-1 weakness (CritLearningFit.md finding 5) is fixed. LEARNING.md:35 counts this as "a disagreement becomes a lesson that adds a grounded `QUALITY.md` criterion".
12. [obs] The verdict cannot be self-granted. LEARNING.md:42-46 says "Self-assessed taste is not discernment … A subagent the lane dispatched is still the lane". This report, and every wave seat, is the lane. **Discernment stays a provisional author-side proposal.**
13. [obs] The round's own gate gives the outside spot-check no reject to sample.
    - The round-24 `## Gate` (`corpus/lessons/round-24.md:5-29`) lists 17 admits, no rejected candidate and no spot-check result, although CORPUS requires "candidates, admitted, rejected with reasons, spot-check result" (/home/vgpnk/Projects/shokunin/CORPUS.md:19-20).
    - The SOURCES `rejected` count is 9 at both revisions (row parse of `git show <rev>:corpus/SOURCES.md`).
    - SOURCES has no round-24 search-log note. Rounds 20-23 each have one (`corpus/SOURCES.md:164-170`), and CORPUS rule 5 requires one (/home/vgpnk/Projects/shokunin/CORPUS.md:126-128). A grep for "round 24" in SOURCES matches only row S098.
    - Because of these gaps, LEARNING's first route ("the spot-check agrees with the gate on admits *and* rejects") cannot be sampled from round-24 decisions.

    Smallest correction: append a round-24 search-log note to SOURCES (identified, screened, included and excluded counts, exclusion reasons, stop rationale), and add `rejected`/`excluded` and `spot-check: pending` lines to the lesson Gate, even when a count is 0.
14. [obs] QUALITY 55 and 56 must not be counted toward route two. Both come from in-lane wave-1 critics (`corpus/lessons/round-24.md:45-46`, "caught by the wave-1 critics", "SentinelCapture (wave 1)"), not from an outside disagreement. They have lessons behind them, so they are not discernment harm either.
    - [inf] The round already breaks QUALITY 55 in its own corpus (findings 8 and 9). A criterion that is written and not applied in the same round is weak evidence of learned taste.
    - [inf] QUALITY 56's "shown able to fail" is a synthetic test recorded only as lesson prose (`round-24.md:46`). `git grep -l -E "shokunin-other|other-project" 22fd1642` finds only the lesson and `w1/ExecPacmanLogCensus.md`, so no script or output is committed. By QUALITY 54's own rule, those printed results are not recoverable from retained bytes.
    - The committed l1-4 capture does emit both labels (2 `inside-fleet-repo`, 40 `outside-fleet-repo`, by `grep -c`), so the rule's behaviour is observable at one commit.

    Smallest correction: commit the four-line synthetic test and its output beside `capture.sh`, or label the lesson's results "author recollection".
15. [obs] C1 cannot add discernment credit beyond the label rule.
    - The declared unit is a conjunction, and it holds for 267 of 268 findings (`SCORECARD.md:763`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/CritC1Honesty.md findings 1-2). The measured file `.ufo/waves/round-24/measure/c1-22fd1642.json` gives `attributed_findings` 268, `attributed_with_recorded_operation` 267 and `attributed_seat_level` 1.
    - The assignment's own claim text leads with "268 of 268". Reporting C1 as met would be author-side inflation of the calibration axis that feeds discernment (LEARNING.md:85-86).
    - [inf] One routed round-23 line-64 item has no disposition row in `corpus/lessons/round-24.md:31-39`: "exact baseline/input/emitter identities and explicit native-completion-versus-trace-completeness states" (`round-23-verifier-spotcheck.md:64`; CritC1Honesty.md:79-82). An outside judge could read it as a routed item left unlearned and lower discernment to `unchanged`.

    Smallest correction: record C1 as "not met as declared; 267 of 268 by the declared conjunction, plus 1 seat-level; target not narrowed", and add a lesson disposition row for the emitter and native-completion item (delivered, or not delivered with a reason).

**Discernment: improved, bounded to QUALITY 54; provisional, author-side; outside spot-check decides.**

## Impacted axes

Depth (C2 axis): findings 6-10. Calibration (C1 axis, discernment): findings 11-15. Coverage and adjacency (expansion): findings 1-5. No ordinal changes are proposed.

Scope: read=SCORECARD.md:600-763; corpus/QUALITY.md (criteria 8, 10, 46-56); corpus/README.md (map, Frontier, round sections, :221-227); corpus/SOURCES.md at f169b3ba and 22fd1642 (row parse, search-log notes); corpus/lessons/round-24.md; corpus/lessons/round-23-verifier-spotcheck.md; corpus/knowledge/pause-lift-gate-r24.md and .json keys; targeted ranges of package-state-plane.md, update-safety-note.md, host-health-report-r3.md, partial-upgrade-recheck-r15.md and SKILL.md at f169b3ba and 22fd1642; tools/report-red-causes.py (grep); capture/l1-4/capture.txt:36-56 and checkupdates.out; capture.sh (grep); .ufo/waves/round-24/measure/*.json; w1 CritLearningFit, ScoutCorpusNovelty, ScoutStalePremiseWalk, ExecMirrorTimestamps, CritMirrorReading, CritClaimSizing (heads); w2 CritSupersedes (full), CritC1Honesty (partial) and heads of the other delivered w2 reports; /home/vgpnk/Projects/shokunin/LEARNING.md; /home/vgpnk/Projects/shokunin/CORPUS.md:1-137 (partial); PROTOCOL.md (grep); /home/vgpnk/.agents/skills/godspeed/SKILL.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/CritTrendVerdicts.md. I also wrote three transient scratch copies of committed blobs (/tmp/ctv-src0.md, /tmp/ctv-src.md, /tmp/ctv-skill.md) outside the allowed directory and deleted them before this report; this was a contract deviation, and no lane file was affected. executed=read-only git (log, diff, diff --stat, show, grep, ls-files, status, rev-parse), sha256sum, wc, grep, sed, awk, cut, ls, a python3 json parse of committed JSON, rm of the three /tmp scratch files; no lane tool, checker or selftest was run.
Installs: none
