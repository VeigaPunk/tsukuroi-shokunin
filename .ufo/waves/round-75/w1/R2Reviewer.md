Verdict so far: C2 CHECKER IS INSUFFICIENT AS REPAIR PROOF; recommendation only, not admission. Eleven adversarial fixtures pass all four predicates despite invalid or unrelated repair content. The genuinely verb-free axes control is rejected.
Still unchecked: L1 final landing/committed repair bytes and final citing note. Planned S314–S316 rows reviewed; no row-shape or anchor defect found.

# R2Reviewer — round 75

Axes: freshness, C2 predicate integrity, attack coverage; C1 registry correctness. No implementation, checker, registry, sibling artifact or runtime was modified. No subagents, tool installs, git mutations, judgment or integration.

## Ranked findings

### P1 — Non-counting strings satisfy the axes counting-command requirement

`tools/check-r74-routed-r75.py:42,105-118` accepts any nonempty backticked substring on each axis row. It does not establish an executable command, an axis-specific count, a valid score, or even a rendered Markdown table. Fixture `R2Reviewer/03-identical-backticks/SCORECARD.md` supplies the identical literal `banana` for all six axes and passes `ROUTED_OK=4/4`. Identical commands alone are not inherently wrong; accepting demonstrably non-counting text is the concrete defect.

`R2Reviewer/07-commented-table/SCORECARD.md` hides the entire accepted block inside an HTML comment. `R2Reviewer/11-command-supersedence/SCORECARD.md` has no superseding sentence at all: six scores of -999 and identical `echo correction round-65` strings satisfy both the round-65 mention and verb predicates. These are syntactic false positives against the declared counting/superseding behavior. Require independent review of meaningful, scoped, runnable counting commands and an explicit superseding statement; the frozen checker passing is not that review.

### P1 — Required words can assert the opposite repair and still pass

`tools/check-r74-routed-r75.py:63-84,125-134` tests only case-insensitive substring presence. It never interprets polarity, associates an OID with its real/fabricated role, checks that a referenced report exists, or establishes what earlier statement is replaced.

- `R2Reviewer/05-negative-fabricated/.../receipt-g-landing.txt` retains the fabricated header, says no correction is required, and quotes the fabricated OID only in a negative assertion. Passes all four.
- `R2Reviewer/08-reversed-oids/.../receipt-g-landing.txt` calls the real OID fabricated and the fabricated OID real. Passes all four.
- `R2Reviewer/06-negated-lessons/corpus/lessons/round-74.md` explicitly denies the missing receipt/error and rejects the accurate phrase; says the referenced report is absent. Passes all four. No report file exists in any fixture.
- `R2Reviewer/10-combined-false-repair/` combines reversed OIDs, denied lesson corrections, a hidden table and non-counting strings; passes all four simultaneously.

The claim is naming the missing death receipt, not manufacturing a death receipt: this review does not incorrectly demand a new historical death artifact. The defect is that denial/token presence also suffices. Review actual correction propositions, including OID roles and the already-existing report, outside this frozen lexical gate.

### P2 — Report path supplies the supposedly named unit; token dump needs no unit assertion

`tools/check-r74-routed-r75.py:75-81,125-130` looks for `SC3Index` anywhere in the death token's window. In `R2Reviewer/01-token-dump-no-unit/corpus/lessons/round-74.md`, all required strings occupy one line without any named death unit. The only `SC3Index` is embedded in `w1/SC3Index/report.md`, belonging to the other item. It passes all four. `01b-token-dump` also passes with a standalone unit string but no correction narrative. Thus the two lesson checks are not independent semantic evidence. Bind the unit/class to the death-receipt correction during content review.

### P2 — Window leakage and substring verbs permit unrelated later sections

`tools/check-r74-routed-r75.py:54-65` takes the first token occurrence and 80 following lines regardless of headings, and recognizes verbs as arbitrary substrings. `R2Reviewer/02-later-heading/` places both tokens before `## Unrelated later section`; every satisfying detail is after that later heading. It passes all four. `09-substring-verb` passes with only “uncorrected errors,” which contains `corrected` but asserts no supersession. The truly verb-free fixture `04-no-verb` fails as expected. The cross-heading window is explicitly frozen behavior, not an accidental deviation from the implementation's comment; nevertheless it cannot establish that a named correction block carries its own evidence.

## Fixture receipts and exact outcomes

Durable paths below are relative to this report's directory: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-75/w1/`. Every fixture is a complete independent mirror with only the three checker input files. Original roots were `/fast/scratch/hyaku/tsukuroi-r75/R2Reviewer/<name>`; durable copies are `R2Reviewer/<name>`. `R2Reviewer/results.json` preserves exact argv-root identities, return codes, stdout and stderr. All stderr values were empty.

Executed, concurrently in a six-worker batch: `TMPDIR=/fast/scratch/hyaku/tsukuroi-r75/R2Reviewer python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-r74-routed-r75.py --root /fast/scratch/hyaku/tsukuroi-r75/R2Reviewer/<name>`. The final command-only fixture was scored separately after construction. Checker SHA256 independently measured: `4b5c801ce4be7ea7562d9b472ce58badcd113d1062280220500275730f567d2c`, identical to declaration.

| Fixture | Checker rc | Exact stdout (newline escaped) | Meaning |
|---|---|---|---|
| control | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | lexical positive control, not real repair evidence |
| 01-token-dump-no-unit | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | false acceptance; unit leaks from report path |
| 01b-token-dump | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | false acceptance; unstructured words |
| 02-later-heading | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | false acceptance; unrelated later section |
| 03-identical-backticks | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | false acceptance; banana is not a count |
| 04-no-verb | 1 | `ROUTED_STALE=1 ROUTED_OK=3/4\nR74-STALE-AXES-TABLE STALE reason=verb path=SCORECARD.md\n` | correct rejection |
| 05-negative-fabricated | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | false acceptance; denial, not correction |
| 06-negated-lessons | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | false acceptance; explicit opposite assertions |
| 07-commented-table | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | false acceptance; no visible axes block |
| 08-reversed-oids | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | false acceptance; wrong OID roles |
| 09-substring-verb | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | false acceptance; uncorrected is not superseded |
| 10-combined-false-repair | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | simultaneous all-four semantic failure |
| 11-command-supersedence | 0 | `ROUTED_STALE=0 ROUTED_OK=4/4\n` | false acceptance; no superseding sentence |

## Predicate attack coverage

All code-level ways to decouple the four predicates from the declared repair fall into these observable classes:

1. Context/polarity/attribution: naked strings, denials, hypothetical examples, quotes, wrong OID roles, unrelated facts, fabricated factual assertions. Naked strings, denials and reversed roles proved above; hypothetical prose is an inference from the same substring predicate, not separately executed.
2. Context boundaries: borrow content from another named item or a later heading within the 81-line window; hide evidence in comments/code examples. Cross-item unit leakage, later headings and HTML-hidden axes proved. Code fences are an unexecuted inference; no Markdown parsing exists.
3. Verb weakness: unrelated, negated or embedded verb substrings rather than an actual supersession. Negation, “uncorrected,” and command-only mentions proved.
4. Axis weakness: any six matching prefixes and any backticks, without valid columns/scores, command existence, output, axis relevance or unique rows. Wrong scores/noncommands proved. Duplicate extra rows, arbitrary column placement and conflicting later blocks are static inferences from first-match selection at lines 93-110, not separately executed. The frozen claim does not require six different commands if one meaningful command legitimately measures all axes.
5. Provenance/existence/history: no check that the report exists or supports the statement, no git-object verification of the OIDs, no append-only ancestry comparison, no relation between comments and visible current-use prose. Missing fixture report proved. False historical provenance, later contradictions, deletion of old material and arbitrary uncommitted `--root` inputs are static limitations; this review does not misrepresent fixture success as committed-byte success. `--revision` reads committed paths but still does not validate those semantic/history properties.

This is a complete classification of checks omitted by this finite predicate, not a claim to enumerate every possible natural-language deception. A frozen lexical gate can be retained as a necessary syntactic check; its score must not be represented as sufficient semantic closure.

## S314–S316 registry review

Reviewed exact planned rows at `.ufo/waves/round-75/w1/SC2Sources.md:13-15` after that seat supplied the draft. These rows were not yet present in `corpus/SOURCES.md` during initial inspection. Contract: fleet `CORPUS.md:86-108` requires eleven cells, no internal pipe, revision-qualified anchors, legal status, date/cadence recheck, and citing used-by paths.

| Row | Source evidence inspected | Result |
|---|---|---|
| S314 | pinned transaction.c:800-881 begins `transaction_activate` at 800 and contains all ten labelled steps at 822-879; 1143-1217 contains required/ignored start, verify, required/ignored stop and try-restart propagation | Accurate anchor; 11 cells / 12 separators; no internal pipe |
| S315 | pinned job.c:398-440 contains algebra comment and `job_type_lookup_merge` at 426; 443-480 contains the complete `job_type_is_redundant` definition | Accurate anchor; 11 cells / 12 separators; no internal pipe |
| S316 | pinned job.h:33-36 contains JOB_TRY_RESTART exclusion; 60-76 contains the full JobResult enum, including ASSERT through CONCURRENCY | Accurate anchor; this names enum/rules, not a function; 11 cells / 12 separators; no internal pipe |

All three explicitly pin v262; `status=mined`, `recheck=on-release` are contract-legal. Every used-by cell is exactly `corpus/knowledge/systemd-job-transaction-plane-r75.md`, with no lesson/other note. `mined` remains conditional on the landing of a note that actually cites the row; a planned status is not already an admitted fact. Final note existence/citations are outside this unlanded-draft review.

Independently hashed all three pinned source bytes: transaction.c `c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3`; job.c `024a1accfd833223f2913d72e1f106fd40175429d31fcaca2321370fb5a10897`; job.h `22d7b942426402ddba376c7b713bc9937c2eaa9f5817e8735dec8d5b6cf57c3a`. Each matches the draft and manifest. A small row-shape evaluation printed all three successful row results then also matched the Gate table and raised IndexError; only the unexecuted hashing step was retried, successfully. No successful fixture was rerun.

## Residual risk and verification gaps

- `xd://lsp` is unavailable (device reports “No such tool”). Thus no LSP status/references/definition/diagnostics were possible; literal source lookup and direct definition-range inspection were fallback evidence, not semantic LSP proof.
- Reviewed actual declaration diff base→1e2bb29: checker is newly added; repair surfaces were not yet landed. This is a predicate/draft review, not certification of final C2 prose or committed acceptance.
- No canonical runtime, reroute, saturation or resume-path code is changed by this scoped diff; no such behavior was exercised or inferred. No runtime/judge invoked.
- No additional build/lint/selftest run; assignment-authorized checks were tamper fixtures, row-shape inspection and source hashing only. No host mutation or tool installation.
- Durable fixture copies and exact output receipts retained in own seat directory; scratch cleanup recorded below after preservation.

## Self-evaluation

Accuracy 4/5: exact counter outputs and source ranges supplied; final landing not observed. Completeness 4/5: all requested tamper classes and planned rows covered; final actual repair bytes were unavailable. Clarity 4/5: separates checker acceptance, repair truth and inferred limitations; long audit detail remains. Actionability 4/5: concrete fixture per finding; frozen predicate cannot be silently strengthened this round. Conciseness 4/5: detailed receipts are required for replay. Overall 4.0/5. Improvement priorities: independently review final committed correction propositions and command semantics, then confirm landed mined-row citations. Self-check: findings do not mistake fixture success for real closure.

Cleanup outcome: final receipt copy and removal of `/fast/scratch/hyaku/tsukuroi-r75/R2Reviewer` completed with exit 0. All thirteen fixture mirrors and results.json remain under the owned durable `w1/R2Reviewer/` directory.
