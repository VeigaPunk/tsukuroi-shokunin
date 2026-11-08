# The third component's cap, the accepted leading-zero form, and a registry row's declared values

source: `corpus/SOURCES.md` S389 (CPython documentation, integer string conversion length
limitation — the 4300-digit default, opened 2026-11-08) and S391 (CPython documentation,
`sys.int_info.default_max_str_digits`, opened 2026-11-08; supersedes S390), both re-opened from
their pinned copies on 2026-11-08 (command `python3 - <pins dir>` printing each file's sha256 and
the cited byte offsets; receipt
`.ufo/waves/round-97/w1/ScribeKnowledge/receipts/pc1-sources-reopen.txt`: `stdtypes.html`
815447 B sha256 `6bf2ce2b…`, the "The default limit is 4300 digits as provided in
sys.int_info.default_max_str_digits" sentence at byte 785297; `sys315.html` 280632 B sha256
`a7e00587…`, the "The default value for sys.get_int_max_str_digits() when it is not otherwise
explicitly configured." sentence at byte 157851);
S### (new row this round — the CPython `int()` built-in-functions page: the string form of
`int(x, base)` may "have leading zeros", and base 0 disallows them; pinned copy
`int-functions.html` 331022 B sha256 `d92580dd…`, the leading-zero sentence at byte 157767 and
"Base 0 also disallows leading zeros: `int('010', 0)` is not legal, while `int('010')` and
`int('010', 8)` are." at byte 159303 — command `python3 -` over the pinned copy; receipt
`.ufo/waves/round-97/w1/ScribeKnowledge/receipts/pc2-int-doc-anchors.txt`; the L1 substitutes the
row id);
own-work: `tools/check-limine-pins.py` `parse_limine_version()` and `VISIBILITY_ERA_SPLIT`,
`tools/limine-pin-battery-r97.py` (the two families named below, the bends `N05-z-cap-8` and
`N06-leading-zero-reject` under `.ufo/waves/round-97/before/controls/bends/`) and
`tools/check-registry-content.py` (the seven bindings below); the instruments are pinned in
`.ufo/waves/round-97/before/instruments.sha256` (gate `7d79ac29…`, r97 battery `e678c34f…`,
r97 bend maker `972c672b…`, registry-content checker `2daf5926…`, coverage gate `6fcb2d0a…`;
command `sha256sum -c .ufo/waves/round-97/before/instruments.sha256`, receipt
`receipts/instruments-sha256-check.txt`).
verified-at: 2026-11-08 (round 97; every number below is a receipt this seat ran —
`.ufo/waves/round-97/w1/ScribeKnowledge/receipts/`, indexed by `receipts/COMMANDS.md`).
recheck: `python3 tools/limine-pin-battery-r97.py --gate tools/check-limine-pins.py --runs 3
--work <scratch> --json OUT` (three runs read `families_passed 105/105 verdict met failed -`, 0
error rows each — receipt `receipts/c1-gate-landed.txt`, `receipts/c1-gate-landed-count-runs.json`);
`python3 tools/check-limine-pins.py --selftest` (`selftest PASS 39/39` — receipt
`receipts/gate-selftest.txt`); `python3 tools/check-registry-content.py --revision <REV> --json OUT`
(`status PASS`, `bindings 7`, `findings []` — receipt `receipts/c2-content-landed.json`);
`python3 tools/check-registry-content.py --selftest` (`selftest PASS 12/12` — receipt
`receipts/c2-content-selftest.txt`).

## PC1 — the 1-9-digit cap is per component, and the THIRD component was the uncertified leg

`tools/check-limine-pins.py` accepts a `--limine-version` only as three ASCII-digit components of
1-9 digits each (`parse_limine_version()`, `tools/check-limine-pins.py:91-101`: `if len(parts) != 3
or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts): return None`; command
`sed -n '91,101p' tools/check-limine-pins.py`, receipt
`receipts/pc1-gate-parser-source.txt`), because handing an unbounded component to `int()`
raises above CPython's decimal-conversion digit limit — the 4300-digit default S389 states and
S391 names. The bound is therefore **per component**, and the earlier rounds had certified only
the first two positions: the X leg (`999999999.9.9`, the r95 family's
`REFUSAL-VERSIONS-9DIGIT`) and the Y leg (`12.999999999.4`, `0.999999999.0`, the r96 family's
`REFUSAL-VERSIONS-9DIGIT-Y`), while the r96 Frontier named the **third** component as
uncertified — "`corpus/README.md` Frontier (round-96 addition)": "The Z component's 9-digit
boundary is **uncertified**: MutBound's `M06-z-cap-8` survives 103/103 … QUALITY 139's boundary
rule therefore holds at family level for X and Y only" (command
`sed -n '1173,1177p' corpus/README.md`; receipt `receipts/pc1-r96-frontier-readme.txt`).

Round 97 closes that leg. The family `REFUSAL-VERSIONS-9DIGIT-Z` sends the cap member in the
third component, `12.9.999999999` (whole tuple `>= 12.9.5`, era B) and `0.9.999999999` (era A)
(`tools/limine-pin-battery-r97.py:1798`, `Z_DIGIT9 = ("12.9.999999999", "0.9.999999999")`; command
`grep -n 'Z_DIGIT9 = ' tools/limine-pin-battery-r97.py`, receipt
`receipts/limits-family-shapes.txt`). Both are **in-bound**, so the gate must answer a verdict —
never the rc-64 usage refusal — and the answer must come from the era the whole tuple selects:
measured per case, `12.9.999999999` returns rc 1 / `DEGRADED` with the era-B answer `panic` and
`0.9.999999999` returns rc 1 / `DEGRADED` with the era-A answer `prompt` (command
`python3 tools/limine-pin-battery-r97.py --gate tools/check-limine-pins.py --runs 3 --work <scratch>
--json OUT`, then reading the two families' rows of run 0; receipt
`receipts/pc1-pc2-case-rows.txt`). The parser probe
shows why the two differ: `parse_limine_version("12.9.999999999")` → `(12, 9, 999999999)` (era
`12.9.5+`) and `parse_limine_version("0.9.999999999")` → `(0, 9, 999999999)` (era `pre-12.9.5`),
because the era split is the whole tuple `(12, 9, 5)`, not the largest component (command
`python3 <scratch>/probe/parse-probe.py tools/check-limine-pins.py`; receipt
`receipts/pc2-parse-probe.txt`).

Witnesses, all run by this seat:

- **the r97 family**: on the landed gate the family reads 4 cases, 4 passed, 0 failed in each of
  three runs (`families_passed 105/105 verdict met failed -` ×3; commands
  `python3 tools/limine-pin-battery-r97.py --gate tools/check-limine-pins.py --runs 3 --work
  <scratch> --json OUT` and
  `python3 .ufo/waves/round-95/before/controls/count-runs.py OUT --family
  REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE`; receipts
  `receipts/c1-gate-landed.txt`, `receipts/c1-gate-landed-count-runs.json`, whose per-family tally
  is `{'REFUSAL-VERSIONS-9DIGIT-Z': [4, 0]}`, `{'LEADING-ZERO-NORMALIZE': [4, 0]}`).
- **the bend `N05-z-cap-8`** (the Z bound bent to `<= 8`): three runs read
  `families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z`
  (command `python3 tools/limine-pin-battery-r97.py --gate
  .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py --runs 3 --work <scratch> --json OUT`;
  receipt `receipts/c1-bend-N05.txt`), the per-family tally `{'LEADING-ZERO-NORMALIZE': [2, 2],
  'REFUSAL-VERSIONS-9DIGIT-Z': [0, 4]}` and `error_rows 6` per run (same count-runs command;
  receipt `receipts/c1-bend-N05-count-runs.json`). The four Z error rows are the bend's own
  refusals — `bad-output: JSONDecodeError rc=64 stderr=usage: gate.py … check-limine-pins:
  --limine-version must be X.Y.Z or auto` (reading run 0's `error` fields of the same battery JSON;
  receipt `receipts/c1-bend-N05.json`) — and the instrument's own `--usage-check` mode reads the
  same two Z versions as rc 64 on that bend (command `python3 tools/limine-pin-battery-r97.py
  --usage-check --gate .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py --work <scratch>`;
  receipt `receipts/c1-usage-N05.txt`).
- **the r96 roster is blind to it**: the r96 do-nothing battery
  (`.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py`, sha256 `f06d90ae…`) reads
  `families_passed 103/103 verdict met failed -` in each of three runs on the landed gate **and on
  the `N05-z-cap-8` bend** (commands `python3
  .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py --gate <gate> --runs 3 --work
  <scratch> --json OUT` for each gate; receipts `receipts/c1-dn-gate.txt`,
  `receipts/c1-dn-bend-N05.txt`), and the r96 roster has neither family (command
  `grep -n 'Z_DIGIT9\|LEADING_ZERO' .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py`
  → no match; receipt `receipts/limits-r96-instrument-level.txt`).

## PC2 — a leading-zero component is a legal decimal spelling, normalized by `int()`

`parse_limine_version` splits on `.`, requires each component to be ASCII digits of 1-9
characters, and converts with `int()` — `return tuple(int(p) for p in parts)`
(`tools/check-limine-pins.py:101`; command `sed -n '91,101p' tools/check-limine-pins.py`, receipt
`receipts/pc1-gate-parser-source.txt`), so a component
written `09`, `000000012` or `000000009` is the *same number* as its short form, and the era
follows the numeric tuple, not the spelling. Measured by the parser probe (command
`python3 <scratch>/probe/parse-probe.py tools/check-limine-pins.py`; receipt
`receipts/pc2-parse-probe.txt`):

| spelling | parsed tuple | era |
|---|---|---|
| `12.09.4` | `(12, 9, 4)` | `pre-12.9.5` (A) |
| `000000012.9.4` | `(12, 9, 4)` | `pre-12.9.5` (A) |
| `12.000000009.000000005` | `(12, 9, 5)` | `12.9.5+` (B) |
| `000000000.000000000.000000000` | `(0, 0, 0)` | `pre-12.9.5` (A) |

So `000000012.9.4` is 12.9.4 (era A) and `12.000000009.000000005` is 12.9.5 (era B) — the era
moves with the value, and the leading zeros are not a second grammar. Upstream, this is CPython's
own `int()` contract for an explicit base: the string "can be preceded by `+` or `-` … **have
leading zeros**, be surrounded by whitespace …" and "Base 0 also disallows leading zeros:
`int('010', 0)` is not legal, while `int('010')` and `int('010', 8)` are." (S###, new row this
round; bytes 157767 and 159303 of the 331022 B pin sha256 `d92580dd…`; command
`python3 - <pins dir>` printing each sha256 and offset; receipts
`receipts/pc2-int-doc-anchors.txt`, `receipts/pc1-sources-reopen.txt`). The gate calls `int(p)`
with the default base 10, which is the `int('010')` case the page calls legal.

Witnesses, all run by this seat:

- **the r97 family `LEADING-ZERO-NORMALIZE`**: the four members above are each sent once per run
  (`tools/limine-pin-battery-r97.py:1799`, `LEADING_ZERO_VALUES = ("12.09.4", "000000012.9.4",
  "12.000000009.000000005", "000000000.000000000.000000000")`; command
  `grep -n 'LEADING_ZERO_VALUES = ' tools/limine-pin-battery-r97.py`, receipt
  `receipts/limits-family-shapes.txt`), each accepted with its own era's answer — `12.09.4` and
  `000000012.9.4` give the era-A answer `prompt`, `12.000000009.000000005` gives the era-B answer
  `panic`, `000000000.000000000.000000000` gives `prompt` (command: the r97 battery JSON's
  `case_log` rows for the family, run 0; receipt `receipts/pc1-pc2-case-rows.txt`); 4 passed /
  0 failed per run (command `python3 .ufo/waves/round-95/before/controls/count-runs.py OUT --family
  LEADING-ZERO-NORMALIZE`; receipt `receipts/c1-gate-landed-count-runs.json`).
- **the bend `N06-leading-zero-reject`** (a component whose first digit is `0` refused): three runs
  read `families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE` with `error_rows 4`
  per run and the per-family tally `{'LEADING-ZERO-NORMALIZE': [0, 4],
  'REFUSAL-VERSIONS-9DIGIT-Z': [4, 0]}` (commands `python3 tools/limine-pin-battery-r97.py --gate
  .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py --runs 3 --work <scratch>
  --json OUT` and the same count-runs command; receipts `receipts/c1-bend-N06.txt`,
  `receipts/c1-bend-N06-count-runs.json`); the four error rows are again the bend's own rc-64
  refusals (reading run 0's `error` fields; receipt `receipts/c1-bend-N06.json`).
- **the r96 roster is blind to it** at roster level: the r96 do-nothing battery reads
  `families_passed 103/103 verdict met failed -` ×3 on the landed gate and on the `N06` bend
  (commands `python3 .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py --gate <gate>
  --runs 3 --work <scratch> --json OUT`; receipts `receipts/c1-dn-gate.txt`,
  `receipts/c1-dn-bend-N06.txt`). *Scope note:* at
  **instrument** level the leading-zero class was sampled before this round — the r96 battery's
  `--usage-check` mode already sends `12.09.4` and `00.00.00` (both expected rc 0) and reads
  `unmet` on the `N06` bend on exactly those two rows (command `python3
  .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py --usage-check --gate
  .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py --work <scratch>`; receipt
  `receipts/c1-dn-usage-N06.txt`), while the
  r97 instrument's own `--usage-check` reads `unmet` on `N06` for `12.09.4`, `00.00.00` **and**
  `000000012.9.4` (command `python3 tools/limine-pin-battery-r97.py --usage-check --gate
  .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py --work <scratch>`; receipt
  `receipts/c1-usage-N06.txt`). So the Z class is unsampled by both legs of the
  r96 instrument, and the leading-zero class is new at roster level only.

## PC3 — a registry row's declared values are claims; a presence-only gate certifies rows, not the values a row declares

`tools/check-registry-coverage.py` certifies that every `tools/` file has exactly one operative row
and that a row's self-test flag text occurs in the tool; it never reads a row's declared values
(`tools/check-registry-coverage.py`, `_coverage()`: it consumes the row's *name*, *kind*,
*entry paths*, *verdict map* and *self-test flag*, and never the numbers the row states).
`tools/check-registry-content.py` binds **seven cell values over four rows** — the gate's argparse
default (`RC-ENTRY-DEFAULT`), its `--selftest` tally re-derived by running it
(`RC-SELFTEST-COUNT`), its JSON schema token (`RC-SCHEMA`), the r96 battery's roster size in two
cells by AST count (`RC-ROSTER-VERDICT`, `RC-ROSTER-PINNED`), the r96 calibration checker's
selftest tally (`RC-CAL-SELFTEST`) and the r96 bends generator's variant span (`RC-BEND-SPAN`)
(command `python3 -` importing the frozen `tools/check-registry-content.py` and printing
`BINDINGS`; receipt `receipts/pc3-binding-inventory.txt`; the bound rows are `limine-pins`,
`limine-pin-battery-r96`, `check-r96-calibration`, `make-r96-bends`).

At the landed revision `a57e88cd57f30bae206d908b534508d9463bf734` the checker reads
`status PASS bindings 7/7 findings 0` with 154 operative rows (command `python3
tools/check-registry-content.py --revision a57e88cd57f30bae206d908b534508d9463bf734 --json OUT`;
receipts `receipts/c2-content-landed.txt`, `receipts/c2-content-landed.json`), and its
`--selftest` reads `selftest PASS 12/12` (command `python3 tools/check-registry-content.py
--selftest`; receipt `receipts/c2-content-selftest.txt`).

On a **content-doctored** table — six content-only cell doctors, the row set, the tool set and every
path unchanged (`default `auto`` → `default `12.9.4``, `(39 fixtures` → `(88 fixtures`, `roster
103 (` → `roster 99 (`, `FAMILY_ROSTER, 103,` → `FAMILY_ROSTER, 99,`, ``--selftest` (7 cases`` →
``--selftest` (29 cases``, `r96 VARIANTS N01-N04` → `r96 VARIANTS N01-N05``) — the content
checker reads `status FAIL` with exactly **six `RC-VALUE-MISMATCH` findings**, one per doctor, each
naming its row and the value it derives from the tool's bytes, e.g. "RC-ENTRY-DEFAULT states
'12.9.4', tools/check-limine-pins.py derives 'auto'" and "RC-ROSTER-VERDICT states '99',
tools/limine-pin-battery-r96.py derives '103'" (command: `python3 <scratch clone>/fixture/
check-registry-content.py --revision <doctored rev> --json OUT` on a `git clone --shared` of the
lane with one fixture commit; receipt `receipts/c2-content-doctored-r96tip.txt`). On that same
revision the unchanged coverage gate
reads `status PASS`, `registered 154`, `rows_total 154`, `tools_total 154`, `missing 0`,
`findings []` (command `python3 <scratch clone>/tools/check-registry-coverage.py --revision
<doctored rev>`; receipt `receipts/c2-coverage-doctored-r96tip.json`) — the presence-only gate
certifies the doctored table. The same holds on a post-freeze base that carries the round's own
three registry rows: content `FAIL` with the same six findings, coverage `PASS` with `registered
157`, `findings []` (the same two commands on the second scratch clone; receipts
`receipts/c2-content-doctored-master.txt`, `receipts/c2-coverage-doctored-master.json`).
*Scope note:* at the **landed commit** `a57e88cd`
the coverage gate itself reads `FAIL` with three `REGISTRY-ROW-MISSING` findings, because the
round's three new tools are committed there while their registry rows land only at settle
(command `python3 tools/check-registry-coverage.py --revision a57e88cd57f30bae206d908b534508d9463bf734`;
receipt `receipts/c2-coverage-landed.json`; the row count and tool count at that revision are 154
and 157 — command `git ls-tree -r --name-only a57e88cd -- tools/ | wc -l`, receipt
`receipts/pc3-before-leg.txt`).

## Limits

- **The two families sample a small set of spellings, not every form.** Each family sends four
  cases per run (`CASES_PER_FAMILY = 4`, `tools/limine-pin-battery-r97.py:2001`; command
  `grep -n 'CASES_PER_FAMILY = ' tools/limine-pin-battery-r97.py`, receipt
  `receipts/limits-family-shapes.txt`), drawn from a fixed tuple: the Z family cycles two
  spellings (`12.9.999999999`, `0.9.999999999`) — each appearing twice per run — and the
  leading-zero family cycles four spellings, one per case ordinal (command: counting the distinct
  `version` per family over the three runs of the landed-gate battery JSON; receipt
  `receipts/limits-distinct-versions.txt`: Z 6 + 6 instances of its two spellings, leading-zero
  3 + 3 + 3 + 3 of its four). So the sample is four cases per member class, not
  every 9-digit third component and not every leading-zero spelling. The 10-digit out-of-bound
  member is the r94 family's `REFUSAL-VERSIONS-10DIGIT` (`REFUSAL_DIGIT10`,
  `tools/limine-pin-battery-r97.py:1678`, whose third member `0.0.1234567890` does put a ten-digit
  component in the third position), not this round's.
- **The Z bend is not single-family.** `N05-z-cap-8` also fails two `LEADING-ZERO-NORMALIZE`
  members, whose third components are 9 digits (`12.000000009.000000005` and
  `000000000.000000000.000000000`); `N06-leading-zero-reject` is the leading-zero family's own
  discriminator (command `python3 .ufo/waves/round-95/before/controls/count-runs.py OUT --family
  REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE` on each bend's battery JSON;
  receipts `receipts/c1-bend-N05-count-runs.json`, `receipts/c1-bend-N06-count-runs.json`).
- **The content checker binds 4 of the 154 operative rows** (seven cells); the other 150 rows stay
  presence-only, and a row added after the r97 freeze is not bound until a later freeze (commands:
  the frozen checker's `BINDINGS` printed by `python3 -`, and
  `python3 tools/check-registry-content.py --revision a57e88cd… --json OUT`'s `rows` field;
  receipts `receipts/pc3-binding-inventory.txt`, `receipts/c2-content-landed.json`).
- Two of the seven bindings read a **printed tally** (`RC-SELFTEST-COUNT`, `RC-CAL-SELFTEST`): a
  tool that printed `PASS N/N` without running its cases would satisfy them.
- The checker reads the highest `## Gate and probe registry — round<N> superseding current rows`
  section, like the coverage gate; append-only continuation rows outside it are not bound.
- The Z class and the leading-zero class are new at **roster** level; at instrument level the r96
  battery's `--usage-check` mode already sent two leading-zero spellings (see PC2's scope note).

{"seat":"ScribeKnowledge","verdict":"findings","notes":"Draft of the round-97 knowledge entry (L1 integrates). Provenance trio first; PC1 the third component at the 1-9-digit cap (12.9.999999999 era B, 0.9.999999999 era A; family REFUSAL-VERSIONS-9DIGIT-Z, bend N05-z-cap-8); PC2 leading zeros normalized by int() so the era follows the numeric tuple (000000012.9.4 = 12.9.4 era A, 12.000000009.000000005 = 12.9.5 era B; family LEADING-ZERO-NORMALIZE, bend N06-leading-zero-reject); PC3 a registry row's declared values are claims and the presence-only coverage gate certifies rows, not the values a row declares (check-registry-content.py binds 7 cells over 4 of the 154 operative rows). Limits name the bounded spelling sample and the 4-of-154 binding, plus four more. Every number carries its receipt and command under .ufo/waves/round-97/w1/ScribeKnowledge/receipts/ (60 files, index receipts/COMMANDS.md). The new SOURCES row is left as S### (new row this round) for the L1 to substitute."}
