# CritC1Honesty — honesty attack on round-24 claim C1 and its SCORECARD wording

Verdict: I attacked the honesty of the C1 after-value "268 of 268" and of the "repair" label at commit `22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0`. Both are **falsified as worded**; the instrument itself survives with defects.

- Against the declared unit, "red findings attributed to a named cause and a recorded tool operation", the measured value is **267 of 268**. The 268th finding is seat-level. It can never have a recorded tool operation, so the declared target was unattainable by construction. The field `attributed_findings` reads 268 only because it counts a wider predicate than the one declared.
- "Repair" is not honest for spot-check lines 52 and 64. No round-23 byte or result changes. The new report acts on the line-64 routing and applies the line-52 label rule in new output. One line-64 item, emitter identity plus the native-completion versus trace-completeness state, is not delivered.
- The closure should record C1 as **not met as declared (honest stop), target not narrowed**, with the bounded content result stated next to it. The exact wording is in finding 9.

## Findings

1. **[obs] The declared unit is a conjunction, and only 267 findings satisfy it.**
   - The declaration's Before cell defines the unit: "0 of 268 red findings attributed to a named cause and a recorded tool operation". The After cell reuses that unit by ellipsis: "268 of 268 attributed" (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:748`).
   - Command (run from the lane root): `python3 tools/report-red-causes.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0`. Exit 0. Output: `attributed_findings` 268, `attributed_with_recorded_operation` 267, `attributed_seat_level` 1, `preserved` true.
   - My scratch-clone rerun is byte-identical to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/measure/c1-22fd1642.json` (`cmp` exit 0).
   - The seat-level row is built with `operation` None and the literal `'none (seat-level trace state)'` (`git show 22fd1642:tools/report-red-causes.py`, lines 142-148). It is then counted into `attributed` at line 152, the same as event rows.
   - So `attributed_findings` means "attributed to a cause and either a recorded operation or the seat's trace state". The declaration never stated that disjunction.
   - Impacted axes: calibration (the claimed axis) and false provenance of the after-value.

2. **[obs] The lane's own rules turn this into a miss, not a met target.**
   - `SCORECARD.md:751` reads: "A miss on either value is an honest stop; the targets will not be narrowed."
   - `SCORECARD.md:757` says the after-values "are not changed".
   - `SCORECARD.md:763` concedes that the phrase "holds for 267 of the 268; the measured outcome will state that, not round it up."
   - The claim text under attack leads with "field attributed_findings 268 of 268 (267 with a recorded tool operation plus 1 seat-level)". That leads with the rounded-up number, which the refinement promised not to do.
   - There are only two ways to report 268 of 268 as met:
     - loosen the predicate to include seat-level state; or
     - narrow the denominator to the 267 event-level findings.
   - Both change the declared target.
   - Strongest counter-reading: the After cell also lists "the incomplete seat `ConnFxPlanner` … kept visible", so the author always meant the seat finding to count. This fails. Keeping a seat visible is a separate preserved invariant; it does not supply a recorded tool operation. The author's own refinement at `SCORECARD.md:763` rejects that reading.
   - [inf] This is not a fixable code defect. It is the trade-off the canonical judge must reject as "met". Recording it as an honest miss is correct, and it is not a failure of the instrument.

3. **[obs] "Named cause" is not measured by the counting field.**
   - Scratch clone `/fast/scratch/hyaku/tsuku24w2-CritC1Honesty/lane` at `22fd1642`. I made one mutant (branch `mut-nocause`) that sets every subcause to None: line 131 (path subcause), line 136 (schema subcause) and the line-144 seat subcause.

     | Run | Exit | `attributed_findings` | `preserved` | Rows with no subcause |
     |---|---|---|---|---|
     | Pristine | 0 | 268 | true | 0 |
     | Mutant | 0 | 268 | true | 268 |
     | Restored | 0 | 268 | true | 0 (byte-identical to pristine) |

   - The only "cause" the count can depend on is the frozen checker's finding id. That id was already present in the checker output at the base.
   - So the count's real new content is the join to a recorded operation, which is the 267 in finding 1. The subcause labels are useful observability, but they are unmeasured text.
   - Impacted axes: calibration, discernment.

4. **[obs] 8 of the 15 rows labelled "outside the lane root" assert a location the bytes do not establish.**
   - The label is assigned whenever the spelling does not start with the lane root (tool lines 89-90). The spellings were read from `.ufo/waves/round-23/falsify/events.json` at each `per_finding` site.
   - Four are `..` traversals that normalise lexically to inside the lane: FxC1Selftest:12 and :13, FxC3Build06:7, and ConnFxPlanner:28. Example spelling: `/home/vgpnk/Projects/shokunin/tsukuroi-showin/../tsukuroi-shokunin/.ufo/...`.
     - Today the prefix directories do not exist: `stat` on `/home/vgpnk/Projects/shokunin/tsukuroi-showin` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokuroi` returns "No such file or directory".
     - [inf] Physical resolution would therefore fail; it would not land outside the lane.
   - Three are `redacted-internal-uri`: FxC2OracleLegacy:17, SentFxPrivacy:13 and :14. The original target is redacted, so its location is [unk].
   - One is a relative path: FxSources:38, `.ufo/waves/round-23/falsify/FxSources.md`. Its resolution depends on a working directory that is not recorded, so its location is [unk].
   - The other 7 are genuinely outside the lane: five misspelt sibling roots and two fleet-root paths.
   - My normalisation check of every "inside the lane" row found none that escapes the lane, so that label holds.
   - Seven glob patterns carry "base path undeclared". For a pattern, "base path" is vacuous but not false.
   - Impacted axis: discernment. The finding id stays correct, so no count changes.

5. **[obs] The seat-level cause "trace ends before a final message" is an author inference that no recorded evidence supports.**
   - The collector sets `complete` to `parsed and report_capture_ok and (closed or confirmed_failure or native_final)` (`git show 22fd1642:.ufo/waves/round-23/collect.py`, line 280). It also forces `complete` to False for a non-string tool name (lines 284-286).
   - For ConnFxPlanner the retained bytes show:
     - `terminal_evidence.session_exit_line` null and `native_failure` null (`events.json`);
     - native status `completed` (`.ufo/waves/round-23/falsify/native-outcomes.json:593` onward).
   - The failing conjunct is not retained, so parse failure, report-capture failure and missing final text all remain possible.
   - `git grep "final message"` at `22fd1642` finds the phrase only in the new tool (line 144) and in older rounds' unrelated death files. Round-23's own wording is weaker: "ConnFxPlanner lacks a complete terminal trace" (`corpus/lessons/round-23.md:86`).
   - QUALITY 54 (`corpus/QUALITY.md:107`) is the rule this round wrote for `replace_all`: a summary may name something only when the retained bytes contain it. That rule applies here too. This cause name is not recoverable from retained events.
   - Impacted axes: provenance, calibration.

6. **[obs] The "repair" label overstates what happened.**
   - Where the word still appears:
     - the declaration row "(repair of the routed defects at spot-check lines 52 and 64)" (`SCORECARD.md:748`);
     - the tool docstring "Repairs the routed defects at … lines 52 and 64" (tool line 4);
     - the lesson row for line 52, "Fixed in output and as criterion" (`corpus/lessons/round-24.md:35`).
   - Spot-check line 52 (`corpus/lessons/round-23-verifier-spotcheck.md:52`) is a disclosure constraint ("do not elevate this explanatory list into original-trace proof"). It is not a defect that a later round can fix.
     - The round-23 file `falsify-limit.json` still lists `replace_all` unlabelled. Its blob is pinned unchanged (tool `PINS`, lines 35-40).
     - What is new is a label in a new output. MutC1Label (`.ufo/waves/round-24/w2/MutC1Label.md`) shows that label is enforced.
   - Spot-check line 64 is routing for the next round. The round-23 rejection cause, C2 operability mode 0 and exit 2, is unchanged and deliberately preserved.
   - The refinement at `SCORECARD.md:763` already defines "repair" this narrowly. The declaration row, the docstring and the lesson "Fixed" cell still say more than that.
   - Impacted axis: discernment.

7. **[obs] One line-64 routed item is neither delivered nor dispositioned.**
   - Line 64 requires: "Preserve exact baseline/input/emitter identities and explicit native-completion-versus-trace-completeness states."
   - Emitter identity is not pinned. `PINS` (tool lines 35-40) covers the checker, manifest, events and limit file, but not the collector `.ufo/waves/round-23/collect.py` that emitted `events.json`.
   - Native completion is not shown. A search of `c1-22fd1642.json` finds no `native` key. `incomplete_seats` shows only `trace_complete` false for ConnFxPlanner, not its native `completed` status.
   - The lesson's disposition table (`corpus/lessons/round-24.md:35-39`) lists three line-64 items and omits this one.
   - [inf] Omitting an item without saying so shrinks scope. Here the omission also weakens the "repair" wording.

8. **[obs] Minor provenance point.** The cited outputs under `.ufo/waves/round-24/measure/` are untracked at `22fd1642` (`git ls-files --error-unmatch` fails, and `git status` shows `?? .ufo/waves/round-24/measure/`). They are re-derivable; my rerun matched byte for byte. They must not be described as committed evidence until they are committed.

9. **Verdict wording the closure should see (target kept at 268 of 268, not narrowed):**

   > C1 (per-cause report of the frozen round-23 falsify red cohort), measured at `22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0`: **declared after-value not met — honest stop; target unchanged.** Against the declared unit "red findings attributed to a named cause and a recorded tool operation", the count is **267 of 268** (`attributed_with_recorded_operation` 267). The 268th, `SCOPE-TRACE-INCOMPLETE` on `ConnFxPlanner`, is a seat-level finding with no recorded tool operation by construction, so 268 of 268 was unattainable as declared. Field `attributed_findings` reads 268 only because it also counts that seat-level finding, which is a wider predicate than the one declared. Before at `f169b3ba`: tool absent, exit 2, no value (counted as 0). Preserved invariants hold: checker `CANNOT_EVALUATE`, exit 2, `ConnFxPlanner` listed trace-incomplete, `__unknown_argument__` retained at `FxC3Build08:17`, `replace_all` labelled author recollection, four inputs pinned to the `f169b3ba` blobs, split 266/1/1. "Named cause" is enforced only as the checker's finding id. Sub-cause labels are descriptive and unchecked by the count: 8 "outside the lane root" rows overstate location, and the seat-level "trace ends before a final message" is not recoverable from retained events. This is not a repair of round-23 defects: no round-23 byte or result changed. The report acts on spot-check line 64 and applies the line-52 labelling rule in new output. Line 64's emitter-identity and native-versus-trace-completeness items are not delivered. Calibration 9 → 9 (0). Author-side only; outside closure decides admission.

## Smallest safe corrections

| Finding | Correction | What it does not change |
|---|---|---|
| 1, 2 | Measured outcome reports 267 of 268 as a miss, using the finding-9 wording. Never headline "268 of 268". | The target is not narrowed and the predicate is not loosened. |
| 3 | State in the outcome that "named cause" equals the checker finding id. Optionally add a `preserved` condition requiring a non-null subcause per row; mutant `mut-nocause` then becomes a killed control. | — |
| 4 | Rename the tool line-90 label to "not lane-local: spelling does not start with the lane root". Better: split it into "other absolute prefix", "dot-dot traversal", "relative path, working directory not recorded" and "redacted internal URI, location unknown". | No count changes. |
| 5 | Replace the line-144 subcause with "collector `complete` flag false; native status completed; failing condition not retained". | — |
| 6 | Drop "repair" and "Fixed" (append-only notice where the text is frozen). Use "acts on the line-64 routing; applies the line-52 label rule in new output". | Round-23 bytes stay frozen. |
| 7 | Pin the collector digest and add ConnFxPlanner's native `completed` status to `incomplete_seats`, or list the item as not delivered in the lesson's routed-defects table. | — |
| 8 | Commit the measure outputs, or label them uncommitted reruns. | — |

Scope: read=SCORECARD.md lines 700-763, corpus/lessons/round-23-verifier-spotcheck.md, corpus/lessons/round-24.md lines 25-60, corpus/lessons/round-23.md:86, corpus/QUALITY.md lines 107-109, SKILL.md:2284 (via git show at 22fd1642), tools/report-red-causes.py, tools/check-seat-bindings.py and tools/_revision.py (grep), .ufo/waves/round-23/collect.py lines 200-310, round-23 falsify events.json, bindings.json, native-outcomes.json and falsify-limit.json, round-24 measure c1 JSON files, w1 CritC1Construction.md, RevC1Attribution.md and CritClaimSizing.md, w2 MutC1Label.md and MutC1Reclassify.md (heads), ~/.agents/skills/godspeed/SKILL.md, /home/vgpnk/.omp/agent/RULES.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/CritC1Honesty.md, plus a scratch clone at /fast/scratch/hyaku/tsuku24w2-CritC1Honesty/lane (local mutant branch `mut-nocause`) with pristine.json, mut-nocause.json and restored.json beside it; executed=read-only git in the lane (log, status, show, grep, ls-tree, ls-files), read-only python3 analyses of the frozen JSON files, stat of two nonexistent prefix directories, cmp; in the scratch clone: git clone, checkout, remote remove, branch, commit, and `python3 tools/report-red-causes.py --revision <sha> [--branch mut-nocause]` for the pristine (exit 0), mutant (exit 0) and restored (exit 0) runs
Installs: none
