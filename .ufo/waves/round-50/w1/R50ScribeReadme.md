VERDICT: draft

Seat R50ScribeReadme — item D-2 (prose): draft the `corpus/README.md` round-50 line. All lane bytes below
were read at the freeze `8029cdba1049df25632c91a23c8db4eefb54be5f` via `git -C …/tsukuroi-shokunin show
<freeze>:<path>`; the cohort snapshot was read from the working tree, never written.

## Evidence read (commands run)

- `git show 8029cdba…:corpus/README.md` → 500 lines; coverage-map table at lines 5-21 (header row :5,
  15 note rows :7-21); `## Frontier` section at :28-43; last block `## Round 49 — GR rows re-read; portable
  ownership pointers` at :482 with `### Frontier notice — round 49` at :492. No round-50 text exists in the
  frozen or working-tree README (`grep -n "Round-50\|Round 50"` on the working-tree file → no hits).
- `git show 8029cdba…:corpus/knowledge/btrfs-scrub-grounding-r45.md` → `## Gate status — round 50
  (pending; the round-50 cohort has not settled)` at :297; the four R49CritGR2b corrections are in the
  bytes (S240 on the `source:` line :1 and named as cited in the round-50 parenthetical; not re-verified here).
- `git diff --name-status <base-b866a1d> <freeze-8029cdba>` (read-only) → round-50 byte changes are
  `M corpus/knowledge/btrfs-scrub-grounding-r45.md`, `M corpus/knowledge/adjacency-anchors-r19.json`,
  `M corpus/SOURCES.md`, `M tools/tsukuroi-census.sh`, `M SCORECARD.md`, and three new counters
  `A tools/check-{scrub-admission,selftest-matcher,adjacency-table}-r50.py`. No new knowledge entry, no
  JSON companion, no coverage-map surface.
- `git show 8029cdba…:PROVINCE.md` → last appended section is `## Round 49 — the ownership-source column
  now cites portable anchors` (:297); storage integrity is Core since `## Round-38 promotion` (:199) and
  the scrub-record view since `## Round-44 promotion — R44-SCRUB-VIEW` (:256). No round-50 section.
- `git show 8029cdba…:.ufo/waves/round-50/frozen/FROZEN.md` → frozen rule: "A bound-format negative
  (`partly`/`fails`) on the current hash blocks the row whatever its citations".

## Cohort snapshot (working tree, read-only, 2026-10-28T19:16:14Z)

Receipt: `.ufo/waves/round-50/w1/R50ScribeReadme/cohort-snapshot.txt`. All 18 expected GR reports exist as
files (`ls .ufo/waves/round-50/w1/R50{Rev,Crit}GR*.md` → 18); every `SECTION SHA256:` equals the frozen row
hash. Line-1 verdicts: holds 7, **partly 11** — GR1: 1/6 partly (R50RevGR1b); GR2: 4/6 (R50RevGR2c,
R50CritGR2a/b/c); GR3: 6/6 (R50RevGR3a/b/c, R50CritGR3a/b/c). Every row has at least one bound `partly` on
the current hash, so under the frozen rule `verdicts_ok == 3` cannot hold on these reports. `w1-results.json`
does not yet exist in the working tree (`ls` → no such file), so whether every report binds as a completed
seat is the counter's question, not this seat's. Named defects (verbatim, for the canonical judge):
- R50RevGR1b (GR1): "Quote exactness at cmdline.c:147 — one of the row's twelve Quote lines is a
  line-slice, not the cited line's text."
- R50CritGR2b (GR2): "False provenance in the row body (entry.md:76): 'by SR7,
  `btrfs_dev_replace_cancel` stops it with `btrfs_scrub_cancel`'", plus an undeclared S242 coverage gap
  and a `-ENOTCONN` wording defect.
- R50CritGR3a (GR3): "two S237 citations fall outside the registered ranges and are undeclared"
  (`scrub.c:439` and `:1546`; the S237 gap sentence names only `:421`).

## Deliverable — the round-50 block

Placement: append at the end of `corpus/README.md` (after frozen line 500, the round-49 Frontier notice),
matching the "## Round-NN coverage note (appended <date>)" convention of the round-44 (:427), round-45
(:454) and round-46 (:468) blocks. Because the observed cohort binds `partly`, the honest text is the
**pending variant** below; the item's requested "admitted round 50" sentence is supplied as a conditional
variant valid only if `tools/check-scrub-admission-r50.py` scores `verdicts_ok == 3` at the integrated
revision (i.e., a cohort that settles `holds` on the row bytes then current).

### Variant P — matches the observed cohort (pending; recommended)

```markdown
## Round-50 coverage note (appended 2026-10-28)

Append-only; the coverage map, the Frontier bullets and the notes above stay as written. The round adds no
coverage-map row and no new surface: its three claims move held surfaces (the round-45 scrub-grounding
entry, the census selftest harness, the ADJ anchor table), so nothing is inserted in the table above.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/btrfs-scrub-grounding-r45.md` (round-50 read) | The four defects the round-49 counted critic `R49CritGR2b` named are corrected in the bytes before the freeze (the `[inference]` mark narrowed to btrfs-progs printing, S240 in the `source:` line and QUALITY item 7, the `dev-replace.c:1128` quote exact, the S247/S240 range gaps declared in Limits); the round-50 counted cohort of one wave (`w1`, 18 seats) did not settle the rows — 11 of 18 bound `partly` on the frozen hashes (GR1 1/6, GR2 4/6, GR3 6/6) — so GR1-GR3 stay **pending** (`## Gate status — round 50 (pending…)` in the entry) and are not admitted round 50; counter `tools/check-scrub-admission-r50.py` | S237-S249 (re-opened by round-50 seats 2026-10-28); `.ufo/waves/round-50/frozen/FROZEN.md`; `.ufo/waves/round-50/w1/` |
```

### Variant A — only if the C1 counter measures PASS at the integrated revision

Replace the row cell with:

```markdown
| `knowledge/btrfs-scrub-grounding-r45.md` (round-50 read) | The four defects the round-49 counted critic `R49CritGR2b` named are corrected in the bytes before the freeze (the `[inference]` mark narrowed to btrfs-progs printing, S240 in the `source:` line and QUALITY item 7, the `dev-replace.c:1128` quote exact, the S247/S240 range gaps declared in Limits), and a fresh counted cohort of one wave (`w1`, 18 seats: three reviewers and three critics per row) read GR1-GR3 `holds` on those bytes, so **GR1-GR3 are admitted round 50**; the frozen predicate, row hashes and seat-binding format are in `.ufo/waves/round-50/frozen/FROZEN.md`, counter `tools/check-scrub-admission-r50.py` | S237-S249 (re-opened by round-50 seats 2026-10-28); `.ufo/waves/round-50/w1/` |
```

The single sentence the item asked for, verbatim: "The four defects the round-49 counted critic
`R49CritGR2b` named are corrected in the bytes before the freeze, and a fresh counted cohort of one wave
(`w1`, 18 seats) read GR1-GR3 `holds` on those bytes, so **GR1-GR3 in `btrfs-scrub-grounding-r45.md` are
admitted round 50**." — write it only on a PASS; on the observed bytes it is not earned.

## Coverage-map table row

None — the round adds no surface. The base→freeze diff adds three counters and edits existing bytes only;
no new `corpus/knowledge/` file and no `## Round-50 … promotion` section exists in `PROVINCE.md` at the
freeze. The drafted block says so in its lead paragraph rather than by a table edit.

## Frontier — did any row advance this round? (one line)

No: no entry moved Frontier → Core — `PROVINCE.md` at the freeze carries no round-50 promotion section
(its last appended section is `## Round 49`, :297) — and no bullet in this README's `## Frontier`
(:28-43) is rewritten; round 50 deepens ground already promoted in rounds 38 and 44.

## Why the entry is depth work on an existing Core surface (one line)

Storage integrity has been Core since the round-38 promotion (`PROVINCE.md:199`) and the unprivileged
scrub-record view since the round-44 promotion (`PROVINCE.md:256`), and `btrfs-scrub-grounding-r45.md` is
already on this map from round 45 (`corpus/README.md:460`); round 50 changes four sentences inside that
existing entry and re-reads its three rows — the base→freeze diff adds no knowledge file — so the axis it
moves is depth, not coverage.

## Not done / limits

- I did not run `tools/check-scrub-admission-r50.py` (not a command named by this item; EXEC-AUTHORIZED).
  The C1 verdict is measured by the frozen counter against the integrated revision, not by my file-count
  of report headers — the partly tally above is a read-only snapshot, and a report could still be replaced
  by a completed seat before the counter runs.
- I did not draft the block's C2 (census selftest matcher) or C3 (ADJ anchors) rows; the item scopes this
  seat to the GR sentence and the coverage-map question. The block skeleton leaves the table open for
  those rows from their own scribes.
- Lane README/PROVINCE were never written by this seat; the draft above is prose for the L1 to place.
- Tooling: nothing installed or upgraded (no need arose); read-only `git show`/`diff`/`ls`/`sed`/`grep`
  only. Receipt dir `.ufo/waves/round-50/w1/R50ScribeReadme/` holds `cohort-snapshot.txt` (~2 KB).
- Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ScribeReadme/` (frozen README/PROVINCE/GR extracts) removed
  on finish.
