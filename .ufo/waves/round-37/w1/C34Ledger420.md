# C34Ledger420 — C3 falsification item 4/8: self-assessment mismatch repair (forward-stability + evidence-retention attack)

Round 37 attempt 1, wave 1, seat C34Ledger420. Axis: **calibration / C3:self-assessment-mismatch**.
Milestone: C3 baseline/mismatch attack.

**Scope note (item distinctness).** Sibling seats in this wave attack the *same* C3 claim and overlap
on the lineage table (C31/C33/C35/C37 walk the base→tip revision ladder; C32/C36 attack K17's
case-count token and the K16 shared-table prerequisite). This seat does **not** re-report that
ladder. It attacks the claim on two axes no sibling report states:

1. **Forward-stability.** The claim's predicate is `mismatches == 0 && checked == 27 && exit == 0`
   "at the measured round-37 branch-tip revision". The tip is not a fixed point: the round's own
   next content commit re-breaks it. Demonstrated with four single-file fixtures (F6–F9).
2. **Evidence retention.** The repair reached `mismatches == 0` by *deleting* four still-present
   evidence pointers from the capability rows. The checker cannot see this deletion, so the claim's
   counter certifies a *narrower* self-assessment than the one it supersedes.

Tooling rule read first: `/home/vgpnk/.omp/agent/RULES.md` lines 1–14. **No tool installed or
updated** (nothing needed; `python3`/`git` preinstalled). No pacman, no host changes, no delegation,
no background jobs, no campaign tools. Every lane read was through `git show`/`git ls-tree` at
pinned revisions; the only lane bytes written are this report and its seat directory.

Access date for every source cited below: **2026-10-25**.

---

## 1. Verdict

**The C3 claim's frozen predicate holds exactly at the tip and nowhere else, and the repair that
produced it is a snapshot, not a fix.** Three findings, all measured:

| # | Finding | Evidence |
|---|---|---|
| **A** | The claim's *after* state is **not stable under the round's own next content commit**. Adding one `corpus/knowledge/*.md` note → K07 mismatch; one `corpus/lessons/*.md` file → K10; one line to `SKILL.md` → K08; one line to `corpus/README.md` → K11. Each is a single-file commit, the exact shape of the round's planned change commit. **The prediction fired inside this round**: the lane's live tip `29b22df` drifted on all five counts and had to append a *third* round-37 axes table (`SCORECARD.md:2047`) to stay green. | F6–F9, §3.1 |
| **B** | The repair reached zero mismatches by **deleting four evidence pointers that are still present at the tip**. The tip's capability rows name 6 paths; the superseded round-35 rows named 10. All four dropped paths exist at `0e5f70f`. The checker's K16–K19 only assert that *named* paths exist — it cannot detect that a pointer was *removed*. | path-set diff (§4), F5 |
| **C** | The append-only correction idiom that produced the repair is **fragile in a way the claim does not disclose**: appending a partial one-row capabilities table (at either `##` or `###` heading level) drives the unchanged checker to **exit 2 CANNOT_EVALUATE** (`missing capability row: sources-registry`), because `pick_table` audits only the **last** table under the last `## Capabilities` heading. This is not hypothetical — it is what commit `5124bf3` did, and it is the lane's own idiom. | F10–F12, lineage table (§2) |

**Concrete fixed check + correction proposal (as assigned): K11**, with the full five-cell
correction in §5, validated to `checked 27, mismatches 0, status PASS, exit 0` by the **unchanged**
checker on a fresh fixture (F1). The minimal one-cell correction alone is **not** sufficient —
the claim's own description of the repair ("append-only correction of the five current
self-assessment count cells") is correct that five cells need correcting, but the correction must
also satisfy the parser's *literal phrase* grammar, which is a second, unstated requirement.

---

## 2. Observed lineage (reproduced, read-only, one run per revision)

`python3 tools/check-self-assessment.py --revision <REV> --repo <lane>`, checker bytes identical
throughout (sha256 `1e1ab6113d665684e15d147c0f3dae519cf2d313877e1603b841ad4db85d4257` at base and
tip; `git diff --stat 564db0b614 0e5f70f -- tools/` is empty — no tool byte changed).

| Revision | exit | status | mismatches | checked | failing checks |
|---|---|---|---|---|---|
| `564db0b614` (declaration base) | 1 | FAIL | 5 | 27 | K07 K08 K09 K10 K11 |
| `083cd0c` (declaration) | 1 | FAIL | 5 | 27 | K07 K08 K09 K10 K11 |
| `b8ededd` (pre-freeze C3 correction) | 1 | FAIL | 5 | 27 | K07 K08 K09 K10 K11 |
| `d06cedb` (first repair) | 1 | FAIL | 2 | 27 | K17 K18 |
| `ee36f9e` | 1 | FAIL | 1 | 27 | K17 |
| `5124bf3` | **2** | **CANNOT_EVALUATE** | — | 0 | `missing capability row: sources-registry` |
| `0e5f70f` (repair tip) | 0 | PASS | 0 | 27 | — |
| `29b22df` (live tip, landed during this seat) | 0 | PASS | 0 | 27 | — (after a *third* round-37 axes table; see §3.1) |

Machine-readable copies: `fixtures/out/lane-<rev>.json`, `fixtures/out/lane-live-tip-29b22df.json`.

The claim's *before* value reproduces exactly (5 mismatches, K07–K11, exit 1). The claim's *after*
value reproduces exactly at the tip only. Raw receipt for the base: the lane's own
`.ufo/waves/round-37/before/c3-before.json` (`checked 27, mismatches 5, FAIL`) and
`c3-before-exit.txt` (`exit=1`) agree with my independent rerun.

---

## 3. Finding A — the repair is not stable under the round's own next commit

The claim (SCORECARD.md, commit `b8ededd`, "Round 37 — pre-freeze C3 correction") states the after
state as *"the same command at the measured round-37 branch-tip revision reports `checked: 27`,
`mismatches: 0`, `status: PASS`, exit 0"*. The predicate names a **branch tip**, but the repaired
axes table hard-codes *tree counts* (56 notes, 3110 SKILL.md lines, 839 table lines, 49 lesson
files, 269 README lines). Any later commit that touches one of those five trees moves the observed
value and re-breaks the matching check — the self-assessment is only correct **at the instant it
was measured**.

Four single-file fixtures on the tip tree (each: fresh `mktemp` repo, `git -C <root> init`,
top-level verified equal to the fixture root before commit, one added file, one commit):

| Fixture | Mutation | exit | status | mismatches | failing check (verbatim reason) |
|---|---|---|---|---|---|
| F6 | + `corpus/knowledge/round-37-staleness-probe.md` | 1 | FAIL | 1 | K07 | `depth row states 56 notes; corpus/knowledge holds 57 .md files` |
| F7 | + `corpus/lessons/round-37-staleness-probe.md` | 1 | FAIL | 1 | K10 | `depth row states 49 lesson files; corpus/lessons holds 50 files` |
| F8 | + 1 line in `SKILL.md` | 1 | FAIL | 1 | K08 | `depth row states 3110 SKILL.md lines; SKILL.md holds 3112 newline characters` |
| F9 | + 1 line in `corpus/README.md` | 1 | FAIL | 1 | K11 | `coverage row states 269 corpus/README.md lines; the file holds 271 newline characters` |

Receipts: `fixtures/out/F6-…json`, `F7-…json`, `F8-…json`, `F9-…json`.

**This is not hypothetical for round 37.** The round-37 declaration's own order (SCORECARD.md at
`083cd0c`, "Order:" paragraph) schedules exactly these mutations:

> "… the change commit (probe V8, C2 corrections + checker, C3 ledger + checker, **SOURCES rows,
> lesson skeleton, registry rows**); after battery receipts; wave 2 …; the measured outcome,
> **lesson, SOURCES/README/SKILL rows** and report."

A **lesson skeleton** is a new file under `corpus/lessons/` → breaks **K10** (F7). **SKILL rows**
are appended lines in `SKILL.md` → break **K08** (F8). **README rows** are appended lines in
`corpus/README.md` → break **K11** (F9). A new **knowledge note** (the round-37 C2 note
`corpus/knowledge/journalctl-v262-field-filter-r36.md` is already present at the tip; the
assimilation package admits `errno-contract-variance-r37.md`, absent at the tip) → breaks **K07**
(F6). The lane's own `corpus/lessons/` history shows the per-round pattern
(`round-34.md`, `round-35.md`, `round-36.md` — each round lands its own lesson file), and
`corpus/README.md` and `SKILL.md` carry per-round rows through `round-36`.

**Prediction (falsifiable):** at the round-37 change commit, the unchanged checker reports
**≥ 1 mismatch** against the round-37 axes table, unless a *second* axes table is appended after
the change commit re-deriving the five counts. The claim as written has no mechanism to deliver
that; it names the branch tip, which moves.

### 3.1 The prediction fired inside this very round (live confirmation, not extrapolation)

While this seat was running, the lane landed the round's own change commits and the prediction
materialised **exactly as F6–F9 predict**. Measured on the live lane tip `29b22df`
("round-37: freeze V8 livefive counter and current assessment", 2026-10-25 16:34:37 −03:00):

| Count | repaired tip `0e5f70f` | live tip `29b22df` | drift |
|---|---|---|---|
| `corpus/knowledge/*.md` notes | 56 | **58** | +2 (F6: one note → +1 each) |
| `SKILL.md` newline characters | 3110 | **3112** | +2 (F8: one appended line → +2) |
| `SKILL.md` pipe-prefixed lines | 839 | **841** | +2 |
| `corpus/lessons/` files | 49 | **50** | +1 (F7: one lesson file → +1) |
| `corpus/README.md` newline characters | 269 | **282** | +13 (F9: README rows) |

The lane's own commit `29b22df` therefore had to append a **third** round-37 axes table —
`## Axes — current self-assessment (round 37 final measured surface)` at `SCORECARD.md:2047` —
carrying the re-derived counts (`58 notes`, `SKILL.md` 3112 `wc -l` / 841 table lines,
`` `corpus/lessons/` 50 files ``, `` `corpus/README.md` 282 `wc -l` ``). The round-37 pile-up at
the live tip is now **three** `## Axes … round 37` tables (lines 1976, 2000, 2047) and **three**
`## Capabilities … round 37` tables — six round-37 tables, of which only the last of each kind is
operative (`find_section` + `pick_table`).

So the claim's predicate was satisfied at `0e5f70f` only because the lane re-appended a table at
the moment the counts moved. Every content commit in the round forces another append; the
self-assessment is a **moving snapshot**, and the number of superseded tables is the direct cost
of that design. The claim's predicate names "the measured round-37 branch-tip revision", which
moved from `0e5f70f` to `29b22df` *within the same round*, with the predicate holding at both only
because a new table was appended each time.

The checker's verdict at the live tip is still `checked 27, mismatches 0, PASS, exit 0` — the
repair is currently green — but it is green *again*, not *durably*.

**This is a calibration defect, not a counter defect.** The checker's job is to detect a stale
self-assessment; it does. The defect is that the *repair* — five hard-coded counts — cannot be
durable, because the lane keeps appending to the trees it counts. A durable repair would state
the counts as of a **named revision** and pin the predicate to that revision, or state the counts
in a form the checker evaluates against the tree *at the same revision it names*. The claim's
predicate pins neither.

---

## 4. Finding B — the repair reached zero mismatches by deleting still-present evidence

The claim states: *"The checker bytes and fixed 27-check population are unchanged; only the
self-assessment values may change."* The K16–K19 checks assert that every path a capability row
**names** exists at the revision (`tools/check-self-assessment.py` lines 671–727). They cannot
detect a path that was **removed** from a row.

Named-path-set diff, base operative capabilities table (`SCORECARD.md:1582-1587`) vs tip operative
capabilities table (`SCORECARD.md:2036-2041`), computed with the checker's own grammar
(backtick spans → `PATH_CHARSET` → suffix filter):

| capability | base paths | tip paths | dropped | still present at tip tree? |
|---|---|---|---|---|
| sources-registry | 2 | 1 | `.ufo/evidence/round-1-kaika/after.md` | **yes** (1/1) |
| host-census-gate | 3 | 2 | `.ufo/evidence/round-1-kaika/after.md` | **yes** (1/1) |
| root-metadata-observer | 3 | 1 | `.ufo/waves/round-12/resumed/selftest-after.json`, `.ufo/waves/round-12/resumed/mode-policy-mutant.json` | **yes** (2/2) |
| boot-chain-audit | 2 | 2 | — | — |
| **total** | **10** | **6** | **4** | **4/4** |

Verified present at `0e5f70f` independently via `git ls-tree -r --name-only 0e5f70f -- <path>`
(all four resolve; the bare-basename forms `after.md` / `selftest-after.json` /
`mode-policy-mutant.json` do **not** exist at the repo root, which is exactly why the first
repair attempt `d06cedb` failed K17/K18 — the checker's path grammar resolves a token *from the
token itself*, with no resolution against a preceding directory, per its own docstring lines
63–67 and `is_path_like`/`resolve_paths`).

**The four deleted pointers were not needed to be deleted.** Fixture **F5** = tip tree + an
appended `## Capabilities — current (round 37)` table that restores all four pointers, fully
qualified (`.../round-1-kaika/after.md`, `.../resumed/selftest-after.json`,
`.../resumed/mode-policy-mutant.json`):

> **F5: exit=0, status=PASS, mismatches=0, checked=27** — with K16 naming 2 paths, K17 naming 3
> and stating 105 cases, K18 naming 3, K19 naming 2 (the base's full evidence set restored).

So the tip could have carried the *base's* full evidence set and still reported zero mismatches.
Instead it carries a narrower set, and the claim's counter cannot tell the difference: **the same
`mismatches == 0` reading certifies both**. A checker that validated *"the capability rows name
every pointer the superseded rows named"* (or that a superseded table's pointer set is a subset of
its successor's) would have caught the deletion; K16–K19 as implemented cannot, by construction.

Fixture **F2** = base tree + the §5 axes-table correction + the same restored capability rows →
**exit=0, PASS, mismatches=0, checked=27** with the base's full 10-pointer evidence set. The
repair and the evidence retention are jointly achievable; the lane landed only the first.

---

## 5. Correction proposal (do not implement here)

### 5.1 The assigned fixed check: K11 — coverage row `corpus/README.md` line count

- **Check:** K11 — "coverage row corpus/README.md line count equals the line count of
  corpus/README.md" (`tools/check-self-assessment.py` lines 613–622).
- **Stale self-assessment value at the declaration base `564db0b614`:** the operative round-35
  coverage row (`SCORECARD.md:1571`) states **256**; the tree holds **269** newline characters.
  Checker verdict, verbatim: `coverage row states 256 corpus/README.md lines; the file holds 269
  newline characters` — **mismatch**, exit 1.
- **Correction (one cell):** in the operative coverage row, state `` `corpus/README.md` 269 `wc -l` ``.
  The parser takes the number after the path token (`stated_in` → `number_after(tail,
  r"(\d+)\s+`?wc -l`?")`, lines 613–619); the phrase `wc -l` must be adjacent to the count.
- **Why one cell is not enough, and what the full correction is.** The five base mismatches are
  five cells in **two** rows, and each cell must carry the parser's literal phrase:

  | Check | stale value at base | observed | required phrase in the corrected cell |
  |---|---|---|---|
  | K07 | 55 notes | 56 | `56 notes` |
  | K08 | `SKILL.md` 3009 `wc -l` | 3110 | `` `SKILL.md` 3110 `wc -l` `` |
  | K09 | 784 table lines | 839 | `839 table lines` |
  | K10 | `corpus/lessons/` (46 files) | 49 | `` `corpus/lessons/` 49 files `` |
  | K11 | `corpus/README.md` 256 `wc -l` | 269 | `` `corpus/README.md` 269 `wc -l` `` |

- **Correction proposal (append-only, one section, no capabilities table touched):** append one
  new `## Axes — current self-assessment (round 37)` section to `SCORECARD.md`, carrying the six
  rows with the five corrected cells. The exact text used in fixture **F1** is in
  `fixtures/build-fixtures.sh` (`PROPOSED_TABLE`). It deliberately keeps the phrase forms the
  unchanged checker parses (`56 notes`, `` `SKILL.md` 3110 `wc -l` ``, `839 table lines`,
  `` `corpus/lessons/` 49 files ``, `` `corpus/README.md` 269 `wc -l` ``, `PASS (105 cases, …)`,
  `` `--identity` not landed ``, `formal overlap table present`).
- **Prediction, then measurement:** with the correction applied to the base tree and the checker
  unchanged, `checked == 27`, `mismatches == 0`, `status == PASS`, `exit == 0`.
- **Measured:** fixture **F1** (base tree + the proposed axes table, unchanged checker):
  **exit=0, status=PASS, mismatches=0, checked=27**, `declaring_round=37`, `axes_heading=## Axes —
  current self-assessment (round 37)`. Receipt: `fixtures/out/F1-base-plus-proposed-axes-table.json`.
  K01–K06 also match, because the declaring round moves 35 → 37 and the reference window then
  excludes the round-37 sections and admits the round-35/36 measured-outcome records
  (`reference_lines` 350 at the base → 422 in F1 and at the tip; last recorded transition per axis
  at `SCORECARD.md:1560`: depth 8→8, coverage 9→9, operability 9→9, freshness 9→9,
  calibration 9→9, adjacency 8→8 — identical to the base's own readings, which also resolve to
  `SCORECARD.md:1480`/`:1560` with the same after-values). The base's `reference_lines: 350` is the
  lane's own recorded value (`.ufo/waves/round-37/before/c3-before.json`); F1's 422 and the tip's
  422 are the checker's own reported fields, cross-checked by re-implementing `reference_lines`
  against the HEAD blob.

### 5.2 The negative control that makes the correction non-trivial

Fixture **F3** = base tree + an axes table whose coverage row phrases the README count the way the
**first** round-37 attempt did (`269 newline characters (`wc -l corpus/README.md`)`) — the same
numbers, a different phrase shape:

> **F3: exit=1, FAIL, mismatches=1** — K11 `stated=None`, `observed=269`:
> `coverage row states None corpus/README.md lines; the file holds 269 newline characters`.

Same five corrected numbers, and the check still fails, because the count token is not adjacent to
the `wc -l` phrase the parser looks for.

The lane hit this wall in production, and the repair is visible in the file. Commit `d06cedb`
shipped **two** round-37 axes tables in one commit: the first at `SCORECARD.md:1976` with the
coverage row phrased `269 newline characters (`wc -l corpus/README.md`)` (line 1983), and the
second at `SCORECARD.md:2000` with the coverage row phrased `` `corpus/README.md` 269 `wc -l` ``
(line 2007) and the prose *"the self-assessment parser requires the literal count phrases shown
here"* (line 2002). Because `find_section`/`pick_table` audit only the **last** `## Axes - ` table,
the mis-phrased first table was dead on arrival — at `d06cedb` K11 **matched**, and the only
failures were K17/K18 (lineage table in §2). The mis-phrasing was therefore never itself a
failure; it is dead text.

That makes F3 a statement of the *rule*, not of a past failure: had the mis-phrased table been the
operative one, the checker would have read `stated=None` and failed K11. The correction proposal
must therefore specify phrase shapes, not just numbers — a requirement the claim text does not
state, and one the lane satisfied by appending a second table whose prose explains it.

### 5.3 The capability-row correction that avoids the exit-2 trap

If the capability rows are touched at all, the correction must append **all four rows** in one
`## Capabilities` table. Fixture **F10** (tip + an `###`-level one-row capabilities table) and
**F11** (tip + a `##`-level one-row capabilities table) both yield:

> **exit=2, status=CANNOT_EVALUATE, checked=0, `missing capability row: sources-registry`**

while fixture **F12** (tip + an `###`-level **four-row** capabilities table) yields
**exit=0, PASS, mismatches=0, checked=27**. The heading level is irrelevant; the **last table under
the last `## Capabilities` heading** is the one audited (`find_section` + `pick_table`,
lines 476–489). This is precisely the defect commit `5124bf3` introduced and `0e5f70f` had to
work around by appending a *complete* table. Any future correction that appends a partial
capability table will re-break the checker the same way.

### 5.4 The durable form of the correction (recommended, beyond the assigned scope)

To make the claim's predicate durable rather than a snapshot, pin the counts to a named revision
and pin the predicate to that revision — e.g. state the five counts as measured at `<sha>`, and
declare the predicate as `mismatches == 0 && checked == 27 && exit == 0` **at `<sha>`**, not "at
the branch tip". As measured in §3, "at the branch tip" is falsified by the round's own next
content commit.

---

## 6. Method, gates, and limits

**Read-only discipline.** Every lane read went through `git show`/`git ls-tree`/`git archive` at
pinned revisions; the working tree was never the measurement source except for the two
`git status --porcelain` observations quoted in §7. No `git add`/`commit`/`push`/`fetch` and no
mutating `jj` ran against the lane, the fleet repo, or any sibling lane. No lane Git or jj state,
index, or tracked file was mutated.

**Fixture discipline.** Every fixture is a fresh `mktemp -d` root; the lane tree is exported with
`git -C <lane> archive` (read-only); `git -C <root> init -q`; the fixture top-level is compared
against the fixture root and the script aborts (exit 3) on mismatch **before** any commit; all
commits happen inside the fixture repo. Scripts: `fixtures/build-fixtures.sh`,
`fixtures/run-exit-codes-and-staleness.sh`, `fixtures/run-heading-trap.sh`,
`fixtures/run-evidence-drop.sh`. All fixture roots live under `/tmp` and are disposable; the
durable artefacts are the JSON receipts and the scripts under this seat directory.

**What I did not do.** I did not implement the correction in the lane; I did not mutate
`SCORECARD.md`, `LOG.md`, `SKILL.md`, or any tracked file; I did not run the census against the
live host (the checker runs the census selftest itself from `git archive` in a temp dir); I did
not run `pacman` or any host mutation; I did not dispatch subagents.

**Limits of the evidence.** (a) The staleness prediction in §3 is a prediction about a future
commit; I demonstrated each trigger in isolation on the current tip tree, not the future commit
itself. (b) The phrase-grammar requirements in §5 are read from the checker source and confirmed
by fixture outcome (F3), not by a separate spec document — the checker's docstring does not
enumerate them. (c) `reference_lines` re-implementation for the K01–K06 window was checked against
the checker's own reported `reference_lines` (422 at HEAD) and its per-check `observed_line`
(1560 for all six axes), which agrees.

---

## 7. Lane working-tree state observed (not caused by this seat)

`git status --porcelain` in the lane at the time of this report shows ` M LOG.md`, ` M SCORECARD.md`,
` M SKILL.md` and untracked round-37 wave artefacts (`tools/probe-child-env-allowlist-r37.py`,
`.ufo/waves/round-37/after-c3-*.json`, `.ufo/waves/round-37/before/*`, `.ufo/waves/round-37/w1/`).
These are the concurrent round's own in-flight bytes; **this seat wrote none of them**. The only
bytes this seat wrote are under `.ufo/waves/round-37/w1/C34Ledger420/` and this report file.

## 8. Sources opened (access date 2026-10-25)

- `tools/check-self-assessment.py` — read: docstring lines 1–45 (27 fixed checks K01–K27, exit-code
  map), path grammar lines 63–67 / `path_candidates` / `is_path_like` / `resolve_paths`,
  `find_section` + `pick_table` (last-table selection), `reference_lines` + `heading_sections`
  (ordinal reference window), `stated_case_count` (accepted count phrasings), `evaluate()` lines
  434–810 (K01–K27 emission).
- `SCORECARD.md` at `564db0b614`, `083cd0c`, `b8ededd`, `d06cedb`, `ee36f9e`, `5124bf3`,
  `0e5f70f`, and the live tip `29b22df` — located quotes: C3 claim text (base `b8ededd`,
  "Round 37 — pre-freeze C3 correction", SCORECARD.md:1950–1974); round-37 declaration order
  (base `083cd0c`, SCORECARD.md:1946–1948); operative axes table (tip `0e5f70f` :2000–2011);
  operative capabilities table (tip `0e5f70f` :2032–2041); superseded round-35 axes/capabilities
  tables (base :1564–1587); live-tip third round-37 axes table (`29b22df` :2047) and the count
  drift it re-derives (§3.1).
- `.ufo/waves/round-37/before/c3-before.json` and `c3-before-exit.txt` — the lane's own before
  receipt (checked 27, mismatches 5, FAIL, exit=1).
- `tools/tsukuroi-census.sh` and `corpus/README.md`, `SKILL.md`, `corpus/lessons/`,
  `corpus/knowledge/` — tree contents at `0e5f70f` via `git ls-tree` (per-round artifact pattern
  used in §3).
- `git log --oneline` / `git diff --stat` in the lane (lineage and the empty `tools/` diff).
- `/home/vgpnk/.omp/agent/RULES.md` lines 1–14 (tooling channels and the update-safety gate).
- Sibling seat reports `C31Ledger117.md`, `C32Ledger218.md`, `C33Ledger319.md`, `C35Ledger521.md`,
  `C36Ledger622.md`, `C37Ledger723.md` in `.ufo/waves/round-37/w1/` — read for item distinctness.

**Tooling record:** none installed, none updated. No pacman transaction (host-wide pacman pause
observed and honoured). Reason: python3 and git were already present and sufficient; the generic
tooling directive's channel order was not exercised because no install or upgrade was needed.

---

## Final answer

The C3 repair claim is **true but non-durable and evidence-losing**: the unchanged checker reports `checked 27 / mismatches 0 / PASS / exit 0` at `0e5f70f`, but only there — one added knowledge note, lesson file, `SKILL.md` line or `corpus/README.md` line re-breaks K07/K10/K08/K11 (F6–F9), and the prediction fired in-round: the live tip `29b22df` drifted on all five counts (56→58, 3110→3112, 839→841, 49→50, 269→282) and needed a *third* round-37 axes table (`SCORECARD.md:2047`) to stay green.
The repair also reached zero by deleting four still-present evidence pointers (10 named paths → 6); K16–K19 cannot detect removal, and F5 proves the tip could carry the full base evidence set and still report zero.
Assigned check **K11** (base coverage row states 256 `corpus/README.md` lines, tree holds 269) plus the four sibling count cells, in one appended axes table using the parser's literal phrase forms, is verified on a fresh fixture (F1) at `checked 27 / mismatches 0 / PASS / exit 0` with checker bytes unchanged.
The phrase requirement is real (F3: same numbers, wrong phrasing → K11 `stated=None`), and any partial capabilities table re-breaks the checker to exit 2 CANNOT_EVALUATE (F10/F11) — the defect `5124bf3` already introduced.
Recommendation: pin the five counts and the predicate to a named revision instead of "the branch tip", and never append a partial capabilities table.
