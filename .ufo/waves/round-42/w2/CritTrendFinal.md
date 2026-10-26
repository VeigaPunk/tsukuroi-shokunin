VERDICT: falsifies

# F-19 — trend verdicts for round 42 at `78abb8b5` (seat CritTrendFinal, critic, axis discernment)

Measured revision `78abb8b5cdc9da511b4fc523e661517a68dd33d3` (base `c8efaa3f`, freeze `a84fc9de`). Prior read:
`.ufo/waves/round-42/w1/CritTrend.md` (all three `unchanged` at `87c4f7c6`). Read-only: `read`, `grep`, `git show/log/diff/
cat-file/ls-tree`, `sed`, `python3` on committed JSON. No counter, no census selftest, no patch-offset run, no fetch, no
tool installed (nothing to record under the operator tooling directive). Scratch
`/fast/scratch/hyaku/tsukuroi-r42/CritTrendFinal` used and removed; receipts at
`.ufo/waves/round-42/w2/CritTrendFinal/receipts.txt`. No lane file other than this report and that receipts file was
written.

`improved` is false for all three trends at this revision. Expansion and discernment are `unchanged` on the round's own
bytes; quality is **`harmed`** by the letter of `LEARNING.md:34`, because the round's own 108-pin instrument flags a
drifted pin that this round's remedy then leaves unmarked. All three are one small commit away from the verdicts the
lane would rather report.

| Trend | Lane-available claim | Supportable at `78abb8b5` | Decisive basis |
|---|---|---|---|
| expansion | `improved` (deepening read) | `unchanged` | `corpus/README.md:412-413`, `PROVINCE.md:212-213`, `:234`, `:239-243`; entry `btrfs-scrub-record-r42.md:158`; no capability row |
| quality | `improved` (offset notes + corrections) | `harmed`; `improved` false, `unchanged` only if the lane denies the drift it marked | `r38:136` + `SKILL.md` pins unmarked against the round's own `out.json` row; `adjacency-anchors-r19.md:204,231` unswept |
| discernment | `improved` (QUALITY 90 landed) | `unchanged` (not claimable) | no non-author spot-check (`lessons/round-42.md:63`), zero wave-2 reports at the revision, criterion's lesson not in the revision (`QUALITY.md:177`) |

## Counterexample — the round's own 108-pin ledger is one short, and the missing row is an entry

The round's packaging-offset instrument reports **108 cited pins, 15 drifting**
(`.ufo/waves/round-42/w1/ConsiderPatchOffset/out.json`: 108 `cited` rows, 15 `risk: shift …` rows — receipts §4). The
notes it landed cover **14** of those 15: six `add.c` rows in `pacman-transaction-order-r39.md:87-96`, three `util.c`
rows already recorded in the r40 annex, three `makepkg.sh.in` and two `PKGBUILD.5.asciidoc` rows in
`alpm-package-anatomy-r41.md:104-113`.

The fifteenth is `lib/libalpm/add.c:670-687`, and the only knowledge entry that carries it is
`corpus/knowledge/pacman-hook-order-r38.md:136`:

> "- **HO6 host cell, corrected.** Commits are per target with no rollback (`add.c:670-687`, `sync.c:1336-1360` at
> 54d9411; …)"

`out.json` records that row as `{"cited": "lib/libalpm/add.c:670-687", "patch": "patch-reproducible-builds.patch",
"risk": "shift +23 -> :693", "method": "anchor"}`. `r38` has no round-42 note: `grep -c "Round-42"` over
`78abb8b5:corpus/knowledge/pacman-hook-order-r38.md` is **0** (receipts §3); the same line numbers are reproduced in
`SKILL.md:3189`, and the r39/r41 pins the notes correct are there too (`SKILL.md:3270-3273`, `:3325`, `:3729-3733`)
— the sweep's own scope was `corpus/knowledge/*-r38..r41.md` only, `w1/ConsiderPatchOffset.md` §"What the check does" 4).

The seat's report lumps the drift as "`lib/libalpm/add.c` shifts +23 (r39, 7 distinct line pins)", but r39's distinct
`add.c` pins are `:466-474`, `:468-469`, `:470-474`, `:616-636`, `:616-648`, `:669-688`, `:676-692`; `out.json` omits
`:616-636` and carries `:670-687` instead — the r38 pin. The L1's lesson repeats the two-entry remedy:
"Landed as appended notes in `pacman-transaction-order-r39.md` and `alpm-package-anatomy-r41.md` (the r40 util.c offset
was already recorded)" (`corpus/lessons/round-42.md:58`, untracked at the revision). So the ledger's single
unattributed row became the single unmarked entry.

Why this is `harmed` and not a nit: `LEARNING.md:34` — quality is `harmed` when "an entry is found false or stale and
left unmarked". The round's own instrument found it; the round's own remedy standard (the r39/r41 notes, which say the
pins are upstream `54d9411` and give the built-tree offset) is exactly what r38 is missing. Either the drift is a
defect worth marking — then r38 is harm — or upstream pins are not stale — then the r39/r41 notes are mere caveats and
cannot support `improved` either. The lane cannot take `improved` from the notes while leaving their twin unmarked.

## Expansion — `unchanged` (the round's own note says so)

The item's question answers itself in committed bytes:

1. `corpus/README.md:412-413`: "the scrub record stays Frontier (no census arm reads it); round 42 deepens it from
   source, **it does not enter new coverage-map ground** (the scrub record has been a Frontier line since round 26)."
   The note's row at `:410` is a deepening entry, not a coverage-map row.
2. `PROVINCE.md:212-213` still lists the scrub record under "**Still Frontier:** … no census arm reads them";
   `:234` "**Still Frontier, unchanged:** the scrub record and NVMe SMART"; `:239-243` the round-42 note adds "The
   scrub record stays Frontier … The promotion condition (a read-only census arm) is unchanged."
3. The entry says it: `btrfs-scrub-record-r42.md:158` "No census arm reads the record; this entry stays on Frontier
   ground." The round-26 promotion rule it cites is `corpus/README.md:243` ("becomes Core only after a read-only census
   arm reads it").
4. No capability row: `git diff -U0 c8efaa3f 78abb8b5 -- SCORECARD.md | grep -c '^+.*[Cc]apabilit'` → **0**
   (receipts §8); the declaration's ordinals stand (`SCORECARD.md:2567`: depth 8, coverage 9, …).
5. No new source kind: S237 is a `code` row beside S132/S133/S230/S233; S238 is `docs` (`corpus/SOURCES.md:247`);
   S239 continues the lane's own-work series (`corpus/SOURCES.md:246-248`). Opening "the btrfs-progs release-notes half of the round-26 lead"
   (`corpus/README.md:413-414` reading) is opening a lead, not admitted ground.
6. The entry is not admitted: at this revision there is no `w2` tree (`git ls-tree 78abb8b5 .ufo/waves/round-42/` has
   no `w2` entry) and the frozen counter binds row verdicts only through `w2-dispatch.json`/`w2-results.json`
   (`tools/check-scrub-record-r42.py:16-22`, `:211-212`).

Not `harmed` either: the bar-failure condition needs an admitted entry, and none is admitted yet. `QUALITY 68`
(`corpus/QUALITY.md:136`) is why the lane wrote "deeper ground" instead of "new" — and the round declines the
new-ground claim outright, so no QUALITY-68 sweep is owed for it; none is cited in the README note either, so a later
round that wants `expansion: improved` must show that sweep's command and output before calling any of this new.

## Quality — no supersession, one re-verification, one harm

Rule: `LEARNING.md:34`; `QUALITY 49` `corpus/QUALITY.md:97`, with its clarification at `:104` ("prior entry" means an
existing corpus **content proposition**, not a previous report's trend label).

**Does any prior entry get superseded?** No. Both notes say so: "The statements are unchanged (the patched hunks do not
touch the cited logic …); only the line numbers differ in the binary's source" (`r39:95-96`, `r41:112-113`). SH3/SH4
are untouched by the round (`git diff --stat c8efaa3f 78abb8b5 -- corpus/knowledge/storage-health-r26.md` is empty;
SH4 statement `storage-health-r26.md:57`, host reading `:59`, verdict `:61`, `verified-at: 2026-10-22` `:2`). The C2 entry's corrections
(SC1/SC3/SC4/scope/triage, `git diff f50c28d8 78abb8b5 -- corpus/knowledge/btrfs-scrub-record-r42.md`; the triage token
`UNRECORDED` withdrawn, `corpus/lessons/round-42.md:37`) are revisions of the round's own unadmitted draft, not a prior
entry.

**Does any prior entry get re-verified?** One prior artifact, and not by the offset notes: the IN-109 anchor row. C1's
census edit moved the D14/D15 case, so `adjacency-anchors-r19.json` `found_line` moved 2452 → 2468 with an appended
round-42 sentence (JSON line `:2465` and the note; receipts §6). The repin is **correct**: `tools/tsukuroi-census.sh:2452`
at `c8efaa3f` and `:2468` at `78abb8b5` both print `check 'degraded: kernel ring class counts are evidence (D14/D15)' 1
DEGRADED`. But the correction reaches the JSON only:

- its companion still reads the round-32 value — `adjacency-anchors-r19.md:204` ("… | 2277 | …") and `:231` ("line
  2277") at both base and tip, so the correction is not marked in each companion (`QUALITY 67`,
  `corpus/QUALITY.md:135`; the r32 repair updated both cells, `corpus/lessons/round-32.md:53-54`); the .md staleness
  predates the round (base md 2277 vs base JSON 2452), but r42's own edit of that row was the moment to sweep it;
- the round's lesson has no IN-109 line at all (`grep -n "IN-109" corpus/lessons/round-42.md` → none), so the
  `QUALITY 60` disclosure list is incomplete for an in-place edit to `corpus/`.

The fresh `btrfs scrub status /` host reading (`btrfs-scrub-record-r42.md:118-121`, w1 `C2ExecHostRecheck` §2) does
re-observe SH4's headline fact, but at the same versions as SH4's own capture (kernel `7.2.11-arch1-1`, btrfs-progs
`7.1-1`, `storage-health-r26.md:2`); it is a four-day same-value confirmation with `verified-at` untouched and the
verdict kept (`btrfs-scrub-record-r42.md:144` "`UNVERIFIED`, SH4"; `:158` Frontier). That is not "stale entries
re-verify".

**The correction clause is stronger than its receipt.** "only the line numbers differ in the binary's source"
(`r39:95-96`, `r41:112-113`) is contradicted for makepkg by the seat's own `evidence.txt:13-18`: the built makepkg
carries `find_libdepends()` at `:472` and `find_libprovides()` at `:537`, called at `:628-629`, while the pinned r41
file has zero occurrences (`evidence.txt:19`). The seat called it "more than an offset" and put that sentence in its
proposed note; the landed note drops it. No r41 *row* asserts `write_pkginfo` content (`grep` finds none), so this is
an imprecise provenance sentence, not a false row — but it is the sentence a later round would cite as the correction's
evidence.

**Verdict.** `harmed` by the letter of `LEARNING.md:34` on the r38 row (found drifting by the round's own instrument,
left unmarked while its twins were marked); `unchanged` at the very best if the lane repairs it and denies the notes
any re-verification credit; `improved` is false at this revision. The r41 precedent is directly on point: an anchor
drift marked in a prior entry did not stop that round grading `quality: unchanged` when its new entry had not passed
(`corpus/lessons/round-41-verifier-spotcheck.md:143`). The r40 precedent shows what *would* carry `improved`:
"appended corrections/disclosures; no admitted entry fails its re-check (8/8)"
(`corpus/lessons/round-40-verifier-spotcheck.md:134-136`).

## Discernment — `unchanged` at this revision; `improved` blocked on the spot-check, not on QUALITY 90

Rule: `LEARNING.md:35` and the paragraph at `:42-45` ("Each round a non-author … spot-checks a sample of that round's
gate decisions, at least one admit and one reject … A subagent the lane dispatched is still the lane").

1. **The criterion is real and committed.** `QUALITY 90` is in the revision (`corpus/QUALITY.md:177`), its failing
   examples are committed w1 receipts (`w1/C1CritNsView.md` §3-4, `C1CritEvasion.md` §1, `C2CritControl.md` D1 — all
   present at `78abb8b5`), and its lesson row exists on disk (`corpus/lessons/round-42.md:70` `R42-OBSERVED-CHANNEL`,
   with the uid-1000 able-to-fail run from the same w1 receipt).
2. **Its lesson is not in the revision.** `corpus/QUALITY.md:177` ends "Lesson: `corpus/lessons/round-42.md` Mistakes
   R42-OBSERVED-CHANNEL"; `git cat-file -e 78abb8b5:corpus/lessons/round-42.md` → `fatal: path 'corpus/lessons/round-42.md'
   exists on disk, but not in '78abb8b5'`, and `git log --all -- corpus/lessons/round-42.md` is empty (receipts §2). This
   is the lane's normal sequencing, not a defect at a wave-2 dispatch tip: `QUALITY 89` landed at `d7bf279f` while
   round 41's lesson did not exist, and the lesson landed at `64f9062e` (receipts §9). It becomes a defect only if the
   round's outcome commit repeats that ordering without the lesson, and it means the criterion's route cannot be
   credited at the revision under test.
3. **The Gate reject that w1 said was missing now exists on disk.** `corpus/lessons/round-42.md:38` "Rejected: none of
   the five rows; rejected sentence: the draft's … (false — SH4 held the name pattern; C2CritNovelty §2)"; `:48`
   rejects staged P2 ("Reason class: false statement"). So the sample a spot-check needs (one admit plus one reject)
   is nameable — but only in an untracked file, and by a lane-dispatched seat.
4. **The non-author spot-check is still pending.** `corpus/lessons/round-42.md:63` "Non-author closure pending."
5. **Zero counted verdicts exist at the revision.** No `w2` tree in the commit (`git ls-tree 78abb8b5
   .ufo/waves/round-42/` — receipts §8; the ten `C2RevSC<n>`/`C2CritSC<n>` reports are untracked live files), and the
   counter's verdict conjunct binds only the w2 dispatch/results (`tools/check-scrub-record-r42.py:16-22`, `:211-212`).

So `improved` is blocked twice over: no outside agreement on admits *and* rejects, and no bound verdicts on the
round's own rows. Route (b) — "a disagreement becomes a lesson that adds a grounded `QUALITY.md` criterion" — is
genuinely satisfied by QUALITY 90 once the lesson commits (r21/r22 used author-side route (b); the r23 closure showed
the non-author labels supersede author-side ones, `corpus/lessons/round-23.md:42`), but the lane's practice since r25
records `improved` on the spot-check itself (`corpus/lessons/round-40-verifier-spotcheck.md:137-140`,
`round-41-verifier-spotcheck.md:145-147`). No ordinal moves with any of these three verdicts.

## Impacted axes

`LEARNING.md:85-87` maps expansion to `coverage`/`adjacency`, quality to `depth`/`freshness`/`operability`, discernment
to `calibration`. This attack lands on the coverage reading (expansion), the freshness reading of the prior-entry
corrections (quality), and the calibration reading (discernment). No axis ordinal moves in either direction: the r38
pin is a marking gap, not a false proposition, and the round's own depth claim is unmeasured at this revision, not
failed.

## Smallest safe correction

1. Append the round-42 packaging-offset note to `corpus/knowledge/pacman-hook-order-r38.md` for its one drifted pin
   (`add.c:670-687` reads `:693-710`; `sync.c:1336-1360` does not move), with the same text/date/seat the other two
   notes carry. This closes the 14/15 ledger gap and removes the `harmed` ground.
2. Give the SKILL card the same treatment or, at minimum, a `recheck:` line: `SKILL.md:3189`, `:3270-3273`, `:3325`,
   `:3729-3733` reproduce drifted pins and were outside the 108-pin sweep's `corpus/knowledge` scope.
3. Update `corpus/knowledge/adjacency-anchors-r19.md:204` and `:231` to `2468` (the JSON is already there) and add the
   IN-109 in-place edit to the round-42 lesson's `QUALITY 60` list; r42 edited the row, so `QUALITY 67`'s
   "each companion in the same commit" applies to it even though the .md lag predates the round.
4. Restore the scoping clause in `r39:95-96`/`r41:112-113`: the cited logic is unchanged, but the built makepkg also
   carries `find_libdepends`/`find_libprovides` (`evidence.txt:13-18`) — the seat's own sentence, not "only the line
   numbers differ".
5. Commit `corpus/lessons/round-42.md` (with `R42-OBSERVED-CHANNEL`, the Gate reject at `:38`, and the disclosure list)
   before any trend line is written. Then write:
   `expansion: unchanged` (README `:412-413`, PROVINCE `:212-213`/`:239-243`); `quality: unchanged` if 1–4 land before
   the outcome commit, rising to `improved` only under the r40 shape (corrections landed, no admitted entry failing its
   re-check) — not before the ten counted verdicts; `discernment: improved` only with the non-author spot-check on
   record agreeing on one admit and the named reject.

## What would change each verdict

- **expansion → `improved`:** a read-only census arm that reads the record lands and moves it Frontier → Core under
  `corpus/README.md:243`, recorded as a capability row; or a `QUALITY 68` sweep at the measured revision shows a
  proposition the coverage map does not hold. Deepening SH3/SH4 is not enough (`README.md:412-413` says so).
- **quality → `improved`:** the four repairs above plus the ten counted C2 verdicts holding and no admitted entry
  failing its re-check (the r40 `8/8` shape). → `unchanged`: only 1–4 landed, with the lane recording explicitly that
  the offset notes are caveats, not re-verification.
- **discernment → `improved`:** the lesson committed with its Gate reject, *and* a non-author the lane did not dispatch
  spot-checking at least one admit (S237/SC4 or S238/SC5) and the named reject with `agree`, recorded in
  `corpus/lessons/round-42.md`; or a disagreement landed as a new grounded criterion. With the lesson left
  uncommitted at the outcome commit, the `harmed` letter ("a criterion is added with no lesson behind it",
  `LEARNING.md:35`) applies instead.

## Not done / limits of this seat

- Did not run `tools/score-size-invariance-r42.py`, `tools/check-scrub-record-r42.py`, the census `--selftest`, or
  `w1/ConsiderPatchOffset/patch-offset.py`; the offset arithmetic is taken from that seat's committed receipts
  (`out.json`, `evidence.txt`) and its `108 / 15` figures, not re-measured here.
- Did not treat the untracked live `w2/` seat reports as evidence: they are not in `78abb8b5`, and the report judges
  only committed bytes at the revision.
- Did not inspect `~/.omp` transcripts (`transcripts_bound`) or the fleet MANIFEST; no fetch, no host probe, no
  package/service/sysfs change, no lane write outside `.ufo/waves/round-42/w2/CritTrendFinal{,.md}`.
- The verdicts above do not assert any proposition of `btrfs-scrub-record-r42.md` SC1-SC5 is false; on the evidence
  read here the entry keeps SH4's Frontier status and its `UNVERIFIED` verdict honestly. I did not re-check the entry's
  source quotes against the frozen snapshots.
