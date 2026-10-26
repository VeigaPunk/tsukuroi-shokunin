# ConnClaims receipts — K5X / K5Y / K5Z variants (scratch clones, read-only lane)

All three variants are clones of the lane at BASE `c8efaa3f120834541f8de1e5e0367e8d1593bae6`
(`git clone --shared`, origin removed, toplevel verified, fixture identity `fixture@invalid`),
modified only in `tools/tsukuroi-census.sh`, committed, and scored with the frozen counter bytes at
freeze `a84fc9dec860f8bea516dff7ddfdc98223cdae52` (`tools/score-size-invariance-r42.py`, identical at
tip 87c4f7c6; `git diff a84fc9de 87c4f7c6 -- tools/score-size-invariance-r42.py` empty).
Variant commits (scratch-local, deleted with scratch): K5X `9f4059bb…`, K5Y `1fb4b201…`, K5Z `43de04c8…`.

- K5X (result: k5x-result.jsonl): `run_controls_c1.variant('K5', base)` filter extended to also drop
  `^error:` lines. Result: FAIL — invariant 10, ns_invariant 0 (per-run token stripped with the error
  line), selftest_pass 0, default_equal 1.
- K5Y (result: k5y-result.jsonl): filter keeps the first `^error:` line (token survives), drops
  remaining error lines, warnings, zero-altered summaries. Result: FAIL — invariant 10, ns_invariant 3,
  selftest_pass 0 (selftest case D05 fails: nonroot_artifacts=0, expected 1), default_equal 1.
- K5Z (result: k5z-result.jsonl): filter keeps the first `^error:` line and keeps warning lines that
  carry the parser-relevant literals `(Permission denied)` / `(failed to calculate SHA256 checksum)`
  (census :705-706), drops all other warnings and zero-altered summaries. Result: **PASS, exit 0** —
  cases 10, invariant 10, ns_invariant 3, selftest_pass 1 (128/128), default_equal 1.
  The base early readers `printf '%s\n' "$s_out" | grep -q '^error:'` and `| grep -m1` (the
  R41-CENSUS-PIPEFAIL-692 constructs) are retained verbatim; the filter runs before them, so the early
  reader never sees a >64 KiB stream.
