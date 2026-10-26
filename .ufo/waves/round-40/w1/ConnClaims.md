VERDICT: defect-found

Item X-1 (cross-claim patterns C1/C2; propose one generalized QUALITY criterion).

## Shared defect class: the counters read their own frozen constants, not the declaration's named parameters

Both round-40 counters were built to close the round-39 class "counter does not read what it credits"
(R39-CONTENT-UNREAD, R39-FIXTURE-MONOCULTURE; `corpus/lessons/round-39.md:70-71`). Both now read *some*
content (C1: the selftest's behavioural reaction to nine frozen mutants; C2: rule-cell tokens, derived
values, polarity, length, quote-at-cited-lines). But the residual, shared gap is at the *parameter* level:
**neither counter reads the specific content parameters the declaration names — C1 never reads the fixture
set (count, axes), C2 never reads the rule's proposition (only token presence). A writer who knows the
frozen counter can satisfy every frozen check while violating a declared parameter.** Both are demonstrated
empirically below with scratch-clone variants (lane untouched; origin removed; receipts committed under
`/ufo/waves/round-40/w1/ConnClaims-5/`).

### Demonstration 1 — C2: token-compliant false proposition passes (exit 0, rules_verified 8)

Variant commit `08997b7d5424aceae77b2f595e2b8dcc7c376380` (scratch clone `c2fx.1qBN0i`, lane untouched)
rewrites only the EX7 rule cell of `corpus/knowledge/pacman-exec-environment-r40.md:27` to:

> The running log line appears after Depends are checked, and a missing satisfy dependencies clause aborts
> the transaction whenever AbortOnFail is listed for any hook

This states the opposite of the declared claim ("EX7 `running` logged before `Depends` is checked";
SCORECARD.md:2304) and of the pinned source (log at `hook.c:653`, `_alpm_hook_run_hook` at `:660`;
`--ufo/waves/round-40/frozen/src/hook.c`, `grep -n "running '%s'"` / `grep -n "_alpm_hook_run_hook(handle, hook)"`).
Observed counter output (command: `python3 tools/check-exec-environment-r40.py --repo <clone> --revision 08997b7d… --branch master`):
`exit=0`, `"result": "PASS"`, `"rules_verified": 8`, EX7 `{"verified": true, "reasons": []}` — receipt
`c2-variant-false-ex7.json`. Every frozen check still passes because the rule contains all four EX7 tokens
(`Depends`, `running`, `AbortOnFail`, `satisfy dependencies`; `tools/check-exec-environment-r40.py:92`),
carries no NEG word (`:97` — reversed attribution/ordering is not a negation), is ≥12 words, contains no
own quote, and the value/source/host cells are untouched. The scripted-writer control the author did commit
(C2-K5, quote copied as rule + every token → FAIL, `controls/controls.jsonl:7`) does not cover a *false
proposition expressed without negation words*; my variant is exactly that missing arm and passes.

### Demonstration 2 — C1: four of the five declared fixtures pass (exit 0, survivors 0)

Variant commit `540c696c3e9ab7cf14f95045767715932f966836` (scratch clone `c1fx.yGc4JW`, lane untouched)
deletes the `storage-mounts-varied-multi` selftest case (`tools/tsukuroi-census.sh:3018-3024` — the only
fixture that varies subvolume, `subvolid=263,subvol=/machines`, and is a read-only btrfs mount among four
lines; the two remaining btrfs-mount fixtures both carry `subvolid=5,subvol=/`). Observed counter output
(`python3 tools/score-selftest-literals-r40.py --repo <clone> --revision 540c696c… --branch master --scratch <dir> --jobs 2`):
`exit=0`, `"result": "PASS"`, baseline `PASS (123 cases, 123 passed, 0 failed)`, `"mutants_applied": 9`,
`"survivors": 0`, `"selfref": 5` — receipt `c1-variant-4fixtures.json`. The counter never inspects the
selftest's fixture table: it only runs the 13-run mutant/neutral/selfref battery, and its PASS regex
captures the case count but discards it (`tools/score-selftest-literals-r40.py:55,92-108`). The declared
parameters "five mount-table fixtures that vary device, mountpoint, options, subvolume, line position and
fstype case, plus an unlistable root with btrfs mounted" (SCORECARD.md:2303; seat prompt) are therefore not
read: four of five cases and a lost variation axis still PASS.

## Comparison with QUALITY 72, 73, 80, 81, 87

- 72 (`R27-COUNTER-PERMISSIVE`, QUALITY.md:140) — should-fail cases before a count stands: both counters
  have committed should-fail batteries (`controls/controls.jsonl:1-14`). Not the gap.
- 73 (`R28-BATTERY-MEASURE`, :141) — committed battery whose count is the claim's measure: satisfied by
  both; the battery's mutants/tokens are author-chosen, which is exactly the residual surface.
- 80 (`R31-DEPTH-UNFALSIFIABLE`, :153) — one frozen predicate, snapshot pins, novelty sweep, cheapest
  controls under that predicate: C2 has novelty_base_hits and the do-nothing/held/forgery-style controls;
  C1's predicate still omits every fixture-content parameter (count, axes), so the declaration's concrete
  parameters are not part of the frozen predicate.
- 81 (`R31-SCRIPTED-NONREADER`, :157) — a mechanical predicate is a format check; the frozen control set
  includes a scripted fetch-and-fill writer scoring below the target. C2's K5 covers quote-copying only;
  no control generates a token-compliant *false proposition* (my EX7 variant is the missing one). C1 has
  no scripted fixture-builder control at all, so nothing forces the fixture set to instantiate the
  declared count/axes.
- 87 (`R39-CONTENT-UNREAD`, :171) — reads the rule cell / varies fixture shape: implemented via tokens and
  the one-literal fixture control (C1-K1, controls.jsonl:11), but the *parameters the declaration names*
  (five fixtures; six axes; the proposition itself) are still unread.

## Proposed QUALITY criterion (exact text)

**88. A counter's acceptance implies the declaration's named content parameters, with a control that
violates exactly one of them (R40-CLAIM-PARAMETERS):** where the declaration names concrete content
parameters of the scored artifact — a fixture count or an axis list, a per-row proposition, a required
ordering — the frozen predicate includes a check over those parameters themselves (the fixture set's size
and varied axes; the rule's stated proposition), never only over the counter's own constants derived from
them; and the pre-data controls include a variant that satisfies every other frozen check while violating
exactly one named parameter, which must fail. Failing examples (both from the round-40 controls/claims):
the round-40 C1 counter passes a census keeping four of the five declared mount-table fixtures and losing the
declared subvolume variation (case `storage-mounts-varied-multi` removed; receipt
`.ufo/waves/round-40/w1/ConnClaims-5/c1-variant-4fixtures.json`); the round-40 C2 counter passes an entry
whose EX7 rule states the opposite ordering (`running` logged after `Depends` are checked) while carrying
every frozen token, value and quote (receipt `.ufo/waves/round-40/w1/ConnClaims-5/c2-variant-false-ex7.json`).

## Scope notes

- All variants live in scratch clones (`/fast/scratch/hyaku/tsukuroi-r40/ConnClaims-5/`, `--shared`, origin
  removed, fixture identity `<fixture@shokunin.local>`); no lane file was edited, created or deleted; no
  host mutation; no subagents.
- I did not re-run the counters on the lane's own commits (the committed before/after receipts
  `after/c1-after-c707e35.jsonl`, `after/c2-after-bf23805.jsonl` and `controls/controls.jsonl` were used as
  recorded), and I did not run the census selftest on the live host.
