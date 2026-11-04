# ReviewDeps — second review on the corrected bytes (C1)

Bound at 2026-11-04 16:24 -0300:
`data.json` sha256 `1b8f833df5d8138b63b0a9c57fef138d9613679ce62aae28acdc04021cc37d5a`,
`note.md` sha256 `8c6b3809aca948ccd1080692e71be50d0689870cdae6082cce40dc53d437eaca`.
The landing copies must be byte-identical; a later edit voids this review.
The first review, which found DP6 partly-holds and defects F1–F7, is preserved
unchanged at `review-first.md` (sha256
`c58d84283d64aaf37fb3efd0a72e59a0c82f372be9e6e83f7591be796154c850`).

## What changed in the data

`data.json` parsed content differs from `before/expected.json` in exactly one field:
DP6's `statement`, now "While the configuring unit is up, listed units found inactive
or failed are started when no job is queued for them." Every other row, quote, line,
digest and the row order are unchanged. All eight quotes still locate uniquely at their
recorded ranges under the counter's token rule.

## Per-row judgement on the corrected bytes

### DP1 — holds

Source 665–668: "Units listed in this option will be started if the configuring unit
is. However, if the listed units fail to start or cannot be added to the transaction,
this has no impact on the validity of the transaction as a whole, and this unit will
still be started." The statement keeps the condition, the validity consequence and the
outcome; plural→singular is distributive.

### DP2 — holds

Source 688–692: the quoted sentence ("Besides, with or without specifying After=, this
unit will be stopped (or restarted) if one of the other units is explicitly stopped (or
restarted).") is complete; both branches are kept. The preceding failure-to-activate
sentence is a different proposition, now carried in (d).

### DP3 — holds

Source 713–717: both halves of "they will not be started and the starting of this unit
will fail immediately" are kept; the ordering caveat is not claimed (and is in (d)).

### DP4 — holds

Source 733–737: "Beyond Requires=" carries the Requires= effects (including the
restart branch); "stops" narrows "does so" rather than overclaiming. Held in the first
review, unchanged here.

### DP5 — holds

Source 763–767: the quote is the complete sentence; the one-way clause is the next
sentence and the statement claims no bidirectionality.

### DP6 — holds (corrected)

Source 783–786: "Configures dependencies similar to Wants=, but as long as this unit is
up, all units listed in Upholds= are started whenever found to be inactive or failed,
and no job is queued for them." The row's quote still stops at "failed," but the
statement now carries "when no job is queued for them", which is the source's
precondition on line 785 inside the recorded line range. Word by word: "While the
configuring unit is up" = "as long as this unit is up"; "listed units found inactive or
failed are started" = "all units listed in Upholds= are started whenever found to be
inactive or failed"; "when no job is queued for them" = "and no job is queued for
them." No broader trigger remains. The companion's (d) quotes the clause
(`note.md:110-113`).

### DP7 — holds

Source 936–939: both dependency types are kept; "the specified paths" follows the
directive's argument domain ("space-separated list of absolute paths", 936–937); the
`noauto` paragraph (941–944) is separate and not claimed.

### DP8 — holds

Source 855–859: the quote ends mid-sentence but the statement claims only that the
manual names the combination as a common pattern; the ordering consequence is not
claimed (and is in (c)).

## Companion fixes verified

- F1: `note.md:152` now reads `WantsMountsFor=`; the snapshot has no
  `RequisiteMountsFor` string (grep count 0). Consistent with `note.md:173`.
- F2: `note.md:74-78` now reads "Before=/After= do not pull anything in; ordering is
  configured with them, and requirement dependencies do not substitute for it", followed
  by the two exact quotes. Correct subject.
- F3: `note.md:159-161` now scopes the registry-tail fact to the review revision and
  states that S329 is appended in the same integration step. True at this revision
  (328 rows, S329 absent). Integration must append S329 in the same step.
- F4: partly repaired — scope named ("The sweep is limited to that entry, not the whole
  manual", `note.md:93-95`), but no command/date and the QUALITY 9 bullet still lists
  only two negative readings. Residual minor.
- F5: `note.md:110-113` now states the precondition reading and that no job-result
  claim is made.
- F6: `note.md:219-236` now says the landed set keeps its branches, names DP6 as the
  corrected row, and no longer counts DP2/DP5/DP7 as narrower than their quoted
  sentences. The stale DP1 ":665-667" cite is gone.
- F7: fixed with the same bullet.

No material companion defect remains. Residual minor items: F4's command/date; the DP6
`quote` cell still ends at "failed," although the statement now carries the qualifier
(supported by line 785 and (d); a 23-word span such as "all units listed in Upholds=
are started whenever found to be inactive or failed, and no job is queued for them."
would show it directly — recommendation only). DP4's restart branch is carried by
"Beyond Requires=" rather than repeated; held.

## C1 status

`tools/measure-unit-deps-r79.py` (lines 92–132) compares the data to
`before/expected.json` before reading the review (`finite-content-mismatch` at :98).
Because the corrected DP6 statement differs from the frozen tuple, the predicate reads
`rows=0 ... reason=finite-content-mismatch` at this revision; the all-`holds` review map
does not change that. C1 remains a declared miss this round — the correction is corpus
quality work, not a rescue. The companion states the same (`note.md:219-229`).

## Limits

No gate or selftest executed; counter behaviour read from source, not observed. S329 is
absent from `corpus/SOURCES.md` at this revision (328 rows); the registry leg of C1 is
unverified here. Landing copies under `corpus/knowledge/` do not exist yet. No LSP
server mounted. No installed-build or live-state claim made or checked.

## Execution record

Read-only: `sha256sum`; `python3` heredocs (JSON/regex reads); `grep`; `awk`/`sed` line
windows. One disclosed deviation from the original read-only list: the L1's follow-up
instructed copying the first review to `review-first.md`, so `cp -p review.md
review-first.md` was run inside this seat's own directory (bytes verified identical,
sha256 `c58d8428…`). No gate, no selftest, no other mutation, no git/jj, no tool
install, no scratch tree. Writes: this file, `verdict.json`, `review-first.md`, and the
report only.
