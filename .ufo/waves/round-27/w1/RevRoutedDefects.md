# RevRoutedDefects: round-26 routed defects 1 to 5 at db9eecfa

Verdict: defects 1, 2, 3 and 5 are confirmed as still present (defect 2 is live at db9eecfa, not latent, and worse than routed); defect 4 is changed, because both `.err` files are gone and confirmed absent.

Revision basis: items 1 to 3 and the scratch runs use the db9eecfa tree (a `git archive` export). Items 4 and 5 read the lane working tree, whose HEAD is 75784ea; db9eecfa is an ancestor of that HEAD (`merge-base --is-ancestor`, exit 0). The w1-dispatch.json file is byte-identical at both points.

## 1. Defect 1, withdrawn texts in storage-health-r26.json: confirmed

Named texts, with exact JSON paths in `corpus/knowledge/storage-health-r26.json` at db9eecfa:
- `rows[1].statement` (line 87), SH2: "clears them only on an explicit reset". Withdrawn as a universal at `corpus/knowledge/storage-health-r26.md:132`.
- `rows[3].statement` (line 180), SH4: "Ordinary reads do verify checksums". Withdrawn at md:131.
- `rows[5].statement` (line 271), SH6 trigger: "increments only when main power is lost while the controller had not reported it was ready to power off" and "so it is not a count of host-visible crashes". Both withdrawn at md:125.
- `rows[5].verdict` (line 273), SH6: "HEALTHY". md:125 splits the verdict: HEALTHY for media and data integrity errors and error-log entries (both 0), UNVERIFIED for the 200 unexpected power losses.
- `rows[2].quotes[4].location` (line 163), S129 quote: "btrfs-scrub.rst line 190". md:134 says the quote is at line 192.

S129 snapshot: `.ufo/waves/round-26/sources/S129.rst:192` reads "*  *Uncorrectable* -- errors detected at read time but not possible to repair from other copy". Line 188 is a different "Uncorrectable:  72" line inside a code block. The snapshot sha256 is 7900b474aebfee2be79ff168c750f282ee33803ee6914928c20117a24aefe3f0 in both the export and the lane, equal to the anchor at `corpus/SOURCES.md:135`.

No in-file marker: a case-insensitive search of the JSON for withdrawn, correction, superseded, narrow, amend and stale finds only quoted source text. The top-level keys (schema, entry, lane, round, claim, drafted_by, drafted_at, capture, verdict_vocabulary, counting_note, adjacent, rows) carry no correction field.

[obs] The same unmarked class also appears in four statements the spot-check does not name: `rows[0].statement` (line 30, "under shorter names (write_errs, read_errs, flush_errs, corruption_errs, generation_errs)"; md:128 says only write, read and flush have shorter names); `rows[2].statement` (line 130, "systemd sets that attribute on journal files by default"; md:135 calls it stale for systemd 262); `rows[3].statement` (line 180, "No scrub record exists on this host"; narrowed at md:133); and `rows[4].statement` (line 229, "FAILED! otherwise"; md:129 says it holds only after a successful SMART log read).

## 2. Defect 2, K01 to K06 compare the round with its own record: confirmed, live at db9eecfa

Reference logic in `tools/check-self-assessment.py`:
- Line 361 (`reference_lines`) and its docstring at line 365: any line of any section whose heading contains "measured outcome" qualifies, "from any round". Nothing excludes the declaring round.
- Line 424 reads `declaring_round` from the last `## Axes — ` heading. Line 425 builds `reference` and never uses that round number. `declaring_round` is only reported (line 769).
- Lines 474–513 are the K01 to K06 loop. Line 484 skips the axes table itself, line 486 keeps only lines in `reference`, and lines 492–493 let the last matching transition win (`observed = after`, `observed_line = index + 1`). Lines 512–513 record the check.
- Lines 910–917 (selftest `declaring-round-measured-outcome-line`) assert that a round-1 measured-outcome line sets K01's reference. That is the self-read.
- QUALITY 65 (`corpus/QUALITY.md:132`) forbids this. The tool does not implement it.

Run: `python3 tools/check-self-assessment.py --revision <scratch commit>` on the db9eecfa tree (scratch commit 5e6a7670, one commit, exit 1). declaring_round is 26, and the axes heading is "## Axes — current self-assessment (round 26)" at SCORECARD.md:970. Each of K01 to K06 reports observed_line 960, inside "### Round 26 measured outcome" (lines 951–961). Example: K01 reads "axes table depth score 8 equals the after-value 8 of the last recorded transition (SCORECARD.md:960)". All six match, so the round's calibration checks pass against its own record.

[obs] The round-27 section (SCORECARD.md:983 on) has no axes table, so at db9eecfa the checker still treats round 26 as the declaring round.
[obs] The same run reports one mismatch, K10 (lines 574–582): "depth row states 28 lesson files; corpus/lessons holds 29 files". The depth row is at SCORECARD.md:976. `ls corpus/lessons | wc -l` gives 29 at db9eecfa. K10 counts files, not history, so the single-commit scratch history does not cause it. [inf] The extra file is probably `corpus/lessons/round-26-verifier-spotcheck.md`, which the table's count predates. The round-26 falsify record's "0 of 27" (SCORECARD.md:962) is for revision 7dfea92, not db9eecfa.
[obs] SCORECARD.md has two identical headings "## Axes — current self-assessment (round 26)" at lines 938 and 970; the checker reads the last one.

## 3. Defect 3, Gate column offset in check-storage-health.py: confirmed, reproduced end to end

Function-level reproduction with the db9eecfa `tools/check-storage-health.py`: for the unquoted S128 Gate row, `cell_spans` returns the texts `''`, `'S128'`, the URL, `'2026-10-22'`, the quote text, the location and `''`. `cell_quotes(row, 3)` returns `['2026-10-22']`. With the same quote in double quotes, it returns `'The device stats keep persistent record of several error classes related to'`.

The offset, by line:
- Lines 103–105 (`split_cells`) strip the outer pipes, so the header `| Source | URL | Opened | Located quote … | Location |` gives the quote column index 3 (set in `gate_quotes`, lines 344–345).
- Line 71 (`CELL_SPLIT`) and lines 150–163 (`cell_spans`) split the raw line, which starts with a pipe. That makes an empty span at index 0, so every cell sits one index higher, and index 3 is the Opened cell.
- Lines 204–219 (`cell_quotes`): a quoted cell is found by the scan to the line end (lines 214–215), so quoted cells work. A plain cell falls back to `spans[3]` (lines 218–219), which is the Opened date.

End to end, on the scratch copy: the base (every Gate quote quoted) gives `python3 tools/check-storage-health.py --revision <base>` exit 0, status PASS, verified_rows 6, findings []. A scratch variant with one Gate cell unquoted (commit c71b96e) gives exit 1, status FAIL, verified_rows 5, and finding `SH-GATE-QUOTE-MISSING` at site "SH2: S128".

Why it is latent for the present lesson: every Gate quote in `corpus/lessons/round-26.md` is quoted, so the checker passes today. The selftest never writes an unquoted Gate cell. `tools/check-storage-health.py:902` writes each fixture cell in double quotes, so the QUALITY 64 cell shapes are not covered (`corpus/QUALITY.md:131`).

[obs] `corpus/lessons/round-26.md:90` says the tool reads "from the column after `Opened` onward". The reproduction shows that the plain read lands on the Opened cell itself. The lesson wording should be corrected with the fix.

## 4. Defect 4, the two .err files: confirmed gone; routed defect is changed (closed)

- `ls -la` on `.ufo/waves/round-26/w1-dispatch.err` and `.ufo/waves/round-26/w2-dispatch.err` in the lane: "No such file or directory" for both (exit 2).
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain --untracked-files=all` (exit 0) lists only these untracked paths: `.ufo/waves/round-27/w1-dispatch.json`, `.ufo/waves/round-27/w1-spec.json`, `.ufo/waves/round-27/w1-taskresult.json`, `.ufo/waves/round-27/w1/swarm-registry.json`, `corpus/lessons/round-27.md`. No `.err` line appears.
- Neither file is tracked at db9eecfa: `git ls-tree -r --name-only db9eecfa876a865f799aa56856a780d299b4f067 | grep -c 'round-26/w[12]-dispatch\.err'` gives 0.
- [obs] The class persists elsewhere. 19 `.err` files are tracked at db9eecfa: 10 under `.ufo/waves/round-24/`, 6 under `round-25/` and 3 under `round-26/w2/RerunC1/`. All 19 are 0 bytes (`find .ufo -name '*.err' -size 0` gives 19 of 19). The routed remedy, "write validator stderr outside the lane repo", has not been applied to them.

## 5. Defect 5, dispatched text versus validated taskCall: confirmed at the record level; sent bytes unknown

- `.ufo/waves/round-26/w1-dispatch.json` is byte-identical at db9eecfa and in the lane (sha256 8e67391819d7c1f97439d787eaee5e81df859fe3fd0785f5de9e1587c3128164).
- Compared task: `taskCall.tasks[0]`, seat `SrcBtrfsDeviceDoc` (agent `scribe`), 1480 characters, ending "Report: write your scoped findings to .ufo/waves/round-26/w1/SrcBtrfsDeviceDoc.md". It contains no "Tooling directive" string and no "plymouth" text. `w1-spec.json` also has zero "Tooling directive" matches.
- What the round-26 report says was sent: `corpus/lessons/round-26-verifier-spotcheck.md:28`, "in both waves each seat's task text carried the operator tooling-directive block after the validator's text, so the dispatched text differs from the validated `taskCall`". The validated record lacks the block, which matches the report's description of the difference. The round-26 lesson does not mention the block (`grep -i tooling corpus/lessons/round-26.md` returns nothing).
- [unk] The bytes actually transmitted cannot be observed from the lane, because no round-26 transcript is readable here. The difference is confirmed from the report and the record only.
- [obs] The untracked round-27 `w1-dispatch.json` and `w1-spec.json` contain no "Tooling directive" string either. That does not show whether round 27 sent it. [unk]

## Residual risk and verification gaps

- The K01 to K06 run used a one-commit scratch repository. K01 to K06 read only SCORECARD.md, so their results do not depend on history. The K10 mismatch is a file count and holds at db9eecfa.
- The Gate end-to-end result comes from a one-cell variant I made in the scratch copy. The lane was not touched.
- Item 5's transmitted text is [unk].
- No lane tool ran. The checkers ran only in the scratch copy.

Scope: read=lane at db9eecfa via git-archive export (corpus/knowledge/storage-health-r26.json and .md, corpus/lessons/round-26.md and round-26-verifier-spotcheck.md, corpus/QUALITY.md, corpus/SOURCES.md, SCORECARD.md, tools/check-self-assessment.py, tools/check-storage-health.py, .ufo/waves/round-26/sources/S129.rst); lane working tree (.ufo/waves/round-26/w1-dispatch.json, w1-spec.json, .ufo/waves/round-26/w1/ConnSiblingOverlap.md, the two .err paths, the .ufo/waves/round-27 listing, corpus/lessons/round-27.md); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w1/RevRoutedDefects.md and /fast/scratch/hyaku/tsuku27/RevRoutedDefects/ (export, scratch commits, selfassess-base.json, selfassess-base.err); executed=`git archive db9eecfa | tar -x` into the scratch export; `git init`, `git add -A`, `git commit` in the scratch export only (no remote, no lane writes); `git -C <lane> status --porcelain --untracked-files=all` (exit 0); `git -C <lane> ls-tree`, `rev-parse` and `merge-base --is-ancestor` (exit 0); `ls -la` on the two .err paths (exit 2); `sha256sum`; `grep`, `sed`, `find` and `python3` read-only inspection; `python3 tools/check-self-assessment.py --revision <scratch>` (exit 1, one mismatch, K10); `python3 tools/check-storage-health.py --revision <scratch base>` (exit 0, PASS 6 of 6) and `--revision <scratch variant>` (exit 1, FAIL 5 of 6)
Model: anthropic/claude-haiku-5-5 (as shown in the host project-context block; not otherwise verified)
Installs: none
