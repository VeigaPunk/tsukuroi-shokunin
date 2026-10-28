VERDICT: draft

# GScribeMarks — C2-D1: the three round-48 admission marks (exact draft text)

Item C2-D1 only. Nothing here is landed; the L1 is the integrator and lands these bytes ONLY on a C2 counter PASS.
All work was done in a throwaway clone under `/fast/scratch/hyaku/tsukuroi-r48/GScribeMarks/`; no lane file was written.

## What was read, and with what it was measured

- Frozen counter bytes: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ae99f021b76f8eb1c8805d32d80644464afb1ff6:tools/check-scrub-admission-r48.py` (mark constants at `:72-75`,
  mark evaluation at `:360-365`: `entry` is an exact line, `skill` an exact line, `readme` any line holding both
  `btrfs-scrub-grounding-r45.md` and `admitted round 48` with no `unadmitted|not admitted|never admitted|stay pending|stays pending`).
- Frozen structure re-measured: `python3 counter.py --revision ae99f021b76f8eb1c8805d32d80644464afb1ff6 --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --section-hash` →
  `{"structural_ok": 1, "problems": [], "section_sha256": {"GR1": "fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8",
  "GR2": "e0b391e198f67ff57ce7971e2dd589faaa9390ebf2d2fd49dc6d103c163a52ce", "GR3": "43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c"}}` —
  identical to the declared hashes.
- Fixture `fx2.QIF2d0` (clone of the lane, `git rev-parse --show-toplevel` asserted equal to the fixture dir, detached at
  `ae99f021b76f8eb1c8805d32d80644464afb1ff6`, commits made as `fixture <fixture@invalid>`). Candidate revision
  `b4e65e905bd095fa00115ffa608a8f05371e07b9` = frozen bytes + the three blocks below:
  `python3 counter.py --lane <fixture> --revision b4e65e9` → exit 1,
  `marks {"entry": true, "readme": true, "skill": true}`, `marks_ok` 3, `structural_ok` 1,
  `quotes_ok` 3 (GR1 12/12 quote lines, GR2 29/29, GR3 12/12), `verdicts_ok` 0 (no `w2-dispatch.json` /
  `w2-results.json` / seat reports exist yet), `verdict` FAIL.
- `counter-final.json` is the same counter run at the landed revision `fa5a031ae82e806a1efd5a6f96f8469704569b4c`
  (final drafts + the C3 restatement named in Finding 1); it reads `marks_ok 3`, `structural_ok 1`, `quotes_ok 3`,
  `verdicts_ok 0`, exit 1.

## (a) Entry block — `corpus/knowledge/btrfs-scrub-grounding-r45.md`

Append at end of file, after line 269 (the file ends with a newline; the block is one leading blank line, then the header
line, then the text below; +43 lines → 312). The block starts with the exact line the counter matches.

```markdown

## Gate status — round 48 (GR1-GR3 admitted)

Round 48 read GR1-GR3 through the seat-written channel of its one counted wave (`w2`): `tools/check-scrub-admission-r48.py`
(frozen with the claims at `ae99f021b76f8eb1c8805d32d80644464afb1ff6`) binds each counted seat through the report file it
writes — line 1 `ROW GR<n> VERDICT: holds|partly|fails`, line 2 `SECTION SHA256: <hex>` — and credits it only on the
current row hash with every `file:line` citation resolving in the pinned snapshot. The frozen predicate is
`structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`, run as
`python3 tools/check-scrub-admission-r48.py --revision <REV>`. A row is admitted when at least three credited seats read
`holds`, at least one of them a reviewer and one a critic, their report bodies pairwise distinct, and no bound-format
seat on the current row hash reads `partly` or `fails`.

Frozen section hashes at `ae99f021b76f8eb1c8805d32d80644464afb1ff6` (whole-row extent, `## GR<n>` up to the next header):

| Row | Section sha256 |
|---|---|
| GR1 | `fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8` |
| GR2 | `e0b391e198f67ff57ce7971e2dd589faaa9390ebf2d2fd49dc6d103c163a52ce` |
| GR3 | `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` |

The 18 counted seats of wave `w2`, three reviewers and three critics per row; fill each verdict and hash cell from the
first two lines of `.ufo/waves/round-48/w2/<seat>.md` before landing this block.

| Row | Seat | Role | Verdict | Section sha256 |
|---|---|---|---|---|
| GR1 | R48RevGR1a | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR1 | R48RevGR1b | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR1 | R48RevGR1c | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR1 | R48CritGR1a | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR1 | R48CritGR1b | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR1 | R48CritGR1c | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48RevGR2a | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48RevGR2b | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48RevGR2c | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48CritGR2a | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48CritGR2b | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48CritGR2c | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48RevGR3a | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48RevGR3b | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48RevGR3c | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48CritGR3a | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48CritGR3b | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48CritGR3c | critic | <fill: holds / partly / fails> | <fill: hex> |
```

## (b) SKILL.md block — append at end of `SKILL.md`

Append after line 4546 (one leading blank line, then the header line, then 6 body lines; +9 lines → 4555). The first line
is the exact line the counter matches; it adds no `|`-prefixed line, so the depth row's table-line count stays 1323.

```markdown

## Scrub grounding — round 48 admission

Admitted 2026-10-28 (round-48 C2; drafted by wave seat GScribeMarks, landed by the L1 on the counter PASS): GR1, GR2 and
GR3 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` (entry section "Gate status — round 48 (GR1-GR3 admitted)") passed the
depth gate — `python3 tools/check-scrub-admission-r48.py --revision <REV>` reports `structural_ok` 1, `quotes_ok` 3 and
`verdicts_ok` 3 over the 18 counted seats of wave `w2`, which ground SR8 on S246 (Linux v7.2.11 `lib/cmdline.c`,
`lib/vsprintf.c`, `lib/kstrtox.c`) and S243, SR7 on S247 and S242, SR9 on S248, S244 and the own-work S249 capture
(`.ufo/waves/round-45/frozen/hostcap/capture.txt`; every snapshot is digest-pinned in its wave's `frozen/src/SHA256SUMS`).
```

## (c) corpus/README.md row — append at end of `corpus/README.md`

Append after line 480 (one leading blank line, then a two-line heading and a three-line table; +8 lines → 488). The marked
line is the table row; it holds both tokens and no negation word.

```markdown

## Round-48 coverage note (appended 2026-10-28)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-46 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/btrfs-scrub-grounding-r45.md` | GR1, GR2 and GR3 admitted round 48: three reviewers and three critics of wave `w2` bound `holds` on the frozen row bytes and the depth gate PASSed (`structural_ok` 1, `quotes_ok` 3, `verdicts_ok` 3, `marks_ok` 3) | S246-S249; S242, S243, S244, S237; entry section "Gate status — round 48 (GR1-GR3 admitted)" |
```

## Non-admission variants — use these instead when any row fails

Self-contained replacements; any one of them keeps all three marks false (measured, control K9). They carry no
`admitted round 48` substring at all, so they cannot be misread as an admission; the README row also says `stay pending`,
which the negation guard rejects on its own.

(a') entry, in place of the admission block:

```markdown

## Gate status — round 48 (the depth gate FAILED; GR2 stays pending)

Round 48 bound the rows through the seat-written channel of its one counted wave (`w2`): `tools/check-scrub-admission-r48.py`
(frozen at `ae99f021b76f8eb1c8805d32d80644464afb1ff6`) credited no seat on GR2's current bytes (section sha256
`e0b391e198f67ff57ce7971e2dd589faaa9390ebf2d2fd49dc6d103c163a52ce`). GR1 and GR3 stay pending too: the predicate needs all
three rows. No row is admitted this round; the marks are not written and the entry's GR2 narrowing is unread by any counted seat.
```

(b') SKILL.md, in place of the admission block:

```markdown

## Scrub grounding — round 48 status (the depth gate FAILED; GR1-GR3 stay pending)

Round 48's counted wave `w2` bound no seat on GR2's corrected bytes with a `holds` verdict, so
`corpus/knowledge/btrfs-scrub-grounding-r45.md` (entry section "Gate status — round 48") is not admitted: GR1-GR3 stay
pending, and the README carries no admission line for it.
```

(c') corpus/README.md, in place of the admission row:

```markdown

## Round-48 coverage note (appended 2026-10-28)

| Note | Holds | Sources |
|---|---|---|
| `knowledge/btrfs-scrub-grounding-r45.md` | GR1-GR3 stay pending in round 48: the counted wave bound no verdict, so no row is admitted | S246-S249 |
```

Variant rule: if one row fails, all three rows stay pending — the predicate needs `verdicts_ok == 3` — so write the
failing row's evidence into block (a') and leave GR1-GR3 pending. A README line that names only some rows as admitted
must not be written: see Finding 2.

## Controls — `controls-r48-marks.jsonl` (each leg commits over frozen `ae99f021b76f8eb1c8805d32d80644464afb1ff6` in the fixture)

| Control | Rev | Exit | Marks entry / skill / readme | marks_ok | structural_ok | quotes_ok | verdicts_ok |
|---|---|---|---|---|---|---|---|
| K0 frozen base, no marks | `ae99f021b76f` | 1 | False / False / False | 0 | 1 | 3 | 0 |
| K1 README "GR3 not admitted round 48" | `7e1959831e98` | 1 | True / True / False | 2 | 1 | 3 | 0 |
| K2 README "GR1-GR3 stay pending in round 48" | `63e48e1839ca` | 1 | True / True / False | 2 | 1 | 3 | 0 |
| K3 entry header prefix "## Gate status — round 48" | `2b7b9dd2c332` | 1 | False / True / True | 2 | 1 | 3 | 0 |
| K4 SKILL header with one trailing space | `83ea68350a9b` | 1 | True / False / True | 2 | 1 | 3 | 0 |
| K5 README "GR3 unadmitted round 48" | `36d9c7d0fb8d` | 1 | True / True / False | 2 | 1 | 3 | 0 |
| K6 candidate: final drafts as written | `8b79c11345b1` | 1 | True / True / True | 3 | 1 | 3 | 0 |
| K7 README partial claim + "stays pending" | `c4251fad61e0` | 1 | True / True / False | 2 | 1 | 3 | 0 |
| K8 README partial claim, no negation word | `ebaca636b62d` | 1 | True / True / True | 3 | 1 | 3 | 0 |
| K9 non-admission variants | `debe9eddbdb6` | 1 | False / False / False | 0 | 1 | 3 | 0 |

K0 shows the base earns nothing. K1-K5 show each mark is the exact-line or negation-guarded leg it claims to be: a
prefix header loses `entry` (K3), one trailing space loses `skill` (K4), `not admitted` / `unadmitted` / `stay pending`
lose `readme` (K1/K2/K5). K6 is the candidate (all three marks). K9 is the non-admission set (all three marks false).

## Findings

1. **C3 harm unless the SCORECARD axes line counts are restated with the marks.** The 27 checks bind two literal line
   counts: depth row `SKILL.md` 4546 (`SCORECARD.md:3029`) and coverage row `corpus/README.md` 480 (`SCORECARD.md:3030`).
   With the marks appended the files hold 4555 and 488 lines (`git show <fixture>:SKILL.md | wc -l`,
   `git show <fixture>:corpus/README.md | wc -l`), so K08 and K11 turn into mismatches: measured at the earlier 8-line
   SKILL draft (`cfa41230`) `check-self-assessment.py` reported `checked` 27, `mismatches` 5 — K08 (stated 4546, observed
   4557), K10, K11 (stated 480, observed 488), K13, K17 (`sa-cfa41230.json`). With the final 6-line block and both numbers
   restated, the same tool at `fa5a031` reports `checked` 27, `mismatches` 3 — K10, K13, K17, exactly the declared
   baseline (`sa-restated.json`). So the landing must carry `SKILL.md` 4546 → 4555 and `corpus/README.md` 480 → 488 in the
   same restatement; if any later SKILL.md/README edit lands, recount first with `wc -l`. K09 (SKILL `|` lines 1323) is
   untouched.
2. **The README leg has no per-row binding.** Control K8 writes `GR1 and GR2 admitted round 48` alone: `readme` is true
   and, with the other two marks present, `marks_ok` 3, although GR3 is not claimed. The guard is keyword- and
   line-scoped only (K7, the same claim plus `GR3 stays pending`, is rejected). Consequence: never write
   `admitted round 48` on a line unless all three rows passed, and never use the partial-claim form as a shortcut.
3. **The marks alone cannot make the counter PASS.** Every control with `marks_ok` 3 still exits 1 because
   `verdicts_ok` is 0 until the 18 seats bind. A premature landing is therefore caught by the counter, but it would leave
   a false admission statement in the tree until reverted — which is why the variants above exist.
4. **The entry block is C3-neutral.** The 27 checks bind line counts only for `SKILL.md` (K08, K09) and
   `corpus/README.md` (K11); the entry's +43 lines are read by no check.

## No regression elsewhere at the marks revision

Run at `fa5a031` (= final drafts + restatement) and compared with the same tool at `ae99f021b76f8eb1c8805d32d80644464afb1ff6`:

| Tool | At ae99f021b76f8eb1c8805d32d80644464afb1ff6 | At fa5a031 (with marks) |
|---|---|---|
| `check-appended-notices.py` | PASS, `record_count` 97 | PASS, `record_count` 97 |
| `check-section-citations.py` | PASS | PASS |
| `check-adjacency-anchors.py` | PASS | PASS |
| `check-knowledge-header.py` | (not run at frozen) | PASS |
| `check-registry-coverage.py` | FAIL, 3 `REGISTRY-ROW-MISSING` (r47, r48, score-selftest-tmpdir-r48) | FAIL, the same 3 findings |
| `check-scrub-grounding-r45.py` | FAIL `verdicts_ok 0`, other legs 3/3/3/1/1 | identical legs and per-row output |
| `check-self-assessment.py` | 27 checked, 3 mismatches | 3 mismatches (K10, K13, K17) with the restatement |

`check-registry-coverage` is already red at the frozen revision on the same three tool files; the marks add no finding.

## Not done

- No counted seat, dispatch or results file exists for wave `w2`; `verdicts_ok` is 0 in every run, so I did **not**
  observe a PASS and make no claim about one.
- The final block size's own K08/K11 outcome without the restatement was not re-run; it follows from the equality check
  and the measured counts (4555, 488). The measured 5-mismatch run (`sa-cfa41230.json`) used the earlier 8-line block.
- No mutation tests, no C1 work, no counted seat's work; no tooling installed; no pacman transaction.
- The census selftest ran only inside `check-self-assessment.py` (two serial runs; K13 observed `166 cases` at both
  revisions); I did not run `bash tools/tsukuroi-census.sh --selftest` on its own.

## Receipts (this directory)

`draft-a.md`, `draft-b.md`, `draft-c.md` (exact block bytes), `draft-na-a.md`, `draft-na-b.md`, `draft-na-c.md`
(non-admission bytes), `controls-r48-marks.jsonl` (K0-K9, marks per control), `counter-final.json` (counter at
`fa5a031`), `sa-ae99f021.json`, `sa-cfa41230.json`, `sa-restated.json` (self-assessment runs), `adj-*.json`,
`check-*.json` (the tools above at `fa5a031`), `fixture-path.txt` (fixture dir + candidate rev).

Scratch `/fast/scratch/hyaku/tsukuroi-r48/GScribeMarks/` (both fixture clones) was removed after these receipts were copied; the fixture paths in `fixture-path.txt` no longer resolve.
