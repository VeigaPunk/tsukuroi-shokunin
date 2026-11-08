# ReviewBattery — round 99, C1 independent attack

Seat `ReviewBattery-9` (role reviewer, leaf; no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, pre-round tip `f107da3afe511f7db8cdc30235a992b774903158`.
Scratch `/fast/scratch/hyaku/tsukuroi-r99/ReviewBattery-9` (deleted before yield).
Target: re-derive C1's legs with my own runs and try to falsify the claim's **wording**, not only its
numbers. Every number below was produced by me; receipts are under
`.ufo/waves/round-99/w1/ReviewBattery-9/receipts/`.

## 0. Verdict in one paragraph

C1's **frozen target holds in full, in both layouts**: landed gate `105/105 met` ×3 canonical and ×3
clone, `failed_families []`, 0 error rows; N09 `unmet 104/105` ×3 both layouts, exactly
`[REFUSAL-VERSIONS-9DIGIT-Y]`; N11 `unmet 103/105` ×3 both layouts, exactly
`[EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]`; the r98 control is `met 105/105` ×3 on the gate and
on N09 and `unmet 104/105` ×3 on N11 with exactly `[EXPLICIT-VERSION-ERA]`; both new lie kinds read
`unmet`; `--selftest` (no reference) `PASS 5/5`. The wording does not survive inspection at three
points: the predicate's "exactly two changes" is a third change short (the battery's JSON `schema`
token moves `…-r97-v1` → `…-r99-v1`); the field-fidelity closure it advertises is certified only for
the twelve spellings the roster sends (two one-clause gates read `met 105/105` while lying off-roster);
and the plan's C1 heading "the battery selftest sees an assertion removal" is **falsified** — with both
metadata assertions disabled the wrapped-gate readings are still `unmet` (100/105 and 98/105), i.e. the
two lie legs pass whether or not the fields are asserted. One further, lower-severity finding: the X-family's new
assertions are a QUALITY-136 twin of `EXPLICIT-VERSION-ECHO`/`-ERA`'s fourth row (same spelling, same
fixture constructor, same expected pins).

## 1. Instrument integrity

```
$ cd tsukuroi-shokunin && sha256sum -c .ufo/waves/round-99/before/instruments.sha256
tools/limine-pin-battery-r99.py: OK
tools/make-r99-bends.py: OK
tools/check-registry-content-r99.py: OK
tools/check-limine-pins.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-99/before/controls/do-nothing-checker-r98.py: OK
.ufo/waves/round-99/before/controls/bends/N09-y-era.py: OK
.ufo/waves/round-99/before/controls/bends/N11-x-era.py: OK
.ufo/waves/round-99/before/dev/make-fixtures.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/plans/round-99.md: OK
rc=0   (16/16 OK; re-verified at report time in receipts/13-final-pins.txt)
```

Control identity against the pre-round tip (read-only `git show`), receipt `receipts/03-control-identity.txt`:

| path | at `f107da3a` | committed control |
|---|---|---|
| `tools/limine-pin-battery-r98.py` | `8198bd848eff…` | `do-nothing-battery-r98.py` `8198bd848eff…` |
| `tools/check-registry-content-r98.py` | `5bb1441eed43…` | `do-nothing-checker-r98.py` `5bb1441eed43…` |
| `tools/check-limine-pins.py` | `7d79ac296daa…` | `do-nothing-gate.py` `7d79ac296daa…` |

Byte-level anchors (`grep -abo` on the pinned bytes), receipt `receipts/01-byte-anchors.txt`:
`c.check_echo = True` at 79015 / 79893 / 81666 / 83173 / 84390; `c.check_era = True` at 79039 / 80414 /
81690 / 83197 / 84414; `def fam_refusal_versions_9digit(` at 78027; `def fam_refusal_versions_9digit_y(`
at 80521; bend clause at byte 17191 in both bends; `tsukuroi-limine-pin-battery-r99-v1` at 105742 in the
r99 battery, `tsukuroi-limine-pin-battery-r97-v1` at 104316 in the r98 control.

Both bends are exactly one changed line against the gate (`diff`: 1 removed, 1 added; receipt
`receipts/05-bend-one-clause.txt`), each keying the swapped label on the literal component
`"999999999"` (`N09` second component, `N11` first component).

## 2. Structural re-derivation of "the r98 battery … with exactly two changes"

Receipt `receipts/02-battery-diff-summary.txt` (module import + block diff, not a text guess):

| check | reading |
|---|---|
| roster literal | 105 both, `repr` sha256 `43458dd75308…` both, `tuple(FAMILIES) == FAMILY_ROSTER` true |
| `CASES_PER_FAMILY` | 4 -> 420 cases |
| family bodies that differ | exactly `fam_refusal_versions_9digit`, `fam_refusal_versions_9digit_y`; each gains exactly `c.check_echo = True` + `c.check_era = True` (r98: neither flag) |
| `LIE_KINDS` | 12 -> 14, added exactly `limine-version`, `visibility-era`, with the two wrapper branches |
| **third change** | the battery's own JSON `schema` token `tsukuroi-limine-pin-battery-r97-v1` -> `tsukuroi-limine-pin-battery-r99-v1` (byte 105742 vs 104316) plus docstring text |

The token change is inert — `grep` over `tools/` and the wave dirs finds no consumer other than the
batteries' own emitter, `count-runs.py` never reads it, and the wave's own `make-spec.py` asks the seat
to *expect* the new token — but it is a third change and the predicate says "exactly two".

## 3. Leg table (own `--work` dirs, `--runs 3`, parsed with `count-runs.py`)

Canonical layout = the lane tree; clone layout = `git clone --shared` of the lane at `f107da3a`
(toplevel verified equal to my scratch clone path) with the four untracked r99 instruments copied in at
their lane-relative paths and `sha256sum -c` 16/16 inside the clone (`receipts/11-clone-verify.txt`) —
the r99 tools are untracked at HEAD (`git ls-tree HEAD tools/` shows only up to `…-r98.py`), so a clone
cannot otherwise contain them.

| leg | expected (frozen target) | my reading — canonical | my reading — clone | verdict |
|---|---|---|---|---|
| r99 battery, landed gate | `met 105/105`, `[]`, 0 err, ×3 | `met 105/105` ×3, `[]`, 0 err | `met 105/105` ×3, `[]`, 0 err | PASS |
| r99 battery, N09-y-era | `unmet 104/105`, exactly `[REFUSAL-VERSIONS-9DIGIT-Y]`, 0 err, ×3 | `unmet 104/105` ×3, `[Y]`, 0 err | `unmet 104/105` ×3, `[Y]`, 0 err | PASS |
| r99 battery, N11-x-era | `unmet 103/105`, exactly `[EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]`, 0 err, ×3 | `unmet 103/105` ×3, `[E, X]`, 0 err | `unmet 103/105` ×3, `[E, X]`, 0 err | PASS |
| r98 control, landed gate | `met 105/105` ×3 | `met 105/105` ×3 | `met 105/105` ×3 | PASS |
| r98 control, N09 (blind) | `met 105/105` ×3 | `met 105/105` ×3 | `met 105/105` ×3 | PASS |
| r98 control, N11 | `unmet 104/105` ×3, exactly `[EXPLICIT-VERSION-ERA]` | `unmet 104/105` ×3, `[E]` | `unmet 104/105` ×3, `[E]` | PASS |
| r99 `--selftest` (no reference) | `PASS 5/5` | `PASS 5/5` | — (single run) | PASS |
| r99 battery, `lie-limine-version` gate | `unmet` | `unmet 93/105`, 12 families, 0 err | — | PASS |
| r99 battery, `lie-visibility-era` gate | `unmet` | `unmet 95/105`, 10 families, 0 err | — | PASS |

Per-family case counts on the landed gate (`EXPLICIT-VERSION-ERA`, `X`, `Y`, `Z` all `4/0` passed) and on
the bends (`N09`: `Y 0/4`, everything else `4/0`; `N11`: `X 0/4`, `EXPLICIT-VERSION-ERA 3/1`) are in
`receipts/12-all-legs.txt`; `count-runs.py` output in `receipts/07-canon-count-runs.txt` and
`receipts/clone-*.count.txt`.

Commands (one example per shape; every leg in `receipts/12-all-legs.txt` was run the same way):

```
python3 tools/limine-pin-battery-r99.py --gate <GATE> --runs 3 --work <scratch>/work/<tag> --json <seat>/receipts/<tag>.json
python3 tools/limine-pin-battery-r98.py --gate <GATE> --runs 3 --work <scratch>/work/<tag> --json <seat>/receipts/<tag>.json
python3 .ufo/waves/round-95/before/controls/count-runs.py <seat>/receipts/<tag>.json \
    --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family REFUSAL-VERSIONS-9DIGIT-Z
python3 tools/limine-pin-battery-r99.py --selftest
```

## 4. Causality: one assertion removed at a time

Four mutants of the **r99 battery**, each deleting exactly one flag line inside one family (verified
one-line diffs; sha256 in `receipts/08-artifact-hashes.txt`; the frozen instrument was never touched):

| mutant | one deletion | on N09 (frozen `unmet 104/105 [Y]`) | on N11 (frozen `unmet 103/105 [E, X]`) | seen by a bend? |
|---|---|---|---|---|
| Ma | X family `c.check_echo = True` | `unmet 104/105 [Y]` — unchanged | `unmet 103/105 [E, X]` — unchanged | **no** (survives both) |
| Mb | X family `c.check_era = True` | `unmet 104/105 [Y]` — unchanged | `unmet 104/105 [E]` — **moved** (better) | **yes, N11** → killed |
| Mc | Y family `c.check_echo = True` | `unmet 104/105 [Y]` — unchanged | `unmet 103/105 [E, X]` — unchanged | **no** (survives both) |
| Md | Y family `c.check_era = True` | **`met 105/105`** — moved (better) | `unmet 103/105 [E, X]` — unchanged | **yes, N09** → killed |

Direction read under R98-MUTANT-DIRECTION-READ: a reading that moves *better* than frozen is the leg
detecting the mutant. So N11 sees the X-era deletion (103→104) and N09 sees the Y-era deletion
(104→met). **Neither bend can see either echo assertion**: removing X's or Y's `check_echo` leaves both
bend readings byte-identical (same verdict, same counts, same failed sets). That is the plan's own named
limit, now measured: `receipts/12-all-legs.txt`, legs `mut-Ma-*`, `mut-Mc-*`.

Two further legs bound what the *selftest* can see (added because the first four leave that open):

| leg | reading | what it shows |
|---|---|---|
| Ma / Mc on the `limine-version` wrapper | `unmet 93/105`, **the same 12 families** as the pristine lie leg | removing X's or Y's echo flag does not change the lie leg at all |
| Mb / Md on the `visibility-era` wrapper | `unmet 95/105`, **the same 10 families** as pristine | same for the era flag |
| Me: **both** field checks disabled in `meta_ok` (`if False and c.check_echo …`) | landed gate `met 105/105`; `lie-limine-version` `unmet 98/105`; `lie-visibility-era` **`unmet 100/105`** (only the 5 refusal-shaped families fail) | the wrapped-gate reading is `unmet` **with zero field assertions** — it is caused by the wrapper failing on refusal-shaped cases (empty stdout → `json.loads("")`, no `try`), not by the assertion, so the leg (`verdict == "unmet"`) still passes |

## 5. Wording attack

Two one-clause wrappers around the landed gate, in scratch only, each read by the r99 battery `--runs 3`
and by direct gate probes (`receipts/00-direct-probes.txt`, `receipts/09-lie-wording-summary.txt`):

**W1 `W1-roster-echo.py`** (sha256 `d36190a39cc7…`) — echoes the flag spelling verbatim **only** for the
twelve spellings the roster sends, `0.0.0` otherwise (both emission sites patched).

- battery: `met 105/105` ×3.
- probe: `--limine-version 6.9.9` → `limine_version: "0.0.0"` (pristine: `"6.9.9"`); `12.9.7` → `"0.0.0"`
  (pristine `"12.9.7"`); `12.9.4`, `12.9.5`, `999999999.9.9` → verbatim.

**W2 `W2-x-string-era.py`** (sha256 `aa56832d2432…`) — the era's first component compared as **text**
(`str(X) >= "12"` unless `X == 12`), which agrees with integer order for every first component the
roster sends (`0` and `>= 12`) and inverts for `X in 1..9`.

- battery: `met 105/105` ×3.
- probe: `--limine-version 6.9.9` → `visibility_era: "12.9.5+"` (pristine `pre-12.9.5`); `12.9.4`,
  `12.9.5`, `12.9.7`, `999999999.9.9` correct.

### Per-sentence verdicts

Frozen predicate (`claims.json`):

| # | sentence | verdict | falsifying/narrowing artifact |
|---|---|---|---|
| P1 | "…is the r98 battery (roster unchanged at 105) with **exactly two changes**" | **narrow** | `tools/limine-pin-battery-r99.py` byte 105742 vs `do-nothing-battery-r98.py` byte 104316: the `schema` token changes too (third change, inert) |
| P2 | "(a) … set `check_echo` and `check_era`, so each case asserts the flag spelling echoed verbatim with source `flag` and the era label the whole tuple selects" | **narrow** | `w/W1-roster-echo.py` `met 105/105` ×3, `w/W2-x-string-era.py` `met 105/105` ×3 |
| P3 | "(b) `LIE_KINDS` gains `limine-version` and `visibility-era`, so the `--selftest --reference` leg falsifies the two reported fields" | **holds** (literal) | wrapper branches at the frozen bytes; both wrappers read `unmet` (93/105, 95/105). The leg's *verdict* is not a witness that a field is asserted — see the plan-heading row below |
| P4 | "The r98 Frontier names both limits: the metadata assertion is bound to the two r97 families only, and the X leg rides on one EXPLICIT case (A5)" | **holds** | `corpus/README.md` line 1241 ("bound to the two r97 families only") and line 1267 ("saw that article through one EXPLICIT case (A5)") |

Target:

| # | sentence | verdict | evidence |
|---|---|---|---|
| T1 | landed `105/105 met`, `[]`, 0 errors, ×3 canonical + ×3 clone | **holds** | `receipts/canon-r99-gate.json`, `receipts/clone-r99-gate.json` |
| T2 | N09 `unmet 104/105` ×3 both layouts, exactly `[Y]`, 0 errors | **holds** | `receipts/canon-r99-n09.json`, `receipts/clone-r99-n09.json` |
| T3 | N11 `unmet 103/105` ×3 both layouts, exactly `[E, X]`, 0 errors | **holds** | `receipts/canon-r99-n11.json`, `receipts/clone-r99-n11.json` |
| T4 | r98 control `met` ×3 gate, `met` ×3 N09, `unmet 104/105` ×3 N11 exactly `[E]` | **holds** | `receipts/canon-r98-*.json`, `receipts/clone-r98-*.json` |
| T5 | `--selftest` (no reference) `PASS 5/5` | **holds** | `receipts/selftest-no-reference.txt` |
| T6 | both new lie kinds make the battery read `unmet` | **holds** | `receipts/lie-limine-version.json` `93/105`, `receipts/lie-visibility-era.json` `95/105` |

Round C1 heading (`.ufo/plans/round-99.md`, §C1): "**the two accepted-cap families assert the reported
fields, and the battery selftest sees an assertion removal**" — first clause **holds**, second clause
**falsified** by `receipts/mut-Me-on-lie-era.json` (`unmet 100/105` with both field checks disabled —
the leg still passes) and by `receipts/mut-Ma-on-lie-echo.json` / `mut-Mc-on-lie-echo.json` /
`mut-Mb-on-lie-era.json` / `mut-Md-on-lie-era.json` (single removals leave the lie legs at exactly
`93/105` and `95/105` with identical family sets).

### Proposed narrowings (exact sentences)

- P1: "…is the r98 battery (roster literal unchanged at 105) with exactly two **behavioural** changes —
  the four metadata flags and the two lie kinds — plus the battery's own inert JSON `schema` token
  (`…-r97-v1` → `…-r99-v1`) and docstring text."
- P2: "…so each case asserts the echoed spelling verbatim with source `flag` and the era label of the
  whole tuple **for the twelve spellings the roster sends** (`12.9.4`, `12.9.5`, `12.9.6`,
  `999999999.9.9`, `12.999999999.4`, `0.999999999.0`, `12.9.999999999`, `0.9.999999999`, `12.09.4`,
  `000000012.9.4`, `12.000000009.000000005`, `000000000.000000000.000000000`); a gate that echoes
  verbatim only for those strings, or that compares the first component as text, reads `met 105/105`."
- C1 heading: "…and the battery selftest gains lie kinds for the two reported fields (its legs are red
  for any gate those lie kinds wrap, including a battery with no field assertion at all); it still does
  not see a per-family assertion removal."

## 6. `--selftest` without reference — what 5/5 does and does not cover

`receipts/selftest-no-reference.txt` (5m16s):

```
reference-gate      skipped (no --reference)
roster-literal     PASS families_passed=105
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
selftest PASS 5/5
rc=0
```

It covers exactly two things: the roster literal equals `FAMILIES` (105 names), and four negative-control
gates (`absent`, a constant-HEALTHY printer, a non-JSON printer, a constant-DEGRADED printer) each read
`unmet`. It does **not** cover: any `LIE_KINDS` leg (all 14 are skipped without `--reference`), any
family's expected pins, the metadata assertions this round adds, the reference gate's full-coverage
condition, or the clone layout.

## 7. Findings by severity

1. **F1 — falsified C1 clause (medium, wording/claim-scope).** The plan heading "the battery selftest
   sees an assertion removal" is false as measured: the wrapped-gate reading is `unmet` with **no** field
   assertion present, so the leg passes (`mut-Me-on-lie-era.json` `unmet 100/105`; the leg checks only
   `verdict == "unmet"`), because `LIE_WRAPPER` does `json.loads(p.stdout)` with no guard and every
   refusal-shaped case (empty stdout) therefore fails under *any* lie kind. Removing one family's flag
   leaves both legs bit-for-bit at their pristine tallies (93/105 / 95/105, identical family sets). The
   r98 scoreboard row "`--selftest` cannot see an assertion removal" is therefore **not** closed; only
   its narrower sub-clause "`LIE_KINDS` has no member falsifying these fields" is.
2. **F2 — "exactly two changes" is three (low, wording).** See §2: the `schema` token moves. Inert (no
   lane consumer) but undeclared.
3. **F3 — field-fidelity closure is roster-scoped (low, wording).** W1 and W2 each read `met 105/105`
   while lying off-roster; the assertion is certified for the twelve strings the roster sends, not for
   the accepted grammar.
4. **F4 — the X-family assertions are a QUALITY-136 twin (low, no numeric effect).** `_explicit_fixture`
   is `_era_first_line_panic`; `EXPLICIT_VERSION_META[3] == REFUSAL_DIGIT9 == "999999999.9.9"`, so
   `REFUSAL-VERSIONS-9DIGIT`'s new `check_echo`/`check_era` assert the *same input, same fixture, same
   expected pins* as `EXPLICIT-VERSION-ECHO`/`-ERA`'s fourth row. The N11 delta `104/105` -> `103/105`
   is a second family on an article r98 already caught, not new spelling or fixture coverage (Mb makes
   that explicit: with the X flags removed N11 returns to `104/105 [E]`). The genuinely new coverage in
   C1 is the Y family (new spellings; N09 `met` -> `unmet`) and the two lie kinds. Receipt:
   `receipts/04-twin-analysis.txt`. Under QUALITY 136 ("a family that only re-answers a case the old
   roster already covered is a twin, not a boundary") the X addition is a twin at the article level;
   the round applies the same rule to drop its Z-echo bend, so the standard is the round's own.

## 8. Residual risk and verification gaps

- I did **not** run the full `--selftest --reference` (16 legs × 420 cases); I ran the two lie wrappers
  directly (byte-identical construction from the frozen `LIE_WRAPPER` template and the pinned gate) plus
  the no-assertion mutant. The reference-gate leg's full-coverage condition is unverified by me; the
  landed gate's own `met 105/105` over 420 cases is the closest control I ran.
- Consequently the statement "the selftest would still PASS 16/16 on the no-assertion mutant" is
  `[INFERENCE]` from the legs I did run: the only legs whose reading can move are the 14 lie legs (13 of
  which do not touch `limine_version`/`visibility_era` at all), and the two that do (`lie-limine-version
  98/105`, `lie-visibility-era 100/105`) both still read `unmet`; the reference-gate leg reads `met`
  (`mut-Me-on-landed.json`). The measured claim in F1 is narrower and direct: the two new lie kinds do
  not witness the presence of either field assertion.
- The clone layout cannot contain the r99 instruments by construction (they are untracked at HEAD); I
  copied the four pinned files in and verified `sha256sum -c` 16/16 inside the clone. "Clone layout"
  therefore means *same bytes, fresh tree root*, not *committed bytes*.
- My scratch root was deleted at ~11:24 by a sibling seat (`CriticClaims-21`, seat disclosure) while the
  first clone/lie/wording batch was running; those legs were re-executed from rebuilt artifacts. The
  surviving mutant receipts were re-verified against rebuilt artifacts with identical sha256
  (`receipts/08-artifact-hashes.txt`).
- `--runs 3` varies only the random fixture labels/case casing per run; all three runs agreed in every
  leg, so the readings are stable but the fixture *shape* is fixed by construction (this is what F4 is
  about).
- No tool was installed or upgraded; no pacman transaction was run; scratch was deleted before yield.

## 9. Receipts

`receipts/00-direct-probes.txt`, `01-byte-anchors.txt`, `02-battery-diff-summary.txt`,
`03-control-identity.txt`, `04-twin-analysis.txt`, `05-bend-one-clause.txt`, `06-canon-summary.txt`,
`07-canon-count-runs.txt`, `08-artifact-hashes.txt`, `09-lie-wording-summary.txt`,
`10-clone-summary.txt`, `11-clone-verify.txt`, `12-all-legs.txt`, `selftest-no-reference.txt`,
`canon-*.json`, `clone-*.json` + `clone-*.count.txt`, `lie-*.json`, `w1-*.json`, `w2-*.json`,
`mut-*.json`.

{"seat":"ReviewBattery-9","verdict":"findings","notes":"C1 target fully holds in both layouts (landed 105/105 met x3+ x3; N09 104/105 [Y]; N11 103/105 [E,X]; r98 control met/met/104 [E]; selftest 5/5; both lie kinds unmet 93 and 95). Wording: (1) plan clause 'the selftest sees an assertion removal' is falsified — with both metadata assertions disabled the lie legs still read unmet 100/105 and 98/105, and single-flag removals leave them at exactly 93/105 and 95/105 with identical family sets; (2) 'exactly two changes' misses the schema token r97-v1->r99-v1 (inert); (3) the field closure is roster-scoped: W1 (roster-fit echo) and W2 (text first-component era) each read met 105/105 while lying off-roster; (4) the X family's new flags are a QUALITY-136 twin of EXPLICIT-VERSION-*/4th row (same spelling, same _era_first_line_panic fixture, same pins) — the N11 delta is multiplicity, not new coverage. Echo assertions are invisible to both bends (named limit, measured)."}
