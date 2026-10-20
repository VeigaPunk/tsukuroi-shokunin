# FxBindMutants

[obs] Axes: C3 operability, detector sensitivity, byte restoration. C3’s 5/5 count SURVIVES; detector coverage FAILS: five killed, one survived.

`D=tools/check-revision-binding.py`; `R=dd15c183f2f2481db67d0234038117a0d5b7034c`. Six no-hardlink clones under `/tmp/FxBindMutants.RuUwPw7j/`: M1=lane; M2–6=m2–m6.

Detectors: `python3 D --selftest` (expected mutant exit=1), `python3 D --tools-revision R`. Each ran pristine/mutated/restored. Pristine/restored: `PASS (23 cases, 23 passed, 0 failed)`, exit=0. All 18 landed measurements: `status=PASS,bound_tools=5,total=5`, exit=0.

| Mutant, D:line | Mutated selftest output | Verdict | Mutated Git-blob SHA-1 |
|---|---|---|---|
| M1 :103 accept HEAD | FAIL 22/23; bind-head got=None | KILLED | 5d7f931794d06520b3f5f7541de50cb79e3bf7c7 |
| M2 :109 skip NOT-LANDED | FAIL 22/23; bind-unlanded got=None | KILLED | 2a5e83b427205f34dca139c789683e7ee3343535 |
| M3 :245 bound=tip_code!=2 | FAIL 18/23; mixed-count got=5 want=3 | KILLED | 55141a8e48736afd6ba1c2c8e8a4f769d9b3c253 |
| M4 :244 revision self-comparison | PASS 23/23 | SURVIVED | 649c8afb0b4e9c33e4d291d88b3dc357d2e477be |
| M5 :233 ignore HEAD finding | FAIL 21/23; wrong-id-count got=5 want=4 | KILLED | 3597c6121459a5a3b0e6e1b7d89ba5b31174cf02 |
| M6 :112 skip NOT-PUSHED | FAIL 22/23; bind-not-pushed got=None | KILLED | b113c8df8d6ea2bb8aeb8b22e1cb95363b5c8ed4 |

Killed selftests exited 1; survivor exited 0. [obs] Every pristine/restored blob: `eca7bc93bfe342bbe2b9d3f65ad7dc364fb92f94`; exact restoration confirmed. Lane source untouched.

[inf] Wrong-revision fixture coverage is missing. [unk] This does not establish incorrect binding by any measured tool.

Scope: executed=mktemp -d,git clone --quiet --no-hardlinks,git rev-parse,git hash-object,python3 tools/check-revision-binding.py --selftest,python3 tools/check-revision-binding.py --tools-revision dd15c183f2f2481db67d0234038117a0d5b7034c
