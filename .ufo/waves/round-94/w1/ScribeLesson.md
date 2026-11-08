# ScribeLesson — round-94 lesson blocks + QUALITY criterion (wave w1, seat ScribeLesson)

Seat: scribe (axes: discernment). Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch
`master`, jj-colocated). Freeze `eb3b3e5150a63507a382003fa1a70039b190396b`; lane tip observed
`b6447374`. Read-only on the lane: this seat wrote **no** lane file except this report and the
receipts under `.ufo/waves/round-94/w1/ScribeLesson/receipts/`. No `git`/`jj` mutation was run in
the lane (`git log/show/diff/status/grep/cat-file/ls-tree` only). Scratch
`/fast/scratch/hyaku/tsukuroi-r94/ScribeLesson/` — deleted on exit (§7).

Receipts (all under `.ufo/waves/round-94/w1/ScribeLesson/receipts/`):
`01-quality-numbering.txt`, `02-boundary-measurements.txt`, `03-s385-pin.txt`,
`04-manifest-void-detector.txt`, `05-draft-probes.txt`.

---

## 0. What this seat found before drafting (the measurement that decides every draft below)

The seat was asked to draft three blocks. Two of the three ("the QUALITY 139 row", "the S385
rule-1 row", "the README round-94 Frontier section") already exist in the lane, and one of the
two Mistakes rows (M1) already exists. So the seat's job was not only to draft but to *check the
landed text against the instruments*, and to say where it differs. It differs in four measured
places; §5 lists them.

### 0.1 The nine-digit boundary member is not in the scored roster — only in the usage roster

This is the load-bearing fact for QUALITY 139, and it is not visible from the family roster.

```
$ grep -c '999999999' tools/limine-pin-battery-r94.py                       # -> 1
$ grep -c '999999999' .ufo/waves/round-94/before/controls/do-nothing-battery-r93.py   # -> 0
$ grep -c '1000000000' tools/limine-pin-battery-r94.py                      # -> 0
```

The single `999999999` in the r94 battery is on line 2278, inside `usage_check()`'s **usage
roster** (`("999999999.0.0", 0)`) — a different CLI mode (`--usage-check`) from the scored
family roster. The **family** roster (`REFUSAL_DIGIT10`, line 1638) holds four ten-digit values
and **no** nine-digit member at all. So the "largest value inside the bound" — the accepted
member `999999999.0.0` — is never sent by any scored family case; only the `--usage-check`
leg exercises it, and `--usage-check` is **not** in C1's counting command
(`--gate G --runs 3` then `count-runs.py`).

Measured consequence (`receipts/02-boundary-measurements.txt` §B):

| mutant copy (one clause bent in the gate) | r94 battery | `--usage-check` |
|---|---|---|
| `m13` — bound `<= 10` (the r93 survivor) | **unmet** 97/98, failed `REFUSAL-VERSIONS-10DIGIT` | unmet |
| `inside8` — bound `<= 8` (refuses the 9-digit member) | **met** 98/98 | **unmet** (`999999999.0.0` want 0 got 64) |
| `capvalue` — refuses by **value** (`int(p) <= 10**9`) not by digit count | **met** 98/98 | **met** |

`capvalue` is the sharpest one. It accepts `1000000000.0.0` (which the landed gate refuses, rc
64) because it caps by value rather than by digit count, and **no** r94 roster sends
`1000000000.0.0` — the plan itself names that value as the adversary ("the 10-digit `'1' +
'0'*9` = 1,000,000,000", plan line 21), but the battery's enumeration sends `1234567890`
instead. A gate that enforces the bound by value rather than by digit count passes the whole
r94 battery and its usage roster.

### 0.2 The bound's two legs are not both certified by the instrument the criterion names

QUALITY 139's rule text demands two legs: "the largest value inside the bound, which must be
ACCEPTED — and the smallest value outside it, which must be REFUSED". The landed Fix clause says
the ten-digit enumeration and the usage roster's `999999999.0.0` row supply them. That is
true, but the "smallest value outside it" is **1,000,000,000**, and the battery never sends it
— the ten-digit values it does send (`1234567890`, `0.1234567890`, `0.0.1234567890`,
`1234567890.1234567890.1234567890`) are all *larger* than 1,000,000,000 and all have the same
ten-digit length, so they cannot separate "refuses by length" from "refuses by value ≥ 1e9".
`receipts/02-boundary-measurements.txt` §D shows the landed gate refusing `1000000000.0.0`
(rc 64) while `capvalue` accepts it (rc 0) — and no scored row sees the difference.

### 0.3 The wrong-clause bend that scored `met` is reproducible, and it is not the shape clause

The landed lesson M1 says the first N01 attempt bent "version must be X.Y.Z" and scored `met`.
Measured (`receipts/02-boundary-measurements.txt` §B): a bend of the **shape** clause
(`len(parts) != 3` → `> 3`) reads **unmet** with `REFUSAL-VERSIONS` failing — the r93 roster
sends `12.9.5.1` and `12.9`, so the shape clause *is* observed. The bend that reads `met` is
the one that drops `p.isascii()` from the same `all(...)` expression (`wrongclause`): `met` 98/98,
0 error rows, because no roster row carries a non-ASCII digit. And `isdig` (dropping `p.isdigit()`)
also reads unmet via `REFUSAL-VERSIONS` (the roster sends `abc`).

So M1's "shown able to fail" is true as a class but its named example is the wrong clause: the
`isascii()` drop is the clause the roster does not observe. The maker's exact-once guard does
not catch it either — `make-r94-bends.py` counts *matches*, not *clauses*: a wrong-clause
substitution that matches exactly once is emitted happily (reproduced in
`receipts/05-draft-probes.txt` §C).

### 0.4 The r93 f6 leakage class does **not** survive the r94 battery — the Frontier bullet is stale

The r93 wave recorded f6 (a gate that reads `<cwd>/bin/limine`'s *source* instead of executing the
probe) as a **survivor**: `met` 96/96
(`.ufo/waves/round-93/w1/CriticForgers.md:80`). The round-94 README Frontier bullet 2
(`corpus/README.md:1114-1115`) carries that forward: the leakage "is disclosed in the battery
docstring (CriticForgers f6), **not closed**."

Measured with the **unmodified r93 forger file**
(`.ufo/waves/round-93/w1/CriticForgers/f6-gate.py`), unchanged
(`receipts/06-f6-leakage-closed.txt`):

* **control** — that forger file on the r93 battery: `met` **96/96**, `failed_families []`,
  reproducing the recorded survivor exactly (so neither the forger nor the r93 battery moved);
* **the same file on the r94 battery**: `unmet` **97/98**, failed `['AUTO-PROBE-SHAPES']`,
  **0 error rows**, reproduced on a second independent run.

The mechanism is exact: the r94 `AUTO-PROBE-SHAPES` fake's *source* still contains the literal
`Limine 12.9.6` (`tools/limine-pin-battery-r94.py:1916`), so the r93 f6 regex harvests `12.9.6`
from it and the forger answers a **verdict** where the family expects **rc 64** — the family fails
it. The r93 battery had no such family, hence the survivor.

So the leakage is **disclosed** in the r94 docstring (`:177-179`) *and* **closed** by the new
family. The Frontier bullet's "not closed" is false on the evidence.

(The seat's own `f6r94` copy — the r93 probe transplanted into the r94 gate — reads `unmet` 96/98
with 4 error rows in `ERA-DEFAULT`; that is an artefact of the transplant, since the r94 default is
`auto` and a source-reading probe cannot answer it. It is not the control, and the receipt says so.
The control is the unmodified r93 file above.)

### 0.5 Two landed citations do not resolve

- `corpus/lessons/round-94.md:50` cites `after/bend-N0{id,…}.json` — a literal placeholder
  with braces and an ellipsis, not a path; and `.ufo/waves/round-94/after/` **does not exist**
  in the lane (`ls` → no such directory). The real bend receipts are in the wave, not in
  `after/`.
- `corpus/lessons/round-94.md:72` names "the `shokunin/conf` tail". That string exists in no
  committed revision of the plan and nowhere in the lane at `eb3b3e51` except the lesson row
  itself (`git grep -c 'shokunin/conf' eb3b3e51 -- .` → only `corpus/lessons/round-94.md`). It
  is not a citation a reader can check.
- The `N.=M:` edit contract the landed M3 leans on is not a lane rule: the only copies in the
  fleet are in a sibling lane's frozen round-8 lesson copy
  (`kasegi-shokunin/.ufo/waves/round-25/.../corpus/lessons/round-8.md`). The tsukuroi lane has
  no such contract (`git grep -ln 'N\.=M' eb3b3e51 -- .` → only the round-94 lesson itself).

---

## 1. Draft A — the QUALITY 139 row (house shape, ready to paste)

The landed row is at `corpus/QUALITY.md:345-346`; its Lesson pointer is on line 346. Number 139 is
free-to-occupied correctly: the file's numbers are contiguous `1..139`, no duplicates
(`receipts/01-quality-numbering.txt`), so 139 is the next number after 138 and 140 is free.

**House shape note (from the same receipt).** Rows 130-135 carry `Red:` + `Green:` + `Shown able
to fail:`; 136-137 carry `Red:` (+`Green:`) with no shown-able-to-fail; 138 carries `Red:` +
`Shown able to fail:`; the landed 139 carries `Red:` + `Fix:` and **no** shown-able-to-fail clause.
`Fix:` occurs exactly once in the whole file (row 139); `Green:` occurs 9 times. The nearest
house precedent for a criterion that names a specific mutant family and its bend is 138
(`Red:` + `Shown able to fail:` + `Lesson:`), and 133/137 (`Red:`+`Green:`+`Lesson:`). The draft
below uses `Red:` + `Fix:` + `Shown able to fail:` + `Lesson:` — keeping the landed row's
`Fix:` label (it is the landed row's own word for that clause) and adding the shown-able-to-fail
leg the house uses for the rows that name a mutant and a bend.

```markdown
139. **A numeric bound the gate publishes is certified at its boundary, never only above it (R94-BOUND-CERTIFIED-ONLY-ABOVE):** when a gate's refusal rests on a published numeric bound (a digit count, a length, a component cap), the battery that certifies it sends the boundary member itself — the largest value inside the bound, which must be ACCEPTED — and the smallest value outside it, which must be REFUSED — and the usage roster names which of its rows are in-bound and which are out-of-bound; a roster that only ever sends values above the largest refused member (or only values far below the smallest accepted one) certifies nothing about where the boundary is. Red: round 93's `REFUSAL-VERSIONS` sent the 5000-digit value and never a ten-digit component, so MutEra M13 (`<= 10`) survived 96/96 — the nine-digit member that would have fixed the other side of the bound was never sent either. Fix: round 94's `REFUSAL-VERSIONS-10DIGIT` enumerates four ten-digit values and the usage roster's `999999999.0.0` accepted-boundary row certifies the 9-digit cap from inside. Shown able to fail: a copy of the landed gate whose refusal is capped by value instead of by digit count — `len(p) <= 9 or (len(p) <= 10 and int(p) <= 10**9)` — accepts `1000000000.0.0` (rc 0) where the landed gate refuses it (rc 64), and reads `met` 98/98 on the r94 battery with 0 error rows, because the ten-digit values the roster sends (`1234567890` and relatives) are all above 1,000,000,000 and so are refused by both rules; a battery that cannot separate a length rule from a value rule has not certified the boundary. Lesson: `corpus/lessons/round-94.md` Mistakes `M1`; extends QUALITY 133 (both legs) with the numeric-bound leg: a bound is two legs (accepted inside, refused outside), not one.
```

**Where this draft differs from the landed row.** The landed row is `corpus/QUALITY.md:345` and its
Lesson line `:346`. Two changes, both measured:

1. **The red clause's member name is corrected** ("never a nine-digit component" → "never a
   ten-digit component"). A nine-digit member does **not** discriminate M13: at the gate,
   `999999999.0.0` is accepted identically by the landed gate and by the M13 copy (rc 0, 763 bytes
   each), while the **ten-digit** member is what separates them (landed gate rc 64 / 0 bytes; M13
   copy rc 0 / 764 bytes). M13's survival is caused by the missing *outside*-boundary member;
   the missing *inside*-boundary member is a different gap (it is what lets a mutant that wrongly
   refuses nine digits pass — measured, the `inside8` copy reads `met` 98/98 on the family roster
   and `unmet` only under `--usage-check`). The draft names both, because the criterion's own rule
   text demands both legs.
2. **A `Shown able to fail:` leg is added**, naming a mutant copy that passes the whole battery,
   because the criterion's rule ("the smallest value outside it") is not exercised by the roster
   the instrument ships: `1000000000.0.0` — the value the plan itself names as the adversary
   (`.ufo/plans/round-94.md:21`) — is sent by no r94 roster line at all
   (`grep -c '1000000000' tools/limine-pin-battery-r94.py` → 0).

If the L1 prefers the landed text unchanged, the criterion is still true as written — it says the
battery *must* send the boundary member — and the new row's weight comes from naming the mutant
the round did **not** close.

---

## 2. Draft B — the S385 rule-1 row (for the round-94 lesson `## Gate`)

The r93 spot-check routed this defect (§6 item 2): S385 is a **new** row in r93 (it superseded
S377) and the r93 lesson's `## Gate` table carried only S382-S384, so S385 has no rule-1 record
anywhere. The round-94 lesson's Gate table already carries a row for it — at
`corpus/lessons/round-94.md:13-14`:

```
| S385 (r93 routed 2, rule-1 row now supplied) | https://docs.python.org/3.15/using/cmdline.html#cmdoption-P | A | "1. Command line and environment — Python 3.15.2 documentation" (title, fetched 2026-11-08, sha256 `d3c503060e…`) |
```

**This is correct and needs no change.** Rule 1 of `CORPUS.md` §SOURCES requires the URL, the
access date, and a ≤25-word quote with its location grounding `teaches`. The landed row has all
three: the version-pinned URL, `fetched 2026-11-08`, and a 9-word quote. Verified
(`receipts/03-s385-pin.txt`):

* the quote is the anchor S385's own registry row names (`corpus/SOURCES.md:396`: "title
  `1. Command line and environment — Python 3.15.2 documentation`"), read at raw line 20 of the
  pinned snapshot;
* the pinned copy's sha256 is `d3c503060ebf18e5a807ba35d8527cfde49f8322373b9111e5c26d657b658cf6`,
  byte-identical to the digest S385's anchor cell records;
* the pin carries `Python 3.15.2` twice and `Python 3.14` zero times — the superseded string is
  gone from the snapshot, which is what the row is for;
* the QUALITY-127 landing sweep for the superseded phrase is clean at HEAD
  (`git grep -F 'Python 3.14 docs' HEAD -- corpus SCORECORD.md LOG.md
  ':!corpus/lessons/*-verifier-spotcheck.md'` → rc 1, nothing printed).

One **addition** the L1 should make, and one **quibble**:

* **Addition.** The row sits in the Gate table but is *not* in the lesson's "Admitted" line: the
  lesson reads "Admitted: all three new rows" (naming S386-S388) while the table carries four
  rows. S385 is not a new r94 row — it is a r93 row whose rule-1 record is supplied here. The
  Gate section should say so in one clause, e.g. after the Admitted line: "S385 is a r93 row
  (it superseded S377); its rule-1 record is supplied here because the r93 spot-check routed
  that defect (§6 item 2) and no row cites it before this round."
* **Quibble (do not change without a decision).** The quote is the page **title**. It grounds
  S385's `teaches` cell — "the pinned snapshot and the live page both carry `Python 3.15.2`" —
  but not the other half of that cell, "the `-I`/`-P` quote is unchanged". The title is the
  right choice for a row whose subject is the version anchor; the `-P` sentence was already
  quoted for S377 in the r92 lesson and is unchanged byte-for-byte between the r92 pin
  (`.ufo/waves/round-92/before/src/python-3-cmdline.txt:241`) and the r94 pin (raw line 569) —
  including its typographic apostrophes (U+2019, not ASCII). If the L1 wants one row to ground
  both halves, the `-P` sentence is the byte-exact alternative:
  `"python script.py command line: Don’t prepend the script’s directory."` (9 words, raw line
  569 of the pin). **Recommendation: keep the title.** It is the anchor the registry row names,
  and a row that quotes one thing grounds one thing; the `-P` sentence's byte-identity is already
  recorded here.

---

## 3. Draft C — the two Mistakes rows (M1 and M3), house style

House style, from `corpus/lessons/round-93.md` M2 (the nearest analogue — a `calibration` class
found by measurement, with `Fix (shown able to fail):` inline):

```
- **M2 (`calibration`, self-found by the measured do-nothing leg) — a refusal-shaped control cannot
  certify a refusal family.** Class: `calibration`. <what was measured, with the receipt path>.
  Captured-by: none for this shape — <what would have caught it> ; this round adds QUALITY 137.
  Fix (shown able to fail): <the fix, and the receipt that shows it can fail>.
```

The landed round-94 lesson already carries M1 (`corpus/lessons/round-94.md:47-53`), M2 (`:55-65`)
and M3 (`:68-76`). The drafts below replace **M1** and **M3** only (M2 is out of this seat's
brief). Both keep the landed row's heading and class verbatim.

### 3.1 M1 — the wrong-clause bend (replaces `corpus/lessons/round-94.md:47-53`)

```markdown
- **M1 (`calibration`, self-found) — a bend written from the battery docstring read the wrong clause and
  scored `met`.** Class: `calibration`. The r93 battery's `REFUSAL-VERSIONS` docstring names the
  family by what it refuses (anything outside `X.Y.Z`), not by the digit-count clause the gate
  actually applies, so a bend written from that docstring edits a neighbouring clause of the same
  `all(...)` expression and the battery never sees the difference: a copy of the landed gate with
  `p.isascii()` dropped from `parse_limine_version`'s bound reads `met` 98/98 with 0 error rows,
  because no r94 roster row carries a non-ASCII digit. Captured-by: none for this shape — the
  make-bends rule counts *matches*, not *clauses*: a wrong-clause substitution that matches
  exactly once passes the exact-once guard and is emitted without complaint
  (`.ufo/waves/round-94/w1/ScribeLesson/receipts/05-draft-probes.txt` §B). This round adds
  QUALITY 139. Fix (shown able to fail): N01/N03 bend the `len(p) <= N` literal in
  `parse_limine_version`; each reads `unmet` 97/98 with `REFUSAL-VERSIONS-10DIGIT` in
  `failed_families` and 0 error rows
  (`.ufo/waves/round-94/w1/ExecBends/N01.json`, `N03.json`;
  `.ufo/waves/round-94/w1/ExecReplicate/N01-x3.json`, `N03-x3.json`), and the same two bends
  read `unmet` under the clone layout, so the family discriminates the digit-count clause from
  the shape clause and the ASCII clause that the roster does not observe.
```

Three measured corrections against the landed M1, all in `receipts/02-boundary-measurements.txt` §B:

| landed M1 says | measurement |
|---|---|
| "the first `N01` attempt bent 'version must be X.Y.Z' and scored `met`" | a **shape**-clause bend reads **unmet** (`REFUSAL-VERSIONS` fails: the roster sends `12.9.5.1` and `12.9`). The clause that reads `met` is the **`isascii()`** drop. |
| "a bend that matched zero times or the wrong clause reads `met` or a usage error in the battery receipt" | a zero-match substitution makes the maker **raise** (`matched 0 times, expected 1`, `make-r94-bends.py`), not read `met`; the wrong-clause bend reads `met` in the *battery* receipt, which is a different artefact from the maker's guard. |
| Fix cites `after/bend-N0{id,…}.json` | that path is a literal placeholder and `.ufo/waves/round-94/after/` does not exist; the real receipts are the wave files cited above. |

### 3.2 M3 — the mid-edit repair (replaces `corpus/lessons/round-94.md:68-76`)

```markdown
- **M3 (`curation`, self-found) — the plan's USER-guide sentence lost a draft word mid-edit.** Class:
  `curation`. A repair whose line range covered lines never re-read since the previous edit
  consumed a neighbouring clause and left a fragment; the paragraph was restored by re-reading it
  (`read :79-85`) and verifying with a full-file `grep -n` of the C2 clause words, which now
  names the exact flag-default line (`ap.add_argument("--limine-version", default="12.9.4")`) and
  the `pacman -Si limine` probe. Captured-by: none for this shape — the lane holds no edit-range
  contract of its own (the only `N.=M:` copies in the fleet are a sibling lane's frozen round-8
  lesson), so nothing obliged the range to be re-read whole. Fix (shown able to fail): the
  restored paragraph is greppable by its own clause words — `grep -c 'pacman -Si limine'
  .ufo/plans/round-94.md` reads 1 and `grep -c 'default="12.9.4"' .ufo/plans/round-94.md` reads 1
  — so a re-edit that drops either word is visible in one command, and the plan's own sha256 line
  in `.ufo/waves/round-94/before/freeze-manifest.sha256` binds the repaired bytes.
```

Two corrections against the landed M3:

* The landed row's *fix* cites the freeze manifest's plan digest as binding the repaired text.
  That is true **of the manifest as it now stands** but the manifest's plan line was rewritten
  after the freeze, in the same commit that amended the plan (§4 below). So "the frozen plan's
  sha256 binds it" is a weaker claim than it reads; the honest form is "the manifest's plan
  line binds the bytes as amended, and the freeze-time manifest no longer verifies" —
  see §4.
* The landed row cites "the `shokunin/conf` tail" as the consumed fragment. That string is in no
  committed revision of the plan and nowhere in the lane at `eb3b3e51` except the lesson row
  itself, so a reader cannot check it. The draft above names the *checkable* residue (the two
  greppable clause words) instead of the fragment.

---

## 4. Findings for the canonical judge / L1 (read-only observations; no lane edit made)

1. **The freeze manifest's void detector cannot fire on the two files it most needs to watch.**
   `.ufo/waves/round-94/before/freeze-manifest.sha256` and `…/instruments.sha256` were both
   rewritten in commit `a85796ac` ("wording amendment A2"), in the same commit that amended
   `.ufo/plans/round-94.md` and `.ufo/waves/round-94/claims.json`. The freeze-time manifest
   now **fails** against the current tree on exactly those two lines
   (`sha256sum -c` → 2 FAILED, rc 1) while the current manifest passes 12/12 — so "sha256sum -c
   verifies" now certifies only that the manifest was updated in step with the files it names.
   C1's kill rule says "void if any instrument byte differs from
   `.ufo/waves/round-94/before/instruments.sha256`", and `claims.json`'s line in that file was
   likewise rewritten (`ae50b0b2…` → `8615e03e…`), so the detector cannot fire on the claim
   file it exists to protect. The r92 precedent (A8) deliberately excluded declarations from the
   manifest for this reason. Full evidence: `receipts/04-manifest-void-detector.txt`.

2. **The C1 target's "N04 `failed_families` is non-empty" is measured false.** Three seats
   agree (ExecBends, ExecReplicate ×3 in a clone, and this seat's own independent `--runs 1`):
   `N04-stale-tree` reads `met` 98/98 with `failed_families []` and 0 error rows, in the
   canonical lane and in the clone, and still does under `LIM_STD_VERSION=12.9.6`. The bend is a
   single never-read assignment (`.ufo/waves/round-94/before/controls/bends/N04-stale-tree.py`,
   `make-r94-bends.py` line 11-12 says "never invoked: a decoy"), so no environment can move it.
   C1's kill rule ("unmet if any named bend does not read `unmet` in all three runs in both
   layouts") is therefore not met by the round as it stands. The r94 README Frontier section
   (draft D below) should say so plainly rather than list only the two closures.

3. **A mutant that enforces the digit cap by value passes the whole r94 battery** (`capvalue`,
   `receipts/02-boundary-measurements.txt` §B/§D): it accepts `1000000000.0.0` where the landed
   gate refuses it, and reads `met` 98/98 with 0 error rows, because no r94 roster row sends
   `1000000000.0.0`. The plan names that value as the adversary (line 21); the battery sends
   `1234567890`. This is the substance of the QUALITY-139 row drafted in §1 and of the
   Frontier bullet in §5.

4. **The plan's C1 predicate names four values the battery never sends.** Plan lines 42-44
   enumerate `12.9.-1`, `12.9.+1`, `+12.9.1`, `12.9.1#` as the ten-digit family's members;
   `grep -cF` for each returns **0** in both the r94 battery and the r93 do-nothing battery,
   and none of the four is ten-digit (their components are 1-2 digits). The battery's actual
   family members are `REFUSAL_DIGIT10` (`tools/limine-pin-battery-r94.py:1638`). The claim
   text in `claims.json` is correct ("four X.Y.Z-shaped values, each with one component of
   exactly ten digits"); the plan's parenthetical enumeration is the drifted copy. Note also
   that the fourth real member, `1234567890.1234567890.1234567890`, carries **three** ten-digit
   components, where `claims.json` says "each with one component of exactly ten digits" — the
   same wording looseness ExecReplicate §7 recorded.

5. **`corpus/lessons/round-94.md:50` and `:72` carry citations that do not resolve** — the
   `after/bend-N0{id,…}.json` placeholder (and `after/` does not exist) and the `shokunin/conf`
   fragment (in no committed revision). §3 gives the replacements.

6. **The r93 knowledge entry is now stale on the round-94 change.**
   `corpus/knowledge/limine-version-probe-r93.md:53-54` still says "The probe remains opt-in:
   `--limine-version` still defaults to `12.9.4`" — the default is `auto` since V4
   (`tools/check-limine-pins.py:503`), and `corpus/README.md:1092` still repeats the claim in the
   r93 Frontier bullet. The r94 entry (`corpus/knowledge/limine-auto-default-r94.md`) states the
   new default but nowhere retracts the old sentence. Per QUALITY 75/88 the correction carries a
   sweep receipt; at HEAD `git grep -F 'still defaults to' corpus/knowledge/` prints that one
   stale line only. This is a curation defect the L1 can close by an appended erratum.

7. **The r94 lesson's M1 "wrong clause" example is the wrong clause** (§0.3): the shape clause is
   observed by the roster (`12.9.5.1`, `12.9`); the unobserved clause is `p.isascii()`. The
   lesson as landed names the shape clause, so its "shown able to fail" leg points at a bend that
   would have been caught. The draft in §3.1 names the reproducing clause.

8. **The README's "leakage not closed" is stale — it is closed** (§0.4). The r93 f6 forger file,
   unchanged, scores `met` 96/96 on the r93 battery (reproducing the recorded survivor) and
   `unmet` 97/98 with `AUTO-PROBE-SHAPES` failing and 0 error rows on the r94 battery. The
   disclosure in the r94 battery docstring remains accurate; the Frontier bullet's "not closed"
   is not. Full control pair: `receipts/06-f6-leakage-closed.txt`.

9. **The QUALITY 139 red leg's nine-digit attribution is wrong** (§0.1). The red clause says the
   r93 roster "never [sent] a nine-digit component, so MutEra M13 (`<= 10`) survived 96/96". A
   nine-digit member does **not** discriminate M13 — measured at the gate, `999999999.0.0` is
   accepted identically by the landed gate and by the M13 copy (rc 0, 763 bytes each). The
   **ten-digit** member is what discriminates it (landed gate rc 64/0 bytes; M13 copy rc 0/764
   bytes). The red clause is about the wrong member: it names the inside-boundary member, while
   M13's survival is caused by the missing outside-boundary member. The fix leg is right — the
   ten-digit enumeration is what kills M13, and the r94 battery does kill it (my own M13 copy
   reads `unmet` 97/98, failed `REFUSAL-VERSIONS-10DIGIT`). So the criterion's *rule* and *fix*
   are sound; only the red clause's member name is off. The draft in §1 corrects it.

---

## 5. Draft D — the README round-94 Frontier section (3 bullets, each naming its evidence pointer)

The landed section is `corpus/README.md:1108-1117`. The house shape for a Frontier bullet
(`corpus/README.md` r92/r93 additions) is: one surface, what it now holds, and the evidence
pointer that shows it. The landed r94 bullets name the families and the bends but no receipt
path, and the first bullet omits N04's measured non-kill. Draft:

```markdown
### Frontier (round-94 addition)

- The ten-digit enumeration (`REFUSAL-VERSIONS-10DIGIT`) and the probe-shape family
  (`AUTO-PROBE-SHAPES`, the suffixed `12.9.6-rc1` answer the unanchored regex accepts) are the
  r93 survivors' closures, and each is killed by a one-clause bend (N01/N03, N02) at `unmet` with
  the family in `failed_families` and 0 error rows — `.ufo/waves/round-94/w1/ExecBends/N01.json`,
  `N02.json`, `N03.json`, and `ExecReplicate/N01-x3.json`, `N02-x3.json`, `N03-x3.json` (clone).
  The fourth bend, `N04-stale-tree`, is **not** a closure: it is one never-read assignment, so it
  reads `met` 98/98 with `failed_families []` in the canonical lane, in the clone ×3, and under
  `LIM_STD_VERSION=12.9.6` — `.ufo/waves/round-94/w1/ExecBends/N04.json`, `ExecReplicate/N04-x3.json`,
  `ExecReplicate/N04-env.json`; the C1 target's "N04 `failed_families` is non-empty" is unmet as
  the round stands.
- The 9-digit cap is now closed **only from above**, and the bound's smallest out-of-bound member
  is unsent: the r94 family roster carries four ten-digit values (`1234567890` and relatives) and
  no nine-digit member, so `999999999.0.0` is reached only by the separate `--usage-check` leg,
  and `1000000000.0.0` — the value the plan names as the adversary — is sent by no roster at all;
  a gate that caps the refusal by value instead of by digit count reads `met` 98/98 —
  `.ufo/waves/round-94/w1/ScribeLesson/receipts/02-boundary-measurements.txt` §B/§D.
- The `auto` default is now the gate's default: a host upgraded without the flag is judged by the
  probed binary's era, and the flag-free live JSON reads `limine_version` `12.9.4` with
  `limine_version_source` `probe` and era `pre-12.9.5` —
  `.ufo/waves/round-94/w1/ExecLive/flagfree-real.json`, `.ufo/waves/round-94/w1/ExecLints/03-live-noflag.txt`;
  the gate selftest reads `PASS 39/39` (`.ufo/waves/round-94/w1/ExecLints/01-gate-selftest.txt`).
  The r92 launcher residuals stay open; the r93 AUTO-fake literal leakage is disclosed in the
  battery docstring (`tools/limine-pin-battery-r94.py:177-179`) and is **now closed** — the r93
  forger that read `<cwd>/bin/limine`'s source scored `met` 96/96 on the r93 battery and reads
  `unmet` 97/98 on the r94 one (`AUTO-PROBE-SHAPES` failing, 0 error rows) —
  `.ufo/waves/round-94/w1/ScribeLesson/receipts/06-f6-leakage-closed.txt`.
```

Notes for the L1 on this section:

* The landed first bullet says "each is killed by a one-clause bend (N01/N03, N02)" — three
  bends for two families. The draft keeps that mapping and adds the fourth bend's measured
  non-kill, because a Frontier section that lists two closures and omits the third bend's
  measurement reads as a round with no open bend when it has one.
* The landed third bullet says "`999999999.0.0` (accepted) certifies the 9-digit cap from
  inside". That is true of the `--usage-check` roster only; the scored family roster never sends
  it. The draft says which roster carries it.
* The landed second bullet says the r93 AUTO-fake literal leakage is "not closed". **Measured,
  that is now false** (§0.4): the r93 forger scores `met` 96/96 on the r93 battery and
  `unmet` 97/98 on the r94 one. The draft states the closure and its control.
* The r93 Frontier bullets carry no receipt paths either; the draft's paths are the wave files
  that exist, so the section stays re-checkable from the tree.

---

## 6. Receipt paths the L1 should adopt

| claim / row | receipt path | what it shows |
|---|---|---|
| QUALITY 139 shown-able-to-fail leg | `.ufo/waves/round-94/w1/ScribeLesson/receipts/02-boundary-measurements.txt` §B, §C, §D | `capvalue` reads `met` 98/98 and `met` under `--usage-check`; the landed gate refuses `1000000000.0.0` (rc 64) |
| QUALITY 139 red leg (M13 killed) | `.ufo/waves/round-94/w1/ExecBends/N01.json`, `N03.json`; `ExecReplicate/N01-x3.json`, `N03-x3.json` | N01/N03 `unmet` 97/98, `REFUSAL-VERSIONS-10DIGIT` in `failed_families`, 0 error rows, canonical + clone ×3 |
| QUALITY 139 inside-bound leg | same receipt §C (`usage-inside8`) | `999999999.0.0` want 0 got 64 → the usage roster is the only leg that observes the inside member |
| S385 rule-1 row | `.ufo/waves/round-94/w1/ScribeLesson/receipts/03-s385-pin.txt` | pin sha256 `d3c503060e…` = the registry anchor; title quote at raw line 20; `Python 3.14` absent; QUALITY-127 landing sweep clean |
| M1 wrong-clause reproduction | `.ufo/waves/round-94/w1/ScribeLesson/receipts/02-boundary-measurements.txt` §B (`wrongclause`, `isdig`, `shapebend`) and `05-draft-probes.txt` §B/§C | `isascii()` drop → `met` 98/98; shape/isdigit bends → `unmet`; maker guard passes a wrong-clause substitution that matches once and raises on a zero-match one |
| M3 repair | `.ufo/waves/round-94/w1/ScribeLesson/receipts/01-quality-numbering.txt` (plan grep pair, §3.2 text) | `grep -c 'pacman -Si limine'` = 1, `grep -c 'default="12.9.4"'` = 1 in the plan |
| manifest / void detector | `.ufo/waves/round-94/w1/ScribeLesson/receipts/04-manifest-void-detector.txt` | current manifest 12/12 OK; freeze-time manifest 2 FAILED on the plan and claims.json; the claims.json digest was rewritten post-freeze |
| N04 non-kill (independent) | `.ufo/waves/round-94/w1/ScribeLesson/receipts/05-draft-probes.txt` §A | this seat's own `--runs 1`: `met` 98/98, `failed_families []`, 392 cases |
| Frontier bullet pointers | `.ufo/waves/round-94/w1/ExecBends/*.json`, `ExecReplicate/*.json`, `ExecLive/flagfree-real.json`, `ExecLints/01-gate-selftest.txt`, `03-live-noflag.txt` | the wave receipts the three bullets cite |
| f6 leakage closure (Frontier bullet 2) | `.ufo/waves/round-94/w1/ScribeLesson/receipts/06-f6-leakage-closed.txt` | the r93 f6 forger file reads `met` 96/96 on the r93 battery (control, reproducing the recorded survivor) and `unmet` 97/98 with `AUTO-PROBE-SHAPES` failing and 0 error rows on the r94 battery |
| probe digests + the raw battery JSONs | `.ufo/waves/round-94/w1/ScribeLesson/receipts/07-probe-digests.txt` and `receipts/probe-json/*.json` | the sha256 of every mutant gate copy that was scored, its one changed line, and the battery JSON each produced |

---

## 7. Scratch and cleanup

Scratch root `/fast/scratch/hyaku/tsukuroi-r94/ScribeLesson/` held the mutant gate copies
(`m13.py`, `inside8.py`, `capvalue.py`, `wrongclause.py`, `shapebend.py`, `isdig.py`,
`f6r94.py`), the two fake-limiter trees used to exercise `make-r94-bends.py` (one with a
wrong-clause substitution, one with a zero-match pattern), the battery run JSONs, and the scratch
conf/esp used for the direct gate probes. Every artefact the report cites was copied into
`receipts/` **before** removal; the scratch tree was then deleted, so no scratch tree is left
behind.

---

## Verdict

**Both claims stand on the evidence this seat could check, and the round's QUALITY work is
admissible as landed — with four corrections the L1 should make before filing, and one new
criterion the measurements support.**

* **C1 (depth 8) — the two new families exist and each is killed by a one-clause bend**, exactly
  as the target says: N01/N03 read `unmet` 97/98 with `REFUSAL-VERSIONS-10DIGIT` in
  `failed_families` and 0 error rows (canonical and clone ×3); N02 reads `unmet` with
  `AUTO-PROBE-SHAPES`; the landed gate reads `98/98 met` ×3 in the canonical lane and ×3 in a
  `git clone --shared`. **But C1's fourth named bend, N04, reads `met` 98/98 with
  `failed_families []` in every layout measured by three seats and by this seat**, so the frozen
  kill rule ("unmet if any named bend does not read `unmet`") is **not met as the round stands**,
  and the README Frontier section must say so.
* **C2 (operability 9) — the default is `auto` and the probe is fail-closed**: the flag-free
  live JSON reads `limine_version` `12.9.4` with `limine_version_source` `probe` and era
  `pre-12.9.5`, and the gate selftest reads `PASS 39/39`. The r93 knowledge entry
  (`limine-version-probe-r93.md:53-54`) and the r93 README Frontier bullet still assert the
  opposite default and need an appended erratum.
* **QUALITY 139**: the landed row is *true as written* (it says the battery **must** send the
  boundary member) but the round-94 instrument does not send the smallest value outside the
  bound, and a gate that caps the refusal by value rather than by digit count passes the whole
  battery — measured. The draft in §1 keeps the landed wording and adds the shown-able-to-fail
  leg that names that mutant.
* **Corrections to make before filing:** (i) rewrite the manifest lines for the plan and
  `claims.json` so the void detector can fire again, or drop declarations from it as r92's A8
  did (§4.1); (ii) state N04's measured non-kill in the README Frontier section (§4.2, §5);
  (iii) name the `isascii()` clause — not the shape clause — in the lesson's M1, and cite the
  wave receipt paths that exist instead of the `after/bend-N0{id,…}.json` placeholder and the
  uncheckable `shokunin/conf` fragment (§3, §4.5); (iv) retract the stale
  "still defaults to `12.9.4`" sentence in the r93 knowledge entry and README bullet (§4.6);
  (v) correct the README's "leakage not closed" — it **is** closed by `AUTO-PROBE-SHAPES`, with a
  control pair that reproduces the r93 survivor (§4.8, §5); (vi) correct the QUALITY 139 red
  clause's member name (§4.9).
* **Also for the L1:** the plan's C1 parenthetical names four ten-digit values the battery never
  sends, and `claims.json`'s "one component of exactly ten digits" is loose for the fourth
  member (§4.4).
* **One measured closure the round has not recorded:** the r93 f6 leakage class — a gate that
  reads the fake `limine`'s *source* instead of executing it — is killed by the r94 battery
  (`AUTO-PROBE-SHAPES` failing, 0 error rows), while the same forger file still reads `met` 96/96 on
  the r93 battery. The round's own README Frontier says the opposite.
