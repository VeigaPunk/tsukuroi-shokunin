# AttackClaimInflation — R16 wave 1 (static)

Errata JSON, gate and R16 SCORECARD were absent when read, so these findings apply at integration. No checks were run. Tools installed: none.

1. **Wave-1 critics do not satisfy the falsify wave.** `build/dispatch.json` shows policy waveMin64 and a total of 64 seats, of which 10 are critics. The prompt (`tsukuroi-round-16.md:170-172`) requires a separate 32–64-seat wave 2 under policy v1. Falsifier: if no round-16 falsify `spec.json` and `record-result.json` exist, any statement that the wave debt is resolved is false. The verifier (`:135`) classes this as status-neutral, so it earns no claim and no calibration or discernment credit.
2. **Rows 3–4 of DraftLesson (wave debt, execution scope)** have no `captured-by` entry and no check that can fail. The prompt (`:71`) counts a fix "only once shown able to fail." Label both rows as open process debt.
3. **The gate is not a capability.** Precedent: `SCORECARD.md:312`. Falsifier: the capabilities row count `awk '/^## Capabilities/,/^## Saturation/' SCORECARD.md | grep -c '^| [a-z]'` is 3 at db68e62 and must still be 3.
4. **The count must be exactly 2.** Only `jq '.corrections|length'`=2 counts. Notices, S050, QUALITY23 and routed defects #3/#4 must not raise it. The R16 table must have one `| C1` row; the other axes and expansion stay unchanged.
