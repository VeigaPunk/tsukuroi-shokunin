VERDICT: defect-found

## Result

Exercised the frozen C1 counter at `8029cdba1049df25632c91a23c8db4eefb54be5f` with a synthetic, valid 18-seat cohort. The baseline was `PASS`, `marks={"entry":true,"readme":true,"skill":true}`, `marks_ok=3`; all fixture cases retained `structural_ok=1, corr_ok=1, quotes_ok=3, verdicts_ok=3, seats_ok=18`. Thus the following verdict changes isolate the marks leg. Full counter JSON and reproducible fixture drivers are in `.ufo/waves/round-50/w1/R50ExecMarkCounter/`.

| Case | Counter verdict | `marks` / `marks_ok` | Receipt |
|---|---|---|---|
| Baseline | PASS | `{entry:true, readme:true, skill:true}` / 3 | `R50ExecMarkCounter/00-baseline-pass.json` |
| (a) no SKILL mark | FAIL | `{entry:true, readme:true, skill:false}` / 2 | `R50ExecMarkCounter/a-no-skill-mark.json` |
| (b) SKILL mark only as substring of longer line | FAIL | `{entry:true, readme:true, skill:false}` / 2 | `R50ExecMarkCounter/b-skill-substring.json` |
| (c1) “not admitted round 50” | FAIL | `{entry:true, readme:false, skill:true}` / 2 | `R50ExecMarkCounter/c1-not-admitted.json` |
| (c2) “remains unadmitted round 50” | FAIL | `{entry:true, readme:false, skill:true}` / 2 | `R50ExecMarkCounter/c2-remains-unadmitted.json` |
| (c3) “never admitted round 50” | FAIL | `{entry:true, readme:false, skill:true}` / 2 | `R50ExecMarkCounter/c3-never-admitted.json` |
| (c4) “GR1-GR3 are unadmitted round 50” | FAIL | `{entry:true, readme:false, skill:true}` / 2 | `R50ExecMarkCounter/c4-gr-unadmitted.json` |
| (d) entry heading twice | PASS | `{entry:true, readme:true, skill:true}` / 3 | `R50ExecMarkCounter/d-entry-heading-twice.json` |
| (e) entry heading only inside fenced code | PASS | `{entry:true, readme:true, skill:true}` / 3 | `R50ExecMarkCounter/e-entry-heading-in-fence.json` |

The counter rejects (a), (b), and all four specified README negations, but passes (d) and (e): its entry check is presence of an exact line, not uniqueness or rendered-Markdown presence. The skill check also accepts the exact mark inside a code fence (`y4-skill-in-fence.json`). Source: frozen `tools/check-scrub-admission-r50.py:96-99,360-370`; `marks['entry']` uses membership in `entry.split('\n')`, while the skill test compares stripped lines and neither checks fenced context or count.

## Negation coverage

The existing `NEGATE_RE` is `unadmitted|not admitted|never admitted|stay pending|stays pending` (frozen counter lines 98-99). It covers all four requested phrasings when they occur in the same sentence as the filename and `admitted round 50`; measured results are c1–c4 above. It does **not** cover ordinary hostile variants or a negation separated into another sentence. In the additional fixtures, all of these were accepted as `PASS`, `readme:true`, `marks_ok=3`: “no longer admitted,” “not currently admitted,” “isn't admitted,” “has not been admitted,” “not yet admitted,” “un-admitted,” “withdrawn,” and a clean admission sentence followed by “GR1-GR3 are unadmitted round 50.” See `x1`–`x7`, `x9` receipts. Conversely, `x8-unrelated-negation.json` was rejected (`readme:false`) because “not admitted as a kernel fact” appears in the same sentence, despite not negating the round-50 admission; `x10-stay-pending.json` was also rejected by the broad `stay pending` alternative. `marks_leg` splits on sentence punctuation at line 366 and only tests the candidate sentence, explaining the cross-sentence escape and same-sentence false rejection.

The regex therefore catches the four named forms but does **not** cover common hostile-editor variants or cross-sentence contradiction, and can reject unrelated same-sentence negation. A measured candidate guard (probed against all four requested negatives, the additional hostile variants, positive unrelated-negation examples, and the frozen README/entry/SKILL content) is:

```python
NEGATE_RE = re.compile(
r"(?:not|never|no\s+longer|isn'?t|has\s+not\s+been|not\s+yet|un-?)\s*"
r"(?:currently\s+|yet\s+|been\s+)?admitted\s+round\s*50")
RETRACT_RE = re.compile(r"\b(?:in error|withdrawn|revoked|retracted|void)\b")
GR_CONTEXT_RE = re.compile(r"\b(?:GR1|GR2|GR3)\b")
# Veto the README mark if any sentence naming the entry or a GR row denies/retracts admission.
denied = any((name in sentence or GR_CONTEXT_RE.search(sentence))
             and (NEGATE_RE.search(sentence) or RETRACT_RE.search(sentence))
             for sentence in sentences)
```

The candidate probe accepted the positive cases, rejected the named and tested hostile negations (including cross-sentence GR1–GR3 denial), and found no such denial/retraction sentence in the frozen README, entry, or SKILL. Exact source evidence for the four requested forms is the per-case JSON above; candidate measurement was performed in scratch and its exploratory script was not retained as a receipt.

## Entry/skill mark integrity and retained pending text

The freeze entry already contains `## Gate status — round 50 (pending; the round-50 cohort has not settled)` at line 297, and the entry says “This heading records **pending**, not admission” at line 307. The baseline fixture appends the admitted heading without removing those bytes and still scores `PASS`; the dedicated `z3-pending-heading-retained.json` does too. `z2-entry-contradiction.json` also passes with an explicit “GR1-GR3 are not admitted round 50” sentence after the admitted heading. Thus a present admission heading can coexist with retained pending/contradictory prose and satisfy `marks_ok`.

Additional shape probes: entry trailing whitespace and ASCII hyphen variants fail (`y1`, `y2`); skill trailing whitespace passes because its line is stripped (`y3`). A README filename and admission phrase split across sentences fails (`z4-readme-split-sentences`). These are captured in the corresponding receipts.

Recommended implementation shape (not applied; this seat only exercised the counter): count exactly one unfenced round-50 gate heading in the entry and require it to equal `MARK_ENTRY`; count exactly one unfenced `MARK_SKILL` line; and make README negation/retraction vetoes sentence-scoped to the filename or a GR row, using a negation pattern tied to the round-50 admission phrase rather than generic `stay pending`.

## Commands and scope

Ran `TMPDIR=/fast/scratch/hyaku/tsukuroi-r50/R50ExecMarkCounter timeout 900 python3 drive.py` and `TMPDIR=/fast/scratch/hyaku/tsukuroi-r50/R50ExecMarkCounter timeout 600 python3 drive2.py`, each from the seat scratch directory. Both completed with the observed results recorded above. The fixture drivers read all lane bytes via `git show <freeze>:<path>` and invoked the frozen counter with fixture file overrides; no lane-tracked files were modified. Scratch was removed after copying receipts. No build, lint, test suite, or formatter was run.
