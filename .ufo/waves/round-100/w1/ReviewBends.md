# ReviewBends — C1 stated-wording attack (round 100, wave w1)

Seat: `ReviewBends` (leaf; no subagent dispatch). Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
(HEAD `69474c55eb38632f3e740923b58029dc43e01300`, detached; no mutating git/jj command was run).
All runs below are mine, in `/fast/scratch/hyaku/tsukuroi-r100/ReviewBends/`, with every receipt under
`.ufo/waves/round-100/w1/ReviewBends/receipts/`. The pinned manifest
`.ufo/waves/round-100/before/instruments.sha256` verified `16/16 OK` in the lane and in the clone before
any measurement (`receipts/clone-identity.txt`). No instrument or frozen file was edited.

## Axes

- **D — depth/wording fidelity:** does the frozen sentence describe exactly what the gate, the bends and
  the r99 battery enforce?
- **N — number fidelity:** are the frozen target numbers reproduced from my own runs?
- **C — clause discrimination:** does the declared evidence distinguish the one-clause diff from another
  bend that produces the same family-level reading?

Moves kept only when they improved D/N/C and harmed neither: re-derivation of both bends from the
generator's `VARIANTS` (AST-extracted, generator never executed), 15 battery legs × `--runs 3` in two
layouts, five constructed counterexample bends (E1, E1b, E2, E3, E4), one blanket `limine-version` lie
wrapper, and two direct gate probes. Nothing was retried toward a pass.

## The four frozen legs, re-derived (own runs, `--runs 3`, both layouts)

Canonical = the lane tree. Clone = `git clone --shared` of the lane at `69474c55`, toplevel asserted
`/fast/scratch/hyaku/tsukuroi-r100/ReviewBends/clone`, `sha256sum -c` `16/16` inside the clone
(`receipts/clone-identity.txt`). The clone and canonical readings below are identical run-for-run.

| leg | layout | runs | verdict | families | failed_families (instrument order) | failed rows/run | error rows/run |
|---|---|---|---|---|---|---|---|
| landed gate `7d79ac29…` | canonical | 3 | met | 105/105 | `[]` | 0 | 0 |
| landed gate | clone | 3 | met | 105/105 | `[]` | 0 | 0 |
| `N13-y-echo` | canonical | 3 | unmet | 104/105 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | 4 | 0 |
| `N13-y-echo` | clone | 3 | unmet | 104/105 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | 4 | 0 |
| `N12-x-echo` | canonical | 3 | unmet | 103/105 | `["EXPLICIT-VERSION-ECHO", "REFUSAL-VERSIONS-9DIGIT"]` | 5 | 0 |
| `N12-x-echo` | clone | 3 | unmet | 103/105 | `["EXPLICIT-VERSION-ECHO", "REFUSAL-VERSIONS-9DIGIT"]` | 5 | 0 |
| r98 control `8198bd84…` on N13 | canonical | 3 | met | 105/105 | `[]` | 0 | 0 |
| r98 control on N13 | clone | 3 | met | 105/105 | `[]` | 0 | 0 |
| r98 control on N12 | canonical | 3 | unmet | 104/105 | `["EXPLICIT-VERSION-ECHO"]` | 1 | 0 |
| r98 control on N12 | clone | 3 | unmet | 104/105 | `["EXPLICIT-VERSION-ECHO"]` | 1 | 0 |

Named-family case counts (identical in every run of a leg, both layouts):

- N12: `REFUSAL-VERSIONS-9DIGIT` 0/4, `REFUSAL-VERSIONS-9DIGIT-Y` 4/4, `EXPLICIT-VERSION-ECHO` 3/4 —
  the cap spelling is exactly ONE member of the four-case E family (the predicate's singular "member").
- N13: X 4/4, Y 0/4, E 4/4.
- r98 on N12: X 4/4, Y 4/4, E 3/4.
- r98 on N13 and the landed gate: all three 4/4.

Receipts: `receipts/canon-{gate,N12,N13,r98-N12,r98-N13}.json`,
`receipts/clone-{gate,N12,N13,r98-N12,r98-N13}.json`, parsed by the frozen counting command into
`receipts/count-runs-core.txt`; per-run census `receipts/census.json`.

Static pre-checks, byte-measured on the pinned bytes (`grep -abo`, QUALITY 141):

- The gate has **two** `limine_version` emission sites: BYTE **11230** (early `conf unreadable` return)
  and BYTE **16931** (final verdict return); `visibility_era` at BYTEs 11344 / 17037.
- Both committed bends change the entry at BYTE **16931** only; `diff -u` shows exactly one `-`/`+` pair
  each (`receipts/bend-diffs.txt`).
- Re-deriving both bends from `tools/make-r100-bends.py`'s `VARIANTS` (extracted with `ast.literal_eval`,
  the generator was NEVER run) reproduces the committed bytes: N12 `eb247e16…`, N13 `e1e5916f…`, both
  `IDENTICAL` (`receipts/bend-diffs.txt`).
- `meta_ok`'s echo assertion is exact string equality: `got[8] == c.version and got[9] == "flag"` at BYTE
  **99430**; the echo-checked families are X (echo@79015), E (79893), Y (81666), Z (83173), LZ (84390);
  `Y_DIGIT9` at BYTE 77254; `FAMILY_ROSTER` is 105 unique names.

## Attack shapes and verdicts

### A. Two-clause bend: Y echo lie **plus** a `visibility_era` lie — does "ONLY the emitted JSON `limine_version` line" still describe the instrument? — **neutral (with an evidence-structure finding)**

Constructed in scratch (`instr/E1-y-echo-plus-era.py`, two changed lines; `instr/E1b-y-era-only.py`, era
only; both one-substitution, exact-once, `compile()`d). r99 `--runs 3`:

- E1 (echo+era): unmet **104/105 `["REFUSAL-VERSIONS-9DIGIT-Y"]`**, 4 failed rows — the same
  family-level reading as the committed N13.
- E1b (era ONLY, no `limine_version` lie at all): unmet **104/105 `["REFUSAL-VERSIONS-9DIGIT-Y"]`**, 2
  failed rows (the `0.999999999.0` member's true era is already `pre-12.9.5`, so the era lie is a no-op
  there; the `12.999999999.4` member fails). Its failed rows carry `got[5] == "12.999999999.4"` — the
  echo is TRUE; the only lie is the era.

So the target's family-level numbers (`104/105 [Y]`) are produced identically by a one-clause echo lie,
a two-clause echo+era lie, and an era-only lie. The frozen sentence's "ONLY" is therefore enforced by the
**one-line diff at BYTE 16931**, not by the battery reading. The sentence itself is true (the committed
bends do change one line and do not move `visibility_era`); the reading is simply not clause-discriminating.
Direct field probe on a readable conf (`receipts/direct-path-and-field-probe.json`): against the landed
gate, N12 differs in exactly `["limine_version"]` on the X cap, N13 in exactly `["limine_version"]` on the
Y cap, and both differ in **zero** fields on non-cap spellings; `rc`, `verdict`, `visibility_era`,
`limine_version_source` are byte-identical. No amendment for A.

### B. Leading-zero echo (`12.999999999.4` vs `012.999999999.4`) — does `check_echo` fail it, and does the claim say so? — **neutral (instrument is stricter than the sentence's subject; roster-finite limit)**

- `check_echo` is exact spelling equality (BYTE 99430), not cap-keyed. E2 (`instr/E2-leading-zero-echo.py`,
  echo re-rendered from the parsed tuple when any component has a leading zero) reads unmet
  **104/105 `["LEADING-ZERO-NORMALIZE"]`**, 4/4 LZ rows failed, everything else green
  (`receipts/canon-E2.json`). So yes: a gate that echoes `12.9.4` for the flag `12.09.4` is failed.
- The exact example is live: `012.999999999.4` is ACCEPTED by the landed gate (rc 0, echo verbatim,
  `visibility_era 12.9.5+`), and N13 DOES fire on it (echo `12.999999998.4`) — the second component is the
  literal cap (`receipts/direct-cap-spellings-probe.json`). A hypothetical bend keyed **only** on that
  roster-absent spelling (`instr/E4-y-cap-leading-zero.py`) reads **met 105/105**
  (`receipts/canon-E4.json`): the Y-cap family witnesses two spellings (`Y_DIGIT9`, BYTE 77254), not
  every accepted spelling with the cap in the second component.
- The frozen sentence is about the committed bend, and there the "exactly when" is exact: no accepted
  ≤9-digit spelling of 999999999 other than the literal `999999999` exists, and `0999999999.9.9` is
  refused rc 64 (`receipts/direct-cap-spellings-probe.json`). No amendment; the limit is roster finiteness
  (same class as r99 A8/W1), not a false clause. If anyone reads the sentence as a property of
  `check_echo`, it is false there: the check also fires on any non-verbatim echo (E2).

### C. A bend keyed on the THIRD component — does the target's "second component" wording stay exact? — **neutral (confirms)**

`instr/E3-z-echo.py` (echo lies when `split(".")[2] == "999999999"`) reads unmet
**104/105 `["REFUSAL-VERSIONS-9DIGIT-Z"]`**, Z 0/4, **Y 4/4 green**, X 4/4 green, 0 error rows
(`receipts/canon-E3.json`, 3/3 runs). The component attribution is exact and discriminating: the Z bend
hits Z and not Y; N13 hits Y and not Z.

### D. The X zig-zag — does N12 ever include Y or exclude `EXPLICIT-VERSION-ECHO`? — **neutral (confirms)**

No: 3/3 canonical and 3/3 clone runs read exactly `["EXPLICIT-VERSION-ECHO",
"REFUSAL-VERSIONS-9DIGIT"]`; Y is 4/4 green in every run; the E family fails exactly its one cap member
(3/4). The r98 control on the same article is exactly `["EXPLICIT-VERSION-ECHO"]` (X 4/4 green) — the
one-family discrimination delta.

### E. The **other** `limine_version` return path — **falsifies-wording** → amendment **A1**

Both bends change only the final verdict-return entry at BYTE 16931. The gate's early `conf unreadable`
return emits `limine_version` too (BYTE 11230) and is untouched. Direct probe with a cap spelling and
`--conf` = a directory (`receipts/direct-path-and-field-probe.json`):

- landed / N12 / N13 all return rc 2 `CANNOT-EVALUATE` with `limine_version` **`999999999.9.9`** and
  `12.999999999.4` respectively — the bends do **not** falsify the field on this path;
  `fields_differing_from_landed` is `[]` for both bends.
- `fam_conf_unreadable` (r99) sets neither `check_echo` nor a cap version, so the battery cannot see this;
  the frozen 103/105 and 104/105 readings are unaffected (not a number falsification).

The predicate's "falsifies that field exactly when the FIRST/SECOND component is the cap" therefore omits
the readable-conf conjunct. When the conf is unreadable and the component is the cap, the field is
returned TRUE. **Proposed amendment A1** (narrowing; record in the plan's amendment slot):

> A1 — replace "each changing ONLY the returned JSON `limine_version` line: `N12-x-echo` falsifies that
> field exactly when the FIRST version component is the cap `999999999` … and `N13-y-echo` exactly when the
> SECOND component is `999999999`" with "each changing ONLY the final verdict-return JSON `limine_version`
> entry (the gate's early `conf unreadable` return, BYTE 11230, still echoes the true value, so a cap
> spelling on an unreadable conf is NOT falsified): `N12-x-echo` falsifies that entry exactly when the conf
> is readable and the FIRST version component is the cap `999999999` … and `N13-y-echo` exactly when the
> conf is readable and the SECOND component is `999999999`".
> Receipt: `.ufo/waves/round-100/w1/ReviewBends/receipts/direct-path-and-field-probe.json`.

### F. The r98 control gloss "never a met-to-unmet flip" — **falsifies-wording at the sentence's own unit** → amendment **A2**

The clause reports a family-level reading and then glosses it at a run/leg-level unit. Measured on the
same article: landed gate `105/105 met []`; r98 control on N12 `104/105 unmet ["EXPLICIT-VERSION-ECHO"]`;
r99 on N12 `103/105 unmet ["EXPLICIT-VERSION-ECHO","REFUSAL-VERSIONS-9DIGIT"]`. At the family unit the
control does flip `EXPLICIT-VERSION-ECHO` from met to unmet (one family); it is the run-level "the control
is already unmet" that is not a flip. **Proposed amendment A2**:

> A2 — replace "(a one-family delta, never a met-to-unmet flip)" with "(the control's run is already
> `unmet`; at the family unit the control flips exactly `EXPLICIT-VERSION-ECHO` from the landed gate's
> `met`, and r99 adds exactly `REFUSAL-VERSIONS-9DIGIT` — a one-family delta in the failed set, not a
> blind control)".
> Receipts: `receipts/canon-gate.json`, `receipts/canon-r98-N12.json`, `receipts/canon-N12.json`.

### G. The plan predicate's paraphrase of the round-99 Frontier — **falsifies-wording (plan text)** → amendment **A3**

The plan says the bends "must move the two families whose `check_echo` flag the round-99 Frontier says no
bend has ever exercised". The Frontier says **"no spelling-targeted committed bend"**, not "no bend". The
r99 blanket `lie-limine-version` wrapper does exercise the flag: re-run by me against the r99 battery,
`--runs 1`, it reads **unmet 93/105** with X/Y/Z/LZ 0/4 (12 families named), 0 error rows
(`receipts/lie-limine-version-r99.json`, `.count.txt`). So the field is exercised; what is missing is a
spelling-targeted committed bend. **Proposed amendment A3**:

> A3 — replace "whose `check_echo` flag the round-99 Frontier says no bend has ever exercised" with
> "whose `check_echo` flag no spelling-targeted committed bend has exercised (the r99 blanket
> `lie-limine-version` wrapper does exercise the field — `unmet 93/105`, X/Y/Z/LZ named — so it proves the
> field, not the family)".
> Receipt: `.ufo/waves/round-100/w1/ReviewBends/receipts/lie-limine-version-r99.json`.

### H. `--selftest` without `--reference`, and the conflict kill — **neutral (holds)**

`python3 tools/limine-pin-battery-r99.py --selftest` prints `selftest PASS 5/5`, rc 0, with
`reference-gate skipped (no --reference)` (`receipts/selftest-no-reference.txt`). The kill clause's
"0 error rows" and "one changed line" conditions hold for every measured run.

## Error-row census (per run, from the parsed JSON, not an assertion)

15 legs × `--runs 3` = **45 runs**, 420 case rows each = **18,900 case rows**. `error is not None`:
**0 in every run** (45/45). `got is None`: **20 per run** (900 total), all of them `kind: "usage"` rows of
the five refusal/probe families, all `passed: true` — they are not errors. Failed rows per run: landed
gate 0 (both layouts), N13 4 (both), N12 5 (both), r98-N13 0 (both), r98-N12 1 (both), E1 4, E1b 2, E2 4,
E3 4, E4 0. The blanket lie run adds 1 run × 420 rows, 0 error rows. Machine-readable:
`receipts/census.json`.

## PASS/FAIL against the frozen target lines

| frozen line (claims.json C1 target) | expected | measured | verdict |
|---|---|---|---|
| landed gate | met 105/105 `[]`, 0 error rows, ×3 canonical + ×3 clone | 3/3 + 3/3 exactly | PASS |
| N13 | unmet 104/105 ×3 both, exactly `[Y]`, 0 error rows | 3/3 + 3/3 exactly | PASS |
| N12 | unmet 103/105 ×3 both, exactly `[E, X]`, 0 error rows | 3/3 + 3/3 exactly | PASS |
| r98 on N13 | met 105/105 ×3 both | 3/3 + 3/3 | PASS |
| r98 on N12 | unmet 104/105 ×3 both, exactly `[E]` | 3/3 + 3/3 | PASS |
| each bend diff | exactly one changed line | one `-`/`+` pair each; re-derived bytes identical | PASS |
| `--selftest` (no `--reference`) | PASS 5/5 | PASS 5/5, rc 0 | PASS |

## Residual risk and verification gaps

- The family-level target cannot witness the "ONLY `limine_version`" clause (shape A): an era-only Y lie
  produces the identical 104/105 `[Y]`. The diff is the witness; a future claim that cites the reading as
  proof of the clause would be over-reading.
- The Y-cap echo coverage is roster-finite: `Y_DIGIT9` carries two spellings; `012.999999999.4` is an
  accepted, N13-covered spelling that no family carries, so a bend keyed only on it reads 105/105 (E4).
  The same r99 A8/W1 roster-fit limit, unchanged.
- `check_echo` is a conjunction (`echo == flag` AND `source == "flag"`); a source-only lie is also
  indistinguishable at family level. Not attacked this round (the bends leave source true).
- The plan's C1 Predicate and the claims.json C1 predicate are not verbatim identical (the glosses differ:
  "a one-family discrimination delta, the same shape the r99 N11-x-era leg …" vs "a one-family delta,
  never a met-to-unmet flip"). The numbers agree; the plan line "(the same sentence in … claims.json)" is
  loose. Amendments A2/A3 should land in both texts.
- I did not run `tools/make-r100-bends.py` (it writes the frozen wave dir); the re-derivation proves its
  two substitutions byte-for-byte but not its write path.
- No tool was installed or upgraded; `bwrap` was already present (`/usr/bin/bwrap`); pacman was not used.
  Scratch `/fast/scratch/hyaku/tsukuroi-r100/ReviewBends` was removed before this file was written.

{"seat":"ReviewBends","verdict":"findings","notes":"C1 numbers reproduce in full (gate met 105/105 x3+x3; N13 104/105 [Y] x3+x3; N12 103/105 [E,X] x3+x3; r98 104/105 [E] and met x3+x3; selftest 5/5; 0 error rows in 45 runs / 18,900 rows). Wording: A1 the 'exactly when the component is the cap' clause omits the readable-conf conjunct — the early conf-unreadable return (BYTE 11230) still echoes the true value, so a cap spelling there is not falsified (amendment proposed); A2 'never a met-to-unmet flip' contradicts the same sentence's family-level reading (the control flips EXPLICIT-VERSION-ECHO from the landed gate's met to unmet); A3 the plan attributes 'no bend has ever exercised' to the round-99 Frontier, which says 'no spelling-targeted committed bend' — my re-run of the blanket lie wrapper reads 93/105 with X/Y/Z/LZ named. Clause discrimination is by the one-line diff (BYTE 16931) only: an era-only Y lie and a two-clause Y lie both read 104/105 [Y]. Z-keyed bend hits Z not Y; X never includes Y; leading-zero normalization is failed by check_echo (E2 104/105 [LZ]); a Y-cap lie on the roster-absent spelling 012.999999999.4 survives 105/105."}
