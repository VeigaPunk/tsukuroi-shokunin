Verdict so far: READY FOR L1 APPEND — four exact 11-column registry rows and Gate material drafted below from inspected sources; S317 refusal measured HTTP 200, 141009 bytes.
Still unchecked: L1 landing, frozen C1/C2 counters, canonical judgment. This seat makes no execution or committed-byte claim.

## Behavior and scope

Axes: depth, C1, registry. Read S309–S313 before drafting and retained their 11-column registry convention. This seat writes only its report and refusal receipt; L1 owns corpus/SOURCES.md. Included the three pinned v262 implementation sources; rejected one opened tier-A CLI manual for this internal-rule question.

## Exact registry rows

Append these rows without the code fence. No cell contains a pipe.

```text
| S314 | systemd v262 src/core/transaction.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/core/transaction.c | code | A | Transaction activation stages and dependency-class pull-in flags (JT5-JT6) | transaction.c at v262, lines 800-881 (transaction_activate) and 1143-1217 (pull-in classes and restart propagation); sha256 c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3 | Ten labelled activation steps; required start and verify use MATTERS, required stop adds CONFLICTS, ignored classes omit those flags; restart propagates only as try-restart | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-job-transaction-plane-r75.md |
| S315 | systemd v262 src/core/job.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/core/job.c | code | A | Job merging algebra and state-dependent redundancy (JT1-JT2) | job.c at v262, lines 398-440 (merging algebra and lower-triangle lookup) and 443-480 (job_type_is_redundant); sha256 024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897 | Merge is commutative; immediate collapse gives associativity and mergeability transitivity; start/verify-active redundant when active-or-reloading, stop when inactive-or-failed, reload/restart never, nop always | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-job-transaction-plane-r75.md |
| S316 | systemd v262 src/core/job.h — https://raw.githubusercontent.com/systemd/systemd/v262/src/core/job.h | code | A | Transaction job-type boundary and JobResult outcomes (JT3-JT4) | job.h at v262, lines 33-36 (JOB_TRY_RESTART exclusion) and 60-76 (JobResult); sha256 22d7b942426402ddba376c7b713bc9937c2eaa9f5817e8735dec8d5b6cf57c3a | JOB_TRY_RESTART collapses to JOB_RESTART or JOB_NOP before entering a transaction; JobResult lists DONE, CANCELED, TIMEOUT, FAILED, DEPENDENCY, SKIPPED, INVALID, ASSERT, UNSUPPORTED, COLLECTED, ONCE, FROZEN and CONCURRENCY | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-job-transaction-plane-r75.md |
| S317 | Arch Linux systemctl(1) manual — https://man.archlinux.org/man/systemctl.1 | docs | A | Screened for internal job merging and transaction rules | Accessed 2026-11-04; HTTP 200, 141009 bytes; NAME and DESCRIPTION, saved HTML lines 63-75; sha256 406c79cf7bf77a6607af8203af76e7bfffd273a79fe7c4d9aab5265e884fa307 | REJECTED: documents the systemctl CLI surface, not the internal merge algebra or transaction activation rules; flip: a located passage directly specifies those internal rules for the pinned release | rejected | 2026-11-04 | on-release | — |
```

## Gate — exact table

Quotes are at most 25 words each. Access means inspection of the supplied pinned snapshot for S314–S316, not a fresh upstream fetch. S317 was fetched live once.

| id | URL | access date | located quote | disposition |
| --- | --- | --- | --- | --- |
| S314 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/transaction.c | 2026-11-04 | transaction.c:1203-1204: “We propagate RESTART only as TRY_RESTART, in order not to start dependencies that are not around.” | included: internal dependency propagation; activation steps at 822-879 and pull-in flags at 1143-1217 |
| S315 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/job.c | 2026-11-04 | job.c:399-400: “Merging is commutative, so imagine the matrix as symmetric. We store only its lower triangle to avoid duplication.” | included: merge algebra and redundancy; immediate-collapse qualification at 403-411 |
| S316 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/job.h | 2026-11-04 | job.h:33-34: “JOB_TRY_RESTART can never appear in a transaction, because it always collapses into JOB_RESTART or JOB_NOP before entering.” | included: transaction type boundary and JobResult enum |
| S317 | https://man.archlinux.org/man/systemctl.1 | 2026-11-04 | DESCRIPTION, saved HTML:72-73: “systemctl may be used to introspect and control the state of the "systemd" system and service manager.” | rejected for this question: CLI surface rather than internal merge/transaction rules; flip on a located pinned-release passage directly specifying those rules |

## Search log — exact paragraph

Question: what are systemd v262's internal job merging, redundancy, transaction-entry, result, activation and dependency pull-in rules? Searched the supplied round-75 pinned src/transaction.c, src/job.c and src/job.h snapshots by transaction_activate, JOB_TRY_RESTART, commutative, associative, transitive, redundant, JobResult and pull-in symbols, then read the located ranges. Screened and included S314–S316 because they directly define the six JT rule groups, with tag, source URLs and digests supplied by before/src/SOURCES.json. Opened https://man.archlinux.org/man/systemctl.1 as one tier-A candidate; its HTTP 200 response measured 141009 bytes and its DESCRIPTION says systemctl controls/introspects the manager. Rejected S317 as evidence for this internal plane: a CLI guide does not ground the selected implementation rules; reconsider only if a located passage directly specifies those rules for the pinned release. Stopped because all six requested rule groups had direct implementation anchors and one honest alternative-source refusal had been measured; no broader source-exhaustiveness claim.

## Provenance and commands

Pinned provenance read from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-75/before/src/SOURCES.json`: transaction.c 57987 bytes; job.c 63346 bytes; job.h 7851 bytes. Digests in registry rows are transcribed from that manifest, not independently rehashed by this seat. Local source ranges were read directly using the read/grep tools.

Commands executed (working directory scratch except initial mkdir):

```sh
mkdir -p /fast/scratch/hyaku/tsukuroi-r75/SC2Sources
TMPDIR=/fast/scratch/hyaku/tsukuroi-r75/SC2Sources curl --location --silent --show-error --output /fast/scratch/hyaku/tsukuroi-r75/SC2Sources/systemctl.1.html --write-out 'http_status=%{http_code}\nbytes=%{size_download}\neffective_url=%{url_effective}\n' https://man.archlinux.org/man/systemctl.1
sha256sum /fast/scratch/hyaku/tsukuroi-r75/SC2Sources/systemctl.1.html
mkdir -p /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-75/w1/SC2Sources && cp /fast/scratch/hyaku/tsukuroi-r75/SC2Sources/systemctl.1.html /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-75/w1/SC2Sources/systemctl.1.html
```

Observed curl outcome: exit 0; `http_status=200`, `bytes=141009`, `effective_url=https://man.archlinux.org/man/systemctl.1`. sha256sum exit 0 yielded the S317 digest above. No tool install/update.

## Touched surfaces, findings and limits

- Report: `.ufo/waves/round-75/w1/SC2Sources.md`.
- Preserved raw refusal receipt: `.ufo/waves/round-75/w1/SC2Sources/systemctl.1.html`.
- No corpus registry, knowledge entry, product code, checker, commit, push or deployment modified/executed by this seat.
- No frozen counter, selftest or canonical judge run. L1 must land the rows and run its assigned gates; the declaration's target outcomes are not this seat's observed outcomes.
- S317 refusal is relevance-scoped, not a claim that the manual contains no transaction discussion anywhere. No version-equivalence claim for the live manual.
- No conflict discovered in the inspected source passages. Cross-seat execution and committed landing remain outside this evidence.

## Self-evaluation

Accuracy 4/5: quotes and ranges inspected, but pinned digests are manifest provenance rather than independent hash measurements. Completeness 5/5: four exact rows, four Gate quotes, measured refusal, flip condition and search paragraph supplied. Clarity 4/5: separate evidence and landing limits, with long registry lines required for byte-for-byte use. Actionability 5/5: rows and Gate ready to copy. Conciseness 4/5: command/provenance detail retained for audit. Overall 4.4/5. Highest-value improvement belongs to L1's assigned landing/counter gates, not a rerun by this scribe. Self-check: the report explicitly separates a completed draft from unobserved integration.

## Receipt preservation and cleanup outcomes

The mkdir/cp receipt-preservation command completed with exit 0. Final cleanup command `rm -r /fast/scratch/hyaku/tsukuroi-r75/SC2Sources` completed with exit 0; the owned scratch tree was removed after receipt preservation. The durable raw HTML receipt remains at the path listed above.
