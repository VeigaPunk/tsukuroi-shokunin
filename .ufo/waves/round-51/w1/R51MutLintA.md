VERDICT: defect-found

Seat R51MutLintA · item C1-L3 · lint = `tools/lint-grounding-r51.py` at 2732ee6c06108c031c4d8043239b994e0504eb2f (blob sha256 35df03c5…f83a5, equal to the FROZEN-hashes.txt line `35df03c5…f83a5  tools/lint-grounding-r51.py`).

## Method (what was run)

- Copied the frozen lint to `/fast/scratch/hyaku/tsukuroi-r51/R51MutLintA/mut/orig.py` (bytes from `git -C …/tsukuroi-shokunin show <REV>:tools/lint-grounding-r51.py`).
- Made four single-site mutants, each asserted to match exactly one site in orig (diffs in `w1/R51MutLintA/M1..M4.diff`).
- Each mutant and the original were run as `python3 <mut> --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision <REV> [--entry-file F]` against:
  - `real`: the entry at REV (no entry file);
  - `K2`, `K3`, `K3b`: built by the exact `battery.py` c1 replacements (`rep(raw, '"* potentially suffixed …"', '"potentially suffixed …"')`, `rep(raw, 'scrub.c:3094-3153', 'scrub.c:3094-3153 and :3200')`, `rep(raw, '"if (btrfs_fs_closing(fs_info))"', '"btrfs_fs_closing(fs_info)"')`) plus the `battery.marks()` gate-status suffix;
  - two supplementary fixtures beyond the battery: `KE` (declared-but-uncited gap `1198` added to the S247 line of the Range-gaps block) and `KU` (prose cite `btrfs-scrub@.service:999`, unresolvable).
- Raw matrix: `w1/R51MutLintA/results.json`; fixtures: `w1/R51MutLintA/fixture-K*.md`.
- Scratch removed after receipts were copied.

Command output, lint_ok (rows clean; gate-leg in parentheses where it matters):

| mutant | real | K2 | K3 | K3b | KE (supp.) | KU (supp.) |
|---|---|---|---|---|---|---|
| orig | 3 | 2 | 0 | 2 | 0 | 2 (cite_bad 1) |
| M1 substring quote | 3 | **3** | 0 | **3** | 0 | 2 |
| M2 gap_extra ignored | 3 | 2 | 0 | 2 | **3** | 2 |
| M3 `cite_bad` not incremented | 3 | 2 | 0 | 2 | 0 | 2 (**cite_bad 0**) |
| M4 range end exclusive | **0** (gap_missing 703, 1235, 1268; 3075; 1512; 10) | 0 | 0 | 0 | 0 | 0 |

Original on the battery fixtures: K2 FAIL (2), K3 FAIL (0), K3b FAIL (2) — as declared.

## Per-mutant verdicts

- **M1 (quote equality → substring): KILLED.** K2 and K3b score lint_ok 3 under M1 (orig: 2). Line: `lint-grounding-r51.py:233` (`if norm(want) != norm(src[n - 1]):`). Real entry unchanged (3). Killed by the battery's own K2 and K3b fixtures. (Only the quote leg flips; K2/K3b still shows quote_bad 0 under M1 — the substring test accepts the fragment and the leader-less quote alike.)

- **M2 (gap leg ignores gap_extra): SURVIVES the battery's fixtures — CONTROL GAP.** `lint-grounding-r51.py:329` (`gap_ok = int(not gap_missing and not gap_extra and not snap_problems)`). Under M2 K2, K3, K3b stay at their orig values (K3 still gap_missing → 0). Only the supplementary `KE` (declared line with no citation) flips: M2 → lint_ok 3, orig → 0. The battery has no fixture whose defect is a declared-but-uncited gap line, so the `gap_extra` leg is unexercised by the freeze battery. Real entry unchanged (3).

- **M3 (`cite_bad` never incremented): SURVIVES as a verdict mutant — equivalent for lint_ok; CONTROL GAP for the printed counter.** `lint-grounding-r51.py:244` (`ncb += 1`). The problem string is still appended (`:245`), so `rows_clean`/`lint_ok` are unchanged on every fixture (KU: lint_ok 2 under both). Only the printed `cite_bad` changes (KU: 1 → 0). Nothing in the tree reads `cite_bad`: `git -C …/tsukuroi-shokunin grep -n cite_bad <REV> -- tools .ufo/waves/round-51/controls` lists only lint-internal occurrences (`lint-grounding-r51.py:214,248,335`). The battery has no unresolved-prose-cite fixture and does not assert the counter. Killing this one requires a fixture plus an assertion on `cite_bad`, or dropping the field.

- **M4 (range end exclusive): NOT a silent survivor on the real entry — it FAILS the real entry (lint_ok 0).** `lint-grounding-r51.py:146` (`return any(a <= n <= b …)`). Under M4 the real entry gets gap_missing `S247 dev-replace.c: 703, 1235, 1268`, `S240 ioctl.c: 3075`, `S237 scrub.c: 1512`, `S244 btrfs-scrub@.service: 10` — so M4 is not equivalent and is killed by the real-entry control (K-pass). But strictly by the item's criterion it SURVIVES the three K fixtures: M4 never turns a K fixture into PASS (K2 changes 2→0, K3b 2→0, K3 stays 0). A narrower-reading control gap: the K-battery alone does not detect it; the real-entry PASS control does.

## Control gaps for the L1 (proposed additions; not run in this seat, not applied)

Proposed amendment to `controls/battery.py` (c1 block), each expected FAIL with the named lint field — to be verified by the L1 before freeze/w2 use:

1. K9 (kills M2): `entry.replace('- S247 dev-replace.c: 1197', '- S247 dev-replace.c: 1197, 1198', 1)` on the freeze entry with all-holds cohort; expected verdict FAIL, lint `gap_extra == ['S247 dev-replace.c: 1198']`.
2. K10 (kills M3, counter leg): prose insert `(btrfs-scrub@.service:999)` into the GR3 "Host reading" paragraph; expected FAIL, lint `cite_bad == 1`, `lint_ok == 2`. Requires the battery to assert the counter, not only the verdict.
3. M4: already caught by the K-pass real-entry control if the C1 run of `check-scrub-admission-r51` reads lint on the real entry; no new fixture needed, but the K-battery alone does not catch it — state that in the battery's docstring.

## Limits / not done

- Only the lint was mutated; the C1 counter and battery were NOT run (outside EXEC-AUTHORIZED for this item). The K-fixture construction replicates `battery.py` string replacements and the `marks()` suffix; section hashes (`section_hashes`) were not computed since lint does not read them.
- Mutant equivalence was checked only on the real entry and the listed fixtures; no exhaustive input search.
- No tool installed; no pacman, no writes outside scratch and this seat's receipts.
