# R2Reviewer — C2/C3 attack findings

Axes: operability, freshness, hermeticity, discriminating coverage. Frozen declaration 6b4267623b3d6cf88b32c2df8daaad1a5bc9f19e was read; no predicate or tool was amended. Severity ordering below is a review recommendation, not admission.

## High — C3 accepts a token list without the claimed five paths
`tools/check-r71-routed-r72.py:86-90` checks only four substrings after `## Correction`. With an otherwise correct fixture, the entire note `## Correction
R71-NOTE-MODPROBE-COUNT five four /usr/lib/modprobe.d` returns `ROUTED_STALE=0`, rc 0. It neither enumerates the five paths nor supplies a correction. The inverted sentence “five /usr/lib/modprobe.d paths is wrong; four remains correct” also returns 0. These are two demonstrated semantic false passes; the frozen checker must remain frozen, so actual correction bytes require independent review.

## Medium — C3 accepts an explicitly denied erratum
`tools/check-r71-routed-r72.py:75-79` only requires the receipt/revision substrings in the matching header block. A block saying “This is NOT an erratum; do NOT correct [receipt] at 2b358d2d. No change is recorded.” returns STALE=0, rc 0. This is a third semantic false pass, not a request to reinterpret the frozen predicate: the narrow literal naming predicate is satisfied while semantic closure is not proved.

## Medium — C2 seventh case is vacuous; file-fixture construction is not exercised
Captured `tools/check-selftest-tally.py:108` uses `("green-control", receipt, "", 0, "added_figures_mismatched=0")`: its empty diff names no census selftest and exercises no figure. All eight disabling mutants leave SELFTEST-green-control passing. Other cases correctly kill their intended mutants. In addition, `:83-86,111-123` creates/removes an empty temp root; receipt and diff fixtures remain strings and the root is unused. Filesystem audit records exactly mkdtemp/mkdir/rmdir and no fixture writes. Thus the declared build-under-TMPDIR file-fixture behavior is not demonstrated, despite seven passing names. The matching-figure case also remains green when the CASE loop is removed; it asserts absence of mismatches rather than an affirmative OK finding (weak positive control, not counted as an additional wholly vacuous case).

## Medium — C3 rejects two otherwise correct corrections
Using the same green fixture, change only lowercase `five` to `Five`: STALE=1, rc 1. Change only note heading `## Correction` to `## Erratum`: STALE=1, rc 1. Both still state the defect id, five concrete filenames, superseded four figure and directory; the frozen prose does not require those exact capitalization/header choices. These are two semantic false-fail observations; actual proposed repair uses the accepted spelling. Additional double-space receipt summary is rejected by exact summary equality, as specified, and is not counted as a false fail.

## Low — invalid TMPDIR can fall back outside the requested root
`tools/check-selftest-tally.py:83-86` sets `base=None` when TMPDIR names a nonexistent directory; instrumented tempfile call receives `dir=None`. Valid TMPDIR was honoured and no /tmp writes occurred in the exercised suite. An actual /tmp fallback was deliberately NOT executed; leak count is observed writes, not inferred writes. Recommendation: fail explicitly rather than silently discard an explicit TMPDIR.

## Successful attacks/controls and contracts
- C2 suite: seven named PASS lines, rc 0; eight branch mutants each produce suite rc 1. Case-compare -> mismatch fails; label-compare -> label-mismatch; superseded -> superseded-skip; scope -> out-of-scope; no-receipt -> no-receipt-line; forced wrong positive -> match; ignored figures -> mismatch; wrong exit -> mismatch and label-mismatch.
- Normal CLI independently returns 0 matching, 1 mismatch, 2 missing receipt PASS line; no-argument usage returns 2. Existing r70 self-demo remains rc 0, `added_figures_mismatched=0 skipped_superseded=0 receipt_cases=214 receipt_labels=18`.
- C3 correct fixture STALE=0/rc0; plausible wrong summary STALE=1/rc1; missing defect id STALE=1/rc1. A receipt copied with exactly matching summaries passes by design, irrespective of non-summary text: this proves re-derivability, not provenance, and is not counted as a false pass.
- Real re-derivation: one byte changed in fixture counter (`MP_ROWS=` -> `MP_ROWS:`), receipt changed to match doctored output. Still STALE=1/rc1. Audit observes canonical invocation `[python3, <scratch>/clone/tools/count-mp-rows-r71.py, --revision, 2b358d2d]`, not fixture/tools. See `counter_summary()` at checker lines 49-55. Fixture cannot override counter selection. Counter subprocess status is not checked; summary presence/equality is the actual contract.

## Residual risk and verification gaps
- LSP device unavailable (`xd://lsp`: No such tool); references/definitions/diagnostics could not run. Text/observed execution is reported, not semantic LSP proof.
- C2 captured live worktree bytes, not a completed E2 draft or committed final revision. C3 fixture tests exercise frozen logic; they do not certify committed final repair. Main must check final revision and actual five paths; no host config contents were read.
- No installs, package/service/host mutations, staging or commits. Scratch clones and mutants only. Initial discovery included read-only git commands against the source lane rather than the prescribed clone; subsequent attack git access is through the clone. This command-routing deviation is disclosed, not claimed compliant.
- Hard write scope excludes the conflicting sibling report trailer `w1/R2Reviewer.md`; this in-directory findings file is the scoped report.
- Self-evaluation: accuracy 4 (observed results; invalid TMPDIR leak remains inference); completeness 4 (no committed final revision); clarity 4 (semantic vs frozen literal limits separated); actionability 4 (named cases/lines); conciseness 4 (full raw evidence retained separately). No runtime admission, saturation or resume claim is made by this review.

C2_VACUOUS_CASES=1
C2_TMPDIR_LEAK=0
C3_FALSE_PASSES=3
C3_FALSE_FAILS=2
