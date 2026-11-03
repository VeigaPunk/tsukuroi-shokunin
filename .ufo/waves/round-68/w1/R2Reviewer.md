2026-11-03T22:36:58Z
# R2Reviewer — C2 gate draft review (round 68, w1)

Full receipt with commands, excerpts and line numbers: `.ufo/waves/round-68/drafts/c2/R2-attack.md`.
Draft: `.ufo/waves/round-68/drafts/c2/check-knowledge-refs-r68.py`, sha256 `d4390b7aa2c7fa1418ea5ff078f95c3faef19c6d12ecb6473d426a90fe7858d5`.

## Findings (by severity)

1. **HIGH — fail-open on fenced registry rows (FALSIFIED).** `registry_ids_at` (draft lines 163-167, `ROW` line 63) has no fence state, so a `| S999 |` row inside a fenced example in `corpus/SOURCES.md` registers `S999`. Fixture B: registry 285 → 286; every `S999` citation clears (`dangling_count` 9 → 2). Fix: apply the header gate's fence state machine (draft lines 175-193) to the registry parse; add a red selftest case.

2. **HIGH — glued ids evade, contrary to the frozen predicate (FALSIFIED).** `ID = \bS\d{3,}\b` (line 62) drops ids touching word characters. Frozen C2 text says "extracts the `S\d{3,}` ids". Probes: `source: own-work S999a` (`refs []`), `source: S138_S999` (`refs []`), `source: own-work 1S999` (`refs []`). Fix: use `S\d{3,}` as frozen (optionally `(?<![A-Za-z])`); add a red selftest case.

3. **Survives:** (a) committed bytes only, dirty worktree ignored; binding refuses `HEAD` with rc 2. (b) fence rule identical to the header gate; 8 probes agree on line number. (c) `MS999` not an id, as the item states. (d) registry read at the bound revision (A read 285 rows while HEAD was C). (e) trailing-comment ids counted. (f) no raw note text in JSON (grep of fake token: 0). (g) no bytecode, no writes on the run path; selftest uses inherited TMPDIR (same as header gate).

4. **Minor:** `\d` matches Unicode digits (`S٩٩٩` flagged; conservative false positive). Selftest has 19 cases and no glued-id or fenced-registry case, which is why findings 1 and 2 pass it.

## Live base
`$ python3 -B "$S/lane/tools/check-knowledge-refs-r68.py" --revision 42400ec6 --lane "$S/lane"` → rc 0, PASS, note_count 85, sourced 85, ref_count 247, dangling 0, registry_id_count 285. Matches my independent oracle at base.

## Residual risk / verification gaps
- Draft changed during my review (`6dec466a…` → `d4390b7a…`). I re-checked the rule lines, not the whole file. E1Probe should confirm the final version.
- Selftest result (19/19) was on the draft's own fixtures; it does not cover findings 1-2.
- Verdicts 1-2 are against the fixture repos under scratch, which are deleted at exit. The commands and excerpts are in the R2-attack.md receipt.

ATTACKS=9 FALSIFIED=2 LIVE_BASE_RC=0 DRAFT=PRESENT
