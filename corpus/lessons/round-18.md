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
| S064 | `.ufo/waves/round-17/l1-capture/supplement-capture.txt` | 2026-10-20 | line113: “LoaderEntrySelected-4a67b082-0a4c-41cf-b6c7-440b29bb8c4f: Omarchy.linux”; bare header line2 has no timezone suffix |
| S065 | `.ufo/waves/round-18/l1-capture/pacman-events-r18.txt` (read-only retained host log ranges) | 2026-10-20 | line43: “[ALPM] upgraded elephant (2.21.0-1 -> 2.22.1-1)”; line69: “[ALPM] transaction completed” |

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


### Final falsifier dispositions and retrospective source

- C1: FxCritSemantics/Correction1–4/Prefix correctly exposed untested typed-source predicates and unbound image/directory context. Added independent capture-side extra-operand, current-init digest, LTS-hook digest, extraction-heading, directory-context and filename/copy-digest cases. CORR04 now compares the live/history SHA256s and embedded filename digest; CORR02/03 resolve actual extraction headers. Final main evidence includes an always-true-source-check mutant, not only wrong-Now fixtures.
- C2: FxJudgeAst's ambiguity is repaired with explicit consistency status_scope versus consolidation_status/consolidated_tools. FxRevEdge's unavailable-repository case now yields E-GIT-FAILED independently of branch syntax; the shared Git environment also suppresses global/system config instead of dropping those overrides. Fixed explicit empty --registry-from in freshness-r17; added caller-boundary cases. All nine still import the single binder; the judge stays independent.
- Rechecks: FxRecheckPointer was right that§7's incidental pacman-T mention did not test the actual wrong-pointer defect. Explicit Unknowns/out-of-reach headings cannot be procedure targets; baseline remains red without that mention, and a correct§6 pointer independently finds the real unsafe command. FxRecheckHeading's empty-quote/wrapper-only bypass now fails parseable-argv0 checks, with fixed-ID cases. The R18 file-read replacements remain substantive.
- Compound citations: all affected R18 records now carry complete supporting command/output ranges, not a single positive line offered as absence/multiple-property evidence. S060-only pending/checkupdates statements are narrowed to this capture, not a universal session audit. Journal hooks are dated R17 image observations; no R18 image reinspection is invented.
- S065: rather than leaving tool-obtainable historical event questions unverified, opened bounded /var/log/pacman.log ranges through read (no pacman invocation). Retained pacman-events-r18.txt shows13 elephant upgraded events and ALPM completion09:31:04, specific removals, and zcode installed/completed13:23:09. Counting command is retained in the main runner; these are ALPM receipts, not client exit/health/current classification or actor evidence. This sixth newA/mined source makes final SOURCES59→65; its exact quote/access is in Gate. S060-only evidence limits remain true of that narrower source; S065 explicitly resolves the specified historical events.
- New current-use neighbors are now93 records=49primary+44supplementary/17paths, not the intermediate88. sar standing capability, AUR R4/R5/R9/orphan and full v3 elephant-family scope are addressed. R5's literal12+1+2 enumeration is15, not14; no current payload count is claimed. earlyoom active-since is distinct from enabled-since. Mtime is no local-refresh receipt.
- Source mutable fields: S058 used-by old boot-chain-r17.md → boot-chain-r17.md,journal-boot-plane.md; S064 used-by old round18 lesson → round18,round17 lessons. Both sources reopened; no immutable cells or old HTTP W04 rows changed. Zswap precision: the source shows Y for shrinker_enabled, not the quoted enabled example; S063 never claims the raw enabled=Y spelling comes from that documentation.
- Accounting: the prior wording36individual429receipts is withdrawn;36names share one aggregate error. Operator reports44dead429; artifact-level individual causes are not invented. Final-summary citations use retained outcome-interim-144309.json rather than mutable outcome.json.
- CritNoHarm A is repaired: annotated none is a malformed/ambiguous declaration, not an observed execution; it is not silently normalized into permission. Counts never prove actual execution/absence. B's suggested in-place old-row annotation is declined because it would violate the preserved historical prefix; an explicit latest-table operative selector and committed selected-row evidence make the old rows non-operative. The final independent closure must judge that disposition; no author-side no-harm certification replaces it.

Build variants at68a8ae0 and original drafts/falsifier reports are retained as rejected same-round evidence. Post-build refinement changes only new, unadmitted R18 suffixes/registries; every pre-round knowledge/skill byte at842a531 remains the required protected prefix. Closed prior-round lessons receive appended errata, never rewrites, and the non-author spot-check remains untouched.


### Last per-surface sweep corrections

FxFresh11's final package review exposed four additional neighboring loci: foreign/explicit counts, zero-pending, no-repository/no-yay-cache, and old Snapper versions/empty configs. Added SUPPLEMENT45–48; final candidate97=49primary+48supplementary across17paths. Package-directory count is not a repeated binary -Q result; configured repos are not inferred from files in the sync directory; directory inode mtime is not an audit of the latest desc-file content write. The keyring date was a dated inference, not retroactively labelled a conflation. S060's snapshot limitation is source-bounded and retains the R17 observations while leaving persistence/restore unknown.

All primary and supplementary counts above are candidate/earlier-commit observations until main measurement. Per-surface semantic reviewers and the three separability experiments passed their bounded controls at68a8ae0: C1 survives C3 rollback; C3 survives C1 rollback; C2's nine remain clean when a discovered checker fails. The final source-predicate, pointer, declaration-classification and event-citation repairs require the final immutable main run; no unrun new check is reported green.
