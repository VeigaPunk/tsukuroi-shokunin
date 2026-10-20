# Round 18 — lesson (tsukuroi, 2026-10-20)

author: tsukuroi L1 (TsukuroiR18-2). Baseline `842a5312b704b5cda10fd80ec1fdee5fb381ba97`; prerequisite `51dd9eeaa305539fa3cfc6ee275978dc18043b79`. Motivating evidence: `round-17-verifier-spotcheck.md` §5 and `LOG.md` round18 entries.

## Gate

| Candidate | Decision | Evidence and limits |
|---|---|---|
| Consolidating revision binding changes no behavior | reject | Same independent evaluator on baseline: bound9/9 but consistent1/9; six copied-code divergences were real (`measure/c2-before-842a531.json`). First-error precedence and uniform branch findings deliberately change malformed-input behavior, not domain verdicts. |
| Shared `tools/_revision.py` replaces the independent judge | reject | Judge must not import the implementation it grades; `tools/check-revision-binding.py` keeps separate bind logic and fixed expected fixture ids. |
| Current installed count remains1394 after the morning upgrade | reject | S060 capture line25 is1395 at16:06; later log entries identify zcode installation at13:23. Historical1394 remains a dated capture, not current inventory. |
| Snapper configs prove a tested rollback path | reject | S060 records filenames `home`/`root`, not restoration, snapshot consistency or a test boot. |
| Pending updates are now zero | reject | No pending-update query or metadata refresh ran. Installed directory names and a historical full-upgrade log do not answer pending updates. |
| S060 dated observations | admit as source, narrow scope | Capture script and digest are committed; no pacman/sudo/service/boot action. Runtime enabled state is not OOM causality or pressure health. |

### Sources opened this round

| Row | URL/path | Access date | Located quote (≤25 words) |
|---|---|---|---|
| S060 | `.ufo/waves/round-18/l1-capture/host-capture-r18.txt` | 2026-10-20 | line34: `/var/lib/pacman/local/mkinitcpio-42.2-1`; lines17-18: `active` / `enabled`; lines76-77: `home` / `root` |
| S061 | https://git-scm.com/docs/git-merge-base | 2026-10-20 | OPERATION MODES > --is-ancestor: “Errors are signaled by a non-zero status that is not 1.” |
| S062 | https://git-scm.com/docs/git-check-ref-format | 2026-10-20 | DESCRIPTION rule3: “They cannot have two consecutive dots .. anywhere.”; rule6 forbids beginning/ending slash. |
| S063 | https://docs.kernel.org/admin-guide/mm/zswap.html | 2026-10-20 | Overview #overview: “Zswap can also be enabled and disabled at runtime using the sysfs interface.” |

S051 reopened at boot-chain-capture.txt:59,124,182-184,198-200 for C1 count/citation corrections; opening a prior source does not rewrite its immutable `opened` field. S060 is the sourced C3 claim. No inherited SOURCES row was changed by this initial curation; mutable-field changes, if any, are logged in the final outcome below.

## Mistakes

| ID | Class | Evidence | Captured-by | Fix shown able to fail |
|---|---|---|---|---|
| R18-COPY-DIVERGENCE | survivor / reference-drift | R17 FxSimplifyBind lists bad-branch ids, branch/revision precedence, merge-base≥2, duplicate root-dac findings, missing branch, malformed branch strings. Baseline judge output: bound9/9 but consistent1/9, shared0/copies9. | QUALITY27 covered landing but not a shared semantic contract | Shared `tools/_revision.py` plus independent judge's seven divergence probes; baseline `842a531` fails exit1 (`.ufo/waves/round-18/measure/c2-before-842a531.json`). Shared selftest37/37 and judge40/40 at prerequisite51dd9ee. |
| R18-BOOT-LOCATORS | number-drift / reference-drift | R17 closure defect3:13 named packages vs12 at capture59; bothUKI equality missing linux-lts198-200; mtime reference115 names history copy not live124. | QUALITY2/10/23 | Named appended corrections and independently resolved capture-line records, never rewriting the historical note. The final outcome records actual stale-before and repaired-after outputs. |
| R18-REPORT-TAIL | landing / provider | R17 closure defect1:cca3343 and661020f landed after final report addendum; outcome.json stayed29delivered/16running although final37delivered/44dead. | PROTOCOL lands-last; no round-local final tally reconciliation | Preserve interim outcome as historical evidence, append final derived outcome and cover both late commits in this round's report; report18 lands after its final lane commit. |

## Routed defects from round17

1. Report coverage/final tally: prior report immutable; round18 report names cca3343/661020f and final81/37/44 derivation.
2. Shared binding: C2, seven explicit divergence probes and original-nine continuity measure.
3. Boot count/citations: C1 named appended correction, historical verdicts preserved.
4. Registry/capability count drift: superseding round18 registry and capability count clarification, never false claims that old rows were current.
5. Freshness backlog: C3 eight named target files and additional sweep findings; only verified records credited, unknown pending state stays unknown.
6. Indirect recheck pointer: aur-risk §7 resolution and an appended R18-RECHECK procedure; ordinary pointer-only text must no longer evade the gate.
7. L1 execution scope: shell wrapper emits command/output/rc itself in R18 host capture; earlier R17 hand-written excerpt remains limited historical evidence.
8. Seat scope: remeasure round17 build/falsify at immutable842a531; reconcile30 versus29, record all deviations instead of authorizing them after the fact.
9. Dead outside attacks: re-attack separability, README frontier, sibling-overlap and frozen-marker in build and falsify seats.
10. Routing map: operator/protocol-owned; current addendum critic→m_swe, sentinel→m_opus controls; MISSION role-class buckets are now explicitly advisory. No lane edits of routing configuration or aliases.

## Inherited and non-author files

`corpus/lessons/round-17-verifier-spotcheck.md` read and preserved; no initial uncommitted lane state at dispatch. jj helper state: local=remote842a531, ahead0/behind0/tracked0/untracked0. Host safety read-only throughout: no pacman, sudo, service restart or boot-file writes. No tool installed in this initial phase.

### Execution provenance and sourced semantics

S061 grounds C2's fatal-git versus non-ancestry distinction; S062 grounds malformed literal branch rejection. S063 supports the narrow runtime-parameter explanation, not the undocumented `Y` spelling or a pressure verdict. New rows4, all tierA/mined; no inherited mutable fields changed in this curation. S060 is cited by current-use notice drafts and the admitted-source decision above.

R18's command/output log is bound to the actual capture invocation and tool-result records in `.ufo/waves/round-18/l1-capture/harness-probe-capture.json` (record ids `e6ad937b`/`cff2269b`, matching tool-call id). It omits thinking and unrelated session data. This is an exact harness excerpt for one wrapper capture, not a claim to exhaustive shell tracing; the script emits `$ command`/output/exit itself. The old R17 excerpt remains historical and is not retrospectively upgraded into a harness trace.

Mutation evidence: build/MutateShared.md kills three isolated precedence/fatal-git/first-error mutants (each36passed/1failed exit1); pristine/restored37/37 exit0. No production mutation or host action.


### First-falsifier decisions and integration repairs

- CritDepth's counterexample is accepted: a self-consistent registry can omit an actual defect or say the wrong `now`. C1 is hardened with MigBoot's domain-specific `--statement-corrections` mode, four fixed IDs and source arithmetic/digest/mtime checks; generic notice mode is not presented as semantic proof.
- CritSeparability's denominator contamination is accepted: C2 grades only the original nine, with discovered tools fully observed but informational. C1/C3 registries and targets remain disjoint. The generic checker adds homogeneous ID-family, unique quote and l1-capture-only reference constraints; C3 additionally reports the17-path count and primary eight-file coverage.
- ReviewJudge/ReviewIndependence/CritOperability: dead import text is not shared use; judge uses AST import+bind-call census outside constant-false branches, rejects extra unrelated findings, checks every refusal's one-ID shape and the origin-absent path. This is bounded structural/runtime evidence, not protection against a deliberately probe-aware malicious script.
- SentRevision: clone isolation was not process isolation. Trust boundary is now explicit; judge suppresses ambient global/system Git config and uses empty hooksPath. Executed candidates are reviewed local gate code, not untrusted external input. Resource/descendant containment is not claimed.
- ConnL0: B:82 is truncated, so the12-package correction cites only complete argvB:59. Do not confuse12 packages with13 historical pacman invocations or revive withdrawn hook-override option(b).
- ConnW04/ReviewFrozen: appended active S058-versus-S051 source-scope clarification and withdrew SKILL's historical JSON-oracle authority. No immutable source row or prior fixture was rewritten.
- RerunSeats at immutable842a531 confirms build30 unauthorized declarations (not lesson29), falsify19 unauthorized and44 missing (not the earlier worktree16/52). Exact pinned outputs are in build/RerunSeats-*-output.txt; these remain deviations, never retrospective authorization.
- Capture precision:1395 is a count of listed local-db entries;13:23:09 is the last captured log event, not an independently verified installation transaction. Filemtime is not local metadata refresh time; invocation text is not completion. Narrowed five AUR notices accordingly (`build/integration-proposition-repairs.json`).

39 supplementary correction-sweep records join49 primary freshness records across17 paths. Boot/systemd/recovery no-new-evidence results remain bounded rejections, not fabricated refreshed values. For every notice the original dated snapshot is preserved; current pending updates and unmeasured executable/unit/snapshot details stay unknown.


### Late source precision correction (S064)

ReviewSources5156 found the round17 Gate's loader-variable string was elided, not literally verbatim, and S056 appended a timezone absent from its capture header. Reopened `.ufo/waves/round-17/l1-capture/supplement-capture.txt` on2026-10-20: line113 exact quote “LoaderEntrySelected-4a67b082-0a4c-41cf-b6c7-440b29bb8c4f: Omarchy.linux” (two whitespace tokens); line2 `captured: 2026-10-20T13:03:06` has no timezone. S064 (own-work,A,mined) supersedes S056 only for this header/loader precision. Fallback hashes,448 recount and journal/fstab scope remain the other supported S056 observations; no boot verdict changes. S051's snapshot-entry wording denotes configured image bytes, not proof that an unbooted entry ran.

Final curation now59→64 (five new tierA/mined rowsS060–S064), rather than the initial59→63 snapshot. No inherited mutable field changed. The initial4-source search paragraph is a dated intermediate record; this additional identified/screened/included own-work correction is1/1/1, excluded0. No W04 rows merged or immutable S056 cells rewritten.


### Process deviations retained, not approved

- Several no-execution build seats ran read-only Git/text/Python inspections; e.g. NoticeForeign acknowledged its commands after L1's scope reminder, and SrcZswap/SrcGitMerge disclosed shell reads. Some trailers say `executed=none` while describing read-only commands elsewhere; a self-reported Scope parser cannot establish absence of execution. These are QUALITY24 deviations, not harmless-by-definition authorization. No disclosed command is a package transaction, service change or boot write. Exact final scope counts and missing-seat identities are retained in the final evidence/report.
- L1 completed full canonical re-read after phase0 and dispatch rather than the addendum's required load order; early exploration also used shell text-reading helpers where specialized tools were available. This is a process/tooling conformance defect, not a claim that the later re-read retroactively fixed ordering. No protocol or host routing configuration was edited.
- A build reviewer (RerunExecLog) died with provider invalid_prompt; it is not relabelled429 or replaced. L1's assigned immutable final verification covers the reachable exec-log work. A dead seat remains dead in both registries and the report.

A round's independent closure still decides admission/no-harm. Author-side source checks, code reviewers and mutation results do not constitute a new outside SHONEN verifier.
