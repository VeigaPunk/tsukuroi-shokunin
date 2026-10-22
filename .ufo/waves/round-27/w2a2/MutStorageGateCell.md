# MutStorageGateCell — mutation test of the round-27 Gate-cell parsing fix

Verdict: partly holds. 14 mutants on `tools/check-storage-health.py` (the round-27
fix, commit 4c487fc9) were run against the selftest (44 cases) and the revision
counter at `099c7b3f42d073203d9448807860f04c175eccd7`. 11 mutants were killed and
3 survived.  Two of the three survivors are real behavioural gaps in the round-27
selftest additions (`gate-cell-unquoted` and `gate-cell-backticks` do not pin what
they claim to pin); the third survivor, M13, is provably equivalent to the pristine
code and is not a defect.  No lane byte was modified; the mutated tool file was
restored byte-for-byte and its sha256 equals the lane commit blob.

## Scope and method

Target file: `tools/check-storage-health.py` at revision
`099c7b3f42d073203d9448807860f04c175eccd7`, functions `cell_quotes` (line 204),
`cell_spans` (line 150), `quoted_spans` (line 188), `straight_quote_spans`
(line 170) and `extract_quote` (line 140).

The lane was never written to.  The pristine tree was exported read-only with
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive
099c7b3f42d073203d9448807860f04c175eccd7 | tar -x -C
/fast/scratch/hyaku/tsuku27a2/MutStorageGateCell/tree`.  Each mutant was applied to
a private copy at `/fast/scratch/hyaku/tsuku27a2/MutStorageGateCell/work/tools/check-storage-health.py`.

Detectors, run on pristine bytes, on each mutant, and again on the restored bytes:

- D1 selftest: `python3 tools/check-storage-health.py --selftest` — 44 hermetic cases.
- D2 revision: `python3 tools/check-storage-health.py --revision
  099c7b3f42d073203d9448807860f04c175eccd7 --repo
  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin` — the tool reads the lane
  through git only; the mutated file lives in the scratch tree and is the code
  under test.

Baseline (pristine bytes): D1 `PASS`, 44 cases, 0 failed, exit 0; D2 `PASS`,
`verified_rows` 6, exit 0, no findings.  Tool file sha256
`6d19189df9cc4a63d8ec182c6075e9d4ccb68b71e75f0e700f917858ff502319`.

A mutant counts as killed when either detector changes its baseline verdict.
After the battery, the working copy was restored and re-measured: sha256
`6d19189df9cc4a63d8ec182c6075e9d4ccb68b71e75f0e700f917858ff502319`, D1 `PASS`
44/0 exit 0, D2 `PASS` 6 exit 0 — byte-identical to the export, to the lane
commit blob (`git show 099c7b3f:tools/check-storage-health.py`, same sha256) and
to the lane working-tree file.  Driver: `/fast/scratch/hyaku/tsuku27a2/MutStorageGateCell/mutate.py`;
machine-readable log: `/fast/scratch/hyaku/tsuku27a2/MutStorageGateCell/mutants.json`.

## Findings

1. **Killed — M01, keep the empty leading cell: `cell_quotes` drops the leading-cell
   adjustment.** The round-27 block `if line.lstrip().startswith('|'): spans = spans[1:]`
   (`tools/check-storage-health.py:214-216`) was deleted, so the header-derived
   column index lands one cell to the left and the quote is read from the `Opened`
   column. D1: exit 1, 36 of 44 cases fail, including `clean-pass`,
   `gate-quote-missing`, `gate-cell-unquoted`, `gate-cell-backticks` and
   `gate-quote-in-location-cell`. D2: exit 1, `verified_rows` 0, finding
   `SH-GATE-QUOTE-MISSING`. Mutated sha256
   `909f0b5fe06cd8f437a734314301cbaa9a9204620dce5574b356817f230544a3`.

2. **Killed — M02, keep the empty leading cell: `split_cells` stops stripping the
   leading pipe** (`tools/check-storage-health.py:104`). The header index then
   counts the empty leading cell while the raw spans still drop it, so the two
   sides disagree by one column. D1: exit 1, 37 of 44 cases fail. D2: exit 1,
   `verified_rows` 0, eight blocking findings
   (`SH-GATE-QUOTE-MISSING`, `SH-GATE-LINE-MALFORMED`, `SH-SKILL-ROW-MISSING`,
   `SH-SNAPSHOT-DIGEST-NOT-IN-ANCHOR`, `SH-SOURCE-OPENED-WRONG`,
   `SH-SOURCE-STATUS-NOT-MINED`, `SH-SOURCE-TIER-MISSING`,
   `SH-SOURCE-USED-BY-MISSING`). Mutated sha256
   `03a6b383dff4728663719fa6fb84a4be73c5fb5b110facc121f1687ad2611198`.

3. **Survived — M03, read a fixed column index.** `cell_quotes` was made to ignore
   the header-derived `quote_col` and always read the fourth cell
   (`quote_col = 3` inserted before `tools/check-storage-health.py:217`). D1: exit 0,
   0 failed of 44. D2: exit 0, `verified_rows` 6, no findings. Mutated sha256
   `72a972ce9a4df42bdd969246cef5850f573bac02de5f8202eb142984f9928bc0`.
   **This is a real coverage gap, not an equivalent mutant.** The missing case is a
   Gate table whose `Located quote` column is not the fourth one. Demonstrated at
   `/fast/scratch/hyaku/tsuku27a2/MutStorageGateCell/missing_cases.py` with the
   lesson header `| Source | Located quote (at most 25 words) | URL | Opened | Location |`:
   pristine gives `exit=0 verified_rows=6 findings=[]`, M03 gives
   `exit=1 verified_rows=0 findings=['SH-GATE-QUOTE-MISSING']`. The same holds for
   the header `| Source | quote | URL | Opened | Location |`. Every Gate table in
   the selftest and in the lane lesson puts the quote column fourth, so the fixed
   index is indistinguishable from the header lookup. [inf] The header-name lookup
   in `gate_quotes` (`tools/check-storage-health.py:350-351`) is therefore not
   covered by any case: the selftest only ever exercises the column position, not
   the name.

4. **Killed — M04, require a quoted cell: the plain-text fallback is removed.**
   `tools/check-storage-health.py:224-225` (`return [extract_quote(text)] if text
   else []`) was replaced by `return []`, so a Gate cell with no quote mark yields
   no located quote. D1: exit 1, exactly one case fails, `gate-cell-unquoted` —
   the round-27 QUALITY 64 case that was added for this behaviour. D2: exit 0,
   `verified_rows` 6. Mutated sha256
   `cf7be80d9615d86fb6c8e21912c1a840d12336d2ada398103544e92cea8eafc7`.

5. **Killed — M05, accept a quote that starts outside the quote cell.** The bound
   `if start <= span_start < end` (`tools/check-storage-health.py:221`) was relaxed
   to `if span_start >= start`, so a quote that begins in a later cell is read as
   the located quote. D1: exit 1, exactly one case fails,
   `gate-quote-in-location-cell` — the other round-27 QUALITY 64 case. D2: exit 0,
   `verified_rows` 6. Mutated sha256
   `c49b85a11bcd9080f25eec95f7265e37ebf1948583d56741cab2d75c577eda15`.

6. **Survived — M06, strip quotes twice.** `extract_quote`
   (`tools/check-storage-health.py:146`) was changed to
   `return match.group(1).strip().strip('"')`. D1: exit 0, 0 failed of 44. D2:
   exit 0, `verified_rows` 6, no findings. Mutated sha256
   `944a39d6fe22571faf13feccae7015118e742b39f8c64fa4ffc2920343aa4b11`.
   **This is a real coverage gap.** The difference is observable only when the
   extracted group itself begins or ends with a double-quote character, which the
   backtick pattern can produce: `extract_quote('`"alpha"`')` returns `'"alpha"'`
   under the pristine code and `'alpha'` under M06
   (`/fast/scratch/hyaku/tsuku27a2/MutStorageGateCell/probe.py`). The missing case
   is a Gate cell whose quote text is itself a double-quoted string. Demonstrated
   at `/fast/scratch/hyaku/tsuku27a2/MutStorageGateCell/missing_cases.py` with
   entry quote text `` `the marker is `"alpha"` here` `` and Gate cell `"alpha"`:
   pristine gives `exit=1 verified_rows=5 findings=['SH-GATE-QUOTE-MISSING']`,
   M06 gives `exit=0 verified_rows=6 findings=[]`. The mutant is the *more
   permissive* one here, so a Gate cell and an entry quote that differ only in
   redundant quoting are silently reconciled instead of reported.

7. **Killed — M07, strip quotes twice: `straight_quote_spans` strips one character
   too many at each end** (`text[start + 1:end]` became `text[start + 2:end - 1]`
   at `tools/check-storage-health.py:186`). D1: exit 1, 36 of 44 cases fail. D2:
   exit 1, `verified_rows` 0, finding `SH-GATE-QUOTE-MISSING`. Mutated sha256
   `79f9ff0a8a729d63748b29050af91f00e886bebd910a3eb1ae6956aa8b2adb02`.

8. **Killed — M08, drop backtick handling: the backtick span scan and the
   backtick pattern of `extract_quote` are both removed**
   (`tools/check-storage-health.py:196-197` and `:145`). D1: exit 0, 0 failed of
   44 — **the selftest does not detect this at all**. D2: exit 1,
   `verified_rows` 5, row `SH5` fails with `SH-GATE-QUOTE-MISSING` on source
   `S134`. Mutated sha256
   `66db0ac1d969cf65120de36e03a850fc99e4cf0a0ea44949332c1366a693aa6b`.
   The real lesson row `| S134 | … | `(!w ? "PASSED" : "FAILED!"));` | … |`
   (`corpus/lessons/round-26.md:33`) is what kills it: without backticks the
   straight-quote scan returns `PASSED" : "FAILED!` instead of the whole span.

9. **Killed — M09, drop backtick handling: only the backtick span scan of
   `quoted_spans` is removed** (`tools/check-storage-health.py:196-197`); the
   backtick pattern of `extract_quote` is kept. D1: exit 0, 0 failed of 44 — again
   **not detected by the selftest**. D2: exit 1, `verified_rows` 5, row `SH5`
   fails with `SH-GATE-QUOTE-MISSING` on source `S134`. Mutated sha256
   `726f543b97ac7ac24b333a41365a622106537dfd936e289c73f5affd0c9b837b`.

10. **Killed — M10, keep the empty leading cell: the index bound is off by one**
    (`quote_col >= len(spans)` became `quote_col > len(spans)` at
    `tools/check-storage-health.py:217`). D1: exit 1, two cases fail,
    `gate-row-malformed` and `lesson-prose-line-replaces-gate-row`; the mutant
    raises `IndexError: list index out of range` on the short row
    `| S129 | https://example.invalid/S129 |`, which is caught by the selftest
    harness and scored as a failed case. D2: exit 0, `verified_rows` 6. Mutated
    sha256 `d7d5f1d89d8d6b04afaf5bf02ae3b97fb58e73a52fcbe80c1bcab2917854eb4a`.

11. **Killed — M11, keep the empty leading cell: two cells are dropped instead of
    one** (`spans = spans[2:]`, `tools/check-storage-health.py:216`). D1: exit 1,
    36 of 44 cases fail. D2: exit 1, `verified_rows` 0, finding
    `SH-GATE-QUOTE-MISSING`. Mutated sha256
    `d57e7d972411cc459ba0cc73db749e9a05307fa424f925141366ce65d400acb8`.

12. **Killed — M12, keep the empty leading cell: the leading-pipe guard is
    dropped** and the first cell is removed unconditionally
    (`tools/check-storage-health.py:214-216`). D1: exit 1, 36 of 44 cases fail.
    D2: exit 1, `verified_rows` 0, finding `SH-GATE-QUOTE-MISSING`. Mutated
    sha256 `d89e008b8226579f02f1f23f0b1599e4543e6315fbe796b7e46782a683618e44`.
    [obs] The guard is dead weight for the fixture and the lane lesson, because
    every Gate row starts with a pipe; the mutant is killed only because the
    dropped cell shifts the columns of every row, not because of the guard itself.

13. **Survived — M13, accept a quote that starts outside the quote cell: the bound
    is inclusive at the end** (`if start <= span_start <= end`,
    `tools/check-storage-health.py:221`). D1: exit 0, 0 failed of 44. D2: exit 0,
    `verified_rows` 6. Mutated sha256
    `211195239a5c5094753c5789b435a3da6a194952bcaec4a237b78abe7f58ac0b`.
    **This mutant is equivalent to the pristine code, not a defect.** The cell end
    index of a span is always the index of the terminating `|` or the end of the
    line, and a quoted span always starts at a `"` or a backtick, so
    `span_start == end` cannot occur. Verified by exhaustive enumeration over
    every line of length 1 to 6 drawn from the alphabet `` | ` " a  space ``
    (279,930 line/column combinations) and by 400,000 random lines: zero
    behavioural differences. The two structural invariants were checked over 80,000
    random lines and held without exception (cell end index not at a pipe: 0;
    quoted-span start index not at a quote character: 0).

14. **Killed — M14, require a quoted cell: the quoted span must lie wholly inside
    the quote cell** (`tools/check-storage-health.py:220-221`, adding
    `and span_end <= end`). D1: exit 1, exactly one case fails,
    `gate-quote-with-pipe` — the quote that contains a pipe is no longer read
    whole. D2: exit 0, `verified_rows` 6. Mutated sha256
    `c3eb3c7fc0a65f44f7c8b2d978e9c4f837a2158b50abed4cfa844d36c48f0000`.

## Coverage findings for the round-27 selftest additions

15. **The two round-27 QUALITY 64 cases do not cover what their names claim.**
    `gate-cell-unquoted` and `gate-cell-backticks` were added in commit 4c487fc9
    (`tools/check-storage-health.py:1279-1295`) to cover an unquoted cell and a
    backticked cell. M04 (remove the plain-text fallback) and M05 (accept a quote
    from a later cell) are killed by exactly these two cases, so they do have
    discriminating power. M08 and M09 (drop backtick handling) are **not** killed by
    any of the 44 cases; only the lane revision run catches them. The reason is
    that the round-27 backtick case uses the plain fixture quote, which contains
    no double quote character, so a backtick-blind parser and a backtick-aware one
    return the same text. Demonstrated at
    `/fast/scratch/hyaku/tsuku27a2/MutStorageGateCell/backtick_gap.py`: with the
    existing case shape (`Gate cell = `the btrfs device error counters are
    cumulative per device``) pristine, M08 and M09 all give
    `exit=0 rows=6 findings=[]`; with the cell
    `` `(!w ? "PASSED" : "FAILED!"));` `` (the shape the real `S134` row uses)
    pristine gives `exit=0 rows=6 findings=[]` while M08 and M09 give
    `exit=1 rows=5 findings=['SH-GATE-QUOTE-MISSING']`. [inf] A backtick case whose
    content carries an inner double quote would close this gap; the lane lesson
    already contains such a row at `corpus/lessons/round-26.md:33`.

16. **Two further coverage gaps, both in the same area.** M03 (fixed column index)
    is undetected because no case moves the `Located quote` column away from the
    fourth position, so the header-name lookup in `gate_quotes`
    (`tools/check-storage-health.py:350-351`) is never exercised as a lookup. M06
    (strip quotes twice) is undetected because no case carries a located quote
    whose text is itself a double-quoted string. [inf] Both are additions to the
    round-27 selftest, not changes to the contract; the contract itself is not in
    question, and the surviving mutants are reported as coverage findings for the
    L1 to decide on.

## Restoration evidence

- Export, working copy after restore, and the lane commit blob all hash to
  `6d19189df9cc4a63d8ec182c6075e9d4ccb68b71e75f0e700f917858ff502319`; the three
  byte strings compare equal.
- The lane working-tree file `tools/check-storage-health.py` hashes to the same
  value, so nothing in the lane was touched.
- Post-restore re-measurement: selftest `PASS` 44 cases 0 failed exit 0; revision
  `PASS` `verified_rows` 6 exit 0 — identical to the baseline.
- `git status --porcelain` in the lane shows only the L1's own modified files and
  the wave-2 seat reports; the storage checker is not among them.
- All mutant files, logs and probes live under
  `/fast/scratch/hyaku/tsuku27a2/MutStorageGateCell/` and
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/MutStorageGateCell.md`.

Scope: read=lane revision 099c7b3f42d073203d9448807860f04c175eccd7 (tools/check-storage-health.py, corpus/lessons/round-26.md, corpus/knowledge/storage-health-r26.json, commit 4c487fc9 diff, SCORECARD.md not read); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/MutStorageGateCell.md, /fast/scratch/hyaku/tsuku27a2/MutStorageGateCell/{mutate.py,probe.py,missing_cases.py,backtick_gap.py,mutants.json,tree/,work/,mutant-src/,mutrun/}; executed=git archive|tar export, 14 mutant applications with --selftest and --revision each (pristine baseline, per-mutant, post-restore), exhaustive and random equivalence probes, python3 unit-level probes of cell_quotes/extract_quote/gate_quotes, git status/sha256 verification. No pacman, uv or other install was needed; no package was installed or updated.
Model: not exposed
Installs: none
