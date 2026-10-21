# Round 20 independent source oracle

Axes: **C1 adjacency**, **C2 operability**, **C3 calibration**. This is a source-only oracle, not a review of candidate code or measurement output.

## Scope and source support before measurement

No candidate worktree or candidate output was read, and no evaluator, fixture, host, or boot audit was run. Source paths below are read from the production lane; I did not run Git to independently authenticate that each working-tree file is the stated baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472`. No LSP status/reference/definition/diagnostics query was made: the seat's permitted interface was read/grep/glob plus this report write, so there is no semantic caller/diagnostic evidence.

**Scope disclosure:** my first read of `preregister.json` returned the full JSON, exposing the C2/C3 expected entries. Those entries influenced the C2/C3 case naming/selection below; treat those sections as source cross-checks, not independent oracle derivations. I subsequently read only `.expected.C1` for the permitted C1 expectation. No candidate output was used. The full-file read is a scope deviation, so this artifact cannot claim C2/C3 oracle independence.

Pre-measurement conclusion: **C1 is semantically source-supported but its exact checker outcomes are not all derivable from baseline code; C2's object/commit rules are source- and documentation-supported but the new object-only cases/metric are not implemented in baseline source; C3's live-vs-selftest distinction is directly source-supported but the audit-live-map finding/count evaluator is absent from baseline source.** No actual measurements are claimed.

## C1 — OUT-009 ownership correction

**Fixed source identity.** `corpus/knowledge/adjacency-anchors-r19.json`, record `OUT-009`, binds the sibling declaration to commit `cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97`, blob SHA-256 `63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f`, snapshot `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md`, heading `# revenger province`, quote line 3. The pinned text at lines 3–7 names shipped-artifact RE and its evidence-ledger scope; lines 19–29 bound its refusal and write scope. These facts support attributing the quoted domain to Revenger, not expanding it into Tsukuroi authority. The hash is the recorded pin; it was not independently recomputed in this no-exec review.

`PROVINCE.md:51` says the kaidoku/revenger ownership is unresolved and requires an integrator ruling before RE work; `PROVINCE.md:79–80` says both declare shipped-artifact RE and Tsukuroi does not select an owner. `ownership-correction.txt:1` supplies the fixed correction wording: the OUT-009 text is Revenger's sibling declaration, not a Tsukuroi ownership grant; arbitration stays unresolved; ask the integrator before an internals handoff; no configuration/service/package/boot/sibling-file write is authorized.

| Fixed class | Expected result | Source support / limit |
|---|---|---|
| `missing`: omit the OUT-009 correction while retaining the pinned OUT-009 source identity | `OWNERSHIP-CORRECTION-MISSING`; expected gate failure exit **1** is inferred from the baseline adjacency gate's `PASS=0, FAIL=1, CANNOT=2` (`tools/check-adjacency-anchors.py:20,603–610`). | The ID is preregistered in `.expected.C1`; baseline source supports the source obligation, but does not define this new ID. No negative-branch count is specified by `.expected.C1`. |
| `altered`: use the fixed correction with the single falsifying mutation `It is not a tsukuroi grant of ownership` → `It is a tsukuroi grant of ownership` | `OWNERSHIP-CORRECTION-INVALID`; expected exit **1** by the same gate-map inference. | The falsification contradicts `PROVINCE.md:51,79–80` and the pinned scope. The exact invalid ID is preregistered; baseline evaluator has no such mode. No negative-branch count is specified. |
| `positive`: exact bytes of `ownership-correction.txt:1`, bound to the OUT-009 snapshot/commit/blob pin above | `ownership_corrections=1`; exit **0** (the preregistered positive). | One named correction and one OUT-009 identity support a count of one. This is source-backed as a finite intended count, not as measured output. |

**Causal criterion:** move from absent/false attribution to exactly one correction that accurately records the sibling's own pinned declaration while preserving unresolved arbitration and all no-write/no-remediation boundaries. It must not choose kaidoku or revenger, transfer handoff authority, or claim sibling/host safety. `tools/check-adjacency-anchors.py:207–217,613–629` shows the baseline's existing counters and CLI are only the R19 10/114 anchor census (`--revision`, `--selftest`); there is no baseline `--ownership-corrections` metric or evaluator. Thus the semantic requirement is supported; the new error IDs and mode behavior are not baseline-evaluator evidence.

## C2 — object-only revision selectors

**Baseline behavior and official semantics.** `tools/_revision.py:40` accepts 7–64 hexadecimal characters, and `:97–115` passes the raw selector to `git rev-parse --verify --quiet --end-of-options "${ref}^{commit}"`. `:134–154` then checks the resulting commit against the local branch and, if present, `origin/<branch>`. Its selftest at `:194–233` already pins uppercase-hex acceptance, invalid non-hex/ref forms, non-commit blob rejection, unlanded and unpushed classes. `tools/check-revision-binding.py:61–80` defines the five legacy tools plus four R17 tools: **nine original consumers**. `:361–369` defines accepted binding as a non-CANNOT result whose JSON `revision` equals the expected commit; `:424–429` requires refusals to be a single typed finding. The current probe cases at `:380–435` do not contain the new object-only controls, and its CLI at `:515–525` has no `--object-selectors` flag.

The official [Git `rev-parse` documentation](https://git-scm.com/docs/git-rev-parse) says `--verify` converts one parameter to an object name; `^{commit}` checks for a commit-ish and peels an annotated tag to its commit; `--end-of-options` prevents an untrusted name being parsed as an option. Under “SPECIFYING REVISIONS,” Git permits both a full/unique hexadecimal object name and ref names such as `master`/`refs/heads/master`; `--disambiguate=<prefix>` lists every matching object for a prefix of at least four hex digits. Therefore `rev-parse`'s revision syntax alone is broader than “this hexadecimal input names an object.” The selector controls below test that distinction; no precedence rule is inferred beyond what the docs state.

| Fixed fixture class | Expected selector outcome | Expected binding assertion |
|---|---|---|
| `ghost_hex_branch`, `ghost_hex_tag`: selector is a full-width all-hex string used as a branch/tag name, with no object having that exact ID | exit **2**, `E-REVISION-INVALID`, one refusal finding; no bound SHA | Reject the ref-name resolution; hexadecimal spelling alone is insufficient. |
| `valid_prefix_shadow_branch`, `valid_prefix_shadow_tag`: unique object prefix `P` identifies commit `C`; branch/tag named `P` points to a different commit `D` | Accepted (not a binding refusal); JSON bound SHA is exactly full object ID `C`, never `D` | Test requires fixture uniqueness and separately recorded `C`/`D` object IDs. |
| `uppercase_object`: uppercase spelling of a valid object ID | Accepted; same full commit SHA as lowercase input | Existing `_revision.py:198` is the source precedent. |
| `noncommit_blob`: full object ID of a blob | exit **2**, `E-REVISION-INVALID`, one refusal finding; no bound SHA | `^{commit}` disallows a blob as a commit-ish. |
| `unlanded`: valid commit not reachable from the selected local branch | exit **2**, `E-REVISION-NOT-LANDED`, one refusal finding; no bound SHA | Existing `bind()` and selftest contract (`:146–147,206`) support this. |
| `unpushed`: local branch contains the commit, but `origin/<branch>` points only to its parent | exit **2**, `E-REVISION-NOT-PUSHED`, one refusal finding; no bound SHA | Existing `bind()` and selftest contract (`:148–153,219–225`) support this. |
| `full_id`: full object ID of a landed commit | Accepted; JSON bound SHA equals that full ID | Positive object-identity control. |
| `annotated_tag_object`: unique full object ID of an annotated tag whose target is a landed commit | Accepted; JSON bound SHA equals the peeled target commit ID | Preserves the existing commit-ish contract; tag-object ID is not the expected bound SHA. |

**Count/aggregate:** `object_selector_tools=9`, covering the nine names at `tools/check-revision-binding.py:61–80`; newly discovered tools remain separately reported and do not enlarge this denominator. Overall object-selector mode is clean only when all nine pass; valid-case comparison must use the fixture's full expected commit SHA, and refusal cases must retain their single exact ID. The source does not provide literal object IDs for these new synthetic fixtures; record each fixture's expected full OIDs independently when constructing the fixture, rather than inventing values here.

**Causal criterion:** before, the input gate is a hex regex followed by general Git revision resolution; after, a hexadecimal-looking ref cannot stand in for an object, while unique actual object selectors still bind the object they identify. Preserve commit peeling, uppercase/full/unique-prefix object acceptance, and the existing local-landed/origin-pushed checks. Nine is the source-defined consumer denominator; baseline source does not support a claim that nine new object-selector probes already run or pass.

## C3 — boot-chain audit live-map calibration

**Runtime source contract (static only).** `tools/boot-chain-audit.sh:81–86` documents the normal exit vocabulary and explicitly says no schema-v2 live verdict maps to exit 1; 1 is never emitted under the live schema. In `audit()` (`:794–806`), the summary is only `UNKNOWN`/rc 2 when an unknown condition exists (or no eligible kernel evaluation exists), otherwise `CONSISTENT`/rc 0. `run_selftest()` returns 0 on pass and 1 on failed assertions (`:1217–1222`). Live preflight failures also fail closed as `UNKNOWN`/2 (`:1248–1294`). This supports the corrected distinction: live map is 0 CONSISTENT/observation and 2 UNKNOWN/could-not-evaluate; selftest 1 is a selftest failure, not live DEGRADED.

The baseline operative round-19 registry row at `SKILL.md:2073` still advertises `1 DEGRADED`; the source append at `:2086` identifies that operative-row error, while `:2096–2109` states the corrected live/selftest separation. These are source statements, not a measurement of the host. No boot image, host state, or readiness claim is inferred.

| Fixed registry fixture | Expected registry-audit result | Source support / limit |
|---|---|---|
| `legacy_live_1`: highest operative boot-chain-audit row includes `0 CONSISTENT;1 DEGRADED;2 UNKNOWN` | exit **1**, `REGISTRY-AUDIT-LIVE-MAP`, `audit_live_map_errors=1` | One false live mapping is identifiable against the shell source. The exact finding/count are the oracle contract, not emitted by baseline checker code. |
| `corrected_live_map`: highest operative row says live `0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate`, and separately says selftest `0 PASS;1 FAIL` | exit **0**, `audit_live_map_errors=0` | Matches the shell's live and selftest exit paths. |
| `selftest1_only`: code 1 appears only in the `--selftest` outcome, not the live map | allowed; exit **0**, `audit_live_map_errors=0` | A selftest failure remains meaningful and must not be treated as a live DEGRADED result. |
| `historical_row_only_fix`: correct a historical row but leave the unique highest operative round-19 row unchanged | exit **1**, `REGISTRY-AUDIT-LIVE-MAP`, `audit_live_map_errors=1` | The table-selection rule makes the unchanged operative row controlling; editing history cannot satisfy the live-map criterion. |

**Causal criterion:** change the operative live mapping of code 1 from false `DEGRADED` to “not a live verdict”; preserve code 1 only as selftest failure. Exactly one false operative mapping yields one error before and zero after. `tools/check-registry-coverage.py:219–236,281–292` is baseline generic registry coverage: it checks numeric completeness for gates/probes and exposes no `--audit-live-map` path or `REGISTRY-AUDIT-LIVE-MAP` evaluator. Thus the shell-source distinction is directly supported, but the error ID/count and historical-vs-operative behavioral assertions require the new evaluator and fixed fixtures; they are not baseline measurements.

## Residual risk and verification gaps

All oracle checks are finite source/fixture classes, not arbitrary Git-revision semantics, arbitrary program behavior, a live boot audit, or host/boot-readiness evidence. The C2 expected full OIDs need fixed synthetic fixture records; the C1/C3 new finding IDs and negative counts are not implemented by the baseline evaluators. No candidate diff was reviewed, no LSP checks or tests were performed, and no runtime or host command was executed. The report records the source-based expected behavior only.

Scope: executed=none