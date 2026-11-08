# CriticForgers — round 92 w1: forgery battery against the era families

Scope: discrimination of the r92 battery, not isolation. Instruments read-only; every mutant is a
copy under `/fast/scratch/hyaku/tsukuroi-r92/CriticForgers/`. Lane root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Frozen at `da99b2f4`; A3 (`689623fd`) landed the
hardened gate (`35c1088b`) and battery (`aef33925`) mid-wave while I measured, so each receipt names
the bytes it ran against.

Instrument hashes I measured:
- pre-A3: gate `af90ae63…`, battery `fde864ea…` (the seat-spec freeze bytes, `sha256sum -c` clean at
  02:09).
- post-A3: gate `35c1088b7bacb31dfe92e087416136271b6ddef9aebf8fb36727696af8d5c87f`, battery
  `aef3392516aabf2942192cd55d637560b6276bc98b8bf8796f33bd464d02614f`; the regenerated
  `.ufo/waves/round-92/before/freeze-manifest.sha256` verifies clean.

## 1. Docstring-only independent implementation (honest floor)

`base.py` is a from-scratch gate written only from the battery docstring's RULE SET (R1-R10, V1, V2,
U1) and GATE OUTPUT CONTRACT — no import of the battery or the gate, no reading of their bodies for
the rules. It parses `--limine-version X.Y.Z`, applies V1 before 12.9.5 and the `create_menu_tree`
cut (no first-line exception) from 12.9.5, refuses non-X.Y.Z with rc 64, and emits
`{verdict, rc, on_panic, pins, hash_mismatch_panic, unverified_image_lines}`.

Receipt: `base-runs1.json` (pre-A3 battery `fde864ea…`), `base2.json` + `usage-base2.out` (post-A3
battery `aef33925…`).

Result: **89/89 `met`, 0 error rows** on both the pre-A3 battery (`fde864ea…`, `base-runs1.json`) and
the post-A3 battery (`aef33925…`, `base2.json`). Every family's expected answer followed from the
docstring without consulting the battery oracle.

One ambiguity found — in V2's version text, not the families. The docstring says
`--limine-version` is "`X.Y.Z`, ASCII digits only" and "an unknown or malformed version is a usage
error (rc 64)" but states **no bound on component length**. A faithful implementation therefore feeds
a 5004-digit component to `int()`, which raises (`ValueError: Exceeds the limit (4300 digits)`), and
the gate exits rc 1 instead of 64. Measured on the post-A3 `--usage-check` (`usage-base2.out`):

| version | want rc | base rc | ok |
|---|---|---|---|
| `12.9`, `abc`, `12.9.6.1`, `` (empty) | 64 | 64 | yes |
| `9…9` (5004 chars) `.0.0` | 64 | **1** | **no** |
| `12.9.4`, `12.9.5`, `13.0.0`, `12.09.4`, `00.00.00`, absent | 0 | 0 | yes |

10/11 rows pass; the one failure is the 5004-digit component. The docstring's "digits only" admits
unbounded digit runs, so the docstring text and the battery oracle disagree on the digit domain: the
oracle demands rc 64 for a run the docstring's wording permits. A3 (`689623fd`, ReviewGate F1)
resolved this in the gate by capping components at 9 digits — a bound the docstring does not carry.
`base-bounded.py` adds that exact 9-digit cap and then reads **89/89 families and 11/11 usage rows**
(`base-bounded.json`, `usage-base-bounded.out`), so the unstated bound is the only divergence.

## 2. One-clause forgers against the era rules

Each forger is `base.py` with exactly one clause bent, run as
`limine-pin-battery-r92.py --gate <forger> --runs 1` (pre-A3 battery `fde864ea…`). The 89-family
roster is unchanged by A3, so the kill set is stable; post-A3 re-runs of the positive gate and of
`f1`/`f3` are in `base2.json` / `*-current.json`.

| forger | clause bent | verdict | passed | failed families | error rows |
|---|---|---|---|---|---|
| `f1-prompt-firstline` | era flag ignored; a first-line entry ⇒ whole file visible (the 12.9.4 rule applied in both eras) | unmet | 87/89 | ERA-FLE-PANIC-B, ERA-FLE-MEASURED-B | 0 |
| `f2-panic-firstline` | era flag ignored; the first-line exception is never applied (always cut) | unmet | 85/89 | ERA-DEFAULT, ERA-FLE-MEASURED-A, ERA-FLE-PANIC-A, FIRST-LINE-ENTRY | 0 |
| `f3-dual-read` | flag ignored; tries to satisfy both eras by re-reading the file | unmet | 87/89 | ERA-FLE-PANIC-B, ERA-FLE-MEASURED-B | 0 |
| `f4-wholefile-panic` | visibility ignored for `hash_mismatch_panic` (scans the whole file) | unmet | 86/89 | ERA-FLE-PANIC-B, GLOBAL-VS-ENTRY, PANIC-AFTER-PIN | 0 |
| `f5-lc-onpanic` | `on_panic` from a hardcoded line-count→value table, no visibility read | unmet | 28/89 | 61 families incl. every `MEASURED-*` and `PANIC-*` | 0 |

All five are **killed**. Landed gate for comparison: `89/89 met`, 0 errors on both batteries.
Post-A3 re-runs confirm the same kill sets for the positive gate and the era forgers:
`base2.json` 89/89 met; `f1-prompt-firstline.py-current.json` and `f3-dual-read.py-current.json`
each 87/89 unmet with exactly `ERA-FLE-MEASURED-B, ERA-FLE-PANIC-B` — the families are unchanged by
A3, so the discrimination is stable across the instrument revision.

Note on `f3`: "ignore the flag but match both eras" is not implementable, and the reason is the
discrimination result — the same 7-line first-line-entry shape has different expected answers under
`12.9.4` and `12.9.6` (see §3), so any flag-ignoring gate must lose one era. `f3` therefore collapses
to `f1` behaviourally; that collapse is itself evidence that the `--limine-version` flag is
load-bearing, not decorative.

## 3. Answer-leakage analysis (QUALITY 128/129)

Probe receipt (`vis-*` probe under the frozen ISOLATION launcher, run once per era family). What the
gate can see from the case directory:

- **cwd** holds exactly two entries: the conf file (random 5-14 char `[a-z0-9_-]` name + `.conf`) and
  the ESP directory (independent random name). No family label, no digest, no expected answer on disk;
  the conf is a sibling of the ESP, not inside it.
- **gate dir** holds only `gate.py`. **env** is cleared to `PATH=/usr/bin HOME=/tmp LC_ALL=C
  TMPDIR=/tmp PWD=<case>`. **sys.path** is the stdlib only (`python3 -I`). **argv** carries
  `--conf`, `--esp`, `--limine-version` — the version flag is the legitimate input.

Observable-vs-answer, 60 draws per family (era families):

| family | lines | first line entry | ESP files | verdict | on_panic | version |
|---|---|---|---|---|---|---|
| ERA-FLE-PANIC-A | 7 | yes | 2 | DEGRADED | menu | 12.9.4 |
| ERA-FLE-PANIC-B | 7 | yes | 2 | DEGRADED | menu | 12.9.6 |
| ERA-FLE-MEASURED-A | 7 | yes | 2 | HEALTHY | halt | 12.9.4 |
| ERA-FLE-MEASURED-B | 7 | yes | 2 | HEALTHY | menu | 12.9.6 |
| ERA-DEFAULT | 7 | yes | 2 | DEGRADED | menu | (flag omitted) |
| ERA-GLOBAL-KEY-A/B | 8 or 9 | no | 2 | DEGRADED | menu | 12.9.5 / 12.9.6 |

Conf size, 80 draws: ERA-FLE-PANIC-A 394-455, PANIC-B 384-444, MEASURED-A 387-441, MEASURED-B
381-448, DEFAULT 389-442 (means 411-419). **Every era family overlaps every other on line count,
file count and byte size.**

Conclusion a forger can draw from the directory alone: nothing that yields the answer.
`PANIC-A` (prompt) and `MEASURED-A` (halt) share `(lines=7, first_entry=True, nfiles=2,
version=12.9.4)` yet expect different pins and `on_panic`; they are separable only by reading the key
name on line 4 — i.e. by applying the rule. Sizes and names vary only fields the answer cannot be
built from, as QUALITY 128 requires. Ordering is invisible: one fresh subprocess per case, so no
cross-case memory and the shuffled family plan cannot leak.

Residual (disclosed, not a defect): each era family is a fixed 7-line shape repeated 4× per run (one
distinct observable signature per family), so the era certificate rests on one shape per family; the
version flag is the sole A/B discriminator. That is the intended input, not a leak, but the depth of
the era certificate is one shape, not a varied draw.

## 4. Routed finding — the round's own N01/N02 near-miss controls are non-compiling

The declaration (`.ufo/plans/round-92.md:65-66`) states the near-miss variants `N01-era-flat-a`
(2 families fail), `N02-era-flat-b` (3 fail), `N03-default-b` (ERA-DEFAULT fails), each `unmet` ×3
both layouts. Measured against the frozen control bytes:

| control | frozen sha256 | compiles? | battery | error rows | declared |
|---|---|---|---|---|---|
| N01-era-flat-a | `579ae90b…` | **NO — IndentationError line 158** | 0/89 unmet | 356/run (1068/3 runs) | 2 families |
| N02-era-flat-b | `f834193f…` | **NO — IndentationError line 158** | 0/89 unmet | 356/run (1068/3 runs) | 3 families |
| N03-default-b | `979df3fd…` | yes | 88/89 unmet (ERA-DEFAULT) | 0 | ERA-DEFAULT ✓ |
| N04-accept-any | `5706dbf2…` | yes | 89/89 met | 0 | survives ✓ (`--usage-check` catches it) |

Cause: `make-c2-gates.py` appends the bent line at column 0 inside the indented `check()` body
(`era_b = version >= VISIBILITY_ERA_SPLIT` is indented 4 spaces; the injected second assignment is
not). I reproduced the frozen bytes exactly from the current gate source, so the frozen artifacts are
the generator's output — this is a generator bug, not a manual edit.

Consequence: N01/N02 read `unmet` **by crash**, not by a computed verdict. Under QUALITY 126 a control
that crashes on every case is not evidence of rejection, so as frozen these two near-misses prove
nothing about the era clause. The wave's own `after/c2-near-misses/*/summary.tsv` already records
`errors 1068` for both, but the declaration still advertises 2/3 family counts.

Corrected reconstructions (indentation fixed; N01 from the pre-A3 gate, N01b/N02b from the current
`35c1088b` gate), run on the same battery:

| corrected bend | gate it was built from | passed | failed families | error rows |
|---|---|---|---|---|
| `n01-fixed` (era_b=False) | pre-A3 `af90ae63` | 87/89 | ERA-FLE-PANIC-B, ERA-FLE-MEASURED-B | 0 |
| `n01b-fixed` (era_b=False) | post-A3 `35c1088b` | 87/89 | ERA-FLE-PANIC-B, ERA-FLE-MEASURED-B | 0 |
| `n02-fixed` (era_b=True) | pre-A3 `af90ae63` | 85/89 | ERA-DEFAULT, ERA-FLE-MEASURED-A, ERA-FLE-PANIC-A, **FIRST-LINE-ENTRY** | 0 |
| `n02b-fixed` (era_b=True) | post-A3 `35c1088b` | 85/89 | ERA-DEFAULT, ERA-FLE-MEASURED-A, ERA-FLE-PANIC-A, **FIRST-LINE-ENTRY** | 0 |

So: the declared N01 count (2) is right once the bend runs, but the declared N02 count (3) is **wrong**
— forcing the new era also breaks the r91 `FIRST-LINE-ENTRY` family, so the true count is 4 in both
gate revisions. The regression is identical pre- and post-A3, so it is the generator's indentation,
not A3's gate edit, that differs from the declaration.

Receipt provenance (QUALITY 38): the canonical near-miss receipts are **stale**.
`after/c2-near-misses/canonical/summary.tsv` records pre-A3 gate hashes (`8ee18b3…`, `03662dec…`,
`350e2963…`, `aa0bd858…`), which do not match the frozen post-A3 control bytes
(`579ae90b…`, `f834193f…`, `979df3fd…`, `5706dbf2…`). The clone leg
(`after/c2-near-misses/clone/summary.tsv`) does bind the frozen hashes — and still records
`0,0,0` / 1068 errors for N01 and N02, so the crash is in the frozen bytes, not only in the stale
canonical run. The canonical leg must be re-measured to bind the bytes the manifest pins.

### Concurrent repair (A4) and what it leaves open

While I measured, another actor landed the fix I recommend: `make-c2-gates.py` now does a one-line
right-hand-side replacement (`era_b = False` / `era_b = True`) instead of appending a second line, and
`c2gates/N01-era-flat-a.py` (`32a151da…`) and `N02-era-flat-b.py` (`ffc99478…`) were regenerated
(working tree, uncommitted at my measurement). Both now compile. Measured on the repaired bytes with
the current battery (`A4-N01-era-flat-a.json`, `A4-N02-era-flat-b.json`):

| repaired control | passed | failed families | error rows | declared |
|---|---|---|---|---|
| N01-era-flat-a | 87/89 | ERA-FLE-PANIC-B, ERA-FLE-MEASURED-B | 0 | 2 ✓ |
| N02-era-flat-b | 85/89 | ERA-DEFAULT, ERA-FLE-MEASURED-A, ERA-FLE-PANIC-A, **FIRST-LINE-ENTRY** | 0 | 3 ✗ |

So A4 closes the compile defect and N01 now matches its declared count. **N02 still contradicts the
declaration**: the repaired bend fails 4 families, not 3, because forcing the new era also breaks the
r91 `FIRST-LINE-ENTRY` family. The declaration must be amended to 4 (or state the target as "every V1
family the flag selects") before N02's `unmet` is cited as evidence.

### Smallest safe correction

1. In `make-c2-gates.py`, bend the right-hand side instead of appending a line: replace
   `era_b = version >= VISIBILITY_ERA_SPLIT` with `era_b = False  # N01: one v92 clause bent`
   (and `True` for N02). This keeps indentation and is a true one-clause bend.
2. Add `py_compile.compile(..., doraise=True)` to the generator so a non-compiling control cannot be
   frozen.
3. Re-run the canonical near-miss receipts post-A3 so their `gate_sha256` binds the frozen bytes.
4. Append an amendment correcting the declaration's N02 count from 3 to 4, or state the count as
   "all V1 families the flag selects" rather than a literal.

## 5. Other observations (adjacent, not my seat's claim)

- K4-syspath was repaired mid-wave (Amendment A2) and re-measured in `*-fixed/` dirs binding the
  frozen hash `efb53f76…` (before-clone 82/82 met, after 0/89 unmet, 0 errors). The stale
  `before-clone` receipt (K4 0/82, 984 errors) is superseded by `before-clone-fixed`; the declaration
  should cite the fixed receipts.
- The C1 control receipts for K3/K5/K6/K7 bind their frozen hashes; K4's non-fixed receipts do not
  (superseded by A2). C1's target is met by the fixed receipts.

Scope: executed the battery `--gate <forger> --runs 1` runs and `--usage-check` named here; read-only
git reads only; no lane writes outside `.ufo/waves/round-92/w1/CriticForgers/`. Scratch deleted on
exit.

## Verdict

C2 (depth) is **supported on its families**: an independent docstring-only gate reads 89/89 on both
battery revisions, and every flag-ignoring or visibility-bending forger is killed by the era families
(`ERA-FLE-PANIC-B`, `ERA-FLE-MEASURED-B` for the 12.9.4-for-both form; `ERA-DEFAULT`,
`ERA-FLE-PANIC-A`, `ERA-FLE-MEASURED-A` for the always-cut form), with no leakage in names, sizes,
line counts or ordering. Three defects do not falsify C2 but must be repaired before the round's
receipts are cited: (a) the docstring's V2 "`X.Y.Z`, ASCII digits only" text carries no digit-length
bound, so a faithful implementation crashes on a 5004-digit component (10/11 usage rows; the gate's
9-digit cap is an unstated rule — a docstring/oracle disagreement to record, and `base-bounded.py`
shows the bound is the only divergence); (b) the round's own N01/N02 near-miss controls as frozen
(`579ae90b…`/`f834193f…`) were **non-compiling** (IndentationError, 356 error rows/run; the clone leg
bound the frozen bytes and still showed 1068 errors), so under QUALITY 126 they proved nothing — the
concurrent A4 repair (one-line RHS replacement, `32a151da…`/`ffc99478…`) closes this and N01 now
reads its declared 2 families with 0 errors; (c) the declared N02 count (3) still does not reproduce
— the A4-repaired bend fails 4 families in both gate revisions, also breaking `FIRST-LINE-ENTRY` —
and the canonical near-miss receipts bind pre-A3 bytes.

Receipts: `base-runs1.json`, `base2.json`, `base-bounded.json`, `usage-base2.out`,
`usage-base-bounded.out`, `usage-landed2.out`, `f1..f5*.json`, `n01-fixed.py.json`,
`n02-fixed.py.json`, `n01b-fixed.py.json`, `n02b-fixed.py.json`, `N01..N04-*.json`,
`A4-N01-era-flat-a.json`, `A4-N02-era-flat-b.json`, `vis-probe.txt`, and the generator/source copies,
all under this directory.
