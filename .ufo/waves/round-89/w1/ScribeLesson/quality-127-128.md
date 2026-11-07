# Draft — QUALITY criteria 127 and 128 (seat ScribeLesson)

**Integration status, measured at the tip `665408cc` on 2026-11-06T22:3x.** A criterion numbered **127 is already
written in the working tree** (`corpus/QUALITY.md`, 3 uncommitted inserted lines, `git diff --stat` = `1 file changed,
3 insertions(+)`), class token `R88-CORRECTION-NOT-SWEPT`, requiring the pre-correction and landing `git grep`s with
the exclusion pathspec `':!corpus/lessons/*-verifier-spotcheck.md'`. That text already carries the falsifiable-gradient
requirement my §127 draft below argues for, so **do not add a second 127**: keep the working-tree text, and the only
elements worth folding into it are (a) the pattern is the *defective* token, not the corrected wording, and (b) the
"empty after" leg is over the pathspec-excluded scope, which its own text already states. My §127 below stays as the
record of the reasoning and as the receipt pair the text should cite (`receipts/m1-sweep.txt`, plus the peer receipts
`.ufo/waves/round-89/w1/ExecLints.md` and `.ufo/waves/round-89/after/m1-sweep.txt`). **128 is not written anywhere**
(`corpus/QUALITY.md` ends at 127 in the working tree) and is this draft's live proposal.

Last landed criterion at master: **126** (`corpus/QUALITY.md:306`). The round-89 lesson's disposition table
(`corpus/lessons/round-89.md:15`) already promises "QUALITY 127" for M1's fix; 128 is the M2 draft. Both texts are
written in the file's own style (bold title + parenthesised tag, rule, why, captured-by, `Lesson:` line) so the L1
can paste them.

## 127 — the sweep must be shown able to see the defect

```markdown
127. **A correction carries its sweep in both directions, so the sweep is shown able to see the defect
(R89-SWEEP-UNFALSIFIABLE):** a record that corrects a proposition carries, in the same commit, the sweep QUALITY 108
names, **run twice and printed**: once at the pre-correction revision with at least one hit (`file:line`, non-empty),
and once at the correcting revision with no hit outside the files that keep the superseded text on purpose (each
marked `standing as falsified record` or `historical evidence` per QUALITY 108). The record names the pattern — the
defective token, not the corrected wording — and the scope (paths in, paths out). Extends QUALITY 108: 108 asks which
companions carry the proposition; this asks whether the sweep could see it at all, because a grep that is empty at
the correcting revision is indistinguishable from a grep for the wrong token, and a correction whose sweep was empty
*before* it too has proved nothing. Red: round 89 corrected `corpus/README.md` 977-978 at `81f68d00` (now 976-981)
with no sweep file in the commit, although the defective sentence was non-empty at `dfeaab29:corpus/README.md:978`.
Green: the same two commands at `dfeaab29` (rc 0, one `file:line`) and at the correction (rc 1 over the tracked tree)
— `.ufo/waves/round-89/w1/ScribeLesson/receipts/m1-sweep.txt`. Scoping rule the red case exposes: the token
"`limine-install`'s body" legitimately survives in `corpus/lessons/round-88-verifier-spotcheck.md:129` as the round
record that filed the defect, so the "empty after" leg is over the correcting revision excluding files so marked,
and the record says which.
Lesson: `corpus/lessons/round-89.md` Mistakes `R89-CORRECTION-SWEEP-UNFALSIFIABLE`.
```

## 128 — a battery case always presents the clause it certifies

```markdown
128. **Every case a family generates presents that family's discriminating element (R89-CERTIFY-BY-DRAW):** a
battery family that exists to certify clause C generates cases that each differ from a conforming input in C's own
field; randomness may vary only fields the gate's answer cannot be built from (file names, sizes, blank and
comment shapes, entry order, which pin line comes first), and where C ranges over a finite set — path keys,
resources, hash encodings, line endings — the family enumerates the set inside one case or over the run instead of
drawing from it, or the predicate names the single member it certifies. The predicate states per family whether its
discriminating field is unconditional. **Not QUALITY 126:** 126 governs a control's verdict and the layouts it ran
in, and a drawn variant passes it in every layout; the clause is missing, not the control. **The run count does not
rescue it:** with k cases per run and a 1-in-m draw, one run escapes with (1-1/m)^k, and the three-run predicate
therefore mis-reads a gate that errs for one member with 1-[1-(1-1/m)^k]^3 — 1/16 per run and 17.6 % over three runs
for m=2, k=4, and (2/3)^4 = 19.8 % per run, 48 % over three, for m=3. Red: round 89's first candidate drew
`path =` for `KEY-EQUALS` with p 0.5 and read `61/62` in run 2 (`.ufo/waves/round-89/after/dev/README.txt`); round
88's forger `g16` states the same arithmetic in its own docstring, "(3/4)^4 = 31.6% per run". Green, in the r89
battery: `fam_optional_hash_format` enumerates both optional keys in one case
(`tools/limine-pin-battery-r89.py:565-573`), `fam_all_pin_keys` pins all eight keys every run (`:659-671`),
`WHITESPACE-CRLF` writes CRLF in every case (`:351`), `KEY-EQUALS` writes the touching form in every case
(`:821-829`). A successor that keeps a draw must say in its predicate which member each family certifies; the r89
residual is `:798` (three keys), `:838` (two keys), `:727`/`:735` (two optional keys), `:850` (six forms).
Lesson: `corpus/lessons/round-89.md` Mistakes `R89-CERTIFY-BY-DRAW`.
```

## Why these two and not a third

- 127 is a one-clause extension of 108 with a printed gradient; it does not restate 108's map, and its red case is
  the round's own landed correction, so it is falsifiable against the tree.
- 128 is the only criterion that would have caught the r89 first candidate before the L1 scored it, and the only
  QUALITY entry that speaks to how a family's cases are *generated* (125 maps clauses to families, 126 governs
  control verdicts and layouts, 109 governs host-state rechecks).
- Together they cover both mistakes this round without touching a frozen instrument: M1's fix is a sweep receipt,
  M2's is a generator line.
