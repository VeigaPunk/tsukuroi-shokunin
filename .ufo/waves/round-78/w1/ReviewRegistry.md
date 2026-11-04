# ReviewRegistry — Round 78

Axes: depth and operability. Independent static review of base `b9019a1d0558241bf67cf31ff90256284d8657af`, frozen claim `07a607df1a5157daafc91bb5c26858af14415f43`, and final ExecRegistry rows.json, fixes.json and interface-fixes.json. Recommendation only, not outside admission.

## Findings by severity

No actionable findings remain in the final executor drafts inspected. All eight additions, both complete repaired rows, and the new r78 row hold against scoped static source inspection. Exact per-tool holds/reasons, source-line evidence, pin paths and resolved corrections are in ReviewRegistry/verdict.json. L1 must integrate the complete corrected cells, not only fixes.json code-2 `after` strings.

Resolved medium finding: initial full JT/r74 repaired rows omitted explicit --repo and said writes nothing despite temporary selftest fixtures. Final fixes.json entries include --repo and scopes disclose fixture writes. Evidence: tools/count-jt-rows-r75.py:240-242,367-378; tools/check-r74-routed-r75.py:175-178,218-225,246-258. Working-file reads without revision are now disclosed too.

Resolved low finding: initial r78 scope said committed reads only, but tools/measure-journal-usage-r78.py:126 always loads expected.json from installed instrument checkout. Final interface-fixes.json distinguishes that specification from committed target/source/review inputs and isolated --root reads. Startup specification load failures remain outside score error handling; the repaired row does not promise their conversion into a named predicate rejection.

## Ten inherited findings and exact contracts

Frozen before/controls.json C2-do-nothing records 116 tools, 108 registered rows, eight missing rows, two incomplete maps, rc 1. Eight omissions: check-r71-routed-r72, check-r72-routed-r73, check-r73-routed-r74, check-r75-routed-r76, count-jd-rows-r76, count-md-rows-r72, count-uf-rows-r74, count-ul-rows-r73 (tools/*.py). Both incomplete maps: count-jt-rows-r75 and check-r74-routed-r75. Their added code 2 is argparse usage, not missing data.

- MD and r71-r72 have no selftest flag. r71-r72 fixture mode still reruns the historical counter at pinned 2b358d2d (:50-55,72); not fixture-only isolation.
- r72-r73: rc 2 for missing/non-directory TMPDIR or argparse; rc 3 selftest failure. Exact flag --selftest.
- r73-r74: rc 2 conflates argparse refusal and failed selftest; final map explicitly preserves the distinction. Selftest uses in-memory texts.
- UL: rc 2 TMPDIR guards/argparse, rc 3 selftest failure, rc 128 missing note/registry/map. Corpus-derived samples and committed snapshots are accurately disclosed.
- UF: actual selftest has no TMPDIR refusal despite stale header; final map correctly assigns 2 only to argparse, 3 selftest failure, 128 missing data. Its unconditional PASS summary text (:355-356) can coexist with failure rc 3; registry coverage does not establish whole-tool conformance.
- JT/JD: rc 3 selftest failure and rc 128 absent note/registry/map; synthetic snapshots in private temporary fixtures.
- r74-r75/r75-r76: missing content is stale rc 1, not 2; failed selftest rc 3.

Exact note/registry/map pin paths are in verdict.json: snapshot maps are .ufo/waves/round-{72,73,74,75,76}/before/src/SOURCES.json; source registry is corpus/SOURCES.md. Corrected rows preserve digest, source/quote, finite target, snapshot reuse and host-limit distinctions. New r78 entry, --selftest, 0/1/argparse-2 map and limited digest-binding claim match source :15-19,40-77,119-138.

## Coverage and limitations

Actual frozen base-to-claim SKILL/tools diff adds only r78 tool/row; the ten C2 findings are inherited. Executor coverage.json reports frozen-reader candidate 117 tools/117 rows/zero findings; frozen starts 117/109/10 because r78 added one tool/row. That receipt was not independently executed here.

check-registry-coverage.py:262-326 checks path coverage, kinds, numeric code presence and literal selftest-flag presence. It does not establish parser acceptance, semantic status mapping, pins, write scope, whole-tool conformance, Linux capability, host clearance or semantic truth. Zero findings means registry coverage clean only. No runtime routing, resume-continuity or saturation paths change in this scoped diff.

LSP unavailable (xd://lsp returned No such tool); references/definition/diagnostics unavailable. Source/text fallback is not semantic-server proof. No gates, selftests, build/lint, host probes or installations executed here. No production edits, git mutations, clones, privileged operations or sibling writes. Empty private scratch removed. Operator rules and relevant skills read. Remaining verification: L1 integrates full drafts and runs the canonical frozen coverage counter against the landed revision.

Report: .ufo/waves/round-78/w1/ReviewRegistry.md
