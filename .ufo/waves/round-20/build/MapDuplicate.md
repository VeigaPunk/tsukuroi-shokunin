# C3 duplicate-highest-heading review

**Axes:** C1 adjacency, C2 operability, C3 calibration. This review is limited to C3.

## Required mutation/control

Start with an otherwise coverage-clean fixture containing one complete, unique highest registry table and a `boot-chain-audit` probe row whose live map says `0 CONSISTENT` and `2 UNKNOWN`, with selftest failure `1` kept distinct. Duplicate the exact highest heading (`## Gate and probe registry — round20 superseding current rows`) and include a complete table under the duplicate; change no other fixture bytes. This makes the highest registry heading ambiguous rather than repairing or altering a historical row.

Expected selector result, preserving the baseline checker contract: **exit 2**, `status: CANNOT_EVALUATE`, one finding `E-REGISTRY-TABLE` at `SKILL.md`, detail `round20 heading is duplicated`. The existing `_operative_rows` selects the maximum exact heading number and raises `TableError` when that number occurs more than once (`tools/check-registry-coverage.py:133-145`); `main` maps `TableError` to `CANNOT`/2 and `E-REGISTRY-TABLE` (`:331-337`), and `_emit` labels code 2 `CANNOT_EVALUATE` (`:272-278`). Since selection fails, do not report a semantic C3 pass, `REGISTRY-AUDIT-LIVE-MAP`, or `audit_live_map_errors=0`; do not fall back to round19 or any older row. If testing the baseline heading number instead, the corresponding exact detail is `round19 heading is duplicated`.

## Why historical-row and digit-presence checks are insufficient

The recorded operative rule requires the unique highest exact heading and says a duplicate highest table is could-not-evaluate, never fallback (`SKILL.md:1997-2000`; round19 restates it at `:2060-2063`). A corrected lower row cannot resolve which duplicate highest table is authoritative. Likewise, baseline generic probe coverage merely checks that digits `0` and `2` occur in the verdict cell (`tools/check-registry-coverage.py:229-236`); that does not establish that they are live mappings, exclude an additional live `1 DEGRADED`, or distinguish live outcomes from a separate selftest map.

The source pin is S079, `tools/boot-chain-audit.sh` at baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472` (`corpus/SOURCES.md:86`). It documents that live exit 1 is never emitted (`tools/boot-chain-audit.sh:81-85`) and the live summary returns only `UNKNOWN`/2 or `CONSISTENT`/0 (`:794-800`). The round19 registry row nevertheless advertises live `1 DEGRADED` (`SKILL.md:2060-2073`); the preregistered C3 semantic expectations require `REGISTRY-AUDIT-LIVE-MAP`/exit 1 for that operative map, `audit_live_map_errors=0`/exit 0 for the corrected map, and rejection of a historical-row-only fix (`.ufo/waves/round-20/preregister.json:21-27,49-53`). These semantic expectations apply only after a unique highest table is selected; the duplicate control must remain CANNOT_EVALUATE.

## Residual risk and verification gaps

This is a source-based mutation design, not a candidate-diff review or observed fixture result. The exact duplicate-heading ID/exit is derived from the baseline selector's error path; this review did not run the new `--audit-live-map` mode or inspect candidate output. No host, boot-readiness, or safety claim is made.

Scope: executed=none
