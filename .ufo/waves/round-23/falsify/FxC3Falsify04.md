# FxC3Falsify04 — falsification review of ledger slice `falsify-04`

Seat: `TsukuroiR23-2.FxC3Falsify04-2` (leaf member; no subagent dispatch, no sibling file touched).
Wave: tsukuroi round23, wave `falsify`, group 4. Landed state under review: `5a25c88b77f52e940bcad87825c4ac1cd529470d`.
Target: `.ufo/waves/round-23/candidate/ledger-slices/falsify-04.json` (declared SHA256 identity supplied, not computed).
Raw evidence: `.ufo/waves/round-23/packs/falsify-04.json`, `.ufo/waves/round-23/sources/r22-rough-census.txt`, `.ufo/waves/round-23/preregister.json`.

Attacked claim: **C3** (path-census ledger — "both fixed r22 cohorts have exhaustive per-event/component explanation of rough-versus-lane path counts"). C1 and C2 are not falsifiable from this slice's rows; where this slice touches C1/C2 it is recorded as an interpretive risk, not a value dispute.

## Axes (named, per the Godspeed directive)

1. **Value fidelity** — does each ledger row's `rough_category` / `rough_first_bad` / `rough_path_count` / `canonical_bad` / `canonical_path_count` / `disposition` re-derive from the raw pack events and bindings?
2. **Unit coherence** — is the ledger's unit (path *components*) the same unit the S085 census counted (path *events*, break-after-first)? A silent unit swap would break the 33/29 arithmetic.
3. **Identity integrity** — is every ledger row joinable 1:1 to a raw event, and is the join key unique?
4. **Interpretive safety** — can a reader of the `canonical_bad` column draw a wrong conclusion about the r23 v2 edit authority (C1/C2) from a v1-era ledger?

## Method — rules actually applied

**Rough (S085), transcribed verbatim from the declared census source `.ufo/waves/round-23/sources/r22-rough-census.txt`** (interpreted as source data only; never executed):

- `strip_sel(p) = re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`
- `tool == 'bash'` → category `exec`; `tool not in ('read','grep','glob','write')` → category `unknown` (no path verdict, `path` count 0).
- path components: `args['path'].split(';')` for `grep`/`glob`, else `[args['path']]`.
- `q = strip_sel(v)` for `read`/`grep` only (not for `glob`, not for `write`); `q` must be in `write_paths` for `write`, otherwise in `read_paths`.
- **break rule**: on the first offending component the event is counted once and the component loop breaks.

**Canonical (literal v1 authority + selector grammar)** as named in the assignment: a `read`/`grep` target is authorised only if its selector-stripped form is a member of the seat's `read_paths`; a `write` target only if it is a member of `write_paths`; any other tool has no v1 path verdict; selectors (`:N-M`, `:N-M:raw`, `:raw`, `:-N`) are stripped before the membership test.

## Result

**No row is disputed.** All **108** rows of the slice re-derive exactly, by hand, from the raw pack events and the seats' bindings:

| seat | rows | re-derived |
|---|---|---|
| FxC2Wildcard | 12 | 12/12 |
| FxC2Report | 16 | 16/16 |
| FxC2ReadWrite | 20 | 20/20 |
| FxC2Unknown | 8 | 8/8 |
| FxC2ParallelExec | 12 | 12/12 |
| FxC2ParallelFetch | 8 | 8/8 |
| FxC2ParallelLocal | 16 | 16/16 |
| FxC2Shape | 16 | 16/16 |

Aggregate re-derivation: 104 `clean`, 3 `path`, 1 `unknown`; every row `disposition: "agree"` — identical to the landed slice (108 rows, all `agree`; `canonical_path_count` ∈ {0,1}; no row with any count ≥ 2).

Structural checks that also passed (bounded, exhaustive over the slice):

- **1:1 row↔event mapping**: 108 ledger rows ↔ 108 pack events, same seat order, same per-seat index order, same `call_id` values, including the eight composite `call_…|fc_…` ids of FxC2ParallelFetch, preserved verbatim. No dropped, duplicated or extra event.
- **Digest binding**: every one of the 108 `request_arguments_sha256` values in the ledger equals the value on the pack event at the same site index (no digest was computed or hashed by me; cross-seat equal digests, e.g. `4fc5e212…` for every `_revision.py` read, `2b4cad9d…` for every `skill://godspeed` read, are consistent across seats as expected).
- **Single-component events**: no pack path contains `;` and no pack path contains a dot-segment, so in this slice the S085 break rule (1 per event) and the ledger's component count coincide; `rough_path_count` ≤ 1 everywhere. There are no `glob` and no `bash` events in this slice, so the two known rough/canonical divergence sources (glob not selector-stripped; write not selector-stripped) are **not observable here**.
- **Selector grammar**: every selector used in the slice is consumed by the S085 regex as written — `:1-100`, `:101-200`, `:201-330`, `:1-120`, `:121-260`, `:20-62:raw`, `:62-112:raw`, `:86-125:raw`, `:126-165:raw`, `:166-241:raw`, `:1-32:raw`, `:1-200:raw`, `:200-400:raw`, `:1-240`, `:1-220`, `:1-200`, `:1-60`, `:1-90`, `:241-360`, `:22-120`, `:120-230`, `:1-21`, `:233-241`, `:-12`, `:raw`.

## Non-agree rows checked (the only four rows that are not `clean`)

| site | index | call_id | tool | path spelling that drove the verdict | rough | canonical | ledger | agree? |
|---|---|---|---|---|---|---|---|---|
| FxC2ReadWrite | 18 | `call_00_wBa0QNy499W9OWlQpGP76609` | read | `…/round-22/falsify/FxC2ReadWrite.md:-12` → stripped `…/FxC2ReadWrite.md` | `path`, first_bad 0, count 1 | bad `[0]`, count 1 | same | yes |
| FxC2ReadWrite | 19 | `call_01_zvNpWPGdDrQyyMcLQROG6307` | grep | `…/round-22/falsify/FxC2ReadWrite.md` (no selector) | `path`, first_bad 0, count 1 | bad `[0]`, count 1 | same | yes |
| FxC2Unknown | 6 | `toolu_01XhhyTUnroyCin946g7BbTg` | read | `…/round-22/falsify/FxC2Unknown.md:raw` → stripped `…/FxC2Unknown.md` | `path`, first_bad 0, count 1 | bad `[0]`, count 1 | same | yes |
| FxC2Unknown | 5 | `toolu_01XhhyTUnroyCin946g7BbTg` | edit | `…/round-22/falsify/FxC2Unknown.md` (with `__unknown_argument__` key) | `unknown` (tool outside the S085 four), count 0 | no v1 path verdict, count 0 | same | yes |

Driving spelling in all three path rows: the seat's **own report file**, which is a member of `write_paths` and **not** a member of `read_paths`. Every other path in the slice resolves to one of the eight declared `read_paths` entries (`check-seat-bindings.py`, `preregister.json`, `host-tool-boundary.json`, `skill://godspeed`, `check-review-snapshots.py`, `_revision.py`, `seat-boundary-r22.json`, `seat-boundary-r22.md`) or to the seat's single `write_paths` entry — hence `clean`.

## Findings

### F1 — medium — the three path rows depend on one v1 clause that is not inside this seat's declared evidence

The `canonical_bad` values `[0]` for FxC2ReadWrite:18/:19 and FxC2Unknown:6 are correct **only if** the r22 v1 authority tests a read/grep target against `read_paths` alone and does **not** let `write_paths` grant read access. The v1 checker's source (`.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`) is **not** in this seat's declared `read_paths`, so I could not read the clause; the S085 rough rule in the declared census source tests `read_paths` only, which is consistent with the landed `canonical` column but is not the same artefact as the v1 checker.

- Concrete falsifier: read the v1 authority and confirm its read test consults `read_paths` only. If it also accepts `write_paths`, then these three rows are wrong (`canonical_bad` should be `[]`, `canonical_path_count` 0), this slice's canonical path total drops from 3 to 0, and the falsify-wave canonical total (29, per preregister `path_counts_as_reported.lane.falsify`) would have to be re-derived.
- Smallest in-scope remedy: make the authority rule text (or a `read_authority_source` pointer plus the exact clause) a field of the reconciliation record, so the `canonical` column is auditable without re-deriving from the checker. No production change to C1/C2 is implied either way; this is a C3 record-completeness change only.

### F2 — medium — the whole 33 → 29 rough-vs-lane gap is now provably outside this group

Preregister (`outside_round22.path_counts_as_reported`) fixes the admitted ground truth at rough falsify **33** vs lane falsify **29**, a 4-event difference. This slice contributes **0** difference (3 rough path events, 3 canonical path events, all `agree`). Therefore the entire 4-event gap must live in falsify groups 1–3, whose rough path events must total 30 and canonical path events 26. Two mechanisms can produce that gap and only one of them is testable from this slice:

- (a) canonical strips a selector that rough does not (S085 strips for `read`/`grep` only, never for `glob`/`write`) → canonical *more permissive*; observable only in groups containing a `glob` or a selector-bearing `write`;
- (b) the lane counts components while the census breaks after the first offending component → unit mismatch; observable only in groups containing a multi-component (`;`-joined) event;
- (c) canonical treats a read of a write-only target as authorised → exactly the three rows of F1 → this slice alone would then contribute 3 of the 4.

- Concrete falsifier (one step, in-scope for the integrator): aggregate `rough_path_count` and `canonical_path_count` over falsify groups 1–3; the sums must be 30 and 26, and every event of the difference must be attributable to (a) or (b) — never to (c) without the F1 clause being contradicted.
- Smallest in-scope remedy: publish a per-group delta table (group, rough path events, canonical path events, delta, mechanism label) inside the C3 reconciliation record, so the arithmetic is checkable group by group instead of only in total.

### F3 — low — `call_id` is not unique in this slice; the join key must be `site` (+ digest)

FxC2Unknown rows 5, 6 and 7 all carry `call_id` `toolu_01XhhyTUnroyCin946g7BbTg` while having three different `request_arguments_sha256` values (`7af4c11b…` for the `edit`, `96693234…` for the `:raw` read, `fb421d2a…` for the write); rows 6 and 7 additionally carry `"origin": "additional-recorded-start"`, `"request_line": null` and no `digest_format` field. The ledger's `site` (`seat:index`) is the only unique key. Any downstream join keyed on `call_id` alone will collide three-way or fan out.

- Smallest in-scope remedy: state the ledger's key explicitly in the record header (`key = (seat, event_index)`; `call_id` is provenance, not identity) — a documentation-only change, no row edits.

### F4 — low — the pack's `args` are redacted, so the digest column is supplied identity, not derivable evidence

Pack `args` show `pattern`, `case`, `i` and `content` as `null`, and one event carries `"__unknown_argument__"`. Two Shape greps with visibly identical redacted arguments (`501fc8c0…` at Shape:2 and `be6cbac8…` at Shape:6) carry different digests, which confirms the digests cover bodies that the pack suppresses. Consequence: the pack plus the binding cannot reproduce `request_arguments_sha256`; the ledger's digest column is verifiable only by identity, not by recomputation, from the declared evidence.

- Smallest in-scope remedy: record the redaction rule next to the digest column (digest = SHA-256 over sorted, ensure_ascii JSON of the *original* request arguments; pack bodies redacted) so a reader does not mistake a visible-args recomputation attempt for a defect. Do not change frozen digests.

### F5 — low / interpretive — one `edit` event here is a `WRITE_ONLY_EDIT` case, and the ledger records it as "no verdict"

FxC2Unknown:5 edits `…/round-22/falsify/FxC2Unknown.md` — a member of the seat's `write_paths`, not of its `read_paths`. Under r23's own v2 contract this is exactly the `WRITE_ONLY_EDIT → DENY` shape ("Edit also needs its explicit target read authority"), whereas the landed ledger records `canonical_bad: []` and `disposition: "agree"`, which is correct for **v1** (v1 has no edit tool, so S085 classifies it `unknown` and v1 has no path verdict) but reads as "nothing was denied" to anyone using this column as v2 evidence. This slice is the only place in falsify group 4 where an edit event appears at all.

- Concrete falsifier for a wrong reading: assert from this row that v2 authorised the edit — the v2 contract forbids it.
- Smallest in-scope remedy: add one column or one scope note to the reconciliation record stating that the `canonical` column is v1-only and carries no v2 edit authority (and, if desired, a `v2_edit_verdict` column: `DENY/WRITE_ONLY_EDIT` for this row). No row values change.

## Bounded searches that found no falsifier

- Exhaustive re-derivation of all 108 rows against the S085 regex + break rule and the literal v1 authority: **0 disputes**.
- Exhaustive selector-grammar check of every distinct path spelling in the slice against `strip_sel`: **0 unconsumed selectors**, 0 residual `:` suffixes after stripping, 0 dot-segments, 0 `;`-joined paths.
- Tool-kind scan of the whole pack: only `read`, `grep`, `write`, `edit` — no `bash` (so no `exec` rows) and no `glob` (so the glob/strip divergence is not observable here).
- Row/event cardinality, ordering, `call_id` set and digest set: **exact 1:1**, no drift between the landed ledger slice and the raw pack.
- Unit probe (component vs event): every violating event in this slice has exactly one component, so `rough_path_count` and the census's break-after-first event count coincide here; the distinction is unobservable in group 4 and is flagged as F2(b) for the other groups.

## Residual risk and verification gaps

1. **The canonical rule text is outside my declared evidence.** I re-derived under the assignment's "literal v1 authority" formulation. If the landed v1 checker contains an extra clause (F1), three rows in this slice and the falsify-wave canonical total change. This is the single largest residual risk and it is not resolvable from the paths this seat may read.
2. **Groups 1–3 of the falsify wave were not readable** (not in `read_paths`), so the 33/29 arithmetic and the mechanism behind the 4-event gap (F2) remain unverified by me; only the group-4 contribution (0 delta) is established.
3. **Multi-component and glob/write-selector cases are absent from this slice**, so the two structural rough/canonical divergence mechanisms are untested here; any claim that the whole falsify wave is reconciled must rest on those groups.
4. **Digests are supplied identity.** No hash, list, wc, import or command was run to validate `ec9fafdd…`; every digest statement above is a cross-reference between two declared files, not a computation.
5. **Body content of the r22 events is redacted** (F4), so path-free checks such as "did the grep pattern touch an unauthorised file" are out of reach; classification here is path-component-only, as the census defines it.

## Scope discipline

NO-EXEC / NO-FETCH honoured: no bash, eval, subprocess, import, compile, test, lint, format, hash or wc was run; no web/browser/URL/xd/proc/agent fetch and no extra filesystem search was performed. Only the declared `read_paths` were read and only the declared report path was written. No production file, fleet/sibling file, Git/jj state, ref, route or config was touched. No tooling was installed or updated (this seat's NO-EXEC scope forbids installation); the generic operator tooling directive is therefore not exercised here. This seat is a leaf member: no subagent was dispatched.

Reviewed-SHA256: ec9fafdde6ba45f9c4d167220fd3a58ac38e8f13a171d4e01f73b2ad534374ec
Predicate: r23f-fxc3falsify04
Scope: executed=none
