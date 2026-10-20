# FxTypeBlindFix — R17-TYPE-BLIND fix

**Verdict: FAILS.** Claim attacked: `round-17.md:37` says "the v1 DEGRADED record fails re-derivation against the typed evidence".

- [obs] A literal v1 record does go red, but only from schema and vocabulary: `schema` other than v2 gives BOOTCHAIN-SCHEMA (`check-boot-chain.py:353`). `derive()` (218–244) can never return `DEGRADED`, so lines 334–336 raise BOOTCHAIN-VERDICT. Neither red depends on the `dirs:` line or on any typed line.
- [obs] Nothing ever checks `image_new_root` against the evidence. It is `str?` with no enum (line 75). `entry_findings` (299–326) and `block_issue` (256–275) do not test it, and `extraction_blocks` has no entry-type field.
- [obs] No selftest case uses DEGRADED. `derivation-image-dir` (904–906) goes red only because the recorded verdict is left stale.
- [inf] Counterexample that stays green: in fixture entry `snap`, set `image_new_root:"directory"` (the type-blind reading) and `verdict:"UNTESTED"`. Its evidence already cites `dirs: new_root sysroot` (lines 673, 728). Derivation gives UNTESTED, so the case is green. Dropping `ref("emulation",2)` as well also stays green. The real JSON also cites the `dirs:` line (`boot-chain-capture.txt:181`, `boot-chain-r17.json:92`).
- [unk] I ran none of these cases; no EXEC authorization.

**Impacted axes:** C1 depth, QUALITY 25.

**Smallest safe fix:** make `image_new_root` an enum. Require a cited typed line for it (`-> sysroot` or an `ls -l` mode); a `dirs:` line does not count. Add the selftest cases `restored-defect-type-blind` and `restored-defect-degraded`. Otherwise, reword the lesson to "red by verdict vocabulary only".

Scope: executed=none
