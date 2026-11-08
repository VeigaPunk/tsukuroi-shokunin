# Limine r95 — the 1-9-digit component bound, certified at both ends

source: S389 (Python 3 documentation, `stdtypes` — "Integer string conversion length limitation"), new row, opened 2026-11-08, pinned copy sha256 `6bf2ce2b…` (`w1/ScoutSources/receipts/pin-table.tsv`); S382 (Limine v12.9.5 `common/lib/config.c`), S384 (Limine v12.9.5 `host/limine.c`), S386 (Limine v12.9.6 `common/lib/config.c`), S387 (Limine v12.9.6 ChangeLog), S388 (Limine v12.9.6 `host/limine.c`), re-opened from the pinned copies (HTTP 200, sha256s in the same pin table)
verified-at: 2026-11-08 (freeze `2abddda5`, landed tip `884ed06b`; the receipt that carries each number is named beside it)
recheck: re-open S386-S388 on any `limine` package update (cadence on-release); re-open S389 on any CPython docs update (the 4300-digit default it records is CPython policy, not a constant); re-run `python3 tools/limine-pin-battery-r95.py --gate tools/check-limine-pins.py --runs 3` after any change to `parse_limine_version`

Round 95. One rule, two legs. The lane's version gate publishes a numeric bound — a component of a `--limine-version` may carry one to nine digits — and a published bound is certified at its boundary, never only above it. Round 94 held the refused leg; round 95 adds the accepted leg, so the bound is now certified at both ends.

## The two legs the lane now holds

The gate refuses a `--limine-version` outside `X.Y.Z` with rc 64 and empty stdout (`tools/check-limine-pins.py:190-192`). Its published component bound is the clause at `tools/check-limine-pins.py:99`:

```
    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
```

| leg | family | what it sends | expected |
|---|---|---|---|
| refused | `REFUSAL-VERSIONS-10DIGIT` | `1234567890.0.0`, `0.1234567890.0`, `0.0.1234567890`, `1234567890.1234567890.1234567890` (`tools/limine-pin-battery-r95.py:1648`) | rc 64, empty stdout, no verdict |
| accepted | `REFUSAL-VERSIONS-9DIGIT` | `999999999.9.9` — a boundary member: the first component at the cap, 999,999,999 (`tools/limine-pin-battery-r95.py:1694`) | rc 1, verdict `DEGRADED`, the LP-MISMATCH pin with consequence `panic` |

The refused leg is r94's, unchanged. The accepted leg is r95's, and it is the one that was missing.

## The gate clauses, quoted by file and line

- The bound: `tools/check-limine-pins.py:99`, `len(p) <= 9`, inside `parse_limine_version` (`tools/check-limine-pins.py:91-101`). Its docstring states the published contract — "`X.Y.Z`, ASCII digits only (1-9 digits per component; leading zeros are accepted and normalized by int(), e.g. `12.09.4` == `12.9.4`)" and "A component longer than 9 digits is refused rather than handed to int(), which raises above 4300 digits (round-92 ReviewGate F1)" (`tools/check-limine-pins.py:92-95`).
- The era split: `tools/check-limine-pins.py:104`, `VISIBILITY_ERA_SPLIT = (12, 9, 5)   # first upstream release with the create_menu_tree() cut`, applied at `tools/check-limine-pins.py:193`, `era_b = version >= VISIBILITY_ERA_SPLIT`.
- The refusal is total, not a default (`tools/check-limine-pins.py:190-192`), and the boundary member parses, so the era it selects is era B: `(999999999, 9, 9) >= (12, 9, 5)`.

## Why the accepted leg was missing

Round 94's battery declared the boundary member and never sent it; the constant stood alone:

```
tools/limine-pin-battery-r94.py:1684
REFUSAL_DIGIT9 = "9" * 9 + ".9.9"  # X.Y.Z-shaped, first component 999,999,999: the cap's boundary member, ACCEPTED
```

`grep -c REFUSAL_DIGIT9` reads **1** in `tools/limine-pin-battery-r94.py` — the declaration and nothing else, referenced nowhere (`w1/ScribeKnowledge/receipts/02-refusal-digit9-grep.txt`). Round 94's verifier spot-check named the defect — "`REFUSAL_DIGIT9` (battery 1684) is declared and referenced nowhere" (`corpus/lessons/round-94-verifier-spotcheck.md:242`) — and routed it as defect 8 of that round's queue (`corpus/lessons/round-94-verifier-spotcheck.md:241-244`). In the r95 battery the same grep reads **3**: the docstring's mention (`tools/limine-pin-battery-r95.py:29`), the declaration (`:1694`), and the one use that makes it live (`:1715`, `_era_first_line_panic(c, REFUSAL_DIGIT9)`) — same receipt. The roster grew by exactly the family that uses it: `FAMILY_ROSTER` holds **99** names in `tools/limine-pin-battery-r95.py` and **98** in `tools/limine-pin-battery-r94.py`, the difference being `REFUSAL-VERSIONS-9DIGIT` alone (AST parse, same receipt).

## The family's fixture shape and expected answer

`fam_refusal_versions_9digit` (`tools/limine-pin-battery-r95.py:1707-1715`) builds on the shared era fixture `_era_first_line_panic` (`tools/limine-pin-battery-r95.py:1567-1579`): the file's **first physical line is an entry label**, the body carries a mismatch pin and, after the body, a `hash_mismatch_panic: no`; a second efi entry carries an OK pin. The version sent is the boundary member itself. The expected answer is era B's: `999999999` is at or above the 12.9.5 split, so the label-end NUL leaves the global section empty and the `hash_mismatch_panic: no` is **invisible** — the mismatch falls to `panic`, not `prompt`. The family therefore certifies two things at once: that the gate **accepts** the in-bound value (rc 1 with a verdict, never rc 64), and that it reads the **era** the value selects. A gate that accepts `999999999.9.9` but answers `prompt` fails it.

The landed gate answers exactly that in all three runs of the canonical and clone layouts (`w1/ExecBattery/c1-canonical.json`, `w1/ExecBattery/c1-clone.json`; sha256s in `w1/ScribeKnowledge/receipts/04-sibling-receipts-reparse.txt`): `met`, **99/99** families, `failed_families []`, 0 error rows, **396** cases. The four family rows read `want` = `[1, 'DEGRADED', [[3, 'LP-MISMATCH', 'panic'], [7, 'OK', 'none']], 'menu']` and `got` = `[1, 'DEGRADED', [[3, 'LP-MISMATCH', 'panic'], [7, 'OK', 'none']], 1, 'menu', '999999999.9.9', 'flag']` — the version and its source `flag` are part of the answer (`tools/limine-pin-battery-r95.py:2002`).

## The bend N05, and what it proves

`N05-strict-8` bends the gate's own bound by one clause — `len(p) <= 9` becomes `len(p) <= 8` (`w1/ExecBend/n05-diff.txt`; one hunk, one minus line, one plus line per `w1/ExecBend/diff-counts.txt`) — so the gate **refuses** the in-bound 9-digit member. Against the r95 battery the bend reads `unmet` **98/99** in each of three runs, with `failed_families` exactly `["REFUSAL-VERSIONS-9DIGIT"]` (`w1/ExecBend/n05-canonical.json`; `w1/ExecBend/count-runs-canonical.txt`, exit code 1 per `w1/ExecBend/count-runs-canonical.rc`). Its four family rows carry the battery's error text — `bad-output: JSONDecodeError rc=64 stderr=… check-limine-pins: --limine-version must be X.Y.Z or auto` (`w1/ExecBend/n05-canonical-analysis.txt`): the bend refuses with rc 64 and emits no JSON, so those four error rows are the bend's refusal receipt, not a crash. No row outside that family errors (`error_rows_outside_digit9=0`, same receipt).

## The do-nothing blindness this closes

The r94 battery cannot see the bend, because the family does not exist in it. Run against `N05-strict-8`, the r94 battery reads `met` **98/98** in each of three runs, 0 error rows, and **0** `REFUSAL-VERSIONS-9DIGIT` rows in its `case_log` (`w1/ExecDoNothing/dn-n05.json`). Run against the landed gate it reads the same `met` 98/98 ×3, 0 error rows, 0 rows of that family (`w1/ExecDoNothing/dn-gate.json`) — the family is absent there, not failing. The over-strict `<= 8` gate was invisible to the r94 roster; the r95 roster reads it as `unmet` with that one family named.

## Limits

- **One in-bound version, and only the first component's.** The family sends exactly one in-bound 9-digit value, `999999999.9.9` (`tools/limine-pin-battery-r95.py:1694`); the other in-bound 9-digit shapes are not sent, so the accepted leg certifies that the membership boundary is *at* 999,999,999 in the **first** component — not that the gate accepts every in-bound spelling. The cap admits all three components at nine digits (`999999999.999999999.999999999` reads rc 1, `DEGRADED`, era `12.9.5+`, `w1/ReviewBattery/boundary-probe.txt`), and a bend of the **second** component's bound to `<= 8` still reads `met` 99/99 on the same roster (`w1/ReviewBattery/middle-bound-probe.txt`). The per-component accepted boundary is Frontier work.
- **The 1-9-digit cap is the gate's own contract.** It is the lane's published bound (`tools/check-limine-pins.py:92-99`), not an upstream one; upstream's own limit is far looser — CPython's default integer-string conversion limit is 4300 digits, and exceeding it raises `ValueError` (S389). The family certifies where this gate's boundary is, not that nine digits is the right design.
- **The extra-component `12.9.6.1` shape stays open at battery level.** It is the *probe* shape that is unexercised: `AUTO-PROBE-SHAPES` sends a no-parsable answer and the suffixed `Limine 12.9.6-rc1` on stdout, never the extra-component `Limine 12.9.6.1` (`tools/limine-pin-battery-r95.py:1718`, `:1938`), so a probe guard that admits `12.9.6.1` while still blocking `-rc1` is not distinguished by any family — the gap r94 recorded (`.ufo/waves/round-94/w1/ReviewBattery.md:36`, `corpus/lessons/round-94-verifier-spotcheck.md:245-247`). The *refusal* side of the four-component shape is exercised: the scored roster sends `12.9.5.1` (`tools/limine-pin-battery-r95.py:1643`).
- **The ten-digit enumeration does not start at the smallest out-of-bound value.** It sends `1234567890` and its digit-permutations (`tools/limine-pin-battery-r95.py:1648`), not `1000000000` (1,000,000,000), the smallest ten-digit number; the gap was measured in round 94 (`.ufo/waves/round-94/w1/ScribeLesson/receipts/02-boundary-measurements.txt`) and the accepted leg does not change it.

## Gate

| row | URL opened | tier | located quote (≤25 words) |
|---|---|---|---|
| S389 | `https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation` | A | "The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits." |
| S386 | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/common/lib/config.c` | A | "if (p > config_addr) { *(p - 1) = '\0'; }" (pinned copy raw 328-330) |
| S387 | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/ChangeLog` | A | "A config whose first line is an entry has had no global options since 12.9.5." |
| S388 | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/host/limine.c` | A | `puts("Limine " LIMINE_VERSION);` (pinned copy raw 2035) |

Re-opened from the pinned copies: S382 (v12.9.5 `common/lib/config.c`, sha256 `a940acae…`, byte-identical to S386) and S384 (v12.9.5 `host/limine.c`, sha256 `4da21c7c…`, byte-identical to S388). Both pairs are recorded in `w1/ScoutSources/receipts/pin-table.tsv`; the byte-identity is the fact the r94 entry recorded, re-measured from this round's pins.
