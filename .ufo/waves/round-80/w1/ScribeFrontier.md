# Seat ScribeFrontier — binding report (round 80, wave w1)

Execution class: **NO-EXEC** (read-only drafting; no claim tool run, no
network fetch, no host domain command, no git/jj mutation, no production
edit).

Status: **COMPLETE** — artifacts written and finalized; binding file written
first, deepened at the end.

Base `467a9b7891a5939dab8460ec6f591fbb16bd82e9`; frozen commit
`61ec89ec6e6f284b6fba2127721359e6931a5789` ("round-80: freeze restart matrix
and two gate-standard predicates"). Axes judged: **depth** and **operability**.

## What this seat serves

The **frontier step** of round 80: the source row and the `## Gate` block the
L1 integrates into `corpus/lessons/round-80.md`, plus the lesson draft that
carries the round's mined mistakes, the seat-harm tally and the QUALITY check.
This seat writes no registry row, no corpus file and no tool; it writes only
its own report and its own `ScribeFrontier/` directory.

## Artifacts

All under
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-80/w1/ScribeFrontier/`:

- `source-row.txt` — the drafted **S330** registry row (one row, 11 cells) with
  per-cell provenance and the three landing consequences the L1 must know.
- `gate-block.md` — the `## Gate` block draft: URL, access date `2026-11-04`,
  a located ≤25-word quote for S330, one admit and four rejects each with a
  reason and a flip condition, plus the preserved rejected history and the
  notes the L1 must carry.
- `lesson.md` — the lesson draft with `## Gate`, `## Mistakes`, `## Seat harm`
  and `## QUALITY check`.
- `derivation.md` — the read-only derivation receipts behind every number in
  the three artifacts above (digests, the independent 42-cell re-derivation,
  the per-cell line map, the located-quote table with occurrence counts, and
  the registry facts).

Binding report: `.ufo/waves/round-80/w1/ScribeFrontier.md` (this file).

## Behaviour of the drafted S330 row

- **Id**: `S330` — the next unused id in the committed registry (329 rows,
  `S001`–`S329` contiguous), and also the id the frozen instrument forces
  (`tools/measure-round80.py:35` greps literally for a line starting
  `| S330 |`).
- **Kind/tier/status**: `docs` / `A` / `mined` — the upstream v262 manual is
  the primary source for the `Restart=` directive semantics, the same tier-A
  `docs` treatment `S329` gives the sibling `systemd.unit.xml` page.
- **Scope**: exactly the `Restart=` settings-to-exit-cause table and the
  conditions that qualify it. Not `S329`'s dependency keywords, not `S070`'s
  `ExecStopPost=` scope, not any host unit's behaviour.
- **Used-by**: both planned companions — `corpus/knowledge/service-restart-matrix-r80.md`
  and `corpus/knowledge/service-restart-matrix-r80.json`.
- **Shape check against the frozen counter's own parser** (run read-only on
  the draft text): exactly one `| S330 |` line, 13 `|`-split fields,
  `row[3]='docs'`, `row[4]='A'`, `row[8]='mined'`, the expected URL inside the
  source cell, and `corpus/knowledge/service-restart-matrix-r80.json` inside
  the used-by cell — all satisfied.
- **Census expectations derived from the rule code** (no census was run):
  no `W04`/`E04` duplicate-URL finding, because `url_of()` takes the first URL
  in the source cell and no existing row's first URL is that string; but
  `E11` fires unless both used-by paths exist at census time and `E12` fires
  if the row lands outside the `## Registry` section.

## Independent verification this seat performed (read-only, no tool run)

- Re-derived the 42 matrix cells **structurally** from the pinned XML table
  (parsing `<row>`/`<entry>` elements, not copying the answer key): the
  derived `settings` list and `rows` array are deep-equal to
  `before/expected.json`; 42 cells, 18 marked, 24 empty.
- Confirmed the snapshot digest `12770f86…f66d44` and the expected-object
  digest `05abbf14…65153` against the frozen files and the scorecard.
- Located every quoted span with the round-79 locator rule (tag-stripped,
  whitespace-normalised token stream) and counted its occurrences over the
  whole 1977-line file — every cited span occurs exactly once.
- Measured the **prose-order vs table-header-order divergence** at
  `:885-886` vs `:920-929`: the same seven settings are listed in two
  different orders, and the frozen object follows the table. A re-derivation
  from the prose sentence would transpose six of seven columns.
- Measured the **per-cell line map** for all six rows and independently
  reproduced ReviewMatrix's finding that the `on-abnormal` and `on-abort`
  columns differ in **three** rows (`:968`/`:969`, `:978`/`:979`, `:988`/`:989`),
  not one — and that the OOM row's marked set equals the `Timeout` row's, not
  `Unclean exit code`'s.

## Mistakes mined in the lesson draft

Six rows, each with an evidence anchor a reader can re-run:

1. **R79-C1-EQUALITY-SHADOWS-DEEP-LEGS** (my r79 unreachable output leg) —
   r79's frozen equality leg made `quote-location`/`row-shape` unreachable for
   data-side perturbations; round 80 repeats the shape at
   `tools/measure-round80.py:41-46`, and `before/controls.json` shows the two
   kills are mutually exclusive (`wrong-restart-cell` → `matrix-mismatch`,
   `forged-review` → `review-binding`), so no single control exercises both.
2. **R80-C1-NO-SOURCE-LEG** (the r79 DP6 shape, re-measured) — no counter leg
   compares the matrix to the pinned XML; the conditions that qualify the
   table live only in the companion, so a reader of the JSON alone reads
   "always restarts on all six causes" without the exceptions. Declared
   exposure, mitigated by the companion and the `teaches` cell, not closed.
3. **R80-TABLE-HEADER-VS-PROSE-ORDER** — the same page states the same seven
   settings in two orders; the frozen object follows the table.
4. **R80-C1-ARTIFACT-EQUALS-ANSWER-KEY** — the reviewed artifact is
   byte-identical to the frozen answer key, so source entailment has exactly
   one entrance (the pinned XML) and a fabricated review bundle passes.
5. **R80-COMPANION-COLUMN-DIVERGENCE** — independently reproduced the
   companion's false "exactly one place" count; a *count* of divergences is a
   claim about the whole matrix, so the sweep must enumerate all six rows.
6. **R80-S330-USED-BY-E11** and **R80-C2-STATIC-RECEIPT-NO-RERUN** — the
   landing-order constraint on the row, and the inherited fact that C2 is a
   receipt-binding gate that never re-executes the tool.

## Seat harm recorded

The `## Seat harm` table in the lesson draft carries one empty verdict (no
destructive seat-to-seat incident observed in any round-80 w1 seat report read
by this seat; the wave settlement is marked **PENDING** because
`w1-results.json` does not exist yet), one **latent risk** row for the
companion digest-lock coupling, and two **resolved** review-driven
interactions (ReviewMatrix's KR isolation finding → ExecKR's amendment →
re-review; and the companion's false column-divergence count → ScribeMatrix's
correction → re-review), both with the preserving artefact named.

## Honest limits of this seat's evidence

- **No claim tool was run.** `tools/measure-round80.py` was read (its SHA-256
  matches the frozen value) but never executed by this seat; `before/controls.json`
  was read, not re-run; no census was run; no gate was executed. Every
  statement about the counter's and the census's behaviour is derived from
  reading their own source code and the frozen artefacts.
- **The drafted row is not landed.** `S330` is absent from
  `corpus/SOURCES.md` at the time of this report, and the two companions are
  still in the wave tree, so the C1 count is 0. This seat did not land them
  and did not claim otherwise.
- **The `teaches` cell is a summary of located sentences**, not a claim that
  these are the only relevant sentences in a 1977-line file.
- **The four rejections are refutations of claims about documentation
  semantics.** They say nothing about any host's unit files and are not
  allegations against any seat.
- **This seat's independent re-derivation is corroboration from a scribe, not
  the non-author verdict.** ReviewMatrix's verdict is the verdict; this seat
  issues none and claims no promotion authority.

## Deviations and hygiene

- Execution class: **NO-EXEC**. Commands actually run, all read-only, none
  mutating: `mkdir -p` of this seat's own directory and scratch; `ls`,
  `read`, `grep`, `sed -n`, `head`/`tail`, `wc`, `stat`-free listing, `git
  rev-parse`/`cat-file`/`log`/`status`/`show` (read-only), `sha256sum` on the
  pinned snapshot and the frozen expected object, `python3` heredocs that
  *parse committed/pinned bytes and print results* (no writes, no bytecode
  written — `sys.dont_writebytecode` was not needed because no project module
  was imported; only `re`/`json`/`hashlib` from the stdlib), and one
  `python3` invocation that read the `w1-dispatch.json`/`w1-spec.json` JSON.
  No tool was installed or upgraded; nothing was written to `~/.local/bin` or
  any PATH directory; no pacman transaction was attempted; no sudo was used;
  no host service was touched; no secret or config file was read.
- No git or jj mutation of any kind: no commit, push, stage, stash, checkout
  or reset, in the lane, the fleet root or any sibling. No fixture repository
  was created. The only paths written were this seat's directory and this
  seat's binding report — the paths the seat spec names. No fleet-root
  tracked file (`LOG.md`, `SCORECARD.md`, `MANIFEST.json`, …) was touched,
  and no sibling seat's directory was written.
- Scratch: `/fast/scratch/hyaku/tsukuroi-r80/ScribeFrontier/` was created and
  is **deleted** before yield; it held no durable artefact, because every
  receipt this seat produced was written into this seat's own directory
  (`derivation.md`).
- Model: no model parameter was passed.

Scope: executed=none
