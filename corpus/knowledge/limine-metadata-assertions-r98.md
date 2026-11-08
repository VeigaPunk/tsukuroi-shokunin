# What a version-flagged gate must report, and how a battery proves it

source: `corpus/SOURCES.md` S394 (own-work: the `tools/check-limine-pins.py` JSON report contract,
opened 2026-11-08; the MAIN return's field lines at BYTE 16931 and BYTE 17037, with the
CANNOT-EVALUATE early return's copies at BYTE 11230 / 11344 — S394 supersedes S393, whose anchor
labelled the early-return sites as the main return) and S392 (CPython `int()`, opened 2026-11-08;
leading-zero components are legal decimal spellings for an explicit base);
own-work: `tools/limine-pin-battery-r98.py` (`meta_ok`, `fam_refusal_versions_9digit_z`,
`fam_leading_zero_normalize`), `tools/make-r98-bends.py`, and the round-98 receipts under
`.ufo/waves/round-98/before/dev/`.
verified-at: 2026-11-08 (round 98; instruments pinned in
`.ufo/waves/round-98/before/instruments.sha256`).
recheck: on-release + 180d — `python3 tools/limine-pin-battery-r98.py --gate
tools/check-limine-pins.py --runs 3 --json OUT` (verdict `met`, `families_total 105`);
`python3 .ufo/waves/round-95/before/controls/count-runs.py OUT --family
REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE`.

## PC1 — the echo is the flag's spelling, verbatim, and it names its source

`check()` returns `limine_version` as the string the flag was given (the main return's emitter at
BYTE 16931 is `"limine_version": limine_version`, not a re-rendered tuple; the same field text also
appears at BYTE 11230 in the CANNOT-EVALUATE early return) together with
`limine_version_source: "flag"` for an explicit `--limine-version` and `"probe"` for the installed
version probe. Both spellings are observable: `--limine-version 12.09.4` reports
`"limine_version": "12.09.4"` and `"visibility_era": "pre-12.9.5"`, while
`--limine-version 12.9.999999999` reports `"limine_version": "12.9.999999999"` and
`"visibility_era": "12.9.5+"` (`before/dev/` receipts of this round's gate capture). A consumer
that compares the echo to a canonical form would therefore read a conforming gate as wrong, which
is why the battery asserts the flag spelling and not a normalized one.

## PC2 — the era label follows the whole numeric tuple, at the 12.9.5 boundary

`visibility_era` is `pre-12.9.5` when `parse_limine_version(flag)` is below `(12, 9, 5)` and
`12.9.5+` at or above it (main-return emitter at BYTE 17037, early-return copy at BYTE 11344; the
split constant is `VISIBILITY_ERA_SPLIT`).
Because the parser converts each component with `int()` (S392: leading zeros are a legal spelling
for an explicit base, and base 0's refusal does not apply), the label follows the numeric tuple:
`12.09.4` and `000000012.9.4` are era A, `12.000000009.000000005` era B,
`000000000.000000000.000000000` era A and `0.9.999999999` era A, `12.9.999999999` era B. On the fixture in `before/dev/gate-spellings/fixture.conf` (first physical line an entry,
`hash_mismatch_panic: no` in the entry body, a mismatch pin) the era decides whether that key is
visible at all: era A reports `hash_mismatch_panic {"line": 4, "value": "no"}`, era B reports
`null` (the same split the ERA families assert). The `prompt`/`panic` consequence itself follows
from the key's visibility **and** its `no` value; a fixture without the key, or with a non-`no`
value, answers `panic` in both eras.

## PC3 — a family that asserts pins but not the reported fields certifies only half its case

The r97 battery sent exactly these spellings in `REFUSAL-VERSIONS-9DIGIT-Z` and
`LEADING-ZERO-NORMALIZE` and asserted the pin list, rc and verdict — not the echo and not the era
label. The r97 wave measured the gap with two attack gates: one that answered every pin correctly while
reporting a lying `visibility_era` **for the Z tuple only**, and one that echoed the numeric tuple
for a leading-zero spelling; both read `met 105/105` on the r97 battery (ReviewBattery
`attack-1-field.json`, `attack-2.json`; amendments A7). r98 sets the battery's
`check_echo`/`check_era` flags on the two families. The round's own bends are wider than those
attacks — `N07-era-field-lie` lies in the era label for **every** Z/LZ spelling (9-digit third
component or a leading-zero component of more than one digit) and `N08-echo-norm` normalizes the
echo — and they read `103/105` (two families) and `104/105` (one family); the r97 battery stays
blind at `met 105/105` on both. The lesson generalizes: a
family's expectation must cover every field its claim names, or the claim is wider than the
instrument — the class QUALITY 122 names for "must X" sentences.

## PC4 — the source token is asserted, and it is a separate field from the echo

`meta_ok` asserts `got[8] == c.version` **and** `got[9] == "flag"`; a gate that echoes the flag
spelling verbatim but labels its source `probe` fails. Measured on a scratch gate that lies only in
the source for the Z/LZ spellings: `unmet 103/105` with the two families named on the r98 battery,
while the r97 control reads `met 105/105` (ScribeKnowledge's review, §6 PC4; the same shape is
`w1/ReviewBattery/g4-probe-source-r98.json` at `102/105`, which also flips the echo families
because it lies for every explicit flag). A consumer that reads only the echo has verified half of
what the gate reports.

## Limits

- The assertion is bound to the two r97 families. The X and Y boundary families
  (`REFUSAL-VERSIONS-9DIGIT`, `REFUSAL-VERSIONS-9DIGIT-Y`) still do not set `check_echo` or
  `check_era`, so a field lie on their spellings is not caught by this round.
- `N07`'s lie triggers on `len(p) == 9` for the third component or `len(p) > 1 and
  p.startswith("0")` for any component; a bare `0` component does not trigger it (`0.9.4` gets no
  lie), and a field lie on any spelling outside that condition is outside the bend's clause. The
  Y-cap spellings are exactly such a class: a Y-only era lie reads `met 105/105` on both batteries
  (`w1/ReviewBattery/g6-y-era-r98.json`; amendment A4).
- The echo assertion fixes the gate's current contract (verbatim spelling). If the gate ever
  canonicalizes the echo, this family fails by design and the entry's PC1 is what must be
  re-decided, not the family bent.
