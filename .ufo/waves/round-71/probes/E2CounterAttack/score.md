# E2CounterAttack — source-level attack on the frozen C1 counter

Base: `tools/count-mp-rows-r71.py`, sha256 `fa67d4deb5f01a5124120276a8571fa36c7367d9db711ceb39bc1ca6fded48bc` (re-hashed on the byte copy used for mutation).
Fixture mirror: built by an independent builder kept in scratch (not the committed battery),
four committed snapshots copied unchanged, `SOURCES.json` regenerated from the copied bytes.

## Verdict rule (literal, as specified)
A mutant deletes exactly one frozen clause from the counter source. It is **KILLED** when the
matched bad fixture still reads `met=0 rc 1`, or when the control stops reading `met=1`;
**SURVIVOR** otherwise (control `met=1 rc 0` and the bad fixture `met=1 rc 0`). Read that way, a
survivor is a clause the specimen depends on alone: the broken note becomes acceptable the moment
the clause is gone. A kill means another clause still rejects the specimen (dead or subsumed
clause) or the mutation broke the control.

## Result: MUTANTS=13 KILLED=2 SURVIVORS=11; the committed battery alone catches 3 of 11 survivors.

Appendix check: all 13 mutants, rebuilt from `mutants.txt` §MUTATION APPENDIX against the
frozen base, reproduce the recorded sha256 (13/13), so the attack is reproducible without
the scratch tree.

| mutant | clause removed | control | isolating fixture | mutant on fixture | verdict | battery deviations |
|---|---|---|---|---|---|---|
| `m01-share-drop` | share of grounded tokens >= 0.5 | met=1 rc0 | `b01` | rc=0 met=1 | **SURVIVOR** | none |
| `m02-anchor-drop` | registry anchor cell contains snapshot basename | met=1 rc0 | `b02` | rc=0 met=1 | **SURVIVOR** | none |
| `m03-malformed-drop` | MP-shaped unparseable line is a finding | met=1 rc0 | `b03` | rc=0 met=1 | **SURVIVOR** | `mutant-malformed-row` |
| `m04-reuse3` | no snapshot cited more than twice | met=1 rc0 | `b04` | rc=0 met=1 | **SURVIVOR** | `mutant-snapshot-reuse` |
| `m05-quote-locate-drop` | quote located verbatim in the snapshot | met=1 rc0 | `b05` | rc=0 met=1 | **SURVIVOR** | `mutant-quote-absent` |
| `m06-minwords7` | statement >= 12 words | met=1 rc0 | `b06` | rc=0 met=1 | **SURVIVOR** | none |
| `m07-contiguous-drop` | id set contiguous from 1 | met=1 rc0 | `b07` | rc=0 met=1 | **SURVIVOR** | none |
| `m08-mapdigest-drop` | row digest equals SOURCES.json digest | met=1 rc0 | `b08` | rc=0 met=1 | **SURVIVOR** | none |
| `m09-quotewords` | quote <= 25 words | met=1 rc0 | `b09` | rc=0 met=1 | **SURVIVOR** | none |
| `m10-dupid-drop` | id unique | met=1 rc0 | `b10` | rc=0 met=1 | **SURVIVOR** | none |
| `m11-mintokens-drop` | >= 6 distinct grounded tokens | met=1 rc0 | `b11` | rc=0 met=1 | **SURVIVOR** | none |
| `m12-quotepipe-drop` | quote contains no pipe | met=1 rc0 | `b12` | rc=1 met=0 | **KILLED** | none |
| `m13-mapurl-drop` | map url present (map-url) | met=1 rc0 | `b13` | rc=1 met=0 | **KILLED** | none |

Isolation evidence (frozen counter on each specimen, one reason each):

- `b01` targets *share >= 0.5* → `MP_ROW fail MP1 statement-grounding=6/13`
- `b02` targets *anchor cell contains snapshot basename* → `MP_ROW fail MP1 anchor-not-bound`; `MP_ROW fail MP2 anchor-not-bound`
- `b03` targets *malformed-row detection* → `MP_ROW fail malformed-row: |MP7| short | source=S297 | snapshot=params.c | digest=0 | quote="x" |`
- `b04` targets *snapshot reuse <= 2* → `MP_ROW fail snapshot-reuse params.c=3`
- `b05` targets *quote located verbatim* → `MP_ROW fail MP2 quote-absent`
- `b06` targets *statement >= 12 words* → `MP_ROW fail MP1 statement-words=7`
- `b07` targets *id set contiguous from 1* → `MP_ROW fail ids-not-contiguous`
- `b08` targets *row digest == SOURCES.json digest* → `MP_ROW fail MP1 map-digest`; `MP_ROW fail MP2 map-digest`
- `b09` targets *quote <= 25 words* → `MP_ROW fail MP6 quote-words=29`
- `b10` targets *id unique* → `MP_ROW fail MP3 duplicate-id`
- `b11` targets *>= 6 distinct grounded tokens* → `MP_ROW fail MP1 statement-grounding=3/6`
- `b12` targets *quote contains no pipe* → `MP_ROW fail malformed-row: | MP1 | module_param_sysfs_setup skips any kparam whose perm equals ze`; `MP_ROW fail ids-not-contiguous`
- `b13` targets *map url present (map-url)* → `MP_ROW fail MP1 map-url source-not-bound`; `MP_ROW fail MP2 map-url source-not-bound`

## Findings

**F0 — every mutation is a loosening, so no control broke.** All 13 controls read `met=1 rc 0`;
the KILLED leg is reachable only when another clause still rejects the specimen, i.e. through
dead or subsumed clauses (F4, F5).

**F1 — 8 of the 11 load-bearing clauses have no isolating guard in the committed battery.**
Battery cases deviate under only these mutants: `m03-malformed-drop`, `m04-reuse3`, `m05-quote-locate-drop`.
Unaffected: `m01-share-drop`, `m02-anchor-drop`, `m06-minwords7`, `m07-contiguous-drop`, `m08-mapdigest-drop`, `m09-quotewords`, `m10-dupid-drop`, `m11-mintokens-drop`.
The battery's 12/12 is real but narrow: five of its eleven bad cases fire two independent
reasons at once (content-free, source-unbound, short-statement, duplicate-id, digest-swap),
and a sixth never contains the defect it names (F2).

**F2 — the committed `mutant-duplicate-id` case cannot emit a duplicate id at all.** Its
builder assigns ids positionally (`enumerate(rows, 1)`), so appending a copy of row 1 yields
MP7 with row 1's text: the replicated run fails with `snapshot-reuse params.c=3` and a
seven-row count, and never with `duplicate-id`. The clause is unexercised by the committed
battery; `m10` therefore has zero deviations, while my six-row specimen with id 3 twice
(`b10`, the sixth row otherwise fully verified and citing S300) is accepted once the clause
is gone.

**F3 — the remaining confounded pairs.**
- `mutant-source-unbound` reports `source-not-bound anchor-not-bound`: S298's anchor names
  `moduleparam.h`, so removing the anchor clause alone is invisible (`m02`).
- `mutant-digest-swap` zeroes the note digest, so `digest-mismatch` fires before `map-digest`;
  the row-vs-`SOURCES.json` binding is never isolated (`m08` passes an all-zero map digest).
- `mutant-short-statement` is four words *and* ungrounded (1/1): two reasons fire, so `m06`
  (7-word bound) cannot be seen; my `b06` is a 7-word statement grounded 7/7.
- `mutant-five-rows` has no row-level failure at all: it is caught by the row count, so it
  says nothing about id contiguity (`b07` does: ids 1-5 and 7, all rows otherwise verified).
- Truly isolating in the battery: `mutant-malformed-row` (`m03`), `mutant-snapshot-reuse`
  (`m04`; four distinct snapshots survive that edit), `mutant-quote-absent` (`m05`).

**F4 — the `quote-pipe` clause is unreachable (equivalent mutant, `m12` KILLED).**
`ROW_RE`'s literals account for exactly seven pipes; an eighth pipe inside the quote fails the
`line.count("|") == 7` gate first, so a pipe-bearing quote is reported as `malformed-row`
(and, because its row is dropped, as `ids-not-contiguous`). The `m12` run is byte-identical to
the frozen counter's; no fixture can distinguish them. Outcome stays `met=0`, so this costs a
diagnostic class, not soundness.

**F5 — `map-url` is subsumed (`m13` KILLED).** A missing map `url` also makes
`not url or url not in regrow["source"]` fire, so `source-not-bound` rejects the specimen
with or without the clause (both lines carry `map-url source-not-bound`; dropping the first
leaves the second). The clause adds a message, not discrimination.

**F6 — probe (not a clause mutant): the counter never reads the revision.** With `h=v7.2.10`
URLs in both `SOURCES.json` and the registry and the committed digests unchanged, the frozen
counter reads rc=0 met1=True. Per the frozen predicates that is the
specified outcome (the map URL is bound by containment only), so this is a predicate limit: an
URL's tag is never compared with the snapshot's, and the map is specimen-author-controlled.

## Limits
- Specimens are synthetic mirrors of the committed snapshots; no lane tree was read at another
  revision and no Git object was required. The frozen counter was not modified in place;
  every mutant is a separate copy under scratch.
- The battery replication is re-implemented from the committed case shapes (statements and
  fixture edits), not imported; its control and 11 bad cases reproduce the committed
  expectations under the frozen counter.
- A survivor is not a counter defeat on real content: it shows the clause is the single guard
  for that class. The actionable reading is the battery coverage column, not the survivor count.
