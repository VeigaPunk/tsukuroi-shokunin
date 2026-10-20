# GateContractReview — round 14: Gate standard vs r13 checker

Baseline 8606bad4cbc6451ac2890c9f8e2548a36c386db6. Static reads only; nothing executed.
[code-read] = inferred from source. Revision outcomes are quoted from the r13 lesson, not re-measured.
Read: PROTOCOL.md:375-423; SKILL.md:1705-1740; tools/check-root-dac-correction.py; root-dac-correction-r13.{md,json}; lesson:108-153, 233-258.

## Findings (severity order)

**H1 — Checker cannot see the live r13 defect (high).** MD:97 says strict "is the only value that covers
the hierarchy (S041); the value set is not exhaustive". Documented domain: boolean argument or full/strict (S044).
Predicates are whole-document presence tests: `nonexhaustive` (checker:112) is satisfied by MD:31
"illustrative and non-exhaustive". `active-exclusive` (OLD :28-30) needs "only strict … would make", absent
from MD:97. JSON `protect_system_values` (32-61) is never read. Revision run passes (lesson:123).

**H2 — Crashes exit 1, which reads as "failed" (high).** PROTOCOL: 1 = failed. `main` traps only `Cannot`
(:358-370). [code-read] git absent → FileNotFoundError from unguarded `subprocess.run` (:229); a top-level
JSON array in r12/r13 → AttributeError at `.get` (`json_sites`, `json12_issues`, `json13_issues`); non-list
`branches` or non-dict `corrected_universal` → TypeError/AttributeError. All exit 1. argparse usage exits 2
with no CHECK line; the registry row does not declare "usage" (census row does, SKILL:1709).

**H3 — Selftest expectations are not independent (high).**
- Expected IDs are literals (:302-323) compared as subset (`want - got`, :333): extra findings never fail.
- PASS fixture `corrected` (:306) is built from constants (:256-290) that contain the predicate tokens. It proves
  self-consistency, not truth.
- MD-side predicates killed by 0 mutants (headings, mechanisms, scope, nonexhaustive, strict, namespace, source,
  MD active-exclusive, MD overclaim). Only `table-broken` (:324) touches MD13.
- Lesson:118-121: first red (`closed-list-restored: missing=R13-JSON-PIN`) was fixed by editing that expected set
  after seeing output. The retained red is honest; the edit is expectation-tuning PROTOCOL forbids.

**H4 — `correction_count` is a function of exit code (medium-high).** `1 if code == PASS else 0` (:210), printed
at :213. The lesson's "bounded 0→1 counter" (lesson:83) cannot differ from the verdict; only the plain-Python
count (lesson:79-81) is a measurement.

**M5 — Revision run does not pin the gate that produced it (medium).** `repo = Path(__file__)…` (:357): `--revision R`
runs worktree checker bytes over R inputs. Verdict echoes commit (:365) but no gate digest, no input blob
digests. Tree mode prints only `source=tree`. Lesson:114-116 does not say which gate bytes made the 44677cc run.

**M6 — Registry row misses PROTOCOL schema (medium).** SKILL:1737 "Pinned values: … inside tools/…py" is a
description, not a pinned-value path. Entry uses `python` (shebang python3; minor). States no non-verified scope.

**M7 — gate_contract declares more than the checker consumes (medium).** JSON 210-221: 10 headings vs checker 5
(:100-104). JSON 222-236: 13 scan fields vs ~9 derived (:151-152); omits root_view_not_intrinsically_read_only,
api_scope, unknowns.captured_property_set. JSON 242 rule needs markers at historical_revision 70fede2; checker never
reads it. History check (:167-170) tests 3 presences vs 8 markers (JSON 193-202).

**M8 — Table widths unenforced (low-medium).** `tables` (:116) counts only 5-pipe delimiters. MD:96 is 3-column and
unchecked, despite QUALITY item 10's "checked at integration".

**M9 — Missing-input rule inconsistent (low).** Missing r12 → CANNOT (:161); missing r13 → FAIL (:181-188).

**L10 — Metadata drift (low, route to erratum).** JSON sources[0] S041 `status: reserved`, `registry_owner:
SourceRegistry` (267-268); lesson:250-252 says mined.

## Recommendations

1. **Registry row (new).** `source-scope-correction`; gate; `python3 tools/check-source-scope-correction.py [--revision REV]`;
   0 clean / 1 failed (closed ID vocabulary) / 2 could-not-evaluate (usage, missing/unparseable/digest-mismatched input,
   invalid revision, trapped exception); self-test `--selftest` (0 exact-match, 1 otherwise); pinned values
   `tools/fixtures/source-scope-correction-r14.expected.json` + committed fixtures; write scope none; owner tsukuroi.
   Scope: "bounded conformance — schema, two IDs, pointers, quotes ≤25 words verbatim in pinned snapshot, lexical
   rules. Not source truth, not live URLs."
2. **Exit mapping.** Catch-all in `main` → CANNOT, return 2. argparse error → 2, declared "usage". Shape-check every
   JSON node before access. Trap git absence. Selftest asserts exit 2 for malformed JSON, non-object root, missing
   git (injected), usage error.
3. **Independent expected IDs.** Before implementing, commit a table: per mutant — fixture, owning predicate ID,
   expected exit, exact ID set. Assert `got == want`. Fixtures must not reuse predicate tokens. Add mutants: each
   heading removed; document-wide "only `strict` would make" inserted; "value set is not exhaustive" near the
   ProtectSystem sentence; corrections count 1 and 3; quote >25 words; quote absent from snapshot; self-description
   without basis quote. Any later expected-set change needs a LOG line naming the owning predicate.
4. **R14-VALUE-DOMAIN-EXHAUSTIVE (proposed).** Localize to the sentence/row. Flag "ProtectSystem" + "exhaustive" when the
   subject is the value set or domain, unless it says "mechanism(s)". Require JSON `protect_system_values` to equal
   the pinned domain {boolean argument, full, strict} from the S044 snapshot.
5. **R14-ATTRIBUTION-UNSUPPORTED (proposed).** A row claiming "self-described", "model-generated" or "automated triage"
   must carry a `basis_quote` verbatim in the pinned snapshot for that exact comment URL. No snapshot → CANNOT.
6. **Revision measurement.** (a) `--revision R` evaluates gate bytes at R (copy `git show R:tools/…` to temp), or
   records the running sha256 and requires it to equal `git show R:…` recorded in the expected file. (b) Per input:
   40-hex commit + blob sha256 vs pinned digests; mismatch → CANNOT. (c) Tree mode prints `HEAD=` and `dirty=`; dirty
   is not citable. (d) Red-before at e1fc8fd1992dfdefc81c4e9f07aee897b4275ea0: exit 1, exact R14 IDs; fixed revision
   exit 0; both pinned with digests. (e) Remove `correction_count` or derive from parsed corrections.
7. **Contract reconciliation.** Trim gate_contract to the enforced subset and label the rest "reviewer checklist, not
   gate-enforced", or implement it. The row states which. A passing counter must not imply full enforcement.
8. **Missing-input rule.** Declare: absent required input → CANNOT; absent expected correction → FAIL. Apply uniformly.

## Residual risk and gaps
- Nothing executed; H2 and H1/H3 analysis are [code-read]. Live S044/S045 text not re-opened by this seat.
- 44677cc and c35d356 measurements quoted, not re-run. LOG.md and SCORECARD.md not reviewed.

## Tooling
Installed or updated: **none**. Read-only file reads, `git log -8`, `git status --porcelain`. No checker, selftest,
census, or package transaction run.
