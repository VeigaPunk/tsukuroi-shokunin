# FxC3Falsify03 — C3 path-census ledger, slice falsify-03

Seat: `TsukuroiR23-2.FxC3Falsify03-2` (leaf; no children, no background jobs, no commands, no fetches).
Slice: `.ufo/waves/round-23/candidate/ledger-slices/falsify-03.json`, landed `5a25c88b77f52e940bcad87825c4ac1cd529470d`, declared SHA256 `3db853d86d4471ca134d217958678ef9283834287e8ab90adf7918227ff9bf54` (supplied identity — not computed, not re-derived).
Pack: `.ufo/waves/round-23/packs/falsify-03.json` (r22 falsify group 3: 8 seats, 115 events).
Authority: each seat's own `binding.read_paths` / `binding.write_paths` in the pack; the exact S085 census code in `.ufo/waves/round-23/sources/r22-rough-census.txt`.

## Axes iterated

1. **A1 exactness** — every recorded field re-derived per row from pack args + binding, under the literal S085 predicate.
2. **A2 coverage** — row set ↔ pack event set identity (count, per-seat index contiguity, tool, call_id, request digest).
3. **A3 rule sensitivity** — which rows' values depend on an unstated rule choice (edit vocabulary, redaction).
4. **A4 disposition** — whether `agree` is defensible for each non-clean row and what it actually asserts.

Each move was read-only; no production file, no sibling file, no git/jj state touched.

## Re-derivation rule (verbatim, from S085)

```
def strip_sel(p):
  return re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)
...
if t=='bash': f['exec']+=1; seats.add(...); continue
if t not in ('read','grep','glob','write'): f['unknown']+=1; seats.add(...); continue
vals=str(a.get('path','')).split(';') if t in('grep','glob') else [str(a.get('path',''))]
for v in vals:
  q=strip_sel(v) if t in('read','grep') else v
  if q not in (b['write_paths'] if t=='write' else b['read_paths']):
    f['path']+=1; seats.add(x['name']); break
```

Derived predicate used for every row: category `path` iff at least one component of `args.path` (split on `;` for grep/glob, selector stripped for read/grep) is absent from the seat's write list (write) or read list (all other four-tool events); `first_bad` = index of that component in the split list; `rough_path_count` ∈ {0,1} because of the `break`; `unknown` iff tool ∉ {read, grep, glob, write}; canonical = same authority with no `break`, over the v1 four-tool vocabulary, recording component indices.

Selector grammar is load-bearing: 42 of 115 events carry a selector that `strip_sel` must remove (`:1-80:raw`, `:1-40,60-70`, `:-12`, `:raw`, …). All 42 strip cleanly; 40 land on a declared read path and 2 land on a write-only report path (the `FxC2XD:19` and `FxC2Skill:8` rows below).

## Result — 0 disputed rows

All 115 rows are `disposition: agree`; no row disagrees with its own re-derivation. The non-clean rows checked, with the path spelling that drove each:

| seat:index | call_id | recorded spelling | derivation | recorded | verdict |
|---|---|---|---|---|---|
| FxC2XD:19 | call_00_00xyaozzfaapomroplo1yy6q | `…/.ufo/waves/round-22/falsify/FxC2XD.md:-12` | `:-\d+` strips → `…/round-22/falsify/FxC2XD.md`, in **write_paths only**, absent from read_paths | path@0 / 1 / canonical `[0]` / 1 | correct |
| FxC2Skill:6 | toolu_01Y8GnbHxk2TnQJuzQ1pdMV7 (origin `additional-recorded-start`) | `redacted-internal-uri` | no selector match; literal string absent from read_paths | path@0 / 1 / canonical `[0]` / 1 | correct as recorded (spelling is a redaction — see R2) |
| FxC2Skill:8 | toolu_01HSUsLHKD2NbFYwef6kMs7U (origin `additional-recorded-start`) | `…/.ufo/waves/round-22/falsify/FxC2Skill.md:raw` | `:raw` alternative strips → report path, **write_paths only** | path@0 / 1 / canonical `[0]` / 1 | correct |
| FxC2Prefix:16 | call_00_84bnqrqrgm15l7r7fjqtb7te | `…/.ufo/waves/round-22/falsify/FxC2Prefix.md` | grep, single component, no selector; absent from read_paths | path@0 / 1 / canonical `[0]` / 1 | correct |
| FxC2Search:18 | toolu_01U5kGBAhSFfj3bRb73tEFM8 | *(none)* — args `{i:null, __unknown_argument__:null}` | tool `edit` ∉ v1 vocabulary → `unknown` | unknown / 0 / canonical `[]` / 0 | correct under literal v1 |
| FxC2Skill:7 | toolu_01HSUsLHKD2NbFYwef6kMs7U | args `{path: …/round-22/falsify/FxC2Skill.md, __unknown_argument__:null}` | tool `edit` ∉ v1 vocabulary → `unknown`; path is **write_paths only** (`inread=false`) | unknown / 0 / canonical `[]` / 0 | correct under literal v1 — sole rule-sensitive row (R1) |

Multi-component events were checked component-by-component and are all clean: `FxC2Relative:13` (3 grep components), `FxC2Semicolon:14` (3), `FxC2Semicolon:15` (7 glob components). No multi-component event contains a bad component, so `first_bad=0` is the only non-null value the slice can legitimately contain — and it is.

## Mechanical identity checks (read-side projections only; no execution)

- Row set ↔ pack events: 115 = 115; per-seat index ranges contiguous and complete (Search 0–18, XD 0–19, Selector 0–9, Skill 0–9, Relative 0–14, Traversal 0–6, Prefix 0–16, Semicolon 0–16); no duplicate `site`.
- Tuple identity over (site / pack `name:index` | tool | call_id | request_arguments_sha256), sorted: both sides give `n=115`, joined length `13847`, folds `h1=7423180242`, `h2=68293480287632`. No row is bound to the wrong event, tool, call id or digest.
- Aggregate re-derivation from the pack under the S085 predicate: `{clean:109, path:4, unknown:2}` with bad set `{FxC2XD:19@0, FxC2Skill:6@0, FxC2Skill:8@0, FxC2Prefix:16@0}` and unknown set `{FxC2Search:18, FxC2Skill:7}` — identical to the slice's recorded fields.
- Canonical re-derivation (no break, component indices): `Σ canonical_path_count = 4`; `canonical_bad` length equals `canonical_path_count` on all 115 rows; `Σ retained_path_count = 4`; zero `clean` rows carry a non-zero canonical or retained count.

## Attacked claim, falsifier, bounded search

**Attacked claim: C3** — `unexplained_cohorts` 2 → 0, i.e. "both fixed r22 cohorts have exhaustive per-event/component explanation of rough-versus-lane path counts, frozen digests and declared arithmetic", as borne by this pack's slice. C1 and C2 were probed only where this slice can bear on them (the two `edit` events); the eight-decision table and the v2 authority are prose/checker artifacts not present in the pack, so this slice can neither confirm nor refute C1 or C2, and nothing here supports a runtime-enforcement claim.

**Concrete falsifier attempted:** a row whose `rough_category`, `rough_first_bad`, `rough_path_count`, `canonical_bad`, `canonical_path_count`, `retained_path_count`, or `disposition` fails re-derivation from pack args + binding under the exact S085 regex/`break` rule and literal v1 tool vocabulary. Also attempted: a binding mismatch (wrong call_id/digest/site), an index gap, a duplicate site, a clean row hiding a bad component, and a multi-component event whose `first_bad` is wrong.

**Bounded search, no counterexample:** all 115 rows, both non-four-tool rows, all 42 selector-bearing rows, all 9 multi-component grep/glob events, and the full tuple/digest binding. The four `path` rows are genuine out-of-authority accesses (three reads/greps of the seat's own report, which holds write authority only, plus one undeclared internal-URI read); the two `edit` rows are correctly outside v1's four-tool vocabulary.

**Smallest in-scope remedy:** none required for any recorded row value — the slice is arithmetically exact for this pack. If the ledger is to be self-explaining at row level, the minimal addition is one field (`canonical_category`, or a one-line `note`) on the two `edit` rows distinguishing "outside v1 vocabulary" from "clean"; no new production behavior, no reclassification of any existing field.

## Residual unknowns (stated, not resolved)

- **R1 — edit rows collapse two situations into `canonical_path_count: 0`.** `FxC2Skill:7` has a recorded structured target that is write-only (`READ_ONLY_EDIT`/`WRITE_ONLY_EDIT` shape, DENY under C1's own table); `FxC2Search:18` has no target at all (`OPAQUE_PATCH`, UNKNOWN). Under a canonical rule that adjudicates `edit` as read+write, `FxC2Skill:7` flips from 0 to 1 bad component and this slice's `Σ canonical = 4` becomes 5. The recorded 0 is correct only under the stated "literal v1 authority" definition (four-tool vocabulary); the slice does not carry the vocabulary, so the reading is imported from S085, not proved by the slice.
- **R2 — one spelling is redacted.** `redacted-internal-uri` is not the actual target text. Classifying it as an undeclared read is robust because the *declared* `skill://godspeed` start of the same call_id was left in clear while its sibling start was redacted; the alternative (redaction also masks declared paths) would make the count 0 instead of 1. This is the only evidence-gapped value in the slice.
- **R3 — the 33 → 29 arithmetic is not in this file.** The slice exposes rough and canonical per row but no lane column, no cohort header and no ledger-level totals; `Σ rough_path_count = 4` here is one pack's contribution, not the falsify aggregate. C3's "declared arithmetic" half is therefore unverifiable from this slice alone (and the ledger aggregate is outside this seat's declared read paths). No improvised read was attempted.
- **R4 — `disposition` semantics are inferred.** All 115 rows are `agree`; the only reading under which that is consistent with the recorded columns is rough-count = canonical-count (+ zero unknown-row paths), because for the two `edit` rows the *categories* differ (`unknown` vs no canonical category). If `disposition` instead compares rough against the r22 lane, the four `path` rows are unverifiable here for lack of the lane column.

Tooling: no installs or updates performed; pacman transactions remain paused host-wide; this seat's NO-EXEC/NO-FETCH scope forbids them. No commands, no fetches, no delegation — the only actions were `read`/`grep` on the declared files and one `write` of this report.

Reviewed-SHA256: 3db853d86d4471ca134d217958678ef9283834287e8ab90adf7918227ff9bf54
Predicate: r23f-fxc3falsify03
Scope: executed=none
