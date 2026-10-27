VERDICT: defect-found

Seat C2MutFinalResidual — item C2-5, residual-binding attack (C2ResSR<n>), wave w2, frozen tip
`8eee79db608b5815c325a5af7cbfdeac50eda9f4`. Evidence: `.ufo/waves/round-44/w2/C2MutFinalResidual/`
(`probes.jsonl` 39 probe lines, `crash-stderr.txt`, `baseline-tip.json`).

## Method

Scratch clone `git clone -q --shared` of the lane, origin removed, `git rev-parse --show-toplevel`
asserted equal to the clone; detached at the frozen tip. Frozen counter verified byte-identical to the
declared sha256 `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059` before scoring.
Baseline at the tip: verdict FAIL with `verdicts_ok 0` (w2 verdict seats not committed at the tip) and
every lexical/global conjunct passing (`rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1,
novelty_base_hits 0, pointer_ok 1, snapshots_ok, capture_ok`) — exactly the declared state. Each probe
is one fixture-identity commit (`user.name=fixture <fixture@invalid>`) on top of the tip, scored with
`python3 <clone>/tools/check-scrub-record-r44.py --lane <clone> --revision <sha> --sessions <empty
scratch dir>`; `transcripts_bound 0` on every probe. Frame for residual probes: main records forged
with `C2RevSR7 = partly`, all other counted seats `holds`, so SR7's `verdict_ok` isolates the
`C2ResSR7` binding. Between probes the clone is reset (`checkout --detach -f <tip>`, `clean -qfdx`);
after the run the clone and scratch were removed. The lane got no writes outside this report and the
receipt dir; no git/jj mutation in the lane.

## Finding 1 (defect, crash — no verdict line on forged containers)

Seven committed-bytes shapes crash the frozen counter with an `AttributeError` traceback, exit 1 and
**zero stdout lines** — the counter's declared output contract ("Output: one JSON line; exit 0 PASS,
1 FAIL, 2 usage/read error") is broken, and a scoring harness that reads the verdict line (as
`run_controls_c2.py` does) cannot score the revision at all:

- `residual-results.json` a top-level non-empty JSON array (R2d) — full stderr in `crash-stderr.txt`:
  `bound()` line 212, `res.get('results')` on a `list`.
- `residual-dispatch.json` a top-level non-empty JSON array (R2e).
- `taskCall` an array (R2f); `tasks` a dict (R2g); `results` a dict (R2h) — all residual paths.
- The same shared `bound()` helper serves the main binding: `w2-results.json` (X1) and
  `w2-dispatch.json` (X2) as top-level non-empty arrays crash identically, with no `partly` needed.

The residual instances only detonate behind the `partly` gate (X3: all-holds main records + a malformed
`residual-results.json` array → clean exit 0 PASS, residual never read), but the main-record instances
have no such gate. Exit code stays 1 (nominally FAIL), so this is denial-of-verdict, not a false PASS.

## Finding 2 (binds — undeclared shape accepted, coverage finding)

Duplicate `verdict_line` keys in the residual results output **bind — last key wins** (Python `json`
semantics; no `object_pairs_hook` rejection):

- R1: `{"verdict_line": "ROW SR7 VERDICT: fails", "verdict_line": "ROW SR7 VERDICT: holds"}` →
  residual binds `holds`, `verdicts_ok 3`, verdict PASS (exit 0).
- R1b: order reversed → binds `fails`, row not ok (exit 1). The last key decides in both directions.
- R1c: adding an explicit contradictory `verdict` key closes it (binds nothing).

The frozen contract says only "must hold a string `verdict_line`"; the w1 battery K0–K19 has no
duplicate-key shape, so this acceptance is undeclared. It does not falsify any declared conjunct, but
the residual gate — the thing that lets a `partly` row pass — accepts a verdict-carrying shape the
declaration does not specify.

## What the residual binding refuses (killed, all structured FAIL, `residual: null`)

- Arrays as the recorded output (3): `["ROW SR7 VERDICT: holds"]` (R2), array of objects (R2b),
  `verdict_line` as an array (R2c).
- Missing/mismatched names (6): dispatch task without `name` (R3), results entry without `name` (R3b),
  results `agent` ≠ `reviewer` (R3c), dispatch task without `agent` (R3d), duplicated dispatch tasks
  (R3e), duplicated results entries (R3f) — the exactly-once rule holds on both files.
- Padded lines (5): JSON `verdict_line` with leading (R4) or trailing (R4b) space; raw output opened
  with two spaces (R4c, residual-side K14); report file first line padded (R4d) or blank-line-prefixed
  (R4e, residual-side K15) while the JSON line is clean.
- Contradictory JSON (1): `verdict_line` holds beside `verdict: fails` (R5, residual-side K16).
- Semantic gates: wrong-row residual `ROW SR8 …` on C2ResSR7 (R6); residual bound `partly` (R7) or
  `fails` (R7b) → row still not ok; `partly` with no residual at all (R0b, K5-equivalent); residual
  report file absent (R9); residual `holds` cannot rescue a main `fails` and is not even consulted
  (R8b).

Declared-legal binds reproduced as controls: legit residual JSON `holds` passes a `partly` row
(R0, K19-equivalent, verdicts_ok 3 PASS); consistent `verdict` key binds (R5b); all-holds main records
ignore residual records entirely (R8, gate confirmed); forged main records with all six seats `holds`
PASS with `transcripts_bound 0` (M-full-holds, K3 concession, by design).

## Main binding K14–K16 still refused (exact w1 battery shapes, at the frozen tip)

- M14 (K14 padded verdict line, two spaces, output and report): SR7 `rev` unbound → verdicts_ok 2, FAIL.
- M15 (K15 blank-line-prefixed verdict): SR9 `crit` unbound → verdicts_ok 2, FAIL.
- M16 (K16 contradictory JSON `verdict`): SR8 `crit` unbound → verdicts_ok 2, FAIL.

## Verdict rationale

No declared conjunct of the frozen C2 claim measured false, and every shape the declaration names as
refused is refused, so this is not `falsifies`. But the probe set found a real counter defect (Finding
1: seven forged record shapes deny the declared one-JSON-line verdict output) plus one undeclared
binding acceptance (Finding 2), hence `defect-found`.

## Proposed text (for the L1 to route; wording for SCORECARD/next-round ledger)

"Wave-2 residual-binding attack (C2MutFinalResidual, 39 probe commits at 8eee79db): the C2ResSR<n>
binding holds its declared lexical gates — exactly-once name/agent on both files, first-line report
identity, no padding, no contradictory `verdict`, wrong-row and wrong-word residuals, report presence —
and stays gated on `partly`; K14–K16 shapes remain refused on the main binding. Two findings route
forward: (1) duplicate `verdict_line` JSON keys bind last-key-wins (undeclared shape; reject via an
object_pairs_hook duplicate check or add a battery control); (2) a dispatch/results file that is valid
JSON but not the declared object shape (top-level array, or array/dict `taskCall`/`tasks`/`results`)
crashes `bound()` with `AttributeError` — exit 1 but no JSON verdict line, breaking the declared output
contract for both the residual and main bindings; harden the shape checks or record it as a named
input-robustness limit beside `transcripts_bound`."
