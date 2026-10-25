# Scratch census mirror design — tsukuroi design item 11/12

## What this is

An isolated, runnable check for the lane's **scratch census mirror gate**
(validate-before-append for `corpus/SOURCES.md`), implemented as
[`scratch-census-mirror.py`](scratch-census-mirror.py).

Contract (derived from the round-36 verifier closure and the fleet-wide
`scripts/sources-census.sh` contract):

1. Before the first real registry append, the candidate rows must be
   validated **in an isolated scratch mirror**: a copy of the lane tree (or
   at least every used-by root), plus the append block.
2. `scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`
   must exit 0 (warnings allowed).
3. The gate must **fail on the unchanged baseline**: an empty append block is
   a hard refusal, and the before-row count is bound to the lane HEAD base
   (`--expect-rows-before`, default 199 = the row count at lane HEAD
   `0e5f70f`), so a drifted or unchanged registry can never pass silently.

## How the check fails on the unchanged baseline

Observed on the unchanged lane (HEAD `0e5f70f`, `corpus/SOURCES.md` 199 rows,
no diff to the worktree):

| Arm | Result | Why |
|---|---|---|
| Empty append block (`rows.empty`) | **REFUSE, exit 1** | no delta ⇒ no after state; a vacuous green would be indistinguishable from "no change". Message: `no appended rows: unchanged baseline has no after state; the mirror gate refuses a vacuous pass`. |
| Row-count binding drift (fixture 1 row vs bound 199) | **REFUSE, exit 1** | `registry holds 1 rows, not the frozen base literal 199` — drift is loud, not silent. |
| Baseline census itself | exit 0, 199 rows, **31 W04** duplicate-url advisories, 0 E findings | the lane is "clean with warnings", which is exactly why the gate must not rely on the *source* state: it validates the candidate. |

So the design's guarantee is that the gate cannot pass on unchanged bytes —
it always demands a real, disjoint, well-formed after-state.

## What after state it measures

The receipt (`validate_exit` line at the end) binds bytes, not just exit
codes:

- `rows_before` / `rows_appended` / `rows_after` (199 → 200 in the good arm),
- `ids_appended` (must be disjoint from the registry),
- `rows_sha256` (append block), `source_registry_sha256` (lane bytes,
  re-checked after the build), `mirror_registry_sha256` (after-state bytes),
- `w04_before` / `w04_after` (duplicate-url advisory counts; a candidate that
  reuses an already-warned URL across a scope scope raises the after count
  31 → 32 while the census still exits 0 — proof the gate measures the
  candidate, not just the source),
- `e_findings` (E-finding count in the mirror validation),
- the validate program's own stdout (W04 lines, `ok` line) and exit code.

## Empirical findings from this seat

1. **A corpus-only mirror fails with E11.** `sources-census.sh --file`
   resolves `used-by` against the parent of the file's parent (the mirror
   root) (`scripts/sources-census.sh:500-501`, `:567`). The lane's registry
   references `tools/` and `SKILL.md` (326 corpus / 17 SKILL.md / 8 tools
   references). A corpus-only mirror reported 25 E11 findings (S146,
   S148-S169, S191-S193) and `validate_exit=1`. The mirror must therefore
   copy every used-by top-level root (corpus/, tools/, SKILL.md). This is the
   single most important correctness constraint for the design in this lane.
2. **Static refusals happen before any mirror is created** (bad tier, bad
   NF, duplicate id, empty block, drift): `ls -d dest` shows nothing, so a
   refused gate leaves no artifact behind.
3. **Source integrity is double-checked**: the source registry digest is
   re-measured after the mirror build; any change mid-build refuses.
4. **Advisory drift is measurable even at exit 0**: the W04 before/after
   delta is part of the receipt, so a candidate that grows the duplicate-url
   class is visible even though the census treats W04 as non-fatal.

## Sandbox / repo rules honored

- Lane corpus opened read-only; only the mirror receives the appended rows;
  the source digest is re-checked after the build.
- `--dest` hard-bounds to `/var/tmp`, `/tmp`, the seat directory, or the
  lane root's parent; the default is a fresh `mktemp` directory.
- Fixture Git: every run does `git init -q -b main <dest>` and verifies
  `git rev-parse --show-toplevel` equals the fixture root **before** any
  commit (`--commit` only after a clean validation). No git/jj writes ever
  occur in the lane, fleet, or sibling repos.
- No tool installations were needed (host `git` 2.56.0, `bash`, `gawk`,
  `python3`; `RULES.md` read first, lines 1-14). No pacman/host changes.

## Files in this seat

- `scratch-census-mirror.py` — the runnable gate (~460 lines).
- `rows.*` — candidate append-block inputs (empty / good / bad tier / W04
  probe / fixture).
- `receipt-*.txt` — captured receipts for arms A-F (see table above).
- This `README.md`.
