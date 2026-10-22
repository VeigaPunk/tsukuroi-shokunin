# RevQualityLabels — routed defect 6 check (round 25, wave 1, 2026-10-22)

Verdict: the routed defect 6 mismatch is confirmed exactly as described; the lesson Mistake IDs (`R24-KEY-RECOLLECTION`, `R24-STALE-PREMISE`) should win, and the fix is a docs-only appended correction in `corpus/QUALITY.md` (optional mirrored note in the lesson); no code, tool, SKILL or registry text depends on either spelling.

## Findings

1. [obs] Mismatch confirmed for criterion 54. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:107` heading reads "…they summarize (R24-SUMMARY-RECALL):" while the same line's trailer reads "Lesson: `corpus/lessons/round-24.md` Mistakes R24-KEY-RECOLLECTION; outside `corpus/lessons/round-23-verifier-spotcheck.md:52`." The lesson defines the row as `R24-KEY-RECOLLECTION` at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-24.md:47`. One line of QUALITY 54 therefore carries both spellings and contradicts itself; the heading parenthetical is the drift.

2. [obs] Mismatch confirmed for criterion 55. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:108` heading reads "…mirror advance (R24-PREMISE-STALE):" while the same line's trailer reads "Lesson: `corpus/lessons/round-24.md` Mistakes R24-STALE-PREMISE." The lesson defines the row as `R24-STALE-PREMISE` at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-24.md:45`. Same self-contradiction pattern as finding 1.

3. [obs] The drift was born in a single landing; history gives no winner. Read-only pickaxe (`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log -S'<label>' -- .`, exit 0) shows all four labels first appear in the same commit `22fd1642` ("round-24: land C1 hardened per-cause report, C2 pause-lift gate entry with 17 sources, criteria 54-56, SKILL table and registry, wave-1 evidence", 2026-10-22), later touched by `44e95428` and `b9046016`. The parallel wave-1 scribes coined different IDs for the same two mistakes: the criteria seat used its labels at `.ufo/waves/round-24/w1/ScribeQualityCriteria.md:6-7` and `.ufo/waves/round-24/w1/ScribeQualityCriteria/quality-append.md:6,8`, the lesson seat used the lesson IDs at `.ufo/waves/round-24/w1/ScribeLessonMistakes/round-24-mistakes.md:10` (and the STALE-PREMISE row that became round-24.md:45).

4. [obs] Census: exactly 13 files under the lane use any of the four labels; no other file uses either spelling. Method: the lane's grep tool over `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` with gitignore off (so ignored and hidden files were included); `.git` returned no paths and is excluded per the assignment. Four per-label runs plus one combined run produced mutually consistent file sets, and a combined run with an explicit upper/lower-case alternation (`R24-(SUMMARY-RECALL|KEY-RECOLLECTION|PREMISE-STALE|STALE-PREMISE)|r24-(summary-recall|key-recollection|premise-stale|stale-premise)`) matched the identical file and line set, so no mixed-case variants exist. The 13 files:
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md` (:107 both spellings of pair 1; :108 both spellings of pair 2)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-24.md` (:45, :47)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-24-verifier-spotcheck.md` (:94 KEY-RECOLLECTION; :103 all four, the defect 6 text itself)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md` (:759 R24-STALE-PREMISE)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ScribeQualityCriteria.md` (:6, :7 — drift origin)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ScribeQualityCriteria/quality-append.md` (:6, :8 — drift origin)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ScribeLessonMistakes/round-24-mistakes.md` (:10)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/CritTrendVerdicts.md` (:34, :71 — lesson IDs)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevLessonMistakes.md` (:87, :89 — lesson IDs)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevQuality54.md` (:1 quotes the QUALITY 54 heading label; :9 lesson ID)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1-dispatch-result.txt` (:1, one line embedding this round's dispatch payloads)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1-dispatch.json` (:395, :400, :415)
   - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1-spec.json` (:135, :140, :155)
   The three round-25 files only describe the defect in dispatch payloads; they are not endorsements of either spelling.

5. [obs] No machine consumer of either spelling exists. A scoped grep over `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/LOG.md`, `SKILL.md`, `PROVINCE.md`, `SHONEN.md` and the whole `tools/` directory returned no matches for any of the four labels (the lane-wide census in finding 4 independently shows the same). So aligning is a documentation-only change with zero code or selftest risk; either direction would be mechanically safe, and the choice is by convention and citation, not by breakage.

6. [inf] The lesson Mistake IDs should win. Grounds: (a) QUALITY 54/55's own `Lesson:` trailers already cite the lesson IDs on the very lines that carry the drifted headings (finding 1, 2), so mapping the headings to the cited IDs resolves the contradiction with no change of meaning; (b) the QUALITY convention is that the parenthetical is the lesson Mistake ID — criterion 56 does exactly this (`corpus/QUALITY.md:109` heading `(R24-REDACTION-OVERWRITE)` matching lesson row `R24-REDACTION-OVERWRITE` at `corpus/lessons/round-24.md:46`), as do criteria 21-53 (for example criterion 39 `R20-C2-REFUSAL-ECHO` with its matching `Lesson:` trailer at `corpus/QUALITY.md:39`); (c) downstream references outside the drift-origin drafts use the lesson IDs: SCORECARD.md:759, the outside spot-check's own discernment paragraph (round-24-verifier-spotcheck.md:94), and the wave-2 critics (CritTrendVerdicts.md:34,71; RevLessonMistakes.md:87,89); (d) `R24-STALE-PREMISE` follows the fleet mistake-class vocabulary name `stale-premise` (quoted in `.ufo/waves/round-25/w1-dispatch-result.txt:1` as sourced from `/home/vgpnk/Projects/shokunin/CORPUS.md`), which `R24-PREMISE-STALE` inverts; (e) outside the three round-25 dispatch artifacts, the QUALITY-side spellings occur only in the criteria drafts themselves plus RevQuality54.md:1 quoting the heading, while the lesson IDs have more non-descriptive uses. The routed defect text itself (round-24-verifier-spotcheck.md:103) already frames the lesson IDs as "the lesson's Mistake IDs", that is, the canonical side.

7. [obs] Correction must be appended, not rewritten. Both drifted headings are landed historical bytes; the lane's own practice is appended named corrections that leave old bytes intact (for example "R24 clarification to 54" appended at `corpus/QUALITY.md:111` and "Corrections to the Mistakes table" appended at `corpus/lessons/round-24.md:86`). `corpus/QUALITY.md` is 113 lines and ends with the "R24 clarification to 56" paragraph at line 113, so the correction appends at end of file.

## Exact appended correction lines

Primary fix — append to the end of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md` (after line 113), preceded by one blank line:

```markdown
R25 correction to 54 and 55 (routed defect 6 of `corpus/lessons/round-24-verifier-spotcheck.md`, appended 2026-10-22): the parenthetical labels in the 54 and 55 headings are authoring drift, not separate identifiers; the binding mistake IDs are the ones each criterion's own `Lesson:` trailer already cites. Criterion 54 is `R24-KEY-RECOLLECTION`, not `R24-SUMMARY-RECALL`; criterion 55 is `R24-STALE-PREMISE`, not `R24-PREMISE-STALE`. The heading bytes above are historical and are not rewritten; references from round 25 on use the lesson IDs. The lane-wide census of both spellings taken before this append is `.ufo/waves/round-25/w1/RevQualityLabels.md`.
```

Optional mirrored cross-note — append to the end of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-24.md` (after its last paragraph, the model-provenance debt paragraph), preceded by one blank line. Recommended for discoverability because defect 6 names both files, but the QUALITY append alone satisfies "align them by appended correction":

```markdown
Correction (2026-10-22, routed defect 6): the QUALITY 54/55 heading labels `R24-SUMMARY-RECALL` and `R24-PREMISE-STALE` are drift for this table's Mistake rows `R24-KEY-RECOLLECTION` and `R24-STALE-PREMISE`; `corpus/QUALITY.md` carries the appended alignment, and references from round 25 on use this table's IDs.
```

Neither draft rewrites any historical byte; both name the drift explicitly so the superseded spellings stay searchable.

## Residual risk and verification gaps

- [unk] Git packfile (.git) contents were not searched, per the assignment's exclusion. Historical blobs certainly contain both spellings (finding 3); this is immutable history and out of scope.
- [obs] The lane grep tool's case-insensitive mode misbehaved during this check: with `case=false`, the pattern `r24-(summar|key-rec|premise|stale-prem)` over the lane returned "No matches found" although case-sensitive runs of the equivalent uppercase patterns match the 13 files above. I filed this to the tool report channel and replaced that check with the explicit upper/lower alternation run (finding 4), which is unaffected. The census conclusion does not rest on the misbehaving mode.
- [obs] The tool's `skip` pagination parameter returned output identical to `skip=0`, so pagination semantics could not be exercised; saturation is instead established by the mutually consistent per-label and combined runs plus the scoped no-match run over production files and `tools/` (findings 4, 5).
- [inf] After the L1 appends the correction, QUALITY.md will intentionally contain both spellings side by side (the correction names the superseded labels). Future census runs should attribute those occurrences to this correction paragraph, not to new drift.

Scope: read=lane production files (corpus/QUALITY.md, corpus/lessons/round-24.md, corpus/lessons/round-24-verifier-spotcheck.md, SCORECARD.md section Round 25), round-24 wave reports, repo-wide greps including ignored files; wrote=.ufo/waves/round-25/w1/RevQualityLabels.md; executed=read-only git log -S pickaxe queries over the lane repo (four label pickaxes, exit 0)
Model: zai/glm-5.3-flash
Installs: none
