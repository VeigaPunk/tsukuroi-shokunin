# ConnectorOverlap — sibling-overlap scan, considerthese assimilation item, r98 carry-over check

Round 99, wave w1, seat `ConnectorOverlap` (connector; leaf member, no dispatch).
Lane `tsukuroi-shokunin` (host operability & system repair), campaign hyaku run 15.
Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; HEAD `f107da3afe511f7db8cdc30235a992b774903158`
(read-only: `git rev-parse HEAD`; no git/jj mutation was run, no commit was made anywhere).
Judged on depth and freshness; no claim of this round is measured by this seat.

Receipts (all written by this seat, all under `.ufo/waves/round-99/w1/ConnectorOverlap/`):

| receipt | what it holds |
|---|---|
| `instruments-check.txt` | `sha256sum -c .ufo/waves/round-99/before/instruments.sha256` → 16 `OK`, rc 0 |
| `scan-surface-a.txt` | surface A ("registry drift / cell binding") sweep over all 20 sibling corpora |
| `scan-surface-b.txt` | surface B ("battery metadata assertion / selftest lie kind") sweep over all 20 sibling corpora |
| `scan-surface-b-named-lanes.txt` | the five prompt-named lanes plus tameshi, bounded P2 scan (annex) |
| `carryover.txt` | CO-1/CO-2/CO-3, the three r98 carry-over lines measured against this tree |
| `considerthese-pick.txt` | all five proposals of the newest batch, byte offsets, implementation checks |
| `connector-move.txt` | the one bounded move: the missing ECHO witness for the Y-cap family |
| `report.md` | this file |

## 0. Axes named (godspeed, step 1)

Two contract axes are in play and one is the seat's own:

- **depth** — C1: does the r99 battery actually assert the two fields its clauses name, on the X- and
  Y-cap families, and does its selftest see the assertion removed?
- **freshness** — C2: does the registry checker refuse a hybrid / restated cell, and does its selftest
  exercise the ancestor branch?
- **adjacency** (the seat's axis, not a claim axis this round) — is this ground already owned by a
  sibling, and does the newest reflection batch still have an executable item?

The moves kept are the ones that improve one of the first two or the third **and harm none**: no
sibling file written, no campaign tool run, no instrument touched, no claim edited.

## 1. Tooling / environment record

- Host `python3` 3.14.8, `/usr/bin/git` 2.56.0, GNU grep/sed/awk/diff; all sweeps read-only.
- **Zero installs, zero upgrades, zero removals.** pacman is paused host-wide and was not invoked.
  Nothing was written to `~/.local/bin`, PATH directories, host sysctls, services, kernel parameters
  or `/boot`. No `sudo`.
- Scratch `/fast/scratch/hyaku/tsukuroi-r99/ConnectorOverlap` used for two hit lists and one rc probe;
  **deleted before yield** (`test -e` → absent, §10).
- `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` read before the sweeps:
  `/fast/scratch/hyaku` 61 % used, 320.5 G free; `/tmp` 63 %, 48.1 G free. No ENOSPC.
- **Seat-to-seat harm, disclosed not inferred (QUALITY 110 / 75):** at ~11:24 -0300 seat
  `CriticClaims-21` ran `rm -rf /fast/scratch/hyaku/tsukuroi-r99` (the shared parent) and disclosed
  it (its own §7b, message time 11:24 -0300). **Effect on this seat: none** — this seat's scratch dir
  had already been removed at 11:23 as its binding rule requires, and all eight receipts live in the
  lane seat dir, re-listed intact after the disclosure. Recorded here for the round's tally; no
  action taken and no re-run needed.
- No sibling file was written; no `tools/make-r99-bends.py` or earlier `make-r*-bends.py` was run.

## 2. Instrument freeze check (supporting; CO-1)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-99/before/instruments.sha256
tools/limine-pin-battery-r99.py: OK
tools/make-r99-bends.py: OK
tools/check-registry-content-r99.py: OK
tools/check-limine-pins.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-99/before/controls/do-nothing-checker-r98.py: OK
.ufo/waves/round-99/before/controls/bends/N09-y-era.py: OK
.ufo/waves/round-99/before/controls/bends/N11-x-era.py: OK
.ufo/waves/round-99/before/dev/make-fixtures.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/plans/round-99.md: OK
  rc=0  OK_lines=16  listed=16
```

PASS — 16/16 listed files present and byte-identical to the frozen manifest, exit 0. Receipt
`instruments-check.txt` (the same run, redirected).

## 3. Surface A — "registry drift / cell binding" — hit table

Sweep (read-only; tsukuroi excluded; `.md` only; all 20 sibling lanes):

```
$ cd /home/vgpnk/Projects/shokunin
$ grep -rnIE --include='*.md' \
    'registry drift|registry-cell|cell binding|row-id.reader|registry-cell-unchanged' \
    ./*-shokunin/corpus/ | grep -v '^./tsukuroi-shokunin/'
→ 48 line hits in 39 files across 13 lanes
```

Exact round-99 tokens, zero-hit screen (complete, every sibling corpus):

```
RC-BEND-SPAN 0 · RC-CELL-MISSING 0 · RC-CELL-AMBIGUOUS 0 · check-registry-content 0   sibling files
```

Decision codes: **(a)** genuinely the sibling's domain → report, never absorb (handoff row named);
**(b)** generic technique both lanes may hold; **(c)** this lane's own ground.

| sibling | file:line | relevance | decision |
|---|---|---|---|
| kumitate | `corpus/QUALITY.md:875` (Q47) | "the lane's registry drifted to four live duplicate groups" — SOURCES-registry drift caught by `scripts/sources-census.sh` W04, which never gates | (b) generic: mechanical registry-drift detection; the SOURCES registry is kumitate's own ground |
| kumitate | `corpus/knowledge/layer-axes.md:304` | "one row of registry drift away from moving" — axis-score registry drift | (a) kumitate's own axis bookkeeping; no handoff needed for a reading, name only |
| kumitate | `corpus/README.md:296` (+ `knowledge/row-id-reader-class.md`) | registry row ids read as the census `row_pass` grammar (LF records, 0-3 SP indent, SP/TAB pad) | (b) closest sibling analogue to C2's cell capture; different registry (SOURCES ids), same technique |
| kumitate | `corpus/README.md:297`; `lessons/round-100.md:1,32,44,78`; `lessons/round-100-verifier-spotcheck.md:127` | round-100 row-id readers, "M2 undrawn-class arms", capture binding | (b) generic: selftest arms for an undrawn reader class |
| kumitate | `corpus/SOURCES.md:235,236` | MDN rows for `^`/`$` boundary assertions and the ECMAScript line-terminator set | (b) generic: the *source* for a boundary-guard argument (C2's `(?![0-9,-])` is exactly this class) |
| kotoba | — | **zero hits on this surface** | — re-derived, not assumed (see §3.1) |
| kake | `corpus/lessons/round-82.md:37,172` | `d1-registry-cell-unchanged` mutant; "item_d1 reads the two cells from the registry and never a sentence" | (b) generic: a mutant whose only defect is a stale registry cell — the nearest sibling analogue to C2's binding |
| kake | `corpus/lessons/round-59-verifier-spotcheck.md:128` | "S425's scope-cell overstatement … is a registry-cell defect, not a false entry" | (b) generic: cell defect ≠ entry defect, the distinction C2 enforces |
| kake | `corpus/knowledge/ops-automation.md:87` | `grokbots [--check\|--status]` "keeper roster health: cards, registry drift, last probe" | (a) kake's own keeper tool; not this lane's ground |
| kagi | — | **zero hits on this surface** | — re-derived (see §3.1) |
| kama | `corpus/lessons/round-65-verifier-spotcheck.md:136` | "the registry drift repaired by 20 registrations" | (a) kama's own registry; not this lane's ground |
| kaidoku | `corpus/knowledge/2026-11-04-r71-registry-grammar.md:14`; `README.md:382`; `lessons/round-71.md:5` | "the registry drift census reads its own block" — a grammar census over its own SKILL registry block | (b) generic: a registry-grammar census with its own reader class |
| kaidoku | `corpus/lessons/round-77-verifier-spotcheck.md:125` | "red fixtures for … the path-from-another-cell binding" | (b) generic: a should-fail fixture for a cross-cell binding — the shape C2's `ancestor` case is |
| chousa | `corpus/QUALITY.md:1140` (183) | "a registry-cell rule is scoped by a phrase, not by a vocabulary, and a flagged row needs a disposition" | (b) generic; chousa's SOURCES registry is its own ground |
| chousa | `corpus/lessons/round-81.md:79`; `lessons/round-89.md:158` | registry-cell edits with no existing cell changed | (b) generic |
| kengaku | `corpus/QUALITY.md:1146`; `lessons/round-52.md:64`; `lessons/round-53.md:28` | `false-registry-cell` / `counter-reachable-without-the-work` classes | (b) generic: cell binding that a counter reaches without the work |
| kengaku | `corpus/lessons/round-56.md:42` | "a registry-cell edit added a pipe into an 8-cell row; the r52 counter's pipe-splitter dropped the row" | (b) generic — **the closest precedent to C2's capture-fidelity problem**: a cell edit defeating a parser, fixed by a splitter repair |
| kengaku | `corpus/evidence/round73/w1/c2-row-fix.md:1` | "two registry-cell corrections" (SKILL lines 600/682) | (b) generic |
| kengaku | `corpus/lessons/round-75-verifier-spotcheck.md:198`; `lessons/round-76-verifier-spotcheck.md:189` | "R75-D4 / R76-V2 (registry drift) — routed": rows pinning superseded values | (b) generic — the drift class C2 binds |
| kengaku | `corpus/lessons/round-99.md:108` | M5 "registry-cell convention not checked before C" | (b) generic |
| kengaku | `corpus/README.md:98,558,919,921`; `lessons/round-32.md:41`, `round-58-verifier-spotcheck.md:290` | README index / row-edit history / cell refreshes | (b) generic bookkeeping; listed for completeness |
| revenger | `corpus/lessons/round-68.md:96` | M46 "landing/registry drift — the authoritative registry row was not re-derived from the repaired instrument's bytes after a repair" | (b) generic, and *the same predicate as C2*: a registry row bound to the tool's bytes |
| revenger | `corpus/lessons/round-62-verifier-spotcheck.md:51`; `round-63-verifier-spotcheck.md:47` | census re-runs of the shared `scripts/sources-census.sh` | (a) the fleet census is tameshi's declared Core surface (ADJ-07) — see §3.2 |
| mado | `corpus/lessons/round-83-verifier-spotcheck.md:123` | "R1 — gate-registry drift at the registry home. SKILL.md §Gate registry carries …" | (b) generic: the gate-registry drift class tsukuroi's `check-registry-content` binds |
| mado | `corpus/lessons/round-72-verifier-spotcheck.md:144` | "defects routed below are documentation/registry drift (stale selftest tallies …)" | (b) generic |
| souji | `corpus/lessons/round-18.md:98` | "SKILL registry drift. souji-seat-audit row said 49 selftest cases …; the tool runs 66" | (b) generic: a registry row's declared case count vs the tool's bytes — exactly C2's measured surface |
| mori | `corpus/lessons/round-14.md:37` | supersession wording, matched only on "registry-cell" in a quote | (b) incidental; listed for completeness |
| kasegi | `corpus/lessons/round-60.md:3` | round header, matched on incidental vocabulary | (b) incidental; listed for completeness |
| kotodama | `corpus/lessons/round-54-verifier-spotcheck.md:72`; `round-55.md:19` | "three registry-cell items are carried" | (b) generic; kotodama's own registry |
| game-dev-2d | `corpus/live/r95-scribe/RECEIPTS.md:42` | "own-cell binding … 35/35 r95b bound to own boundary cells" | (b) homonym-adjacent: boundary cells, not registry cells; listed for completeness |

### 3.1 kotoba and kagi — zero hits, re-derived

`grep -rnI --include='*.md' -E 'cell binding|registry drift|registry-cell|RC-BEND-SPAN|check-registry-content|check_echo|check_era|visibility_era|lie kind|lie-kind|metadata assertion|field assertion' kotoba-shokunin/corpus/` → no lines. Same for `kagi-shokunin/corpus/`. This is a measured zero, not an omission: both lanes appear in the sweep commands and produced nothing. kagi does own surface-B-adjacent ground under a different vocabulary (`claim-instrument-falsifiability.md`), reported in §4.

### 3.2 A finding the sweep produced: the shared fleet census has one declared owner — tameshi

Every lane cites `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (the ten largest
citation sets run 196–417 files per lane). Four `PROVINCE.md` files name it, and only one declares
it:

```
$ grep -ln "sources-census\|/Projects/shokunin/scripts\|fleet-root scripts" ./*-shokunin/PROVINCE.md
./kagi-shokunin/PROVINCE.md      ← its OWN corpus/sources-census.sh (lane-local homonym, round 21)
./kaidoku-shokunin/PROVINCE.md   ← naming-alias observation (lane dir ≠ lane id), not ownership
./souji-shokunin/PROVINCE.md     ← host path-shape note, not ownership
./tameshi-shokunin/PROVINCE.md   ← declares it
```

`tameshi-shokunin/PROVINCE.md:194-197` (Core, round 90 append): "The fleet's own registry gate,
`scripts/sources-census.sh` in the fleet root (pinned `f47ad6ba`), enters Core as a read-only
primary surface: 'the fleet's existing gates' (line 7) include fleet-root gates, not only
sibling-lane ones."

Decision: **(a) tameshi's domain — ADJ-07 / OUT-010.** A defect in the shared census is reported
there, never repaired from this lane; this lane consumes it read-only, as it did this round
(`before/census-before-after.txt`: 394 rows at `f107da3a` → 395 with the working-tree S395,
after exit 0). ADJ-07's trigger text is "a census blind spot raises a reusable
verification/mutation-testing question", which is the right edge for a census *falsifier*; a plain
tool defect sits at that row's edge and should say so when it is filed.

## 4. Surface B — "battery metadata assertion / selftest lie kind" — hit table

Sweep (read-only; tsukuroi excluded; `.md` only; all 20 sibling lanes):

```
$ grep -rnIE --include='*.md' \
    'assertion removal|lie (kind|class)|lie-kind|selftest.{0,45}(blind|cannot see|sees only)|mutant-kill|reported field|metadata assertion' \
    ./*-shokunin/corpus/ | grep -v '^./tsukuroi-shokunin/'
→ 79 line hits in 68 files across 15 lanes
```

Bare `kill rule` is a generic fleet term (each lane freezes one; 517 files across 12 lanes) and is
**not** part of this surface; its per-lane file counts are in `scan-surface-b.txt` §B.4 as context
only.

Exact round-99 tokens, zero-hit screen (complete):

```
check_echo 0 · check_era 0 · visibility_era 0 · limine_version 0 · LIE_KINDS 0 · metadata assertion 0 · REFUSAL-VERSIONS 0   sibling files
```

| sibling | file:line | relevance | decision |
|---|---|---|---|
| **kumitate** | `corpus/QUALITY.md:329` (Q25) | "a mutation battery has one kill predicate, frozen before any counted run and stated" | (b) generic; the fleet-wide battery discipline |
| kumitate | `corpus/QUALITY.md:1682-1699` (Q95) | a round's close battery runs every lane gate that reads a file the round writes | (b) generic: gate-battery completeness |
| kumitate | `corpus/QUALITY.md:1468` | a claim's kill rule ranges over input classes → at least two members per class per run | (b) generic: population rule for a kill rule (the QUALITY-128 analogue C1 relies on) |
| kumitate | `corpus/lessons/round-51.md:38` | "M2 — a declared kill rule that was never tested against its own control" | (b) generic — the "assertion never exercised by an adversary" class |
| kumitate | `corpus/knowledge/receipt-subject-binding.md:173,209`; `receipt-invisible-prefix-fields.md:35` | a receipt-bind counter that reached 47/47 without the field-line behaviour | (b) generic: a field-level assertion that reads as met without the field |
| kumitate | `corpus/knowledge/row-id-reader-class.md`, `sources-check-registry-section.md:150,153` | "six wrong readers outside the class grid still read HELD" | (b) generic: a closed class grid ≠ an enumeration — the same limit C2's selftest carries |
| **kotoba** | `corpus/SOURCES.md:131` | S120 — Petrović et al., "Practical Mutation Testing at Scale: A view from Google" (arXiv 2102.11378), tier A paper row | (b) generic **source both lanes may hold**; a candidate citation for the lane's kill-direction rule (§8) |
| **kake** | `corpus/lessons/round-86.md:85` | "vacuous / selftest blind spots — Comparator basis-check and R4 flip-conjunct mutants survive selftest 10/10 … MutCounters targeted discriminators" | (b) generic — **the same class and the same fix as C1's lie kinds**: a selftest blind to an assertion removal, closed by targeted discriminators |
| kake | `corpus/lessons/round-38.md:96`; `round-73-verifier-spotcheck.md:85`; `round-95.md:119` | selftests written blind; frozen attack corpus | (b) generic |
| **kagi** | `corpus/knowledge/claim-instrument-falsifiability.md` (C1 §) | "a structural item that tests only **token presence** accepts a sentence that keeps every token and denies the assertion" — five forgeries accepted at `value=0` | (b) generic — **the nearest sibling statement of C1's premise**: a field assertion that tests presence, not the asserted position |
| kagi | `corpus/lessons/round-11.md:166` | "selftest cannot see the default wiring; a liar stub prints PASS — accepted, bounded: a self-test cannot prove its own honesty" | (b) generic, and a *bound* the lane should adopt: the lie kinds falsify fields, they do not prove the selftest honest |
| **kama** | `corpus/QUALITY.md:493` (KQ99) | "A battery gate that claims a named leg's expected outcome is bound to an actual field and exit must fail a one-call control that routes the same `--counter`/`--expect` argument" | (b) generic — **the same criterion as C1**, independently derived: bind the *field*, and add a control that only wins by routing the argument |
| kama | `corpus/knowledge/battery-execution-evidence.md` | what a `sys.setprofile` record of a battery establishes (entry of a named frame) and does not | (b) generic: "the battery ran" ≠ "the battery asserted" |
| kama | `corpus/lessons/round-18.md:295` | "`GateModelsStatus` (tool selftest blind to a relaxed model-status check)" | (b) generic |
| kama | `corpus/knowledge/served-model-identity.md:5` | "these additional commands select only the **reported fields**" — the endpoint-reading sense of the phrase | (b) incidental homonym; listed for completeness, kama's own ground |
| kama | `corpus/lessons/round-56.md:26`; `round-29-verifier-spotcheck.md:40`; `round-82-verifier-spotcheck.md:39` | "the battery's field comparison lacked a negative substring control"; mutant-killing cases | (b) generic |
| **tameshi** | `corpus/knowledge/mutation-case-tsukuroi-census.md` (whole entry) | **a mutation case run on THIS lane's `tools/tsukuroi-census.sh`** (B1-B10, one replacement per defect, control run, per-mutant evidence), including **B9 "roll-line fields (unasserted verdict fields)"** | **(a) tameshi's domain — ADJ-07 / OUT-010**: the reusable mutation/verification method is tameshi's; tsukuroi is the measured substrate. Report, never absorb |
| tameshi | `corpus/knowledge/fleet-kill-rate-ledger.md:47,144-145` | row 3 `tsukuroi · tools/tsukuroi-census.sh (r5) | 26 cases | 6/10 (60 %)`; survivor class **(a) "reported-but-unasserted surface"** with `tsukuroi B9` named | **(a) ADJ-07** — and *the class this round's C1 closes was already on record on 2026-10-14* (§7 contradiction C-2) |
| tameshi | `corpus/knowledge/mutation-score-semantics.md:39` | cross-lane table: `Bash Tsukuroi census 6/4/0; B7 cap, B8 usage exit, B9 reported fields, B10 unreached PCI arm` | (a) ADJ-07; also the composition rule (a rate is never implied to hold at a later revision) |
| tameshi | `corpus/knowledge/mutation-case-kumitate-claims.md:91,98` | same method on kumitate's `claims-check.mjs` (D6 "reported field" killed) | (a) ADJ-07 |
| tameshi | `corpus/lessons/round-58-verifier-spotcheck.md:24` | registry rows re-measured plus counter evidence-verified | (b) generic |
| kaidoku | `corpus/knowledge/2026-11-04-r85-mutant-kill-binding.md` | "a mutant counts as killed only when a named detector's outcome changes under the mutant and does not change on pristine"; sourced S304 (Papadakis et al., mutation-testing survey); limit: a kill binds a **case name**, not the case's semantics | **(b) generic — and it is tameshi's method ground (ADJ-07)**: kaidoku holds the *source*, tsukuroi holds the application. Cite, do not absorb |
| kaidoku | `corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` (§a) | "the kill-rule blind-spot class: a rule that never reaches the gate it asserts … the class generalises beyond this lane" | (b) generic — the exact shape of C1's lie-kind gap |
| kaidoku | `corpus/lessons/round-96.md:130` | `N4 … killed by K-dmain pos exit 1 | selftest blind (no head-binding case)` | (b) generic: a named field the selftest has no case for |
| kaidoku | `corpus/lessons/round-94.md:50` | "the counter's own selftest never exercised the public `--json-out` path" | (b) generic — the ancestor-branch analogue C2 closes |
| kaidoku | `corpus/lessons/round-62.md:44`; `round-94.md:65`; `round-97.md:94`; `README.md:126,278`; `SOURCES.md:220`; `lessons/round-85-verifier-spotcheck.md:193` | method application, kill tables, the S304 row | (a)/(b) as above |
| kasegi | `corpus/lessons/round-76.md:29` | "**M76-3 — semantic RESULT assertion removal survives.** deleting the `res6` assignment makes the amended selftest crash with NameError" | (b) generic — **the identical class to the r98 "lie-kind coverage" gap** |
| kasegi | `corpus/lessons/round-60.md:82` | "the write-flag screen is defeated by token spelling" | (b) generic |
| mado | `corpus/knowledge/control-set-mutant-kill-r73.md:82` | "A set whose mutant-kill fraction is below its mutation count is a set with a named blind spot" | (b) generic: the control set as an instrument |
| mado | `corpus/lessons/round-86.md:29`; `round-100-verifier-spotcheck.md:155`; `round-72.md:131`; `round-25.md:88` | "That selftest blind spot is open"; "finite-set blind spot" | (b) generic |
| mado | `corpus/README.md:185,215`; `SOURCES.md:391,394`; `lessons/round-70.md:57`, `round-77.md:120,122`, `round-80.md:201` | mutant-kill set measured as an instrument; source rows for the reading form | (b)/(a) as applicable to mado's own gate |
| revenger | `corpus/lessons/round-79.md:92`; `round-79-verifier-spotcheck.md:93` | "`selftest: blind comparator accepted mutated receipt`" | (b) generic: a blind comparator reads PASS on a mutant |
| revenger | `corpus/lessons/round-82.md:140`, `round-83.md:143`, `round-84.md:115`, `round-85.md:110`, `round-86-verifier-spotcheck.md:97`, `round-87.md:46,125`, `round-87-verifier-spotcheck.md:78`, `round-88.md:56`, `round-82-verifier-spotcheck.md:181`, `round-83-verifier-spotcheck.md:34`, `round-84-verifier-spotcheck.md:96`, `round-85-verifier-spotcheck.md:104` | per-round `sweepN-mutant-kill-after.log` / `negctl-mutant-kill-after.log` receipts: one-substitution mutants with committed kill receipts | (b) generic — the receipt *shape* a one-clause bend should carry |
| revenger | `corpus/knowledge/round-62-evm-dispatch-byte-evidence.md:219`; `corpus/live/runs/round-40/reviewer.md:28` | "the saved records supply the reported fields, never the expected ones" | (b) generic: reported-vs-expected separation |
| souji | `corpus/README.md:1030` | "A mutant-kill tally binds each receipt to the mutant it is filed under (frontier)" | (b) generic — the receipt-name/subject binding the r98 mistake R98-RECEIPT-NAME-MISMATCH needs |
| souji | `corpus/lessons/round-20.md:17`; `QUALITY.md:99,353`; `lessons/round-17.md:7`, `round-70.md:68`, `round-76-verifier-spotcheck.md:43` | "A durable revision with an incomplete measured path list does not bind all reported fields"; "the selftest kills the four r69-found instrument blind spots" overreach | (b) generic |
| chousa | `corpus/lessons/round-35.md:31` | "the selftest alone cannot see the defect" (`offsets=1 first=5`) | (b) generic |
| kotodama | `corpus/lessons/round-62.md:75`, `round-73.md:112`, `round-81.md:137` | "contract gaps the fixture cannot see"; a counter that read the worktree not the committed ledger | (b) generic |
| mori | `corpus/knowledge/census-cgroup-levels-r45.md:1,11` | "a selftest that cannot see the switch" — a silent preference order | (b) generic — *and* mori is a lane this one routes host pressure to (ADJ-04) |
| mori | `corpus/lessons/round-93.md:54`; `round-38.md:50`; `round-59-verifier-spotcheck.md:41,106`; `QUALITY.md:592`; `README.md:871` | "three conjuncts that no frozen control flips"; mutation adequacy | (b) generic |
| kengaku | `corpus/lessons/round-42-verifier-spotcheck.md:102`; `round-43-verifier-spotcheck.md:139` | "attributed-mutant-kills"; "value-attributed mutant kills" | (b) generic: attribution of a kill to a measured leg |
| tabi | `corpus/lessons/round-62.md:73`; `README.md:919,971` | "NOT the old mutant-kill" (a leg that does not inherit a kill) | (b) generic |

### 4.1 The one overlap that is a *sibling's own ground*, not a shared technique

`tameshi` holds the fleet's mutation-testing method (ADJ-07 / OUT-010, quoted in `PROVINCE.md:52`:
"A census blind spot raises a reusable verification/mutation-testing question" → tameshi, evidence
"Minimal failing behavior, command/exit, measured census revision and expected domain invariant; ask
for method advice, not transfer of gate ownership or a general claim from one lane"). Its
`mutation-case-tsukuroi-census.md` and `fleet-kill-rate-ledger.md` row 3 measured **this lane's own
census** and named the survivor class this round's C1 closes. That is method ownership on this
lane's substrate: reported under ADJ-07, never absorbed. Under ADJ-07's own text the lane keeps its
gate; only the method question is theirs.

## 5. Surface C (this lane's own ground) — what no sibling holds

All nine tsukuroi-specific tokens are at **zero** sibling files:
`check_echo`, `check_era`, `visibility_era`, `limine_version`, `LIE_KINDS`, `REFUSAL-VERSIONS`,
`RC-BEND-SPAN`, `RC-CELL-MISSING`, `RC-CELL-AMBIGUOUS`, `check-registry-content`. No sibling lane
names the gate, the battery families, the registry checker or its finding ids, so **the limine pin
gate, the 105-family battery and the registry-content binding are this lane's own ground** (decision
(c)), consistent with `PROVINCE.md` Core ("boot health") and its refusals (no sibling is routed boot
state).

## 6. considerthese — the single pick

Newest batch: `considerthese/2026-10-26.md` (7 files on disk, newest is 2026-10-26; batch sha256
`6f49c88d95d5f072678dfdf8cc6f3cff21207e14396924fa4bf7d6d2afdac50b`, 4551 bytes). Byte offsets
measured with `bytes.find` on the raw bytes, not a decoded index (QUALITY 141):

| proposal | BYTE | implementation state (measured this round) |
|---|---|---|
| Burst-aware reading | 3198 | implemented as `corpus/QUALITY.md:219` (112), adopted r80 |
| Counter-attack scoreboard | 3487 | implemented as `corpus/QUALITY.md:226` (115) |
| Seat-harm incident log | 3768 | implemented as `corpus/QUALITY.md:215` (110), a `## Seat harm` table per round lesson |
| **Downstream patch-offset check** | **4027** | **partial and still open** — rule at `QUALITY.md:201` (103, r69); the automated leg is not built |
| Cross-note correction propagation map | 4281 | implemented as `corpus/QUALITY.md:211` (108) |

**Pick — "Downstream patch-offset check", quoted from `considerthese/2026-10-26.md:20`:**

> **Downstream patch-offset check.** Round 40 found an Arch patch shifts util.c lines after :675 by +5. I could flag any knowledge anchor that cites upstream line numbers for code the host runs as a patched Arch build, so line pins don't silently drift.

**The file it points at** — `corpus/knowledge/pacman-exec-environment-r40.md`, opened. It already
carries the offset, in its appended "Wave-1 corrections — packaging patch" section (line 110):

> **Line numbers are upstream 54d9411, not the installed build** (seat C2RevenPatches). Of the four patches the Arch package applies (PKGBUILD:51-55), `0001-libalpm-invalidate-curl-data-in-child.patch` inserts 5 lines into `_alpm_run_chroot` after util.c:675, so in the installed source every cited util.c line after :675 (EX1 :677-687, EX2 :722-726, EX3 :688-698) sits 5 lines later

**Implemented? No, not as a gate.** Measured:

```
$ grep -n 'Patch-offset host-build check' corpus/README.md
844:- Patch-offset host-build check (considerthese/2026-10-26.md "Downstream patch-offset check", partial): needs a host-build measurement outside the frozen legs.
$ grep -n 'patch-offset\|patch_offset' tools/*.py | head -5
(no output — no tools/ instrument)
$ grep -n 'ConsiderPatchOffset' SKILL.md
3956:  `alpm-package-anatomy-r41.md`; check `.ufo/waves/round-42/w1/ConsiderPatchOffset/patch-offset.py`).
```

So three parts exist — the QUALITY 103 rule (r69), the r40 offset paragraph, and a one-off probe
(`.ufo/waves/round-42/w1/ConsiderPatchOffset/patch-offset.py`, 20506 B, with `out.json`, `run.txt`
and five patch files: a wave artifact, not a registry gate) — and **no re-runnable instrument, no
`tools/` file, no SKILL gate row**. The frontier row is still open.

**Lesson candidate (one paragraph).** A line pin taken from an upstream tag is not a host-build line
number, and the lane has so far enforced that only as prose: `QUALITY` 103 tells a writer to state the
offset, the r40 entry states the one measured offset (+5 after `util.c:675`), and a one-off wave probe
measured 108 pins once at r42 — but nothing re-derives the offset when the host package moves, so the
pin drifts silently exactly as the proposal predicted. The executable form is a committed instrument
that reads a *declared* anchor table (upstream file, pinned line, upstream commit, host package
version) and compares the pinned text against the host's installed bytes through its packaging patch
set, printing one line per anchor and a count; the rule stays documentation-only until such an
instrument exists, which is why the frontier row has survived 30 rounds.

**Falsifiable next-round claim sketch (a sketch, not a claim; this round freezes nothing).**
Land `tools/check-anchor-offsets-r100.py` plus its registry row (QUALITY 70) and its should-fail
battery (QUALITY 73/72). Predicate: `python3 tools/check-anchor-offsets-r100.py --revision <pre-round
tip>` prints `ANCHORS anchors=<n> ok=<n> drifted=0 unreadable=0` and exits 0; a should-fail fixture
whose anchor line is shifted by the Arch patch set prints `drifted=1` naming exactly that anchor id
and exits 1; an absent-host-source fixture prints `unreadable=1` and exits 1; the r40 util.c anchors
(EX1/EX2/EX3) are in the declared table and read `ok` at the tip. Kill: unmet if the tip run is not
`drifted=0`, if either fixture does not read exactly its named anchor, or if the instrument's bytes
differ from the manifest at scoring time.

**Contradiction stated, not smoothed (C-1).** `corpus/README.md:844` says the item is partial because
it "needs a host-build measurement outside the frozen legs" — but a host-build patch-offset probe was
already run twice: r42 for libalpm (108 pins, `out.json`) and r91 for limine
(`corpus/lessons/round-91.md:90`: "host-build patch-offset probe PASS for uri.c/chainload.c/config.c
(Arch PKGBUILD sha matches .BUILDINFO; bootstrap touches none of them)"). The frontier's *reason* is
stale; its *substance* (no committed, registry-rowed re-runnable instrument) holds. A later round
should correct the reason when it closes the row, not inherit it.

## 7. The r98 carry-over list against the current tree — three lines

**CO-1 — `before/instruments.sha256` verified: YES.** `sha256sum -c` over the 16-entry manifest →
16 × `OK`, rc 0 (§2, receipt `instruments-check.txt`, `carryover.txt` CO-1).

**CO-2 — is the `after/c2/coverage-tip.json` pointer still dangling (R99-D1): YES, still dangling,
and now only for r98.** Measured with `test -e` over both waves:

```
PRESENT .ufo/waves/round-97/after/c2/coverage-tip.json
ABSENT  .ufo/waves/round-98/after/c2/coverage-tip.json     (dir holds content-freeze.json, content-freeze.txt, coverage-freeze.json)
```

Live citations of the literal path outside this wave's `w1/` (5 lines, `grep -rn`): 
`.ufo/plans/round-99.md:117` (naming the defect, by design), `.ufo/waves/round-98/after/report-draft.md:110`,
`SCORECARD.md:7984`, `corpus/lessons/round-97-verifier-spotcheck.md:105` (the r97 receipt, which *does*
exist), `corpus/lessons/round-98-verifier-spotcheck.md:113` (the defect's own record). So the pointer
dangles only in the r98 location; the r97 location resolves. (Seat `ExecDrift` reached the same two
citations independently this wave, `w1/ExecDrift.md:124-137`; this line is my own measurement, not a
citation of that receipt.)

**CO-3 — does `.ufo/waves/round-99/before/` already hold the tip receipt: YES.**
`r99-d1-coverage-tip-f107da3a.txt` → `{"status":"PASS","counts":{"findings":0,"missing":0,"registered":160,"rows_total":160,"tools_total":160},"revision":"f107da3a…"}`;
`c2-content-tip-f107da3a.json` → `status PASS, bindings 7, rows 160, findings []`, schema
`tsukuroi-registry-content-r99-v1`; plus `r99-d1-coverage-r98settle-270ca298.txt` (the r98 settle
revision, also `PASS 160/160`). The R99-D1 artifact drop the r98 spot-check routed is done; what
remains is the append-only correction of the stale *pointer text*, which the r99 plan explicitly
routes to the report and lesson rather than to an edit of the r98 lesson.

## 8. The bounded move (connector; one, not a campaign)

**Evidence.** The plan's own named limit (`.ufo/plans/round-99.md`, BYTE 8487):

> - The X/Y **echo** leg has no spelling-targeted committed bend: N09/N11 falsify `visibility_era`
>   only. The echo legs are exercised by the blanket `lie-limine-version` wrapper (which fails X, Y,
>   Z and LZ) and by the r98-carried fixed-echo attack, not by a one-clause bend of their own.

Measured field-assertion map (`awk` over the frozen bytes, `connector-move.txt` §M.2): r98 sets
`check_echo` on `EXPLICIT-VERSION-ECHO`, `9DIGIT-Z` and `LEADING-ZERO-NORMALIZE` only; r99 adds
`check_echo`/`check_era` to `9DIGIT` and `9DIGIT-Y`. The Y spellings are owned by exactly one family
(`Y_DIGIT9` defined at `tools/limine-pin-battery-r99.py:1750`, consumed once at `:1819`). Therefore a
lie in the *echo* keyed to the Y spellings is: r98-blind (`met 105/105`) and r99-single-family
(`unmet 104/105`, `[REFUSAL-VERSIONS-9DIGIT-Y]`).

**Affected axes.** depth (C1's own axis) — it is the missing witness for the `check_echo` half of the
new assertion; freshness untouched; no axis harmed (the gate's bytes, the r98 battery's bytes and the
registry checker are not touched).

**Proposed move.** A fourth bend, `N12-y-echo.py`, one clause at the same dict literal the committed
bends use:

```
-            "limine_version": limine_version,
+            "limine_version": ("0.0.0" if limine_version.split(".")[1] == "999999999" else limine_version),  # N12 (echo lies for Y-cap spellings only)
```

`"0.0.0"` is chosen so the falsified echo cannot be read as either Y member or as an era hint; the
era label, the source and every pin stay correct, so only `meta_ok`'s echo conjunct can fire.

**Not a twin under QUALITY 136.** The r99 plan dropped a Z-only echo bend because the *r98 control
already caught it* (r98 sets `check_echo` on Z). This clause has the opposite property: r98 is blind
to it, and it exercises the other field of the family N09 exercises. `R98-FIELD-NOT-ASSERTED` is a
per-field mistake, so a per-family witness (N09) does not cover `check_echo`.

**Risks.** (1) A critic will call it a twin of N09 — same condition, same family; the answer is the
previous paragraph, and the fallback is the X-cap variant of the same clause (`failed_families` becomes
`[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]`, r98 control `104/105`, a delta instead of
blindness). (2) Host load: six extra battery runs must not be dispatched beside an existing bend seat
(this wave's N09/N11 legs already run 12). (3) It keys on the *spelling*; the round that lands it must
state that the echo is asserted on the spelling, not the number, or a future normalizing gate will fail
it for the wrong reason.

**Verification (for whoever lands it, not this seat).** `--runs 3` both layouts, r99 read
`unmet 104/105` with exactly `[REFUSAL-VERSIONS-9DIGIT-Y]` and 0 error rows; r98 do-nothing read
`met 105/105`; the instrument manifest still verifies 16/16 before either number is cited.

**Second-order observation for a later round (not a move this round).** The r98 mistake
`R98-MUTANT-DIRECTION-READ` produced a proposed criterion with **no source row**, while three siblings
hold sources for it: `kaidoku`'s S304 (Papadakis et al., mutation-testing survey, tier A),
`kotoba`'s S120 (Petrović et al., Practical Mutation Testing at Scale, tier A) and `kagi`'s r62
S128/S129 captures (pitest / Stryker kill-and-survive sentences). The lane's `corpus/SOURCES.md`
census this round went 394 → 395 rows (`before/census-before-after.txt`) with no row for the
criterion. Citing one of those sources would ground the criterion without touching depth or
freshness; it is recorded here as an assimilation candidate, not executed.

## 9. Contradictions, stated

- **C-1** — `corpus/README.md:844` gives a stale reason for an open frontier row (§6).
- **C-2** — The class C1 closes is **already on record in a sibling lane from 2026-10-14**:
  `tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md:144-145` names survivor class
  "**(a) reported-but-unasserted surface**" with `tsukuroi B9` among its instances, and
  `mutation-case-tsukuroi-census.md` measured it on this lane's census. The r98 lesson presents
  `R98-FIELD-NOT-ASSERTED` as a fresh class; it is a re-derivation on a different instrument. Both
  readings are true; the honest record names the prior and its owner (ADJ-07), and does not claim
  the class as new.
- **C-3** — Both sibling measurements of this lane are stale by design and must not be quoted as
  current: tameshi's census pin `165307fe` is **728 commits** behind HEAD and its substrate sha
  `084951be…` (976 lines) is not today's `tools/tsukuroi-census.sh` (4815 lines, sha256
  `89026b9a8012a3da20501a5b0eaee3b6dec8b335ab72278214f325685399b1d6`); kotoba's sibling-overlap
  census pins this lane at `8bd001f5`, **477 commits** behind. Both lanes' own disciplines say a rate
  or a class is not implied to hold at a later revision — so the *class* transfers, the *number* does
  not.
- **C-4** — `mori`'s and `tameshi`'s entries both touch this lane's ground (ADJ-04 host pressure,
  ADJ-07 method) but neither is a duplicate claim of this round's two surfaces.

## 10. PASS/FAIL per expected line

| expected | measured | verdict |
|---|---|---|
| `sha256sum -c before/instruments.sha256` verifies | 16/16 OK, rc 0 | **PASS** |
| surface A swept over all 20 sibling corpora, every hit named | 48 line hits / 39 files / 13 lanes, table §3 | **PASS** |
| surface B swept over all 20 sibling corpora, every hit named | 79 line hits / 68 files / 15 lanes, table §4 | **PASS** |
| kumitate, kotoba, kake, kagi, kama each checked by name | all five scanned twice (surface A, surface B); kotoba and kagi zero-hit re-derived (§3.1) | **PASS** |
| each hit decided (a)/(b)/(c) with handoff row or `new handoff needed` | table §3/§4; ADJ-07/OUT-010 named for tameshi's method ground **and** for the shared fleet census (§3.2); no hit needed a new handoff row | **PASS** |
| exactly one considerthese pick, quote + target + implemented check | §6: "Downstream patch-offset check", BYTE 4027, `pacman-exec-environment-r40.md` opened, not implemented as a gate | **PASS** |
| three r98 carry-over lines | §7 CO-1/CO-2/CO-3 | **PASS** |
| no sibling file written; no campaign tool run; no instrument modified | measured after all work: `git status --porcelain -- .ufo/waves/round-99/w1/ConnectorOverlap` → only `?? .ufo/waves/round-99/w1/ConnectorOverlap/` (this seat's own dir; the tree's other `M`/`??` entries are other seats' and the L1's writes, untouched by this seat); post-work `sha256sum -c` rc 0 again; no battery, checker, bend or `make-r*-bends.py` executed | **PASS** |
| scratch removed | `/fast/scratch/hyaku/tsukuroi-r99/ConnectorOverlap` deleted | **PASS** |

## 11. Verdict

{"seat":"ConnectorOverlap","verdict":"met","notes":"Sibling sweep over all 20 corpora: surface A (registry drift / cell binding) 48 hits in 39 files across 13 lanes, surface B (battery metadata assertion / selftest lie kind) 79 hits in 68 files across 15 lanes. Every tsukuroi-specific token (check_echo, check_era, visibility_era, limine_version, LIE_KINDS, REFUSAL-VERSIONS, RC-BEND-SPAN, RC-CELL-MISSING, RC-CELL-AMBIGUOUS, check-registry-content) is at zero sibling files, so the gate, the 105-family battery and the registry binding are this lane's own ground. The one true sibling-domain overlap is tameshi: ADJ-07/OUT-010 owns the mutation/verification method, its mutation-case-tsukuroi-census.md and fleet-kill-rate-ledger.md:47 already measured this lane's census 6/10 and named the 'reported-but-unasserted surface' class (tsukuroi B9) on 2026-10-14 that C1 re-derives, and its PROVINCE.md:194-197 declares the shared fleet scripts/sources-census.sh Core as a read-only primary surface (so a census defect routes there). kotoba and kagi are zero-hit on both surfaces (kagi's nearest ground is claim-instrument-falsifiability.md under other vocabulary; kotoba's S120 is a tier-A mutation-testing source the lane holds no row for). considerthese pick: 'Downstream patch-offset check' (BYTE 4027 of a 4551-byte batch), target corpus/knowledge/pacman-exec-environment-r40.md opened (it carries the +5 offset at line 110); QUALITY 103 rule + r42 one-off probe exist, but no tools/ instrument and no SKILL gate row, and frontier corpus/README.md:844 is still open with a stale reason (host-build probes ran at r42 for libalpm and r91 for limine). Carry-over: instruments 16/16 OK rc0; after/c2/coverage-tip.json still ABSENT for r98 (PRESENT for r97) and still cited by round-98/after/report-draft.md:110, SCORECARD.md:7984 and the two spot-checks; round-99 before/ already holds the tip receipts (coverage PASS 160/160 findings 0 at f107da3a and at the r98 settle 270ca298; content PASS bindings 7 rows 160). Bounded move: N12-y-echo, one clause at the same dict literal as N09, predicted r99 unmet 104/105 exactly [REFUSAL-VERSIONS-9DIGIT-Y] with 0 error rows vs r98 do-nothing met 105/105 (blind); twin-free under QUALITY 136 because the r98 control cannot see it, and it witnesses check_echo, the field N09 leaves unwitnessed. No sibling file written, no campaign tool run, no install/upgrade, scratch deleted."}
