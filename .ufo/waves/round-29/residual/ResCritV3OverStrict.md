# ResCritV3OverStrict — owed counter v3 over-strictness, round 29 residual

Verdict: partly holds. At 06e00dafbbaa4695bc74decf68c816da8151b00a, counter v3 still scores 12 of 12, and none of the twelve landed markers depends on luck. Of the four shape families the assignment named, v3 accepts the `- ` list item and a prose `now` with numbers and units. It refuses a cited line shifted or appended by the round, a JSON marker with a `round` key, and a terse numeric `now`. Across every family tried, it refuses 19 of 27 should-pass variants (one item lost each, unless noted). Two of those refusals are clear defects with a small fix: cited lines shifted by the round's own insertion, and a JSON prose cross-reference that is counted as a second marker. The rest are tradeoffs that the judge should rule on.

Method [obs]: the sandbox clone is /fast/scratch/hyaku/tsukuroi-r29/ResCritV3OverStrict/repo, checked out at the tip. Counter sha256 1c37d49206e1e6656dd1c3115fb8fc2e594f6827d53b3830856a107678bf5891 (the v3 named in 75257ea6). The harness is /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/residual/ResCritV3OverStrict/harness.py (sha256 aa5451c0bb439d74a196e88c5706433fb2fe40a2ee28a24946caf566c29f415b). For each variant it applies a single edit on top of the tip, commits it in the sandbox clone only, and runs `python3 tools/check-owed-statements-r29.py --revision <sha> --lane <clone>`. Raw output is in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/residual/ResCritV3OverStrict/results.json (sha256 53e7a48766d5dd9d69d4b1086d72cd37a4d6b234c7d57c416e70ac69d374f5ef). The harness exited 0, and the unmodified tip gave rc 0 with marked 12.

## Findings

1. [obs] **`- ` list item: accepted.** Both `- [R29-OWED-O01] …` and `- **[R29-OWED-O01]** …` score 12 of 12 (results.json, variants `list-dash` and `list-dash-bold`).

   Every other CommonMark list or container form is refused with "M2 0 markers": `* `, `+ `, `1. `, nested `  - `, `-  ` (two spaces after the dash) and `> ` (blockquote). The cause is that `MARKER_START` and `MD_MARKER` hard-code `^(?:- )?` (/fast/scratch/hyaku/tsukuroi-r29/ResCritV3OverStrict/repo/tools/check-owed-statements-r29.py:116 and :118).
   - Impacted axis: depth (C1). These are false negatives, and the reported reason is misleading: the file plainly holds a marker, yet the counter says there are none.
   - Smallest safe correction: change the prefix in both regexes to `^ {0,3}(?:[-*+] +|\d{1,9}[.)] +)?`. Keep blockquotes refused; that is a tradeoff the judge can decide.
   - [obs] A capitalised verdict, `verdict: Corrected`, is refused with "M2 marker line is not in the required shape", because the regex uses `[a-z]+` (line 116; variant `verdict-capital`). The reason given is misleading, since the real failure is the M4 vocabulary. [inf] Keeping the verdict case-strict is a fair tradeoff, but the regex should capture `[A-Za-z]+` so the refusal is reported as M4.

2. [obs] **Inline HTML comment on the marker line: refused.** A marker line ending in ` <!-- r29 -->` scores 11, with O01 reported as "M2 0 markers" (variant `trailing-anchor-comment`).

   `live_lines` drops any line that contains `<!--`, even when the comment closes on the same line (check-owed-statements-r29.py:178-181).
   - Smallest safe correction: strip closed `<!--…-->` spans from the line before `marker_id`, and drop the line only when a comment stays open.

3. [obs] **Cited path line whose position changed because the round edited the file: refused. This is a defect.** The tip added two lines to SKILL.md at line 2320 (`git diff -U0 16e9ab2a 06e00daf -- SKILL.md` shows hunk `@@ -2319,0 +2320,2 @@`). That moves 186 non-blank, unchanged base lines down by 2.

   - Line 2400 at the tip is byte-identical to line 2398 at base (both read `| seat-scope | gate | …`). Citing it as `SKILL.md:2400`, its real current line number, gives "M6 no resolvable basis reference" (variant `path-shifted-by-round-insert`).
   - Inserting one note line near the top of corpus/knowledge/storage-health-r26.md drops the count to 10: O10 and O11 lose their only basis (lines 135 and 133). O09 and O12 survive only because S133 and S134 back them (variant `cited-file-insert-above`).
   - Appending to the end of a cited file keeps 12 of 12 (variant `cited-file-append-only`).

   The cause is the positional test `n <= len(base_lines) and base_lines[n - 1] == lines[n - 1]` (check-owed-statements-r29.py:225). It requires the same line number, when the stated intent is an unchanged line.
   - Impacted axes: depth, plus durability of the landed markers (see finding 9).
   - Smallest safe correction: map the tip line back to the base through `git diff -U0 CLAIM_BASE rev -- path`. Accept the line when it lies outside every added hunk (a context line), keeping the not-blank and not-a-marker tests. This still refuses every line the round authored. A weaker alternative, "the content occurs anywhere at base", is not safe: repeated lines such as `615.78.08` occur 4 times in capture.txt, and table separators or fence lines would match by chance.

4. [obs] **Line the round appended to the cited file, and bytes the round captured: refused. This is a tradeoff.**
   - Citing a line appended this round to storage-health-r26.md as `corpus/knowledge/storage-health-r26.md:136` refuses O10 (variant `path-appended-this-round`).
   - Citing committed source bytes fetched this round, `.ufo/waves/round-29/w1/RevOomMechanism/oom_kill.c:69`, refuses O07 (variant `path-this-round-capture`).

   [inf] Both refusals look intentional: they stop a round from citing evidence it wrote itself. A fresh capture can still be credited by registering it as an `S###` row (status `mined`, opened 2026-10-22, used-by listing the target file), and that is how O01-O04 pass.
   - Impacted axis: provenance stays strict, at the cost of an extra step for depth.
   - Correction: none required. State in the docstring that this-round paths are refused by design and that fresh evidence must go through an `S###` row, so a future writer is not surprised.

5. [obs] **JSON marker with a `round` key: refused.** Adding `"round": 29` gives "M2 JSON marker keys are not exactly …", and O09 is lost (variant `json-round-key`). So does a date key `marked_at` (variant `json-date-key`).

   So does adding the lane's own `corrections_r27` vocabulary, `marked_by` and `status`. Those keys are on every `corrections_r27` object in both JSON targets (verified by parsing the tip files; variant `json-r27-shape-keys`). The cause is the exact-set test `set(m) != JSON_KEYS` (check-owed-statements-r29.py:310). The docstring itself calls the shape "the round-27 `corrections_r27` pattern plus …" (line 35), yet the pattern's own keys are refused.
   - Impacted axis: depth (false negatives).
   - Smallest safe correction: require `JSON_KEYS <= set(m)`, with no repeated key, and allow extra keys only from an explicit metadata allowlist: `round`, `marked_by`, `marked_at`, `status`, `corrected_by`. Keep every other extra key refused, which preserves the v3 guard against alias keys such as `original`.

6. [obs] **A JSON prose cross-reference counts as a second marker. This is a defect.** Appending "See also R29-OWED-O06 for the action field." to O07's `now` refuses O06 with "M2 2 markers" (variant `json-crossref-in-now`).

   The JSON census adds `text.count('R29-OWED-' + iid)` minus the listed markers as phantom hits (check-owed-statements-r29.py:270-274). The same cross-reference mid-line in Markdown is harmless and scores 12 (variant `md-crossref-midline`), so the two file kinds disagree.
   - Smallest safe correction: count only `re.findall(r'"id"\s*:\s*"R29-OWED-' + iid + r'"', text)`. That still catches a marker object placed outside `corrections_r29`, which is the hollow shape the raw count was guarding.

7. [obs] **`now` with numbers and units: accepted when written as prose. A terse numeric `now` is refused, which is a tradeoff.**
   - A 33-token `now` full of figures ("oom_score_adj +200 adds 3,381,800 points (12.9 GiB) … 0.0 % margin.") scores 12, with spaced or glued units (variants `now-numbers-units` and `now-units-glued`).
   - A terse measurement line, `oom_score_adj=200 → 3381800 pts = 12.9 GiB; victim 14080000 pts = 53.7 GiB; 24.0 % of score; 1 pass, max wins.` (21 tokens), yields only 11 letter-words, 9 distinct. That fails M5 (12 and 10), because `words_of` drops tokens with no letter (check-owed-statements-r29.py:196-198). This was computed with the counter's own `words_of` and `norm`, not committed as a variant.

   [inf] Not counting bare numbers toward the floor is a defensible anti-padding choice.
   - Correction: none required. If the judge wants numbers to count, count a numeral token followed by a unit token as one word.

   [obs] The floor is lenient in the other direction: `GiB;` and `GiB` count as distinct words, because words are split on whitespace only.

8. [obs] **Shared correction across near-identical anchors: refused. This is a tradeoff.**
   - O02's anchor is "the +200 band is chosen first" and O04's is "the +200 band is scanned first", in different files. Reusing O02's `now` verbatim for O04 refuses O04 with "M5 now overlaps item O02 by more than 60 percent" (variant `now-shared-mechanism`).
   - Separately, `nows[iid] = wset` is recorded at line 342, before the basis check at line 350. So an item that later fails M6 still blocks a later item through the Jaccard test. [inf] This cascade is not exercised at the tip.
   - Smallest safe correction: move line 342 after a successful `basis_ok`. Keep the 60 percent rule, which is the anti-copy guard.

9. [obs] **No landed marker relies on luck at the tip.**
   - Every path cite resolves into a file that is byte-unchanged from the claim base 16e9ab2a to the tip: corpus/knowledge/memory-pressure-r25.md (402 lines at both), corpus/knowledge/storage-health-r26.md (135 at both) and .ufo/waves/round-27/capture/capture.txt (138 at both). An empty diff and `git log 16e9ab2a..06e00daf` lists no commit for any of the three. Positional equality therefore holds by construction, not by coincidence.
   - Among SKILL.md lines 2322 and later, no non-blank line equals its base line at the same number by chance. I computed 0 such lines, so a shifted SKILL.md cite cannot pass by accident today.
   - M5 margins are wide: the smallest marker is O05 with 25 words, 25 distinct, and the largest pairwise Jaccard is 0.256 (O05 and O06), against the 0.6 limit.
   - M7 opened cells are plain dates in all 151 SOURCES rows.

   [inf] The landed markers are fragile, though, because of finding 3. Inserting any line above line 387 of memory-pressure-r25.md silently drops O05, whose only basis is a path. Inserting above lines 133 and 135 of storage-health-r26.md drops O10 and O11. Inserting into capture.txt drops O08. Today the cited lines sit at or near the end of their files, so append-only edits are safe.

10. [obs] **The M7 opened date is frozen.** Setting S148 and S149 opened to `2026-10-23` (a source opened after UTC midnight while the round is still open) refuses O01-O04, giving marked 8 (variant `sources-opened-next-day`). The annotated cell `2026-10-22 (r29)` is refused the same way, but no current row uses that form.
    - [inf] This is a tradeoff, low risk for this round.
    - Correction: if the round can span two UTC dates, compare against the set of dates between the declaration commit and the revision.

Variants accepted, so not over-strict: `list-dash`, `list-dash-bold`, `path-range` (`file:387-390`), `path-dot-slash` (`./corpus/…:387`), `cited-file-append-only`, `md-crossref-midline`, `now-numbers-units` and `now-units-glued`.

Defects to fix, ranked by impact: finding 3 (positional cite identity), finding 6 (the JSON raw-substring census), finding 5 (exact JSON key set against the lane's own corrections pattern), finding 1 (list prefixes) and finding 2 (the inline comment). Tradeoffs for the judge: findings 4, 7, 8 and 10.

Scope: read=SCORECARD round-29 declaration via task brief, tools/check-owed-statements-r29.py (v3, full), SOURCES rows S121/S123/S133/S134/S148-S151, landed marker lines in the six target files, cited lines in memory-pressure-r25.md/storage-health-r26.md/round-27 capture.txt, git diff/log 16e9ab2a..06e00daf; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/residual/ResCritV3OverStrict.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/residual/ResCritV3OverStrict/harness.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/residual/ResCritV3OverStrict/results.json, sandbox clone and commits under /fast/scratch/hyaku/tsukuroi-r29/ResCritV3OverStrict/; executed=env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-local + checkout (sandbox), python3 tools/check-owed-statements-r29.py --revision HEAD (sandbox, exit 0, marked 12), python3 harness.py (27 sandbox variant commits, exit 0), read-only git diff/log/show/blame/ls-files, python3 one-off margin and Jaccard computations importing the counter
Model: not exposed
Installs: none
