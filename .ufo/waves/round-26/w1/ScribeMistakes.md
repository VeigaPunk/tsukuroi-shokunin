# Round 26 — Mistakes table draft (ScribeMistakes, wave 1)

Seat: `TsukuroiR26.ScribeMistakes`. Read-only lane seat; the lane was not edited. Author: `hyaku` closure scribe, non-author integrator (no author-side self-grading).

Scope of this seat: mine the mistakes recorded in `corpus/lessons/round-25-verifier-spotcheck.md` (routed defects 1 to 8), `corpus/lessons/round-25.md` (`## Mistakes` and the later sections) and the round-25 git history, then draft the `## Mistakes` table for `corpus/lessons/round-26.md` with, for every row, the existing `QUALITY.md` criterion that should have caught it (or `none`) and a fix that can be shown able to fail — a command whose output was red before the fix.

Installs: none. All commands read committed git objects or the lane working tree; no pacman transaction, no service action, no host mutation, no git write command against the lane.

## Verdict

Done, with one divergence the L1 must resolve: the three required rows are reproduced with a red-before command each, but the round-26 C2 base value declared as "3 of 27 (K10, K24, K26)" is **not** what the pinned v2 tool reports at `e9f5356c`; it reports **5 of 27** (K02 and K06 added). The lane's own appended refinement already records this supersession, so the claim is not falsified, but the *declaration text* still carries the stale prediction and the lesson's `## Mistakes` table does not carry a row for it.

## 1. R26-UNDISCLOSED-INPLACE — the `SCORECARD.md:51` in-place edit

**Holds** — the defect is real, reproducible and still unrepaired in the round-25 record.

Evidence pointer:

- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff b9046016 157ee255 -- SCORECARD.md | grep -c '^-[^-]'` → exit 0, output `1`. The single removed line is the round-11 axes table's calibration row.
- Original wording at `b9046016`, `SCORECARD.md:51`: ``the claim→re-measure→append→supersede→rule loop with its mismeasure rows``. After `c93bd70f`, `SCORECARD.md:51`: ``the claim→re-measure→append→supersede→rule loop for rounds 1 to 9``.
- `grep -c 'mismeasure rows' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-25.md` → exit 1, output `0`: the removed wording is quoted nowhere in the round-25 lesson.
- `grep -c 'SCORECARD.md:51' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-25.md` → exit 1, output `0`.
- `corpus/lessons/round-25.md:82` is the heading `## Record of the one in-place edit (appended after wave 2)`; line 84 names only `SHONEN.md` box 2. The heading's own claim ("the one in-place edit") is therefore false.

**Existing criterion that should have caught it: `none` at the lane's `QUALITY.md`, and that is the finding.** `grep -n /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md` shows the two candidates and why neither fires:

- criterion 4 (`corpus/QUALITY.md:7`) `Errata are append-only blocks.` — it constrains *how* an erratum is written, not *whether an edit is disclosed*. An in-place rewrite can satisfy it if the erratum is a block.
- criterion 2 (`corpus/QUALITY.md:4`) `Every claim carries a source: a measured anchor (path:line, command, evidence id) — never oral knowledge.` — the round-25 lesson's claim "the one in-place edit" is exactly an unanchored count: no command, no `path:line`, no scope. The count `1` was asserted, not measured. The lane's own `CORPUS.md:34` rule `A count carries its command.` names the same defect and was not in `QUALITY.md` either.

So the honest captured-by is **`none`**, with a new criterion required. The lane has since added one — `QUALITY 60` in the working-tree `corpus/QUALITY.md` (added at `ef72f10`) — but `60` is a *fix*, not a criterion that could have caught the round-25 defect, and its sweep has a blind spot (finding 5).

**Fix shown able to fail.** Draft check `tools/check-in-place-disclosure.py --base b9046016 --head 157ee255 --lesson corpus/lessons/round-25.md`: it diffs the lane's append-only surfaces, computes the wording each edit removed by word-level diff, and requires a lesson line that names the surface, anchors it to a line, and quotes the removed wording.

- Red before the fix (measured): exit **1**, `undisclosed_in_place_edits: 1`, the finding naming `SCORECARD.md`, `removed_segment: "with its mismeasure rows;"`, `disclosed_in_lesson: false`. The `SHONEN.md` edit is *not* a finding, because the round-25 lesson names it and quotes the changed token — the check discriminates, it does not merely count.
- Green after the fix: the round-26 lesson's in-place record names `SCORECARD.md:51` and quotes `with its mismeasure rows`, and the same command exits 0.

## 2. R26-GATE-RECORD-MISSING — S126 and S127 have no `## Gate` record

**Holds** — both rows are `mined` and cited by the entry, and neither has a lesson Gate record.

Evidence pointer:

- `awk -F'|' '/^\| S12[67] \|/' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-25.md | wc -l` → exit 0, output `0`.
- `grep -cE '^\| S12[67] \|' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md` → exit 0, output `2`. Both rows are `status=mined`, `opened=2026-10-22`, `recheck=on-release`, `used-by` = `corpus/knowledge/memory-pressure-r25.md, corpus/knowledge/memory-pressure-r25.json`.
- `grep -c 'S127' corpus/lessons/round-25.md` → exit 1, output `0` (S127 is named nowhere in the round-25 lesson). `grep -c 'S126'` → `1`, and that single hit is the Gate-errata paragraph at `corpus/lessons/round-25.md:72`, which mentions S126 as a side note and carries no URL, access date or located quote for it.

**Existing criterion that should have caught it: `none` in the lane's `QUALITY.md`.** The rule that binds is outside it: `CORPUS.md:112` (`SOURCES.md` → Rules → 1, "A row is a claim. Write it only after opening the source in the round that writes the row. The round lesson's `## Gate` records, for every new row, the URL, the access date, and a ≤25-word quote with its location grounding `teaches`."). The lane's `corpus/QUALITY.md` criterion 7 (`corpus/QUALITY.md:11`) requires an external claim to cite an exact `S###` row, tier and anchor — it does not require the row to have a Gate record. So the captured-by for the lesson's own table is best stated as **`none` (protocol rule `CORPUS.md` SOURCES rule 1)**, matching the committed lesson's row.

**Fix shown able to fail.** Draft check `tools/check-gate-record.py --revision 157ee255 --base-revision b9046016 --lesson corpus/lessons/round-25.md`: it computes the registry rows that are new relative to the claim base, and for each `mined` row requires a lesson Gate row carrying a locator, an ISO date, a quote of at most 25 words and a location.

- Red before the fix (measured): exit **1**, `new_mined_rows: 13`, `rows_without_gate_record: 2`, findings `S126` and `S127` with `gate_rows_in_lesson: 0`. The other eleven rows (S115 to S125) pass, so the check discriminates by row and does not flag the whole round.
- Green after the fix: the round-26 lesson supplies Gate records for S126 and S127 (the lane's `QUALITY 61` and the `SH-GATE-QUOTE-MISSING` finding in the pinned storage checker), and the same command exits 0.

## 3. R26-SELF-REFERENT-ORDINAL — K01/K04/K05 read the declaring round's own prose

**Holds** — at the round-25 head the ordinal checks were satisfied by round 25's own declaration and refinement prose.

Evidence pointer, measured in a clean sandbox built from the committed bytes (`git archive 157ee255` into a scratch tree, `git init`, one commit), so the v1 tool is the committed one and not the lane's working-tree v2:

- `python3 tools/check-self-assessment.py --revision <scratch-sha>` → exit 0, `checks 23`, `mismatches 0` — the check set passed.
- Yet `K01 observed_line 793`, `K04 observed_line 807`, `K05 observed_line 792`, and those lines are, at `157ee255`: `792` the C1 row of round 25's own declaration table (`| C1 self-assessment mismatch count ... | calibration 9 → 9 |`), `793` the C2 row of the same table (`| C2 memory-pressure reading ... | depth 8 → 8 (tied lowest) |`), `807` a bullet of round 25's own `### Round 25 declaration refinements` section. A round-25 declaration line cannot be a dated move record of round 25's own ordinal.
- Independent re-derivation, not reusing the lane's tool: draft check `tools/check-self-referential-ordinal.py --revision 157ee255` → exit **1**, `self_referential_resolutions: 3`, findings `K01` @793, `K04` @807, `K05` @792, each with `resolved_in_declaring_round_prose: true` and `resolved_in_measured_outcome: false`.
- The same defect at the round-26 base, measured with the lane's pinned v2 tool: `python3 tools/check-self-assessment.py --revision e9f5356c` → exit 1, `mismatches 5`; `K01` now resolves to `SCORECARD.md:730` and `K04`/`K05` to `:772`/`:771`, all inside `### Round 25 measured outcome` — dated move records. The v1 → v2 change is exactly the fix.

**Existing criterion that should have caught it: `QUALITY 57`** (`corpus/QUALITY.md:116`, present at the round-26 base `e9f5356c`): "…an axis score or count in the SCORECARD axes table, the Capabilities table or SHONEN.md is admissible only when its counting command, run at the named revision, reproduces it; **ordinals come from the latest move records, never from an old table**." The word *records* is the part v1 violated: it accepted plan prose as the record. The committed lesson's row says "QUALITY 57 (partly: it required re-measurement, not dated records)" — that is accurate and I keep it.

**Fix shown able to fail.** The v2 rule qualifies only SCORECARD lines inside a section whose heading carries `measured outcome`, from any round; an axis with no transition in any such section is a mismatch `no dated move record`, never a silent pass.

- Red before the fix (measured): the v1 tool at `157ee255` exits 0 with `mismatches 0` while resolving K01/K04/K05 to the declaring round's own declaration lines — a green result that certifies nothing. The independent checker exits 1 on the same revision.
- Green after the fix: the v2 tool at `157ee255` exits 1 with `mismatches 4` (`K02`, `K06`, `K24`, `K26`), and `K01`/`K04`/`K05` resolve to `:730`, `:772`, `:771` — measured-outcome lines.

## 4. R26-DECLARED-BASE-PREDICTION-WRONG — new, not in the committed lesson

**The C2 base value the declaration predicts is not what the pinned tool reports.** The round-26 declaration (`b13e991`, `SCORECARD.md` "Round 26 — declaration, attempt 1", the C2 row of the claim table) states the before-value as "the number the v2 tool reports at `e9f5356c` (hand count by the L1 predicts **3 of 27**: K10, K24, K26)".

Measured with the pinned v2 tool (`tools/check-self-assessment.py`, sha256 `77c946a91635ab76aa9869a786e4d206d37b3e52c00b80ec1f4c09a17be0c26d`, committed at `4de2b6b`):

- `python3 tools/check-self-assessment.py --revision e9f5356c` → exit **1**, `checks 27`, `mismatches` **5**.
- The five are `K02` and `K06` (`no dated move record for coverage` / `for adjacency`), `K10` (`depth row states 26 lesson files; corpus/lessons holds 27 files`), `K24` and `K26` (`corpus/knowledge/root-dac-decision-r12.md` carries a supersession marker at its line 7).
- The lane's appended declaration refinement already records the correction ("C2 before-value, measured: the v2 tool … reports 5 of 27 at `e9f5356c` … The hand prediction of 3 is superseded by this measurement"), so the claim is not falsified — the *before* column of the claim table still reads "3 of 27" and no `## Mistakes` row records the superseded prediction.

Root cause, measured independently: the v2 rule qualifies only `measured outcome` sections, and in the whole of `SCORECARD.md` at `157ee255` **no** measured-outcome section records a coverage or an adjacency transition (counted transitions in measured-outcome sections: depth 3, freshness 1, calibration 3, operability 3, coverage **0**, adjacency **0**). The stricter rule therefore turns two axes into `no dated move record` at the base. Under the *declared* (weaker) rule — exclude only sections naming the declaring round — coverage resolves to `SCORECARD.md:224` and adjacency to `:620`, and the base would indeed be 3. Draft check `tools/check-declared-vs-implemented-rule.py --revision e9f5356c` → `declared_rule_mismatching_axes: []`, `implemented_rule_mismatching_axes: ["coverage", "adjacency"]`, `rules_diverge: true`.

Fix shown able to fail: the declaration's before-cell must state the tool's measured output, not a hand count; the command `python3 tools/check-self-assessment.py --revision e9f5356c` is the check, and it exits 1 with `mismatches 5` — red against the declared "3".

## 5. QUALITY 60's sweep has a blind spot (finding for the L1, not a lesson row)

`QUALITY 60` (working tree, added at `ef72f10`) requires the sweep `git diff -U0 <base> <REV> -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md | grep -E '^-[^-]'` to equal the lesson's list of changed lines. Two measured weaknesses:

1. **It cannot see an edit made inside the round.** A base→head diff shows only net removals. `git diff -U0 b9046016 e9f5356c -- SKILL.md | grep -cE '^-[^-]'` → `0`, but `git diff -U0 5e7c04e c93bd70f -- SKILL.md | grep -cE '^-[^-]'` → **3**: round 25 rewrote three `SKILL.md` lines in place (the S120 digest copies) inside the round, and a base→head sweep cannot see them. Those three edits were disclosed only in prose (`corpus/lessons/round-25.md:72`, "the three copies in this round's SKILL.md section were corrected in place"), not by any sweep.
2. **Its file list omits `SKILL.md` and `PROVINCE.md`,** both of which round 25 and round 26 do edit.

A sweep that cannot see within-round edits and omits two edited surfaces is a sweep that can pass while a lane surface was rewritten. I recommend the lane either widen the file list and diff each round commit against its parent (`git log -p base..REV`), or state the limitation in the criterion text.

## Draft `## Mistakes` table for `corpus/lessons/round-26.md`

Column order per `CORPUS.md:171` (`class · evidence pointer · captured-by (the QUALITY.md criterion or protocol rule that should have caught it, or none) · fix`). The `class` values are the round-26 lane's own vocabulary; the `CORPUS.md:171` list (`vacuous, survivor, stale-premise, reference-drift, number-drift, scope, attribution, landing, provider`) does not include `disclosure`, `curation`, `measurement` or `tool` — worth a decision from the L1, since the round-25 lesson used `stale-premise` and `landing`.

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R26-UNDISCLOSED-INPLACE | disclosure | `c93bd70f` changed `SCORECARD.md:51` from "loop with its mismeasure rows" to "loop for rounds 1 to 9" (`git diff b9046016 157ee255 -- SCORECARD.md \| grep -c '^-[^-]'` → 1); the round-25 lesson's `## Record of the one in-place edit` (line 82) names only `SHONEN.md` box 2, and `grep -c 'mismeasure rows' corpus/lessons/round-25.md` → 0 | **none** — `QUALITY 4` (`corpus/QUALITY.md:7`) constrains erratum form, not disclosure, and `QUALITY 2` (`corpus/QUALITY.md:4`, "never oral knowledge") is the count-carries-its-command rule that `CORPUS.md:34` states and `QUALITY.md` lacks | `QUALITY 60` plus a lesson record naming `SCORECARD.md:51` and quoting the removed wording; `tools/check-in-place-disclosure.py --base b9046016 --head 157ee255 --lesson corpus/lessons/round-25.md` exits **1** with `undisclosed_in_place_edits: 1`, `removed_segment: "with its mismeasure rows;"` (the disclosed SHONEN edit is not a finding); it exits 0 once the lesson names and quotes the line |
| R26-GATE-RECORD-MISSING | curation | S126 and S127 are `mined`, `opened 2026-10-22`, `used-by corpus/knowledge/memory-pressure-r25.md{,.json}` (`grep -cE '^\| S12[67] \|' corpus/SOURCES.md` → 2) but have no lesson Gate row (`awk -F'\|' '/^\| S12[67] \|/' corpus/lessons/round-25.md \| wc -l` → 0; `grep -c 'S127' corpus/lessons/round-25.md` → 0) | **none** in `QUALITY.md`; the binding rule is `CORPUS.md:112` SOURCES rule 1 ("The round lesson's `## Gate` records, for every new row, the URL, the access date, and a ≤25-word quote with its location grounding `teaches`"). `QUALITY 7` (`corpus/QUALITY.md:11`) requires an exact row to be cited, not to carry a Gate record | `QUALITY 61`; `tools/check-gate-record.py --revision 157ee255 --base-revision b9046016 --lesson corpus/lessons/round-25.md` exits **1** with `new_mined_rows: 13`, `rows_without_gate_record: 2` (S126, S127; the eleven other new rows pass); it exits 0 once both Gate records are supplied |
| R26-SELF-REFERENT-ORDINAL | measurement | At `157ee255` the v1 checker exits 0 with `mismatches 0` while `K01 observed_line 793`, `K04 807`, `K05 792` — round 25's own declaration table (792, 793) and refinement bullet (807); independent re-derivation `tools/check-self-referential-ordinal.py --revision 157ee255` exits **1** with `self_referential_resolutions: 3` | `QUALITY 57` (`corpus/QUALITY.md:116`) — "ordinals come from the latest **move records**, never from an old table"; v1 accepted plan prose as the record | `QUALITY 62`; v2 qualifies only `measured outcome` sections. Red before: v1 at `157ee255` exits 0 and resolves K01 to the declaration line 793; green after: v2 at the same revision exits 1 with `mismatches 4` and resolves K01/K04/K05 to `:730`, `:772`, `:771`, all measured-outcome lines |
| R26-DECLARED-BASE-PREDICTION-WRONG | stale-premise | The C2 before-cell of the round-26 claim table says "hand count by the L1 predicts 3 of 27: K10, K24, K26"; the pinned v2 tool at `e9f5356c` reports **5 of 27** (`K02`, `K06` `no dated move record`, `K10`, `K24`, `K26`), exit 1. No measured-outcome section in `SCORECARD.md` at `157ee255` records a coverage or adjacency transition (measured-outcome transition counts: depth 3, freshness 1, calibration 3, operability 3, coverage 0, adjacency 0) | **none** — `QUALITY 55` (`corpus/QUALITY.md:108`) covers a stale *host-state* premise, not a stale hand count of a tool's own output | The before-cell states the tool's measured output, not a hand count. Red before: `python3 tools/check-self-assessment.py --revision e9f5356c` exits 1 with `mismatches 5`; the declared "3" is superseded by the measurement, as the appended declaration refinement already says. `tools/check-declared-vs-implemented-rule.py --revision e9f5356c` shows `rules_diverge: true` and names the two axes the stricter rule drops |

## Reproduction

Draft checkers (all read-only, all outside the lane, under `/fast/scratch/hyaku/tsuku26/ScribeMistakes/`):

- `check-in-place-disclosure.py --base b9046016 --head 157ee255 --lesson corpus/lessons/round-25.md` → exit 1, one finding (SCORECARD.md).
- `check-gate-record.py --revision 157ee255 --base-revision b9046016 --lesson corpus/lessons/round-25.md` → exit 1, two findings (S126, S127).
- `check-self-referential-ordinal.py --revision 157ee255` → exit 1, three findings (K01, K04, K05).
- `check-declared-vs-implemented-rule.py --revision e9f5356c` → `rules_diverge: true`.
- `red-states.py` → the consolidated evidence dump for rows 1 to 3.

The crash reproduction for routed defect 4 (`c93bd70f` `tools/check-memory-pressure.py` crashing on lesson prose with `AttributeError: 'NoneType' object has no attribute 'strip'` at `recheck_log`, triggered by `corpus/lessons/round-25.md:72` containing an S-id and the word `recheck` with no arrow; the lane reworded the lesson line at `d70af4a` rather than fixing the tool — `git diff --stat c93bd70f d70af4a -- tools/check-memory-pressure.py` is empty) was reproduced in a scratch tree and is reported as context only; the pinned storage checker supersedes that tool for round 26.

## Out of scope / not mine

The lane's own `## Mistakes` table (committed at `ef72f10`) already contains `R26-UNDISCLOSED-INPLACE`, `R26-GATE-RECORD-MISSING`, `R26-SELF-REFERENT-ORDINAL`, `R26-PREMISE-BEFORE-SOURCE` and `R26-GATE-COLUMN-OFFSET`. I did not re-derive the last two and do not dispute them. I did not touch the lane, did not write to `.ufo/state/` or `.ufo/watchdog.log`, and did not run any git write command against the lane.

## Findings the canonical judge should weigh

1. The declaration's C2 before-cell (3 of 27) disagrees with the pinned tool (5 of 27). The claim target is unaffected; the record is. Row `R26-DECLARED-BASE-PREDICTION-WRONG` is proposed above.
2. `QUALITY 60`'s sweep cannot see a within-round in-place edit and omits `SKILL.md` and `PROVINCE.md` from its file list. Finding 5 above.
3. The `CORPUS.md:171` class vocabulary does not contain `disclosure`, `curation`, `measurement` or `tool`, which the round-26 table uses. The L1 should either extend the vocabulary or map the four to the listed ones (`R26-UNDISCLOSED-INPLACE` → `attribution`, `R26-GATE-RECORD-MISSING` → `scope`, `R26-SELF-REFERENT-ORDINAL` → `vacuous`, `R26-GATE-COLUMN-OFFSET` → `survivor` are the plausible readings).

Scope: read=`corpus/lessons/round-25.md`, `corpus/lessons/round-25-verifier-spotcheck.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `PROVINCE.md`, `tools/check-self-assessment.py`, `tools/check-memory-pressure.py`, `/home/vgpnk/Projects/shokunin/CORPUS.md`, `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w1/mistakes.md`, git history `b9046016..e9f5356c` and `e9f5356c..7dfea92`; wrote=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/ScribeMistakes.md`, `/fast/scratch/hyaku/tsuku26/ScribeMistakes/{check-in-place-disclosure.py,check-gate-record.py,check-self-referential-ordinal.py,check-declared-vs-implemented-rule.py,red-states.py}` and scratch sandboxes `repro`, `repro2`, `v1` under the same directory; executed=`git diff`, `git show`, `git log`, `git status`, `git archive` (read-only, lane), `grep -n`, `grep -c`, `awk`, `sed -n`, `wc -l`, `python3 tools/check-self-assessment.py --revision 157ee255|e9f5356c`, `python3 tools/check-memory-pressure.py --revision <sha>` in scratch trees, and the four draft checkers listed above`

Model: not exposed

Installs: none
