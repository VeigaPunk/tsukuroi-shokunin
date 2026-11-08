# CriticClaims — round-98 w1 (C1 depth / C2 freshness clause falsification)

Axes: **depth (C1)** — per-family metadata-assertion coverage of the pin battery; **freshness (C2)** — binding of registry values to re-derived tool bytes. Discipline: every number below is a value I ran in this seat; run wins over sentence.

## Commands (exact, trimmed output)

All from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` unless noted; work dirs under `/fast/scratch/hyaku/tsukuroi-r98/CriticClaims` (deleted before yield).

- `sha256sum -c .ufo/waves/round-98/before/instruments.sha256` → 27 OK, 0 FAILED → `receipts/00-instruments.txt` — **PASS**
- `python3 tools/limine-pin-battery-r98.py --gate tools/check-limine-pins.py --runs 3 --work … --json c1-gate-runs3.json` → `met 105/105` ×3 → `receipts/01-c1-gate-raw.txt` — **PASS** (canonical; clone leg: no seat receipt seen in `w1/ExecGateRuns` at check time — must remain an L1 leg)
- `python3 tools/limine-pin-battery-r98.py --gate …/N07-era-field-lie.py --runs 3 …` → `unmet 103/105` ×3 → `receipts/batt-n07.txt` — **PASS**
- same with `N08-echo-norm.py` → `unmet 104/105` ×3 → `receipts/batt-n08.txt` — **PASS**
- `python3 …/do-nothing-battery-r97.py` on landed / N07 / N08 (`--runs 3`) → `met 105/105` ×3 each → `receipts/batt-dn-*.txt` — **PASS**
- `grep -n check_echo|check_era` + AST walk → r98 asserts flags on `fam_explicit_version_echo` (echo only), `fam_explicit_version_era` (era only), `fam_refusal_versions_9digit_z` and `fam_leading_zero_normalize` (both); r97 do-nothing battery asserts only the two EXPLICIT families — **PASS** (structural, mine)
- `diff do-nothing-battery-r97.py tools/limine-pin-battery-r98.py` → module header + Z/LZ docstring suffixes + the two flag lines + corrected LZ member/direction sentence — **PASS** (roster 105 both, AST-measured)
- `python3 tools/check-registry-content-r98.py --selftest` → `PASS 14/14` rc0 → `receipts/02-c2-selftest.txt` — **PASS**
- `… --revision b3be3f90…` and `--revision master` → `PASS bindings 7/7 findings 0` rc0 → `receipts/03-…`, `04-…` — **PASS**
- D1 revision `aab954f1…`, D2 `d17ebc56…`, lie `3155fd3d…` via clone's `fixture/check-registry-content-r98.py` (`--revision` uses the tool-file ROOT, so the lane tool cannot resolve scratch revs — measured limitation of neatness, not of the claim): D1 FAIL one `RC-VALUE-MISMATCH`, D2 PASS 7/7, lie FAIL one — `receipts/12-14-…` — **PASS**; coverage via clone's `tools/check-registry-coverage.py` → `PASS registered 157 findings 0` on D1 and D2 → `receipts/10-11-…` — **PASS**
- M08 mutant re-derived in scratch (contiguity check on `labels[0]` only): `--selftest` → `FAIL 12/14` (span-gap + span-gap-lie red) → `receipts/21-…`; D2 → FAIL one mismatch, lie twin → PASS → `receipts/22-23-…` — **PASS**. (Two naïve "first label only" variants — truncate labels, collapse to `N01-N01` — give `2/14` and are the wrong shape; the contiguity-blind variant reproduces the frozen `12/14` exactly.)

## Clause table (observed vs sentence)

| # | clause (claim) | observed value (mine) | verdict |
|---|---|---|---|
| C1-1 | roster 105 unchanged | AST `FAMILY_ROSTER len=105` on r98 **and** r97 control; diff shows no roster edit | **met** |
| C1-2 | Z/LZ set `check_echo`+`check_era` | AST: both flags set in `fam_refusal_versions_9digit_z`, `fam_leading_zero_normalize`; `meta_ok` verbatim-echo + whole-tuple era | **met** |
| C1-3 | landed 105/105 met ×3, `failed []`, 0 errors, canonical | `met 105/105` ×3, failed `[]`, error rows 0, cases 420 ×3 (`receipts/counts-from-my-jsons.txt`) | **met** |
| C1-4 | N07 103/105 unmet ×3, failed exactly `[LZ, Z]`, 0 errors | verbatim both runs (`receipts/batt-n07.txt`) | **met** |
| C1-5 | N08 104/105 unmet ×3, failed exactly `[LZ]`, 0 errors | verbatim (`receipts/batt-n08.txt`) | **met** |
| C1-6 | do-nothing battery met 105/105 ×3 on landed + both bends, 0 errors | all three ×3 `met 105/105`, 0 errors ("blindness receipt") | **met** |
| C1-7 | corrected LZ docstring (member `12.000000009.000000005`, text-era-A / int-era-B) | diff shows exactly that sentence replacing the `000000012.9.4`-era-B sentence | **met** |
| C2-1 | landed PASS, findings `[]`, bindings 7 | `PASS bindings 7/7 findings 0` at base and at master | **met** |
| C2-2 | selftest PASS 14/14 (12→14) | `PASS 14/14`, span-gap + span-gap-lie green | **met** |
| C2-3 | M08 FAILS selftest 12/14 | `FAIL 12/14`, both gap cases red | **met** |
| C2-4 | D1 FAIL exactly one `RC-VALUE-MISMATCH` (r98); coverage PASS 157/157 | D1 FAIL one mismatch naming `RC-BEND-SPAN`; coverage PASS 157/157 findings 0 | **met** |
| C2-5 | D2 r98 PASS / M08 FAIL one; lie twin r98 FAIL / M08 PASS | exactly as stated on my runs | **met** |
| C2-6 | capture binds `N<digits>[-N<digits>|,N<digits>...]` | `N01,N03` ✓; `N01,N03,N05` ✓ (full chain); `N01,N03 ` ✓ (trailing space ignored); **`N01, N03` ✗ no capture; `n01,n03` ✗ no capture** → `receipts/capture-audit.txt` | **wording-only falsification** |
| C1-8 (scope) | *"the sharpening closes the A7 limit on THESE families"* — X/Y implication | **Y-spelling-only era lie reads `met 105/105` ×3** (see §Scope) | **neutral (scope named; not falsified)** |

## Load-bearing receipts

1. **C1 counts-from-my-jsons.txt** (canonical counting command `count-runs.py` over my five `--json` outputs): landed 105/105 met, N07 103/105 unmet `[LZ, Z]`, N08 104/105 unmet `[LZ]`, DN all 105/105 met — every `failed_families` exactly as frozen, error rows 0, cases 420.
2. **C2 doctored-leg set**: `12-d1-rev.txt` (FAIL, one mismatch), `13-d2-rev.txt` (PASS 7/7), `14-d2lie-rev.txt` (FAIL, one), `10-11-…coverage` (PASS 157/157, 0), `21-23-…` (M08 `12/14`, D2 FAIL / lie PASS).

## Scope attack — C1 X/Y residue (the genuine counterexample, currently named-but-not-closed)

`EXPLICIT-VERSION-ERA` (era-only) and `EXPLICIT-VERSION-ECHO` (echo-only) send versions `12.9.4, 12.9.5, 12.9.6, 999999999.9.9` — so an **X-spelling** (`999999999.9.9`) field lie **is** certified via the EXPLICIT families. But the only sender of **Y spellings** (`12.999999999.4`, `0.999999999.0`) is the Y family, which sets neither flag; the first-component-only era reader is correspondingly caught only on the EXPLICIT `12.9.4` row (the Y docstring's LIMIT note is honest about this). I built the N07-analogue restricted to Y spellings (pinned, `receipts/y-field-lie2.py`, sha256 in `hash-y2.txt`): direct calls flip `12.999999999.4` `12.9.5+→pre-12.9.5` and `0.999999999.0` `pre-12.9.5→12.9.5+` while leaving Z/LZ untouched, and the r98 battery reads **`met 105/105` ×3** on it (`receipts/batt-y2.txt`, `y2-count.txt`). A gate that lies in either field *only* for Y spellings passes every r98 family. A first cut of the witness (`len(second)==9` without the leading-zero exclusion) failed LZ's `12.000000009.000000005` — that incarnation read `104/105 unmet [LZ]` (`receipts/batt-y.txt`) and was discarded, not spun. The claim sentence ("A gate that answers every pin correctly but lies in either field reads `unmet`") is scope-correct ("on the r98 battery" + the Z/LZ-scoped first clause + plan Limits `plan:122-124` naming the X/Y exclusion); a reader who generalizes it to every spelling is wrong — the sentence that would mislead is the unqualified "lies in either field" without the preceding Z/LZ scoping. Ledger row C1-1 records this as neutral with the Y witness.

## Capture audit — C2

Hybrid/edge shapes (all measured on the pinned regex; `None` = no capture = RC-CELL-MISSING):

| row text | capture reads |
|---|---|
| `VARIANTS N01-N03,N05` (hybrid dash+comma) | `N01-N03` (truncated at dash arm; `,N05` outside capture) |
| `VARIANTS N01,N03-N05` (comma then dash) | `N01,N03` (truncated at dash arm) |
| `VARIANTS N01-N03-N05` (double dash) | `N01-N03` (first dash arm only) |
| `VARIANTS N01,N03,N03` (duplicate label) | `N01,N03,N03` (bound whole; derivation's set dedups, so a duplicate row still risks VALUE-MISMATCH-vs-derived mismatch) |
| `VARIANTS n01,n03` (lowercase) | `None` |
| `VARIANTS N01, N03` (comma+space) | `None` |
| `VARIANTS N01 ,N03` (space before comma) | `None` |
| `VARIANTS N01,N03 ` / `N01-N03 ` (trailing space) | `N01,N03` / `N01-N03` |
| `VARIANTS N01,N03.` (trailing punctuation) | `N01,N03` |

Measured on the pinned regex `VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))` (`receipts/capture-audit.txt`): plain `N01-N03` ✓, `N01,N03` ✓, trailing space `N01,N03 ` ✓ (captures `N01,N03`), three-label `N01,N03,N05` ✓ (full chain), **comma+space `N01, N03` ✗** (no capture → `RC-CELL-MISSING`, never `RC-VALUE-MISMATCH`), space-before-comma `N01 ,N03` ✗, lowercase `n01,n03` ✗. Neither the frozen sentence nor plan `plan:127` tokenizes a space, so the spaced form is doubly outside: unclaimed and unbound. Verdict: **falsifies-wording** — the capture sentence should say the binding is exactly this regex, not the looser `N<digits>[-N<digits>|,N<digits>...]`. (This is second-order: behavior is coherent; only the description over-promises.)

Clone leg (C1): whether the "clone --shared" layout leg is run by a seat or by the L1 is **unresolvable from my seat dir and from `w1/ExecGateRuns` contents at check time** — I ran the canonical layout only, and I do not cite the clone leg. The C2 doctored/clone legs I cite were run from the L1-committed fixture clone's own tool copies (that mechanism reproduced the frozen tallies bit-for-bit).

## Verdicts

- C1: frontier holds on its stated scope; the residue is the Y-spelling field-lie witness (**one named counterexample on the generalized reading; zero falsifications of the frozen sentences**).
- C2: tallies hold; one wording over-claim on the capture pattern.
- Smallest safe correction: no amendment required to score either claim; for the ledger, keep the X/Y scope note (plan Limits already carries it) and tighten the RC-BEND-SPAN sentence to the exact regex.

{"seat":"CriticClaims","verdict":"findings","notes":"Claims verify on frozen scope (C1: landed/N07/N08/do-nothing tallies + failed_families exact from my runs; C2: PASS 7/7, selftest 14/14, M08 12/14, D1/D2/lie discriminated, coverage 157/157). One genuine counterexample: Y-spelling-only era lie reads met 105/105 x3 (witness receipts/y-field-lie2.py, batt-y2.txt); plan Limits already scope this out. One wording falsification: RC-BEND-SPAN capture reads no binding for comma+space N01, N03 and lowercase n01,n03 (receipts/capture-audit.txt). Ledger draft: .ufo/waves/round-98/w1/CriticClaims/ledger-draft.tsv (5 rows)."}
