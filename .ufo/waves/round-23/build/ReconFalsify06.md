# ReconFalsify06 — r23 falsify group 6: rough-vs-old-v1 path-authority reconciliation

Scope seat: `ReconFalsify06` (leaf, no dispatch). Input pack: `.ufo/waves/round-23/packs/falsify-06.json`
(schema `tsukuroi-path-oracle-pack-v1`, wave `falsify`, group `6`, 8 seats, 134 events).
Authority source: `.ufo/waves/round-23/sources/r22-rough-census.txt` (frozen r22 rough path-census source cell,
read as source data only, never executed). Declared old-v1 authority: `.ufo/waves/round-23/preregister.json`
(`outside_round22.path_counts_as_reported`, C2 "legacy schema-v1 policy" scope wording, C3 claim).

## Axes named (godspeed)

| Axis | Question | Move (cheap, parallel) | Outcome |
|---|---|---|---|
| A. Per-event path verdict | For every event, does the exact rough algorithm flag a path violation? | hand-derive per event from the frozen cell | 134/134 events adjudicated |
| B. Component order / one-per-event break | Does the `;` split and the per-event `break` change the count? | enumerate components of the only multi-path event | 1 event order-sensitive; break unexercised |
| C. Selector-normalization width | Which raw suffixes does `strip_sel` actually strip, and where would a narrower stripper flip the verdict? | classify every suffix form | 7 outcome-critical forms, 2 already-violating |
| D. Counter-bucket arithmetic | `path` vs `unknown` vs `exec` vs total — which bucket does each event land in? | bucket arithmetic per seat | pack rough = path 3 / unknown 4 / exec 0 / total 7 |
| E. Event identity | Does one event equal one recorded unit? | compare call_id cardinality to event cardinality | 1 seat reuses a call_id across 3 events |
| F. Authority containment | v1 vs v2 semantics; what may not be imported | preregister separability/limits | v2 edit rules excluded from v1 arithmetic |

No move was retained that improves no axis or harms another: the D/E findings are re-expressions of A, not new
verdicts, and the F bound removes exactly the one inference (re-labelling the 4 edit events as v1 path
violations) that would have been unsupported.

## 1. Exact rough algorithm, as frozen

From `.ufo/waves/round-23/sources/r22-rough-census.txt` (interpreted, not run):

1. `bash` -> `f['exec'] += 1`, seat marked, `continue`.
2. tool not in `('read','grep','glob','write')` -> `f['unknown'] += 1`, seat marked, `continue`.
3. `vals = str(a.get('path','')).split(';')` for `grep`/`glob`; otherwise `[str(a.get('path',''))]`.
4. `q = strip_sel(v)` for `read`/`grep` only; for `write`/`glob` the raw string is compared.
5. membership test: `q not in (b['write_paths'] if t=='write' else b['read_paths'])` -> `f['path'] += 1`,
   seat marked, `break` (one violation per event, first offending component only).
6. `strip_sel` = `re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`.

Consequences I rely on (hand-derived, verified by reading the regex, not by execution):

- The range character class `[\d\-+,:]` **includes `,` and `:`**, so comma-separated ranges
  (`:31-73,85-120,135-160`) strip as one unit, and the optional trailing `(:raw)?` lets `:1-140:raw` and
  `:24:raw` strip as one unit. `-\d+` covers the negative tail form `:-8`; `raw` covers the bare `:raw`.
- `strip_sel` is **not** applied to `write` or `glob` in this cell.
- `read`/`grep` are tested against `read_paths` only; `write` against `write_paths` only. A `read` of a
  write-declared path is a violation under this cell.
- One `path` increment per event maximum, attributed to the first offending component in list order.

## 2. Declared old-v1 authority used for comparison

The r23 preregister declares only the aggregate pair (ground truth, not re-derived): rough `build 25 /
falsify 33`, lane `build 23 / falsify 29`, and states the lane figures come from the legacy schema-v1 path
authority while r23 adds a new explicit schema-v2 edit-target authority (C2) that "does not change legacy
schema-v1 policy and historical reds". The v1 per-event rule this seat reconstructs from the frozen cell is:
read/grep/glob -> `read_paths`; write -> `write_paths`; per-event first-offending-component; **no v1 edit
rule**. The lane's own v1 checker source (`round-22/candidate/tools/check-seat-bindings.py` and the round-22
preregister) is **outside this seat's declared read scope**, so every v1 statement below is labelled as a
reconstruction from the frozen cell + pack binding, not as a reading of the v1 tool.

## 3. Per-seat, per-event ledger (134 events, exhaustive)

Verdict codes: `OK` = no path violation under the exact rough cell; `P` = path violation
(`f['path'] += 1`); `U` = unknown-tool bucket (`f['unknown'] += 1`, not a path verdict);
`URI` = compliant only because the literal string `skill://godspeed` is present in `read_paths`.

Suffix column gives the **raw** path suffix exactly as recorded in the pack.

### FxC3Clean (24 events; agent TsukuroiR22.FxC3Clean-2)
```
ev0  read  cohort.py                    (no suffix)  OK
ev1  read  snapshots.py                  (no suffix)  OK
ev2  read  _revision.py                  (no suffix)  OK
ev3  read  preregister.json              (no suffix)  OK
ev4  read  host-tool-boundary.json       (no suffix)  OK
ev5  read  seat-boundary-r22.json        (no suffix)  OK
ev6  read  seat-boundary-r22.md          (no suffix)  OK
ev7  read  skill://godspeed              (no suffix)  OK (URI)
ev8  read  cohort.py                    :31-73       OK
ev9  read  cohort.py                    :83-123      OK
ev10 read  cohort.py                    :124-164     OK
ev11 read  snapshots.py                  :1-11        OK
ev12 read  snapshots.py                  :27-60       OK
ev13 read  snapshots.py                  :61-130      OK
ev14 read  snapshots.py                  :131-175     OK
ev15 read  snapshots.py                  :15-25       OK
ev16 read  snapshots.py                  :178-241     OK
ev17 read  snapshots.py                  :242-278     OK
ev18 read  _revision.py                  :3-38        OK
ev19 read  _revision.py                  :62-66       OK
ev20 read  _revision.py                  :172-192     OK
ev21 read  _revision.py                  :42-111      OK
ev22 read  _revision.py                  :112-170     OK
ev23 write falsify/FxC3Clean.md          (no suffix)  OK (exact write_paths[0])
```
Bucket: path 0, unknown 0, exec 0, total 0. Seat not marked.

### FxC3Faulty (17 events; TsukuroiR22.FxC3Faulty-2)
```
ev0  read  skill://godspeed              (no suffix)  OK (URI)
ev1  read  cohort.py                    (no suffix)  OK
ev2  read  cohort.py                    :1-140:raw   OK
ev3  read  cohort.py                    :141-260:raw OK
ev4  read  snapshots.py                  :1-160:raw   OK
ev5  read  preregister.json              (no suffix)  OK
ev6  read  snapshots.py                  :161-278:raw OK
ev7  read  host-tool-boundary.json       (no suffix)  OK
ev8  read  seat-boundary-r22.json        (no suffix)  OK
ev9  read  seat-boundary-r22.md          (no suffix)  OK
ev10 read  _revision.py                  (no suffix)  OK
ev11 read  cohort.py                    :24-100      OK
ev12 read  cohort.py                    :100-164     OK
ev13 read  snapshots.py                  :70-120      OK
ev14 grep  cohort.py                    (no suffix)  OK
ev15 grep  snapshots.py                  (no suffix)  OK
ev16 write falsify/FxC3Faulty.md         (no suffix)  OK
```
Bucket: path 0, unknown 0, exec 0, total 0. Seat not marked.

### FxC3Dead (18 events; TsukuroiR22.FxC3Dead-2)
```
ev0  read  cohort.py                    (no suffix)  OK
ev1  read  preregister.json              (no suffix)  OK
ev2  read  skill://godspeed              (no suffix)  OK (URI)
ev3  read  cohort.py                    :1-120       OK
ev4  read  cohort.py                    :120-220     OK
ev5  read  snapshots.py                  (no suffix)  OK
ev6  read  _revision.py                  (no suffix)  OK
ev7  read  seat-boundary-r22.json        (no suffix)  OK
ev8  read  seat-boundary-r22.md          (no suffix)  OK
ev9  read  host-tool-boundary.json       (no suffix)  OK
ev10 read  snapshots.py                  :1-130       OK
ev11 read  snapshots.py                  :130-280     OK
ev12 grep  cohort.py                    (no suffix)  OK
ev13 grep  snapshots.py                  (no suffix)  OK
ev14 read  cohort.py                    :40-80       OK
ev15 grep  snapshots.py                  (no suffix)  OK
ev16 grep  cohort.py                    (no suffix)  OK
ev17 write falsify/FxC3Dead.md           (no suffix)  OK
```
Bucket: path 0, unknown 0, exec 0, total 0. Seat not marked.

### FxC3Unresolved (10 events; TsukuroiR22.FxC3Unresolved-2) — seat marked
```
ev0  read  cohort.py                    (no suffix)  OK
ev1  read  preregister.json              (no suffix)  OK
ev2  read  snapshots.py                  (no suffix)  OK
ev3  read  _revision.py                  (no suffix)  OK
ev4  read  seat-boundary-r22.md          (no suffix)  OK
ev5  read  seat-boundary-r22.json        (no suffix)  OK
ev6  read  host-tool-boundary.json       (no suffix)  OK
ev7  edit  falsify/FxC3Unresolved.md     (no suffix)  U   (tool 'edit' not path-checked; target == write_paths[0])
ev8  read  falsify/FxC3Unresolved.md    :raw         P   (base is write-declared, absent from read_paths)
ev9  write falsify/FxC3Unresolved.md     (no suffix)  OK
```
Bucket: path 1, unknown 1, exec 0, total 2. Call_id cardinality 8 for 10 events (ev7/ev8/ev9 share one).

### FxC3Partial (17 events; TsukuroiR22.FxC3Partial-2)
```
ev0  read  skill://godspeed              (no suffix)  OK (URI)
ev1  read  cohort.py                    (no suffix)  OK
ev2  grep  cohort.py                    (no suffix)  OK
ev3  read  preregister.json              (no suffix)  OK
ev4  read  host-tool-boundary.json       (no suffix)  OK
ev5  read  cohort.py                    :31-73,85-120,135-160      OK
ev6  read  snapshots.py                  (no suffix)  OK
ev7  read  _revision.py                  (no suffix)  OK
ev8  read  cohort.py                    :121-133     OK
ev9  read  snapshots.py                  :4-11,28-29,47-128,131-142 OK
ev10 grep  5 ';'-joined read_paths      (components) OK  (0 violations; 5 components enumerated below)
ev11 read  seat-boundary-r22.md          :1-40        OK
ev12 read  seat-boundary-r22.md          :24:raw      OK
ev13 read  seat-boundary-r22.json        (no suffix)  OK
ev14 read  snapshots.py                  :33-39       OK
ev15 read  _revision.py                  :62-66       OK
ev16 write falsify/FxC3Partial.md        (no suffix)  OK
```
Bucket: path 0, unknown 0, exec 0, total 0. Seat not marked.

### FxC3FalseDeath (6 events; TsukuroiR22.FxC3FalseDeath-2)
```
ev0  read  skill://godspeed              (no suffix)  OK (URI)
ev1  read  cohort.py                    :1-220       OK
ev2  read  preregister.json              :1-180       OK
ev3  read  host-tool-boundary.json       :1-160       OK
ev4  read  snapshots.py                  :1-240       OK
ev5  write falsify/FxC3FalseDeath.md      (no suffix)  OK
```
Bucket: path 0, unknown 0, exec 0, total 0. Seat not marked.

### FxC3DuplicateSettlement (23 events; TsukuroiR22.FxC3DuplicateSettlement-2) — seat marked
```
ev0  read  skill://godspeed              (no suffix)  OK (URI)
ev1  read  cohort.py                    (no suffix)  OK
ev2  read  preregister.json              (no suffix)  OK
ev3  read  host-tool-boundary.json       (no suffix)  OK
ev4  read  cohort.py                    :20-140      OK
ev5  read  cohort.py                    :140-260     OK
ev6  read  snapshots.py                  (no suffix)  OK
ev7  read  _revision.py                  (no suffix)  OK
ev8  read  snapshots.py                  :36-175      OK
ev9  read  snapshots.py                  :175-300     OK
ev10 read  seat-boundary-r22.json        (no suffix)  OK
ev11 read  seat-boundary-r22.md          (no suffix)  OK
ev12 grep  cohort.py                    (no suffix)  OK
ev13 read  cohort.py                    :52-80       OK
ev14 read  cohort.py                    :104-124     OK
ev15 grep  snapshots.py                  (no suffix)  OK
ev16 read  cohort.py                    :65-77       OK
ev17 write falsify/FxC3DuplicateSettlement.md (no suffix) OK
ev18 grep  falsify/FxC3DuplicateSettlement.md (no suffix) P
ev19 read  falsify/FxC3DuplicateSettlement.md :-8        P
ev20 edit  falsify/FxC3DuplicateSettlement.md (no suffix) U
ev21 edit  falsify/FxC3DuplicateSettlement.md (no suffix) U
ev22 edit  falsify/FxC3DuplicateSettlement.md (no suffix) U
```
Bucket: path 2, unknown 3, exec 0, total 5. Call_id cardinality 23 for 23 events (no reuse).

### FxC3MissingSettlement (19 events; TsukuroiR22.FxC3MissingSettlement-2)
```
ev0  read  cohort.py                    (no suffix)  OK
ev1  read  preregister.json              (no suffix)  OK
ev2  read  host-tool-boundary.json       (no suffix)  OK
ev3  read  skill://godspeed              (no suffix)  OK (URI)
ev4  read  snapshots.py                  (no suffix)  OK
ev5  read  _revision.py                  (no suffix)  OK
ev6  read  seat-boundary-r22.json        (no suffix)  OK
ev7  read  seat-boundary-r22.md          (no suffix)  OK
ev8  read  cohort.py                    :29-80       OK
ev9  read  cohort.py                    :81-135      OK
ev10 read  cohort.py                    :134-164     OK
ev11 read  snapshots.py                  :1-60        OK
ev12 read  snapshots.py                  :47-130      OK
ev13 read  snapshots.py                  :131-145     OK
ev14 read  snapshots.py                  :244-278     OK
ev15 read  _revision.py                  :1-40        OK
ev16 read  _revision.py                  :62-67       OK
ev17 read  _revision.py                  :69-192      OK
ev18 write falsify/FxC3MissingSettlement.md (no suffix) OK
```
Bucket: path 0, unknown 0, exec 0, total 0. Seat not marked.

### Pack arithmetic (hand-derived, no counter run)
- events 134 = read 111 + grep 11 + write 8 + edit 4 (+ bash 0, glob 0).
- path-checked components 138 (134 events + 4 extra components from the one 5-way `;` split).
- Components in `read_paths`/`write_paths` after `strip_sel`: 135 of 138; offending 3.
- Offending components fall in **3 distinct events** (no event holds 2 offending components) -> the
  one-per-event `break` is arithmetically consistent with a per-component count here.
- Rough buckets for this pack: `path 3`, `unknown 4`, `exec 0`, `sum 7`; seats marked 2
  (FxC3Unresolved, FxC3DuplicateSettlement).
- Path-only (lane-style v1) count for this pack: **3**, i.e. the pack-local rough-minus-path-only gap is
  **4**, produced entirely by the 4 unknown-tool events. Pack-local gap 4 is numerically equal to the
  wave-level falsify gap 33-29 = 4; **this is an arithmetic coincidence candidate, not an established
  mapping** — this pack is group 6 of the falsify wave and its own total (7) is far below the wave total
  (33), so the wave reconciliation cannot be closed from this pack alone.

## 4. Candidate divergence events (seat, event index, call_id, raw suffix, bounded reason)

Each item states what differs between the exact rough cell and a v1 path authority, and what the
consequence would be. Nothing here asserts a v2 rule; v2 edit authority is explicitly out of scope (item C1
states the bound).

**C1 — unknown-tool bucket: 4 events, rough total +4, path +0**
| seat | ev | call_id | raw suffix | bounded reason |
|---|---|---|---|---|
| FxC3Unresolved | 7 | `toolu_017qJKF6VFUbvrJpQFGn3QDQ` | (none) | tool `edit` is not in `('read','grep','glob','write')`, so the cell routes it to `unknown` and never path-checks it. args carry `__unknown_argument__` and no `i`; the target equals `write_paths[0]`, so a v1 checker that path-checks edit-as-write would also record 0. v1 has no edit rule, so no v1 path verdict may be asserted. |
| FxC3DuplicateSettlement | 20 | `call_00_i2tgj6mjk8ymxsasr9gden2p` | (none) | same routing; target equals `write_paths[0]`. |
| FxC3DuplicateSettlement | 21 | `call_01_outb7rxboltcmxe47huj1pe5` | (none) | same routing; target equals `write_paths[0]`. |
| FxC3DuplicateSettlement | 22 | `call_00_tbaqsilgpw8669cvv0hvysng` | (none) | same routing; target equals `write_paths[0]`. |

Bound: the 4-unit pack-local gap is a **category difference**, not four v1 path violations. Relabelling
these as v1 path violations would require a v1 edit rule that the declared old-v1 authority does not state,
and would import r23's new edit-target authority (C1/C2 of the preregister) into frozen r22 history —
excluded by the preregister's separability and "no historical manifest/report rewrite" limit. Under the new
r23 v2 rules these four edits would be red for a *different* reason (write-declared target without read
authority, and `OPAQUE_PATCH`/`READ_ONLY_EDIT` style decisions); that verdict belongs to r23 v2 and must not
be fed back into the v1 arithmetic.

**C2 — read of a write-declared report path: 3 events, path +1 each (the only path violations in the pack)**
| seat | ev | call_id | raw suffix | bounded reason |
|---|---|---|---|---|
| FxC3Unresolved | 8 | `toolu_017qJKF6VFUbvrJpQFGn3QDQ` | `:raw` | `strip_sel` removes `:raw`, leaving `.../round-22/falsify/FxC3Unresolved.md`, which is in `write_paths` but **not** in `read_paths`; the cell tests `read` against `read_paths` only -> path violation. A v1 authority that unions read and write authority (or that treats the seat's own report as implicitly readable) would record 0 instead. |
| FxC3DuplicateSettlement | 18 | `call_00_ej5hvuodqjytjevnkczrm8qw` | (none) | `grep` on `.../falsify/FxC3DuplicateSettlement.md`; no selector, base not in `read_paths` -> path violation; same union-authority caveat. |
| FxC3DuplicateSettlement | 19 | `call_01_uvnmw8myucm39uhlne9k06z8` | `:-8` | `strip_sel` removes `:-8` via the `-\d+` alternative, leaving the same report base -> path violation; same union-authority caveat. |

Bound: these three are the pack's entire path-verdict content. Under the cell they are 3 path units in 3
distinct events; they are *not* additionally re-countable as component units, and they are not the six-unit
wave gap.

**C3 — component order / one-per-event break: 1 event, order-sensitive**
| seat | ev | call_id | raw path | bounded reason |
|---|---|---|---|---|
| FxC3Partial | 10 | `toolu_01BNBRe88HZk15Mv4LWYmBt4` | 5 `;`-joined paths | components in recorded order: `candidate/tools/check-review-cohort.py`; `candidate/tools/check-review-snapshots.py`; `candidate/corpus/knowledge/seat-boundary-r22.md`; `candidate/corpus/knowledge/seat-boundary-r22.json`; `round-22/preregister.json`. All five are in `read_paths`, so the cell's `break` never fires and the event yields 0. A v1 checker that treats the whole `;` string as one path would yield 1; one that splits but counts per component would also yield 0 here. This is the **only** event in the pack where the `;` split and component order are observable at all. |

Bound: the one-per-event `break` is **unexercised** in this pack — no event contains two or more offending
components, so "one-per-event" and "per-component" are numerically identical for all 138 components here.
Any wave-level claim that the break (or component order) moves the rough-vs-lane count must be sourced
outside this pack.

**C4 — selector-normalization width: 7 events where a narrower stripper would flip the verdict**
Rough's `strip_sel` accepts comma lists, `:raw` after a range, a bare `:raw`, and a negative tail. A v1
stripper of narrower width would leave the raw string unstripped and hence outside `read_paths`, turning an
`OK` into a path violation.

| seat | ev | call_id | raw suffix | why the narrow form matters |
|---|---|---|---|---|
| FxC3Partial | 5 | `toolu_018fTRVq1pBeXwrafEami8ce` | `:31-73,85-120,135-160` | comma list: needs `,` inside the range class. |
| FxC3Partial | 9 | `toolu_01LEBE2xesCjxfspmsa2wHbB` | `:4-11,28-29,47-128,131-142` | comma list. |
| FxC3Faulty | 2 | `call_00_u3Z2axoQ8BnzzxeKTpEV8720` | `:1-140:raw` | range **plus** trailing `:raw` (the trailing `(:raw)?` group). |
| FxC3Faulty | 3 | `call_01_QE0eH8tyWbu2QLAU7pyp0534` | `:141-260:raw` | range + `:raw`. |
| FxC3Faulty | 4 | `call_00_ixEmKTTgEvH5I3TUxQl13049` | `:1-160:raw` | range + `:raw`. |
| FxC3Faulty | 6 | `call_00_8U4IaqG80mOHJK2LTf8Y5818` | `:161-278:raw` | range + `:raw`. |
| FxC3Partial | 12 | `toolu_01PWgaUyEM5PGEuxCUZcmQBf` | `:24:raw` | single line + `:raw`. |

Already-violating selector forms (normalization changes the *stated reason*, not the count):
`FxC3Unresolved` ev 8 `:raw`; `FxC3DuplicateSettlement` ev 19 `:-8`.
Robust under any reasonable stripper (single `:N-M` or `:N-M,M-M` forms): the 50-odd remaining
selector-bearing reads in FxC3Clean, FxC3Dead, FxC3MissingSettlement, FxC3DuplicateSettlement,
FxC3FalseDeath, FxC3Partial.

Bound: **normalization is outcome-neutral for 3 of these 7 events only because their bases are already
offending**. For the 7 listed above, the pack's `OK` verdicts are *conditional on the stripper width*, and
this seat cannot certify the lane stripper's width because the lane v1 tool source is outside its declared
read scope.

**C5 — URI-literal read authority: 7 events, compliant only by literal string equality**
| seat | ev | call_id | raw suffix | bounded reason |
|---|---|---|---|---|
| FxC3Clean | 7 | `toolu_016G5vup1cEvVNMcAK145ujN` | (none) | path `skill://godspeed`; `strip_sel` does not alter it (no `:` followed by a matchable selector token at end of string). |
| FxC3Faulty | 0 | `call_00_ET_nQ0v9OMuQDnjVqQciggB7207` | (none) | same. |
| FxC3Dead | 2 | `call_02_ET_VEK9NzUkpeZeqTy47NTJ8155` | (none) | same. |
| FxC3Partial | 0 | `toolu_01TUgC8tzJyYJB3ZRmMMkSYd` | (none) | same. |
| FxC3FalseDeath | 0 | `call_d30fe02c28a94f8c85bce7d88dfed29d\|fc_02a4c1d0bc0b9a2d016ad8d28cd63881918e0fc2ea707172f2` | (none) | same. |
| FxC3DuplicateSettlement | 0 | `call_00_ET_rUES01iq0p3llx8VycGw3620` | (none) | same. |
| FxC3MissingSettlement | 3 | `toolu_017TRUZrvpyS1fYs5BYn2iJy` | (none) | same. |

Bound: each is `OK` only because the seat's `read_paths` literally contains `skill://godspeed` while every
other entry is a filesystem path under the seat root. A v1 authority that requires every read target to be a
filesystem path under `root` (or that resolves URIs) would record 7 path violations in this pack and flip
the pack's path total from 3 to 10. This is a second, independent width-of-authority sensitivity that the
preregister's C3 scope does not yet enumerate.

**C6 — event identity: one call_id spans three events in one seat**
| seat | events | call_id | bounded reason |
|---|---|---|---|
| FxC3Unresolved | 7, 8, 9 | `toolu_017qJKF6VFUbvrJpQFGn3QDQ` | The seat has 10 events but 8 distinct call_ids: the `edit` (ev 7), the `:raw` `read` (ev 8) and the `write` (ev 9) share one call_id, and ev 8/ev 9 carry `request_line: null`. A checker keying violations by call_id instead of by recorded event would attribute this seat's 2 rough units to 1 key (or split them into 1 unknown + 1 path), not 2+1 independent events. |

Bound: this is the concrete reason why "unit" must not be equated with "unique event" in the r23 C3
arithmetic, and it is inside this pack. It is *not* evidence for the wave-level difference.

**C7 — branches of the cell that this pack does not exercise (coverage gaps, not findings)**
- `bash` -> `exec` bucket: 0 events in this pack, so the pack contributes 0 to any `exec` component of the
  rough total. The build-side 2-unit wave gap cannot be attributed from here.
- `glob`: 0 events; its no-strip and `;`-split behaviour is unexercised.
- `write` with a selector suffix: 0 events; the cell's asymmetric "no `strip_sel` for write" branch is
  unexercised (all 8 writes match `write_paths[0]` exactly).
- `read`/`grep` on a path that is in `read_paths` only after a *non-selector* rewrite: 0 events.

## 5. Arithmetic the r23 reconciliation may use from this seat

- Pack rough totals (hand-derived): `path 3`, `unknown 4`, `exec 0`, `sum 7`; 2 of 8 seats marked.
- Pack v1 path-only totals: `3`.
- Pack-local rough-minus-lane gap: **4**, mechanism = unknown-tool bucket (C1) only. No path-verdict
  disagreement exists between the cell and a v1 read/write authority in this pack.
- The wave-level gap the preregister declares is `build 25-23 = 2` and `falsify 33-29 = 4`, total **6**.
  This seat explicitly does **not** assert "six unique events": in this pack the whole 4-unit falsify-side
  gap is one mechanism (4 unknown-tool events) and 3 of the 6 units, if they were ever attributed here, are
  the 3 report-path reads in C2 (a different mechanism). The 6 units must be explained per cohort by
  mechanism, not assumed to be 6 distinct events, and this pack alone cannot close the wave reconciliation
  (pack sum 7 vs wave 33).

## 6. Falsification targets for the r23 C3 record

1. If the r23 C3 record claims the falsify gap of 4 is 4 path violations, this seat's evidence contradicts
   it: in this pack the falsify-shaped gap of 4 is 4 unknown-tool events with 0 path violations.
2. If the r23 C3 record claims the `break`/one-per-event rule or component order moved the counts, this
   seat's evidence contradicts it for this pack: no event has two offending components and only one event
   is multi-path.
3. If the r23 C3 record claims selector normalization is irrelevant, this seat's evidence contradicts it:
   7 events' verdicts are conditional on stripper width (C4), and 7 more are conditional on whether a
   non-filesystem URI can be read-authorized (C5).
4. If the r23 C3 record counts units as events, it will over-count FxC3Unresolved, whose 3 events share one
   call_id (C6).

## 7. Method, limits, and honest gaps

- Executed: nothing. No gate, checker, counter, hash, import, or subprocess was run; the declared digest is
  treated as supplied identity, not independently computed. All figures above are hand-derived from the
  frozen rough cell, the pack's own seat bindings, and the pack's recorded request metadata.
- No tool was installed or updated (this seat's scope is NO-EXEC/NO-FETCH, which forbids installations;
  channel, version and reason are therefore not applicable).
- The v1 authority used for comparison is a **reconstruction** from the frozen rough cell plus the pack
  bindings. The lane's own v1 checker source, the round-22 preregister, and the round-22 bindings.json are
  outside this seat's declared read paths, so I could not confirm: (a) the lane stripper's exact width, (b)
  whether the lane treats a seat's own report path as readable, (c) whether the lane admits `skill://` read
  targets, (d) the lane's event-identity key (event index vs call_id). Items C4, C5, C6 exist precisely
  because those four properties are unresolved from inside the seat.
- The pack's embedded `binding` blocks were used as the seat authority. If the wave's `bindings.json`
  differs from the pack's embedded copies, the membership verdicts in section 3 would change; the pack
  schema states raw preserved request metadata only and does not certify binding equality.
- No v2 rule was applied to v1 history; no new edit permission was imported; no round-24 work was started.
- Report trailer path (relative to the wave root): `.ufo/waves/round-23/build/ReconFalsify06.md`.

Reviewed-SHA256: a46229b596bb665b17aaebb103163c1a39c6cd688a7b37d9a322a572ad9697e3
Predicate: r23-reconfalsify06
Scope: executed=none
