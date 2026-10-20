# FxLesson — SURVIVES, with one low metadata finding

## Findings (Low)
- `corpus/SOURCES.md:70` lists S064 `used-by` only as `corpus/lessons/round-18.md`, but `corpus/lessons/round-17.md:71` explicitly cites “Active precision row S064” in its loader-quote/header correction. The source consumer index omits that direct R17 lesson use; add the consumer or clarify the field’s scope.

## Assessment
- **SURVIVES — Gate and source quotes:** `round-18.md:9-24` decisions align with the evidence. S060 capture `:25` records 1395; `:75-77` only names `home`/`root`; no pending-update query is present. S061–S063 quotations match the opened primary URLs. S064 capture `supplement-capture.txt:2,113-115` confirms the exact loader value and header without timezone.
- **SURVIVES — QUALITY 28/30 at source level:** `measure/c2-before-842a531.json:1` records `status=FAIL`, `bound_tools=9`, `consistent_tools=1`, `shared_tools=0`, `local_rev_regex_copies=9`. `check-boot-chain.py:1432-1467` contains wrong-count, omitted-LTS-cite, wrong-mtime and baseline-without-notice fixtures. Registry data reads show 88 freshness records / 17 paths (49 primary + 39 supplementary).
- **UNPROVEN — QUALITY 29 / final R18 closure:** prior R17 report-tail failure is directly documented at `round-17-verifier-spotcheck.md:33,89-95`; the final R18 ledger/report is pending. No final R18 pass is inferred.

## Residual risk / verification gaps
No gates or tests executed by this read-only seat; the C1 fixtures were inspected, not run. LSP is unavailable (`read xd://lsp` returned “No such tool”); literal search was only a locator, not semantic proof.

Scope: executed=none