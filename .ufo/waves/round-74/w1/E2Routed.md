status: done
verdict: C2 repair drafts pass the declared predicate in committed-bytes mode (ROUTED_STALE=0 ROUTED_OK=2/2, rc 0) under the frozen instrument (Form A) and hardened prototype (Forms A and B); base revision d749a625 correctly fails as a true negative (ROUTED_STALE=2, rc 1); 20 tamper probes executed with 14 held, 2 negation-blind survivals, and 4 format-dependent findings; instrument defect F1 (forward-match shadowing of block 158 in check_r73_log_count) and F2 (negation-blindness) recorded with exact receipts.

# E2Routed — C2 repair drafts and tamper probes (r74/w1)

Full report: `.ufo/waves/round-74/w1/E2Routed/report.md`.
Drafts: `.ufo/waves/round-74/w1/E2Routed/drafts/`.
Receipts: `.ufo/waves/round-74/w1/E2Routed/receipts/`.

## Headline

- **Selftest & Base Control**: `python3 tools/check-r73-routed-r74.py --selftest` → `PASS (6 cases, 6 passed, 0 failed)` rc 0 (`receipts/selftest.txt`). Base revision `d749a625` → `ROUTED_STALE=2 ROUTED_OK=0/2` rc 1 (`receipts/base-revision-d749a625.txt`).
- **Fixture Scoring**: Fixture built strictly from committed base blobs at `d749a625`:
  - Base without drafts: `ROUTED_STALE=2 ROUTED_OK=0/2` rc 1 (`receipts/P0b-base-without-drafts.txt`).
  - Base + drafts (Draft 0 + Draft 1 Form A): `ROUTED_STALE=0 ROUTED_OK=2/2` rc 0 (`receipts/P0-control.txt`).
- **Committed-Bytes Mode**: Tested in a dedicated git fixture repository:
  - Base commit: `ROUTED_STALE=2` rc 1 (`receipts/G1-git-base-committed.txt`).
  - Drafts written to worktree but uncommitted: `ROUTED_STALE=2` rc 1 (`receipts/G2-git-drafts-uncommitted.txt`).
  - Drafts committed: `ROUTED_STALE=0` rc 0 (`receipts/G3-git-drafts-committed.txt`).
- **Drafts Verbatim**:
  - `drafts/00-lesson-correction.md` (sha256 `f1d3c3dd…`): Appends `## Correction 3 (round 74, C2 routed repair; append-only)` naming `R73-GATE-QUOTE-LINE-DRIFT`, `install.c:2383` (superseding 2387), `:368-370` (superseding :367-370), `:237-238` (superseding :236-238), and `:238-239` (superseding :238-240).
  - `drafts/01-log-correction.md` (Form A, sha256 `37fc80c2…`): Appends unheaded bullet item within Round 73 entry in `LOG.md` naming `R73-LOG-COUNT-STALE`, mid-wave counts 12 and 11, and restating final committed instrument counts 13 and 14. (Bypasses instrument defect F1).
  - `drafts/01b-log-correction-h2.md` (Form B, sha256 `72c7d213…`): Appends `## Round 73 — instrument count correction...` heading for use under the hardened checker.
- **Instrument Defect F1 (Forward-Match Shadowing)**: `check_r73_log_count` splits `LOG.md` on `\n##+ ` and searches forward for `("Round 73" in b and "correction" in b.lower() and "selftest" in b)`. Block 158 (the existing round 73 entry) already matches all three words, but lacks `14`. Thus any appended `## ` block (Form B) is shadowed and fails with `missing token '14' in LOG.md correction block body` (`receipts/F1-form-b-h2-defect.txt`). Hardened checker prototype using reverse search (`reversed(blocks)`) or prioritizing `R73-LOG-COUNT-STALE` passes both forms (`receipts/hardened-checker-receipt.txt`).
- **Tamper Probes**: 20 probes executed (`receipts/probe-summary.txt`):
  - 14 held with named failure diagnostics (missing heading, heading-only tokens, missing specific line tokens, missing counts, denial replacements, truncated ranges, swallow traps, empty files).
  - 2 survived due to lexical negation-blindness (P7a, P7b: appended denials).
  - 4 format-dependent survivals in Form A (P5a, P5c, P5d: tokens 13, 12, 11 already present in block 158; Form B correctly requires all four under hardened checker).
- **Independent Grounding**:
  - S306 quote `"path = path_make_absolute(*name, config_path);"` verified at line 2383 (not 2387) of `before/src/install.c`.
  - S304 quote anchors verified at `:368-370`, `:237-238`, and `:238-239` in `before/src/systemd.unit.xml`.
  - Final round 73 instrument counts verified: `count-ul-rows-r73.py` at 13 cases (`MAPLIST`), `check-r72-routed-r73.py` at 14 cases (`TITLE-TOKEN`).
- **Host & Environment Guards**: Zero lane mutation, no PATH alterations, no commits. Scratch deleted before yield.
