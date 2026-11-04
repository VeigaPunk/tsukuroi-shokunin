# ReviewDeps — per-row reasoning (C1 companion review)

Bound at 2026-11-04 16:16 -0300:
`data.json` sha256 `85ac6da934c482890f0f0a7e46359bc163c4382eb6f2014cabfa3d3885bb80df`,
`note.md` sha256 `c1149b5faf62754afaac1e2303dc86c8ee2f558d90146757249d48ecda53382a`.
The landing copies must be byte-identical; a later edit voids this verdict.
Quote location was re-derived independently with the counter's rule (strip inline tags per
line, tokenise, join with one space); every quote occurs exactly once in that token stream and
computes to its recorded range.

## DP1 — holds

Read: snapshot 665–668, tag-stripped:
"Units listed in this option will be started if the configuring unit is. However, if the listed
units fail to start or cannot be added to the transaction, this has no impact on the validity of
the transaction as a whole, and this unit will still be started."
Quote (666-667) is the second sentence's consequent; the statement supplies the condition from
665–666. "leaves the transaction valid" = "no impact on the validity of the transaction as a
whole"; "the configuring unit still starts" = "this unit will still be started". Plural source
("the listed units") read distributively as "a listed unit" — no strengthening.

## DP2 — holds

Read: 688–692:
"If this unit gets activated, the units listed will be activated as well. If one of the other
units fails to activate, and an ordering dependency After= on the failing unit is set, this unit
will not be started. Besides, with or without specifying After=, this unit will be stopped (or
restarted) if one of the other units is explicitly stopped (or restarted)."
The quote is the complete second sentence; the statement keeps both branches ("with or without
After=", "stopped or restarted"). The preceding sentence's failure-to-activate rule is a
different proposition, not claimed by DP2.

## DP3 — holds

Read: 713–717:
"Similar to Requires=. However, if the units listed here are not started already, they will not
be started and the starting of this unit will fail immediately. Requisite= does not imply an
ordering dependency, even if both units are started in the same transaction."
The statement keeps both halves of the quoted sentence. The ordering caveat is outside the quote
and is not claimed (the note carries it in (d)).

## DP4 — holds

Read: 733–737:
"Configures requirement dependencies, very similar in style to Requires=. However, this
dependency type is stronger: in addition to the effects of Requires=, which already stops (or
restarts) the configuring unit when a listed unit is explicitly stopped (or restarted), it also
does so when a listed unit stops unexpectedly (which includes when it fails)."
The quote is the second clause; the statement supplies "Beyond Requires=" from the same sentence
and reads "does so" as "stops (or restarts)". "Stops" alone is a narrowing (the restart branch is
carried by the Requires= reference), not an overclaim.

## DP5 — holds

Read: 763–767:
"Configures dependencies similar to Requires=, but limited to stopping and restarting of units.
When systemd stops or restarts the units listed here, the action is propagated to this unit. Note
that this is a one-way dependency — changes to this unit do not affect the listed units."
The quote is the complete sentence; the one-way clause is the next sentence and the statement
claims no bidirectionality.

## DP6 — partly-holds

Read: 783–786:
"Configures dependencies similar to Wants=, but as long as this unit is up, all units listed in
Upholds= are started whenever found to be inactive or failed, and no job is queued for them. While
a Wants= dependency on another unit has a one-time effect ..."
The row's quote stops at the comma after "failed," mid-sentence; the sentence continues on the
same line 785 with "and no job is queued for them." That clause is a precondition of the start:
the uphold check acts only when no job is already queued for the unit. The statement —
"While the configuring unit is up, listed units found inactive or failed are started." — drops it
and therefore asserts a broader trigger than the source. Corrected sentence:
"While the configuring unit is up, listed units found inactive or failed are started when no job
is queued for them."

The companion already records this drop (`note.md:110-112`, `:230-231`) and calls the eight
statements "Partly met" (`note.md:219-224`). The row is still the counted object, so the verdict
stays partly-holds; the companion's prose disclosure does not widen the row.

## DP7 — holds

Read: 936–939:
"Takes a space-separated list of absolute paths. Automatically adds dependencies of type Requires=
and After= for all mount units required to access the specified path."
Both added dependency types are kept. "the specified paths" (plural) follows the directive's own
argument domain ("space-separated list of absolute paths", 936–937); it is not a stronger claim
than the singular quote cell. The `noauto` paragraph (941–944) is separate and is not claimed.

## DP8 — holds

Read: 855–859:
"Note that those settings are independent of and orthogonal to the requirement dependencies as
configured by Requires=, Wants=, Requisite=, or BindsTo=. It is a common pattern to include a
unit name in both the After= and Wants= options, in which case the unit listed will be started
before the unit that is configured with these options."
The quote ends mid-sentence, but the statement claims only that the manual names the combination
as a common pattern; the consequence (start order) is not claimed. Accurate.

## Consequence for the frozen counter

`tools/measure-unit-deps-r79.py` (lines 92–132; `finite-content-mismatch` at :98, `review-not-bound` at :121) requires the data to equal `before/expected.json`'s
rows exactly (`finite-content-mismatch` otherwise) and requires the review map to be all `holds`
(`review-not-bound` otherwise). DP6 partly-holds therefore means:

- frozen data + this review → `review-not-bound`, rows 0, rc 1;
- widened DP6 + this review → `finite-content-mismatch`, rows 0, rc 1;
- changed expected.json/counter → a different instrument, outside this seat and the frozen claim.

C1 is a declared miss this round unless an operator-authorized new instrument is declared. That is
the honest close; a `holds` I cannot defend would be the fabricated green the declaration's kill
rule exists to catch.

## Companion defects

F1 (medium) `note.md:151`: names the `:952` hit "the `RequisiteMountsFor=` entry". No
`RequisiteMountsFor` string exists in the snapshot (grep count 0); the entry at 950–954 is
`WantsMountsFor=`, and the note's own bullet at `note.md:171-172` says so. Internal contradiction.

F2 (medium) `note.md:74-75`: "`Before=`/`After=` do not pull anything in and do not affect start
order by themselves". The cited quotes say requirement dependencies do not influence order and
ordering must be configured with After=/Before=; the ordering directives are exactly what affects
start order. The sentence should read: requirement dependencies neither pull in nor order; ordering
is configured with `Before=`/`After=`.

F3 (low-medium) `note.md:158-160`: "`corpus/SOURCES.md` ends at `S328`". True when measured (328
rows; S329 absent at 16:16), but C1 requires S329 to resolve in SOURCES.md at the landing revision,
so the landed entry would carry a false current statement. Rephrase or update before landing.

F4 (low) `note.md:93-95`: "The manual does not say the opposite either" is a whole-manual negative
without the bounded sweep/scope/date QUALITY 9 requires; the note's QUALITY 9 bullet does not cover
it. Scope it to the passage or add the sweep.

F5 (low) `note.md:110-112`: "so the keep-alive is not an observable queued job" misreads "and no
job is queued for them". The clause is a precondition (start only when no job is already queued for
the unit), not a statement that no job results.

F6 (low) `note.md:223-235`: QUALITY 66 says four rows are narrower "than the sentence they quote".
DP2, DP5 and DP7 match their quoted sentences; the clauses the note names are in the preceding
sentence (DP2, `:688-690`), the preceding/next sentences (DP5, `:763-764`, `:766-768`) and the
preceding/next paragraphs (DP7, `:936-937`, `:941-944`). Only DP6's quote is a mid-sentence
fragment whose continuation holds the dropped clause; DP8's continuation loses nothing the
statement claims. Over-disclosure is not an overclaim, but the audit's "four of eight" is wrong;
the material row-level gap is DP6 alone.

F7 (nit) `note.md:237`: cites DP1 at ":665-667" while the row cell is 666-667.

## Accuracies confirmed

- Boundary legs are honest: upstream v262 tag lines, explicitly not installed-build lines
  (QUALITY 103); no live daemon state; no live-host measurement; quotes defined as tag-stripped
  token spans; the note does not claim the round passes.
- Spot-checked citations resolve as described: `:802-804` Conflicts=, `:791-793` UpheldBy=,
  `:2266-2270` Upholds=/UpheldBy= table row, `:2328-2331` "cannot be used directly as a unit
  configuration setting", `:941-944` `noauto`, `:2245-2300` contains no RequiresMountsFor= row.
- Selection is disclosed as the round's frozen choice (six requirement-family values plus two
  helpers) with the non-exhaustiveness named; no claim over directives outside the eight.

## Limits

No gate or selftest executed; counter behaviour read from source, not observed. S329 is absent from
`corpus/SOURCES.md` at review time (registry leg unverified — another seat's file). Landing copies
under `corpus/knowledge/` do not exist yet. No LSP server mounted (no code under review). No
installed-build or live-state claim made or checked.

## Execution record

Read-only: `sha256sum`; `python3` heredocs (JSON/regex reads); `grep`; `awk`/`sed` line windows.
No gate, no selftest, no mutation, no git/jj, no tool install, no scratch tree. Writes: this file,
`verdict.json` and the report only.
