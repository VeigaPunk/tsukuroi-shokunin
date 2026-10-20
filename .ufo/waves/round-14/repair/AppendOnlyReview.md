# AppendOnlyReview — tsukuroi round 14 (seat TsukuroiR14.AppendOnlyReview)

Report only. Read-only git plumbing (`show`, `diff`, `log`, `cat-file`) and an in-memory stdlib dry run over blobs; nothing written except this file. No gate, selftest, census or test run.

## Pins
- Round-14 baseline: `8606bad4cbc6451ac2890c9f8e2548a36c386db6` (HEAD; tracked tree clean at start).
- r12 frozen floor: `70fede2a7a890cb50a72db2d4230ee541183bf7b` (r12 MD/JSON, SKILL, PROVINCE, QUALITY, README, snapper note, round-12.md).
- Introducing commits: r12 lesson `9574a18`; r13 MD/JSON `44677cc` (unchanged since, verified `git diff --quiet`); `round-13.md` `44677cc`+`e1fc8fd` (74 appended lines, 0 removed); `round-13-verifier-spotcheck.md` `8606bad`.

## Evidence
1. **History is insertion-only in line terms.** `git diff --numstat 70fede2 HEAD` deletions: SKILL.md 1, every other corpus/LOG/SCORECARD/PROVINCE file 0.
2. **The SKILL.md "1 deletion" is an EOF artifact.** Base ends `` `corpus/lessons/round-12.md`. `` with no LF; HEAD is base bytes + `\n\n## Round 13 …`. `HEAD.startswith(base)` is True. A split-line difflib sees no change at all, so line-split tools are blind here; git hunks flag it.
3. **Insertion positions are not tail-only.** SCORECARD.md has a mid-file insertion (`@@ -162,0 +163 @@`) plus a tail block (`@@ -240,0 +242,101 @@`). A "base is prefix of new" check fails on SCORECARD although it is pure insertion. LOG.md is a true prefix (`@@ -473,0 +474,137 @@`).
4. **r12 notices are the only r12 edits** (`root-dac-decision-r12.md`): hunk `+7,6` (header blockquote "Superseded after outside rejection") and `+129..160` (`## Round-13 correction …`). `root-dac-decision-r12.json`: two top-level keys inserted before `schema` (`superseded_by`, `correction_notice`). Removing those keys leaves the 70fede2 ordered pairs exactly (order-preserving check True). Dict equality would also pass but ignores order.
5. **r13 MD:97 is pinned bytes.** `corpus/knowledge/root-dac-correction-r13.md` line 97 still reads "…strict is the only value that covers the hierarchy (S041); the value set is not exhaustive." The R14 repair must be an appended notice; editing line 97 is a replacement, which the contract forbids.
6. **Non-notice appends already exist in history.** A "notice-only" rule would reject these at r13 HEAD: `corpus/lessons/round-12.md` `## Gate — measured integration` (+38 at 134–171); `corpus/SOURCES.md` search-log paragraphs at 75–80 ("Additional S027 section check", "Round-13 correction source re-open", "Draft correction"); `SKILL.md` `## Round 13 …` section (+1716..1753); LOG entries (ledger class).
7. **Stale active pointers in baseline lines.** Edits in place are forbidden, so each needs an appended notice: `PROVINCE.md:92–93` ("the active refinement is now root-dac-correction-r13.md"); `corpus/README.md` `## Round 13 — correction superseding…` table; `SKILL.md` round-13 section; `corpus/knowledge/snapper-eacces-mechanism.md:93–105` erratum; `root-dac-decision-r12.md` header notice (points to r13). `root-dac-correction-r13.json` has no `superseded_by` key yet; `supersedes` is an object, so a new `superseded_by` key is additive.
8. **Attribution phrase sites (baseline).** "self-described model-generated automated triage": `corpus/SOURCES.md:48` (S042 row, #8047 — the unsupported transfer; body of comment 6071740243 does not self-describe), `:49` (S043 row, #6629 — supported by "This review is by Claude Opus 5.5 alone"), `corpus/lessons/round-13.md:68–70` (baseline), `round-13-verifier-spotcheck.md:156–163` (the critique itself, must not be edited). `corpus/QUALITY.md` criteria 17–18 at 23–25 (baseline) — check wording before citing.
9. **Live-tree drift.** After my first status (clean), a peer left an uncommitted `M corpus/QUALITY.md` (+3, R14 criteria 19–20). Any checker must read committed candidate revisions, not the worktree, or record worktree blob hashes.

## Recommended design: content-preservation comparison
Inputs: `R0` (pinned baseline commit), `R1` (committed candidate commit), manifest of files with `R0` blob sha256.

Step 1 — byte floor per manifest file. Parse `git diff -U0 R0 R1 -- F`. Every hunk must have old-count 0 (`-a,0`). Only exception: EOF-no-LF, where `R0` lacks a final LF and `R1` bytes `startswith` `R0` bytes. Do not use difflib on split lines.

Step 2 — classify every inserted hunk. A hunk must fall wholly inside one class, else it is UNCLASSIFIED (fail):
- (a) EXPLICIT-NOTICE: contiguous block starting with a fixed sentinel from the spec (e.g. `> **Superseded`, `## Round-14 — …`, `## Erratum (… round 14)`), naming a correction id that exists in the R14 correction JSON and a supersedes path.
- (b) JSON-ADDED-KEY: `.json` only. Keys in `R1` minus keys in `R0` must be a fixed allowlist (`superseded_by`, `correction_notice`, plus R14 names). Remove them; ordered `object_pairs_hook` pairs must equal `R0`; remaining values deep-equal.
- (c) LEDGER-ROW (needs main-agent decision, see below): `S\d{3}` rows and LOG headings keyed by ID. Existing keys byte-identical; new keys only; count delta = number of new IDs; position may be mid-file.
- (d) HISTORICAL-ADDENDUM: pre-R14 non-notice appends (list in evidence item 6), accepted only by an explicit commit-hash allowlist, never by pattern.

Step 3 — invariants independent of diff shape: S001–S043 rows byte-identical to `R0`; QUALITY criteria 1–18 text unchanged; `root-dac-correction-r13.md` line 97 bytes unchanged; LOG `R0` prefix; r12 MD/JSON bytes preserved as in Step 1.

Step 4 — output per file: hunk count, pure-insertion count, class per insertion, unclassified count (must be 0), EOF-artifact count, `R0`/`R1` blob shas. The checker proves preservation and shape only; it does not prove the inserted text is source-true (that remains the source/outside reviewers' job, and the r13 closure's MD:97 defect shows why).

## Decisions for main agent
- The stated exclusion set (notices + additive JSON keys) would reject the required R14 deliverables: S044/S045 rows, LOG entry, QUALITY 19–20. Recommend sanctioning class (c) explicitly, or stating that required new records are out of this checker's scope.
- Recommend deciding class (d) as a frozen allowlist before the R14 checker runs, not by inspection after failure.
- Recommend the R14 candidate be committed before the checker runs, since the worktree is shared.

## Limitations
- Analysis pinned to `8606bad`; did not check uncommitted peer edits beyond noting `QUALITY.md`.
- Dry-run results are design evidence only; they are not the lane gate and not a verdict on R14 content.
- `.ufo/waves/` artifacts were not classified (wave-local, outside corpus scope).

## Tooling
Installed or updated: none. Used system `git` and stdlib `python3` (eval kernel). No package or privileged action.
