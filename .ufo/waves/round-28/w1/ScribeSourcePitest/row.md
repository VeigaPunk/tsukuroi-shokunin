# S147 draft — pitest "Basic concepts" (round 28, wave 1, seat ScribeSourcePitest)

Fetch receipt: `https://pitest.org/quickstart/basic_concepts/`, ordinary `curl -sS -L`
(no challenge, no auth), saved to
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/w1/ScribeSourcePitest/S147.html`,
12155 bytes, sha256 `c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a`,
fetched 2026-10-22 (clock read `2026-10-22T19:02:04Z` immediately after the fetch). The page
carries no version, date or commit marker; its only provenance hook is the "Improve this
page" link to `github.com/hcoles/pitest-site/edit/gh-pages/quickstart/basic_concepts.markdown`
(S147.html:71), which is an edit URL, not a pin.

## Decision

Mined, at one narrow scope: PIT's own classification of the outcome of an executed mutant,
plus the existence of equivalent mutations. Not adopted: the page's mutation-operator,
coverage-analysis and test-selection content, and all JVM-specific mechanics. That second
part is an explicit **defer** with its reason and flip condition, recorded below for the
round-28 Gate.

## Row (registry shape, `corpus/SOURCES.md`)

`| S147 | PIT Basic Concepts — https://pitest.org/quickstart/basic_concepts/ | docs | A | PIT's own reported outcome classes for an executed mutant (killed, survived, no coverage, non viable, timed out, memory error, run error) and the existence of equivalent mutations, as the classification vocabulary for a mutation battery's refusal count; not a general theory of mutation testing, not this lane's method, and not the bytecode mutation-operator or coverage-driven test-selection content | § Equivalent Mutations and § Running the tests outcome list; S147.html:120-152 and :163-196; page fetched 2026-10-22, naive HTML sha256 c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a, 12155 bytes, no version or date marker on the page | A kill is a detection ("a test caught the mutation successfully", :175), while a non viable mutant ("could not be loaded by the JVM as the bytecode was in some way invalid", :184) and a run error ("something went wrong when trying to test the mutation", :192) are separate classes that are not evidence of detection, and "no coverage" is ranked with survived (:179); some mutations cannot be detected at all because "the resulting mutant behaves in exactly the same way as the original" (:122-128) or differs "outside the scope of testing" (:146) | mined | 2026-10-22 | 90d | — |` 

Landing condition, stated so the L1 can land it mechanically: set `used-by` to
`corpus/lessons/round-28.md` and keep `mined` only if that lesson (or the round-28 C1 report)
cites S147 as the rule for classifying a battery refusal. If it does not, change the row's
status to `queued` and its `used-by` to `—` in the same commit; the teaching stays available
and uncounted, exactly as S039/S040 were queued before a note cited them.

## What the page teaches that a general definition does not

1. [obs] A mutant's outcome is a class, not a boolean. The page lists seven outcomes
   (S147.html:163-172, list items :166-172) and defines them separately: killed = caught by a test (:175);
   survived = not detected (:177); no coverage = same as survived with no test exercising the
   line (:179); non viable = could not be loaded (:184); run error = failure in the attempt to
   test the mutation (:192). The closing sentence says "Under normal circumstances you should
   see no non viable mutations or run errors." (:196), which states that these classes are
   abnormal harness states, not findings about the code.
2. [obs] Equivalence is a property the harness cannot fix. "not all mutations will behave
   differently than the unmutated class. These mutants are referred to as equivalent
   mutations." (:122-123), with the two listed reasons: identical behaviour (:128) and
   behaviour that differs only "outside the scope of testing" (:146). The page gives no
   detector for this; it is a screen to apply before counting.
3. [obs] The page's own mechanism is bytecode operators plus line coverage plus per-test
   selection (:76-109, :154-161). That mechanism needs Java debug info (:102-109) and a JVM
   (:184), and does not describe a gate that reads data.

## Why this lane's batteries need 1 and 2, concretely

The round-28 C1 claim is "0 of 24 accepted" with `control_live_anchored_rows` 6, where
"accepted" is exit 0 with the full count in any run of the mutant. The lane's battery counts
exactly that:

- `tools/mutants-adjacency-overlap.py:121` (at `f8e3a8f`) sets
  `accepted = any(exit == 0 and anchored_rows == 6)`; a run that crashes, or exits 2
  `CANNOT_EVALUATE`, is therefore counted as *not accepted*, i.e. silently credited to the
  gate's refusal power. The same file records per run `exit`, `anchored_rows`, `finding` and
  `stderr_tail` (:113-119) and prints only `should_fail_accepted` in the summary (:394), so
  the evidence to separate the classes exists and the summary does not use it.
- The counter itself already has the three-way split the page names:
  `tools/check-adjacency-overlap.py:107-119` returns exit 2 `CANNOT_EVALUATE` for
  revision-invalid, register-missing and register-unreadable, exit 1 with per-row findings for
  a refusal, and exit 0 PASS. Exit 2 is the page's non-viable/run-error analogue; exit 1 is
  the killed analogue. [obs] (read from the exported tree at `f8e3a8f`)

So two rules follow for the round-28 counter batteries, and they can only tighten the count:

- R1, from pitest's class separation: in the C1 report a should-fail mutant counts as refused
  only when its run produced the counter's own structured refusal (exit 1 with the JSON
  carrying the failing row identities). A run with exit 2 `CANNOT_EVALUATE`, or with no JSON
  at all (a traceback, which the page classes as non viable/run error), is reported in its own
  class and never folded into the refusal count. This does not change what "accepted" means; it
  stops a broken harness from being read as a kill.
- R2, from equivalent mutations: before "0 of N accepted" is declared achievable, each
  should-fail shape must be shown to change the effective input the counter parses. A shape
  that leaves that input unchanged (a field the counter never reads, or a formatting-only
  edit the parser normalises) is equivalent with respect to this gate and cannot be refused by
  any correct counter; it must be named and removed from the denominator with that reason, not
  counted as a counter failure. Without this screen, a 0 is only meaningful if every shape is
  non-equivalent, and an accidental 0 is indistinguishable from a real one. [inf] The transfer
  of the class names from code mutants to data mutants is this lane's inference; the page
  speaks only of Java classes and bytecode.
- R3 (corollary, [inf], not taught by the page): "no coverage is the same as Survived"
  (:179) read for a refusal battery means a refusal produced by a rule other than the one the
  mutant targets does not show that the targeted rule fires. The report should name the
  finding per mutant, which the battery already records (:113-119).

## Explicit defer, for the round-28 Gate (routed defect 1)

Deferred: the page's mutation-operator set, the debug-info requirement, the line-coverage
analysis and per-test selection, and the JVM non-viable/memory-error mechanics
(S147.html:76-109, :154-161, :184-190).

Reason: this lane's round-28 mutants are edits to the register and entry JSON that a Python
counter reads. There is no bytecode to mutate, no instrumented line coverage, no per-test
selection to exploit and no JVM, so the page's central mechanism has no operand here; adopting
it would be a second convention on ground where the lane's own battery already defines the
run. The transferable part is the outcome classification only (above), and even that is
adopted as a counting rule for data mutants, not as a claim about PIT.

Flip condition: the lane lands a code-mutation battery that mutates its own checker source
(not the data the checker reads), for example a Python-level mutant run of
`tools/check-adjacency-overlap.py` itself. At that point the operator, coverage and viability
classes become operative and this defer flips to a mined row at that wider scope.

## Adjacency boundary

[obs] `PROVINCE.md:130` (OUT-010, `tameshi-shokunin/PROVINCE.md` @ `01d586ddbc5f`) records that
tameshi owns "the reusable verification/mutation-testing method, applied to fleet gates". S147
therefore must not be cited as this lane's mutation-testing method, recipe or kill-rate
standard; it is cited only for the outcome vocabulary that names a class the lane's own
battery already produces. The lane's existing method precedent stays
`corpus/knowledge/memory-arm-mutants-s8.md` §3 (tameshi `mutate-and-run.sh` recipe), untouched.

## Limits

- [unk] The page is unversioned and undated; the saved bytes are a fetch-time snapshot only,
  and a later edit cannot be excluded. `recheck: 90d` is proposed for that reason, not
  `on-release`: no release page is referenced.
- [unk] Whether any of the round-28 C1 24 shapes is equivalent in the R2 sense was not
  measured by this seat; that is a battery/report question, and this row only supplies the
  screen.
- [inf] Tier A is proposed because the page is the primary documentation of the tool that
  defines these class names. If the registry prefers a lower tier for a living, unversioned
  doc site, tier B does not change the row's scope or its teaching.
- [obs] Id S147 is provisional: the registry at `f8e3a8f` ends at S145 (`corpus/SOURCES.md:151`)
  and S146 was not present when this row was drafted; if another seat takes S146 or S147, the
  L1 must renumber this row and change no other cell.
