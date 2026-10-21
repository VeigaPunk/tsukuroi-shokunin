# FxC3Disposition — falsification of `derive()` disposition classification (round 23, attempt 1)

Seat: `TsukuroiR23-2.FxC3Disposition-2` (FALSIFY lane, leaf member).
Target: `tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-path-reconciliation.py`
Supplied digest (not independently computed, no hashing performed): `fd0393be9140579424bdfc3c099b2b82fee11ccf9306d926c998235ce7ee1a6b`.

## Attacked claim

**C3 (calibration, `unexplained_cohorts` 2 → 0)** and, with it, the round-23 frontier step that the
ledger is an *explanation*, not merely a count match. The preregistered C3 scope reads: "Both fixed
r22 cohorts have exhaustive per-event/component explanation of rough-versus-lane path counts"
(`.ufo/waves/round-23/preregister.json`, `claims[2].scope`); the tool's own scope line says it
"explains counting-method differences" (`check-path-reconciliation.py:30-31`).

The falsifiable content of C3 is therefore **not** "the totals can be made to add up" but "each
disposition states the true cause of that event's difference". I attack that content.

Secondary target: the **frontier** invariant that a calibration record must not assert an
explanation it does not hold. C1 (eight edit-contract decisions) and C2 (v2 edit audit authority)
are *not* attacked here — the reconciliation tool reads neither, and I found no interaction.

## Axes named (godspeed)

1. **Label fidelity** — does each `disposition` state the true cause of that event's difference?
2. **Class coverage** — does the disposition vocabulary cover every event class the frozen cohorts
   can contain, or are whole classes forced into a wrong bucket?
3. **Rule fidelity** — does `canonical_event` actually re-author the lane rule whose frozen output
   it must reproduce (`snapshot/tools/check-seat-bindings.py`)?
4. **Arithmetic honesty** — do the aggregate identities follow from the row labels, or does the
   verdict hold only because a wrong label is placed in the bucket the identity expects?
5. **Constrainability** — is the defect region pinned by the selftest and by the landed mutation
   record, or is it unconstrained?

## Method and constraints

NO-EXEC / NO-FETCH. Nothing was executed, imported, hashed, listed or counted by command; the
digest above is supplied identity. All findings below are static traces over two rule files and the
outside rule re-authored in `sources/r22-rough-census.txt` (S085). Files read (seat-bound only):
the target tool, `snapshot/tools/check-seat-bindings.py` (the frozen v1 lane auditor),
`frozen/reconciliation-inputs.json`, `preregister.json`, `sources/r22-rough-census.txt`,
`candidate/.ufo/waves/round-23/measure/l1-mutation.json`, `sources/godspeed-directive.txt`.

Three rules are in play and they must be compared pairwise:

* **R (outside rough)** — re-authored at `check-path-reconciliation.py:61-72`; its source
  (`sources/r22-rough-census.txt`) has exactly three buckets: `bash` → `exec`, a tool outside
  `read|grep|glob|write` → `unknown`, otherwise one `path` per event, stopping at the first
  component not in the seat's authority list. **R has no fetch bucket and no URL concept at all.**
* **L (lane v1)** — `snapshot/tools/check-seat-bindings.py:43-107`. It has buckets
  `SCOPE-PATH-DENIED`, `SCOPE-FETCH-DENIED`, `SCOPE-EXEC-DENIED`, `SCOPE-TOOL-UNKNOWN`,
  `SCOPE-SCHEMA`; it normalizes qualified tool names (`:65-66`), expands parallel wrappers
  (`:76-88`), short-circuits malformed arguments to `SCOPE-SCHEMA` (`:96-98`), and strips a
  selector only for `read`/`grep` (`:50-54`, `:102`).
* **K (canonical, the re-author inside the tool)** — `check-path-reconciliation.py:94-108`. It is
  supposed to reproduce L's *path-denial* axis exactly, so that `canonical_path == retained_path`
  (`:181-182`) can be used as a fidelity oracle.

`derive()` (`:111-167`) then chooses one of four labels per event (`:29`, `:136-144`):
`agree`, `selector-normalization`, `unit-difference`, `unexplained`.

---

## Findings, by severity

### F1 — HIGH — a fetch-class read can be labelled `selector-normalization`: a false explanation that still passes every check

`canonical_event` skips fetch spellings (`:101-102`), so a URL component is never counted as a
path denial. `rough_event` has no fetch concept (`:61-72`), so the same URL component is counted
as one rough `path` event. The lane records `SCOPE-FETCH-DENIED`, not a path denial
(`snapshot/tools/check-seat-bindings.py:46-47`), so `retained_path_count` for that site is 0.

The `selector-normalization` branch (`:138-140`) is then reached, because its guard only compares
the *rough-stripped* string against the *canonical* base string:

```
rough_count == 1 and kept == 0 and not canonical and tool in ('read','grep')
and ROUGH_SUFFIX.sub('', v) != canonical_base(v, True)
```

Deterministic trace for `v = 'https://example.invalid:8080'` (seat `read_paths = [L+'a.md']`,
audit empty):

| step | value | source |
|---|---|---|
| `ROUGH_SUFFIX.sub('', v)` | `'https://example.invalid'` (the `:8080` tail is eaten by `\d[\d\-+,:]*`) | `:33`, `:139` |
| `canonical_base(v, True)` | `'https://example.invalid:8080'` (tokens `['//example.invalid','8080']` are not selector tokens, so the base is not returned) | `:79-84` |
| the two differ | **True** | `:139` |
| `rough_count` | 1 (`path`) | `:68-71` |
| `kept` | 0 (lane: fetch) | `snapshot:46-47` |
| `canonical` | `[]` | `:101-102` |
| **disposition** | **`selector-normalization`** | `:138-140` |

The true cause is not a selector spelling difference. It is a **classifier difference**: R has no
fetch bucket, so it charges a URL as `path`; L charges it as a fetch and records no path denial.
The label asserts the opposite.

The mislabel is not caught downstream. `cohort_findings` checks `canonical_path == retained_path`
(`:181-182`) — both are 0 for this row — and the arithmetic identity
`rough_path - retained_path == selector-normalization - unit_extra` (`:183-185`) is satisfied *by
the false label* (both sides grow by exactly 1). So a cohort containing such an event can report
`explained`, exit 0, and still carry a row whose stated cause is false. That is the C3 claim
("exhaustive per-event/component explanation") failing while the metric
(`unexplained_cohorts == 0`) passes.

**Falsifier (concrete, hand-checkable, no execution needed):** the single event
`('read', 'https://example.invalid:8080')` with `read_paths=[L+'a.md']` and an empty audit yields
`rough_category='path'`, `canonical_bad=[]`, `retained_path_count=0`,
`disposition='selector-normalization'`. The correct disposition is a fetch/classifier difference.

**Sharpener:** the label of a fetch event depends on an incidental spelling accident — whether
the URL's last `:`-segment is digits/`raw`-like. The same URL with a trailing path
(`'https://example.invalid/x'`, or `'https://example.invalid:8080/x'`) has
`ROUGH_SUFFIX.sub(...) == canonical_base(...)` (no `:digits` tail to eat), the branch guard
fails, and the row falls through to `unexplained` (`:143-144`). Two spellings of one semantic
class get two different wrong labels.

### F2 — HIGH — qualified tool names (`functions.read`) are not modelled at all: `unexplained`, and a canonical-vs-retained mismatch

L strips a `functions.` prefix before classifying (`snapshot:65-66`) and its own selftest pins that
behaviour (`snapshot:184` `case('qualified','functions.read',...)`, `:214` `qualified-write`,
`:219` `qualified-parallel`). K does not strip the prefix and `ROUGH_TOOLS` (`:34`) does not
contain qualified names, so:

* `canonical_event` returns `[]` immediately (`:96-97`) — the event is invisible to the canonical rule;
* `rough_event` classifies it as `unknown` (`:66-67`) — R likewise has no notion of qualified names.

Trace for `('functions.read', {'path': L+'denied.md'})` where `denied.md` is not in `read_paths`:

| quantity | value | source |
|---|---|---|
| rough | `unknown` → `rough_path_count` 0 | `:66-67` |
| canonical | `[]` → 0 | `:96-97` |
| lane | `SCOPE-PATH-DENIED` → `kept` = 1 | `snapshot:65-66, :102-106` |

Disposition walk: `agree` needs `0 == 0 == 1` (false, `:136-137`); `selector-normalization` needs
`rough_count == 1` (false, `:138`); `unit-difference` needs `rough_count == 1` (false, `:141`) →
**`unexplained`** (`:143-144`). The cohort then also fails `canonical_path != retained_path`
(`:181-182`, 0 vs 1) and the arithmetic identity (`:184-185`, 0−1 vs 0). So a cohort whose only
path denial was issued through a qualified tool name is reported as *unexplained residue* — a
false FAIL whose stated cause is wrong, and which is unrecoverable by the current code because the
label has no slot for "the two methods spell the tool differently".

### F3 — HIGH — parallel wrapper events are not expanded: `unexplained` plus a canonical-vs-retained mismatch

L expands `multi_tool_use.parallel` / `parallel` into children and classifies each child
(`snapshot:76-88`), recording `SCOPE-PATH-DENIED` at the *wrapper's* site when a child path is
denied; its selftest pins this (`snapshot:201-204`, `:219`, `:246-250` nesting). K does not:
`ROUGH_TOOLS` (`:34`) contains no wrapper name, so `canonical_event` returns `[]` (`:96-97`),
and R's rule classifies the wrapper as `unknown` (`:66-67`).

Trace for `('multi_tool_use.parallel', {'tool_uses': [{'recipient_name':'functions.read',
'parameters':{'path': L+'denied.md'}}]})`, `denied.md` not in `read_paths`: rough 0, canonical 0,
lane `kept` = 1 → `unexplained` (`:143-144`) + `RECONCILIATION-CANONICAL-MISMATCH` (`:181-182`) +
arithmetic break (`:184-185`). Same shape as F2: a whole class of real path denials that the
reconciliation structurally cannot explain, and it explains them wrongly rather than abstaining.

### F4 — MEDIUM — schema-class events are counted as path denials by K but never by L

`components()` coerces a missing/empty/non-string `path` to `''` (`:56-58`), and `_local('')` is
false, so `canonical_event` charges the event as a denied component (`:106-107`). L instead
short-circuits a missing or non-string path to `SCOPE-SCHEMA` and never reaches the path check
(`snapshot:96-98`, `:200` `case('bad-args','read',{},2,'SCOPE-SCHEMA')`). Likewise a non-dict
`args`: K returns `[]` (`:96-97`) while R charges `path` (R's own `str(a.get('path',''))`
coercion, `sources/r22-rough-census.txt`).

Trace for `('read', {})`: rough 1 (`path`, because `''` is not in the authority), canonical 1,
lane `kept` 0 (schema, not a path denial) → `agree` fails (`1 == 1 == 0`), `selector-normalization`
fails (`not canonical` is false), `unit-difference` fails (`kept == len(canonical) > 1` is false)
→ **`unexplained`** (`:143-144`) and `canonical_path (1) != retained_path (0)` (`:181-182`).
The true cause is a schema-class difference; the ledger reports unexplained residue.

### F5 — MEDIUM — `agree` is decided by counts only; it never checks *which* component was denied

The `agree` branch compares three counts (`:136-137`). It never compares the rough first-bad
component with the canonical denied components, even though both are carried in the row payload
(`:145-152`). Consequence: an event where R's "path" was a *fetch* component and L's path denial
was a *different* component is labelled `agree`.

Trace for `('grep', {'path': 'https://host:8080;' + L + 'denied.md'})` with `denied.md` not in
`read_paths`: R charges `path` at component 0 (the URL, `:68-71`); K skips the URL as fetch and
charges component 1 (`:101-107`); L records one fetch finding plus one `SCOPE-PATH-DENIED`
(`snapshot:102-106`) → `kept` 1. Counts are `1 == 1 == 1` → **`agree`**, while the row payload
simultaneously records `rough_first_bad: 0` and `canonical_bad: [1]` — the two methods flagged
different components of the same event, and the disposition says they agree. C3's wording is
"per-event/component explanation"; a component-level divergence reported as agreement is not one.

### F6 — MEDIUM — the arithmetic identity presupposes that R's `path` bucket contains no fetch-class events, so the "explained" verdict is contingent on F1's mislabel

`:183-185` asserts

```
rough_path - retained_path == selector_normalization - unit_extra
```

which holds only if every rough `path` event is either a lane path denial, a selector
normalization, or a unit difference. R has no fetch bucket, so any fetch-class read inflates
`rough_path` with no counterpart in any bucket. Two mutually exclusive outcomes, both wrong:

* the fetch URL does not end in `:<digits>` → the row is `unexplained` and the identity breaks →
  `RECONCILIATION-ARITHMETIC` + `RECONCILIATION-UNEXPLAINED` → spurious FAIL on a fully
  explainable difference;
* the fetch URL ends in `:<digits>` (or `:raw`) → the row is mislabelled `selector-normalization`
  (F1) → the identity balances → the cohort reports `explained`.

So the checker can only ever "explain" a fetch-class event by asserting something false about it.
The identity must be restated as
`rough - retained == fetch_classification + selector_normalization - unit_extra`, with a real
fetch bucket.

### F7 — LOW — `agree` also covers zero-count non-path events, overstating method agreement

An `exec` event (R: `exec`, L: `SCOPE-EXEC-DENIED`, `snapshot:68-69`), an unknown tool (R:
`unknown`, L: `SCOPE-TOOL-UNKNOWN`, `snapshot:72-73`) and a `web_search` (R: `unknown`, L:
`SCOPE-FETCH-DENIED`, `snapshot:70-71`) all reach `rough_path_count == canonical_path_count ==
retained_path_count == 0` and are labelled `agree` (`:136-137`). On the path axis the two methods
do agree, but the label asserts agreement of the methods, and the methods in fact classify these
events into different buckets. The row does keep `rough_category` (`:147`), so the divergence is
auditable — but the label is not. Either narrow the label's meaning to the path axis in the
ledger text, or keep a per-class bucket.

### F8 — MEDIUM (verification gap, supports F1–F4) — the defect region is pinned by neither the selftest nor the mutation record

* The reconciliation's selftest contains **no fetch/URL fixture at all**. Its only URL-shaped
  fixture is `('read','skill://godspeed')` (`:327-329`), which is exempted by the *skill* branch
  (`:104-105`), not by the fetch branch. The unit controls (`:336-344`) contain no URL either.
  Consequence: **deleting the two fetch-skip lines `:101-102` leaves the selftest green** — the
  defect region is unconstrained.
* The landed mutation record (`candidate/.ufo/waves/round-23/measure/l1-mutation.json`, 27/27
  killed) contains ten mutants for this tool and **none of them targets the fetch skip
  (`:101-102`), the `selector-normalization` guard (`:138-140`), the qualified-name handling, the
  wrapper expansion, or the schema branch**. The mutants that exist touch `ROUGH_SUFFIX` (0), the
  ledger-equality check (1), the snapshot digest check (2), the rough first-bad index (3), the
  rough rule's return (4), the `unit-difference` condition (5), the retained-count check (6), the
  `_local` conjunct (7), `canonical_base` (8) and the orphan check (9). F1–F4 live outside the
  killed region.

Notably, the *lane* auditor's own selftest does pin the fetch class
(`snapshot:190-191`: `https://example.invalid`, `HTTPS://EXAMPLE.INVALID/:1-5`,
`http://127.0.0.1/`, `localhost:9222/` → `SCOPE-FETCH-DENIED`) and the qualified/parallel classes
(`snapshot:184, :201-204, :214, :219`). The reconciliation is the component that lacks the
fixtures.

---

## Bounded search performed, and the bound it did not reach

**Reached (exhaustive over the rule files, by hand):** I enumerated the event classes the two
rules can produce — tool class × argument shape × path spelling — and compared R, L and K on each:

| class | R | L | K | disposition produced | verdict |
|---|---|---|---|---|---|
| clean local read | `clean` | none | `[]` | `agree` | correct |
| denied local read | `path` | PATH-DENIED | `[i]` | `agree` | correct |
| selector read (`:raw:N-M`) | `path` (R's single-suffix regex misses) | none | `[]` | `selector-normalization` | correct |
| selector read (`:N-M:raw`) | `clean` | none | `[]` | `agree` | correct |
| multi-component, 2 denied | `path` | 2× PATH-DENIED | 2 | `unit-difference` | correct |
| multi-component, 1 denied | `path` | 1 | 1 | `agree` | correct (count-wise) |
| **fetch URL ending `:<digits>`** | `path` | FETCH-DENIED | `[]` | **`selector-normalization`** | **F1 — false label, can pass** |
| **fetch URL not ending `:<digits>`** | `path` | FETCH-DENIED | `[]` | **`unexplained`** | **F1/F6 — false FAIL** |
| **qualified `functions.read`, denied path** | `unknown` | PATH-DENIED | `[]` | **`unexplained`** | **F2 — false FAIL + count mismatch** |
| **parallel wrapper with denied child** | `unknown` | PATH-DENIED | `[]` | **`unexplained`** | **F3 — false FAIL + count mismatch** |
| **schema args (missing/empty path)** | `path` | SCHEMA (no path finding) | `[i]` | **`unexplained`** | **F4 — false FAIL + count mismatch** |
| **fetch first, denied second (grep)** | `path`@0 | FETCH + PATH-DENIED | `[1]` | **`agree`** | **F5 — component divergence hidden** |
| `bash` / unknown tool / `web_search` | `exec`/`unknown`/`unknown` | EXEC/TOOL-UNKNOWN/FETCH | `[]` | `agree` | **F7 — overstatement** |
| `write` with selector | `path` | PATH-DENIED | `[i]` | `agree` | correct (`:344` pins it) |
| `skill://godspeed` in authority | `clean` | none | `[]` | `agree` | correct |
| `skill://godspeed` not in authority | `path` | PATH-DENIED | `[i]` | `agree` | correct (L exempts only the *local* check, `:48-49`, then still authority-checks at `:105-106`; K matches at `:104-107`) |
| `skill://godspeed:raw` | `path` | PATH-DENIED | `[i]` | `agree` | correct (`snapshot:217` matches K) |

This search found **no** mislabeling in the write-selector, skill-URI, dot-segment, invalid-selector
or multi-component classes: those are handled consistently by R, L and K, and the selftest pins
them (`:341-344`).

**Not reached — declared gap, not improvised around.** The frozen cohort payloads
(`.ufo/waves/round-23/snapshot/r22/{build,falsify}/{events,audit}.json`) and the landed ledger
(`.ufo/waves/round-23/path-reconciliation.json`) are **not in this seat's `read_paths`**, and my
seat is NO-EXEC, so I could not determine *whether* the cohorts contain a fetch-class, qualified-name,
wrapper or schema-class event, nor whether the landed ledger already carries F1's false label. I
deliberately did not ask a peer to read those files for me: doing so would circumvent this seat's
declared read boundary. The bound I could reach establishes the *defect* (the labels and the
verdict mechanism are wrong as specified); establishing *occurrence* in the two frozen cohorts
requires the four snapshot files and the ledger.

The occurrence question is not academic. The reported difference between the two methods is
exactly `rough 25 vs lane 23` (build) and `rough 33 vs lane 29` (falsify)
(`frozen/reconciliation-inputs.json`, `expected`; `preregister.json`,
`outside_round22.path_counts_as_reported`). Every difference term must come from one of the
classes above, and the classes I found to be mis-handled (fetch, qualified name, wrapper) are
precisely the ones whose contribution R and L record differently. If any of them occurs, the C3
verdict is either a false PASS (F1/F6) or a false FAIL (F2/F3/F4).

---

## Smallest in-scope remedy

Remedy scope: `tools/check-path-reconciliation.py` only, no change to the frozen inputs, the
ledger schema's pinned inputs, C1 or C2. Four edits, in dependency order.

**R1 — forbid the false label (F1, one-line guard).** In the `selector-normalization` branch
(`:138-140`), require that the rough first-bad component is not a fetch spelling:

```python
def _fetch_spelling(value):
    return bool(re.match(r'(?i)^https?://', value) or re.match(r'^[^/:\s]+:[0-9]+/', value))
...
elif (rough_count == 1 and kept == 0 and not canonical and tool in ('read', 'grep')
      and not _fetch_spelling(components(tool, args)[first_bad])
      and ROUGH_SUFFIX.sub('', components(tool, args)[first_bad]) != canonical_base(components(tool, args)[first_bad], True)):
    disposition = 'selector-normalization'
```

Note `_fetch_spelling` must be the *lane's* predicate (`snapshot:46`), not a new one, so that R1
and the canonical rule cannot drift apart.

**R2 — give the class a real label (F1, F6).** Add one disposition to `DISPOSITIONS` (`:29`), e.g.
`'fetch-classification'`, selected when the rough first-bad component is a fetch spelling, and
restate the identity at `:184-185` as

```
rough_path - retained_path == fetch_classification + selector_normalization - unit_extra
```

Without R2 the fetch class is merely moved from a false PASS to a false FAIL; the ledger must be
able to *say* that R has no fetch bucket and L does.

**R3 — make K reproduce L on the three classes it currently misses (F2, F3, F4).** Smallest
version, inside `canonical_event` (`:94-108`): strip a leading `functions.` from `tool`; treat
`multi_tool_use.parallel` / `parallel` by expanding `args['tool_uses']` and classifying each
child's `parameters.path` into the component list (bounded by L's own depth limit of 8,
`snapshot:64`); and treat a missing/empty/non-string `path` (or non-dict `args`) as a schema-class
event with zero path denials, matching `snapshot:96-98`. Each of these produces a *class
difference* (R says `unknown`, L says PATH-DENIED), not a path-selector difference, so each needs
its own bucket — e.g. `'tool-spelling'` for the qualified-name case and `'wrapper-expansion'` for
the parallel case — and each must appear in the identity from R2.

**R4 — pin it (F8).** Add one selftest fixture per new class and one mutant per new branch:
a fetch fixture at both spellings (`'https://example.invalid:8080'` → must be
`fetch-classification`, not `selector-normalization`; `'https://example.invalid/x'` → same
disposition, so the two spellings cannot diverge), a `functions.read` fixture, a
`multi_tool_use.parallel` fixture with a denied child, and a `('read', {})` schema fixture; plus a
mutant that deletes the fetch-skip lines at `:101-102` (currently unkillable, F8) and a mutant
that deletes the `functions.` strip.

**Optional strengthening (cheap, uses data already pinned).** The frozen `audit.json` for each
cohort carries the lane's *other* finding ids (`SCOPE-FETCH-DENIED`, `SCOPE-SCHEMA`,
`SCOPE-EXEC-DENIED`, `SCOPE-TOOL-UNKNOWN`) with their sites, and `derive()` currently reads only
`SCOPE-PATH-DENIED` (`:118-121`). Consuming those ids turns them into a per-site class oracle:
each event's class difference becomes checkable against the lane's own record instead of being
inferred from counts. That is what would have caught F1–F4 immediately, and it needs no new
inputs.

---

## Residual risk and verification gaps

1. **Occurrence unverified.** I cannot show from my bound that the frozen cohorts contain a
   fetch-class, qualified-name, wrapper or schema-class event. F1–F4 are defects in the
   disposition rules and the verdict mechanism as specified; whether the landed ledger already
   carries a false label or a false FAIL requires the four snapshot payloads and the ledger
   (outside this seat's `read_paths`).
2. **No execution.** Every trace above is a static, line-by-line derivation over two rule files;
   I ran nothing and computed no digest. Each trace is stated so a reader can confirm it by hand
   against the cited lines. I make **no** claim that the checker currently exits 0 or 1 on the
   frozen cohorts.
3. **The canonical rule is a third re-authoring.** K (`check-path-reconciliation.py:94-108`) is
   not derived from, and not checked against, the landed auditor. The landed seat-bindings tool is
   v2 (the landed mutation record shows `edit_paths` / `allow_structured_edit` handling in
   `check-seat-bindings.py`), while the frozen r22 audit was produced by v1
   (`snapshot/tools/check-seat-bindings.py`). The reconciliation correctly scopes itself to the
   frozen v1 cohorts, but nothing in the wave ties K to either version of the auditor, so drift
   between the re-authored canonical rule and the real lane rule is invisible to the whole wave.
   (The candidate's v2 file is not in this seat's `read_paths`, so I cannot cite its finding ids.)
4. **Ledger mutability.** `evaluate()` recomputes the derivation and compares it to the committed
   ledger (`:186-190`, `RECONCILIATION-LEDGER-MISMATCH`), so a forged or stale disposition is
   detected as a *mismatch* — but a forged disposition that the recomputation itself produces (F1)
   is undetectable by that mechanism. The integrity check protects the ledger against
   hand-editing, not against a wrong rule.
5. **Scope of the falsification.** C1 and C2 are untouched by these findings: the reconciliation
   tool reads neither the edit contract nor the v2 audit authority, and no disposition defect
   bears on the eight edit-contract decisions or on the structured-edit audit semantics.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: fd0393be9140579424bdfc3c099b2b82fee11ccf9306d926c998235ce7ee1a6b
Predicate: r23f-fxc3disposition
Scope: executed=none
