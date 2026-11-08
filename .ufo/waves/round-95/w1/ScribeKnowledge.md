# ScribeKnowledge — round-95 knowledge-entry draft (wave w1, seat ScribeKnowledge)

Seat: scribe (axes: depth). Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch
`master`, jj-colocated; git HEAD detached at `884ed06b`). **This seat wrote no lane file outside
its own seat dir**: the only paths it created are
`.ufo/waves/round-95/w1/ScribeKnowledge.md` (this report) and the tree under
`.ufo/waves/round-95/w1/ScribeKnowledge/` (the draft entry + receipts). No `git`/`jj` mutation was
run (read-only `git log`/`git status`/`git rev-parse` only); no `git commit|push|stash|checkout|
reset|switch` and no `jj` write. `tools/make-r94-bends.py` and `tools/make-r95-bends.py` were
**not** run (they write into the lane's frozen wave dir). The battery was **not** run by this
seat, per the seat spec — every battery number in the draft is cited by path to the L1's or an
Exec seat's committed receipt, and this seat re-parsed those receipts read-only into
`receipts/04-sibling-receipts-reparse.txt`.

Deliverable (the draft the L1 integrates into `corpus/knowledge/limine-bound-9digit-r95.md`):

- **`.ufo/waves/round-95/w1/ScribeKnowledge/draft/knowledge/limine-bound-9digit-r95.md`** — 71
  lines (spec: 60-110), prose only, every number naming the artifact that carries it.

Receipts (all under `.ufo/waves/round-95/w1/ScribeKnowledge/receipts/`):
`01-gate-clauses.txt`, `02-refusal-digit9-grep.txt`, `03-family-source.txt`,
`04-sibling-receipts-reparse.txt`, `05-extra-component-shape.txt`, `06-instruments-check.txt`,
`07-python-int-limit.txt`, `08-source-pins.txt`, `09-gate-quotes.txt`.

---

## 1. What the seat did, in one line

Drafted the round's knowledge entry (the r95 accepted leg of the gate's published 1-9-digit
component bound) and, for every number in it, resolved the artifact that carries it — the gate
clause by `file:line`, the battery's roster by AST parse, the sibling receipts by read-only
re-parse with their sha256 pinned.

## 2. The commands run, and their raw output (trimmed)

All commands were run with `cwd` = the lane root unless noted; every one is read-only.

### 2.1 The gate clauses (`receipts/01-gate-clauses.txt`)

```
$ sha256sum tools/check-limine-pins.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
$ grep -n 'len(p) <= 9' tools/check-limine-pins.py
99:    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
$ grep -n 'VISIBILITY_ERA_SPLIT' tools/check-limine-pins.py
104:VISIBILITY_ERA_SPLIT = (12, 9, 5)   # first upstream release with the create_menu_tree() cut
193:    era_b = version >= VISIBILITY_ERA_SPLIT
```

The sha256 matches the frozen instrument digest the round's brief states for
`tools/check-limine-pins.py` (`7d79ac29…`), and `receipts/06-instruments-check.txt` shows
`sha256sum -c .ufo/waves/round-95/before/instruments.sha256` → 9/9 `OK`, rc 0.

### 2.2 `grep -c REFUSAL_DIGIT9`, before and after (`receipts/02-refusal-digit9-grep.txt`)

```
$ grep -c REFUSAL_DIGIT9 tools/limine-pin-battery-r94.py
1
$ grep -c REFUSAL_DIGIT9 tools/limine-pin-battery-r95.py
3
$ grep -n REFUSAL_DIGIT9 tools/limine-pin-battery-r94.py
1684:REFUSAL_DIGIT9 = "9" * 9 + ".9.9"  # X.Y.Z-shaped, first component 999,999,999: the cap's boundary member, ACCEPTED
$ grep -n REFUSAL_DIGIT9 tools/limine-pin-battery-r95.py
29:values and never the largest in-bound member, and the declared `REFUSAL_DIGIT9` constant is
1694:REFUSAL_DIGIT9 = "9" * 9 + ".9.9"  # X.Y.Z-shaped, first component 999,999,999: the cap's boundary member, ACCEPTED
1715:    _era_first_line_panic(c, REFUSAL_DIGIT9)
```

Before: **1** line — the declaration, referenced nowhere. After: **3** lines — a docstring
mention, the declaration, and the single use that makes it live. `grep -o | wc -l` agrees (1 → 3).

### 2.3 The roster, measured by AST parse (the battery was not executed)

```
$ python3 - <<'EOF'   # ast.literal_eval on the FAMILY_ROSTER assignment
r95 FAMILY_ROSTER: 99 names, 99 unique, has REFUSAL-VERSIONS-9DIGIT: True
r94 FAMILY_ROSTER: 98 names, 98 unique, has REFUSAL-VERSIONS-9DIGIT: False
r95 - r94 = ['REFUSAL-VERSIONS-9DIGIT']
```

### 2.4 The sibling receipts, re-parsed (`receipts/04-sibling-receipts-reparse.txt`)

```
## .ufo/waves/round-95/after/c1-canonical.json        sha256 b67391b7cd334b92…
   run0 verdict=met families_passed=99/99 failed_families=[] cases=396 error_rows=0 REFUSAL-VERSIONS-9DIGIT_rows=4
   run1 verdict=met families_passed=99/99 failed_families=[] cases=396 error_rows=0 REFUSAL-VERSIONS-9DIGIT_rows=4
   run2 verdict=met families_passed=99/99 failed_families=[] cases=396 error_rows=0 REFUSAL-VERSIONS-9DIGIT_rows=4
   row: passed=True want=[1, 'DEGRADED', [[3, 'LP-MISMATCH', 'panic'], [7, 'OK', 'none']], 'menu']
             got=[1, 'DEGRADED', [[3, 'LP-MISMATCH', 'panic'], [7, 'OK', 'none']], 1, 'menu', '999999999.9.9', 'flag'] error=None

## .ufo/waves/round-95/w1/ExecBattery/c1-canonical.json  sha256 ce04582e11b08d68…   met 99/99 ×3, error_rows=0
## .ufo/waves/round-95/w1/ExecBattery/c1-clone.json      sha256 eb54cb1eb12aee60…   met 99/99 ×3, error_rows=0
## .ufo/waves/round-95/w1/ExecBend/n05-canonical.json    sha256 5c89b704965824e1…
   run0 verdict=unmet families_passed=98/99 failed_families=['REFUSAL-VERSIONS-9DIGIT'] cases=396 error_rows=4
   row: passed=False want=[1, 'DEGRADED', [[3, 'LP-MISMATCH', 'panic'], [7, 'OK', 'none']], 'menu'] got=None
        error=bad-output: JSONDecodeError rc=64 stderr=… check-limine-pins: --limine-version must be X.Y.Z or auto
## .ufo/waves/round-95/w1/ExecDoNothing/dn-n05.json      sha256 9c8cfd8996994654…  met 98/98 ×3, 9DIGIT_rows=0, error_rows=0
## .ufo/waves/round-95/w1/ExecDoNothing/dn-gate.json      sha256 4b165aa965ff4cd3…  met 98/98 ×3, 9DIGIT_rows=0, error_rows=0
```

### 2.5 The extra-component shape (`receipts/05-extra-component-shape.txt`)

```
$ grep -n '12.9.6.1' tools/limine-pin-battery-r95.py
153:     and `12.9.6.1` are probe failures), and select V1/V2 from that value; the JSON's
2299:        cases = [("12.9", 64), ("abc", 64), ("12.9.6.1", 64), …
$ grep -n 'Limine 12.9.6.1' tools/limine-pin-battery-r95.py
(grep rc=1 -> no match: no family sends the probe's extra-component answer)
```

This corrected a draft error: my first pass said the four-component *shape* was unexercised. It
is not — `REFUSAL-VERSIONS` sends `12.9.5.1` (`tools/limine-pin-battery-r95.py:1643`). What is
open is the **probe** answer `Limine 12.9.6.1`, which `AUTO-PROBE-SHAPES` never sends
(`tools/limine-pin-battery-r95.py:1718`, `:1938`). The entry now says exactly that.

### 2.6 The entry's Gate-table quotes, checked against the pins (`receipts/09-gate-quotes.txt`)

```
## S389 — python-3-stdtypes.html
quote: The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits.
words: 10
present (text-stripped grep): True
## S386 — limine-12.9.6-common_lib_config.c (raw 328-330)
    if (p > config_addr) {
        *(p - 1) = '\0';
    }
## S387 — limine-12.9.6-ChangeLog (the #700 sentence)
14:          has been the case since 4.0. A config whose first line is an entry
15-          has had no global options since 12.9.5, whereas every option in it
16-          used to count as global. Fixes #700.
## S388 — limine-12.9.6-host_limine.c (raw 2035)
    puts("Limine " LIMINE_VERSION);
```

`cmp` on the S382/S386 and S384/S388 pairs returns rc 0 (receipt 08).

## 3. PASS/FAIL per expected line of the seat spec

| expected | result | where |
|---|---|---|
| draft `corpus/knowledge/limine-bound-9digit-r95.md`, 60-110 lines, prose only | **PASS** (71 lines) | `ScribeKnowledge/draft/knowledge/limine-bound-9digit-r95.md` |
| header states the rule: a published numeric bound is certified at its boundary, two legs | **PASS** | entry lines 1-9 |
| the two legs the lane now holds (10DIGIT refused, 9DIGIT accepted) | **PASS** | entry §"The two legs the lane now holds" |
| exact gate clauses: `len(p) <= 9` quoted with file:line, and the era split | **PASS** (`tools/check-limine-pins.py:99`, `:104`, `:193`) | entry §"The gate clauses" |
| why the accepted leg was missing: r94's declared-but-unreferenced `REFUSAL_DIGIT9`, constant quoted, `grep -c` before/after | **PASS** (1 → 3; the constant is quoted verbatim) | entry §"Why the accepted leg was missing" |
| the family's fixture shape and expected answer (`panic`, era B) | **PASS** (first physical line is an entry label; `panic` because the key is invisible in era B) | entry §"The family's fixture shape and expected answer" |
| the bend N05 and its `failed_families` | **PASS** (`unmet` 98/99 ×3, `failed_families` exactly `["REFUSAL-VERSIONS-9DIGIT"]`, cited to the ExecBend receipt) | entry §"The bend N05" |
| the do-nothing blindness (r94 battery met 98/98) | **PASS** (both legs: on N05 and on the landed gate) | entry §"The do-nothing blindness" |
| sources cited (S389 new; S382/S384/S386/S387/S388 re-opened) in the entry's `source:` line | **PASS** | entry line 3 |
| Limits section: one in-bound version; the 1-9-digit cap is the gate's own contract; the extra-component `12.9.6.1` shape stays open | **PASS** (4 bullets; the third is the probe shape, corrected) | entry §"Limits" |
| every number names the artifact that carries it | **PASS** — see §4 | — |
| do not run the battery | **PASS** — not run; sibling receipts cited by path and re-parsed | — |
| receipts under the seat dir, written by this seat | **PASS** (9 receipt files + the draft) | `ScribeKnowledge/receipts/` |

## 4. The "every number names its artifact" audit

Every number in the draft, with the artifact that carries it (all verified to exist and to resolve
at the cited line):

| number in the draft | artifact |
|---|---|
| `len(p) <= 9`; `1-9 digits per component`; `4300 digits` | `tools/check-limine-pins.py:99`, `:92-95` (sha256 `7d79ac29…`, receipt 01) |
| `(12, 9, 5)` era split | `tools/check-limine-pins.py:104`, applied at `:193` (receipt 01) |
| rc 64 / empty stdout refusal | `tools/check-limine-pins.py:190-192` (receipt 01) |
| the four ten-digit values | `tools/limine-pin-battery-r95.py:1648` (receipt 03) |
| `999999999.9.9` / 999,999,999 | `tools/limine-pin-battery-r95.py:1694` (receipt 03) |
| `grep -c` 1 → 3; roster 99 / 98; difference = one family | receipt 02 (AST parse + grep, both re-run) |
| r94's constant, quoted | `tools/limine-pin-battery-r94.py:1684` (receipt 03) |
| the defect quote "declared and referenced nowhere" | `corpus/lessons/round-94-verifier-spotcheck.md:242`, routed at `:241-244` |
| fixture helper and family source | `tools/limine-pin-battery-r95.py:1567-1579`, `:1707-1715` (receipt 03) |
| `met` 99/99 ×3, 0 error rows, 396 cases; the four `want`/`got` rows | `w1/ExecBattery/c1-canonical.json`, `c1-clone.json`, re-parsed in receipt 04 |
| version + source in the answer tuple | `tools/limine-pin-battery-r95.py:2002` |
| N05 one-clause diff; 1 hunk / 1 minus / 1 plus | `w1/ExecBend/n05-diff.txt`, `w1/ExecBend/diff-counts.txt` |
| `unmet` 98/99 ×3; `failed_families` exactly `["REFUSAL-VERSIONS-9DIGIT"]`; rc 1 from count-runs | `w1/ExecBend/n05-canonical.json`, `count-runs-canonical.txt`, `count-runs-canonical.rc` |
| the four error rows' text; `error_rows_outside_digit9=0` | `w1/ExecBend/n05-canonical-analysis.txt` |
| r94 battery `met` 98/98 ×3, 0 rows of the family | `w1/ExecDoNothing/dn-n05.json`, `dn-gate.json` (receipt 04) |
| 4300-digit default limit, `ValueError` | S389, pinned copy sha256 `6bf2ce2b…` in `w1/ScoutSources/receipts/pin-table.tsv` and in receipt 08; the same limit re-observed by this seat on this host — `python3 -c "int('2'*5432)"` → `ValueError: Exceeds the limit (4300 digits) …`, `sys.int_info.default_max_str_digits` → `4300` (receipt 07) |
| S382 == S386 and S384 == S388 byte-identity | `cmp` rc 0 on both pairs in `w1/ScoutSources/pins/` (receipt 08) |
| `12.9.5.1` in the scored roster | `tools/limine-pin-battery-r95.py:1643` (receipt 05) |
| the probe's extra-component answer unsent | `tools/limine-pin-battery-r95.py:1718`, `:1938` (receipt 05) |
| `1000000000` gap, r94-measured | `.ufo/waves/round-94/w1/ScribeLesson/receipts/02-boundary-measurements.txt` |
| the `12.9.6.1` gap as r94 recorded it | `.ufo/waves/round-94/w1/ReviewBattery.md:36`, `corpus/lessons/round-94-verifier-spotcheck.md:245-247` |
| freeze `2abddda5`, tip `884ed06b` | `git log --oneline` (read-only) |

## 5. Findings (for the L1 / the canonical judge)

1. **The extra-component `12.9.6.1` gap is the PROBE shape, not the refusal shape.** The r94
   verifier's routed item 9 (`corpus/lessons/round-94-verifier-spotcheck.md:245-247`) and r94's
   ReviewBattery F1 (`.ufo/waves/round-94/w1/ReviewBattery.md:36`) name the `12.9.6.1`
   extra-component shape as unexercised at battery level. The **refusal** side is exercised — the
   scored `REFUSAL-VERSIONS` roster sends the four-component value `12.9.5.1`
   (`tools/limine-pin-battery-r95.py:1643`). What no family sends is the **probe** answer
   `Limine 12.9.6.1` (`AUTO-PROBE-SHAPES` sends only a no-parsable answer and the suffixed
   `Limine 12.9.6-rc1`, `tools/limine-pin-battery-r95.py:1718`, `:1938`). The r95 entry states it
   in that form. If the round's Frontier bullet intends the probe shape, the wording carries; if it
   intends a refusal-shape gap, that bullet is stale. **The wording correction belongs in the
   lesson's Frontier, not in this entry.**
2. **The r94 ten-digit enumeration still does not start at the smallest out-of-bound value.**
   `REFUSAL_DIGIT10` sends `1234567890` and its digit-permutations
   (`tools/limine-pin-battery-r95.py:1648`), never `1000000000` (1,000,000,000), the smallest
   ten-digit number; r94's ScribeLesson measured that gap
   (`.ufo/waves/round-94/w1/ScribeLesson/receipts/02-boundary-measurements.txt`). The r95 accepted
   leg closes the *other* end (999,999,999), which QUALITY 139 requires, so the entry records the
   gap as still open rather than claiming the bound is certified at **both** extremes. A gate that
   refuses by value (≥ 1e9) instead of by digit count would still pass the r95 roster — the r94
   lesson's `capvalue` mutant is the counterexample and it is unaffected by this round.
3. **The refused leg's own roster is r94's, unchanged** — the r95 battery's `REFUSAL-VERSIONS-10DIGIT`
   is byte-identical in content to r94's (`tools/limine-pin-battery-r95.py:1697-1704`). The entry
   says so rather than implying r95 re-certified it.
4. **`REFUSAL_DIGIT9`'s r94 declaration was the right constant to keep.** It is the same string
   r95 now sends (`tools/limine-pin-battery-r95.py:1694` vs `tools/limine-pin-battery-r94.py:1684`),
   so the r94 defect closed by *reference*, not by a rewrite. The entry says that.
5. **The L1 landed its own entry at `corpus/knowledge/limine-bound-9digit-r95.md` before this
   seat's draft finished (07:05:18), then merged this seat's findings into it.** The timeline:
   the L1's own 95-line text landed at 07:04:58; this seat's draft was written at 07:05:18; the
   L1's message to this seat asked for the three items listed below; the landed file was then
   rewritten to **106 lines** (mtime 07:12) and now carries the **`grep -c REFUSAL_DIGIT9`
   before/after evidence** (`:55-57`: "→ **1** in `tools/limine-pin-battery-r94.py`, the
   declaration only" and "→ **3** in `tools/limine-pin-battery-r95.py`: docstring `:29`,
   declaration `:1694`, the live use `:1715`"), the **`12.9.6.1` probe-shape Limits bullet**
   (`:90-93`: "The open `12.9.6.1` gap is the PROBE answer … The refusal roster does send
   `12.9.5.1` … so a 'refusal-shape gap' wording would be stale"), and the
   **ten-digit smallest-outside-value bullet** (`:94-95`). This seat did not write that file —
   `corpus/` is outside the seat's write scope; the merge is the L1's. **This seat's draft at
   `.ufo/waves/round-95/w1/ScribeKnowledge/draft/knowledge/limine-bound-9digit-r95.md` (71 lines)
   remains the independent second text** and carries the same three items with its own citations.
   One wording item is still open in the landed text: its table row (`:45`) reads "`999999999.9.9`
   — a boundary member: the first component is 999,999,999 (the largest nine-digit value), the
   second and third are 9". The parenthetical still says "the largest nine-digit value" for the
   first component; `w1/ReviewBattery.md:110-113` measured that the cap admits
   `999999999.999999999.999999999` — strictly larger — and asked for the wording "a boundary
   member: first component at the cap" (`w1/ReviewBattery/boundary-probe.txt`). The landed row now
   scopes the value to "the first component", which is the fix's substance; the parenthetical
   itself is redundant with it. This seat's draft drops the parenthetical. Neither the frozen claim
   nor the landed entry is falsified by the measurement (the claim sentence in
   `.ufo/waves/round-95/claims.json` carries the same superlative); it is a wording call, and the
   judge may take it or leave it.

No conflict with the L1's or the Exec seats' receipts was found: every number re-parsed from those
receipts agrees with the frozen target in `.ufo/waves/round-95/claims.json` (A1-narrowed C1
target), and none disagrees.

## 6. Scope, tooling, and cleanup

- **Files written by this seat, all inside its own scope:**
  `.ufo/waves/round-95/w1/ScribeKnowledge.md` (this report);
  `.ufo/waves/round-95/w1/ScribeKnowledge/draft/knowledge/limine-bound-9digit-r95.md`;
  `.ufo/waves/round-95/w1/ScribeKnowledge/receipts/01-gate-clauses.txt`,
  `02-refusal-digit9-grep.txt`, `03-family-source.txt`, `04-sibling-receipts-reparse.txt`,
  `05-extra-component-shape.txt`, `06-instruments-check.txt`, `07-python-int-limit.txt`,
  `08-source-pins.txt`, `09-gate-quotes.txt`.
  **Nothing** outside `.ufo/waves/round-95/w1/ScribeKnowledge/` was written — in particular
  `corpus/`, `tools/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `.ufo/plans/`,
  `.ufo/waves/round-95/before/`, `claims.json`, `.ufo/state/` and `.scratch/` are untouched.
  The entry itself is a **draft** for the L1 to land; this seat did not write
  `corpus/knowledge/limine-bound-9digit-r95.md` (it is outside the seat's write scope).
- **Tooling: no install, no upgrade, no host change.** No `pacman` transaction (host-wide pause
  respected), no `uv tool`/`npx`/`cargo` install, no `~/.local/bin` write, no sysctl/service/kernel
  change. The seat needed nothing beyond `python3` (3.14, already present), `grep`, `sed`, `sha256sum`.
  Nothing to record in the tooling ledger.
- **Scratch:** `/fast/scratch/hyaku/tsukuroi-r95/ScribeKnowledge/` was created for the read-only
  scratch space and is removed before this report is filed. No fixture was generated, no battery
  was run, no clone was made.
- **Instruments:** `sha256sum -c .ufo/waves/round-95/before/instruments.sha256` → 9/9 `OK`, rc 0
  (`receipts/06-instruments-check.txt`). `tools/check-limine-pins.py` reads
  `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32` and
  `tools/limine-pin-battery-r95.py` reads
  `a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb` — both as the round's brief
  states. `tools/make-r94-bends.py` and `tools/make-r95-bends.py` were not run.

## 7. What the main agent should check

1. The entry is **already landed** at `corpus/knowledge/limine-bound-9digit-r95.md` (106 lines,
   mtime 07:12) and the S389 row is already in `corpus/SOURCES.md:400`. The L1 merged this seat's
   three findings into the landed text after this seat's message (finding 5). This seat's draft is
   an **independent second text** at
   `.ufo/waves/round-95/w1/ScribeKnowledge/draft/knowledge/limine-bound-9digit-r95.md` (71 lines),
   still on disk for the judge's comparison; this seat did not touch `corpus/`.
2. The one wording item still open in the landed text is the "largest nine-digit value"
   parenthetical in its table row (finding 5) — the judge's call, not a falsification.
3. Confirm the sibling receipts cited by path are the ones the L1 intends to file (they were
   present and consistent at this seat's read time; a later re-run would change their sha256).

{"seat":"ScribeKnowledge","verdict":"findings","notes":"Drafted the round's knowledge entry (71 lines, prose only) at .ufo/waves/round-95/w1/ScribeKnowledge/draft/knowledge/limine-bound-9digit-r95.md; every number names the artifact that carries it (gate clauses by file:line, roster by AST parse, battery numbers by the L1/Exec receipt paths re-parsed read-only with sha256 pinned). Covers the two-leg rule, the 10DIGIT-refused / 9DIGIT-accepted legs, the len(p) <= 9 clause (check-limine-pins.py:99) and the (12,9,5) era split (:104/:193), r94's declared-but-unreferenced REFUSAL_DIGIT9 with grep -c 1 -> 3, the fixture shape and the panic/era-B expected answer, bend N05 (unmet 98/99 x3, failed_families exactly ['REFUSAL-VERSIONS-9DIGIT']), the r94-battery blindness (met 98/98 x3, 0 family rows), the source: line (S389 new; S382/S384/S386/S387/S388 re-opened), and a Limits section. Battery NOT run; no instrument, corpus or product file touched; 9 receipts under the seat dir; no tooling installed; scratch removed. FINDINGS: (1) the 12.9.6.1 gap is the PROBE answer (Limine 12.9.6.1), not the refusal shape - 12.9.5.1 IS sent by REFUSAL-VERSIONS, so a Frontier bullet worded as a refusal-shape gap would be stale; (2) the ten-digit leg still does not send the smallest out-of-bound value 1000000000, so a value-capping mutant would still pass the r95 roster - carried, not closed; (3) the accepted leg certifies only the FIRST component's boundary - a bend of Y's bound to <= 8 still reads met 99/99 (w1/ReviewBattery/middle-bound-probe.txt), so the per-component accepted boundary stays Frontier work; (4) the L1 landed its own entry at corpus/knowledge/limine-bound-9digit-r95.md (95 lines at 07:04:58, before this seat's draft at 07:05:18) and, after this seat's message, merged three of this seat's findings into it (106 lines at 07:12): the grep -c REFUSAL_DIGIT9 before/after evidence, the 12.9.6.1 probe-shape Limits bullet, and the ten-digit smallest-outside-value bullet. One wording item remains open in the landed text (its table row still carries the parenthetical 'the largest nine-digit value' for the first component, which w1/ReviewBattery.md:110-113 measured as inaccurate - the cap admits 999999999.999999999.999999999); this seat's draft drops it. This seat wrote nothing in corpus/ - the merge is the L1's."}
