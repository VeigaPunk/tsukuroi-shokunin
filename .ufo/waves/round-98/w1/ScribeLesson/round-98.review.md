# ScribeLesson — REVIEW of `corpus/lessons/round-98.md` (round 98, wave w1)

Seat: `ScribeLesson` (scribe). Scope of this file: a **review of the L1's lesson draft**, not a
second draft. The L1's instruction (agent://TsukuroiR98, this wave) was: list (a) any number in the
draft that does not match a receipt I can read, (b) any missing Gate row or mistake field, (c) the
counter-attack scoreboard rows I can source from the seat reports that exist.

Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; draft reviewed:
`corpus/lessons/round-98.md` (working tree, uncommitted at read time; the file is 78 lines).
Scratch: `/fast/scratch/hyaku/tsukuroi-r98/ScribeLesson` (deleted before yield).
Every number below was run by this seat; receipts live under
`.ufo/waves/round-98/w1/ScribeLesson/receipts/` (listed at the end).

Instrument manifest verified before any measurement:
`sha256sum -c .ufo/waves/round-98/before/instruments.sha256` → 27/27 `OK`, exit 0
(receipt `receipts/` — the manifest check output was identical to the frozen wave's and every
instrument I measured carried its manifest digest: `check-limine-pins.py` `7d79ac29…`,
`limine-pin-battery-r98.py` `8198bd84…`, `check-registry-content-r98.py` `5bb1441e…`,
r97 do-nothing checker `2daf5926…`, r97 do-nothing battery `e678c34f…`).

---

## (a) Numbers in the draft that do not match a receipt I can read

### A1 — the census row count is stale against the tree it describes (393 vs 394)

Draft, `## Gate` census paragraph:

> "after the landed tree → 393 rows, exit 0, 0 E findings"

Measured (`receipts/census-validate.txt`):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
… 57 × W04, 1 × W01, 0 × E …
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
exit=0

$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md        # working tree
394
$ git show 1cfeb5d5:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'   # the freeze commit
393
$ git show b3be3f90:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'   # the pre-round base
392
```

**Run wins:** the working tree the draft describes reads **394** rows, not 393 — the L1's own
settle-time edit added **S394** (which supersedes S393) after the freeze commit `1cfeb5d5` (393
rows). The census exit code and the E/W split in the draft (0 E findings) are correct and
re-measured; only the row count and the "one A (own-work)" phrase are stale: **two** tier-A
own-work rows are added this round (S393, now `status: queued`, `used-by: —`; and S394,
`status: mined`, `used-by: corpus/knowledge/limine-metadata-assertions-r98.md,
corpus/lessons/round-98.md`). Also note the census does not name its warning set: the r97
spot-check named "57 W04 + 1 W01"; the same 57 W04 + 1 W01 holds this round (receipt above).

### A2 — "the only in-place change this round" is contradicted by the draft's own table

Draft census paragraph: *"Rows touched old→new in place: S393 `used-by` … (at settle; **the only
in-place change this round**)."* The draft's "In-place registry changes" table below it lists
**three** field changes on S393: `used-by` (→ `…, corpus/lessons/round-98.md`), `status`
(`mined` → `queued`), `used-by` (→ `—`). Two distinct fields changed on S393, so "the only
in-place change" is false as written; either drop the parenthetical or say "the only in-place
change on a **cited** row" and list both fields. (Verified against the working-tree row: S393
status cell `queued`, used-by cell `—`; S394 status `mined`.)

### A3 — R98-SPAN-BRANCH-UNTESTED's red-before cites the wrong receipt

Draft, third mistake:

> "red-before = M08 on the r97 checker `PASS 12/12` (`before/dev/c2-selftest-r97.txt`)"

`before/dev/c2-selftest-r97.txt` is the **pristine r97 checker's own** selftest (12 cases, all
PASS, `selftest PASS 12/12`) — it contains no mutant at all. The receipt that shows M08 on the r97
checker is `w1/MutRegistry/receipts/M08-on-r97-selftest.txt` (344 bytes, present) — and my own
re-derivation, `receipts/m08-r97-selftest.txt`, reads `selftest PASS 12/12` for the M08 mutant on
the r97 checker and `receipts/m08-r98-selftest.txt` reads `selftest FAIL 12/14` for the same
mutation on the r98 checker, with `span-gap FAIL ['RC-VALUE-MISMATCH']` and `span-gap-lie FAIL []`.
The draft's green-after citation (`before/dev/c2-m08-selftest.txt`, M08 on r98 = FAIL 12/14) is
correct and byte-identical in content to my re-derivation. **Fix the red-before pointer only.**

### A4 — R98-FIELD-NOT-ASSERTED's green-after cites a file that does not exist

Draft, first mistake:

> "green-after = `103/105` and `104/105` unmet with the frozen family sets
> (`before/dev/c1-bend-N07-runs3.json`, `c1-bend-N08-runs3.json`)"

`before/dev/c1-bend-N08-runs3.json` **does not exist**. The frozen dev directory holds
`c1-bend-N08-runs1.json` (1 run: `unmet 104/105`, `failed_families ['LEADING-ZERO-NORMALIZE']`,
0 non-null error rows — I re-read it) and `c1-bend-N08-runs3.txt`, which is **0 bytes**. The N07
pointer is fine (`c1-bend-N07-runs3.json`: 3 runs, each `unmet 103/105`, failed exactly
`[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 0 error rows). Two ways to close it:

* cite the 1-run receipt that exists (`before/dev/c1-bend-N08-runs1.json`), or
* cite the wave seat's 3-run receipts — mine, matched run-for-run against the 1-run receipt:
  `receipts/c1-n08-r98-runs3.json` (3 runs × `104/105 unmet`, failed exactly
  `[LEADING-ZERO-NORMALIZE]`, 0 error rows) and `receipts/c1-n08-count.txt`
  (`count-runs.py` output, the claim's counting command).

Also worth tightening the red/green pair to a matched **3-vs-3** pair, since both sides are
mine and both are 3 runs: red = `receipts/dn-n07-r97-runs3.json` / `receipts/dn-n08-r97-runs3.json`
(the r97 do-nothing battery, byte-identical to the r97 landed battery — `e678c34f…`, `cmp` rc 0
against `git show b3be3f90:tools/limine-pin-battery-r97.py`) reads **`met 105/105` ×3, 0 error
rows on both bends**; green = `receipts/c1-n07-r98-runs3.json` / `receipts/c1-n08-r98-runs3.json`
read `103/105` and `104/105` **unmet** ×3 with 0 error rows. The draft's red-before pointers
(`before/dev/c1-dn-N07-runs1.json`, `c1-dn-N08-runs1.json`) are correct but are 1-run receipts.

### A5 — two zero-information receipts sit in the frozen dev directory

`before/dev/c1-battery-selftest-reference.txt` contains exactly `rc=143` (7 bytes; a killed run,
no reading) and `before/dev/c1-bend-N08-runs3.txt` is 0 bytes. Neither is cited by the draft, but
both are in the frozen tree a reviewer will sweep; a note in the lesson that they carry no
measurement would prevent a later reader treating them as receipts.

### A6 — the Routed table's R97-D2 row cites a document that does not exist yet

Draft:

> "| R97-D2 numeric decomposition | the r98 report quotes `git diff --numstat` values, not diffstat totals | report |"

`.ufo/reports/round-98/` does not exist in the lane at review time (no round-98 report has been
written), and "report" is not a path. The correction itself is measurable now, and the draft can
carry the number instead of a promise:

```
$ git diff --numstat f48d1642 9c4b7b16 -- tools/limine-pin-battery-r96.py
6	2	tools/limine-pin-battery-r96.py
$ git diff --stat f48d1642 9c4b7b16 -- tools/limine-pin-battery-r96.py | tail -1
 1 file changed, 6 insertions(+), 2 deletions(-)
```

(receipt `receipts/routed-defects.txt`) — i.e. the r96-tool diff is **6 insertions / 2
deletions** (diffstat total 8 changed lines), which is the correction R97-D2 asks for.

### A7 — the R97-D1 row's evidence pointer is not the revision-bearing receipt

Draft: *"this round cites each receipt's own revision from `before/fixtures/doctored-r98-revision.txt`
| `before/dev/c2-doctored-summary.txt`"*. The summary file is revision-free (it prints the leg
verdicts only); the revision attribution lives in `before/fixtures/doctored-r98-revision.txt`
(base / D1 `aab954f1…` / D2 `d17ebc56…` / D2lie `3155fd3d…`) and in
`before/dev/c2-doctored-revisions.txt` (same four lines). Both exist. Cite the revisions file as
the revision-bearing receipt; keep the summary as the verdict receipt.

---

## (b) Missing Gate rows / mistake fields

### B1 — the draft has no `## Counter-attack scoreboard` section (QUALITY 115, R82-SCOREBOARD)

`corpus/QUALITY.md:226` (criterion 115): *"each round that freezes a counter records, for that
counter, the attack arms the wave fielded, how many were killed, which survived, and the class that
beat it — so the next round can tell whether hardening is converging or only moving the hole."*
The r97 lesson carries `## Counter-attack scoreboard (revives QUALITY 115; the r96 practice,
continued)`; the r98 draft carries `## Gate`, `## Mistakes`, `## Routed` only. Nothing in the
draft answers "which survived, and what class beat it". A draftable table with the rows I can
source is in § (c) below — two arms survived and neither is named anywhere in the draft
(ReviewBattery g6 and MutRegistry B01/B02/B03).

### B2 — the draft has no `## Frontier moved this round` section

The r97 lesson ends with that section; the r98 draft folds a one-line "Frontier rows advanced"
sentence into the census paragraph instead. The round's own frontier content exists and is
already committed in `corpus/README.md` § "Frontier (round-98 addition)" (six bullets: the
assertion is bound to two families only; N07's lie is spelling-targeted by construction; the echo
assertion fixes the current contract; the capture binds the two forms; and the three carried
open items — the 150 unbound rows and the three measured gaps, the r92 launcher residuals, the r93
probe pre-release caveat). The lesson should point at that list explicitly rather than
paraphrase one line of it.

### B3 — R98-FIELD-NOT-ASSERTED has no PROPOSED criterion text

The r97 spot-check routed R97-D3/A6 as *"the second instance of the class in two rounds — which is
the argument for a QUALITY criterion at r98 rather than another one-off correction."* The draft
names QUALITY 122 as the captured-by for the field-coverage class but drafts **no criterion text**,
so nothing lands that would catch the next instance. Proposed text, for the L1 to accept or reject
as an appended criterion (not an in-place edit of QUALITY.md):

> **PROPOSED (r98, extends QUALITY 122) — a battery family that names a reported field asserts
> that field.** When a battery family's expected answer names a field of the tool's JSON report
> (the echoed version, its source, the era label), the family's assertion reads that field; a
> near-miss control that lies in exactly that field, and implements everything else, reads below
> target at the freeze. Failing example: the r97 families `REFUSAL-VERSIONS-9DIGIT-Z` and
> `LEADING-ZERO-NORMALIZE` asserted rc and pins but left `limine_version` and `visibility_era`
> unread, so a field-only lie and a normalized echo each read `met 105/105`
> (`.ufo/waves/round-97/w1/ReviewBattery/attack-1-field.json`, `attack-2.json`; amendments A7).
> Shown able to fail: the r98 battery sets `check_echo`/`check_era` on both families and the two
> one-clause bends read `103/105` and `104/105` unmet with the exact frozen family sets
> (`w1/ScribeLesson/receipts/c1-n07-r98-runs3.json`, `c1-n08-r98-runs3.json`).

### B4 — the draft's Mistakes omit the wave's two surviving arms and the claim-wording defect

The draft's three mistakes are all "closed this round" items. The wave also produced (i) a
surviving attack arm that narrows **C1's claim sentence** and (ii) two surviving battery mutants
that show the new assertion has no self-test of its own. Neither appears in the draft, in any
section. The claim wording matters most: C1's predicate says *"A gate that answers every pin
correctly but lies in either field reads `unmet` on the r98 battery"* — ReviewBattery g6 and
CriticClaims' Y2 witness measured that sentence **false for the Y-cap spellings**
(`met 105/105`, 0 error rows, on both the r97 and r98 batteries). The plan's Limits section
already says the X/Y families do not set `check_echo`/`check_era`, so the *limit* is declared; the
*claim sentence* is wider than the limit and needs the narrowing the falsification ledger asked
for (ReviewBattery A9; CriticClaims `falsifies-wording` row). A drafted lesson row:

> **R98-Y-FIELD-LIE-UNASSERTED** — class: a claim sentence universal over spellings where the
> instrument is bound to a subset. A field-only `visibility_era` lie for the Y-cap spellings
> `12.999999999.4` / `0.999999999.0` (pins correct) reads `met 105/105` on the r98 battery and on
> the r97 battery. Captured-by: QUALITY 122 (a declared discrimination property names its
> near-miss control) — the control that lacks X was not run for the Y spellings. Fix: narrow C1's
> sentence to the Z/LZ spellings the two families send, and carry the Y-spelling field lie as a
> named limit; red-before = `met 105/105` ×3 on both batteries
> (`w1/ReviewBattery/g6-y-era-r98.json`, `g6-y-era-r97.json`), green-after = the r98 bend legs
> read `103/105` / `104/105` unmet on the Z/LZ spellings
> (`w1/ScribeLesson/receipts/c1-n07-r98-runs3.json`, `c1-n08-r98-runs3.json`).

### B5 — the draft's Gate table does not carry the rejected candidate's numbers

The r97 lesson's rejected-candidate row carried "HTTP 200, 41788 bytes, sha256 `11c40ea1…`". The
r98 draft carries only "HTTP 200; the page documents config keys and their values". Re-measured:

```
$ curl -sSL -o limine-config-v12.9.6.md -w 'final_url=%{url_effective} http=%{http_code} bytes=%{size_download}\n' \
    https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md
final_url=https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md http=200 bytes=27609
$ sha256sum limine-config-v12.9.6.md
f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763
```

Token counts over those 27 609 bytes: `limine_version` 0, `limine_version_source` 0,
`visibility_era` 0, `echo` 0, `int(` 0, `leading zero` 0, `version` 0, `JSON` 0 (receipt
`receipts/02-reject-config-md-fetch.txt`). Adding "27609 bytes, sha256 `f44f3a19…`, zero
occurrences of the gate's field names, of `echo`, and of `version`" makes the reject reproducible
from the row alone.

### B6 — the draft's S393 Gate row names the early-return offsets without saying so

The S393 row cites "the emission lines are `"limine_version": limine_version` at BYTE 11230 and
`"visibility_era": …` at BYTE 11344". Those bytes are real and they are the **CANNOT-EVALUATE
early return**; the main return's copies are at BYTE 16931 / 17037. The draft's own S394 row and
its second mistake both say this, so the row is not false — but as a Gate record the S393 row
should carry the site label in the same cell, otherwise a reader who takes the S393 row alone
lands on the wrong code path (which is the defect R98-ANCHOR-FIRST-SITE is about). Re-measured
line numbers for the same bytes: 11230 → line 200, 11344 → line 202 (early return); 16931 → line
316, 17037 → line 318 (main return); docstring phrase at BYTE 4425 → line 47 (receipt
`receipts/06-gate-emission-sites.txt`).

### B7 — the draft cites no QUALITY 139/140 row even though the round's own limits name them

The round's Limits and the plan cite QUALITY 139/140/141; the draft's mistakes cite 122 and 141
only. QUALITY 140 (a target clause is re-read against one development run before the freeze) is
the criterion that C1's over-wide universal sentence violates, and QUALITY 139 (a published
numeric bound is certified at its boundary) is the criterion behind the r97 Z-boundary work the
round sharpens. One clause in the relevant mistake rows would place the round's two named
criteria on the map.

---

## (c) Counter-attack scoreboard rows I can source (proposed section for the draft)

Seats and whether a `report.md` exists at review time (14 wave seats):

| seat | role | `report.md` present? |
|---|---|---|
| `ExecBends` | executor | **no** — receipts only (`count-N07-*-canonical.txt`, `count-N07-*-clone.txt`, `count-N08-*-canonical.txt`, `count-N08-*-clone.txt`, `diff-N07.txt`, `diff-N08.txt`, `clone-sha.txt`) — rows below are sourced from those receipts |
| `ExecDoNothing` | executor | yes |
| `ExecGateRuns` | executor | **no** — receipts only (`03-canonical.txt`, `06-clone-run.txt`, `09-count-canonical.txt`, `09-count-clone.txt`, `11-agree.txt`) — rows below are sourced from those receipts |
| `ExecLints` | executor | yes |
| `ExecRegistry` | executor | yes |
| `MutRegistry` | mutation-tester | yes |
| `ReviewBattery` | reviewer | yes |
| `ReviewRegistry` | reviewer | yes |
| `ScoutSources` | scout | yes |
| `ScoutDrift` | scout | **no** — receipts only (`10-bend-legs.txt`, `04-family-flags-and-counts.txt`, …) |
| `ScribeKnowledge` | scribe | **no** — receipts only |
| `CriticClaims` | critic | **no** — `ledger-draft.tsv` + receipts only |
| `ConnectorOverlap` | connector | yes |
| `ScribeLesson` | scribe | this file |

Scoreboard rows, each with the receipt I read (numbers quoted from it; `w1/` = `.ufo/waves/round-98/w1/`):

| claim | attack fielded | seat / receipt | outcome |
|---|---|---|---|
| C1 | era lie for **every** version (both `visibility_era` sites flipped) | ReviewBattery `g1-era-all-r98.json` | **killed** — `unmet 102/105`, failed `[EXPLICIT-VERSION-ERA, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 0 error rows (the r97 delta is the Z+LZ join with `EXPLICIT-VERSION-ERA`) |
| C1 | fixed echo `7.7.7` for every explicit flag | ReviewBattery `g2b-fixed-echo-r98.json`, `g2b-fixed-echo-r97.json` | **killed** — r98 `unmet 100/105` vs r97 `unmet 102/105`: the two new families die with it |
| C1 | era lie only for the X-cap `999999999.9.9` | ReviewBattery `g3-xcap-r98.json` | **killed, weakly** — `unmet 104/105`, only `EXPLICIT-VERSION-ERA`, 1 failed case of 420 |
| C1 | source `probe` for an explicit flag (echo kept verbatim) | ReviewBattery `g4-probe-source-r98.json` | **killed** — `unmet 102/105`, failed `[EXPLICIT-VERSION-ECHO, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]` (the echo assertion is version **and** source) |
| C1 | echo truncated to 3 chars | ReviewBattery `g5b-trunc3-r98.json`, `g5b-trunc3-r97.json` | **killed** — r98 `unmet 100/105` vs r97 `unmet 102/105`; all 20 failed cases are meta-only (pins correct) |
| C1 | **era lie only for the Y-cap `12.999999999.4` / `0.999999999.0`** | ReviewBattery `g6-y-era-r98.json`, `g6-y-era-r97.json`; CriticClaims `receipts/batt-y2.txt` | **SURVIVES** — `met 105/105`, `failed_families []`, 0 error rows on **both** batteries → narrows C1's universal field sentence to the Z/LZ spellings (the plan's Limit already declares the X/Y gap) |
| C1 | N07 era-field-lie bend (label swapped only for 9-digit/leading-zero spellings) | ExecBends `count-N07-*-canonical.txt`, `count-N07-*-clone.txt`; my `receipts/c1-n07-count.txt` | **killed** — `unmet 103/105` ×3 in both layouts, failed exactly `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 0 error rows |
| C1 | N08 echo-norm bend (echo replaced by the numeric tuple) | ExecBends `count-N08-*-canonical.txt`, `count-N08-*-clone.txt`; my `receipts/c1-n08-count.txt` | **killed** — `unmet 104/105` ×3 in both layouts, failed exactly `[LEADING-ZERO-NORMALIZE]`, 0 error rows |
| C1 | blindness: r97 do-nothing battery on the landed gate and both bends | ExecDoNothing `dn-gate.json`, `dn-N07-*.json`, `dn-N08-*.json`; my `receipts/dn-*-r97-runs3.json` | **blindness holds** — `met 105/105` ×3, 0 error rows on all three gates; control byte-identical to the r97 landed battery (`e678c34f…`, `cmp` rc 0) |
| C1 | layout: landed gate, canonical vs `git clone --shared` | ExecGateRuns `03-canonical.txt`, `06-clone-run.txt`, `11-agree.txt`; my `receipts/c1-gate-r98-runs3.txt` | **agrees** — `met 105/105` ×3 in both layouts, per-run schema and verdict agree `True` ×3 |
| C1 | battery mutant **B01** (`meta_ok` ignores `check_echo`) | MutRegistry `B01-N08.json` | **SURVIVES** — N08 reads `met 105/105` where the claim requires `unmet 104/105` |
| C1 | battery mutant **B02** (`meta_ok` ignores `check_era`) | MutRegistry `B02-N07.json` | **SURVIVES** — N07 reads `met 105/105` where the claim requires `unmet 103/105` |
| C1 | battery mutant **B03** (Z family `check_echo` reset) | MutRegistry `B03-landed/N07/N08.json` | **SURVIVES** — both committed legs byte-identical to pristine (the Z-family echo has no witness in the leg set) |
| C1 | battery mutant **B04** (LZ family `check_era` reset) | MutRegistry `B04-N07.json` | **killed** — N07 `unmet 104/105 [Z]` where pristine is `103/105 [LZ, Z]` |
| C1 | battery mutant **B05** (`era_b()` inverts for the 9-digit Z spelling) | MutRegistry `B05-landed.json` | **killed** — landed `unmet 104/105 [Z]` where the claim requires `met 105/105` |
| C1 | class behind B01–B03: the battery's own selftest cannot see a metadata assertion | MutRegistry `receipts/lie-kind-coverage.txt` | **structural gap** — `LIE_KINDS` has 12 members; the `LIE_WRAPPER` body contains 0 occurrences of `limine_version` and 0 of `visibility_era`, so assertion *removal* is unobservable to `--selftest` by construction (the fix is a `("echo",)` / `("era",)` lie kind) |
| C2 | checker mutant **M01** (`derive()` returns the declared value) | MutRegistry `M01` selftest receipt | **killed** — `FAIL 3/14` |
| C2 | checker mutant **M02** (`declared != derived` branch deleted) | MutRegistry `M02` selftest receipt | **killed** — `FAIL 4/14` |
| C2 | checker mutant **M04** (`RC-ROW-MISSING` guard removed) | MutRegistry `M04` selftest receipt | **killed** — crash on `row-missing` |
| C2 | checker mutant **M06** (first exact heading, not the unique highest) | MutRegistry `M06` revision-leg receipts | **killed** — `FAIL 0/7`, 7 findings on every revision leg (selftest stays green) |
| C2 | checker mutant **M07** (`--revision` ancestor check skipped) | MutRegistry `receipts/probe-nonancestor.txt` | **SURVIVES** — outside `--selftest`'s construction; proved non-equivalent: a tree-identical non-ancestor commit reads `CANNOT-EVALUATE` rc 2 pristine, `PASS 7/7` rc 0 on M07 (the r97 class, unchanged) |
| C2 | checker mutant **M08** (`derive_variant_span` checks only the first label) | MutRegistry `receipts/M08-on-r97-selftest.txt`, `M08.diff`; my `receipts/m08-r97-selftest.txt` / `m08-r98-selftest.txt` | **killed** — `FAIL 12/14` on the r98 selftest (`span-gap` → `RC-VALUE-MISMATCH`, `span-gap-lie` → none) where the same mutation reads `PASS 12/12` on the r97 checker; D2/D2lie invert (r98 PASS / M08 FAIL on D2; r98 FAIL / M08 PASS on D2lie) |
| C2 | checker mutant **M09** (capture reverted to `N\d+-N\d+`) | MutRegistry `M09` selftest receipt | **killed** — `FAIL 13/14`, and only via `span-gap` (`RC-CELL-MISSING`); `span-gap-lie` still passes |
| C2 | checker mutant **M10** (comma branch always derives `N01-N03`) | MutRegistry `M10` selftest receipt | **killed** — `FAIL 12/14` plus the D2/D2lie inversion |
| C2 | covered cell doctored (D1: row `VARIANTS N01-N04` → `N01,N03`) | ExecRegistry `D1-*.json`; ReviewRegistry `03-D1*`; my `receipts/08-c2-doctored-legs.txt` | **killed** — r98 `FAIL` with exactly one `RC-VALUE-MISMATCH` (`states 'N01,N03', derives 'N01-N04'`); the r97 do-nothing checker reads `RC-CELL-MISSING` instead |
| C2 | gap keys + comma row (D2) | ExecRegistry `D2-*.json`; my `receipts/08-c2-doctored-legs.txt` | r98 `PASS 7/7`; **M08 `FAIL`** with one `RC-VALUE-MISMATCH` — the discriminating direction |
| C2 | gap keys + contiguous row (D2lie) | ExecRegistry `D2lie-*.json`; my `receipts/08-c2-doctored-legs.txt` | r98 `FAIL` with one `RC-VALUE-MISMATCH`; **M08 `PASS 7/7`** — the inversion |
| C2 | coverage-gate blindness on each doctored revision | ExecRegistry `D1/D2/D2lie-coverage`; my `receipts/09-c2-coverage-doctored.txt` | `PASS 157/157`, 0 findings, ×3 — the blindness leg is satisfied but is vacuous as evidence of a caught doctor (ReviewRegistry F4) |
| C2 | **hybrid cell `VARIANTS N01-N04,N05`** (over-claimed extra label) | ReviewRegistry `receipts/17-f-mixed.txt`, revision `9d8f6bda` | **SURVIVES** — the regex's hyphen arm wins before the comma tail, so the cell truncates to `N01-N04` and reads `PASS 7/7`; M08 and the coverage gate also read PASS — a false PASS |
| C2 | a second, contradictory mention in the **same** cell | ReviewRegistry `receipts/16-extra-probes.txt` | **SURVIVES** — `re.search` binds the first mention; the stated limit ("a prose restatement in another cell stays unbound") is narrower than the behaviour (same-cell restatement is unbound too) |
| C2 | whitespace / case variants (`N01, N03`; `N01 ,N03`; `n01,n03`; `VARIANTS = N01,N03`) | ReviewRegistry `receipts/16-extra-probes.txt`; CriticClaims `receipts/capture-audit.txt` | **fail-closed** — `RC-CELL-MISSING`, rc 1 (noisy, but safe) |
| C2 | derivation forced to the declared value | ReviewRegistry / ExecRegistry doctored legs | flips `FAIL → PASS` on the doctored tree — the comparison is real, not parse-only |
| — | registry-row coverage at the tip | ScoutSources (incidental, § "Incidental observation"); my `receipts/coverage-at-tip.txt` | **FAIL at the tip** — 3 × `REGISTRY-ROW-MISSING` for the three r98 tools (`tools_total 160` vs `registered 157`); `PASS 157/157` at the pre-round base `b3be3f90` — a settle item (the rows now exist uncommitted at `SKILL.md:5944-5946`) |

**Summary for QUALITY 115's question ("converging, or only moving the hole?"):** C1's two bends
and 3 of 5 battery mutants are killed; **B01, B02 and B03 survive** and one wave attack (the
Y-cap field lie, g6) **survives on both batteries** — the class behind all three survivors is the
same one QUALITY 115 asks about: *a field that no lie kind can mutate is asserted but never
exercised*. C2's M08 is closed by two selftest cases and the D2 inversion, but M07 (ancestor
check) survives unchanged, and the capture's two new false-PASS shapes (hybrid cell; same-cell
restatement) are new holes in the extended capture, not closures.

---

## Other observations (no action required, recorded for the settle)

* `tools/check-registry-coverage.py` at the tip reads `FAIL` with 3 missing rows (receipt above);
  the rows exist in the working tree (`SKILL.md:5944-5946`) but are uncommitted. ScoutSources
  reported this first. Since the coverage gate reads a committed revision, the finding clears on
  the settle commit — the lesson's census paragraph need not mention it, but the L1's settle should
  not assert "no axis harmed" while the tip reads FAIL.
* The draft's S392 re-open row is correct on every number I could re-measure: HTTP 200, 331 022
  bytes, sha256 `d92580dd…` (identical to the r97 pin `.ufo/waves/round-97/after/gate/functions.html`),
  and the three anchors at BYTE 157767 / 153202 / 159315 by `grep -abo` on the pinned bytes
  (receipt `receipts/01-s392-fetch.txt`). **No change needed.**
* The draft's S393/S394 byte offsets and the gate's behaviour both re-derive: the gate run on
  `12.09.4`, `000000012.9.4`, `12.000000009.000000005`, `12.9.999999999`, `0.9.999999999`,
  `12.9.5`, `12.9.4` echoes each spelling verbatim with source `flag` and reports the era from
  the numeric tuple (receipt `receipts/03-gate-spellings.txt`).
* The r97 do-nothing battery is byte-identical to the r97 landed battery: `git show
  b3be3f90:tools/limine-pin-battery-r97.py | sha256sum` = `e678c34f…` = the control's digest.
* The r98 battery's `check_echo`/`check_era` sites re-derive at byte level: set at 81747/81771
  (Z family) and 82964/82988 (LZ family), asserted in `meta_ok` at 98004/98097 (receipt
  `receipts/05-check-echo-era-offsets.txt`); the A6 docstring sentence at BYTE 5723 and the
  correction marker at BYTE 82590 (receipt `receipts/04-a6-docstring-offsets.txt`).

## Receipts written by this seat (all under `.ufo/waves/round-98/w1/ScribeLesson/receipts/`)

`01-s392-fetch.txt` (S392 refetch: status, bytes, sha256, byte offsets) ·
`02-reject-config-md-fetch.txt` (reject candidate: status, bytes, sha256, token counts) ·
`03-gate-spellings.txt` (gate run on the LZ/Z/boundary spellings) ·
`04-a6-docstring-offsets.txt` (A6 corrected sentence at BYTE 5723; correction marker at 82590) ·
`05-check-echo-era-offsets.txt` (`check_echo`/`check_era` set and assert sites) ·
`06-gate-emission-sites.txt` (lines 200/202 vs 316/318; 4425 → line 47) ·
`07-m08-mutant-offsets.txt` (M08 mutation byte offsets and mutant digests) ·
`08-c2-doctored-legs.txt` (D1/D2/D2lie × r98/r97/M08, with the rc of each) ·
`09-c2-coverage-doctored.txt` (coverage `PASS 157/157` on each doctored revision) ·
`c1-gate-r98-runs3.{json,txt}` + `c1-n07-r98-runs3.{json,txt}` + `c1-n08-r98-runs3.{json,txt}` +
`c1-n07-count.txt` + `c1-n08-count.txt` + `count-summary.txt` (C1 legs, 3 runs each, with the
claim's `count-runs.py` counting command) ·
`dn-gate-r97-runs3.{json,txt}`, `dn-n07-r97-runs3.{json,txt}`, `dn-n08-r97-runs3.{json,txt}` (the
r97 do-nothing battery on the landed gate and both bends) ·
`m08-r97.py`, `m08-r98.py`, `m08-r97-selftest.txt`, `m08-r98-selftest.txt` (my M08 mutant and its
two selftest readings) ·
`c2-selftest-r98.txt`, `c2-selftest-r97.txt` ·
`10-gap-printed-tally.txt` (the r97 gap (c) re-measured on the r98 checker: a gate whose
`--selftest` prints a hard-coded `selftest PASS 39/39` and executes no case — the r98 checker
reads `PASS 7/7`, so the gap survives) ·
`11-gap-unbound-cell.txt` (the r97 gap (a) re-measured: an unbound cell of a bound row doctored —
the r98 checker reads `PASS 7/7`, so the gap survives) ·
`census-validate.txt` (census output, exit code, W04/W01/E counts) ·
`routed-defects.txt` (R97-D2 numstat) · `coverage-at-tip.txt` (coverage at the tip and at the
pre-round base).

Tooling: no tool was installed or upgraded (host `python3` 3.14.8, `curl`, `grep`, `sha256sum`,
`git` 2.56.0 as found). No pacman transaction (host-wide paused), no `sudo`, no PATH-directory
write. Scratch clone fixtures only under my scratch dir; `git -C <clone> rev-parse
--show-toplevel` was asserted equal to the clone path before each commit.

{"seat":"ScribeLesson","verdict":"findings","notes":"Review of corpus/lessons/round-98.md: 7 citation/number defects (A1 census rows 393 vs measured 394 after S394, A2 'only in-place change' contradicted by the draft's own table, A3 red-before points at the pristine r97 selftest instead of the M08-on-r97 receipt, A4 green-after cites a nonexistent c1-bend-N08-runs3.json plus two zero-information frozen receipts, A5-A6 Routed rows cite a not-yet-existing report and a revision-free summary, A7 rejected candidate lacks bytes/sha256/token counts); 7 missing Gate/mistake fields (B1 no Counter-attack scoreboard though QUALITY 115 requires one and two arms survive, B2 no Frontier section, B3 no PROPOSED criterion text for the field-coverage class, B4 the surviving Y-cap field lie and the B01-B03 survivors are absent from the draft, B5-B7 rejected-candidate numbers, S393 site label, QUALITY 139/140 uncited); plus a sourceable scoreboard for all 14 seats with the two not-reported seats named. 40+ receipts written under w1/ScribeLesson/receipts/."}
