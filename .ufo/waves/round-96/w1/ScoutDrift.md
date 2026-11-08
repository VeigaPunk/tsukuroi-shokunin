# ScoutDrift — round 96 wave w1 (bounded planning data-walk + drift checks)

Seat: `ScoutDrift` (scout; axis **calibration**). Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Measured at HEAD `8fdb05e17596291acb92c19f4ad8db1699b4d1ac` ("round-96: S390 locator byte corrected …").
Receipts: `.ufo/waves/round-96/w1/ScoutDrift/` (`receipts.txt` is the consolidated run; `probe-output.txt`,
`p4-f4-blindspot.txt`, `p5-p6.txt`, `manifest-check.txt` are the individual probes; the `*.py` are the scripts
that produced them, copied from my scratch).
Tooling: `Python 3.14.8`, `git 2.56.0`. **No installs, no upgrades, no pacman transaction** (nothing was
needed; pacman is paused host-wide). Read-only git only (`git show`, `git log`, `git diff`, `git rev-parse`,
`sha256sum`, `grep`, `sed -n`). No file outside `.ufo/waves/round-96/w1/ScoutDrift/` was written.

**Verdict: findings.** The four mandated items are answered and each passes, but four drifts are recorded
below (D1–D4). D1 and D2 are calibration-axis defects in the landed tree; D3 is a docstring/code mismatch in a
frozen instrument (routed to r97 by `CriticClaims` F-4); D4 is a broken pointer in `corpus/README.md`.

---

## Item 1 — the C1/C2 sentences in `claims.json` vs the plan vs the frozen plan

**Expected: no difference. Observed: none. PASS.**

Script `cmp_claims.py` (receipt `cmp_claims.py`; output folded into `receipts.txt` §R2). It parses the plan's
`### C1 —` / `### C2 —` blocks into their four `**Predicate.** / **Target.** / **Kill rule.** /
**Counting command.**` sentences, normalises whitespace (`re.sub(r"\s+", " ", s).strip()`), and compares
against `claims.json`'s `predicate`/`target`/`kill`/`counting` fields.

```
== step 0: .ufo/plans/round-96.md vs .ufo/waves/round-96/before/plan-frozen.md ==
[IDENTICAL] whole file (normalised)
   raw byte equality: True

== step 1: claims.json vs plan ==
[IDENTICAL] C1.predicate   [IDENTICAL] C1.target   [IDENTICAL] C1.kill   [IDENTICAL] C1.counting
[IDENTICAL] C2.predicate   [IDENTICAL] C2.target   [IDENTICAL] C2.kill   [IDENTICAL] C2.counting

== step 1: claims.json vs frozen-plan ==
[IDENTICAL] (same eight)

== summary ==
NO DIFFERENCES: every C1/C2 sentence is byte-identical after whitespace normalisation.
```

Independent hash confirmation (`receipts.txt` §R3): `sha256(.ufo/plans/round-96.md)` =
`sha256(.ufo/waves/round-96/before/plan-frozen.md)` = `5d389241abc136b18d69d84e906fa5365bf826bd8943829e940be640f2780948`,
byte-identical — **the plan's bytes were never edited in place**, so the freeze manifest's plan line still
holds (`receipts.txt` §R1: `sha256sum -c .ufo/waves/round-96/before/instruments.sha256` → exit 0, **17 OK, 0 FAILED**).

The round's narrowings live in a **separate append-only file**, not in the plan's `## Amendment slot`
(`receipts.txt` §R4):

- `.ufo/waves/round-96/before/plan-amendments-A1-A2.md` exists and carries **5** amendment headings
  (`grep -c '^### A[0-9]'` → 5) — the **file name says "A1-A2" but the content runs A1–A5** (D2, below).
- The plan's own `## Amendment slot` holds **0** amendment headings (the plan bytes are still the frozen ones).
- The r95 precedent has no such file (`.ufo/waves/round-95/before/` holds `controls/ dev-runs/
  freeze-manifest.sha256 instruments.sha256 plan-frozen.md`; `grep -rn '^### A[0-9]'` over it and
  `.ufo/plans/round-95.md` → none).

**PASS per the expected line.** The frozen claim sentences and the frozen plan agree byte-for-byte.

---

## Item 2 — the r95 Frontier correction: is `EXTRA-COMPONENT` broadened, not first?

**Expected: the r96 declaration records it as broadened, not first. Observed: yes. PASS**, with one drift (D3).

The instructed grep (`receipts.txt` §R5):

```
1662:REFUSAL_VERSIONS = ("12.9", "12.9.5.1", "abc", "", " 12.9.5", "12.9.5 ", "+12.9.5", "12..5",
1663-                    "12.9.5-rc1", "9" * 5000 + ".0.0")
```

The **pre-r96 roster already sampled one four-component value**, `12.9.5.1` — identical line in the r95
battery at `:1643` (`receipts.txt` §R5 shows both). The lane's own r95 knowledge entry said so at the time
(`corpus/knowledge/limine-bound-9digit-r95.md:92`): *"The refusal roster does send `12.9.5.1` (battery `:1643`),
so a 'refusal-shape gap' wording would be stale."*

**The r95 README/R-frontier sentence that says otherwise** (quoted verbatim, `corpus/README.md` at HEAD,
round-95 Frontier, last bullet of that block):

> `- Still open from r94: the `12.9.6.1` extra-component shape (not sent at battery level); the r92`
> `  launcher residuals; r89's blanks-before-CRLF, ESP containment and empty labels.`

**The r96 family that broadens it** (`tools/limine-pin-battery-r96.py:1720`, `1780-1793`, receipt §R11):

> `EXTRA_COMPONENT_VALUES = ("12.9.6.1", "12.9.6.1.0", "12.9.6.99", "12.9.6.7")`
> `    """r96 C1 (the four-component shape the r95 Frontier lists as not sent at battery level): a`
> `    version with a fourth component — `12.9.6.1`, `12.9.6.1.0`, `12.9.6.99`, `12.9.6.7` — is outside`
> `    the gate's published `X.Y.Z` grammar and must be refused rc 64 with empty stdout; `12.9.6` is`
> `    the same-list positive control and must answer a verdict (rc 0 on the healthy fixture), so a`
> `    blanket refuser fails too. …"`

**Does the r96 declaration record it as broadened, not first? YES — three places, all measured:**

1. `.ufo/plans/round-96.md` → *Limits declared before data*: *"**`EXTRA-COMPONENT` broadens a class the r95
   roster sampled once (`12.9.5.1`)**; its bend is also killed by that pre-existing row, which this
   declaration records instead of claiming a first."*
2. `.ufo/waves/round-96/claims.json` C1.predicate: *"the second member is the pre-existing `12.9.5.1` row —
   the four-component class was sampled once before this round"*.
3. `.ufo/waves/round-96/before/plan-amendments-A1-A2.md` A4 narrows further, to a **twin**: *"**three** of them
   (`EXPLICIT-VERSION-ECHO`, `EXPLICIT-VERSION-ERA`, `REFUSAL-VERSIONS-9DIGIT-Y`) sample classes the r95 roster
   does not; `EXTRA-COMPONENT` re-answers the four-component refusal class the r95 roster already carries
   (`REFUSAL_VERSIONS` value `12.9.5.1`) and the r95 instrument's `--usage-check` mode already sends
   (`12.9.6.1`) … the round's measured discrimination delta is three families, not four."*

**PASS per the expected line.** The claim is broadened-not-first, recorded in the declaration, in
`claims.json`, and in the amendment file.

Corroboration of the roster arithmetic by my own parse (`receipts.txt` §R6):
`tools/limine-pin-battery-r95.py` roster = **99** (99 unique); `tools/limine-pin-battery-r96.py` roster =
**103** (103 unique), and all four new names are present in the r96 roster.

---

## Item 3 — `considerthese/2026-10-26.md`: every proposal, its status, and one selection

Read in full (`receipts.txt` §R10). The file is the tsukuroi lane's own copy, sha256
`6f49c88d95d5f072678dfdf8cc6f3cff21207e14396924fa4bf7d6d2afdac50b`. It ends with a section headed
**`## Self-improvement ideas (proposed only, not acted on)`** — that is the status line the file itself gives
every bullet, and it is the reason the plan's *"considerthese/2026-10-26.md (the newest proposal batch; the
assimilation item rides §2b)"* line exists. Five proposals, each with the same status line
("proposed only, not acted on" as of 2026-10-26) and its landing state as of this round:

| # | proposal (file line) | status line in the file | landed as | where |
|---|---|---|---|---|
| 1 | **Burst-aware reading** (L17) | proposed only, not acted on | **implemented** | `corpus/QUALITY.md:219` criterion 112; `corpus/lessons/round-46.md:97` |
| 2 | **Counter-attack scoreboard** (L18) | proposed only, not acted on | **implemented** | `corpus/QUALITY.md:226` criterion 115 (R82-SCOREBOARD); `SKILL.md:3833,3935,5603,6286`; `corpus/lessons/round-82.md:53` |
| 3 | **Seat-harm incident log** (L19) | proposed only, not acted on | **implemented** | `corpus/QUALITY.md:215` criterion 110 (R79-SEAT-HARM-LOG); `corpus/lessons/round-79.md`…`round-85.md` |
| 4 | **Downstream patch-offset check** (L20) | proposed only, not acted on | **partially implemented, still open** | `corpus/QUALITY.md:201` criterion 103 (R69-PATCH-OFFSET); `corpus/lessons/round-42.md:53`; open row at `corpus/README.md:844` |
| 5 | **Cross-note correction propagation map** (L21) | proposed only, not acted on | **implemented** | `corpus/QUALITY.md:211` criterion 108 (R75-CORRECTION-PROPAGATION); `corpus/lessons/round-43.md:83` |

**Selection (AT MOST ONE): the Counter-attack scoreboard (proposal 2)** — the only one that is still
*unimplemented as a practice* and that fits this round's claims.

- **Grounding (opened, quoted, dated).** `corpus/QUALITY.md:226`, criterion 115, verbatim: *"**A frozen counter
  carries a counter-attack scoreboard (R82-SCOREBOARD):** each round that freezes a counter records, for that
  counter, the attack arms the wave fielded, how many were killed, which survived, and the class that beat it —
  so the next round can tell whether hardening is converging or only moving the hole. Grounded in the operator
  reflection `considerthese/2026-10-26.md` (2026-10-26) and landed as the table in
  `corpus/lessons/round-82.md` § Counter-attack scoreboard."* The date the proposal names is **2026-10-26**; the
  criterion that adopted it is QUALITY 115 (r82). The proposal text itself (`considerthese/2026-10-26.md:18`):
  *"For each frozen counter, track how many attack arms the wave fielded, how many survived, and which class beat
  it (leak read, fixture literal, answer-key read)."* The ledger template it names is
  `corpus/lessons/round-82.md:53` §"Counter-attack scoreboard", whose table columns are exactly
  `Counter | Arms fielded | Killed / total | Survivors | Class that beat it`.
- **Why it is still unimplemented in this lane's practice.** Measured over every lesson r85–r95, the scoreboard
  section is **absent in all eleven** (`grep -ci scoreboard` → 0 for `round-85.md` … `round-95.md`,
  `receipts.txt` §R10) although QUALITY 115 requires it of *every* round that freezes a counter. The r96 lesson
  now carries one (`corpus/lessons/round-96.md` §"Counter-attack scoreboard (considerthese/2026-10-26.md, mined
  2026-11-08)"), with the measured arms: *"C1 fielded 4 one-clause bends + 8 mutants + 7 forgers: bends 4/4
  killed at their named families; mutants 5/8 killed (M06 Z-cap and M08 leading-zero survive — Frontier; M07
  `lower()` is equivalent); forgers 5/7 killed, F-E (label-boundary-only) and F-G (trailing-zero) survive —
  Frontier. C2 fielded 6 one-fault fixtures (all id-exact) plus 11 green-without-work probes (U1-U5, E1b-E4,
  atk-*), of which the first-match and provenance passes are named limits (A5)."*
- **It fits this round's claims:** C1 froze a counter (`tools/limine-pin-battery-r96.py`) and C2 froze another
  (`tools/check-r96-calibration.py`), and this wave fielded the arms it names.
- **Caveat on the selection's own wording (a finding, D1).** The r96 lesson at `59cbfe2f` called this proposal
  *"its first unimplemented item that fits this round's claims"* (`corpus/lessons/round-96.md:56`). That
  superlative is **false against the lane's own bytes**: QUALITY 115 adopted the scoreboard at r82 and the
  ledger has been carried in at least twelve lessons (`round-41,47,52,64,68,70,71,72,73,82,84` — measured by
  `grep -ln 'Counter-attack scoreboard' corpus/lessons/*.md`). The honest statement is "still **unimplemented in
  the r85–r95 practice**, re-instated this round", not "first unimplemented". The current HEAD
  (`8fdb05e1`) no longer carries the word "unimplemented" in the lesson (`grep -c unimplemented
  corpus/lessons/round-96.md` → 0), so this is already partly corrected — but the *record* that the criterion
  was adopted at r82 is what a reader needs, and the lesson's scoreboard paragraph does not say it.

---

## Item 4 — do the four new families' docstrings match their code?

**Three of four match. One does not (D3).** Read the functions and their helpers directly
(`receipts.txt` §R11; `tools/limine-pin-battery-r96.py:1745-1793`).

**`EXPLICIT-VERSION-ECHO` — matches.** Docstring: *"an explicit `--limine-version` — one per case: `12.9.4`,
`12.9.5`, `12.9.6`, `999999999.9.9` — must be ECHOED in the JSON's `limine_version` and named with source
`flag`."* Code: `c.check_echo = True`; `meta_ok` (`:2097`) asserts `got[8] == c.version and got[9] == "flag"`;
`EXPLICIT_VERSION_META = ("12.9.4", "12.9.5", "12.9.6", REFUSAL_DIGIT9)` where `REFUSAL_DIGIT9 = "9"*9 + ".9.9"`
= `999999999.9.9`; the case enumerator is `EXPLICIT_VERSION_META[c.index % len(…)]` with `CASES_PER_FAMILY = 4`
(`:1955`), so each of the four versions is sent once per family per run. **Matches.**

**`EXPLICIT-VERSION-ERA` — matches.** Docstring: *"the same four explicit versions must report
`visibility_era` selected from the WHOLE tuple — `pre-12.9.5` below the split, `12.9.5+` at or above."* Code:
`meta_ok` (`:2099`) asserts `got[10] == ("12.9.5+" if c.era_b() else "pre-12.9.5")`, and `Case.era_b()` (`:340`)
computes `tuple(int(p) for p in version.split(".")) >= (12, 9, 5)` — the **whole tuple**, matching the
docstring. My arithmetic probe (`probe-output.txt` §P1) confirms the battery's whole-tuple rule and the gate's
(`check()`: `era_b = version >= VISIBILITY_ERA_SPLIT`) agree on all four META versions. **Matches.**

**`EXTRA-COMPONENT` — matches its code.** Docstring: *"a version with a fourth component — `12.9.6.1`,
`12.9.6.1.0`, `12.9.6.99`, `12.9.6.7` — is outside the gate's published `X.Y.Z` grammar and must be refused
rc 64 with empty stdout; `12.9.6` is the same-list positive control and must answer a verdict (rc 0 on the
healthy fixture)".* Code: `c.usage = list(EXTRA_COMPONENT_VALUES) + ["12.9.6"]`, `c.usage_positive = {"12.9.6"}`;
`run_usage` (`:2121-2136`) requires a positive row to be rc 0 with parseable JSON and every other row to be
rc 64 with empty stdout. The list matches the docstring exactly, in order. **Matches.**
*Minor, worth noting but not a mismatch of code and docstring:* the docstring's phrase *"a version with a fourth
component"* describes `12.9.6.1.0`, which has **five** components (`receipts.txt` §R7: `12.9.6.1.0 components=5`).
The claim and the lesson both call the family "four four-component spellings" (`corpus/README.md:1171`), so the
lane's own prose repeats the same slip — but the **code sends exactly the four values the claim names**, and the
gate refuses all of them for the same reason (`parse_limine_version` requires `len(parts) == 3`). See D4.

**`REFUSAL-VERSIONS-9DIGIT-Y` — DOES NOT MATCH (D3).** Docstring: *"one that reads the era **from X alone**
answers era B for `0.999999999.0` and fails."* Code: `fam_refusal_versions_9digit_y` sets **no** era flag —
it sets `c.version` and calls `_era_first_line_panic(c, Y_DIGIT9[c.index % len(Y_DIGIT9)])`, so the era is
exercised only through the **pins** the fixture expects, never through the `visibility_era` string. And the
sentence is not satisfiable as written: for `0.999999999.0` the first component is `0`, so a rule that reads the
era from the first component alone yields **era A** (`pre-12.9.5`), not era B. My arithmetic probe
(`probe-output.txt` §P1) prints it: `Y_DIGIT9 v=0.999999999.0 whole=False -> pre-12.9.5 | X-only=False ->
pre-12.9.5 | Y-only=True -> 12.9.5+ | max-only=True` — the rule that answers **era B** for that value is a
*second*-component (Y-only) or max-component rule, not an X-only one. The sibling seat reached the same
conclusion by building the mutant (`w1/CriticClaims.md` F-4, receipt `w1/CriticClaims/receipts/era-reader-mutant.txt`):
*"An X-only era reader **passes the Y family** and is caught by the ERA family. The Y family does discriminate a
Y-only bound (F-5/C1-4), but not an era bug, and the docstring attributes to it a discrimination it does not
have."* The L1 has already routed this: `SCORECARD.md` Frontier records *"the r96 Y-family docstring's era claim
is false (an X-only era reader passes Y, fails ERA — CriticClaims F-4, routed to r97)"*.

**Verdict for item 4: 3 of 4 match; `REFUSAL-VERSIONS-9DIGIT-Y`'s era sentence is false (D3, already routed to
r97 by `CriticClaims` F-4; the frozen claim sentence is unaffected — it says only *"each accepted with its era's
own answer, never rc 64"*).**

---

## Findings (drift), with evidence

### D1 — the r96 lesson's "first unimplemented item" superlative is false against the lane's own bytes (calibration axis)

- **Claim made:** `corpus/lessons/round-96.md:56` at `59cbfe2f`: the scoreboard is *"its **first** unimplemented
  item that fits this round's claims"*.
- **Evidence against:** `corpus/QUALITY.md:226` (criterion 115, R82-SCOREBOARD) adopted this exact proposal and
  names it; the ledger exists in `corpus/lessons/round-82.md:53` and in ≥11 other lessons
  (`round-41,47,52,64,68,70,71,72,73,82,84`). The honest residual is *"implemented as a criterion, but not
  practised in r85–r95"* (measured: 0 scoreboard mentions in each of `round-85.md`…`round-95.md`).
- **Status:** HEAD `8fdb05e1` has already dropped the word "unimplemented" from the lesson
  (`grep -c unimplemented corpus/lessons/round-96.md` → 0), so the literal superlative is gone from the landed
  tree. **The lesson still does not say the criterion was adopted at r82**, which is what makes the practice
  look new. Carry to r97 as a one-line addition; no byte here contradicts a frozen claim.

### D2 — the round's amendment file is misnamed and sits outside the plan's declared slot (calibration axis)

- **Evidence:** `.ufo/waves/round-96/before/plan-amendments-A1-A2.md` holds **5** amendment headings
  (`grep -c '^### A[0-9]'` → 5: A1, A2, A3, A4, A5) while its name says "A1-A2". The plan's own
  `## Amendment slot` — which states *"Amendments are appended here (A1, A2, …) with the datum that forced them,
  exactly as in rounds 92-95"* — holds **0**, because the plan bytes are still the frozen ones
  (sha `5d389241…` = `before/plan-frozen.md`). The r95 precedent has no such file at all.
- **Why it matters:** the plan promises the amendments live in the plan's slot; a reader following that promise
  finds an empty slot, and a reader following the filename finds A1–A2 and misses A3–A5 (A4 is the amendment
  that turns the round's headline "four families beyond the r95 roster" into "three families" — the one a
  closure reader most needs). Recommend the L1 note the file's real name and range in the SCORECARD row, or
  rename it in a later commit (it is inside `before/`, so **I did not touch it** — that directory is frozen).

### D3 — `REFUSAL-VERSIONS-9DIGIT-Y`'s docstring names an era rule the family does not test (already routed to r97)

See item 4 above. Evidence: `tools/limine-pin-battery-r96.py:1770-1778` (docstring) vs `:1777` (code sets no era
flag) and `probe-output.txt` §P1 (`X-only=False -> pre-12.9.5` for `0.999999999.0`, where the docstring claims
era B). The battery is frozen by `instruments.sha256` (`f06d90ae…`), so **the fix belongs to r97**, matching
`SCORECARD.md`'s Frontier row and `w1/CriticClaims.md` F-4. No frozen claim sentence is affected.

### D4 — `corpus/README.md:844` points at a proposal number that does not exist in this lane's copy

- **Evidence:** `corpus/README.md:844` reads *"- Patch-offset host-build check (considerthese/2026-10-26.md **#22**,
  partial): needs a host-build measurement outside the frozen legs."* The lane's own
  `considerthese/2026-10-26.md` (sha256 `6f49c88d…`) has **3** numbered lines (the "Three most important gains")
  and **5** unnumbered `## Self-improvement ideas` bullets; there is **no item 22** (`grep -cE '^[0-9]+\. '` → 3;
  `"22." in text` → False; `p5-p6.txt` §P6). A scan of **every** lane's `considerthese/2026-10-26.md` under
  `/home/vgpnk/Projects/shokunin/*/` found **no** copy with a `22.` item either. So the pointer does not resolve
  anywhere in the fleet. The row's substance (a still-open patch-offset measurement) is real and matches
  QUALITY 103; only the locator is broken. This is a stale cross-reference of exactly the class the round's own
  QUALITY 108 (R75-CORRECTION-PROPAGATION) governs.

### (not a finding, recorded for the closure) — two landed corpus sentences disagree on "once" vs "twice"

`corpus/README.md:1164` at HEAD reads *"the class reached the r95 instrument **twice** (the roster's `12.9.5.1`
row and the `--usage-check` value …)"*, and `corpus/knowledge/limine-bound-per-component-r96.md:42` reads *"The
class **was** sampled before this round — **twice**"*. Both agree, and both agree with the frozen plan's narrower
*"broadens a class the r95 roster sampled **once** (`12.9.5.1`)"* (which scopes "once" to the **roster**, the
other two to the **instrument**). Consistent under each reading; flagged only so a closure reader does not read
the plan's "once" as contradicting the corpus's "twice".

---

## Instrument drift checks (item: drift)

- **Freeze manifest holds.** `sha256sum -c .ufo/waves/round-96/before/instruments.sha256` → exit 0, **17 OK, 0
  FAILED** (`manifest-check.txt`, `receipts.txt` §R1) at HEAD `8fdb05e1`.
- **The C2 checker's mid-round byte drift is closed.** At `07:54` the working tree carried
  `ad894667…` (a whitespace-flattening edit) against the manifest's `7ff63524…`; at HEAD the working bytes are
  `7ff63524…` again (the L1 restored them; recorded as A2 in the amendments file). My own
  `sha256sum tools/check-r96-calibration.py` = `7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4`
  = the manifest line. **No drift now.**
- **The frozen checker's F4 clause 2 has a newline-wrap blind spot** (`p4-f4-blindspot.txt`, `p4_f4.py`):
  a README carrying the scope sentence **and** the over-scope sentence *wrapped across a newline* yields
  `findings []` (status PASS), while the same over-scope sentence on one line yields `['F4','F4']`. The frozen
  checker's clause is a raw substring test (`"before instrument has no in-bound" in readme`) and the real r95
  README wraps that phrase (`corpus/README.md` at `73c47107`, line 1127-1128: *"the before instrument has no\nin-bound
  9-digit case"* — measured: the raw substring is **False**, the whitespace-flattened one **True**). I did **not**
  modify the checker (frozen); the L1's reflow workaround for the same defect is recorded in A2 and
  `w1/ExecCalibration.md` §4d. **Not a kill-rule breach**: the C2 kill rule asks that F1–F6 be *absent before* and
  *none remain after*, and F4 does fire on the pre-round tree via its first clause ("README does not scope the
  sentence to the r94 family roster", `before/c2-before-73c47107.json`) — but the class's *second* half is not
  machine-enforced in the landed bytes, so a future re-wrap of the over-scope sentence would pass silently.
  Worth an r97 criterion.
- **F3's clause 1 has no such blind spot** (`p5-p6.txt`): a wrapped *"largest in-bound"* still fires F3, because
  F3's other clause ("does not say boundary member") fires on the same edit.

## Receipts

| file | what it is |
|---|---|
| `.ufo/waves/round-96/w1/ScoutDrift/receipts.txt` | consolidated run of `receipts.py` (R1–R11) |
| `.ufo/waves/round-96/w1/ScoutDrift/receipts.py` | the script that produced it |
| `.ufo/waves/round-96/w1/ScoutDrift/cmp_claims.py` | the C1/C2 sentence comparator (item 1) |
| `.ufo/waves/round-96/w1/ScoutDrift/probes.py` | era arithmetic + component counts (items 2, 4) |
| `.ufo/waves/round-96/w1/ScoutDrift/probe-output.txt` | P1 era arithmetic, P2 component counts |
| `.ufo/waves/round-96/w1/ScoutDrift/p4_f4.py`, `p4-f4-blindspot.txt` | F4 clause-2 wrap blind spot |
| `.ufo/waves/round-96/w1/ScoutDrift/p5_p6.py`, `p5-p6.txt` | F3 wrap probe + the `#22` pointer probe |
| `.ufo/waves/round-96/w1/ScoutDrift/manifest-check.txt` | `sha256sum -c` of the freeze manifest (17 OK) |

## PASS/FAIL per expected line

| # | expected | observed | verdict |
|---|---|---|---|
| 1 | claims.json C1/C2 sentences == plan == before/plan-frozen.md, byte-level after whitespace normalisation; expected none | 8/8 sentences identical; plan and frozen plan byte-identical (`5d389241…`) | **PASS** |
| 2 | pre-r96 roster already sampled one four-component value (12.9.5.1); quote the r95 sentence that says otherwise and the r96 family that broadens it; the declaration must record broadened-not-first | `12.9.5.1` in both r95 `:1643` and r96 `:1662`; r95 Frontier bullet quoted; `EXTRA_COMPONENT_VALUES` + `fam_extra_component` quoted; "broadens a class the r95 roster sampled once … instead of claiming a first" in the plan, plus claims.json and A4 | **PASS** |
| 3 | read `considerthese/2026-10-26.md` in full; list every proposal with its status; select AT MOST ONE still-unimplemented proposal that fits, grounded by opening what it points at | 5 proposals listed with status + landing; **one** selected (Counter-attack scoreboard), grounded in `corpus/QUALITY.md:226`, `corpus/lessons/round-82.md:53`, `SKILL.md:3833ff`, proposal text L18, date 2026-10-26 | **PASS** (with D1 on the lesson's superlative) |
| 4 | the four new families' docstrings must match their code; flag any mismatch | 3/4 match; `REFUSAL-VERSIONS-9DIGIT-Y`'s era sentence is false (D3, routed to r97) | **PASS with one flagged mismatch** |
| D1 | lesson's "first unimplemented" superlative | false against QUALITY 115 / r82 ledger; already softened at HEAD | **finding** |
| D2 | amendments live in the plan's declared slot | they live in a misnamed `before/` file (5 headings, name says A1-A2); slot empty | **finding** |
| D3 | Y-family docstring | false era sentence | **finding** (routed to r97) |
| D4 | `corpus/README.md:844` pointer `considerthese/2026-10-26.md #22` | no `22.` item in this lane's copy or any lane's copy | **finding** |

**Not run / out of scope:** I ran no battery, no bend, no clone and no checker selftest — those are the executor
seats' measurements, and my seat's scope is the planning data-walk and the drift checks. Every number above is
from a run I made and whose raw output is in the receipts; I cite no number I did not produce.

{"seat":"ScoutDrift","verdict":"findings","notes":"Items 1-4 all answered and each meets its expected line (claims.json == plan == before/plan-frozen.md byte-identical after whitespace normalisation, 8/8 sentences, plan sha 5d389241 == frozen; pre-r96 roster already sampled 12.9.5.1 and the r96 declaration records EXTRA-COMPONENT as broadened-not-first in three places; considerthese swept 5 proposals with status lines, ONE selected (Counter-attack scoreboard) and grounded in QUALITY 115 + lessons/round-82.md + SKILL.md 3833ff, date 2026-10-26; 3 of 4 family docstrings match their code). Four drifts: D1 the lesson's 'first unimplemented item' superlative is false (QUALITY 115 adopted it at r82; already softened at HEAD 8fdb05e1); D2 the amendments live in .ufo/waves/round-96/before/plan-amendments-A1-A2.md (5 headings, name says A1-A2) with the plan's declared Amendment slot empty, and no r95 precedent; D3 REFUSAL-VERSIONS-9DIGIT-Y's docstring claims an X-only era reader answers era B for 0.999999999.0 - my arithmetic shows X=0 gives era A, so the rule that gives era B is Y-only/max; already routed to r97 by CriticClaims F-4; D4 corpus/README.md:844 cites 'considerthese/2026-10-26.md #22' but no such item exists in this lane's copy (3 numbered lines, 5 bullets) or in ANY lane's copy. Also recorded: the frozen C2 checker's F4 clause 2 is a raw substring test and misses a newline-wrapped over-scope sentence (probe p4-f4-blindspot.txt) - not a kill-rule breach (F4 does fire before via clause 1) but an r97 candidate; the 07:54 ad894667 checker drift is closed (7ff63524 restored, manifest 17 OK). No installs, no pacman, read-only git; scratch /fast/scratch/hyaku/tsukuroi-r96/ScoutDrift deleted before yield."}
