# AttackHistoryMask — critic (static; gate/JSON absent, nothing run)

**Counterexamples**
1. **Lexical exemption hides the baseline defect.** Both wrong locators sit under `## R15-UPDATE-STATE … supersession`, after "preserved and remain historical" (host-health:578-581; v3:395-398). `check-locator-clarification.py:103,115` skips hits near supersed/withdraw markers. If that pattern is reused, db68e62 exits 0, not red.
2. **The notice section swallows later text.** Each R16 notice is the last `##` section, so it runs to EOF. If occurrences inside it are exempt, appending "see §1 verdict-board row 5" after the notice still passes.
3. **Count/token collision.** In v3, `§7 rank` appears at :366 (a correct reference to v2's §7) and :398. v2:372 repeats the phrase correctly (§7 heading :244, row :253).
4. **A valid notice masks history loss.** If the history check only looks for the locator line, deleting host-health:596 "No agent install…" stays green.

**Axes:** depth, calibration, provenance.

**Smallest fix:** Key exemption by path, with exactly one baseline occurrence. The baseline file bytes must be an exact prefix (as in the `history_issues` prefix/digest pattern). In the suffix, allow exactly one quoted old_locator, inside its exact notice. Do not use keyword exemptions. Add selftest cases for 1, 2 and 4.
