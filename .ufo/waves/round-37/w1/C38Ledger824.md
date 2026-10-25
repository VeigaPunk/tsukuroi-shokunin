# C38Ledger824 — C3 falsification item 8/8: self-assessment mismatch repair claim

**Seat:** C38Ledger824 (scout, round 37 wave 1, attempt 1)
**Lane:** tsukuroi, round 37, claim C3 (calibration)
**Declaration base:** `564db0b614b2914de5452f9ebd537a0653ae1de5`
**Measured tip at report time:** `d621b7126e088824fed354e19839a9c1bd4e74f0`
**Verifier:** none — this is an author's-own falsification seat; no non-author closure is claimed.
**Lane writes:** none. Every lane read was `git show` / `git ls-tree` / `git archive` / `git status` (read-only).
All fixtures ran in `mktemp -d` repos with the top-level verified against the fixture root before every commit.

---

## 1. Verdict

**The C3 claim as declared does not hold, and the repair as landed is a moving target.**

The declared before-value is **reproduced exactly**: at the declaration base the unchanged checker reports
`checked: 27, mismatches: 5, status: FAIL`, exit 1, with mismatches `K07 K08 K09 K10 K11` — byte-identical to the
lane's own receipt `.ufo/waves/round-37/before/c3-before.json`. The checker bytes are unchanged
(`sha256 1e1ab6113d665684e15d147c0f3dae519cf2d313877e1603b841ad4db85d4257`, identical at base and tip).

But the declared after-value — *"the same command at the measured round-37 branch-tip revision reports
`checked: 27`, `mismatches: 0`, `status: PASS`, exit 0"* — is **false at the measured tip**. Measured at the tip
`d621b71`:

```
python3 tools/check-self-assessment.py --revision d621b7126e088824fed354e19839a9c1bd4e74f0
exit 1   checked: 27   mismatches: 5   status: FAIL
  K07 mismatch | depth row states 56 notes; corpus/knowledge holds 58 .md files
  K08 mismatch | depth row states 3110 SKILL.md lines; SKILL.md holds 3111 newline characters
  K09 mismatch | depth row states 839 table lines; SKILL.md holds 840 pipe-prefixed lines
  K10 mismatch | depth row states 49 lesson files; corpus/lessons holds 50 files
  K11 mismatch | coverage row states 269 corpus/README.md lines; the file holds 282 newline characters
```

The five count cells are **revision-bound**: the repair restates them at one revision, and the round's own
subsequent commits (the change commit, the lesson file, the SOURCES/README/SKILL rows) move the counts they state.
The mismatch count therefore re-drifts upward as the round proceeds — it is not a repair that converges.

**Concrete fixed check whose currently stale self-assessment value produces a mismatch at the declaration base:**
**K10** — *the depth row's `corpus/lessons/` file count equals the file count under `corpus/lessons/`*. At the base
the depth row states `46` lesson files while `corpus/lessons/` holds `49` (`check-self-assessment.py:671-680`;
`git ls-tree -r --name-only 564db0b6 corpus/lessons/ | wc -l` → 49). K10 is also the check the lane has had to
repair in five consecutive rounds (rounds 28, 31, 32, 33, 36 per `SCORECARD.md:1086,1282,1386,1803`), which is
independent evidence that this is the load-bearing stale value.

**Correction proposal that makes the unchanged checker report zero mismatches** — see §3. It is verified
end-to-end at both the base and the tip by the unchanged checker.

---

## 2. What I ran (observed results only)

### 2.1 Base reproduction — the before-value is honest

| measurement | command | result |
|---|---|---|
| base, unchanged checker | `python3 tools/check-self-assessment.py --revision 564db0b6...` | exit 1, `checked 27`, `mismatches 5`, `FAIL`; `K07 K08 K09 K10 K11` |
| lane's own receipt | `.ufo/waves/round-37/before/c3-before.json` | exit 1, `checked 27`, `mismatches 5`, `FAIL`; same five ids |
| checker bytes, base vs tip | `sha256sum tools/check-self-assessment.py` | `1e1ab611…4257` at both |
| checker selftest | `python3 tools/check-self-assessment.py --selftest` | exit 0, `selftest PASS`, 19 cases, 0 failures |
| census selftest determinism | `bash tools/tsukuroi-census.sh --selftest` ×3 | 3/3 `PASS (105 cases, 105 passed, 0 failed)`, exit 0 |

My independent base measurement and the lane's receipt agree exactly. The five mismatches are real, the
before-value is correctly stated, and the checker itself is sound and stable. **The claim does not fail at the
base.**

### 2.2 The repair as landed never passed cleanly on the first attempt

The lane's own receipts (`.ufo/waves/round-37/after-c3-*.json`) record four successive commits. Replaying each
landed `SCORECARD.md` blob over the base tree in an isolated fixture and scoring it with the **unchanged** checker
(`fixture-scope.sh`) reproduces the lane's receipts exactly and attributes each intermediate failure:

| commit | exit | checked / mismatches | failing checks |
|---|---|---|---|
| base `564db0b6` | 1 | 27 / 5 | K07 K08 K09 K10 K11 |
| `d06cedb` (counts corrected) | 1 | 27 / **2** | K17 `after.md` absent; K18 `mode-policy-mutant.json, selftest-after.json` absent |
| `ee36f9e` (capability pointers) | 1 | 27 / **1** | K17 `states None cases` |
| `5124bf3` (case count) | **2** | **0 / None — `CANNOT_EVALUATE: missing capability row (sources-registry)`** | — |
| `0e5f70f` (complete table) | 0 | 27 / 0 | — |

Two things follow.

**(a) The declared repair scope is wrong.** The declaration scopes the change to *"append-only correction of the
five current self-assessment count cells to the measured tip values"* and states *"only the self-assessment values
may change"*. But the landed repair also appended a **third** `## Capabilities` table (`d06cedb`) and then two more
(`ee36f9e`, `5124bf3`, `0e5f70f`), changing the capabilities *evidence pointers* — not self-assessment values. That
extra scope is what caused the K17/K18 failures: the new rows cited `after.md`, `selftest-after.json` and
`mode-policy-mutant.json` as bare tokens, and the checker's path grammar treats a `.md`/`.json` suffix as a
repository path (`check-self-assessment.py:263-276`), so those bare names resolve to paths that do not exist at the
revision. The round-35 rows they were copied from spelled the same files with their full directory prefixes
(`SCORECARD.md:1585-1586`), which is why the base passed.

**(b) The declared freeze is breached by the repair itself.** `5124bf3` — a commit made *after* the freeze
commit — produces **exit 2 `CANNOT_EVALUATE`**, not a mismatch count. The declared predicate is
`mismatches == 0 && checked == 27 && exit == 0`; at `5124bf3` the checker reports `checked: 0, mismatches: null`,
so the declared command does not evaluate the claim at all at that revision. The lane's own receipt
`after-c3-5124bf.json` records this (`"status": "CANNOT_EVALUATE", "error": "missing capability row"`), so this
is not an artifact of my fixture — my replay reproduces the lane's file byte-for-byte and gets byte-identical
output.

### 2.3 The after-value re-drifts as the round lands its own commits

The mismatch count is **not monotone**; it rises again as round-37 lands the commits its own declaration schedules.
Measured with the unchanged checker at each landed commit (`--revision <rev>`):

| revision | commit | mismatches | failing checks |
|---|---|---|---|
| `0e5f70f` | complete current capability evidence table | **0** | — (exit 0, PASS) |
| `8936643` | assimilate sourced errno entries and quarantine gate | **3** | K07 K10 K11 |
| `543a7ce` | correct journalctl v262 note and add finite counter | **5** | K07 K08 K09 K10 K11 |
| `718cc8f` | align C2 counter with source identifier spelling | **5** | K07 K08 K09 K10 K11 |
| `d621b71` | align C2 action assertion and mutation fixture | **5** | K07 K08 K09 K10 K11 |

The tip `d621b71` is `FAIL`, exit 1 — the claim's declared after-value **does not hold at the measured tip**.
The cause is structural, not accidental: K07 counts `corpus/knowledge/*.md`, K08/K09 count `SKILL.md` lines and
pipe lines, K10 counts `corpus/lessons/` files, K11 counts `corpus/README.md` lines. The round's change commit
adds a knowledge note (`corpus/knowledge/journalctl-v262-field-filter-r36.md` corrections), a lesson file
(`corpus/lessons/round-37.md`), SOURCES/README/SKILL registry rows — so it moves the counts the table states.
A count restated at revision *R* is stale at revision *R+1* by construction.

This is not a new observation about this round only: it is the **same failure the lane has repaired five times
already**. `SCORECARD.md:1086` (round 28: *"K10 mismatch at the base `3b9e0430`"*), `:1282` (round 32: *"the
round-31 depth row states 38 lesson files while `corpus/lessons` holds 39"*), `:1386` (round 33: *"the round-32
row's 40 was stale"*), `:1803` (round 36: *"this axes row states the current counts (K07/K10 self-assessment drift
repaired)"*). Each round restates the counts at its tip, and the next round's first commit invalidates them
again. C3 as declared reproduces the loop rather than breaking it.

### 2.4 The minimal correction is sufficient — and the extra scope was not

`fixture-scope.sh` / `fixture-minimal-correction.sh` test the declared scope in isolation. Starting from the base
export and changing **only** the five axes count cells (no capabilities edit at all), the unchanged checker reports:

```
M1 (base + five-cell axes correction only):  exit 0, checked 27, mismatches 0, status PASS
```

So the declaration's stated repair scope **does** produce the declared after-value at the base — the extra
capabilities-table churn in the landed repair was unnecessary, and it is what produced the K17/K18 failures and
the exit-2 state. The lane's landing was a superset of what the claim needed, and the superset is where the
intermediate breakage came from.

---

## 3. Correction proposal (does not touch the checker)

Two parts. Part A is the repair; Part B is the one-line predicate change that makes the claim's after-value
**durable** rather than a snapshot.

### Part A — the cell-level correction (append-only, verified)

Append a new `## Axes — current self-assessment (round 37)` section to `SCORECARD.md` whose depth and coverage
rows state the counts measured **at the revision that adds the section**, using the literal phrases the parser
requires (the round-35 wording `grep -c '^[|]' SKILL.md` and `find corpus/lessons -type f` do **not** match the
K08/K09/K10 patterns — `check-self-assessment.py:648-680`):

```
| depth | 8 | 58 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3111 `wc -l` / 840 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 50 files (`find corpus/lessons -type f | wc -l`); four standing rules near the top of SKILL cite no knowledge note; no ordinal move claimed. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 282 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes; four declared round-1 read-only surfaces link knowledge; pacnew census arm C1 was not verified in round 35, no coverage ordinal move. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
```

(The five numbers are the measured tip values at `d621b71`: 58 notes, 3111 SKILL.md lines, 840 pipe lines, 50
lesson files, 282 README lines.) **Leave the capabilities table untouched** — the base capabilities rows already
satisfy K16–K19 (they name full paths, and K17's `105 cases` matches the census).

Verified end-to-end by `fixture-restatement-at-tip.sh` against the tip tree, unchanged checker:

```
T0 (tip export, untouched):          exit 1, checked 27, mismatches 5, FAIL
T1 (tip + re-stated five cells):      exit 0, checked 27, mismatches 0, PASS
```

and at the base by `fixture-minimal-correction.sh`:

```
M0 base:                exit 1, checked 27, mismatches 5, FAIL
M1 five-cell correction: exit 0, checked 27, mismatches 0, PASS
M2 + change commit:     exit 1, checked 27, mismatches 4, FAIL   (K07 K08 K09 K10 — the drift returns)
M3 + re-stated cells:   exit 0, checked 27, mismatches 0, PASS
```

### Part B — the durable predicate (the actual fix for C3's calibration axis)

Part A alone is a snapshot: the M2 row shows it is invalidated by the very next content commit, and §2.3 shows
the lane's landed repair failing exactly that way. To make the after-value mean something, the declared predicate
should be **per-revision rather than per-tip**:

> The frozen predicate is: for the measured revision *R*, `check-self-assessment.py --revision R` reports
> `checked: 27`, `mismatches: 0`, `exit 0`; **and** for every commit that changes any counted corpus
> (`corpus/knowledge/*.md`, `corpus/lessons/`, `SKILL.md`, `corpus/README.md`), the axes table's stated counts
> equal the counts at that commit's own revision.

Under Part B, the base-to-tip series becomes: 5 → 0 (corrected) → 4 (change commit invalidates it) → 0
(re-stated). The round ends with a *state*, not a snapshot, and the "re-measure at every later commit" rule the
lane already writes into its own tables (`SCORECARD.md:906`: *"the tool always measures at the revision given, so a
later commit cannot change the measured result, and every later round re-measures"*) becomes part of the claim's
own pass condition instead of an admission that the repair does not hold.

Part B also subsumes the two smaller defects found:

- **K17's case count** should be read from a *full* table row (all four capability rows present), not from a
  partial table — `pick_table` (`check-self-assessment.py:295-303`) takes the last table whose header names
  `Capability`, so a one-row correction table shadows the full one and drops three required rows, producing the
  `5124bf3` exit-2 state.
- **The `after.md` / `selftest-after.json` path tokens**: any capabilities row naming a file must give it with
  its full repository path, since the path grammar resolves a bare `.md`/`.json` name against the repository root.

---

## 4. Confidence and remaining unknowns

**High confidence (directly observed, reproduced twice by independent fixtures and by the lane's own receipts):**
- The base before-value (27 checked, 5 mismatches, K07–K11, exit 1) — exact reproduction.
- The declared after-value is **false at the measured tip** (`d621b71`: 5 mismatches, exit 1) and was false at
  every commit from `8936643` onward.
- The mismatch count rises monotonically-ish with each content commit that the round lands (0 → 3 → 5 → 5 → 5).
- The minimal five-cell correction alone yields `mismatches 0, exit 0` at both base and tip under the unchanged
  checker; the landed capabilities-table churn was the source of the K17/K18 failures and the exit-2 state.
- `5124bf3` returns exit 2 `CANNOT_EVALUATE`, so the declared predicate does not evaluate at that revision — the
  lane's own receipt agrees.

**Medium confidence:**
- That K10 is the *most* load-bearing stale value rather than K07. Both are stale at the base and both recur
  across rounds. K10 is named because it is the check the lane's own history shows failing at five consecutive
  round bases; K07 is equally defensible.

**Open unknowns (not resolvable from this seat):**
- Whether the round intends to land one further axes-table commit after the last content commit (which would
  restore `mismatches 0` at the tip). If so, the claim's after-value becomes true at the tip but remains a
  snapshot; if not, the claim as declared is unmet.
- Whether the lane will accept the Part B predicate change. It changes the *claim*, not the checker, and the
  declaration's own "re-measures every later round" language suggests the L1 is aware of the issue.
- The `checked: 27` population is fixed by construction (6 ordinal + 9 observed-state + 4 capability + 4 SHONEN-path
  + 4 SHONEN-note = 27) and did not drift across the five commits I measured.

---

## 5. Artifacts in this seat directory

All under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-37/w1/C38Ledger824/`:

| file | what it does |
|---|---|
| `fixture-durability.sh` | base export → simulated change commit → proposed correction; shows the correction restores 0 and that the next content commit re-breaks it |
| `fixture-scope.sh` | replays each landed `SCORECARD.md` blob over the base tree and attributes every intermediate failure (5 → 2 → 1 → exit 2 → 0) |
| `fixture-minimal-correction.sh` | the minimal five-cell correction in isolation (M0–M3) |
| `fixture-restatement-at-tip.sh` | re-statement at the post-change-commit tip (T0–T1) |
| `results/` | the JSON output, stderr and exit code of every checker run |

Every fixture: fresh `mktemp -d` repo, `git init`, top-level asserted equal to the fixture root **before** any
commit, lane accessed read-only via `git archive` / `git show` only. No lane, fleet, sibling or
`/home/vgpnk/Projects/shokuknow` write; no pacman; no `git add`/`commit`/`push`/`fetch` in any lane repository; no
delegation or background wave spawns.

## 6. Sources actually opened this round

| source | how opened | located quote |
|---|---|---|
| `tools/check-self-assessment.py` | read in full (1123 lines) + `sha256sum` | docstring: *"Fixed check set v2, K01 to K27, declared in SCORECARD.md, 'Round 26 - declaration, attempt 1'"*; K10 at `:671-680`; path grammar `:263-276`; `pick_table` `:295-303` |
| `SCORECARD.md` (lane, working tree at tip) | read `:1-300`, `:1780-2011`; `git show` per revision | round-37 C3 pre-freeze correction: *"the same command at the measured round-37 branch-tip revision reports `checked: 27`, `mismatches: 0`, `status: PASS`, exit 0"*; base table `:1564-1575`; recurrence `:1086,1282,1386,1803` |
| `.ufo/waves/round-37/before/c3-before.json` | read | `"mismatches": 5`, `"status": "FAIL"`, ids `K07 K08 K09 K10 K11` |
| `.ufo/waves/round-37/after-c3-{d06cedb,ee36f9e,5124bf3,0e5f70f}.json` | read | `5124bf3`: `"status": "CANNOT_EVALUATE", "error": "missing capability row"` |
| `tools/tsukuroi-census.sh` | read `:2810-2835`; executed `--selftest` ×3 | `printf 'TSUKUROI_CENSUS_SELFTEST: %s (%d cases, %d passed, %d failed)\n'` |
| `corpus/SOURCES.md`, `PROVINCE.md`, `SHONEN.md` | read via `git show` at base and tip | K12/K15 evidence: PROVINCE holds `## Core`/`## Frontier`/`## Adjacent` and a `\| ID \| Finding` table |

No external URL was opened this round; every source is a lane file read from this workstation, and every quoted
figure was produced by a command recorded above.

## 7. Tooling

No tool was installed or updated this round — **no pacman transaction** (host-wide pause in force; nothing in this
seat required a new binary). Tools used, all pre-existing: `git` (read-only: `show`, `ls-tree`, `archive`,
`rev-parse`, `status`), `python3` (checker execution), `bash` (census selftest, fixture scripts), `sha256sum`,
`grep`/`sed`/`awk`/`mktemp`/`tar`.
