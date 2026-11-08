# The third component's cap, the accepted leading-zero form, and a registry row's declared values

source: `corpus/SOURCES.md` S392 (CPython `int()` documentation, opened 2026-11-08; the string form
of `int(x, base)` accepts leading zeros for an explicit base and base 0 does not), S389 (CPython,
integer string conversion length limitation, opened 2026-11-08) and S391 (CPython,
`sys.int_info.default_max_str_digits`, opened 2026-11-08; supersedes S390);
own-work: `tools/check-limine-pins.py` `parse_limine_version()` / `--selftest`,
`tools/limine-pin-battery-r97.py` (families named below) and `tools/check-registry-content.py`
(the seven bindings below).
verified-at: 2026-11-08 (round 97; the instruments are pinned in
`.ufo/waves/round-97/before/instruments.sha256`).
recheck: `python3 tools/limine-pin-battery-r97.py --gate tools/check-limine-pins.py --runs 3
--json OUT` (verdict `met`, `families_total 105`); `python3 tools/check-limine-pins.py --selftest`
(`PASS 39/39`); `python3 tools/check-registry-content.py --revision <REV>` (`status PASS`,
`bindings 7`).

## PC1 — the 1-9-digit cap is a bound on every component, and the third is the last uncertified leg

`tools/check-limine-pins.py` accepts a `--limine-version` only as three ASCII-digit components of
1-9 digits each (`parse_limine_version()`), because handing an unbounded component to `int()` raises
above CPython's decimal-conversion digit limit (S389's 4300-digit default, whose configured value
S391 names). The bound is **per component**: r95 certified the X leg (`999999999.9.9`) and r96 the Y
leg (`12.999999999.4`, `0.999999999.0`), while r96's own wave measured the Z leg uncertified —
`M06-z-cap-8` (a gate whose Z bound is `<= 8`) survived `103/103`
(`.ufo/waves/round-96/w1/MutBound.md`). Round 97's family `REFUSAL-VERSIONS-9DIGIT-Z` sends
`12.9.999999999` (era B) and `0.9.999999999` (era A): both are in-bound, so the gate must answer a
verdict (rc 1 on the fixture's mismatch pin) in the era the whole tuple selects, and the bend
`N05-z-cap-8` now reads `103/105` unmet with the family named. The same bend also refuses two
members of `LEADING-ZERO-NORMALIZE` (their third components are 9 digits), which is the coupling the
family sets record.

## PC2 — a leading-zero component is a legal decimal spelling, not a second grammar

S392 documents `int(x, base)`'s string form as optionally carrying "leading zeros" for an explicit
base, and records that base 0 disallows them. `parse_limine_version` splits on `.`, requires each
component to be ASCII digits of 1-9 characters and converts with `int()`, so a component written
`09`, `000000012` or `000000009` is the same number as its short form and the era follows the
numeric tuple: `12.09.4` and `000000012.9.4` are 12.9.4 (era A), `12.000000009.000000005` is
12.9.5 (era B), and `000000000.000000000.000000000` is 0.0.0 (era A). Round 97's family
`LEADING-ZERO-NORMALIZE` sends one member per case; a gate that refuses a component whose first
digit is `0` reads `104/105` unmet (`N06-leading-zero-reject`), and the r96 roster is blind to the
same bend (`103/103` met). Scope: the r96 instrument's `--usage-check` mode already sends `12.09.4`
and `00.00.00`, so at instrument level this class was sampled before r97 and is new at roster level
only (A3); the Z class is unsampled by both r96 legs.

## PC3 — a registry row's declared values are claims, and a presence check does not read them

`tools/check-registry-coverage.py` certifies that every `tools/` file has exactly one operative row
and that a row's self-test flag text occurs in the tool; it does not read a row's declared values.
Round 95's wave measured a real table with `limine-pins` reading `default 12.9.4` and `88 fixtures`
still reading `PASS 151/151` (`.ufo/waves/round-95/w1/ExecRegistry.md` §6), and round 96 repeated the
finding. `tools/check-registry-content.py` binds seven cells over four rows — the gate's argparse
default, its `--selftest` tally re-derived by running it, its JSON schema token, the r96 battery's
roster size in two cells by AST count, the r96 calibration checker's selftest tally, and the r96
bends generator's variant span — and reads `FAIL` with one `RC-VALUE-MISMATCH` per doctored cell on a
revision whose table the coverage gate still certifies `PASS 154/154`.

## Limits

- The two new families sample four spellings per class, not every 9-digit Z form or every leading-zero
  form; `LEADING-ZERO-NORMALIZE` cycles four members over four cases.
- The Z bend is not single-family: it also fails two `LEADING-ZERO-NORMALIZE` members. `N06` is that
  family's own discriminator.
- `check-registry-content.py` binds 7 cells of 4 rows. Measured decomposition of the other 150 rows
  at the 154-row table (`w1/ScoutDrift/report.md` §3): 21 carry a cell whose shape a BINDINGS
  capture matches, 15 of those re-derive today, and 11 are machine-checkable but unbound; even
  inside a bound row only the captured value is checked (its verdict map, write scope and prose are
  not — `w1/ReviewRegistryContent/receipts/02b-content.json`). A row added after the r97 freeze is
  not bound until a later freeze.
- The checker compares committed cell text to committed tool bytes at the SAME revision, so a tool
  and its cell doctored together read PASS (`receipts/02c-content.json`); it measures drift between
  the table and the tools, never the honesty of a tool.
- Its two `selftest_total` bindings read a printed tally; a tool whose `--selftest` prints `PASS N/N`
  without running cases satisfies them (`receipts/02d-content.json`).
- The checker's own selftest does not exercise the non-contiguous `VARIANTS` branch: a mutant that
  compares only the first label survives all three legs (`w1/MutRegistry.md` M08) — routed to r98.
- The two new families assert acceptance and the era's pin answer, not the JSON `visibility_era`
  field and not the echoed `limine_version`: a gate that answers `panic` but reports `pre-12.9.5`
  for `12.9.999999999`, and one that echoes `12.9.4` for `12.09.4`, each read `met 105/105` ×3
  (`w1/ReviewBattery/attack-1-field.txt`, `attack-2.txt`; A7). `check_era`/`check_echo` on these
  families are r98 candidates.
- The checker reads the highest `## Gate and probe registry — round<N> superseding current rows`
  section, like the coverage gate; append-only continuation rows outside it are not bound.
