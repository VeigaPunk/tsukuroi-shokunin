VERDICT: falsifies

Seat CritTrend, item G-4 (critic, axis discernment, milestone "trend verdict attack"). Round 42 wave 1. Lane tip read:
`87c4f7c627e377e5f6d361498e8db9b3886d7953` (base `c8efaa3f120834541f8de1e5e0367e8d1593bae6`). Read-only: `read`,
`grep`, `sed`, `git log`/`rev-parse`, `wc`. No counter, no census selftest, no network fetch, no host probe, no tool
installed (nothing to record under the operator tooling directive).

`improved` is falsified for all three trends on the committed evidence at this tip. The supportable verdicts are
`expansion: unchanged`, `quality: unchanged`, `discernment: unchanged` (pending the non-author closure; not claimable
now). The two questions the item asks answer themselves from the lane's own bytes: the scrub record is **covered**
coverage-map ground, and **no** prior weaker entry is superseded by SC1-SC5 — SH4 is explicitly preserved.

## Counterexample (the strongest one available, internal to the round)

The entry the three trends would have to rest on declares itself held ground and unmet promotion conditions, and the
lesson declares the outside check pending:

- `corpus/knowledge/btrfs-scrub-record-r42.md:149-150` — "No census arm reads the record; this entry stays on Frontier
  ground (`PROVINCE.md` promotion condition for the scrub record unchanged)."
- `corpus/knowledge/btrfs-scrub-record-r42.md:136-137` — "Read "no scrub record" as `UNRECORDED`, not
  `NEVER SCRUBBED` (SC3); the lane's SH4 verdict `UNVERIFIED` for stored data stands."
- `corpus/lessons/round-42.md:7-8` — "Seats are the lane, not outside reviewers (LEARNING.md); this round's
  non-author closure is pending."

A round cannot earn `expansion improved` on ground its own entry says is unchanged, `quality improved` on a prior
proposition it explicitly keeps standing, or `discernment improved` on a spot-check its own lesson says is pending.
The nearest identical precedent is the round-40/41 reading of the same storage item: `corpus/README.md:335` and
`:385` record "the storage items are unchanged — the scrub record and NVMe SMART stay Frontier". Round 41 was graded
`expansion unchanged` on exactly that reasoning (`corpus/lessons/round-41-verifier-spotcheck.md` §5: "no uncovered
coverage-map ground or Frontier move").

## Expansion — falsifies `improved`; evidence supports `unchanged`

Observable and rule: LEARNING.md:33 (`expansion`) admits `improved` for "net new admitted entries **on uncovered
ground**, each citing its coverage-map row"; QUALITY 68 (`corpus/QUALITY.md:136`, R27-DECLARED-FRONTIER-OVERCLAIM)
requires a sweep of the lane's own corpus before ground is called new, and "existing coverage makes the claim "deeper
ground" or a supersession instead."

1. **The scrub record is held ground, not uncovered.** `corpus/README.md:239` (round-26 row) states the holds
   verbatim: "SH3 scrub repairs only from a replica …; SH4 no scrub record exists on this host (`UNVERIFIED`)" — and
   SH4's own statement names the file family: "`/var/lib/btrfs`, where btrfs-progs keeps scrub.status.<UUID> files"
   (`corpus/knowledge/storage-health-r26.md:57`, sourced S139). The mechanism detail is new; the ground is not.
2. **It is named Frontier ground already.** `PROVINCE.md:212-213`: "**Still Frontier:** the scrub record (`btrfs scrub
   status`, `/var/lib/btrfs/scrub.status.*`, `btrfs-scrub@.timer`; SH3/SH4) … — no census arm reads them." Entering a
   Frontier area therefore did not happen this round; the area was entered in round 26 and re-declared Frontier in
   rounds 38 to 41 (`corpus/README.md:296`, `:335`, `:385`; round 39 at `PROVINCE.md:234` "Still Frontier, unchanged: the
   scrub record and NVMe SMART").
3. **No Frontier→Core move.** `corpus/README.md:243` is the round-26 rule: storage integrity "becomes Core only after a
   read-only census arm reads it". C2 adds no census arm; C1 changes the early readers under `set -o pipefail` and
   `run_selftest` cases (`SCORECARD.md:2573`), which the declaration itself places on **operability**, not coverage.
4. **No new kind of source.** S237 is the first btrfs-progs *source-code* row (`corpus/SOURCES.md:246`, kind `code`,
   tier A), but upstream `code` rows were already mined — S132 (`SOURCES.md:138`), S133 (`:139`, Linux kernel), S230
   (`:239`), S233 (`:242`, libalpm). S239 continues the lane's own-work series (S236, `:245`). "New kinds of source"
   (LEARNING.md:33) is not met by a new artifact inside a kind already in use.
5. **No capability row.** The declaration's claims are C1 operability and C2 depth (`SCORECARD.md:2573-2574`); nothing
   is admitted to the capabilities table (`git diff -U0 c8efaa3f..87c4f7c6 -- SCORECARD.md | grep -c
   '^+.*[Cc]apabilit'` → 0), and the base ordinals stand (depth 8, coverage 9, …).
6. **The entry is still a draft.** The C2 entry commit `f50c28d8` reads "C2 entry btrfs-scrub-record-r42.md SC1-SC5
   (draft for wave review)"; its admission is not final, and the frozen counter binds row verdicts only from
   `w2-dispatch.json`/`w2-results.json` (`tools/check-scrub-record-r42.py:16-23`, `:211-212`). An entry not yet
   admitted cannot be the "net new admitted entry" the trend rule requires.

**Answer to the item's question:** no — the scrub record is *not* uncovered coverage-map ground. `README.md:239` holds
it (SH3/SH4), `README.md:243` conditions its promotion on a census arm, `PROVINCE.md:212-213` names it as still
Frontier, and the entry itself says it stays there (`:149-150`).

## Quality — falsifies `improved`; evidence supports `unchanged`

Rule: QUALITY 49 (`corpus/QUALITY.md:97`): "new instrument existence, fixture growth or in-round hardening is not by
itself `quality: improved`. Name the prior weaker/stale entry that was superseded or reverified, with actual evidence;
otherwise retain unchanged." Clarification at `corpus/QUALITY.md:104`: "prior entry" means an existing corpus content
proposition, not a previous report's trend label.

1. **C1 is in-round tool hardening.** Two new selftest cases (128→130) plus here-string/`awk NR` readers
   (`SCORECARD.md:2573`). No corpus content proposition is superseded. Round 41 graded the same class of C1 (census selftest
   hardening) `operability improved` with `quality unchanged` (round-41 closure §2 C1 / §5), the lane's own precedent.
2. **The nearest prior proposition is preserved, not superseded.** SH4 (`corpus/knowledge/storage-health-r26.md:55-57`)
   says "No scrub record exists on this host … `btrfs scrub status /` reports no stats, and /var/lib/btrfs … does not
   exist … Verdict `UNVERIFIED`." The new entry says that verdict "stands" (`btrfs-scrub-record-r42.md:136-137`) and
   its Limits repeat that the host readings "cannot show that no scrub ever ran" (`:148`). A preserved proposition
   is not a superseded weaker one.
3. **No re-verification either, and one reading is missing.** The round-42 capture re-observes two of SH4's three
   readings — `capture.txt:6` `var_lib_btrfs absent`, `:8` `scrub_timer_unit_file btrfs-scrub@.timer disabled` — but
   SH4's headline reading, "`btrfs scrub status /` reports no stats", was not re-run: "the command itself was not run"
   (`btrfs-scrub-record-r42.md:112`). SH4's `verified-at: 2026-10-22` and cadence `on-release`
   (`storage-health-r26.md:3`) are untouched, and no release made the recheck due — `capture.txt:2-3` read kernel
   `7.2.11-arch1-1` and btrfs-progs `7.1-1`, the same versions as round 26's capture. A four-day same-value
   re-observation missing one fact is not "stale entries re-verify" (LEARNING.md:34).
4. **S139's prose is a source row, not a corpus content proposition.** Sharpening the docs sentence "recorded in
   :file:`/var/lib/btrfs/` in textual files named" (S139, cited by SH4) with S237's exact name, `_tmp`+rename and
   `flock` is new detail on held ground; under the R23 clarification it earns no quality-trend point.
5. **Nothing is admitted yet.** The entry is a wave-1 draft (commit `f50c28d8`, "draft for wave review"); the predicate's
   row verdicts come only from wave-2 seats (`tools/check-scrub-record-r42.py:16-23`), so there is no admitted entry
   whose re-check could satisfy the trend rule either way.

**Answer to the item's question:** SC1-SC5 supersede **no** prior weaker entry, and re-verify **none** in the
QUALITY-49 sense. SH4 is the nearest entry: SC1/SC3/SC4 (and the fresh capture) explain *why* "no record" is not
"never scrubbed", which SH4 already qualified as `UNVERIFIED`; the entry keeps SH4 explicitly. SH3 is untouched.

## Discernment — falsifies `improved`; evidence supports `unchanged` (not merely "unproven")

Rule: LEARNING.md:42-46 — "Each round a non-author — a fresh reviewer or the operator — spot-checks a sample of that
round's gate decisions, **at least one admit and one reject**, and records `agree`/`disagree` … in the round's lesson.
A subagent the lane dispatched is still the lane." LEARNING.md:35: `improved` only when the spot-check agrees on admits
*and* rejects, or a disagreement becomes a lesson that adds a grounded QUALITY criterion.

1. **The non-author spot-check has not happened.** `corpus/lessons/round-42.md:20-23`: "Non-author closure pending.
   Candidates for it: one admit (S237 / SC4 or S238 / SC5) and one reject from the assimilation set below." The file
   has no assimilation section — 37 lines, headings `## Gate` (:14), `### New SOURCES rows` (:16), `### Spot-check`
   (:20), `## Mistakes` (:25), `## Round-41 routed defects` (:29), `## Sources census` (:33) — so the required reject
   is not merely undecided, it is unnamed and has no landed Gate record. The Gate's admit/reject rows are the
   `<!-- GATE-ROWS -->` placeholder (`corpus/lessons/round-42.md:18`).
2. **Wave-1 C2 seats cannot substitute.** They are lane-dispatched falsifiers (the seat prompt says so; the lesson
   states "Seats are the lane, not outside reviewers", `:7-8`), and the frozen counter counts only the wave-2 bound
   seats: `tools/check-scrub-record-r42.py:19-22` — "Seats per row: `C2RevSC<n>` (reviewer) and `C2CritSC<n>` (critic)
   … bound through `w2-dispatch.json` … `w2-results.json`"; `:211-212` binds `w2` only.
3. **No criterion was added behind a lesson this round.** The second discernment route needs a disagreement that lands
   as a grounded `QUALITY.md` criterion; the Gate and Mistakes sections are placeholders (`:18`, `:27`), so there is
   nothing of that class to cite.
4. **Self-attestation cannot carry it.** LEARNING.md:42 ("Self-assessed taste is not discernment") and :48-50 (the
   exploratory label is admitted "never through self-attestation").

## Impacted axes

LEARNING.md:87-88 maps expansion to `coverage`/`adjacency`, quality to `depth`/`freshness`/`operability`, discernment to
`calibration`. This attack therefore lands on the coverage reading (expansion), the depth and freshness readings
(quality), and the calibration reading (discernment); no ordinal moves either way, because nothing here is harmed —
the scrub-record detail is true on its pinned sources and does not make any prior proposition false.

| Trend | Claim attacked | Verdict the evidence supports | Basis |
|---|---|---|---|
| expansion | `improved` | `unchanged` | held ground (`README.md:239`, `PROVINCE.md:212-213`), no census arm/Core promotion (`README.md:243`), no new source kind, entry draft (`f50c28d8`) |
| quality | `improved` | `unchanged` | QUALITY 49 (`QUALITY.md:97`, `:104`); SH4 preserved (`btrfs-scrub-record-r42.md:136-137`, `storage-health-r26.md:55-57`); C1 is tool hardening |
| discernment | `improved` | `unchanged` (not claimed) | non-author spot-check pending, no Gate reject named (`lessons/round-42.md:20-23`); lane seats excluded (`LEARNING.md:46`; counter `:16-23`) |

## Smallest safe correction

Nothing to change in the entry's content on trend grounds; the correction is the round report's trend lines plus one
Gate record. Proposed exact text for the report's trend section:

```
- **expansion: unchanged** — `btrfs-scrub-record-r42.md` SC1-SC5 deepens held storage-integrity Frontier ground
  (`corpus/README.md:239`, SH3/SH4; `PROVINCE.md:212-213` "Still Frontier: the scrub record …"; the entry's own
  `:149-150` "this entry stays on Frontier ground"). No census arm reads the record (`corpus/README.md:243`
  promotion rule), no new source kind (S237 is a `code` row beside S132/S133 and S230/S233), no capability row.
- **quality: unchanged** — QUALITY 49 (`corpus/QUALITY.md:97`): no prior corpus proposition is superseded or
  reverified. SH4 (`storage-health-r26.md:55-57`) stands by the entry's own words (`btrfs-scrub-record-r42.md:136-137`);
  its 2026-10-22 `verified-at` / `on-release` cadence is untouched, and the fresh capture re-observes two of its three
  readings (`capture.txt:6,8`) while `btrfs scrub status` was not re-run (`btrfs-scrub-record-r42.md:112`). C1's two
  selftest cases are in-round hardening, not quality-trend evidence.
- **discernment: unchanged, not claimed** — the non-author spot-check is pending (`corpus/lessons/round-42.md:7-8,20-23`)
  and no Gate reject is yet named; wave-1 C2 seats are lane falsifiers (`LEARNING.md:46`;
  `tools/check-scrub-record-r42.py:16-23`).
```

Plus one Gate-record line: the round's `## Gate` must name at least one rejected candidate with its reason before a
non-author spot-check can cover "at least one admit and one reject" (LEARNING.md:44); "one reject from the assimilation
set below" (`lessons/round-42.md:22-23`) currently points at no section.

## What would change each verdict

- **expansion → `improved`:** a read-only census arm that reads the scrub record lands and the item moves Frontier →
  Core under `corpus/README.md:243`, recorded as a capability; or a QUALITY-68 sweep at the measured revision shows a
  proposition that `README.md:239`, `PROVINCE.md:212-213` and `README.md:296/335/385` do not hold. Deepening SH3/SH4 is
  not enough.
- **quality → `improved`:** a *named* prior corpus proposition superseded or re-verified with evidence at the measured
  revision — e.g., SH4's `verified-at` refreshed by an actual `btrfs scrub status` reading plus the directory and timer
  re-reads (all three facts), or a committed correction naming the superseded SH3/SH4 text — with no admitted entry
  failing its own re-check. A wave-2 PASS of `check-scrub-record-r42.py` alone is instrument evidence, not this.
- **discernment → `improved`:** a spot-check recorded in `corpus/lessons/round-42.md` by a non-author the lane did not
  dispatch, covering at least one admit **and** a named Gate reject with reasons, both agreeing; or a disagreement
  landed as a lesson behind a new grounded `QUALITY.md` criterion. The Gate must first contain a reject decision.

## Not done / limits of this seat

- Did not run `tools/score-size-invariance-r42.py`, `tools/check-scrub-record-r42.py`, the census `--selftest`, or any
  fetch; did not inspect wave-2 dispatch (it does not exist yet at this tip). Whether a wave-2 seat later supplies the
  Gate reject, and whether the closure grades these trend lines at all, is outside this seat.
- The verdicts above are what the committed bytes at `87c4f7c6` support; they do not assert any proposition in the
  scrub-record entry is false. No lane file other than this report was written; no scratch tree was created or left.
