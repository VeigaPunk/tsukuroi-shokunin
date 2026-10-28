VERDICT: draft

# R49ScribeScore — `## Round 49 — measured outcome` draft (item F-7)

Seat: scribe, round 49 / hyaku run 11, wave `w1`. Execution class EXEC-AUTHORIZED: the only commands run are the
reads named in the item (round-48 outcome section, round-49 declaration, `FROZEN.md`) plus read-only byte reads of
the same freeze and of the already-existing `before/` receipts and `controls/` summaries. **No counter, selftest or
census was executed by this seat** (not in the item's authorization; counter runs also cost 60 s–10 min each).
Nothing was installed. No scratch dir was created and no receipt dir was needed — this seat wrote exactly one file,
this report. Nothing outside the lane's `.ufo/waves/round-49/w1/` was touched.

Deliverable: paste-ready section text between the `BEGIN DRAFT` / `END DRAFT` markers, plus the token fill table
(section 4) the L1 uses to close every placeholder.

---

## 1. Sources read (all at FREEZE `55c07cd3f8bff2e12117c34d57b4c618de74d85c`)

| Source | Read as | Used for |
|---|---|---|
| `SCORECARD.md:3110-3122` | `git show <FREEZE>:SCORECARD.md` | round-48 outcome **shape**: 4-column `Claim \| Frozen before → measured after \| Verdict \| Axis effect` table, `**PASS**`/`**FAIL**` bold vocabulary inside cells, a `No ordinal score changes.` paragraph, then one `Trend verdicts:` paragraph ending `Non-author spot-check remains pending.` |
| `SCORECARD.md:3124-3141` | same | round-49 declaration: ordinals at base (depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency tied lowest; saturation 9 / window 3, line 3126-3128), wave shape "ONE v2 wave (`w1`) sized 64–128" (line 3130), claim rows 3134-3136 with counters and kill rules, controls 3138-3139, causal separability 3140-3141 |
| `.ufo/waves/round-49/frozen/FROZEN.md:11-26` | `git show <FREEZE>:...` | claim/before/predicate table, frozen row-hash extents (`GR1` → `## GR1`..`## GR2`, `GR2` → `## GR2`..`## GR3`, `GR3` → `## GR3`..`## How this changes OS triage`) |
| `FROZEN.md:31-39` | same | C1 binding format (`ROW GR<n> VERDICT: holds\|partly\|fails`, `SECTION SHA256:`, ≥300-byte body, one `w1-results.json` entry + one dispatch task per seat, 18 seats) |
| `FROZEN.md:41-50` | same | control literature (K0..K6 / K0..K3 FAIL, K-pass PASS; K-pass fixtures are never the measurement; "the measurement is the live integrated revision") |
| `.ufo/waves/round-49/before/c1-at-base.json`, `c2-at-base.json`, `c3-at-base.json` | direct reads | exact **before** vectors used in the draft (all say `"revision": "6256760d…"`, `"verdict": "FAIL"`) |
| `.ufo/waves/round-49/controls/battery-summary-r49-c{1,2,3}.jsonl` | direct reads | control behaviour actually recorded: C1 7×`FAIL` + 1×`PASS`, C2 4×`FAIL` + 1×`PASS`, C3 3×`FAIL` + 1×`PASS` — matches `FROZEN.md:45-47` |
| `.ufo/waves/round-49/w1-dispatch.json`, `w1.ready`, `l1-summary.py` | direct reads | dispatch accounting the outcome header cites (`counts.spawn` 73; role mix; `l1-summary.py` prints `dispatched=… results=… reports=… attack=…/…` and `missing_or_unbound`) |
| `SCORECARD.md:3023-3033` | same | round-48 axes table wording (`| Axis | Score | Evidence pointer (counting command) | Last change |`) so the draft's ordinal sentences stay consistent with it |

## 2. Read-only pre-checks this seat performed (byte reads, no counter run)

1. **Frozen row hashes reproduce from the freeze blob.** Extents as `FROZEN.md:22-26` define them, LF-joined, no
   trailing LF:
   - GR1 → `3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1` (2366 B)
   - GR2 → `d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f` (5909 B)
   - GR3 → `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` (3291 B)
   All three equal the values in `FROZEN.md:24-26`, so the "corrections landed before data" claim is true of the
   freeze bytes. At the base revision the same computation gives GR1 `fe77ac76…`, GR2 `e0b391e1…`, GR3
   `43430a14…` (`before/c1-at-base.json` `section_sha256`) — **only GR1 and GR2 bytes moved**; GR3 was already at
   its frozen hash.
2. **The five forbidden defect strings are absent from the freeze blob** (`leading `0x` followed by a hex digit`,
   `which by SR7`, `dev-replace.c:1171-1199`, `only sets the state to SUSPENDED`, `which it is for a replace in
   state`) — consistent with `corr_forbidden_present: []` at the freeze; the base receipt carries all five.
3. **C2 at the freeze** `PROVINCE.md:46-52`: every ADJ-01..07 `Ownership source` cell names `OUT-002`…`OUT-010`
   (`ADJ-05` names `OUT-006, OUT-007`; `ADJ-06` names `OUT-008, OUT-009`), and the anchor table at
   `PROVINCE.md:122-130` has one row per OUT id with sibling pointer, `# …` heading, quote and registry fields.
   Nine sibling `PROVINCE.md:N-M` strings still exist in the file (`PROVINCE.md:33,197,301-305`) but **outside** the
   ownership cells; the C2 counter counts bare ranges only inside those cells
   (`tools/check-adjacency-table-r49.py:135`: `row_bare = BARE.findall(own)`), so they cannot hold `bare_ranges`
   above 0. `w1.ready.partial` shows the partial-report tail; whether any counted seat returns a bound negative is
   wave data this seat does not have.
4. **C3 at the freeze** `tools/tsukuroi-census.sh`: the stale `/tmp`-fixture comment is gone (usage line 608-609 now
   names the diagnostic instead), the resolver records `ST_BASE_ERR` (2079-2096), the named diagnostic is
   `selftest: fd band %s exhausted …; no /tmp fallback (R49-C3)` (2113-2119), and the `(R49-C3)` selftest case sits
   at 3574-3599 (`ST_BASE_ERR=fd-band`, empty `ST_BASE_DIR`/`ST_BASE_FD`). The counted `cases == 167` is the
   counter's own selftest run and was **not** measured here.
5. **Controls behaved as frozen** — see the `controls/` row above; every K-expectation in `FROZEN.md:45-47` holds in
   the recorded summaries.

## 3. Draft — paste verbatim between the markers

<!-- BEGIN DRAFT -->

## Round 49 — measured outcome (<DATE_UTC>; author-side, non-author closure pending)

Freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`; counted wave `w1`, the round's one v2 wave declared at 64–128
seats (`SCORECARD.md:3130`), <W1_DISPATCHED> seats dispatched (reviewer 18, critic 15, scout 13, executor 10,
scribe 7, mutation-tester 4, sentinel 4, connector 2 — `.ufo/waves/round-49/w1-dispatch.json`; attack roles
37/<W1_DISPATCHED> = <W1_ATTACK_SHARE>; <W1_REPORTS> reports and <W1_RESULTS> result entries landed;
<W1_DEATHS> seats missing or unbound — `python3 .ufo/waves/round-49/l1-summary.py`). L1 held the planner seat.
Measured revision `<AFTER_REV>`: every claim read at that revision with its frozen counter, no other revision.

Before receipts `.ufo/waves/round-49/before/c{1,2,3}-at-base.json` (all at base `6256760d`, all `FAIL`); after
receipts `<C1_RECEIPT>`, `<C2_RECEIPT>`, `<C3_RECEIPT>`. Pre-data controls behaved exactly as frozen, and their
K-pass fixtures are not reported as measurements (`FROZEN.md:49-50`): C1 K0-K6 `FAIL` + K-pass `PASS` (8/8,
`.ufo/waves/round-49/controls/battery-summary-r49-c1.jsonl`), C2 K0-K3 `FAIL` + K-pass `PASS` (5/5, `-c2.jsonl`),
C3 K0-K2 `FAIL` + K-pass `PASS` (4/4, `-c3.jsonl`).

Verdict vocabulary: **PASS** / **FAIL** only, decided by the frozen predicate at the measured revision. There is no
third claim-level verdict; a row-level `partly`/`fails` report on a current row hash is a C1 blocking condition
(`FROZEN.md:36-37`) and is reported inside the C1 row, never as a claim verdict.

| Claim | Frozen before → measured after | Verdict | Axis effect |
|---|---|---|---|
| C1 depth | `python3 tools/check-scrub-admission-r49.py --revision <AFTER_REV>` — before at base: `structural_ok 1, quotes_ok 3, corr_ok 0, verdicts_ok 0, seats_ok 0, marks_ok 0` (`before/c1-at-base.json`; marks entry/readme/skill all false; GR1 `fe77ac76…`, GR2 `e0b391e1…`, GR3 `43430a14…`) → after: `structural_ok <C1_STRUCTURAL>, quotes_ok <C1_QUOTES>, corr_ok <C1_CORR>, verdicts_ok <C1_VERDICTS>, seats_ok <C1_SEATS>, marks_ok <C1_MARKS>`; row hashes GR1 `<C1_GR1_SHA>`, GR2 `<C1_GR2_SHA>`, GR3 `<C1_GR3_SHA>` against the frozen extents `3a2ba180…`/`d4296085…`/`43430a14…` (`FROZEN.md:22-26`); receipt `<C1_RECEIPT>`; cohort <C1_BOUND_SEATS>/18 bound (`<C1_COHORT_NOTE>`) | **<C1_VERDICT>** | depth **unchanged** (ordinal 8, tied lowest; saturation band). A PASS closes the seven round-48 GR defects on frozen row bytes and adds a fresh 18-seat re-read, but admits no new knowledge entry and no new measured surface, so the ordinal does not move; no axis harmed observed. |
| C2 adjacency | `python3 tools/check-adjacency-table-r49.py --revision <AFTER_REV>` — before at base: `adj_rows 7, linked_rows 0, bare_ranges 9, anchors_ok 0, registry_ok 0, anchors_checker_rc 0` (`before/c2-at-base.json`) → after: `adj_rows <C2_ADJ_ROWS>, linked_rows <C2_LINKED>, bare_ranges <C2_BARE>, anchors_ok <C2_ANCHORS>, registry_ok <C2_REGISTRY>, anchors_checker_rc <C2_CHECKER_RC>`; receipt `<C2_RECEIPT>` | **<C2_VERDICT>** | adjacency **unchanged** (ordinal 8, tied lowest). The nine bare sibling ranges in the ADJ-01..07 ownership cells are replaced by portable `OUT-002`…`OUT-010` anchors whose pin, heading, quote and registry digest are checked — a locator-class repair of a capability already declared at fleet round 1, no ordinal move; no axis harmed observed. |
| C3 operability | `python3 tools/check-fd-band-r49.py --revision <AFTER_REV>` — before at base: `stale_ok 0, diag_ok 0, band_ok 0, cases 166`, while the selftest still printed `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)` (`before/c3-at-base.json` — the silent fallback was green) → after: `stale_ok <C3_STALE>, diag_ok <C3_DIAG>, band_ok <C3_BAND>, cases <C3_CASES>`; census blob sha256 `<C3_CENSUS_SHA>`; receipt `<C3_RECEIPT>` | **<C3_VERDICT>** | operability **unchanged** (ordinal 9, saturation band). The capability already existed; exhausted descriptor-band aliasing now fails by name (`fd band … exhausted`) and is proven by the `(R49-C3)` selftest case instead of silently falling back — behavior hardened, no ordinal move; no axis harmed observed. |

Kill rules (`SCORECARD.md:3132-3136`): C1 `<C1_KILL_RULE>` — <C1_KILL_STATUS>; of the 18 expected counted seats
<C1_BOUND_SEATS> bound (report file + `w1-results.json` entry + declared role) and <C1_DISTINCT> bodies are
byte-distinct; row verdicts read GR1 `<C1_GR1_VERDICTS>`, GR2 `<C1_GR2_VERDICTS>`, GR3 `<C1_GR3_VERDICTS>`.
C2 `<C2_KILL_RULE>` — <C2_KILL_STATUS>. C3 `<C3_KILL_RULE>` — <C3_KILL_STATUS>.

No ordinal score changes: depth 8, adjacency 8, operability 9 hold at `<AFTER_REV>`; coverage 9, freshness 9 and
calibration 9 are unchanged and not measured by this round's three claims. <ORDINAL_NOTE>

<MISSES_PARAGRAPH>

Sources and admission: <SOURCE_ADMISSION> — S255 (bash `fd>9` band exhaustion) was re-opened by the declaration
rather than newly admitted (`SCORECARD.md:3136`); no knowledge entry, SKILL row or README mark is admitted by this
round's outcome beyond the C1 marks the counter reads. Assimilation: <ASSIMILATION_STATUS>. No other lane is
contacted or called; no residual call is needed.

Trend verdicts: expansion **<EXPANSION_VERDICT>** (<EXPANSION_REASON>); quality **<QUALITY_VERDICT>**
(<QUALITY_REASON>); discernment **<DISCERNMENT_VERDICT>** (<DISCERNMENT_REASON>). Non-author spot-check remains
<SPOTCHECK_STATUS>.

<!-- END DRAFT -->

## 4. Token fill table (L1 closes these from receipts)

| Token | Source of truth | Expected on PASS |
|---|---|---|
| `<DATE_UTC>` | filing time | e.g. `2026-10-28T…Z`, matching the `.ufo/waves/round-49/` receipt mtimes |
| `<AFTER_REV>` | the integrated revision the counters were run at | 40-hex lane commit; must be the same revision for all three claims |
| `<W1_DISPATCHED>` | `w1-dispatch.json` `counts.spawn` (73 at dispatch, read this seat) or `l1-summary.py` `dispatched=` | integer |
| `<W1_ATTACK_SHARE>` | `w1-dispatch.json`: (reviewer+critic+mutation-tester)/dispatched = 37/N | decimal, 3 dp |
| `<W1_REPORTS>`, `<W1_RESULTS>`, `<W1_DEATHS>` | `l1-summary.py`: `reports=`, `results=`, `missing_or_unbound` | integers |
| `<C1_STRUCTURAL>`,`<C1_QUOTES>`,`<C1_CORR>`,`<C1_VERDICTS>`,`<C1_SEATS>`,`<C1_MARKS>` | `check-scrub-admission-r49.py` JSON keys `structural_ok`,`quotes_ok`,`corr_ok`,`verdicts_ok`,`seats_ok`,`marks_ok` | `1, 3, 1, 3, 18, 3` |
| `<C1_GR{1,2,3}_SHA>` | same JSON `section_sha256.GR<n>` | `3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1`, `d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f`, `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` |
| `<C1_BOUND_SEATS>`, `<C1_DISTINCT>` | `l1-summary.py` rows + the 18 report files | `18`, `18` |
| `<C1_GR{1,2,3}_VERDICTS>` | line 1 of the nine seats per row | `holds`×3 per row (any `partly`/`fails` on the current hash blocks) |
| `<C1_COHORT_NOTE>` | `w1-results.json` + report bytes | e.g. `9 reviewers + 9 critics, distinct bodies` |
| `<C1_RECEIPT>`,`<C2_RECEIPT>`,`<C3_RECEIPT>` | named by the L1 when the counters are run | `.ufo/waves/round-49/after/c1-final.json`, `c2-final.json`, `c3-final.json` (round-48 convention, `SCORECARD.md:3116-3118`) |
| `<C2_ADJ_ROWS>`,`<C2_LINKED>`,`<C2_BARE>`,`<C2_ANCHORS>`,`<C2_REGISTRY>`,`<C2_CHECKER_RC>` | `check-adjacency-table-r49.py` JSON keys `adj_rows`,`linked_rows`,`bare_ranges`,`anchors_ok`,`registry_ok`,`anchors_checker_rc` | `7, 7, 0, 7, 7, 0` |
| `<C3_STALE>`,`<C3_DIAG>`,`<C3_BAND>`,`<C3_CASES>` | `check-fd-band-r49.py` JSON keys `stale_ok`,`diag_ok`,`band_ok`,`cases` | `1, 1, 1, 167` |
| `<C3_CENSUS_SHA>` | `sha256sum tools/tsukuroi-census.sh` at `<AFTER_REV>` | 64-hex, truncated `…` form is fine if the full digest is in the receipt |
| `<C{1,2,3}_VERDICT>` | the counter's own `verdict` field | `PASS` / `FAIL` only — never a partial |
| `<C{1,2,3}_KILL_RULE>`, `<C{1,2,3}_KILL_STATUS>` | declaration 3134-3136 + the wave's mutation/labrat reports | literal rule text + `not fired` / `fired: <receipt>` |
| `<ORDINAL_NOTE>` | only if a claim FAILs | e.g. `depth stays 8 with the misses below named` |
| `<MISSES_PARAGRAPH>` | per-claim after data | round-48 style: name the surviving findings with report paths, and say when nothing was narrowed |
| `<SOURCE_ADMISSION>`, `<ASSIMILATION_STATUS>` | `corpus/SOURCES.md`, `.ufo/waves/round-49/assimilation/` (if any) | one clause each; `none` where nothing landed |
| `<EXPANSION_VERDICT>`/`<QUALITY_VERDICT>`/`<DISCERNMENT_VERDICT>` | see 5 below | `unchanged` / `improved` / `regressed` |
| `<SPOTCHECK_STATUS>` | non-author verification | `pending` unless a non-author seat filed a spot-check |

## 5. Trend-verdict decision rules (so the skeleton resolves deterministically)

- **expansion** — `improved` only if a new knowledge entry, source id or capability is *admitted* this round. C1's
  mark is an admission mark on an existing entry (`FROZEN.md:15`, `SCORECARD.md:3134`), so the default here is
  `unchanged` with reason `no new knowledge entry or source id admitted`.
- **quality** — `improved` if C1 and C3 are PASS (frozen row bytes bound by 18 seats; the silent fallback replaced
  by a named diagnostic and a selftest case) and the no-harm gates stay at base; `unchanged` if any claim is FAIL
  with no regression; `regressed` only with a named gate that passed at base and fails at `<AFTER_REV>`.
- **discernment** — `improved` if the three frozen counters refused all their negative controls (they did: 8/8,
  5/5, 4/4) **and** the round records its own kills; `unchanged` otherwise. The control batteries are already
  recorded, so this token is decided by the wave's kill/no-harm reporting.

## 6. Calibration limits of this draft

- Every after-value is a placeholder; **no claim verdict in this draft is a measurement by this seat**. The only
  numbers filled in are (a) before values from the frozen `before/` receipts, (b) the frozen row hashes, which this
  seat recomputed from the freeze blob and found identical to `FROZEN.md:24-26`, and (c) dispatch accounting read
  from `w1-dispatch.json`.
- This seat did not run `check-scrub-admission-r49.py`, `check-adjacency-table-r49.py`, `check-fd-band-r49.py`,
  `tools/tsukuroi-census.sh --selftest`, `l1-summary.py` or `check-self-assessment.py`; the counters' PASS/FAIL at
  `<AFTER_REV>` is unmeasured here.
- `w1-results.json` did not exist when this draft was written, so `<W1_RESULTS>`, `<W1_DEATHS>`, `<C1_BOUND_SEATS>`
  and every cohort token are placeholders by construction, not by choice.
- If a counted seat returns a bound negative on a *current* row hash, the C1 row must read **FAIL** and the axis
  sentence must keep `depth unchanged (8)` — the draft already assumes that outcome; only `<C1_VERDICT>` and the
  misses paragraph change.
