VERDICT: defect-found

Scope: item C3-A1, review of `tools/check-adjacency-table-r51.py` at freeze `2732ee6c06108c031c4d8043239b994e0504eb2f` (file sha256 `3d09a8e9…4cf380`, matches FROZEN-hashes.txt). Leaf seat, not counted. No lane file, index, fleet file or sibling was written. Receipts: `.ufo/waves/round-51/w1/R51RevC3/` (`counter-runs.json`, `fixtures.txt`, `R51RevC3-candidate.patch`, `check-adjacency-table-r51.candidate.py`).

## 1. Summary

The frozen counter prints PASS on inputs that contain a false displayed locator, a false displayed digest, or a non-counted extra anchor, and it reads `anchors_checker_rc` from the mutable working tree instead of the revision. Its legs are blind to duplicate rows; the override gate misses `--lane` and ambient `GIT_*` env. A candidate fix (186-line diff, §4) rejects every attack below and keeps the freeze PASS with identical leg values.

| # | Severity | Defect | Reproducer (fixture, §3) | Frozen result | Candidate result |
|---|---|---|---|---|---|
| D1 | High | Anchor rows parsed last-wins (dict); a false earlier row is never bound. The forge control misses it because its regex needs ` @ ` spacing. | fx-dupanchor2 | **PASS**, no override flag | CONTROL-FAIL (`anchor_rows_exact` 0) |
| D2 | High | Extra rows and repeated `## Adjacent — portable…` sections are not counted; `bound == 10` is a count of bound rows, not of rows. | fx-extra-row, fx-dupsection2 | **PASS** both | CONTROL-FAIL both |
| D3 | High | `digests_bound` scans the whole file and keeps the first valid line per id; a true copy elsewhere hides a false list line. | fx-digest-shadow | **PASS**, `digests_bound_ok` 10 with a wrong OUT-009 sha in the list | CONTROL-FAIL (`digests_bound_ok` 9) |
| D4 | High | Override gate (`overridden`, lines 206-207) does not see `--lane <other clone>` or ambient `GIT_*` env. Both change the bytes the counter reads. | fx-dupanchor2 with `--lane`; `GIT_DIR=/nonexistent` | measured, not `OVERRIDE-NOT-MEASURED` | exit 3 without `--control` |
| D5 | High | `anchors_checker_rc` runs `os.path.join(lane, CHECKER)` (r50 line 352): the working-tree file, not `git show REV:`. | fx-wt (freeze + WT exit 1); fx-repin + WT stub | freeze **FAIL** with a committed-good checker; fx-repin + WT stub **PASS** although the committed checker rejects the revision (rc 1) | `checker_rev_bytes` 0 → rc -2 |
| D6 | Medium | ADJ rows last-wins; `bare_ranges` is blind to a shadowed bare locator. Frozen FAIL is incidental (checker rc 1 from line-shift). | fx-dupadj2 | `bare_ranges` 0 while ADJ-07 row 1 shows `../tameshi-shokunin/PROVINCE.md:3-18` | `bare_all` 1 |
| D7 | Medium | Unnamed gap: a coordinated re-pin of OUT-009 (table + registry + digest list) to a real later revenger commit passes every counter leg; only the checker rejects it, and that checker is D5's working-tree file. | fx-repin | all counter legs 10/10/10, pins 9, live 9; only checker rc 1 | rejected (rev-bytes) |
| D8 | Low | `display_forge_fails` is the only sensitivity control; it forges only the OUT-009 commit prefix (no control for heading, quote, path, or digest list), and `hit == 1` makes duplicate-row FAILs accidental. | fx-dupsection (spaced) FAIL via `hit`=2 | — | not changed |

Frozen baseline (`base-run.json`): PASS; adj_rows 7, linked 7, bare 0, anchors_ok 7, registry_ok 7, checker rc 0, quote_at_pin 9, live 9, stub_fails 1, display_bound 10, quote_specific 10, display_forge 1, override_blocked 1, r50_blind 1, digests 10.

## 2. Answers to the audit questions (code at freeze, `git show 2732ee6:tools/check-adjacency-table-r51.py`)

- **`bound_legs` empty or 1-char prefix (lines 96-108): cannot happen.** `SIB` (r50 line 73) is `[0-9a-f]{12,40}` and `fullmatch` runs first; the `startswith` branch only runs when the match succeeds. An empty `full_commit` (registry lacks the field) gives `''.startswith(x)` = False. Checked by code and regex; no fixture run.
- **Heading dash tolerance (lines 109, 129): none.** Both comparisons are exact after `strip()`; a hyphen-for-em-dash fails closed. All ten registry headings and the displayed headings use U+2014 (checked: `\u2014`). No hyphen-variant run.
- **`quote_line` 1-based (line 127): correct.** Checked on all ten pinned blobs: `quote_line` equals the one line that contains the quote (OUT-001 9, OUT-002 12, OUT-003 3, OUT-004 6, OUT-005 8, OUT-006 3, OUT-007 12, OUT-008 3, OUT-009 3, OUT-010 7).
- **Section test (lines 129-135):** heading occurs once in each blob; section ends at the next `#`…`######` line (OUT-001 section 1-20, quote at 9; OUT-009 1-34, quote at 3; all ten contain their quote). A quote inside a fenced block would be accepted (no fence logic); none of the ten quote lines is in a fence. Not exercised.
- **`digests_bound` (lines 143-161):** the regex is strict and the list is correct at freeze (10). Defect D3: it scans every line of the file (line 150) and `seen` takes the first valid line per id (lines 152-157), so a false list line after a true copy is skipped.
- **`forged_province` (lines 190-202):** changes exactly one hex char of the first `revenger-shokunin/PROVINCE.md` @ commit cell on each OUT-009 table row, nothing else; `hit == 1` required. Correct for its purpose; see D8.
- **Override gate (lines 205-211):** `overridden` covers `--province-file`, `--registry-file`, non-default `--siblings-root`, `--skip-anchors-check`. Missed (D4): `--lane` (line 302 default is the tool's own repo; any other path is read silently), `GIT_*` env (honored: `GIT_DIR=/nonexistent` gives `base unreadable`, rc 2), and the working-tree checker (D5). `--siblings-root` is flagged; `--no-base-check` only skips an existence check.

## 3. Reproducers

Build method: `git clone -q --shared <lane> <fx>`; `git -C <fx> checkout -q --detach 2732ee6…`; assert `rev-parse --show-toplevel`; apply the edit in `PROVINCE.md` (and `corpus/knowledge/adjacency-anchors-r19.json` where stated); commit with fixture identity; `update-ref refs/heads/master <new>` and delete `refs/remotes/origin/master` (the checker needs the revision landed on master; without it rc 2 for every fixture). Run: `python3 <lane>/tools/check-adjacency-table-r51.py --revision <new> --lane <fx>`. Fixture commits are listed in `R51RevC3/fixtures.txt`; the edits:

- **fx-display** (sanity, must FAIL): OUT-009 table cell `cf02419276e5` → `df02419276e5`. Result FAIL, display_bound 9.
- **fx-dupanchor** (spaced duplicate): first OUT-009 row forged as above; true copy inserted after the OUT-010 row. Result FAIL (display_bound 10, display_forge 0 because `hit`=2). The FAIL is accidental (D8).
- **fx-dupanchor2 (D1, PASS):** insert before the OUT-009 row a copy with `cf02419276e5`→`df02419276e5` and `` `revenger-shokunin/PROVINCE.md` @ `` → `` `revenger-shokunin/PROVINCE.md`@ `` (no spaces). Result **PASS**: display_bound 10, quote_specific 10, digests 10, display_forge 1, override 1, r50_blind 1, checker rc 0. The reader sees `df02…` in the first OUT-009 row (PROVINCE.md line 129); the counter binds line 130.
- **fx-extra-row (D2, PASS):** insert after the OUT-010 row `| OUT-011 | ADJ-06 | \`revenger-shokunin/PROVINCE.md\` @ \`df02419276e5\` | …` with no registry record. Result **PASS** (bound 10 of 11).
- **fx-dupsection2 (D2, PASS):** append a second `## Adjacent — portable ownership anchors (round 19)` section with a single false OUT-009 row (no-space `@`). Result **PASS**. (The spaced variant FAILs only through `hit`=2.)
- **fx-digest-shadow (D3, PASS):** list line `- OUT-009 … sha256 63acc3…` → `sha256 73acc3…`; insert the true line `- OUT-009 \`revenger-shokunin/PROVINCE.md\` @ cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97 sha256 63acc3d0…b19f` before the `Limits (round-19` paragraph. Result **PASS**, digests_bound 10, anchors_checker_rc **0**. The real checker also accepts it: `_outbound_publication` (checker lines 417-427) uses `any(anchor_id in line and digest in line for line in region)`.
- **fx-digest-only (control, FAIL correctly):** same list edit without the shadow. digests 9, checker rc 1.
- **fx-dupadj2 (D6):** insert before the real ADJ-07 row `| ADJ-07 | bare shadow | x | x | x | \`../tameshi-shokunin/PROVINCE.md:3-18\` |`. Frozen legs: `bare_ranges` 0. Verdict FAIL is from checker rc 1 (`INBOUND-CLASSIFICATION-WRONG`, a line-number-based inbound check triggered by the inserted line), not from the bare leg.
- **fx-repin (D7):** OUT-009 re-pinned in table, digest list and registry to revenger `18200a4b18e8…` (sha256 `6c3694f9…a9b`, which has the same heading and quote at line 3; 13 other revenger commits do too). Frozen: FAIL only by checker rc 1 (`ANCHOR-SNAPSHOT-TAMPERED`; checker lines 85 and 100 hard-code the `63acc3…` blob sha). All counter legs pass.
- **fx-repin + WT stub (D5, PASS):** same fixture, with the working-tree `tools/check-adjacency-anchors.py` replaced by an uncommitted `print PASS; exit 0`. `--lane fx-repin --revision <fx>`: **PASS**, checker rc 0.
- **fx-wt (D5):** fresh clone at freeze, working-tree checker replaced by an uncommitted `exit 1`. `--lane fx-wt --revision 2732ee6…`: **FAIL**, `anchors_checker_rc` 1, although the committed checker passes at that revision (base-run rc 0).
- **GIT env (D4):** `GIT_DIR=/nonexistent python3 …check-adjacency-table-r51.py --revision 2732ee6… --lane <lane>` → `{"error": "base c0ad548… unreadable", "verdict": "FAIL"}`, rc 2: ambient git env reaches the counter's reads.

## 4. Exact replacement code (what each defect needs)

Full diff is `R51RevC3/R51RevC3-candidate.patch` (186 lines; candidate file `R51RevC3/check-adjacency-table-r51.candidate.py`). Core changes:

1. `parse_tables` returns row lists, not dicts, and reads every section headed `ANCHOR_HEAD` / `ADJ_HEAD` (`all_section_lines`). Counts are `anchor_rows_exact = sorted(ids) == OUT-001..010` and `adj_exact = sorted(ids) == ADJ-01..07`; `bare_all` counts over every ADJ row.
2. `bound_legs` iterates `enumerate(anchors)` (no `sorted(dict)`), keyed `f'{out}#{n}'`.
3. `digests_bound` reads only `digest_list_lines` (from `Portable digests` to `## ` or `Limits `) and returns 0 unless the list ids are exactly OUT-001..010.
4. `overridden` adds `os.path.abspath(a.lane) != os.path.abspath(DEFAULT_LANE)` and `any(k.startswith('GIT_') for k in os.environ)`.
5. `checker_is_rev_bytes(lane, rev)` compares `git show REV:tools/check-adjacency-anchors.py` and `tools/_revision.py` against the working-tree bytes; mismatch → `anchors_checker_rc = -2`.
6. `ok` adds `anchor_rows_exact == 1 and adj_exact == 1 and bare_all == 0`.

Candidate caveats: its `PREDICATE` string is not updated (add `and anchor_rows_exact == 1 and adj_exact == 1 and bare_all == 0`). It does not fix the checker's own `any(...)` publication test (D3's second half), so `anchors_checker_rc` still accepts a shadow digest line; that needs a change to `tools/check-adjacency-anchors.py`, which is outside this item. It does not add a registry pin for D7.

Candidate results (scratch clone detached at freeze with master set to it; receipt `counter-runs.json`, key `out-patched-freeze.json`):
- freeze: **PASS**; display 10, quote_specific 10, digests 10, display_forge 1, override 1, r50_blind 1, anchor_rows_exact 1, adj_exact 1, bare_all 0, checker_rev_bytes 1, checker rc 0.
- fx-dupanchor2 without `--control`: exit 3 `OVERRIDE-NOT-MEASURED`. With `--control`: CONTROL-FAIL (anchor_rows_exact 0, quote_specific 11).
- fx-extra-row, fx-dupsection2: CONTROL-FAIL (anchor_rows_exact 0).
- fx-digest-shadow, fx-digest-only: CONTROL-FAIL (digests 9).
- fx-dupadj2: CONTROL-FAIL (adj_exact 0, bare_all 1).
- fx-display: CONTROL-FAIL (display 9).
- fx-repin + WT stub: CONTROL-FAIL (checker_rev_bytes 0, rc -2).

Note: the candidate changes a FROZEN counter (sha in FROZEN-hashes.txt). Whether an amendment to that file is allowed before w2 is the planner's decision; I did not assume it.

## 5. Not run / limits

- Not run: a hyphen-variant heading, a fenced-block quote, a `--siblings-root` symlink, `--no-base-check` variations, the C2 scorer, the battery (`controls/battery.py`), and `check-adjacency-table-r51.py --control` on the frozen controls. The candidate is not in the lane and was not run through the battery.
- The candidate was not run with the committed checker on fx-repin (it fails there regardless).
- Byte-level claims are for the freeze bytes only (`git show 2732ee6…`).
- The lane's working tree was not read as evidence (only `git show` and the scratch clone).

## 6. Hand-off to L1

- Apply D1-D5 in the amendment: the candidate patch covers them in the counter. D6 is covered by `bare_all`. D7 needs a registry or checker decision (for example, the counter asserting OUT-001..010 `sibling_commit`/`sibling_blob_sha256` against a constant or the BASE registry). D8 needs new controls (heading, quote, digest-list forgery), not a code change to the existing one.
- Checks to run once after landing: the frozen battery `controls/battery.py`, `check-adjacency-table-r51.py --revision <amended>` (must PASS on the real lane), and the fixture set in §3 (each must FAIL, except the freeze).
- Installs: none. Scratch `/fast/scratch/hyaku/tsukuroi-r51/R51RevC3/` removed after the receipts were copied.
