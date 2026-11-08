# CriticClaims — round 100 w1 — falsification of the frozen C1/C2 sentences

Seat: `CriticClaims` (roster id `CriticClaims-22`). Lane root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Lane HEAD at every run below:
`69474c55eb38632f3e740923b58029dc43e01300` (`== master`); freeze tip `ce73ccaf75d0279385977f03ccb35945c1cf8e07`.
Scratch: `/fast/scratch/hyaku/tsukuroi-r100/CriticClaims` (deleted before yield; every receipt cited
below was written by this seat under `.ufo/waves/round-100/w1/CriticClaims/`).

This seat wrote nothing outside its seat dir and its scratch. The `M corpus/QUALITY.md` /
`M corpus/lessons/round-100.md` visible in `git status` during the wave are the L1's live edits
(QUALITY 142 appears only in the working tree, not at HEAD); they are not this seat's writes and are
not cited as frozen text.

## 0. Harm guard first — pinned bytes

```
$ sha256sum -c .ufo/waves/round-100/before/instruments.sha256
tools/check-limine-pins.py: OK                    tools/limine-pin-battery-r99.py: OK
tools/limine-pin-battery-r98.py: OK               tools/check-registry-content-r99.py: OK
tools/check-registry-content-r100.py: OK          tools/make-r100-bends.py: OK
tools/make-r96-bends.py: OK                       tools/check-registry-coverage.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r99.py: OK
.ufo/waves/round-100/before/controls/do-nothing-checker-r99.py: OK
.ufo/waves/round-100/before/controls/bends/N12-x-echo.py: OK
.ufo/waves/round-100/before/controls/bends/N13-y-echo.py: OK
.ufo/waves/round-100/before/dev/make-fixtures.py: OK
.ufo/waves/round-100/claims.json: OK              .ufo/plans/round-100.md: OK
```

"Unchanged" is corroborated across rounds: the r99 manifest
`.ufo/waves/round-99/before/instruments.sha256` already pins the same gate `7d79ac29…`, r99 battery
`c2e8c8fc…`, r98 battery `8198bd84…` and r99 checker `b489f5b8…`; the r98 manifest pins the same
gate and r98 battery. All 16 manifest lines verified OK at the run moments.

Registry coverage gate (harm guard), as found:

```
$ python3 tools/check-registry-coverage.py --revision 69474c55
{"branch":"master","branch_tip":"69474c55…","counts":{"findings":0,"missing":0,
 "registered":165,"rows_total":165,"tools_total":165},"findings":[],"status":"PASS"}
$ python3 tools/check-registry-coverage.py --revision ce73ccaf
{… "registered":163,"rows_total":163,"tools_total":163 … "status":"PASS"}
$ python3 tools/check-registry-coverage.py --revision HEAD
{"findings":[{"detail":"7-64 hex commit required","id":"E-REVISION-INVALID",…}],"status":"CANNOT_EVALUATE"}
```

PASS at both the freeze tip and the landing tip; the gate accepts only a hex revision (`HEAD` is
rejected as a literal — a CLI quirk, not a finding against the round). Receipt:
`coverage.txt`.

## 1. Axes named

| axis | question this seat asks |
|---|---|
| depth (C1) | Does each bend move exactly the field assertion claimed, on both layouts, without moving any other field, and is the sentence true of the code at every return path? |
| freshness (C2) | Is the `RC-BEND-SPAN` binding truly set-valued and exact (both directions), does it close both r99 named limits, and do all previously fail-closed shapes stay closed? |
| provenance/harm | Instruments unchanged (manifest), controls unchanged, coverage gate still PASS, no writes outside the seat. |

## 2. C1 — clause by clause

Frozen predicate quote (claims.json, byte 0…; the C1 predicate is line 7 of the JSON):

> `tools/make-r100-bends.py` emits exactly two one-clause bends of the landed gate … each changing
> ONLY the returned JSON `limine_version` line: `N12-x-echo` falsifies that field exactly when the
> FIRST version component is the cap `999999999` … and `N13-y-echo` exactly when the SECOND
> component is `999999999` …; pins, rc and `visibility_era` are computed from the true value.

### C1.1 "emits exactly two one-clause bends"

Two readings: (a) the generator's `VARIANTS` table has exactly two entries and the committed control
dir has exactly two files; (b) re-running the generator on the unchanged gate reproduces those two
bytes and nothing else.

```
$ wc -l tools/make-r100-bends.py      → 78        (VARIANTS = { … } has two entries, lines 40-61)
$ ls .ufo/waves/round-100/before/controls/bends/   → N12-x-echo.py  N13-y-echo.py   (exactly two)
$ cp tools/{check-limine-pins.py,make-r100-bends.py} $SCRATCH/reemit/tools/ && \
  (cd $SCRATCH/reemit && python3 tools/make-r100-bends.py)
wrote …/reemit/.ufo/waves/round-100/before/controls/bends/N12-x-echo.py (30409 bytes, one clause bent)
wrote …/reemit/.ufo/waves/round-100/before/controls/bends/N13-y-echo.py (30446 bytes, one clause bent)
$ cmp -s $SCRATCH/reemit/…/N12-x-echo.py .ufo/…/N12-x-echo.py && echo N12 IDENTICAL
N12 IDENTICAL
N13 IDENTICAL
```

Guard probe (the pattern is made to miss by one trailing space on the main return line):

```
$ python3 tools/make-r100-bends.py      (in $SCRATCH/reemit-miss, perturbed gate copy)
N12-x-echo: pattern '    return {"schema": …' matched 0 times, expected 1
guard-rc=1        (no output dir written)
```

Observed: exactly two variants; re-emission byte-identical; a non-matching pattern is refused and
nothing is written. The no-op branch (`if out == text`) is unreachable for these two substitutions
(old ≠ new), so it is a code-read guard, not a measured one.

**Verdict: enforced.**

### C1.2 "each changing ONLY the returned JSON `limine_version` line"

Two readings: (a) the file diff is one line; (b) the JSON output changes only that key.

```
$ diff -u tools/check-limine-pins.py .ufo/…/bends/N12-x-echo.py
@@ -313,7 +313,7 @@
-            "limine_version": limine_version,
+            "limine_version": ("999999998.9.9" if limine_version.split(".")[0] == "999999999" else limine_version),  # N12 …
$ diff -u tools/check-limine-pins.py .ufo/…/bends/N13-y-echo.py
@@ -313,7 +313,7 @@
-            "limine_version": limine_version,
+            "limine_version": ("12.999999998.4" if limine_version.count(".") >= 1 and limine_version.split(".")[1] == "999999999" else limine_version),  # N13 …
$ diff -u … | grep -c '^[+-][^+-]'       → 2 (one `-`/`+` pair; one hunk; no other hunk)
```

JSON-output reading (`c1-fieldcmp.txt`; a real conf with one OK pin and one mismatching pin, so
`rc`/`pins`/`findings` are non-trivial; each bend compared with the gate on the same argv, all keys
deep-compared):

```
N12 999999999.9.9   rc=1/rc=1 keys-differing={"limine_version": ["999999999.9.9","999999998.9.9"]}
N12 12.999999999.4  rc=1/rc=1 keys-differing={}
N12 0.999999999.0   rc=1/rc=1 keys-differing={}
N12 12.9.4          rc=1/rc=1 keys-differing={}
N13 999999999.9.9   rc=1/rc=1 keys-differing={}
N13 12.999999999.4  rc=1/rc=1 keys-differing={"limine_version": ["12.999999999.4","12.999999998.4"]}
N13 0.999999999.0   rc=1/rc=1 keys-differing={"limine_version": ["0.999999999.0","12.999999998.4"]}
N13 12.9.4          rc=1/rc=1 keys-differing={}
```

Observed: one line replaced; the only JSON key that ever differs is `limine_version`, and only on
the trigger spelling; `pins`, `rc`, `verdict`, `visibility_era`, `limine_version_source`,
`on_panic`, `findings` are byte-identical to the gate.

**Verdict: enforced (both readings).**

### C1.3 "N12-x-echo falsifies that field exactly when the FIRST version component is the cap"

Two readings: (a) trigger reading — whenever the first component is `999999999`, the reported value
differs from the truth, and otherwise it does not; (b) universal reading — *every* JSON return that
carries `limine_version` obeys (a).

Direct CLI probes on the main return (`c1-fieldcmp.txt` / raw table in §2 commands):

```
N12 --limine-version 999999999.9.9   → limine_version '999999998.9.9'   (falsified)
N12 --limine-version 12.999999999.4  → '12.999999999.4'                 (truth)
N12 --limine-version 0.999999999.0   → '0.999999999.0'                  (truth)
N12 --limine-version 9.999999999.9   → '9.999999999.9'                  (truth)
N12 --limine-version 12.9.4          → '12.9.4'                         (truth)
```

Early (unreadable-conf) return of the *same* field:

```
$ python3 .ufo/…/N12-x-echo.py --conf <absent> --esp <dir> --limine-version 999999999.9.9
verdict CANNOT-EVALUATE rc 2 limine_version '999999999.9.9'   ← NOT falsified
```

The file has two returns that emit the field — `grep -abo '"limine_version": limine_version,'`
gives bytes **11230** (line 200, `CANNOT-EVALUATE` path, 16-space indent) and **16931** (line 316,
main path, 12-space indent). The generator's exact-once pattern includes the 12-space main-return
line only; the 16-space early return cannot match it. Read (a) is enforced on the main return; read
(b) is false.

**Verdict: narrower-than-stated** (the implementation falsifies on a strict subset of the returns
that carry the field). Amendment A1 in §5.

### C1.4 "N13-y-echo … exactly when the SECOND component is `999999999`"

Trigger probes (`c1-fieldcmp.txt`):

```
N13 --limine-version 12.999999999.4  → '12.999999998.4'   (falsified)
N13 --limine-version 0.999999999.0   → '12.999999998.4'   (falsified; the FIRST component changes too)
N13 --limine-version 9.999999999.9   → '12.999999998.4'   (falsified; X and Z also change)
N13 --limine-version 999999999.9.9   → '999999999.9.9'    (truth — second component is 9)
N13 --limine-version 12.9.4          → '12.9.4'           (truth)
N13 --limine-version 999999999.9.9 --conf <absent> → '999999999.9.9' (early return, truth)
```

Two readings: (a) the *trigger* is keyed on the second component — true for every spelling sent and
for the code; (b) the *payload* is a Y-component substitution — false: the replacement is the fixed
string `12.999999998.4`, so for `0.999999999.0` (and `9.999999999.9`) the reported first component
changes as well. The sentence names the trigger, so (a) is the natural reading and it is enforced;
the payload reading is narrower than the code's actual lie. The same early-return exception as C1.3
applies (byte 11230 vs 16931).

**Verdict: enforced on the trigger reading; narrower-than-stated on the payload reading (and on the
early return). Amendments A1/A2 in §5.**

### C1.5 "pins, rc and `visibility_era` are computed from the true value"

Read from the code (`check()` computes `era_b`, `panic_setting`, every pin and `rc` before the
return; the bend only transforms the JSON value at return) and measured at the output level by
C1.2's deep compare: every key except `limine_version` is identical to the gate's, including `rc`
and `visibility_era` on the trigger spellings (`12.999999999.4` → era `12.9.5+`; `0.999999999.0` →
era `pre-12.9.5`, even though the lie reports `12.999999998.4`, which would be a different era if
the era were derived from the lie).

**Verdict: enforced.**

### C1.6 "the landed battery must move the field assertion the round-99 Frontier names"

Frontier quote re-read at the byte level (`grep -abo`): `corpus/README.md` byte **141199**
"`The X/Y **echo** legs have no spelling-targeted`"; `corpus/lessons/round-99.md:160` repeats it.
The premise that N09/N11 falsify `visibility_era` only is re-measured: `diff -u` of
`.ufo/waves/round-99/before/controls/bends/N09-y-era.py` and `N11-x-era.py` against the gate changes
the `visibility_era` line only. The r99 battery asserts the echo at
`tools/limine-pin-battery-r99.py:2181` (`if c.check_echo and not (got[8] == c.version and got[9] ==
"flag")`), and the three relevant families set `check_echo = True` (lines 1775, 1792, 1817).

Measured, `--runs 3`, both layouts (canonical = lane path; clone = `git clone --shared` at HEAD in
scratch, clone's own path used, no path prefixing):

```
LANDED GATE   x3 canonical: met 105/105, failed [],            cases 420, errors 0
LANDED GATE   x3 clone:     met 105/105, failed [],            cases 420, errors 0
N12-x-echo    x3 canonical: unmet 103/105, failed
                            ['EXPLICIT-VERSION-ECHO','REFUSAL-VERSIONS-9DIGIT'], errors 0
N12-x-echo    x3 clone:     unmet 103/105, same two families, errors 0
N13-y-echo    x3 canonical: unmet 104/105, failed ['REFUSAL-VERSIONS-9DIGIT-Y'], errors 0
N13-y-echo    x3 clone:     unmet 104/105, same family, errors 0
```

Named-family case counts (from `count-runs.py` and the same parse on the clone JSONs):

```
N12 x3: EXPLICIT-VERSION-ECHO [3,1]; REFUSAL-VERSIONS-9DIGIT [0,4]; REFUSAL-VERSIONS-9DIGIT-Y [4,0]
N13 x3: EXPLICIT-VERSION-ECHO [4,0]; REFUSAL-VERSIONS-9DIGIT [4,0]; REFUSAL-VERSIONS-9DIGIT-Y [0,4]
gate x3: all three named families [4,0]
```

The X lie trips all four X-family cases and one of the four explicit-echo versions; the Y lie trips
all four Y-family cases (both spellings × two layouts of the fixture). Receipts:
`c1-gate-r99-x3-canonical.json`, `c1-gate-r99-x3-clone.json`,
`c1-r99-N12-x3-canonical.json`, `c1-r99-N12-x3-clone.json`,
`c1-r99-N13-x3-canonical.json`, `c1-r99-N13-x3-clone.json`, `c1-summary.txt`,
`c1-count-runs-canonical.txt`.

**Verdict: enforced.**

### C1.7 r98 do-nothing control: is X really a delta, is Y blind?

```
r98 on N12 x3 canonical: unmet 104/105, failed ['EXPLICIT-VERSION-ECHO'], errors 0
r98 on N12 x3 clone:     unmet 104/105, failed ['EXPLICIT-VERSION-ECHO'], errors 0
r98 on N13 x3 canonical: met 105/105, failed [], errors 0
r98 on N13 x3 clone:     met 105/105, failed [], errors 0
```

Observed: the r98 control is **not blind** to the X lie (it kills the same bend on the r96
`EXPLICIT-VERSION-ECHO` family, one case of four: [3,1]); the r99 battery adds the
`REFUSAL-VERSIONS-9DIGIT` family on top (103/105). The plan's named limit ("the X echo leg is a
delta, not a flip") is exactly right. The Y leg is a true met-to-unmet closure: r98 reads met
105/105 on N13 and r99 reads 104/105. Receipts: `c1-r98-*-x3-{canonical,clone}.json`.

**Verdict: enforced; the pre-frozen limit is accurate, not understated.**

### C1.8 "`--selftest` without `--reference` PASS 5/5"

```
$ python3 tools/limine-pin-battery-r99.py --selftest
reference-gate      skipped (no --reference)
roster-literal     PASS families_passed=105
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
selftest PASS 5/5
```

The battery's `selftest()` appends the reference leg to `results` only when `--reference` is given;
the skipped leg is printed but excluded from the denominator (`sum(x[1])/len(results)`). So "PASS
5/5" is literally true and literally means 5 of 5 *non-reference* checks. Receipt:
`c1-battery-selftest-noref.txt`.

**Verdict: enforced, with the reading note that 5/5 excludes the owed reference leg by
construction.**

### C1.9 target numbers / kill clause

| frozen target line | observed | verdict |
|---|---|---|
| landed gate `met 105/105`, `failed_families []`, 0 error rows, x3 canonical + x3 clone | exactly | PASS |
| N13 `unmet 104/105` x3 both layouts, exactly `[REFUSAL-VERSIONS-9DIGIT-Y]`, 0 errors | exactly | PASS |
| N12 `unmet 103/105` x3 both layouts, exactly `[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]`, 0 errors | exactly | PASS |
| r98 N13 `met 105/105` x3 both layouts | exactly | PASS |
| r98 N12 `unmet 104/105` x3 both layouts exactly `[EXPLICIT-VERSION-ECHO]` | exactly | PASS |
| each bend's diff exactly one changed line | one `-`/`+` pair, one hunk | PASS |
| battery `--selftest` without `--reference` `PASS 5/5` | 5/5, reference skipped | PASS |
| void if any pinned instrument byte differs | all 16 manifest lines OK | PASS (not void) |

## 3. C2 — clause by clause

Frozen predicate quote (claims.json, byte 3059 begins "`RC-BEND-SPAN` as a LABEL SET"):

> `tools/check-registry-content-r100.py` binds RC-BEND-SPAN as a LABEL SET instead of a span
> string: one `VARIANTS` mention is tokenised into `N<digits>` and `N<digits>-N<digits>` tokens (a
> range expanded to its members) joined only by `,`, whitespace, `;`, `+`, `/` or the word `and`,
> and the declared set must equal the set of N-labels its tool's module-level `VARIANTS` keys
> carry. This closes the two round-99 named limits … `tools/check-registry-content-r99.py` … is the
> do-nothing control; every previously fail-closed shape must stay closed at set granularity.

### C2.1 "binds RC-BEND-SPAN as a LABEL SET instead of a span string"

Reading (a): the binding is set-valued (`{"set": True, "derive": "variant_labels"}`) rather than a
capture regex; (b) the observable consequence is that a cell spelling the same set differently is
accepted, and a cell stating a different set is rejected.

```
r100 binding: {'id':'RC-BEND-SPAN','row':'make-r96-bends','cell':5,'set':True,
               'derive':'variant_labels','tool':'tools/make-r96-bends.py'}
r99  binding: {… 'capture':'VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))(?![0-9,-])',
               'derive':'variant_span','unique':True …}
```

r99's deriver returns a *string* — `N01-N03` for contiguous keys, `N01,N03` otherwise
(`derive_variant_span`) — so any other spelling of the same set reads `RC-VALUE-MISMATCH`. Measured
on a plain comma list `VARIANTS N01,N02,N03` against keys `{N01,N02,N03}`:
`A-COMMA r100 rc=0 PASS | r99 rc=1 RC-VALUE-MISMATCH`. This is exactly "instead of a span string".

**Verdict: enforced.**

### C2.2 "one `VARIANTS` mention is tokenised"

```
A-LOWER (cell 'variants N01-N03')          r100 CELL-MISSING   (no `VARIANTS` mention)
A-EMPTY (cell 'VARIANTS')                  r100 CELL-MISSING   (no label stated)
A-TWO-MENTIONS ('…; VARIANTS N01,N02,N03') r100 CELL-AMBIGUOUS (mentions > 1)
RESTATED fixture                           r100 CELL-AMBIGUOUS
```

A cell with the word `VARIANTS` in trailing prose is also `RC-CELL-AMBIGUOUS` (fail-closed); a cell
with no mention is `RC-CELL-MISSING`. Exactly one mention is parsed; >1 is refused.

**Verdict: enforced.**

### C2.3 "tokens `N<digits>` / `N<digits>-N<digits>` (a range expanded to its members)"

```
A-DESC-RANGE  'VARIANTS N03-N01'   → CELL-MISSING (descending range refused)
A-WIDTH-MIX   'VARIANTS N01-N3'    → PASS (expanded N01,N02,N03 — first token's width)
A-UNPADDED    'VARIANTS N1-N3'     → VALUE-MISMATCH (set {N1,N2,N3} ≠ {N01,N02,N03})
A-RANGE-THEN-TO 'VARIANTS N01-N02 to N03' → CELL-MISSING
WIDE-RANGE    'VARIANTS N01-N02-N03' → CELL-MISSING
```

Reading note: `parse_label_set` expands `range(first, last+1)` with the *first* token's zero-padding
width; a mixed-width range is silently normalised to the first width (accepts `N01-N3`). A
descending range is refused. Not claimed, not harmful for the live cell.

**Verdict: enforced; the width rule is an unstated normalisation (limit L4).**

### C2.4 "joined only by `,`, whitespace, `;`, `+`, `/` or the word `and`"

Adversarial test (`c2-adversarial.txt`, `c2-dangling-separators.txt`):

```
A-PIPE           r100 rc=2 (the Markdown table parser splits the row on `|`; never reaches the tokeniser)
A-AMP            CELL-MISSING        A-DOTDOT CELL-MISSING     A-TO CELL-MISSING
A-DASH (em dash) CELL-MISSING        A-AND-NOSPACE CELL-MISSING
A-COMMA / A-COMMA-SPACE / A-AND-REPEAT / A-SEMI-COMMA-MIX / A-PLUS-NOSPACE /
A-SLASH-SPACE / A-TAB                    → PASS  (the six stated separators)
TRAIL-AND   'VARIANTS N01-N03 and'       → PASS   (also PASS on r99)
LEAD-AND    'VARIANTS and N01-N03'       → PASS   (r99: CELL-MISSING)
DOUBLE-SEMI 'VARIANTS N01; ; N02; N03'   → PASS   (r99: CELL-MISSING)
TWO-SEPARATORS 'VARIANTS N01 , ; N02 , / N03' → PASS (r99: CELL-MISSING)
TRAIL-SLASH 'VARIANTS N01-N03 /'         → PASS   (also PASS on r99)
```

Two readings: (a) every token is joined by a stated separator — true; (b) the cell may contain
*only* tokens and single stated separators — false, because empty tokens (leading, trailing,
adjacent or doubled separators) are skipped (`if not part: continue`). No wrong *set* can be
accepted this way (the set-equality check still runs), so the safety property is intact; the join
grammar is more permissive than stated.

**Verdict: wider-than-stated (grammar only; set equality unaffected). Amendment A3 in §5.**

### C2.5 "the declared set must equal the set of N-labels its tool's `VARIANTS` keys carry"

Both directions and the live table:

```
live make-r96-bends keys → derived labels ['N01','N02','N03','N04']; live cell 5 = 'r96 VARIANTS N01-N04'
live r100 --revision HEAD / ce73ccaf: status PASS bindings 7/7 findings 0 rows 165 / 163
live r99  --revision HEAD / ce73ccaf: status PASS bindings 7/7 findings 0
A-EXTRA-LABEL 'VARIANTS N01-N03,N09' → VALUE-MISMATCH (extra)
GAP-LIE (contiguous declared vs gap keys) → VALUE-MISMATCH (missing)
NON-N-KEY  (keys N01,N02,N03,X04; cell N01-N03)  → PASS on r100 and on r99
SUFFIX-KEY (keys N01a,N02,N03;   cell N01-N03)  → PASS on r100 and on r99
```

Both set directions are enforced against the *N-labelled* keys. Reading note: a key that carries no
`N<digits>` prefix (`X04`) is invisible to both checkers, and a key `N01a-…` contributes `N01`
(prefix match) — a latent fail-open shared with the r99 control, not introduced by r100. Limit L5.

**Verdict: enforced as literally stated; the unlabelled-key class is unproven (L5).**

### C2.6 "This closes the two round-99 named limits"

Limit 1 (`corpus/README.md` bytes 1281-1282): "the capture's alphabet is still `N<digits>` with no
space token."

```
SEP-SPACE 'VARIANTS N01 N02 N03'   r99 RC-CELL-MISSING → r100 PASS
```

Limit 2 (README bytes 1281-1282): "a registry cell that legitimately states two spans in one cell
must be rewritten to one span."

```
UNION 'VARIANTS N01-N02 and N04-N05' (keys N01,N02,N04,N05)  r99 RC-VALUE-MISMATCH → r100 PASS
```

Both named limits are closed by the measured flip. The six frozen acceptance cells all reproduce:

```
fixture        r99 finding              r100
SEP-SPACE      RC-CELL-MISSING          PASS
SEP-SEMICOLON  RC-CELL-MISSING          PASS
SEP-AND        RC-VALUE-MISMATCH        PASS
SEP-SLASH      RC-CELL-MISSING          PASS
SEP-PLUS       RC-CELL-MISSING          PASS
UNION          RC-VALUE-MISMATCH        PASS
```

**Verdict: enforced.**

### C2.7 "every previously fail-closed shape must stay closed at set granularity"

```
LETTER     r100 RC-CELL-MISSING        PROSE      r100 RC-CELL-MISSING
UNION-LIE  r100 RC-VALUE-MISMATCH      HYBRID     r100 RC-VALUE-MISMATCH
RESTATED   r100 RC-CELL-AMBIGUOUS      GAP        PASS on both checkers
```

Cross-check of the two instruments' selftest tables: r99's 16 `SELFTEST_CASES` names all appear in
r100's 25 (+ `ancestor` = 26), with **one expectation change**: `span-hybrid` expected
`RC-CELL-MISSING` on r99 and expects `RC-VALUE-MISMATCH` on r100. The shape still fails closed; the
id sharpened because the set is now parsed and compared instead of failing to capture. `span-cell`
(`N01-N05` vs keys `N01-N03`), `span-gap-lie`, `span-restated` and every non-span binding keep their
expectations. One r99 *fail-open* is now closed: `VARIANTS N01-N03 (the three)` read PASS on r99 and
reads `RC-CELL-MISSING` on r100 (`A-TRAIL-PROSE`).

**Verdict: enforced (one fail-closed id changed, still a finding; one r99 fail-open closed).**

### C2.8 selftest, live table, coverage

```
r100 --selftest → selftest PASS 26/26   (receipt r100-selftest.txt)
r99  --selftest → selftest PASS 17/17   (receipt r99-selftest.txt)
live r100 --revision HEAD    → status PASS bindings 7/7 findings 0 rows 165
live r100 --revision ce73ccaf→ status PASS bindings 7/7 findings 0 rows 163
live r99  --revision HEAD / ce73ccaf → status PASS bindings 7/7 findings 0
```

**Verdict: enforced.**

## 4. Named limits attacked (what the round does not prove)

| limit attacked | measurement | result |
|---|---|---|
| "the X echo leg is a delta, not a flip" | r98 on N12 x3 both layouts | true — r98 kills it on `EXPLICIT-VERSION-ECHO` ([3,1]); only the +1 `REFUSAL-VERSIONS-9DIGIT` family is new |
| "`--selftest --reference` is not run this round" | `--selftest` prints `reference-gate skipped (no --reference)`; no `--reference` output exists in the dev receipts | true — the owed leg is untouched; 5/5 excludes it |
| "`N01 through N03` stays a finding" | PROSE and A-TO fixtures | true — `RC-CELL-MISSING` |
| "a letter-suffixed token stays a finding" | LETTER (`N01a-N03`) | true — `RC-CELL-MISSING` |
| "the capture still does not bind N labels outside VARIANTS keys" | NON-N-KEY / SUFFIX-KEY probes | true, and shared with r99 (see L5) |

Additional things the round does **not** prove (plain):

1. **The main-return-only lie.** Both bends leave the `CANNOT-EVALUATE` early return's
   `limine_version` truthful (bytes 11230 vs 16931). "Exactly when" is therefore true of the main
   return and false of the field as a whole. No battery family pairs an unreadable conf with a
   cap-version, so the measured readings are unaffected.
2. **The N13 payload is a constant, not a component substitution.** For `0.999999999.0` the reported
   first component changes too; the trigger is still the second component.
3. **The blanket lie-kind wrapper.** The r99 selftest's 14 `LIE_KINDS` (including the blanket
   `limine-version` and `visibility-era` wrappers) are still only exercised by `--selftest
   --reference`, which is not run. The new bends do not replace that coverage.
4. **The full `--reference` leg is absent.** `PASS 5/5` is five non-reference checks; the reference
   gate plus fourteen lie wrappers are unmeasured this round.
5. **The r100 generator's own registry row is unbound.** `RC-BEND-SPAN` binds
   `make-r96-bends` cell 5 only; the new row's cell `r100 VARIANTS N12,N13` (SKILL.md byte 1625473,
   `grep -abo`) is not parsed by any binding — coverage checks row presence, not span content.
6. **Pass-key blindness (shared with r99).** `VARIANTS` keys without an `N<digits>` prefix are
   invisible; a key renamed `N01a` still derives `N01`.
7. **Unbounded range expansion.** `parse_label_set` materialises `range(first, last+1)` with no cap;
   a typo like `N01-N999999999` would hang/OOM the checker. Not claimed, not measured (code-read).
8. **Degenerate separators.** Leading/trailing/adjacent separators are accepted (§C2.4).
9. **Clone-layout provenance was not committed before the freeze.** The dev receipts contain one
   canonical run per leg; the x3 clone legs are measured here, not by the round's freeze receipts.
10. **Harness-fault warning (live).** The L1's working-tree QUALITY 142 records that the first clone
    receipts for these legs read `0/105` because of a `$CLONE/$ABS_PATH` path prefix. This seat's
    clone legs used the clone's own path (`clone/…` with cwd in scratch), verified the clone top
    level, and read the frozen sets; no `0/N` run is cited here.

## 5. Amendments for the plan's amendment slot (exact sentences)

**A1 (C1, narrower-than-stated — required).**
> Each bend falsifies the **main (post-parse) JSON return's** `limine_version` exactly when the named
> component is the cap; the `CANNOT-EVALUATE` early return that also carries `limine_version`
> (unreadable conf) is not bent and echoes the true value.

**A2 (C1, N13 payload reading — required if the sentence is read as a component substitution).**
> `N13-y-echo`'s replacement is the fixed string `12.999999998.4`, so for the `0.999999999.0`
> spelling the reported first component also changes; the trigger, not the payload, is the second
> component.

**A3 (C2, wider-than-stated — required if the join grammar is stated as "only").**
> The tokeniser skips empty tokens, so a cell with a leading, trailing, adjacent or doubled
> separator (`VARIANTS and N01-N03`, `VARIANTS N01-N03 and`, `VARIANTS N01; ; N02; N03`) reads
> `PASS`; only a non-empty part that is not an `N<digits>`/`N<digits>-N<digits>` token is
> `RC-CELL-MISSING`.

**A4 (C2, optional sharpening, no claim change).**
> `RC-BEND-SPAN` compares the declared set against the `N<digits>`-prefixed labels of the bound
> tool's literal `VARIANTS` keys; keys without that prefix are not bound, and a mixed-width range is
> normalised to the first token's zero-padding width.

## 6. Commands run (raw, trimmed) and receipts

All commands run with cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` unless noted; battery
work dirs under `/fast/scratch/hyaku/tsukuroi-r100/CriticClaims/…`; JSON receipts under
`.ufo/waves/round-100/w1/CriticClaims/`.

```
sha256sum -c .ufo/waves/round-100/before/instruments.sha256                  → 16 × OK
python3 tools/check-registry-coverage.py --revision 69474c55                 → PASS 165/165
python3 tools/check-registry-coverage.py --revision ce73ccaf                 → PASS 163/163
python3 tools/check-registry-content-r100.py --revision HEAD --json …        → PASS 7/7 findings 0
python3 tools/check-registry-content-r100.py --revision ce73ccaf --json …    → PASS 7/7 findings 0
python3 tools/check-registry-content-r99.py  --revision HEAD --json …        → PASS 7/7 findings 0
python3 tools/check-registry-content-r99.py  --revision ce73ccaf --json …    → PASS 7/7 findings 0
python3 tools/check-registry-content-r100.py --selftest                      → PASS 26/26
python3 tools/check-registry-content-r99.py  --selftest                      → PASS 17/17
python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 --work … --json …
python3 tools/limine-pin-battery-r99.py --gate .ufo/…/N12-x-echo.py --runs 3 …
python3 tools/limine-pin-battery-r99.py --gate .ufo/…/N13-y-echo.py --runs 3 …
python3 tools/limine-pin-battery-r98.py  --gate .ufo/…/N12-x-echo.py --runs 3 …
python3 tools/limine-pin-battery-r98.py  --gate .ufo/…/N13-y-echo.py --runs 3 …
git clone --shared <lane> $SCRATCH/clone                                     → clone toplevel = $SCRATCH/clone, HEAD 69474c55
<same four battery legs with --gate clone/…>                                 → see C1.6/C1.7
python3 .ufo/waves/round-95/before/controls/count-runs.py <json> --family …  → see c1-count-runs-canonical.txt
python3 .ufo/waves/round-100/before/dev/make-fixtures.py $SCRATCH/fx         → 12 fixture trees
for T in <12 tags>: python3 tools/check-registry-content-r{100,99}.py --root $SCRATCH/fx/$T
python3 $SCRATCH/adv.py                                                      → c2-adversarial.txt
python3 $SCRATCH/dangling.py                                                 → c2-dangling-separators.txt
python3 $SCRATCH/keys.py                                                     → c2-keyedge.txt
python3 $SCRATCH/fieldcmp.py                                                 → c1-fieldcmp.txt
python3 tools/limine-pin-battery-r99.py --selftest                           → c1-battery-selftest-noref.txt
diff -u tools/check-limine-pins.py .ufo/…/controls/bends/{N12,N13}.py        → one hunk each
grep -abo '"limine_version": limine_version,' tools/check-limine-pins.py     → 11230, 16931
grep -abo 'RC-BEND-SPAN as a LABEL SET' .ufo/waves/round-100/claims.json     → 3059
grep -abo 'The X/Y \*\*echo\*\* legs have no spelling-targeted' corpus/README.md → 141199
python3 tools/make-r100-bends.py (scratch copy)                              → two bends, byte-identical
<perturbed scratch gate> (scratch copy)                                      → "matched 0 times, expected 1", rc 1
```

Receipts under `.ufo/waves/round-100/w1/CriticClaims/`:
`coverage.txt`, `r100-selftest.txt`, `r99-selftest.txt`, `live-r100-HEAD.json`, `live-r100-ce73ccaf.json`,
`live-r99-HEAD.json`, `live-r99-ce73ccaf.json`, `c1-gate-x1-timing.json`,
`c1-gate-r99-x3-canonical.json`, `c1-gate-r99-x3-clone.json`, `c1-r99-N12-x3-canonical.json`,
`c1-r99-N12-x3-clone.json`, `c1-r99-N13-x3-canonical.json`, `c1-r99-N13-x3-clone.json`,
`c1-r98-N12-x3-canonical.json`, `c1-r98-N12-x3-clone.json`, `c1-r98-N13-x3-canonical.json`,
`c1-r98-N13-x3-clone.json`, `c1-summary.txt`, `c1-count-runs-canonical.txt`,
`c1-battery-selftest-noref.txt`, `c1-fieldcmp.txt`, `c1-reflie-probe.txt` (see §7),
`c2-fixtures-rerun.txt`, `c2-adversarial.txt`, `c2-dangling-separators.txt`, `c2-keyedge.txt`.

## 7. Owed-leg probe (informational, not part of the claim)

`c1-reflie-probe.txt`: the frozen battery's `run_battery` was exercised directly on the landed gate
(reference leg) and on the two r99 lie wrappers (`limine-version`, `visibility-era`) built with the
battery's own `LIE_WRAPPER`, to say whether the owed `--reference` leg would pass. This does not
substitute for `--selftest --reference` (the other 12 lie kinds are not run here) and is not offered
as a claim measurement.

`c1-reflie-probe.txt`:

```
reference-gate           verdict=met families=105/105 failed=[]
lie-limine-version       verdict=unmet families=93/105 failed=['AUTO-ERA-A','AUTO-ERA-B','AUTO-PROBE-FAIL',
  'AUTO-PROBE-SHAPES','EXPLICIT-VERSION-ECHO','EXTRA-COMPONENT','LEADING-ZERO-NORMALIZE',
  'REFUSAL-VERSIONS','REFUSAL-VERSIONS-10DIGIT','REFUSAL-VERSIONS-9DIGIT','REFUSAL-VERSIONS-9DIGIT-Y',
  'REFUSAL-VERSIONS-9DIGIT-Z']
lie-visibility-era       verdict=unmet families=95/105 failed=['AUTO-PROBE-FAIL','AUTO-PROBE-SHAPES',
  'EXPLICIT-VERSION-ERA','EXTRA-COMPONENT','LEADING-ZERO-NORMALIZE','REFUSAL-VERSIONS',
  'REFUSAL-VERSIONS-10DIGIT','REFUSAL-VERSIONS-9DIGIT','REFUSAL-VERSIONS-9DIGIT-Y','REFUSAL-VERSIONS-9DIGIT-Z']
```

Reading: the reference gate reads met 105/105 on the landed bytes, and the two lie kinds r99 added
still read unmet at the same counts the r99 lesson records (93/105, 95/105). The other twelve
`LIE_KINDS` are not run here, so this does **not** discharge the owed `--selftest --reference` leg;
it shows the two field lies the Frontier named are still killed when wrapped around the landed gate.

## 8. Final verdict

The frozen **measured targets** are met on every run and both layouts (C1) and on every frozen
fixture, live table and selftest (C2). The frozen **predicate sentences** overstate two things
(narrow) and one C2 grammar clause (permissive): the C1 "exactly when" is main-return-only, the N13
payload is a constant, and the C2 join grammar tolerates empty tokens. None changes a frozen target
number, a family set, an error-row count or a fixture reading. Amendments A1-A3 are the smallest
wording changes that make the sentences literally true.

{"seat":"CriticClaims","verdict":"findings","notes":"C1 targets met on x3 canonical+clone (gate 105/105, N12 103/105 [EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT], N13 104/105 [REFUSAL-VERSIONS-9DIGIT-Y], r98 control N12 104/105 [EXPLICIT-VERSION-ECHO], N13 met; one-line diffs; selftest 5/5 with reference skipped). C2 targets met (live PASS 7/7 at ce73ccaf and HEAD, six acceptance cells PASS-before-FAIL, five fail-closed + GAP, selftest 26/26 vs 17/17). Clause-level overstatements: C1 'exactly when' is main-return-only (CANNOT-EVALUATE early return echoes truth at bytes 11230 vs 16931); N13 payload is fixed 12.999999998.4 so 0.999999999.0 changes X too; C2 tokeniser skips empty tokens (leading/trailing/adjacent separators PASS). Amendments A1-A3 recorded. Not proven: full --reference leg (14 lie kinds), r100 row span unbound, non-N VARIANTS keys invisible, unbounded range expansion."}
