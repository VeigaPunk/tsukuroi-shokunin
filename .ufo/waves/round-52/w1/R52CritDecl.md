VERDICT: defect-found

# W-D1 — declaration attack

Axes: calibration, declaration. All code references below name bytes at `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`, unless explicitly marked otherwise. These are critic findings, not an admission decision. No tracked lane content was changed.

## (a) Predicate text — holds; implementation qualifications below

Exact string comparison against FROZEN.md returned True for C1, C2 and C3. C1 has `PREDICATE` at `tools/check-scrub-admission-r52.py:87-88`; C2 uses the declared string inline at `tools/score-counter-cheats-r51.py:181` and in its docstring at :26 (not a named PREDICATE constant); C3 has its constant at `tools/check-adjacency-table-r51.py:86-91`.

Every one of the seven FROZEN-hashes.txt entries matched SHA256 of `git show ff9470ea:<path>` bytes. `--section-hash` at ff9470ea returned structural_ok=1 and exactly the three published GR hashes. `git diff --stat 6abef5d0edd19e0c6d21870b6add3b4c71c5ea68 ff9470ea -- corpus/knowledge/btrfs-scrub-grounding-r45.md` was empty.

**Qualification: “exactly four round bindings changed and no logic change” is incomplete.** Besides the listed bindings, r52 adds `LANE_FILES['check-scrub-admission-r52.py']` (:104) and changes receipt counter identifiers. The new artifact entry has a behavioral consequence: an out-of-range citation to that basename now disqualifies a report instead of being ignored as an unknown basename. My fixture returned FAIL, verdicts_ok=2, with `check-scrub-admission-r52.py:9999 outside tools/check-scrub-admission-r52.py (418 lines)`. The attempted whole-r51 comparison was inconclusive because its R51 seat universe/marks did not match the R52 fixture; do not treat that attempt as an equivalence test.

Smallest safe correction text: “The target predicate and admission algorithm are retained; round-specific bindings, receipt identifiers and the lane-artifact citation map are updated. The new r52-counter basename is now resolution-checked.” Do not claim literal behavioral identity.

## (b) Skip-the-wave reachability — disclosed measurement tradeoff, not evidence of surface improvement

**C1: holds for an honest skip.** The committed before receipt has structural_ok=1, lint_ok=3, quotes_ok=3, verdicts_ok=0, seats_ok=0, marks_ok=0, FAIL. No cohort artifacts means no admission. Synthetic fixture PASS is not proof that a genuine cohort ran; authorship is a process trust boundary, not independently authenticated by this counter. The FROZEN file-binding rule and synthetic K-pass disclosure already describe much of that boundary. I do not count a fabricated wave as a literal do-nothing control.

**C2: numerical target reachable without any round-52 byte work.** I actually ran:

`TMPDIR=/fast/scratch/hyaku/tsukuroi-r52/R52CritDecl/c2base python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-counter-cheats-r51.py --revision cc88b81d78bcbe06bce3f6bf722a108432ad276f --scratch /fast/scratch/hyaku/tsukuroi-r52/R52CritDecl/c2base/scr`

Observed PASS: real_pass=1, cheats=5, cheats_rejected=5, r50_cheats_rejected=0; all r50 rows PASS, all five r51 cheats FAIL rc=1, r51 real PASS rc=0. Receipt: `R52CritDecl/c2-at-base.json` beside this report. The relevant census, matcher and scorer paths have no base-to-freeze diff.

**C3: numerical target already reachable at base and freeze.** I ran the named counter at ff9470ea with TMPDIR in my scratch and the canonical lane argument. It returned rc=0, mode=measurement, PASS, all twenty declared legs satisfied. Comparing this receipt with before/c3-at-base-r52.json found only the revision field different; the other top-level values and predicate agreed. Receipt: `R52CritDecl/c3-at-freeze.json`. PROVINCE.md and the registry are not among base-to-freeze changed files.

Thus a seat can skip the wave and obtain green C2/C3 measurements. Their kill rules reject broken runs/regressions, but do not require wave activity. **However, these base/freeze receipts do not by themselves satisfy the full declared claim of measurement at the later integrated revision.** The declaration explicitly labels these instrument-measurement-completion claims. Treat this as a disclosed tradeoff: producing the correctly bound later receipt is the deliverable, not evidence that census or adjacency content improved. I am not rejecting that declared tradeoff or replacing the canonical judge.

Smallest safe clarification text: “C2/C3 numerical predicates are reachable on pre-wave bytes. Completion requires fresh receipts whose revision equals the single named post-wave integration commit, plus the declared battery/kill-rule checks. These claims do not establish a content improvement.”

## (c) Universal/process clauses not fully enforced — defects

### C1: “no negation word governs” is a finite string guard

`tools/check-scrub-admission-r52.py:82` enumerates only `unadmitted|not admitted|never admitted|stay pending|stays pending`; :310-319 applies it to the README sentence.

Counterexample README sentence:

“The btrfs scrub grounding entry `btrfs-scrub-grounding-r45.md` is not yet admitted round 52 and stays in review.”

An otherwise passing synthetic fixture with precisely that sentence returned rc=0, PASS, marks={entry:true,readme:true,skill:true}, verdicts_ok=3, seats_ok=18. Control with an affirmative sentence also PASSed. Inputs/reproducer: `R52CritDecl/fx2.py`. This is a fixable false-admission-mark defect, not a semantic-entailment tradeoff.

Smallest safe correction: require an exact affirmative admission sentence, rather than claiming the five-pattern blacklist recognizes every governing negation. Exact declaration text until any properly re-frozen instrument change: “The current README guard rejects only its enumerated phrases; acceptance additionally requires the canonical affirmative admission sentence, with no qualification or negation.”

### C1: “dispatch carries it once” is not checked

`dispatch_tasks()` at :263-267 collapses the task list into a name-to-role dict. A duplicate `R52RevGR1a` with the same reviewer role was accepted: rc=0 PASS, seats_ok=18. A conflicting duplicate placed last instead produced seats_ok=17, demonstrating last-wins behavior rather than multiplicity validation. The actual dispatch inspected had 64 tasks and 64 unique names, so no current duplicate was found.

Smallest safe correction text: “Acceptance separately requires exactly one dispatch-list occurrence per expected seat; the frozen counter checks only the role after dictionary collapse.” Fix the instrument in a newly declared revision, not by silently changing this freeze.

### C1: blocking behavior is broader than the declared negative-only description

At :304-306, ANY_VERDICT_RE scans the report body and converts any different row/verdict token into a blocking partly. A GR1 body mentioning the positive token `ROW GR2 VERDICT: holds` returned FAIL, verdicts_ok=2, seats_ok=18, while the otherwise identical control PASSed. Reproducer: `R52CritDecl/fx.py`.

This is a false-block risk, not a bypass. Smallest safe clarification text: “Any body occurrence matching `ROW GR<n> VERDICT: <word>` that differs from the report's own row/verdict blocks its row, including positive references to another row.” Do not soften an actual counted negative because of this finding. The live reviewer reports inspected had no body verdict tokens; they are mutable working-tree observations, not frozen claim evidence.

### C2: kill rules are stronger than the scorer's PASS predicate

At `tools/score-counter-cheats-r51.py:175`, only FAIL/rc=1 counts as rejection. r50 ERROR rows therefore produce r50_cheats_rejected=0. The inherited broken receipt concretely exhibits zero r50 rejections alongside ERROR rows. A synthetic in-process probe replacing only `score()` results with r51 real PASS, five r51 cheat FAILs, and all six r50 rows ERROR made the scorer return rc=0 PASS with all four numeric predicate fields satisfied. This probe is a unit-level arithmetic demonstration, not a real measured receipt.

The declaration's explicit **any ERROR row** kill rule closes that gap if applied to detail; the scorer's own verdict does not implement it. Likewise :179 and :182-183 allow `--skip-r50` to emit null for the r50 field while permitting PASS. The declared literal predicate rejects null, so checking fields closes that route. My full skip-r50 run was canceled and produced no usable result; that finding is source-derived, not an exercised PASS.

Scratch integrity/ordering also requires an external run record: the scorer receipt has no scratch identity and removes its temporary work directory (:188). These are process clauses, not counter-enumerated facts.

Smallest safe acceptance text: “Accept only the literal predicate over receipt fields, r50_cheats_rejected an integer zero, no skipped sensitivity run, no ERROR detail row, and an external command/lifecycle record establishing undisturbed scratch. Scorer exit 0 alone is insufficient.”

## (d) Before receipts — holds, with provenance wording correction

The values quoted in the declaration agree with the committed before receipts:

- C1: lint_ok=3, quotes_ok=3, verdicts_ok=0, seats_ok=0, marks_ok=0, FAIL; stored rc=1.
- C3: all twenty conjuncts satisfied, live_quote_ok=9, r50_blind=1, PASS; stored rc=0; revision=cc88b81d. Its separate base field c0ad548a is the reused counter's internal base, not a conflicting measured revision.
- Registry coverage: registered=88, rows_total=88, tools_total=88, PASS.
- Self-assessment: checked=27, mismatches=3; K08 stated4594/observed4605, K09 stated1326/observed1337, K10 stated75/observed77. Freeze receipt: 27/0 PASS. Frozen tree counts independently matched 4606 SKILL lines, 1338 table lines, 78 lesson files, 67 direct knowledge Markdown files, 522 README lines.
- sources-census-start.txt ends in an `ok` row. No separate exit-code receipt was found, so I did not independently establish the actual historical exit status solely from that text.

Provenance wording defect: `git show ff9470ea:.ufo/waves/round-51/before/c2-cheats-at-amend1.json | wc -c` returned **0 bytes**. The inherited ERROR-row copy is 1157 bytes, not those committed bytes. The post-hoc round-51 lesson accurately distinguishes committed-empty from working-copy ERROR rows. Exact correction: “The round-51 committed amend1 receipt is empty; recovered working-copy ERROR-row bytes are preserved under inherited/.” The historical four-cheat base receipt also exists and PASSes its older predicate; it is not a valid receipt for the amended five-cheat target.

## Scope / evidence limitations

I exceeded the item's read/grep-oriented execution scope by running counters/scorers and scratch synthetic probes. These supplemental probes are explicitly labeled above; none is a canonical judgment or the claim measurement. I also used temporary files under /tmp in two earlier comparisons, contrary to the scratch guard; those files were removed. No tracked lane/fleet file, index, branch or config was modified. No tools installed. The full base C2 run completed before I started the skip-r50 run; the latter was canceled, with no remaining matching scratch processes observed. All scratch is removed after copying the named receipts/reproducers.

Self-evaluation: accuracy 4/5 (synthetic/source-derived results explicitly separated); completeness 4/5 (all a-d covered; historical census exit not independently evidenced); clarity 4/5 (findings separated from disclosed measurement tradeoffs); actionability 4/5 (exact text corrections provided); conciseness 3/5 (supplemental probe coverage enlarged the report). Overall 3.8/5. Main should prioritize the README-negation and dispatch-multiplicity defects; do not treat base-green instrument receipts as proof of a post-wave completion claim.
