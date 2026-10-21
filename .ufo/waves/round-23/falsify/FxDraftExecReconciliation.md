# FxDraftExecReconciliation — wave-1 draft vs landed candidate divergence review

Seat: `TsukuroiR23-2.FxDraftExecReconciliation-2` · reviewer · round23 attempt1 · scope `executed=none`.

## Target and binding

- Landed candidate (reviewed artifact, digest **supplied** as `fd0393be9140579424bdfc3c099b2b82fee11ccf9306d926c998235ce7ee1a6b`, **not** computed here):
  `.ufo/waves/round-23/candidate/tools/check-path-reconciliation.py` (387 lines, read in full via `:raw`).
- Independent wave-1 draft: `.ufo/waves/round-23/worktrees/ExecReconciliation/draft/check-path-reconciliation.py` (676 lines, read in full via `:raw`).
- Wave-1 report: `.ufo/waves/round-23/build/ExecReconciliation.md`; claim text: `.ufo/waves/round-23/preregister.json`.
- No execution, import, compile, test, lint, format, hash, wc, listing, or fetch was performed. Every statement below is derived from source text and hand-traced control flow only. No installs were made (this seat's narrower NO-EXEC/NO-FETCH scope forbids them; nothing else was needed).
- Note on the two docs: both `candidate/tools/check-path-reconciliation.py` and `worktrees/ExecReconciliation/draft/check-path-reconciliation.py` carry the identical first docstring line "Reconcile the outside rough round22 path census with retained lane audit findings." — the landed file is a **rewrite**, not the wave-1 draft promoted. The divergence list below is therefore not cosmetic.

## Attacked claim

**C3 (preregister `claims[2]`, axis `calibration`, metric `unexplained_cohorts`, before 2 → target 0)**, specifically the part that the landed gate can in fact reach `unexplained_cohorts = 0` on the fixed r22 cohorts and that its per-event ledger is an exhaustive *explanation* (not merely a re-count) of rough-vs-lane path differences.

Secondary target: the wave-1 report's integration guidance (`.ufo/waves/round-23/build/ExecReconciliation.md`: "`derive()` is the intended generator", disposition vocabulary `non-path/agreement/selector-normalization/unit-difference`, "canonical-denied events with the 23/29 retained sites"), which the main agent may still treat as the authoritative description of the landed record.

Not attacked and not claimed here: C1 edit decisions, C2 v2 edit audit authority, and any claim of native runtime enforcement (this tool is a static gate over frozen bytes).

## Method

Full raw reads of both implementations, then a predicate-level sweep of six decision surfaces in each: (1) rough classifier, (2) canonical classifier, (3) disposition classifier, (4) cohort validator / arithmetic, (5) ledger + frozen-input gate, (6) CLI and selftest. Each divergence is classified as decision / finding ID / exit / disposition / control, and adjudicated by hand-tracing a literal case through both code paths. No test was run; every "→" below is a hand trace over quoted source.

## Findings by severity

### HIGH

**H1 — Candidate compares a *component* count against a *site* count, so a legitimate per-component difference becomes an unexplained cohort (candidate wrong).**

Candidate `derive` counts `canonical_path_count = len(canonical)` (number of denied **path components** in an event) and `cohort_findings` then asserts `totals['canonical_path'] != totals['retained_path'] → RECONCILIATION-CANONICAL-MISMATCH`, while `retained_path_count` is the number of retained `SCOPE-PATH-DENIED` **sites** (`seat:index`, one site per event in the r22 audit shape). The lane records one site per event regardless of how many components of that event are denied, so the two totals are in different units.

Literal case (hand-traced through candidate `rough_event` → `canonical_event` → disposition ladder → `cohort_findings`):

- binding `read_paths = ['<LANE>/a.md']`; event 0 = `grep` with `args.path = '<LANE>/secret1.md;<LANE>/secret2.md'`; audit records one `SCOPE-PATH-DENIED` at site `S:0`.
- `rough_event`: grep splits on `;` → first component `<LANE>/secret1.md` not in `read_paths` → `('path', 0)`, `rough_path_count = 1`.
- `canonical_event`: component 0 and component 1 both fail exact membership → `canonical = [0, 1]`, `canonical_path_count = 2`.
- `kept = 1` (one retained site at `S:0`).
- Disposition ladder: `agree` needs `1 == 2 == 1` → no; `selector-normalization` needs `kept == 0` → no; `unit-difference` needs `kept == len(canonical) > 1`, i.e. `1 == 2` → no → row falls to **`unexplained`** → `RECONCILIATION-UNEXPLAINED`, and the totals add `RECONCILIATION-CANONICAL-MISMATCH` (2 ≠ 1). Cohort → `explained=False`, `unexplained_cohorts ≥ 1`, exit 1.

The rough-vs-lane difference here is *fully explainable* (one event, one site), yet the landed gate fails the cohort. Consequence: the C3 target `unexplained_cohorts = 0` is unreachable for any cohort containing an event with ≥2 denied components. Draft side: `derive` classifies that row `agreement` and compares only `rough_path_events` vs `rough_as_reported` and `retained_path_sites` vs `lane_retained` (`lane_valid`), i.e. it never compares component counts to site counts → draft is **right on the unit of comparison**; the candidate is wrong.

Compounding: the candidate's `unit-difference` branch (`rough_count == 1 and kept == len(canonical) > 1 and first_bad == canonical[0]`) can only fire when the **same** site string carries two retained findings (its own selftest forges `audit('S:0','S:0')` for this). Under the real r22 audit shape (one finding per event site) `kept ≤ 1` always, so the `unit-difference` label is **unreachable on real data**, and the genuine unit difference (components > sites) is the one case that ends up `unexplained`. The candidate's disposition taxonomy therefore has its unit-difference predicate inverted relative to the r22 audit shape.

Smallest in-scope remedy (landed candidate, production): in `derive`, keep the component list but add an event-level boolean `canonical_denied = bool(canonical)`; count `canonical_path` as denied **events** for the totals that are compared against `retained_path` (sites); classify a row with `len(canonical) > kept >= 1` as `unit-difference` (explained, component-vs-site) instead of `unexplained`; drop or rebase `RECONCILIATION-CANONICAL-MISMATCH` onto the event-level count; and add one selftest fixture with two denied components in one grep event.

**H2 — Draft treats every absolute path as "component rejected", so it denies selector-suffixed reads of bound members; its 23/29 claim is unsupported and its own selftest contradicts it (draft wrong).**

Draft `component_rejected` splits on `/` and rejects if **any** part is `""`, `"."`, `".."`. For an absolute member path the first part is `""`, so *every absolute path* is "rejected". `canonical_bad_indices` checks exact membership **before** `component_rejected`, so a bare absolute member is clean, but a member **with a selector suffix** is not an exact member and is then rejected outright — the selector is never stripped.

Literal case (hand-traced through draft `canonical_bad_indices` → `derive` → `lane_valid`):

- binding `read_paths = ['/home/.../tsukuroi-shokunin/a.md']` (the seat-binding style used in this wave and in the candidate's own selftest); event = `read` with `args.path = '/home/.../tsukuroi-shokunin/a.md:raw'`.
- `component in members`? no (suffix). `component_rejected`? `parts[0] == ''` → **True** → `bad = [0]` → `canonical_path_failures = 1`.
- `rough_first_bad`: `strip_rough` removes `:raw` → the member → rough clean.
- So: rough 0, canonical 1, retained 0 → draft disposition falls through to `unit-difference` → `lane_valid` returns `False` at the `else` branch → `COHORT-UNEXPLAINED`, exit 1.
- The same shape hits the draft's own fixture: `Alpha:1` (`/r/a.json:2-4:raw`), `Beta:0` (`/r/b.md:2-4:raw`), `Beta:1` (`/r/b.md:raw:2-4`), `Beta:4` (`/r/a.json:5-9,20-22`) are all absolute, so all are "rejected". That makes the draft's selftest case `clean` (expect exit 0, ids `[]`) and its explicit assertion `by_key[("build","Beta",1)]["canonical_path_failures"] == 0` fail by hand trace — i.e. **the draft's selftest would report FAIL if it were ever executed**, and the draft report's "canonical-denied events with the 23/29 retained sites" cannot hold when member paths are absolute.

Candidate side is right: `canonical_base` strips the selector first and `_local` checks `path.split('/')[1:]` (skipping the leading empty segment), so `/home/.../a.md:raw` is a member → clean.

Remedy for the draft (non-production wave-1 artifact): split the guard — absolute paths must not be treated as dot-segment rejections; strip the selector before the dot/control rejection; then re-derive the 23/29 claim and re-run the draft's selftest expectations. Until then, treat the wave-1 report's "23/29" and "canonical-denied events" statements as unverified, and do not use them as evidence.

### MEDIUM

**M1 — Candidate's "fetch spellings are a separate class" is implemented on one side only, turning any URL read into a guaranteed unexplained row (candidate contract statement wrong).**

Candidate `canonical_event` skips components matching `(?i)^https?://` or `^[^/:\s]+:[0-9]+/` (continue → not denied), but `rough_event` has no such exclusion: the rough side strips and compares the URL string against `read_paths`, which never contains it → `('path', 0)`, `rough_path_count = 1`. Then the disposition ladder: `agree` needs `1 == 0 == 0` → no; `selector-normalization` requires the rough-stripped string to differ from the canonical base — for `https://example.com/x` `canonical_base` returns the value unchanged (tokens `['//example.com/x']` are not selector tokens), so they are **equal** → the branch is refused; `unit-difference` needs `kept == len(canonical) > 1` → no → row = `unexplained` → `RECONCILIATION-UNEXPLAINED`.

So the docstring's promise ("fetch spellings are a separate class") is not delivered by the implementation: a URL-valued read is an unexplainable row rather than a separate class. Draft side counts the URL as a canonical denial → `rough and bad and kept(0)` fails → `unit-difference` → `lane_valid` False → `COHORT-UNEXPLAINED`: also a failure, but with a different ID and a different (coherent) mechanism. Neither side is right; the class must exist on **both** classifiers.

Remedy (candidate): apply the same URL/fetch exclusion in `rough_event` (or route such components into a distinct `fetch` class excluded from both cohorts and counted separately).

**M2 — Candidate hardcodes `skill://godspeed` and the absolute lane prefix instead of honouring literal per-seat membership (candidate wrong in principle).**

Candidate `canonical_base` special-cases only the literal `skill://godspeed`; `canonical_event` continues only when `base == 'skill://godspeed' and base in authority`. Any other bound URI — e.g. `skill://shokunin`, which is a legal skill URI in this estate — falls through to `_local`, which requires the path to start with the hardcoded absolute `LANE + '/'` → `_local` false → `bad`. The draft treats **any** exact member as authoritative (`if component in members: continue`), matching "skill URIs are literal members".

Literal case: `read_paths = ['skill://shokunin']`, event `read` `args.path = 'skill://shokunin'` → candidate: `canonical = [0]` (denied) vs retained 0 → `unexplained` → cohort FAIL; draft: member → clean → agree.

Related hardcoding: `_local` requires `path.startswith('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/')` and rejects any path containing `*?[];:`. A bound member that is relative, or that contains a glob metacharacter, is denied by the candidate although the draft (exact membership) would accept it. The r22 member paths are outside this seat's read scope, so I cannot confirm which shape the frozen bindings use — but the literal-membership rule is the one both the preregister and the draft state.

Remedy (candidate): derive membership from the binding only (exact member after selector strip), and keep the dot-segment / control-character rejection as a *separate* guard; drop the LANE-prefix and hardcoded-URI special cases.

**M3 — Candidate omits three roster/shape controls the draft has (draft stronger).**

1. Roster identity across all three frozen sources: draft `check_roster` requires the events, bindings **and audit** seat sets to be equal, names to match `[A-Za-z0-9][A-Za-z0-9._-]{0,127}`, and no duplicates → `SNAPSHOT-SCHEMA` (exit 2). Candidate `derive` checks only events↔bindings (`set(bound) != names` → `RECONCILIATION-INPUT-MALFORMED`, exit 2) and never inspects the audit's seat roster — an audit whose seat roster disagrees with the events passes the landed gate.
2. Schema fields on the frozen snapshots: draft enforces `tsukuroi-seat-events-v1` / `tsukuroi-seat-bindings-v1` and the audit shape (`findings` list + `seats` list); candidate enforces neither (it only needs `seats`/`events`/`findings` keys to exist), so a snapshot file with the wrong schema but the right shape passes.
3. Audit site format: draft requires `':'` in the site, a numeric index, and a seat present in the roster (else `SNAPSHOT-SCHEMA`); candidate accepts any string and reports a non-matching site as `RECONCILIATION-ORPHAN-FINDING` (exit 1).

Remedy (candidate): port the roster cross-check and the two snapshot schema assertions from the draft; keep the candidate's orphan finding as an *additional*, not a replacement, signal.

**M4 — `unexplained_cohorts` is `null` under CANNOT_EVALUATE and cohort accounting counts record defects as unexplained cohorts (candidate wrong for the C3 metric).**

The candidate's `evaluate` returns `unexplained_cohorts=None` on every CANNOT_EVALUATE path (`SNAPSHOT-MISSING`, `SNAPSHOT-TAMPERED`, `RECONCILIATION-PINS`, `RECONCILIATION-INPUT-MALFORMED`, and in `main` for `RevisionError` / `Unevaluable` / read errors), while the C3 metric in the preregister is an integer count (`before: 2`). The draft consistently reports `2` (`finish(2, len(LANES))`). A metric extractor reading `null` cannot compare it to 0 or 2.

Second half: candidate `unexplained += bool(local)` where `local` includes `RECONCILIATION-LEDGER-MISMATCH` and `RECONCILIATION-ARITHMETIC` — record-integrity defects are counted as *unexplained cohorts*, whereas the draft separates them (`RECONCILIATION-MISMATCH` + `RECONCILIATION-ARITHMETIC` with `unexplained_cohorts = 0` for a pure arithmetic defect, as its own selftest `wrong-arithmetic` expects). Under the candidate a single forged ledger row reports `unexplained_cohorts = 1`, i.e. a record defect masquerades as a cohort explanation failure.

Remedy (candidate): report `unexplained_cohorts = len(COHORTS)` (2) on CANNOT_EVALUATE, and count only cohort-explanation findings (row-level `unexplained`, count mismatches, canonical mismatch) toward `unexplained_cohorts`.

**M5 — The wave-1 report's record guidance is void against the landed tool; records produced from the draft are rejected by the landed gate (report wrong, candidate authoritative).**

The two tools define mutually unreadable records:

| aspect | candidate (landed) | draft |
|---|---|---|
| record keys | exactly `{schema, inputs_sha256, cohorts}` | `{schema, unexplained_cohorts, source_counts, lane_counts, lanes}` |
| cohort container | list, ordered `build`,`falsify` | dict keyed by wave |
| cohort body | `{wave, rows, orphan_retained_sites, totals}` | `{wave, rough_path_events, retained_path_sites, rows}` |
| row identity | `site` (`seat:index`) | `seat` + `index` + computed `identity` digest |
| rough detail | `rough_category` ∈ clean/path/exec/unknown, `rough_first_bad` = **index** | `rough_class`, `rough_first_bad` = **component string** |
| counts | `rough_path_count`, `canonical_path_count`, `retained_path_count` | `rough_path_failures`, `canonical_path_failures`, `retained_sites` |
| dispositions | `agree`, `selector-normalization`, `unit-difference`, `unexplained` | `non-path`, `agreement`, `selector-normalization`, `unit-difference` |
| generator | `--emit-ledger` (self-producing) | none (report says L1 constructs it) |

A record built from the draft's `derive()` fails the landed gate with `RECONCILIATION-SCHEMA` (candidate requires the exact key set and the pins digest) — exit 1, permanently. The wave-1 report's statement "`derive()` is the intended generator. First integration run should be exit 1 `RECONCILIATION-MISSING`, then 0 after the record lands" is therefore not executable against the landed tool, and its disposition vocabulary does not exist in the landed code. Any integration performed from the wave-1 report alone would land an unreadable record.

### LOW

- **L1 (candidate right, keep).** Candidate's `selector-normalization` predicate additionally requires the rough-stripped string to differ from the canonical base, which the draft does not check. That refuses to label a genuine denial (e.g. `<LANE>/x.md:foo`, invalid token) as a selector artifact; the draft's looser rule would mislabel such rows. Keep the candidate's form.
- **L2 (candidate right, keep).** Candidate's selector token set accepts `raw`, `img`, `conflicts` and range tokens; the draft accepts only `raw` + digit/range family, so a bound file read as `<LANE>/a.md:img` is clean in the candidate and denied by the draft. The `img`/`conflicts` selectors are real read-tool selectors, so the candidate's grammar is the better one; the draft should adopt it.
- **L3 (exit divergence).** Malformed committed record: candidate → exit 1 `FAIL` + `RECONCILIATION-SCHEMA`; draft → exit 2 `CANNOT_EVALUATE` + `RECONCILIATION-SCHEMA`. Same ID, different exit and status; the candidate's selftest pins exit 1, the draft's selftest pins exit 2. Other exit/ID pairs that differ for the same condition: missing frozen input (candidate `SNAPSHOT-MISSING` exit 2 vs draft `SNAPSHOT-TAMPERED`/`SNAPSHOT-READ-FAILED` exit 2 — candidate's distinction is better), roster mismatch (candidate `RECONCILIATION-INPUT-MALFORMED` vs draft `SNAPSHOT-SCHEMA`), frozen manifest shape (candidate `RECONCILIATION-PINS` vs draft `FROZEN-SCHEMA`), count mismatch (candidate `RECONCILIATION-ROUGH-COUNT` + `RECONCILIATION-RETAINED-COUNT` vs draft `LANE-CENSUS-MISMATCH`), unexplained cohort (candidate `RECONCILIATION-UNEXPLAINED` vs draft `COHORT-UNEXPLAINED`), record mismatch (candidate `RECONCILIATION-LEDGER-MISMATCH` vs draft `RECONCILIATION-MISMATCH`), read error (candidate `RECONCILIATION-READ` vs draft `E-READ`). Only four IDs are shared (`SNAPSHOT-TAMPERED`, `RECONCILIATION-MISSING`, `RECONCILIATION-SCHEMA`, `RECONCILIATION-ARITHMETIC`); any consumer keyed on the wave-1 IDs must be updated to the candidate's set, and the two core-outcome IDs should be stabilised.
- **L4 (control/ID granularity).** Draft additionally validates each pinned input path (relative, no traversal, no absolute, no control chars) and each digest as 64 lowercase hex (`FROZEN-SCHEMA`), and computes its own per-row identity digest instead of trusting the snapshot's `call_id`/`request_arguments_sha256`; the candidate trusts the audited artifact's own digest fields and validates neither path nor digest form. Draft is stronger on both points.
- **L5.** Candidate's `--emit-ledger` prints a recomputed ledger even when that ledger contains `unexplained` rows, i.e. it can emit a record that its own gate will then FAIL — a self-inconsistent artifact can be committed. Draft has no generator (L1's role).
- **L6 (misleading coverage).** Candidate's selftest exercises `unit-difference` only with forged duplicate sites (`audit('S:0','S:0')`) — a shape real r22 audits do not have — and never exercises the real component>site case; the draft's selftest fixture uses absolute member paths and therefore contradicts its own expectations (H2). Neither selftest was executed by its author (NO-EXEC), and both are green-looking for the wrong reason.
- **L7 (error-ID mislabel).** Candidate `cohort_findings` runs **outside** the `try` that guards `derive`; a malformed `pins['expected'][wave]` (e.g. missing `rough_as_reported`) raises `KeyError` there, is caught by `main`'s generic handler, and is reported as exit 2 `RECONCILIATION-READ` / site `revision` — a read-failure label for a data-shape defect. Draft reports `FROZEN-SCHEMA`.

## Divergence inventory (compact)

| # | surface | candidate | draft | side that is right |
|---|---|---|---|---|
| D1 | canonical count unit compared to retained | component count vs site count | event-level only | draft |
| D2 | absolute member + selector suffix | clean (strip first) | denied (`''` part ⇒ rejected) | candidate |
| D3 | selector token set | `raw`/`img`/`conflicts`/ranges | `raw`/ranges only | candidate |
| D4 | URL/fetch class | canonical-only ⇒ guaranteed `unexplained` | counted as denial ⇒ `unit-difference` | neither; class must be on both sides |
| D5 | membership test | exact member **and** LANE-prefix **and** hardcoded `skill://godspeed` | exact member (+ dot/control guard) | draft |
| D6 | disposition vocabulary | `agree`/`selector-normalization`/`unit-difference`/`unexplained` | `non-path`/`agreement`/`selector-normalization`/`unit-difference` | draft (keeps non-path separate); candidate must add `non-path` count |
| D7 | `agree` strictness | `rough == canonical == kept` (exact) | truthy conjunction | candidate is stricter but wrong here (D1) |
| D8 | `unit-difference` reachability | needs duplicate site ⇒ dead on real audit shape | any leftover | candidate (fix predicate per H1) |
| D9 | `selector-normalization` soundness | requires stripped ≠ canonical base | unchecked | candidate |
| D10 | arithmetic | cross-unit equality + `unit_extra` term | row-level `lane_valid` + reported counts | draft |
| D11 | record schema | `{schema, inputs_sha256, cohorts[]}` | `{schema, unexplained_cohorts, source_counts, lane_counts, lanes{}}` | candidate (landed) — wave-1 report void |
| D12 | finding-ID vocabulary | 14 candidate IDs | 12 draft IDs, 4 shared | candidate (landed), stabilise core two |
| D13 | exit codes for identical conditions | 1 for malformed record; 2 elsewhere | 2 for malformed record | disagreement; either is defensible, must be pinned |
| D14 | `unexplained_cohorts` under CANNOT_EVALUATE | `null` | `2` | draft |
| D15 | cohort accounting of record defects | counted as unexplained cohort | separated | draft |
| D16 | roster cross-check (events/bindings/audit) | events↔bindings only | all three + name charset | draft |
| D17 | frozen snapshot schema assertions | none | events/bindings schema + audit shape | draft |
| D18 | audit site format validation | none (unmatchable ⇒ orphan) | `':'` + numeric + roster seat | draft (keep orphan as extra) |
| D19 | pins manifest path/digest hygiene | none | path safety + 64-hex digest | draft |
| D20 | row identity binding | trusts snapshot `call_id`/`request_arguments_sha256` | computed digest | draft |
| D21 | record key strictness | exact key set | subset | candidate (brittle to provenance keys) |
| D22 | CLI path surface | fixed paths, no spec surface | `--record`/`--frozen` + `safe_path` | candidate |
| D23 | ledger generator | `--emit-ledger` (can emit a self-failing record) | none | candidate |
| D24 | pins `expected` shape error ID | `RECONCILIATION-READ` (mislabel) | `FROZEN-SCHEMA` | draft |
| D25 | selftest realism | forged duplicate sites; no multi-denied event | absolute-member fixture contradicting own expectations | neither |

## Bounded search performed, and what it found

Searched, by full raw read of both files plus targeted comparison of every decision predicate, ID string, exit code, disposition label, record field, and CLI flag in the two implementations (no execution): the six surfaces listed under Method. Result: 25 divergences (table above), of which 2 are HIGH, 3 MEDIUM, 7 LOW. No divergence was found in: the rough classifier (both use the same `:(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$` suffix rule, applied to `read`/`grep` only, first failing component wins, `bash`→`exec`, other tools→`unknown`); the `;`-component split for `grep`/`glob`; the read/write authority split (`write`→`write_paths`, others→`read_paths`); the snapshot-digest-first gate (both hash every frozen input before evaluating, exit 2 on mismatch); strict duplicate-key JSON parsing in both; the `git show`+`ls-tree` read path; and the `--revision`/`--branch`/`_revision.bind` binding surface. The rough-side census arithmetic (25/33 reported vs 23/29 retained) is therefore identical on both sides, and the *only* places the two implementations can disagree about the real r22 data are D1–D5 and D7–D10.

Concrete falsifiers (hand-traced, not executed):

- F1 (H1): `grep` over two unbound components with one retained site → candidate `unexplained` + `RECONCILIATION-CANONICAL-MISMATCH` ⇒ exit 1; draft ⇒ cohort can pass.
- F2 (H2): `read` of an absolute bound member with `:raw` → candidate clean/`agree`; draft `component_rejected` ⇒ `unit-difference` ⇒ `COHORT-UNEXPLAINED`, and the draft's own `clean` selftest case and `mixed-raw-first` assertion fail.
- F3 (M1): `read` of `https://example.com/x` → candidate `unexplained` (its own docstring says fetch spellings are a separate class).
- F4 (M2): `read` of `skill://shokunin` bound for the seat → candidate denies, draft accepts.
- F5 (M5): a record built from the draft's `derive()` → candidate `RECONCILIATION-SCHEMA`, exit 1, permanently unreadable.

## Smallest in-scope remedy

Production (`tools/check-path-reconciliation.py`, candidate) — one predicate change plus two one-liners:

1. **H1:** in `derive`, add `canonical_denied = bool(canonical)` per row; count `totals['canonical_path']` in denied **events**; change the disposition ladder so `len(canonical) > kept >= 1` (component-vs-site) is `unit-difference` (explained), and `rough_count == 1 and kept == len(canonical) > 1` is the per-event-vs-per-component label it was meant to be; rebase `RECONCILIATION-CANONICAL-MISMATCH` onto the event-level comparison; add one selftest fixture with a two-denied-component grep event (this is also the missing coverage in L6).
2. **M1:** apply the URL/fetch exclusion inside `rough_event` as well (or classify such components into a separate `fetch` class excluded from both cohorts).
3. **M4:** return `unexplained_cohorts=len(COHORTS)` on CANNOT_EVALUATE paths, and exclude record-integrity findings from the cohort-unexplained count.

Optional but cheap, same file: **M2** (drop the hardcoded `skill://godspeed` and LANE-prefix gates; keep exact membership plus a separate dot/control guard), **M3** (port the draft's roster cross-check and snapshot schema assertions), **L7** (move `cohort_findings` inside the guarded block and label pins-shape errors `RECONCILIATION-PINS`).

Wave-1 artifacts (not production, no edit performed by this seat): the draft's `component_rejected` must stop treating absolute paths as dot-segment rejections, and its selftest expectations plus the build report's "23/29 canonical == retained" and "`derive()` is the intended generator" statements must be re-derived before they are cited as evidence. Until then the wave-1 report is not a usable integration guide for the landed record (M5).

## Residual risk

- **Highest residual risk is unmeasured, not unthought:** whether the frozen r22 events actually contain a multi-denied-component event (H1), a URL-valued read (M1), a non-`skill://godspeed` bound URI or a relative member path (M2) is not decidable from this seat's declared read scope — the frozen inputs, snapshot, bindings and the committed `path-reconciliation.json` are outside it. If H1/M1 do not occur in the fixed data, the landed gate may still exit 0 today, while the latent false-failure remains and the C3 metric's reachability is unproven rather than demonstrated.
- The landed candidate's `RECONCILIATION-CANONICAL-MISMATCH` currently compares units; if the frozen data happens to have exactly one denied component per denied event, the check passes for the wrong reason and would mask a future lane undercount (components > sites) as well as a lane overcount (components < sites). The defect is symmetric in direction but the failure mode is always FAIL, not a silent pass.
- The candidate's `edit` tool path is excluded from the path cohort (`canonical_event` returns `[]` for tools outside `read/grep/glob/write`), as in the draft. If any r22 `SCOPE-PATH-DENIED` site belongs to an `edit` event, both sides undercount and the retained-vs-canonical comparison fails for reasons unrelated to the classifier difference. Unverifiable from declared files.
- No claim of native runtime enforcement is made anywhere in this report; the tool is a static gate over frozen bytes, and the round-24 follow-up surface is out of scope for this seat.

## Verification gaps

1. No execution, import, compile, test, lint, format, hash, wc, or listing was performed (NO-EXEC/NO-FETCH seat, `commands: []`, `fetches: []`). Every "→" is a hand trace over quoted source; the draft selftest failure (H2) is hand-traced, not observed.
2. The reviewed digest `fd0393be9140579424bdfc3c099b2b82fee11ccf9306d926c998235ce7ee1a6b` is a supplied identity and was **not** independently computed.
3. The frozen inputs, the r22 snapshot (events/bindings/audits), and the committed `.ufo/waves/round-23/path-reconciliation.json` were not read (outside this seat's declared read paths), so: (a) the real member-path shape and the real per-event component counts are unconfirmed; (b) whether the landed record was produced by the candidate's `--emit-ledger` and with which disposition vocabulary is unconfirmed; (c) the candidate's end-to-end exit code on the landed revision is unconfirmed.
4. No LSP server was available for this seat (the reviewed files are standalone Python with no workspace server declared under the seat's tooling authorization, and the contract forbids extra filesystem search and all execution); therefore all caller/reference/diagnostic checks in this report are literal source reads, recorded as such — no semantic-equivalence claim is made from grep output.
5. Installations: none. The tooling directive is noted; this seat's NO-EXEC/NO-FETCH scope forbids installation, and no tool was needed beyond the declared read/write paths.

Reviewed-SHA256: fd0393be9140579424bdfc3c099b2b82fee11ccf9306d926c998235ce7ee1a6b
Predicate: r23f-fxdraftexecreconciliation
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
