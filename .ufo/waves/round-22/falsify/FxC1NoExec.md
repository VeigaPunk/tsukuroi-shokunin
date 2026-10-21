# FxC1NoExec — round-22 source-only falsification

Target: `.ufo/waves/round-22/candidate/tools/check-boundary-contract.py` (175 lines, read in full as raw source). Attack: NO_EXEC DENY to ALLOW. Required outcome: count 5 with an exact mismatch, not count 6.

## Method and limits

- Read-only. No commands, tests, imports, compiles, fetches, or delegation. No candidate file was modified and no fixture was written to disk; every fixture below is a textual description.
- The declared hash `1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485` came from the assignment. It was not recomputed because hashing requires execution, so byte identity with it is unverified. The read tool's `#6D78` is a snapshot tag, not a SHA-256.
- Read: the target (full), `_revision.py` lines 1-203 (the `bind` path, lines 172-192, is used), the seat-boundary JSON and Markdown, `preregister.json`, `host-tool-boundary.json`, `check-review-snapshots.py` (header only; not on this path), and the godspeed skill.
- Expected verdicts are static derivations from source. Observed runtime: none. Statements about GFM/CommonMark rendering come from the spec rules, not from rendered output, and are marked [INFERENCE].

## 1. Requested attack: holds for every single-cell NO_EXEC edit

Every single-cell edit to the NO_EXEC decision gives the same static result: exit 1, status FAIL, `validated_boundary_decisions` 5, and exactly one finding, `BOUNDARY-DECISION-MISMATCH` at site `NO_EXEC`.

| Variant (only NO_EXEC edited) | Static result |
|---|---|
| JSON `decision` DENY to ALLOW; prose unchanged | count 5, exit 1, mismatch at NO_EXEC |
| Visible prose cell DENY to ALLOW; JSON unchanged | count 5, exit 1, mismatch at NO_EXEC |
| Both surfaces flipped | count 5, exit 1, one finding (lines 89-90 add once per row) |
| Prose cell ALLOW with an inline HTML comment (line dropped by lines 42-47) | count 5, exit 1 (matches is empty) |

Bounded reason count 6 is unreachable from these edits:

- Line 87: `correct` requires the JSON row's decision to equal `DENY`.
- Lines 82 and 88-89: `matches` requires exactly one visible prose row for NO_EXEC, equal to the expected cells.
- Lines 66, 70, 83: duplicate JSON keys raise, exactly six unique IDs are required, and `by_id` is built from the single parsed object, so no shadow row can carry DENY.
- Lines 91-92: the count increments only when both checks pass.
- Lines 75 (host), 80 (source rows) and 93 (scope) are unaffected by a NO_EXEC edit, so the finding set is exactly one.

Expected fixture verdict (derived, not executed): exit code 1; `status` FAIL; `validated_boundary_decisions` 5; `total_decisions` 6; `findings` = `[{"id": "BOUNDARY-DECISION-MISMATCH", "site": "NO_EXEC"}]`. `main()` (lines 150-171) additionally adds `revision`, `branch` and `branch_tip`, with keys sorted. Observed runtime: not observed.

Note: the selftest does exercise NO_EXEC flips (line 112 sets FORGED on index 0; line 125 `wrong-table` replaces the first `| DENY |`, which is the NO_EXEC row). Its pass test (line 134) checks only the exit code and finding ID, never the count. The count-5 result is therefore source-derived and untested.

## 2. Counterexamples to "a NO_EXEC ALLOW cannot reach count 6"

These are prose-only edits; the JSON stays DENY. They go beyond the literal single-cell flip in section 1, so they do not contradict it. They show that `validated_boundary_decisions` = 6 is not a sound statement about what the rendered document asserts.

**CX1 — in-place rendered ALLOW plus a checker-visible DENY decoy (static: exit 0, PASS, validated 6).**

1. In the NO_EXEC table row, the decision cell becomes `ALLOW` followed by an inline HTML comment (for example `ALLOW <!-- note -->`). Only that cell changes.
2. Directly after the table's terminating blank line, insert four lines: (a) a line of three backticks; (b) three backticks immediately followed by the word `text`; (c) the original NO_EXEC DENY row, byte-identical; (d) a line of three backticks.

Checker trace: lines 42-47 drop the edited row, since the comment opens and closes on one line. Lines 48-51: (a) opens a fence; (b) closes it, because line 51 compares only the marker character and ignores the info string; (c) is appended at lines 53-54 and enters `cells` at line 82, so `matches` equals the expected row and the count increments; (d) reopens the fence and hides the rest. Line 93 passes from raw text. Result: no findings.

GFM trace [INFERENCE from CommonMark/GFM rules]: the table ends at the blank line; (a) opens a code block; (b) is content, because a closing fence may not carry an info string; (c) is code text; (d) closes the block. Rendered output: the NO_EXEC table row reads ALLOW, and a code block shows the DENY row as text.

Intended verdict (my inference from the docstring and the LIMIT scope): FAIL with `BOUNDARY-DECISION-MISMATCH` at NO_EXEC, because the rendered document asserts two NO_EXEC decisions.

**CX2 — duplicate NO_EXEC row hidden by an inline comment (static: exit 0, PASS, validated 6).**

Keep the visible DENY row. Add a second NO_EXEC row to the same table whose decision cell is `ALLOW` plus an inline HTML comment. Lines 42-47 drop it, `matches` holds one DENY row, and the count is 6. GFM renders both rows [INFERENCE].

**CX3 — free-text assertion outside the table (static: exit 0, PASS, validated 6).**

Add a paragraph stating that NO_EXEC is ALLOW for hash-only checks. No check reads free prose for decision IDs: cells come only from table lines (line 82), the scope check is a phrase test (line 93), and the JSON is authoritative. This is by design, but the C1 wording "six validated decisions" can be read as covering the whole document.

## 3. Root causes (source-visible)

- Lines 41 and 48: fence detection runs after `lstrip()`, so an indented fence-like line of four or more spaces toggles the checker's fence state. CommonMark treats such a line as indented code, not a fence [INFERENCE for renderer].
- Line 51: the closer check compares only the marker character. A line of backticks followed by text closes a fence; CommonMark closers take no info string [INFERENCE for renderer].
- Lines 42-47: any line containing an HTML comment opener is discarded whole, including visible cell text on that line.
- Line 82: the column-0 pipe requirement hides rows. Combined with the two items above, it is the lever for CX1 and CX2.
- Line 93: the scope sentence is searched in raw text, including hidden regions.
- Line 87: only five row keys are read; extra keys are silently ignored (A3).

## 4. Adjacent findings (not specific to NO_EXEC)

- A1 (low): line 93 accepts the scope sentence from hidden content. The JSON scope check on the same line still applies, so this gap is partial.
- A2 (low, test gap): the selftest asserts exit code and finding ID only (line 134). There is no count assertion and no fixture for CX1-CX3.
- A3 (info): extra row or top-level keys are ignored. Any consumer that reads them is outside this seat's read set and is unverified.
- A4 (trivial): `import hashlib` (line 6) is unused in this file.
- A5 (info): `git_read` (lines 140-147) and `main` (lines 150-171) validate committed bytes at the landed SHA, so working-tree edits are invisible until committed. This is by design.

## 5. Recommended hardening (planner decides; not applied)

1. Census raw lines, not visible lines: for each decision-ID token, every raw line containing it must be the single expected row. This closes CX1-CX3.
2. Use a CommonMark-faithful fence and comment scanner, or fail on any ambiguous fence or comment line that touches a decision row.
3. Run the scope-sentence check on visible text.
4. Assert `validated_boundary_decisions` in the selftest, and add negative fixtures for CX1-CX3 and for each variant in section 1.
5. Pin the exact key set for rows and the top level.
6. Remove `import hashlib`.

## 6. Verification gaps

- The declared hash was not recomputed.
- No runtime observation was made. GFM rendering is spec-based [INFERENCE].
- Not read: `_revision.py` lines 204-440 (selftest body, off the bind path); `check-review-snapshots.py` beyond its header (off this path); the C2 and C3 tools (not in the read set); renderer-specific hidden HTML (not analysed).

## 7. Hand-off

- This seat ran no checks. For the main agent after landing: run `tools/check-boundary-contract.py --selftest`, then `--revision <landed>`, once fixtures CX1-CX3 and count assertions have been added.
- No installs, tool changes, or lane Git/jj state were touched.
