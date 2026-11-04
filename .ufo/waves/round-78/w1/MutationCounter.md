# MutationCounter — Round 78

Axes: depth, operability. Frozen C1 actual `--root` CLI exercised on explicitly synthetic fixtures only.

- Final runner rc0: 20 cases × two identical passes × pristine/mutated/restored = 120 CLI invocations.
- Fourteen rejection mutants killed. All pristine/restored controls rc0/count6; exact before/restored hashes matched for every fixture.
- Stable rejection reasons: finite-content-mismatch, snapshot-tampered, unreadable:FileNotFoundError, review-not-bound, result-identity, result-digest, unreadable:ValueError.
- JSON-wrapped string final accepted by design; typed object/null rejected. Whitespace-only data changes invalidate stale review binding.
- Fully fabricated self-consistent bundle passes: known non-authentication limit, not actual seat evidence or a contract change.
- Counter SHA256 `cffc3e9d9c04cecd3f98810117cd92fe429261483308b58e3f539ca51de449f1` matched frozen claim commit. No production modifications or registry selftest. Scratch removal observed: `scratch_removed=true`.

Full findings: `.ufo/waves/round-78/w1/MutationCounter/report.md`.
Reproducible runner: `.ufo/waves/round-78/w1/MutationCounter/runner.py`.
Actual outputs, RCs, stable reasons, pristine/mutated/restored SHA256 maps: `.ufo/waves/round-78/w1/MutationCounter/matrix.json`.

Limit: finite synthetic counter probe; no upstream semantic verdict, authentication proof, C2 result, or outside admission claimed.
