# FxC3Falsify06 — r23 falsify wave, ledger slice `falsify-06`

Seat: FxC3Falsify06. Scope: one landed ledger slice, re-derived by hand from the raw pack.
Reviewed artifact: `.ufo/waves/round-23/candidate/ledger-slices/falsify-06.json` (declared SHA256
6d721fd05ee1040d6eb143c39dfeadb387409b23495cf60f6811dbd77c614c9d — supplied identity, not recomputed here).

## 1. Attacked claim

- **Primary: C3** — the path-census ledger must give exhaustive per-event/per-component explanation of the
  rough-versus-lane path counts for both frozen r22 cohorts (`metric: unexplained_cohorts`, target 0).
  Attacked surface: every row of slice `falsify-06` (8 seats, 134 rows) against the raw pack
  `.ufo/waves/round-23/packs/falsify-06.json` (8 bindings, 134 captured events).
- **Secondary: C2 interface** — the four `edit` rows in this slice are the only rows where the rough census
  and the canonical v1 authority produce *different categories* rather than different counts; they are the
  point where a v2 edit-audit authority could leak into a v1 path ledger. Attacked for cross-contamination only.

## 2. Rules used for re-derivation (no execution, hand-applied)

Rough (S085 source cell, `.ufo/waves/round-23/sources/r22-rough-census.txt`, treated as data, never run):

- selector strip regex `:(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$`, applied to `read`/`grep` components only;
- tool set {read, grep, glob, write} is path-bearing; `bash` → `exec`; every other tool → `unknown`;
- membership is literal against `write_paths` for `write`, against `read_paths` otherwise;
- `grep`/`glob` component lists are split on `;`; the loop **breaks at the first undeclared component**,
  so one event contributes at most one rough `path` fault, and `rough_first_bad` is that component's index;
- a fully declared event contributes no counter and is recorded as `clean`.

Canonical (literal v1 authority + the same selector grammar, per the preregister's v1/v2 separation):

- component is bad iff, after the same selector strip, the literal string is absent from the seat's declared
  `read_paths` (read/grep) or `write_paths` (write); `edit` is not a path-audited tool under v1.

Applied bindings: all eight seats share the identical 8-entry `read_paths`
(`…/round-22/candidate/tools/check-review-cohort.py`, `…/round-22/preregister.json`,
`…/round-22/sources/host-tool-boundary.json`, `skill://godspeed`,
`…/round-22/candidate/tools/check-review-snapshots.py`, `…/round-22/candidate/tools/_revision.py`,
`…/round-22/candidate/corpus/knowledge/seat-boundary-r22.json`,
`…/round-22/candidate/corpus/knowledge/seat-boundary-r22.md`) and a single-entry `write_paths`
(their own `…/round-22/falsify/<Seat>.md`). `commands`/`fetches` are empty everywhere, matching S085's
`exec` bucket being unreachable in this slice.

## 3. Coverage

| seat | ledger rows | pack events | rows reproduced | rows disputed |
|---|---|---|---|---|
| FxC3Clean | 24 (`:0`–`:23`) | 24 | 24 | 0 |
| FxC3Faulty | 17 (`:0`–`:16`) | 17 | 17 | 0 |
| FxC3Dead | 18 (`:0`–`:17`) | 18 | 18 | 0 |
| FxC3Unresolved | 10 (`:0`–`:9`) | 10 | 10 | 0 |
| FxC3Partial | 17 (`:0`–`:16`) | 17 | 17 | 0 |
| FxC3FalseDeath | 6 (`:0`–`:5`) | 6 | 6 | 0 |
| FxC3DuplicateSettlement | 23 (`:0`–`:22`) | 23 | 23 | 0 |
| FxC3MissingSettlement | 19 (`:0`–`:18`) | 19 | 19 | 0 |
| **total** | **134** | **134** | **134** | **0** |

Row ↔ event correspondence was checked 1:1 by seat index, by `call_id`, and by
`request_arguments_sha256` (each ledger row's digest equals the digest of the pack event at the same seat
index; identical arguments recur with identical digests across seats, e.g. `skill://godspeed` read =
`2b4cad9d…` in five seats, `host-tool-boundary.json` = `a0250763…`, `seat-boundary-r22.json` = `dc8ca735…`,
`check-review-cohort.py` = `47928ff6…`/`c5cbca26…` per tool). No ledger row lacks a pack event, no pack event
lacks a ledger row, and no tool other than `read`/`grep`/`write`/`edit` occurs anywhere in the pack.

## 4. Rows whose recorded value I dispute

**None.** Every one of the 134 rows re-derives to the recorded `rough_category`, `rough_first_bad`,
`rough_path_count`, `canonical_bad`, `canonical_path_count`, `retained_path_count` and `disposition`.
The falsifier I set out to apply — *a row whose re-derived rough or canonical value differs from the recorded
one* — was not realised by any row in this slice; see §7 for the one condition under which
`FxC3Unresolved:8` would flip.

## 5. Non-agree rows checked (rough category ≠ canonical outcome), and the path spelling that drove them

These four rows are the only rows in the slice where the rough census and the canonical v1 authority do not
produce the same *category* (they still agree on *counts*, hence `disposition: agree`):

| seat | index | call_id | tool | path spelling that drove it | rough | canonical |
|---|---|---|---|---|---|---|
| FxC3Unresolved | 7 | `toolu_017qJKF6VFUbvrJpQFGn3QDQ` | edit | `…/round-22/falsify/FxC3Unresolved.md` with args key `__unknown_argument__` | `unknown` (tool outside S085's path-bearing set → `unknown` bucket, no component evaluated) | no bad component (v1 does not path-audit `edit`; and the target is the seat's declared write target anyway) |
| FxC3DuplicateSettlement | 20 | `call_00_i2tgj6mjk8ymxsasr9gden2p` | edit | `…/round-22/falsify/FxC3DuplicateSettlement.md` + `__unknown_argument__` | `unknown` | no bad component (same reasons) |
| FxC3DuplicateSettlement | 21 | `call_01_outb7rxboltcmxe47huj1pe5` | edit | `…/round-22/falsify/FxC3DuplicateSettlement.md` + `__unknown_argument__` | `unknown` | no bad component |
| FxC3DuplicateSettlement | 22 | `call_00_tbaqsilgpw8669cvv0hvysng` | edit | `…/round-22/falsify/FxC3DuplicateSettlement.md` + `__unknown_argument__` | `unknown` | no bad component |

Because every `edit` target in this slice is the seat's own declared `write_paths` entry, the rows' canonical
values are invariant to whether or not an edit target is audited at all — so this slice cannot be used to
smuggle v2 edit authority into the v1 path ledger, and the C1/C2 edit-decision table
(`DECLARED_EDIT/UNDECLARED_EDIT/READ_ONLY_EDIT/WRITE_ONLY_EDIT/OPAQUE_PATCH/EDIT_TRAVERSAL/EDIT_EXTERNAL/
EXPANSION`) is not contradicted by any row here.

## 6. The three path-fault rows (rough = canonical = `path`, first bad component `0`)

| seat | index | call_id | tool | path spelling | why it is a fault |
|---|---|---|---|---|---|
| FxC3Unresolved | 8 | `toolu_017qJKF6VFUbvrJpQFGn3QDQ` | read | `…/round-22/falsify/FxC3Unresolved.md:raw` | `:raw` strips (branch `raw`); base path is **write-only** (in `write_paths`, absent from `read_paths`) → read outside read authority |
| FxC3DuplicateSettlement | 18 | `call_00_ej5hvuodqjytjevnkczrm8qw` | grep | `…/round-22/falsify/FxC3DuplicateSettlement.md` (no selector) | not in `read_paths` → grep outside read authority |
| FxC3DuplicateSettlement | 19 | `call_01_uvnmw8myucm39uhlne9k06z8` | read | `…/round-22/falsify/FxC3DuplicateSettlement.md:-8` | `:-8` strips (branch `-\d+`); base path write-only → read outside read authority |

Robustness note that matters for the whole-wave reconciliation: **all three fault rows are
grammar-independent** — the unstripped spellings (`:raw`, `:-8`) are equally absent from `read_paths`, so the
fault survives either selector grammar. No row in this slice can therefore be a "the two classifiers disagree
because of selector grammar" row.

## 7. Findings, by severity

**LOW-1 — the canonical column has no category for non-path-audited tools; the four `unknown` rows are
indistinguishable from `clean` rows on the canonical side.**
Rows `FxC3Unresolved:7`, `FxC3DuplicateSettlement:20/21/22` carry `rough_category: "unknown"` but
`canonical_bad: []`, `canonical_path_count: 0`. A consumer that reads the canonical side as "no bad component
⇒ clean" cannot tell "v1 says clean" from "v1 has no opinion because `edit` is not path-audited". The
`rough_category` field carries that distinction; the canonical side does not.
*Smallest in-scope remedy:* add one sibling field to the slice schema (e.g. `canonical_category` with values
`clean|path|not-audited`) for those four rows, or state in the schema prose that `canonical_*` is
path-only and that `rough_category` alone carries the "no canonical opinion" case. No row value changes.

**LOW-2 — `call_id` is not a unique row key in this slice, and recorder-derived rows are not marked in the
ledger.**
`FxC3Unresolved:7`, `:8` and `:9` all carry `call_id = toolu_017qJKF6VFUbvrJpQFGn3QDQ` with three *different*
argument digests (`18e89130…` edit, `b205550e…` read, `6e10925c…` write). The pack marks the latter two
`"origin": "additional-recorded-start"` with `"request_line": null`; the ledger rows do not carry that marker,
so a downstream join keyed on `(seat, call_id)` mis-resolves this seat three-way and a reader cannot tell
which row corresponds to an actual request. The unique key that does work is `site` (`seat:index`).
*Smallest in-scope remedy:* copy the pack's `origin` field onto the three affected rows (or add a
`derived: true/false` flag), and name `site` as the row key in the schema prose. No recorded value changes.

**INFO-1 — this slice contributes exactly 0 to the 33→29 falsify reconciliation, which localises the whole
4-row difference to packs 01–05, 07 and 08.**
Slice totals: rough `path` rows = 3 (all in §6), canonical bad rows = 3, retained = 3, rough `unknown` rows = 4
(§5), `exec` rows = 0. Since every rough `path` row here is also canonical-bad and retained, the ledger cannot
be pointing at this slice to explain `path_counts_as_reported` `rough.falsify = 33` versus `lane.falsify = 29`.
*Concrete falsifier handed to the other slices' seats:* a row with `rough_category: "path"` and
`canonical_bad: []` (or `retained_path_count` < `rough_path_count`), i.e. an event whose undeclared component
is stripped by the rough regex into a **declared** path, or an event the lane does not count at all.

**INFO-2 — one open condition that could flip a row in this slice (not decidable within this seat's bound
paths).**
`FxC3Unresolved:8` (read `…/FxC3Unresolved.md:raw`) is a recorder-derived row: `"origin":
"additional-recorded-start"`, `"request_line": null`, and it duplicates the same tool_use as the `edit` at
`:7`. If the r22 lane's 29-count was produced over *request-bearing* events only (`request_line != null`),
then the correct row values are `canonical_bad: []`, `canonical_path_count: 0`, `retained_path_count: 0`,
`disposition: "disagree"` (rough `path` with no canonical counterpart), and this slice's delta becomes 1
instead of 0. The row's *rough* values are unaffected either way (S085 iterates all events of
`events.json`, derived entries included). Deciding this requires the r22 lane artifact /
`tools/check-seat-bindings.py` at the r22 revision, which is **not** among this seat's declared read paths, so
I report the condition rather than assert it. Note the direction of the risk is symmetric: if instead the lane
did count derived rows, this slice's delta is 0 and the 4-row gap sits entirely in the other packs (INFO-1).

## 8. Bounded search that found no falsifier

- Enumerated all 134 pack events across the 8 seats in the pack and all 134 ledger rows in the slice; the two
  sets correspond 1:1 by seat index, `call_id` and argument digest, with no extras, omissions or duplicates.
- Applied the S085 regex by hand to every `read`/`grep` component: `raw`, `\d[\d\-+,:]*` (covers
  `:31-73`, `:1-140:raw`, `:31-73,85-120,135-160`, `:4-11,28-29,47-128,131-142`, `:24:raw`), `-\d+` (`:-8`) and
  `\d+-` branches; confirmed `skill://godspeed` is **not** stripped (the only `:` is followed by `//`, which
  matches no branch) and still matches a declared `read_paths` entry.
- Confirmed membership of every one of the ~140 distinct path spellings against the seat bindings; the only
  undeclared spellings are the three in §6, all of them the seat's own write-only report file.
- Confirmed no `bash`, `glob` or other tool occurs in the pack, so the `exec`/`unknown` counters cannot affect
  the path arithmetic of this slice.
- Confirmed this slice contains **no** multi-component `grep`/`glob` with an undeclared component, so the
  rough break-rule (≤1 fault/event) versus canonical all-components distinction is not exercised here and is
  not falsifiable from this slice.

## 9. Residual risk and verification gaps

1. **The canonical column was re-derived from binding semantics, not from the r22 lane implementation.**
   `tools/check-seat-bindings.py` at the r22 revision is outside this seat's declared read paths. My canonical
   rule (literal membership of the selector-stripped component in the declared read/write path list) reproduces
   all 134 recorded canonical values, but the lane's original per-row attribution remains unverified by me.
   This is the residual risk behind INFO-2.
2. **Digests were not recomputed** (NO-EXEC; digest is supplied identity). Cross-seat recurrence of identical
   argument digests was used as a consistency check on `request_arguments_sha256` instead — that check is
   self-consistent, not an independent hash verification.
3. **Whole-wave arithmetic not adjudicated here.** `rough.falsify = 33` vs `lane.falsify = 29` cannot be closed
   from one slice; this slice's contribution is 3 = 3 (delta 0), which is itself the falsifier localisation
   reported in INFO-1.
4. **`FxC3FalseDeath`'s fused identifiers** (`call_…|fc_…`) show the recorder merged ids for that seat; all
   six rows are clean under both classifiers, so the fusion has no numeric effect here, but it is another
   reason `call_id` must not be used as a ledger key (see LOW-2).

## 10. Smallest in-scope remedy (summary)

No recorded value in slice `falsify-06` needs correction. Two additive, non-behavioural ledger-schema changes
(LOW-1, LOW-2) and one cross-slice falsifier to be discharged by the other packs' seats (INFO-1, INFO-2) are the
whole remedy set. Nothing outside `.ufo/waves/round-23/` was touched; no production file, index, ref, route or
service was modified; no round-24 work was started.

## 11. Tooling

No installation or update was performed. This seat's binding is `commands: []`, `fetches: []` (NO-EXEC /
NO-FETCH) and the seat's narrower scope forbids installs, so the operator tooling directive was not exercised;
no package manager, service or host action was invoked.

Reviewed-SHA256: 6d721fd05ee1040d6eb143c39dfeadb387409b23495cf60f6811dbd77c614c9d
Predicate: r23f-fxc3falsify06
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
