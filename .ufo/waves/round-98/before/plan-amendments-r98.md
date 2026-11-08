# Round-98 plan amendments (the plan bytes are frozen at `1cfeb5d5`; this file is append-only)

### A1 (2026-11-08, after `w1/ReviewRegistry` F1/F2, before the report; datum: `w1/ReviewRegistry/receipts/10-a-to-e.txt`)

C2's predicate says the `RC-BEND-SPAN` capture "extended to the comma form (`VARIANTS N01,N03`)".
Measured scope, now stated: the capture is a single ordered alternation
`N<digits>-N<digits>|N<digits>(,N<digits>)+`, so a **hybrid** cell that carries both a hyphen span
and a comma tail (`VARIANTS N01-N04,N05`) binds on the hyphen branch as `N01-N04` and the extra
label is silently dropped — a row that over-claims one label reads `PASS` (F1). A **second**
contradictory span mentioned later in the same cell is likewise unbound (first match wins, F2).
Neither shape is inside the frozen sentences' scope: the claim names the two pure forms and the
doctored legs are pure-form doctors. Both are recorded as named limits in the round's README
Frontier and routed to r99. No predicate, counter, kill rule or target number changes.

### A2 (2026-11-08, after `w1/CriticClaims`, before the report; datum: `w1/CriticClaims/receipts/15-m08-selftest.txt`)

A wave receipt named `15-m08-selftest.txt` shows a checker selftest reading `FAIL 2/14` with an
extra `RC-VALUE-MISMATCH` on almost every case — the signature of a **comma-always** mutant
(`derive_variant_span` returning the comma form unconditionally), not of the frozen M08
(`numbers[:1]` first-label-only), whose selftest reads `FAIL 12/14` with exactly `span-gap` and
`span-gap-lie` red. The M08 kill is therefore carried by the L1 receipt
`before/dev/c2-m08-selftest.txt` (12/14, those two cases red) and by `w1/ExecRegistry`'s
independent re-derivation (same 12/14); the CriticClaims receipt is recorded as a second,
differently-shaped mutant. The claim's sentence about M08 is unchanged; the receipt is not cited
for it.

### A3 (2026-11-08, after `w1/CriticClaims` capture audit, before the report; datum: `w1/CriticClaims/receipts/capture-audit.txt`)

The C2 capture's stated alphabet is `N<digits>`, and the regex is a single ordered alternation
(`N<digits>-N<digits>` | `N<digits>(,N<digits>)+`). Measured shapes outside it: a comma **followed by
a space** (`N01, N03`), a space **before** the comma (`N01 ,N03`) and lowercase labels (`n01,n03`)
produce no capture and read `RC-CELL-MISSING` (fail-closed, not a false pass); hybrid arms
(`N01-N03,N05`, `N01,N03-N05`) bind only their first arm (A1's F1); a duplicate label
(`N01,N03,N03`) captures whole and the set derivation collapses it. None of these forms is produced
by `derive_variant_span` itself (it emits either `N<num>-N<num>` or a sorted comma-joined set), so
the reading is consistent; the claim's phrase is narrowed here to the exact alphabet. No target
number changes.

### A4 (2026-11-08, after `w1/ReviewBattery` g6, before the report; datum: `w1/ReviewBattery/g6-y-era-r98.json`)

C1's predicate carries the sentence "A gate that answers every pin correctly but lies in either
field reads `unmet` on the r98 battery". Measured, that universal is false for spellings outside
the two sharpened families: a gate that lies in `visibility_era` **only for the Y-cap spellings**
(`12.999999999.4`, `0.999999999.0`) answers every pin correctly and reads `met 105/105 x3` on the
r98 battery (and on the r97 battery) — `g6-y-era-r98.json`. The sentence is narrowed to the scope
the claim actually lands: "…lies in either field **for a Z or LZ spelling**". The target numbers,
kill rule and do-nothing readings are unchanged. The X-cap analogue is A5.

### A5 (2026-11-08, after `w1/ReviewBattery` g3, before the report; datum: `w1/ReviewBattery/g3-xcap-r98.json`)

The same predicate implies the X-cap boundary's fields are certified. Measured: a gate that lies in
`visibility_era` only for `999999999.9.9` reads `unmet 104/105` — caught by `EXPLICIT-VERSION-ERA`
alone (one case of 420), because `REFUSAL-VERSIONS-9DIGIT` sends the same spelling with no
`check_era`/`check_echo`. So the X-cap's *field* fidelity rides on one EXPLICIT case, not on the
family whose name claims the boundary. Recorded as a named limit for r99 (the family that sends the
spelling should be the one that asserts its fields); no frozen number changes.

### A6 (2026-11-08, after `w1/ScoutDrift` finding 1, before the report; datum: `w1/ScoutDrift/report.md` §3)

The plan's Limits sentence and C2's named limit say "the other 150 rows stay presence-only". That
count was r97's (154 rows - 4 bound = 150). At this round's pre-round base `b3be3f90` the operative
table has **157 rows**, so the unbound count is **153**; the worktree at settle has **160 rows**
(the three r98 rows land with this round) and therefore **156** unbound. Measured with
`python3 tools/check-registry-coverage.py --revision b3be3f90` (`registered 157`) and, at the tip,
`--revision <settle>` (160). The bound set is unchanged (4 rows / 7 cells). No target number moves;
the correction is this amendment plus the README/lesson/SCORECARD text.

### A7 (2026-11-08, after `w1/ScoutDrift` finding 3, before the report; datum: `w1/ScoutDrift/report.md` §4)

`tools/limine-pin-battery-r98.py` still emits `"schema": "tsukuroi-limine-pin-battery-r97-v1"` (the
successor copied the constant). The claim does not rest on the schema string, and the frozen
instrument bytes are not edited mid-round (the kill rule voids on instrument drift). Routed to r99 as
a naming defect: the successor's JSON should carry an r98 schema token, or the token should be
version-free with a separate `instrument` field.
