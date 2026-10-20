# AttackVacuity — round 15 C1 checker: red reason and clean-fixture vacuity

Axis: depth. Critic only; no files edited outside this report. Checker
`tools/check-locator-clarification.py` did **not exist** at review time (tools/ lists only the
r13/r14 checkers and census), so this attacks the LocatorGate contract against real bytes
and the in-progress ActiveRefs notices (worktree diff, r14 MD/JSON +41 lines each, 04:45).

## Actual baseline defect loci (0db618a; worktree r14 bytes above line 205 unchanged)
- LOCATOR: r14 MD:34 `rendered lines 1266-1267` (source-object sentence); JSON
  `corrections[0].location`; JSON `sources[0].anchor` (S044, line 167). Walk of the JSON
  found exactly these plus the two new `r15_supersession.notices[*].superseded_text`.
- NEGATIVE: r14 MD:41-42 `The opened revision documents no further values for ProtectSystem=`
  (backticked); MD:52-53 `and documents no` / `further values for this option` — **split across
  a line break**: a line-wise `grep 'no further values'` found MD:42 but missed MD:52-53;
  JSON `corrections[0].replacement`.

## Counterexamples (each passes a plausible checker yet proves nothing)
1. **Missing-file red.** If LOCATOR_UNQUALIFIED / NEGATIVE_DOMAIN_UNSWEPT fire on "r15 pair or
   notice absent", baseline is red with the right IDs even if r14 had no defect. r14 precedent
   gates the defect ID on *defect bytes present AND notice absent*
   (`check-source-scope-correction.py:289-319`); copy that, not file presence.
2. **Clean-by-deletion.** Removing `1266-1267` / the absence sentence from r14 silences both IDs.
   Green must also require defect bytes still present (r14's `R14-HISTORY-REWRITTEN`, :291-294).
3. **Unrepresentative clean fixture.** A clean fixture whose r14 literals lack the old defects
   passes without exercising notice gating. Real green retains them *and* repeats them inside
   both notices (MD § R15 supersession; JSON `superseded_text`). Clean must be
   baseline-defect literals + appended notice + new pair, exactly that shape.
4. **Notice ordering mismatch.** ActiveRefs appended the MD notice at the **end** (after the sites).
   r14's `md13_notice_ok` demands marker < site and has a FAIL case `notice-after-site`
   (:106, :477). Reusing that makes real green red; a selftest-only "moved" case built on
   preceding placement would pass while the real tree fails. Define "moved" as wrong file /
   outside a `## R15 supersession` heading / JSON outside `r15_supersession`, matching reality.
5. **Over-broad numeric scope.** Real new pair must explain the withdrawn `1266-1267` and quote
   the superseded sentence; true location carries `systemd.exec(5)`, `262.1`, `2026-10-20`.
   A regex like `\d{2,}\s*[-–]\s*\d{2,}` hits `2026-10`. Scope the line-number predicate to the
   new JSON `location` and MD R15-LOCATOR source-object line; include these numerals, the
   withdrawal sentence and r14 MD:35-36 `rendered line break` (no digits) in clean fixtures.
6. **Line-wise negative detection** misses MD:52-53 (above). Normalize whitespace and backticks
   per block (`plain()`, :50-51) before matching.
7. **Self-referential pins.** Fixture quote/heading built from the checker's own constants passes
   tautologically. Cheap independent anchor: require new R15 quote == r14
   `corrections[0].quote` bytes (outside verifier already confirmed it exact, 11 words).

## Live defects in ActiveRefs notices — routed, fixed, re-read
- **Residual un-noticed locator:** JSON `sources[0].anchor` (`rendered lines 1266-1267`) was
  outside both notices. Re-read after fix: R15-LOCATOR `supersedes` =
  `corrections[0].location; sources[0].anchor (S044)`; MD notice names it; anchor bytes kept.
  Checker must still scan `sources[0].anchor` so this coverage is enforced, not just written.
- **False provenance pointer:** notices cited the AF_UNIX/1270 reading at verifier lesson
  `:143-165` (gate-evidence rows). Re-read after fix: MD and JSON now cite § Adjudicated
  concerns and routing item 1, `:233-239`; `143-165` absent from `r15_supersession`.

## Recommended discriminating selftest cases (expected IDs, not just exit)
- `defect-free-r14-no-pair`: r14 literals without defects, no pair/notices → MISSING/HISTORY
  IDs only; **no** LOCATOR_UNQUALIFIED / NEGATIVE_DOMAIN_UNSWEPT.
- `pair-present-notices-absent`: new pair valid, r14 defects, no notices → both defect IDs,
  count 0. With case 1 this proves the red reason is the defect, not the file.
- `anchor-only-defect`: only `sources[0].anchor` retains the bare locator, un-noticed → LOCATOR.
- `negative-across-linebreak`: MD:52-53 shape only → NEGATIVE_DOMAIN_UNSWEPT.
- `clean` as in item 3 with item-5 numerals → PASS, count 2.
L1 baseline evidence should record finding **sites**, asserting LOCATOR ⊇ {MD source-object,
JSON location, JSON sources anchor} and NEGATIVE ⊇ {MD:41-42, MD:52-53, JSON replacement};
baseline count 0 is trivially caused by the missing JSON and is not red-reason evidence.

## Sources / limits / tools
Read: r14 MD/JSON (worktree + `git diff`), `tools/check-source-scope-correction.py`,
`.ufo/waves/round-14/repair/verification.json`, round-14 verifier lesson :141-146, :233-246,
spec.json LocatorGate/ActiveRefs prompts. Python JSON walk and `sed`/`grep` reads only.
Limits: checker unwritten, so no predicate of it was inspected; nothing executed; no source
URL reopened; ActiveRefs bytes may change after 04:45. Tools installed/updated: none.
