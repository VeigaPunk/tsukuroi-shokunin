# What a version-flagged gate must report, and how a battery proves it

source: `corpus/SOURCES.md` S393 (own-work: the `tools/check-limine-pins.py` JSON report contract,
opened 2026-11-08; emission lines at BYTE 11230 and BYTE 11344 of the gate's bytes as pinned in
`.ufo/waves/round-98/before/instruments.sha256`) and S392 (CPython `int()`, opened 2026-11-08;
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

`check()` returns `limine_version` as the string the flag was given (the emitter at BYTE 11230 is
`"limine_version": limine_version`, not a re-rendered tuple) together with
`limine_version_source: "flag"` for an explicit `--limine-version` and `"probe"` for the installed
version probe. Both spellings are observable: `--limine-version 12.09.4` reports
`"limine_version": "12.09.4"` and `"visibility_era": "pre-12.9.5"`, while
`--limine-version 12.9.999999999` reports `"limine_version": "12.9.999999999"` and
`"visibility_era": "12.9.5+"` (`before/dev/` receipts of this round's gate capture). A consumer
that compares the echo to a canonical form would therefore read a conforming gate as wrong, which
is why the battery asserts the flag spelling and not a normalized one.

## PC2 — the era label follows the whole numeric tuple, at the 12.9.5 boundary

`visibility_era` is `pre-12.9.5` when `parse_limine_version(flag)` is below `(12, 9, 5)` and
`12.9.5+` at or above it (emitter at BYTE 11344; the split constant is `VISIBILITY_ERA_SPLIT`).
Because the parser converts each component with `int()` (S392: leading zeros are a legal spelling
for an explicit base, and base 0's refusal does not apply), the label follows the numeric tuple:
`12.09.4` and `000000012.9.4` are era A, `12.000000009.000000005` and `12.9.999999999` era B, and
`000000000.000000000.000000000` era A. The pin consequence on a first-line-entry fixture follows
the same split (`prompt` for era A, `panic` for era B).

## PC3 — a family that asserts pins but not the reported fields certifies only half its case

The r97 battery sent exactly these spellings in `REFUSAL-VERSIONS-9DIGIT-Z` and
`LEADING-ZERO-NORMALIZE` and asserted the pin list, rc and verdict — not the echo and not the era
label. The r97 wave measured the gap: a gate that answers every pin correctly while reporting a
lying `visibility_era` for the Z tuple, and one that echoes the numeric tuple for a leading-zero
spelling, both read `met 105/105` (ReviewBattery `attack-1-field.json`, `attack-2.json`; amendments
A7). r98 sets the battery's `check_echo`/`check_era` flags on those two families, and the same two
lies now read `103/105` (`N07-era-field-lie`, two families) and `104/105` (`N08-echo-norm`, one
family) while the r97 battery remains blind at `105/105` on both bends. The lesson generalizes: a
family's expectation must cover every field its claim names, or the claim is wider than the
instrument — the class QUALITY 122 names for "must X" sentences.

## Limits

- The assertion is bound to the two r97 families. The X and Y boundary families
  (`REFUSAL-VERSIONS-9DIGIT`, `REFUSAL-VERSIONS-9DIGIT-Y`) still do not set `check_echo` or
  `check_era`, so a field lie on their spellings is not caught by this round.
- `N07`'s lie is targeted at the Z/LZ spellings by construction (a 9-digit third component or a
  leading-zero component); a field lie on any other spelling is outside that bend's clause.
- The echo assertion fixes the gate's current contract (verbatim spelling). If the gate ever
  canonicalizes the echo, this family fails by design and the entry's PC1 is what must be
  re-decided, not the family bent.
