# E2CounterAttack — source-level mutants of the frozen C1 counter (round 71, w1)

Read-only against the lane tree: no lane-tree write, no git/jj mutation, no sysfs//proc read, no
secret content. All work ran `python3 tools/count-mp-rows-r71.py --fixture <scratch root>`; the
lane revision path (`--revision`) was never used, so no lane content was read by the counter.
Frozen base re-hashed on the byte copy used for mutation:
`fa67d4deb5f01a5124120276a8571fa36c7367d9db711ceb39bc1ca6fded48bc`.

## Method

- **13 mutants**, one frozen clause each. Each is a separate copy of the frozen counter with one
  textual deletion; every replacement is asserted to occur exactly once, and each mutant's sha256
  plus the full old/new block is in `mutants.txt` §MUTATION APPENDIX, so the mutation is
  reproducible from the frozen base without my scratch.
- **Independent fixture mirror** (not the committed battery): the four committed snapshots copied
  byte-exact, `SOURCES.json` regenerated from the copied bytes, control + 13 isolating specimens.
  Each specimen's exact note text is in `mutants.txt` §FIXTURE APPENDIX.
- **Isolation proof**: for every specimen, the frozen counter's own failure line names exactly the
  targeted clause (e.g. `statement-grounding=6/13`, `anchor-not-bound`, `map-digest`,
  `quote-words=29`); no specimen is rejected for a second reason.
- **Committed-battery replication**: the battery's control and 11 bad cases re-implemented from
  their shapes (data only, no import) and run under every mutant, to answer "would the battery
  alone have caught it".
- **Verdict rule applied literally**: KILLED iff the matched bad fixture still reads `met=0 rc 1`,
  or the control stops reading `met=1`. SURVIVOR otherwise. Under that rule a survivor is a clause
  the specimen depends on alone; a kill means another clause still rejects the specimen (dead or
  subsumed clause) or the control broke.

## Result

MUTANTS=13 KILLED=2 SURVIVORS=11. The committed battery alone catches **3 of the 11** survivors.
Rebuilding all 13 mutants from the published old/new blocks against the frozen base reproduces
every recorded sha256 (13/13), so the whole attack is re-runnable from the two probe files alone.

| mutant | clause removed | verdict | battery catches |
|---|---|---|---|
| m01-share-drop | share of grounded tokens >= 0.5 | SURVIVOR | no |
| m02-anchor-drop | registry anchor cell contains snapshot basename | SURVIVOR | no |
| m03-malformed-drop | MP-shaped unparseable line is a finding | SURVIVOR | yes |
| m04-reuse3 | no snapshot cited more than twice | SURVIVOR | yes |
| m05-quote-locate-drop | quote located verbatim in the snapshot | SURVIVOR | yes |
| m06-minwords7 | statement >= 12 words | SURVIVOR | no |
| m07-contiguous-drop | id set contiguous from 1 | SURVIVOR | no |
| m08-mapdigest-drop | row digest equals SOURCES.json digest | SURVIVOR | no |
| m09-quotewords | quote <= 25 words | SURVIVOR | no |
| m10-dupid-drop | id unique | SURVIVOR | no |
| m11-mintokens-drop | >= 6 distinct grounded tokens | SURVIVOR | no |
| m12-quotepipe-drop | quote contains no pipe | KILLED | no |
| m13-mapurl-drop | map url present (map-url) | KILLED | no |

## Findings

1. **Coverage gap, not a logic gap.** The committed 12/12 is real but narrow: only
   `mutant-malformed-row`, `mutant-snapshot-reuse` and `mutant-quote-absent` isolate a single
   clause. Five of its eleven bad cases fire two independent reasons at once (content-free,
   source-unbound, short-statement, duplicate-id, digest-swap), so removing either clause alone
   leaves the case red and the battery silent.
2. **The committed `mutant-duplicate-id` case cannot emit a duplicate id.** Its builder assigns
   ids positionally (`enumerate(rows, 1)`); appending a copy of row 1 yields MP7 with row 1's text
   (verified: `MP_ROWS=7 MP_VERIFIED=7`, failure `snapshot-reuse params.c=3`, never
   `duplicate-id`). The clause is unexercised; `m10` has zero deviations. My specimen keeps six
   rows and reuses id 3 on an otherwise fully verified row citing S300.
3. **Other confounded pairs.** `source-unbound` also breaks the anchor cell (S298's anchor names
   `moduleparam.h`); `digest-swap` zeroes the note digest so `digest-mismatch` fires before
   `map-digest`; `short-statement` is four words *and* grounded 1/1; `five-rows` has no row-level
   failure at all (the row count is what pins it).
4. **Dead clause.** The `quote-pipe` check is unreachable: `ROW_RE`'s literals already account for
   exactly seven pipes, so an eighth pipe inside the quote fails the `line.count("|") == 7` gate
   first and the row is reported `malformed-row`. `m12` is byte-identical in behaviour to the
   frozen counter on every specimen; no fixture can distinguish them. Outcome stays `met=0`, so
   this costs a diagnostic class, not soundness.
5. **Subsumed clause.** `map-url` is always accompanied by `source-not-bound` (both read the same
   missing `url`), so `m13` is killed by its specimen: the clause adds a message, not
   discrimination.
6. **Probe (not a clause mutant): the counter never reads the revision.** With `h=v7.2.10` URLs in
   both `SOURCES.json` and the registry and the committed digests unchanged, the frozen counter
   reads `rc=0 met=1`. Per the frozen predicates that is the specified outcome (the map URL is
   bound by containment only), so it is a predicate limit: no URL tag is ever compared with the
   snapshot, and the map is specimen-author-controlled.

## Advisory for the C1 note (not a verdict)

The counter's discrimination held on every specimen I could construct; what the round lacks is
fixture coverage, not clauses. To make the battery pin the declaration, it needs isolating cases
for: share 6/13, anchor-only, six-row duplicate id, id gap 1-5+7, map-digest vs file digest,
7-word grounded statement, 29-word verbatim quote, 3-grounded/14-word statement. All eight
specimen texts are in `mutants.txt` §FIXTURE APPENDIX and need no scratch to reuse.

## Limits

- Specimens are synthetic mirrors of the committed snapshots; no live host surface was touched.
- The battery replication is a re-implementation from the committed case shapes; its control and
  eleven bad cases reproduce the committed expectations under the frozen counter.
- A survivor is not a soundness failure on real content: it marks a clause that is the single
  guard for one class. The actionable column is battery coverage.
- Scratch `/fast/scratch/hyaku/tsukuroi-r71/E2CounterAttack` removed before yield; the two probe
  files below are self-contained (mutants, fixtures, verdicts, byte hashes).
- Tooling: no install or upgrade was needed (TOOLS_INSTALLED=none); no pacman transaction.

## Evidence

- `.ufo/waves/round-71/probes/E2CounterAttack/mutants.txt` (337 lines, sha256
  `beb3df7e9049c3b00b8f009a46cd497d6ab013911db6686a5b35341e146a3c95`): mutant table, isolation
  evidence, battery replication with MP summaries, mutant-effect table, mutation appendix,
  fixture appendix.
- `.ufo/waves/round-71/probes/E2CounterAttack/score.md` (112 lines, sha256
  `0ef73396525252dad068a343f5d2e9155c134553bacb722c375d43e3916da45a`): method, verdict rule,
  full mutant table, findings F0-F6, limits.

KEY=VALUE: MUTANTS=13 KILLED=2 SURVIVORS=11 SURVIVOR_CLASSES=share-threshold,anchor-binding,malformed-row,snapshot-reuse,quote-location,min-statement-words,id-contiguity,map-digest-binding,quote-word-bound,id-uniqueness,min-grounded-tokens BATTERY_CATCHES=3 DEAD_CLAUSES=1 SUBSUMED_CLAUSES=1 PROBE_REV_BLIND=met=1
