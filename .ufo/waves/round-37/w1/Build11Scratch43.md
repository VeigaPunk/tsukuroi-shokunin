# Build11Scratch43 — design item 11/12: scratch census mirror design

**Axes:** operability · build:scratch census mirror design. **Milestone:**
Independent runnable design.

**Verdict:** delivered a runnable, isolated scratch-census-mirror gate at
`.ufo/waves/round-37/w1/Build11Scratch43/scratch-census-mirror.py` (with
`README.md`, input rows, and captured receipts `receipt-*.txt`). The gate
**fails on the unchanged baseline** (empty append block → REFUSE exit 1;
row-count binding drift → REFUSE exit 1) and **measures the after state** by
byte-bound receipt: `rows_before/rows_appended/rows_after`, `ids_appended`,
`source_registry_sha256` vs `mirror_registry_sha256`, `w04_before/after`,
`e_findings`, and the validate exit.

## Evidence opened this round (access date 2026-10-25)

- `scripts/sources-census.sh` — `:2-38` (modes/exit codes: `exit: 0 clean or warnings · 1 E/overdue findings`); `:495-504` (`--file` resolves `dir_abs=$(realpath -- "$(dirname -- "$file_abs")/..")`, i.e. the mirror root); `:538-571` (E11: `used-by` checked as `[ ! -e "$dir/$path" ]`); `:600-654` (W04/E04 duplicate-url rules).
- `corpus/SOURCES.md` (lane HEAD `0e5f70f`, 199 rows) — header row at `:5`, tail rows S194-S199 at `:200-208`.
- `.ufo/waves/round-36/w2/W2RevCounter/W2RevCounter.md` and `corpus/lessons/round-36-verifier-spotcheck.md:79` — closure re-ran `scripts/sources-census.sh validate --root … tsukuroi` → "exit 0, 199 rows, 31 W04 duplicate-url advisories".
- `souji-shokunin/.ufo/waves/round-26/w1/ExecScratchMirror.md` — fleet precedent for the mirror gate mechanics (used-by resolution, receipt binding, refusal table).
- `.ufo/waves/round-37/w1-spec.json` / `w1-plan.json` — seat assignment and contract.

## How the check fails on the unchanged baseline (observed)

Baseline census (read-only, on the unchanged lane) is *clean with warnings*:
`validate` exit 0, 199 rows, 31 W04 duplicates, 0 E findings. That clean-ness
is the vacuity trap the gate is built to close:

| arm | exit | observed |
|---|---|---|
| `rows.empty` (no append) | 1 | `REFUSED: no appended rows: unchanged baseline has no after state; the mirror gate refuses a vacuous pass` |
| fixture corpus with 1 row vs bound 199 | 1 | `REFUSED: registry holds 1 rows, not the frozen base literal 199` |
| malformed candidate (tier `D`) | 1 | `REFUSED: S200: tier='D' not in {A,B,C}` — before any mirror is created |

Receipts: `receipt-empty-baseline.txt`, `receipt-drift-binding.txt`,
`receipt-malformed-tier.txt`.

## What after state it measures (observed)

- Good arm (`rows.good`, real lane corpus read-only): 199→200 rows,
  `ids_appended=S200`, `source_registry_sha256=76da7e58…`,
  `mirror_registry_sha256=2b25c6fc…`, `w04_before=31 w04_after=31`,
  `e_findings=0`, `validate_exit=0` (`receipt-gate-good.txt`).
- W04-drift arm (`rows.w04`, candidate reuses an already-warned URL across a
  fresh scope): `w04_before=31 w04_after=32`, `e_findings=0`, exit 0 —
  the receipt measures advisory growth even when the census exits 0
  (`receipt-w04-drift.txt`).
- Fixture+commit arm: builds a synthetic corpus, validates (exit 0) and
  commits the after-state inside the mktemp fixture repo only, top-level
  verified before the commit (`receipt-fixture-commit.txt`).

## Findings

1. **A corpus-only mirror fails with E11.** `--file` mode resolves `used-by`
   against the mirror root, and this lane's registry references `tools/`
   and `SKILL.md` (326 corpus / 17 SKILL.md / 8 tools references). The first
   corpus-only build reported 25 E11 findings (S146, S148–S169, S191–S193)
   and `validate_exit=1`. The mirror must copy every used-by top-level root;
   this is the key correctness constraint for the design.
2. Static refusals leave no destination behind (fail-before-write).
3. Source registry digest is re-checked after the build; any change
   mid-build refuses.
4. The receipt binds bytes (hashes), so the L1 can tie the validated mirror
   to the bytes that later land.

## Gates / touched surfaces / limits

- No lane tracked file changed (`git diff --quiet HEAD` → 0). Only the seat
  directory was written. Fleet/sibling repos untouched. No pacman, no host
  changes, no delegation, no tool installs (`RULES.md` read first, lines
  1–14; host `git` 2.56.0, `bash`, `gawk`, `python3` already present).
- Sandbox: `--dest` hard-bounds to `/var/tmp`, `/tmp`, the seat dir, or the
  lane root's parent; fresh `mktemp` default; `git init` + top-level
  verification before any commit; `--commit` only after clean validation.
- The candidate rows are synthetic (`*.invalid` URLs) and are **not**
  proposed registry additions; the gate is the deliverable.
