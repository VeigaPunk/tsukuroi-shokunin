# ScoutDrift — round 97 wave w1 — drift surface and the named limit C2 discloses

Seat: `ScoutDrift` (scout, leaf member; no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch `master`, HEAD `a57e88cd`, detached).
Pre-round tip: `f48d16428d8bb92fd6cf546a745bff5b624e3f18`.
Scratch root (created, used, deleted): `/fast/scratch/hyaku/tsukuroi-r97/ScoutDrift`.
Seat dir (the only thing this seat wrote in the lane):
`.ufo/waves/round-97/w1/ScoutDrift/` — `report.md`, `measure.py`, `receipts/`, `receipts-frozen/`.

No file outside this seat dir was edited. No `git`/`jj` mutation was run in the lane; the only
commits this seat made were inside scratch clones, each preceded by
`git -C <clone> rev-parse --show-toplevel` printing that clone's own path (recorded in
`receipts/doctored-fixture-rebuild.txt`). No tool was installed (none needed): the seat used only
`git`, `python3` (3.14.8, preinstalled), `sha256sum`, `grep`, `sed`/`awk` via `bash`. No pacman
transaction (pacman is paused host-wide).

---

## 1. Hash comparison table

Command (lane root):

```
sha256sum tools/check-limine-pins.py .ufo/waves/round-97/before/controls/do-nothing-gate.py \
          .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py \
          tools/check-registry-coverage.py \
          .ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py \
          tools/limine-pin-battery-r97.py tools/check-registry-content.py \
          tools/check-r96-calibration.py tools/make-r97-bends.py
```

Raw output:

```
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  .ufo/waves/round-97/before/controls/do-nothing-gate.py
f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba  .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py
6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812  tools/check-registry-coverage.py
6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812  .ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py
e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8  tools/limine-pin-battery-r97.py
2daf59267ed923370fd825c21d9ac33ec2fbe95f58216a125a5346b7540cb3a6  tools/check-registry-content.py
7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4  tools/check-r96-calibration.py
972c672b337021130b807a88813ed79e01a58b63969581dbd9019a3dbd09177e  tools/make-r97-bends.py
```

| file | expected | observed | match |
|---|---|---|---|
| `tools/check-limine-pins.py` | `7d79ac29…` (gate, unchanged this round) | `7d79ac29…6090d32` | **PASS** |
| `.ufo/waves/round-97/before/controls/do-nothing-gate.py` | `7d79ac29…` | `7d79ac29…6090d32` | **PASS** (byte-identical to the gate) |
| `.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py` | `f06d90ae…` | `f06d90ae…ae73bba` | **PASS** |
| `tools/check-registry-coverage.py` | `6fcb2d0a…` | `6fcb2d0a…720a24812` | **PASS** |
| `.ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py` | `6fcb2d0a…` | `6fcb2d0a…720a24812` | **PASS** (byte-identical) |
| `tools/limine-pin-battery-r97.py` | `e678c34f…` (frozen manifest) | `e678c34f…a080e6a1a8` | **PASS** |
| `tools/check-registry-content.py` | `2daf5926…` (frozen manifest) | `2daf5926…7540cb3a6` | **PASS** |
| `tools/check-r96-calibration.py` | `7ff63524…` (frozen manifest) | `7ff63524…81dbc4` | **PASS** |
| `tools/make-r97-bends.py` | `972c672b…` (frozen manifest) | `972c672b…3d09177e` | **PASS** |
| `tools/limine-pin-battery-r96.py` (worktree) | `f06d90ae…` at the pre-round tip | `0d98b5bd0ac0ce68671b7355256c41aec636b7842be1a6069b707e6954007eab` | **FAIL (expected, disclosed)** — the r96 Y-family docstring correction (routed defects 2/3) landed in the worktree; the *scored* bytes stay re-derivable at `f48d1642:tools/limine-pin-battery-r96.py` = `f06d90ae…`. The frozen do-nothing control copy is still `f06d90ae…`. Recorded in `corpus/lessons/round-97.md` § Routed item 2/3. |

`sha256sum -c .ufo/waves/round-97/before/instruments.sha256` (run in the lane root):

```
.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh: FAILED
sha256sum: WARNING: 1 computed checksum(s) did NOT match
```

19 of 20 lines OK; the single FAILED line is the **recipe** (not a scored instrument). Its
worktree bytes are `e4cf82a0f4c6307e057fd0b75c7bcadb21eb6c972859cd3ba1c837eccc74081f`; the frozen
manifest line names `c2ecf729…` (the committed blob). The lane's own sidecar
`.ufo/waves/round-97/before/instruments-r97-after-fixture-pin.sha256` pins the corrected set:
`sha256sum -c .ufo/waves/round-97/before/instruments-r97-after-fixture-pin.sha256` → **20/20 OK**
(no output other than the OK lines). The narrowing pointer is
`.ufo/waves/round-97/before/plan-amendments-r97.md` § A1 (a `plan-amendments-r97.md` sidecar, the
append-only slot the frozen plan names; the plan bytes themselves are untouched).

**Every scored instrument is byte-identical to the freeze manifest.** The only manifest FAILED line
is a recipe the plan's Amendment slot and A1 already re-pin.

## 2. Copied controls vs the frozen pre-round tip

```
git show f48d1642:tools/limine-pin-battery-r96.py   | sha256sum
git show f48d1642:tools/check-limine-pins.py       | sha256sum
git show f48d1642:tools/check-registry-coverage.py | sha256sum
```

| control copy | pre-round path | control sha256 | pre-round sha256 | difference |
|---|---|---|---|---|
| `.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py` | `f48d1642:tools/limine-pin-battery-r96.py` | `f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba` | `f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba` | **none (byte-identical)** |
| `.ufo/waves/round-97/before/controls/do-nothing-gate.py` | `f48d1642:tools/check-limine-pins.py` | `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32` | `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32` | **none (byte-identical)** |
| `.ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py` | `f48d1642:tools/check-registry-coverage.py` | `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812` | `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812` | **none (byte-identical)** |

**No difference on any of the three.** The do-nothing battery is the r96 landed bytes; the gate is
unchanged since the pre-round tip; the coverage gate is unchanged since the pre-round tip.

### 2b. Coverage-gate drift at the landed tip (a finding the round's own plan implies but does not state)

```
python3 tools/check-registry-coverage.py --revision a57e88cd   # the freeze / landed tip
{"branch":"master","branch_tip":"a57e88cd…","counts":{"findings":3,"missing":3,"registered":154,"rows_total":154,"tools_total":157},
 "findings":[{"id":"REGISTRY-ROW-MISSING","site":"tools/check-registry-content.py"},
             {"id":"REGISTRY-ROW-MISSING","site":"tools/limine-pin-battery-r97.py"},
             {"id":"REGISTRY-ROW-MISSING","site":"tools/make-r97-bends.py"}],"status":"FAIL"}

python3 tools/check-registry-coverage.py --revision f48d1642   # the pre-round tip
{"…","counts":{"findings":0,"missing":0,"registered":154,"rows_total":154,"tools_total":154},"findings":[],"status":"PASS"}
```

At the freeze tip the coverage gate reads **FAIL / 3 missing** because the freeze commit added the
round's three tools under `tools/` without their registry rows (QUALITY 70, R27-REGISTRY-ROW-MISSING).
The working tree already carries the three rows (`SKILL.md` +3 lines) and the coverage gate reads
**PASS 157/157 findings 0** at that table — verified by committing the worktree `SKILL.md` into a
scratch clone on the freeze tip (`a8461e8dd79cf8a45da4f0e01861a0042221cc13`):
`{"counts":{"findings":0,"missing":0,"registered":157,"rows_total":157,"tools_total":157},"status":"PASS"}`,
and `tools/check-registry-content.py --revision a8461e8d…` → `registry-content: status PASS
bindings 7/7 findings 0`. **The settle's own rows are still uncommitted at the time of this seat's
reading**, so the coverage gate is red at the landed tip and green only once they land.

### 2c. C2's doctored-leg blindness depends on the fixture base (re-derived, not copied)

Full receipt: `receipts/doctored-fixture-rebuild.txt`.

* **Base = lane master `a57e88cd` (the freeze tip).** The six content-only substitutions each
  matched exactly once; the content checker reads `status FAIL bindings 1/7 findings 6` (one
  `RC-VALUE-MISMATCH` per doctor, naming its row) — but the **coverage gate reads FAIL with 3
  `REGISTRY-ROW-MISSING` findings**, not `PASS 154/154`. The claim's blindness leg does not hold
  on this base.
* **Base = the pinned pre-round tip `f48d1642`.** Same six substitutions, each matched exactly
  once; content checker `status FAIL bindings 1/7 findings 6` (the identical six findings), coverage
  gate `{"counts":{"findings":0,"missing":0,"registered":154,"rows_total":154,"tools_total":154},"status":"PASS"}`.
  **The claim's C2 blindness leg reproduces exactly on this base.**

This is the drift amendment A1 records (the recipe was corrected after the freeze to pin
`BASE=f48d1642…`). The seat's independent re-derivation confirms A1's reading: the fixture base is
load-bearing for the blindness leg, and the pinned base is the one on which the leg holds.

## 3. The named limit C2 discloses — the operative table's binding coverage

**Command** (this seat's `measure.py`, written under the seat dir; it reads the operative table
with the frozen checker's own locator `operative_rows()` and re-derives every candidate cell with
the frozen checker's own derivers `crc.DERIVERS` / `crc.parse_tally`):

```
python3 .ufo/waves/round-97/w1/ScoutDrift/measure.py <lane> <outdir> [<SKILL.md to read>]
```

Receipts: `receipts/measure-frozen-154rows.json` (the 154-row table at `a57e88cd`),
`receipts/measure-worktree.json` (the 157-row table in the working tree),
`receipts/deriv-full-worktree.json` (per-cell detail), `receipts-frozen/measure-stdout.txt`.

### 3a. The count

At the **154-row operative table the claim's limits speak of** (read from the freeze tip
`a57e88cd`):

| quantity | value |
|---|---|
| operative rows | **154** |
| rows carrying a cell whose shape a BINDINGS capture matches (all 7 kinds) | **21** |
| rows carrying a **numeric** bound-kind cell (selftest tally / roster size / variant span) | **20** |
| rows whose bound-kind cell is **machine-checkable today** (the value re-derives from the named tool's bytes and equals the declared value) | **15** |
| rows whose bound-kind cell **cannot** be re-derived (derivation fails closed) | **7** (of which 2 — `limine-pin-battery-r88`, `limine-pin-battery-r89` — have a *second*, roster cell that does derive) |
| rows **bound** by `BINDINGS` | **4** (`limine-pins`, `limine-pin-battery-r96`, `check-r96-calibration`, `make-r96-bends`), 7 cells |
| rows that are machine-checkable but **not bound** | **11** |

So the disclosure is:

* `154 − 20 = 134` rows carry **no** numeric bound-kind cell at all (nothing a content-binding
  checker could re-derive);
* `154 − 15 = 139` rows carry nothing machine-checkable today;
* `154 − 4 = 150` rows are left presence-only by the freeze — **but 11 of those 150 are already
  machine-checkable** and are left unbound only because the binding set is frozen at 4 rows.

**The claim's stated limit ("C2 binds 4 of the operative table's 154 rows (7 cells). Every other row
stays presence-only") is accurate as written. The seat's measurement adds the sharper number the
limit does not state: the bindable surface at the freeze is 15 rows, not 4 — 11 more rows are
re-derivable today at zero new-instrument cost.** That is the drift surface C2's limit discloses,
and it is the natural next round's depth.

The 4 rows C2 binds, with the exact cell and its re-derived value (all verified to match):

| row | cell | declared | re-derived from | value |
|---|---|---|---|---|
| `limine-pins` | 2 (entry command) | `default \`auto\`` | `tools/check-limine-pins.py` argparse `--limine-version` default | `auto` |
| `limine-pins` | 4 (self-test) | `(39 fixtures` | `tools/check-limine-pins.py --selftest` printed tally | `39` |
| `limine-pins` | 5 (pinned values) | `schema \`tsukuroi-limine-pins-v3\`` | `tools/check-limine-pins.py` JSON schema literal | `tsukuroi-limine-pins-v3` |
| `limine-pin-battery-r96` | 3 (verdict map) | `FAMILY_ROSTER, 103,` | AST count of `tools/limine-pin-battery-r96.py` | `103` |
| `limine-pin-battery-r96` | 5 (pinned values) | `roster 103 (` | same AST count | `103` |
| `check-r96-calibration` | 4 (self-test) | `(7 cases` | `tools/check-r96-calibration.py --selftest` printed tally | `7` |
| `make-r96-bends` | 5 (pinned values) | `VARIANTS N01-N04` | AST keys of `tools/make-r96-bends.py` | `N01-N04` |

The 11 machine-checkable rows left unbound (each with at least one cell that re-derives cleanly
today): `append-receipt` (5), `check-line-endings-r64` (7), `limine-pin-battery-r88` (38),
`limine-pin-battery-r89` (50), `limine-pin-battery-r90` (73), `limine-pin-battery-r91` (82),
`limine-pin-battery-r92` (89), `limine-pin-battery-r93` (96), `limine-pin-battery-r94` (98, in two
cells), `limine-pin-battery-r95` (99, in two cells), `make-r94-bends` (`N01-N04`).

Rows whose bound-kind cell does **not** re-derive (so a binding there would read `RC-DERIVE-FAILED`,
not a mismatch): `check-cited-receipts-r62` (no `PASS N/N` tally printed), `count-mp-rows-r71`
(`--selftest` exits 2: needs `--revision`/`--fixture`), `count-resume-rows-r84` (`--selftest` exits 2),
`hibernate-resume` (prints `{"cases": 13, …}` JSON, no `N/N` tally),
`limine-pin-battery-r87` (`--selftest` exits 1: its `reference-gate` case needs a committed fixture
path under `.ufo/waves/round-87/…`), and the *self-test* cells of `limine-pin-battery-r88`/`r89`
(same `reference-gate` dependency — their roster cells do derive). `scorecard-unique-sections-r55`
matches the `default \`…\`` shape but is not a `--limine-version` default, so the argparse deriver
fails it by design.

### 3b. The same measurement at the working-tree table (157 rows)

| quantity | value |
|---|---|
| operative rows | **157** |
| rows with a bound-kind cell (all kinds) | **24** |
| rows with a numeric bound-kind cell | **23** |
| rows machine-checkable today | **18** |
| rows bound by `BINDINGS` | **4** (the same four; the three new r97 rows are **not** bound, exactly as the freeze's limit says) |

The three rows added by the settle (`limine-pin-battery-r97`, `make-r97-bends`,
`check-registry-content`) each carry bound-kind cells that re-derive cleanly against their own
tool — verified by re-deriving them the same way:
`limine-pin-battery-r97` roster `105` (AST) and self-test `5`;
`make-r97-bends` variant span `N05-N06`; `check-registry-content` self-test `12`. They are unbound
because `BINDINGS` was frozen at 7 cells over 4 rows — the disclosed limit ("a row added after this
freeze is not bound"), confirmed by measurement, not by reading.

**Note on the count the freeze's own documents quote.** The limit text and the new row's cell 5 both
say "the other **150** rows stay presence-only" / "the other 150 operative rows". That number is
`154 − 4` and is correct **for the 154-row table at the freeze**, but the table the settle produces
has **157** rows, so at the settled tip the correct figure is **153**. The row that carries the
number (`check-registry-content`, cell 5) is itself one of the three new rows, and its own count
will be stale the moment its own table gains its neighbours. Not a claim defect (the claim's
sentence says "154"), but a self-referential cell whose value the frozen checker does not bind.

## 4. Drift sweep over the r96 documents the round corrects

Command (as specified):

```
git grep -n "103/103" -- corpus SCORECARD.md LOG.md | wc -l      →  13
git grep -n "Z-cap\|leading-zero" -- corpus                      →  4
```

Both counts are at the **committed** tree (`a57e88cd`, HEAD). The same two sweeps in the working
tree (which already carries the round's settle edits) read **16** and **8** respectively — the
increase is the round's own new prose, listed below.

### 4a. `103/103` — 13 committed carriers, and which survive this round

| carrier | line | statement | still accurate after this round? |
|---|---|---|---|
| `corpus/knowledge/limine-bound-per-component-r96.md` | 53 | "`… --runs 3` reads `103/103 met`" (r96's own measurement) | **yes** — a dated r96 measurement; historical record |
| `corpus/knowledge/limine-bound-per-component-r96.md` | 76 | "`M06-z-cap-8` and `M08-refusal-9digit-below-1e8` survive 103/103 … QUALITY 139's boundary rule is certified at family level for X and Y only" | **NO — superseded by this round** (see 4c) |
| `corpus/README.md` | 1173 | "The Z component's 9-digit boundary is **uncertified**: `M06-z-cap-8` survives 103/103" | **NO — superseded by this round** (see 4c) |
| `corpus/README.md` | 1175 | "a 9-digit component with leading zeros (`000000001.0.0`) is unsent — `M08` survives 103/103" | **NO — superseded by this round** (see 4c) |
| `SCORECARD.md` | 7399 | "`check-knowledge-header.py --revision 46d48a71` PASS 103/103" | **yes** — an unrelated tool |
| `SCORECARD.md` | 7938 | r96 C1 measured row (roster 99 → 103) | **yes** — dated r96 record |
| `SCORECARD.md` | 7953 | "leading zeros are uncertified (`MutBound` M06/M08 survive `103/103`)" (r96 Frontier, measured this round) | **NO — superseded by this round** (see 4c) |
| `LOG.md` | 3907 | an r-round census line "103/103" | **yes** — unrelated |
| `LOG.md` | 4222 | r96 settle: "landed gate `103/103 met`" | **yes** — dated r96 record |
| `corpus/lessons/round-56-verifier-spotcheck.md` | 82 | probe receipts "103/103/36/36/0/103" | **yes** — unrelated historical spot-check |
| `corpus/lessons/round-57-verifier-spotcheck.md` | 29 | same | **yes** — unrelated |
| `corpus/lessons/round-87-verifier-spotcheck.md` | 83 | `check-knowledge-header` PASS 103/103 | **yes** — unrelated |
| `corpus/lessons/round-96-verifier-spotcheck.md` | 150 | "103/103 battery re-run" | **yes** — dated r96 record |

Working-tree additions (the round's own prose, all dated r97 and correct): `LOG.md:4264` ("the r96
control `met 103/103` ×3"), `SCORECARD.md:7971` ("blind to both **on its roster leg** (`met 103/103`)"),
`corpus/README.md:1198` ("`met 103/103`; its `--usage-check` already sends `12.09.4`/`00.00.00`").

The seat independently confirmed the roster-leg blindness reading the r97 SCORECARD asserts, by
running the frozen do-nothing battery's `--usage-check` mode (not its roster leg) against the two
new bends and the gate:

```
$ python3 -I do-nothing-battery-r96.py --usage-check --gate ./N06-leading-zero-reject.py   →  "verdict": "unmet"
$ python3 -I do-nothing-battery-r96.py --usage-check --gate ./N05-z-cap-8.py                →  "verdict": "met"   (15 cases)
$ python3 -I do-nothing-battery-r96.py --usage-check --gate ./check-limine-pins.py          →  "verdict": "met"   (15 cases)
```

So the r96 battery's *usage* mode is **not** blind to the leading-zero class (it reads `unmet` on
`N06`) — it is blind only on its roster leg, exactly as the r97 SCORECARD and README now word it.
The Z class is blind at both levels. This confirms the round's A3 narrowing rather than the
looser pre-amendment wording; the freeze's own C1 target sentence says "blindness receipt for both
new families" without qualifying the mode, and the amendment narrows it.

### 4b. `Z-cap|leading-zero` — 4 committed carriers in `corpus/`

| carrier | line | note |
|---|---|---|
| `corpus/lessons/round-96.md` | 41 | r96 lesson prose ("the new Z-cap, leading-zero … limits in the README") — historical |
| `corpus/lessons/round-96.md` | 107–108 | r96 lesson: "mutants 5/8 killed (M06 Z-cap and M08 leading-zero survive — Frontier)" — historical |
| `corpus/lessons/round-92.md` | 109 | r92 lesson: "leading-zero versions unpinned (MED)" — historical |

(Three carriers by grep count; `round-96.md` matches on two lines, 41 and 107/108.) The working
tree adds five more, all in the round's own new material: `corpus/README.md:1187,1192,1196`,
`corpus/SOURCES.md:403` (the S392 row's `teaches` cell).

### 4c. Are r96's Frontier statements still accurate, and does one need a supersession pointer?

Four committed carriers still assert, in the present tense, the two things this round closes:

1. `corpus/README.md:1173` — "The Z component's 9-digit boundary is **uncertified**";
2. `corpus/README.md:1175` — "a 9-digit component with leading zeros (`000000001.0.0`) is unsent";
3. `corpus/knowledge/limine-bound-per-component-r96.md:75` — "The Z component's 9-digit boundary and
   a 9-digit component with leading zeros are **unsent**";
4. `SCORECARD.md:7953` — "leading zeros are uncertified (`MutBound` M06/M08 survive `103/103`)".

After this round both are **closed**: the r97 battery carries `REFUSAL-VERSIONS-9DIGIT-Z` and
`LEADING-ZERO-NORMALIZE`, the bends `N05-z-cap-8` / `N06-leading-zero-reject` kill them
(`103/105` and `104/105`), and `corpus/README.md` § Round 97 and `corpus/lessons/round-97.md`
§ "Frontier moved this round" both say so.

**Do they need a supersession pointer?** Under the lane's own append-only corpus discipline the
*records* stay (QUALITY 60/99/127 — a correction is an appended block, never an in-place edit), so
leaving the r96 sentences standing is correct as a historical record. What is missing is the
**pointer**:

* `corpus/knowledge/limine-bound-9digit-z-r97.md` (the new entry) **does not name
  `corpus/knowledge/limine-bound-per-component-r96.md`** as the entry it supersedes
  (`git grep -n "limine-bound-per-component" -- corpus/knowledge/limine-bound-9digit-z-r97.md` → no
  hit; `grep -n "^supersedes:" corpus/knowledge/*.md` → no hit in the whole knowledge directory).
  Compare the lane's own precedent one round earlier: `corpus/knowledge/limine-bound-per-component-r96.md:45`
  writes "The r95 Frontier's 'not sent at battery level' is therefore corrected here", i.e. the
  successor entry named the superseded frontier sentence in prose. The r97 entry states the new
  facts (`PC1`: "r96's own wave measured the Z leg uncertified"; `PC2`: "r96's Frontier names the
  leading-zero normalization … unsent at family level") but never names the r96 *entry* or the r96
  *sentences* it supersedes.
* `corpus/lessons/round-97.md` § "Frontier moved this round" **does** name both sentences verbatim
  ("The r96 Frontier's 'Z component's 9-digit boundary is uncertified' and 'a 9-digit component
  with leading zeros is unsent' are closed as families"), and § Routed carries a row
  "r96 Frontier: Z cap and leading-zero unsent → closed by C1's two families". **So the pointer
  exists at the lesson layer** and is missing only at the entry layer.
* `SCORECARD.md` has **no `## Round 97 — measured outcome` block** yet (only
  `## Round 97 — declaration`, line 7958). Every earlier round carries one
  (`## Round 96 — measured outcome` at 7934, `## Round 95 — measured outcome` at 7875), and each
  earlier measured outcome ends with a "Frontier (measured this round)" paragraph (r96's at
  7952). QUALITY 62 (R26-SELF-REFERENT-ORDINAL) and 65 (R26-SELF-AGREEMENT-ORDINAL) make the
  *next* round's ordinal check read an **earlier** round's measured-outcome record; the r96 measured
  outcome is the latest one, and it still says the Z leg and leading-zero are uncertified. A
  `Round 97 — measured outcome` block with its own Frontier paragraph is the missing carrier, and
  the r97 lesson already supplies the text for it.

**Bottom line of the drift sweep:** every r96 *measurement* remains accurate as a dated record; the
four r96 *Frontier assertions* listed in 4c are the ones this round closes, they are correctly
left standing (append-only), and what the corpus still lacks is (i) an explicit superseded-entry
pointer in `corpus/knowledge/limine-bound-9digit-z-r97.md` naming
`corpus/knowledge/limine-bound-per-component-r96.md`, and (ii) the `## Round 97 — measured outcome`
block in `SCORECARD.md` with its Frontier paragraph, without which the lane's latest measured
Frontier still reads "leading zeros are uncertified". Neither is a claim defect; both are
settle-time corpus items this seat reports and does not edit.

## 5. PASS/FAIL per expected line

| # | expected line | reading | verdict |
|---|---|---|---|
| 1 | `sha256sum tools/check-limine-pins.py` = `7d79ac29…` | `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32` | **PASS** |
| 2 | `sha256sum .ufo/waves/round-97/before/controls/do-nothing-gate.py` = `7d79ac29…` | same | **PASS** |
| 3 | `sha256sum .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py` = `f06d90ae…` | `f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba` | **PASS** |
| 4 | `sha256sum tools/check-registry-coverage.py` = `6fcb2d0a…` | `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812` | **PASS** |
| 5 | `git show f48d1642:tools/limine-pin-battery-r96.py \| sha256sum` == the do-nothing copy | `f06d90ae…` == `f06d90ae…` | **PASS** (no difference) |
| 6 | `git show f48d1642:tools/check-limine-pins.py \| sha256sum` == the do-nothing gate | `7d79ac29…` == `7d79ac29…` | **PASS** (no difference) |
| 7 | `git show f48d1642:tools/check-registry-coverage.py \| sha256sum` == the current coverage gate | `6fcb2d0a…` == `6fcb2d0a…` | **PASS** (no difference) |
| 8 | operative table = 154 rows at the freeze | 154 | **PASS** |
| 9 | binding-coverage count with command | 20 rows carry a numeric bound-kind cell; 15 are machine-checkable; 4 are bound (7 cells); `154 − 20 = 134` / `154 − 15 = 139` / `154 − 4 = 150` | **PASS** (reported) |
| 10 | the 4 rows C2 binds, listed | `limine-pins` (3 cells), `limine-pin-battery-r96` (2), `check-r96-calibration` (1), `make-r96-bends` (1) — all 7 values re-derived and matching | **PASS** |
| 11 | `git grep -n "103/103" -- corpus SCORECARD.md LOG.md \| wc -l` | 13 (committed) / 16 (working tree, incl. the round's own new prose) | **PASS** (reported) |
| 12 | `git grep -n "Z-cap\|leading-zero" -- corpus` | 4 (committed) / 8 (working tree) | **PASS** (reported) |
| 13 | r96 Frontier statements still accurate? | 4 of 13 `103/103` carriers are superseded Frontier assertions; measurements stay accurate as dated records | **PASS** (reported) |
| 14 | any statement needing a supersession pointer | yes — 2 corpus items (entry-level pointer; `SCORECARD.md` `Round 97 — measured outcome` block) | **PASS** (reported) |
| 15 | no file edited | only `.ufo/waves/round-97/w1/ScoutDrift/**` written | **PASS** |

## 6. Receipts (all under the seat dir)

| path | content |
|---|---|
| `.ufo/waves/round-97/w1/ScoutDrift/measure.py` | the measurement script (read-only over the lane; writes only into its outdir) |
| `.ufo/waves/round-97/w1/ScoutDrift/receipts/measure-frozen-154rows.json` | binding-coverage + drift sweep over the **154-row** table at `a57e88cd` |
| `.ufo/waves/round-97/w1/ScoutDrift/receipts/measure-worktree.json` | the same over the **157-row** working-tree table |
| `.ufo/waves/round-97/w1/ScoutDrift/receipts/deriv-full-worktree.json` | per-cell derivation detail (31 bound-kind cells: row, line, binding, cell index, declared, tool, status, derived, match) |
| `.ufo/waves/round-97/w1/ScoutDrift/receipts/doctored-fixture-rebuild.txt` | the two-base doctored-fixture re-derivation (own clones, own commits, toplevel asserted) |
| `.ufo/waves/round-97/w1/ScoutDrift/receipts/measure-stdout.txt` | stdout of the worktree measurement run |
| `.ufo/waves/round-97/w1/ScoutDrift/receipts-frozen/measure-stdout.txt` | stdout of the frozen-table measurement run |
| `.ufo/waves/round-97/w1/ScoutDrift/receipts/content-doctored.json` | the content checker's JSON on the lane-master-based doctored revision |

Scratch deleted (`/fast/scratch/hyaku/tsukuroi-r97/ScoutDrift`, including both clones and the bare
origins) before this yield.

## 7. Findings (reported, not edited)

1. **The coverage gate is red at the landed tip.** `check-registry-coverage.py --revision a57e88cd`
   reads **FAIL, 3 missing** (the round's three tools have no registry row at the freeze commit);
   it reads PASS 154/154 at the pre-round tip and PASS 157/157 once the settle's three rows land
   (verified in scratch). QUALITY 70 wants the row in the same round as the tool; the settle must
   land those rows for the gate to be green.
2. **C2's blindness leg is base-dependent.** Reproduced independently: on the lane master
   (`a57e88cd`) the doctored revision's coverage gate reads FAIL (3 missing), not `PASS 154/154`;
   only on the pinned pre-round base `f48d1642` does it read `PASS 154/154` with the content
   checker reading FAIL with exactly six `RC-VALUE-MISMATCH`. This is what amendment A1 records;
   the seat's re-derivation confirms it and adds the second leg's exact output.
3. **The bindable surface is 15 rows, not 4.** At the 154-row freeze table, 15 rows carry a cell
   that the frozen checker's own derivers re-derive today; C2 binds 4. The 11 unbound-but-checkable
   rows are the cheapest next round's depth (no new instrument needed).
4. **The "150 rows stay presence-only" figure is a self-referential cell that the settle
   invalidates.** It is `154 − 4`; at the settled 157-row table the figure is 153. The cell lives
   in the `check-registry-content` row, which the freeze does not bind.
5. **Two corpus pointers are missing (settle-time items).** (a) the new
   `corpus/knowledge/limine-bound-9digit-z-r97.md` does not name
   `corpus/knowledge/limine-bound-per-component-r96.md` as superseded (no `supersedes:` field
   anywhere in `corpus/knowledge/`, and the r96 entry did name its predecessor's sentence in
   prose); (b) `SCORECARD.md` has no `## Round 97 — measured outcome` block, so the lane's latest
   measured Frontier still reads "leading zeros are uncertified" — QUALITY 62/65 make the next
   round read exactly that record. The r97 lesson already carries the text for both.
6. **The r96 battery is blind to the Z class at both levels but to the leading-zero class only on
   its roster leg.** Measured with the frozen do-nothing copy's `--usage-check` mode: `unmet` on
   `N06-leading-zero-reject`, `met` on `N05-z-cap-8` and on the gate. The freeze's C1 sentence
   ("blindness receipt for both new families") is looser than the measurement; the settle's
   SCORECARD/README wording ("blind to both **on its roster leg**", "A3") is the accurate one.

## 8. Tooling

No tool was installed or upgraded. Environment used: `git` (preinstalled), `python3` 3.14.8
(preinstalled), `sha256sum` (coreutils, preinstalled), `grep`/`sed`/`awk` (preinstalled). The
generic tooling directive's channel order (pacman → `uv tool` → official binary → cargo/npm) was
not entered because the seat needed nothing beyond the preinstalled toolchain; pacman was left
alone (host-wide pause). No `sudo`, no sysctl/service/kernel/boot change.

{"seat":"ScoutDrift","verdict":"findings","notes":"Gate and all three copied controls are byte-identical to the freeze manifest and to the pre-round tip f48d1642 (no difference); the only manifest FAILED line is the doctored-fixture recipe, re-pinned by the lane's own sidecar (20/20 OK). Binding-coverage count at the 154-row freeze table: 20 rows carry a numeric BINDINGS-kind cell, 15 are machine-checkable today, 4 are bound (7 cells, all 7 re-derived and matching), 11 are machine-checkable but unbound -> 154-20=134 rows with nothing bindable, 154-15=139, 154-4=150 (the settle's 157-row table makes it 153). Drift sweep: 13 committed '103/103' carriers (16 in the worktree) and 4 'Z-cap|leading-zero' carriers (8); 4 of the 13 are Frontier assertions this round closes (README:1173/1175, limine-bound-per-component-r96.md:75, SCORECARD:7953) and still stand without a pointer. Findings: coverage gate reads FAIL 3 missing at the landed tip a57e88cd (PASS 157/157 once the settle's three rows land); C2's blindness leg reproduces only on the pinned pre-round base f48d1642 (on the lane master the doctored revision's coverage reads FAIL); the r96 battery's --usage-check reads unmet on N06 but met on N05 and the gate, so the blindness is roster-leg-only for the leading-zero class; two settle-time corpus pointers missing (no superseded-entry pointer in the new r97 knowledge entry, and no 'Round 97 - measured outcome' block in SCORECARD.md). No file outside .ufo/waves/round-97/w1/ScoutDrift/ was edited; scratch deleted."}
