VERDICT: defect-found

Seat R51RevSeparability (w1, uncounted). Scope: claim sizing (rule 9), causal separability, do-nothing controls for C1/C2/C3. Base c0ad548a93425a3bf8813d28d92f26fe2f64b9d4; freeze 2732ee6c06108c031c4d8043239b994e0504eb2f. Read-only; scratch fixtures under /fast/scratch/hyaku/tsukuroi-r51/R51RevSeparability (removed).

## Sources of the rules
- Rule 9 (`.ufo/prompts/tsukuroi-round-51.md:529-545`): "Declare each after-state as one concrete value that the closure can re-derive with one command over committed bytes"; "Use no universal clauses ... unless the counting command enumerates the full set"; "A target must be one a do-nothing control cannot reach ... if it meets the target, the counter or target is wrong — fix it before data."
- Frozen claims: `.ufo/waves/round-51/frozen/FROZEN.md` claims table. Frozen tool hashes match the freeze bytes (`sha256sum` of `git show 2732ee6c:tools/*r51.py` equals `FROZEN-hashes.txt`; battery.py `12eeffb5…` matches).

## Pre-freeze receipts were produced at base by the frozen counters
- `before/c1-at-base.json`, `c2-cheats-at-base.json`, `c3-at-base.json`: "base" = c0ad548a. The only commit touching `tools/` since base is 2732ee6c (`git log --oneline c0ad548..2732ee6c -- tools .ufo/waves/round-51/before` → one line), so the receipts were produced by the frozen counters.
- Reruns at base (fixture `git clone --shared` checked out at c0ad548, frozen counters copied into the worktree) reproduce the receipts exactly: C1 `identical`; C3 `before-receipt == rerun: True`; C2 `real_pass 1 cheats 4 cheats_rejected 4 r50_cheats_rejected 0 PASS` on both.
- The base has no r51 file (`git ls-tree -r --name-only c0ad548 | grep -i r51` → empty).

## (a) One concrete value per after-state; universal clauses
1. C1 — predicate is six concrete values; `seats_ok == 18` enumerates the fixed 18-seat universe (`check-scrub-admission-r51.py:72-73, 381-382`). Not a universal clause.
   DEFECT (command not bound to committed bytes): the frozen command passes `--wave-dir`, `--results-file`, `--dispatch-file`. `read_text`/`load_json` read a file from disk when an override is given (`check-scrub-admission-r51.py` lines 120-147), and `bind_seat` reads seat reports from `wave_dir` on disk (lines 275-278). Only when the overrides are omitted do reads come from `show(lane, rev, …)` (lines 278-281). So the frozen command is not "over committed bytes": it re-derives from the working tree. Fix options for the amendment: drop the three flags so the counter reads `REV:.ufo/waves/round-51/w2/…` (requires the w2 wave committed at the counted REV), or have the counter refuse overrides unless `--control` as C3 does.
2. C2 — `cheats == 4` is a constant of the scorer (`score-counter-cheats-r51.py` predicate line). The counter under test is read from the worktree (`counter = os.path.join(lane, a.counter)`, line ~86-87), not REV; the census is read at REV (`git show REV:tools/tsukuroi-census.sh`). Frozen claim is not fully REV-bound on the counter side; acceptable only if the closure checks out REV.
3. C3 — DEFECT, universal clause not enumerated: `digests_bound_ok == 10` (C3 claim: "the `Portable digests` list" bound to the registry). `digests_bound()` in `check-adjacency-table-r51.py` (~lines 146-160) skips any line whose OUT id is unknown to the registry or already `seen`, and counts only the first line per id. It never checks the list length or that every list line binds. Attacks, both run with `--control --province-file` (control mode, so no override block):
   - extra unknown line `- OUT-011 … @ 000… sha256 000…` inserted after OUT-010 → `digests_bound_ok 10`, `verdict CONTROL-PASS` (`attack-extra-digest.json`).
   - wrong duplicate `- OUT-010 … @ 000… sha256 000…` inserted after the correct OUT-010 line → `digests_bound_ok 10`, `verdict CONTROL-PASS` (`attack-dup-wrong.json`).
   The battery does not cover these: C3 K5 alters an existing line's digest (`battery-summary-r51-freeze-c3.jsonl`), it does not add or duplicate a line.
   Also `live_quote_ok >= 8` (C3 target) is measured against each sibling's live HEAD (`check-adjacency-table-r50.py` lines ~152-163, `git -C repo rev-parse HEAD`), so the value moves when a sibling commits, with no lane byte changing. Re-derivable from sibling repos, not from REV.

## (b) Universal clauses
- C1: none beyond fixed enumerations (rows GR1–3, 18 seats, 3 marks). OK.
- C3: `bare_ranges == 0` is over the 7 ADJ rows (`adj_rows == 7` is asserted, OK). `display_bound_ok == 10` and `quote_specific_ok == 10` are over the 10 OUT ids (`git show c0ad548:PROVINCE.md | grep -o 'OUT-[0-9]\{3\}' | sort -u | wc -l` → 10), OK. `digests_bound_ok == 10` is the defect above.

## (c) Causal separability
- C1 output is identical with C2/C3 counter files removed from the worktree: `c1-frz.json` vs `c1-frz-noC23.json` (`cmp` → identical; `git status` showed the three deletions only). C1 counter imports only `lint-grounding-r51.py` and reads SOURCES/entry/snapshots at REV.
- Cross-reference grep over the five freeze counters (`grep -o` on `git show 2732ee6c:tools/<f>`): C2 scorer references only `check-selftest-matcher-r51`, `check-selftest-matcher-r50`, `tsukuroi-census.sh`; C3 counter references only `check-adjacency-table-r50` (loaded from HERE) and PROVINCE/registry at REV. No C2 file references a C1 or C3 counter and vice versa. Separable.
- C2 and C3 reruns at base do not depend on C1 bytes (base has none; reruns identical to receipts).

## (d) Do-nothing controls (base bytes + frozen counter; then the cheapest reachable control)
- C1 base + frozen counter (`c1-base-rerun.json`, identical to `before/c1-at-base.json`): `structural_ok 1, lint_ok 0, quotes_ok 2, verdicts_ok 0, seats_ok 0, marks_ok 0, verdict FAIL`; `lint.per_row.GR1` quote_bad 1 (`quote S246 cmdline.c:147: not the whole line; line is '* potentially suffixed with K, M, G, T, P, E.'`). Target not met by base. Matches expectation (lint_ok 0).
- C2 — SAY PLAINLY: base bytes + frozen counter already meet the full target (`c2-base-run.json`, identical to `before/c2-cheats-at-base.json`): `real_pass 1, cheats 4, cheats_rejected 4, r50_cheats_rejected 0, verdict PASS`. The claim's measured change is therefore the counter alone; the lane bytes do not move the value. Control with round-50 counter in the claim slot (`c2-r50slot-run.json`, `score-counter-cheats-r51.py --counter tools/check-selftest-matcher-r50.py`): `real_pass 1, cheats 4, cheats_rejected 0, r50_cheats_rejected 0, verdict FAIL` (all four r50 cheats PASS, so r50 rejects 0 of 4). This control does not reach the target. Discrepancy: `battery-summary-r51-freeze-c2.jsonl` K0 records `cheats_rejected 1` for the same control; my rerun records 0. Both FAIL the predicate, but FROZEN.md's "rejects 0 of 4" conflicts with the battery receipt. Needs an explanation or a re-run recorded by the L1.
- C3 — SAY PLAINLY: base bytes + frozen counter already meet every clause (`c3-base-rerun.json` = `before/c3-at-base.json`): 15 of 15 clauses true (`adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7, registry_ok 7, anchors_checker_rc 0, quote_at_pin_ok 9, live_quote_ok 9, stub_fails 1, display_bound_ok 10, quote_specific_ok 10, digests_bound_ok 10, display_forge_fails 1, override_blocked 1, r50_blind 1`). The `display_forge_fails`, `override_blocked`, `r50_blind` and `stub_fails` legs are counter-internal forgery fixtures, not lane state. Control with round-50 counter in the claim slot (`c3-r50-base.json`, `check-adjacency-table-r50.py --revision c0ad548`): 9 of 15 clauses true; six missing as fields (`display_bound_ok, quote_specific_ok, display_forge_fails, override_blocked, digests_bound_ok, r50_blind`). That control does not reach the target. The sensitivity control that does exist is battery K0 (false displayed OUT-009 commit → `display_bound_ok 9, display_forge_fails 0, r50_blind 0`, CONTROL-FAIL; `battery-summary-r51-freeze-c3.jsonl`). The C3 "before" is therefore not a measured before: it is the new counter's own PASS.
- Minor: `c3-r50-base.json` reports `"base": "b866a1d3…"`, the r50 counter's own constant, not the run revision. Harmless, noted for receipts.

## Recommendations for the planner (L1 decides; nothing here is a counted verdict)
1. C2 and C3: by rule 9 the targets are met by base bytes + frozen counter. Either re-declare their before-state as the round-50 counter in the claim slot (C2: 0/4 rejects, FAIL; C3: 9/15, FAIL) so the claim is a measured before→after, or record them openly as instrument claims whose before is the counter's own legs.
2. C1: remove `--wave-dir`/`--results-file`/`--dispatch-file` from the counted command, or make the counter refuse overrides without `--control`, so the counted value is re-derived over committed REV bytes.
3. C3: `digests_bound` lacks a length check and per-line completeness; the two attacks above pass. A counter edit is a change to a frozen counter and needs the L1's amendment decision before data.
4. Reconcile the C2 K0 receipt (1) with the rerun (0) and with FROZEN.md ("rejects 0 of 4").
5. C1 marks leg is 0 at freeze (`marks_ok 0`, `marks.entry/readme/skill false`): expected, the amendment must add the mark strings.

## Did not do
- Did not run the full C1 predicate (no w2 cohort exists yet); verified only the counter legs that do not need seats.
- Did not run the battery or the C3 K-pass beyond reading their summaries.
- Did not run C2 with `--runs > 1`.

## Commands and environment
- `git clone -q --shared` fixtures under scratch; `git -C <fixture> rev-parse --show-toplevel` equalled the fixture path before use. No commits made.
- Counter runs: `python3 tools/check-scrub-admission-r51.py --revision c0ad548 --lane fx-base`; `python3 tools/check-scrub-admission-r51.py --revision 2732ee6c --lane fx-frz` (and with C2/C3 counter files removed); `python3 tools/check-adjacency-table-r51.py --revision c0ad548 --lane fx-base` (and with `--control --province-file` attacks); `python3 tools/check-adjacency-table-r50.py --revision c0ad548 --lane fx-base`; `python3 tools/score-counter-cheats-r51.py --revision c0ad548 --scratch <dir> --lane fx-base` (≈372 s) and with `--counter tools/check-selftest-matcher-r50.py` (≈115 s). One selftest-bearing command at a time.
- Receipts copied to `.ufo/waves/round-51/w1/R51RevSeparability/` (48 KB: c1-*.json, c2-*.json, c3-*.json, attack-*.json, base-tools.sha, frz-tools.sha). Scratch removed.
- Tooling installed: none.
