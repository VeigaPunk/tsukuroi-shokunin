VERDICT: supports

# F-1 — considerthese/ mine (round-48 w2, seat ScoutConsider)

Scope: `ls -l` of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/considerthese/`, all seven files read
whole (the required newest three 2026-10-24, -25, -26 plus the four older for context). Lane bytes read at
the freeze revision `ae99f021b76f8eb1c8805d32d80644464afb1ff6` via `git show`; implementation status
checked by `git grep` at the freeze revision and at HEAD (`23f85377433c…`, same hits). The round-48
declaration explicitly authorizes this item: `SCORECARD.md:3110` "considerthese/: one proposal mined by a
wave scout, landed only if the lane's own bar grounds it."

## Method note — the lane already mines these

Every mined proposal lands as a `### considerthese — <name>` section in `corpus/lessons/round-*.md` (and
sometimes a SKILL/SCORECARD artifact). `git grep -l considerthese corpus/lessons/` →
round-{26-verifier-spotcheck,37,38,39,40,41,41-verifier-spotcheck,42,43,45,46,47}.md. So "still
unimplemented" here means: no mined section, no lane artifact, and grep of the distinctive vocabulary at
the freeze revision finds nothing in SKILL/SCORECARD/corpus/tools.

## Inventory of proposal status (every proposal in the directory)

Files: `2026-10-19.md` (5 proposals), `2026-10-20.md` (5), `2026-10-22.md` (5), `2026-10-23.md` (5),
`2026-10-24.md` (5), `2026-10-25.md` (4), `2026-10-26.md` (5).

Mined or already landed — not candidates:
- 2026-10-26 "Counter-attack scoreboard" → `SKILL.md:3833` "Counter-attack scoreboard — rounds 40-41",
  `:3935` round-42 continuation; disclosed `SCORECARD.md:2508`; mined round 41
  (`corpus/lessons/round-41.md:99`) and re-mined open at round 47 (`corpus/lessons/round-47.md:71`:
  "no longitudinal survivor ledger was added; the proposal remains open").
- 2026-10-26 "Seat-harm incident log" → 10-incident ledger, `corpus/lessons/round-45.md:124-164`;
  open residue noted there: "no gate reads this ledger" (`round-45.md:166`).
- 2026-10-26 "Downstream patch-offset check" → appended notes in three knowledge rows
  (`SCORECARD.md:2611`; `pacman-hook-order-r38.md:159`, `pacman-transaction-order-r39.md:87`,
  `alpm-package-anatomy-r41.md:104`); mined `corpus/lessons/round-42.md:53`.
- 2026-10-26 "Cross-note correction propagation map" → built for the round-42 SC1/SC3/SC4/SC5
  corrections, `corpus/lessons/round-43.md:83-96` ("34 dependent sites… 4 restated… closed by
  append-only pointers"; open: "no gate reads a correction pointer").
- 2026-10-26 "Burst-aware reading" → measured on rounds 43-45, `corpus/lessons/round-46.md:97-109`.
- 2026-10-25 "Probe lineage table" → 11-row version table, `corpus/lessons/round-38.md:109`,
  extended `corpus/lessons/round-40.md:95`; a round-36 wave seat also ran a per-rule lineage audit
  (`.ufo/waves/round-36/l1/gen-w1-spec.py:168` RevProbeLineage).
- 2026-10-25 "Evidence-weight watch" → `corpus/lessons/round-39.md:94`.
- 2026-10-23 "Verified-rate ledger" → `corpus/knowledge/verified-rate-ledger-r37.md` +
  `tools/check-verified-rate-ledger.py` (`SCORECARD.md:1921-1930`); mined-not-implemented rationale
  kept at `corpus/lessons/round-37.md:64-66` — precedent that a mined proposal may be declined
  with the reason recorded.
- 2026-10-24 "Upstream release watch": partially covered for mkinitcpio only —
  `corpus/README.md:146-153` carries an explicit on-release watch; no general pinned-version watch
  for systemd/pacman/btrfs-progs (grep at freeze rev: none). Relevant to C2 marginally: GR1-GR3
  pin Linux v7.2.11 and systemd 259 man-page sources; nothing in this round's claims requires a
  release recheck, and the round's own re-opens (S237, S240, S242-S249 re-opened live) cover it.

Still unimplemented AND relevant to this round's claims or the lane frontier:

1. **"Routed-debt carry-over check"** — `considerthese/2026-10-24.md:18` (committed `f0b8f7a5`,
   2026-10-24 09:32). "check whether the following round closed each one … report what is carried
   over and for how long." RELEVANT: round 48 is literally carried debt — C1 is the R47-TMPDIR fix
   retried (`R47-C2-TMPDIR-FALLBACK`, `corpus/lessons/round-47.md:45`), C2 is the GR1-GR3 admission
   retried after round-45/46/47 gate failures (`btrfs-scrub-grounding-r45.md:227-269`), C3 is the
   recurring K10 restatement debt. Per-round disposition tables exist
   (`corpus/lessons/round-47.md:57-66` "Round-46 routed defects — round-47 disposition";
   `round-46.md:76-86`) but no consolidated age ledger: a debt listed "carried" (e.g.
   `corpus/lessons/round-38.md:103` row 2, the counter-freeze-sha debt; row 4, the V8 mutant wave)
   has no row anywhere counting how many rounds it has survived. `git grep` at freeze rev for
   `debt.{0,20}carry|carry.over.{0,20}debt` in SKILL/SCORECARD/corpus/tools → only wave artifacts,
   no lane mechanism.
2. **"Claim-arc length"** — `considerthese/2026-10-24.md:21`. "track how many rounds a single goal
   has run without a verified close … when the instrument, not the fix, needs the next round."
   RELEVANT to frontier: C2's scrub-admission goal is now at four declared rounds (r45/r46/r47
   gates FAILED, r48 open); the r36 lesson already made the instrument-vs-fix call qualitatively
   (allow-list arc 31-36, `considerthese/2026-10-24.md:9`). No arc ledger exists (`git grep`
   'claim arc|arc length' → nothing outside `.ufo/` wave text; `SCORECARD.md:49` uses "Arc:" only
   as prose inside one axes row).
3. "Next-round pickup sheet" — `considerthese/2026-10-25.md:18`. Same debt-enumeration function as
   (1); narrower (a pre-round list), so subsumed.
4. "Seat-loss tally" — `considerthese/2026-10-24.md:19`. Frontier-relevant (attempt-1's void `w1`
   was mass seat loss; round-45 lost `C2RevGR1` mid-turn, `btrfs-scrub-grounding-r45.md:230-232`)
   but weaker: no seat-loss mechanism exists to ground a table beyond incident prose already in
   LOG/lessons.
5. "Author-versus-verifier calibration ledger" — `considerthese/2026-10-20.md:47-49`. RELEVANT to
   C3 (calibration) but largely superseded by the landed verified-rate ledger
   (`corpus/knowledge/verified-rate-ledger-r37.md`) and C3's own fixed 27-check counter.
6. "Receipt-first verification of headline numbers" — `considerthese/2026-10-22.md:21`. RELEVANT
   (this seat does exactly it) but it is a reviewer-workflow rule, not a lane artifact; QUALITY 77
   and the frozen-receipt discipline already encode the harder half.
7. "Waived-obligation tracker" — `considerthese/2026-10-20.md:56-57`. Frontier-relevant debt
   ledger (R16-FALSIFY, boot-hook blocker); overlaps (1) — it is the same carry-over table with a
   different debt kind.
8. "Pending-update watch" — `considerthese/2026-10-22.md:20`. Frontier (the pause-lift gate is
   operator-owned); `tools/measure-update-recheck.py` exists but the bot-side reminder does not.
9. "Quiet-day mode" — `considerthese/2026-10-25.md:17` (reflection-bot housekeeping, not a lane
   artifact). "Daily pin-integrity check" — `2026-10-19.md:32-34` (sibling-repo pins; adjacent to
   this round's R47-C2-DIGEST-TRUNCATION defect but pinning is already checked per-row in the C2
   counter). "Daily source-quote sampling" — `2026-10-20.md:50-52` (C2's counted seats do it per
   row already). "Signal-first review path" (`2026-10-20.md:53`), "Stagnation and saturation
   watch" (`2026-10-19.md:38-40`), "Cross-lane receipt watch" (`2026-10-19.md:41-42`), "Round-velocity
   awareness" (`2026-10-23.md:18`), "Late-evidence contradiction watch" (`2026-10-23.md:19`), "Env
   allow-list drift check" (`2026-10-23.md:20`), "Coverage-frontier map" (`2026-10-23.md:21`),
   "Missed-run catch-up" (`2026-10-22.md:18`), "Scope-violation trend line"
   (`2026-10-22.md:19`), "Volume-aware reading order" (`2026-10-22.md:22`), "Promotion-debt ledger"
   (`2026-10-19.md:35-37`), "Live-harm flag for env changes" (`2026-10-24.md:20`): all checked via
   the same grep; none implemented; relevance to this round's three claims is weak or the function
   already lives inside a landed mechanism (e.g. coverage-frontier map ≈ `PROVINCE.md` Frontier
   section; stagnation watch ≈ `SCORECARD.md:177-178` declared N=3).

## Best ONE candidate: "Routed-debt carry-over check"

- **File / date:** `considerthese/2026-10-24.md` (reflection file dated 2026-10-24, committed
  `f0b8f7a5` 2026-10-24 09:32), line 18.
- **Exact words (proposal, 15 words):** "check whether the following round closed each one … and
  report what is carried over and for how long".
- **What it would change:** the per-round "routed defects — disposition" tables are appended under
  each lesson but never consolidated; this adds one table that carries every routed defect id with
  (a) the round that opened it, (b) its first disposition, (c) its current state, (d) rounds since
  opening — so a debt's age is a row value, not something a reader reconstructs across 20+ lesson
  files. Concretely for the L1's close of round 48: the table would immediately show
  R47-C2-TMPDIR-FALLBACK (opened r47, addressed by C1), the GR1-GR3 admission debt (opened r45,
  addressed by C2 across four rounds), K10-style restatement debt (recurring, C3), plus the still
  open older items a `carried` row left behind (`corpus/lessons/round-38.md` rows 2 and 4; the
  `R42-C1-SCRATCH-FALLBACK-TMP` open leg named in `corpus/lessons/round-45.md:153`;
  seat-harm ledger's "no gate reads this ledger", `round-45.md:166`).
- **How the lane's own bar grounds it (what to open):** the reflection is a pointer; the ground is
  the lane's own two artifacts: (1) `corpus/lessons/round-*.md` disposition tables — grep
  `routed defects — round-.* disposition` across `corpus/lessons/` gives the row set; (2) the
  frozen counter pattern — the seat-harm mine already built a small checker
  (`.ufo/waves/round-45/a2w1/ConsiderMine/seat-harm-log.py` + `seat-harm.jsonl`, 15 mutants
  killed, `round-45.md:131-132`) proving the lane's bar accepts a lesson-section table whose rows
  bind each entry to a lane cite and are shown able to fail. A carry-over table's entries bind to
  the routed-defect rows by id (`R4x-*`, `D<n>`), each row's quote sitting on its cited line — the
  same binding shape.
- **Can it land as a QUALITY.md criterion or lesson this round without a new claim?** Yes — as a
  `### considerthese — routed-debt carry-over check` section in `corpus/lessons/round-48.md`, the
  established landing shape (r37 declined-with-reason, r45 ledger-with-rule, r46 measured-rule
  precedent all used a lesson section). It should NOT become a QUALITY.md row: QUALITY 78+ entries
  are declaration-time gates on frozen predicates/controls, while this proposal is a ledger the
  closure writes at integration; round 47 kept the same distinction (`round-47.md:71` mined the
  scoreboard into the lesson rather than QUALITY). It needs no new claim because `SCORECARD.md:3110`
  already names exactly this item ("one proposal mined by a wave scout, landed only if the lane's
  own bar grounds it").

### Exact proposed text (for `corpus/lessons/round-48.md`, under "## Assimilation and considerthese")

```
### considerthese — routed-debt carry-over check (`considerthese/2026-10-24.md`, proposal "Routed-debt
carry-over check", filed 2026-10-24)

Mined: "check whether the following round closed each one … and report what is carried over and for
how long." The disposition tables under each lesson's "Round-N routed defects" heading name states,
not ages. Consolidated rows below; each id cites the lesson line that opened it and the line that
last named it, so an open debt's age is a row, not a reconstruction.

| Debt | Opened | Last named | Rounds open | State this round |
|---|---|---|---|---|
| GR1-GR3 scrub-row admission (C2 arc) | r45 (`round-45.md:227-236`) | round-48 C2 declaration (`SCORECARD.md` "Round 48") | 4 | addressed — counted seats of w2 |
| R47-C2-TMPDIR-FALLBACK | r47 (`round-47.md:45`) | round-48 C1 declaration | 1 | addressed — the /proc/self/fd alias, `static_ok` leg |
| K10/K13/K17 self-assessment restatement | r28 (`round-28/w1/CritAxisHarm.md` §9 pattern) | round-48 C3 declaration | recurring | addressed at round end by restatement |
| counter free-sha/no-freeze (round-38 routed 2) | r38 (`round-38.md` row 2) | `round-38.md` row 2 only | 10 | open — no later row names it |
| V8-mutant-per-fix + dynamic channel (round-38 routed 4) | r38 (`round-38.md` row 4, "carried") | `round-38.md` row 4 only | 10 | open — attaches to any future re-claim |
| R42-C1-SCRATCH-FALLBACK-TMP residual | r42 (`round-45.md:153`) | `round-45.md:153` ("open ×1") | 6 | open — counter still takes `--scratch` optionally |
| seat-harm ledger unread by a gate | r45 (`round-45.md:166`) | `round-45.md:166` | 3 | open — no tool reads the ledger |
| R16-FALSIFY waived obligation | r16 (`2026-10-20.md` "Waived-obligation tracker") | lesson errata only | 32 | open — never exercised |

Rule taken: a routed defect may be marked "carried" at most once before it appears in this table
with its age; anything older than the stagnation window (N = 3) without a re-dispatch is reported as
lapsed, not open — matching the verified-rate ledger's rule that a rate inferred without a fixed
outcome source is not a measurement (`corpus/lessons/round-37.md:64-66`). Rows cite `round-*.md`
lines; the table is rebuilt at each round's integration from `git grep -n "routed defects —
round-.* disposition" corpus/lessons/` plus this table's prior rows.
```

(Line numbers in the draft table are the observer's pointers to open, not fresh measurements — the
L1 should re-resolve them at integration.)

## Residual unknowns

- Whether the L1 wants the ledger appended inside `round-48.md` (recommended here) or as a standing
  `corpus/knowledge/` note with a counter; the lesson-section shape is the one the declaration's
  "no new claim" clause permits without a counter.
- The exact open state of debts older than r38 (e.g. `R16-FALSIFY`, the mkinitcpio hook blocker) was
  verified only by grep absence at the freeze revision, not by re-running their original checks.
