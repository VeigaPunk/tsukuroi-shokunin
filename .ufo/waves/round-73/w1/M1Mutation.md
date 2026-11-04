# M1Mutation — clause-isolated mutant batteries, round 73 w1

status: done
verdict: both frozen instruments are operable and clause-separable; 38 mutants
(21 counter + 17 routed checker), 6 survivors, all 6 dead/entailed/crashing clauses
rather than wrong verdicts. The C1 target reads met=1 and the C2 target reads 0/3
with the *frozen* bytes at the landed HEAD.

## 0. What was mutated

The frozen instruments are the **declared bytes at 74937132**, not the worktree (which
another seat hardened concurrently during this wave):

| instrument | frozen sha256 |
|---|---|
| `tools/count-ul-rows-r73.py` | `542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6` |
| `tools/check-r72-routed-r73.py` | `93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e` |

Both digests matched the declaration before any copy was taken. Every mutant is a
**one-line edit** of those bytes, generated in `$S` and never written into the lane
(per-mutant sha256 and changed-line counts are in `counter_matrix.json` /
`c2_matrix.json`). Fixtures are built by the instruments' own `build_fixture` from
the three committed v262 snapshots, then one clause is violated.

Detectors and verdict words used below:

- **selftest** — the instrument's own committed `--selftest`. `killed` = suite fails (rc 3).
- **fixture** — a mirror that only the mutated clause can reject (pristine rc 1, target
  problem id present, no other problem id). `killed` = mutant loses the rejection
  (rc flips 1→0); `token-lost` = rc unchanged but the clause's problem id disappears
  (another clause rejects the same defect); `survived` = output identical.

All commands below are reproducible, e.g.
`bash .ufo/waves/round-73/w1/M1Mutation/repro.sh mutant U15 reuse` (the harness
re-extracts the frozen bytes from Git and cleans `$S` on exit).

## 1. C1 — `count-ul-rows-r73.py` matrix (21 mutants, 24 fixtures)

| mutant | clause | selftest | fixture isolation | command |
|---|---|---|---|---|
| U01 | id contiguity | survived | killed (`contig`, rc 1→0) | mutant U01 contig |
| U02 | statement words | killed | killed (`words`) | mutant U02 words |
| U03 | grounding | killed | killed (`ground`) | mutant U03 ground |
| U04 | source kind, both arms | killed | killed (`kind_bogus`, `kind_own`) | mutant U04 kind_bogus |
| U05 | source kind, KINDS membership arm | survived | killed (`kind_bogus`) | mutant U05 kind_bogus |
| U06 | source kind, own-work arm | survived | **survived** (`kind_own`, 1→1) | mutant U06 kind_own |
| U07 | digest (file vs note) | killed | killed (`digest`) | mutant U07 digest |
| U08 | map binding (map digest) | survived | killed (`mapdigest`) | mutant U08 mapdigest |
| U09 | map binding (map url type) | survived | token-lost (`mapurl_none`) / **survived** (`mapurl`, crash) | mutant U09 mapurl_none |
| U10 | map binding (source cell carries url) | survived | killed (`srcbound`) | mutant U10 srcbound |
| U11 | anchor binding | survived | killed (`anchor`) | mutant U11 anchor |
| U12 | quote location | killed | killed (`quoteloc`) | mutant U12 quoteloc |
| U13 | quote length | survived | killed (`quotelen`, 30 words) | mutant U13 quotelen |
| U14 | quote pipe | survived | **survived** (`quotepipe`, unreachable) | mutant U14 quotepipe |
| U15 | snapshot reuse | killed | killed (`reuse`, 3×) | mutant U15 reuse |
| U16 | malformed-row counting | killed | killed (`malformed`) | mutant U16 malformed |
| U17 | target arithmetic (verified==6) | killed | killed (`ground`, 1→0) | mutant U17 ground |
| U18 | target arithmetic (rows==6) | survived | killed (`seven`, 1→0) | mutant U18 seven |
| U19 | target arithmetic (sources>=3) | survived | killed (`tgtsrc`, 1→0) | mutant U19 tgtsrc |
| U20 | target arithmetic (snapshots>=3) | survived | **survived** (`two_snap`, entailed) | mutant U20 two_snap |
| U21 | target arithmetic (malformed==0) | killed | killed (`malformed`) | mutant U21 malformed |

Fixture readings used as the isolation baselines (pristine, frozen bytes):

```
control          rc=0  UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0  met=1
contig           rc=1  ids-not-contiguous
words            rc=1  UL1 statement-words=8
ground           rc=1  UL6 statement-grounding=0/12
kind_bogus/own   rc=1  source-kind=blog / own-work
digest           rc=1  UL3,UL4 digest-mismatch
mapdigest        rc=1  UL3,UL4 map-digest
mapurl_none      rc=1  UL3,UL4 map-url source-not-bound
mapurl           rc=EXC TypeError: 'in <string>' requires string as left operand, not int
srcbound         rc=1  UL5,UL6 source-not-bound
anchor           rc=1  UL1,UL2 anchor-not-bound
quoteloc         rc=1  UL6 quote-absent
quotelen         rc=1  UL1 quote-words=30
quotepipe        rc=1  malformed-row + ids-not-contiguous (quote-pipe token never emitted)
reuse            rc=1  snapshot-reuse systemd.unit.xml=3
malformed        rc=1  malformed-row
seven            rc=1  UL_ROWS=7 UL_VERIFIED=6; UL7 statement-words=8
tgtsrc           rc=1  UL_SOURCES=2, no row problem
two_snap         rc=1  UL_SNAPSHOTS=2, snapshot-reuse systemd.unit.xml=4
```

## 2. C2 — `check-r72-routed-r73.py` matrix (17 mutants, 24 fixtures)

| mutant | clause | selftest | fixture isolation | command |
|---|---|---|---|---|
| C01 | lesson token `R72-LESSON-SUPERSEDED-CLAIMS` | survived | killed (`l_no_id`) | mutant C01 l_no_id |
| C02 | lesson token `No capability row enters this round` | survived | killed (`l_no_nocap`) | mutant C02 l_no_nocap |
| C03 | lesson token `nine hermetic cases` | survived | killed (`l_no_nine`) | mutant C03 l_no_nine |
| C04 | lesson token `gate-selftest` | survived | killed (`l_no_gs`) | mutant C04 l_no_gs |
| C05 | lesson token `ten` | survived | killed (`l_no_ten_strict`) | mutant C05 l_no_ten_strict |
| C06 | lesson token `10 cases` | survived | killed (`l_no_10cases`) | mutant C06 l_no_10cases |
| C07 | digest token `OLD_DIGEST` | survived | killed (`d_no_old`) | mutant C07 d_no_old |
| C08 | digest token `TIP_DIGEST` | survived | killed (`d_no_tip`) | mutant C08 d_no_tip |
| C09 | digest `need_any` receipt alternative | survived | killed (`d_receipt_only`, 0→1) | mutant C09 d_receipt_only |
| C10 | capability token `gate-selftest` | survived | killed (`c_no_gs`) | mutant C10 c_no_gs |
| C11 | capability token `ten` | survived | killed (`c_no_ten`) | mutant C11 c_no_ten |
| C12 | capability token `RECEIPT` | survived | killed (`c_no_receipt`) | mutant C12 c_no_receipt |
| C13 | block-heading line-start anchor | survived | killed (`anchor_midline`, 1→0) | mutant C13 anchor_midline |
| C14 | item-heading line-start anchor (lesson) | survived | **survived** (`anchor_midline`, redundant) | mutant C14 anchor_midline |
| C15 | lesson `need_any` | survived | **survived** (`l_needany_gone`, entailed) | mutant C15 l_needany_gone |
| C16 | digest `need_any` | survived | killed (`d_no_needany`) | mutant C16 d_no_needany |
| C17 | capability `need_any` | survived | killed (`c_needany_gone`) | mutant C17 c_needany_gone |

Every clause-isolated C2 fixture is rejected by pristine and accepted by its mutant,
except the three annotated equivalences; e.g. `bash repro.sh c2fixture anchor_midline`
gives `LESSON-STALE ... ROUTED_STALE=1` and `bash repro.sh c2mutant C13 anchor_midline`
gives `ROUTED_STALE=0`.

## 3. Committed-selftest scoring (item 4)

**Counter: 11 cases; 9 assert a named finding id, 2 assert a non-id string, 0 assert
only rc.** Isolation of the case fixtures (replayed independently, `selftest_cases`
in `counter_matrix.json`):

| case | asserted token | problem ids actually emitted | single-clause? |
|---|---|---|---|
| CONTROL | `UL_TARGET` | none | control only |
| SHORT | `statement-words` | `statement-words=4 statement-grounding=1/2` | no — cascade |
| UNREGISTERED | `source-unregistered` | `source-unregistered` | yes |
| QUOTE | `quote-absent` | `quote-absent` | yes |
| FIVE | `UL_ROWS=5` (summary line) | none | no problem id asserted |
| DUPID | `duplicate-id` | `duplicate-id` | yes |
| REUSE | `snapshot-reuse` | `digest-mismatch map-digest quote-absent source-not-bound anchor-not-bound` + `snapshot-reuse` | no — 5 cascades |
| UNGROUNDED | `statement-grounding` | `statement-grounding=0/12` | yes |
| MALFORMED | `malformed-row` | `malformed-row` | yes |
| DIGEST | `digest-mismatch` | `digest-mismatch map-digest` | no — cascade |
| OWNWORK | `source-kind` | `source-kind=own-work` (×2) | yes |

So 6/9 named-id cases are single-clause; 3/9 pass on a token that another clause also
emits (`SHORT`, `REUSE`, `DIGEST`). The FIVE case asserts a counter line, not the
`met` decision — U18 (rows==6 removed) and U17 (verified removed) show the difference:
U18 survives the suite, U17 kills it through seven *other* cases.

**Routed checker: 5 cases; 4 assert a named finding id, 1 asserts the summary
(`ROUTED_STALE=0`), 0 assert only rc.** Clause isolation is 0/5:

| case | asserted | why it fails on the mutant fixture | exercises |
|---|---|---|---|
| CONTROL | `ROUTED_STALE=0` | — | happy path |
| LESSON | `LESSON-STALE` | block heading is `## Gate`, never matches | heading only |
| DIGEST | `DIGEST-STALE` | heading matches, but the block has **zero** tokens and **zero** need_any alternatives | cannot isolate a token |
| CAPABILITY | `CAPABILITY-STALE` | block heading is `## Note`, never matches | heading only |
| UNANCHORED | `LESSON-STALE` | the prose lives inside the `## Gate` block; there is no `## Correction` at all | heading only — *not* an anchor test |

This is measured, not inferred: **17/17 checker mutants survive the committed suite**
(including C13, the line-start anchor), and 12/21 counter mutants survive it. The
committed suites detect whole-feature removal but almost no single-clause removal.

## 4. Attacks (frozen bytes) — `held` / `survived`

| # | attempt to satisfy the predicate without the work | command | observed | verdict |
|---|---|---|---|---|
| A1 | six content-free rows: each statement is a 16-token bag drawn from its own snapshot (no rule asserted) | `repro.sh fixture tokensalad` | `UL_VERIFIED=6 ... met=1`, rc 0 | **survived** (lexical grounding only) |
| A2 | quote is verbatim in the snapshot but unrelated to the statement | `repro.sh fixture quote_unrelated` | rc 0, met=1 | **survived** (quote presence ≠ support) |
| A3 | empty quote `quote=""` on all six rows | `repro.sh fixture empty_quote` | rc 0, met=1 (frozen); committed HEAD 97f6f5ec: `quote-words=0`, rc 1 | **survived** frozen, **held** by hardened |
| A4 | doctored snapshot: append bytes, recompute map digest and note digest (self-consistent conspiracy) | `repro.sh fixture doctored` | rc 0, met=1 | **survived** (digest chain proves consistency, not provenance) |
| A5 | mid-line `## Correction ...` carrying every token (unanchored block) | `repro.sh c2fixture anchor_midline` | `LESSON-STALE`, rc 1 | **held** |
| A6 | finding id only in the block **heading**, body omits it | `repro.sh c2fixture heading_token` | `ROUTED_STALE=0`, rc 0 | **survived** (heading text is part of `body` in `blocks()`) |
| A7 | `ten` matched inside `sentences` / `often` | `repro.sh c2fixture l_no_ten` + `python3 -c 'print("ten" in "sentences")'` | rc 0; `True` | **survived** frozen (substring); **held** by hardened `has_token` |
| A8 | required tokens only outside the satisfying block | `repro.sh c2fixture l_outside_block` | `LESSON-STALE`, rc 1 | **held** |
| A9 | receipt path named but no receipt file exists | `repro.sh c2fixture good` (fixture tree has no `.ufo/...` file) | rc 0 | **survived** frozen (path is a literal, never read); **held** by hardened (existence + ≥10 cases) |
| A10 | SOURCES.json `url` is an integer | `repro.sh fixture mapurl` | `TypeError: 'in <string>' requires string as left operand, not int`, process rc 1 | instrument crash — see §6 |
| A11 | quote containing `\|` | `repro.sh fixture quotepipe` | row is `malformed-row`; `quote-pipe` never emitted | clause unreachable |

Snapshot provenance was checked out-of-band against the real v262 URLs and **held**:
all three committed files hash to the same sha256 as
`raw.githubusercontent.com/systemd/systemd/v262/...` (`systemd.unit.xml
eb9479be…`, `unit.c 47e98d39…`, `install.c c11cd575…`). A4 is therefore a limit of
the instrument, not a defect in the committed data.

## 5. Survivors — class and what would kill them

| survivor | class | why no fixture can kill it (as written) | what would kill it |
|---|---|---|---|
| U06 (own-work arm) | clause duplicated | `own-work ∉ KINDS`, so the membership test rejects it too; the explicit QUALITY-86 arm is dead code | add `own-work` to `KINDS` and keep the explicit arm — then only `f_kind_own` distinguishes |
| U09 (map url type) | instrument crash + token redundant | truthy non-string url crashes the later `url not in regrow["source"]`; falsy non-string also trips `source-not-bound`, so `map-url` is never load-bearing | type-guard `url` before the `in` test, then a fixture with a truthy non-string url rejected only by `map-url` |
| U14 (quote pipe) | clause unreachable | any `\|` in the quote makes `line.count("\|") == 8`, so the row is `malformed-row` before the quote test | replace the `count==7` shape test with grammar parsing (or delete the clause) |
| U20 (snapshots>=3) | entailed conjunct | 6 verified rows with `max_reuse=2` imply ≥3 distinct snapshots; the nearest fixture (`two_snap`) hits reuse 4 first | none while `verified==6` and `max_reuse=2` are conjuncts — it is algebraically implied |
| C14 (item-heading `^`) | redundant anchor | `blocks()` only yields substrings that begin at a `## ` match, so `head` always starts with `## `; even an unanchored `HEADING_RE` leaves `head` starting at `##` | change `blocks()` to yield a heading that does not begin with `##` |
| C15 (lesson need_any) | entailed clause | `10 cases` is both a required token and a `need_any` alternative, so token completion always satisfies it | remove `10 cases` from the token list (or the alternative), then a correct-heading block with no alternative |

## 6. Operability findings, with commands

1. **Non-string map URL crashes the instrument** (frozen *and* committed HEAD):
   `repro.sh fixture mapurl` → TypeError, process exit 1 — indistinguishable from
   the documented stale verdict (rc 1). A type guard is missing before
   `url not in regrow["source"]`.
2. **Absent data file returns rc 128**, outside the frozen exit map (0/1/2/3):
   `repro.sh absent` → `UL_NOTE absent ... rc=128`. The hardened committed HEAD
   documents 128; the frozen header does not.
3. **`quote-pipe` is dead code** (`quotepipe` fixture): the row-shape check rejects
   any quote containing `|` as `malformed-row` first.
4. **C1/C2 at the landed HEAD with the frozen bytes** (stable claims):
   `repro.sh c1at HEAD` → `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3
   UL_MALFORMED=0`, `met=1`, rc 0; `repro.sh routed HEAD` → `ROUTED_STALE=0
   ROUTED_OK=3/3`, rc 0; `repro.sh routed eb105757…` → `ROUTED_STALE=3`, rc 1
   (matches the declaration's "at base it reads ROUTED_STALE=3").
5. **Concurrent instrument drift during the wave** (recorded, not a finding against
   the frozen matrix): at 02:06Z HEAD was `8eeadcb9` with both files at the declared
   digests (counter: note absent, rc 128; checker: 3/3 stale). The lane then landed
   `09dac09f`, `583eea87`, and finally `3efb9b24`, where the committed instruments are
   `97f6f5ec…` (counter, 12/12 selftest) and `71931c1c…` (checker, 11/11 selftest).
   A transient uncommitted edit to the checker was observed failing its own
   `--selftest`: one snapshot raised `AttributeError: 'NoneType' object has no attribute
   'items'` at `case("PLACEHOLDER", None, ...)`, and a later snapshot of the same
   in-flight file returned rc 3 with `PLACEHOLDER` still at line 265; the committed
   HEAD blob is clean and was re-extracted from Git before the post-fix spot check, so
   no report is made against that transient state.
6. **Post-fix spot check on the committed HEAD instruments** (digests above):
   empty quote now rejected (`quote-words=0`); mid-line block still rejected; the
   "ten"-inside-a-word trick closed by whole-token matching; but `heading_token`
   (A6) still returns `ROUTED_STALE=0`, the map-url crash (A10) is unchanged, and
   `tokensalad` / `quote_unrelated` / `doctored` still pass the counter (inherent to
   a lexical grounding design).

Tools installed/upgraded: none. Only read-only `git show`/`cat-file`, `curl` (three
v262 snapshots), Python stdlib. No lane file was written; all fixtures and mutants
lived in `/fast/scratch/hyaku/tsukuroi-r73/M1Mutation` and were deleted at yield.

## 7. Reproduction

```
bash .ufo/waves/round-73/w1/M1Mutation/repro.sh counter        # 21-mutant matrix + case table
bash .ufo/waves/round-73/w1/M1Mutation/repro.sh c2             # 17-mutant matrix
bash .ufo/waves/round-73/w1/M1Mutation/repro.sh mutant U15 reuse
bash .ufo/waves/round-73/w1/M1Mutation/repro.sh c2mutant C13 anchor_midline
bash .ufo/waves/round-73/w1/M1Mutation/repro.sh absent
bash .ufo/waves/round-73/w1/M1Mutation/repro.sh c1at HEAD
bash .ufo/waves/round-73/w1/M1Mutation/repro.sh routed eb1057575d5d8b940c4846e21611674cf5571aea
```

SURVIVORS=6 classes=clause-duplicated,instrument-crash+token-redundant,unreachable-clause,entailed-conjunct,redundant-anchor,entailed-clause
