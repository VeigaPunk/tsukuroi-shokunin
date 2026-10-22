# ExecRegistryCoverage — draft registry rows for the round-28 battery tools

Draft rows for `tools/check-registry-coverage.py` (QUALITY 70: a tool lands with its row in the
operative `## Gate and probe registry — round<N> superseding current rows` table of the same round).

Each row below is a single Markdown table line with the eight cells of the round-27 header
(`Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner`),
copied from `SKILL.md:2444-2480` at `f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0`.

## D1 — the two new battery rows (verbatim text)

```
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 could-not-evaluate | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and with an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 could-not-evaluate | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
```

## D2 — the round-28 table preamble (verbatim text)

The two rows above go at the end of a new `## Gate and probe registry — round28 superseding current rows`
section, after all 31 round-27 rows carried over verbatim. The checker selects the unique
highest-numbered heading of that exact form, so the round-28 table must be complete; a table
carrying only the two new rows would report the other 31 tools as missing.

```
## Gate and probe registry — round28 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every
round27 row is retained verbatim; round28 adds the two should-fail batteries that measure
claims C1 and C2 (QUALITY 70: a tool lands with its row). A self-test flag is resolved against
the committed tool source at the bound revision, not against this prose. Selftest capability is
distinct from a real measurement.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
```

followed by the 31 round-27 rows of `SKILL.md:2446-2476` byte-for-byte, then the two rows of D1.

## D3 — format constraints the checker enforces (measured, not inferred)

1. Eight cells exactly. A cell containing an unescaped `|` splits the row and the checker exits 2
   with `E-REGISTRY-TABLE` / `malformed registry row at line N` — the `\|` escape in the entry
   command of both rows above is load-bearing.
2. `Kind` must be `gate`, `probe` or `library`. Both rows above are `probe`.
3. A `probe` verdict map must contain a `0` and a `2`; a `gate` verdict map must contain `0`, `1`
   and `2`. Both rows above carry all three, so they pass either kind.
4. One row, one tool. A row naming two or more `tools/` paths raises `REGISTRY-ROW-AMBIGUOUS`.
   Neither row names a second `tools/` path, so both stay one-tool rows.
5. A row naming a `tools/` path that is not a committed regular file at the bound revision raises
   `REGISTRY-ROW-ORPHAN`. The `kernel-taint-battery` row therefore requires
   `tools/mutants-kernel-taint.py` to be committed before the row lands.
6. A self-test flag written in the Self-test cell is resolved against the committed tool source at
   the bound revision. Both batteries have no `--selftest` flag, so both rows say `none:` and name
   no flag; a `--selftest` written into either row would raise `REGISTRY-SELFTEST-UNRESOLVED`.

## D4 — verification of D1 and D2 in a private sandbox

Measured on private `git archive` exports under `/fast/scratch/hyaku/tsuku28/ExecRegistryCoverage/`;
the lane was never written to.

| Sandbox | Base revision | Table content | `check-registry-coverage.py` |
|---|---|---|---|
| `sandbox3` | `f8e3a8f2` | round-28 table, 31 round-27 rows + `adjacency-battery` | exit 0, PASS, 32 of 32 tools, 0 findings |
| `sandbox6` | `79d4264` | round-28 table, 31 round-27 rows + both rows of D1 | exit 0, PASS, 33 of 33 tools, 0 findings |
| `sandbox2` | `f8e3a8f2` | round-28 table, 31 round-27 rows + both rows of D1 | exit 1, FAIL, `REGISTRY-ROW-ORPHAN` for `tools/mutants-kernel-taint.py` (the tool is not committed at that revision) |
| `neg1` | `f8e3a8f2` | one row appended below the round-27 table without a new heading | exit 1, FAIL, `REGISTRY-ROW-MISSING` for `tools/mutants-adjacency-overlap.py` (the round-27 table stays operative) |
| `neg2` | `f8e3a8f2` | one row inside the round-27 table with an unescaped `|` in a cell | exit 2, CANNOT_EVALUATE, `E-REGISTRY-TABLE` / `malformed registry row at line 2481` |
