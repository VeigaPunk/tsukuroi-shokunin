# C1 pre-freeze attack list — CriticClaimShape

Review stamp: 02:49:56Z. Axes: **operability / C1 / attack:design**. This is a critic's evidence and proposed control inventory, not a canonical judgment, admission, implementation, or scored mutant result.

## Scope and dependency

The declaration at `6d76fb20f6ecbc940e5c8fff36c74060c885e161` was opened first with the assigned `git show`. The proposed file `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ExecProbeR36/probe-child-env-allowlist-r36.py` was absent at inspection. **D01: the successor's actual collector, invocation manifest, normalization and battery result remain [unk].** This review therefore attacks the declaration plus the existing r34 probe. The wave specification is proposal data, not permission to change the declaration. No dependency was awaited.

`[obs]` below means read bytes or existing receipts; `[inf]` means a reasoned counterexample, not an executed control. No new probes, tool mutants, runtime code, or tests were executed by this seat. Control labels A01–A15 are proposed attack-item names, not existing seat identities.

## Frozen acceptance that must not be weakened

E01 declares **all five** targets, before exposure on **each** target, after zero, empty `harness_errors`, exit 0, both historical mutants above zero, and `claim`/`r33claim`/`regression` at base zero in the same run. Its kill rule includes **any builder reading ambient, any prefix filter, any inheriting spawn**. A mutant of one target is scored against the complete five-target candidate; the other four being correct does not excuse the mutant.

A zero leak count alone is not that acceptance. A zero with a missing target, failed observer, absent required sensitivity run, wrong revision, or nonempty errors is not an after-value and must not be promoted into one. No below-zero ordinal claim is made here.

## Highest-value counterexamples

1. **The proposed untraced wrappers are unreachable as specified.** E03 puts them after `/usr/bin:/bin` in PATH. E13 says executable lookup searches from beginning to end. Installed `git`, `python3`, `bash`, and `sh` win first. Installing wrappers without proving hits yields a non-observer, not an independent channel. [inf]
2. **Fixing PATH order still cannot detect the required MutAttrgetterCopy with PATH interposition alone.** E06's mutant copies arbitrary ambient variables but explicitly restores fixed PATH. Its ordinary evidence used a direct actual-builder exercise and explicitly says a PATH wrapper would be bypassed. E07 proves the untraced leak. [obs]
3. **The required old survivors are invocation-coverage failures, not demonstrated trace-awareness.** MutPathCopy's report names the selftest's upstream fixed PATH as the reason the real reader was never exposed (E08:31). Adding an untraced run of the same selftest does not repair that fact. E06 likewise changes the production `git()` builder, not `sandbox_git()`. [obs; implication inf]
4. **The proposed permission to freeze four targets contradicts C1.** E03 says “the set may name four”; E01 requires all five. r34 itself requires a git child, whereas the btrfs mutant battery launches Python children. Keeping that eligibility rule verbatim would discard a required target for an observer-specific reason. [obs; exclusion inf]

## Attack items and pre-freeze controls

### A01 — Ambient copy with an expanded prefix/name deny-list

- **Counterexample:** preserve ambient-copy construction but enlarge the exclusions until they cover known canaries, common host names, or the generator's finite name domain; retain an untested ambient name/prefix. Merely extending the `GIT_*` or `TSUKUROI_*` blacklist is not the declared fixed-dict work. [inf]
- **Caught?** Ordinary direct `os.environ` filters are caught by r34 source scanning regardless of runtime canaries (E02:750-752). Fresh random names defeat a fixed historical name snapshot; E11 is an existing example that did not meet the after-value. Nevertheless, the generator excludes `LC_`, `GIT_`, `XDG_`, `LD_`, `PYTHON`, `PWD`, `IFS` and existing names, and bounds generated lengths at 2–200 (E02:223-234,414-438). Finite sampling cannot establish fixed-dict provenance. An indirect reader plus a filter targeted to the sampled domain is a remaining design attack, not a newly scored survivor.
- **Kill rule:** explicitly includes prefix filters; no prefix-filter exception.
- **Required control:** score an expanded-prefix/snapshot filter and a retained untested-name variant on all five; add a source-evasive reader control separately so a static hit does not masquerade as dynamic sensitivity. Expected rejection is a leak or a clearly non-accepting harness outcome, never silent target exclusion.
- **Smallest safe correction:** retain source rejection of ambient copying and test outside the canary generator's exclusions; do not describe random names as proof of exact fixed-dict construction.

### A02 — Detect the tracer, wrappers, exported tree, or other observation footprint

- **Counterexample:** the unsafe branch runs in ordinary use, but a clean branch runs when instrumentation files, altered PATH, export layout, caller, or tracing is recognizable. A fresh directory name does not make its layout or wrapper contents undiscoverable. [inf]
- **Caught?** Direct `TracerPid`/proc strings and named hiding constructs are source findings (E02:66-100,750-799). Untraced execution removes the ptrace signal but supplies a wrapper signal. E02 explicitly admits unlisted read-side hiding constructs. Base-output parity cannot distinguish two branches deliberately producing equal output.
- **Named limit?** Historical E12 names the S181 **procfs/tracer** read-side limit. It does not specifically authorize a PATH-wrapper/fixture detector. The r34 docstring has a broader known-scan limitation, but E01's r36 kill rule contains no wrapper-detection exception and calls the export a view the tool cannot tell from production. A documented observer limitation is not automatically an exception to that kill rule.
- **Required control:** separate trace-gated, wrapper-gated and export-versus-real-checkout-gated variants; establish the ordinary leak independently, then score each against the frozen full battery. A trace-aware control alone does not cover wrapper awareness.
- **Smallest safe correction:** remove the claim of indistinguishability unless supported; preserve the declared kill rule for such survivors. If an observer-awareness tradeoff is intended, the canonical owner must decide and disclose its exact pre-freeze boundary, not invent an exemption after a survivor.

### A03 — Drop only injected names, rather than stop ambient copying

- **Counterexample:** remove the fixed canary names, or remove discovered/random canaries by name/value/shape, while retaining other ambient values and overwriting the ten value-channel settings. [inf]
- **Caught?** Dropping only `BASH_ENV`, `ENV`, `GCONV_PATH`, `PERL5OPT` is caught by eight new random names in both channels; `quiet` also avoids a fixed-name-presence trigger (E02:47-65,462-492). Ordinary ambient readers remain source findings. A source-evasive filter that recognizes the entire injected population may leave all observed canaries absent without doing fixed-dict work. The value channel must remain active in quiet.
- **Kill rule:** explicitly includes the ambient reader/filter, even if every injected name was removed.
- **Required control:** fixed-four-only removal, generated-name/marker removal with value overrides, and quiet-without-fixed-canaries. Score exact full after-value; record which clause rejects each.
- **Smallest safe correction:** keep independent names/quiet/value/source checks and require a canary-targeted filter control, rather than infer immunity from randomization alone.

### A04 — Absolute-path execution bypasses PATH wrappers

- **Counterexample:** a dirty environment is passed to `/usr/bin/git`, `/bin/git`, or an absolute Python/bash child, so an untraced PATH wrapper is never selected. [inf]
- **Caught?** **Yes by retained traced channels when that spawn is actually reached.** r34 traces descendant `execve`/`execveat`, and name/value carrier checks inspect all successful parsed execs after the initial target exec, not only git (E02:285-320,357-377,495-538). `is_git()` has a narrower path list, affecting git-count/kept-setting/parity attribution, not ordinary canary checks. Absolute paths alone do not defeat strace.
- **Kill rule:** a true all-five zero survivor with a real unsafe child still falls under it. An untraced zero alone is insufficient.
- **Required control:** dirty absolute-path git and non-git children, plus a fixed-PATH ambient-copy variant. Separately verify `/bin/git` classification; do not let a classifier miss become an eligible-set reduction.
- **Smallest safe correction:** preserve traced all-child attribution and retain the parent-to-wrapper exec environment even when excluding instrumentation. Do not exclude an entire PID lineage just because it later runs a wrapper.

### A05 — Engineer a target into `harness_error` to leave the measured set

- **Counterexample:** fail or time out the control run, make A/B disagree, or start no recognized child. [inf]
- **Caught?** **Yes, if the declared conjunction is enforced.** r34 appends the target to `errors`, skips its channels, and exits 2 when errors exist (E02:911-930,1004-1010). Thus `leaking_pairs=[]` can coexist with non-acceptance. E11 contains an actual skipped target and exit 2.
- **Kill rule:** this does not satisfy its empty-errors/exit-0 premise. It is not an accepted shortcut merely because the leak count is zero.
- **Required control:** one stable control failure, one no-recognized-child case, and one timeout; verify all five identities remain declared, errors remain visible, and the battery refuses acceptance. No replacing the denominator with only successful targets.
- **Smallest safe correction:** keep the fail-closed behavior and assert complete frozen target/channel coverage alongside the zero count.

### A06 — Freeze an invocation that never exposes the unsafe builder

- **Counterexample:** a selftest runs clean sandbox builders, sanitizes the caller environment before reaching the production builder, returns from help, or stops after unrelated clean children. The unsafe production builder remains. [inf]
- **Caught?** **Not reliably.** “At least one child” proves activity, not coverage of the changed builder. Source catches simple readers but misses both committed historical reader forms. E06/E08 and E07/E09 document genuine ordinary leaks with full r34 0/27, empty errors, exit 0. These are the strongest available local counterexamples, not hypothetical new executions.
- **Kill rule:** catches any such survivor once ordinary leakage plus the complete frozen after-value is shown. Adding an untraced copy of the same non-observing invocation is not a repair.
- **Required control:** the exact committed MutAttrgetterCopy and MutPathCopy with invocation paths that reach their mutated production builders; plus one builder/site-specific regression on every livefive target. Before exposure must be attributed to that builder's real child environment, not merely to the source channel or a different helper.
- **Smallest safe correction:** freeze per-tool normal CLI argv and per-builder child evidence. For the two historical sensitivity controls, use an actual builder/ordinary CLI path, not only their original selftests.

### A07 — A child scrubs its environment after exec before the wrapper reads procfs

- **Counterexample assessed:** the final real git/Python program clears its environment before a trusted interposition wrapper can log it.
- **Caught/reasoned?** **That ordering is not possible for an actual wrapper-first execution.** Exec replaces the program (E14); when PATH selects the wrapper, the wrapper/interpreter is the program running. The eventual real binary has not executed until the wrapper logs and then execs it. It cannot race its predecessor's earlier logger. In addition, `/proc/pid/environ` reports the initial exec environment; ordinary `putenv`/environ-pointer changes do not erase that initial snapshot (E15). A script spawning an external reader must identify which process's procfs bytes it reads; `/proc/self` is relative to the opener.
- **Limits:** a late external poll of an arbitrary child is different; overwriting initial backing memory or relocating the procfs environment range can change what is read. Interpreter/loader startup precedes script logging, so trust in the collector's startup matters. None of these is evidence that the eventual real binary can run before a trusted wrapper's first action. Absolute-path bypass is A04, not a scrubbing race.
- **Kill rule:** if a genuine different construction survives, it remains subject to the rule; do not declare the ordinary post-wrapper scrub a survivor without an ordering witness.
- **Required control:** a benign real child that clears its own environment only after wrapper handoff; the wrapper's pre-handoff initial snapshot must still contain the canary. Verify against traced exec input. This is a collector-conformance control, not an executed mutant here.
- **Smallest safe correction:** log raw initial bytes before delegation, use a trusted absolute interpreter/collector with controlled startup, and document observation timing. Do not replace this with polling after child startup.

### A08 — Wrapper installation exists, but no wrapper ever runs

- **Counterexample:** the draft instructions' `/usr/bin:/bin:<inject>/<random>` PATH finds system executables first; absent log entries are interpreted as clean environments. [inf from exact proposal]
- **Caught?** Traced/source channels can still expose ordinary copying, but this does not supply the required independent untraced sensitivity. E03's proposed wrapper order directly conflicts with its claim that inheriting children hit wrappers; E13 supplies lookup semantics.
- **Kill rule:** failed observation alone is not a scored full-battery survivor. It is a fixable pre-freeze counter defect; an all-zero accepted unsafe variant would trigger the rule.
- **Required control:** prove an untraced control child actually entered each installed wrapper; record observed wrapper hits and captured ambient canaries, not merely wrapper installation or empty-log counts. Run skipped-installation mutation against the required sensitivity controls, not only obvious source-readable ambient copies.
- **Smallest safe correction:** put the interposition directory first for that view and demonstrate reachability. This fixes ordering only, not A09.

### A09 — Ambient copy with fixed PATH defeats the entire PATH-only read channel

- **Counterexample/evidence:** E06's actual MutAttrgetterCopy copies ambient via split-string attrgetter, filters GIT names, then resets PATH. E07 records `ZZ_R34_AMBIENT=1` reaching its child with parent tracer PID 0; E10 records full frozen r34 0/27. E06:27 explicitly states that a PATH wrapper would be bypassed.
- **Caught?** A correctly reached traced execution should see the leak. The unchanged r34 source scan missed it. PATH-interposition alone cannot add observation of this variant, with either PATH order. Therefore the promised sensitivity conjunction cannot be inferred merely from “untraced wrappers added.”
- **Kill rule:** directly relevant to the explicitly required historical-mutant sensitivity; this is not a named trace-awareness exception.
- **Required control:** score the exact committed mutant through its unsafe builder and show actual environment observation independent of PATH selection; also retain a pristine/restored clean comparison from committed evidence or an authorized rerun. Attribute sensitivity to the channel that really observed it.
- **Smallest safe correction:** repair invocation coverage and provide a child-environment witness that does not depend on ambient PATH for this control. Merely prepending PATH or banning one attrgetter spelling is not a general read-side repair.

### A10 — Hide the ambient reader/source dependency while keeping syntactically valid env shape

- **Counterexample:** an indirect/stdlib reader or an unscanned helper supplies ambient values to a dict display; the source channel accepts the dict shape while the selected run does not expose the branch. [inf; historical examples E06/E08]
- **Caught?** Reachable dirty execs remain dynamically visible. Source scanning is not a proof of fixed-dict provenance: it accepts `Dict`, `DictComp`, and `dict(...)` shapes and only follows detected flat `tools/<module>.py` imports (E02:674-713,823-852). The two required historical mutants demonstrate unflagged read forms.
- **Kill rule:** any actual all-five survivor still triggers it. “Not listed by AST scan” is an observer limitation, not permission for ambient builders.
- **Required control:** source-evasive ambient reader with reachable normal spawn; and one unsafe helper/second-builder path not reached by the nominal CLI. Score whole battery, not source-only.
- **Smallest safe correction:** freeze dynamic builder exposure evidence and state the static scan's actual scope; do not claim source shape alone establishes fixed-dict construction.

### A11 — Broad normalization or environment-key exemptions erase real leakage

- **Counterexample:** classify every HOME-derived/scratch-looking value, every `GIT_CEILING_DIRECTORIES`, or every 7–40-hex string as legitimate, including a direct ambient value under an unrelated key. [inf]
- **Caught?** Direct ambient source reads should still fail. But the existing calibration debt really includes legitimate computed run-private values matching ambient TMPDIR, and random short argv hashes (E05); it cannot safely be repaired with a blanket exemption. E02's raw name/value/any-name checks and parity normalization are distinct mechanisms.
- **Kill rule:** unchanged; repaired normalization must not legalize ambient-copy variants. Green historical sets alone do not establish this.
- **Required control:** paired fixtures for each normalization class: one legitimate computed setting and one actual ambient copy of the same shape, including an unrelated environment key containing a canary. Also vary a meaningful nonrandom short-hash argument so over-normalized parity cannot erase a behavior change.
- **Smallest safe correction:** scope normalization to the field and run-private relation justified by evidence. Never normalize raw leak evidence into a clean value, or exempt every key/value sharing a path shape.

### A12 — Replace real work with one clean child, cached output, or a stub response

- **Counterexample:** satisfy “starts a child” and output success without performing the target's production operation; dirty builders remain unexercised. [inf]
- **Caught?** r34 base parity compares exit, normalized stdout, git count, and normalized git argv, specifically introduced against the clean-git/no-work shortcut (E02:108-118,398-405). It helps only for the chosen argv and retained fields; count-only eligibility is insufficient. Normalization broadening must not suppress the distinguishing output/argv.
- **Kill rule:** any real skip-work variant that meets the full frozen acceptance is covered.
- **Required control:** no-op/help-only, one clean `git --version`, cached result, and a second-builder left unsafe. Require base parity to reject them for an attributable reason, not an unrelated harness failure.
- **Smallest safe correction:** retain base parity and per-builder reachability; make schema changes distinguish legitimate non-git children without throwing away functional parity.

### A13 — Fork without exec (or later environment materialization)

- **Counterexample:** a fork-only child inherits the parent's environment but makes no exec, so neither exec tracing nor PATH wrapping observes a launch environment. A child constructing its environment after an initially clean exec is also not measured by an exec-input snapshot. [inf]
- **Caught?** Dynamic r34 channels do not cover those observations. A direct `os.fork()` is listed for spawn alias checks but is not the direct inheriting-spawn branch (E02:547-550,793-794; E12's historical discussion). E04 records the earlier post-report fork exclusion as a substantive narrowing, and requires it to be named for a successor.
- **Kill rule/limit:** r36 says “every child” and “any inheriting spawn,” but does not itself restate the fork-only exclusion. Do not silently import the narrowed historical rule into a new acceptance. If the canonical owner intends an exec-only boundary, that is a pre-freeze contract/claim tradeoff, not an observer fix this seat can authorize.
- **Required control:** benign fork-only inheritance alongside an ordinary exec control; separately state whether later child-side reconstruction is claimed. No unscored fork case may be retrospectively declared outside the claim after meeting the after-value.
- **Smallest safe correction:** explicitly reconcile the declaration with the intended observation boundary before freeze, or cover the direct inheriting fork. Do not call exec-input observation proof about all possible child runtime environments.

### A14 — Execveat, oversized/unparseable environment, and noncanonical git paths

- **Counterexample:** evade the exact exec parser or git classifier rather than remove ambient copying. [inf]
- **Caught?** Retained r34 fails closed on any execveat call or unparseable exec record (E02:285-320,984-988); those must not disappear in the successor. `/bin/git` may evade git-specific counts/settings (E02:323-324), but not name/value checks for a parsed ordinary exec (A04).
- **Kill rule:** a true all-five zero accepted survivor is covered; a parsing error reported as leak is not a survivor.
- **Required control:** preserve execveat and unparseable-record negative controls, plus an absolute noncanonical git path and an ordinary non-git child. Ensure wrapper-noise removal does not drop their records.
- **Smallest safe correction:** keep fail-closed attribution and distinguish git identity from all-child leak observation.

### A15 — Zero by schema, selection, wrong revision, or target-denominator drift

- **Counterexample:** count only returned successful targets, choose a no-matching `--only`, count only one channel, score clean tool bytes instead of the mutant, or interpret an empty list as a numeric field without a frozen schema. [inf]
- **Caught?** E01's canonical command does not request `--only`, requires all five, and pins the revision. r34 itself permits `--only`, increments only selected targets, and does not assert a nonempty selection (E02:903-906); a zero-target call would be a noncanonical invocation, not the specified after-value. It emits numeric `leaking`, list `leaking_pairs`, `PREDICATE_LABEL='leaking'`, VERSION 6 (E02:215-217,1004-1008). E01 instead names `leaking_pairs`, calls the source VERSION 4 and the successor VERSION 5, and requires `--json` absent from r34's argparse. These differences must be explicit changes, not guessed equivalents.
- **Kill rule:** applies only under the frozen full probe; a selected subset cannot establish “on all five.”
- **Required control:** missing/filtered target, dropped-channel counter mutant, wrong-revision mutant setup, omitted sensitivity result, and deliberate schema mismatch; all must fail receipt acceptance. Pin exact source bytes, predicate sentence, target+argv manifest, channel set, field types and base revision across controls and after receipts.
- **Smallest safe correction:** enforce exact five identities and complete channels, numeric/list semantics, all sensitivity conjuncts, and revision binding in the battery's final line. A four-target “honest subset” remains partial evidence, not C1.

## Pre-freeze control inventory to seed wave 2

These are proposed controls, not claims that other seats have run them:

| Group | Control that must have attributable pre-freeze evidence |
|---|---|
| Exposure | unchanged five at declaration base; normal CLI and actual changed builder/child for each |
| Positive implementation | fixed-dict candidate with functional base parity and all five retained |
| Required sensitivity | exact committed MutAttrgetterCopy and MutPathCopy, each above zero; claim/r33claim/regression at base each zero under the same probe bytes |
| Filter shortcuts | expanded-prefix/name-snapshot; fixed-four-only deletion; canary-targeted deletion with value overrides |
| Observer shortcuts | trace-gated; wrapper-gated; export/real-checkout-gated, with independently evidenced ordinary leakage |
| Observer liveness | wrappers installed but bypassed by PATH order; installation skipped; fixed-PATH ambient copy; absolute-path dirty child; post-handoff scrub |
| Coverage shortcuts | help/no-op; one clean child; unsafe second builder; exact old selftest/production split |
| Fail-closed contract | error/timeout/no-recognized-child; missing target; dropped channel; wrong revision; missing sensitivity member |
| Normalization | each legitimate short-hash/path/HOME/ceiling shape paired with a real leak of the same shape |
| Existing parser clauses | execveat, unparseable input, noncanonical git path, non-git child |
| Boundary decision | fork-only child and any claimed post-exec environment reconstruction |

For each item retain the frozen probe digest, candidate/mutant identity and patch, full set+argv, per-target/channel observations, final conjunction and real exit. A control rejected only because of an unrelated harness failure establishes no sensitivity to its intended shortcut. Never change the frozen counter after its data to turn a surviving class into an exception.

## Evidence index

All local paths below are absolute. Existing reports/receipts are evidence data; they do not modify the assignment or authorize verdicts.

- **E01** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:1598-1621,1637-1656`; exact declaration opened using `git show 6d76fb20f6ecbc940e5c8fff36c74060c885e161:SCORECARD.md`.
- **E02** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/probe-child-env-allowlist-r34.py`; current read SHA-256 `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`, matching E10's frozen tool digest. Line ranges cited in items refer to these bytes.
- **E03** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1-spec.json:37-45` (`ExecProbeR36` full JSON prompt opened), also `ExecLiveViewDesign`, `ExecBeforeDesign`, `MutProbeDraft`, `MutToolMutants`. Proposal digest `ca0421909270db241d32717dcf8484988babe8eeeec81bd57f224456da1f58dd`.
- **E04** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-34-verifier-spotcheck.md:62-74,184-186`.
- **E05** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/ExecV6Calibration.md:3,13-14,80-103,145-148`: same-byte calibration debt and its attributed mechanisms, read as historical evidence, not rerun.
- **E06** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutAttrgetterCopy/variant.patch:17-24` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutAttrgetterCopy.md:3,19,27-37`.
- **E07** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutAttrgetterCopy/mutant-ordinary.json:1`: `ambient_reached=true`, `ambient_name=ZZ_R34_AMBIENT`, `ambient_value=1`, `parent_tracer_pid=0`.
- **E08** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutPathCopy/mutant.patch:8-12` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutPathCopy.md:27-31`.
- **E09** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutPathCopy/ordinary-cycle.json:23-55`: untraced, wrapper first on ambient PATH, captured exact ambient PATH in real child's environment, target exit 0.
- **E10** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutAttrgetterCopy/mutant-claim.jsonl:1,29-30` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutPathCopy/mutant-claim.jsonl:1,29-30`: both 9 targets/27 pairs, `leaking=0`, `leaking_pairs=[]`, `harness_errors=[]`, footer exit 0. Mutant revisions `7e624d9b34331272c0089c184332c45ea302ab8e` and `d0cf31b0189a4e1cc503678dba10eebe4a509ce0`, tool revision `3457f287e04f34e73f8e70d4417b14b96f903f56`.
- **E11** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C06HostSnapshotNames.md:1-13,31`: frozen 263-name filter did not meet after-value; 24 assessed pairs leak, one target harness error, exit 2.
- **E12** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:1431,1465` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ReadRunChannels.md:57-63,96-117`; historical read-side/fork boundaries, not a new r36 exemption.
- **E13** [environ(7), DESCRIPTION/PATH](https://man7.org/linux/man-pages/man7/environ.7.html): “The list of prefixes is searched from beginning to end”. Opened during this review, Linux man-pages 6.19.
- **E14** [execve(2), DESCRIPTION](https://man7.org/linux/man-pages/man2/execve.2.html): “replaced with a new program”; interpreter-script execution and envp semantics. Opened during this review.
- **E15** [proc_pid_environ(5), DESCRIPTION](https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html): “initial environment”; ordinary post-exec environment modifications are not reflected, and procfs memory-range relocation is a distinct possibility. Opened during this review, Linux man-pages 6.19.

Additional child-path evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/mutants-btrfs-space-r30.py:318-364,371-403` launches Python counter children, not git; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-census-handoff-r32.py:433-440,774-800,841-844` has inheriting export/default-resolution children as well as the live-check ambient-copy builder. One observed child is not evidence covering every builder.

Installs/updates: none. New executed verification: none. Read-only fact commands: the assigned declaration `git show`, two-source `sha256sum`, and `date -u +%H:%M:%SZ`. Production writes, VCS mutations, delegation, canonical judgment/runtime invocation: none.

## Peer evidence received after the initial handoff

Read-only follow-up evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/MutProbeDraft/mutants.md:119-153,244-276` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/MutProbeDraft.md:47-81,91-109`. These describe that seat's independently constructed draft, **not** the absent ExecProbeR36 implementation or a frozen counter. This critic has not reproduced the runs.

- The peer reports six untraced wrapper hits for run-receipt, but zero for check-report-receipts despite that target leaking on names/quiet/source. This strengthens A08/A09's distinction between no observation and a clean observation.
- The peer reports an actual collector-conformance failure: its shell `tr`/procfs shim emitted delimiters but no environment entries; substituting an environment-printing collector emitted entries. This supports A07/A08's need for a controlled known-dirty capture test and exact procfs-opener/startup semantics. It does **not** demonstrate that the eventual real child ran before a wrapper-first logger, nor establish the empty capture's root cause.
- Correct an inference in the peer's initial prose: **MutPathCopy does not keep fixed PATH**. Its patch preserves ambient PATH through `os.get_exec_path()`, and E09 proves a prepended wrapper reached its ordinary CLI. Its historical selftest failed to expose the ambient PATH upstream. MutAttrgetterCopy does explicitly restore fixed PATH. The peer was sent this distinction.
- The peer says it did not reconstruct/re-score either historical mutant (`mutants.md:265-276`); do not promote its mechanistic discussion into measured mutant sensitivity.
- A collector that misses fixed-PATH after-state children must report the observation boundary honestly. Requiring a wrapper hit from every correctly fixed-PATH target would itself reject the desired implementation. Demonstrate collector liveness with a separate known-dirty control; do not interpret a zero-hit target channel as affirmative cleanliness.

These additions preserve the original findings and kill rule; no new control was executed by this seat.
