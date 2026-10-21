# CritNoHarm — round22 critic report

Seat: CritNoHarm (critic, leaf). Task: test the unsupported no-harm claim, and the claim that complete evidence makes a receipt correct.

## Inputs actually read

| Input | Read? | Note |
|---|---|---|
| `.ufo/waves/round-22/snapshot/corpus/QUALITY.md` | yes | primary target; criteria 1–46 |
| `.ufo/waves/round-22/preregister.json` | yes | claims C1–C3, `C3_bound`, `host_decision`, `ordinal_deltas`, `limits` |
| `.ufo/waves/round-22/sources/host-tool-boundary.json` | yes | `native_per_seat_allowlist: false`, `authority`, `approved_scope` |
| `skill://godspeed` | **no** | This seat's tools can read only local file paths. Resolving the internal URL would mean guessing a filesystem path outside the declared bindings, so I did not open it. The godspeed axis rules are taken from the assignment text only. |

Tool calls this seat made: three file reads (the paths above) and one write (this file). It made no shell, eval, subprocess, fetch, or child-task calls, and installed nothing. Under QUALITY42/46, this disclosure and the trailer below are **declarations**. They do not prove what this seat did.

I did not compute the SHA-256 of the reviewed file, because NO-EXEC forbids it. The `Reviewed-SHA256` trailer value is copied from the assignment. It is not a digest I measured. [unknown] Whether the bytes I read match 7f2bd224…e14d.

## Findings

### F1 — The no-harm claim is stated but never measured (severity: high)

- **Counterexample.** `preregister.json` sets `"ordinal_deltas":0` and lists ordinals for all six axes, but only three of them have a command: depth, operability, and calibration (C1–C3). Adjacency, coverage, and freshness have no before or after measurement. So a round22 landing that regresses coverage would still match this preregistration. Concrete case: the `limits` entry "No replacement seats" plus C3's `absent-dead` class let a seat drop out of coverage while every C1–C3 target still turns green.
- **Evidence.** In `preregister.json`, the `claims[]` list has three entries, and only those carry a `command`. `ordinals` covers six axes, and `ordinal_deltas` is a bare number with no derivation. QUALITY1 says every claim must be falsifiable or marked as opinion, and QUALITY9 says a negative claim (here, "no harm") needs a bounded sweep command, scope, and date.
- **Axes affected.** Calibration (the claim exceeds its evidence), plus every axis without a command (adjacency, coverage, freshness).
- **Smallest safe fix.** Either preregister one no-regression probe per non-target axis, for example re-running the round21 gates at the candidate revision and comparing against baseline `894d1e2`, or state in `limits`: "no-harm on adjacency/coverage/freshness is unmeasured". Do not record `ordinal_deltas:0` as a no-harm finding. **Classification:** fixable defect. If neither change lands, the judge must refuse any no-harm assertion.

### F2 — C3 "accounting complete" can be green while every receipt is wrong (severity: high)

- **Counterexample.** The C3 metric `cohort_accounting_mode` goes from 0 to 1, a single binary flag. Consider a settlement that puts every declared seat in `absent-unresolved` or `delivered-faulty`. The accounting is complete, so the mode is 1 and C3 hits its target, yet zero receipts conform. The `C3_bound` prose correctly says this is "not an every-receipt-conforms claim", but neither the metric nor the target encodes that distinction. A reader of the C3 result would see "1/1" with no way to tell full accounting from a cohort that is all faulty.
- **Evidence.** In `preregister.json`, the C3 entry has `"before":0,"target":1`, and `C3_bound` lists four classes. QUALITY44 says dead or malformed evidence stays visible and non-clean. QUALITY42 says "A receipt is a declaration, not proof of actual reading or command nonexecution."
- **Axes affected.** Calibration (complete accounting reads as correct receipts) and coverage.
- **Smallest safe fix.** Have C3 always emit the four class counts plus the strict receipt-finding count alongside the mode flag. The judge then grades accounting completeness (all seats classified) and receipt correctness (`delivered-conformant` count against declared seats) as two separate propositions. Neither may be reported as the other.

### F3 — Two authorities judge seat conformance: C3 `delivered-conformant` ignores the C2 request audit (severity: high)

- **Counterexample.** The C3 command (`check-review-cohort.py --manifest reviews.json --settlement settlement.json`) takes no `--events` input. Only C2 (`check-seat-bindings.py ... --events events.json`) sees request events. Suppose a seat delivers a well-formed receipt containing the scope trailer, but C2's events show a shell or eval call. C3 can still class it `delivered-conformant` while C2 reports a binding violation. That is exactly the contradiction QUALITY46 forbids: a literal no-execution declaration "never overrides an observed Bash/eval/child invocation".
- **Evidence.** The `command` strings for C2 and C3 in `preregister.json`, and QUALITY46. QUALITY31 also makes `tools/check-seat-scope.py` the green-wave gate for the same seat-scope proposition. That gives three gates — `check-seat-scope`, `check-seat-bindings` and `check-review-cohort` — with no stated order of precedence.
- **Axes affected.** Calibration and operability (gates can disagree with no tie-break), and depth (the boundary decisions in C1 are undermined if seat verdicts conflict).
- **Smallest safe fix.** Two parts. First, the C3 class `delivered-conformant` must require a clean per-seat C2 audit result, consumed by digest or file path. Otherwise rename the class to `delivered-receipt-wellformed`. Second, record one precedence rule: an observed violation from any gate overrides a declaration-only pass. **Classification:** fixable defect.

### F4 — The C2 audit can be "clean" because its events are incomplete (severity: medium-high)

- **Counterexample.** C2 reads the requests recorded in `events.json`. If a seat's transcript is missing, cut short by provider death, or unexported, there are no events for it. A fail-open reading of that is "no violations". QUALITY46 says provider death and an absent final message "do not establish absence of earlier tool use". The preregistration does not say how complete each seat's events must be, or which source produces them.
- **Evidence.** In `preregister.json`, C2's metric `request_audit_mode` goes from 0 to 1, again a binary mode with no per-seat coverage count. `approved_scope` claims a "fail-closed post-hoc audit", but nothing defines what fails closed when events are missing.
- **Axes affected.** Operability and calibration.
- **Smallest safe fix.** Have `check-seat-bindings.py` emit `CANNOT_EVALUATE` for every seat that is in `bindings.json` but has no complete event stream, and report `seats_with_events / seats_declared` next to the mode. A seat with no events is never counted clean.

### F5 — The host-boundary authority is an oral message, not an anchored source (severity: medium)

- **Counterexample.** The `host-tool-boundary.json` field `authority` reads "Main message to TsukuroiR22: Confirmed: …". It has no message ID, transcript path or line, or capture digest. The `task_fields` schema has no capture locator either: no tool-schema dump, digest, or revision. New source S084 ("current exposed task tool schema and Main host decision") therefore rests on a message that later readers cannot re-resolve. Also, Main is both the round's planner and the one who approved this boundary, so the approval is not independent.
- **Evidence.** QUALITY2 ("never oral knowledge"), QUALITY21 (portable locators: heading or fragment, exact quote, revision), and QUALITY35 ("a quoted 'Owns' declaration is not an integrator ownership award").
- **Axes affected.** Freshness and calibration.
- **Smallest safe fix.** Persist the exact Main message, with its ID, timestamp and SHA-256, and the captured `task` tool schema bytes as files under `.ufo/waves/round-22/sources/`. Cite those files from S084. Keep the "prompt-level, not runtime enforcement" limit unchanged; that wording is correct.

### F6 — The receipt instruction contradicts itself (three lines vs four) (severity: medium)

- **Counterexample.** This seat's assignment says the report "must end with these three physical lines". It then lists **four**: Reviewed-SHA256, Predicate, Scope, and the "Lane bounds" line. A strict trailer gate that checks for exactly three trailing lines would mark a fully compliant report `TRAILER-MALFORMED`. A gate checking for four would mark a report that obeyed "three" as malformed. Either way, receipt "correctness" depends on which instruction the gate encodes, not on what the seat did. This is a live R21-TRAILER20-class hazard (QUALITY44).
- **Evidence.** The assignment text (`# Required receipt` section) and QUALITY44.
- **Axes affected.** Calibration and operability.
- **Smallest safe fix.** Restate the instruction and the gate as one literal block with an explicit line count of four. Until then, grade reports by the delivered block as-is, and record the miscount as a dispatch-template defect, not a seat fault. This report ends with all four listed lines verbatim.

### F7 — A digest in the receipt does not show the bytes were reviewed (severity: medium, by design)

- **Counterexample.** Under NO-EXEC, no seat can hash its input, so every round22 `Reviewed-SHA256` value is copied from the prompt. A report with a correct digest field proves only that the prompt was copied correctly. If the target file changed between snapshot and read, the receipt would still "match".
- **Evidence.** QUALITY38 and QUALITY42, and NO-EXEC in the seat contract.
- **Axes affected.** Calibration.
- **Smallest safe fix.** L1 records the target's SHA-256 at dispatch, as QUALITY42 already requires, and separately at settlement time. C3 treats "receipt digest equals dispatch digest" as a declaration-consistency check and never as evidence that the bytes were read. Say this explicitly in the C3 output schema. **Classification:** a tradeoff accepted under NO-EXEC, provided it is labelled.

## Separating fixable defects from tradeoffs the judge must reject

- **Fixable before integration:** F1, F2, F3, F4, F5, F6. Each needs only a preregistration or schema change, plus a gate input or output field.
- **Tradeoffs the canonical judge must reject as stated:**
  - Any round22 result that says "no harm" or "no ordinal regression" without the F1 probes.
  - Any C3 result where `delivered-conformant` is not tied to the C2 audit (F3).
- **Accepted tradeoff, if labelled:** F7.

## Observation / inference / unknown

- **Observed** (from the files read): the three-command claim set; the binary C2 and C3 metrics; C3 has no events input; the authority is a message quote; the receipt-count mismatch.
- **Inferred:** the scenarios in F2, F3 and F4 follow from the stated command interfaces. I did not read the `tools/check-*.py` sources, because they are outside this seat's read binding.
- **Unknown:**
  - The actual logic of `check-review-cohort.py` and `check-seat-bindings.py`. They may already cover F2–F4 internally. Not checked: outside the binding.
  - Whether the reviewed bytes match the stated digest.
  - The contents of `skill://godspeed`.

Reviewed-SHA256: 7f2bd22429b53446939e56bcfdfb188126fe711e5cc72ef957e2a0140206e14d
Predicate: r22-critnoharm
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
