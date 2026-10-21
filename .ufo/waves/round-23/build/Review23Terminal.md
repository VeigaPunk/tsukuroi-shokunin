# Review23Terminal — scoped review of the round-23 structured-edit observation source

## 0. Scope, authority, and what this review did not do

Reviewed source (declared identity, not independently computed):
`.ufo/waves/round-23/sources/structured-edit-observations.json`
declared SHA256 `19d85129bf0f7fd71f5aea93c35660b21d305150500dc63b58104019851af12a`.

Also in scope for this seat: `.ufo/waves/round-23/preregister.json`,
`.ufo/waves/round-23/snapshot/tools/check-review-cohort.py`,
`.ufo/waves/round-23/sources/godspeed-directive.txt`, `skill://godspeed`.

This seat executed nothing: no command, no fetch, no delegation, no hashing, no listing,
no import of the observed transcripts, no opening of raw unbound session paths. Every
statement below is derived from the bytes of the four declared files above. All cited
line numbers refer to those files as read.

Two authorities are distinguished throughout and never merged:

- **Job receipt** — the three-field per-seat receipt. It is a *declaration* by the seat.
  It is machine-checkable for shape only.
- **Provider trace** — request keys, recorded adapter steps, transcript digests. It is a
  *second-hand record* of tool-shaped activity, and the source itself disclaims effects,
  native permission enforcement, universal tool semantics, and reading proof
  (`structured-edit-observations.json:101`).

Completion of a seat (a receipt present and well formed) is therefore **not** evidence of
record completeness, effect completeness, or reading. The cohort accounting tool makes the
same distinction explicit for the review cohort
(`check-review-cohort.py:20`, `:99`).

## 1. Axes named (godspeed)

1. **Authority separation** — receipt vs. trace vs. effect; which claim each artifact may carry.
2. **Shape coverage** — which observed argument-key shapes the r23 decision taxonomy can actually classify.
3. **Target identity** — whether recorded paths are comparable as edit targets (selectors, spellings).
4. **Precedence** — whether recorded line fields can establish read-before-write-before-edit.
5. **Calibration honesty** — saturation/exhaustiveness claims vs. declared denominators.
6. **Accounting semantics** — what a cohort tool's green result does and does not certify.

Findings below are grouped by severity. Each finding cites evidence and ends with a bounded,
source-only recommendation (no execution implied).

## 2. Findings

### HIGH-1 — A green cohort result can coexist with faulty receipts; `status` does not reflect receipt conformance

`check-review-cohort.py:76` buckets **any** seat whose strict exit is non-zero as
`delivered_faulty`, but adds **no finding** for it. `:89` computes
`code = 2 if strict_code == 2 or unclassified else (1 if findings else 0)`, and `:100` maps
that code straight onto `result['status'] = ('PASS','FAIL','CANNOT_EVALUATE')[code]`.
A seat with a malformed receipt therefore raises neither `findings` nor `unclassified`, so
the cohort as a whole evaluates to `status: PASS`.

The selftest locks this behaviour in rather than treating it as incidental:

- `:123` — `partial-failed`: expected exit `0`, category `delivered_faulty`, `strict_exit=1`.
- `:126` — the receipt-fault family (trailing period on the scope field, wrong predicate,
  wrong digest): expected exit `0`, category `delivered_faulty`, `strict_exit=1`.

The module discloses this in prose: `:20` states that `delivered_conformant` means
"receipt-well-formed, not request-scope conformity, command nonexecution, reading,
chronology, no-harm or native enforcement", and `:99` publishes a separate
`strict_conformance` verdict (`PASS` / `FAIL` / `CANNOT_EVALUATE`). The disclosure is
honest, but the primary `status` key does not carry it.

**Impact.** Any round-23 artifact that cites the cohort tool's `status` as evidence that
receipts conformed would overstate the run: a fully green `status` is compatible with
`delivered_faulty > 0` and with `strict_conformance == 'FAIL'`.

**Recommendation.** Round-23 must cite `strict_conformance` (and `strict_receipt_exit`, plus
the per-seat `strict_exit` field at `:83`) when it makes any receipt-conformance statement,
and must never cite `status` alone. If a landed artifact needs a single green receipt
statement, derive it from `strict_conformance == 'PASS'`, not from `status == 'PASS'`.

### HIGH-2 — The observation source contains no negative example, so it grounds no DENY row of the r23 taxonomy

Every one of the four observations is an `edit` call whose target is the seat's own
round-22 report path (`:16`, `:50`, `:73`, `:96` for the respective recorded steps;
observation `path` fields at `:16`, `:43`, `:66`, `:89`). No observation has a target
outside the seat's own report, no undeclared target, no read-only-seat case, no dot-segment
or alternate spelling, no remote/internal URI, and no opaque patch body — the bodies are
explicitly not copied (`:17`, `:45`, `:68`, `:91`).

Against the eight rows in `preregister.json` (`edit_decisions`), the source supplies:

| decision row | verdict | observation support in S086 |
|---|---|---|
| `DECLARED_EDIT` | ALLOW | partial — a structured, explicitly-pathed own-report edit; "predeclared" is not visible in the source |
| `UNDECLARED_EDIT` | DENY | none |
| `READ_ONLY_EDIT` | DENY | none |
| `WRITE_ONLY_EDIT` | DENY | none — no observation where a target was written without a recorded read |
| `OPAQUE_PATCH` | UNKNOWN | none — no observation carries a patch body |
| `EDIT_TRAVERSAL` | DENY | none — no alternate spelling or dot-segment path appears |
| `EDIT_EXTERNAL` | DENY | none — every recorded path is a plain absolute filesystem path |
| `EXPANSION` | CHECK_EACH | one partial analogue — the CritRuntime three-step chain only (`:18-28`) |

**Impact.** The source is a positive-case, shape-diversity sample. It cannot validate a
single denial rule, and it cannot validate any read-authority prerequisite (see HIGH-3 and
MEDIUM-4 for the additional reasons the prerequisite is not exercised). C1's own scope
wording — "new document contract, not eight repaired runtime behaviors" — is the honest
frame; the risk is that a downstream artifact cites S086 as *evidence for* the eight rows
rather than as the *occasion* for writing them.

**Recommendation.** Keep C1's existing scope sentence verbatim and append one clause:
the observation source is a positive-case sample that supports no denial row. Any policy
row citing S086 must cite it for observed argument-key shape only, never as behavioural
proof of that row's verdict.

### HIGH-3 — The only recorded read carries a selector suffix, so exact-path target matching would not count it as read authority

The single read recorded anywhere in the source is at `:20-22`:

```
"line": 12, "tool": "read",
"path": ".../.ufo/waves/round-22/build/CritRuntime.md:raw"
```

while the corresponding edit target at `:16` is `.../round-22/build/CritRuntime.md` — with no
selector. The recorded write at `:26-27` has the same selector-free path.

`:raw` is a read *selector* form, not part of the filesystem path. Under a v2 audit rule
that compares recorded paths for exact equality against the declared edit target, the only
read in the entire source would fail to satisfy:

- `DECLARED_EDIT` — "Exact target is predeclared for edit **and for both read and write**"
- `WRITE_ONLY_EDIT` — "Edit also needs its explicit target read authority"

The CritRuntime chain would then be adjudicated as missing read authority on the strength
of a selector-suffixed read that a human reader would recognise as the same target.

**Impact.** This is a concrete, mechanical defect risk in the exact place C2 is meant to
bind. It is a false-denial risk in the audit, and it is invisible unless selector
normalisation is specified before comparison.

**Recommendation.** The v2 audit contract must define target normalisation explicitly —
strip read selectors (`:raw`, `:N-M`, `:raw:N-M`) and any query suffix before comparing —
and the events schema should carry a normalised target field next to the raw path so the
comparison rule is auditable rather than implicit. This is a contract recommendation for
the C2 author; this seat does not decide the normalisation rule.

### MEDIUM-4 — `recorded_starts` line fields are not uniformly ordered and cannot establish precedence beyond one chain

For three of the four observations the recorded "start" line is **later** than the request
line: `:35` request line 30 vs `:48` start line 31; `:58` request line 33 vs `:71` start line
34; `:81` request line 36 vs `:94` start line 37. Each such `recorded_starts` entry names an
`edit` — i.e. the same operation class as the request it annotates.

Only CritRuntime (`:9` request line 15) lists steps that precede its request: read at `:20`
(line 12), write at `:26` (line 13).

The source's scope sentence (`:101`) says these are "recorded adapter steps" and explicitly
not "reading proof", which is consistent with treating them as an unordered set of scoped
steps rather than a timeline.

**Impact.** An audit that infers "read happened before edit" from these line numbers will
mis-order three of four observations. Conversely, an audit that requires ordering evidence
will find ordering evidence for exactly one chain.

**Recommendation.** The `EXPANSION` row ("Every recorded adapter read or write remains
separately scoped") should be implemented as *per-step scoping without ordering
inference*, matching the source's own scope sentence. If ordering is to become an
auditable fact, the v2 events schema needs an explicit monotonic step sequence per
observation; transcript-relative line numbers are insufficient and, as recorded, are
internally inconsistent.

### MEDIUM-5 — Two distinct edit signatures exist and the eight-row taxonomy has no row for a non-canonical structured signature

Observed argument-key shapes:

- `["path", "stream_content"]` (`:12-15`) — CritRuntime;
- `["i", "new_string", "old_string", "path"]` (`:38-42`, `:61-65`, `:84-88`) — all three
  OraclePathArtifact observations.

Two differences matter for any audit. First, the canonical four-key shape is not universal:
one observed edit carries neither `old_string` nor `new_string`, and `stream_content` is
not defined anywhere in the source. Second, the `i` (intent) key is present in one shape and
absent in the other — so key *presence* is not a reliable discriminator of tool identity
either.

Note the distinction the taxonomy currently blurs: the CritRuntime call has a **structured
target** (an explicit `path`) and a **non-canonical payload** (a whole-content replacement
rather than a found/replaced span). `OPAQUE_PATCH` is defined as "Missing structured target
is not inferred from opaque patch text" — which is a *target-opacity* rule, and does not
describe this observation.

**Impact.** If the v2 audit keys classification on the canonical four-key shape, a
`stream_content` edit is unclassifiable and can fall out of the audit entirely rather than
being adjudicated — the precise failure mode `OPAQUE_PATCH → UNKNOWN` exists to prevent.
The eight-row decision set also has no home for "structured target, non-canonical payload".

**Recommendation.** Route to the C1 author (this seat's source cannot decide the decision
set): the v2 classification must be signature-agnostic, and either a new row is added for
"structured target with full-content payload" or such calls are explicitly classified
`UNKNOWN` alongside `OPAQUE_PATCH`. Either way the requirement is that no edit-shaped call
is left unadjudicated. Recording the observed shapes verbatim in the v2 events schema
(including the key set, not just the target path) is the minimum needed to make that
checkable.

### MEDIUM-6 — The source is round-22 evidence and carries no round-23 conformance information

Every agent id is round-22 (`:7`, `:33`, `:56`, `:79`) and every recorded path is under
`.ufo/waves/round-22/build/` (`:16`, `:22`, `:27`, `:50`, `:73`, `:96`). Round-23 seats have
different wave directories and different per-seat write paths.

**Impact.** The source justifies the *design* of the v2 audit by analogy with observed
round-22 call shapes. It is not evidence that round-23 seats conform to the v2 authority.
Any round-23 conformance statement must come from round-23's own captured events
(`preregister.json` C2 command: `--events .ufo/waves/round-23/<WAVE>/events.json`).

**Recommendation.** Label S086 as prospective / design-justifying in every round-23
artifact that cites it, and keep it out of the evidence chain for round-23 seat behaviour.

### MEDIUM-7 — The source declares no denominator, so it cannot be cited as an exhaustive census

The observations array (`:4-99`) closes with the scope sentence at `:101`, which bounds
*what the records mean* but never states whether these four observations are **all** edit
calls in the reviewed round-22 cohort or a selected sample. No count, no selection rule, no
list of inspected transcripts, and no seat coverage statement are present.

This matters because the round-23 preregistration carries an explicit path census
(`outside_round22.path_counts_as_reported`: rough build 25 / falsify 33; lane build 23 /
falsify 29) and C3's stated goal is an "exhaustive per-event/component explanation" of
those counts.

**Impact.** If the C3 reconciliation record uses S086 to explain edit-related path counts,
it must not silently treat four observations as a census. The distinction is the difference
between an exhaustive reconciliation and a partial one dressed as exhaustive.

**Recommendation.** The reconciliation record must carry the observation denominator (how
many edit calls were observed across which transcripts and seats) together with the
selection rule, or must declare the observation set explicitly non-exhaustive. Absent
either, the reconciliation may not use the word "exhaustive" for anything derived from
this source.

### MEDIUM-8 — Receipt presence, record presence, and effect presence are three distinct states and the round-23 artifacts need to keep them apart

This is the seat's central work statement, and the bound files are consistent about it:

- the observation source disclaims effects, native enforcement, universal tool semantics and
  reading proof (`:101`);
- the cohort checker states that `delivered_conformant` means receipt-well-formed only, and
  that report hashes bind evaluated-revision bytes to the trusted producer settlement
  "not independently proven timing or provider causes" (`:20`);
- the round-23 limits bar runtime prevention, effect/reading/recorder-completeness claims,
  and universal tool/patch semantics (`preregister.json` → `limits`).

The cohort tool already carries the vocabulary needed to keep these apart, and round-23
should reuse it rather than invent a parallel one:

- `category` — `delivered_conformant` / `delivered_faulty` / `absent_dead` /
  `absent_unresolved` (`:76`, `:83`);
- `report_read_available` — whether the report bytes were actually retrievable (`:83`);
- `strict_conformance` / `strict_receipt_exit` — the receipt-conformance verdict (`:98-99`);
- `unclassified` — seats that could not be classified at all (`:71`, `:91`).

**Recommendation.** Every round-23 artifact should state, in prose adjacent to any
completion claim, which of the four states it is asserting: *receipt well formed*, *record
present*, *effect observed*, *reading proved*. A seat that delivered a well-formed receipt
has asserted only the first.

### MEDIUM-9 — A strict-evaluation failure can be silently reclassified as a seat fault

`check-review-cohort.py:61` synthesises a one-seat manifest containing only `schema` and
`reviews`:

```
one_manifest = json.dumps({'schema': data['schema'], 'reviews': [review]})
```

Every other top-level manifest field is dropped. The strict evaluator's manifest-schema
requirements are outside this seat's read scope, so it cannot be confirmed that `schema`
plus `reviews` is sufficient. If it is not, the per-seat strict evaluation returns exit 2
(`CANNOT_EVALUATE`) and `:76` — `category = 'delivered_conformant' if one_code == 0 else
'delivered_faulty'` — files an *unevaluable* seat under `delivered_faulty`, with
`strict_exit: 2` visible only inside the seat row (`:83`) and no cohort-level finding
raised (`:89`).

**Impact.** A manifest-shape problem can be masked as a per-seat receipt fault, and
`unclassified` (`:71`) — the bucket reserved for "cannot classify" — stays at zero.

**Recommendation.** The per-seat classification should distinguish strict exit 2
(`CANNOT_EVALUATE`) from exit 1 (`FAIL`), and a per-seat `CANNOT_EVALUATE` should raise a
cohort-level finding rather than being absorbed into `delivered_faulty`. Independently,
the one-seat manifest should preserve the whole manifest's shape rather than two fields.

### LOW-10 — Chronology is date-only and transcript-relative

`"accessed": "2026-10-21"` (`:2`) carries no time or timezone. The `request_line` and
`recorded_starts[].line` fields are transcript-relative with no wall-clock anchor, and the
source's own scope disclaims chronology-grade claims indirectly by disclaiming reading
proof (`:101`). Sub-day ordering claims, and any claim tying an observation to a specific
round-22 closure event, are unsupported by this source.

### LOW-11 — The transcript digests and argument keys are asserted, not re-derived here

`transcript_sha256` values appear at `:8`, `:34`, `:57`, `:80`. Per this seat's contract no
raw unbound session path was opened and no digest was computed; the argument-key lists are
therefore taken as asserted by the source and were checked only for internal consistency
with the recorded `tool` and `path` fields.

### LOW-12 — No validator for the observation schema is in scope

The file declares `"schema": "tsukuroi-structured-edit-observations-v1"` (`:1`). The only
validator in this seat's read scope is `check-review-cohort.py`, which validates review
manifests and settlements — not this schema. Whether a validator exists, and whether this
file satisfies any shape beyond what was read here, cannot be confirmed from the bound
files.

## 3. Bounded recommendations (source-only; no execution implied)

1. Cite `strict_conformance` / `strict_receipt_exit` / per-seat `strict_exit`, never the
   cohort tool's `status`, as receipt-conformance evidence (HIGH-1).
2. State that S086 is a positive-case, shape-diversity sample supporting no denial row;
   keep C1's "document contract, not repaired runtime behaviors" framing (HIGH-2).
3. Specify target normalisation — selector stripping — before any read/write/edit target
   comparison, and record a normalised target field (HIGH-3).
4. Implement `EXPANSION` as per-step scoping without ordering inference, and add an
   explicit step sequence to the v2 events schema if ordering is to become auditable
   (MEDIUM-4).
5. Make v2 classification signature-agnostic and route the "structured target, non-canonical
   payload" shape to a defined decision so it cannot fall through unadjudicated (MEDIUM-5).
6. Label S086 as prospective/design-justifying; source round-23 conformance only from
   round-23 events (MEDIUM-6).
7. Attach an observation denominator and selection rule to the C3 reconciliation record, or
   declare the set non-exhaustive (MEDIUM-7).
8. Use the cohort tool's existing four-state vocabulary for receipt / record / effect /
   reading claims in every round-23 artifact (MEDIUM-8).
9. Separate strict exit 2 from exit 1 in per-seat classification and preserve the full
   manifest shape in the one-seat manifest (MEDIUM-9).

## 4. Residual risk and verification gaps

- **Not executed.** Nothing in this review was run, fetched, hashed, listed, imported or
  delegated. No digest was computed; the source identity is the supplied declaration.
- **Strict evaluator out of scope.** `tools/check-review-snapshots.py` is not in this seat's
  read scope. Its `has_controls` semantics, its manifest-schema requirements, and its
  finding ids are inherited by the cohort tool but were not read here (LOW-12, MEDIUM-9).
- **Transcripts not opened.** The argument-key sets and recorded steps are asserted by the
  source; they could not be re-derived or refuted within scope (LOW-11).
- **Effects unproven by construction.** The source disclaims effects, native enforcement and
  reading proof (`:101`). No statement in this report should be read as evidence that any
  recorded edit changed any file.
- **Denominator unknown.** Whether the four observations are a census or a sample is
  undetermined (MEDIUM-7); every conclusion above that depends on coverage is therefore
  scoped to "the observations as recorded".
- **Ordering unproven.** Only one of four observations carries steps that precede its
  request line, and those line fields are internally inconsistent across observations
  (MEDIUM-4).
- **Unverified schema conformance** of the observation source against any validator
  (LOW-12).
- **Recommendation routing.** Items 3, 4 and 5 touch the C1/C2 contract text, which this
  seat does not own and cannot amend; they are routed as findings rather than applied.

## 5. Lane bounds

Leaf member — no subagent dispatch. Read-only against all bound sources; the only write is
this report.

Reviewed-SHA256: 19d85129bf0f7fd71f5aea93c35660b21d305150500dc63b58104019851af12a
Predicate: r23-review23terminal
Scope: executed=none
