# Round 75 — the systemd job-transaction plane, the four r74 routed repairs, and one over-broad frozen clause

Declaration `1e2bb29cb452d49822e35ada0f5fad419b19e24c`; base
`a21302a48d24cf5242ac2a66cc5b5b453f7a1b20` (round-74 verifier spot-check). Two frozen claims on two
axes: C1 depth (lowest tied, 8) and C2 freshness (9). C2 verifies on committed bytes. C1's six JT
rows are all true and the frozen counter reads `met=1`, but one clause of the frozen C1 sentence —
"propagating restart only as try-restart" — is over-broad against the pinned source, so C1 is
**not verified as declared**; the erratum `R75-DECL-PROPAGATE-SCOPE` below names it. No ordinal
uplift is self-awarded; closure belongs to the outside verifier.

## Gate

All sources opened 2026-11-04. Three upstream v262 snapshots were pinned before the declaration
under `.ufo/waves/round-75/before/src/` with `SHA256SUMS` and `SOURCES.json`
(`sha256sum -c SHA256SUMS` reads 3/3 OK; S1Scout re-fetched all three by a second route and got
identical digests). Host systemd reports 262.1-1-arch; upstream code lines are not claimed as
Arch-patched line numbers (QUALITY 103).

| row | URL | located quote (at most 25 words) | disposition |
|---|---|---|---|
| S314 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/transaction.c | :1203-1204, "We propagate RESTART only as TRY_RESTART, in order not to start dependencies that are not around." | mined, JT5-JT6 |
| S315 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/job.c | :399, "Merging is commutative, so imagine the matrix as symmetric. We store only" | mined, JT1-JT2 |
| S316 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/job.h | :33, "JOB_TRY_RESTART can never appear in a transaction, because" | mined, JT3-JT4 |
| S317 | https://man.archlinux.org/man/systemctl.1 | DESCRIPTION, "systemctl may be used to introspect and control the state of the systemd system and service manager." (saved HTML :72-73) | rejected: CLI surface, not the internal merge, collapse or activation rules; flip: a located passage directly states those internal rules for the pinned release |

S317's refusal is relevance-scoped: the manual does contain one transaction sentence ("enqueued in
a single job transaction", which orders `After=`/`Before=`), and the refusal says plainly that this
is narrower than the plane and cannot ground a merge, collapse or pull-in rule. Registry
313 → 317 rows (3 mined, 1 rejected); knowledge notes 92 → 93. Census start and end both exit 0
with pre-existing W04 duplicate-URL warnings only; receipt `.ufo/waves/round-75/before/census-start.txt`
and the round-end rerun in the report.

## Search log

Question: what are systemd v262's internal job merging, redundancy, transaction-entry, result,
activation and dependency pull-in rules? Searched the three pinned snapshots by the symbols
`job_type_lookup_merge`, `job_merging_table`, `job_type_is_redundant`, `job_type_collapse`,
`transaction_activate`, `transaction_add_job_and_dependencies`, `PULL_IN_*`, `matters_to_anchor`,
`JobType`, `JobResult`, then read each located range in full. Screened five candidates (the three
mined files, the systemctl(1) manual, and the meant-but-404 `src/core/unit-load.c` shape carried
from round 74): included three, rejected one, and did not re-screen the round-74 refusal.
Stop: the three snapshots ground every rule row; the manual adds only the CLI surface.

Assimilation: **none**. The `corpus-expansion-1` package `merge/tsukuroi/` was checked read-only
this round and 114 of its 147 staged S-ids collide with the current registry
(`.ufo/waves/round-75/assimilation/{reg-ids,staged-ids,collisions}`), which is the mass-id-drift
case the contract routes to an L0 question instead of an append; the question is filed
(`tsukuroi | round-75`). `considerthese/2026-10-26.md` was opened and its "Cross-note correction
propagation map" proposal is adopted as QUALITY 108 and exercised below; the counter-attack
scoreboard and downstream patch-offset check were already adopted at rounds 64 and 69 and are not
relabelled.

## Mistakes

- **R75-DECL-PROPAGATE-SCOPE** · evidence R1Reviewer M-1 and `transaction.c:999-1027,1199-1247` ·
  captured-by QUALITY 106 (enum/set read from the pinned definition before freezing) — missed
  because this is a scope word, not a set member: the frozen sentence says restart propagates
  "only as try-restart", which is the source comment's own sentence for the `PROPAGATE_STOP`
  branch, while the later `PROPAGATE_STOP_GRACEFUL` branch may enqueue a direct `JOB_RESTART` when
  a `JOB_START` is already in the transaction. · fix: JT6 states both branches; the erratum
  `R75-DECL-PROPAGATE-SCOPE` is appended to `SCORECARD.md`; C1 is reported not verified as
  declared. Able to fail: R1Reviewer's per-row verdict rejects the unqualified sentence while it
  holds the branch-scoped one, and re-running the same review on the landed JT6 entails it.
- **R75-QUOTE-LEADER** · evidence the six row quotes scored pre-data in
  `before/draft-row-control.txt` · captured-by the frozen counter, before data · fix: three draft
  quotes crossed a comment line and the whitespace normalization kept the `*` leader, so they were
  not located; each was replaced with a single-line located quote. Able to fail: the three original
  quotes each produced `quote not located in snapshot` and the replacements score 6/6.
- **R75-C2-LINEBREAK** · evidence `ROUTED_STALE=1` on the first landed wording of the
  `R74-REPORT-WORDING` block · captured-by nothing (found by running the gate) · fix: the required
  phrase is landed on one unbroken line. A writer's correctly-worded but wrapped correction reads
  stale; the instrument cannot tell a wrapped phrase from a missing one. Recorded as a named limit.
- **R75-COUNTER-NONREADER** · evidence E1Counter's scripted non-reader, which fetched the pinned
  sources and passed the full predicate · captured-by QUALITY 81's control requirement · fix:
  reported as a named limit; C1's truth rests on R1Reviewer's per-row entailment, never on the
  counter. Able to fail: the scripted writer passes the counter while its statements are
  mechanically assembled from source words.
- **R75-WAVE-SIZE** (process) · evidence wave `w1` results · the wave ran twelve seats and
  `m_zfl`-routed reviewer seats were not distinguishable from `m_flash` seats in the results file,
  so no route claim is made. No seat was replaced and no seat was killed for cause.

## Attack ledger / verdict limits

- **E1Counter**: initial `--selftest` 13/13 rc 0; base `JT_MAP absent` rc 128; mirror `6/6 met=1`;
  scripted non-reader passes (above). 27 attacker cases named in its report.
- **R1Reviewer**: JT1 holds, JT2 holds, JT3 holds, JT4 partly, JT5 holds, JT6 partly; independent
  counts of the ten step comments and the thirteen `JobResult` members; JT4 and JT6 refused
  unchanged and their corrected sentences are the landed rows.
- **R2Reviewer**: eleven fixtures pass all four C2 predicates without a genuine repair — the axes
  rule accepts any backticked string (its `banana` fixture reads `ROUTED_OK=4/4`), and a token dump
  satisfies the lesson items. Named limit: C2's four items are evidence-persistence checks, not
  repair proofs.
- **K1Critic**: declaration critique; its findings are carried in the round report and, where they
  name a limit, in this ledger.
- **M1Mutation**: clause-isolated batteries — C1 7 mutants built, 3 killed, 4 survived; C2 5 built,
  2 killed, 3 survived. Survivors are instrument-coverage gaps, not claim failures.
- **S1Scout**: sources 3/3 on a second route, quotes 6/6 located, five anchor ranges are
  substrings of a function rather than full extents, one host reading transiently differed.
- **C1Connector**: no sibling lane holds the job-transaction ground (20 sibling repos scanned,
  tracked tree); no held-corpus restatement at the declaration revision.

## Correction propagation map

Produced by the QUALITY 108 sweep at `1e2bb29c`
(`.ufo/waves/round-75/before/propagation-map.txt`); each carrier is marked with what this round did
to it. Three corrected propositions, three carrier sets:

**1. The r74 false alias set ("volume").** `SCORECARD.md:6092` (declaration) — standing as the
falsified record; `:6102` (erratum) and `:6139` (measured outcome) — the correction itself;
`SKILL.md` round-74 decision table — already states the true timer/path set and names the error;
`PROVINCE.md:529` — states the error is not admitted; `corpus/knowledge/systemd-unit-fragment-plane-r74.md:13,32`
— the true set; `corpus/lessons/round-74.md:5,50` — the honest-stop record. No file still asserts
the false set as current.

**2. The fabricated full base OID `d749a625f483c6…`.** `corpus/lessons/round-74-verifier-spotcheck.md:173`
— the closure's own record; `SCORECARD.md:6050` (declaration) and `:6107` (erratum) — the
declaration keeps the error, the erratum names it; `.ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt:4`
— corrected this round by `R74-SWEEP-RESIDUE`; `.ufo/waves/round-74/{w1-spec.json,w1-dispatch.json}`
and the round-74 seat reports — historical evidence, left standing because they are frozen
artifacts of that round, and this map is the pointer that says so.

**3. The superseded r73 selftest counts (12 / 11).** `LOG.md:3207,3209` — the original entry;
`:3224-3225` — the unheaded correction naming the final 13/14; `SCORECARD.md:5886,5940` — the
instrument record; `corpus/lessons/round-73-verifier-spotcheck.md:62,165` — the outside check. No
carrier still presents 12/11 as current.

## Owed to the next round

- K1Critic's and R2Reviewer's named limits on C2 (token dumps, `banana` commands) are instrument
  gaps; a future round that revises the checker must re-run the before control with the final bytes
  (the frozen instrument-change rule).
- The `corpus-expansion-1` id drift awaits the L0 answer.
- R1Reviewer's note that five `S314`-`S316` anchor ranges are substrings of functions rather than
  full extents is worth a future anchor widening; the rows' quotes and statements are unaffected.
