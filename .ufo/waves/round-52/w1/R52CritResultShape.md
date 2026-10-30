VERDICT: supports

# W-B3 — results/dispatch binding shapes for check-scrub-admission-r52.py

Seat: R52CritResultShape (critic, leaf). Counter bytes under test: working-tree
`tools/check-scrub-admission-r52.py` sha256 `bd5563af9b4a978552130e15d583614000e225fb7fb3f7c2e1c193dba7c08a80`
== `git show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:tools/check-scrub-admission-r52.py` ==
FROZEN-hashes.txt line for the counter (all three printed `bd5563af…`; `git status --porcelain
tools/check-scrub-admission-r52.py` empty). The battery therefore exercised the frozen bytes.

Precheck at the freeze revision (observed): `python3 …/check-scrub-admission-r52.py --revision
ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 --section-hash` → `structural_ok: 1`, `problems: []`,
`section_sha256` GR1 `98fa4e07768d240eaf5ea2cce13ce0623fdb756054e5df9f7b9fe68ab2e63987`, GR2
`9fd581a0c9d02b02100b6a15648b7c6e4be896ac746ed09303a88dc8a24f0ec5`, GR3
`0405f38a5783c49b6c078b118c9868543eb494b43f8b1c5e6c14284a123b9eac` — matches the round claims
exactly (FROZEN.md; task text).

## Method

Synthetic dispatch/results/wave-dir fixtures under `/fast/scratch/hyaku/tsukuroi-r52/R52CritResultShape/fx/`
(driver `battery.py`, archived at `shapes/../battery.py`). Each shape runs the counter with the
production-flag set `--revision ff9470e… --lane tsukuroi-shokunin` plus the fixture overrides
`--results-file --dispatch-file --wave-dir` (the counter's documented fixture overrides,
docstring lines "Fixture overrides (control batteries only; production reads the revision's
committed bytes)"). Golden seat `R52RevGR1a` (reviewer, GR1): report `.md` line 1
`ROW GR1 VERDICT: holds`, line 2 `SECTION SHA256: 98fa4e…`, body ≥300 bytes citing
`scrub.c:1` + `sysfs.c:1` (both resolve in pinned snapshots). Positive control s00 credits the
seat, so the harness is sound. Wall time 1.13 s for all 17 runs; no selftest-bearing command used.

## Per-shape results (seat leg extracted from `per_row.GR1.seats.R52RevGR1a`)

| shape | credited | observed `detail` |
|---|---|---|
| s00 golden control | yes | `R52RevGR1a.md` |
| (a1) results `output` = JSON **string** carrying the verdict | **yes** | `R52RevGR1a.md` |
| (a2) report .md line 1 = JSON-wrapped verdict | no | ``first line '{"report": "seat", "verdict": "holds"}'`` |
| (a3) report .md line 1 = bare JSON string of verdict | no | ``first line '"ROW GR1 VERDICT: holds"'`` |
| (b) preamble line before the verdict line | no | `first line 'Reading GR1 against pinned bytes.'` |
| (c) two results entries for one seat | no | `not exactly one results entry` |
| (d1) dispatch reviewer / results critic | no | `results agent 'critic' != reviewer` |
| (d2) dispatch critic / results reviewer | no | `dispatch agent 'critic' != reviewer` |
| (d3) dispatch omits the seat | no | `dispatch agent None != reviewer` |
| (e1) results `output` = `""` | no | `no completed output` |
| (e2) report file empty (0 bytes) | no | `report too short` |
| (f) trailing space after `holds` on line 1 | no | ``first line 'ROW GR1 VERDICT: holds '`` |
| (g) body contains `ROW GR2 VERDICT: holds` | no (bound `partly`) | `contradicting line ROW GR2 VERDICT: holds` |
| (h) results `output` = JSON **object** | **yes** | `R52RevGR1a.md` |
| (i) CRLF line endings in report | no | ``first line 'ROW GR1 VERDICT: holds\r'`` |
| (j) dispatch lists the seat twice (critic, reviewer) | **yes** (last wins) | `R52RevGR1a.md` |
| (k) hash line missing/blank | no | `second line ''` |

All runs exited 1 as expected (only one seat bound, admission marks absent → predicate FAIL);
the seat-level binding above is the finding. Raw counter output per shape:
`.ufo/waves/round-52/w1/R52CritResultShape/shapes/<tag>/counter-out.json` (+ `summary.json`,
fixture `dispatch.json`/`results.json`).

## Is the 18-seat leg robust to the shapes the orchestrator actually produces?

Yes — supported on both channels:

- **Results channel.** Round-51 `w1-results.json` entries are `{name, agent, output:
  "<json string>", note: null}` (e.g. `R51W1PreRevGR1a` at `.ufo/waves/round-51/w1-results.json:6-15`).
  `bind_seat` (tools/check-scrub-admission-r52.py:253-261) never parses `output` content: it
  requires exactly one entry with the seat name, `agent` equal to the universe role, and a
  truthy `output`. Shapes (a1)/(h) confirm any non-empty output shape — JSON string, JSON
  object, plain text — credits identically; (c)/(d1)/(e1) confirm the one-entry/one-role/non-empty
  guards reject with precise detail strings. The run-9 failure mode (counter choking on
  JSON-wrapped output) is absent by construction: the results file carries identity and
  completeness, never the verdict.
- **Dispatch channel.** Real on-disk round-52 dispatch `.ufo/waves/round-52/w1-dispatch.json`
  has `taskCall.tasks` = 64 rows of `{name, agent}`; all 18 counted seats
  `R52RevGR<n>{a,b,c}`/`R52CritGR<n>{a,b,c}` present, 0 duplicate names, roles reviewer/critic
  exactly as `dispatch_tasks`/`universe()` expect (observed via `git show` attempt +
  JSON parse of the working-tree file; the file is **not yet committed** at ff9470e —
  `git show ff9470e:.ufo/waves/round-52/w1-dispatch.json` → "exists on disk, but not in
  'ff9470ea…'"). (d2)/(d3) confirm missing or mismatched dispatch rows fail the seat closed.

The binding weight therefore sits entirely on the per-seat report file — consistent with the
frozen contract "Seat reports bind on FILES, first line `ROW GR<n> VERDICT: …`, second line
`SECTION SHA256: <hex>`" (counter docstring). The fragile channel is **seat-side header
discipline**, and six realistic seat shapes kill a seat's credit: JSON-wrapped first line,
preamble line, trailing space, CRLF endings, blank second line, empty file (s02–s04, s10, s11,
s14, s16). Trailing space and CRLF are the dangerous ones — invisible in an editor. This is
strictness by design (`VERDICT_RE.fullmatch`, counter line ~300), not a defect: every
rejection is closed-world (a seat that follows the two-line convention credits; every deviation
rejects loudly with the offending line quoted in `seat_notes`).

## Observations (not defects this round; for the record)

1. **Dispatch duplicate-name collapse** (s15): `dispatch_tasks` builds `{t.get('name'):
   t.get('agent') …}`, so two `taskCall.tasks` rows for one seat silently keep the LAST role;
   the seat binds if the last row carries the declared role. The results side enforces
   exactly-once; the dispatch side does not. The real dispatch has 0 duplicate names, and the
   counter is frozen pre-round — no change proposed now; flagging for a future counter rev.
2. **`output` content is never cross-checked** against the report verdict: a results entry
   saying `"verdict": "fails"` with a `holds` .md still credits (by design — the file binds).
3. **Production sequencing** [INFERENCE from code + observed absence]: the counted run's
   production form (no overrides) reads `git show REV:.ufo/waves/round-52/w1{,-dispatch.json,
   -results.json,/<seat>.md}`; at ff9470e the wave artifacts are not committed yet, so the L1's
   counted `--revision` must be a cutover commit carrying dispatch, results, and the 18 seat
   reports (or the controls-style overrides must be used, as the round claims do for the
   battery).
4. **Cross-row verdict guard** (s12): any `ROW GRx VERDICT: <word>` after line 2 with
   x ≠ row or word ≠ line-1's word downgrades the seat to `partly`, which blocks the whole row
   (`row_ok` requires `not blocking`) even before the hash check. Seats quoting the header
   format inside their body will block their own row.

## Not done

- Full 18-seat end-to-end PASS exercise (that is the L1's counted run at the freeze/cutover;
  this seat isolated `bind_seat`/`dispatch_tasks` per shape as assigned).
- Lint/quote/citation-leg stress (out of W-B3 scope).
- No tool installs (none needed). Scratch `/fast/scratch/hyaku/tsukuroi-r52/R52CritResultShape/fx/`
  (396G free at start) removed after receipt copy.
