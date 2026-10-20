# ReviewJudge

Axes: probes, denominator, shared use.

**Verdict:** **SURVIVES** listed D1-D6/core vectors only; **FAILS** exhaustive/off-probe and shared-use claims; **UNPROVEN** at runtime (no execution).

- **High — FAILS: finite-probe evasion.** `probe_tool` enumerates fixed argv; `accepted` checks exit and returned SHA, `refused` exit and one ID. A stub can special-case those inputs yet accept an off-branch SHA [inf] (`tools/check-revision-binding.py:296-311,322-364`). Selftests reject simple mutants, not probe-aware ones (`tools/check-revision-binding.py:674-682`). D1-D6 are covered (`tools/check-revision-binding.py:322-358`).

- **High — FAILS: incomplete denominator.** `discover` scans nonrecursive `tools/`, ignores `_*.py`, and matches only exact double-quoted `"--revision"`; total is fixed names plus matches (`tools/check-revision-binding.py:186-197,367-408`). Nested, underscore, single-quoted or aliased gates evade it. Selftest covers only a top-level literal extra (`tools/check-revision-binding.py:651-661`). The narrow declaration is explicit (`tools/check-revision-binding.py:12-15`), not exhaustive.

- **High — FAILS: shared census is spoofable.** `shared()` counts import text and exact `{7,64}` only (`tools/check-revision-binding.py:218-220`). Its fixture injects dead `if False: import _revision` while using a local parameterized HEX validator; the selftest expects shared=1/local=0 (`tools/check-revision-binding.py:449-455,515-517,662-667`). This does not show callers use the shared binder; alternate regex syntax evades the copy count.

- **Low — FAILS: judge binder misses branch-first contract.** It checks revision first and never validates branch (`tools/check-revision-binding.py:136-149`), unlike `_revision.bind` (`tools/_revision.py:11-24,130-150`). Bad branch plus `HEAD` therefore misses E-BRANCH-INVALID; the judge selftest omits precedence (`tools/check-revision-binding.py:684-703`).

**Gaps:** No LSP device is mounted; no semantic queries. Grep was literal fallback only. No code or gate ran; findings are static.

Scope: executed=read-only git cat-file/log/diff-stat and source grep only (no code or gates).