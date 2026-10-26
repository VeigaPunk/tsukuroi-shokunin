VERDICT: defect-found

# Seat C2CritControl — round-43 C2 battery attack (item C2-9)

Scope: `tsukuroi-shokunin/.ufo/waves/round-43/controls/run_controls_c2.py` and its outputs
(`C2-K*.jsonl`, `battery-summary-c2.jsonl`), scored by the frozen counter
`tools/check-scrub-record-r43.py` (sha256 `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854`),
against QUALITY 80/81/87/88/89/90.

Result in one line: **all 12 should-fail controls fail for the reason they name (none fails
incidentally), but the battery does not close the QUALITY 81/87(a)/88/89/90 families: at least
four cheap forgeries other than K3 pass the full predicate** — a statement that keeps every
frozen token but asserts the opposite (A-inv-SR1, A-inv-all), the scripted writer from K1 now
run under the full predicate with forged records (B-scripted), a counted seat's output JSON that
contains a literal `ROW SR3 VERDICT: fails` assertion while binding `holds` (C-smuggle), and a
`partly` verdict paid off with a planted residual-holds chain (D-residual).

## 1. Per-control verification: each should-fail control fails for its named reason

Checks are read from the runner's docstring (`run_controls_c2.py:9-25`) and from the counter
(`tools/check-scrub-record-r43.py`; line refs below). Every control result below is the
committed `C2-K*.jsonl` line 2 (counter JSON) in `.ufo/waves/round-43/controls/`.

| Control | Named reason | Observed failing conjunct | Mechanism (counter lines) |
|---|---|---|---|
| K0 | do-nothing BASE | `rows 0` | no `## SR<n>` sections at base; snaps/capture absent too |
| K1 | scripted writer, planted reports, no orchestrator records | `verdicts_ok 0` | no dispatch → `bound()` returns before parsing (`bound` 180-184: `tasks` empty → sum ≠ 1) |
| K2 | forged results without dispatch tasks | `verdicts_ok 0` | same: `w2-results.json` present but `w2-dispatch.json` absent → seats unbound |
| K4 | one counted `fails` | `verdicts_ok 2`, SR3 `verdict_ok false` | `'fails' in vs` → row not ok (`v_ok` 289-290) |
| K5 | one `partly` with no residual | `verdicts_ok 2`, SR1 `verdict_ok false` | `resid` None → `all(v=='holds') or resid=='holds'` false (289-290) |
| K6 | mention-not-assertion (QUALITY 90) | `verdicts_ok 2`, SR6 crit null | output not JSON → `declared_line` = first non-empty line = the disputing sentence; `re.fullmatch('ROW SR<n> VERDICT: …')` rejects (157-168, 189-191) |
| K7 | content-free statements | `props_ok 0` | tokens removed → `p_ok` false (277) |
| K8 | SR6 cites scrub.c only (S240 quotes dropped) | `quotes_ok 2`, SR6 `quote_ok false` | `files == {'scrub.c','ioctl.c'}` fails for SR6 (275) |
| K9 | one quote line shifted | `quotes_ok 2`, SR1 `bad 1` | quote text not on named snapshot line (268) |
| K10 | ioctl.c quote labelled S237 | `quotes_ok 2`, SR6 `bad 1` | `sid == SNAP[f][1]` fails (268) |
| K11 | round-42 entry without pointer line | `pointer_ok 0` | first 20 lines of r42.md lack the r43 name (319-321) |
| K12 | S240 row status `queued` | `sources_ok 0`, S240 false | `c[7] == 'mined'` fails (308-312) |
| K13 | JSON verdict_line holds, report opens with different line | `verdicts_ok 2`, SR3 rev null | `first_line(rep) != line` (192-194) |
| K3 | forged records must PASS (recorded limit) | `verdict PASS`, `transcripts_bound 0` | committed-bytes predicate cannot tell forged from real; transcripts advisory (docstring 41-42) |

`battery-summary-c2.jsonl` line 2: `should_fail_accepted 0, control_accepted 1` — consistent
with the table. No should-fail control fails on an incidental metric (each named conjunct is the
one that zeroed).

## 2. Cheap forgeries beyond K3 that PASS the full predicate

All fixtures built in scratch (`/fast/scratch/hyaku/tsukuroi-r43/C2CritControl`, gone after
cleanup; receipts copied to `w1/C2CritControl/`): a `--shared` clone of the lane at BASE,
candidate C2 surface from `controls/c2-candidate/` overlaid (same bytes the runner uses),
committed as fixture identity, scored with
`python3 tools/check-scrub-record-r43.py --lane <D> --revision <sha> --sessions <empty>`.
Full JSON receipts: `w1/C2CritControl/forgery-results.jsonl`; builder: `w1/C2CritControl/build_forgeries.py`.

| Fixture | Change vs candidate surface | Verdict | Failing/no conjunct |
|---|---|---|---|
| Z-k3 | none (control K3 reproduction) | PASS | — (harness parity) |
| A-inv-SR1 | SR1 statement replaced by the semantic negation, tokens `O_TRUNC _tmp rename unlink` kept verbatim; quotes/host/registry untouched | **PASS** | `props_ok 3 quotes_ok 3 host_ok 3 sources_ok 1 verdicts_ok 3 novelty 0 pointer 1` |
| A-inv-all | all three statements negated, all frozen tokens kept | **PASS** | same |
| B-scripted | scripted writer rows (K1's `scripted_entry`, token-list statements, real quotes) **plus forged all-holds records (K3's)** | **PASS** | same |
| C-smuggle | candidate entry; result output JSON for C2CritSR3 = `{"verdict_line":"ROW SR3 VERDICT: holds","note":"ROW SR3 VERDICT: fails"}` | **PASS** | `declared_line` prefers the JSON field (161-164); the literal opposing assertion is invisible to the predicate |
| D-residual | `C2CritSR1` partial partly + planted residual chain (`residual-dispatch/results`, `residual/C2ResSR1.md`) reading holds | **PASS** | `resid == 'holds'` → row ok (289-290) |
| E-dupdispatch | dispatch contains two tasks named `C2RevSR1` | FAIL | reviewer unbound (`sum != 1`, 183) — a should-fail shape the battery never includes |

Notes:
- A-inv-SR1's statement contradicts its own quotes (the quoted `scrub.c:517` shows
  `O_WRONLY|O_CREAT` with no `O_TRUNC`; the renamed success path is quoted at :925; `unlink`
  is quoted on `sock_path` at :1485), yet every check passes: the counter never reads
  statement↔quote agreement. This is the QUALITY 88 failing example family ("EX7 states the
  opposite ordering while carrying every frozen token, value and quote") and the QUALITY 87(a)
  "(or the opposite)" arm, and the QUALITY 89 literal-emitting writer.
- B-scripted is the QUALITY 81 writer scored under the *full* predicate (records present): it
  reaches the target, so the demanded control would not fail. K1 only fails because it omits the
  records — that is the K3 channel, not a content/truth gate.
- D-residual shows the residual channel is unguarded exactly like K3: a `partly` verdict plus a
  planted `holds` residual converts into full row credit; nothing checks the residual's truth.

## 3. QUALITY 80/81/87/88/89/90: which demanded controls are missing

- **80 (R31-DEPTH-UNFALSIFIABLE)**: present: K0 do-nothing; K1 ≈ "junk rows over real pinned
  sources". Missing: the "held knowledge restated under the new ids" arm; the "sourceless
  forgery" arm; the "each quote copied as its statement" arm; and the novelty sweep is
  token-grep only (`novelty_hits` 210-224 greps `O_TRUNC`, `scrub_resumed_stats`,
  `is_scrub_running_in_kernel`) with **no synonym/paraphrase sweep over SKILL.md/PROVINCE.md/
  corpus/**, and the scorecard declaration (`SCORECARD.md:2662`) does not record that limit
  (unlike C1's "named open" channels at :2667-2668).
- **81 (R31-SCRIPTED-NONREADER)**: demands the scripted fetch-and-fill writer *scored under the
  full predicate*, reading below target. K1 is scored without records (fails on the K3 channel);
  with records (B-scripted) it reads at target. The demanded control is missing and its expected
  outcome fails — the same gap round-31's K6 exposed.
- **87 (R39-CONTENT-UNREAD)**: content-free entry present (K7) ✓. The "(or the opposite)"
  statement arm is missing (A-inv-* passes). (The one-literal fixture-shape arm is for
  behavioural counters; not applicable.)
- **88 (R40-CLAIM-PARAMETERS)**: one-parameter violations present for quotes/position/id/status/
  pointer/report (K8-K13). But the declaration names each row's proposition as a content
  parameter (`SCORECARD.md:2662` row text), and there is no control violating exactly that
  parameter alone; A-inv-SR1 (violates SR1's proposition only) passes.
- **89 (R41-GUARD-BYPASS)**: demands the family member that emits exactly the required literals
  without reading the source, together with the verdict files that writer can plant, scored
  under the full predicate and refused by a *non-lexical* check; "where no such check refuses
  it the family is reported open, not closed". A-inv-*/B-scripted are that member and PASS; the
  only non-lexical gate (verdict binding) is itself forgeable (K3, declared). The family is
  open and is **not** recorded as open (the scorecard records only K3, :2666).
- **90 (R42-OBSERVED-CHANNEL)**: anchored asserted-line binding present and scored (K6, K13) ✓.
  Missing channel arms: the residual channel has no control at all (neither partly+residual-holds
  D-residual shape, nor partly+residual-fails, nor malformed residual records); the "exactly one
  entry" clauses of dispatch/results (score E-dupdispatch) are untested; and the JSON-`verdict_line`
  precedence (C-smuggle) is untested — a seat can record a literal `ROW SR3 VERDICT: fails`
  line in its own output and still bind `holds`.

## 4. Smallest safe corrections (draft)

Add to `run_controls_c2.py` (each scored under the frozen counter; each must FAIL except where
noted):
1. **K14** — candidate surface, all three statements replaced by their negation with every frozen
   token kept (counterpart of A-inv-all), forged all-holds records → must FAIL (fills 87(a)/88/
   89; currently PASS).
2. **K15** — K1's scripted writer now with forged all-holds records (counterpart of B-scripted)
   → must FAIL (fills 81/89; currently PASS).
3. **K16** — results output JSON carries `verdict_line` holds plus a literal
   `ROW SR3 VERDICT: fails` line in the same JSON, report opens with the holds line → must FAIL
   or be recorded as a named limit (fills 90 JSON-channel arm; currently PASS).
4. **K17a/K17b/K17c** — residual arms: `partly` + residual-holds (should PASS, declares the
   intended shape), `partly` + residual-fails (must FAIL), and residual records present but
   report-first-line mismatch (must FAIL) (fills 90 residual channel).
5. **K18** — dispatch with two entries for one seat → must FAIL (fills 90 "exactly one entry"
   clause; currently FAIL but untested).
6. **Declaration** — record alongside K3 that the literal-emitting/scripted-with-records family is
   open per QUALITY 89 (no non-lexical check refuses it), and record the token-vs-fact novelty
   limit per QUALITY 80 (no synonym sweep), both in `SCORECARD.md` round-43 declaration text,
   which today lists neither.

## Evidence

- `run_controls_c2.py` docstring 9-25 (control intent), 52-73 (`records`), 76-102
  (`scripted_entry`), 137-158 (K9-K13 constructions).
- `tools/check-scrub-record-r43.py`: 157-168 (`declared_line`), 178-195 (`bound`), 259-301
  (per-row checks), 304-321 (sources/pointer), 41-42 (transcript advisory).
- Control outputs: `controls/C2-K0..K13.jsonl` line 2 (per_row), `controls/battery-summary-c2.jsonl`.
- Forgery receipts: `w1/C2CritControl/forgery-results.jsonl` (7 fixtures, exit+verdict+per_row),
  `w1/C2CritControl/build_forgeries.py` (builder; clones verified by
  `git rev-parse --show-toplevel`).
- QUALITY: `corpus/QUALITY.md` items 80 (:153), 81 (:157), 87 (:171), 88 (:173), 89 (:175),
  90 (:177); declaration `SCORECARD.md:2662,2664-2668`.

Not run: C1 battery, census, live-host scrub probes (out of scope; read-only seat).
