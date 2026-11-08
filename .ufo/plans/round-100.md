# Round 100 — declaration (frozen before any seat runs; controls committed with it)

Lane: tsukuroi (operability + freshness; host operability and repair). Fleet campaign: hyaku, run 15.
Round: 100 (attempt 1; the campaign's graduation round for this lane). Pre-round lane tip:
`ce73ccaf75d0279385977f03ccb35945c1cf8e07` (`master` == `origin/master`, clean, `ahead=0`).

## Inputs read before this freeze

- The round-99 closure (`MANIFEST.json` `rounds[]`: admitted) and its non-author spot-check
  `corpus/lessons/round-99-verifier-spotcheck.md`: routed defects **R99-D2** (LOG round-99 headings
  still read `(pending)`/`(pending-settle)` — append a correction entry), **R99-D3** (S395's anchor
  names one byte offset for two `LIE_KINDS` members: 108455 = `limine-version`, 108473 =
  `visibility-era`; a lesson note corrects it), **R99-D4** (record the census BEFORE command's exit
  code, not only the AFTER's), plus the carried items: the X/Y echo spelling bends, the five
  surviving C2 cell classes (A1), the C5 always-ok ancestor survivor's compound witness, and the
  owed `--selftest --reference` leg.
- `corpus/lessons/round-99.md`: Mistakes and the counter-attack scoreboard; `## Frontier moved this
  round` names by name "The X/Y **echo** legs have no spelling-targeted committed bend" and "the
  `unique` rule is fail-closed for a cell that legitimately states two spans".
- `corpus/README.md` § "Round 99" and its Frontier (round-99 addition).
- `corpus/QUALITY.md` 136-141 (136 named-limit-to-family closure; 139 the numeric bound's two legs;
  140 a target clause is re-read against one development run before the freeze; 141 byte-level
  anchors).
- `SCORECARD.md` axes: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8.
  Lowest non-retired axes: **depth 8** and **adjacency 8** (tied). C1 works depth; C2 works
  freshness. No adjacency move is declarable (kaidoku/revenger ownership is operator-owned,
  unruled — reported, not absorbed).
- `considerthese/2026-10-26.md` (newest batch) — mined by the connector seat; no proposal is
  implemented as a claim this round (the claims are instrument moves under the 1-3 cap).

Fresh-start status: not applicable — r95-r99 closures are all `ok`; the lane's fresh-start base is
r91 (Amendment 62) and no rejection has accrued since.

## Claims (2; frozen sentences; the same sentence in `.ufo/waves/round-100/claims.json`)

### C1 — depth 8 (tied lowest) — the accepted-cap families' ECHO legs get spelling-targeted bends

**Predicate.** `tools/check-limine-pins.py` is unchanged (`7d79ac29…`). `tools/make-r100-bends.py`
(new; exact-once substitution guard; refuses to emit a no-op) emits two one-clause bends of it:

- `N12-x-echo`: the returned JSON `limine_version` is falsified exactly when the FIRST version
  component is `999999999`; pins, rc and `visibility_era` stay the true values.
- `N13-y-echo`: the same, keyed on the SECOND component `999999999`.

Run against those articles, the landed battery `tools/limine-pin-battery-r99.py` (`c2e8c8fc…`,
unchanged) must move the two families whose `check_echo` flag the round-99 Frontier says no bend has
ever exercised.

**Target.** Landed gate `met 105/105`, `failed_families []`, 0 error rows, x3 canonical + x3 clone.
`N13-y-echo`: `unmet 104/105` x3 both layouts, exactly `["REFUSAL-VERSIONS-9DIGIT-Y"]`, 0 error
rows. `N12-x-echo`: `unmet 103/105` x3 both layouts, exactly
`["EXPLICIT-VERSION-ECHO", "REFUSAL-VERSIONS-9DIGIT"]`, 0 error rows. The r98 do-nothing battery
(`8198bd84…`) on the same articles: `N13` `met 105/105` x3 both layouts (blind — the Y assertion is
r99's alone), `N12` `unmet 104/105` x3 both layouts exactly `["EXPLICIT-VERSION-ECHO"]` (a
one-family discrimination delta, the same shape the r99 N11-x-era leg was measured and reported
in). Each bend's diff against the gate is exactly one changed line. `--selftest` without
`--reference` `PASS 5/5`.

**Development run (QUALITY 140, run before this freeze; receipts `.ufo/waves/round-100/before/dev/`).**
One run each: landed gate `105/105 met`; r99 on `N12` `103/105 [EXPLICIT-VERSION-ECHO,
REFUSAL-VERSIONS-9DIGIT]`; r99 on `N13` `104/105 [REFUSAL-VERSIONS-9DIGIT-Y]`; r98 on `N12`
`104/105 [EXPLICIT-VERSION-ECHO]`; r98 on `N13` `105/105 met`. Every frozen clause above is the
reading the instrument already produced; none was written from imagination.

### C2 — freshness 9 — the registry capture binds the cell's full label SET

**Predicate.** `tools/check-registry-content-r100.py` (successor; `check-registry-content-r99.py`
keeps its bytes as the do-nothing control) binds `RC-BEND-SPAN` as a label set: one `VARIANTS`
mention whose tokens are `N<digits>` or `N<digits>-N<digits>` (ranges expanded) joined only by `,`,
whitespace, `;`, `+`, `/` or the word `and`, and the declared set must equal the set derived from
the tool's `VARIANTS` keys. This closes the round-99 named limits — "the capture's alphabet is
still `N<digits>` with no space token" and "a registry cell that legitimately states two spans in
one cell must be rewritten to one span" — while every previously fail-closed shape stays closed.

**Target.** Live table at the freeze tip and at the landing tip: r100 `PASS bindings 7/7
findings 0`; the r99 control `PASS 7/7` on the same table. Six fixture cells read PASS on r100
where r99 reads a finding: `SEP-SPACE`, `SEP-SEMICOLON`, `SEP-PLUS`, `SEP-SLASH` (r99
`RC-CELL-MISSING`), `SEP-AND` and `UNION` (r99 `RC-VALUE-MISMATCH`). Five fail-closed controls:
`LETTER`/`PROSE` `RC-CELL-MISSING`, `UNION-LIE`/`HYBRID` `RC-VALUE-MISMATCH`, `RESTATED`
`RC-CELL-AMBIGUOUS`; `GAP` PASS on both. `--selftest PASS 26/26` (r99 control `17/17`).

**Development run.** r100 `--selftest PASS 26/26`; r99 `PASS 17/17`; live table `PASS 7/7` for both
at `ce73ccaf`; the twelve fixture readings in
`.ufo/waves/round-100/before/dev/c2-fixtures.txt` (6 PASS-before-FAIL, 5 fail-closed, 1 positive
control). Fixtures are built by the committed
`.ufo/waves/round-100/before/dev/make-fixtures.py`, which calls the frozen checker's own
`build_fixture` (no hand-copied bytes).

## Limits (named, not claimed)

- The X echo leg is a **delta**, not a flip: the r96 `EXPLICIT-VERSION-ECHO` family sends the same
  `999999999.9.9` spelling and already reads the echo, so the r98 control is not blind to it. Only
  the Y leg is a met-to-unmet closure.
- The r99 battery's blanket `lie-limine-version` selftest wrapper is not re-run with
  `--reference` this round (it needs a reference gate run, which the wave measures only if the
  `--selftest` leg's reference is exercised; the owed r99 A6a leg stays owed unless a seat measures
  it).
- C2 accepts separators, not prose: `N01 through N03` stays a finding, and a letter-suffixed token
  (`N01a-N03`) stays a finding. The capture still does not bind `N` labels outside `VARIANTS` keys.
- The other 158 operative registry rows stay presence-only (the coverage gate's scope); C2 binds the
  same seven cells it bound in r99/r98.
- The `--selftest --reference` leg, the C5 compound witness and the unbound-row class stay carried
  debt unless a wave seat measures them.

## Amendment slot

Any wording change forced by a wave artifact is recorded here, before the report, with the artifact
path and the narrowed sentence; the claims.json sentence is the frozen text and a widening after a
seat has scored is never the claim's rule. This slot is empty at freeze time.

## Axis and separability

- C1: depth 8 → 8 (a sharper instrument; no ordinal uplift). C2: freshness 9 → 9 (assurance arm; no
  ordinal claim). Neither claim touches the other's surface: C1 reads battery JSON from gate
  articles; C2 reads the SKILL.md registry table and fixture trees. Each verifies without the other
  landing.
- No axis is harmed: the gate and both r98/r99 controls keep their bytes; the corpus is additive;
  `SCORECARD.md` is append-only; `PROVINCE.md` and `SHONEN.md` are untouched by the round.

## Amendment slot — A1 (recorded 2026-11-08, after the wave, before filing)

**A1 — what "the landing tip" denotes.** SentinelHarm F1 and ExecRegistry measured that the first
landing commit `c450cd68` carried a 7-of-8-cell registry row, so all three registry gates read
`CANNOT_EVALUATE` at that revision, and that the repaired commit `69474c55` reads PASS. Ruling: the
C2 target's two surfaces are the **freeze tip** (`743ce449`; table 163 rows) and the **final landing
tip** (`69474c55` and any later round-100 commit), which are the revisions the round's landing is
measured at; an intermediate commit superseded inside the same round is not a scoring surface. The
intermediate failure is disclosed as mistake `R100-REGISTRY-ROW-CELL-COUNT` with its pair sweep, and
the repaired row's bytes are appended as the correction in `corpus/lessons/round-100.md`. This entry
records which revision the frozen sentence names; it does not widen or narrow the enforced property
(both named surfaces are PASS), and it is written after the fact only because the seat's artifact
raised the ambiguity.

Artifacts: `.ufo/waves/round-100/w1/SentinelHarm.md`, `.ufo/waves/round-100/w1/ExecRegistry/*`.

## Amendment slot — A2-A7 (recorded 2026-11-08 from wave artifacts, before filing)

The wave's two independent attackers (ReviewBends, CriticClaims) converged on the same narrowings;
each amendment cites its artifact. The frozen target numbers are unchanged: every one of them is
re-derived PASS in `after/c1/` and `after/c2/`.

- **A2 — C1's "ONLY the returned JSON `limine_version` line" is narrowed to the main return.**
  Both bends change the final verdict return's entry (BYTE 16931); the gate's early
  `conf unreadable` return also emits `limine_version` (BYTE 11230) and is untouched, so a cap
  spelling on an unreadable conf is not falsified and no claim is made about that path.
  Artifact: `.ufo/waves/round-100/w1/ReviewBends/receipts/direct-path-and-field-probe.json`;
  `.ufo/waves/round-100/w1/CriticClaims.md` C1.3 / its A1.
- **A3 — C1's X-leg unit.** The r98 control's *run* is already `unmet` on the N12 article; at the
  family unit the control flips exactly `EXPLICIT-VERSION-ECHO` from the landed gate's `met`, and
  r99 adds exactly `REFUSAL-VERSIONS-9DIGIT`. "Never a met-to-unmet flip" is therefore a run-level
  statement, not a family-level one. Artifact: `w1/ReviewBends/receipts/canon-*.json` (its A2).
- **A4 — the plan's paraphrase of the r99 Frontier is corrected to its own words.** The Frontier
  says "no spelling-targeted committed bend", not "no bend has ever exercised": the blanket r99
  `lie-limine-version` wrapper exercises the field (`unmet 93/105`, X/Y/Z/LZ named, 0 error rows).
  Artifact: `w1/ReviewBends/receipts/lie-limine-version-r99.json` (its A3).
- **A5 — C1's N13 payload.** `N13-y-echo`'s replacement is the fixed string `12.999999998.4`, so for
  the `0.999999999.0` spelling the reported first component also changes; the *trigger* is the second
  component. Artifact: `w1/CriticClaims.md` C1.4 / its A2.
- **A6 — C2's join grammar.** The tokeniser skips empty tokens, so `VARIANTS and N01-N03`,
  `VARIANTS N01-N03 and` and `VARIANTS N01; ; N02; N03` read PASS; only a non-empty part that is not
  an `N<digits>`/`N<digits>-N<digits>` token is `RC-CELL-MISSING`. Artifact:
  `w1/CriticClaims.md` C2.4 / its A3.
- **A7 — C2's set vs keys (sharpening, no claim change).** `RC-BEND-SPAN` compares against the
  `N<digits>`-prefixed labels of the bound tool's literal `VARIANTS` keys (unprefixed keys are not
  bound), and a mixed-width range normalises to the first token's zero-padding width. Artifact:
  `w1/CriticClaims.md` C2.3 / its A4.

No frozen predicate, counter, kill rule or target number is widened or narrowed by A2-A7: the claim
sentences in `.ufo/waves/round-100/claims.json` stay as frozen, and the report's verdicts use the
narrowed unit each amendment names.
