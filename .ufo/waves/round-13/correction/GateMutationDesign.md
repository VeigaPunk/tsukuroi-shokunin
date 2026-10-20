# Round 13 — correction-checker mutant design

**Scope:** design only, as assigned. No checker was run, no mutant was applied, and no source or sibling file was edited. This is not a killed/survived result.

## Axes

- **Semantic correctness:** retain the valid `ProtectSystem=full` versus `strict` distinction while rejecting the false unit-wide `only` claim.
- **Alternative coverage:** keep the documented unit path-view alternatives in the canonical B2 signal.
- **Evidence scope / preservation:** do not turn an unmeasured unit namespace into an absence claim; keep round-12 bytes as historical evidence and check the active superseding pair.

## Observed anchors

- Outside spotcheck identifies the defect in the MD current-host explanation, R13, and JSON B2 `limit`; the false universal is “only” `ProtectSystem=strict` or `ReadOnlyPaths=`. It lists `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=` and `RootImage=` as alternatives and records the source reopen for read-only bind paths and `TemporaryFileSystem=:ro` (`corpus/lessons/round-12-verifier-spotcheck.md:143-154,237-241`).
- In the inspected round-12 files, MD line 53 and R13 line 86 contain the exclusive claim; JSON B2 `expected_signal` line 84 already lists the alternatives, while `evidence_kind` line 86 says the unit-private namespace is unobserved and `limit` line 87 repeats the exclusivity. MD line 53 also says the added properties were not in that capture (`corpus/knowledge/root-dac-decision-r12.md:53,86`; `corpus/knowledge/root-dac-decision-r12.json:77-87`).
- S028 is the existing `systemd.exec(5)` source row (`corpus/SOURCES.md:34`); the corrected wording must cite the precise source anchors for each asserted mechanism, not treat a property-name list as authority. Do not alter registry/history from this seat.

## Narrow red/green oracle for L1

Run one semantic check against the preserved round-12 delivered MD/JSON bytes and the active superseding MD/JSON pair. It should return **FAIL** for the delivered round-12 pair due to the exhaustive unit-path claim, and **PASS** for the corrected active pair only when both files retain the source-scoped `ProtectSystem` comparison, all B2 alternate path-view mechanisms, and the recorded “not captured / namespace unobserved” limit. Point it at active files explicitly: a historical R12 sentence retained with a supersession notice is not an active contradiction. The full delivered revision recorded by the spotcheck is `f3868cdef07027f7ec8ecd095457d95108f75676` (spotcheck lines 5-10).

The check should inspect parsed B2 fields plus the active MD R13/current-host claims, not rely on a whole-repository word search for `only`: the valid proposition is specifically “among `ProtectSystem` values, `full` does not cover `/`, while `strict` does (subject to exceptions).” Expected red/green labels (proposed, not observed): `FAIL B2_UNIT_MECHANISM_EXCLUSIVITY` on old bytes; `PASS` on corrected active content.

## Sole-delta mutants (apply individually to a disposable checker fixture)

| Mutant | One semantic delta | Expected detector result |
|---|---|---|
| **M1 — remove alternative** | In corrected JSON B2 `discriminator.expected_signal`, delete only the `BindReadOnlyPaths=` route; leave MD, other alternatives, and all other bytes unchanged. | `FAIL B2_SIGNAL_MISSING_BIND_READONLYPATHS`. The canonical discriminator must not silently lose a documented route merely because MD still mentions it. |
| **M2 — restore “only”** | In active MD R13 only, replace the corrected non-exclusive unit-path statement with the old proposition that only `ProtectSystem=strict` or `ReadOnlyPaths=` covering `/` can make `/` read-only through the unit. Leave JSON untouched. | `FAIL B2_UNIT_MECHANISM_EXCLUSIVITY` (and, if the checker compares representations, an MD/JSON semantic mismatch). This exercises MD independently of canonical JSON. |
| **M3 — overclaim namespace absence** | In corrected JSON B2 `evidence_kind`, change only `unit-private namespace unobserved` to `unit-private namespace ruled out` (or its exact semantic equivalent). Do not add any measurement. | `FAIL B2_UNOBSERVED_UNIT_VIEW_ASSERTED_ABSENT`. The captured properties did not include `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=` or `RootImage=`; a host `findmnt` result and `ProtectSystem=no`/empty `ReadOnlyPaths=` cannot establish their absence. |

Each mutant changes one semantic assertion in one active representation; do not combine mutants. Expected per-mutant output above is an oracle proposal, not a detector transcript. A checker that passes any mutant has a coverage gap in that named axis.

## Execution / restoration record

- Actual detector output: **not run** (explicit task bound this seat to design only).
- Mutant verdicts: **not executed / no killed-or-survived verdict**; no mutant was applied.
- Before/after hashes and restoration: **not applicable**; this seat made no source-byte change, so there are no mutant bytes to restore. Main should obtain hashes and actual outputs only if a later task authorizes execution.
- Tool installs/updates: **none**; none was needed.
