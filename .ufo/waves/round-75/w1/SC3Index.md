# SC3Index — round 75 w1 binding report

Verdict: FOUR DRAFTS DELIVERED; NOT LANDED OR JUDGED. Static revision-pinned counting commands executed successfully; no C1/C2 gate, selftest or host job probe executed by this seat.
Unchecked: integration into canonical documentation, complete C2 closure, semantic admission by reviewers, and canonical Rust judgment. The proposed note was initially absent; JT identifier mapping was subsequently confirmed by SC1Entry-6. No execution evidence is inferred from that confirmation.

## Behavior and axes

Seat axes: calibration, C2, skill. Delivered the five-symptom read-only diagnosis table, Core/Frontier/operator boundary, corpus index row, and six-axis table. Ordinals remain depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. Counts describe document surfaces only and do not derive those ordinals.

## Commands and outcomes

Initial command, cwd `/home/vgpnk/Projects/shokunin`:

```sh
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && git rev-parse HEAD && wc -l SKILL.md PROVINCE.md corpus/README.md SCORECARD.md corpus/knowledge/systemd-job-transaction-plane-r75.md corpus/lessons/round-75.md corpus/lessons/round-74.md 2>&1
```

Observed HEAD `1e2bb29cb452d49822e35ada0f5fad419b19e24c`; line counts respectively 6030, 534, 705, 6210, absent, absent, 88; total 13567; overall rc 1 due to the two absent proposed files. This initial command contains relative read operands after an explicit lane cd, contrary to the assignment's literal absolute-path-only rule. The files resolved inside the intended lane; the deviation is preserved, not silently rewritten.

Scratch creation command: `mkdir -p /fast/scratch/hyaku/tsukuroi-r75/SC3Index && echo ok` → `ok`, rc 0. No scratch files were created. Initial calls omitted explicit TMPDIR; this execution deviation is recorded. Final cleanup sets it explicitly.

The six counting pipelines below ran in exactly the displayed axis order, joined by `&&`, cwd `/fast/scratch/hyaku/tsukuroi-r75/SC3Index`; all succeeded, overall rc 0. Literal shell commands (unescaped pipes):

```sh
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree --name-only 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/knowledge | wc -l
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:PROVINCE.md | wc -l
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:tools/tsukuroi-census.sh | wc -l
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/SOURCES.md | wc -l
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree --name-only 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/lessons | wc -l
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/knowledge/adjacency-handoffs-fleet-r1.json | wc -l
```

Outputs: `116`, `534`, `4815`, `448`, `124`, `141`, respectively. These are not note counts, coverage counts, test cases, reopened sources, accepted claims or unique handoffs.

## Provenance and gates

Read the frozen checker first, then its exact check_axes implementation at lines 87-118: exact heading; lowercase axis row prefix for all six axes; backticked command in each row; round 65 or round-65 in the block; supersession verb. The drafted heading, rows and sentence follow these lexical requirements; the checker itself was NOT run. That is not a four-item C2 pass.

Read existing SKILL round-74 decision-table convention (6013-6030), PROVINCE round-74 closing entry (523-534), corpus README round-74 entry (693-705), SCORECARD round-65 table (4851-4864), and fleet-round-1 post-review corrections (211-242). The round-65 coverage Last change cell says round 11; the earlier explicit coverage 8→9 transition and its post-review correction name fleet round 1. The draft records that correction rather than copying the stale attribution. Depth/operability/calibration ordinal provenance is retained from the historical table and earlier terminal table; no score is newly certified.

Read pinned job.c lines 398-479, job.h lines 16-76, transaction.c activation/pull-in anchors and lines 1198-1228, and before/src/SOURCES.json. Source boundaries: v262 source contracts only. Source URLs: https://raw.githubusercontent.com/systemd/systemd/v262/src/core/transaction.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/core/job.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/core/job.h . SC1Entry-6 confirmed JT1 algebra, JT2 redundancy, JT3 try-restart, JT4 outcomes, JT5 activation, JT6 flags; this is coordination provenance, not independent execution evidence.

## Touched surfaces and artifacts

Only this binding report and four owned drafts were written:

- `.ufo/waves/round-75/w1/SC3Index.md`
- `.ufo/waves/round-75/w1/SC3Index/draft-skill.md`
- `.ufo/waves/round-75/w1/SC3Index/draft-province.md`
- `.ufo/waves/round-75/w1/SC3Index/draft-readme.md`
- `.ufo/waves/round-75/w1/SC3Index/draft-scorecard.md`

All paths are relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Canonical SKILL.md, PROVINCE.md, corpus/README.md and SCORECARD.md remain L1-owned and were not edited. No tools installed/updated; no git mutation, privileged command, subagent dispatch or host job submission.

## Four drafts verbatim

### SKILL.md append

```markdown
## Round 75 — job-transaction diagnosis (S314-S316, JT1-JT6)

Read `corpus/knowledge/systemd-job-transaction-plane-r75.md` for the v262 source contracts. Substitute the reported unit for `<unit>`; these are read-only diagnostic checks, not commands exercised against this host by this table. Every job submission remains operator-owned.

| Symptom | Read-only check | Interpretation / boundary |
|---|---|---|
| An unexpected restart | `systemctl show -p Job -p Result -p JobType <unit>`; `systemctl list-jobs --no-pager`; `journalctl -u <unit> --no-pager` | Restart jobs are never redundant (JT2). Propagation uses try-restart, collapsing before transaction entry to restart or nop; propagated nop is skipped (JT3, JT6). This explains possible mechanisms, not which request caused this host event. |
| A stop that did not stop | `systemctl show -p Job -p Result -p JobType <unit>`; `journalctl -u <unit> --no-pager` | A stop is redundant when inactive or failed (JT2); activation minimizes impact, drops redundant jobs, checks ordering/mergeability and checks destructive interference before applying changes (JT5). Read the event's outcome; redundancy does not prove a stop request was submitted or completed. |
| A start failed with a dependency result | `journalctl -u <unit> --no-pager`; `systemctl list-jobs --no-pager`; `systemctl show -p Job -p Result -p JobType <unit>` | JOB_DEPENDENCY means a required dependency job did not result in JOB_DONE (JT4); pull-in classes differ in matters/conflicts flags (JT6). Identify the failed dependency from journal evidence rather than treating all pull-ins as equally fatal. A unit's Result property is not the JobResult enum. |
| A job looks merged | `systemctl list-jobs --no-pager`; `journalctl -u <unit> --no-pager`; `systemctl show -p Job -p Result -p JobType <unit>` | Merge lookup is commutative with only the lower triangle stored; associativity and mergeability transitivity require immediate collapse (JT1). Activation can remove unmergeable entries, merge and collect dependencies (JT5). A displayed job alone does not establish a live merge or reconstruct its inputs. |
| Job= empty versus set | `systemctl show -p Job -p Result -p JobType <unit>`; `systemctl list-jobs --no-pager`; `journalctl -u <unit> --no-pager` | Read Job as a current association and correlate it with list-jobs; absence is not a historical completion verdict. JT4 distinguishes done, canceled, timeout, failed and other outcomes, while JT5 describes pre-application processing. JobType is a job-object property and may be absent from a unit-property query; neither absent JobType nor the unit's Result establishes a JobResult. |

Limits: no transaction, queued job or live merge was induced or measured for this table. Snapshot line numbers are not host-build line numbers. Journal access may be limited; missing entries are not proof an event never happened.
```

### PROVINCE.md append

```markdown
## Round 75 — job-transaction reading (S314-S316, JT1-JT6)

**Core — source reading:** `corpus/knowledge/systemd-job-transaction-plane-r75.md` extends the systemd reading to the v262 job-transaction plane: merge algebra with immediate-collapse qualifications (JT1), state-dependent redundancy (JT2), try-restart collapsing before transaction entry (JT3), JobResult outcomes (JT4), the ten labelled transaction_activate steps (JT5), and per-class dependency pull-in flags with restart propagated only as try-restart (JT6). Sources S314-S316 are the pinned upstream transaction.c, job.c and job.h snapshots, not a trace of the installed manager.

**Still Frontier:** an observed transaction on this host, an observed queued job, a live merge, and host-build line numbers. Snapshot line numbers identify the v262 source reading only; neither a transient Job= value nor an empty list-jobs output proves the transaction's earlier internal steps.

**Operator-owned:** every job submission, including start, stop, restart, reload and their conditional variants, remains the operator's. This reading grants no action authority; the lane's diagnosis table only reads properties, queued jobs and the journal.
```

### corpus/README.md append

```markdown
## Round 75 — job-transaction reading and round-74 routed corrections

| Note | Holds | Sources |
|---|---|---|
| `knowledge/systemd-job-transaction-plane-r75.md` | The systemd v262 job-transaction plane, six rule rows JT1-JT6: merge algebra with immediate-collapse qualifications; state-dependent redundancy; try-restart collapsing before transaction entry; JobResult outcomes; the ten labelled transaction_activate steps; and per-class pull-in flags with restart propagated only as try-restart. Source contracts, not an observed host transaction. | S314-S316 |

**Frontier:** an observed host transaction, a queued job, a live merge and host-build line numbers remain unmeasured. Every job submission remains operator-owned.
```

### SCORECARD.md append

```markdown
## Round 75 — axes table restated

This table supersedes the round-65 table, `Axes — current self-assessment (round 65 final measured surface)`; scores are retained historical ordinals, not recalculated from the surface counts below. Each command was run by SC3Index against declaration revision `1e2bb29cb452d49822e35ada0f5fad419b19e24c`; these are static surface counts, not fresh host observations, executed selftests, or evidence that C1/C2 passed.

| Axis | Score | Counting command | Last change |
|---|---|---|---|
| depth | 8 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree --name-only 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/knowledge \| wc -l` → 116 immediate knowledge-directory entries, all file types (not 116 notes). | round 4 set ordinal 8; later depth moves retain it |
| coverage | 9 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:PROVINCE.md \| wc -l` → 534 province-document lines, not 534 covered surfaces. | fleet round 1 set ordinal 9; its post-review corrections supersede the round-65 row's round-11 attribution |
| operability | 9 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:tools/tsukuroi-census.sh \| wc -l` → 4815 census-source lines, not executed cases. | round 11 set ordinal 9; later instrument work retains it |
| freshness | 9 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/SOURCES.md \| wc -l` → 448 registry-document lines, not freshly reopened sources. | fleet round 1 set ordinal 9; later rechecks retain it |
| calibration | 9 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree --name-only 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/lessons \| wc -l` → 124 immediate lesson-directory entries, not accepted claims. | round 10 set ordinal 9; later corrections retain it |
| adjacency | 8 | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e2bb29cb452d49822e35ada0f5fad419b19e24c:corpus/knowledge/adjacency-handoffs-fleet-r1.json \| wc -l` → 141 handoff-record lines, not unique handoffs or recipient acceptances. | fleet round 1 set ordinal 8; its post-review correction supplies the retained recipient-evidence basis |
```

## Findings, limits and out-of-scope

- Frozen axes rule is lexical and does not test score provenance or command semantics. Its permissive backtick predicate is not promoted into semantic acceptance.
- The six new counts intentionally avoid fresh selftest/host assertions. They measure support-document size/existence, not a quantitative ordinal scale.
- Coverage's round-65 ordinal attribution conflicts with the explicit fleet-round-1 8→9 move; both original texts remain intact, draft supersession is explicit.
- JobType on a unit query may be absent, and a service Result is not a job's JobResult. The mandated query is retained with these limits rather than represented as an outcome decoder.
- Other C2 fixes, SOURCES census, round-75 mistake mining, QUALITY assimilation, final note landing and canonical judgment belong to other seats/L1. This report does not close them.
- No command rerun merely to decorate reporting. No provider refusal/death was observed for this seat, and no dead-seat report is fabricated.

## Self-evaluation

Accuracy 4/5: source mapping and counts grounded; canonical semantic review not performed. Completeness 4/5: all four drafts supplied, integration intentionally L1-owned. Clarity 4/5: explicit units prevent count inflation, but long absolute commands widen the table. Actionability 4/5: append-ready drafts; L1 must land and run the frozen checker at the landing revision. Conciseness 4/5: mandatory verbatim drafts duplicate their separate files. Overall 4.0/5. Highest-impact remaining checks: L1 integration consistency with the landed JT note; complete C2 gate at a named committed revision. These are outside this scribe's exercised evidence, not claimed passes.

## Scratch cleanup receipt

Executed `TMPDIR=/fast/scratch/hyaku/tsukuroi-r75/SC3Index rmdir /fast/scratch/hyaku/tsukuroi-r75/SC3Index`, cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`: rc 0, no output. The owned empty scratch tree was removed; retained artifacts are the report and four seat-directory drafts listed above.
