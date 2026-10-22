# CritPaddingOverStrict — round 29 wave 2

Verdict: fails. At 10d5288f the adjacency counter wrongly refuses 15 of 19 should-pass register variants (13 are defects, 2 are disclosed tradeoffs), and it still accepts all 24 of 24 new should-fail padding shapes.

Method [obs]: I made a sandbox clone at /fast/scratch/hyaku/tsukuroi-r29/CritPaddingOverStrict/repo, checked out at 10d5288fc1051364e711203855e7c53710dfcc21. The counter there has sha256 f7a0e9d2f2cc0ca649baa86f42da63d6a247d2095179ce26474f568ed96affba, the same as the `counter_sha256` in .ufo/waves/round-29/measure/padding/padding-shapes-merged-counter.jsonl. The harness (.ufo/waves/round-29/w2/CritPaddingOverStrict/harness.py, sha256 92b051e2…) commits each variant of the register or PROVINCE.md on a detached HEAD in the clone. It then runs `tools/check-adjacency-overlap.py --revision <sha> --repo <clone>` with every GIT_* variable removed. The results are in .ufo/waves/round-29/w2/CritPaddingOverStrict/variants.jsonl (sha256 8d49ac6b…), one line per variant with its commit sha, exit code, anchored_rows and reasons. Every run reported `sibling-verified` against the live mori checkout. The control is a fresh commit of the tip bytes: exit 0, 6 of 6. The tip selftest gives 55 cases with 0 failures. None of my variants duplicates a shape in the round-29 padding receipts.

To decide what GitHub actually renders, I sent a probe file (.ufo/waves/round-29/w2/CritPaddingOverStrict/gfm-probe.md, sha256 9818c270…) to GitHub's own renderer: `gh api -X POST /markdown -f mode=gfm`, exit 0. The output is saved as gfm-probe.github.html (sha256 1676a986…).

## Over-strict: correct registers the counter now refuses

1. [obs] B13 refuses every row when the section has a nested heading anywhere, even an honest note after the table. Adding `### Round 29 follow-up` plus one sentence after the table gives exit 1 with anchored_rows 0; a `#### Note` does the same. The lane already uses this structure: PROVINCE.md:54 is `### Handoff checklist` under `## Adjacent — finding-to-owner handoffs`. The cause is tools/check-adjacency-overlap.py:170-172, where any heading of level 3 or deeper inside the section sets `invalid`, and line 208, which then returns `{}`. Axes: operability (honest edits zero the claim) and false refusal. [inf] The round-28 "withdrawn subsection" shape only needs the rows *after* a nested heading to stop counting, not the whole section to be invalidated.

2. [obs] B13 treats an indented code line as a heading. Two variants show it:
   - The section heading quoted in an indented code block in the Frontier section gives anchored_rows 0, because the section count reaches 2.
   - An indented `    ### example` code line inside the section also gives 0.

   GitHub renders the indented line as code, not a heading (gfm-probe.github.html:63, `<pre class="notranslate"><code class="notranslate">## Adjacent`). The cause is tools/check-adjacency-overlap.py:162, which tests the stripped line before the indent check at lines 176-179.

3. [obs] The HTML-comment stripper does not respect inline code. In variant `p-b13-inline-code-comment-opener`, the OV3 pointer cell mentions `` `<!--` `` in inline code, and rows OV3 to OV6 disappear: anchored_rows 2, reason `province-row-missing`. GitHub renders that cell as text and keeps the next row (gfm-probe.github.html:54 `<code class="notranslate">&lt;!--</code>` and line 57 `<td>OV4</td>`). The cause is tools/check-adjacency-overlap.py:125-141.

4. [obs] GFM delimiter rows with fewer than three hyphens are refused: `|-|-|-|-|` gives anchored_rows 0, and `| :-- | :-: | --: | -- |` gives 0. GitHub renders a one-hyphen delimiter row as a table (gfm-probe.github.html:2-15). The cause is the regex `:?-{3,}:?` at tools/check-adjacency-overlap.py:197.

5. [obs] One pipeless row (legal in GFM) zeroes the whole section. Writing OV3 as `OV3 | tsukuroi | AGREES | …` gives anchored_rows 0, not 5. That line resets `in_table` at lines 183-185, so every later OV row is seen before a delimiter and sets `invalid` at lines 189-191. GitHub keeps the pipeless row and every row after it in the table (gfm-probe.github.html:31-40).

6. [obs] A bold id cell `| **OV1** |` is refused (anchored_rows 5, OV1 `province-row-missing`). The owner and class cells already have `*` stripped (line 354), but the id cell only has backticks removed (lines 205-206). This inconsistency was not introduced by this commit, but it remains.

7. [obs] B15 ignores negation, so correct pointers are refused. Each of these gives anchored_rows 5 with `province-pointer-disagrees`:
   - OV4 (CONFLICTS): "mori F8 does not agree with the lane's OOMRules= qualifier …"
   - OV5 (CONFLICTS): "… mori agreed to correct its r12 entry"
   - OV3 (AGREES): "… mori does not contradict the lane"
   - OV3 (AGREES): "… mori HEAD no longer conflicts with the ancestor clause"

   The cause is the regex at tools/check-adjacency-overlap.py:105-111.

8. [obs] Tradeoff. The B4 five-word floor refuses a precise short anchor. Variant `p-b4-three-token-attribute-names` gives OV6 the quote "the `user.oomd_ooms` / `user.oomd_kill`" at line 198 and gets `quote-too-short` (anchored_rows 5). The floor is a disclosed length rule, but finding 13 shows it does not measure distinctiveness.

9. [obs] Tradeoff. B8 refuses both rows when two overlaps cite the same mori sentence: OV4 copying OV3's quote and line gives anchored_rows 4. The docstring states this, so it is a judgment for the judge to make, not a defect.

These should-pass variants are accepted, as they should be: OV6 quote_line corrected from 196 to 198 (the correction `corrections_r27_a2` records), OV4 quoting the OOMRules= sentence at memory-pressure-r25.md:387, OV2 quoting PROVINCE.md:30-31, and OV1 quoting the 5-token unit list.

## Padding shapes it still accepts (each exit 0, 6 of 6)

10. [obs] B8 is bypassed by shifting quote_line. In `f-b8-quote-line-shift`, OV4 copies OV3's quote with quote_line 145 instead of 146; the three-line window still contains it. In `f-b8-five-rows-one-sentence`, OV1 to OV5 all anchor fragments of the one OV3 mori sentence by mixing line shifts (144, 145, 146) with trimmed sub-quotes. The key at tools/check-adjacency-overlap.py:242 is the triple (path, the quote_line you declared, exact normalised quote), so neither a shifted line nor a substring collides. Axes: duplicate authority and padding.

11. [obs] Lane anchors have no uniqueness check. In `f-lane-anchor-reused`, OV1, OV4 and OV5 copy OV3's lane_quote from the allowed file. This is also accepted inside the five-rows shape above. The earlier receipt `r29-dup-anchor-lane-side-only` was only refused because it included OV2, which B9 catches.

12. [obs] B9 lets OV2 anchor on the register's own mirror. OV2's allowed file is PROVINCE.md, and two variants use that:
    - `f-b9-ov2-self-mirror`: OV2's lane_quote is its own pointer cell in the round-27 table.
    - `f-b9-ov2-section-heading`: OV2's lane_quote is the round-27 section heading text.

    Both are accepted. This is the self-referential shape that B5 forbids for register files, reached through the one allow-listed file that contains the mirror.

13. [obs] B10 counts punctuation inside a token as a boundary, because tools/check-adjacency-overlap.py:100-102 tests boundaries against `\w`. Three cuts are accepted:
    - `f-b10-version-cut`: OV5 "… does not exist in earlyoom 1.9", where the source says 1.9.0. This changes the version claim.
    - `f-b10-unit-name-cut`: OV1 lane "… `user@1000.service`, `user-1000", cut inside a unit name.
    - `f-b10-hyphen-cut`: OV3 "oomd is inactive and disabled here, and every unit the", which starts inside "systemd-oomd".

    `f-b4-five-function-words` (OV5 quote "is a statement about a", line 140) is also accepted. It shows the five-word floor only moved the floor.

14. [obs] B11 accepts filler. Every action set to "see the register row" is accepted, and so is "x x x x". The rule at line 349 counts whitespace-separated tokens and is the same test as A6.

15. [obs] Withdrawn content still counts:
    - `f-b12-withdrawn-in-action`: every action reads "WITHDRAWN: not an anchor any more, history only".
    - `f-b12-withdrawn-top-level-only`: a top-level `"status": "withdrawn"` plus a `corrections_r27_a2` entry withdrawing all rows. B12 at lines 256-257 checks only the keys inside each row.
    - `f-b13-prose-withdrawal`: the PROVINCE section gains a bold "**Withdrawn:** no row below is an anchor any more" line before the table.

16. [obs] B13 misses headings and wrappers that GitHub does render. Each of these is accepted:
    - `f-b13-setext-heading`: the table is placed under a setext h2 ("Withdrawn rows (history only)" over a dash line). GitHub renders a new `<h2>` that holds the table (gfm-probe.github.html:66-80).
    - `f-b13-setext-h1`: the same with an `===` underline.
    - `f-b13-html-heading`: an `<h3>` line before the table (rendered, line 87).
    - `f-b13-pre-block`: the table wrapped in `<pre>`. GitHub renders the rows as raw text with no `<table>` (lines 82-85).
    - `f-b13-details-collapsed`: the table inside a collapsed `<details>` labelled withdrawn. [inf] This one is weaker, because the table is visible once expanded.

    The heading test at line 162 recognises only ATX `#` headings, and no HTML block except comments is treated as opaque.

17. [obs] B15 misses paraphrased contradictions. Each of these is accepted:
    - OV4 (CONFLICTS): "in full agreement with the lane; nothing to report". `agree(?:s|d)?\b` does not match "agreement".
    - OV5 (CONFLICTS): "no conflicts: lane and mori say the same". `no\s+conflict\b` does not match the plural.
    - OV4 (CONFLICTS): "mori F8 is consistent with lane lines 387-390".
    - OV3 (AGREES): "mori disagrees: conflicting meaning of `auto`".
    - `f-b15-fifth-column`: a fifth "note" column carries "no conflict: lane and mori agree". Only column 4 is read (line 356).

    Combined with finding 7, B15 is wrong in both directions. [inf] Prose cannot be judged with a regex, so this is a tradeoff the judge should reject rather than one more pattern to add.

## Smallest safe corrections

- B13 nested headings (finding 1): a nested heading should end row collection, so rows after it do not count, instead of invalidating the section. This keeps the withdrawn-subsection receipt refused. [inf]
- Indented headings (finding 2): match headings only when the indent is under 4 columns, for both section counting and nested headings.
- Comment stripping (finding 3): remove code spans before scanning for `<!--`.
- Delimiter and pipeless rows (findings 4 and 5): relax the delimiter regex to `:?-+:?`. Once in a table, a non-blank line containing `|` continues it.
- Bold id (finding 6): strip `*` from the id cell, as is already done for owner and class.
- B10 boundaries (finding 13): use a boundary that also refuses a cut at an in-token `.`, `-`, `@`, `/` or `:`, that is `(?<![\w])(?<![\w][.\-@/:])…(?![\w]|[.\-@/:]\w)`. I tested this with b10fix.py (sha256 f3820e5b…), which monkeypatches only `contains_anchor`. The tip control stays at 6, the three cut shapes each fall to 5, the three accepted should-pass variants from the B9 and OV6 checks stay at 6, and the selftest stays at 55 cases with 0 failed (exit 0). [obs]
- B8 and lane reuse (findings 10 and 11): key each anchor on where its match actually sits in the file (start and end offsets), not on the declared quote_line. Refuse overlapping spans across rows, on both the sibling side and the lane side.
- OV2 self-mirror (finding 12): leave the lines of the round-27 section out of the PROVINCE.md text that OV2's lane quote is searched in.
- Withdrawn register (finding 15): limit top-level keys and correction `status` values to the round-27 set.
- Headings and wrappers GitHub renders (finding 16): treat setext underlines and `<h1>`–`<h6>` lines as headings, and treat `<pre>` blocks as opaque.
- B15 (findings 7 and 17): drop B15 from the counted claim and leave whether the pointer matches the class to reviewers, or replace the prose check with a structured field.

Impacted axes: C2 adjacency claim validity (false refusals undercount honest work, and accepted padding overcounts), duplicate authority (findings 10 to 12), and operability (findings 1 to 5 make normal markdown editing fragile).

Scope: read=SCORECARD round-29 task context, tools/check-adjacency-overlap.py at 10d5288f (docstring, rules, selftest), adjacency-mori-oom-r27.json, PROVINCE.md, memory-pressure-r25.md, the mori snapshot userspace-oom-killers-r26.md, the round-29 padding receipts; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/CritPaddingOverStrict.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/CritPaddingOverStrict/{variants.jsonl,harness.py,b10fix.py,gfm-probe.md,gfm-probe.github.html}, sandbox commits only in /fast/scratch/hyaku/tsukuroi-r29/CritPaddingOverStrict/repo; executed=sandbox `git clone --no-local` and `checkout` (GIT_* unset), `python3 tools/check-adjacency-overlap.py --revision HEAD` (exit 0, 6) and `--selftest` (55 cases, 0 failed), harness.py (44 variants, exit 0), b10fix.py (exit 0), `gh api -X POST /markdown -f mode=gfm` (exit 0), read-only git show/diff/log in the clone
Model: not exposed
Installs: none
