# Round 76 — the journald retention plane, six round-75 repairs and one host-config drift

Declaration `d5f0565bfb42a405ec024d8a5b0796514fb92002`; base
`865b38c96c23ec0bcace8ca3ee884f860693ce43` (round-75 verifier spot-check). Two frozen claims on two
axes: C1 depth (lowest tied, 8) and C2 freshness (9). C1 lands eight JD rows on ground the lane never
held and derives this host's effective limit; C2 closes the six round-75 routed defects and corrects
three stale journald negative claims. No ordinal uplift is self-awarded; closure belongs to the
outside verifier.

## Gate

All sources opened 2026-11-04. Four upstream v262 snapshots were pinned before the declaration under
`.ufo/waves/round-76/before/src/` with `SHA256SUMS` and `SOURCES.json`
(`sha256sum -c SHA256SUMS` reads 4/4 OK; S1Scout re-fetched all four by a second route and got
identical digests). Host systemd reports 262.1-1-arch; upstream code lines are not claimed as
Arch-patched line numbers (QUALITY 103).

| row | URL | located quote (at most 25 words) | disposition |
|---|---|---|---|
| S318 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journald.conf.xml | :274-285, "The first pair defaults to 10% and the second to 15% of the size of the respective file system" | mined, JD1/JD2/JD5/JD6 |
| S319 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-config.c | :24-27, "#define DEFAULT_RATE_LIMIT_INTERVAL (30*USEC_PER_SEC) #define DEFAULT_RATE_LIMIT_BURST 10000" | mined, JD7 |
| S320 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c | :170, "space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use);" | mined, JD3/JD4 |
| S321 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | :954-956, "removes the oldest archived journal files until the disk space they use falls below the specified size" | mined, JD8 |

Registry 317 → 322 rows (S318–S321 mined, S322 the S314 supersede); knowledge notes 93 → 94. Census
start and end both exit 0 with pre-existing W04 duplicate-URL warnings only; receipts
`.ufo/waves/round-76/before/census-start.txt` and the round-end rerun in the report.

## Search log

Question: what are systemd v262's journald storage-mode, size-cap, rotation, rate-limit and vacuum
rules, and what is this host's effective limit? Searched the four pinned snapshots by the symbols
`Storage`, `SystemMaxUse`, `SystemKeepFree`, `SystemMaxFileSize`, `SystemMaxFiles`, `RuntimeMax*`,
`RateLimitIntervalSec`, `RateLimitBurst`, `SyncIntervalSec`, `MaxFileSec`, `MaxRetentionSec`,
`vacuum-size`, `disk-usage`, then read each located range in full. Screened four candidates
(the four snapshots); included four, rejected none this round. The host read
`systemd-analyze cat-config systemd/journald.conf` added the `/etc/systemd/journald.conf.d/size.conf`
drop-in that the held notes did not know about. Stop: the four snapshots ground every rule row and
the host receipt grounds the effective-limit derivation.

Assimilation: **none**. The `corpus-expansion-1` package `merge/tsukuroi/` stays read-only and
quarantined under the open `tsukuroi | round-75` L0 id-drift question (114 of 147 staged S-ids
collide with the registry); nothing is adopted. `considerthese/2026-10-26.md` was opened: its
counter-attack scoreboard, seat-harm tally, downstream patch-offset check and cross-note propagation
map are already adopted at rounds 41/66/69/75, so no proposal is still unimplemented.

## Mistakes

- **R76-JD-CONFIG-DRIFT** · evidence `corpus/knowledge/degraded-triage-r4.md:70` ("no retention
  policy configured anywhere (merged coredump/journald conf = defaults only)") and
  `/etc/systemd/journald.conf.d/size.conf`, born 2026-10-16 11:53:47 -03, setting
  `SystemMaxUse=256M` · captured-by `none` — the corpus rule required a sweep at write time, not a
  recheck cadence, so a negative host claim written before the drop-in existed stayed false for
  ~70 rounds · fix: QUALITY 109 (a negative host-state claim names its recheck command and cadence,
  and the round-start host probe re-runs it) plus appended errata on the three carriers
  (`journal-boot-plane.md`, `degraded-triage-r4.md`, `boot-plane.md`). Able to fail: the round-76
  host probe re-ran `systemd-analyze cat-config systemd/journald.conf` and found the drop-in, while
  the held notes still said defaults-only.
- **R76-R75-RESIDUE** · evidence the round-75 closure's six routed items · captured-by the closure's
  own section 7 · fix: the six repairs below, checked by `tools/check-r75-routed-r76.py`. Able to
  fail: the checker reads `ROUTED_STALE=8 ROUTED_OK=0/8` at the base.

## Round-75 routed repairs (C2)

- **R76-S314-SUPERSEDE** — the registry's new **S322** row supersedes S314: restart propagation
  "only as try-restart" holds for the `PROPAGATE_STOP` branch (`transaction.c:1203-1204`), while the
  graceful branch may enqueue a direct `JOB_RESTART` when a `JOB_START` is already in the transaction
  (`:1019`). The round-75 note's JT6 row already states both branches; S322 is the registry-level
  correction the closure asked for.
- **R76-JT5-COUNT** — `corpus/knowledge/systemd-job-transaction-plane-r75.md` now carries the
  round-76 erratum: the JT5 row has **eight comma-separated items** and **ten labels** after the
  split method, not "nine comma items".
- **R76-R75-MISTAKE-COUNT** — the round-75 lesson's `## Mistakes` section has **five** rows
  (`R75-DECL-PROPAGATE-SCOPE`, `R75-QUOTE-LEADER`, `R75-C2-LINEBREAK`, `R75-COUNTER-NONREADER`,
  `R75-WAVE-SIZE`) plus **two owed** rows in `## Owed to the next round` (`R75-JT2-REFRESH`,
  `R75-JT5-ENUM`); the round-75 report's "six mined mistakes" figure was wrong. Counting command:
  `awk '/^## Mistakes$/{f=1;next} /^## /{f=0} f && /^- \*\*R75-/' corpus/lessons/round-75.md | wc -l`
  → 5.
- **R76-R75-RECEIPT-REPOINT** — both round-75 instruments were re-run at the round-75 final
  measurement revision **bd0acc44**, not at the receipt head **e5f5ca9e**:
  `.ufo/waves/round-76/before/recheck-r75-at-tip.txt` reads `JT_ROWS=6 JT_VERIFIED=6 … met=1` rc 0
  and `ROUTED_STALE=0 ROUTED_OK=4/4` rc 0 at `bd0acc44`. The earlier receipt's head is named as the
  superseded pointer.
- **R76-WAVE-MARKERS** — the seven carried wave markers are now tracked in the lane
  (`.ufo/waves/round-66/w1.ready.dispatched`, `round-67/w1.ready.dispatched`,
  `round-73/w1-run.stderr`, `round-73/w1.ready.dispatched`, `round-74/w1.ready.dispatched`,
  `round-75/w1.ready`, `round-75/w1.ready.dispatched`); they are runtime bookkeeping, committed as
  wave evidence so the worktree is clean.
- **R76-QUALITY-WORDING** — the narrowed sentence stands: **no admitted knowledge entry is left failing its own re-check**. The round-75 report's "no admitted artifact" wording was over-broad
  because the S314 `teaches` cell and the JT5 count were defects in admitted artifacts; both are now
  corrected append-only (S322 and the JT5 erratum), so the narrowed claim is true for the entries.

## Correction propagation map (round-76)

Produced by the QUALITY 108 sweep at `d5f0565b` and re-run at the measured revision; each carrier is
marked with what this round did to it.

**1. The journald "defaults-only / no retention policy" proposition.**
`corpus/knowledge/journal-boot-plane.md:51,362` — `corrected` (round-76 erratum appended);
`corpus/knowledge/degraded-triage-r4.md:70` — `corrected` (round-76 correction appended);
`corpus/knowledge/boot-plane.md:79,240` — `corrected` (round-76 erratum appended);
`corpus/README.md` — the r3/r4 index rows are `historical evidence` (they describe the capture, not
the current config); `SKILL.md` — no carrier of the claim (swept, 0 hits outside the coredump
`Storage=none` row).

**2. The S314 "restart only as try-restart" proposition.**
`corpus/SOURCES.md:325` (S314) — `standing as falsified record` (the row keeps its over-broad
`teaches`, superseded by S322 at `:333`); `corpus/knowledge/systemd-job-transaction-plane-r75.md:65`
(JT6) — `corrected` (states both branches); `corpus/lessons/round-75.md:55` and
`round-75-verifier-spotcheck.md` — `historical evidence`; `SCORECARD.md` round-75 erratum —
`corrected`.

**3. The JT5 "nine comma items" count.**
`corpus/knowledge/systemd-job-transaction-plane-r75.md:97` — `standing as falsified record` (the
round-75 erratum keeps its sentence), corrected by the appended round-76 erratum at `:107`;
`corpus/lessons/round-75-verifier-spotcheck.md:151,168` — `historical evidence`.

## Attack ledger / verdict limits

- **R1Reviewer**: per-row verdicts (HOLD/PARTLY/FAIL) against the pinned snapshots; the truth leg.
- **R2Reviewer**: C2 checker attacks; pass-without-repair fixtures are named limits.
- **K1Critic**: declaration critique; over-broad conjuncts named before landing.
- **M1Mutation**: clause-isolated batteries; survivors are instrument-coverage debt.
- **S1Scout**: second-route digests and quote locations.
- **C1Connector**: sibling-overlap scan for the journald retention ground.

The wave's reports are the source for these rows; this section is filled from them at integration and
the final figures are in the report.

## Owed to the next round

- The C1 counter is a form instrument: grounding is lexical, so row truth rests on R1Reviewer's
  verdicts and the closure judge, never on the counter alone.
- The C2 checker is a token/block checker: R2Reviewer's pass-without-repair fixtures are named limits.
- `corpus/knowledge/modprobe-config-plane-r72.md` and `corpus/knowledge/module-parameter-plane-r71.md` still carry a
  non-ISO `verified-at:` line (2 pre-existing header findings); `check-adjacency-anchors.py` still
  reports one open classification finding at `adjacency-anchors-r19.json:inbound[108]`.

## Wave attack results (appended 2026-11-04, after WAVE-DONE)

- **R1Reviewer**: final-note re-review at `b698d13d` — JD1–JD8 all HOLD; host/limits HOLD as an
  explicitly qualified configuration derivation, not a live `min_use` measurement
  (`w1/R1Reviewer/verdicts-final.md`, `rows-final.tsv`). Its first pass on the pre-correction note
  returned JD3 FAIL and JD7 PARTLY; E3Note's correction and the declaration erratum
  `R76-DECL-SPACE-CLAUSE` close both.
- **S1Scout**: 4/4 second-route digests match; 8/8 draft quotes located; two draft rows PARTLY
  (JD3 arithmetic, JD7 attribution) and one registry anchor PARTLY — S318 named MaxFileSec and
  MaxRetentionSec outside its ranges; corrected by S323.
- **K1Critic**: HIGH JD3 arithmetic (corrected), HIGH C2 propagation-map/count omission (the map and
  the counting command are present in this lesson; the critic read the pre-correction tree), MEDIUM
  "usually" dropped in the declaration (the JD5 row keeps it; the declaration erratum records the
  sentence), MEDIUM host limit is conditional (the note says so), token-only C2 (named limit).
- **R2Reviewer**: a minimal non-repair fixture passes `ROUTED_STALE=0 ROUTED_OK=8/8` — the checker is
  a text instrument; eight named limits (`w1/R2Reviewer/attacks.md`).
- **M1Mutation**: structural mutants killed 8/8 JD and 8/8 closure; 3 semantic survivors (JD numeric
  truth 100→101, receipt negation retaining success literals, criterion-109 obligation negation
  retaining keywords) are coverage debt (`w1/M1Mutation/report.md`).
- **E4InstrumentCheck**: digests match the declaration; selftests 14/14 and 10/10; base controls
  128 and 8/0 rc 1; working-tree predicates pass; a host-block deletion on a copy fails with
  `JD_HOST=0` (`w1/E4InstrumentCheck/report.md`).
- **C1Connector**: 20 sibling trees swept; mori's `journal-reach-r49.md` and mado's
  `SafetyService.md:73-74` hold overlapping journald statements; the boundary is reported, not
  absorbed (`w1/C1Connector/report.md`).
- **E5MarkerAudit**: the seven carried markers are regular, untracked at base, bookkeeping-only
  (`w1/E5MarkerAudit/markers.txt`).
- **S4Drift**: the three errata and criterion 109 were already present in the tree; its
  qualification notes are adopted (coredump scope, historical date).
- **S2Skill**: the decision table landed in `SKILL.md` as "Round 76 — journald retention diagnosis".
- **E2HostProbe**: derived the same 256M/32M result from the measured inputs and named the `LESS_BY`
  correction (`w1/E2HostProbe/03-derivation.txt`).

## Mistakes — round-76 additions (append-only)

- **R76-REGISTRY-ANCHOR** · evidence S318's anchor cell names MaxFileSec/MaxRetentionSec inside the
  range 243-320, while `grep -n 'MaxFileSec' journald.conf.xml` reads 321 · captured-by the counter's
  anchor-basename check, which does not read the range contents — S1Scout caught it · fix: S323
  supersedes S318 with corrected ranges. Able to fail: the grep reads 321 while the range ends at 320.
