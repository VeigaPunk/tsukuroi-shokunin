# Round 80 — service restart matrix and gate self-invocation

Base `467a9b7891a5939dab8460ec6f591fbb16bd82e9`; freeze
`61ec89ec6e6f284b6fba2127721359e6931a5789`; validated dispatch
`aad05ef173176cf5223f7c315297240c2db1abe2`. C1 works depth8 (tied lowest);
C2 works operability9. Ordinals are not arbitrarily raised. The original
predicates and targets remain frozen; a missed conjunct cannot be repaired
by changing the counter after data. Source/semantic truth is separate from
finite equality and byte-binding. No promotion or capability is claimed.

## Gate

Opened live by L1 on 2026-11-04 and independently re-fetched by ScoutSource:
https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml .
Raw snapshot `.ufo/waves/round-80/before/systemd.service.xml`, SHA256
`12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44`.
Table title :914: `Exit causes and the effect of the Restart= settings`
(9 words, XML tags stripped). Complete raw rows :932-991 independently agree
on all42 cells. The admitted companion preserves complete XML rows instead
of the draft's partial-line quotations. Access date for each row below is
2026-11-04; every quote is from that same pinned URL after XML tag stripping.

| Candidate | Located quote (at most25 words) | Decision, reason and flip |
|---|---|---|
| S330, A/docs/mined | :877-878: `Configures whether the service shall be restarted when the service process exits, is killed, or a timeout is reached.` | admit documentation matrix only; stop, oneshot, clean-status, main-process override and rate-limit exceptions remain visible; no installed-build equivalence |
| always restarts after an operator stop | :999-1000: `the service is stopped with systemctl stop or an equivalent operation.` | reject: explicit stop is an exception, not an unqualified always policy; flip: version-pinned passage explicitly allowing automatic restart after that stop |
| always is accepted for oneshot | :910-911: `always and on-success are rejected for them.` | reject: those policies are rejected for oneshot, not merely inert; flip: version-pinned source permits them |
| on-watchdog covers unclean exit code | :906-907: `the service will be restarted only if the watchdog timeout for the service expires.` | reject: the unclean-exit-code row has an empty on-watchdog cell; flip: located source expands it to exit codes |
| prevent-exit list applies to helper processes | :1126-1128: `this setting has no effect on processes configured via ExecStartPre=, ExecStartPost=, ExecStop=, ExecStopPost= or ExecReload=,` | reject: the option applies to the main process only; flip: located source includes those helpers |

S330 is the next unused lane id. New rows by tier: A+1/B+0/C+0. No existing
status/recheck/used-by changes (old→new: none). Prior rejected rows and prior
rejected rounds are preserved. Outside admit/reject spot-check: pending;
ReviewMatrix is author-side, not the outside closure.

Assimilation: none. The operator-held staged package is not adopted. Its
S330 names an own-work mirror-language capture, not this document; the bare
id collision stays documented, with no arithmetic renumbering or source-repo
write (`w1/ConnectorScope/boundary-scan.json`, ScribeFrontier source-row draft).
Connector's statement that four latest reflection proposals remain unimplemented
is not adopted: QUALITY103/108 and SKILL counter-attack scoreboard already
implement several. Only the still-unimplemented burst-aware-reading proposal
is mined this round: read recent LOG and outside closure first, then investigate
disagreements. The r79 closure's extra null-output leg motivated file binding;
the frozen r79 predicate and rejection are not retroactively repaired.

## Mistakes

| Class / id | Evidence | Captured-by | Fix shown able to fail |
|---|---|---|---|
| reference-drift R80-C2-REGISTRY-NAME | `after/l1-static-findings.json`; current registry name transaction-order-r39 vs frozen counter's check-transaction-order-r39 | QUALITY102/104; new111 | Keep the true row name and the frozen counter. Actual after measurement must report the missing second row even though both selftests work. Synthetic positives used the counter's invented name; this is not actual-input positive coverage. No duplicate row or rename to game the metric. |
| vacuous R79-RESULT-NULL | r79 outside spot-check routed1/2; round80 before controls answer-copy-without-review | QUALITY93/96 | Counter now binds a seat-written verdict file; absent-review control fails rc1 despite complete matrix. Null result outputs cannot supply the missing review. Both r79 failing legs (DP6 and null output) stay named. |
| source-entailment R80-DRAFT-COLUMNS | `w1/ReviewMatrix/review-8a99e339.json` and ReviewMatrix report | QUALITY66/94 | Reviewer rejected draft OOM/unclean-code equivalence and one-difference assertion; source shows on-abnormal/on-abort differ in Timeout, Watchdog and OOM. Corrected final table keeps all three differences; prior failing review retained. |
| scope R80-KR-ENV | `w1/ReviewMatrix.md` initial and final KR sections | QUALITY28/31 | Initial copy inherited ambient Git controls, then PATH; final copy uses fixed allowlist and pinned PATH. Green and red receipts renewed at final digest908592d2…; no unsupported filesystem-confinement claim retained. |
| vacuous R80-INSTRUMENT-SELFTEST | `after/l1-static-findings.json` | gate-standard self-invocation clause | New instrument's own helper-only absent-reader selftest is disclosed as conformance debt, not certified as full self-invocation. Two repaired old tools instead invoke their actual public CLI and have red-before mutated controls. |
| provider R80-ATTACK-SEATS | `after/settlement.json`; Main's observed provider record | none; operator routing | CriticCounter-2 and MutationCounter-3 died on 402 insufficient funds before deliverables. Dead seats are not replaced, their absent attacks receive no credit. Routing fixed later by orchestrator fleet commit f7de7779, not by this lane. |
| scope R80-SCOUT-EXTRA | `w1/ScoutSource.md` Scope | QUALITY24/31 | Scout fetched additional versions/API/code and read installed man data beyond its explicitly assigned pinned URL. Extra model/implementation/source results are supplemental, not authorized evidence or installed-build equivalence; deviation remains recorded. |

## Seat harm

| Round | Harmed seat | Causing seat | Evidence class | Effect | Fix |
|---|---|---|---|---|---|
|80|—|—|eight delivered seat reports plus WAVE-DONE and after/settlement.json|entries: none observed; no attributable cross-seat kill or escaped write reported|none required; provider deaths have no identified causing sibling|

Review-driven amendments are not seat harm. Final companion was rewritten by
L1 for provenance/complete-line compliance, then returned to the same reviewer
for renewed byte binding. Old draft bindings are retained, not reused.

## Domain task

`w1/ExecHost/handoff.md`: four authorized read-only commands, all rc0.
System failed units0, user failed scopes2; journald Restart=always and
manager Result=success, NRestarts0; dbus alias resolves to dbus-broker with
Restart=no, Result=success, NRestarts0. Both report start burst5/interval10s.
These are captures, not current universal state or historical reliability.
Scopes are not services; no historical cause or future restart is inferred.
No unit start/stop/restart, package transaction, sudo, configuration or secret
read was performed by the domain-task seat. Operator boundary remains intact.

## Wave settlement

WAVE-DONE received before this lesson integration/report. One v1 wave10;
roles executor3/scribe2/scout1/connector1/reviewer1/critic1/mutation-tester1.
Attack allocation3/10; delivered reviewer1, dead attack seats2. L1 held planner
before dispatch (validator forbids planner). Residual0. Eight durable seat
reports; two dead seats with exact error in after/settlement.json. Results
carry ten null outputs after orchestrator kernel restart; no output or vote
was reconstructed. Binding files, not outputs, are used by this round.

## QUALITY check

Applicable1/2/3/5/7/8/14/19/21/23/66/93/94/96/103: finite source scope,
explicit admits/rejects and flips, typed evidence/unknowns, durable files,
complete raw row excerpts and final byte-bound review. QUALITY102/104 failed
for the C2 actual-row-name premise; that miss is retained. QUALITY99: no old
lesson or rejection was rewritten; current registry interface updates are
explicitly superseding old none cells, not historical retroactive executions.
No capability/frontier promotion or arbitrary score uplift. Final numeric
outcomes and actual commands are recorded in SCORECARD and after receipts.
