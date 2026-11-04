Verdict: read-only host probe complete; observed an idle job surface, not a transaction execution.
Unchecked/unproved: transaction construction, job enqueueing, merging, dependency pull-ins, redundancy elimination, JobResult outcome coverage, and correspondence of installed package bytes to upstream source snapshots.

# E3HostProbe — round 75 w1

## Axes and scope

- Operability: all retained host query commands completed; inactive-unit status intentionally returned 3.
- C1 host-scope accuracy: host systemd major version is 262, but observations do not verify the source-level transaction claims.
- Probe completeness: service/socket/timer properties, per-unit Result, filtered journal, inactive status, and unit-file read retained. No mutating systemctl operation was invoked.

Captures began at 2026-11-04T04:27:10 UTC. Commands used an explicit seat-local TMPDIR. No privileges, installs, source edits, builds, tests, linters, or formatters were used. No environment or credential material was printed.

## Retained receipts

All paths below are relative to the lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`:

| File | Exact retained evidence |
|---|---|
| `.ufo/waves/round-75/w1/E3HostProbe/01-surface.txt` | `systemctl --version`: `systemd 262 (262.1-1-arch)`, rc 0; `systemctl list-jobs --no-pager`: `No jobs running.`, rc 0; requested running-service count pipeline: `21`, rc 0 with pipefail. |
| `.ufo/waves/round-75/w1/E3HostProbe/02-properties.txt` | Seven requested properties queried with `show --all` for each selected unit; exact returned lines and rc 0 for each. |
| `.ufo/waves/round-75/w1/E3HostProbe/03-results.txt` | Separate `systemctl show -p Result` requests: `Result=success` for all three units, rc 0 each. |
| `.ufo/waves/round-75/w1/E3HostProbe/04-journal.txt` | `journalctl -b -u systemd-journald.service --no-pager`, rc 0, empty stderr; zero case-insensitive `job|result` matches. |
| `.ufo/waves/round-75/w1/E3HostProbe/05-failure-reads.txt` | Inactive `fstrim.service` status rc 3 and full unit-file read rc 0. |

The journal output was filtered in memory using case-insensitive `job|result`, retaining its last 20 matching lines, equivalent to the requested grep/tail selection. The recorded rc is journalctl's rc, not an invented grep exit status. Zero matches gives no result vocabulary from this journal sample and does not establish journal completeness or absence of jobs elsewhere.

## Exact property observations

| Property | systemd-journald.service | systemd-journald.socket | systemd-tmpfiles-clean.timer |
|---|---|---|---|
| Id | systemd-journald.service | systemd-journald.socket | systemd-tmpfiles-clean.timer |
| ActiveState | active | active | active |
| SubState | running | running | waiting |
| Job | empty (`Job=`) | empty (`Job=`) | empty (`Job=`) |
| JobType | not emitted | not emitted | not emitted |
| Result | success | success | success |
| NRestarts | 0 | not emitted | not emitted |

Empty Job means no queued job for that unit at the observation instant. Omitted properties are not empty-value observations: neither JobType nor socket/timer NRestarts was emitted, even with `--all`. Do not infer zero values or an enum member from omission. All property queries returned rc 0 and empty stderr.

## Failure-mode reads

`systemctl status fstrim.service --no-pager` reported `Loaded: loaded (/usr/lib/systemd/system/fstrim.service; static)` and `Active: inactive (dead)`, with `TriggeredBy: fstrim.timer`, rc 3, empty stderr. In this observed case, non-zero describes inactive/not-running status; it is not evidence that the read failed, the unit was started, or the unit's latest job failed.

`systemctl cat fstrim.service --no-pager` returned the existing `/usr/lib/systemd/system/fstrim.service` contents, rc 0 and empty stderr. Its displayed ExecStart was merely read, never executed. No non-zero cat result was observed; this receipt does not test missing-file, permission, or masked-unit cases. An inactive existing unit satisfies the requested inactive-or-masked case.

## Host paragraph for C1 / PROVINCE

> On this host, systemctl identified systemd 262 (262.1-1-arch). A read-only sample at 2026-11-04T04:27:10 UTC found no jobs running and counted 21 running services. systemd-journald.service and systemd-journald.socket were active/running; systemd-tmpfiles-clean.timer was active/waiting. All three showed an empty Job and Result=success; only the service emitted NRestarts=0. An inactive fstrim.service status read returned 3, while reading its unit file returned 0. The current-boot journald-unit journal read returned 0 with no case-insensitive job/result matches. These are observational host-surface receipts, not execution evidence for the sourced job-transaction plane: this probe built no transaction, queued no job, and observed no merge. Unit Result=success is not coverage of the JobResult outcome set.

## Non-claims and limitations

No transaction was built by this probe; no job was queued by this probe; no merge was observed. An empty list-jobs sample cannot establish that other actors never queued work before, after, or between reads. Independent queries are not an atomic snapshot. Host major version 262 aligns with the source labels but does not prove package/source identity or execute merging algebra, redundancy predicates, TRY_RESTART handling, activation steps, or pull-in flags. Unit Result properties are distinct from exhaustive observation of job outcomes.

The named C1 note was absent when initially read, so no note content was edited or presumed. The source-note scribe received the exact retained receipt paths and the Unit Result versus JobResult caveat. Initial shell attempts did not execute because their configured scratch cwd did not yet exist; setup was corrected before capturing retained receipts.

## Cleanup and self-evaluation

Raw captures were copied to the exclusive receipt directory before `/fast/scratch/hyaku/tsukuroi-r75/E3HostProbe` was removed successfully. No scratch scripts remain. No LSP-supported symbols were involved; no LSP operation was needed.

Self-evaluation (advisory, not a claim judgment): accuracy 4/5 (source/package identity remains unproved); completeness 4/5 (journal selection uses equivalent in-memory filtering rather than literal grep/tail); clarity 4/5 (raw command detail lives in five linked receipts); actionability 5/5 (quotable host paragraph and exact paths supplied); conciseness 4/5 (non-claims repeat deliberately to prevent source/host conflation). Average 4.2/5. Improvements: retain source/package distinction in downstream prose; cite the property receipt when describing omissions. Expected user assessment: useful bounded evidence, not transaction validation.

Parent-owned checks: inspect receipt links and integrate the host paragraph without promoting it into evidence of source-level JT behavior. No build/test gate is required for these observational report-only artifacts.
