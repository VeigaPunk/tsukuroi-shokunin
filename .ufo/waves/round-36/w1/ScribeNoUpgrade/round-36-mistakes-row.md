# Drafted `corpus/lessons/round-36.md` — `## Mistakes` row (routed repair 4)

**Answer to the seat question: yes, this sweep warrants a row.** Reasons:

1. Precedent inside this round: the round-36 lesson skeleton already carries a `## Mistakes` row for
   a routed round-35 spot-check defect — `R36-TARBALL-LEFTOVER`, captured-by "round-35 spot-check
   §6 defect 1" (`.ufo/waves/round-36/w1/ScribeLessonDraft/round-36-lesson-skeleton.md`, `## Mistakes`).
   The NoUpgrade sweep is the same shape: a defect recorded by the outside verifier in
   `corpus/lessons/round-35-verifier-spotcheck.md` §6 item 4 and routed to round 36.
2. Precedent from the previous round: `corpus/lessons/round-35.md` `## Mistakes` carries
   `R34-MUTBINGITALIAS-HOLD` with captured-by "round-34 spot-check §5 item 6" — a routed
   spot-check defect recorded in the next round's Mistakes table.
3. The class is nameable and recurred: a supersession asserted inside one note
   (`corpus/knowledge/pacman-backup-files-r35.md:32` names the four loci) was not carried to the
   files that still state the superseded classification, so a reader of `SKILL.md:397-399` still
   reads `NoUpgrade`/`NoExtract` as version pins. The same class is what the spot-check's quality
   verdict flagged twice (`corpus/lessons/round-35-verifier-spotcheck.md:82` and `:90`).

Placement note: if the L1 prefers a "routed defects" section (the round-35 lesson has both a
`## Routed defects from the round-34 spot-check` section and a `## Mistakes` table), the row below
still fits; only its heading changes.

## Row to append to the `## Mistakes` table

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R36-SUPERSESSION-SWEEP-INCOMPLETE | a classification supersession asserted in one note but not carried to the sites that still state the superseded classification | `corpus/knowledge/pacman-backup-files-r35.md:32` supersedes the grouping of `NoUpgrade`/`NoExtract` with `IgnorePkg` as version pins and names the loci, yet at round-35 closure none of the three named files named the superseding note: `grep -c 'pacman-backup-files-r35\.md'` reads `0` for `SKILL.md`, `0` for `corpus/knowledge/update-safety-note.md`, `0` for `corpus/knowledge/update-safety-v2.md` (`.ufo/waves/round-36/w1/ScribeNoUpgrade/ability-to-fail-before.txt`); the four loci are quoted verbatim there. Recorded at `corpus/lessons/round-35-verifier-spotcheck.md:90` (§6 item 4) | round-35 verifier spot-check §6 item 4 | Four append-only correction blocks land at EOF of the three files (`.ufo/waves/round-36/w1/ScribeNoUpgrade/`, one draft per site), each naming `corpus/knowledge/pacman-backup-files-r35.md` with S191/S195 and giving the replacement sentence. Able to fail: the same sweep must read `1 / 1 / 2` after the landing and any unmarked site keeps its `0`; and the blocks were checked against the real gate functions before landing — `check-recheck-commands.assess_file` counts and findings, `check-knowledge-header.evaluate`, the registered-heading occurrence counts, and the r18 baseline-prefix rule are all unchanged pre/post (`.ufo/waves/round-36/w1/ScribeNoUpgrade/verify-drafts.txt`) |

## Sweep command for the "Fix" column (re-runnable, read-only)

```sh
for f in SKILL.md corpus/knowledge/update-safety-note.md corpus/knowledge/update-safety-v2.md; do
  printf '%s\t%s\n' "$(grep -c 'pacman-backup-files-r35\.md' "$f")" "$f"
done
```

Expected before the landing: `0 0 0`. Expected after: `1 1 2` (the v2 fragment appears in both v2
blocks). A site whose count stays `0` is an unswept locus.

## Adjacent defect this row does not claim

The round-35 note's own sweep sentence lists `update-safety-v2.md:52,193-198`, while the routed
defect and the round-36 declaration list `:52` and `:198`. Both resolve to the same §5 row
(`:198` is inside `193-198`); recorded as a citation-shape difference, not a contradiction.
Residual mentions beyond the routed four are in `residual-mentions.md`.
