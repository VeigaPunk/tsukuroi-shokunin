VERDICT: defect-found

Seat R49Simplify (P-5 simplifier pass), leaf, no dispatch. Read-only on lane bytes.
All line numbers below are **the FREEZE revision** `55c07cd` (`git -C <lane> show 55c07cd:<path>`), not the
working tree. Receipts: `.ufo/waves/round-49/w1/R49Simplify/receipts.txt`.

## Axes

1. **deletion** — lines removable with provably zero behavior change on the frozen predicate.
2. **guard-preservation** — no deletion that leaves a real cheat unguarded (a leg a control cannot see).
3. **evidence-shape** — one producer per printed string; one authority per datum; nothing printed that nothing reads.

Moves were kept only when they reduce (1) without touching (2). Verdict vocabulary: *take* / *nominal* / *do-not*.

## Round diff, for scale

`git diff --numstat 6256760 55c07cd`: 10 files, +1042/−28. By addition count: three new counters 781
(`check-scrub-admission-r49.py` 421/0, `check-adjacency-table-r49.py` 223/0, `check-fd-band-r49.py` 137/0),
frozen record 60/0, before-receipt 41/0, census 56/9, entry 30/12, PROVINCE 32/7, LOG 23/0, SCORECARD 19/0.
The round's own code surface is 837 added lines against 9 removed in the script it changed — the deletion
budget below is therefore the frontier, not the margin.

## Findings by severity

### F1 (medium) — unreachable guard in the C1 counter, and the docstring claims a property it does not check

`tools/check-scrub-admission-r49.py:166-175`: `j` at :171 is the first index `> i` whose line
`startswith('## ')`, therefore `lines[i+1:j]` contains no such line, therefore `inner` at :172 is **always**
`[]` and the return at :174 can never execute. The branch is dead by construction, not by luck.

The docstring (`:11-12`) sells it as `structural_ok ... one header each, no inner heading (F1 carry-over)`.
The F1 property is delivered by `j` (a row simply ends at the next `## ` heading), not by this branch. Worse,
the dead branch does not even cover the case it reads as covering: a `### Sub` line inside a row neither
terminates the extent (`'###'.startswith('## ')` is false) nor trips `inner`, so it is silently folded into
the row hash. So the branch is both dead and misleading.

Nothing is lost by deleting it: a row that grows a `## ` line is caught by the row-hash leg
(`:367-369`, `h != hashes.get(row)`) and by the frozen hash table, not here.

**Proposal (take).** Delete `:172-174` (3 lines). Keep `:175`.
Predicate-safety: `inner` is provably empty for every input, so `problems` from `row_extent` is unchanged for
every row, `structural_ok` stays 1 for the freeze bytes, and `structural_ok == 1` stays satisfiable.
Docstring (`:11-12`): `structural_ok the bound extent of each row is `## GR<n>` up to the next `## ` heading,
                one header each (F1 carry-over).`

### F2 (medium) — the C3 counter documents a leg stronger than it implements: the `passed` count is parsed and never read

`tools/check-fd-band-r49.py:18-20` says `band_ok` requires the last line
`TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)`. `SUMMARY` (`:48`) captures four groups;
`band_ok` (`:105-106`) reads `(1)` status, `(2)` cases, `(4)` failed — **`(3)` passed is never compared**.
A census whose summary read `PASS (167 cases, 0 passed, 0 failed)` would satisfy `band_ok` and `cases`.
The mutation/falsifier seats (C3-B2/B6 in `.ufo/waves/round-49/make-w1-spec.py:131,139`) therefore test a leg
weaker than the frozen text.

**Proposal (not a deletion — one-line tightening, do not apply to the frozen counter mid-round):**
`and summary.group(3) == summary.group(2)` inside `band_ok`, or delete the "167 passed" promise from the
docstring. Both keep the predicate satisfiable today (the live census prints 167/167, receipt
`controls/battery-summary-r49-c3.jsonl` K-pass).

### F3 (medium) — census: the usage text quotes a diagnostic string no code path can print

`tools/tsukuroi-census.sh:608` — ``named diagnostic `fd band 240-249 exhausted` instead of a silent retry``.
The only producer is `:2115-2116`, which expands `${SELFTEST_FD_BAND:-240 241 … 249}` into `%s`, so the live
message is `fd band 240 241 242 243 244 245 246 247 248 249 exhausted`. The literal in the usage block has no
producer; a reader grepping for the documented form finds only the doc.

`diag_ok` (`check-fd-band-r49.py:92-93`) requires the literal `fd band %s exhausted` — satisfied by :2115 —
plus `text.count('fd band') >= 2`, which the usage line helps satisfy. So the doc line is currently
load-bearing for a *count*, not for a string that anyone can observe.

**Proposal (take, text only).** `:606-609` →
```
               alias inside TMPDIR, never /tmp — R48-C2; when the resolver's descriptor
               band (default 240 241 … 249, overridable via SELFTEST_FD_BAND) is
               exhausted, the resolver fails with the named diagnostic
               `fd band <members> exhausted` instead of a silent retry — R49-C3); exit 0 pass, 1 fail
```
Predicate-safety: `stale_ok` untouched (`builds a /tmp fixture tree` absent either way), `diag_ok` still sees
`fd band %s exhausted` at :2115 and still counts ≥2 `fd band` occurrences, `band_ok` runs the case, `cases`
unchanged.

### F4 (low) — duplicated default band literal in the census (drift hazard)

`tools/tsukuroi-census.sh:2082` and `:2116` both carry the literal `240 241 242 243 244 245 246 247 248 249`.
If the band ever changes in `selftest_base_dir`, the diagnostic keeps naming the old band; if it changes only in
the diagnostic, the message lies. There is no reader that compares the two (the selftest asserts
`ST_BASE_ERR`, not the message — `:3589-3592`).

**Proposal (take, post-measurement).** After `:2082` add `ST_BASE_BAND=$band` (same carrier convention as
`ST_BASE_DIR`/`ST_BASE_FD`/`ST_BASE_ERR`, already reset at `:2077-2079`), and replace the literal at `:2116`
with `"${ST_BASE_BAND:-240 …}"`. Net −1 line, one source of truth. `band_ok` sets `SELFTEST_FD_BAND='240 241'`
explicitly (`:3586`), so the printed band is `240 241` before and after; `diag_ok` unaffected (string and count
both survive at :2115, :608, :3588/3590/3592).

*Caveat for the L1:* `tools/tsukuroi-census.sh` is C3's measured blob. F3 and F4 must not land before the live
C3 measurement, or the measurement revision and the reported blob diverge.

### F5 (low) — C3 `extract()` is a tar pipeline for one file

`tools/check-fd-band-r49.py:63-72` runs `git archive --format=tar`, `import io` inside the function (`:69`),
and `tarfile` (`:38`) to materialise one blob. `git show rev:path` yields identical bytes and needs no archive,
no `io`, no extraction.

**Proposal (take).** Delete `:38 import tarfile`, `:69 import io`, and `:64-71`; replace with
```python
def extract(lane, rev, dest):
    p = git(lane, 'show', f'{rev}:{CENSUS}')
    if p.returncode != 0:
        return None
    path = os.path.join(dest, CENSUS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as fh:
        fh.write(p.stdout)
    return path
```
−2 lines, −2 imports, same bytes into `--work`. No leg reads the extraction route.

### F6 (low) — PROVINCE note copies the data it points at

`PROVINCE.md:301-305` re-enumerates the nine removed sibling ranges verbatim, and `:308-310` re-states the
ADJ→OUT mapping `(ADJ-01 → OUT-002, … ADJ-07 → OUT-010)` that `:46-52` already carries. Two problems:
(a) the mapping is data restated in prose and can drift from the table with no reader to catch it; (b) the nine
literal `…/PROVINCE.md:N-M` strings in the note are fresh matches for the very locator class the round
outlaws — `BARE` in the counter is scoped to the ownership cells (`check-adjacency-table-r49.py:49,134-136`),
so C2 is unaffected, but any later bare-range scan widened to the whole file would fire on this note.

**Proposal (take, post-measurement).** Delete `:301-305`'s parenthetical list and `:308-310`'s mapping;
keep provenance as a pointer, i.e. apply the round's own locator rule to its own note:
```
Append-only note, 2026-10-28. The seven rows of `## Adjacent — finding-to-owner handoffs` carried bare
sibling line ranges in their **Ownership source** cell (nine `*.md:N[-M]` occurrences, preserved in the
base revision `6256760d1382ce4ce20fcba830d4b2912cfbf12b` at `PROVINCE.md`, lines 46-52). That is the
locator class QUALITY 32 / R19-ADJ-POINTERS rules out: a line range is not a locator, and a quote that
moved must resolve by quote plus pinned blob. Each cell now names the `OUT-0NN` anchor whose own
**ADJ row** cell names that finding class. The anchor rows carry the pinned sibling commit, exact
heading, ≤25-word quote and the registry blob sha256, so the ownership pointer now resolves by content.
The round-19 rule "the line-range table is not changed" is superseded for this column only; the finding
classes, retains, recipients and handoff evidence are unchanged.
```
≈ −6 lines. Predicate-safety verified: the C2 counter reads only `## Adjacent — finding-to-owner handoffs` and
`## Adjacent — portable ownership anchors (round 19)` (`:44-45,96-112`); it never reads the round-49 note, and
the replacement contains no `\.md:\d+` match (`*.md:N[-M]` has no digit after `:`).

### F7 (low) — C1 docstring names a flag this script does not define

`tools/check-scrub-admission-r49.py:38` — `--skip-anchors-check is not used here; --lane names the repo.`
`--skip-anchors-check` is C2's flag (`check-adjacency-table-r49.py:211`); C1's parser (`:400-409`) has no such
option, and `--lane` is already shown in the usage line at `:40`.

**Proposal (take).** Delete `:38`. −1 line, no behavior.

### F8 (low) — C1 `marks_leg` takes a parameter it never reads

`tools/check-scrub-admission-r49.py:312` `def marks_leg(entry, skill, readme, hashes)` — `hashes` does not
appear in the body (`:313-322`); the only caller passes it (`:384`). The signature advertises a coupling
(hash-gated marks) the body does not implement.

**Proposal (take).** `def marks_leg(entry, skill, readme)` and `marks, marks_ok = marks_leg(entry, skill, readme)`.
No leg reads it.

### F9 (nominal — recommend NOT applying) — `cases` conjunct duplicated inside and outside `band_ok`

`check-fd-band-r49.py:105-106` already requires `cases == TARGET_CASES`, and `:113` requires it again. Removing
it from `band_ok` is behavior-identical (`:113` still gates PASS/FAIL). But the duplication is the honest
belt-and-braces against a later edit of the predicate line, and the file is frozen mid-measurement. **Nominal
only.**

### F10 (informational) — duplication across the three counters

Measured shapes: `git()` ×3 (`check-scrub-admission-r49.py:130-131`, `check-adjacency-table-r49.py:58-59`,
`check-fd-band-r49.py:52-53`), the `--lane` default expression ×3 (`:402`, `:208`, `:124`), `BASE` ×3
(`:51`, `:40`, `:41`), the `except Exception → FAIL(2)` footer ×3 (`:414-417`, `:216-219`, `:130-133`), plus
`read_text`/`load_json` override dance (`check-scrub…:139-163`) that C2 re-shapes as `show_text` (`:62-70`).
A `tools/_r49common.py` would absorb ≈15 lines.

**Recommendation: do not do it, for these three.** "Frozen counter" means *its bytes are the artifact whose
digest the wave cites*; a shared module turns three frozen counters into one mutable dependency, so a future
edit to the helper silently changes three measurements without re-freezing. Adopt the pattern only if a fourth
`check-*-r49`-shaped counter appears (round 50+): one `_common.py` with `git()`, `show()`, `lane_default()`,
`fail_footer()`. F5 is the one dedup that can be taken *inside* C3 without creating that dependency.

## What I would NOT delete (each guards something a control or a cheat needs)

| Kept | Why |
|---|---|
| `SNAPSHOTS` S240 `ioctl.c`, S249 `capture.txt` (`check-scrub…:63-66,79-80`) | Look unused if you scan only `**Quote.**` lines — public quotes use S237/S242/S243/S244/S246/S247/S248 only (receipt 8). But `CITE['GR2']` needs `ioctl.c` and `CITE['GR3']` needs `capture.txt` (`:82-84`), and `verify_citation` resolves report citations from that cache (`:235-241,244-256`). Deleting them makes every GR2/GR3 seat report uncitable. **This is the trap a dead-weight scan is most likely to fall into.** |
| The contradicting-line scan (`check-scrub…:306-308`, `ANY_VERDICT_RE:90`) | Blocks a report whose first line says `holds` and whose body says another row/verdict. No control exercises it (K3 covers only a first-line `partly`), but removing it is a one-line cheat against `verdicts_ok`. |
| `no_dups`/`DupKey` (`check-scrub…:117-127`, used at `:154,161`) | `json.loads` silently keeps the last duplicate key; without this a `w1-results.json` carrying two entries for one seat binds as one — a direct `seats_ok == 18` cheat. Unexercised by the battery (K6 removes entries instead). |
| The row-source citation leg (`check-scrub…:244-251`, `CITE`) | Forces each seat report to cite *its row's* sources, not any pinned file. |
| C2 `problems`/`per_row` accumulators (`check-adjacency-table-r49.py:98-102,124-126,138-184`) | No predicate leg, but they are the only human-readable reason a FAIL happened; deleting them makes a FAIL unarguable. |
| `case_pass` + `DIAG_CASE` line test (`check-fd-band…:104`) | Catches a census that prints 167 cases while `(R49-C3)` is a `bad` line. |
| `r49_held` reservation and its `bad` fallback (`tsukuroi-census.sh:3579-3582,3598-3599`) | Without the fallback the case silently skips and the suite still prints 167 PASS — the exact "silent success" C3 exists to remove. |
| `OWNERSHIP_*` note line `The round-19 rule … superseded for this column only` (`PROVINCE.md:312-313`) | It is the written supersession of a prior recorded rule; deleting it leaves a silent reversal. |

## Residual risks / verification gaps (not deletions)

- **R1 — the C2 cross-check leg is never falsified.** K0–K3 carry `anchors_checker_rc: -1`
  (`controls/battery-summary-r49-c2.jsonl`), i.e. they ran with `--skip-anchors-check`, while the same base
  province measured plainly gives `anchors_checker_rc: 0` (`before/c2-at-base.json`). No control shows the leg
  exiting non-zero for a *checker* reason; K-pass is the only observation of `0`. Proposed control (for the L1,
  not this seat): freeze province + live registry, then mutate one anchor's `sibling_commit` in a fixture so the
  checker exits 1 — the counter must FAIL with `adj_rows/linked_rows/bare_ranges/anchors_ok/registry_ok` all
  green.
- **R2 — the control battery is not replayable from its receipts.** Every receipt's key set is
  `_rc, base, control, note, <legs>`; no `argv`/flags field. Which override each control used is inferable only
  from `anchors_checker_rc: -1` (F/R1) and from the C1 fixture overrides named in the docstring. A receipt that
  does not name its command cannot be re-run by a later seat.
- **R3 — R20 baseline-prefix invariant is now permanently broken (not a round-49 regression).**
  `check-adjacency-anchors.py:189-193` requires `current == baseline + exact R20 suffix`;
  `0cbc34dd`'s `PROVINCE.md` is 146 lines, an exact prefix of **base** (`YES`) but not of freeze
  (`cmp: differ: char 3079, line 46`). So `--ownership-corrections` (the gate row at `SKILL.md:2116`) fails on
  the freeze province — and already failed at base, because base:154 is `## Round-26 frontier — storage
  integrity`, not the R20 suffix. Record this so no later seat files it as a C2 regression, and so any repair
  knows line 46 is no longer baseline bytes. The C2 counter's default-mode invocation
  (`check-adjacency-table-r49.py:188-189`, no `--ownership-corrections`) is correct for what it measures.
- **R4 — `check-fd-band-r49.py:105` never checks the `passed` count** (F2). Until tightened, the docstring's
  `(167 cases, 167 passed, 0 failed)` is a stronger claim than the code.
- **R5 — the R49-C3 case is host-dependent on fds 240/241 free** (`tsukuroi-census.sh:3580`). If either is
  occupied by a wrapper, the whole selftest prints a failed case (via `:3599`) although the audit is
  meaningless; picking the first two free members of the band would make it portable. Deterministic on this
  host (K-pass PASS, receipt), so a latent risk, not a present defect.
- **R6 — C1 `snapshots()` swallows digest mismatches** (`check-scrub…:191-199`, `continue`), so the JSON cannot
  distinguish "snapshot absent" from "digest moved"; the evidence that `quotes_ok` rests on digest-pinned bytes
  is implicit in `per_row[row]['quotes']['bad']` strings only.
- **Not run by this seat:** none of the three counters, no selftest, no clone, no mutant. Every claim here comes
  from reading frozen bytes, the control receipts, and byte comparisons of lane blobs. I did not verify that the
  counters currently PASS (other seats hold that measurement), and I did not execute the checker's
  `--ownership-corrections` mode — R3 is derived from its source and a `cmp` of the two blobs.

## Deletion ledger

| # | Where | Lines | Verdict |
|---|---|---|---|
| F1 | `check-scrub-admission-r49.py:172-174` | −3 | take |
| F2 | `check-fd-band-r49.py:105-106` (add `group(3)` test) | +0 / −0 | take as a fix, not a deletion |
| F3 | `tsukuroi-census.sh:606-609` (usage text) | ±0 | take |
| F4 | `tsukuroi-census.sh:2082` + `:2116` | −1 | take, post-measurement |
| F5 | `check-fd-band-r49.py:38,64-71,69` | −2, −2 imports | take |
| F6 | `PROVINCE.md:301-305,308-310` | ≈−6 | take, post-measurement |
| F7 | `check-scrub-admission-r49.py:38` | −1 | take |
| F8 | `check-scrub-admission-r49.py:312,384` | ±0 (token) | take |
| F9 | `check-fd-band-r49.py:105-106` `cases` conjunct | −1 | nominal, keep |
| F10 | cross-counter `git()`/`BASE`/`--lane`/footer | ≈−15 | do-not (breaks frozen byte-identity) |

Net honest deletion with every frozen predicate still satisfiable: **≈13 lines and 2 imports**, no leg
removed, no control made weaker.
