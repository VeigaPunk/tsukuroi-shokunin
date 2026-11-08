# ReviewBattery — round 95 reviewer (w1 seat ReviewBattery)

Scratch: `/fast/scratch/hyaku/tsukuroi-r95/ReviewBattery` (removed on exit). Receipts: this directory
(`.ufo/waves/round-95/w1/ReviewBattery/`). Instruments verified before and after the attack:
`sha256sum -c .ufo/waves/round-95/before/instruments.sha256` → 9/9 OK, including
`tools/check-limine-pins.py` `7d79ac29…` and `tools/limine-pin-battery-r95.py` `a51dca18…`.
No instrument byte was edited; every gate variant is a copy under this seat's receipts
(`variant-a.py` … `variant-f.py`), each a one-clause diff against the landed gate (`variant-*.diff`).

Axes attacked: depth (C1's wording vs what the battery actually enforces), enumeration
(which 9-digit members are certified), mechanism-vs-observable (era selection, echoed version).

## 1. One-clause variants (r95 battery `--runs 1`, isolated `--work` in scratch)

| variant | one clause bent (gate line) | r95 battery on the variant | frozen r94 roster on the variant |
|---|---|---|---|
| a | keep `len(p) <= 9`, reject exactly `(999999999,9,9)` (`parse_limine_version`, gate 99-102) | `unmet` 98/99, failed `["REFUSAL-VERSIONS-9DIGIT"]`, 4 error rows (rc 64, no JSON) | `met` 98/98 |
| b | accept it, force era A for a 9-digit first component (`era_b`, gate 193) | `unmet` 98/99, failed `["REFUSAL-VERSIONS-9DIGIT"]`, 0 errors, got consequence `prompt` | `met` 98/98 |
| c | accept any 9-digit first component, clamp the era tuple to `(12,9,5)` (`check`, gate 193-194) | **`met` 99/99** | `met` 98/98 |
| d | accept it, echo `limine_version: "12.9.4"` in the JSON (gate 316) | **`met` 99/99** | `met` 98/98 |
| e (extra) | report `on_panic: "halt"` for a 9-digit first component (gate 323) | `unmet` 98/99, failed `["REFUSAL-VERSIONS-9DIGIT"]`, 0 errors, got `on_panic` `halt` | `met` 98/98 |
| f (extra) | accept 9-digit X but bend the Y-component bound to `<= 8` (gate 99-100) | **`met` 99/99** | `met` 98/98 |

Raw rows: `battery-{landed,variant-a..f,n05-r95,n05-r94,landed-r94}.json`; per-case extraction in
`case-rows.txt` / `case-rows-legs.txt`; `count-runs.txt`; matrix in `summary.json`.

Clause each variant tests and the catch verdict:

- **a** — the accepted side of the bound (the gate must answer a verdict for the in-bound value, never
  rc 64). Killed. `case-rows.txt`: all four rows `bad-output: JSONDecodeError rc=64`.
- **b** — the era-B observable (`consequence panic`). Killed: the gate answers `prompt`, pins mismatch.
- **c** — the *mechanism* sentence "999999999 is at or above the 12.9.5 split": the gate ignores the
  magnitude and clamps to the split. **Not caught** (99/99) because the observable era-B answer is
  identical and the battery never reads `visibility_era` (`run_gate`'s tuple has no slot for it,
  battery 1995-2004). C1's stated answer (`panic`) survives this bend; the explanatory mechanism does
  not.
- **d** — the version the gate reports back. The battery captures `got[8] = out["limine_version"]`
  (battery 2003) but `auto_ok` returns `True` whenever `c.auto is None` (battery 2010-2015), so a
  flag-driven case never asserts it — the passing row carries `limine_version "12.9.4"` for a run sent
  `999999999.9.9`. **Not caught.** C1 does not claim the echo, but the field is one line from being
  checkable.
- **e** — `on_panic as the fixture fixes it`. Killed: the expected value is compared
  (`want_op = c.want_on_panic()` / `got[6] == want_op`, battery 2107-2111).
- **f** — the published cap is *per component* ("1-9 digits per component", gate 92-94); the accepted
  leg sends 9 digits only in X. A gate that refuses a 9-digit Y (`0.999999999.9` → rc 64,
  `middle-bound-probe.txt`) still reads `met` 99/99. **Not caught.** This is the same class as
  ReviewBattery F2 (r94) but on the accepted side of Y/Z.

## 2. Fixture soundness (not just killability)

Fixture reproduced from the battery's own `Case` (`fixture-probe.txt`; names/bytes are fresh per
build — two builds give different conf bytes and disjoint file names):

```
 1 | /0m-04tw
 2 |   protocol: efi
 3 |   path: boot():/-zz3vodwqrj.efi#f1404b31…c90f
 4 | hash_mismatch_panic: no
 5 | /xqdmh
 6 |   protocol:	efi
 7 |   path: boot():/zgc1ooi6/2adq_3ns.efi#c18840b2…8b67
```

Expectation: `finish() = (1, 'DEGRADED', [(3, 'LP-MISMATCH', 'panic'), (7, 'OK', 'none')])`,
`want_on_panic() = menu`, `r1_panic() = None`, `global_lines() = []`, `era_b() = True`.

The era-B answer (`panic`) is exactly what `tools/check-limine-pins.py`'s visibility rule requires
(gate unchanged, `gate-code-excerpt.txt`):

- `parse_limine_version` (gate 91-103): three components, ASCII digits, each `len <= 9` →
  `(999999999, 9, 9)`; `VISIBILITY_ERA_SPLIT = (12, 9, 5)` (gate 104).
- `era_b = version >= VISIBILITY_ERA_SPLIT` (gate 193) → `True` (`999999999 > 12`).
- first-entry scan (gate 216-220): line 1 `"/0m-04tw"` → `first_entry = 1`; the loop (gate 223-226)
  sets `in_global = False` at line 1 because `first_entry == 1 and era_b` — this is the 12.9.5+ rule
  with no first-line exception.
- line 4's `hash_mismatch_panic: no` is therefore skipped (`if in_global and key == …`, gate 235-236)
  → `panic_setting is None` → `prompt` stays false (gate 258) and the mismatch consequence is `panic`
  (gate 305-306).
- JSON `visibility_era` = `"12.9.5+"` (gate 318).

The fixture is era-discriminating, so the same file witnesses the split (`era-discriminator.txt`):
`12.9.4` → pins `[(3,'LP-MISMATCH','prompt')]` era `pre-12.9.5`; `12.9.5`, `12.9.6` and
`999999999.9.9` → `[(3,'LP-MISMATCH','panic')]` era `12.9.5+`. Sound, not vacuous.

## 3. Sentence-by-sentence enforcement in C1

| C1 sentence fragment | verdict | artifact |
|---|---|---|
| "carries … the family REFUSAL-VERSIONS-9DIGIT" | **enforced** | roster 99 unique, family once, `FAMILIES == FAMILY_ROSTER`, 4 cases/run (`rosters.txt`, `case-rows.txt`) |
| "on fixtures generated fresh per run" | **enforced** (construction; not asserted) | per-run `random.Random(secrets.randbits(64))` (battery 2086), `secrets.token_bytes`/`token_hex`; two-build probe differs (`fixture-probe.txt`) |
| "the version 999999999.9.9 … is sent as the --limine-version" | **enforced** (harness side) | `_era_first_line_panic(c, REFUSAL_DIGIT9)` (battery 1694, 1707-1715), `inner += ["--limine-version", c.version]` (battery 1982); rows echo `999999999.9.9` |
| "the gate's report of that version" (variant d) | **not-enforced-by-instrument** | `auto_ok` only checks auto cases (battery 2010-2015); variant d met 99/99 |
| "the largest in-bound member of … 1-9-digit component cap, first component 999,999,999" | **falsified as a superlative; per-component accepted leg not-enforced** | the true component-wise maximum `999999999.999999999.999999999` is in-bound (gate 99) and accepted by the landed gate (`boundary-probe.txt`: rc 1, era B) but never sent; variant f (Y bound `<=8`) met 99/99 |
| "a fixture whose first physical line is an entry label" | **enforced** (construction) | `fixture-probe.txt` line 1; `global_lines() == []` |
| "must answer rc 1, verdict DEGRADED" | **enforced** | full tuple compared (battery 2108-2112); variant a fails; landed rows match |
| "the LP-MISMATCH pin with consequence panic" | **enforced** | pins list compared exactly; variant b (`prompt`) fails |
| "era B: … at or above the 12.9.5 split, so the key is invisible" | **observable enforced / mechanism not-enforced** | consequence `panic` witnesses invisibility; `visibility_era` is never read; variant c met 99/99 |
| "on_panic as the fixture fixes it" | **enforced** (but constant `menu`) | `want_on_panic()` compared (battery 2107, 2111); variant e fails; the fixture fixes `menu` in every case (no visible `measured_boot`, no SB) |
| "against N05-strict-8 … unmet … in every run" | **enforced** | bend diff one line (`n05-diff.txt`); r95 ×3: unmet 98/99 each, failed exactly the family, 4 rc-64 error rows each (`x3-detail.txt`) |
| "0 error rows" (target, landed and r94 legs) | **enforced as a corollary of `met`** | an error row implies a failed case; measured 0 on landed ×3, landed-r94, n05-r94; 4 on n05-r95 (A1's expected bend receipt) |
| "99/99 met ×3 canonical and clone" | canonical **enforced** by my ×3; **clone untested here** | `battery-landed-x3.json` (met 99/99 ×3); clone is the execution seat's leg |

## 4. Findings

**F1 — C1's "largest in-bound member" is false; the cap's accepted leg is only X-certified.**
`REFUSAL_DIGIT9` is `999999999.9.9`, i.e. the *first component* at the cap with Y and Z at the
single-digit floor. The cap (`len(p) <= 9` per component) admits `999999999.999999999.999999999`,
which is strictly larger and which the landed gate accepts (`boundary-probe.txt`: rc 1, verdict
DEGRADED, era `12.9.5+`). The battery sends neither that value nor any 9-digit Y/Z, so variant f
(bend only Y's bound to `<= 8`; it refuses `0.999999999.9` at rc 64, `middle-bound-probe.txt`) still
reads `met` 99/99. The parenthetical "first component 999,999,999" is accurate and scopes the family;
the superlative is not. Fix the sentence to "a boundary member: first component at the cap" and put
the per-component accepted boundary on the frontier (or enumerate X/Y/Z 9-digit positions as the r94
digit10 family does for the refused side).

**F2 — the era-selection mechanism and `visibility_era` are unasserted.** Variant c ignores the
version's magnitude, clamps the era tuple to `(12,9,5)`, and reads `met` 99/99; the battery's got tuple
has no `visibility_era` slot. C1's required observable (`panic` because the key is invisible) is still
enforced — variant b, which makes the key visible (era A), fails on `prompt`. So C1's answer list is
sound; its explanatory mechanism is not certified. Either assert `visibility_era == "12.9.5+"` for
this family or say the mechanism is unclaimed.

**F3 — the echoed `limine_version` is recorded, never compared for flag cases.** Variant d reports
`12.9.4` for a run sent `999999999.9.9` and reads `met` 99/99 (`case-rows.txt`: got
`limine_version 12.9.4`). `auto_ok` short-circuits on `c.auto is None`. C1 does not claim the echo, so
this is a coverage gap, not a falsification; one assertion (`got[8] == c.version` when
`c.pass_version`) closes it and would also make variant d killable.

**F4 — `on_panic` is checked but the fixture fixes it to a constant.** For this family there is no
visible `measured_boot` and no Secure Boot, so `want_on_panic()` is `menu` for all four cases; variant e
proves the field is compared (unmet, got `halt`). The clause is enforced, but it carries less
discriminating power here than its wording suggests; other families (measured/TPM) carry the rest.

## 5. Verdict per clause

| clause | verdict |
|---|---|
| family carried / roster literal / 4 cases per run | **enforced** |
| fresh fixtures per run | **enforced** (construction, demonstrated) |
| version sent as `--limine-version` | **enforced** |
| gate's echoed version | **not-enforced-by-instrument** (not claimed by C1) |
| "largest in-bound member" | **falsified** as a superlative |
| per-component accepted 9-digit boundary (X, Y, Z) | **not-enforced-by-instrument** (only X) |
| first physical line is an entry label | **enforced** |
| rc 1 + DEGRADED | **enforced** |
| LP-MISMATCH + consequence panic | **enforced** |
| "era B … key invisible" mechanism / `visibility_era` | **not-enforced-by-instrument**; observable enforced |
| `on_panic` as the fixture fixes it | **enforced** (constant `menu`) |
| N05-strict-8 differential, every run | **enforced** (×3) |
| 0 error rows on the landed/r94 legs | **enforced** as a `met` corollary |
| clone layout | **untested** by this seat |

## 6. Bearing on C1 (depth)

The operational target reproduces in my own runs: landed gate r95 `met` 99/99 ×3 with `failed_families
[]` and 0 error rows; N05-strict-8 r95 `unmet` 98/99 ×3 with `failed_families` exactly
`["REFUSAL-VERSIONS-9DIGIT"]` and four rc-64 error rows per run; both r94 do-nothing legs `met` 98/98
with 0 error rows and 0 `REFUSAL-VERSIONS-9DIGIT` rows (the blindness proof); the frozen r94 roster is
blind to every one of the six variants (all `met` 98/98). The family is sound, non-vacuous and
era-discriminating.

The wording ships one false superlative (F1) and two unenforced mechanism clauses (F2, F3), plus a
per-component coverage gap (F1). None of these weakens the landed-gate target or the N05 differential;
none widens a target in my reading. Recommendation (not an admission): C1 verifies on its stated
answer list; narrow the superlative to a boundary-member sentence and either assert
`visibility_era`/`limine_version` or declare them unclaimed.

## Residual risk and verification gaps

- Clone layout not re-run by this seat (`git clone --shared` + battery is the execution seat's leg).
- r94 do-nothing legs were run `--runs 1` each (98/98 both); the r95 landed and N05 legs were run
  `--runs 3` (99/99 ×3, 98/99 ×3).
- No Python language server answered for these scripts (no project config; `lsp` not applicable), so
  call-site/definition checks rest on direct line reads of the pinned gate and battery plus the
  executed runs — not on semantic-index queries.
- Scratch removed; every cited number is a receipt in this directory.

{"seat":"ReviewBattery","verdict":"findings","notes":"C1 operational target reproduced (landed 99/99 x3, N05 98/99 x3 family-only with 4 rc64 errors, r94 blindness 98/98, instruments verified); wording gaps: 'largest in-bound member' falsified (true component-wise max unexercised), era mechanism/visibility_era and echoed limine_version unasserted (variants c,d met 99/99), per-component accepted cap only X-certified (variant f met 99/99), on_panic checked but constant; clone leg untested here."}
