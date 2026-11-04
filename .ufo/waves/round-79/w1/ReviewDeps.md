review_sha256=0c2dd4ad601e179110df546ec4933f2b3e8249e462a548db8263cbf5da1c8168
claim=C1
verdict=DP1 holds
verdict=DP2 holds
verdict=DP3 holds
verdict=DP4 holds
verdict=DP5 holds
verdict=DP6 holds
verdict=DP7 holds
verdict=DP8 holds
blocked=none
first_review=ReviewDeps/review-first.md (sha256 c58d84283d64aaf37fb3efd0a72e59a0c82f372be9e6e83f7591be796154c850; DP6 partly-holds)
claim_status=C1 remains a declared miss: corrected data no longer equals before/expected.json (finite-content-mismatch), independent of this review

# ReviewDeps — second review on the corrected C1 bundle

Second review, 2026-11-04 16:24 -0300, on the bytes the L1 corrected after the
first review (preserved unchanged at `ReviewDeps/review-first.md`).

Bound bytes:

- `data.json` sha256 `1b8f833df5d8138b63b0a9c57fef138d9613679ce62aae28acdc04021cc37d5a`
  (3974 B; only DP6's `statement` changed against `before/expected.json`; all other
  rows, quotes, lines, digests identical; quote word counts 20/24/23/15/16/21/18/17).
- `note.md` sha256 `8c6b3809aca948ccd1080692e71be50d0689870cdae6082cce40dc53d437eaca`
  (254 lines).
- Snapshot sha256 `eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6`
  and `before/expected.json` sha256 `0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21`
  recomputed from disk and matching the frozen values.

**Landing must be byte-identical to these two digests.** Any later edit voids this
review and needs another pass.

## Quote location (independent, counter's rule)

Each quote occurs exactly once in the tag-stripped token stream and computes to its
recorded range: DP1 666-667, DP2 690-692, DP3 713-715, DP4 736-737, DP5 765-766,
DP6 783-785, DP7 937-939, DP8 857-858.

## Row verdicts on the corrected bytes

- **DP1 holds** (snapshot 665–668): condition, validity consequence and `this unit will
  still be started` all kept; plural→singular distributive.
- **DP2 holds** (688–692): both branches of the quoted sentence kept; the preceding
  failure-to-activate rule is not claimed.
- **DP3 holds** (713–717): both halves kept; ordering caveat not claimed.
- **DP4 holds** (733–737): `Beyond Requires=` carries the Requires= effects; `stops`
  narrows `does so` rather than overclaiming.
- **DP5 holds** (763–767): complete sentence; one-way clause is the next sentence and
  no bidirectionality is claimed.
- **DP6 holds now** (783–785): the corrected statement reads "While the configuring
  unit is up, listed units found inactive or failed are started when no job is queued
  for them." The source sentence continues past the quote's comma with "and no job is
  queued for them." (line 785); the statement now carries that precondition, so it no
  longer asserts a broader trigger. The row's quote cell is still the truncated span,
  but the qualifier is inside the recorded line range and the companion quotes it
  (`note.md:110-113`); the statement is supported by the located text.
- **DP7 holds** (936–939): both dependency types kept; plural `paths` follows the
  directive's own argument domain; `noauto` is a separate paragraph.
- **DP8 holds** (855–859): claims only the named common pattern; the ordering
  consequence is not claimed.

## First-review findings and their disposition

The first review found DP6 partly-holds (dropped `and no job is queued for them`) and
seven companion defects (F1–F7). On the corrected bytes:

- DP6: **repaired**. The statement now carries the clause; verified word by word
  against 783–785.
- F1 `RequisiteMountsFor=` → **fixed** at `note.md:152` (`WantsMountsFor=`), consistent
  with the cited-lines bullet at `:173`.
- F2 order sentence → **fixed** at `note.md:74-78`: "Before=/After= do not pull anything
  in; ordering is configured with them, and requirement dependencies do not substitute
  for it."
- F3 registry-tail claim → **repaired** at `note.md:159-161`: now scoped ("At the
  round-79 review revision corpus/SOURCES.md ends at S328; the S329 row is appended in
  the same integration step as this note"). True at this review revision (328 rows,
  S329 absent). Integration condition: S329 must be appended in the same step, or the
  sentence becomes false.
- F4 whole-manual negative → **partly repaired** at `note.md:93-95`: scope is now named
  ("The sweep is limited to that entry, not the whole manual"), but no command/date is
  given and the QUALITY 9 bullet still enumerates only two negative readings. Residual
  minor: name the bounded read/command and date, or add it to the QUALITY 9 list.
- F5 DP6 gloss → **fixed** at `note.md:110-113`: "the uphold check acts only when no job
  is already queued for the unit. It does not say that no job results."
- F6 QUALITY 66 count → **fixed** at `note.md:219-236`: the bullet now says the landed
  set keeps its branches, names DP6 as the corrected row, and treats DP2/DP5/DP7/DP8's
  adjacent clauses as carried in (d)/(c) rather than as row gaps. The stale DP1
  `:665-667` cite is gone.
- F7 → **fixed** (same bullet).

No material companion defect remains. Residual (minor) items: F4's command/date; and the
DP6 `quote` cell still ends before the qualifier although the statement now carries it
(supported by line 785 and (d); under the 25-word cap a span such as "all units listed
in Upholds= are started whenever found to be inactive or failed, and no job is queued
for them." would show the clause directly — a recommendation, not a defect).
DP4's restart branch is carried by "Beyond Requires=" rather than repeated; held.

## C1 status — not rescued by this review

The corrected `data.json` differs from `before/expected.json` in DP6's statement, and
`tools/measure-unit-deps-r79.py` (lines 92–132) checks exact content equality before the
review (`finite-content-mismatch` at :98). So the frozen C1 predicate reads
`rows=0 ... reason=finite-content-mismatch` at this revision, independent of the review
map. My all-`holds` verdict does not change that: the miss is a frozen-instrument
consequence of correcting DP6, exactly as the companion records (`note.md:219-229`).
C1 stays a declared miss this round.

## Limits

No gate or selftest executed (read from source, not run). S329 is absent from
`corpus/SOURCES.md` at this review revision (328 rows), so the registry leg of C1 is
unverified here. Landing copies under `corpus/knowledge/` do not exist yet. No LSP
server mounted. No installed-build or live-state claim made or checked.

## Execution record

Read-only: `sha256sum`; `python3` heredocs (JSON/regex reads); `grep`; `awk`/`sed` line
windows. One disclosed deviation from the original read-only list: the L1's follow-up
instructed "first copy your current review to review-first.md", so `cp -p review.md
review-first.md` was run inside this seat's own directory (bytes verified identical by
sha256 c58d8428…). No gate, no selftest, no other mutation, no git/jj, no tool install,
no scratch tree. Writes: this report, `ReviewDeps/{verdict.json,review.md,review-first.md}`.

Report: .ufo/waves/round-79/w1/ReviewDeps.md
