VERDICT: defect-found

## Evidence

- Pristine run: exit 0, emitted 22/22 control records; expected aggregate PASS.
- Pristine SHA256: `28c409bef9a87338831e0cab4c194a78e7fedfefbd9c4a300a33f30b24dd11d8`; after all probes: `28c409bef9a87338831e0cab4c194a78e7fedfefbd9c4a300a33f30b24dd11d8`. Frozen source was not mutated.
- Battery driver source: `.ufo/waves/round-46/controls/run_controls_c2.py:148-176`; binding implementation: `tools/check-scrub-admission-r46.py:141-189,192-203,206-258`.
- Exact observations are in `.ufo/waves/round-46/w1/C2MutBinding/{baseline-results.json,mutation-results.json}`.

## Kill matrix

| Mutant | Result | Killed controls (expected outcome changed) | Survivors (expected outcome retained) |
|---|---|---|---|
| drop_dispatch_count | killed | K0-donothing, K1-marks-only, K2-reports-no-dispatch, K3-forged-all, K4-partly-current, K5-stale-hash, K6-json-first-line, K7-preamble, K8-fails-old-hash, K9-outside-universe, K10-two-waves, K11-wrong-agent, K12-contradiction, K13-content-free, K14-no-citation, K15-any-wave-name, K16-quote-broken, K17-no-results, K18-amend-residual, K19-dup-key, K20-cr-first-line, K21-no-marks |  |
| drop_agent_role | survived | none | K0-donothing, K1-marks-only, K2-reports-no-dispatch, K3-forged-all, K4-partly-current, K5-stale-hash, K6-json-first-line, K7-preamble, K8-fails-old-hash, K9-outside-universe, K10-two-waves, K11-wrong-agent, K12-contradiction, K13-content-free, K14-no-citation, K15-any-wave-name, K16-quote-broken, K17-no-results, K18-amend-residual, K19-dup-key, K20-cr-first-line, K21-no-marks |
| drop_results_count | survived | none | K0-donothing, K1-marks-only, K2-reports-no-dispatch, K3-forged-all, K4-partly-current, K5-stale-hash, K6-json-first-line, K7-preamble, K8-fails-old-hash, K9-outside-universe, K10-two-waves, K11-wrong-agent, K12-contradiction, K13-content-free, K14-no-citation, K15-any-wave-name, K16-quote-broken, K17-no-results, K18-amend-residual, K19-dup-key, K20-cr-first-line, K21-no-marks |
| accept_cr | killed | K20-cr-first-line | K0-donothing, K1-marks-only, K2-reports-no-dispatch, K3-forged-all, K4-partly-current, K5-stale-hash, K6-json-first-line, K7-preamble, K8-fails-old-hash, K9-outside-universe, K10-two-waves, K11-wrong-agent, K12-contradiction, K13-content-free, K14-no-citation, K15-any-wave-name, K16-quote-broken, K17-no-results, K18-amend-residual, K19-dup-key, K21-no-marks |
| skip_contradictions | killed | K12-contradiction | K0-donothing, K1-marks-only, K2-reports-no-dispatch, K3-forged-all, K4-partly-current, K5-stale-hash, K6-json-first-line, K7-preamble, K8-fails-old-hash, K9-outside-universe, K10-two-waves, K11-wrong-agent, K13-content-free, K14-no-citation, K15-any-wave-name, K16-quote-broken, K17-no-results, K18-amend-residual, K19-dup-key, K20-cr-first-line, K21-no-marks |
| quorum_one | survived | none | K0-donothing, K1-marks-only, K2-reports-no-dispatch, K3-forged-all, K4-partly-current, K5-stale-hash, K6-json-first-line, K7-preamble, K8-fails-old-hash, K9-outside-universe, K10-two-waves, K11-wrong-agent, K12-contradiction, K13-content-free, K14-no-citation, K15-any-wave-name, K16-quote-broken, K17-no-results, K18-amend-residual, K19-dup-key, K20-cr-first-line, K21-no-marks |
| ignore_old_fails | inconclusive | none | unapplied: anchor absent |
| drop_body_length | survived | none | K0-donothing, K1-marks-only, K2-reports-no-dispatch, K3-forged-all, K4-partly-current, K5-stale-hash, K6-json-first-line, K7-preamble, K8-fails-old-hash, K9-outside-universe, K10-two-waves, K11-wrong-agent, K12-contradiction, K13-content-free, K14-no-citation, K15-any-wave-name, K16-quote-broken, K17-no-results, K18-amend-residual, K19-dup-key, K20-cr-first-line, K21-no-marks |
| drop_citation | killed | K14-no-citation | K0-donothing, K1-marks-only, K2-reports-no-dispatch, K3-forged-all, K4-partly-current, K5-stale-hash, K6-json-first-line, K7-preamble, K8-fails-old-hash, K9-outside-universe, K10-two-waves, K11-wrong-agent, K12-contradiction, K13-content-free, K15-any-wave-name, K16-quote-broken, K17-no-results, K18-amend-residual, K19-dup-key, K20-cr-first-line, K21-no-marks |
| drop_r45_sha | survived | none | K0-donothing, K1-marks-only, K2-reports-no-dispatch, K3-forged-all, K4-partly-current, K5-stale-hash, K6-json-first-line, K7-preamble, K8-fails-old-hash, K9-outside-universe, K10-two-waves, K11-wrong-agent, K12-contradiction, K13-content-free, K14-no-citation, K15-any-wave-name, K16-quote-broken, K17-no-results, K18-amend-residual, K19-dup-key, K20-cr-first-line, K21-no-marks |
| drop_mark_check | survived | none | K0-donothing, K1-marks-only, K2-reports-no-dispatch, K3-forged-all, K4-partly-current, K5-stale-hash, K6-json-first-line, K7-preamble, K8-fails-old-hash, K9-outside-universe, K10-two-waves, K11-wrong-agent, K12-contradiction, K13-content-free, K14-no-citation, K15-any-wave-name, K16-quote-broken, K17-no-results, K18-amend-residual, K19-dup-key, K20-cr-first-line, K21-no-marks |

## Survivors and proposed controls

- **drop_agent_role** survives all 22 controls. Proposed control: alter one dispatched counted seat to role executor while preserving report and result role; expect rejection.
- **drop_results_count** survives all 22 controls. Proposed control: remove a counted seat result record while retaining dispatch/report; expect rejection.
- **quorum_one** survives all 22 controls. Proposed control: make only one counted seat per row valid while the remaining counted seats are missing/invalid; require failure.
- **drop_body_length** survives all 22 controls. Proposed control: valid verdict, hash and citation with under-300-byte body; require rejection.
- **drop_r45_sha** survives all 22 controls. Proposed control: substitute a modified R45 counter preserving acceptable reported leg metrics; require pinned-digest rejection.
- **drop_mark_check** survives all 22 controls. Proposed control: remove exactly one admission marker with all reports valid; require failure.

Mutants were separate scratch copies; scratch removed after receipts were copied.
