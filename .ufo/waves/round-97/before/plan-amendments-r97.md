# Round-97 plan amendments (the plan bytes are frozen at `a57e88cd`; this file is append-only)

### A1 (2026-11-08, after the wave's bend receipts, before the report; datum: `w1/ExecBend` report note + `sha256sum -c .ufo/waves/round-97/before/instruments.sha256`)

The C2 fixture **recipe** `before/fixtures/build-doctored-fixture.sh` was corrected after the freeze
(worktree mtime 08:52; the committed blob is the pre-correction one). The first version cloned the
lane's `master` as its base; once the freeze commit added the round's three tools, that base reads
`tools_total 157` against a 154-row operative table, so a re-run of the blindness leg returns the
coverage gate's own `REGISTRY-ROW-MISSING` FAIL instead of the `PASS 154/154` the claim states. The
corrected script pins `BASE=f48d16428d8bb92fd6cf546a745bff5b624e3f18` (the pre-round tip) into a
scratch bare origin, asserts the clone's base equals it, and records the checker's sha256. It also
re-ran the fixture: doctored revision `46fae1bae37e25b16088cf1ff2812eb8a7e04c77`, content `FAIL` with
6 `RC-VALUE-MISMATCH`, coverage `PASS 154/154 findings 0`, both fail-closed legs rc 2.

The recipe is not a scoring instrument. The instruments the claims read are byte-identical to the
freeze manifest, which stays as filed: `sha256sum -c .ufo/waves/round-97/before/instruments.sha256`
→ 19 OK, 1 FAILED (this recipe line only). The corrected set is pinned in
`before/instruments-r97-after-fixture-pin.sha256` (20/20 OK), and the C2 void clause is evaluated on
that file with this amendment as its narrowing pointer. No predicate, counter, kill rule or target
number changes.

The same window explains the other worktree changes under `before/dev/`: the do-nothing legs
(`c1-dn-bend-N05-z-cap-8`, `c1-dn-bend-N06-leading-zero-reject`) completed after the freeze commit
and their receipts were rewritten by the fixture re-run. They are evidence files, not instruments,
and they are committed at settle.

### A2 (2026-11-08, after the wave, before the report; datum: `w1/ExecDoNothing`, `w1/ReviewBattery`)

C1's target sentence says the landed-gate and do-nothing legs carry "0 error rows" and the bend legs
carry exactly 6 (N05) and 4 (N06) non-null `error` rows. Measured: every landed, clone, and
do-nothing run reads 0, and every bend run reads exactly 6 / 4, all `bad-output: JSONDecodeError
rc=64` (the bends' own refusals). No clause needs narrowing; this amendment records that the
development run and the wave agree, so the numbers stand as frozen.

### A3 (2026-11-08, after `w1/ExecDoNothing`, before the report; datum: `w1/ExecDoNothing/dn-usage-N06-leading-zero-reject.json`)

C1's target sentence calls the r96 do-nothing leg a "blindness receipt for both new families". The
measured scope is narrower and is now stated: the blindness is the **roster** leg (`--runs 3`,
`met 103/103`, 0 error rows) — exactly the numbers the frozen target names. At *instrument* level the
r96 battery's `--usage-check` mode already sends `12.09.4` and `00.00.00` (both `want_rc 0`) and
reads `unmet` on `N06-leading-zero-reject` with those two rows (`[('12.09.4', 0, 64), ('00.00.00',
0, 64)]`), and `met` on `N05-z-cap-8` and on the landed gate. Therefore: the **Z class** is
unsampled by both legs of the r96 instrument (its usage rows put the 9-digit cap in X and Y only);
the **leading-zero class** was sampled before this round at instrument level and is new at roster
level only — under QUALITY 136 the family is a roster-level closure, not a new instrument-level
sample. The roster readings, both bends and every other clause stand as frozen; the report, the
knowledge entry, the lesson and the SCORECARD state the split.

### A4 (2026-11-08, after `w1/ReviewRegistryContent` Z-1/F-1, before the report)

C2's target sentence reads "coverage gate on the doctored revision PASS 154/154 findings 0". Measured
scope: that holds on the revision **built on the pinned base `f48d1642`** (154 tools / 154 rows),
which the committed fixture script pins and asserts. On a post-freeze base the coverage gate reads
`FAIL` with three `REGISTRY-ROW-MISSING` findings for the freeze's own three tools (they land rows
only at settle), so a doctor built there cannot carry the blindness leg; at the settled tip the gate
reads `PASS 157/157`. The sentence is bound to the pinned base: receipts
`.ufo/waves/round-97/before/dev/c2-coverage-doctored.json` (doctored `46fae1ba…`, `PASS 154/154`,
`findings 0`) and `w1/ExecRegistryContent/06b-doctored2-coverage.txt` (doctored `9e052291…`, same
reading). No target number, doctor, predicate or kill rule changes.

The same amendment extends the named Limits with the three gaps the wave measured, each confirmed by
its own receipt and none of them a defect of the bound cells:
- (b) uncovered cells of a bound row read PASS (`w1/ReviewRegistryContent/receipts/02b-content.json`:
  the limine-pins verdict-map cell doctored, `status PASS bindings 7/7`);
- (c) a tool and its cell doctored together read PASS — the checker compares committed cell text to
  committed tool bytes at the SAME revision and cannot see a consistent dual edit
  (`receipts/02c-content.json`, `1 file changed` on the tool with a real extra selftest case);
- (d) a `selftest_total` binding parses a printed tally and does not execute the cases for the tool
  (`receipts/02d-content.json`: a `--selftest` replaced by `print("selftest PASS 7/7")` reads PASS).

### A5 (2026-11-08, after `w1/MutRegistry`, before the report; datum: `w1/MutRegistry.md` §3/§5)

Mutation testing of `tools/check-registry-content.py` killed 6 of 8 one-fault mutants and left two
survivors, both classified and neither a defect of C2's stated target: M07 (the `--revision`
ancestor check) is unreachable from `--selftest` by construction, and its non-equivalence is proved
by the round's own `c2-nonancestor` leg (`before/dev/c2-nonancestor.txt`, rc 2) which the mutant
turns into a PASS; M08 (`derive_variant_span` compares only the first label) is a genuine hole in
the checker's OWN tests — no fixture carries a non-contiguous `VARIANTS` label set, so the comma
branch is never exercised. M08 is routed to r98 as a selftest case (a `VARIANTS` set `N01,N03`);
the frozen selftest tally stays 12/12 and no instrument byte changes this round.

### A6 (2026-11-08, after `w1/CriticClaims` C1 docstring bullet, before the report; datum: `w1/CriticClaims/report.md` "Docstring defect" + receipts `05-*`, `06-*`)

`tools/limine-pin-battery-r97.py`'s `fam_leading_zero_normalize` docstring carries an illustrative
sentence that is wrong about which member a text comparison breaks. Measured (own re-derivation, and
the seat's two load-bearing gates): a raw-text comparison against `12.9.5` orders `12.09.4` and
`000000012.9.4` as era A (correct) and `12.000000009.000000005` as era A where `int()` gives era B —
the single discriminating member — so the docstring's "`000000012.9.4` as era B (wrong)" is false and
it names the wrong member. The frozen C1 predicate does not repeat the sentence (it says only
"accepted with its era's own answer"), so no number, family, expectation or kill rule changes; the
seat's text-comparison gate reads `104/105` unmet with exactly `[LEADING-ZERO-NORMALIZE]`, which is
the load-bearing evidence the claim needs. The frozen instrument bytes are not edited this round
(void clause); the sentence is corrected in the r98 successor with its own manifest — the same
treatment r96 gave its own Y-family sentence, and the round records it as mistake
`R97-LZ-DOCSTRING-TEXT`.

Two finer facts the seat measured, recorded as limits, not claims: in `REFUSAL-VERSIONS-9DIGIT-Z`
only the era-B member discriminates an era-blind gate (the era-A member and the second case of each
are acceptance redundancy), and in `LEADING-ZERO-NORMALIZE` only `12.000000009.000000005`
discriminates a text comparer.

### A7 (2026-11-08, after `w1/ReviewBattery` attacks 1-field and 2, before the report; datum: `w1/ReviewBattery/attack-1-field.txt`, `attack-2.txt`, `attack-derivation.txt`)

C1's sentence says the two new families' members are "each accepted … and answered from the era the
whole tuple selects (`panic` for era B, `prompt` for era A)". Two otherwise-conforming gates read
`met 105/105` ×3: one that answers the correct pins/consequence but reports `visibility_era:
pre-12.9.5` for `12.9.999999999` (`attack1-eraA-field`, one clause at the JSON field), and one that
echoes the NORMALIZED version (`12.9.4` instead of `12.09.4`) for the leading-zero members
(`attack2-echo-norm`, one clause). The measurement is therefore narrowed to what the families
assert: acceptance (never rc 64) and the era's own PIN ANSWER (`panic`/`prompt`), not the JSON
`visibility_era` field and not the echoed `limine_version` string. Those two properties are asserted
only by `EXPLICIT-VERSION-ECHO`/`EXPLICIT-VERSION-ERA` for their four explicit versions; for the new
members they are unsampled at family level and are named limits (r98 candidates: set `check_era` on
the Z family and `check_echo` on the LZ family). No number, family, bend or error-row clause
changes; the seat's attacks 1-pin (`104/105`, `[REFUSAL-VERSIONS-9DIGIT-Z]`), 3 (all-zero refusal,
`104/105`, `[LEADING-ZERO-NORMALIZE]`) and 4 (constant, `0/105`) are killed, and the error-row
strings are the bends' own rc-64 refusals.
