# FxC3Build06 — falsification of the r23 build-06 path-census ledger slice

Seat: FxC3Build06 (reviewer, leaf)
Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/ledger-slices/build-06.json`
Declared SHA256 of target: 8e285eec3e107094d5fb347b900863116291721d7d6a4c107f091c1ad8318edc (supplied declaration; not independently computed, per receipt rule)
Companion evidence read: `.ufo/waves/round-23/packs/build-06.json` (raw preserved request metadata), `.ufo/waves/round-23/preregister.json`, `.ufo/waves/round-23/sources/r22-rough-census.txt` (S085 rough path-census source cell), `.ufo/waves/round-23/sources/godspeed-directive.txt`
Landed revision under attack: 5a25c88b77f52e940bcad87825c4ac1cd529470d (matches the slice's own `landed` field)
Baseline for reference: ae01e50f582016384e620022be38bf5367000e2e

## Attacked claim

**C3 (calibration) — "Both fixed r22 cohorts have exhaustive per-event/component explanation of rough-versus-lane path counts, frozen digests and declared arithmetic."** Concretely, for this slice: every row of the landed build-06 ledger must be re-derivable from the raw pack events plus the seat bindings by (a) the exact S085 rough classifier and break rule, and (b) literal v1 authority plus the canonical selector grammar, with the disposition being an honest statement of rough-vs-canonical agreement at that event.

C1/C2 are not the primary target of this slice, but the two `edit` rows in it touch C1's `OPAQUE_PATCH → UNKNOWN` and `WRITE_ONLY_EDIT → DENY` decisions and C2's "explicit schema-v2 audit authority for exact predeclared structured edit targets"; that adjacency is reported under F1 below and is not used to dispute any recorded path count.

## Method (NO-EXEC, NO-FETCH)

Every derivation below is by hand from the two JSON artifacts using only read-side structured queries (`read` with a JSON projection filter) on the four declared local paths. No `bash`, `eval`, subprocess, import, compile, test, lint, format, hash, `wc`, or `mkdir` was run; no network/fetch occurred; no subagent was dispatched. The declared digest was carried as identity and never recomputed.

Re-derivation of the rough side used the S085 source cell exactly as recorded in `sources/r22-rough-census.txt`:

- `strip_sel(p) = re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`
- `bash` → `exec` counter, `continue` (no path inspection)
- tool not in `('read','grep','glob','write')` → `unknown` counter, `continue` (no path inspection)
- `read`/`write` → one component; `grep`/`glob` → `path.split(';')`
- `strip_sel` applied only to `read` and `grep`; `write` compared unstripped
- membership against `write_paths` for `write`, otherwise `read_paths`
- `f['path'] += 1` then **`break`** — the rough count is **per event**, and only the first failing component is recorded

I applied that rule independently to all 72 pack events against all 8 seat bindings and compared the result to every ledger row field (`rough_category`, `rough_first_bad`, `rough_path_count`, `canonical_bad`, `canonical_path_count`, `retained_path_count`, `disposition`), and also re-derived the canonical side under literal v1 authority (read/grep component ∈ `read_paths` after selector strip; write target ∈ `write_paths`; edit target ∈ `write_paths`).

## Join and structural integrity of the slice

- Pack: 8 seats, 72 events, 0 `commands` and 0 `fetches` for every seat, single `root` `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, binding `name` always equal to seat `name`.
- Ledger slice: 72 rows, `wave=build`, `group=6`, `landed=5a25c88b…` — all three agree with the pack and with the round-23 assignment.
- Seat sets: pack seat names == slice `seats` array (8 names, same set, different order). Slice `seats` includes `OracleReceiptPredicate`, which has **zero** events and therefore zero rows.
- Row↔event join is exact and order-preserving: the 20-hex `request_arguments_sha256` sequence emitted per seat from the pack (`seat#index=digest`) is character-identical to the one emitted from the ledger rows, for all 7 row-bearing seats, index 0…n-1 with no drift, no reordering, no insertion and no deletion. Per-seat row counts match per-seat event counts exactly (Period 11, Digest 6, Duplicate 10, CRLF 16, Unicode 6, Dead 8, Unknown 15 = 72).
- `request_arguments_sha256` is not a unique key in either file (68 distinct of 72). The duplicated values are explained, not suspicious: the digest is over the arguments object, and the same file path requested with different argument sets yields different digests. The pair `(call_id, request_arguments_sha256)` is unique 72/72 in **both** files, so the row↔event key is sound.
- `call_id` alone is **not** unique: `toolu_vrtx_01R14vyhySPQ9Y5MXDeAU7Un` appears on 3 rows (OracleReceiptDigest:3, :4, :5) and `call_9b940ef9a2a145d595abc782` etc. are unique elsewhere. The slice keeps the three Digest rows distinct by `site` index and by digest, so no conflation occurred — but see F2.
- Internal invariants over all 72 rows: `canonical_path_count == len(canonical_bad)` (0 violations), `retained_path_count == canonical_path_count` (0 violations), `rough_first_bad == canonical_bad[0]` wherever non-null (0 violations), no row with `rough_category=="path"` and empty `canonical_bad`, no row with `rough_category!="path"` and non-empty `canonical_bad`, all `site` indices unique, all `site` indices within their seat's event count.
- Row distribution: `rough_category` = clean 66, path 3, exec 1, unknown 2; `disposition` = `agree` 72/72. Sums: rough_path 3, canonical_path 3, retained 3.
- No non-ASCII byte appears in any recorded path (checked), so no Unicode-normalization or NFC/NFD path-spelling question arises in this slice.

## Row-by-row result

**Disputed rows: none.** Every one of the 72 rows re-derives to the recorded value under both the S085 rough rule and literal v1 canonical authority, including the component index, both counts, and the disposition. There is no arithmetic or classification row in this slice whose recorded value I can falsify.

The non-clean rows I checked, with the path spelling that drove each (these are the only rows in the slice where a decision was made at all):

1. **OracleReceiptPeriod:9** — `call_00_ZfNOvkvIfZg2LS3wQdB45683` — tool `read`, path `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/OracleReceiptPeriod.md:-6:raw`. S085 strip removes the whole `:-6:raw` tail (alternative `-\d+` then optional `(:raw)`), leaving `…/round-22/build/OracleReceiptPeriod.md`; that file is in this seat's `write_paths` but **not** in `read_paths`, so the read is out of authority → `path`, first bad component 0, rough count 1, canonical bad `[0]`, canonical count 1, retained 1, `agree`. Driving spelling: the seat's own report file, read-scoped.
2. **OracleReceiptPeriod:10** — `call_01_GxhQOpLj7TGmPXH2FQEu9605` — tool `grep`, path `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/OracleReceiptPeriod.md` (no selector). Same file, same outcome: `path`, first bad 0, counts 1/1/1, `agree`. This is the only `grep` in the slice whose single component is not an authorized `read_paths` entry.
3. **OracleReceiptDigest:4** — `toolu_vrtx_01R14vyhySPQ9Y5MXDeAU7Un` — tool `read`, path `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/OracleReceiptDigest.md:raw`. S085 strip removes `:raw`, leaving the seat's own report file, which is in `write_paths` and not in `read_paths` → `path`, first bad 0, counts 1/1/1, `agree`. Driving spelling: same own-output read-scoped pattern as #1.
4. **OracleReceiptDigest:3** — `toolu_vrtx_01R14vyhySPQ9Y5MXDeAU7Un` — tool `edit`, args keys `__unknown_argument__,path`, target `…/round-22/build/OracleReceiptDigest.md`. S085 does not inspect `edit` (not in `('read','grep','glob','write')`) → `unknown`, rough count 0, no first bad. Canonical: target ∈ this seat's `write_paths` → no bad component, count 0, `agree`. Note the request body is **partly unrecorded** (`__unknown_argument__`), see F1/F2.
5. **OracleReceiptCRLF:15** — `call_00_uwi09mqjyp0hg8ztg51ae14s` — tool `edit`, args keys `__unknown_argument__,i,path`, target `…/round-22/build/OracleReceiptCRLF.md`. Same handling: `unknown`, counts 0, canonical `[]`, `agree`.
6. **OracleReceiptCRLF:7** — `call_03_mAEiBaNgj6lNEn9plfOF0806` — tool `bash`, args `{}` (command body not preserved). S085 `bash` branch → `exec`, counts 0, no path inspection; canonical has no path component → `[]`, count 0, `agree`. This seat's binding declares `commands: []`, so no command authority could have been exercised either way; see F1.

All 66 remaining rows are reads/greps/writes of `…/round-22/snapshot/tools/check-review-snapshots.py`, `…/round-22/preregister.json`, `…/round-22/sources/host-tool-boundary.json` or `skill://godspeed` — all four are literal `read_paths` entries of every seat in this pack — or writes to the seat's own `write_paths` entry, with selectors in the 23 distinct forms `:-6:raw`, `:raw`, `:1-105`, `:1-120:raw`, `:1-220`, `:1-60`, `:1-90:raw`, `:106-230`, `:121-180`, `:121-240:raw`, `:121-270:raw`, `:145-205`, `:181-240`, `:200-320:raw`, `:224-278`, `:234-278`, `:241-278:raw`, `:241-360:raw`, `:244-278`, `:250-270:raw`, `:271-278:raw`, `:61-120`, `:90-200:raw`. Every one of those 23 forms strips to its base path under the exact S085 regex, and the two `;`-joined greps (CRLF:9 with 3 components, CohortUnknown:8 with 2 components) have **all** components in `read_paths`, so no component index other than 0 ever appears.

## Falsifier attempted, and why it did not fire

**Falsifier F-A (canonical v1 might treat a seat's own report file as readable, making the 3 path rows `disagree`).** Under that hypothesis the slice would contribute 3 divergent events; the round-23 preregister's reported wave-level gap is only 2 (`rough.build 25` vs `lane.build 23`) and 4 for falsify. A lane classifier permissive about own-output reads would therefore over-count the build divergence by at least 1, so the hypothesis is arithmetically inconsistent with the reported r22 counts. The ledger's canonical verdict (flag all three) is the only one consistent with the wave arithmetic. **Not fired.**

**Falsifier F-B (the S085 strip leaves a residue on `:-6:raw`, so Period:9 is clean).** Refuted directly: with the exact S085 alternation `:(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$`, the tail `:-6:raw` is matched whole by `-\d+` + optional `(:raw)`, leaving `…/build/OracleReceiptPeriod.md` — a `write_paths`-only path, hence a genuine read-authority miss. Independently, the same residue question for `:raw` and `:1-120:raw` was checked across all 39 distinct path spellings in the pack; every one strips to its base path. **Not fired.**

**Falsifier F-C (a mis-joined or reordered row hides behind the duplicated digests).** The 4 duplicated digest values are all explainable as identical argument objects (e.g. `2b4cad9d…` is the read of `skill://godspeed` with `i:null` shared by Period:3, CRLF:0 and CohortUnknown:3; `7cb935bd…` and `a720c78a…` are the same `preregister.json` / `host-tool-boundary.json` reads with `i:null` from different seats). The `(call_id, digest)` pair is unique 72/72 in both artifacts, and the per-seat 20-hex sequences are character-identical. **Not fired.**

**Falsifier F-D (the `bash` or `edit` rows hide a path violation the rough census skipped).** For the two `edit` rows the recorded target is in the seat's own `write_paths`, so no read/write-authority violation exists under either v1 reading. For the `bash` row the recorded args are empty, so no path is available to inspect; the seat's `commands` list is empty, so a command-authority question is unanswerable from preserved evidence, but command authority is outside the path-census metric this slice reports. **Not fired as a path dispute.**

**Falsifier F-E (the slice hides the wave-level 25-vs-23 rough/lane gap).** This slice's rough and canonical path counts are equal (3 = 3) and all 72 dispositions are `agree`, so this slice contributes **zero** to the r22 build-wave divergence of 2. The gap must live in other build slices. This is not a defect of build-06, but it is a real coverage limit: build-06 alone cannot falsify C3's wave-level claim.

## Findings

### F1 (medium) — `disposition: "agree"` is recorded for rows where the rough side produced **no** path verdict at all, conflating "agreement" with "absence of judgment"

Rows: `OracleReceiptDigest:3` (call `toolu_vrtx_01R14vyhySPQ9Y5MXDeAU7Un`), `OracleReceiptCRLF:15` (call `call_00_uwi09mqjyp0hg8ztg51ae14s`), `OracleReceiptCRLF:7` (call `call_03_mAEiBaNgj6lNEn9plfOF0806`).

Evidence: the S085 source cell `continue`s out of the event loop for `bash` and for any tool outside `('read','grep','glob','write')`, so for these three events the rough classifier never inspects a path and never emits a path verdict — the `rough_category` values `exec` and `unknown` are *classifications of the event's tool*, not path verdicts. The canonical side, by contrast, does produce a path verdict for the two `edit` rows (target ∈ `write_paths` → `[]`) and, for the `bash` row, has literally no path to judge (args `{}`; the seat's `commands` list is empty). The slice nevertheless stamps `disposition: "agree"` on all three, so a downstream reader sees 72/72 agreement when in truth 69 rows carry a two-sided path comparison and 3 rows carry agreement-by-absence.

Why it matters for C3: C3 claims "exhaustive per-event/component explanation of rough-versus-lane path counts". A lane-only violation on one of these three events (an opaque edit body that actually touched an unauthorized path, or a bash command that did) is invisible under this encoding: the rough side abstained, and the ledger's `agree` records no divergence. The arithmetic of the reported path counts is unaffected, so this is an honesty/traceability defect in the encoding rather than a wrong count.

Also note for C1/C2: the two `edit` requests carry `__unknown_argument__` — an argument the packer could not name — so under C1's `OPAQUE_PATCH → UNKNOWN` these are exactly the requests whose structured target is not recoverable, and under C2's v2 audit authority they cannot be affirmed as predeclared structured edit targets. The ledger records them as `agree`/`[]` with no marker of opacity, which reads as a positive clearance it cannot support.

Smallest in-scope remedy: give the 3 non-comparable rows a disposition distinct from `agree` (e.g. `not-comparable` / `rough-skipped`) or add a boolean `comparable` field to the row, leaving all path values untouched; no recomputation and no change to the 25/23, 33/29 arithmetic is required.

### F2 (low) — the slice erases event provenance, so two of the 72 rows are not distinguishable from primary-origin events

Rows: `OracleReceiptDigest:4` (call `toolu_vrtx_01R14vyhySPQ9Y5MXDeAU7Un`) and `OracleReceiptDigest:5` (same call id) carry pack fields `origin: "additional-recorded-start"`, `request_line: null`, and **no** `digest_format` field, whereas the other 70 events carry both a `request_line` and the `digest_format` declaration `sorted ensure_ascii JSON arguments; not raw JSONL bytes`. The slice's row schema has no `origin`/`digest_format` field, so the two secondary-origin events — one of which (`OracleReceiptDigest:4`) is one of the 3 path rows — are flattened into the same provenance class as the 70 primary events.

Why it matters for C3: the S085 census iterates the recorded event list of the r22 wave; if the two additional-recorded-start entries were reconstructed beyond the original r22 event list, then this slice's rough contribution (3, of which 1 comes from `OracleReceiptDigest:4`) would not equal the r22 census's own contribution for these seats, and the wave-level `rough.build 25` would shift. I could not test this: the r22 `events.json`/`bindings.json` are outside my declared read scope, and the r23 reconciliation tool source is likewise out of scope. The row values are correct on the evidence I can see; what is missing is the provenance marker that would let an auditor decide the question.

Smallest in-scope remedy: carry `origin` (and `digest_format`) as a per-row field in the slice, or state in the slice's `scope` string that origin is normalized away and that the 72 rows are the pack's 72 events 1:1. A one-sentence scope clarification is the smaller of the two and does not touch row values.

### F3 (low, coverage) — the rough/canonical unit asymmetry is unobservable in this slice, so the falsify lane cannot exercise it here

The S085 rough counter is **event-level** (`f['path'] += 1` then `break`), while `canonical_bad`/`canonical_path_count` are **component-level** (a list of bad component indices and its length). In this slice no event has two or more bad components: the three path rows are all single-component events, and the only multi-component events (CRLF:9, three components; CohortUnknown:8, two components) are entirely clean, so `rough_path_count` and `canonical_path_count` coincide on every row and the `rough_first_bad` vs `canonical_bad[0]` comparison is degenerate. A lane/rough divergence that is purely a unit difference (one event, two bad components) would be structurally invisible in build-06.

Smallest in-scope remedy for the wave: in the reconciliation record, state the unit of each counter explicitly (rough = events, canonical = components) and carry a per-row component count so a unit-only divergence is expressible; nothing needs to change in this slice's rows.

### F4 (observation, not a defect) — the slice's entire path signal is one pattern, and the wave-level gap is elsewhere

All 3 path rows are the seat reading or grepping its **own** report file (`…/round-22/build/<Seat>.md`), which is in `write_paths` and not in `read_paths`; the spelling that drives them is the `:-6:raw` / `:raw` / bare-file form of that own output path. Every other authorized read is of the three r22 shared files or `skill://godspeed`, and every write is to the seat's own `write_paths` entry. Because the two classifiers coincide here (3 = 3, 72/72 `agree`), build-06 contributes nothing to the r22 build divergence of 2 (`rough 25` vs `lane 23`); that difference must be carried by the other build slices. Any falsification of C3's arithmetic has to be made there.

## Residual risk and verification gaps

- The r23 reconciliation tool (`check-path-reconciliation.py`) and the r22 wave `events.json`/`bindings.json` are outside this seat's declared read scope, so I could verify the slice against the *recorded* S085 source cell and the recorded bindings, not against the executing implementation. If the landed tool's actual strip regex, `break` placement, or edit/bash handling differ from the S085 cell as recorded, my agreement for rows 4–6 above would be void; the path rows 1–3 depend only on the S085 cell text and on the literal binding lists, both of which I read directly.
- The r22 reported counts themselves (`rough.build 25`, `lane.build 23`, `rough.falsify 33`, `lane.falsify 29`) are treated as ground truth per the preregister's `outside_round22` scope; I did not recompute them and cannot from this slice.
- Whether the two `additional-recorded-start` events were present in the r22 census's own event list is unresolved (F2); it is the one question in this slice whose answer could change a number rather than a label.
- No `edit` request in this slice has a fully recorded structured target, so the C2 v2-authority behaviour for `edit` is not exercised here and no C2 conclusion is drawn from this slice.
- `skill://godspeed` is a URI listed literally in `read_paths`; it is authorized by literal string match here. Whether a URI in a read path is a filesystem path at all is a C1 `EDIT_EXTERNAL` question that concerns edits, not these reads; no row was disputed on that basis.

## Conclusion

No recorded row value in the build-06 ledger slice is falsifiable. The slice is internally consistent, joins 1:1 to the pack, and reproduces the S085 rough classification and the literal v1 canonical classification for all 72 rows. Three findings are actionable at the ledger-schema level without touching any count: F1 (a distinct disposition for the 3 rows where the rough side abstained), F2 (carry event provenance so the 2 secondary-origin rows are auditable), F3 (state the rough-event vs canonical-component units and carry a component count). F4 records that the wave-level 25-vs-23 gap is not carried by this slice and must be falsified elsewhere.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: 8e285eec3e107094d5fb347b900863116291721d7d6a4c107f091c1ad8318edc
Predicate: r23f-fxc3build06
Scope: executed=none
