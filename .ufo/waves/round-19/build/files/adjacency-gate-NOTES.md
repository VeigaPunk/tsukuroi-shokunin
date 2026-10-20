# Round-19 adjacency gate draft

## CLI
- `python3 tools/check-adjacency-anchors.py --revision <hex> [--branch master] [--registry corpus/knowledge/adjacency-anchors-r19.json] [--registry-from <hex>] [--siblings-root /home/vgpnk/Projects/shokunin]` checks a landed revision; `--selftest` runs the hermetic fixture suite.
- Exit codes are 0 clean, 1 findings, and 2 could-not-evaluate. A normal run emits one sorted-key JSON object with status, revision, branch, branch tip, counts, and `{id,site,detail}` findings.
- Lane content is read from regular committed Git blobs. `--registry-from` selects the registry, census, and sibling snapshots; PROVINCE.md, the knowledge entry, and inbound target files remain from `--revision`.

## Counts and behavior
- Counts include `outbound_total`, `outbound_portable`, `inbound_total`, `inbound_classified`, `inbound_by_class`, `inbound_by_scope`, `live_object_checked`, and `live_object_match`. Per-class/scope totals include only unique inbound entries whose census identity, classification, evidence limits, and publication checks pass.
- Outbound checks validate captured-census coverage, snapshot SHA-256, exact heading/section and quote line, 25-word maximums, pointer presence, and a published id+quote line after the portable-anchor heading. `outbound_portable` counts records passing all checks.
- Inbound checks require one record per census id; compare sibling/pointer/target fields and derived scope; recompute RESOLVES, DRIFTED, or UNRESOLVABLE from the target file at `--revision`; and require the id in the knowledge entry.
- With `--siblings-root`, successful local sibling-object reads contribute informational `live_object_checked`/`live_object_match` counts. Missing/unreadable sibling repos never alter the exit code.

## Findings
- Outbound: `OUTBOUND-FIELDS`, `OUTBOUND-ID`, `OUTBOUND-DUPLICATE`, `OUTBOUND-PROPOSITION-TOO-LONG`, `OUTBOUND-CENSUS-UNKNOWN`, `OUTBOUND-POINTER-MISMATCH`, `OUTBOUND-CENSUS-INCOMPLETE`, `ANCHOR-SNAPSHOT-TAMPERED`, `ANCHOR-HEADING-MISSING`, `ANCHOR-QUOTE-MISSING`, `ANCHOR-QUOTE-TOO-LONG`, `ANCHOR-POINTER-MISSING`, `ANCHOR-UNPUBLISHED`.
- Inbound: `INBOUND-FIELDS`, `INBOUND-DUPLICATE`, `CENSUS-INCOMPLETE`, `INBOUND-CENSUS-UNKNOWN`, `INBOUND-POINTER-MISMATCH`, `INBOUND-QUOTE-TOO-LONG`, `INBOUND-RELIED-ON-TOO-LONG`, `INBOUND-CLASSIFICATION-WRONG`, `INBOUND-UNPUBLISHED`.
- Unreadable, malformed, unsafe, or unbound inputs return a single `E-*` finding with exit 2; snapshot byte mismatch/missing snapshot is `ANCHOR-SNAPSHOT-TAMPERED` with exit 1.

## Selftest
- Executed `python3 tools/check-adjacency-anchors.py --selftest`; observed `PASS (12 cases, 12 passed, 0 failed)`.
- The 12 isolated Git-fixture cases cover clean pass, snapshot tamper, missing heading, quote outside section, overlong quote, unpublished anchor, census gap, wrong RESOLVES, wrong DRIFTED, unpublished inbound, baseline `--registry-from` without entries, and bad revision.
- `python3 tools/check-adjacency-anchors.py --help` displayed all requested CLI options. The real round-19 registry revision was not exercised in this seat.
