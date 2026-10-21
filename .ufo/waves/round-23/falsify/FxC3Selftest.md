# FxC3Selftest — falsification of the path-reconciliation selftest controls and its L1 mutant record

Round 23, attempt 1. Seat: FxC3Selftest (leaf, no dispatch).

## 0. Scope, method, constraints

- **Target (declared identity, not recomputed):** `.ufo/waves/round-23/candidate/tools/check-path-reconciliation.py`, supplied SHA256 `fd0393be9140579424bdfc3c099b2b82fee11ccf9306d926c998235ce7ee1a6b`. No hashing, listing, wc, import, compile, test or execution was performed.
- **Attacked claim: C3** (`preregister.json` → `claims[2]`, axis *calibration*, metric `unexplained_cohorts`, before 2 → target 0, command `python3 tools/check-path-reconciliation.py --revision <REV>`), and specifically the *evidence integrity* of C3's verification apparatus: the selftest control set and the 10 recorded L1 mutants for this tool in `.ufo/waves/round-23/measure/l1-mutation.json`.
- **Read (all bound paths only):** the candidate tool; `preregister.json`; `frozen/reconciliation-inputs.json`; `sources/r22-rough-census.txt` (S085); `snapshot/tools/check-seat-bindings.py` (the C2 authority tool); `measure/l1-mutation.json`; the godspeed directive copy. Nothing else was opened; no filesystem search beyond the declared paths.
- **Method:** NO-EXEC/NO-FETCH, so every statement below is a *static trace* over the declared file contents. The bounded search was: (a) enumerate the tool's single-line mutable surfaces; (b) cross-reference each surface against the tool's own observation set to decide whether any observation can observe it; (c) re-derive, for each of the 10 recorded mutants, the specific observation that changes its verdict; (d) compare the re-authored rough rule line-by-line against the S085 source text.
- **Verdict vocabulary:** "unkilled" = the mutation leaves every observation's `pass` verdict unchanged, i.e. the control set cannot observe the change.

## 1. Baseline reconciliation of the control inventory (so the rest is checkable)

The tool's `selftest()` builds **19 case-level fixtures + 8 unit controls = 27 observations** (cases at lines 293, 295, 298, 301, 303, 306, 307, 308, 312, 313, 314, 315, 317, 319, 321, 322, 323, 326, 329; units at lines 337–344). The assignment's premise of "26 controls" is **off by one**; the tool's own printed `cases` field will read `27`.

Baseline is green by static trace. Two structural facts make that tractable and are used repeatedly below:

- For **every explained disposition** the canonical count equals the retained count: `agree` ⇒ `rough == len(canonical) == kept` (line 136); `selector-normalization` ⇒ `not canonical` and `kept == 0` (lines 138–139); `unit-difference` ⇒ `kept == len(canonical) > 1` (line 141). Hence for a fully explained cohort `totals['canonical_path'] == totals['retained_path']` (rows only) and the arithmetic identity at line 184 holds by construction.
- `derive()` raises `Unevaluable` for roster/shape violations, and `evaluate()` converts pins/ledger shape errors into exit 2 *before* cohort evaluation, so fixture cases that fail early never reach the count checks.

Recorded-mutant cross-check (bounded search result). Every one of the 10 recorded mutants for this tool does have a dedicated killing observation, independent of the other fixtures:

| mutant | line mutated | observation that actually kills it |
|---|---|---|
| 0 (ROUGH_SUFFIX regex) | 33 | unit `rough-misses-raw-first` (337) |
| 1 (drop ledger equality) | ~189 | `forged-disposition`/`dropped-row`/`duplicate-row`/`wrong-arithmetic-total` (312–315) |
| 2 (pins digest → `if False`) | ~205 | `snapshot-tampered` (319) |
| 3 (`return 'path', index` → `0`) | 71 | `one-per-event-vs-per-component` (301) |
| 4 (`return 'path'` → `continue`) | 70–71 | `rough-misses-raw-first` (337) + `agree-clean` (308) |
| 5 (unit-difference guard weakened) | 141 | `unit-count-mismatch` (303) |
| 6 (retained-count check → `if False`) | 179 | `wrong-retained-total` (307) |
| 7 (drop `_local` conjunct) | 106 | unit `canonical-dot-denied` (343) |
| 8 (`canonical_base` always strips) | 84 | unit `canonical-invalid-token-denied` (342) |
| 9 (orphan check → `if False`) | 176 | `orphan-retained` (317) |

Record hygiene defects (method-level, no per-mutant error):

- `measure/l1-mutation.json` states the criterion as *"run `--selftest`; killed = nonzero exit"* but carries **no baseline row**. With that criterion, a red baseline would mark every mutant "killed" indistinguishably. The record must anchor on a baseline observation (exit 0 / `failed` 0) for its kills to mean "behaviour changed".
- The record's `results` cover **10 of the ≥8 mutable surfaces** but only 10 named mutants; the six surfaces below are absent from the mutant space, so "killed 27 / total 27" reads as coverage of the recorded mutants only, not of the tool.

## 2. F1 (HIGH) — both cohort-total checks are pinned in one direction only; the over-count direction is unkilled and yields a false C3 green

**Mutants (one line each):**

- line 177: `if totals['rough_path'] != expected['rough_as_reported']:` → `if totals['rough_path'] < expected['rough_as_reported']:`
- line 179: `if totals['retained_path'] != expected['lane_retained']:` → `if totals['retained_path'] < expected['lane_retained']:`

**Why the control set cannot observe them.** Computed-vs-expected per fixture (rough / retained):

| fixture | computed rough | expected rough | computed retained | expected retained |
|---|---|---|---|---|
| 293 `mixed-raw-range-order` | 2 | 2 | 1 | 1 |
| 295 `selector-but-retained` | 2 | 2 | 2 | 2 |
| 298 `offsetting-pair-net-zero` | 1 | 1 | 1 | 1 |
| 301 `one-per-event-vs-per-component` | 1 | 1 | 2 | 2 |
| 303 `unit-count-mismatch` | 1 | 1 | 3 | 3 |
| 306 `wrong-rough-total` | 1 | **2** | 1 | 1 |
| 307 `wrong-retained-total` | 1 | 1 | 1 | **2** |
| 308, 312–315 | 1 | 1 | 1 | 1 |
| 317 `orphan-retained` | 1 | 1 | **2** | 1 |
| 319–326 | n/a (exit 2 before counts) | | | |
| 329 `non-path-events` | 0 | 0 | 0 | 0 |

The only rough-total fixture (306) pins the **computed < expected** direction; no fixture has computed rough **>** expected. The only fixture whose computed retained count exceeds expected is 317, whose `want_id` is `RECONCILIATION-ORPHAN-FINDING`; the retained-count check is not what that fixture asserts, and under the mutant 317 still fails (orphan finding present) → the mutant survives. Both `!=` → `<` mutations therefore leave all 27 observations' verdicts unchanged.

**Consequence (the false green).** The pinned outside numbers are `25`/`33` (`preregister.json` → `outside_round22.path_counts_as_reported.rough`; `frozen/reconciliation-inputs.json` → `expected.*.rough_as_reported`) and the pinned lane numbers `23`/`29`. Under the rough mutant, a re-authored rule that counts **more** path events than the outside census is not flagged: each extra rough row becomes `selector-normalization` (explained, lines 138–139), `canonical_path == retained_path` still holds, the arithmetic identity at line 184 still holds, and no row is `unexplained` → the cohort is reported `explained=True` and the tool exits 0 with `unexplained_cohorts=0`. The C3 artifact would then assert a completed calibration while its own recomputed rough census **contradicts** the outside report it claims to reconcile — i.e. the artifact-level falsifier for the calibration claim. The retained mutant is the mirror case: if the tool's canonical rule and the lane's audit move up together (both above the pinned lane number), the retained check is the only signal that would have caught it.

**Smallest in-scope remedy (two fixtures, selftest block only):**

```
case('rough-over-count', events(('read', b), ('read', b)), bindings([a]), audit('S:0', 'S:1'),
     1, 2, 1, 'RECONCILIATION-ROUGH-COUNT')
case('retained-over-count', clean, bindings([a]), audit('S:1', 'S:1'),
     1, 1, 1, 'RECONCILIATION-RETAINED-COUNT')
```

Trace of the first: two `read b` events against `read_paths=[a]` → computed rough 2 > expected 1 (canonical 2, retained 2, `agree` rows, no unexplained) → under the correct `!=` it raises `RECONCILIATION-ROUGH-COUNT`; under the mutant it raises nothing → the case fails → mutant killed. Second: retained computed 2 > expected 1 → same asymmetry, killed only by the mutant-side failure to raise the id.

## 3. F2 (MEDIUM) — the re-authored rough rule applies the selector strip to `read` but not `grep`; the grep branch is unexercised and breaks S085 fidelity

**Mutant (line 69):** `candidate = ROUGH_SUFFIX.sub('', value) if tool in ('read', 'grep') else value` → `if tool == 'read'`.

**S085 ground truth.** `sources/r22-rough-census.txt` (outside source cell, re-authored, never executed): `q=strip_sel(v) if t in('read','grep') else v`, with `strip_sel = re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`. The tool's line 33 regex is byte-identical to S085's, and line 69 is the only place the tool's copy of S085 diverges from it: the tool strips for `read` only, S085 strips for `read` **and** `grep`.

**Why it is unkilled.** The only `grep` events in the whole control set are `multi` (lines 301, 303): `('grep', a + ';' + b + ';' + L + 'c.md')` — its components contain no `:` suffix, so `ROUGH_SUFFIX.sub` is a no-op under either mutant. The unit controls use `read` (337, 338, 340, 342) and `glob` (339, 341) only. There is **no** fixture with a `grep` event carrying a selector suffix, so the mutant leaves all 27 verdicts unchanged.

**Consequence.** A `grep` read of `<path>:raw` (or `:1-9`, `:raw:1-9`) would be classified `path` by the rough side while the canonical side (line 103, which still strips for `read`/`grep`) classifies it clean. The row lands as `selector-normalization` (explained), so it does **not** raise `RECONCILIATION-UNEXPLAINED`; it inflates `rough_path` instead. Combined with F1's rough mutant, that inflation is entirely silent → the cohort reports PASS with a rough census that disagrees with S085's own re-authoring. Whether the frozen r22 cohorts actually contain `grep` events with selector suffixes could not be checked here (the snapshot inputs are outside this seat's bound read paths) — that half is `[INFERENCE]`.

**Smallest in-scope remedy (one unit control):**
`('rough-strips-selector-on-grep', rough_event('grep', {'path': a + ':raw:1-2'}, {'read_paths': [a]}) == ('clean', None))` — baseline `('clean', None)` (strip → `a` ∈ authority); under the mutant `('path', 0)` → killed.

## 4. F3 (MEDIUM) — the canonical rule stops requiring the skill URI in the seat's read authority, breaking the C2 mirror

**Mutant (line 104):** `if base == 'skill://godspeed' and base in authority:` → `if base == 'skill://godspeed':`

**Why it is unkilled.** The only fixture that mentions the skill URI is `non-path-events` (328–329), and there the binding *does* include `'skill://godspeed'` in `read_paths` (`bindings([a, 'skill://godspeed'])`) → identical outcome before and after the mutation. No fixture reads the skill URI from a seat that lacks it, so all 27 verdicts are unchanged.

**Why it matters.** The C2 authority tool in this very wave (`snapshot/tools/check-seat-bindings.py`) treats the skill URI as a *value* exemption only: `requested_path()` returns `(value, None)` for `'skill://godspeed'`, and `classify()` then enforces membership — `elif path not in binding['write_paths' if tool == 'write' else 'read_paths']: findings.append('SCOPE-PATH-DENIED')`. The reconciliation tool's `canonical_event` is the lane-side mirror of exactly that rule (it is what `retained_path` is compared against), so the mutant makes the two tools disagree about the same read: C2 denies it as `SCOPE-PATH-DENIED`, C3's canonical side counts it clean. Under the round-23 contract ("per-seat literal v2 binding is narrower than generic role defaults") that divergence is a real authority difference, not a stylistic one. Effect on the artifact: canonical under-counts → `canonical_path != retained_path` → `RECONCILIATION-CANONICAL-MISMATCH`/`RECONCILIATION-UNEXPLAINED` (a false FAIL) if the lane did deny it; and if the lane also failed to deny it, a genuine denial is masked. Which of the two occurs depends on the frozen r22 bindings/audits (outside this seat's read paths) — `[INFERENCE]`.

**Smallest in-scope remedy (one unit control):**
`('canonical-skill-requires-authority', canonical_event('read', {'path': 'skill://godspeed'}, {'read_paths': [a]}) == [0])` — baseline `[0]` (URI not in authority → `_local` false → denied); under the mutant `[]` → killed.

## 5. F4 (MEDIUM) — the selector token vocabulary is only one-third covered

**Mutant (line 76):** `token in ('raw', 'img', 'conflicts')` → `token in ('raw',)`.

**Why it is unkilled.** No fixture or unit control ever uses `:img` or `:conflicts`; the exercised tokens are `raw` and numeric ranges only (337, 338, 340, 342, 344). All 27 verdicts are unchanged.

**Why it matters.** The C2 sibling's `valid_token` (snapshot `check-seat-bindings.py`) carries the *identical* tuple `('raw','img','conflicts')`, so the reconciliation's canonical rule is meant to mirror it. Narrowing the tuple makes C3 deny `:img`/`:conflicts` spellings that C2 allows, inflating `canonical_path` relative to the lane's retained count → `RECONCILIATION-CANONICAL-MISMATCH` / `UNEXPLAINED` false reds on any r22 event using those selectors (`[INFERENCE]`, data-dependent).

**Smallest in-scope remedy (one unit control):**
`('canonical-img-selector-allowed', canonical_event('read', {'path': a + ':img'}, {'read_paths': [a]}) == [])` (optionally a second for `':conflicts'`).

## 6. F5 (MEDIUM) — the "URL is a separate class" branch has no fixture at all

**Mutant (line 101):** `if re.match(r'(?i)^https?://', value) or re.match(r'^[^/:\s]+:[0-9]+/', value):` → drop either alternative, e.g. `re.match(r'(?i)^https://', value)`.

**Why it is unkilled.** Line 327's comment claims *"URL is a separate class in both totals"*, but the fixture it introduces (line 328) is `events(('bash', ''), ('edit', a), ('read', 'skill://godspeed'))` — **no URL at all**. A grep of the file shows the only occurrences of `http`/`https` are the two regexes at line 101 itself. There is no `https://`, `HTTPS://`, `http://127.0.0.1/` or `host:port/` fixture anywhere in the 27 observations. All verdicts are unchanged.

**Why it matters.** The C2 tool has four explicit fetch-spelling controls (`fetch-https://example.invalid`, `fetch-HTTPS://EXAMPLE.INVALID/:1-5`, `fetch-http://127.0.0.1/`, `fetch-localhost:9222/`); the reconciliation tool has none, yet its `canonical_event` docstring (line 95) and the cohort comment both assert the fetch class is excluded. A fetch-spelled read that should sit outside the path class would instead be counted path-denied by the canonical side → divergence from the lane's retained count → false red / spurious `unit-difference` labelling. Conversely, a mutant that *widens* the skip (e.g. skipping any `x:`-prefixed value) would silently drop real path denials. Unobserved either way.

**Smallest in-scope remedy (one unit control):**
`('canonical-fetch-url-not-path', canonical_event('read', {'path': 'https://example.invalid'}, {'read_paths': [a]}) == [])` and, for the host:port branch, `('canonical-fetch-hostport-not-path', canonical_event('read', {'path': 'localhost:9222/'}, {'read_paths': [a]}) == [])`.

## 7. F6 (LOW) — the binding-roster coverage check is unreachable from the control set

**Mutant (line 153):** `if set(bound) != names:` → `if False:`.

**Why it is unkilled.** Every fixture binds exactly seat `'S'` and every events roster contains `'S'`, so `set(bound) == names` always holds; the only roster-forgery fixture (326, seat `'GHOST'`) is caught earlier by `derive()`'s per-seat identity guard (`name not in bound`), never reaching line 153. All 27 verdicts are unchanged.

**Why it matters.** The check is the sole guarantee that *every* bound seat contributed events, i.e. that the ledger's "exhaustive per-event explanation" (the C3 scope sentence) covers the whole cohort. If a frozen cohort contained a bound seat with no recorded events, the mutant would let that seat be silently omitted. Partial mitigation: a lane finding for the missing seat would surface as `RECONCILIATION-ORPHAN-FINDING` (line 176) — but a seat with no findings would not, and the cohort would still report `explained=True`.

**Smallest in-scope remedy (one case):** a fixture whose `bindings` list a seat absent from `events`, expecting `RECONCILIATION-INPUT-MALFORMED` (exit 2).

## 8. F7 (LOW) — two checks can never be the sole signal, so their direction is unpinned

`RECONCILIATION-CANONICAL-MISMATCH` (181–182) and `RECONCILIATION-ARITHMETIC` (184–185) are structurally redundant: by §1, an explained cohort always satisfies `canonical == retained` (rows) and the arithmetic identity. The only ways to violate them are an orphan (which fires `RECONCILIATION-ORPHAN-FINDING` at 176 in the same pass) or an unexplained row (which fires `RECONCILIATION-UNEXPLAINED` at 188). Therefore no fixture can isolate either id, and mutating them — including flipping their comparison direction — is unkillable. They are corroboration, not independent controls; a reader of the ledger's finding ids could over-credit them as separate guarantees.

## 9. F8 (LOW) — `_local`'s character bans are inert against the membership test

`_local` (87–91) rejects control characters, `*?[];:` and dot segments. Because `canonical_event` also requires `base in authority` (106) and the bound paths are themselves validated as local by the C2 tool when a manifest is validated, the character and glob bans can only reject paths the membership test already rejects. Consequently `write-no-selector-strip` (344) passes through the **membership** test, not through `_local`: removing `':'` from line 90 leaves all 27 verdicts unchanged (the path `r.md:raw` is still not a member of `write_paths`). Only the dot-segment clause is meaningfully exercised, by `canonical-dot-denied` (343). This is harmless today, but the control does not test what its name asserts, and `_local` is the *only* locality gate on the reconciliation path — the reconciliation tool never validates the frozen bindings' own locality (the C2 tool does that at manifest-validation time, and the frozen snapshot bypasses it).

## 10. Smallest in-scope remedy (single location: the `selftest()` block of the candidate tool, plus the measurement record)

Six additions, all inside `selftest()`; no production file, ledger, pin, or snapshot is touched:

1. `case('rough-over-count', …)` and `case('retained-over-count', …)` — pin the over-count direction of lines 177/179 (F1).
2. `('rough-strips-selector-on-grep', …)` — pin line 69's `grep` branch against S085 (F2).
3. `('canonical-skill-requires-authority', …)` — pin line 104's authority conjunct and the C2 mirror (F3).
4. `('canonical-img-selector-allowed', …)` — pin line 76's token vocabulary (F4).
5. `('canonical-fetch-url-not-path', …)` (+ host:port twin) — pin line 101's fetch class (F5).
6. one roster-coverage case — pin line 153 (F6).

Record hygiene: add a baseline row to `measure/l1-mutation.json` (`baseline selftest exit 0, failed 0`) so "killed = nonzero exit" is anchored, add the six mutants above to the mutant set, and correct the control count to 27 (19 case fixtures + 8 unit controls).

Each addition above is independently sufficient to kill the corresponding mutant: the standard L1 procedure (temp copy, single textual edit, `--selftest`) must show that mutant flipping exactly one observation's `pass` to false while the baseline stays green.

## 11. Residual risk and verification gaps

- **Nothing was executed** (NO-EXEC/NO-FETCH): every verdict above is a static trace over the declared contents of the candidate tool. No digest was computed, no test run, no import. The verifier for each finding is the existing temp-copy `--selftest` procedure; each mutant must leave the `observations` array and the `failed` count unchanged.
- **Frozen snapshot not readable here.** `.ufo/waves/round-23/snapshot/r22/{build,falsify}/{events,bindings,audit}.json` are outside this seat's bound read paths (only their pinned digests in `frozen/reconciliation-inputs.json` were available), so the data-dependent halves of F2–F5 (do the cohorts contain `grep` events with selector suffixes, `:img`/`:conflicts` selectors, skill reads without authority, or URL-spelled reads?) are marked `[INFERENCE]` and remain unverified here.
- **What is *not* in doubt:** the tool's rough rule matches S085 line-by-line (identical regex at line 33; strip for `read`; `write_paths` for `write` and `read_paths` otherwise; break at the first failing component), so the recomputed rough counts should reproduce the outside 25/33 by construction. The defect is not the current rule; it is that the control set cannot *observe* a deviation from it, and that the two cohort-total checks are pinned in one direction only.
- **Production status of C3 not re-verified.** The landed `check-path-reconciliation.py --revision <REV>` run was not executed and the committed ledger `path-reconciliation.json` was not readable under this seat's bindings; no claim is made here about whether the landed command currently exits 0.
- **Out of scope by contract:** no production file, ledger, pin, route, config or Git state was modified; this report is the only artifact written.
- Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: fd0393be9140579424bdfc3c099b2b82fee11ccf9306d926c998235ce7ee1a6b
Predicate: r23f-fxc3selftest
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
