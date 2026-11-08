# ScribeLesson — round-93 lesson blocks + QUALITY criteria (wave w1, seat ScribeLesson)

Seat: scribe. Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch `master`, jj-colocated).
Read-only on the lane: this seat edited **no** lane file except its own seat report
`.ufo/waves/round-93/w1/ScribeLesson.md` and its receipts under `.ufo/waves/round-93/w1/ScribeLesson/receipts/`.
No `git`/`jj` mutation was run in the lane; `git log/show/diff/status/ls-tree` only.
Scratch: `/fast/scratch/hyaku/tsukuroi-r93/ScribeLesson/` — removed on exit (see §7).
Receipts: `.ufo/waves/round-93/w1/ScribeLesson/receipts/`
(`01-number-check.txt`, `02-freeze-manifest-check.txt`, `03-count-runs-error-rows.txt`,
`04-probe-never-defaults.txt`, `05-routed-defects.txt`, `06-quality60-sweep.txt`,
`07-sweep-fixtures/`).

Freeze `c633f49aa512e1c8a0e0464b7fb5d354c70096cf`; the L1's land commit is
`b02384c705c2b5a65c02401f93b4bc871a402b13` ("round-93: land — era/refusal families, installed-version
probe, corpus and registry"). Tree state read 2026-11-08 03:05–03:40 local, across that landing:
criteria 136/137 are committed at the tip, `corpus/lessons/round-93.md` is still modified in the
working tree (uncommitted) at my last read.

---

## 1. Number check — 136 and 137 were free at seat start; the L1 took both mid-seat

At this seat's first read of `corpus/QUALITY.md`:

```
$ grep -nE '^(13[6-9])[.] ' corpus/QUALITY.md        # -> no match, rc 1
$ grep -oE '^[0-9]+\.' corpus/QUALITY.md | tr -d '.' | sort -n | uniq \
    | awk 'NR!=$1{print "GAP";g=1} END{if(!g) print "contiguous 1.."NR}'
contiguous 1..135
$ grep -oE '^[0-9]+\.' corpus/QUALITY.md | tr -d '.' | sort -n | uniq -d
(no output — no duplicate numbers)
```

So the numbers were contiguous `1..135`, no duplicates, and **136/137 were both free** at seat
start — the brief's premise ("assign 136/137 iff free") was correct when written.

During the seat the L1 landed two criteria (`corpus/QUALITY.md:336` and `:339`), both now committed
in the working tree:

| number | tag | subject |
|---|---|---|
| 136 | `R93-ROSTER-LIMIT-BY-NAME` | brief item 2(a) — a named limit a later round closes is listed by family name and closed by a family a committed bend kills |
| 137 | `R93-REFUSAL-CONTROL-NOT-SELF-CERTIFYING` | the round's own M2 class — a refusal-shaped control cannot certify a refusal family |

**Consequence for the brief.** Brief item 2(a) is landed as **136** — I review it in §2 rather than
re-draft it. Brief item 2(b), `R93-PROBE-NEVER-DEFAULTS`, is **not** landed: 137 was taken by the
M2 class. The next free number is **138** — `grep -c '^138\. ' corpus/QUALITY.md` → 0 in the working
tree and `git show b02384c7:corpus/QUALITY.md | grep -c '^138\. '` → 0 at the land commit; the
highest committed number is 137 and the sequence stays contiguous — so I draft 2(b) as **138** in §3.

Receipt: `receipts/01-number-check.txt`.

---

## 2. What the landed criteria say (review of 136 and 137)

`corpus/QUALITY.md:336` (136) — shape: bold title + tag, red, green, shown-able-to-fail,
`Lesson:` pointer. All four required parts are present. Its red leg names the r92 limits (three era
limits + `N04-accept-any`'s family-level survival, "A5/A7") and its green leg names the four r93
families and the bend that kills each. The brief asked the text to say "what the r92 A5/A7 limits
were and how r93's four families close three of them and N04" — the landed text says the three
families each close one era limit and `REFUSAL-VERSIONS` closes `N04`; the one-clause-per-family
mapping (which family closes *which* limit) is in the r93 plan's predicate and the report's
"Frontier rows advanced" bullet, not in the criterion paragraph. That is adequate; **no change
recommended**.

`corpus/QUALITY.md:339` (137) — same shape, red = the r92-gate do-nothing leg passing
`AUTO-PROBE-FAIL` 4/4, green = N06 + CriticForgers f3. Anchor `Lesson: corpus/lessons/round-93.md
Mistakes M2` — verified: the lesson's M2 exists and is exactly that class.

---

## 3. Drafted criterion 138 — `R93-PROBE-NEVER-DEFAULTS` (house shape, ready to paste)

The brief's item 2(b): *a version/era resolved by probing an external binary must fail rc 64 with
empty stdout when the probe fails, and its JSON must name the value and its source; a silent
fallback to a package default is the defect.*

```markdown
138. **A version resolved by probing an external binary is named with its source and never falls back to a default (R93-PROBE-NEVER-DEFAULTS):** when a tool resolves the version it acts on by running an installed binary (PATH lookup, read-only, bounded timeout), the resolution is reported with the value *and* its origin — the JSON names both the version and that it came from a `probe` — and a probe that fails (binary absent, non-zero exit, timeout, no parsable version) is a refusal with rc 64 and empty stdout, never a silent substitution of the packaged default; the default the tool falls back to when the probe fails is the defect, because a wrong era is then applied to a host whose bootloader was never read. **Red:** round 93's `N06-auto-fallback` bend (probe failure → `12.9.4`) answers with a verdict where a refusal was required, so `AUTO-PROBE-FAIL` reads `unmet` with the family in `failed_families` (`after/bend-N06-auto-fallback.json`, `unmet` ×3, 0 error rows); the same round's r92 gate, which refuses every `auto` value with rc 64, passes the same family 4/4 — a refusal-shaped answer and a defaulted answer are indistinguishable from the family alone, which is why the discriminating bend is named (`after/c2-donothing-r92-gate.json`, `94/96 unmet`, failed `AUTO-ERA-A,AUTO-ERA-B` only, 8 error rows). **Green, round 93:** the landed gate answers `--limine-version auto` from a read-only `limine --version` probe, and its live JSON names both the value and the origin — `limine_version 12.9.4`, `limine_version_source "probe"`, `visibility_era "pre-12.9.5"` (`after/live-c2.json`); a probe that fails produces rc 64 and **0 bytes** on stdout (measured by this seat with a failing `limine` first on `PATH` — transcript at `.ufo/waves/round-93/w1/ScribeLesson/receipts/04-probe-never-defaults.txt` and
`receipts/07-sweep-fixtures/probe-fail.{stdout,stderr}`; the L1 should land that transcript as a lane
receipt under `after/` so the criterion cites only lane paths). **Shown able to fail:** the
`AUTO-ERA-A`/`AUTO-ERA-B` families (a fake `limine` answering `12.9.4`/`12.9.6` on the case `PATH`)
are killed by `N05-auto-ignore` (`failed_families ['AUTO-ERA-B']` ×3) and by `N06-auto-fallback`
(`failed_families ['AUTO-PROBE-FAIL']` ×3), each with 0 error rows, so a gate that probes but ignores
the answer and a gate that falls back are two separate, individually visible failures. Lesson: `corpus/lessons/round-93.md` Mistakes `M2`; extends QUALITY 137 (a refusal-shaped control cannot certify a refusal family) with the instrument-side rule that a failed probe refuses rather than defaults.
```

Facts this draft rests on, all measured (receipt `04-probe-never-defaults.txt`):

* gate code, `tools/check-limine-pins.py:503-511` — `if version == "auto": probed =
  probe_limine_version(); if probed is None: … return 64` (the message goes to `stderr`, nothing to
  `stdout`); `:104-121` — the probe is `subprocess.run([executable, "--version"], …,
  timeout=5)`, PATH lookup by default, first `\d+\.\d+\.\d+` in stdout, `None` on non-zero exit /
  timeout / OSError / unparsable.
* live receipt `after/live-c2.json` → `limine_version 12.9.4`, `limine_version_source probe`,
  `visibility_era pre-12.9.5`, `verdict DEGRADED`, `rc 1`, findings `LP-MISMATCH line 30/38`.
* this seat's own probe-failure run: a `limine` that exits 1 first on `PATH` → **rc 64**,
  **stdout 0 bytes** (`receipts/04-probe-never-defaults.txt`).
* `after/bend-N05-auto-ignore.json` → `unmet`, `failed_families ['AUTO-ERA-B']`, ×3, 0 error rows;
  `after/bend-N06-auto-fallback.json` → `unmet`, `failed_families ['AUTO-PROBE-FAIL']`, ×3, 0 error
  rows (via the frozen `count-runs.py`).
* `after/c2-donothing-r92-gate.json` → `94/96 unmet`, failed `AUTO-ERA-A,AUTO-ERA-B`, **8 error
  rows**; `AUTO-PROBE-FAIL` passes there (the r92 gate refuses every `auto` value).

---

## 4. Drafted `## Mistakes` rows (from verified artifacts only; the L1 pastes the final evidence)

### M1 — the pre-freeze smoke run is a non-receipt (`landing`)

The lesson already carries this row (`corpus/lessons/round-93.md:47`). Two corrections this seat
recommends, both verified:

1. **The `captured-by` pointer does not resolve in the lane.** The row cites
   `PROTOCOL.md` for "the freeze-before-score rule". The lane has **no** `PROTOCOL.md`:
   `git ls-tree c633f49a --name-only` lists `AGENTS.md LOG.md MINT.md PROVINCE.md SCORECARD.md
   SHONEN.md SKILL.md considerthese corpus plans reports tools` — no `PROTOCOL.md`, and
   `git log --all -- PROTOCOL.md` is empty. The fleet-root file
   `/home/vgpnk/Projects/shokunin/PROTOCOL.md` (46 627 B) contains **no** freeze rule and no receipt
   rule: `grep -a -c -i 'freeze'` → 0, `grep -a -c -i 'receipt'` → 0 (it does carry "A lane report
   **lands last**" at line 117, the rule the r92 lesson cited). The rule that *is* in this lane, and
   in the freeze commit itself, is the round-93 declaration's own sentence — `SCORECARD.md:7776-7777`
   (frozen at `c633f49a`): *"Disclosure: the candidate was drafted alongside the battery; no score of
   it is a receipt. The landed gate is committed and scored only after this freeze."* The row's
   second half ("the r92 declaration's 'No score of it is a receipt'") resolves — that sentence is
   at the r92 declaration (`SCORECORD.md:7640-7642`) — but the `PROTOCOL.md` half does not.
   **Recommendation:** `captured-by` = the round-93 declaration disclosure sentence
   (`SCORECORD.md:7776-7777`, frozen at `c633f49a`) + QUALITY 114 (`R82-FROZEN-CONTROLS`: the
   instrument is committed "before any candidate file of the round is authored, run or scored") +
   QUALITY 73 (`R28-BATTERY-MEASURE`: "a run of uncommitted counter bytes is development output —
   disclosed as such, never offered as the measured value").
2. **No named amendment records the smoke.** The plan carries A1 (controls only), A2 and A3
   (claim-wording narrowings); none names the pre-freeze run. If the L1 wants the disclosure to be a
   frozen, citable fact rather than a lesson sentence, it belongs in an appended amendment
   (A4) naming it as instrument development. (Recommendation, not a required change — the disclosure
   in the frozen declaration already covers it.)

### M2 — `count-runs.py` counts a run with `error` rows as failed even when its verdict is `met`

**The statement is TRUE**, verified two ways (`receipts/03-count-runs-error-rows.txt`):

* code (`before/controls/count-runs.py`, frozen, sha `666eace6…`): `if r.get("verdict") != "met" or
  errors: ok = False` — the exit code is the conjunction *met ∧ zero error rows*, not *met*.
* a synthetic fixture (a run with `verdict: "met"`, `families_passed 96/96`, and one non-null
  `error` row) → the helper prints `"verdict": "met"` and exits **1**. Fixture retained at
  `receipts/07-sweep-fixtures/synth-error-rows.json`.

Two further measured facts that matter for how the L1 cites it:

* **The `--family` filter does not narrow the pass/fail.** With `--family ERA-EXACT-125` on the N01
  bend leg the helper still exits 1 (the run verdict is `unmet`); the filter only changes what is
  printed under `named` (`{'ERA-EXACT-125': [0, 4]}`). A receipt that reads "count-runs.py
  `--family X` exits 0/1" as a per-family verdict is misreading it.
* **Every receipt this round already cites is unaffected.** Landed-gate leg: `met`, 0 error rows,
  rc 0. Bend legs: `unmet`, 0 error rows, rc 1 (the intended reading). Do-nothing leg: `unmet`,
  8 error rows, rc 1. No cited reading changes.

**Answer to the brief's question — the L1 must NOT patch it before citing.** `count-runs.py` is
pinned by the freeze manifest (`666eace66ca27e34350c9878f8a681e02e2d143de6c62506dc28953bc38908e4`),
and both claims' kill rules read *"void if any instrument byte differs from
`.ufo/waves/round-93/before/freeze-manifest.sha256`"* — editing the frozen helper would trip the
void clause it is meant to measure. The correct fix is citation discipline, not a code change:
cite the JSON fields the helper already prints (`verdict`, `failed_families`, `error_rows`, and the
per-family `named` tally), never the exit code alone as "the family failed". If a separated exit
code is wanted for a receipt, it belongs in a copy under a seat directory, cited as such.

*(The lesson's own M2 is a different class — the refusal-shaped control — and is anchored by
criterion 137. This row is a separate finding; the L1 should number it after M4 or fold it into the
report's counting-command note.)*

---

## 5. Where the r92 spot-check's routed defects 1–5 land in the r93 report

Read from `corpus/lessons/round-92-verifier-spotcheck.md` §6; each carrier checked against the tree
(receipt `05-routed-defects.txt`).

| # | r92 routed defect | r93 carrier | state this seat measured |
|---|---|---|---|
| 1 | the r92 report's Landed-changes table stopped four commits short (`b5cb636a`, `98185b9b`, `1d1c7439`, `7793773a`) | the **r93 report's** `## Landed changes` table (`.ufo/reports/round-93/tsukuroi.md`, currently `TBD-LANDED`) names the four r92 commits; the r93 lesson M3 also carries the inheritance | the r92 report names none of the first three (`grep` on the r92 report → only `7793773a`, as its tip); the r93 report's routed-defects paragraph (line 67) names all four. **Not yet carried** — `## Landed changes` is still `TBD-LANDED`; that is where routed 1 must land |
| 2 | registry-coverage PASS cited at a revision with no receipt | `after/registry-coverage-tip.json` (re-run at the r93 tip) + the two `SKILL.md` registry rows for `limine-pin-battery-r93` and `make-r93-bends` | the tip receipt now exists and reads `status PASS`, `registered 147/147`, `revision b02384c7`; the freeze-revision receipt reads `FAIL` with exactly the 2 expected missing rows (`w1/ExecLints/registry-coverage.log`). **Carried** |
| 3 | S377's anchor named the `Python 3.14` docs line | a new appended registry row **S385** (version-pinned `3.15` URL, sha256 `d3c50306…`) plus the logged in-place anchor edit of S377, with the QUALITY-127 sweep receipts `after/q127-s377-pre.txt` and `after/q127-s377-landing.txt` | S385 present (`corpus/SOURCES.md:396`, `used-by` names the r92 entry, the r92 and r93 lessons); SOURCES 381 → **385** rows; the pre-leg receipt prints the old cell at the freeze revision. **One defect in the landing leg:** `q127-s377-landing.txt`'s first grep (`git grep -F "Python 3.14 docs"`) **exits 0**, because the appended S385 row quotes the superseded phrase in its `supersedes` cell — QUALITY 127 requires the landing leg to print nothing (rc 1). The second grep (S384 `print at raw 2029`) does exit 1. **Recommend** the L1 re-cut the landing leg so the phrase searched is the S377 *anchor cell* text (or the S377 row id), not a phrase the superseding row legitimately quotes |
| 4 | `claims.json` C2's frozen literal still reads `--usage-check met (8/8 cases)`; the reconciliation is A7 §5 | the r93 **plan** carries the pointer (`.ufo/plans/round-93.md:13` "the r92 `claims.json` A7 §5 pointer", and `:24` "r92 A5/A7"), and the r93 report restates it (routed-defects paragraph). The frozen r93 `claims.json` is not edited | the r92 `claims.json` still reads `usage-check met (8/8 cases)` (verified) and the r92 report cites `met 11/11`; the r93 plan names A7 §5. **Carried** |
| 5 | the r92 pre-A3 usage receipts (`after/c1-controls/usage-{canonical,clone}.json`, 8 cases each) must stay labelled pre-A3 and uncited | the r93 report says they stay labelled and are not cited for any r92 number | verified: both r92 files hold 8 `"version"` cases; the r92 report cites the 11-case seat receipts. **Carried** |

---

## 6. Findings for the canonical judge / L1 (read-only observations, no lane edit made)

1. **The freeze manifest check does not pass in the canonical tree — at the freeze *and* at the land
   commit — and the manifest pins a declaration.** `before/freeze-manifest.sha256` has **14** lines
   (the brief said 13 — see receipt `02`). `sha256sum -c` from the lane root prints 13 `OK` and
   **1 `FAILED: `.ufo/plans/round-93.md`** (exit 1), **both** in the working tree and at the lane tip
   `b02384c7` (receipt `06`). The manifest still pins the plan's *pre-amendment* digest `4600cfa3…`,
   while the plan as landed (amended by A1/A2/A3) hashes `70423d69…`; at the freeze commit the plan
   hashes `4600cfa3…`, so the line was correct when frozen and went stale with the first amendment.
   The r92 precedent is explicit: r92 amendment A8 dropped declarations from the manifest for exactly
   this reason ("Declaration files … are deliberately NOT in it: they were amended after the
   freeze"), and the r92 manifest indeed pins no `plans/round-92.md` and no `claims.json`. The r93
   manifest pins both.
   **Recommend** the L1 regenerate the r93 manifest in the r92 A8 instrument-only form (recording the
   manifest's own sha256) or, at minimum, cite the instrument lines (13) rather than the whole file
   when claiming "the manifest check passes" — the lesson's M1 "shown able to fail: the
   freeze-manifest check (`sha256sum -c`) passes on the exact bytes the receipts scored" is
   currently **false** as written, because of the plan line. The clone legs at the freeze commit
   legitimately read 14/14 `OK` (`w1/ExecReplicate/clone-identity.txt`).
2. **Number drift in a sibling seat report.** `w1/ExecReplicate.md` says `sha256sum -c … # 13/13 OK`
   and "the full 13-line manifest" (lines 23, 26, 100, 115), while the manifest has 14 lines and the
   seat's own `clone-identity.txt` prints 14 `OK` lines. `w1/ExecAutoReplicate.md` gets it right
   ("14/14 `OK` … the manifest file itself carries 14 lines, not 13"). The r92 lesson's precedent
   (ScribeLesson row) is to *record* such a mismatch rather than renumber; recommend the L1 cite the
   14-line form.
3. **The report's counting command should not read as a family-scoped verdict.** `count-runs.py`'s
   `--family` filter changes only the printed `named` tally; the pass/fail is over the whole run
   (§4). The report's "Counting command: the same battery invocation with the `count-runs.py`
   family filter" is accurate but easy to misread as "the exit code is that family's verdict".
4. **The QUALITY-60 (non-append) sweep prints exactly one removed line**, the S377 registry row
   (receipt `06-quality60-sweep.txt`): the anchor cell was edited in place *and* an S385 row
   appended. The r93 lesson should disclose that one removed line by name and the sweep command
   (`git diff -U0 <base> <REV> -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ |
   grep -E '^-[^-]'`), per QUALITY 60 as clarified in round 26 (record files, every consecutive
   commit pair). Neither the lesson nor the report currently carries that disclosure line.
5. **Lesson M4 (`curation`, S384 anchor coordinates) checks out.** `after/s384-line-receipt.txt`
   prints `nl -ba` of the pinned v12.9.5 `host/limine.c`: line 2029 is blank, 2031 is
   `puts(LIMINE_VERSION);`, 2035 is `puts("Limine " LIMINE_VERSION);`, 2089-2091 the `--version`
   dispatch — matching M4's corrected coordinates.
6. **Report placeholders still open** at filing time: `TBD-LANE-TIP`, `TBD-WAVE-SUMMARY`,
   `TBD-PREFILE`, `TBD-LANDED`, `TBD-MEASUREMENTS`, `TBD-SHONEN`, `TBD-PREFILE-LINE`. Routed 1 and
   the M1/M2 lesson rows land in those slots.
7. **The "SOURCES 381 → 385" figure is right but is not carried by the census receipt.** The row
   count checks out independently: 381 `S###` rows at the freeze commit, **385** at the land tip
   `b02384c7` and in the working tree (S382, S383, S384, S385 added) — and the report and the
   lesson both say `381 → 385`. But `after/census-after.txt` holds only the 57 warning rows
   (`W04`/`W01`/`ok`), **no row total**, so the cited census receipt does not by itself carry the
   number the report states. Recommend the L1 either re-run the census at the tip into a receipt
   that prints its row count, or cite the `S###` count command explicitly beside it, so the figure
   is re-derivable from the named receipt.

---

## 7. Scratch and cleanup

Scratch root `/fast/scratch/hyaku/tsukuroi-r93/ScribeLesson/` held the synthetic `count-runs.py`
fixture and the probe-failure stdout/stderr. The fixture and the probe-failure transcript were
copied into `receipts/07-sweep-fixtures/` and `receipts/04-probe-never-defaults.txt` **before**
removal; the scratch tree was then deleted, so no scratch tree is left behind.

---

## Verdict

**Both claims stand on the evidence I could check, and the round's QUALITY work is admissible as
landed — with seven corrections the L1 should make before filing.**

* C1 (depth 8) — the four new families exist and are killed by exactly one bend each:
  `ERA-EXACT-125` ← N01, `ERA-B-FIRST-BODY` ← N02, `ERA-B-U1` ← N03, `REFUSAL-VERSIONS` ← N04, each
  `unmet` ×3 in the canonical legs with the named family in `failed_families` and **0 error rows**;
  the landed gate reads `96/96 met` ×3 canonical (`after/c1-canonical.json`) and ×3 in a
  `git clone --shared` (`w1/ExecReplicate/c1-gate.json`), and the r92 do-nothing battery holds none
  of the four family names (`grep -c` = 0) while scoring the landed gate `89/89 met`.
  Receipts `03`, `05`.
* C2 (operability 9) — the probe is fail-closed with empty stdout (rc 64, 0 bytes on stdout,
  measured directly), the JSON names value *and* origin (`12.9.4` / `probe`), and the discriminating
  bends kill `AUTO-ERA-B` (N05) and `AUTO-PROBE-FAIL` (N06). Receipt `04`.
* **Criteria:** 136 = `R93-ROSTER-LIMIT-BY-NAME` (brief item 2(a)) — landed, shape complete, no
  change recommended. 137 = `R93-REFUSAL-CONTROL-NOT-SELF-CERTIFYING` — landed, anchors the
  lesson's M2. **Brief item 2(b) `R93-PROBE-NEVER-DEFAULTS` is not landed and takes the next free
  number, 138** (§3, ready to paste; 136/137 were free at seat start but the L1 took both mid-seat).
* **Corrections before filing:** (i) the freeze manifest pins `.ufo/plans/round-93.md`, which has
  been amended since the freeze, so `sha256sum -c` exits 1 in the canonical tree — regenerate it
  instrument-only per r92 A8, or cite the 13 instrument lines; the lesson's M1 "shown able to fail"
  currently rests on a check that fails (§6.1). (ii) lesson M1's `captured-by` cites `PROTOCOL.md`,
  which is not in this lane and whose fleet-root copy contains no freeze or receipt rule — point it
  at the frozen declaration sentence (`SCORECORDER.md:7776-7777`) plus QUALITY 114/73 (§4, M1).
  (iii) `count-runs.py` does treat error rows as failure (verified) — but it is manifest-pinned, so
  it must **not** be patched; cite its JSON fields rather than its exit code, and note that
  `--family` does not narrow the pass/fail (§4, M2). (iv) the QUALITY-127 landing leg for S377
  exits 0 because the appended S385 row quotes the superseded phrase; re-cut the search (§5, #3).
  (v) the r92 non-append disclosure sweep prints one removed line (the S377 row) that no round
  document lists yet (§6.4). (vi) `w1/ExecReplicate.md` says "13/13" where the manifest has 14 lines
  (§6.2). (vii) the "SOURCES 381 → 385" figure is correct but the cited census receipt carries no
  row total, so the number is not re-derivable from the receipt as named (§6.7).
