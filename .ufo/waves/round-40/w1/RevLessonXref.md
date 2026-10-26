VERDICT: supports

Item R-5 — the seven routed defects of `corpus/lessons/round-39-verifier-spotcheck.md` §6 and their round-40
dispositions. All seven have a disposition; none is unowned. Four of the seven are fully landed in tracked lane
files; three (§6.3, §6.4, §6.5) are assigned to wave items R-1/R-2/R-3 whose drafted corrections were **not yet
appended** to SCORECARD.md/LOG.md at check time (2026-10-26, lane tip `f951f288483c1af0cef4afd458488b84cf7a2165`,
HEAD = tip), and §6.2's last sub-item (the `census_exit` decision) has its drafted text in `w1/RoutedCensusExit.md`
but is not yet in the lesson. The round-39 Gate spot-check cross-reference the round-40 lesson needs is present and
line-accurate in the draft lesson; its "dispositioned below" promise is not yet fulfilled by the draft's body.

Method: reads, greps and read-only git queries in the lane only. No counter, selftest or clone was run; nothing
was installed; no scratch directory was created (no fixture or mutant work was needed for this item).

## 1. The seven routed defects and their dispositions

Source list: `corpus/lessons/round-39-verifier-spotcheck.md:178` ("## 6. Routed defects / next-round debts
(owner: tsukuroi)"), numbered items at `:180`, `:184`, `:188`, `:189`, `:190`, `:191`, `:192`.

| # | Routed defect (spotcheck line) | Round-40 artefact that addresses it | State at check |
|---|---|---|---|
| 1 | C2 counter reads no content, R39-CONTENT-UNREAD (`:180`) | C2 counter `tools/check-exec-environment-r40.py` (frozen `a447b67b`, sha256 `d4a2bb94…`) reads every rule cell; frozen should-fail controls `C2-K1` X-empty, `C2-K2a`/`C2-K2b` X-false; wave attacks `C2CritXFalse`, `C2MutCounter`, `C2CritControl` | landed (counter + controls); transaction-order counter itself not amended — no re-claim exists this round (see §2.1 residual) |
| 2 | C1 fixture monoculture + detect-honest class, R39-FIXTURE-MONOCULTURE (`:184`) | C1 implementation `c707e356` (five varied-literal `R40-C1` selftest cases + unlistable root), counter `tools/score-selftest-literals-r40.py` M1–M9, should-fail control `C1-K1` one-literal; `census_exit` sub-item routed to wave item R-4 | landed except the `census_exit` decision text (drafted, not yet in lesson) |
| 3 | Future-dated timestamps (`:188`) | Wave item R-1 `RoutedTimestamps` (drafts the append-only correction); declaration adds the commit-time-is-authority rule for its own section | assigned; correction not yet appended; R-1 report `VERDICT: defect-found` (scope grew beyond the two known headings) |
| 4 | Gates receipt disclosure (`:189`) | Wave item R-2 `RoutedGatesRow` (drafts the append-only correction naming the 8th row of `after/gates-final-a2d7aad.txt`) | assigned; report not on disk at check time — the only routed seat with no observable output yet |
| 5 | Receipt-provenance wording (`:190`) | Wave item R-3 `RoutedProvenance` (drafts the scoping correction for `SCORECARD.md:2245` + round-40 receipt header audit) | assigned; `SCORECARD.md:2245` unchanged at tip; R-3 report `VERDICT: defect-found` |
| 6 | Residual staged propositions (`:191`) | C2 entry `corpus/knowledge/pacman-exec-environment-r40.md` (commit `bf238050`) EX1/EX4/EX6/EX8 on new rows S219–S225; round-40 lesson Gate residual-propositions table; wave item F-2 `AsmStagedResidual` | landed in entry + Gate table; F-2 report `VERDICT: defect-found` (one staged inference rejected/corrected) |
| 7 | Lesson cross-reference (`:192`) | Draft lesson `corpus/lessons/round-40.md:8-11` cross-references the Gate spot-check to `round-39-verifier-spotcheck.md` §3 | draft present (untracked file); text verified accurate; the promised per-defect disposition block is missing from the draft (§4 below) |

No routed defect lacks a disposition. Landed-state evidence: `git status --porcelain -- SCORECARD.md LOG.md corpus/`
returns only `?? corpus/lessons/round-40.md`; the last SCORECARD outcome section is "## Round 39 — measured outcome"
(`SCORECARD.md:2241`), so no round-40 correction paragraph exists in any tracked file yet.

## 2. Per-defect evidence

### 2.1 §6.1 R39-CONTENT-UNREAD (`round-39-verifier-spotcheck.md:180-183`)

- Amended-counter pattern landed: `tools/check-exec-environment-r40.py:4` "EX1-EX8, each rule READ (QUALITY 87)";
  `:8` names the lineage "R39-CONTENT-UNREAD (round-39 verifier spot-check §6.1): the round-39 counter read only the
  source and host …"; the content check is implemented at `:279` ("# --- content (QUALITY 87) ---").
- X-empty / X-false frozen as should-fail controls (the spotcheck's explicit ask): `.ufo/waves/round-40/controls/controls.jsonl`
  rows `C2-K1-x-empty`, `C2-K2a-x-false-negated`, `C2-K2b-x-false-values` — each `exit 1`, `rules_verified 0`,
  `result FAIL`, all under `counter_sha256 d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`;
  declared at `SCORECARD.md:2308-2309`. Candidate `C2-K7` is the only C2 control that PASSes (`controls.jsonl`).
- Standing instrument: before/after receipts exist at `f951f28` (`.ufo/waves/round-40/before/c2-before.jsonl`,
  `.ufo/waves/round-40/after/c2-after-bf23805.jsonl`, commit `f951f28` stat), so the content counter is a rerunnable
  instrument for the new entry, not a one-time re-derivation.
- Residual, stated honestly: `git log --oneline 53b294a..f951f28 -- tools/check-transaction-order-r39.py
  tools/score-storage-hidden-r39.py` returns empty — both round-39 counters are byte-unchanged this round. The
  spotcheck's duty is conditional ("Any re-claim on transaction order must use an amended counter"); round 40's C2
  moves to a different scope (`SCORECARD.md:2304`, exec environment), so the condition has no live trigger. The
  amendment for transaction order itself still does not exist and must be written before any future re-claim.

### 2.2 §6.2 R39-FIXTURE-MONOCULTURE (`round-39-verifier-spotcheck.md:184-187`)

- Varied literals: `SCORECARD.md:2303` (C1 row) — fixtures "vary device, mountpoint, options, subvolume, line
  position and fstype case, plus an unlistable root with btrfs mounted", implementation commit `c707e356`; counter
  docstring `tools/score-selftest-literals-r40.py:5-9` names R39-FIXTURE-MONOCULTURE and the single round-39 string
  `/dev/mapper/root / btrfs rw,noatime,subvolid=256,subvol=/@ 0 0`; the nine frozen mutants M1–M9 map to the round-39
  arms VA, VB, VC, VG, MutParse (a), (b), MutCrossCheck (e) plus `subvol=/@`-keyed and last-line-only
  (`SCORECARD.md:2303`). Before at base: survivors 9 FAIL (`C1-K0`); candidate: survivors 0, selfref 5, PASS
  (`C1-K4`) — `controls.jsonl`.
- One-literal should-fail control (QUALITY 87 b): `C1-K1-one-literal-fixtures` — five added cases of the one round-39
  literal shape, survivors 9, FAIL (`controls.jsonl`; `SCORECARD.md:2311-2312`).
- Detect-honest honesty: `C1-K2-self-reading-selftest` FAILed its own baseline (`baseline_pass 0`, `selfref 6`) and
  is recorded as NOT isolating the self-reference guard, with a wave item attacking it (`SCORECARD.md:2312-2313`;
  `C1CritControl`, item C1-5). The excluded equivalent mutant (`$fsn`→`$devn`) is named with its reason at
  `tools/score-selftest-literals-r40.py:33-34` and `SCORECARD.md:2316-2317`.
- `census_exit` sub-item ("decide whether that is intended and record the decision"): not decided in any landed
  lane file — `grep -c census_exit` over both round-40 counters returns 0. It is routed to wave item R-4
  (`w1-spec.json` item `RoutedCensusExit`, prompt "Item R-4 (round-39 closure §6.2 last bullet)", targeting
  `tools/score-storage-hidden-r39.py` and `.ufo/waves/round-39/after/c1-final-a2d7aad.jsonl`). R-4's report exists
  at check time (`w1/RoutedCensusExit.md`, `VERDICT: supports`) with the drafted decision paragraph at its §5;
  the decision is "ignoring the exit is correct but unrecorded — state it in the docstring and make the counter
  consume the field (exit == rank of the printed rollup verdict)". Not yet landed anywhere tracked.

### 2.3 §6.3 Future-dated timestamps (`round-39-verifier-spotcheck.md:188`)

- Forward rule in the declaration: "Every timestamp in this section is the time it was written; the commit time is
  the authority (round-39 routed defect §6.3)" — `SCORECARD.md:2295`.
- Correction itself: assigned to R-1 `RoutedTimestamps` (`w1-spec.json`, "Item R-1 (round-39 closure §6.3)"): measure
  both headings' commit times with `git log -S`, sweep every SCORECARD/LOG heading of rounds 35-39, draft the exact
  append-only paragraph. Not appended: SCORECARD.md/LOG.md are unmodified in the working tree and no round-40
  outcome section exists. `w1/RoutedTimestamps.md` is on disk with `VERDICT: defect-found`, i.e. the sweep found
  future-dated headings beyond the two known ones — landing the named correction before the round closes is now
  mandatory, not optional.

### 2.4 §6.4 Gates receipt disclosure (`round-39-verifier-spotcheck.md:189`)

- Assigned to R-2 `RoutedGatesRow` (`w1-spec.json`, "Item R-2 (round-39 closure §6.4)"): name the 8th row of
  `after/gates-final-a2d7aad.txt` (`check-self-assessment rc=1`, 7 mismatches, `declaring_round 38`), why it was red,
  and the `eeba342e` 27/0 PASS supersession, as an append-only correction.
- Gap at check time: `w1/RoutedGatesRow.md` did not exist (`head -3` → no report) while every other routed seat's
  report did. Assigned, not missing — but it is the one routed defect whose seat output I could not observe.

### 2.5 §6.5 Receipt-provenance wording (`round-39-verifier-spotcheck.md:190`)

- The defective sentence is still live at the tip: `SCORECARD.md:2245` reads "each written by `tools/run-receipt.py`
  (revision, tool, tool_sha256, tool_revision `6a08925d`)".
- Assigned to R-3 `RoutedProvenance` (`w1-spec.json`, "Item R-3 (round-39 closure §6.5)"): per-file header audit
  under `.ufo/waves/round-39/after/`, draft scoping correction, plus which round-40 before/after receipts carry the
  header. `w1/RoutedProvenance.md` is on disk with `VERDICT: defect-found`. Correction not yet appended.

### 2.6 §6.6 Residual staged propositions (`round-39-verifier-spotcheck.md:191`)

- The round-39 Gate flip condition required "a round-40 entry … that states each with its line" on new rows "(next
  free S219)" (`corpus/lessons/round-39.md` Gate, residual-mechanism-propositions row). Delivered exactly:
  `corpus/knowledge/pacman-exec-environment-r40.md` EX1 (cwd `/`), EX4 (scriptlet shell — S219 default `/bin/sh`,
  S220 Arch `/usr/bin/bash`), EX6 (NeedsTargets stdin sorted, de-duplicated — S224), EX8 (`.pacnew` outcome still
  matches; `Path` triggers on file-list names, NoUpgrade ignored), commit `bf238050`; declaration row
  `SCORECARD.md:2304`.
- The round-40 lesson Gate re-grounds all five staged lines: four admits (one admit-with-correction) and one reject
  (`corpus/lessons/round-40.md`, "residual propositions re-grounded" table). Wave item F-2 `AsmStagedResidual`
  re-judges each against EX1-EX8 (`w1/AsmStagedResidual.md`, `VERDICT: defect-found`).

### 2.7 §6.7 Lesson cross-reference (`round-39-verifier-spotcheck.md:192`)

- The Gate text to cross-reference: `corpus/lessons/round-39.md:61` is the heading "### Spot-check"; `:63-64` reads
  "Non-author closure pending. Suggested sample: admit S216 (re-open `util.c` at 54d9411, line 527) and the reject of
  the staged interpretive sentences (`pacman-hook-timing-r25.md:22`, `:26-27`) against `alpm-hooks.5.asciidoc:38-39`."
- The draft lesson already carries the cross-reference (`corpus/lessons/round-40.md:8-11`, untracked working-tree
  file, 55 lines): it points at `round-39-verifier-spotcheck.md` §3, cites `:121-147`, and says all four samples
  agreed. Every claim in it checks out:
  - `:121` is the §3 heading (verified: `sed -n '121p'` → "## 3. Discernment spot-check (LEARNING.md — from outside)").
  - The §3 table rows `:125-128` cover a superset of the suggested sample: the S216 admit and the staged-interpretive
    reject that the Gate asked for, plus the S214 admit and the "independent confirmation" reject.
  - `:147` is the Result line: "the closure agrees with every sampled admit (S216, S214) and with both sampled
    rejects." (verified: `sed -n '147p'`). §7 closes the round `ok`/`admitted`.
- One inaccuracy of promise, not of fact: the draft says "its §6 routed the seven debts dispositioned below"
  (`round-40.md:11`), but the draft's body ends at the residual-propositions assimilation result (`:55`) and contains
  no per-defect disposition block. The block must be appended before the lesson is committed, or the sentence
  softened. Proposed text in §4 closes this.

## 3. Wave-seat state at check time (2026-10-26, tip `f951f28`)

`w1-spec.json` declares 65 seats; the routed lane is R-1 `RoutedTimestamps`, R-2 `RoutedGatesRow`, R-3
`RoutedProvenance`, R-4 `RoutedCensusExit`, R-5 `RevLessonXref` (this seat), plus F-2 `AsmStagedResidual` for §6.6.
Reports on disk and their first-line verdicts: `w1/RoutedTimestamps.md` defect-found; `w1/RoutedProvenance.md`
defect-found; `w1/RoutedCensusExit.md` supports; `w1/AsmStagedResidual.md` defect-found; `w1/RoutedGatesRow.md`
absent. I read only the verdict lines of R-1/R-3/F-2 (their evidence is their items' scope) and R-4's full report.

## 4. Exact proposed text

(a) Cross-reference paragraph for `corpus/lessons/round-40.md` (the draft's `:8-11` is correct; this form sharpens
the cites and keeps the "below" promise explicit until §4(b) is appended):

> The round-39 Gate's "Spot-check: Non-author closure pending" (`corpus/lessons/round-39.md:61-64`) is answered by
> `corpus/lessons/round-39-verifier-spotcheck.md`: its §3 (`:121-147`) re-opened the suggested sample — the S216
> admit (`:125`) and the reject of the staged interpretive sentences (`:127`) — and, beyond the sample, the S214
> admit (`:126`) and the "independent confirmation" reject (`:128`), agreeing with all four (`:147`); its §7 closes
> the round `ok`/`admitted`. Its §6 (`:178-192`) routed the seven debts dispositioned below.

(b) Disposition block to append to the lesson so the "dispositioned below" promise is true (fill the R-1/R-2/R-3
cells from those seats' drafted paragraphs before committing; R-4's decision text is already drafted at
`w1/RoutedCensusExit.md` §5):

> ### Round-39 routed defects — round-40 disposition (`round-39-verifier-spotcheck.md` §6, `:178-192`)
>
> | # | Defect | Disposition |
> |---|---|---|
> | 1 | C2 counter reads no content (R39-CONTENT-UNREAD, `:180`) | Closed for this round's surface: the C2 counter reads every rule cell (QUALITY 87; `tools/check-exec-environment-r40.py:4,8,279`) and X-empty / X-false-negated / X-false-values are frozen should-fail controls (`controls.jsonl` `C2-K1`, `C2-K2a`, `C2-K2b`). The round-39 transaction-order counter is not amended; no transaction-order re-claim is made this round, and any future re-claim must first write the amended counter. |
> | 2 | C1 fixture monoculture (R39-FIXTURE-MONOCULTURE, `:184`) | Closed: five varied-literal `R40-C1` fixtures plus an unlistable root (`c707e356`), nine frozen mutants M1–M9, one-literal should-fail control `C1-K1`; `census_exit` decision per `w1/RoutedCensusExit.md` §5 (ignore is correct, must be recorded, and the counter must require `census_exit == rank(printed rollup verdict)`). The self-reading control `C1-K2` failed its own baseline and does not isolate the selfref guard — recorded, attacked by C1CritControl. |
> | 3 | Future-dated timestamps (`:188`) | Appended correction (no rewrite) naming every future-dated heading with its stated and commit time; commit time is the authority. Text: `w1/RoutedTimestamps.md`. |
> | 4 | Gates receipt disclosure (`:189`) | Appended correction naming the 8th row of `after/gates-final-a2d7aad.txt` (`check-self-assessment rc=1`, 7 mismatches, `declaring_round 38`) and the `eeba342e` 27/0 PASS supersession. Text: `w1/RoutedGatesRow.md`. |
> | 5 | Receipt-provenance wording (`:190`) | Appended scoping correction for `SCORECARD.md:2245`; the round-40 claim receipts carry run-receipt.py headers. Text: `w1/RoutedProvenance.md`. |
> | 6 | Residual staged propositions (`:191`) | Landed on new rows S219–S225 in `pacman-exec-environment-r40.md` (EX1 cwd `/`, EX4 scriptlet shell, EX6 NeedsTargets stdin, EX8 `.pacnew`); Gate table: four admits (one with correction), one staged inference rejected. |
> | 7 | Lesson cross-reference (`:192`) | This section and the paragraph above: the Gate spot-check is answered by `round-39-verifier-spotcheck.md` §3 (`:121-147`), all four samples agreed. |

## 5. Residual risk and verification gaps

- R-2 `RoutedGatesRow` had no report on disk at check time; §6.4 is the one disposition I could not observe beyond
  its assignment.
- §6.3 and §6.5 corrections exist only as wave drafts; until the L1 appends them (and the R-1 sweep's newly found
  future-dated headings are included), `SCORECARD.md:2245` and the round-39 headings remain as the spotcheck
  described them.
- The lesson draft's "dispositioned below" sentence is currently unmet by its own body (§2.7).
- I verified the existence and verdict lines of the routed seats' reports, not their evidence (their items' scope);
  I did not run any counter, selftest or census — every check here is a read, grep or read-only git query, and an
  unrun check has not passed.
- Tooling: nothing installed; no scratch directory created; no lane file written except this report.
