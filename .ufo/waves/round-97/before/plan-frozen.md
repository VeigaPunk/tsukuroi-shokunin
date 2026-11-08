# Round 97 — declaration (frozen before any candidate is scored; controls committed with it)

Lane: tsukuroi (operability + freshness; host operability and repair). Fleet campaign: hyaku, run 15.
Round: 97 (attempt 1). Pre-round lane tip: `f48d16428d8bb92fd6cf546a745bff5b624e3f18`.

## Inputs read before this freeze

- The round-96 closure (`MANIFEST.json` `rounds[]`: `ok`) and its non-author spot-check
  `corpus/lessons/round-96-verifier-spotcheck.md`: routed defects (1) the r96 untracked receipt
  `.ufo/waves/round-96/after/registry-final.json`, (2) the Y-family docstring's false era sentence,
  (3) the same correction carried. Its standing verdict: expansion/quality/discernment `unchanged`.
- `corpus/lessons/round-96.md` (Mistakes R96-FRONTIER-NOT-SENT, R96-N04-TWO-FAMILIES,
  R96-N02-ERRORROWS, R96-EXTRA-TWIN, R96-Y-DOCSTRING-ERA, R96-C2-REMEDY-CHECKLIST, R96-FREEZE-DRIFT,
  R96-REPORT-WORD-COUNT) and its Frontier (r96 addition).
- `corpus/QUALITY.md` 136-140 (139: a published numeric bound is certified at its boundary on both
  legs; 140: a target clause is re-read against one development run before the freeze).
- `corpus/README.md` § "Round 96" and its Frontier bullets (r96 addition).
- `SCORECARD.md` axes: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8.
  Lowest non-retired axes: **depth 8** and **adjacency 8** (tied). C1 works depth.
- `considerthese/2026-10-26.md` (the newest batch; the connector evaluates its open proposals).
- MANIFEST tsukuroi closures r94-r96 are all `ok`; no fresh-start window is open for this round.

No adjacency move is declarable this round: the one open adjacency item (kaidoku/revenger
reverse-engineering ownership) is operator-owned and unruled; reported, not absorbed.

## Claims (2; frozen sentences; the same sentence in `claims.json`)

### C1 — depth 8 (tied lowest) — the third component's cap and the accepted leading-zero form

**Predicate.** `tools/limine-pin-battery-r97.py --gate G --runs 3` carries, on fixtures generated
fresh per run, two families beyond the r96 roster (103):

- `REFUSAL-VERSIONS-9DIGIT-Z` — a boundary member of the gate's published 1-9-digit component cap
  whose cap sits in the THIRD component: `12.9.999999999` (whole tuple `>= 12.9.5`, era B) and
  `0.9.999999999` (era A). Each must be ACCEPTED — rc 1 for the fixture's mismatch pin, never rc 64 —
  and answered from the era the whole tuple selects (`panic` for era B, `prompt` for era A).
- `LEADING-ZERO-NORMALIZE` — a component written with leading zeros, in-bound and normalized by
  `int()`: `12.09.4` and `000000012.9.4` (era A), `12.000000009.000000005` (era B) and
  `000000000.000000000.000000000` (era A), each accepted with its era's own answer.

The landed gate reads `105/105` met in every run. Against two one-clause bends the same battery
reports exactly: `N05-z-cap-8` (the Z bound bent to `<= 8`) fails
`["LEADING-ZERO-NORMALIZE", "REFUSAL-VERSIONS-9DIGIT-Z"]` — the Z member and the two leading-zero
members whose third component is 9 digits are refused — and `N06-leading-zero-reject` (a component
whose first digit is `0` refused) fails `["LEADING-ZERO-NORMALIZE"]`.

**Target.** Landed gate: `105/105` met in each of three runs, `failed_families []`, 0 error rows, in
the canonical lane and in a `git clone --shared`. N05: `103/105` unmet in each of three runs in both
layouts, `failed_families` exactly `["LEADING-ZERO-NORMALIZE", "REFUSAL-VERSIONS-9DIGIT-Z"]`, with
exactly 6 non-null `error` rows per run — 4 in `REFUSAL-VERSIONS-9DIGIT-Z` and 2 in
`LEADING-ZERO-NORMALIZE` — each being the bend's own rc-64 refusal (`bad-output: JSONDecodeError
rc=64`), which is the refusal the bend exists to make, not a transport failure. N06: `104/105`
unmet in each of three runs in both layouts, `failed_families` exactly `["LEADING-ZERO-NORMALIZE"]`,
with exactly 4 non-null `error` rows per run, each the same rc-64 refusal class. The r96 do-nothing
battery (`.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py`, sha256 `f06d90ae…`,
byte-identical to the r96 landed bytes) on the landed gate and on both bends: `met 103/103` in each
of three runs, 0 error rows (blindness receipt for both new families).

**Kill rule.** Unmet if any landed-gate run reads below 105/105 or carries a non-null `error` row;
unmet if any bend run is not `unmet`, if its `failed_families` is not exactly the frozen list, or if
its non-null error-row count or class differs from the frozen one; unmet if any do-nothing leg
differs from its frozen reading above; void if any instrument byte differs from
`.ufo/waves/round-97/before/instruments.sha256` at scoring time.

**Counting command.**
`python3 tools/limine-pin-battery-r97.py --gate <GATE> --runs 3 --work <scratch> --json <out>`; then
`python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family REFUSAL-VERSIONS-9DIGIT-Z
--family LEADING-ZERO-NORMALIZE`.

**Do-nothing and near-miss controls (committed with this freeze).**
`.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py` (sha256 `f06d90ae…`, the r96 landed
battery), `.ufo/waves/round-97/before/controls/do-nothing-gate.py` (`7d79ac29…`, the unchanged gate),
`.ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py` and `N06-leading-zero-reject.py` (emitted
by `tools/make-r97-bends.py`, each exactly one clause and asserted one match). Development receipts:
`before/dev/c1-battery-gate.txt` (105/105 met), `before/dev/c1-bend-N05-z-cap-8.txt` (103/105,
two families, 6 refusal rows), `before/dev/c1-bend-N06-leading-zero-reject.txt` (104/105, one family,
4 refusal rows).

### C2 — freshness 9 — a registry row's declared values re-derived from the tool's bytes

**Predicate.** `python3 tools/check-registry-content.py --revision R` re-derives seven frozen cell
values of the operative `SKILL.md` registry from the bytes of the tool each row names, and reports
`status PASS` with `findings []` at the landed revision: `limine-pins`' argparse default (`auto`),
its `--selftest` tally (39, re-derived by running it), its JSON schema token
(`tsukuroi-limine-pins-v3`), `limine-pin-battery-r96`'s roster size in two cells (103, by AST count),
`check-r96-calibration`'s selftest tally (7, re-derived by running it) and `make-r96-bends`' variant
span (`N01-N04`). Against a scratch `git clone --shared` whose `SKILL.md` carries six content-only
cell doctors — `default 12.9.4`, `(88 fixtures`, `roster 99 (`, `FAMILY_ROSTER, 99,`,
`--selftest` (29 cases`, `r96 VARIANTS N01-N05` — with the row set, the tool set and every path
unchanged, it reports `status FAIL` with six `RC-VALUE-MISMATCH` findings naming those rows and the
derived values, while the unchanged `tools/check-registry-coverage.py --revision <same>` reads
`PASS` with `registered 154`, `findings 0` on that same revision. The checker's `--selftest` reads
`PASS 12/12`, and each one-cell doctor fires exactly its own finding id.

**Target.** After: content `status PASS`, `findings []`, `bindings 7`; doctored revision
`status FAIL` with exactly six `RC-VALUE-MISMATCH` findings (one per doctor, each naming its row);
coverage gate on the doctored revision `PASS 154/154 findings 0`; selftest `PASS 12/12`. Before: no
such checker exists, and the coverage gate certifies the same doctored table. No work: the doctored
table is reached by nobody (the coverage gate is measured green on it).

**Kill rule.** Unmet if the landed run is not PASS with 0 findings, or if any binding's value is not
re-derived from the tool (a constant answer would pass the landed leg and fail the doctored leg —
both are required); unmet if the doctored revision reads PASS on any doctored cell, or if the
coverage gate does NOT read PASS 154/154 on it (that would make the blindness leg vacuous); unmet if
any selftest case is not id-exact or the tally is not 12/12; void if
`tools/check-registry-content.py` differs from `.ufo/waves/round-97/before/instruments.sha256` at
scoring time.

**Counting command.** `python3 tools/check-registry-content.py --revision <R> --json <out>` and
`python3 tools/check-registry-content.py --selftest`; the doctored leg is reproduced by
`sh .ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh` (recipe committed as
`before/fixtures/doctored-recipe.txt` and the byte diff as `before/fixtures/doctored.diff`).

**Do-nothing control (committed with this freeze).**
`.ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py` (`6fcb2d0a…`, the unchanged
coverage gate) plus the pre-round baseline receipt `before/registry-baseline.json`
(`PASS 154/154 findings 0` at `f48d1642`).

## Limits (named, not claimed)

- The two new families sample four spellings per class, not every 9-digit Z form or every leading-zero
  form; the four-member `LEADING-ZERO-NORMALIZE` cycle covers one member per case ordinal.
- `N05` also fails two cases of `LEADING-ZERO-NORMALIZE` (its all-zero and `12.000000009.…` members
  carry a 9-digit third component). The claim states the exact set; the Z bend is not claimed to be
  single-family, and `N06` is the family's own discriminator.
- C2 binds 4 of the operative table's 154 rows (7 cells). Every other row stays presence-only
  (the coverage gate's scope); a row added after this freeze is not bound.
- C2's `selftest` derivations run the bound tools' own `--selftest` and read its printed tally; a tool
  that printed a tally without running cases would satisfy that binding (the reviewer's control (d)).
- The registry-content checker reads the highest `## Gate and probe registry — round<N> superseding
  current rows` section, like the coverage gate; append-only continuation rows outside it are not
  bound.

## Amendment slot

Empty on purpose: the declaration bytes are pinned in `before/instruments.sha256`, so a pre-report
narrowing is an append-only sidecar (`before/plan-amendments-r97.md`) the falsification ledger's
`narrowing` pointers name, never an in-place edit of this file.

## Axis and separability

C1 (depth 8) changes the battery's family roster and its bends; C2 (freshness 9) changes the lane's
drift detection over `SKILL.md`'s registry cells. They share no instrument and no counting command:
C1's legs read battery JSON, C2's legs read the registry table and tool bytes. Each is verifiable
with the other's work absent (the battery needs no registry row; the checker needs no new family).
No axis is harmed: the gate bytes are unchanged (`7d79ac29…`), the r96 battery still reads `103/103`
on the landed gate, the coverage gate still certifies `154/154` before the settle's own rows, and no
corpus entry is removed.
