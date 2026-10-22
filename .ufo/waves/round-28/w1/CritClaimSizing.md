Verdict: fails as framed. Both round-28 claims are instrument-validity (operability) moves labelled as depth and adjacency. The declared C1 after-value is also met by a degenerate byte-pin counter. The round's tip also harms operability: the registry-coverage gate goes from PASS to FAIL.

Revision under attack: f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 (base 3b9e0430b88d01415c241dd5a18b8939b8a520ac). All lane tools ran on the export /fast/scratch/hyaku/tsuku28/CritClaimSizing/tree, and the registry gate ran in a scratch git sandbox at /fast/scratch/hyaku/tsuku28/CritClaimSizing/regrun.

## Findings

1. [obs] Round 28 adds no bytes to either axis's content surface, so neither axis's AXES signal can have moved. `git diff --stat 3b9e0430 f8e3a8f2 -- corpus PROVINCE.md SKILL.md` prints nothing (exit 0). The whole round diff is SCORECARD.md, tools/check-adjacency-overlap.py and tools/mutants-adjacency-overlap.py: 3 files, 525 insertions.
   - AXES.md:11 defines depth as "Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources", and its signal is "A reader can act on SKILL.md alone". SKILL.md is unchanged.
   - AXES.md:16 defines adjacency as "evidence belonging to another domain reported, not absorbed". No register row, no PROVINCE row and no mori item changes.
   - AXES.md:13 defines operability as "Runnable artifacts: checklists that are executable, commands that exist, scripts that run". A gate that refuses inputs it should refuse is exactly that definition.
   - [inf] Both claims are therefore operability (instrument) moves. Impacted axes: depth, adjacency (claimed but unmoved) and operability (the real axis, which is not claimed).

2. [inf] Re-labelled honestly, the two claims sit on one axis. AXES.md:31-32 says "name distinct axes; two claims on one axis in one round count as one claim". Both claims have the same shape: harden a round-27 counter against a should-fail battery while the live control keeps 6. Once they are one operability claim, the lowest-axis duty (AXES.md:33) is not met, because operability is at 9 and not lowest.
   - The stagnation waiver does not apply. The lane's saturation line is 9 (SCORECARD.md:177 at f8e3a8f2), and depth and adjacency are at 8.

3. [obs] The lane's own record says routed defects are status-neutral and are not claims.
   - The round-27 spot-check heading at corpus/lessons/round-27-verifier-spotcheck.md:97 reads "Routed defects (the lane fixes these next round; all status-neutral)".
   - Round 27 treated its routed defects this way: SCORECARD.md:1006 reads "Routed round-26 defects (each fixed or explained in the round-27 lesson, none is a claim)".
   - Round 28 turns routed defects 2 and 3 into its only two claims (SCORECARD.md:1054, 1058, 1059). [inf] This is an identity change of the claim type from the lane's own precedent, and the declaration does not explain it.

4. [obs] "No ordinal change" (SCORECARD.md:1067) fits "works the lowest axis" (SCORECARD.md:1054) only under a reading in which touching a tool that is associated with an axis counts as working it.
   - AXES.md:28 asks a claim to "land one verifiable improvement, measure it". Here the improvement and the measure are about the tool, not the axis.
   - Round 27's 8 → 8 claims at least added axis content: KT1 to KT6, OV1 to OV6, and 6 tier-A sources. Round 28 adds none (finding 1).
   - The depth ordinal was last moved at round 4 (round-27 axes table, depth row, SCORECARD.md:1027). This is the second round in a row that "works" both lowest axes at 8 → 8. [inf] Under this reading the lowest-axis duty can be met forever without the axis moving, which is premature saturation by relabelling.

5. [obs] The C1 after-value does not tell rule hardening apart from byte pinning. Counterexample: /fast/scratch/hyaku/tsuku28/CritClaimSizing/pin-counter.py adds no B1 to B7 rule. It is the dd94cb1f counter unchanged, plus a sha256 pin of three things at f8e3a8f2: the register content, the PROVINCE.md bytes and the snapshot bytes.
   - Command: `python3 tools/mutants-adjacency-overlap.py --lane <lane> --base f8e3a8f2… --counter-file …/pin-counter.py`, exit 0.
   - Last line: `"control_live_anchored_rows": 6, … "should_fail_accepted": 0, "accepted_mutants": [], "should_pass_accepted": 0`.
   - That meets the declared after-value at SCORECARD.md:1058 exactly ("0 of 24 accepted, and control_live_anchored_rows 6 with exit 0").
   - The real round-28 counter gives `"should_fail_accepted": 0 … "should_pass_accepted": 4` (exit 0). The old dd94cb1f counter gives 19 of 24 should-fail accepted and 0 should-pass. Both declared values reproduce.
   - The only field that separates a real rule from a pin is `should_pass_accepted`, and it is not in the declared after-value.
   - Impacted axis: the claimed adjacency improvement is not shown by the declared count.

6. [obs] The counter is hard-wired to the closed round-27 register, so no future adjacency count goes through it.
   - At f8e3a8f2, tools/check-adjacency-overlap.py lines 50-56 hard-code `REGISTER = 'corpus/knowledge/adjacency-mori-oom-r27.json'`, the pinned mori commit and path, `IDS = OV1..OV6` and the round-27 PROVINCE section.
   - Rule B6, "at most one LANE-GAP row counts" (docstring lines 38-39), equals the live register exactly: OV6 is its only LANE-GAP row (parsed from the register at f8e3a8f2).
   - [inf] Hardening this tool re-grades a count the lane already recorded (round-27 measured outcome, "6 of 6 rows OV1 to OV6"). That is self-assessment accuracy, which AXES.md:15 calls calibration ("gaps named honestly, confidence graded, overreach caught"). It is not new adjacency.

7. The question of a calibration claim "in disguise, third in a row":
   - [obs] The literal premise does not hold. Rounds 25 and 26 claimed calibration, and round 27 did not: SCORECARD.md:1023 says "calibration is not claimed". [unk] I found no written "third in a row" rule. `git grep -i -E 'in a row|consecutive|third'` over SCORECARD.md, QUALITY.md, lessons, SKILL.md and LOG.md, plus AXES.md, MISSION.md and the goal file, finds no calibration-repeat rule.
   - [inf] In substance, C1 (finding 6) and C2 (which by the same logic re-grades the round-27 KT count) are calibration-shaped: they correct how well a recorded count reflects reality.
   - [obs] As calibration claims they would also fail the required form. The prompt at .ufo/prompts/tsukuroi-round-28.md:347-348 says "A calibration claim must count mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state". QUALITY 57 says the same. These claims count accepted mutants, not self-assessment mismatches.
   - So the claims are either operability moves (finding 2) or calibration moves in the wrong form. In neither case are they depth or adjacency moves.

8. [obs] Harm at the tip: the registry-coverage gate goes from PASS to FAIL. In the sandbox (`cd …/regrun && python3 tools/check-registry-coverage.py --revision <REV>`):
   - At 3b9e0430: exit 0, `"status":"PASS"`, 31 of 31.
   - At f8e3a8f2: exit 1, `"status":"FAIL"`, finding `REGISTRY-ROW-MISSING` at `tools/mutants-adjacency-overlap.py`.
   - This repeats the round-27 mistake R27-REGISTRY-ROW-MISSING (SCORECARD.md, round-27 falsify-wave outcome). The C2 battery `tools/mutants-kernel-taint.py` will do the same unless it gets a row.
   - Impacted axis: operability. Under AXES.md:35 ("no axis is harmed") this blocks admission until it is fixed.

9. [obs] The round-28 counter change also widens what the counter accepts, and the declaration does not say so.
   - The docstring calls the B1 to B7 rules "Round-28 tightenings (QUALITY 72, R27-COUNTER-PERMISSIVE; each can only refuse)".
   - The battery shows four shapes that the old counter refused and the new one accepts: upper-case-sha256, province-backticked-id, province-indented-row and register-utf8-bom. The old counter accepts 0 of them, the new one 4 (…/old.out, …/new.out).
   - Diff sites in `git diff dd94cb1f f8e3a8f2 -- tools/check-adjacency-overlap.py`: `.lower() != digest`, backtick stripping of PROVINCE ids, and `splitlines()`.
   - [inf] These may be correct normalisations. But SCORECARD.md:1058 states the claim only as "refuses", so the counter's meaning changed beyond what was declared. This is a hidden identity change of the measuring tool.

10. [obs] Neither claim is sourced. Section 2b item 4 of the prompt (.ufo/prompts/tsukuroi-round-28.md:73-74) requires that "one of the round's claims rests on a SOURCES.md row opened this round". A grep of SCORECARD.md:1052-1067 for `sourced|SOURCES|S1[0-9]{2}|learning claim` returns no match (exit 1). Neither claim's after-value depends on a source row. [inf] The frontier-step conformance item is unmet by the declared claims.

11. [obs] Routed defect 5 is wrongly attributed. SCORECARD.md:1067 says "routed 5 and 8 are mori's or the operator's". But corpus/lessons/round-27-verifier-spotcheck.md:103 routes 5 to the lane: mori says the lane's "+200 band scanned first" reading is false, and the instruction is "Check it against a source and correct or rebut it". The section heading at line 97 says "the lane fixes these next round". [inf] This is false provenance. It sets aside the one routed item that is real sourced depth and adjacency content.

12. [obs] The C1 after-value was observed before it was declared. SCORECARD.md:1065 says the L1 ran the uncommitted counter through the battery "(0 of 24 accepted, control 6)". The battery and the counter land in the same commit, f8e3a8f. [inf] The target is a retrodiction sized to a known result, not a falsifiable prediction. That is honest, because it is disclosed, but it carries little evidential weight.

## Strongest case against admission

Neither claim lands any depth or adjacency content: zero bytes of corpus/, PROVINCE.md or SKILL.md change. Both are the same kind of move, counter hardening, so under AXES.md:31-32 they are one claim. That axis is operability at 9, so the lowest-axis duty is not met. The declared C1 value is also met by a pin-only counter, so it proves nothing beyond the 24 fixed shapes. And at f8e3a8f2 operability is harmed, because registry coverage goes from PASS to FAIL. The causes of failure are a fixable defect (finding 8) plus a framing tradeoff that the judge should reject (findings 1 to 4).

## Smallest safe correction

- (a) Add a SKILL.md registry row for tools/mutants-adjacency-overlap.py, and later for tools/mutants-kernel-taint.py, before measuring.
- (b) Re-declare C1 and C2 honestly as one operability (instrument-validity) claim. Add `should_pass_accepted` with its value at the round-28 counter to the declared after-value, or disclose that byte pinning also meets the value. Disclose the four widened acceptances.
- (c) Restore the lowest-axis duty with a real content claim. The cheapest one already owed is routed defect 5: check the "+200 band scanned first" reading in oom-event-plane.md:116,349 and kill-event-deep-r8.md:147,260 against a source opened this round, then correct or rebut it. That is sourced depth that also satisfies section 2b item 4, and it touches mori's adjacency. Alternatively, keep the 8 → 8 labels only with an explicit, judge-visible statement that "works" means tooling only, and let the operator rule.

Scope: read=SCORECARD.md@f8e3a8f2 lines 983-1067 and 177; AXES.md; .ufo/prompts/tsukuroi-round-28.md (all); round-27-verifier-spotcheck.md@f8e3a8f2 lines 85-115; tools/check-adjacency-overlap.py and tools/mutants-adjacency-overlap.py @f8e3a8f2; dd94cb1f counter diff; adjacency register JSON; CritC1Tool/mutants.out lines 2,3,16,17,18; goal file grep; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/w1/CritClaimSizing.md, /fast/scratch/hyaku/tsuku28/CritClaimSizing/{tree/,regrun/,pin-counter.py,old-counter.py,pins.json,new.out,new.err,old.out,old.err,pin.out,pin.err,reg-*.json}; executed=git archive f8e3a8f2 | tar -x; git show/diff/ls-tree/grep/rev-parse (read-only) on the lane; python3 tools/mutants-adjacency-overlap.py --lane <lane> with --counter-rev f8e3a8f2 (exit 0), with --counter-rev dd94cb1f --base 3b9e0430 (exit 0), with --counter-file pin-counter.py (exit 0); git init and git fetch of two revisions into the scratch sandbox regrun, plus update-ref in that sandbox only; python3 tools/check-registry-coverage.py --revision 3b9e0430 (exit 0) and --revision f8e3a8f2 (exit 1) in the sandbox
Model: not exposed
Installs: none
