# ScoutRegistryRowsA — C3: round18 registry rows 1–7 vs tools/

Model: commandcode/deepseek/deepseek-v4.1-flash.

Current rows: SKILL.md:1958–1964. All seven entry-command files exist in tools/ [obs].

Self-test spelling: all seven cells say `--selftest`, each accepted by its source — tools/tsukuroi-census.sh:2618 (usage :475), tools/check-root-dac-correction.py:538, tools/check-source-scope-correction.py:620, tools/check-locator-clarification.py:478, tools/measure-update-recheck.py:743, tools/check-section-citations.py:438, tools/check-boot-chain.py:838 [obs].

Kind/verdict agreement, 6/7:
- host-census gate: exit 0/1/2 map tools/tsukuroi-census.sh:57–58, :2673–2676; usage errors exit 2 (:2628), i.e. could-not-evaluate [obs].
- root-dac-correction, source-scope-correction, locator-clarification, section-citations: documented "0 clean, 1 failed, 2 could-not-evaluate" at tools/check-root-dac-correction.py:4, tools/check-source-scope-correction.py:6–7, tools/check-locator-clarification.py:10–11, tools/check-section-citations.py:27–29; constants 0,1,2 at :31, :17, :23, :38 respectively [obs].
- boot-chain gate: exit map :37, constants :56; `--statement-corrections` :842; default payload `verdicted_kernel_entries` :791; C1 payload `correction_count` :775 [obs].

Mismatch (1):
- SKILL.md:1962 update-recheck declares "1 failed". tools/measure-update-recheck.py defines only `PASS, CANNOT = 0, 2` (:36), documents exits 0 and 2 with no 1 (:4–8), and emit returns PASS for COUNTED/ABSENT else CANNOT (:435). Exit 1 exists only as selftest failure (:722, :729). SKILL.md:1819 already recorded "no 1"; the current cell regresses [obs]. Consumer impact: probe mode can never signal "1 failed" [inf]. Round-18 ledger shows only exits 0 and 2 for this tool (.ufo/waves/round-18/measure/final/results.json `runs`) [obs].

Minor naming drift: SKILL.md:1964 writes "R18-CORR01..04"; tool ids are "R18-CORR-01".."R18-CORR-04" (tools/check-boot-chain.py:77, :85, :92, :99) [obs].

Rejected: update-recheck Kind is correct — "probe" matches its docstring "counting probe", "not a truth gate" (tools/measure-update-recheck.py:1–8) [obs]. Remaining unknown: none blocking; live-mode verdicts were intentionally not executed [unk].

No admission authority; findings only.

Scope: executed=none
