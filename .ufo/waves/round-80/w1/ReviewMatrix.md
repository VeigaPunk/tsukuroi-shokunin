# ReviewMatrix — round80 w1

Execution class: **NO-EXEC**. Axes: **depth + operability**.
Root for every relative path below: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

## Findings by severity

### Medium — KR selftest does not fully isolate ambient Git state

Reviewed copy: `.ufo/waves/round-80/w1/ExecKR/count-kr-rows-r69.py`, sha256 `3faec4a06df43e120cd33c4e9dd9405af9ec6346a92eaaded95314baa9b4eced`.
At lines151-166 `_selftest_env()` copies all `os.environ` and overrides only selected keys. Ambient `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_CONFIG_COUNT`, `GIT_CONFIG_PARAMETERS` and `GIT_TEMPLATE_DIR` remain. Lines170-172 pass this environment into fixture Git; lines188-190 run add/commit. In particular an external absolute `GIT_INDEX_FILE` redirects index writes outside the fixture despite lines181-183 verifying the worktree top-level. Template/config injection also undermines the stated hermetic interface. This is a static, unexercised error-path finding, not a claim that the recorded run escaped its fixture. Use a fixed allowlist rather than copying ambient Git controls; existing `tools/_revision.py:62-66` demonstrates that convention. Notified ExecKR. Repaired bytes would need a fresh execution receipt. C2 finite token/digest equality does not establish isolation.

### Resolved before final C1 verdict — companion source contradictions

The initial companion described OOM as marked like Unclean exit code and described on-abnormal as signal-defined; source `before/systemd.service.xml:948,988` distinguishes their on-abnormal cells, and :902-904 includes timeouts/watchdog. A revision then said the on-abnormal/on-abort columns differ in exactly one place, but :968-969,978-979,988-989 show three rows. The QUALITY94 label also claimed complete cited lines while quoting fragments (source :907 includes both watchdog and always clauses). Author corrected all these in the final bytes. Prior failing digest-bound review is preserved at `.ufo/waves/round-80/w1/ReviewMatrix/review-8a99e339.json`. No earlier failed review is promoted as a passing review.

## Final C1 semantic review

Binding file: `.ufo/waves/round-80/w1/ReviewMatrix/verdict.json`, with exactly the required three keys and six `holds`.

Reviewed draft data: `.ufo/waves/round-80/w1/ScribeMatrix/data.json`, 1406 bytes, sha256 `05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153`.
Reviewed final companion: `.ufo/waves/round-80/w1/ScribeMatrix/note.md`, 21274 bytes, sha256 `1aae7b2a5362c6e63ccdd2df1c7cb06c8712b71950c275fdc9047ab3bba67a0b`.
Independent digest calculation also matched frozen expected and raw snapshot (`12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44`). Any companion/data byte change requires renewed review; these hashes do not bless a modified landing.

Source locators below are `.ufo/waves/round-80/before/systemd.service.xml`; header policy order is :920-929: no, always, on-success, on-failure, on-abnormal, on-abort, on-watchdog. All 42 cells were independently read against the displayed raw table, not inferred from expected equality:

| Row | Source | True settings; all other settings false | Verdict |
|---|---|---|---|
| Clean exit code or signal | :932-941 | always, on-success | holds |
| Unclean exit code | :942-951 | always, on-failure | holds |
| Unclean signal | :952-961 | always, on-failure, on-abnormal, on-abort | holds |
| Timeout | :962-971 | always, on-failure, on-abnormal | holds |
| Watchdog | :972-981 | always, on-failure, on-abnormal, on-watchdog | holds |
| Termination due to OOM | :982-991 | always, on-failure, on-abnormal | holds |

Totals: 18 marked / 24 empty. Read surrounding qualifiers :877-911, :996-1015, :1064-1148, OOM :1409-1418, and oneshot example :1779-1780. Final note retains systemd/manual-stop suppression, configurable clean-status classification, oneshot rejected policies and successful-exit suppression, main-process scope of prevent/force status lists, and rate limits. OOM is explicitly a table reading, not invented causality; its marked set equals Timeout, not Unclean exit code. Exact quoted fragments agree with the source passages I read; final QUALITY94 explicitly admits incomplete-line quoting rather than claiming full compliance. No remaining source-inconsistent row or companion statement identified.

## Separate C2 selftest-quality assessment

Both executor copies genuinely invoke their own public CLI in subprocesses with committed fixture inputs and assert exit status plus output. They are not helper-only tests or unconditional success stubs.

- KR: :251-275 public invocation and positive five-row case; :276-346 negative missing note/snapshot, source/quote/digest/cell defects, invalid revision, absent directory and usage; :347-360 failure aggregation returns3. Recorded stdout reports10/10, and receipt binds the reviewed source digest. Isolation defect above remains separate from case quality.
- Transaction: `.ufo/waves/round-80/w1/ExecTransaction/check-transaction-order-r39.py`, sha256 `c7055a81f98b8462b3a34ba17545087bdb09bb17532594dd1a9823aa9b5aec33`; :175-194 fixture setup uses `_revision.clean_env()` and checks fixture top-level; :266-269 public CLI invocation; :310-362 positive8/8 and negative entry/source/quote/header/malformed/duplicate/count/revision cases assert rc and parsed fields; :371-378 setup failures return3. Receipt digest matches; recorded stdout reports9/9. Minor limitation: `has_reason` at303-308 is unused, so several negatives assert aggregate seven verified rather than the specific failure reason; this does not negate genuine isolated positive/negative coverage.

These are read-only code and receipt reviews, not independent test executions. The frozen instrument at `tools/measure-round80.py:24-44,45-64` is only finite equality/binding; controls.json records11 green controls, not review authenticity. Its own selftest :75-79 checks only absent evidence and must not be represented as the two tools' substantive test coverage.

## Residual risk and verification gaps

- `corpus/SOURCES.md:340` ends the current registry at S329; S330 absent when reviewed. Draft note explicitly discloses this. Final C1 admission still requires the real source row and byte-identical companion landing; this report does not assert the integrated count42.
- No integration, source edits, Git/jj mutations, builds, tool runs, host checks, installs, sudo, package transactions or service operations performed. No scratch tree created, so none remains to remove.
- LSP device unavailable: `read xd://lsp` returned “No such tool.” Static file reads and literal searches were used, not presented as semantic reference/diagnostic proof. Caller/definition/diagnostic server checks therefore unavailable. No runtime/rerouting/resume changes are present in these assigned artifacts; no resume-continuity or runtime-saturation conclusion is made.
- Verdict is a scoped semantic recommendation, not promotion authority. Main must resolve the KR isolation finding and independently assess landing/receipts; no claim of full inherited gate-debt closure.

Self-evaluation: accuracy4 (static environment defect not exercised); completeness4 (landing and runtime checks excluded by NO-EXEC); clarity4 (separates C1 from C2 and historical failures); actionability5 (exact sites and required renewal named); conciseness4 (historical binding detail retained for audit). Overall4.2/5. Highest-value next action is the fixed KR environment plus new authorized receipt; then compare landed artifact hashes to the binding file. Would the user agree? Expected yes: the remaining C2 risk and absence of admission authority are explicit.

## Post-review KR amendment

After the initial report, ExecKR replaced the copied environment with an explicit allowlist. Independently read the amended copy at :152-174 and :219-221: Git control variables are absent, HOME/TMPDIR point to the temporary root, and system config is disabled. The original medium Git-control finding above is **resolved in this amended implementation**, retained above as historical evidence. ExecKR reports renewed green/red runs and digest `44b62b3353b8a30bdadcb25a70e8a481c6f83c2cfc433c2d78a79116d789d88e`; those newly reported receipt bytes were not independently bound in this amendment.

Residual trust boundary: :162 still inherits PATH. This permits executable substitution; HOME/TMPDIR are not filesystem confinement. ExecKR's message claiming a hostile PATH cannot write outside the sandbox or alter receipts is unsupported and was explicitly corrected back to the author. Pin PATH as `_revision.clean_env` does, or limit hermeticity to a trusted resolved Git binary. No exploit run. C1 matrix verdict is unaffected by this separate C2 amendment.

## Final KR resolution

Supersedes the outstanding KR concerns above: independently read final `_selftest_env` at :152-176. PATH is now pinned to `/usr/bin:/bin`, all other environment entries are explicit, and the docstring states trust in the system Git executable rather than OS filesystem confinement. The author withdrew the unsupported confinement claim. Independently calculated final tool sha256 `908592d2f8a209fdd070c6adc3157f04d69fcfe6815bda5ceb3d9981848ac97d`, matching the renewed binding receipt; read that receipt (rc0, passed10, failed0) and renewed stdout (10/10), with red-control rc3 recorded in the receipt. These are corroborated executor runs, not reviewer executions. **No unresolved actionable KR isolation finding remains in the reviewed final copy.** Availability of system Git at the pinned PATH remains an explicit deployment assumption, consistent with `_revision.clean_env`.

## Final production-companion renewal

At L1's request, independently read the replacement production companion `corpus/knowledge/service-restart-matrix-r80.md` in full (:1-173), production JSON (:1-88), cited ExecHost handoff, and final S330 registry row at `corpus/SOURCES.md:341` including its complete raw line. This supersedes the draft-companion binding and pending-registration gap above.

Production JSON remains1406 bytes, sha256 `05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153`. Production companion is7038 bytes, independently calculated sha256 `81006519e1b5f4d9144c8b6003536204d749f3b1428578aac115b8b5e28e4a56`. Renewed `ReviewMatrix/verdict.json` binds these final production bytes and six holds; prior passing draft verdict retained at `ReviewMatrix/verdict-draft-1aae7b2a.json`, in addition to the earlier failing review.

Final note's decision table :22-27 preserves all42 source cells. Six complete raw XML row excerpts :67-155 match source :932-991, including all seven entries per cause; each has at most25 whitespace-delimited words. Provenance trio now occupies lines1-3 with literal on-release cadence. Qualifiers :35-51 retain manual-stop suppression, configurable clean exits, oneshot rejection and success suppression even for force-listed statuses, main-process prevent/force scope, helper exclusion and start-rate limiting. Source registry row is docs/A/mined, contains pinned URL/digest, both companion used-by paths, and covers every cited source range. Host handoff reference :57-58 correctly distinguishes failed scopes from services and makes no historical-cause inference. Finite-gate authenticity limits and lack of installed-build equivalence remain explicit. No unresolved source inconsistency identified in these final bytes; no new execution performed.

Scope: executed=none
