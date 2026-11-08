# ScoutDrift — round 98 wave w1 — drift surface this round touches, and the limits C1/C2 disclose

Seat: `ScoutDrift` (scout, leaf member — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch `master`, git HEAD detached at
`1cfeb5d5089097fdffef761ad0e2b8dfa75a2793` — the round-98 freeze commit).
Pre-round tip: `b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a`.
Scratch root (created, used, deleted): `/fast/scratch/hyaku/tsukuroi-r98/ScoutDrift`.
Seat dir (the only thing this seat wrote in the lane): `.ufo/waves/round-98/w1/ScoutDrift/` —
`report.md` and `receipts/01..12`.

No file outside this seat dir was edited. No `git`/`jj` mutation was run in the lane; `git show`,
`git cat-file`, `git ls-tree`, `git rev-parse`, `git diff` and `git status` (read-only) were used.
`tools/make-r98-bends.py` was **not** run — the two bends were re-derived in the seat's scratch
from the pinned gate's bytes and compared byte-for-byte (§3). No tool was installed (none needed):
the seat used only `git`, `python3` (3.14.8, preinstalled), `sha256sum`, `grep`, `diff`, `sed`.
No pacman transaction (pacman is paused host-wide).

**Verdict: `findings`** — the freeze's bytes all verify (28/28 manifest lines OK, every scored
instrument byte-identical), both bend legs read exactly the claim's frozen targets, and the drift
sweep is clean — but three drift-surface facts need a pointer before this round's documents are
filed, and one is a numeric drift in a limit both the plan and the README still carry (§5, §6).

---

## 1. Hash comparison table

### 1a. The five files the item names

Command (lane root):

```
sha256sum tools/check-limine-pins.py \
          .ufo/waves/round-98/before/controls/do-nothing-gate.py \
          .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py \
          .ufo/waves/round-98/before/controls/do-nothing-checker-r97.py \
          tools/check-registry-coverage.py
```

Raw output:

```
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  .ufo/waves/round-98/before/controls/do-nothing-gate.py
e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8  .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py
2daf59267ed923370fd825c21d9ac33ec2fbe95f58216a125a5346b7540cb3a6  .ufo/waves/round-98/before/controls/do-nothing-checker-r97.py
6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812  tools/check-registry-coverage.py
```

| file | expected (manifest) | observed | match |
|---|---|---|---|
| `tools/check-limine-pins.py` | `7d79ac29…6090d32` | `7d79ac29…6090d32` | **PASS** — byte-identical to the frozen do-nothing gate copy |
| `.ufo/waves/round-98/before/controls/do-nothing-gate.py` | `7d79ac29…6090d32` | `7d79ac29…6090d32` | **PASS** — byte-identical to the live gate |
| `.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py` | `e678c34f…a080e6a1a8` | `e678c34f…a080e6a1a8` | **PASS** — byte-identical to `tools/limine-pin-battery-r97.py` |
| `.ufo/waves/round-98/before/controls/do-nothing-checker-r97.py` | `2daf5926…7540cb3a6` | `2daf5926…7540cb3a6` | **PASS** — byte-identical to `tools/check-registry-content.py` |
| `tools/check-registry-coverage.py` | `6fcb2d0a…720a24812` | `6fcb2d0a…720a24812` | **PASS** — byte-identical at the pre-round tip |

Manifest check (lane root), `sha256sum -c .ufo/waves/round-98/before/instruments.sha256`:

```
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r98.py: OK
tools/make-r98-bends.py: OK
tools/check-registry-content-r98.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-98.md: OK
.ufo/waves/round-98/before/plan-frozen.md: OK
.ufo/waves/round-98/claims.json: OK
.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py: OK
.ufo/waves/round-98/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-98/before/controls/do-nothing-checker-r97.py: OK
.ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py: OK
.ufo/waves/round-98/before/controls/bends/N08-echo-norm.py: OK
.ufo/waves/round-98/before/registry-baseline-r98.json: OK
.ufo/waves/round-98/before/fixtures/build-doctored-fixture-r98.sh: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D1: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2lie: OK
.ufo/waves/round-98/before/dev/c1-gate-runs3.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c2-selftest-r98.txt: OK
.ufo/waves/round-98/before/dev/c2-selftest-r97.txt: OK
.ufo/waves/round-98/before/dev/c2-doctored-summary.txt: OK
```

**27 of 27 manifest lines OK; 0 FAILED.** (Re-run after the wave's other seats had begun editing
the worktree: still 27/27 OK — no scored instrument drifted under this seat's feet.) The manifest
has **27** entries, matching the SCORECARD's "27 entries" (`SCORECARD.md:8013`).

Receipt: `receipts/01-hashes-and-manifest.txt`.

### 1b. The same five paths at `git show b3be3f90:<path>`

Command:

```
for p in <the five paths>; do
  printf "%s  " "$p"; git show b3be3f90:"$p" 2>/dev/null | sha256sum
  git cat-file -e b3be3f90:"$p" && echo present-at-base || echo ABSENT-at-base
done
```

| file | at `b3be3f90` (pre-round tip) | match to live/manifest |
|---|---|---|
| `tools/check-limine-pins.py` | `7d79ac29…6090d32` | **PASS** — identical to the live gate and the frozen control |
| `.ufo/waves/round-98/before/controls/do-nothing-gate.py` | **ABSENT at the base** (control committed *after* the base, in the freeze commit `1cfeb5d5`) | **n/a** — the base cannot carry it; the live copy is `7d79ac29…`, identical to `b3be3f90:tools/check-limine-pins.py` |
| `.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py` | **ABSENT at the base** (same reason) | **n/a** — the live copy is `e678c34f…`, identical to `b3be3f90:tools/limine-pin-battery-r97.py` |
| `.ufo/waves/round-98/before/controls/do-nothing-checker-r97.py` | **ABSENT at the base** (same reason) | **n/a** — the live copy is `2daf5926…`, identical to `b3be3f90:tools/check-registry-content.py` |
| `tools/check-registry-coverage.py` | `6fcb2d0a…720a24812` | **PASS** — identical to the live copy |

The three controls are absent at the base **by construction** — they are the round's own frozen
control copies, committed with the freeze. Their *sources* are what the base comparison must use:

```
git show b3be3f90:tools/limine-pin-battery-r97.py  | sha256sum  ->  e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8
git show b3be3f90:tools/check-registry-content.py   | sha256sum  ->  2daf59267ed923370fd825c21d9ac33ec2fbe95f58216a125a5346b7540cb3a6
git show b3be3f90:tools/check-limine-pins.py        | sha256sum  ->  7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32
git show b3be3f90:tools/check-registry-coverage.py  | sha256sum  ->  6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812
```

Each source hash equals its control copy's hash exactly. The do-nothing battery is
byte-identical to the r97 landed battery (`e678c34f…`, the plan's stated value) and the
do-nothing checker to the r97 landed checker (`2daf5926…`, the plan's stated value).

The same five paths at the freeze commit `HEAD` (`1cfeb5d5`) return the same five hashes as the
live tree — i.e. nothing under `tools/` or under the round's `before/controls/` drifted between
the freeze and this seat's run.

Receipt: `receipts/02-git-show-base.txt`.

---

## 2. The two diffs, classified

### 2a. `diff -u tools/limine-pin-battery-r97.py tools/limine-pin-battery-r98.py`

Raw diff: `receipts/03-diffs.txt`. Numstat `22 2` (22 insertions, 2 deletions — the *diffstat*
total would read "24 +/-", which is the R97-D2 class of mislabel; the numstat form is the one
quoted here). Three hunks:

| # | hunk (r97 line → r98 line) | lines | classification |
|---|---|---|---|
| 1 | `@@ -58,6 +58,16 @@` | +10 / −0 | **header / module docstring** — a new "Round-98 claim (C1, SCORECARD.md …)" paragraph in the battery's module docstring, stating the A7 closure and the A6 docstring correction. Narrative only; no executable code. New paragraph begins at **byte 4936** of the r98 battery (`bytes.find(b"Round-98 claim (C1, SCORECARD.md")`). |
| 2 | `@@ -1806,7 +1816,11 @@` (`fam_refusal_versions_9digit_z`) | +4 / −1 | **family flags + docstring** — the docstring gains the "r98: the case also asserts the echo … and the `visibility_era` label" sentence (the −1/+1 pair is the sentence `…this family is the Z leg's only witness."` → `…only witness. r98: the case also asserts …"`), and two new **executable** lines `c.check_echo = True` / `c.check_era = True`. The flag pair sits at **byte 81743**. |
| 3 | `@@ -1817,7 +1831,13 @@` (`fam_leading_zero_normalize`) | +6 / −1 | **docstring (the A6/R97-D3 correction) + family flags** — the text-comparer sentence is corrected (`"000000012.9.4"` → `"12.000000009.000000005"`, and the direction corrected to "text comparer orders it era A while `int()` reads 12.9.5"), plus a parenthetical naming the correction, plus the two executable `c.check_echo = True` / `c.check_era = True` lines at **byte 82960**. The A6 correction sentence is at **byte 82590**. |

Byte-level anchors (measured with `bytes.find` on the pinned bytes, QUALITY 141):

```
r98 battery: b"Round-98 claim (C1, SCORECARD.md"        -> 4936
r98 battery: b"    c.check_echo = True\n    c.check_era = True\n" -> 81743 (in fam_refusal_versions_9digit_z), 82960 (in fam_leading_zero_normalize)
r98 battery: b"r97 correction R97-D3/A6"                 -> 82590
r97 battery: b'orders `"12.09.4"` as era A'              -> 81323
r98 battery: b'orders `"12.09.4"` as era A'              -> 82439
r98 battery: b'but `"12.000000009.000000005"` as era A'  -> 82481   (absent in the r97 bytes: find -> -1)
```

**Executable delta: 4 lines** (two flag pairs) plus **no** change to `FAMILY_ROSTER`, `CASES_PER_FAMILY`,
`meta_ok`, `auto_ok` or the case builder. **Everything else is docstring.** The claim's "two
one-line changes" reads as *four* executable lines across two families (`check_echo` and
`check_era` on each) — the claim's own predicate wording ("sets `check_echo` and `check_era`") is
the accurate one; only the "two one-line changes" phrasing undercounts.

### 2b. `diff -u tools/check-registry-content.py tools/check-registry-content-r98.py`

Numstat `33 4`. Six hunks:

| # | hunk | lines | classification |
|---|---|---|---|
| 1 | `@@ -1,5 +1,5 @@` | +1 / −1 | **header** — `"""Round-97 registry CONTENT binding …` → `"""Round-98 registry CONTENT binding (tsukuroi lane; successor of the r97 checker): …`. At **byte 26**. |
| 2 | `@@ -38,6 +38,16 @@` | +10 / −0 | **module docstring** — the "Round-98 (C2, freshness 9)" paragraph naming the r97 M08 class, the new capture, and the two new selftest cases. At **byte 3283**. |
| 3 | `@@ -248,7 +258,7 @@` | +1 / −1 | **the executable change** — the `RC-BEND-SPAN` capture regex: `r"VARIANTS (N\d+-N\d+)"` → `r"VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))"`. At **byte 12743**. This is the *only* line that changes behaviour of the landed run. |
| 4 | `@@ -368,8 +378,18 @@` | +10 / −0 | **fixture (selftest support)** — the `FIXTURE_BENDS_GAP` non-contiguous `VARIANTS` fixture (`N01-one`, `N03-three`) and `FIXTURE_SKILL_GAP` (the SKILL row restating `VARIANTS N01,N03`), plus the `build_fixture` docstring's `gap` doctor sentence. At **byte 17996**. |
| 5 | `@@ -380,7 +400,14 @@` | +7 / −0 | **fixture (selftest support)** — `build_fixture` writes `FIXTURE_BENDS_GAP` for the `("GAP", None, None)` / `("GAP-LIE", None, None)` doctors and picks `FIXTURE_SKILL_GAP` only for `GAP`. |
| 6 | `@@ -414,6 +441,8 @@` | +2 / −0 | **selftest cases** — `("span-gap", ("GAP", None, None), [])` and `("span-gap-lie", ("GAP-LIE", None, None), ["RC-VALUE-MISMATCH"])`, at **bytes 21180** and **21223**. This is the "12 → 14" tally. |

**`BINDINGS` is unchanged**: 7 entries over 4 rows in both checkers, with the same ids
(`RC-ENTRY-DEFAULT`, `RC-SELFTEST-COUNT`, `RC-SCHEMA`, `RC-ROSTER-VERDICT`, `RC-ROSTER-PINNED`,
`RC-CAL-SELFTEST`, `RC-BEND-SPAN`) over the same rows (`limine-pins`, `limine-pin-battery-r96`,
`check-r96-calibration`, `make-r96-bends`). The r98 checker is a **successor**, not an in-place
edit: `tools/check-registry-content.py` keeps its r97 bytes (`2daf5926…`) and *is* the round's
do-nothing control.

Both diffs are therefore: **header + docstring + (for C1) two families' flag lines + (for C2) one
capture regex + two selftest cases and their fixture.** No roster change, no binding-set change,
no verdict-map change.

---

## 3. The frozen bend files, re-derived (not run through `make-r98-bends.py`)

`tools/make-r98-bends.py` was **not** run (it writes into the lane's frozen wave dirs). The two
substitutions were re-implemented in the seat's scratch from the pinned gate's bytes and compared
byte-for-byte with the frozen controls:

```
N07-era-field-lie      rederived=2d8f4f6eb4dbaed2 frozen=2d8f4f6eb4dbaed2 IDENTICAL
N08-echo-norm          rederived=45d8d00dbf19ad98 frozen=45d8d00dbf19ad98 IDENTICAL
```

Both re-derivations are byte-identical to the freeze manifest's values, so the frozen bends are
exactly what `make-r98-bends.py`'s single-clause substitutions produce from the pinned gate.

Receipt: `receipts/08-bends-rederived.txt`.

---

## 4. The two named limits, counted

### 4a. (a) r97 families that still set neither `check_echo` nor `check_era`

Two independent readings, both from the **r98** source as the item asks.

**AST parse** (`ast` over `FAMILY_ROSTER` → `FAMILIES` → each family's `c.check_echo` /
`c.check_era` assignments; lambdas resolved to the function they call):

| battery | roster | sets BOTH | echo only | era only | sets NEITHER |
|---|---|---|---|---|---|
| r97 | 105 | 0 | 1 (`EXPLICIT-VERSION-ECHO`) | 1 (`EXPLICIT-VERSION-ERA`) | **103** |
| r98 | 105 | **2** (`REFUSAL-VERSIONS-9DIGIT-Z`, `LEADING-ZERO-NORMALIZE`) | 1 | 1 | **101** |

`FAMILY_ROSTER` is 105 in both and `FAMILIES` has exactly the same 105 keys in both (no
roster/FAMILIES mismatch — the battery's own usage error never fires).

**Runtime probe** (each family's `Case` constructed in-process from the pinned battery; the
`Case` object's flags read after the family function runs):

| battery | roster | families sending an **explicit** `--limine-version` | of those, sets NEITHER | echo only | era only | BOTH | families sending no explicit flag |
|---|---|---|---|---|---|---|---|
| r97 | 105 | 100 | **98** | 1 | 1 | 0 | 5 (4 probe families + `ERA-DEFAULT`) |
| r98 | 105 | 100 | **96** | 1 | 1 | **2** | 5 |

**The count: 96 r98 families still set neither flag** (101 of the whole 105 roster; the other
four are the probe families and `ERA-DEFAULT`, which send no explicit flag and for which the
echo/era assertions do not apply). The r97 battery's corresponding figure is 98 of 100 — the
round moved exactly two families from "neither" to "both" and left every other family untouched.

**The sharper number, and the drift surface this discloses.** The flags are per-family, but what a
field lie can hide is per-*spelling*. Mapping every distinct version spelling the battery sends to
the families that assert its echo and its era:

| spelling sent | echo asserted by | era asserted by |
|---|---|---|
| `12.9.999999999`, `0.9.999999999` | `REFUSAL-VERSIONS-9DIGIT-Z` | `REFUSAL-VERSIONS-9DIGIT-Z` |
| `12.09.4`, `000000012.9.4`, `12.000000009.000000005`, `000000000.000000000.000000000` | `LEADING-ZERO-NORMALIZE` | `LEADING-ZERO-NORMALIZE` |
| `12.9.4`, `12.9.5`, `12.9.6`, `999999999.9.9` | `EXPLICIT-VERSION-ECHO` | `EXPLICIT-VERSION-ERA` |
| **`12.999999999.4`, `0.999999999.0`** | **— NONE —** | **— NONE —** |
| `auto` ×4 (probe shapes), `12.9.4` with `pass_version=False` (`ERA-DEFAULT`) | — NONE — | — NONE — |

So the **uncertified explicit-spelling surface after r98 is exactly two spellings** —
`12.999999999.4` and `0.999999999.0`, the two `REFUSAL-VERSIONS-9DIGIT-Y` members — plus the
probe-sourced cases (which read `source: "probe"`, where `auto_ok` covers the echo and the era
label follows the probed binary). The `REFUSAL-VERSIONS-9DIGIT` (X-cap) spelling `999999999.9.9`
**is** covered — by `EXPLICIT-VERSION-ECHO`/`-ERA`, which include `REFUSAL_DIGIT9` in
`EXPLICIT_VERSION_META`.

Receipts: `receipts/04-family-flags-and-counts.txt`, `receipts/11-spelling-coverage-map.txt`.

### 4b. (b) How many of the 157 operative registry rows C2 binds (7 cells over 4 rows)

Command (the r98 checker's **own** operative-table locator, `operative_rows()`, so the count is
the checker's, not the seat's):

```
python3 -c "… crc.operative_rows(SKILL.md) …"   # and the same over `git show <rev>:SKILL.md`
```

| revision | operative rows | rows bound by `BINDINGS` | bound cells | **rows left presence-only** | cells left presence-only |
|---|---|---|---|---|---|
| `f48d1642` (r97's base) | 154 | 4 | 7 | 150 | 154×8 − 7 = 1225 |
| `b3be3f90` (**r98's base**) | **157** | 4 | 7 | **153** | 157×8 − 7 = 1249 |
| `1cfeb5d5` (the freeze commit) | 157 | 4 | 7 | 153 | 1249 |
| worktree (with the three r98 rows added) | 160 | 4 | 7 | 156 | 160×8 − 7 = 1273 |

**The count: C2 binds 4 of the 157 operative rows (7 of 1256 cells) at the r98 base; 153 rows and
1249 cells stay presence-only.** The rows bound are `limine-pins` (3 cells: `RC-ENTRY-DEFAULT`,
`RC-SELFTEST-COUNT`, `RC-SCHEMA`), `limine-pin-battery-r96` (2: `RC-ROSTER-VERDICT`,
`RC-ROSTER-PINNED`), `check-r96-calibration` (1: `RC-CAL-SELFTEST`), `make-r96-bends` (1:
`RC-BEND-SPAN`).

The r98 capture change widens the *shape* match, not the row set: measured with the r97 capture
and with the r98 capture against the same table, the counts of rows carrying a bindable-shape cell
are **identical** (27 on the 160-row worktree table; 24 at `b3be3f90`, of which 4 are bound and 20
are unbound), because the comma form appears in no other row's cell. The r98 capture therefore
binds exactly the same four rows it did — **the C2 change is a freshness change on one cell's
accepted shape, not a widening of the bound row set.**

Receipt: `receipts/05-registry-coverage.txt`, `receipts/07-registry-row-counts.txt`.

---

## 5. Drift sweep

### 5a. `git grep -n "105/105" -- corpus SCORECARD.md LOG.md | wc -l`

**28** in the live worktree; **24** at the freeze commit `HEAD`. The 28 are: `LOG.md` (7),
`SCORECARD.md` (7), `corpus/knowledge/limine-bound-9digit-z-r97.md` (1),
`corpus/knowledge/limine-metadata-assertions-r98.md` (3),
`corpus/lessons/round-97-verifier-spotcheck.md` (5), `corpus/lessons/round-97.md` (2),
`corpus/lessons/round-35-verifier-spotcheck.md` (1), `corpus/lessons/round-71.md` (1),
`corpus/lessons/round-89-verifier-spotcheck.md` (1), `corpus/lessons/round-89.md` (1),
`corpus/lessons/round-90.md` (1). Every one is a *historical record of a past round's reading* —
none is a statement that the **current** instrument reads `105/105` on a lie.

The two r97 lesson lines are the ones the round's own subject names:

```
corpus/lessons/round-97.md:98:| C1 | era field lies while pins answer era B (`attack1-eraA-field`) | `w1/ReviewBattery/attack-1-field.txt` | **survives** `105/105` ×3 — the families never read `visibility_era` (A7 limit) |
corpus/lessons/round-97.md:99:| C1 | echo normalized for leading-zero members (`attack2-echo-norm`) | `w1/ReviewBattery/attack-2.txt` | **survives** `105/105` ×3 — the LZ family never reads the echo (A7 limit) |
```

Byte offsets (QUALITY 141 — measured on the bytes): `corpus/lessons/round-97.md` `105/105` at
**10319** and **10510**; `A7 limit` at **10378** and **10563**.

### 5b. `git grep -n "A7\|field-only\|echo" -- corpus/README.md corpus/lessons/round-97.md`

**19** lines in the live worktree; **12** at `HEAD`. The `A7` hits are `corpus/README.md:1232`
("the r97 A7 limit closed") and the two r97 lesson lines above; the rest are the `echo` word in
the round-95/96 Frontier prose and the new round-98 section.

### 5c. Does any r97 statement need a supersession pointer after this round?

**Yes — three statements, all of them statements about the *r97* battery that the round-98
instruments have now overtaken.** Nothing is edited by this seat; the pointers belong to whoever
files the round's documents.

| # | the statement (file:line, byte offset) | why it is now stale | pointer owed |
|---|---|---|---|
| 1 | `corpus/lessons/round-97.md:98` and `:99` — "**survives** `105/105` ×3 — the families never read `visibility_era` (A7 limit)" / "the LZ family never reads the echo (A7 limit)" (bytes 10319/10378 and 10510/10563) | these two attacks now **die** on the r98 battery — measured below: N07 `103/105` `failed_families [LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, N08 `104/105` `failed_families [LEADING-ZERO-NORMALIZE]` | a pointer from the r97 lesson's A7 lines to the r98 closure. `corpus/README.md` already carries it (`corpus/README.md:1232`, "the r97 A7 limit closed") and the r98 lesson names the A7 closure in its Frontier paragraph — but neither names the two r97 lesson *lines* as the carriers. QUALITY 108 asks the correction record to carry one `file:line` per carrier marked `corrected` / `standing as falsified record` / `historical evidence`; the r98 lesson carries **no companion map** (no `carrier` / `standing as` / `historical evidence` string anywhere in `corpus/lessons/round-98.md`). The r97 lesson lines are *historical evidence* of the r97 wave and should be marked as such, not edited. |
| 2 | `corpus/README.md:1138` — "The battery never reads `visibility_era`, and it compares the echoed `limine_version` only on AUTO cases (`auto_ok` short-circuits when `c.auto is None`); M06 (echo `99.9.9` for a `999999999.9.9` run) survives 99/99" (byte **130479**) | this is the **round-95** Frontier bullet. It was already superseded by round 96 (which added `EXPLICIT-VERSION-ECHO`/`-ERA` and named `M06` closed) and again by round 98 (which adds `check_echo`/`check_era` to the Z/LZ families). It is the last unreconciled carrier of the "the battery never reads `visibility_era`" proposition. | the round-96 and round-98 Frontier bullets state the newer state; the round-95 bullet is historical by the README's own convention ("Historical Frontier bullets … remain superseded by their explicit later entries, not silently rewritten" — `corpus/README.md:165`). **No edit needed; the pointer exists.** Recorded here so the reader knows the sweep was run. |
| 3 | `corpus/knowledge/limine-bound-9digit-z-r97.md:81` — "families are r98 candidates." (after the sentence "The two new families assert acceptance and the era's pin answer, not the JSON `visibility_era` field and not the echoed `limine_version`") | the candidates were **taken**: the r98 battery sets both flags on those two families. | the r98 knowledge entry `corpus/knowledge/limine-metadata-assertions-r98.md` states the closure in PC3 but **does not name its predecessor** — `grep -c "limine-bound-9digit-z-r97" corpus/knowledge/limine-metadata-assertions-r98.md` → **0**. A reader arriving at the r97 entry is told the work is "candidates"; a reader arriving at the r98 entry is not pointed back. A one-line cross-reference would close it. |

**Nothing else needs a pointer.** The `150 unbound rows` figure, the `150 rows` figure and the
`21 carry a bindable cell shape` figure are the subject of §6.

Receipt: `receipts/06-drift-sweep.txt`.

---

## 6. Findings — the numeric drift in a limit both the plan and the README still carry

**The `150 unbound rows` figure is stale in four places, and the r98 plan's own Limits section
freezes the stale number.**

The r97 README's Frontier measured the bindable surface at the **154-row** table the r97 freeze
carried: `154 − 4 = 150` rows left presence-only. The r98 base table is **157** rows, so the
figure is **153**; the worktree table (with the three r98 registry rows added) is **160** rows, so
**156** — and the r98 registry row for `check-registry-content-r98` already says "the other
**156** rows stay presence-only" (`SKILL.md:5946`), which is the *worktree* figure and is correct
there.

Carriers of the stale `150`:

| file | line | byte offset | the text |
|---|---|---|---|
| `.ufo/plans/round-98.md` | (Limits) | **1453** | "C2's 150 unbound rows and three measured gaps" (in the *Inputs read before this freeze* list, quoting the r97 README) |
| `.ufo/plans/round-98.md` | (Limits) | **9361** | "C2 binds the same 4 rows / 7 cells as r97. **The 150 unbound rows** and the three r97 measured gaps … stand unchanged." |
| `corpus/README.md` | 1251 (r98 Frontier) | **139562** | "Still open from r97: the C2 checker's **150 unbound rows** and its three measured gaps" |
| `corpus/lessons/round-97.md` | 111 | **11591** | "the C2 checker's **150 unbound rows** and its three measured gaps (A4)" |
| `SCORECARD.md` | 8013-ish | **1130379** | "C2's **150 unbound rows** and three measured gaps" (round-98 declaration inputs, quoting the r97 README) |

The plan's byte-9361 sentence is the load-bearing one: it asserts the figure **"stand[s]
unchanged"**. Measured, it did not stand unchanged — it moved from 150 (the r97 base's 154-row
table) to **153** at the r98 base (`b3be3f90`, 157 rows) and to **156** in the worktree (160 rows).
The three r97 registry rows the r97 round landed (`limine-pin-battery-r97`, `make-r97-bends`,
`check-registry-content`) are exactly the three rows that moved the number.

The r97 lesson's line 111 and the two plan/SCORECARD lines that *quote the r97 README's Frontier*
are correct as quotations — they say what the r97 Frontier said. The README's **round-98** Frontier
line 1251 is not a quotation: it is a fresh r98 statement of a still-open limit, and it carries the
stale number. That is the one that needs the pointer.

The plan's bytes are frozen (`e2f92347…`, manifest line 8) and the plan's own Amendment slot says
a narrowing is an append-only sidecar (`before/plan-amendments-r98.md`), never an in-place edit.
So the correction's home is the sidecar plus the round-98 README/lesson text — **not** the plan.

**The corrected figures, with the commands, all measured (not quoted):**

| quantity | at `f48d1642` (r97 base) | at `b3be3f90` (r98 base) | at the freeze commit `1cfeb5d5` | worktree |
|---|---|---|---|---|
| operative rows (r98 checker's own `operative_rows()`) | 154 | **157** | 157 | **160** |
| rows bound by `BINDINGS` | 4 | 4 | 4 | 4 |
| **rows left presence-only** | 150 | **153** | 153 | **156** |
| cells left presence-only (8 cells/row) | 1225 | **1249** | 1249 | 1273 |
| rows carrying a bindable-shape cell | 21 | 24 | 24 | 27 |
| of those, unbound | 17 | 20 | 20 | 23 |

**Second finding — a fresh drift surface the round has not named.** The r98 registry row for
`check-registry-content-r98` was added to the worktree, and the coverage gate reads it correctly.
But at the freeze commit `1cfeb5d5` the coverage gate **FAILS with 3 findings**, because the three
r98 tools landed in `tools/` without their registry rows:

```
$ python3 tools/check-registry-coverage.py --revision b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a
{"counts":{"findings":0,"missing":0,"registered":157,"rows_total":157,"tools_total":157},"findings":[],"revision":"b3be3f90…","status":"PASS"}

$ python3 tools/check-registry-coverage.py --revision 1cfeb5d5089097fdffef761ad0e2b8dfa75a2793
{"counts":{"findings":3,"missing":3,"registered":157,"rows_total":157,"tools_total":160},
 "findings":[{"id":"REGISTRY-ROW-MISSING","site":"tools/check-registry-content-r98.py"},
             {"id":"REGISTRY-ROW-MISSING","site":"tools/limine-pin-battery-r98.py"},
             {"id":"REGISTRY-ROW-MISSING","site":"tools/make-r98-bends.py"}],
 "revision":"1cfeb5d5…","status":"FAIL"}
```

The worktree `SKILL.md` (uncommitted when this seat ran) carries all three rows — `SKILL.md:5944`
`limine-pin-battery-r98`, `:5945` `make-r98-bends`, `:5946` `check-registry-content-r98` — and the
worktree table reads 160 rows / 4 bound / 156 unbound, so the gate will read PASS once those rows
land. **This is the r97 A1 defect recurring in the same shape** (r97's A1: "a post-freeze clone
carries the round's three tools without their rows, so the coverage gate's own FAIL masks the
blindness leg"), and the C2 kill rule depends on the coverage leg reading `PASS 157/157` on the
doctored revisions. The doctored fixture rides the base `b3be3f90` with the checker at `fixture/`,
so the base's `PASS 157/157` holds for the doctored legs — but **the round's own settle tip must
carry the three rows**, and until it does, the lane's own coverage gate is red. Recorded so the
L1 sees it before the settle.

**Third finding — the r98 battery's JSON schema tag still says `r97`.** `tools/limine-pin-battery-r98.py:2290`
emits `{"schema": "tsukuroi-limine-pin-battery-r97-v1", …}` — byte-identical to the r97 battery's
line 2270. Every receipt this seat produced reads `schema tsukuroi-limine-pin-battery-r97-v1` even
though the run was the r98 battery. The schema tag identifies the *battery's* JSON shape, which did
not change, so this is defensible — but a consumer that keys on the schema string cannot tell an
r98 run from an r97 run, and the claim's own counting command (`count-runs.py --family …`) reads
the JSON. Worth a note in the report, not a code change: the frozen bytes are what they are.

---

## 7. The claims' own targets, measured on this seat's run

Not the seat's item, but every measurement above is a receipt the L1 needs, and all are under this
seat's dir.

**Blindness (the r97 do-nothing battery on the r98 bends)** — the receipt the claim calls for:

```
$ python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py \
    --gate …/bends/N07-era-field-lie.py --runs 1 --work <scratch> --json OUT
families_passed 105/105 verdict met failed -
```

The r97 battery reads `met 105/105` on the N07 bend — it cannot see either lie. That is the
blindness receipt for the new assertion.

**The r98 battery on the two frozen bends** (one run each):

```
$ python3 tools/limine-pin-battery-r98.py --gate …/bends/N07-era-field-lie.py --runs 1 --work <scratch> --json OUT
families_total 105 families_passed 103 cases 420
verdict unmet
failed_families ['LEADING-ZERO-NORMALIZE', 'REFUSAL-VERSIONS-9DIGIT-Z']
non-null error rows: 0

$ python3 tools/limine-pin-battery-r98.py --gate …/bends/N08-echo-norm.py --runs 1 --work <scratch> --json OUT
families_total 105 families_passed 104 cases 420
verdict unmet
failed_families ['LEADING-ZERO-NORMALIZE']
non-null error rows: 0
```

Both match the claim's frozen targets exactly: N07 `103/105` with `failed_families` exactly
`["LEADING-ZERO-NORMALIZE", "REFUSAL-VERSIONS-9DIGIT-Z"]`, N08 `104/105` with `failed_families`
exactly `["LEADING-ZERO-NORMALIZE"]`, 0 error rows in each.

**C2's selftest tallies:**

```
$ python3 tools/check-registry-content-r98.py --selftest   ->  selftest PASS 14/14   (rc 0)
$ python3 tools/check-registry-content.py --selftest        ->  selftest PASS 12/12   (rc 0)   [the do-nothing control]
```

Receipts: `receipts/09-blindness-dn-r97-on-N07.txt`, `receipts/10-bend-legs.txt`,
`receipts/05-registry-coverage.txt`.

---

## 8. What this seat did not measure

- **Not run — time-bounded:** the per-cell re-derivation of all bindable-shape cells at the r98
  base `b3be3f90` (the seat's `derive_at.py` over the r98 checker and the r98-base table) was
  started and **cancelled** when the L1 called the seat to land. The r97-base equivalent
  (`154` rows, 21 shape rows, 11 unbound-machine-checkable) **did** complete and is in
  `receipts/` context; the r98-base per-cell derivation is therefore **not run** and no number is
  claimed from it. The r98-base *row counts* (157 / 4 bound / 153 unbound, 24 shape rows / 20
  unbound) are measured by the checker's own `operative_rows()` plus the capture regexes, which is
  a different and complete computation; only the *value re-derivation* (does each declared cell
  still match its tool's bytes?) is missing at that base.
- **Not run:** the doctored-fixture legs D1 / D2 / D2lie and the M08 mutant — those are the
  mutation-tester's and executors' items, and `build-doctored-fixture-r98.sh` writes into the
  lane's frozen fixture dirs.
- **Not run:** the landed-gate battery runs (105/105 ×3, canonical and clone) and the three-run
  repetitions of the bend legs — the executors' items; this seat ran one run per bend leg, which
  is enough to read the family sets and the error-row count, and is reported as one run, not three.
- **Not run:** `git clone --shared` fixture commits — no clone was needed for this seat's
  measurements, so no commit was made anywhere.

---

## 9. Receipt index (all under this seat's dir)

| receipt | what it holds |
|---|---|
| `receipts/01-hashes-and-manifest.txt` | the five live hashes + the 27-line manifest verification |
| `receipts/02-git-show-base.txt` | `git show b3be3f90:` and `git show HEAD:` for the five paths, plus the four control *sources* at the base |
| `receipts/03-diffs.txt` | both diffs in full + both numstats |
| `receipts/04-family-flags-and-counts.txt` | AST and runtime flag census on both batteries; the explicit-flag classification |
| `receipts/05-registry-coverage.txt` | operative-row counts by revision; r97 vs r98 capture comparison; both coverage-gate readings; both selftest tallies |
| `receipts/06-drift-sweep.txt` | both drift sweeps, byte offsets for every located quote, the r98 Frontier bullet verbatim from the bytes |
| `receipts/07-registry-row-counts.txt` | the three r98 registry rows; the unbound-row count at four revisions |
| `receipts/08-bends-rederived.txt` | the two bends re-derived in scratch and compared byte-for-byte with the frozen controls |
| `receipts/09-blindness-dn-r97-on-N07.txt` | the r97 do-nothing battery's `met 105/105` on N07 (the blindness receipt) |
| `receipts/10-bend-legs.txt` | the r98 battery's N07 and N08 readings (family sets + error-row counts) |
| `receipts/11-spelling-coverage-map.txt` | every version spelling the battery sends → the families asserting its echo and its era |
| `receipts/12-probe-bends-X-Y-gap.txt` | the seat's own two probe bends (in scratch, one clause each) and the r98 battery's readings on them — the measurement that separates the X-cap spelling (caught by `EXPLICIT-VERSION-ERA`) from the Y-cap spellings (uncertified) |

**Probe-bend note (an addition beyond the item, kept because it is already measured).** The seat
re-derived two one-clause era lies in its scratch (the frozen `make-r98-bends.py` was not run):
`X02` swaps the era label only when the first component has 9 digits and does not start with `0`
(so it targets exactly `999999999.9.9`), and `Y01` swaps it only when the second component has 9
digits and the third does not (so it targets exactly `12.999999999.4` and `0.999999999.0`). The
r98 battery reads `104/105 unmet [EXPLICIT-VERSION-ERA]` on X02 and `105/105 met` on Y01 — i.e.
the **X-cap spelling is covered** (by `EXPLICIT-VERSION-ERA`, which shares
`REFUSAL_DIGIT9`), and the **Y-cap spellings are the ones no family covers**. This sharpens
§4a: the uncertified explicit-spelling surface after r98 is exactly the two `REFUSAL-VERSIONS-9DIGIT-Y`
members. The L1's landing call arrived after these two runs completed; the runs were stopped there
and no further probe was started.

---

## 10. PASS/FAIL per expected line

| # | expected line | result | evidence |
|---|---|---|---|
| 1 | `tools/check-limine-pins.py` = `7d79ac29…` | **PASS** | `receipts/01`, `02` |
| 2 | `…/do-nothing-gate.py` = `7d79ac29…` | **PASS** | `receipts/01`, `02` |
| 3 | `…/do-nothing-battery-r97.py` = `e678c34f…` | **PASS** | `receipts/01`, `02` |
| 4 | `…/do-nothing-checker-r97.py` = `2daf5926…` | **PASS** | `receipts/01`, `02` |
| 5 | `tools/check-registry-coverage.py` = `6fcb2d0a…` | **PASS** | `receipts/01`, `02` |
| 6 | manifest `sha256sum -c` — all lines OK | **PASS** (27/27) | `receipts/01` |
| 7 | each of the five compared with `git show b3be3f90:<path>` | **PASS** for the two that exist at the base; the three control copies are absent there by construction and are compared against their *sources* at the base instead — **PASS** | `receipts/02` |
| 8 | r97→r98 battery diff: changed lines classified | **PASS** — 3 hunks; 4 executable lines (2 families × 2 flags), the rest header/docstring | `receipts/03` |
| 9 | r97→r98 checker diff: changed lines classified | **PASS** — 6 hunks; 1 executable capture line + 2 selftest cases + their fixture, the rest header/docstring | `receipts/03` |
| 10 | (a) r97 families that still set neither `check_echo` nor `check_era` | **PASS** — **96** of the 100 explicit-flag families (101 of the 105 roster); r97 was 98 of 100 | `receipts/04` |
| 11 | (b) how many of the 157 operative rows C2 binds | **PASS** — **4 rows / 7 cells**; 153 rows and 1249 cells presence-only at the r98 base | `receipts/05`, `07` |
| 12 | `git grep -n "105/105" -- corpus SCORECARD.md LOG.md \| wc -l` | **PASS** — 28 (worktree) / 24 (HEAD) | `receipts/06` |
| 13 | `git grep -n "A7\|field-only\|echo" -- corpus/README.md corpus/lessons/round-97.md` | **PASS** — 19 (worktree) / 12 (HEAD) | `receipts/06` |
| 14 | does any r97 statement need a supersession pointer | **PASS** — yes, **3** named (§5c), all pointers owed, none made by this seat | `receipts/06` |
| 15 | no file is edited | **PASS** — the seat wrote only under `.ufo/waves/round-98/w1/ScoutDrift/` and its scratch | `git status --porcelain` shows the lane's other changes, none of them this seat's |

**Files edited by this seat: none.** The only lane paths written are
`.ufo/waves/round-98/w1/ScoutDrift/report.md` and `.ufo/waves/round-98/w1/ScoutDrift/receipts/*`.

{"seat":"ScoutDrift","verdict":"findings","notes":"Freeze bytes verify: sha256sum -c of the 27-line manifest is 27/27 OK, and all five named files (gate 7d79ac29, do-nothing gate 7d79ac29, do-nothing battery e678c34f, do-nothing checker 2daf5926, coverage 6fcb2d0a) match the manifest byte-for-byte; the three control copies are absent at the pre-round base b3be3f90 by construction and match their sources there exactly. Diffs classified: battery r97->r98 = 3 hunks, 4 executable lines (check_echo+check_era on REFUSAL-VERSIONS-9DIGIT-Z and LEADING-ZERO-NORMALIZE at bytes 81743/82960) plus header and the A6/R97-D3 docstring correction (byte 82590), roster unchanged at 105; checker r97->r98 = 6 hunks, 1 executable capture regex (byte 12743) plus 2 selftest cases (bytes 21180/21223) and their fixture, BINDINGS unchanged at 7 cells over 4 rows. Limit (a): 96 of the 100 explicit-flag families still set neither flag (101 of the 105 roster; r97 was 98 of 100); sharper per-spelling map leaves exactly two uncertified spellings, 12.999999999.4 and 0.999999999.0 (the Y-cap members) - the X-cap 999999999.9.9 is covered by EXPLICIT-VERSION-ECHO/-ERA, and a one-clause probe bend on the X spelling reads 104/105 unmet [EXPLICIT-VERSION-ERA] while the same on the Y spellings reads 105/105 met. Limit (b): C2 binds 4 of 157 operative rows / 7 of 1256 cells; 153 rows and 1249 cells presence-only at b3be3f90. Drift sweep: 28 '105/105' carriers (24 at HEAD) and 19 'A7|field-only|echo' carriers (12 at HEAD); 3 r97 statements need a supersession pointer (round-97.md:98/99 A7 lines, README:1138 round-95 bullet already superseded, limine-bound-9digit-z-r97.md:81 'r98 candidates' with no back-pointer from the r98 entry). FINDINGS: (1) the '150 unbound rows' figure is stale in 4 places - it is 153 at the r98 base and 156 in the worktree, and the frozen plan's byte-9361 Limits sentence says it 'stands unchanged' when it moved with r97's 3 new registry rows; the round-98 README Frontier line 1251 is a fresh (not quoted) statement carrying the stale number. (2) the coverage gate reads FAIL 3 (REGISTRY-ROW-MISSING for the 3 r98 tools) at the freeze commit 1cfeb5d5 - the r97 A1 shape recurring - and the settle tip must carry the three rows; the worktree already has them. (3) the r98 battery still emits schema tsukuroi-limine-pin-battery-r97-v1. Bend legs measured: r98 battery on N07 = 103/105 unmet failed_families [LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z], on N08 = 104/105 unmet [LEADING-ZERO-NORMALIZE], 0 error rows each; the r97 do-nothing battery reads met 105/105 on N07 (blindness). r98 checker --selftest PASS 14/14 vs r97 control PASS 12/12. Not run (time-bounded, cancelled on the L1 landing call): the per-cell re-derivation of bindable cells at b3be3f90, so no value-level number is claimed from that base; the row counts there are from the checker's own operative_rows() plus the capture regexes."}
