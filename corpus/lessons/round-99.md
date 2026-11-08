# Round 99 lesson — tsukuroi lane

Round 99 (attempt 1), pre-round tip `f107da3afe511f7db8cdc30235a992b774903158`. Claims: C1
(depth 8) `tools/limine-pin-battery-r99.py` — the X-cap `REFUSAL-VERSIONS-9DIGIT` and the Y-cap
`REFUSAL-VERSIONS-9DIGIT-Y` set `check_echo`/`check_era`, and `LIE_KINDS` gains `limine-version`
and `visibility-era`; C2 (freshness 9) `tools/check-registry-content-r99.py` — the guarded
`RC-BEND-SPAN` capture with the `unique` mark and the `span-hybrid`/`span-restated`/`ancestor`
selftest cases (14 -> 17).

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

| row | source opened 2026-11-08 | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S395 (new, own-work) | `tools/limine-pin-battery-r99.py` and `tools/check-limine-pins.py` at this round's working tree (gate sha256 `7d79ac29…`, battery sha256 `c2e8c8fc…`) | A | `if c.check_echo and not (got[8] == c.version and got[9] == "flag")` (BYTE 99430, line 2181); era assertion at BYTE 99523 (line 2183); `def meta_ok` at BYTE 99305 (line 2179) | **admit** — the row's anchor names both assertion sites plus the five `check_echo` and five `check_era` assignment sites and the gate's two emission sites (BYTEs 16931 / 17037, early return 11230 / 11344); measurement is at the byte level (QUALITY 141) |
| S392 (re-open) | https://docs.python.org/3/library/functions.html#int | A | the r98 pin's three offsets re-measured byte-identically; the page still states an explicit base accepts leading zeros | **admit** (re-open, no drift) — cited by the entry for the leading-zero spelling's legality |
| rejected candidate | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md | — | HTTP 200 with zero occurrences of `limine_version`, `visibility_era` and `echo` (r98 measurement, unchanged this round) | **reject** — the page documents config keys; it states nothing about the gate's reported fields, so it grounds no proposition of this round |

Census (frozen command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi`): before — `git show f107da3a:corpus/SOURCES.md | grep -cE
'^\|[[:space:]]*S[0-9]{3,}'` → **394**; round start exit 0. After — the landed tree → **395 rows**,
exit **0** (the standing 57 W04 + 1 W01 warning set, 0 errors). Receipt:
`.ufo/waves/round-99/before/census-before-after.txt`. Rows added by tier: one A (own-work, S395).
Rows touched old→new in place: S395 `status` `queued` → `mined` and `used-by` `—` → the two paths
below, both logged in the in-place table. Frontier rows advanced: the r98 Frontier's Y-cap field
fidelity and X-cap field fidelity bullets, and the r98 scoreboard's lie-kind structural gap.

### In-place registry changes (old → new)

| row | field | old | new |
|---|---|---|---|
| S395 | status | `queued` | `mined` |
| S395 | used-by | `—` | `corpus/knowledge/limine-metadata-cap-families-r99.md, corpus/lessons/round-99.md` |

## Mistakes

- **R99-TWIN-BEND** — class: `vacuous`. A near-miss control that the do-nothing instrument already
  rejects witnesses the predecessor, never the round. The drafted third bend `N10-z-echo` (echoed
  `limine_version` falsified for the Z spellings) was measured against the r98 do-nothing battery and
  read `unmet 104/105` with `failed_families [REFUSAL-VERSIONS-9DIGIT-Z]`
  (`.ufo/waves/round-99/before/dev/c1-N10-twin-r98-control.json`), because round 98 had already set
  `check_echo` on that family; the bend was dropped from `tools/make-r99-bends.py` before the freeze
  so the round's roster changes nothing but would have counted a control it did not make.
  Captured-by: QUALITY 136 ("a family whose expected answer does not change under any committed
  bend is not a closure, and a family that only re-answers a case the old roster already covered is
  a twin") — the rule existed and this round applied it before the freeze, not after. Fix: the
  freeze carries the twin's reading as a receipt and the ledger names it; the instrument's docstring
  says a Z-echo bend was dropped and why.
- **R99-X-LIMIT-DELTA** — class: `scope`. A named limit can close as a *delta* rather than a flip,
  and the claim must say which. The r98 Frontier's X-cap bullet said the X leg "rides on one
  `EXPLICIT-VERSION-ERA` case". The committed bend `N11-x-era` (era label swapped when the FIRST
  component is `999999999`) therefore reads `unmet 104/105` on the r98 control — one family,
  `EXPLICIT-VERSION-ERA` — and `unmet 103/105` on r99, adding `REFUSAL-VERSIONS-9DIGIT`. Counting
  that as a met-to-unmet closure would have overstated the round by one family. Captured-by: QUALITY
  125 (every clause of a predicate maps to a family whose expected answer changes) read together
  with QUALITY 136; the lane had no rule that a closure's *direction* must be named. Fix: the
  declaration's C1 target states "N11 103/105 unmet ... exactly `[EXPLICIT-VERSION-ERA,
  REFUSAL-VERSIONS-9DIGIT]`" and this row states the delta; the DO-nothing leg for N11 is the
  receipt that makes the delta visible.

- **R99-SEAT-HARM-PARENT-DELETE** — class: `landing` (seat-to-seat harm). A seat deleted not only
  its own scratch dir but the shared parent `/fast/scratch/hyaku/tsukuroi-r99`, wiping six sibling
  seats' and the lane's `dev` scratch dirs mid-round (four were re-created by their seats within a
  minute; `ConnectorOverlap`, `MutRegistry` and `dev` were not). Evidence:
  `.ufo/waves/round-99/w1/CriticClaims.md` §7b (seat disclosure with the command and timestamp);
  no committed receipt was lost, because every receipt this round cites had already been copied into
  the seat dir or `before/`. Captured-by: PROTOCOL §7 (scratch discipline: "a seat removes its
  scratch dir before it yields") names the directory but not the delete's *scope*; the lane had no
  rule that a recursive delete must be scoped to `/<SeatName>`. Fix: the rule below, plus the
  amendment A6 record.

- **R99-LIEKIND-ROSTER-SCOPED** — class: `scope`. A selftest lie kind certifies that an instrument
  notices a *field* lie somewhere, never that a named family asserts the field. With both metadata
  assertions removed from the r99 battery, the `limine-version` and `visibility-era` legs still read
  `unmet 100/105` and `98/105`; the discrimination is supplied by the r98-carried Z/LZ/EXPLICIT
  assertions (`.ufo/waves/round-99/w1/ReviewBattery.md` wording finding 1;
  `.ufo/waves/round-99/w1/CriticClaims/receipts/17-*`). Captured-by: none — the lane's rule set had
  no sentence distinguishing a *kind* (falsify field F) from a *family* (assert field F on its own
  cases); QUALITY 128 governs per-family certifying draws, not the lie-kind layer. Fix: the lesson
  and the entry's §4-§5 state the split, and C1's verdict credits the lie kinds only with "a field
  lie is now a selftest kind".
- **R99-ROSTER-FINITE** — class: `scope`. The battery is a finite roster, so a gate that lies only
  off-roster still reads `met 105/105`: the r99 wave's W1 forgery echoes correctly only for the
  roster's spellings and W2 selects the era from the first component as text, and both pass
  (`.ufo/waves/round-99/w1/ReviewBattery.md` wording finding 3). Captured-by: QUALITY 128 (a family
  presents its own discriminating element) — it governs the family's cases, not the gap between the
  roster and the input space. Fix: named as a limit in the entry and in README's round-99 frontier;
  widening the roster is r100's work.
- **R99-TWIN-RECEIPT-ABSENT** — class: `reference-drift`. A frozen declaration cited
  `before/dev/c1-N10-twin-r98-control.json`, but the L1's copy step landed no such file (a wrong
  source name plus a swallowed error), so a claim's cited receipt did not exist when the round was
  filed. Captured-by: QUALITY 127's sweep discipline is about superseded sentences, not about
  cited-file existence; the instrument is the wave's own `grep -abo` sweep
  (`w1/ScribeLesson/receipts/17-twin-receipt-existence.txt`). Fix: the measurement was re-derived by
  `ScribeLesson` and the receipt now exists at that path, copied byte-exact from the seat's
  committed JSON (amendment A9); the plan's pointer is repaired by sidecar, never by editing the
  frozen bytes.

## Seat harm (this round)

| who | what | when | evidence | effect |
|---|---|---|---|---|
| `CriticClaims` | `rm -rf /fast/scratch/hyaku/tsukuroi-r99` (shared parent) | 2026-11-08 ~11:23–11:24 -0300 | `w1/CriticClaims.md` §7b | six sibling scratch dirs + lane `dev` deleted; four re-created; no committed receipt lost |

Rule that follows (for every later round's wave context): *a seat deletes only
`/fast/scratch/hyaku/tsukuroi-r<NN>/<SeatName>` and asserts the path it is about to remove ends in
`/<SeatName>` before running the delete; a shared parent is never removed by a seat.*

## Counter-attack scoreboard (QUALITY 115)

`w1/` = `.ufo/waves/round-99/w1/`. Direction: a mutant is killed when a leg's reading moves away
from the frozen expectation (r98 R98-MUTANT-DIRECTION-READ).

| claim | attack fielded | receipt | outcome |
|---|---|---|---|
| C1 | Y-only era lie, r99 and r98 control, both layouts | `ExecBends/c1-bend-N09-*`, `ExecDoNothing/dn-n09-*` | killed on r99 (`104/105`, exactly the Y family); control blind (`met 105/105`) |
| C1 | X-cap era lie, r99 and r98 control, both layouts | `ExecBends/c1-bend-N11-*`, `ExecDoNothing/dn-n11-*` | killed on r99 (`103/105`, two families); control sees one family (`104/105`) — the delta |
| C1 | blanket echo lie (new lie kind) | `ExecGateRuns/c1-lie-limine-version.json` | killed — `unmet 93/105`, X/Y/Z/LZ named |
| C1 | blanket era lie (new lie kind) | `ExecGateRuns/c1-lie-visibility-era.json` | killed — `unmet 95/105`, X/Y/Z/LZ named |
| C1 | X echo flag removed (M1) | `MutRegistry/receipts/M1-*` | **survives** the two bends; killed only by the constructed E1 echo bend (not committed) |
| C1 | X era flag removed (M2) | `MutRegistry/receipts/M2-N11-run.txt` | killed — N11 `104/105 [EXPLICIT-VERSION-ERA]` vs frozen `103/105 [E, X]` |
| C1 | Y echo flag removed (M3) | `MutRegistry/receipts/M3-*` | **survives** the two bends; killed only by the constructed E2 echo bend |
| C1 | Y era flag removed (M4) | `MutRegistry/receipts/M4-N09-run.txt`; `ReviewBattery-9/receipts/mut-Md-y-era-on-N09.json` | killed — N09 reads `met 105/105` where the frozen leg is `unmet 104/105` |
| C1 | lie arm / kind removal (M5-M8) | `MutRegistry/receipts/M5-selftest.txt` … `M8-selftest.txt` | **survives** — any wrapper reads `unmet`, and the reference case list is derived from `LIE_KINDS` |
| C1 | off-roster forgeries W1/W2 | `ReviewBattery.md` wording findings 3-4 | **survives** (`met 105/105`) — roster-finite field closure (A8) |
| C2 | hybrid cell | `ExecRegistry/fx-{r98,r99}-hybrid.json` | killed — r98 `PASS`, r99 `FAIL RC-CELL-MISSING` |
| C2 | same-cell restatement | `ExecRegistry/fx-{r98,r99}-restated.json` | killed — r98 `PASS`, r99 `FAIL RC-CELL-AMBIGUOUS` |
| C2 | M07 ancestor check skipped | `ExecRegistry/m07-on-{r98,r99}-selftest.txt` | killed — r99 `FAIL 16/17` (only `ancestor`), r98 `PASS 14/14` |
| C2 | 28 forged cells and guard breaks | `ReviewRegistry.md` §2; `CriticClaims/receipts/10-xv*` | 8 shapes newly rejected; **5 classes still PASS** (A1) |
| C2 | boundary guard removed (C1) | `MutRegistry/receipts/C1-selftest.txt` | killed — selftest `FAIL 16/17`, `span-hybrid` red |
| C2 | `unique` mark removed (C2) | `MutRegistry/receipts/C2-selftest.txt` | killed — selftest `FAIL 16/17`, `span-restated` red |
| C2 | ambiguity branch removed (C3) | `MutRegistry/receipts/C3-selftest.txt` | killed — observationally identical to C2 on every leg |
| C2 | ancestor case dropped from `selftest()` (C4) | `MutRegistry/receipts/C4-selftest.txt` | killed by the denominator only (`PASS 16/16` vs the frozen `17/17`) |
| C2 | ancestor case forced ok (C5) | `MutRegistry/receipts/C5-selftest.txt`, `C5M07-selftest.txt` | **survives alone**; killed by the compound M07 probe (which then reads `PASS 17/17`) |
| — | coverage at the pre-round tip, the r98 settle and the r97 settle | `before/r99-d1-coverage-*.txt` | `PASS 160/160` (tip, r98 settle) and `157/157` (r97 settle) — the cited figures re-derive |

**Converging, or moving the hole?** C1: the era legs are now genuinely certified (M2/M4 kill), while
the two *echo* flags and the whole lie-kind layer have no committed witness — a class the round
names rather than claims. C2: both frozen shapes and the ancestor branch are certified and
mutation-killed; the capture's remaining holes are separator/spelling classes, not the shapes the
round froze. Both rounds' survivors share one class: *a property certified at the granularity the
instrument happens to observe, not at the granularity the sentence claims* — which is why the
amendments, not new instruments, carry the corrections.

## Routed (r98 -> r99)

| r98 routed item | r99 treatment | evidence |
|---|---|---|
| R99-D1 unlanded `160/160` tip receipt | closed — the coverage receipt for `f107da3a` and for the r98 settle `270ca298` is committed under `.ufo/waves/round-99/before/`; the r98 `after/report-draft.md` pointer stays as filed history (append-only) | `before/r99-d1-coverage-tip-f107da3a.txt`, `before/r99-d1-coverage-r98settle-270ca298.txt` |
| Y-cap field fidelity (G6 survivor) | closed — the Y family sets `check_echo`/`check_era`; `N09-y-era` now reads unmet where the r98 control is blind | `before/dev/c1-N09-*.json` |
| X-cap field fidelity (A5) | closed as a delta — one additional failed family | `before/dev/c1-N11-*.json` |
| battery selftest's missing echo/era lie kind | closed — two lie kinds added and measured | `before/dev/c1-lie-*.json` |
| hybrid and same-cell-restatement capture shapes | closed — both fail closed in r99 | `ExecRegistry/fx-*` |
| M07 ancestor branch | closed — a git-fixture selftest case kills the mutant | `ExecRegistry/m07-*` |
| unbound rows, co-doctoring, printed-tally parsing | carried, unchanged | `corpus/README.md` § "Frontier (round-99 addition)" |

## Frontier moved this round

The two r98 field-fidelity limits and the lie-kind structural gap are closed by measurement; the
hybrid, restatement and ancestor survivors are closed by a case that the do-nothing instrument
fails. What remains, by name: the X/Y echo legs have no spelling-targeted bend; the `unique` rule is
fail-closed for a cell that legitimately states two spans; the unbound registry rows and the three
r98 C2 gaps; the carried r96/r93/r89 items.
