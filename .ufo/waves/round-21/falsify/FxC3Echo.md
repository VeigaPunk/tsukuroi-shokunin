# FxC3Echo — C3 receipt echo limits, source-only

Seat: TsukuroiR21.FxC3Echo (reviewer, round-21 falsify wave; fresh attack seat, not a build resume).
Candidate revision `0a14952b59d20179e1c813af58befaecd6992a17`.
Primary file: `.ufo/waves/round-21/candidate/tools/check-review-snapshots.py` (169 lines, inspected 1–169 in full).
Pre-dispatch digest declared at `candidate-files.json:94-98` (revision `0a14952b…`), matching the item.

Reviewed-SHA256: 736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e
Predicate: C3-receipt echo limits

## Axes

- calibration (C3 primary): what the receipt gate can and cannot establish — declared primary identity versus actual reading/comprehension or capture of all secondary bytes.
- operability: discriminators, exit map and diagnosability of the receipt checks (`REVIEW-*` finding taxonomy, 0/1/2 exit semantics).
- depth (minor): what the predicate string itself binds — the assignment↔manifest↔report chain.

## Observations (pinned bytes read; nothing run)

- Gate source `candidate/tools/check-review-snapshots.py` lines 1–169 (docstring, `safe_path` 20–23, `evaluate` 26–86, `git_read` 89–100, `selftest` 103–133, `main` 136–165).
- Dependency `candidate/tools/_revision.py` — `bind` 172–193, `clean_env` 62–66 (shared landed/pushed revision binding used by `main` 154–160).
- Claim/policy texts in the candidate copy: `preregister.json` (wave file, C3 block 36–43), `SCORECARD.md` 632–650, `corpus/lessons/round-21.md` (Gate table 5–17, critique dispositions 47–54), `corpus/knowledge/selector-contract-r21.md` 27–35, `corpus/QUALITY.md` criteria 42–44, `SKILL.md` 2124–2125 and registry row 2151.
- Manifests: `reviews.json` (build, 64 rows counted from 453 lines = 3 header + 64×7 + 2 footer; dead seat `ScribeDecision` retained at lines 25–31) and `falsify-reviews.json` (64 rows by the same count; my row at 417–423; C3 attack rows 382–437; cross rows 438–451).
- Sibling evidence cross-checked read-only: `build/CritNoHarm.md` 39–58 (dead-row exit-1 contract; `discover()` interplay), `build/ReviewTrailer.md` 38–42 (last-hit trailer semantics of the old scope gate), `falsify/FxCrossMetrics.md` F1/F6, `falsify/FxCrossScope.md` R2, draft `drafts/ExecReview/check-review-snapshots.py` (conservative `PATH_CHARS` at line 38 vs production `safe_path`).

Every statement below is tagged [OBSERVATION] (read from pinned bytes) or [PREDICTION] (source-derived behavior if the gate were run; L1 alone runs final checks, and this seat ran nothing).

## Answer to the assigned attack: the docs do not overclaim

Test: do candidate documents claim the C3 gate establishes comprehension (actual reading) or capture of all secondary bytes, despite the source-only echo limitation?

[OBSERVATION] Every located self-description states the opposite — the echo limit is disclosed at each level:

- Gate docstring, `check-review-snapshots.py:2`: "Check declared review byte/predicate identity, never actual reading or nonexecution."; payload scope string `:86`: "primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution".
- `SKILL.md:2151` (registry row): "declares identities, never proves reading or command nonexecution"; `SKILL.md:2125`: "the receipt gate checks declarations only, not actual reading or independent command absence".
- `preregister.json:42` (C3 limits): "Declared digest binding, not proof of actual reading or actual command nonexecution. Historical 13 missing and 20 malformed remain red."
- `SCORECARD.md:650`: "C3 counts primary snapshot/predicate declarations …; secondary build consumer/sibling reads were unpinned and remain a disclosed limitation, not retrospectively pinned."
- `corpus/lessons/round-21.md:51`: "receipts are disclosed strings and therefore cannot establish actual reading/comprehension"; `:12` gate row: "not proof of actual reading or command nonexecution".
- `selector-contract-r21.md:33`: "A scope/hash declaration is not proof of actual nonexecution/reading."; `QUALITY.md:87` (criterion 42): "A receipt is a declaration, not proof of actual reading or command nonexecution."

Verdict: the primary C3 attack (documentation overclaim) is refuted. No candidate document claims comprehension, proven reading, or all-secondary capture; each states the echo limit explicitly and consistently. [OBSERVATION from pinned bytes; no execution.]

## What the echo actually binds (prediction chain)

[PREDICTION from `check-review-snapshots.py:57-79`] The gate's complete binding power is three string comparisons per row:

1. committed `source` blob digest vs manifest `sha256` (`:59-62`) — exactly one primary file per row, read at the bound revision;
2. report receipt lines vs manifest `sha256` and `predicate` (`:66-74`) — pure string echo, exactly one column-0 line each;
3. report `Scope:` line vs the literal `executed=none` (`:75-76`).

Consequently a report consisting solely of the three receipt-shaped lines — naming no source, quoting no reviewed content, evaluating nothing — passes and increments `pinned_reviews`. The manifest↔dispatch-assignment link (predicate chosen at preregistration `c05af5c…` before the fifth dispatch) rests entirely on wave process evidence; no tool checks it. This is precisely the disclosed echo limit, and the docs disclose it (section above). The residual C3 risk is not misstatement but misreading by consumers: `pinned_reviews` is receipt hygiene, not review quality.

## Findings

### F1 — moderate: one malformed report blob erases all other findings and mislabels the cause [PREDICTION]

- A committed report blob that is not valid UTF-8 raises `UnicodeDecodeError` at `report.decode("utf-8")` (`:66`). `UnicodeDecodeError ⊂ UnicodeError` is caught by the manifest-schema handler `:80-82`, so the whole run becomes exit 2 with the single finding `REVIEW-MANIFEST-SCHEMA` and `str(exc)` text about codec bytes.
- Effects: all findings accumulated for earlier rows are discarded — including the deliberate `REVIEW-REPORT-MISSING` for dead `ScribeDecision` (`reviews.json:25-31`; CritNoHarm's "must exit 1 … never silently omit" contract) — and rows after the malformed one are never evaluated; `total_reviews` stays 64 while `pinned_reviews` is a partial count.
- The promised red class survives only as *a* red, not as *the named* red: the gate's taxonomy (SKILL registry row: exit 1 "missing/mismatched receipt", exit 2 "schema/path/revision/read/CLI") degrades a report-encoding defect into a manifest-schema label, and the missing-dead-report control becomes invisible in findings.
- Same abort shape for `RuntimeError` from `git_read` (`:89-100`, e.g. a `source` path resolving to a tree or submodule at the bound revision) → `E-READ`, exit 2, partial findings discarded.
- `--selftest` (`:110-124`) has no non-UTF-8 report case, no directory-path case, and no partial-run case, so it cannot detect this behavior.

### F2 — low/moderate: receipt scanner is column-0 prefix matching, quote- and fence-unaware [PREDICTION]

- Detection is `line.startswith(prefix)` over `splitlines()` (`:67-70`). A report that legitimately quotes a receipt template or lists a foreign seat's receipt at column 0 (e.g. inside a fenced block) produces extra matching lines and goes red (`REVIEW-SNAPSHOT-MISMATCH` / `REVIEW-SCOPE-MISMATCH` / `REVIEW-PREDICATE-MISMATCH`) despite a correct own receipt — false red.
- Conversely, a fence-quoted *complete* foreign receipt satisfies the scan in place of an own trailer: the echo limit permits receipt-shaped text in any textual role. The gate cannot distinguish a receipt from a quotation of a receipt without semantics it deliberately lacks. It errs red for partial quotes and can be satisfied by any complete receipt-shaped echo — never green for wrong declared bytes.
- Practical note: this report keeps every receipt mention inside bullets/backticks or indented, so it cannot trip its own manifest row.

### F3 — low: C3 scope check diverges from the operative seat-scope trailer semantics [OBSERVATION of both sources; PREDICTION of disagreement]

- C3 requires exactly one column-0 `Scope:` line anywhere in the report (`:70-76`).
- `check-seat-scope.py` grades the *last* `Scope:` line as the trailer (selftest cases `last-line-clean` / `last-line-unauthorized` at its `:346-350`; build evidence `ReviewTrailer.md:38-42`: "last-hit semantics, not per-line scanning").
- A report carrying a mid-body `Scope: executed=none` and a final `Scope: executed=probe` therefore passes C3's receipt scan (single `Scope:` line, exact value) while the operative scope gate fails it (`SCOPE-EXEC-UNAUTHORIZED`). Such a report counts toward `pinned_reviews`. Both gates run per wave, so the operative red still lands — but the two calibrated measures can disagree on identical bytes, which the round docs do not name.

### F4 — low: the preregistered C3 command covers only the build manifest, while the claim text covers falsify too [OBSERVATION]

- `preregister.json:40-41`: claim "every delivered build/falsify review has preregistered file digest and exact predicate", command `--manifest .ufo/waves/round-21/reviews.json` only.
- Falsify receipts live in `falsify-reviews.json` (64 rows; frozen before falsify dispatch per `round-21.md:52`) and are checkable only via a second, separately flagged invocation that the frozen command does not name (sibling `FxCrossScope.md` command list shows both runs).
- Net: coverage of 64 falsify receipt rows rests on L1 running the unfrozen second invocation, not on the preregistered metric as written. A final receipt quoting only the frozen command would not have measured the falsify manifest.

### F5 — info: one finding ID spans three distinct failures [OBSERVATION]

`REVIEW-SNAPSHOT-MISMATCH` is emitted for missing source bytes (`:61-62`), source digest mismatch (`:61-62`), and report digest-line mismatch (`:71-72`); `site` is only the seat name (`:30-31`). An operator cannot tell which without rerunning by hand. The selftest's `report-digest` case (`:114`) shows the conflation is deliberate naming, not an accident.

### F6 — info: production `safe_path` is looser than the draft's charset [OBSERVATION of both; PREDICTION of impact]

- Production `safe_path` (`:20-23`) rejects absolute paths, backslashes, and `.`/`..`/empty segments but accepts `:`, newlines and other control characters. The executor draft (`drafts/ExecReview/check-review-snapshots.py:38`) used the conservative `^[A-Za-z0-9._/-]+$`; the production version dropped it.
- [PREDICTION] No revision-smuggling found: `git show` treats everything after the first `:` in `f"{rev}:{path}"` (`:90`) as a path, so odd paths fail closed (`REVIEW-SNAPSHOT-MISMATCH` for absent paths, `RuntimeError` → `E-READ` for trees). Impact is schema looseness and diagnosability only.

### F7 — info: auxiliary snapshot dependencies are structurally unbindable [OBSERVATION + disclosed]

The schema has one `source` plus one `sha256` per row; auxiliary files a seat actually read (the falsify contract's prose-listed dependencies) are checked by no tool. `SCORECARD.md:650` discloses exactly this ("secondary build consumer/sibling reads were unpinned and remain a disclosed limitation"), so it is a documented limit, not a defect. Fx siblings' prose-listed auxiliary digests are decorative under C3.

### F8 — info: selftest coverage gaps [PREDICTION]

No fixture exists for: non-UTF-8 report (F1); CRLF report (`splitlines` retains `\r`, so all three receipt comparisons fail red [PREDICTION]); duplicate `Scope:` line (duplicate `Reviewed-SHA256:` is covered at `:117`, duplicate scope is not); missing `Predicate:` line as its own case; `source` equal to `report` path; a manifest predicate whose value embeds a receipt prefix. `--selftest` passing therefore does not exercise the F1/F2/F3 behaviors.

## Residual risk and verification gaps

- All gate behaviors above are source predictions; this seat is forbidden from running the gate, its selftest, or any mutant, so F1–F3 and F8 lack execution confirmation. L1's final runs are the only measurements.
- `reviews.json` and `falsify-reviews.json` were read in place at their current bytes; they are wave files, not candidate copies, and my receipt does not pin them.
- My receipt binds only the named primary file; the auxiliary dependencies below were read under their declared pre-dispatch digests, which I could not recompute under NO-EXEC.

## Auxiliary snapshot dependencies (outside the primary receipt)

- Declared via `candidate-files.json` (digests as declared, not recomputed): `tools/_revision.py` `06b71e8c…` (bind/clean_env used by the CLI path); `corpus/QUALITY.md` `1ac63541…`; `corpus/lessons/round-21.md` `ab841b25…`; `SKILL.md` `c43477cb…`; `SCORECARD.md` `04403120…`; `corpus/knowledge/selector-contract-r21.md` `b4966a9b…`; `PROVINCE.md` `a296da87…`.
- Wave files read for context, not digest-pinned: `preregister.json`, `reviews.json`, `falsify-reviews.json`, `falsify/spec.json`, `drafts/ExecReview/check-review-snapshots.py`, sibling reports `build/CritNoHarm.md`, `build/ReviewTrailer.md`, `falsify/FxCrossMetrics.md`, `falsify/FxCrossScope.md`.

Tooling directive: no tool installation was needed or performed; nothing to hand to L1 on that account.

These findings are advisory recommendations to L1; no non-author closure, admission, or outside promotion is claimed by this seat.

Scope: executed=none