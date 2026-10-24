# CriticClaimShape — C1 counter-shape review

Axes: **operability / C1 / attack:design**. No canonical judgment or score is issued.

Deliverable: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/CriticClaimShape/attack-list.md` — 15 individually analyzed shortcut/control classes, including all seven requested classes, with evidence, frozen-rule treatment and smallest safe corrections.

## Dependency and evidence boundary

The declaration was opened first with the assigned `git show 6d76fb20f6ecbc940e5c8fff36c74060c885e161:SCORECARD.md`. The proposed ExecProbeR36 file was absent at inspection. Actual successor behavior is **[unk]**; this is the requested fallback review of the declaration and r34 design. The wave specification was read as proposal data only. No sibling was awaited.

No controls or tests were executed by this critic. Historical receipt results below were read, not reproduced. New execution was limited to the assigned read-only declaration `git show`, `sha256sum` on the two reviewed sources, and the required timestamp command. No code, production files, VCS state, or sibling artifacts were changed.

## Strongest counterexample

**Adding PATH wrappers is not sufficient to repay the required MutAttrgetterCopy sensitivity.**

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutAttrgetterCopy/variant.patch:17-24` copies ambient variables indirectly and then explicitly restores fixed PATH.
- Its ordinary evidence, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutAttrgetterCopy/mutant-ordinary.json:1`, records `ZZ_R34_AMBIENT=1` reaching a real child with parent tracer PID 0.
- Its frozen receipt, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutAttrgetterCopy/mutant-claim.jsonl:29-30`, records 0/27, empty errors, exit 0.
- Its report at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutAttrgetterCopy.md:27` explicitly says a PATH wrapper would be bypassed.

**Smallest safe correction:** expose the actual unsafe builder and supply an environment witness independent of ambient PATH selection for this control. Record which observation channel really rejects it; installing wrappers or getting a source-only hit is not evidence that the untraced collector observed the child.

## Additional fixable pre-freeze defects

1. **Wrappers appended after system PATH are non-observing.** The full ExecProbeR36 prompt in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1-spec.json:39` specifies `/usr/bin:/bin:<inject>/<random>`. System executables resolve before the wrappers. Prepend for the interposition view and prove real wrapper hits. This still does not solve the fixed-PATH counterexample above.
2. **An untraced copy of a non-observing selftest does not repair invocation coverage.** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutPathCopy.md:31` attributes the historical survivor to selftest upstream PATH sanitization; the mutant has no trace-detection branch. Freeze normal CLI/builder exposure, not merely a child count.
3. **Four targets cannot satisfy the five-target declaration.** The drafting prompt's permission to exclude targets is proposal text, not a new contract. The r34 eligibility gate at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/probe-child-env-allowlist-r34.py:915-916` demands a git child, while `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/mutants-btrfs-space-r30.py:362-364` launches Python children. Preserve every required target while making child viability accurately cover its production operation.
4. **Schema/version identity needs an explicit cutover.** Reviewed r34 bytes are VERSION 6, predicate label `leaking`, numeric `leaking`, list `leaking_pairs`, and no `--json` argument. The declaration names VERSION 4 to 5, label `leaking_pairs` and `--json`. Freeze actual bytes, field types, predicate sentence, five target identities/argv, channel manifest and conjunctive final summary; do not treat these mismatches as interchangeable identifiers.
5. **Normalization must preserve leak evidence.** The existing calibration debt requires narrow handling of legitimate private paths and random hash argv, not a blanket HOME/ceiling/scratch/hash exemption. Pair each legitimate normalized shape with an actual ambient-copy shape before freeze.

## Requested classes: rule treatment

| Class | Does the existing design catch it? | Required pre-freeze control |
|---|---|---|
| Expanded prefix/name filter | Direct reader: source catches it; random names defeat a static snapshot. Source-evasive/domain-targeted filters remain [inf] attacks; kill rule explicitly covers them. | Expanded filter plus retained untested name; independent source-evasive reader |
| Detect wrappers/tracer/export | Named source forms are caught. Wrapper detection is not specifically named as a r36 kill-rule exception; historical S181 names tracer/procfs. | Separate observer-gated variants with independently evidenced ordinary leakage |
| Drop only injected names | Fixed four: quiet/random/value channels catch it. Dropping all identified canaries can fool sampling if the reader also escapes source detection. | Fixed-four removal and discovered-canary removal with value overrides |
| Absolute-path exec | Evades wrappers, **not reached strace exec-input checks**, including non-git children. | Dirty absolute git/non-git child, full battery |
| Engineered harness error | Cannot meet empty-errors/exit-0 acceptance if r34 fail-closed handling is retained. | Failure, timeout and no-recognized-child; retain all five identities |
| Non-observing invocation | Not reliably caught; historical survivors are direct evidence. Child count is insufficient. | Both committed mutants through real builders; each live target's changed builder/site |
| Child post-exec scrub | Not a race against a trusted wrapper-first logger: the eventual binary runs after logging. Procfs exposes initial exec environment; ordinary environment-pointer updates do not erase it. | Benign scrub only after wrapper handoff; compare pre-handoff bytes with exec input |

Detailed items A08–A15 additionally cover collector hit-rate, fixed-PATH copying, source/import gaps, normalization laundering, no-op/cached work, fork-only inheritance, parser fail-closed clauses and selection/schema/revision drift.

## Tradeoffs the canonical owner must not silently waive

- The declaration calls its export a view indistinguishable from production, but wrappers/export layout are observable. A surviving wrapper-gated variant cannot be retrospectively excused as an unnamed limit.
- Fork-without-exec was a substantive historical narrowing (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-34-verifier-spotcheck.md:73,186`). r36's “every child”/“any inheriting spawn” wording does not itself restate that exclusion. The inherited scan omits direct fork from `OS_INHERIT` at lines 543-544; exec tracers and PATH wrappers do not observe a fork-only launch environment. Reconcile scope explicitly before freeze or cover the case; this seat does not authorize narrowing it.
- Finite sampling and an explicitly incomplete source scan cannot by themselves prove universal fixed-dict provenance. Preserve the kill rule and report any qualifying counterexample, rather than declare saturation because the planned six simple mutants were rejected.

## Procfs/order sources opened

- [environ(7), PATH](https://man7.org/linux/man-pages/man7/environ.7.html): search proceeds from beginning to end.
- [execve(2), DESCRIPTION](https://man7.org/linux/man-pages/man2/execve.2.html): successful exec replaces the running program; the eventual real binary cannot precede the wrapper's handoff.
- [proc_pid_environ(5), DESCRIPTION](https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html): initial exec environment; ordinary post-exec modifications do not update this view. Explicit backing-memory/range changes or an untrusted interpreter startup are different constructions, not the proposed final-child race.

## Handoff and scope

The attack list names the exact proposed control inventory and its expected attributable rejection conditions. These are recommendations, **not exercised checks**. No new receipt or mutant result is fabricated. Actual successor bytes and scored pre-freeze controls remain missing evidence at this review's inspection boundary.

Writes are confined to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/CriticClaimShape/`. The stricter developer seat-directory bound was followed instead of writing the requested parent-level report file. This nested report is the scoped report artifact for integration.

Installs/updates: none. Production edits: none. Delegation or alternate runtime: none.

## Follow-up peer evidence and correction

Read `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/MutProbeDraft/mutants.md:119-153,244-276` after the initial handoff. It reports zero untraced wrapper hits on genuinely leaking check-report-receipts, and a shell/procfs collector that wrote delimiters but empty environment data. These are peer-reported measurements on that seat's own draft, not runs performed here or frozen-counter results. They strengthen the collector-liveness controls in A07–A09.

Do **not** carry forward the peer's initial statement that both historical mutants restore fixed PATH: only MutAttrgetterCopy does. MutPathCopy reads ambient PATH through `os.get_exec_path()`; its ordinary-cycle capture proves a prepended wrapper can reach it when the normal CLI exposes the builder. The peer was sent this correction. Its report also says neither historical mutant was reconstructed/re-scored; no new sensitivity result follows from that report.

Finally, zero wrapper hits cannot simply become a mandatory target error in every after run: correctly fixed-PATH targets bypass these wrappers by design. Require a separate known-dirty collector-liveness control and distinguish **unobserved** from **observed clean** on target channels. The full battery must still satisfy the declared all-five conjunction.
