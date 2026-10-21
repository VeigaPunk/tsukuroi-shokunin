# FxC3Distinct — C3 distinct-files denominator (falsify review)

Seat: TsukuroiR21.FxC3Distinct. Round 21, baseline 82e519203e676c532b1dc5ea91a85671f2286e7b, candidate revision 0a14952b59d20179e1c813af58befaecd6992a17.

Primary reviewed file: `tools/check-review-snapshots.py` at the exact digest on the Reviewed-SHA256 line below (matches `candidate-files.json:94-98` and the falsify manifest row `FxC3Distinct`, falsify-reviews.json:432-437). Read from the pinned candidate snapshot only; no live/moving files were read for this verdict.

Auxiliary snapshot dependencies (prose disclosure, read-only):
- `tools/_revision.py` candidate snapshot, sha256 `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf` (candidate-files.json:64-68) — imported by the primary at line 14; its `bind`/`clean_env` behavior conditions every `git_read` the primary performs. Reviewed for dependency context only; verdict binds the primary file.
- `.ufo/waves/round-21/reviews.json` and `.ufo/waves/round-21/falsify-reviews.json` — wave working-tree manifests read as declared data; no predispatch digest for them was supplied in candidate-files.json, so manifest counts below are session observations, not pinned evidence.
- `.ufo/waves/round-21/preregister.json` — same caveat; used for the C3 metric/command/limits text.

Tooling directive: no tool installed or upgraded (source-only review; nothing needed; nothing to report to L1). NO-EXEC honored: read/grep/glob/write only; no Bash/eval/import/compile/network/child agents; the tool was never run — all payload values below are hand counts from manifest bytes and source reading.

## Axes named

- Calibration (primary): honesty and enforceability of the C3 denominator — does `distinct_source_files` guard against review-count inflation, and is it consumed anywhere?
- Depth (secondary): binding fidelity — does a receipt's pinned digest certify the artifact its predicate names?
- Operability (tertiary): verdict-visibility — can a consumer of the checker payload distinguish 64 distinct-file reviews from 64 rows over one file without reading internals?

## Source predictions versus observations

- P1 (assigned prediction): dozens of same-source reviews are not dozens of distinct files or capability gains, and the checker's verdict does not separate them. CONFIRMED structurally from bytes (O2, O3): `distinct` is computed (line 56) but the exit code derives solely from `findings` (line 79); `distinct` appears only in the JSON payload (line 84). Nothing in the tool gates on the denominator.
- P2 (assigned prediction): the C3 gate deliberately stays red for missing dead reports. CONFIRMED by design reading plus lane documents: a declared report absent at the bound revision yields `REVIEW-REPORT-MISSING` (lines 63-64) and any dead/stub report fails the strict receipt equality (lines 71-76), either way `code = 1` (line 79). Candidate `corpus/lessons/round-21.md` records the disposition: build manifest retains all 64 rows including dead ScribeDecision, "no dropped denominator or substitute report", and expected-red treatment is accepted. The red is achieved by including, not excluding, the dead row.

## Observations (byte-cited, primary file unless noted)

- O1: `distinct = len({row["source"] for row in reviews})` (line 56) — distinctness is over declared source path strings, after schema validation (lines 43-54), before any byte verification (lines 59-78).
- O2: `code` is set only from `findings` (line 33/34/62-82); `distinct` feeds only payload key `distinct_source_files` (line 84). `pinned` (line 78) counts rows with zero findings; at PASS `pinned == total`.
- O3: schema dedup applies to `name` and `report` only (lines 46, 52-54); repeated `source` values and repeated `(source, predicate)` pairs raise no finding. Same-source fan-out under distinct names is the admitted shape.
- O4: selftest (lines 103-133) asserts only exit code + finding-id sets; no case asserts `distinct_source_files`, and no case has more than one review row. The denominator is executable-specification-free: a mutant changing line 56 passes all 16 cases.
- O5 (manifest, hand count): `reviews.json` declares 64 rows over 6 distinct declared source paths: snapshot `tools/_revision.py` 39 rows (ExecDecision, ScribeDecision, ReviewSource + 36 oracle rows), snapshot `corpus/lessons/round-20.md` 14 rows (13 Debt + ReviewHistory), `tools/check-revision-binding.py` 3, `tools/check-seat-scope.py` 3, `corpus/QUALITY.md` 3, `PROVINCE.md` 2. Expected payload at a clean run: `total_reviews=64, pinned_reviews=64, distinct_source_files=6` — a 64:6 review-to-file ratio, by construction.
- O6 (manifest): the 36 oracle rows' predicates name nine different consumer tool files (check-locator-clarification.py through check-seat-scope.py) while every one pins `_revision.py`'s digest `06b71e8c…`. The receipt certifies the shared binder, not the artifact named in the predicate. Candidate `corpus/lessons/round-21.md` discloses this as convention ("Primary `_revision.py` bytes were frozen before dispatch; those secondary observations remain qualified, not retroactively relabeled pinned"), and SCORECARD round-21 (line 650) declares "secondary build consumer/sibling reads were unpinned and remain a disclosed limitation". The checker cannot enforce predicate↔source agreement — the predicate is opaque free text (lines 50-51 check only non-empty, no CR/LF).
- O7 (manifest, hand count): `falsify-reviews.json` declares 63 rows over 13 distinct declared sources (9 candidate tools, selector-contract-r21.json ×8, check-review-snapshots.py ×8, PROVINCE.md, SKILL.md); here digests do bind the predicate-named files. preregister.json:41's C3 command names only `reviews.json`; a checker run against the falsify manifest is not preregistered as a command.
- O8: one non-UTF-8 report raises `UnicodeDecodeError` (line 66) inside the row loop, caught by `except (ValueError, TypeError, UnicodeError)` (line 80) → whole-manifest `REVIEW-MANIFEST-SCHEMA` / `CANNOT_EVALUATE` with `site=str(exc)[:100]`, all counts zeroed, remaining rows unvalidated. A report-encoding defect is conflated with a manifest-schema defect.
- O9: repo-wide search (`grep` over the shokunin tree) for `pinned_reviews|distinct_source_files|total_reviews` finds no consumer outside the tool itself; the SCORECARD prose ("reports distinct source files beside review count", line 650) is the only declared consumer. Candidate `tools/check-appended-notices.py` has an analogous, selftest-asserted `distinct_paths` (lines 822-828), so the lane already owns the stricter pattern this tool lacks.

## Findings by severity

- F1 (moderate, calibration): the distinct-files denominator is reported, never enforced. At PASS the payload can read 64 pinned reviews over 1 distinct source file and the tool still exits 0; the verdict cannot distinguish distinct-file coverage from same-source fan-out. The lane's declared claim is disclosure-shaped ("counts … and reports distinct source files beside review count"), so this is not infidelity to the written claim — but the reviewer instruction's guard ("dozens of same-source reviews are not dozens of distinct files or capability gains") exists only as an emitted number a human must compare. Any summary quoting `pinned_reviews` alone re-inflates the headline; the round's own accepted count-inflation correction pattern (lessons, CritBaseline/ConnPlanner disposition) is the precedent for requiring the denominator beside any count.
- F2 (minor, calibration): denominator semantics are declared-count, not evidenced-count, in both directions. (a) It includes rows that later fail (missing reports, dead seats, tampered digests still counted — computed at line 56 before verification); on red runs the denominator overstates verified files. (b) It is path-set distinctness: identical bytes at two declared paths count twice, so even the honest PASS-time number is a distinct-path count, not a distinct-reviewed-bytes count (`len({sha256})` would differ).
- F3 (minor, testability): selftest never exercises the denominator (O4). The one quantity this round's predicate is about has no executable assertion; the lane's own `distinct_paths` pattern in check-appended-notices.py:822-828 shows the missing standard.
- F4 (minor, robustness): non-UTF-8 report content aborts the whole manifest into a schema-classified CANNOT_EVALUATE (O8), zeroing counts and skipping remaining rows — a per-row `REVIEW-REPORT-MISSING`-style finding with honest partial counts would preserve the denominator's meaning on red runs.
- F5 (info, gate coverage): the preregistered C3 command binds one manifest (`reviews.json`); the separately frozen falsify manifest (63 rows) has no preregistered checking command (O7). L1 should either run the checker against `falsify-reviews.json` as a named second command or narrow the C3 "after" wording, which currently says "every delivered build/falsify review".
- F6 (residual risk, depth — documented convention, not a hidden defect): a receipt's Reviewed-SHA256 certifies only the declared `source` path; the artifact named inside the predicate is not tool-bound (O6). The lane discloses this (lessons + SCORECARD:650), so I record it as residual binding-fidelity risk: the tool structurally cannot catch a manifest that pins bytes of file A while the predicate claims review of file B, beyond what disclosure covers.

## Residual risk and verification gaps

- All manifest counts (64/6, 63/13) are hand counts from wave working-tree bytes, not tool output and not predispatch-pinned digests; L1's actual `check-review-snapshots.py` run is the only authoritative measurement. Cross-check: candidate lessons round-21 states "the build wave's 64 primary snapshot/predicate bindings were committed in preregistration c05af5c…", consistent with the 64-row count.
- I did not verify that `build/ScribeDecision.md` at the bound revision lacks receipt lines (it exists in the wave tree; its red contribution is asserted by lane documents, not by my byte read of the committed blob at a revision).
- Whether L1 will run the checker against `falsify-reviews.json` is undetermined (F5).
- The historical 13 missing / 20 malformed round-20 receipts are outside this manifest entirely; their red status is declared (preregister limits, SCORECARD:642) and not re-verifiable from this manifest.
- grep-based consumer search (O9) respects ignore rules; tracked files (`tools/`, `corpus/`, SCORECARD.md) are covered, untracked scratch is not.

## Limits

No execution of the tool, its selftest, or any mutant; no test/doc scaffolding written; verdict is source-grounded static analysis plus manifest byte inspection. Findings are recommendations to L1 (canonical planner/integration owner); this seat claims no closure, admission, or promotion authority.

Reviewed-SHA256: 736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e
Predicate: C3-distinct files denominator
Scope: executed=none