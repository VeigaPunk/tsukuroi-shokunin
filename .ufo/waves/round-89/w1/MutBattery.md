# Round 89 w1 — seat MutBattery

Mutation test of the r89 `limine-pins` battery and kill-robustness measurement of its 62 roster
negatives. Lane axes: operability + freshness (host operability and repair); judged on operability.
Everything below was produced in this seat's scratch
`/fast/scratch/hyaku/tsukuroi-r89/MutBattery/`; no lane file was edited, no commit, push or jj/git
mutation was run in the lane or the fleet root.

## 1. Instruments measured (frozen; not edited)

| instrument | path | sha256 |
|---|---|---|
| battery | `tools/limine-pin-battery-r89.py` | `3bae11e939cf6900fd29bb24033e6d134de8bf0ae7069cdec3f12f716e8df7f8` |
| counter | `tools/battery-discrimination-r89.py` | `c666323a35e736fc534634b6b826313e5ff2895dff9d3df3f8bd8c1cd0c9a0e5` |
| roster | `.ufo/waves/round-89/before/roster/roster-r89.json` | `799b1fb47587432f7fb47d171e312892a3dfb439bc2980077dbfb8642f3415cc` |
| freeze manifest | `.ufo/waves/round-89/before/freeze-manifest.sha256` | `f95bdbfe1947a0ee830a011838261af6a14815c1213b476aabd9c71a478e5387` |

Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` =
`665408cc45a88ed49717e22f4593e8e6152ac665`. Working tree at measurement time: sibling-seat edits only
(`M corpus/QUALITY.md`, `?? corpus/lessons/round-89.md`, `?? .ufo/waves/round-89/after/m1-sweep.txt`,
`?? .ufo/waves/round-89/w1*`); no file under `tools/` or `.ufo/waves/round-89/before/` changed.

Clean copy: `git clone --shared <lane> $S/lane`; `git -C $S/lane rev-parse --show-toplevel` = the clone;
clone master `665408cc`; battery and counter bytes in the clone carry the sha256 above. Mutant sources
are generated from the lane bytes by counted literal replacement (`make_mutants.py`), never from the clone.

Baseline on the pristine battery, lane counter, this seat's environment (one counter run):

```
$ python3 <lane>/tools/battery-discrimination-r89.py --battery <lane>/tools/limine-pin-battery-r89.py \
      --runs 1 --jobs 4 --scratch "$S/c" --json $S/mut/baseline.counter.json
run 1 positives 3/3 negatives 62/62 errors 0 failures -
verdict met
EXIT=0        (real 9m19s; receipt isolation "isolated", error_rows 0)
```

## 2. Method

1. **19 single-point mutants** of the battery's bytes, each compile-checked and each verified to keep
   `tuple(FAMILIES) == FAMILY_ROSTER` (the battery is a usage error otherwise):
   - the 12 r89 families (BLANK-CLASS, OPTIONAL-MISSING, OPTIONAL-UNRESOLVED, EMPTY-PIN-LIST,
     DOUBLE-DOLLAR, ENTRY-LABEL-EDGES, PANIC-VALUE-BLANKS, CR-INTERNAL, RESOURCE-CASE, KEY-EQUALS,
     EMPTY-PATH, OPTIONAL-KEY-CASE) deleted from `FAMILIES` **and** `FAMILY_ROSTER`;
   - `r8_ok`'s value comparison weakened to `isinstance(pm, dict) and pm.get("line") == want_panic[0]`
     (the r88 M18 field);
   - the r88 p 0.6 CRLF draw restored in `fam_whitespace` (`if c.rng.random() < 0.6: c.eol = "\r\n"`);
   - five of this seat's choice: drop the process-exit-code comparison, ignore the consequence field,
     `CASES_PER_FAMILY = 1`, drop the `entry` comparison, drop the `hash_mismatch_panic.line` comparison.
   Each mutant was run through the frozen counter exactly as the claim's counting command does
   (`--runs 1 --jobs 4`), with `--battery <mutant>`; the battery is not in the freeze manifest, so the
   counter's manifest check is unaffected. Every mutant receipt records which roster negatives read
   `met` (escaped).
2. **Kill robustness of the pristine battery**: each of the 62 NEGATIVE roster gates was handed to the
   battery directly, `--runs 10`, one separate `--work` per gate; per run the receipt records
   `unmet|met` and `failed_families`.
3. **Controls**: four degenerate batteries (constant `met`, constant `unmet`, crash/missing receipt)
   and the pristine battery's own `--selftest`.

Commands actually run (per mutant, `$S=/fast/scratch/hyaku/tsukuroi-r89/MutBattery`):

```
python3 <lane>/tools/battery-discrimination-r89.py --battery "$S/mut/src/<mutant>.py" \
    --runs 1 --jobs 4 --scratch "$S/c" --json "$S/mut/<mutant>.counter.json"
python3 <lane>/tools/limine-pin-battery-r89.py --gate <roster>/<negative>.py \
    --runs 10 --work "$S/sw/<negative>" --json "$S/sweep/<negative>.json"
```

`--scratch "$S/c"` (45 bytes) rather than the claim's `--scratch "$S/work"` because the counter cannot
bind at `$S/work`; that defect is section 7.

Concurrency, stated for the record since the host was loaded (~90-100 runnable, other seats): the 62-gate
sweep ran as two shards of six battery processes; the 19 mutant runs ran as up to six counter processes
concurrently (each `--jobs 4`). Wall times below are therefore not comparable to a quiet host; the
receipts, not the clocks, are the evidence. Verbatim sample (`del-blank-class`):

```
run 1 positives 3/3 negatives 61/62 errors 0 failures N-f01-any-whitespace-blank-class
verdict unmet
EXIT=1
```

## 3. Controls: the counter is not trivially satisfiable

| battery given to the counter | positives | negatives | error rows | counter verdict | exit |
|---|---|---|---|---|---|
| constant `met` receipt (no cases run) | 3/3 | 0/62 | 0 | unmet | 1 |
| constant `unmet` receipt | 0/3 | 62/62 | 0 | unmet | 1 |
| crash / no receipt (`raise SystemExit(7)`) | 0/3 | 0/62 | 65 | could-not-evaluate | 3 |
| pristine battery (baseline) | 3/3 | 62/62 | 0 | met | 0 |

The error-row path behaves as the KILL RULE states: 65 error rows (a missing receipt is an error, never
a verdict) force `could-not-evaluate` (exit 3), and a battery that answers `met` for everything is
rejected as `unmet`, never as `met`. The pristine battery's own selftest: `selftest PASS 15/15`.

## 4. Mutants: what the frozen counter detects, `--runs 1 --jobs 4`

| mutant | battery sha256 | counter verdict | P | N | err | pre-registered detector | observed escapes | positives failed | note |
|---|---|---|---|---|---|---|---|---|---|
| cases-per-family-1 | 597074409a39 | met | 3/3 | 62/62 | 0 | none expected (every family's case is defect-exposing or equivalent) | none | none | SURVIVOR: no roster negative needs more than one case per family |
| crlf-p06-r88 | c9a39f87c009 | met | 3/3 | 62/62 | 0 | g15, m22 (only when no case draws CRLF: p = 0.4^4 = 2.56% per gate per run) | none | none | SURVIVOR: g15/m22 are also killed by CR-INTERNAL in every run, so the roster cannot see the weaker CRLF draw at all |
| del-blank-class | 2b073cd798d1 | unmet | 3/3 | 61/62 | 0 | f01 | N-f01-any-whitespace-blank-class | none |  |
| del-cr-internal | 36feefbeee3f | unmet | 3/3 | 61/62 | 0 | f14, g00 | N-f14-cr-stripped-only-trailing | none | g00 did not escape: EMPTY-PATH kills it; the family is load-bearing for f14 only |
| del-double-dollar | 5180be4f9b7c | unmet | 3/3 | 61/62 | 0 | f07 | N-f07-dollar-lstrip-all | none |  |
| del-empty-path | 0ada0f575316 | unmet | 3/3 | 61/62 | 0 | h10, g00 | N-h10-empty-path-pin-ignored | none | g00 did not escape: CR-INTERNAL kills it; the family is load-bearing for h10 only |
| del-empty-pin-list | 655ea22a14f4 | unmet | 3/3 | 61/62 | 0 | f06 | N-f06-empty-pin-list-cannot-evaluate | none |  |
| del-entry-label-edges | fda40b5d9f6f | unmet | 3/3 | 59/62 | 0 | f08, f19, h19 | N-f08-entry-label-trailing-plus, N-f19-entry-label-not-trimmed, N-h19-entry-plus-kept | none | all three entry-label negatives escape; the family is load-bearing for all three |
| del-key-equals | a3fc0fbba3da | unmet | 3/3 | 61/62 | 0 | h01 | N-h01-key-sep-equals | none |  |
| del-optional-key-case | 8f65630ec90c | unmet | 3/3 | 61/62 | 0 | h11 | N-h11-optional-case-sensitive | none |  |
| del-optional-missing | 051f54cb4f97 | unmet | 3/3 | 61/62 | 0 | f03 | N-f03-optional-missing-skip | none |  |
| del-optional-unresolved | 94d8873facd2 | unmet | 3/3 | 61/62 | 0 | f16 | N-f16-optional-unresolved-skip | none |  |
| del-panic-value-blanks | 03ccf2d236c3 | unmet | 3/3 | 61/62 | 0 | f12, m31 | N-f12-panic-value-raw-trailing-blanks | none | m31 did not escape: PANIC-METADATA/PANIC-FIRST also report a panic value with blanks; the family is load-bearing for f12 only |
| del-resource-case | cac49a204b4b | unmet | 3/3 | 60/62 | 0 | f18, h20 | N-f18-resource-case-insensitive, N-h20-resource-case-insensitive | none | both resource-case negatives escape |
| drop-exitcode-compare | 47a5e243238e | met | 3/3 | 62/62 | 0 | none expected (every roster gate exits its own rc) | none | none | SURVIVOR: no roster gate misreports its process exit code; only the battery's own selftest (lie-exit-code) exercises that clause |
| ignore-consequence | 54afa854f20a | unmet | 3/3 | 54/62 | 0 | m15, g12, g13, m16, m17, m18 (consequence-only defects) | N-f03-optional-missing-skip, N-f16-optional-unresolved-skip, N-h11-optional-case-sensitive, N-m15-panic-default-prompt, N-m16-panic-no-inverted, N-m17-secureboot-ignored, N-m18-optional-no-skip, N-m27-optional-wallpaper-dropped | none | eight consequence-only defects escape |
| r8ok-no-entry-check | 2bd346d75e8d | unmet | 3/3 | 58/62 | 0 | m24, f08, f19, h19 | N-f08-entry-label-trailing-plus, N-f19-entry-label-not-trimmed, N-h19-entry-plus-kept, N-m24-entry-not-tracked | none | four entry-field defects escape |
| r8ok-no-panic-line-check | 140cc63dd280 | unmet | 3/3 | 61/62 | 0 | m25 | N-m25-panic-line-metadata-zero | none | the panic-line defect escapes |
| r8ok-value-weakened | 4720413a3125 | unmet | 3/3 | 61/62 | 0 | m31 (the only gate whose reported panic value is wrong while its consequence is right) | N-m31-panic-value-untrimmed | none | the panic-value defect escapes; f12 stays killed by its wrong consequence |

Killed (counter reads `unmet`): 16/19 — del-blank-class, del-cr-internal, del-double-dollar, del-empty-path, del-empty-pin-list, del-entry-label-edges, del-key-equals, del-optional-key-case, del-optional-missing, del-optional-unresolved, del-panic-value-blanks, del-resource-case, ignore-consequence, r8ok-no-entry-check, r8ok-no-panic-line-check, r8ok-value-weakened.

Survived (counter reads `met`): 3/19 — cases-per-family-1, crlf-p06-r88, drop-exitcode-compare.

Cross-check against section 5: a deletion mutant should escape exactly the negatives whose sole killing family is the deleted one.

| mutant | predicted escapes (sole killer from the 10-run sweep) | observed escapes | match |
|---|---|---|---|
| del-blank-class | N-f01-any-whitespace-blank-class | N-f01-any-whitespace-blank-class | yes |
| del-cr-internal | N-f14-cr-stripped-only-trailing | N-f14-cr-stripped-only-trailing | yes |
| del-double-dollar | N-f07-dollar-lstrip-all | N-f07-dollar-lstrip-all | yes |
| del-empty-path | N-h10-empty-path-pin-ignored | N-h10-empty-path-pin-ignored | yes |
| del-empty-pin-list | N-f06-empty-pin-list-cannot-evaluate | N-f06-empty-pin-list-cannot-evaluate | yes |
| del-entry-label-edges | N-f08-entry-label-trailing-plus, N-f19-entry-label-not-trimmed, N-h19-entry-plus-kept | N-f08-entry-label-trailing-plus, N-f19-entry-label-not-trimmed, N-h19-entry-plus-kept | yes |
| del-key-equals | N-h01-key-sep-equals | N-h01-key-sep-equals | yes |
| del-optional-key-case | N-h11-optional-case-sensitive | N-h11-optional-case-sensitive | yes |
| del-optional-missing | N-f03-optional-missing-skip | N-f03-optional-missing-skip | yes |
| del-optional-unresolved | N-f16-optional-unresolved-skip | N-f16-optional-unresolved-skip | yes |
| del-panic-value-blanks | N-f12-panic-value-raw-trailing-blanks | N-f12-panic-value-raw-trailing-blanks | yes |
| del-resource-case | N-f18-resource-case-insensitive, N-h20-resource-case-insensitive | N-f18-resource-case-insensitive, N-h20-resource-case-insensitive | yes |

Exact matches: 12/12 deletion mutants.

Reading the table: a deletion mutant is `unmet` exactly when the deleted family was the sole killer of at
least one roster negative; every one of the 12 r89 families is load-bearing for between one and three
negatives. Three mutants survive, and each is a coverage finding rather than a contract change:

- `cases-per-family-1` (`CASES_PER_FAMILY = 4` -> `1`) survives: no roster negative needs more than one
  case per family, so the four-case repetition the claim describes is not exercised by the roster. The
  battery reads `met` with 50 cases per run exactly as with 200.
- `crlf-p06-r88` (the r88 `if rng.random() < 0.6: eol = "\r\n"` draw) survives: the two CR-blind
  negatives (`g15-no-cr-strip`, `m22-cr-not-stripped`) are killed by CR-INTERNAL in 10/10 pristine runs
  (section 5), so weakening WHITESPACE-CRLF's CRLF draw cannot let either of them escape. The r89 fix is
  sound but its claimed effect is invisible to C1.
- `drop-exitcode-compare` (the battery stops comparing the gate's process exit code with its JSON `rc`)
  survives: every roster gate exits its own `rc`, so no negative detects the dropped check. That clause
  is exercised only by the battery's own selftest (`lie-exit-code PASS`, section 3), not by the counter.

## 5. Kill robustness of the 62 NEGATIVE roster gates (pristine battery, 10 direct runs each)

| negative | unmet/10 | killer families (union over 10 runs) | runs with exactly one killer |
|---|---|---|---|
| N-f01-any-whitespace-blank-class | 10/10 | BLANK-CLASS | 10 |
| N-f03-optional-missing-skip | 10/10 | OPTIONAL-MISSING | 10 |
| N-f06-empty-pin-list-cannot-evaluate | 10/10 | EMPTY-PIN-LIST | 10 |
| N-f07-dollar-lstrip-all | 10/10 | DOUBLE-DOLLAR | 10 |
| N-f08-entry-label-trailing-plus | 10/10 | ENTRY-LABEL-EDGES | 10 |
| N-f12-panic-value-raw-trailing-blanks | 10/10 | PANIC-VALUE-BLANKS | 10 |
| N-f14-cr-stripped-only-trailing | 10/10 | CR-INTERNAL | 10 |
| N-f16-optional-unresolved-skip | 10/10 | OPTIONAL-UNRESOLVED | 10 |
| N-f18-resource-case-insensitive | 10/10 | RESOURCE-CASE | 10 |
| N-f19-entry-label-not-trimmed | 10/10 | ENTRY-LABEL-EDGES | 10 |
| N-g00-trailing-cr-only | 10/10 | CR-INTERNAL, EMPTY-PATH | 0 |
| N-g01-loose-key | 10/10 | CR-INTERNAL, EMPTY-PATH, KEY-SPACING | 0 |
| N-g02-no-paren | 10/10 | CR-INTERNAL, EMPTY-PATH, NO-PAREN | 0 |
| N-g03-format-after-resolve | 10/10 | CR-INTERNAL, EMPTY-PATH, FORMAT-BEFORE-RESOLVE | 0 |
| N-g04-hashformat-optional-panic | 10/10 | CR-INTERNAL, EMPTY-PATH, OPTIONAL-HASH-FORMAT | 0 |
| N-g05-last-uri-sep | 10/10 | CR-INTERNAL, EMPTY-PATH, FIRST-URI-SEP | 0 |
| N-g06-any-empty-root | 10/10 | CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, EMPTY-ROOT-RESOURCE, RESOURCE-CASE | 0 |
| N-g07-panic-key-case | 10/10 | CR-INTERNAL, EMPTY-PATH, PANIC-KEY-CASE | 0 |
| N-g08-sb-presence | 10/10 | ALL-PIN-KEYS, CR-INTERNAL, EMPTY-PATH, HOST-SHAPE, MULTI-FAULT, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-VALUE-BLANKS, SB-FLAG-ZERO | 0 |
| N-g09-nohash | 10/10 | ALL-PIN-KEYS, CR-INTERNAL, EMPTY-PATH, ENTRY-LABEL, ENTRY-LABEL-EDGES, FIRST-URI-SEP, GZ-RAW, HOST-SHAPE, KEY-CASE, KEY-SPACING, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MULTI-FAULT, OPTIONAL-KEY-CASE, OPTIONAL-SKIP, PANIC-DEFAULT, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-RAW-DECOY, PANIC-VALUE-BLANKS, PAREN-PATH, SB-FLAG-ZERO, SECUREBOOT, WHITESPACE-CRLF | 0 |
| N-g10-raw-panic-scan | 10/10 | CR-INTERNAL, EMPTY-PATH, PANIC-KEY-CASE, PANIC-RAW-DECOY | 0 |
| N-g11-first-hash-control | 10/10 | CR-INTERNAL, EMPTY-PATH, LAST-HASH | 0 |
| N-g12-any-non-yes-control | 10/10 | CR-INTERNAL, EMPTY-PATH, PANIC-NO-ONLY, PANIC-NON-NO | 0 |
| N-g13-constant-panic-control | 10/10 | ALL-PIN-KEYS, CR-INTERNAL, EMPTY-PATH, HOST-SHAPE, MULTI-FAULT, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-VALUE-BLANKS, SB-FLAG-ZERO | 0 |
| N-g14-eacces-rc1 | 10/10 | CONF-UNREADABLE, CR-INTERNAL, EMPTY-PATH | 0 |
| N-g15-no-cr-strip | 10/10 | CR-INTERNAL, EMPTY-PATH, WHITESPACE-CRLF | 0 |
| N-g16-drop-global-dtb | 10/10 | ALL-PIN-KEYS, CR-INTERNAL, EMPTY-PATH, KEY-CASE | 0 |
| N-h01-key-sep-equals | 10/10 | KEY-EQUALS | 10 |
| N-h10-empty-path-pin-ignored | 10/10 | EMPTY-PATH | 10 |
| N-h11-optional-case-sensitive | 10/10 | OPTIONAL-KEY-CASE | 10 |
| N-h19-entry-plus-kept | 10/10 | ENTRY-LABEL-EDGES | 10 |
| N-h20-resource-case-insensitive | 10/10 | RESOURCE-CASE | 10 |
| N-m02-no-blank-strip | 10/10 | ALL-PIN-KEYS, BLANK-CLASS, COMMENT-DECOY, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, EMPTY-ROOT-RESOURCE, ENTRY-LABEL, ENTRY-LABEL-EDGES, FIRST-URI-SEP, FORMAT-BEFORE-RESOLVE, GZ-RAW, HASH-LENGTH, HASH-NONHEX, HASH-UPPER, HOST-SHAPE, KEY-CASE, KEY-EQUALS, KEY-SPACING, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MISSING, MULTI-FAULT, NO-PAREN, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-MISSING, OPTIONAL-SKIP, OPTIONAL-UNRESOLVED, PANIC-DEFAULT, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-RAW-DECOY, PANIC-VALUE-BLANKS, PAREN-PATH, POSITIVE, RESOURCE-CASE, ROOT-ON-BOOT, SB-FLAG-ZERO, SECUREBOOT, UNHASHED-DECOYS, UNRESOLVED, WHITESPACE-CRLF | 0 |
| N-m03-key-case-sensitive | 10/10 | KEY-CASE, OPTIONAL-KEY-CASE, PANIC-KEY-CASE | 0 |
| N-m04-first-hash | 10/10 | LAST-HASH | 10 |
| N-m05-last-open-paren | 10/10 | PAREN-PATH | 10 |
| N-m06-hash-127 | 10/10 | ALL-PIN-KEYS, BLANK-CLASS, COMMENT-DECOY, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, EMPTY-ROOT-RESOURCE, ENTRY-LABEL, ENTRY-LABEL-EDGES, FIRST-URI-SEP, FORMAT-BEFORE-RESOLVE, GZ-RAW, HASH-LENGTH, HASH-NONHEX, HASH-UPPER, HOST-SHAPE, KEY-CASE, KEY-EQUALS, KEY-SPACING, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MISSING, MULTI-FAULT, NO-PAREN, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-MISSING, OPTIONAL-SKIP, OPTIONAL-UNRESOLVED, PANIC-DEFAULT, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-RAW-DECOY, PANIC-VALUE-BLANKS, PAREN-PATH, POSITIVE, RESOURCE-CASE, ROOT-ON-BOOT, SB-FLAG-ZERO, SECUREBOOT, UNHASHED-DECOYS, UNRESOLVED, WHITESPACE-CRLF | 0 |
| N-m07-hash-129 | 10/10 | ALL-PIN-KEYS, BLANK-CLASS, COMMENT-DECOY, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, EMPTY-ROOT-RESOURCE, ENTRY-LABEL, ENTRY-LABEL-EDGES, FIRST-URI-SEP, FORMAT-BEFORE-RESOLVE, GZ-RAW, HASH-LENGTH, HASH-NONHEX, HASH-UPPER, HOST-SHAPE, KEY-CASE, KEY-EQUALS, KEY-SPACING, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MISSING, MULTI-FAULT, NO-PAREN, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-MISSING, OPTIONAL-SKIP, OPTIONAL-UNRESOLVED, PANIC-DEFAULT, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-RAW-DECOY, PANIC-VALUE-BLANKS, PAREN-PATH, POSITIVE, RESOURCE-CASE, ROOT-ON-BOOT, SB-FLAG-ZERO, SECUREBOOT, UNHASHED-DECOYS, UNRESOLVED, WHITESPACE-CRLF | 0 |
| N-m08-hex-lowercase-only | 10/10 | HASH-UPPER | 10 |
| N-m09-any-resource-resolves | 10/10 | DOUBLE-DOLLAR, EMPTY-ROOT-RESOURCE, MULTI-FAULT, OPTIONAL-UNRESOLVED, RESOURCE-CASE, ROOT-ON-BOOT, UNRESOLVED | 0 |
| N-m10-root-ignored | 10/10 | OPTIONAL-UNRESOLVED, ROOT-ON-BOOT, UNRESOLVED | 0 |
| N-m11-gzip-decompress | 10/10 | ALL-PIN-KEYS, DOUBLE-DOLLAR, GZ-RAW | 0 |
| N-m12-missing-as-unresolved | 10/10 | EMPTY-PATH, MISSING, MULTI-FAULT, OPTIONAL-MISSING | 0 |
| N-m13-missing-as-ok | 10/10 | EMPTY-PATH, MISSING, MULTI-FAULT, OPTIONAL-MISSING | 0 |
| N-m14-panic-last-wins | 10/10 | PANIC-FIRST, PANIC-METADATA | 0 |
| N-m15-panic-default-prompt | 10/10 | ALL-PIN-KEYS, CR-INTERNAL, ENTRY-LABEL, ENTRY-LABEL-EDGES, FIRST-URI-SEP, GZ-RAW, KEY-CASE, KEY-SPACING, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MULTI-FAULT, PANIC-DEFAULT, PANIC-RAW-DECOY, PAREN-PATH, WHITESPACE-CRLF | 0 |
| N-m16-panic-no-inverted | 10/10 | ALL-PIN-KEYS, HOST-SHAPE, MULTI-FAULT, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-RAW-DECOY, PANIC-VALUE-BLANKS, SB-FLAG-ZERO | 0 |
| N-m17-secureboot-ignored | 10/10 | SECUREBOOT | 10 |
| N-m18-optional-no-skip | 10/10 | ALL-PIN-KEYS, OPTIONAL-KEY-CASE, OPTIONAL-SKIP | 0 |
| N-m19-degraded-only-mismatch | 10/10 | BLANK-CLASS, EMPTY-PATH, FORMAT-BEFORE-RESOLVE, HASH-LENGTH, HASH-NONHEX, MISSING, OPTIONAL-HASH-FORMAT, OPTIONAL-MISSING | 0 |
| N-m20-unresolved-precedence-first | 10/10 | MULTI-FAULT | 10 |
| N-m21-lines-0-based | 10/10 | ALL-PIN-KEYS, BLANK-CLASS, COMMENT-DECOY, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, EMPTY-PIN-LIST, EMPTY-ROOT-RESOURCE, ENTRY-LABEL, ENTRY-LABEL-EDGES, FIRST-URI-SEP, FORMAT-BEFORE-RESOLVE, GZ-RAW, HASH-LENGTH, HASH-NONHEX, HASH-UPPER, HOST-SHAPE, KEY-CASE, KEY-EQUALS, KEY-SPACING, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MISSING, MULTI-FAULT, NO-PAREN, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-MISSING, OPTIONAL-SKIP, OPTIONAL-UNRESOLVED, PANIC-DEFAULT, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-RAW-DECOY, PANIC-VALUE-BLANKS, PAREN-PATH, POSITIVE, RESOURCE-CASE, ROOT-ON-BOOT, SB-FLAG-ZERO, SECUREBOOT, UNHASHED-DECOYS, UNRESOLVED, WHITESPACE-CRLF | 0 |
| N-m22-cr-not-stripped | 10/10 | CR-INTERNAL, WHITESPACE-CRLF | 0 |
| N-m23-value-not-lstripped | 10/10 | ALL-PIN-KEYS, BLANK-CLASS, COMMENT-DECOY, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, EMPTY-PIN-LIST, EMPTY-ROOT-RESOURCE, ENTRY-LABEL, ENTRY-LABEL-EDGES, FIRST-URI-SEP, FORMAT-BEFORE-RESOLVE, GZ-RAW, HASH-LENGTH, HASH-NONHEX, HASH-UPPER, HOST-SHAPE, KEY-CASE, KEY-EQUALS, KEY-SPACING, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MISSING, MULTI-FAULT, NO-PAREN, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-MISSING, OPTIONAL-SKIP, OPTIONAL-UNRESOLVED, PANIC-DEFAULT, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-RAW-DECOY, PANIC-VALUE-BLANKS, PAREN-PATH, POSITIVE, RESOURCE-CASE, ROOT-ON-BOOT, SB-FLAG-ZERO, SECUREBOOT, UNHASHED-DECOYS, UNRESOLVED, WHITESPACE-CRLF | 0 |
| N-m24-entry-not-tracked | 10/10 | ALL-PIN-KEYS, BLANK-CLASS, COMMENT-DECOY, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, EMPTY-ROOT-RESOURCE, ENTRY-LABEL, ENTRY-LABEL-EDGES, FIRST-URI-SEP, FORMAT-BEFORE-RESOLVE, GZ-RAW, HASH-LENGTH, HASH-NONHEX, HASH-UPPER, HOST-SHAPE, KEY-CASE, KEY-EQUALS, KEY-SPACING, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MISSING, MULTI-FAULT, NO-PAREN, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-MISSING, OPTIONAL-SKIP, OPTIONAL-UNRESOLVED, PANIC-DEFAULT, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-RAW-DECOY, PANIC-VALUE-BLANKS, PAREN-PATH, POSITIVE, RESOURCE-CASE, ROOT-ON-BOOT, SB-FLAG-ZERO, SECUREBOOT, UNHASHED-DECOYS, UNRESOLVED, WHITESPACE-CRLF | 0 |
| N-m25-panic-line-metadata-zero | 10/10 | ALL-PIN-KEYS, EMPTY-PIN-LIST, HOST-SHAPE, MULTI-FAULT, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-SKIP, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-RAW-DECOY, PANIC-VALUE-BLANKS, SB-FLAG-ZERO, SECUREBOOT | 0 |
| N-m26-pin-keys-path-only | 10/10 | ALL-PIN-KEYS, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, GZ-RAW, KEY-CASE, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-MISSING, OPTIONAL-SKIP, OPTIONAL-UNRESOLVED, PAREN-PATH | 0 |
| N-m27-optional-wallpaper-dropped | 10/10 | ALL-PIN-KEYS, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-SKIP | 0 |
| N-m28-hash-case-sensitive-compare | 10/10 | HASH-UPPER | 10 |
| N-m29-sha256-instead-of-blake2b | 10/10 | ALL-PIN-KEYS, BLANK-CLASS, COMMENT-DECOY, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, EMPTY-ROOT-RESOURCE, ENTRY-LABEL, ENTRY-LABEL-EDGES, FIRST-URI-SEP, FORMAT-BEFORE-RESOLVE, GZ-RAW, HASH-LENGTH, HASH-NONHEX, HASH-UPPER, HOST-SHAPE, KEY-CASE, KEY-EQUALS, KEY-SPACING, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MISSING, MULTI-FAULT, NO-PAREN, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-MISSING, OPTIONAL-SKIP, OPTIONAL-UNRESOLVED, PANIC-DEFAULT, PANIC-KEY-CASE, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-VALUE-BLANKS, PAREN-PATH, POSITIVE, RESOURCE-CASE, ROOT-ON-BOOT, SB-FLAG-ZERO, SECUREBOOT, UNHASHED-DECOYS, UNRESOLVED, WHITESPACE-CRLF | 0 |
| N-m30-last-pin-only | 10/10 | ALL-PIN-KEYS, BLANK-CLASS, CR-INTERNAL, DOUBLE-DOLLAR, EMPTY-PATH, EMPTY-ROOT-RESOURCE, ENTRY-LABEL, ENTRY-LABEL-EDGES, FIRST-URI-SEP, FORMAT-BEFORE-RESOLVE, GZ-RAW, HASH-LENGTH, HASH-NONHEX, HASH-UPPER, HOST-SHAPE, KEY-CASE, KEY-SPACING, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MISSING, MULTI-FAULT, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-MISSING, OPTIONAL-SKIP, OPTIONAL-UNRESOLVED, PANIC-DEFAULT, PANIC-KEY-CASE, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-VALUE-BLANKS, PAREN-PATH, POSITIVE, RESOURCE-CASE, ROOT-ON-BOOT, SB-FLAG-ZERO, SECUREBOOT, UNRESOLVED, WHITESPACE-CRLF | 0 |
| N-m31-panic-value-untrimmed | 10/10 | ALL-PIN-KEYS, EMPTY-PIN-LIST, HOST-SHAPE, MULTI-FAULT, OPTIONAL-HASH-FORMAT, OPTIONAL-KEY-CASE, OPTIONAL-SKIP, PANIC-FIRST, PANIC-KEY-CASE, PANIC-METADATA, PANIC-NO-ONLY, PANIC-NON-NO, PANIC-RAW-DECOY, PANIC-VALUE-BLANKS, SB-FLAG-ZERO, SECUREBOOT | 0 |

Receipts: 62/62 NEGATIVE gates.

Every one of the 62 negatives read `unmet` in all 10 runs (620/620). The union column names every family
that failed at least once in 10 runs; 21 negatives have a single-family union and the rest have 2-48
families, so most of the roster is redundantly killed.

## 6. Flake risk (r88 R88-R2 class)

Measured, 62 NEGATIVE gates x 10 direct runs of the pristine battery: 62/62 read `unmet` in 10/10 runs; 21 gates have a single-family killer union; 41 have a multi-family union.

No gate fell below 10/10.

Single-family killer unions (the r88 R88-R2 question):

| negative | sole killer family | draw that the family makes per case | can the draw mask the defect? |
|---|---|---|---|
| N-f01-any-whitespace-blank-class | BLANK-CLASS | one of 6 control whitespace chars (`\x0b \x0c \x1c-\x1f`) | no - every char is stripped by a Unicode-blank gate |
| N-f03-optional-missing-skip | OPTIONAL-MISSING | wallpaper|term_font | no - both keys are optional under R6 |
| N-f06-empty-pin-list-cannot-evaluate | EMPTY-PIN-LIST | whether a panic line is present; 1-3 entry blocks | no - any panic/entry mix has no pin |
| N-f07-dollar-lstrip-all | DOUBLE-DOLLAR | none (fixed fixture) | no - fixed |
| N-f08-entry-label-trailing-plus | ENTRY-LABEL-EDGES | which of the 3 entry forms comes first; blanks/plus prefix | no - all three forms are emitted in every case |
| N-f12-panic-value-raw-trailing-blanks | PANIC-VALUE-BLANKS | no|No|NO and which blanks | no - blanks are always >= 1 and all values are `no` |
| N-f14-cr-stripped-only-trailing | CR-INTERNAL | which key and CR positions (always internal) | no - the CR is internal by construction |
| N-f16-optional-unresolved-skip | OPTIONAL-UNRESOLVED | wallpaper|term_font and one of 4 non-resolving resources | no - every resource is non-boot |
| N-f18-resource-case-insensitive | RESOURCE-CASE | which of 4 wrong-case spellings (all wrong) | no - all four spellings are wrong |
| N-f19-entry-label-not-trimmed | ENTRY-LABEL-EDGES | which of the 3 entry forms comes first; blanks/plus prefix | no - all three forms are emitted in every case |
| N-h01-key-sep-equals | KEY-EQUALS | blank after '=' (all three forms are pins) | no - every form yields a pin for an '='-accepting gate |
| N-h10-empty-path-pin-ignored | EMPTY-PATH | path|kernel_path (both are pins) | no - both keys are pins |
| N-h11-optional-case-sensitive | OPTIONAL-KEY-CASE | which of 6 non-lowercase key spellings (all wrong) | no - all six spellings carry uppercase |
| N-h19-entry-plus-kept | ENTRY-LABEL-EDGES | which of the 3 entry forms comes first; blanks/plus prefix | no - all three forms are emitted in every case |
| N-h20-resource-case-insensitive | RESOURCE-CASE | which of 4 wrong-case spellings (all wrong) | no - all four spellings are wrong |
| N-m04-first-hash | LAST-HASH | none (fixed fixture: file names carry '#' and 'x') | no - fixed |
| N-m05-last-open-paren | PAREN-PATH | the digit inside the stored path's '(' ... ')' | no - any digit leaves the '(' ... ')' in the path |
| N-m08-hex-lowercase-only | HASH-UPPER | all-upper vs per-character mixed case | no - p(all-lowercase in the mixed branch) = 2^-128, all-upper always carries uppercase |
| N-m17-secureboot-ignored | SECUREBOOT | none (fixed fixture: sb enabled, panic value no) | no - fixed |
| N-m20-unresolved-precedence-first | MULTI-FAULT | the order of a fixed six-kind list (shuffled) | no - every kind is emitted in every case |
| N-m28-hash-case-sensitive-compare | HASH-UPPER | all-upper vs per-character mixed case | no - p(all-lowercase in the mixed branch) = 2^-128, all-upper always carries uppercase |

Families whose draw CAN mask a defect (r88 R88-R2 shape) but are not the sole killer of any roster negative: HASH-LENGTH (line 298 draws one of {127,129,64,0} per case) and the optional-key draw (lines 727/735/850). Measured: m06-hash-127 and m07-hash-129 are killed by 47/50 families including POSITIVE (3/50 passed on each of 3 runs), so HASH-LENGTH is never their sole killer; no roster gate is wrong for only one optional key. PANIC-NO-ONLY's 50/50 no|non-no branch is covered in both branches by PANIC-FIRST, so m16 is not a single-draw kill.

Conclusion: no NEGATIVE in the frozen roster is killed by a single family whose draw can mask its defect; the measured kill robustness is 62/62 negatives x 10/10 runs = 620/620.

Redundancy the roster does have: g15-no-cr-strip and m22-cr-not-stripped are killed by CR-INTERNAL in 10/10 runs as well as by WHITESPACE-CRLF, so the r89 CRLF determinism fix cannot be observed by the roster at all (mutant crlf-p06-r88 survives, section 4). The single-family unions above are the load-bearing detectors; every other negative has 2-48 killing families.

## 7. Operability findings (reported, not fixed; patches under `w1/MutBattery/`)

### 7.1 The counter cannot bind its launcher socket at the documented scratch path

The counting command in the declaration uses `--scratch "$S/work"`. At this seat root
(`/fast/scratch/hyaku/tsukuroi-r89/MutBattery`, 43 bytes) that is 48 bytes, and the counter dies before
the first gate:

```
$ python3 <lane>/tools/battery-discrimination-r89.py --battery <lane>/tools/limine-pin-battery-r89.py \
      --runs 1 --jobs 4 --scratch "$S/work"
  File "<lane>/tools/battery-discrimination-r89.py", line 216, in one
    sock.bind(sp)
OSError: AF_UNIX path too long
EXIT=1
```

Arithmetic (measured boundary: 107-byte paths bind, 108-byte fail): the socket path is
`len(--scratch) + 62` (`battery-discrimination-r89-` + 8, `bd-` + 8, `/s` + `token_hex(6)`), so the
counter only binds when `--scratch` is at most 45 bytes; `$S/work` needs a seat name of at most 7
characters. Measured in this seat: `$S/c` (45) binds at 107; `$S/p` (45) binds; `$S/pf` (46) fails at
108; `$S/work` (48) fails at 110; `$S/work-baseline` (57) fails at 119. The exception is uncaught:
exit 1 is the counter's `unmet` exit code, no `--json` receipt is written, and it never reaches the
`could-not-evaluate` (exit 3) path. Patch proposal: `w1/MutBattery/patch-counter-af-unix.md`
(shorten the socket name to `/s`, and turn an over-long socket path into an error row so the KILL RULE
yields exit 3).

### 7.2 The preflight's ancestor-sibling clause cannot see a host sibling

`preflight()` runs inside the same `bwrap` sandbox, where only the bound case directory (and its
materialised parent chain) exists. A host scratch holding a sibling is therefore invisible to it:
`$S/p` contained `sibling.txt` and the counter still printed `isolation: isolated` and completed
(`$S/ctl/sibling.counter.json`). The isolation guarantee rests on the allowlist bind, not on that
clause; the receipt wording ("any ancestor of the case directory lists a sibling (so no other scratch,
clone or home content is reachable)") describes something the probe cannot observe. Not a defect in
the sandbox, but the receipt should not be read as evidence of that specific check. No patch proposed:
making the check host-side would void legitimate parallel runs that share a `--scratch` parent.

## 8. Refusals and limits

- No lane file edited, no commit/push/jj or git mutation in the lane or the fleet root; only
  `.ufo/waves/round-89/w1/MutBattery/` was written plus the seat scratch.
- No `sudo`, no host write, no package manager, no tool install.
- No subagent dispatched.
- The predicates, targets, kill rules and instrument digests were not re-scoped; mutants are
  proposals under this wave directory only.
- A surviving mutant is a coverage finding, not a contract change.
- The mutant protocol runs the counter once (`--runs 1`) as tasked; the claim's predicate is three
  runs. None of the three survivors is a sampling artifact: each has a structural cause named in
  section 4 (no roster negative needs more than one case per family; CR-INTERNAL subsumes the CRLF
  draw; no roster gate misreports its process exit code), and section 6 finds no draw-dependent sole
  killer anywhere in the roster.
- Tooling log: nothing installed or upgraded; the host was used read-only (its committed receipt
  `.ufo/waves/round-89/before/host/receipt.txt` was not needed).
