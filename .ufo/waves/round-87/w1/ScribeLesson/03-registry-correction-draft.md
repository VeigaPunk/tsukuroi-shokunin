# Draft — appended `SKILL.md` correction for the `resume-gate-battery-r86` row

Seat: ScribeLesson (scribe, leaf). Draft only; the L1 lands. Read, not re-run:
`.ufo/waves/round-86/before/controls/controls-summary.txt` and `controls-receipt.txt` (both committed at
`2f67de80`), `.ufo/waves/round-86/w1/CriticClaims.md:98,115-116`, `corpus/lessons/round-86-verifier-spotcheck.md:26,125-126`
and the row at `SKILL.md:5920`. Receipts: `ScribeLesson/receipts/r04`.

## The superseded sentence (quoted so the correction names it)

`SKILL.md:5920`, `Pinned values` cell, as written:

```text
controls in `.ufo/waves/round-86/before/controls/` (K1 r85 gate 26/30; near-miss N01-N12 26-29/30, each failing
exactly its property family; r85-carried forgers, mutants and controls 0-25/30); `--selftest` PASS 4/4
```

The range `26-29/30` is right. `each failing exactly its property family` is not: ten of the twelve fail exactly
one family, N11 fails two and N12 four.

## Text to append (after the registry table's existing correction blocks; append-only)

```text
## Round-87 correction — R87-REG-1: the `resume-gate-battery-r86` near-miss cell

Append-only; the `resume-gate-battery-r86` row above stays as written. Its `Pinned values` cell says the
near-miss controls N01-N12 read "26-29/30, each failing exactly its property family". The range holds; the
universal does not: ten of the twelve fail exactly one family, N11 fails two and N12 four. From
`.ufo/waves/round-86/before/controls/controls-summary.txt` (committed at `2f67de80`; families_passed of 30, three
runs each, the failed-family set identical across runs):

N01-noresume-exact: 29 29 29  NORESUME-VALUED
N02-nohib-exact: 29 29 29  NOHIB-VALUED
N03-empty-resume: 29 29 29  EMPTY-RESUME
N04-first-offset: 29 29 29  OFFSET-DUP
N05-offset-malformed: 29 29 29  OFFSET-SSCANF
N06-no-dash: 29 29 29  OFFSET-SSCANF
N07-hib-literal: 29 29 29  HIBERNATE-NOX
N08-boundary-le: 29 29 29  SWAP-BOUNDARY
N09-first-swap: 29 29 29  MULTI-SWAP
N10-no-bool-guard: 29 29 29  BOOL-FOR-INT
N11-substring: 28 28 28  DECOYS-R86,PREC-DECOYS
N12-short-prefix: 26 26 26  DECOYS-R86,EMPTY-RESUME,HR-NO-RESUME-ARG,PREC-NO-RESUME-ARG

N11 fails 2 families (`DECOYS-R86, PREC-DECOYS`) and N12 fails 4 (`DECOYS-R86, EMPTY-RESUME,
HR-NO-RESUME-ARG, PREC-NO-RESUME-ARG`); N01-N10 each fail the one family their removed property serves. The
disclosure existed only in prose — `controls-receipt.txt:9-10` ("N11 also PREC-DECOYS; N12 also the
resume=-dependent families") and `CriticClaims.md` §4 table (`:115-116`) — not in this row, the round-86 report
or `SCORECARD.md`. The row's other clauses stand: K1 r85 gate `26 26 26` of 30; the r85-carried forgers,
mutants and controls `0-25/30`; `--selftest` PASS 4/4. Found by the non-author closure
(`corpus/lessons/round-86-verifier-spotcheck.md` §5 routed 3; row at `:26`), repaired at round 87 by this
append; no row text is edited. QUALITY 122 is why the sets matter: a near-miss control that fails a family its
removed property does not serve is weaker evidence than the row claims.
```

## Form notes for the L1

- The block is a **new level-2 section**, matching the `## Round-81 correction — R81-REG-1` form already in
  `SKILL.md` (table lines at `:5925-5934`). It is not an edit to the registry table and not a `|` row, so the
  table's column count and the `check-registry-coverage.py` row parser are untouched (QUALITY 99, append-only).
- `R87-REG-1` is a section id local to this correction. The defect it repairs is round-86 routed defect 3
  (`corpus/lessons/round-86-verifier-spotcheck.md` §5.3), which the r86 lesson's `## Inputs read` table already
  books as an owed repair; it is not carried as a round-87 `## Mistakes` row (the draft's third-candidate note
  explains why: one defect, one record, and the row text cannot be edited).
- Class id, if the lesson text wants one: `R87-REGISTRY-SET-OVERGENERAL`. Nothing in this draft depends on the
  spelling; the correction's content is the set list.
- If the r86 battery is ever retired, this correction stays valid: it describes committed bytes at `2f67de80`,
  not a live tool.
