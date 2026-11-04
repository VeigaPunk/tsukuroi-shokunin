# systemd job-transaction plane: job merging, redundancy, result and collapse rules, activation stages and dependency pull-in (round 75)

source: S314, S315 and S316 in `corpus/SOURCES.md` (systemd v262 `src/core/transaction.c`, `src/core/job.c`, `src/core/job.h`; snapshots under `.ufo/waves/round-75/before/src/` with digests in `before/src/SOURCES.json`), plus the read-only host receipts `before/host.txt` and `w1/E3HostProbe/` under `.ufo/waves/round-75/` (2026-11-04; systemd 262.1-1-arch)
verified-at: 2026-11-04 (snapshot sha256 compared with `before/src/SOURCES.json` and `before/src/SHA256SUMS`; every quote located verbatim in its snapshot; rows reviewed independently by the wave's R1Reviewer, which held JT1, JT2, JT3 and JT5 and supplied the corrected JT4 and JT6 sentences landed here)
recheck: `python3 tools/count-jt-rows-r75.py --revision <REV>` for the six row predicates; re-run the read-only reads `systemctl list-jobs`, `systemctl show -p Job -p JobType -p Result -p NRestarts <unit>` and `systemctl show -p Result <unit>`; re-open the three files at the next systemd tag; cadence on-release

The job-transaction plane is the layer between "a client asked for a job" and "the manager
runs it": how two requested job types for one unit merge, which jobs are dropped as redundant
before they run, which job types may enter a transaction at all, what a job can end as, the
staged pipeline that turns a queue of prospective jobs into installed ones, and which
dependency atoms pull a job in with which flags. Every rule row below is anchored to one
committed snapshot under `.ufo/waves/round-75/before/src/`; the digest cell is the sha256 of
those exact bytes and the quote cell carries the sentence the row was written from.

| id | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| JT1 | Job type merging is commutative; with the merged type collapsed immediately afterwards, merging is associative and mergeability is transitive, and the table stores only its lower triangle. | source=S315 | snapshot=job.c | digest=024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897 | quote="Merging is commutative, so imagine the matrix as symmetric. We store only" |
| JT2 | A JOB_START or JOB_VERIFY_ACTIVE job is redundant when the unit is already active or reloading, a JOB_STOP when inactive or failed, while JOB_RELOAD and JOB_RESTART are never redundant and JOB_NOP always is. | source=S315 | snapshot=job.c | digest=024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897 | quote="Reload jobs are never considered redundant/duplicate." |
| JT3 | JOB_TRY_RESTART can never appear inside a transaction because the enum places it at _JOB_TYPE_MAX_IN_TRANSACTION and it always collapses into JOB_RESTART or JOB_NOP before entering. | source=S316 | snapshot=job.h | digest=22d7b942426402ddba376c7b713bc9937c2eaa9f5817e8735dec8d5b6cf57c3a | quote="JOB_TRY_RESTART can never appear in a transaction, because" |
| JT4 | JobResult's operational outcomes are JOB_DONE (successful completion or skip due to an unmet ConditionXYZ=), JOB_CANCELED, JOB_TIMEOUT, JOB_FAILED, JOB_DEPENDENCY (a required dependency job did not result in JOB_DONE), JOB_SKIPPED (negative JOB_VERIFY_ACTIVE result or ExecCondition= skip), JOB_INVALID (reload of an inactive unit), JOB_ASSERT, JOB_UNSUPPORTED, JOB_COLLECTED, JOB_ONCE, JOB_FROZEN and JOB_CONCURRENCY; _JOB_RESULT_MAX and _JOB_RESULT_INVALID are enum sentinels. | source=S316 | snapshot=job.h | digest=22d7b942426402ddba376c7b713bc9937c2eaa9f5817e8735dec8d5b6cf57c3a | quote="A required dependency job did not result in JOB_DONE" |
| JT5 | transaction_activate runs ten labelled steps: matter discovery, impact minimization, redundant dropping, garbage collection, order verification with cycle repair, job merging, a second collection and redundant drop, the destructive check and apply. | source=S314 | snapshot=transaction.c | digest=c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3 | quote="/* Fifth step: verify order makes sense and correct cycles if necessary and possible. */" |
| JT6 | For start and restart dependency expansion, PULL_IN_START adds JOB_START with TRANSACTION_MATTERS, PULL_IN_START_IGNORED adds JOB_START without it, PULL_IN_VERIFY adds JOB_VERIFY_ACTIVE with TRANSACTION_MATTERS, while PULL_IN_STOP adds JOB_STOP with TRANSACTION_MATTERS and TRANSACTION_CONFLICTS and PULL_IN_STOP_IGNORED adds JOB_STOP without those flags; in the PROPAGATE_STOP branch stop uses JOB_STOP and restart uses a collapsed JOB_TRY_RESTART, and graceful-stop propagation separately selects JOB_STOP, JOB_RESTART or no new job according to existing transaction jobs. | source=S314 | snapshot=transaction.c | digest=c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3 | quote="We propagate RESTART only as TRY_RESTART, in order not to start dependencies that" |

## Reading the rows

JT1 and JT2 are the merge arithmetic (`job.c:398-479`, S315). The merging table at
`job.c:416-424` stores only the lower triangle of a symmetric matrix, because "A merged with A
is simply A" and the main diagonal is therefore never stored; `job_type_lookup_merge` swaps its
arguments so the larger value indexes the row (`job.c:426-440`), and the comment at
`job.c:399-411` states the qualification the row keeps: commutativity holds unconditionally,
while associativity and mergeability transitivity hold **if the resulting type is collapsed
immediately afterwards** — `job_type_merge_and_collapse` does exactly that (`job.c:518-529`).
`job_type_is_redundant` (`job.c:443-479`) is the drop predicate: start and verify-active are
redundant once the unit is active or reloading, stop once it is inactive or failed, reload and
restart are never redundant (the comment at `:453-472` explains the ACTIVATING restart case),
and nop is always redundant.

JT3 and JT4 are the enum boundaries (`job.h:8-76`, S316). `JOB_TRY_RESTART` sits at
`_JOB_TYPE_MAX_IN_TRANSACTION` (`job.h:33-36`) because it never enters a transaction: the
collapse in `job_type_collapse` (`job.c:482-515`) turns it into `JOB_RESTART` while the unit is
active or activating and into `JOB_NOP` otherwise, and `transaction_add_job_and_dependencies`
asserts `type < _JOB_TYPE_MAX_IN_TRANSACTION` (`transaction.c:1045`). `JobResult` (`job.h:60-76`)
is the outcome vocabulary a job reports: one success member with the ConditionXYZ= skip
qualification, four flow outcomes (canceled, timeout, failed, dependency), three short-circuit
outcomes (skipped, invalid, assert), and the terminal states unsupported, collected, once,
frozen and concurrency; the two underscore-prefixed members are sentinels, not outcomes.

JT5 and JT6 are the transaction pipeline (`transaction.c:800-1247`, S314). `transaction_activate`
carries ten labelled step comments (first at `:822`, tenth at `:878`): the fourth and fifth, and
the sixth and seventh, sit in retry loops — the fifth returns `-EAGAIN` when the ordering graph
is cyclic and re-runs the fourth, the sixth returns `-EAGAIN` when a merge dropped an entry and
re-runs the seventh — and `JOB_ISOLATE` suppresses both collection steps, so "ten labelled
steps" describes the pipeline, not ten unconditional executions. The pull-in block
(`:1143-1217`) is the per-class flag map: required start and verify atoms carry
`TRANSACTION_MATTERS`, their ignored variants do not, required stop adds `TRANSACTION_CONFLICTS`,
and every recursion keeps the caller's `TRANSACTION_IGNORE_ORDER`. Inside the
`UNIT_ATOM_PROPAGATE_STOP` branch a restart is propagated only as `JOB_TRY_RESTART`, collapsed
against the dependency so an inactive unit yields `JOB_NOP` and is not started; the later
graceful-stop branch (`:1220-1247`) is a different rule — it reads the jobs already in the
transaction and returns `JOB_STOP`, a direct `JOB_RESTART` when a `JOB_START` is already queued
(`:999-1027`), or `JOB_NOP` when a stop or restart is already in place.

## Host readings

Read-only captures in `.ufo/waves/round-75/before/host.txt` and `w1/E3HostProbe/`: systemd
262.1-1-arch (`pacman -Q systemd`), twelve entries from `systemd-analyze unit-paths`, no queued
jobs at capture time (`systemctl list-jobs` printed nothing), and `systemctl show -p Job` empty
for the probed units. These readings establish the installed version and the idle state of the
job queue; they do not observe a transaction, a merge or a job result.

## Limits

- No transaction was built and no job was queued in these readings; every rule above comes from
  the pinned source bytes, not from observed manager behaviour.
- `UNIT_ATOM_*` membership (which `After=`, `Requires=`, `PropagatesStopTo=` setting maps to
  which atom) lives outside the three snapshots, so the rows state the flag each atom receives,
  never the unit-file directive that produces it.
- `job_type_is_redundant`'s three macro predicates (`UNIT_IS_ACTIVE_OR_RELOADING`,
  `UNIT_IS_INACTIVE_OR_FAILED`, `UNIT_IS_ACTIVE_OR_ACTIVATING`) are expanded outside the pinned
  snapshots; the rows quote the predicate names, not their expansions.
- The host runs a distribution build of 262.1; the line numbers above are upstream tag lines and
  are not verified against the installed binary's build (QUALITY 103).
- Nothing here authorises building, cancelling or forcing a job, a `systemctl start/stop/restart`,
  a `daemon-reload`, or any unit edit; every such write remains operator-owned.
