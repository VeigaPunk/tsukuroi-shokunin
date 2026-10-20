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
