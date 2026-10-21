# ReconBuild07 — eight-seat build cohort, rough-source vs declared old-v1 authority

Seat: TsukuroiR23-2.ReconBuild07-7. Wave build, group 7, pack `build-07.json`
(declared identity `b160c8c29f8664f1943d1d0ebc55eb737e9c8d527b39f14fea64e42d984aa79e`,
supplied, not recomputed). `executed=none`: no command, fetcher, hash, count utility or
importer was run; every number below is hand-derived from the two declared local sources.

Sources actually opened (all inside the declared read set):
- `.ufo/waves/round-23/packs/build-07.json` (raw preserved request metadata, 8 seats, 74 event records)
- `.ufo/waves/round-23/sources/r22-rough-census.txt` (the exact original rough source cell)
- `.ufo/waves/round-23/preregister.json` (reported 25/33 vs 23/29, C1–C3 scope, edit decisions)
- `skill://godspeed` (occupation directive)

Not opened, not in this seat's read set: round-22 `events.json`/`bindings.json`, any falsify
pack, any lane accounting record. Consequences are stated as gaps in §7, never filled by guess.

## 1. The two things being compared

### 1.1 Exact original rough source (verbatim algorithm, `r22-rough-census.txt`)

```
def strip_sel(p):
  return re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)
for w in ['build','falsify']:
  ev=obj(f'{W}/{w}/events.json'); bd={s['name']:s for s in obj(f'{W}/{w}/bindings.json')['seats']}
  f=collections.Counter(); seats=set()
  for x in ev['seats']:
    b=bd[x['name']]
    for e in x['events']:
      t=e['tool']; a=e.get('args') or {}
      if t=='bash': f['exec']+=1; seats.add(x['name']); continue
      if t not in ('read','grep','glob','write'): f['unknown']+=1; seats.add(x['name']); continue
      vals=str(a.get('path','')).split(';') if t in('grep','glob') else [str(a.get('path',''))]
      for v in vals:
        q=strip_sel(v) if t in('read','grep') else v
        if q not in (b['write_paths'] if t=='write' else b['read_paths']): f['path']+=1; seats.add(x['name']); break
  print(w,dict(f),sum(f.values()),'seats',len(seats))
```

Four properties of that cell drive every candidate below. They are properties of the *source*,
observed, not inferred:

1. **Dispatch order.** `bash` is tested first and `continue`s; the unknown-tool test is second;
   path membership is third. An event is classified by the first branch that fires.
2. **Membership test.** `read`/`grep` are compared against `b['read_paths']` only; `write`
   against `b['write_paths']` only. There is no union, no precedence, no ordering state.
3. **Selector normalisation.** `strip_sel` is applied to `read` and `grep` only, never to
   `write`, and never to `glob`. The regex is anchored at `$` and is leftmost-match, so
   `:N-M:raw` strips whole (`\d[\d\-+,:]*` backtracks to `N-M`, then the optional `(:raw)`
   matches), whereas a hypothetical `:raw:N-M` strips only `:N-M` and leaves a trailing
   `:raw` that cannot equal a declared base path.
4. **Counting unit.** One increment per *event record*: the `path` branch `break`s after the
   first non-member value, so a multi-path event would contribute exactly 1 even if several
   of its paths fail. `sum(f.values())` is therefore a count of flagged **records**, not of
   flagged paths, not of requests, not of call ids, and not of seats.

### 1.2 Declared old-v1 authority (the pack's own `binding` blocks)

All eight bindings have exactly the keys `name, root, read_paths, write_paths, commands,
fetches`; `commands` and `fetches` are empty in every seat; **there is no `edit_paths` key in
any v1 binding**. Each seat declares one or two source read paths, `skill://godspeed`, and
exactly one write path — its own `round-22/build/<Seat>.md`. No seat declares its own report
as a **read** path. [OBSERVED]

## 2. Exhaustive per-seat replay (all 74 records)

Indices are the pack's 0-based `events[]` positions. `sel` = records carrying a selector
suffix; all of them were normalised by hand against the §1.1 regex.

| Seat | records | read | grep | write | edit | bash | selector-bearing reads | clean | exec | path | unknown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| OracleCohortPartial | 12 | 9 | 2 | 1 | 0 | 0 | 5 | 12 | 0 | 0 | 0 |
| OracleCohortBiject | 9 | 8 | 0 | 1 | 0 | 0 | 4 | 9 | 0 | 0 | 0 |
| OracleCohortDuplicate | 6 | 4 | 0 | 1 | 1 | 0 | 1 | 4 | 0 | 1 | 1 |
| OracleCohortFalseDeath | 8 | 7 | 0 | 1 | 0 | 0 | 3 | 8 | 0 | 0 | 0 |
| OracleCohortStrictRed | 11 | 9 | 1 | 1 | 0 | 0 | 5 | 11 | 0 | 0 | 0 |
| OracleCohortDigest | 6 | 5 | 0 | 1 | 0 | 0 | 4 | 6 | 0 | 0 | 0 |
| DebtBash | 7 | 6 | 0 | 1 | 0 | 0 | 2 | 6 | 0 | 1 | 0 |
| DebtFetch | 15 | 8 | 5 | 1 | 0 | 1 | 4 | 14 | 1 | 0 | 0 |
| **Totals** | **74** | **56** | **8** | **8** | **1** | **1** | **28** | **70** | **1** | **2** | **1** |

Tool totals match an independent pack-wide grouping exactly (read 56, grep 8, write 8, edit 1,
bash 1); the replay therefore accounts for every record, with none dropped and none double
counted. Hand-derived expectation for this pack under the exact rough source: `{'exec': 1,
'path': 2, 'unknown': 1}`, `sum = 4`, `seats = 3`.

Selector-class census of the 28 selector-bearing reads (all reduce to their declared base,
26 of them landing in `read_paths` and 2 failing the base membership shown in §3):
- `:N-M` plain range — 14 (Partial e2,e3; Biject e4–e7; FalseDeath e4,e5; StrictRed e7,e8; Digest e1–e4)
- `:N-M:raw` range-then-raw — 8 (Partial e8–e10; StrictRed e4–e6; DebtFetch e7,e9)
- `:a,b,c:raw` comma-list-then-raw — 3 (FalseDeath e6; DebtFetch e8,e10)
- `:raw` bare — 2 (Duplicate e4; DebtBash e4)
- `:-N:raw` tail-then-raw — 1 (DebtBash e6)

No record in this pack carries `?q=`, `%3A`, a dot-segment, an alternate spelling, or more
than one `;`-separated path (a pack-wide `contains(";")` check on path values returns 0), so
the `break` in the `path` branch never suppresses a second component here.

## 3. Candidate components where normalisation or order differs

Four records, exhaustively — these are the only records whose classification is sensitive to
the rough cell's dispatch order, membership list, or record-identity handling. Everything
else is invariant across the classes below.

### C-1 — OracleCohortDuplicate, event index 3
- `tool`: `edit` · `call_id`: `toolu_015tSz2JMMi9eYMAmfqdWnaf` · request_line 15, start_line 12, start_lines [12,13]
- raw path: `…/.ufo/waves/round-22/build/OracleCohortDuplicate.md` — **suffix: none**
- args: `{"path": …, "__unknown_argument__": null}` · recorded digest `c3309b2f76b0da4eb038c81fef95e9381e15c751322cf95ca90a133bba1f2c3f`
- v1 category: **unknown**. Bounded reason: `edit` is not in `('read','grep','glob','write')`,
  so the second branch fires before the path is ever examined. The single path it names is a
  declared **write** path, so the record is not a path violation in substance either; the red
  is purely a missing tool branch. The `__unknown_argument__` sentinel marks the call's body
  as unparsed, so the structured edit target is not recoverable from this metadata.

### C-2 — OracleCohortDuplicate, event index 4
- `tool`: `read` · `call_id`: `toolu_015tSz2JMMi9eYMAmfqdWnaf` (same call as C-1) · request_line **null**, start_line 12, `origin: "additional-recorded-start"`
- raw path: `…/.ufo/waves/round-22/build/OracleCohortDuplicate.md:raw` — **suffix `:raw`**
- recorded digest `317a70cb6536fa03e7e198aea1ddf2eedc0ee108a44c9564ce9bd3c94b49f8c9`
- v1 category: **path**. Bounded reason: `:raw` strips cleanly to the base, then base ∉
  `read_paths` (it exists only in `write_paths`) → membership fails. Order-sensitive: this
  read start is a derivation of the *edit* call, recorded after that call's own write start,
  and its authority is checked statelessly against the read list with no knowledge that the
  seat itself had just produced the file.

### C-3 — DebtBash, event index 6
- `tool`: `read` · `call_id`: `call_00_2hSTsiM0i5bcqrJM6Nby0686` · request_line 28, start_line 29
- raw path: `…/.ufo/waves/round-22/build/DebtBash.md:-6:raw` — **suffix `:-6:raw`**
- recorded digest `7efb137abd8fc2cc940e3586b486b74f6d26c45bf22b06a9ea4aac598aeee1cb`
- v1 category: **path**. Bounded reason: the leftmost colon is the one before `-6`; the
  `-\d+` alternative consumes `-6` and the optional `(:raw)` consumes `:raw`, so the whole
  suffix strips and the base is `…/build/DebtBash.md`. Base ∉ `read_paths` (write-only) →
  membership fails. Ordering: this is a genuine, separately-called post-write self-read — the
  seat wrote that exact path at event 5 (`call_00_6yfQhUMc6NLbcJdN4fhg4711`) and read it back
  six lines from the end.

### C-4 — DebtFetch, event index 5
- `tool`: `bash` · `call_id`: `call_01_9Ya6CQp0DQzKikwG1uKD3940` · request_line 22, start_line 24
- args: `{}` — **suffix: none; no path value exists** · recorded digest `76099b45f22254e17efad2b144732d1e4c38e0a6eee5bfaf35efad8ba3f9843c`
- v1 category: **exec**. Bounded reason: dispatch order — the `bash` branch increments `exec`
  and `continue`s before any path branch, so the record's authority content is never examined.
  With `args == {}` the path expression would have yielded `''` had the order been reversed,
  which would have produced a *path* increment instead. The command body itself is not present
  in the preserved metadata, so no path verdict — clean or red — is derivable for this call.
  This is an order-sensitive category assignment with a fixed sum.

Bounded negative result: no candidate arises from the numeric/raw/comma/csv selector classes
themselves (all 28 normalise exactly as the source intends), and no candidate arises from the
`break` suppression (no multi-path events). The latent failure class `:raw:N-M` (raw **before**
the range) is real in the regex but **unexercised in this pack**; it would mis-normalise an
otherwise declared read into `base:raw` and flag it. Any reconciliation that claims to have
covered "selector forms" must therefore record that this class was not instantiated here.

## 4. Record identity vs the "six unique events" temptation

The unit of count is unstable across three plausible keys, and the pack proves it internally:

- **event records**: 74
- **distinct `call_id`**: 72 — `toolu_015tSz2JMMi9eYMAmfqdWnaf` appears three times
  (Duplicate e3 `edit`, e4 `read`, e5 `write`); every other call id is unique in this pack.
- **records with non-null `request_line`**: 72 — Duplicate e4 and e5 carry
  `request_line: null` with `origin: "additional-recorded-start"`; those two are recorded
  *starts* derived from the edit call, not independent requests.
- **seats**: 8.

Consequences, all derived from the above and none requiring a run:
- Flagged **records** = 4; flagged **call ids** = 3 (C-1 and C-2 collapse); flagged **seats** = 3
  (Duplicate, DebtBash, DebtFetch). A call-keyed lane and a record-keyed lane disagree by 1 on
  this pack before any rule about authority is applied.
- A request_line-keyed lane drops Duplicate e4 (flagged) and e5 (clean) outright, silently
  removing one path component.
- C-1/C-2/C-3 share a single file: the edit, its derived read start, and its write start all
  target `round-22/build/OracleCohortDuplicate.md`; the write record is the only one of the
  eight writes in the pack whose args lack `content` (all seven real writes carry
  `{content,i,path}`), which corroborates that it is a derived, body-less start.

Therefore "six unique events" is **not** a safe restatement of a 2 + 4 differential: the two
deltas need not share a unit, and inside this pack alone the same 4 components can be counted
as 4, 3 or 2 depending on key choice. The only defensible unit statement is the one the source
itself prints: flagged **records** per wave.

## 5. Rough-vs-lane arithmetic, bounded

Given outside totals (preregister, ground truth): rough build 25 / falsify 33; lane build 23 /
falsify 29. Deltas: build **2**, falsify **4**, naive sum **6**.

Hand-derived facts bearing on the build delta:
- This pack's full v1 expectation is 4 flagged records — **more than the entire build delta of
  2**. Build 23 is therefore *not* "rough 25 minus these 4". At least 2 of the 4 records here
  must be congruent between the two totals (present in both 25 and 23), or the lane's unit is
  narrower than the rough's. Either way, no accounting can attribute the build delta to this
  pack wholesale.
- The only magnitude-2 subset inside this pack is {C-2, C-3}: both are **path** components, both
  are reads of the seat's *own declared draft*, both fail for one single reason — the v1
  membership test consults `read_paths` alone while the draft lives only in `write_paths`. If
  the lane reconciles reads against `read_paths ∪ write_paths` (or exempts a seat's own
  declared write target), build 25 → 23 with exactly those two removals. [INFERENCE]
- That fit is a coincidence of magnitude until the lane record is read; it is not attribution.
  The remaining two components here (C-1 unknown, C-4 exec) would then have to be congruent in
  both totals — which is consistent with a lane that still counts exec and unknown reds, and
  inconsistent with a lane that counts only path components.
- Competing reading: if the lane number counts only the `path` category while the rough's
  `sum(f.values())` mixes exec + path + unknown, the build differential is again a
  path-category difference of 2, C-2/C-3 are the only path components this seat can offer, and
  C-1/C-4 are structurally outside the lane unit. Under this reading the falsify delta of 4 is
  likewise a path-category difference and cannot be added to a build delta that also excludes
  exec/unknown without mixing units.
- Third, insufficient contributor: a call-keyed lane collapses C-1+C-2 to 1, moving the build
  mix by 1 — not 2, and it would also move the denominator of 23, so it cannot by itself
  account for the delta.

What this seat will not assert: that the build delta is these two records; that the total of 6
is six distinct events; that any component here was mis-classified by the rough cell. The rough
cell's output for this pack is exactly `exec 1, path 2, unknown 1, sum 4, seats 3`, and that is
the whole hand-derived expectation.

## 6. Old-v1 permission discipline

No new edit authority is imported into old v1 anywhere in this report.
- C-1 stays **unknown**. Making it clean would require adding an `edit` branch and an
  `edit_paths` authority to a *historical* binding that declares neither — a retroactive
  permission grant, which the preregister's limits forbid ("No historical manifest/report
  rewrite or retrospective authorization").
- Even the round-23 v2 decision table would not bless it: `DECLARED_EDIT` requires the target
  predeclared for edit **and** for both read and write; here the target is write-only, which is
  `WRITE_ONLY_EDIT → DENY`, and the `__unknown_argument__` body is `OPAQUE_PATCH → UNKNOWN`.
  The historical event is therefore red-adjacent under both authorities, for different reasons.
- C-2 and C-3 stay **path** flags. Explaining them as an authority-scope artifact is a
  count reconciliation, not a reclassification: C3's scope is explanation of rough-versus-lane
  counts and "does not relabel old violations".
- C-4 stays **exec**; the command body is absent from the preserved metadata, so neither v1 nor
  v2 can produce a path verdict for it, and no claim of runtime enforcement or effect is made.

## 7. Remaining unknowns (gaps, not conclusions)

1. **Lane unit and denominator.** No lane accounting record is in this seat's read set. That
   single fact decides between the union-membership reading and the path-only-category reading
   of §5. Unresolved here by scope, not by omission.
2. **Falsify side.** No falsify pack is readable here; the falsify delta of 4 has zero
   observations from this seat. Any claim of "six events" would be half-unfounded.
3. **Other build groups.** This pack is group 7 only; whether the true build delta lives wholly,
   partly or not at all in these three seats cannot be decided from one group.
4. **Historical binding identity.** I replayed against the bindings the pack reproduces. Whether
   round-22's own `bindings.json` is byte-identical was not checkable (outside read set); the
   pack declares raw preserved metadata, which I treated as authoritative source data.
5. **Latent selector class.** `:raw:N-M` is unexercised here; its presence or absence in other
   packs is unknown to this seat.

## 8. Handoff

For the reconciliation record that consumes this seat: the build-group-7 arithmetic anchor is
`exec 1 / path 2 / unknown 1 = 4 records, 3 call ids, 3 seats`, with the only magnitude-2
subset being the two self-draft reads (C-2, C-3) whose shared cause is the read/write
authority split in `strip_sel`'s caller, not the selector regex. C-1 and C-4 must be carried as
congruent reds, not as delta, unless the lane record says otherwise. No gate or counter was run;
these are source expectations only.

Lane bounds (informational, not a receipt field): leaf member — no subagent dispatch.

Reviewed-SHA256: b160c8c29f8664f1943d1d0ebc55eb737e9c8d527b39f14fea64e42d984aa79e
Predicate: r23-reconbuild07
Scope: executed=none
