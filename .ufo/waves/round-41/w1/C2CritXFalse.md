VERDICT: defect-found

## Counterexample

A rule row that asserts the opposite of its frozen proposition still passes every lexical gate: with
PA2, PA4, PA6 and PA8 written as four affirmative falsehoods and eight all-holds verdict files that say
in their body they are not reviews, `tools/check-package-anatomy-r41.py` returns `PASS`, exit 0,
`rules_verified 8`, `verdicts_ok 8`, `host_ok 6` (receipt `06-combined-false.json`, revision
`20cfe55d`). The counter's own
docstring concedes that lexical checks are shape gates (`tools/check-package-anatomy-r41.py:17-22`,
"the verdict files are the read, the lexical checks are shape gates"), so the new finding is the second
half: the verdict gate is not a read the entry author cannot write, so the whole predicate is reachable
with four false rules and zero review.

## What I ran

Scratch clone of the lane at `71851d636ab1bffaf8fee5016617c88878a666f1` (clone under
`/fast/scratch/hyaku/tsukuroi-r41/C2CritXFalse/fx.Y9AV4E`, `origin` removed, toplevel verified, identity
`fixture <fixture@shokunin.local>`, every probe commit on `master`). Counter digest verified equal to the
declared one before use: `sha256sum tools/check-package-anatomy-r41.py` =
`c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`.

Every run: `python3 tools/check-package-anatomy-r41.py --repo "$D" --revision <sha>`, from the lane's own
counter (frozen snapshots read from `.ufo/waves/round-41/frozen/`, read-only). Thirteen scoring runs plus
one timing repeat; a run costs 148 ms wall (git reads only, no selftest), so the C1 run budget does not
apply here.

| # | commit | content | result | exit | rules | verdicts |
|---|---|---|---|---|---|---|
| 01 | `22115f66` | control: entry unchanged + 8 fixture verdict files | PASS | 0 | 8 | 8 |
| 02 | `b6b6f7f9` | PA2 false | PASS | 0 | 8 | 8 |
| 03 | `7c6a450d` | PA4 false | PASS | 0 | 8 | 8 |
| 04 | `32de3744` | PA6 false | PASS | 0 | 8 | 8 |
| 05 | `663dcf43` | PA8 false | PASS | 0 | 8 | 8 |
| 06 | `20cfe55d` | all four false at once | PASS | 0 | 8 | 8 |
| 07 | `d7af80b0` | PA8 inversion with relation 1 dropped | FAIL | 1 | 7 | 8 |
| 08 | `8df9af32` | PA4 mapping swap `.INSTALL`->`changelog` | FAIL | 1 | 7 | 8 |
| 09 | `f1925826` | **true** PA2 rule phrased with "without" | FAIL | 1 | 7 | 8 |
| 10 | `3f2a3ca0` | PA8 value cell changed | FAIL | 1 | 7 | 8 |
| 11 | `b119696f` | PA6 false rule + false host-cell addendum | PASS | 0 | 8 | 8 |
| 12 | `71851d63` | lane tip (true entry), no verdict files | FAIL | 1 | 8 | 0 |
| 13 | `7f1d1382` | four false rows, fixture verdicts removed | FAIL | 1 | 8 | 0 |

Verdict fixture used in runs 01-11: `.ufo/waves/round-41/w1/C2RevPA{1..8}GuardFixt.md`, first line
`VERDICT: holds`, body: "Synthetic all-holds fixture written by seat C2CritXFalse (item C2-18) in a
scratch clone ... It is not a review: row PA<n> was not checked by a reviewer here." The counter credited
all eight (`verdicts_ok 8`), i.e. it does not read the body (see defect below).

## The four false rows (verbatim cell text) and why each is false

Each variant changes the rule cell only: the value cell, the source cell (S-id, cited range and quote) and
the host cell are byte-identical to the entry at `71851d63`; run 11 additionally falsifies the PA6 host
cell, as marked there. `14-variants.patch` is the whole diff.

PA2 (run 02/06, `b6b6f7f9`, `20cfe55d`):
> When libalpm loads a package file, only `.PKGINFO` sets the metadata flag according to the comment,
> while the loader accepts any dot file as metadata; a file whose archive lacks `.PKGINFO` loads normally
> and `missing package metadata` is printed only as a warning, an empty name or version loads, and a
> version string lacking a dash loads, while `.MTREE` is read only on a full load to build the file list
> and `.BUILDINFO` is passed over like every other unhandled dot file

False at three places: `config = 1` is set only inside the `.PKGINFO` branch
(`.ufo/waves/round-41/frozen/src/be_package.c:598-618`); an absent `.PKGINFO` ends in
`goto pkg_invalid` (`be_package.c:652-655`); empty name, empty version and a version with no dash each
`goto pkg_invalid` (`be_package.c:605-616`). The counter keeps the row because RELATIONS only require the
literals `only .PKGINFO`, `.PKGINFO ... missing package metadata`, `.MTREE ... full load`,
`.BUILDINFO ... passed over` in that order; nothing binds "fails"/"loads".

PA4 (run 03/06, `7c6a450d`, `20cfe55d`):
> During install libalpm stores three root members inside the local database entry `<name>-<version>/`:
> `.INSTALL` becomes `install`, `.CHANGELOG` becomes `changelog` and `.MTREE` becomes `mtree`, each with
> mode 0644, and every other root dot file, `.PKGINFO` and `.BUILDINFO` included, is skipped and kept for
> future use; the entry also keeps `.PKGINFO` as `desc` beside them so the package name reads back

The added clause is false and contradicts the pinned clause in the same cell: `extract_db_file` maps only
the three names, then `else if(*entryname == '.')` logs "skipping extraction" and returns before
`archive_entry_set_perm(entry, 0644)` (`.ufo/waves/round-41/frozen/src/add.c:174-186`); `desc` is written
from the in-memory `info->desc`, never from the archive's dot file
(`.ufo/waves/round-41/frozen/src/be_local.c:994-1011`), and the frozen host capture shows 0 of 1409 local
entries carry a dot-named file (`hostcap/localdb-anatomy.tsv`). PA4 is the strongest of the four rows:
its mapping literals are pinned, so a swap fails (run 08), and only an additive falsehood passes.

PA6 (run 04/06, `32de3744`, `20cfe55d`):
> `pacman -Qkk` (check level 2) runs `check_pkg_full`, which opens the kept local `mtree`; when that file
> is absent the check aborts the remaining package checks and returns 0, so every file of such a package
> is reported as missing yet the package adds zero errors, while `-Qk` (level 1) runs the fast check and
> compares file sizes as well as existence

False: the absent-mtree path prints the notice and `return 0` *before* the file loop
(`.ufo/waves/round-41/frozen/src/check.c:314-320`), so nothing is reported and nothing is aborted — the
per-target loop continues after `display()` returns (`.ufo/waves/round-41/frozen/src/query.c:438-447`,
`:502-508`). Level 1 calls `check_file_exists` and adds a directory/file-type comparison only
(`check.c:270-281`, `:29-49`); size and checksum are never compared there, so "compares file sizes as
well as existence" is false.

PA8 (run 05/06, `663dcf43`, `20cfe55d`):
> libalpm compares two full versions by comparing the release first, then the epoch, and only afterwards
> the version; the documented order is the epoch first, then the version, and the release only when both
> strings carry one, an absent epoch counting as 0 so any epoch 1 build outranks every epoch 0 build,
> while `1.0` equals `1.0-5` and `2.0-1` outranks `1:1.0-1`

False twice: the code compares epoch, then version, then release-if-both
(`.ufo/waves/round-41/frozen/src/version.c:249-255`), and `2.0-1` does not outrank `1:1.0-1` — observed
`vercmp 2.0-1 1:1.0-1` = `-1`, `vercmp 1:1.0-1 2.0-1` = `1`, `vercmp 1.0 1.0-5` = `0` (host pacman
7.1.0.r9.g54d9411-3). It passes because the true sentence survives as a subordinate clause ("the
documented order is ...") after the false one; RELATIONS are order-preserving literals, not uniqueness
constraints.

Note on the item's examples: "only .MTREE sets the metadata flag" cannot be realized while keeping
RELATIONS PA2[0] = `\bonly \.PKGINFO\b`; the inversion has to be carried by a second clause, exactly as
above. "the release first, then the epoch" likewise needs the true literal retained.

## Which pass, which fail, and why

Pass (false, affirmative, relations intact): 02, 03, 04, 05, 06. All eight rows verify; only the verdict
gate differs from the lane-tip failure.

Fail, and the exact reason the counter reports:
- 07 `['relation unmet: \\bthe epoch first\\b.*\\bthen the version\\b.*\\bthe release only when both\\b']`
- 08 `['relation unmet: \\.INSTALL becomes install\\b']`
- 09 `["rule carries negation word 'without'"]` — this is a **true** rule rejected for its wording; the
  NEG gate is a false-negative machine. [INFERENCE] the same word list would also reject a rule that
  says "no .MTREE file is kept".
- 10 `["value 'release, then epoch, then version' != derived 'epoch, then version, then release when both
  carry one'"]` — the value cell is an exact key, the one gate that does bind ordering.
- 11 PASS, `host_ok 6`: the host cell only needs the captured substrings to be contained
  (`all(x in hc)`), so a false sentence appended after them is invisible; PA6's host cell read
  "... mtree 1409 of 1409 entries (`localdb-anatomy.tsv`); additionally, every kept mtree was opened and
  every file of all 1409 packages was reported missing" and the counter passed it.

Gate map: value cell = exact key (bites); RELATIONS = ordered literal pairings (bites mapping swaps and
dropped clauses; blind to polarity and to added clauses); NEG = word blacklist (bites true statements);
12-word floor, quote-inside-window, S-id/upstream registry, novelty grep = strings; host cell =
containment; verdicts = first-line string + row id in body.

## The defect (the verdict gate)

Run 13 is the isolating control: the four false rows are still `verified: true` for all four
(`rules_verified 8`), and the predicate fails only because `verdicts_ok == 0`. Run 01 is the converse:
the *unmodified* true entry plus eight files I wrote myself reaches `verdicts_ok 8` and PASS. The counter
reads only the first line and checks that the row id appears somewhere in the body
(`tools/check-package-anatomy-r41.py:269-287`); it has no reviewer identity, no author check, no
ledger, no signature. So `verdicts_ok` measures "eight files exist", not "eight non-author readers
agree" — QUALITY 81's "non-author verdict" is unenforced by the implementation, and the entry's own
author can satisfy the whole predicate with four false rows (run 06, PASS exit 0).

This is a fixable defect, not a tradeoff: the lexical-shape tradeoff is declared in the docstring, the
forged-read is not.

## Impacted axes

- C2 depth / `rules_verified`: counts shape only; a row asserting the negation of its proposition scores.
  It must never be reported as "the rule is true".
- C2 depth / `verdicts_ok`: satisfiable by the author's own commit; `PASS` therefore does not certify a
  reviewed entry.
- `host_ok`: containment, not equality; a false addendum is free.
- QUALITY 81 ("non-author verdict per row"): the counter cannot see authorship.

Nothing here changes what the entry itself says at `71851d63`; this is about what a PASS certifies.

## Smallest safe correction

Inside the frozen round nothing may change in the counter; the correction is a residual for round 42 and
a reading rule for this round: **a verdict file must be read in full, and its body must name the
reviewer and the proposition checked; a file whose body disclaims review must be treated as absent.**
The eight files above would have been rejected by that rule and run 06 would be FAIL.

For round 42, cheapest first:
1. Verdict authenticity: require line 2 `REVIEWER: <id>` and a committed ledger
   `.ufo/waves/round-41/reviewers.json` mapping row -> reviewer; the counter requires the id to appear in
   the ledger and requires `git log --format=%ae` on the verdict file's introducing commit to differ from
   the entry's author. (Three `git log` calls; no new authority.)
2. Row-local unicity for the rows I broke: `rc.count('.PKGINFO') == 1` (PA4);
   `rc.count('first') == 1` and no `release first` (PA8); require `fails with` adjacent to the
   `.PKGINFO`/missing-metadata pair and forbid `loads normally` (PA2); forbid `aborts`,
   `reported as missing`, `file sizes` (PA6). These are examples, not a theory of truth — an adversary
   finds the next added clause, which is why (1) is the real fix.
3. If `host_ok` is meant to certify the host reading, compare equality (or a per-row required exact
   sentence) instead of containment.

## Not done, limits

- Did not run the C1 counter, did not read lane content beyond the sources cited, did not modify the
  lane (the pre-existing dirty state in the lane worktree — `M tools/check-self-assessment.py`, untracked
  `.ufo/waves/round-41/w1/` and dispatch files — was already there and is not mine).
- The PASS results are on scratch revisions in a clone; at probe time the lane had no verdict files at
  `71851d63` (`git ls-tree 71851d63:.ufo/waves/round-41/w1` fails), so run 12 is what that revision
  scores.
- No host mutation, no package transaction, no tool installed. Nothing was judged, admitted or shipped.
- Scratch clone and receipts: scratch removed after copying; receipts under
  `.ufo/waves/round-41/w1/C2CritXFalse/` (`01`-`13` JSON, `14-variants.patch` = the four false rows as a
  diff from the control commit, `15-verdict-fixture-template.md`, `MANIFEST.txt`).
