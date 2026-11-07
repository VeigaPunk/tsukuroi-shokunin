# CriticForgers — docstring-only forgers against the r89 `limine-pins` battery

Lane measured: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` at
`git rev-parse master` = `665408cc45a88ed49717e22f4593e8e6152ac665`.
Battery under test: `tools/limine-pin-battery-r89.py`, sha256
`3bae11e939cf6900fd29bb24033e6d134de8bf0ae7069cdec3f12f716e8df7f8` (= the candidate
`81f68d00` bytes; `git show fba764ca…:tools/limine-pin-battery-r89.py` is empty, so the
battery is new in the candidate and is not one of the frozen instruments — the freeze
manifest pins the counter `c666323a…` and the r88 battery only).
No lane file was created or edited except this report and my own
`.ufo/waves/round-89/w1/CriticForgers/` receipts; nothing was committed.

## Method

Read only the module docstring (`ast.get_docstring`); the gate, battery body and roster
were not read. `base.py` is a from-the-docstring reimplementation of R1-R8 plus the gate
output contract; each forger `fx_*.py` is `base.py` with exactly one textual substitution
(unified diffs in `forgers.diff`, clause list in `forgers.manifest.tsv`), each run through
`limine-pin-battery-r89.py --runs 3`.

Base, verbatim (first run, exit code shown by the wrapper):

```
families_passed 50/50 verdict met failed -
families_passed 50/50 verdict met failed -
families_passed 50/50 verdict met failed -
EXIT=0
```

## Results: 38 one-clause forgers, 3 runs each

`killed` = at least one run `unmet`; families in brackets are the failing ones per run.

| # | forger | clause bent (docstring) | run1 | run2 | run3 |
|---|--------|------------------------|------|------|------|
| 1 | f01_cr_kept | R1 removes EVERY CR anywhere in the file | 48 unm [CR-INTERNAL,WHITESPACE-CRLF] | 48 unm [CR-INTERNAL,WHITESPACE-CRLF] | 48 unm [CR-INTERNAL,WHITESPACE-CRLF] |
| 2 | f02_lead_tab_kept | R1 leading spaces/tabs stripped (blanks = space and tab) | 49 unm [WHITESPACE-CRLF] | 49 unm [WHITESPACE-CRLF] | 49 unm [WHITESPACE-CRLF] |
| 3 | f03_trail_tab_kept | R1 value trailing spaces/tabs stripped | 48 unm [PANIC-VALUE-BLANKS,WHITESPACE-CRLF] | 48 unm [same] | 48 unm [same] |
| 4 | **f04_digits_in_key** | **R1 key = letters/underscores then ':'** | **50 met** | **50 met** | **50 met** |
| 5 | f05_equals_sep | R1 key followed directly by ':' (not '=') | 49 unm [KEY-EQUALS] | 49 unm [KEY-EQUALS] | 49 unm [KEY-EQUALS] |
| 6 | f06_comment_hash_stripped | R1 line whose first non-blank char is '#' is not a key line | 48 unm [COMMENT-DECOY,PANIC-RAW-DECOY] | 48 unm [same] | 48 unm [same] |
| 7 | f07_drop_term_font | R2 path-valued key list (…, wallpaper, term_font) | 45 unm [ALL-PIN-KEYS,OPTIONAL-*] | 44 unm [ALL-PIN-KEYS,OPTIONAL-*] | 44 unm [ALL-PIN-KEYS,OPTIONAL-*] |
| 8 | f08_hash_first_hash | R2 hash = text after the LAST '#' | 49 unm [LAST-HASH] | 49 unm [LAST-HASH] | 49 unm [LAST-HASH] |
| 9 | f09_empty_path_not_pin | R2 empty path is still a pin | 49 unm [EMPTY-PATH] | 49 unm [EMPTY-PATH] | 49 unm [EMPTY-PATH] |
| 10 | f10_len_ge_128 | R3 hash exactly 128 characters | 48 unm [HASH-LENGTH,OPTIONAL-HASH-FORMAT] | 49 unm [HASH-LENGTH] | 49 unm [OPTIONAL-HASH-FORMAT] |
| 11 | f11_upper_hex_rejected | R3 [0-9a-fA-F] | 49 unm [HASH-UPPER] | 49 unm [HASH-UPPER] | 49 unm [HASH-UPPER] |
| 12 | f12_resource_case_insensitive | R4 resource compared case-sensitively | 49 unm [RESOURCE-CASE] | 49 unm [RESOURCE-CASE] | 49 unm [RESOURCE-CASE] |
| 13 | f13_all_dollars_dropped | R4 ONE leading '$' dropped | 49 unm [DOUBLE-DOLLAR] | 49 unm [DOUBLE-DOLLAR] | 49 unm [DOUBLE-DOLLAR] |
| 14 | f14_root_ignored | R4 only `boot` with empty root resolves | 47 unm [OPTIONAL-UNRESOLVED,ROOT-ON-BOOT,UNRESOLVED] | 49 unm [ROOT-ON-BOOT] | 47 unm [OPTIONAL-UNRESOLVED,ROOT-ON-BOOT,UNRESOLVED] |
| 15 | f15_dir_mismatch | R5 path naming a directory → LP-MISSING | 49 unm [EMPTY-PATH] | 49 unm [EMPTY-PATH] | 49 unm [EMPTY-PATH] |
| 16 | f16_gzip_decompressed | R5 gzip files are NOT decompressed | 48 unm [DOUBLE-DOLLAR,GZ-RAW] | 48 unm [same] | 48 unm [same] |
| 17 | f17_hash_case_sensitive_cmp | R5 hash compared case-insensitively | 49 unm [HASH-UPPER] | 49 unm [HASH-UPPER] | 49 unm [HASH-UPPER] |
| 18 | f18_optional_key_case_sensitive | R6 optional keys matched case-insensitively | 49 unm [OPTIONAL-KEY-CASE] | 49 unm [OPTIONAL-KEY-CASE] | 49 unm [OPTIONAL-KEY-CASE] |
| 19 | f19_secure_boot_ignored | R6 MISMATCH → panic when --secure-boot-enforced 1 | 49 unm [SECUREBOOT] | 49 unm [SECUREBOOT] | 49 unm [SECUREBOOT] |
| 20 | f20_last_hmp_line | R6/R8 the FIRST `hash_mismatch_panic` key line | 48 unm [PANIC-FIRST,PANIC-METADATA] | 48 unm [same] | 48 unm [same] |
| 21 | f21_no_value_case_insensitive | R6 value equal to `no` case-insensitively | 47 unm [PANIC-KEY-CASE,PANIC-METADATA,PANIC-VALUE-BLANKS] | 46 unm [+PANIC-NO-ONLY] | 46 unm [+PANIC-NO-ONLY] |
| 22 | f22_unresolved_before_degraded | R7 precedence DEGRADED before CANNOT-EVALUATE | 49 unm [MULTI-FAULT] | 49 unm [MULTI-FAULT] | 49 unm [MULTI-FAULT] |
| 23 | f23_unreadable_conf_degraded | R7 unreadable --conf → CANNOT-EVALUATE rc 2 | 48 unm [CONF-UNREADABLE,MALFORMED-INPUT] | 48 unm [same] | 48 unm [same] |
| 24 | f24_no_plus_removal | R8 label without a leading '+' | 49 unm [ENTRY-LABEL-EDGES] | 49 unm [ENTRY-LABEL-EDGES] | 49 unm [ENTRY-LABEL-EDGES] |
| 25 | f25_trailing_plus_dropped | R8 a trailing '+' stays | 49 unm [ENTRY-LABEL-EDGES] | 49 unm [ENTRY-LABEL-EDGES] | 49 unm [ENTRY-LABEL-EDGES] |
| 26 | f26_entry_untrimmed | R8 label trimmed of spaces/tabs at both ends | 49 unm [ENTRY-LABEL-EDGES] | 49 unm [ENTRY-LABEL-EDGES] | 49 unm [ENTRY-LABEL-EDGES] |
| 27 | f27_path_key_case_sensitive | R2 path-valued keys matched case-insensitively | 47 unm [KEY-CASE,OPTIONAL-KEY-CASE,PANIC-KEY-CASE] | 47 unm [same] | 47 unm [same] |
| 28 | f28_optional_hashformat_panic | R6 optional keys -> skip also for LP-HASH-FORMAT | 46 unm [ALL-PIN-KEYS,OPTIONAL-*] | 46 unm [same] | 46 unm [same] |
| 29 | f29_empty_pin_list_cannot | R7 HEALTHY rc 0 also with no pin at all | 49 unm [EMPTY-PIN-LIST] | 49 unm [EMPTY-PIN-LIST] | 49 unm [EMPTY-PIN-LIST] |
| 30 | f30_vtab_ff_leading | R1 a line starting with another char (FF, VT) is not a key line | 49 unm [BLANK-CLASS] | 49 unm [BLANK-CLASS] | 49 unm [BLANK-CLASS] |
| 31 | f31_vtab_ff_trailing | R1 other trailing chars (VT, FF) stay in the value | 49 unm [BLANK-CLASS] | 49 unm [BLANK-CLASS] | 49 unm [BLANK-CLASS] |
| 32 | f32_hash_format_after_resolution | R3 LP-HASH-FORMAT checked before resolution | 49 unm [FORMAT-BEFORE-RESOLVE] | 49 unm [FORMAT-BEFORE-RESOLVE] | 49 unm [FORMAT-BEFORE-RESOLVE] |
| 33 | f33_no_dollar_dropped | R4 ONE leading '$' is dropped | 48 unm [DOUBLE-DOLLAR,GZ-RAW] | 48 unm [same] | 48 unm [same] |
| 34 | f34_entry_column0 | R8 line whose first non-blank char is '/' | 47 unm [ENTRY-LABEL,ENTRY-LABEL-EDGES,HOST-SHAPE] | 47 unm [same] | 47 unm [same] |
| 35 | f35_one_slash_stripped | R8 label without its leading '/' characters | 47 unm [ENTRY-LABEL,ENTRY-LABEL-EDGES,HOST-SHAPE] | 47 unm [same] | 47 unm [same] |
| 36 | f36_hmp_key_case_sensitive | R8 metadata key line (R1: config keys case-insensitive) | 49 unm [PANIC-KEY-CASE] | 49 unm [PANIC-KEY-CASE] | 49 unm [PANIC-KEY-CASE] |
| 37 | f37_dir_conf_healthy | R7 unreadable --conf (a directory) → CANNOT-EVALUATE | 49 unm [CONF-UNREADABLE] | 49 unm [CONF-UNREADABLE] | 49 unm [CONF-UNREADABLE] |
| 38 | f41_value_lead_blank_kept | R1 value with leading spaces/tabs removed | 2 unm [47 families] | 2 unm [47 families] | 2 unm [47 families] |

Machine-readable copy: `results_table.txt`; raw battery stdout per forger:
`receipts/` (`fx_*` and `f*` files, one per gate).

Aggregate: 37/38 killed, **1 survivor**; 21 forgers were killed by exactly one family, 16 by
more than one; all 50 FAMILY_ROSTER families appear as the killing family for at least one
forger (ENTRY-LABEL-EDGES 6, OPTIONAL-KEY-CASE 5, DOUBLE-DOLLAR/PANIC-KEY-CASE/
WHITESPACE-CRLF/OPTIONAL-HASH-FORMAT 4 each).

## Survivor: `f04_digits_in_key` — R1 key charset ("letters/underscores")

Proved 4 independent invocations x 3 runs = 12 runs, every run
`families_passed 50/50 verdict met`, rc 0 (`receipts/f04_digits_in_key.txt`,
`receipts/f04_prob2.txt`…`f04_prob4.txt`).

Is it a docstring defect or a missing family? **Neither is exactly right; it is a docstring
defect, not a battery gap.** The clause is unambiguous but *inert*: the key charset only
decides which lines count as key lines (R1), and a key line matters only through (a)
membership in the R2 path-valued key list and (b) equality with `hash_mismatch_panic` (R6/R8).
No key in either enumeration contains a digit. A line such as `path2: boot:/x#…` is therefore
"not a key line" under the docstring reading and "a key line with key `path2`" under the
forger reading, and both yield no pin and no metadata line — identical (rc, verdict, pins,
hash_mismatch_panic) for every possible input. No battery family can discriminate, so this is
not "the battery lacks a family".

Corroboration: differential probe `diff_probe_f04.py`, 1200 randomized cases (CRLF, tabs,
`\v`/`\f`, digit-bearing and digit-leading keys, comment decoys, gzip ESP files, both
`--secure-boot-enforced` values), comparing full stdout + rc of `base.py` vs
`fx_f04_digits_in_key.py`:

```
 "cases": 1200,
 "differences": 0,
 "samples": []
}
EXIT=0
```

Smallest safe correction (docstring only, candidate `tools/limine-pin-battery-r89.py`,
module docstring line 29, "…it starts with letters/underscores then ':'": append one
sentence, or add the clause to the "Not modelled (limits, not families)" list at line 76:

> The key charset is observable only through the enumerated keys: no path-valued key and no
> `hash_mismatch_panic` key contains a digit, so admitting digits … changes no output; the
> battery does not certify this clause.

Exact insertion text: `patch_f04_docstring.md` in this directory. No lane file was touched;
the L1 decides whether it lands, and if it lands it should also be reflected in C2's
`limine-uri-failure-r89.md` only if that entry repeats the clause (it does not, per its stated
scope).

## R8 contract probes (not clause bends)

Four probes test the docstring's own MAY/allowed language against what the battery enforces;
all met 3/3, rc 0 (receipts `receipts/p0*.txt`, diffs `probes.diff`):

| probe | docstring clause | result |
|---|---|---|
| p01_omit_entry | R8 a pin record MAY carry "entry" | 50/50 met x3 |
| p02_omit_hmp | R8 top-level object MAY carry "hash_mismatch_panic" | 50/50 met x3 |
| p03_reversed_pins | "sorted per-pin (line, status, consequence)" | 50/50 met x3 |
| p04_extra_keys | "Other extra keys are allowed and ignored" | 50/50 met x3 |

Contract-consistent, but it delimits C1: a gate that simply never emits the two optional R8
fields still reads `met`, so R8's `entry`/`hash_mismatch_panic` computations are certified only
for gates that choose to emit them (the r89 ENTRY-LABEL-EDGES / PANIC-METADATA families exercise
them only conditionally). Pin ordering is likewise uncertified (documented). Neither is a defect;
both are scope limits a reader of the "conformance" claim should not over-read.

## Observations on run-to-run discrimination

Case generation is shuffled per run and families are not guaranteed to fire in every run:
f10's OPTIONAL-HASH-FORMAT appeared in run 1 only, f14's UNRESOLVED/OPTIONAL-UNRESOLVED in
runs 1 and 3 only, f21's PANIC-NO-ONLY in runs 2-3 only. Every such forger was still killed by
another family in every run, so the `--runs 3` protocol's verdict is unaffected here; a deviant
gate whose *only* defect sits in a low-probability family is caught with the per-run probability
of that family, not with certainty.

## Refused / not run

- Did not read the gate, the battery body or the roster (seat bounds); no lane edits, no commits,
  no host writes, no `sudo`.
- No counters/roster, no C1 counting command, no host receipt re-derivation — out of seat scope.
- One finding file's line reference (battery source, non-docstring) was not inspected beyond the
  grep hit at line 531, which I did not use as evidence.
