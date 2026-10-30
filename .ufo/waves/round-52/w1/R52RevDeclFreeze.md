VERDICT: defect-found

# W-D5 — frozen declaration review

Revision reviewed: `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`. Axes: calibration, declaration. All numbered source citations below refer to `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:<path>`, not mutable tracked files. No tracked file changed; no counter or selftest executed.

## Findings, by severity

### Medium — C2's universal absence wording exceeds the enumerated evidence (item c: defect)

`.ufo/waves/round-52/frozen/FROZEN.md:29` says “no valid receipt exists anywhere”; `SCORECARD.md:3343` says “no valid receipt exists” and “the only committed one is broken”. The named scorer enumerates the census and counter blobs at one revision and twelve current counter/fixture jobs, not the universe of prior receipts (`tools/score-counter-cheats-r51.py:134-163`). The inherited files establish one specific failed attempt, not absence everywhere. This is an unsupported scope expansion, not evidence that some valid receipt actually exists.

Exact proposed replacement for the C2 do-nothing wording: “Skipping the run produces no new named-revision receipt. The preserved round-51 amend1 receipt is FAIL (real_pass 0, cheats_rejected 1/5, with ERROR rows); this round requires a fresh valid receipt in an undisturbed scratch.”

### Medium — C2's ERROR kill rule is stronger than the scorer's PASS decision (items a/c: qualification/defect)

Both declarations require killing “any ERROR row” (`FROZEN.md:29`, `SCORECARD.md:3343`). The scorer records each row's verdict/rc (`tools/score-counter-cheats-r51.py:167-171`), but increments r50 rejection only for FAIL/rc=1 (`:175-176`). Its PASS decision checks only real_pass, five fixtures, five r51 rejections, and zero r50 rejections (`:182-184`). Consequently an r50 ERROR does not itself fail the numeric predicate; it counts as zero rejections, just like the intended control PASS. This is static control-flow evidence, not an executed mutant. The human kill rule can still reject such a receipt, but the command's PASS alone does not certify that rule. Scratch non-disturbance is likewise an external condition, not an emitted leg.

Proposed declaration clarification: “The numeric predicate is necessary, not sufficient: independently inspect every detail row and reject any ERROR or invalid process result, and retain evidence that scratch was undisturbed.” Do not silently change this frozen counter during scoring.

## Per-item disposition

### (a) Predicates — holds for canonical formula identity; qualification above

- C1: `tools/check-scrub-admission-r52.py:87-88` PREDICATE exactly equals the sentence in `FROZEN.md:28` and `SCORECARD.md:3342`: `structural_ok == 1 and lint_ok == 3 and quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3`.
- C2: there is no named PREDICATE constant in this scorer. Its docstring `:26` and output's `predicate` literal `:181` exactly match both declarations: `real_pass == 1 and cheats == 5 and cheats_rejected == 5 and r50_cheats_rejected == 0`. Default decision `:182-183` implements those numeric legs; the declaration's additional ERROR/scratch requirements are not equivalent to that decision, as above. The assignment's named command does not use `--skip-r50`.
- C3: `tools/check-adjacency-table-r51.py:86-91` PREDICATE exactly equals `FROZEN.md:30`, including all twenty conjuncts ending `ancestry_ok == 10 and recipient_ok == 7`. `SCORECARD.md:3344` explicitly abbreviates it as `adj_rows == 7 … and recipient_ok == 7`; therefore SCORECARD is not literally the same sentence, but points to the full r51 predicate rather than declaring different numeric thresholds. Expanding the abbreviation would meet a strict literal-identity requirement.

Method: fetched the three frozen counter blobs with git show and parsed assignments with Python AST without importing/executing the counters. Direct string comparison returned C1 IN_FROZEN=True, IN_SCORECARD=True; C3 IN_FROZEN=True, IN_SCORECARD=False (the documented abbreviation).

### (b) Axes counts — holds

Observed frozen-blob/tree recount:

| Measure | Observed | Declaration |
|---|---:|---|
| SKILL.md newline count / wc -l | 4606 | SCORECARD.md:3366 |
| SKILL.md lines beginning literal `|` | 1338 | SCORECARD.md:3366 |
| Files recursively under corpus/lessons/ | 78 | SCORECARD.md:3366 |
| Immediate corpus/knowledge/*.md files | 67 | SCORECARD.md:3366 |
| corpus/README.md newline count / wc -l | 522 | SCORECARD.md:3367 |

Commands/data: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <FREEZE>:SKILL.md` and `:corpus/README.md` supplied bytes to `wc -l`, yielding 4606 and 522. Table count used `line.startswith('|')` on frozen SKILL bytes (1338). File census used `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree -r --name-only <FREEZE>`, filtered recursively for lessons and immediate `.md` children for knowledge (78, 67). This is a frozen-tree enumeration equivalent to the declared find scopes, not a count of mutable working-tree files. Numeric ordinals are unchanged at 8/9/9/9/9/8, saturation 9/window 3 is explicitly no waiver (`SCORECARD.md:3321-3322`); no all-axes-saturated claim occurs there.

### (c) Universal scope — defect, as above

The C2 absence claim is not enumerated by its command. The ERROR kill rule requires explicit receipt review beyond numeric PASS. The remaining measurement wording correctly distinguishes fixture K-pass from integrated-revision measurement (`FROZEN.md:69-70`) and discloses semantic limits (`:74-78`); this review does not certify those future measurements or a universal truth guarantee.

### (d) Inherited-residue description — holds for contents; deletion cause not independently established

Both directory listing and frozen tree contain exactly:
- `.ufo/waves/round-52/inherited/c2-cheats-at-amend1.json`
- `.ufo/waves/round-52/inherited/c2-cheats-at-amend1.rc`

Frozen JSON line 1 identifies revision `6abef5d0edd19e0c6d21870b6add3b4c71c5ea68`, `verdict: FAIL`, `real_pass: 0`, `cheats: 5`, `cheats_rejected: 1`, `r50_cheats_rejected: 0`; all six r50 detail rows are ERROR/rc=2, and r51 F4/F5 are ERROR/rc=2. The rc file line 1 says `exit 1`. Direct byte comparison of each inherited working file to its git-show freeze blob returned True. These receipts substantiate the declared broken attempt with ERROR rows (`FROZEN.md:11-12,29`; `SCORECARD.md:3343`). They do not, by themselves, prove the historical causal explanation of scratch deletion; that explanation is attributed to the lesson in `FROZEN.md:12`.

## Residual risk and verification gaps

LSP device unavailable: reading `xd://lsp` returned “No such tool”; semantic references/definition/diagnostics could not be requested. Frozen text/AST checks are not semantic-server proof. No selftest, battery, receipt-history-wide search, runtime rerouting or resume preflight exercised; none is certified by this scoped declaration review. No tools installed. Review scratch contained no fixture and is removed before yielding.

Self-evaluation: accuracy 4/5 (static ERROR-path result not reproduced); completeness 4/5 (counts use immutable tree enumeration rather than mutable find); clarity 4/5 (C3 literal abbreviation separately qualified); actionability 4/5 (proposed text preserves frozen scoring); conciseness 4/5 (full item evidence retained). Mean 4.0. Highest-impact improvement is external validation of every C2 detail row, not reliance on top-level PASS. User should agree given the explicit execution boundary.
