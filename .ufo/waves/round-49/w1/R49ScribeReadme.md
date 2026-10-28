VERDICT: draft

# R49ScribeReadme — item F-9: round-49 `corpus/README.md` append (draft, text only)

Lane bytes read only at the freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`
(`git -C …/tsukuroi-shokunin show <FREEZE>:<path>`). Nothing in the lane, the fleet repo, a sibling lane or a
PATH directory was written; the lane working tree was never the bytes under test. Scratch
`/fast/scratch/hyaku/tsukuroi-r49/R49ScribeReadme/` removed at the end of this seat.

## Axes

- **README (primary):** one append-only drop-in block that matches the round-42…46 note style (heading, append-only
  preamble line, `| Note | Holds | Sources |` table, a `### Frontier notice` paragraph, prose lines under ~110 cols),
  whose table carries C1/C2/C3 with sources and the three frozen counter paths, whose Frontier notice answers both
  questions the item asks, and which contains the exact sentence `marks_leg` demands.
- **Depth (secondary):** every factual assertion in the text is tied to a freeze-path line or an observed command,
  and the two axes where a README can quietly overclaim (a locator change read as an ownership change; a test-surface
  diagnostic read as a contract change) are written with their limits named.

## What I produced

- Proposed text (drop-in, 6 215 bytes, sha256 `4a44ff4…`): the whole block is in the section *Exact proposed text*
  below and byte-identical at `.ufo/waves/round-49/w1/R49ScribeReadme/append-candidate.md`.
- Placement: appended to the end of `corpus/README.md` (frozen length 480 lines, last line `…not a new host
  surface.` + LF), preceded by one blank line so the file ends `…surface.\n\n## Round-49 coverage note …`.
  Verified append-only: `head -480` of frozen+draft differs from the frozen README by 0 lines
  (`prefix-unchanged.diff`, 0 bytes).
- Style match: the last five notes are `## Round-4n coverage note (appended 2026-10-2n)`, then one append-only
  sentence naming the notes above that stay as written, then a `| Note | Holds | Sources |` table, then a Frontier
  paragraph (`corpus/README.md:406,416,427,454,468`). Round 44 opens its notice with "The round-26 condition at
  `corpus/README.md:243` is met…" (`:438`); round 45 opens with the flat "Frontier: nothing moves." (`:462`), round
  46 with "Frontier: nothing moves this round" (`:479-480`). The draft uses the flat opener and names both reasons,
  as round 46 does.

## The sentence the C1 counter looks for

`tools/check-scrub-admission-r49.py:85-88` fixes the mark:

```
MARK_README = ('btrfs-scrub-grounding-r45.md', 'admitted round 49')
NEGATE_RE   = re.compile(r'unadmitted|not admitted|never admitted|stay pending|stays pending')
```

and `marks_leg` (`:312-322`) normalizes whitespace, splits on `(?<=[.!?])\s+`, and requires **one** sentence that
contains both strings and no negation word. `marks_ok` is the **count** of the three marks (`entry`, `skill`,
`readme`), so the C1 predicate `marks_ok == 3` needs all three; the README sentence supplies one of them.

Exact sentence (PASS branch, as landed in the draft):

> C1 admission: `corpus/knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3 are admitted round 49 — the fresh 18-seat w1
> cohort re-read the corrected rows `holds` with distinct bodies and the frozen counter passes all six legs — so the
> rows leave the pending state that the round-45 and round-46 gate sections recorded.

Observed (`.ufo/waves/round-49/w1/R49ScribeReadme/marks-leg-tests.txt`, sha256 `894fbf6…`):

```
frozen README + draft: matching sentences = 1 | negated = [False]
marks.readme (draft) = True
marks.readme (frozen README) = False
variant 'admitted'                                                     -> marks.readme True
variant 'unadmitted'                                                   -> marks.readme False
variant 'not admitted'                                                 -> marks.readme False
variant 'never admitted'                                               -> marks.readme False
variant 'admitted, and the rows stay pending for the rest of the wave' -> marks.readme False
FAIL-branch sentence -> marks.readme False
```

Integration of the leg through the real counter, production entry and SKILL bytes at the freeze, README overridden:

```
python3 tools/check-scrub-admission-r49.py --revision 55c07cd3f8bff2e12117c34d57b4c618de74d85c \
  --readme-file …/readme-pass.md
→ {"verdict": "FAIL", "marks": {"entry": false, "readme": true, "skill": false}, "marks_ok": 1,
   "structural_ok": 1, "corr_ok": 1, "quotes_ok": 3, "verdicts_ok": 0, "seats_ok": 0}
```

(`counter-with-draft.json`, sha256 `af8721d…`; stderr empty.) The overall FAIL is the freeze state — the cohort has
not run and the entry heading is still `## Gate status — round 49 (pending; the frozen cohort has not settled)`
(`corpus/knowledge/btrfs-scrub-grounding-r45.md:277`) — not a defect in the README text. The run reads only git
objects (`subprocess.run(['git', …])` at `:131`), so it runs no census selftest.

FAIL branch — replace the whole `C1 admission:` paragraph with this one sentence (verified `marks.readme False`,
i.e. it does **not** forge the mark):

> The rows of `corpus/knowledge/btrfs-scrub-grounding-r45.md` stay pending round 49: the counted cohort did not settle
> `holds` on the frozen row bytes, so nothing is admitted.

Land exactly one branch. The PASS branch's word "pending" is safe only because `NEGATE_RE` needs `stay pending` /
`stays pending`; do not reflow the sentence across either phrase or add a negation word to it.

## The two Frontier questions

**C2 — do the anchors the ownership cells now cite move any Frontier ground? No, nothing moves.** Evidence:

- The round-49 edit is the seven **Ownership source** cells plus one appended PROVINCE section; diff BASE→FREEZE
  for `PROVINCE.md` is 25 added lines (the `## Round 49 —` note) and seven single-line row replacements
  (`git diff -U0 6256760d 55c07cd3` → `@@ -46,7 +46,7 @@` and `@@ -295,0 +296,25 @@`). The anchor table
  `## Adjacent — portable ownership anchors (round 19)` (`PROVINCE.md:108-130`, OUT-002…OUT-010) is **not**
  touched: the cells started citing anchors that already existed, so no new anchor, pin, quote or recipient is
  authored this round.
- Recipients and finding classes are unchanged; ADJ-06 still names both OUT-008 (kaidoku) and OUT-009 (revenger)
  (`PROVINCE.md:51`, anchors `:128-129`) and the round-49 note keeps the arbitration open
  (`PROVINCE.md:314-315`, "the kaidoku/revenger ownership arbitration stays open"), so the contested-ownership
  bullet (`corpus/README.md:33-34`) stays as written.
- An anchor is a pinned sibling commit + heading + ≤25-word quote (`PROVINCE.md:122-130`), i.e. a snapshot of what
  the sibling declared. It is not a recipient-side acknowledgement or closure, so the replay/acceptance bullet
  (`corpus/README.md:30-32`) gains nothing; drift of a sibling is caught by
  `tools/check-adjacency-anchors.py` whose rc is the counted `anchors_checker_rc` leg
  (`tools/check-adjacency-table-r49.py:15-24,54-55`), not absorbed silently.
- No census arm reads the table or the registry: `grep -n 'PROVINCE\|adjacency-anchors' tools/tsukuroi-census.sh`
  returns comment-only matches and **no** `adjacency-anchors` reference at all; the census's own ADJ surface is the
  round-32 `HANDOFF ADJ-04` line (`tools/tsukuroi-census.sh:51-60,3717-3731`), which publishes counts its probes
  already measured. So the round-26 rule (`corpus/README.md:243`, "becomes Core only after a read-only census arm
  reads it") does not fire and adjacency stays a handoff surface.

**C3 — does the `fd band … exhausted` diagnostic change the census contract? No.** Evidence:

- `git diff --numstat 6256760d 55c07cd3 -- tools/tsukuroi-census.sh` → `56 9` (56 insertions, 9 deletions), nine
  hunks, every one inside the hermetic-selftest surface: header comment `:415-417`, `--selftest` usage text
  `:606-609`, `selftest_base_dir` `:2076-2097`, the base-failure branch of `run_selftest` `:2112-2122`, and the new
  `(R49-C3)` case `:3574-3601`.
- `git diff … -- tools/tsukuroi-census.sh | grep -E 'TSUKUROI_CENSUS:|HEALTHY|DEGRADED|BLOCKED'` → **no match**
  (67 touched lines counted with the `---`/`+++` headers). No `probe_*` arm, verdict token, plane line, rollup term
  or exit-map entry changes, so the round-3 contract row (`corpus/README.md:12`) stands.
- What moves is the `--selftest` receipt: 166 → 167 cases and a named stderr diagnostic where the resolver returned
  1 without a word (`:2112-2121`). The stale string `builds a /tmp fixture tree` is absent from the frozen script
  (`grep -c` → `0`).
- Limit 1: the new `SELFTEST_FD_BAND` override (`:2082`, consumed at `:2115-2116`) is an unvalidated environment
  input; its only production caller is `selftest_base_dir` from `run_selftest` (`:2112`), so a hostile value can
  narrow the alias band in a test but cannot reach a probe arm. Recorded, not repaired — a lane-repair decision, not
  this seat's.
- Limit 2: no current `SKILL.md` line declares either count. `grep -oE 'PASS \([0-9]+ cases'` over the frozen
  `SKILL.md` has its maximum at 154 (`SKILL.md:4259`, inside the round-45 census-readers block); 166/167 appear
  nowhere, so the draft records the count without asserting a SKILL expectation.

## Facts asserted in the draft, and how each was checked

| Assertion | Check / source |
|---|---|
| seven corrections, five defect strings gone | `corpus/knowledge/btrfs-scrub-grounding-r45.md:279-283` (the list), counter C7 set `CORR_REQ` and C8 set `CORR_FORBID` at `tools/check-scrub-admission-r49.py:96-114`; `corr_ok 1` observed on the freeze bytes (counter run above) |
| 18 seats = 3 reviewers + 3 critics per row, distinct bodies, `holds` only | `tools/check-scrub-admission-r49.py:9-24` (docstring legs), `.ufo/waves/round-49/frozen/FROZEN.md` "Counted cohort" |
| row extents `## GR<n>` → next `## `, no inner heading; hashes | `FROZEN.md` hash table (GR1 `3a2ba180…`, GR2 `d4296085…`, GR3 `43430a14…`); headings `corpus/knowledge/btrfs-scrub-grounding-r45.md:14,56,152,198`; `structural_ok 1` observed |
| every `**Quote.**` line resolves on its digest-pinned snapshot | counter `quotes_ok 3` observed; snapshots pinned in `tools/check-scrub-admission-r49.py:57-80` |
| ADJ → OUT mapping, 9 bare ranges at base → 0 | `PROVINCE.md:46-52` (cells), `:122-130` (anchors), `tools/check-adjacency-table-r49.py:15-24,54-55`; base count `9` from `FROZEN.md` "Before at base" — **not re-measured by this seat** |
| registry carries the blob sha256; anchors pin commit/heading/≤25-word quote | `corpus/knowledge/adjacency-anchors-r19.json` (`sibling_commit`, `sibling_blob_sha256`, `heading`, `quote` fields, OUT-001 example), `PROVINCE.md:122-130` |
| census contract unchanged by C3 | the three diff observations above |
| 166 → 167 cases | `FROZEN.md` C3 row and `tools/check-fd-band-r49.py:13-23,43` (`TARGET_CASES = 167`) — **not re-measured by this seat** |

## What I did not do

- Did not run the C2 or C3 counters, the census `--selftest`, or the source re-opens — other seats hold those
  measurements; the `9 → 0` and `166 → 167` figures are quoted from the frozen target and must land in the README
  only with the measured PASS at the integrated revision.
- Did not verify sibling ledger drift against live sibling bytes (that is `tools/check-adjacency-anchors.py`'s
  counted `anchors_checker_rc` leg, `tools/check-adjacency-table-r49.py:15-27`).
- Did not edit `corpus/README.md`, `PROVINCE.md`, `SKILL.md` or the entry; no git/jj mutation anywhere; no tool
  installed (nothing needed). At this seat's exit the lane working tree reported `M corpus/SOURCES.md` plus the wave
  directory's untracked files (`git -C … status --porcelain`); that modification is **not mine** — every SOURCES.md
  byte I cite was read through `git show <FREEZE>:corpus/SOURCES.md`, and I wrote no lane file.

## L1 landing checklist (outside this seat)

1. Land the block only with `verdict PASS` at the integrated revision; otherwise land the FAIL-branch sentence.
2. The other two marks are L1 post-wave edits, both outside every frozen row extent: entry heading
   `## Gate status — round 49 (GR1-GR3 admitted)` (replaces `:277`, `MARK_ENTRY`) and the exact SKILL line
   `## Scrub grounding — round 49 admission` (`MARK_SKILL`, matched as a whole stripped line, `:314`).
3. The draft's table row for C2 states the ownership cells only; the round-19 registry's OUT-001 row keeps a
   `province_pointer` of `../mori-shokunin/PROVINCE.md:6-16` and no ADJ row cites OUT-001, so the `bare_ranges`
   leg never sees it. Do not widen the row's claim to "no line ranges anywhere".

## Exact proposed text (drop-in at the end of `corpus/README.md`)

```markdown

## Round-49 coverage note (appended 2026-10-28)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-46 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/btrfs-scrub-grounding-r45.md` (round-49 depth admission, GR1-GR3) | The seven corrections the round-48 counted cohort named are in the row bytes and the five defect strings it named are gone: GR1's `0X` prefix and its host-reading inference mark, and GR2's `is_valid` gate, cancel-sentence subject, suspend-path range and effects, `ioctl.c:3132` citation and `-ENODEV` devid case. A fresh cohort of one wave (18 seats: three reviewers and three critics per row) re-reads the corrected rows `holds` with pairwise distinct bodies, every `**Quote.**` line resolves on its digest-pinned snapshot, and each row extent is pinned by sha256 at the freeze (GR1 `3a2ba180…`, GR2 `d4296085…`, GR3 `43430a14…`; `## GR<n>` to the next `## ` heading, no inner heading) | S246-S249 (Linux v7.2.11, systemd v262); `corpus/knowledge/btrfs-scrub-grounding-r45.md:277-287`; `.ufo/waves/round-49/frozen/FROZEN.md`; counter `tools/check-scrub-admission-r49.py --revision <REV>` |
| `../PROVINCE.md` `## Adjacent — finding-to-owner handoffs` (round-49 C2) | The seven **Ownership source** cells cite portable `OUT-0NN` anchors (ADJ-01 → OUT-002, ADJ-02 → OUT-003, ADJ-03 → OUT-004, ADJ-04 → OUT-005, ADJ-05 → OUT-006 and OUT-007, ADJ-06 → OUT-008 and OUT-009, ADJ-07 → OUT-010) instead of sibling `*.md:N-M` ranges, of which 9 occurrences stood at the base and 0 remain in those cells. Each cited anchor carries its ADJ class, a pinned sibling `PROVINCE.md` commit, an `# …` heading and a ≤25-word quote, with the blob sha256 in the round-19 registry. Finding classes, retains, recipients and handoff evidence are unchanged, and the withdrawn ranges survive only as history in the PROVINCE round-49 note | `../PROVINCE.md:108-130` (anchor table), `:296-320` (round-49 note), `:46-52` (ADJ rows); `knowledge/adjacency-anchors-r19.json`; counter `tools/check-adjacency-table-r49.py --revision <REV>`, cross-check `tools/check-adjacency-anchors.py` |
| `../tools/tsukuroi-census.sh` (`selftest_base_dir` / `run_selftest`, round-49 C3) | Descriptor-band exhaustion is named, not silent: the resolver records `ST_BASE_ERR` (`fd-band`, `dirty-missing`, `alias-open`, `alias-not-dir`), `run_selftest` prints `selftest: fd band 240-249 exhausted (every descriptor already open), cannot alias TMPDIR <…>; no /tmp fallback (R49-C3)` on stderr and returns 1, and the stale `builds a /tmp fixture tree` comment is gone. One new case `(R49-C3)` pins the exhausted-band path under a narrowed two-descriptor band: `--selftest` now ends `PASS (167 cases, 167 passed, 0 failed)`, 166 at the base. `+56/−9` in nine hunks, all inside the hermetic-selftest surface; probe arms, verdict vocabulary and exit map untouched (Frontier notice below) | S255 (GNU bash 5.3 reference, `Redirections`, the fd>9 caveat); S252 and S253 (the `$TMPDIR` base contract of rounds 47-48); counter `tools/check-fd-band-r49.py --revision <REV>` |

### Frontier notice — round 49

Frontier: nothing moves, on either moved surface.

C2 changes a locator class, not ownership. The seven ownership cells gained `OUT-0NN` anchors and lost their
bare ranges (`../PROVINCE.md:296-320`); the anchor table itself is unchanged since round 19 (`:108-130`), the
finding classes, retains, recipients and evidence columns are unchanged, and ADJ-06 still names both OUT-008
(kaidoku) and OUT-009 (revenger) while the round-49 note keeps that arbitration open (`:314-315`), so the
contested-ownership bullet (`:33-34`) stays as written. An anchor pins a sibling commit, its heading and a
≤25-word quote: a snapshot of what that sibling declared, not a recipient-side acknowledgement, so the
replay/acceptance bullet (`:30-32`) gains nothing either. No census arm reads the adjacency table or the
anchor registry — the census carries a round-32 `HANDOFF ADJ-04` line that publishes counts its own probes
already measured, and it never opens `PROVINCE.md` or `knowledge/adjacency-anchors-r19.json` — so the round-26
promotion rule (`:243`) does not fire and adjacency stays a handoff surface, not new host ground. One limit
stays named: the registry keeps OUT-001's round-19 `province_pointer` as a `PROVINCE.md:6-16` range and no ADJ
row cites OUT-001, so the range leg is scoped to the seven ownership cells and never sees that row.

C3 does not change the census contract. The BASE→FREEZE diff of `../tools/tsukuroi-census.sh` is `+56/−9` and
every hunk sits in the hermetic-selftest surface: the header comment (`:415-417`), the `--selftest` usage text
(`:606-609`), `selftest_base_dir` (`:2076-2097`), the base-failure branch of `run_selftest` (`:2112-2122`) and
the new `(R49-C3)` case (`:3574-3601`). No probe arm changes, and no verdict token or exit-map entry changes:
`git diff <BASE> <FREEZE> -- tools/tsukuroi-census.sh | grep -E 'TSUKUROI_CENSUS:|HEALTHY|DEGRADED|BLOCKED'`
matches nothing, so the four-plane contract, the rollup and the 0/1/2 exit map (`corpus/README.md:12`) stand as
written. What moves is the `--selftest` receipt — 166 → 167 cases, plus a named stderr diagnostic where the
resolver used to fail without a word — and that is a test surface, not a reading of the host. Two limits stay
named. The new `SELFTEST_FD_BAND` override (`:2082`) is an unvalidated environment input read only by
`selftest_base_dir`, whose only production caller is `run_selftest` (`:2112`), so it can narrow the alias band
in a test and never reaches a probe arm. And no current `SKILL.md` line declares either count — the highest one
it declares is the `154 cases` line inside the round-45 census-readers block (`SKILL.md:4259`) — so this note
records the count without asserting a SKILL expectation.

C1 admission: `corpus/knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3 are admitted round 49 — the fresh
18-seat w1 cohort re-read the corrected rows `holds` with distinct bodies and the frozen counter passes all
six legs — so the rows leave the pending state that the round-45 and round-46 gate sections recorded.
```

## Findings for the L1 (not repaired here, not this seat's surface)

1. **The Registry's OUT-001 pointer is still a bare range.** `corpus/knowledge/adjacency-anchors-r19.json`
   keeps `"province_pointer": "../mori-shokunin/PROVINCE.md:6-16"` for OUT-001. C2's `bare_ranges` leg scans the
   seven ADJ ownership cells only (`tools/check-adjacency-table-r49.py:135` runs `BARE.findall` on that cell alone), so the claim is true as scoped and
   the registry is untouched — but a reader who generalises the round-49 note to "no bare ranges in the adjacency
   surface" would be wrong. The draft states the scope explicitly.
2. **`SELFTEST_FD_BAND` is an unvalidated environment input** (`tools/tsukuroi-census.sh:2082`). It cannot reach a
   probe arm today, but nothing validates its contents (a value naming a low descriptor would be `exec`-ed). It is
   recorded as a limit in the draft; a repair would be a lane decision.
3. **No `SKILL.md` line declares the current selftest count.** The highest count declared anywhere in the frozen
   `SKILL.md` is 154 (`:4259`), while the census at the base runs 166 cases (`.ufo/waves/round-49/frozen/FROZEN.md`
   C3 row). If the L1 wants the 167-case receipt pinned, that is a new SKILL append, not a correction of an
   existing line; the draft does not claim one exists.

## Artifacts

- `.ufo/waves/round-49/w1/R49ScribeReadme.md` — this report.
- `.ufo/waves/round-49/w1/R49ScribeReadme/append-candidate.md` — the drop-in block, sha256
  `4a44ff4f2884a3c53ccd45da433faca3dd4d782a567684d76af69cc82154928b`, 6 215 bytes.
- `.ufo/waves/round-49/w1/R49ScribeReadme/counter-with-draft.json` (3 881 B, sha256 `af8721d9…`) and
  `counter-summary.txt` (383 B, sha256 `fef53e96…`) — the C1 counter run with `--readme-file` at the freeze.
- `.ufo/waves/round-49/w1/R49ScribeReadme/marks-leg-tests.txt` (962 B, sha256 `894fbf67…`) — `marks_leg` on the
  draft, on the frozen README, and on five negation variants plus the FAIL-branch sentence.
- `.ufo/waves/round-49/w1/R49ScribeReadme/prefix-unchanged.diff` (0 B) — the append touches no existing README line.
- Tooling: nothing installed or upgraded (no need); no pacman transaction.
