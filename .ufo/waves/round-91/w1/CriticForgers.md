# CriticForgers — docstring-only forgers (round-91, w1)

Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` = `b516d6ae13ec0bba3ef89589ac1cac86f73a9632`.
Method: read ONLY battery docstring lines 1-145 of `tools/limine-pin-battery-r91.py`; never opened gate code. Wrote `base.py` from rules R1-R10/V1/U1/R8 alone. Battery: `python3 tools/limine-pin-battery-r91.py --gate <file> --runs 3 --work "$S/w"` (cwd scratch).
Axes: operability (gate accuracy vs frozen rules) + freshness (docstring vs pinned Limine sources).

## Base gate
`base.py` — **met 82/82 at `--runs 3`** (three consecutive `families_passed 82/82 verdict met`). Docstring alone is sufficient to implement the gate; no ambiguity hit.

## Forgers (27; each bends exactly one clause; all distinct from N01-N10 in `INDEX.tsv`)
Sweep at `--runs 1` in parallel (xargs -P4), then survivors re-confirmed at `--runs 3`. Receipts in `CriticForgers/receipts/` (gate .py + battery output .txt).

### Killed (23) — battery catches the bend
| id | bend | result |
|---|---|---|
| F02_v1_entry_any_slash | entry = any '/' anywhere in line (not first non-blank) | unmet 50/82 |
| F03_v1_entry_col0_only | entry only at column 0 (ignore leading blanks) | unmet 78/82 |
| F07_u1_all_path_lines | unverified = any path/image_path line, not efi image lines | unmet 77/82 |
| F08_u1_no_imagepath_fallback | unverified/r9 ignores image_path fallback | unmet 79/82 |
| F09_u1_zero_based | unverified line numbers 0-based | unmet 72/82 |
| F10_u1_hash_only | unverified = missing '#' only (ignores missing URI shape) | unmet 81/82 |
| F11_r6_missing_never_panic | LP-MISSING never panics on efi image line | unmet 64/82 |
| F12_r6_skip_mismatch_only | skip only for LP-MISMATCH (not FORMAT/BAD-RESOURCE) | unmet 80/82 |
| F13_r6_sb_absent_panic | SB absent -> panic (inverts SB logic) | unmet 69/82 |
| F14_r9_second_path | image line = 2nd path key line | unmet 56/82 |
| F15_r9_protocol_case_insens | protocol value case-insensitive (EFI accepted) | unmet 81/82 |
| F16_r9_last_protocol | protocol = last matching key, not first | unmet 81/82 |
| F17_r9_imagepath_first | prefers image_path over path | unmet 56/82 |
| F18_r10_measured_case_insens | measured_boot value case-insensitive | unmet 81/82 |
| F19_r10_absent_menu | tpm absent -> menu (not halt-if-tpm) | unmet 81/82 |
| F20_r10_tpm0_halt | tpm 0 -> halt (not menu) | unmet 80/82 |
| F21_r6_panic_case_sensitive | hash_mismatch_panic compared case-sensitively | unmet 78/82 |
| F22_r8_hmp_anywhere | R8 hash_mismatch_panic reported from anywhere | unmet 81/82 |
| F23_r2_hash_first_hash | hash = after FIRST '#', not last | unmet 81/82 |
| F24_r3_hash_64 | hash length 64 vs 128 | unmet 3/82 |
| F25_r4_resource_case_insens | resource strcmp made case-insensitive | unmet 80/82 |
| F26_r4_boot_root_unresolved | boot() empty root made unresolvable | unmet 5/82 |
| F27_u1_global_first_only | unverified = only first image line across all entries | unmet 75/82 |

### SURVIVORS (4) — battery lacks a family (docstring is NOT ambiguous)
All survived at `--runs 3` (82/82 met). Each is a real behavioral bend the docstring states explicitly, so the gap is a missing family, not ambiguity.

1. **F01_v1_blank_first_wholefile** — treats blank-line(s)-before-first-entry as whole-file-visible. Docstring V1 (lines 113-115) says explicitly: "A config whose first line is blank (spaces/tabs) before the first '/'-line keeps the cut … the global section is those blank lines only." Battery has no family distinguishing this (BLANK-CLASS covers key-line blank rules, not V1 visibility).
2. **F04_v1_last_panic_wins** — takes LAST visible hash_mismatch_panic instead of FIRST (drops `break`). R6/R8/V1 all say FIRST. No family has two visible hash_mismatch_panic lines with different values where first-vs-last matters.
3. **F05_v1_exception_measured_only** — first-line-is-entry exception applied to measured_boot only, not hash_mismatch_panic. V1 states exception covers both keys ("hash_mismatch_panic (R6) and measured_boot (R10) are read only from the global section" with whole-file exception). No FIRST-LINE-ENTRY case mixes the two keys.
4. **F06_v1_include_entry_line** — global section INCLUDES the first entry line itself. V1: "every physical line before the first entry line". A hash_mismatch_panic/measured_boot key line ON the entry line is not a key line (starts with '/'), so only observable if key line parsing ever overlaps — in practice killed only if a family puts a visible key line exactly on the entry line boundary. Battery lacks that boundary family.

### N01-N10 distinctness check
N01/N02 = whole-file for one key (mine: F04 last-wins, F05 split-exception, F06 boundary — different); N03/N04 = no/inverted first-line exception (mine: F01 blank variant, none equals N03/N04); N05-N09 unverified-field variants (mine: F07 scope-all-path-lines, F08 fallback, F09 0-based, F10 hash-only, F27 global-first — none equals a lane near-miss); N10 = first-anywhere (mine: F22 R8-only variant, killed by PANIC-AFTER-PIN).

## Proposed docstring wording (for survivor families, if added)
No wording change needed — add families instead: (a) blank-first-line V1 visibility with measured_boot=no in an entry body; (b) two visible hash_mismatch_panic lines (no then yes) asserting FIRST wins; (c) first-line-is-entry with only hash_mismatch_panic=no present asserting whole-file for both keys; (d) key line on entry line boundary.

## Pinned-source cross-check
`before/src/limine-v12.9.4-common_lib_config.c` raw 642-650 and `limine-v12.9.4-common_lib_uri.c` raw 46-63 match docstring V1/U1 verbatim; no docstring-vs-source conflict found.

## Refused / not done
No lane files edited; no mutating git; gates run only in scratch.
