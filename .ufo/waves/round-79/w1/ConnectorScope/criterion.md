# Proposed QUALITY.md Criterion Text — Seat-Harm Incident Log

## Context & Audit of considerthese/2026-10-26.md Proposals
Review of the five self-improvement ideas in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/considerthese/2026-10-26.md`:

1. **Burst-aware reading:**
   - Proposal: Read LOG entries and verifier spot-checks first during high-frequency burst rounds; sample commits only on disagreements.
   - Status: **Already implemented** (adopted in round 46 / round 70 cadence and review workflows).
2. **Counter-attack scoreboard:**
   - Proposal: Track fielded attack arms, surviving mutants, and defeat classes per frozen counter.
   - Status: **Already implemented** (adopted in round 41 in `SCORECARD.md`, `corpus/README.md`, and round-41 lesson; tracked in Round 79 declaration as `attack share 4/12`).
3. **Downstream patch-offset check:**
   - Proposal: Flag upstream line pins against distribution build line shifts.
   - Status: **Already implemented** as **QUALITY 103** (`R69-PATCH-OFFSET`, adopted in round 69).
4. **Cross-note correction propagation map:**
   - Proposal: Maintain a map of note dependencies to ensure corrections reach all dependent documents.
   - Status: **Already implemented** as **QUALITY 108** (`R75-CORRECTION-PROPAGATION`, adopted in round 75).
5. **Seat-harm incident log:**
   - Proposal: Track recurring seat-to-seat and seat-to-host damage (pkill, `/tmp` misroot, fleet-root writes) separately from ordinary seat loss via a running per-round tally.
   - Status: **Unimplemented in QUALITY.md** until Round 79. Round 79 declaration (`SCORECARD.md:6665-6668`) explicitly designates this for adoption as a QUALITY criterion.

---

## Exact Proposed QUALITY.md Criterion Text

```markdown
110. **A round records a per-round seat-harm tally under a dedicated heading, classifying any peer disruption or host misroot across concurrent seats (R79-SEAT-HARM-LOG):** each round's report or lesson carries an explicit `## Seat harm` section that tallies every cross-seat or seat-to-host interference incident observed during the wave, distinguishing seat-to-seat damage from ordinary seat loss (timeouts, provider errors, or unforced exits). An incident is recorded if a seat touches a path outside its assigned wave directory or isolated scratch tree (e.g. `/tmp` misroots, fleet-root edits), executes uncoordinated process termination affecting sibling runs (e.g. `pkill`/`killall`), or exhausts shared host resources; if no cross-seat interference occurred, the section explicitly records `0` incidents (or `none`). A round that omits the tally or silences an observed cross-seat harm is not admitted. Failing examples: R39's `pkill -f` killing concurrent sibling census runs (`R39-SEAT-PKILL`), R40 seats allocating 294 MB archives under `/tmp` (`R40-TMP-MISROOT`), and R51's bare path edit misrooting into the fleet root (`R51-MISROOT`). Green example: round 79 files an explicit `## Seat harm` tally of 0 incidents under enforced `/fast/scratch/hyaku/tsukuroi-r79/<seat>` isolation. This is the lane's adoption of the `considerthese/2026-10-26.md` proposal "Seat-harm incident log" (opened 2026-10-26; adopted round 79).
```
