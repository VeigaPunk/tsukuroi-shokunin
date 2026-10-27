VERDICT: supports

# C1-M2 — Mutation test of the seat-report binding channel (wave-fabrication probes)

Item: mutate the smallest behavior-bearing points of a counted C1 seat report in a scratch
clone and observe the frozen counter. Detector (frozen, digest-verified):
`tools/check-scrub-admission-r47.py` sha256
`e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b`.
Predicate: `structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`.

## Method

- Fixture: `git clone -q --shared <lane> $D` under `/fast/scratch/hyaku/tsukuroi-r47/C1MutReports/fx.dpr6x416`,
  origin removed, `git rev-parse --show-toplevel` == $D asserted; all commits with
  `-c user.name=fixture -c user.email=fixture@invalid`. Lane HEAD at clone time: `f6bc6d05`.
- The real `w1-dispatch.json` was removed in the fixture and a fabricated wave `w9` was
  committed: `w9-dispatch.json` + `w9-results.json` dispatching exactly the 18 frozen C1 seats
  with correct roles, plus 18 valid reports `w9/<seat>.md`
  (first line `ROW GR<n> VERDICT: holds`, second `SECTION SHA256: <F1 extent hash>`, body
  ≥300 bytes citing only pinned snapshot lines). Both dispatch files present would make every
  seat "dispatched 2 times", so exactly one wave channel exists in the fixture.
- Background legs: HEAD still carries the round-46 gate-status line and no round-47 SKILL /
  README marks (the L1 writes those only at integrator admission), so the pristine fixture
  commit also appends the three round-47 marks verbatim per the frozen constants. This leaves
  the entry row extents and section hashes untouched (marks appended at EOF, after
  `## How this changes OS triage`); the probe channel under test is not affected.
- F1 section hashes at the fixture entry (identical to the lane entry at HEAD, verified via
  `--section-hash`, receipt `baseline-section-hash.json`):
  GR1 `fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8`,
  GR2 `909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2`,
  GR3 `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c`.
  Note: the lane *worktree* entry currently differs from HEAD (L1 mid-edit); the counter reads
  revision bytes, so all runs used HEAD bytes — worktree state is irrelevant to these results.
- Pristine baseline: counter rc 0, `verdict PASS`, structural_ok=1, quotes_ok=3, verdicts_ok=3,
  marks_ok=3, 6/row bound on current, distinct bodies, Res2 seats ignored
  ("dispatched 0 times"). Receipt: `baseline.json`.
- Each mutant is one commit on top of the baseline altering only
  `.ufo/waves/round-47/w9/R47RevGR1a.md` (the GR1 reviewer-a seat); the frozen counter and
  `--section-hash` were run per mutant revision. Receipts: `C1MutReports/M*.json`.

## Matrix

bind = `bind()` returned a verdict; counted = hash equals the counter-computed current extent
hash so the seat feeds `bound_on_current` / row_ok. "overall" is the counter's final verdict.

| # | mutant | mechanism | bind? | counted? | bound GR1 | row_ok GR1 | overall | detector detail (reason string) |
|---|--------|-----------|-------|----------|-----------|------------|---------|---------------------------------|
| M1 | preamble first | verdict moved to line 2 behind a `# …` preamble | refused | no | 5 | True | PASS | `first line '# w9 fabricated seat report — preamble probe'` |
| M2 | trailing space | `ROW GR1 VERDICT: holds ` (ASCII space) | refused | no | 5 | True | PASS | `first line 'ROW GR1 VERDICT: holds '` |
| M3 | NBSP homoglyph | `ROW GR1 VERDICT:\u00a0holds` (U+00A0) | refused | no | 5 | True | PASS | `first line 'ROW GR1 VERDICT:\xa0holds'` |
| M4 | wrong extent, +next header | hash over lines[`## GR1`..`## GR2`] inclusive (`bfa09a9e…`) | binds | **no** | 5 | True | PASS | (bind detail `w9/R47RevGR1a.md`; hash ≠ current) |
| M5 | wrong extent, −trailing blank | hash over extent minus the blank line before `## GR2` (`1ecf6f44…`) | binds | **no** | 5 | True | PASS | (same; hash ≠ current) |
| M6 | valid hash, wrong row | GR2's correct section hash in a GR1 report | binds | **no** | 5 | True | PASS | (same; hash ≠ current) |
| M7 | cross-row verdict in body | line `ROW GR2 VERDICT: holds` inside the GR1 report | refused | no | 5 | True | PASS | `contradicting line ROW GR2 VERDICT: holds` |
| M8 | duplicate own verdict | body line `ROW GR1 VERDICT: holds` (row and word identical to line 1) | **binds** | **yes** | 6 | True | PASS | (binds and counts — see coverage note) |
| M9 | uppercase hex | `SECTION SHA256: FE77AC…` | refused | no | 5 | True | PASS | `second line 'SECTION SHA256: FE77AC…'` |
| M10 | CRLF endings | whole report `\r\n` | refused | no | 5 | True | PASS | `first line 'ROW GR1 VERDICT: holds\r'` |
| M11 | short body | valid first two lines, body 1 byte | refused | no | 5 | True | PASS | `report body under 300 bytes` |
| M12 | trailing space on hash line | `SECTION SHA256: fe77…ca8 ` | refused | no | 5 | True | PASS | `second line 'SECTION SHA256: fe77…ca8 '` |

Assigned classes: (a)=M1 refused; (b)=M2 and M3 refused; (c)=M4/M5 refused *counting* — the
seat's verdict is parsed but the hash leg pins admission to the counter-computed F1 extent, so
a hash over any wrong extent (include next header, drop trailing blank, or a different row's
valid hash) never feeds `bound_on_current`; (d)=M7 refused by the contradiction scan.

## Findings

1. All four assigned forgery classes are discriminated. No mutant bound wrongly: every refused
   seat shows `verdict: null` with an explicit reason; every wrong-extent hash seat binds but
   is excluded from admission counting, leaving `row_ok=True` only because the remaining five
   valid seats carry the row (bound drops 6→5).
2. Coverage note (not a defect): the contradiction scan (`ANY_VERDICT_RE` over lines[1:])
   only kills on a *different row or a different word* (counter source, `bind()`), so a seat
   may repeat its own `ROW GR1 VERDICT: holds` inside its body (M8) and still bind and count.
   This cannot forge or alter a verdict — it is tolerance of redundant self-consistent text.
3. Hash-line strictness is byte-exact: uppercase hex (M9), trailing space (M12), and CRLF
   (M10, which also breaks line 1 via `\r`) all fail closed via `fullmatch`.
4. `--section-hash` output was stable across all 12 mutants (identical
   `section_sha256`/`structural_ok=1`; only the embedded revision field differs), confirming
   no mutant touched the entry.

## Restoration evidence

- Probe file `.ufo/waves/round-47/w9/R47RevGR1a.md` sha256 **before**:
  `2a48af481b2551da1e6d740be9199dd438c46a15acf051ed43e4970059103f2b`; **after** the 12-commit
  mutant chain, `git checkout <baseline> -- <file>` restored byte-identical content
  (sha256 re-verified equal, observed `restored == pristine bytes: True`).
- Baseline commit `c74e4fbbe0d064c8d0645a49cf3d09aa68608a9c` object intact; counter rerun on it
  after the chain: rc 0 and output byte-identical to `baseline.json`.
- Full mutant→commit map: receipt `mutant-commits.tsv`.

## Not done / bounds

- Only the GR1 seat `R47RevGR1a` was mutated (one seat suffices: all rows share the same
  `bind()` path); GR2/GR3 reports were left valid to keep `row_ok` comparison meaningful.
- No host mutation, no lane writes outside this seat's report/receipts, no packages installed
  (none needed), no subagents spawned.

Report bytes: this file. Receipts: `.ufo/waves/round-47/w1/C1MutReports/`.
