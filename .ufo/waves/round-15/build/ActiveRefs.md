# ActiveRefs — round 15 routing, r14 notices, gate/probe registration

Baseline 0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2. Leaf; no dispatch, package, service, sudo, credential or test action. Tools installed/updated: none.

## Files changed

1. `corpus/knowledge/source-scope-correction-r14.md:207` — appended `## R15 supersession (2026-10-20) — locator and positive-domain notices`. R15-LOCATOR supersedes only the bare `rendered lines 1266-1267` locator (R14 source-object sentence, JSON `corrections[0].location`, `sources[0].anchor`); active locator is SANDBOXING > ProtectSystem= plus the observed systemd 262.1 footer. R15-POSITIVE-DOMAIN supersedes only `documents no further values for this option`; the 11-word quote and mechanism-scope sentences stand.
2. `corpus/knowledge/source-scope-correction-r14.json:203` — additive `r15_supersession` key only. Object minus the key equals `git show HEAD:` (True). Canonical digests reproduce the gate pins: r14 MD prefix (rstripped) `9f7cc3cf…8dc04` = `MD14_SHA`; normalized JSON minus key `1a4cccac…effb5` = `JSON14_SHA`. Only diff artefact is the final `]` gaining a comma.
3. `SKILL.md:1787` — Round-15 routes plus registry rows: locator gate (`tools/check-locator-clarification.py`; 0/1/2; `--selftest` 21+2=23; pins = tool constants, headings/fields/quote, r14 canonical digests; no writes; owner tsukuroi) and update probe (`tools/measure-update-recheck.py`; 0 = ABSENT or COUNTED, neither clean; 2 = cannot-evaluate; no 1; no selftest; C2 schema/keys/source_ids S047-S049/raw-byte digest binding). Boundaries: no installs/services/privileged probes; operator-only pending assessment; no clearance; mkinitcpio-42 hook risk untested; no host repair.
4. `corpus/README.md:96` — matching Round-15 route; gate vs counting probe, probe exit 0 ≠ clean.
5-8. `update-safety-note.md:498`, `update-safety-v2.md:368`, `update-safety-v3.md:395`, `host-health-report-r3.md:578` — short R15-UPDATE-STATE appendices routing current use to `partial-upgrade-recheck-r15.md`/`.json`, quoting the superseded `INERT`/“Do nothing now” statements. Append-only: 22-23 insertions, 0 deletions each.

## Evidence checked statically (nothing executed)

- C1 pair landed: MD headings exactly `## R15-LOCATOR`, `## R15-POSITIVE-DOMAIN`, `## QUALITY check`, provenance trio first; JSON schema `tsukuroi-locator-clarification-v1`, exactly 2 corrections, 7 fields each, both quotes the exact 11-word sentence, locations line-number free. A reviewer-found LOC quote mismatch (20-word variant) was corrected by the author; routing names only IDs/paths/schema.
- r14 notice tokens required by `md14_notice_ok`/`json14_notice_ok` all present: both IDs, the two superseded literals, corrections[0].location/replacement, sources[0].anchor, schema, pair filename; locator `active_locator` has SANDBOXING+ProtectSystem= and no line-number hit.
- C2 record: source_ids S047/S048/S049; observed_at = snapshot_captured_at = 2026-10-20T07:44:39Z; snapshot_sha256 b101f374…ea81; pending 413; decision BLOCKED_FOR_AGENT_PACKAGE_ACTION; libinput_log 07:25:17Z (upgrade line). The four notices name the 04:25:16-0300 command and the 04:25:17-0300 upgrade line, so both agree.
- Probe interface confirmed from source and independently by ReviewGateRegistry: `--revision` only; 0 for COUNTED/ABSENT, 2 for CANNOT; internal `status: COUNTED` is not a gate clean; digest lives in the C2 JSON and is checked against raw snapshot bytes; stdlib reads only.
- Expected, not failures: W04 duplicate-URL warnings for S046 (systemd.exec) and S048/S049 (pacman.8); census exits 0.

## Limits

- No gate, selftest, probe, test, build, lint or formatter was executed; no verdict, source-truth, parser or host-health claim is made here.
- C1 pair/gate and C2 record/probe were authored by sibling seats; I verified their landed interface by static read only.
- Historical gate/census counts were not rewritten; the four notes keep their 2026-10-14 bytes. The mkinitcpio-42 `/new_root` reading is an untested future risk, not an observed failure.

## Recommendations for L1

1. Run `check-locator-clarification.py --revision 0db618a…` (expect LOCATOR_UNQUALIFIED/NEGATIVE_DOMAIN_UNSWEPT red) and on the final revision (expect 0, correction_count 2), plus `--selftest`.
2. Run `measure-update-recheck.py --revision <baseline>` (expect ABSENT, record_count 0) and final (expect COUNTED, record_count 1, pending 413, installed_libinput 1.32.0-1); report exit 0 as observation, not clean.
3. Keep depth 8/freshness 9; describe both as documentation/dated-record repairs, not ordinal lifts or host repair.
