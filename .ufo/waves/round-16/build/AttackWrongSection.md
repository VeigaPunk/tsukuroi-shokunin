# AttackWrongSection — R16 critic

Status: errata JSON/MD and `tools/check-section-citations.py` are absent, so no output was seen. These are concerns, not observed failures.

**Counterexample 1 (notice keeps the wrong section):** Change the JSON quote to another substring of the same row, for example ``"`DEGRADED` (arm vocabulary)"``. Then add the exact notice heading with a body that copies R15 line 581, "The §1 verdict-board row 5 …", and never says §0. The planned checks are heading → unique row → quote ∈ row → heading present, so all of them pass. The planned cases (spec.json) cover missing, wrong heading/row/quote, duplicate, malformed, revision and restored notice, but none covers this. The same works for update-safety-v3 by keeping "§7 rank 1 row".

**Counterexample 2 (wrong file):** In baseline `update-safety-v2.md`, §7 row 253 has `| 1 | Do nothing now |` and contains the quote ``"`-Syu` would be INERT: 0"``. Line 372 there gives the correct citation, "§7 rank 1 row “Do nothing now”". So a v2-path record that is consistent with itself still resolves.

**Axes affected:** correctness, provenance and history.

**Smallest fix:**
1. Pin the path and heading for each id.
2. Fail when the new notice is missing §0/§5, or when it repeats the old locator outside one explicit `superseded:` line.
3. Limit old-locator detection to the two target paths.
4. Add both counterexamples to `--selftest`.
