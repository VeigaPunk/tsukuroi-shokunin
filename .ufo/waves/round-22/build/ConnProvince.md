Report: .ufo/waves/round-22/build/ConnProvince.md

# ConnProvince — round-22 scope-bleed connector

Role: find one non-obvious, non-harmful move for the declared axes, using only the
round cache. This is an advisory boundary analysis. It judges, admits, edits,
integrates, ships, and invokes no runtime, and reads no sibling or operator file.

## Method and evidence base

Files read, exactly and only:

- `.ufo/waves/round-22/snapshot/PROVINCE.md` (digest taken from the seat binding; no
  hashing command was executed, so the digest is asserted as bound, not re-derived)
- `.ufo/waves/round-22/preregister.json`
- `.ufo/waves/round-22/sources/host-tool-boundary.json`
- `skill://godspeed`

No execution, no fetch, no network, no sibling reads, no fleet/operator files, no
Git or VCS state, no tests. Every quotation below is from the three cache files
above; sibling ownership words are attributed to the sibling through the snapshot's
pinned locator, never asserted as tsukuroi authority. The pin is stale by design
(`PROVINCE.md`: "Re-read the cited declaration before a later handoff; the table does
not freeze another lane's authority."), and this seat cannot re-read it.

## Axes named

| Axis | Round metric | This report's contribution | Harm check |
|---|---|---|---|
| C1 depth | `validated_boundary_decisions` 0 → 6 | Nominate two decision slots with exact machine-checkable text: D-JURIS (jurisdiction) and D-ATTEST (evidence provenance) | Does not invent the other four; does not legislate sibling scope; adds no surface |
| C2 operability | `request_audit_mode` 0 → 1 | Bound the audit's verdict space to conformant / nonconformant / unverifiable and state what it must never claim | Adds an explicit unknown state rather than loosening detection; fail-closed preserved |
| C3 calibration | `cohort_accounting_mode` 0 → 1 | Force a four-class partition with absence≠fault and a named-artifact citation for every absence | Strengthens strictness; resolves the fail-closed/absence contradiction instead of hiding it |

The move harms no axis: C1 gains a real boundary rather than a padded one, C2 gains
an honest third verdict, C3 gains a partition invariant it already implies.

## The bleed surface, split into three layers

"Tool/runtime authority" is ambiguous and the ambiguity is where the bleed lives.
Separate it before writing any claim:

- **L1 — host dispatch schema.** `host-tool-boundary.json` enumerates `task_fields` as
  `i`, `context`, `tasks[{task, solutionSpace, name?, agent?, tools?, sourceSession?,
  model?}]`. There is no path, command, fetch, or per-seat permission field. The seat
  bindings used this round (`read_paths`, `write_paths`, `commands`, `fetches`) are
  prompt text, not dispatch arguments. `native_per_seat_allowlist` is `false`, and the
  file's own `authority` is "Main message to TsukuroiR22"; `tools_semantics` is
  "Eval-defined additive extras; not an allowlist or replacement of native tools."
  L1 is a Main-attested host fact and an input, not a tsukuroi probe.
- **L2 — OMP task/hub and orchestration runtime.** `PROVINCE.md` OUT-006 quotes
  kumitate's title-preamble scope as "**Domain:** orchestration & tooling — scopes OMP
  task/hub, ufo-fsd scripts & runtime", and proposes that "task/hub dispatch and
  routing semantics are its analysis, not tsukuroi's". ADJ-05 routes the same trigger
  to kumitate and requires that unit liveness "cannot prove dispatch correctness".
  L2 is out of province. Note the pinned-commit caveat: the locator is OUT-006 at
  `1770305fae20`, not a live declaration.
- **L3 — this repo's own checkers.** `check-boundary-contract.py`, `check-seat-bindings.py`,
  `check-review-cohort.py` are implementation in this repo. ADJ-07 retains for
  tsukuroi "Census bug, domain contract, implementation and repair in this repo" and
  asks tameshi only for method advice, "not transfer of gate ownership or a general
  claim from one lane". L3 is in province **as detection**, exactly as the round-12
  refinement says: "The census owns detection only; no mode repair, service restart,
  subvolume creation, boot or package transaction is authorized by a finding."

The bleed is any sentence that smuggles an L1 or L2 property into an L3 artifact, or
that upgrades L3 detection into an L1/L2 capability.

## Decision rule: lane-local safety evidence vs owning global enforcement

Apply a four-part test. Enforcement requires all four; evidence requires none:

1. **Policy authority** — the actor may bind all seats, not only its own declared ones.
2. **Pre-request evaluation** — the check sits in the dispatch or pre-execution path.
3. **Denial power** — a failing check can stop or alter the request.
4. **System of record** — the verdict is authoritative for the runtime.

Round 22 has (1) only inside its own prompt-declared seats, (2) no (`host_decision`
approves a "fail-closed post-hoc audit"), (3) no (`limits` includes "No native
preventive tool enforcement"), (4) no (events are lane-recorded). Therefore every
round-22 artifact is lane-local safety **evidence**, and any wording that reaches
(2), (3), or (4) is scope bleed into the host dispatch path and into kumitate's L2.

Corollary that costs nothing and closes a real hole: *the verifier's read set must be
a subset of what it is entitled to read, and it must not open the paths it judges.*
Path conformance is a string comparison against declared bindings and recorded
events; if the audit must `stat` or read the requested path to decide, the audit
itself crosses the boundary it is measuring. State this as an invariant, not a hope.

Corollary two: `fail-closed` is an **evidence-quality** property — missing or
unparseable evidence cannot yield success — not a runtime property. The runtime does
nothing; the checker declines to certify.

## Bleed register (trigger → owner → bounded replacement)

| ID | Trigger phrase or artifact shape | Bleeds into | Why out of province | Bounded replacement |
|---|---|---|---|---|
| B-01 | "enforce", "enforcement", "gate", "block", "prevent" applied to seat scope | Host dispatch (L1), kumitate (L2) | `host_decision`: "Never call this runtime enforcement"; `limits`: "No native preventive tool enforcement" | "post-hoc detection with fail-closed reporting" |
| B-02 | "allowlist" applied to the `tools` field | L1/L2 | `tools_semantics`: "not an allowlist or replacement of native tools" | "eval-defined additive extras; a missing extra is never a nonconformance" |
| B-03 | "added/verified a per-seat allowlist" | L1 | `native_per_seat_allowlist: false` | "prompt-level declared scope bindings, outside the dispatch schema" |
| B-04 | "the task tool accepts only declared paths" | L1 | `task_fields` contains no path, command, or fetch field | "the binding text is handed in the prompt; dispatch carries no path field to validate" |
| B-05 | "the seat could not have read/wrote X" | L1 evidence claim | `limits`: "No proof of actual reading, request effects" | "no recorded request names X; actual I/O is unverified" |
| B-06 | "covers all requests" / fleet-wide coverage | L2, fleet | Seat scope forbids fleet reads; dispatch is kumitate's analysis | "seats declared in this round's tsukuroi manifest" |
| B-07 | "the audit prevents/halts a bad request" | L1/L2 | Post hoc by construction; no denial power | "the audit runs after a declared cut and reports; it changes nothing" |
| B-08 | "the shell command stayed in scope" | L1 evidence claim | `limits`: "arbitrary-shell semantics" unproven | "exec recorded; shell path containment unverifiable; a declared empty `commands` list makes any exec nonconformant" |
| B-09 | "no receipt, so the seat failed" | C3 calibration | `C3_bound` requires four classes; `limits`: "No replacement seats" | "absent-dead / absent-unresolved, with the missing artifact named" |
| B-10 | "wave/seat caused the OOM or pressure" | mori | `PROVINCE.md`: counters "do not establish which fleet wave caused pressure" | "host pressure observed at T; wave attribution not claimed" |
| B-11 | "tsukuroi verified OMP runtime behavior" | kumitate L2 | OUT-006 includes "ufo-fsd scripts & runtime" | "the lane's own checker behavior; OMP runtime semantics are out of province" |
| B-12 | "the boundary contract defines fleet rules" | tameshi method ownership | ADJ-07: method advice only, "not transfer of gate ownership" | "validates this round's written decisions, not fleet-wide rules" |
| B-13 | "the model/sourceSession choice was wrong" | kumitate (dispatch) / kama (served identity) | ADJ-05 and ADJ-01 split these from host state | "recorded only; not adjudicated" |
| B-14 | `bindings.json` treated as the authoritative roster | Verification surface | The manifest is both scope source and audit input → self-attestation loop | "roster from the round's declared seat list; the manifest must cover every declared seat or the audit fails closed naming the uncovered seat" |
| B-15 | Event records carrying argv, environment, tokens, or secrets | ADJ-05 / ADJ-02 evidence hygiene | ADJ-05: "exclude tokens, environment and raw process arguments"; ADJ-02 forbids secret values | "record path strings and declared command literals only; redact argv/env/token material at capture time" |

## Proposed move — two decision slots plus exact claim language

D-JURIS and D-ATTEST are **candidates for slots among C1's six**. This connector does
not assert that six exist, does not name the other four, and does not treat these as
already validated. Whatever the six are, the contract checker should reject any
decision record missing `prohibited`, `non_claims`, or `recipient`, so that over-claim
cannot validate.

### D-JURIS — lane-local prompt scope vs dispatch/tool-runtime authority

- **Surface:** the line between a lane's own prompt-declared seat scope and host or
  kumitate-owned dispatch and tool-runtime authority.
- **Permitted (in province):** declare per-seat prompt-level read/write/exec/fetch
  bindings for seats this lane dispatches; record lane-local request/response events
  for those seats; validate recorded requests against those bindings after the fact;
  report each request as conformant, nonconformant, or unverifiable; account for every
  declared seat in the C3 cohort.
- **Prohibited (out of province):** asserting, implementing, or implying any host-side
  allowlist, interception, denial, or preventive enforcement; modelling or judging OMP
  task/hub dispatch, routing, tool selection, or runtime semantics; treating `tools` as
  a permission set; claiming proof of actual reading, request effects, arbitrary-shell
  semantics, or host recovery; attributing host pressure or outcome to a wave or seat.
- **Recipient for the prohibited half:** kumitate for dispatch, routing, and
  orchestration semantics (ADJ-05; OUT-006 at `1770305fae20`); the protocol integrator
  where ownership is unresolved, since "unresolved ownership goes to the protocol
  integrator, never to whichever lane answered first." Recording the Main-attested
  absence of a native allowlist is an input, not a tsukuroi finding about L2.
- **Evidence class:** lane-local recorded events, the literal binding text handed to
  each seat, the round manifest, and the Main-attested host decision of 2026-10-21.
- **Non-claims:** no runtime enforcement; no dispatch-path behaviour; no actual reading
  or request effect; no shell-semantics containment; no replacement seat; no fleet
  census.
- **Falsifier:** a checker that passes a request naming an undeclared path; that
  reports success when a declared seat has no events; or that restates `tools` as an
  allowlist.

### D-ATTEST — host-runtime facts are attributed inputs, not lane probes

"Host-runtime facts used by round 22 — the task field inventory, `tools` as
eval-defined additive extras, and the absence of a native per-seat allowlist in the
dispatch path — are recorded with their authority (Main message, 2026-10-21). They are
inputs of stated provenance, not tsukuroi probes or findings. The lane may restate
them only together with that attribution and may not extend them to unobserved host
behaviour. If later evidence contradicts one, the round records a superseding entry;
it does not retrofit the earlier claim and does not silently widen it."

Precedent for phrasing-level correction rather than silent re-reading exists in this
snapshot: R20-OUT009 "explicitly supersedes only the OUT-009 proposition's unqualified
'Revenger owns' wording and its broad 'packages' paraphrase." D-ATTEST generalises
that discipline to host facts.

### C2 — exact bounded claim language (`request_audit_mode`)

> Round-22 C2 adds a post-hoc, lane-local request audit. Given the round's declared
> per-seat bindings and the events recorded for those seats, it returns for each
> recorded request one of conformant, nonconformant, or unverifiable, by comparing the
> requested path, command, or fetch against that seat's declared `read_paths`,
> `write_paths`, `commands`, and `fetches`. Unverifiable is not conformant and forces a
> non-success audit result. A declared seat with no recorded events is reported as
> absent-unresolved or absent-dead under C3, never as delivered-faulty. The audit runs
> after a declared cut, does not intercept, deny, or alter any request, does not open
> or stat the paths it judges, does not assert that any seat actually read, wrote,
> fetched, or executed anything, and does not describe or depend on task/hub dispatch
> or tool-runtime semantics. `tools` remains eval-defined additive extras; a missing
> extra is never a nonconformance. This is detection and evidence, not runtime
> enforcement.

Operational clauses that belong in the same artifact, not in prose elsewhere: the cut
is a UTC timestamp plus the events-file identity, so a mid-flight snapshot cannot make
in-flight requests look absent; path containment is normalised (no raw `startswith`,
so `/a/bc` is not inside `/a/b`; reject or flag `..`; decide trailing-slash and case
handling explicitly); and the audit's read set never includes the paths it judges.

### C3 — exact bounded claim language (`cohort_accounting_mode`)

> Round-22 C3 accounts for every seat declared for this round as exactly one of
> delivered-conformant, delivered-faulty, absent-dead, or absent-unresolved, citing for
> each the strict receipt findings it relies on and naming every missing or
> unparseable artifact. Absence of a receipt is classified by absence, not fault; a
> seat is never marked delivered-faulty for data that was not delivered. The cohort is
> this round's declared tsukuroi seats; it is not a fleet census and does not stand in
> for one. The accounting reports how many declared seats were classified, that the
> four classes partition the cohort, and which findings were strict. It does not claim
> that every receipt conforms, does not infer seat behaviour beyond the receipts, and
> does not replace a seat or repair a missing one.

## Contradictions, stated rather than smoothed

1. **Fail-closed vs absence≠fault.** C2's fail-closed reporting and C3's four-class
   accounting pull in opposite directions if applied at the same level. Resolved by
   level, not by compromise: fail-closed governs the per-request predicate
   (unverifiable cannot pass); the four-class partition governs cohort membership
   (no events cannot become a fault). A tool exit status of non-zero with a cohort
   line of absent-unresolved is the correct, non-contradictory output.
2. **C1 depth vs sibling authority.** The province text says the anchor table "does
   not freeze another lane's authority," so D-JURIS must decide *this lane's* claim
   surface, not re-declare kumitate's scope. A decision phrased as "kumitate owns X"
   would inflate C1 depth by legislating a sibling and would contradict the locator's
   own limits. Phrase it as "tsukuroi may not model X; the route is ADJ-05/OUT-006."
3. **Generic install authorization vs this seat's scope.** The operator tooling
   directive authorizes installs with passwordless sudo; the seat contract's NO-EXEC
   takes precedence and host pacman transactions are paused host-wide. This report
   performs no install and records none, and round-22 claim language must not imply
   that audit findings authorize host mutation — `PROVINCE.md` already states
   "Never installs, upgrades, or removes packages; never restarts services. Detection
   and report; the operator remediates."
4. **"Mode" naming vs capability.** A metric called a *mode* invites readers to assume
   the feature toggles runtime behaviour. Nothing in the host decision or the task
   schema supports that. The claim language above is independent of the flag's name;
   if the implementation uses "mode", its documentation must state that the mode
   selects reporting strictness only, not request handling.

## Second-order effects

**Runtime.** Nothing enters the dispatch path, so the audit cannot reduce a bad
request's blast radius; its only runtime effect is latency in a report job. If a later
round wants prevention, the required change is a host or dispatch facility owned by
kumitate or the integrator, and round-22 evidence must not be cited as proof such a
facility exists. A mid-flight audit also creates a race where in-flight requests read
as absent; the declared cut plus events-file identity is the mitigation.

**Contract.** No ADJ row and no OUT anchor changes. D-JURIS points at ADJ-05 and
OUT-006 as locators only; it must not quote live sibling bytes and must not edit the
adjacency table. If kumitate's declaration drifted after `1770305fae20`, the handoff
requires a re-read at its then-HEAD, which this seat cannot perform; the decision
should say "stale by design" rather than imply current scope.

**Substrate.** Host package, service, boot, and firmware state stay untouched. The
current host-wide pause on pacman transactions and the no-restart rule are respected.
Event capture must be redacted at record time (B-15), because ADJ-05's own minimum
evidence packet excludes tokens, environments, and raw process arguments, and ADJ-02
excludes secret values; an audit log that ingests argv would itself create the
handoff leak the province forbids.

**Verification.** The manifest is both the scope source and the audit's input, an
attestation loop; B-14 breaks it only if roster membership comes from the declared
seat list. Conformance is conditional on event honesty, because events are
lane-recorded; the claim wording above says "recorded request", never "request". The
audit's own read set is a verification surface too: it must not open judged paths,
which also keeps the verifier inside the seat's NO-FETCH/NO-EXEC bounds.

## Risks

| Risk | Effect | Mitigation in this proposal |
|---|---|---|
| Over-claim by verb or by tool name (`check-seat-bindings`) | Reader infers host-level seat validation | B-01..B-04; name the object "declared prompt-scope bindings against recorded events" |
| Manifest self-attestation | A dropped seat silently shrinks the cohort | B-14; fail closed naming the uncovered seat |
| Absence→fault conflation | C3 overstated, calibration axis harmed | Four-class partition clause; exit status separated from cohort class |
| Second-hand host fact treated as probe | A single Main attestation hardens into a runtime claim | D-ATTEST; supersession clause |
| Stale OUT-006 pin used as live scope | Misrouted handoff to kumitate | Cite as locator; require re-read before handoff |
| Redaction deferred to handoff | Tokens or argv leak into build artifacts | B-15; redact at capture |
| Naive path containment | Prefix-collision false conformant | Normalisation clause plus fixture in verification |

## Verification (source-only; for the round's executor, not performed here)

1. Grep every round-22 artifact for the B-01..B-03 trigger set; each hit must sit in a
   negation, limit, or attribution context.
2. Confirm each C1 decision record has `permitted`, `prohibited`, `recipient`,
   `evidence_class`, `non_claims`, and `falsifier`; a missing field is a validation
   failure, not a warning.
3. Fixture: an event naming an undeclared path → nonconformant, non-zero exit.
   Fixture: `/root/abc` event against declared `/root/ab` → nonconformant.
   Fixture: a `..`-bearing path event → unverifiable.
4. Fixture: a declared seat with zero events → absent-dead or absent-unresolved; the
   four classes must sum to the declared seat count.
5. Fixture: malformed receipt → absent-unresolved naming the artifact; never
   delivered-faulty.
6. Fixture: conformant request with no `tools` entry → still conformant (no allowlist
   semantics).
7. Confirm no path outside `.ufo/waves/round-22/build/` is written and no sibling,
   lane-Git, or operator file is read.
8. Confirm the audit does not open or stat judged paths, by design review or read-set
   trace.

## Non-claims

No runtime enforcement. No host allowlist. No dispatch or routing semantics. No proof
of actual reading, request effects, shell semantics, or host recovery. No fleet
census. No replacement seat. No sibling authority. No install, update, restart, or
package transaction. No assertion that the other four C1 decisions exist or are
correct.

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: a296da872e83731f7f7a7737662988558ebb97e4399681a1099fab4a259b7a79
Predicate: r22-connprovince
Scope: executed=none
