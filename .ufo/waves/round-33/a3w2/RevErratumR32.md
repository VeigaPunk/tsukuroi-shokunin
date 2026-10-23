VERIFIED — every time and seat name in the erratum is right, and `git diff 1f521b93 5a967ce2 -- .ufo/waves/round-32/controls/README.md` is append-only (4 insertions, 0 deletions), so the original "Update — final counters" paragraph is unedited.

1. [obs] Append-only confirmed. `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff 1f521b93 5a967ce2 -- .ufo/waves/round-32/controls/README.md` reports "1 file changed, 4 insertions(+), 0 deletions(-)". The only change is the appended `## Erratum` block (new lines 30–33 of /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/controls/README.md). Line 27 ("The table above was written under C1 v2 and probe v1; … all committed before the first data seat: …") is untouched, so the erratum's "line 27" pointer and its claim "The paragraph above stays as written" are both correct.

2. [obs] C1 controls commit time correct. `git log -1 --format=%cI 462e40a7` → `2026-10-22T22:59:46-03:00`, exactly as the erratum states; subject "round-32: final C1 control receipts under scorer v3 (K0-K4, K6-K10; only positive K8 exits 0), before any data seat" confirms it is the C1 controls commit.

3. [obs] C2 controls commit time correct. `git log -1 --format=%cI 4e685163` → `2026-10-22T23:05:54-03:00`, matching the erratum's "23:05:54-03:00"; subject "round-32: final C2 control receipts under probe v2 (H0-H6; only H5 empty-env exits 0)" confirms it is the C2 controls commit.

4. [obs] Seat names and dispatch times correct. corpus/lessons/round-32-verifier-spotcheck.md:29 (the §9 ruling paragraph, inside section 1 "Step-1 conformance") states ExecHandoffCensus was dispatched at 01:59:51.5Z (22:59:51-03:00) and ExecAllowA and ExecAllowB at 02:06:02.9Z (23:06:02-03:00); line 32 names the same three as the data executors. The erratum's "ExecHandoffCensus (dispatched 22:59:51-03:00)" and "ExecAllowA and ExecAllowB (23:06:02-03:00)" match verbatim, and the erratum's citation "section 1, 'Conformance defects' and the §9 ruling" is accurate — both subsections are in section 1 (lines 29 and 31).

5. [obs] Ordering claims hold. 22:59:46 (462e40a7) precedes 22:59:51 (ExecHandoffCensus dispatch) — margin ~5.5 s; 23:05:54 (4e685163) precedes 23:06:02 (ExecAllowA/B dispatch) — margin ~9 s; and 23:05:54 follows the C1 data seat's 22:59:51 start. So "all committed before the first data seat" indeed holds per claim only, exactly as the erratum says.

6. [obs] Defect reference correct. The erratum header names "round-32 spot-check routed defect 4"; corpus/lessons/round-32-verifier-spotcheck.md:141 item 4 under "## 5. Routed defects" is the sequence-statements defect requiring exactly this appended-erratum correction ("the C2 final receipts (`4e685163`, 23:05:54) follow the C1 data seat's start (22:59:51); the order holds per claim only"). The erratum implements the prescribed fix.

7. [obs] Append date correct. `git log -1 --format=%cI 5a967ce2` → `2026-10-23T03:57:30-03:00`, subject "round-33: attempt 3 start (… round-32 controls erratum re-derived …)", matching the erratum header "appended round 33, attempt 3, 2026-10-23".

8. [inf] Minor wording only: the lesson calls the three actors "executors"; the erratum calls ExecHandoffCensus "the C1 data seat". The names are identical and the README's own convention is "seat", so this is not a defect.

No residual defects found; no unknowns.

Scope: read=skill godspeed, .ufo/waves/round-32/controls/README.md (full, 33 lines), corpus/lessons/round-32-verifier-spotcheck.md (headers map + lines 136-148, §1 lines 29/32), git log %cI for 462e40a7/4e685163/5a967ce2, git diff 1f521b93..5a967ce2 for the README; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/RevErratumR32.md; executed=git log -1 --format=%cI on the three commits, git diff (read-only), git grep on the lesson file
Model: devin/swe-2
Installs: none
