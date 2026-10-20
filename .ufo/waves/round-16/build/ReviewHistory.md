# ReviewHistory: round-16 append-only retention

**Status: not implemented.** Absent: `tools/check-section-citations.py`, `corpus/knowledge/section-citation-errata-r16.{md,json}`, `.ufo/waves/round-16/build/frozen-cases.json`, all R16 notices. Targets still equal db68e62: `host-health-report-r3.md` (38589 B, sha256 `bfd1c422…`), `update-safety-v3.md` (33401 B, sha256 `84b3d6c5…`).

**F1 (high): the specified gate proves presence, not retention.** It resolves heading, row, quote and notice headings, with no baseline pin. These falsifiers pass:
- Delete the R15-UPDATE-STATE notice (`host-health-report-r3.md:578-599`) and append valid R16 headings.
- Rewrite `:581` "§1 verdict-board row 5" to §0 in place, then append the notice.
- Insert an R16 heading mid-file and edit the tail.

**Precedent:** `check-locator-clarification.py` pins the sha256 of the rstrip'd `0db618a` blob (verified `9f7cc3…`), so a notice placed mid-file changes the prefix and fails. Its JSON check is canonical-value, not bytes, so its "exact bytes" comment overstates.

**Recommendation:** pin db68e62 sha and size per file; at `--revision`, require `current.startswith(baseline)` with a tail holding only the exact notice headings and bodies. Scope locator detection to the two files; `update-safety-v2.md:372` is a legitimate v2 §7 reference.

**Limits:** static `git show` and `sha256sum` only; no gate or selftest run; installs none. Future rounds need per-round pins.
