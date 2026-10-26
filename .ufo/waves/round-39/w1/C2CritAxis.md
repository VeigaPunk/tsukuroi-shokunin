VERDICT: falsifies

# C2CritAxis — item C2-17: C2 attacked as a depth claim

Lane read-only at tip `394e1ba4fab39a417abe66a7802f87cf1ff8dd61`; counter `tools/check-transaction-order-r39.py`
sha256 `f1c97836…` (the frozen one). Every control below was scored in a scratch clone
(`git clone -q --shared …; remote remove origin`, toplevel verified) based on `2e1c2a4` (author-after-receipts);
only `corpus/knowledge/pacman-transaction-order-r39.md` was rewritten, `corpus/SOURCES.md` untouched. No lane
file, index, jj state or host state was touched. Scratch removed; receipts kept in
`.ufo/waves/round-39/w1/C2CritAxis/`.

**What is falsified.** Not the entry's content (all eight rules hold — see the per-row lines at the end), but the
proposition that the frozen C2 target demonstrates a *depth* move: the target is met 8/8 by a control that writes
no transaction order at all. Per the frozen claim-sizing rule (`.ufo/prompts/tsukuroi-round-39.md:448-452`,
"build the cheapest control that skips the claimed work … if it meets the target, the counter or target is wrong")
that is a defective target, and per `:457-461` ("Re-scoring a rule the lane already holds … is quality work, never
coverage or depth") TO1 is a re-score the predicate cannot see.

## A. The frozen target is reached by an entry that states no order

| control | revision | rules_verified | result | contents |
|---|---|---|---|---|
| C2-X-empty | `46222c3196b9c45116a76855cce88643924abf9f` | 8 | **PASS** exit 0 | every rule cell `RULE NOT SUPPLIED — this control states no transaction order`; every source cell `<S-id> <file>:1-30 “Copyright (c) 20xx-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>”`; host cells only `control host cell, no host evidence` plus `60 transactions` / `252 of 441`; the `## Order of one transaction` and `## Boundaries` prose deleted, so no rule statement survives anywhere in the file (only the intro's topic list and the QUALITY prose, neither read by the counter) |
| C2-X-sourceless | `1e75d0183a54937c91863a5fdf265c6536abbf8b` | 8 | PASS exit 0 | same, with the prose sections still present |
| C2-X-false | `6048c233d70876cb37bac4cbcf7d0376da414703` | 8 | PASS exit 0 | all eight rule cells replaced by the **opposite** of the source (TO1: "PostTransaction hooks run **before** `transaction started` …"); source and host cells byte-identical to the candidate |
| C2-X-ho | `3a3169aa1edeaa7e3e793c9db8cdc3b989cc087f` | 8 | PASS exit 0 | all eight rule cells replaced by round-38 HO1–HO7 text (HO7 twice) — the held ground, with C2's citations |
| C2-candidate | `2e1c2a4` / `394e1ba` | 8 | PASS exit 0 | unchanged entry |

Receipts: `.ufo/waves/round-39/w1/C2CritAxis/controls.jsonl` (sha256 `d55756f5…`), fixtures
`X-empty.entry.md` `c8e42738…`, `X-sourceless.entry.md` `46b0cc0e…`, `X-false.entry.md` `fc5d3e19…`,
`X-ho.entry.md` `d684a375…`; generators `x3.py` `93ee1ea5…`, `mutate.py` `e3dd7331…`.

Why: the counter reads only `cells[2]` (source) and `cells[3]` (host) — `tools/check-transaction-order-r39.py:199`;
its row test is the S-id row, the per-TO required file, and that any 4–25-word curly quote occurs inside lines A..B
(`:200-221`). The rule cell `cells[1]` is never read, and the predicate (`:227-228`) therefore cannot distinguish an
order from a placeholder. X-empty is the "cheapest control that skips the claimed work": to build it one needs only
the file names and S-ids already printed in the declaration, a header comment from lines 1–30 of each file, and the
two numbers the counter prints itself.

## B. The committed control set never tests rule text

`.ufo/waves/round-39/controls/c2-entries/` diffed against the candidate: E1 rewrites the `source:` line and every
row's source cell to the own-work row S218 (rule cells verbatim), E2 shifts the `file:line` refs, E3 drops S213 from
`source:`, E4 duplicates the rules block, E5 rewrites the two host cells. Every fixture keeps the candidate's rule
cells, so the shape in A was never scored before data. The round's do-nothing control is
`C2-K0-do-nothing` at `6a08925` — 0/8 FAIL (`controls.jsonl:6`) — which shows only that an absent entry scores
zero, not that a citation-shaped entry must carry the order.

## C. `counts_ok` is circular

The counter computes and prints `host` before it reads the entry (`:167-170`). I ran it at the base `6a08925`
where the entry does not exist: output `rules_verified 0`, `host {"windows": 86, "transactions_started": 60,
"scriptlet_tag_outside_commit": 252, "scriptlet_tag_total": 441, "running_inside_commit": 0}`. `counts_ok` then
only asks the entry to contain `60 transactions` (TO1) and `252 of 441` (TO8) — exactly the printed strings
(`:223-226`). A control that runs the counter once and copies its output satisfies both conjuncts without reading
`frozen/txcapture/`; X-empty did precisely that.

## D. The re-scoring leg is real but narrower than eight

- **TO1** (`corpus/knowledge/pacman-transaction-order-r39.md:24`) restates **HO5**
  (`corpus/knowledge/pacman-hook-order-r38.md:25`: Pre failure returns before the transaction starts, `trans.c:201-204`)
  and **HO6** (`:26`: Post hooks only after `transaction completed`, `trans.c:212-240`) on the **same bytes**: S217
  (`corpus/SOURCES.md:226`) has sha256 `637c1165…`, identical to S210 (`:219`), and exists only because the round-38
  closure routed an anchor-symbol fix (`corpus/lessons/round-38-verifier-spotcheck.md:32-34`, `:181`). S217's first
  range `201-204` is exactly HO5's. TO1's only added proposition is where the two log lines sit.
- **S213 add.c** (`SOURCES.md:222`) is byte-identical to **S191 add.c** (`:197`), both `fd313629…`; **S215 remove.c**
  (`:224`) is byte-identical to **S192 remove.c** (`:198`), both `a052d455…`; **S217 trans.c** is byte-identical to
  **S210** (above), and **S208 hook.c** is round-38's own row. So three of the five code rows in S213–S217 re-open
  mined bytes; only S214 (`sync.c`) and S216 (`util.c`) open files the lane had never mined.
- So the depth delta is seven new rule propositions (TO2–TO8), two of them on new files; TO1 is held ground plus a
  log-line placement. That is a real increment — but the predicate cannot show it: X-ho passes 8/8 with the held
  rules, and a *true* re-score of HO5+HO6 with these trans.c quotes would also survive the kill rule
  (`SCORECARD.md:2221`, "any TO row judged false against the pinned source at its cited lines"), because the rule
  text is true and the cited quote supports it.

## Impacted axes

- **depth (C2):** the axis move is not demonstrated by the frozen artifacts; the target is reachable without the
  claimed work and cannot separate new depth from held truth. This is the axis I falsify.
- **quality / sourcing:** unaffected — the entry cites mined rows, the digests pin, and the rules are true.
- operability, freshness, calibration, adjacency: untouched by this finding.

## Strongest argument against admission

The frozen C2 target is `rules_verified == 8 and duplicate_rows == 0 and duplicate_headings == 0 and source_ok == 1
and counts_ok == 2 and oracle_violations == 0` (`SCORECARD.md:2221`), and revision `46222c31` meets it 8/8 while
containing no statement about transaction order: eight placeholder rule cells, eight copyright-header quotes from
lines 1–30 of the required files, and two host cells copied from the counter's own output. `6048c233` (all rules
reversed) and `3a3169aa` (the held HO rules) also pass 8/8. The frozen rule is explicit that a target meeting the
cheapest work-skipping control is a wrong target (`prompt:448-452`); C2's committed controls (E1–E5) score only
citation edits, so the obligation was not met before data, and the declaration's kill rule cannot repair it: it only
rejects *false* rules, while TO1 is a *true* re-score of HO5+HO6 on duplicate bytes (`S217 = S210`) that the kill
rule must accept. On the round's own artifacts, C2 is a sourced-entry claim, not a measured depth move.

## Smallest safe correction

The predicate may not be changed after data (`prompt:453-455`), so do **not** edit the counter or the target this
round. The safe disposition is:

1. Keep C2's frozen PASS as a sourced-entry claim; record the four controls above (with revisions) in the round-39
   lessons line, e.g.:

   > C2 predicate scope: `rules_verified` tests citation shape, not rule text. Controls X-empty (`46222c31`),
   > X-false (`6048c233`), X-ho (`3a3169aa`) meet the frozen target 8/8; the frozen controls (E1–E5) do not cover
   > this class. C2 is admitted as sourced knowledge; its depth attribution is withheld.

2. Do not score the depth ordinal as moved for C2; depth stays at its declared value (8) and the axis attribution
   waits for a predicate that binds the rule column.
3. Round 40 freezes that predicate *before* data with the two conjuncts the control needs — `rule_cells_present == 8`
   (each TO rule cell must contain a declarative order statement, not a placeholder) and `held_rule_hits == 0` (no
   TO rule cell equal, after whitespace/backtick normalisation, to any HO rule cell of
   `corpus/knowledge/pacman-hook-order-r38.md`) — and commits X-empty as a required-FAIL control. If the author
   wants depth on this surface sooner, the honest alternative is a different target: a host-oracle rule (each TO
   rule that predicts the log is checked against `frozen/txcapture/`), which X-empty could not meet.

## Per-row verdicts (declared kill rule, QUALITY 81)

TO1: holds — trans.c:201-208, 232-239
TO2: holds — sync.c:1341-1354
TO3: holds — add.c:467-474, 560, 599, 618-631, 638-647
TO4: holds — add.c:470-474; trans.c:400-406
TO5: holds — hook.c:532-560 (opendir :554)
TO6: holds — add.c:677-692
TO7: holds — remove.c:698-733
TO8: holds — util.c:521-528; hook.c:525-528; util.c:820

Notes on the judged rows (none false, so the kill rule does not fire):
- TO3's rule is true but two of its four steps (extraction `add.c:560`, local DB write `:599`) lie outside the cited
  `616-648`; the counter accepts the comment quote and never checks the uncited steps.
- TO4's argv order is built at `trans.c:400-406` (`. %s; %s %s %s`), not at the cited `add.c:470-474`; the call's
  argument order at the cited lines is the only cited support. True, citation partial.
- TO6's rule holds at `add.c:677-692`, but its host cell ("An interrupted transaction logs `transaction interrupted`")
  is exact only for the state-check path: a package failure sets `STATE_INTERRUPTED` (`add.c:679`) yet
  `trans.c:221-227` (sync branch; `:213-219` on the remove branch) logs `transaction failed` and returns before the
  `STATE_INTERRUPTED` check at `trans.c:230`. The
  entry's step 7 (`:41`) states both branches, so the table cell is incomplete rather than false.
- TO5's host column is self-declared consistency, not proof (`:48-50`); I did not re-derive its 17-hook claim.

## What I did not do

- No live host read, no pacman run, no capture re-verification beyond the counter's own MANIFEST check.
- No `--branch`/origin variants; bindings were local-branch only.
- No tools installed or upgraded (none needed).
- Scratch `/fast/scratch/hyaku/tsukuroi-r39/C2CritAxis/` removed after copying receipts into the seat dir.
