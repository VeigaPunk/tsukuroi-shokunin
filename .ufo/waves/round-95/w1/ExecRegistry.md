# ExecRegistry — round-95 wave w1 (C2 operability)

Seat: `ExecRegistry` (executor). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Judged axis: **operability** (C2). The three axes this seat walked: (1) the lane's own registry gate is
green at the landed revision and at the branch tip; (2) each of the four new registry rows is honest
(its path resolves, it names one tool, its content claims hold); (3) attack coverage — which of the
gate's checks a new row can fail that a PASS run does not exercise, and which dishonest rows still pass.
Moves kept: three gate runs, the four-row inspection, three tool selftests, ten attack fixtures; no lane
file was written outside `.ufo/waves/round-95/w1/ExecRegistry/`.

Lane state at measurement: `git rev-parse --show-toplevel` → the lane root; `git rev-parse master` →
`884ed06bdc7681ad73e757cf8a02bee21de2c480`. All git commands below are read-only
(`rev-parse`, `show`, `ls-tree`, `log`, `diff`).

## 1. Item 1 — pre-round tip must read FAIL

```
$ python3 tools/check-registry-coverage.py --revision c0a20cef641ada6feeab1ca107ea62c1848d1da0
rc=1
{"branch":"master","branch_tip":"884ed06bdc7681ad73e757cf8a02bee21de2c480","counts":{"findings":2,"missing":2,"registered":147,"rows_total":147,"tools_total":149},"findings":[{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/limine-pin-battery-r94.py"},{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/make-r94-bends.py"}],"revision":"c0a20cef641ada6feeab1ca107ea62c1848d1da0","status":"FAIL"}
```

| expected | observed | verdict |
|---|---|---|
| `status` FAIL | FAIL | PASS |
| `findings` 2 | 2 | PASS |
| `missing` 2 | 2 | PASS |
| `tools_total` 149 | 149 | PASS |
| `registered` 147 | 147 | PASS |
| the two findings are the r94 tools | `tools/limine-pin-battery-r94.py`, `tools/make-r94-bends.py` | PASS |

Receipt: `w1/ExecRegistry/c0a20cef-registry.json` (stderr empty).

## 2. Item 2 — landed revision and branch tip must read PASS

```
$ python3 tools/check-registry-coverage.py --revision b66e6be5cf3506aff427c3c4fd59deaa8f45d0ca
rc=0
{"branch":"master","branch_tip":"884ed06bdc7681ad73e757cf8a02bee21de2c480","counts":{"findings":0,"missing":0,"registered":151,"rows_total":151,"tools_total":151},"findings":[],"revision":"b66e6be5cf3506aff427c3c4fd59deaa8f45d0ca","status":"PASS"}

$ git rev-parse master
884ed06bdc7681ad73e757cf8a02bee21de2c480
$ python3 tools/check-registry-coverage.py --revision $(git rev-parse master)
rc=0
{"branch":"master","branch_tip":"884ed06bdc7681ad73e757cf8a02bee21de2c480","counts":{"findings":0,"missing":0,"registered":151,"rows_total":151,"tools_total":151},"findings":[],"revision":"884ed06bdc7681ad73e757cf8a02bee21de2c480","status":"PASS"}
```

**The branch tip has moved** past the landed revision given in the item: `884ed06b` is one commit on top
of `b66e6be5` (`git log --oneline b66e6be5..884ed06b` → `884ed06b round-95: wave w1 dispatch (13 seats)
+ C2 receipts + freeze A2`). **The numbers do not differ**: both revisions read PASS, findings 0,
missing 0, tools_total 151, registered 151. The moved commit touches only `.ufo/` files:
`git diff --stat b66e6be5..884ed06b` lists 11 files, none under `tools/` and not `SKILL.md`
(`SKILL.md` sha256 `40602afb67cba5fdd1d6ff1043ed5ae4343d86c7c12253d9b822734e659e47d0` at both revisions;
at the pre-round `c0a20cef` it was `97291755208a99abc937228c59b572fc2dbd86078f6d4b5280e8e65deb61695d`).

| expected | observed at `b66e6be5` | observed at tip `884ed06b` | verdict |
|---|---|---|---|
| `status` PASS | PASS | PASS | PASS |
| `findings` 0 | 0 | 0 | PASS |
| `missing` 0 | 0 | 0 | PASS |
| `tools_total` 151 | 151 | 151 | PASS |
| `registered` 151 | 151 | 151 | PASS |

Receipts: `w1/ExecRegistry/b66e6be5-registry.json`, `w1/ExecRegistry/tip-registry.json`,
`w1/ExecRegistry/git-facts.txt`.

## 3. Item 3 — the gate's own selftest

```
$ python3 tools/check-registry-coverage.py --selftest
rc=0
PASS (23 cases, 23 passed, 0 failed)
```

Expected `PASS (23 cases, 23 passed, 0 failed)` — matched. The 23 cases cover clean, missing-row,
duplicate-row, ambiguous-row, orphan-row, invalid-kind, unresolved-selftest, incomplete-verdict,
unique-highest-table, duplicate-highest, no-table, baseline-split, bad-revision and 10
audit-live-map cases (`tools/check-registry-coverage.py:508-746`).
Receipt: `w1/ExecRegistry/selftest.txt`.

## 4. Item 4 — the four new rows at the landed revision

```
$ git show b66e6be5cf3506aff427c3c4fd59deaa8f45d0ca:SKILL.md | grep -n 'limine-pin-battery-r9[45]\|make-r9[45]-bends'
5934:| limine-pin-battery-r94 | gate | `python3 tools/limine-pin-battery-r94.py ...`
5935:| make-r94-bends | gate | `python3 tools/make-r94-bends.py` | ...
5936:| limine-pin-battery-r95 | gate | `python3 tools/limine-pin-battery-r95.py ...`
5937:| make-r95-bends | gate | `python3 tools/make-r95-bends.py` | ...
```

Each row was re-parsed with the gate's own `_operative_rows` / `_paths` / `SELFTEST_FLAG` functions
(`rows-inspect.json`), and each named path was resolved with `git ls-tree` at `b66e6be5`:

| row (line) | kind | `tools/` paths in entry ∪ self-test | all cells | `git ls-tree -r` | verdict |
|---|---|---|---|---|---|
| `limine-pin-battery-r94` (5934) | gate | exactly 1: `tools/limine-pin-battery-r94.py` | 1 | `100755 blob 31688e7f… tools/limine-pin-battery-r94.py` | PASS |
| `make-r94-bends` (5935) | gate | exactly 1: `tools/make-r94-bends.py` | 1 | `100644 blob 9dec104f… tools/make-r94-bends.py` | PASS |
| `limine-pin-battery-r95` (5936) | gate | exactly 1: `tools/limine-pin-battery-r95.py` | 1 | `100755 blob dd943287… tools/limine-pin-battery-r95.py` | PASS |
| `make-r95-bends` (5937) | gate | exactly 1: `tools/make-r95-bends.py` | 1 | `100755 blob 4162d6b2… tools/make-r95-bends.py` | PASS |

- Every path is a committed **regular blob** (mode `100644`/`100755`; the gate's own `tool_files` filter
  accepts only those two modes, and it found all four).
- Every row names **exactly one** committed `tools/` path, so no `REGISTRY-ROW-AMBIGUOUS` can fire
  (the rule counts `entry_paths | self_paths` intersected with the committed tool set).
- The two battery rows carry a `--selftest`-shaped flag in the self-test cell; that flag resolves in the
  named tool's source (the gate reports `findings: []`; the typo counter-test in §6 fires the same check,
  proving it is live). The two `make-*-bends` rows carry no flag-shaped token at all, so the gate checks
  nothing in their self-test cell (see §6, H4).
- Cells are identical at the tip (`rows-inspect.json` second object, revision `884ed06b`).

Receipts: `w1/ExecRegistry/rows-grep.txt`, `w1/ExecRegistry/rows-inspect.json`,
`w1/ExecRegistry/git-facts.txt`.

## 5. Item 5 — the `limine-pins` row at the landed revision

Row at `SKILL.md:5923` (identical at the tip):

```
$ git show b66e6be5…:SKILL.md | sed -n '5923p' | grep -o 'default `auto`\|default `12.9.4`\|(39 fixtures'
default `auto`
(39 fixtures
$ git show b66e6be5…:SKILL.md | sed -n '5923p' | grep -c '12\.9\.4'
0
$ git show b66e6be5…:SKILL.md | sed -n '5923p' | grep -o '.\{0,60\}37.\{0,60\}'
_version`/`visibility_era`; sources S350-S353, S361, S362, S374-S376, S379, S380 (S381 community lead only) | read-only ov
```

| expected | observed | verdict |
|---|---|---|
| contains ``default `auto` `` | entry cell: ``(default `auto`, the installed-version probe since r94/V4 …`` | PASS |
| contains `(39 fixtures` | self-test cell: `python3 tools/check-limine-pins.py --selftest` (39 fixtures, asserting rc, …) | PASS |
| does not contain ``default `12.9.4` `` | `12.9.4` occurs 0 times in the row | PASS |
| no 37-case selftest named | the only `37` is the source range `S374-S376`; no `37 fixtures` / `37 cases` | PASS |

The tally claim is corroborated by execution, not only by the string:

```
$ TMPDIR=<scratch>/tmp python3 tools/check-limine-pins.py --selftest
rc=0
... 39 fixture lines, each PASS ...
selftest PASS 39/39
```

Receipts: `w1/ExecRegistry/git-facts.txt`, `w1/ExecRegistry/limine-pins-selftest.txt`.

## 6. Item 6 — attack: checks the PASS run does not exercise, and what slips through

Read of `tools/check-registry-coverage.py` (754 lines; unchanged across `c0a20cef`, `b66e6be5`,
`884ed06b` — sha256 `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812`). The checks are
`REGISTRY-KIND-INVALID`, `REGISTRY-ROW-AMBIGUOUS`, `REGISTRY-VERDICT-INCOMPLETE`, `REGISTRY-ROW-ORPHAN`,
`REGISTRY-SELFTEST-UNRESOLVED`, `REGISTRY-ROW-MISSING`, `REGISTRY-ROW-DUPLICATE`,
`REGISTRY-AUDIT-LIVE-MAP` (only with `--audit-live-map`), plus `E-REGISTRY-TABLE` / `E-REVISION-INVALID`.
A PASS run exercises none of the negatives; each was driven in a throwaway fixture repo in scratch
(`git init` in the fixture, `git rev-parse --show-toplevel` asserted to be the fixture before commit;
the lane was only read). Fixtures embed a copy of the gate itself, so the results are the gate's own
verdicts.

| fixture | mutation | gate result | what it shows |
|---|---|---|---|
| `swap` | two rows exchange entry paths (`alpha`→`tools/beta.py`, `beta`→`tools/alpha.py`) | **PASS** | no check binds a row's Name to its path |
| `real-swap` | **the real 151-row table**, with the r94/r95 battery rows' entry+self-test cells exchanged (lines 5934↔5936) | **PASS**, 151/151 | the production table can be swapped between the two batteries and still read green |
| `phantom-content` | row claims `--selftest` (mention only, in a comment) with `(40 fixtures, every one passes)`, `default \`12.9.4\``, write scope `writes /etc and /boot` | **PASS** | cell content is not verified; the flag check is a source-substring search |
| `real-content-lie` | **the real table**, `limine-pins` cells changed `default \`auto\``→`default \`12.9.4\`` and `(39 fixtures`→`(88 fixtures` | **PASS**, 151/151 | the two cells C2 certifies are **not** gate-verified; my grep + the 39/39 selftest are the only certifiers |
| `library-bypass` | tool row with `kind = library`, verdict `n/a` | **PASS** | `library` rows are exempt from `REGISTRY-VERDICT-INCOMPLETE` |
| `gate-verdict-required` | same row with `kind = gate`, verdict `n/a` | FAIL `REGISTRY-VERDICT-INCOMPLETE` | the verdict check is live (negative control) |
| `bare-digit-verdict` | gate row, verdict cell `0 1 2` | **PASS** | the check is a bare-digit search, not a mapping check |
| `incidental-one` | gate row, verdict cell `0 2 (the 1 case is untested)` | **PASS** | an incidental `1` satisfies the "gate publishes 1" rule |
| `real-selftest-flag-typo` | real table, r95 battery self-test flag `--selftest`→`--selftest-all` | FAIL `REGISTRY-SELFTEST-UNRESOLVED` | the flag check is live for flag-carrying rows |
| `correction-section` | the only row for a tool placed in a `## Round-95 correction — …` section below the operative table | FAIL `REGISTRY-ROW-MISSING` | correction-section rows are not operative |
| `real-plus-phantom` | one row names its real tool and `tools/ghost.py` | FAIL `REGISTRY-ROW-ORPHAN` only | `AMBIGUOUS` counts only **committed** tool paths |
| `path-outside-entry` | tool path named only in the pinned-values cell | FAIL `REGISTRY-ROW-MISSING` | coverage scans only the entry and self-test cells |

Receipts: `w1/ExecRegistry/attack-fixtures.json` (row fixtures, each with the fixture commit hex),
`w1/ExecRegistry/real-row-attacks.json` (the real-table attacks). Fixture commits are scratch-repo
hashes, not lane revisions.

**Real holes (what slips through a green run).**

- **H1 — no name↔path binding.** A new row can name another committed tool's path and vice versa; if
  every tool still has exactly one row, the gate reads PASS (`swap`, `real-swap`). The registry's
  "one row, one tool" rule is satisfied by the path set, not by the row's subject.
- **H2 — no content verification of any cell except the `--selftest` substring.** `real-content-lie`
  proves the C2 content target (`default auto`, `39 fixtures`) is certifiable only out of band. A row
  claiming `40 fixtures`, `default 12.9.4`, or a false write scope passes. For C2 this means the gate's
  PASS does not by itself certify the two named cells; this seat's grep (§5) and the gate's own
  `--selftest` run (39/39) do.
- **H3 — `kind = library` bypasses the verdict-map requirement** (`library-bypass`). A tool row
  mislabeled `library` loses both the gate and probe verdict checks while still covering the tool.
- **H4 — `REGISTRY-SELFTEST-UNRESOLVED` is conditional and substring-only.** It fires only for
  `--selftest`-shaped tokens in the self-test cell; the two `make-*-bends` rows carry none, so nothing
  in their self-test cell is checked. Where it does fire, a mention in a comment satisfies it
  (`phantom-content`), and the tally numbers are never checked. A new row that writes its self-test as
  prose ("self-test: the exact-once guard") escapes entirely; the typo fixture proves the check itself
  is live when the token is present.
- **H5 — the verdict map is a bare-digit search.** `0 1 2` and `0 2 (the 1 case is untested)` both pass
  (`bare-digit-verdict`, `incidental-one`); the mapping text between the codes is unchecked.
- **H6 — coverage reads only entry + self-test cells.** A tool named in another cell reads
  `REGISTRY-ROW-MISSING` (`path-outside-entry`) — a trap for a new row, not a hole.
- **H7 — rows outside the operative table are invisible.** A row in a correction section reads
  `REGISTRY-ROW-MISSING` (`correction-section`) — a trap: this SKILL.md carries r90/r92/r93 correction
  sections, so a new row placed there instead of in the highest-numbered registry table fails.
- **H8 — `REGISTRY-ROW-AMBIGUOUS` is really "at most one committed tool path".** A row naming one real
  and one phantom tool yields only `ORPHAN` (`real-plus-phantom`); a row naming two real tools is caught
  (selftest `ambiguous-row`). It also does not read paths in the pinned/scope/owner cells.
- **H9 — the freeze manifest does not pin the registry gate.** `grep -c 'check-registry-coverage\|SKILL.md'`
  over `.ufo/waves/round-95/before/freeze-manifest.sha256` and `instruments.sha256` → `0` for both files.
  C2's void clause ("void if the registry gate bytes differ from the freeze manifest") therefore cannot
  be evaluated from the manifest. Measured directly instead: the gate hashes
  `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812` at `c0a20cef`, `b66e6be5` and
  `884ed06b` (identical), and `SKILL.md` is byte-identical at `b66e6be5` and the tip. `SKILL.md` is
  likewise unpinned, so the landed table's bytes rest on the commit hashes only.
- **H10 — `--audit-live-map` changes which lines are read** (`ignore_fenced_code=True` in
  `_operative_rows`); C2's counting command runs without it, so C2's counts are the default-mode counts.
  No fenced registry heading/row exists in the landed `SKILL.md`, so the two modes agree today; a future
  fenced example table inside the operative section would be read as operative by the C2 command and
  skipped by the audit command.

**Checks a new row could fail that the PASS run does not exercise:** all negative branches, concretely
`REGISTRY-KIND-INVALID` (a kind outside gate/probe/library), `REGISTRY-ROW-ORPHAN` (a path typo — note
the swap case H1 is the inverse: a real but wrong path), `REGISTRY-ROW-DUPLICATE` (two rows for one
tool), `REGISTRY-VERDICT-INCOMPLETE` (a `gate` row missing 0/1/2 — proven live above), and
`REGISTRY-SELFTEST-UNRESOLVED` (proven live above). The four landed rows are structurally immune to
kind/ambiguous/orphan/verdict/duplicate/flag failures: each is `gate` with all three codes, names one
committed regular blob, and both battery flags resolve.

## 7. Honesty of each new row (content, verified where the binding rules allow)

| row | content claim | verification | verdict |
|---|---|---|---|
| `limine-pin-battery-r94` | roster 98, self-test 5 cases | `--selftest` → `selftest PASS 5/5`, `roster-literal PASS families_passed=98` | PASS |
| `limine-pin-battery-r95` | roster 99, self-test 5 cases, bytes pinned in the r95 instruments manifest | `--selftest` → `selftest PASS 5/5`, `roster-literal PASS families_passed=99`; `sha256 tools/limine-pin-battery-r95.py` = `a51dca18…` = manifest row | PASS |
| `make-r94-bends` | four one-clause bends, writes `.ufo/waves/round-94/before/controls/bends/` only, pinned in the r94 freeze manifest | NOT run (binding rule forbids it: it writes into the frozen wave dir). Read-only: `make-r94-bends.py:19` `OUT = …/round-94/before/controls/bends`, `VARIANTS` N01-N04; the four bends exist there and all four hashes are pinned in `.ufo/waves/round-94/before/freeze-manifest.sha256` | PASS (source + manifest only) |
| `make-r95-bends` | one-clause bend `N05-strict-8`, writes `.ufo/waves/round-95/before/controls/bends/` only, pinned in the r95 freeze manifest | NOT run (same rule). Read-only: `make-r95-bends.py:16` `OUT = …/round-95/before/controls/bends`, `VARIANTS = {"N05-strict-8": …}`; the bend exists with `sha256 a1dead8b…` = its manifest row | PASS (source + manifest only) |

```
$ TMPDIR=<scratch>/tmp python3 tools/limine-pin-battery-r95.py --selftest
roster-literal     PASS families_passed=99
... 
selftest PASS 5/5            rc=0
$ TMPDIR=<scratch>/tmp python3 tools/limine-pin-battery-r94.py --selftest
roster-literal     PASS families_passed=98
...
selftest PASS 5/5            rc=0
```

Receipts: `w1/ExecRegistry/battery-r95-selftest.txt`,
`w1/ExecRegistry/battery-r94-selftest.txt`.

## 8. Receipts (all written by this seat, under `w1/ExecRegistry/`)

| file | content |
|---|---|
| `c0a20cef-registry.json` | item 1 gate output at the pre-round tip (FAIL 2/2/149/147) |
| `b66e6be5-registry.json` | item 2 gate output at the landed revision (PASS 0/0/151/151) |
| `tip-registry.json` | item 2 gate output at `git rev-parse master` = `884ed06b` (PASS 0/0/151/151) |
| `selftest.txt` | item 3 `PASS (23 cases, 23 passed, 0 failed)` |
| `rows-grep.txt`, `rows-inspect.json` | item 4 rows and their parsed path/flag sets at both revisions |
| `git-facts.txt` | item 2/4/5 git facts: tip move, diff stat, gate and SKILL.md hashes at 3 revisions, `ls-tree` of the four tools, SKILL.md diff |
| `limine-pins-selftest.txt` | item 5 corroboration `selftest PASS 39/39` |
| `battery-r94-selftest.txt`, `battery-r95-selftest.txt` | item 7 roster/case counts |
| `attack-fixtures.json` | item 6 row fixtures (`swap`, `phantom-content`, `library-bypass`, `gate-verdict-required`, `bare-digit-verdict`, `incidental-one`, `correction-section`, `real-plus-phantom`, `path-outside-entry`) |
| `real-row-attacks.json` | item 6 real-table attacks (`real-swap`, `real-content-lie`, `real-selftest-flag-typo`) |

Scratch root `/fast/scratch/hyaku/tsukuroi-r95/ExecRegistry` (fixtures, `tmp/`, driver scripts) was
deleted before yield; nothing under it is cited.

## 9. Risks and blockers

- No blocker; no tool was installed or upgraded. No pacman transaction was attempted.
- C2 verifies at the landed revision **and** at the moved tip (`884ed06b`), with identical counts. The
  tip move is disclosed; it touches no `tools/` file and not `SKILL.md`.
- The gate's PASS does not certify row content (H2) or the row's subject/tool correspondence (H1); the
  two cells C2 names are certified by this seat's grep and by `check-limine-pins.py --selftest` 39/39,
  not by the registry gate. If a future round must lean on the gate alone, the gate needs a
  content-binding check (name↔basename, expected talley parsed from the tool) — reported, not implemented
  here (out of seat scope).
- `make-r94-bends` / `make-r95-bends` rows could not be execution-verified under the binding rule against
  running those tools; their claims are corroborated by source read plus the committed bends and their
  manifest pins.
- The round's freeze manifest pins neither `tools/check-registry-coverage.py` nor `SKILL.md` (H9); C2's
  void clause is unverifiable from the manifest. The gate's bytes are identical at all three measured
  revisions, and `SKILL.md` is identical at the landed revision and the tip.

```json
{"seat":"ExecRegistry","verdict":"findings","notes":"C2 verified: registry gate PASS at b66e6be5 and at tip 884ed06b (moved one commit, numbers unchanged) findings 0 missing 0 tools_total 151 registered 151; pre-round c0a20cef FAIL 2/2/149/147; selftest PASS 23/23; four new rows each name exactly one committed regular tools/ path and the limine-pins row reads default auto and 39 fixtures (selftest 39/39, no 12.9.4, 37 only inside S374-S376). Gate blind spots found: no name-path binding (real table swap reads PASS 151/151), no content verification (real table with limine-pins default 12.9.4 and 88 fixtures reads PASS 151/151), library kind bypasses the verdict map, selftest-flag check is substring-only and absent for make-*-bends rows, verdict check is a bare-digit search. Freeze manifest pins neither the registry gate nor SKILL.md; gate bytes 6fcb2d0a identical at c0a20cef/b66e6be5/884ed06b."}
```
