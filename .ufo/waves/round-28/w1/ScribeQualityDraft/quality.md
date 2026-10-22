# Draft QUALITY.md edits — round 28 wave 1, seat ScribeQualityDraft

Both edits target `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md` at
`f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0`. This file is a draft; nothing here is committed.

## Edit (a) — criterion 69 names its lesson id (routed defect 7)

The id `R27-SIBLING-POINTER-DRIFT` exists at `corpus/lessons/round-27.md:92` (Mistakes table row,
verified). Routing: `corpus/lessons/round-27-verifier-spotcheck.md:105` item 7.

Replace `corpus/QUALITY.md:137` (the whole line) with:

```text
69. **A sibling pointer is replayed by quote and pinned blob before it is cited as an overlap or an acknowledgement (R27-SIBLING-POINTER-DRIFT):** a register row names the sibling commit, the blob digest of a committed snapshot, the nearest heading and a quote of at most 25 words, and the lane side by quote at the measured revision; a sibling citing this lane is recorded as a resolved or drifted inbound pointer, never as recipient acknowledgement. Failing example: mori's `PROVINCE.md:66` pointer to lane `PROVINCE.md:21-24,35-44` drifted to lines 30-33 and 44-53 without either lane recording it (register row OV2). Lesson: `corpus/lessons/round-27.md`.
```

Only the heading parenthetical changes: `(C2, round 27)` → `(R27-SIBLING-POINTER-DRIFT)`. The rule
text, failing example and `Lesson:` pointer are byte-identical to the current line, so the link is
greppable both ways (`R27-SIBLING-POINTER-DRIFT` now appears in both the criterion and the lesson row).

## Edit (b) — new criterion 73 (round 28)

Append immediately after criterion 72 (the last line of the file, contiguous with 67–72, no blank
line), same one-paragraph shape:

```text
73. **A counter's evidence is a committed should-fail battery whose count is the claim's measure (R28-BATTERY-MEASURE):** before a counter's count stands as a claim's evidence, the same commit that offers the count also commits the battery that runs the counter against should-fail mutants it must refuse and a live control it must accept; the declaration's counting command is that battery and its declared measure is the battery's last-line field (`should_fail_accepted` with its control field), never the bare counter's own count. A bare-counter count, a selftest-only run or a run of uncommitted counter bytes is development output — disclosed as such, never offered as the measured value; a counter whose battery accepts any should-fail mutant reports a count of anchors or links, not the claim's measure (QUALITY 72). Failing examples: the round-27 adjacency counter at `dd94cb1f` was offered as the C2 claim's measure with no committed battery and accepts 19 of 24 should-fail register shapes (`corpus/lessons/round-27-verifier-spotcheck.md:100`), and the round-27 kernel-taint counter at `75f410c8` likewise accepted the CritC1Tool mutants (`corpus/lessons/round-27.md:91`). Lesson: `corpus/lessons/round-28.md`.
```

Notes for the integrator:

- `R28-BATTERY-MEASURE` is a minted id: no `R28-` token exists anywhere yet (`grep -rn "R28-" corpus/
  SCORECARD.md LOG.md` empty at `f8e3a8f`). The round-28 lesson's Mistakes row must use this exact
  token, per the same greppable-both-ways rationale as routed defect 7.
- `corpus/lessons/round-28.md` does not exist at `f8e3a8f`; the round-28 declaration
  (`SCORECARD.md:1067`) requires its Gate to record at least one reject or defer decision, so the
  file lands this round. The `Lesson:` pointer is forward-looking but matches the declared plan.
- Contrast case behind the rule, already in the declaration: the 18:56Z run of the *uncommitted* C1
  counter (`SCORECARD.md:1065`) was disclosed as development output and is re-measured at the round's
  commits — that is the behavior the second sentence prescribes, kept here as context rather than as
  a failing example since it was handled correctly.
