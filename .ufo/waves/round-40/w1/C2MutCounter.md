VERDICT: defect-found

Seat C2MutCounter-3, item C2-12 (tsukuroi lane round 40 w1). Mutation test of the frozen C2 counter
`tools/check-exec-environment-r40.py` against the pre-data C2 controls
`.ufo/waves/round-40/controls/controls.jsonl`. Finding: of the five counter conjuncts probed, only the
NEG check is guarded by a frozen control (C2-K2a flips). Dropping the paraphrase check, accepting base
rows, skipping the value compare, and skipping novelty each flip **no** frozen control — four unguarded
conjuncts. Three of the four are live and guardable (proven with supplementary controls built in
scratch); the novelty term is structurally a lane-history constant and cannot be guarded by any control
of this design.

## Method

- Re-implemented only the C2 half of `.ufo/waves/round-40/controls/run_controls.py` in scratch
  (receipt `mut_counter.py`): `git clone -q --shared` of the lane at freeze `a447b67b2502bae1e96fda341ae5ad32243ae524`,
  `git remote remove origin`, `rev-parse --show-toplevel` asserted before every commit, fixture identity
  `fixture@shokunin.local`; candidate bytes from `git show bf2380503b8e4a5d33162026854b0b7b66d18b86:<path>`
  sha256-verified against `.ufo/waves/round-40/controls/candidate-sha256.txt` (`corpus/SOURCES.md`
  `1676992a3d2013e2c9e4a9d6715f704bb287e37cc6942bd0f05c5c1a2c2c42a1`, entry `2230ccaf4037ccfcb8628b97f15fcff9eca86f9e5e37bee1c5392712ce21c9ef`);
  variant builders K1–K6 copied verbatim; K0 = counter at base `53b294a274656be6479aadf2ec2fee890ded77ce`;
  K7 = candidate commit. Working tree at tip f951f288483c1af0cef4afd458488b84cf7a2165 hashes identical to
  the candidate files, so the landed state is the scored candidate.
- **Baseline validation**: the pristine counter reproduces all nine recorded C2 controls field-by-field —
  exit, result, rules_verified, source_ok, counts_ok, novelty_base_hits, duplicate_rows,
  duplicate_headings, and every row_reasons list identical. Observed: `validation vs controls.jsonl: OK`
  (receipt `validation.txt`). One immaterial deviation: my K0 runs with the candidate files present in the
  working tree; the counter reads entry/SOURCES only via `git show` at the bound revision
  (tools/check-exec-environment-r40.py:262-263), so tree state cannot affect it — confirmed by the
  field-identical reproduction.
- Mutants: exact substring replacements on the frozen counter bytes; each old string asserted to occur
  exactly once; every mutant compiled before running; unified diffs in the receipt dir. Counter sha256
  before: `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d` (equal in lane tree and at
  the freeze commit, asserted by the runner).
  - `M1-drop-neg` — removes the NEG block, counter lines 287-289 (NEG regex defined at :97).
  - `M2-drop-paraphrase` — removes the whole paraphrase check: `rc = collapse(rule)` + the <12-words
    reason (:290-292), the `copied` accumulation (:315) and the copied-quote reason (:318-319).
  - `M2a-drop-minwords` / `M2b-drop-copied-quote` — the two halves of M2 separately (supplementary; the
    counter docstring defines paraphrase as both conditions).
  - `M3-accept-base-rows` — drops `i not in base_ids` from the upstream comprehension (:299).
  - `M4-skip-value-compare` — removes the value compare (:280-281).
  - `M5-skip-novelty` — drops `and nov_total == 0` from the predicate (:329); the grep (:212-215) and its
    exit-2 path remain, so this is the smallest edit that skips the novelty conjunct.
- 104 runs: 8 counter variants × 13 controls (9 frozen + 4 supplementary C2X, below). Full data:
  receipt `runs.jsonl`; matrix: `flip-matrix.txt`.

## Flip report — frozen control set (the item's deliverable)

| counter mutant | control flipping FAIL→PASS | reading |
|---|---|---|
| M1 drop NEG | **C2-K2a-x-false-negated** (exit 1→0, rules_verified 0→8) | NEG conjunct **is guarded** |
| M2 drop paraphrase | NONE | **defect: unguarded** |
| M3 accept base rows | NONE | **defect: unguarded** |
| M4 skip value compare | NONE | **defect: unguarded** |
| M5 skip novelty | NONE | **defect: unguarded (structurally)** |

No mutant caused any PASS→FAIL flip or exit-2 (`other_verdict_changes=none` for all seven, receipt
`flip-matrix.txt`); K7-candidate stays PASS under every mutant.

## Diagnoses (why no frozen control flips)

**M2 (paraphrase) — K5 is overdetermined.** K5-scripted-quote-rule sets each rule to the source cell's
first quote + all tokens; it fails on the copied-quote check for all 8 rows, **and** its EX7 rule
additionally carries the negation word `not`, because EX7's only qualifying quote is
`“_("unable to run hook %s: %s\n"), hook->name, _("could not satisfy dependencies"));”`
(corpus/knowledge/pacman-exec-environment-r40.md:27, first curly quote of the EX7 source cell; `not` is a
NEG word, counter :97). Under M2, K5 moves rules_verified 0→7 but stays FAIL on EX7's negation reason
(runs.jsonl `K5-under-M2`: `exit=1 FAIL verified=7 reasons={"EX7": ["rule carries negation word 'not'"]}`).
So K5 guards the conjunction {paraphrase ∧ NEG-on-EX7}, not paraphrase alone. Both halves separately
(M2a, M2b) also flip nothing: K1 fails min-words only jointly with tokens+negation; K5 fails copied-quote
only jointly with EX7's negation.

**M3 (base rows) — K4 fails on used_by, never reaching the base-registry exclusion.** K4's held rows
S208/S216/S217 are in the base registry and pass status/opened/kind/title but fail **only**
`used_by_names_entry` (probe receipt `probe.txt`: S216 `used_by=[corpus/knowledge/pacman-transaction-order-r39.md]`,
S208 names r38/r39/boot-writers entries; row cells from `git show bf2380503b8e4a5d33162026854b0b7b66d18b86:corpus/SOURCES.md`).
Under M3, K4's output is byte-identical to pristine (flip-matrix diff: `C2-K4-held-rows: identical`) — the
exclusion at :299 never fires in any control. EX4's held row (the frozen map sends PKGBUILD→S216,
run_controls.py held dict) also fails both title conditions, and no base row names `packages/pacman`
(`git show 53b294a…:corpus/SOURCES.md | awk -F'|' '$0 ~ /packages\/pacman/' → 0 rows`), so EX4 cannot be
pointed at a qualifying held row at all.

**M4 (value compare) — K2b's tampering is caught by the token check instead.** K2b tampers rule and value
together; with the value compare dropped, EX3/EX4 still fail on tokens (`0022`, `/usr/bin/bash` were
removed from the rules): runs.jsonl `K2b-under-M4`: `exit=1 FAIL verified=6
reasons={"EX3": ["rule lacks tokens: 0022"], "EX4": ["rule lacks tokens: /usr/bin/bash"]}`. No frozen
control tampers the value cell alone (K1/K2a/K5 rewrite the rule, K3/K4 the source cells, K6 duplicates
the block).

**M5 (novelty) — the term is a lane-history constant; the mutant is equivalent.** `novelty_hits` greps the
pinned BASE commit (counter :215, `git grep -F -c -e tok BASE -- corpus SKILL.md PROVINCE.md`); any
repository containing `53b294a…` yields the same hits (content-addressed), and any repository without it
exits 2 before the predicate — so `nov_total == 0` can never discriminate a candidate. Observed:
`novelty_base_hits==0 in every run: True` across all 104 runs, and probe 2 ran the counter's own grep in
the scratch clone: all 8 tokens (counter :95-96) `git-exit=1 hits=(none)` (receipt `probe.txt`). The
mutant is behaviorally identical to the pristine counter on every input it can accept; if the novelty
premise is wanted as a live check it must be evaluated against something a candidate can vary (e.g. the
entry/SOURCES at `<REV>`), or asserted outside the counter predicate.

## Supplementary liveness proofs (C2X controls built in scratch — not part of the frozen set)

Built to show the unguarded conjuncts are live and guardable (all flips are FAIL→PASS with
rules_verified 0→8, receipt `runs.jsonl` / `flip-matrix.txt`):

| supplementary control | design | flips under |
|---|---|---|
| C2X-K1b-tokens-only-rule | rule = the row's frozen tokens only (<12 words) | M2, M2a |
| C2X-K5c-quote-rule-clean | K5 but EX7 quotes a negation-free hook.c:519-526 line added to its source cell | M2, M2b |
| C2X-K2c-value-only | only the value cell tampered (`unknown`), rules intact | M4 |
| C2X-K4b-held-rows-usedby | K4 held rows for EX1-3/5-8 (EX4 kept on S220 — no qualifying held row exists for PKGBUILD), entry appended to S208/S216/S217 `used_by` | M3 |

Each flips under its own conjunct's mutant only. These are demonstrations in scratch, not proposals to
land; the L1 owns any control-set change.

## Not done / out of scope

- No tokens mutant: not in the item's five. Observed (not a run): no frozen control fails solely on
  tokens — K1 fails tokens jointly with negation+min-words, K2b jointly with the value compare — so the
  same operational test would likely find tokens unguarded too; not claimed as a run result.
- The same applies to quote_ok (quote-at-cited-lines), source_ok, counts_ok (no control touches a host
  cell), duplicate checks and the own-work exclusion — not probed.
- C1 counter, census, host capture: untouched (item is C2-only). No lane file created or modified; no
  counter was ever run against the lane tree itself (all runs in the scratch clone).
- No tools installed or upgraded (python3 + git sufficed); no pacman transaction, no sudo, no service
  touched.

## Restoration evidence

- Lane counter sha256 before the work and after scratch removal:
  `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d tools/check-exec-environment-r40.py`
  (`sha256sum` after `rm -rf` of the scratch dir; entry `2230ccaf…` and SOURCES `1676992a…` also
  unchanged; lane tip still `f951f288483c1af0cef4afd458488b84cf7a2165`).
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/C2MutCounter/` removed (its name no longer in
  /fast/scratch/hyaku/tsukuroi-r40/). TMPDIR was pointed at the scratch dir for every run; nothing was
  built under /tmp.

Receipts (all under 2 MB): `.ufo/waves/round-40/w1/C2MutCounter/{mut_counter.py,probe.py,summarize.py,
runs.jsonl,flip-matrix.txt,validation.txt,key-records.json,probe.txt,M1-drop-neg.diff,
M2-drop-paraphrase.diff,M2a-drop-minwords.diff,M2b-drop-copied-quote.diff,M3-accept-base-rows.diff,
M4-skip-value-compare.diff,M5-skip-novelty.diff}`.
