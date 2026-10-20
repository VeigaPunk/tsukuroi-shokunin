# SimplifyRunner — r19 runner carry-over

[obs] round-18/measure/run.py:1-204; repair.py:1-101. Baseline lane has exactly 14 tools files (.ufo/waves/round-19/build/spec.json:278-281 names the r19 runs).

## Keep (minimal)
| run.py lines | Keep for |
|---|---|
| 1,6-8,11-14 | shebang; hashlib,json,os,Path,subprocess,sys,tempfile |
| 16,18-24 | LANE, MEASURE, argv TIP/outdir, mkdir, ENV, results |
| 27-42 | record(): DEVNULL stdin, stdout/stderr spill, JSON parse, results.json append (drop env_override param) |
| 45-53 | mktemp clone --no-hardlinks, remove origin, detach TARGET, master ref |
| 61-66 | evaluator-digests.json sha256 map |
| 201-202 | live-lane census, labelled live |

[inf] Replace 54-60 (hardcoded 14 tools) with sorted `tools/*` enumeration at TARGET: .sh→bash, sha256, `--selftest`, absent→skipped.

## Delete (round-18-only)
- :2-4 r18 docstring.
- :9-10 `re`, `shutil` (unused once below goes).
- :17 BASE=842a5312… → 452a0546….
- :54-60 stale tool list (re-adds r17/r18 gates the r19 item excludes).
- :68-79 C1/C2/C3 r18 matrix: check-boot-chain --statement-corrections, check-revision-binding, check-appended-notices on statement-corrections-r18/freshness-recheck-r18, recheck-aur, stale-baseline.
- :80-84 legacy-boot, legacy-freshness, recheck-all, exec-log host-capture-r18.txt.
- :85-89 round-18 wave paths (keep exists() guard, swap to round-19).
- :90-113 r18 protected identities, eight-primary-path set, 49/48 arithmetic, r18 baseline prefixes.
- :114-139 bytecode guard: positive control + 12 consumer repeats.
- :140-155 check-boot-chain typed-source mutant.
- :156 r5-literal-arithmetic.
- :157-175 elephant count, 99-line capture replay, capture-script digest.
- :176-200 inline SKILL parse asserting 13 rows / five-probe — check-registry-coverage.py owns this; carrying it forces red.

repair.py: delete :1-101 entirely. Specifics not to carry: :38-39 hardcoded initial SHA `c0f6303…`; :49-61 r18 after-runs; :62-75 SOURCES column-4/8 histogram; :76-99 fixed_inputs equality + r18 prefix checks; :100-101 census duplicate. [inf] One record() schema only; reruns come from run.py's outdir argument.
