VERDICT: defect-found

# Seat R49ExecGates — item P-6 (predecessor gates must not regress)

All runs were read-only against committed objects of the lane
(`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`), never the mutable working tree.
BASE = `6256760d1382ce4ce20fcba830d4b2912cfbf12b`, FREEZE =
`55c07cd3f8bff2e12117c34d57b4c618de74d85c` (both resolve to commit objects; the freeze is an
ancestor of the current `refs/heads/master` tip `d7cfc27308e8af51b76b5cfe0c656acc1788cefb`,
`merge-base --is-ancestor` rc=0). Raw JSON for every row is under
`.ufo/waves/round-49/w1/R49ExecGates/` (same directory name as this report minus `.md`).

CLI note: the item names several gates without arguments, but every one of them requires an
explicit revision. Bare `check-registry-coverage.py` returns
`{"status":"CANNOT_EVALUATE","findings":[{"id":"E-CLI","site":"cli","detail":"--revision REV or --selftest required"}]}`
(rc=0); the other gates are argparse-mandatory (`--revision`/`--tools-revision`). Every row below
therefore used the required selector at BASE and at FREEZE, exactly one run per endpoint, no
`--selftest` anywhere (so the one-selftest-at-a-time rule was never engaged).

## Status table (observed, one run per endpoint)

| # | Gate | Command form run | BASE 6256760 | FREEZE 55c07cd | Shape |
|---|---|---|---|---|---|
| 1 | `check-adjacency-anchors.py` | `--revision <rev>` | **PASS** (rc=0, findings `[]`) | **FAIL** (rc=1, 1 finding) | **PASS → FAIL** |
| 2 | `check-adjacency-overlap.py` | `--revision <rev>` | PASS (rc=0, `anchored_rows 6 == expected_rows 6`, `sibling_check sibling-verified`) | PASS (rc=0, same counts, `shape_errors []`) | PASS → PASS |
| 3 | `check-registry-coverage.py` | `--revision <rev>` | FAIL (rc=1, `missing 3`, `registered 74/74`, `tools_total 77`) | FAIL (rc=1, `missing 6`, `registered 74/74`, `tools_total 80`) | FAIL → FAIL |
| 4 | `check-recheck-commands.py` | `--revision <rev>` | PASS (rc=0, `clean_count 51/67`, `flagged_count 0`, `resolved_count 16`) | PASS (rc=0, identical counts) | PASS → PASS |
| 5 | `check-knowledge-header.py` | `--revision <rev>` | PASS (rc=0, `complete_count 67/67`, `finding_count 0`) | PASS (rc=0, `complete_count 67/67`, `finding_count 0`) | PASS → PASS |
| 6 | `check-seat-bindings.py` | `--revision <rev>` | FAIL (rc=1, 41 findings) | FAIL (rc=1, 41 findings) | FAIL → FAIL |
| 7 | `check-revision-binding.py` | `--tools-revision <rev>` | rc=0, `consistency_status PASS`, `consolidation_status FAIL` | rc=0, `consistency_status PASS`, `consolidation_status FAIL` | FAIL → FAIL (unchanged) |
| 8 | `check-section-citations.py` | `--revision <rev>` | PASS (rc=0, `correction_count 2`, `findings []`) | PASS (rc=0, `correction_count 2`, `findings []`) | PASS → PASS |
| 9 | `check-self-assessment.py` | `--revision 6256760… --scratch <scratch>/sa` | `mismatches 0`, `checked 27`, `status PASS` | not run (item: ONCE at base) | expected 1, observed 0 |

## The one regression (row 1) — exact mechanism

Observed at FREEZE (receipt `anchors-freeze.json`):

```
{"counts": {"inbound_by_class": {"DRIFTED": 16, "RESOLVES": 96, "UNRESOLVABLE": 1},
            "inbound_by_scope": {"historical": 89, "operative": 24},
            "inbound_classified": 113, "inbound_total": 114, ...},
 "findings": [{"detail": "classification DRIFTED is inconsistent: found_line is not an occurrence of evidence_quote (or empty quote requires line 0)",
               "id": "INBOUND-CLASSIFICATION-WRONG",
               "site": "corpus/knowledge/adjacency-anchors-r19.json:inbound[108]"}],
 "status": "FAIL"}
```

At BASE the same command returns `status PASS`, `findings []`, `inbound_by_class DRIFTED 17`,
`inbound_classified 114` (`anchors-base.json`). Both runs were executed twice with identical
results (once inline, once saved), so this is not a flake.

The entry is `IN-109` (`registry blob at FREEZE, line 2453`: `"id": "IN-109"`), pointer
`tsukuroi-shokunin/tools/tsukuroi-census.sh:915-970`, classification `DRIFTED`,
`found_line: 2642`, evidence quote
`check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED`.

Cause, measured directly in the two blobs:

```
git show 6256760…:tools/tsukuroi-census.sh | grep -n "D14/D15"
 2604:  # D14/D15 driver class counts, …
 2642:  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
git show 55c07cd…:tools/tsukuroi-census.sh | grep -n "D14/D15"
 2622:  # D14/D15 driver class counts, …
 2660:  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
```

The round-49 C3 census edit (`tools/tsukuroi-census.sh`, present in the freeze commit itself:
`git diff --stat 6256760… 55c07cd…` lists `tools/tsukuroi-census.sh | 65 +++-`) inserts 18 lines
above the D14/D15 selftest case, moving the quote from 2642 to 2660, while the anchor registry
still records `found_line: 2642`. `check-adjacency-anchors.py:739-754` recomputes the quote's
occurrence lines at `--revision`; 2642 is no longer an occurrence, so the classification is judged
wrong (`INBOUND-CLASSIFICATION-WRONG`) and the gate exits 1.

## Is the regression still live?

No — but only because of a **post-freeze** repair. `git log --oneline 55c07cd…..d7cfc273 --
corpus/knowledge/adjacency-anchors-r19.json` returns exactly one commit:

```
32a85560 round-49: w1 spec + validated dispatch (73 seats, policy v2); IN-109 repin 2642->2660
```

`git show 32a85560 -- corpus/knowledge/adjacency-anchors-r19.json` shows `- "found_line": 2642` /
`+ "found_line": 2660` (same hunk also extends the `note`). Supplementary (outside the item's two
endpoints, run for the kill-rule decision): `check-adjacency-anchors.py --revision
d7cfc27308e8af51b76b5cfe0c656acc1788cefb` → `status PASS`, `findings []`, `DRIFTED 17`.

So: the frozen bytes under test (`55c07cd…`) do **not** hold the milestone
`predecessor gates PASS->PASS`; the repair landed at `32a85560`, i.e. after the freeze and before
the wave dispatch. Whether the kill rule reads the freeze revision (FAIL) or the current tip (PASS)
is the L1's ruling; both facts are measured above.

## Non-regression observations (reported, not counted as kill-rule failures)

- Row 3 `check-registry-coverage.py`: FAIL at both endpoints. BASE misses
  `tools/check-scrub-admission-r47.py`, `tools/check-scrub-admission-r48.py`,
  `tools/score-selftest-tmpdir-r48.py` (`regcov-base.json`); FREEZE misses those three plus this
  round's new `tools/check-adjacency-table-r49.py`, `tools/check-fd-band-r49.py`,
  `tools/check-scrub-admission-r49.py` (`rc-freeze.json`, `missing 6`, `tools_total 80`). Not a
  PASS→FAIL, but the round adds three unregistered tools, so the gap widens by exactly 3.
- Row 6 `check-seat-bindings.py`: byte-identical shape at both endpoints — 41 findings, class
  histogram `SCOPE-PATH-DENIED 23, SCOPE-TOOL-UNKNOWN 16, SCOPE-EXEC-DENIED 2`, first sites
  `OracleFetchHTTPS:2`, `OracleFetchHTTPS:3`, `OracleFetchBare:4`. No change attributable to
  round-49 bytes.
- Row 7 `check-revision-binding.py`: `consolidation_status FAIL` at both endpoints, yet the process
  exits 0 (`rb-base.json`, `rb-freeze.json`). A caller that keys on rc alone would read this gate
  as green; the FAIL lives only in the JSON field (`all_bound_tools 17`,
  `all_consistent_tools 16`, `all_total 19`).

## Row 9 — self-assessment mismatch count does not match the round's premise

Ran once, exactly as instructed:
`python3 tools/check-self-assessment.py --revision 6256760d1382ce4ce20fcba830d4b2912cfbf12b
--scratch /fast/scratch/hyaku/tsukuroi-r49/R49ExecGates/sa` (rc=0, 67 s), receipt `sa-base.json`:

- `"mismatches": 0`, `"checked": 27`, `"status": "PASS"`, `"declaring_round": 48`,
  `"axes_heading": "## Axes — current self-assessment (round 48 final measured surface)"`.
- Every K01..K27 is `match`. The round expected 1 mismatch at base, "K10"; the shipped counter
  reports K10 as `{"stated": 72, "observed": 72, "status": "match", "reason": "depth row states 72
  lesson files; corpus/lessons holds 72 files"}`.
- Independent confirmation of that number outside the tool:
  `git ls-tree -r --name-only 6256760… corpus/lessons/ | wc -l` → `72` (and `72` at FREEZE too).
  So the absence of a K10 mismatch is not an extraction bug: the depth row and the tree agree at
  base. The round-49 premise "1 mismatch at base (K10)" was **not reproduced**; I did not run the
  counter a second time (item forbids it) and did not run it at FREEZE.

## Proposed text / disposition for the L1

1. Kill-rule line (freeze-accurate):
   `check-adjacency-anchors at FREEZE 55c07cd: FAIL (INBOUND-CLASSIFICATION-WRONG, inbound[108] IN-109) — PASS at BASE 6256760; regression introduced by the C3 census edit in the freeze commit, repaired post-freeze by 32a85560 (IN-109 found_line 2642 -> 2660).`
2. The repair is already the right one; if the round wants the frozen gate table to read
   PASS→PASS, the IN-109 repin must be part of the freeze commit, not a later one. No re-edit of
   the registry is proposed from this seat (read-only seat; the bytes are already correct at tip).
3. Do not cite "1 mismatch at base (K10)" as measured: the counter at base reports 0/27. Either the
   round's expected value or its K-id is wrong; the evidence above pins which.

## Risks / blockers / limits

- Not run: any `--selftest` (not requested; the item's one-selftest cost rule and 5-10 min budget
  apply), `check-self-assessment` at FREEZE or at the tip (item: exactly once, at base), any gate
  with `--ownership-corrections`, `--audit-live-map`, `--baseline-tools`, `--paths`, `--exec-log`,
  `--forbid`, or the object-selector modes — all optional flags the item did not name.
- Host load (~90 seats) was not a factor: every run finished well inside its timeout; the heaviest
  was `check-self-assessment` at 67 s and `check-revision-binding` at 30-43 s. No timeout retries
  were needed.
- No tool was installed or upgraded; no pacman transaction was attempted.
- Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ExecGates/` removed after receipts were copied;
  nothing was written outside this report, its receipts directory, and that scratch path.
