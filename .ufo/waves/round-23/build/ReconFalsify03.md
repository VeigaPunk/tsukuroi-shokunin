# ReconFalsify03 — r23 falsify group 3: rough census vs declared old-v1 path authority

Seat: ReconFalsify03 (leaf). Root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Review target: `.ufo/waves/round-23/packs/falsify-03.json` (8 seats). Supplied digest identity:
`5397c4fc4c99cbe5995ff18801141cbdcc29bb1fe8c94a47da524311f38feba7` — supplied, not recomputed.

Inputs actually read: the pack above; `.ufo/waves/round-23/preregister.json`;
`.ufo/waves/round-23/sources/r22-rough-census.txt`; the Godspeed directive (copied source form).
No shell, command, gate, checker, import, hash, size, unit test, or network access was used.
JSON field reads only; every path-membership decision, `strip_sel` application, and tally below is
hand-derived. Scope receipt: `executed=none`.

Authority convention used here: the pack's per-seat `binding.read_paths` / `binding.write_paths`
are treated as the **declared old-v1 path authority**. The binding schema is observed to have keys
`commands, fetches, name, read_paths, root, write_paths` — there is **no `edit_paths` key**. The
frozen r22 `events.json` / `bindings.json` themselves are outside this seat's declared reads and were
not opened; see Gaps G1/G2.

## 1. What the preserved rough source actually counts

From `sources/r22-rough-census.txt` (interpreted as data, never executed):

```
strip_sel(p) = re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$', '', p)
for w in ['build','falsify']:
  ev, bd = events.json, {name: seat from bindings.json}
  for x in ev['seats']:
    b = bd[x['name']]
    for e in x['events']:
      t, a = e['tool'], e.get('args') or {}
      if t == 'bash':                     exec++;    seats.add(x['name']); continue
      if t not in ('read','grep','glob','write'):
                                          unknown++; seats.add(x['name']); continue
      vals = path.split(';') if t in ('grep','glob') else [path]
      for v in vals:
        q = strip_sel(v) if t in ('read','grep') else v
        if q not in (write_paths if t=='write' else read_paths):
                                          path++; seats.add(x['name']); break
```

Consequences that matter for reconciliation (all derived by reading the source):

- The counting unit is the **event row**, at most **one `path` increment per event**. `break` stops
  the component loop at the **first** mismatching component; later components are never tested.
- Selector normalization applies to `read` and `grep` only. `write` and `glob` are compared
  **exactly**; no selector is stripped.
- `edit` is not in the allowed tool set, so every `edit` row becomes `unknown` before any path is
  examined. Old v1 has no edit authority to consult.
- `bash` is `exec`; no `bash` row exists in this pack, so the pack's `exec` expectation is 0.
- The reported `seats` value is a **set of seat names**, not an event count.
- The printed dict/sum mixes three counters (`exec`, `unknown`, `path`). Only `path` is a path count.

## 2. Declared authority for all eight seats

All eight bindings carry the **same** 8-path read set (one unique read set observed) and one distinct
write path each (8 unique write sets); one root; `commands: []` and `fetches: []` everywhere.
Let `R` be the shared read set:

| code | path (all under ROOT unless noted) |
|---|---|
| CSB  | `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py` |
| PRE  | `.ufo/waves/round-22/preregister.json` |
| HOST | `.ufo/waves/round-22/sources/host-tool-boundary.json` |
| SKILL| `skill://godspeed` |
| CRS  | `.ufo/waves/round-22/candidate/tools/check-review-snapshots.py` |
| REV  | `.ufo/waves/round-22/candidate/tools/_revision.py` |
| SBJ  | `.ufo/waves/round-22/candidate/corpus/knowledge/seat-boundary-r22.json` |
| SBM  | `.ufo/waves/round-22/candidate/corpus/knowledge/seat-boundary-r22.md` |

`W(seat)` is exactly `.ufo/waves/round-22/falsify/<seat>.md`, one per seat.
`FxC2Skill`'s `W` is `.../falsify/FxC2Skill.md`; no seat has read authority for any `falsify/` path.

## 3. Seat roster and hand-derived census expectation (this pack only)

Event index `e` is the 0-based position in `seats[i].events` as recorded in the pack.

| seat | agent | events | tool mix | hand-derived census | flagged |
|---|---|---|---|---|---|
| FxC2Search | TsukuroiR22.FxC2Search-2 | 19 | read 16, grep 1, write 1, edit 1 | `path 0, unknown 1, exec 0` | yes (unknown) |
| FxC2XD | TsukuroiR22.FxC2XD-2 | 20 | read 19, write 1 | `path 1` | yes (path) |
| FxC2Selector | TsukuroiR22.FxC2Selector-2 | 10 | read 9, write 1 | `0` | no |
| FxC2Skill | TsukuroiR22.FxC2Skill-2 | 10 | read 8, edit 1, write 1 | `path 2, unknown 1` | yes (both) |
| FxC2Relative | TsukuroiR22.FxC2Relative-2 | 15 | read 13, grep 1, write 1 | `0` | no |
| FxC2Traversal | TsukuroiR22.FxC2Traversal-2 | 7 | read 6, write 1 | `0` | no |
| FxC2Prefix | TsukuroiR22.FxC2Prefix-2 | 17 | read 12, grep 4, write 1 | `path 1` | yes (path) |
| FxC2Semicolon | TsukuroiR22.FxC2Semicolon-2 | 17 | read 12, grep 3, glob 1, write 1 | `0` | no |

Pack aggregate, hand-derived: **path 4, unknown 2, exec 0, sum 6, seats 4**.
Compliant-row count by subtraction: 109 of 115 rows (18 + 19 + 10 + 7 + 15 + 7 + 16 + 17).
The census's insertion order would print `unknown` before `path` because FxC2Search e18 (unknown) is
reached before FxC2XD e19 (path); that key order is a presentation artifact, not a stable identity.

This is one **group** of the falsify wave, not the wave. It establishes a local expectation of
4 path units; it does not establish the wave's 33-vs-29 figures (Section 7).

## 4. Candidate class N — selector normalization differs from literal authority

`strip_sel` transforms 42 `read` rows. In 40 of them the normalized base is in `R`, so the census
scores them **compliant even though the raw path string is not literally a member of the declared
list**. Under a literal exact-string reading of the same binding, those 40 rows would each be a
`path` unit, making 44 local path units instead of 4. Normalization is therefore verdict-changing for
40 rows, verdict-neutral for 2 rows (both still undeclared after stripping), and irrelevant to the
remaining 2 path units (no selector). All 42 selector-bearing rows are `read`; no `grep`, `glob`, or
`write` row in this pack carries a selector, so `strip_sel` on grep is identity here, and the
glob/write no-strip branches are untested by any selector-bearing row.

Reason codes: **N1** = suffix stripped, base ∈ `R`, census compliant / exact-string would flag;
**N2** = suffix stripped, base ∉ `R` (base is write-only or absent), census path +1 either way.

### FxC2Search (all N1)

| e | call_id | raw suffix | base |
|---|---|---|---|
| 8 | toolu_01T1nXqGYiudr54KGFNJscbg | `:1-80:raw` | CSB |
| 9 | toolu_016YHYuUr6jTvAvashv6ZLSe | `:81-160:raw` | CSB |
| 10 | toolu_01GiXvj8yYAcN2nTAiyqfL1f | `:161-241:raw` | CSB |
| 12 | toolu_01C5nu5rSQuPfKkKPW6tQ2zc | `:1-38:raw` | REV |
| 13 | toolu_015Frhy4QcAiqjYNcrZMebjc | `:62-66:raw` | REV |
| 14 | toolu_01QgdNmZ9GUyLHQBrmMmCb2H | `:98-192:raw` | REV |
| 15 | toolu_011jRgTUMbqGJ9D9faLXkFyu | `:1-30:raw` | CRS |
| 16 | toolu_017H2khTTQrcJwduxbHtPn2x | `:131-143:raw` | CRS |

### FxC2XD (10 × N1, 1 × N2)

| e | call_id | raw suffix | base | code |
|---|---|---|---|---|
| 4 | call_00_aVaa8qm6heCIEMGmKSaz2586 | `:1-70:raw` | CSB | N1 |
| 5 | call_01_Wg6NGcwhM6xbihl3VDGu1737 | `:71-150:raw` | CSB | N1 |
| 6 | call_02_IphnaWFe6n7kbVGZyKOB3011 | `:151-260:raw` | CSB | N1 |
| 11 | call_00_wK3BGBgFxdf85gP7ixxE9067 | `:1-120:raw` | REV | N1 |
| 12 | call_01_YwwP7CusRTSvgVDvretL7821 | `:121-260:raw` | REV | N1 |
| 13 | call_02_WqP3GNvc7tZIDDdHpk3U1324 | `:261-380:raw` | REV | N1 |
| 14 | call_03_JpPb7uDqJid6D8L6Xbwo3655 | `:1-120:raw` | CRS | N1 |
| 15 | call_00_oxlsxy4nv0t92ukrebbctk6l | `:29-60` | CSB | N1 |
| 16 | call_01_wdsw5a4j1q749sqmjxz46g07 | `:105-122` | CSB | N1 |
| 17 | call_02_l9bycko6t9c47r22g1ew172y | `:196-225` | CSB | N1 |
| 19 | call_00_00xyaozzfaapomroplo1yy6q | `:-12` | `falsify/FxC2XD.md` | **N2** |

### FxC2Selector (2 × N1)

| e | call_id | raw suffix | base |
|---|---|---|---|
| 3 | call_00_miQtCugAfYwGWCFEvgo94081 | `:1-140` | CSB |
| 5 | call_00_1bb8HXMMdxJf9s4OL4tY9119 | `:143-241` | CSB |

### FxC2Skill (1 × N2; row also belongs to class U)

| e | call_id | raw suffix | base | code |
|---|---|---|---|---|
| 8 | toolu_01HSUsLHKD2NbFYwef6kMs7U | `:raw` | `falsify/FxC2Skill.md` | **N2** |

### FxC2Relative (7 × N1)

| e | call_id | raw suffix | base |
|---|---|---|---|
| 2 | toolu_016ijL2e4pL4qVVYuhJWjALW | `:1-220` | CSB |
| 3 | toolu_01NDYmcxrRRtF9HxbJn3Rc3b | `:220-440` | CSB |
| 4 | toolu_01GEWpnaf3PSxhsmpQ5MDWss | `:440-660` | CSB |
| 9 | toolu_01FshWaHkfBGUntttiFifPvs | `:1-200` | REV |
| 10 | toolu_017Zqfh8s9saqbK7j3wX5cfr | `:1-200` | CRS |
| 11 | toolu_01QxrHhtujncpEzE6CBDEWk6 | `:200-278` | CRS |
| 12 | toolu_01VW2QemWQDwCCxD2AJDz1fy | `:204-440` | REV |

### FxC2Traversal (5 × N1)

| e | call_id | raw suffix | base |
|---|---|---|---|
| 1 | call_487375dc0c2943a3ae45263faeb834c4\|fc_035baa7b8ff45beb016ad8d29ab0388191825761ed5f31a93d | `:1-240` | CSB |
| 2 | call_2a58a6ae18a04e428b6fc387e840ef9b\|fc_035baa7b8ff45beb016ad8d29cc2888191a652d2dcee2032d8 | `:1-220` | PRE |
| 3 | call_9038e0e16b274c1b876f07b4d0575627\|fc_035baa7b8ff45beb016ad8d29cc28c81918e75ebafefa21506 | `:1-220` | HOST |
| 4 | call_8f67bf1e64b34f93aaa67ea5daa2ea60\|fc_035baa7b8ff45beb016ad8d2b6aa2081919d35f9692ce14545 | `:1-220` | SBJ |
| 5 | call_48b9fc0f6e0847e8babc746201a44021\|fc_035baa7b8ff45beb016ad8d2b7f7dc819180d91c8fbef5ab9a | `:1-220` | SBM |

### FxC2Prefix (4 × N1)

| e | call_id | raw suffix | base |
|---|---|---|---|
| 4 | call_00_JP5i4E26JfIEU9dB6AlD3870 | `:1-140` | CSB |
| 5 | call_01_2CuFnqzmkpiOUQM2ko0B7829 | `:140-260` | CSB |
| 11 | call_00_WvzYb3ZcOc3BOLqB8BYQ6405 | `:155-200` | CSB |
| 12 | call_01_SKmaFa5TJv2S5mejfhIk2397 | `:31-95` | CSB |

### FxC2Semicolon (4 × N1)

| e | call_id | raw suffix | base |
|---|---|---|---|
| 8 | toolu_01EHvJV5LT5U23Uzs6mi4u4r | `:1-120` | CSB |
| 9 | toolu_01X8uhMa8y7P4eR8D15zEFnY | `:121-241` | CSB |
| 10 | toolu_019AY9heMJxNRM2wcp43qn19 | `:1-40,60-70` | REV |
| 13 | toolu_01XzJuDdJrqEmf7PNRgJ6Ugc | `:26-31` | CRS |

Bounded reasons for the 2 N2 rows: in both, the stripped base exists only in `write_paths`; the
declared `read_paths` never contain a `falsify/` path. Normalization therefore does not rescue the
row — it is a `path` unit under both the literal and the normalized reading. `FxC2XD` e19 is a
read-back **after** its write (write at request 57/start 58; read at request 60/start 61).
`FxC2Skill` e8 is a read of the report **before** its write (start 15 vs 16), so no
"read-after-own-write" carve-out unifies the three report reads in Section 6.

Normalization breadth note (INFERENCE, bounded): the regex accepts `+`, commas, nested colons and
repeated hyphens inside the numeric group and never validates that the base exists or the range is
in bounds. In this pack `FxC2Relative` e4 requests `CSB:440-660` while `FxC2Search` e10's own
`CSB:161-241:raw` is the largest observed extent for that file; whether 441–660 exists cannot be
established from the pack and was not probed. Either way the row is normalized compliant, so a
syntactically valid but semantically empty selector is indistinguishable from a real one here.

## 5. Candidate class O — component order and the one-per-event `break`

Only three rows carry more than one path component. Components are checked left-to-right; the count
is capped at one per row and `break` skips the remainder after the first mismatch.

| seat | e | call_id | tool | components in recorded order | all ∈ R | census |
|---|---|---|---|---|---|---|
| FxC2Relative | 13 | toolu_01G4DC7TaEApaA3xBVfsx8Cq | grep | CSB ; REV ; CRS | yes (3/3) | 0 |
| FxC2Semicolon | 14 | toolu_011QimqDuzPJJiSM1FEvZNEn | grep | CRS ; REV ; SBM | yes (3/3) | 0 |
| FxC2Semicolon | 15 | toolu_01LiQwEniR22qvwaiyKM7aYw | glob | CSB ; PRE ; HOST ; CRS ; REV ; SBJ ; SBM | yes (7/7) | 0 |

Hand-derived consequence: 13 component checks over 3 rows, 0 increments under either per-component
or per-event accounting. **Therefore this pack contains no row where the one-per-event cap changes a
count**, and it cannot supply evidence for or against component-level accounting. The cap is real but
unexercised here: had one component of e15 been undeclared, the row would still contribute exactly 1,
and components to its right would never be tested. Order is also inert here because every component
matches. The `glob` row confirms the no-strip branch only vacuously (no component has a selector).

Two non-path anomalies in the same rows, recorded but not countable: `FxC2Relative` e2/e3/e4 overlap at
tokens 220 and 440, so boundary lines appear in two requests; and no component has a dot-segment.

## 6. Candidate class U — per-event vs per-call vs per-start, and `additional-recorded-start`

All duplicate `call_id` values in the pack are confined to `FxC2Skill`, and they coincide exactly with
the three rows the pack marks `origin: "additional-recorded-start"`. Those three rows have
`request_line: null`, `start_lines: null`, a digest but **no `digest_format`**, and (for the write) no
`content` key. The other 112 rows carry `digest_format: "sorted ensure_ascii JSON arguments; not raw
JSONL bytes"`.

Group 1 — `toolu_01Y8GnbHxk2TnQJuzQ1pdMV7`:

| e | role | tool | path | request_line | start_line | origin | census |
|---|---|---|---|---|---|---|---|
| 5 | primary | read | `skill://godspeed` ∈ R | 18 | 14 | — | 0 |
| 6 | additional start | read | `redacted-internal-uri` ∉ R | null | 14 | additional-recorded-start | path +1 |

Group 2 — `toolu_01HSUsLHKD2NbFYwef6kMs7U`:

| e | role | tool | path | request_line | start_line / start_lines | origin | census |
|---|---|---|---|---|---|---|---|
| 7 | primary | edit | `falsify/FxC2Skill.md` ∈ W, ∉ R | 18 | 15, `[15,16]` | — | unknown +1 |
| 8 | additional start | read | `falsify/FxC2Skill.md` + `:raw` | null | 15 | additional-recorded-start | path +1 |
| 9 | additional start | write | `falsify/FxC2Skill.md` ∈ W | null | 16 | additional-recorded-start | 0 |

Unit arithmetic for the six counted units in this pack (all hand-derived):

| unit definition | value | composition |
|---|---|---|
| event rows (the preserved source) | **6** | 4 path + 2 unknown |
| distinct `call_id`s | **5** | group 2 contributes 2 units under one call |
| primary-shape rows only (`origin` absent) | **4** | 2 path + 2 unknown |
| one classification per call | **4–5** | ambiguous: one call carries unknown *and* path |
| distinct flagged seats | **4** | Search, XD, Skill, Prefix |
| additional-start rows among the 6 | **2** | Skill e6, e8 (both path) |
| path-only units | **4** | XD e19, Skill e6, Skill e8, Prefix e16 |

Bounded reason: the preserved source counts event rows, so it necessarily counts the three
additional starts as independent rows. They are not independent tool calls: group 1 shares one start
line (14); group 2 has unique start lines {15, 16} but four row-level start tokens
(`e7:[15,16]`, `e8:15`, `e9:16`). Counting per primary row yields 4; per call yields 4–5; per start
is not well-defined (group 1 ties at start 14; group 2 has four start tokens over two unique starts).
None of these unit choices yields 6.
This is the concrete reason the six local units must not be reported as "six unique events."

Chronology within group 2 (by start line): edit at 15, read at 15, write at 16 — the read is not a
post-write read-back, so any temporal exemption applied to `FxC2XD` e19 / `FxC2Prefix` e16 would not
cover `FxC2Skill` e8. Whether these rows are edit-internal read/write steps rather than policy tool
calls is INFERENCE; the only observed marker is the pack's `origin` label.

## 7. Candidate class E — `edit` is folded to `unknown` before any path check

Old v1 declares only `read_paths` and `write_paths`; there is no edit authority to import.

| seat | e | call_id | recorded args | request/start | census | bounded reading |
|---|---|---|---|---|---|---|
| FxC2Search | 18 | toolu_01U5kGBAhSFfj3bRb73tEFM8 | keys `i`, `__unknown_argument__`; **no path key** | 58 / 59 | unknown +1 | target is unrecoverable; nothing to check; no allow/deny claim is derivable |
| FxC2Skill | 7 | toolu_01HSUsLHKD2NbFYwef6kMs7U | keys `__unknown_argument__`, `path` = `falsify/FxC2Skill.md` | 18 / [15,16] | unknown +1 | target is write-declared only; v1 grants no edit, and no read authority exists for it either |

Do **not** import the r23 v2 edit decisions into these rows: v1 has no edit class, so "declared write
implies edit allowed" and "missing read makes it WRITE_ONLY_EDIT" are both new-policy statements.
The census's `unknown` is the only v1-faithful bucket. `FxC2Search` e18 additionally lacks a target
altogether, so even an edit-aware authority would have to treat it as unknown.

## 8. Write authority, bodies, and the non-flat path

All 8 writes match their seat's single `write_paths` entry exactly; none carries a selector, and the
source does not normalize writes anyway.

| seat | e | call_id | target | exact | body field | origin |
|---|---|---|---|---|---|---|
| FxC2Search | 17 | toolu_01LS7YPbc7TBvrX8fTEdrZFT | `falsify/FxC2Search.md` | yes | `content` present, null | — |
| FxC2XD | 18 | call_00_y9lmc7pnizvhu2f51cq8o4zn | `falsify/FxC2XD.md` | yes | present, null | — |
| FxC2Selector | 9 | call_fb2d28565c0a423698bba4a337402f6d\|fc_087d3b33bb5a5901016ad8d328d6248191b7e9c59db24a4556 | `falsify/FxC2Selector.md` | yes | present, null | — |
| FxC2Skill | 9 | toolu_01HSUsLHKD2NbFYwef6kMs7U | `falsify/FxC2Skill.md` | yes | **absent** | additional-recorded-start |
| FxC2Relative | 14 | toolu_01KbGvbWVqrVALeuLox19wMe | `falsify/FxC2Relative.md` | yes | present, null | — |
| FxC2Traversal | 6 | call_ee20fd2b96134ddfa7e33774ac2bdd89\|fc_035baa7b8ff45beb016ad8d2d31c48819182778f0c258850b0 | `falsify/FxC2Traversal.md` | yes | present, null | — |
| FxC2Prefix | 15 | call_00_yZpXRsQhH6mWkndg9Mpi7166 | `falsify/FxC2Prefix.md` | yes | present, null | — |
| FxC2Semicolon | 16 | toolu_01WXxmhWrtSHbYLUFhaLLx9t | `falsify/FxC2Semicolon.md` | yes | present, null | — |

Body content is not copied (null or absent), and all 9 grep / 1 glob `pattern` values are null, so no
content-level classification is available or attempted; path counting is unaffected.

One recorded path is not a filesystem path and is not resolvable:

- `FxC2Skill` e6, `toolu_01Y8GnbHxk2TnQJuzQ1pdMV7`, read `redacted-internal-uri`.
  Census: `path +1` because the literal string is not in `R`. Bounded reason: the literal is a
  redaction token, not a URI; the real target cannot be recovered from this pack. The only defensible
  statement is "the recorded string is undeclared"; any claim about the actual resource is unsupported.
  It is also an additional-recorded-start row (Section 6).

## 9. Path-shape negatives (what does *not* differ)

- 105 filesystem path strings, all absolute under the declared root; 8 `skill://godspeed` reads; 1
  redaction token; 1 edit row with no path key. Total 114 path-bearing rows of 115.
- No `/../` or `/./` segment, no relative path, no alternate spelling, no backslash, no trailing colon,
  and no `;` on any `read` or `write` path. Dot-segment and expansion classes are inert in this pack.
- No `path: null` on any `read`/`grep`/`glob`/`write` row, so the source's `str(a.get('path',''))`
  cannot manufacture a `"None"` target here. The only missing path is the Search edit, which is
  consumed by the `unknown` branch before path handling.
- No `bash` row; `exec = 0`. Tools present: read 95, grep 9, glob 1, write 8, edit 2.
- All events reference round-22 wave artifacts only; no production tree, VCS state, round-23 file, or
  cross-seat report appears in any recorded path.

## 10. Comparison summary: where the rough algorithm and literal v1 authority differ

| divergence | rows | effect on this pack's counts |
|---|---|---|
| N: selector stripped into `R` | 40 | verdict-changing: literal authority would add 40 path units (44 total vs 4) |
| N: selector stripped, base ∉ `R` | 2 | verdict-neutral: path +1 either way |
| O: multi-component order / one-per-event cap | 3 rows, 13 components | count-neutral here; cap unexercised; no multi-mismatch row |
| U: additional-recorded-start / shared call_id | 3 rows, 2 calls | event 6 vs call 5 vs primary 4 vs seat 4 |
| E: `edit` → `unknown` | 2 | 2 unknown units; no path decision possible under v1 |
| W: writes | 8 | 8/8 exact; body opaque; no normalization exercised |
| X: opaque internal URI | 1 | path +1 on an unrecoverable literal |
| P: Counter/dict insertion order | — | presentation-only; counts stable, key order not |

## 11. Outside-count reconciliation (25/33 rough vs 23/29 lane)

Observed from the preregister: rough build 25 / falsify 33; lane build 23 / falsify 29; deltas 2 and 4.
This pack is falsify **group 3** and yields, hand-derived, **4 path + 2 unknown = 6 units, 4 seats,
5 call_ids**.

- Do not read the six units as six unique events. They are 6 event rows, 5 calls, 4 seats, 4
  primary-shape rows, and only 4 path units; two units are `unknown` (non-path), and two are
  additional-recorded-start rows.
- Do not map the falsify delta of 4 onto these 4 path rows. This pack is one group of the wave; the
  other falsify groups' path units are not in evidence, the lane classifier is not in evidence, and
  two of the four local path units are additional-start rows whose presence in the frozen r22 events
  file is unverified (G1). Magnitude compatibility is not attribution.
- Do not use the local 6 against a path-count delta of 4. If the outside numbers are path-only (the
  preregister's label says path counts), the comparable local figure is 4; if they are census sums,
  they mix `unknown`/`exec` with `path` by construction. The pack cannot distinguish the two readings.
- The build delta of 2 has **zero** candidates here; this pack contains no build seats, and nothing in
  it supports transferring a falsify-unit explanation across waves.
- Normalization is not a plausible wave-scale explanation for a 2-or-4-unit delta: within this group
  alone, normalization suppresses 40 of 44 literal-string path mismatches. A delta smaller than that
  by two orders of magnitude would require offsetting behavior in unseen seats; no such evidence exists
  here.
- Importing v2 edit permissions into old v1 would not change any of the six local units (edits are
  already `unknown`), but it would misdescribe them. Both edit rows must stay `unknown` under v1.

## 12. Gaps (not resolvable from this seat's declared reads)

- **G1 — row-set identity.** The frozen r22 `events.json` / `bindings.json` are outside this seat's
  read set. If the frozen events file did not contain the three `additional-recorded-start` rows, the
  local tally changes from path 4 / unknown 2 (sum 6) to path 2 / unknown 2 (sum 4). This is the single
  largest fork in the reconciliation and remains unverified.
- **G2 — authority identity.** The pack's `binding` arrays are assumed to equal the declared v1 binding
  used by the rough census. A narrower or wider frozen binding would change membership outcomes. Not
  independently checked.
- **G3 — lane unit definition.** The lane's classification/unit rules (per event, per call, per
  component, path-only or sum) are not stated in the pack, and no checker output was consulted.
- **G4 — wave roster.** Only these 8 falsify seats are in evidence; the ship of the other falsify and
  build seats, and therefore any wave-level attribution, is unknown.
- **G5 — extents.** Range validity (e.g., `CSB:440-660`, `REV:261-380`) cannot be established without
  file reads/IO, which this seat does not perform.
- **G6 — digest normalization.** The three additional-start rows carry a digest but no
  `digest_format`, so their argument-digest interpretation is undeclared; no digest was computed here.

No further work is possible within this seat's NO-EXEC / NO-FETCH and declared-read boundary without
the frozen r22 artifacts and the lane definition.

Reviewed-SHA256: 5397c4fc4c99cbe5995ff18801141cbdcc29bb1fe8c94a47da524311f38feba7
Predicate: r23-reconfalsify03
Scope: executed=none
