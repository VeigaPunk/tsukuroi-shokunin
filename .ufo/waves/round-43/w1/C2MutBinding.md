VERDICT: defect-found

# Seat C2MutBinding — item C2-7: binding attacks on `tools/check-scrub-record-r43.py` beyond controls C2-K0..K13

Counter under attack: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-record-r43.py`, sha256
`b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854` (frozen declaration value,
`SCORECARD.md:2662`; recomputed over the lane working file this run — unchanged). The binding under attack is
`bound()` (`tools/check-scrub-record-r43.py:178-194`) with helpers `declared_line` (:157-168) and `first_line`
(:171-175); the frozen rule it implements is the docstring :21-27 ("the declared verdict line is the JSON field
`verdict_line` when the recorded output parses as a JSON object, otherwise the output's first non-empty line, and
it must be exactly `ROW SR<n> VERDICT: <holds|partly|fails>` for that row (anchored, a line of its own); the
committed report … must open with that identical line") and `SCORECARD.md:2662` ("declared verdict line = JSON
`verdict_line` field, else the output's first non-empty line … and the committed report's first line").

## Method

Every variant is a commit in a private scratch clone of the lane, scored by the frozen counter run from its lane
path (never copied, never edited):

```
S=/fast/scratch/hyaku/tsukuroi-r43/C2MutBinding
D=$(mktemp -d "$S"/c2mutbind.XXXXXX/clone)          # driver.py does: git clone -q --shared <lane> "$D"
git -C "$D" remote remove origin
git -C "$D" rev-parse --show-toplevel               # asserted == "$D" before every commit
git -C "$D" checkout -q --detach -f 6951ead90566b2d74f7c45b4efca29246badad64 && git -C "$D" clean -qfdx
# write candidate surface (controls/c2-candidate/: entry r43, r42 pointer, SOURCES.md, ioctl.c, capture.txt)
#   + forged .ufo/waves/round-43/w2-dispatch.json, w2-results.json, w2/<seat>.md  (variant-specific)
git -C "$D" add -A
git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -q --allow-empty -m 'binding variant <ID>'
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-record-r43.py \
        --lane "$D" --revision <sha> --sessions "$S"/c2mutbind.XXXXXX/no-sessions
```

The golden fixture (GOLD) replicates declared control C2-K3 exactly (candidate surface + forged dispatch
`{"taskCall":{"tasks":[6 × {name, agent, task}]}}`, results entries with JSON outputs
`{"verdict_line": "ROW SR<n> VERDICT: holds", "row", "seat"}`, reports opening with the verdict line). Observed
GOLD: exit 0, `verdict PASS`, `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, verdicts_ok 3,
novelty_base_hits 0, pointer_ok 1, transcripts_bound 0` (receipt `GOLD.jsonl` line 2, fixture
`0e361c62eab997dc54745ae41b370907915915cd`). This is the declared K3 limit: the committed-bytes predicate cannot
tell forged orchestrator records from real ones (`SCORECARD.md:2666`). Every variant below differs from GOLD only
in the binding artifacts; `driver.py` asserts each variant's file set differs from GOLD's before committing.
22 fixtures, 22 counter runs, ~4 s wall total; all 22 matched the classification predicted from the code
(`summary.jsonl`: `"all_matched_expectations": true`).

## Results

| ID | attack (forged bytes) | predicted | observed | fixture sha |
|---|---|---|---|---|
| GOLD | C2-K3-equivalent golden | PASS | PASS | `0e361c62` |
| A | (a) SR1 reviewer output `{"verdict_line": "ROW SR1 VERDICT: holds", "verdict": "fails"}` | PASS | PASS | `7df3aab6` |
| B | (b) SR1 reviewer output is a JSON list `[{"verdict_line": … holds …}]` | FAIL | FAIL | `df721b92` |
| C | (c) SR1 reviewer output `ROW SR1 VERDICT: holds\nROW SR1 VERDICT: fails\n` | PASS | PASS | `c16e1bec` |
| D1 | (d) SR1 report first line `ROW SR1 VERDICT: holds   ` (trailing spaces) | FAIL | FAIL | `2b545472` |
| D2 | (d) SR1 report with CRLF endings (`…holds\r\n\r\nforged report body\r\n`) | PASS | PASS | `e3536356` |
| E1 | (e) dispatch lists `C2RevSR1`/`reviewer` twice | FAIL | FAIL | `fba9e4f6` |
| E2 | (e) dispatch adds a second `C2RevSR1` task with agent `critic` | PASS | PASS | `e0122395` |
| F1 | (f) SR1 reviewer results entry has `"agent": "critic"` (dispatch says reviewer) | FAIL | FAIL | `08cae018` |
| F2 | (f) dispatch and results both say agent `executor` for `C2RevSR1` | FAIL | FAIL | `2fb57dbe` |
| G1 | (g) SR1 reviewer verdict line (and report) name SR3 | FAIL | FAIL | `9a031c3f` |
| G2 | (g) SR1↔SR3 reviewers cross-wired (each binds the other's row) | FAIL | FAIL | `8ef01dd3` |
| H | extra: SR1 reviewer output `  ROW SR1 VERDICT: holds  ` (leading+trailing spaces) | PASS | PASS | `0084ef58` |
| I | extra: SR1 report opens with two blank lines, verdict line third | PASS | PASS | `d330dd3f` |
| J1 | extra: `w2-results.json` is a top-level JSON list | CRASH | CRASH | `d811a47c` |
| J2 | extra: `w2-dispatch.json` is a top-level JSON list | CRASH | CRASH | `9ad72cc6` |
| K | extra: output `{"verdict_line": "…fails…", "verdict_line": "…holds…"}` (duplicate keys) | PASS | PASS | `938aa12f` |
| L | extra: results lists the `C2RevSR1`/`reviewer` entry twice | FAIL | FAIL | `8f90ee72` |
| M | extra: SR1 critic `partly` + forged residual `C2ResSR1` reviewer `holds` | PASS | PASS | `ce5cbade` |
| N | extra: SR1 report starts with a UTF-8 BOM | FAIL | FAIL | `a5b67eb2` |
| O | extra: SR1 reviewer output JSON preceded by a UTF-8 BOM | FAIL | FAIL | `ecd876ef` |
| Q | extra: JSON `verdict_line` `"ROW SR1 VERDICT: holds "` (trailing space inside the string) | FAIL | FAIL | `439c6c67` |

Observed values quoted from each variant's receipt (`<ID>.jsonl`, line 1 = metadata, line 2 = the counter's full
JSON output; `verdicts_ok` was 3 on every PASS and 2/1 on the FAILs, always losing exactly the attacked seat).

## Defects — PASSes that should not, with the exact counter line responsible

1. **H — a recorded output line that is not exactly the verdict line binds anyway.** Forged SR1 reviewer output
   `  ROW SR1 VERDICT: holds  ` (leading and trailing spaces): the counter binds `holds`, `verdicts_ok 3`,
   exit 0 PASS (`H.jsonl`; fixture `0084ef58`). The frozen rule says the declared line "must be exactly
   `ROW SR<n> VERDICT: <holds|partly|fails>`" (`tools/check-scrub-record-r43.py:23-25`); the line the rule names
   is "the output's first non-empty line" (:23), which here is `  ROW SR1 VERDICT: holds  ` — not exactly the
   pattern. Responsible line: `tools/check-scrub-record-r43.py:167` (`return ln.strip()` in `declared_line`) —
   the strip runs before the exactness test at :189, so the counter tests a different string than the rule
   names. Severity: low (whitespace only; the verdict word itself is unambiguous), but it is a rule-vs-code
   deviation, and it is asymmetric with the JSON path, which does not strip (variant Q fails on a trailing
   space inside the JSON string, :189 fullmatch).
2. **I — a committed report that does not open with the verdict line binds anyway.** Forged
   `.ufo/waves/round-43/w2/C2RevSR1.md` starting with two blank lines before `ROW SR1 VERDICT: holds`: the
   counter binds `holds`, `verdicts_ok 3`, exit 0 PASS (`I.jsonl`; fixture `d330dd3f`). The frozen rule says the
   report "must open with that identical line" (:25-26); a file whose first line is empty does not open with it.
   Responsible lines: `tools/check-scrub-record-r43.py:173-174` — `first_line` skips every blank or
   whitespace-only leading line (`if ln.strip():`), so the comparison at :193 is against the first *non-empty*
   line, not the first line. Severity: low (only whitespace-prefixed reports slip past; any non-blank wrong
   first line still fails, as K13 and variant D1/N show), but again a rule-vs-code deviation.
3. **K — duplicate `verdict_line` keys: last one wins, silently overriding an earlier `fails`.** Forged SR1
   reviewer output `{"verdict_line": "ROW SR1 VERDICT: fails", "verdict_line": "ROW SR1 VERDICT: holds"}`: the
   counter binds `holds`, `verdicts_ok 3`, exit 0 PASS (`K.jsonl`; fixture `938aa12f`). Responsible lines:
   `tools/check-scrub-record-r43.py:160-164` — `json.loads` keeps the last duplicate key (Python semantics), and
   the counter never learns a contradiction existed. The frozen rule says "the JSON field `verdict_line`"
   (:22-23) without defining duplicate-key behavior, so this is an implementation-defined choice on ambiguous
   input rather than a clean rule violation; a record whose first-declared verdict is `fails` and whose
   last-declared is `holds` is bound `holds`. Severity: low/exotic (hand-written JSON), but it is the same shape
   as defect A with the contradiction inside the anchor field itself.

## Rule-level blind spots — the counter conforms to the frozen rule; the rule is the weaker link

- **A (declared variant a): a contradictory sibling field is never read.** Output
  `{"verdict_line": "ROW SR1 VERDICT: holds", "verdict": "fails"}` binds `holds` → PASS (`A.jsonl`,
  `7df3aab6`). Per the frozen rule the declared verdict line IS the `verdict_line` field when the output parses
  as a JSON object (:22-23, `SCORECARD.md:2662`), so the counter does what the rule says; the `'verdict'` field
  is never consulted (`:162-164` read only `verdict_line`). Net effect: the kill rule "any bound `fails`"
  (`SCORECARD.md:2662`) sees only what binds, and a fails recorded outside the anchor field cannot bind.
- **C (declared variant c): a later retraction is invisible.** Output
  `ROW SR1 VERDICT: holds\nROW SR1 VERDICT: fails\n` binds `holds` → PASS (`C.jsonl`, `c16e1bec`). The rule
  anchors to the first non-empty line (:23) and says "A mention elsewhere counts for nothing" (:26); the later
  `fails` line is exactly such a mention. Same structural property as A: only the anchor line can bind a fails.
- **D2 (declared variant d, CRLF half): a CRLF report binds.** Report bytes with `\r\n` endings bind `holds` →
  PASS (`D2.jsonl`, `e3536356`). `first_line` normalizes with `rstrip('\r')` (:174). The line's content is
  identical, so under a line-oriented reading of "open with that identical line" this is conformant leniency;
  the trailing-space half (D1) is rejected (:174 keeps spaces), so the counter is strict there.
- **E2 (declared variant e, mixed-role half): a same-name different-role duplicate task is inert.** Dispatch
  with a second `C2RevSR1` task as `critic` still PASSes (`E2.jsonl`, `e0122395`): the binding is per
  (name, role) pair (:183, :185), and no counted seat queries `(C2RevSR1, critic)`. Conformant; the declared
  half (two tasks with the same name AND role, E1) is refused by the `!= 1` check at :183.
- **M: the residual escape hatch is forgeable exactly like the main path.** SR1 critic `partly` + forged
  `residual-dispatch.json` / `residual-results.json` / `residual/C2ResSR1.md` (reviewer, `holds`) → PASS
  (`M.jsonl`, `ce5cbade`). This is the declared K3-class limit applied to the residual wave (rule :27-30); the
  committed-bytes predicate cannot tell these forged records from real ones either.

## Robust confirmations — no false PASS (each refused by the named line)

- **B** (output is a JSON list): `declared_line` takes the dict branch only (:162 `isinstance(obj, dict)`), so a
  list falls to the raw first non-empty line `[{"verdict_line": …` which fails the anchored fullmatch at :189 →
  unbound, FAIL (`B.jsonl`, `df721b92`).
- **D1** (report first line trailing spaces): `first_line` keeps them (:174 strips only `\r`), :193 mismatch →
  FAIL (`D1.jsonl`, `2b545472`).
- **E1** (two dispatch tasks same name+role): `sum(…) != 1` at :183 → unbound, FAIL (`E1.jsonl`, `fba9e4f6`).
- **F1** (results entry agent differs): the :185 filter requires `agent == role` → no entry → FAIL
  (`F1.jsonl`, `08cae018`). **F2** (both records moved to `executor`): dispatch count 0 at :183 → FAIL
  (`F2.jsonl`, `2fb57dbe`).
- **G1/G2** (verdict line for the wrong row): :190 `m.group(1) != row` → unbound, FAIL (`G1.jsonl` `9a031c3f`,
  `G2.jsonl` `8ef01dd3`; G2 also drops SR3's reviewer, `verdicts_ok 1`).
- **L** (two results entries same name+role): `len(ent) != 1` at :186 → FAIL (`L.jsonl`, `8f90ee72`).
- **N** (report BOM) and **O** (output BOM): BOM survives into the compared strings / breaks `json.loads` →
  unbound, FAIL (`N.jsonl` `a5b67eb2`, `O.jsonl` `ecd876ef`).
- **Q** (JSON `verdict_line` with trailing space): the JSON path does not strip, :189 fullmatch fails → FAIL
  (`Q.jsonl`, `439c6c67`) — the strict twin of defect H.

## Robustness finding (crash, not a false PASS)

- **J1/J2 — malformed orchestrator record shapes crash the counter instead of scoring FAIL.**
  `w2-results.json` as a top-level JSON list → `AttributeError: 'list' object has no attribute 'get'` at
  `tools/check-scrub-record-r43.py:185` (`J1.jsonl` line 2, fixture `d811a47c`); `w2-dispatch.json` as a
  top-level list → same at :182 (`J2.jsonl`, `9ad72cc6`). Both exit 1 with an empty stdout — no JSON verdict
  line — breaking the declared output contract ("Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read
  error", :29-30). By exit code alone a crash is indistinguishable from FAIL, and a consumer that parses the
  last stdout line (as `controls/run_controls_c2.py:172-174` does) gets an error, not a verdict. The `or {}`
  coercions at :180-181 only absorb *falsy* JSON values (`null`, `[]`); any non-dict truthy shape crashes. No
  false PASS is reachable this way — every malformed shape I tried either crashes or leaves the seat unbound —
  but the counter should degrade to a clean FAIL for these shapes.

## Summary for the planner

The anchored binding is **structurally sound against the declared attack classes**: wrong-row lines (g),
agent mismatches (f), duplicate tasks/entries (e), list outputs (b) and whitespace/BOM-mangled reports (d1, n)
all refuse to bind, each at a single named check. What it cannot do is see contradictions that sit outside the
anchor: a `fails` recorded as a sibling JSON field (a), on a later line (c), or behind a duplicate key (K) never
binds, so the kill rule "any bound `fails`" only ever fires on the anchor's own word. Two code-level leniencies
deviate from the frozen rule's letter and produce PASSes a strict reading forbids: the results line is stripped
before the exactness test (:167, defect H) and the report check skips leading blank lines (:173, defect I). Both
are whitespace-class, exploitable only by a seat that already controls its own recorded output and report — the
same trust boundary K3 already declares unverifiable — so I read them as hardening items for a future counter,
not as grounds to reject the C2 claim. The crash shapes (J1/J2) are a robustness gap with no false-PASS path.

## Not done

- I did not attack the quote/proposition/host/registry/novelty/pointer conjuncts (battery K7-K12 own those) and
  did not re-run any C1 counter or census selftest (not this seat's item).
- `transcripts_bound` was kept at 0 by pointing `--sessions` at a nonexistent dir in every run (recorded in each
  receipt); I did not probe the host sessions side-channel, which the counter reports outside the predicate
  (docstring :31-33).
- I did not test verdict words other than `holds|partly|fails` in the anchor (the :189 alternation is exact) nor
  the `SR\d` single-digit bound against two-digit row names beyond G1 (a line `ROW SR11 …` cannot fullmatch).

## Cleanup

- Scratch `/fast/scratch/hyaku/tsukuroi-r43/C2MutBinding/` (driver + clone + work dirs) removed after copying
  receipts; nothing under `/tmp` was used. The lane was only read, plus the sanctioned writes: this report and
  the receipts in `.ufo/waves/round-43/w1/C2MutBinding/` (22 variant receipts + `summary.jsonl` + `driver.py`).
- Counter file untouched: sha256 `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854` before and
  after (recorded in every receipt line 1).
