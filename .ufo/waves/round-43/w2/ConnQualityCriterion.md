VERDICT: draft

# Seat ConnQualityCriterion — item N-12: is a new QUALITY criterion warranted by a mistake mined this round?

Read (all absolute, read-only): `tsukuroi-shokunin/corpus/lessons/round-43.md` (Mistakes table, lines 91-100; Entry gate 36-62), `tsukuroi-shokunin/.ufo/waves/round-43/w1/C2MutBinding.md`, `w1/C1CritChannels.md`, `w1/ConnClaims.md`, `tsukuroi-shokunin/corpus/QUALITY.md` (criteria 76-91). Verified in-repo: the duplicated round-42 header rows at `SCORECARD.md:2630,2632`; the six Mistakes rows' IDs. No counter was run (read-only seat); all quotes are from the committed files.

## 1. Verdict: one new criterion is warranted — number 92, from R43-CAP-HEADER-DUP

Of the six Mistakes rows mined this round, exactly one has no capturing criterion: **R43-CAP-HEADER-DUP** has `Captured-by: none — no criterion reads a rendered table` (round-43.md:98). The round's own fix ("the round-43 table carries one header row", with an "able to fail" awk count printing 2 red / 1 green) is a machine-checkable document invariant of the same family QUALITY already governs (78: exactly one `SKILL.md` line with the exact bytes; 84: machine-grammar tokens echo only validated values). Since no existing criterion covers a rendered table's header integrity, a new numbered criterion is the right instrument (there is nothing to amend). Draft:

```
92. **A rendered table in a committed scorecard or report carries exactly one header row (R43-CAP-HEADER-DUP):** a table presented as machine-readable in a committed artifact (`SCORECARD.md` capabilities tables, gate/evidence tables in reports) has exactly one header row at its top, named by the same cell pattern; the heading-bounded count of header-pattern rows under the table's `##` heading prints 1, and any tool counting the table's body counts data rows only. Failing example: the round-42 capabilities table repeats its header — `SCORECARD.md:2630` and `:2632` both read `| Capability | What it can now do | Evidence pointer | First-working round |` — and the heading-bounded count `awk '/^## Capabilities — current full evidence set \(round 42\)/{f=1;next} /^## /{f=0} f&&/^\| Capability \|/{n++} END{print n+0}' SCORECARD.md` prints 2; after the fix the same count for round 43 prints 1. Lesson: `corpus/lessons/round-43.md` Mistakes R43-CAP-HEADER-DUP.
```

Evidence for the failing example, verified in the lane at the current tip: `SCORECARD.md:2628` heading `## Capabilities — current full evidence set (round 42)`; `:2630` and `:2632` both hold `| Capability | What it can now do | Evidence pointer | First-working round |` (the separator row `|---|---|---|---|` follows each). A count of the header pattern under that heading is 2, exactly the lesson's red case.

## 2. The other five rows are already captured — no further new criterion is warranted for them

| Mistake row | Captured by | Why no new criterion |
|---|---|---|
| R43-SIB-PIN-UNREPORTED | QUALITY 69 (`QUALITY.md:137`, "a sibling pointer is replayed by quote and pinned blob…") | The row's own `Captured-by` names 69; the obligation (report a moved sibling pin) is squarely inside it. |
| R43-MORI-ARITH | QUALITY 21 (`QUALITY.md:29`, "Portable locators… Supplemental reader line numbers require the renderer and source snapshot") | The defect is a line-number referent drifting from its revision; 21 states the rule (a reader line number needs its snapshot). The fix (one sentence per coordinate naming its starting revision) is exactly 21's remedy. |
| R43-CENSUS-PROBE-COORDS | QUALITY 21 (same row) | Same class: `R42-C1-CLASS-UNSWEPT`'s probe line numbers were true at `44766208` but not at `6951ead9`; 21 requires the snapshot/revision attached to reader line numbers. The round's fix (cite readers by content plus revision) implements it. |
| R43-L1-SCRATCH-STRAY | ROUND-PROMPT §7 (scratch discipline: one dir per seat, delete on exit) | The obligation (scratch hygiene) lives in the standing round prompt, not in QUALITY; the mistake is operational (files straying into shared roots and lane `__pycache__` hidden by `.gitignore`), not a claim/evidence-quality gap. A QUALITY criterion would duplicate governance without adding a new obligation. |
| R43-VERDICT-JSON-UNBOUND | QUALITY 90, with a precision gap → amendment, not a new number | The substantive rule — a verdict binding counts only a declared, anchored verdict line — is already QUALITY 90 (`QUALITY.md:177`). The row's `Captured-by` states the gap precisely: "QUALITY 90 named no accepted serialization". The round already closed the operational side (the round-43 counter binds JSON `verdict_line` or the first non-blank line, plus the report's first line; seat prompts name that one form). What remains is a text-level precision gap in 90, which the file's established convention handles by an appended correction note (precedent: the R31 corrections to 78/79 and the wave-2 correction to 80), not by a new number. Recommended appended clause for 90: "the declared serialization of the verdict line (a plain first line and/or a named JSON field, e.g. `verdict_line`) is named in the frozen rule, and the counter binds exactly the named form(s)". |

## 3. Wave-1 proposals that do NOT satisfy the lesson-row requirement

- `w1/ConnClaims.md` §4 proposed a criterion 92 ("A residual the counter itself measures or names is enforced…") with `Lesson: corpus/lessons/round-43.md (to be written by the round)`. The round's Mistakes table is now written, and **no row covers self-identified residuals** (mount table / uid_map / script path / forged orchestrator records): the six rows are SIB-PIN-UNREPORTED, MORI-ARITH, VERDICT-JSON-UNBOUND, CAP-HEADER-DUP, CENSUS-PROBE-COORDS, L1-SCRATCH-STRAY. Under the standing rule that each criterion cites a lesson row, that proposal cannot stand as grounded this round; if the integrator wants it, it needs its own Mistakes row (or a next-round flip) first.
- `w1/C2MutBinding.md` defects H/I/K (whitespace-stripped binding, blank-line-skipped report check, duplicate JSON keys) and `w1/C1CritChannels.md` channel findings are seat findings, not lesson rows; likewise they cannot ground a criterion under the citation rule.

## 4. What I did not do

No counter, selftest or control was run; no lane file was modified; no scratch/fixture was created. All evidence is from committed-file reads (`round-43.md`, `QUALITY.md`, `SCORECARD.md`, `w1/*` reports). The proposed criterion text above is exact and ready for the L1 to number and integrate.
