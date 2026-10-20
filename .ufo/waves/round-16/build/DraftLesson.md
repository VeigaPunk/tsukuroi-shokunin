# Round 16 lesson draft — Gate and Mistakes

Static reads only; no checks, installs, or commits.

## Gate

Candidate: `corpus/knowledge/section-citation-errata-r16.json` with additive corrections `R16-BOARD-SECTION` and `R16-RANK-SECTION`. Pending: errata JSON and `tools/check-section-citations.py` absent; nothing evaluated.

## Mistakes

| class | evidence | fix |
|---|---|---|
| wrong section locator: board | host-health-report-r3.md:581 says §1; heading §0 at line 23, row 5 at 31 | named correction; keep history |
| wrong section locator: rank | update-safety-v3.md:398 says §7; heading §5 at line 208, row 1 at 216 | named correction; keep history |
| wave debt: no falsification wave | round-15.md:36; round-15-verifier-spotcheck.md:16,135 | run attack wave when build claims exist |
| execution scope: extra reads, authoring py_compile | round-15.md:82–90 | single-probe, no-compile author instructions |

## Boundary

Pending, not pass: gate red/green and corrections unobserved; wave2 not run; host recovery operator-owned.
