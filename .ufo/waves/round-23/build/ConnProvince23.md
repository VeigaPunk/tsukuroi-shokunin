# ConnProvince23 — r23 build: is the new edit-target audit lane-local, or does it annex orchestration?

## Binding and evidence floor

- Reviewed artifact: `.ufo/waves/round-23/snapshot/PROVINCE.md`, declared SHA256
  `a296da872e83731f7f7a7737662988558ebb97e4399681a1099fab4a259b7a79`. That digest is a
  supplied identity; it was not recomputed, and nothing in this report depends on bytes
  outside the bound files.
- Read inside binding: `preregister.json`; `sources/edit-decision-policy.json`;
  `sources/godspeed-directive.txt`; `skill://godspeed`; `snapshot/PROVINCE.md`.
- **Declared gap, not improvised:** `edit-decision-policy.json` names its evidence source as
  `source_path: .ufo/waves/round-23/sources/structured-edit-observations.json`, and all eight
  decisions cite `evidence: S086`. That path is not in this seat's read binding. This report
  therefore audits *declarations, cross-artifact consistency and scope wording*; it does not
  claim to have seen the observed request keys or adapter steps. "Source-grounded" in C1 is
  taken as declared, unverified here.
- `executed=none`. No command, fetch, listing, hash, import, delegation or write beyond this
  file. Claims about tool behavior below come from this seat's own tool contract, which is
  system-authored, not from a probe.

## Axes

1. **C1 depth** — eight source-grounded structured-edit authority decisions; count fixed at 8, before 0.
2. **C2 operability** — schema-v2 audit authority for exact predeclared structured edit targets.
3. **C3 calibration** — frozen-r22 path-census reconciliation of the two fixed cohorts.
4. **Connector axis (this seat):** does the audit/reconciliation remain *local-artifact* evidence —
   the same class as the province's existing log-plus-readable-file pairing — while avoiding
   native orchestration enforcement, runtime state claims, and routing/recorder ownership?

A wording move is kept only if it improves at least one axis and harms none.

## Findings

### F1 (pass) — the audit is local-artifact evidence of an existing province class

The policy file's own scope line bounds it to "Declared audit authority for structured target
metadata only; no native prevention, opaque patch interpretation, effect or reading proof."
`preregister.json:limits[0]` says "No native per-seat restrictive tool interface exists", and
`limits[1]` excludes "runtime prevention, effect/reading/recorder-completeness or universal
tool/patch semantics". C1's scope says "new document contract, not eight repaired runtime
behaviors"; C2's says "Body data opaque, no native enforcement/effects claim."

The checker inputs are declared binding text and captured event text — repository files read
the way PROVINCE.md already reads `.pacnew`/`.pacsave` drift ("Pair pacman-log history with
current readable filesystem findings; report skipped unreadable paths"). No probe, unit,
package, service or boot surface is added, and the snapshot's Core table plus ADJ-01..ADJ-07
remain untouched by r23. Nothing in the bound text puts a new surface into Core; a build that
did so would be an unratified surface expansion, since the reviewed snapshot's last refinement
is R20-OUT009.

Cross-artifact consistency holds: the eight ids, verdicts, reason strings and order in
`preregister.json:edit_decisions` are identical to `decisions[]` in the policy file, and the
policy pins `policy: round23-preregister`. C1's `target: 8` is a count of declared decisions,
not an inventory claim.

Live discriminative test on this seat's own binding, which is the cheapest real evidence the
taxonomy separates what it claims to separate: `build/ConnProvince23.md` is in `read_paths`,
`write_paths` and `edit_paths` → DECLARED_EDIT/ALLOW; `preregister.json`, `PROVINCE.md` and the
policy JSON are read-only → READ_ONLY_EDIT/DENY; `sources/structured-edit-observations.json`
is in neither list → UNDECLARED_EDIT/DENY. Three cells fire correctly on one real binding
without any runtime cooperation.

### F2 — `DENY` is an audit verdict, not a block, and the cells do not say so

The eight cells mix ALLOW / DENY / UNKNOWN / CHECK_EACH. Read alone, DENY reads as "the
adapter refused" or "the harness forbids it" — exactly the native-prevention claim that
`limits[1]` and the seat contract forbid. The exclusion exists in the scope line and limits,
but not where a reader actually looks: inside the decision row. One defining sentence under
the table makes all eight cells self-describing at the point of use.

### F3 — `EDIT_EXTERNAL` adjudicates a routing surface this lane does not own (primary finding)

Current cell: `["EDIT_EXTERNAL", "DENY", "Remote or internal URIs do not become filesystem edit targets"]`.

**Concrete counterexample.** This seat's own tool contract states that `write` targets
`xd://<tool>` (JSON args as `content` to `xd://report_issue`), and peer coordination targets
`write agent://<id>`. A `write` to `xd://report_issue` is a sanctioned, expected operation in
this very runtime. It is not a filesystem path. A captured adapter step recording that write
would fall in the class the cell names ("internal URIs"), and a literal application of the
reason records **DENY against a sanctioned device write**. Two consequences follow, and both
are ownership problems rather than wording taste:

1. The audit would be stating a *resolution rule* for harness URI/device selectors. OUT-006
   assigns that surface elsewhere: "**Domain:** orchestration & tooling — scopes OMP task/hub,
   ufo-fsd scripts & runtime", with the proposition "Kumitate scopes OMP task/hub and
   orchestration tooling, so task/hub dispatch and routing semantics are its analysis, not
   tsukuroi's." A lane that resolves `xd://`/`agent://`/`local://`/`proc://` is doing routing
   analysis, not host evidence.
2. The DENY also asserts a prevention outcome ("do not become"), which `limits[1]` excludes.
   PROVINCE.md is blunt about this pattern: "Shared evidence is not shared ownership;
   unresolved ownership goes to the protocol integrator, never to whichever lane answered
   first."

This is in the anticipated class, not hypothetical: the policy author wrote "internal URIs"
into the cell, so events of this shape were expected and are exactly where the leak lands.

**Wording recommendation (keeps all eight ids, verdicts and the count of 8 intact).** Add one
sentence in the C1 record directly under the decision table, and mirror it in C2's scope:
*"DENY here means the operation's structured target is not a declared filesystem member of
that seat's target list. URI and device selectors — `xd://`, `agent://`, `local://`,
`proc://`, `skill://` — are outside this audit's domain and are recorded as 'not a declared
filesystem target', never as 'the adapter refused' or 'the harness forbids it'."* The policy
JSON's own reason text is the ideal place for the same qualifier, but that file is outside
this seat's write binding; the recommendation is addressed to whichever seat holds it.

### F4 — absence of captured events is not compliance

C2 consumes `--events`. A NO-EXEC seat — this one, with `commands: []` and `fetches: []` —
produces no captured events by construction. If the checker or a downstream report treats
"no events" as "no violation", or as "declared scope respected", self-attestation is promoted
to audit result. `limits[1]` excludes recorder-completeness, so the honest phrasing is
already available and needs to be used: *no captured event means no captured event*; for empty
command/fetch lists the status stays `declared, unverified`. This is also the one place where
an operator could mistake C2's `structured_edit_mode` before 0 → 1 for "seats are now
restricted". The metric name says "mode"; `limits[0]` says no such state exists. Paraphrase the
metric as "v2 audit classification available in the document contract", never as a runtime mode.

### F5 — C3 stays lane-local only as a labeling rule over frozen bytes

The reconciliation explains rough-vs-lane path counts (`build` 25→23, `falsify` 33→29) for the
two fixed r22 cohorts. The arithmetic anchor is exact and should be stated as such: the
explanations must sum to **2** and **4**, not to a plausible total; a residual is declared as
unknown, and then `target: 0` is not met rather than being rounded away.

Ownership is bounded by ADJ-07, whose retained column is "Census bug, domain contract,
implementation and repair in this repo" and whose handoff instruction is "ask for method
advice, not transfer of gate ownership or a general claim from one lane". So: a reconciliation
that says *"the census's classification rule maps these recorded path components differently"*
stays here; a reconciliation that says *"the wave routed N seats under the wrong cohort"* has
left the lane and entered ADJ-05/kumitate routing. The preregister's own framing supports the
former ("explains classifier/unit differences rather than rerunning closure merely to confirm
them"), and the round-12/round-13 refinements repeat the constraint "without absorbing sibling
verification methods".

Second-order check on the C3 command: it must read frozen r22 records. If
`check-path-reconciliation.py` recomputes the r22 census with current code, it is a retry of a
historic check, which the C3 scope and the outside-round22 scope both forbid. The record must
carry the frozen digests it reconciled, not merely point at r22 paths whose bytes can move.

### F6 — a failing checker is advisory evidence until L1 adopts it

`check-edit-contract.py`, `check-seat-bindings.py` and `check-path-reconciliation.py` exit
statuses are local verification evidence. L1 is the sole production/VCS integrator, so a
nonzero exit does not by itself block a landing, and no r23 prose should imply a pipeline gate
the lane does not own. Symmetrically, a zero exit must not be reported as an authorization.

### F7 — the v1/v2 homonym reads as a contradiction

C2 says "legacy schema-v1 policy and historical reds unchanged", while the artifact that
carries the eight decisions is `"schema": "tsukuroi-edit-policy-v1"` and is itself introduced
in r23 with `before: 0`. On a plain reading, C2 calls new C1 material "legacy". The consistent
reading is that C2's v1 refers to *binding/manifest* schema v1 while the policy file's v1 is a
different namespace — but nothing in the text distinguishes them. Suggested prose fix: always
qualify — "policy schema v1 (eight decisions)" versus "seat-binding schema v2 (audit targets)".
This is a naming risk, not a verdict change, and it is the cheapest way to protect C1/C2
separability, which the preregister states as a property ("C2 reads only explicit v2 authority
and captured events").

### F8 — sibling boundaries retained unresolved (no absorption, no ruling)

- ADJ-06: "protocol integrator — kaidoku/revenger ownership unresolved", and the Frontier
  repeats it: "Kaidoku and revenger both declare shipped-artifact RE. The integrator must
  arbitrate this shared scope; tsukuroi neither picks an owner nor absorbs it." r23 does not
  touch this; neither should any r23 report.
- R20-OUT009 narrows OUT-009 to Electron/JavaScript packages and keeps the original quote as
  historical evidence; ADJ-06's unresolved recipient stays controlling.
- Frontier: "Recipient acknowledgement and independently replayed handoffs are not verified."
  The 1/8 matching pin and 7/8 drift observation is dated 2026-10-19; the portable-anchor
  section states the pins are "stale by design once a sibling commits again". Any r23 sentence
  citing sibling authority should therefore use anchor ids OUT-001..OUT-010 with pinned blob
  digests, never the ADJ table's line-range form (`../kumitate-shokunin/PROVINCE.md:3-6`),
  because line ranges drift with the 7/8.
- OUT-010 keeps reusable method with tameshi while "each lane keeps its own gate". That is
  what makes C1/C2/C3 legitimate here at all: keeping the gate is endorsed, exporting the
  method is not this lane's act.

## Proposed move (one, bounded)

Adopt F3's sentence — domain clause plus verdict semantics — in the C1 record and C2 scope.
It improves C1 (cells become self-describing without changing the eight ids, verdicts or the
`target: 8` count) and C2 (audit authority stays metadata-only: it never resolves a URI and
never asserts an adapter outcome), and it leaves C3 untouched. It harms nothing: no verdict
changes, no preregister edit, no historical red cleared, no sibling ownership taken.

## Risks

- **Carve-out read as permission.** "Out of domain" could be taken as licence to ignore
  external-selector events. Mitigation: out-of-domain records are still *reported*, as selector
  shape plus the words "not a declared filesystem target", so the omission is visible rather
  than silent. A silent drop would be worse than the current over-broad DENY.
- **F7 unqualified.** If the v1/v2 homonym survives into the build prose, a reader can conclude
  the eight decisions are pre-existing, which contradicts `before: 0`.
- **F5 scope creep.** Cohort counts invite a causal sentence about the wave. Any causal claim
  about seat routing belongs to kumitate under ADJ-05/OUT-006, and any kill/pressure causation
  claim belongs to mori under ADJ-04/OUT-001.
- **F4's null result.** Vacuous C2 passes on event-less seats are the most likely way this
  round reports operability it did not observe.

## Verification (for main — this seat executed nothing)

1. C1: `python3 tools/check-edit-contract.py --revision <REV>` — expect 8 decisions, and no
   output line describing a repaired runtime behavior.
2. C2: `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`
   — expect v2 classification; confirm a seat with an empty event list is *not* scored
   compliant; confirm historical v1 reds are still red.
3. C3: `python3 tools/check-path-reconciliation.py --revision <REV>` — expect per-event and
   per-component explanation summing to exactly 2 (build) and 4 (falsify), frozen r22 digests
   cited in the record, and no recomputation of the historic census.
4. Wording sweep over built reports: `grep -nEi 'enforc|prevent|restrict|blocked|runtime mode'`
   in `.ufo/waves/round-23/build/*.md` should show only quoted limits, never a lane claim.
5. Receipt discipline: confirm every build report's trailer carries exactly the three receipt
   prefixes once, unfenced, and that no fourth field was promoted.

Reviewed-SHA256: a296da872e83731f7f7a7737662988558ebb97e4399681a1099fab4a259b7a79
Predicate: r23-connprovince23
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
