# CritClaimSizing — claim-sizing attack on the round-24 declaration, attempt 2

Verdict: neither claim is correctly sized as declared. The C1 before value of 0 cannot be re-derived, because the declared command already returns 268 of 268 at the claim base `f169b3ba`. The C2 axis ordinal and before value are wrong, and the C2 counting command can reach 5 of 5 without a capture line, without a source opened this round, and without any resolved verdict. Every defect below has a correction that keeps the targets (268 of 268 and 5 premises) unchanged or makes them stricter.

Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:740-753` (declared at `674891dfbcb853432a863a6eb82e7b2a9bdb3958`). The tools were measured as landed at `10b45f050c16f5f1d4f7e15a285d9f5294f7a486`.

The five sizing checks used below:

- (a) one concrete after-value;
- (b) re-derivable by one command over committed bytes;
- (c) no universal clause without full enumeration;
- (d) causal separability;
- (e) an honest before value at `f169b3ba`.

## C1 — per-cause report of the frozen round-23 falsify red cohort

1. **The before value cannot be re-derived, and the counting command cannot tell the base apart from the repaired revision.** Impacted checks: (b) and (e).
   - [obs] Counterexample: `python3 tools/report-red-causes.py --revision f169b3ba` exits 0 with `total_findings` 268, `attributed_findings` 268 and `preserved` true. The same command at `674891d` gives the same result, and at `10b45f0` it also gives 268 with exit 0.
   - [obs] Cause: the tool runs from the working tree, but it reads only the round-23 inputs from the revision (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/report-red-causes.py:127-138`). Those inputs are byte-identical between the base and HEAD: `git diff --stat f169b3ba 10b45f0 -- .ufo/waves/round-23 tools/check-seat-bindings.py` prints nothing.
   - [inf] The declared value 268 therefore measures the tool, which lives in the working tree, and not the committed bytes at `<REV>`. The declared before value "0 of 268" is true only because the tool file is absent at the base, and the declared command does not express that.
   - Smallest safe correction: bind the tool to its own revision blob, using the pattern it already applies to the checker (`report-red-causes.py:56-59`). The command would then exit 2 at any revision that lacks `tools/report-red-causes.py`.
   - Suggested Before-cell wording: "At `f169b3ba` the counting tool is absent from the revision, so the command bound to that revision exits 2 and reports no `attributed_findings` (counted as 0)."

2. **The universal clause "attributed to a named cause and a recorded tool operation" is false for 1 of the 268 findings.** Impacted checks: (c) and (a).
   - [obs] The `SCOPE-TRACE-INCOMPLETE` finding on `ConnFxPlanner` is a seat-level finding with no request site. The tool assigns it the synthetic operation `'seat-level trace state'` (`report-red-causes.py:90-91`), and the run at `f169b3ba` shows that row with count 1. That label is not a recorded tool operation.
   - Suggested After-cell wording, which keeps 268 of 268: "268 of 268 attributed: 267 site findings to a named cause and the recorded tool operation of the request at that site, and 1 seat-level finding (`SCOPE-TRACE-INCOMPLETE`, `ConnFxPlanner`) to its cause and the seat's trace state."

3. **"Named cause" is undefined, and the tool equates it with the checker's finding id. That id merges two distinct checker causes for 266 of the 268 findings.** Impacted checks: (a) and (e).
   - [obs] The tool groups rows by `(finding id, operation)` (`report-red-causes.py:95-96`), so its "cause" is the finding code the checker already emits for every finding.
   - [obs] `SCOPE-PATH-DENIED` comes from two separate branches of the checker:
     - a non-local path (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-seat-bindings.py:56-57`);
     - a local path missing from the seat's binding (`check-seat-bindings.py:111-112`).
   - [obs] I replayed those two branches over the frozen bytes at `f169b3ba` with an inline Python script (exit 0). Result: 197 non-local paths (188 read, 5 glob, 2 grep, 2 write) and 69 local paths outside the binding (42 read, 26 grep, 1 glob), for 266 in total. There are 268 unique sites and no site carries more than one finding.
   - [inf] With cause defined as the finding id, the "cause" half of the target is already 268 of 268 in the checker output at the base. Only the operation join is new.
   - Smallest safe correction: name the cause vocabulary in the declaration. Wording that keeps 268 of 268 but makes the cause real: "named cause = the checker branch that raised the finding: non-local path, local path outside the seat binding, unsupported edit shape, or incomplete trace." Alternatively, if the finding id is the intended cause, say so explicitly: "named cause = checker finding id".

4. **The after-value is compound, but the declared field carries only one part of it, and the frozen inputs and the seat's identity are not pinned.** Impacted checks: (a) and (b).
   - [obs] The status, exit 2, incomplete seat and unknown key are checked only inside `preserved` and the exit code (`report-red-causes.py:119-122`), not in `attributed_findings`.
   - [obs] `preserved` requires only that some seat is incomplete (`bool(incomplete)`, `report-red-causes.py:98-99, 120`). It does not require that seat to be `ConnFxPlanner`.
   - [obs] The input digests are printed but never compared with pinned values (`report-red-causes.py:136-137`). Nothing in the command therefore enforces "frozen".
   - [inf] An edit to `.ufo/waves/round-23/falsify/events.json` at a later `<REV>` that kept 268 findings but marked a different seat incomplete would still give 268 with `preserved` true.
   - Suggested After-cell wording, which keeps the target:
     - "`attributed_findings` = 268, with `preserved` true and exit 0;
     - `incomplete_seats` = [`ConnFxPlanner`];
     - `inputs` sha256 equal to their values at `f169b3ba`:
       - `bindings.json` 8c72460b…a9044;
       - `events.json` 52a5021b…62b83;
       - `falsify-limit.json` e8e22aae…f1db;
       - `check-seat-bindings.py` 35079db5…d880."
   - The tool should enforce these digests.

5. **"No such report exists" is a universal clause that is not enumerated, and it is partly false.** Impacted checks: (c) and (e).
   - [obs] At `f169b3ba`, `SCORECARD.md:735` already names `FxC3Build08:17` with its unlisted key and names `ConnFxPlanner` as trace-incomplete. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/measure/post-falsify/falsify-limit.json:6-7,18-19` records `incomplete_seat`, `schema_site`, `path_findings` 266 and `path_finding_seats` 21.
   - [inf] Before this round, 2 of 268 findings were already named with cause and site, and the other 266 were counted by cause. None was joined to a recorded tool operation.
   - Suggested wording: "Before: 2 of 268 findings were named with cause and site (`SCORECARD.md:735`, `falsify-limit.json`), and 266 were counted by cause only. 0 of 268 were joined to a recorded tool operation."

## C2 — pause-lift update-safety gate entry

6. **The axis ordinal is wrong: freshness is 9 at the base, not 8, and it is not tied lowest.** Impacted check: (e).
   - [obs] `SCORECARD.md:240` records freshness 8→9 in fleet round 1. The round-19 baseline lists freshness 9 and names depth and adjacency as tied lowest at 8 (`SCORECARD.md:587`). Round 20 repeats this (`SCORECARD.md:616`), and round 22 inherits freshness 9 (`SCORECARD.md:684`).
   - [obs] `corpus/lessons/round-17-verifier-spotcheck.md:88` reads "freshness 9→9". `git grep` at `f169b3ba` finds no record of freshness being lowered.
   - Suggested wording: "freshness 9 → 9 (0)". The phrase "tied lowest" should be removed: depth and adjacency are the tied-lowest axes at 8, and C2 works neither.

7. **The before value "0 premises carry a dated verdict in the lane corpus (the corpus still records 413 pending upgrades and a pending mkinitcpio 42 upgrade)" is an unenumerated universal, and its parenthetical misstates what the base records.** Impacted checks: (c) and (e).
   - [obs] At `f169b3ba`, dated supersessions already exist for P1:
     - `corpus/knowledge/freshness-recheck-r17.json:258-259` reads "413 not re-measured; superseded by full upgrade at 09:15:31";
     - `corpus/knowledge/freshness-recheck-r18.json:619` calls 413 "a dated R15 snapshot";
     - `corpus/knowledge/host-health-report-r3.md:628` reads "neither 413 nor zero is current".
   - [obs] Dated supersessions also exist for P3:
     - `freshness-recheck-r18.json:58-62` records that mkinitcpio 42.2-1 is installed;
     - `SKILL.md:1927` corrects the pending text at `SKILL.md:1833`;
     - `corpus/knowledge/initramfs-v42-sysroot-recovery.md:85` records the `new_root -> sysroot` symlink.
   - [obs] The "pending mkinitcpio 42" text survives only at loci that later notices correct (`corpus/README.md:38` is corrected at `:149`).
   - [obs] The only before value the command can re-derive: `python3 tools/check-pause-gate.py --revision f169b3ba` exits 1 with `premises_verified` 0 and `GATE-MISSING`.
   - Suggested wording: "Before: 0 premises verified at `f169b3ba` (exit 1, `GATE-MISSING`; no pause-gate entry exists). Earlier dated rechecks already supersede the 413 count (`freshness-recheck-r17.json:258-259`) and the pending mkinitcpio 42 state (`freshness-recheck-r18.json:58-62`). No entry ties the five pause premises to a verdict, a capture line and a source opened this round."

8. **"A line in the committed round-24 capture" is not enforced, and the phrase is now ambiguous.** Impacted checks: (b) and (c).
   - [obs] The checker accepts evidence from any committed path (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-pause-gate.py:100-115`) and never reads the gate's `capture` field.
   - [obs] Counterexample A, an in-memory gate run against the bytes at `10b45f0`, scored `premises_verified` 5 with exit 0. All five premises pointed only at `SCORECARD.md:749` with substring `5 premises`, which is the declaration itself.
   - [obs] Two captures are now committed: `.ufo/waves/round-24/capture/l1/capture.txt` (landed with the declaration at `674891d`, sha256 `63baf1c8…01bb`) and `.ufo/waves/round-24/capture/l1-2/capture.txt` (landed later at `10b45f0`, sha256 `ba041f12…cfa`). Both match their `capture.sha256` files.
   - Suggested wording: "each with at least one evidence line in `.ufo/waves/round-24/capture/l1/capture.txt` (sha256 `63baf1c8522f2d597f4616c32caa77dfa1debae42a33a65a1e3b30db826601bb`)". If `l1-2` is admissible too, list it with its digest. The checker should require that path and that digest.

9. **"Opened this round" is controlled by the author, and the planned gate schema and the checker disagree.** Impacted checks: (b) and (d), through a duplicate authority.
   - [obs] The opened date is read from the gate's own `sources_opened` field (`check-pause-gate.py:78, 120-123`), not fixed at 2026-10-22.
   - [obs] Counterexample A set `sources_opened` to 2026-10-21 and cited S086, whose opened cell is 2026-10-21, and it counted.
   - [obs] Counterexample B used the planned schema (`captured_at` and `capture`, no `sources_opened`) with valid capture evidence. It exited 1 with `GATE-SCHEMA` and `premises_verified` 0.
   - [obs] At both `f169b3ba` and `10b45f0`, `corpus/SOURCES.md` has 0 rows containing 2026-10-22, and all 86 rows split into 11 cells.
   - Suggested wording: "every listed source id is a row of `corpus/SOURCES.md` whose `opened` cell contains 2026-10-22." The checker should fix that date as a constant. The schema should be one document, either adding `sources_opened` to the planned schema or removing it from the checker.

10. **The declaration says "at least one SOURCES row opened this round", but the checker and the assignment require every listed source to be opened this round.** Impacted check: (b), through a duplicate authority.
    - [obs] The checker rejects a premise if any listed source fails the date test (`check-pause-gate.py:120-123`).
    - [inf] A P3 premise citing one new row plus the older S002 row counts under the declaration but fails the checker.
    - Suggested wording, which matches the counting authority and is stricter, not narrower: "at least one source id is listed, and every listed source id is a row opened 2026-10-22."

11. **The verdict "unverified" counts toward 5, so the after-value can be met without resolving any premise.** Impacted check: (a).
    - [obs] `VERDICTS` includes `unverified` (`check-pause-gate.py:31`), and counterexample A reached 5 of 5 with five `unverified` verdicts.
    - [obs] The declaration says only "each with a verdict" (`SCORECARD.md:749`).
    - Smallest safe correction, which keeps 5: "5 premises verified; each verdict is one of cleared, still-holds, changed or unverified. The verdict list for P1 to P5 is reported with the count, and an `unverified` premise is reported as unresolved."

12. **P1, P3, P4 and P5 are not single propositions, so a single verdict on each is ambiguous.** Impacted check: (a).
    - [obs] P1 "pending upgrade count" is a quantity rather than a proposition.
    - [obs] P3 states a fact ("hooks that still name `/new_root`"), which is true according to the capture. The pause actually rests on a risk claim: that those hooks break boot under mkinitcpio 42 (operator directive: "the host's `btrfs-overlayfs` and `plymouth` hooks still expect `/new_root`").
    - [obs] P4 joins two claims: sync-database freshness and which mirror sets the target. P5 also joins two: rollback by package cache and transactions during the pause (`SCORECARD.md:751`).
    - [inf] P3 could honestly be "still-holds" as a fact and "cleared" as a risk at the same time.
    - Suggested wording, keeping the five ids:
      - P1: "pending upgrades against the current sync databases include boot-chain packages (corpus: 413)."
      - P3: "under mkinitcpio 42 the `btrfs-overlayfs` and `plymouth` hooks fail because they expect `/new_root`."
      - P4 and P5 keep both halves, with a declared rule: "cleared only if both halves clear; changed if either half changed."

## Cross-claim checks

13. **Causal separability holds in code, but the "reads only" universals are too broad.** Impacted checks: (d) and (c).
    - [obs] C1 reads only the four round-23 inputs (`report-red-causes.py:29-32`). C2 reads the gate, `corpus/SOURCES.md` and whatever paths its evidence names (`check-pause-gate.py:27-28, 105-107`). The only shared pieces are `tools/_revision.py` and the tool registry rows.
    - [inf] "C2 reads only this round's host capture and newly opened sources" is false as written, because the checker reads the whole registry and any committed evidence path.
    - Suggested wording: "C2 reads the gate entry, `corpus/SOURCES.md` and the files its evidence pointers name; it reads no round-23 evidence. C1 reads only the four frozen round-23 inputs."

14. **The fixture count wording is off by one.** Impacted check: (c), honesty.
    - [obs] Commit `eef0b8e9` changes 37 files: 36 under `.ufo/waves/round-24/fixtures/` plus `.ufo/waves/round-24/fixture-data-D-index.json`. The declaration's phrase "37 fixture files under `fixtures/` and `fixture-data-D-index.json`" reads as 38.
    - Suggested wording: "37 files: 36 under `.ufo/waves/round-24/fixtures/` and `fixture-data-D-index.json`".

15. **"The three previous rounds all worked the seat-audit surface" is only partly true.** Impacted check: (c).
    - [obs] Rounds 22 and 23 worked seat boundaries, seat bindings and receipts (`SCORECARD.md:678-680, 716-718`). Round 21 worked selector types, target-type controls and review snapshot binding (`SCORECARD.md:638-640`).
    - Suggested wording: "Rounds 22 and 23 worked the seat-audit surface and round 21 the review-evidence surface."

16. **`<REV>` has to be a commit id.** Impacted check: (b).
    - [obs] `--revision HEAD` makes both commands exit 2 with `E-REVISION-INVALID`. A full commit id works (exit 0 for C1 and exit 1 for C2 at `10b45f0`).
    - Suggested wording: "`<REV>` = a landed, pushed commit id (not `HEAD`)".

[unk] I did not judge whether the P1 to P5 premise facts in the capture are correct; other seats own the capture, mirror and hook reviews. No new SOURCES row is drafted here, because I opened no public page this session.

Scope: read=SCORECARD.md (axes table, round 12 to 24 sections), corpus/lessons/round-23-verifier-spotcheck.md, tools/report-red-causes.py, tools/check-pause-gate.py, tools/check-seat-bindings.py:40-119, tools/_revision.py (grep), PROVINCE.md:1-34, falsify-limit.json, w1-spec.json (grep), git grep of corpus, SKILL.md and LOG.md at f169b3ba, ~/.agents/skills/godspeed; wrote=.ufo/waves/round-24/w1/CritClaimSizing.md, plus three throwaway outputs outside the lane at /tmp/crit-rc-{f169b3ba,674891d,HEAD}.json, which were then removed (a contract slip, disclosed); executed=git rev-parse/log/status/ls-tree/show/diff/grep (read-only), python3 tools/report-red-causes.py --revision {f169b3ba,674891d,HEAD,10b45f0}, python3 tools/check-pause-gate.py --revision {f169b3ba,674891d,HEAD,10b45f0}, inline python3 replays of check-seat-bindings.evaluate/requested_path at f169b3ba and check-pause-gate.evaluate with in-memory gates A and B, sha256sum of both capture files
Installs: none
