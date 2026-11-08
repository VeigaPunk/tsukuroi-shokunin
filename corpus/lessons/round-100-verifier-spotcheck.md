author: hyaku closure (non-author integrator, @m_zfl)

# Round 100 — non-author verifier spot-check (tsukuroi)

Verifier: hyaku closure integrator of record for tsukuroi round 100 (fresh subagent, not the author
of this round). Lane tip at closure `23151986441fbfd8d32778b68292d955035d9341` (`master`,
`ahead=0 behind=0 tracked=0 untracked=0`), pre-round tip `ce73ccaf75d0279385977f03ccb35945c1cf8e07`.
This file is the only lane artifact the verifier writes; no lane-authored file was edited.

## 1. Step-1 conformance

| item | result | evidence / command |
|---|---|---|
| report committed by the lane identity | **pass** | `git log --format='%an %H' -- .ufo/reports/round-100/tsukuroi.md` → `tsukuroi-shokunin aee9ed82…` (correction) over `tsukuroi-shokunin 609ebc37…` (report); author e-mail `tsukuroi@shokunin.local` |
| report path / name | **pass** | `.ufo/reports/round-100/tsukuroi.md` |
| `SHONEN` heading, one line per box | **pass** | `grep -c '^## SHONEN'` = 1; `grep -cE '^- `\[[x~ ]\]`'` = 4; `SHONEN.md` has 4 boxes; all four are `[~]` (no self-attested `[x]`) |
| every cited lane commit exists and is an ancestor of the branch | **pass** | `git merge-base --is-ancestor <h> refs/heads/master` for `ce73ccaf 743ce449 60b5636f c450cd68 69474c55 ef12af4c 7961738a 9da23561 23151986` → all 9 `ancestor` (branch tested, never `@{u}`; HEAD is detached at the tip) |
| no uncommitted round work; repo pushed | **pass** | `jj-lane.sh state` → `branch=master local=23151986… remote=23151986… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty |
| prompt carries the template contract | **pass** | `.ufo/prompts/tsukuroi-round-100.md` §1 mission/axes binding, §2 1–3 claims + lowest-axis duty, §3 L2 floor (≥8 in one batched AgentSwarm call), §5 commit-then-push + push scope + L0 side channel; child items: report path (L101), commit-before-report ordering (L462-473), `SHONEN` heading (L118, L521), commit-hash citation (L106-107, L472-475), write scope (L499-511) |
| dispatch/completion digest | **pass** | `.ufo/watchdog.log` L3373 `2026-11-08T11:54:19-03:00 launch tsukuroi round=100 pgid=2232722 driver=hyaku-inline attempt=1`; L3381 `2026-11-08T12:55:57-03:00 complete tsukuroi round=100; hyaku-inline attempt=1` |
| wave shape | **pass** | `w1-results.json`: 14 seats; 13 with non-empty output, `ReviewRegistry` 0 bytes (dead at spawn, recorded `w1/ReviewRegistry-DEAD-AT-SPAWN.md`, not credited, not replaced); attack roles ReviewBends/CriticClaims/MutInstruments/SentinelHarm/ConnectorOverlap + dead ReviewRegistry = 6/14 = 42.9 % (floor 25 %); `w1-validate.err` 0 bytes |

Defects (status-neutral, named in §6): the report prose says the lesson "mines five mistakes" while
the lesson carries nine `## Mistakes` rows (its own parenthetical names seven); two residual
imprecisions stand in the round's own S396 `SOURCES.md` row; one knowledge-entry byte anchor is off
by one byte against the quoted clause.

## 2. Pre-file falsification ledger (addendum §8, Amendment 59)

`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tsukuroi --round 100`
→ `PREFILE-FALSIFICATION: pass claims=2 rows=14 attack_seats=6 findings=0`, exit **0**.

Coverage re-read from `.ufo/waves/round-100/claim-falsification.tsv` (14 rows): both claims
(`C1` 7 rows, `C2` 7 rows) and all six attack-role seats (ReviewBends, CriticClaims, MutInstruments,
SentinelHarm, ConnectorOverlap, plus the L1's `ReviewRegistry-DEAD-AT-SPAWN` record for the dead
seat). Three rows are `falsifies-wording`, each naming a narrowing — adjudicated:

| row | adjudication |
|---|---|
| C1 / ReviewBends (A2: bends cover the main return at BYTE 16931; the early `CANNOT-EVALUATE` return at BYTE 11230 still echoes true) | **not a falsification** — the frozen predicate says "each changing ONLY the returned JSON `limine_version` line" about the emitted artifact (re-derived: exactly one changed line) and "falsifies that field exactly when the FIRST/SECOND component is `999999999`" about the trigger; neither sentence claims every return path. Real observation, wording holds as narrowed |
| C1 / CriticClaims (A2 then A5: N13's payload is the fixed string `12.999999998.4`, so for `0.999999999.0` the first component also changes) | **not a falsification** — the condition (`split(".")[1] == "999999999"`) is exact; "falsifies the field when …" does not assert that only that component is rewritten. The payload detail is a named narrowing |
| C2 / CriticClaims (A6 then A7: empty separator runs are skipped; set equality against N-prefixed keys with mixed-width ranges normalised to the first token's width) | **not a falsification** — the grammar sentence constrains the allowed joins (`,`, whitespace, `;`, `+`, `/`, `and`) and an empty run carries no illegal token; my independent tokeniser reproduces set equality on all 12 frozen cells. Lenience and width normalisation are named |

No unreconciled falsifies-wording row: the ledger is present, complete, and its three rows are
reconciled by amendment text that the artifacts match.

## 3. Per-claim re-check (re-derived against the lane tip)

Every value below was computed by the verifier from committed bytes (JSON receipts, `git show`,
`diff`, `sha256sum`, a re-run of the bend generator in a scratch copy, an independent label-set
parser). Lane-owned gates and batteries were **not executed** (PROTOCOL §Gate standard,
Closure consequence); their committed evidence (frozen-run JSON, selftest tally, revision measured)
was verified instead.

### C1 — depth (declared 8, target `met as narrowed`)

Instrument bytes first: `sha256sum -c .ufo/waves/round-100/before/instruments.sha256` → 14 × `OK`
(gate `7d79ac29…`, r99 battery `c2e8c8fc…`, r98 battery `8198bd84…`, r99 checker `b489f5b8…`,
r100 checker `7a23a522…`, bend generator `7ccfe69e…`, both control copies, both pinned bends, the
fixture builder).

Re-emission (plain measurement, scratch tree: `tools/{check-limine-pins.py,make-r100-bends.py}` +
empty `.ufo/waves/round-100/before/controls/bends/`):

```
$ python3 <scratch>/tools/make-r100-bends.py
wrote …/N12-x-echo.py (30409 bytes, one clause bent)
wrote …/N13-y-echo.py (30446 bytes, one clause bent)
$ diff -u tools/check-limine-pins.py …/N12-x-echo.py   # 2 changed lines = 1 removed + 1 added
-            "limine_version": limine_version,
+            "limine_version": ("999999998.9.9" if limine_version.split(".")[0] == "999999999" else limine_version),  # N12 …
$ sha256sum …/N12-x-echo.py .ufo/waves/round-100/before/controls/bends/N12-x-echo.py
eb247e16…  (both)          # N13 likewise e1e5916f… (both)
```

No-work control: `git cat-file -e ce73ccaf:tools/make-r100-bends.py` → exit **128**
(`path … exists on disk, but not in 'ce73ccaf…'`).

Battery receipts, recomputed from `after/c1/*.json` (30 runs; `err` = `case_log` entries with a
non-null `error`):

| receipt | verdict | passed/total | error rows | failed_families |
|---|---|---|---|---|
| `gate-canonical`, `gate-clone` (×3 each) | met | 105/105 | 0 | `[]` |
| `bend-N13-y-echo-canonical`, `-clone` (×3 each) | unmet | 104/105 | 0 | `['REFUSAL-VERSIONS-9DIGIT-Y']` |
| `bend-N12-x-echo-canonical`, `-clone` (×3 each) | unmet | 103/105 | 0 | `['EXPLICIT-VERSION-ECHO', 'REFUSAL-VERSIONS-9DIGIT']` |
| `control-N13-y-echo-canonical`, `-clone` (×3 each) | met | 105/105 | 0 | `[]` (blind) |
| `control-N12-x-echo-canonical`, `-clone` (×3 each) | unmet | 104/105 | 0 | `['EXPLICIT-VERSION-ECHO']` |

Assertion sites inspected, so the reading is not merely a stored number: r99 sets `check_echo` on
`REFUSAL-VERSIONS-9DIGIT` (line 1775), `EXPLICIT-VERSION-ECHO` (1792), `REFUSAL-VERSIONS-9DIGIT-Y`
(1817), `REFUSAL-VERSIONS-9DIGIT-Z` (1840), `LEADING-ZERO-NORMALIZE` (1857); r98 sets it on only
`EXPLICIT-VERSION-ECHO`, `…-Z` and `LEADING-ZERO-NORMALIZE` — which is exactly why N13 is blind and
N12 is a one-family delta on the r98 control. **C1 verifies as declared, narrowed**: the Y leg is a
met→unmet flip, the X leg a delta (A3), and no axis byte moved (gate/battery/checker diffs empty).

### C2 — freshness (declared 9, target `met as narrowed`)

Live table, independent locator (highest `## Gate and probe registry — round<N>` heading, its unique
8-cell header, consecutive rows): `ce73ccaf` and `743ce449` → **163** rows; `69474c55` and the tip
→ **165** rows. The two added rows are `make-r100-bends` and `check-registry-content-r100`.

Binding, independent implementation (own tokeniser: `N<digits>` / `N<digits>-N<digits>`, ranges
expanded, separators `,` `;` `+` `/` `and` whitespace):

```
SPACE/SEMICOLON/AND/SLASH/PLUS -> {N01,N02,N03} == fixture VARIANTS keys        -> bind
UNION "N01-N02,N04-N05"        -> {N01,N02,N04,N05} == fixture keys             -> bind
LETTER "N01a-N03" / PROSE "… through …"  -> parse refused                       -> fail closed
UNION-LIE "N01-N04,N05" vs {N01,N02,N04,N05} -> set mismatch                   -> fail closed
HYBRID    "N01-N04,N05" vs {N01,N02,N03,N04} -> set mismatch                   -> fail closed
GAP "N01,N03" vs {N01,N03}                                                     -> pass
live cell5 "r96 VARIANTS N01-N04" -> {N01..N04} == tools/make-r96-bends.py keys
```

Committed evidence verified: `after/c2/selftest-r100.txt` = `selftest PASS 26/26` (25 `SELFTEST_CASES`
+ the `ancestor` git case, counted in source), `selftest-r99.txt` = `PASS 17/17` (16 + `ancestor`);
`content-tip.json` = `PASS`, `bindings 7`, `rows 165`, findings 0 at `69474c55`; `content-tip-r99.json`
= `PASS 7/7`; `coverage-tip.json` = `PASS`, findings 0, branch tip `69474c55`; `fixtures.txt` = 12/12
readings (six acceptance cells none on r100 vs a finding on r99; five forged cells a finding on both;
`GAP` none on both).

One observation, not a defect: `HYBRID` reads `RC-CELL-MISSING` on the r99 control and
`RC-VALUE-MISMATCH` on r100 — the frozen target's "unchanged or sharper" covers it, and the committed
fixture receipt shows the move, so the kill rule ("an id other than the frozen one") is satisfied by
the r100 id.

**C2 verifies as declared, narrowed** (A6 empty-run lenience, A7 set-vs-keys width).

## 4. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth | **improved** | the gate's `check_echo` legs are now proven per spelling by a committed one-clause article: Y `104/105` exactly `[REFUSAL-VERSIONS-9DIGIT-Y]` where the r98 control is blind, X `103/105` exactly `[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]` (delta of one family); both bends reproduce byte-identically; the lane conservatively scores 8 → 8 (no ordinal uplift claimed) |
| freshness | **improved** | `RC-BEND-SPAN` is a label set; six cells the r99 control rejects now bind, five forged shapes stay closed, selftest 17 → 26; live table 165 rows `PASS 7/7` at both tips |
| coverage | unchanged | two new tools, both registered (`make-r100-bends`, `check-registry-content-r100`); coverage gate receipt `PASS 165/165/165`, my own row count 163 → 165; no surface lost |
| operability | unchanged | the generator runs (re-executed here, rc 0, deterministic bytes); both rows carry entry command, verdict map, self-test and write scope; no claimed operability move |
| calibration | unchanged | SHONEN boxes left `[~]`, SCORECARD rows match observed state, four of the round's own defects disclosed raw (7-cell row, tool-without-row, manifest scope, brief example); no overreach carried into the claims |
| adjacency | unchanged | `PROVINCE.md` byte-identical; `ConnectorOverlap` found no sibling instrument or label-set binder; the kaidoku/revenger reverse-engineering ownership stays operator-owned and unruled (carried, §6) |

No owned axis is harmed: `git diff --numstat ce73ccaf 23151986` over `SCORECARD.md` `50/0`,
`LOG.md` `38/0`, `SKILL.md` `18/0`, `corpus/QUALITY.md` `3/0`, `corpus/SOURCES.md` `3/0`,
`corpus/README.md` `25/0`, the knowledge entry `97/0` and the lesson `133/0` (all additions);
`PROVINCE.md`, `SHONEN.md`, `tools/check-limine-pins.py`, `tools/limine-pin-battery-r98.py`,
`tools/limine-pin-battery-r99.py`, `tools/check-registry-content-r99.py` show no diff at all.

## 5. Discernment spot-check (LEARNING.md §"Discernment is checked from outside")

`corpus/lessons/round-100.md` §Gate, rows re-opened 2026-11-08 by this verifier (network fetches on
the verifier host; the lane's own-work row re-measured on the pinned bytes).

| item | decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| S397 — CPython `re` docs, tier A | **admit** | `https://docs.python.org/3/library/re.html`, HTTP 200, 257722 bytes, sha256 `69d64759…` (identical to the row) | **agree** | `bytes.find(b'If the whole <em>string</em> matches the regular expression <em>pattern</em>')` = **112171**, exactly the row's offset; rendering strips to `If the whole string matches the regular expression pattern, return a corresponding Match.` (13 words); `id="re.fullmatch"` at **111489**; the `\b` sentence is present. The corrected quote is verbatim (the earlier "match object" wording is absent — `bytes.find` → −1; `match object` occurs only at 57156-adjacent table cells) |
| S398 — Limine v12.9.6 `CONFIG.md`, tier C | **reject** | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md`, HTTP 200, 27609 bytes, sha256 `f44f3a19…` | **agree** | `grep -c` for `limine_version`, `visibility_era`, `echo`, `version` → **0/0/0/0**, as the row states; the page documents config keys and states nothing about the gate's reported JSON fields or the battery's families. The flip condition is well-formed |
| S396 — own-work instruments, tier A | **admit** (with a named row defect) | `tools/make-r100-bends.py` (`7ccfe69e…`), `tools/check-registry-content-r100.py` (`7a23a522…`) | **agree** on the decision | both anchors resolve: `bytes.find(b'"limine_version": ("999999998.9.9"…')` = 2615, the N13 clause at 3365 (lie literal 3384), `def parse_label_set` = 12134, `TOKEN`/`SEPARATORS` = 12025/12073; the row grounds both instruments the round relies on. The row's *wording* is defective: "emission lines at BYTE 2615 (N12) and BYTE 3384 (N13)" labels 3384 an emission-line start when it is the lie literal inside the N13 line (line start 3344, clause start 3365), and its `teaches` cell says "exactly the family" where the X leg's measured set is two families — both disclosed in the lesson's append-only correction, neither swept from the row (see §6) |

Census (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`):
`ok … corpus/SOURCES.md`, **exit 0**, 57 W04 + 1 W01 warnings, 0 errors; `grep -cE '^\\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` = **398** — identical to the report's before (395, exit 0) → after (398, exit 0).

## 6. Trend verdicts

| trend | verdict | evidence |
|---|---|---|
| expansion | **improved** | two admitted mined rows on ground the map did not hold (S396 own-work instruments with byte anchors, S397 the `re` primitives the tokeniser depends on), one kept rejection with its flip (S398), one knowledge entry (`limine-echo-bends-r100.md`) whose `source:` cites both rows; census 395 → 398, exit 0 both ends |
| quality | **improved** | a shape the r99 instrument could not see now fails closed (Y flip `met 105/105` → `unmet 104/105` exact, six registry cells bind, selftest 17 → 26, mutation kills M1–M6/M8 by named cases); QUALITY 142 added from a harness fault the round itself produced; no admitted entry fails its re-check — all three rows and the knowledge entry re-opened, instrument bytes unchanged |
| discernment | **improved** | this non-author spot-check agrees with the gate on the sampled admit (S397) and reject (S398); the wave narrowed the round's own wording before filing (A2–A7, including the X-delta overstatement) and two corpus precision defects were re-measured and corrected append-only; the surviving row-level defect is on record with the correct offsets and is routed below |

No trend is harmed. Growth is not traded for quality: depth/freshness rose while the gate, both
control batteries and the r99 checker held their bytes.

## 7. Routed defects (lane must fix; status-neutral)

1. **R100-VER-1 — S396 anchor unit mismatch (row left standing).** `corpus/SOURCES.md` S396 says
   "generator emission lines at BYTE 2615 (N12) and BYTE 3384 (N13)"; 3384 is the N13 *lie literal*,
   the emission clause starts at **3365** (line 3344). The lesson's append-only correction names the
   right pair, but S396 was written this round, and PROTOCOL §Evidence standard ("corrections sweep
   every mention") requires the corrected fact not to stand superseded in a file the round touched.
   Fix next round: rewrite S396's anchor cell to 2615/3365 (or add S399 and mark S396 superseded).
2. **R100-VER-2 — S396 `teaches` says one family where the measurement is two.** X reads
   `[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]`; the cell's "exactly the family" reads as
   singular. Same fix vehicle as R100-VER-1.
3. **R100-VER-3 — report prose count.** `.ufo/reports/round-100/tsukuroi.md` L53 says the lesson
   "mines five mistakes"; `grep -cE '^- \\*\\*[A-Z0-9]' corpus/lessons/round-100.md` = **9**, and the
   sentence's own parenthetical names seven. Filed bytes stay; append an erratum in the next round's
   report or lesson naming the superseded sentence.
4. **R100-VER-4 — knowledge-entry byte anchor off by one.** `corpus/knowledge/limine-echo-bends-r100.md`
   §1 cites the gate's `limine_version` emission "at BYTE 16931"; 16931 is the newline before the
   clause, the quoted clause starts at **16932** (and the generator anchors in the same entry use a
   first-content byte, 2615). Re-measure with the quote's first byte under QUALITY 141 and correct the
   cell (append-only note if the entry is treated as frozen).
5. **Carried (operator-owned, not a lane defect).** `adjacency` (8, tied lowest) carried no claim this
   round: the kaidoku/revenger reverse-engineering ownership stays unruled, exactly as the declaration
   states. Depth, the other tied-lowest axis, carried C1, so the lowest-axis obligation is met.
   Promotion: all four `SHONEN` boxes are now supported by evidence a non-author can
   re-execute (this file); writing `[x]`, deleting `SHONEN.md` and bumping `MANIFEST.json` remain
   operator work.
