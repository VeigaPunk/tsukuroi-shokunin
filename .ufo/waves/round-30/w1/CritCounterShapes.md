# CritCounterShapes — round 30, wave 1: attack on the C1 counter `tools/check-btrfs-space-r30.py` at 8976ca92

Verdict: fails. The counter (sha256 `1bf7ee14…c079`) accepts 39 of the 49 should-fail shapes I built: 30 a mechanical counter could refuse, and 9 only a reviewer can. It also refuses 11 legitimate shapes, plus 1 debatable one (a BOM in the JSON). Six of the 11 are verbatim quotes of real round-30 snapshot lines. The stock battery stays clean (control 10, 0 of 46 accepted, 0 of 6 refused), so the battery does not measure these classes.

Harness and outputs, all under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/CritCounterShapes/`:
- `shapes.py` (sha256 `fee7e8d0…fa63a`) runs 57 shapes in `--tree` mode, reusing the battery's `base_fixture()`, and renders `SKILL.md` with `cmark --unsafe` for the marker shapes. Its output is `shapes-out.jsonl` (`d7119d5d…e8ff`).
- `gitmode.py` (`144f2609…e8af`) runs 6 shapes in `--revision` mode on commits that exist only in the scratch clone `/fast/scratch/hyaku/tsukuroi-r30/CritCounterShapes/repo`. Its output is `gitmode-out.jsonl` (`0e80af0b…e961`).
- `battery-stock-out.jsonl` (`1b640f06…e42d`) is the stock battery run from the clone.

Reproduce with `python3 shapes.py <clone> <outdir>` and `python3 gitmode.py <clone> <outdir>`. The fixture trees are regenerated on each run.

## Findings

### Quote rules R6 and R7

1. [obs] **Tag stripping lets a quote that is not in the source verify (A01, accepted, should fail; mechanical).**
   - The snapshot line is `Metadata writes <- do not -> succeed when unallocated space is exhausted.`
   - The quote `Metadata writes succeed when unallocated space is exhausted` verifies, and its meaning is the opposite of the line.
   - `sed -n 2p | grep -cF` on that quote gives 0.
   - Cause: `strip_markup` (counter lines 91-92) removes the regex `<[^>]*>` from every snapshot, including plain text and C source. Any span from a `<` to a later `>` is deleted, and the window is the three lines joined (line 227), so the deleted span can cross lines.

2. [obs] **The same stripping refuses verbatim quotes of real lines (A18, A20, A19a, all refused, should pass; mechanical).**
   - A18: `if (global_rsv->reserved < global_rsv->size)` is refused with "R6 quote not at the cited line".
   - A20: `* Path: /sys/fs/btrfs/<uuid>/allocation/` is refused.
   - A19a: an HTML line quoted verbatim with `&amp;` is refused.
   - Real round-30 snapshots have these lines. Among token-bearing lines, these can never verify verbatim:
     - `w1/ScribeSrcSpaceInfo/S159-space-info.c:1113` and `:1118` (global_rsv, D02 and D10)
     - `S159-space-info.c:2155` (reclaim, D05)
     - `w1/ScribeSrcKSysfs/S158-sysfs.c:37,39,40,721,1021,1064` (allocation, D06)
     - `w1/ScribeSrcBalance/S153-balance-filters.rst:50` (`usage=<percent>`, D03)
     - `w1/ScribeSrcFsUsage/S152-btrfs-filesystem.rst:366`
     - `w1/ScribeSrcMkfs/S155-mkfs.btrfs.rst:47,54,77` (DUP and metadata, D04)
   - Counter-accepted forms of these lines fail the wave's own verbatim check. Example: `sed -n Np | grep -cF` on `Path: /sys/fs/btrfs/ /allocation/` gives 0.
   - So the counter and the scribe contract define "quote" twice, in contradiction (duplicate authority). The battery's should-pass P02 (`mutants-btrfs-space-r30.py:199`, quote `…reclaim behaviour &` for source bytes `&amp;`) encodes the non-verbatim form as correct.
   - A19b is the mirror case: the unescaped quote is accepted, but `grep -cF` gives 0.

3. [obs] **Line numbering differs from `sed` (A15a, A16, A17 refused, should pass; A15b accepted, should fail; mechanical).**
   - The counter splits snapshots with `str.splitlines()` (line 219; captures at line 245; `SKILL.md` at line 137).
   - `splitlines()` also breaks lines at `\x0c` (form feed), `\x0b`, `\x1c`-`\x1e`, U+0085, U+2028, U+2029 and a lone `\r`. `sed` counts only `\n`.
   - With a form feed on line 2, the quote that `sed -n 3p` prints is refused at line 3 (A15a) but accepted at line 4, where `sed -n 4p | grep -cF` gives 0 (A15b).
   - The same happens for a lone CR (A16) and U+2028 in inline script (A17).
   - CRLF is handled correctly (A13 accepted), and so is a snapshot BOM (A14a accepted).
   - [obs] No round-30 peer snapshot currently contains these separators (a scan of `w1/` found none). The exposure is latent.

4. [obs] **The "cited line used by no earlier row" rule can be bypassed four ways (A06, A07, A09, A08, all accepted, should fail; mechanical).** In each case two rows cite the same sentence.
   - A06: D01 cites an empty line 1. `max(len(first),1)` at line 229 then allows `pos == 0`, which is the start of line 2. D02 then cites line 2.
   - A07: D01 cites line 2. D02 cites line 1 with a quote that starts at that line's last character (`X On ENOSPC …`).
   - A09: a byte-identical copy of the snapshot is registered under a second S-id.
   - A08: an aliased path `fixture/./S900.txt`. This verifies only in tree mode; see item 15.
   - Cause: `used_lines` (line 231) is keyed on (path string, line), not on content.

5. [obs] **Frozen tokens match as substrings (A10a and A10b accepted, should fail; mechanical).** Line 234 uses `t in q.lower()`.
   - D09's `data` matches inside `The metadata block groups hold the extent tree`.
   - D04's `dup` matches inside `A duplicate device id is rejected…`.

6. [obs] **Several bad rows verify that no counter can judge (A02, A03, A04, A11, A12, A23, all accepted, should fail; semantic).**
   - A02: the quote comes from a code comment that says the claim is wrong (`/* WRONG, removed in v6.1: unallocated space is never used … */`).
   - A03: the quote comes from the body of an HTML comment that is invisible on the rendered page.
     - This one is partly mechanical: comment and script bodies could be dropped before matching in HTML snapshots.
   - A04: the statement contradicts its quote.
   - A11: the quote is off-topic but has the token (`For usage of the device scan command…` for D03).
   - A12: the statement is 12 filler words (`a a a … a`).
   - A23: the snapshot is fabricated, with a matching registry sha256. Only re-fetching the URL and comparing the digest catches this, and the counter is offline.
   - A05 (one source for three unrelated rows, accepted) is legitimate. Whether a source really covers each question is for a reviewer.

### Host rules R8

7. [obs] **The host value can be a non-measurement (H01, H02, H03, all accepted, should fail; mechanical).**
   - H01: `2026` taken from `# captured 2026-10-22T21:13Z`.
   - H02: `7` taken from a `grep -n` prefix (`7:/sys/fs/btrfs/…:1008`).
   - H03: the statement says `1000000 bytes` while the value is `100`. The statement check at line 249 is `v not in statement`, with no digit boundary. The marker check at line 259 does use a boundary.

8. [obs] **The host value is not tied to the sysfs file its question names (H04, H05 accepted, should fail; mechanical).**
   - H04: D10's global-reserve value is read from the `data/total_bytes` line.
   - H05: D08, D09 and D10 all cite one capture line and one value.
   - H06 (accepted, should fail): a documentation example line serves as the "host capture". The proposed capture-line format rule refuses it mechanically; the provenance question remains a reviewer's.
   - The capture file is not hashed or registered anywhere.

### Marker rule R9 (checked against `cmark --unsafe` rendering, recorded in `cmark_context`)

9. [obs] **Five shapes hide the marker from a renderer while the counter sees it (K07, K08, K09, K10, K11, all accepted, should fail; mechanical).** The counter's fence and comment scanner (lines 131-150) does not follow CommonMark.
   - K07: an extra fence line `    ```` (4 spaces) closes the fence for the counter (`s = line.strip()` at line 138). CommonMark treats it as content, so cmark renders the marker inside `<pre><code>`.
   - K08: a fence line `` ```\x0c `` also closes the fence for the counter (`splitlines`). cmark again renders the marker inside `<pre><code>`.
   - K09: a `<script type="text/plain">` block hides the marker.
   - K10: a `<?hidden … ?>` processing instruction hides it (browsers treat it as a bogus comment).
   - K11: a `<![CDATA[ … ]]>` block hides it.

10. [obs] **The marker need not be a decision-table row (K03b, K04, K05, K06 accepted, should fail).**
    - K03b (mechanical): inside a `<details>` HTML block with no blank line, cmark renders the "table" as raw text.
    - K04 (mechanical): a lone marker followed by `===` renders as `<h1>` (setext heading).
    - K05 (mechanical): a lone marker inside prose renders as a paragraph line.
    - K06 (semantic): a second table under `## Withdrawn rows (do not use)`.
    - K03a (blank line inside `<details>`, so a real table that is collapsed when rendered) is accepted. I judge that acceptable: agents read raw bytes, so this is a tradeoff rather than a defect.

11. [obs] **Legitimate marker files are refused (K01a, K01b, K02, K12, K13, all refused, should pass; mechanical).**
    - K01a and K01b: a marker line followed by a trailing `<!-- reviewed r30 -->` or `<!-->` is refused. Line 143 makes any line containing `<!--` invisible.
    - K02: one earlier prose line containing the code span `` `<!--` `` hides every later marker, so all 10 rows fail.
    - K12: a line starting ```` ```a`b ```` is not a fence in CommonMark, but the counter opens one, and all 10 rows fail.
    - K13: an indented code block that shows ```` ```bash ```` text has the same effect, and all 10 rows fail.
    - K14 (marker with a no-break space after the id) is correctly refused.

### JSON rules R1 and R2

12. [obs] **Hidden or withdrawn rows are ignored (J01, J02, J03 accepted, should fail; mechanical).** These are the same family as the battery's F03 `status: withdrawn`.
    - J01: a second row with id `D01\u200b` and statement `WITHDRAWN: … the D01 claim is wrong`.
    - J02: top-level keys `"withdrawn": ["D01"]` and `"status": "superseded"`.
    - J03: a bare string row `D01 is withdrawn; see errata`.
    - Cause: rows other than D01-D10, non-dict rows and extra top-level keys are never checked (lines 170 and 186).
    - J04 (id written as `\u0044\u0030\u0031`, which is the same id) is correctly accepted. Duplicate keys hidden by escapes are caught, because the duplicate-key hook sees decoded keys.
    - A14b: the counter refuses a JSON file with a UTF-8 BOM. [inf] That is defensible: RFC 8259 §8.1 says writers MUST NOT add a BOM.

### Registry rule R4

13. [obs] **The registry row is not anchored to the registry table (R01, R02, R04 accepted, should fail; mechanical; R03 accepted, should fail; semantic).** `registry_rows` (lines 95-101) takes any line matching `^\| S\d{3} \|` anywhere in `corpus/SOURCES.md`.
    - R01: an S-row inside a fenced example counts as registered.
    - R02: an S-row inside an HTML comment counts as registered.
    - R03: a second table under `## Rejected candidates`.
    - R04: a second table whose 8th column header means something else (`verdict-word`). The cells are read by position only.

### Symlinks and paths: tree mode and revision mode disagree

14. [obs] **In tree mode, symlinks and path aliases verify (A21, A22, A08 accepted, should fail).** `tree_reader` (lines 78-84) checks the path string and `os.path.isfile`, which follows symlinks.
    - A21: a snapshot symlinked to a file outside the fixture tree verifies, so the counter read a file outside the tree.
    - A22: a snapshot symlinked to a sibling evidence file verifies.
    - A08: the aliased path `/./` verifies.

15. [obs] **Revision mode, which is the declared counting command, gives the opposite results (`gitmode-out.jsonl`).**
    - G1 and G2: the same symlinks are refused ("R4 snapshot sha256 not in source row"), because `git show` returns the link text.
    - G4 and G5: `/./` and `//` aliases are refused ("R5 snapshot missing").
    - G3: a dangling symlink whose link text is the "snapshot" sentence verifies 10 of 10 in revision mode (commit `91c24e00` in the scratch clone). Tree mode refuses it with R5.
    - So a "snapshot" that is not a file verifies under the real counting command.
    - [inf] Battery results for this class do not transfer from fixture mode to revision mode.

## Mechanical versus semantic

A counter can catch these, using the corrections below:
- A01, A06-A10, A15b, A19b, A21, A22 and G3
- H01-H05, and H06 through a capture-line format rule
- K03b, K04, K05, K07-K11
- J01-J03
- R01, R02, R04, and R03 by anchoring rows to the registry table

It can also stop refusing A15a-A20, K01, K02, K12 and K13.

Only a reviewer can catch these: A02 (a comment that negates the claim), A03 (partly mechanical for HTML), A04 (a statement that contradicts its quote), A11 (an off-topic quote), A12 (a hollow statement), A23 (a fabricated snapshot, unless a re-fetch checker exists), K06 (a "withdrawn" section) and the provenance of H06.

## Impacted axes

- **Depth (C1):** the `verified` count can be inflated by hollow, hidden, fabricated or duplicated rows.
- **Operability:** scribes must avoid real kernel and RST lines containing `<…>`. This is the sixth over-strict shape listed above, and it collides with the verbatim quote contract.
- **Calibration:** "battery 0 of 46" is read as robustness, but the battery measures only fixture mode and none of these classes.

## Smallest safe corrections, by rule

- **R6 (quote match):**
  - Match `norm(quote)` against the whitespace-normalised raw window. Drop tag stripping, or apply it only to `.html` snapshots and additionally require a raw-byte match.
  - Flip P02 to a verbatim `&amp;` quote.
- **Line splitting:** split snapshots, captures and `SKILL.md` on `\n` only, removing one trailing `\r` per line.
- **Cited-line uniqueness:**
  - Key `used_lines` on (sha256 of the snapshot bytes, line).
  - Refuse an empty cited line.
  - Require at least `min(len(q), 20)` characters of the quote to lie on line `line`.
- **R7 (tokens):** match tokens as whole words, using `re.search(r'(?<![a-z_])tok(?![a-z_])', q.lower())`.
- **R8 (host values):**
  - The capture line must have the form `/sys/fs/btrfs/<uuid>/allocation/<file>:<int>`, with `value` equal to that integer.
  - `<file>` must match the row's question.
  - (capture, capture_line) must be unique.
  - The statement must contain the value with digit boundaries.
- **R9 (markers):**
  - Line-start-only `<!--` block comments, ignoring code spans.
  - Allow a comment that opens and closes after the marker on the same line.
  - CommonMark fences: an opener or closer has at most 3 spaces of indent, a closer has only spaces or tabs after it, and a backtick info string contains no backtick.
  - Treat HTML block types 1, 3, 4, 5 and 6 (`<script`/`<pre`/`<style`/`<textarea`, `<?`, `<!X`, `<![CDATA[`, `<details`/`<div`…) as hiding until their end condition.
  - Require the marker to sit in a pipe table whose header and delimiter rows precede it with no blank line between. A cmark-gfm AST check is the robust form; only plain `cmark` is installed.
- **R1/R2 (JSON):** the top-level keys are exactly `{rows}`, every row is a dict, and the ids are exactly D01-D10.
- **R4 (registry):** read only the contiguous table that follows the canonical header (`corpus/SOURCES.md:5`), outside fences and comments.
- **Readers:**
  - Refuse symlinks in both readers: tree mode by `os.path.islink`/`realpath` under the root plus `normpath(p) == p`; git mode by `git ls-tree` mode `100644` only.
  - Add a battery shape for each class above, with should-pass shapes for A18, A20, K01 and K02.

Scope: read=tools/check-btrfs-space-r30.py and tools/mutants-btrfs-space-r30.py at 8976ca92, SCORECARD.md round-30 declaration, corpus/SOURCES.md header, round-30 w1 peer snapshot files (read-only scans); wrote=.ufo/waves/round-30/w1/CritCounterShapes.md, .ufo/waves/round-30/w1/CritCounterShapes/{shapes.py,gitmode.py,shapes-out.jsonl,gitmode-out.jsonl,battery-stock-out.jsonl,outside-snapshot.txt,gitwork/,work/}, /fast/scratch/hyaku/tsukuroi-r30/CritCounterShapes/repo (clone, fixture commits detached, left at 8976ca92); executed=git clone --no-local and git checkout/add/commit/clean in the scratch clone only (env -u GIT_*), python3 shapes.py, python3 gitmode.py, python3 tools/mutants-btrfs-space-r30.py (clone, exit 0; also once from the lane worktree path, which wrote only to its own temporary directory, same summary), cmark --unsafe, sed/grep -cF checks, sha256sum
Model: not exposed
Installs: none
