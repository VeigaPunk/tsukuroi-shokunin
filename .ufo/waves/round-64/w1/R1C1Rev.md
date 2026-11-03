# R1C1Rev — C1-ATTACK report — 2026-11-03T18:41Z (UTC)

Preconditions met on first poll (2026-11-03T18:38:34Z): guard tool present (11859 B) and CR counts
0/0/0 — no waiting consumed. Full evidence receipt: `.ufo/waves/round-64/after/review-c1.md`.

## Frozen C1 predicate verdicts (all commands run by this seat)

- **(a) census: PASS** — `sources-census.sh validate --root <fleet> tsukuroi` → rc 0,
  E-code lines 0, W04 lines 42 (exact, disclosed), final line `ok … corpus/SOURCES.md`.
- **(b) identity: PASS** — `git show 2f3061ef:F | tr -d '\r' | cmp - F` silent rc 0 for all three
  files; proof attacked independently: blob stray-CR (mid-file / not-before-LF) = 0/0/0,
  worktree CR = 0/0/0, size-delta == CR-count per file (381 / 5452 / 4723), and
  sha256(blob|tr -d '\r') == sha256(worktree) ×3. Kill rule not triggered.
- **(c) guard: PASS** — `--selftest` → 5/5 cases PASS, rc 0 (includes CRLF kill + allowlisted
  `.ufo` capture); `--check` → `PASS (326 file(s) checked, 0 violation(s))`, rc 0.
- **(d) mutant: PASS** — CR appended as the LAST byte of SCORECARD.md in a scratch `--shared`
  clone (no trailing newline; od -c shows `d . \n \r`) → `--check` exit 1 naming
  `SCORECARD.md:4724: CR byte at offset 768591`.

**C1: 4/4 predicates PASS; no routed defect in the claim.**

## Guard holes / findings

- **F1 LOW (doc/code divergence):** docstring says `.ufo` must be a *leading* path component;
  code `ALLOW_DIR in parts` matches ANY component → a CRLF file at `corpus/.ufo/x.md` silently
  bypasses (demonstrated: `PASS (0 checked, 1 allow-listed)` rc 0). Zero exposure today
  (`git ls-files` nested-`.ufo` sweep under corpus|plans → 0 rows). One-line fix or docstring fix.
- **F2 INFO:** default-mode summary always reports "0 allow-listed" (skips pre-filtered in
  `guarded_set`); weakens that disclosure field.
- **F3 INFO:** LOG's SCORECARD before-count 4654/4701 is the 44fc183b figure; the declaration
  commit 2f3061ef itself added 69 CRLF lines (4723/4723 at the fix base). Receipt-accurate at its
  measurement time; (b) is defined against 2f3061ef and holds.
- **F4 INFO:** accidental positive control — `git checkout-index -f` restored the CRLF HEAD blob
  in the clone; guard flagged it (`corpus/SOURCES.md:1: CR byte at offset 35`, rc 1). It catches
  the real pre-fix state.

## Adversarial edges

- (a) `.ufo` allowlist skip: DISCLOSED behavior (header docs + "1 allow-listed" in summary) — not a hole.
- (b) guarded path → symlink into `.ufo/`: GUARD WINS — tracked path name decides; bytes read
  through the link; `corpus/SOURCES.md:1: CR byte at offset 15`, rc 1. Broken symlink at a guarded
  path counts as ", 1 missing", disclosed, not a violation.
- (c) empty file → clean PASS rc 0; binary+NUL no CR → PASS; binary+NUL+CR → FAIL named offset.
  No crash; no text/binary sniffing (guarded set is 100% text today — mime sweep receipted).

Residual: fix is worktree-only (3 M files + untracked guard tool) — L1 lands it; re-run §1–§4 of
review-c1.md after integration. Scratch /fast/scratch/hyaku/tsukuroi-r64/R1C1Rev deleted after
receipts were inlined here. Tools installed: none. No commits made.

Addendum 18:46Z: E1LineEnd fixed F1 (allowlist anchored to leading `.ufo`; nested
`corpus/.ufo/inner.md` now FAILs rc 1 — my re-probe) and F2 (default mode now prints a separate
`22370 allow-listed .ufo path(s) skipped` disclosure line — my re-run). (c)/(d) re-run by this seat
against the final tool sha 15f0e65c889acc3b591ca44c7e52fe16fa14d79c367e743ebcc905b17d50c030
(350 lines, matches E1's statement): selftest 5/5 PASS rc 0, lane --check PASS rc 0, EOF-CR mutant
FAIL rc 1 (`SCORECARD.md:4724: CR byte at offset 768591`). **All verdicts stand: C1 = 4/4 PASS on
the final tool.** Evidence: review-c1.md §9. A transient lane-side 381-CR state (18:43:21Z, ~3 s,
self-restored) was attributed to a mutate-and-restore probe cycle by another seat — not this seat
(clearance proof: review-c1.md §7).
