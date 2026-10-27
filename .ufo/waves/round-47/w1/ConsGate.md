VERDICT: draft

# ConsGate — considerthese mine, round 47 w1

Seat ConsGate (L2 leaf, tsukuroi r47 hyaku 10, wave w1). Item F-3. Lane read-only; writes are this
report and `ConsGate/receipts.txt` only. Scratch `/fast/scratch/hyaku/tsukuroi-r47/ConsGate` used for
nothing but `mkdir -p`/`pwd` and removed at exit. Method and raw outputs: `ConsGate/receipts.txt`.

## 1. What was read

- `ls /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/considerthese/` — 7 operator files
  (2026-10-19/20/22/23/24/25/26). Newest three read in full: `considerthese/2026-10-24.md`,
  `considerthese/2026-10-25.md`, `considerthese/2026-10-26.md` ("Self-improvement ideas (proposed
  only, not acted on)" — 14 proposals total: 5 + 4 + 5).
- Implementation status of every proposal checked against committed lane content only
  (`SKILL.md`, `corpus/lessons/`, `corpus/QUALITY.md`, `corpus/SOURCES.md`), with prior mining-seat
  reports in `.ufo/waves/round-4*/` as corroboration (receipts §2).
- Round-47 work surface: `.ufo/waves/round-47/make-w1-spec.py` seat list (64 seats) and git log
  (receipts §3-4); `corpus/SOURCES.md` S246-S249/S252 rows and `.ufo/waves/round-47/frozen/src/FETCH.txt`
  (receipts §5); `corpus/QUALITY.md` sweep (receipts §6).

## 2. Status of all 14 proposals

| # | Proposal (file:line) | Status | Evidence |
|---|---|---|---|
| 1 | Burst-aware reading (2026-10-26.md:17) | **LANDED** (round 46) | `corpus/lessons/round-46.md:97-107` section + "Rule taken" at :106; mined by seat ConsiderMine (`.ufo/waves/round-46/w1/ConsiderMine.md`, verdict draft; 28 comparable LOG-vs-spotcheck statements on rounds 43-45, 3 disagreements, all status/harm wording). See §4. |
| 2 | Counter-attack scoreboard (2026-10-26.md:18) | landed (round 41, continued r42) | `SKILL.md:3833` "## Counter-attack scoreboard — rounds 40-41"; `SKILL.md:3935-3943` round-42 continuation; `SKILL.md:3122-3123` registry rows; `corpus/lessons/round-41.md:99` |
| 3 | Seat-harm incident log (2026-10-26.md:19) | landed (round 45) | `corpus/lessons/round-45.md:124` section header, ten-row ledger + `seat-harm.jsonl` receipt, 15/15 mutants killed (:132-135, :163) |
| 4 | Downstream patch-offset check (2026-10-26.md:20) | landed (round 42) | `corpus/lessons/round-42.md:53`; `w1/ConsiderPatchOffset/patch-offset.py` (108 pins, 15 drifting); offset NOTEs appended to knowledge notes |
| 5 | Cross-note correction propagation map (2026-10-26.md:21) | landed (round 43) | `corpus/lessons/round-43.md:83` |
| 6 | Quiet-day mode (2026-10-25.md:9) | **unimplemented** | 0 hits in `SKILL.md`/`corpus/lessons/`/`corpus/QUALITY.md`/`corpus/SOURCES.md` |
| 7 | Next-round pickup sheet (2026-10-25.md:10) | **unimplemented** | 0 hits ("pickup") |
| 8 | Probe lineage table (2026-10-25.md:11) | landed (rounds 38/40/42) | r38 `w1/ProbeLineage.md:41-44` (probe lineage from committed bytes); r40 counter lineage (ConsiderLineage/ConsiderLineageVerify); `SKILL.md:3926-3931` "Counter lineage — round 42 rows" |
| 9 | Evidence-weight watch (2026-10-25.md:12) | landed (round 39, measured r41) | `corpus/lessons/round-39.md:94`; `corpus/lessons/round-41.md:105` |
| 10 | Upstream release watch (2026-10-24.md:9) | **unimplemented** | 0 hits ("release watch"/"upstream watch") |
| 11 | Routed-debt carry-over check (2026-10-24.md:10) | **unimplemented** (as a standing check) | 0 hits; only unrelated round-29 spotcheck usage of the words |
| 12 | Seat-loss tally (2026-10-24.md:11) | **unimplemented** | 0 hits ("seat-loss") |
| 13 | Live-harm flag for env changes (2026-10-24.md:12) | **unimplemented** (as a standing flag) | only the round-36 XDG_RUNTIME_DIR narrative at `corpus/lessons/round-36-verifier-spotcheck.md:97`, not a flag/criterion |
| 14 | Claim-arc length (2026-10-24.md:13) | **unimplemented** | 0 hits ("claim-arc"/"claim arc") |

## 3. Relevant-and-unimplemented items (the answer)

Relevance filter: this round's claims — C1 counter/verdict binding (`tools/check-scrub-admission-r47.py`,
18 counted seats binding `ROW GR<n> VERDICT:` + `SECTION SHA256:` first lines), C2 selftest harness
robustness (`tools/tsukuroi-census.sh` TMPDIR-space fix, `root_locator_class` fixture-base derivation,
164-case selftest), C1 scrub grounding (GR1/GR2/GR3 of
`corpus/knowledge/btrfs-scrub-grounding-r45.md`, sources S246-S249 pinned Linux v7.2.11 / systemd
v262 / btrfs-progs v7.1). Four proposals pass both filters:

### 3.1 Upstream release watch — relevant to scrub grounding; NOT covered this round

- **Points at:** the corpus pins upstream artifacts by tag — S246/S247 pin Linux `v7.2.11`
  (`corpus/SOURCES.md:255-256`), S248 pins `systemd v262` (:257), S242/S243/S237 pin btrfs-progs
  v7.1 `scrub.c`/`sysfs.c`; GR3 grounds stop semantics on systemd v262. The proposal: watch the
  pinned upstreams and flag notes whose pinned version falls behind the latest release before a
  round trips over it (as round 36 tripped over systemd 262's `-F` change).
- **Already covered? No.** The registry has a `recheck:` cadence column (`on-release` for
  S246-S248, `30d` S249, `180d` S252 — receipts §5) and QUALITY criterion 8 (`corpus/QUALITY.md:8`)
  requires the column to exist, but nothing executes the watch: no round-47 seat compares a pinned
  tag against the current upstream release (nearest seats: `C2ScoutMktemp` re-opens S252 only,
  `SrcGate` curates rows). The host kernel is 7.2.11 (`workstation` context) — S246/S247's pin —
  so the watch's live question "is v7.2.11 still the host's kernel line, and is it still latest
  stable?" is unasked this round.
- **What would land it:** (1) a standing w1 scout seat (like this one) that each round lists every
  `kind: code|docs` registry row, its pinned tag, the latest upstream release at read time, and the
  delta, reporting to the sources gate; (2) a QUALITY criterion making that sweep a named, receipted
  check (criterion 8's recheck column becomes measured, not just present); (3) a lesson row in
  `corpus/lessons/round-47.md` recording the first sweep's result. A SOURCES row alone cannot land
  it — the rows and cadences already exist; the watch mechanism is the missing half.

### 3.2 Routed-debt carry-over check — relevant to counter/verdict binding; PARTIALLY covered this round

- **Points at:** each verifier spot-check ends with routed defects; the proposal checks whether the
  following round closed each one and reports carry-over age. Directly on-axis this round: round 47
  exists because rounds 44-46 closed badly (three consecutive rejected closures), and the GR2
  amendment ("filesystem-closing `-EAGAIN` check leads the ordering; suspend narrowed to the
  unmount path", `git log` 3629c46a) is itself the closure of a round-46 routed residual — the
  counted counter binds verdicts on the amended bytes only.
- **Already covered? Partially, once.** Seat LessonScribe (item F-4, `.ufo/waves/round-47/make-w1-spec.py:181`)
  drafts the "## Round-46 routed defects — round-47 disposition" table for `corpus/lessons/round-47.md`
  (D1-D10 + carried items, each with state at 77e9e2b2 and an evidence command). That is exactly one
  instance of the proposal (round-46 debts → round-47 disposition). But the standing mechanism —
  every spot-check's debt list checked against the next round, with carry-over age — is not
  implemented: no QUALITY criterion requires the table, and no seat next round is bound to repeat it.
- **What would land it:** a QUALITY criterion: "a round's lesson carries a disposition row for every
  routed defect named in the previous round's verifier spot-check, each with state and an evidence
  command at the measured revision; debts carried two or more rounds are named with their age."
  Round 47's LessonScribe output is the first instance and can be cited as the passing example; the
  lesson section records adoption. No SOURCES row is needed (this is a process gate, not a source).

### 3.3 Live-harm flag for env changes — relevant to selftest harness robustness; NOT covered this round

- **Points at:** when a round changes child-process environments, check whether a live-oracle seat
  validated the change against real desktop/systemd state, and flag rounds where only leak counts
  were measured. Direct ancestor: round 36's allow-list over-strip broke the systemd plane via
  `XDG_RUNTIME_DIR` (`corpus/lessons/round-36-verifier-spotcheck.md:97`; the live-oracle catch is
  why that lesson exists).
- **Already covered? No.** Round 47's C2 deliberately changes child-env handling — the counting
  command runs `env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" bash tools/tsukuroi-census.sh
  --selftest` and the harness now derives a classifiable fixture base (`root_locator_class`
  charset, falling back to `/tmp`). The round's kill rules bind `--identity` line shape and
  byte-identity of output — but no seat runs the changed census under the *ambient* host
  environment as a live-oracle control (e.g. `bash tools/tsukuroi-census.sh --identity` with the
  real env, proving the `root_locator_class` derivation does not misfire on this host's actual
  `TMPDIR`/locale). Seat `C2SentTmp` attacks tmp-fallback safety adversarially, which is adjacent
  but not a live-harm receipt.
- **What would land it:** a QUALITY criterion: "a round that changes the child-environment
  construction of a counted tool must include a live-oracle receipt against the real host state
  (for the census, `--identity` and one selftest case under the ambient environment; for
  systemd-plane tools, `systemctl is-system-running`); leak counts or byte-identity alone are not
  evidence of no harm." Failing example already in hand: round 36 pre-repair. Landing artifact: the
  criterion plus one lesson row; a receipt would live in the seat's dir like other wave receipts.

### 3.4 Claim-arc length — relevant to scrub grounding; NOT covered this round

- **Points at:** track how many rounds a single goal has run without a verified close, so it is
  visible when the instrument, not the fix, needs the round. The scrub-grounding goal (GR1-GR3) has
  run rounds 44 → 45 → 46 (rejected) → 47 with no verified close; round 47 is declared a fresh-start
  round after three consecutive rejected closures. That is precisely the situation a claim-arc
  counter surfaces — the same way the proposal's motivating example was the allow-list goal's
  six-round arc (rounds 31-36, `considerthese/2026-10-24.md:13`).
- **Already covered? No.** The round-47 declaration (`SCORECARD.md` "Round 47 — declaration", freeze
  77e9e2b2) names the claims, the freeze revision, the counted seats, and the amendment — but no
  lane surface states the GR arc length or a stale-goal alarm. No round-47 seat tracks it
  (`ScoutQuality` sweeps existing criteria; none covers arcs).
- **What would land it:** a QUALITY criterion or a standing SCORECARD declaration element: "each
  declaration names every open goal's arc length in rounds since first declared without a verified
  close, and states whether the current blocker is the instrument or the fix." Landing artifacts:
  the criterion (QUALITY.md) + the first measured row in the round-47 or round-48 declaration
  ("scrub grounding: arc 4 (r44→r47); three rejected closures; instrument = verdict-binding counter,
  fix = GR amendment landed r47"). No SOURCES row needed.

## 4. Burst-aware reading — round-46 check (assigned follow-up)

**Landed; not still open.** Round 46's ConsiderMine seat mined it (the only then-unmined
2026-10-26 proposal; the other four were mined in rounds 41/42/43/45 — verified by grep at
`.ufo/waves/round-46/w1/ConsiderMine.md:15-18`). It is committed as a lesson rule:
`corpus/lessons/round-46.md:97-107` ("Rule taken" at :106: a burst read opens with the window's
round count and compares LOG and spot-check field by field; numeric agreement is weak evidence and
never replaces a receipt). The mechanical checker (`w1/ConsiderMine/check-log-axis-coverage.py`)
remains wave evidence, not a lane gate, and no QUALITY criterion encodes it — so "landed as lesson
text; not mechanized" is the precise state. LOG.md:1668-1669 records the mining under round 46.

## 5. Unimplemented but NOT relevant to this round's claims (filtering shown for completeness)

- **Quiet-day mode** (2026-10-25.md:9) — reflection-writing process when no commits land; touches no
  counter, selftest, or grounding surface.
- **Next-round pickup sheet** (2026-10-25.md:10) — assembling open debts during pauses is
  operator-side planning; adjacent to §3.2 but not itself a lane-verifiable binding/robustness
  mechanism. Its substance arrives via §3.2's disposition table instead.
- **Seat-loss tally** (2026-10-24.md:11) — provider `cyber_policy` holds / silent spawn drops; a
  coverage-attribution concern. The landed seat-harm ledger (round 45) covers seat-to-seat damage;
  loss-to-provider is a different class and off the three named axes.

## 6. What I did not do

- Did not edit `considerthese/` or any lane file (read-only seat); did not run any counter, selftest,
  or census (no seat item required it, and the host guard forbids heavy concurrent runs).
- Did not verify upstream release currency for §3.1 (e.g. query kernel.org/systemd releases) — the
  proposal's implementation status is judged from committed lane bytes per the item; the live
  comparison is the future seat's job, not this report's.
- Line numbers cited are from the working tree at HEAD f6bc6d05; `corpus/lessons/round-47.md` does
  not exist yet at this revision (LessonScribe's F-4 target), so §3.2's "first instance" is the seat
  item, not committed text.
