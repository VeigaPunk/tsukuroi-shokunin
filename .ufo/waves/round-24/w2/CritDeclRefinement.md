Verdict: the SCORECARD section "Round 24 declaration refinements after wave 1" (`SCORECARD.md:755-763`, landed at `22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0`) survives with defects. Its header claim "targets unchanged" is falsified for C1's counted predicate. The C2 axis move fixes a lowest-axis rule miss that the section never mentions. The C2 before-value switches metric to keep 0 even though the section admits the base corpus already held dated verdicts. The original declaration text itself is intact, and every C2 counting-rule tightening checked against the earlier tool really is stricter.

Attacked: each of the five refinement bullets, compared with the original declaration at `SCORECARD.md:740-753` (landed at `674891dfbcb853432a863a6eb82e7b2a9bdb3958`). For each bullet I asked three questions: does it narrow a declared target, does it move an axis to dodge a miss, and does it change a before-value dishonestly? Impacted axes are named per finding.

## Findings

1. [obs] The original declaration was not rewritten in place. However, the refinements landed in the same commit as the evidence they admit, and no frozen preregistration exists for round 24.
   - `git diff 674891d 22fd164 -- SCORECARD.md` shows only additions after line 753. Lines 740-753 are byte-identical.
   - Commit times, read-only from `git log`: the declaration landed at 674891d (05:22:09 -03). The first tools and the L1 gate runs landed at 10b45f0 (05:31:02). The refinements landed at 22fd164 (05:59:42), together with the gate JSON, rows S087-S103, the hardened tools and the l1-4 capture (`git show 22fd164 --stat`).
   - `.ufo/waves/round-24/` has no `preregister.json` (`ls … | grep -i prereg`, exit 1). Round 23 had one (`SCORECARD.md:722`).
   - [inf] Committed bytes cannot show that any refinement came before the gate content it scores.
   - Smallest correction: the measured outcome labels these refinements as written after the evidence. Future refinements land in their own commit before the measured artifact.
   - Impacted: provenance.

2. [obs] C1: the counted predicate was relaxed for one finding while the number 268 was kept. This is a narrowing, disclosed but labelled "not changed".
   - The declaration defines the counted unit in the before cell: "red findings attributed to a named cause and a recorded tool operation" (`SCORECARD.md:748`). It promises: "A miss on either value is an honest stop; the targets will not be narrowed" (`SCORECARD.md:751`).
   - The refinement concedes that the predicate "holds for 267 of the 268" (`SCORECARD.md:763`). It still states "The declared after-values … are not changed" (`SCORECARD.md:757`) under the heading "targets unchanged" (`SCORECARD.md:755`).
   - Measured at 22fd164 (`python3 tools/report-red-causes.py --revision 22fd1642…`, exit 0; also `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/measure/c1-22fd1642.json`): `attributed_findings` 268, `attributed_with_recorded_operation` 267, `attributed_seat_level` 1. The field the target names therefore counts the one finding that fails the declared predicate.
   - [inf] The declaration was internally inconsistent from the start. The seat-level `SCOPE-TRACE-INCOMPLETE` finding on `ConnFxPlanner` was already public before the declaration (`SCORECARD.md:731,735`). The refinement resolved that inconsistency toward the easier reading.
   - This is a tradeoff for the canonical judge, not a defect an edit can remove.
   - Smallest correction: retitle the section "target number unchanged; counted predicate relaxed for one seat-level finding". The measured outcome then records C1 as "267 of 268 under the declared predicate; 268 in the refined field", so the judge rules on the miss by one.
   - Impacted: calibration (the C1 axis) and declaration honesty.

3. [obs] C2: moving the axis from freshness to depth restores compliance with the fleet rule "at least one on the lane's lowest non-retired axis". The refinement does not say so, and the counted unit is freshness work.
   - The rule appears at `/home/vgpnk/Projects/shokunin/MISSION.md:41-43` and `/home/vgpnk/Projects/shokunin/PROTOCOL.md:96-97`.
   - At the base, depth and adjacency are tied lowest at 8, and freshness is 9 (`SCORECARD.md:587`, `:616`, `:684`).
   - The original declaration put C1 on calibration (9) and C2 on freshness (actually 9). As declared, the round had no claim on a lowest axis. The refinement re-books the same work, with no change to its deliverable or its counter, to depth (`SCORECARD.md:759`), which makes the round compliant.
   - The stated reason, "supersedes weaker update-safety statements, which is depth work", conflicts with the axis definitions:
     - `/home/vgpnk/Projects/shokunin/AXES.md:14` defines freshness as "skill claims re-verified against live surfaces; stale items flagged or fixed". That is exactly what `premises_verified` counts: premises re-verified against a live capture.
     - `AXES.md:11` defines depth as decision tables with real thresholds and cited sources. `AXES.md:21` maps quality supersession to depth and freshness together.
   - Wave 1 recommended "freshness 9 → 9 (0)" and said C2 "works neither" depth nor adjacency (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/CritClaimSizing.md:62`). The refinement departs from that without giving a reason.
   - The lesson records only "freshness 8" as a stale self-assessment, not the lowest-axis consequence (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-24.md:45`).
   - Counter-evidence: the landed table at `SKILL.md:2239-2250` is a depth-shaped deliverable (a decision table with commands and cited entries). But no counting command measures it.
   - The ordinal delta is 0 under either axis, so no ordinal miss was dodged.
   - This is a tradeoff for the judge.
   - Smallest correction: append one sentence stating that the declaration as written had no lowest-axis claim and that the relabel is what makes the round compliant. Then either add a depth counting unit (for example, decision-table rows each bound to a verified gate premise), or keep freshness 9 → 9 and record the lowest-axis miss.
   - Impacted: depth, freshness and round-contract compliance.

4. [obs] C2: the before-value changes metric so the declared 0 survives, although the refinement itself admits the declared metric was not 0.
   - The declared metric is "premises of the host-wide pacman pause [that] carry a dated verdict in the lane corpus" = 0 (`SCORECARD.md:749`). The refinement concedes the round-17 dated notices exist, then redefines the before-value as the new checker's output, 0 (`SCORECARD.md:760`).
   - Under the declared metric at `f169b3ba`, two premises already carried dated verdicts:
     - P1: `corpus/knowledge/partial-upgrade-recheck-r15.md:176` (R17-FRESH-PARTIAL-02, "413 not re-measured; superseded by full upgrade at 09:15:31"), and record R17-FRESH-26 in `corpus/knowledge/freshness-recheck-r17.json`.
     - P3: `corpus/README.md:147-151` ("superseded for this host … both hooks resolve (namespace emulation; not boot-tested)"), and record R18-FRESH-NoticeSkill-06 in `corpus/knowledge/freshness-recheck-r18.json` (mkinitcpio 42.2-1 installed). All read with `git show f169b3ba:<path>`.
     - P2, P4 and P5: none found. `corpus/knowledge/package-state-plane.md:39` leaves P4's mirror lag as "[unknown]".
   - The declared before is therefore 2 of 5, not 0. The refinement keeps the full 0 → 5 delta by switching to an instrument whose before is 0 only because it does not exist yet. QUALITY criterion 49 says instrument existence alone is not an improvement (cited at `w1/CritLearningFit.md:9`).
   - The gate also scores P1 "changed" against the 413 proposition (`corpus/knowledge/pause-lift-gate-r24.json:9`), which the base had already marked historical.
   - Smallest correction: report both values: "declared metric 2 of 5 at `f169b3ba` (P1 and P3); checker count 0 (gate absent)". Credit C2 as 3 new premise verdicts (P2, P4, P5) plus 2 refreshed (P1 adds the 3 and 134 counts; P3 adds boot evidence).
   - Impacted: depth or freshness (the C2 axis), calibration and quality-trend provenance.

5. [obs] C2's before and after are produced by the uncommitted working-tree checker. The self-binding fix the refinement applied to C1 (`SCORECARD.md:762`) was not applied to C2, so the two claims use different before-value methods.
   - In my clone at 22fd164, I changed only the working-tree line `COUNTED = (…)` to `COUNTED = ()` in `tools/check-pause-gate.py` and ran `python3 tools/check-pause-gate.py --revision 22fd1642…`:
     - pristine: exit 0, verified 5;
     - mutant: exit 1, verified 0, revision 22fd164;
     - restored: exit 0, verified 5.
     - Outputs: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/CritDeclRefinement/wt-mutant.json` and `wt-restored.json`.
   - The same kind of change to `tools/report-red-causes.py` gives exit 2 with "working-tree report tool differs from the revision blob".
   - The C2 checker binds only the bytes it reads, not its own code (`tools/check-pause-gate.py:245-249`). Under C1's rule, the C2 command at `f169b3ba` would exit 2. Instead the working-tree tool prints 0 (`measure/c2-f169b3ba.json`; my rerun, exit 1). That contradicts the declaration's "over committed bytes at `<REV>`" (`SCORECARD.md:746`).
   - This is a fixable defect.
   - Smallest correction: give `check-pause-gate.py` the same self-blob check as the C1 tool. Restate C2's before as "absent, exit 2", consistent with C1.
   - Impacted: the C2 axis and measurement provenance.

6. [obs] The claim that the counting rule was "made stricter (never looser)" holds against the 10b45f0 tool. It is mislabelled for the capture change.
   - `git diff 10b45f0 22fd164 -- tools/check-pause-gate.py` shows only tightenings:
     - the round date is now a constant (`:37`), replacing the gate's own `sources_opened`;
     - the capture path and sha256 are checked (`:38`, `:92-96`);
     - at least one unique, non-boilerplate capture anchor is required (`:122-126`);
     - every source must be `mined`, opened 2026-10-22, with a used-by that names the gate, and the list must be non-empty (`:146-158`);
     - duplicate source rows are flagged;
     - `unverified` verdicts are excluded (`:35`, `:111-112`);
     - `premise` and `limits` must be non-empty.
   - "Every listed source", instead of the declaration's "at least one", is also stricter.
   - The capture repin is a different matter. At declaration time the only committed capture was `l1/capture.txt` (198 lines, sha256 `63baf1c8…`). `l1-4` was taken later, at 08:46:28Z (`l1-4/capture.txt:3`), after `capture.sh` had been extended twice (10b45f0: +8/-1; 22fd164: +23). The extensions added sections including mirror-servers, cache-package-files, cache-entries, paccache-runs-since-pause, stable-mirror-headers and checkupdates-temp-db (`grep -n '^### '` across the four captures). That is a change of evidence base, not a tightening.
   - Strongest counterexample tested, and it fails: re-pointing the gate at `l1` does not produce a miss.
     - Method: a mutant commit `7232ca6` in my clone sets `CAPTURE` and the gate's capture fields to `l1` and keeps only the needles that occur in `l1`.
     - Result: pristine PASS 5, then mutant PASS 5, then restored PASS 5.
     - Evidence: `w2/CritDeclRefinement/mut-pristine.json`, `mut-l1.json`, `mut-restored.json` and `mutant-l1-commit.txt`.
     - So the repin did not dodge a count miss.
   - Smallest correction: reword the bullet to "evidence base moved from l1, the only capture committed with the declaration, to the later l1-4 with an extended script; the count is unchanged under l1".
   - Impacted: provenance.

7. [obs] That same mutant exposes a gap the "stricter" rule leaves open: a two-part premise counts on evidence for only one part. And "an unverified verdict does not count" is avoided below the premise level.
   - The declared premises P3 (two hooks), P4 and P5 each join two claims (`SCORECARD.md:751`).
   - Under `l1`, P4 verifies on the single pointer `/var/lib/pacman/sync/core.db`: database freshness only, with no mirror evidence. P5 verifies on `installed zcode (3.16.2-1)`: transactions only, with no cache evidence (`mut-l1.json`).
   - At 22fd164, P3 counts with the verdict "changed". Its own limits say the btrfs-overlayfs path "stays unverified" (`corpus/knowledge/pause-lift-gate-r24.json:140`), and `SKILL.md:2247` says "the read-only snapshot-boot overlay path is untested". The operator rule names both hooks (`/home/vgpnk/.omp/agent/RULES.md:11-12`).
   - Wave 1 offered a two-part rule that keeps the target (`w1/CritClaimSizing.md:100-108`), plus a section map (`w1/RevGateSchema.md:18`). The refinement adopted neither.
   - [inf] Under a per-part rule, P3 would be unresolved for btrfs-overlayfs, giving 4 of 5.
   - This is a fixable defect; the judge should weigh the possible miss.
   - Smallest correction: declare a state for each part of P3, P4 and P5, require a unique capture anchor per part, and report P3's btrfs-overlayfs part as unverified in the count.
   - Impacted: the C2 axis and calibration.

8. [obs] The premise wording was never frozen. Neither the declaration nor the refinement maps the declared topics to the propositions the gate actually scores.
   - P4 was declared as "sync database freshness and which mirror sets the upgrade target". The gate proposition is "The local sync databases show how far the host is from its upgrade target" (`pause-lift-gate-r24.json:144`). The mirror part appears only in the limits.
   - P1 was declared as "pending upgrade count". The gate proposition targets the historical 413 figure (`:9`).
   - This is low severity, not a narrowing in itself.
   - Smallest correction: append a mapping of declared topic to gate proposition for P1-P5.

9. [obs] C1's before-value change, from "0 of 268" to "absent, exit 2" (`SCORECARD.md:762`), is honest.
   - My reruns: exit 2 at f169b3ba and at 674891d ("tools/report-red-causes.py is absent at this revision"), exit 2 at 10b45f0 (the working-tree tool differs from the revision blob), and exit 0 with 268 at 22fd164. This matches `measure/c1-f169b3ba.json`.
   - Residual: the declaration's clause "(no such report exists)" is left uncorrected, although 2 of 268 findings were already named with cause and site at the base (`SCORECARD.md:735`; `w1/CritClaimSizing.md:52-55`).
   - The 0 → 268 framing now measures instrument existence (`w1/CritLearningFit.md:96`). That is a tradeoff for the judge.
   - Smallest correction: one line retracting "no such report exists" in favour of "2 named with cause and site, 266 counted by cause, 0 joined to a recorded operation".

10. [obs] Narrowing "repair" to "acting on the spot-check's routing … and labelling the line-52 name" (`SCORECARD.md:763`) shrinks the claim title's meaning. The shrinkage is disclosed item by item: the lesson marks one line-64 item "Not exercised" and one "Carried unchanged" (`corpus/lessons/round-24.md:33-39`).
    - This survives.
    - Smallest correction: the measured outcome renames C1 "per-cause report honouring the routed constraints" instead of "repair".

[unk] I did not judge whether the gate's verdict facts are true on the host; other seats own the P1-P5 reviews.

Scope: read=SCORECARD.md:680-763, the four cited wave-1 reports (CritClaimSizing, CritLearningFit, CritC1Construction, RevGateSchema), corpus/knowledge/pause-lift-gate-r24.json, tools/check-pause-gate.py, corpus/lessons/round-24.md, corpus/lessons/round-23-verifier-spotcheck.md:45-64, SKILL.md:2239-2256 and grep hits, the four round-24 captures (section headers and needle counts), measure/*.json, base-revision blobs (freshness-recheck-r17.json, freshness-recheck-r18.json, partial-upgrade-recheck-r15.md, corpus/README.md, package-state-plane.md), /home/vgpnk/Projects/shokunin/{MISSION.md,PROTOCOL.md,AXES.md} (grep and ranges), /home/vgpnk/.omp/agent/RULES.md, ~/.agents/skills/godspeed/SKILL.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/CritDeclRefinement.md and the evidence copies /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/CritDeclRefinement/{mut-pristine.json,mut-l1.json,mut-restored.json,wt-mutant.json,wt-restored.json,mutant-l1-commit.txt}; outside the lane, the scratch clone /fast/scratch/hyaku/tsuku24w2-CritDeclRefinement/lane (mutant commit 7232ca6 on local branch mutl1, working tree restored to 22fd164) and raw tool outputs placed next to it in /fast/scratch/hyaku/tsuku24w2-CritDeclRefinement/ rather than inside the seat directory (disclosed); executed=read-only git in the lane (log, show, diff, status), sha256sum, wc and grep over the captures, inline python3 needle-count probe over the committed captures, and in the scratch clone only: git clone/checkout/commit/branch, python3 tools/report-red-causes.py and tools/check-pause-gate.py --revision at f169b3ba, 674891d, 10b45f0 and 22fd164 (C1 exits 2/2/2/0; C2 exits 1/1/1/0), the l1-capture mutant (pristine, mutant, restored: 0/0/0, verified 5/5/5), and the working-tree COUNTED mutant (0/1/0, verified 5/0/5) plus the matching C1 working-tree mutant (exit 2)
Installs: none
