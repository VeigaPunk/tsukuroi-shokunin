# FxC3ReportDigest — round 22 falsifier (source-only)

Target: `.ufo/waves/round-22/candidate/tools/check-review-cohort.py` (assigned SHA-256 below; not independently re-hashed — NO-EXEC).
Attack: appending bytes after settlement changes the measured report digest; this is not chronology assurance.

## Verdict

The attack **holds in both halves**, and there is a concrete, source-visible consequence that goes beyond "the digest changes":

1. The digest does change. `report_sha256` is `hashlib.sha256(report).hexdigest()` over the full bytes returned by `read_bytes(review['report'])` (lines 56, 65). Any appended byte changes it.
2. It is not chronology assurance. Nothing in the input can express "before or after settlement":
   - the settlement schema (`tsukuroi-review-settlement-v1`, lines 38–49) accepts only `name`, `agent`, `outcome`, `error`. It has no settled report digest, no timestamp, and no commit reference;
   - the manifest, the settlement and every report are read from the **same** tree, `binding.sha` (line 153). `_revision.bind` proves only that the commit is an ancestor of `refs/heads/<branch>` (and of origin when present). It says nothing about when a report path last changed relative to the settlement file;
   - `report_sha256` is emitted but never compared to anything. It is an unanchored observation of the report as it exists at the evaluated revision.
3. **Counterexample with a real effect (fixable defect):** an append made after settlement can turn `delivered_faulty` into `delivered_conformant`, and `strict_conformance` from FAIL into PASS, with no finding. The seat's settled `outcome: failed` is left as it was. The tool cannot see this repair of a historical receipt, even though `seat-boundary-r22.md` checklist item 4 says "Never ... repair historical report lines". The same reasoning, extended to a report created rather than appended, clears `COHORT-UNRESOLVED`.

Bounded reason the digest itself is internally sound: at a fixed `binding.sha`, every `git show <sha>:<path>` read returns the same content-addressed blob. So `report_sha256`, the per-seat strict verdict (line 57) and the aggregate strict verdict (line 33) all cover identical bytes, and there is no read-time race within one run. The weakness is that the bytes are anchored to the evaluated revision, not to settlement.

## Counterexample fixtures

Expected verdicts below come only from reading the source. **Observed runtime: none. Nothing was executed, imported or mutated.**

All fixtures reuse the selftest base: source `b'fixed source\n'`, `sha = sha256(source)`, manifest row `{'name':'A','source':'s','report':'r','sha256':sha,'predicate':'p'}`. `R` is the clean report bytes, shown indented so they are not declarations:

    Reviewed-SHA256: <sha>
    Predicate: p
    Scope: executed=none

### F1 — harmless append after settlement (digest drifts, verdict does not)
- Settlement: `A / agent-A / completed / ''`.
- Revision C1: `r = R`. Revision C2: `r = R + b'\nAddendum written after settlement.\n'`.
- Expected at C1: exit 0, `PASS`, `delivered_conformant=1`, `strict_receipt_exit=0`, `report_sha256 = sha256(R)`, `findings=[]`.
- Expected at C2: exit 0, `PASS`, `delivered_conformant=1`, `strict_receipt_exit=0`, `report_sha256 = sha256(R + addendum) ≠ sha256(R)`, `findings=[]`.
- Why: the appended physical lines start with none of the three receipt prefixes (lines 108–118 of `check-review-snapshots.py`). Each prefix still appears exactly once.
- Effect: two PASS results with different digests. Nothing marks either one as the settlement-time bytes.

### F2 — append that repairs the receipt after settlement (category flips, no finding)
- Settlement: `A / agent-A / failed / 'observed provider failure'`.
- Revision C1: `r = b'partial'`. This is the selftest `partial-failed` case.
- Revision C2: `r = b'partial\n' + R`.
- Expected at C1: exit 0, `delivered_faulty=1`, `strict_receipt_exit=1`, `strict_conformance=FAIL`, `findings=[]`. Cohort exit is 0 because `delivered_faulty` adds no cohort finding (line 70).
- Expected at C2: exit 0, `delivered_conformant=1`, `strict_receipt_exit=0`, `strict_conformance=PASS`, `findings=[]`. The seat row still shows `outcome: failed`.
- Why: physical lines become `['partial', 'Reviewed-SHA256: <sha>', 'Predicate: p', 'Scope: executed=none', '']`. Each prefix list equals its one required line exactly. No code relates `outcome == 'failed'` to the category, and no settled digest exists to compare against.
- Effect: the calibration counts at C2 are not the settlement-time counts, and the strict receipt fault on record disappears at the later revision without any trace.

### F3 — appended file instead of appended bytes (adjacent; clears the only cohort finding)
- Settlement: `A / agent-A / completed / ''`.
- Revision C1: no `r` (blob absent). Revision C2: `r = R`.
- Expected at C1: exit 1, `absent_unresolved=1`, finding `COHORT-UNRESOLVED`.
- Expected at C2: exit 0, `PASS`, `delivered_conformant=1`, `findings=[]`.
- The same path applies to `absent_dead` (`failed` with no report) at C1, which becomes `delivered_conformant` at C2.

### F4 — control: an append that is detected
- `r = R + b'Reviewed-SHA256: <sha>\n'` gives `delivered_faulty`, `strict_receipt_exit=1`. This matches the selftest `duplicate-receipt` case.
- Detection happens only because the appended bytes add a receipt-prefixed physical line. It reveals that the report changed, not when it changed.

## Impacted axes
- **calibration (C3), primary.** `cohort_accounting_mode=1` and the four counts describe the evaluated revision, not settlement. F2 shows a post-settlement append raising `delivered_conformant` and lowering `delivered_faulty`. F3 shows `absent_unresolved` cleared.
- **operability, secondary.** `report_sha256` reads like preserved settlement evidence, which checklist item 3 asks for ("After settlement, preserve raw report bytes"). It is only a measurement at the chosen revision.
- **Disclosure gap.** The strict tool's scope says "not proof of reading, chronology or command nonexecution". The cohort `SCOPE` (line 19) leaves out **chronology**. Its output adds a digest field that invites a chronology reading.
- No identity change and no duplicate authority: the strict evaluator stays the only receipt authority, used through `strict.evaluate`.

## Fixable defect versus tradeoff
- **Tradeoff the judge may accept:** at a fixed revision, a measured digest with no time anchor is acceptable if it is disclosed honestly. Preregister C3 claims "detection and evidence", not an ordering between settlement and report bytes.
- **Fixable defect:** the cohort `SCOPE` does not disclaim chronology. `report_sha256` is not labelled as measured at the revision. A post-settlement receipt repair (F2) passes silently.

## Smallest safe correction
1. **Minimal, wording only. Must be done.** Add chronology to the cohort `SCOPE` (for example, "...not request-scope conformity, reading, chronology, no-harm or native enforcement; report_sha256 is measured at the evaluated revision"). This makes the stated scope match what the tool actually does, at no cost to any axis.
2. **Optional, strengthens calibration.** Add a required `report_sha256` field to each settlement row, nullable when no report existed at settlement. When the measured digest differs from it, or when null is not matched by an absent blob, emit `COHORT-REPORT-DRIFT`. Add fixtures F1, F2 and F3 as negative cases. Even then, this only checks byte consistency between the settlement record and the reports. It gives no ordering unless the settlement commit itself is shown to precede later edits, so the chronology disclaimer from step 1 must remain.

## Seat compliance
Read only the declared paths. `skill://godspeed` was not read, because the godspeed text was already inline in the assignment. Wrote only this report. No commands, fetches, installs, delegation, tests or mutations.

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3reportdigest
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
