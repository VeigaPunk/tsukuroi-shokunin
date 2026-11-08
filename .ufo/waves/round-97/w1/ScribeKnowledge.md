# ScribeKnowledge — round 97, wave w1 (scoped findings)

Seat: scribe (leaf member, no dispatch). Scope: draft the round's knowledge entry (prose only) and
carry the receipts for it.

- **Draft:** `.ufo/waves/round-97/w1/ScribeKnowledge/limine-bound-9digit-z-r97.md` — the draft of
  `corpus/knowledge/limine-bound-9digit-z-r97.md`: the CORPUS provenance trio (`source:`,
  `verified-at:`, `recheck:`), three proposition sections each naming its family and its bend
  (PC1 `REFUSAL-VERSIONS-9DIGIT-Z` / `N05-z-cap-8`; PC2 `LEADING-ZERO-NORMALIZE` /
  `N06-leading-zero-reject`; PC3 `tools/check-registry-content.py`'s seven bindings and the
  presence-only coverage gate), and a Limits section carrying the two required disclosures (the
  families sample a bounded set of spellings, not every 9-digit / leading-zero form; the content
  checker binds 4 of the 154 operative rows) plus four more.
- **Seat report with commands, raw output and the PASS/FAIL table:**
  `.ufo/waves/round-97/w1/ScribeKnowledge/report.md`
- **Receipts:** `.ufo/waves/round-97/w1/ScribeKnowledge/receipts/` (60 files)

## What this seat measured (own runs, own receipts)

| leg | measured | verdict |
|---|---|---|
| roster | 105 unique families (AST count of `FAMILY_ROSTER`), the last two `REFUSAL-VERSIONS-9DIGIT-Z` and `LEADING-ZERO-NORMALIZE` | PASS |
| landed gate, 3 runs | `met 105/105`, `failed_families []`, 0 error rows, each new family `[4, 0]` | PASS |
| per-case answers | `12.9.999999999` → rc 1 `DEGRADED` era-answer `panic`; `0.9.999999999` → rc 1 `DEGRADED` era-answer `prompt`; `12.09.4` / `000000012.9.4` → `prompt`; `12.000000009.000000005` → `panic`; `000000000.000000000.000000000` → `prompt` | PASS |
| `N05-z-cap-8`, 3 runs | `unmet 103/105`, `["LEADING-ZERO-NORMALIZE","REFUSAL-VERSIONS-9DIGIT-Z"]`, **6 error rows per run** (4 Z + 2 LZ), all the bend's own `JSONDecodeError rc=64` | PASS |
| `N06-leading-zero-reject`, 3 runs | `unmet 104/105`, `["LEADING-ZERO-NORMALIZE"]`, **4 error rows per run**, same rc-64 class | PASS |
| r96 do-nothing battery, 3 runs × landed gate and both bends | `met 103/103`, 0 error rows (blind to both new families) | PASS |
| parser probe (frozen gate, read-only import) | `12.9.999999999`→(12,9,999999999) `12.9.5+`; `0.9.999999999`→(0,9,999999999) `pre-12.9.5`; `12.09.4`→(12,9,4); `000000012.9.4`→(12,9,4); `12.000000009.000000005`→(12,9,5) `12.9.5+`; `000000000.000000000.000000000`→(0,0,0) | PASS |
| content checker, landed revision `a57e88cd` | `status PASS`, `bindings 7/7`, `findings []`, 154 rows | PASS |
| content checker `--selftest` | `selftest PASS 12/12` | PASS |
| doctored table (six content-only cell doctors, re-derived in scratch) | content `FAIL` with exactly six `RC-VALUE-MISMATCH` findings, one per doctor, each naming its row and the derived value | PASS |
| coverage gate on the doctored revision | `PASS`, `registered 154`, `rows_total 154`, `tools_total 154`, `findings []` (pinned base `f48d1642`); `PASS registered 157 findings []` on the settled-rows base | PASS |
| gate selftest | `selftest PASS 39/39` | PASS |
| source re-opens | S389 `stdtypes.html` 815447 B `6bf2ce2b…` (the 4300-digit sentence at byte 785297); S391 `sys315.html` 280632 B `a7e00587…` (the default-value sentence at byte 157851); `int-functions.html` 331022 B `d92580dd…` ("have leading zeros" at byte 157767, "Base 0 also disallows leading zeros: int('010', 0) is not legal, while int('010') and int('010', 8) are." at byte 159303) | PASS |

## Findings (reported, not edited — the instruments are frozen)

1. **The r96 blindness is roster-level, not instrument-level.** The r96 `--usage-check` mode
   already sends `12.09.4` and `00.00.00` and reads `unmet` on `N06-leading-zero-reject` on those
   two rows, so `LEADING-ZERO-NORMALIZE` is new at roster level only; the **Z** class is unsampled
   by both r96 legs. The draft carries this as PC2's scope note and a Limits bullet (the L1's
   amendment A3 records the same narrowing).
2. **The coverage gate reads `FAIL` at the landed commit `a57e88cd`** with three
   `REGISTRY-ROW-MISSING` findings: the round's three new tools are committed while their registry
   rows land only at settle. The blindness leg is therefore read on a doctored revision, which the
   draft states in PC3's scope note (same ground as amendment A4).
3. **The freeze manifest's single FAILED line is the doctored-fixture *recipe*, not an instrument**
   any claim reads (19 OK / 1 FAILED; amendment A1 pins the corrected set separately). The recipe
   was not run; the doctored table was re-derived in scratch.
4. **The new SOURCES row's byte anchors do not match its own pin.** `id="int"` is at byte 153202,
   not 153028 (byte 153028 is inside `builtins.input/result`), and the row's quoted phrase occurs
   0 times in the pin ("radix string" occurs 0 times). The real anchors are 157767 and 159303. The
   draft cites the corrected bytes; the corpus row's anchor cells are the L1's to fix.
5. **The plan's "four spellings per class" limit is looser than the measurement.** Each family
   sends four cases per run, but the Z family draws them from two distinct spellings (each twice)
   while the leading-zero family draws four (one per ordinal). The draft states the measured
   shape, so no universal is claimed that the instrument does not send.

## Relation to the entry the L1 already wrote

The L1 wrote `corpus/knowledge/limine-bound-9digit-z-r97.md` in the worktree while this seat
worked. The draft agrees with it on every clause I could measure and adds (a) the S-id placeholder
`S### (new row this round)` with the corrected byte anchors for the L1 to substitute, (b) the
r96-instrument-level scope of the leading-zero class, and (c) the coverage gate's landed-commit
reading.

## Constraints honoured

Only `.ufo/waves/round-97/w1/ScribeKnowledge/` (this trailer's seat dir: draft, report, receipts)
and the scratch root `/fast/scratch/hyaku/tsukuroi-r97/ScribeKnowledge` were written; the scratch
tree was deleted before the report. No lane file was edited — `tools/`, `SKILL.md`, `corpus/`,
`SCORECARD.md`, `LOG.md`, `.ufo/plans/`, `.ufo/waves/round-97/before/` and `claims.json` are
untouched by this seat. `tools/make-r97-bends.py` and every earlier `make-r*-bends.py` were **not**
run; every bend used is the frozen copy under `before/controls/bends/`, and the doctored table was
re-derived in scratch with each of the six substitutions asserted to match exactly once. The only
commits made were inside two scratch clones, each after `git -C <clone> rev-parse --show-toplevel`
printed that clone's own path, with the fixture identity only. No git or jj mutation in the lane
repo; no tool installed or upgraded; no subagent dispatched.

{"seat":"ScribeKnowledge","verdict":"findings","notes":"Draft at .ufo/waves/round-97/w1/ScribeKnowledge/limine-bound-9digit-z-r97.md; seat report and 60 receipts under the seat dir (index receipts/COMMANDS.md). Own measurements confirm the frozen shape: landed gate 105/105 met x3 (0 error rows, each new family [4,0]); N05-z-cap-8 103/105 unmet with failed_families exactly [LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z] and 6 rc-64 refusal rows per run; N06-leading-zero-reject 104/105 unmet with failed_families [LEADING-ZERO-NORMALIZE] and 4 rc-64 rows per run; r96 do-nothing 103/103 met x3 on the landed gate and on both bends (blindness); parser probe confirms int() normalization (000000012.9.4 = 12.9.4 era A, 12.000000009.000000005 = 12.9.5 era B); content checker PASS bindings 7/7 findings 0 at a57e88cd and selftest 12/12; the doctored table reads exactly six RC-VALUE-MISMATCH findings while the coverage gate reads PASS 154/154 findings 0 (pinned base) and PASS 157/157 (settled rows). Five findings: the r96 --usage-check already sent 12.09.4 and 00.00.00 so the leading-zero class is new at roster level only and the Z class is unsampled by both r96 legs (A3 agrees); the coverage gate reads FAIL with three REGISTRY-ROW-MISSING at the landed commit until the three registry rows land at settle (A4 agrees); the manifest's single FAILED line is the doctored-fixture recipe, not an instrument, and the fixture was re-derived in scratch rather than run; the new SOURCES row's byte anchors do not match its own pin (id=\"int\" at 153202 not 153028, the quoted phrase occurs 0 times; the real anchors are 157767 and 159303) and the draft cites the corrected bytes; and the plan's 'four spellings per class' limit is looser than the measurement (the Z family draws its four cases from two spellings, the leading-zero family from four), so the draft states the measured shape. The new row's id is left as S### for the L1 to substitute."}
