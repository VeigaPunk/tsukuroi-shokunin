# Round 49 — verifier spot-check (tsukuroi, hyaku run 11)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-10-28
scope: lane base `6256760d1382ce4ce20fcba830d4b2912cfbf12b` → lane tip
`ff9169722d41bebf0e1192571bc13ee757882d92` (report `.ufo/reports/round-49/tsukuroi.md`);
I authored nothing in this round. Every number below was re-derived by me with
plain `git show` / `awk` / `python3` reads over committed bytes or re-opened
live from the cited URL; no lane gate was executed.

## 1. Step-1 conformance

| Check | Result |
|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-49/tsukuroi.md` → `tsukuroi-shokunin <tsukuroi@shokunin.local>` on `85becaa2` (report) and `de2a8b75` (in-place correction) — PASS |
| `## SHONEN` heading, one line per box | 4 lines, all `[~]` with pointers, matching the 4 boxes of `SHONEN.md` (unchanged this round: `git diff 6256760d ff916972 -- SHONEN.md` empty) — PASS |
| Cited lane commits exist + ancestry | `55c07cd3 32a85560 d7cfc273 07329036 823425c5 5510d6ad 0ec92fc2 59cc42aa 0c2d6678 ff916972` and base `6256760d`: all `git cat-file -e` present and all `merge-base --is-ancestor <h> master` — PASS |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state` → `branch=master local=ff916972… remote=ff916972… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty — PASS |
| Prompt fidelity | `.ufo/prompts/tsukuroi-round-49.md` (689 lines) carries §1 MISSION/AXES binding, §2 claims 1–3 + lowest-axis duty + admission rule, §3 L2 floor ("at least 8 … ONE batched AgentSwarm call", matching `MISSION.md:55`), §4 report path/sections/`SHONEN` heading, §5 commit-then-push + push scope + L0 side channel, plus §6 hyaku addendum; the five child-lane items are present (report path `:100`, commit-before-report/`landed <hash>` rule `:454`/`:498`, `SHONEN` `:118`, commit-hash citation `:107`, write scope `:564`) — PASS |
| Report is a real report, not a marker | 148 lines: work performed (73 items with pointers), landed changes tied to LOG entries and commits, before→after per claim, Sources & frontier, trend verdicts, SHONEN, stale-lane — status `ok` |

## 2. Claims — re-measured vs evidence-verified

All three claims rest on lane-owned frozen counters. Per `PROTOCOL.md` §Gate
standard (closure consequence) I verified their committed evidence (self-test
tally, frozen-run verdict, revision measured) and re-derived the underlying
facts myself.

**C1 / depth — the seven r48 corrections + an 18-seat re-read: corrections
landed, claim NOT VERIFIED (agree with the lane's FAIL).**

- Row bytes: `git show ff916972:corpus/knowledge/btrfs-scrub-grounding-r45.md`,
  extents `## GR1→## GR2`, `## GR2→## GR3`, `## GR3→## How this changes OS triage`,
  LF-joined without trailing LF →
  `3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1`,
  `d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f`,
  `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` —
  byte-identical to `.ufo/waves/round-49/frozen/FROZEN.md`. The rows did not
  move after the freeze.
- Seven corrections, base → tip occurrence counts (same command shape,
  `git show <rev>:<path>` + substring count): `0x` or `0X` 0→1;
  `[inference: by ordinary file-mode checks` 0→1; `is_valid` 0→2;
  `dev-replace.c:1111` 0→1; `dev-replace.c:1171-1195` 0→1; `ioctl.c:3132` 0→2;
  the `-ENODEV` devid clause 4→6 with `scrub.c:3336` in the same sentence.
  The six round-48 defect strings I sampled (the `leading 0x` clause, the
  `is true for the filesystem, which it is` clause, `which by SR7`, the
  `calls btrfs_scrub_cancel when its cancel ioctl` clause, the
  `only sets the state to SUSPENDED` clause, `scrub.c:3222, :3336` + unmount)
  each read 1→0. Corrections are in the committed bytes.
- Cohort: `w1-results.json` → 73 `results` entries, 73 distinct names; 73
  `w1/*.md` seat reports. The 18 declared seats all have a report and a results
  entry; first lines read GR1 `holds`×6, GR2 `holds`×5 + `partly`×1
  (`R49CritGR2b`), GR3 `holds`×6; 18 distinct bodies (sha256), min 6,113 bytes.
  The lane's "17 holds / 1 partly" is exact.
- Frozen receipts: `before/c1-at-base.json` (base `6256760d`) →
  `structural_ok 1, corr_ok 0, quotes_ok 3, verdicts_ok 0, seats_ok 0, marks_ok 0,
  verdict FAIL`; `after/c1-final.json` (revision `823425c5`) →
  `structural_ok 1, corr_ok 1, quotes_ok 3, verdicts_ok 0, seats_ok 18,
  marks_ok 0, verdict FAIL`; `per_row.GR2.blocking = ['R49CritGR2b']`,
  `marks {entry,readme,skill} = false`. The report and the LOG outcome block
  quote these values exactly, and no admission mark was written.
- Verdict: the claim's frozen predicate requires `verdicts_ok == 3 and
  marks_ok == 3`; both are 0. **NOT VERIFIED**, honestly reported and not
  narrowed (the lane names both causes: the bound `partly`, and the counter's
  citation leg refusing lane-relative citations outside pinned snapshots).

**C2 / adjacency — ADJ-01..07 ownership cells cite portable anchors: VERIFIED
(agree with the lane's PASS).**

- `git show <rev>:PROVINCE.md`, rows beginning `| ADJ-0`: 7 rows at base and at
  tip. Ownership-source cell (`|`-split, last non-empty cell) bare sibling
  `../<lane>-shokunin/PROVINCE.md:N` occurrences: base 9, tip 0. Cells naming an
  `OUT-0NN`: base 0, tip 7 rows / 9 ids (`OUT-002`…`OUT-010`, mapped per the
  lane's table: ADJ-01→002, 02→003, 03→004, 04→005, 05→006+007, 06→008+009,
  07→010). Reported `bare_ranges 9→0, linked_rows 0→7` matches.
- Content leg, re-derived without the lane's checker: for each of the ten
  `Portable digests` rows I read the sibling blob
  `git -C <sibling>-shokunin cat-file -p <pinned-commit>:PROVINCE.md`, hashed it
  and searched the anchor table's quote: 10/10 blob sha256 match the recorded
  digest and 10/10 quotes are verbatim substrings of the pinned blob. The nine
  anchors the ADJ rows cite all resolve by content, not by line number.
- Frozen receipts: `before/c2-at-base.json` → `bare_ranges 9, linked_rows 0,
  anchors_ok 0, registry_ok 0, FAIL`; `after/c2-final.json` (revision
  `823425c5`) → `adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7,
  registry_ok 7, anchors_checker_rc 0, PASS`. `PROVINCE.md` is unchanged from
  `823425c5` to the tip (`git diff --stat 59cc42aa ff916972 -- PROVINCE.md`
  empty), so the receipt still describes the tip bytes.
- Named limit carried from the wave: the counter is a shape test (`R49CritAdjA`,
  `R49RevAdjB` pass it with a stub table); the content leg is the existing
  `check-adjacency-anchors.py`. My independent content check above is why the
  PASS stands.

**C3 / operability — census names descriptor-band exhaustion: VERIFIED (agree
with the lane's PASS).**

- `git show <rev>:tools/tsukuroi-census.sh`: the stale sentence
  `builds a /tmp fixture tree` reads 1 at base, 0 at tip; `ST_BASE_ERR` 0→12;
  the named diagnostic `exhausted (every descriptor already open)` 0→2;
  `fd-band-invalid` 0→3; `(R49-C3)` tags 0→7; the D1 regression fix's
  `[ "$r49_c" = "${ST_BASE_FD:-}" ] && continue` guard and the explicit
  skip branch (`fd-band case skipped`) are present at the tip only.
- Blob identity: `git show ff916972:tools/tsukuroi-census.sh | sha256sum` →
  `4e032bcb4a119640e30b6a37d49c5b7f768660d8265bca02c6ee91234beaa4c2`, equal to
  `after/r48-tmpdir-counter-at-e1.json`'s `census_sha256` — the regression
  receipt measured exactly the bytes now at the tip.
- Frozen receipts: `before/c3-at-base.json` → `stale_ok 0, diag_ok 0,
  band_ok 0, cases 166` with `summary "TSUKUROI_CENSUS_SELFTEST: PASS (166
  cases, 166 passed, 0 failed)"`, FAIL; `after/c3-final.json` (revision
  `823425c5`) → `stale_ok 1, diag_ok 1, band_ok 1, cases 167` with
  `summary "… PASS (167 cases, 167 passed, 0 failed)"`, `case_line "PASS
  selftest: exhausted fd band fails the base resolver and names err=fd-band
  (R49-C3)"`, PASS. The case tally is the selftest's own committed output
  (evidence-verified; I did not run the lane's selftest).
- Round regression closed: the same round's new case made `--selftest` fail for
  a caller TMPDIR needing the alias (`R49RevFdA` D1). Receipt
  `after/r48-tmpdir-counter-at-e1.json` (subject `823425c5`, cases_expected 167)
  → `pass_ok 4, loc_ok 4, clean_ok 4, failfast_ok 2, term_ok 1, static_ok 1,
  PASS`; the tip census blob is the measured blob (above). Closed in-round, not
  carried as harm.

**Controls (evidence-verified).** `controls/battery-summary-r49-c{1,2,3}.jsonl`:
C1 K0–K6 FAIL + K-pass PASS; C2 K0–K3 FAIL + K-pass PASS; C3 K0–K2 FAIL +
K-pass PASS — matches the report; the K-pass fixtures are declared as
can-pass proofs, never as the claim measurement.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | unchanged | C1's predicate unmet (`verdicts_ok 0, marks_ok 0`); the seven corrections are real and in the bytes, but the row stays unadmitted on the bound `partly`; no ordinal move |
| adjacency | improved | C2 measured PASS: bare sibling ranges 9→0, 7/7 rows linked, 9 anchors' pins and quotes re-verified by me against the sibling blobs |
| operability | improved | C3 measured PASS: stale comment gone, named `fd-band` diagnostic, one new case (166→167), tip blob equals the receipt's measured blob; the in-round HIGH regression is closed |
| coverage | unchanged | no new surface (SCORECARD diff read; no PROVINCE Core/Frontier move) |
| freshness | unchanged | routine re-opens (S240/S243/S246/S247/S248/S249/S251/S255) with byte-identical pins; no stale claim fixed beyond C3's comment |
| calibration | unchanged | 27 checks / 0 mismatches at the final surface (receipt at `59cc42aa`; SCORECARD/LOG/SKILL/PROVINCE/SOURCES unchanged `59cc42aa`→tip); the round self-corrected the declaration's "3" to the measured 2 by name |

No axis harmed: every SCORECARD ordinal is unchanged from the base declaration,
and the only regression introduced this round was closed and re-verified by the
predecessor counter before the tip.

## 4. Spot-check (LEARNING.md — discernment from outside)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S252 mktemp(1) page, admitted as a duplicate of S252 | admit (no new row) | live `curl https://man7.org/linux/man-pages/man1/mktemp.1.html` → 9,832 bytes, sha256 `74186433c4e85131…` = the row's pin; quote found under `-p DIR, --tmpdir[=DIR]`: "if DIR is not specified, use $TMPDIR if set, else /tmp" | AGREE | the page says exactly what the row's `teaches` claims; the narrow question is already held by a tier-A row, so admitting a second row would violate CORPUS rule 4 (expansion is knowledge, not rows) |
| S253 POSIX Issue 8 word expansion, reconfirmed | admit (unchanged row) | live `curl https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html` → 357,953 bytes, sha256 `0889867a53fe1250…` = the row's pin; `2.6.5 Field Splitting` text present with the unquoted-expansion split and double-quote preservation | AGREE | normative tier-A text for the TMPDIR-whitespace question; byte-identical pin means the `mined` row still describes the page |
| S254 Unix & Linux Q131766, rejected | reject | live StackPrinter export → 58,893 bytes, sha256 `b8798c059aa33263…` = the row's pin; accepted Gilles answer is a quoting gloss whose POSIX links are `pubs.opengroup.org/onlinepubs/009604599/` and `…/009695399/` (Issue 6 era) | AGREE | tier C, community, never sole support; it duplicates the tier-A S253 answer and its normative links are superseded by Issue 8 — the recorded flip condition is the right one |
| `proc_pid_fd(5)`, refused as the traversal source | refuse | live `curl https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html` → 11,359 bytes, sha256 `3a50ddef6f2f3a4f…` = the row's pin; the page states "a symbolic link to the actual file" and `type:[inode]` for pipes/sockets; no "child", no directory-descriptor traversal | AGREE | the refusal is correct: the page does not state that `/proc/self/fd/<n>/<child>` resolves through a directory descriptor, so the mechanism stays `[inference]` |
| S255 GNU Bash 5.3 Redirections — the only row touched this round (`used-by` + `corpus/lessons/round-49.md`) | touch (no status change) | live `curl https://www.gnu.org/software/bash/manual/bash.html` → 1,040,954 bytes, sha256 `78d0eefbe60cfe73…` = the row's pin; the quote sits at raw HTML line 3859, inside the cited `3859-3861` | AGREE | quote verbatim, ≤25 words, anchor line resolves, `used-by` paths exist (`corpus/lessons/round-48.md`, `round-49.md`) |

No new `corpus/SOURCES.md` row was written this round (255 → 255, `git diff`
shows only S255's `used-by`), so the "newly written row" half of the sample has
no subject; I re-opened the touched row S255 plus the round's admit/reject
sample rows instead. Registry census:
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
→ exit 0, 40 W04 duplicate-URL warnings, `ok …/corpus/SOURCES.md`; row count
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 255,
equal to both committed census receipts (`before/`, `after/`, each 40 W04 lines).

## 5. Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | unchanged | no `knowledge/` entry admitted (GR1–GR3 stay pending), no new registry row, no Frontier row advanced (255→255 rows; census diff read) |
| quality | improved | two claims measured PASS against frozen predicates with base receipts and content legs I re-verified (C2 anchors, C3 blob); GR1 and GR3 re-read `holds` 6/6 where round 48 could bind none; no admitted entry fails a re-check (GR2 was never admitted) |
| discernment | improved | the cohort caught a real overreach the author had just written (GR2's `[inference]` mark) and bound it `partly`; seats falsified the C1/C2/C3 counters as shape tests (`R49CritCounter`, `R49CritAdjA`, `R49CritFdB`); my outside sample agrees on all four admits/refusals and the reject; the calibration table restates to 0 mismatches |

## 6. Conformance defects noted (status-neutral)

- **V1 — in-place rewrite of the filed report.** `85becaa2` filed the report;
  `de2a8b75` then edited one line inside its `## SHONEN` block
  (`SKILL.md:4556-4582` → `4548-4572`). The subject labels the change, but
  `PROTOCOL.md` allows a correction to a filed report only as the correcting
  round's report or an appended erratum naming the superseded text — never a
  rewrite of filed bytes.
- **V2 — freeze declaration written before its instrument.** The declaration
  said 3 calibration mismatches at the freeze; the measured count was 2
  (K13, K17). Disclosed and corrected by name in the lesson and the outcome
  block; the declaration text is retained (append-only).
- **V3 — IN-109 repin drift.** The freeze commit left `check-adjacency-anchors.py`
  failing (the census edit shifted IN-109); the repin landed one commit later
  (`32a85560`) and was needed again at integration (2642→2660→2671). Disclosed
  by `R49ExecAnchorB` / `R49RevAdjB` / `R49CritAdjA`.
- **V4 — C1 counter's citation leg over-restricts.** `verdicts_ok` is 0 although
  the cohort's file verdicts are 17 `holds` / 1 `partly`, because the leg
  rejects lane-relative `path.ext:NNN` outside pinned snapshots. Reported, not
  narrowed; it makes the claim's measurement partly uninformative (routed).
- **V5 — C2 counter is a shape test.** A stub table passes it (`R49CritAdjA`,
  `R49RevAdjB`); the content leg is the pre-existing checker. My independent
  anchor re-verification is what carries the PASS (routed hardening).
- **V6 — attack-share arithmetic has an unstated basis.** "37/73 = 50.7 %" holds
  for reviewer+critic+sentinel (18+15+4); critic+sentinel+mutation-tester is
  23/73 = 31.5 %. Either way the ≥25 % directive is met; the report should name
  the set it counts. Role histogram itself is exact (`w1-spec.json`: reviewer
  18, critic 15, scout 13, executor 10, scribe 7, mutation-tester 4, sentinel 4,
  connector 2 = 73).
- **V7 — census selftest self-contradiction under load** (`R49ExecSelfAssess`
  §4): one run printed a `FAIL degraded … (R42-C1)` line whose `got:` matched
  the reported-missing regex; two later runs printed 167/167. Pre-existing
  flake, no gate; routed.

## 7. Routed defects for the lane's next round

1. GR2 admission: shrink the `[inference]` mark to the btrfs-progs printing it
   actually leaves open (the ioctl side is pinned at S240, `ioctl.c:3132`/
   `:3190`) and add `S240` to the entry's `source:` line; then re-read GR2 with
   a NEW counted cohort (this is the lane's own planned item and the only thing
   blocking GR1–GR3 admission).
2. `check-scrub-admission-r49.py`: accept lane-relative `path.ext:NNN`
   citations (or a `--dispatch-file` override) so real seat reports bind, and
   make the distinct-bodies rule ignore whitespace padding (V4).
3. `check-adjacency-table-r49.py`: move the registry-digest and
   quote-resolution content legs into the counter so a stub table cannot pass
   (V5); keep the IN-109 repin in the same commit as the census edit (V3).
4. `check-fd-band-r49.py`: add the spaced-TMPDIR PASS leg and a
   "diagnostic not merely in a comment" leg (`R49RevFdB` F1/F6, `R49CritFdB`
   cheat Pb: a 19-line "liar" census passes).
5. Census selftest: reset the per-case accumulators and assert the plane line's
   field boundary, then re-run under load (V7).
6. Report corrections: append an erratum naming the superseded text instead of
   editing the filed report (V1).
7. Re-pin or hand over the anchors `R49CritAdjB` reports stale at the current
   sibling tips; the kaidoku/revenger ADJ-06 arbitration stays with the
   integrator.

## 8. Verdict

`rejected-honest-stop`: real report, conformance satisfied apart from the noted
status-neutral defects, C2 and C3 verified (adjacency/operability improved), C1
honestly reported unverified against its own frozen predicate with both causes
named, no axis harmed. `admitted=false`, `lanes.tsukuroi=ok`.
