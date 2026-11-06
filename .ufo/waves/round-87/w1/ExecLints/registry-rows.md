# Draft registry rows for the two round-87 tools (ExecLints, round 87 w1)

Status: DRAFT. Not landed. `tools/check-registry-coverage.py` reads the highest-numbered
`## Gate and probe registry — round<N> superseding current rows` heading; at the measured tip
(`cefb4188b484329c4908a19a277f8fb120fb4f56`) that is `SKILL.md:5777` (`round71`), whose table
runs `SKILL.md:5785` (header) … `SKILL.md:5922` (last row, `nonauthor-label`). The round-72…86
rows are appended to that same table; the `## Round-76 instrument registry (append-only
continuation)` table at `SKILL.md:6013` is explicitly NON-OPERATIVE and the `## Gate and probe
registry — round 77 addition` heading at `SKILL.md:6127` does not match the parser's regex
(`round([0-9]+)` with no space), so neither is read.

## Where they go

Insert both rows immediately after `SKILL.md:5922` (`| nonauthor-label | gate | …`)
and **before** the blank line at `SKILL.md:5923`. A blank line ends the table for the parser
(`tools/check-registry-coverage.py:_operative_rows` breaks at the first non-blank-less line), so
a row separated by a blank line is invisible and the two `REGISTRY-ROW-MISSING` findings stay.

## The rows (verbatim, 8 columns, same format as `resume-gate-battery-r86` / `hibernate-resume`)

| limine-pins | gate | `python3 tools/check-limine-pins.py --conf <FILE> --esp <DIR> [--secure-boot-enforced {0,1}]` (or `--live`; not live-run round87) | 0 HEALTHY; 1 DEGRADED (any LP-MISMATCH, LP-MISSING or LP-HASH-FORMAT pin); 2 CANNOT-EVALUATE (conf unreadable, or any LP-UNRESOLVED pin); 64 usage | `python3 tools/check-limine-pins.py --selftest` (14 fixtures, asserting rc and the sorted per-pin (line, status, consequence); exit 0 PASS / 1 FAIL) | Limine v12.9.4 rule set R1-R7 frozen in the `limine-pin-battery-r87` docstring; sources S350-S353; pin keys path, kernel_path, image_path, module_path, dtb_path, global_dtb, wallpaper, term_font; BLAKE2b-512 over the raw stored bytes, gzip not decompressed | read-only: conf and ESP files opened read-only; selftest private mkdtemp under `$TMPDIR`; never writes `/boot` | tsukuroi |
| limine-pin-battery-r87 | gate | `python3 tools/limine-pin-battery-r87.py --gate <PATH> [--runs <N>] [--work <DIR>] [--json <FILE>]` | 0 met (22 of 22 families); 1 unmet; 2 usage/could-not-evaluate (no `--gate`) | `python3 tools/limine-pin-battery-r87.py --selftest` (5 cases: absent, constant-HEALTHY, non-JSON and constant-DEGRADED gates at 0/22 plus a reference gate at 22/22, asserting battery rc and the failed-family set) | Round-87 C1 instrument sha256 `f2551c8e8386d599e3c2aca8888d5fbb0351a5a399dc43dc448556e99361989d` in `.ufo/waves/round-87/before/freeze-manifest.sha256`; rule set R1-R7 in its docstring; fixtures generated fresh per run with OS-entropy names, bytes and layouts, case list shuffled per run | fixtures under `--work` (default `$TMPDIR`), removed before exit; reads the gate path and its own fixtures only | tsukuroi |

## Why each cell reads what it reads

- One row per tool. The parser raises `REGISTRY-ROW-AMBIGUOUS` when a row's Entry-command or
  Self-test cell names two committed `tools/` files, so the gate row names only
  `tools/check-limine-pins.py` and the battery row only `tools/limine-pin-battery-r87.py`. The
  cross-reference to the battery in the gate row lives in the Pinned-values cell, which the
  parser does not scan for paths.
- Gate rows must publish all three verdict codes (`REGISTRY-VERDICT-INCOMPLETE`); both rows carry
  a literal `0`, `1` and `2`.
- `--selftest` must appear literally in the named tool (`REGISTRY-SELFTEST-UNRESOLVED`); it does
  in both (`tools/check-limine-pins.py:225`, `tools/limine-pin-battery-r87.py:592`).
- Verdict maps are the tools' own documented exit contracts, not new claims: gate docstring
  `tools/check-limine-pins.py:20-22` (`Exit: 0 HEALTHY; 1 DEGRADED …; 2 CANNOT-EVALUATE …; 64
  usage`) and battery docstring `tools/limine-pin-battery-r87.py:55-56` (`Exit: 0 met; 1 unmet;
  2 usage/could-not-evaluate`).
- Selftest figures are measured at the tip, not copied from a claim: `selftest PASS 14/14` rc 0
  and `selftest PASS 5/5` rc 0 (`receipts/04-selftests.txt`). The gate's 14 fixture names are
  `ok, upper, mismatch-panic, mismatch-prompt, first-setting, secureboot, comment, missing,
  format, unresolved, wallpaper-skip, non-path-key, crlf-blanks, conf-absent`.
- `{0,1}` is written instead of `0|1` so the cell carries no pipe; the parser's `_split_table_row`
  would keep an escaped `\|` intact, but an unescaped `|` would split the row.

## Verification (fixture only, lane untouched)

A `git clone --shared` of the lane at master, the two rows appended after the `nonauthor-label`
row, one fixture commit on a local branch `fixture-rows`:

```
$ python3 tools/check-registry-coverage.py --revision 4d11e4cd29b0c07453236a06ee2a101eb427ac7a --branch fixture-rows
{"branch":"fixture-rows","branch_tip":"4d11e4cd29b0c07453236a06ee2a101eb427ac7a","counts":{"findings":0,"missing":0,"registered":138,"rows_total":138,"tools_total":138},"findings":[],"revision":"4d11e4cd29b0c07453236a06ee2a101eb427ac7a","status":"PASS"}
RC=0

$ git diff --stat cefb4188b484329c4908a19a277f8fb120fb4f56..HEAD
 SKILL.md | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
```

Baseline at the same tip without the rows: `registered 136 / tools_total 138`, two
`REGISTRY-ROW-MISSING` findings, rc 1 (`receipts/01-registry-coverage.txt`). The fixture delta is
exactly `SKILL.md` +2 rows −1 blank line; no other file changed.

First attempt inserted the rows *after* the blank line and the gate still read 136/138 with both
findings — recorded here because that is the failure mode a landing seat will hit if it appends
at the end of the section instead of at the end of the table.
