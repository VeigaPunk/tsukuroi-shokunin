Verdict so far: SOURCE INSPECTION COMPLETE — six quote anchors located verbatim; complete knowledge-note draft supplied below and as a standalone seat artifact. Not a canonical claim verdict.
Still unchecked: integrated-revision frozen counter result; canonical judge outcome; host runtime transaction behavior. This seat did not execute a transaction or run the counter.

# SC1Entry — C1 knowledge entry

## Behavior, axes and gates

Axes: depth, C1 source fidelity, note completeness. Completed source-level inspection of JT1–JT6 and prepared the full entry for L1 integration. The binding file was written first with UNCHECKED status before source reads. All filesystem paths used were absolute; only this report and its seat-owned draft were written.

Frozen target `JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1` is contract data, not this seat's observed result. No checker/selftest/build/lint execution occurred. The report does not certify either frozen claim or commit landing.

## Provenance and exact operations

Source reads used `functions.read` on the seed rows, prior header lines 1–5, `before/host.txt`, `before/src/SOURCES.json`, and these inspected source ranges: `job.c:398–505`, `job.h:13–85`, `transaction.c:800–885`, `transaction.c:1090–1235`, `transaction.c:1030–1078`. Source-line output identifies the surrounding functions and every clause's support.

The requested grep-style quote location used the specialized `functions.grep` tool, not shell grep. Literal quote searches (regex punctuation escaped where needed) printed these located lines:

- `job.c:399`: ` * Merging is commutative, so imagine the matrix as symmetric. We store only`
- `job.c:454`: `                /* Reload jobs are never considered redundant/duplicate. Refer to jobs_may_late_merge() for`
- `job.h:33`: `        /* JOB_TRY_RESTART can never appear in a transaction, because`
- `job.h:65`: `        JOB_DEPENDENCY,          /* A required dependency job did not result in JOB_DONE */`
- `transaction.c:841`: `                /* Fifth step: verify order makes sense and correct cycles if necessary and possible. */`
- `transaction.c:1203`: `                        /* We propagate RESTART only as TRY_RESTART, in order not to start dependencies that`

The seed JT4 quote `JOB_DEPENDENCY, /* A required dependency job did not result in JOB_DONE */` produced `No matches found` because source alignment has multiple spaces after the comma. Replaced it with the verbatim nine-word substring `A required dependency job did not result in JOB_DONE` from the same line. All final quote anchors are at most 25 words. A short quote anchors its row; surrounding inspected lines support the other clauses.

Exact shell command executed (rc 0):

```sh
sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-75/before/src/job.c /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-75/before/src/job.h /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-75/before/src/transaction.c
```

Observed digests, agreeing with the seed rows and manifest:

```text
024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897  job.c
22d7b942426402ddba376c7b713bc9937c2eaa9f5817e8735dec8d5b6cf57c3a  job.h
c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3  transaction.c
```

Initial receipt discovery found none. E3HostProbe subsequently supplied paths, and this seat read its retained `01-surface.txt:1–100`, `02-properties.txt:1–110`, and `03-results.txt:1–110`; the final draft cites those receipts rather than the initial absence. Their commands/outcomes are quoted in the complete note below; none was rerun by this seat.

## Findings and statement changes

- JT1 and JT2: retained seed statements; merge properties at `job.c:398–440`, redundancy switch at `443–479` support every clause.
- JT3: changed causal wording from “because the enum places it…” to “the enum places it…, and it always collapses…”. The exclusion is the documented collapse rule, not a claim that enum placement alone causes runtime collapse (`job.h:31–36`; corroborating `job.c:482–496` and assertion `transaction.c:1045`).
- JT4: expanded incomplete seven-outcome wording to all thirteen named outcomes in `job.h:60–76`, distinguishing the two enum sentinels. Qualified JOB_DONE with unmet ConditionXYZ= so “successful” does not imply a start actually ran. Replaced whitespace-mismatched quote as recorded above.
- JT5: replaced unconditional “runs ten” wording with “has ten labelled steps”; preserved cycle repair only if possible and included unmergeable dropping. Seventh-step collection is conditional after merge-loop `-EAGAIN`; collection skips JOB_ISOLATE (`transaction.c:836–867`). The reading prose names those qualifications.
- JT6: expanded the seed's incomplete class account to five pull-in classes and their exact flags (`transaction.c:1143–1197`), including VERIFY and both STOP variants. Narrowed “restart or stop propagates only” to the ordinary PROPAGATE_STOP path and included the flagged-start condition, nop skip, and propagation flags (`1199–1217`). Graceful stop is expressly outside this row (`1220` onward).
- Host counts differ: frozen capture 22, later receipt 21. Preserved both, with timestamps; did not invent reconciliation or treat one as erroneous. Unit `Result=success` is not execution evidence of the entire `JobResult` set.

## Touched surfaces and out of scope

Written artifacts only:

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-75/w1/SC1Entry.md`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-75/w1/SC1Entry/systemd-job-transaction-plane-r75.md`

The intended integration path is `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/systemd-job-transaction-plane-r75.md`; this seat did not write it. No product code, SOURCE registry, scorecard, lesson, index, judge, shared state, fleet file, git metadata, or sibling artifact was edited. No runtime was launched, no tools installed, no privileged commands executed, no scratch tree created (thus none remained to delete), and no subagents dispatched. C2 closure, census, mistake mining, QUALITY assimilation, commit operations and canonical judging remain outside this seat's scope.

Recommended main-agent check: run the frozen `python3 tools/count-jt-rows-r75.py --revision <REV>` on the integrated committed revision. In particular, final source-faithful row wording differs from seed wording; this seat does not assert counter acceptance without execution.

## Complete note, ready to land

```markdown
source: S314, S315 and S316 in `corpus/SOURCES.md` (systemd v262 `src/core/transaction.c`, `src/core/job.c`, `src/core/job.h`; snapshots under `.ufo/waves/round-75/before/src/` with digests in `before/src/SOURCES.json`), plus read-only host capture `.ufo/waves/round-75/before/host.txt` and receipts `w1/E3HostProbe/01-surface.txt`, `02-properties.txt`, `03-results.txt` under `.ufo/waves/round-75/` (2026-11-04; systemd 262.1-1-arch)
verified-at: 2026-11-04 (six quote substrings located in snapshots; statement clauses inspected at the line ranges below; snapshot sha256 recomputed and agreeing with `before/src/SOURCES.json`; host capture read, not re-measured by this seat)
recheck: `python3 tools/count-jt-rows-r75.py --revision <REV>` for the six row predicates; re-run `systemctl --version`, `systemctl list-jobs --no-pager --no-legend`, and `systemctl show -p Id -p Job -p ActiveState -p SubState sshd.service` read-only; re-open the three files at the next systemd tag; cadence on-release

# systemd job-transaction plane: merging, redundancy, outcomes, activation and dependency pull-in (round 75)

The job-transaction plane constructs dependency jobs, decides which jobs matter, removes or merges entries, checks ordering and destructiveness, and applies the resulting transaction to the manager. The rows describe upstream v262 source rules, not an executed transaction on this host. S314 is `transaction.c`, S315 is `job.c`, and S316 is `job.h`.

| id | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| JT1 | Job type merging is commutative; with the merged type collapsed immediately afterwards, merging is associative and mergeability is transitive, and the table stores only its lower triangle. | source=S315 | snapshot=job.c | digest=024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897 | quote="Merging is commutative, so imagine the matrix as symmetric. We store only" |
| JT2 | A JOB_START or JOB_VERIFY_ACTIVE job is redundant when the unit is already active or reloading, a JOB_STOP when inactive or failed, while JOB_RELOAD and JOB_RESTART are never redundant and JOB_NOP always is. | source=S315 | snapshot=job.c | digest=024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897 | quote="Reload jobs are never considered redundant/duplicate." |
| JT3 | JOB_TRY_RESTART can never appear inside a transaction: the enum places it at _JOB_TYPE_MAX_IN_TRANSACTION, and it always collapses into JOB_RESTART or JOB_NOP before entering. | source=S316 | snapshot=job.h | digest=22d7b942426402ddba376c7b713bc9937c2eaa9f5817e8735dec8d5b6cf57c3a | quote="JOB_TRY_RESTART can never appear in a transaction, because" |
| JT4 | JobResult outcomes are JOB_DONE (successful completion or unmet ConditionXYZ=), JOB_CANCELED, JOB_TIMEOUT, JOB_FAILED, JOB_DEPENDENCY (a required dependency job did not result in JOB_DONE), JOB_SKIPPED, JOB_INVALID, JOB_ASSERT, JOB_UNSUPPORTED, JOB_COLLECTED, JOB_ONCE, JOB_FROZEN and JOB_CONCURRENCY; _JOB_RESULT_MAX and _JOB_RESULT_INVALID are enum sentinels. | source=S316 | snapshot=job.h | digest=22d7b942426402ddba376c7b713bc9937c2eaa9f5817e8735dec8d5b6cf57c3a | quote="A required dependency job did not result in JOB_DONE" |
| JT5 | transaction_activate has ten labelled steps: matter discovery, impact minimization, redundant dropping, garbage collection, order verification with cycle repair if possible, dropping unmergeable entries if possible and merging mergeable entries, garbage collection after a merge-loop drop, a second redundant drop, the destructive check and apply. | source=S314 | snapshot=transaction.c | digest=c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3 | quote="/* Fifth step: verify order makes sense and correct cycles if necessary and possible. */" |
| JT6 | For start or restart, PULL_IN_START adds JOB_START with TRANSACTION_MATTERS, PULL_IN_START_IGNORED adds JOB_START without it, PULL_IN_VERIFY adds JOB_VERIFY_ACTIVE with TRANSACTION_MATTERS, PULL_IN_STOP adds JOB_STOP with TRANSACTION_MATTERS and TRANSACTION_CONFLICTS, and PULL_IN_STOP_IGNORED adds JOB_STOP without either; all retain only incoming TRANSACTION_IGNORE_ORDER. PROPAGATE_STOP for restart or stop (also start flagged TRANSACTION_PROPAGATE_START_AS_RESTART) collapses JOB_TRY_RESTART or JOB_STOP, skips JOB_NOP, and adds the result with TRANSACTION_MATTERS plus incoming TRANSACTION_IGNORE_ORDER. | source=S314 | snapshot=transaction.c | digest=c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3 | quote="We propagate RESTART only as TRY_RESTART, in order not to start dependencies that" |

## Reading the rows

**JT1–JT2 — merge algebra and redundancy.** In `job.c:398–440`, the comment over `job_merging_table` states commutativity, lower-triangle storage without the diagonal, and the immediate-collapse precondition for associativity and transitive mergeability. `job_type_lookup_merge()` returns identical operands directly and swaps unequal operands into the stored triangle. These properties do not mean every pair is mergeable: the table includes `-1` entries. `job_type_is_redundant()` at `job.c:443–479` separately uses active-or-reloading for start/verify-active and inactive-or-failed for stop, always retains reload/restart, and always considers nop redundant. Mergeability and state redundancy answer different questions.

**JT3–JT4 — transaction types and result vocabulary.** `JobType` at `job.h:23–46` allows `JOB_NOP` into a transaction but excludes `JOB_TRY_RESTART`, whose boundary value and explanatory comment appear at lines 31–36. `job_type_collapse()` at `job.c:482–496` supplies the state-dependent implementation: try-restart becomes nop unless active-or-activating, otherwise restart. `JobResult` at `job.h:60–76` supplies the thirteen outcomes, not just the seed row's first seven. In particular, unmet `ConditionXYZ=` can yield `JOB_DONE`; `JOB_SKIPPED` covers negative verify-active or `ExecCondition=` skip; `JOB_INVALID` is reload of an inactive unit. The remaining comments distinguish failed assertions, unsupported unit type, garbage collection, once-only startup, frozen units and slice hard concurrency limits. Enum sentinels are not additional ordinary outcomes.

**JT5–JT6 — activation and dependency construction.** `transaction_activate()` at `transaction.c:800–881` labels its ten stages at lines 822, 825, 833, 837, 841, 853, 862, 869, 872 and 878. Stages four/five loop on repair, stages six/seven loop on merge repair, and either can return an error; the seventh stage runs after `-EAGAIN`, not on every successful merge. Garbage collection at stages four and seven is skipped for `JOB_ISOLATE`. Thus the labels are not a promise that every invocation executes ten operations. In `transaction_add_job_and_dependencies()`, `transaction.c:1103–1126` adds the job/link and returns early for an existing job, ignored requirements or nop; `1143–1197` then specifies the five pull-in classes and their flags. `1199–1217` handles ordinary stop propagation, demoting restart to try-restart and collapsing it before recursion so absent dependencies are not started. Graceful stop propagation is a separate path beginning at `1220`; JT6 does not replace that path or claim to enumerate all dependency atoms.

## Host readings

The read-only capture [before/host.txt](../../../.ufo/waves/round-75/before/host.txt), timestamped `2026-11-04T04:20:32Z`, reports `systemd 262 (262.1-1-arch)` and package `systemd 262.1-1` (lines 1–5). `systemctl list-jobs --no-pager --no-legend` has no listed rows between its command and the next command (lines 19–20); the capture therefore supplies no observed job queue or executed merge. Its `sshd.service` reading is inactive/dead with an empty `Job=` (lines 25–29), and its running-service count is 22 (lines 30–31). E3HostProbe's later [01-surface.txt](../../../.ufo/waves/round-75/w1/E3HostProbe/01-surface.txt), captured at `2026-11-04T04:27:10.622957+00:00`, reports the same version, `No jobs running.`, and 21 running services, with each command rc 0. The two counts are distinct time-stamped readings, not a single stable census. [02-properties.txt](../../../.ufo/waves/round-75/w1/E3HostProbe/02-properties.txt) shows journald service/socket and tmpfiles-clean timer active with empty `Job=` and `Result=success`; `JobType` was requested but omitted. [03-results.txt](../../../.ufo/waves/round-75/w1/E3HostProbe/03-results.txt) repeats their `Result=success`, each rc 0. A unit's `Result` property does not demonstrate the complete `JobResult` enum. These are retained observations by other seats, not live measurements by this seat.

## Limits

- These upstream snapshots describe source-level rules; they do not prove a resolved merge on this host, exercise a cycle repair, or demonstrate a destructive transaction rejection.
- There is no observed job queue in the cited capture. Empty listed output and empty `Job=` are point-in-time readings, not proof that jobs never occur.
- The host runs `262.1-1-arch`; the sources are upstream tag `v262`. Upstream snapshot line numbers are not host-build line numbers, and packaging differences are not ruled out (QUALITY 103).
- The six short quotes are anchors, not complete proofs of every row clause; the named line ranges provide the surrounding evidence. The frozen counter's target is a declared gate, not an execution result of this seat. Rechecking at an integrated revision remains necessary.
- The dependency row covers the five pull-in classes and ordinary `PROPAGATE_STOP`; it does not establish every graceful-stop/reload propagation path, unit configuration, runtime ordering, or job outcome frequency.
```

## Self-evaluation

Accuracy 4/5: all six anchors and statement regions inspected; no runtime transaction or integrated counter evidence. Completeness 5/5: six rows, exact digests, header trio, three paired reading paragraphs, host receipts, and explicit limits delivered. Clarity 4/5: JT6 is intentionally dense to retain all class flags. Actionability 4/5: complete standalone draft and embedded note provided, but L1 must integrate and exercise its revision gate. Conciseness 4/5: embedding the requested full note duplicates the standalone artifact. Average 4.2/5. Improvement priorities: main-agent integrated counter run; consider prose layout refinements only if row predicates remain intact. Self-check: these limits are visible rather than hidden behind a claim of passing gates.
