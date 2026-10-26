VERDICT: draft

Seat DefCarried, item D-7 — round-38 disposition of the 8 routed defects in
`corpus/lessons/round-37-verifier-spotcheck.md` §6 (`:125`–`:132`), given that round 38 does not
re-claim the C1 child-env probe or the C2 journalctl counter. Deliverable: the table the round-38
lesson should carry (under "Proposed table").

## Method (read and run)

- Read `corpus/lessons/round-37-verifier-spotcheck.md:125-132` — the 8 routed defects, one per numbered line.
- Read `.ufo/waves/round-38/w1-spec.json` seat items and their self-identified defect numbers:
  DefDupBlock `:440` ("Item D-1 (round-37 closure routed defect 1…)"), DefFlip `:450` ("Item D-2 (routed defect 6)"),
  DefOwnWorkCopy `:459` ("Item D-3 (routed defect 7)"), DefJournalDebt `:469` ("Item D-3b (routed defect 3, depth debt)"),
  QualCriterion `:496` ("Item D-6", QUALITY criterion draft), ProbeLineage `:478` ("Item D-4", considerthese probe-lineage
  mining), RevLessonGateR37 `:684` ("Item R-9 … (routed defect 8)" cross-reference sentence).
- Read `SCORECARD.md:2117-2118` (round-38 C1 = storage-integrity census arm, counter sha256 `e649bfb3…`;
  C2 = ALPM hook order, counter sha256 `60e3635b…`, frozen capture MANIFEST) and `:2130-2131`
  ("Measured revision: the lane branch tip named in the round-38 outcome section, declared before the
  after-run; no self-assessment count is claimed this round.").
- Verified the non-re-claim premise from the lane itself, not only the dispatch:
  `git log --oneline -2 -- tools/check-journalctl-v262-corrections.py` → `d621b71`, `718cc8f` (both round-37);
  `git log --oneline -2 -- tools/probe-child-env-allowlist-r37.py` → `29b22df` (round-37);
  `git log --oneline 8bd001f..HEAD --name-only | grep -E '^(tools/check-journalctl|tools/probe-child-env)'`
  → no output (grep exit 1). No round-38 commit touches either counter.
- Lane tip at check time: `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` (`git rev-parse HEAD`). Round-38 commits:
  `7cbaeb6` freeze, `52ffd65` C1 arm, `1fe28e7` C2 entry, `9c9bb64` pre-seat amendment, `5edb6c2` registry rows.
  None applies a defect fix yet — the fixed dispositions rest on the wave items (drafts in flight), not on landed edits.
- Spot re-verification of defect subjects at the tip: duplicate correction headings still at
  `corpus/knowledge/journalctl-v262-field-filter-r36.md:129` and `:158` (grep `^## Round 37 correction` → 2 hits);
  S206/S207 still cite sibling paths at `corpus/SOURCES.md:215-216`; pending-closure lines at
  `corpus/lessons/round-37.md:24` ("Non-author sample: pending outside closure…") and `:105`
  ("Non-author closure remains pending…"); the `mount-errno-contract-r26.md` rejection paragraph at
  `corpus/lessons/round-37.md:74`.
- No scratch dir was needed (no clone, fixture or mutant; nothing to clean). No tool installed or upgraded.
  No lane file edited; no receipts to keep (all evidence is committed lane content or quoted command output).

## Proposed table (exact text for `corpus/lessons/round-38.md`)

Round-38 disposition of the round-37 spot-check routed defects (`corpus/lessons/round-37-verifier-spotcheck.md:125-132`).
Round 38 does not re-claim the C1 child-env probe or the C2 journalctl counter, so their defects are carried with the
prescription attached; the rest are covered by wave items or answered.

| r37 §6 | Routed defect | r38 disposition | Covered by / reason | Evidence |
|---|---|---|---|---|
| 1 | `corpus/knowledge/journalctl-v262-field-filter-r36.md` carries the round-37 correction block twice (headings `:129`, `:158`, introduced by `543a7ce`) | fixed-this-round | D-1 `DefDupBlock` drafts the append-only `## Round 38 correction — duplicate round-37 block` naming both headings, the introducing commit and which block is operative (no deletion) | spotcheck `:125`; w1-spec.json `:440-448`; note `:129`,`:158` at tip `5edb6c2` |
| 2 | `tools/check-journalctl-v262-corrections.py` has no freeze sha or kill rule and was amended twice after the change commit (`718cc8f`, `d621b71`) | carried | Round 38 does not re-claim the C2 journalctl counter (the round-38 C2 is ALPM hook order on a new, frozen counter), so the counter bytes stay untouched this round; the prescription — freeze the counter bytes and add the rejection-line-verbatim assertion — binds any future re-claim; round-38's own counters are declared with sha256 and kill rules, so the practice defect 2 asks for is now standard for new counters | spotcheck `:126`; SCORECARD.md `:2117-2118`; git log: last touch `d621b71` (round-37), no round-38 commit on the path |
| 3 | Depth debt from C24ActionOverride12: the reverse order (`--list-boots -F` → field list) and the `--list-boots --merge` error class (`journalctl.c:962-964`) are unrecorded | fixed-this-round | D-3b `DefJournalDebt` re-opens systemd v262 `journalctl.c` (around `:805-814` and `:962-964`) and drafts the append-only record of both behaviours with line citations | spotcheck `:127`; w1-spec.json `:469-476` |
| 4 | C1 re-claim: deliver one committed V8 mutant per fix, each reading `leaking > 0`; score V-B2 under V8, not V7; the `shutil.which`/`os.path.expandvars` ambient-PATH family needs a dynamic or value-provenance channel | carried | Round 38 does not re-claim the C1 child-env probe (the round-38 C1 is the storage-integrity census arm), so no V8 mutant wave runs this round; the V8-mutant-per-fix and dynamic-channel duties attach to any future re-claim; D-4 `ProbeLineage` builds the committed-bytes probe lineage table (the considerthese proposal) as supporting material, not the re-claim | spotcheck `:128`; SCORECARD.md `:2117`; w1-spec.json `:478-485`; git log: probe last touch `29b22df` (round-37), no round-38 commit on the path |
| 5 | C3 design: count cells coupled to same-round commits make a moving snapshot — bind the calibration predicate to an explicit final measured revision declared up front, or exclude same-round-mutated counts | fixed-this-round | D-6 `QualCriterion` drafts the QUALITY criterion (verdict follows the declared conjuncts and kill rules; findings outside declared conjuncts route as debt, not downgrades); the binding half is already enacted in the round-38 declaration: the measured revision is the tip named in the outcome section, declared before the after-run, and no self-assessment count is claimed this round | spotcheck `:129`; SCORECARD.md `:2130-2131`; w1-spec.json `:496-503` |
| 6 | The Gate rejection of `mount-errno-contract-r26.md` (`corpus/lessons/round-37.md:74`) lacks a flip condition, while the report says "with flip conditions" for both rejects | fixed-this-round | D-2 `DefFlip` drafts one precise flip condition (what evidence would change the reject) for the round-38 lesson Gate | spotcheck `:130`; round-37.md `:74`; w1-spec.json `:450-457` |
| 7 | S206/S207 own-work anchors are sibling-repo paths (`shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt`, `lane-errno13-probe.txt`) | fixed-this-round | D-3 `DefOwnWorkCopy` copies both captures byte-exact into the lane (seat dir, `cmp`+`sha256sum` verified) and drafts the append-only correction sentence giving the lane anchor path | spotcheck `:131`; SOURCES.md `:215-216` (sibling paths at tip `5edb6c2`); w1-spec.json `:459-467` |
| 8 | `corpus/lessons/round-37.md:24` and `:105` still say "Non-author closure remains pending" | answered | The closure file itself answers them: its §3 re-opened one admitted row and both rejects with agree/disagree and reasons, and `:132` states "This file answers them"; R-9 `RevLessonGateR37` drafts the exact cross-reference sentence the round-38 lesson carries | spotcheck `:132` (§3 table); round-37.md `:24`,`:105`; w1-spec.json `:684-691` |

## Per-row notes

- Defect 5 mapping nuance, stated honestly: the wave item D-6's prompt subject is the closure-vs-author
  downgrade disagreement; defect 5 is the C3 moving-snapshot design. They are the same defect seen from both
  ends — the author's C3 downgrade was the moving-snapshot complaint (`corpus/lessons/round-37.md:74-79`,
  "the after value moved from 0 to 5 mismatches during the round and required re-stating counts"), and the
  closure held the frozen predicate verified. Round 38 answers the design half by declaration
  (SCORECARD.md:2130-2131 binds the measured revision up front and drops self-assessment counts) and the
  verdict-discipline half by the D-6 criterion draft. With defects 2 and 4 carried and 8 answered, D-6 is the
  only remaining cover for defect 5.
- Defect 2's carried reason is observable in the round-38 declaration itself: both new counters carry declared
  sha256 digests and the declaration table has a Kill rule column (SCORECARD.md:2117-2118), and the pre-seat
  amendment adds a third counter (`tools/score-storage-arm-r38-q82.py`) under QUALITY 82 — the freeze-sha
  practice defect 2 demands is applied to everything round 38 freezes, while the round-37 journalctl counter
  itself is deliberately left untouched (git log evidence above).
- Defect 4's carried reason likewise: the round-38 C1 surface is btrfs storage integrity, not the child-env
  probe; the probe's last commit is the round-37 freeze `29b22df`, and no round-38 commit touches it.

## Not done / limits

- The five fixed-this-round rows are covered by wave items whose seat reports were not yet filed when this
  report was written (checked `.ufo/waves/round-38/w1/*.md`: no `DefDupBlock.md`, `DefFlip.md`,
  `DefOwnWorkCopy.md`, `DefJournalDebt.md`, `QualCriterion.md`; the listed peers were still running). The
  dispositions therefore rest on the wave-item definitions in `w1-spec.json`, not on completed seat outputs;
  the lesson should cite the seat reports once they land.
- I did not run either round-38 counter, did not re-open upstream sources, and did not verify the drafts'
  content (D-3b's seat re-opens `journalctl.c`; D-1's seat diffs the two blocks) — a disposition table needs
  the covering item to exist and address the defect, which the spec prompts show; the drafts' correctness is
  those seats' deliverable.
- I did not verify whether the round-38 lesson file exists yet or integrate this table into it (seats are
  read-only on lane content; the table above is the proposed text for whoever writes the lesson).
