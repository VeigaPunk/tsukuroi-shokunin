VERDICT: defect-found

Scope: framing of round 51 (claims C1/C2/C3, the counted-cohort bar, and the trend sentences). Read at FREEZE `2732ee6c06108c031c4d8043239b994e0504eb2f` only (`git show`, `git ls-tree`, `git cat-file`, `git diff`). Not run: any counter, selftest, census or battery; the K-pass and K-control results below are read from the committed battery source and from the working-tree receipt `controls/battery-summary-r51-freeze-c1.jsonl`, which is not committed at FREEZE (`git ls-tree` lists only `battery.py` under `controls/`). Counter hashes at FREEZE match `frozen/FROZEN-hashes.txt` for all five counters and `battery.py`.

## Summary

The round's three claims are measured on counters whose targets are not the thing the claims name. Three defects an outside reader will find first:

1. **C1 PASS would be a count of well-formed assertions.** The counter never checks a verdict against its cited line, and the round's own battery contains a templated all-`holds` cohort that reaches the target predicate.
2. **C1 FAIL is built in by the bar.** One `partly` from any of six seats blocks a row, and a negative needs no evidence while a positive needs two resolving citations. Four rounds in a row already failed this way.
3. **C2 and C3 do not measure a lane change.** The three r51 counters do not exist at base; their "before" receipts run the new counters over base bytes and already read PASS on the target predicates. The census, PROVINCE.md and the registry are unchanged, so "operability" and "adjacency" as axis labels overstate what moved.

## 1. C1 PASS would be an assertion count (FROZEN.md:15; check-scrub-admission-r51.py:237-249, 362-371)

- A bound `holds` is credited when the body is at least 300 bytes, cites at least two distinct row-source files at lines that exist in a pinned snapshot, and has a normalised body hash distinct from its siblings (`check-scrub-admission-r51.py:237-249`, credit path `:360-368`). Nothing compares the verdict to the cited line.
- The K-pass body is a fixed template: `Clause check for {row} by {seat}: the cited lines {c1} and {c2} decide the statement … This body is distinct for {seat}.` plus twelve repeats, where `c1, c2` are the entry's own cited lines (`battery.py:24-25`, body template `:62-64`). Its receipt is `controls/battery-summary-r51-freeze-c1.jsonl`, K-pass: `verdicts_ok 3`, `PASS`.
- Every all-`holds` control that fails does so on lint legs: K2 `lint_ok 2`, K3 `lint_ok 0`, K3b `lint_ok 2`, each with `verdicts_ok 3` (same receipt). The verdict leg refuses only `partly` (K4), identical bodies (K5) and missing/lane-only citations (K8).
- FROZEN.md:15 says every claim is one "a do-nothing control cannot reach (§9)". For the C1 cohort leg that is false on the round's own evidence: K-pass is a non-reading cohort that reaches the target predicate. The precedent is SCORECARD.md:1241 (round 24): a scripted non-reader control reading 8 of 8 was ruled "not depth evidence" under hyaku addendum §9.
- Outside reader: a C1 PASS on this counter is an unverified count of seat assertions. Without a named non-author re-open of the 18 verdicts, depth cannot be called verified.

## 2. The bar is asymmetric and its FAIL is predictable (FROZEN.md:52-54; check-scrub-admission-r51.py:352-354, 369-370)

- Negatives block with no evidence: `partly`/`fails` is appended to `blocking` and skips the citation check (`:352-354`, the citation call is at `:360`). FROZEN.md:53-54 says so: a negative blocks "whatever its citations". A positive needs two resolving citations.
- Six seats per row (`R51RevGR<n>{a,b,c}`, `R51CritGR<n>{a,b,c}`); `row_ok` requires `not blocking` across all six (`:369-370`). One `partly` in eighteen seats blocks its row.
- The seat roles include three critics per row. The w1 critic spec in the working tree frames the role as "attack" (`.ufo/waves/round-51/w1-spec.json`, item R51CritTrends; mutable, prompt text only). The w2 prompts are not frozen (see §3), so I cannot confirm the counted critics' wording.
- History: rounds 47–50 each closed `rejected-honest-stop` on C1 depth (FROZEN.md:11-12). Round 50 had four `partly` on GR2, one on GR1 and six on GR3 (SCORECARD.md:3232 measured outcome). The round-50 closer re-opened four of those calls and agreed with each (`corpus/lessons/round-50-verifier-spotcheck.md` §4).
- So the bar is a clean sweep by six seats including three attackers, and a FAIL means "an attacker still found something". The report must say that, or a FAIL reads as "the rows are false".

## 3. What makes a fifth cohort different, and what does not

Different:
- an uncounted pre-read of the freeze bytes (FROZEN.md:56-57);
- mechanical lint: whole-line quotes (QUALITY 94, `corpus/QUALITY.md:184`) and a generated `### Range gaps (R51)` block (`lint-grounding-r51.py:232, 247, 257, 283`).

Not different:
- the verdicts. The same seat roles and the same credit rule decide them, and the verdict leg accepts templated holds (§1);
- the author. The amendment is written by the L1, who wrote the rows, and the freeze does not require each pre-read negative to be applied or refused with a reason before dispatch.

Limits of the new lint:
- The gap block is built from the entry's own citations (`cited.setdefault` at `lint-grounding-r51.py:232, 247`; `out = {n for n in nums if not in_ranges(n, ranges)}` at `:257`). It checks agreement with what the entry cites. An uncited range the row needs never appears. R50's "incomplete range list" defect class is of this kind.
- `git diff --stat c0ad548 2732ee6c -- corpus/knowledge/btrfs-scrub-grounding-r45.md`: 104 insertions, 68 deletions. The GR2 statement is replaced, not corrected, and the new text adds fresh claims (the ordering of `-EPERM`, `-EINVAL`, `memdup_user`, `-EOPNOTSUPP`, `mnt_want_write_file`, `-EFAULT`; the progress-query returns). New claims are new surface. A second `partly` on GR2 is the expected outcome, not a tail risk.

Not frozen:
- `git ls-tree -r --name-only 2732ee6c -- .ufo/waves/round-51/` lists only `before/`, `controls/` and `frozen/`. `frozen/FROZEN-hashes.txt` hashes six counter/battery files. The w2 dispatch and seat prompts are uncommitted, so the counted instructions can change after freeze with no record.

## 4. C2 and C3 are counter claims, and their before-receipts already PASS

- `git cat-file -e c0ad548:<path>` fails for `tools/check-selftest-matcher-r51.py`, `tools/score-counter-cheats-r51.py`, `tools/check-adjacency-table-r51.py`, `tools/lint-grounding-r51.py` and `tools/check-scrub-admission-r51.py`. The receipts labelled `before/…-at-base` therefore run the new counters over base data.
- `before/c2-cheats-at-base.json`: top-level `verdict PASS` (`real_pass 1, cheats 4, cheats_rejected 4, r50_cheats_rejected 0`). `before/c3-at-base.json`: `verdict PASS` with every target leg at its predicate value.
- The census, PROVINCE.md and the registry are unchanged (FROZEN.md:41-43 says so), so the target predicates do not measure a lane change. The one real before/after is the counter's behaviour on the same bytes: the round-50 counter accepts F1–F4 (`before/c2-cheats-at-base.json`: `r50:F1-liar … r50:F4-neutered` all PASS), and the r51 counter rejects all four (`r51:F1…F4` FAIL).
- Labels: the claim table calls C2 "operability" and C3 "adjacency". An outside reader will read those as axis moves. The declaration keeps ordinals at operability 9 and adjacency 8 (SCORECARD.md:3296-3300). The honest label is "instrument (discernment), matcher counter" and "instrument (discernment), adjacency counter; no adjacency surface changed".
- The cheat set is the lane's own list. The round-50 closure named the liar-census and `${out}` evasions as limits (`corpus/lessons/round-50-verifier-spotcheck.md` §6 item 5). A cheat-set PASS shows only those spellings are caught. The lane's own precedent for a self-enumerated check that needs a named outside reader is SCORECARD.md:1343 (exploratory: `unprovable-but-better` only with a named non-author reviewer, otherwise `unprovable`). It applies by analogy here.
- C3's live leg is set at `live_quote_ok >= 8`, while the base receipt measures 9 (`before/c3-at-base.json`). Either give the sibling-drift reason for 8 or use 9.
- C3 binds displayed anchors to `corpus/knowledge/adjacency-anchors-r19.json`, a lane-authored registry. `registry_ok` proves consistency with the lane's own file. Only the live-quote legs touch sibling repos, and those are byte-substring checks, which the round-50 closure already noted are not semantic entailment (`corpus/lessons/round-50-verifier-spotcheck.md` §2, C3). "Adjacency improved" cannot be claimed.

## 5. Trend calibration from round 50

- Author: quality `harmed`, discernment `unprovable-but-better` (SCORECARD.md:3284-3296).
- Closer: quality `unchanged` (corrections real, rows pending, no admitted entry shown false) and discernment `improved` on a six-item spot-check (`corpus/lessons/round-50-verifier-spotcheck.md` §5).
- The two graders disagree on both verdicts for the same evidence. Round 51 must name which grader its verdicts rely on, and must not repeat an unnamed self-grade.
- QUALITY 49 (`corpus/QUALITY.md:97`) says in-round hardening is not by itself `improved`; it needs a named superseded prior text with evidence. The superseded texts exist (GR1's quote line and GR2's statement, per the diff in §3), so a quality improvement can be argued on that basis, but only for the superseded text, and the new text needs a re-open (QUALITY 91, `corpus/QUALITY.md:179`).

## 6. Proposed sentences

Trend verdicts, C1 PASS (counted cohort reads `holds` on all three rows):

- `expansion: unchanged — no knowledge entry, SOURCES row or Frontier row was added; GR1–GR3 are edits to the existing note corpus/knowledge/btrfs-scrub-grounding-r45.md.`
- `depth: unchanged at 8 — depth is counted by notes and SKILL lines (67 notes, 4594 SKILL lines), which this round does not change; the admitted rows are a quality fact, not a depth count.`
- `quality: unprovable-but-better — GR1's cmdline.c:147 quote and GR2's statement are superseded in place (QUALITY 49, 94), and six seats per row read holds on the amended bytes. The counter checks report format and citation existence, not verdict correctness; no non-author has re-opened the rewritten GR2 clauses. Becomes improved only with a named non-author re-open of those clauses.`
- `discernment: unprovable-but-better — the uncounted pre-read and the lint found defects before counting; the counted cohort (three critics per row) found no bound negative. The verdicts are lane-dispatched seat assertions, and the verdict leg accepts templated holds (battery K-pass).`

Trend verdicts, C1 FAIL (at least one row bound `partly`/`fails`):

- `expansion: unchanged.`
- `depth: unchanged at 8.`
- `quality: unchanged — the corrections (GR1 whole-line quote, the lint-generated gap block) are real, but no row is admitted. The entry's Gate status section names each bound negative. Harmed only if a rewritten clause is found false and left unmarked, which needs a named non-author check.`
- `discernment: unprovable-but-better — the blocking seats' negatives are recorded in the entry; their correctness is the lane's own call until a named non-author check is on record.`

Instrument sentence (required in the report under either outcome):

`C2 and C3 change the counters, not the lane. The three r51 counters were absent at c0ad548; the before-receipts run them over unchanged base bytes and already read PASS on their target predicates. The census, PROVINCE.md and the registry are byte-identical to base, and the operability (9) and adjacency (8) ordinals do not move. The measured delta is the matcher counter refusing the four enumerated cheats (r50 accepted 4 of 4 on the same census bytes; r51 rejects 4 of 4). The cheats are the lane's own list, so discernment for C2 and C3 is unprovable-but-better: the PASS does not show other fakes fail, and the C3 live-quote leg is set at 8 of 9.`

## 7. Smallest pre-w2 changes (amendment commit only; no frozen counter changes)

1. Write into the amendment: every pre-read negative is either applied or refused with a reason in the entry's gate section before w2 dispatch.
2. Hash the w2 dispatch and seat prompts into the amendment or FROZEN-hashes.
3. Pre-declare in the report that a C1 PASS is a count of seat verdicts, and name the non-author who will re-open the rewritten GR2 clauses.
4. Relabel C2 and C3 as instrument (discernment) claims; state that operability and adjacency ordinals do not move.
5. Set the C3 live-quote leg to 9, or write the sibling-drift reason for 8.
6. Optional: a battery control "clean lint, wrong claim, templated all-holds cohort must FAIL". This changes the frozen battery, so it needs its own recorded freeze or must be stated as a gap.

No tooling was installed. No tracked lane file was written. Scratch used: `/fast/scratch/hyaku/tsukuroi-r51/R51CritTrends` (created empty, removed).
