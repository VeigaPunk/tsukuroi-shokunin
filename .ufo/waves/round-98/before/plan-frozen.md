# Round 98 — declaration (frozen before any candidate is scored; controls committed with it)

Lane: tsukuroi (operability + freshness; host operability and repair). Fleet campaign: hyaku, run 15.
Round: 98 (attempt 1). Pre-round lane tip: `b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a`.

## Inputs read before this freeze

- The round-97 closure (`MANIFEST.json` `rounds[]`: `ok`, admitted) and its non-author spot-check
  `corpus/lessons/round-97-verifier-spotcheck.md`: routed defects R97-D1 (C2 doctored-leg revision
  attribution — cite the receipt's own revision, never `46fae1ba` without a receipt), R97-D2
  (r96-tool diff is `6 2` numstat, not "8 +/-"), R97-D3 (LZ docstring wrong member/direction,
  second instance of the class in two rounds), R97-D4 (C2's three gaps stay on the queue).
- `corpus/lessons/round-97.md` (Mistakes R97-N05-COUPLED, R97-SPEC-KEY, R97-LZ-DOCSTRING-TEXT,
  R97-CHAR-VS-BYTE, R97-DOCTOR-NOT-UNIQUE; Frontier; scoreboard) and its amendment sidecar
  `before/plan-amendments-r97.md` (A1-A7).
- `corpus/QUALITY.md` 139-141 (139: a published numeric bound is certified at its boundary on both
  legs; 140: a target clause is re-read against one development run before the freeze; 141: a
  located quote's offset unit is measured at the byte level).
- `corpus/README.md` § "Round 97" and its Frontier bullets (r97 addition): A6 docstring owed to
  r98, A7 field/echo coverage of the new members, M08 selftest case, C2's 150 unbound rows and
  three measured gaps.
- `SCORECARD.md` axes: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8.
  Lowest non-retired axes: **depth 8** and **adjacency 8** (tied). C1 works depth.
- `considerthese/2026-10-26.md` (the newest batch; the connector evaluates its open proposals).
- MANIFEST tsukuroi closures r95-r97 are all `ok`; no fresh-start window is open for this round.

No adjacency move is declarable this round: the one open adjacency item (kaidoku/revenger
reverse-engineering ownership) is operator-owned and unruled; reported, not absorbed.

## Claims (2; frozen sentences; the same sentence in `claims.json`)

### C1 — depth 8 (tied lowest) — closing the r97 A7 limit: the Z/LZ families assert the echo and the era label

**Predicate.** `tools/limine-pin-battery-r98.py --gate G --runs 3` is the r97 battery with two
one-line changes, both inside the families the r97 Frontier leaves as limits:

- `REFUSAL-VERSIONS-9DIGIT-Z` and `LEADING-ZERO-NORMALIZE` set `check_echo` and `check_era`
  (the battery's `meta_ok` then asserts `limine_version` equals the flag spelling verbatim with
  source `flag`, and `visibility_era` equals the label the whole tuple selects). A gate that
  answers every pin correctly but lies in either field reads `unmet` on the r98 battery and
  read `met 105/105` on the r97 battery, whose two families never checked either field (r97
  wave seats ReviewBattery attack-1-field/attack-2, amendments A7).
- The `LEADING-ZERO-NORMALIZE` docstring's text-comparer sentence is corrected (R97-D3/A6):
  the discriminating member is `12.000000009.000000005`, not `000000012.9.4`, and the
  direction is that the text comparer orders it era A while `int()` reads 12.9.5 (era B).
  The roster is unchanged at 105; the succession is sharpening, not new families.

**Target.** Landed gate: `105/105` met in each of three runs, `failed_families []`, 0 error rows, in
the canonical lane and in a `git clone --shared`. N07 (era label swapped exactly when the spelling
has a 9-digit third component or a leading-zero component; pins correct): `103/105` unmet in each
of three runs in both layouts, `failed_families` exactly
`["LEADING-ZERO-NORMALIZE", "REFUSAL-VERSIONS-9DIGIT-Z"]`, 0 error rows. N08 (echo reported as the
numeric tuple): `104/105` unmet in each of three runs in both layouts, `failed_families` exactly
`["LEADING-ZERO-NORMALIZE"]`, 0 error rows. The r97 do-nothing battery
(`before/controls/do-nothing-battery-r97.py`, sha256 `e678c34f…`, byte-identical to the r97 landed
bytes) on the landed gate and on both bends: `met 105/105` in each of three runs, 0 error rows
(blindness receipt for the new assertion).

**Kill rule.** Unmet if any landed-gate run reads below 105/105 or carries a non-null `error` row;
unmet if any bend run is not `unmet`, if its `failed_families` is not exactly the frozen list, or
if its non-null error-row count is not 0; unmet if any do-nothing leg differs from its frozen
reading above; void if any instrument byte differs from
`.ufo/waves/round-98/before/instruments.sha256` at scoring time.

**Counting command.**
`python3 tools/limine-pin-battery-r98.py --gate <GATE> --runs 3 --work <scratch> --json <out>`;
then `python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family
REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE`.

**Do-nothing and near-miss controls (committed with this freeze).**
`before/controls/do-nothing-battery-r97.py` (the r97 landed battery, `e678c34f…`),
`before/controls/do-nothing-gate.py` (the unchanged gate, `7d79ac29…`),
`before/controls/bends/N07-era-field-lie.py` and `N08-echo-norm.py` (emitted by
`tools/make-r98-bends.py`, each exactly one clause: N07 is a single-line label-expression
substitution in the main return; N08 is a single inserted echo-normalization line). Development
receipts: `before/dev/c1-battery-gate.txt`, `before/dev/c1-bend-N07-*.txt`,
`before/dev/c1-bend-N08-*.txt`, `before/dev/c1-dn-*.txt`.

### C2 — freshness 9 — the variant-span checker's non-contiguous branch gains a selftest

**Predicate.** `python3 tools/check-registry-content-r98.py --revision R` is the r97 checker with
the `RC-BEND-SPAN` capture extended to the comma form (`VARIANTS N01,N03`) and a `--selftest`
that covers the non-contiguous branch of `derive_variant_span` (the r97 MutRegistry M08 class:
a `VARIANTS` set whose labels are not a contiguous run). The capture now binds a pinned-values
cell stating either `N01-N03` or `N01,N03`; the derivation returns the comma form exactly when the
labels are non-contiguous. Two new selftest cases — `span-gap` (an `N01,N03` fixture whose row
states `N01,N03` reads no findings) and `span-gap-lie` (the same tools against a row stating
`N01-N03` reads exactly one `RC-VALUE-MISMATCH`) — pin the branch.

**Target.** After: landed `status PASS`, `findings []`, `bindings 7`; `--selftest`
`PASS 14/14`. The M08 one-fault mutant of the r98 checker (`derive_variant_span` checks only the
first label) FAILS `--selftest` (`12/14`, both gap cases red), where on the r97 checker it read
`PASS 12/12`. Two doctored revisions on the pinned pre-round base `b3be3f90` (checker rides at
`fixture/`, so the coverage gate's tool set is unchanged): D1 doctors only the make-r96-bends row
(`VARIANTS N01-N04` -> `VARIANTS N01,N03`) and reads `status FAIL` with exactly one
`RC-VALUE-MISMATCH` (`RC-BEND-SPAN`) on the r98 checker and `RC-CELL-MISSING` on the r97
do-nothing checker; D2 doctors the make-r96-bends VARIANTS keys to `N01,N03` and the row to
`VARIANTS N01,N03`, reading `status PASS` on the r98 checker and `status FAIL` with exactly one
`RC-VALUE-MISMATCH` on the M08 mutant (its lie twin — same keys, row `VARIANTS N01-N03` — inverts
both: r98 `FAIL`, M08 `PASS`). The coverage gate on each doctored revision reads `PASS 157/157
findings 0`. Before: the r97 checker has no comma capture and no gap case, and M08 survives it.

**Kill rule.** Unmet if the landed run is not PASS with 0 findings, or if any binding's value is
not re-derived from the tool; unmet if `--selftest` is not `PASS 14/14`; unmet if the M08 mutant
reads PASS on `--selftest`, or fails to discriminate on D2 (r98 PASS / M08 FAIL and the lie twin
r98 FAIL / M08 PASS); unmet if D1 does not read FAIL with exactly one `RC-VALUE-MISMATCH` on the
r98 checker, or if the coverage gate does NOT read PASS 157/157 on a doctored revision (that
would make the blindness leg vacuous); void if `tools/check-registry-content-r98.py` differs from
`.ufo/waves/round-98/before/instruments.sha256` at scoring time.

**Counting command.** `python3 tools/check-registry-content-r98.py --revision <R> --json <out>`
and `python3 tools/check-registry-content-r98.py --selftest`; the doctored legs are reproduced by
`sh .ufo/waves/round-98/before/fixtures/build-doctored-fixture-r98.sh`.

**Do-nothing control (committed with this freeze).**
`before/controls/do-nothing-checker-r97.py` (`2daf5926…`, the r97 landed checker) and the
pre-round baseline receipt `before/registry-baseline.json` (coverage `PASS 157/157 findings 0`
at `b3be3f90`; content `PASS 7/7` on both checkers at the landed revision).

## Limits (named, not claimed)

- C1 sharpens two existing families; it adds no new family and no new version spelling. The
  echo/era assertion on the X/Y/Z/Y-digit families remains as it was (X and Y families do not set
  `check_echo`/`check_era`); only the r97 families gain the fields.
- `N07`'s label lie is targeted at the Z/LZ spellings by construction (9-digit third component or
  leading-zero component); a field lie on any other spelling is not this bend's clause.
- The `RC-BEND-SPAN` capture binds cells stating `N<digits>-N<digits>` or `N<digits>,N<digits>...`
  in the same `VARIANTS` cell; a prose restatement of the span in another cell stays unbound.
- C2 binds the same 4 rows / 7 cells as r97. The 150 unbound rows and the three r97 measured gaps
  (uncovered-cell doctoring, tool+cell co-doctoring, printed-tally parsing) stand unchanged.
- The battery's `meta_ok` asserts the echo verbatim: the gate echoes the flag spelling as sent, so
  `12.09.4` must echo `12.09.4`. A gate that canonicalizes the spelling fails N08's family, by
  the claim's design, not by a Limine rule.

## Amendment slot

Empty on purpose: the declaration bytes are pinned in `before/instruments.sha256`, so a pre-report
narrowing is an append-only sidecar (`before/plan-amendments-r98.md`) the falsification ledger's
`narrowing` pointers name, never an in-place edit of this file.

## Axis and separability

C1 (depth 8) changes the battery's metadata assertions on two families; C2 (freshness 9) changes
the registry drift checker's span capture and selftest. They share no instrument: C1's legs read
battery JSON, C2's legs read the registry table and the make-r96-bends bytes. Each is verifiable
with the other's work absent (the battery needs no checker change; the checker needs no new
family). No axis is harmed: the gate bytes are unchanged (`7d79ac29…`), the r97 battery still
reads `105/105` on the landed gate, the coverage gate still certifies `157/157` at the pre-round
tip, and no corpus entry is removed.
