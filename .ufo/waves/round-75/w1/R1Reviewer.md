Verdict: JT1 holds; JT2 holds; JT3 holds; JT4 partly holds; JT5 holds; JT6 partly holds. Refuse JT4 and JT6 unchanged for the frozen C1 claim.
Unchecked: no dynamic systemd execution, algebra model check, or checker acceptance run; this is source-entailment review, not admission. No pending source-reading item within the assigned six-row review.

# R1Reviewer — round 75

Axes: depth, C1 entailment, adversarial attack. Target: frozen `before/draft-rows-validated.md` lines 4–9 against the three pinned v262 snapshots. All source coordinates below are relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-75/before/src/`; draft coordinates are relative to the `before/` directory. These are recommendations, not an admission decision.

## Findings by severity

### Medium — JT6's unqualified “only” crosses the ordinary-propagation boundary

Draft line 9 correctly describes the two start classes, but its final “restart or stop propagates only as JOB_STOP or a TRY_RESTART that collapses” does not cover the adjacent graceful-stop propagation branch. `transaction.c:1199–1217` supports that statement specifically for `UNIT_ATOM_PROPAGATE_STOP`: line 1207 collapses `is_stop ? JOB_STOP : JOB_TRY_RESTART`, skips NOP at 1208–1209, and recurses at 1211. In contrast, `transaction.c:1220–1234` processes `UNIT_ATOM_PROPAGATE_STOP_GRACEFUL`, calling `job_type_propagate_stop_graceful`. That helper returns a direct `JOB_RESTART` when an existing transaction job is `JOB_START` (`transaction.c:1015–1019,1027`), without a TRY_RESTART collapse. The quote's “only” is locally correct; extending it to all propagation is not.

Additionally the frozen C1 requires per-class pull-in flags, but JT6 omits PULL_IN_VERIFY, PULL_IN_STOP, PULL_IN_STOP_IGNORED, the CONFLICTS bit, and the common IGNORE_ORDER bit. This is a completeness defect against the declared row objective, not proof that its two stated start-class flags are wrong.

### Medium — JT4 is not the declared JobResult outcome set

Draft line 7 lists seven results, while `job.h:60–76` defines thirteen operational results before the sentinels. Missing: `JOB_ASSERT`, `JOB_UNSUPPORTED`, `JOB_COLLECTED`, `JOB_ONCE`, `JOB_FROZEN`, `JOB_CONCURRENCY` (`job.h:68–73`). As an explicitly non-exhaustive selection its named members would be supported; as the frozen “JobResult outcome set” it is incomplete. “A successful JOB_DONE” also needs the source's qualification that unmet ConditionXYZ= can produce JOB_DONE without running the job (`job.h:61`). Do not turn this into “all members are negative outcomes”: JOB_DONE is explicitly successful-or-condition-skipped, and the enum does not label every other member as a failure.

### Low — JT4 quote is not whitespace-verbatim

Draft line 7 quotes `JOB_DEPENDENCY, /* A required dependency job did not result in JOB_DONE */`. `job.h:65` has ten spaces between the comma and `/*`, not one. The comment text is verbatim; the full supplied quote is whitespace-normalized. Use just `A required dependency job did not result in JOB_DONE` as the exact quote, or preserve the source spacing.

## Per-row entailment

### JT1 — holds

Checked `job.c:398–440`, particularly 399–411 and 416–424. Every stated clause is supported: commutativity at 399; immediate-collapse condition at 403–405; associativity at 407–408; mergeability transitivity at 410–411; lower-triangle storage at 399–401. The condition is essential and must not be deleted. The main diagonal is not stored (400–401); equal arguments return themselves at 431–432. The draft quote is a byte-verbatim substring of line 399, excluding the comment prefix.

Quantifier audit: “only” qualifies the stored triangle and is supported; the algebra claims are conditional, not unconditional. No overstating word in the row.

Specific JOB_STOP attack: the table does NOT store -1 for every imaginable JOB_STOP pair. It stores -1 for STOP/START and STOP/VERIFY_ACTIVE at 421, RELOAD/STOP at 422, and RESTART/STOP at 423. STOP/STOP is not stored and lookup returns JOB_STOP through 431–432. JOB_NOP and TRY_RESTART are outside the lookup domain (`job.h:21–36`, `job.c:427–429`). JT1 does not make the false all-pairs claim, so this attack does not invalidate it.

### JT2 — holds

Checked `job.c:443–479`: START/VERIFY_ACTIVE return `UNIT_IS_ACTIVE_OR_RELOADING` at 446–448; STOP returns `UNIT_IS_INACTIVE_OR_FAILED` at 450–451; RELOAD/RESTART return false at 453–472; NOP returns true at 474–475. Every clause matches the predicate. The quote is an exact substring of line 454.

Quantifier audit: “never” for reload/restart and “always” for nop are supported within `job_type_is_redundant`; they must not be generalized to every possible reason a job can be removed. Macro expansions are not among these three snapshots; the code directly supplies the predicate names, not independent expansion evidence.

### JT3 — holds

Checked `job.h:31–36`, `job.c:482–496,512–514`, and `transaction.c:1030–1046`. The quote is verbatim at `job.h:33`. The comment explicitly says “can never” and “always collapses” at 33–35; the enum assigns TRY_RESTART to the transaction-domain boundary at 36. Collapse returns NOP or RESTART at `job.c:487–496`, and transaction insertion asserts `type < _JOB_TYPE_MAX_IN_TRANSACTION` at `transaction.c:1045`. Every clause is supported.

Quantifier audit: “never” and “always” describe valid transaction construction, not behavior after bypassing assertions or violating the API's preconditions. The boundary assignment documents/enforces the exclusion; the operational reason is pre-insertion collapse, not enum placement magically performing the collapse. Crucially, ACTIVATING is included by the collapse predicate (`job.c:488–496`); do not simplify this to active-or-reloading.

### JT4 — partly holds

Checked all of `job.h:60–76`. The named constants exist; the dependency description is exact at 65; SKIPPED and INVALID have the specific meanings at 66–67. Not every clause is adequate for the frozen outcome-set contract: six operational results are missing and JOB_DONE's successful-or-condition-skipped qualification is omitted. Quote fidelity and overstatement findings are above. The risky wording is the unqualified “successful” and the set-like enumeration, not any literal “never” or “only” (neither occurs in this row).

Corrected sentence: “JobResult's operational outcomes are JOB_DONE (successful completion or skip due to an unmet ConditionXYZ=), JOB_CANCELED, JOB_TIMEOUT, JOB_FAILED, JOB_DEPENDENCY (a required dependency job did not result in JOB_DONE), JOB_SKIPPED (negative JOB_VERIFY_ACTIVE result or ExecCondition= skip), JOB_INVALID (reload of an inactive unit), JOB_ASSERT, JOB_UNSUPPORTED, JOB_COLLECTED, JOB_ONCE, JOB_FROZEN and JOB_CONCURRENCY; _JOB_RESULT_MAX and _JOB_RESULT_INVALID are enum sentinels.”

### JT5 — holds

Checked `transaction.c:811–891`. Independently counted exactly ten labelled step comments, with coordinates and operations:

1. First, 822–823: matter discovery.
2. Second, 825–827: minimize impact.
3. Third, 833–834: drop redundant.
4. Fourth, 837–839: collect unneeded jobs unless ISOLATE.
5. Fifth, 841–847: order verification/cycle repair, fatal error if unfixable.
6. Sixth, 853–859: discard unmergeable entries where possible and merge.
7. Seventh, 862–864: collect dependencies after a merge retry drops an entry, unless ISOLATE.
8. “Eights” [source spelling], 869–870: second redundant drop.
9. Ninth, 872–876: destructive check.
10. Tenth, 878–881: apply.

Every summarized stage is supported; the supplied quote is verbatim at 841. “Ten labelled steps” is true, but not ten unconditional executions: fourth/fifth and sixth/seventh live in loops, seventh is reached only after -EAGAIN, ISOLATE suppresses collections, and earlier errors prevent later stages. The row is accepted as a labelled-stage summary, not a guarantee that all ten run on every invocation. “With cycle repair” retains the source's necessary-and-possible limitation; it must not promise successful repair for every cycle.

### JT6 — partly holds

Checked `transaction.c:999–1027,1103–1126,1143–1247` and `job.c:339–365,487–496`. Start/restart guard is at 1144. PULL_IN_START really DOES supply `TRANSACTION_MATTERS` at 1146; PULL_IN_START_IGNORED supplies only the masked IGNORE_ORDER bit at 1156. The boolean is transferred into the dependency link at 1113 and stored as `.matters` at `job.c:356`. It is an edge flag, not unconditional proof that the dependency matters to every anchor: source `transaction.c:60–77` requires a fully mattering path from an anchor.

The draft quote is verbatim at 1203. The supported per-class flags are START→START/MATTERS (1145–1146), START_IGNORED→START/no MATTERS (1155–1156), VERIFY→VERIFY_ACTIVE/MATTERS (1168–1169), STOP→STOP/MATTERS+CONFLICTS (1178–1179), STOP_IGNORED→STOP/no MATTERS (1188–1189); all preserve `flags & TRANSACTION_IGNORE_ORDER`. Ordinary stop propagation at 1202–1211 matches the quote, but graceful propagation is a counterexample to the draft's unqualified “only”, as detailed above. Not every clause is supported at that breadth.

Corrected sentence: “For start/restart dependency expansion, PULL_IN_START adds JOB_START with TRANSACTION_MATTERS; PULL_IN_START_IGNORED adds JOB_START without it; PULL_IN_VERIFY adds JOB_VERIFY_ACTIVE with TRANSACTION_MATTERS; PULL_IN_STOP adds JOB_STOP with TRANSACTION_MATTERS|TRANSACTION_CONFLICTS; and PULL_IN_STOP_IGNORED adds JOB_STOP without those flags; each preserves TRANSACTION_IGNORE_ORDER. In the UNIT_ATOM_PROPAGATE_STOP branch specifically, stop uses JOB_STOP and restart uses JOB_TRY_RESTART collapsed before insertion, with NOP skipped and MATTERS set on inserted links; a flagged start also enters this branch. Graceful-stop propagation separately selects JOB_STOP, JOB_RESTART or no new job according to existing transaction jobs.”

## Residual risk and verification gaps

- The six-row draft is the reviewed object. The knowledge-entry path did not exist when initially read; the declaration diff stat showed the draft/snapshots/checkers and SCORECARD, not the final knowledge entry. No claim that later live landing bytes match this review.
- Read-only declaration/base diff stat was inspected. No git mutation, integration, judgment runtime, systemd runtime, checker execution or unrelated C2/frontier review was performed. Canonical-runtime, rerouting, saturation and resume-continuity behavior are not asserted by these six source rows and were not invented as extra review scope.
- LSP device unavailable: reading `xd://lsp` returned “No such tool”. Semantic references/definition/diagnostics were therefore unavailable; fallback text search located regions, followed by exact source reads. Search results are not presented as semantic caller proof.
- Snapshot hashes recomputed and matched both draft and SHA256SUMS: job.c `024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897`; job.h `22d7b942426402ddba376c7b713bc9937c2eaa9f5817e8735dec8d5b6cf57c3a`; transaction.c `c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3`. These establish local snapshot identity, not independent remote authenticity.
- No tools installed or updated. Scratch contained no probe artifacts and is removed before yield.

Self-evaluation: accuracy 4/5 (source-entailment rather than executed behavior); completeness 5/5 (all six verdicts, quote checks, quantified wording, four named attacks and corrections); clarity 4/5 (necessarily detailed source coordinates); actionability 5/5 (JT4/JT6 replacement sentences and explicit refusal); conciseness 4/5 (some evidence repeated between findings and rows). Overall 4.4/5. Highest-impact improvement applied: JT6 correction explicitly scopes the quote to its branch rather than deleting the contradictory graceful branch from consideration.
