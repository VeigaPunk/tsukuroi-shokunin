Verdict: fails. Counter version 2 at 29bf87fa (sha256 4953203d…) accepts 33 new should-fail fixture shapes: 29 mechanical defects, 1 tradeoff that QUALITY 79 sanctions, and 3 semantic shapes. It also accepts four mutations of the real lane tree and still accepts the 7 semantic wave-1 shapes. It also refuses 9 legitimate SKILL.md layouts that GitHub's cmark-gfm renders as visible table rows. Battery version 2 reproduces as claimed (0 of 72 and 0 of 11), but it does not cover any of these shapes.

All counter line references point to /fast/scratch/hyaku/tsukuroi-r30/CritCounterV2/repo/tools/check-btrfs-space-r30.py, which is the tip bytes (`sha256sum` printed 4953203d2b03fe5e…6e55eba). The harness and outputs are in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/CritCounterV2/. Every new shape is in shapes2.py, and its output is shapes2-out.jsonl (sha256 32a11b93…). The oracle is cmarkgfm 2025.10.22, which wraps GitHub's cmark-gfm, run with the unsafe option and the GFM extensions. Each rendered verdict is in the `gfm` field of its shape line.

1. [obs] Baselines reproduce. Battery v2 against counter v2 gave control 10, should_fail_accepted 0 of 72 and should_pass_refused 0 of 11, with exit 0 (battery-v2-out.jsonl, last line). The new-harness CONTROL gave 10 of 10 with counter_sha256 4953203d… (shapes2-out.jsonl, line 1). The REAL-CONTROL run on the tip tree from `git archive` with the base fbfec6bd registry gave 10 of 10.

2. [obs] Rerun of the wave-1 CritCounterShapes shapes.py, unchanged (w1rerun/shapes-v2-out.jsonl, last line): 49 of 57 shapes are now judged correctly and 8 are still misjudged.
   - Still accepted although they should fail, all semantic: A02 (a quote taken from a code comment that says the opposite), A03 (a quote from an HTML-comment body inside a .txt snapshot), A04 (a statement that contradicts its quote), A11 (an off-topic quote that happens to carry the token), A12 (a hollow 12-word statement), A23 (a fabricated but self-consistent snapshot) and K06 (the marker sits in a "Withdrawn rows" table).
   - Still refused although it is legitimate, mechanical: A14b (a JSON file with a BOM; the failure is "R1 json invalid: Unexpected UTF-8 BOM"). [inf] Refusing a BOM is a defensible tradeoff, not a defect.
   - Revision mode (gitmode2.py, run in the private clone /fast/scratch/hyaku/tsukuroi-r30/CritCounterV2/gitclone; output gitmode2-out.jsonl): G1 to G5, which are the symlink and path-alias shapes, are all refused in both git and tree mode, and G0 reads 10.

3. [obs] Mechanical, should fail, and accepted only because of a fixture artefact in wave 1. The wave-1 host shapes H01 to H06 are now refused only with "R8 capture line lacks <key>", because their fixture captures omit the new capture key. They do not show that the underlying defect is fixed. Re-keyed variants are all accepted with 10 of 10 (shapes2-out.jsonl):
   - H01k: the value 2026 is the year in "sampled 2026-10-22".
   - H02k: the value 7 is a `grep -n` line number.
   - H04k: the value 5000 belongs to the total_bytes key on the same line.
   - H05k: two host rows share one measurement through a byte-identical copy of the capture, because `used_captures` is keyed by path, not by digest (lines 351-353).
   - H07: the line reads "unallocated: not read", so the key is present but negated.
   - H08: the value 454 is a digit run inside the hex filesystem UUID.
   Cause: `number_in` uses digit-only boundaries (lines 142-143), and the key check is a bare substring test that does not bind the value to the key (line 349).
   - Semantic, still accepted: H06k, where the capture is a documentation example line under .ufo/waves/round-30/ rather than a host reading.

4. [obs] Mechanical, should fail, on the real lane tree. Each case changes one row's value, statement and marker consistently, and v2 accepts each one with 10 of 10:
   - D09 value 95. On capture line 98, 95 is a line-number operand ("(device byte size, line 95)").
   - D09 value 998037782528. This is the device size, not the unallocated space.
   - D08 value 454 and D10 value 60902. Both are digit runs inside the fsid `1d02a454-c549-4a35-b567-89d60902af8e`.
   Evidence: the mutated tree at /fast/scratch/hyaku/tsukuroi-r30/CritCounterV2/v2run/real/REAL-D09-value-95-a-line-number-operand-on-line-98/ (SKILL.md:2614 reads "Host unallocated 95 bytes"), and the REAL-* lines of shapes2-out.jsonl.
   - [obs] The real D09 capture line is not a sysfs reading. It is seat-written arithmetic: capture line 98 begins "Unallocated bytes = 998037782528 (device byte size, line 95) - [229789138944 (data disk_total, line 28)". [inf] Semantic: R8's "capture contains value" check is satisfied by a derived line that any author can type. Whether lsblk's device size equals btrfs's device size is [unk].

5. [obs] Mechanical, should fail: R9 accepts markers that GFM hides, breaks or contradicts. The counter accepts all of these with 10 of 10, and cmark-gfm shows the problem:
   - The marker is hidden, so cmark-gfm finds no table row (`gfm_marker_in_table_row` is false, with 0 or 1 rendered mentions):
     - N01: the delimiter row has fewer cells than the header, so GFM renders a paragraph. `DELIM` (line 195) never compares column counts.
     - N07, N08, N09: the table sits inside a processing instruction `<?…?>`, a CDATA block or a `<!X…>` declaration, with a blank line before the table. These HTML block types run across blank lines, and `visible_table_lines` does not track them (lines 194, 210-231).
     - N10, N11, N12: the fence "closer" is followed by a form feed, preceded by a tab, or followed by a no-break space. v2 closes the fence because `s = line.strip()` (line 204) strips Unicode whitespace and the indentation test counts only spaces (lines 206-207). CommonMark keeps the fence open.
     - N13: `</pre >` closes the raw block in v2 (line 211 allows `\s*`), but cmark-gfm needs the exact `</pre>`.
     - N14: a fence opener with the info string `<!--` is read as a comment opener first, because the comment scan runs before fence detection (lines 214-223). The later `-->` then reopens visibility inside the code block.
   - The marker row renders, but the bytes the counter matched are invisible:
     - N02: the source sits in a cell beyond the header width, which GFM drops. The rendered row text is "statement".
     - N03: the source appears only inside `<!-- S900 -->` on the marker line. The rendered row text is "statement none".
     - N04: the host value appears only inside an inline comment. The source check and the value check search the raw line (lines 362-365).
   - A second mention renders, but the counter does not count it:
     - N05 (`R30\-D01`) and N06 (`R30&#45;D01`) both render as "R30-D01" (gfm_mentions 2). The mention check matches raw bytes (line 358).
   - Semantic: N15 puts the table in `<div hidden>`. cmark-gfm keeps the row, so it is renderer-dependent.

6. [obs] Mechanical, should pass: R9 refuses legitimate layouts. Each of these drops all ten rows to 0 of 10, while cmark-gfm renders the marker as the first cell of a visible table row:
   - P20: the table directly follows a closed `<!-- … -->` line.
   - P21: the table directly follows a fence closer.
   - P22: the table directly follows a paragraph line ("Rows:").
   - P23: a bare `<!--` appears mid-prose. CommonMark leaves it as literal text, but v2 opens a comment that never closes.
   - P24: a table cell contains an unclosed `<!--`.
   - P25: the delimiter row has no trailing pipe.
   - P26: the header row has no leading pipe.
   - P29: the fence info string is `html <!-- x -->`. The fence is never opened, so the closer flips the fence state.
   - P30: `<pre>` is closed by `</textarea>`. CommonMark accepts any of the four end tags.
   Cause: lines 239-241 require the line before the table to be blank or to start with `#`, and lines 214-222 and 228-231 implement comment and raw-block rules that differ from CommonMark.
   - [obs] P27 (CRLF line endings in SKILL.md and SOURCES.md) and P28 (a `#tag` line before the table) are accepted correctly.
   - [inf] The real SKILL.md (lines 2604-2605) uses a blank line before the header, so the claim is unaffected today. The risk is brittleness: one benign edit zeroes every row.

7. [obs] Mechanical, should fail: R6 and R7 still accept these.
   - N40: D02 cites line 1 of D01's snapshot and puts the 20 required characters on that line. Its quote then runs into line 2, which D01 already cites, and the frozen token "global reserve" is only on line 2. The reuse key is (sha256, line) (line 331), and the token check reads the whole window (line 335).
   - N41: "meta-data" satisfies D09's token "data".
   - N42: "de-dup" satisfies D04's token "dup". `word_in` treats a hyphen as a word boundary (lines 138-139). This is the same defect class as wave-1 A10a and A10b, which v2 claims to fix.
   - N43: a snapshot copy that differs by one trailing newline has a different digest, so the same sentence verifies twice.

8. [obs] HTML snapshots: three of the four `.html` shapes are defects. The fourth is sanctioned by the criterion.
   - Mechanical, should fail:
     - N45: the quote is the body of a multi-line `<!-- … -->` comment. Tags are stripped per line, and comment and script bodies are kept (line 129).
     - N46: the quote is the body of a `<script>` block.
     - N47: stripping `</td><td>` turns three separate cells into one sentence the page never shows: "unallocated space is exhausted never". The `verbatim_one_line` field is false.
   - Tradeoff, not a defect: N44 accepts an entity-unescaped quote, which fails the seat `sed | grep -cF` contract. corpus/QUALITY.md:151 (criterion 79) explicitly allows matching "after HTML tags are removed and entities unescaped".
   - [obs] Documentation drift: the same QUALITY.md:151 sentence still applies tag removal to every snapshot, but v2 R6 limits it to `.html` and `.htm` (docstring lines 31-33, code lines 128-130).

9. [obs] Mechanical, should fail: R4 still accepts these.
   - N50: a decoy copy of the registry header and the S900 row sits inside an HTML comment above the real table, and the real table lacks S900. `registry_rows` takes the first exact header line it finds, ignoring fences and comments, and stops there (lines 150-159). This contradicts the v2 docstring's "rows in fences, comments … do not count" (lines 25-26).
   - N51: the header is followed by a data row instead of a delimiter row, so it is not a table. The code skips line i+1 without checking it (line 153).
   - [obs] The base fbfec6bd has exactly one header line (line 5), so the decoy cannot be applied to the base comparison today.

10. [obs] Semantic, should fail: R1 still accepts N16, where `"supporting_citations": {"D01": "WITHDRAWN: wrong, do not use"}` passes. Only the names of the top-level keys are constrained (line 268).

Smallest safe corrections, each to be paired with a new battery shape (all mechanical):
- R8: bind the value to the key on the capture line. For example, match `^<path ending in KEY>:\s*(\d+)\s*$` and compare the captured group to `value`, instead of combining a substring test with number_in.
- R8: key `used_captures` on the capture's sha256 plus line, not on its path.
- R9 marker hiding: model CommonMark HTML block types 3, 4 and 5. Close fences only on an exact `^ {0,3}FENCE[ \t]*$`. Detect fence openers before scanning for comments. Match end tags exactly. Check that the delimiter row's column count equals the header's.
- R9 source and value checks: run them on the marker line after removing comments, and only on cells up to the header width. Count mentions after backslash escapes and entities are resolved.
- R9 over-strictness: accept a table start after any line that ends a block, or render with cmark-gfm.
- R6 and R7: treat a hyphen as part of a word in `word_in`. Require at least one frozen token on the cited line. Key line reuse on the normalised line text as well as on the digest.
- HTML snapshots: drop comment, script and style bodies before stripping tags, and replace a tag with a cell separator rather than a space. Alternatively, keep raw-verbatim matching and change QUALITY 79 to match.
- R4: apply the same fence and comment visibility pass to SOURCES.md, and require a delimiter row at i+1.

The semantic items (A02, A03, A04, A11, A12, A23, K06, H06k, N15, N16 and the derived D09 capture line) cannot be caught by a string counter. They belong to reviewer rows.

Scope: read=SCORECARD round-30 declaration context via assignment, tools/check-btrfs-space-r30.py and tools/mutants-btrfs-space-r30.py at 29bf87fa, w1/CritCounterShapes/{shapes.py,gitmode.py}, corpus/QUALITY.md:151, SKILL.md:2598-2615, corpus/knowledge/btrfs-space-r30.json, w1/ExecHostCapture/btrfs-allocation-capture.txt; wrote=.ufo/waves/round-30/w2/CritCounterV2.md, .ufo/waves/round-30/w2/CritCounterV2/{shapes2.py,shapes2-out.jsonl,shapes2-err.txt,gitmode2.py,gitmode2-out.jsonl,gitmode2-err.txt,battery-v2-out.jsonl,w1rerun/shapes.py,w1rerun/gitmode.py,w1rerun/shapes-v2-out.jsonl,w1rerun/shapes-v2-err.txt}, /fast/scratch/hyaku/tsukuroi-r30/CritCounterV2/{repo,gitclone,gfm,w1rerun,v2run,gitout}; executed=git clone --no-local and checkout 29bf87fa into /fast/scratch/hyaku/tsukuroi-r30/CritCounterV2/repo and gitclone (GIT_* unset), git remote remove origin in gitclone, git archive/show (read-only), python3 w1rerun/shapes.py (rc 0), gfm/bin/python shapes2.py (rc 0), python3 gitmode2.py on gitclone with commits only in gitclone (rc 0), python3 tools/mutants-btrfs-space-r30.py (rc 0), uv venv + uv pip install cmarkgfm
Model: not exposed
Installs: cmarkgfm 2025.10.22 (PyPI via `uv pip install` into the private venv /fast/scratch/hyaku/tsukuroi-r30/CritCounterV2/gfm; reason: GitHub cmark-gfm render oracle for the SKILL.md marker shapes)
