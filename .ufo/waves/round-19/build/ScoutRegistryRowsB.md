# ScoutRegistryRowsB — C3 rows 8–13 + tools/ census

Operative table `## Gate and probe registry — round18 superseding current rows` (SKILL.md:1952), rows :1965–:1970. Model: commandcode/deepseek/deepseek-v4.1-flash.

- boot-chain-audit (:1965, probe): exists; `--selftest` tools/boot-chain-audit.sh:1222, dispatch :1234; map matches source :77. Exit 1 unreachable ("no v2 verdict maps to it" :80–81; `audit` 0/2 only :784–796; usage/root/fixture/missing-cmd also 2 :1242–1281). [obs]
- freshness-r17 (:1966, gate): `--selftest` :386; 0/1/2 :54; STALE-UNFLAGGED :292→FAIL :296; R17-FRESH-MISSING FAIL :268; E-REGISTRY-* CANNOT :265/:273. Consistent. [obs]
- appended-notices (:1967, gate): `--selftest` :434; 0/1/2 :24; NOTICE-MISSING FAIL :317; STALE-UNFLAGGED :258; E-REGISTRY-* CANNOT :315/:328; default `--registry` :27 matches row; C1 same flag with statement-corrections-r18.json (selftest :836). Consistent. [obs]
- recheck-commands (:1968, gate): `--selftest` :713; 0/1/2 :57; named IDs :531/:545/:554 and :578. DEFECT: closed "or" map omits exit-1 RECHECK-POINTER-UNRESOLVED :557 and RECHECK-STEER-SAFE-INVALID :506/:512/:534/:537 (FAIL via :597). [inf] gap to carry into check-registry-coverage.
- seat-scope (:1969, gate): `--selftest` :234; 0/1/2 :38; IDS :42–43 exactly the four listed, all exit-1. Entry cell omits `--worktree` :233 (round-17 :1901 had it). [obs]
- revision-binding (:1970, gate): `--selftest` :522; 0/1/2 :59; PASS iff consistent==TOTAL. probe→gate covered by :1954 withdrawing "probe". Consistent. [obs]

tools/ (14 files): registered — boot-chain-audit.sh:1965, check-appended-notices.py:1967, check-boot-chain.py:1964, check-freshness-r17.py:1966, check-locator-clarification.py:1961, check-recheck-commands.py:1968, check-revision-binding.py:1970, check-root-dac-correction.py:1959, check-seat-scope.py:1969, check-section-citations.py:1963, check-source-scope-correction.py:1960, measure-update-recheck.py:1962, tsukuroi-census.sh:1958. No row: tools/_revision.py only (closure defect 2, corpus/lessons/round-18-verifier-spotcheck.md:261). tools/check-registry-coverage.py absent at baseline. [obs]

Deviation: NO-EXEC item; bash used only for read-only grep/awk/sed reads of lane files — no host access, git or writes.

Scope: executed=grep, awk, sed, echo, cd (read-only, lane files)
