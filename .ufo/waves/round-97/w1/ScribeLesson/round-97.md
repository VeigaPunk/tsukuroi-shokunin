# Round 97 lesson — tsukuroi lane (DRAFT by seat ScribeLesson; the L1 integrates)

Draft only. Every number below carries the command that produced it and a receipt under
`.ufo/waves/round-97/w1/ScribeLesson/`. Numbers this seat did not run are cited to the seat report
that ran them, and are marked with that seat's name; nothing here is adopted on trust.

Lane: **tsukuroi** (operability + freshness). Round **97** (attempt 1). Pre-round tip
`f48d16428d8bb92fd6cf546a745bff5b624e3f18`; freeze `a57e88cd57f30bae206d908b534508d9463bf734`.

**C1 (depth 8, tied lowest).** `tools/limine-pin-battery-r97.py` carries two families beyond the r96
roster (103 → 105) — `REFUSAL-VERSIONS-9DIGIT-Z` (the Z component at the published 1-9-digit cap,
both eras) and `LEADING-ZERO-NORMALIZE` (leading-zero components accepted and era-selected by
`int()` value) — each killed by its own one-clause bend (`N05-z-cap-8`, `N06-leading-zero-reject`),
which the r96 battery is blind to.

**C2 (freshness 9).** `tools/check-registry-content.py` re-derives seven frozen `SKILL.md` registry
cell values from the bytes of the tool each row names; it reads PASS at the landed revision and FAIL
on a content-only doctored table that `tools/check-registry-coverage.py` still certifies PASS
154/154.

---

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

Pins under `ScribeLesson/pins/` (fetched by this seat with `curl -sSL`, 2026-11-08); digests
`ScribeLesson/receipts/01-gate-pins.sha256.txt`; the located-quote byte check
`ScribeLesson/receipts/05-gate-quote-bytes.txt`; the rejections
`ScribeLesson/receipts/07-gate-reject.txt`; the two re-opens
`ScribeLesson/receipts/08-gate-reopens.txt`. The row S392's own fetch is ScoutSources'
(`w1/ScoutSources/pins/int-functions.html`, sha256 `d92580dd…`); **this seat re-fetched the same URL
and got byte-identical bytes** (`cmp` between the two pins → identical), so the two receipts agree.

| row | URL opened 2026-11-08 | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S392 (new; the round's source) | https://docs.python.org/3/library/functions.html (301 → `/3/builtins/functions.html`) | A | "have leading zeros, be surrounded by whitespace," (17 words, byte **157767** of the 331022-byte pin, sha256 `d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7`); the `id="int"` anchor at byte **153202** | **admit** — the documented string form of `int(x, base)`: a component with leading zeros is a legal decimal spelling that `int()` normalizes, which is exactly the behaviour `LEADING-ZERO-NORMALIZE` exercises. The same page states the contrast "Base 0 also disallows leading zeros:" (byte **159310**), so the explicit-base reading is the right one. |
| S389 (re-open) | https://docs.python.org/3/library/stdtypes.html | A | pinned bytes byte-identical to the r96 pin: 815447 bytes, sha256 `6bf2ce2b…` | **admit** (re-open, **no drift**) — the 4300-digit default the per-component 1-9-digit cap sits under. |
| S391 (re-open) | https://docs.python.org/3.15/library/sys.html | A | pinned bytes byte-identical to the r96 pin: 280632 bytes, sha256 `a7e00587…` | **admit** (re-open, **no drift**) — the configured default of the digit limit. |
| rejected candidate | https://man.archlinux.org/man/python.1 (302 → `/man/python3.14.1.en`) | — | HTTP 200, 41788 bytes, sha256 `11c40ea1…`, title "python3.14(1) — Arch manual pages" | **reject** — the interpreter's command-line manual. A text scan of the fetched bytes finds **0** occurrences of "leading zero", "int(", "base 10" and "radix" (the single "decimal" hit is `PYTHONHASHSEED`'s range); it states no behaviour about `int()`'s string form, so it cannot ground C1's family or S392's claim. It is also a *moving* target: `python.1` is a version alias, not a pinned locator. |

### Gate finding — the landed S392 row's two offsets are CHARACTER offsets, not byte offsets

The row as landed reads *"`int` heading (`id="int"` at byte 153028) … quoted phrase at byte 157622"*.
Re-read against the very pin the row names (sha256 `d92580dd…`, 331022 bytes — the sha256 and byte
count in the row are **correct**):

| S392 cites | read as BYTE offset | read as CHARACTER offset (utf-8 decoded) |
|---|---|---|
| `id="int"` at 153028 | `b'an class="pre">builtins.input/result</span></code>\nwith the '` — **ABSENT** | `'<dt class="sig sig-object py" id="int">\n<span class="pr'` — lands on the element carrying the id (the `id="int"` attribute itself is at char 153058) |
| quoted phrase at 157622 | `b'e"><span class="pre">+</span></code> or <code class="docutil'` — **ABSENT** | `'have leading zeros, be surrounded by whitespace,\nand ha'` — lands **exactly** on the quoted phrase |

Commands: `python3 -c "b=open('pins/functions.html','rb').read(); …"` — receipt
`ScribeLesson/receipts/05-gate-quote-bytes.txt`; the sibling seat measured the same fact
(`w1/ScoutSources/report.md` §1c). The r96 rows on the same table **are** byte offsets and land
exactly when read as bytes (`grep -bo 'id="sys.int_info.default_max_str_digits"' pins/sys315.html` →
157525; slicing there yields `id="sys.int_info.default_max_str_digits">`), so byte offsets are the
table's convention and S392 departs from it.

**Route to the L1 (a decision, not a blocker):** restate S392's anchor as byte offsets `153202`
(`id="int"`) and `157767` (the quoted phrase), or state the unit as characters explicitly. This seat
edited nothing under `corpus/` (out of scope). This is the r96 S390→S391 defect class (a locator
whose stated unit does not survive re-reading) recurring one row later, on the very table the round's
C2 checker now re-derives cell values from.

### Census (frozen command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`)

| leg | command | exit | rows | findings |
|---|---|---|---|---|
| **before** (pre-round tip `f48d1642`, extracted read-only with `git archive f48d1642 \| tar -x -C <scratch>/before-fleet/tsukuroi-shokunin`; the fleet's `shokunin.conf` copied in so the lane resolves) | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <scratch>/before-fleet tsukuroi` | **0** | **391** (`grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` in the before tree → 391; `git show f48d1642:corpus/SOURCES.md \| grep -cE …` → 391) | 0 E, 57 W04 + 1 W01 (receipt `ScribeLesson/receipts/03-census-before.txt`) |
| **after** (the live fleet root, with the L1's row S392 present in the worktree) | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | **0** | **392** (`grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → 392) | 0 E, 57 W04 + 1 W01 (receipt `ScribeLesson/receipts/02-census-after.txt`) |

Row counts and the census exits: `ScribeLesson/receipts/04-sources-rows.txt`. Rows added by tier:
**one A** (S392). Rows touched old→new in place: none — S389 and S391 were re-opened only, their
`status` and `used-by` unchanged.

---

## Mistakes

**R97-Y-DOCSTRING-ERA** — class: **instrument text vs the behaviour the family actually tests.**
Round 96's `fam_refusal_versions_9digit_y` docstring asserted a discrimination the family does not
have: *"one that reads the era from `X` alone answers era B for `0.999999999.0` and fails."* An X-only
era reader answers **era A** for `0.999999999.0` — which is the *correct* era — and therefore
**passes** that family 4 of 4; the reader is caught elsewhere, by `EXPLICIT-VERSION-ERA` on its
`12.9.4` row.

- **evidence pointer:** r96 `w1/CriticClaims/report.md` §1 F-4 (the finding that named it), with the
  measurement at `w1/CriticClaims/receipts/era-reader-mutant.txt` — `REFUSAL-VERSIONS-9DIGIT-Y` all 4
  cases `case_ok=true` (era "12.9.5+" for `12.999999999.4`, era "pre-12.9.5" for `0.999999999.0`),
  while `EXPLICIT-VERSION-ERA`'s `12.9.4` case reads `case_ok=false` (`got era "12.9.5+"`, want
  `prompt`).
- **captured-by:** **QUALITY 122** (`corpus/QUALITY.md:240`, R85-MUST-HAS-CONTROL) — *"a declared
  discrimination property names its near-miss control"* — which the docstring was never checked
  against: the sentence attributes a discrimination to a family, and nothing in the lane's gate
  required the sentence's own control to be named or demonstrated.
- **fix:** the successor instrument `tools/limine-pin-battery-r97.py` carries a `LIMIT` paragraph in
  the same docstring that states what the family does **not** test (an era reader that looks at X
  alone is not caught by this family; it is caught by `EXPLICIT-VERSION-ERA`), and says the r96
  sentence was wrong and that the family and its expectation are unchanged.

**Demonstrated red/green pair** (receipt `ScribeLesson/receipts/06-mistake-redgreen.txt`; red rev
`f48d1642`, green rev `a57e88cd`):

```
$ git show f48d1642:tools/limine-pin-battery-r96.py | grep -c 'answers era B for'   -> 1   # RED: the false claim is there
$ git show a57e88cd:tools/limine-pin-battery-r97.py | grep -c 'answers era B for'   -> 0   # GREEN: it is gone
$ git show f48d1642:tools/limine-pin-battery-r96.py | grep -c 'LIMIT (r96 CriticClaims'  -> 0  # RED: no correction
$ git show a57e88cd:tools/limine-pin-battery-r97.py | grep -c 'LIMIT (r96 CriticClaims'  -> 1  # GREEN: the correction is there
```

**One command in the item does not discriminate, and the run wins.** The seat item named
`grep -c 'LIMIT (r96 CriticClaims F-4'` as the green signal. Read literally it returns **0 on both
revisions**: the sentence is line-wrapped in the source, so the one-line pattern cannot match it —
the raw bytes are `LIMIT (r96 CriticClaims\n    F-4, corrected here in r97): …`. The instrument was
not edited and no retry-to-pass was performed. The discriminating forms are the single-line prefix
above (0 → 1) and the cross-line form `grep -cPzo 'LIMIT \(r96 CriticClaims\s+F-4'` (0 → 1). Both
are in the receipt. **The lesson for the next round: a red/green check on a line-wrapped sentence
must anchor on a token that is not split across lines, or it will read "0 = pass" on both sides.**

**Residual — and it was closed in place, mid-wave, by the L1.** When this seat first measured it the
false sentence still stood in the *live, registry-listed* r96 instrument
`tools/limine-pin-battery-r96.py:1776` (`grep -rn 'answers era B for' tools/` → one hit), because
the correction had landed only in the successor file: C1's target binds the do-nothing control as
*"byte-identical to the r96 landed bytes"*, and the r96 battery still has an operative `SKILL.md`
row (`SKILL.md:5938`) and two cells bound by `tools/check-registry-content.py`
(`RC-ROSTER-VERDICT`, `RC-ROSTER-PINNED`), so a reader of the registered r96 tool would still read
the false sentence. `w1/ScoutSources/report.md` §3 routed it with three options; the L1 took the
in-place option. Re-read at this seat's write time (receipt
`ScribeLesson/receipts/10-r96-battery-in-place-correction.txt`):

```
$ git diff -- tools/limine-pin-battery-r96.py
-    both; one that applies `<= 8` to Y refuses the cap member and fails, and one that reads the era
-    from X alone answers era B for `0.999999999.0` and fails."""
+    both; one that applies `<= 8` to Y refuses the cap member and fails. LIMIT (r96 CriticClaims
+    F-4, corrected in r97): an era reader that looks at X alone is NOT caught by this family -- X=12
+    and X=0 answer era B and era A correctly for these two members; that reader is caught by
+    `EXPLICIT-VERSION-ERA` on its `12.9.4` row. The sentence this docstring carried is withdrawn; the
+    family and its expectation are unchanged. Bytes of the r96 landed tool are re-derivable at
+    `f48d1642:tools/limine-pin-battery-r96.py` (sha256 f06d90ae...)."""
$ grep -c 'answers era B for' tools/limine-pin-battery-r96.py        -> 0
$ grep -c 'LIMIT (r96 CriticClaims' tools/limine-pin-battery-r96.py  -> 1
$ sha256sum tools/limine-pin-battery-r96.py                           -> 0d98b5bd0ac0ce68671b7355256c41aec636b7842be1a6069b707e6954007eab
$ git show HEAD:tools/limine-pin-battery-r96.py | sha256sum          -> f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba
$ sha256sum .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py -> f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba
```

Two consequences the L1 must record, both visible above:

1. **The correction is docstring-only** — the diff touches one docstring; the family and its
   expectation are unchanged, and the frozen `do-nothing-battery-r96.py` control copy still hashes
   `f06d90ae…`, so C1's do-nothing leg and the r97 roster reading are untouched. But the *live* r96
   battery moved `f06d90ae…` → `0d98b5bd…`, so **`.ufo/waves/round-96/before/instruments.sha256` no
   longer holds for that file in the worktree** (`sha256sum -c
   .ufo/waves/round-96/before/instruments.sha256` → `tools/limine-pin-battery-r96.py: FAILED`). Its
   scored bytes remain re-derivable at `f48d1642:tools/limine-pin-battery-r96.py` (`f06d90ae…`),
   which the new docstring itself names. This is the same manifest-relation pattern r96 used for its
   own r95 docstring edits (r96 lesson §"Relation to the r95 freeze manifest").
2. **C1's do-nothing byte-identity clause is now bound to the control copy, not to the live file.**
   The frozen clause reads *"`.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py`, sha256
   `f06d90ae…`, byte-identical to the r96 landed bytes"*; the control copy still is `f06d90ae…` and
   HEAD still is `f06d90ae…`, so the clause as written still holds at HEAD — but the live
   `tools/limine-pin-battery-r96.py` is no longer that file's byte twin. The lesson should state the
   clause as bound to the **control copy** (which is what the claim reads), so a future docstring
   repair of the live r96 tool does not silently falsify it.

The r97 successor file carries the same correction with a slightly different wording
(`corrected here in r97` vs `corrected in r97`) — a wording difference only; both paragraphs state
the same limit and both leave the family and its expectation unchanged.

### The same class recurs one family later, in the same round

**R97-LZ-DOCSTRING-TEXT** — the r97 battery's own `fam_leading_zero_normalize` docstring carries an
illustrative sentence that is wrong about *which member* a text comparison breaks: it says a raw-text
compare against `12.9.5` orders "`000000012.9.4` as era B (wrong)". Measured, a text comparison
orders `12.09.4` and `000000012.9.4` as era A (correct) and `12.000000009.000000005` as era A where
`int()` gives era B — so the sentence names the wrong member and the *single* discriminating member
is `12.000000009.000000005`. Evidence: `w1/CriticClaims/report.md` §C1 "Docstring defect" and its
receipts `05-zera-*` / `06-lztext-*` (the text-comparison gate reads `104/105` unmet with exactly
`[LEADING-ZERO-NORMALIZE]`, 0 error rows, 3 runs). Captured-by: none yet — QUALITY 122 would catch it
if a docstring were read against its own near-miss control, which nothing does today. Fix: the frozen
bytes are not edited this round (the C1 void clause); the sentence is corrected in the r98 successor
with its own manifest, the same treatment r96 gave its Y-family sentence. Recorded as amendment A6
in `.ufo/waves/round-97/before/plan-amendments-r97.md`. **The pattern the two rounds together show:
a docstring's *illustrative* sentence is the least-checked sentence in an instrument, and it is
wrong twice in two consecutive rounds.**

---

## Counter-attack scoreboard

The proposal "track how many attack arms the wave fielded, how many survived, and which class beat
it" was adopted as QUALITY 115 at round 82 and revived at r96. This round practises it again. Cells
read from the seat reports that exist at this seat's write time; a seat with no report yet is named
`not reported` rather than filled in.

### C1 (depth 8) — the battery's roster and its two bends

| arm | what was fielded | survived? | which class beat it | source |
|---|---|---|---|---|
| bends (one-clause) | `N05-z-cap-8` (the Z bound bent to `<= 8`) and `N06-leading-zero-reject` (a component whose first digit is `0` refused) — 2 arms | **0 survived** — both killed at their frozen families: N05 `103/105`, `failed_families [LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 6 non-null error rows/run (4 Z + 2 LZ); N06 `104/105`, `failed_families [LEADING-ZERO-NORMALIZE]`, 4 error rows/run; every non-null row is the bend's own `bad-output: JSONDecodeError rc=64` refusal. Reproduced in the canonical lane **and** a `git clone --shared`, 3/3 runs each | the **one-clause bend** class; the frozen target's exact family set was reproduced, not a wider one | `w1/ExecBend/report.md` §4-5 (per-bend per-layout table) — independently re-counted by `w1/ReviewBattery/counted-N05-count.txt` / `counted-N06-count.txt` |
| mutants / own gates (one-clause, in-scratch) | 5 arms under `w1/ReviewBattery/`: `attack1-eraA-pin` (`era_b` forced False for exactly `(12, 9, 999999999)`), `attack1-eraA-field` (pins correct, the reported `visibility_era` string lies for exactly the Z boundary tuple), `attack2-echo-norm` (echoes `12.09.4` / `000000012.9.4` as `12.9.4`), `attack3-refuse-allzero` (refuses only the all-zero member), `attack4-constant` (answers `met` for every case) | **3 killed, 2 survived.** `attack1-eraA-pin` **killed** (3× `104/105 unmet`, `failed [REFUSAL-VERSIONS-9DIGIT-Z]`, 0 error rows — it answers `prompt` where the pin expectation is `panic`); `attack3-refuse-allzero` **killed** (3× `104/105 unmet`, `failed [LEADING-ZERO-NORMALIZE]`, **exactly 1** non-null error row per run, the rc-64 refusal class — the all-zero member is hit exactly once in every run because `LEADING_ZERO_VALUES` has 4 members cycled by `c.index % 4` over 4 cases, 12 builds over `--runs 3`); `attack4-constant` **killed** (3× `0/105 unmet`, all 105 families failed, 0 error rows — a constant gate is reported as a pin/verdict mismatch, not a transport error). **SURVIVED:** `attack1-eraA-field` (3× `105/105 met`) — only the `visibility_era` *string* lies; the only family that asserts that field is `EXPLICIT-VERSION-ERA`, whose members (`12.9.4`, `12.9.5`, `12.9.6`, `999999999.9.9`) never include the Z tuple; `attack2-echo-norm` (3× `105/105 met`) — the only family that asserts the echo is `EXPLICIT-VERSION-ECHO`, whose members contain no leading-zero spelling | the **uncertified-field** and **uncertified-echo** classes: the two new families bind *acceptance* and the *pin consequence* (era's own answer), not the `visibility_era` string and not the echoed spelling. A claim that reads "answered from the era the whole tuple selects" as including the field string or the echo would be **wrong** — the ledger names both as Limits, not predicate cuts | `w1/ReviewBattery.md` §4 (per-arm verdicts with the exact substitutions and the arithmetic) and §5 (the two `falsifies-wording` ledger rows); receipts `attack-1.txt`, `attack-1-field.txt`, `attack-2.txt`, `attack-3.txt`, `attack-4.txt`, `summaries.txt`, `attack-derivation.txt` |
| load-bearing-ness (own gates, `w1/CriticClaims`) | 2 arms: a Z-era-blind gate (`era_b = … and version[2] != 999999999`) and an LZ text-compare gate (`era_b = version >= "12.9.5"`) | both **killed** (3× `104/105` each, exactly the one family), 0 error rows — and each kills only **one** member: Z's era-A member and the second case of each are acceptance redundancy; LZ's only discriminating member is `12.000000009.000000005` | the **acceptance-redundancy** class: a family of 4 members can be load-bearing on 1 and redundant on 3 — the frozen predicate's "each accepted with its era's own answer" is checked by fewer members than the roster suggests | `w1/CriticClaims/05-zera-count.txt`, `06-lztext-count.txt`, `15-scope-quant.txt` |
| do-nothing (blindness control) | the r96 battery (`f06d90ae…`, byte-identical to the r96 landed bytes) on the landed gate and on both bends — 9 runs | **the control survives the new families at roster level** (3× `103/103 met`, 0 error rows, on all three gates) — that is the intended blindness receipt. **But at instrument level it is not blind to the leading-zero class**: its `--usage-check` mode sends `12.09.4` and `00.00.00` (both `want_rc 0`) and reads `unmet` on `N06-leading-zero-reject`; the Z class is unsampled by both legs | the **instrument-level / roster-level split**: the leading-zero class was sampled *before* this round at instrument level and is new at roster level only (amendment A3) | `w1/ExecDoNothing/report.md` §2-4 (F1) |

### C2 (freshness 9) — the registry-content checker

| arm | what was fielded | survived? | which class beat it | source |
|---|---|---|---|---|
| mutants (one-fault) | 8 one-fault mutants M01-M08 against `tools/check-registry-content.py` — M01 constant derivation, M02 the mismatch branch deleted, M03 `parse_tally` → `(0,0)`, M04 `RC-ROW-MISSING` removed, M05 `derive_roster_size` → constant 103, M06 first heading instead of the unique highest, M07 the `--revision` ancestor check removed, M08 `derive_variant_span` compares only the first label | **6 killed, 2 survived.** M07 **SURVIVED** — unreachable from `--selftest` by construction; its non-equivalence is proved by a non-ancestor revision leg (pristine rc 2, M07 rc 0). M08 **SURVIVED** — a genuine hole in the checker's own tests: every `VARIANTS` label set it meets is contiguous, so the comma branch is never exercised | the **unreachable-branch** class (M07) and the **missing-fixture-shape** class (M08). M08 is routed to r98 as a selftest case (`VARIANTS` set `N01,N03`); the frozen selftest tally stays 12/12 (amendment A5) | `w1/MutRegistry/report.md` §3, §5, §6 |
| forgers / doctors (content-only) | 6 content-only cell doctors on the pinned base `f48d1642`: `default 12.9.4`, `(88 fixtures`, `roster 99 (`, `FAMILY_ROSTER, 99,`, `--selftest` (29 cases`, `r96 VARIANTS N01-N05` | **0 survived** — the doctored revision reads `status FAIL`, exactly six `RC-VALUE-MISMATCH` findings, one per doctor, each naming its row; the coverage gate on the same revision reads `PASS 154/154 findings 0` (blindness confirmed) | the **content-only doctor** class; the derivation is genuinely re-derived, not a constant — forcing the derivation to a constant flips the same tree FAIL → PASS | `w1/ExecRegistryContent/report.md` §3 (6 findings, coverage PASS 154/154, diff is SKILL.md-only); `w1/ReviewRegistryContent/receipts/02a-*`; `w1/CriticClaims/11-*`, `12-*`; `w1/MutRegistry/report.md` §3 (baseline doctored leg: FAIL 6) |
| forgers / doctors (in-scope limits) | 4 further doctors by `w1/ReviewRegistryContent`: (a) a covered cell, (b) an **uncovered** cell of a bound row, (c) a tool **and** its cell doctored together, (d) a `selftest_total` binding whose tool prints a tally without running cases | (a) **killed** — FAIL, exactly one `RC-VALUE-MISMATCH` naming the row. (b) **SURVIVED** — only seven cells are bound; the other 147 rows and the other cells of the four bound rows stay presence-only. (c) **SURVIVED** — the checker compares committed cell text to committed tool bytes at the *same* revision and cannot see a consistent dual edit. (d) **SURVIVED** — the tally binding parses a printed `PASS N/M` line and does not execute the cases | the **scope** class: what the checker binds is exactly what it binds, and the three named gaps (b, c, d) are the C2 claim's own declared limits, confirmed as real by measurement rather than asserted (amendment A4) | `w1/ReviewRegistryContent/report.md` §2(a)-(d) with receipts `02a-*` … `02d-*` |
| semantic probes | `w1/CriticClaims` §14 capture-slippage probes: doctored-first token, an extra roster member, a second schema literal | all **AGREE** with the expected id sets — no capture slippage; the declared limit (d) (tally-only binding) stands | — | `w1/CriticClaims/14-c2-semantic-probes.txt` |
| sibling overlap | 5-token sweep across 20 sibling repos (`registry-content`, `leading zero`, `leading-zero`, `9-digit`, `FAMILY_ROSTER`) + a sweep for sibling checkers that bind `SKILL.md` cells | **0 duplicate claims, 0 contradictions**; 5 sibling checkers found (kaidoku r100, tameshi r17/r80, kama r32, souji r29), all independent | — | `w1/ConnectorOverlap/report.md` §2 |

**Not reported at this seat's write time** (no seat report file existed under
`.ufo/waves/round-97/w1/`): **ScoutDrift**, **ScribeKnowledge**. (`w1/ReviewBattery/` had receipts
but no `report.md`; its numbers above are read from the receipts the seat wrote — `summaries.txt`
carries a per-arm, per-run table.)

**What the scoreboard says the next round should compare.** Two families of survivors recur across
both claims: (i) *a family with four members can be load-bearing on one and redundant on three*
(C1's two new families) and (ii) *a checker binds what it binds and nothing else* (C2's three named
gaps). Neither is a defect of a frozen target; both are places where a future round can add a
family or a binding. The counter-attack arms that beat the round were **not** one-clause bends —
they were an **uncertified field** and an **uncertified echo** (C1: 2 of 5 own gates survived) and
an **unreachable branch** plus a **missing fixture shape** (C2: 2 of 8 mutants survived). A next
round that fields only more bends would not test those: **the bends all died (0 of 2 survived), and
the partially-wrong gates all lived (2 of 5).** The same shape appears on both claims — a check that
binds one *observable* consequence of a behaviour leaves every other consequence of the same
behaviour uncaught. The lesson for r98: name the uncertified consequence in the claim's Limits
sentence, not only in the ledger.

---

## Routed

| r96 routed item (from `corpus/lessons/round-96-verifier-spotcheck.md`) | r97 treatment | evidence |
|---|---|---|
| **1 — the r96 untracked receipt** `.ufo/waves/round-96/after/registry-final.json` (`??` status in the lane repo at r96 close) | **closed.** The receipt is tracked at the r97 freeze: `git ls-tree -r a57e88cd --name-only \| grep 'round-96/after/registry-final.json'` → the path is present; `git show a57e88cd:.ufo/waves/round-96/after/registry-final.json` → `{"status":"PASS","counts":{"findings":0,"missing":0,"registered":154,…},"revision":"c67861483ad64491954fdcfd2003189b2dfad8b9"}`. At the pre-round tip `f48d1642` it was *not* tracked, so the round-97 freeze commit is where the leftover was picked up. | `git ls-tree` / `git show` above; the r97 freeze commit body (`round-97: freeze — … r96 leftover receipt`) |
| **2 — the Y-family docstring's false era sentence** (the r96 spot-check's own defect 2; "Lane owes: a docstring correction with its own manifest") | **closed, in place, in the live instrument.** `tools/limine-pin-battery-r97.py`'s `fam_refusal_versions_9digit_y` docstring carries the `LIMIT (r96 CriticClaims F-4, corrected here in r97)` paragraph stating what the family does not test, and the **live** `tools/limine-pin-battery-r96.py` was corrected in place with the same paragraph plus its manifest relation (the L1 took route (b) of the three `w1/ScoutSources` offered): `grep -c 'answers era B for' tools/limine-pin-battery-r96.py` → **0**, `grep -c 'LIMIT (r96 CriticClaims' …` → **1**. Family and expectation unchanged in both files; the frozen do-nothing control copy still hashes `f06d90ae…`, so C1's do-nothing leg is untouched. **The L1 must record the manifest relation:** the live r96 battery moved `f06d90ae…` → `0d98b5bd…`, so `.ufo/waves/round-96/before/instruments.sha256` no longer holds for that file in the worktree (its scored bytes are re-derivable at `f48d1642:tools/limine-pin-battery-r96.py`), and C1's do-nothing byte-identity clause should be stated as bound to the **control copy** rather than to the live file. | `ScribeLesson/receipts/10-r96-battery-in-place-correction.txt` (the diff, both hashes, both greps, the r96 manifest check); `ScribeLesson/receipts/06-mistake-redgreen.txt` (red/green pair at the two revisions) |
| **3 — the same correction, carried** (the spot-check's defect 3 duplicates defect 2) | **closed with defect 2.** After the in-place correction the sweep finds **no** file outside `.ufo/waves/` that asserts the false claim: `grep -rn 'answers era B for' . --include='*.py' --include='*.md' \| grep -v '^\./\.ufo/waves/'` → **1** hit, and that one hit is the r97 lesson's own table row quoting the withdrawn sentence in order to report it (a mention, not an assertion); 21 files inside `.ufo/waves/` carry it as historical r96/r97 wave evidence, never rewritten. Where the corpus discusses the sentence it states the corrected version (`corpus/knowledge/limine-bound-per-component-r96.md:60`, `corpus/lessons/round-96.md:79`). | `ScribeLesson/receipts/10-r96-battery-in-place-correction.txt` (the sweep counts); `w1/ScoutSources/report.md` §3 (the 17-hit sweep that first found the residual) |

### Also routed out of this round (not r96 items; raised by this wave)

| item | treatment | evidence |
|---|---|---|
| the S392 row's two cited offsets are character offsets presented as byte offsets | **open, for the L1** — restate as bytes `153202` / `157767`, or state the unit. Same class as the r96 S390→S391 supersession. | `ScribeLesson/receipts/05-gate-quote-bytes.txt`; `w1/ScoutSources/report.md` §1c |
| the r97 battery's own LZ docstring sentence names the wrong discriminating member | **routed to r98** as a successor docstring correction (amendment A6); the frozen bytes are not edited this round. | `w1/CriticClaims/report.md` §C1 "Docstring defect"; `before/plan-amendments-r97.md` A6 |
| MutRegistry M08 — `derive_variant_span`'s comma branch is never exercised by any selftest fixture | **routed to r98** as a selftest case (a `VARIANTS` set `N01,N03`); frozen tally stays 12/12 (amendment A5). | `w1/MutRegistry/report.md` §5 (M08) |
| `before/fixtures/build-doctored-fixture.sh` changed in-tree under the frozen manifest during the wave | **narrowed, not repaired, by the L1**: amendment A1 states the recipe is not a scoring instrument, the corrected set is pinned in `before/instruments-r97-after-fixture-pin.sha256`, and the C2 void clause is evaluated on that file. At this seat's write time `sha256sum -c .ufo/waves/round-97/before/instruments.sha256` still reads **19 OK, 1 FAILED** (that line only); HEAD still carries the pinned bytes `c2ecf729…`, the worktree reads `e4cf82a0…`. | `ScribeLesson/receipts/09-manifest-at-write-time.txt`; `before/plan-amendments-r97.md` A1; `w1/ExecBend/report.md` "Observation routed to L1"; `w1/MutRegistry/report.md` §7 |
| the r96 do-nothing battery's `--usage-check` leg already samples leading zeros, so "the r96 battery is blind to the leading-zero class" holds at roster level only | **narrowed by amendment A3**: the roster readings stand as frozen; the report, knowledge entry, lesson and SCORECARD state the roster/instrument split. | `before/plan-amendments-r97.md` A3; `w1/ExecDoNothing/report.md` F1 |
| the coverage-blindness leg needs the pinned pre-round base (the freeze added three tools with no rows yet) | **narrowed by amendment A4**: the sentence is bound to the pinned base `f48d1642`; at the settled tip the gate reads `PASS 157/157`. | `before/plan-amendments-r97.md` A4; `w1/ReviewRegistryContent/report.md` Z-1 |

---

## Tooling

Nothing installed, upgraded or updated by this seat. Commands used: `git` (read-only: `show`,
`ls-tree`, `rev-parse`, `status`, `archive`, `diff` — no mutating git/jj command was run),
`bash`, `python3` (stdlib only), `curl`, `sha256sum`, `grep`, `cmp`, `sed`/`awk` only inside
pipelines. No `sudo`, no `pacman` transaction, no PATH-directory write, no host-state change.

## Scratch

Scratch root `/fast/scratch/hyaku/tsukuroi-r97/ScribeLesson` held the three fetched pins, the
read-only `git archive` extraction of the pre-round tree used for the census *before* leg, and the
intermediate census outputs. It is deleted before this seat yields; every byte cited above lives
under `.ufo/waves/round-97/w1/ScribeLesson/` (pins/ + receipts/ + this draft).

## Receipts (all written by this seat, under `.ufo/waves/round-97/w1/ScribeLesson/`)

| path | content |
|---|---|
| `pins/functions.html` | the round's new source, 331022 bytes, sha256 `d92580dd…` (byte-identical to ScoutSources' pin and to the L1's `after/gate/functions.html`) |
| `pins/stdtypes.html` | re-opened S389 page, 815447 bytes, sha256 `6bf2ce2b…` (byte-identical to the r96 pin) |
| `pins/sys315.html` | re-opened S391 page, 280632 bytes, sha256 `a7e00587…` (byte-identical to the r96 pin) |
| `pins/python1-man.html` | the rejected candidate, 41788 bytes, sha256 `11c40ea1…` |
| `receipts/01-gate-pins.sha256.txt` | digests of the four pins |
| `receipts/02-census-after.txt` | census **after** leg: command, full output, exit 0 |
| `receipts/03-census-before.txt` | census **before** leg: command, full output, exit 0, row counts |
| `receipts/04-sources-rows.txt` | before/after row counts with their commands, `git rev-parse HEAD`, `git status` |
| `receipts/05-gate-quote-bytes.txt` | the S392 offset-unit check: byte vs character reading, the true byte offsets, and the r96 contrast |
| `receipts/06-mistake-redgreen.txt` | the red/green pair for the Y-docstring mistake, the line-wrap caveat with the two discriminating forms, and the residual sweep |
| `receipts/07-gate-reject.txt` | the rejected candidate's fetch, digest, title and the zero-hit behaviour scan |
| `receipts/08-gate-reopens.txt` | the two re-open comparisons against the r96 pins |
| `receipts/09-manifest-at-write-time.txt` | `sha256sum -c` of the frozen manifest at write time (19 OK, 1 FAILED), HEAD vs worktree bytes of the drifted line |
| `round-97.md` | this draft |
