# ReconBuild08 — r22 build-wave pack group 8: rough-vs-lane path-count reconciliation (hand-derived)

Scope: the eight named round-22 seats in `.ufo/waves/round-23/packs/build-08.json`
(`DebtSixReceipts`, `CritSeparable`, `CritNoHarm`, `CritRuntime`, `SentinelMetadata`,
`ReviewReservation`, `ReviewScopeTrailer`, `ReviewSources`).
Contribution target: C3 (calibration) — exhaustive per-event/component explanation of
rough-versus-lane path counts over frozen r22 evidence. No new C1/C2 content read or used.

Axes touched by this seat: calibration (count reconciliation), coverage (per-event ledger
completeness), freshness (none — frozen r22 inputs only), operability (none).

Method: pure hand-derivation from the pack's raw preserved request metadata, the recorded
rough census source (`sources/r22-rough-census.txt`), and the declared old-v1 seat
authorities carried in the pack. **No command, hash, import, run, or fetch was performed.**
The pack digest `bf44df672b524bc234fe5e7f72cd648d3ecd66cc9d71e8fd8ed3da6e2805cd29` is
treated as supplied identity, not independently computed.

---

## 1. Declared old-v1 authority per seat (verbatim from pack binding)

| seat | agent | read_paths (v1) | write_paths (v1) |
|---|---|---|---|
| DebtSixReceipts | TsukuroiR22.DebtSixReceipts-3 | r21.md; round-22/preregister.json; round-22/sources/host-tool-boundary.json; skill://godspeed | round-22/build/DebtSixReceipts.md |
| CritSeparable | TsukuroiR22.CritSeparable-3 | round-22/sources/boundary-contract.json; round-22/preregister.json; round-22/sources/host-tool-boundary.json; skill://godspeed | round-22/build/CritSeparable.md |
| CritNoHarm | TsukuroiR22.CritNoHarm-3 | round-22/snapshot/corpus/QUALITY.md; round-22/preregister.json; round-22/sources/host-tool-boundary.json; skill://godspeed | round-22/build/CritNoHarm.md |
| CritRuntime | TsukuroiR22.CritRuntime-3 | round-22/sources/host-tool-boundary.json; round-22/preregister.json; skill://godspeed | round-22/build/CritRuntime.md |
| SentinelMetadata | TsukuroiR22.SentinelMetadata-3 | round-22/snapshot/.ufo/waves/round-21/measure/seat-tool-audit.json; round-22/preregister.json; round-22/sources/host-tool-boundary.json; skill://godspeed | round-22/build/SentinelMetadata.md |
| ReviewReservation | TsukuroiR22.ReviewReservation-3 | r21.md; round-22/preregister.json; round-22/sources/host-tool-boundary.json; skill://godspeed | round-22/build/ReviewReservation.md |
| ReviewScopeTrailer | TsukuroiR22.ReviewScopeTrailer-3 | round-22/snapshot/tools/check-seat-scope.py; round-22/preregister.json; round-22/sources/host-tool-boundary.json; skill://godspeed | round-22/build/ReviewScopeTrailer.md |
| ReviewSources | TsukuroiR22.ReviewSources-3 | round-22/sources/boundary-contract.json; round-22/preregister.json; round-22/sources/host-tool-boundary.json; skill://godspeed | round-22/build/ReviewSources.md |

`commands` and `fetches` are empty for every seat in this pack.

## 2. The exact original rough algorithm (transcribed from `sources/r22-rough-census.txt`)

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

Behavioural properties that drive every difference below:

- **P1 (selector normalization).** `strip_sel` removes at most **one** trailing selector
  group. `(:raw)?` may only be consumed as part of the *same* match, so a compound selector
  `:raw:58-58` is reduced to `:58-58` and the leading `:raw` **survives** → result
  `…/round-21.md:raw`. `strip_sel` is applied to `read` and `grep` only; **`glob` and
  `write` paths are never stripped.**
- **P2 (component split scope).** Only `grep` and `glob` split their `path` on `;`.
  `read` and `write` compare the raw string as a single component.
- **P3 (one-per-event break).** The `break` fires on the **first** non-declared component,
  so one event contributes **at most one** to `f['path']`, regardless of how many components
  violate.
- **P4 (authority split).** `write` is checked against `write_paths`; every other audited
  tool is checked against `read_paths`. A path that is a declared **write** target is **not**
  a legal **read** target under v1.
- **P5 (tool taxonomy).** `bash` → `exec`; anything outside
  `('read','grep','glob','write')` — notably `edit` — → `unknown`; only the four audited
  tools can produce a `path` count.
- **P6 (counter ambiguity).** The census prints `dict(f)`, `sum(f.values())` **and**
  `'seats', len(seats)`. The preregister reports only one pair of numbers per lane
  ("rough build 25 / falsify 33", "lane build 23 / falsify 29"). Whether those figures are
  `f['path']` alone or `sum(f.values())` (which also absorbs `exec` and `unknown`) is **not
  declared anywhere in the declared inputs** and materially changes the reconciliation.

## 3. Per-event ledger for all eight seats (rough classification, hand-derived)

`V` = rough `f['path']` count (violation); `U` = rough `f['unknown']` bucket;
`—` = clean under declared v1 authority. Event index is 0-based within the seat's
`events` array, in pack order.

### 3.1 DebtSixReceipts (6 events)
| idx | tool | call_id | raw path suffix | rough | reason |
|---|---|---|---|---|---|
| 0 | read | call_35763651453349ed92d5727e | `skill://godspeed` | — | no `:`-suffix match; equals declared read path |
| 1 | read | call_8c19566ca27642bfb4853e57 | `…/round-21.md` | — | declared read path |
| 2 | read | call_0c3c1faf62424b0fbf291662 | `…/round-22/preregister.json` | — | declared read path |
| 3 | read | call_4c066b3dfdfc4bf585198d21 | `…/round-22/sources/host-tool-boundary.json` | — | declared read path |
| 4 | read | call_2824ccfabf13434f969518b5 | `:raw:58-58` | **V** | strip_sel leaves `…/round-21.md:raw`; not a member of `read_paths` (P1) |
| 5 | write | call_91f664012dc34665a3e886d5 | — | — | equals declared write path |

### 3.2 CritSeparable (8 events)
| idx | tool | call_id | raw path suffix | rough | reason |
|---|---|---|---|---|---|
| 0 | read | toolu_01LFaDMg6njVAqRHTFFRMKdu | — | — | declared read path (`boundary-contract.json`) |
| 1 | read | toolu_01A3MMeokdNGtDJpABkxhAS7 | — | — | declared read path |
| 2 | read | toolu_01DukrQrC57RkkPoa8GT4jFb | — | — | declared read path |
| 3 | grep | toolu_014RQUGKh4MpLcsPbjwdscsd | — | — | single component, declared read path |
| 4 | grep | toolu_01Xs2w2fypZApRp7kdhBWWZ9 | — | — | single component, declared read path |
| 5 | edit | toolu_01K98z2EYvWyDkpSct3PH9Yd | — | **U** | P5: `edit` is not audited; path itself is the declared write path |
| 6 | read | toolu_01K98z2EYvWyDkpSct3PH9Yd (`origin: additional-recorded-start`) | `:raw` | **V** | strip_sel → `…/build/CritSeparable.md`, a declared **write** path only → not in `read_paths` (P4) |
| 7 | write | toolu_01K98z2EYvWyDkpSct3PH9Yd (`origin: additional-recorded-start`) | — | — | equals declared write path |

### 3.3 CritNoHarm (6 events)
| idx | tool | call_id | raw path suffix | rough | reason |
|---|---|---|---|---|---|
| 0 | read | toolu_01Y1QvFeNkqU5vXxLuz6KYvw | — | — | declared read path (`QUALITY.md`) |
| 1 | read | toolu_01BUX7RQANRaHcbraAJruey2 | — | — | declared read path |
| 2 | read | toolu_01MgPeZov9A6EHvL7LZTtzst | — | — | declared read path |
| 3 | edit | toolu_01PLKzcS4ozjJ1wt2L5DM8oY | — | **U** | P5 |
| 4 | read | toolu_01PLKzcS4ozjJ1wt2L5DM8oY (`origin: additional-recorded-start`) | `:raw` | **V** | strip_sel → `…/build/CritNoHarm.md` = declared write path only → not in `read_paths` (P4) |
| 5 | write | toolu_01PLKzcS4ozjJ1wt2L5DM8oY (`origin: additional-recorded-start`) | — | — | equals declared write path |

### 3.4 CritRuntime (7 events)
| idx | tool | call_id | raw path suffix | rough | reason |
|---|---|---|---|---|---|
| 0 | read | toolu_01XrBgZbthPUE18NQ5ZVHDV5 | — | — | declared read path |
| 1 | read | toolu_01EH2DRWnYVXGbUbGB3K4yHt | — | — | declared read path |
| 2 | read | toolu_01RJ3iknqAefXg8aVWoGH95y | `skill://godspeed` | — | declared read path |
| 3 | read | toolu_01RJ3iknqAefXg8aVWoGH95y (`origin: additional-recorded-start`, `request_line: null`, `start_line: 11`) | `redacted-internal-uri` (whole value) | **V** | non-filesystem/redacted token; `strip_sel` leaves it unchanged; not a member of `read_paths` |
| 4 | edit | toolu_014nToY7USd3cckcqeieNJ4o | — | **U** | P5 |
| 5 | read | toolu_014nToY7USd3cckcqeieNJ4o (`origin: additional-recorded-start`) | `:raw` | **V** | strip_sel → `…/build/CritRuntime.md` = declared write path only → not in `read_paths` (P4) |
| 6 | write | toolu_014nToY7USd3cckcqeieNJ4o (`origin: additional-recorded-start`) | — | — | equals declared write path |

### 3.5 SentinelMetadata (0 events)
No recorded events; contributes nothing to any counter and is not added to the rough `seats` set.

### 3.6 ReviewReservation (7 events)
| idx | tool | call_id | raw path suffix | rough | reason |
|---|---|---|---|---|---|
| 0 | read | call_d74821c3d389459d887cb582 | `skill://godspeed` | — | declared read path |
| 1 | read | call_86a6311f9206410c96861ebe | — | — | declared read path (`…/round-21.md`) |
| 2 | read | call_2ddc0091f40c49789ec35634 | — | — | declared read path |
| 3 | read | call_f3721e91ba0845ea99960f65 | — | — | declared read path |
| 4 | read | call_a6b2165b628a4b4283fde50c | `:raw:58-58` | **V** | strip_sel leaves `…/round-21.md:raw`; not in `read_paths` (P1) |
| 5 | read | call_83fe2ec6df41480d84b61a71 | `:59-146` | — | strip_sel → `…/round-21.md` = declared read path |
| 6 | write | call_9b57999576034c198d7706450d3de065\|fc_0caf22dfa49af16f016ad8d0895be0819180d15bf088f81122 | — | — | equals declared write path |

### 3.7 ReviewScopeTrailer (12 events)
| idx | tool | call_id | raw path suffix | rough | reason |
|---|---|---|---|---|---|
| 0 | read | call_274d650bec6e4c11a9933aad | `skill://godspeed` | — | declared read path |
| 1 | read | call_4409589fba0048f4af7caa97 | — | — | declared read path (`…/snapshot/tools/check-seat-scope.py`) |
| 2 | read | call_e87f1e1146864712bc3dc8fc | — | — | declared read path |
| 3 | read | call_9db53022a4244dceb137dc84 | — | — | declared read path |
| 4 | read | call_d6eb84cf3bab40acb99b9571 | `:1-60` | — | strip_sel → declared read path |
| 5 | read | call_3ab248174c0846858ba95601 | `:60-160` | — | strip_sel → declared read path |
| 6 | read | call_237671e012ea47e890debbfe | `:160-260` | — | strip_sel → declared read path |
| 7 | read | call_607293477cef43f3b74b8ef4 | `:260-360` | — | strip_sel → declared read path |
| 8 | read | call_97641fd369a244cdab3c7f | `:360-470` | — | strip_sel → declared read path |
| 9 | read | call_e19e67c395734c3a84dcd96d | `:470-560` | — | strip_sel → declared read path |
| 10 | read | call_a78a387305ed4909967ebd0b | `:564-673` | — | strip_sel → declared read path |
| 11 | write | call_501b3eec392e4c97be2e5838d5f6c1dc\|fc_08fc6b032cfe3144016ad8d0a9faec8191af63aeafb2ef9d59 | — | — | equals declared write path |

### 3.8 ReviewSources (5 events)
| idx | tool | call_id | raw path suffix | rough | reason |
|---|---|---|---|---|---|
| 0 | read | call_b568f6d61e884dbfa6a78f03 | `skill://godspeed` | — | declared read path |
| 1 | read | call_37eb42b6c7c845d180ab3141 | — | — | declared read path (`boundary-contract.json`) |
| 2 | read | call_672aecfdfdc5449db2bd498d | — | — | declared read path |
| 3 | read | call_50b652d021e5474783f19013 | — | — | declared read path |
| 4 | write | call_091ca0d199b34c82bfe2fde0 | — | — | equals declared write path |

### 3.9 Group totals under the rough algorithm
`f['path'] = 6` · `f['unknown'] = 3` · `f['exec'] = 0` · `sum(f.values()) = 9` ·
rough `seats` set = 5 ({DebtSixReceipts, CritSeparable, CritNoHarm, CritRuntime, ReviewReservation}).
The six `path` events are exactly: DebtSixReceipts#4, CritSeparable#6, CritNoHarm#4,
CritRuntime#3, CritRuntime#5, ReviewReservation#4.
The three `unknown` events are exactly: CritSeparable#5, CritNoHarm#3, CritRuntime#4.

---

## 4. Candidate divergence rows (rough algorithm vs declared old-v1 lane authority)

Nine distinct candidate events. Every row states the mechanism, the direction it moves the
count, and the bounded reason. **No row asserts that the lane resolves it the way the rough
source does** — the lane tool's source is outside this seat's declared read authority (see §6).

| # | seat | event idx | call_id | raw path suffix | mechanism | rough | lane, if it differs | bounded reason |
|---|---|---|---|---|---|---|---|---|
| C-α1 | DebtSixReceipts | 4 | call_2824ccfabf13434f969518b5 | `:raw:58-58` | selector normalization (P1) | V | clean | rough strips one group and leaves `:raw`, producing `…/round-21.md:raw`, which is not the declared read path `…/round-21.md`; a lane that normalizes the whole selector chain to the bare path resolves to the declared path |
| C-α2 | ReviewReservation | 4 | call_a6b2165b628a4b4283fde50c | `:raw:58-58` | selector normalization (P1) | V | clean | identical residue as C-α1 on the same declared read path `…/round-21.md` |
| C-β1 | CritSeparable | 6 | toolu_01K98z2EYvWyDkpSct3PH9Yd | `:raw` | adapter-step accounting | V | may not exist as a separate counted event | `origin: additional-recorded-start`; shares the parent `call_id` with the `edit` at idx 5; a lane that keys on call/request identity collapses it into the parent request |
| C-β2 | CritNoHarm | 4 | toolu_01PLKzcS4ozjJ1wt2L5DM8oY | `:raw` | adapter-step accounting | V | may not exist as a separate counted event | as C-β1, parent `edit` at idx 3 |
| C-β3 | CritRuntime | 5 | toolu_014nToY7USd3cckcqeieNJ4o | `:raw` | adapter-step accounting | V | may not exist as a separate counted event | as C-β1, parent `edit` at idx 4 |
| C-β4 | CritRuntime | 3 | toolu_01RJ3iknqAefXg8aVWoGH95y | `redacted-internal-uri` | adapter-step accounting / non-filesystem token | V | may not exist as a separate counted event, or may not be a path at all | `origin: additional-recorded-start`, `request_line: null`, same `start_line: 11` as the parent `read skill://godspeed` at idx 2; the value is a redacted internal URI, not a filesystem path, so a lane that audits only filesystem paths would not count it |
| C-γ1 | CritSeparable | 6 | toolu_01K98z2EYvWyDkpSct3PH9Yd | `:raw` | authority split (P4) | V | clean only if the lane admits declared-write targets for reads | target is the seat's own declared **write** path `…/build/CritSeparable.md`; under the declared old-v1 authority as written it is **not** in `read_paths`. This row must **not** be closed by importing any new edit permission: the r23 v2 decision set keeps `WRITE_ONLY_EDIT → DENY`, so a v1 read of a write target remains a v1 violation. It is listed only as a *candidate classifier difference* for the C3 record |
| C-γ2 | CritNoHarm | 4 | toolu_01PLKzcS4ozjJ1wt2L5DM8oY | `:raw` | authority split (P4) | V | as C-γ1 | as C-γ1, target `…/build/CritNoHarm.md` |
| C-γ3 | CritRuntime | 5 | toolu_014nToY7USd3cckcqeieNJ4o | `:raw` | authority split (P4) | V | as C-γ1 | as C-γ1, target `…/build/CritRuntime.md` |
| C-ε1 | CritSeparable | 5 | toolu_01K98z2EYvWyDkpSct3PH9Yd | — | tool taxonomy (P5) | U | write-checked, clean | `edit` falls into the rough `unknown` bucket and therefore contributes to `sum(f.values())` but never to `f['path']`; the edit target is the declared write path, so a lane that classifies `edit` as a write finds no violation |
| C-ε2 | CritNoHarm | 3 | toolu_01PLKzcS4ozjJ1wt2L5DM8oY | — | tool taxonomy (P5) | U | write-checked, clean | as C-ε1 |
| C-ε3 | CritRuntime | 4 | toolu_014nToY7USd3cckcqeieNJ4o | — | tool taxonomy (P5) | U | write-checked, clean | as C-ε1 |

Structural mechanisms that this pack does **not** exercise (zero rows here — they must be
covered by the other round-23 build/falsify packs, and are named here so the C3 record does
not over-claim completeness from this group alone):

- **C-ζ (component split / per-component counting).** No `grep` or `glob` event in this pack
  carries a `;`-separated multi-component path, so the P2 split scope and the P3
  one-per-event break cannot diverge here. A lane that counts *components* rather than
  *events* would diverge on such rows.
- **C-η (glob selector non-stripping).** `strip_sel` is not applied to `glob` (P1); no `glob`
  event exists in this pack.
- **C-θ (exec bucket).** No `bash` event exists in this pack; `f['exec'] = 0` here.
- **C-ι (counter semantics).** The preregister's "path_counts_as_reported" does not state
  whether the reported 25/33 is `f['path']` or `sum(f.values())`. If it is the total, the
  three `edit` rows (C-ε1..3) enter the arithmetic as well, and this group's rough total
  becomes 9 rather than 6.

---

## 5. Arithmetic reconciliation against the outside totals (no new assumptions)

Outside ground truth (preregister `outside_round22.path_counts_as_reported`): rough build 25 /
falsify 33; lane build 23 / falsify 29 → gaps of **2** (build) and **4** (falsify), total 6.

Observed in this group: rough `f['path'] = 6` across 5 seats, plus 3 `unknown` events, in
**9 candidate events**.

Candidate partition P1 (each row of §4 used at most once), consistent with the outside gaps:

| outside gap | candidate subset | magnitude | preconditions |
|---|---|---|---|
| build 25 → 23 (2) | {C-α1, C-α2} | 2 | the lane normalizes the whole selector chain, so the two `:raw:58-58` reads resolve to their declared read path; DebtSixReceipts and ReviewReservation sit in the **r22 build** lane |
| falsify 33 → 29 (4) | {C-β1, C-β2, C-β3, C-β4} | 4 | the lane collapses `additional-recorded-start` adapter steps (or does not treat a redacted internal URI as a filesystem path); CritSeparable, CritNoHarm and CritRuntime sit in the **r22 falsify** lane |

Alternative partition P2 (not excluded by the declared inputs): a single lane semantics that
ignores adapter steps **and** normalizes selectors fully would drop this group from 6 to 0,
which exceeds both individual outside gaps (2 and 4) and therefore cannot be reconciled unless
this group's seats are split across the two lanes in the pattern of P1. Conversely a lane that
counts every recorded event against the literal v1 authority (only selector normalization
differing) yields this group 4 lane-violations (C-γ1..3 + C-β4) and a gap of 2 — the same
magnitude as P1's build gap but a different event set.

**Explicit non-claims (per the assignment):**

1. The gap of 6 is **not** assumed to be six unique events. In this group the six rough
   `path` counts sit in six distinct events, but the *lane* side of any partition is
   hypothesis-dependent, and one rough event can be reclassified (α) or removed (β) rather
   than paired with a distinct lane event.
2. **No new edit permission is imported into old v1.** Rows C-γ1..3 are recorded as
   *classifier-difference candidates* only. Under the declared old-v1 authority as written,
   reading a seat's own declared write target is **not** covered by `read_paths`; the r23 v2
   decision set (`WRITE_ONLY_EDIT → DENY`, `READ_ONLY_EDIT → DENY`) is not used to relax it,
   and no r22 event is re-labelled as permitted.
3. This group's evidence is **necessary but not sufficient** for the C3 claim: the other
   round-23 build packs (groups 01–07) and the falsify packs must show that no further
   α-type residue events exist in the build lane, and must close the remaining 23 and 29
   lane-side counts.
4. No runtime/enforcement claim is made or implied: nothing here asserts that any tool or
   harness prevented, would prevent, or can detect any of these paths.

---

## 6. Residual risk and verification gaps

1. **Lane membership undeclared.** The pack's `"wave": "build"` is the r23 wave label; the
   pack does not state which r22 lane (`build`/`falsify`) each of the eight seats belonged
   to. P1 therefore requires a lane assignment to be confirmed from the r22 lane manifests
   by the C3 record author; this seat cannot confirm it from its declared inputs.
2. **Lane tool source unread.** The r22 lane's own checker (the `…/round-22/snapshot/tools/
   check-seat-scope.py` that ReviewScopeTrailer read at idx 1 and 4–10) is **not** in this
   seat's declared `read_paths`; it was not opened. Every §4 "lane, if it differs" column is
   therefore a bounded conditional, not an observation.
3. **Counter ambiguity (P6).** `f['path']` vs `sum(f.values())` for 25/33 is undeclared; the
   two readings give group totals 6 and 9 respectively, and different candidate sets.
4. **Uncovered classifier branches.** Component splitting (C-ζ), glob selector handling
   (C-η) and the exec bucket (C-θ) have zero rows here; this group cannot be used as
   evidence that those branches agree between rough and lane.
5. **Redaction limits.** CritRuntime idx 3's path is the literal token
   `redacted-internal-uri`; whether it denotes a filesystem path, an internal URI, or a
   redaction artifact is not decidable from the declared inputs, so C-β4's lane behaviour
   is left as a two-way conditional.
6. **Digest not independently verified.** The pack digest is supplied identity; no hash was
   computed (seat is NO-EXEC / NO-FETCH by binding).

## 7. Evidence used

- `.ufo/waves/round-23/packs/build-08.json` — eight seat bindings + raw event metadata
- `.ufo/waves/round-23/preregister.json` — outside counts, claims, edit_decisions, limits
- `.ufo/waves/round-23/sources/r22-rough-census.txt` — the original rough source (data only)
- `.ufo/waves/round-23/sources/godspeed-directive.txt` — working directive
- `skill://godspeed` — working directive
- No command was executed; no fetch was performed; no file outside this seat's declared
  write path was created or modified.
