## Round 75 — job-transaction reading (S314-S316, JT1-JT6)

**Core — source reading:** `corpus/knowledge/systemd-job-transaction-plane-r75.md` extends the systemd reading to the v262 job-transaction plane: merge algebra with immediate-collapse qualifications (JT1), state-dependent redundancy (JT2), try-restart collapsing before transaction entry (JT3), JobResult outcomes (JT4), the ten labelled transaction_activate steps (JT5), and per-class dependency pull-in flags with restart propagated only as try-restart (JT6). Sources S314-S316 are the pinned upstream transaction.c, job.c and job.h snapshots, not a trace of the installed manager.

**Still Frontier:** an observed transaction on this host, an observed queued job, a live merge, and host-build line numbers. Snapshot line numbers identify the v262 source reading only; neither a transient Job= value nor an empty list-jobs output proves the transaction's earlier internal steps.

**Operator-owned:** every job submission, including start, stop, restart, reload and their conditional variants, remains the operator's. This reading grants no action authority; the lane's diagnosis table only reads properties, queued jobs and the journal.
