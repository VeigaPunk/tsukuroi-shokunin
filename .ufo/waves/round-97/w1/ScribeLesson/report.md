# ScribeLesson — round 97 wave w1 — the round lesson draft

Seat: **ScribeLesson**. Lane: `tsukuroi-shokunin` @ `a57e88cd57f30bae206d908b534508d9463bf734`
(the r97 freeze; `git rev-parse HEAD` agrees with `receipts/04-sources-rows.txt`). No claim rests on
this seat; this is the round-lesson draft and its receipts. Deliverable:
**`.ufo/waves/round-97/w1/ScribeLesson/round-97.md`** (the draft the L1 integrates).

Tools: stock `python3` (stdlib only), `git` (read-only), `bash`, `curl`, `sha256sum`, `grep`, `cmp`.
**Nothing installed, upgraded or updated** — no `pacman` transaction (host-wide pause), no `sudo`,
no PATH-directory write. Tool/version/channel/reason record: **no tool install was needed**, so there
is nothing to record beyond "none".

---

## 1. Pre-flight — the frozen instrument manifest

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-97/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r97.py: OK
tools/make-r97-bends.py: OK
tools/check-registry-content.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-97.md: OK
.ufo/waves/round-97/before/plan-frozen.md: OK
.ufo/waves/round-97/claims.json: OK
.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py: OK
.ufo/waves/round-97/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py: OK
.ufo/waves/round-97/before/controls/do-nothing-r96-calibration.py: OK
.ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py: OK
.ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py: OK
.ufo/waves/round-97/before/registry-baseline.json: OK
.ufo/waves/round-97/before/fixtures/doctored.diff: OK
.ufo/waves/round-97/before/fixtures/doctored-recipe.txt: OK
.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh: FAILED
.ufo/waves/round-97/before/dev/run-dev.sh: OK
sha256sum: WARNING: 1 computed checksum(s) did NOT match
```

Receipt: `receipts/09-manifest-at-write-time.txt`. **PASS on 19 of 20 lines; the one FAILED line is
reported raw and not smoothed.** It is *not* an instrument the claims read: it is the C2
doctored-fixture **recipe**, mutated in-tree by another writer during the wave (see §6). The five
frozen instruments the claims score all read OK. The L1 narrowed the void clause onto a re-pinned
manifest (`before/instruments-r97-after-fixture-pin.sha256`) via amendment A1.

The same check at the **start** of this seat read **20 OK, 0 FAILED** — the drift appeared between
08:48 and 08:52 local, i.e. during the wave, after the freeze commit.

---

## 2. Gate — the round's candidate sources

### 2a. The new Python-docs page (the round's source)

```
$ cd /fast/scratch/hyaku/tsukuroi-r97/ScribeLesson
$ curl -sSL -o functions.html -w 'HTTP=%{http_code} BYTES=%{size_download} URL=%{url_effective}\n' \
    'https://docs.python.org/3/library/functions.html'
HTTP=200 BYTES=331022 URL=https://docs.python.org/3/builtins/functions.html
$ sha256sum functions.html
d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7  functions.html
```

A first fetch **without** `-L` returned `HTTP=301`, 162 bytes — the redirect to `/3/builtins/` is
real and is recorded, not hidden.

**Reuse of ScoutSources' receipt, re-verified independently.** The sibling seat's pin
`w1/ScoutSources/pins/int-functions.html` and this seat's fetch are **byte-identical**:
`cmp .ufo/waves/round-97/after/gate/functions.html .ufo/waves/round-97/w1/ScribeLesson/pins/functions.html`
→ identical, and the same sha256 `d92580dd…` and byte count 331022 appear in ScoutSources'
`receipts/fetches.json`. The L1's own pin under `.ufo/waves/round-97/after/gate/functions.html` is
the same bytes.

**The quote, re-verified at the cited byte with `python3 -c`** (receipt
`receipts/05-gate-quote-bytes.txt`):

```
$ python3 -c "b=open('pins/functions.html','rb').read(); …"
pin bytes 331022 sha256 d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7

## A) read as BYTE offsets (the SOURCES.md convention)
byte 157622 cited 'have leading zeros, be surrounded by whitespace,' -> ABSENT  b'e"><span class="pre">+</span></code> or <code cl'
byte 159164 cited 'also disallows leading zeros:'                  -> ABSENT  b'ers"><span class="std std-ref'
byte 153028 cited 'id="int"'                                       -> ABSENT  b'an class'

## B) the TRUE byte offsets of the same three sites in the same pinned file
byte 157767 b'have leading zeros, be surrounded by whitespace,'
byte 159310 b'also disallows leading zeros:'
byte 153202 b'id="int"'

## C) the same three offsets read as CHARACTER offsets (utf-8 decoded) - they land exactly
char 157622 'have leading zeros, be surrounded by whitespace,'
char 159159 'also disallows leading zeros:'
char 153058 'id="int"'

## D) contrast: the r96 row S391 cites byte 157525 on the sys pin and lands exactly
byte 157525 -> b'id="sys.int_info.default_max_str_digits">\n<span cl'
```

**FINDING (reported raw).** The landed S392 row reads *"`int` heading (`id="int"` at byte 153028) …
quoted phrase at byte 157622"*; read as **bytes**, neither offset lands on the cited text. Read as
**character** offsets of the utf-8-decoded page, both land (the `id="int"` attribute itself is at
char 153058; the row's 153028 is the start of the `<dt … id="int">` element carrying it). The r96
rows on the same table **are** byte offsets and land exactly when read as bytes (§D). So S392's
offsets are character offsets presented as byte offsets — the r96 S390→S391 defect class recurring
one row later, on the very table C2's new checker re-derives cell values from. **Not edited by this
seat** (`corpus/` is out of scope); routed to the L1 as a decision: restate as bytes `153202` /
`157767`, or state the unit as characters.

### 2b. The two r96 re-opens

```
$ curl -sSL -o stdtypes.html 'https://docs.python.org/3/library/stdtypes.html'   # HTTP=200, 815447 bytes
$ curl -sSL -o sys315.html  'https://docs.python.org/3.15/library/sys.html'      # HTTP=200, 280632 bytes
```

Receipt `receipts/08-gate-reopens.txt`:

| row | file | bytes | sha256 | r96 pin | verdict |
|---|---|---|---|---|---|
| S389 re-open | `pins/stdtypes.html` | 815447 | `6bf2ce2ba49d30974485266d70aecd4c4eb89334eb73367f3f99bfa036c7e9a8` | `6bf2ce2b…` | **BYTE-IDENTICAL, no drift → admit** |
| S391 re-open | `pins/sys315.html` | 280632 | `a7e005875e4152bcccaf44b9a834c123cc69bf7b66b3b8398aef91cffe77dd0e` | `a7e00587…` | **BYTE-IDENTICAL, no drift → admit** |

### 2c. The rejected candidate

```
$ curl -sSL -o pins/python1-man.html -w 'EFFECTIVE=%{url_effective} HTTP=%{http_code} BYTES=%{size_download}' \
    'https://man.archlinux.org/man/python.1'
EFFECTIVE=https://man.archlinux.org/man/python3.14.1.en HTTP=200 BYTES=41788
sha256 11c40ea191395fda4991cd254305162603edf2a0437bcc5341691201ccca10c7
title   python3.14(1) — Arch manual pages
```

Receipt `receipts/07-gate-reject.txt`: occurrences of "leading zero" **0**, "int(" **0**,
"base 10" **0**, "radix" **0** in the page text (the single "decimal" hit is `PYTHONHASHSEED`'s
range). **REJECT** — the interpreter's CLI manual states no behaviour about `int()`'s string form, so
it cannot ground C1's family or S392's claim; it is also a version alias (`python.1` → the current
`python3.14.1` build), i.e. a moving target rather than a pinned locator.

**Gate verdict: 3 admits (S392 new, S389 re-open, S391 re-open), 1 reject.**

---

## 3. Census — before and after

Frozen command: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`.

**Before leg** (the pre-round tip `f48d1642` tree, extracted read-only with `git archive f48d1642 |
tar -x -C <scratch>/before-fleet/tsukuroi-shokunin`, with the fleet's `shokunin.conf` copied in so
the lane resolves):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <scratch>/before-fleet tsukuroi
tsukuroi	W04	S322 duplicate url raw.githubusercontent.com/systemd/systemd/v262/src/core/transaction.c across scopes
… (57 W04 lines) …
tsukuroi	W01	S381 tierC mined used-by=corpus/knowledge/limine-r92-oracle-isolation.md, corpus/lessons/round-92.md
tsukuroi	ok	<scratch>/before-fleet/tsukuroi-shokunin/corpus/SOURCES.md
exit=0
```

**After leg** (the live fleet root, with the L1's row S392 present in the worktree):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
… 59 lines: 57 × W04 + 1 × W01 + 1 × ok …
exit=0
```

Receipts `receipts/03-census-before.txt` (before) and `receipts/02-census-after.txt` (after);
row counts in `receipts/04-sources-rows.txt`:

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md                              -> 392   # AFTER
$ git show f48d1642:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'           -> 391   # BEFORE
$ git rev-parse HEAD                                                                   -> a57e88cd57f30bae206d908b534508d9463bf734
$ git status --porcelain -- corpus/SOURCES.md SKILL.md
 M SKILL.md
 M corpus/SOURCES.md
```

**PASS on both legs**: exit 0, 0 E findings, 57 W04 + 1 W01 on each; **391 → 392 rows** (one A row
added, S392; no row touched in place).

---

## 4. Mistakes — the mined mistake, with its red/green pair

**Mined: (a) r96's Y-family docstring asserted an era behaviour the family does not test.**

- **class:** instrument text vs the behaviour the family actually tests.
- **evidence pointer:** r96 `w1/CriticClaims/report.md` §1 **F-4**, with the measurement at
  `w1/CriticClaims/receipts/era-reader-mutant.txt` (`REFUSAL-VERSIONS-9DIGIT-Y` all 4 cases
  `case_ok=true`; `EXPLICIT-VERSION-ERA`'s `12.9.4` case `case_ok=false`, `got era "12.9.5+"`,
  want `prompt`).
- **captured-by:** **QUALITY 122** (`corpus/QUALITY.md:240`, R85-MUST-HAS-CONTROL) — *"a declared
  discrimination property names its near-miss control"* — which the docstring was never checked
  against.
- **fix:** the r97 docstring's `LIMIT` paragraph stating what the family does **not** test.

**Red/green pair** (receipt `receipts/06-mistake-redgreen.txt`; red `f48d1642`, green `a57e88cd`):

```
$ git show f48d1642:tools/limine-pin-battery-r96.py | grep -c 'answers era B for'       -> 1   # RED
$ git show a57e88cd:tools/limine-pin-battery-r97.py | grep -c 'answers era B for'       -> 0   # GREEN
$ git show f48d1642:tools/limine-pin-battery-r96.py | grep -c 'LIMIT (r96 CriticClaims' -> 0   # RED
$ git show a57e88cd:tools/limine-pin-battery-r97.py | grep -c 'LIMIT (r96 CriticClaims' -> 1   # GREEN
```

**The item's literal command does not discriminate, and the run wins.** The item named
`grep -c 'LIMIT (r96 CriticClaims F-4'` as the green signal; read literally it returns **0 on both
revisions**, because the sentence is line-wrapped in the source — the raw bytes are
`LIMIT (r96 CriticClaims\n    F-4, corrected here in r97): …`. The instrument was **not** edited and
**no retry-to-pass** was performed. The two forms that do discriminate (both in the receipt): the
single-line prefix above (0 → 1) and the cross-line `grep -cPzo 'LIMIT \(r96 CriticClaims\s+F-4'`
(0 → 1). **Lesson for r98: a red/green check on a line-wrapped sentence must anchor on a token that
is not split across lines, or it reads "0 = pass" on both sides.**

**Residual — closed in place by the L1 during the wave.** When this seat first measured it, the false
sentence still stood in the live, registry-listed `tools/limine-pin-battery-r96.py:1776`, because
C1's do-nothing clause binds the control copy as *"byte-identical to the r96 landed bytes"*. ScoutSources
routed three options (`w1/ScoutSources/report.md` §3); the L1 took the in-place option. Re-read at
write time (receipt `receipts/10-r96-battery-in-place-correction.txt`):

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
$ sha256sum -c .ufo/waves/round-96/before/instruments.sha256
tools/limine-pin-battery-r96.py: FAILED
$ grep -rn 'answers era B for' . --include='*.py' --include='*.md' | grep -v '^\./\.ufo/waves/' | wc -l -> 1
```

**PASS on the correction; two consequences the L1 must record:** (i) the edit is docstring-only, so
the frozen do-nothing control copy still hashes `f06d90ae…` and C1's do-nothing leg is untouched;
(ii) the **live** r96 battery moved `f06d90ae…` → `0d98b5bd…`, so
`.ufo/waves/round-96/before/instruments.sha256` no longer holds for that file in the worktree (its
scored bytes stay re-derivable at `f48d1642:tools/limine-pin-battery-r96.py`, which the new docstring
itself names), and C1's do-nothing byte-identity clause should be stated as bound to the **control
copy** rather than to the live file. The single remaining hit outside `.ufo/waves/` is the r97
lesson's own table row quoting the withdrawn sentence in order to report it — a mention, not an
assertion.

---

## 5. Counter-attack scoreboard — what was fielded, what survived, which class beat it

Filled from the seat reports that exist at this seat's write time; seats with no report are named
`not reported`. Every cell names the seat and the receipt it was read from.

### C1 (depth 8)

| arm | fielded | survived | class that beat it | source seat |
|---|---|---|---|---|
| one-clause bends | 2 (`N05-z-cap-8`, `N06-leading-zero-reject`) | **0** — N05 `103/105`, `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 6 error rows/run (4 Z + 2 LZ); N06 `104/105`, `[LEADING-ZERO-NORMALIZE]`, 4 error rows/run; all rc-64 refusals; canonical **and** `git clone --shared`, 3/3 runs each | the one-clause bend class | `ExecBend` §4-5; re-counted by `ReviewBattery/counted-N05-count.txt`, `counted-N06-count.txt` |
| own scratch gates | 5 (`attack1-eraA-pin`, `attack1-eraA-field`, `attack2-echo-norm`, `attack3-refuse-allzero`, `attack4-constant`) | **2 survived** — `attack1-eraA-field` and `attack2-echo-norm` both `105/105 met` ×3. **3 killed** — `attack1-eraA-pin` `104/105 [REFUSAL-VERSIONS-9DIGIT-Z]`; `attack3-refuse-allzero` `104/105 [LEADING-ZERO-NORMALIZE]` with 1 rc-64 error row; `attack4-constant` `0/105` | the **uncertified-field** and **uncertified-echo** classes — the two new families bind acceptance and the pin consequence, not the `visibility_era` string and not the echoed spelling | `ReviewBattery.md` §4 and §5 (two `falsifies-wording` ledger rows); receipts `attack-*.txt`, `summaries.txt` |
| load-bearing-ness | 2 own gates (Z-era-blind, LZ-text-compare) | both **killed** (3× `104/105`, exactly one family, 0 error rows) — and each kills only **one** member | the **acceptance-redundancy** class (4 members, 1 load-bearing) | `CriticClaims` `05-zera-*`, `06-lztext-*`, `15-scope-quant.txt` |
| do-nothing blindness | the r96 battery on the landed gate and both bends, 9 runs | the control **survives** the new families at roster level (`103/103 met`, 0 error rows, ×3 each) — the intended receipt. But at *instrument* level it is **not** blind to the leading-zero class: its `--usage-check` sends `12.09.4` and `00.00.00` (`want_rc 0`) and reads `unmet` on `N06` | the **roster-level / instrument-level split** (amendment A3) | `ExecDoNothing` §2-4 (F1) |

### C2 (freshness 9)

| arm | fielded | survived | class that beat it | source seat |
|---|---|---|---|---|
| one-fault mutants | 8 (M01-M08) | **2 survived** — M07 (the `--revision` ancestor check, unreachable from `--selftest` by construction) and M08 (`derive_variant_span` compares only the first label — no fixture carries a non-contiguous `VARIANTS` set). **6 killed** | the **unreachable-branch** and **missing-fixture-shape** classes (M08 routed to r98 as a selftest case; amendment A5) | `MutRegistry` §3, §5, §6 |
| content-only doctors | 6 on the pinned base `f48d1642` | **0 survived** — the doctored revision reads `status FAIL` with exactly six `RC-VALUE-MISMATCH`, one per doctor, each naming its row; the coverage gate on the same revision reads `PASS 154/154 findings 0` | the content-only doctor class; the derivation is genuinely re-derived (forcing it constant flips the same tree FAIL → PASS) | `ExecRegistryContent` §3; `ReviewRegistryContent/receipts/02a-*`; `CriticClaims` `11-*`, `12-*` |
| in-scope limit doctors | 4 (`w1/ReviewRegistryContent`): covered cell, **uncovered** cell, tool **and** cell together, a printed tally with no cases run | (a) **killed** — FAIL, one `RC-VALUE-MISMATCH` naming the row. (b)(c)(d) **survived** | the **scope** class — the checker binds exactly seven cells; the three gaps are C2's own declared limits, now measured rather than asserted (amendment A4) | `ReviewRegistryContent` §2(a)-(d), receipts `02a-*`…`02d-*` |
| semantic probes | 3 (doctored-first token, extra roster member, second schema literal) | none slipped — all AGREE with the expected id sets | — | `CriticClaims` `14-c2-semantic-probes.txt` |
| sibling overlap | 5-token sweep across 20 sibling repos + a sweep for sibling cell-binding checkers | **0 duplicate claims, 0 contradictions**; 5 sibling checkers found, all independent | — | `ConnectorOverlap` §2 |

**Not reported at this seat's write time:** **ScoutDrift**, **ScribeKnowledge** (no seat report file
under `.ufo/waves/round-97/w1/`). Every other seat's report existed and was read.

---

## 6. Routed — the r96 spot-check's three defects, and this round's treatment

| r96 routed item | r97 treatment | evidence |
|---|---|---|
| **1** — the untracked receipt `.ufo/waves/round-96/after/registry-final.json` | **closed.** Tracked at the r97 freeze: `git ls-tree -r a57e88cd --name-only \| grep 'round-96/after/registry-final.json'` → present; `git show a57e88cd:.ufo/waves/round-96/after/registry-final.json` → `{"status":"PASS","counts":{"findings":0,"missing":0,"registered":154,…},"revision":"c67861483ad64491954fdcfd2003189b2dfad8b9"}`. At the pre-round tip `f48d1642` it was **not** tracked. | `git ls-tree` / `git show` (read-only) |
| **2** — the Y-family docstring's false era sentence | **closed in place** by the L1 during the wave (§4 above), with the manifest relation to record and C1's do-nothing clause to be stated against the control copy. | `receipts/10-r96-battery-in-place-correction.txt`; `receipts/06-mistake-redgreen.txt` |
| **3** — the same correction, carried | **closed with 2.** `grep -rn 'answers era B for' . --include='*.py' --include='*.md' \| grep -v '^\./\.ufo/waves/'` → **1** hit, and it is the r97 lesson's own row quoting the withdrawn sentence to report it. 21 files inside `.ufo/waves/` carry it as historical wave evidence, never rewritten. The corpus states the corrected version (`corpus/knowledge/limine-bound-per-component-r96.md:60`, `corpus/lessons/round-96.md:79`). | `receipts/10-r96-battery-in-place-correction.txt`; `w1/ScoutSources/report.md` §3 |

**Also routed out of this round (raised by the wave, not r96 items):**

- the S392 row's two offsets are character offsets presented as byte offsets → **open, for the L1**
  (§2a);
- the r97 battery's own LZ docstring sentence names the wrong discriminating member → **routed to
  r98** as a successor docstring correction (amendment A6);
- MutRegistry M08 (`derive_variant_span`'s comma branch never exercised) → **routed to r98** as a
  selftest case (amendment A5);
- `before/fixtures/build-doctored-fixture.sh` drifted under the frozen manifest during the wave →
  **narrowed by amendment A1** (the recipe is not a scoring instrument; the void clause is
  evaluated on `before/instruments-r97-after-fixture-pin.sha256`);
- the r96 do-nothing battery's `--usage-check` already samples leading zeros → **narrowed by
  amendment A3** (the blindness is a roster-level statement);
- the coverage-blindness leg needs the pinned pre-round base → **narrowed by amendment A4**.

---

## 7. PASS/FAIL per expected line

| expected line | verdict | evidence |
|---|---|---|
| Read the five required inputs before writing (claims.json, plans/round-97.md, instruments.sha256, r96 spot-check lesson, QUALITY 139-140) | **PASS** | all five read at the start of the seat; QUALITY 139/140 read raw at `corpus/QUALITY.md:345,348` |
| Verify the frozen manifest before citing a measurement | **PASS (19/20; 1 FAILED reported raw)** | `receipts/09-manifest-at-write-time.txt`; the failed line is the C2 recipe, not a scoring instrument |
| Gate: the round's new Python-docs page — URL, status, bytes, sha256, quote, byte offset | **PASS** | `receipts/01-gate-pins.sha256.txt`, `receipts/05-gate-quote-bytes.txt`; sha256 `d92580dd…`, 331022 bytes, byte-identical to ScoutSources' pin and to the L1's pin |
| Gate: re-verify the quote is present **at the cited byte** yourself with `python3 -c` | **PASS, with a finding** | the quote is **ABSENT** at the row's cited byte 157622 and **PRESENT** at byte 157767; the cited numbers are character offsets — reported raw, not smoothed (`receipts/05-gate-quote-bytes.txt`) |
| Gate: S389 and S391 re-opens compared with the r96 pins | **PASS** | both byte-identical, no drift (`receipts/08-gate-reopens.txt`) |
| Gate: at least one admit and one reject, each with its reason | **PASS** | 3 admits (S392, S389, S391) and 1 reject (`man.archlinux.org/man/python.1`, zero behaviour hits) — `receipts/07-gate-reject.txt` |
| Census: the frozen command run on both legs, with both exits and the row counts | **PASS** | exit 0 / 391 rows before, exit 0 / 392 rows after (`receipts/02-census-after.txt`, `03-census-before.txt`, `04-sources-rows.txt`) |
| Mistakes: one mistake with class · evidence pointer · captured-by · fix | **PASS** | R97-Y-DOCSTRING-ERA: class = instrument text vs measured behaviour; pointer = r96 `w1/CriticClaims` F-4 + `receipts/era-reader-mutant.txt`; captured-by = QUALITY 122 (`corpus/QUALITY.md:240`); fix = the r97 `LIMIT` paragraph |
| Mistakes: a demonstrated red/green pair | **PASS, with the item's literal command reported as non-discriminating** | `grep -c 'answers era B for'` 1 → 0; `grep -c 'LIMIT (r96 CriticClaims'` 0 → 1; the item's one-line `…F-4` form reads 0 on both sides (line-wrap) and is reported raw (`receipts/06-mistake-redgreen.txt`) |
| Counter-attack scoreboard: what the wave fielded per claim, how many survived, which class beat it, filled from the seat reports that exist, missing seats named `not reported` | **PASS** | §5; 12 seat reports read, 2 seats named `not reported` (ScoutDrift, ScribeKnowledge) |
| Routed: r96's three routed defects and this round's treatment | **PASS** | §6 |
| Every number carries a command | **PASS** | every figure in `round-97.md` names the command that produced it and the receipt under this seat dir |
| Write only under the seat dir + scratch; no mutating git/jj; no `sudo`; no tool install | **PASS** | writes confined to `.ufo/waves/round-97/w1/ScribeLesson/`; git used read-only (`show`, `ls-tree`, `rev-parse`, `status`, `diff`, `archive`); scratch deleted before yield |
| Deliverable: `<SeatDir>/round-97.md` with `## Gate`, `## Mistakes`, the census block and the counter-attack scoreboard | **PASS** | `round-97.md` — all four sections present, plus `## Routed`, tooling and receipt sections |

---

## 8. Receipts (all written by this seat, under `.ufo/waves/round-97/w1/ScribeLesson/`)

| path | content |
|---|---|
| `pins/functions.html` | the round's new source, 331022 bytes, sha256 `d92580dd…` (byte-identical to ScoutSources' pin and to the L1's `after/gate/functions.html`) |
| `pins/stdtypes.html` | re-opened S389 page, 815447 bytes, sha256 `6bf2ce2b…` |
| `pins/sys315.html` | re-opened S391 page, 280632 bytes, sha256 `a7e00587…` |
| `pins/python1-man.html` | the rejected candidate, 41788 bytes, sha256 `11c40ea1…` |
| `receipts/01-gate-pins.sha256.txt` | digests of the four pins |
| `receipts/02-census-after.txt` | census **after** leg: command, full output, exit 0 |
| `receipts/03-census-before.txt` | census **before** leg: command, full output, exit 0, row counts |
| `receipts/04-sources-rows.txt` | before/after row counts with their commands, `git rev-parse HEAD`, `git status` |
| `receipts/05-gate-quote-bytes.txt` | the S392 offset-unit check: byte vs character reading, the true byte offsets, the r96 contrast |
| `receipts/06-mistake-redgreen.txt` | the red/green pair, the line-wrap caveat with both discriminating forms, and the first-pass residual sweep |
| `receipts/07-gate-reject.txt` | the rejected candidate's fetch, digest, title and the zero-hit behaviour scan |
| `receipts/08-gate-reopens.txt` | the two re-open comparisons against the r96 pins |
| `receipts/09-manifest-at-write-time.txt` | `sha256sum -c` of the frozen manifest at write time (19 OK, 1 FAILED), HEAD vs worktree bytes of the drifted line |
| `receipts/10-r96-battery-in-place-correction.txt` | the L1's in-place docstring correction: the diff, both hashes, both greps, the r96 manifest check, the residual sweep count |
| `round-97.md` | **the lesson draft** (the deliverable) |
| `report.md` | this report |

Scratch root `/fast/scratch/hyaku/tsukuroi-r97/ScribeLesson` (the fetched pins, the read-only
`git archive` extraction used for the census *before* leg, the intermediate census outputs) is
deleted before this seat yields; every byte cited above lives under the seat dir.

{"seat":"ScribeLesson","verdict":"findings","notes":"Lesson draft at .ufo/waves/round-97/w1/ScribeLesson/round-97.md with ## Gate (3 admits, 1 reject, all self-fetched and re-verified), ## Mistakes (R97-Y-DOCSTRING-ERA: class, r96 CriticClaims F-4 pointer, QUALITY 122 capture, r97 LIMIT-paragraph fix, demonstrated red/green pair 1->0 and 0->1), census block (exit 0 / 391 rows before at f48d1642, exit 0 / 392 rows after with the L1's S392), counter-attack scoreboard (C1: 2 bends 0 survived, 5 own gates 2 survived, do-nothing roster-level blindness with the instrument-level qualification; C2: 8 mutants 2 survived, 6 content doctors 0 survived, 3 named scope limits measured), and ## Routed (r96's three defects closed, with the manifest relation and the do-nothing clause binding to be recorded). FINDINGS: (1) the landed S392 row's two offsets (153028, 157622) are CHARACTER offsets presented as byte offsets - the quote is ABSENT at byte 157622 and PRESENT at byte 157767, the anchor at byte 153202; routed to the L1, not edited. (2) The item's literal red/green command 'grep -c \"LIMIT (r96 CriticClaims F-4\"' reads 0 on both revisions because the sentence is line-wrapped - reported raw, with the two forms that do discriminate. (3) The r96 battery was corrected IN PLACE by the L1 mid-wave, moving it f06d90ae->0d98b5bd and breaking .ufo/waves/round-96/before/instruments.sha256 for that file; the frozen do-nothing control copy is untouched, so C1's do-nothing leg stands. (4) At write time sha256sum -c of the r97 manifest reads 19 OK / 1 FAILED - the C2 doctored-fixture recipe, narrowed by amendment A1. (5) The r97 battery's own LZ docstring names the wrong discriminating member (amendment A6, routed to r98). 2 seats not reported at write time: ScoutDrift, ScribeKnowledge. No tool installed; no mutating git/jj; scratch deleted."}
