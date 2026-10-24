# ExecC1Design — C1 fixed child environments

## Result

Produced a unified patch design against `6d76fb20f6ecbc940e5c8fff36c74060c885e161` and per-tool rationale/risk analysis. No production files were edited.

Artifacts:
- `c1-five-tools.diff` — fixed child dictionaries for all five tools; also sets the fixed environment on the scorer's two direct Git spawns that previously inherited the ambient environment.
- `rationale.md` — per-tool behavior, ambient-read risk table, and source/declaration discrepancy.
- `patch-dry-run.txt` — exact archive/dry-run commands and observed output.

## Retained evidence

- Frozen `SCORECARD.md` declaration at the base says each tool uses `PATH=/usr/bin:/bin`, `LC_ALL=C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, the already-fixed per-tool Git settings, and the private HOME/XDG/ceiling settings for receipt checking and `run-receipt.py` (Round 36 — declaration, C1).
- Frozen-source anchors: `check-revision-binding.py:103-107`; `check-report-receipts.py:309-328`; `score-census-handoff-r32.py:437-440, 488-490, 786-800, 841-845`; `mutants-btrfs-space-r30.py:362-364`; `run-receipt.py:36-43, 50-53, 80-103`.
- Environment/spawn search found no direct environment reads outside the builders. It also found scorer `git archive` and default-HEAD `git rev-parse` spawns without `env=`; the patch passes the same fixed dictionary to both. The generated binding stub's nested Git calls inherit the fixed environment of the stub process launched via `clean_env()`.
- Archive extraction was run from the frozen commit into `/tmp/tmp.b1rUY00bKY`; the final `patch -p1 --dry-run` emitted checks for all five files and no failure line. Full observed output is in `patch-dry-run.txt`; two hunks report fuzz (2 and 1), retained as a patch-context risk.
- **Source/declaration mismatch:** base `run-receipt.py:36-43` does not set `GIT_CEILING_DIRECTORIES`. The patch adds the declaration-required value computed from `home`'s parent; that addition is not baseline-preserving and can affect Git upward discovery. This is flagged in `rationale.md` for L1 integration.
- `TMPDIR`, `TEMP`, and `TMP` are indirectly used by parent `tempfile` scratch selection in all five tools (with conditions noted in the table); no environment-backed argument defaults were found. Child scratch-path behavior was not executed. LSP was unavailable in the provided tool inventory. No builds/tests/linters/formatters were run and no tools were installed.

## Risks and blockers

- The run-receipt ceiling is required by the frozen declaration but absent from the base implementation; strict behavior preservation and that requirement cannot both be asserted. The diff includes it and does not conceal the conflict.
- `patch --dry-run` passed without a failure line, but two hunks used fuzz; L1 should review the sparse-context hunks before applying.
- No C1 probe/battery was run by this seat; the after-state counter and sensitivity conjunction remain for the parent gate.

Report: `.ufo/waves/round-36/w1/ExecC1Design/`