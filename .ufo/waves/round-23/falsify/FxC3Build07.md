# FxC3Build07 — C3 path-census ledger, build pack 7

Seat: FxC3Build07. Slice: `.ufo/waves/round-23/candidate/ledger-slices/build-07.json`
(8 seats, 74 rows). Pack: `.ufo/waves/round-23/packs/build-07.json`. Rough rule source:
`.ufo/waves/round-23/sources/r22-rough-census.txt`. Receipt digest is the supplied declaration
only; it was not computed, hashed, listed, imported, or executed.

## Attacked claim

C3 — `unexplained_cohorts` 2 → 0: that both fixed r22 cohorts have exhaustive per-event
component explanation of rough-versus-lane path counts. This slice is the build-wave group-7
part of that reconciliation ledger. If any row's recorded rough category, first bad component,
canonical bad components, or disposition is wrong, the reconciliation is not exhaustive for
group 7 and C3's target is unsupported by this slice.

## Method (hand re-derivation, no execution)

Rough (literal S085 script semantics in `r22-rough-census.txt`):

- `bash` → `exec`, no path component.
- Tool outside `{read, grep, glob, write}` → `unknown`, no path component.
- `read`/`grep`: `str(args.path).split(';')`, each value through
  `re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`; first value whose stripped form is
  not in `binding.read_paths` increments `path` once and breaks the value loop (per event).
- `write`: raw `args.path`, compared literally against `binding.write_paths` (no selector strip).
- `glob` (unused here): split on `;`, no strip, checked against read_paths.

Canonical (literal v1 authority as materialized in the pack bindings): only `read_paths` and
`write_paths` exist, `commands`/`fetches` empty; the v1 tool grammar is the same four tools.
A bad component is the index of the offending `;`-component in the retained path list; a tool
outside the grammar is canonical `unknown` with no components; an exec is canonical `exec` with
no components. Disposition is `agree` iff the derived (category, first bad component) equals the
recorded (rough category, canonical bad set).

## Per-row re-derivation (all 74 rows)

Encoding: `site:derived` — `c` clean, `p@0` path with bad component 0, `x` exec, `u` unknown.
Recorded values were read from the slice; derived values below are mine.

- OracleCohortPartial: 0: c, 1: c, 2: c, 3: c, 4: c, 5: c, 6: c, 7: c, 8: c, 9: c, 10: c, 11: c.
  Path spellings: `skill://godspeed`; `.../round-22/snapshot/tools/check-review-snapshots.py`
  bare and with `:1-140`, `:140-280`, `:56-81:raw`, `:119-143:raw`, `:244-278:raw`;
  `.../round-22/preregister.json`; `.../round-22/sources/host-tool-boundary.json`; write
  `.../round-22/build/OracleCohortPartial.md`. Every stripped read form is a declared read
  path; the write is the declared write path.
- OracleCohortBiject: 0: c, 1: c, 2: c, 3: c, 4: c, 5: c, 6: c, 7: c, 8: c. Same four declared
  inputs, selectors `:1-140`, `:140-300`, `:100-128`, `:246-278`; write
  `.../build/OracleCohortBiject.md` declared.
- OracleCohortDuplicate: 0: c, 1: c, 2: c, 3: u, 4: p@0, 5: c. Details in next section.
- OracleCohortFalseDeath: 0: c, 1: c, 2: c, 3: c, 4: c, 5: c, 6: c, 7: c. Selectors
  `:21-129`, `:145-241`, `:131-142,244-274` (the comma form is consumed by `\d[\d\-+,:]*`);
  write `.../build/OracleCohortFalseDeath.md` declared.
- OracleCohortStrictRed: 0: c, 1: c, 2: c, 3: c, 4: c, 5: c, 6: c, 7: c, 8: c, 9: c, 10: c.
  Selectors `:1-120:raw`, `:121-240:raw`, `:241-360:raw`, `:45-130`, `:141-185`; grep path is
  the declared snapshot tool; write `.../build/OracleCohortStrictRed.md` declared.
- OracleCohortDigest: 0: c, 1: c, 2: c, 3: c, 4: c, 5: c. Selectors `:1-200`, `:1-220`,
  `:1-200`, `:204-278`; write `.../build/OracleCohortDigest.md` declared.
- DebtBash: 0: c, 1: c, 2: c, 3: c, 4: c, 5: c, 6: p@0. Details in next section.
- DebtFetch: 0: c, 1: c, 2: c, 3: c, 4: c, 5: x, 6: c, 7: c, 8: c, 9: c, 10: c, 11: c, 12: c,
  13: c, 14: c. Reads/greps all target
  `.../snapshot/corpus/lessons/round-21.md` (declared) with selectors `:136-146:raw`,
  `:25,41,43:raw`, `:56-68:raw`, `:94,98,112,114:raw`; bash event has empty args; write
  `.../build/DebtFetch.md` declared.

Every row's recorded `tool`, `call_id`, `request_arguments_sha256`, `rough_category`,
`rough_first_bad`, `rough_path_count`, `canonical_bad`, `canonical_path_count`,
`retained_path_count` and `disposition` reproduced exactly from the pack events and bindings.
There is no row where the derived value differs from the recorded value.

## The four non-agree (non-clean) rows, checked in full

1. `OracleCohortDuplicate:3` — call_id `toolu_015tSz2JMMi9eYMAmfqdWnaf`, tool `edit`,
   args `{path: ".../round-22/build/OracleCohortDuplicate.md", "__unknown_argument__": null}`.
   Derived: `unknown` (edit is outside the four-tool v1 grammar; the path is present but is not
   a read/write component under v1). Recorded: `unknown`, `rough_first_bad: null`,
   `canonical_bad: []`, retained 0, agree. Reproduced.
2. `OracleCohortDuplicate:4` — same call_id, tool `read`, path spelling
   `.../round-22/build/OracleCohortDuplicate.md:raw`. Strip `:raw` → the declared *write* path,
   absent from `read_paths` → `path` at component 0, break. Recorded: `path`, first bad 0,
   `canonical_bad: [0]`, canonical count 1, retained 1, agree. Reproduced; the driving spelling
   is the `:raw` selector over a write-only file.
3. `DebtBash:6` — call_id `call_00_2hSTsiM0i5bcqrJM6Nby0686`, tool `read`, path spelling
   `.../round-22/build/DebtBash.md:-6:raw`. The regex third alternative `-\d+` plus optional
   `:raw` strips `:-6:raw` → the declared *write* path, absent from `read_paths` → `path` at
   component 0. Recorded: `path`, first bad 0, `canonical_bad: [0]`, counts 1/1, agree.
   Reproduced; the driving spelling is the negative-line selector over a write-only file.
4. `DebtFetch:5` — call_id `call_01_9Ya6CQp0DQzKikwG1uKD3940`, tool `bash`, empty args.
   Derived and recorded: `exec`, no first-bad component, no canonical component, agree.
   Reproduced; bindings declare `commands: []`, so the exec is unauthorized but its rough and
   canonical units are both the event itself, not a path component.

## Edge cases specifically attacked

- Shared `call_id` across three events: `OracleCohortDuplicate` events 3/4/5 all carry
  `toolu_015tSz2JMMi9eYMAmfqdWnaf`; events 4 and 5 are `additional-recorded-start` entries with
  no `request_line`. The slice keeps three distinct rows (`:3` unknown, `:4` path, `:5` clean),
  so the census unit is the recorded event, not the call — consistent with the S085 loop over
  `x['events']`. No double count is hidden; the duplication is disclosed row by row.
- Write-vs-read-only membership inversions: rows `OracleCohortDuplicate:4` and `DebtBash:6`
  read from `write_paths` only; both are flagged `path`, matching the rule that a `read` is
  checked against `read_paths` alone (no implicit read from write ownership).
- Selector forms: `:N-M`, `:N-M:raw`, comma lists `:a,b,c`, negative `:-6`, and bare `:raw`
  all strip under the exact regex; none of the stripped forms fell outside a declared list.
- Writes carry no selector; each write path equals a declared `write_paths` entry literally
  (trailing `.md`, no `:raw`), so no literal write mismatch exists in this slice.
- Seeds/null args: grep events carry `pattern: null` and writes `content: null`; body opacity
  does not affect the path census, and no read/grep/write event in this pack lacks a path arg.
- Seat coverage: pack seat order (Partial, Biject, Duplicate, FalseDeath, StrictRed, Digest,
  DebtBash, DebtFetch) matches the row order; the slice's `seats` array is only alphabetically
  sorted (DebtBash, DebtFetch, …). Cosmetic, no row consequence.

## Result

No disputed row. Seat/index/call_id/reason list: empty. Falsifier attempted: a row where the
literal S085 regex/break rule, the literal write-list comparison, the four-tool v1 grammar, or
the exec branch yields a different (category, bad component) or disposition than recorded; the
74-row hand re-derivation above found none, and the bounded search is exactly the slice's own
row set (no other group-7 events exist in the pack, and no pack event is unrepresented:
12+9+6+8+11+6+7+15 = 74). This slice therefore supports C3 for build group 7; it does not by
itself prove the aggregate build rough count of 25 (other packs' slices are outside this seat's
read set) and it does not claim runtime enforcement of any kind.

Smallest in-scope remedy: none required for this slice. If the round wants belt-and-braces
disclosure, the only minimal addition is one line in the reconciliation record noting that
group 7's non-clean contributions are exactly two `path` events (`OracleCohortDuplicate:4`,
`DebtBash:6`), one `exec` (`DebtFetch:5`), and one `unknown` (`OracleCohortDuplicate:3`), with
the latter sharing its `call_id` with the two adjacent `additional-recorded-start` rows — no
code, tool, ledger, or binding change.

## Epistemic status

- Observed: the slice rows, pack bindings/events, the S085 snippet, and the preregister claim
  text, all read directly from the declared paths.
- [INFERENCE] The canonical ledger and checker source were not in this seat's read set; the
  canonical `unknown` classification of `edit` is inferred from the four-tool grammar and the
  absence of `edit_paths` in every group-7 binding, not from the checker's internals. If the
  landed checker classifies `edit` differently, only row `OracleCohortDuplicate:3` could flip,
  and its recorded `canonical_bad: []` would need review.
- Unresolved: aggregate-level arithmetic (preregister build rough = 25) cannot be confirmed
  from this slice alone; slice SHA-256 is a supplied declaration and was not computed.

Reviewed-SHA256: f356d6ae91cc47899eff8802f0faec4a9f0023c610ebeb9894ff95d59c146507
Predicate: r23f-fxc3build07
Scope: executed=none
