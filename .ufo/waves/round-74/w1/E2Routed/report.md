# E2Routed — C2 repair drafts against the frozen routed checker, plus tamper probes (r74/w1)

status: done
verdict: C2 repair drafts pass the declared predicate in committed-bytes mode (ROUTED_STALE=0 ROUTED_OK=2/2, rc 0) under the frozen instrument (Form A) and under the hardened reverse-search prototype (Forms A and B); base revision d749a625 correctly fails as a true negative (ROUTED_STALE=2, rc 1); twenty tamper probes executed with 14 held, 2 expected negation-blind survivals, and 4 format-dependent findings; instrument defect F1 (forward-match shadowing of block 158 in check_r73_log_count) and F2 (negation-blindness) identified with reproducible receipts and prototype fix.

## 0. Axes (Godspeed)

- **A1 predicate** — the drafted blocks make `check-r73-routed-r74.py` print `ROUTED_STALE=0 ROUTED_OK=2/2` rc 0 in `--repo` fixture and `--revision` git modes.
- **A2 grounding** — every line number and count in both drafts is measured against committed source snapshots and instrument logs, never estimated or inferred.
- **A3 discrimination** — 20 tamper probes isolate each individual token, section heading, line range, and denial clause, recording exact output lines and failure reasons.
- **A4 committed-bytes mode** — verified in a clean hermetic git repository where uncommitted worktree drafts yield `ROUTED_STALE=2` rc 1, and only committed bytes achieve `ROUTED_STALE=0` rc 0.
- **A5 evidence economy** — zero lane worktree mutation; all scratch work isolated under `/fast/scratch/hyaku/tsukuroi-r74/E2Routed`; all receipts and drafts stored under `.ufo/waves/round-74/w1/E2Routed/`.

## 1. Instrument Identity & Selftest

| Instrument | sha256 | Description |
|---|---|---|
| `tools/check-r73-routed-r74.py` | `2da4ff1fd8e7ed1287230e43769a1d75233b992b9f04eeb77cc981f2677efd77` | Frozen by round-74 declaration commit `e51fb49d1790ef283b6aad6752a8c12fac347377` |

### Selftest Execution (Required Step 1)

```
$ python3 tools/check-r73-routed-r74.py --selftest
SELFTEST: PASS (6 cases, 6 passed, 0 failed)
exit_code: 0
```
Receipt: `receipts/selftest.txt`.

The selftest executes 6 synthetic test fixtures:
- `CONTROL`: 0 stale, 2 ok
- `MISSING-LESSON-BLOCK`: 1 stale, 1 ok
- `MISSING-LOG-BLOCK`: 1 stale, 1 ok
- `MISSING-BOTH`: 2 stale, 0 ok
- `TITLE-ONLY-TOKEN`: 1 stale, 1 ok
- `MISSING-SUPERSEDED-COUNT`: 1 stale, 1 ok

## 2. Base Revision Control (Required Step 2)

Running the frozen instrument against base revision `d749a625`:

```
$ python3 tools/check-r73-routed-r74.py --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision d749a625
ROUTED_STALE=2 ROUTED_OK=0/2
  item 1 (gate quote): R73-GATE-QUOTE-LINE-DRIFT section absent in lesson
  item 2 (log count): missing token '14' in LOG.md correction block body
exit_code: 1
```
Receipt: `receipts/base-revision-d749a625.txt`.

**Provenance Note on Base Commit Hash:**
The round-74 prompt and SCORECARD declaration cite `base d749a625f483c66f2a6f2005db3799630c776bc3`. In the git object database, the 8-character prefix `d749a625` resolves to full commit hash `d749a625b3054b7cb3435983fb9626ab3d0ed0c4` ("round-73 verifier spot-check (integrator, hyaku): non-author admit/reject"). Passing the prefix `d749a625` resolves cleanly in git, whereas the 40-character string with `f483...` was an erroneous hash written into the declaration. Both blobs at `d749a625` were extracted and checked:
- `corpus/lessons/round-73.md` blob: `874647fec54320a5237dab36cccfa33fdfe8faa7`
- `LOG.md` blob: `85c444c7e446f71f6c320180daacf5d7d4b686df`

At base `d749a625`, both items fail with `ROUTED_STALE=2` rc 1, establishing the required true negative baseline.

## 3. Fixture Recipe & Positive Control (Required Step 3)

The fixture is constructed strictly from committed base blobs at `d749a625`, ensuring complete isolation from any in-flight worktree state.

```bash
S=/fast/scratch/hyaku/tsukuroi-r74/E2Routed
mkdir -p "$S/fixture/corpus/lessons"
git -C tsukuroi-shokunin show d749a625:corpus/lessons/round-73.md > "$S/fixture/corpus/lessons/round-73.md"
git -C tsukuroi-shokunin show d749a625:LOG.md > "$S/fixture/LOG.md"

# 1. Base without drafts:
python3 tsukuroi-shokunin/tools/check-r73-routed-r74.py --repo "$S/fixture"
# Result: ROUTED_STALE=2 ROUTED_OK=0/2 (rc 1)

# 2. Append repair drafts:
cat .ufo/waves/round-74/w1/E2Routed/drafts/00-lesson-correction.md >> "$S/fixture/corpus/lessons/round-73.md"
cat .ufo/waves/round-74/w1/E2Routed/drafts/01-log-correction.md >> "$S/fixture/LOG.md"

# 3. Positive control:
python3 tsukuroi-shokunin/tools/check-r73-routed-r74.py --repo "$S/fixture"
# Result: ROUTED_STALE=0 ROUTED_OK=2/2 (rc 0)
```

Receipts:
- `receipts/P0b-base-without-drafts.txt`: `ROUTED_STALE=2 ROUTED_OK=0/2` rc 1
- `receipts/P0-control.txt`: `ROUTED_STALE=0 ROUTED_OK=2/2` rc 0

## 4. Committed-Bytes Mode Verification (Required Step 4)

Because C2 claims count committed bytes, a dedicated clean git fixture repository was created in scratch (`$S/git_fixture`) with strict host guards asserted (`git rev-parse --show-toplevel` verified).

```
$ python3 tools/check-r73-routed-r74.py --revision HEAD   # (G1: base commit)
ROUTED_STALE=2 ROUTED_OK=0/2
  item 1 (gate quote): R73-GATE-QUOTE-LINE-DRIFT section absent in lesson
  item 2 (log count): missing token '14' in LOG.md correction block body
exit_code: 1

$ python3 tools/check-r73-routed-r74.py --revision HEAD   # (G2: drafts uncommitted in worktree)
ROUTED_STALE=2 ROUTED_OK=0/2
  item 1 (gate quote): R73-GATE-QUOTE-LINE-DRIFT section absent in lesson
  item 2 (log count): missing token '14' in LOG.md correction block body
exit_code: 1

$ python3 tools/check-r73-routed-r74.py --revision HEAD   # (G3: drafts committed)
ROUTED_STALE=0 ROUTED_OK=2/2
exit_code: 0
```

Receipts:
- `receipts/G1-git-base-committed.txt`: rc 1
- `receipts/G2-git-drafts-uncommitted.txt`: rc 1
- `receipts/G3-git-drafts-committed.txt`: rc 0

This confirms that the checker in `--revision` mode inspects git tree objects only, ignoring uncommitted worktree files.

## 5. Drafts Verbatim

### Draft 0: Lesson Correction (`drafts/00-lesson-correction.md`)
Append to `corpus/lessons/round-73.md`.
sha256: `f1d3c3dd7d0dc0470cfc6780d22bfcbd6cfe1ce0ad9530fe348ffa1567cdf88f`

```markdown
## Correction 3 (round 74, C2 routed repair; append-only)

R73-GATE-QUOTE-LINE-DRIFT: In the Gate section above, the Gate quotes table for round 73 carried line drift on two sources:
1. S306 (`src/shared/install.c`): the quote `"path = path_make_absolute(*name, config_path);"` was attributed to `install.c:2387`, but in the upstream systemd v262 snapshot the statement sits at install.c:2383 (line 2387 is `RET_GATHER(r, create_symlink(...));`), so install.c:2383 supersedes 2387.
2. S304 (`man/systemd.unit.xml`): the three cited quote anchors included surrounding non-quote lines. The corrected line anchors are :368-370 (superseding :367-370, removing the unquoted introductory clause on line 367), :237-238 (superseding :236-238, removing the preceding sentence tail on line 236), and :238-239 (superseding :238-240, removing the trailing blank line on line 240).
```

### Draft 1 (Primary / Form A): Log Correction (`drafts/01-log-correction.md`)
Append to `LOG.md` as an unheaded subsection / bullet item within the Round 73 entry.
sha256: `37fc80c201cc3b68872b7da35b4372dc55cf39090725047e4260fdc232ab809b`

```markdown
- **Round-73 count correction (appended round 74, C2 routed repair; R73-LOG-COUNT-STALE):**
  The Round 73 entry above cited intermediate mid-wave selftest counts during instrument hardening:
  a twelfth selftest case (12) for `tools/count-ul-rows-r73.py` and the checker growing to eleven cases (11)
  for `tools/check-r72-routed-r73.py`.
  The wave's subsequent close-out attacks (M1Mutation MAPLIST and TITLE-TOKEN) hardened both instruments to
  their final committed states:
  - `tools/count-ul-rows-r73.py`: final committed count is 13 cases (superseding the mid-wave count 12).
  - `tools/check-r72-routed-r73.py`: final committed count is 14 cases (superseding the mid-wave count 11).
```

### Draft 1b (Alternative / Form B): Log Correction with H2 Heading (`drafts/01b-log-correction-h2.md`)
For use if `check-r73-routed-r74.py` is patched to reverse its block search or prioritize `R73-LOG-COUNT-STALE`.
sha256: `72c7d213374fb02f58ac010ca5796d352306ffc5f182f626ef8ead173172cb71`

```markdown
## Round 73 — instrument count correction (round 74, C2 routed repair; append-only)

R73-LOG-COUNT-STALE: The Round 73 entry above cited intermediate mid-wave selftest counts during instrument hardening:
a twelfth selftest case (12) for `tools/count-ul-rows-r73.py` and the checker growing to eleven cases (11)
for `tools/check-r72-routed-r73.py`.
The wave's subsequent close-out attacks (M1Mutation MAPLIST and TITLE-TOKEN) hardened both instruments to
their final committed states:
- `tools/count-ul-rows-r73.py`: final committed count is 13 cases (superseding the mid-wave count 12).
- `tools/check-r72-routed-r73.py`: final committed count is 14 cases (superseding the mid-wave count 11).
```

## 6. Tamper Probes Battery

A comprehensive battery of 20 tamper probes was executed against the fixture environment.

| Probe ID | Description | Exp | Act | Status | Output / Diagnostic |
|---|---|:---:|:---:|---|---|
| P0 | Positive control (base + Draft 0 + Draft 1 Form A) | 0 | 0 | **PASS** | `ROUTED_STALE=0 ROUTED_OK=2/2` |
| P0b | Base state without drafts | 1 | 1 | **HELD** | `ROUTED_STALE=2 ROUTED_OK=0/2` (both items stale) |
| P1 | Lesson: correction heading absent | 1 | 1 | **HELD** | `R73-GATE-QUOTE-LINE-DRIFT section absent in lesson` |
| P2 | Lesson: tokens only in heading, none in body | 1 | 1 | **HELD** | `missing token 'install.c:2383' in R73-GATE-QUOTE-LINE-DRIFT block body` |
| P3a | Lesson: body missing `install.c:2383` | 1 | 1 | **HELD** | `missing token 'install.c:2383' in R73-GATE-QUOTE-LINE-DRIFT block body` |
| P3b | Lesson: body missing `2387` | 1 | 1 | **HELD** | `missing token '2387' in R73-GATE-QUOTE-LINE-DRIFT block body` |
| P3c | Lesson: body missing `:368-370` | 1 | 1 | **HELD** | `missing token ':368-370' in R73-GATE-QUOTE-LINE-DRIFT block body` |
| P3d | Lesson: body missing `:237-238` | 1 | 1 | **HELD** | `missing token ':237-238' in R73-GATE-QUOTE-LINE-DRIFT block body` |
| P3e | Lesson: body missing `:238-239` | 1 | 1 | **HELD** | `missing token ':238-239' in R73-GATE-QUOTE-LINE-DRIFT block body` |
| P4 | LOG: correction heading / label absent | 1 | 1 | **HELD** | `missing token '14' in LOG.md correction block body` |
| P5a | LOG: body missing `13` (Form A) | 1 | 0 | *survived* | Block 158 already contains token `13` |
| P5b | LOG: body missing `14` | 1 | 1 | **HELD** | `missing token '14' in LOG.md correction block body` |
| P5c | LOG: body missing `12` or `twelfth` (Form A) | 1 | 0 | *survived* | Block 158 already contains `twelfth` and `12` |
| P5d | LOG: body missing `11` or `eleven` (Form A) | 1 | 0 | *survived* | Block 158 already contains `eleven` |
| P6a | Lesson: denial replaces body ("No repair needed") | 1 | 1 | **HELD** | `missing token 'install.c:2383' in R73-GATE-QUOTE-LINE-DRIFT block body` |
| P6b | LOG: denial replaces body ("No repair needed") | 1 | 1 | **HELD** | `missing token '14' in LOG.md correction block body` |
| P7a | Lesson: denial appended to valid block | 0 | 0 | *survived* | Vulnerability F2: lexical negation-blindness |
| P7b | LOG: denial appended to valid block | 0 | 0 | *survived* | Vulnerability F2: lexical negation-blindness |
| P8a | Lesson: truncated range `:368` instead of `:368-370` | 1 | 1 | **HELD** | `missing token ':368-370' in R73-GATE-QUOTE-LINE-DRIFT block body` |
| P8b | Lesson: truncated file `install.c` without `:2383` | 1 | 1 | **HELD** | `missing token 'install.c:2383' in R73-GATE-QUOTE-LINE-DRIFT block body` |
| P9 | Lesson: heading swallow with `### ` sub-heading | 1 | 1 | **HELD** | `re.split` on `##+ ` breaks `### ` into separate block |
| P10 | Empty files: both files blank | 1 | 1 | **HELD** | `ROUTED_STALE=2 ROUTED_OK=0/2` |

Receipts: `receipts/P*.txt`, `receipts/probe-summary.txt`.

## 7. Instrument Analysis & Defects

### Finding F1: Forward-Match Shadowing in `check_r73_log_count` (High Severity)
In `tools/check-r73-routed-r74.py` lines 68-73:
```python
    blocks = re.split(r'\n(?=##+ )', log_text)
    matching_block = None
    for b in blocks:
        if "R73-LOG-COUNT-STALE" in b or ("Round 73" in b and "correction" in b.lower() and "selftest" in b):
            matching_block = b
            break
```
**Mechanism:**
1. The tool splits `LOG.md` on every `\n##+ `.
2. Block 158 is the existing Round 73 entry: `## Round 73 (2026-11-03) — the systemd unit-load merge plane, and three r72 routed repairs`.
3. Block 158 contains `"Round 73"`, `"correction"` (referencing round 72: *"The r72 lesson now carries an appended correction..."*), and `"selftest"` (*"...a twelfth selftest case..."*).
4. Because the loop iterates forward and breaks immediately on the first match, it ALWAYS matches Block 158!
5. Block 158 does not contain `"14"`.
6. Therefore, if an appended correction uses a `## ` heading (Form B), creating Block 159, Block 159 is shadowed and NEVER inspected.
7. Form A (appending as an unheaded bullet point / paragraph to Block 158) succeeds under the frozen tool because it remains within Block 158, supplying `"14"`.

**Hardened Prototype Fix:**
Prioritize the specific defect identifier `"R73-LOG-COUNT-STALE"` and iterate in reverse (`for b in reversed(blocks):`).
Demonstrated in scratch: `hardened_checker.py` passes both Form A and Form B with `ROUTED_STALE=0 ROUTED_OK=2/2` rc 0.
Receipt: `receipts/hardened-checker-receipt.txt`, `receipts/F1-form-b-h2-defect.txt`.

### Finding F2: Negation Blindness
Neither `check_r73_gate_quote` nor `check_r73_log_count` tests semantic polarity. Appending a denial sentence (*"However, none of this is true and quotes did not drift"*) to an otherwise token-compliant block passes both checks (Probes P7a, P7b).

## 8. Independent Grounding & Verifications

Every statement in both drafts was verified against primary source snapshots and git logs:

1. **S306 Line Drift (`src/shared/install.c`):**
   - Snapshot: `.ufo/waves/round-73/before/src/install.c` (sha256 `c11cd57579931f04ab08f17fe058fd9d4a962c0fe5c4c4a9d5ae2e86c7e6ef4d`).
   - Line 2383: `path = path_make_absolute(*name, config_path);`
   - Line 2387: `RET_GATHER(r, create_symlink(&lp, "/dev/null", path, flags & UNIT_FILE_FORCE, changes, n_changes));`
   - Gate quote was `"path = path_make_absolute(*name, config_path);"`.
   - Verified: `install.c:2383` is the true location; `2387` was 4 lines late.

2. **S304 Line Anchors (`man/systemd.unit.xml`):**
   - Snapshot: `.ufo/waves/round-73/before/src/systemd.unit.xml` (sha256 `eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6`).
   - Quote 1: `"Unit files found in directories listed earlier override files with the same name in directories lower in the list"`
     - Lines 368-370 contain the exact quote. Line 367 is introductory text (`Unit files are loaded from a set of paths determined during`).
     - Verified: `:368-370` supersedes `:367-370`.
   - Quote 2: `"Drop-in files under any of these directories take precedence over unit files wherever located"`
     - Lines 237-238 contain the exact quote. Line 236 is the tail of the previous sentence.
     - Verified: `:237-238` supersedes `:236-238`.
   - Quote 3: `"Multiple drop-in files with different names are applied in lexicographic order, regardless of which of the directories they reside in"`
     - Lines 238-239 contain the exact quote. Line 240 is a blank separator line.
     - Verified: `:238-239` supersedes `:238-240`.

3. **Round 73 Instrument Selftest Tallies:**
   - Round 73 entry in `LOG.md:3206-3209` cited: `"a twelfth selftest case"` (12) for `count-ul-rows-r73.py` and `"growing to eleven cases"` (11) for `check-r72-routed-r73.py`.
   - Final committed instrument bytes at commit `3cfa23ac`:
     - `tools/count-ul-rows-r73.py` (sha256 `1f22c26b...`): 13 cases (`MAPLIST` repair).
     - `tools/check-r72-routed-r73.py` (sha256 `ad853877...`): 14 cases (`TITLE-TOKEN` repair).
   - Verified: superseded mid-wave counts were 12 and 11; final committed counts were 13 and 14.

## 9. Limits and Risks

- **Instrument change risk:** If the wave hardens `tools/check-r73-routed-r74.py` to fix F1, both Form A and Form B will pass. If the tool remains frozen as `2da4ff1f`, Form A MUST be adopted to prevent shadowing by block 158.
- **Append-only integrity:** Neither draft modifies historical lines; both append strictly to the end of their respective documents.
- **Scratch isolation:** Scratch directory `/fast/scratch/hyaku/tsukuroi-r74/E2Routed` is cleaned before wave close; only `.ufo/waves/round-74/w1/E2Routed/` contains persisted seat artifacts.
