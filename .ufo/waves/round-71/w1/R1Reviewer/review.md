# R1Reviewer — C1 independent falsification

Axes: clause coverage, independent implementation, row-verdict agreement, source-level semantic fidelity. No axis or frozen predicate amended.

## Findings by severity

1. **P2 — MP6 omits the built-in-only route constraint required by the frozen claim.** Draft `SC1Entry/module-parameter-plane-r71.md:16,31-33` describes both routes without restricting them to loadable modules; nowhere in the draft does it state that built-ins require the kernel command line. `before/src/kernel-parameters.rst:26-30` explicitly requires that route for built-ins. Its located MP6 quote is at lines 20-21 and stops before this qualifier. Add the built-in constraint; do not represent the lexical counter pass as complete coverage of the declaration.

2. **P2 — MP3 drops part of its own quoted get contract and the declared optional-callback qualifier.** Draft line 13 says get returns the length written, but `before/src/moduleparam.h:65-66` says length **or -errno**; this is the very text quoted by MP3. Neither row nor explanation at lines 25-27 says set/get may be absent (only free is marked optional). `before/src/params.c:569-570,586-587` explicitly handles absent get/set with -EPERM. Preserve the get error result and distinguish optional set/get from the optional free hook.

3. **P2 — MP2 explanation confuses visibility with store installation.** Draft lines 22-24 calls a nonzero perm “the condition for a store callback.” `before/src/params.c:669-675` installs store only if a write bit is set; otherwise store is NULL even for a nonzero perm such as 0444. The next draft phrase and MP2 row are more accurate, making the explanation internally inconsistent. Replace the nonzero condition with the write-bit test.

These are recommendation findings, not an admission/verdict. No lane files were edited.

## Independent comparison

Frozen declaration read from the Git object at `0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e`. Four snapshot SHA256 values and counter digest matched the assignment pins. Draft SHA256: `cdc4b7af71224ccc6c22b8b4e26c9547d257da7104aad35d902b091a9090281f`.

The independent checker uses physical-line cell splitting, explicit field validation, digest/map/registry binding checks, quote normalization, identifier tracking, grounding sets and global targets. No import of the lane counter. Its initial whole-row regex was replaced by the independent cell parser. Its generic-English stopword vocabulary and hyphen boundaries are not identical to the frozen counter; this is a disclosed implementation limitation, not a proposed predicate amendment or proof of universal equivalence. The lane counter remains the authoritative frozen measurement. All observed row pass/fail outcomes agree.

The draft mirror combines the unchanged SC1Entry note with the declaration-revision registry plus the four exact registry rows inside SC2Sources/rows.md's first text fence. It is **not** a claim of a committed integrated revision. Existing registry: 296 rows; assembled registry: 300. Both checkers on the draft returned rc 0 and `MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0`, met=1. This mechanical pass does not erase the semantic omissions above.

Built an independent six-row fixture against real pinned snapshots, with its own statements, quotes and four registry bindings. Base control passes both checkers. Sixteen mutants fail both: short statement; ungrounded statement; swapped digest; absent quote; located 28-word quote; extra cell; duplicate id; noncontiguous ids; unregistered source; snapshot reused three times; absent anchor binding; absent URL binding; irregularly spaced MP-shaped line; map digest mismatch; five rows; real-token/gibberish mixture. Reuse mutation also fails other clauses; it is not an isolated proof of the reuse gate. Initial source-URL mutation had not actually changed its intended field; it was corrected before the final battery recorded here.

Observed agreement: **105/105 parsed row occurrences**, retaining the second duplicate-id occurrence separately; **18/18 whole-input return codes** (draft, base, 16 mutants). Malformed rows are excluded from parsed-row totals but remain recorded in raw evidence and whole-input results. `verdicts.tsv` is the row-by-row diff. `evidence.json` preserves every stdout/stderr and return code.

## Quote and substance audit, every row

| Row | Located quote in committed snapshot | Substance outcome |
|---|---|---|
| MP1 | params.c:633 | Supported with context: BUG_ON at 634; module skip at 710-711; builtin skip at 826-827. The comment alone is weaker than the surrounding control flow. |
| MP2 | params.c:669 | Row supported by 670-675 and missing-set handling at 586-587; explanation contradicts the write-bit gate (finding 3). |
| MP3 | moduleparam.h:65 | Set contract at 63-64 and free at 67-68 support the other clauses; get's -errno alternative and optional set/get are omitted (finding 2). |
| MP4 | main.c:3393 | Supported by 3384-3394: async_probe and dyndbg handling precede the warning; return 0 is unconditional. A successfully handled dyndbg parameter is not warned. |
| MP5 | main.c:3407 | Supported by comma-list matching at 2934-2953 and refusal with -EPERM at 3406-3408. EPERM in the row is shorthand; the source's actual returned integer is negative. |
| MP6 | kernel-parameters.rst:20-21 | Two routes supported, examples at 23-24; built-in qualifier at 26-30 omitted (finding 1). Disclosure at 34-35 supports its added clause. |

## Residual risk and verification gaps

- Semantic LSP unavailable: `xd://lsp` returned “No such tool”; no status/references/definition/diagnostics interface was mounted. Text/source inspection is fallback evidence, not semantic indexing proof.
- No production/runtime or census/C2/resume behavior changed or exercised; those are outside this C1 seat. No saturation or same-identity rerouting assertion is made.
- No integrated revision was reviewed, and no host writes, package installs, service actions, secrets, sysfs writes, staging or commits occurred. Only own scratch clone and report artifacts were written.
- Independent source and fixture-builder preserved alongside raw evidence; run them after recreating the specified scratch clone and placing checker.py there as check_c1.py. Snapshot/registry inputs still refer to the canonical lane's read-only committed material. Scratch deleted before terminal yield.

Self-evaluation: accuracy 4 (source pins and raw outputs preserved; lexical equivalence not claimed); completeness 4 (all six rows and sixteen mutants; no exhaustive token equivalence); clarity 4 (findings separate semantics from mechanical pass); actionability 4 (specific draft lines and source spans); conciseness 4 (audit evidence retained outside this summary). Overall 4.0. Highest-impact improvements are the built-in qualifier, then the full ops contract. Would the user agree: evidence is reproducible, with limitations explicit.

ROWS=6 AGREE=105/105 DEFECTS=3 INDEPENDENT_RC=0
