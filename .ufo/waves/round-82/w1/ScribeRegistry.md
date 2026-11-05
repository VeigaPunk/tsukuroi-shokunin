# Seat ScribeRegistry — round-82 w1

Verdict: the two named deliverables are written and verified. The three registry rows and the
two QUALITY criteria are in the lane working tree; the L1 landed them at `8111113c`, and a later
L1 commit `804dc4cb` (measured outcome) sits on top, so the rows are committed. My two refinements
(one clause in the C2 row, one wording precision in criterion 113) are still uncommitted in the
working tree for the L1; coverage at `804dc4cb` is `PASS findings 0 registered 125 == tools_total 125` rc 0.

## 1. The three registry rows (verbatim, `SKILL.md:5909-5911`)

Appended to the sole operative table, `## Gate and probe registry — round71 superseding current
rows` (heading at `SKILL.md:5777`, header row at `:5785`), immediately after the `measure-round81`
row. Eight columns, same shape as the newest rows; no other row touched.

```
| check-anchor-coordinates | gate | `python3 tools/check-anchor-coordinates.py --revision <REV>` (or `--fixture <DIR>`) | 0 met (every MT row's cited `lines` IS the located raw span); 1 unmet (a cited range that merely contains the quote does not count); 2 could-not-evaluate (entry or snapshot absent at the bound revision); 3 self-test failed (--selftest) | `python3 tools/check-anchor-coordinates.py --selftest` — twelve hermetic cases; prints `SELFTEST total=12 passed=12 failed=0` | Round-82 C1; the eight `MT` rows of `corpus/knowledge/mount-unit-fstab-plane-r81.json` against the pinned snapshot `.ufo/waves/round-81/before/src/`; the per-line strip keeps index i = raw line i+1, so a cited number is a raw file line; instrument sha256 `fedd45ce…c3b3`; counts anchor exactness, not that a quote supports its statement | committed reads at the bound revision; the selftest uses one `$TMPDIR` root | tsukuroi |
| mutation-kill-r82 | gate | `python3 tools/mutation-kill-r82.py --revision <REV>` (or `--work <DIR>`) | 0 met (`killed >= 24 / 26` and `genuine_killed == 17 / 17`); 1 unmet; 2 could-not-evaluate (recipes absent, or a pristine baseline whose own `--selftest` is red); 3 self-test failed (--selftest) | `python3 tools/mutation-kill-r82.py --selftest` — four hermetic cases; prints `SELFTEST total=4 passed=4 failed=0` | Round-82 C2; 26 committed single-clause recipes in `.ufo/waves/round-82/before/mutants-r82.json` sha256 `5e176afc…cb43`, 17 of them `genuine_gap`; a mutant is killed only when its own `--selftest` exits non-zero, so the count is a selftest-coverage measurement and not a proof that the counter is correct; a recipe whose `old` string no longer occurs in the tool is not a kill; the two equivalent recipes (C06, C07) are excluded from the genuine leg; instrument sha256 `6e6d9715…7c24` | committed reads at the bound revision; each mutant runs in its own scratch directory under `$TMPDIR`, removed at exit | tsukuroi |
| check-scorecard-ordinals | gate | `python3 tools/check-scorecard-ordinals.py --revision <REV>` (or `--fixture <PATH>`) | 0 clean (0 findings); 1 findings (two standing blocks disagree on one after-ordinal); 2 could-not-evaluate (no round blocks); 3 self-test failed (--selftest) | `python3 tools/check-scorecard-ordinals.py --selftest` — eight hermetic cases; prints `SELFTEST total=8 passed=8 failed=0` | Round-82 C3; one after-ordinal per (round, axis) across the `## Round N` blocks of `SCORECARD.md`; a block retires an earlier assertion only through a machine-readable `supersedes-ordinal: round-N axis` line, so a correction that names nothing retires nothing; instrument sha256 `888a3da9…1e84` | committed reads at the bound revision; the selftest uses one `$TMPDIR` root | tsukuroi |
```

Each row names role `gate`, what it decides, the verdict map including `3 self-test failed
(--selftest)`, the self-test cell `python3 tools/<name> --selftest`, and its limits.

## 2. Registry-coverage output (pasted)

`python3 tools/check-registry-coverage.py --revision <REV>` reads committed blobs, so the
verification ran in a scratch clone at `/fast/scratch/hyaku/tsukuroi-r82/ScribeRegistry/clone`
whose `SKILL.md`/`corpus/QUALITY.md` are my files (fixture commit `1efd287c`; the lane index was
never touched — the fixture used `hash-object`/`update-index`/`write-tree`/`commit-tree` only).

```
$ python3 tools/check-registry-coverage.py --revision 1efd287c17baa36e269f5ec72cd3ae24047fdb6e
{"branch":"master","branch_tip":"1efd287c17baa36e269f5ec72cd3ae24047fdb6e","counts":{"findings":0,"missing":0,"registered":125,"rows_total":125,"tools_total":125},"findings":[],"revision":"1efd287c17baa36e269f5ec72cd3ae24047fdb6e","status":"PASS"}
rc=0
```

`findings 0`, `registered == tools_total == 125`, `missing 0`, exit 0.

Baseline for the same gate before my rows (lane `683ae456`, three new tools unregistered):

```
$ python3 tools/check-registry-coverage.py --revision 683ae4563bf6967ed0cc533aec06c971a1a87bbc
{"counts":{"findings":3,"missing":3,"registered":122,"rows_total":122,"tools_total":125},"findings":[
 {"id":"REGISTRY-ROW-MISSING","site":"tools/check-anchor-coordinates.py"},
 {"id":"REGISTRY-ROW-MISSING","site":"tools/check-scorecard-ordinals.py"},
 {"id":"REGISTRY-ROW-MISSING","site":"tools/mutation-kill-r82.py"}],"status":"FAIL"}
```

The same PASS also holds against the lane's own committed HEAD after the L1 landing:

```
$ python3 tools/check-registry-coverage.py --revision 8111113ce1402aad9923d0207ebe22a7760c90db
{"counts":{"findings":0,"missing":0,"registered":125,"rows_total":125,"tools_total":125},"status":"PASS"} rc=0
```

Adjacent gates re-run in the same fixture, unchanged by my edit:
`check-gate-standard-r79.py` → `duplicates=0 shape_ok=2/2 met=1` rc 0 (my three rows are not
duplicate tool paths); `check-cited-receipts-r62.py --round 82` → `PASS 0`; `check-r75-routed-r76.py`
→ `ROUTED_STALE=0 ROUTED_OK=8/8` rc 0; `check-line-endings-r64.py --check` → `PASS (413 file(s)
checked, 0 violation(s))`; `check-freshness-r17.py` → `findings []` rc 0; `check-selector-contract.py`
→ `PASS` rc 0.

## 3. The two QUALITY criteria (`corpus/QUALITY.md:221` and `:223`)

Appended as numbered entries 113 and 114 in the file's existing row format (bolded lead with a
rule id, blank-line separated, `Lesson:` pointer). Numbering stays sequential: the file now holds
114 entries, `1..114` with no gap.

> **113. A cited line number is a RAW file line, and an anchor instrument proves the span exactly,
> not merely containment (R82-RAW-LINE-ANCHOR):** the line number a corpus entry cites is the line
> number of the raw file as stored — never of a tag-stripped, reflowed or otherwise rewritten view —
> and the instrument that reads that anchor proves that the cited range IS the located span
> `[first,last]`, not that the quote falls somewhere inside the range. A range that merely contains
> the quote is a finding, not a pass, because a uniform shift keeps every quote inside its range:
> round 81's eight MT rows cited the tag-stripped index while the raw file sat two lines lower, and
> the round-82 no-work control at the lane tip reads `count 0 / target 8 / unmet` with all eight
> rows `cited-range-not-the-quote-span`; measured on the pinned snapshot, the quote's first line in
> the raw file is exactly two lines later than its line in the tag-stripped view for all eight rows.
> Red: `.ufo/waves/round-82/before/controls.txt` (C1 no-work at
> `d5b3e13492b3878fc8734368b0bbcab04f6c79c0`). Green: `tools/check-anchor-coordinates.py`
> (sha256 `fedd45ce…c3b3`) counts a row only when the cited pair equals the located pair, over a
> per-line strip whose index i is raw line i+1; its own red cases `shifted-two-lines`,
> `fabricated-quote`, `range-too-wide` all fail and `correct-span` passes. Lesson:
> `corpus/lessons/round-82.md` § Gate and § Mistakes.
>
> **114. An instrument is frozen with its no-work and red controls before any candidate is scored,
> and a correction to a self-assessment names the claim it supersedes on a machine-readable line
> (R82-FROZEN-CONTROLS):** the instrument's bytes, its predicate, its target, its kill rule, its
> recipe set and its controls are committed together before any candidate file of the round is
> authored, run or scored, so the no-work score is measured against the frozen instrument and never
> against a later rewrite; and a correction to a filed self-assessment names the claim it
> supersedes on one machine-readable line, so a reader and a counter agree on which block still
> stands — a correction that names nothing retires nothing and the finding stays. Round-82
> evidence: freeze commit `2786562e49d71e0b3962ad996397c010cf787b16` carries the three instruments,
> the 26 mutation recipes (sha256 `5e176afc…cb43`) and the control receipt
> `.ufo/waves/round-82/before/controls.txt`; the C2 no-work score at that commit is `killed 6 / 26`
> and `genuine 0 / 17` (rc 1), the C3 no-work score is one finding (round 81, depth `{8, 9}`, blocks
> at `SCORECARD.md:6861` and `:6903`, rc 1), and `tools/check-scorecard-ordinals.py` (sha256
> `888a3da9…1e84`) counts a `(round, axis)` as disputed only when two non-retired blocks disagree,
> retiring an assertion only on a `supersedes-ordinal: round-N axis` line. Lesson:
> `corpus/lessons/round-82.md` § Gate and § Mistakes.

Both name their lesson (`corpus/lessons/round-82.md`, § Gate and § Mistakes — that file exists,
`## Gate` at `:7`, `## Mistakes` at `:41`, written by seat ScribeLesson).

## 4. Debt the gates still report

- **C2 is unmet at the lane tip.** `python3 tools/mutation-kill-r82.py --revision 8111113c` →
  `killed 22 / 26`, `genuine_killed 16 / 17`, `finding unmet`, rc 1 (target `24/26` and `17/17`).
  Survivors: `C06-source-id-shape`, `C07-own-work-rejection` (both `genuine_gap: false`, the
  declared equivalent pair, excluded from the genuine leg), `C16-empty-manifest` (`genuine_gap:
  true`) and `M06-mutation-unlink-noop` (`genuine_gap: false`).
- **The two `old_occurs=0` recipes are an encoding mismatch, not surviving behaviour.** In
  `.ufo/waves/round-82/before/mutants-r82.json`, `C16-empty-manifest.old` and
  `M06-mutation-unlink-noop.old` carry the two characters `\n` where the tool source has a real
  newline (`repr`: `"if not digests:\\n        raise CannotEvaluate('snapshot-manifest-empty')"`).
  Decoded, the string occurs 0 times in the tool, so the counter records
  `recipe-missing:old-string-occurs-0x` and does not score the mutant. The round's own
  applicability receipt `.ufo/waves/round-82/after/c2-recipe-applicability.txt:31-34` re-writes
  each with a real newline and shows `old_occurs(real-newline)=1` and
  `mutant --selftest rc=3` for both — i.e. under a real newline both are killed. This is the
  executor/mutation seat's open item (the frozen recipe file is out of my write scope); I only
  record it and state the kill rule in the row.
- **C1 and C3 are met at the lane tip** (`check-anchor-coordinates.py --revision 8111113c` →
  `count 8 / target 8 / met` rc 0, all eight rows `exact: true`; `check-scorecard-ordinals.py` →
  `count 0 findings`, `examined 77`, `finding clean` rc 0). The C3 correction landed as the
  machine-readable line `supersedes-ordinal: round-81 depth` at `SCORECARD.md:7005`.
- **Inherited coverage debt, unchanged by this seat:** the round-81 C1 counter's own selftest kills
  3 of 18 single-clause mutants and the C2 table's case A is a string check a token-printing
  `--selftest` survives (`SKILL.md:6199-6207`, `SCORECARD.md` round-81 measured outcome).

## Boundaries observed

- Wrote only `SKILL.md`, `corpus/QUALITY.md` and this report. No lane commit, no `git add`,
  no worktree/index mutation: the lane index was never written (`git status` shows only ` M
  SKILL.md`, ` M corpus/QUALITY.md` for my files, plus the other seats' files).
- `corpus/SOURCES.md` and `corpus/lessons/round-82.md` were modified by seat ScribeLesson, not by
  me; I did not touch them.
- Scratch: `/fast/scratch/hyaku/tsukuroi-r82/ScribeRegistry/` (one `git clone` fixture plus small
  receipts), removed before this report was filed.
- No tool was installed or upgraded; no `pacman` transaction. No `/tmp` hardcoding observed in
  the three instruments (each uses `$TMPDIR` or its own `--fixture`/`--work`).

## Checks the L1 should run after landing

1. `python3 tools/check-registry-coverage.py --revision <new-tip>` → expect `status PASS`,
   `findings 0`, `registered == tools_total`.
2. `python3 tools/check-gate-standard-r79.py --revision <new-tip>` → expect `duplicates=0
   shape_ok=2/2 met=1`.
3. `python3 tools/check-cited-receipts-r62.py --revision <new-tip> --round 82` → expect `PASS 0`
   (my criteria cite `.ufo/waves/round-82/before/controls.txt` and `corpus/lessons/round-82.md`,
   both of which must exist as blobs at the landed revision).
4. `python3 tools/check-line-endings-r64.py --check` → expect 0 violations (both edited files are
   CR-free).
5. `python3 tools/check-selftest-tally.py --receipt <round-82 receipt> --label <TOKEN> --range
   <A>..<B> -- SKILL.md` — my rows print `SELFTEST total=12/4/8 passed=… failed=0`; the figures
   must match the round's final receipt lines. Note the shipped
   `.ufo/waves/round-82/before/controls.txt` records the three selftest figures as
   `SELFTEST total=12/4/8 passed=… failed=0` but not in the `PASS (N cases, N passed, N failed)`
   shape this sweep parses, so the sweep over that file reports `SWEEP: no receipt line
   [SWEEP-NO-RECEIPT]` (exit 2) — a receipt-shape mismatch in the round's control file, not a
   figure I wrote.
