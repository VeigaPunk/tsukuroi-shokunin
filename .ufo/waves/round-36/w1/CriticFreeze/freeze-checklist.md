# Round 36 C1 freeze-readiness — NO-GO

Axes: **operability / C1 / freeze-gate**, with calibration and existing scorer behavior as no-harm constraints.

This is a procedural freeze recommendation, not a canonical Rust judgment or claim verdict. Reviewed declaration: `6d76fb20f6ecbc940e5c8fff36c74060c885e161:SCORECARD.md`, round-36 section, lines 1589–1684. The declaration was read first with the assigned `git show`. Source snapshots are identified in `reviewed-inputs.sha256`. No probe, battery, gate, test, alternate runtime, or judge was executed by this seat.

## Direct answers

| Question | Finding |
|---|---|
| Does the after-value include the sensitivity conjuncts in the measure's sentence? | **YES, textually.** Lines 1615–1619 put `leaking_pairs` zero, empty `harness_errors`, exit 0, both named mutants above zero, and `claim`/`r33claim`/`regression` at base zero in one sentence, ending after “in the same run”. This is not evidence that those checks run. |
| Is `leaking_pairs` one frozen predicate sentence across declaration/probe/receipts? | **NO, not established.** Lines 1620–1621 assert sameness but never supply the semantic sentence defining a leaking pair. The pinned predecessor has `PREDICATE_LABEL = 'leaking'`, a numeric `leaking`, and an array `leaking_pairs`, not the declared numeric `leaking_pairs`. The successor and its receipts were absent at the final dependency inventory. |
| Does the set avoid fixture properties encoding leak/no-leak? | **Target membership: yes. Generator/views: unproved.** Lines 1601–1605 explicitly identify five production files rather than choosing targets by fixture name/length or observed score. But invocation arguments, child coverage, untraced observation, fixture distributions and view distinguishers are not frozen there. A random directory name or a fresh export does not establish non-encoding. |
| Is the declaration self-consistent? | **Not as a freeze-ready specification.** It conflates bare-probe and battery measures, calls an export production-indistinguishable, identifies a VERSION 4 predecessor whose committed executable constant is VERSION 6, and overstates the allowed environments of the existing handoff scorer. Details below. |

## Blockers, counterexamples, and smallest safe corrections

### B1 — QUALITY 73 is asserted, not specified as an executable battery

**Evidence:** Declaration lines 1613–1621 name a probe invocation and its `leaking_pairs`; lines 1652–1653 instead call the measure “the battery receipt's last line”. QUALITY 73 (`corpus/QUALITY.md:141`) requires that the declaration's counting command **is the battery**, accepting its live control and refusing its should-fail mutants; a bare counter or uncommitted bytes are development output.

**Counterexample [inf]:** A successor retaining the predecessor's ordinary per-target summary can expose `leaking_pairs=0` while separate, manual sensitivity runs fail, are skipped, or use different bytes. Merely naming those checks in prose does not make the command a battery. Conversely, comparing the predecessor's `leaking_pairs=[]` to the integer 0 is not the declared comparison. A receipt envelope's actual last line is its footer, not the tool's measurement (`tools/run-receipt.py:99–113`).

**Smallest correction:** Before freeze, define this exact command as a battery entry point, with a frozen last-stdout-JSON schema: numeric `leaking_pairs`, per-target coverage, explicit mutant/control results, and an overall result that cannot be green if any conjunct fails. State which stdout summary is extracted before the receipt footer. Commit the battery and the bytes it scores; do not substitute a separately executed selftest or aggregate counter zero. No extra wrapper is necessary if the probe itself implements the whole battery.

**Impacted axes:** C1 operability, calibration, freeze-gate.

### B2 — Label, predicate sentence, schema and successor provenance are different authorities

**Evidence:** Declaration lines 1620–1621 promise “the same sentence” without quoting one; lines 1638–1639 say predecessor VERSION 4 / successor VERSION 5. At the declaration commit, `tools/probe-child-env-allowlist-r34.py:195–217` defines the actual long `PREDICATE`, `PREDICATE_LABEL = 'leaking'`, and `VERSION = 6`; lines 1004–1008 emit numeric `leaking` and list-valued `leaking_pairs`. The pinned predecessor SHA-256 is `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`. QUALITY's round-31 correction (`corpus/QUALITY.md:159`) explicitly distinguishes a receipt label from a sentence.

**Counterexample:** A receipt can accurately say `predicate_label=leaking` and `leaking_pairs=[]` while a report relabels that as the new numeric `leaking_pairs=0` claim. The old receipt would not establish the new schema or predicate. This is an observed predecessor schema, not a demonstrated r36 failure.

**Smallest correction:** Publish one actual semantic predicate sentence before freeze, including observation channels/views, failure conditions and coverage unit. Use that exact sentence in the declaration, `PREDICATE`, and a defined receipt field; keep `predicate_label` exactly `leaking_pairs`. Explicitly define the numeric count and any separate pair-detail array. Name the actual predecessor commit/digest and executable version, and the intended successor version, without treating the stale predecessor docstring as executable identity.

**Impacted axes:** C1 operability, calibration, freeze-gate.

### B3 — QUALITY 82: export is distinguishable; required controls and changing live view are absent from the declaration

**Evidence:** Declaration lines 1653–1656 call a fresh export “a view the tool cannot tell from production” and schedule the real-checkout live view only at the after state. The inherited exporter (`tools/probe-child-env-allowlist-r34.py:327–330`) uses `git archive`; that does not supply checkout Git metadata. QUALITY 82 (`corpus/QUALITY.md:161`) requires an actual production-indistinguishable live read-only view, a second live view with per-run changed expected answer where caching is possible, and **pre-data fixture-gated and cached-live controls**, each below target.

**Counterexample [inf]:** Ordinary checkout metadata/path differences can distinguish the exported view. A behavior that is correct only in the exported invocation or returns a cached clean observation need not perform production work. No claim is made that such a variant defeats the not-yet-available r36 source channel; the declaration's indistinguishability assertion is nevertheless unsupported.

**Smallest correction:** Name the genuine live/untraced view and, where applicable, the changing second view in the frozen predicate. Score fixture-gated and cached-live should-fail variants through that full predicate before freeze. The real after-state receipt remains due after the change; its implementation and discriminator controls must not first be invented then. Record the read-only boundary: real lane/host read-only, private tool writes confined to scratch.

**Impacted axes:** C1 operability, freeze-gate.

### B4 — Strongest local counterexample: selftest sanitization can mask a real child leak without any tracer-aware branch

**Observed retained evidence, not rerun:**

- `MutPathCopy` changes normal `measure-update-recheck.py` PATH construction at commit `d0cf31b0189a4e1cc503678dba10eebe4a509ce0`. Its full predecessor probe receipt (`.ufo/waves/round-34/w2/MutPathCopy/mutant-claim.jsonl:28–30`) has no source findings, `leaking=0`, `leaking_pairs=[]`, no harness errors, exit 0.
- Its retained ordinary capture (`MutPathCopy/ordinary-cycle.json:23–55`) records `untraced=true`, `ambient_PATH_reached=true`, target exit 0, detector exit 1. The seat's explanation (`MutPathCopy.md:31`) identifies the selftest's sanitized inner environment as the masking boundary, not a tracer branch.
- `MutAttrgetterCopy/mutant-ordinary.json:1` independently records `ambient_reached=true` with `parent_tracer_pid="0"`; its report and full-set receipt describe the same frozen-probe false negative.
- Round-35 calibration did not already cure this: retained `ExecV6Calibration/r33claim-v6.jsonl:17–18` reads 8/15 leaking, exit 1; `regression-v6.jsonl:35–36` reads 22/33, exit 1. Those are historical failures, not results at the r36 base.

**Smallest correction:** Both committed mutants must become positive-leak results in the successor's same-run battery, via the ordinary production builder/CLI that actually receives the injected environment. An untraced run of the same environment-sanitizing selftest is not sufficient. The old three sets must separately reach zero at the declared base without deleting targets or normalizing away actual ambient markers.

**Impacted axes:** C1 operability, regression calibration, freeze-gate.

### B5 — Literal environment scope conflicts with existing scorer operation

**Evidence:** Declaration lines 1607–1612 require **every** child environment to have the literal system PATH and retain **only** the two tools' listed private settings. But `tools/score-census-handoff-r32.py:454–484` already constructs a fixed-key fixture environment with a stub-prefixed PATH, computed HOME/TMPDIR and many `TSUKUROI_*` seams; `:774–805` requires a run-private journalctl wrapper in its second live view. Its export and default-revision subprocesses also currently inherit the environment (`:438–440`, `:842–844`). `run-receipt.py:36–43` does not currently set the claimed retained `GIT_CEILING_DIRECTORIES` setting.

**Counterexample:** Applying the stated literal PATH/only-settings rule to the scorer's already-fixed fixture environment removes its command stubs and overrides, contradicting the existing hermetic scenario behavior. Repairing only the ambient-copy line leaves inheriting export/default-HEAD spawns, contradicting “every child”. Also, “Any non-`GIT_*` ambient name ... reaches every child” (1605–1606) is literally false for names already overridden, such as PATH in `check-report-receipts.py:320`.

**Smallest correction:** Before freeze, enumerate tool-owned computed fixture/live settings separately from ambient inheritance, preserve the existing fixed-key scorer seams, and cover every actual spawn site including implicit inheritance. Correct the before-state universal wording and the run-receipt ceiling attribution. Do not quietly narrow the claim to Git-only children or to a single builder after freeze.

**Impacted axes:** C1 operability, existing handoff/scorer behavior, freeze-gate.

### B6 — Freeze wording permits a stale-control-byte gap

**Evidence:** Lines 1645–1648 say control seats score the probe and the freeze commit names bytes; they do not expressly require those bytes to equal every scored control's bytes. Lines 1679–1683 require all wave-1 control receipts committed before freeze, which is necessary but does not alone prove byte equality. The declaration also supplies no enumerated fixture-gated/cached-live control roster.

**Counterexample [inf]:** Controls score draft A, draft B is frozen, and the old receipts are committed. That satisfies the literal order while establishing no control result for B.

**Smallest correction:** Freeze only the exact digest scored by every required control/battery receipt. Any pre-freeze change invalidates the stale results for freeze purposes and requires all controls on the new bytes. Explicitly state the complete checklist below. Preserve the fixed kill rule; no after-freeze carve-out for a successful skipper, no silent target drop, and no post-freeze predicate/schema/normalization edits.

**Impacted axes:** C1 operability, provenance/calibration, freeze-gate.

## Required pre-freeze checklist

Checked items below are declaration facts only. Unchecked means required evidence was not established in this review, not that an unrun check failed.

- [x] C1 measure sentence includes all named sensitivity conjuncts (1615–1619).
- [x] Five production file identities are listed independently of fixture properties (1601–1605).
- [ ] **PREDICATE / schema / membership manifest:** one exact sentence, `predicate_label=leaking_pairs`, numeric measure, precise target arguments, channels/views, expected target/pair counts, and fixed base identity. No `--only`, omitted failed target, or zero-target success can satisfy C1.
- [ ] **Committed counter + battery:** same command as the declaration; same-run fail-closed conjuncts; positive/live control and should-fail results visible in its last stdout JSON; exact counter/tool/mutant digests recorded.
- [ ] **BEFORE-LIVEFIVE:** all five base tools execute the relevant leaking builder/child paths; each target has at least one leaking pair; `harness_errors=[]`. An aggregate positive count is insufficient.
- [ ] **POSITIVE-FIXED-DICT:** a genuine sandbox-only all-five fixed-dict control reaches zero with functioning tools, required child activity, retained private settings and base behavioral parity. It may exist before production cutover; it is not the after claim.
- [ ] **SENS-MutAttrgetterCopy:** exact committed mutant above zero, observed through its real ordinary/untraced leaking path, with no harness error.
- [ ] **SENS-MutPathCopy:** exact committed mutant above zero, observed through its real ordinary/untraced leaking path, with no harness error.
- [ ] **BASE-claim / BASE-r33claim / BASE-regression:** each complete historical set reads zero at the explicitly named base; all expected targets/pairs present, no harness errors, same successor digest as LIVEFIVE.
- [ ] **BAD-AMBIENT-READ / BAD-PREFIX-COPY / BAD-INHERITING-SPAWN:** representative variants that violate each explicitly named kill-rule family are refused. For one-target mutants, keep the other four targets genuinely fixed so their known baseline leaks cannot mask a missed mutant; retain per-target discrimination.
- [ ] **BAD-FIXTURE-GATED:** recognized fixture/export/selftest-only correctness does not meet the full frozen target, including the production-like view (QUALITY 82).
- [ ] **BAD-CACHED-LIVE:** a cached live answer does not meet the full frozen target; provide a second live view with changed expected answer when caching is possible (QUALITY 82).
- [ ] **BAD-NO-WORK:** do-nothing/empty-builder or dropped-reader behavior is not mistaken for an improvement merely because no child carried an injected variable; base functionality/required settings remain required.
- [ ] **ROLE/SHAPE controls:** audit marker names, lengths, prefixes, directory layouts and forced contributions for leak/no-leak labels; do not credit randomized spelling as proof. Where a forced fixture contribution can be replaced by a constant, vary its multiplicity, including 0 and 2+, and score that shortcut. Fixed test-matrix sizes themselves need not vary (R35-V1-ROLE-LENGTH; R35-V2-FORCED-SHAPE-CONSTANTS).
- [ ] **Normalization discrimination:** short hashes, fixture paths, HOME-derived and ceiling paths normalize legitimate run-private differences, while an actual ambient value under an original or renamed key still counts. Keep a restored-leak should-fail case; do not obtain base zero by erasing the leak signal.
- [ ] **Coverage/viability:** explicitly handle the previously excluded paths: predecessor docstring lines 14–17 says report-receipts selftest starts no Git child, revision-binding selftest did not finish under its limit, and the btrfs mutant has no Git-starting mode. Observe the relevant non-Git child where appropriate rather than excluding the named tool or demanding a nonexistent Git child.
- [ ] **Read-only live design:** live lane/host data is not mutated; private fixtures and child writes are confined to scratch; ordinary and traced paths exercise the same relevant builder, not a pre-sanitizing substitute.
- [ ] **Receipt/commit identity:** L1 commits every required wave-1 control receipt before freeze. Each identifies measured revision, counter tool revision/digest, exact mutant/control bytes, full stdout and actual exit/timeout. Missing/held controls remain unscored, not passed.
- [ ] **Freeze equality:** freeze LOG digest equals every required control's counter digest, with all predicate, label, target-set and after-value identities agreed. Changed bytes require new controls before freeze, never a stale receipt or post-freeze repair.

### Order and no-harm guards, not premature after requirements

The actual changed-tools after receipt, genuine after live view, wave-2 falsification, C2 closure review, and the seven gates at the **first C1 change commit** remain later obligations. Do not require an after-state receipt before the after state exists, and do not defer battery/discriminator design until then. Wave-1 gate baselines are baseline evidence, not a replacement for C1 controls.

A new probe also needs its operative registry row (QUALITY 70, `corpus/QUALITY.md:138`); do not defer that solely to C2's later registry work while claiming C1 independently lands with no registry change (declaration 1660–1663, 1683). This is an integration sequencing correction, not a new C1 success condition.

## Sibling cross-check / independent-wave dependencies

### B7 — Delivered designs contradict the five-target contract and do not implement its sensitivity gate

An unsolicited message from `tsukuroi-r36.CriticClaimShape` arrived after the initial report write. It identified the routed spec's four-target allowance, unreachable PATH wrappers, and fixed-PATH mutant gap. The following source reads independently corroborated those points; peer text was treated as evidence to investigate, not as a change to the assignment.

**Routed probe design:** `.ufo/waves/round-36/w1-spec.json:39` explicitly says “Exclude any target whose control run is not viable ... the set may name four”. That conflicts with declaration 1616 and 1651: all five are required. Its proposed wrapper directory is appended after `/usr/bin:/bin`, so existing system `git`/`python3`/`bash`/`sh` resolve before the wrappers. Moving the directory earlier still cannot observe the known MutAttrgetterCopy leak: the committed `variant.patch:19–21` copies ambient values and then restores `PATH=/usr/bin:/bin`, bypassing PATH wrappers. The spec also says to keep the predicate/channels byte-identical while adding a channel and a new label, an unresolved identity conflict rather than a valid freeze specification.

**Delivered before runner:** `ExecBeforeDesign/run-before.sh` and `expected-output.md` became available during the review and were read, not run. The runner has good byte-binding checks (`:37–49`): it requires the probe to be tracked at HEAD and compares worktree/committed SHA-256. It explicitly requests all five in the expectation file and treats a missing historical mutant sandbox as a dependency, not success (`:78–98`).

However, it performs six separate probe invocations (`:73–76,87`), checks only exit codes (`:65–69`), and has no summary validator or aggregate last-line battery result. Thus it alone cannot enforce per-target leak coverage, complete sets, zero harness errors, or the declaration's same-run sensitivity conjuncts. The livefive entry point would have to enforce them internally, which remains unobserved. `expected-output.md:7–18,25–28` explicitly keeps `leaking_pairs` list-valued while the declaration names it as the zero/above-zero measure. For mutant runs the outer receipt header is deliberately bound to BASE (`run-before.sh:59`) while the inner probe actually scores a different mutant revision (`:87`; `expected-output.md:33`): those are not receipts at the mutant revision under QUALITY 77. Finally, the expectation document says “all six sensitivity runs plus the livefive run” (`:35`), but the script defines three base-set and two mutant sensitivity calls plus livefive: six calls total, not seven.

**Smallest correction:** Do not let a routed seat brief narrow the declared set. Fix viability using the relevant child type, not the inherited Git-only requirement. Replace the wrapper-only observation proposal with an independently effective untraced observation of the actual leaking builders, demonstrated on both named mutants. Reconcile predicate/channels/schema before freeze. Make the declared entry point enforce and emit the complete battery result, and bind each receipt to its actual measured revision with a separate counter tool revision. Correct the expectation's count/schema rather than reinterpreting array emptiness as a declared numeric result after data.

**Impacted axes:** C1 operability, provenance/calibration, freeze-gate. These are design findings; no new probe pass/fail is claimed.

| Requested artifact | Final observed state | Consequence |
|---|---|---|
| `ExecBeforeDesign/run-before.sh` and `expected-output.md` | Delivered and inspected; source-bound in `reviewed-inputs.sha256`. | B7 identifies exact checklist gaps; the script was not executed. |
| `ExecBeforeDesign/harness-dry.jsonl` | Header names `tools/check-recheck-commands.py` at declaration commit; stdout says PASS; footer exit 0. | A recheck-command gate smoke receipt, not a LIVEFIVE before or sensitivity receipt; it clears no C1 control. |
| `ExecProbeR36` draft | Directory absent in the latest inventory. | Predicate, numeric schema, actual observation implementation and battery behavior remain a dependency. The routed spec is not a delivered counter. |
| `CriticClaimShape` attack list | No directory artifact at the latest inventory; direct peer message received and cross-checked against spec/source. | Corroboration for B2/B7, not a substitute for same-byte control receipts. |

No peer was waited on or messaged by this seat. The roster/registry is dispatch metadata, not proof that a missing artifact was delivered. The late runner reduces one dependency gap but does not change the NO-GO.

## Disposition

**NO-GO for the freeze as currently specified.** B1–B7 are fixable before-freeze design/wording defects or unresolved required evidence. Missing sibling artifacts are additional evidence gaps, not the sole basis for NO-GO. If a skipper later meets the frozen after-value, the declaration requires C1 **not verified**; this seat does not admit the result, waive the kill, or authorize another redesign after freeze. No saturation or ordinal improvement is inferred.

Scope: read=assigned declaration, QUALITY 73/82 and nearby identity/registry rules, round-35 lessons, predecessor and five target source sections, retained mutant/calibration evidence, wave artifact listings, routed w1 spec, before-seat script/expectation/dry receipt, and one unsolicited peer message; wrote=only this seat directory; executed=read-only git show, sha256sum, mkdir. Tests/gates/probes run by this seat: none. Tool installs/updates: none.
