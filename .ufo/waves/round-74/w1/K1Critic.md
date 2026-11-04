# K1Critic — round-74 w1 — declaration critique & attack (scoped summary)

Basis: declaration commit `e51fb49d`, base `d749a625`, tip `810daf13`. Full report + evidence:
`.ufo/waves/round-74/w1/K1Critic/report.md` and `.ufo/waves/round-74/w1/K1Critic/evidence/attacks.txt`
(battery.py execution receipts). Zero repo bytes mutated, zero tools installed, scratch clean.

## Findings by Severity

1. **HIGH (Unfalsifiable Conjunct) — C1 counter `snapshots_used >= TARGET_SNAPSHOTS` is mathematically unfalsifiable.**
   In `tools/count-uf-rows-r74.py` line 237, `len(snapshots_used) >= TARGET_SNAPSHOTS` in `met` is strictly entailed by `len(parsed_rows) == 6` and `findings == 0` (enforcing `MAX_SNAPSHOT_REUSE = 2`). By the pigeonhole principle ($\lceil 6/2 \rceil = 3$), any passing 6-row note must use $\ge 3$ snapshots. Neutralizing the conjunct (`and True`) leaves all 13 selftest cases passing with 0 failures (`battery.py` Attack 5).
2. **HIGH (Sizing Contradiction) — Frozen claim text and predicate threshold disagree by two registry rows.**
   `SCORECARD.md:6092` explicitly claims: `"Rows UF1-UF6, sources S309-S311 (v262 unit-file.c, load-fragment.c, unit-file.h)"` — exactly 3 sources ($308 + 3 = 311$). But the kill rule at line 6092 enforces `registry < 313` (+5 rows), line 6095 states `"five registry rows"`, and `w1-spec.json` tasks SC2Sources with S309-S313. An honest implementation following the claim text (adding S309-S311) fails the round on `registry < 313`.
3. **HIGH (Answer-Key Leakage) — C2 instrument embeds verbatim solution blocks in selftest.**
   `tools/check-r73-routed-r74.py:123-142` embeds literal strings `good_lesson` and `good_log`. Extracting and evaluating these strings passes the checker directly (`ROUTED_STALE=0 ROUTED_OK=2/2` rc 0; `battery.py` Attack 2). An author can trivially copy-paste the selftest constants to satisfy C2 without investigating round-73 defects.
4. **MEDIUM (First-Match Shadowing) — C2 checker blocks honest EOF append in LOG.md.**
   `check_r73_log_count` in `tools/check-r73-routed-r74.py` searches blocks forward and breaks on the first match. The existing Round 73 entry matches the fallback `("Round 73" in b and "correction" in b.lower() and "selftest" in b)` and lacks token `14`. An appended correction at EOF (the declared C2 shape) is never evaluated, failing with `missing token '14' in LOG.md correction block body` (`battery.py` Attack 8).
5. **MEDIUM (Semantic Detachment) — C1 counter verifies lexical tokens only, accepting negated statements.**
   `tools/count-uf-rows-r74.py:193-200` enforces only token overlap count and verbatim quote existence. A candidate note asserting the direct opposite of systemd logic ("unit search paths NEVER process in priority order", "Unit symlinks PERMIT self aliases") evaluates to `rc=0 met=1 findings=[]` (`battery.py` Attack 4).
6. **LOW (Pure Lexical Channel) — C2 checker accepts explicit denials and token jumbles.**
   `tools/check-r73-routed-r74.py` checks raw substring presence without directionality; explicit denials ("We strictly reject that install.c:2383 supersedes 2387") and raw token dumps (`11 12 13 14`) pass `ROUTED_STALE=0 ROUTED_OK=2/2` (`battery.py` Attack 3).
7. **LOW (Dead Code) — Unreachable disjunct `or rinfo["kind"] == "own-work"` in C1 counter.**
   `count-uf-rows-r74.py:205` contains `if rinfo["kind"] not in KINDS or rinfo["kind"] == "own-work":`. Because `"own-work"` is not in `KINDS`, the second disjunct is dead code (`battery.py` Attack 6).

## Controls Evaluation

- **Absence controls** (`before/absence-controls.txt`): Note absent (rc 128), C2 stale (rc 1, `ROUTED_STALE=2 ROUTED_OK=0/2`). Held.
- **Held-ground sweep** (`before/held-ground.txt`): 0 matches for plane tokens across base tree. Held.
- **Pinned sources** (`before/src/`): Exact sha256 match for `unit-file.c`, `load-fragment.c`, `unit-file.h` matching host systemd 262.1-1-arch. Held.
- **Instruments**: Both sha256 digests (`94d46a5e...`, `2da4ff1f...`) match SCORECARD.md byte-for-byte; selftests pass hermetically (13 cases and 6 cases). Held.
